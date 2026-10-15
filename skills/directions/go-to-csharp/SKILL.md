---
name: go-to-csharp
description: Use when converting Go source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → C# 语言转换规则

> **适用基线**：Go 1.27 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 Go](../../references/languages/go.md)与[目标语言 C#](../../references/languages/csharp.md)，按源码选择适用规则。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Go → C# 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-CS-01：Go 结构体值传递向 C# struct/class 语义划分映射
1. **源码触发条件**：Go 源码中定义 `type Data struct` 并以值接收者 `func (d Data)` 传参。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Struct_types）；目标语言 C# 12 / .NET 8（MS-CS-SPEC）。
3. **原可观察行为**：接收者值复制，直接修改其值字段不改变调用者的结构体；指针、切片、map 等字段仍可能共享底层对象，通过它们写入可被外部观察，不作深复制保证。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按字段保留 Go 接收者副本及引用字段的共享。C# struct 只是候选：在可变变量上调用会修改 this 的实例方法不自动产生 Go 值接收者副本，须显式按值参数/副本承接；class 候选也须对应复制与别名行为，不能只按大小选型。
   - *不适用条件*：严禁将值接收者方法所在结构体无脑翻译为 `class`，否则后续调用会产生意外的别名修改副作用。
5. **错误机械替换反例**：
   ```csharp
   // 错误：将 Go 值类型结构体映射为 C# class 导致方法内修改污染外部
   public class Config {
       public int Timeout;
       public void SetTimeout(int t) { this.Timeout = t; }
   }
   // Go 原型为值接收者，调用后外部 Config 未变；C# class 会直接修改外部对象！
   // 候选数据表示：struct 本身不保证其可变实例方法等价于 Go 值接收者
   public struct Config {
       public int Timeout;
   }
   ```
6. **信息不足或实现相关时的处理**：若结构体包含大量字段，标记性能权衡并提示用户选择。
7. **资料依据（名称/版本/章节）**：MS-CS-SPEC；GO-SPEC #Struct_types。

### 规则 GO-CS-02：Go error 返回向 C# 结构化异常抛出映射
1. **源码触发条件**：Go 源码中使用 `return nil, errors.New("not found")`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 C# 12 / .NET 8（MS-CS-EXCEPT）。
3. **原可观察行为**：error 经返回值传递；调用方可以检查或忽略，按源实际分流保留。
4. **目标可选写法和不适用条件**：
   - *可选映射*：保留元组/结果对象及实际调用分支；接口与整条传播边界均允许时才考虑异常或 Try 模式。错误字段、身份与成功零值不能丢失。
   - *不适用条件*：不得新增或删除源的忽略分支，也不因惯用法禁止元组；频率与风格不能决定是否改接口。
5. **错误机械替换反例**：
   ```csharp
   // 候选：源接口与调用方观察两项结果时保留元组；错误对象类型另按实际字段映射
   public (User, string) FindUser(int id) { ... }
   // 另一候选：仅接口与错误细节允许 Try 模式时适用
   public bool TryFindUser(int id, out User user) { ... }
   ```
6. **信息不足或实现相关时的处理**：若源错误代码作为系统进程返回码，映射为带退出码的异常。
7. **资料依据（名称/版本/章节）**：MS-CS-EXCEPT。

### 规则 GO-CS-03：Go context.Context 取消树向 C# CancellationTokenSource 映射
1. **源码触发条件**：Go 源码中使用 `ctx, cancel := context.WithCancel(parentCtx)` 并通过 `<-ctx.Done()` 监听取消。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-PKG-CONTEXT）；目标语言 C# 12 / .NET 8（MS-CS-CANCEL）。
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
7. **资料依据（名称/版本/章节）**：MS-CS-CANCEL；GO-PKG-CONTEXT。

### 规则 GO-CS-04：Go 切片/string 向 C# T[]、Span<T> 与 List<T> 的长度容量语义映射
1. **源码触发条件**：Go 源码使用 `make([]T, 0, n)` 预分配容量、`items = append(items, x)` 追加、`metas[:min(len(metas), 15)]` 截断、`string(bytes.ToUpper([]byte(outText)))` 或 `[]byte(content)` 做字节/文本互转（如 `doc_zip_chunk_upload.go` 的 `make([]FileMeta, 0, n)`、`local_tasking_workers.go` 的 `results[:min(30, len(results))]`）。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Slice_types）；目标语言 C# 12 / .NET 8（MS-CS-ARRAY、MS-CS-COLL）。
3. **原可观察行为**：len 为元素个数，cap 决定可重切片范围及 append 是否复用数组，别名写入可观察；扩容得到新数组时旧切片仍保留旧数组。Go string 与 []byte 可含非 UTF-8 字节，互转不自动校验/替换这些字节，长度按字节计。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按固定元素/独立追加/共享视图分别核数组、List 或 Span 候选；List 容量不代 Go 可重切片的 cap。文本确有 UTF-8 契约且错误策略一致时才用 Encoding.UTF8；任意字节保留 byte[]。Span 的保活、后续容器扩容与写入权限仍须对应源。
   - *不适用条件*：严禁把 `new List<T>(capacity)` 的容量当成元素个数——`Count` 仍为 0，凡是用“已有元素”遍历或建索引的代码都会立刻越界；严禁把 Go 子切片的别名共享语义套到 `List<T>` 上，`new List<T>(other)` 与 `other.ToArray()` 都是立即产生的独立副本。
5. **错误机械替换反例**：
   ```csharp
   // 错误：把 Go 的 make([]FileMeta, 0, n) 与后续下标写入直接搬过来
   var metas = new List<FileMeta>(capacity: n);
   metas[i] = new FileMeta(...);        // ArgumentOutOfRangeException：Count 仍为 0
   // 正确：容量只是提示；先 Add 或按需 AddRange，再按索引读写
   var metas = new List<FileMeta>(capacity: n);
   metas.Add(new FileMeta(...));         // 对应 Go 的 append
   // 候选只读视图：仅 limit 合法、借用期间 List 不改长度且源不通过此视图写入时适用
   ReadOnlySpan<FileMeta> head = CollectionsMarshal.AsSpan(metas).Slice(0, limit);
   ```
6. **信息不足或实现相关时的处理**：已知源有可观察别名时必须保留，不问目标是否“有意”保留；具体保活/扩容表示未知则记录实现缺口并停止受影响映射，不以默认拷贝代替。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Slice_types；MS-CS-ARRAY、MS-CS-COLL。

### 规则 GO-CS-05：Go nil map 与 nil 切片向 C# null 与空集合的可见性区分映射
1. **源码触发条件**：Go 源码声明零值集合后再使用，例如 `var obj map[string]string`、`chunks := map[int][]byte{}`、`var ports []int`、`portList, err := parsePortRange(...)` 失败时 `return nil, ...`，并把它们写入 `map[string]any` 后序列化（如 `c2_task_cycle.go` 的 `var obj map[string]string`、`doc_zip_chunk_upload.go` 的 `keys := make([]int, 0, len(chunks))`）。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Map_types, #Slice_types）；目标语言 C# 12 / .NET 8（MS-CS-NULLABLE、MS-CS-JSON）。
3. **原可观察行为**：nil map 可读（返回零值）但写入 panic；nil 切片可 `len`/`range`/`append`；`encoding/json` 把 nil map 与 nil 切片编码为 `null`，把空 map 编码为 `{}`、空切片编码为 `[]`；`len(nil)` 与 `len(空)` 同为 0。
4. **目标可选写法和不适用条件**：
   - *可选映射*：可空容器候选须分别实现源 nil map 的读零值、写失败和 nil slice 的 len/range/append；序列化须保留 null 与空容器，而不是一律忽略 null 属性。仅源确有初始化时点才物化 map，不为“读写安全”提前初始化。
   - *不适用条件*：严禁用 `Enumerable.Empty<T>()`、`Array.Empty<T>()` 或 `new Dictionary<...>()` 统一承接 nil，除非已确认 nil 与空集合在原程序中不可区分——否则 JSON 输出会由 `null` 变成 `[]`、由 `null` 变成 `{}`，调用方的判空分支随之改变；也不得对可空集合省略空值检查后直接 `foreach`（会抛 `NullReferenceException`）。
5. **错误机械替换反例**：
   ```csharp
   // 错误：把 Go 的 var obj map[string]string 零值统一写成空集合，丢失 null 可见性
   var obj = new Dictionary<string, string>();     // Go 中此处是 nil map
   report["payload"] = obj;                        // 原程序序列化为 null，这里是 {}
   // 正确：让可空性与原 Go 状态一一对应
   Dictionary<string, string>? obj = null;         // 对应 Go 的 nil map（只读安全）
   report["payload"] = obj;                        // 序列化仍为 null
   // 源若直接写 nil map，应保留其失败；仅对应源显式 make/字面量初始化时才建立 Dictionary。
   ```
6. **信息不足或实现相关时的处理**：若无法确认某个 nil 状态是否可被外部观察（例如只在本文件内读写、从未进入序列化或返回值），必须标注“nil 与空集合是否需区分待确认”，不得自行选择统一策略。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Map_types, #Slice_types；MS-CS-NULLABLE、MS-CS-JSON。

### 规则 GO-CS-06：Go 并发汇聚写入共享容器向 C# 线程安全集合与同步的映射
1. **源码触发条件**：Go 源码启动多个 `go func()` 工作协程，用 `sync.WaitGroup` 汇聚，并通过 `sync.Mutex` 保护的切片（`local_tasking_workers.go` 的 `ServerStore.addResult`、`addEvent`）或缓冲 channel（`tcp_port_scanner.go` 的 `portChan`/`openPorts`）收集结果。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Go_statements、GO-MEM）；目标语言 C# 12 / .NET 8（MS-CS-THREADING、MS-CS-CONCCOLL）。
3. **原可观察行为**：互斥量保护下对共享切片的追加彼此可见且不撕裂；`wg.Wait()` 之后所有工作协程的结果都已汇聚；channel 接收端在发送端 `close` 后结束 `range`；结果集合的内容集合不依赖调度顺序（但顺序可能不同）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：仅调度与等待义务一致时用 Task/WhenAll；共享追加可考虑 lock + List 或对应并发集合。保持源收集/消费顺序；仅源排序或冻结允许差异明确无序时才考虑排序，不能为输出稳定新加业务排序。
   - *不适用条件*：严禁把 Go 中受 `sync.Mutex` 保护的切片机械写成无同步的 `List<T>.Add`——多线程写入会抛 `InvalidOperationException`（集合迭代 fail-fast）或损坏内部状态；也不得假定 `ConcurrentBag<T>` 等并发集合的枚举顺序稳定，它不承接 Go 侧任何顺序保证。
5. **错误机械替换反例**：
   ```csharp
   // 错误：并发工作协程直接往同一个 List<T> 写入（Go 原型有 sync.Mutex 保护）
   var results = new List<Result>();
   await Task.WhenAll(tasks.Select(t => Task.Run(() => results.Add(Execute(t)))));
   // 正确：用线程安全集合，或在同一把锁下写入
   var results = new ConcurrentQueue<Result>();
   await Task.WhenAll(tasks.Select(t => Task.Run(() => results.Enqueue(Execute(t)))));
   var collected = results.ToList(); // 若顺序可观察，集合选择/入队时点仍须对应源；不自动按 Id 排序
   ```
6. **信息不足或实现相关时的处理**：若源码依赖 channel 的阻塞/缓冲容量与关闭时机来实现背压或终止条件，必须标注“channel 背压与关闭语义在 C# 中无直接对等物，需重新设计”，交由并发场景 Skill 与架构审阅决定，不得声称行为等价。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Go_statements；MS-CS-THREADING、MS-CS-CONCCOLL。

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
7. **资料依据（名称/版本/章节）**：Go `os.WriteFile`；.NET 8 `File` 方法与重载；.NET `FileStreamOptions.UnixCreateMode`。

### 规则 GO-CS-08：Go 标准库派生出的宿主元数据必须逐字段保真

1. **源码触发条件**：Go 源码把**标准库派生出的字符串或默认值**写入输出/序列化载荷——`net.Flags` 的 `String()`（`up|broadcast|loopback|pointtopoint|multicast|running`）、`os.Environ()` 的原始条目（**含 `=C:=...` 这类以 `=` 开头的隐藏条目**）、`os/user.Current().Username` 的 `DOMAIN\username` 形式、`http.Client` 的**无超时**行为，或 `time` 格式串；或用**不限定方法**的 `ServeMux` 处理器注册。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（`net.Flags`、`os.Environ`、`http.Client`）；目标语言 C# 12 / .NET 8（`NetworkInterface`、`Environment.GetEnvironmentVariables`、`HttpClient.Timeout`）。
3. **原可观察行为**：
   - `Flags.String()` 按**固定顺序**输出**全部**已置位标志，包括 `multicast` 与 `running`；`.NET` 的 `NetworkInterface` **没有**同构的“标志字符串”概念，`NetworkInterfaceType` 与 `SupportsMulticast`/`OperationalStatus` 是**不同维度**，不能互相推导。
   - `os.Environ()` 返回**原始环境块**，**不剔除**以 `=` 开头的驱动器条目（`=C:=C:\...`）。这些串以 `0x3D` 开头，按字节序排序会**排在最前**，因此是否保留它们会改变“前 N 条”的**成员集合**。
   - `http.Client` **默认无超时**（请求可无限阻塞）；`HttpClient.Timeout` **默认为 100 秒**。这不是“更安全”，而是改变了工作循环的终止时机。
   - `os/user.Current().Username` 在 Windows 上返回 **`DOMAIN\username`** 形式（本机账户为 `MACHINE\user`）；`Environment.UserName` 只返回**裸账户名**，无域前缀。写入 JSON 与摘要行即产生字节差异。
   - Go `ServeMux` 的 `mux.HandleFunc("/task", ...)` **不限定 HTTP 方法**——`POST /task` 与 `GET /register` 都会被接受；若目标把路由硬编码成“方法 + 路径”相等，服务面即被**收窄**。
4. **目标可选写法和不适用条件**：
   - *元数据字符串*：逐字段重建源的**完整集合与顺序**（标志集合、环境条目集合、用户名形式），不得只实现“常见的那几个”。Windows 用户名形式用 `WindowsIdentity.GetCurrent().Name`，或当域非空时拼 `Environment.UserDomainName + "\\" + Environment.UserName`，并保留失败时的原兜底值。
   - *路由契约*：Go `ServeMux` 不限定方法时，目标不得无依据增加方法限制；完整路由接受域、重定向及路径处理仍按实际源注册保持，不把“只按路径相等”当完整ServeMux实现。收窄须有生成前明确许可及冻结范围，事后登记不构成许可。
   - *超时*：源无超时时可用 `HttpClient { Timeout = Timeout.InfiniteTimeSpan }` 保持该设置；**不得**静默引入 100 秒默认值。新增超时须有源语义依据或生成前明确许可，记录其影响；不能仅登记为差异就采用。
   - *不适用条件*：若源码本就给定了超时（`http.Client{Timeout: ...}`），则按源值设置；若源码自身就过滤了某些环境条目、或已按方法分派（显式检查 `r.Method`），则保留源码的逻辑，**不要**以“目标 API 的行为”为由增删过滤或放宽路由。
5. **错误机械替换反例**：
   ```csharp
   // 错误一：只实现部分标志且顺序不同
   var flags = new List<string>();
   if (up) flags.Add("up");
   if (broadcast) flags.Add("broadcast");        // 永远不输出 multicast / running
   // 错误二：用 NetworkInterfaceType 推导 broadcast/pointtopoint（与 Go 的判定依据不同）
   // 错误三：为“稳妥”给无超时的源加上默认超时
   var httpClient = new HttpClient();            // Timeout 默认 100 秒 → 源不会失败处失败
   // 错误四：以注释断言“Go 会省略 =C:= 条目”并据此过滤
   if (key.Length == 0 || key[0] == '=') continue;   // 改变排序后前 15 条的成员
   // 错误五：用裸账户名承接 Go 的 DOMAIN\username
   username = Environment.UserName;                  // 缺少域前缀 → JSON 与摘要行字节不同
   // 错误六：把不限定方法的路由收窄为“方法 + 路径”相等
   if (path == "/task" && method == "GET") { ... } else { WriteResponse(stream, 404, ...); }
   // 局部候选：下列各行分别须满足对应源字段/消费者前提，不构成整段等价实现
   if (nic.SupportsMulticast) flags.Add("multicast");       // 按 Go 的顺序追加
   if (nic.OperationalStatus == OperationalStatus.Up) flags.Add("running");
   var httpClient = new HttpClient { Timeout = Timeout.InfiniteTimeSpan };
   if (key.Length == 0) continue;                            // 仅处理空键，不按 '=' 过滤
   username = WindowsIdentity.GetCurrent().Name;              // DOMAIN\user 形式
   if (path == "/task") { ServeTask(); }                      // 仅示意不额外限制method；完整路由接受域另核
   ```
6. **信息不足或实现相关时的处理**：目标API不能取得源派生值时，定位具体字段与消费者，记未映射/知识缺口，不凭一个API缺值断言永远不可恢复。没有源语义依据或生成前许可时停止受影响映射，不用近似值补成完整实现；已有目标中的确认误译按根闭环有限修复或明确未解决交付。启发式只作有条件提案，有限oracle匹配不构成采用近似的许可。
7. **资料依据（名称/版本/章节）**：Go `net.Flags`、`os.Environ`、`os/user.Current`、`http.Client`、`ServeMux`；.NET `HttpClient.Timeout`、`NetworkInterface`、`Environment.GetEnvironmentVariables`、`WindowsIdentity.Name`。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
