---
name: ruby-to-powershell
description: Use when converting Ruby source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → PowerShell 语言转换规则

> **适用基线**：CRuby 3.4 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Ruby](../../references/languages/ruby.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/ruby-to-powershell/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Ruby → PowerShell 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 RB-PS-01：Ruby 动态方法与哈希向 PowerShell PSCustomObject 映射
1. **源码触发条件**：Ruby 源码中定义包含动态方法或属性的纯数据对象，或操作复杂 `Hash`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)）；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）。
3. **原可观察行为**：通过方法或键访问对象属性。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `[PSCustomObject]`；若需附加动态计算方法，使用 `Add-Member -MemberType ScriptMethod`。
   - *不适用条件*：严禁在 PowerShell 中使用不稳定的字符串哈希键拼接访问。
5. **错误机械替换反例**：
   ```powershell
   # 错误：在 PowerShell 中直接调用未绑定的哈希表属性方法
   $h = @{ Name = "test" }
   # $h.DoAction() 报错：MethodInvocationException
   # 正确：使用 PSCustomObject 加 ScriptMethod
   $obj = [PSCustomObject]@{ Name = "test" }
   $obj | Add-Member -MemberType ScriptMethod -Name "DoAction" -Value { Write-Output $this.Name }
   ```
6. **信息不足或实现相关时的处理**：若包含深度嵌套字典，使用自定义递归包装。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

### 规则 RB-PS-02：Ruby 异常捕获向 PowerShell 终止错误与 $? 状态映射
1. **源码触发条件**：Ruby 源码中使用 `rescue` 捕获异常并返回降级值。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 PowerShell 7.6（[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）。
3. **原可观察行为**：捕获异常并执行恢复分支。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 PowerShell 中使用 `try { ... } catch { ... }` 结构。
   - *不适用条件*：必须注意若调用外部命令产生非零退出码，它不会触发 PowerShell 的 `catch`（必须手动检查 `$LASTEXITCODE -ne 0`）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：以为 try-catch 能捕获外部命令行程序的非零退出码
   try {
       git clone invalid_url # 原生程序报错退出，返回码非零，但不触发 catch！
   } catch {
       Write-Output "Clone failed" # 永远进不来！
   }
   # 正确：显式检查 $LASTEXITCODE
   git clone invalid_url
   if ($LASTEXITCODE -ne 0) {
       Write-Error "Clone failed with exit code $LASTEXITCODE"
   }
   ```
6. **信息不足或实现相关时的处理**：区分内部 Cmdlet 异常与外部进程退出码。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)。

### 规则 RB-PS-03：Ruby 字符串内插与正则表达式向 PowerShell 语法适配映射
1. **源码触发条件**：Ruby 源码中使用 `"hello #{name}"` 字符串内插或 `/pattern/` 正则表达式字面量。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4；目标语言 PowerShell 7.6。
3. **原可观察行为**：双引号内插表达式；正则作为一等对象。
4. **目标可选写法和不适用条件**：
   - *可选映射*：PowerShell 双引号支持变量内插 `"hello $name"` 或子表达式 `"hello $($user.Name)"`；正则比对使用 `-match` 操作符，匹配结果存放在自动变量 `$Matches` 中。
   - *不适用条件*：严禁在 PowerShell 中直接保留 Ruby 的 `#{...}` 语法（PowerShell 会原样输出 `#{...}` 字面量）。
5. **错误机械替换反例**：
   ```powershell
   # 错误：在 PowerShell 中照抄 Ruby 的内插语法
   $name = "Alice"
   $str = "Hello #{name}" # 输出 "Hello #{name}"，内插彻底失效！
   # 正确：使用 PowerShell 内插语法
   $str = "Hello $name"
   # 或包含复杂属性时使用子表达式
   $str = "Hello $($user.Name)"
   ```
6. **信息不足或实现相关时的处理**：扫描所有正则修饰符，确保与 .NET 正则引擎选项对应。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
