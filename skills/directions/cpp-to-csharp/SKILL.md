---
name: cpp-to-csharp
description: Use when converting C++ source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → C# 语言转换规则

> **适用基线**：ISO C++17 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C++](../../references/languages/cpp.md)与[目标语言 C#](../../references/languages/csharp.md)，按源码选择适用规则。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C++ → C# 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-CS-01：C++ RAII 确定性析构向 C# IDisposable 与 using 作用域映射
1. **源码触发条件**：C++ 源码中依赖对象析构函数（RAII）管理内存外的系统资源（句柄、文件、锁）。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（WG21-N4659 Clause 6.7）；目标语言 C# 12 / .NET 8（MS-CS-DISPOSE）。
3. **原可观察行为**：对象离开局部作用域时逆序、确定性执行析构函数。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C# 中实现 `IDisposable` 接口，在调用点使用 `using var res = new ...` 或 `using (...)` 确保退出作用域时调用 `Dispose()`。
   - *不适用条件*：严禁将 C++ 析构函数机械翻译为 C# 析构函数（Finalizer：`~ClassName()`），因为 CLR 终结器执行时机非确定，会导致资源锁定与泄漏。
5. **错误机械替换反例**：
   ```csharp
   // 错误：将 C++ 析构函数直接翻译为 C# Finalizer
   public class MutexLock {
       private readonly object _lock;
       public MutexLock(object l) { _lock = l; Monitor.Enter(_lock); }
       ~MutexLock() { Monitor.Exit(_lock); } // 致命错误：GC 跨线程触发导致死锁或异常！
   }
   // 正确：使用 IDisposable 保证同步释放
   public sealed class MutexLock : IDisposable {
       private readonly object _lock;
       public MutexLock(object l) { _lock = l; Monitor.Enter(_lock); }
       public void Dispose() { Monitor.Exit(_lock); }
   }
   ```
6. **信息不足或实现相关时的处理**：若源类仅为纯内存数据结构，交由 GC 托管，无需强制实现 `IDisposable`。
7. **资料依据（名称/版本/章节）**：MS-CS-DISPOSE；WG21-N4659 Clause 6.7。

### 规则 CPP-CS-02：C++ 多重继承与虚基类向 C# 单继承加接口组合映射
1. **源码触发条件**：C++ 源码中派生类同时继承两个或多个非纯抽象基类。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（WG21-N4659 Clause 13）；目标语言 C# 12 / .NET 8（MS-CS-SPEC）。
3. **原可观察行为**：C++ 对象内存布局包含多个基类子对象，支持交叉向任意基类指针类型转换。
4. **目标可选写法和不适用条件**：
   - *可选映射*：选择一个主基类继承，其余基类转换为接口（`interface`），派生类内部通过内嵌组件对象并转发接口方法（组合优于继承）。
   - *不适用条件*：C# 语法不支持类多重继承，严禁使用任何黑魔法尝试模拟多基类字段直接合并。
5. **错误机械替换反例**：
   ```csharp
   // 错误：C# 编译器直接拒绝多类继承
   // public class Derived : BaseA, BaseB { } // 编译报错：CS1721 类不能有多个基类
   // 正确：接口加组合模式
   public interface IBaseB { void ActionB(); }
   public class Derived : BaseA, IBaseB {
       private readonly BaseB _b = new();
       public void ActionB() => _b.ActionB();
   }
   ```
6. **信息不足或实现相关时的处理**：默认实现、基类状态或调用分派存在依赖时，定位源实现及消费者并核组合候选能否保持；未知部分记缺口，停止受影响映射。不以“记录抽象层次降级”允许删实现或改变分派，采用差异须有生成前许可。
7. **资料依据（名称/版本/章节）**：MS-CS-SPEC。

### 规则 CPP-CS-03：C++ std::future/std::thread 向 C# Task-based Asynchronous Pattern (TAP) 映射
1. **源码触发条件**：C++ 源码中使用 `std::async` 或 `std::future::get()` 等待异步结果。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（WG21-N4659 Clause 33.6）；目标语言 C# 12 / .NET 8（MS-CS-ASYNC）。
3. **原可观察行为**：get 等待共享状态并取值/传播存储异常；源 launch::deferred 时可能在等待线程执行，不能全称后台任务。启动、一次取值/失效、阻塞点与异常分别可观察。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按实际启动策略与调用链保留同步/延迟/异步及取值点；仅接口与调度/异常/取消边界允许时才考虑 async/await，不为风险自动新加 CancellationToken 或改同步接口。
   - *不适用条件*：同步 Task 取值在特定上下文可能死锁，须核该上下文与调度；这不是所有 ASP.NET Core/Result 都必死锁的保证，也不能据此把源同步 get 一律改 await。
5. **错误机械替换反例**：
   ```csharp
   // 错误：机械模拟 future::get() 造成死锁
   public int Calculate() {
       return ComputeAsync().Result; // 错误：在特定同步上下文引发死锁
   }
   // 条件候选：仅源接口/调度允许整条调用链异步化且行为对应时适用
   public async Task<int> CalculateAsync() {
       return await ComputeAsync();
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及底层线程优先级设置，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **资料依据（名称/版本/章节）**：MS-CS-ASYNC。

### 规则 CPP-CS-04：C++ std::string/char 的文本与字节双重角色向 C# byte[]/string + 显式 Encoding 映射
1. **源码触发条件**：C++ 源码把 `std::string` 当字节缓冲使用（`std::string data((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());` 后 `send(s, data.c_str(), static_cast<int>(data.size()), 0);`），从字节指针+长度构造 `std::string(buf, n)`，或对 `char` 逐字节异或（`for (char& c : out) c ^= key;`、`encoded.push_back(c ^ 0x2A)`）。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（WG21-N4659 Clause 24.3）；目标语言 C# 12 / .NET 8（MS-CS-STRING, MS-DOTNET-API）。
3. **原可观察行为**：`std::string` 记录独立长度、允许内部 `\0`，元素是 1 字节的 `char`，标准库不做任何编码转换；`c_str()` 只保证追加尾随 `\0`，长度仍须用 `size()`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：字节语义一律用 `byte[]`/`ReadOnlySpan<byte>`（`File.ReadAllBytes`、`Stream.Read`），文本语义才用 `string`，并在每个跨越边界处显式选择编码（`Encoding.UTF8`/`Encoding.Latin1`/`Encoding.Unicode`）；逐字节异或改为 `out[i] = (byte)(out[i] ^ key);`；长度用 `.Length` 并说明其单位是字节。
   - *不适用条件*：严禁默认用 `Encoding.UTF8.GetString(bytes)` 做"字节→string→字节"往返（任意字节序列不可逆，会被替换为 U+FFFD 且长度改变）；严禁把 `std::string` 直译为 C# `string` 后用 `.Length` 当字节数（那是 UTF-16 代码单元数，含代理对时与字节数无关）；严禁用 `char[]`/`string` 承载协议头或文件字节。
5. **错误机械替换反例**：
   ```csharp
   // 错误：把 std::string 的字节缓冲直译为 string，并做 UTF-8 往返
   string data = File.ReadAllText(path);        // 二进制内容被按文本解码
   byte[] raw = Encoding.UTF8.GetBytes(data);   // 错误：往返不可逆，字节数与内容已改变
   Send(raw, raw.Length);                       // 与 C++ data.size() 不再对应
   // 正确：字节用 byte[]，文本才用 string
   byte[] raw2 = File.ReadAllBytes(path);
   Send(raw2, raw2.Length);
   ```
6. **信息不足或实现相关时的处理**：若同一 `std::string` 在不同使用点分别承载文本与字节、或源编码未在源码中体现，必须逐使用点停下确认，不得统一按 UTF-8 处理；涉及 socket/文件字节数时加载 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md) 或 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)。
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 24.3；MS-CS-STRING；MS-DOTNET-API。

### 规则 CPP-CS-05：C++ std::map/operator[] 的有序遍历与默认插入向 C# SortedDictionary 与 TryGetValue 映射
1. **源码触发条件**：C++ 源码用 `std::map`/`std::set` 统计并按键序输出（`std::map<std::string, int> typeCount; typeCount[parts[2]]++; for (const auto& kv : typeCount) report << kv.first << "=" << kv.second << "\n";`），或用容器 `operator[]` 读取可能不存在的键（`typeCount[key]`、`probes[i]`、`names[i]`）。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（WG21-N4659 Clause 26）；目标语言 C# 12 / .NET 8（MS-CS-MEMBERACCESS, MS-DOTNET-API）。
3. **原可观察行为**：`std::map` 按比较器严格有序，遍历顺序确定且与插入顺序无关；`std::map::operator[]` 在键不存在时先插入默认构造值再返回引用（是写操作）；`std::vector::operator[]` 不做边界检查。
4. **目标可选写法和不适用条件**：
   - *可选映射*：需要源键序时用显式对应源比较器的 SortedDictionary/SortedSet；string 默认文化比较不自动等于 C++ 字节序。源 map operator[] 的读取也会默认插入，TryGetValue 必须配合对应插入才能承接；纯查找候选只用于源 find/at 等实际语义。计数写成 `dict[k] = dict.TryGetValue(k, out var c) ? c + 1 : 1;`。
   - *不适用条件*：严禁把 `std::map` 直译为 `Dictionary` 后沿用原有遍历顺序（`Dictionary` 的遍历顺序不受保证，报告行序会变化）；严禁用 C# 索引器读取可能缺失的键来顶替 `std::map::operator[]` 的"默认插入"语义（前者抛 `KeyNotFoundException`）；也不得反过来用 `TryAdd` 忽略已存在的键（会丢计数，与 `typeCount[key]++` 语义不同）。
5. **错误机械替换反例**：
   ```csharp
   // 错误：有序 map 直译为 Dictionary；缺失键用索引器自增
   var typeCount = new Dictionary<string, int>();
   typeCount[parts[2]]++;                                  // 新键 → KeyNotFoundException
   foreach (var kv in typeCount) report.AppendLine($"{kv.Key}={kv.Value}"); // 顺序不受保证
   // 正确：顺序敏感用 SortedDictionary，计数用 TryGetValue
   var sorted = new SortedDictionary<string, int>(StringComparer.Ordinal); // 仅已确认源键序与序号比较一致时适用
   sorted[parts[2]] = sorted.TryGetValue(parts[2], out var c) ? c + 1 : 1;
   foreach (var kv in sorted) report.AppendLine($"{kv.Key}={kv.Value}");
   ```
6. **信息不足或实现相关时的处理**：输出是否要求按键有序、键缺失时应插入还是视为错误，属于需求事实；无法从源码确认时必须停下询问，不得用 `Dictionary` 的当前遍历顺序充当"看起来一致"的证据。
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 26；MS-CS-MEMBERACCESS；MS-DOTNET-API。

### 规则 CPP-CS-06：C++ iostream 失败位与异常层次向 C# 抛异常 API 与 catch 过滤映射
1. **源码触发条件**：C++ 源码用失败位而非异常判断 I/O 结果（`std::ifstream in(p); if (!in) { ... }`、`while (std::getline(in, line))`、`std::getline(ss, item, d)`），同时调用默认抛异常的设施（`fs::create_directories`、`fs::exists`、`std::stoi`、`.at()`），并出现 `catch (const std::exception&)`/`catch (...)` 与 `what()`。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（WG21-N4659 Clause 18）；目标语言 C# 12 / .NET 8（MS-CS-EXCEPT, MS-CS-WHEN）。
3. **原可观察行为**：iostream 默认不抛异常（失败置位并继续让调用方检查状态）；`<filesystem>` 与数值转换函数默认抛异常；`std::exception::what()` 返回错误消息；未捕获异常导致 `std::terminate()`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：把"失败位 + 检查"改写为 C# 的 `try`/`catch` 包裹会抛异常的 API（`File.OpenRead`、`Directory.CreateDirectory`、`int.Parse`），并按目标实际抛出的异常类型分流：文件/目录失败用 `IOException`/`UnauthorizedAccessException`/`DirectoryNotFoundException`，解析失败用 `FormatException`/`OverflowException`；`what()` 映射为 `ex.Message`；`catch (...)` 保留为 `catch (Exception)` 并记录为未分类失败；需要按条件分流时用 `catch (Exception ex) when (...)`。
   - *不适用条件*：不得删源失败位检查而让目标异常越过原处理边界；catch 的范围与动作对应源，源本为空捕获时不自动添加日志/传播，也不将 Exception 声称覆盖所有 C++ 可抛值。重抛须保持适用的传播与堆栈语义。
5. **错误机械替换反例**：
   ```csharp
   // 错误：C++ 的失败位检查被省略，会抛异常的 API 未被包裹
   var lines = File.ReadAllLines(path);   // 文件缺失 → 抛异常，而原逻辑是"返回空并继续"
   int count = int.Parse(lines[0]);       // 空行 → FormatException 直接终止
   // 正确：区分"可预期的缺失"与"必须上抛的失败"
   if (!File.Exists(path)) { Console.WriteLine("{\"rows\":0}"); return; }
   try { ... } catch (FormatException ex) { Console.Error.WriteLine(ex.Message); }
   ```
6. **信息不足或实现相关时的处理**：源 C++ 是否设置了流的 `exceptions()` 掩码、以及 `catch` 实际捕获的异常类型，必须从源码逐个确认；第三方库抛出的未文档化异常要保留未分类通道并标注异常语义不确定。
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 18；MS-CS-EXCEPT；MS-CS-WHEN。

### 规则 CPP-CS-07：Windows 文本模式标准输出的行尾与刷新语义
1. **源码触发条件**：C++ 用 `std::cout << text << std::endl` 输出需要按字节比对的行，目标为 Windows C# 控制台程序。
2. **冻结版本/运行时/API 前提**：ISO C++17、Windows CRT 文本模式 stdout → C# 12 / .NET 8；先核对源是否改为二进制模式，以及输出是控制台、重定向文件还是管道。
3. **原可观察行为**：`std::endl` 插入换行并刷新流；在本例 Windows 文本模式下，输出的 LF 经 CRT 转成 CRLF。行尾字节与输出时机都可能被观察。
4. **目标可选写法和不适用条件**：源确为文本模式且目标按同一 Windows 行尾输出时，用 `Console.Out.WriteLine(text)`（必要时再 `Flush()`）或显式采用已核对的 `TextWriter.NewLine`；不要把裸 `"\n"` 当作字节等价。源设为二进制模式、输出格式只按归一化文本比较、或目标 OS 不同时，须按实际要求重新选行尾与刷新策略。
5. **错误机械替换反例**：
   ```csharp
   Console.Out.Write(json + "\n");      // 错误：裸 LF 不保留本例的 CRLF
   Console.Out.WriteLine(json);          // Windows 文本行尾；若刷新可见，再 Flush()
   ```
6. **信息不足或实现相关时的处理**：无法确认 CRT 模式、目标 `TextWriter.NewLine`、编码或刷新是否属于 oracle 时，分别标记这些字节/时序差异为未验证，不凭注释或 build PASS 断言 stdout 等价。
7. **资料依据（名称/版本/章节）**：Microsoft CRT `_setmode`；.NET `TextWriter.NewLine`。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
