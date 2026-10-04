---
name: go-to-c
description: Use when converting Go source code (Go 1.27) to C (ISO C11) while preserving observable behavior; covers goroutines/channels without built-in equivalents, slice triplet & reallocation, interface dynamic types, GC to explicit lifecycle, defer, and error/panic boundaries. Not for C to Go or other language pairs.
---

# Go → C 语言转换规则

> **适用基线**：源语言 Go 1.27 ([GO-SPEC](https://go.dev/ref/spec), [GO-RT-DOC](https://go.dev/doc/gc-guide)) → 目标语言 ISO C11 ([WG14-N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf))
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 C](../../references/languages/c.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/go-to-c/README.md)；候选、冻结任务与第三方回传须分层记录。
> **真实构建证据口径**：当前仓库中 Go→C 方向处于**`未验证/阻断`**状态（尚无项目级目标编译 PASS 证据）；本 Skill 仅提供静态决策依据，不代表转换产物已通过编译或功能验证。
> **规范硬约束**：严格遵循 Go 1.27 语言规范与 ISO C11 标准；C 语言无内建并发等价物，语言级并发契约丢失，需根据调用语义选择单线程顺序化、事件循环或工作池；若需系统级线程库则委托 B 类 Skill。

---

## 一、适用范围与前提

用于将已有 Go 1.27 代码降级转换为 ISO C11 代码。转换的核心挑战在于**将 Go 深度绑定的运行时特性（运行时调度器、Goroutine、Channel、动态三色标记清除 GC、切片自动扩容）解构为 C11 显式的数据结构、手动内存分配与底层同步原语**。严禁做简单机械的 API 替换，必须在理解原程序并发与生命周期契约的前提下重构。

---

## 二、转换时优先守住的行为

- **并发模型与调度选型**：Go 的 Goroutine 是轻量用户态任务，Channel 包含线程安全的阻塞与唤醒机制。**C 无语言内建并发等价物，语言级并发契约丢失**。必须按业务场景在单线程顺序化、工作池或事件循环中作案例级选型；若需系统级线程库则委托 B 类 Skill。
- **切片三元组与重分配分离**：Go 切片由 `(Data, Len, Cap)` 组成。当 `append` 导致扩容时，Go 会分配新底层数组，原切片引用的底层数组与新数组自此脱钩。在 C 中必须显式定义类似结构体，并在重新分配内存后准确处理指针重定向与旧指针失效。
- **内存生命周期与所有权转移**：Go 具备自动垃圾收集（GC），局部变量可安全返回（由编译器逃逸分析自动分配至堆）；在 C 中严禁返回指向局部栈变量的指针！所有逃逸对象必须在堆上显式 `malloc`，并明确指定唯一的所有权释放点。
- **`defer` 与多出口资源清理**：Go 的 `defer` 确保在函数返回前按 LIFO 逆序确定性执行；C 必须通过显式构造的 `goto cleanup` 标签块实现等价清理，确保所有提前返回分支均无资源泄漏。

---

## 三、七段式核心转换规则

### 规则 1：Go Goroutine 与 Channel 向 C 并发架构决策与委托选型

1. **触发条件**：Go 源码中使用 `go worker(...)` 启动并发任务，并通过 `chan T` 信道进行同步、缓冲传输或 `select` 多路复用。
2. **适用前提**：源语言 Go 1.27，目标语言 ISO C11。
3. **应保留行为**：保持任务的计算结果、时序因果关系与外部可观察数据契约；保证无数据竞争（Data Race）。
4. **可选映射与不适用条件**：
   - *可选映射*：C 语言无内建并发原语与调度器，语言级并发契约丢失；需根据调用语义选择单线程顺序化、事件循环或工作池架构设计；
   - *不适用条件*：**严禁在 A 类规则中机械将 goroutine 映射为特定 OS 原生线程创建函数**；若需系统级线程库则委托 B 类 Skill；严禁在未同步的多线程环境下无保护并发读写共享变量。
5. **错误机械替换反例**：
   ```c
   // 错误反例：未理清并发契约，简单忽略同步机制导致数据破坏与逻辑错乱
   void process_items(int* items, size_t count) {
       for (size_t i = 0; i < count; i++) {
           // 错误：在无任何同步或架构调度设计下随意并发调用，产生严重竞态
           run_async_unprotected(&items[i]);
       }
   }
   ```
6. **不确定性处理**：若 Go 源码依赖复杂的信道通信与 Context 级联取消，因 C 语言层缺少等价通信原语，必须在转换报告中明确标注语言级并发模型缺失，提请架构审阅并由 B 类并发 Skill 处理系统级线程与同步细节。
7. **官方依据**：[GO-SPEC #Go_statements, #Channel_types](https://go.dev/ref/spec)；[GO-MEM](https://go.dev/ref/mem)；[WG14-N1570 §7.17, §7.26](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 2：Go 切片三元组与 `append` 扩容机制向 C 手动结构体与连续内存映射

1. **触发条件**：Go 源码中使用切片（`[]T`）、子切片（`s[a:b]`）以及内建 `append(s, item)` 动态追加元素。
2. **适用前提**：源语言 Go 1.27，目标语言 ISO C11。
3. **应保留行为**：保持连续内存布局；保持长度（`len`）与容量（`cap`）语义；当追加超出容量时，保持内存重新分配与已有数据完整性。
4. **可选映射与不适用条件**：
   - *可选映射*：在 C11 中定义包含指针、大小与容量的三元组结构体：
     ```c
     typedef struct { T* data; size_t len; size_t cap; } Slice_T;
     ```
     扩容函数封装 `realloc`，并在容量不足时重新分配内存；
   - *不适用条件*：严禁在追加扩容后继续使用旧结构体中的 `data` 指针（因为 `realloc` 可能在另一个地址分配新内存并释放旧内存，导致持有旧指针的代码发生悬挂解引用）；不可将切片简单退化为固定大小的原生数组。
5. **错误机械替换反例**：
   ```c
   // 错误反例：扩容后外部仍持有旧指针，引发野指针写入与堆破坏
   void append_val(Slice_int* s, int val) {
       if (s->len >= s->cap) {
           s->cap = s->cap ? s->cap * 2 : 4;
           s->data = (int*)realloc(s->data, s->cap * sizeof(int)); // 地址可能已迁移
       }
       s->data[s->len++] = val;
   }
   // 若调用方之前缓存了 int* p = &s->data[0]; 此时 p 已成为悬空野指针！
   ```
6. **不确定性处理**：若源 Go 源码依赖子切片与原切片共享底层数组的联动修改特性（在未扩容前生效，扩容后分离），降级至 C 时必须在注释中显式说明该共享契约，或在调用点严格审查是否产生意外的别名副作用。
7. **官方依据**：[GO-SPEC #Slice_types, #Appending_and_copying_slices](https://go.dev/ref/spec)；[WG14-N1570 §7.22.3.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 3：Go 自动垃圾收集与逃逸变量向 C 显式堆分配与所有权交接映射

1. **触发条件**：Go 源码中函数返回局部变量的指针（如 `func NewObj() *MyStruct { return &MyStruct{...} }`），在 Go 中由编译器逃逸分析自动将其分配到堆上。
2. **适用前提**：源语言 Go 1.27，目标语言 ISO C11。
3. **应保留行为**：确保返回给外部调用者的对象在函数返回后依然驻留合法内存，内容完整且可继续读写；最终在生命周期结束时被彻底释放。
4. **可选映射与不适用条件**：
   - *可选映射*：在 C 函数内部显式使用 `malloc(sizeof(MyStruct))` 在堆上分配，完成字段初始化后返回该指针；同时必须在头文件与接口文档中明确规定**调用方拥有该内存的释放责任（Caller-owns-free）**，或提供配对的 `MyStruct_destroy(MyStruct* p)` 释放函数；
   - *不适用条件*：**绝对禁止在 C 中直接返回局部栈变量的地址**（这是典型的严重 C 缺陷，函数返回后栈帧被覆写，指针立即成为野指针，解引用将造成数据错乱或崩溃）。
5. **错误机械替换反例**：
   ```c
   // 错误反例：直接返回局部栈对象的指针，引发未定义行为（悬挂指针）
   struct Packet* make_packet(int id) {
       struct Packet pkt; // 局部栈变量
       pkt.id = id;
       return &pkt; // 致命错误：返回局部变量地址！函数退出后栈内存立即失效！
   }
   ```
6. **不确定性处理**：若源 Go 代码在复杂闭包或并发任务之间共享对象（缺乏单一清晰的所有权归宿），在 C 中必须引入显式引用计数控制，标注多所有权对象生命周期复杂度。
7. **官方依据**：[GO-SPEC #Variables](https://go.dev/ref/spec)；[GO-RT-DOC](https://go.dev/doc/gc-guide)；[WG14-N1570 §6.2.4](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 4：Go `defer` 语句延迟执行向 C `goto cleanup` 结构化退出映射

1. **触发条件**：Go 源码中使用 `defer res.Close()`、`defer mu.Unlock()` 将资源释放延迟至函数退出。
2. **适用前提**：源语言 Go 1.27，目标语言 ISO C11。
3. **应保留行为**：保证无论正常返回还是发生提早退出分支，已登记的清理动作均按照后进先出（LIFO）的逆序严格执行；保证错误返回值不被破坏。
4. **可选映射与不适用条件**：
   - *可选映射*：在 C 函数底部建立标签链（如 `cleanup_3:`, `cleanup_2:`, `cleanup_1:`），每个提前返回点使用 `ret = ERR; goto cleanup_X;` 跳转至对应位置按序清理；
   - *不适用条件*：严禁在每个 `return` 分支机械重复清理代码（维护成本极高，极易遗漏新增分支）；不可将 Go 中直接写在循环内的 `defer` 盲目映射为函数底部的 `cleanup`（违背了单次迭代清理的原意）。
5. **错误机械替换反例**：
   ```c
   // 错误反例：清理顺序颠倒，导致依赖前置句柄的清理动作失败或段错误
   int do_work(void) {
       void* mem = malloc(100);
       FILE* fp = fopen("data.bin", "rb");
       if (!fp) { free(mem); return -1; }
       // 错误：清理时先释放了数据缓冲区，后试图从 fp 读取残余并关闭
       free(mem);
       fclose(fp); // 若逻辑颠倒或提前释放了关联对象，引发崩溃
       return 0;
   }
   ```
6. **不确定性处理**：若 Go 源码在 `defer` 中修改了具名返回值（如 `defer func() { err = fmt.Errorf(...) }()`），在 C 中必须在 `cleanup` 标签之后提供显式的状态重写逻辑，并标明具名返回值副作用依赖。
7. **官方依据**：[GO-SPEC #Defer_statements](https://go.dev/ref/spec)；[WG14-N1570 §6.8.6.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

## 四、跨场景与系统规则按需加载

> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

- **网络与套接字调用**：当涉及 Go 原生 `net` 包映射至底层 Socket 时，加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)；跨 POSIX/Winsock 时加读 [`skills/systems/posix-winsock/SKILL.md`](../../systems/posix-winsock/SKILL.md)。
- **文件与路径**：当涉及 `os.Open`、`os.PathSeparator` 时，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)；跨 OS 路径分隔符加读 [`skills/systems/posix-windows-filesystem/SKILL.md`](../../systems/posix-windows-filesystem/SKILL.md)。
- **并发与原生线程**：跨 OS 线程调度与系统同步原语加读 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md) 与 [`skills/systems/posix-windows-threads/SKILL.md`](../../systems/posix-windows-threads/SKILL.md)。

---

## 五、模型自检与质量结论声明

1. **模型自检重点**：核对切片边界检查是否完善、循环内 `defer` 是否被正确剥离至子函数、常量溢出是否在编译前消除。该自检属于模型自评，严禁作为编译通过证据。
2. **证据状态声明**：当前 Go→C 方向处于 `未验证/阻断` 状态，在未经独立第三方工具链真实编译之前，一律保持 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`，绝对不宣称转换成功或行为等价。
