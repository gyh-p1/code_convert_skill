---
name: c-to-csharp
description: Use when converting C source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C → C# 语言转换规则

> **适用基线**：ISO C11 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C](../../references/languages/c.md)与[目标语言 C#](../../references/languages/csharp.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/c-to-csharp/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C → C# 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 C-CS-01：C 结构体裸指针与定宽整数向 C# struct/class 划分与 checked 上下文映射
1. **源码触发条件**：C 源码中定义包含数值或数组的结构体并按值传递，或存在定宽无符号整数回绕算术计算。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（[WG14-N1570 §6.2.5, §6.2.6.2](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types), [MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)）。
3. **原可观察行为**：C 结构体赋值与传参为全量字节值拷贝；无符号整数运算严格按模 $2^n$ 截断回绕；有符号溢出为 UB。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若需保留值传递与无 GC 堆分配语义，声明为 C# `struct`；若需表达多态或共享引用，声明为 `class`；整数回绕计算在默认 `unchecked` 上下文中执行，若需强校验则使用 `checked` 语句。
   - *不适用条件*：严禁将所有 C 结构体机械映射为 C# `class`，否则后续传参变为引用别名，原独立副本被修改导致非预期副作用。
5. **错误机械替换反例**：
   ```csharp
   // 错误：机械映射为 class 导致传参产生别名共享修改
   public class Point { public int X; public int Y; }
   void Offset(Point p) { p.X += 10; } // 修改了外部传入的原始对象！
   // 正确：使用 struct 保持值传递独立性
   public struct Point { public int X; public int Y; }
   ```
6. **信息不足或实现相关时的处理**：若无法确认结构体是否跨线程共享，应向用户标记所有权模型未决并默认采用 `struct`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)；[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)。

### 规则 C-CS-02：C 错误指示码与 errno 向 C# 结构化异常与 using/IDisposable 映射
1. **源码触发条件**：C 源码中使用负数或非零返回码指示操作失败，或依赖显式资源关闭函数（如 `free`, `close`）。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/), [MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）。
3. **原可观察行为**：调用方通过 `if (ret < 0)` 检查并手动跳转清理；操作系统错误通过 `errno` 暴露。
4. **目标可选写法和不适用条件**：
   - *可选映射*：底层严重失败转换为抛出派生自 `System.Exception` 的结构化异常（如 `InvalidOperationException`）；封装非托管资源的对象必须实现 `IDisposable` 并配合 `using` 语句释放。
   - *不适用条件*：严禁将 C 的所有返回码机械忽略或仅作为返回值而不加检查；严禁将析构逻辑置于 Finalizer 中期待即时执行。
5. **错误机械替换反例**：
   ```csharp
   // 错误：非内存资源未实现 IDisposable，导致句柄泄漏直到不可预期的 GC Finalizer
   public class NativeBuffer {
       private IntPtr _buf;
       ~NativeBuffer() { FreeNative(_buf); } // 错误：执行时机完全不确定！
   }
   // 正确：实现 IDisposable 并在 using 中确定性释放
   public sealed class NativeBuffer : IDisposable {
       private IntPtr _buf;
       public void Dispose() { FreeNative(_buf); GC.SuppressFinalize(this); }
   }
   ```
6. **信息不足或实现相关时的处理**：若出现文件/套接字操作，说明语言层资源释放契约后加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md) 或 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)；[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)。

### 规则 C-CS-03：C 标志位/信号量同步向 C# Task/async-await 与 CancellationToken 映射
1. **源码触发条件**：C 源码中使用 volatile 标志位循环轮询或条件变量等待操作终止。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（[WG14-N1570 §7.17](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）；目标语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/), [MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)）。
3. **原可观察行为**：C 线程阻塞在等待循环或信号量上，通过原子修改标志位通知退出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重构为异步方法返回 `Task`，接收 `CancellationToken` 参数，调用 `token.ThrowIfCancellationRequested()` 或使用异步等待 `Task.Delay(..., token)`。
   - *不适用条件*：严禁在 C# 中使用无休止的 `while (!flag)` 忙等待占用线程池线程；严禁在异步上下文中调用 `.Result` 或 `.Wait()`，可能引发死锁。
5. **错误机械替换反例**：
   ```csharp
   // 错误：在异步上下文中阻塞等待导致死锁或线程耗尽
   public void Process() {
       var task = DoWorkAsync();
       task.Wait(); // 错误：在特定同步上下文中极易引发死锁
   }
   // 正确：使用 await 并传递取消令牌
   public async Task ProcessAsync(CancellationToken token) {
       await DoWorkAsync(token);
   }
   ```
6. **信息不足或实现相关时的处理**：若源代码涉及操作系统原生线程创建，加载 [`skills/systems/posix-windows-threads/SKILL.md`](../../systems/posix-windows-threads/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)；[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
