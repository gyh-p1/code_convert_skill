---
name: c-to-csharp
description: Use when converting C source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C → C# 语言转换规则

> **适用基线**：ISO C11 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C](../../references/languages/c.md)与[目标语言 C#](../../references/languages/csharp.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 C → C# 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 C-CS-01：C 结构体裸指针与定宽整数向 C# struct/class 划分与 checked 上下文映射
1. **源码触发条件**：C 源码中定义包含数值或数组的结构体并按值传递，或存在定宽无符号整数回绕算术计算。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（WG14-N1570 §6.2.5, §6.2.6.2）；目标语言 C# 12 / .NET 8（MS-CS-SPEC, MS-CS-CHECKED）。
3. **原可观察行为**：C 结构体按成员值复制，内嵌数组随值复制，指针字段仍指同一对象；填充字节不作全量一致保证。无符号按具体提升/转换及位宽保留回绕，有符号溢出属 UB，不能泛化为补码保证。
4. **目标可选写法和不适用条件**：
   - *可选映射*：struct 可承接值字段，但托管数组字段复制的是引用，不能代 C 内嵌数组独立副本；按源布局/消费者选择内联存储或对应成员复制。struct 不保证无 GC 分配（装箱等可分配），class 也不因需要多态就免源复制。按源定宽算术选择 unchecked；源无 checked 失败时不为加固新增 checked。
   - *不适用条件*：严禁将所有 C 结构体机械映射为 C# `class`，否则后续传参变为引用别名，原独立副本被修改导致非预期副作用。
5. **错误机械替换反例**：
   ```csharp
   // 错误：机械映射为 class 导致传参产生别名共享修改
   public class Point { public int X; public int Y; }
   void Offset(Point p) { p.X += 10; } // 修改了外部传入的原始对象！
   // 正确：使用 struct 保持值传递独立性
   public struct Point { public int X; public int Y; }
   ```
6. **信息不足或实现相关时的处理**：布局、内嵌数组/指针、共享或复制消费者未知时记录并停受影响映射，不默认 struct 或深复制；按已冻结 ABI 处理互操作布局，托管表示相似不证明字节等价。
7. **资料依据（名称/版本/章节）**：MS-CS-SPEC；MS-CS-CHECKED。

### 规则 C-CS-02：C 错误指示码与 errno 向 C# 结构化异常与 using/IDisposable 映射
1. **源码触发条件**：C 源码中使用负数或非零返回码指示操作失败，或依赖显式资源关闭函数（如 `free`, `close`）。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 C# 12 / .NET 8（MS-CS-EXCEPT, MS-CS-DISPOSE）。
3. **原可观察行为**：调用方通过 `if (ret < 0)` 检查并手动跳转清理；操作系统错误通过 `errno` 暴露。
4. **目标可选写法和不适用条件**：
   - *可选映射*：底层严重失败转换为抛出派生自 `System.Exception` 的结构化异常（如 `InvalidOperationException`）；封装非托管资源的对象必须实现 `IDisposable` 并配合 `using` 语句释放。
   - *不适用条件*：不得删掉源实际存在的返回码检查，也不为源忽略的失败新增抛错/检查；仅接口与传播边界可对应时考虑异常。源显式释放不能只靠 Finalizer 期待即时执行；using/Dispose 的释放时点与失败副作用仍须对应源。
5. **错误机械替换反例**：
   ```csharp
   // 错误：非内存资源未实现 IDisposable，导致句柄泄漏直到不可预期的 GC Finalizer
   public class NativeBuffer {
       private IntPtr _buf;
       ~NativeBuffer() { FreeNative(_buf); } // 错误：执行时机完全不确定！
   }
   // 正确：实现 IDisposable 并在 using 中确定性释放
   public sealed class NativeBuffer : IDisposable {
       private IntPtr _buf;
       public void Dispose() { FreeNative(_buf); GC.SuppressFinalize(this); }
   }
   ```
6. **信息不足或实现相关时的处理**：若出现文件/套接字操作，说明语言层资源释放契约后加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md) 或 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)。
7. **资料依据（名称/版本/章节）**：MS-CS-EXCEPT；MS-CS-DISPOSE。

### 规则 C-CS-03：C 标志位/信号量同步向 C# Task/async-await 与 CancellationToken 映射
1. **源码触发条件**：C 源码中使用 volatile 标志位循环轮询或条件变量等待操作终止。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（WG14-N1570 §7.17）；目标语言 C# 12 / .NET 8（MS-CS-ASYNC, MS-CS-CANCEL）。
3. **原可观察行为**：C 线程阻塞在等待循环或信号量上，通过原子修改标志位通知退出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重构为异步方法返回 `Task`，接收 `CancellationToken` 参数，调用 `token.ThrowIfCancellationRequested()` 或使用异步等待 `Task.Delay(..., token)`。
   - *不适用条件*：严禁在 C# 中使用无休止的 `while (!flag)` 忙等待占用线程池线程；严禁在异步上下文中调用 `.Result` 或 `.Wait()`，可能引发死锁。
5. **错误机械替换反例**：
   ```csharp
   // 错误：在异步上下文中阻塞等待导致死锁或线程耗尽
   public void Process() {
       var task = DoWorkAsync();
       task.Wait(); // 错误：在特定同步上下文中极易引发死锁
   }
   // 正确：使用 await 并传递取消令牌
   public async Task ProcessAsync(CancellationToken token) {
       await DoWorkAsync(token);
   }
   ```
6. **信息不足或实现相关时的处理**：若源代码涉及操作系统原生线程创建，加载 [`skills/systems/posix-windows-threads/SKILL.md`](../../systems/posix-windows-threads/SKILL.md)。
7. **资料依据（名称/版本/章节）**：MS-CS-ASYNC；MS-CS-CANCEL。

### 规则 C-CS-04：C 定长字节缓冲与出参长度向 C# byte[]/Span<byte> 与 BinaryReader 边界映射
1. **源码触发条件**：C 源码用 `char buffer[BUFFER_SIZE]`、`unsigned char payload[] = {0x..}` 承载原始字节，长度由出参（`DWORD bytesRead`、`int recv_len`）或独立字段（`NameLength / 2`、`ValueOffset`）传递，或对含 `0x00` 的数组调用 `strlen`（如 `strlen(exploit_req)`、`strlen(complete_passwd_line)`）。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（WG14-N1570 §6.2.5, §7.23）；目标语言 C# 12 / .NET 8（MS-CS-STRING, MS-DOTNET-API）。
3. **原可观察行为**：缓冲区每个元素恒为 1 字节，字节数等于元素个数；当首字节或中间字节为 `0x00` 时，任何按 `\0` 结尾解读的函数都在该处停止，实际发送/比较/复制的字节数因此静默变短。
4. **目标可选写法和不适用条件**：
   - *可选映射*：byte[]/Span 表示缓冲区；实际消费长度按源逐调用决定：显式长度/出参保实际数，strlen 保首 NUL 前缀，sizeof 数组与指针分别核。Length 仅对应源全缓冲区元素数，不能用它修源 strlen 截断。目标 Read/BinaryReader 还须保持短读/EOF/错误与循环行为。
   - *不适用条件*：char/string 不代任意字节；源用显式长度时不新增 NUL 截断，源确用 strlen 时则保持该截断而不换 Length。不得将 sizeof(ptr) 换成集合 Length；源无合法终止符的越界风险单列，不凭缓冲区容量反推成功。
5. **错误机械替换反例**：
   ```csharp
   // 错误：把 C 的 char buffer[N] 直译为 C# char[]，缓冲区不再是 N 字节
   char[] buffer = new char[4096];                  // 4096 个 UTF-16 代码单元，非 4096 字节
   int bytesRead = textReader.Read(buffer, 0, buffer.Length); // 错误：选到了字符语义的 Read
   // 正确：原始字节一律用 byte[]，长度取实际读取返回值（取代 DWORD 出参）
   byte[] buf = new byte[4096];
   int n = stream.Read(buf, 0, buf.Length);
   Send(buf, n);
   ```
6. **信息不足或实现相关时的处理**：若同一 `char*`/缓冲在不同调用点分别承载文本与二进制，必须逐调用点确认语义与编码，不得默认 UTF-8；涉及文件/套接字读写时加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md) 或 [`skills/scenes/network-io/SKILL.md`](../../scenes/network-io/SKILL.md)，并保持字节计数语义。
7. **资料依据（名称/版本/章节）**：WG14-N1570 §6.2.5, §7.23；MS-CS-STRING；MS-DOTNET-API。

### 规则 C-CS-05：C 自相对偏移指针解析与位域/柔性数组成员向 C# Span 切片与显式位掩码映射
1. **源码触发条件**：C 源码用 `(PCHAR)pApiSetMap + pApiEntry->NameOffset` 形式的自相对偏移在字节块内定位子结构，用 `Array[ANYSIZE_ARRAY]` 柔性数组成员表示变长数组，用 `WORD offset:12; WORD type:4;` 位域压缩字段，或用 `DEREF_32(addr)`/`*(DWORD *)p` 之类宏按固定宽度取值。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（WG14-N1570 §6.7.2.1, §6.5.6）；目标语言 C# 12 / .NET 8（MS-CS-ARRAY, MS-DOTNET-API）。
3. **原可观察行为**：记录内偏移指向同一字节块内的另一个位置，越界读取在块内仍会返回"可读但错误"的数据而不报错；位域的存储分配顺序与是否跨存储单元由实现定义；`ANYSIZE_ARRAY` 的实际长度由头部 `Count` 字段决定。
4. **目标可选写法和不适用条件**：
   - *可选映射*：用 `ReadOnlySpan<byte>` 的 `Slice(offset)` / `Slice(offset, length)` 表达记录内偏移，用 `BinaryPrimitives.ReadUInt16LittleEndian(span)` 之类显式端序读取，用位移掩码还原位域（`raw & 0x0FFF`、`raw >> 12`）；变长数组用 `span.Slice(headerSize, count * elementSize)` 显式长度表达；仅在目标 ABI 已冻结且确有互操作需求时才使用 `[StructLayout]` + `Marshal`。
   - *不适用条件*：严禁用托管结构体覆盖强转（`MemoryMarshal.Read`/`MemoryMarshal.Cast`/`Unsafe.As`）机械替代偏移与位域解析——CLR 不保证与源 ABI 相同的位域布局与对齐，`ANYSIZE_ARRAY` 也无法直接映射，结果会是错位字段；严禁把 12/4 位字段当作单个 16 位整数使用。
5. **错误机械替换反例**：
   ```csharp
   // 错误：用托管结构体覆盖强转替代位域拆分与自相对偏移
   [StructLayout(LayoutKind.Sequential)]
   struct Reloc { public ushort OffsetAndType; }        // 错误：丢失 12 位偏移 / 4 位类型的拆分
   Reloc r = MemoryMarshal.Read<Reloc>(span);
   int offset = r.OffsetAndType;                        // 错误：整个 16 位被当成偏移（含类型位）
   // 正确：显式读取 2 字节并分位
   ushort raw = BinaryPrimitives.ReadUInt16LittleEndian(span.Slice(i, 2));
   int offset2 = raw & 0x0FFF;
   int type = raw >> 12;
   ```
6. **信息不足或实现相关时的处理**：源文件未给出目标 ABI、字节序、位域分配方向或结构体对齐时，必须停标为待确认，不得用 C# 默认布局反推；若偏移来自未验证的映射内存（如 PEB/API-SET），必须同时说明该数据来源属于平台事实而非 C 语言保证。
7. **资料依据（名称/版本/章节）**：WG14-N1570 §6.7.2.1, §6.5.6；MS-CS-ARRAY；MS-DOTNET-API。

### 规则 C-CS-06：C 函数指针（取址后强转调用）向 C# UnmanagedFunctionPointer 委托与存活期映射
1. **源码触发条件**：C 源码声明函数指针变量（如 `BOOL(*MiniDumpWriteDump)(HANDLE, DWORD, HANDLE, DWORD, VOID*, VOID*, VOID*);`、`typedef HMODULE (WINAPI * LOADLIBRARYA)(LPCSTR);`），经 `GetProcAddress` 或 `(LOADLIBRARYA)(uiBaseAddress + DEREF_32(...))` 取址后直接调用，并在调用前做 `== NULL` 检查。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（WG14-N1570 §6.3.2.3, §6.5.2.2）；目标语言 C# 12 / .NET 8（MS-CS-DELEGATES, MS-DOTNET-API）。
3. **原可观察行为**：函数地址的调用约定由源码中的 `WINAPI`/`NTAPI` 等宏决定；地址为空时跳过调用；调用发生在当前进程地址空间内，参数按其原生宽度传递。
4. **目标可选写法和不适用条件**：
   - *可选映射*：已知 ABI 的原生地址可用 GetDelegateForFunctionPointer<TDelegate> 包装并直接调用，核签名/调用约定与模块存活。反向把托管 delegate 交给原生方保存/异步回调时，才需让该托管对象保活至最后回调；一次同步调用结束不因局部引用消失自动错误。
   - *不适用条件*：不得混淆“调用原生函数地址”与“原生保存托管回调”；签名/架构或模块存活未知停映射。字段级保活不是所有函数指针的强制方案，也不允许删源实际地址输出/算术消费者。
5. **错误机械替换反例**：
   ```csharp
   // 此处是包装原生地址后同步调用，不是注册异步托管回调；ABI 必须先核
   delegate bool DumpFn(IntPtr h, uint pid, IntPtr f, uint t, IntPtr a, IntPtr b, IntPtr c);
   var dump = Marshal.GetDelegateForFunctionPointer<DumpFn>(addr);
   return dump(hProc, pid, hFile, 2, nint.Zero, nint.Zero, nint.Zero);
   // 委托类型的调用约定候选；仅模块/签名/Winapi ABI 已匹配时使用
   [UnmanagedFunctionPointer(CallingConvention.Winapi)]
   delegate bool DumpFnNative(IntPtr h, uint pid, IntPtr f, uint t, IntPtr a, IntPtr b, IntPtr c);
   // 保活字段仅在原生方保存托管回调时考虑，不对上述一次同步调用强加。
   ```
6. **信息不足或实现相关时的处理**：源码未展开 `WINAPI`/`NTAPI` 宏、未给出目标架构或参数宽度时，必须停标并要求冻结 ABI；缺少 ABI 事实时不得声称该委托可直接调用，也不得把"语法改写完成"当作可调用性结论。
7. **资料依据（名称/版本/章节）**：WG14-N1570 §6.3.2.3, §6.5.2.2；MS-CS-DELEGATES；MS-DOTNET-API。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
