# C# 语言共性语义（C# 12 / .NET 8）

> **用途**：供以 C# 为源语言或目标语言的方向 Skill 按需读取；本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 值类型（`struct`、内置数值、`enum`）变量保存值，赋值/传参/返回通常按值复制；引用类型（`class`、`interface`、`delegate`、`record class`）变量保存对象引用；`readonly struct` 与 `in` 参数只读传递。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` 内存分配位置（栈、堆、寄存器、内联嵌入）由 CoreCLR JIT 逃逸分析与优化裁定；装箱（Boxing）将值类型包装为堆上对象引用。
- **机械等价禁区与转换约束**：避免对分配位置作绝对假设（不作物理存储位置断言）；不可将引用传递机械等同于指针别名。
- **官方资料依据**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` `sbyte`/`byte` (8), `short`/`ushort` (16), `int`/`uint` (32), `long`/`ulong` (64), `nint`/`nuint` (原生宽度)。
- **有符号溢出行为**：`[语言规范保证]` 默认处于 `unchecked` 上下文：**按补码截断回绕**；在 `checked` 作用域或编译选项下超出表示范围抛出 `OverflowException`。
- **无符号溢出行为**：`[语言规范保证]` **按模截断回绕**（在 `checked` 作用域下若超出上限同样抛出 `OverflowException`）。
- **隐式提升与转换陷阱**：`[语言规范保证]` 较小整型进行算术运算时自动提升为 `int`，必须显式强转回目标窄类型。
- **官方资料依据**：[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `System.String`（不可变对象，UTF-16 代码单元序列，显式长度）。
- **字节序列数据结构**：`[语言规范保证]` `byte[]` 或 `ReadOnlySpan<byte>`。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` 字符串内部允许包含 `\0`，不作为终止符；互操作与流输出时需显式注意 C 语言 NUL 终止符差异。
- **编码假设与转换陷阱**：`[语言规范保证]` 索引与 `Length` 按 UTF-16 代码单元计量，代理对占用 2 个代码单元。
- **官方资料依据**：[MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)

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
