---
name: process-execution
description: Use alongside a matching conversion direction when source code starts a child process, invokes a shell, captures stdout/stderr, waits with a timeout, or observes exit status. Preserves process-tree, stream, timeout, and cleanup semantics across languages; it is not an independent conversion direction or execution authorization.
---

# 进程执行场景：转换语义

本场景只在源码确有子进程启动、shell 调用、输出捕获、等待或退出状态观察时与方向 Skill **共同阅读**。它不按“命令执行”“C2”等标签推断行为，也不授权运行样本。先确认源码是显式 shell 调用还是直接可执行文件、参数边界、工作目录/环境继承、流捕获方式、超时/取消和后代进程策略。

## 转换时保留的决策边界

| 源码依赖 | 应保留或确认 | 常见误改 |
|---|---|---|
| 调用形态 | 显式 shell 与直接 `argv` 的差异；shell 管道、展开、重定向是否属于源行为 | 给直接 `argv` 额外套 shell，扩大解释面；把显式 shell 改成参数数组而丢失管道/展开 |
| 参数与环境 | 参数边界、空参数、工作目录、环境变量继承/覆盖、stdin 来源 | 用字符串拼接重新解释参数；静默重置 cwd/env |
| stdout/stderr | 是否分离、合并顺序、文本解码、截断上限、读取线程/非阻塞策略 | 合并两条流改变顺序；无上限读取导致内存耗尽；只读一条流导致管道阻塞 |
| 等待与超时 | 直接进程退出、管道 EOF、超时预算、取消后的回收顺序 | 把“进程已退出”与“输出管道已排空”混为一谈；超时后无限等待后代 EOF |
| 后代进程 | 是否要求杀进程树、作业/进程组、平台限制 | 只杀直接子进程却宣称全树终止；改变源程序没有的强制终止语义 |
| 退出与错误 | 正常退出码、信号/异常终止、启动失败、超时、I/O 错误的可观察分类 | 把所有非零结果压成一个错误；丢失退出码或部分输出 |
| 资源清理 | 管道、句柄、临时文件、线程和进程对象的关闭顺序与失败传播 | 依赖 GC/析构时机；清理失败静默忽略 |

## L2-PROC-01 宿主输出通道属于可观察行为，不得只图可用

**触发条件**：源码把信息写到**非 stdout/stderr 的宿主渠道**——Shell 的 warning 流 / verbose 流 / information 流 / host 流（如 PowerShell `Write-Warning`、`Write-Verbose`、`ShouldProcess` 提示）、日志框架的独立通道，或源码对 stdout/stderr 的**分离与交错顺序**有依赖。


**义务**：

1. **通道归属是义务**：源写进 warning/host 流的内容，**不得**被静默合并到 stdout 或 stderr。目标语言若没有同构通道，须显式登记“该通道在目标中映射到何处”这一决策，而不是挑一个可用流就写。
2. **不得合成源中不存在的文本**：给非交互调用补 `What if: ...` 之类的交互式提示文本，属**新增可观察输出**，会改变下游解析。若源只在交互模式下输出该提示，目标必须复现同样的触发条件。
3. **stdout/stderr 的分离与顺序**：两条流是否合并、合并后顺序如何、是否行缓冲，都属可观察契约；把分离改成合并（或反之）会改变下游读取顺序。
4. **退出状态与流内容分开核对**：写到哪条流、退出码是多少是两件事，不得用“退出码正确”替代通道核对。
5. **行终止符的“抑制”规则属义务**：某些语言的打印函数在**参数已以换行结尾时会抑制**追加换行（Ruby `puts`），而另一些**总是追加**行终止符（.NET `Console.WriteLine` 追加 `Environment.NewLine`）。把二者互相映射会改变字节数——尤其是一行一行写 JSON 或将输出做哈希比较时。映射前必须确认源函数的实际换行规则，而不是按“都是打印一行”推断。

**错误机械替换反例**：

```ruby
# 源（C#）：Console.WriteLine(s) 总是追加 Environment.NewLine
# 目标（错误）：把全部 Console.WriteLine 映射为 puts
puts payload          # payload 已以 "\n" 结尾时，Ruby 不再追加换行 → 字节不同
```

```text
正确做法：把 .NET 的“总是追加行终止符”显式重建为 write + 行终止符，
          或改用 print/STDOUT.write 并显式写出源所使用的终止符。
```

**错误机械替换反例**：

```powershell
# 源：提示走 PowerShell 的 warning/host 流，不污染 stdout 的数据载荷
Write-Warning "volume shadow copy not available"
Write-Output $json                  # stdout 恰好一行 JSON
```
```go
// 目标（错误）：把警告写进 os.Stderr 并自行合成了源中没有的提示文本
fmt.Fprintln(os.Stderr, "What if: Performing operation ...")   // 新增了可观察输出
// 目标（错误之二）：把警告与 JSON 一起写进 stdout，破坏“恰好一行”契约
fmt.Println("warning:", msg)
fmt.Println(json)
```

**不适用条件**：源本身把全部输出写在同一条流上（无独立 warning/host 通道）时，不存在通道归属问题，只要保持该单通道的字节与顺序即可。

**信息不足时的处理**：无法确认源写的是哪条流、或目标语言无同构通道时，标为“输出通道归属待确认”并显式登记该决策；不得用“都能看见”推断等价。

**官方依据**：[PowerShell `Write-Warning`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/write-warning)、[`Write-Verbose`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/write-verbose)、[`ShouldProcess`](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess)、[about_Redirection](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection)；[POSIX `stderr`（`<stdio.h>`）](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/stdio.h.html)；[Ruby `Kernel#puts`（已有换行时抑制追加）](https://docs.ruby-lang.org/en/3.4/Kernel.html#method-i-puts)；[.NET `Console.WriteLine`](https://learn.microsoft.com/en-us/dotnet/api/system.console.writeline)。


## 语言与平台映射边界
- **Go `os/exec` → C++**：`exec.CommandContext` 只保证向直接进程发送 Kill；`WaitDelay` 限制的是等待 I/O 管道关闭的额外时间，不承诺回收整个进程树。C++ 目标须用具体平台 API 分别实现启动、管道读取、等待和超时，不能把 Go 的 `Cmd` 行为逐字段臆造到 `std::system` 或 `popen`。
- **shell 语义**：Windows `cmd /C`、PowerShell、POSIX `/bin/sh -c` 的引用、展开、内建命令和退出码不同。只有源码明确调用 shell 时才保留解释语义；目标解释器不明时标为缺口。
- **输出捕获**：stdout/stderr 分离需要两个独立管道和并发排空，否则子进程可能因管道写满而阻塞。捕获上限、解码方式和截断行为属于可观察契约。
- **超时/取消**：超时后需要区分“直接进程已回收”“管道已关闭”“后代仍存活”三种状态；目标平台若只能杀直接子进程，应在交付中明确限制。

## 与方向 Skill 的组合

方向 Skill 负责语言 API 与错误模型映射，本场景负责进程可观察语义。跨 POSIX/Linux 与 Windows 边界时，须共同加载 [POSIX ↔ Windows 进程创建与身份/权限](../../systems/posix-windows-process-identity/SKILL.md)（进程创建/替换/等待/终止与令牌特权的平台差异）；涉及并发 worker 时另读[并发场景](../concurrency/SKILL.md)；服务与注册表行为加读 [Windows 注册表与服务子系统](../../systems/windows-registry-service-subsystem/SKILL.md)。跨 OS 的进程/权限 API 若无对应条目，应列缺口，不把 POSIX 与 Win32 进程模型当成同名等价。

不运行来源不明的命令或构建脚本；只以固定合成命令、受控 cwd/env 和隔离环境设计行为 oracle。本文件不证明任何进程样例已获运行许可或已完成验证。

## 依据

- [Go `os/exec`](https://pkg.go.dev/os/exec)：`Cmd`、`WaitDelay`、`StdoutPipe`/`StderrPipe` 与进程回收边界。
- [POSIX `posix_spawn`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/posix_spawn.html)、[`waitpid`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/waitpid.html)：启动、状态宏与等待语义。
- [Microsoft `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)、[`WaitForSingleObject`](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)：Windows 进程创建、句柄与等待语义。

---

**执行顺序受根入口三道硬门禁约束**（分类 `ALLOWED` → 源侧构建预检 → 评估就绪核对），见 [AGENTS.md](../../../AGENTS.md) 执行约束 §3。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)；本场景 Skill **不替代门禁、不构成执行授权**。
