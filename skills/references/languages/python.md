# Python 语言共性语义（CPython 3.12）

> **用途**：供以 Python 为源语言或目标语言的方向 Skill 按需读取；本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 一切变量皆为对象引用；赋值仅绑定名字与对象，传参为“对象引用按值传递”；对象分为不可变（`int`、`float`、`str`、`tuple`、`frozenset`、`bytes`）与可变（`list`、`dict`、`set`、`bytearray`）。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` CPython 采用小整数与短字符串驻留（Interning），属于解释器优化细节，非跨实现语言保证；具体内存由解释器内存池管理。
- **机械等价禁区与转换约束**：严禁将可变容器（如 `list`）的直接赋值当作独立拷贝（修改会产生隐式别名污染）。
- **官方资料依据**：[PY-REF-DATA §3.1](https://docs.python.org/3.12/reference/datamodel.html)

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` `int` 为**任意精度整数**（Arbitrary-precision integer），理论上仅受可用内存限制；无固定定宽整数。
- **有符号溢出行为**：`[语言规范保证]` **无溢出概念**；数值超出 64 位自动扩展内存表示。
- **无符号溢出行为**：`[语言规范保证]` **无溢出概念**；不支持无符号数原生类型。
- **隐式提升与转换陷阱**：`[语言规范保证]` 无法原生模拟定宽溢出截断；若需定宽溢出行为，必须显式施加位掩码（`& 0xFFFFFFFF`）。
- **官方资料依据**：[PY-REF-DATA §3.2 Numbers](https://docs.python.org/3.12/reference/datamodel.html)

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `str`：不可变 Unicode 码点序列。
- **字节序列数据结构**：`[语言规范保证]` `bytes`：不可变 8 位字节序列；`bytearray`：可变字节序列。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` `str` 与 `bytes` 均显式记录长度，内容可自由包含 `\0`。
- **编码假设与转换陷阱**：`[语言规范保证]` **`str` 与 `bytes` 严格隔离**；严禁隐式转换，必须显式通过 `.encode('utf-8')` 与 `.decode('utf-8')` 互转。
- **官方资料依据**：[PY-REF-DATA §3.2 Strings, Bytes](https://docs.python.org/3.12/reference/datamodel.html)

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` `list`：动态可变序列；`tuple`：固定长度不可变序列。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `dict`：键值映射类型。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` **语言规范保证保持键值对的插入顺序**（Insertion-order preservation）。
- **迭代期间修改（Fail-Fast）**：`[语言规范保证]` 迭代中改变 `dict` 大小立即抛出 `RuntimeError: dictionary changed size during iteration`。
- **官方资料依据**：[PY-REF-DATA §3.2 Dictionaries](https://docs.python.org/3.12/reference/datamodel.html)

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` 异常驱动控制流（EAFP：Easier to Ask for Forgiveness than Permission）；`try`/`except`/`finally`/`else`。
- **异常展开与性能模型**：`[语言规范保证]` 异常为一等对象，抛出并回溯展开栈帧。
- **进程退出码回传机制**：`[语言规范保证]` `sys.exit(int/str)` 抛出 `SystemExit` 异常，若未捕获则解释器退出并设置退出码；未捕获普通异常退出码为 1。
- **跨语言映射关键风险**：不可将 C 常见负数返回值当成 Python 正常状态；必须明确区分业务状态与真实失败。
- **官方资料依据**：[PY-REF-DATA §3.2 Exceptions](https://docs.python.org/3.12/reference/datamodel.html)

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[指定运行时的实现相关事实]` CPython 采用**引用计数（Reference Counting）即时回收**为主，分代循环垃圾收集器（Cyclic GC）为辅。
- **资源确定性释放机制**：`[语言规范保证]` 上下文管理器 `with` 语句确保退出时触发 `__exit__()` 释放非内存资源；`__del__` 时机不可靠。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 循环垃圾检测器分为 3 代，定期遍历检测孤立循环引用；无法保证跨实现确定性析构。
- **悬垂与泄漏防范**：循环引用在仅靠引用计数时无法立即回收，依赖 Cyclic GC 扫描；非内存资源严禁依赖 `__del__`。
- **官方资料依据**：[CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/)<br>[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` `threading`；`multiprocessing`；`asyncio`（单线程事件循环协程）。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` CPython 全局解释器锁（GIL）确保同一时刻仅一个线程执行字节码；多线程无法利用多核进行 CPU 密集计算。
- **级联取消与超时机制**：`[语言规范保证]` `asyncio.Task.cancel()` 抛出 `CancelledError`；`asyncio.wait_for` 设定超时。
- **内存模型与数据竞争**：`[指定运行时的实现相关事实]` 虽受 GIL 保护基础操作原子性，但复合状态操作仍存在竞态，必须使用 `threading.Lock`。
- **官方资料依据**：[CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/)<br>[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)

## 使用边界

将本页与所选的源→目标方向 Skill 及另一语言的共性页组合使用；映射前先确认源码真实行为。文件、网络、并发和跨 OS API 的具体差异仍按[共性索引的场景/系统分流](../seven-language-common-semantics.md)选读，不从语言事实直接推断系统 API 等价。没有逐例第三方证据时，语法/构建与功能结论保持 `UNVERIFIED`；本机不运行或编译样本。
