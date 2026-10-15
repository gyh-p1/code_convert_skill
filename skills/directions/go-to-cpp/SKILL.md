---
name: go-to-cpp
description: Use when converting Go source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → C++ 语言转换规则

> **适用基线**：Go 1.27 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 Go](../../references/languages/go.md)与[目标语言 C++](../../references/languages/cpp.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 Go → C++ 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-CPP-01：Go (T, error) 显式多返回值向 C++17 自定义 Result 结构体或 std::optional 映射
1. **源码触发条件**：Go 源码中函数返回 `(Result, error)`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Errors）；目标语言 ISO C++17（WG21-N4659）。
3. **原可观察行为**：显式多值返回，调用方通过 `if err != nil` 检查错误。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若只需表达有无数据，使用 `std::optional<T>`；若需携带错误细节，定义 `struct ResultOrError { T val; std::string error_msg; bool ok; }` 或使用输出参数；或者在失败时抛出异常。
   - *不适用条件*：严禁在 C++17 中使用 `std::expected`（C++23 特性，超出冻结规范）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：在 C++17 基线代码中使用 C++23 的 std::expected
   // std::expected<int, std::string> Divide(int a, int b); // 编译报错：C++17 无此特性！
   // 正确：使用带状态结构体或 std::optional
   struct Result { int value; std::string err; bool ok; bool is_ok() const { return ok; } };
   // ok 独立承接 err == nil；非 nil error 的消息也可能为空，不能以消息长度判成功。
   ```
6. **信息不足或实现相关时的处理**：若原 Go 代码无错误传递直接返回，直接映射为 C++ 对应单一返回值。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Errors；WG21-N4659 Clause 23.6。

### 规则 GO-CPP-02：Go defer 逆序清理向 C++17 局部作用域析构 (RAII) 映射
1. **源码触发条件**：Go 源码中使用 `defer mu.Unlock()` 或 `defer file.Close()`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Defer_statements）；目标语言 ISO C++17（WG21-N4659 Clause 6.7）。
3. **原可观察行为**：注册的清理函数在外层函数返回前以 LIFO（后进先出）逆序确定性执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：仅清理时点、注册顺序和参数取值相同才用函数级 RAII 守卫；内层块的 `std::lock_guard` 在块末析构，不自动承接 Go 函数级 `defer`。直接延迟调用保存注册时的函数/参数，闭包则按源实际捕获方式处理；循环多次注册须逐次保存并逆序执行。
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
6. **信息不足或实现相关时的处理**：若 defer 修改具名返回值，须在形成最终返回值之前执行相应副作用；不能指望返回值已复制后的局部析构改变该副本。清理若会失败，另核传播/覆盖规则，不能把它移入会终止进程的析构路径。无法确认作用域与捕获时点时停止受影响映射。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Defer_statements；WG21-N4659 Clause 6.7。

### 规则 GO-CPP-03：Go Goroutine 与 Channel 向 C++17 std::thread 与并发阻塞队列映射
1. **源码触发条件**：Go 源码中使用 `go worker()` 启动协程并通过 `chan T` 通信。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Go_statements）；目标语言 ISO C++17（WG21-N4659 Clause 33）。
3. **原可观察行为**：轻量级 Goroutine 协作调度，Channel 阻塞传递数据。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按资源边界核对 `std::thread` 或经允许的调度实现。固定线程池不是大量 goroutine 的自动等价：阻塞发送/接收可能占满 worker，令负责解锁的任务无法被调度而死锁。先核对依赖拓扑、背压、唤醒/取消和资源上限，不能只把每个 goroutine 塞入固定池。Channel 须保持无缓冲 rendezvous/有缓冲容量、close 后排空、关闭发送错误与 select 语义；普通阻塞队列不能冒充这些义务全部已映射。
   - *不适用条件*：严禁无限制创建 `std::thread`（C++ 线程为原生 OS 线程，创建数万个会导致系统资源枯竭甚至进程崩溃）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：对成千上万个任务直接 1:1 创建 std::thread
   for (int i = 0; i < 100000; ++i) {
       std::thread(worker).detach(); // 致命错误：OS 线程资源耗尽导致 std::system_error 崩溃！
   }
   // 有条件的示意：仅任务无相互阻塞依赖且线程池契约匹配时适用
   ThreadPool pool(4);
   for (int i = 0; i < 100000; ++i) {
       pool.enqueue(worker);
   }
   ```
6. **信息不足或实现相关时的处理**：所有实际并发都加载[并发场景](../../scenes/concurrency/SKILL.md)，网络另读[网络场景](../../scenes/network-io/SKILL.md)。调度/Channel 义务未明确时标知识缺口，不通过改变原并发模型掩盖。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Go_statements；WG21-N4659 Clause 33。

### 规则 GO-CPP-04：Go 切片与 string 向 C++17 std::vector/std::string 的所有权与共享语义选择
1. **源码触发条件**：Go 源码在 `[]byte`/`[]T`/`string` 上做子切片、`append`、`bytes.NewReader(...)`、`strings.Join(parts, "|")`、`string(output)` 与 `[]byte(text)` 互转（如 `crypto/sha256` + `hex.EncodeToString(sum[:])`、`payload, _ := json.Marshal(inObj)`）。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Slice_types）；目标语言 ISO C++17（WG21-N4659）。
3. **原可观察行为**：`s[a:b]` 得到的新切片与原切片共享底层数组，通过任一路径写入都可被另一路径观察到，直到 `append` 触发扩容后才分离；`string` 为只读字节序列且自带长度；切片值传递不复制元素。
4. **目标可选写法和不适用条件**：
   - *可选映射*：源确需独立数据时可用 `std::vector<uint8_t>` / `std::string` 拷贝；共享切片需共享保活的数组与独立 offset/len/cap。C++17 的只读文本借用可用 `std::string_view`，其他借用可采用经核对的指针+长度表示；`std::span` 是 C++20 特性，不用于本页 C++17 基线。显式声明“谁持有、谁保活、何时失效”，不能让容器扩容使仍有效的源切片别名失效。
   - *不适用条件*：严禁把 Go 子切片共享底层数组的性质默认成 `std::vector` 的构造或赋值——`std::vector` 的拷贝构造与 `operator=` 会立即产生独立副本，对副本的写入不再回写到“原切片”；也严禁把带内部 `'\0'` 的 Go `string`/`[]byte` 交给 `strlen`/`c_str()` 语义推断长度。
5. **错误机械替换反例**：
   ```cpp
   // 错误：以为 std::vector 的拷贝共享底层存储，后续写入丢失
   std::vector<uint8_t> src = DecodeBase64(blob);
   std::vector<uint8_t> view = src;   // Go 里这是共享底层数组的子切片语义
   view[0] ^= 0xFF;                   // 只改了副本！src[0] 未变，后续校验和静默不一致
   // 有条件的 C++17 借用示意：仅 src 保活、无扩容且借用范围一致时适用
   auto* alias = src.data();
   const auto alias_len = src.size();
   // 若后续存在 Go 式扩容/旧别名，须另行保持旧数组存活，不能只保存此裸指针。
   std::vector<uint8_t> owned = src;  // 仅源需要独立副本时适用
   ```
6. **信息不足或实现相关时的处理**：若源码中存在跨线程共享同一底层数组的切片，必须先确认目标侧的同步与保活责任，标注“共享视图的线程安全与生命周期待确认”，不得仅凭类型相近就断定语义等价。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Slice_types, #String_types；WG21-N4659 Clause 24, Clause 21。

### 规则 GO-CPP-05：Go error 返回与 panic 向 C++17 异常或错误码的选择边界
1. **源码触发条件**：Go 源码以 `(T, error)` 返回并 `if err != nil` 分流（`errors.New`、`fmt.Errorf("...: %w", err)`），或在越界/非法输入处 `panic`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Errors, #Handling_panics）；目标语言 ISO C++17（WG21-N4659）。
3. **原可观察行为**：错误经返回值显式传递，未检查不会自动中断控制流；`panic` 展开当前 Goroutine 的栈并执行已注册的 `defer`，可由 `recover()` 截断。
4. **目标可选写法和不适用条件**：
   - *可选映射*：返回错误或异常候选均须保持源检查/忽略与捕获边界；panic 先核当前 goroutine 的 defer/recover、传播和最终退出，不按“结构性”自动 terminate。C ABI/回调边界按具体 API 契约在边界内处理错误，不能改变源可恢复的结果。
   - *不适用条件*：异常逃出 noexcept 会 terminate；extern "C" 是语言链接属性，不是自动 terminate 的充分条件，但未约定异常互操作的 C API 边界仍不得让异常逃出。不得为每个 err 检查机械添加 throw，也不以 terminate 跳过源清理/recover。
5. **错误机械替换反例**：
   ```cpp
   // 错误：异常穿过 C ABI 边界抛出，C 调用方无法接住
   extern "C" int process_payload(const uint8_t* buf, size_t n) {
       if (n < 16) throw std::runtime_error("truncated"); // 逃出 extern "C" → std::terminate
       return 0;
   }
   // 正确：边界内翻译为错误码，异常只留在 C++ 内部
   extern "C" int process_payload(const uint8_t* buf, size_t n) {
       try {
           if (n < 16) throw std::runtime_error("truncated");
           return DoProcess(buf, n);
       } catch (const std::exception&) {
           return -1;   // 对照 Go 的 (T, error) 失败语义
       }
   }
   ```
6. **信息不足或实现相关时的处理**：若原 Go 代码把 `err` 作为可忽略的普通值继续执行（例如仅记录日志后返回部分结果），必须先确认哪一侧语义是契约，标注“异常安全性/错误传播范围待确认”后再选异常或错误码。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Errors, #Handling_panics；WG21-N4659 Clause 18.8, Clause 15。

### 规则 GO-CPP-06：Go interface{} 动态类型向 C++17 std::variant/std::any 的标签与访问映射
1. **源码触发条件**：Go 源码把任意类型装入 `interface{}`/`any`，例如 `map[string]any{"count": n, "results": results}`、`logInfo(title string, content interface{})`，并通过类型断言 `v, ok := x.(*net.IPNet)` 或 `switch v := x.(type)` 取回具体类型。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Interface_types, #Type_assertions）；目标语言 ISO C++17（WG21-N4659 Clause 20.7, Clause 20.8）。
3. **原可观察行为**：类型标签随值一起保存；类型断言失败返回该类型的零值与 `false`，`switch x.(type)` 的 `default` 分支承接未知类型；接口值为 `nil` 与持有一个“值为 nil 的具体类型”是两种不同状态。
4. **目标可选写法和不适用条件**：
   - *可选映射*：类型集合封闭时用 `std::variant<...>` 并配 `std::visit` / `std::get_if`，把 Go 的类型断言失败显式映射为 `get_if` 返回空指针；类型集合真正开放时用 `std::any` 并配 `std::any_cast`；需要保留“nil 具体类型”这一区分时，额外保存一个显式标签（枚举或 `std::monostate`）而不是依赖空值推断。
   - *不适用条件*：严禁用 `std::get<T>` 替代带 `ok` 的断言——`std::get` 失败会抛 `std::bad_variant_access`，改变原程序“返回零值 + false”的可观察失败形态；也不得把一个可能为 `std::monostate` 的 `variant` 交给未处理该分支的 `visit`，那会编译失败或漏掉分支。
5. **错误机械替换反例**：
   ```cpp
   // 错误：用 std::get 替代 Go 的 x.(*T) 带 ok 断言，失败即抛异常中断
   std::variant<int64_t, std::string, std::vector<uint8_t>> cell = ParseCell(raw);
   auto n = std::get<int64_t>(cell);   // Go: n, ok := x.(int64); ok == false 时继续执行
   // 正确：用 get_if 保留失败可见性，并对每个分支显式处理
   if (auto* n = std::get_if<int64_t>(&cell)) {
       UseCount(*n);
   } else if (auto* s = std::get_if<std::string>(&cell)) {
       UseText(*s);
   } else {
       /* 对应 Go switch 的 default 分支 */
   }
   ```
6. **信息不足或实现相关时的处理**：若 `interface{}` 承载的具体类型集合无法从源码穷举（依赖反射、注册表或调用方注入），必须标注“类型集合封闭性待确认”，在 `std::variant` 与 `std::any` 之间取舍前先向调用方确认。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Interface_types, #Type_assertions；WG21-N4659 Clause 20.7.3, Clause 20.8。

### 规则 GO-CPP-07：Go 监听器关闭向 C++ 裸 fd 的唤醒与唯一所有权映射
1. **源码触发条件**：Go 在 `net.Listener.Close()` 或 `http.Server.Close()` 后等待服务协程退出；目标 C++ 用监听 fd、`accept()` 线程和 `join()` 表达该生命周期。
2. **冻结版本/运行时/API 前提**：Go 1.27 → Linux x64 / C++17 POSIX socket；其他 OS 的 `accept`/关闭唤醒行为不得照搬。本例还在离开作用域时二次触发监听器清理。
3. **原可观察行为**：Go `Listener.Close` 使阻塞的 `Accept` 返回错误，后续等待能够结束。裸 fd 在一个线程阻塞 I/O 时由另一线程直接 `close`，不能据此保证唤醒；关闭后 fd 数值可被重用，重复 `close` 可能误关新资源。
4. **目标可选写法和不适用条件**：在关闭前建立明确的停止/唤醒路径，例如停止标志配合有界 `poll`，按冻结平台核对 `shutdown` 对监听 socket 的效果，然后关闭 fd、立即置为 `-1` 并等待线程退出；`Close()` 需只在 fd 有效时执行并避免与显式关闭二次作用。若目标使用 RAII socket 包装或其他事件循环，改用其可证明的取消机制，不机械复制本例的 POSIX 调用。
5. **错误机械替换反例**：
   ```cpp
   ::close(listener_fd); worker.join();  // 错误：阻塞的 accept 不保证因此返回
   ::close(listener_fd);                 // 错误：fd 可能已经被重用
   // 目标方案须先通知/唤醒 worker，再一次性关闭并使持有者失效。
   ```
6. **信息不足或实现相关时的处理**：若无法确认线程对 fd 的并发访问、`shutdown`/`poll` 的目标平台语义、关闭后是否仍有回调或析构，保留为未解决的生命周期问题；只看到 build PASS 不能证明没有挂起或误关。
7. **资料依据（名称/版本/章节）**：Go `net.Listener`；Linux `close(2)` 的多线程说明；Linux `poll(2)`。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。

## 子进程 API 映射

仅在 os/exec 触发时读取。CommandContext 的默认取消针对直接进程，WaitDelay 约束管道等待，不承诺整树回收。目标用实际平台 API 分别映射启动、双流排空、等待与超时，不能将 Cmd 字段臆造给 std::system/popen。通用观察义务读[进程场景](../../scenes/process-execution/SKILL.md)，跨 OS 读[进程系统页](../../systems/posix-windows-process-identity/SKILL.md)。源自定义 Cancel/WaitDelay 或目标杀树能力未知时记录待确认，不声明已验证。
