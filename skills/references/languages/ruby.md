# Ruby 语言共性语义（CRuby 3.4）

> **用途**：供以 Ruby 为源语言或目标语言的方向 Skill 按需读取；本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 纯面向对象模型；一切变量皆持有对象的引用；可变对象原地修改（如 `String#<<`、`Array#push`），不可变对象包含 `Integer`、`Float`、`Symbol`、`true`、`false`、`nil`。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` 立即数（Immediate values：Fixnum、Symbol 等）在 MRI 中直接编码在指针位中，无独立堆分配，属于实现优化。
- **机械等价禁区与转换约束**：严禁忽视 Ruby 原地方法（带 `!` 或 `<<`）对全部别名持有者的同步副作用。
- **官方资料依据**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` `Integer` 统一表示（具备任意精度整数语义）。
- **有符号溢出行为**：`[语言规范保证]` **无溢出概念**；超出机器字长时自动无缝升级为大数表示。
- **无符号溢出行为**：`[语言规范保证]` 无原生无符号整数；按位操作将负数视为无限补码展开。
- **隐式提升与转换陷阱**：`[语言规范保证]` 位操作中未显式截断可能导致带符号大数，需显式使用 `& ((1 << N) - 1)` 保持位宽。
- **官方资料依据**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `String`：可变字节序列，**显式附带 `Encoding` 元数据标签**（默认 UTF-8）。
- **字节序列数据结构**：`[语言规范保证]` 同样为 `String`，其编码标记为 `Encoding::BINARY` (`ASCII-8BIT`)。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` 显式记录长度，允许包含 `\0` 字节；底层 C 扩展遇到 `\0` 可能抛出 `ArgumentError`。
- **编码假设与转换陷阱**：`[语言规范保证]` 两个不同 Encoding 的 String 进行拼接时，若无法无损转码将抛出 `Encoding::CompatibilityError`。
- **官方资料依据**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` `Array` 为内建可变序列容器，支持负数下标索引。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `Hash` 为内建键值映射容器。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` **语言规范保证保持键的插入顺序**。
- **迭代期间修改（Fail-Fast）**：`[语言规范保证]` 迭代中修改散列表键值可能导致遗漏或抛出异常。
- **官方资料依据**：[RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)<br>[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` `raise`/`rescue`/`ensure`/`else` 异常结构；异常派生自 `Exception`，常规异常派生自 `StandardError`。
- **异常展开与性能模型**：`[语言规范保证]` 栈回溯与异常对象实例化。
- **进程退出码回传机制**：`[语言规范保证]` `exit(int)` 抛出 `SystemExit` 异常；`exit!` 绕过 `ensure` 立即底层退出。
- **跨语言映射关键风险**：`rescue => e` 默认只捕获 `StandardError`，不捕获 `Exception`（如 `NoMemoryError`、`SignalException`）。
- **官方资料依据**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[指定运行时的实现相关事实]` MRI 内存管理；自动垃圾回收（RGenGC）；非托管资源需手动绑定。
- **资源确定性释放机制**：`[语言规范保证]` 代码块闭包确保资源释放模式（如 `File.open(...) do |f| ... end` 保证自动关闭）。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 分代三色 RGenGC；GC 扫描期间受运行时机制支配。
- **悬垂与泄漏防范**：遗漏 block 形式直接调用裸 `File.open` 会导致文件描述符泄漏直至下一次 GC。
- **官方资料依据**：[RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` `Thread`；`Fiber`（轻量协作式协程）。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` MRI 全局 VM 锁（GVL）限制多线程同一时刻仅有一个在 CPU 上执行 Ruby 字节码。
- **级联取消与超时机制**：`[语言规范保证]` 线程超时控制（`Timeout.timeout`）；Fiber 协作式让出控制权。
- **内存模型与数据竞争**：`[指定运行时的实现相关事实]` 跨线程共享可变对象需互斥锁（`Mutex`）保护。
- **官方资料依据**：[RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)<br>[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)

## 使用边界

将本页与所选的源→目标方向 Skill 及另一语言的共性页组合使用；映射前先确认源码真实行为。文件、网络、并发和跨 OS API 的具体差异仍按[共性索引的场景/系统分流](../seven-language-common-semantics.md)选读，不从语言事实直接推断系统 API 等价。没有逐例第三方证据时，语法/构建与功能结论保持 `UNVERIFIED`；本机不运行或编译样本。
