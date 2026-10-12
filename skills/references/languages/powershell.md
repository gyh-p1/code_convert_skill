# PowerShell 语言共性语义（PowerShell 7.6）

> **用途**：以 PowerShell 为源语言或目标语言的任务必读本页，按源码选择适用条目；加载与门禁先见根[转换入口](../../../SKILL.md)。本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 变量持有 .NET 对象引用；标量基本类型按值语义求值；管道传递对象流时通过 `PSObject` 包装层反射解包。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` 管道对象解包与属性投影开销受 PowerShell 引擎管道缓冲区机制支配。
- **机械等价禁区与转换约束**：管道单元素展开（Unrolling）会将单元素数组隐式退化为标量，破坏类型契约；**不得把 PowerShell 的 `$null`/空数组/空串判定与其他语言互相当作等价**（见下条）。
- **官方资料依据**：MS-PS-PIPE

### L1-PS-01 `$null`、空集合与单元素展开是三种不同判定
1. **源码触发条件**：源码用 `if ($x)` / `if ($null -ne $x)` / `if ($x.Count -eq 0)` / `if ([string]::IsNullOrEmpty($x))` 分流，或把 `@()`/管道结果直接当真值使用。
2. **冻结版本/运行时/API 前提**：PowerShell 7.6；`$null` 比较与集合计数语义见 MS-PS-AUTO、about_Arrays。
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
7. **资料依据（名称/版本/章节）**：about_Booleans（集合转换）；about_Arrays；about_Comparison_Operators。

### L1-PS-05 参数绑定与实参来源必须显式重建

1. **源码触发条件**：函数/脚本用 `param()` 声明参数（`[Parameter(Position=n)]`、默认值、`[switch]`、`ValueFromRemainingArguments`），或读取 `$args`/`$PSBoundParameters`。
2. **冻结版本/运行时/API 前提**：PowerShell 7.6（about_Functions_Advanced_Parameters、about_Automatic_Variables）。
3. **原可观察行为**：
   - **参数有三种来源**：**未绑定**、**显式传入**、**默认值生效**。默认值**仅在参数被省略时**生效；`$PSBoundParameters` 只含**真正传入**的参数。
   - 函数参数默认可按声明顺序位置绑定；显式 Position、CmdletBinding 的 PositionalBinding、参数集及 switch 等影响实际绑定。不能仅凭没有 Position 就判只能按名传入；需要稳定公开位置接口时显式记录/声明位置。
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
7. **资料依据（名称/版本/章节）**：about_Functions_Advanced_Parameters；about_Automatic_Variables（`$PSBoundParameters`、`$args`）；about_Parameter_Binding（缩写与歧义）。

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` 底层为 .NET 整数体系；支持整型字面量后缀（`100L`, `1000D` 等）。
- **有符号溢出行为**：`[指定运行时的实现相关事实]` 默认算术超出当前类型上限时，PowerShell 引擎会**自动提升为更大宽度整型**（如 `[int32]::MaxValue + 1` 自动转为 `[int64]` 或 `[double]`）。
- **无符号溢出行为**：`[指定运行时的实现相关事实]` 数值转换要求目标类型能容纳结果；类型约束或强制转换不是通用模回绕。源要求截断/回绕时须有显式位宽算法或准确 API 契约，不能用“底层是 .NET”代替依据。
- **隐式提升与转换陷阱**：`[指定运行时的实现相关事实]` 动态弱类型转换系统在算术中自动升级类型，可能破坏对底层二进制溢出截断的依赖。
- **官方资料依据**：MS-PS-AUTO

### L1-PS-02 数值文本输出必须钉住类型与格式字符串
1. **源码触发条件**：源码把数值转成文本——字符串内插 `"$x"`、`-f` 格式运算符、`.ToString()`、`[string]::Format`，或对定宽整数做宽度依赖的运算。
2. **冻结版本/运行时/API 前提**：PowerShell 7.6；自动类型提升与格式运算符见 about_Operators、about_Arithmetic_Operators、MS-CS-FORMAT。
3. **原可观察行为**：
   - 普通算术超出当前类型范围可能提升为更宽类型，不自动保持源的固定宽度回绕；Go 的有符号/无符号回绕、C 的无符号回绕与 C 有符号溢出分别按其语言页理解，不能合称同一规则。
   - 可展开字符串的内插使用 invariant culture；`-f`/.NET 普通数值格式化与无提供程序的数值 ToString 另核当前区域、实际类型/重载。不能把内插与直接 ToString 当同一格式路径。
   - `"$x"` 对 `$null` 产生空串（不是 `"$null"`），对数组产生空格分隔的元素串；对 `[double]` 使用较短表示。
4. **目标可选写法和不适用条件**：
   - *PowerShell 作为源*：保持实际自动提升/数值范围与具体格式通道，不能反向强改为会截断的定宽运算；目标定宽不足时标出表示缺口。
   - *PowerShell 作为目标*：源有已定义的定宽回绕时显式保持位宽，不靠自动提升或强制转换保证截断；源要求固定文本格式时保持实际精度、进制、符号和文化规则，不因目标 API 更常见而替换。
   - *不适用条件*：源本身只做任意精度算术（Python/Ruby）时，不涉及定宽；但格式化位数与区域仍需核对。
5. **错误机械替换反例**：
   ```powershell
   # 错误：把 C 的 uint32 回绕搬运成 PowerShell 算术
   $h = [uint32]::MaxValue
   $h = $h + 1                       # PowerShell 提升为更大类型，得到 4294967296 而非 0
   # 错误之二：源要求 invariant 数值文本，却改用当前文化的直接 ToString
   $value.ToString()                  # 在逗号小数点文化下可改变文本
   # 正确：显式定宽与固定格式
    $h = [uint32](($h + 1) -band ([uint64][uint32]::MaxValue)) # 明确正值掩码，不依赖十六进制的符号解释
   [string]::Format([cultureinfo]::InvariantCulture, '{0}', $value)
   ```
6. **信息不足或实现相关时的处理**：无法确定源的类型宽度或有效位数时，标为“数值类型与格式待确认”，并把该文本列入 oracle 观察点。
7. **资料依据（名称/版本/章节）**：PowerShell 7.6 about_Arithmetic_Operators、about_Type_Conversion、about_Quoting_Rules（可展开字符串的 invariant culture）；.NET 数值 ToString/复合格式化的具体重载与提供程序。

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` 基于 .NET `System.String`（不可变 UTF-16 字符串）。
- **字节序列数据结构**：`[语言规范保证]` `[byte[]]` 数组。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` 内容中允许包含 `\0`；重定向到外部原生程序可能受宿主控制台编码截断。
- **编码假设与转换陷阱**：`[指定运行时的实现相关事实]` PowerShell 7+ 默认将文件重定向与外部管道输出编码设为 UTF-8（无 BOM）。
- **官方资料依据**：MS-PS-PIPE

### L1-PS-03 重定向与外部管道的编码和换行不得静默改写字节
1. **源码触发条件**：源码做文件重定向（`>`/`>>`/`Out-File`/`Set-Content`/`Add-Content`）、调用外部原生程序并读写其管道（`|`、`$out = & prog`），或用 `[byte[]]`/`Get-Content -Encoding Byte` 处理二进制。
2. **冻结版本/运行时/API 前提**：PowerShell 7.6；`$OutputEncoding`、`[Console]::OutputEncoding`、`$PSDefaultParameterValues['Out-File:Encoding']` 与 `Set-Content` 的编码语义见 about_Character_Encoding。
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
7. **资料依据（名称/版本/章节）**：about_Redirection（7.4 原生字节流）；about_Character_Encoding；`Out-File`。

### L1-PS-06 固定文本须区分字面值、插值与输出终止符

1. **触发/前提**：PowerShell 7.6；源/目标有固定帮助文本、路径标签、协议字段或多行字符串。冻结宿主/.NET writer、字符编码和允许差异。
2. **原行为**：双引号字符串会展开变量/子表达式并处理反引号转义；单引号字符串不插值，内部单引号需重复。here-string 也有单/双引号之别；结束标记所用的最后换行不加入其内容，内部行尾仍须核实际文本。
3. **映射条件**：只改目标语法所需的转义，保持求值后的固定内容、顺序和空白。不擅改固定标签/帮助全文，也不把源已有换行统一替换为 Environment.NewLine。`.NET Console.WriteLine` 另追加 writer 的终止符，即使参数已有换行；若源只写入内含行尾的字符串，须选择符合该行为的 Write/字节通道，具体通道见 §八。
4. **反例**：固定文本 `cost=$5` 改用可插值字符串；多行常量无意多出/少掉首尾换行；源固定 LF 文本加 WriteLine 后多出宿主行尾；将错误诊断写到 success 流以求显示相同。
5. **未知处理**：不知道源文本是否固定、writer 配置或捕获通道时逐项记待核；格式化显示/归一化比较不足以证明原始字节保持，不硬编码特定运行时异常栈。
6. **官方依据**：about_Quoting_Rules、Console.WriteLine；.NET 实际版本按宿主冻结。

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` 数组底层为固定大小 `object[]`；`[指定运行时的实现相关事实]` `+=` 追加元素会导致分配新数组并全量复制元素；存在单元素自动展开为标量机制。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `[hashtable]` 与 `[ordered]@{}` 映射结构。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` 默认 `hashtable` 遍历无序；显式声明 `[ordered]@{}` 保证插入顺序。
- **迭代期间修改（Fail-Fast）**：`[指定运行时的实现相关事实]` 遍历中修改集合会抛出集合已修改异常。
- **官方资料依据**：MS-PS-ARRAY<br>MS-PS-HASH

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` 严格区分**终止错误**（Terminating Error，中断控制流）与**非终止错误**（Non-terminating Error，写入错误流继续运行）。
- **异常展开与性能模型**：`[指定运行时的实现相关事实]` `try`/`catch` **默认只能捕获终止错误**；受 `$ErrorActionPreference` 偏好变量严格控制。
- **进程退出码回传机制**：`[指定运行时的实现相关事实]` `$LASTEXITCODE` 记录外部进程最后返回码；Cmdlet 自身成败由 `$?`（`$true`/`$false`）记录；`exit` 终止宿主。
- **跨语言映射关键风险**：不可将 PS Cmdlet 写入的错误流直接等同于进程标准错误输出；`$?` 会被后续任意语句覆盖。
- **官方资料依据**：MS-PS-PREF<br>MS-PS-AUTO

### L1-PS-04 非终止错误不得被压成终止，终止错误不得被静默吞掉
1. **源码触发条件**：源码产生或处理**非终止错误**（cmdlet 失败后继续、`Write-Error`、`-ErrorAction Continue/SilentlyContinue`），**或**依赖终止错误中断控制流（`throw`、`-ErrorAction Stop`、`exit` 非零）。
2. **冻结版本/运行时/API 前提**：PowerShell 7.6；`$ErrorActionPreference`/`-ErrorAction` 与 `try/catch` **默认只捕终止错误**见 about_Preference_Variables、about_Try_Catch_Finally。
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
   Copy-Item a b -ErrorAction Stop       # 源要求失败传播时，不再 catch 后静默继续
   ```
6. **信息不足或实现相关时的处理**：无法确认源的失败是终止还是非终止、或无法确认源是否检查 `$?` 时，把该错误路径单列为待验证 oracle；不得用“更严格更安全”为由改变控制流。
7. **资料依据（名称/版本/章节）**：about_Preference_Variables；about_Try_Catch_Finally；about_Automatic_Variables。

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[指定运行时的实现相关事实]` 底层依赖 .NET CLR GC；处理大量管道对象时在进程内存中产生托管堆压力。
- **资源确定性释放机制**：`[指定运行时的实现相关事实]` 显式调用 `.Dispose()`，COM 对象必须调用 `[System.Runtime.InteropServices.Marshal]::ReleaseComObject()`。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 随宿主 .NET 运行时触发 GC。
- **悬垂与泄漏防范**：未释放的 COM 互操作对象将导致宿主子进程句柄泄露、阻碍外部进程终止。
- **官方资料依据**：MS-PS-COM

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` `Start-Job`（后台进程）；`Start-ThreadJob` / `ForEach-Object -Parallel`（多 Runspace 线程池）。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` Runspace 池映射至 .NET 线程池线程；脚本块隔离执行。
- **级联取消与超时机制**：`[指定运行时的实现相关事实]` 支持作业超时与取消命令；受宿主环境与具体命令控制。
- **内存模型与数据竞争**：`[指定运行时的实现相关事实]` 共享变量访问需使用同步包装或显式 .NET 同步锁，否则竞态数据损毁。
- **官方资料依据**：MS-PS-PIPE<br>MS-PS-THREADJOB

## 八、宿主输出

### 宿主与输出通道

迁入原进程场景的语言事实：success、error、warning、verbose、debug、information 与 host 显示的归属/重定向条件须按源码调用和宿主区分，不能因“都能看见”合成 stdout/stderr。保留 Write-Warning/Write-Verbose/ShouldProcess 的触发条件，不新增 What if 提示文本；公开数据流不能被提示污染。普通脚本输出也适用，进程场景只管子进程捕获与等待。来源：about_Redirection、ShouldProcess。

## 九、普通控制流

### L1-PS-07 标签只能承接目标语言支持的控制流

1. **触发/前提**：PowerShell 7.6；源码存在标签、goto、嵌套 break/continue 或清理出口。本规则对普通单线程程序也适用。
2. **原行为**：PowerShell 的循环标签以 `:name` 放在循环语句前，`break name` 退出对应循环；不是 C/C++ 的 `name:` 任意跳转目的地。循环外的 break 还可能影响调用栈，不能拿它当任意 return/goto。
3. **映射条件**：按源的到达条件、跳转目的地、后续语句及清理范围选目标结构。源未被引用的标签可在确认不改变流程后去掉；有 goto/出口引用的标签先重建控制流，再处理名称。`finally`/函数返回/循环退出各有范围，不能只为通过语法而互换。
4. **反例**：把 C++ `report_ready:` 原样放入目标，被作为命令尝试调用；为消除该命令错误直接删掉仍被跳转引用的目标；合法的 PowerShell `:outer while (...)` 被当残留删除。
5. **未知处理**：标签引用、清理顺序或循环范围未定位时保留待确认，不声称等价；静态检查只核对应关系，不运行目标来试探语法。
6. **官方依据**：about_Break、about_Continue。

## 十、对象管道与外部状态的选择引导

PowerShell7.6的管道对象、输出流和外部进程是不同语义层。先看源需要的返回类型、字节、通道、等待及错误路径，不因语法更短合并它们。

- 外部程序直接调用后从LASTEXITCODE取得该次状态并及时保存；Start-Process返回/等待采用Process对象渠道，ArgumentList拼接与流重定向另核。源忽略非零状态时不新增throw，源传播失败时不吞掉；`$?`也不代完整退出码。
- Cmdlet非终止错误与.NET抛异常分开；只在源捕获的相应调用上考虑ErrorAction Stop，不无条件改变作用域。源静默兜底时不额外Write-Error/Verbose，以免增加可观察诊断。
- .NET字符串、char数组、byte数组及Base64文本分层；文本写入须看编码/BOM/换行，源写编码结果时不能改写成原始byte数组。返回管道时还看数组展开、单项/空项和是否混入诊断对象。
- 数值强转的舍入与源整除、原生字段宽度及容器值类型分别判断；不因为一项默认值相同就统一类型。环境展开、注册表原始值及身份查询依精确API，不能用惯用Trim或大小写忽略抹掉源条件。

依据：PowerShell7.6 about_Automatic_Variables、Start-Process、about_Preference_Variables、about_Pipelines、about_Character_Encoding；.NET对应类型/API。示例是选择引导，非语法/行为验证记录。

## 使用边界

将本页与所选方向和另一语言事实页组合；具体场景/系统差异按[共性索引](../seven-language-common-semantics.md)选读。缺逐例第三方证据保持 UNVERIFIED，本机不运行或编译。
