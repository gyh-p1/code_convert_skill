---
name: go-to-powershell
description: Use when converting Go source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → PowerShell 语言转换规则

> **适用基线**：Go 1.27 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
> **方向案例与证据**：如本地工作区存在 `docs/test/dataset/go-to-powershell/README.md`，按其中 case 分层查看；该本地数据目录不随 Git/Skill 分发。
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

### 规则 GO-PS-02：Go os.Exit 退出码向 PowerShell $LASTEXITCODE 与终止错误映射
1. **源码触发条件**：Go 源码中调用 `os.Exit(code)` 立即退出进程。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC](https://go.dev/ref/spec)）；目标语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)）。
3. **原可观察行为**：Go 进程立即终止并回传状态码，**跳过所有 defer 语句**！
4. **目标可选写法和不适用条件**：
   - *可选映射*：在独立脚本中映射为 `exit $code`；在模块函数中改写为设置 `$global:LASTEXITCODE = $code` 并 `throw` 终止错误。
   - *不适用条件*：严禁在函数内盲目调用 `exit` 终止用户当前会话。
5. **错误机械替换反例**：
   ```powershell
   # 错误：模块函数内直接 exit 杀掉交互式窗口
   function Run-Task { if ($failed) { exit 2 } } # 用户当前终端直接闪退！
   # 正确：抛出终止错误
   function Run-Task { if ($failed) { throw "Task failed with exit code 2" } }
   ```
6. **信息不足或实现相关时的处理**：若原 Go 代码中有未执行的 defer，在报告中警告其确定性丢失。
7. **直接官方 HTTPS 依据链接**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

### 规则 GO-PS-03：Go 常驻守护任务向 PowerShell 短生命周期脚本模型转换边界
1. **源码触发条件**：Go 源码中通过 `select {}` 实现常驻后台服务并监听信号。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 PowerShell 7.6（[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）。
3. **原可观察行为**：编译为原生守护进程长期运行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 PowerShell 中重构为单次触发任务或通过 `Start-Job` 注册后台作业，或依赖外部任务计划程序（Task Scheduler）。
   - *不适用条件*：严禁在交互式 PowerShell 脚本中写永久死循环死等，会占用宿主线程。
5. **错误机械替换反例**：
   ```powershell
   # 错误：直接在前台脚本写死循环阻塞控制台且无法优雅响应中断
   while ($true) { Start-Sleep -Seconds 1 }
   ```
6. **信息不足或实现相关时的处理**：若必须常驻，向用户提示脚本宿主生命周期限制。
7. **直接官方 HTTPS 依据链接**：[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)。

### 规则 GO-PS-04：Go []byte 字节切片向 PowerShell [byte[]] 与文本编码边界的映射
1. **源码触发条件**：Go 源码在字节层读写与变换数据，例如 `_ = os.WriteFile(in, []byte("operator=translator\nmode=controlled\n"), 0o644)`、`raw, _ := os.ReadFile(in)`、`[]byte(strings.TrimSpace(string(raw)))`、以及底层的 `sha256.Sum256(data)`/`base64.StdEncoding.EncodeToString`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #String_types](https://go.dev/ref/spec)）；目标语言 PowerShell 7.6（[MS-PS-CONTENT](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-content)、[MS-PS-ENCODING](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)）。
3. **原可观察行为**：Go 字符串是只读字节序列、允许包含 `0x00`；`[]byte(s)` 与 `string(b)` 互转按原始字节解释且长度按字节计；`os.WriteFile` 写出的正是给的这些字节，不做换行或 BOM 增删。
4. **目标可选写法和不适用条件**：
   - *可选映射*：字节数组用 `[byte[]]`；需要精确字节级写入时用 `[System.IO.File]::WriteAllBytes($path, $bytes)`，需要精确字节级读取时用 `[System.IO.File]::ReadAllBytes($path)`；确需 cmdlet 路径时使用面向字节的参数（`Set-Content -AsByteStream` / `Get-Content -AsByteStream`），并显式指定 `-Encoding utf8NoBOM` 以固定编码而不依赖宿主默认。
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

### 规则 GO-PS-06：Go error 返回与 defer 清理向 PowerShell 错误流、$? 与 finally 的映射
1. **源码触发条件**：Go 源码以 `(T, error)` 返回并在调用点 `if err != nil` 分流，同时用 `defer` 登记清理（如 `overwrite_rollback_check.go`/`recoverable_overwrite.go` 的备份—覆写—回滚顺序、`inbox_kv_parse.go` 的 `strings.Split` 解析失败分支），`parallel_cmd_runner.go` 还有 `defer cancel()` 与 `context.WithTimeout` 的超时错误分支。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Errors, #Defer_statements](https://go.dev/ref/spec)）；目标语言 PowerShell 7.6（[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)、[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)）。
3. **原可观察行为**：错误经返回值显式传递，调用方必须检查 `err != nil` 才会失败；未检查则继续执行；`defer` 在外层函数返回前按 LIFO 逆序执行，且对正常返回、`return` 提前退出与 `panic` 展开都生效。
4. **目标可选写法和不适用条件**：
   - *可选映射*：把“可继续的失败”写成非终止错误（`Write-Error`/`$PSCmdlet.WriteError()`）并保留后续处理，把“必须中断的失败”写成终止错误（`throw`/`-ErrorAction Stop`）；需要 `catch` 兜住 Cmdlet 的非终止错误时显式加 `-ErrorAction Stop`；清理动作放进 `finally`，按 Go 的逆序排列；判断外部进程结果时读 `$LASTEXITCODE`，判断 Cmdlet 结果时读 `$?`。
   - *不适用条件*：严禁用 `$?` 或 `$LASTEXITCODE` 作为跨多条语句的统一错误判断——`$?` 会被任何后续语句覆盖，`$LASTEXITCODE` 只在外部原生进程执行后更新，对纯 Cmdlet 流程不反映成败；`try`/`catch` 默认不捕获非终止错误；`exit` 会终止宿主、可能不执行 `finally`，因此**不得用 `exit` 代替 Go 中会在函数返回时执行的 `defer` 清理**。
5. **错误机械替换反例**：
   ```powershell
   # 错误：用 $? 承接 Go 的 err 检查，并用 exit 代替 defer 清理
   function Invoke-Stage {
       Write-FileAtomic $target $payload       # 内部以非终止错误报告失败
       if ($?) { Write-Host "ok" }             # 上一条语句已覆盖 $?，判断不可靠
       if (-not $?) { exit 1 }                 # exit 绕过 finally：备份/临时文件未清理
   }
   # 正确：终止错误 + finally 承接 defer 的清理职责
   function Invoke-Stage {
       try {
           Write-FileAtomic $target $payload -ErrorAction Stop
       } catch {
           Write-Error "stage failed: $($_.Exception.Message)"   # 对照 Go 的 error 返回
           throw                                                  # 对照 Go 的必须中断
       } finally {
           Remove-Item -LiteralPath $staging -ErrorAction SilentlyContinue  # 对照 defer
       }
   }
   ```
6. **信息不足或实现相关时的处理**：若无法确认某个 Go 错误在原程序中是“必须中断”还是“可忽略继续”，必须标注“错误严重级别待确认”，不得默认按终止错误处理；若原 Go 代码用 `panic`+`recover` 表达非局部失败，标注“panic/recover 与 PowerShell 错误流的对应关系待确认”。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Errors, #Defer_statements](https://go.dev/ref/spec)；[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)、[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

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
8. **来源与证据边界**：batch-01 B22（`handoff-2026-10-02-d30-inbox-kv-parse-go`）`self-review-1` 定位多余外层 `Join-Path` 与空字符串绑定，`target.self-repair-1.ps1` 修订后第 2 次自审无定位缺陷；目标侧解析/build PASS（job `eval-20261005-073327-f2280eff`）。仅作静态规则提炼；功能 oracle 未设，行为仍 `UNVERIFIED`。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
