---
name: cpp-to-c
description: Use when converting C++ source code (ISO C++17) to C (ISO C11) while preserving observable behavior; covers semantic downgrades including RAII to manual cleanup, exceptions to error codes, classes/virtual dispatch to structs, and template monomorphization. Not for C to C++ or other language pairs.
---

# C++ → C 语言转换规则

> **适用基线**：源语言 ISO C++17 ([WG21-N4659](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)) → 目标语言 ISO C11 ([WG14-N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf))
> **共性语义依据**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/cpp-to-c/README.md)；候选、冻结任务与第三方回传须分层记录。
> **真实构建证据口径**：当前仓库中 C++ 作为源语言、C 作为目标语言的方向处于**`未验证/阻断`**状态（尚无项目级目标编译 PASS 证据）；本 Skill 仅提供静态决策依据，不代表转换产物已通过编译或功能验证。
> **规范硬约束**：源基线以 ISO C++17 为限（不含 C++20 Concepts、协程等）；目标基线以 ISO C11 为限（不含 C23 特性）。

---

## 一、适用范围与前提

用于将已有 C++17 代码降级转换为 C11，核心挑战在于**将 C++ 隐式语言机制（RAII 析构、异常展开、虚函数分派、模板泛型）重构为 C11 显式过程与数据结构**。转换必须优先守住控制流拓扑、资源释放时机与错误传播行为，杜绝因机制丢失导致内存泄露或未定义行为。

---

## 二、转换时优先守住的行为

- **资源释放顺序与异常安全**：C++ 保证离开作用域时局部对象按构造逆序确定性析构；降级至 C 时，必须在函数的**每一个可能提前返回的出口**显式执行对应清理，或统一通过 `goto cleanup` 保持 LIFO 释放顺序。
- **错误与失败可见性**：C++ 异常抛出后中断正常执行并向上传播；降级至 C 时必须设计显式错误码返回值或状态出参，并在每一层调用点显式检查并级联返回，不得静默吞并错误。
- **虚函数与运行时多态**：保留基类指针调用派生类覆盖方法的动态分派行为；若实例化类型集合在编译期完全闭合，可考虑标签联合（Tagged Union）或显式函数指针虚表（vtable）。
- **对象布局与生命周期**：C++ 构造与析构包含基类到派生类的级联调用链；在 C 中必须提供显式的 `_init` 与 `_destroy` 函数，并在内存分配成功后按序初始化。

---

## 三、七段式核心转换规则

### 规则 1：C++ RAII 作用域确定性析构向 C11 `goto cleanup` 逆序显式释放映射

1. **触发条件**：C++ 源码中依赖对象析构函数（如 `std::unique_ptr`、`std::lock_guard`、自定义 RAII 类）在离开作用域时自动释放资源，且函数包含多个提前返回分支。
2. **适用前提**：源语言 ISO C++17，目标语言 ISO C11；目标环境无编译器私有作用域属性（保持纯 ISO C11 兼容）。
3. **应保留行为**：保持资源在退出作用域时严格按初始化的逆序（LIFO）完全释放；保证所有分支（正常与错误返回）均不发生句柄或内存泄漏。
4. **可选映射与不适用条件**：
   - *可选映射*：在 C 函数入口处将所有资源句柄/指针初始化为 `NULL`/`-1`；在退出前设置统一的 `goto cleanup` 汇聚标签，按 LIFO 顺序依次判断并释放；
   - *不适用条件*：严禁在各个 `return` 语句前机械复制粘贴清理逻辑（极易遗漏中间分支，产生资源泄漏）；不可假定 `free(NULL)` 可以推论到所有资源释放函数（如 `fclose(NULL)` 或 `close(-1)` 行为未定义或产生错误）。
5. **错误机械替换反例**：
   ```c
   // 错误反例：提前返回分支遗漏清理，导致内存与句柄严重泄漏
   int process_packet(const uint8_t* data, size_t len) {
       char* buf = (char*)malloc(len);
       FILE* fp = fopen("log.txt", "w");
       if (len < 4) {
           return -1; // 致命：buf 未 free，fp 未 fclose！
       }
       // ... 正常处理 ...
       fclose(fp);
       free(buf);
       return 0;
   }
   ```
6. **不确定性处理**：若源 C++ 对象的生命周期被转移（如通过 `std::move` 转交给全局容器或另一个长期对象），禁止转换为函数级局部 `goto cleanup`，必须追溯其所有权终点并设计显式的所有权交接函数。
7. **官方依据**：[WG21-N4659 Clause 15.4, Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[WG14-N1570 §6.8.6.1, §7.22.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 2：C++ 异常处理机制向 C11 显式错误码与状态传播降级映射

1. **触发条件**：C++ 源码中使用 `throw` 抛出异常，并由外层调用链中的 `try ... catch` 捕获处理。
2. **适用前提**：源语言 ISO C++17，目标语言 ISO C11；目标函数签名允许修改返回值或增加状态出参。
3. **应保留行为**：保持错误发生时的错误类型/错误码、错误信息可观察性；保持异常中断后续语句执行并逐层回退调用栈的控制流拓扑。
4. **可选映射与不适用条件**：
   - *可选映射*：将函数返回值重构为 `int` 错误码（`0` 表示成功，非 `0` 表示具体错误枚举），原返回值转为出参指针（`T* out_result`）；调用方每一处调用后显式检查错误码并向上回退；
   - *不适用条件*：严禁使用 C 标准库的 `setjmp`/`longjmp` 来模拟异常处理（`longjmp` 跳过调用帧局部资源清理导致泄漏）；严禁将未处理的异常静默忽略。
5. **错误机械替换反例**：
   ```c
   // 错误反例：删除 throw 却未向调用方传递错误状态，导致上层在无效数据上继续执行
   int parse_int(const char* s, int* out) {
       if (!s) {
           // 机械删除了 throw std::invalid_argument("null");
           // 却未设置错误码或直接返回，导致调用方误认为成功
       }
       *out = atoi(s); // 若 s 为 NULL 则触发段错误崩溃！
       return 0;
   }
   ```
6. **不确定性处理**：若 C++ 源码捕获的是第三方库未文档化的未知异常（如 `catch (...)`），必须在 C 错误码中预留 `ERR_UNKNOWN`，并记录日志或向调用方暴露未分类失败状态，标注异常语义不确定性。
7. **官方依据**：[WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[WG14-N1570 §7.5, §7.13](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 3：C++ 类继承、虚函数（`virtual`）向 C11 结构体与函数指针虚表映射

1. **触发条件**：C++ 源码中定义包含 `virtual` 虚函数的类、单继承派生类，并通过基类指针/引用调用虚函数实现动态多态。
2. **适用前提**：源语言 ISO C++17，目标语言 ISO C11。
3. **应保留行为**：保持运行时根据对象实际派生类型调用对应实现的动态分派机制；保持基类到派生类成员的内存连续与访问正确。
4. **可选映射与不适用条件**：
   - *可选映射*：在 C11 中显式定义虚表结构体（包含各个虚函数指针）；基类结构体首字段放置指向虚表的指针 `const struct VTable* vptr;`；派生类结构体首字段嵌套基类实例以保证结构体首地址指针可安全强转为基类指针（单继承兼容）；
   - *不适用条件*：若派生类数目固定且很少（如 2~3 个），亦可映射为标签联合（Tagged Union + `switch` 分派），但不适用于可扩展场景；多继承在 C 中涉及复杂的指针偏移计算，需单独手工处理，不可机械转换。
5. **错误机械替换反例**：
   ```c
   // 错误反例：派生结构体未在首字段内嵌基类，导致类型转换后指针偏移错位，内存访问错乱
   struct Base { const struct VTable* vptr; int id; };
   struct Derived {
       int extra_flag; // 错误：把派生字段放在最前面，破坏了 Base 的内存对齐！
       struct Base base;
   };
   // ((struct Base*)derived_ptr)->vptr 将读取到 extra_flag，引发野指针崩溃！
   ```
6. **不确定性处理**：若源 C++ 使用了 RTTI（`dynamic_cast` 或 `typeid`），降级至 C 时必须在基类结构体中显式增加 `int type_tag` 标识，并在类型转换前做显式校验；若继承体系包含复杂的虚继承，应标记为结构性不确定并提请架构审阅。
7. **官方依据**：[WG21-N4659 Clause 13, Clause 13.3, Clause 13.3.2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[WG14-N1570 §6.2.5, §6.7.2.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 4：C++ 函数模板与类模板向 C11 单态化（Monomorphization）与独立前缀命名映射

1. **触发条件**：C++ 源码中使用 `template <typename T>` 定义模板函数或模板类，并在程序中以若干具体类型（如 `int`, `double`, `const char*`）进行了具现化（Instantiation）。
2. **适用前提**：源语言 ISO C++17，目标语言 ISO C11；源码中所有被实际调用的具体类型参数集合可完全枚举。
3. **应保留行为**：针对每种具体类型保留各自特化的独立代码逻辑与数据类型安全，保持运算精度与内存大小不变。
4. **可选映射与不适用条件**：
   - *可选映射*：采用显式单态化（Monomorphization）技术：为每个实际具现化的类型生成一个独立的 C 结构体和函数，并使用类型后缀进行命名区分（如 `Vector_int`、`Vector_int_push_back`、`Vector_float`）；
   - *不适用条件*：严禁一律将所有泛型指针降级为 `void*`，因为 `void*` 会抹除对象真实大小（`sizeof(T)`）、破坏类型安全、阻碍编译器算术优化，且对于值类型必须引入非必要的额外堆内存分配。
5. **错误机械替换反例**：
   ```c
   // 错误反例：将所有泛型容器降级为 void* 数组，丢失值语义并引入非必要堆分配与类型失真
   struct GenericVector { void** items; size_t count; };
   // 存储 int 时必须每个 int 单独 malloc(sizeof(int))，内存碎片暴增，缓存局部性彻底丧失
   ```
6. **不确定性处理**：若模板包含高度复杂的 SFINAE（`std::enable_if_t`）条件特化，必须静态提取其在当前源码中实际命中的具现化版本，对未使用的特化分支进行剪枝，并记录裁剪理由。
7. **官方依据**：[WG21-N4659 Clause 17, Clause 17.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[WG14-N1570 §6.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

## 四、跨场景与系统规则按需加载

> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

- **网络与套接字调用**：当 C++ 源码中出现网络通信、套接字调用时，加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)；跨 POSIX/Windows 平台时加读 [`skills/systems/posix-winsock/SKILL.md`](../../systems/posix-winsock/SKILL.md)。
- **文件 I/O 与路径**：源码中存在文件读写时，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)；跨 OS 路径加载 [`skills/systems/posix-windows-filesystem/SKILL.md`](../../systems/posix-windows-filesystem/SKILL.md)。
- **并发与原生线程**：源码中使用 `std::thread` 或互斥锁时，加读 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)；跨平台线程原语加读 [`skills/systems/posix-windows-threads/SKILL.md`](../../systems/posix-windows-threads/SKILL.md)。

---

## 五、模型自检与质量结论声明

1. **模型自检性质**：转换模型生成的 C11 代码必须做一次内部静态核查，清点所有函数分支是否均已显式闭合资源释放路径、错误码是否逐层向上传递。该自检是**模型自评**，严禁标记为编译通过或语法无误。
2. **语法与行为结论分离**：因当前方向处于 `未验证/阻断` 状态，任何生成的 C 代码在未经独立第三方工具链真实编译之前，一律保持 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`；绝对不宣称转换成功或行为等价。
