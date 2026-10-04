---
name: go-to-cpp
description: Use when converting Go source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → C++ 语言转换规则

> **适用基线**：Go 1.27 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 C++](../../references/languages/cpp.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/go-to-cpp/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Go → C++ 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-CPP-01：Go (T, error) 显式多返回值向 C++17 自定义 Result 结构体或 std::optional 映射
1. **源码触发条件**：Go 源码中函数返回 `(Result, error)`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec)）；目标语言 ISO C++17（[WG21-N4659](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：显式多值返回，调用方通过 `if err != nil` 检查错误。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若只需表达有无数据，使用 `std::optional<T>`；若需携带错误细节，定义 `struct ResultOrError { T val; std::string error_msg; bool ok; }` 或使用输出参数；或者在失败时抛出异常。
   - *不适用条件*：严禁在 C++17 中使用 `std::expected`（C++23 特性，超出冻结规范）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：在 C++17 基线代码中使用 C++23 的 std::expected
   // std::expected<int, std::string> Divide(int a, int b); // 编译报错：C++17 无此特性！
   // 正确：使用带状态结构体或 std::optional
   struct Result { int value; std::string err; bool is_ok() const { return err.empty(); } };
   ```
6. **信息不足或实现相关时的处理**：若原 Go 代码无错误传递直接返回，直接映射为 C++ 对应单一返回值。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Errors](https://go.dev/ref/spec)；[WG21-N4659 Clause 23.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 GO-CPP-02：Go defer 逆序清理向 C++17 局部作用域析构 (RAII) 映射
1. **源码触发条件**：Go 源码中使用 `defer mu.Unlock()` 或 `defer file.Close()`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Defer_statements](https://go.dev/ref/spec)）；目标语言 ISO C++17（[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：注册的清理函数在外层函数返回前以 LIFO（后进先出）逆序确定性执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：互斥锁使用 `std::lock_guard`；文件/资源封装为 RAII 守卫类；或编写简易 ScopeGuard 类在析构时调用 lambda。
   - *不适用条件*：严禁遗漏任何提前 `return` 分支中的资源释放。
5. **错误机械替换反例**：
   ```cpp
   // 错误：将 Go defer 机械写在函数末尾，导致提前 return 时资源未释放
   void Process() {
       FILE* f = fopen("test.txt", "r");
       if (check(f) == -1) return; // 错误：f 泄漏！
       fclose(f);
   }
   // 正确：使用 ScopeGuard 或局部析构包装
   void Process() {
       auto file_guard = std::unique_ptr<FILE, decltype(&fclose)>(fopen("test.txt", "r"), &fclose);
       if (check(file_guard.get()) == -1) return; // 析构自动 fclose！
   }
   ```
6. **信息不足或实现相关时的处理**：若 defer 包含修改具名返回值的副作用，需在 C++ 中显式转化为返回前变量修改。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Defer_statements](https://go.dev/ref/spec)；[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 GO-CPP-03：Go Goroutine 与 Channel 向 C++17 std::thread 与并发阻塞队列映射
1. **源码触发条件**：Go 源码中使用 `go worker()` 启动协程并通过 `chan T` 通信。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Go_statements](https://go.dev/ref/spec)）；目标语言 ISO C++17（[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：轻量级 Goroutine 协作调度，Channel 阻塞传递数据。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Goroutine 数量有限时映射为 `std::thread`，大量并发时必须使用固定大小线程池；Channel 映射为结合 `std::mutex` 和 `std::condition_variable` 的线程安全阻塞队列。
   - *不适用条件*：严禁无限制创建 `std::thread`（C++ 线程为原生 OS 线程，创建数万个会导致系统资源枯竭甚至进程崩溃）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：对成千上万个任务直接 1:1 创建 std::thread
   for (int i = 0; i < 100000; ++i) {
       std::thread(worker).detach(); // 致命错误：OS 线程资源耗尽导致 std::system_error 崩溃！
   }
   // 正确：使用线程池任务分发
   ThreadPool pool(4);
   for (int i = 0; i < 100000; ++i) {
       pool.enqueue(worker);
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及底层网络套接字并发，加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Go_statements](https://go.dev/ref/spec)；[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
