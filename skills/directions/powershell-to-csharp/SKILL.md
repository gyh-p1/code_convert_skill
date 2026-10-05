---
name: powershell-to-csharp
description: Use when converting PowerShell source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → C# 语言转换规则

> **适用基线**：PowerShell 7.6 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 PowerShell](../../references/languages/powershell.md)与[目标语言 C#](../../references/languages/csharp.md)。
> **方向案例与证据**：如本地工作区存在 `docs/test/dataset/powershell-to-csharp/README.md`，按其中 case 分层查看；该本地数据目录不随 Git/Skill 分发。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 PowerShell → C# 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PS-CS-01：PowerShell 哈希表与动态对象向 C# Dictionary 与强类型类映射
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

### 规则 PS-CS-02：PowerShell 数组 += 扩容向 C# List<T> 动态集合映射
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

### 规则 PS-CS-03：PowerShell 环境变量与作用域向 C# Environment 与命名空间映射
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
6. **信息不足或实现相关时的处理**：若包含特定平台注册表或驱动器虚拟路径，加载 [`skills/systems/posix-windows-filesystem/SKILL.md`](../../systems/posix-windows-filesystem/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)。

### 规则 PS-CS-04：PowerShell 属性包与对象管道结果向 C# 强类型记录与 LINQ 查询映射
1. **源码触发条件**：源码在管道里过滤/投影对象并只取首条，例如 `$r = $apps | Where-Object {$_.Name -eq $appName}` 后接 `if ($r -ne $null) { return $r.AppID }`、`$processList = Get-Process | where-object {$_.Name.ToLower() -eq $processName}`、`$DllInfo = (...).Modules | Where-Object { $_.FileName.ToLower().Contains($FileName) }`；或逐字段装配属性包并输出，例如 `$Output = @{}` 后 `New-Object PSObject -Property $Output`、`$Properties = @{}` 加 `if ($EntryPoint) { $Properties['EntryPoint'] = $EntryPoint }`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines), [MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables)）；目标语言 C# 12 / .NET 8（[MS-CS-LINQ](https://learn.microsoft.com/en-us/dotnet/csharp/linq/), [MS-CS-EXPR](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/statements-expressions-operators/lambda-expressions)）。
3. **原可观察行为**：管道过滤的结果既不是“总是集合”也不是“总是单个对象”——零条为 `$null`、一条为对象本身、多条为 `Object[]`，因此下游 `$r.AppID` 在零条时读到 `$null`，在多条时只作用于数组元素或形成数组属性投影；`Where-Object` 的脚本块条件按 PS 真值语义判定；属性包输出的列集合由运行期键决定，缺少某列时该属性为 `$null`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：用 `IEnumerable<T>` 接收管道，`.Where(...)` 过滤后用 `.FirstOrDefault()`/`.OrderBy(...).First()` 显式表达“取首条”或“可能为 `null`”，并配合 `is null`/`??` 分支；输出侧定义 `record`/`class`（或 `IReadOnlyDictionary<string, object?>` 仅在列集合确实动态时使用）；需要保持插入顺序时用 `List<T>` 或 `Dictionary`（.NET 的 `Dictionary` 不承诺遍历顺序，须按语言共性页的要求不依赖序）。
   - *不适用条件*：严禁把 `$arr | Where-Object {...}` 机械替换为 `.Where(...)` 并把结果当单个对象解引用（`Where` 返回 `IEnumerable<T>`，编译期就会暴露，但改写成 `.First()` 又会把“零条 = `$null`”变成 `InvalidOperationException`，与源的可观察行为不同）；严禁用 `dynamic`/`ExpandoObject` 承载属性包来“保持动态性”。
5. **错误机械替换反例**：
   ```csharp
   // 错误：把管道过滤直接当集合，又用 First 丢掉“零条即无结果”的语义
   var r = apps.Where(a => a.Name == appName);
   return r.First().AppID; // 零条时抛 InvalidOperationException，源返回 $null
   // 正确：显式区分“无结果”与“有结果”
   var r = apps.FirstOrDefault(a => a.Name == appName);
   return r?.AppID ?? appID;
   ```
6. **信息不足或实现相关时的处理**：管道在源里可能产生零条还是恰好一条、属性包列集合是否随输入变化、以及大小写比较是否与源的 `-eq` 一致，都必须先确认；确认不了就停下标注，不要用 `.First()` 或 `dynamic` 猜一个行为。
7. **直接官方 HTTPS 依据链接**：[MS-CS-LINQ](https://learn.microsoft.com/en-us/dotnet/csharp/linq/)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

### 规则 PS-CS-05：PowerShell `$null` 与空字符串真值向 C# 显式 null/空值判定与异常映射
1. **源码触发条件**：源码在同一处同时面对 `$null`、空字符串、空数组或数值 0，例如 `if ($global:credential.Domain -eq '' -or $global:credential.Domain -eq $null)`、`if (-not [string]::IsNullOrEmpty($tmp))`、`if ($global:credential.UserName -and $global:credential.UserName -ne '')`、`if ($icon -ne $null)`、`if ($EntryPoint) { ... }`、`while ($validCreds -eq $false -and $global:VerifyCreds -eq $true)`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)）；目标语言 C# 12 / .NET 8（[MS-CS-NULL](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references), [MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)）。
3. **原可观察行为**：PS 布尔化把 `$null`、空字符串、空集合与 0 都当假，`$null -eq ''` 为假但 `if ($null)` 与 `if ('')` 都为假；`[string]::IsNullOrEmpty` 只覆盖“`$null` 或空串”，不覆盖仅含空白；`$switch` 参数未提供时为 `$false` 而不是 `$null`；绑定的 `[bool]` 参数在源里可能由 `$null` 传入并被转换成 `$false`。C# 的 `string?`、`bool?`、数值类型是三套不同判定，`if (s)` 无法编译。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按源的真实集合逐项判定——`s is null`、`string.IsNullOrEmpty(s)`、`string.IsNullOrWhiteSpace(s)`、`list is null || list.Count == 0`；可空布尔用 `bool?`；可选值用 `T?` 与 `??`/`?.`；判空后进入的失败路径用显式 `throw` 或返回 `null`，与源分支结构一一对应。
   - *不适用条件*：严禁用 `if (s != null)` 覆盖源的“`$null` 或空串”判定（会放过空串分支）；严禁把 `$null` 机械映射为 `default`/`false`/`0`（源里 `$null` 与 0 是可区分的两个状态，例如“未提供”与“设为 0”）；严禁依赖 `dynamic` 让 `if (x)` 在运行期按 PS 真值求值。
5. **错误机械替换反例**：
   ```csharp
   // 错误：只判定 null，空串走进 else，源里空串与 null 同分支
   if (credential.Domain != null) { UseDomain(credential.Domain); }
   // 正确：按源的真实集合判定
   if (!string.IsNullOrEmpty(credential.Domain)) { UseDomain(credential.Domain); }
   else if (credential.Domain is null or "") { credential.Domain = Environment.MachineName; }
   ```
6. **信息不足或实现相关时的处理**：某变量在源里是否可能为“仅空白字符串”、`$switch` 参数与 `[bool]` 参数的实际取值集合、以及 `[string]` 强类型参数把 `$null` 转成了什么，都必须先确认；确认不了就停下标注，不要把 PS 真值集合猜成 C# 的某一套判定。
7. **直接官方 HTTPS 依据链接**：[MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)；[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)。

### 规则 PS-CS-06：PowerShell 中直调 .NET API 与手工非托管内存向 C# 等价调用、`try/finally` 栈与 `using` 映射
1. **源码触发条件**：源码已经直接调用 .NET API 并自行管理非托管资源，例如 `$TableBuffer = [Runtime.InteropServices.Marshal]::AllocHGlobal($TableBufferSize)` 与 `[Runtime.InteropServices.Marshal]::FreeHGlobal($TableBuffer)`、`[Runtime.InteropServices.Marshal]::PtrToStringUni($ServiceTagQuery.Buffer)`、`[Runtime.InteropServices.Marshal]::SizeOf($credUi)`、`[System.BitConverter]::GetBytes($TcpRow.LocalPort)`、`$FileDownload = $Downloader.DownloadFileTaskAsync($Url, $TmpFile)` 与 `Register-ObjectEvent`/`Unregister-Event`，以及 `try { ... } catch [Exception] { ... } finally { $Downloader.Dispose() }` 这类显式清理。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-TRY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）；目标语言 C# 12 / .NET 8（[MS-DOTNET-API](https://learn.microsoft.com/en-us/dotnet/api/), [MS-CS-USING](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/using)）。
3. **原可观察行为**：PS 调用 .NET 方法可观察到与 C# 调用同一方法一致的返回值、异常类型与 `[ref]` 输出参数语义，但所有权与生命周期由 PS 侧显式语句控制：`AllocHGlobal` 的内存只有在显式 `FreeHGlobal` 时才释放，`Dispose()` 只有被调用才生效，事件注册只有 `Unregister-Event` 才解除，GC 只兜底不保证时机。`catch [Exception]` 捕获所有 CLR 异常；`$_.FullyQualifiedErrorId` 这类 PS 侧标识没有对应的 C# 类型。
4. **目标可选写法和不适用条件**：
   - *可选映射*：直接保留同名的 .NET 调用（`Marshal.PtrToStringUni`、`BinaryPrimitives`/`BitConverter`、`Marshal.SizeOf<T>`），让异常类型与返回值语义与源一致；非托管缓冲区改用 `using`/`SafeHandle`/`try ... finally` 保证释放；`IDisposable`/`IAsyncDisposable` 资源用 `using` 或 `using var`；事件订阅用 `-=` 在 `finally`/`Dispose` 中解除。
   - *不适用条件*：严禁把已经直调 .NET 的部分重新表达为 P/Invoke `[DllImport]` 或 `unsafe` 指针算术（改变了异常、编组与所有权语义，也丢掉了源已依赖的托管行为）；严禁把 `[ref]` 输出参数机械改成返回值（会改变调用形态与错误路径）；严禁省略 `FreeHGlobal`/`Dispose`/事件解除，指望 GC 兜底。
5. **错误机械替换反例**：
   ```csharp
   // 错误：非托管缓冲区无 finally 兜底，异常路径泄漏
   IntPtr table = Marshal.AllocHGlobal(size);
   Fill(table);                       // 抛异常时 table 永不释放
   Marshal.FreeHGlobal(table);
   // 正确：用 finally（或 SafeHandle）保证释放
   IntPtr table = Marshal.AllocHGlobal(size);
   try { Fill(table); }
   finally { Marshal.FreeHGlobal(table); }
   ```
6. **信息不足或实现相关时的处理**：调用点用到的 .NET API 在目标框架版本中是否存在同签名重载、`[ref]` 参数是 `ref` 还是 `out`、以及源里的清理是否已经在某条路径上做过，都必须先确认；确认不了就停下标注，不要改写成 P/Invoke 或换用另一个 API 来“凑等价”。
7. **直接官方 HTTPS 依据链接**：[MS-DOTNET-API](https://learn.microsoft.com/en-us/dotnet/api/)；[MS-CS-USING](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/using)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
