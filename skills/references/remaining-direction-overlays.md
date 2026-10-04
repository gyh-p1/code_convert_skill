# 剩余 36 个语言转换方向专向规则覆盖参考库

> **文档性质**：七语言剩余 36 个有向方向转换决策规则真源（依据《任务 03：D7–D9 剩余方向差异与矩阵收尾》）
> **知识基线**：C11（WG14 N1570）、C++17（WG21 N4659）、C# 12/.NET 8（MS-CS-*）、CPython 3.12（PY-REF-*）、Go 1.27（GO-SPEC, GO-MEM）、PowerShell 7.6（MS-PS-*）、CRuby 3.4（RB-DOC-*）
> **共性机制依据**：[七语言共性语义参考库](seven-language-common-semantics.md)
> **核心边界声明**：本文档仅提供静态转换时的**语言层决策依据与差异禁区**；**绝对不代表转换验证，不代表目标工具链已安装或目标代码功能等价**。除 C→C++ 具 5 个案例的 MinGW g++ 目标编译 PASS 记录外，其余全部方向在真实证据模型中均处于 `未验证/阻断` 状态。
> **A/B 类规则分流边界**：凡源码涉及底层操作系统、文件路径、网络套接字、系统线程或 ATT&CK 行为，一律按需加载对应 B 类场景/系统 Skill，本文件仅声明应保留的语言层契约，严禁复制操作系统与 API 映射。

---

## 目录与快速导航

| 源语言 | 覆盖的目标语言方向锚点 |
|---|---|
| **C** | [C → C#](#c-to-csharp) ｜ [C → PowerShell](#c-to-powershell) ｜ [C → Ruby](#c-to-ruby) |
| **C++** | [C++ → C#](#cpp-to-csharp) ｜ [C++ → Python](#cpp-to-python) ｜ [C++ → Go](#cpp-to-go) ｜ [C++ → PowerShell](#cpp-to-powershell) ｜ [C++ → Ruby](#cpp-to-ruby) |
| **C#** | [C# → C](#csharp-to-c) ｜ [C# → C++](#csharp-to-cpp) ｜ [C# → Python](#csharp-to-python) ｜ [C# → Go](#csharp-to-go) ｜ [C# → PowerShell](#csharp-to-powershell) ｜ [C# → Ruby](#csharp-to-ruby) |
| **Python** | [Python → C](#python-to-c) ｜ [Python → C++](#python-to-cpp) ｜ [Python → C#](#python-to-csharp) ｜ [Python → PowerShell](#python-to-powershell) ｜ [Python → Ruby](#python-to-ruby) |
| **Go** | [Go → C++](#go-to-cpp) ｜ [Go → C#](#go-to-csharp) ｜ [Go → Python](#go-to-python) ｜ [Go → PowerShell](#go-to-powershell) ｜ [Go → Ruby](#go-to-ruby) |
| **PowerShell** | [PowerShell → C](#powershell-to-c) ｜ [PowerShell → C++](#powershell-to-cpp) ｜ [PowerShell → C#](#powershell-to-csharp) ｜ [PowerShell → Python](#powershell-to-python) ｜ [PowerShell → Go](#powershell-to-go) ｜ [PowerShell → Ruby](#powershell-to-ruby) |
| **Ruby** | [Ruby → C](#ruby-to-c) ｜ [Ruby → C++](#ruby-to-cpp) ｜ [Ruby → C#](#ruby-to-csharp) ｜ [Ruby → Python](#ruby-to-python) ｜ [Ruby → Go](#ruby-to-go) ｜ [Ruby → PowerShell](#ruby-to-powershell) |

---

## 一、以 C 语言为源语言的剩余方向 (3 个方向)

<a id="c-to-csharp"></a>
### 1. C → C# (ISO C11 → C# 12 / .NET 8)

#### 规则 C-CS-01：C 结构体裸指针与定宽整数向 C# struct/class 划分与 checked 上下文映射
1. **源码触发条件**：C 源码中定义包含数值或数组的结构体并按值传递，或存在定宽无符号整数回绕算术计算。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（[WG14-N1570 §6.2.5, §6.2.6.2](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types), [MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)）。
3. **原可观察行为**：C 结构体赋值与传参为全量字节值拷贝；无符号整数运算严格按模 $2^n$ 截断回绕；有符号溢出为 UB。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若需保留值传递与无 GC 堆分配语义，声明为 C# `struct`；若需表达多态或共享引用，声明为 `class`；整数回绕计算在默认 `unchecked` 上下文中执行，若需强校验则使用 `checked` 语句。
   - *不适用条件*：严禁将所有 C 结构体机械映射为 C# `class`，否则后续传参变为引用别名，原独立副本被修改导致非预期副作用。
5. **错误机械替换反例**：
   ```csharp
   // 错误：机械映射为 class 导致传参产生别名共享修改
   public class Point { public int X; public int Y; }
   void Offset(Point p) { p.X += 10; } // 修改了外部传入的原始对象！
   // 正确：使用 struct 保持值传递独立性
   public struct Point { public int X; public int Y; }
   ```
6. **信息不足或实现相关时的处理**：若无法确认结构体是否跨线程共享，应向用户标记所有权模型未决并默认采用 `struct`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)；[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)。

#### 规则 C-CS-02：C 错误指示码与 errno 向 C# 结构化异常与 using/IDisposable 映射
1. **源码触发条件**：C 源码中使用负数或非零返回码指示操作失败，或依赖显式资源关闭函数（如 `free`, `close`）。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/), [MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）。
3. **原可观察行为**：调用方通过 `if (ret < 0)` 检查并手动跳转清理；操作系统错误通过 `errno` 暴露。
4. **目标可选写法和不适用条件**：
   - *可选映射*：底层严重失败转换为抛出派生自 `System.Exception` 的结构化异常（如 `InvalidOperationException`）；封装非托管资源的对象必须实现 `IDisposable` 并配合 `using` 语句释放。
   - *不适用条件*：严禁将 C 的所有返回码机械忽略或仅作为返回值而不加检查；严禁将析构逻辑置于 Finalizer 中期待即时执行。
5. **错误机械替换反例**：
   ```csharp
   // 错误：非内存资源未实现 IDisposable，导致句柄泄漏直到不可预期的 GC Finalizer
   public class NativeBuffer {
       private IntPtr _buf;
       ~NativeBuffer() { FreeNative(_buf); } // 错误：执行时机完全不确定！
   }
   // 正确：实现 IDisposable 并在 using 中确定性释放
   public sealed class NativeBuffer : IDisposable {
       private IntPtr _buf;
       public void Dispose() { FreeNative(_buf); GC.SuppressFinalize(this); }
   }
   ```
6. **信息不足或实现相关时的处理**：若出现文件/套接字操作，说明语言层资源释放契约后加载 [`skills/scenes/file-io/SKILL.md`](../scenes/file-io/SKILL.md) 或 [`skills/scenes/network-io/SKILL.md`](../scenes/network-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)；[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)。

#### 规则 C-CS-03：C 标志位/信号量同步向 C# Task/async-await 与 CancellationToken 映射
1. **源码触发条件**：C 源码中使用 volatile 标志位循环轮询或条件变量等待操作终止。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（[WG14-N1570 §7.17](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）；目标语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/), [MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)）。
3. **原可观察行为**：C 线程阻塞在等待循环或信号量上，通过原子修改标志位通知退出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重构为异步方法返回 `Task`，接收 `CancellationToken` 参数，调用 `token.ThrowIfCancellationRequested()` 或使用异步等待 `Task.Delay(..., token)`。
   - *不适用条件*：严禁在 C# 中使用无休止的 `while (!flag)` 忙等待占用线程池线程；严禁在异步上下文中调用 `.Result` 或 `.Wait()`，可能引发死锁。
5. **错误机械替换反例**：
   ```csharp
   // 错误：在异步上下文中阻塞等待导致死锁或线程耗尽
   public void Process() {
       var task = DoWorkAsync();
       task.Wait(); // 错误：在特定同步上下文中极易引发死锁
   }
   // 正确：使用 await 并传递取消令牌
   public async Task ProcessAsync(CancellationToken token) {
       await DoWorkAsync(token);
   }
   ```
6. **信息不足或实现相关时的处理**：若源代码涉及操作系统原生线程创建，加载 [`skills/systems/posix-windows-threads/SKILL.md`](../systems/posix-windows-threads/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)；[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)。

---

<a id="c-to-powershell"></a>
### 2. C → PowerShell (ISO C11 → PowerShell 7.6)

#### 规则 C-PS-01：C 裸字节流与缓冲区向 PowerShell 字节数组与字符编码 (utf8NoBOM) 映射
1. **源码触发条件**：C 源码中使用 `unsigned char[]` 操作二进制流或输出文本至标准输出。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines), [MS-PS-ENC](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)）。
3. **原可观察行为**：C 逐字节读写，无隐式转码；字符串以 `\0` 结尾。
4. **目标可选写法和不适用条件**：
   - *可选映射*：二进制数据显式声明为 `[byte[]]`；文本输出依赖 PS 7+ 的默认 `utf8NoBOM`，管道重定向时需确保未发生字符串格式化包装。
   - *不适用条件*：严禁将原始二进制字节直接通过文本管道传递（`Write-Output` 默认调用对象的 `.ToString()` 导致二进制损坏）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：将字节流当成文本字符串输出，导致二进制协议头被解码截断
   [byte[]]$bytes = @(0x00, 0x01, 0x02)
   Write-Output $bytes # 在管道中输出的是三个整数对象，而非原生字节流！
   # 正确：写入底层流或使用专门的字节输出
   [Console]::OpenStandardOutput().Write($bytes, 0, $bytes.Length)
   ```
6. **信息不足或实现相关时的处理**：若涉及文件重定向与外部编码，在转换报告中标明控制台代码页依赖。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ENC](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

#### 规则 C-PS-02：C 退出码与 exit(code) 向 PowerShell $LASTEXITCODE 与终止错误分流映射
1. **源码触发条件**：C 源码中调用 `exit(code)` 退出程序，或在 `main` 中返回状态码。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（[WG14-N1570 §7.22.4.4](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）；目标语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables), [MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)）。
3. **原可观察行为**：C 进程终止并向宿主返回整数状态码。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若转换目标为模块函数或脚本，操作失败应使用 `throw` 抛出终止错误或写入错误流并设 `$global:LASTEXITCODE = code`；仅当转换目标为独立 CLI 进程脚本时才允许调用 `exit $code`。
   - *不适用条件*：严禁在函数中直接调用 `exit`，这会导致调用者的整个 PowerShell 宿主会话直接退出崩溃。
5. **错误机械替换反例**：
   ```powershell
   # 错误：在函数内部直接调用 exit 杀死宿主控制台
   function Test-Valid {
       param($file)
       if (-not (Test-Path $file)) { exit 1 } # 错误：关闭了调用方 PowerShell 终端！
   }
   # 正确：抛出错误或使用 return 控制
   function Test-Valid {
       param($file)
       if (-not (Test-Path $file)) { throw [System.IO.FileNotFoundException]::new("File not found: $file") }
   }
   ```
6. **信息不足或实现相关时的处理**：若代码属于库函数还是入口脚本不明，向用户询问交付形态。
7. **直接官方 HTTPS 依据链接**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)；[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)。

#### 规则 C-PS-03：C 多线程并发向 PowerShell Start-ThreadJob 与 Runspace 隔离映射
1. **源码触发条件**：C 源码中使用 POSIX pthread 或 Windows 线程并发执行后台任务。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 PowerShell 7.6（[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）。
3. **原可观察行为**：多线程在同一进程空间并发执行，直接读写共享内存。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `Start-ThreadJob` 或 `ForEach-Object -Parallel` 在当前进程 Runspace 线程池中并发执行，共享变量使用线程安全集合或 `[System.Threading.Monitor]` 同步。
   - *不适用条件*：严禁在无同步机制下直接从多个 Runspace 读写脚本变量 `$using:var`，会造成竞态与数据损毁。
5. **错误机械替换反例**：
   ```powershell
   # 错误：无锁并发修改非线程安全哈希表
   $hash = @{}
   1..10 | ForEach-Object -Parallel {
       $using:hash[$_] = $_ # 错误：并发修改导致数据丢失或内部哈希损坏！
   }
   # 正确：使用线程安全并发字典
   $dict = [System.Collections.Concurrent.ConcurrentDictionary[int, int]]::new()
   1..10 | ForEach-Object -Parallel {
       $using:dict.TryAdd($_, $_)
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及系统级进程派生，加载 [`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)。

---

<a id="c-to-ruby"></a>
### 3. C → Ruby (ISO C11 → CRuby 3.4)

#### 规则 C-RB-01：C 整数溢出截断与布尔真假向 Ruby 任意精度 Integer 与真值模型映射
1. **源码触发条件**：C 源码中以 `0` 作为假进行条件判断，或利用定宽整数溢出回绕实现循环哈希算法。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：C 中 `0` 为假；数值到达上限后按模截断。
4. **目标可选写法和不适用条件**：
   - *可选映射*：条件判断显式写为 `if val != 0`；数值回绕显式施加位掩码 `& 0xFFFFFFFF`。
   - *不适用条件*：**致命禁区**：绝对禁止将 C 代码 `if (x)` 机械转换为 Ruby `if x`（Ruby 中 `0` 与 `""` 均为真，直接反转控制流！）。
5. **错误机械替换反例**：
   ```ruby
   # 错误：C 中 0 为假，Ruby 中 0 为真，逻辑彻底颠倒！
   status = 0 # C 原型返回 0 表示成功
   if status  # 错误：在 Ruby 中 0 为真（Truthy），导致错误分支在成功时反向执行！
     handle_error()
   end
   # 正确：显式与 0 比较
   if status != 0
     handle_error()
   end
   ```
6. **信息不足或实现相关时的处理**：扫描所有源判断表达式，标明隐式非零假定。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

#### 规则 C-RB-02：C 手动资源释放向 Ruby 块模式 (Block/Yield) 与 ensure 映射
1. **源码触发条件**：C 源码中使用 `fopen`/`fclose`、`malloc`/`free` 配对管理生命周期。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/), [RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)）。
3. **原可观察行为**：函数退出或提前返回时显式调用释放函数。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重构为接收代码块的作用域模式（如 `File.open(...) do |f| ... end`），或使用 `begin ... ensure close end` 结构。
   - *不适用条件*：严禁依赖 Ruby GC 的自动终结清理文件描述符或套接字，可能导致句柄泄漏。
5. **错误机械替换反例**：
   ```ruby
   # 错误：打开文件后未通过块或 ensure 关闭，依赖 GC 终结导致描述符耗尽
   def read_data(path)
     f = File.open(path, 'rb')
     f.read # 错误：如果发生异常或多次调用，文件句柄直到下一次 GC 前保持打开！
   end
   # 正确：使用代码块保证离开时立即关闭
   def read_data(path)
     File.open(path, 'rb') { |f| f.read }
   end
   ```
6. **信息不足或实现相关时的处理**：若涉及文件 I/O，加载 [`skills/scenes/file-io/SKILL.md`](../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)。

#### 规则 C-RB-03：C 细粒度并发向 Ruby Thread/Mutex 与 MRI GVL 约束映射
1. **源码触发条件**：C 源码中通过多线程加速纯 CPU 计算密集任务。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html), [RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)）。
3. **原可观察行为**：C 线程在多个物理 CPU 核心上实现真正的并行执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：I/O 密集型并发使用 `Thread` 与 `Mutex`；CPU 密集型必须重构为 `Ractor` 或多进程（`Process.fork`），并在报告中声明并发模型转变。
   - *不适用条件*：严禁假设 Ruby `Thread` 能直接并行计算；MRI 全局 VM 锁（GVL）限制同一时刻仅一个线程执行 Ruby 字节码。
5. **错误机械替换反例**：
   ```ruby
   # 错误：期望通过多个 Thread 加速 CPU 密集计算，因 GVL 限制毫无加速甚至变慢
   threads = 4.times.map do
     Thread.new { compute_heavy_hash() }
   end
   threads.each(&:join) # 无法利用多核！
   ```
6. **信息不足或实现相关时的处理**：若需要系统原生线程同步，加载 [`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)；[RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)。

---

## 二、以 C++ 语言为源语言的剩余方向 (5 个方向)

<a id="cpp-to-csharp"></a>
### 4. C++ → C# (ISO C++17 → C# 12 / .NET 8)

#### 规则 CPP-CS-01：C++ RAII 确定性析构向 C# IDisposable 与 using 作用域映射
1. **源码触发条件**：C++ 源码中依赖对象析构函数（RAII）管理内存外的系统资源（句柄、文件、锁）。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 C# 12 / .NET 8（[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）。
3. **原可观察行为**：对象离开局部作用域时逆序、确定性执行析构函数。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C# 中实现 `IDisposable` 接口，在调用点使用 `using var res = new ...` 或 `using (...)` 确保退出作用域时调用 `Dispose()`。
   - *不适用条件*：严禁将 C++ 析构函数机械翻译为 C# 析构函数（Finalizer：`~ClassName()`），因为 CLR 终结器执行时机非确定，会导致资源锁定与泄漏。
5. **错误机械替换反例**：
   ```csharp
   // 错误：将 C++ 析构函数直接翻译为 C# Finalizer
   public class MutexLock {
       private readonly object _lock;
       public MutexLock(object l) { _lock = l; Monitor.Enter(_lock); }
       ~MutexLock() { Monitor.Exit(_lock); } // 致命错误：GC 跨线程触发导致死锁或异常！
   }
   // 正确：使用 IDisposable 保证同步释放
   public sealed class MutexLock : IDisposable {
       private readonly object _lock;
       public MutexLock(object l) { _lock = l; Monitor.Enter(_lock); }
       public void Dispose() { Monitor.Exit(_lock); }
   }
   ```
6. **信息不足或实现相关时的处理**：若源类仅为纯内存数据结构，交由 GC 托管，无需强制实现 `IDisposable`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)；[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

#### 规则 CPP-CS-02：C++ 多重继承与虚基类向 C# 单继承加接口组合映射
1. **源码触发条件**：C++ 源码中派生类同时继承两个或多个非纯抽象基类。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 13](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：C++ 对象内存布局包含多个基类子对象，支持交叉向任意基类指针类型转换。
4. **目标可选写法和不适用条件**：
   - *可选映射*：选择一个主基类继承，其余基类转换为接口（`interface`），派生类内部通过内嵌组件对象并转发接口方法（组合优于继承）。
   - *不适用条件*：C# 语法不支持类多重继承，严禁使用任何黑魔法尝试模拟多基类字段直接合并。
5. **错误机械替换反例**：
   ```csharp
   // 错误：C# 编译器直接拒绝多类继承
   // public class Derived : BaseA, BaseB { } // 编译报错：CS1721 类不能有多个基类
   // 正确：接口加组合模式
   public interface IBaseB { void ActionB(); }
   public class Derived : BaseA, IBaseB {
       private readonly BaseB _b = new();
       public void ActionB() => _b.ActionB();
   }
   ```
6. **信息不足或实现相关时的处理**：若接口存在默认实现依赖，记录抽象层次降级并在转换日志中说明。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)。

#### 规则 CPP-CS-03：C++ std::future/std::thread 向 C# Task-based Asynchronous Pattern (TAP) 映射
1. **源码触发条件**：C++ 源码中使用 `std::async` 或 `std::future::get()` 等待异步结果。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 33.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)）。
3. **原可观察行为**：`get()` 阻塞调用线程直至后台线程计算完成并返回值。
4. **目标可选写法和不适用条件**：
   - *可选映射*：方法重构为 `async Task<T>`，使用 `await` 进行非阻塞等待，协同取消通过 `CancellationToken` 级联传递。
   - *不适用条件*：严禁在 ASP.NET Core 或 UI 上下文中直接调用 `task.Result` 模拟同步 `get()`，极易导致死锁。
5. **错误机械替换反例**：
   ```csharp
   // 错误：机械模拟 future::get() 造成死锁
   public int Calculate() {
       return ComputeAsync().Result; // 错误：在特定同步上下文引发死锁
   }
   // 正确：使用完整 async/await 调用链
   public async Task<int> CalculateAsync() {
       return await ComputeAsync();
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及底层线程优先级设置，加载 [`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)。

---

<a id="cpp-to-python"></a>
### 5. C++ → Python (ISO C++17 → CPython 3.12)

#### 规则 CPP-PY-01：C++ 模板泛型特化向 Python 动态方法派发与类型标注映射
1. **源码触发条件**：C++ 源码中定义函数模板或类模板，依赖静态类型推导。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 17](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：编译期针对每个实例化类型生成独立机器码，不匹配类型触发编译报错。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为接收通用对象的单动态函数，结合 `typing.TypeVar` 标注；若有特定类型的分支逻辑，使用 `functools.singledispatch`。
   - *不适用条件*：严禁尝试在 Python 运行期模拟 C++ 编译期 SFINAE 或模板元编程递归展开。
5. **错误机械替换反例**：
   ```python
   # 错误：试图通过字符串反射检查类型模拟模板重载
   def process(val):
       if type(val).__name__ == 'int': ... # 脆弱且破坏多态
   # 正确：使用标准 singledispatch 装饰器分派
   from functools import singledispatch
   @singledispatch
   def process(val):
       raise NotImplementedError(f"Unsupported type: {type(val)}")
   @process.register(int)
   def _(val: int): ...
   ```
6. **信息不足或实现相关时的处理**：若存在重度模板数值计算，在报告中标明 Python 运行期解释性能损失。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

#### 规则 CPP-PY-02：C++ 运算符重载向 Python 双下划线特殊方法映射
1. **源码触发条件**：C++ 源码中重载 `operator==`、`operator<`、`operator[]` 等运算符。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 Python 3.12（[PY-REF-DATA §3.3](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：通过中缀表达式调用自定义函数；`const` 引用传参。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重写为 `__eq__`、`__lt__`、`__getitem__`；需同时保持 `__hash__` 一致性（可哈希对象若实现 `__eq__` 必须实现 `__hash__`）。
   - *不适用条件*：严禁只实现 `__eq__` 而遗漏 `__hash__` 导致自定义对象无法存入 `set` 或作为 `dict` 键。
5. **错误机械替换反例**：
   ```python
   # 错误：实现 __eq__ 未实现 __hash__，导致对象变为不可哈希（unhashable）
   class Item:
       def __init__(self, id): self.id = id
       def __eq__(self, other): return isinstance(other, Item) and self.id == other.id
   # s = {Item(1)} # 抛出 TypeError: unhashable type: 'Item'
   # 正确：显式实现 __hash__
   class Item:
       def __init__(self, id): self.id = id
       def __eq__(self, other): return isinstance(other, Item) and self.id == other.id
       def __hash__(self): return hash(self.id)
   ```
6. **信息不足或实现相关时的处理**：若重载了逗号表达式或地址运算符 `&`，Python 无等价魔术方法，必须重构成显式普通函数。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA §3.3](https://docs.python.org/3.12/reference/datamodel.html)。

#### 规则 CPP-PY-03：C++ std::thread 多核并行向 Python 进程池/异步与 GIL 约束映射
1. **源码触发条件**：C++ 源码中启动多个 `std::thread` 并发执行密集数学计算。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 Python 3.12 / CPython 3.12（[CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/)）。
3. **原可观察行为**：多线程在多个物理核上并发推进，线性缩短总运行时间。
4. **目标可选写法和不适用条件**：
   - *可选映射*：CPU 密集型任务必须重写为 `multiprocessing.Pool` 或 `concurrent.futures.ProcessPoolExecutor`；若为 I/O 阻塞，可使用 `asyncio`。
   - *不适用条件*：严禁直接替换为 `threading.Thread`，受 CPython GIL 限制，纯 Python 代码的多线程无法实现多核 CPU 并行计算加速。
5. **错误机械替换反例**：
   ```python
   # 错误：使用 threading.Thread 进行 CPU 密集型运算，受 GIL 限制无加速
   import threading
   threads = [threading.Thread(target=heavy_calc) for _ in range(4)]
   for t in threads: t.start()
   for t in threads: t.join() # 实际由于 GIL 轮流锁，耗时比单线程还长！
   # 正确：使用进程池突破 GIL
   from concurrent.futures import ProcessPoolExecutor
   with ProcessPoolExecutor() as executor:
       futures = [executor.submit(heavy_calc) for _ in range(4)]
   ```
6. **信息不足或实现相关时的处理**：若代码涉及共享内存通信，加载 [`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/)。

---

<a id="cpp-to-go"></a>
### 6. C++ → Go (ISO C++17 → Go 1.27)

#### 规则 CPP-GO-01：C++ 类继承虚函数多态向 Go 隐式接口与结构体内嵌组合映射
1. **源码触发条件**：C++ 源码中定义包含纯虚函数的基类，派生类通过 `override` 覆写接口。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 13.3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 Go 1.27（[GO-SPEC #Interface_types](https://go.dev/ref/spec)）。
3. **原可观察行为**：通过基类指针或引用调用虚函数触发动态分派。
4. **目标可选写法和不适用条件**：
   - *可选映射*：将纯虚基类定义为 Go 的 `interface`；派生类定义为独立 `struct` 并实现相同签名的方法，实现隐式满足；代码复用通过结构体内嵌（Embedding）实现。
   - *不适用条件*：严禁在 Go 结构体内嵌中假设多态的“反向虚调用”（内嵌外层方法不会自动覆盖内层方法的内部调用）。
5. **错误机械替换反例**：
   ```go
   // 错误：在 Go 内嵌结构体中期待 C++ 虚函数双向覆盖行为
   type Base struct{}
   func (b *Base) TemplateMethod() { b.Hook() } // 永远调用 Base.Hook，无法多态覆盖！
   func (b *Base) Hook() { fmt.Println("Base") }
   type Derived struct{ Base }
   func (d *Derived) Hook() { fmt.Println("Derived") }
   // 正确：将多态解耦为显式接口参数传递
   type Hooker interface { Hook() }
   func TemplateMethod(h Hooker) { h.Hook() }
   ```
6. **信息不足或实现相关时的处理**：若 C++ 基类包含非公开私有虚函数，重构为包内私有方法。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Interface_types](https://go.dev/ref/spec)。

#### 规则 CPP-GO-02：C++ 异常控制流向 Go 显式多返回值 (T, error) 与 defer 逆序清理映射
1. **源码触发条件**：C++ 源码中使用 `throw` 抛出异常并在外层 `try ... catch` 捕获。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 Go 1.27（[GO-SPEC #Errors, #Defer_statements](https://go.dev/ref/spec)）。
3. **原可观察行为**：异常沿调用栈向上展开，自动析构局部对象，直至被匹配的 catch 捕获。
4. **目标可选写法和不适用条件**：
   - *可选映射*：改写函数签名增加 `error` 返回值（如 `func DoWork() (Result, error)`）；调用点显式检查 `if err != nil`；资源清理使用 `defer res.Close()`。
   - *不适用条件*：严禁将业务异常机械翻译为 Go `panic`；Go 中 `panic` 仅限致命未恢复故障，不可用作正常业务流分支。
5. **错误机械替换反例**：
   ```go
   // 错误：将常规的查找不到或输入校验错误机械替换为 panic
   func FindUser(id int) User {
       if id <= 0 { panic("invalid id") } // 错误：将常规可预期校验写为 panic！
       return user
   }
   // 正确：显式返回 error
   func FindUser(id int) (User, error) {
       if id <= 0 { return User{}, errors.New("invalid id") }
       return user, nil
   }
   ```
6. **信息不足或实现相关时的处理**：若源异常携带丰富错误上下文，定义自定义错误结构体实现 `Error() string`。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Errors](https://go.dev/ref/spec)；[GO-SPEC #Defer_statements](https://go.dev/ref/spec)。

#### 规则 CPP-GO-03：C++ std::mutex/std::condition_variable 向 Go sync/Channel 映射
1. **源码触发条件**：C++ 源码中使用 `std::unique_lock` 和条件变量进行生产者-消费者通知。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 Go 1.27（[GO-SPEC #Channel_types](https://go.dev/ref/spec), [GO-MEM](https://go.dev/ref/mem)）。
3. **原可观察行为**：消费者在条件变量上阻塞等待唤醒，互斥锁保护队列临界区。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重构为原生的 Go `chan T` 通信，通过无缓冲或有缓冲通道安全传递数据与完成通知；状态同步保留 `sync.Mutex`。
   - *不适用条件*：必须注意 Go 数据竞争不是未定义行为，但含竞争会导致状态损毁或程序终止，严禁无保护并发读写变量。
5. **错误机械替换反例**：
   ```go
   // 错误：使用裸变量轮询代替条件变量，且未加锁导致数据竞争
   var ready bool
   go func() { ready = true }()
   for !ready {} // 错误：数据竞争（Data Race），且极易在编译器优化下死循环！
   // 正确：使用 channel 进行安全通知
   done := make(chan struct{})
   go func() { close(done) }()
   <-done
   ```
6. **信息不足或实现相关时的处理**：若需级联取消与超时，结合 `context.WithTimeout` 处理。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Channel_types](https://go.dev/ref/spec)；[GO-MEM](https://go.dev/ref/mem)。

---

<a id="cpp-to-powershell"></a>
### 7. C++ → PowerShell (ISO C++17 → PowerShell 7.6)

#### 规则 CPP-PS-01：C++ 结构化数据打印向 PowerShell PSObject 管道对象流映射
1. **源码触发条件**：C++ 源码中遍历结构体列表并通过 `std::cout` 格式化打印制表符分隔文本。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）。
3. **原可观察行为**：控制台输出无结构信息的字符流。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 PowerShell 中实例化 `[PSCustomObject]` 并直接推入管道，保留属性名与强类型属性值。
   - *不适用条件*：严禁将 C++ 数据拼接为长字符串通过 `Write-Host` 输出，这会破坏后续命令对属性的过滤（如 `Where-Object`）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：将结构体字符串化输出，下游无法按属性处理
   Write-Host "ID:$id Name:$name" # 丢失对象元数据
   # 正确：输出 PSCustomObject
   [PSCustomObject]@{
       Id   = $id
       Name = $name
   }
   ```
6. **信息不足或实现相关时的处理**：若调用方要求纯文本输出，在管道末尾追加 `Out-String`。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

#### 规则 CPP-PS-02：C++ 异常分类捕获向 PowerShell 终止错误提升与 catch 分流映射
1. **源码触发条件**：C++ 源码中包含多个派生异常的 `catch (const SpecificException& e)`。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 PowerShell 7.6（[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）。
3. **原可观察行为**：根据抛出异常的运行时类型精准命中对应的 `catch` 块。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 PowerShell 中使用 `try { ... } catch [System.IO.IOException] { ... } catch { ... }` 精确捕获对应 .NET 异常类型。
   - *不适用条件*：必须注意 PowerShell `try/catch` 默认仅捕获终止错误；若调用的 Cmdlet 抛出非终止错误，必须显式附加 `-ErrorAction Stop` 才能被捕获。
5. **错误机械替换反例**：
   ```powershell
   # 错误：未配置 ErrorAction Stop，非终止错误跳过 catch 块继续向下执行
   try {
       Remove-Item -Path $file # 若文件不存在抛出非终止错误，直接跳过 catch！
   } catch {
       Write-Error "Clean failed"
   }
   # 正确：提升为终止错误
   try {
       Remove-Item -Path $file -ErrorAction Stop
   } catch {
       Write-Error "Clean failed: $_"
   }
   ```
6. **信息不足或实现相关时的处理**：若源异常为自定义非标准类，在 PS 中捕获基类 `[Exception]` 并检查消息。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)。

#### 规则 CPP-PS-03：C++ 互斥锁与临界区向 PowerShell Monitor 同步包装映射
1. **源码触发条件**：C++ 源码中使用 `std::mutex` 保护多线程共享的全局状态。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 PowerShell 7.6（[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）。
3. **原可观察行为**：确保同一时刻仅一个线程进入临界区执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `[System.Threading.Monitor]::Enter($syncObj)` 与 `[System.Threading.Monitor]::Exit($syncObj)`，或使用 `[System.Collections.Concurrent]` 线程安全集合。
   - *不适用条件*：严禁在多 Runspace 并发下直接操作非同步哈希表，会导致数据损坏或死循环。
5. **错误机械替换反例**：
   ```powershell
   # 错误：未在 finally 块中释放锁导致死锁
   [System.Threading.Monitor]::Enter($lock)
   Do-Work # 若发生异常，$lock 永远不被释放，导致全进程死锁！
   [System.Threading.Monitor]::Exit($lock)
   # 正确：使用 try-finally 确保释放
   [System.Threading.Monitor]::Enter($lock)
   try { Do-Work } finally { [System.Threading.Monitor]::Exit($lock) }
   ```
6. **信息不足或实现相关时的处理**：若涉及跨进程同步，加载 [`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)。

---

<a id="cpp-to-ruby"></a>
### 8. C++ → Ruby (ISO C++17 → CRuby 3.4)

#### 规则 CPP-RB-01：C++ 拷贝构造与对象封装向 Ruby 对象引用与深拷贝映射
1. **源码触发条件**：C++ 源码中依赖对象按值传递或显式自定义拷贝构造函数完成深拷贝。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：赋值产生完全独立的内存副本，修改新对象完全不影响原对象。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若需深拷贝，显式实现 `initialize_copy` 或使用 `Marshal.load(Marshal.dump(obj))`；传参注意在 Ruby 中皆为对象引用传递。
   - *不适用条件*：严禁认为 `b = a` 会产生独立拷贝，Ruby 仅复制对象引用别名。
5. **错误机械替换反例**：
   ```ruby
   # 错误：将对象别名直接传递，修改内部状态污染原对象
   class Config
     attr_accessor :data
     def initialize(d); @data = d; end
   end
   c1 = Config.new([1, 2])
   c2 = c1 # 仅仅是别名！
   c2.data << 3 # c1.data 也被污染变成 [1, 2, 3]！
   # 正确：实现 initialize_copy 配合 dup
   class Config
     def initialize_copy(orig)
       super
       @data = orig.data.dup
     end
   end
   c2 = c1.dup
   ```
6. **信息不足或实现相关时的处理**：若对象包含复杂原生资源指针，在转换报告中标明不可序列化限制。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

#### 规则 CPP-RB-02：C++ RAII 锁管理向 Ruby Mutex#synchronize 作用域映射
1. **源码触发条件**：C++ 源码中使用 `std::lock_guard<std::mutex> lock(mtx)`。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)）。
3. **原可观察行为**：进入作用域加锁，退出作用域无论是否抛出异常均自动解锁。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `mutex.synchronize do ... end` 代码块。
   - *不适用条件*：严禁手动调用裸 `mutex.lock` 而不放在 `begin ... ensure mutex.unlock end` 中，否则异常会导致死锁。
5. **错误机械替换反例**：
   ```ruby
   # 错误：手动加锁未设 ensure，异常导致永久死锁
   mtx.lock
   dangerous_action() # 抛出异常！
   mtx.unlock # 永远无法执行，死锁！
   # 正确：使用 synchronize 块
   mtx.synchronize do
     dangerous_action()
   end
   ```
6. **信息不足或实现相关时的处理**：若代码涉及递归加锁，使用 `Monitor` 替代 `Mutex`。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)。

#### 规则 CPP-RB-03：C++ std::map 有序关联容器向 Ruby Hash 插入顺序语义约束
1. **源码触发条件**：C++ 源码中使用 `std::map<Key, Value>` 依赖遍历时按键升序排列的性质。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 26.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)）。
3. **原可观察行为**：`std::map` 无论插入顺序如何，遍历顺序严格按照键的 `operator<` 排序。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby 的 `Hash` 保证的是**键的插入顺序**，而非按键排序！若需要按键有序遍历，必须在遍历前显式调用 `.sort_by { |k, v| k }`。
   - *不适用条件*：严禁将 C++ `std::map` 机械替换为 Ruby 原生 `Hash` 后直接依赖遍历有序性，插入顺序不同将导致遍历结果完全不同。
5. **错误机械替换反例**：
   ```ruby
   # 错误：误以为 Ruby Hash 自动按键排序
   h = {}
   h[10] = "b"; h[1] = "a"
   h.keys # 得到 [10, 1]，而 C++ std::map 遍历得到的是 [1, 10]！
   # 正确：显式按键排序遍历
   h.sort.each do |key, val|
     # 此处严格按键递增遍历
   end
   ```
6. **信息不足或实现相关时的处理**：若键类型无自然排序，向用户确认排序依据并在报告中标注。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)。

---

## 三、以 C# 语言为源语言的剩余方向 (6 个方向)

<a id="csharp-to-c"></a>
### 9. C# → C (C# 12 / .NET 8 → ISO C11)

#### 规则 CS-C-01：C# 引用类型与托管堆对象向 C 显式 malloc/free 结构体映射
1. **源码触发条件**：C# 源码中定义 `class` 并通过 `new` 频繁分配对象，依赖 CoreCLR GC 自动回收。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types), [MS-CS-GC](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals)）；目标语言 ISO C11（[WG14-N1570 §7.22.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：对象由 GC 在分代回收时自动清除，无内存悬垂，无需手动跟踪生命周期。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 C 语言堆分配结构体指针，并在模块中显式设计构造（`xxx_create`）与销毁（`xxx_destroy`）函数；若生命周期局限在函数内，优先转换为栈上局部结构体。
   - *不适用条件*：严禁在 C 中遗漏对称的 `free`；严禁重复释放或在 `free` 后解引用野指针。
5. **错误机械替换反例**：
   ```c
   // 错误：函数提前返回分支遗漏 free，引发严重内存泄漏
   MyObject* obj = my_object_create();
   if (!validate(obj)) {
       return -1; // 错误：未调用 my_object_destroy(obj) 导致泄漏！
   }
   // 正确：使用 goto cleanup 或显式逐分支释放
   if (!validate(obj)) {
       my_object_destroy(obj);
       return -1;
   }
   ```
6. **信息不足或实现相关时的处理**：若对象所有权涉及跨线程传递，标明所有权转移契约并生成文档注释。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §7.22.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[MS-CS-GC](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals)。

#### 规则 CS-C-02：C# 结构化异常体系向 C 整数错误码与返回值分流降级映射
1. **源码触发条件**：C# 源码中使用 `throw new MyException(...)` 中断控制流并在上层捕获。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）；目标语言 ISO C11（[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：抛出异常后触发运行时栈展开，跳过中间代码直到 catch 块。
4. **目标可选写法和不适用条件**：
   - *可选映射*：将函数返回值定义为 `int` 错误码（`0` 表示成功，非零/负数表示具体错误），原返回值改用指针输出参数返回；调用点逐层使用 `if (err != 0)` 检查。
   - *不适用条件*：C 语言无语言级异常展开，严禁在 C 生产代码中滥用 `setjmp`/`longjmp` 模拟高级异常。
5. **错误机械替换反例**：
   ```c
   // 错误：将 C# 抛出异常忽略，导致调用方在错误状态下继续使用未初始化数据
   // C# 原型: int Parse(string s) => throw new FormatException();
   int parse(const char* s, int* out_val) {
       // 未做错误处理直接返回
       *out_val = 0;
       return -1; // 必须返回明确错误码！
   }
   ```
6. **信息不足或实现相关时的处理**：若 C# 异常携带特定上下文消息，在 C 中定义全局或线程局部的错误缓冲区。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)；[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

#### 规则 CS-C-03：C# async/await 异步任务向 C 同步阻塞或回调状态机降级映射
1. **源码触发条件**：C# 源码中使用 `async Task<int>` 与 `await` 异步调用。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)）；目标语言 ISO C11。
3. **原可观察行为**：调用点在等待 I/O 时让出线程，由 .NET 运行时状态机恢复执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：降级为标准同步阻塞函数（若并发性能非强要求）；若必须保持异步，手工实现带结构体上下文的状态机或显式事件循环。
   - *不适用条件*：严禁在 C 中留下伪异步占位代码，必须明确其同步或回调模型。
5. **错误机械替换反例**：
   ```c
   // 错误：在 C 中简单将 async 方法写为直接返回，未处理尚未完成的异步任务
   // 导致数据竞争或未完成读取
   ```
6. **信息不足或实现相关时的处理**：若涉及套接字异步多路复用，加载 [`skills/scenes/network-io/SKILL.md`](../scenes/network-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)。

---

<a id="csharp-to-cpp"></a>
### 10. C# → C++ (C# 12 / .NET 8 → ISO C++17)

#### 规则 CS-CPP-01：C# using 资源管理向 C++17 RAII 作用域守护类映射
1. **源码触发条件**：C# 源码中使用 `using (var resource = ...)` 或 `using var` 语句。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）；目标语言 ISO C++17（[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：退出作用域时无论正常分支还是异常，均立即同步调用 `Dispose()`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 C++ 具备确定性析构函数的局部栈对象（RAII 类），或使用包含自定义 Deleter 的 `std::unique_ptr`。
   - *不适用条件*：严禁在 C++ 中将托管资源转换为裸指针后手动调用释放，容易在异常抛出时造成泄漏。
5. **错误机械替换反例**：
   ```cpp
   // 错误：在 C++ 中手动 delete 模拟 using，在发生异常时直接跳过 delete
   void Process() {
       MyResource* res = new MyResource();
       DoAction(); // 若抛出异常，res 发生内存/句柄泄漏！
       delete res;
   }
   // 正确：使用局部栈对象或 unique_ptr
   void Process() {
       auto res = std::make_unique<MyResource>();
       DoAction(); // 异常发生时自动调用析构函数安全释放
   }
   ```
6. **信息不足或实现相关时的处理**：若资源类型为系统文件或套接字，加载 [`skills/scenes/file-io/SKILL.md`](../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)；[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

#### 规则 CS-CPP-02：C# event/delegate 多播事件向 C++ std::function 与观察者容器映射
1. **源码触发条件**：C# 源码中使用 `event Action<T>` 并通过 `+=`/`-=` 进行订阅和注销。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-EVENT](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/events/delegates-events)）；目标语言 ISO C++17（[WG21-N4659 Clause 23.14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：外部调用者无法直接覆写委托链，触发事件时按顺序依次调用所有注册回调。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C++ 中实现一个简易观察者类，内部维护包含 `std::function<void(T)>` 的容器，提供 `subscribe()` 和 `unsubscribe()` 方法，注意捕获对象生命周期避免野指针。
   - *不适用条件*：严禁直接使用裸函数指针数组，无法支持带上下文状态的 lambda 闭包。
5. **错误机械替换反例**：
   ```cpp
   // 错误：使用裸函数指针无法捕获局部上下文
   typedef void (*Callback)(int);
   // 正确：使用 std::function 容器
   class Event {
       std::vector<std::function<void(int)>> handlers;
   public:
       void subscribe(std::function<void(int)> h) { handlers.push_back(h); }
       void invoke(int val) { for (auto& h : handlers) h(val); }
   };
   ```
6. **信息不足或实现相关时的处理**：若涉及多线程触发事件，给观察者容器增加 `std::mutex` 保护。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EVENT](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/events/delegates-events)；[WG21-N4659 Clause 23.14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

#### 规则 CS-CPP-03：C# CancellationToken 协同取消向 C++17 原子标志或条件变量映射
1. **源码触发条件**：C# 源码中使用 `CancellationToken` 并在循环或 I/O 中轮询 `IsCancellationRequested`。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)）；目标语言 ISO C++17（[WG21-N4659 Clause 32](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：调用方请求取消后，工作线程检测到信号抛出 `OperationCanceledException` 退出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C++17 中使用 `std::shared_ptr<std::atomic<bool>>` 作为停止标志；在条件变量阻塞时配合带谓词的 `wait_for`。
   - *不适用条件*：禁止直接使用 C++20 的 `std::stop_token`（超出冻结 C++17 范围）；严禁使用非原子普通 `bool` 变量跨线程传递取消（触发未定义行为的数据竞争）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：普通 bool 变量跨线程读取引发数据竞争 UB
   bool cancel_requested = false;
   void Worker() { while (!cancel_requested) { ... } } // UB！
   // 正确：使用 std::atomic<bool>
   std::atomic<bool> cancel_requested{false};
   void Worker() { while (!cancel_requested.load(std::memory_order_relaxed)) { ... } }
   ```
6. **信息不足或实现相关时的处理**：若取消涉及网络连接中断，需显式关闭底层套接字。
7. **直接官方 HTTPS 依据链接**：[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)；[WG21-N4659 Clause 32](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

---

<a id="csharp-to-python"></a>
### 11. C# → Python (C# 12 / .NET 8 → CPython 3.12)

#### 规则 CS-PY-01：C# 泛型强类型容器向 Python 动态列表/字典与类型注解映射
1. **源码触发条件**：C# 源码中使用 `List<T>`、`Dictionary<TKey, TValue>` 等静态强类型集合。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：编译器在编译期强制元素类型一致，插入不匹配类型直接编译失败。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Python 原生 `list` 与 `dict`，添加标准类型提示（`list[T]`, `dict[K, V]`）；若需严格运行时类型校验，可使用轻量装饰器或辅助检查。
   - *不适用条件*：严禁认为类型注解会在 Python 运行期自动抛出类型异常。
5. **错误机械替换反例**：
   ```python
   # 错误：以为声明类型标注后会拦截非法类型，Python 仍然允许异构数据插入
   items: list[int] = []
   items.append("text") # 运行期完全不报错，破坏后续算术逻辑！
   # 正确：必要时添加显式 isinstance 校验
   def add_item(items: list[int], val: int):
       if not isinstance(val, int): raise TypeError("Expected int")
       items.append(val)
   ```
6. **信息不足或实现相关时的处理**：若包含多维数组，转换为嵌套列表或记录结构转换。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)；[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators)。

#### 规则 CS-PY-02：C# IDisposable/using 向 Python with 上下文管理器映射
1. **源码触发条件**：C# 源码中使用 `using (var r = ...)` 管理互斥锁、数据库连接或临时文件。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）；目标语言 Python 3.12（[PY-REF-DATA §3.3.9](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：退出 `using` 代码块时确定性调用 `Dispose()`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Python 的 `with` 上下文管理器，自定义对象实现 `__enter__` 与 `__exit__` 方法，或使用 `contextlib.contextmanager` 装饰器。
   - *不适用条件*：严禁在 Python 中依赖 `__del__` 进行确定性资源释放。
5. **错误机械替换反例**：
   ```python
   # 错误：依赖 __del__ 进行非内存资源清理
   class LockGuard:
       def __del__(self): release_lock() # 错误：GC 时机不确定，易引发死锁！
   # 正确：实现上下文协议
   class LockGuard:
       def __enter__(self): acquire_lock(); return self
       def __exit__(self, exc_type, exc_val, exc_tb): release_lock()
   ```
6. **信息不足或实现相关时的处理**：若涉及标准库原生支持（如 `threading.Lock`），直接使用 `with lock:`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)；[PY-REF-DATA §3.3.9](https://docs.python.org/3.12/reference/datamodel.html)。

#### 规则 CS-PY-03：C# async/await (TAP) 向 Python asyncio 协程映射
1. **源码触发条件**：C# 源码中使用 `async Task<string>` 与 `await` 进行并发异步调用。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：基于线程池的非阻塞异步任务执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：定义为 `async def`，内部调用 `await`；调用顶层使用 `asyncio.run()` 驱动事件循环。
   - *不适用条件*：严禁在未进入事件循环的情况下直接调用异步函数（仅返回协程对象而不执行）；严禁在 Python 协程内执行长耗时同步阻塞系统调用（会卡死整个单线程事件循环）。
5. **错误机械替换反例**：
   ```python
   # 错误：在协程中直接调用同步 sleep 或阻塞 I/O，阻塞整个事件循环
   async def handle():
       time.sleep(5) # 错误：卡死所有并发协程！
   # 正确：使用异步非阻塞库
   async def handle():
       await asyncio.sleep(5)
   ```
6. **信息不足或实现相关时的处理**：若必须调用阻塞库，使用 `asyncio.to_thread()` 将其分流至单独线程。
7. **直接官方 HTTPS 依据链接**：[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)。

---

<a id="csharp-to-go"></a>
### 12. C# → Go (C# 12 / .NET 8 → Go 1.27)

#### 规则 CS-GO-01：C# 异常体系向 Go 显式 (T, error) 多返回值映射
1. **源码触发条件**：C# 源码中使用 `throw` 抛出异常并在多层上层通过 `try-catch` 捕获。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）；目标语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec)）。
3. **原可观察行为**：异常抛出后栈展开，未捕获导致进程异常终止。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重写函数签名返回 `(T, error)`，在失败分支返回明确的错误值，在调用点逐层做 `if err != nil` 检查与传播。
   - *不适用条件*：严禁将业务异常机械转换为 Go `panic`。
5. **错误机械替换反例**：
   ```go
   // 错误：将常规 C# 异常映射为 panic
   func ParseInt(s string) int {
       v, err := strconv.Atoi(s)
       if err != nil { panic(err) } // 错误：在库函数中随意 panic！
       return v
   }
   // 正确：返回 error
   func ParseInt(s string) (int, error) {
       return strconv.Atoi(s)
   }
   ```
6. **信息不足或实现相关时的处理**：若 C# 存在复杂异常树，在 Go 中定义不同的接口或哨兵错误（`var ErrNotFound = errors.New(...)`）支持 `errors.Is`/`errors.As`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)；[GO-SPEC #Errors](https://go.dev/ref/spec)。

#### 规则 CS-GO-02：C# using/IDisposable 向 Go defer 逆序资源清理映射
1. **源码触发条件**：C# 源码中使用 `using` 语句管理文件、互斥锁或连接生命周期。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）；目标语言 Go 1.27（[GO-SPEC #Defer_statements](https://go.dev/ref/spec)）。
3. **原可观察行为**：离开作用域时无论如何立即调用 `Dispose()`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在资源成功获取后，紧接着使用 `defer resource.Close()`。
   - *不适用条件*：严禁在长循环内部直接使用 `defer`（`defer` 在外层函数退出时才执行，循环内使用会导致句柄在循环结束前累积耗尽）。
5. **错误机械替换反例**：
   ```go
   // 错误：在循环内部滥用 defer 导致文件描述符泄漏耗尽
   for _, path := range paths {
       f, err := os.Open(path)
       if err != nil { return err }
       defer f.Close() // 致命错误：直到整个大函数退出前，所有文件句柄都不会释放！
   }
   // 正确：将循环体拆解为独立子函数或显式关闭
   for _, path := range paths {
       if err := processFile(path); err != nil { return err }
   }
   ```
6. **信息不足或实现相关时的处理**：若包含多资源依序释放，注意 Go `defer` 是 LIFO（后进先出）逆序执行。
7. **直接官方 HTTPS 依据链接**：[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)；[GO-SPEC #Defer_statements](https://go.dev/ref/spec)。

#### 规则 CS-GO-03：C# CancellationToken 向 Go context.Context 树状级联取消映射
1. **源码触发条件**：C# 源码中使用 `CancellationToken` 并在异步方法间逐层传递。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)）；目标语言 Go 1.27（[GO-PKG-CONTEXT](https://pkg.go.dev/context)）。
3. **原可观察行为**：通过 `CancellationTokenSource.Cancel()` 触发所有下游持有者的取消状态。
4. **目标可选写法和不适用条件**：
   - *可选映射*：函数首参数传入 `ctx context.Context`，在耗时循环或 I/O 中通过 `select { case <-ctx.Done(): return ctx.Err() default: }` 进行响应。
   - *不适用条件*：严禁传递 `nil` context；严禁在子 Goroutine 中忽略 `ctx.Done()` 导致协程泄漏。
5. **错误机械替换反例**：
   ```go
   // 错误：忽略取消信号，导致后台 Goroutine 永远无法退出而内存泄漏
   func Worker(ctx context.Context) {
       for {
           // 错误：没有 select 监听 ctx.Done()
           doStep()
       }
   }
   // 正确：监听 ctx.Done()
   func Worker(ctx context.Context) {
       for {
           select {
           case <-ctx.Done():
               return
           default:
               doStep()
           }
       }
   }
   ```
6. **信息不足或实现相关时的处理**：若源方法具备超时参数，使用 `context.WithTimeout` 生成子 context。
7. **直接官方 HTTPS 依据链接**：[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)；[GO-PKG-CONTEXT](https://pkg.go.dev/context)。

---

<a id="csharp-to-powershell"></a>
### 13. C# → PowerShell (C# 12 / .NET 8 → PowerShell 7.6)

#### 规则 CS-PS-01：C# 泛型 LINQ 查询向 PowerShell 管道 Where/Select 映射
1. **源码触发条件**：C# 源码中使用 `list.Where(x => ...).Select(x => ...)` 进行链式集合投影。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators)）；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）。
3. **原可观察行为**：强类型委托延迟执行（惰性求值）过滤与投影。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 PowerShell 管道命令 `$list | Where-Object { ... } | ForEach-Object { ... }`；若数据量巨大追求性能，使用 .NET 原生方法。
   - *不适用条件*：必须注意 PowerShell 管道处理单元素集合时会自动解包展开（Unrolling），可能破坏后续针对数组长度的判定。
5. **错误机械替换反例**：
   ```powershell
   # 错误：单元素过滤结果被自动解包为单个标量对象，破坏数组方法调用
   $res = $list | Where-Object { $_.Id -eq 1 }
   # 若仅匹配 1 条记录，$res 变为标量，不再具有 .Count 属性（在早期版本或严格模式下报错）
   # 正确：使用 @() 数组子表达式强制包装为数组
   $res = @($list | Where-Object { $_.Id -eq 1 })
   ```
6. **信息不足或实现相关时的处理**：若 LINQ 包含复杂分组或关联查询，在转换日志中说明性能权衡。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)；[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)。

#### 规则 CS-PS-02：C# 强类型异常向 PowerShell 终止错误提升控制映射
1. **源码触发条件**：C# 源码中抛出特定类型异常，期望立即中断当前执行流。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）；目标语言 PowerShell 7.6（[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）。
3. **原可观察行为**：异常抛出后中断当前调用链。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `throw [System.InvalidOperationException]::new("...")` 或配置 `$ErrorActionPreference = 'Stop'`。
   - *不适用条件*：严禁仅使用 `Write-Error` 代替 `throw`（`Write-Error` 默认产生非终止错误，不会中断脚本继续向下执行）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：使用 Write-Error 代替异常抛出，导致后续危险操作在错误状态下继续执行
   if ($authFailed) {
       Write-Error "Auth failed" # 脚本继续执行下一步删除操作！
   }
   Delete-AllData
   # 正确：使用 throw 抛出终止错误
   if ($authFailed) {
       throw [System.Security.Authentication.AuthenticationException]::new("Auth failed")
   }
   ```
6. **信息不足或实现相关时的处理**：若需兼容函数返回码，显式设置 `$global:LASTEXITCODE`。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)。

#### 规则 CS-PS-03：C# async/await 向 PowerShell 异步作业与同步上下文等待映射
1. **源码触发条件**：C# 源码中使用 `await DoAsync()` 等待异步结果。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)）；目标语言 PowerShell 7.6（[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）。
3. **原可观察行为**：非阻塞异步挂起，计算完成后恢复。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `Start-ThreadJob` 启动作业并配合 `Receive-Job -Wait`；对于 .NET 异步任务，可直接调用 `.GetAwaiter().GetResult()` 同步取回结果。
   - *不适用条件*：严禁在未处理异常的情况下直接等待后台任务，未捕获异常可能导致作业状态异常沉默。
5. **错误机械替换反例**：
   ```powershell
   # 错误：遗漏 Receive-Job 导致后台作业结果丢失与作业泄漏
   $job = Start-ThreadJob { Do-HeavyTask }
   # 正确：显式等待并取回数据，最后清理 Job
   $job = Start-ThreadJob { Do-HeavyTask }
   $result = Receive-Job -Job $job -Wait -AutoRemoveJob
   ```
6. **信息不足或实现相关时的处理**：若需超时控制，向 `Wait-Job` 传入 `-Timeout` 参数。
7. **直接官方 HTTPS 依据链接**：[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)。

---

<a id="csharp-to-ruby"></a>
### 14. C# → Ruby (C# 12 / .NET 8 → CRuby 3.4)

#### 规则 CS-RB-01：C# 方法重载向 Ruby 单方法动态参数与模式分流映射
1. **源码触发条件**：C# 源码中定义多个同名但不同参数类型或参数个数的重载方法。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：编译期根据实参静态类型绑定精确的目标方法重载版本。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby 不支持方法同名重载！后定义的同名方法会静默覆盖前者。必须合并为单个方法，使用默认参数、可变参数（`*args`）或关键字参数（`**kwargs`），并在方法体内根据 `case/when` 动态类型分流。
   - *不适用条件*：严禁在 Ruby 类中直接编写同名方法，否则先前的方法完全丢失。
5. **错误机械替换反例**：
   ```ruby
   # 错误：Ruby 顺序定义同名方法，导致前一个方法被彻底覆盖丢失
   class Calculator
     def add(a, b); a + b; end
     def add(a, b, c); a + b + c; end # 覆盖了两个参数的版本！
   end
   # Calculator.new.add(1, 2) # 报错 ArgumentError: wrong number of arguments (given 2, expected 3)
   # 正确：合并为单一方法并提供可选参数
   class Calculator
     def add(a, b, c = nil)
       c ? a + b + c : a + b
     end
   end
   ```
6. **信息不足或实现相关时的处理**：若重载差异极大，考虑重命名为具备明确意图的独立方法。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

#### 规则 CS-RB-02：C# checked 整数溢出检查向 Ruby 任意精度 Integer 显式校验映射
1. **源码触发条件**：C# 源码中使用 `checked { a + b }` 显式检测整数溢出并期望抛出 `OverflowException`。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：超出定宽整数上限时，CLR 运行时即时抛出 `System.OverflowException`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby 的 `Integer` 为任意精度大数，算术永不溢出！若需模拟 C# 的 `checked` 语义，必须在算术后显式检查数值是否超出 `2**31 - 1` 或 `2**63 - 1`，超出时显式抛出 `RangeError`。
   - *不适用条件*：严禁照抄算术表达式而不加界限检查，会导致溢出保护彻底失效。
5. **错误机械替换反例**：
   ```ruby
   # 错误：Ruby 自动升级为大整数，未抛出溢出异常
   # C# 原型: checked { int x = int.MaxValue + 1; } -> 抛出 OverflowException
   x = 2147483647 + 1 # 结果静默变为 2147483648，未产生任何异常！
   # 正确：显式检查并抛出异常
   def checked_add_i32(a, b)
     res = a + b
     raise RangeError, "integer overflow" if res > 2147483647 || res < -2147483648
     res
   end
   ```
6. **信息不足或实现相关时的处理**：若源上下文为 `unchecked`，则显式施加补码截断。
7. **直接官方 HTTPS 依据链接**：[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

#### 规则 CS-RB-03：C# 结构化 Task 并发向 Ruby Thread/Queue 与 GVL 约束映射
1. **源码触发条件**：C# 源码中使用 `Task.Run` 在后台并行处理数据。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)）；目标语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)）。
3. **原可观察行为**：多线程在托管线程池上并行推进，可利用多核 CPU。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Ruby `Thread.new` 配合线程安全的 `Thread::Queue` 进行任务分发；注意子线程未捕获异常默认静默终止，建议设置 `Thread.abort_on_exception = true`。
   - *不适用条件*：受 MRI GVL 约束，无法加速纯 CPU 密集计算。
5. **错误机械替换反例**：
   ```ruby
   # 错误：子线程发生未捕获异常，主线程 join 之前静默失败无任何提示
   t = Thread.new { raise "Fatal" }
   # 若未显式 t.join，错误将被完全吞没！
   # 正确：设置 abort_on_exception 并在主线程管理生命周期
   t = Thread.new do
     Thread.current.abort_on_exception = true
     do_work()
   end
   t.join
   ```
6. **信息不足或实现相关时的处理**：若需多核纯并行，声明切换为 `Ractor` 或多进程并记录未验证状态。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)。

---

## 四、以 Python 语言为源语言的剩余方向 (5 个方向)

<a id="python-to-c"></a>
### 15. Python → C (CPython 3.12 → ISO C11)

#### 规则 PY-C-01：Python 动态鸭子类型向 C 静态强类型与标量/联合体具化映射
1. **源码触发条件**：Python 源码中变量动态赋值不同类型（如先赋数字后赋字典），或函数接受异构参数。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 ISO C11（[WG14-N1570 §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：Python 变量纯粹是指向堆对象的指针，动态分派方法。
4. **目标可选写法和不适用条件**：
   - *可选映射*：推导变量的真实业务类型，具化为 C 静态类型；若必须支持有限几种变体，定义带类型标签的结构体（Tagged Union）。
   - *不适用条件*：严禁在 C 中滥用 `void*` 绕过类型系统，极易触犯 C11 严格别名规则（Strict Aliasing UB）。
5. **错误机械替换反例**：
   ```c
   // 错误：使用 void* 相互强转并解引用，触犯严格别名规则引发未定义行为
   void* ptr = &my_float;
   int val = *(int*)ptr; // UB！
   // 正确：使用带类型标签的联合体
   typedef struct {
       enum { TYPE_INT, TYPE_FLOAT } type;
       union { int i; float f; } data;
   } Variant;
   ```
6. **信息不足或实现相关时的处理**：若动态类型在源码中无法静态推导，向用户报告阻断并请求类型标注。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.5 ¶7](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

#### 规则 PY-C-02：Python 异构容器与负索引向 C 定长数组与显式长度换算映射
1. **源码触发条件**：Python 源码中使用 `list[-1]` 访问末尾元素，或使用 `list.append()` 动态追加。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 ISO C11。
3. **原可观察行为**：负索引自动加上容器长度访问元素；超出范围抛出 `IndexError`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 C 语言数组与长度变量，访问前手动换算下标：`int real_idx = idx < 0 ? len + idx : idx;`，并严格执行 `real_idx >= 0 && real_idx < len` 边界检查。
   - *不适用条件*：严禁在 C 语言中直接传入负数下标（如 `arr[-1]` 会直接越界访问数组头部之前的非法内存导致内存崩溃）。
5. **错误机械替换反例**：
   ```c
   // 错误：直接在 C 数组中使用负数索引
   // Python: return arr[-1]
   int get_last(const int* arr, size_t len) {
       return arr[-1]; // 严重错误：向前越界解引用非法内存！
   }
   // 正确：显式换算并校验
   int get_last(const int* arr, size_t len, int* out_val) {
       if (len == 0) return -1;
       *out_val = arr[len - 1];
       return 0;
   }
   ```
6. **信息不足或实现相关时的处理**：若容器大小动态变化，实现带 `capacity` 和 `size` 的动态数组结构体。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.5.2.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

#### 规则 PY-C-03：Python 任意精度 int 向 C 定宽整数防截断失真映射
1. **源码触发条件**：Python 源码中使用大整数进行乘方、大素数或密集移位计算。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 ISO C11（[WG14-N1570 §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：Python 自动扩展位宽，永不发生算术截断溢出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：确认数值范围在 64 位内时，选用 `int64_t` 或 `uint64_t`；若确认属于密码学大整数，必须在报告中声明依赖第三方大数库（如 GMP）或重构算法。
   - *不适用条件*：严禁直接将 Python 大整数运算机械套用 C `int`，静默截断会导致计算逻辑全盘失真。
5. **错误机械替换反例**：
   ```c
   // 错误：Python 中的 1 << 40 在 C 32位系统下直接溢出未定义或截断为 0
   // Python: x = 1 << 40
   int64_t x = 1 << 40; // 错误：字面量 1 为 32 位 int，左移 40 位属未定义行为！
   // 正确：显式指定 64 位字面量
   int64_t x = ((int64_t)1) << 40;
   ```
6. **信息不足或实现相关时的处理**：若无法确认数值是否超过 64 位，向用户标记潜在溢出截断风险。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.5.7](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

---

<a id="python-to-cpp"></a>
### 16. Python → C++ (CPython 3.12 → ISO C++17)

#### 规则 PY-CPP-01：Python 生成器 (yield) 向 C++17 状态机迭代器类重构映射
1. **源码触发条件**：Python 源码中包含 `def gen(): yield x` 生成器函数。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 27](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：调用生成器返回迭代器对象，通过 `next()` 逐步执行并在退出时触发清理。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C++17 中手动编写一个包含状态枚举、局部变量和 `next()` 或满足迭代器协议 `operator++`/`operator*` 的类；或者重构为一次性批量生成 `std::vector`。
   - *不适用条件*：严禁使用 C++20 协程关键字（`co_yield`, `co_return`），超出 C++17 冻结基线。
5. **错误机械替换反例**：
   ```cpp
   // 错误：在 C++17 基线中违规引入 C++20 协程
   // std::generator<int> MyGen() { co_yield 1; } // 编译报错：C++17 不支持协程
   // 正确：手动实现状态机类
   class MyGen {
       int state = 0;
       int current_val;
   public:
       bool next(int& val) {
           if (state == 0) { current_val = 1; state = 1; val = current_val; return true; }
           return false;
       }
   };
   ```
6. **信息不足或实现相关时的处理**：若生成器包含复杂的异常双向传递（`gen.throw()`），必须在报告中声明该复杂控制流降级。
7. **直接官方 HTTPS 依据链接**：[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)；[WG21-N4659 Clause 27](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

#### 规则 PY-CPP-02：Python 函数返回 None 作为可选值向 C++17 std::optional 映射
1. **源码触发条件**：Python 源码中函数在查找到数据时返回对象，未查找到时返回 `None`。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 ISO C++17（[WG21-N4659 Clause 23.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：调用方使用 `if res is None` 判定缺失。
4. **目标可选写法和不适用条件**：
   - *可选映射*：方法返回值定义为 `std::optional<T>`；缺失时返回 `std::nullopt`；调用点使用 `has_value()` 或布尔上下文检查。
   - *不适用条件*：严禁机械转换为返回裸指针 `T*` 并返回 `nullptr`（会导致所有权归属混淆及悬垂指针风险）；严禁使用 C++23 的 `std::expected`。
5. **错误机械替换反例**：
   ```cpp
   // 错误：将值对象返回转换为裸指针并返回 nullptr，造成内存泄漏或解引用崩溃
   Item* FindItem(int id) {
       if (id <= 0) return nullptr; // 谁负责释放返回的 Item*？
       return new Item(id); // 泄漏！
   }
   // 正确：使用 std::optional
   std::optional<Item> FindItem(int id) {
       if (id <= 0) return std::nullopt;
       return Item(id);
   }
   ```
6. **信息不足或实现相关时的处理**：若需要表达具体错误原因而不只是简单缺失，使用自定义 Result 结构体。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 23.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

#### 规则 PY-CPP-03：Python with 上下文管理器向 C++17 RAII 作用域析构映射
1. **源码触发条件**：Python 源码中使用 `with lock:` 或 `with open(...) as f:` 管理作用域生命周期。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 ISO C++17（[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：离开代码块时触发 `__exit__`，无论是否抛出异常均保证清理。
4. **目标可选写法和不适用条件**：
   - *可选映射*：互斥锁使用 `std::lock_guard` 或 `std::unique_lock`；文件使用 `std::ifstream`/`std::ofstream` 栈对象。
   - *不适用条件*：严禁在 C++ 中手动编写 `lock.unlock()` 并在中间留下未经保护的异常抛出点。
5. **错误机械替换反例**：
   ```cpp
   // 错误：手动管理锁，遇到异常跳过解锁
   std::mutex mtx;
   void Action() {
       mtx.lock();
       DoWork(); // 抛出异常！
       mtx.unlock(); // 永远不执行，死锁！
   }
   // 正确：RAII 守卫
   void Action() {
       std::lock_guard<std::mutex> lock(mtx);
       DoWork();
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及文件 I/O，加载 [`skills/scenes/file-io/SKILL.md`](../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

---

<a id="python-to-csharp"></a>
### 17. Python → C# (CPython 3.12 → C# 12 / .NET 8)

#### 规则 PY-CS-01：Python **kwargs 动态参数向 C# 强类型选项对象或命名参数映射
1. **源码触发条件**：Python 源码中使用 `**kwargs` 接收任意键值对参数并在内部动态取值。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：运行期动态解包字典，未传递键通过 `.get('key', default)` 处理。
4. **目标可选写法和不适用条件**：
   - *可选映射*：定义包含所需字段的强类型 Options 类或 record；或者在 C# 方法中定义具备默认值的命名可选参数。
   - *不适用条件*：严禁全部使用 `Dictionary<string, object>` 替代，会丧失静态编译强类型检查并引入装箱与拆箱性能开销。
5. **错误机械替换反例**：
   ```csharp
   // 错误：在 C# 中大量使用弱类型字典模拟 kwargs
   public void Setup(Dictionary<string, object> kwargs) {
       int timeout = (int)kwargs["timeout"]; // 缺少键时抛 KeyNotFoundException，类型不符抛 InvalidCastException
   }
   // 正确：使用强类型 Options
   public record SetupOptions(int Timeout = 30, string Host = "localhost");
   public void Setup(SetupOptions options) { ... }
   ```
6. **信息不足或实现相关时的处理**：若选项高度动态，可提供辅助构造方法或向用户确认字段完整性。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)。

#### 规则 PY-CS-02：Python 多返回值元组向 C# ValueTuple 与析构声明映射
1. **源码触发条件**：Python 源码中函数通过 `return a, b` 返回多个值，调用方通过 `x, y = fn()` 解构。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：返回不可变的 `tuple` 对象，支持位置匹配解包。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 C# 具名 ValueTuple：`public (int Count, string Name) GetData()`，调用点使用 `var (count, name) = GetData()` 解构。
   - *不适用条件*：严禁使用遗留的引用类型 `System.Tuple<T1, T2>`（不可变 class，产生多余堆分配且属性名退化为 `Item1, Item2`）。
5. **错误机械替换反例**：
   ```csharp
   // 错误：使用遗留 Tuple 产生堆分配且丢失可读性
   public Tuple<int, string> GetData() => new Tuple<int, string>(1, "a");
   // 正确：使用轻量栈分配 ValueTuple
   public (int Id, string Name) GetData() => (1, "a");
   ```
6. **信息不足或实现相关时的处理**：若解构变量超过 4 个，建议重构成具备业务语义的 `record`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)。

#### 规则 PY-CS-03：Python with 资源管理向 C# using 声明与 IDisposable 映射
1. **源码触发条件**：Python 源码中使用 `with open(...)` 或自定义上下文管理器。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 C# 12 / .NET 8（[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）。
3. **原可观察行为**：退出代码块时立即触发释放。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `using var stream = ...` 语法糖，离开局部代码块时自动调用 `Dispose()`。
   - *不适用条件*：严禁遗漏 `using` 关键字，C# 引用对象直到 GC Finalizer 前不会释放句柄。
5. **错误机械替换反例**：
   ```csharp
   // 错误：裸分配 IDisposable 对象而未加 using
   var fs = File.OpenRead(path);
   var data = fs.ReadByte();
   // 错误：fs 保持打开状态，直到不知何时 GC 运行！
   // 正确：使用 using 声明
   using var fs = File.OpenRead(path);
   var data = fs.ReadByte();
   ```
6. **信息不足或实现相关时的处理**：若涉及文件路径操作，加载 [`skills/scenes/file-io/SKILL.md`](../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)。

---

<a id="python-to-powershell"></a>
### 18. Python → PowerShell (CPython 3.12 → PowerShell 7.6)

#### 规则 PY-PS-01：Python 大小写敏感变量/方法向 PowerShell 大小写不敏感环境重构映射
1. **源码触发条件**：Python 源码中定义仅有大小写差异的不同标识符（如 `data` 与 `Data`，或 `val` 与 `VAL`）。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)）。
3. **原可观察行为**：Python 严格区分大小写，`data` 和 `Data` 是两个完全独立、互不干扰的变量。
4. **目标可选写法和不适用条件**：
   - *可选映射*：PowerShell 语法与变量查找**默认大小写不敏感**！`$data` 与 `$Data` 会访问同一个变量。必须对同名大小写变量显式重命名（如 `$dataVal` 与 `$dataObj`），消除冲突。
   - *不适用条件*：严禁照抄仅大小写不同的变量名，会导致其中一个变量被隐式覆盖损毁。
5. **错误机械替换反例**：
   ```powershell
   # 错误：在 PowerShell 中 $data 与 $Data 是同一个变量，发生相互覆盖
   $data = "initial"
   $Data = "override" # 覆盖了 $data！
   # Write-Output $data 输出 "override"，原数据丢失！
   # 正确：显式区分变量命名
   $dataText = "initial"
   $dataRecord = "override"
   ```
6. **信息不足或实现相关时的处理**：扫描源文件全部符号表，建立大小写冲突清单并报告用户。
7. **直接官方 HTTPS 依据链接**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

#### 规则 PY-PS-02：Python 列表推导向 PowerShell 管道过滤与展开映射
1. **源码触发条件**：Python 源码中使用 `[x * 2 for x in items if x > 0]` 列表推导式。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）。
3. **原可观察行为**：即时计算并生成新的 `list` 对象。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `$items | Where-Object { $_ -gt 0 } | ForEach-Object { $_ * 2 }`；若在循环内追求极速，使用 `foreach ($x in $items)` 语句。
   - *不适用条件*：注意 PowerShell 数组通过 `+=` 扩展时会全量复制数组，大循环累加必须使用 `[System.Collections.Generic.List[T]]`。
5. **错误机械替换反例**：
   ```powershell
   # 错误：在大循环中使用 += 累加数组，时间复杂度退化为 O(N^2)
   $res = @()
   foreach ($x in $items) { $res += $x } # 每次分配新数组并全量复制！
   # 正确：使用管道或 Generic.List
   $res = [System.Collections.Generic.List[object]]::new()
   foreach ($x in $items) { $res.Add($x) }
   ```
6. **信息不足或实现相关时的处理**：数据规模未标明时，默认提供管道实现并在性能敏感处提示。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

#### 规则 PY-PS-03：Python 异常层次向 PowerShell 终止错误与 catch 映射
1. **源码触发条件**：Python 源码中使用 `raise ValueError(...)` 并通过 `except Exception as e:` 捕获。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 PowerShell 7.6（[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）。
3. **原可观察行为**：抛出异常，中断执行，打印 traceback。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `throw [System.ArgumentException]::new("...")`；捕获使用 `try { ... } catch { ... }`，通过 `$_` 获取当前异常对象。
   - *不适用条件*：严禁在 catch 块中忽略 `$_` 的具体内容而直接静默返回。
5. **错误机械替换反例**：
   ```powershell
   # 错误：捕获后未打印或记录异常信息，静默掩盖严重系统故障
   try { Dangerous-Action } catch { } # 盲捕获吞没错误！
   # 正确：至少记录错误
   try { Dangerous-Action } catch { Write-Error "Action failed: $_" }
   ```
6. **信息不足或实现相关时的处理**：若源异常为特定业务自定义类，映射为 `[System.Exception]` 并包含原异常名。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)。

---

<a id="python-to-ruby"></a>
### 19. Python → Ruby (CPython 3.12 → CRuby 3.4)

#### 规则 PY-RB-01：Python 与 Ruby 真值模型 (0, "" 真假异同) 冲突防反转映射
1. **源码触发条件**：Python 源码中使用 `if val:` 进行条件分支判断，其中 `val` 可能是数字 `0` 或空字符串 `""`。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：在 Python 中，数字 `0`、浮点 `0.0`、空字符串 `""`、空列表 `[]`、空字典 `{}` 均为**假（Falsy）**！
4. **目标可选写法和不适用条件**：
   - *可选映射*：**在 Ruby 中，只有 `false` 和 `nil` 为假，`0` 和 `""` 均为真（Truthy）**！若原 Python 意图是判断非零，必须在 Ruby 中显式写为 `if val != 0`；若意图是判断非空字符串，必须显式写为 `if !val.empty?`。
   - *不适用条件*：**绝对禁止直接翻译为 `if val`**！这会导致 Python 中条件为假的分支在 Ruby 中 100% 反向执行！
5. **错误机械替换反例**：
   ```ruby
   # 错误：Python 期望在 count == 0 时不进入分支，Ruby 却直接进入分支！
   # Python 原型:
   # if count: print("has items")
   count = 0
   if count # 错误：在 Ruby 中 0 是 Truthy，打印了 "has items"！
     puts "has items"
   end
   # 正确：显式判定
   if count != 0
     puts "has items"
   end
   ```
6. **信息不足或实现相关时的处理**：对每个无比较符的裸 `if x` 条件，严格依据其类型上下文替换为显式谓词。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

#### 规则 PY-RB-02：Python with 上下文管理向 Ruby 资源块模式 (Block/yield) 映射
1. **源码触发条件**：Python 源码中使用 `with open(path) as f:` 进行文件读写。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：离开作用域时无论是否发生异常均确保关闭底层文件句柄。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重构为 Ruby 原生代码块传递：`File.open(path) do |f| ... end`。
   - *不适用条件*：严禁写成无块形式的 `f = File.open(path)` 而不显式 `ensure f.close`。
5. **错误机械替换反例**：
   ```ruby
   # 错误：省略代码块，异常时文件句柄泄漏
   f = File.open(path, 'r')
   content = f.read
   f.close # 若 read 抛出异常，close 被跳过！
   # 正确：使用块自动管理生命周期
   content = File.open(path, 'r') { |f| f.read }
   ```
6. **信息不足或实现相关时的处理**：若涉及文件路径操作，加载 [`skills/scenes/file-io/SKILL.md`](../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

#### 规则 PY-RB-03：Python 异常基类向 Ruby StandardError 捕获边界映射
1. **源码触发条件**：Python 源码中使用 `except Exception as e:` 捕获常规业务异常。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）。
3. **原可观察行为**：捕获所有从 `Exception` 派生的非系统退出异常（`SystemExit`、`KeyboardInterrupt` 继承自 `BaseException` 不被捕获）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Ruby 中使用 `rescue => e` 或 `rescue StandardError => e`（Ruby 默认 rescue 的正是 `StandardError` 及其子类）。
   - *不适用条件*：**致命禁区**：绝对不要在 Ruby 中写 `rescue Exception => e`！在 Ruby 中 `Exception` 是最顶层基类，盲捕获它会导致系统中断信号（`SignalException`）、语法错误（`SyntaxError`）和内存耗尽（`NoMemoryError`）全部被意外吞没，导致进程无法正常终止！
5. **错误机械替换反例**：
   ```ruby
   # 错误：捕获了最顶层 Exception，导致 kill 信号或内存耗尽被吞没
   begin
     do_work()
   rescue Exception => e # 致命错误：屏蔽了系统致命信号！
     puts "error: #{e}"
   end
   # 正确：捕获 StandardError
   begin
     do_work()
   rescue StandardError => e
     puts "error: #{e}"
   end
   ```
6. **信息不足或实现相关时的处理**：若 Python 捕获了专有异常，定义对应的 Ruby 异常派生自 `StandardError`。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)。

---

## 五、以 Go 语言为源语言的剩余方向 (5 个方向)

<a id="go-to-cpp"></a>
### 20. Go → C++ (Go 1.27 → ISO C++17)

#### 规则 GO-CPP-01：Go (T, error) 显式多返回值向 C++17 自定义 Result 结构体或 std::optional 映射
1. **源码触发条件**：Go 源码中函数返回 `(Result, error)`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec)）；目标语言 ISO C++17（[WG21-N4659](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：显式多值返回，调用方通过 `if err != nil` 检查错误。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若只需表达有无数据，使用 `std::optional<T>`；若需携带错误细节，定义 `struct ResultOrError { T val; std::string error_msg; bool ok; }` 或使用输出参数；或者在失败时抛出异常。
   - *不适用条件*：严禁在 C++17 中使用 `std::expected`（C++23 特性，超出冻结规范）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：在 C++17 基线代码中使用 C++23 的 std::expected
   // std::expected<int, std::string> Divide(int a, int b); // 编译报错：C++17 无此特性！
   // 正确：使用带状态结构体或 std::optional
   struct Result { int value; std::string err; bool is_ok() const { return err.empty(); } };
   ```
6. **信息不足或实现相关时的处理**：若原 Go 代码无错误传递直接返回，直接映射为 C++ 对应单一返回值。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Errors](https://go.dev/ref/spec)；[WG21-N4659 Clause 23.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

#### 规则 GO-CPP-02：Go defer 逆序清理向 C++17 局部作用域析构 (RAII) 映射
1. **源码触发条件**：Go 源码中使用 `defer mu.Unlock()` 或 `defer file.Close()`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Defer_statements](https://go.dev/ref/spec)）；目标语言 ISO C++17（[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：注册的清理函数在外层函数返回前以 LIFO（后进先出）逆序确定性执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：互斥锁使用 `std::lock_guard`；文件/资源封装为 RAII 守卫类；或编写简易 ScopeGuard 类在析构时调用 lambda。
   - *不适用条件*：严禁遗漏任何提前 `return` 分支中的资源释放。
5. **错误机械替换反例**：
   ```cpp
   // 错误：将 Go defer 机械写在函数末尾，导致提前 return 时资源未释放
   void Process() {
       FILE* f = fopen("test.txt", "r");
       if (check(f) == -1) return; // 错误：f 泄漏！
       fclose(f);
   }
   // 正确：使用 ScopeGuard 或局部析构包装
   void Process() {
       auto file_guard = std::unique_ptr<FILE, decltype(&fclose)>(fopen("test.txt", "r"), &fclose);
       if (check(file_guard.get()) == -1) return; // 析构自动 fclose！
   }
   ```
6. **信息不足或实现相关时的处理**：若 defer 包含修改具名返回值的副作用，需在 C++ 中显式转化为返回前变量修改。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Defer_statements](https://go.dev/ref/spec)；[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

#### 规则 GO-CPP-03：Go Goroutine 与 Channel 向 C++17 std::thread 与并发阻塞队列映射
1. **源码触发条件**：Go 源码中使用 `go worker()` 启动协程并通过 `chan T` 通信。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Go_statements](https://go.dev/ref/spec)）；目标语言 ISO C++17（[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：轻量级 Goroutine 协作调度，Channel 阻塞传递数据。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Goroutine 数量有限时映射为 `std::thread`，大量并发时必须使用固定大小线程池；Channel 映射为结合 `std::mutex` 和 `std::condition_variable` 的线程安全阻塞队列。
   - *不适用条件*：严禁无限制创建 `std::thread`（C++ 线程为原生 OS 线程，创建数万个会导致系统资源枯竭甚至进程崩溃）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：对成千上万个任务直接 1:1 创建 std::thread
   for (int i = 0; i < 100000; ++i) {
       std::thread(worker).detach(); // 致命错误：OS 线程资源耗尽导致 std::system_error 崩溃！
   }
   // 正确：使用线程池任务分发
   ThreadPool pool(4);
   for (int i = 0; i < 100000; ++i) {
       pool.enqueue(worker);
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及底层网络套接字并发，加载 [`skills/scenes/network-io/SKILL.md`](../scenes/network-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Go_statements](https://go.dev/ref/spec)；[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

---

<a id="go-to-csharp"></a>
### 21. Go → C# (Go 1.27 → C# 12 / .NET 8)

#### 规则 GO-CS-01：Go 结构体值传递向 C# struct/class 语义划分映射
1. **源码触发条件**：Go 源码中定义 `type Data struct` 并以值接收者 `func (d Data)` 传参。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Struct_types](https://go.dev/ref/spec)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：纯值复制，方法内修改 `d` 不影响外部调用者。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若需保持全量值复制且数据结构较小，声明为 C# `struct`；若为大对象或需支持引用语义，声明为 `class` 并在传参时显式创建副本。
   - *不适用条件*：严禁将值接收者方法所在结构体无脑翻译为 `class`，否则后续调用会产生意外的别名修改副作用。
5. **错误机械替换反例**：
   ```csharp
   // 错误：将 Go 值类型结构体映射为 C# class 导致方法内修改污染外部
   public class Config {
       public int Timeout;
       public void SetTimeout(int t) { this.Timeout = t; }
   }
   // Go 原型为值接收者，调用后外部 Config 未变；C# class 会直接修改外部对象！
   // 正确：使用 struct 保持值语义
   public struct Config {
       public int Timeout;
   }
   ```
6. **信息不足或实现相关时的处理**：若结构体包含大量字段，标记性能权衡并提示用户选择。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)；[GO-SPEC #Struct_types](https://go.dev/ref/spec)。

#### 规则 GO-CS-02：Go error 返回向 C# 结构化异常抛出映射
1. **源码触发条件**：Go 源码中使用 `return nil, errors.New("not found")`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）。
3. **原可观察行为**：调用方必须显式判断 `err != nil`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为抛出对应的 C# 异常（如 `throw new KeyNotFoundException(...)`）；或者若该错误属于频繁发生的常规分支，提供形如 `bool TryGetValue(...)` 的 Try 模式方法。
   - *不适用条件*：严禁将业务失败静默忽略。
5. **错误机械替换反例**：
   ```csharp
   // 错误：为了强行对应多返回值，在 C# 中返回二元元组且不加强制检查
   public (User, string) FindUser(int id) { ... } // 违背 C# 习惯用法
   // 正确：使用常规异常或 Try 模式
   public bool TryFindUser(int id, out User user) { ... }
   ```
6. **信息不足或实现相关时的处理**：若源错误代码作为系统进程返回码，映射为带退出码的异常。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)。

#### 规则 GO-CS-03：Go context.Context 取消树向 C# CancellationTokenSource 映射
1. **源码触发条件**：Go 源码中使用 `ctx, cancel := context.WithCancel(parentCtx)` 并通过 `<-ctx.Done()` 监听取消。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-PKG-CONTEXT](https://pkg.go.dev/context)）；目标语言 C# 12 / .NET 8（[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)）。
3. **原可观察行为**：父 context 取消级联触发所有衍生子 context 的 Done 通道关闭。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `CancellationTokenSource.CreateLinkedTokenSource(parentToken)` 构造级联取消令牌源，向异步方法传递 `cts.Token`。
   - *不适用条件*：必须注意 `CancellationTokenSource` 实现了 `IDisposable`，必须在使用完成后显式调用 `Dispose()` 释放底层定时器或句柄资源。
5. **错误机械替换反例**：
   ```csharp
   // 错误：使用带超时的 CTS 未释放导致定时器资源泄漏
   public async Task RunWithTimeout() {
       var cts = new CancellationTokenSource(1000); // 实现了 IDisposable！
       await DoWorkAsync(cts.Token);
       // 缺少 cts.Dispose()！
   }
   // 正确：使用 using 语句
   public async Task RunWithTimeout() {
       using var cts = new CancellationTokenSource(1000);
       await DoWorkAsync(cts.Token);
   }
   ```
6. **信息不足或实现相关时的处理**：若 context 携带 Value 数据，转换为基于 `AsyncLocal<T>` 或显式参数传递。
7. **直接官方 HTTPS 依据链接**：[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)；[GO-PKG-CONTEXT](https://pkg.go.dev/context)。

---

<a id="go-to-python"></a>
### 22. Go → Python (Go 1.27 → CPython 3.12)

#### 规则 GO-PY-01：Go 切片容量共享向 Python list 独立扩容语义隔离映射
1. **源码触发条件**：Go 源码中使用 `s2 := s1[1:3]` 从原切片截取新切片并修改元素。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Slice_types](https://go.dev/ref/spec)）；目标语言 Python 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：Go 中 `s2` 与 `s1` 共享底层数组，修改 `s2` 会原地影响 `s1`；直到发生 `append` 扩容后才分离。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Python 的切片操作 `l2 = l1[1:3]` 会**立即创建一个全新的浅拷贝独立列表**！修改 `l2` 绝不会影响 `l1`！若业务必须依赖共享修改，必须封装带视图指针的自定义类或操作同一个列表下标。
   - *不适用条件*：绝对不能直接假定 Python 切片具有 Go 切片的底层数组共享特性。
5. **错误机械替换反例**：
   ```python
   # 错误：以为 Python 切片像 Go 切片一样共享底层存储
   l1 = [1, 2, 3, 4]
   l2 = l1[1:3] # 生成了独立列表 [2, 3]
   l2[0] = 99   # l1 完全没有变化！l1[1] 依然是 2！
   # 正确：若需修改原列表，必须显式在原列表上修改
   l1[1] = 99
   ```
6. **信息不足或实现相关时的处理**：扫描所有切片赋值，确认是否有向原切片反写数据的依赖并告警。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Slice_types](https://go.dev/ref/spec)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

#### 规则 GO-PY-02：Go 显式 error 检查向 Python 结构化异常体系映射
1. **源码触发条件**：Go 源码中存在大量 `if err != nil { return nil, err }` 样板代码。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 Python 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：错误通过返回值显式传递，未检查不会自动抛出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Python 标准异常（如 `ValueError`, `FileNotFoundError`, `RuntimeError`），依靠异常自动冒泡传播，消除深层样板检查。
   - *不适用条件*：严禁在 Python 中模仿 Go 返回二元元组并在每一步手写 `if err is not None`（严重违背 Python 习惯用法，极易遗漏处理）。
5. **错误机械替换反例**：
   ```python
   # 错误：在 Python 中强行写 Go 风格的返回元组，违背习惯且容易被忽略
   def divide(a, b):
       if b == 0: return None, "divide by zero"
       return a / b, None
   # 正确：抛出内置异常
   def divide(a, b):
       if b == 0: raise ZeroDivisionError("divide by zero")
       return a / b
   ```
6. **信息不足或实现相关时的处理**：若原 Go 错误类型具备专有字段，定义继承自 `Exception` 的子类。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

#### 规则 GO-PY-03：Go 并发 Goroutine 与 Channel 向 Python asyncio 协程与 Queue 映射
1. **源码触发条件**：Go 源码中使用 `go fn()` 与 `ch := make(chan int)`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：轻量级协程在 M:N 调度器下执行，支持高并发 channel 通信。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重写为 `async def`，channel 替换为 `asyncio.Queue`，通信使用 `await queue.put()` 与 `await queue.get()`。
   - *不适用条件*：受 CPython GIL 影响，纯 CPU 运算无法多核加速；严禁在普通函数中直接使用阻塞队列而未设超时。
5. **错误机械替换反例**：
   ```python
   # 错误：在未加入事件循环的普通线程中调用 asyncio.Queue 导致 RuntimeError
   import asyncio
   q = asyncio.Queue() # 无当前运行的事件循环时在旧版本报错或引发跨线程异常
   ```
6. **信息不足或实现相关时的处理**：若代码涉及高吞吐 CPU 运算，向用户建议使用多进程并报告差异。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

---

<a id="go-to-powershell"></a>
### 23. Go → PowerShell (Go 1.27 → PowerShell 7.6)

#### 规则 GO-PS-01：Go 强类型结构体输出向 PowerShell PSCustomObject 管道对象流映射
1. **源码触发条件**：Go 源码中处理结构体切片并进行遍历处理。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）。
3. **原可观察行为**：强类型结构体字段访问，编译期严格类型保证。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `[PSCustomObject]@{ Field = val }` 并推入管道，以便下游通过 `$_` 访问属性。
   - *不适用条件*：严禁序列化为 JSON 字符串直接输出而不解包，会破坏管道后续的无缝处理。
5. **错误机械替换反例**：
   ```powershell
   # 错误：将结构体转为文本 JSON 输出，下游必须手动二次 ConvertFrom-Json
   $json = $data | ConvertTo-Json
   Write-Output $json
   # 正确：直接输出对象
   [PSCustomObject]@{
       Id   = $data.Id
       Name = $data.Name
   }
   ```
6. **信息不足或实现相关时的处理**：若字段涉及首字母大小写可见性，在 PowerShell 中统一规范为 PascalCase。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

#### 规则 GO-PS-02：Go os.Exit 退出码向 PowerShell $LASTEXITCODE 与终止错误映射
1. **源码触发条件**：Go 源码中调用 `os.Exit(code)` 立即退出进程。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC](https://go.dev/ref/spec)）；目标语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)）。
3. **原可观察行为**：Go 进程立即终止并回传状态码，**跳过所有 defer 语句**！
4. **目标可选写法和不适用条件**：
   - *可选映射*：在独立脚本中映射为 `exit $code`；在模块函数中改写为设置 `$global:LASTEXITCODE = $code` 并 `throw` 终止错误。
   - *不适用条件*：严禁在函数内盲目调用 `exit` 终止用户当前会话。
5. **错误机械替换反例**：
   ```powershell
   # 错误：模块函数内直接 exit 杀掉交互式窗口
   function Run-Task { if ($failed) { exit 2 } } # 用户当前终端直接闪退！
   # 正确：抛出终止错误
   function Run-Task { if ($failed) { throw "Task failed with exit code 2" } }
   ```
6. **信息不足或实现相关时的处理**：若原 Go 代码中有未执行的 defer，在报告中警告其确定性丢失。
7. **直接官方 HTTPS 依据链接**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

#### 规则 GO-PS-03：Go 常驻守护任务向 PowerShell 短生命周期脚本模型转换边界
1. **源码触发条件**：Go 源码中通过 `select {}` 实现常驻后台服务并监听信号。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 PowerShell 7.6（[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）。
3. **原可观察行为**：编译为原生守护进程长期运行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 PowerShell 中重构为单次触发任务或通过 `Start-Job` 注册后台作业，或依赖外部任务计划程序（Task Scheduler）。
   - *不适用条件*：严禁在交互式 PowerShell 脚本中写永久死循环死等，会占用宿主线程。
5. **错误机械替换反例**：
   ```powershell
   # 错误：直接在前台脚本写死循环阻塞控制台且无法优雅响应中断
   while ($true) { Start-Sleep -Seconds 1 }
   ```
6. **信息不足或实现相关时的处理**：若必须常驻，向用户提示脚本宿主生命周期限制。
7. **直接官方 HTTPS 依据链接**：[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)。

---

<a id="go-to-ruby"></a>
### 24. Go → Ruby (Go 1.27 → CRuby 3.4)

#### 规则 GO-RB-01：Go map 无序遍历向 Ruby Hash 有序插入遍历的隔离映射
1. **源码触发条件**：Go 源码中通过 `for k, v := range m` 遍历哈希表。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Map_types](https://go.dev/ref/spec)）；目标语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)）。
3. **原可观察行为**：Go 语言规范明确未规定 map 遍历顺序（故意引入随机种子打乱顺序）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby 的 `Hash` 规范**强制保证按键值对的插入顺序遍历**！转换至 Ruby 后，代码切不可隐式产生“顺序依赖”；若业务需要无序性（如测试随机打乱），必须显式调用 `.to_a.shuffle`。
   - *不适用条件*：严禁在转换后代码中依赖插入顺序作为业务逻辑前提，否则逆向回 Go 时必崩溃。
5. **错误机械替换反例**：
   ```ruby
   # 错误：误以为 Ruby Hash 与 Go 一样是随机遍历，编写了依赖顺序或未打乱的逻辑
   # Go: for k := range m { ... } // 每次运行顺序不同
   # Ruby: h.each { |k, v| ... } // 永远按照严格的插入顺序遍历！
   ```
6. **信息不足或实现相关时的处理**：在转换报告中明确标记 Ruby Hash 存在插入有序性保证的事实。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Map_types](https://go.dev/ref/spec)；[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)。

#### 规则 GO-RB-02：Go 定宽整数模截断向 Ruby 任意精度 Integer 显式掩码映射
1. **源码触发条件**：Go 源码中使用 `uint32` 进行运算，依赖其超出 $2^{32}-1$ 时自动按模截断回绕。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：达到上限后自动截断回绕（非 UB）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Ruby 中计算后显式施加位掩码 `& 0xFFFFFFFF`，保留截断值。
   - *不适用条件*：严禁直接计算，Ruby `Integer` 自动升级为大数，高位数据残留导致哈希或校验和计算彻底错误。
5. **错误机械替换反例**：
   ```ruby
   # 错误：未加掩码截断，导致高位无限增长
   # Go: var h uint32 = 0xFFFFFFFF; h = h + 1 // h 变成 0
   h = 0xFFFFFFFF
   h = h + 1 # Ruby 中 h 变成了 4294967296，彻底失真！
   # 正确：显式截断
   h = (h + 1) & 0xFFFFFFFF
   ```
6. **信息不足或实现相关时的处理**：若涉及有符号数转换，提供补码还原函数。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

#### 规则 GO-RB-03：Go CSP 并发模型向 Ruby Queue/Mutex 与 GVL 约束映射
1. **源码触发条件**：Go 源码中使用多个 Goroutine 通过信道传递流水线数据。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)）。
3. **原可观察行为**：轻量协程高效流水线调度。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `Thread` 配合 `Thread::SizedQueue` 模拟带缓冲 Channel；在队列关闭时使用特定的标志对象（Sentinel Object）。
   - *不适用条件*：受 GVL 限制，纯 CPU 运算无法多核并行；注意未关闭队列会导致线程永久挂起。
5. **错误机械替换反例**：
   ```ruby
   # 错误：未关闭队列导致消费者线程 pop 永远阻塞发生死锁
   q = SizedQueue.new(10)
   # 生产者结束未通知，消费者 q.pop 永久挂死！
   # 正确：使用哨兵或关闭机制
   q.close
   ```
6. **信息不足或实现相关时的处理**：若需完全独立并发，建议采用 Ractor 模型并记录实验性质。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)。

---

## 六、以 PowerShell 为源语言的剩余方向 (6 个方向)

<a id="powershell-to-c"></a>
### 25. PowerShell → C (PowerShell 7.6 → ISO C11)

#### 规则 PS-C-01：PowerShell 动态对象管道向 C 底层字节流与固定结构体降级映射
1. **源码触发条件**：PowerShell 源码中通过管道传递具备属性的对象（如 `Get-Process | Select-Object Id, ProcessName`）。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 ISO C11（[WG14-N1570 §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：传递强类型 .NET PSObject 包装对象，下游通过属性名直接提取字段。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C 中定义明确的 `struct` 结构体，字段定宽且强类型化；管道传递转换为结构体指针数组或线性缓冲区循环处理。
   - *不适用条件*：严禁在 C 中尝试模拟动态属性反射字典，维护开销极大且容易内存泄漏。
5. **错误机械替换反例**：
   ```c
   // 错误：在 C 中使用字符串名值对链表模拟 PSObject，内存开销暴增且极易泄漏
   // 正确：定义具体的 C 结构体
   typedef struct {
       int32_t id;
       char name[64];
   } ProcessInfo;
   ```
6. **信息不足或实现相关时的处理**：若源对象属性动态不固定，提取所需字段子集并向用户确认。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)；[WG14-N1570 §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

#### 规则 PS-C-02：PowerShell 弱类型隐式转换向 C 严格显式转换与溢出防范映射
1. **源码触发条件**：PowerShell 源码中将字符串数字与整数直接混算（如 `'100' + 20` 或 `20 + '100'`）。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6；目标语言 ISO C11（[WG14-N1570 §6.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：PowerShell 根据左操作数类型决定是执行字符串拼接（`'100' + 20 -> '10020'`）还是数值相加（`20 + '100' -> 120`）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C 语言中严禁依赖隐式转换！数值计算显式调用 `strtol` 转换并校验错误；字符串拼接显式使用 `snprintf`。
   - *不适用条件*：严禁直接使用 `atoi`（不提供溢出检查与非法字符位置检测）。
5. **错误机械替换反例**：
   ```c
   // 错误：使用 atoi 未检测错误，非法输入时静默返回 0
   int val = atoi(str);
   // 正确：使用 strtol 校验合法性
   char* endptr;
   long val = strtol(str, &endptr, 10);
   if (*endptr != '\0') { /* 解析失败处理 */ }
   ```
6. **信息不足或实现相关时的处理**：标记由于操作数顺序导致语义分化的潜在风险。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

#### 规则 PS-C-03：PowerShell 错误偏好与 $LASTEXITCODE 向 C 显式错误状态码映射
1. **源码触发条件**：PowerShell 源码中配置 `$ErrorActionPreference` 并检查 `$LASTEXITCODE`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables), [MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)）；目标语言 ISO C11。
3. **原可观察行为**：非终止错误被忽略或打印，最后外部程序退出码被 `$LASTEXITCODE` 记录。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C 中每一步系统调用显式检查返回值与 `errno`，在 `main` 退出时通过 `return code;` 或 `exit(code)` 回传。
   - *不适用条件*：严禁在 C 语言中忽略系统调用返回值。
5. **错误机械替换反例**：
   ```c
   // 错误：忽略文件移除返回值，与 PS 的非终止错误静默继续不同，在底层引发数据不一致
   remove(filepath); // 未检查返回值！
   // 正确：显式检查并记录
   if (remove(filepath) != 0) {
       perror("remove failed");
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及外部进程执行，加载 [`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)；[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)。

---

<a id="powershell-to-cpp"></a>
### 26. PowerShell → C++ (PowerShell 7.6 → ISO C++17)

#### 规则 PS-CPP-01：PowerShell 脚本块 (ScriptBlock) 向 C++17 lambda 闭包映射
1. **源码触发条件**：PowerShell 源码中使用 `{ param($x) $x * 2 }` 定义脚本块并作为参数传递。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6；目标语言 ISO C++17（[WG21-N4659 Clause 8.1.5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：脚本块延迟调用，可访问并修改调用栈上下文变量。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 C++17 lambda 表达式，通用存储使用 `std::function<R(Args...)>`；若涉及局部引用捕获 `[&]`，必须保证 lambda 生命周期不超过被捕获变量的作用域。
   - *不适用条件*：严禁将持有引用捕获 `[&]` 的 lambda 跨线程传递或脱离作用域返回（会导致悬挂引用解引用 UB）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：引用捕获局部变量后逃逸，引发悬垂引用未定义行为
   std::function<int()> MakeAdder(int x) {
       return [&x]() { return x + 1; }; // 严重错误：x 是局部形参，函数退出后引用失效！
   }
   // 正确：使用值捕获 [=] 或显式转移
   std::function<int()> MakeAdder(int x) {
       return [x]() { return x + 1; };
   }
   ```
6. **信息不足或实现相关时的处理**：若脚本块动态修改了外层作用域变量，在转换报告中标明生命周期约束。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 8.1.5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

#### 规则 PS-CPP-02：PowerShell 终止错误向 C++17 结构化异常体系映射
1. **源码触发条件**：PowerShell 源码中使用 `throw "Error message"` 或捕捉到终止错误。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）；目标语言 ISO C++17（[WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：终止当前执行管道，向上回溯调用栈。
4. **目标可选写法和不适用条件**：
   - *可选映射*：抛出继承自 `std::exception` 的 C++ 异常（如 `std::runtime_error("...")`），上层使用 `try ... catch` 捕获。
   - *不适用条件*：严禁抛出非 `std::exception` 派生的裸字符串或整数字面量（如 `throw "err";`），违背 C++ 现代异常安全规范。
5. **错误机械替换反例**：
   ```cpp
   // 错误：抛出裸字符串字面量，难以进行统一的多态异常捕获
   throw "operation failed"; // 无法被 catch (const std::exception&) 捕获！
   // 正确：抛出标准异常派生类
   throw std::runtime_error("operation failed");
   ```
6. **信息不足或实现相关时的处理**：若需要还原 PowerShell 的原生报错格式，封装包含错误信息的派生异常类。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)；[WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

#### 规则 PS-CPP-03：PowerShell ForEach-Object -Parallel 向 C++17 线程池与同步映射
1. **源码触发条件**：PowerShell 源码中使用 `$items | ForEach-Object -Parallel { ... }` 并发处理。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）；目标语言 ISO C++17。
3. **原可观察行为**：利用 Runspace 线程池在多个线程并发执行脚本块。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `std::async(std::launch::async, ...)` 配合 `std::future`，或使用固定工作线程池；共享资源使用 `std::mutex` 保护。
   - *不适用条件*：严禁在无同步原语下并发写入 C++ 容器（如 `std::vector::push_back`），直接引发内存重配数据竞争崩溃。
5. **错误机械替换反例**：
   ```cpp
   // 错误：多线程无锁并发 push_back
   std::vector<int> out;
   // 多个线程同时 out.push_back(val); // 致命崩溃：内部缓冲区重分配数据竞争！
   // 正确：加锁保护
   std::mutex mtx;
   {
       std::lock_guard<std::mutex> lock(mtx);
       out.push_back(val);
   }
   ```
6. **信息不足或实现相关时的处理**：若代码涉及操作系统线程亲和性，加载 [`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)；[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

---

<a id="powershell-to-csharp"></a>
### 27. PowerShell → C# (PowerShell 7.6 → C# 12 / .NET 8)

#### 规则 PS-CS-01：PowerShell 哈希表与动态对象向 C# Dictionary 与强类型类映射
1. **源码触发条件**：PowerShell 源码中定义哈希表 `@{ key = 'val' }` 或 `[PSCustomObject]@{ ... }`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables)）；目标语言 C# 12 / .NET 8（[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators)）。
3. **原可观察行为**：无序哈希映射，支持动态添加字段。
4. **目标可选写法和不适用条件**：
   - *可选映射*：键值对映射转换为 `Dictionary<string, string>` 或 `Dictionary<string, object>`；对于具备固定字段的对象，转换为 C# `class` 或 `record`。
   - *不适用条件*：严禁在 C# 中滥用 `dynamic` 或 `ExpandoObject`，这会丢失编译期强类型检查并增加 DLR 运行时开销。
5. **错误机械替换反例**：
   ```csharp
   // 错误：在 C# 中大量使用 dynamic 模拟 PowerShell 动态属性
   dynamic obj = new System.Dynamic.ExpandoObject();
   obj.Name = "test"; // 丢失全部强类型智能提示与编译检查，拼写错误在运行期才暴露！
   // 正确：定义明确的模型类
   public record UserProfile(string Name);
   ```
6. **信息不足或实现相关时的处理**：若使用了 `[ordered]@{}`，在 C# 中映射为 `OrderedDictionary` 或保持插入顺序的集合。
7. **直接官方 HTTPS 依据链接**：[MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables)；[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators)。

#### 规则 PS-CS-02：PowerShell 数组 += 扩容向 C# List<T> 动态集合映射
1. **源码触发条件**：PowerShell 源码中使用 `$arr = @(); $arr += $item`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)）；目标语言 C# 12 / .NET 8（[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators)）。
3. **原可观察行为**：每次 `+=` 都在底层分配新数组并全量拷贝旧元素。
4. **目标可选写法和不适用条件**：
   - *可选映射*：直接转换为 C# `List<T>`，调用 `.Add(item)` 获得均摊 $O(1)$ 的扩容性能。
   - *不适用条件*：严禁在 C# 中使用 `Array.Resize(ref arr, arr.Length + 1)` 机械模拟 PS 的 `+=` 行为。
5. **错误机械替换反例**：
   ```csharp
   // 错误：在 C# 中每次循环 Array.Resize
   int[] arr = Array.Empty<int>();
   for (int i = 0; i < 10000; i++) {
       Array.Resize(ref arr, arr.Length + 1); // 性能极其低下，O(N^2) 全量内存拷贝
       arr[^1] = i;
   }
   // 正确：使用 List<int>
   var list = new List<int>();
   for (int i = 0; i < 10000; i++) list.Add(i);
   ```
6. **信息不足或实现相关时的处理**：若数组最终固定且不修改，调用 `.ToArray()` 封闭。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)；[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators)。

#### 规则 PS-CS-03：PowerShell 环境变量与作用域向 C# Environment 与命名空间映射
1. **源码触发条件**：PowerShell 源码中使用 `$env:VAR_NAME` 读取或设置环境变量。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6；目标语言 C# 12 / .NET 8。
3. **原可观察行为**：直接访问当前进程环境变量。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `Environment.GetEnvironmentVariable("VAR_NAME")` 与 `Environment.SetEnvironmentVariable("VAR_NAME", val)`。
   - *不适用条件*：注意环境变量返回值在不存在时为 `null`，必须做好空值检查（`??`）。
5. **错误机械替换反例**：
   ```csharp
   // 错误：未做 null 检查直接使用，引发 NullReferenceException
   string path = Environment.GetEnvironmentVariable("MY_PATH")!;
   int len = path.Length; // 若环境变量不存在直接崩溃！
   // 正确：使用空合并运算符
   string path = Environment.GetEnvironmentVariable("MY_PATH") ?? string.Empty;
   ```
6. **信息不足或实现相关时的处理**：若包含特定平台注册表或驱动器虚拟路径，加载 [`skills/systems/posix-windows-filesystem/SKILL.md`](../systems/posix-windows-filesystem/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)。

---

<a id="powershell-to-python"></a>
### 28. PowerShell → Python (PowerShell 7.6 → CPython 3.12)

#### 规则 PS-PY-01：PowerShell 管道命令链向 Python 迭代器生成器与高阶函数映射
1. **源码触发条件**：PowerShell 源码中使用 `$input | Where-Object { ... } | ForEach-Object { ... }`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：对象逐个在管道中流式传递，处理大流时不占用全部内存。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用生成器表达式 `(fn(x) for x in input if cond(x))` 保持流式惰性求值；若需立即全量结果，使用列表推导 `[fn(x) for x in input if cond(x)]`。
   - *不适用条件*：严禁在无限流上使用列表推导（会导致内存耗尽 OOM）。
5. **错误机械替换反例**：
   ```python
   # 错误：针对大文件流或无限生成流使用列表推导，撑爆内存
   # lines = [line.strip() for line in huge_file]
   # 正确：使用生成器表达式流式处理
   lines = (line.strip() for line in huge_file)
   ```
6. **信息不足或实现相关时的处理**：若源管道包含特定 Cmdlet（如 `Sort-Object`），在 Python 中需要物化为列表再排序。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)；[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

#### 规则 PS-PY-02：PowerShell 单元素解包机制向 Python 列表长度隔离映射
1. **源码触发条件**：PowerShell 源码中处理管道输出，当结果仅有一项时自动变为标量。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)）；目标语言 Python 3.12。
3. **原可观察行为**：PS 管道输出零个元素返回 `$null`，一个元素返回标量对象，两个以上返回 `object[]`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Python 函数必须保持确定的返回类型契约！若声明返回 `list`，无论空、单元素还是多元素，统一返回 `list`。
   - *不适用条件*：严禁在 Python 中模仿 PowerShell 的自动解包行为（根据元素数量动态返回标量或列表），会给调用方类型检查带来极大混乱。
5. **错误机械替换反例**：
   ```python
   # 错误：模仿 PowerShell 的动态类型展开，破坏 Python 确定性接口契约
   def query_items():
       results = fetch()
       if len(results) == 1: return results[0] # 破坏了返回 list 的约定！
       return results
   # 正确：统一返回 list
   def query_items() -> list[Item]:
       return fetch()
   ```
6. **信息不足或实现相关时的处理**：对现有调用方做出防御性 `isinstance(res, list)` 适配。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)。

#### 规则 PS-PY-03：PowerShell 退出码回写向 Python sys.exit 与返回值映射
1. **源码触发条件**：PowerShell 源码中使用 `exit $code` 或检查 `$LASTEXITCODE`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)）；目标语言 Python 3.12。
3. **原可观察行为**：回传退出状态码。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 CLI 入口处调用 `sys.exit(code)`；在普通模块函数中返回整数状态码或抛出异常。
   - *不适用条件*：严禁在被导入的模块内部直接调用 `sys.exit()`，会导致宿主解释器退出。
5. **错误机械替换反例**：
   ```python
   # 错误：在模块库函数内部调用 sys.exit
   def validate_config(cfg):
       if not cfg: sys.exit(1) # 导致第三方调用者进程无故终止！
   # 正确：抛出异常
   def validate_config(cfg):
       if not cfg: raise ValueError("Invalid configuration")
   ```
6. **信息不足或实现相关时的处理**：若需要调用外部原生命令并获取退出码，使用 `subprocess.run(..., check=False).returncode`。
7. **直接官方 HTTPS 依据链接**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

---

<a id="powershell-to-go"></a>
### 29. PowerShell → Go (PowerShell 7.6 → Go 1.27)

#### 规则 PS-GO-01：PowerShell 弱类型管道数据向 Go 显式结构体与切片映射
1. **源码触发条件**：PowerShell 源码中通过动态哈希表或对象管道传递松散属性。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 Go 1.27（[GO-SPEC #Struct_types](https://go.dev/ref/spec)）。
3. **原可观察行为**：弱类型反射访问，属性缺失返回 `$null`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Go 中定义静态 `type Record struct`，属性定义为显式字段；通过结构体切片 `[]Record` 批量传递。
   - *不适用条件*：严禁全部使用 `map[string]interface{}` 替代，会丧失静态编译检查且必须频繁进行类型断言。
5. **错误机械替换反例**：
   ```go
   // 错误：在 Go 中大量使用 map[string]any，类型断言失败引发运行时 panic
   m := map[string]any{"id": 1}
   id := m["id"].(string) // panic: interface conversion: any is int, not string
   // 正确：定义明确结构体
   type Record struct { ID int }
   ```
6. **信息不足或实现相关时的处理**：若源数据来自未知外部 JSON，结合 `json.Unmarshal` 到结构体进行验证。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Struct_types](https://go.dev/ref/spec)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

#### 规则 PS-GO-02：PowerShell 错误流重定向向 Go 显式 error 与 stderr 隔离映射
1. **源码触发条件**：PowerShell 源码中使用 `2>&1` 将错误流合并到标准输出，或判断 `$?`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables), [MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)）；目标语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec)）。
3. **原可观察行为**：PS 将错误记录混合进管道输出流。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Go 语言中严格区分数据返回与错误流！函数返回 `(Data, error)`；CLI 标准输出与标准错误分别写入 `os.Stdout` 和 `os.Stderr`。
   - *不适用条件*：严禁将普通业务错误信息直接格式化打印到标准输出而返回 `nil` error。
5. **错误机械替换反例**：
   ```go
   // 错误：将错误信息打印至 stdout 并返回 nil
   func Process() error {
       fmt.Println("Error: something failed")
       return nil // 调用方误以为成功！
   }
   // 正确：返回 error
   func Process() error {
       return errors.New("something failed")
   }
   ```
6. **信息不足或实现相关时的处理**：若原脚本调用了原生可执行程序并重定向输出，加载 [`skills/scenes/file-io/SKILL.md`](../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Errors](https://go.dev/ref/spec)；[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

#### 规则 PS-GO-03：PowerShell Start-ThreadJob 向 Go Goroutine 轻量并发与 WaitGroup 映射
1. **源码触发条件**：PowerShell 源码中使用 `Start-ThreadJob` 启动后台任务。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）；目标语言 Go 1.27（[GO-SPEC #Go_statements](https://go.dev/ref/spec)）。
3. **原可观察行为**：在后台 Runspace 线程池中并发执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `go worker()`，主线程使用 `sync.WaitGroup` 等待全部任务退出。
   - *不适用条件*：严禁在启动 Goroutine 时捕获循环迭代变量（Go 1.22 虽修正循环变量作用域，但保持显式传参是最佳防错实践）；共享数据必须同步。
5. **错误机械替换反例**：
   ```go
   // 错误：启动后台 Goroutine 未做同步等待，主函数提前退出导致后台任务被杀死
   func main() {
       go doBackground()
   } // main 退出，所有 Goroutine 立即终止！
   // 正确：使用 sync.WaitGroup
   func main() {
       var wg sync.WaitGroup
       wg.Add(1)
       go func() { defer wg.Done(); doBackground() }()
       wg.Wait()
   }
   ```
6. **信息不足或实现相关时的处理**：若需获取后台任务返回值，结合 Channel 传递。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Go_statements](https://go.dev/ref/spec)；[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)。

---

<a id="powershell-to-ruby"></a>
### 30. PowerShell → Ruby (PowerShell 7.6 → CRuby 3.4)

#### 规则 PS-RB-01：PowerShell 管道流式传输向 Ruby Enumerable 链式方法调用映射
1. **源码触发条件**：PowerShell 源码中使用 `$data | Where-Object { ... } | ForEach-Object { ... }`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：对象逐个通过管道过滤与投影。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 Ruby `Enumerable` 链式调用：`data.select { |x| ... }.map { |x| ... }`；若针对大集合需惰性求值，在链首追加 `.lazy`（如 `data.lazy.select { ... }.map { ... }`）。
   - *不适用条件*：严禁直接在巨型数组上链式调用全量数组生成方法，避免多次中间数组分配。
5. **错误机械替换反例**：
   ```ruby
   # 错误：对超大流未使用 lazy，导致连续创建多重巨型中间数组引发内存溢出
   # huge_data.select { ... }.map { ... }
   # 正确：使用 .lazy 保持管道惰性流式计算
   huge_data.lazy.select { |x| x.valid? }.map { |x| x.process }
   ```
6. **信息不足或实现相关时的处理**：若源数据为哈希表，注意 Ruby 中迭代得到的是 `[key, value]` 数组。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

#### 规则 PS-RB-02：PowerShell 非终止错误策略向 Ruby 显式 rescue 代码块映射
1. **源码触发条件**：PowerShell 源码中使用 `$ErrorActionPreference = 'SilentlyContinue'` 忽略命令错误。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)）；目标语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）。
3. **原可观察行为**：命令遇到非终止错误时不中断脚本，静默跳过继续执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Ruby 中对易出错的方法显式包裹 `begin ... rescue StandardError ... end`，或在单行使用 `action rescue nil`（仅限明确无副作用的只读探测）。
   - *不适用条件*：严禁在关键文件写或网络通信中滥用全局 `rescue nil`，会掩盖权限或路径等严重错误。
5. **错误机械替换反例**：
   ```ruby
   # 错误：滥用 rescue nil 掩盖核心业务异常
   File.write(target_path, content) rescue nil # 若目录不存在或无权限，静默失败且无日志！
   # 正确：针对性捕获并处理
   begin
     File.write(target_path, content)
   rescue SystemCallError => e
     warn "Write failed: #{e.message}"
   end
   ```
6. **信息不足或实现相关时的处理**：在报告中列出所有被降级为静默忽略的错误点。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)。

#### 规则 PS-RB-03：PowerShell 字符转义反引号向 Ruby 双引号标准转义映射
1. **源码触发条件**：PowerShell 源码中使用反引号进行转义（如 `` `n `` 代表换行，`` `t `` 代表制表符，`` `$ `` 代表转义美元符）。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：PowerShell 特有的反引号作为转义前缀。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Ruby 双引号标准转义字符（`\n`, `\t`）；变量内插转换为 `#{var}`。
   - *不适用条件*：严禁在 Ruby 字符串中保留反引号转义字符，Ruby 双引号中反引号没有转义语义，会导致字面残留 `\``。
5. **错误机械替换反例**：
   ```ruby
   # 错误：将 PS 的反引号转义原样保留
   text = "`nHello" # 在 Ruby 中输出的是 "`nHello" 字面量，而不是换行！
   # 正确：转换为标准反斜杠转义
   text = "\nHello"
   ```
6. **信息不足或实现相关时的处理**：扫描源码所有反引号转义并做正规化替换。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

---

## 七、以 Ruby 语言为源语言的剩余方向 (6 个方向)

<a id="ruby-to-c"></a>
### 31. Ruby → C (CRuby 3.4 → ISO C11)

#### 规则 RB-C-01：Ruby 真值模型 (0 为真) 向 C 条件分支逻辑翻转防范映射
1. **源码触发条件**：Ruby 源码中使用 `if val`，且 `val` 的计算结果可能为数值 `0`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 ISO C11（[WG14-N1570 §6.8.4.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：**在 Ruby 中 `0` 为真（Truthy）**，`if 0` 分支必然进入执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C 语言中 `0` 代表假！若源 Ruby 代码依赖了 `0` 为真（即仅有 `nil` 或 `false` 时才不执行），在 C 中必须显式转换为检查“是否存在/有效”的标志位；若该变量本身是业务状态码，必须显式重写条件。
   - *不适用条件*：**致命禁区**：严禁直接机械翻译为 C 的 `if (val)`，因为当 `val == 0` 时，C 语言会判定为假直接跳过分支，导致逻辑 100% 翻转！
5. **错误机械替换反例**：
   ```c
   // 错误：Ruby 原型为 if val (val 可能为 0，依然执行分支)
   // 在 C 中直接写 if (val)：
   int val = 0;
   if (val) { // 错误：在 C 中 0 为假，分支被跳过！与 Ruby 运行结果相反！
       action();
   }
   // 正确：显式检查是否有效
   if (is_valid) {
       action();
   }
   ```
6. **信息不足或实现相关时的处理**：在报告中标记所有由 Ruby 真值模型引发的潜在条件歧义。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[WG14-N1570 §6.8.4.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

#### 规则 RB-C-02：Ruby 动态方法派发与开放类向 C 固定数据结构与函数指针映射
1. **源码触发条件**：Ruby 源码中使用动态方法查找、`send(:method_name)` 或在运行期动态给类增加方法。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 ISO C11。
3. **原可观察行为**：运行期动态通过符号查找方法实现并分派。
4. **目标可选写法和不适用条件**：
   - *可选映射*：完全静态化具化为固定函数；若必须支持动态多态，定义包含显式函数指针的虚表结构体（VTable）。
   - *不适用条件*：C 语言为静态编译，严禁在 C 中尝试模拟字符串形式的符号分派。
5. **错误机械替换反例**：
   ```c
   // 错误：在 C 中尝试用字符串比较模拟动态分发，性能低下且无编译检查
   // 正确：使用函数指针表
   typedef struct {
       void (*action)(void* ctx);
   } OperationVTable;
   ```
6. **信息不足或实现相关时的处理**：若源元编程极度复杂，将不可静态化的部分列为未验证阻断项。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

#### 规则 RB-C-03：Ruby 异常展开向 C 返回值错误码与 goto cleanup 释放映射
1. **源码触发条件**：Ruby 源码中使用 `raise` 抛出异常并在外层 `rescue`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 ISO C11（[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：异常展开栈帧，执行 `ensure` 块，最后被 `rescue` 捕获。
4. **目标可选写法和不适用条件**：
   - *可选映射*：函数返回整数错误码；在函数末尾定义 `cleanup:` 标签，各失败点通过 `goto cleanup;` 集中释放已分配资源。
   - *不适用条件*：严禁在 C 语言中忽略分配的资源直接提前返回。
5. **错误机械替换反例**：
   ```c
   // 错误：模拟异常提前退出导致资源未释放
   char* buf = malloc(1024);
   if (check() < 0) return -1; // 错误：buf 泄漏！
   free(buf);
   // 正确：goto cleanup 确保释放
   int ret = 0;
   char* buf = malloc(1024);
   if (check() < 0) { ret = -1; goto cleanup; }
   cleanup:
   free(buf);
   return ret;
   ```
6. **信息不足或实现相关时的处理**：记录异常消息传递降级。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

<a id="ruby-to-cpp"></a>
### 32. Ruby → C++ (CRuby 3.4 → ISO C++17)

#### 规则 RB-CPP-01：Ruby 开放类与猴子补丁向 C++17 装饰器/组合模式重构映射
1. **源码触发条件**：Ruby 源码中打开已有类（如标准类 `String` 或第三方类）追加新方法（Monkey Patching）。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 ISO C++17（[WG21-N4659 Clause 12](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：全局范围内所有该类实例均获得新方法。
4. **目标可选写法和不适用条件**：
   - *可选映射*：C++ 封闭已有类！严禁尝试直接给 `std::string` 加成员函数。必须重构为独立的命名空间自由函数（`namespace utils { void MyFunc(const std::string&); }`），或定义派生类/包装类。
   - *不适用条件*：严禁向 `std` 命名空间添加自定义函数（根据 ISO C++ 规范此举属于未定义行为 UB！）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：向 std 命名空间注入自由函数（标准未定义行为 UB！）
   namespace std {
       void my_extension(string& s) { ... } // 严重违反 C++ 标准规范！
   }
   // 正确：定义独立的工具命名空间
   namespace MyProject::StringUtils {
       void MyExtension(std::string& s) { ... }
   }
   ```
6. **信息不足或实现相关时的处理**：若源猴子补丁覆写了核心行为，在转换报告中标明侵入性修改已降级为显式调用。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 12](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

#### 规则 RB-CPP-02：Ruby 资源块模式 (File.open do...end) 向 C++17 RAII 作用域析构映射
1. **源码触发条件**：Ruby 源码中使用带有代码块的文件或网络打开操作。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4；目标语言 ISO C++17（[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：代码块执行完毕自动关闭底层资源句柄。
4. **目标可选写法和不适用条件**：
   - *可选映射*：利用 C++ 局部对象作用域析构特性（RAII），如 `std::ifstream file(path);`。
   - *不适用条件*：严禁在堆上 `new` 出文件对象而不妥善管理其指针生命周期。
5. **错误机械替换反例**：
   ```cpp
   // 错误：在堆上创建流指针且未保护释放
   auto f = new std::ifstream(path);
   // 正确：使用局部栈对象
   std::ifstream f(path);
   ```
6. **信息不足或实现相关时的处理**：若涉及底层文件系统路径跨平台差异，加载 [`skills/systems/posix-windows-filesystem/SKILL.md`](../systems/posix-windows-filesystem/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

#### 规则 RB-CPP-03：Ruby Thread 并发向 C++17 std::thread 与数据竞争防范映射
1. **源码触发条件**：Ruby 源码中使用 `Thread.new` 处理并发任务。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：受 MRI GVL 保护，基础数据结构读写不会引发内存重排崩溃。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `std::thread`；**关键差异**：C++ 没有 GVL！任何跨线程共享的数据结构（如 `std::vector` 或类成员）必须显式施加 `std::mutex` 保护，否则在 C++ 中直接触发未定义行为（Data Race UB）导致内存损坏或崩溃。
   - *不适用条件*：严禁在无互斥锁保护下直接照抄 Ruby 中对共享变量的读写。
5. **错误机械替换反例**：
   ```cpp
   // 错误：认为像 Ruby 一样可以直接多线程对数组 push
   std::vector<int> shared_vec;
   // thread 1 & thread 2: shared_vec.push_back(1); // 致命 UB 崩溃！
   // 正确：显式互斥锁同步
   std::mutex mtx;
   {
       std::lock_guard<std::mutex> lock(mtx);
       shared_vec.push_back(1);
   }
   ```
6. **信息不足或实现相关时的处理**：若代码涉及原子标量，改用 `std::atomic<T>`。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)。

---

<a id="ruby-to-csharp"></a>
### 33. Ruby → C# (CRuby 3.4 → C# 12 / .NET 8)

#### 规则 RB-CS-01：Ruby Module/Mixin 多继承向 C# 接口多继承与扩展方法映射
1. **源码触发条件**：Ruby 源码中通过 `include MyModule` 将模块的方法混入类继承链中。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-MODULE](https://docs.ruby-lang.org/en/3.4/Module.html)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：模块内的方法动态插入到宿主类的祖先继承链（`ancestors`）中。
4. **目标可选写法和不适用条件**：
   - *可选映射*：将 Module 转换为 C# 的 `interface`，配合 C# 8+ 接口默认实现（Default Interface Methods）或静态扩展方法（Extension Methods）；若包含实例状态，必须在宿主类中维护字段。
   - *不适用条件*：严禁在 C# 中尝试继承多个基类。
5. **错误机械替换反例**：
   ```csharp
   // 错误：试图在 C# 中多继承类模拟 Module
   // public class User : BaseEntity, LogModule { } // 编译报错！
   // 正确：使用接口与默认方法或扩展方法
   public interface ILogModule {
       void Log(string msg) => Console.WriteLine($"LOG: {msg}");
   }
   public class User : BaseEntity, ILogModule { }
   ```
6. **信息不足或实现相关时的处理**：若模块内通过 `prepend` 劫持了父类方法，转换为显式装饰器模式。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-MODULE](https://docs.ruby-lang.org/en/3.4/Module.html)；[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)。

#### 规则 RB-CS-02：Ruby 符号 (:symbol) 对象向 C# 枚举或常量字符串映射
1. **源码触发条件**：Ruby 源码中大量使用 `:active`、`:pending` 等不可变 Symbol 对象作为状态标记或散列键。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：全局唯一的不可变标识符，整数比对速度，不被常规垃圾回收频繁重复分配。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若属于离散状态值，映射为 C# 强类型 `enum`；若属于动态字符串键，映射为 `const string` 或普通 `string`。
   - *不适用条件*：严禁为每个符号在 C# 堆上动态拼接字符串，避免无谓的内存开销。
5. **错误机械替换反例**：
   ```csharp
   // 错误：将固定的符号状态当成弱类型字符串散落各处，容易拼写错误
   if (status == "pending") { ... }
   // 正确：映射为强类型 enum
   public enum Status { Active, Pending }
   if (status == Status.Pending) { ... }
   ```
6. **信息不足或实现相关时的处理**：若 Symbol 来自外部输入动态生成，映射为 `string`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

#### 规则 RB-CS-03：Ruby rescue StandardError 捕获向 C# catch (Exception) 映射
1. **源码触发条件**：Ruby 源码中使用 `rescue => e` 处理业务异常。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）。
3. **原可观察行为**：默认只捕获 `StandardError` 及其子类，系统级致命错误自动放行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C# 中捕获 `catch (Exception ex)`（C# 的 `System.Exception` 对应常规托管异常）。
   - *不适用条件*：注意在 C# 中不可使用空 catch 块 `catch { }` 吞没异常信息。
5. **错误机械替换反例**：
   ```csharp
   // 错误：空 catch 吞没异常，导致关键调试信息丢失
   try { Action(); } catch { }
   // 正确：显式捕获并记录
   try { Action(); } catch (Exception ex) { Logger.LogError(ex); }
   ```
6. **信息不足或实现相关时的处理**：若 Ruby 抛出特定异常，映射至对应的 .NET 异常类型。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)。

---

<a id="ruby-to-python"></a>
### 34. Ruby → Python (CRuby 3.4 → CPython 3.12)

#### 规则 RB-PY-01：Ruby 与 Python 真值模型 (0, "" 真假异同) 冲突防反转映射
1. **源码触发条件**：Ruby 源码中使用 `if obj`，且 `obj` 可能为 `0` 或空字符串 `""`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：**在 Ruby 中 `0` 与 `""` 均为真（Truthy）**，分支必然执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：**在 Python 中 `0` 与 `""` 均为假（Falsy）**！若原 Ruby 意图是判断对象是否存在（即非 `nil`），在 Python 中必须显式写为 `if obj is not None:`！
   - *不适用条件*：**绝对禁止直接翻译为 `if obj:`**！当 `obj == 0` 时，Python 判定为假导致分支被跳过，控制流发生完全逆转！
5. **错误机械替换反例**：
   ```python
   # 错误：Ruby 原型为 if val (val 可能为 0，依然执行分支)
   # 在 Python 中直接写 if val:
   val = 0
   if val: # 错误：在 Python 中 0 为 Falsy，分支被意外跳过！
       do_action()
   # 正确：显式检查是否为 None
   if val is not None:
       do_action()
   ```
6. **信息不足或实现相关时的处理**：对每个无显式操作符的条件表达式，结合上下文标注真值映射依据。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

#### 规则 RB-PY-02：Ruby 代码块 (Block/yield) 向 Python 回调函数与生成器映射
1. **源码触发条件**：Ruby 源码中使用 `def my_each; yield item; end` 或传递代码块。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4；目标语言 CPython 3.12（[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)）。
3. **原可观察行为**：隐式代码块接收并调用 `yield`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若用于迭代，改写为 Python 的 `yield` 生成器函数；若用于回调处理，定义显式函数参数 `callback: Callable` 并显式调用 `callback(item)`。
   - *不适用条件*：严禁在 Python 中省略回调参数，Python 没有 Ruby 的隐式代码块机制。
5. **错误机械替换反例**：
   ```python
   # 错误：试图在普通函数中直接使用 yield 但期望它表现为外部传入的回调
   # 正确：显式接收可调用对象
   def for_each(items, callback):
       for item in items:
           callback(item)
   ```
6. **信息不足或实现相关时的处理**：若代码块包含 `break` 提前退出且向外层返回值，改写为显式循环。
7. **直接官方 HTTPS 依据链接**：[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)。

#### 规则 RB-PY-03：Ruby 字符串内建 Encoding 向 Python str/bytes 隔离映射
1. **源码触发条件**：Ruby 源码中调用 `str.encoding`、`str.force_encoding` 或处理二进制 `ASCII-8BIT` 字符串。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：Ruby 中 `String` 是字节序列并附带编码标签。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若编码为 `ASCII-8BIT` / `BINARY`，映射为 Python 原生 `bytes`；若为文本（如 `UTF-8`），映射为 Python `str`；互转必须显式 `.encode()` / `.decode()`。
   - *不适用条件*：严禁在 Python 中将二进制数据当成 `str`，或混淆两者进行隐式拼接。
5. **错误机械替换反例**：
   ```python
   # 错误：将字节流与文本字符串直接相加
   b = b"header:"
   s = "data"
   # msg = b + s # 抛出 TypeError: can't concat str to bytes
   # 正确：统一类型再拼接
   msg = b + s.encode('utf-8')
   ```
6. **信息不足或实现相关时的处理**：若字符串来源不可信，使用 `errors='replace'` 或在报告中标记转码风险。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

---

<a id="ruby-to-go"></a>
### 35. Ruby → Go (CRuby 3.4 → Go 1.27)

#### 规则 RB-GO-01：Ruby 动态鸭子类型向 Go 显式接口定义与满足映射
1. **源码触发条件**：Ruby 源码中依赖对象具备某个方法即可调用（鸭子类型），未声明显式继承或接口。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4；目标语言 Go 1.27（[GO-SPEC #Interface_types](https://go.dev/ref/spec)）。
3. **原可观察行为**：运行期只要响应方法（`respond_to?`）即调用成功，否则抛出 `NoMethodError`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Go 中显式定义 `type Duck interface { Method() }`，Go 结构体只需拥有对应签名的方法即可自动、隐式满足该接口，完美契合鸭子类型本质。
   - *不适用条件*：严禁使用 `interface{}` / `any` 加大量的运行时反射（`reflect`），会极大破坏 Go 性能与静态类型安全。
5. **错误机械替换反例**：
   ```go
   // 错误：滥用 reflect 反射调用方法模拟鸭子类型
   func Invoke(obj any) {
       reflect.ValueOf(obj).MethodByName("Action").Call(nil) // 脆弱、极其低效
   }
   // 正确：定义精确接口
   type Actioner interface { Action() }
   func Invoke(obj Actioner) { obj.Action() }
   ```
6. **信息不足或实现相关时的处理**：若对象响应的方法集极度动态，提取公共最小子集接口。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Interface_types](https://go.dev/ref/spec)。

#### 规则 RB-GO-02：Ruby 异常控制流向 Go 显式多返回值 (T, error) 映射
1. **源码触发条件**：Ruby 源码中使用 `raise CustomError.new(...)` 并依赖多层拦截。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec)）。
3. **原可观察行为**：抛出异常后中断当前调用链。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重写为 Go 的 `(T, error)` 返回值；在调用点逐层处理。
   - *不适用条件*：严禁将业务异常机械翻译为 Go `panic`。
5. **错误机械替换反例**：
   ```go
   // 错误：将 Ruby 的常规业务异常翻译为 panic
   func Validate(age int) {
       if age < 0 { panic("invalid age") } // 错误：导致不可预期的崩溃！
   }
   // 正确：返回 error
   func Validate(age int) error {
       if age < 0 { return errors.New("invalid age") }
       return nil
   }
   ```
6. **信息不足或实现相关时的处理**：若原 Ruby 错误存在丰富字段，定义包含相同字段的 Go 结构体。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[GO-SPEC #Errors](https://go.dev/ref/spec)。

#### 规则 RB-GO-03：Ruby 任意精度数值向 Go 定宽整数模截断防溢出映射
1. **源码触发条件**：Ruby 源码中使用大整数算术或位运算。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 Go 1.27（[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)）。
3. **原可观察行为**：数值任意精度，无固定溢出边界。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若数值在 64 位内，使用 `int64`/`uint64`，注意溢出时 Go 是按模截断回绕（不会抛出异常）；若需保持无限精度，使用 `math/big.Int`。
   - *不适用条件*：严禁在数值可能超过 64 位时仍然采用裸 `int`。
5. **错误机械替换反例**：
   ```go
   // 错误：在 Go 中使用普通 int 进行超大数计算导致溢出截断
   // Ruby: 2**100
   var x int64 = 1 << 100 // 编译报错或溢出！
   // 正确：使用 big.Int
   x := new(big.Int).Exp(big.NewInt(2), big.NewInt(100), nil)
   ```
6. **信息不足或实现相关时的处理**：若无法确定上限，优先使用 `math/big` 并在报告中提示性能开销。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

---

<a id="ruby-to-powershell"></a>
### 36. Ruby → PowerShell (CRuby 3.4 → PowerShell 7.6)

#### 规则 RB-PS-01：Ruby 动态方法与哈希向 PowerShell PSCustomObject 映射
1. **源码触发条件**：Ruby 源码中定义包含动态方法或属性的纯数据对象，或操作复杂 `Hash`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)）；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）。
3. **原可观察行为**：通过方法或键访问对象属性。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `[PSCustomObject]`；若需附加动态计算方法，使用 `Add-Member -MemberType ScriptMethod`。
   - *不适用条件*：严禁在 PowerShell 中使用不稳定的字符串哈希键拼接访问。
5. **错误机械替换反例**：
   ```powershell
   # 错误：在 PowerShell 中直接调用未绑定的哈希表属性方法
   $h = @{ Name = "test" }
   # $h.DoAction() 报错：MethodInvocationException
   # 正确：使用 PSCustomObject 加 ScriptMethod
   $obj = [PSCustomObject]@{ Name = "test" }
   $obj | Add-Member -MemberType ScriptMethod -Name "DoAction" -Value { Write-Output $this.Name }
   ```
6. **信息不足或实现相关时的处理**：若包含深度嵌套字典，使用自定义递归包装。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

#### 规则 RB-PS-02：Ruby 异常捕获向 PowerShell 终止错误与 $? 状态映射
1. **源码触发条件**：Ruby 源码中使用 `rescue` 捕获异常并返回降级值。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 PowerShell 7.6（[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）。
3. **原可观察行为**：捕获异常并执行恢复分支。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 PowerShell 中使用 `try { ... } catch { ... }` 结构。
   - *不适用条件*：必须注意若调用外部命令产生非零退出码，它不会触发 PowerShell 的 `catch`（必须手动检查 `$LASTEXITCODE -ne 0`）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：以为 try-catch 能捕获外部命令行程序的非零退出码
   try {
       git clone invalid_url # 原生程序报错退出，返回码非零，但不触发 catch！
   } catch {
       Write-Output "Clone failed" # 永远进不来！
   }
   # 正确：显式检查 $LASTEXITCODE
   git clone invalid_url
   if ($LASTEXITCODE -ne 0) {
       Write-Error "Clone failed with exit code $LASTEXITCODE"
   }
   ```
6. **信息不足或实现相关时的处理**：区分内部 Cmdlet 异常与外部进程退出码。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)。

#### 规则 RB-PS-03：Ruby 字符串内插与正则表达式向 PowerShell 语法适配映射
1. **源码触发条件**：Ruby 源码中使用 `"hello #{name}"` 字符串内插或 `/pattern/` 正则表达式字面量。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4；目标语言 PowerShell 7.6。
3. **原可观察行为**：双引号内插表达式；正则作为一等对象。
4. **目标可选写法和不适用条件**：
   - *可选映射*：PowerShell 双引号支持变量内插 `"hello $name"` 或子表达式 `"hello $($user.Name)"`；正则比对使用 `-match` 操作符，匹配结果存放在自动变量 `$Matches` 中。
   - *不适用条件*：严禁在 PowerShell 中直接保留 Ruby 的 `#{...}` 语法（PowerShell 会原样输出 `#{...}` 字面量）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：在 PowerShell 中照抄 Ruby 的内插语法
   $name = "Alice"
   $str = "Hello #{name}" # 输出 "Hello #{name}"，内插彻底失效！
   # 正确：使用 PowerShell 内插语法
   $str = "Hello $name"
   # 或包含复杂属性时使用子表达式
   $str = "Hello $($user.Name)"
   ```
6. **信息不足或实现相关时的处理**：扫描所有正则修饰符，确保与 .NET 正则引擎选项对应。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。
