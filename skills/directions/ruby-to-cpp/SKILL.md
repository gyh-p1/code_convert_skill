---
name: ruby-to-cpp
description: Use when converting Ruby source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → C++ 语言转换规则

> **适用基线**：CRuby 3.4 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Ruby](../../references/languages/ruby.md)与[目标语言 C++](../../references/languages/cpp.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/ruby-to-cpp/README.md)；候选、冻结任务与第三方回传须分层记录。
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
