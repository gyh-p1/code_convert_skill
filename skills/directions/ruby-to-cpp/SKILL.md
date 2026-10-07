---
name: ruby-to-cpp
description: Use when converting Ruby source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → C++ 语言转换规则

> **适用基线**：CRuby 3.4 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Ruby](../../references/languages/ruby.md)与[目标语言 C++](../../references/languages/cpp.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Ruby → C++ 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 RB-CPP-01：Ruby 开放类与猴子补丁向 C++17 装饰器/组合模式重构映射
1. **源码触发条件**：Ruby 源码中打开已有类（如标准类 `String` 或第三方类）追加新方法（Monkey Patching）。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 ISO C++17（[WG21-N4659 Clause 12](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：全局范围内所有该类实例均获得新方法。
4. **目标可选写法和不适用条件**：
   - *可选映射*：C++ 封闭已有类！严禁尝试直接给 `std::string` 加成员函数。必须重构为独立的命名空间自由函数（`namespace utils { void MyFunc(const std::string&); }`），或定义派生类/包装类。
   - *不适用条件*：严禁向 `std` 命名空间添加自定义函数（根据 ISO C++ 规范此举属于未定义行为 UB！）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：向 std 命名空间注入自由函数（标准未定义行为 UB！）
   namespace std {
       void my_extension(string& s) { ... } // 严重违反 C++ 标准规范！
   }
   // 正确：定义独立的工具命名空间
   namespace MyProject::StringUtils {
       void MyExtension(std::string& s) { ... }
   }
   ```
6. **信息不足或实现相关时的处理**：若源猴子补丁覆写了核心行为，在转换报告中标明侵入性修改已降级为显式调用。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 12](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 RB-CPP-02：Ruby 资源块模式 (File.open do...end) 向 C++17 RAII 作用域析构映射
1. **源码触发条件**：Ruby 源码中使用带有代码块的文件或网络打开操作。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4；目标语言 ISO C++17（[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：代码块执行完毕自动关闭底层资源句柄。
4. **目标可选写法和不适用条件**：
   - *可选映射*：利用 C++ 局部对象作用域析构特性（RAII），如 `std::ifstream file(path);`。
   - *不适用条件*：严禁在堆上 `new` 出文件对象而不妥善管理其指针生命周期。
5. **错误机械替换反例**：
   ```cpp
   // 错误：在堆上创建流指针且未保护释放
   auto f = new std::ifstream(path);
   // 正确：使用局部栈对象
   std::ifstream f(path);
   ```
6. **信息不足或实现相关时的处理**：若涉及底层文件系统路径跨平台差异，加载 [`skills/systems/posix-windows-filesystem/SKILL.md`](../../systems/posix-windows-filesystem/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 RB-CPP-03：Ruby Thread 并发向 C++17 std::thread 与数据竞争防范映射
1. **源码触发条件**：Ruby 源码中使用 `Thread.new` 处理并发任务。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：受 MRI GVL 保护，基础数据结构读写不会引发内存重排崩溃。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `std::thread`；**关键差异**：C++ 没有 GVL！任何跨线程共享的数据结构（如 `std::vector` 或类成员）必须显式施加 `std::mutex` 保护，否则在 C++ 中直接触发未定义行为（Data Race UB）导致内存损坏或崩溃。
   - *不适用条件*：严禁在无互斥锁保护下直接照抄 Ruby 中对共享变量的读写。
5. **错误机械替换反例**：
   ```cpp
   // 错误：认为像 Ruby 一样可以直接多线程对数组 push
   std::vector<int> shared_vec;
   // thread 1 & thread 2: shared_vec.push_back(1); // 致命 UB 崩溃！
   // 正确：显式互斥锁同步
   std::mutex mtx;
   {
       std::lock_guard<std::mutex> lock(mtx);
       shared_vec.push_back(1);
   }
   ```
6. **信息不足或实现相关时的处理**：若代码涉及原子标量，改用 `std::atomic<T>`。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)。

### 规则 RB-CPP-04：Ruby 块/闭包捕获向 C++17 std::function 与 lambda 的捕获生命周期映射
1. **源码触发条件**：Ruby 源码把块当作可传递的一等过程使用，例如 `getfile.each do |file| ... end`、`datastore['FILE_GLOBS'].split(',').each do |glob| ... end`、`hashes.each do |hash| ... end`，以及把块写入变量、作为参数多次转发（`&blk`）或在容器里保存后再调用。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-PROC](https://docs.ruby-lang.org/en/3.4/Proc.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 11.3, Clause 20.14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：块是携带词法环境的一等对象，可被转发、延迟执行与多次调用；每次调用看到的是定义处捕获的那些变量（按引用看到变量本身，因此调用时机影响可观察结果）；块内的 `break`/`next`/`return` 由调用方方法决定其控制流含义。
4. **目标可选写法和不适用条件**：
   - *可选映射*：同步、单次、立即调用的迭代体用 lambda（`[&](const auto& item){ ... }`）或范围 `for` 直接展开，避免引入间接层；需要存储或转发时用 `std::function<R(Args...)>` 并**按值捕获**（`[=]`/`[x]`）需要跨作用域存活的状态；只被同步调用且明显不逃逸时才用引用捕获，并把“被捕获变量的作用域覆盖所有调用点”写进报告。
   - *不适用条件*：严禁在源 lambda 中用引用捕获（`[&]`）后把它存进 `std::function` 再于原作用域之外调用——被引用对象已析构，属未定义行为；也严禁把 Ruby 的“块捕获”直接当作 `std::function` 按值捕获处理：Ruby 里块看到的是变量本身的变化，按值捕获会冻结调用时刻的值。
5. **错误机械替换反例**：
   ```cpp
   // 错误：引用捕获后存起来延迟调用，块看到的对象已析构
   std::function<void()> make_cb() {
       std::string glob = "*.config";
       return [&]() { use(glob); };   // UB：glob 在返回后即销毁
   }
   // 正确：按值捕获，或让 lambda 只作同步调用
   std::function<void()> make_cb() {
       std::string glob = "*.config";
       return [glob]() { use(glob); };
   }
   ```
6. **信息不足或实现相关时的处理**：块被保存后何时调用、被谁调用在源码中不明确时（例如存进容器、随对象字段携带），必须标注"调用时机与存活期未定"并询问，不得默认按同步调用处理；块内若出现 `break`/`next`/`return`，需先确认这些控制流应落到哪一层（`std::function` 无法表达从调用方返回）。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 11.3, Clause 20.14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[RB-DOC-PROC](https://docs.ruby-lang.org/en/3.4/Proc.html)。

### 规则 RB-CPP-05：Ruby Symbol 与 Hash 向 C++17 enum class / std::unordered_map 的键身份与遍历顺序映射
1. **源码触发条件**：Ruby 源码以 `Symbol` 作状态标记或哈希键，例如 `origin_type: :session`、`private_type: :ntlm_hash`、`update: :unique_data`、`data: { :company => company }`，以及读取 `sysinfo['Computer']`、`tokens['delegation']` 这类字符串键映射。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-SYMBOL](https://docs.ruby-lang.org/en/3.4/Symbol.html)、[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 9.6, Clause 26.2.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：`Symbol` 是全局唯一、不可变的原子标识符（同一字面量处处同一对象），相等比较按身份；`Hash` 保留键的**插入顺序**，`each` 按插入顺序产出 `[key, value]`，且允许 `nil` 值存在而键仍在。
4. **目标可选写法和不适用条件**：
   - *可选映射*：取值集合在编译期封闭的 Symbol（如状态、类型标记）映射为 `enum class`，与外部交换时显式提供 `to_string`/`from_string`；键集合动态或来自外部输入的映射为 `std::unordered_map<std::string, V>`（需要保留插入顺序以匹配 Ruby 遍历语义时改用 `std::vector<std::pair<K,V>>` 或 `std::map` 并在报告里说明顺序来源）；捕获环境里的固定键改用 `static constexpr std::string_view` 常量，避免重复构造 `std::string`。
   - *不适用条件*：严禁把 Ruby 的 Symbol 一律落成散落的字符串字面量比较（丢失"编译期封闭、拼写受检查"的性质，且每次比较构造临时 `std::string`）；严禁依赖 `std::unordered_map` 的遍历顺序去复现 Ruby `Hash` 的插入顺序——规范不保证任何顺序，重哈希后顺序可变。
5. **错误机械替换反例**：
   ```cpp
   // 错误：Symbol 退化成散落字符串，Hash 顺序被 unordered_map 打乱
   std::unordered_map<std::string, std::string> info;
   for (const auto& kv : info) {          // 错误：顺序与 Ruby Hash 的插入顺序无关
       if (kv.first == "Computer") { }    // 错误：拼写错误到运行期才暴露
   }
   // 正确：封闭取值用 enum class；需要顺序语义时用保序容器
   enum class CredType { Session, NtlmHash };
   std::vector<std::pair<std::string, std::string>> info_ordered;
   ```
6. **信息不足或实现相关时的处理**：Symbol 的取值集合是否封闭（是否来自 `datastore`、外部 JSON 或用户输入）必须先从源码确认；无法确认时标注"键集合开放"并询问，不得强行用 `enum class` 收窄；Ruby `Hash` 是否允许 `nil` 值与"键存在但值为空"的区分要在报告中标出（C++ 侧 `operator[]` 会默认构造插入，与 Ruby 的 `[]` 只读不同）。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-SYMBOL](https://docs.ruby-lang.org/en/3.4/Symbol.html)；[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)；[WG21-N4659 Clause 26.2.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 RB-CPP-06：Ruby 异常展开与 ensure 向 C++17 异常安全作用域与 RAII 清理映射
1. **源码触发条件**：Ruby 源码使用 `begin ... rescue A ... rescue B ... ensure ... end`（可带 `raise` 重新抛出），例如 `rescue StandardError`、`rescue Timeout::Error`、`rescue ::Rex::Post::Meterpreter::RequestError => e` 后按 `e.message =~ /.../` 分派、以及在同一段里 `ensure` 做清理。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 18, Clause 15.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：异常沿栈展开，途经的 `ensure` **必被执行**（正常返回、抛出、`return` 都执行）；裸 `rescue` 只匹配 `StandardError` 及其子类，`Exception` 的其他分支（如 `SystemExit`、`SignalException`、`NoMemoryError`）不被捕获；`rescue` 子句按书写顺序自上而下取第一个匹配者，`raise e` 保留原异常对象与回溯。
4. **目标可选写法和不适用条件**：
   - *可选映射*：每个 `rescue` 子句映射为一个 `catch` 块，类型按 Ruby 异常类逐一对到自定义 C++ 异常类型，`e.message =~ /.../` 这类分派改写为 `catch (const X& e)` 中的条件判断或 `catch` 顺序；`ensure` 的清理改由 RAII 对象在作用域退出时执行（`std::unique_ptr`、`std::lock_guard`、自定义析构器），需要"无论成败都要跑"的收尾动作放进包装对象的析构函数；重新抛出用裸 `throw;`。
   - *不适用条件*：严禁把 Ruby 的裸 `rescue`（只捕获 `StandardError`）机械翻译为 `catch (...)`——后者会吞掉本应向上传播的不可恢复异常，改变失败路径拓扑；严禁用 `catch (const std::exception& e) { throw e; }` 代替 `throw;`（前者按 `std::exception` 切片复制，丢失派生类型与诊断信息）；也严禁让这些异常跨越 C ABI 边界。
5. **错误机械替换反例**：
   ```cpp
   // 错误：裸 rescue 被翻成 catch(...)，且重新抛出时切片
   try {
       hashes = client.sam_hashes();
   } catch (const std::exception& e) {
       throw e;                       // 错误：按 std::exception 切片，派生类型丢失
   } catch (...) {
       report("access denied");       // 错误：连不可恢复异常一起吞掉，与 Ruby 裸 rescue 不符
   }
   // 正确：逐类捕获，保证清理由 RAII 完成
   try {
       hashes = client.sam_hashes();
   } catch (const StdError& e) {      // 对应 rescue StandardError
       report(e.what());
   }
   ```
6. **信息不足或实现相关时的处理**：Ruby 侧抛出的异常类若来自框架（如 `Rex`/`Msf` 命名空间下的错误类型）或第三方库，必须先把"该类型在 C++ 侧有没有对应表示"标注为缺口并询问，不得用泛化的 `std::runtime_error` 顶替；`ensure` 中如果含有依赖顺序的多步清理（如先解锁后释放句柄），需明确声明期望的析构顺序。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[WG21-N4659 Clause 18, Clause 15.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
