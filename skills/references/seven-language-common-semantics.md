# 七语言共性语义与机制参考库

> **文档性质**：七语言共享语义事实真源（依据《任务 02：D3–D6 共性机制与高风险方向规则》§4 D3）
> **适用基线**：C11、C++17、C# 12/.NET 8、CPython 3.12、Go 1.27、PowerShell 7.6、CRuby 3.4
> **使用方式**：由各语言转换方向 Skill 实际链接与按需消费，不按 42 个方向复制。遇跨 OS、文件/网络系统 API 时转向既有 B 类规则。
> **分类体系规范**：每项事实必须严格属于下列三类之一：
> - `[语言规范保证]`：由语言标准、规范或官方定义保证的确定性语义；
> - `[指定运行时的实现相关事实]`：仅适用于冻结运行时基线的实现行为，非跨实现规范保证；
> - `[待专题核验，不可用于确定转换规则]`：缺乏冻结版本一手官方资料支撑，严禁作为转换规则前提。

---

## 一、值、引用、别名与可变性

| 语言与冻结基线 | 语言规范保证 | 实现相关 / 运行时优化行为 | 机械等价禁区与转换约束 | 官方资料依据 |
|---|---|---|---|---|
| **C**<br>(ISO C11) | `[语言规范保证]` 默认纯值传递；指针传递指针值；`const` 仅声明只读视窗，不保证对象物理不可变；严格别名规则（Strict Aliasing）：不同类型指针强转互解引用属于未定义行为（UB）（`char*` 除外）。 | `[指定运行时的实现相关事实]` 变量物理分配位置（寄存器/栈/静态区/堆）由编译器优化与存储期决定，非跨实现语言保证；对齐边界由 ABI 决定。 | 严禁用指针强转在不同类型间做物理重解释；不可假定值拷贝开销固定。 | [WG14-N1570 §6.5 ¶7, §6.7.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) |
| **C++**<br>(ISO C++17) | `[语言规范保证]` 纯值传递与显式左值引用（`&`）/右值引用（`&&`）；移动语义（Move Semantics）转移资源所有权，原对象进入有效但未指定状态；`const` 限定符在类型系统中强制。 | `[语言规范保证]` 复制省略（Guaranteed Copy Elision / RVO）由规范强制；`[指定运行时的实现相关事实]` 具体内存分配由存储期与编译器裁定。 | 不可将 C++ 移动语义机械等同于浅拷贝或解引用；移动后原对象析构仍会被调用。 | [WG21-N4659 Clause 11.3, Clause 15.8](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf) |
| **C#**<br>(C# 12 / .NET 8) | `[语言规范保证]` 值类型（`struct`、内置数值、`enum`）变量保存值，赋值/传参/返回通常按值复制；引用类型（`class`、`interface`、`delegate`、`record class`）变量保存对象引用；`readonly struct` 与 `in` 参数只读传递。 | `[指定运行时的实现相关事实]` 内存分配位置（栈、堆、寄存器、内联嵌入）由 CoreCLR JIT 逃逸分析与优化裁定；装箱（Boxing）将值类型包装为堆上对象引用。 | 避免对分配位置作绝对假设（不作物理存储位置断言）；不可将引用传递机械等同于指针别名。 | [MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types) |
| **Python**<br>(CPython 3.12) | `[语言规范保证]` 一切变量皆为对象引用；赋值仅绑定名字与对象，传参为“对象引用按值传递”；对象分为不可变（`int`、`float`、`str`、`tuple`、`frozenset`、`bytes`）与可变（`list`、`dict`、`set`、`bytearray`）。 | `[指定运行时的实现相关事实]` CPython 采用小整数与短字符串驻留（Interning），属于解释器优化细节，非跨实现语言保证；具体内存由解释器内存池管理。 | 严禁将可变容器（如 `list`）的直接赋值当作独立拷贝（修改会产生隐式别名污染）。 | [PY-REF-DATA §3.1](https://docs.python.org/3.12/reference/datamodel.html) |
| **Go**<br>(Go 1.27) | `[语言规范保证]` 严格纯值传递；指针传递指针值（内存地址拷贝），显式指针禁用算术运算（除 `unsafe.Pointer`）；切片、map、channel、interface 内部包含指针头部，值传递时其底层数据共享。 | `[指定运行时的实现相关事实]` 编译器逃逸分析（Escape Analysis）决定变量分配在 Goroutine 栈还是堆上，属于编译器实现细节，语言规范不作物理存储位置保证。 | 不可认为切片传递是深拷贝（共享底层数组）；切片扩容后会静默与原数组分离。 | [GO-SPEC #Type_identity, #Slice_types](https://go.dev/ref/spec) |
| **PowerShell**<br>(PowerShell 7.6) | `[语言规范保证]` 变量持有 .NET 对象引用；标量基本类型按值语义求值；管道传递对象流时通过 `PSObject` 包装层反射解包。 | `[指定运行时的实现相关事实]` 管道对象解包与属性投影开销受 PowerShell 引擎管道缓冲区机制支配。 | 管道单元素展开（Unrolling）会将单元素数组隐式退化为标量，破坏类型契约。 | [MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines) |
| **Ruby**<br>(CRuby 3.4) | `[语言规范保证]` 纯面向对象模型；一切变量皆持有对象的引用；可变对象原地修改（如 `String#<<`、`Array#push`），不可变对象包含 `Integer`、`Float`、`Symbol`、`true`、`false`、`nil`。 | `[指定运行时的实现相关事实]` 立即数（Immediate values：Fixnum、Symbol 等）在 MRI 中直接编码在指针位中，无独立堆分配，属于实现优化。 | 严禁忽视 Ruby 原地方法（带 `!` 或 `<<`）对全部别名持有者的同步副作用。 | [RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/) |

---

## 二、整数宽度、溢出、符号性与转换

| 语言与冻结基线 | 整数宽度规范 | 有符号溢出行为 | 无符号溢出行为 | 隐式提升与转换陷阱 | 官方资料依据 |
|---|---|---|---|---|---|
| **C**<br>(ISO C11) | `[语言规范保证]` `short` $\ge 16$, `int` $\ge 16$, `long` $\ge 32$, `long long` $\ge 64$ 位；精确宽度见 `<stdint.h>`。 | `[语言规范保证]` **未定义行为（Undefined Behavior, UB）**；编译器假定不溢出并优化代码。 | `[语言规范保证]` **按模截断回绕**（Modulo $2^n$），属于严格合法的确定性行为。 | `[语言规范保证]` 整型提升（Integer Promotion）：小于 `int` 的类型先提升为 `int`；有/无符号混算转为无符号。 | [WG14-N1570 §6.2.5, §6.3.1.1, §6.5 ¶5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) |
| **C++**<br>(ISO C++17) | `[语言规范保证]` 宽度规则继承 C；定义 `std::int32_t` 等定宽类型。 | `[语言规范保证]` **未定义行为（UB）**（规范与 C 保持严格一致）。 | `[语言规范保证]` **按模截断回绕**（Modulo $2^n$）。 | `[语言规范保证]` 继承 C 整型提升规则；`std::size_t` 与带符号整数比较易引发反常循环。 | [WG21-N4659 Clause 6.9.1, Clause 7.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf) |
| **C#**<br>(C# 12 / .NET 8) | `[语言规范保证]` `sbyte`/`byte` (8), `short`/`ushort` (16), `int`/`uint` (32), `long`/`ulong` (64), `nint`/`nuint` (原生宽度)。 | `[语言规范保证]` 默认处于 `unchecked` 上下文：**按补码截断回绕**；在 `checked` 作用域或编译选项下超出表示范围抛出 `OverflowException`。 | `[语言规范保证]` **按模截断回绕**（在 `checked` 作用域下若超出上限同样抛出 `OverflowException`）。 | `[语言规范保证]` 较小整型进行算术运算时自动提升为 `int`，必须显式强转回目标窄类型。 | [MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked) |
| **Python**<br>(CPython 3.12) | `[语言规范保证]` `int` 为**任意精度整数**（Arbitrary-precision integer），理论上仅受可用内存限制；无固定定宽整数。 | `[语言规范保证]` **无溢出概念**；数值超出 64 位自动扩展内存表示。 | `[语言规范保证]` **无溢出概念**；不支持无符号数原生类型。 | `[语言规范保证]` 无法原生模拟定宽溢出截断；若需定宽溢出行为，必须显式施加位掩码（`& 0xFFFFFFFF`）。 | [PY-REF-DATA §3.2 Numbers](https://docs.python.org/3.12/reference/datamodel.html) |
| **Go**<br>(Go 1.27) | `[语言规范保证]` `int8`..`int64`, `uint8`..`uint64` 严格定宽；`int`/`uint` 大小取决于架构（32 或 64 位）；`uintptr` 存指针位。 | `[语言规范保证]` **按补码截断回绕**（二进制算术确定行为，非 UB）；**常数表达式溢出属于编译错误**。 | `[语言规范保证]` **按模截断回绕**（二进制算术确定行为）。 | `[语言规范保证]` **严格禁止隐式类型转换**；即使 `int32` 与 `int` 在 64 位架构下同宽，亦必须显式强制转换。 | [GO-SPEC #Numeric_types, #Arithmetic_operators](https://go.dev/ref/spec) |
| **PowerShell**<br>(PowerShell 7.6) | `[语言规范保证]` 底层为 .NET 整数体系；支持整型字面量后缀（`100L`, `1000D` 等）。 | `[指定运行时的实现相关事实]` 默认算术超出当前类型上限时，PowerShell 引擎会**自动提升为更大宽度整型**（如 `[int32]::MaxValue + 1` 自动转为 `[int64]` 或 `[double]`）。 | `[指定运行时的实现相关事实]` 显式通过 .NET 静态方法或强类型声明时遵循 .NET `unchecked` 回绕规则。 | `[指定运行时的实现相关事实]` 动态弱类型转换系统在算术中自动升级类型，可能破坏对底层二进制溢出截断的依赖。 | [MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables) |
| **Ruby**<br>(CRuby 3.4) | `[语言规范保证]` `Integer` 统一表示（具备任意精度整数语义）。 | `[语言规范保证]` **无溢出概念**；超出机器字长时自动无缝升级为大数表示。 | `[语言规范保证]` 无原生无符号整数；按位操作将负数视为无限补码展开。 | `[语言规范保证]` 位操作中未显式截断可能导致带符号大数，需显式使用 `& ((1 << N) - 1)` 保持位宽。 | [RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/) |

---

## 三、字符串、字节、NUL、Unicode 与编码

| 语言与冻结基线 | 字符串数据结构 | 字节序列数据结构 | NUL (`\0`) 字符语义与处理 | 编码假设与转换陷阱 | 官方资料依据 |
|---|---|---|---|---|---|
| **C**<br>(ISO C11) | `[语言规范保证]` `char*` / `char[]` 以 `\0` 字节结尾的序列；无内置长度记录字段。 | `[语言规范保证]` `unsigned char[]` / `uint8_t[]`；必须外部显式传递长度。 | `[语言规范保证]` **`\0` 是字符串的唯一终止标记**；中间出现 `\0` 将导致截断；若末尾缺少 `\0` 导致越界读取 UB。 | `[语言规范保证]` C 语言本身不假设编码（视平台/终端为 ASCII/UTF-8/GBK 等本地代码页）；宽字符由 `wchar_t` 支持。 | [WG14-N1570 §7.1.1, §7.24](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) |
| **C++**<br>(ISO C++17) | `[语言规范保证]` `std::string`（显式长度 + 缓冲区）；`std::string_view`（非拥有视窗：指针 + 长度）。 | `[语言规范保证]` `std::vector<uint8_t>` 或 `std::byte[]`。 | `[语言规范保证]` `std::string` 允许内容包含内部 `\0`，`size()` 独立于内容；`c_str()` 追加尾随 `\0`；`std::string_view` **不保证以 `\0` 结尾**。 | `[语言规范保证]` 基础类型按代码单元操作；标准库不执行隐式编码转码。 | [WG21-N4659 Clause 24.3, Clause 24.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf) |
| **C#**<br>(C# 12 / .NET 8) | `[语言规范保证]` `System.String`（不可变对象，UTF-16 代码单元序列，显式长度）。 | `[语言规范保证]` `byte[]` 或 `ReadOnlySpan<byte>`。 | `[语言规范保证]` 字符串内部允许包含 `\0`，不作为终止符；互操作与流输出时需显式注意 C 语言 NUL 终止符差异。 | `[语言规范保证]` 索引与 `Length` 按 UTF-16 代码单元计量，代理对占用 2 个代码单元。 | [MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/) |
| **Python**<br>(CPython 3.12) | `[语言规范保证]` `str`：不可变 Unicode 码点序列。 | `[语言规范保证]` `bytes`：不可变 8 位字节序列；`bytearray`：可变字节序列。 | `[语言规范保证]` `str` 与 `bytes` 均显式记录长度，内容可自由包含 `\0`。 | `[语言规范保证]` **`str` 与 `bytes` 严格隔离**；严禁隐式转换，必须显式通过 `.encode('utf-8')` 与 `.decode('utf-8')` 互转。 | [PY-REF-DATA §3.2 Strings, Bytes](https://docs.python.org/3.12/reference/datamodel.html) |
| **Go**<br>(Go 1.27) | `[语言规范保证]` `string`：只读字节切片头部（指针 + 长度）；通常但非强制保存 UTF-8 编码字节。 | `[语言规范保证]` `[]byte`：可变 8 位字节切片。 | `[语言规范保证]` 字符串由显式 `len` 界定，允许内部包含 `\0`；跨系统 C 调用需显式转为 NUL 结尾。 | `[语言规范保证]` `for range string` 按 UTF-8 解码出 Unicode 码点（`rune`），直接下标索引 `str[i]` 访问的是裸字节。 | [GO-SPEC #String_types, #For_statements](https://go.dev/ref/spec) |
| **PowerShell**<br>(PowerShell 7.6) | `[语言规范保证]` 基于 .NET `System.String`（不可变 UTF-16 字符串）。 | `[语言规范保证]` `[byte[]]` 数组。 | `[语言规范保证]` 内容中允许包含 `\0`；重定向到外部原生程序可能受宿主控制台编码截断。 | `[指定运行时的实现相关事实]` PowerShell 7+ 默认将文件重定向与外部管道输出编码设为 UTF-8（无 BOM）。 | [MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines) |
| **Ruby**<br>(CRuby 3.4) | `[语言规范保证]` `String`：可变字节序列，**显式附带 `Encoding` 元数据标签**（默认 UTF-8）。 | `[语言规范保证]` 同样为 `String`，其编码标记为 `Encoding::BINARY` (`ASCII-8BIT`)。 | `[语言规范保证]` 显式记录长度，允许包含 `\0` 字节；底层 C 扩展遇到 `\0` 可能抛出 `ArgumentError`。 | `[语言规范保证]` 两个不同 Encoding 的 String 进行拼接时，若无法无损转码将抛出 `Encoding::CompatibilityError`。 | [RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/) |

---

## 四、数组、容器、切片、迭代和顺序

| 语言与冻结基线 | 数组/切片连续性与扩容 | 键值映射（Map/Dict）实现 | Map 遍历迭代顺序保证 | 迭代期间修改（Fail-Fast） | 官方资料依据 |
|---|---|---|---|---|---|
| **C**<br>(ISO C11) | `[语言规范保证]` 静态原生数组物理连续；动态数组依赖 `malloc`/`realloc` 手工管理，扩容可能迁移地址并使外部旧指针失效。 | `[语言规范保证]` 无语言内建映射容器；必须依赖第三方库或手工哈希表。 | `[语言规范保证]` 无原生规范；完全取决于手写实现。 | `[语言规范保证]` 手写遍历中若发生重分配，旧迭代指针立即悬挂（UB）。 | [WG14-N1570 §6.2.5, §7.22.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) |
| **C++**<br>(ISO C++17) | `[语言规范保证]` `std::vector` 元素存储物理连续；`std::array` 固定容量连续存储，存储期与宿主对象一致；`[指定运行时的实现相关事实]` `vector` 扩容增长策略由实现决定，规范仅保证均摊常数复杂度。 | `[语言规范保证]` `std::map` 为按键比较严格有序关联容器；`std::unordered_map` 为无序关联容器。 | `[语言规范保证]` `std::map` 严格按键排序遍历；`std::unordered_map` 不保证任何顺序，重哈希可能改变顺序。 | `[语言规范保证]` 容器修改可能引发迭代器失效（`vector` 插入可能失效全部迭代器；树节点关联容器插入不失效现有节点迭代器）。 | [WG21-N4659 Clause 26](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf) |
| **C#**<br>(C# 12 / .NET 8) | `[语言规范保证]` `T[]` 为连续内存固定大小数组；`List<T>` 为动态扩容集合；`[指定运行时的实现相关事实]` 扩容策略具均摊常数复杂度。 | `[语言规范保证]` `Dictionary<TKey, TValue>` 为键值哈希映射；`SortedDictionary<TKey, TValue>` 为按键有序树映射。 | `[语言规范保证]` `Dictionary` 不保证遍历顺序，绝对禁止依赖；`SortedDictionary` 严格按键排序。 | `[语言规范保证]` `foreach` 迭代中若集合发生修改立即抛出 `InvalidOperationException`。 | [MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators) |
| **Python**<br>(CPython 3.12) | `[语言规范保证]` `list`：动态可变序列；`tuple`：固定长度不可变序列。 | `[语言规范保证]` `dict`：键值映射类型。 | `[语言规范保证]` **语言规范保证保持键值对的插入顺序**（Insertion-order preservation）。 | `[语言规范保证]` 迭代中改变 `dict` 大小立即抛出 `RuntimeError: dictionary changed size during iteration`。 | [PY-REF-DATA §3.2 Dictionaries](https://docs.python.org/3.12/reference/datamodel.html) |
| **Go**<br>(Go 1.27) | `[语言规范保证]` 切片（`[]T`）为 `(ptr, len, cap)` 结构；`append` 超出 cap 时自动重分配新底层数组；`[指定运行时的实现相关事实]` 切片扩容策略属于实现相关行为，规则不得依赖具体增长比例或阈值。 | `[语言规范保证]` `map[K]V` 为内建映射类型，值传递共享数据引用。 | `[语言规范保证]` **Go 规范明确未规定 map 迭代顺序**；转换后代码绝对不得依赖遍历顺序。 | `[语言规范保证]` Go 数据竞争是错误，必须通过同步机制避免；`[指定运行时的实现相关事实]` 运行时若检测到并发写操作可能终止程序。 | [GO-SPEC #Map_types, #Range_clause](https://go.dev/ref/spec) |
| **PowerShell**<br>(PowerShell 7.6) | `[语言规范保证]` 数组底层为固定大小 `object[]`；`[指定运行时的实现相关事实]` `+=` 追加元素会导致分配新数组并全量复制元素；存在单元素自动展开为标量机制。 | `[语言规范保证]` `[hashtable]` 与 `[ordered]@{}` 映射结构。 | `[语言规范保证]` 默认 `hashtable` 遍历无序；显式声明 `[ordered]@{}` 保证插入顺序。 | `[指定运行时的实现相关事实]` 遍历中修改集合会抛出集合已修改异常。 | [MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)<br>[MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables) |
| **Ruby**<br>(CRuby 3.4) | `[语言规范保证]` `Array` 为内建可变序列容器，支持负数下标索引。 | `[语言规范保证]` `Hash` 为内建键值映射容器。 | `[语言规范保证]` **语言规范保证保持键的插入顺序**。 | `[语言规范保证]` 迭代中修改散列表键值可能导致遗漏或抛出异常。 | [RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)<br>[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html) |

---

## 五、异常、错误、退出码与可观察失败

| 语言与冻结基线 | 语言级错误表示机制 | 异常展开与性能模型 | 进程退出码回传机制 | 跨语言映射关键风险 | 官方资料依据 |
|---|---|---|---|---|---|
| **C**<br>(ISO C11) | `[语言规范保证]` 返回值整数错误码（`int`）、输出参数或全局 `errno`（正整数，宏展开为线程局部左值）；无语言级异常。 | `[语言规范保证]` 无异常展开；`setjmp`/`longjmp` 仅做非局部长跳转（不调用析构/清理）。 | `[语言规范保证]` `exit(int status)` 或 `main` 返回值回传进程退出码；`[指定运行时的实现相关事实]` 操作系统对退出状态位宽的处理属于平台环境范畴。 | 严禁将 C 返回值机械替换为异常（会改变调用方控制流拓扑与执行开销）；`errno` 易受后续调用覆盖。 | [WG14-N1570 §7.5, §7.22.4.4](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) |
| **C++**<br>(ISO C++17) | `[语言规范保证]` `try`/`catch`/`throw` 异常处理；无 `std::expected`（C++23）；错误码模式（`std::error_code`）。 | `[语言规范保证]` 语言规范定义异常类型体系与栈展开（Stack Unwinding）语义，沿栈逆序调用已构造局部对象的析构函数（RAII 展开）；标准不作底层“零成本”实现保证。 | `[语言规范保证]` 继承 C 的 `exit()` 与 `main` 返回机制；未捕获异常导致调用 `std::terminate()` 异常终止。 | **严禁让 C++ 异常跨越 C ABI 边界**；跨界必须在边界包裹 `try ... catch(...)` 并转为错误码。 | [WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf) |
| **C#**<br>(C# 12 / .NET 8) | `[语言规范保证]` 强类型异常与结构化 `try`/`catch`/`finally`，以 `System.Exception` 为顶层根类。 | `[指定运行时的实现相关事实]` 两阶段异常展开；`finally` 块保证清理；未捕获异常导致应用程序退出。 | `[指定运行时的实现相关事实]` `Environment.Exit(int)` 立即退出；未捕获异常退出码由 CLR 运行时代管。 | 异常不得用于常规业务流分支控制；非托管错误码需显式转为相应异常或保持密封。 | [MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/) |
| **Python**<br>(CPython 3.12) | `[语言规范保证]` 异常驱动控制流（EAFP：Easier to Ask for Forgiveness than Permission）；`try`/`except`/`finally`/`else`。 | `[语言规范保证]` 异常为一等对象，抛出并回溯展开栈帧。 | `[语言规范保证]` `sys.exit(int/str)` 抛出 `SystemExit` 异常，若未捕获则解释器退出并设置退出码；未捕获普通异常退出码为 1。 | 不可将 C 常见负数返回值当成 Python 正常状态；必须明确区分业务状态与真实失败。 | [PY-REF-DATA §3.2 Exceptions](https://docs.python.org/3.12/reference/datamodel.html) |
| **Go**<br>(Go 1.27) | `[语言规范保证]` **显式多返回值 `(result, error)`**；`error` 为内置接口类型；严重致命故障使用 `panic`。 | `[语言规范保证]` `panic` 展开当前 Goroutine 栈，执行已注册的 `defer` 链；在 `defer` 中通过 `recover()` 截断崩溃。 | `[语言规范保证]` `os.Exit(int)` 立即终止进程（**不执行任何 `defer`！**）；`main` 正常返回退出码为 0。 | **严禁将常规 error 机械写为 panic**；切忌用 `os.Exit` 代替错误返回，否则资源泄漏。 | [GO-SPEC #Errors, #Handling_panics](https://go.dev/ref/spec) |
| **PowerShell**<br>(PowerShell 7.6) | `[语言规范保证]` 严格区分**终止错误**（Terminating Error，中断控制流）与**非终止错误**（Non-terminating Error，写入错误流继续运行）。 | `[指定运行时的实现相关事实]` `try`/`catch` **默认只能捕获终止错误**；受 `$ErrorActionPreference` 偏好变量严格控制。 | `[指定运行时的实现相关事实]` `$LASTEXITCODE` 记录外部进程最后返回码；Cmdlet 自身成败由 `$?`（`$true`/`$false`）记录；`exit` 终止宿主。 | 不可将 PS Cmdlet 写入的错误流直接等同于进程标准错误输出；`$?` 会被后续任意语句覆盖。 | [MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)<br>[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables) |
| **Ruby**<br>(CRuby 3.4) | `[语言规范保证]` `raise`/`rescue`/`ensure`/`else` 异常结构；异常派生自 `Exception`，常规异常派生自 `StandardError`。 | `[语言规范保证]` 栈回溯与异常对象实例化。 | `[语言规范保证]` `exit(int)` 抛出 `SystemExit` 异常；`exit!` 绕过 `ensure` 立即底层退出。 | `rescue => e` 默认只捕获 `StandardError`，不捕获 `Exception`（如 `NoMemoryError`、`SignalException`）。 | [RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html) |

---

## 六、内存、资源所有权、析构、GC 与终结

| 语言与冻结基线 | 内存管理模型 | 资源确定性释放机制 | 垃圾收集（GC）停顿与机制 | 悬垂与泄漏防范 | 官方资料依据 |
|---|---|---|---|---|---|
| **C**<br>(ISO C11) | `[语言规范保证]` 手动显式管理（`malloc`/`calloc`/`realloc`/`free`）；无析构函数；无垃圾收集。 | `[语言规范保证]` **无语言级确定性作用域释放**；必须在每个函数出口、`goto cleanup` 或提前返回时手工释放。 | `[语言规范保证]` 无 GC。 | `free` 后指针成为野指针（Dangling Pointer）；重复释放（Double Free）属于未定义行为（UB）。 | [WG14-N1570 §7.22.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) |
| **C++**<br>(ISO C++17) | `[语言规范保证]` RAII（Resource Acquisition Is Initialization）：对象生命周期与作用域严格绑定；智能指针（`unique_ptr`, `shared_ptr`）。 | `[语言规范保证]` **确定性析构（Deterministic Destruction）**：离开作用域逆序调用析构函数，保证异常安全。 | `[语言规范保证]` 无原生内置 GC。 | `std::string_view` 或引用引向已析构临时对象会导致严重悬挂引用。 | [WG21-N4659 Clause 6.7, Clause 15.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf) |
| **C#**<br>(C# 12 / .NET 8) | `[指定运行时的实现相关事实]` CoreCLR 自动分代垃圾回收（Generation 0, 1, 2）；非托管资源由平台安全句柄或包装类管理。 | `[指定运行时的实现相关事实]` `using` 语句 / `using var` 声明调用 `IDisposable.Dispose()`；终结器（Finalizer）执行时机非确定。 | `[指定运行时的实现相关事实]` 基于代际标记压缩的分代垃圾回收；非内存资源必须由 `IDisposable.Dispose` 或 `using` 显式保障释放。 | 事件未注销（`+=` 未 `-=`）会导致订阅者被强引用而长久内存泄漏。 | [MS-CS-GC](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals) |
| **Python**<br>(CPython 3.12) | `[指定运行时的实现相关事实]` CPython 采用**引用计数（Reference Counting）即时回收**为主，分代循环垃圾收集器（Cyclic GC）为辅。 | `[语言规范保证]` 上下文管理器 `with` 语句确保退出时触发 `__exit__()` 释放非内存资源；`__del__` 时机不可靠。 | `[指定运行时的实现相关事实]` 循环垃圾检测器分为 3 代，定期遍历检测孤立循环引用；无法保证跨实现确定性析构。 | 循环引用在仅靠引用计数时无法立即回收，依赖 Cyclic GC 扫描；非内存资源严禁依赖 `__del__`。 | [CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/)<br>[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html) |
| **Go**<br>(Go 1.27) | `[语言规范保证]` 自动内存管理；编译器逃逸分析；运行时垃圾收集器回收无引用堆对象。 | `[语言规范保证]` `defer` 语句将资源清理延迟到**外层函数返回前按 LIFO 逆序确定性执行**；无作用域级自动析构。 | `[指定运行时的实现相关事实]` 并发三色标记清除垃圾回收（依据 `GO-RT-DOC`）；非内存资源通过显式 `Close` 配合 `defer` 逆序释放。 | 在长循环内部直接使用 `defer` 会导致资源直到整函数退出才释放，极易耗尽句柄。 | [GO-SPEC #Defer_statements](https://go.dev/ref/spec)<br>[GO-RT-DOC](https://go.dev/doc/gc-guide) |
| **PowerShell**<br>(PowerShell 7.6) | `[指定运行时的实现相关事实]` 底层依赖 .NET CLR GC；处理大量管道对象时在进程内存中产生托管堆压力。 | `[指定运行时的实现相关事实]` 显式调用 `.Dispose()`，COM 对象必须调用 `[System.Runtime.InteropServices.Marshal]::ReleaseComObject()`。 | `[指定运行时的实现相关事实]` 随宿主 .NET 运行时触发 GC。 | 未释放的 COM 互操作对象将导致宿主子进程句柄泄露、阻碍外部进程终止。 | [MS-PS-COM](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/new-object) |
| **Ruby**<br>(CRuby 3.4) | `[指定运行时的实现相关事实]` MRI 内存管理；自动垃圾回收（RGenGC）；非托管资源需手动绑定。 | `[语言规范保证]` 代码块闭包确保资源释放模式（如 `File.open(...) do |f| ... end` 保证自动关闭）。 | `[指定运行时的实现相关事实]` 分代三色 RGenGC；GC 扫描期间受运行时机制支配。 | 遗漏 block 形式直接调用裸 `File.open` 会导致文件描述符泄漏直至下一次 GC。 | [RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html) |

---

## 七、异步、并发、取消与阻塞

| 语言与冻结基线 | 语言内建并发原语 | 线程/调度实体映射关系 | 级联取消与超时机制 | 内存模型与数据竞争 | 官方资料依据 |
|---|---|---|---|---|---|
| **C**<br>(ISO C11) | `[语言规范保证]` C11 `<threads.h>`（可选支持，多平台缺失）；C11 `<stdatomic.h>` 提供语言级原子操作与内存序。 | `[语言规范保证]` 语言规范抽象执行线程；底层 OS 线程映射属于平台实现，规范不作映射保证。 | `[语言规范保证]` 无语言内建取消；依赖显式全局标志位、原子变量或条件变量广播唤醒。 | `[语言规范保证]` C11 `<stdatomic.h>` 提供严格内存序（Acquire/Release/SeqCst）；无保护共享写属 UB。 | [WG14-N1570 §7.17, §7.26](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) |
| **C++**<br>(ISO C++17) | `[语言规范保证]` `std::thread`, `std::mutex`, `std::condition_variable`, `std::async`/`std::future`；无协程（C++20）。 | `[语言规范保证]` 标准定义程序内执行线程；底层 OS 线程调度属于平台实现，规范不作 1:1 映射保证。 | `[语言规范保证]` `std::future` 超时等待（`wait_for`）；无统一取消 Token（`std::stop_token` 为 C++20）。 | `[语言规范保证]` 严格 C++11/C++17 内存模型；数据竞争（Data Race）属于未定义行为（UB）。 | [WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf) |
| **C#**<br>(C# 12 / .NET 8) | `[语言规范保证]` 基于 Task 的异步模式（TAP：`async`/`await`）；`Task`/`Task<TResult>` 异步状态机。 | `[指定运行时的实现相关事实]` CLR 线程池调度托管任务与 OS 线程映射，受工作窃取算法管理。 | `[指定运行时的实现相关事实]` 统一的 `CancellationToken` / `CancellationTokenSource` 级联协作取消模型。 | `[指定运行时的实现相关事实]` 共享可变状态多线程访问需 `lock` (`Monitor`) 或原子操作同步，否则发生数据竞争。 | [MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)<br>[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads) |
| **Python**<br>(CPython 3.12) | `[语言规范保证]` `threading`；`multiprocessing`；`asyncio`（单线程事件循环协程）。 | `[指定运行时的实现相关事实]` CPython 全局解释器锁（GIL）确保同一时刻仅一个线程执行字节码；多线程无法利用多核进行 CPU 密集计算。 | `[语言规范保证]` `asyncio.Task.cancel()` 抛出 `CancelledError`；`asyncio.wait_for` 设定超时。 | `[指定运行时的实现相关事实]` 虽受 GIL 保护基础操作原子性，但复合状态操作仍存在竞态，必须使用 `threading.Lock`。 | [CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/)<br>[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html) |
| **Go**<br>(Go 1.27) | `[语言规范保证]` 原生 Goroutine（轻量并发任务）；Channel（信道通信）；`select` 多路复用。 | `[指定运行时的实现相关事实]` M:N 运行时调度器（G: Goroutine, M: OS 线程, P: 逻辑处理器），由运行时根据协作与系统调用动态调度。 | `[指定运行时的实现相关事实]` `context.Context`（`WithCancel`, `WithTimeout`）通过 `ctx.Done()` 信道级联传递取消。 | `[语言规范保证]` Go 数据竞争是错误，必须通过 channel、sync 或 sync/atomic 等同步机制避免。Go 内存模型对含数据竞争程序仍规定有限的实现约束：实现可以报告该竞争并终止程序；无竞争程序才获得顺序一致性保证。不得将 Go 的数据竞争机械描述为 C/C++ 式完全未定义行为。 | [GO-SPEC #Go_statements](https://go.dev/ref/spec)<br>[GO-RT-DOC](https://go.dev/doc/gc-guide)<br>[GO-MEM](https://go.dev/ref/mem)<br>[GO-PKG-CONTEXT](https://pkg.go.dev/context) |
| **PowerShell**<br>(PowerShell 7.6) | `[语言规范保证]` `Start-Job`（后台进程）；`Start-ThreadJob` / `ForEach-Object -Parallel`（多 Runspace 线程池）。 | `[指定运行时的实现相关事实]` Runspace 池映射至 .NET 线程池线程；脚本块隔离执行。 | `[指定运行时的实现相关事实]` 支持作业超时与取消命令；受宿主环境与具体命令控制。 | `[指定运行时的实现相关事实]` 共享变量访问需使用同步包装或显式 .NET 同步锁，否则竞态数据损毁。 | [MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)<br>[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs) |
| **Ruby**<br>(CRuby 3.4) | `[语言规范保证]` `Thread`；`Fiber`（轻量协作式协程）。 | `[指定运行时的实现相关事实]` MRI 全局 VM 锁（GVL）限制多线程同一时刻仅有一个在 CPU 上执行 Ruby 字节码。 | `[语言规范保证]` 线程超时控制（`Timeout.timeout`）；Fiber 协作式让出控制权。 | `[指定运行时的实现相关事实]` 跨线程共享可变对象需互斥锁（`Mutex`）保护。 | [RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)<br>[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html) |

---

## 八、文件与网络调用的语言层边界（何时加载 B 类规则）

> [!IMPORTANT]
> **A 类与 B 类职责边界律**：
> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

1. **套接字与网络通信行为**：
   - *源码触发条件*：源码中出现系统网络套接字调用，或各高级语言等价网络库调用（如 Go `net.Dial`, Python `socket.socket`, C# `Socket` / `TcpClient`）。
   - *必须加载的既有 B 类规则*：
     - 通用网络场景：[`skills/scenes/network-io/SKILL.md`](../scenes/network-io/SKILL.md)
     - 涉及 Linux/POSIX 与 Windows 跨系统转换时：[`skills/systems/posix-winsock/SKILL.md`](../systems/posix-winsock/SKILL.md)
   - *语言层核心职责*：保持连接生命周期、错误返回时机、缓冲区所有权与同步/异步阻塞语义；具体 API 结构体填充与平台头文件全部由上述 B 类规则裁定。

2. **文件系统与路径操作行为**：
   - *源码触发条件*：源码中出现底层文件句柄操作、路径拼接分隔符与驱动器解析，或语言层文件读写（如 Go `os.Open`, Python `open()`, C# `FileStream`）。
   - *必须加载的既有 B 类规则*：
     - 通用文件场景：[`skills/scenes/file-io/SKILL.md`](../scenes/file-io/SKILL.md)
     - 涉及 Linux/POSIX 与 Windows 跨系统转换时：[`skills/systems/posix-windows-filesystem/SKILL.md`](../systems/posix-windows-filesystem/SKILL.md)
   - *语言层核心职责*：保证文件句柄在各分支及异常下确定性关闭；确保文本/二进制打开模式与平台换行符（CRLF vs LF）一致；具体路径规范化与目录遍历由 B 类规则裁定。

3. **原生系统线程与并发同步行为**：
   - *源码触发条件*：源码中直接调用底层操作系统原生线程创建、系统事件等待、信号量与进程级同步原语。
   - *必须加载的既有 B 类规则*：
     - 通用并发场景：[`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)
     - 涉及 Linux 与 Windows 跨系统转换时：[`skills/systems/posix-windows-threads/SKILL.md`](../systems/posix-windows-threads/SKILL.md)
   - *语言层核心职责*：管理线程生命周期与同步所有权契约，具体 OS 调度与同步原语映射由 B 类规则裁定。
