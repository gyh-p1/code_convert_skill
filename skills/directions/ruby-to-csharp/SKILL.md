---
name: ruby-to-csharp
description: Use when converting Ruby source to C#; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → C# 语言转换规则

> **适用基线**：CRuby 3.4 → C# 12 / .NET 8。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/ruby-to-csharp/README.md)；候选、冻结任务与第三方回传须分层记录。
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
