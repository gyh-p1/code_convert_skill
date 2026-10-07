# C# 语言共性语义（C# 12 / .NET 8）

> **用途**：供以 C# 为源语言或目标语言的方向 Skill 按需读取；本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 值类型（`struct`、内置数值、`enum`）变量保存值，赋值/传参/返回通常按值复制；引用类型（`class`、`interface`、`delegate`、`record class`）变量保存对象引用；`readonly struct` 与 `in` 参数只读传递。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` 内存分配位置（栈、堆、寄存器、内联嵌入）由 CoreCLR JIT 逃逸分析与优化裁定；装箱（Boxing）将值类型包装为堆上对象引用。
- **机械等价禁区与转换约束**：避免对分配位置作绝对假设（不作物理存储位置断言）；不可将引用传递机械等同于指针别名；**不得把 C# 的 `null` 判定、`""`/`0` 的真值判定与其他语言互相当作等价**（见下条）。
- **官方资料依据**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)

### L1-CS-01 null、空串与零值三种判定必须分开
1. **源码触发条件**：源码用 `x is null` / `x != null` / `string.IsNullOrEmpty` / `x.Length == 0` / `if (flag)` 分流，或把可空值类型与非空值类型混用。
2. **冻结版本/运行时/API 前提**：C# 12 / .NET 8；`is null` 匹配不调用任何用户重载，`== null` 可能调用重载运算符（[MS-CS-NULL](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/member-access-operators)、[MS-CS-OPERATOR](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/equality-operators)）。
3. **原可观察行为**：
   - `str is null` 只判“无对象”；空串 `""` **不是** null。
   - `string.IsNullOrEmpty(s)` 同时覆盖 null 与空串；`string.IsNullOrWhiteSpace(s)` 还覆盖全空白——**三者互不等价**。
   - `Nullable<T>` 的 `HasValue`/`Value` 与 `T` 的默认值是两套模型；`default(int?)` 为 null，`default(int)` 为 0。
   - C# 的 `if (obj)` 不成立（除 `bool` 与显式 `operator true/false`）；不存在 Python/Ruby 式任意对象真值判定。
4. **目标可选写法和不适用条件**：
   - *C# 作为源*：把“无对象”“空串”“全空白”“无值”分别映射到目标语言的对应检查；`IsNullOrEmpty` 必须展开为**两个**判定（null 或空），不能只映射其中一个。
   - *C# 作为目标*：源语言的真值判定必须显式重建为 `is null` / `Length == 0` 等；源为动态语言时，须先确认其假值集合（Ruby 只有 `nil`/`false` 为假）再决定是否引入空串检查。
   - *不适用条件*：源只判纯数值零值时不涉及 null，不要引入空值检查。
5. **错误机械替换反例**：
   ```csharp
   // 错误：把 Python 的 if not s 只映射成 null 判断，漏掉空串
   if (s is null) { return fallback; }        // s == "" 时未走兜底，下游行为改变
   // 错误之二：把 Go 的 err != nil 映射成任意对象真值判断（C# 无法编译/不成立）
   // 正确：按源的判定集合显式重建
   if (string.IsNullOrEmpty(s)) { return fallback; }   // 覆盖 null 与 ""
   ```
6. **信息不足或实现相关时的处理**：无法确定源的判定覆盖哪几种空状态时，标为“空值判定集合待确认”，不得用 `is null` 一概替代 `IsNullOrEmpty`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-NULL](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/member-access-operators)；[`string.IsNullOrEmpty`](https://learn.microsoft.com/en-us/dotnet/api/system.string.isnullorempty)；[`string.IsNullOrWhiteSpace`](https://learn.microsoft.com/en-us/dotnet/api/system.string.isnullorwhitespace)。

### L1-CS-05 程序实参不含程序名，参数绑定与默认值必须显式重建

1. **源码触发条件**：源码从 `Main(string[] args)` 取用实参，或用 `System.CommandLine`/第三方解析器绑定命名参数与位置参数，或依赖参数**默认值**。
2. **冻结版本/运行时/API 前提**：C# 12 / .NET 8（[`Main` 与 `args`](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/program-structure/main-command-line)）。
3. **原可观察行为**：
   - **`args` 不含程序名**——`args[0]` 即第一个用户实参（与 C/C++ 的 `argv[0]`、Go `os.Args[0]`、Python `sys.argv[0]` **不同**）。因此 `args.Length == 0` 表示"没有实参"。
   - 参数**默认值仅在参数被省略时生效**；显式传入与默认值相同的值**无法**由值本身区分，须用显式存在性标记。
4. **目标可选写法和不适用条件**：
   - *C# 作为源*：目标语言实参序列含程序名时（C/C++/Go/Python），必须**补上程序名偏移**；源里的 `args[0]` 对应目标 `argv[1]`/`os.Args[1]`/`sys.argv[1]`。
   - *C# 作为目标*：源的 `argv[1]`/`os.Args[1]` 对应目标的 `args[0]`，须**去掉**程序名；源的"无实参"重建为 `args.Length == 0`。
   - *不适用条件*：源码不使用命令行实参时不适用。
5. **错误机械替换反例**：
   ```csharp
   // 错误：把 C 的 argv 下标直接搬到 C#（args 不含程序名）
   string path = args[1];        // 源 C 的 argv[1] 应是这里的 args[0]
   if (args.Length < 2) { usage(); }   // 源 argc<2 → 这里应为 args.Length < 1
   // 正确
   if (args.Length < 1) { usage(); }
   string path = args[0];
   ```
   ```text
   反方向（C# → C/C++/Go/Python）：
     源 args[0]  → 目标 argv[1] / os.Args[1] / sys.argv[1]
     源 args.Length == 0 → 目标 argc == 1 / len(os.Args) <= 1 / len(sys.argv) <= 1
   ```
6. **信息不足或实现相关时的处理**：无法确认目标语言实参序列是否含程序名时，标为“实参偏移待确认”；不得凭“都叫 args/argv”推断下标一致。
7. **直接官方 HTTPS 依据链接**：[C# `Main` 与 `args`](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/program-structure/main-command-line)；[POSIX `exec` 的 `argv`（程序名在 `argv[0]`）](https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html)；[Go `os.Args`](https://pkg.go.dev/os#pkg-variables)；[Python `sys.argv`](https://docs.python.org/3.12/library/sys.html#sys.argv)。

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` `sbyte`/`byte` (8), `short`/`ushort` (16), `int`/`uint` (32), `long`/`ulong` (64), `nint`/`nuint` (原生宽度)。
- **有符号溢出行为**：`[语言规范保证]` 默认处于 `unchecked` 上下文：**按补码截断回绕**；在 `checked` 作用域或编译选项下超出表示范围抛出 `OverflowException`。
- **无符号溢出行为**：`[语言规范保证]` **按模截断回绕**（在 `checked` 作用域下若超出上限同样抛出 `OverflowException`）。
- **隐式提升与转换陷阱**：`[语言规范保证]` 较小整型进行算术运算时自动提升为 `int`，必须显式强转回目标窄类型。
- **官方资料依据**：[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)

### L1-CS-02 数值文本输出必须钉住格式提供程序与区域设置
1. **源码触发条件**：源码把数值转成文本——`ToString()`、`$"{x}"` 内插、`string.Format`、`Console.WriteLine(x)`。
2. **冻结版本/运行时/API 前提**：C# 12 / .NET 8；数值格式化的**默认提供程序是当前区域设置** `CultureInfo.CurrentCulture`（[MS-CS-FORMAT](https://learn.microsoft.com/en-us/dotnet/standard/base-types/formatting-types)、[`IFormattable.ToString`](https://learn.microsoft.com/en-us/dotnet/api/system.iformattable.tostring)）。
3. **原可观察行为**：
   - 默认格式化**受当前区域设置影响**：小数点符号、千位分组、负数符号都可能改变（如 `1.5` → `1,5`）。
   - `ToString("R")`/`"G17"` 与 `ToString()` 的**有效位数不同**；`double` 的往返格式与默认格式输出不同文本。
   - `DateTime` 与 `TimeSpan` 同样受区域设置影响，且 `DateTime.ToString()` 的默认模式与不变区域不同。
4. **目标可选写法和不适用条件**：
   - *C# 作为源*：目标语言的格式化必须显式冻结区域设置与精度；若源依赖固定区域（如 Go `strconv.FormatFloat`、Python `str`），目标须用 `CultureInfo.InvariantCulture` 或等价的固定格式。
   - *C# 作为目标*：源语言若已固定区域，目标**不得**继承 `CurrentCulture`；跨机器/跨区域复现时尤其致命。
   - *不适用条件*：源**有意**按用户区域设置展示（本地化 UI 输出）时，区域依赖是应保留的行为，须显式冻结区域而不是消除。
5. **错误机械替换反例**：
   ```csharp
   // 错误：源用固定区域输出，"1.5" 在 de-DE 机器上变成 "1,5"
   Console.WriteLine(value);                       // 受 CurrentCulture 影响
   // 错误之二：用默认精度冒充源的往返精度
   var s = (1.0 / 3).ToString();                   // "0.333333333333333"，位数与源不同
   // 正确：钉住不变区域与显式格式
   Console.WriteLine(value.ToString("R", CultureInfo.InvariantCulture));
   Console.WriteLine(value.ToString("F6", CultureInfo.InvariantCulture)); // 精度按源义务冻结
   ```
6. **信息不足或实现相关时的处理**：无法确定源的有效位数与区域依赖时，标为“数值格式与区域设置待确认”，并把该文本列入 oracle 观察点。
7. **直接官方 HTTPS 依据链接**：[MS-CS-FORMAT](https://learn.microsoft.com/en-us/dotnet/standard/base-types/formatting-types)；[`CultureInfo.InvariantCulture`](https://learn.microsoft.com/en-us/dotnet/api/system.globalization.cultureinfo.invariantculture)。

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `System.String`（不可变对象，UTF-16 代码单元序列，显式长度）。
- **字节序列数据结构**：`[语言规范保证]` `byte[]` 或 `ReadOnlySpan<byte>`。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` 字符串内部允许包含 `\0`，不作为终止符；互操作与流输出时需显式注意 C 语言 NUL 终止符差异。
- **编码假设与转换陷阱**：`[语言规范保证]` 索引与 `Length` 按 UTF-16 代码单元计量，代理对占用 2 个代码单元。
- **官方资料依据**：[MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)

### L1-CS-03 `byte[]` 与 `string` 之间必须显式编码，且不得为掩盖差异而替换字节
1. **源码触发条件**：源码在 `byte[]`/`Stream` 与 `string` 之间转换（`Encoding.*.GetString/GetBytes`、`StreamReader`/`StreamWriter`、`File.ReadAllText` vs `File.ReadAllBytes`），或对字节做哈希、压缩与协议帧处理。
2. **冻结版本/运行时/API 前提**：C# 12 / .NET 8；`Encoding.UTF8` 的无效字节处理与 `Encoding.Default` 的平台依赖性见 [MS-CS-ENCODING](https://learn.microsoft.com/en-us/dotnet/api/system.text.encoding)、[`UTF8Encoding`](https://learn.microsoft.com/en-us/dotnet/api/system.text.utf8encoding)。
3. **原可观察行为**：
   - `Encoding.UTF8.GetString` 对非法字节序列**默认用 U+FFFD 替换**（不抛异常），长度与内容都会改变。
   - `new UTF8Encoding(false, true)` 才在非法序列上抛 `DecoderFallbackException`。
   - `.NET Core` 起 `Encoding.Default` 是 UTF-8（不再是系统 ANSI 代码页）；`StreamReader` 默认 UTF-8 且**默认检测 BOM**，`File.ReadAllText` 亦同——是否消费 BOM 会改变首字节。
   - `string` 索引与 `Length` 按 UTF-16 代码单元，非 ASCII 时**不等于**字节数。
4. **目标可选写法和不适用条件**：
   - *C# 作为源*：字节路径必须映射到目标语言的字节类型；文本路径须显式声明编码与 BOM 策略，且不得依赖目标的默认编码。
   - *C# 作为目标*：源语言若以字节为单位，必须走 `byte[]`/`Stream`，**不得**先转 `string` 再处理；仅在需要文本时显式 `Encoding.UTF8.GetString`，并保留源对非法字节的处理方式。
   - *不适用条件*：源确为文本且 BOM 探测是可观察行为（如配置文件读取）时，BOM 处理应**保留**而非消除。
5. **错误机械替换反例**：
   ```csharp
   // 错误：把字节内容经 string 往返，非法字节被替换为 U+FFFD
   string text = Encoding.UTF8.GetString(blob);      // 非法序列 → '\uFFFD'，字节已变
   byte[] back = Encoding.UTF8.GetBytes(text);       // 与 blob 不再相等
   // 错误之二：用 Encoding.Default 冒充源的固定编码（跨平台含义不同）
   var s = Encoding.Default.GetString(blob);
   // 正确：字节进字节出，文本路径显式冻结编码与错误策略
   var sum = SHA256.HashData(blob);                  // 哈希直接对字节做
   string text = new UTF8Encoding(false, throwOnInvalidBytes: true).GetString(blob);
   ```
6. **信息不足或实现相关时的处理**：无法确认源的编码、BOM 策略或非法字节处置时，标为“编码与字节长度语义待确认”；**禁止**用 `Encoding.UTF8.GetString` 的默认替换行为掩盖差异——替换属不可逆信息丢失。也不得用 `string.Length` 承接源按字节计的长度。
7. **直接官方 HTTPS 依据链接**：[MS-CS-ENCODING](https://learn.microsoft.com/en-us/dotnet/api/system.text.encoding)；[`UTF8Encoding`（错误回退策略）](https://learn.microsoft.com/en-us/dotnet/api/system.text.utf8encoding)；[`StreamReader`](https://learn.microsoft.com/en-us/dotnet/api/system.io.streamreader)。

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` `T[]` 为连续内存固定大小数组；`List<T>` 为动态扩容集合；`[指定运行时的实现相关事实]` 扩容策略具均摊常数复杂度。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `Dictionary<TKey, TValue>` 为键值哈希映射；`SortedDictionary<TKey, TValue>` 为按键有序树映射。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` `Dictionary` 不保证遍历顺序，绝对禁止依赖；`SortedDictionary` 严格按键排序。
- **迭代期间修改（Fail-Fast）**：`[语言规范保证]` `foreach` 迭代中若集合发生修改立即抛出 `InvalidOperationException`。
- **官方资料依据**：[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators)

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` 强类型异常与结构化 `try`/`catch`/`finally`，以 `System.Exception` 为顶层根类。
- **异常展开与性能模型**：`[指定运行时的实现相关事实]` 两阶段异常展开；`finally` 块保证清理；未捕获异常导致应用程序退出。
- **进程退出码回传机制**：`[指定运行时的实现相关事实]` `Environment.Exit(int)` 立即退出；未捕获异常退出码由 CLR 运行时代管。
- **跨语言映射关键风险**：异常不得用于常规业务流分支控制；非托管错误码需显式转为相应异常或保持密封。
- **官方资料依据**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)

### L1-CS-04 源端被丢弃的错误不得变成未捕获异常，源端主动失败不得被静默吞掉
1. **源码触发条件**：源码忽略可失败调用的结果（未检查 `bool` 返回的 `Try*`、`catch` 后空处理、丢弃 `Task` 的 `Exception`），**或**在失败时 `throw`、`Environment.Exit(非零)`、`return false`。
2. **冻结版本/运行时/API 前提**：C# 12 / .NET 8；未捕获异常导致进程终止且**退出码由 CLR 代管**（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)、[`Environment.Exit`](https://learn.microsoft.com/en-us/dotnet/api/system.environment.exit)）。
3. **原可观察行为**：
   - 忽略错误的路径：目标不终止，继续并产出**当时能达到的结果**；但**被丢弃的 `Task` 异常**会在 GC 时触发 `UnobservedTaskException`，属独立的可观察事件。
   - 主动失败的路径：`throw` 展开并经 `finally` 清理；未捕获时进程终止，退出码由 CLR 决定（**不是**源显式指定的那个码）。
4. **目标可选写法和不适用条件**（两个方向都必须覆盖）：
   - *源丢弃错误 → 目标不得变成异常终止*：源忽略失败的位置须映射为非致命路径，保留后续执行与最终退出码。
   - *源主动失败 → 目标不得静默继续*：不得用 `catch (Exception) { }`、`catch { }` 把失败吞成成功；也不得把源的非零退出码替换成“不终止”。
   - *不适用条件*：源**确实捕获并有意继续**的路径（如逐文件容错），保留该继续行为是**正确**的，不得反向改成终止。
5. **错误机械替换反例**：
   ```csharp
   // 错误：源忽略打开失败并继续，目标却让异常逃逸终止进程
   var text = File.ReadAllText(path);        // FileNotFoundException 未处理 → 提前终止
   // 错误之二：把源的显式失败分支吞掉
   try { Run(); } catch (Exception) { }      // 静默继续，退出码变成 0
   // 正确：按源的实际检查行为分别重建
   string? text = null;
   try { text = File.ReadAllText(path); }
   catch (IOException) { /* 仅当源确实忽略该失败时 */ }
   if (text is null) { /* 源的“空结果继续”路径 */ }
   ```
6. **信息不足或实现相关时的处理**：无法确认源是否检查返回值、是否输出诊断、失败后是否继续时，把该错误路径单列为待验证 oracle；不得以“捕获更保险”为由改变控制流。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)；[`Environment.Exit`](https://learn.microsoft.com/en-us/dotnet/api/system.environment.exit)；[`TaskScheduler.UnobservedTaskException`](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.taskscheduler.unobservedtaskexception)。

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[指定运行时的实现相关事实]` CoreCLR 自动分代垃圾回收（Generation 0, 1, 2）；非托管资源由平台安全句柄或包装类管理。
- **资源确定性释放机制**：`[指定运行时的实现相关事实]` `using` 语句 / `using var` 声明调用 `IDisposable.Dispose()`；终结器（Finalizer）执行时机非确定。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 基于代际标记压缩的分代垃圾回收；非内存资源必须由 `IDisposable.Dispose` 或 `using` 显式保障释放。
- **悬垂与泄漏防范**：事件未注销（`+=` 未 `-=`）会导致订阅者被强引用而长久内存泄漏。
- **官方资料依据**：[MS-CS-GC](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals)

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` 基于 Task 的异步模式（TAP：`async`/`await`）；`Task`/`Task<TResult>` 异步状态机。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` CLR 线程池调度托管任务与 OS 线程映射，受工作窃取算法管理。
- **级联取消与超时机制**：`[指定运行时的实现相关事实]` 统一的 `CancellationToken` / `CancellationTokenSource` 级联协作取消模型。
- **内存模型与数据竞争**：`[指定运行时的实现相关事实]` 共享可变状态多线程访问需 `lock` (`Monitor`) 或原子操作同步，否则发生数据竞争。
- **官方资料依据**：[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)<br>[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)

## 使用边界

将本页与所选的源→目标方向 Skill 及另一语言的共性页组合使用；映射前先确认源码真实行为。文件、网络、并发和跨 OS API 的具体差异仍按[共性索引的场景/系统分流](../seven-language-common-semantics.md)选读，不从语言事实直接推断系统 API 等价。没有逐例第三方证据时，语法/构建与功能结论保持 `UNVERIFIED`；本机不运行或编译样本。
