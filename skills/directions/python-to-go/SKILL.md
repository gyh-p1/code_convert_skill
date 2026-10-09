---
name: python-to-go
description: Use when converting Python source code (CPython 3.12) to Go (Go 1.27) while preserving observable behavior; covers negative indices/slice bounds, exceptions to (T, error), dynamic types to interfaces, generators, and mutable aliasing/concurrency boundaries. Not for Go to Python or other language pairs.
---

# Python → Go 语言转换规则

> **适用基线**：源语言 Python 3.12 / CPython 3.12 ([PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html), [PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)) → 目标语言 Go 1.27 ([GO-SPEC](https://go.dev/ref/spec), [GO-PKG-CONTEXT](https://pkg.go.dev/context))
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Python](../../references/languages/python.md)与[目标语言 Go](../../references/languages/go.md)。
> **规范硬约束**：严格遵循 Python 3.12 规范与 Go 1.27 语言规范；纠正负索引认知（Go 常量负下标为编译期报错，非常数表达式负索引在运行期触发 panic）；消除任何不具官方依据的实现数字。

---

## 一、适用范围与前提

用于将已有 Python 3.12 动态语言代码转换为 Go 1.27 静态编译型代码。转换的核心挑战在于**将 Python 的动态鸭子类型、内建负索引支持、一等异常机制和 GIL 保护下的伪并发，重构为 Go 的强静态类型、显式边界检查、显式错误返回值与真实多核并行内存模型**。

---

## 二、转换时优先守住的行为

- **索引与切片边界安全**：Python 原生支持负数下标从尾部倒数索引（如 `arr[-1]`）和负步长切片；Go 切片索引表达式**严格禁止负数**（常量负索引直接引发**编译错误**；非常数负表达式在运行期触发 **panic: runtime error: index out of range**）。转换时必须显式计算 `len(s) - n` 并进行非负性前置检查。
- **异常转显式多返回值**：Python 广泛使用 EAFP 风格的异常来表达控制流和错误；Go 强制使用显式多返回值 `(result, error)`。必须在调用链中将捕获的异常降级为错误返回，保持错误信息的清晰可观察。
- **动态类型与鸭子类型接口化**：Python 函数参数不声明类型，运行时只要具备对应方法即可调用；在 Go 中必须提取最小方法集并定义显式接口（`interface`），对于复杂混合类型使用泛型或类型开关（Type Switch）。
- **并发环境与数据竞态**：CPython 具备全局解释器锁（GIL），纯 Python 线程不会出现多核同时破坏底层对象结构的物理竞态；Go 的 Goroutine 是**真实多核并行执行**，任何跨 Goroutine 读写共享可变状态都必须加互斥锁（`sync.Mutex`）或通过信道通信，否则将引发严重的数据竞态（Data Race）。

---

## 三、七段式核心转换规则

### 规则 1：Python 负数下标与切片负边界向 Go 显式长度换算映射

1. **触发条件**：Python 源码中使用负整数对序列进行索引（如 `item = arr[-1]`、`data[-2:]`）。
2. **适用前提**：源语言 Python 3.12，目标语言 Go 1.27。
3. **应保留行为**：保持读取序列末尾倒数第 $n$ 个元素的业务逻辑；保持空序列时的越界保护语义。
4. **可选映射与不适用条件**：
   - *可选映射*：在 Go 中显式编写长度换算逻辑：`idx := len(s) - n`，并前置断言 `if len(s) < n { return 0, ErrIndexOutOfRange }`；安全切片 `s[len(s)-n:]`；
   - *不适用条件*：**绝对禁止在 Go 中直接使用负数字面量或负数变量做索引**。Go 规范明确规定：常量负索引（如 `s[-1]`）直接在**编译期报错**；动态变量负索引（如 `i := -1; s[i]`）在**运行期触发 panic**。
5. **错误机械替换反例**：
   ```go
   // 错误反例：直接将 Python 的 -1 下标机械照搬到 Go
   func GetLast(s []int) int {
       return s[-1] // 编译错误: invalid slice index -1 (index must be non-negative)
   }
   ```
6. **不确定性处理**：若源 Python 代码使用了复杂的动态切片步长（如 `s[::-1]` 倒序），在 Go 中切片不支持负步长表达式，必须手工编写双指针原地逆序循环或构造新切片，标注切片步长算法展开。
7. **官方依据**：[GO-SPEC #Index_expressions, #Slice_expressions](https://go.dev/ref/spec)；[PY-REF-DATA §3.2 Sequences](https://docs.python.org/3.12/reference/datamodel.html)。

---

### 规则 2：Python 异常控制流向 Go 显式 `(T, error)` 返回值映射

1. **触发条件**：Python 源码中使用 `raise ValueError(...)`，并在外层通过 `try ... except ...` 捕获处理。
2. **适用前提**：源语言 Python 3.12，目标语言 Go 1.27。
3. **应保留行为**：保持错误发生时的错误信息、失败原因与分支控制流；保持逐层向上传递错误的能力。
4. **可选映射与不适用条件**：
   - *可选映射*：将函数返回值重构为 `(T, error)`；将 Python 的具体异常类映射为 Go 的预定义哨兵错误或实现 `error` 接口的自定义结构体；外层通过 `if err != nil` 结合 `errors.Is` / `errors.As` 进行处理；
   - *不适用条件*：严禁将普通业务异常机械替换为 Go 的 `panic`；严禁使用空的 `except Exception: pass` 机械对齐为丢弃 Go 的 `err`（会导致静默失效）。
5. **错误机械替换反例**：
   ```go
   // 错误反例：将普通验证异常写成 panic，导致服务异常终止
   func ValidatePort(port int) {
       if port < 1 || port > 65535 {
           panic("invalid port") // 致命：普通输入错误不应引发整个 Goroutine 崩溃！
       }
   }
   ```
6. **不确定性处理**：若 Python 代码捕获了第三方库未文档化的高基类异常，需在 Go 中提供通用 `errors.New("unknown error")`，并在返回时包装原始错误链（`fmt.Errorf("operation failed: %w", err)`）。
7. **官方依据**：[GO-SPEC #Errors, #Handling_panics](https://go.dev/ref/spec)；[PY-REF-DATA §3.2 Exceptions](https://docs.python.org/3.12/reference/datamodel.html)。

---

### 规则 3：Python `yield` 生成器向 Go 闭包迭代器或状态机结构体映射

1. **触发条件**：Python 源码中使用 `yield` 关键字定义生成器函数（Generator Function），以懒加载方式产出序列。
2. **适用前提**：源语言 Python 3.12，目标语言 Go 1.27。
3. **应保留行为**：保持每次迭代时按需计算的懒惰求值（Lazy Evaluation）特性；保持生成器内部的局部状态在各次迭代间得以维持。
4. **可选映射与不适用条件**：
   - *可选映射*：
     1. 闭包迭代器模式：返回一个无参闭包 `func() (T, bool)`，每次调用产出一个值及是否结束标志；
     2. 状态机结构体模式：显式定义结构体保存当前指针与迭代状态，暴露 `Next() bool` 和 `Value() T` 方法；
     3. 信道流模式：启动后台 Goroutine 通过 channel 发送数据（需注意必须具备 Context 取消机制以防 Goroutine 泄漏）；
   - *不适用条件*：若非必要，不建议无条件将所有简单生成器映射为 channel，因为 channel 伴随调度开销与缓冲同步约束；若未建立明确的 channel 关闭与取消协议，极易导致 Goroutine 永久挂起泄漏。
5. **错误机械替换反例**：
   ```go
   // 错误反例：未加退出保护的无界 channel 生成器，调用方提前 break 时 Goroutine 永久泄漏
   func Producer() <-chan int {
       ch := make(chan int)
       go func() {
           for i := 0; ; i++ {
               ch <- i // 若调用方读取若干次后退出循环，此 Goroutine 将永久阻塞在写入端，发生泄漏！
           }
       }()
       return ch
   }
   ```
6. **不确定性处理**：若 Python 生成器依赖 `generator.send()` 或 `.throw()` 等高级双向协程通信，应将其判定为复杂的协程状态机，必须使用显式双向信道重构并标注协程协议依赖。
7. **官方依据**：[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)；[GO-SPEC #Function_types, #Channel_types](https://go.dev/ref/spec)。

---

### 规则 4：Python GIL 下的共享可变状态向 Go 强并发同步映射

1. **触发条件**：Python 源码中使用多线程（`threading.Thread`），并发访问全局变量、共享列表或字典而未加显式锁（依赖 CPython 的 GIL 或单字节码原子性假设）。
2. **适用前提**：源语言 Python 3.12，目标语言 Go 1.27。
3. **应保留行为**：保持并发执行的业务逻辑；保证共享数据结构在并发读写下的完整性与一致性。
4. **可选映射与不适用条件**：
   - *可选映射*：为并发访问的共享状态显式增加 `sync.Mutex` 或 `sync.RWMutex` 进行临界区保护；对于键值映射，可采用 `sync.Map` 或带锁封装结构体；
   - *不适用条件*：**绝对严禁直接在多个 Goroutine 中并发读写未同步的普通 Go `map`**（未同步并发读写属于数据竞争 Data Race，Go 运行时在检测到并发写入时可能直接终止进程）；绝对不可认为 Go 具备任何类似 GIL 的隐式保护。
5. **错误机械替换反例**：
   ```go
   // 错误反例：无锁并发写入 Go map，引发严重数据竞争与运行时崩溃
   func ConcurrentWrite(m map[string]int) {
       for i := 0; i < 10; i++ {
           go func(val int) {
               m["key"] = val // 危险：未同步并发写 map 属于数据竞争，运行时检测到将直接终止！
           }(i)
       }
   }
   ```
6. **不确定性处理**：若静态分析无法穷尽所有跨 Goroutine 的并发读写点，必须在项目测试或交付契约中建议开启 Go 的竞态检测器（`-race`），并在交付说明中提示未验证的数据竞争风险。
7. **官方依据**：[CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/)；[GO-SPEC #Map_types](https://go.dev/ref/spec)。

---

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

## 四、跨场景与系统规则按需加载

> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

- **网络与套接字调用**：Python 中调用 `socket` 模块时，加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)；跨 POSIX/Windows 时加读 [`skills/systems/posix-winsock/SKILL.md`](../../systems/posix-winsock/SKILL.md)。
- **文件与路径**：Python 中调用 `os.path`、`open()` 时，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)；跨 OS 路径分隔符加读 [`skills/systems/posix-windows-filesystem/SKILL.md`](../../systems/posix-windows-filesystem/SKILL.md)。
- **并发场景**：跨 OS 线程调度与系统并发原语加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md) 与 [`skills/systems/posix-windows-threads/SKILL.md`](../../systems/posix-windows-threads/SKILL.md)。

---

## 五、模型自检与质量结论声明

1. **模型自检范围**：模型转换完成后核对切片负索引是否全部换算、生成器是否具有生命周期退出保护、共享 map 是否加锁。该自检属于模型自评，严禁充当客观测试依据。
2. **证据状态声明**：当前 Python→Go 方向无项目目标编译 PASS 证据，状态保持为 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`，不宣称转换成功。
