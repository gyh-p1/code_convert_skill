---
name: powershell-to-ruby
description: Use when converting PowerShell source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → Ruby 语言转换规则

> **适用基线**：PowerShell 7.6 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 PowerShell](../../references/languages/powershell.md)与[目标语言 Ruby](../../references/languages/ruby.md)。
> **方向案例与证据**：如本地工作区存在 `docs/test/dataset/powershell-to-ruby/README.md`，按其中 case 分层查看；该本地数据目录不随 Git/Skill 分发。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 PowerShell → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PS-RB-01：PowerShell 管道流式传输向 Ruby Enumerable 链式方法调用映射
1. **源码触发条件**：PowerShell 源码中使用 `$data | Where-Object { ... } | ForEach-Object { ... }`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：对象逐个通过管道过滤与投影。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 Ruby `Enumerable` 链式调用：`data.select { |x| ... }.map { |x| ... }`；若针对大集合需惰性求值，在链首追加 `.lazy`（如 `data.lazy.select { ... }.map { ... }`）。
   - *不适用条件*：严禁直接在巨型数组上链式调用全量数组生成方法，避免多次中间数组分配。
5. **错误机械替换反例**：
   ```ruby
   # 错误：对超大流未使用 lazy，导致连续创建多重巨型中间数组引发内存溢出
   # huge_data.select { ... }.map { ... }
   # 正确：使用 .lazy 保持管道惰性流式计算
   huge_data.lazy.select { |x| x.valid? }.map { |x| x.process }
   ```
6. **信息不足或实现相关时的处理**：若源数据为哈希表，注意 Ruby 中迭代得到的是 `[key, value]` 数组。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

### 规则 PS-RB-02：PowerShell 非终止错误策略向 Ruby 显式 rescue 代码块映射
1. **源码触发条件**：PowerShell 源码中使用 `$ErrorActionPreference = 'SilentlyContinue'` 忽略命令错误。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)）；目标语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）。
3. **原可观察行为**：命令遇到非终止错误时不中断脚本，静默跳过继续执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Ruby 中对易出错的方法显式包裹 `begin ... rescue StandardError ... end`，或在单行使用 `action rescue nil`（仅限明确无副作用的只读探测）。
   - *不适用条件*：严禁在关键文件写或网络通信中滥用全局 `rescue nil`，会掩盖权限或路径等严重错误。
5. **错误机械替换反例**：
   ```ruby
   # 错误：滥用 rescue nil 掩盖核心业务异常
   File.write(target_path, content) rescue nil # 若目录不存在或无权限，静默失败且无日志！
   # 正确：针对性捕获并处理
   begin
     File.write(target_path, content)
   rescue SystemCallError => e
     warn "Write failed: #{e.message}"
   end
   ```
6. **信息不足或实现相关时的处理**：在报告中列出所有被降级为静默忽略的错误点。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)。

### 规则 PS-RB-03：PowerShell 字符转义反引号向 Ruby 双引号标准转义映射
1. **源码触发条件**：PowerShell 源码中使用反引号进行转义（如 `` `n `` 代表换行，`` `t `` 代表制表符，`` `$ `` 代表转义美元符）。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：PowerShell 特有的反引号作为转义前缀。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Ruby 双引号标准转义字符（`\n`, `\t`）；变量内插转换为 `#{var}`。
   - *不适用条件*：严禁在 Ruby 字符串中保留反引号转义字符，Ruby 双引号中反引号没有转义语义，会导致字面残留 `\``。
5. **错误机械替换反例**：
   ```ruby
   # 错误：将 PS 的反引号转义原样保留
   text = "`nHello" # 在 Ruby 中输出的是 "`nHello" 字面量，而不是换行！
   # 正确：转换为标准反斜杠转义
   text = "\nHello"
   ```
6. **信息不足或实现相关时的处理**：扫描源码所有反引号转义并做正规化替换。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 PS-RB-04：PowerShell `[ordered]@{}` 与属性包枚举向 Ruby `Hash` 与键值块映射
1. **源码触发条件**：源码用有序哈希表或属性包装配数据并按条目遍历，例如 `$standard_commands = [ordered]@{ 'Basic System Information' = 'Start-Process "systeminfo" ...' ; ... }`、`$AccessPermissions = @{ KEY_QUERY_VALUE = 1; ... }`、`$Props = @{ Key = $Key; Time = [DateTime]::Now; Window = $Title.ToString() }`、`ForEach ($command in $commands.GetEnumerator()) { ... $command.Name ... $command.Value }`、`$properties = [pscustomobject]$UserProps`、以及 `$_.properties['ServicePrincipalName']` 这类属性取值。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables)）；目标语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html), [RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：默认 `@{}` 的遍历顺序不作保证，只有 `[ordered]@{}` 才保证插入顺序；键名比较大小写不敏感；`GetEnumerator()` 产出的是带 `Name`/`Value` 两个属性的字典条目对象，而直接对 `@{}` 做管道遍历得到的是条目对象而非 `[key, value]` 数组；属性缺失返回 `$null`，内插进字符串得到空串。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby `Hash` 自 1.9 起按插入顺序遍历，可直接承载 `[ordered]@{}` 的顺序义务；遍历用 `hash.each { |key, value| ... }` 或 `hash.each_pair`；需要“条目对象”的语义时用 `hash.each_entry` 或显式取 `[key, value]`；属性集合固定时优先定义类/`Struct`/`Data` 而不用 Hash 承载字段。
   - *不适用条件*：严禁把 `@{}` 当作“无序即可乱序”的依据而改用 `Set` 之类丢失值语义的容器；严禁用 `hash.keys.zip(hash.values)` 重建条目（多一次分配且不必要）；注意 Ruby 的 `Hash#each` 与 PS 的 `GetEnumerator()` 都给出有序键值，但源若用的是无序 `@{}`，Ruby 的稳定顺序会比源更确定——不得把“顺序更确定”当成等价性证据，需在报告中标注该差异。
5. **错误机械替换反例**：
   ```ruby
   # 错误：把 @{} 的条目对象语义原样搬成数组下标，且丢掉了键名大小写不敏感
   commands.each do |item|
     puts item.Name          # NoMethodError: Array/Hash 没有 Name
   end
   # 正确：按 Ruby 的键值块语义遍历
   commands.each do |name, command|
     puts name
     run_command(command)
   end
   ```
6. **信息不足或实现相关时的处理**：源使用的是 `@{}` 还是 `[ordered]@{}`、键名大小写是否被依赖、以及条目对象上是否还用到 `Name`/`Value` 之外的成员，都必须先确认；确认不了就停下标注，不要默认 Hash 或默认有序。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)；[MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables)。

### 规则 PS-RB-05：PowerShell `$null` 判定与数组展开向 Ruby `nil` 判定与 `compact` 映射
1. **源码触发条件**：源码把 `$null` 与集合混用，例如 `$grepStream = $null; $xmlStream = $null; $readableStream = $null` 之后按需赋值、`if ($Socket -eq $null){break}`、`if (($i -ne $null) -and (($r -ne "") -or ($e -ne "")))`、`$null = $hostList.Add($iHostPart1)` 这种“吞掉返回值”的写法、`$null` 被内插进字符串（`$_.Replace("    All User Profile     : ",$null)`）、以及 `$CurrentIPString = $null` 之后被加入数组。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators), [MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/), [RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)）。
3. **原可观察行为**：`$null` 与空数组在布尔化时都为假，但把 `$null` 加入数组会得到含 `nil` 元素的数组，而“没有输出”（例如 `Where-Object` 无命中）不会产生元素；`$null -eq $null` 为真、`$null -eq 0` 为假；`$null` 参与字符串内插时变成空串；被赋 `$null` 的变量在后续属性访问上会静默得到 `$null`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`$null` 判定映射为 `x.nil?`；容器里的“缺失元素”用 `nil` 表示并显式判定，需要过滤时用 `array.compact`；可选值用 `nil` 加显式分支，不要用 `false`/`0` 顶替；字符串内插中源的 `$null -> ""` 语义用 `x.to_s` 或显式 `x || ""` 表达。
   - *不适用条件*：严禁把 `if ($x -eq $null)` 机械写成 `unless x`——Ruby 中 `false` 与 `nil` 是仅有的假值，但 `unless`/`if !x` 会把 `false` 一并当作“为 nil”，与源 `-eq $null` 可区分；严禁把 `$null` 机械映射为 `0`/`""`（源里三者可区分）；严禁依赖“给数组加 `$null`”与 Ruby `push(nil)` 之外的等价性而不检查元素计数。
5. **错误机械替换反例**：
   ```ruby
   # 错误：-eq $null 被写成 unless，false 被一起吞掉；nil 元素未过滤
   unless socket
     break                       # socket 为 false 时也跳出，源不会
   end
   hosts.each { |h| connect(h) }  # hosts 含 nil 元素时对 nil 调用方法
   # 正确：显式 nil 判定 + 过滤 nil 元素
   break if socket.nil?
   hosts.compact.each { |h| connect(h) }
   ```
6. **信息不足或实现相关时的处理**：某变量是否可能取 `false`（而不仅是 `nil`）、集合中是否允许出现 `nil` 元素、以及源里 `$null` 的出现位置是“赋值占位”还是“真实取值”，都必须先确认；确认不了就停下标注，不要用 `unless` 或 `|| ''` 合并语义。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)。

### 规则 PS-RB-06：PowerShell 条件式 `switch` 与 `-match` 大小写语义向 Ruby `case/if` 与正则敏感度映射
1. **源码触发条件**：源码用条件脚本块或正则驱动分支，例如 `switch ($Path) { { ([regex]::Match($PSItem, "...").Groups | Where-Object -Property "Name" -eq "fileName" | Select-Object -ExpandProperty "Success") -eq $false } { ... } Default { ... } }`、`if ($extended.ToLower() -eq 'extended')`、`if ($Type -eq "group") -or ($Type -eq "user")`、`if ($iHost -match $IPRangeRegex)`、`Where {($_.Access|select -ExpandProperty IdentityReference) -match "Everyone"}`、`'Checking registry ...' = 'Test-Path -Path "..."'` 这类被后续 `Invoke-Expression` 执行的字符串分支。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-SWITCH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_switch), [MS-PS-COMPARE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators)）；目标语言 CRuby 3.4（[RB-DOC-CASE](https://docs.ruby-lang.org/en/3.4/syntax/control_expressions_rdoc.html), [RB-DOC-REGEXP](https://docs.ruby-lang.org/en/3.4/Regexp.html)）。
3. **原可观察行为**：PS `switch` 支持条件脚本块分支（按顺序求值，命中即执行并继续匹配其余分支，除非 `break`），`Default` 为兜底；`-eq`/`-match` 在 PS 中默认大小写不敏感，`-ceq`/`-cmatch` 才敏感；字符串化后交给 `Invoke-Expression` 的“命令表”在源里只是字符串，没有正则语义。
4. **目标可选写法和不适用条件**：
   - *可选映射*：条件式分支映射为 `if/elsif/else`（Ruby 的 `case/when` 也支持 `when ->(x) { ... }` 形式的条件，但 PS 的“命中后继续匹配其余分支”语义需要显式拆成顺序 `if` 并配合提前返回）；大小写不敏感匹配用 `/pattern/i =~ s` 或 `s.match?(/pattern/i)`（对应 `-match`），敏感匹配用不带 `i` 的正则（对应 `-cmatch`）；字面量命令表用普通字符串数组/哈希，不要引入正则。
   - *不适用条件*：严禁把 PS 的条件式 `switch` 机械写成 Ruby 的 `case expr; when cond`（Ruby 的 `when` 是值匹配或 `===`，不是对 `$_` 求值脚本块）；严禁把默认不敏感的 `-match` 写成不带 `i` 的正则（漏命中）；也严禁把源的纯字符串命令表当正则处理。
5. **错误机械替换反例**：
   ```ruby
   # 错误：把条件式 switch 当值匹配，且丢掉 -match 的默认不敏感
   case path
   when ->(p) { p =~ %r{^.+[/\\]$} }   # PS 条件脚本块被误当"值"
     path += "/"
   end
   if identity =~ /Everyone/            # 源 -match 不敏感，这里却大小写敏感
     warn "world-writable"
   end
   # 正确：改成顺序 if，并显式补 IgnoreCase
   if path.match?(%r{^.+[/\\]$})
     path += "/"
   end
   if identity.match?(/Everyone/i)
     warn "world-writable"
   end
   ```
6. **信息不足或实现相关时的处理**：源用的是 `-match` 还是 `-cmatch`、`switch` 分支命中后是否有 `break`/是否依赖继续匹配、以及分支条件是值还是表达式，都必须先确认；确认不了就停下标注，不要默认按值匹配或默认大小写敏感。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-REGEXP](https://docs.ruby-lang.org/en/3.4/Regexp.html)；[MS-PS-COMPARE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
