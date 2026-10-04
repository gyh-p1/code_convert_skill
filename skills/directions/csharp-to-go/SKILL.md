---
name: csharp-to-go
description: Use when converting C# source to Go; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → Go 语言转换规则

> **适用基线**：C# 12 / .NET 8 → Go 1.27。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/csharp-to-go/README.md)；候选、冻结任务与第三方回传须分层记录。
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
