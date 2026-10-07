---
name: python-to-csharp
description: Use when converting Python source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → C# 语言转换规则

> **适用基线**：CPython 3.12 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Python](../../references/languages/python.md)与[目标语言 C#](../../references/languages/csharp.md)。
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

### 规则 PY-CS-04：Python 任意精度 int 向 C# 定宽整数与 checked/unchecked 上下文映射
1. **源码触发条件**：Python 源码对 `int` 做加减乘、移位、位掩码或累加（校验和、哈希、计数器、从 `struct.unpack` 得到的定宽字段），或依赖"永远不会溢出"的算术前提。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 C# 12 / .NET 8（[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)）。
3. **原可观察行为**：Python `int` 为任意精度，算术不发生截断（`1 << 40`、阶乘、大数乘法都保持精确值），仅受可用内存限制；`& 0xFFFFFFFF` 之类的掩码是显式位运算而非溢出保护。C# `int`/`long` 为定宽，默认 `unchecked` 上下文按补码截断回绕（`int.MaxValue + 1` 得 `int.MinValue`），`checked` 作用域内则抛 `System.OverflowException`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：先用源码证据确定数值上界，能落入 64 位的用 `long`/`ulong`，需要与 Python 语义一致的按位运算用 `uint`/`ulong` 并显式声明宽度；需要真正的任意精度时用 `System.Numerics.BigInteger`，且在报告中声明这一依赖与性能含义；需要"越界即失败"的位置写 `checked { ... }` 或 `checked(...)`。
   - *不适用条件*：严禁把任意精度运算机械搬成 `int` 而不确认上界（截断会静默发生，只有在换算/序列化处才暴露）；严禁用 `unchecked` 上下文来"复现 Python 的无溢出"（方向恰好相反：`unchecked` 是回绕，Python 是不回绕）；严禁假定 `checked` 会覆盖被调用方法内部的算术（`checked` 只作用于该语句/作用域内直接书写的运算，不传播进被调用函数的函数体）。
5. **错误机械替换反例**：
   ```csharp
   // Python 原型：h = (h << 5) + h + c        # 无溢出截断，值持续增长
   int h = 0;
   foreach (byte c in data) { h = (h << 5) + h + c; }   // 错误：默认 unchecked，超过 32 位即回绕
   // Python 原型：packed = len(cert) & 0xFFFFFFFF
   // 正确：需要回绕语义时写明宽度，需要失败语义时用 checked
   uint h32 = 0;
   foreach (byte c in data) { unchecked { h32 = (h32 << 5) + h32 + c; } }
   int bounded;
   checked { bounded = int.Parse(lenText); }   // 越界抛 OverflowException
   ```
6. **信息不足或实现相关时的处理**：源码未给出数值上界时，必须先确认业务上界或改用 `long`/`BigInteger`，不得默认取 `int`；若源算术混合有无符号语义（Python 无原生无符号），需逐表达式确认目标类型与掩码位置。
7. **直接官方 HTTPS 依据链接**：[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)；[MS-API-BIGINTEGER](https://learn.microsoft.com/en-us/dotnet/api/)。

### 规则 PY-CS-05：Python 负索引与切片裁剪向 C# 索引/Range 边界映射
1. **源码触发条件**：Python 源码使用 `seq[-1]`、`seq[a:b]`、`seq[:n]`、`seq[r:]`，或在 `range(len(seq) - 1, -1, -1)` 这类逆序遍历中依赖负向边界。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-SUBSCRIPTIONS](https://docs.python.org/3.12/reference/expressions.html)）；目标语言 C# 12 / .NET 8（[MS-CS-INDICES](https://learn.microsoft.com/en-us/dotnet/csharp/)）。
3. **原可观察行为**：Python 负索引等价于 `len + i`；切片对任何边界都做**裁剪**（`seq[0:999]` 取到末尾，`seq[-999:]` 取全部），不抛异常，`seq[a:b]` 在 `a >= b` 时返回空序列。C# 的 `^n` 是"从末尾数第 n 个"（`^1` 为最后一个元素，`^0` 等于 `Length`，越界即抛 `ArgumentOutOfRangeException`），`seq[a..b]` 要求两端都在 `0..Length` 内，越界抛 `ArgumentOutOfRangeException`，且 `a > b` 同样抛异常而非返回空。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`seq[-1]`→`seq[^1]`，`seq[a:b]`→`seq[a..b]`，`seq[:n]`→`seq[..n]`，`seq[r:]`→`seq[r..]`，且在三处显式补齐检查：`a`、`b` 先裁剪到 `[0, Length]`，`a > b` 时直接取空结果，负向步长遍历改为 `for (int i = seq.Length - 1; i >= 0; i--)`。
   - *不适用条件*：严禁把 `seq[a:b]` 机械写成 `seq[a..b]` 而不做裁剪（Python 侧不抛异常的越界切片会在 C# 侧变成运行期异常，失败路径被新增）；严禁在计算 `^n` 时使用 `n <= 0` 或 `n > Length` 的值（`^0` 与超界都抛异常，而 Python 的 `seq[-0]` 就是 `seq[0]`，两者语义不同）；严禁假定 `a > b` 时 `Range` 会返回空（C# 抛 `ArgumentOutOfRangeException`）。
5. **错误机械替换反例**：
   ```csharp
   // Python 原型：head = data[:limit]        # limit 可能大于 len(data)，Python 会裁剪
   var head = data[..limit];                  // 错误：limit > data.Length 时抛 ArgumentOutOfRangeException
   // Python 原型：last = data[-1]; window = data[start:end]
   int safeEnd = Math.Clamp(end, 0, data.Length);
   int safeStart = Math.Clamp(start, 0, safeEnd);
   var window = data[safeStart..safeEnd];     // 正确：先裁剪，且保证 start <= end
   var last = data.Length > 0 ? data[^1] : default; // 正确：^1 需先确认非空
   ```
6. **信息不足或实现相关时的处理**：若源码切片的 `start`/`end` 由外部输入驱动且源码依赖"越界被裁剪"这一行为，必须把该依赖写进任务前提；目标类型是否提供 `Length`/`Count` 与索引器决定了 `^`/`Range` 能否直接使用，不满足时改用 `Array.Copy`/`Span` 显式实现。
7. **直接官方 HTTPS 依据链接**：[MS-CS-INDICES](https://learn.microsoft.com/en-us/dotnet/csharp/)；[PY-REF-SUBSCRIPTIONS](https://docs.python.org/3.12/reference/expressions.html)。

### 规则 PY-CS-06：Python dict 向 Dictionary 与键缺失语义映射
1. **源码触发条件**：Python 源码使用 `d[key]`、`d.get(key, default)`、`key in d`、`d.setdefault(k, v)`、`del d[k]`，或把 `dict` 当作有序结构遍历（`for k, v in d.items()`），或依赖任意可哈希对象（元组、`frozenset`、自定义 `__hash__`/`__eq__` 对象）作为键。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 C# 12 / .NET 8（[MS-API-DICTIONARY](https://learn.microsoft.com/en-us/dotnet/api/)）。
3. **原可观察行为**：`d[key]` 键缺失抛 `KeyError`，`d.get(key, default)` 返回 `default`，`d.get(key)` 返回 `None`；Python 3.7 起 `dict` 保证保持**插入顺序**，`items()` 按插入顺序迭代；键相等性由 `__hash__` 与 `__eq__` 定义，元组等不可变对象可直接作键。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`d[key]`→保留抛错语义时用索引器并让 `KeyNotFoundException` 传播，或统一改用 `dict.TryGetValue(key, out var v)` 加成功分支；`d.get(k, default)`→`dict.GetValueOrDefault(k, default)`；`k in d`→`dict.ContainsKey(k)`；`d.setdefault(k, v)`→`if (!dict.TryAdd(k, v)) { /* 已存在，读回原值 */ }`；需要插入顺序时改用 `List<KeyValuePair<K,V>>` 或额外的顺序索引集合，不能假定 `Dictionary` 保序；键为元组/复合值时自定义 `IEqualityComparer<TKey>`。
   - *不适用条件*：严禁把原样 `dict[key]` 机械写成 C# 索引器后仍按"返回默认值"继续执行（`KeyNotFoundException` 会改变失败路径）；严禁把 `d.get(k)` 的"缺失返回 `None`"改写为返回 `default(T)` 而不核对二者语义（数值键上 `None` 与 `0`、`false` 与 `0` 都会被折叠）；严禁依赖 `Dictionary<TKey,TValue>` 的遍历顺序复现 Python 的插入顺序。
5. **错误机械替换反例**：
   ```csharp
   // Python 原型：service_key = arguments.get("/servicekey")   # 缺失时为 None，后序有 is None 判断
   string serviceKey = arguments["/servicekey"];   // 错误：缺失抛 KeyNotFoundException，而非返回 null
   if (serviceKey != null) { useKey(serviceKey); } // 这段分支在源语言里是正常路径，现在变成崩溃
   // 正确：显式区分"缺失"与"存在但为空"，并让顺序语义可见
   string serviceKey = arguments.GetValueOrDefault("/servicekey"); // 缺失得到 null
   if (arguments.TryGetValue("/servicekey", out var found)) { useKey(found); }
   var ordered = new List<KeyValuePair<string, string>>(arguments);  // 需要插入顺序时显式保序
   ```
6. **信息不足或实现相关时的处理**：若源码依赖 `dict` 的插入顺序做输出或校验，必须确认该顺序是否为可观察行为，否则不能声称等价；自定义键对象的哈希/相等语义在目标侧需显式实现 `IEqualityComparer<TKey>`，无法确认时标为待确认。
7. **直接官方 HTTPS 依据链接**：[MS-API-DICTIONARY](https://learn.microsoft.com/en-us/dotnet/api/)；[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
