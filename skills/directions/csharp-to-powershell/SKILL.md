---
name: csharp-to-powershell
description: Use when converting C# source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → PowerShell 语言转换规则

> **适用基线**：C# 12 / .NET 8 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C#](../../references/languages/csharp.md)与[目标语言 PowerShell](../../references/languages/powershell.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 C# → PowerShell 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CS-PS-01：C# 泛型 LINQ 查询向 PowerShell 管道 Where/Select 映射
1. **源码触发条件**：C# 源码中使用 `list.Where(x => ...).Select(x => ...)` 进行链式集合投影。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-COLL）；目标语言 PowerShell 7.6（MS-PS-PIPE）。
3. **原可观察行为**：强类型委托延迟执行（惰性求值）过滤与投影。
4. **目标可选写法和不适用条件**：
   - *可选映射*：仅源在同一时点消费查询、枚举次数/顺序与副作用一致时考虑 PowerShell 管道；源只构造 IEnumerable 而稍后/多次枚举时保留延迟查询语义，不能在赋值时立即执行管道。数据量或性能不决定能否改变执行时点。
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
7. **资料依据（名称/版本/章节）**：MS-PS-PIPE；MS-PS-ARRAY。

### 规则 CS-PS-02：C# 强类型异常向 PowerShell 终止错误提升控制映射
1. **源码触发条件**：C# 源码中抛出特定类型异常，期望立即中断当前执行流。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-EXCEPT）；目标语言 PowerShell 7.6（MS-PS-ERROR）。
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
7. **资料依据（名称/版本/章节）**：MS-PS-ERROR。

### 规则 CS-PS-03：C# async/await 完成与等待语义向 PowerShell 目标实现映射
1. **源码触发条件**：C# 源码中使用 `await DoAsync()` 等待异步结果。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-ASYNC）；目标语言 PowerShell 7.6（MS-PS-THREADJOB）。
3. **原可观察行为**：等待未完成 Task 时可挂起并把控制权交还调用者，任务完成后继续；已完成 Task 不必挂起。async 不自动代表新线程。保留调用者继续执行、完成/取消/错误与清理时机。
4. **目标可选写法和不适用条件**：
   - *可选映射*：由智能体模型在目标实现中保持完成/等待边界；需要独立作业且符合源的状态、调度及结果传递契约时，可用 `Start-ThreadJob` 并显式收集结果、错误和清理。只有源调用链证明阻塞不改变可观察行为，或用户明确允许相关差异时，才考虑 `Receive-Job -Wait` / `.GetAwaiter().GetResult()` 阻塞等待。
   - *不适用条件*：不把作业 API 或同步取值当 await 的通用替换；源依赖调用者继续、事件循环/锁、同步上下文、取消或超时时不得机械阻塞。源如何观察/传播异常，目标就保持对应路径，不能新增吞错或强制捕获来改变源的失败行为。
5. **错误机械替换反例**：
   ```powershell
   # 错误：遗漏 Receive-Job 导致后台作业结果丢失与作业泄漏
   $job = Start-ThreadJob { Do-HeavyTask }
   # 仅在阻塞等待符合冻结契约时：显式取回数据并清理 Job；这不是通用 await 映射
   $job = Start-ThreadJob { Do-HeavyTask }
   $result = Receive-Job -Job $job -Wait -AutoRemoveJob
   ```
6. **信息不足或实现相关时的处理**：触发本规则即加载并发场景，I/O 另加载实际场景；缺调用链、完成/取消或共享状态条件先记缺口。`Wait-Job -Timeout` 只限制等待，不自动终止后台作业，不等于源任务取消；终止、结果/错误收集与清理按实际源契约处理，不单靠“注明降级”接受差异。
7. **资料依据（名称/版本/章节）**：C# 12 / .NET 8 Task asynchronous programming model；PowerShell 7.6 Wait-Job 的 Timeout；MS-PS-THREADJOB。

### 规则 CS-PS-04：C# using/IDisposable 向 PowerShell try/finally 与显式 .Dispose() 映射
1. **源码触发条件**：C# 源码使用 `using (RegistryKey key = ...)`、`using (SHA256 sha256 = SHA256.Create())` 或 `using` 声明管理 `IDisposable`，或在错误分支手工调用 `Dispose()`。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-DISPOSE）；目标语言 PowerShell 7.6（MS-PS-TRY）。
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
7. **资料依据（名称/版本/章节）**：MS-CS-DISPOSE；MS-PS-TRY。

### 规则 CS-PS-05：C# System.Management WMI 查询向 PowerShell CIM Cmdlet 映射
1. **源码触发条件**：C# 源码使用 `ManagementObjectSearcher`、`ManagementObject`、`ManagementScope`，通过 `result.Properties["Name"].Value` 读属性、`PropertyDataCollection` 遍历属性，或用 `InvokeMethod("Terminate", ...)`、`InvokeMethod("GetOwner", ...)` 调用 WMI 方法。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-API-MANAGEMENT）；目标语言 PowerShell 7.6（MS-PS-CIM）。
3. **原可观察行为**：`Get()` 返回 `ManagementObjectCollection`，属性访问是按名查表（缺失的属性名为 `$null`），`InvokeMethod` 返回方法返回值对象并可被 `Convert.ToInt32` 强转；连接身份通过 `ConnectionOptions`/`ManagementScope` 的显式凭据与计算机名建立。
4. **目标可选写法和不适用条件**：
   - *可选映射*：仅作用域、身份、传输、查询/方法语义一致时考虑 CIM；Get-CimInstance 用 Namespace/ComputerName/CimSession/Filter，没有 Credential 参数。显式凭据在 New-CimSession 中设置，再用 CimSession 传给查询；会话创建/释放也须对应源生命周期。无法表达时记录具体依赖，不只更换 Cmdlet 名。
   - *不适用条件*：严禁依赖单个匹配结果仍为集合——`Where-Object` 过滤出单条时会被自动展开为标量，需 `@(...)` 包裹后再取 `[0]`；严禁把返回对象当作仍具 `Properties["..."]` 集合的对象；严禁把 C# 凭据/命名空间参数省略后按本机身份执行（身份与作用域被静默改变）。
5. **错误机械替换反例**：
   ```powershell
   # C# 原型：var searcher = new ManagementObjectSearcher(scope, query);
   #           foreach (ManagementObject r in searcher.Get()) { props = r.Properties; ... }
   # 对有远端/显式身份的源，省略对应会话会改变作用域；本地源不强制远端
   $r = Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = 1234"
   $v = $r.Properties['Name'].Value   # 错误：CIM 对象没有 Properties 集合，得到 $null
   # 候选：$cimSession 是与源作用域/身份/协议对应的已建会话，非新执行授权
   $r = @(Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = 1234" -CimSession $cimSession)
   if ($r.Count -gt 0) { $name = $r[0].Name }
   ```
6. **信息不足或实现相关时的处理**：若源码依赖 `ManagementObjectSearcher` 的具体返回类型（用 `InvokeMethod` 的原生返回值做位运算或强转），或目标主机只允许 DCOM 通道，须先确认 CIM 通道可用性并在报告中标为待确认，不要假定两者返回对象等价。
7. **资料依据（名称/版本/章节）**：MS-PS-CIM；MS-API-MANAGEMENT。

### 规则 CS-PS-06：C# 属性、索引器与 out 参数向 PowerShell 属性访问、Item() 与 [ref] 映射
1. **源码触发条件**：C# 源码读取计算属性（`this.Result.GetType().Name`、`RawData { get; private set; }`）、用索引器访问（`Properties["sNames"]`、`cred[0]`）、用字典索引判断键存在（`arguments.ContainsKey("/ticket")` 后 `arguments["/ticket"]`），或使用 `TryDequeue(out byte[] bdata)`/`TryParse(out ...)` 这类 `out` 参数自带成功标志的 API。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-PROPS）；目标语言 PowerShell 7.6（MS-PS-OPS）。
3. **原可观察行为**：属性/索引器按实际 getter 与类型契约求值；不同索引器的缺键、失败与副作用不同。out 在正常返回前须被赋值，但返回 false 并不从语言规则保证 default；按具体 Try API 核成功标志、赋值与源消费。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按真实 .NET 类型/适配器选择 obj[key]、get_Item 或 Properties 集合，不通用优先 Properties/Item()。缺键失败、ContainsKey 与 getter 求值次数对应源；out 可考虑 [ref]，但正常/失败/异常后值与是否消费按实际 API/源分支保留。
   - *不适用条件*：严禁把 C# 索引器机械写成 `$obj[key]`（对 `.NET` 集合走 `Item` 索引尚可，对自定义对象可能解析成数组下标或字符串按字符取值）；严禁把 C# 索引器抛 `KeyNotFoundException` 的失败语义改成静默 `$null` 后继续执行；严禁把 `out` 参数写成普通返回值的并列赋值（成功标志与值可能不同步）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：把 out 参数按普通调用处理；C# 原型 TryDequeue(out byte[] bdata)
   $ok = $_senderQueue.TryDequeue($bdata)   # 错误：$bdata 不会被赋值，且方法需要 [ref]
   if ($ok) { $pipe.Write($bdata, 0, $bdata.Length) }  # $bdata 为 $null -> 方法调用失败
   # 正确：显式 [ref] 容器并尊重布尔成功标志
   $bdata = $null
   if ($_senderQueue.TryDequeue([ref]$bdata)) { # 不为源新增 null 过滤；队列可含 null 时保持源后续行为
       $pipe.Write($bdata, 0, $bdata.Length)
   }
   ```
6. **信息不足或实现相关时的处理**：若源码中的属性 getter 带副作用（缓存写入、计数递增），或 `ContainsKey` 与索引器之间存在并发修改窗口，先确认该副作用是否属于外部可观察行为，无法确认时写为待确认而不是直接内联展开。
7. **资料依据（名称/版本/章节）**：MS-PS-OPS；MS-API-DICTIONARY。

### 规则 CS-PS-08：保留基类构造调用，不把自审语法猜测当成编译诊断

1. **源码触发条件**：C# 源码的派生类构造函数使用 **base 构造调用**（`public Derived(...) : base(...)`），且类层次含带参基类；或派生类依赖基类的字段初始化顺序。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8；目标语言 PowerShell 7.6（about_Classes）。
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
7. **资料依据（名称/版本/章节）**：about_Classes_Inheritance，Derived class constructors；C# 构造函数。

### 规则 CS-PS-09：迭代器清理、集合返回与字段单位分别保持

1. **触发／前提**：C# 12/.NET 8 源使用 yield/foreach、嵌套集合或 JSON 对象、Rune 限长和原子状态快照；目标 PowerShell 7.6 基线，实际宿主另冻。
2. **应保留行为**：首次枚举才发生的副作用、break／异常后的确定性清理、成功前后状态及数据对象的类型／形状；语义事实读 [L1-PS-08](../../references/languages/powershell.md#l1-ps-08-函数-success-流集合对象与泛型调用) 和 [L1-CS-09](../../references/languages/csharp.md#l1-cs-09-lengthrune-与文本元素的单位不同)。
3. **可选映射**：按源设计带显式退出协议的块式枚举或状态对象，try/finally 管 reader；成功流只产约定结果，嵌套集合按各返回边界防展开。原子 catch 恢复业务状态但不自动撤销清理审计；源非原子路径保留已成功写入。
4. **不适用／反例**：不能先全量枚举再截断 limit，不能把 source 的 Rune 计数换成 PowerShell Length，也不能用外层 @() 假定递归 ArrayList 类型已保持。limit=0 若源不启动枚举，目标也不能先打开资源；“回滚业务”不等于“删除 finally 的关闭事件”。
5. **核对方式**：在本项正常自审覆盖中对应源状态和调用点；相关输入候选包括 0／1／多项、提前退出、取得资源前后失败、非原子和补充平面文本。实际评估按冻结计划和预算，不新增审阅轮次或辅助驱动。
6. **未知处理**：依赖缺失／合法入口不足与代码映射问题分别登记；泛型绑定未知采用有依据的宿主 API 调用，不吞异常或补固定结果。
7. **依据**：C# iterator/foreach/IDisposable、.NET Rune；PowerShell about_Return/about_Pipelines/about_Try_Catch_Finally；库方法签名仍按本项实际版本。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
