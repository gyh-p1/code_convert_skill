---
name: go-to-c
description: Use when converting Go source code (Go 1.27) to C (ISO C11) while preserving observable behavior; covers goroutines/channels without built-in equivalents, slice triplet & reallocation, interface dynamic types, GC to explicit lifecycle, defer, and error/panic boundaries. Not for C to Go or other language pairs.
---

# Go → C 语言转换规则

> **适用基线**：源语言 Go 1.27 ([GO-SPEC](https://go.dev/ref/spec), [GO-RT-DOC](https://go.dev/doc/gc-guide)) → 目标语言 ISO C11 ([WG14-N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf))
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 C](../../references/languages/c.md)。
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

### 规则 5：Go 多返回值 `(T, error)` 向 C 返回码加出参指针映射

1. **触发条件**：Go 源码中函数以 `(T, error)`、`([]byte, error)` 或 `(T, bool)` 返回（如 `obfuscateData(data []byte, key []byte) ([]byte, error)`、`parsePorts(portStr string) ([]int, error)`），调用方以 `if err != nil` 分流。
2. **适用前提**：源语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec)）；目标语言 ISO C11（[WG14-N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **应保留行为**：失败时调用方能观察到“无结果”这一事实，且失败原因可区分；成功时调用方能取到完整结果与真实长度；失败路径不得让调用方读到未初始化的出参。
4. **可选映射与不适用条件**：
   - *可选映射*：以 `int`（或自定义 `enum`）返回码表示错误类别，结果与长度通过出参指针回传，例如 `int obfuscate_data(const uint8_t* in, size_t in_len, const uint8_t* key, uint8_t** out, size_t* out_len);`；错误详情用线程局部的错误信息缓冲区或错误结构体另行回传；不可恢复的致命故障才用 `abort()`，不把 `panic` 机械写成 `exit`。
   - *不适用条件*：严禁在错误路径上“`goto cleanup` 后又落到成功标签”而把未初始化的出参交回调用方；严禁把 Go 中“成功但值为零值”（如长度为 0 的结果、`false` 的第二返回值）与“失败”合并成同一个返回码——这会让调用方无法区分两者。
5. **错误机械替换反例**：
   ```c
   // 错误反例：用指针返回值表达一切，失败返回 NULL 且无法区分“空结果”
   uint8_t* obfuscate_data(const uint8_t* in, size_t n, size_t* out_len) {
       if (n == 0) { return NULL; }          // Go 中这里返回的是 (空切片, nil)：成功！
       /* ... */
       return out;                            // *out_len 未初始化，调用方读到垃圾长度
   }
   // 正确写法：返回码表示成败，出参先置零再按需填充
   int obfuscate_data(const uint8_t* in, size_t n, const uint8_t* key,
                      uint8_t** out, size_t* out_len) {
       *out = NULL; *out_len = 0;             // 失败路径也必须留下确定值
       if (n == 0) { return 0; }              // 空输入成功，结果为空，长度 0
       /* ... 分配并填充 *out / *out_len，失败时释放并返回非零错误码 ... */
       return 0;
   }
   ```
6. **不确定性处理**：若 Go 源码用 `errors.Is`/类型断言/`%w` 包装区分错误类别，而 C 侧尚未冻结错误码到类别的对应表，必须停下标注“错误分类映射待确认”，不得自行编造错误码取值。
7. **官方依据**：[GO-SPEC #Errors](https://go.dev/ref/spec)；[WG14-N1570 §6.8.4.1, §7.22.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 6：Go 切片向 C 指针加长度对映射与“禁止以 NUL 终止符推断长度”

1. **触发条件**：Go 源码在字节/字符序列上使用切片、子切片与 `append`，例如 `data[k:blockSize]`、`ciphertext[aes.BlockSize:]`、`append(data, padText...)`、`hex.EncodeToString(sum[:])`，以及 `string(output)` 与 `[]byte(text)` 互转。
2. **适用前提**：源语言 Go 1.27（[GO-SPEC #Slice_types](https://go.dev/ref/spec)）；目标语言 ISO C11（[WG14-N1570 §7.24](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **应保留行为**：元素总数（`len`）是内容的一部分；字节切片允许在任意位置包含 `0x00`（如 AES-IV 前缀与分组密文）；子切片在未扩容前与原切片共享底层数组，写入可通过两条路径被观察到。
4. **可选映射与不适用条件**：
   - *可选映射*：用“指针 + 显式长度”表示连续序列，例如 `typedef struct { uint8_t* data; size_t len; } Bytes;`，或以 `(const uint8_t* buf, size_t buf_len)` 成对传参；每次取子切片都重新计算指针偏移与长度，并把长度来源（容器元数据还是调用方实参）写在注释与接口文档中。
   - *不适用条件*：**严禁用 `strlen`/`strcpy`/`strcat` 等 NUL 终止符函数处理由 Go `string`/`[]byte` 映射而来的数据**：内部含 `0x00` 的内容会被截断，未以 `0x00` 结尾的缓冲区会被越界读取（未定义行为）；`strlen` 的返回值不是 `len`，在等长比较、长度字段与完整性校验上会静默产生错误；也不得直接对未终止缓冲区调用 `printf("%s")`。
5. **错误机械替换反例**：
   ```c
   // 错误反例：把 Go 的 len(decrypted) 换成 strlen，忽略分组密文中的 0x00
   Bytes deobfuscate(const uint8_t* data) {
       Bytes r;
       r.data = (uint8_t*)data;
       r.len  = strlen((const char*)data);   // 密文/IV 含 0x00 时此处立即截断
       return r;
   }
   // 正确写法：长度沿用 Go 侧已有的 len 语义显式传递
   int deobfuscate(const uint8_t* data, size_t data_len, Bytes* out) {
       if (data_len < 16) { return ERR_TRUNCATED; }  // 对应 len(decoded) < aes.BlockSize
       /* 以 data_len 为准做全部边界判断与拷贝，绝不调用 strlen */
       return 0;
   }
   ```
6. **不确定性处理**：若无法确定某缓冲区当前长度是来自容器元数据还是调用方实参，或该缓冲区是否被推断为 NUL 结尾，必须标注“长度来源与终止符约定待确认”而不得默认补 `'\0'`。
7. **官方依据**：[GO-SPEC #Slice_types, #String_types](https://go.dev/ref/spec)；[WG14-N1570 §6.4.5, §7.24.6.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

---

### 规则 7：Go 并发结果汇聚向 C11 `_Atomic`/`<threads.h>` 同步基元的委托边界

1. **触发条件**：Go 源码用多个 `go worker(...)` 处理任务队列并把结果写入共享可变状态（如全局 `openPorts` 上的 `mu.Lock()`/`openPorts = append(openPorts, port)`、`var wg sync.WaitGroup` 配 `defer wg.Done()` 的汇聚、`atomic` 计数），再在主流程 `wg.Wait()` 后汇总。
2. **适用前提**：源语言 Go 1.27（[GO-SPEC #Go_statements](https://go.dev/ref/spec)、[GO-MEM](https://go.dev/ref/mem)）；目标语言 ISO C11（[WG14-N1570 §7.17, §7.26](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **应保留行为**：任一时刻对同一共享对象的读写都被同步；汇聚点之后的汇总结果包含全部已完成任务的结果，且不含撕裂读写入的半成品元素；任务计数与完成计数不丢失。
4. **可选映射与不适用条件**：
   - *可选映射*：先用 `_Atomic size_t` 表达完成计数与无锁标志（注意 C11 不保证每个 `_Atomic` 类型无锁，必要时回退为“互斥量保护普通变量”）；需要“保护共享容器 + 阻塞等待任务 + 汇聚”时，用 `mtx_t`/`cnd_t` 实现带条件的队列并由一个汇聚线程取结果；线程创建与取消等系统级细节委托 B 类并发 Skill（[`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)、[`skills/systems/posix-windows-threads/SKILL.md`](../../systems/posix-windows-threads/SKILL.md)）。若 `<threads.h>` 在目标工具链缺失，则整个并发方案需重新选型而不在本 A 类规则内决定。
   - *不适用条件*：严禁在 `mtx_lock` 保护下执行可能阻塞或再次取同一把锁的操作（包括写日志、分配内存、调用回调）；严禁把 Go 习惯的“每个写者各自 `append`”直接搬成无锁的 `realloc` 追加序列——`realloc` 迁移地址且并发访问未同步属于未定义行为；不得把 `sync.WaitGroup` 机械写成忙等 `while (done < n);`。
5. **错误机械替换反例**：
   ```c
   // 错误反例：把 Go 侧受 sync.Mutex 保护的计数与追加改成无同步访问
   static size_t done;
   static int* open_ports;
   static size_t open_len;
   void scan_worker(void* arg) {
       done++;                                            /* 未同步：丢计数 */
       open_ports = realloc(open_ports, (open_len + 1) * sizeof(int)); /* 并发 realloc */
       open_ports[open_len++] = *(int*)arg;               /* 撕裂写入，长度已失真 */
   }
   // 正确写法：计数用原子类型，容器与长度成对由同一把互斥量保护
   static _Atomic size_t done;
   static mtx_t ports_mtx;
   static int* open_ports;
   static size_t open_len;
   void scan_worker_correct(void* arg) {
       mtx_lock(&ports_mtx);
       int* grown = realloc(open_ports, (open_len + 1) * sizeof(int));
       if (grown) { open_ports = grown; open_ports[open_len++] = *(int*)arg; }
       mtx_unlock(&ports_mtx);
       atomic_fetch_add_explicit(&done, 1, memory_order_release);
   }
   ```
6. **不确定性处理**：若源码依赖 `select` 多路复用、`context.Context` 级联取消或 channel 关闭的可观察语义，必须标注“语言级通信与取消语义在 C 中缺失”，交由 B 类 Skill 与架构审阅决定等价方案，不得声称行为等价。
7. **官方依据**：[GO-SPEC #Go_statements](https://go.dev/ref/spec)；[GO-MEM](https://go.dev/ref/mem)；[WG14-N1570 §7.17.7, §7.26.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

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
