---
name: csharp-to-cpp
description: Use when converting C# source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → C++ 语言转换规则

> **适用基线**：C# 12 / .NET 8 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C#](../../references/languages/csharp.md)与[目标语言 C++](../../references/languages/cpp.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

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

### 规则 CS-CPP-05：C# 值类型/引用类型与 `Nullable<T>` 向 C++ 值对象、智能指针与 `std::optional` 映射
1. **源码触发条件**：C# 源码区分值类型 `struct`、引用类型 `class`、可空值类型 `T?`（`Nullable<T>`），或包含树/图节点互相引用。
2. **冻结版本/运行时/API 前提**：C# 12 / .NET 8 → ISO C++17（`<memory>`、`<optional>`）。
3. **原可观察行为**：`struct` 赋值独立拷贝字段；`class` 变量共享同一堆对象身份且可为 `null`，由 GC 处理环状引用；`Nullable<T>` 用 `HasValue`/`Value` 或 `??` 区分缺失与 `default(T)`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`struct`（含记录值类型 `record struct`）优先映射为 C++ 值类型 `struct`；独占所有权的堆对象用 `std::unique_ptr<T>`，共享身份才用 `std::shared_ptr<T>`，存在双向/回指边时反向指针必须使用 `std::weak_ptr<T>` 或明确生命周期安全的非拥有裸指针/观察指针；可空值类型映射为 `std::optional<T>`，解引用前检查 `has_value()`。
   - *不适用条件*：严禁把互相引用的对象图全部写成 `std::shared_ptr`（C++ 引用计数无法回收环路，必定内存泄漏）；严禁对 C# 可为 `null` 的字段在 C++ 改成非空值拷贝而丢失空语义。
5. **错误机械替换反例**：
   ```cpp
   // 错误：将 C# 双向父子节点全部写成 shared_ptr，形成永久引用环泄漏
   struct Node {
       std::shared_ptr<Node> parent;
       std::vector<std::shared_ptr<Node>> children;
   };

   // 正确：向下独占或共享所有权，向上回指使用 weak_ptr 防环
   struct Node {
       std::weak_ptr<Node> parent;
       std::vector<std::shared_ptr<Node>> children;
   };
   ```
6. **信息不足或实现相关时的处理**：涉及多线程共享指针写入同一字段时另核原子访问或互斥保护（见 `concurrency` 场景）。
7. **资料依据（名称/版本/章节）**：MS-CS 语言规范 Types；WG21-N4659 Clause 23.6 (`optional`)、Clause 23.11 (`memory`)。

### 规则 CS-CPP-06：C# 不可变 UTF-16 `string` 与 `Encoding` 字节边界向 C++ 字符串映射
1. **源码触发条件**：C# 源码访问 `s.Length`、字符下标 `s[i]`、切片 `Substring`、`Encoding.UTF8.GetBytes` 或依赖字符串不可变共享。
2. **冻结版本/运行时/API 前提**：C# 12 / .NET 8 → ISO C++17（`std::string`、`std::u16string`、`L1-CS-09`）。
3. **原可观察行为**：C# `string` 是**不可变 UTF-16 代码单元序列**；`Length` 计 UTF-16 单元数（补充平面字符如 U+1F600 计为 2），且传参复制引用但绝不会因别处“修改”改变内容。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在明确字符串只按 UTF-8 传递且不按 UTF-16 代码单元下标/长度截断时可用 `std::string`（传递用 `const std::string&` 或值复制防别名修改）；若业务直接依赖 UTF-16 代码单元计数、`char`（16 位）下标或独立代理项边界，必须映射为 `std::u16string`（或显式 UTF-16 ↔ UTF-8 换算），不直接用 UTF-8 `std::string::size()` 代替 `Length`。
   - *不适用条件*：严禁将 C# `string` 的不可变共享简化成 C++ 非 const 引用 `std::string&` 后原地修改；严禁混淆 `string.Length`（UTF-16 单元）与 UTF-8 字节数。
5. **错误机械替换反例**：
   ```cpp
   // 错误：把 C# s.Length <= 10 的校验直接写成 UTF-8 std::string::size() <= 10
   // 对 4 个 U+1F600：C# Length == 8 (通过)，UTF-8 bytes == 16 (错误拒绝！)
   bool validate(const std::string& utf8) {
       return utf8.size() <= 10;
   }
   // 正确（当源按 UTF-16 代码单元计长时）：使用 std::u16string 或准确 UTF-16 计数函数
   bool validate_u16(const std::u16string& u16) {
       return u16.size() <= 10;
   }
   ```
6. **信息不足或实现相关时的处理**：遇到含无效代理项或编码替换容错的路径时按 `L1-CS-09` 标注并保持源拒绝/替换策略。
7. **资料依据（名称/版本/章节）**：.NET `System.String`、`Encoding`；WG21-N4659 Clause 24.3。

### 规则 CS-CPP-07：C# `checked` / `unchecked` 整数溢出语义向 C++17 无 UB 算术映射
1. **源码触发条件**：C# 源码在 `checked`/`unchecked` 上下文或默认上下文中执行有符号整数加减乘除/强转，或哈希/位运算依赖补码回绕，或期待 `OverflowException`。
2. **冻结版本/运行时/API 前提**：C# 12 / .NET 8 → ISO C++17（WG21-N4659 Clause 8 / `<cstdint>`）。
3. **原可观察行为**：C# 默认/显式 `unchecked` 下有符号整数溢出按确定性二补码回绕（无异常、非未定义行为）；`checked` 上下文溢出必定抛出 `OverflowException`（包含 `int.MinValue / -1`）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`unchecked` 有符号回绕运算必须在 C++ 中先转为对应宽度的**无符号类型**（如 `uint32_t`、`uint64_t`）执行模 $2^W$ 算术后再转换回目标有符号宽度（避免编译器优化假设无有符号溢出）；`checked` 上下文必须在运算前做显式范围校验并转入异常/错误路径。
   - *不适用条件*：严禁将 C# `unchecked` 有符号溢出加减乘直接写成 C++ `int` / `int64_t` 运算——在 C++17 中有符号整数溢出属于**未定义行为（UB）**，优化器可直接删掉溢出检查分支！
5. **错误机械替换反例**：
   ```cpp
   // 错误：直接用 C++ int32_t 做 C# unchecked 补码回绕乘法，触发有符号溢出 UB
   int32_t hash_step(int32_t h, int32_t x) {
       return h * 31 + x; // C++ 有符号溢出是 UB，与 C# 确定性 32 位回绕不等价！
   }

   // 正确：在对应宽度无符号类型下执行确定性模算术，再显式转回
   int32_t hash_step(int32_t h, int32_t x) {
       uint32_t uh = static_cast<uint32_t>(h);
       uint32_t ux = static_cast<uint32_t>(x);
       return static_cast<int32_t>(uh * 31u + ux);
   }
   ```
6. **信息不足或实现相关时的处理**：工程若显式开启 `<CheckForOverflowUnderflow>true</CheckForOverflowUnderflow>` 改变全局默认策略，冻结工程配置后再选对应映射。
7. **资料依据（名称/版本/章节）**：MS-CS `checked`/`unchecked` 语句；WG21-N4659 Clause 6.9.1/8。

### 规则 CS-CPP-08：C# `try / catch / finally` 向 C++17 RAII 清理守卫与析构异常边界映射
1. **源码触发条件**：C# 源码使用 `try { ... } finally { ... }` 或 `try { ... } catch { ... } finally { ... }` 执行必经清理逻辑。
2. **冻结版本/运行时/API 前提**：C# 12 / .NET 8 → ISO C++17（WG21-N4659 Clause 15.4 / 18.2）。
3. **原可观察行为**：离开 `try` 或 `catch` 块前必定同步执行 `finally` 块；若 `finally` 内抛异常，会覆盖先前挂起异常继续向外传播。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用轻量作用域守卫（ScopeGuard / RAII 类）承接 `finally` 中的非抛出清理动作。若 `finally` 逻辑本身在正常路径可能抛出业务异常，正常分支应在作用域末尾显式执行可抛清理（在析构函数外）；在析构守卫内部则只在栈展开期间执行不抛出清理并妥善防护，决不让异常从 C++ 析构函数逃逸。
   - *不适用条件*：C++17 析构函数**默认隐式为 `noexcept(true)`**；严禁把原本可能抛异常的 C# `finally` 块直接放进 C++ 析构函数而不拦截异常——一旦抛出，C++ 运行时将直接调用 `std::terminate()` 强杀进程！
5. **错误机械替换反例**：
   ```cpp
   // 错误：在 C++ RAII 析构中直接抛出异常（模拟 C# finally flush 失败抛异常）
   struct FinallyGuard {
       ~FinallyGuard() {
           flush_or_throw(); // 若抛出异常，默认 noexcept(true) 直接触发 std::terminate() 崩溃！
       }
   };
   ```
6. **信息不足或实现相关时的处理**：若业务要求保留“正常结束和异常退出时不同的清理/覆盖异常语义”，按 `std::uncaught_exceptions()`（C++17）分别处理正常路径与展开路径并写明测试未验证范围。
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 15.4（Exception specifications）、`std::uncaught_exceptions`；MS-CS `try-finally`。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
