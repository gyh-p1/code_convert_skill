---
name: c-to-python
description: Use when converting C source code (ISO C11) to Python (CPython 3.12) while preserving observable behavior; covers pointer/ownership to object model, fixed-width to arbitrary-precision integers, char*/bytes/str boundaries, and error codes to exceptions. Not for Python to C or other language pairs.
---

# C → Python 语言转换规则

> **适用基线**：源语言 ISO C11 ([WG14-N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)) → 目标语言 Python 3.12 / CPython 3.12 ([PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html), [CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/))
> **共性语义依据**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)
> **真实构建证据口径**：当前仓库中以 C 为源、Python 为目标的方向处于**`未验证/阻断`**状态（Controller 虽声明支持 `python`，但本任务未取得版本、安装清单、BOM 或目标构建证据）；本 Skill 仅提供静态决策依据。
> **规范硬约束**：严格遵循 Python 3.12 标准，排除 Python 3.13+ 特性；严格区分 Python 语言规范与 CPython 解释器专有实现（如 GIL、引用计数）。

---

## 一、适用范围与前提

用于将已有 C11 代码转换为 Python 3.12 代码。转换的核心原则是**守住底层系统级语义与行为边界，避免因高级动态特性导致二进制数据损毁、整数精度失真或资源泄漏**。必须在转换前明确：源程序处理的是结构化文本还是二进制原始字节流；目标运行环境是否受 CPython GIL 影响。

---

## 二、转换时优先守住的行为

- **二进制与文本严格隔离**：C 中 `char*` 既可以表示文本字符串，也可以表示任意二进制缓冲区；Python 中 `str`（Unicode 文本）与 `bytes`（8位无符号字节流）**严格隔离且禁止隐式互转**。在缺乏明确字符编码依据时，一律映射为 `bytes`，严禁机械转换为 `str`。
- **定宽整数溢出截断**：C 依赖 32/64 位定宽整数的截断与溢出特性（如哈希计算、加密算法）；Python 的 `int` 具备任意精度，算术运算永不自动溢出。若需要保持截断行为，必须显式施加位掩码（如 `& 0xFFFFFFFF`）。
- **确定性资源释放**：C 依赖显式 `free()`、`fclose()` 或 `close()` 释放资源；Python 依赖垃圾回收机制，但垃圾回收时机对于非内存资源（文件、Socket、锁）不具备跨实现确定性，必须统一映射为 `with` 上下文管理器。
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
7. **官方依据**：[PY-REF-DATA §3.2 Numbers](https://docs.python.org/3.12/reference/datamodel.html)；[WG14-N1570 §6.2.5, §6.3.1.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 2：C 原始字节缓冲区与 `char*` 字符串向 Python `bytes` 与 `str` 严格隔离映射

1. **触发条件**：C 源码中使用 `char*`、`uint8_t[]`、`unsigned char*` 作为网络包数据、二进制协议帧或以 `\0` 结尾的字符串缓冲区。
2. **适用前提**：源语言 ISO C11，目标语言 Python 3.12。
3. **应保留行为**：保持原始字节数据的精确字节序列、内部嵌入的 `\0` 字节不被截断；若为纯文本，保持文本字符集解码一致性。
4. **可选映射与不适用条件**：
   - *可选映射*：对于二进制包、固定长度数据结构或未明码流，映射为 `bytes`（只读）或 `bytearray`（需原地修改时）；仅当确认其输入完全为 UTF-8/ASCII 文本、且作为控制台输出或文本配置时，才可显式调用 `.decode('utf-8')` 转为 `str`；
   - *不适用条件*：**严禁将包含任意字节流或 NUL 的 C 缓冲区直接转换为 Python `str`**（可能引发 `UnicodeDecodeError` 或破坏二进制协议）；无具体编码和 API 依据时一律保持为 `bytes` 并标记 `[待 D3 专题核验]`。
5. **错误机械替换反例**：
   ```python
   # 错误反例：将底层套接字接收到的原始字节缓冲区强制当作 str 处理
   def parse_packet(raw_data: bytes):
       text = str(raw_data)       # 错误：生成的是 "b'\\x01\\x00...'" 字符串字面表示，非解码内容！
       header = raw_data.decode() # 错误：若 raw_data 包含非 UTF-8 字节，直接抛出 UnicodeDecodeError 崩溃！
   ```
6. **不确定性处理**：若源码中字符串来自本地操作系统的文件名或环境参数（可能受平台代码页影响），应使用 `os.fsencode()` / `os.fsdecode()` 处理，并在报告中标记字符编码依赖不确定性。
7. **官方依据**：[PY-REF-DATA §3.2 Strings, Bytes](https://docs.python.org/3.12/reference/datamodel.html)；[WG14-N1570 §7.1.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 3：C 函数返回值错误码与全局 `errno` 向 Python 结构化异常映射

1. **触发条件**：C 源码中通过返回负数错误码（如 `-1`）、`0` 表示成功，或在失败后读取全局 `errno` 判断具体故障。
2. **适用前提**：源语言 ISO C11，目标语言 Python 3.12。
3. **应保留行为**：保持失败时的错误类型（如找不到文件、连接拒绝、权限不足）与错误信息；保证上层调用者能够针对性捕获或向上传播。
4. **可选映射与不适用条件**：
   - *可选映射*：将 C 的负数失败返回重构为抛出 Python 内建异常（如 `OSError`、`ValueError`、`PermissionError`）；系统调用失败可直接构造 `OSError(errno, os.strerror(errno))`；
   - *不适用条件*：严禁将 C 的返回值 `0` 错误判断为 Python 的 `False`，或把负数错误码当成正常的业务返回值；若原 C 函数具备业务状态查询语义（如查找不到返回 `-1`），应权衡返回 `None` 或抛出 `KeyError`/`IndexError`，不可混淆。
5. **错误机械替换反例**：
   ```python
   # 错误反例：机械翻译 C 的错误检查，在 Python 中产生布尔真假反转的严重逻辑漏洞
   # C 原型: if (write_data(fd, buf) != 0) { /* 错误处理 */ }
   if write_data(fd, buf): # 错误：C 成功返回 0，在 Python 中 0 被视作 False，导致错误分支在成功时反向执行！
       handle_error()
   ```
6. **不确定性处理**：若 C 源码定义了专有的私有枚举错误码，应在 Python 中定义专属的派生异常基类（继承自 `Exception`），并在未识别错误码出现时抛出通用运行时异常，标明错误码映射字典未穷尽。
7. **官方依据**：[PY-REF-DATA §3.2 Exceptions](https://docs.python.org/3.12/reference/datamodel.html)；[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 4：C 显式句柄释放向 Python `with` 上下文管理器映射与终结时机约束

1. **触发条件**：C 源码中使用 `fopen`/`fclose`、`socket`/`close`，或手工管理互斥锁的加锁/解锁。
2. **适用前提**：源语言 ISO C11，目标语言 Python 3.12。
3. **应保留行为**：保证无论正常分支还是发生未捕获异常时，底层系统资源（文件句柄、套接字、互斥锁）均能立即、确定性地释放。
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
7. **官方依据**：[CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/)；[PY-REF-DATA §3.3.9](https://docs.python.org/3.12/reference/datamodel.html)。

---

## 四、跨场景与系统规则按需加载

> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

- **网络套接字场景**：涉及原始 `socket` 调用时，加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)；跨 POSIX/Windows 时加读 [`skills/systems/posix-winsock/SKILL.md`](../../systems/posix-winsock/SKILL.md)。
- **文件与路径场景**：涉及系统路径操作时，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)；跨 OS 路径分隔符加载 [`skills/systems/posix-windows-filesystem/SKILL.md`](../../systems/posix-windows-filesystem/SKILL.md)。
- **多线程与并发场景**：使用 Python `threading` 模块时，必须明确受到 CPython GIL 约束（无法多核并行 CPU 密集型任务），并加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。

---

## 五、模型自检与质量结论声明

1. **模型自审边界**：转换生成的 Python 代码应核对位掩码截断是否存在、异常捕获是否对齐、`bytes` 与 `str` 是否混用。该项自审为模型自评，不得标记为语法通过。
2. **证据状态声明**：本项目当前无 Python 目标构建与功能验收证据，状态严格保持为 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`，不宣称转换等价。
