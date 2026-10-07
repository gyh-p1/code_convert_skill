---
name: csharp-to-c
description: Use when converting C# source to C; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → C 语言转换规则

> **适用基线**：C# 12 / .NET 8 → ISO C11。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C#](../../references/languages/csharp.md)与[目标语言 C](../../references/languages/c.md)。
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

### 规则 CS-C-04：C# UTF-16 string 的长度与编码语义向 C11 char*/wchar_t* 及显式长度映射
1. **源码触发条件**：C# 源码用 `string` 完成拼接、查找、截取后跨到字节或原生边界（`allUsers += "\\Microsoft\\Group Policy\\History";`、`user.Substring(user.IndexOf(@"\") + 1)`、`file.Contains("Groups.xml")`、`module.FileName.EndsWith(".dll")`），或把 `string` 交给文件/进程 API（`File.WriteAllText(FilePath, Payload)`）。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/), [MS-DOTNET-API](https://learn.microsoft.com/en-us/dotnet/api/)）；目标语言 ISO C11（[WG14-N1570 §7.23, §7.24](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：`string` 是 UTF-16 代码单元序列，`Length` 按代码单元计数（代理对占 2 个代码单元），允许内部 `\0`；`Substring`/`IndexOf` 的位置是代码单元索引；`File.WriteAllText` 在 .NET Core 上默认按 UTF-8（无 BOM）写入。
4. **目标可选写法和不适用条件**：
   - *可选映射*：内部统一用宽字符（`wchar_t`）+ 显式长度，或只在边界处转成 UTF-8 的 `char*` + 显式字节长度；转换用 `WideCharToMultiByte`（Windows）或 `wcstombs`（须先 `setlocale`，且不得假定其编码为 UTF-8），并以转换函数返回值作为长度；宽字符域的比较/查找用 `wcscmp`/`wcsstr`/`wcsncmp`，需要字节域时再显式转换一次并在注释中写明编码。
   - *不适用条件*：严禁对 UTF-16 缓冲或其转换结果使用 `strlen`/`strcpy`/`printf("%s")`——它们按 1 字节单元计数到首个 `\0`，而 UTF-16 中 ASCII 字符的第二个字节即 `0x00`，长度会被算成 1；严禁把 UTF-16 数据存进 `char*` 后按字节长度回传给托管侧；严禁把 `string.Length` 当字节数（非 ASCII 内容与 UTF-8 字节数不同）。
5. **错误机械替换反例**：
   ```c
   /* 错误：把 UTF-16 字符串按 char* 处理，strlen 在首个 ASCII 字符后即截断 */
   const wchar_t *wide = L"C:\\ProgramData";
   size_t n = strlen((const char *)wide);          /* 致命：结果为 1（'C' 后的 0x00） */
   fwrite(wide, 1, n, f);                          /* 只写出 1 字节，路径内容丢失 */
   /* 正确：显式转换、检查失败、以转换返回值为长度 */
   size_t n2 = wcstombs(dst, wide, sizeof(dst));   /* 失败返回 (size_t)-1，须检查并先 setlocale */
   if (n2 != (size_t)-1) fwrite(dst, 1, n2, f);
   ```
6. **信息不足或实现相关时的处理**：目标是否必须与托管侧文本逐字节一致、目标平台是否提供宽字符 API、是否需要 BOM、以及 `wcstombs` 所依赖的区域设置，都必须停下确认；不得默认按 UTF-8 或本地代码页转换后再当作等价。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §7.23, §7.24](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)；[MS-DOTNET-API](https://learn.microsoft.com/en-us/dotnet/api/)。

### 规则 CS-C-05：C# List<T>/数组/Dictionary 的动态增长与越界语义向 C11 显式容量与 realloc 映射
1. **源码触发条件**：C# 源码用 `List<T>`/数组/`Dictionary<,>` 收集、索引或判存在（`List<String> files = FindFiles(allUsers, "*.xml");`、`Dlls.Add(dllname);`、`Dlls.Contains(modules)`、`foreach (string valuename in keyname)`、`settings.Count != 0`、`parts[0]`）。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-LIST](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1), [MS-CS-ARRAY](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/arrays/)）；目标语言 ISO C11（[WG14-N1570 §7.22.3, §6.5.6](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：`List<T>.Add` 在容量不足时自动扩容并可能迁移底层数组；`T[]` 长度固定，越界索引抛 `IndexOutOfRangeException`；`Dictionary` 查找缺失键抛 `KeyNotFoundException`；`foreach` 期间修改集合抛 `InvalidOperationException`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：C 中显式维护 `T *items; size_t count; size_t capacity;`，插入前检查 `count < capacity`，扩容走 `realloc` 并**只使用返回的新指针**（返回 NULL 时保留旧指针并向上报错）；判存在用显式线性查找或手工哈希表；遍历用 `for (size_t i = 0; i < count; ++i)`，把 `count` 当作独立事实显式传递。
   - *不适用条件*：严禁把 `List<T>.Add` 机械写成 `items[count++] = v` 而不做容量检查（越界写是 UB，可能静默破坏相邻数据）；严禁在 `realloc` 之后继续使用旧指针（地址可能已失效）或把 `realloc` 失败当成功继续写；严禁假定 C 数组越界会给出可捕获的失败（C 无边界检查，越界读是 UB，不会像 `IndexOutOfRangeException` 那样停在确定位置）。
5. **错误机械替换反例**：
   ```c
   /* 错误：List<T>.Add 直译为无容量检查的下标写入，且 realloc 后沿用旧指针 */
   MyItem *items = malloc(4 * sizeof(MyItem));
   size_t count = 0;
   for (size_t i = 0; i < n; ++i) items[count++] = make_item(i);  /* 超过 4 个即越界写（UB） */
   items = realloc(items, (count + 8) * sizeof(MyItem));          /* 未判 NULL */
   /* 正确：显式容量检查 + 只使用 realloc 返回的新指针 */
   size_t capacity = 4;
   if (count == capacity) {
       MyItem *grown = realloc(items, capacity * 2 * sizeof(MyItem));
       if (!grown) return -1;      /* 保留旧指针，避免泄漏 */
       items = grown; capacity *= 2;
   }
   ```
6. **信息不足或实现相关时的处理**：若无法确认集合是否存在容量上限、失败时是否必须继续处理后续元素、或元素是否被外部指针共享（`realloc` 迁移会使这些指针失效），必须停标并向用户确认，不得用"数组足够大"的假设替代容量契约。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §7.22.3, §6.5.6](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[MS-CS-LIST](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1)；[MS-CS-ARRAY](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/arrays/)。

### 规则 CS-C-06：C# object/ToString() 类型擦除与复合格式串向 C11 printf 格式串与显式类型分支映射
1. **源码触发条件**：C# 源码把值放进 `object` 或经 `ToString()` 输出（`Dictionary<string, object> settings;` 后 `kvp.Value.ToString()`），用复合格式串/插值拼消息（`Console.WriteLine("[+] ... {0}\n[+] ... {1} with PID {2}", module.FileName.ToString(), process.ProcessName.ToString(), process.Id.ToString());`、`$"HKLM:\\{autorunLocation} : {binaryPath}"`、`$"HKCU: {AlwaysInstallElevatedHKCU}"`），或用 `string.IsNullOrEmpty` 区分 null 与空串。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/), [MS-DOTNET-API](https://learn.microsoft.com/en-us/dotnet/api/)）；目标语言 ISO C11（[WG14-N1570 §7.21, §7.23](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：`{n}` 按参数位置绑定，占位符序号或个数与实参不匹配时抛 `FormatException`；`Console.WriteLine` 在输出后追加平台换行；`object` 不携带静态类型，`ToString()` 按运行时类型虚分派格式化；拼接与插值产生新字符串。
4. **目标可选写法和不适用条件**：
   - *可选映射*：把复合格式串逐项改写为 C 格式串，并**按每个实参的 C 类型选择转换说明**（`const char *` 用 `%s`、`int` 用 `%d`、`size_t` 用 `%zu`、指针用 `%p`），保持参数顺序一一对应；`Console.WriteLine(s)` 映射为 `printf("%s\n", s)` 或 `fputs` 加换行；需要按运行时类型分流的 `object` 值，在 C 中用显式类型标签/联合或先分支再格式化。
   - *不适用条件*：严禁把 `{n}` 直接改写成 `%` 而不核对参数个数、顺序与 C 类型（`printf` 的转换说明与实参类型不匹配是 UB，而不是可捕获异常）；严禁把 `object`/`ToString()` 的结果当成已知 C 类型继续使用（类型信息已丢失）；严禁把 `string.IsNullOrEmpty(x)` 机械写成单个 `if (!x)`（null 与空串是两种不同状态，C 中必须分别判断）；对 `Regex`、`string.Split` 等无 C 标准库等价物的 API，必须显式标注为"需外部库或行为降级"，不得静默改写。
5. **错误机械替换反例**：
   ```c
   /* 错误：{0}/{1}/{2} 直译为三个 %s，但第三个实参是整数 PID；null 与空串也未区分 */
   printf("[+] Hijackable DLL: %s\n[+] Associated Process is %s with PID %s\n",
          module->name, proc->name, proc->id);   /* 危险：%s 读到整数 → UB */
   /* 正确：逐个按 C 类型选择转换说明 */
   printf("[+] Hijackable DLL: %s\n[+] Associated Process is %s with PID %d\n",
          module->name, proc->name, proc->id);
   ```
6. **信息不足或实现相关时的处理**：源 `object` 的实际运行时类型、每个占位符的目标格式（宽度/进制/大小写）、是否必须保留 `Console.WriteLine` 的换行，都必须停下确认；缺失的 BCL 专属设施（正则、集合判存在、`string.Split`）必须列为知识缺口而不是静默降级。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §7.21, §7.23](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)；[MS-DOTNET-API](https://learn.microsoft.com/en-us/dotnet/api/)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
