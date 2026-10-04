---
name: python-to-csharp
description: Use when converting Python source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → C# 语言转换规则

> **适用基线**：CPython 3.12 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Python](../../references/languages/python.md)与[目标语言 C#](../../references/languages/csharp.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/python-to-csharp/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Python → C# 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PY-CS-01：Python **kwargs 动态参数向 C# 强类型选项对象或命名参数映射
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

### 规则 PY-CS-02：Python 多返回值元组向 C# ValueTuple 与析构声明映射
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

### 规则 PY-CS-03：Python with 资源管理向 C# using 声明与 IDisposable 映射
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
6. **信息不足或实现相关时的处理**：若涉及文件路径操作，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
