# Python 语言共性语义（CPython 3.12）

> **用途**：以 Python 为源语言或目标语言的任务必读本页，按源码选择适用条目；加载与门禁先见根[转换入口](../../../SKILL.md)。本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：按条目中的语言版本、资料依据和源码触发条件选择适用事实；跨语言关注点见[七语言共性索引](../seven-language-common-semantics.md)。目标工具链能力与编译、行为结论须依据本项精确版本的独立证据。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 一切变量皆为对象引用；赋值仅绑定名字与对象，传参为“对象引用按值传递”；对象分为不可变（`int`、`float`、`str`、`tuple`、`frozenset`、`bytes`）与可变（`list`、`dict`、`set`、`bytearray`）。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` CPython 采用小整数与短字符串驻留（Interning），属于解释器优化细节，非跨实现语言保证；具体内存由解释器内存池管理。
- **机械等价禁区与转换约束**：严禁将可变容器（如 `list`）的直接赋值当作独立拷贝（修改会产生隐式别名污染）；**不得把 Python 的假值集合（`None`、`False`、`0`、`""`、`[]`、`{}`）与其他语言的判空互相当作等价**（见下条）。
- **官方资料依据**：PY-REF-DATA §3.1

### L1-PY-01 假值集合不等于判空
1. **源码触发条件**：源码用 `if x:` / `if not x` / `if x is None` / `if len(x) == 0` 分流，或对可能为 `None` 的值直接下标、调用方法。
2. **冻结版本/运行时/API 前提**：CPython 3.12；真值测试与 `__bool__`/`__len__` 语义见 PY-REF-DATA §3.3。
3. **原可观察行为**：
   - `if x:` 在 `x` 为 `None`、`False`、数值 `0`、`""`、`b""`、`[]`、`{}`、`set()` 时**均为假**；自定义类的实例默认恒为真，除非定义 `__bool__`/`__len__`。
   - `x is None` 与 `not x` **不等价**：`""` 与 `0` 使 `not x` 为真但不是 `None`。
   - `x is None` 与 `x == None` 在自定义 `__eq__` 下也可能不同；用 `is` 才是身份判定。
4. **目标可选写法和不适用条件**：
   - *Python 作为源*：按实际值域、__bool__/__len__ 与求值副作用保留 if not x 的真值行为，不能以推测的“作者意图”缩成 null 检查；必要类型/消费者未知时记录缺口。
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
7. **资料依据（名称/版本/章节）**：PY-REF-DATA §3.3 Truth Value Testing；PY-REF-EXPRESSIONS §6.11。

### L1-PY-05 程序实参含程序名，`argparse` 缩写与绑定必须显式重建

1. **源码触发条件**：源码从 `sys.argv` 取用实参、用 `argparse`/`optparse`/`getopt` 解析，或在 `parse_args()` 后读取位置参数。
2. **冻结版本/运行时/API 前提**：CPython 3.12（`sys.argv`、`argparse`）。
3. **原可观察行为**：
   - **`sys.argv[0]` 是脚本名**，用户实参从 **`sys.argv[1:]`** 开始（与 C# `args`、Ruby `ARGV` **不含**程序名不同）。
   - `argparse` 默认允许**长选项唯一前缀缩写**（`--dep` 可匹配 `--depth`）；`allow_abbrev=False` 才关闭。前缀**有歧义**时报错并以**状态码 2** 退出。
   - `argparse` 对位置参数按**声明顺序**绑定；缺必需参数时输出用法到 **stderr** 并**以状态码 2 退出**（不是抛未被捕获的异常）。
   - `argparse` 默认会把 `-` 前缀的未知参数当错误处理；是否支持选项与操作数**交错**取决于实现（`argparse` 支持部分交错，与 `flag` 相反）。
4. **目标可选写法和不适用条件**：
   - *Python 作为源*：目标语言实参序列不含程序名时须去 `sys.argv[0]`；含程序名时（C/C++/Go）须保留偏移。
   - *Python 作为目标*：按源解析器与应用实际行为保留诊断、通道及退出码。只有源契约确为状态码 2 + stderr 用法行时才对应该行为；getopt 返回 `'?'` 并不决定进程码，不能把任意源错误强行改成 argparse 的默认 2，也不把已知源出口改成未捕获异常。
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
7. **资料依据（名称/版本/章节）**：`sys.argv`；`argparse`（`allow_abbrev`、退出码 2）；`argparse` 退出状态。

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` `int` 为**任意精度整数**（Arbitrary-precision integer），理论上仅受可用内存限制；无固定定宽整数。
- **有符号溢出行为**：`[语言规范保证]` **无溢出概念**；数值超出 64 位自动扩展内存表示。
- **无符号溢出行为**：`[语言规范保证]` **无溢出概念**；不支持无符号数原生类型。
- **隐式提升与转换陷阱**：`[语言规范保证]` 无法原生模拟定宽溢出截断；若需定宽溢出行为，必须显式施加位掩码（`& 0xFFFFFFFF`）。
- **官方资料依据**：PY-REF-DATA §3.2 Numbers

### L1-PY-02 数值切片与格式化不得静默改变长度或有效位数
1. **源码触发条件**：源码用切片承载长度契约（`buf[:n]`）、把数值转文本（`str(x)`、`f"{x}"`、`format(x, spec)`），或依赖定宽整数的溢出/截断。
2. **冻结版本/运行时/API 前提**：CPython 3.12；`int` 为任意精度、切片**超出长度不报错而是截断**，见 PY-REF-DATA §3.2、PY-REF-SEQUENCE。
3. **原可观察行为**：
   - `int` **无溢出**：超出机器字长自动扩展，不会按模回绕。
   - `seq[:n]` 在 `n` 大于实际长度时**静默返回较短的结果**（不抛异常），因此用它表达“恰好 n 个字节”的源契约会失真。
   - `str(float)` 使用最短往返表示；`repr(float)` 与 `str(float)` 在 Python 3 中一致，但 `format(f, ".6f")` 等固定精度格式**位数不同**。
   - 数值格式的精度、类型码和区域设置分别核对；n 类型码会使用区域设置，不能概括所有 format 都与 locale 无关。
4. **目标可选写法和不适用条件**：
   - *Python 作为源*：保持实际切片裁剪、写入返回值及源重试/失败分支；源 buf[:n] 不因为 n 较大就自动变成长度错误。
   - *Python 作为目标*：源若依赖定宽溢出回绕，必须显式施加位掩码；源若依赖固定有效位数，目标必须写出相同精度，不得用默认 `str()`。
   - *不适用条件*：源本身只做无限精度算术且无定宽契约时，不涉及掩码；但**格式化位数**仍需核对。
5. **错误机械替换反例**：
   ```python
   # 候选受源限制：C write 请求 len 字节不保证一次完整写入；源缓冲区长度须有真实依据
   # Python 源若就是 buf[:n]，目标应保留其裁剪，不新增长度异常。
   # 错误之二：用默认 str 冒充源的定宽/定精度格式
   out = str(value)                # 位数可能与源不同
   # 源已有长度检查/完整写入循环时才映射对应检查/循环；源越界风险不能冒充定长成功。
   out = format(value, ".17g")     # 仅源本有该精度义务时适用
   ```
6. **信息不足或实现相关时的处理**：无法确定源的长度契约与有效位数时，标为“长度与数值格式待确认”；不得用 `str()` 的默认输出或切片的静默截断充当依据。
7. **资料依据（名称/版本/章节）**：PY-REF-DATA §3.2；通用序列操作（切片语义）。

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `str`：不可变 Unicode 码点序列。
- **字节序列数据结构**：`[语言规范保证]` `bytes`：不可变 8 位字节序列；`bytearray`：可变字节序列。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` `str` 与 `bytes` 均显式记录长度，内容可自由包含 `\0`。
- **编码假设与转换陷阱**：`[语言规范保证]` **`str` 与 `bytes` 严格隔离**；严禁隐式转换，必须显式通过 `.encode('utf-8')` 与 `.decode('utf-8')` 互转。
- **官方资料依据**：PY-REF-DATA §3.2 Strings, Bytes

### L1-PY-03 字节路径不得经文本层，且不得用替换策略掩盖编码差异
1. **源码触发条件**：源码读写二进制（`open(path, 'rb'/'wb')`、`socket.recv`、`hashlib`、`base64`、`zlib`、结构体打包），或在文本与字节之间用 `.encode`/`.decode` 转换。
2. **冻结版本/运行时/API 前提**：CPython 3.12；`decode` 的 `errors` 参数与 `open` 的 `newline`/`encoding` 语义见 PY-REF-DATA §3.2、`bytes.decode`、`open`。
3. **原可观察行为**：
   - `str`/`bytes` **严格隔离**：`b"a" + "b"` 抛 `TypeError`，不存在隐式编解码。
   - `bytes.decode('utf-8')` 对非法序列**默认抛 `UnicodeDecodeError`**；`errors="replace"`/`"ignore"` 则**静默改变内容与长度**。
   - 文本模式 `open(path, 'r')` 默认 `encoding=None`（取 `locale.getpreferredencoding(False)`），且**默认启用通用换行翻译**（`newline=None` 把 CRLF/LF/CR 统一为 `\n`）；`'rb'` 无此翻译。
   - `len(str)` 是码点数，`len(bytes)` 是字节数；非 ASCII 时两者不等。
   - 路径/argv 的 OS 字节表示按 filesystem encoding 和 error handler 转换；`os.fsencode` 使用当前 Python 的配置，不是通用 UTF-8 编码。跨 OS 时，当前目标的编码不自动等于源的窄字符 argv 编码。
   - 文本写入的 `newline=None` 会把 `\n` 翻译为当前系统行分隔符；`newline=''` 或 `'\n'` 不翻译。还须核字符串内部行尾、`print` 的 `end` 与最终 stdout writer，不能以文件 newline 选项代表所有控制台输出。
4. **目标可选写法和不适用条件**：
   - *Python 作为源*：字节路径映射到目标的字节类型；文本路径须显式声明 `encoding` 与 `newline`，**不得**依赖平台默认编码或默认换行翻译。
   - *Python 作为目标*：源若以字节为单位读写，必须走 `'rb'`/`'wb'` 与 `bytes`，**不得**经 `str` 往返；源若以文本为单位，须显式写出编码与换行策略，并保留源对非法字节的处理方式（抛错或替换）。
   - *不适用条件*：源本身是文本 API 且换行翻译属源的可观察行为时，通用换行是要**保留**的行为，须显式冻结而非消除。
   - **按字节计的路径长度**：只在所用 filesystem encoding/error handler 与源路径字节契约一致时，才用 `len(os.fsencode(path))` 承接源字节数；源明确 UTF-8 时按该编码计数。不能用 `len(path)`，也不能在编码未知时随意 `.encode()`。UTF-8 文本 `é` 为一个码点、两个字节，ASCII 路径通过不足以核验此映射。
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
7. **资料依据（名称/版本/章节）**：`bytes.decode`（错误处理策略）；`open`（encoding/newline）；`os.fsencode`（filesystem encoding/error handler）；Python Unicode HOWTO。

### L1-PY-06 字节字面量与十六进制数据不得按外观重写

1. **触发/前提**：CPython 3.12；目标采用 bytes 字面量、`bytes.fromhex` 或分段连接来承接源固定字节数据。
2. **应保留行为**：Python bytes 字面量的 `\x` 后须恰有两个十六进制数字；`bytes.fromhex` 按两个数字构成一字节并允许 ASCII 空白。它们与 C/C++ 可继续消费十六进制数字的 `\x` 转义语法不同，不能照抄字面量源码。
3. **映射条件**：先对应源求值后的元素序列和有效长度，再选择目标表达式；分段拼接核顺序、重复/遗漏、嵌入 NUL 与是否包含源终止 NUL。不得凭“重构更简洁”重算、替换未知用途的常量。
4. **反例**：C 的 `"\x0041"` 的转义值为 0x41，Python `b'\x0041'` 则是 0x00、0x34、0x31 三个字节；照抄转义造成差异。只对照字符个数或总长度可能漏掉同长度的替换。
5. **未知处理**：源转义求值、元素范围或消费者长度不确定时逐点保留待核，不猜数据；静态审阅不运行、解码执行或解释未知数据。
6. **官方依据**：Python 3.12 字符串/字节字面量、`bytes.fromhex`；源侧结合其语言标准核对。

### L1-PY-07 getopt 的顺序策略由源解析器决定

1. **触发/前提**：源实际使用选项解析，拟映射为 CPython 3.12 `getopt`/`gnu_getopt`；冻结源 libc/解析器版本、选项串、环境及解析后的操作数用途。
2. **行为与映射**：`getopt.getopt` 在首个非选项处停止；`gnu_getopt` 默认允许选项与操作数交错，但选项串前导 `+` 或 `POSIXLY_CORRECT` 会改变其模式。仅源确需同类扫描策略时选用；还要核长选项缩写、`--`、剩余参数及错误路径，不能只因函数同名当成等价。
3. **反例**：源允许 `tool operand -a` 继续解析 `-a`，目标改成普通 getopt 而提前停止；反之源应停止而目标继续扫描，同样改变行为。
4. **未知处理**：源实现未知则记录待确认；Python `GetoptError` 的 message/异常输出不自动复现 BSD/GNU 的诊断、通道、程序名和退出码，不硬编码猜测的 libc 文案。
5. **官方依据**：Python 3.12 getopt / gnu_getopt。

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` `list`：动态可变序列；`tuple`：固定长度不可变序列。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `dict`：键值映射类型。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` **语言规范保证保持键值对的插入顺序**（Insertion-order preservation）。
- **迭代期间修改（Fail-Fast）**：`[语言规范保证]` 迭代中改变 `dict` 大小立即抛出 `RuntimeError: dictionary changed size during iteration`。
- **官方资料依据**：PY-REF-DATA §3.2 Dictionaries

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` 异常驱动控制流（EAFP：Easier to Ask for Forgiveness than Permission）；`try`/`except`/`finally`/`else`。
- **异常展开与性能模型**：`[语言规范保证]` 异常为一等对象，抛出并回溯展开栈帧。
- **进程退出码回传机制**：`[语言规范保证]` `sys.exit(int/str)` 抛出 `SystemExit` 异常，若未捕获则解释器退出并设置退出码；未捕获普通异常退出码为 1。
- **跨语言映射关键风险**：不可将 C 常见负数返回值当成 Python 正常状态；必须明确区分业务状态与真实失败。
- **官方资料依据**：PY-REF-DATA §3.2 Exceptions

### L1-PY-04 被丢弃的错误不得变成异常终止，主动失败不得被静默吞掉
1. **源码触发条件**：源码**有意丢弃**可失败操作的结果（未检查返回值、空 `except: pass`、未检查函数返回的 `None`），**或**在失败时 `raise`、`sys.exit(非零)`、返回非零状态。
2. **冻结版本/运行时/API 前提**：CPython 3.12；未捕获异常退出码为 1、`SystemExit` 携带指定码，见 PY-REF-DATA、`sys.exit`。
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
7. **资料依据（名称/版本/章节）**：PY-REF-DATA；`sys.exit`；内置异常层次。

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[指定运行时的实现相关事实]` CPython 采用**引用计数（Reference Counting）即时回收**为主，分代循环垃圾收集器（Cyclic GC）为辅。
- **资源确定性释放机制**：`[语言规范保证]` 上下文管理器 `with` 语句确保退出时触发 `__exit__()` 释放非内存资源；`__del__` 时机不可靠。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 循环垃圾检测器分为 3 代，定期遍历检测孤立循环引用；无法保证跨实现确定性析构。
- **悬垂与泄漏防范**：循环引用在仅靠引用计数时无法立即回收，依赖 Cyclic GC 扫描；非内存资源严禁依赖 `__del__`。
- **官方资料依据**：CPY-DEV-GC<br>PY-REF-DATA

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` `threading`；`multiprocessing`；`asyncio`（单线程事件循环协程）。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` CPython 全局解释器锁（GIL）确保同一时刻仅一个线程执行字节码；多线程无法利用多核进行 CPU 密集计算。
- **级联取消与超时机制**：`[语言规范保证]` `asyncio.Task.cancel()` 抛出 `CancelledError`；`asyncio.wait_for` 设定超时。
- **内存模型与数据竞争**：`[指定运行时的实现相关事实]` 虽受 GIL 保护基础操作原子性，但复合状态操作仍存在竞态，必须使用 `threading.Lock`。
- **官方资料依据**：CPY-DEV-GC<br>PY-REF-DATA

## 八、枚举与终端输入

### L1-PY-08 Enum、IntEnum 与普通常量的身份不同

1. **触发**：枚举成员、值构造、类型测试、整数比较、Flags、输出或序列化。
2. **前提**：CPython 3.12，冻结成员显式值、别名、类型及消费者；不要以 auto 代替已给定数值。
3. **事实**：Enum 成员具有枚举类型、name/value；重复值可为别名，迭代会跳过别名。IntEnum 可作整数使用，整数运算结果丢枚举身份；3.12 的 str(IntEnum) 是整数文本。普通 Enum 默认显示类型与成员名。Flag/IntFlag 的未知位还受 boundary 策略影响。
4. **映射条件**：按源类型、整数互操作、位组合、未知值、名称输出逐项选 Enum/IntEnum/Flag/IntFlag 或其他明确表示；默认 Enum 值构造拒绝未定义值，源允许该值时须保持源路径。
5. **反例**：普通 class 数值属性不提供成员身份；C# 枚举值显示名称时改成 IntEnum 的默认 str 会输出数字。
6. **未知**：仅常量消费者可在确认观察范围后用常量表示；反射/未知值/别名显示未明时不宣布标准库类型完全等价。
7. **依据**：Python 3.12 enum；Enum HOWTO：别名和值构造。

### L1-PY-09 流读取一个字符不等于读取一个终端键事件

1. **触发**：单键等待、回显、特殊键、输入重定向或终端模式。
2. **前提**：CPython 3.12，冻结 OS、TTY、编码、终端模式与实际输入设备。
3. **事实**：input 读一行；sys.stdin.read(1) 读一个文本字符，终端 canonical 模式仍可能等行提交。Unix tty/termios 与 Windows msvcrt 是不同平台 API，getwch 不自动给出 .NET 完整键/修饰键对象；终端模式变化还须恢复。
4. **映射条件**：按源键/字符单位、回显、阻塞、特殊键序列与失败选平台映射；只有已确认只读流字符时才直接用 read(1)。
5. **反例**：用 input 替代 ReadKey 增加 Enter 要求；只用 read(1) 而未确认设备/模式也不能声称“任意键继续”。
6. **未知**：源返回键/修饰键映射未知或无合法 TTY 驱动时记缺口；Agent 不生成辅助驱动，不用伪造异常代源观察。
7. **依据**：input；TextIOBase.read；tty；msvcrt。

## 九、解析器、文本边界与容器的选择引导

本节补充CPython 3.12的具体语义，用来选择映射；不增加转换调度门禁，不要求为每个反例运行测试。

### L1-PY-10 optparse 的接受域与程序名

源码实际使用optparse时，先看选项声明、callback、默认值、剩余参数和error/exit的覆盖，而不是套argparse或getopt的默认行为。optparse允许唯一的长选项前缀；歧义、未知选项、缺参走解析器错误路径，默认打印stderr用法/错误并退出2，应用覆盖这些方法时按覆盖保留。usage中的`%prog`默认取`os.path.basename(sys.argv[0])`，显式prog优先。

目标解析器若不支持唯一前缀，可按已声明选项集保留唯一/歧义分流；没有source触发时不额外增加缩写。`./tool`不能直接当默认显示名，默认空argv下usage相同也不能证明选项分支已保持。具体文案、OS路径解释或callback未知时只标对应缺口，不猜完整诊断。依据：Python 3.12 optparse，OptionParser构造/解析错误/长选项缩写。

### L1-PY-11 空白、分行与制表列位置

先区分`str`的码点操作与`bytes`的字节操作，再确定源用strip、split、splitlines、expandtabs还是textwrap自有谓词；同样叫“空白”不说明集合相同。`str.splitlines`识别LF、CR、CRLF、VT、FF、U+001C至001E、U+0085、U+2028、U+2029；空串返回空列表，末尾分行符不增加空项。`split('\n')`不同，bytes方法也不继承完整Unicode集合。

expandtabs按当前列推进到下一制表位，CR/LF重置列，不是把每个TAB换成固定个数空格；CPython 3.12在tabsize≤0时删除TAB。目标可选择按源集合和列状态处理；只有源明确ASCII范围时才考虑ASCII简化。textwrap还须按实际选项核去空白、断词和保留行尾，不从“Unicode空白”推定其所有谓词。依据：Python 3.12 Built-in Types；CPython v3.12.0 Objects/unicodeobject.c中的unicode_expandtabs_impl；textwrap。

### L1-PY-12 容器操作组合决定顺序

deque既能实现队列也能实现栈。`appendleft`后`popleft`是同端入出，后放入的先返回；`append`后`popleft`才是两端入出。先追踪插入端、取出端、连续pushback、空容器行为及消费者，再选择目标Stack/Queue/双端容器。不能凭名字deque改成Queue，也不能把一个token路径相同当作多个token的顺序保证。

split要核分隔符、maxsplit、首尾空项和首个等号；dict读取默认值、defaultdict和显式插入要核是否改变成员集。稳定排序只在源确有同键顺序义务时对应稳定算法，不能为消噪重排有序序列。依据：Python 3.12 collections.deque、stdtypes字符串/dict及Sorting HOWTO。

### L1-PY-13 编解码的输入接受集合

源调用Base64/数值解析时，分别看编码与解码、接受的空白/非法字符、padding、异常与返回类型。`base64.b64decode`默认validate=False会在padding检查前丢弃非字母表字符，validate=True拒绝此类字符；`b64encode`返回编码后的bytes。选择目标API时保持源实际调用模式，不因同名或“更严格”而自动改变接受域；输出是原始bytes还是编码文本也分别对应。源有异常捕获时保持其范围，解析细节未知则记具体API缺口。依据：Python 3.12 base64、内置数值转换。

涉及临时目录选择时还看源是否按环境优先级、可用性检查、缓存结果或明确传入目录选择；候选目录与真正创建文件分别对应。目标只返回一个默认路径不天然保持源的检查/回退/失败，环境稍后改变是否影响结果也依源缓存契约。具体tempfile API/版本未知时记录该选择点，不从Ruby/Go的顺序反推Python。

### L1-PY-14 tempfile 的候选、可用性与缓存

源码实际调用CPython3.12 tempfile.gettempdir时，默认搜索TMPDIR→TEMP→TMP，再到平台候选：Windows依次`C:\TEMP`、`C:\TMP`、`\TEMP`、`\TMP`；其他平台依次/tmp、/var/tmp、/usr/tmp；最后当前目录。搜索寻找调用用户能创建文件的候选并缓存结果；tempfile.tempdir已设置时会影响默认选择，实际文件API显式dir参数另优先。不能把它仅映射为每次读取一个环境变量或创建一个新目录。

先看源码何时首次选择、是否修改tempdir、是否指定dir以及返回str/bytes的消费者，再选目标的选择/校验/缓存行为。环境变化不自动意味着已有缓存失效；Go os.TempDir的只选路径与Ruby Dir.tmpdir的候选/校验也不能替这套语义。未知OS、变量/缓存状态只写对应前提，不读取本机环境代替冻结条件，不在本机创建文件试验源/目标行为。依据：Python3.12 tempfile.gettempdir/gettempdirb/tempdir及各文件API的dir参数。

### L1-PY-15 ctypes 的 ABI 声明与业务判定分别保持

1. **触发/前提**：CPython3.12 ctypes 调用原生 API；冻结 OS/架构、实际库/SDK、调用约定及精确原型，不把 Python 整数当任意原生宽度。
2. **事实/选择**：ctypes 未声明 restype 的普通外部函数默认按 C int 返回；argtypes、返回类型、结构布局、输入/输出指针及容量单位按实际原型选择。句柄/指针不能依默认 int 截断后继续；通用 void 指针只保地址，不证明它指向正确语义对象。
3. **保持行为/反例**：调用成功、输出参数与业务允许/拒绝分开；把 API 调用失败一律当“权限为假”，或删除真实权限调用改固定字符串，不能保持源判断。声明类型也不能证明 API 对象、返回缓冲及释放时机正确。
4. **未知/依据**：原型/ABI未知时记该调用缺口，不猜偏移、造返回值或读取本机状态验证；Windows令牌/权限消费[进程身份系统页](../../systems/posix-windows-process-identity/SKILL.md#原生环境块令牌与缓冲的选择引导)。依据：Python3.12 ctypes 的返回类型、函数原型、指针和结构说明；Win32语义由系统页维护，不新增权限能力。

### L1-PY-16 Unicode 规范化、折叠与文本长度分别保持

1. **触发／前提**：CPython 3.12 的 `unicodedata.normalize`、`str.casefold`、`len(str)` 参与键、去重、排序、限长或输出。
2. **事实**：`len(str)` 按码点计数；`casefold()` 可将一个字符展开成多个码点，如 `ß`→`ss`；lower 不是完整 casefold。normalize 的 NFC/NFD 与 NFKC/NFKD 分别保留规范／兼容关系，不等于大小写转换，调用顺序也是源语义。
3. **映射／反例**：记录规范化形式、Unicode 数据版本、折叠及长度使用时点；`\u1100\u1161` 经 NFC 组合为 `\uac00`，只写 Latin-1 组合表不能保持该行为。将码点限长换成 UTF-16 Length 或 UTF-8 字节数同样改变接受域；视觉字符数不等于码点数。
4. **未知与边界**：目标库／Unicode 表缺失按构建前提记录离线依赖和具体支持范围，不静默退化成 ToLower；子集实现存在不表示子集已验证，不由一个 ASCII 样例证明完整 Unicode 等价。
5. **依据**：Python 3.12 标准类型 str 的 len/casefold；unicodedata.normalize/unidata_version；Unicode Standard Annex #15 的规范／兼容形式。

### L1-PY-17 JSON 接受域不由输出长得相同决定

1. **触发／前提**：CPython 3.12 `json.loads/dumps` 及其 hooks、parse_constant、strict、ensure_ascii、allow_nan；包括先做 UTF-8 解码的入口。
2. **事实**：默认 loads 的重复同名键保留后值；object_pairs_hook 可改变该策略。默认解析可接受 NaN/Infinity，parse_constant 可改为拒绝；dumps 的 allow_nan 属输出约束，不自动约束 loads。合法原始 UTF-8 字节中的 JSON `\ud800` 转义仍可得到孤立代理项，原始 UTF-8 校验不替代该层处理。
3. **映射／反例**：保持源实际配置、错误码／时点和后续编码策略；不能照搬另一用例的拒绝重复键 hook，或将 Go 的代理项替换规则误当 Python 默认。字面 `"\\u0000"` 与解析为 U+0000 的 `"\u0000"` 分开；层数限制和递归错误依实际入口核对，不强造通用 64 层限制。
4. **未知与依据**：独立核输入字节、解析值和输出转义；合法 JSON 转义表示可按冻结结构比较，但字符串值不能被替换字符、大小写或二次转义改写。依据：Python 3.12 json 的 Standard Compliance、Repeated Names、Infinite and NaN Number Values、Character Encodings、loads/dumps 参数。

## 使用边界

将本页与所选的源→目标方向 Skill 及另一语言的共性页组合使用；映射前先确认源码真实行为。文件、网络、并发和跨 OS API 的具体差异仍按[共性索引的场景/系统分流](../seven-language-common-semantics.md)选读，不从语言事实直接推断系统 API 等价。没有逐例第三方证据时，语法/构建与功能结论保持 `UNVERIFIED`；本机不运行或编译样本。
