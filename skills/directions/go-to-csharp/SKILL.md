---
name: go-to-csharp
description: Use when converting Go source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → C# 语言转换规则

> **适用基线**：Go 1.27 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 C#](../../references/languages/csharp.md)。
> **方向案例与证据**：如本地工作区存在 `docs/test/dataset/go-to-csharp/README.md`，按其中 case 分层查看；该本地数据目录不随 Git/Skill 分发。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Go → C# 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-CS-01：Go 结构体值传递向 C# struct/class 语义划分映射
1. **源码触发条件**：Go 源码中定义 `type Data struct` 并以值接收者 `func (d Data)` 传参。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Struct_types](https://go.dev/ref/spec)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：纯值复制，方法内修改 `d` 不影响外部调用者。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若需保持全量值复制且数据结构较小，声明为 C# `struct`；若为大对象或需支持引用语义，声明为 `class` 并在传参时显式创建副本。
   - *不适用条件*：严禁将值接收者方法所在结构体无脑翻译为 `class`，否则后续调用会产生意外的别名修改副作用。
5. **错误机械替换反例**：
   ```csharp
   // 错误：将 Go 值类型结构体映射为 C# class 导致方法内修改污染外部
   public class Config {
       public int Timeout;
       public void SetTimeout(int t) { this.Timeout = t; }
   }
   // Go 原型为值接收者，调用后外部 Config 未变；C# class 会直接修改外部对象！
   // 正确：使用 struct 保持值语义
   public struct Config {
       public int Timeout;
   }
   ```
6. **信息不足或实现相关时的处理**：若结构体包含大量字段，标记性能权衡并提示用户选择。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)；[GO-SPEC #Struct_types](https://go.dev/ref/spec)。

### 规则 GO-CS-02：Go error 返回向 C# 结构化异常抛出映射
1. **源码触发条件**：Go 源码中使用 `return nil, errors.New("not found")`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）。
3. **原可观察行为**：调用方必须显式判断 `err != nil`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为抛出对应的 C# 异常（如 `throw new KeyNotFoundException(...)`）；或者若该错误属于频繁发生的常规分支，提供形如 `bool TryGetValue(...)` 的 Try 模式方法。
   - *不适用条件*：严禁将业务失败静默忽略。
5. **错误机械替换反例**：
   ```csharp
   // 错误：为了强行对应多返回值，在 C# 中返回二元元组且不加强制检查
   public (User, string) FindUser(int id) { ... } // 违背 C# 习惯用法
   // 正确：使用常规异常或 Try 模式
   public bool TryFindUser(int id, out User user) { ... }
   ```
6. **信息不足或实现相关时的处理**：若源错误代码作为系统进程返回码，映射为带退出码的异常。
7. **直接官方 HTTPS 依据链接**：[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)。

### 规则 GO-CS-03：Go context.Context 取消树向 C# CancellationTokenSource 映射
1. **源码触发条件**：Go 源码中使用 `ctx, cancel := context.WithCancel(parentCtx)` 并通过 `<-ctx.Done()` 监听取消。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-PKG-CONTEXT](https://pkg.go.dev/context)）；目标语言 C# 12 / .NET 8（[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)）。
3. **原可观察行为**：父 context 取消级联触发所有衍生子 context 的 Done 通道关闭。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `CancellationTokenSource.CreateLinkedTokenSource(parentToken)` 构造级联取消令牌源，向异步方法传递 `cts.Token`。
   - *不适用条件*：必须注意 `CancellationTokenSource` 实现了 `IDisposable`，必须在使用完成后显式调用 `Dispose()` 释放底层定时器或句柄资源。
5. **错误机械替换反例**：
   ```csharp
   // 错误：使用带超时的 CTS 未释放导致定时器资源泄漏
   public async Task RunWithTimeout() {
       var cts = new CancellationTokenSource(1000); // 实现了 IDisposable！
       await DoWorkAsync(cts.Token);
       // 缺少 cts.Dispose()！
   }
   // 正确：使用 using 语句
   public async Task RunWithTimeout() {
       using var cts = new CancellationTokenSource(1000);
       await DoWorkAsync(cts.Token);
   }
   ```
6. **信息不足或实现相关时的处理**：若 context 携带 Value 数据，转换为基于 `AsyncLocal<T>` 或显式参数传递。
7. **直接官方 HTTPS 依据链接**：[MS-CS-CANCEL](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)；[GO-PKG-CONTEXT](https://pkg.go.dev/context)。

### 规则 GO-CS-04：Go 切片/string 向 C# T[]、Span<T> 与 List<T> 的长度容量语义映射
1. **源码触发条件**：Go 源码使用 `make([]T, 0, n)` 预分配容量、`items = append(items, x)` 追加、`metas[:min(len(metas), 15)]` 截断、`string(bytes.ToUpper([]byte(outText)))` 或 `[]byte(content)` 做字节/文本互转（如 `doc_zip_chunk_upload.go` 的 `make([]FileMeta, 0, n)`、`local_tasking_workers.go` 的 `results[:min(30, len(results))]`）。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Slice_types](https://go.dev/ref/spec)）；目标语言 C# 12 / .NET 8（[MS-CS-ARRAY](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/arrays/)、[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1)）。
3. **原可观察行为**：`len` 是元素个数，`cap` 是已分配容量，容量只影响是否重分配而不影响可观察内容；子切片与截断结果共享底层数组直到扩容；`[]byte` 与 `string` 的互转按字节与 UTF-8 编码解释，长度按字节计。
4. **目标可选写法和不适用条件**：
   - *可选映射*：元素个数固定用 `T[]`，`new T[n]` 的 `Length` 直接对应 `len`；需要追加与容量增长用 `List<T>`，`new List<T>(capacity: n)` 承接 Go 的容量提示而不是长度；只做只读借用时用 `ReadOnlySpan<T>`/`Span<T>` 切片（`span.Slice(offset, length)`）避免拷贝；字符串与字节互转显式用 `Encoding.UTF8.GetBytes/GetString`。
   - *不适用条件*：严禁把 `new List<T>(capacity)` 的容量当成元素个数——`Count` 仍为 0，凡是用“已有元素”遍历或建索引的代码都会立刻越界；严禁把 Go 子切片的别名共享语义套到 `List<T>` 上，`new List<T>(other)` 与 `other.ToArray()` 都是立即产生的独立副本。
5. **错误机械替换反例**：
   ```csharp
   // 错误：把 Go 的 make([]FileMeta, 0, n) 与后续下标写入直接搬过来
   var metas = new List<FileMeta>(capacity: n);
   metas[i] = new FileMeta(...);        // ArgumentOutOfRangeException：Count 仍为 0
   // 正确：容量只是提示；先 Add 或按需 AddRange，再按索引读写
   var metas = new List<FileMeta>(capacity: n);
   metas.Add(new FileMeta(...));         // 对应 Go 的 append
   // 对应 Go 的 metas[:limit] 视图：用切片而不是拷贝
   ReadOnlySpan<FileMeta> head = CollectionsMarshal.AsSpan(metas).Slice(0, limit);
   ```
6. **信息不足或实现相关时的处理**：若源码依赖子切片与原切片共享底层数组的互相写入，必须先确认目标侧是否有意保留该别名关系，标注“切片别名共享是否需保留待确认”，不得用 `T[]`/`List<T>` 的默认拷贝语义默认承接。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Slice_types](https://go.dev/ref/spec)；[MS-CS-ARRAY](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/arrays/)、[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1)。

### 规则 GO-CS-05：Go nil map 与 nil 切片向 C# null 与空集合的可见性区分映射
1. **源码触发条件**：Go 源码声明零值集合后再使用，例如 `var obj map[string]string`、`chunks := map[int][]byte{}`、`var ports []int`、`portList, err := parsePortRange(...)` 失败时 `return nil, ...`，并把它们写入 `map[string]any` 后序列化（如 `c2_task_cycle.go` 的 `var obj map[string]string`、`doc_zip_chunk_upload.go` 的 `keys := make([]int, 0, len(chunks))`）。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Map_types, #Slice_types](https://go.dev/ref/spec)）；目标语言 C# 12 / .NET 8（[MS-CS-NULLABLE](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references)、[MS-CS-JSON](https://learn.microsoft.com/en-us/dotnet/api/system.text.json)）。
3. **原可观察行为**：nil map 可读（返回零值）但写入 panic；nil 切片可 `len`/`range`/`append`；`encoding/json` 把 nil map 与 nil 切片编码为 `null`，把空 map 编码为 `{}`、空切片编码为 `[]`；`len(nil)` 与 `len(空)` 同为 0。
4. **目标可选写法和不适用条件**：
   - *可选映射*：用 `Dictionary<TKey,TValue>` 承接 map，用 `T[]`/`List<T>` 承接切片；若原 Go 代码把 nil 状态对外暴露（写进 JSON、作为返回值被调用方判空），用可空类型（`null`）显式表示 nil，并用 `JsonSerializerOptions` 与 `[JsonIgnore(Condition = ...)]` 之类的显式标注保留 `null` 与 `[]`/`{}` 的区分；需要“读写都要安全”时改用 `new Dictionary<...>()` 并明确写成空集合。
   - *不适用条件*：严禁用 `Enumerable.Empty<T>()`、`Array.Empty<T>()` 或 `new Dictionary<...>()` 统一承接 nil，除非已确认 nil 与空集合在原程序中不可区分——否则 JSON 输出会由 `null` 变成 `[]`、由 `null` 变成 `{}`，调用方的判空分支随之改变；也不得对可空集合省略空值检查后直接 `foreach`（会抛 `NullReferenceException`）。
5. **错误机械替换反例**：
   ```csharp
   // 错误：把 Go 的 var obj map[string]string 零值统一写成空集合，丢失 null 可见性
   var obj = new Dictionary<string, string>();     // Go 中此处是 nil map
   report["payload"] = obj;                        // 原程序序列化为 null，这里是 {}
   // 正确：让可空性与原 Go 状态一一对应
   Dictionary<string, string>? obj = null;         // 对应 Go 的 nil map（只读安全）
   report["payload"] = obj;                        // 序列化仍为 null
   obj ??= new Dictionary<string, string>();       // 真正要写入时才物化为空 map
   ```
6. **信息不足或实现相关时的处理**：若无法确认某个 nil 状态是否可被外部观察（例如只在本文件内读写、从未进入序列化或返回值），必须标注“nil 与空集合是否需区分待确认”，不得自行选择统一策略。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Map_types, #Slice_types](https://go.dev/ref/spec)；[MS-CS-NULLABLE](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references)、[MS-CS-JSON](https://learn.microsoft.com/en-us/dotnet/api/system.text.json)。

### 规则 GO-CS-06：Go 并发汇聚写入共享容器向 C# 线程安全集合与同步的映射
1. **源码触发条件**：Go 源码启动多个 `go func()` 工作协程，用 `sync.WaitGroup` 汇聚，并通过 `sync.Mutex` 保护的切片（`local_tasking_workers.go` 的 `ServerStore.addResult`、`addEvent`）或缓冲 channel（`tcp_port_scanner.go` 的 `portChan`/`openPorts`）收集结果。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Go_statements](https://go.dev/ref/spec)、[GO-MEM](https://go.dev/ref/mem)）；目标语言 C# 12 / .NET 8（[MS-CS-THREADING](https://learn.microsoft.com/en-us/dotnet/standard/threading/)、[MS-CS-CONCCOLL](https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/)）。
3. **原可观察行为**：互斥量保护下对共享切片的追加彼此可见且不撕裂；`wg.Wait()` 之后所有工作协程的结果都已汇聚；channel 接收端在发送端 `close` 后结束 `range`；结果集合的内容集合不依赖调度顺序（但顺序可能不同）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：每任务无共享收集时用 `Task.Run` 配 `Task.WhenAll` 承接 `WaitGroup` 的汇聚语义；确需共享收集时用 `ConcurrentQueue<T>`/`ConcurrentBag<T>`（或 `lock` + `List<T>`、`Interlocked` 计数），在汇聚点之后按需 `ToList()` 并显式排序以固定顺序。
   - *不适用条件*：严禁把 Go 中受 `sync.Mutex` 保护的切片机械写成无同步的 `List<T>.Add`——多线程写入会抛 `InvalidOperationException`（集合迭代 fail-fast）或损坏内部状态；也不得假定 `ConcurrentBag<T>` 等并发集合的枚举顺序稳定，它不承接 Go 侧任何顺序保证。
5. **错误机械替换反例**：
   ```csharp
   // 错误：并发工作协程直接往同一个 List<T> 写入（Go 原型有 sync.Mutex 保护）
   var results = new List<Result>();
   await Task.WhenAll(tasks.Select(t => Task.Run(() => results.Add(Execute(t)))));
   // 正确：用线程安全集合，或在同一把锁下写入
   var results = new ConcurrentQueue<Result>();
   await Task.WhenAll(tasks.Select(t => Task.Run(() => results.Enqueue(Execute(t)))));
   var ordered = results.OrderBy(r => r.Id).ToList();   // 顺序需显式固定
   ```
6. **信息不足或实现相关时的处理**：若源码依赖 channel 的阻塞/缓冲容量与关闭时机来实现背压或终止条件，必须标注“channel 背压与关闭语义在 C# 中无直接对等物，需重新设计”，交由并发场景 Skill 与架构审阅决定，不得声称行为等价。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Go_statements](https://go.dev/ref/spec)；[MS-CS-THREADING](https://learn.microsoft.com/en-us/dotnet/standard/threading/)、[MS-CS-CONCCOLL](https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/)。

### 规则 GO-CS-07：Go `os.WriteFile` 创建权限向 .NET 文件流选项映射
1. **源码触发条件**：Go 在 Unix 目标上用 `os.WriteFile(path, data, 0o644)` 等显式模式创建或截断文件，转换需保留新文件的权限意图。
2. **冻结版本/运行时/API 前提**：Go 1.27 → C# 12 / .NET 8、目标 OS 为 Linux/Unix；`FileStreamOptions.UnixCreateMode` 的设置在 Windows 不受支持，权限还受进程 umask 影响。
3. **原可观察行为**：`os.WriteFile` 创建新文件时使用给定模式并受 umask 约束；已有文件被截断重写时，该模式不重新设置其现有权限。返回的写入错误是否被调用方忽略须按源码保留。
4. **目标可选写法和不适用条件**：用 `FileStreamOptions` 指定 `FileMode.Create`、`FileAccess.Write` 和 `UnixCreateMode`，以 `FileStream` 写入字节；源若写成 `_ = os.WriteFile(...)`，在对应调用范围处理 .NET 的可预期写入异常后继续。若目标为 Windows、权限由外部部署控制，或源码没有显式模式义务，不机械加入 Unix 模式选项。
5. **错误机械替换反例**：
   ```csharp
   File.WriteAllBytes(path, bytes, UnixFileMode.UserRead); // 错误：.NET 8 无此重载
   var options = new FileStreamOptions {
       Mode = FileMode.Create, Access = FileAccess.Write,
       UnixCreateMode = UnixFileMode.UserRead | UnixFileMode.UserWrite |
                        UnixFileMode.GroupRead | UnixFileMode.OtherRead
   };
   using var stream = new FileStream(path, options);
   stream.Write(bytes);
   ```
6. **信息不足或实现相关时的处理**：先查明文件可能已存在、umask、目标 OS 和源是否丢弃错误；未知时不声称最终权限字节或失败路径等价。`File.SetUnixFileMode` 会改变已有文件权限，不能直接充当本例“只在创建时给 mode”的替代。
7. **直接官方 HTTPS 依据链接**：[Go `os.WriteFile`](https://pkg.go.dev/os#WriteFile)；[.NET 8 `File` 方法与重载](https://learn.microsoft.com/en-us/dotnet/api/system.io.file?view=net-8.0)；[.NET `FileStreamOptions.UnixCreateMode`](https://learn.microsoft.com/en-us/dotnet/api/system.io.filestreamoptions.unixcreatemode?view=net-8.0)。
8. **来源与证据边界**：batch-01 B21（`handoff-2026-10-02-d27-autorun-manifest-write-go`）`self-review-1` 指出不存在的 `File.WriteAllBytes(..., UnixFileMode)` 重载，`target.self-repair-1.cs` 改用 `FileStreamOptions`；最终目标侧 build PASS（job `eval-20261005-080811-e6b394d1`）。该证据只证明此目标版本可构建，权限与失败路径行为仍 `UNVERIFIED`。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
