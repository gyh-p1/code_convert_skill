# PowerShell 语言共性语义（PowerShell 7.6）

> **用途**：供以 PowerShell 为源语言或目标语言的方向 Skill 按需读取；本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 变量持有 .NET 对象引用；标量基本类型按值语义求值；管道传递对象流时通过 `PSObject` 包装层反射解包。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` 管道对象解包与属性投影开销受 PowerShell 引擎管道缓冲区机制支配。
- **机械等价禁区与转换约束**：管道单元素展开（Unrolling）会将单元素数组隐式退化为标量，破坏类型契约；**不得把 PowerShell 的 `$null`/空数组/空串判定与其他语言互相当作等价**（见下条）。
- **官方资料依据**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)

### L1-PS-01 `$null`、空集合与单元素展开是三种不同判定
1. **源码触发条件**：源码用 `if ($x)` / `if ($null -ne $x)` / `if ($x.Count -eq 0)` / `if ([string]::IsNullOrEmpty($x))` 分流，或把 `@()`/管道结果直接当真值使用。
2. **冻结版本/运行时/API 前提**：PowerShell 7.6；`$null` 比较与集合计数语义见 [MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)、[about_Arrays](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)。
3. **原可观察行为**：
   - 布尔上下文中的假值集合包含 `$null`、`$false`、数值 `0`、空串 `""`、空数组 `@()`；单元素集合取该元素的布尔值，所以 `@($null)`、`@(0)` 为假；多元素集合为真，即使各元素均是假值。
   - **单元素展开**：`$x = 1` 与 `$x = @(1)` 在多数上下文中不可区分，`.Count` 在标量上也可用；管道中单元素数组会退化为标量。
   - `$null -eq $collection` 与 `$collection.Count -eq 0` 判断的是不同事实：空数组不等于 `$null`。
4. **目标可选写法和不适用条件**：
   - *PowerShell 作为源*：把“无值”“空集合”“标量单值”分别映射到目标的对应检查；`@()` 合同必须显式写出，不能靠目标的空值判定承接。
   - *PowerShell 作为目标*：源的空指针/零值/长度判断必须分别重建为 `$null -eq`、数值比较、`.Count -eq 0`；**不得**用 `if ($x)` 简化，那会把 `0`/`""`/`@()` 一并并入假分支。
   - *不适用条件*：源确实按“有内容才继续”统一判定且目标同为动态语言时，真值判断可能是等价映射；仍须核对 `0` 与 `""` 是否可能作为合法值出现。
5. **错误机械替换反例**：
   ```powershell
   # 错误：把 C 的指针判空写成 PowerShell 真值判断，空串/0 被误并入守卫分支
   if (-not $cmdline) { return -1 }        # C 源是 !ptr；此处 "" 与 0 也进分支
   # 错误之二：把空数组当作 $null
   if ($null -eq $items) { 'empty' }       # @() 不是 $null，这里不会命中
   # 正确：按源的判定对象分别表达
   if ($null -eq $cmdline) { return -1 }
   if (@($items).Count -eq 0) { 'empty' }  # 显式表达空集合
   ```
6. **信息不足或实现相关时的处理**：无法确定源的判断表达“无值”“空集合”还是“单元素标量”时，标为“空值与集合语义待确认”，不得用统一真值判断合并；**必须**用 `@()` 显式包裹以保证数组合同。
7. **直接官方 HTTPS 依据链接**：[about_Booleans（集合转换）](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_booleans?view=powershell-7.6)；[about_Arrays](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)；[about_Comparison_Operators](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators)。

### L1-PS-05 参数绑定与实参来源必须显式重建

1. **源码触发条件**：函数/脚本用 `param()` 声明参数（`[Parameter(Position=n)]`、默认值、`[switch]`、`ValueFromRemainingArguments`），或读取 `$args`/`$PSBoundParameters`。
2. **冻结版本/运行时/API 前提**：PowerShell 7.6（[about_Functions_Advanced_Parameters](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters)、[about_Automatic_Variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)）。
3. **原可观察行为**：
   - **参数有三种来源**：**未绑定**、**显式传入**、**默认值生效**。默认值**仅在参数被省略时**生效；`$PSBoundParameters` 只含**真正传入**的参数。
   - **位置参数**按 `Position` 绑定；未标 `Position` 的参数只能按名传入。
   - `$args` 只在**没有** `param()` 块（或 `param()` 未声明该参数）时承接剩余位置实参；一旦参数被 `param()` 声明，多余实参的行为依 `ValueFromRemainingArguments` 而变。
   - 名称**缩写**：PowerShell 允许**唯一前缀**缩写参数名（`-Dep` 可匹配 `-Depth`），有歧义时报错。
   - **`[switch]` 的显式假值**：`-Flag:$false` 与**省略** `-Flag` 在 `$PSBoundParameters` 中不同（前者已绑定）。
4. **目标可选写法和不适用条件**：
   - *PowerShell 作为源*：源区分"省略"与"显式默认值"时，目标必须保留该区分（C/C++ 用 `argc`，Go 用 `len(os.Args)`，Python 用 `None` 哨兵或 `argparse` 的 `default=None`）。
   - *PowerShell 作为目标*：需要区分时必须用 `$PSBoundParameters.ContainsKey('X')`，**不得**用"值是否等于默认值"代替。
   - *不适用条件*：源不区分这两种情形（只关心有效值）时，直接使用默认值是等价映射，不必引入 `ContainsKey`。
5. **错误机械替换反例**：
   ```powershell
   # 错误：用“值等于默认值”代替“参数是否被绑定”
   param([Parameter(Position=0)][int]$Depth = 2)
   $usedDefault = ($Depth -eq 2)        # 用户显式传入 -Depth 2 时被误判为未给出
   # 正确
   $usedDefault = -not $PSBoundParameters.ContainsKey('Depth')
   ```
   ```csharp
   // 反方向：把 PowerShell 的参数绑定当成 C# 的固定位置数组
   string path = args[0];      // 源里 -Depth 未给出时，args 内容与源的位置绑定不一致
   ```
6. **信息不足或实现相关时的处理**：无法确定源是否区分"省略/显式默认值"、或源是否依赖参数名缩写时，标为“参数绑定语义待确认”，并保守引入 `ContainsKey`（不影响源未区分时的结果）。
7. **直接官方 HTTPS 依据链接**：[about_Functions_Advanced_Parameters](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters)；[about_Automatic_Variables（`$PSBoundParameters`、`$args`）](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)；[about_Parameter_Binding（缩写与歧义）](https://learn.microsoft.com/en-us/powershell/scripting/learn/experts/parameter-binding)。

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` 底层为 .NET 整数体系；支持整型字面量后缀（`100L`, `1000D` 等）。
- **有符号溢出行为**：`[指定运行时的实现相关事实]` 默认算术超出当前类型上限时，PowerShell 引擎会**自动提升为更大宽度整型**（如 `[int32]::MaxValue + 1` 自动转为 `[int64]` 或 `[double]`）。
- **无符号溢出行为**：`[指定运行时的实现相关事实]` 显式通过 .NET 静态方法或强类型声明时遵循 .NET `unchecked` 回绕规则。
- **隐式提升与转换陷阱**：`[指定运行时的实现相关事实]` 动态弱类型转换系统在算术中自动升级类型，可能破坏对底层二进制溢出截断的依赖。
- **官方资料依据**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)

### L1-PS-02 数值文本输出必须钉住类型与格式字符串
1. **源码触发条件**：源码把数值转成文本——字符串内插 `"$x"`、`-f` 格式运算符、`.ToString()`、`[string]::Format`，或对定宽整数做宽度依赖的运算。
2. **冻结版本/运行时/API 前提**：PowerShell 7.6；自动类型提升与格式运算符见 [about_Operators](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)、[about_Arithmetic_Operators](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators)、[MS-CS-FORMAT](https://learn.microsoft.com/en-us/dotnet/standard/base-types/formatting-types)。
3. **原可观察行为**：
   - 算术超出当前类型上限时，引擎**自动提升为更大宽度整型**（如 `[int32]::MaxValue + 1` 转为 `[int64]` 或 `[double]`），**不按模回绕**——与 C/Go 语义相反。
   - 字符串内插与 `-f` 使用**当前区域设置**；`.ToString()` 亦受 `CurrentCulture` 影响，小数点符号可能改变。
   - `"$x"` 对 `$null` 产生空串（不是 `"$null"`），对数组产生空格分隔的元素串；对 `[double]` 使用较短表示。
4. **目标可选写法和不适用条件**：
   - *PowerShell 作为源*：目标语言的数值输出必须显式钉住类型宽度与格式提供程序；源依赖自动提升的地方须显式转为定宽运算。
   - *PowerShell 作为目标*：源若依赖定宽回绕（C/Go/Rust），必须用 `[int32]`/`[uint32]` 等固定类型与显式掩码，**不得**依赖引擎的自动提升；源若依赖固定区域，必须用 `InvariantCulture` 或显式格式。
   - *不适用条件*：源本身只做任意精度算术（Python/Ruby）时，不涉及定宽；但格式化位数与区域仍需核对。
5. **错误机械替换反例**：
   ```powershell
   # 错误：把 C 的 uint32 回绕搬运成 PowerShell 算术
   $h = [uint32]::MaxValue
   $h = $h + 1                       # PowerShell 提升为更大类型，得到 4294967296 而非 0
   # 错误之二：用内插冒充源的固定格式与区域
   "$value"                          # 受 CurrentCulture 影响，且对 $null 得空串
   # 正确：显式定宽与固定格式
   $h = [uint32](($h + 1) -band 0xFFFFFFFF)
   [string]::Format([cultureinfo]::InvariantCulture, '{0}', $value)
   ```
6. **信息不足或实现相关时的处理**：无法确定源的类型宽度或有效位数时，标为“数值类型与格式待确认”，并把该文本列入 oracle 观察点。
7. **直接官方 HTTPS 依据链接**：[about_Arithmetic_Operators](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators)；[about_Operators（-f 格式运算符）](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)；[MS-CS-FORMAT](https://learn.microsoft.com/en-us/dotnet/standard/base-types/formatting-types)。

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` 基于 .NET `System.String`（不可变 UTF-16 字符串）。
- **字节序列数据结构**：`[语言规范保证]` `[byte[]]` 数组。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` 内容中允许包含 `\0`；重定向到外部原生程序可能受宿主控制台编码截断。
- **编码假设与转换陷阱**：`[指定运行时的实现相关事实]` PowerShell 7+ 默认将文件重定向与外部管道输出编码设为 UTF-8（无 BOM）。
- **官方资料依据**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)

### L1-PS-03 重定向与外部管道的编码和换行不得静默改写字节
1. **源码触发条件**：源码做文件重定向（`>`/`>>`/`Out-File`/`Set-Content`/`Add-Content`）、调用外部原生程序并读写其管道（`|`、`$out = & prog`），或用 `[byte[]]`/`Get-Content -Encoding Byte` 处理二进制。
2. **冻结版本/运行时/API 前提**：PowerShell 7.6；`$OutputEncoding`、`[Console]::OutputEncoding`、`$PSDefaultParameterValues['Out-File:Encoding']` 与 `Set-Content` 的编码语义见 [about_Character_Encoding](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)。
3. **原可观察行为**：
   - **PowerShell 7.4 起**，原生命令 stdout 直接 `>` 到文件、原生字节流直连另一原生命令 stdin 可保留字节，不加文本格式化；在 7.6 基线内不能把它们当成 `Out-File`。
   - Cmdlet/脚本的对象流经 `>`/`Out-File` 仍涉及格式化；`Set-Content`/`Out-File` 在 7+ 默认 UTF-8 无 BOM，覆盖参数须另冻结。
   - `$out = & prog`、`Get-Content` 默认文本行读取与直接原生字节重定向不是同一通道；文本路径可能剥离行尾或重组换行。
   - NUL 是否保留须按具体通道核对，不能以“控制台编码”一概断言截断。
4. **目标可选写法和不适用条件**：
   - *PowerShell 作为源*：字节路径必须映射到目标的字节类型与二进制模式；文本路径须显式冻结编码与 BOM 策略。
   - *PowerShell 作为目标*：源若以字节为单位，选择 `[byte[]]`/二进制 API 或已冻结版本的原生直连字节通道；不得经对象格式化 `Out-File`。文本路径显式冻结编码。
   - *不适用条件*：源本身只是面向控制台的文本输出且换行/编码策略属可观察行为时，须**冻结并保留**该策略，而不是消除它。
5. **错误机械替换反例**：
   ```powershell
   # 错误：将原生输出先解码为对象/文本，再用 Out-File 承载二进制
   $captured = & $tool
   $captured | Out-File out.bin
   # PowerShell 7.6 的直接原生字节重定向不是上述错误路径
   & $tool > out.bin
   # 错误之二：假定默认编码与源一致（5.1 与 7+ 不同）
   Get-Content in.bin | Set-Content out.bin     # 按文本行处理，二进制已损坏
   # 正确：字节进字节出
   [IO.File]::WriteAllBytes($out, $bytes)
   Get-Content -AsByteStream -Raw $in          # 仅在源确为字节路径时
   ```
6. **信息不足或实现相关时的处理**：无法确认源的编码、BOM 策略或换行义务时，标为“编码与换行翻译位置待确认”；**禁止**用替换字符掩盖差异。也不得用文本 cmdlet 的默认行为充当依据。
7. **直接官方 HTTPS 依据链接**：[about_Redirection（7.4 原生字节流）](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection?view=powershell-7.6)；[about_Character_Encoding](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)；[`Out-File`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/out-file)。

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` 数组底层为固定大小 `object[]`；`[指定运行时的实现相关事实]` `+=` 追加元素会导致分配新数组并全量复制元素；存在单元素自动展开为标量机制。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `[hashtable]` 与 `[ordered]@{}` 映射结构。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` 默认 `hashtable` 遍历无序；显式声明 `[ordered]@{}` 保证插入顺序。
- **迭代期间修改（Fail-Fast）**：`[指定运行时的实现相关事实]` 遍历中修改集合会抛出集合已修改异常。
- **官方资料依据**：[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)<br>[MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables)

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` 严格区分**终止错误**（Terminating Error，中断控制流）与**非终止错误**（Non-terminating Error，写入错误流继续运行）。
- **异常展开与性能模型**：`[指定运行时的实现相关事实]` `try`/`catch` **默认只能捕获终止错误**；受 `$ErrorActionPreference` 偏好变量严格控制。
- **进程退出码回传机制**：`[指定运行时的实现相关事实]` `$LASTEXITCODE` 记录外部进程最后返回码；Cmdlet 自身成败由 `$?`（`$true`/`$false`）记录；`exit` 终止宿主。
- **跨语言映射关键风险**：不可将 PS Cmdlet 写入的错误流直接等同于进程标准错误输出；`$?` 会被后续任意语句覆盖。
- **官方资料依据**：[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)<br>[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)

### L1-PS-04 非终止错误不得被压成终止，终止错误不得被静默吞掉
1. **源码触发条件**：源码产生或处理**非终止错误**（cmdlet 失败后继续、`Write-Error`、`-ErrorAction Continue/SilentlyContinue`），**或**依赖终止错误中断控制流（`throw`、`-ErrorAction Stop`、`exit` 非零）。
2. **冻结版本/运行时/API 前提**：PowerShell 7.6；`$ErrorActionPreference`/`-ErrorAction` 与 `try/catch` **默认只捕终止错误**见 [about_Preference_Variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)、[about_Try_Catch_Finally](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)。
3. **原可观察行为**：
   - **非终止错误**写入错误流后**继续执行**，不改变控制流；进程最终退出码可能仍为 0。
   - **终止错误**中断当前语句/脚本，可被 `try/catch` 捕获。
   - `$?` 反映**上一条语句**成败，会被后续任意语句覆盖；`$LASTEXITCODE` 只反映**外部进程**返回码，不反映 cmdlet 成败。
   - `-ErrorAction SilentlyContinue` **压制错误流的可观察输出**但不改变失败事实；`$ErrorActionPreference = 'Stop'` 会把非终止错误**提升**为终止错误——这是行为改变，不是等价映射。
4. **目标可选写法和不适用条件**（两个方向都必须覆盖）：
   - *PowerShell 作为源*：非终止错误的“继续执行 + 错误流输出”必须在目标保留；源主动 `throw`/`exit` 的失败必须传播为非零退出状态，不得被吞。
   - *PowerShell 作为目标*：源语言的失败若在 PowerShell 中是**非终止**形式，目标脚本会继续执行——必须显式用 `-ErrorAction Stop` 或显式检查 `$?`/`$LASTEXITCODE` 才能保留源的失败语义。反过来，源忽略失败时**不得**用 `$ErrorActionPreference='Stop'` 制造终止。
   - *不适用条件*：源确实把错误写入诊断渠道后继续时，目标的“继续 + 输出到 stderr”是正确映射，不应改成终止。
5. **错误机械替换反例**：
   ```powershell
   # 错误一：把源的非终止错误升级成终止错误，改变了控制流
   $ErrorActionPreference = 'Stop'      # 源是“记录并继续”，这里整脚本中断
   Get-ChildItem $path
   # 错误二：用 $LASTEXITCODE 判定 cmdlet 成败（它只对外部进程有效）
   Copy-Item a b
   if ($LASTEXITCODE -ne 0) { throw }   # cmdlet 失败时 $LASTEXITCODE 未被设置
   # 正确：按源的失败语义显式重建
   try { Copy-Item a b -ErrorAction Stop } catch { Write-Error $_ }   # 需要终止语义时
   ```
6. **信息不足或实现相关时的处理**：无法确认源的失败是终止还是非终止、或无法确认源是否检查 `$?` 时，把该错误路径单列为待验证 oracle；不得用“更严格更安全”为由改变控制流。
7. **直接官方 HTTPS 依据链接**：[about_Preference_Variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)；[about_Try_Catch_Finally](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)；[about_Automatic_Variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[指定运行时的实现相关事实]` 底层依赖 .NET CLR GC；处理大量管道对象时在进程内存中产生托管堆压力。
- **资源确定性释放机制**：`[指定运行时的实现相关事实]` 显式调用 `.Dispose()`，COM 对象必须调用 `[System.Runtime.InteropServices.Marshal]::ReleaseComObject()`。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 随宿主 .NET 运行时触发 GC。
- **悬垂与泄漏防范**：未释放的 COM 互操作对象将导致宿主子进程句柄泄露、阻碍外部进程终止。
- **官方资料依据**：[MS-PS-COM](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/new-object)

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` `Start-Job`（后台进程）；`Start-ThreadJob` / `ForEach-Object -Parallel`（多 Runspace 线程池）。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` Runspace 池映射至 .NET 线程池线程；脚本块隔离执行。
- **级联取消与超时机制**：`[指定运行时的实现相关事实]` 支持作业超时与取消命令；受宿主环境与具体命令控制。
- **内存模型与数据竞争**：`[指定运行时的实现相关事实]` 共享变量访问需使用同步包装或显式 .NET 同步锁，否则竞态数据损毁。
- **官方资料依据**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)<br>[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)

## 使用边界

将本页与所选的源→目标方向 Skill 及另一语言的共性页组合使用；映射前先确认源码真实行为。文件、网络、并发和跨 OS API 的具体差异仍按[共性索引的场景/系统分流](../seven-language-common-semantics.md)选读，不从语言事实直接推断系统 API 等价。没有逐例第三方证据时，语法/构建与功能结论保持 `UNVERIFIED`；本机不运行或编译样本。
