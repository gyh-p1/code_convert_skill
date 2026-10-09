---
name: csharp-to-go
description: Use when converting C# source to Go; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → Go 语言转换规则

> **适用基线**：C# 12 / .NET 8 → Go 1.27。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C#](../../references/languages/csharp.md)与[目标语言 Go](../../references/languages/go.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C# → Go 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CS-GO-01：C# 异常体系向 Go 显式 (T, error) 多返回值映射
1. **源码触发条件**：C# 源码中使用 `throw` 抛出异常并在多层上层通过 `try-catch` 捕获。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）；目标语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec)）。
3. **原可观察行为**：异常抛出后栈展开，未捕获导致进程异常终止。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重写函数签名返回 `(T, error)`，在失败分支返回明确的错误值，在调用点逐层做 `if err != nil` 检查与传播。
   - *不适用条件*：严禁将业务异常机械转换为 Go `panic`。
5. **错误机械替换反例**：
   ```go
   // 错误：将常规 C# 异常映射为 panic
   func ParseInt(s string) int {
       v, err := strconv.Atoi(s)
       if err != nil { panic(err) } // 错误：在库函数中随意 panic！
       return v
   }
   // 正确：返回 error
   func ParseInt(s string) (int, error) {
       return strconv.Atoi(s)
   }
   ```
6. **信息不足或实现相关时的处理**：若 C# 存在复杂异常树，在 Go 中定义不同的接口或哨兵错误（`var ErrNotFound = errors.New(...)`）支持 `errors.Is`/`errors.As`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)；[GO-SPEC #Errors](https://go.dev/ref/spec)。

### 规则 CS-GO-02：C# using/IDisposable 向 Go defer 逆序资源清理映射
1. **源码触发条件**：C# 源码中使用 `using` 语句管理文件、互斥锁或连接生命周期。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）；目标语言 Go 1.27（[GO-SPEC #Defer_statements](https://go.dev/ref/spec)）。
3. **原可观察行为**：离开作用域时无论如何立即调用 `Dispose()`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在资源成功获取后，紧接着使用 `defer resource.Close()`。
   - *不适用条件*：严禁在长循环内部直接使用 `defer`（`defer` 在外层函数退出时才执行，循环内使用会导致句柄在循环结束前累积耗尽）。
5. **错误机械替换反例**：
   ```go
   // 错误：在循环内部滥用 defer 导致文件描述符泄漏耗尽
   for _, path := range paths {
       f, err := os.Open(path)
       if err != nil { return err }
       defer f.Close() // 致命错误：直到整个大函数退出前，所有文件句柄都不会释放！
   }
   // 正确：将循环体拆解为独立子函数或显式关闭
   for _, path := range paths {
       if err := processFile(path); err != nil { return err }
   }
   ```
6. **信息不足或实现相关时的处理**：若包含多资源依序释放，注意 Go `defer` 是 LIFO（后进先出）逆序执行。
7. **直接官方 HTTPS 依据链接**：[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)；[GO-SPEC #Defer_statements](https://go.dev/ref/spec)。

### 规则 CS-GO-03：C# CancellationToken 向 Go context.Context 树状级联取消映射
1. **源码触发条件**：C# 源码中使用 `CancellationToken` 并在异步方法间逐层传递。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)）；目标语言 Go 1.27（[GO-PKG-CONTEXT](https://pkg.go.dev/context)）。
3. **原可观察行为**：通过 `CancellationTokenSource.Cancel()` 触发所有下游持有者的取消状态。
4. **目标可选写法和不适用条件**：
   - *可选映射*：函数首参数传入 `ctx context.Context`，在耗时循环或 I/O 中通过 `select { case <-ctx.Done(): return ctx.Err() default: }` 进行响应。
   - *不适用条件*：严禁传递 `nil` context；严禁在子 Goroutine 中忽略 `ctx.Done()` 导致协程泄漏。
5. **错误机械替换反例**：
   ```go
   // 错误：忽略取消信号，导致后台 Goroutine 永远无法退出而内存泄漏
   func Worker(ctx context.Context) {
       for {
           // 错误：没有 select 监听 ctx.Done()
           doStep()
       }
   }
   // 正确：监听 ctx.Done()
   func Worker(ctx context.Context) {
       for {
           select {
           case <-ctx.Done():
               return
           default:
               doStep()
           }
       }
   }
   ```
6. **信息不足或实现相关时的处理**：若源方法具备超时参数，使用 `context.WithTimeout` 生成子 context。
7. **直接官方 HTTPS 依据链接**：[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)；[GO-PKG-CONTEXT](https://pkg.go.dev/context)。

### 规则 CS-GO-04：C# try/finally 与句柄关闭序列向 Go defer 逆序清理映射
1. **源码触发条件**：C# 源码用 `try`/`finally` 手工管理非托管资源，或在多个出口路径上显式调用关闭句柄的方法（`CloseServiceHandle`、`CloseHandle`），或调用 `Marshal.AllocHGlobal` 申请非托管缓冲。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-GC](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals)）；目标语言 Go 1.27（[GO-SPEC #Defer_statements](https://go.dev/ref/spec)）。
3. **原可观察行为**：源构造在每个正常与异常出口上同步执行一次释放；对已为 `IntPtr.Zero` 的句柄先判空再关闭，因此重复清理路径不会产生额外失败，清理时抛出的异常会覆盖原异常。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在资源**成功获取之后**立即 `defer` 释放，多个不同资源各自 `defer`，Go 规范保证按 LIFO 逆序于外层函数返回前执行；需要按取得时的句柄值释放时用 `defer func(h syscall.Handle) { ... }(h)` 以形参捕获当前值。
   - *不适用条件*：严禁把 `defer` 写在长循环体内（它在外层函数返回时才执行，句柄会累积到循环结束）；严禁用 `runtime.SetFinalizer` 顶替显式释放（触发时机不确定、无法保证资源生命周期）；严禁把源语言"同一句柄可能被关闭两次"的容错序列机械改写为两次 `defer` 关闭同一句柄（造成 double-free 或对已释放对象操作）。
5. **错误机械替换反例**：
   ```go
   // C# 原型：IntPtr hToken = IntPtr.Zero; ... finally { if (hToken != IntPtr.Zero) CloseHandle(hToken); }
   var hToken syscall.Handle // nil（0）值
   defer windows.CloseHandle(hToken) // 错误：闭包捕获变量，取的是 defer 执行时的最终值
   if err := openProcessToken(&hToken); err != nil {
       return err // 错误：此处 defer 仍会以 0 句柄调用 CloseHandle
   }
   // 正确：获得有效句柄后再注册释放，且不让 defer 读取可变变量
   if err := openProcessToken(&hToken); err != nil {
       return err
   }
   defer func(h syscall.Handle) { _ = windows.CloseHandle(h) }(hToken)
   ```
6. **信息不足或实现相关时的处理**：若源码中的句柄是否可能重复关闭、或 `CloseHandle` 失败是否需要上报，无法从源码确定，把句柄所有权契约（谁释放、是否允许二次释放）标为待确认再落笔。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Defer_statements](https://go.dev/ref/spec)；[GO-PKG-SYS-WINDOWS](https://pkg.go.dev/golang.org/x/sys/windows)。

### 规则 CS-GO-05：C# UTF-16 字符串长度与 Substring 向 Go 字节/码点边界与 os.Args 索引映射
1. **源码触发条件**：C# 源码用 `string.Length`、`Substring(start, len)`、`IndexOf`/`LastIndexOf` 的返回值做偏移或循环上界，或按字符个数校验命令行参数（`args.Length`、`args[i]`）。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)）；目标语言 Go 1.27（[GO-SPEC #String_types](https://go.dev/ref/spec)、[GO-PKG-UTF8](https://pkg.go.dev/unicode/utf8)）。
3. **原可观察行为**：`string.Length` 计的是 UTF-16 代码单元数，`Substring` 与 `s[i]` 按代码单元定位；BMP 外字符（如 emoji）在 C# 中占 2 个长度单位、1 个用户可见字符。Go 侧 `len(s)` 计 UTF-8 字节、`s[i]` 取单字节，`for range` 按码点迭代，`os.Args[0]` 是程序路径（`len(os.Args)` 为 1 时代表无参数）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：需要"字符个数"时用 `utf8.RuneCountInString(s)` 并显式声明与 C# 的差异；需要按位置截取时统一改用字节下标（`s[3:]`），或先 `[]rune(s)` 再切片；参数校验改为 `len(os.Args) > 1` 并把 `args[i]` 改写为 `os.Args[i+1]`；判断包含关系时优先 `strings.Contains` 而不是 `idx != -1`。
   - *不适用条件*：严禁把 `s[i]`（字节）当作字符访问后再用 `string(...)` 拼接，非 ASCII 输入会被拆成多个无效字节；严禁依赖 `len(s)` 与 C# `Length` 相等（BMP 外字符使 Go 字节数大于 C# 代码单元数，纯 ASCII 时又恰好相等而掩盖问题）。
5. **错误机械替换反例**：
   ```go
   // C# 原型：for (int i = 0; i < args.Length; i++) { ... }
   for i := 0; i < len(os.Args); i++ { // 错误：os.Args 含程序名，且 len 是元素个数而非字节数
       arg := os.Args[i] // 错误：i=0 时取到的是可执行文件路径
       _ = arg
   }
   // 正确：显式跳过程序名，字符/字节语义按需声明
   for _, arg := range os.Args[1:] {
       n := utf8.RuneCountInString(arg) // 码点数；与 C# string.Length 不保证相等
       _ = n
   }
   ```
6. **信息不足或实现相关时的处理**：源字符串是否可能包含 BMP 外字符、源码逻辑究竟按字符还是按字节计数，无法从局部源码判定时，在报告里写明"长度单位未冻结"并请求确认，不得默认两者相等。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #String_types](https://go.dev/ref/spec)；[GO-PKG-UTF8](https://pkg.go.dev/unicode/utf8)；[GO-PKG-OS](https://pkg.go.dev/os)。

### 规则 CS-GO-06：C# object 装箱与 GetType/类型转换向 Go 接口断言与包级错误哨兵映射
1. **源码触发条件**：C# 源码把值类型或引用类型赋给 `object`（装箱容器、异构结果集），用 `GetType().Name` 取运行时类型名，或对接口值做向下转型 `(IList<T>)Results`，并依赖转型失败抛出的 `InvalidCastException` 走错误分支。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）；目标语言 Go 1.27（[GO-SPEC #Type_assertions](https://go.dev/ref/spec)）。
3. **原可观察行为**：每个装箱对象携带精确的运行时类型，`GetType().Name` 返回稳定的类型名字符串，非法向下转型抛 `InvalidCastException`。Go 接口值保存（动态类型, 动态值）二元组，类型断言失败可返回零值加 `false` 而**不 panic**，`==` 比较接口值在动态类型不可比较时 panic，而 nil 指针装进接口后接口本身不是 nil（`iface != nil` 为真）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：容器元素统一为 `any`，读取侧用 `v, ok := x.(T)` 并按 `ok` 分支；需要类型判别时定义自己的 `Kind` 字段或使用 `reflect.TypeOf(x)`；转型失败改为显式返回错误。
   - *不适用条件*：严禁用 `x.(T)` 单值断言代替源语言的"失败分支"（断言失败会 panic，把 `InvalidCastException` 的可捕获失败变成进程崩溃）；严禁把箱装 nil 指针当作 nil 接口判断；严禁把接口值直接当作 map 键而不确认动态类型可比较（不可比较类型会在运行期 panic）。
5. **错误机械替换反例**：
   ```go
   // C# 原型：object Result { get; } ；GetType().Name 作为属性名
   type GenericObjectResult struct{ Result any }
   func (r GenericObjectResult) Name() string { return r.Result.(string) } // 错误：失败即 panic
   // 正确：断言带回退，并显式区分 nil 接口与 nil 指针
   func (r GenericObjectResult) Name() (string, bool) {
       s, ok := r.Result.(string)
       if !ok || r.Result == nil {
           return "", false
       }
       return s, true
   }
   ```
6. **信息不足或实现相关时的处理**：若源类型名被用作序列化键或分支判据，需先确认它在目标侧必须保持的稳定形态（接口、结构体标签还是反射类型名），无法确认时标注为待确认；C# 泛型约束在 Go 泛型约束下无表达方式的部分，在报告中声明为降级。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Type_assertions](https://go.dev/ref/spec)；[GO-PKG-REFLECT](https://pkg.go.dev/reflect)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
