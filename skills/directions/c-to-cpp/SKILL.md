---
name: c-to-cpp
description: Use when converting C source code (ISO C11) to C++ (ISO C++17) while preserving observable behavior; covers semantic boundaries, RAII/exception boundaries, and container/concurrency mapping. Not for C++ to C or other language pairs.
---

# C → C++ 语言转换规则

> **适用基线**：源语言 ISO C11 ([WG14-N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)) → 目标语言 ISO C++17 ([WG21-N4659](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf))
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C](../../references/languages/c.md)与[目标语言 C++](../../references/languages/cpp.md)。
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

### 规则 5：`getopt_long` 的参数置换与长选项唯一前缀必须重建

> **归属说明**：实参绑定的**共享事实**（位置/命名/默认值的绑定规则）归语言层，见 [C 语言页 §五](../../references/languages/c.md)、[C++ 语言页 §五](../../references/languages/cpp.md)。本规则**只写 C→C++ 方向特有**的两点：`getopt_long` 的置换与唯一前缀语义。

1. **触发条件**：C 源码使用 `getopt`/`getopt_long` 解析命令行，且（a）存在**选项与操作数交错**的调用形态（如 `prog <path> -q`），或（b）使用长选项。
2. **适用前提**：源语言 ISO C11 + glibc `getopt(3)`/`getopt_long(3)` 行为；目标语言 ISO C++17。**非 glibc 实现（BSD/musl）行为不同**，须先确认源运行时的实现。
3. **应保留行为**：
   - **参数置换**：glibc 默认置换 `argv`，使 `realpath <path> -q` 与 `realpath -q <path>` 在源相应选项语义下等价；解析结束后 optind 指向剩余操作数起始，不能把它当作全部操作数之后。
   - **长选项唯一前缀**：`getopt_long` 允许**唯一前缀**匹配，`--s` 可匹配 `--si`。
   - **未知选项**：glibc 会**先自行输出诊断行**（形如 `prog: invalid option -- 'x'`）再返回 `'?'`；该输出属可观察行为。见 [C 语言页 §五 规则 L1-C-04](../../references/languages/c.md)。
4. **可选映射与不适用条件**：
   - *可选映射*：用手写循环替换 `getopt` 时，必须显式重建置换顺序与唯一前缀匹配，否则命令行形态等价性丢失。
   - *不适用条件*：POSIXLY_CORRECT/前导 `+` 使解析在首操作数停止；前导 `-` 则以返回值 1 处理非选项，是另一模式，不能等同“停止”。须按实际配置冻结；短选项无交错时不涉及长选项缩写。
5. **错误机械替换反例**：
   ```cpp
   // 错误：只接受精确长选项串，--s 落到 usage()
   if (arg == "si") { /* ... */ } else { usage(); }      // glibc 下 --s 应匹配 --si
   // 错误之二：按位置硬取 argv[1] 作为路径，丢失置换
   const char* path = argv[1];                           // prog -q <path> 时取到的是 "-q"
   // 原 du repair-2 的单长选项 "si" 路径：
   // len > 0 && strncmp(longopt, "si", len) == 0
   // 多选项实现必须另做精确匹配优先/歧义检测，不用“字符串相等”冒充前缀
   ```
6. **不确定性处理**：无法确认源 `getopt` 实现（glibc/BSD/musl）或是否设置 `POSIXLY_CORRECT` 时，标为“参数置换与前缀语义待确认”，不得默认 glibc 行为。
7. **官方依据**：[glibc `getopt_long`（含参数置换与唯一前缀）](https://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Options.html)、[glibc `getopt`（`POSIXLY_CORRECT`）](https://www.gnu.org/software/libc/manual/html_node/Using-Getopt.html)；[POSIX `getopt`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/getopt.html)。

### 规则 6：`argc`/`argv` 指针推进式消费必须完整重建

1. **触发条件**：C 源码对 `argc`/`argv` 做**算术推进**（`argc -= optind; argv += optind;`）后再解析剩余参数，或把 `argv` 传给另一个解析器。
2. **适用前提**：源语言 ISO C11；目标语言 ISO C++17。参数置换前提见规则 5。
3. **应保留行为**：推进后 `argc` 是**剩余参数个数**、`argv` 指向**第一个剩余参数**；后续所有“以 `argv[0]` 为程序名”的逻辑在推进后会指向错误对象。源里 `static int optind = 1;` 之类的**定义位置**（文件作用域 vs 函数内）会改变多次解析时的行为。
4. **可选映射与不适用条件**：
   - *可选映射*：用容器或视图承接参数时，必须显式记录“哪一段已被消费”，并把 `argc`/`argv` 的推进改写为对剩余范围的切片；不得把推进后的 `argv[0]` 当作程序名。
   - *不适用条件*：源码从不对 `argc`/`argv` 做算术推进（只按固定下标读取）时，不适用本规则。
5. **错误机械替换反例**：
   ```cpp
   // 源
   static int pwd_optind = 1;
   /* ... 解析 ... */
   argc -= pwd_optind; argv += pwd_optind;
   if (argc > 0) target = argv[0];        // 第一个剩余参数
   ```
   ```cpp
   // 错误：推进被丢弃，或推进后仍把 argv[0] 当程序名
   if (argc > 0) target = argv[0];        // 未推进 → 取到的是程序名或选项
   std::string prog = argv[0];            // 推进后 argv[0] 已不是程序名
   // 正确：显式记录消费边界
   int consumed = optind;
   if (argc - consumed > 0) target = argv[consumed];
   ```
6. **不确定性处理**：无法确定 `optind` 类变量的定义位置与生命周期时，标为“参数消费边界待确认”；**不得**假定单次解析。
7. **官方依据**：[POSIX `getopt`（`optind` 语义）](https://pubs.opengroup.org/onlinepubs/9799919799/functions/getopt.html)；[WG14-N1570 §5.1.2.2.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

### 规则 7：C→C++ 语法合法性预检（字面量 `const`、存储类、类型双关）

> **归属说明**：本条是**目标语言 C++17 自身**的语法合法性预检，属该方向特有；共享的判空/错误/编码义务见语言页。

1. **触发条件**：源码包含（a）字符串字面量传给 `char*` 形参，（b）`register` 存储类或显式寄存器变量，（c）`void**` 类型双关（如 `ComPtr<T>::addr()`），或（d）目标语言不存在的构造。
2. **适用前提**：目标语言 ISO C++17；**C++11 起字符串字面量的类型是 `const char[N]`**，向 `char*` 的转换在 C 中是历史遗留允许、在 C++17 中**是错误**。
3. **应保留行为**：这些是**编译期**问题，不影响运行语义，但会阻断目标 build。转换时必须逐处修正以保住可编译性，且**不得**用强制转换掩盖真正的写入企图。
4. **可选映射与不适用条件**：
   - *字面量 `const`*：把形参改为 `const char*`；若源确实要写入该缓冲区，说明源本身是 UB，标为“源已存在”并保留原样，**不得**通过 `const_cast` 制造可行的假象。
   - *`register`*：C++17 中 `register` 不再是存储类说明符（C++17 弃用/移除了该用法），须删除该关键字；显式寄存器变量与内联汇编（GCC 扩展）须改为等价的标准写法或标为不可映射。
   - *`void**` 双关*：`ComPtr<T>::addr()` 之类的 “取地址给 `void**` 由被调方回填” 模式，须改用目标 SDK 的官方访问器（如 `GetAddressOf()`/`ReleaseAndGetAddressOf()`）或显式 `reinterpret_cast`，并说明其前提。
   - *不适用条件*：源码本就以 `const char*` 接收字面量、或未使用 `register` 时，不适用对应子项。
5. **错误机械替换反例**：
   ```cpp
   // 错误一：字面量 const 丢失
   void log_line(char* msg);              // 源 log_line("ok") 在 C 中可过，C++17 报错
   log_line("ok");                        // invalid conversion from 'const char*' to 'char*'
   // 错误二：用 const_cast 掩盖写入企图
   log_line(const_cast<char*>("ok"));     // 若函数真写入，即对只读字面量写入 → UB
   // 错误三：保留 C++17 已移除的存储类
   register int i = 0;                    // 目标语言无此存储类用法
   // 正确：形参改 const char*，删除 register
   void log_line(const char* msg);
   int i = 0;
   ```
 6. **不确定性处理**：若字面量在源中确实被写入（源已存在 UB），如实登记为“源已存在缺陷，转换不得顺手修复”，**不**把它转成本方向的修复规则。
7. **官方依据**：[WG21-N4659 Clause 5.13.5（字符串字面量类型）](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)、[Clause A.2（`register` 的移除）](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[Microsoft `ComPtr::GetAddressOf`](https://learn.microsoft.com/en-us/cpp/cppcx/wrl/comptr-class)。

### 规则 8：`fnmatch` 等字符类边角语义：修复本身不得引入新偏差

1. **触发条件**：源码依赖 POSIX `fnmatch` 的模式匹配（尤其字符类），而目标平台无 `fnmatch` 或行为不同，需要手工重建。
2. **适用前提**：源 POSIX `fnmatch` 语义；目标语言 ISO C++17。
3. **应保留行为**：`fnmatch` 的字符类边角是**高风险改写点**：首字符 `]` 在 `[...]` 中**按字面**处理；范围表达式 `[]-a]` 表示“`]` 到 `a` 之间的字符”，与直觉相反；`[!...]` 与 `[^...]` 的取反写法在不同实现下有差异。
4. **可选映射与不适用条件**：
   - *可选映射*：优先使用目标平台的既有实现（`PathMatchSpec`/`std::regex`/自备解析器），并为边角形态写显式测试向量。
   - *不适用条件*：源码不使用字符类（只用 `*`/`?`）时，不涉及这些边角。
5. **错误机械替换反例**：
   ```cpp
   // 第 1 轮：把首字符 ']' 当作普通字符之外的语义处理，过度限制
   // 第 2 轮“修复”为在 ']' 处关闭字符类 —— 反而违反了 fnmatch 的 []-a] 语义
   // 错误：把 ']' 一律当作类结束符
   if (c == ']') { class_end = true; }    // 首字符位置的 ']' 应属字面成员
   // 正确：按 fnmatch 的边角规则处理首字符与范围
   //   首字符 ']'   → 字面成员
   //   []-a]        → 范围 ']'..'a'
   ```
6. **不确定性处理**：无法取得源 `fnmatch` 的准确语义（glibc/FreeBSD/musl 细节有差异）时，标为“字符类边角语义待确认”，并把每个边角形态列为 oracle 观察点；**不得**以“已修过一次”为由宣称收敛。
7. **官方依据**：[POSIX `fnmatch`（模式与字符类语义）](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fnmatch.html)；[Microsoft `PathMatchSpec`](https://learn.microsoft.com/en-us/windows/win32/api/shlwapi/nf-shlwapi-pathmatchspeca)。

---

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

## 四、按需加载的专题与场景规则

> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

- **类型与 ABI 专题**：遇到共享头文件、C ABI 兼容、结构体对齐、`void*` 转换或指定初始化时，读取 [类型、接口与 C ABI](references/type-abi.md)。
- **头文件与宏专题**：遇到 C 宏在 C++ 报未声明或命名冲突时，读取 [头文件与宏可用性](references/header-macro.md)。
- **网络与套接字场景**：源码实际执行 socket I/O 时，共同加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)；跨 Linux/Windows 时加读 [`skills/systems/posix-winsock/SKILL.md`](../../systems/posix-winsock/SKILL.md)。
- **文件 I/O 场景**：源码确有文件读写与路径操作时，共同加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)；跨 OS 路径操作加读 [`skills/systems/posix-windows-filesystem/SKILL.md`](../../systems/posix-windows-filesystem/SKILL.md)。
- **并发场景**：跨 OS 线程调度与系统同步原语加读 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md) 与 [`skills/systems/posix-windows-threads/SKILL.md`](../../systems/posix-windows-threads/SKILL.md)。
- **进程与身份/权限场景**：源码实际创建、替换、等待或终止进程，或查询、切换自身身份与特权时，共同加载 [`skills/systems/posix-windows-process-identity/SKILL.md`](../../systems/posix-windows-process-identity/SKILL.md)。
- **Windows 注册表与服务场景**：源码读写注册表键值，或经 SCM 创建、配置、启动、停止、删除服务时，加载 [`skills/systems/windows-registry-service-subsystem/SKILL.md`](../../systems/windows-registry-service-subsystem/SKILL.md)；POSIX 侧无等价子系统，按不可映射项处理。

---

## 五、模型自检与第三方评估结论分流

1. **模型自检与预检**：转换模型生成的代码仅作内部自审，用于筛查声明遗漏、语法冲突与生命周期疑点。模型说“无问题”不等于无缺陷，严禁给模型自检贴上 `syntaxPassed` 或编译通过标签。
2. **语法结论来源**：语法结论必须由第三方评估机构在目标 MinGW g++ C++17（或批准的工具链）下执行真实编译后回填；未收到结果前一律保持 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`。
3. **功能行为边界**：编译通过绝对不代表功能正确，功能验收必须依据独立的可观察 oracle 判定。
