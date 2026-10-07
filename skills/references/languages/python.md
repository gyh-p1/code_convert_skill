# Python 语言共性语义（CPython 3.12）

> **用途**：供以 Python 为源语言或目标语言的方向 Skill 按需读取；本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 一切变量皆为对象引用；赋值仅绑定名字与对象，传参为“对象引用按值传递”；对象分为不可变（`int`、`float`、`str`、`tuple`、`frozenset`、`bytes`）与可变（`list`、`dict`、`set`、`bytearray`）。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` CPython 采用小整数与短字符串驻留（Interning），属于解释器优化细节，非跨实现语言保证；具体内存由解释器内存池管理。
- **机械等价禁区与转换约束**：严禁将可变容器（如 `list`）的直接赋值当作独立拷贝（修改会产生隐式别名污染）；**不得把 Python 的假值集合（`None`、`False`、`0`、`""`、`[]`、`{}`）与其他语言的判空互相当作等价**（见下条）。
- **官方资料依据**：[PY-REF-DATA §3.1](https://docs.python.org/3.12/reference/datamodel.html)

### L1-PY-01 假值集合不等于判空
1. **源码触发条件**：源码用 `if x:` / `if not x` / `if x is None` / `if len(x) == 0` 分流，或对可能为 `None` 的值直接下标、调用方法。
2. **冻结版本/运行时/API 前提**：CPython 3.12；真值测试与 `__bool__`/`__len__` 语义见 [PY-REF-DATA §3.3](https://docs.python.org/3.12/reference/datamodel.html#object.__bool__)。
3. **原可观察行为**：
   - `if x:` 在 `x` 为 `None`、`False`、数值 `0`、`""`、`b""`、`[]`、`{}`、`set()` 时**均为假**；自定义类的实例默认恒为真，除非定义 `__bool__`/`__len__`。
   - `x is None` 与 `not x` **不等价**：`""` 与 `0` 使 `not x` 为真但不是 `None`。
   - `x is None` 与 `x == None` 在自定义 `__eq__` 下也可能不同；用 `is` 才是身份判定。
4. **目标可选写法和不适用条件**：
   - *Python 作为源*：把源判的是“哪种空”显式映射到目标的对应检查。源写 `if not x:` 时**必须先判断源作者意图**是“无值”还是“空容器/空串/零值”，不可默认只映射成 null 检查。
   - *Python 作为目标*：源为静态类型语言时，源的空指针/零值判断必须分别映射为 `is None` 与 `== 0`/`len(x) == 0`；**不得**用 `if x:` 简化，那会把 `0`/`""` 一并并入假分支而改变控制流。
   - *不适用条件*：源确实按“非空/非零”统一判定（如“有内容才继续”）时，`if x:` 是等价映射，不必拆分。
5. **错误机械替换反例**：
   ```python
   # 错误：把 C 的指针判空写成 Python 真值判断，空串/0 被误并入守卫分支
   if not cmdline:                # C 源是 !ptr（指针判空）；这里 "" 也会进分支
       return -1
   # 错误之二：假定 None 与缺键是一回事
   v = d["k"]                     # 缺键抛 KeyError，与 None 分支行为不同
   # 正确：按源的判定对象分别表达
   if cmdline is None:
       return -1
   if len(cmdline) == 0:          # 源的“内容为空”是独立分支
       handle_empty()
   v = d.get("k")                 # 仅在源确实按“缺键给默认值”时
   ```
6. **信息不足或实现相关时的处理**：无法确定源的判断表达“无值”还是“空值”时，标为“假值与判空语义待确认”，不得用统一真值判断合并两类。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA §3.3 Truth Value Testing](https://docs.python.org/3.12/reference/datamodel.html#object.__bool__)；[PY-REF-EXPRESSIONS §6.11](https://docs.python.org/3.12/reference/expressions.html#boolean-operations)。

### L1-PY-05 程序实参含程序名，`argparse` 缩写与绑定必须显式重建

1. **源码触发条件**：源码从 `sys.argv` 取用实参、用 `argparse`/`optparse`/`getopt` 解析，或在 `parse_args()` 后读取位置参数。
2. **冻结版本/运行时/API 前提**：CPython 3.12（[`sys.argv`](https://docs.python.org/3.12/library/sys.html#sys.argv)、[`argparse`](https://docs.python.org/3.12/library/argparse.html)）。
3. **原可观察行为**：
   - **`sys.argv[0]` 是脚本名**，用户实参从 **`sys.argv[1:]`** 开始（与 C# `args`、Ruby `ARGV` **不含**程序名不同）。
   - `argparse` 默认允许**长选项唯一前缀缩写**（`--dep` 可匹配 `--depth`）；`allow_abbrev=False` 才关闭。前缀**有歧义**时报错并以**状态码 2** 退出。
   - `argparse` 对位置参数按**声明顺序**绑定；缺必需参数时输出用法到 **stderr** 并**以状态码 2 退出**（不是抛未被捕获的异常）。
   - `argparse` 默认会把 `-` 前缀的未知参数当错误处理；是否支持选项与操作数**交错**取决于实现（`argparse` 支持部分交错，与 `flag` 相反）。
4. **目标可选写法和不适用条件**：
   - *Python 作为源*：目标语言实参序列不含程序名时须去 `sys.argv[0]`；含程序名时（C/C++/Go）须保留偏移。
   - *Python 作为目标*：源的"未知选项先输出诊断再返回错误码"须保留为**状态码 2 + stderr 用法行**，不得改成抛出未捕获异常导致退出码变成 1。
   - *不适用条件*：源码不使用命令行实参时不适用；源码显式设 `allow_abbrev=False` 时，**禁止缩写**才是要保留的行为。
5. **错误机械替换反例**：
   ```python
   # 错误一：把 Ruby ARGV（不含程序名）的习惯套到 sys.argv
   path = sys.argv[0]                # 取到的是脚本名
   # 错误二：把 argparse 的退出码 2 改成未捕获异常的退出码 1
   if len(sys.argv) < 2: raise SystemExit(1)   # 源是 argparse 的 2 + stderr 用法
   # 正确
   args = parser.parse_args()        # 保留 2 + stderr 用法行
   path = sys.argv[1]
   ```
6. **信息不足或实现相关时的处理**：无法确定源是否依赖唯一前缀缩写、或目标语言实参序列是否含程序名时，标为“实参偏移与解析器语义待确认”。
7. **直接官方 HTTPS 依据链接**：[`sys.argv`](https://docs.python.org/3.12/library/sys.html#sys.argv)；[`argparse`（`allow_abbrev`、退出码 2）](https://docs.python.org/3.12/library/argparse.html)；[`argparse` 退出状态](https://docs.python.org/3.12/library/argparse.html#exiting-methods)。

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` `int` 为**任意精度整数**（Arbitrary-precision integer），理论上仅受可用内存限制；无固定定宽整数。
- **有符号溢出行为**：`[语言规范保证]` **无溢出概念**；数值超出 64 位自动扩展内存表示。
- **无符号溢出行为**：`[语言规范保证]` **无溢出概念**；不支持无符号数原生类型。
- **隐式提升与转换陷阱**：`[语言规范保证]` 无法原生模拟定宽溢出截断；若需定宽溢出行为，必须显式施加位掩码（`& 0xFFFFFFFF`）。
- **官方资料依据**：[PY-REF-DATA §3.2 Numbers](https://docs.python.org/3.12/reference/datamodel.html)

### L1-PY-02 数值切片与格式化不得静默改变长度或有效位数
1. **源码触发条件**：源码用切片承载长度契约（`buf[:n]`）、把数值转文本（`str(x)`、`f"{x}"`、`format(x, spec)`），或依赖定宽整数的溢出/截断。
2. **冻结版本/运行时/API 前提**：CPython 3.12；`int` 为任意精度、切片**超出长度不报错而是截断**，见 [PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)、[PY-REF-SEQUENCE](https://docs.python.org/3.12/library/stdtypes.html#common-sequence-operations)。
3. **原可观察行为**：
   - `int` **无溢出**：超出机器字长自动扩展，不会按模回绕。
   - `seq[:n]` 在 `n` 大于实际长度时**静默返回较短的结果**（不抛异常），因此用它表达“恰好 n 个字节”的源契约会失真。
   - `str(float)` 使用最短往返表示；`repr(float)` 与 `str(float)` 在 Python 3 中一致，但 `format(f, ".6f")` 等固定精度格式**位数不同**。
   - 格式化与区域设置**无关**（除非显式使用 `locale` 模块）。
4. **目标可选写法和不适用条件**：
   - *Python 作为源*：源按字节数写出的路径必须映射为目标的定长写入或显式长度校验，不得靠目标语言的“超长静默截断”承接。
   - *Python 作为目标*：源若依赖定宽溢出回绕，必须显式施加位掩码；源若依赖固定有效位数，目标必须写出相同精度，不得用默认 `str()`。
   - *不适用条件*：源本身只做无限精度算术且无定宽契约时，不涉及掩码；但**格式化位数**仍需核对。
5. **错误机械替换反例**：
   ```python
   # 错误：用切片冒充源“恰好写 n 字节”的契约
   f.write(user.buf[:user.len])    # C 源 write(f, buf, len) 恰好写 len 字节；
                                   # Python 侧若 buf 更短则静默少写，长度已变
   # 错误之二：用默认 str 冒充源的定宽/定精度格式
   out = str(value)                # 位数可能与源不同
   # 正确：长度与精度都显式校验
   if len(user.buf) < user.len:
       raise ValueError("source wrote exactly user->len bytes")
   f.write(user.buf[:user.len])
   out = format(value, ".17g")     # 精度按源义务冻结
   ```
6. **信息不足或实现相关时的处理**：无法确定源的长度契约与有效位数时，标为“长度与数值格式待确认”；不得用 `str()` 的默认输出或切片的静默截断充当依据。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)；[通用序列操作（切片语义）](https://docs.python.org/3.12/library/stdtypes.html#common-sequence-operations)。

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `str`：不可变 Unicode 码点序列。
- **字节序列数据结构**：`[语言规范保证]` `bytes`：不可变 8 位字节序列；`bytearray`：可变字节序列。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` `str` 与 `bytes` 均显式记录长度，内容可自由包含 `\0`。
- **编码假设与转换陷阱**：`[语言规范保证]` **`str` 与 `bytes` 严格隔离**；严禁隐式转换，必须显式通过 `.encode('utf-8')` 与 `.decode('utf-8')` 互转。
- **官方资料依据**：[PY-REF-DATA §3.2 Strings, Bytes](https://docs.python.org/3.12/reference/datamodel.html)

### L1-PY-03 字节路径不得经文本层，且不得用替换策略掩盖编码差异
1. **源码触发条件**：源码读写二进制（`open(path, 'rb'/'wb')`、`socket.recv`、`hashlib`、`base64`、`zlib`、结构体打包），或在文本与字节之间用 `.encode`/`.decode` 转换。
2. **冻结版本/运行时/API 前提**：CPython 3.12；`decode` 的 `errors` 参数与 `open` 的 `newline`/`encoding` 语义见 [PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)、[`bytes.decode`](https://docs.python.org/3.12/library/stdtypes.html#bytes.decode)、[`open`](https://docs.python.org/3.12/library/functions.html#open)。
3. **原可观察行为**：
   - `str`/`bytes` **严格隔离**：`b"a" + "b"` 抛 `TypeError`，不存在隐式编解码。
   - `bytes.decode('utf-8')` 对非法序列**默认抛 `UnicodeDecodeError`**；`errors="replace"`/`"ignore"` 则**静默改变内容与长度**。
   - 文本模式 `open(path, 'r')` 默认 `encoding=None`（取 `locale.getpreferredencoding(False)`），且**默认启用通用换行翻译**（`newline=None` 把 CRLF/LF/CR 统一为 `\n`）；`'rb'` 无此翻译。
   - `len(str)` 是码点数，`len(bytes)` 是字节数；非 ASCII 时两者不等。
4. **目标可选写法和不适用条件**：
   - *Python 作为源*：字节路径映射到目标的字节类型；文本路径须显式声明 `encoding` 与 `newline`，**不得**依赖平台默认编码或默认换行翻译。
   - *Python 作为目标*：源若以字节为单位读写，必须走 `'rb'`/`'wb'` 与 `bytes`，**不得**经 `str` 往返；源若以文本为单位，须显式写出编码与换行策略，并保留源对非法字节的处理方式（抛错或替换）。
   - *不适用条件*：源本身是文本 API 且换行翻译属源的可观察行为时，通用换行是要**保留**的行为，须显式冻结而非消除。
5. **错误机械替换反例**：
   ```python
   # 错误：二进制内容走了文本模式，字节被改写
   content = open(path).read()                 # 平台默认编码 + 换行翻译
   hexdigest = hashlib.sha256(content.encode()).hexdigest()   # 与源不一致
   # 错误之二：用 replace 掩盖非法字节
   text = blob.decode('utf-8', errors='replace')   # 内容与长度都被改写
   # 正确：字节进字节出；文本路径显式冻结编码与错误策略
   content = open(path, 'rb').read()
   hexdigest = hashlib.sha256(content).hexdigest()
   text = blob.decode('utf-8')                 # 非法序列按源语义抛 UnicodeDecodeError
   ```
6. **信息不足或实现相关时的处理**：无法确认源数据的编码、换行策略或非法字节处置时，标为“编码与字节长度语义待确认”；**禁止**用 `errors='replace'`/`'ignore'` 或 `scrub` 掩盖差异。也不得用 `len(str)` 承接源按字节计的长度。
7. **直接官方 HTTPS 依据链接**：[`bytes.decode`（错误处理策略）](https://docs.python.org/3.12/library/stdtypes.html#bytes.decode)；[`open`（encoding/newline）](https://docs.python.org/3.12/library/functions.html#open)；[Python Unicode HOWTO](https://docs.python.org/3.12/howto/unicode.html)。

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

### L1-PY-04 被丢弃的错误不得变成异常终止，主动失败不得被静默吞掉
1. **源码触发条件**：源码**有意丢弃**可失败操作的结果（未检查返回值、空 `except: pass`、未检查函数返回的 `None`），**或**在失败时 `raise`、`sys.exit(非零)`、返回非零状态。
2. **冻结版本/运行时/API 前提**：CPython 3.12；未捕获异常退出码为 1、`SystemExit` 携带指定码，见 [PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)、[`sys.exit`](https://docs.python.org/3.12/library/sys.html#sys.exit)。
3. **原可观察行为**：
   - 忽略错误的路径：Python 不会自动终止，但**多数内置操作以异常而非错误码报告失败**（如 `open` 抛 `FileNotFoundError`）。因此“源丢弃错误”在 Python 里通常表现为**显式 `try/except` 后继续**，而非“不检查返回值”。
   - 主动失败的路径：未捕获异常 → 解释器以退出码 **1** 结束（不是源可能指定的其他码）；`sys.exit(n)` → 退出码 `n`。
   - 空 `except:` 会捕获 `KeyboardInterrupt`/`SystemExit`（它们派生自 `BaseException`），比 `except Exception:` 危险性更高。
4. **目标可选写法和不适用条件**（两个方向都必须覆盖）：
   - *源丢弃错误 → 目标不得变成异常终止*：仅当源**确实**忽略该失败时才把异常转为非致命路径（`try/except` 后继续），并保留后续空结果路径与最终退出码。
   - *源主动失败 → 目标不得静默继续*：不得用 `except Exception: pass` 把失败吞成成功；也不得把源指定的非零退出码替换成 0。
   - *不适用条件*：源**确实检查并传播**失败时，必须保留失败分支，不能套用“忽略并继续”。
5. **错误机械替换反例**：
   ```python
   # 错误：源忽略打开失败并继续，目标让异常逃逸终止进程
   f = open(path, 'rb')                 # FileNotFoundError 未处理 → 提前终止
   # 错误之二：把源主动失败的路径吞掉（且空 except 还会吞 KeyboardInterrupt）
   try:
       run()
   except:                              # 静默继续，退出码变成 0
       pass
   # 正确：按源的实际检查行为分别重建
   try:
       f = open(path, 'rb')
   except OSError:                      # 仅当源确实忽略该失败时
       f = None
   if f is None:
       write_empty_result()             # 源的“空结果继续”路径
   ```
6. **信息不足或实现相关时的处理**：无法确认源是否检查、是否输出诊断、失败后是否继续时，把该错误路径单列为待验证 oracle；不得以“异常更安全”为由改变控制流。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)；[`sys.exit`](https://docs.python.org/3.12/library/sys.html#sys.exit)；[内置异常层次](https://docs.python.org/3.12/library/exceptions.html#exception-hierarchy)。

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
