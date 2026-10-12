---
name: csharp-to-cpp
description: Use when converting C# source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → C++ 语言转换规则

> **适用基线**：C# 12 / .NET 8 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C#](../../references/languages/csharp.md)与[目标语言 C++](../../references/languages/cpp.md)，按源码选择适用规则。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C# → C++ 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CS-CPP-01：C# using 资源管理向 C++17 RAII 作用域守护类映射
1. **源码触发条件**：C# 源码中使用 `using (var resource = ...)` 或 `using var` 语句。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-DISPOSE）；目标语言 ISO C++17（WG21-N4659 Clause 6.7）。
3. **原可观察行为**：退出作用域时无论正常分支还是异常，均立即同步调用 `Dispose()`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 C++ 具备确定性析构函数的局部栈对象（RAII 类），或使用包含自定义 Deleter 的 `std::unique_ptr`。
   - *不适用条件*：严禁在 C++ 中将托管资源转换为裸指针后手动调用释放，容易在异常抛出时造成泄漏。
5. **错误机械替换反例**：
   ```cpp
   // 错误：在 C++ 中手动 delete 模拟 using，在发生异常时直接跳过 delete
   void Process() {
       MyResource* res = new MyResource();
       DoAction(); // 若抛出异常，res 发生内存/句柄泄漏！
       delete res;
   }
   // 正确：使用局部栈对象或 unique_ptr
   void Process() {
       auto res = std::make_unique<MyResource>();
       DoAction(); // 异常发生时自动调用析构函数安全释放
   }
   ```
6. **信息不足或实现相关时的处理**：若资源类型为系统文件或套接字，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)。
7. **资料依据（名称/版本/章节）**：MS-CS-DISPOSE；WG21-N4659 Clause 6.7。

### 规则 CS-CPP-02：C# event/delegate 多播事件向 C++ std::function 与观察者容器映射
1. **源码触发条件**：C# 源码中使用 `event Action<T>` 并通过 `+=`/`-=` 进行订阅和注销。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-EVENT）；目标语言 ISO C++17（WG21-N4659 Clause 23.14）。
3. **原可观察行为**：外部调用者无法直接覆写委托链，触发事件时按顺序依次调用所有注册回调。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C++ 中实现一个简易观察者类，内部维护包含 `std::function<void(T)>` 的容器，提供 `subscribe()` 和 `unsubscribe()` 方法，注意捕获对象生命周期避免野指针。
   - *不适用条件*：严禁直接使用裸函数指针数组，无法支持带上下文状态的 lambda 闭包。
5. **错误机械替换反例**：
   ```cpp
   // 错误：使用裸函数指针无法捕获局部上下文
   typedef void (*Callback)(int);
   // 正确：使用 std::function 容器
   class Event {
       std::vector<std::function<void(int)>> handlers;
   public:
       void subscribe(std::function<void(int)> h) { handlers.push_back(h); }
       void invoke(int val) { for (auto& h : handlers) h(val); }
   };
   ```
6. **信息不足或实现相关时的处理**：若涉及多线程触发事件，给观察者容器增加 `std::mutex` 保护。
7. **资料依据（名称/版本/章节）**：MS-CS-EVENT；WG21-N4659 Clause 23.14。

### 规则 CS-CPP-03：C# CancellationToken 协同取消向 C++17 原子标志或条件变量映射
1. **源码触发条件**：C# 源码中使用 `CancellationToken` 并在循环或 I/O 中轮询 `IsCancellationRequested`。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（MS-CS-CANCEL）；目标语言 ISO C++17（WG21-N4659 Clause 32）。
3. **原可观察行为**：IsCancellationRequested 只读状态，不自动抛错；源码可能继续、break、返回或另调用 ThrowIfCancellationRequested。回调/取消树/关联 I/O 按实际使用保留，不把所有取消统一成异常退出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C++17 中使用 `std::shared_ptr<std::atomic<bool>>` 作为停止标志；在条件变量阻塞时配合带谓词的 `wait_for`。
   - *不适用条件*：禁止直接使用 C++20 的 `std::stop_token`（超出冻结 C++17 范围）；严禁使用非原子普通 `bool` 变量跨线程传递取消（触发未定义行为的数据竞争）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：普通 bool 变量跨线程读取引发数据竞争 UB
   bool cancel_requested = false;
   void Worker() { while (!cancel_requested) { ... } } // UB！
   // 正确：使用 std::atomic<bool>
   std::atomic<bool> cancel_requested{false};
   void Worker() { while (!cancel_requested.load(std::memory_order_relaxed)) { ... } }
   ```
6. **信息不足或实现相关时的处理**：取消涉及 I/O 时核源唤醒/取消/关闭机制与目标平台支持，加载并发/网络/系统页；不默认关闭套接字或加 wait_for 超时。状态/异常/回调与唤醒关系未知停该映射。
7. **资料依据（名称/版本/章节）**：MS-CS-CANCEL；WG21-N4659 Clause 32。

### 规则 CS-CPP-04：COM 接口指针的取址与类型双关必须用 SDK 官方访问器

1. **源码触发条件**：C# 源码通过 COM 互操作（`[ComImport]`、`Marshal.GetIUnknownForObject`、`Marshal.QueryInterface`、`IntPtr` 转换）获取或传递接口指针，或在 P/Invoke 里把 `ref IntPtr`/`out IntPtr` 交给需要 `void**` 的原生 API。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8；目标语言 ISO C++17 + WRL/ATL（Microsoft `ComPtr`）。
3. **原可观察行为**：封送器、Marshal 或裸 IntPtr 的引用责任不同，按实际 API 与调用者核；void** 只说明指针层级，不保证回填的是 COM 已加引用接口，QueryInterface 等具体 API 才规定其引用/失败语义。
4. **目标可选写法和不适用条件**：
   - *可选映射*：确实采用 WRL 时核 GetAddressOf（不释放）与 ReleaseAndGetAddressOf（先释放）的输出类型/失败契约；源失败保旧值时可需临时输出后成功再交接。不能只按“替换”二字默认先释放，SDK之外的封装另核其真实接口。
   - *不适用条件*：不得用 `reinterpret_cast<void**>(&ptr)` 直接对 `ComPtr<T>` 取地址——这**绕过**了 WRL 内部的状态跟踪，既可能与断言冲突，也会在替换路径上泄漏旧引用。
5. **错误机械替换反例**：
   ```cpp
   // 错误：直接对 ComPtr 取址做 void** 双关，且未释放现有引用
   ComPtr<IUnknown> sp;
   hr = pUnk->QueryInterface(__uuidof(IFoo), reinterpret_cast<void**>(&sp));
   // → 绕过 WRL 跟踪；若 sp 原本非空，旧引用泄漏

   // 条件候选：输出 ComPtr 类型须与查询的接口 IID 对应，宏产生匹配的 IID/void**
   ComPtr<IFoo> output; // 已确认空且 IFoo/SDK 可用时
   hr = pUnk->QueryInterface(IID_PPV_ARGS(output.GetAddressOf()));
   // 对已有值的替换另核失败后保留/释放契约，不把 ReleaseAndGetAddressOf 作为默认。
   ```
6. **信息不足或实现相关时的处理**：持有引用、输出参数覆盖/失败后保留与释放时点未知时停止该映射并核调用契约；不得默认 ReleaseAndGetAddressOf，提前释放可能改变源失败后的对象存活与状态。各访问器是按所有权/出参契约选择的候选，不按“多释放更安全”猜测。
7. **资料依据（名称/版本/章节）**：`Microsoft::WRL::ComPtr`、`ComPtr::GetAddressOf`、`ComPtr::ReleaseAndGetAddressOf`；Microsoft `QueryInterface`)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
