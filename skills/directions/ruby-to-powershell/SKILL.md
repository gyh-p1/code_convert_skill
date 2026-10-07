---
name: ruby-to-powershell
description: Use when converting Ruby source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → PowerShell 语言转换规则

> **适用基线**：CRuby 3.4 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Ruby](../../references/languages/ruby.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
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

### 规则 RB-PS-04：Ruby 真值模型（仅 nil/false 为假）向 PowerShell $null 与布尔转换判定映射
1. **源码触发条件**：Ruby 源码用对象的真值直接控制流程或取后备值，例如 `enum_subkeys(x)&.each do |y| ... end`、`return nil unless key_str`、`subkeys.empty? ? nil : subkeys`、`k = 'Manufacturer' ... value: hash['Mfg'] || 'Unknown'`、`unless session.commands.include?(...)`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 PowerShell 7.6（[MS-PS-TYPES](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_booleans)、[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)）。
3. **原可观察行为**：**Ruby 只有 `nil` 与 `false` 为假**：空字符串 `''`、`0`、空数组、空 Hash 全是真，因此 `if s` 对空串仍进入分支；`a || b` 返回第一个为真的**值本身**，因此 `'' || 'Unknown'` 得到 `''`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`x.nil?` → `$null -eq $x`（把 `$null` 放左侧，避免与数组比较时的元素过滤语义）；`x || default` 在 x 只可能是 `$null` 时 → `if ($null -eq $x) { $default } else { $x }`；需要在管道里做空值兜底时才用 `??`（PowerShell 7 的空合并运算符），并确认左操作数确实只有 `$null`；`x&.m` → `if ($null -ne $x) { $x.m }`。
   - *不适用条件*：严禁把 Ruby 的真值判断机械翻译成 PowerShell 的布尔上下文（`if ($s)`）——PowerShell 另有 `''`、`0`、空集合等假值，同一表达式在两侧的分流不同；也不得把 Ruby 的 `||` 翻成 `??` 后当作等价：Ruby `||` 处理的是"假值"，`??` 处理的是"`$null`"，空串与 `$null` 在两侧的分流并不重合。
5. **错误机械替换反例**：
   ```powershell
   # 错误：照抄 Ruby 的真值判断，PowerShell 把空字符串当假
   $value = $hash['Mfg']
   if ($value) { $label = $value } else { $label = 'Unknown' }  # 错误：空串会走 else，Ruby 不会
   # 错误：用 ?? 顶替 Ruby 的 ||，空串与 $null 的分流被合并
   $label = $hash['Mfg'] ?? 'Unknown'                            # 空串仍返回空串，需回到源码确认意图
   # 正确：显式写出判据
   if ($null -eq $value -or $value -eq '') { $label = 'Unknown' } else { $label = $value }
   ```
6. **信息不足或实现相关时的处理**：条件的判据在源码中不显式（`if $v`、`unless $v`）而 v 可能是字符串/数值/集合时，必须标注"真值判据待确认"并询问；PowerShell 版本与宿主决定可用运算符（`??`、`?.` 需 7.x），任务未冻结宿主版本时不得假定可用。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[MS-PS-TYPES](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_booleans)；[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)。

### 规则 RB-PS-05：Ruby 迭代/块向 PowerShell 管道与显式集合操作映射（单元素解包与上游失败语义）
1. **源码触发条件**：Ruby 源码用块遍历或做集合变换，例如 `paths.each do |path| ... end`、`paths.count`、`files.each do |file| next if ['.', '..'].include?(file) ... end`、`resp.split("\r\r\n\r\r\n").map do |ent| next if ent.strip.empty? ... end`、`objects[:values].compact.each do |k| results << k end`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-ENUMERABLE](https://docs.ruby-lang.org/en/3.4/Enumerable.html)、[RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)）；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)、[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)）。
3. **原可观察行为**：Ruby 的 `each` 逐元素执行块，块内 `next` 跳过本次、`break` 终止整个迭代；集合 `count`/`empty?` 得到确定的元素个数；`Array#compact`/`flatten!` 会就地或复制地改变元素集合；一个元素的数组仍是数组（`size` 恒为 1）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`each` → `foreach ($item in $items) { ... }`（需要流式与 `-Parallel` 时才用 `ForEach-Object`）；`select`/`map` → `Where-Object`/`ForEach-Object`，但把结果显式落进 `@()` 以免被单元素解包；计数用 `@($items).Count`（`@()` 保证计数对象是数组）；判空用 `@($items).Count -eq 0`；`next` → `continue`，`break` → `break`。
   - *不适用条件*：严禁把 `$items.Count` 直接当作 Ruby 的 `size`——管道单元素展开（unrolling）会让单元素结果退化成标量，`.Count` 在标量上随类型而异（可能为 1、也可能报错或被当成属性读取），必须先 `@()` 归一化；管道的单元素展开还会让"返回一个元素的集合"与"返回一个标量"不可区分，需要保持集合类型契约时必须显式 `, $item` 或 `@($item)`。
5. **错误机械替换反例**：
   ```powershell
   # 错误：把 Ruby 的 paths.count / paths.empty? 直接套到管道结果上
   $paths = Get-ChildItem $dir | Where-Object { $_.PSIsContainer } | Select-Object -ExpandProperty FullName
   if ($paths.Count -eq 0) { ... }      # 错误：只有一个目录时退化为字符串，.Count 语义不确定
   foreach ($p in $paths) { ... }       # 错误：单个字符串会被当作一个整体，而不是一个元素的集合
   # 正确：用数组子表达式归一化，显式保持集合契约
   $paths = @(Get-ChildItem $dir | Where-Object { $_.PSIsContainer } | Select-Object -ExpandProperty FullName)
   if ($paths.Count -eq 0) { Write-Error 'No users found with a .ssh directory'; return }
   foreach ($p in $paths) { ... }
   ```
6. **信息不足或实现相关时的处理**：Ruby 块内是否含 `break`/`next` 且其返回值被使用，必须逐个确认后再选 `foreach` 或 `ForEach-Object`（后者在管道中无法用 `break` 跳出整条管道）；集合是否可能为空、是否可能只有一个元素必须从源码与用法确认，空/单元素两种情况都要在报告里写明按哪一侧语义处理。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-ENUMERABLE](https://docs.ruby-lang.org/en/3.4/Enumerable.html)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)；[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)。

### 规则 RB-PS-06：Ruby 字节串与编码转换向 PowerShell .NET 字符串/字节数组映射
1. **源码触发条件**：Ruby 源码在字节与文本之间转换，或按字节/十六进制处理内容，例如 `out << format("%<label>5s\t%<value>75s\n", label: v, value: u.gsub("\x00", ''))`、`ret[data.unpack('V').map { |x| "Disk #{x.to_s(16)}" }.join(' ')] = drive`、`payload.encode('ASCII')`、`resp.split("\r\r\n\r\r\n")` 后 `.lines.map(&:strip)`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)）；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)、[MS-DOTNET-ENCODING](https://learn.microsoft.com/en-us/dotnet/api/system.text.encoding)）。
3. **原可观察行为**：Ruby `String` 是字节序列 + `Encoding` 标签，`encode('ASCII')` 在不兼容时抛 `Encoding::UndefinedConversionError`，`gsub("\x00", '')` 按**字节**删除 NUL，`unpack('V')` 按小端把 4 字节读成整数；内容可含 `\0` 而不被截断。
4. **目标可选写法和不适用条件**：
   - *可选映射*：文本一律用 .NET `[string]`（UTF-16 代码单元序列）；字节一律用 `[byte[]]`，两者互转显式调用 `[System.Text.Encoding]::UTF8.GetBytes($s)` / `.GetString($bytes)`；按字节删除 NUL 用 `[byte[]]` 过滤后重建，而不是对 `[string]` 做 `-replace`；重定向到外部原生程序时显式设置 `$OutputEncoding`/`[Console]::OutputEncoding`。
   - *不适用条件*：严禁把 Ruby 的字节串直接当作 PowerShell 字符串后 `-replace "\x00"`：`[string]` 的 `-replace` 是按 UTF-16 代码单元与 .NET 正则匹配，与 Ruby 按字节删除 NUL 的语义不同；严禁用 `[string]` 承载任意二进制并在其中做 `substring` 切分（多字节/代理对边界会让切片位置与 Ruby 的字节偏移不一致）；不得对 `[string]` 假定"长度等于字节数"。
5. **错误机械替换反例**：
   ```powershell
   # 错误：把 Ruby 的字节级 gsub("\x00", '') 照抄成字符串替换
   $value = $data.ToString()
   $clean = $value -replace "\x00", ''    # 错误：按 UTF-16 与 .NET 正则处理，字节语义不同
   # 错误：对二进制用字符串下标切片，假定 1 字符 == 1 字节
   $prefix = $blob.Substring(0, 2)        # 错误：不是 Ruby 的 payload[0, 2] 字节切片
   # 正确：二进制走 [byte[]]，编码边界显式转换；若确要按字节剔除 NUL 请用 [byte[]] 过滤
   $bytes = [byte[]]$data
   $cleanBytes = [byte[]]($bytes | Where-Object { $_ -ne 0 })
   $prefix = $bytes[0..1]
   $text = [System.Text.Encoding]::UTF8.GetString($cleanBytes)
   ```
6. **信息不足或实现相关时的处理**：Ruby 串的 `encoding` 标签无法从局部源码确定（来自子进程输出、注册表数据、文件读回）时必须标注"编码待确认"并询问，不得默认 UTF-8；跨进程读写的编码还受宿主 `$OutputEncoding`、`[Console]::OutputEncoding` 与被调程序自身编码影响，需按 OS/宿主单独核验，不从语言层相似性推定一致。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)；[MS-DOTNET-ENCODING](https://learn.microsoft.com/en-us/dotnet/api/system.text.encoding)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
