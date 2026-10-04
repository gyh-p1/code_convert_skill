---
name: powershell-to-csharp
description: Use when converting PowerShell source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → C# 语言转换规则

> **适用基线**：PowerShell 7.6 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/powershell-to-csharp/README.md)；候选、冻结任务与第三方回传须分层记录。
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
