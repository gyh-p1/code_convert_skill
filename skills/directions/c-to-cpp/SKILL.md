---
name: c-to-cpp
description: Use when converting C source code (ISO C11) to C++ (ISO C++17) while preserving observable behavior; covers semantic boundaries, RAII/exception boundaries, and container/concurrency mapping. Not for C++ to C or other language pairs.
---

# C → C++ 语言转换规则

> **适用基线**：源语言 ISO C11 ([WG14-N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)) → 目标语言 ISO C++17 ([WG21-N4659](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf))
> **共性语义依据**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)
> **真实构建证据口径**：当前仓库仅 `fe`、`stest`、`realpath`、`pwd`、`chain-reactor` 五个冻结样例在 MinGW-w64 g++ / C++17 目标环境下取得构建 PASS 记录；**功能均未验收**。MSVC 与 Clang 仅为候选工具链，无目标构建证据。
> **规范硬约束**：严格排除 C++20 Concepts、协程及 C++23 `std::expected` 等超出 C++17 基线的特性。

---

## 一、适用范围与前提

用于将已有 C 代码转换为 C++，核心原则是**优先保持原有可观察行为，再考虑 C++ 惯用写法**。先确认目标 C++ 标准（ISO C++17）、目标平台/编译器、调用方是否依赖 C ABI、是否允许引入 C++ 标准库与异常；用户未指定时不要假设可以改变接口、错误模型或分配方式。不能仅凭本 Skill 保证目标代码编译或行为等价。

---

## 二、转换时优先守住的行为

- **接口与数据布局**：保留公开函数签名、返回值约定、结构体布局、整数宽度及符号性假设。跨 C/C++ 边界暴露的符号要判断是否需要 `extern "C"`；它指定语言链接（具体名称表示和调用约定取决于实现），不自动保证对象布局或整体 ABI 兼容。
- **控制流与错误**：保留提前返回、错误码、`errno` 的读写时机、清理分支和部分成功状态。不要未经授权将错误码改为异常，严禁让异常跨越 C ABI 边界。
- **资源与副作用**：保持文件/句柄关闭、内存释放、锁释放和回调调用的时机及顺序；不要为了换成 RAII 而改变共享所有权、生命周期或失败路径。标准输出、文件、环境变量、进程等外部可见行为同样属于转换范围。
- **边界条件**：检查空指针、零长度、溢出/截断、缓冲区边界、字符编码以及未定义或实现定义行为。源程序本身没有确定语义的地方，不宣称存在唯一等价转换。

---

## 三、七段式核心转换规则

### 规则 1：C 风格以 NUL 结尾的 `char*` 字符串向 C++ 视窗与容器映射

1. **触发条件**：C 源码中使用 `const char*`、`char[]` 作为只读字符串传递、查找或解析。
2. **适用前提**：源语言 ISO C11，目标语言 ISO C++17；目标代码引入 `<string_view>` 或 `<string>`。
3. **应保留行为**：保持字符串内容的字符序列、读取边界与只读安全性，避免非必要堆分配拷贝；若后续传递给需要 C ABI 结尾的 API，必须保证存在 `\0` 终止标记。
4. **可选映射与不适用条件**：
   - *可选映射*：若字符串仅在当前函数调用链中只读查看、且源内存生命周期跨越整个视窗，可映射为 `std::string_view`；若目标需要独立拥有所有权、修改内容或向需要 `const char*` 的外部 C API 传参，映射为 `std::string`。
   - *不适用条件*：若二进制缓冲区内部可能含有嵌入的 `\0`，严禁直接使用以 `\0` 结尾为假设的 `std::string(const char*)` 构造函数（会导致截断）；`std::string_view` **不保证以 `\0` 结尾**，绝对禁止直接将其 `.data()` 传入需要以 `\0` 结尾的系统调用（如 `fopen`、`open`）。
5. **错误机械替换反例**：
   ```cpp
   // 错误反例：向系统 fopen 传入未保证 NUL 结尾的 string_view 裸指针，引发越界访问 UB
   void open_file(std::string_view path) {
       FILE* f = fopen(path.data(), "r"); // 危险：path.data() 不保证 '\0' 结尾！
       if (f) fclose(f);
   }
   ```
6. **不确定性处理**：若源码中指针所有权不明确（例如由外部全局或未知库生命周期管理），保持 `const char*` 原型并标注待确认所有权契约，禁止盲目封装为 `std::string`。
7. **官方依据**：[WG21-N4659 Clause 24.3, Clause 24.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[WG14-N1570 §7.1.1, §7.24](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 2：C 手动多出口清理（`goto cleanup`）向 RAII 与异常边界映射

1. **触发条件**：C 源码中使用 `goto cleanup`、显式多分支逆序释放局部资源，并通过返回值传递 `int` 错误码。
2. **适用前提**：源语言 ISO C11，目标语言 ISO C++17；函数可能作为 C 符号导出（`extern "C"`）。
3. **应保留行为**：严格保留资源释放的逆序执行（LIFO）；保持错误码数值或 `errno` 读写时机；若导出给 C 调用方，绝对禁止任何 C++ 异常逸出栈顶。
4. **可选映射与不适用条件**：
   - *可选映射*：局部分配且独占所有权的动态内存，可使用 `std::unique_ptr<T>` 或标准容器；对文件描述符可编写轻量局部析构守卫；
   - *不适用条件*：C++17 排除 C++23 `std::expected`，不得使用不存在的基线特性；若函数签名规定返回 C 错误码，不得擅自改抛异常；若内部逻辑使用 C++ 异常，在 `extern "C"` 边界必须全量捕获。
5. **错误机械替换反例**：
   ```cpp
   // 错误反例：在 extern "C" 导出函数中直接 throw 异常，跨 C ABI 边界导致未捕获崩溃
   extern "C" int parse_config(const char* buf) {
       if (!buf) throw std::invalid_argument("null buffer"); // 致命：破坏 C ABI 异常边界！
       return 0;
   }
   ```
6. **不确定性处理**：若源码中存在复杂的跨函数部分成功/部分失败所有权转移（如部分释放、部分缓存在全局表），禁止机械替换为单作用域 `std::unique_ptr`，应保持原清理结构并标明未验证所有权流向。
7. **官方依据**：[WG21-N4659 Clause 18, Clause 15.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[WG14-N1570 §7.22.4.4](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 3：C 手工容量动态数组向 C++ `std::vector` 映射与别名失效防范

1. **触发条件**：C 源码中使用 `malloc` 分配连续内存，维护指针、`size` 和 `capacity`，并在追加时通过 `realloc` 扩容；同时存在指向内部元素的别名指针。
2. **适用前提**：源语言 ISO C11，目标语言 ISO C++17。
3. **应保留行为**：保持数组元素的物理连续性与遍历顺序；防止因扩容地址迁移导致外部指针悬挂。
4. **可选映射与不适用条件**：
   - *可选映射*：当生命周期封闭于单一函数或类内部、且无外部长期持有的元素裸指针时，可映射为 `std::vector<T>`；
   - *不适用条件*：若外部模块或结构体长期缓存了数组元素的裸指针（如指向某个 `item` 的指针），不可使用常规 `vector::push_back`，否则重分配将使全部旧指针成为野指针（Dangling Pointer）。
5. **错误机械替换反例**：
   ```cpp
   // 错误反例：外部持有元素指针后触发 vector 自动扩容，旧指针失效造成野指针解引用
   std::vector<int> vec = {1, 2, 3};
   int* ptr = &vec[0];
   vec.push_back(4); // 若容量不足触发重新分配，旧内存被释放，ptr 立即失效！
   *ptr = 10;        // 未定义行为（UB）！
   ```
6. **不确定性处理**：若静态分析无法证明所有内部元素指针的生命周期短于下一次重分配，保持 C 风格动态数组分配模式，或使用下标索引代替裸指针，并标注别名生命周期不确定性。
7. **官方依据**：[WG21-N4659 Clause 26.3.11, Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[WG14-N1570 §6.2.5, §7.22.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 4：C 语言级并发与原子原语向 C++17 `<atomic>` 与 `<thread>` 映射

1. **触发条件**：C 源码中使用 ISO C11 语言层并发与原子原语（`<threads.h>` 的 `thrd_create`、`mtx_lock`，或 `<stdatomic.h>` 的 `atomic_int`、`atomic_store`、`atomic_load` 与内存序）。
2. **适用前提**：源语言 ISO C11，目标语言 ISO C++17；目标编译器支持标准 C++ 线程与原子库。
3. **应保留行为**：保持线程生命周期、临界区互斥、原子操作与内存序（Memory Order：Acquire/Release/SeqCst）语义严格一致。
4. **可选映射与不适用条件**：
   - *可选映射*：C11 `<threads.h>` 线程与互斥映射为 C++17 `<thread>` 与 `<mutex>`；C11 `<stdatomic.h>` 原子类型与操作映射为 C++17 `<atomic>`（`std::atomic<T>`、`std::memory_order`）；
   - *不适用条件*：`std::thread` 析构时若仍处于 `joinable()` 状态，将调用 `std::terminate()` 导致程序异常终止；若源 C 源码涉及 POSIX 线程（`pthread`）或 Win32 原生线程库，严禁在 A 类规则中维护 API 映射，必须移交 B 类系统/运行时 Skill。
5. **错误机械替换反例**：
   ```cpp
   // 错误反例：std::thread 创建后离开作用域未 join 亦未 detach，析构直接导致崩溃
   void spawn_worker() {
       std::thread t([]{ /* 执行计算 */ });
       // 离开作用域时 t.~thread() 检查 joinable() == true，直接调用 std::terminate() 崩溃！
   }
   ```
6. **不确定性处理**：若 C 源码涉及操作系统专有线程属性、信号掩码或取消机制（`pthread_cancel`），A 类规则仅说明语言层原子性与同步契约，具体 OS 调度与线程 API 必须委托对应 B 类规则。
7. **官方依据**：[WG21-N4659 Clause 32 Atomics, Clause 33 Threads](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[WG14-N1570 §7.17, §7.26](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

## 四、按需加载的专题与场景规则

> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

- **类型与 ABI 专题**：遇到共享头文件、C ABI 兼容、结构体对齐、`void*` 转换或指定初始化时，读取 [类型、接口与 C ABI](references/type-abi.md)。
- **头文件与宏专题**：遇到 C 宏在 C++ 报未声明或命名冲突时，读取 [头文件与宏可用性](references/header-macro.md)。
- **网络与套接字场景**：源码实际执行 socket I/O 时，共同加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)；跨 Linux/Windows 时加读 [`skills/systems/posix-winsock/SKILL.md`](../../systems/posix-winsock/SKILL.md)。
- **文件 I/O 场景**：源码确有文件读写与路径操作时，共同加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)；跨 OS 路径操作加读 [`skills/systems/posix-windows-filesystem/SKILL.md`](../../systems/posix-windows-filesystem/SKILL.md)。
- **并发场景**：跨 OS 线程调度与系统同步原语加读 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md) 与 [`skills/systems/posix-windows-threads/SKILL.md`](../../systems/posix-windows-threads/SKILL.md)。

---

## 五、模型自检与第三方评估结论分流

1. **模型自检与预检**：转换模型生成的代码仅作内部自审，用于筛查声明遗漏、语法冲突与生命周期疑点。模型说“无问题”不等于无缺陷，严禁给模型自检贴上 `syntaxPassed` 或编译通过标签。
2. **语法结论来源**：语法结论必须由第三方评估机构在目标 MinGW g++ C++17（或批准的工具链）下执行真实编译后回填；未收到结果前一律保持 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`。
3. **功能行为边界**：编译通过绝对不代表功能正确，功能验收必须依据独立的可观察 oracle 判定。
