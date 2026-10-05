---
name: powershell-to-python
description: Use when converting PowerShell source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → Python 语言转换规则

> **适用基线**：PowerShell 7.6 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 PowerShell](../../references/languages/powershell.md)与[目标语言 Python](../../references/languages/python.md)。
> **方向案例与证据**：如本地工作区存在 `docs/test/dataset/powershell-to-python/README.md`，按其中 case 分层查看；该本地数据目录不随 Git/Skill 分发。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 PowerShell → Python 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PS-PY-01：PowerShell 管道命令链向 Python 迭代器生成器与高阶函数映射
1. **源码触发条件**：PowerShell 源码中使用 `$input | Where-Object { ... } | ForEach-Object { ... }`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：对象逐个在管道中流式传递，处理大流时不占用全部内存。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用生成器表达式 `(fn(x) for x in input if cond(x))` 保持流式惰性求值；若需立即全量结果，使用列表推导 `[fn(x) for x in input if cond(x)]`。
   - *不适用条件*：严禁在无限流上使用列表推导（会导致内存耗尽 OOM）。
5. **错误机械替换反例**：
   ```python
   # 错误：针对大文件流或无限生成流使用列表推导，撑爆内存
   # lines = [line.strip() for line in huge_file]
   # 正确：使用生成器表达式流式处理
   lines = (line.strip() for line in huge_file)
   ```
6. **信息不足或实现相关时的处理**：若源管道包含特定 Cmdlet（如 `Sort-Object`），在 Python 中需要物化为列表再排序。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)；[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 PS-PY-02：PowerShell 单元素解包机制向 Python 列表长度隔离映射
1. **源码触发条件**：PowerShell 源码中处理管道输出，当结果仅有一项时自动变为标量。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)）；目标语言 Python 3.12。
3. **原可观察行为**：PS 管道输出零个元素返回 `$null`，一个元素返回标量对象，两个以上返回 `object[]`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Python 函数必须保持确定的返回类型契约！若声明返回 `list`，无论空、单元素还是多元素，统一返回 `list`。
   - *不适用条件*：严禁在 Python 中模仿 PowerShell 的自动解包行为（根据元素数量动态返回标量或列表），会给调用方类型检查带来极大混乱。
5. **错误机械替换反例**：
   ```python
   # 错误：模仿 PowerShell 的动态类型展开，破坏 Python 确定性接口契约
   def query_items():
       results = fetch()
       if len(results) == 1: return results[0] # 破坏了返回 list 的约定！
       return results
   # 正确：统一返回 list
   def query_items() -> list[Item]:
       return fetch()
   ```
6. **信息不足或实现相关时的处理**：对现有调用方做出防御性 `isinstance(res, list)` 适配。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)。

### 规则 PS-PY-03：PowerShell 退出码回写向 Python sys.exit 与返回值映射
1. **源码触发条件**：PowerShell 源码中使用 `exit $code` 或检查 `$LASTEXITCODE`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)）；目标语言 Python 3.12。
3. **原可观察行为**：回传退出状态码。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 CLI 入口处调用 `sys.exit(code)`；在普通模块函数中返回整数状态码或抛出异常。
   - *不适用条件*：严禁在被导入的模块内部直接调用 `sys.exit()`，会导致宿主解释器退出。
5. **错误机械替换反例**：
   ```python
   # 错误：在模块库函数内部调用 sys.exit
   def validate_config(cfg):
       if not cfg: sys.exit(1) # 导致第三方调用者进程无故终止！
   # 正确：抛出异常
   def validate_config(cfg):
       if not cfg: raise ValueError("Invalid configuration")
   ```
6. **信息不足或实现相关时的处理**：若需要调用外部原生命令并获取退出码，使用 `subprocess.run(..., check=False).returncode`。
7. **直接官方 HTTPS 依据链接**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

### 规则 PS-PY-04：PowerShell 对象属性、属性包与单元素退化向 Python `dict`/属性访问映射
1. **源码触发条件**：源码通过属性名从对象或属性包取值，并把结果直接参与后续处理，例如 `$Props = @{ Key = $Key; Time = [DateTime]::Now; Window = $Title.ToString() }` 与 `$obj = New-Object psobject -Property $Props`、`$UserProps.Add('AccountExpires', ...)`、`$attr = $m.Matches.Groups | Where-Object {$_.Name -eq 'Variable'} | ForEach-Object {$_.Value}`、`$userPrincipal.$a` 这种按名动态取值、`$_.properties['ServicePrincipalName']` 与 `$_.properties.name` 混用、以及 `Get-Random -Count 10` 返回单元素时结果为标量而非数组。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables), [MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)）；目标语言 Python 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html), [PY-LIB-DATACLASSES](https://docs.python.org/3.12/library/dataclasses.html)）。
3. **原可观察行为**：属性缺失时 PS 返回 `$null` 而不抛错，把它内插进字符串则得到空串；`@{}` 的键名大小写不敏感，`[ordered]@{}` 才保证插入顺序；同一个属性在不同记录上可能是字符串、日期或数字；管道/枚举结果在只有一个元素时退化为标量，`Group`/`Groups` 这类集合在只有一项时 `.Value` 与 `[0].Value` 表现不同。
4. **目标可选写法和不适用条件**：
   - *可选映射*：字段集合固定时用 `@dataclass`（或 `NamedTuple`）并显式声明类型；列集合确实动态时用 `dict` 并配 `TypedDict` 或键集合常量；按名动态取值用 `getattr(obj, name, None)`；需要保持插入顺序用 `dict`（3.7+ 语言保证）或 `collections.OrderedDict`；“可能没有值”用 `None`/`Optional[T]` 表达并在使用点显式分支。
   - *不适用条件*：严禁用 `obj[name]` 模拟 PS 的“属性缺失返回 `$null`”——Python 会抛 `KeyError`，与源的静默空值分支不同；也严禁用 `SimpleNamespace`/`setattr` 拼装动态属性来复刻 PSObject（丢失键集合与顺序约定）；`getattr(...)` 的默认值不能与“属性存在且为 `None`”混为一谈。
5. **错误机械替换反例**：
   ```python
   # 错误：用下标模拟 PS 的缺失属性语义，缺键即抛 KeyError
   account = row["properties"]["samaccountname"]
   # 正确：显式区分“缺失”与“存在但为空”
   props = row.get("properties", {})
   account = props.get("samaccountname")          # 缺失 -> None
   if account is None:
       account = ""                               # 与源的空串内插一致
   ```
6. **信息不足或实现相关时的处理**：属性集合是否随输入变化、键名大小写是否被依赖、以及源在该字段缺失时究竟是空串还是 `None`，都必须先确认；确认不了就停下标注，不要默认用 `dict` 或默认属性名拼写。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)；[PY-LIB-DATACLASSES](https://docs.python.org/3.12/library/dataclasses.html)。

### 规则 PS-PY-05：PowerShell `$null`/空数组/数值 0 真值向 Python `None` 与假值判定映射
1. **源码触发条件**：源码在条件或 `Where-Object` 脚本块里依赖 PS 真值，例如 `if (($ShiftState -band 0x8000) -eq 0x8000)` 与 `if ($Shift -xor $Caps)`、`if ($HND -eq $null)`、`$waveInGetNumDevsAddr = $null` 后的 `if ($waveInGetNumDevsAddr -eq $null) { Throw ... }`、`if ($DeviceCount -gt 0)`、`if ($Result.ReturnValue -eq 0)`、`if ($PSBoundParameters.Timeout -and (...))`、`while (!($FileDownload.IsCompleted))`、`if ($global:credential.UserName -and $global:credential.UserName -ne '')`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)）；目标语言 Python 3.12（[PY-REF-EXPRESSIONS](https://docs.python.org/3.12/reference/expressions.html), [PY-REF-DATA §3.1](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：`$null`、空数组、空字符串与数值 0 在布尔化时都为假，且 `$null` 与 0 在 `-eq` 下可区分（`$null -eq 0` 为假）但都为假值；`$PSBoundParameters.Timeout` 在参数未提供时不存在（相当于假），而显式传入 0 时同样为假，两条路径在源里走同一分支；把 `$null` 内插进字符串得到空串；`.ToString()` 对 `$null` 会抛错而不是返回空串。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按源真实集合选择判定——`x is None`、`x == ""`、`not x`、`isinstance(x, (list, tuple)) and len(x) == 0`；需要区分“未提供”与“传 0”时用 `None` 作默认值并显式判 `is None`；可选值用 `Optional[T]` 标注，`typing.Optional` 与 `dataclass` 默认值配合表达缺省。
   - *不适用条件*：严禁把 `if ($x -eq $null)` 机械写成 `if not x`——`not x` 会把空串、空列表、0 一并吞掉，扩大源的分支集合；严禁把 `if ($x)` 的 PS 真值语义直接当成 Python 真值语义（两者对“空容器/空串/0”一致，但对 `float('nan')`、自定义对象 `__bool__`、以及 `$null` 与 `False` 的区分并不一致）；`numpy` 等第三方类型的真值不适用本条。
5. **错误机械替换反例**：
   ```python
   # 错误：把 -eq $null 写成 not，0 与空串被一起并入该分支
   if not device_count:
       raise RuntimeError("Failed to enumerate any recording devices")
   # 正确：按源判定的是“句柄为 $null”还是“计数不大于 0”分别写
   if handle is None:
       raise RuntimeError("Failed to acquire handle")
   if device_count <= 0:
       raise RuntimeError("Failed to enumerate any recording devices")
   ```
6. **信息不足或实现相关时的处理**：源里某个判定到底针对 `$null`、空集合还是数值 0，以及参数默认值是 `$null` 还是 0，都必须先确认；确认不了就停下标注，不要用 `not x` 合并这些语义。
7. **直接官方 HTTPS 依据链接**：[PY-REF-EXPRESSIONS](https://docs.python.org/3.12/reference/expressions.html)；[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)。

### 规则 PS-PY-06：PowerShell `-match`/`-replace` 与 `.Replace()` 向 Python `re` 与显式空值替换映射
1. **源码触发条件**：源码用正则匹配或替换，例如 `if ($VideoController.VideoModeDescription -match '(?<ScreenWidth>^\d+) x (?<ScreenHeight>\d+) x .*$')`、`if ($caption -match $r)` 后 `Select-String -Pattern $r` 取 `$m.Matches.Groups`、`$Path -replace '\s+',""`、`$exportdata = $wlans | Foreach-Object {$_.Replace("    All User Profile     : ",$null)}`、`$caption.Replace("{$attr}", $v)`、`.Split('|')` 与 `.Contains('|')`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-COMPARE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators)）；目标语言 Python 3.12（[PY-LIB-RE](https://docs.python.org/3.12/library/re.html), [PY-LIB-STDTTYPES](https://docs.python.org/3.12/library/stdtypes.html)）。
3. **原可观察行为**：`-match`/`-replace` 默认大小写不敏感（可用 `-cmatch`/`-creplace` 改为敏感），使用 .NET 正则语法（命名组 `(?<name>...)`、替换串里的 `$1`/`${name}`），匹配成功会把结果放入 `$Matches` 自动变量；`-replace` 的替换值为 `$null` 时等价于空串，即删除匹配文本；`String.Replace` 是字面量子串替换、区分大小写、不做正则解释；`Select-String` 返回的是 `MatchInfo` 包装对象，其 `Matches.Groups` 结构与 `re.Match.groupdict()` 不同。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`-match` 默认不敏感语义用 `re.search(pattern, s, re.IGNORECASE)`（需要源的大小写敏感分支时用 `-cmatch` 对应的 `re.search(pattern, s)`）；命名组 `(?<name>...)` 改写为 Python 的 `(?P<name>...)` 并用 `m.group("name")` 取值；`-replace` 用 `re.sub(pattern, repl, s, flags=re.IGNORECASE)`，替换串里的 `$1`/`${name}` 改写为 `\1`/`\g<name>`；`String.Replace` 对应 `str.replace(old, new)`；`$null` 替换值对应 `""`。
   - *不适用条件*：严禁把 `-replace` 直接写成 `str.replace`（前者是正则、默认不敏感，后者是字面量且区分大小写，会静默漏替换）；严禁把 `repl` 传成 `None` 去模拟 `$null`（`re.sub` 要求字符串，会抛 `TypeError`）；严禁原样照搬 `$1` 反引用或 `(?<name>...)` 语法（Python 不支持该写法）。
5. **错误机械替换反例**：
   ```python
   # 错误：把默认不敏感的正则替换写成区分大小写的字面量替换，并把 $null 传成 None
   text = line.replace("    All User Profile     : ", None)   # TypeError
   normalized = re.sub(r"\s+", "", s)                         # 少了 IGNORECASE，与源默认不同
   # 正确：字面量替换用空串，正则替换显式声明大小写策略
   text = line.replace("    All User Profile     : ", "")
   normalized = re.sub(r"\s+", "", s, flags=re.IGNORECASE)
   ```
6. **信息不足或实现相关时的处理**：源里该处用的是不敏感还是敏感语义（`-match` 与 `-cmatch`、`.Replace` 与 `-replace` 不同）、命名组名与反引用编号、以及替换值是否可能为 `$null`，都必须先确认；确认不了就停下标注，不要默认按敏感或按字面量替换处理。
7. **直接官方 HTTPS 依据链接**：[PY-LIB-RE](https://docs.python.org/3.12/library/re.html)；[MS-PS-COMPARE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
