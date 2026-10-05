---
name: cpp-to-powershell
description: Use when converting C++ source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → PowerShell 语言转换规则

> **适用基线**：ISO C++17 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C++](../../references/languages/cpp.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
> **方向案例与证据**：如本地工作区存在 `docs/test/dataset/cpp-to-powershell/README.md`，按其中 case 分层查看；该本地数据目录不随 Git/Skill 分发。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C++ → PowerShell 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-PS-01：C++ 结构化数据打印向 PowerShell PSObject 管道对象流映射
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

### 规则 CPP-PS-02：C++ 异常分类捕获向 PowerShell 终止错误提升与 catch 分流映射
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

### 规则 CPP-PS-03：C++ 互斥锁与临界区向 PowerShell Monitor 同步包装映射
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
6. **信息不足或实现相关时的处理**：若涉及跨进程同步，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
