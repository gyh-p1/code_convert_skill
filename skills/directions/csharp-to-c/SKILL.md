---
name: csharp-to-c
description: Use when converting C# source to C; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → C 语言转换规则

> **适用基线**：C# 12 / .NET 8 → ISO C11。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C#](../../references/languages/csharp.md)与[目标语言 C](../../references/languages/c.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/csharp-to-c/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C# → C 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CS-C-01：C# 引用类型与托管堆对象向 C 显式 malloc/free 结构体映射
1. **源码触发条件**：C# 源码中定义 `class` 并通过 `new` 频繁分配对象，依赖 CoreCLR GC 自动回收。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types), [MS-CS-GC](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals)）；目标语言 ISO C11（[WG14-N1570 §7.22.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：对象由 GC 在分代回收时自动清除，无内存悬垂，无需手动跟踪生命周期。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 C 语言堆分配结构体指针，并在模块中显式设计构造（`xxx_create`）与销毁（`xxx_destroy`）函数；若生命周期局限在函数内，优先转换为栈上局部结构体。
   - *不适用条件*：严禁在 C 中遗漏对称的 `free`；严禁重复释放或在 `free` 后解引用野指针。
5. **错误机械替换反例**：
   ```c
   // 错误：函数提前返回分支遗漏 free，引发严重内存泄漏
   MyObject* obj = my_object_create();
   if (!validate(obj)) {
       return -1; // 错误：未调用 my_object_destroy(obj) 导致泄漏！
   }
   // 正确：使用 goto cleanup 或显式逐分支释放
   if (!validate(obj)) {
       my_object_destroy(obj);
       return -1;
   }
   ```
6. **信息不足或实现相关时的处理**：若对象所有权涉及跨线程传递，标明所有权转移契约并生成文档注释。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §7.22.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[MS-CS-GC](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals)。

### 规则 CS-C-02：C# 结构化异常体系向 C 整数错误码与返回值分流降级映射
1. **源码触发条件**：C# 源码中使用 `throw new MyException(...)` 中断控制流并在上层捕获。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）；目标语言 ISO C11（[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：抛出异常后触发运行时栈展开，跳过中间代码直到 catch 块。
4. **目标可选写法和不适用条件**：
   - *可选映射*：将函数返回值定义为 `int` 错误码（`0` 表示成功，非零/负数表示具体错误），原返回值改用指针输出参数返回；调用点逐层使用 `if (err != 0)` 检查。
   - *不适用条件*：C 语言无语言级异常展开，严禁在 C 生产代码中滥用 `setjmp`/`longjmp` 模拟高级异常。
5. **错误机械替换反例**：
   ```c
   // 错误：将 C# 抛出异常忽略，导致调用方在错误状态下继续使用未初始化数据
   // C# 原型: int Parse(string s) => throw new FormatException();
   int parse(const char* s, int* out_val) {
       // 未做错误处理直接返回
       *out_val = 0;
       return -1; // 必须返回明确错误码！
   }
   ```
6. **信息不足或实现相关时的处理**：若 C# 异常携带特定上下文消息，在 C 中定义全局或线程局部的错误缓冲区。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)；[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

### 规则 CS-C-03：C# async/await 异步任务向 C 同步阻塞或回调状态机降级映射
1. **源码触发条件**：C# 源码中使用 `async Task<int>` 与 `await` 异步调用。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)）；目标语言 ISO C11。
3. **原可观察行为**：调用点在等待 I/O 时让出线程，由 .NET 运行时状态机恢复执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：降级为标准同步阻塞函数（若并发性能非强要求）；若必须保持异步，手工实现带结构体上下文的状态机或显式事件循环。
   - *不适用条件*：严禁在 C 中留下伪异步占位代码，必须明确其同步或回调模型。
5. **错误机械替换反例**：
   ```c
   // 错误：在 C 中简单将 async 方法写为直接返回，未处理尚未完成的异步任务
   // 导致数据竞争或未完成读取
   ```
6. **信息不足或实现相关时的处理**：若涉及套接字异步多路复用，加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
