---
name: csharp-to-ruby
description: Use when converting C# source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → Ruby 语言转换规则

> **适用基线**：C# 12 / .NET 8 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C#](../../references/languages/csharp.md)与[目标语言 Ruby](../../references/languages/ruby.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C# → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CS-RB-01：C# 方法重载向 Ruby 单方法动态参数与模式分流映射
1. **源码触发条件**：C# 源码中定义多个同名但不同参数类型或参数个数的重载方法。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：编译期根据实参静态类型绑定精确的目标方法重载版本。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby 不支持方法同名重载！后定义的同名方法会静默覆盖前者。必须合并为单个方法，使用默认参数、可变参数（`*args`）或关键字参数（`**kwargs`），并在方法体内根据 `case/when` 动态类型分流。
   - *不适用条件*：严禁在 Ruby 类中直接编写同名方法，否则先前的方法完全丢失。
5. **错误机械替换反例**：
   ```ruby
   # 错误：Ruby 顺序定义同名方法，导致前一个方法被彻底覆盖丢失
   class Calculator
     def add(a, b); a + b; end
     def add(a, b, c); a + b + c; end # 覆盖了两个参数的版本！
   end
   # Calculator.new.add(1, 2) # 报错 ArgumentError: wrong number of arguments (given 2, expected 3)
   # 正确：合并为单一方法并提供可选参数
   class Calculator
     def add(a, b, c = nil)
       c ? a + b + c : a + b
     end
   end
   ```
6. **信息不足或实现相关时的处理**：若重载差异极大，考虑重命名为具备明确意图的独立方法。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 CS-RB-02：C# checked 整数溢出检查向 Ruby 任意精度 Integer 显式校验映射
1. **源码触发条件**：C# 源码中使用 `checked { a + b }` 显式检测整数溢出并期望抛出 `OverflowException`。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：超出定宽整数上限时，CLR 运行时即时抛出 `System.OverflowException`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby 的 `Integer` 为任意精度大数，算术永不溢出！若需模拟 C# 的 `checked` 语义，必须在算术后显式检查数值是否超出 `2**31 - 1` 或 `2**63 - 1`，超出时显式抛出 `RangeError`。
   - *不适用条件*：严禁照抄算术表达式而不加界限检查，会导致溢出保护彻底失效。
5. **错误机械替换反例**：
   ```ruby
   # 错误：Ruby 自动升级为大整数，未抛出溢出异常
   # C# 原型: checked { int x = int.MaxValue + 1; } -> 抛出 OverflowException
   x = 2147483647 + 1 # 结果静默变为 2147483648，未产生任何异常！
   # 正确：显式检查并抛出异常
   def checked_add_i32(a, b)
     res = a + b
     raise RangeError, "integer overflow" if res > 2147483647 || res < -2147483648
     res
   end
   ```
6. **信息不足或实现相关时的处理**：若源上下文为 `unchecked`，则显式施加补码截断。
7. **直接官方 HTTPS 依据链接**：[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 CS-RB-03：C# 结构化 Task 并发向 Ruby Thread/Queue 与 GVL 约束映射
1. **源码触发条件**：C# 源码中使用 `Task.Run` 在后台并行处理数据。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)）；目标语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)）。
3. **原可观察行为**：多线程在托管线程池上并行推进，可利用多核 CPU。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Ruby `Thread.new` 配合线程安全的 `Thread::Queue` 进行任务分发；注意子线程未捕获异常默认静默终止，建议设置 `Thread.abort_on_exception = true`。
   - *不适用条件*：受 MRI GVL 约束，无法加速纯 CPU 密集计算。
5. **错误机械替换反例**：
   ```ruby
   # 错误：子线程发生未捕获异常，主线程 join 之前静默失败无任何提示
   t = Thread.new { raise "Fatal" }
   # 若未显式 t.join，错误将被完全吞没！
   # 正确：设置 abort_on_exception 并在主线程管理生命周期
   t = Thread.new do
     Thread.current.abort_on_exception = true
     do_work()
   end
   t.join
   ```
6. **信息不足或实现相关时的处理**：若需多核纯并行，声明切换为 `Ractor` 或多进程并记录未验证状态。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)。

### 规则 CS-RB-04：C# null 合并与可空判定向 Ruby nil/false 真值差异映射
1. **源码触发条件**：C# 源码使用 `??` 提供缺省值（`(_targetUser ?? "无")`、`cred.TicketBlob?.Length ?? 0`）、`?.` 空条件调用、`string.IsNullOrEmpty(...)`，或把 `bool` 字段/可空 `bool` 与 `null` 放在同一条件里判断。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：`??` 只在左值为 `null` 时求值右值，`false` 与 `0`、`""` 都不会触发右值；可空布尔（`bool?`）有"未提供"与"false"两种可区分状态。Ruby 中没有 `null`，缺值用 `nil` 表示，且 **`nil` 与 `false` 同为假值，`0`、`""`、`[]` 全为真值**，`a || b` 在 `a` 为 `false` 时同样取 `b`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：缺值判定写 `x.nil?`，缺省值写 `x.nil? ? default : x`；空字符串用 `x.to_s.empty?`（同时覆盖 `nil` 与 `""`）；`?.` 链改写为 `x&.member`；可空布尔用 `true/false/nil` 三态并在报告中标注必须显式比较 `== false`。
   - *不适用条件*：严禁把 `??` 机械替换为 `||`——当右值是 `false` 或 `""` 的有效取值时，`||` 会把"业务假值"一并替换掉；严禁把 `if (path != "")` 之类的空串判定直接搬成 Ruby（`""` 在 Ruby 中为真，判定恒成立）；严禁用 `if (flag)` 语义判定可空布尔（`nil` 与 `false` 在 Ruby 中无法区分）。
5. **错误机械替换反例**：
   ```ruby
   # C# 原型：bool persist = OptBool("persist") ?? false;   // 只对 null 回退
   persist = opt_bool("persist") || false   # 错误：|| 把 false 也当成需要回退的缺值
   # C# 原型：if (path != "" && !path.StartsWith("\"")) { ... }
   if path != ""                            # 错误：Ruby 中空字符串为真，条件恒成立
     report(path)
   end
   # 正确：区分 nil 与 false，空串用 empty? 判定
   persist = opt_bool("persist")
   persist = false if persist.nil?
   report(path) unless path.to_s.empty?
   ```
6. **信息不足或实现相关时的处理**：若字段在源语言里是"可空"而目标侧的 `nil` 会被下游按 `false` 处理，或 C# `bool?` 的三态必须保留，先确认每个字段的缺值语义（未提供 / false / 0），不得统一折叠成一种假值。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 CS-RB-05：C# 查找失败返回 -1 向 Ruby nil 与显式范围检查映射
1. **源码触发条件**：C# 源码用 `IndexOf`/`LastIndexOf` 的返回值参与算术或切片（`path.Substring(0, path.ToLower().IndexOf(".exe") + 4)`、`var pos2 = ant.IndexOf('"', pos + domainPrefix.Length)`），或用 `Contains(...)`、`Substring`、`Split` 结果长度做分支。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)）；目标语言 CRuby 3.4（[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)）。
3. **原可观察行为**：C# 的 `IndexOf` 未命中返回 `-1`（不是异常），`Substring(0, -1 + 4)` 这类表达式会静默取到错误区间，`Substring` 起点越界抛 `ArgumentOutOfRangeException`。Ruby 的 `String#index` 未命中返回 `nil`，`nil + 4` 直接抛 `NoMethodError`，`String#[]` 与 `String#slice` 越界返回 `nil` 而不抛异常，`String#split` 不保留尾部空字段。
4. **目标可选写法和不适用条件**：
   - *可选映射*：未命中写 `idx = s.index('.exe'); next if idx.nil?`，命中后显式换算长度（`s[0, idx + 4]`）；包含判定用 `s.include?(sub)`；切分用 `s.split(sep)` 并确认尾部空字段语义；空白与缺值用 `s.to_s.strip.empty?`。
   - *不适用条件*：严禁把 `-1` 参与运算的表达式直译成 Ruby（`nil` 会以 `NoMethodError` 在另一处失败，失败位置与源语言不同）；严禁依赖 Ruby 切片越界返回 `nil` 来复现 C# 的越界异常语义；严禁把 `Contains` 的大小写不敏感重载（`StringComparison.OrdinalIgnoreCase`）直译为 `include?`（Ruby 默认区分大小写，需 `downcase` 或正则）。
5. **错误机械替换反例**：
   ```ruby
   # C# 原型：path.Substring(0, path.ToLower().IndexOf(".exe") + 4)
   exe_path = path[0, path.downcase.index('.exe') + 4]   # 错误：未命中时 index 为 nil -> NoMethodError
   # 正确：先取下标并显式判空，再切片
   idx = path.downcase.index('.exe')
   next if idx.nil?
   exe_path = path[0, idx + 4]
   # C# 原型：path.ToLower().Contains(" ")  // 若源为 OrdinalIgnoreCase 比较
   spaced = path.downcase.include?(' ')   # 正确：显式 downcase 才能等价
   ```
6. **信息不足或实现相关时的处理**：若源码依赖 `IndexOf` 的 `-1` 参与后续算术而未做判空（即源语言本身已依赖"错误区间"），必须先把该分支的真实期望行为问清、写为待确认，不得自行补一个 `nil` 判定改变失败路径。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)。

### 规则 CS-RB-06：C# 按类型分派的 catch 层次向 Ruby rescue 类层次与 ensure 映射
1. **源码触发条件**：C# 源码用多个按类型排列的 `catch`（`catch (DirectoryNotFoundException)`、`catch (FileNotFoundException)`、`catch (UnauthorizedAccessException)`、末尾 `catch (Exception e)`）分派不同处理，或在 `catch` 中 `throw` 重新抛出、用 `finally` 保证清理。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）；目标语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）。
3. **原可观察行为**：C# 按异常对象类型自上而下匹配第一个兼容的 `catch`，`finally` 在所有出口执行；`throw;` 重抛保留原始堆栈与异常对象。Ruby 的 `begin/rescue` 顺序匹配且 **不带类名的 `rescue` 只捕获 `StandardError` 及其子类**，`SystemExit`、`Interrupt`、`SignalException`、`NoMemoryError` 不会被捕获；`ensure` 对应 `finally`；裸 `raise`（无参数）在 `rescue` 体内重抛原异常。
4. **目标可选写法和不适用条件**：
   - *可选映射*：每个 C# `catch` 对应一个 `rescue` 子句并显式列出异常类（`rescue Errno::ENOENT, Errno::EACCES => e`），顺序保持"具体在前、宽泛在后"；`finally` 改 `ensure`；重抛用裸 `raise`；需要异常对象时用 `=> e` 绑定，`raise e` 只在确需替换时使用。
   - *不适用条件*：严禁把 `catch (Exception)` 直译成裸 `rescue` 后自认为覆盖了全部异常（`SystemExit`/`Interrupt` 会穿透，进程退出与信号语义被改变）；严禁把宽泛 `rescue` 放在具体 `rescue` 之前（后续子句永远不会命中）；严禁用内联 `expr rescue nil` 修饰符替代带清理与重抛的完整 `begin/rescue/ensure`（它不能 `retry`，也不保证 `ensure`）。
5. **错误机械替换反例**：
   ```ruby
   # C# 原型：try { ... } catch (Exception e) { Console.WriteLine(e.Message); }
   begin
     copy_cert(exe, output)
   rescue      # 错误：裸 rescue 只覆盖 StandardError；且把失败静默降级为继续执行
     puts 'failed'
   end
   # 正确：显式类层次 + ensure 清理，需要时重抛
   begin
     copy_cert(exe, output)
   rescue Errno::ENOENT => e
     warn "input missing: #{e.message}"
     raise                # 正确：保留原异常与堆栈
   rescue StandardError => e
     warn "copy failed: #{e.class}: #{e.message}"
   ensure
     cleanup_temp(output)
   end
   ```
6. **信息不足或实现相关时的处理**：若源码的 `catch` 顺序构成有意义的失败拓扑（某类异常被静默吞掉、某类被转成返回值），必须逐类确认目标侧的对应类与处理动作，无法映射的类写为待确认，不得合并成一个 `rescue StandardError`。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
