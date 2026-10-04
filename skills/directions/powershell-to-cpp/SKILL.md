---
name: powershell-to-cpp
description: Use when converting PowerShell source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → C++ 语言转换规则

> **适用基线**：PowerShell 7.6 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/powershell-to-cpp/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 PowerShell → C++ 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PS-CPP-01：PowerShell 脚本块 (ScriptBlock) 向 C++17 lambda 闭包映射
1. **源码触发条件**：PowerShell 源码中使用 `{ param($x) $x * 2 }` 定义脚本块并作为参数传递。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6；目标语言 ISO C++17（[WG21-N4659 Clause 8.1.5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：脚本块延迟调用，可访问并修改调用栈上下文变量。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 C++17 lambda 表达式，通用存储使用 `std::function<R(Args...)>`；若涉及局部引用捕获 `[&]`，必须保证 lambda 生命周期不超过被捕获变量的作用域。
   - *不适用条件*：严禁将持有引用捕获 `[&]` 的 lambda 跨线程传递或脱离作用域返回（会导致悬挂引用解引用 UB）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：引用捕获局部变量后逃逸，引发悬垂引用未定义行为
   std::function<int()> MakeAdder(int x) {
       return [&x]() { return x + 1; }; // 严重错误：x 是局部形参，函数退出后引用失效！
   }
   // 正确：使用值捕获 [=] 或显式转移
   std::function<int()> MakeAdder(int x) {
       return [x]() { return x + 1; };
   }
   ```
6. **信息不足或实现相关时的处理**：若脚本块动态修改了外层作用域变量，在转换报告中标明生命周期约束。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 8.1.5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PS-CPP-02：PowerShell 终止错误向 C++17 结构化异常体系映射
1. **源码触发条件**：PowerShell 源码中使用 `throw "Error message"` 或捕捉到终止错误。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）；目标语言 ISO C++17（[WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：终止当前执行管道，向上回溯调用栈。
4. **目标可选写法和不适用条件**：
   - *可选映射*：抛出继承自 `std::exception` 的 C++ 异常（如 `std::runtime_error("...")`），上层使用 `try ... catch` 捕获。
   - *不适用条件*：严禁抛出非 `std::exception` 派生的裸字符串或整数字面量（如 `throw "err";`），违背 C++ 现代异常安全规范。
5. **错误机械替换反例**：
   ```cpp
   // 错误：抛出裸字符串字面量，难以进行统一的多态异常捕获
   throw "operation failed"; // 无法被 catch (const std::exception&) 捕获！
   // 正确：抛出标准异常派生类
   throw std::runtime_error("operation failed");
   ```
6. **信息不足或实现相关时的处理**：若需要还原 PowerShell 的原生报错格式，封装包含错误信息的派生异常类。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)；[WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PS-CPP-03：PowerShell ForEach-Object -Parallel 向 C++17 线程池与同步映射
1. **源码触发条件**：PowerShell 源码中使用 `$items | ForEach-Object -Parallel { ... }` 并发处理。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）；目标语言 ISO C++17。
3. **原可观察行为**：利用 Runspace 线程池在多个线程并发执行脚本块。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `std::async(std::launch::async, ...)` 配合 `std::future`，或使用固定工作线程池；共享资源使用 `std::mutex` 保护。
   - *不适用条件*：严禁在无同步原语下并发写入 C++ 容器（如 `std::vector::push_back`），直接引发内存重配数据竞争崩溃。
5. **错误机械替换反例**：
   ```cpp
   // 错误：多线程无锁并发 push_back
   std::vector<int> out;
   // 多个线程同时 out.push_back(val); // 致命崩溃：内部缓冲区重分配数据竞争！
   // 正确：加锁保护
   std::mutex mtx;
   {
       std::lock_guard<std::mutex> lock(mtx);
       out.push_back(val);
   }
   ```
6. **信息不足或实现相关时的处理**：若代码涉及操作系统线程亲和性，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)；[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
