---
name: csharp-to-powershell
description: Use when converting C# source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → PowerShell 语言转换规则

> **适用基线**：C# 12 / .NET 8 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/csharp-to-powershell/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C# → PowerShell 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CS-PS-01：C# 泛型 LINQ 查询向 PowerShell 管道 Where/Select 映射
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

### 规则 CS-PS-02：C# 强类型异常向 PowerShell 终止错误提升控制映射
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

### 规则 CS-PS-03：C# async/await 向 PowerShell 异步作业与同步上下文等待映射
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
