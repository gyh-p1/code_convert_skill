---
name: c-to-powershell
description: Use when converting C source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C → PowerShell 语言转换规则

> **适用基线**：ISO C11 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C](../../references/languages/c.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
> **方向案例与证据**：如本地工作区存在 `docs/test/dataset/c-to-powershell/README.md`，按其中 case 分层查看；该本地数据目录不随 Git/Skill 分发。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C → PowerShell 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 C-PS-01：C 裸字节流与缓冲区向 PowerShell 字节数组与字符编码 (utf8NoBOM) 映射
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

### 规则 C-PS-02：C 退出码与 exit(code) 向 PowerShell $LASTEXITCODE 与终止错误分流映射
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

### 规则 C-PS-03：C 多线程并发向 PowerShell Start-ThreadJob 与 Runspace 隔离映射
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
6. **信息不足或实现相关时的处理**：若涉及系统级进程派生，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)。

### 规则 C-PS-04：C 定宽/数据模型相关整型与隐式提升向 PowerShell .NET 整数类型与显式掩码映射
1. **源码触发条件**：C 源码混用 `unsigned long`/`size_t`/`long`/`uint32_t`/`DWORD`/`unsigned`（如 `unsigned long d_ino; unsigned long d_off;`、`const unsigned pipe_size = fcntl(...)`、`hax(char *filename, long offset, uint8_t *data, size_t len)`），或用 `sizeof(buffer)` 与 `unsigned` 比较、用 `(size_t)nbytes < len` 做符号转换比较、用 `~0x10000`/`0xFFFFFFFF` 依赖位宽回绕、用 `strlen(p) / 4` 这类整除求长度。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（[WG14-N1570 §6.2.5, §6.3.1.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)），且必须先冻结源数据模型（`long`/指针宽度随目标平台数据模型变化属实现相关事实）；目标语言 PowerShell 7.6（[MS-PS-ARITH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators), [MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)）。
3. **原可观察行为**：无符号类型按模 $2^n$ 回绕是合法确定性行为，有符号溢出是 UB；有符号/无符号混算把有符号操作数转换为无符号；整除与取模对被除数为负时的结果与向零截断不同；`(size_t)nbytes < len` 中的负值会被重新解释为极大无符号数。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 PowerShell 中显式声明宽度类型（`[int]`/`[long]`/`[uint32]`/`[uint64]`），比较前把两侧转成同一显式类型，需要 C 的按模回绕时显式掩码（`[uint32](($x -band 0xFFFFFFFF))`），并以 `[uint32]::MaxValue` 等 .NET 静态成员表达边界；`long`/`size_t` 按冻结后的数据模型映射为 `[long]`/`[uint64]`，并在报告中记录该数据模型假设。
   - *不适用条件*：严禁依赖 PowerShell 的自动类型提升——算术超出当前类型上限时引擎会提升为更宽整型（如 `[int64]`）或 `[double]`，这会破坏源码依赖的 32 位截断/回绕语义；严禁假定 `[uint32]`/`[int]` 强转与 C 的整型转换同义（C 的转换为按模转换，PowerShell 走 .NET 类型转换路径，对负值与越界值的行为不同，必须显式掩码或改用 `[BitConverter]`/`[System.Buffers.Binary.BinaryPrimitives]` 并在文档中写清假设）；严禁把 `~0x10000` 直译为 `-bnot 0x10000` 而不做位宽掩码（得到的是无限精度补码结果，不是 32 位取反）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：把 C 的 size_t/unsigned long 一律当 [int]（32 位），并依赖自动提升
   [int]$offset = $fileLength          # 源为 size_t（LP64 下 64 位），大偏移被截断
   $h = 0x9E3779B9
   $h = $h * 33                        # 源为 uint32_t 回绕；此处会被提升为更宽整型或 double
   $mask = -bnot 0x10000               # 源为 uint32 取反；此处是无限精度补码
   # 正确：冻结数据模型，显式宽度与掩码
   [uint64]$offset64 = [uint64]$fileLength
   [uint32]$h32 = 0x9E3779B9
   $h32 = [uint32](($h32 * 33) -band 0xFFFFFFFF)
   ```
6. **信息不足或实现相关时的处理**：源平台数据模型（LP64/LLP64）、`long`/`size_t` 的实际宽度、以及是否依赖回绕都属于未决事实；缺一即在转换报告中停标为待确认，不得用 PowerShell 默认类型顶替。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.2.5, §6.3.1.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[MS-PS-ARITH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators)；[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)。

### 规则 C-PS-05：C 部分完成返回值与错误分支向 PowerShell 管道、异常与错误流分流映射
1. **源码触发条件**：C 源码按 I/O 返回值控制循环并累加（`total_sent += sent`、`total += bytesRead`、`r -= n`），用 `if (nbytes < 0)`/`if (ret != 0)`/`if (recsock <= 0)` 分流失败，用 `perror`/`WSAGetLastError`/`GetLastError` 输出错误，或用 `return -1`/`EXIT_FAILURE` 表示失败。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（[WG14-N1570 §7.5, §7.21](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）与 POSIX 的读写返回约定（[POSIX](https://pubs.opengroup.org/onlinepubs/9699919799/)）；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines), [MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables), [MS-PS-TRY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）。
3. **原可观察行为**：C 的一个返回值同时表达"已完成字节数/失败/EOF"，部分完成必须由调用方循环补齐；错误经返回值加 `errno`/`GetLastError` 暴露；`perror` 只写标准错误流而不中断后续语句。
4. **目标可选写法和不适用条件**：
   - *可选映射*：逐调用点选择错误通道——.NET 方法（`[System.IO.FileStream]`/`[System.Net.Sockets.NetworkStream]`）失败抛异常，用 `try`/`catch` 捕获并读 `$_.Exception.Message`；cmdlet 失败走错误流，用 `-ErrorAction Stop` 或 `$ErrorActionPreference` 升级为终止错误；外部程序失败只体现在 `$LASTEXITCODE`，必须显式检查（`$?` 会被后续任意语句覆盖）。C 的部分写循环应改写为一次性 `Write`（.NET 流不返回已写字节数）或改用以偏移/`Position` 表达的显式循环，并在报告中声明"部分写"语义已由流实现承担。
   - *不适用条件*：严禁把 `if (n < 0)` 直译为 `if (-not $n)`（PowerShell 中 `0`、空值、空数组均为假，会把"0 字节/EOF"误判为失败，或反之）；严禁假定 `-ErrorAction` 能作用于 .NET 方法或外部程序（该参数只对 cmdlet 的错误流有效）；严禁在循环中用 `+=` 累积字节（每次 `+=` 分配新数组并全量复制）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：把 C 的部分写循环与"返回已写字节数"照搬到 .NET 流
   $totalSent = 0
   while ($totalSent -lt $total) {
       $sent = $stream.Write($buf, $totalSent, $total - $totalSent)  # Write 返回 void
       if (-not $sent) { break }                                     # $sent 为 $null => 恒为真，立即中断
       $totalSent += $sent
   }
   # 正确：一次写出，失败交给异常通道
   try { $stream.Write($buf, 0, $total) }
   catch { Write-Error "write failed: $($_.Exception.Message)"; throw }
   ```
6. **信息不足或实现相关时的处理**：交付形态（模块函数/脚本/独立进程）与"失败是否必须反映为进程退出码"不明时，必须停下询问，不得在同一转换里混用 `exit` 与 `throw`；源错误的分类（可恢复/致命）不明时逐一标注。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)；[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)；[MS-PS-TRY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)。

### 规则 C-PS-06：C 地址级构造（函数指针替换、内联汇编、寄存器/内核符号）向 PowerShell 无等价构造的停标映射
1. **源码触发条件**：C 源码改写函数指针表项或系统调用表（`SYS_CALL_TABLE[__NR_getdents] = (unsigned long*)HookGetDents;`）、保存原函数指针用于还原（`original_getdents = (void*)SYS_CALL_TABLE[__NR_getdents];`）、内联汇编或架构寄存器读取（`asm("mov %0, %%rax" ...)`、`__readgsqword(0x60)`、`_ReturnAddress()`）、或 `VirtualAlloc(..., PAGE_EXECUTE_READWRITE)` 后跳转执行 shellcode。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11 与源平台 ABI/特权级（[WG14-N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）；目标语言 PowerShell 7.6（[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators), [MS-DOTNET-API](https://learn.microsoft.com/en-us/dotnet/api/)）。
3. **原可观察行为**：这些构造直接改写当前进程/内核地址空间中的机器码或调用目标，其行为取决于架构、特权级与内核版本，属于平台事实而非 C 语言语义；还原路径（把原指针写回）保证可观察的钩子生命周期。
4. **目标可选写法和不适用条件**：
   - *可选映射*：仅当源构造存在明确托管替代时才改写——调用外部进程用 `&` 调用运算符/`Start-Process`；需要 native 入口时用 `Add-Type` + `DllImport` 声明后调用，并在报告中标注需 .NET 互操作且架构一致。
   - *不适用条件*：**严禁声明等价**。PowerShell 没有函数指针、没有内联汇编、没有地址级钩子；系统调用表替换、shellcode 写入后跳转、寄存器直读在 PowerShell 中不存在语言级或 BCL 级对应物。遇到这类构造必须把该转换点标记为"需原生宿主 / 不可语言层转换"并向用户确认，不得用脚本函数覆盖（`Set-Item function:...`）、`Add-Type` 拼装或 `Invoke-Expression` 生成看似等价的代码。
5. **错误机械替换反例**：
   ```powershell
   # 错误：用 PowerShell 函数覆盖冒充"钩子"，与 C 的系统调用表替换无关
   function Get-Hooked { param($Name) Get-Item $Name }
   Set-Item function:Get-ChildItem -Value { Get-Hooked @args }   # 只影响本会话的 cmdlet 解析
   # 错误：把内联汇编/寄存器直读"翻译"成注释后继续产出可运行脚本
   # asm("mov %0, %%rax" :: "r"(shellcode))
   # 正确：停标为不可语言层转换，要求原生宿主或明确互操作边界
   throw [System.NotSupportedException]::new("地址级钩子/内联汇编无 PowerShell 等价构造：需原生宿主，已停止转换")
   ```
6. **信息不足或实现相关时的处理**：架构、特权级、内核版本、是否存在原生宿主一律属于未决事实，缺一即停标；不得把"能写出 PowerShell 语法"当作已实现该能力的证据。
7. **直接官方 HTTPS 依据链接**：[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)；[MS-DOTNET-API](https://learn.microsoft.com/en-us/dotnet/api/)；[WG14-N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
