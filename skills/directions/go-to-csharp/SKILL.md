---
name: go-to-csharp
description: Use when converting Go source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → C# 语言转换规则

> **适用基线**：Go 1.27 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 C#](../../references/languages/csharp.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/go-to-csharp/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Go → C# 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-CS-01：Go 结构体值传递向 C# struct/class 语义划分映射
1. **源码触发条件**：Go 源码中定义 `type Data struct` 并以值接收者 `func (d Data)` 传参。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Struct_types](https://go.dev/ref/spec)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：纯值复制，方法内修改 `d` 不影响外部调用者。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若需保持全量值复制且数据结构较小，声明为 C# `struct`；若为大对象或需支持引用语义，声明为 `class` 并在传参时显式创建副本。
   - *不适用条件*：严禁将值接收者方法所在结构体无脑翻译为 `class`，否则后续调用会产生意外的别名修改副作用。
5. **错误机械替换反例**：
   ```csharp
   // 错误：将 Go 值类型结构体映射为 C# class 导致方法内修改污染外部
   public class Config {
       public int Timeout;
       public void SetTimeout(int t) { this.Timeout = t; }
   }
   // Go 原型为值接收者，调用后外部 Config 未变；C# class 会直接修改外部对象！
   // 正确：使用 struct 保持值语义
   public struct Config {
       public int Timeout;
   }
   ```
6. **信息不足或实现相关时的处理**：若结构体包含大量字段，标记性能权衡并提示用户选择。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)；[GO-SPEC #Struct_types](https://go.dev/ref/spec)。

### 规则 GO-CS-02：Go error 返回向 C# 结构化异常抛出映射
1. **源码触发条件**：Go 源码中使用 `return nil, errors.New("not found")`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）。
3. **原可观察行为**：调用方必须显式判断 `err != nil`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为抛出对应的 C# 异常（如 `throw new KeyNotFoundException(...)`）；或者若该错误属于频繁发生的常规分支，提供形如 `bool TryGetValue(...)` 的 Try 模式方法。
   - *不适用条件*：严禁将业务失败静默忽略。
5. **错误机械替换反例**：
   ```csharp
   // 错误：为了强行对应多返回值，在 C# 中返回二元元组且不加强制检查
   public (User, string) FindUser(int id) { ... } // 违背 C# 习惯用法
   // 正确：使用常规异常或 Try 模式
   public bool TryFindUser(int id, out User user) { ... }
   ```
6. **信息不足或实现相关时的处理**：若源错误代码作为系统进程返回码，映射为带退出码的异常。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)。

### 规则 GO-CS-03：Go context.Context 取消树向 C# CancellationTokenSource 映射
1. **源码触发条件**：Go 源码中使用 `ctx, cancel := context.WithCancel(parentCtx)` 并通过 `<-ctx.Done()` 监听取消。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-PKG-CONTEXT](https://pkg.go.dev/context)）；目标语言 C# 12 / .NET 8（[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)）。
3. **原可观察行为**：父 context 取消级联触发所有衍生子 context 的 Done 通道关闭。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `CancellationTokenSource.CreateLinkedTokenSource(parentToken)` 构造级联取消令牌源，向异步方法传递 `cts.Token`。
   - *不适用条件*：必须注意 `CancellationTokenSource` 实现了 `IDisposable`，必须在使用完成后显式调用 `Dispose()` 释放底层定时器或句柄资源。
5. **错误机械替换反例**：
   ```csharp
   // 错误：使用带超时的 CTS 未释放导致定时器资源泄漏
   public async Task RunWithTimeout() {
       var cts = new CancellationTokenSource(1000); // 实现了 IDisposable！
       await DoWorkAsync(cts.Token);
       // 缺少 cts.Dispose()！
   }
   // 正确：使用 using 语句
   public async Task RunWithTimeout() {
       using var cts = new CancellationTokenSource(1000);
       await DoWorkAsync(cts.Token);
   }
   ```
6. **信息不足或实现相关时的处理**：若 context 携带 Value 数据，转换为基于 `AsyncLocal<T>` 或显式参数传递。
7. **直接官方 HTTPS 依据链接**：[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)；[GO-PKG-CONTEXT](https://pkg.go.dev/context)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
