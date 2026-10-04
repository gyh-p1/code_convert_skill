---
name: cpp-to-csharp
description: Use when converting C++ source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → C# 语言转换规则

> **适用基线**：ISO C++17 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C++](../../references/languages/cpp.md)与[目标语言 C#](../../references/languages/csharp.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/cpp-to-csharp/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C++ → C# 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-CS-01：C++ RAII 确定性析构向 C# IDisposable 与 using 作用域映射
1. **源码触发条件**：C++ 源码中依赖对象析构函数（RAII）管理内存外的系统资源（句柄、文件、锁）。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 C# 12 / .NET 8（[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）。
3. **原可观察行为**：对象离开局部作用域时逆序、确定性执行析构函数。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C# 中实现 `IDisposable` 接口，在调用点使用 `using var res = new ...` 或 `using (...)` 确保退出作用域时调用 `Dispose()`。
   - *不适用条件*：严禁将 C++ 析构函数机械翻译为 C# 析构函数（Finalizer：`~ClassName()`），因为 CLR 终结器执行时机非确定，会导致资源锁定与泄漏。
5. **错误机械替换反例**：
   ```csharp
   // 错误：将 C++ 析构函数直接翻译为 C# Finalizer
   public class MutexLock {
       private readonly object _lock;
       public MutexLock(object l) { _lock = l; Monitor.Enter(_lock); }
       ~MutexLock() { Monitor.Exit(_lock); } // 致命错误：GC 跨线程触发导致死锁或异常！
   }
   // 正确：使用 IDisposable 保证同步释放
   public sealed class MutexLock : IDisposable {
       private readonly object _lock;
       public MutexLock(object l) { _lock = l; Monitor.Enter(_lock); }
       public void Dispose() { Monitor.Exit(_lock); }
   }
   ```
6. **信息不足或实现相关时的处理**：若源类仅为纯内存数据结构，交由 GC 托管，无需强制实现 `IDisposable`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)；[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 CPP-CS-02：C++ 多重继承与虚基类向 C# 单继承加接口组合映射
1. **源码触发条件**：C++ 源码中派生类同时继承两个或多个非纯抽象基类。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 13](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：C++ 对象内存布局包含多个基类子对象，支持交叉向任意基类指针类型转换。
4. **目标可选写法和不适用条件**：
   - *可选映射*：选择一个主基类继承，其余基类转换为接口（`interface`），派生类内部通过内嵌组件对象并转发接口方法（组合优于继承）。
   - *不适用条件*：C# 语法不支持类多重继承，严禁使用任何黑魔法尝试模拟多基类字段直接合并。
5. **错误机械替换反例**：
   ```csharp
   // 错误：C# 编译器直接拒绝多类继承
   // public class Derived : BaseA, BaseB { } // 编译报错：CS1721 类不能有多个基类
   // 正确：接口加组合模式
   public interface IBaseB { void ActionB(); }
   public class Derived : BaseA, IBaseB {
       private readonly BaseB _b = new();
       public void ActionB() => _b.ActionB();
   }
   ```
6. **信息不足或实现相关时的处理**：若接口存在默认实现依赖，记录抽象层次降级并在转换日志中说明。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)。

### 规则 CPP-CS-03：C++ std::future/std::thread 向 C# Task-based Asynchronous Pattern (TAP) 映射
1. **源码触发条件**：C++ 源码中使用 `std::async` 或 `std::future::get()` 等待异步结果。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 33.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)）。
3. **原可观察行为**：`get()` 阻塞调用线程直至后台线程计算完成并返回值。
4. **目标可选写法和不适用条件**：
   - *可选映射*：方法重构为 `async Task<T>`，使用 `await` 进行非阻塞等待，协同取消通过 `CancellationToken` 级联传递。
   - *不适用条件*：严禁在 ASP.NET Core 或 UI 上下文中直接调用 `task.Result` 模拟同步 `get()`，极易导致死锁。
5. **错误机械替换反例**：
   ```csharp
   // 错误：机械模拟 future::get() 造成死锁
   public int Calculate() {
       return ComputeAsync().Result; // 错误：在特定同步上下文引发死锁
   }
   // 正确：使用完整 async/await 调用链
   public async Task<int> CalculateAsync() {
       return await ComputeAsync();
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及底层线程优先级设置，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
