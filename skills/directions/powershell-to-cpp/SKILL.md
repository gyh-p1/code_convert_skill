---
name: powershell-to-cpp
description: Use when converting PowerShell source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → C++ 语言转换规则

> **适用基线**：PowerShell 7.6 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 PowerShell](../../references/languages/powershell.md)与[目标语言 C++](../../references/languages/cpp.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 PowerShell → C++ 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PS-CPP-01：PowerShell 脚本块 (ScriptBlock) 向 C++17 lambda 闭包映射
1. **源码触发条件**：PowerShell 源码中使用 `{ param($x) $x * 2 }` 定义脚本块并作为参数传递。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6；目标语言 ISO C++17（[WG21-N4659 Clause 8.1.5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：脚本块延迟调用，可访问并修改调用栈上下文变量。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 C++17 lambda 表达式，通用存储使用 `std::function<R(Args...)>`；若涉及局部引用捕获 `[&]`，必须保证 lambda 生命周期不超过被捕获变量的作用域。
   - *不适用条件*：严禁将持有引用捕获 `[&]` 的 lambda 跨线程传递或脱离作用域返回（会导致悬挂引用解引用 UB）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：引用捕获局部变量后逃逸，引发悬垂引用未定义行为
   std::function<int()> MakeAdder(int x) {
       return [&x]() { return x + 1; }; // 严重错误：x 是局部形参，函数退出后引用失效！
   }
   // 正确：使用值捕获 [=] 或显式转移
   std::function<int()> MakeAdder(int x) {
       return [x]() { return x + 1; };
   }
   ```
6. **信息不足或实现相关时的处理**：若脚本块动态修改了外层作用域变量，在转换报告中标明生命周期约束。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 8.1.5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PS-CPP-02：PowerShell 终止错误向 C++17 结构化异常体系映射
1. **源码触发条件**：PowerShell 源码中使用 `throw "Error message"` 或捕捉到终止错误。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）；目标语言 ISO C++17（[WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：终止当前执行管道，向上回溯调用栈。
4. **目标可选写法和不适用条件**：
   - *可选映射*：抛出继承自 `std::exception` 的 C++ 异常（如 `std::runtime_error("...")`），上层使用 `try ... catch` 捕获。
   - *不适用条件*：严禁抛出非 `std::exception` 派生的裸字符串或整数字面量（如 `throw "err";`），违背 C++ 现代异常安全规范。
5. **错误机械替换反例**：
   ```cpp
   // 错误：抛出裸字符串字面量，难以进行统一的多态异常捕获
   throw "operation failed"; // 无法被 catch (const std::exception&) 捕获！
   // 正确：抛出标准异常派生类
   throw std::runtime_error("operation failed");
   ```
6. **信息不足或实现相关时的处理**：若需要还原 PowerShell 的原生报错格式，封装包含错误信息的派生异常类。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)；[WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PS-CPP-03：PowerShell ForEach-Object -Parallel 向 C++17 线程池与同步映射
1. **源码触发条件**：PowerShell 源码中使用 `$items | ForEach-Object -Parallel { ... }` 并发处理。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）；目标语言 ISO C++17。
3. **原可观察行为**：利用 Runspace 线程池在多个线程并发执行脚本块。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `std::async(std::launch::async, ...)` 配合 `std::future`，或使用固定工作线程池；共享资源使用 `std::mutex` 保护。
   - *不适用条件*：严禁在无同步原语下并发写入 C++ 容器（如 `std::vector::push_back`），直接引发内存重配数据竞争崩溃。
5. **错误机械替换反例**：
   ```cpp
   // 错误：多线程无锁并发 push_back
   std::vector<int> out;
   // 多个线程同时 out.push_back(val); // 致命崩溃：内部缓冲区重分配数据竞争！
   // 正确：加锁保护
   std::mutex mtx;
   {
       std::lock_guard<std::mutex> lock(mtx);
       out.push_back(val);
   }
   ```
6. **信息不足或实现相关时的处理**：若代码涉及操作系统线程亲和性，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)；[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PS-CPP-04：PowerShell 属性包与同名字段多态取值向 C++ 标准容器与显式和类型映射
1. **源码触发条件**：源码用哈希表或属性包装配结果并逐字段取出，例如 `$UserProps = @{}; $UserProps.Add('Name', "$($_.properties.name)")`、`[pscustomobject]$UserProps`、`New-Object PSObject -Property $Props`（`powercat` 的 `$FuncVars["..."]` 亦同）；并且同一逻辑字段在不同分支被赋予不同类型——`$FuncVars["BufferSize"]` 存整数、`$FuncVars["Encoding"]` 存编码器对象、`$FuncVars["Socket"]` 存套接字、`$FuncVars["SessionId"]` 存字节数组；`Get-SPN` 中 `$UserProps['Created']` 存 `[dateTime]`、`$UserProps['DN']` 存字符串、`'SPN Count'` 存字符串化计数。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables)）；目标语言 ISO C++17（[WG21-N4659 Clause 26, Clause 23.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：属性包按键动态装配与读取，属性缺失返回 `$null`，键名大小写不敏感（`@{}`），取出的值保留其 .NET 运行时类型，`"$($_.properties.name)"` 这种投影把缺失属性变成空字符串而不是 `$null`；同一个键在生命周期内可以被换成另一种类型，读取点无需前置声明。
4. **目标可选写法和不适用条件**：
   - *可选映射*：字段名与类型都固定的属性包映射为 `struct`，数字字段给出定宽类型（`std::int32_t`）；确实同键多态时用 `std::variant<Ts...>` 表达并显式 `std::get`/`std::holds_alternative`；字符串统一 `std::string`，字节序列统一 `std::vector<std::uint8_t>`（与 `std::string` 严格区分）；可选字段用 `std::optional<T>` 表达“可能缺失”。
   - *不适用条件*：严禁用 `std::map<std::string, std::string>` 承载整个属性包来机械模拟动态属性（把所有字段压成字符串会丢失日期、计数与字节数组的语义，并在读取点引入反复解析与异常）；也严禁用裸 `void*`/`reinterpret_cast` 在字段间重解释类型。键名大小写不敏感这一事实不会被 `std::map` 默认比较器继承，需要显式比较器或先规范化键名。
5. **错误机械替换反例**：
   ```cpp
   // 错误：整包压成 map<string,string>，日期/计数/字节数组语义全丢失
   std::map<std::string, std::string> UserProps;
   UserProps["Created"] = ToStringString(entry.whencreated); // 只剩字符串
   // 正确：结构体 + optional/variant 表达真实类型与“可缺失”
   struct UserProps {
       std::string name, sam_account, dn;
       std::optional<std::int64_t> created_filetime;
   };
   ```
6. **信息不足或实现相关时的处理**：字段集合或字段名是否随输入变化、同键是否真的存在多种类型、缺失属性在源里被投影成空串还是保留 `$null`，都必须先确认；确认不了就按“字段集合固定”与“缺失即空串”两个假设分别标注，不要默认二选一。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 26](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables)。

### 规则 PS-CPP-05：PowerShell 数值位宽、符号与自动加宽向 C++ 定宽类型与截断前置校验映射
1. **源码触发条件**：源码在数值边界上做强制转换或依赖自动加宽，例如 `[int] $objDeDomain.Properties['msds-behavior-version'].item(0)`、`[Int] ('0x{0}' -f (...))`、`[Convert]::ToInt16(($PacketElim[0..1] -join ""),16)` 后 `[byte[]]` 收窄、`[UInt32] 2` 与 `$Dll.Length` 传入 `VirtualAllocEx`/`VirtualFreeEx`、`$MiniDumpWithFullMemory` 之类的标志常量、`[DateTime]::MaxValue.Ticks` 与 1600 年加法、`$PortBytes = [System.BitConverter]::GetBytes($TcpRow.LocalPort)`；以及无符号与有符号值的混算与比较。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables), [MS-PS-CONVERT](https://learn.microsoft.com/en-us/dotnet/api/system.convert)）；目标语言 ISO C++17（[WG21-N4659 Clause 6.9.1, Clause 7.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：PowerShell 的 `[int]`/`[Int16]` 在目标类型表示范围内做确定性转换，超出范围时抛出终止错误（可被捕获），而算术溢出会由引擎自动加宽到更大整型或 `[double]`；`[Convert]::ToInt16` 之类的显式转换把超范围输入转成终止错误而不是静默取模；`[byte[]]` 收窄会把值按 8 位取模。这些行为与 C++ 的“有符号溢出是 UB、无符号按模回绕、窄化按模截断”并不一致。
4. **目标可选写法和不适用条件**：
   - *可选映射*：为每个数值字段选择与源 .NET 类型对应的定宽类型 `<cstdint>`（`std::int32_t`、`std::uint32_t`、`std::int64_t`）；窄化前用范围判定转成显式失败路径（返回错误码或抛异常），再赋值；有符号/无符号混算前先把两侧统一到同一类型并检查范围；P/Invoke 参数按目标 API 的签名选定宽度，避免 `int` 与 `std::size_t` 之间隐式转换。
   - *不适用条件*：严禁依赖 C++ 语言本身的截断行为去复刻 .NET 转换——有符号溢出在 C++ 是未定义行为（编译器可假定不发生），而不能像 PowerShell 的算术那样自动加宽；也严禁用 `static_cast` 一次性完成“转换+收窄”，因为它既不检查范围也不抛错。数字字面量后缀/宽度必须显式写清（`0x001F0FFF` 这类标志常量不要落到 `int` 之外再隐式回缩）。
5. **错误机械替换反例**：
   ```cpp
   // 错误：把 [Int] 转换当成 static_cast，超范围时静默截断
   std::uint32_t port = static_cast<std::uint32_t>(row.LocalPort); // 若 LocalPort 为负则按模回绕
   // 正确：范围判定后再收窄，越界走显式失败路径
   if (row.LocalPort < 0 || row.LocalPort > 65535) { return std::nullopt; }
   std::uint16_t port = static_cast<std::uint16_t>(row.LocalPort);
   ```
6. **信息不足或实现相关时的处理**：源值域与目标 API 参数宽度（以及 ABI 下的 `long`/指针宽度）未冻结时必须停下标注；无法判断某处是“源会用终止错误拒绝”还是“源会回绕”时，不要在 C++ 里替源挑一个行为，先记录待确认。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 7.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[MS-PS-CONVERT](https://learn.microsoft.com/en-us/dotnet/api/system.convert)。

### 规则 PS-CPP-06：PowerShell `try/catch/finally`、`-ErrorAction Stop` 与非托管句柄清理向 C++ 异常与 RAII 映射
1. **源码触发条件**：源码用 `try`/`catch`/`finally` 包裹含清理的临界区，或对非托管资源手工释放，例如 `Get-Process -Id $ProcessID -ErrorAction Stop` 被 `catch [System.Management.Automation.ActionPreferenceStopException]` 捕获、`Resolve-Path $Dll -ErrorAction Stop`、`$FileStream.Close()`、`$VirtualFreeEx.Invoke(...)`、`$CloseHandle.Invoke($hProcess)`、`[System.Runtime.InteropServices.Marshal]::FreeHGlobal($TableBuffer)` 与 `[System.Runtime.InteropServices.Marshal]::AllocHGlobal(...)`；以及 `throw 'Unable to open process handle.'` 这类显式终止错误。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-TRY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally), [MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)）；目标语言 ISO C++17（[WG21-N4659 Clause 18, Clause 15.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：`catch` 默认只能捕获终止错误；`-ErrorAction Stop` 的作用是把某个非终止错误提升为可捕获的终止错误；`finally` 在终止错误、正常结束与 `break`/`continue` 跳出时都会执行，常用于关闭流与释放句柄；未捕获的终止错误会沿管道向上传播并可能终结脚本；此外 PS 依赖 GC/终结器兜底，源码里可能存在“路径上忘了释放”的资源。C++ 的栈展开会逆序调用已构造局部对象析构，正好对应 `finally` 的“总会执行”，但只对 RAII 包装的资源成立。
4. **目标可选写法和不适用条件**：
   - *可选映射*：把每个非托管资源包装为 RAII 类型（`std::unique_ptr<T, Deleter>`、自定义句柄类），由析构完成释放；错误通过抛继承 `std::exception` 的类型传播，调用点用 `try ... catch (const std::exception&)`；需要“总会执行”的收尾动作写成局部对象的析构、或显式 `try { ... } catch (...) { cleanup(); throw; }`；把 `ActionPreferenceStopException` 对应到能表达“前置条件检查失败”的异常类型。
   - *不适用条件*：严禁把 `finally` 里的清理机械搬到 `catch` 块——`catch` 在无错误路径上不会执行，会造成资源泄漏；同样严禁只依赖“函数退出时自然释放”而不真做 RAII 包装，源里手工 `Close`/`FreeHGlobal` 的点位在 C++ 中必须有确定的对应物。C++ 异常不得跨越 C ABI 边界，边界处须 `catch(...)` 转错误码。
5. **错误机械替换反例**：
   ```cpp
   // 错误：源里 finally 的释放被搬进 catch，正常路径泄漏句柄
   HANDLE h = OpenProcess(access, FALSE, pid);
   try { work(h); }
   catch (const std::exception&) { CloseHandle(h); throw; } // 无异常时 h 永不关闭
   // 正确：RAII 包装，正常与异常路径都释放
   struct HandleGuard {
       HANDLE h;
       ~HandleGuard() { if (h) CloseHandle(h); }
   } guard{OpenProcess(access, FALSE, pid)};
   if (!guard.h) throw std::runtime_error("open process failed");
   ```
6. **信息不足或实现相关时的处理**：源中哪些错误在当前偏好设置下可被 `catch` 捕获、`finally` 里是否有依赖执行顺序的副作用、以及资源由谁拥有，都必须先确认；跨 DLL/ABI 边界的异常约定未冻结时停下标注，不要默认异常可以穿过边界。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[MS-PS-TRY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
