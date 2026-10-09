---
name: ruby-to-csharp
description: Use when converting Ruby source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → C# 语言转换规则

> **适用基线**：CRuby 3.4 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Ruby](../../references/languages/ruby.md)与[目标语言 C#](../../references/languages/csharp.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Ruby → C# 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 RB-CS-01：Ruby Module/Mixin 多继承向 C# 接口多继承与扩展方法映射
1. **源码触发条件**：Ruby 源码中通过 `include MyModule` 将模块的方法混入类继承链中。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-MODULE](https://docs.ruby-lang.org/en/3.4/Module.html)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：模块内的方法动态插入到宿主类的祖先继承链（`ancestors`）中。
4. **目标可选写法和不适用条件**：
   - *可选映射*：将 Module 转换为 C# 的 `interface`，配合 C# 8+ 接口默认实现（Default Interface Methods）或静态扩展方法（Extension Methods）；若包含实例状态，必须在宿主类中维护字段。
   - *不适用条件*：严禁在 C# 中尝试继承多个基类。
5. **错误机械替换反例**：
   ```csharp
   // 错误：试图在 C# 中多继承类模拟 Module
   // public class User : BaseEntity, LogModule { } // 编译报错！
   // 正确：使用接口与默认方法或扩展方法
   public interface ILogModule {
       void Log(string msg) => Console.WriteLine($"LOG: {msg}");
   }
   public class User : BaseEntity, ILogModule { }
   ```
6. **信息不足或实现相关时的处理**：若模块内通过 `prepend` 劫持了父类方法，转换为显式装饰器模式。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-MODULE](https://docs.ruby-lang.org/en/3.4/Module.html)；[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)。

### 规则 RB-CS-02：Ruby 符号 (:symbol) 对象向 C# 枚举或常量字符串映射
1. **源码触发条件**：Ruby 源码中大量使用 `:active`、`:pending` 等不可变 Symbol 对象作为状态标记或散列键。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 C# 12 / .NET 8（[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)）。
3. **原可观察行为**：全局唯一的不可变标识符，整数比对速度，不被常规垃圾回收频繁重复分配。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若属于离散状态值，映射为 C# 强类型 `enum`；若属于动态字符串键，映射为 `const string` 或普通 `string`。
   - *不适用条件*：严禁为每个符号在 C# 堆上动态拼接字符串，避免无谓的内存开销。
5. **错误机械替换反例**：
   ```csharp
   // 错误：将固定的符号状态当成弱类型字符串散落各处，容易拼写错误
   if (status == "pending") { ... }
   // 正确：映射为强类型 enum
   public enum Status { Active, Pending }
   if (status == Status.Pending) { ... }
   ```
6. **信息不足或实现相关时的处理**：若 Symbol 来自外部输入动态生成，映射为 `string`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-SPEC](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 RB-CS-03：Ruby rescue StandardError 捕获向 C# catch (Exception) 映射
1. **源码触发条件**：Ruby 源码中使用 `rescue => e` 处理业务异常。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）。
3. **原可观察行为**：默认只捕获 `StandardError` 及其子类，系统级致命错误自动放行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C# 中捕获 `catch (Exception ex)`（C# 的 `System.Exception` 对应常规托管异常）。
   - *不适用条件*：注意在 C# 中不可使用空 catch 块 `catch { }` 吞没异常信息。
5. **错误机械替换反例**：
   ```csharp
   // 错误：空 catch 吞没异常，导致关键调试信息丢失
   try { Action(); } catch { }
   // 正确：显式捕获并记录
   try { Action(); } catch (Exception ex) { Logger.LogError(ex); }
   ```
6. **信息不足或实现相关时的处理**：若 Ruby 抛出特定异常，映射至对应的 .NET 异常类型。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)。

### 规则 RB-CS-04：Ruby 真值模型与 `||` 默认值向 C# 显式 null/空值判定映射
1. **源码触发条件**：Ruby 源码用对象的真值直接当布尔使用，或用 `||` 提供默认值，例如 `hostname = sysinfo.nil? ? cmd_exec('hostname') : sysinfo['Computer']`、`com_opts[:target] = datastore['OUTPUT_TARGET'] || session.sys.config.getenv('TEMP') + ...`、`mounted = y if tmp == ...`、`if @record_data and not @record_data.empty?`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 C# 12 / .NET 8（[MS-CS-BOOL](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/bool)、[MS-CS-NULL](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/null-coalescing-operator)）。
3. **原可观察行为**：**Ruby 中只有 `nil` 与 `false` 为假**：`0`、`""`、空数组、空 Hash 都是真；`a || b` 在 `a` 为真时返回 `a` 本身（不是 `true`），因此 `'' || 'x'` 得到 `''`，`0 || 5` 得到 `0`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`x.nil?` → `x is null`；`x || default`（x 可能是 null）→ `x ?? default`；`x` 用作条件且 x 是字符串/数值时，显式写出业务判据（`!string.IsNullOrEmpty(x)`、`x != 0`）并把判据来源写进报告；`if v` / `unless v` 中的 v 若本身已是 `bool`，直接保留。
   - *不适用条件*：严禁把 `a || b` 一律翻成 `a ?? b` 后当作"没变"——当 a 是字符串且源码依赖"空串为真"时，`??` 与 Ruby `||` 在 null 与空串上的分流不同，必须回到源码确认；也严禁把非 `bool` 表达式直接放进 C# 的 `if`/`&&`/`||`（C# 要求 `bool` 操作数），更严禁引入隐式 `bool` 转换来"凑合"（会静默改变分流判据）。
5. **错误机械替换反例**：
   ```csharp
   // 错误：以为 C# 的 || 与 Ruby 的 || 同义，直接照抄
   string target = datastore["OUTPUT_TARGET"] || GetEnv("TEMP"); // 编译错误：string 不能作 || 操作数
   // 错误：用 ?? 顶替后，空串与 null 的分流被合并
   string path = datastore["WRITABLE_DIR"] ?? "/tmp";            // 空串仍返回 ""，语义需回到源码确认
   // 正确：显式写出判据
   string target = string.IsNullOrEmpty(datastore["OUTPUT_TARGET"])
       ? Path.Combine(GetEnv("TEMP"), name)
       : datastore["OUTPUT_TARGET"];
   ```
6. **信息不足或实现相关时的处理**：源码中的条件表达式没有显式比较运算符（`if v`、`while v`）而 v 的类型无法从局部源码确定时，必须标注"真值判据待确认"并询问；Ruby 的 `0`、`""`、空集合为真这一事实不能靠 C# 的运行期隐式转换兜底，判据必须由转换者显式写出。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[MS-CS-BOOL](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/bool)；[MS-CS-NULL](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/null-coalescing-operator)。

### 规则 RB-CS-05：Ruby 动态能力探测（respond_to?/send/&.）向 C# 静态类型、接口与安全调用映射
1. **源码触发条件**：Ruby 源码按"对象是否响应某方法"决定流程或按名字调用方法，例如 `return unless client.respond_to?(:net)`、`session.core.use('priv') if !session.priv`、`enum_subkeys(x)&.each do |y| ... end`、`vals.nil?` 分支后按类型取不同方法。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-OBJECT](https://docs.ruby-lang.org/en/3.4/Object.html)）；目标语言 C# 12 / .NET 8（[MS-CS-IFACE](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/interface)、[MS-CS-OPERATORS](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/member-access-operators)）。
3. **原可观察行为**：`respond_to?(:m)` 在运行期回答"该对象现在是否响应 m"，据此可以走不同分支；`send(:m, ...)` 按名字分派（名字错误在运行期抛 `NoMethodError`）；`x&.m` 只在 `x` 不为 `nil` 时调用，否则整个表达式求值为 `nil` 且**不求值参数**；`method_missing` 把未知方法变成一次可拦截的调用。
4. **目标可选写法和不适用条件**：
   - *可选映射*：能力探测改写为"目标类型实现接口"这一编译期事实：抽出能力接口（如 `interface INetResolver { ... }`），用 `x is INetResolver r` 或 `x as INetResolver` 判定；`x&.m` → `x?.m`（C# 的 null 条件成员访问，同样短路不求值参数）；确需按名字调用时用显式委托字典 `Dictionary<string, Func<...>>` 或 `nameof` 常量表，让拼写在编译期受检查。
   - *不适用条件*：严禁用 `dynamic` + 运行期成员访问去模拟 `send`/`method_missing`（把编译期可查的错误推迟到运行期，并绕过类型系统）；严禁把 `respond_to?` 机械翻译成反射字符串查找（`GetType().GetMethod("net")` 之类），它保留名字拼写错误且丢失接口契约；`method_missing` 在 C# 中**没有**等价物，源码依赖它时必须标注为结构差异而非逐点映射。
5. **错误机械替换反例**：
   ```csharp
   // 错误：用反射按名字探测/调用，保留运行期拼写错误风险
   if (client.GetType().GetMethod("net") != null) { client.net.Resolve(host); } // 错误：名字拼错到运行期才炸
   dynamic dyn = client;
   var result = dyn.net.resolve(host);   // 错误：dynamic 绕过类型系统，参数错误运行期才暴露
   // 正确：能力用接口表达，安全调用用 ?.
   if (client is INetCapable netCapable) { netCapable.Resolve(host); }
   string uid = subkeys?.FirstOrDefault();
   ```
6. **信息不足或实现相关时的处理**：`respond_to?` 的目标方法若来自框架或第三方（该类型定义不在本地源码内），必须先把"该能力在 C# 侧由哪个接口/类型承载"标注为缺口并询问；`send` 的目标名字若只在运行期拼出（来自配置、网络或用户输入），必须停下来标注并询问，不得猜一个具体重载。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-OBJECT](https://docs.ruby-lang.org/en/3.4/Object.html)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[MS-CS-IFACE](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/interface)；[MS-CS-OPERATORS](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/member-access-operators)。

### 规则 RB-CS-06：Ruby 异常类层次与 rescue 分派向 .NET 异常类型与 when 过滤器映射
1. **源码触发条件**：Ruby 源码带异常的 `rescue` 子句并区分类型或按消息分派，例如 `rescue StandardError`、`rescue Zip::Error`、`rescue OpenSSL::OpenSSLError => e` 后 `print_error("Could not load SSH Key: #{e.message}")`、`rescue => e` 后 `puts "[!] Error: #{e.message}"`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)、[MS-CS-WHEN](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/when)）。
3. **原可观察行为**：裸 `rescue`/`rescue => e` 只匹配 `StandardError` 及其子类，`Exception` 的其他分支（`NoMemoryError`、`SignalException`、`SystemExit` 等）继续向上传播；多个 `rescue` 按书写顺序取第一个匹配；`ensure` 在正常与异常路径都执行；`fail_with(Failure::X, msg)` 不是普通异常抛出，而是以既定失败类别终止当前模块流程。
4. **目标可选写法和不适用条件**：
   - *可选映射*：每个带类的 `rescue` 映射为 `catch (对应异常类型 ex)`，`rescue => e` 的重载语义（只抓 StandardError 家族）用"捕获对应的自定义异常基类"表达，而**不是** `catch (Exception)`；`e.message =~ /.../` 的分派改写成异常过滤器 `catch (IOException ex) when (ex.Message.Contains(...))`；`ensure` → `finally`（或 `using`/`IDisposable`，当清理对象是本轮新建的）；`fail_with` 译成一个显式的失败结果或专门的失败异常类型，而不是通用 `Exception`。
   - *不适用条件*：严禁把裸 `rescue` 机械翻译成 `catch (Exception ex)`——那会连 `OutOfMemoryException`、`StackOverflowException` 一类的不可恢复错误也吞掉，把"继续向上传播"改成"就地降级"，失败路径拓扑被改变；也严禁在转换产物中新增空 `catch { }` 静默吞掉异常；用消息子串分派时不得用 `catch (Exception)` 加 `if` 判断代替类型捕获（丢失类型契约）。
5. **错误机械替换反例**：
   ```csharp
   // 错误：裸 rescue 被翻成 catch (Exception)，连不可恢复错误一起吞掉
   try { parsed = JsonSerializer.Deserialize<Config>(file); }
   catch (Exception) { return ""; }          // 错误：与 "rescue => e" 的 StandardError 家族不符
   // 错误：按消息字符串猜类型，且 catch 顺序导致后续子句永久不可达
   try { parsed = JsonSerializer.Deserialize<Config>(file); }
   catch (Exception ex) { if (ex.Message.Contains("Docker")) { } }   // 错误：丢失类型契约
   catch (FormatException ex) { log(ex.Message); }                   // 错误：上面已全部捕获，此处不可达
   // 正确：按类型捕获，条件用 when 过滤器
   try { parsed = JsonSerializer.Deserialize<Config>(file); }
   catch (FormatException ex) when (ex.Message.Contains("auth")) { log(ex.Message); }
   catch (StandardErrorFamily ex) { log(ex.Message); }
   ```
6. **信息不足或实现相关时的处理**：Ruby 的 `fail_with(Failure::...)` 在源框架里既有失败类别也有消息，转换前必须确认 C# 侧的失败表示方式（返回值、专门异常还是结果类型）——缺该信息时停下询问，不得默认翻译成抛 `Exception`；Ruby 异常类若来自框架或第三方（`Zip::Error`、`OpenSSL::OpenSSLError`、`Rex`/`Msf` 命名空间下的类型），必须把"对应 .NET 类型是否已知"标为缺口并询问。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)；[MS-CS-WHEN](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/when)。

### 规则 RB-CS-07：框架元数据字段的赋值目标与字面量空白必须逐字保真

1. **源码触发条件**：Ruby 源码把**框架/宿主元数据**作为字段赋值——`Info = ...`、`Description = %q{...}`、`Name = ...`，尤其该字段在**基类**中声明、而派生类又引入了**同名成员**时；或元数据文本使用 `%q{}`/heredoc 等**保留空白**的字面量。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-LITERALS](https://docs.ruby-lang.org/en/3.4/syntax/literals_rdoc.html)）；目标语言 C# 12 / .NET 8（[MS-CS-HIDING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/how-to-know-when-to-use-override-and-new-keyword)、[CS0108](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-messages/cs0108)）。
3. **原可观察行为**：
   - 元数据字段（如继承来的 `Info`）由框架在**实例构造时**读取；Ruby 侧没有“名称隐藏”概念，方法名与实例变量处于不同命名空间，因此同名方法**不会**遮挡字段赋值。
   - Ruby `%q{ ... }` **逐字符保留**：包含起始换行、每行的前导空格、结尾换行与 `}` 之前的缩进。
4. **目标可选写法和不适用条件**：
   - *名称隐藏*：C# 中派生类引入的**方法**会**隐藏**基类同名**非方法**成员（警告 **CS0108**），使该简单名绑定到**方法组**而非字段，导致赋值目标不是变量（赋值给方法组即编译错误）。必须改名辅助方法（如 `FinishInfo`），或显式写 `base.Info = ...`。
   - *字面量空白*：C# **原始字符串字面量**（`"""`）会**剥除公共缩进**，且不含起始换行与结尾缩进——与 `%q{}` **不等价**。需要字节级保真时必须显式构造（`"\n" + 前导空格 + ... + "\n"`）；若有意规范化，必须写注释**明确登记为有意差异**。
   - *不适用条件*：若元数据字段与辅助方法**不同名**，不涉及名称隐藏；若框架对元数据只做语义比较（不比较空白），规范化不改变可观察行为——但**是否如此必须核实，不得假定**。
5. **错误机械替换反例**：
   ```csharp
   // 错误一：派生类静态方法 Info 隐藏了继承字段 Info（CS0108）
   class MetasploitModule : Msf.Exploit.Local {
       private static ModuleInfo Info(ModuleInfo i) => i;      // 与继承字段同名
       public MetasploitModule() {
           Info = UpdateInfo(info, CreateInfo());               // 目标不是变量：绑到方法组
       }
   }
   // 错误二：用原始字符串字面量冒充 %q{} 的逐字符保留
   Description = """
       first line
       second line
       """;                                                     // 公共缩进被剥除，无起始换行/结尾缩进
   // 正确
   private static ModuleInfo FinishInfo(ModuleInfo i) => i;     // 改名，避免隐藏
   // 或：base.Info = UpdateInfo(info, CreateInfo());
   ```
6. **信息不足或实现相关时的处理**：无法确定元数据字段是**框架强制要求**还是**纯信息字段**时，仍须先保证**赋值成功且字段可读**（改名或 `base.` 二选一），再核对空白保真度；**不得**因为“该字段不影响 check/exploit”就默许空白差异而不登记。若某项确实无法恢复（框架常量被替换、辅助方法已成无用的身份函数），登记为差异而非静默删除。
7. **直接官方 HTTPS 依据链接**：[C# 名称隐藏与 `new`/`override`](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/how-to-know-when-to-use-override-and-new-keyword)、[CS0108](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-messages/cs0108)；[C# 原始字符串字面量](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/reference-types)；[Ruby 字面量（`%q`）](https://docs.ruby-lang.org/en/3.4/syntax/literals_rdoc.html)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
