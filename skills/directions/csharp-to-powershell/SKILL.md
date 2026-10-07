---
name: csharp-to-powershell
description: Use when converting C# source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → PowerShell 语言转换规则

> **适用基线**：C# 12 / .NET 8 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C#](../../references/languages/csharp.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
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

### 规则 CS-PS-04：C# using/IDisposable 向 PowerShell try/finally 与显式 .Dispose() 映射
1. **源码触发条件**：C# 源码使用 `using (RegistryKey key = ...)`、`using (SHA256 sha256 = SHA256.Create())` 或 `using` 声明管理 `IDisposable`，或在错误分支手工调用 `Dispose()`。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）；目标语言 PowerShell 7.6（[MS-PS-TRY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）。
3. **原可观察行为**：离开 `using` 作用域或块时，无论正常返回还是异常展开都确定性调用一次 `Dispose()`；C# 编译器保证该调用发生在异常继续传播之前。
4. **目标可选写法和不适用条件**：
   - *可选映射*：改写为 `try { ... } finally { if ($null -ne $key) { $key.Dispose() } }`；变量在 `try` 之前先赋 `$null`，使"创建动作本身失败"时不至于在 `finally` 中对未定义变量调用方法。
   - *不适用条件*：严禁依赖 PowerShell 托管对象被 CLR GC 回收来代替 `Dispose()`（非内存资源释放时机不确定）；严禁在 `finally` 中不加判空直接调用 `$key.Dispose()`（变量可能未赋值，产生二次错误并掩盖原始异常）；严禁用 `[System.GC]::Collect()` 充当确定性释放。
5. **错误机械替换反例**：
   ```powershell
   # C# 原型：using (RegistryKey key = hive.OpenSubKey($subKeyPath)) { ... }
   # 错误：finally 中不判空就调用 Dispose，OpenSubKey 抛错时 $key 未赋值
   try { $key = $hive.OpenSubKey($subKeyPath); $v = $key.GetValue('ImagePath') }
   finally { $key.Dispose() }   # 错误：变量未定义或 $null -> 二次错误掩盖原始异常
   # 正确：先赋 $null，finally 中判空释放
   $key = $null
   try { $key = $hive.OpenSubKey($subKeyPath); $v = $key.GetValue('ImagePath') }
   finally { if ($null -ne $key) { $key.Dispose() } }
   ```
6. **信息不足或实现相关时的处理**：若源码中同一对象可能被多条路径释放（是否允许二次 `Dispose()`），或该对象同时有 `Close()` 与 `Dispose()` 两个入口，先确认它是否声明幂等释放，再决定是否重复调用。
7. **直接官方 HTTPS 依据链接**：[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)；[MS-PS-TRY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)。

### 规则 CS-PS-05：C# System.Management WMI 查询向 PowerShell CIM Cmdlet 映射
1. **源码触发条件**：C# 源码使用 `ManagementObjectSearcher`、`ManagementObject`、`ManagementScope`，通过 `result.Properties["Name"].Value` 读属性、`PropertyDataCollection` 遍历属性，或用 `InvokeMethod("Terminate", ...)`、`InvokeMethod("GetOwner", ...)` 调用 WMI 方法。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-API-MANAGEMENT](https://learn.microsoft.com/en-us/dotnet/api/)）；目标语言 PowerShell 7.6（[MS-PS-CIM](https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance)）。
3. **原可观察行为**：`Get()` 返回 `ManagementObjectCollection`，属性访问是按名查表（缺失的属性名为 `$null`），`InvokeMethod` 返回方法返回值对象并可被 `Convert.ToInt32` 强转；连接身份通过 `ConnectionOptions`/`ManagementScope` 的显式凭据与计算机名建立。
4. **目标可选写法和不适用条件**：
   - *可选映射*：查询改 `Get-CimInstance -ClassName Win32_Process -Filter "..."`（WQL 仍可用，主要换 Cmdlet 名与参数名 `-Namespace`、`-ComputerName`、`-Credential`、`-Filter`），属性读取改为 `$_.Name`，方法调用改为 `Invoke-CimMethod -MethodName Terminate -Arguments @{...}` 并读返回对象；无法用 CIM 表达时保留 `System.Management` 类型并显式 `.Dispose()`。
   - *不适用条件*：严禁依赖单个匹配结果仍为集合——`Where-Object` 过滤出单条时会被自动展开为标量，需 `@(...)` 包裹后再取 `[0]`；严禁把返回对象当作仍具 `Properties["..."]` 集合的对象；严禁把 C# 凭据/命名空间参数省略后按本机身份执行（身份与作用域被静默改变）。
5. **错误机械替换反例**：
   ```powershell
   # C# 原型：var searcher = new ManagementObjectSearcher(scope, query);
   #           foreach (ManagementObject r in searcher.Get()) { props = r.Properties; ... }
   # 错误：省略 -ComputerName/-Credential 会静默改为本机身份执行
   $r = Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = 1234"
   $v = $r.Properties['Name'].Value   # 错误：CIM 对象没有 Properties 集合，得到 $null
   # 正确：显式作用域与身份，按属性名直接读取
   $r = @(Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = 1234" -ComputerName $host -Credential $cred)
   if ($r.Count -gt 0) { $name = $r[0].Name }
   ```
6. **信息不足或实现相关时的处理**：若源码依赖 `ManagementObjectSearcher` 的具体返回类型（用 `InvokeMethod` 的原生返回值做位运算或强转），或目标主机只允许 DCOM 通道，须先确认 CIM 通道可用性并在报告中标为待确认，不要假定两者返回对象等价。
7. **直接官方 HTTPS 依据链接**：[MS-PS-CIM](https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance)；[MS-API-MANAGEMENT](https://learn.microsoft.com/en-us/dotnet/api/)。

### 规则 CS-PS-06：C# 属性、索引器与 out 参数向 PowerShell 属性访问、Item() 与 [ref] 映射
1. **源码触发条件**：C# 源码读取计算属性（`this.Result.GetType().Name`、`RawData { get; private set; }`）、用索引器访问（`Properties["sNames"]`、`cred[0]`）、用字典索引判断键存在（`arguments.ContainsKey("/ticket")` 后 `arguments["/ticket"]`），或使用 `TryDequeue(out byte[] bdata)`/`TryParse(out ...)` 这类 `out` 参数自带成功标志的 API。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-PROPS](https://learn.microsoft.com/en-us/dotnet/csharp/)）；目标语言 PowerShell 7.6（[MS-PS-OPS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)）。
3. **原可观察行为**：C# 属性访问是一次方法调用，键缺失时索引器抛 `KeyNotFoundException`（`Dictionary`）或返回 `null`（`ManagementBaseObject`）；`out` 参数在返回 `false` 时被赋 `default`，成功标志与返回值同时可观察。
4. **目标可选写法和不适用条件**：
   - *可选映射*：属性访问保持 `$obj.Name`（PowerShell 走 PSObject 适配层调用底层 getter）；索引器用 `$obj.Item('sNames')`，但优先改成 `.Properties['sNames'].Value` 形式；字典用 `$dict['/ticket']` 并**同时**判 `$dict.ContainsKey(...)`；`out` 参数改用已初始化变量加 `[ref]`，以返回的布尔值决定是否使用该值。
   - *不适用条件*：严禁把 C# 索引器机械写成 `$obj[key]`（对 `.NET` 集合走 `Item` 索引尚可，对自定义对象可能解析成数组下标或字符串按字符取值）；严禁把 C# 索引器抛 `KeyNotFoundException` 的失败语义改成静默 `$null` 后继续执行；严禁把 `out` 参数写成普通返回值的并列赋值（成功标志与值可能不同步）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：把 out 参数按普通调用处理；C# 原型 TryDequeue(out byte[] bdata)
   $ok = $_senderQueue.TryDequeue($bdata)   # 错误：$bdata 不会被赋值，且方法需要 [ref]
   if ($ok) { $pipe.Write($bdata, 0, $bdata.Length) }  # $bdata 为 $null -> 方法调用失败
   # 正确：显式 [ref] 容器并尊重布尔成功标志
   $bdata = $null
   if ($_senderQueue.TryDequeue([ref]$bdata) -and $null -ne $bdata) {
       $pipe.Write($bdata, 0, $bdata.Length)
   }
   ```
6. **信息不足或实现相关时的处理**：若源码中的属性 getter 带副作用（缓存写入、计数递增），或 `ContainsKey` 与索引器之间存在并发修改窗口，先确认该副作用是否属于外部可观察行为，无法确认时写为待确认而不是直接内联展开。
7. **直接官方 HTTPS 依据链接**：[MS-PS-OPS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)；[MS-API-DICTIONARY](https://learn.microsoft.com/en-us/dotnet/api/)。

### 规则 CS-PS-08：保留基类构造调用，不把自审语法猜测当成编译诊断

1. **源码触发条件**：C# 源码的派生类构造函数使用 **base 构造调用**（`public Derived(...) : base(...)`），且类层次含带参基类；或派生类依赖基类的字段初始化顺序。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8；目标语言 PowerShell 7.6（[about_Classes](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_classes)）。
3. **原可观察行为**：C# 侧基类构造函数**先于**派生类构造体执行，且 `: base(...)` 的参数在派生类构造体之前求值；基类字段在派生类可见。
4. **目标可选写法和不适用条件**：
   - *可选映射*：PowerShell class 支持在构造参数列表之后、构造体之前写 `: base(...)`。核对实际基类、构造重载与参数类型，保留调用及顺序；**不得**仅因自审说“不支持”就改成字段赋值或组合。
   - *不适用条件*：基类为**无参构造**且无需参数传递时，`class Derived : Base {}` 直接可用，不需要改写。
5. **错误机械替换反例**：
   ```powershell
   # 错误：省略带参基类构造，以字段赋值代替其初始化与副作用
   class Derived : Base {
       Derived([int]$x) {
           $this.BaseValue = $x
       }
   }
   # 可选映射：实际基类提供匹配重载时保留构造链
   class Derived : Base {
       Derived([int]$x) : base($x) { }
   }
   ```
6. **信息不足或实现相关时的处理**：基类实现/程序集缺失、重载不明时记录依赖缺口；语法支持不证明特定基类可加载，也不证明构造副作用等价。
7. **直接官方 HTTPS 依据链接**：[about_Classes_Inheritance，Derived class constructors](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_classes_inheritance?view=powershell-7.6)；[C# 构造函数](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/constructors)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
