---
name: go-to-powershell
description: Use when converting Go source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → PowerShell 语言转换规则

> **适用基线**：Go 1.27 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Go → PowerShell 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-PS-01：Go 强类型结构体输出向 PowerShell PSCustomObject 管道对象流映射
1. **源码触发条件**：Go 源码中处理结构体切片并进行遍历处理。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）。
3. **原可观察行为**：强类型结构体字段访问，编译期严格类型保证。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `[PSCustomObject]@{ Field = val }` 并推入管道，以便下游通过 `$_` 访问属性。
   - *不适用条件*：严禁序列化为 JSON 字符串直接输出而不解包，会破坏管道后续的无缝处理。
5. **错误机械替换反例**：
   ```powershell
   # 错误：将结构体转为文本 JSON 输出，下游必须手动二次 ConvertFrom-Json
   $json = $data | ConvertTo-Json
   Write-Output $json
   # 正确：直接输出对象
   [PSCustomObject]@{
       Id   = $data.Id
       Name = $data.Name
   }
   ```
6. **信息不足或实现相关时的处理**：若字段涉及首字母大小写可见性，在 PowerShell 中统一规范为 PascalCase。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

### 规则 GO-PS-02：Go os.Exit 向 PowerShell 独立进程入口的退出边界
1. **源码触发条件**：源调用 `os.Exit(code)`，与普通函数返回/`panic` 清理不同。
2. **冻结版本/运行时/API 前提**：Go 1.27 → PowerShell 7.6；冻结独立 pwsh 进程还是模块/交互式调用，以及入口退出码与清理契约。
3. **原可观察行为**：`os.Exit` 立即结束整个进程并跳过 defer。PowerShell `exit` 不是“跳过所有 finally”的通用机制；官方文档明确 catch 中 exit 仍会执行 finally。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在独立脚本入口核对 `exit $code`、错误输出及受控清理；若源故意跳过清理，目标 finally 不能无条件新增该清理，需按冻结退出路径设计清理条件，或报告未映射点。
   - *不适用条件*：模块函数中的 `throw` 可以被调用方捕获，设置 `$LASTEXITCODE` 也不等于进程退出；它们不是 `os.Exit` 的自动等价。把独立程序改模块属于显式接口变更，未获允许不能如此降级，更不能退出用户交互会话。
5. **错误机械替换反例**：把所有 Go defer 都写进 finally，再将 os.Exit 替为 exit，可能新增源退出时不执行的清理；反过来删掉全部 finally 又破坏正常 return 的清理。
6. **信息不足或实现相关时的处理**：交付形态或退出路径不明时记录缺口；核对正常返回、panic/recover 和 os.Exit 三类路径，不通过新增强杀进程能力绕过。
7. **直接官方 HTTPS 依据链接**：[Go os.Exit](https://pkg.go.dev/os#Exit)；[PowerShell about_Try_Catch_Finally](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally?view=powershell-7.6)。

### 规则 GO-PS-03：Go 常驻任务向 PowerShell 的生命周期边界
1. **源码触发条件**：源通过循环/select 等维持进程，并具有请求处理、信号、取消或退出协议。
2. **冻结版本/运行时/API 前提**：Go 1.27 → PowerShell 7.6；记录独立宿主、生命周期、并发模型及实际停止条件。
3. **原可观察行为**：进程在明确停止条件前持续提供源码定义的行为；不能把“常驻”只当实现风格。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在受控独立宿主内保持原生命周期与停止协议；按适用并发/进程规则组织等待和清理，不新增持久化、权限或网络能力。
   - *不适用条件*：不能自动改为单次触发、定时任务、Start-Job 或计划程序；它们改变可用期、状态、父进程依赖或部署副作用，只有另行明确允许才是可选变体。
5. **错误机械替换反例**：源持续维护进程内状态，目标单次执行后退出；即使一次输出一致，也没有保留后续请求与状态行为。
6. **信息不足或实现相关时的处理**：宿主/取消/停止条件不明时加载[并发场景](../../scenes/concurrency/SKILL.md)与[进程场景](../../scenes/process-execution/SKILL.md)，登记缺口；文本转换不因此启动常驻任务，本机不运行。
7. **直接官方 HTTPS 依据链接**：[PowerShell about_Jobs](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)（后台作业模型，不是常驻生命周期自动等价保证）。

### 规则 GO-PS-04：Go []byte 字节切片向 PowerShell [byte[]] 与文本编码边界的映射
1. **源码触发条件**：Go 源码在字节层读写与变换数据，例如 `_ = os.WriteFile(in, []byte("operator=translator\nmode=controlled\n"), 0o644)`、`raw, _ := os.ReadFile(in)`、`[]byte(strings.TrimSpace(string(raw)))`、以及底层的 `sha256.Sum256(data)`/`base64.StdEncoding.EncodeToString`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #String_types](https://go.dev/ref/spec)）；目标语言 PowerShell 7.6（[MS-PS-CONTENT](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-content)、[MS-PS-ENCODING](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)）。
3. **原可观察行为**：Go 字符串是只读字节序列、允许包含 `0x00`；`[]byte(s)` 与 `string(b)` 互转按原始字节解释且长度按字节计；`os.WriteFile` 写出的正是给的这些字节，不做换行或 BOM 增删。
4. **目标可选写法和不适用条件**：
   - *可选映射*：字节数组用 `[byte[]]`；需要精确字节级写入时用 `[System.IO.File]::WriteAllBytes($path, $bytes)`，需要精确字节级读取时用 `[System.IO.File]::ReadAllBytes($path)`；确需 cmdlet 路径时使用面向字节的参数（`Set-Content -AsByteStream` / `Get-Content -AsByteStream`），按实际形态核对数组/流及是否需要 `-Raw`。字节流不经过文本编码，不能同时要求 `-Encoding`；只有明确文本交付才另冻结 `utf8NoBOM` 等编码。
   - *不适用条件*：严禁用 `Set-Content`/`Add-Content`/`Out-File` 默认的文本管道承接字节切片——数组元素会被按行连接、默认追加行尾换行、并按默认编码重新编码，字节内容与长度都会与原字节不一致；严禁把二进制数据当 `[string]` 走 `-Encoding` 往返后再当作原字节使用。
5. **错误机械替换反例**：
   ```powershell
   # 错误：把 Go 的 os.WriteFile(path, []byte(content), 0o644) 写成默认文本写入
   $bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
   Set-Content -Path $in -Value $bytes          # 元素被逐行连接 + 追加换行 + 默认编码
   # $bytes.Length 与文件实际字节数不再一致
   # 正确：字节进字节出
   [System.IO.File]::WriteAllBytes($in, $bytes)
   $roundTrip = [System.IO.File]::ReadAllBytes($in)   # 长度与内容逐字节对应
   ```
6. **信息不足或实现相关时的处理**：若无法确认原数据的编码（UTF-8 还是本地代码页）以及是否要求“逐字节一致”，必须标注“字节内容与编码前提待确认”，不得用任何默认编码猜测替代。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #String_types](https://go.dev/ref/spec)；[MS-PS-CONTENT](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-content)、[MS-PS-ENCODING](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)。

### 规则 GO-PS-05：Go Goroutine 与 Channel 汇聚向 PowerShell Runspace 并行的近似映射
1. **源码触发条件**：Go 源码用固定数量工作协程处理任务并汇聚结果，例如 `parallel_cmd_runner.go` 的 `results := make([]cmdResult, len(cmds))` + `var wg sync.WaitGroup` + `go func() { defer wg.Done(); ... }()`，`tcp_port_scanner.go` 的 `portChan` + 多个 `go scanWorker(portChan)`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Go_statements](https://go.dev/ref/spec)、[GO-MEM](https://go.dev/ref/mem)）；目标语言 PowerShell 7.6（[MS-PS-PARALLEL](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/foreach-object)、[MS-PS-JOBS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）。
3. **原可观察行为**：并发任务各自执行、共享状态受显式同步保护；`wg.Wait()` 之后全部结果已就绪；结果写入互不覆盖（每个任务写自己的下标/自己的队列位置）；channel 的缓冲容量决定发送端是否阻塞。
4. **目标可选写法和不适用条件**：
   - *可选映射*：有界并行用 `ForEach-Object -Parallel { ... } -ThrottleLimit N`（外部变量以 `$using:` 引入，结果经管道回收）；需要作业对象与显式等待时用 `Start-ThreadJob`/`Start-Job` 配 `Wait-Job`/`Receive-Job`。
   - *不适用条件*：严禁假定并行块内对父作用域变量的写入会回写父作用域——Runspace 之间不共享变量，写入会静默丢弃；结果必须经管道输出或 `Receive-Job` 收集；也不得依赖并行输出的顺序（与 Go 中显式按索引写 `results[i]` 的确定性不同），需要稳定顺序时必须显式排序。
5. **错误机械替换反例**：
   ```powershell
   # 错误：以为并行块里能像 Go 协程写共享切片那样直接写父作用域变量
   $results = @()
   1..4 | ForEach-Object -Parallel { $results += $_ }   # 每次迭代都是新 Runspace，写入丢失！
   $results.Count                                          # 仍为 0
   # 正确：经管道回收结果，并显式排序以固定顺序
   $results = 1..4 | ForEach-Object -Parallel { $_ } | Sort-Object
   ```
6. **信息不足或实现相关时的处理**：若源码依赖 channel 的阻塞背压、`select` 多路复用或 `context` 级联取消，必须标注“PowerShell 无 channel/select 对等物，背压与取消需重新设计”，交由并发场景 Skill 决定，不得声称行为等价。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Go_statements](https://go.dev/ref/spec)；[MS-PS-PARALLEL](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/foreach-object)、[MS-PS-JOBS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)。

### 规则 GO-PS-06：Go error 返回与 defer 清理向 PowerShell 控制流与 finally 映射
1. **源码触发条件**：源以 `(T, error)` 返回、在调用点检查/忽略错误，并通过 defer 登记清理。
2. **冻结版本/运行时/API 前提**：Go 1.27 → PowerShell 7.6；保留源错误是否被观察、传播、输出，以及实际清理时机。
3. **原可观察行为**：error 是返回值，未检查可以继续且不会自动打印；defer 在函数返回或该 goroutine 的 panic 展开时逆序执行，os.Exit 不执行（另见 GO-PS-02）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：以明确结果/错误表示及调用者检查保持原控制流，避免管道把多返回值意外展平。只有源相应边界确实需终止传播时才用 throw/终止错误；源确实输出错误时才选择对应通道，不因为 error 非 nil 就额外 Write-Error。已注册清理按作用域与逆序放入 finally，清理也可能改变 `$?`，错误要在产生点保存。
   - *不适用条件*：不把 `$?` 或 `$LASTEXITCODE` 当持久 error 对象：读取须紧随对应操作；后续命令可覆盖 `$?`，原生退出码也须及时保存。try/catch 默认不捕非终止错误。不能把普通函数返回换成脚本 exit；但也不能错误宣称 exit 一律绕过 finally。
5. **错误机械替换反例**：
   ```powershell
   # 反例：在读取操作状态前，另一个命令已改变 $?
   Invoke-Operation                    # 待测操作
   Write-Output "finished"           # 新增输出，且更新成功状态
   if (-not $?) { throw "failed" }    # 已不是 Invoke-Operation 的状态
   # 仅对契约以 $? 表示成败的操作，必须立即保存：
   Invoke-Operation
   $operationSucceeded = $?
   # 按冻结契约检查，不把此片段当通用 Go error 映射。
   ```
6. **信息不足或实现相关时的处理**：错误严重级别、输出/传播边界或 panic/recover 对应未知时登记，不默认升级为终止错误，不默认添加 stderr；清理失败与业务失败分别核对。
7. **直接官方 HTTPS 依据链接**：[Go defer](https://go.dev/ref/spec#Defer_statements)；[PowerShell about_Automatic_Variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)；[about_Try_Catch_Finally](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally?view=powershell-7.6)。

### 规则 GO-PS-07：多段路径与空字符串参数的绑定边界
1. **源码触发条件**：Go 用 `filepath.Join(base, part1, part2, ...)` 拼接多段路径，或 `strings.SplitN(line, "=", 2)` 后允许空键、空值并传给 PowerShell 函数。
2. **冻结版本/运行时/API 前提**：Go 1.27 → PowerShell 7.6；先核对目标 PS 版本，因为 `Join-Path -AdditionalChildPath` 自 PowerShell 6.0 起可用，7.6 的 `-ChildPath` 也可接受数组。
3. **原可观察行为**：每个路径段都参与拼接；Go 字符串参数可为 `""`，例如 `=x` 和 `mode=` 分别形成空键与空值，后续 JSON 输出不能因参数绑定失败而中断。
4. **目标可选写法和不适用条件**：每个嵌套 `Join-Path` 都须同时有 `-Path` 与 `-ChildPath`，三段可嵌套两层；在 7.6 也可用 `-AdditionalChildPath` 或数组式 `-ChildPath`。若函数参数必须存在但允许空字符串，加 `[AllowEmptyString()]`；若省略参数也有效，可将其设为非 Mandatory 并显式处理默认值。`[AllowNull()]` 对 `[string]` 参数不能单独保证接收 `$null`，需按实际类型另行设计。
5. **错误机械替换反例**：
   ```powershell
   $root = Join-Path (Join-Path (Join-Path $tmp 'a') 'b') # 错误：最外层缺 ChildPath
   $root = Join-Path (Join-Path $tmp 'a') 'b'             # 两层均有两个参数
   # PowerShell 7.6 也可写：Join-Path -Path $tmp -ChildPath 'a' -AdditionalChildPath 'b'
   function Encode {
     param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Value)
       return $Value
   }
   ```
6. **信息不足或实现相关时的处理**：若源数据是否会有空键/空值、`$null` 或目标 PS 版本不明，先记待确认；不要把 B22 的错误概括成“`Join-Path` 只能接收两段”，也不靠 build PASS 推断所有输入已匹配。
7. **直接官方 HTTPS 依据链接**：[PowerShell 7.6 `Join-Path`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/join-path?view=powershell-7.6)；[高级函数参数的 `AllowEmptyString`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters?view=powershell-7.6)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
