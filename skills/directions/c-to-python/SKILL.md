---
name: c-to-python
description: Use when converting C source code (ISO C11) to Python (CPython 3.12) while preserving observable behavior; covers pointer/ownership to object model, fixed-width to arbitrary-precision integers, char*/bytes/str boundaries, and error codes to exceptions. Not for Python to C or other language pairs.
---

# C → Python 语言转换规则

> **适用基线**：源语言 ISO C11 (WG14-N1570) → 目标语言 Python 3.12 / CPython 3.12 (PY-REF-DATA, CPY-DEV-GC)
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C](../../references/languages/c.md)与[目标语言 Python](../../references/languages/python.md)，按源码选择适用规则。
> **规范硬约束**：严格遵循 Python 3.12 标准，排除 Python 3.13+ 特性；严格区分 Python 语言规范与 CPython 解释器专有实现（如 GIL、引用计数）。

---

## 一、适用范围与前提

用于将已有 C11 代码转换为 Python 3.12 代码。转换的核心原则是**守住底层系统级语义与行为边界，避免因高级动态特性导致二进制数据损毁、整数精度失真或资源泄漏**。必须在转换前明确：源程序处理的是结构化文本还是二进制原始字节流；目标运行环境是否受 CPython GIL 影响。

---

## 二、转换时优先守住的行为

- **二进制与文本严格隔离**：C 中 `char*` 既可以表示文本字符串，也可以表示任意二进制缓冲区；Python 中 `str`（Unicode 文本）与 `bytes`（8位无符号字节流）**严格隔离且禁止隐式互转**。在缺乏明确字符编码依据时，一律映射为 `bytes`，严禁机械转换为 `str`。
- **定宽整数溢出截断**：C 依赖 32/64 位定宽整数的截断与溢出特性（如哈希计算、加密算法）；Python 的 `int` 具备任意精度，算术运算永不自动溢出。若需要保持截断行为，必须显式施加位掩码（如 `& 0xFFFFFFFF`）。
- **确定性资源释放**：保持 C 实际显式释放的时点、顺序及失败副作用。Python 垃圾回收不代显式释放；with 仅在其退出范围与源一致时适用，不为修源泄漏而新增释放路径。
- **指针引用与对象别名**：C 指针传参修改外部结构体；Python 函数参数为“对象引用的按值传递”，对于不可变对象（`int`、`str`、`bytes`）无法原地修改，必须通过返回新值重构。

---

## 三、七段式核心转换规则

### 规则 1：C 定宽整数算术溢出向 Python 任意精度整数与显式位掩码截断映射

1. **触发条件**：C 源码中使用 `uint32_t`、`uint16_t`、`unsigned int` 等类型进行循环累加、移位、哈希计算或加密混淆，依赖模 $2^n$ 截断。
2. **适用前提**：源语言 ISO C11，目标语言 Python 3.12。
3. **应保留行为**：保持在达到 $2^{32}$ 或 $2^{64}$ 上限时的回绕截断行为；保持数值符号性与位级可观察结果一致。
4. **可选映射与不适用条件**：
   - *可选映射*：在每一步复合赋值、加减或移位操作后显式施加位掩码 `& 0xFFFFFFFF`（针对 32 位无符号）或 `& 0xFFFFFFFFFFFFFFFF`（针对 64 位无符号）；若涉及有符号数补码解释，可定义轻量辅助转换函数；
   - *不适用条件*：严禁直接照抄算术表达式而不加掩码（Python 会无限扩展整数位数，导致高位数据残留，哈希或校验和计算彻底失效）。
5. **错误机械替换反例**：
   ```python
   # 错误反例：未加位掩码截断，导致 Python 整数位数无限增长，哈希计算与 C 不一致
   def hash_step(h, c):
       # C 原型: h = (h << 5) + h + c; (uint32_t)
       h = (h << 5) + h + c  # 错误：高位未截断，若干轮后数值远超 32 位！
       return h
   ```
6. **不确定性处理**：若源码中为 C 有符号整数溢出（规范属于 UB，但在特定编译器下表现为补码回绕），应标明该行为依赖实现定义，并提示确认是否按 32 位有符号补码（`ctypes.c_int32`）严格建模。
7. **官方依据**：PY-REF-DATA §3.2 Numbers；WG14-N1570 §6.2.5, §6.3.1.3。

---

### 规则 2：C 原始字节缓冲区与 `char*` 字符串向 Python `bytes` 与 `str` 严格隔离映射

1. **触发条件**：C 源码中使用 `char*`、`uint8_t[]`、`unsigned char*` 作为网络包数据、二进制协议帧或以 `\0` 结尾的字符串缓冲区。
2. **适用前提**：源语言 ISO C11，目标语言 Python 3.12。
3. **应保留行为**：显式长度路径保留全部字节及内部 NUL；源 NUL 终止 API 则保留其实际前缀观察，不扩大到缓冲区其余字节。纯文本按实际编码与消费者解码，不凭 char* 类型决定。
4. **可选映射与不适用条件**：
   - *可选映射*：对于二进制包、固定长度数据结构或未明码流，映射为 `bytes`（只读）或 `bytearray`（需原地修改时）；仅当确认其输入完全为 UTF-8/ASCII 文本、且作为控制台输出或文本配置时，才可显式调用 `.decode('utf-8')` 转为 `str`；
   - *不适用条件*：没有编码和消费者依据不得把任意字节转为 str；NUL 本身不是 Python str 的禁用字符，已知编码的文本可包含它。源若按 NUL 终止 API 观察前缀，须保留该截断，而显式长度缓冲区须保留全部字节；未知时记录具体编码/长度缺口。
5. **错误机械替换反例**：
   ```python
   # 错误反例：将底层套接字接收到的原始字节缓冲区强制当作 str 处理
   def parse_packet(raw_data: bytes):
       text = str(raw_data)       # 错误：生成的是 "b'\\x01\\x00...'" 字符串字面表示，非解码内容！
       header = raw_data.decode() # 错误：若 raw_data 包含非 UTF-8 字节，直接抛出 UnicodeDecodeError 崩溃！
   ```
6. **不确定性处理**：源码字符串来自 OS 文件名或 argv/环境参数时，先核源编码与目标 filesystem encoding/error handler。只有它们与源字节契约一致时才用 `os.fsencode()` / `os.fsdecode()`；跨 OS 不默认一致，源明确编码时按该编码处理。长度不得换成 `len(str)`，详见 [Python L1-PY-03](../../references/languages/python.md#三字符串字节nulunicode-与编码)；信息不足记录待核。
7. **官方依据**：PY-REF-DATA §3.2 Strings, Bytes；WG14-N1570 §7.1.1。

---

### 规则 3：C 函数返回值错误码与全局 `errno` 向 Python 结构化异常映射

1. **触发条件**：C 源码中通过返回负数错误码（如 `-1`）、`0` 表示成功，或在失败后读取全局 `errno` 判断具体故障。
2. **适用前提**：源语言 ISO C11，目标语言 Python 3.12。
3. **应保留行为**：保持失败时的错误类型（如找不到文件、连接拒绝、权限不足）与错误信息；保证上层调用者能够针对性捕获或向上传播。
4. **可选映射与不适用条件**：
   - *可选映射*：先保留返回码及源检查/忽略分支；只有接口、调用链和捕获边界均允许时才考虑 Python 异常。errno 仅在相应 API 的规定失败点取得，不从返回值符号猜测。
   - *不适用条件*：不得把源当正常状态消费的负值自动异常化，也不为未识别错误码添加新的失败；返回 None/异常/原码须由源消费者与冻结契约决定。
5. **错误机械替换反例**：
   ```python
   # 返回值仍为数值码时，明确保留源的非零判断，不猜测目标 API 的返回形态
   # C 原型: if (write_data(fd, buf) != 0) { /* 错误处理 */ }
   if write_data(fd, buf) != 0: # 成功 0 不进入；源非零失败进入，Python 数值真值不会把它反转
       handle_error()
   ```
6. **不确定性处理**：私有枚举或未穷尽错误码保留实际数值、源分流与数据；不能自行给未知码添加通用异常。必要语义未知时记录并停止受影响映射。
7. **官方依据**：PY-REF-DATA §3.2 Exceptions；WG14-N1570 §7.5。

---

### 规则 4：C 显式句柄释放向 Python `with` 上下文管理器映射与终结时机约束

1. **触发条件**：C 源码中使用 `fopen`/`fclose`、`socket`/`close`，或手工管理互斥锁的加锁/解锁。
2. **适用前提**：源语言 ISO C11，目标语言 Python 3.12。
3. **应保留行为**：保持源在正常/失败路径上实际发生的释放、缺失释放、释放顺序及副作用；源已有泄漏单列风险，不作为转换中自动修复的理由。
4. **可选映射与不适用条件**：
   - *可选映射*：使用 Python `with` 上下文管理器（如 `with open(...) as f:`, `with lock:`）；针对无开箱即用支持的资源，使用 `contextlib.contextmanager` 编写封装器；
   - *不适用条件*：**严禁依赖对象的析构方法 `__del__()` 进行非内存资源清理**。CPython 虽然以引用计数为主，但当存在循环引用或在解释器退出阶段时，`__del__` 调用时机完全不确定，可能导致文件句柄耗尽或死锁。
5. **错误机械替换反例**：
   ```python
   # 错误反例：依赖 __del__ 关闭文件句柄，在复杂调用与循环引用下句柄泄漏
   class FileHolder:
       def __init__(self, path):
           self.f = open(path, "w")
       def __del__(self):
           self.f.close() # 极度危险：__del__ 执行时机不可控，循环引用下甚至永远不执行！
   ```
6. **不确定性处理**：若源 C 代码中的资源所有权跨越多个函数且生命周期长于调用栈（例如缓存在全局哈希表中），无法使用局部 `with` 语句包裹时，必须显式提供 `close()` 方法，并在外层建立生命周期守卫，标注资源生命周期非结构化风险。
7. **官方依据**：CPY-DEV-GC；PY-REF-DATA §3.3.9。

---

### 规则 5：C 指针修改外部结构体向 Python 返回值重构映射

1. **触发条件**：C 源码中函数通过指针参数修改外部对象（如 `void update_state(struct State* s)`）。
2. **适用前提**：源语言 ISO C11，目标语言 Python 3.12。
3. **应保留行为**：保持函数对外部状态的修改可见性；保证调用方能观察到修改后的值。
4. **可选映射与不适用条件**：
   - *可选映射*：对于不可变对象（`int`、`str`、`bytes`、`tuple`），无法通过传参原地修改，必须将修改后的新值作为返回值；对于可变对象（`list`、`dict`、自定义类实例），可保持传参并原地修改；若需要修改多个值，使用元组多返回值 `return (val1, val2)` 或返回字典；
   - *不适用条件*：严禁假设 Python 函数参数可以像 C 指针一样修改基本类型的外部变量（如整数、字符串）；严禁混淆可变与不可变对象的修改语义。
5. **错误机械替换反例**：
   ```python
   # 错误反例：试图通过参数修改不可变的整数，调用方无法观察到变化
   # C 原型: void increment(int* x) { (*x)++; }
   def increment(x):  # 错误：x 是整数对象引用，重新赋值不影响外部
       x = x + 1
       # 调用方的变量不会改变！

   # 正确做法：返回新值
   def increment(x):
       return x + 1
   # 调用方：val = increment(val)
   ```
6. **不确定性处理**：若 C 函数既通过指针修改参数，又有返回值表示成功/失败，在 Python 中应返回 `(success, modified_values)` 元组，并在文档注释中说明返回值结构。
7. **官方依据**：PY-REF-DATA §3.1 Objects, values and types；WG14-N1570 §6.2.5。

---

### 规则 6：C 多线程与 POSIX/Win32 原生线程向 Python threading 与 GIL 约束映射

1. **触发条件**：C 源码中使用 `pthread_create`、`CreateThread` 或 C11 `thrd_create` 创建多线程并发任务。
2. **适用前提**：源语言 ISO C11，目标语言 Python 3.12 / CPython。
3. **应保留行为**：保持线程创建数量、入口函数、参数传递、同步与 join 的可观察行为；保持线程间共享状态的同步语义。
4. **可选映射与不适用条件**：
   - *可选映射*：按创建/共享状态/等待/取消义务核 threading.Thread、Lock、Condition。冻结 CPython 构建与原生扩展决定 GIL 影响；性能限制单列，不为 CPU 密集任务自动切成 multiprocessing，否则共享状态、故障和进程副作用会变。
   - *不适用条件*：严禁假设 Python 多线程可以充分利用多核 CPU 进行 CPU 密集计算；严禁在未加锁情况下并发修改共享的可变对象（`list`、`dict`）。
5. **错误机械替换反例**：
   ```python
   # 错误反例：期望多线程并行加速 CPU 密集计算，实际受 GIL 限制性能反而下降
   import threading

   def cpu_intensive_work(data):
       result = 0
       for i in range(10000000):  # CPU 密集循环
           result += i * data
       return result

   # 错误：启动多线程期望并行加速，但 GIL 导致线程串行执行且上下文切换开销更大！
   threads = [threading.Thread(target=cpu_intensive_work, args=(i,)) for i in range(4)]
   # 性能观察不授权改进程模型；multiprocessing 只在另行确认语义与任务范围后考虑。
   ```
6. **不确定性处理**：若 C 源码涉及复杂的线程属性、信号掩码、线程取消或线程局部存储（TLS），Python `threading` 模块不完全对等，必须加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md) 并标注语义差异。
7. **官方依据**：PY-THREADING；CPY-DEV-GC；WG14-N1570 §7.26。

---

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

## 四、跨场景与系统规则按需加载

> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

- **网络套接字场景**：涉及原始 `socket` 调用时，加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)；跨 POSIX/Windows 时加读 [`skills/systems/posix-winsock/SKILL.md`](../../systems/posix-winsock/SKILL.md)。
- **文件与路径场景**：涉及系统路径操作时，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)；跨 OS 路径分隔符加载 [`skills/systems/posix-windows-filesystem/SKILL.md`](../../systems/posix-windows-filesystem/SKILL.md)。
- **多线程与并发场景**：使用 Python `threading` 模块时，必须明确受到 CPython GIL 约束（无法多核并行 CPU 密集型任务），并加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
- **进程与身份/权限场景**：涉及进程创建、替换、等待、终止或身份与特权查询/切换时，共同加载 [`skills/systems/posix-windows-process-identity/SKILL.md`](../../systems/posix-windows-process-identity/SKILL.md)。

---

## 五、模型自检与质量结论声明

1. **模型自审边界**：转换生成的 Python 代码应核对位掩码截断是否存在、异常捕获是否对齐、`bytes` 与 `str` 是否混用。该项自审为模型自评，不得标记为语法通过。
2. **证据状态声明**：本项精确目标版本尚无对应第三方构建证据时保持 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`；取得后按实际编译、执行与观察范围分层报告。不从本页静态知识推定通过，也不把历史未验证状态当作新任务永久结论。

---

## 六、转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。

**执行顺序受根入口三道硬门禁约束**（分类 `ALLOWED` → 源侧预检（构建 + 适用运行基线）→ 评估就绪核对），细节见 [AGENTS.md](../../../AGENTS.md) 执行约束 §3。本方向 Skill 只提供语言映射规则，**不替代门禁、不构成执行授权**。

## 网络 API 映射

迁入网络场景的本方向细节，仅在原始 socket I/O 触发时使用；通用部分 I/O、协议与生命周期仍读[网络场景](../../scenes/network-io/SKILL.md)。C recv 缓冲按显式长度映射为 Python bytes，不转 str；只有源文本契约明确时才显式解码并保留解码失败。完整消息须按源帧/长度循环，不能一次 recv 读满。POSIX 的 -1/errno 与 Python OSError 子类按错误路径对应；Winsock 源另读系统错误模型，不把 errno 泛化到全部 C。版本/错误类别不明时待确认，静态规则不证明运行等价。
