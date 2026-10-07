---
name: concurrency
description: Preserve observable concurrency, shared state, ordering, and resource-lifecycle semantics when converting concurrent code.
---

# 并发场景

本 Skill 仅在源码实际创建或协作使用多个线程/任务时加载。它定义应盘点的行为，不替代 source OS → target OS 的线程 API 映射，也不证明无数据竞争。

## 转换前盘点

- 线程/任务创建点、入口函数签名、参数所有权、启动失败路径与线程数量限制；
- 共享状态的读写者、同步原语、状态机、发布/完成信号与主线程观察时机；
- 每个线程拥有的 socket、缓冲区、文件、锁和句柄，以及成功、失败、取消、退出时的清理顺序；
- join/wait、detach、句柄回收与进程退出路径；
- 可观察的并发拓扑、请求顺序、超时和背压行为。

## 转换约束

- 保持原有并发模型和可观察顺序；不要把每连接线程静默改成线程池、异步 I/O 或串行处理。
- API 名称相似不代表生命周期等价。分别核对线程句柄与线程 ID、join/wait、结果值、取消/强制终止及资源回收。
- 发现普通共享变量被多个线程并发访问而没有同步时，标记为源代码既有风险；不要把 `volatile` 当作同步，也不要在未经授权时静默重构。
- `TerminateThread`、`pthread_cancel` 等强制取消不能视作可互换的常规清理路径；确认代码是否真正调用，再归入行为地图。
- 跨段转换时，将共享状态结构、入口签名、所有权及终止协议作为跨单元契约。
- Worker 计数/等待必须覆盖**实际处理任务的 worker**，不能只等待接收循环。接收循环结束不代表已派发的连接/任务已经完成。
- 保留正常关闭、取消和错误退出三种路径的差异：正常关闭按源语义排空；取消时决定丢弃还是完成；无论哪种路径，读取共享结果前都要等待实际 worker。
- 不要把 WaitGroup/计数器机械映射成 join 循环。先确认 Add/Wait 的配对时机、生产者是否还会新增任务、worker 是否可能阻塞在 I/O 或队列上；不明时记录未映射点。
- 如果 worker 持有 socket、文件或锁，终止协议必须说明由谁释放、何时释放，以及主线程何时可以读取结果或退出进程。

### L2-CONC-01 关闭/取消对阻塞调用的唤醒语义必须逐平台核对

**触发条件**：源码在关闭、取消或超时路径上依赖“关闭某个资源会唤醒阻塞在它上面的调用”，或依赖阻塞调用返回后的错误取值。


**义务**：

1. **裸关闭不保证唤醒**：关闭一个 fd/句柄后，阻塞在 `accept`/`recv`/`poll`/`select` 上的线程**不保证**被唤醒，也不保证返回可区分的错误。要保留源的“取消即唤醒”行为，必须显式选择平台提供的取消机制（如 `shutdown()` 于套接字、关闭事件对象、条件变量广播），并把该选择写进终止协议。
2. **禁用“API 名称相似即等价”**：`close`/`CloseHandle`/`Close`/`.Dispose()`/`Cancel()` 的唤醒效果各不相同，不得按名字推断；判定依据必须是目标平台/运行时的官方文档。
3. **fd 可被复用后重复关闭会误伤新资源**：关闭后 fd 编号可被后续 `open`/`socket` 复用；“谁关闭、关闭几次”必须唯一化（见 L2-CONC-02）。在唤醒尚未返回时重复关闭同一编号，可能关闭到别的线程刚打开的新资源。
4. **last-error 是线程局部的**：源在失败后**同线程立即**读取 `GetLastError()`/`errno`；目标若把失败调用包进其他调用、跨线程读取或延迟读取，取值已被覆盖。错误必须在产生点捕获并显式传递。
5. **回调线程上没有运行时上下文**：由外部子系统在**其自建的原生线程**上回调目标语言的代码时，依赖线程静态（TLS）的运行上下文可能为空。典型：Windows SCM 在自建线程回调 `ServiceMain`/`ControlHandler`，而 PowerShell `ScriptBlock` 需要 runspace，`Runspace.DefaultRunspace` 是线程静态的，在那些线程上为 null。
6. **不要把续体/事件式并发改成轮询**：`ContinueWith`/回调/事件等由运行时唤醒的形式改为轮询线程，会改变可观察的唤醒时机、资源占用与取消响应；除非源本身就是轮询，否则不得替换。

**错误机械替换反例**：

```text
源（Go）：listener.Close() 使阻塞在 Accept() 的 goroutine 立即返回并结束循环。
目标（C++，错误）：仅 close(listen_fd) 后仍 join 阻塞在 accept() 的线程 → 永久挂起，
                  或该 fd 已被复用，close 命中了另一线程的新连接。
正确：按目标平台文档选择能唤醒 accept 的机制（先 shutdown 再 close），
      并保证 fd 生命周期唯一、唤醒后再 join。
```

**不适用条件**：源码本身就是轮询模型（循环 `sleep` + 标志位），或阻塞调用的返回本就是超时驱动（如设置了 deadline 的 `SetReadDeadline`）时，不适用“关闭必须唤醒”的义务；此时应核对的是超时/重试语义，不是唤醒语义。

**信息不足时的处理**：无法确认源的取消是“唤醒阻塞调用”还是“置标志位等下一轮检查”时，标为“取消唤醒语义待确认”，并在终止协议中写明该分歧点；不得假定目标平台的关闭调用与源同义。

**官方依据**：[POSIX `close`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/close.html)、[POSIX `shutdown`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/shutdown.html)、[POSIX `accept`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/accept.html)；[Microsoft `closesocket`](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-closesocket)、[`GetLastError`](https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror)；[Go `net.Listener`](https://pkg.go.dev/net#Listener)；[PowerShell `Runspace.DefaultRunspace`](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.runspaces.runspace.defaultrunspace)。


### L2-CONC-02 资源所有权必须唯一化，关闭后立即失效

**触发条件**：源码创建句柄/fd/锁/线程/进程对象，并在多个分支、多个持有者之间传递或关闭。


**义务**：

1. **所有者唯一化**：每个资源在任一时刻应有**唯一**的关闭责任者。移交所有权（如把 fd 交给子进程、把句柄交给另一线程）必须在交付记录中写明移交后由谁关闭；移交后原持有者不得再关闭。
2. **关闭后立即失效**：目标语言若把关闭做成幂等（第二次 `close` 无操作或返回错误），**不得**因此认为源里“重复关闭是错误”的行为可以丢弃；反之，源若允许重复关闭，目标也必须能安全重复关闭。两者必须按源语义选择，不能按目标的便利性决定。
3. **重复关闭与 `use-after-free`**：关闭后再次使用或再次关闭，在源语言里可能是 UB、可能是安全的 no-op、也可能报错——须按源实际行为重建，不得静默归一。
4. **一次性执行结构不得被改写成循环**：`do { ... } while (0)`、`if (0) {}`、`begin ... end` 等用于**一次执行 + 统一清理**的结构，若被机械改写成无限/条件循环，会重复执行副作用并可能永不进入清理块。这是**结构改写引入的新控制流缺陷**，不是资源语义问题。
5. **清理条件不得被改动**：源里“满足条件才关闭”的判定（如 `if (h != INVALID_HANDLE_VALUE) close(h)`）在目标中必须逐条对应；把条件放宽或收紧都会造成泄漏或误关。

**错误机械替换反例**：

```ruby
# 错误：C 的一次性 do { ... } while(0) 被改写成无限循环
loop do
  inject                    # 成功路径上会重复整个注入流程
  # 缺少 break —— 且永远不进入清理块
end
cleanup

# 错误之二：关闭条件被改动
close_handle(h) if h != 0   # 源是 h != 0 && h != INVALID_HANDLE_VALUE

# 正确：保留一次执行与原有清理条件
begin
  inject
ensure
  close_handle(h) if h != 0 && h != INVALID_HANDLE_VALUE
end
```

**不适用条件**：源使用语言级确定性释放（C++ RAII、Python `with`、C# `using`、Ruby 块式 `File.open`）且所有权本就由语言机制唯一化时，不需要额外的手工所有者登记；但仍须核对**移交**场景（如把 fd 交给子进程）是否被语言机制覆盖。

**信息不足时的处理**：所有权链在源码中跨函数/跨线程不清晰时，标为“所有权移交点待确认”，并在终止协议中列出每个资源的候选关闭者；不得默认“谁创建谁关闭”。

**官方依据**：[POSIX `close`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/close.html)；[Microsoft `CloseHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)、[`INVALID_HANDLE_VALUE`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)；[Go `os.File.Close`](https://pkg.go.dev/os#File.Close)；[Ruby `File.open`（块式）](https://docs.ruby-lang.org/en/3.4/File.html#method-c-open)。


## 跨线程状态观察

工作线程写入普通状态字段、主线程轮询该字段并等待线程结束时，应查清状态读写的同步依据。缺少同步证据就登记风险，不能把增加等待或改变关闭顺序当作已修复数据竞争；静态观察不是竞态检测或运行验证。
