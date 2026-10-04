---
name: c-to-powershell
description: Use when converting C source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C → PowerShell 语言转换规则

> **适用基线**：ISO C11 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C](../../references/languages/c.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/c-to-powershell/README.md)；候选、冻结任务与第三方回传须分层记录。
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
