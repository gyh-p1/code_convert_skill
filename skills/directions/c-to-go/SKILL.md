---
name: c-to-go
description: Use when converting C source code (ISO C11) to Go (Go 1.27) while preserving observable behavior; covers pointer arithmetic/aliasing, integer width/overflow, errno/returns to error, slices/arrays, defer, and missing preprocessor. Not for Go to C or other language pairs.
---

# C → Go 语言转换规则

> **适用基线**：源语言 ISO C11 ([WG14-N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)) → 目标语言 Go 1.27 ([GO-SPEC](https://go.dev/ref/spec), [GO-RT-DOC](https://go.dev/doc/gc-guide))
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C](../../references/languages/c.md)与[目标语言 Go](../../references/languages/go.md)。
> **规范硬约束**：严格遵循 Go 1.27 语言规范；Go 规范未规定 map 迭代顺序；清除无官方逐条出处的具体实现假设；禁用跨实现的无保证推断。

---

## 一、适用范围与前提

用于将已有 C11 代码转换为 Go 1.27 代码。转换的核心原则是**用 Go 的强类型与内存安全机制重构 C 的底层指针与手动内存操作，同时精确保留外部可观察行为与错误分类**。C 拥有强大的预处理器宏、任意指针算术和隐式数值转换，而 Go 完全没有预处理器、严格禁止隐式类型转换、且普通指针完全禁用算术运算。

---

## 二、转换时优先守住的行为

- **指针算术与内存越界保护**：C 允许通过指针加减（`ptr + offset`）自由漫游内存；Go 显式指针禁止算术运算（除 `unsafe` 以外）。必须将连续内存块映射为切片（`[]T`），并通过子切片 `slice[offset:]` 或数组索引代替裸指针移动。
- **显式类型系统与定宽整数**：C 允许在不同宽度的有符号/无符号整数间发生隐式整型提升与转换；Go 严禁任何隐式类型转换（即便是 `int` 与 `int32` 也必须显式强转），且常数算术溢出在 Go 中直接属于**编译期错误**。
- **错误模型转换**：C 依赖负数返回值或全局 `errno`；Go 强制采用显式多返回值 `(result, error)`。必须在调用链中将系统与业务错误包装为标准 `error` 接口返回，严禁使用 `panic` 代替普通业务错误返回。
- **`defer` 与作用域生命周期**：C 在退出作用域或函数时释放资源；Go 的 `defer` 语句仅在**外层函数返回前**按 LIFO 逆序执行，其生命周期与包含块（如 `for`、`if`）无关。

---

## 三、七段式核心转换规则

### 规则 1：C 裸指针算术偏移向 Go 切片索引与子切片视窗映射

1. **触发条件**：C 源码中使用指针加减偏移遍历缓冲区（如 `ptr++`、`*(ptr + i)`、`buf + offset`）。
2. **适用前提**：源语言 ISO C11，目标语言 Go 1.27；目标环境避免引入未受保护的 `unsafe.Pointer`。
3. **应保留行为**：保持对缓冲区内指定偏移位置数据的读写正确性；保留边界保护，防止越界访问。
4. **可选映射与不适用条件**：
   - *可选映射*：将 C 连续内存首地址及长度转换为 Go 切片 `s := buf[offset:end]`；指针向前移动 `ptr += n` 转换为重切片 `s = s[n:]`；访问元素 `*ptr` 转换为 `s[0]`；
   - *不适用条件*：严禁为了盲目对齐 C 语法而大量使用 `unsafe.Pointer` 和 `uintptr` 进行指针算术运算（破坏 Go 运行时的逃逸追踪与栈伸缩移动，引发难以排查的内存损坏）；严禁在未检查长度的情况下对空切片解引用。
5. **错误机械替换反例**：
   ```go
   // 错误反例：误将 uintptr 长期持有当作 C 指针，在 GC 或栈伸缩后产生悬垂指针
   import "unsafe"
   func parse(data []byte) {
       ptr := uintptr(unsafe.Pointer(&data[0]))
       // 危险：uintptr 仅为数值，不被 GC 视为指针引用！若发生栈伸缩或分配，ptr 立即失效！
       ptr += 4
       val := *(*uint32)(unsafe.Pointer(ptr)) // 潜在的未定义行为！
       _ = val
   }
   ```
6. **不确定性处理**：若 C 源码通过指针算术故意访问结构体私有成员偏移或进行非常规内存对齐 hack，必须将该逻辑提取为独立的数据包解析函数，并标记内存布局与 ABI 转换不确定性。
7. **官方依据**：[GO-SPEC #Slice_types, #Index_expressions, #Slice_expressions, #Package_unsafe](https://go.dev/ref/spec)；[WG14-N1570 §6.5.6](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 2：C 整数错误码与 `errno` 向 Go 显式多返回值 `(T, error)` 映射

1. **触发条件**：C 源码中函数返回 `int` 表示成败（`0` 成功，非 `0` 错误），或成功返回有效指针、失败返回 `NULL` 并设置全局 `errno`。
2. **适用前提**：源语言 ISO C11，目标语言 Go 1.27。
3. **应保留行为**：保持错误原因的可观察性（错误信息、底层系统错误码）；保持调用方对错误的主动分支处理能力。
4. **可选映射与不适用条件**：
   - *可选映射*：将函数签名重构为多返回值 `func Foo(...) (T, error)`；成功时返回 `(val, nil)`，失败时返回 `(zeroVal, errors.New(...))` 或 `(zeroVal, fmt.Errorf(...))`；系统调用失败可直接返回 `os.NewSyscallError(...)` 或原生 `syscall.Errno`；
   - *不适用条件*：**绝对禁止将常规业务错误映射为 `panic`**；严禁将 C 的 `0` 错误地直接作为 Go 的 `nil` 比较而不作类型转换。
5. **错误机械替换反例**：
   ```go
   // 错误反例：使用 panic 代替错误返回，导致非致命的输入错误直接击垮整个进程
   func ReadConfig(path string) []byte {
       data, err := os.ReadFile(path)
       if err != nil {
           panic(err) // 致命：错误地把普通 I/O 错误上升为程序崩溃！
       }
       return data
   }
   ```
6. **不确定性处理**：若源 C 函数混合了业务状态与错误码（例如 `-1` 表示无数据，`-2` 表示超时，`-3` 表示鉴权失败），应在 Go 中定义哨兵错误（`var ErrNotFound = errors.New(...)`）或自定义错误类型，方便上层通过 `errors.Is` 进行断言。
7. **官方依据**：[GO-SPEC #Errors, #Calls](https://go.dev/ref/spec)；[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 3：C 手动资源释放向 Go `defer` 语句映射与循环泄露防范

1. **触发条件**：C 源码中使用 `fopen`/`fclose`、`malloc`/`free`、互斥锁锁定/解锁，在函数退出前执行清理。
2. **适用前提**：源语言 ISO C11，目标语言 Go 1.27。
3. **应保留行为**：确保无论后续发生正常返回还是运行时 panic 展开，已成功申请的句柄均能确定性关闭。
4. **可选映射与不适用条件**：
   - *可选映射*：在成功获取资源并校验 `err == nil` 后，紧跟 `defer resource.Close()` 或 `defer mu.Unlock()`；
   - *不适用条件*：**严禁在紧凑的长循环体内部直接使用 `defer`**。Go 规范规定 `defer` 延迟调用的执行时机是**外层函数返回时**，而不是包含它的代码块结束时！在 `for` 循环中直接使用 `defer file.Close()` 会导致所有文件句柄一直累积占用，直至整个外层函数退出，极易在循环中途耗尽系统句柄。
5. **错误机械替换反例**：
   ```go
   // 错误反例：在循环体内部直接使用 defer，导致句柄耗尽崩溃
   func processFiles(paths []string) error {
       for _, p := range paths {
           f, err := os.Open(p)
           if err != nil { return err }
           defer f.Close() // 致命错误：defer 直到 processFiles 返回时才执行，循环中文件句柄全部泄露累积！
           // 处理文件...
       }
       return nil
   }
   ```
6. **不确定性处理**：若在循环内部需要即时释放资源，应将单次循环体提取为独立的辅助函数，使 `defer` 在每次子调用返回时即刻执行；或者显式调用 `f.Close()` 并辅以清理逻辑。
7. **官方依据**：[GO-SPEC #Defer_statements](https://go.dev/ref/spec)；[WG14-N1570 §7.22.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 4：C `char*` 以 NUL 结尾字符串向 Go `string` 与生命周期映射

1. **触发条件**：C 源码中使用 `const char*` 或 `char[]` 传递以 `\0` 结尾的字符串，或使用 `strlen`、`strcpy`、`strcat` 等假定 NUL 终止的字符串函数。
2. **适用前提**：源语言 ISO C11，目标语言 Go 1.27。
3. **应保留行为**：保持字符串内容的字符序列、文本语义与只读/可修改契约；Go `string` 内部可包含 `\0` 字节且由显式长度界定。
4. **可选映射与不适用条件**：
   - *可选映射*：C 的 `const char*` 字符串字面量可直接映射为 Go `string`（Go 字符串不可变）；C 的可修改 `char[]` 缓冲区应映射为 `[]byte`，若需要转为 `string` 使用 `string(byteSlice)` 显式转换（会复制数据）；
   - *不适用条件*：**严禁假设 Go 的 `[]byte` 与 C 的 `char*` 内存布局兼容并直接传递给 CGo 调用**；传递给需要 NUL 结尾的 C 函数时，必须显式追加 `\0` 字节或使用 `C.CString()` 转换（需手动 `C.free()`）；**严禁在二进制协议或含嵌入 `\0` 的缓冲区中使用 C 字符串函数**，否则截断丢失数据。
5. **错误机械替换反例**：
   ```go
   // 错误反例：将可能含嵌入 \0 的二进制数据直接转为 string 并用 C 字符串函数处理
   func parsePacket(data []byte) {
       s := string(data) // 危险：若 data 含 \0，string 长度计算正确但 C 函数会截断！
       // 错误：使用 len(s) 传递给期望 NUL 结尾的 C API
       C.process_data(C.CString(s), C.int(len(s))) // 若 s 内含 \0，C 端按 strlen 计算长度会不一致！
   }
   ```
6. **不确定性处理**：若 C 源码混用文本字符串与二进制缓冲区，且类型标注不明确，必须通过上下文判断是否需要 NUL 终止语义，标记待确认字符编码与二进制边界。
7. **官方依据**：[GO-SPEC #String_types](https://go.dev/ref/spec)；[WG14-N1570 §7.1.1, §7.24](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 5：C 预处理器宏定义向 Go 常量、类型别名与构建标签映射

1. **触发条件**：C 源码中使用 `#define` 定义数值常量、字符串常量、位掩码，或使用 `#ifdef` 进行条件编译。
2. **适用前提**：源语言 ISO C11，目标语言 Go 1.27；Go 无预处理器。
3. **应保留行为**：保持常量的符号名、数值与按位运算特征；保持特定平台或编译选项下的条件代码隔离。
4. **可选映射与不适用条件**：
   - *可选映射*：简单数值宏转换为 Go `const` 或带类型的常量枚举组（使用 `iota`）；位掩码使用 `1 << iota`；对于条件编译，拆分文件并使用 Go 标准的构建标签（Build Tags：`//go:build linux` 或 `//go:build windows`）；
   - *不适用条件*：对于复杂的带参数宏（Function-like macros），不能声明为常量，必须转换为内联函数；严禁使用全局变量代替编译期常量。
5. **错误机械替换反例**：
   ```go
   // 错误反例：带参数的宏直接机械转为全局变量或无法求值的语句
   // C 原型: #define MAX(a, b) ((a) > (b) ? (a) : (b))
   // 错误做法：在 Go 中试图用 var MAX 代替，破坏调用语义与类型安全
   func MaxInt(a, b int) int {
       if a > b { return a }
       return b
   }
   ```
6. **不确定性处理**：若 C 源码中包含用于代码生成的极度复杂宏展开（如 X-Macros 生成多组结构体），无法直接用 Go 常量表达时，应手工将其展开为显式的 Go 结构体定义，并在转换报告中详细记录结构展开依据。
7. **官方依据**：[GO-SPEC #Constants, #Iota](https://go.dev/ref/spec)；[WG14-N1570 §6.10](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 6：C 可变参数函数向 Go 切片参数与类型安全映射

1. **触发条件**：C 源码中使用 `<stdarg.h>` 的 `va_list`、`va_start`、`va_arg`、`va_end` 实现可变参数函数（如 `printf` 风格的函数）。
2. **适用前提**：源语言 ISO C11，目标语言 Go 1.27。
3. **应保留行为**：保持函数能接受任意数量参数的能力；保证参数类型与访问顺序的可观察行为。
4. **可选映射与不适用条件**：
   - *可选映射*：对于同类型可变参数（如 `int sum(int count, ...)`），映射为 Go 变长参数 `func sum(values ...int) int`；对于异构类型可变参数（如 `printf` 风格），映射为 `func format(fmt string, args ...interface{})`，并在函数内使用类型断言或反射提取值；
   - *不适用条件*：**严禁假设 Go 的 `...interface{}` 可以像 C 的 `va_arg` 一样直接按内存布局读取类型**；Go 的 `interface{}` 包含类型信息与值指针，必须通过类型断言 `val, ok := arg.(int)` 或类型切换 `switch v := arg.(type)` 安全提取；**C 的 `va_arg` 类型不匹配是未定义行为，Go 的类型断言失败会 panic，必须显式检查**。
5. **错误机械替换反例**：
   ```go
   // 错误反例：未做类型检查直接断言，运行时类型不匹配导致 panic 崩溃
   // C 原型: void log_values(const char* fmt, ...) { va_list args; va_start(args, fmt); int x = va_arg(args, int); ... }
   func logValues(format string, args ...interface{}) {
       // 危险：假设第一个参数一定是 int，若调用方传入 string 会直接 panic！
       x := args[0].(int)
       // 正确：使用类型断言并检查
       if x, ok := args[0].(int); ok {
           // 处理 int
       } else {
           // 处理类型不匹配
       }
   }
   ```
6. **不确定性处理**：若 C 源码的可变参数依赖格式字符串（如 `printf` 的 `%d`、`%s`）动态推断类型，在 Go 中必须解析格式字符串并按顺序匹配 `args` 中的类型，标注格式解析复杂度与类型不匹配的错误处理策略。
7. **官方依据**：[GO-SPEC #Passing_arguments_to_..._parameters](https://go.dev/ref/spec)；[WG14-N1570 §7.16](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

## 四、跨场景与系统规则按需加载

> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

- **网络套接字场景**：涉及原始网络通信时，加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)；跨 POSIX/Windows 套接字加读 [`skills/systems/posix-winsock/SKILL.md`](../../systems/posix-winsock/SKILL.md)。
- **文件与路径场景**：涉及底层文件与目录操作时，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)；跨 OS 路径分隔符加读 [`skills/systems/posix-windows-filesystem/SKILL.md`](../../systems/posix-windows-filesystem/SKILL.md)。
- **并发与原生线程**：C 原生线程映射至 Go 并发体系时，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)；跨 OS 线程调度加读 [`skills/systems/posix-windows-threads/SKILL.md`](../../systems/posix-windows-threads/SKILL.md)。
- **进程与身份/权限场景**：涉及进程创建、替换、等待、终止或身份与特权查询/切换时，共同加载 [`skills/systems/posix-windows-process-identity/SKILL.md`](../../systems/posix-windows-process-identity/SKILL.md)。
- **Windows 注册表与服务场景**：涉及注册表键值读写或经 SCM 创建、配置、启动、停止、删除服务时，加载 [`skills/systems/windows-registry-service-subsystem/SKILL.md`](../../systems/windows-registry-service-subsystem/SKILL.md)；POSIX 侧无等价子系统，按不可映射项处理。

---

## 五、模型自检与质量结论声明

1. **模型自检重点**：核对切片边界检查是否完善、循环内 `defer` 是否被正确剥离至子函数、常量溢出是否在编译前消除。该自检属于模型自评，严禁作为编译通过证据。
2. **证据状态声明**：当前 C→Go 方向处于 `未验证/阻断` 状态（RC4 历史用例两端未构建），在补丁 `7d77158` 部署并取得第三方构建证据前，一律保持 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`。
