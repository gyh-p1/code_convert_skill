---
name: csharp-to-go
description: Use when converting C# source to Go; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → Go 语言转换规则

> **适用基线**：C# 12 / .NET 8 → Go 1.27。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C#](../../references/languages/csharp.md)与[目标语言 Go](../../references/languages/go.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 C# → Go 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CS-GO-01：C# 异常体系向 Go 显式 (T, error) 多返回值映射
1. **源码触发条件**：C# 源码中使用 `throw` 抛出异常并在多层上层通过 `try-catch` 捕获。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-EXCEPT）；目标语言 Go 1.27（GO-SPEC #Errors）。
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
7. **资料依据（名称/版本/章节）**：MS-CS-EXCEPT；GO-SPEC #Errors。

### 规则 CS-GO-02：C# using/IDisposable 向 Go defer 逆序资源清理映射
1. **源码触发条件**：C# 源码中使用 `using` 语句管理文件、互斥锁或连接生命周期。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-DISPOSE）；目标语言 Go 1.27（GO-SPEC #Defer_statements）。
3. **原可观察行为**：离开作用域时无论如何立即调用 `Dispose()`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：函数级 using 的退出点与当前 Go 函数返回相同时可用 defer；块级 using/try-finally 不能直接移到外层函数末。可考虑对应作用域的目标函数或显式退出处理，但须保持原 return/异常传播、状态和 Dispose 失败；Close 返回值不默认忽略或升级。
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
6. **信息不足或实现相关时的处理**：多资源取得失败、逆序释放、释放自身失败和异常覆盖按源逐路径核对；作用域/失败传播未知时停止该映射，不以函数级 defer 或默认全部忽略定案。
7. **资料依据（名称/版本/章节）**：MS-CS-DISPOSE；GO-SPEC #Defer_statements。

### 规则 CS-GO-03：C# CancellationToken 向 Go context.Context 树状级联取消映射
1. **源码触发条件**：C# 源码中使用 `CancellationToken` 并在异步方法间逐层传递。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-CANCEL）；目标语言 Go 1.27（GO-PKG-CONTEXT）。
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
7. **资料依据（名称/版本/章节）**：MS-CS-CANCEL；GO-PKG-CONTEXT。

### 规则 CS-GO-04：C# try/finally 与句柄关闭序列向 Go defer 逆序清理映射
1. **源码触发条件**：C# 源码用 `try`/`finally` 手工管理非托管资源，或在多个出口路径上显式调用关闭句柄的方法（`CloseServiceHandle`、`CloseHandle`），或调用 `Marshal.AllocHGlobal` 申请非托管缓冲。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-GC）；目标语言 Go 1.27（GO-SPEC #Defer_statements）。
3. **原可观察行为**：源构造在每个正常与异常出口上同步执行一次释放；对已为 `IntPtr.Zero` 的句柄先判空再关闭，因此重复清理路径不会产生额外失败，清理时抛出的异常会覆盖原异常。
4. **目标可选写法和不适用条件**：
   - *可选映射*：仅源 finally 的退出点对应当前函数返回时，在资源成功获取后登记 defer；内层 finally 应在原对应点执行。多个动作按实际注册与 LIFO 对应，取得时的句柄可用 defer 形参保存；源重复关闭、容错/返回值及失败覆盖须保留，不自动去重或加关闭。
   - *不适用条件*：defer 的函数级时点不代块级 finally，Finalizer 不代源显式释放；源确有重复关闭/容错序列时核每次条件、哨兵、调用失败与句柄复用，不任意合并、去重或再加 defer，既有风险单列。
5. **错误机械替换反例**：
   ```go
   // C# 原型：IntPtr hToken = IntPtr.Zero; ... finally { if (hToken != IntPtr.Zero) CloseHandle(hToken); }
   var hToken syscall.Handle // nil（0）值
   defer windows.CloseHandle(hToken) // 错误：此刻参数已求值为 0，后续赋值不会更新已保存的参数
   if err := openProcessToken(&hToken); err != nil {
       return err // 错误：此处 defer 仍会以 0 句柄调用 CloseHandle
   }
   // 有条件的映射：源释放点为函数退出时，获得有效句柄后再注册释放
   if err := openProcessToken(&hToken); err != nil {
       return err
   }
   defer func(h syscall.Handle) { _ = windows.CloseHandle(h) }(hToken)
   ```
6. **信息不足或实现相关时的处理**：若源码中的句柄是否可能重复关闭、或 `CloseHandle` 失败是否需要上报，无法从源码确定，把句柄所有权契约（谁释放、是否允许二次释放）标为待确认再落笔。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Defer_statements；GO-PKG-SYS-WINDOWS。

### 规则 CS-GO-05：C# UTF-16 字符串长度与 Substring 向 Go 字节/码点边界与 os.Args 索引映射
1. **源码触发条件**：C# 源码用 `string.Length`、`Substring(start, len)`、`IndexOf`/`LastIndexOf` 的返回值做偏移或循环上界，或按字符个数校验命令行参数（`args.Length`、`args[i]`）。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-STRING）；目标语言 Go 1.27（GO-SPEC #String_types、GO-PKG-UTF8）。
3. **原可观察行为**：`string.Length` 计的是 UTF-16 代码单元数，`Substring` 与 `s[i]` 按代码单元定位；BMP 外字符（如 emoji）在 C# 中占 2 个长度单位、1 个用户可见字符。Go 侧 `len(s)` 计 UTF-8 字节、`s[i]` 取单字节，`for range` 按码点迭代，`os.Args[0]` 是程序路径（`len(os.Args)` 为 1 时代表无参数）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按两语言页的字符串单位保持UTF-16代码单元长度、索引和截取；RuneCount、[]rune及字节下标均不直接等价。只有源输入域/消费者已证明相应单位一致时才采用简化表示；孤立代理项等在目标表示中不能保持的情况须定位缺口，不靠“声明差异”继续。命令行数组另按不含/含程序名联合映射计数、守卫及全部下标；只有源确为包含关系且比较规则一致时才考虑strings.Contains，源消费位置值则仍须保持其单位。
   - *不适用条件*：严禁把 `s[i]`（字节）当作字符访问后再用 `string(...)` 拼接，非 ASCII 输入会被拆成多个无效字节；严禁依赖 `len(s)` 与 C# `Length` 相等（BMP 外字符使 Go 字节数大于 C# 代码单元数，纯 ASCII 时又恰好相等而掩盖问题）。
5. **错误机械替换反例**：
   ```go
   // C# 原型：for (int i = 0; i < args.Length; i++) { ... }
   for i := 0; i < len(os.Args); i++ { // 错误：os.Args 含程序名，且 len 是元素个数而非字节数
       arg := os.Args[i] // 错误：i=0 时取到的是可执行文件路径
       _ = arg
   }
   // 局部示意：仅展示跳过程序名，不能据此决定字符串长度/下标表示
   for _, arg := range os.Args[1:] {
       _ = arg // 长度、截取及错误路径另按源的UTF-16单位对应
   }
   ```
6. **信息不足或实现相关时的处理**：源字符串是否可能包含 BMP 外字符、源码逻辑究竟按字符还是按字节计数，无法从局部源码判定时，在报告里写明"长度单位未冻结"并请求确认，不得默认两者相等。
7. **资料依据（名称/版本/章节）**：GO-SPEC #String_types；GO-PKG-UTF8；GO-PKG-OS。

### 规则 CS-GO-06：C# object 装箱与 GetType/类型转换向 Go 接口断言与包级错误哨兵映射
1. **源码触发条件**：C# 源码把值类型或引用类型赋给 `object`（装箱容器、异构结果集），用 `GetType().Name` 取运行时类型名，或对接口值做向下转型 `(IList<T>)Results`，并依赖转型失败抛出的 `InvalidCastException` 走错误分支。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-SPEC）；目标语言 Go 1.27（GO-SPEC #Type_assertions）。
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
6. **信息不足或实现相关时的处理**：源类型名被用作序列化键或分支判据时，核实际消费者所需稳定形态，未知则停止受影响映射并记缺口。泛型约束不能直接表达时，先核实例集合、接受域及运行时检查是否可保持；不能仅报告降级就删除源约束，采用不同语义须有生成前许可。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Type_assertions；GO-PKG-REFLECT。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
