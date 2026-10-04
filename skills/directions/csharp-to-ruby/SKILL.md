---
name: csharp-to-ruby
description: Use when converting C# source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → Ruby 语言转换规则

> **适用基线**：C# 12 / .NET 8 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C#](../../references/languages/csharp.md)与[目标语言 Ruby](../../references/languages/ruby.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/csharp-to-ruby/README.md)；候选、冻结任务与第三方回传须分层记录。
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
