---
name: python-to-powershell
description: Use when converting Python source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → PowerShell 语言转换规则

> **适用基线**：CPython 3.12 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Python](../../references/languages/python.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Python → PowerShell 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PY-PS-01：Python 大小写敏感变量/方法向 PowerShell 大小写不敏感环境重构映射
1. **源码触发条件**：Python 源码中定义仅有大小写差异的不同标识符（如 `data` 与 `Data`，或 `val` 与 `VAL`）。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)）。
3. **原可观察行为**：Python 严格区分大小写，`data` 和 `Data` 是两个完全独立、互不干扰的变量。
4. **目标可选写法和不适用条件**：
   - *可选映射*：PowerShell 语法与变量查找**默认大小写不敏感**！`$data` 与 `$Data` 会访问同一个变量。必须对同名大小写变量显式重命名（如 `$dataVal` 与 `$dataObj`），消除冲突。
   - *不适用条件*：严禁照抄仅大小写不同的变量名，会导致其中一个变量被隐式覆盖损毁。
5. **错误机械替换反例**：
   ```powershell
   # 错误：在 PowerShell 中 $data 与 $Data 是同一个变量，发生相互覆盖
   $data = "initial"
   $Data = "override" # 覆盖了 $data！
   # Write-Output $data 输出 "override"，原数据丢失！
   # 正确：显式区分变量命名
   $dataText = "initial"
   $dataRecord = "override"
   ```
6. **信息不足或实现相关时的处理**：扫描源文件全部符号表，建立大小写冲突清单并报告用户。
7. **直接官方 HTTPS 依据链接**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

### 规则 PY-PS-02：Python 列表推导向 PowerShell 管道过滤与展开映射
1. **源码触发条件**：Python 源码中使用 `[x * 2 for x in items if x > 0]` 列表推导式。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）。
3. **原可观察行为**：即时计算并生成新的 `list` 对象。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `$items | Where-Object { $_ -gt 0 } | ForEach-Object { $_ * 2 }`；若在循环内追求极速，使用 `foreach ($x in $items)` 语句。
   - *不适用条件*：注意 PowerShell 数组通过 `+=` 扩展时会全量复制数组，大循环累加必须使用 `[System.Collections.Generic.List[T]]`。
5. **错误机械替换反例**：
   ```powershell
   # 错误：在大循环中使用 += 累加数组，时间复杂度退化为 O(N^2)
   $res = @()
   foreach ($x in $items) { $res += $x } # 每次分配新数组并全量复制！
   # 正确：使用管道或 Generic.List
   $res = [System.Collections.Generic.List[object]]::new()
   foreach ($x in $items) { $res.Add($x) }
   ```
6. **信息不足或实现相关时的处理**：数据规模未标明时，默认提供管道实现并在性能敏感处提示。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

### 规则 PY-PS-03：Python 异常层次向 PowerShell 终止错误与 catch 映射
1. **源码触发条件**：Python 源码中使用 `raise ValueError(...)` 并通过 `except Exception as e:` 捕获。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 PowerShell 7.6（[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）。
3. **原可观察行为**：抛出异常，中断执行，打印 traceback。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `throw [System.ArgumentException]::new("...")`；捕获使用 `try { ... } catch { ... }`，通过 `$_` 获取当前异常对象。
   - *不适用条件*：严禁在 catch 块中忽略 `$_` 的具体内容而直接静默返回。
5. **错误机械替换反例**：
   ```powershell
   # 错误：捕获后未打印或记录异常信息，静默掩盖严重系统故障
   try { Dangerous-Action } catch { } # 盲捕获吞没错误！
   # 正确：至少记录错误
   try { Dangerous-Action } catch { Write-Error "Action failed: $_" }
   ```
6. **信息不足或实现相关时的处理**：若源异常为特定业务自定义类，映射为 `[System.Exception]` 并包含原异常名。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)。

### 规则 PY-PS-04：Python 任意精度整数与整除向 PowerShell/.NET 定宽数值与舍入语义映射
1. **源码触发条件**：Python 源码中出现 `int` 参与的累计计数或大数运算、`//` 整除（如 `score // 10`）、`min(...)` 数值裁剪、掩码 `& 0xFFFFFFFF`，或这些结果被写入容器后再读出。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 PowerShell 7.6（[MS-PS-ARITH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators)）。
3. **原可观察行为**：`int` 为任意精度、无溢出概念；`//` 向下取整（`-7 // 2 == -4`）；如需定宽回绕必须由源码显式施加位掩码。
4. **目标可选写法和不适用条件**：
   - *可选映射*：可能超出 32/64 位的量用 `[long]`/`[bigint]` 显式承载；`a // b` 映射为 `[math]::Floor($a / $b)`（必要时再转 `[long]`）；需要定宽截断时显式 `-band 0xFFFFFFFF`；`min(...)` 用 `[math]::Min(...)` 并保持两侧同一数值类型。
   - *不适用条件*：严禁把 `a // b` 机械替换为 `[int]($a / $b)`——PowerShell 的数值转换在 `.5` 处就近取偶（官方示例 `[int](7 / 2)` 得 `4`、`[int](5 / 2)` 得 `2`），既不同于 Python 的向下取整，也不同于向零截断。也不得假定 PowerShell 算术保持 Python 的任意精度：结果超出 `[long]` 范围时类型会被自动放宽为 `[double]` 并丢失低位精度；而强类型 `[int]`/`[long]` 的变量声明、参数绑定或属性赋值会恢复定宽语义，越界不再自动扩展。
5. **错误机械替换反例**：
   ```powershell
   # Python 原型：level = min(score // 10, 4)
   $score = 15
   $level = [int]($score / 10)                            # 错误：就近取偶得 2，Python 中 15 // 10 得 1
   $level = [math]::Min([math]::Floor($score / 10), 4)    # 正确：向下取整后再裁剪
   # 错误：假定大整数运算不丢精度
   $total = [long]9223372036854775807 + 2     # 结果被放宽为 [double]，低位精度丢失
   $total = [bigint]9223372036854775807 + 2   # 正确：需要任意精度时显式使用 [bigint]
   ```
6. **信息不足或实现相关时的处理**：源数值的取值范围不明时（字节计数、时间戳差值、哈希值、加密大整数）必须停下并要求给出上界，或直接改用 `[bigint]`，不得默认挑 `[int]`；源若依赖 `& 0xFFFFFFFF` 之类掩码，需逐处确认掩码宽度并在目标显式保留。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)；[MS-PS-ARITH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators)。

### 规则 PY-PS-05：Python 异常兜底与原生命令返回值向 PowerShell 非终止错误与 `$LASTEXITCODE` 映射
1. **源码触发条件**：Python 源码用 `except Exception: pass`（或 `except Exception:` 后静默继续）包住平台采集类调用，或用 `subprocess.call([...])`、`os.system("...")` 调外部命令而忽略其返回码，以及依赖“失败必然抛异常”的 `try/except` 结构。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-LIB-SUBPROCESS](https://docs.python.org/3.12/library/subprocess.html)）；目标语言 PowerShell 7.6（[MS-PS-TCF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)、[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)）。
3. **原可观察行为**：Python 中失败即抛异常并被 `except` 捕获；`subprocess.call` 不抛异常而返回退出码，`os.system` 返回等待状态，调用方只有显式检查才能发现失败。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Cmdlet 的失败默认是**非终止错误**（写入错误流、流程继续），`try`/`catch` 不会捕获它；要捕获须在该语句上显式 `-ErrorAction Stop`，或在作用域内设置 `$ErrorActionPreference = 'Stop'`。原生命令（`& exe @args`、`Start-Process`）的成败用 `$LASTEXITCODE` 判定并显式 `throw`，不要把 `$?` 当退出码使用（`$?` 只反映上一条语句，且会被后续语句覆盖）。
   - *不适用条件*：严禁把 `except Exception: pass` 机械替换为 `try { ... } catch { }` 并当作等价——非终止错误会穿过 `try`/`catch`，源中的“静默兜底”在目标中退化为“错误照常输出、流程照常继续”。也严禁用 `if (-not $?)` 取代退出码检查：`$?` 与 `$LASTEXITCODE` 是两个不同信号，前者不区分“Cmdlet 写了非终止错误”与“原生命令返回非零”。
5. **错误机械替换反例**：
   ```powershell
   # Python 原型：for ...: try: get_stats() except Exception: pass
   # 错误：Get-Content 失败只写非终止错误，catch 根本不触发，静默兜底失效
   try { Get-Content -Path $missing } catch { }        # 错误流照样输出，流程继续
   # 正确：先把非终止错误提升为终止错误，再捕获
   try { Get-Content -Path $missing -ErrorAction Stop } catch { Write-Verbose "skip: $_" }
   # 错误：忽略原生命令退出码
   & $nativeTool @toolArgs                             # $LASTEXITCODE 被丢弃
   & $nativeTool @toolArgs
   if ($LASTEXITCODE -ne 0) { throw "native tool failed: $LASTEXITCODE" }   # 正确
   ```
6. **信息不足或实现相关时的处理**：无法确认某命令写的是终止还是非终止错误时（第三方模块、包装函数），一律按非终止处理并要求 `-ErrorAction Stop`；映射 `subprocess.call`/`os.system` 前须逐条列出退出码含义，不得默认非零码即业务正常，也不得假定目标命令沿用同一套退出码。
7. **直接官方 HTTPS 依据链接**：[MS-PS-TCF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)；[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)；[PY-LIB-SUBPROCESS](https://docs.python.org/3.12/library/subprocess.html)。

### 规则 PY-PS-06：Python `str.encode()`/`bytes`/base64 写盘向 PowerShell .NET 字符串与 `[byte[]]` 映射
1. **源码触发条件**：Python 源码中出现 `data.encode()`、`bytes`/`bytearray`、`base64.b64encode(...)`、`open(path, "wb")` 或 `open(path, "rb")` 的二进制读写。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-LIB-BASE64](https://docs.python.org/3.12/library/base64.html)）；目标语言 PowerShell 7.6（[MS-PS-ENC](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)）。
3. **原可观察行为**：`str` 与 `bytes` 严格隔离、混用抛 `TypeError`；`b64encode` 接受并返回 `bytes`；`"wb"` 只接受 bytes，写出的字节与输入逐字节一致（保留 `\0`、不追加换行）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`data.encode()` 映射为 `[System.Text.Encoding]::UTF8.GetBytes($data)`（得到 `[byte[]]`）；`base64.b64encode(...)` 映射为 `[System.Convert]::ToBase64String(<byte[]>)`（返回 `System.String`）；`open(..., "wb")` 映射为 `[System.IO.File]::WriteAllBytes($path, $bytes)` 或 `Set-Content -AsByteStream`；`open(..., "rb")` 映射为 `[System.IO.File]::ReadAllBytes($path)`。
   - *不适用条件*：严禁假定 PowerShell 字符串与 `[byte[]]` 可隐式互转——`System.String` 是 UTF-16 字符序列，`[System.Convert]::ToBase64String` / `FromBase64String` 的重载要求 `[byte[]]`，传入 `.ToCharArray()` 或裸字符串都拿不到正确的 UTF-8 字节序列；严禁用 `Set-Content`/`Out-File` 把 base64 结果（字符串）写进目标文件，那是把 base64 文本当成原始字节；也严禁用 `Get-Content -Raw` 读二进制后再做字符串拼接，文本解码会破坏不属于该编码的字节。
5. **错误机械替换反例**：
   ```powershell
   # Python 原型：encoded_data = base64.b64encode(data.encode()); open(f,"wb").write(encoded_data)
   $data  = "import socketserver; socketserver.TCPServer(('localhost', 9999), socketserver.StreamRequestHandler)"
   $chars = $data.ToCharArray()                 # 错误：得到 [char[]]，不是编码后的字节
   $b64   = [Convert]::ToBase64String($chars)   # 错误：重载要求 [byte[]]；按元素强转得到的也是 UTF-16 代码单元，不是 UTF-8 字节
   Set-Content -Path $filename -Value $b64      # 错误：写进文件的是 base64 文本，不是原始字节
   # 正确：显式编码取字节，再按字节写盘
   $bytes = [System.Text.Encoding]::UTF8.GetBytes($data)
   $b64   = [Convert]::ToBase64String($bytes)
   [System.IO.File]::WriteAllBytes($filename, $bytes)
   ```
6. **信息不足或实现相关时的处理**：源 `.encode()` 未给实参时须确认其默认编码（Python 3 为 UTF-8）；源声明 `latin-1`/`gbk` 等必须显式映射为对应的 .NET `Encoding`，且 .NET (Core) 默认只内置 Unicode/ASCII 编码、非 Unicode 代码页可能需要先注册代码页提供程序才可取到，属于必须核对的目标运行时前提；`open()` 的写入模式（截断/追加）也要一并确认。
7. **直接官方 HTTPS 依据链接**：[PY-LIB-BASE64](https://docs.python.org/3.12/library/base64.html)；[MS-PS-ENC](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)；[DOTNET-API](https://learn.microsoft.com/en-us/dotnet/api/)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
