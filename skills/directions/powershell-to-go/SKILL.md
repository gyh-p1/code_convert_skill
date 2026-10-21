---
name: powershell-to-go
description: Use when converting PowerShell source to Go; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → Go 语言转换规则

> **适用基线**：PowerShell 7.6 → Go 1.27。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 PowerShell](../../references/languages/powershell.md)与[目标语言 Go](../../references/languages/go.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 PowerShell → Go 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PS-GO-01：PowerShell 弱类型管道数据向 Go 显式结构体与切片映射
1. **源码触发条件**：PowerShell 源码中通过动态哈希表或对象管道传递松散属性。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（MS-PS-PIPE）；目标语言 Go 1.27（GO-SPEC #Struct_types）。
3. **原可观察行为**：弱类型反射访问，属性缺失返回 `$null`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：字段和类型封闭时可定义 `type Record struct` 与 `[]Record`；源需枚举未知字段、区分缺失/null 或处理动态对象时，可保留 `map[string]any`、原始字段或显式存在标志，按源逐点校验。
   - *不适用条件*：不能为静态类型偏好丢失源实际读取／拒绝的字段；也不能以 map 为由跳过存在性、数值类型和错误分流。选结构体还是 map 由源可观察行为决定。
5. **错误机械替换反例**：
   ```go
   // 错误：未经类型核对的单返回断言引发 panic；问题不在使用 map 本身
   m := map[string]any{"id": 1}
   id := m["id"].(string) // panic: interface conversion: any is int, not string
   // 正确：定义明确结构体
   type Record struct { ID int }
   ```
6. **信息不足或实现相关时的处理**：若源来自外部 JSON，核源是否枚举／拒绝未知键及是否区分缺失/null；默认结构体解码忽略未知字段不能代替源的 UNKNOWN_FIELD 路径。验证与解码分开，错误字段、选择顺序与时点按源，不默认所有未知字段都拒绝。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Struct_types；MS-PS-PIPE。

### 规则 PS-GO-02：PowerShell 错误流重定向向 Go 显式 error 与 stderr 隔离映射
1. **源码触发条件**：PowerShell 源码中使用 `2>&1` 将错误流合并到标准输出，或判断 `$?`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（MS-PS-AUTO, MS-PS-PREF）；目标语言 Go 1.27（GO-SPEC #Errors）。
3. **原可观察行为**：PS 将错误记录混合进管道输出流。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按源实际重定向保留流合并/分离、ErrorRecord 与字符串对象、顺序和 $?/$LASTEXITCODE 的消费者。Go 可选显式结果/error，但不因惯用法把源2>&1拆回 stderr，记录打印与返回状态也分别保留。
   - *不适用条件*：不得把源写 stdout 的诊断自动挪 stderr 或新增 error；也不能删源实际失败标志。CLI 流与函数返回不是同一个状态。
5. **错误机械替换反例**：
   ```go
   // 条件示意：打印诊断与返回状态须按源，不因名称 Error 自动判这种写法非法
   func Process() error {
       fmt.Println("Error: something failed")
       return nil // 调用方误以为成功！
   }
   // 另一候选：仅源对应失败确实通过返回/终止传递时适用
   func Process() error {
       return errors.New("something failed")
   }
   ```
6. **信息不足或实现相关时的处理**：若原脚本调用了原生可执行程序并重定向输出，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Errors；MS-PS-AUTO。

### 规则 PS-GO-03：PowerShell Start-ThreadJob 向 Go Goroutine 轻量并发与 WaitGroup 映射
1. **源码触发条件**：PowerShell 源码中使用 `Start-ThreadJob` 启动后台任务。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（MS-PS-THREADJOB）；目标语言 Go 1.27（GO-SPEC #Go_statements）。
3. **原可观察行为**：在后台 Runspace 线程池中并发执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：核 Job/Runspace 的启动、作用域、结果与错误保存、Receive/Wait/Stop 时点；goroutine/WaitGroup 仅这些义务对应时用。源不等待时不自动补全等，源后台存活期也不能缩到目标 main 退出。
   - *不适用条件*：捕获按冻结 Go 版本及循环变量声明方式核（:= 的每次迭代变量与复用变量不同），不因防错偏好全禁合法捕获；同步、变量复制与共享按源保留。
5. **错误机械替换反例**：
   ```go
   // 错误：启动后台 Goroutine 未做同步等待，主函数提前退出导致后台任务被杀死
   func main() {
       go doBackground()
   } // main 退出，所有 Goroutine 立即终止！
   // 条件候选：仅源确在此点等待全部任务时适用
   func main() {
       var wg sync.WaitGroup
       wg.Add(1)
       go func() { defer wg.Done(); doBackground() }()
       wg.Wait()
   }
   ```
6. **信息不足或实现相关时的处理**：若需获取后台任务返回值，结合 Channel 传递。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Go_statements；MS-PS-THREADJOB。

### 规则 PS-GO-04：PowerShell WMI/`Invoke-WmiMethod` 返回码与属性存在性向 Go error 值与类型断言映射
1. **源码触发条件**：源码调用 WMI 或同类返回“结果对象 + 返回码”的 .NET API，并检查其属性，例如 `$Result = Invoke-WmiMethod @WmiMethodArgs -Class 'StdRegProv' -Name 'CreateKey' -ArgumentList $Hive, $RegistryKeyPath` 后接 `if ($Result.ReturnValue -ne 0) { throw ... }`，以及 `$Result = ... -Name 'CheckAccess' ...` 后接 `if (-not $Result.bGranted)`、`$PowerShellPath = $Result.sValue`、`if (($Result.ReturnValue -eq 0) -and ($Result.sValue))`；还包括 `$Hive = 2147483650` 这类超出 32 位有符号范围的句柄常量与 `$RequiredPermissions` 的 `-bor` 组合。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（MS-PS-ERROR）；目标语言 Go 1.27（GO-SPEC #Errors, GO-PKG-FMT）。
3. **原可观察行为**：WMI 结果对象的 `ReturnValue` 是提供程序返回的无符号 32 位码，0 表示成功、非 0 表示失败；`bGranted`、`sValue` 等属性只在特定方法上存在，方法失败时对应属性可能缺失而不是空值；`$Result.sValue` 取到的是字符串，`$Result` 本身在调用失败时可能为 `$null`，此时属性访问得到 `$null` 而脚本继续执行（除非抛终止错误）。PS 的整数体系不限制这一层宽度，`2147483650` 这类常量按更大宽度整型承载。
4. **目标可选写法和不适用条件**：
   - *可选映射*：把“结果对象 + 返回码”映射为 `(T, error)`：返回码非 0 时构造 `fmt.Errorf` 并携带原始 `uint32` 码（`%#x` 便于比对）；结果属性用固定 `struct`；只能从 `map[string]any` 或 COM 类动态类型取值时，用带 `ok` 的双返回断言（`v, ok := m["sValue"].(string)`）并把 `!ok` 当作显式错误分支；WMI 的大句柄常量用 `uint32`/`uintptr` 并按目标 API 形参宽度显式标注。
   - *不适用条件*：严禁把返回码检查机械写成“不检查”或直接 `panic`——源里 `throw` 前的条件判定就是失败路径本身；严禁用单返回断言 `m["sValue"].(string)`（属性缺失或类型不同会直接 panic，而源行为是继续或走 `throw`）；严禁把 `int32` 与 `uint32` 之间隐式混用（Go 禁止隐式转换，且 WMI 返回码取负值时符号解释会改变比较结果）。
5. **错误机械替换反例**：
   ```go
   // 错误：单返回断言 + 忽略返回码，缺属性即 panic
   res := callWMIMethod("StdRegProv", "CreateKey")
   key := res["sValue"].(string)          // panic: 失败时无 sValue
   if res["ReturnValue"].(int32) != 0 { } // 类型/符号不符时同样 panic
   // 双返回断言只是安全取值候选；CreateKey/CheckAccess/读取值方法各有不同出参。
   // 仅检查源实际检查的属性与 ReturnValue，不能因缺少不适用的 sValue 就新增失败。
   ```
6. **信息不足或实现相关时的处理**：具体方法的返回码取值集合、属性名与是否可能缺失、以及返回码字段的符号宽度，都必须从目标 API 文档或调用方契约确认；确认不了就停下标注，不要假定“非 0 且非空即成功”或反推一个码表。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Errors；GO-PKG-FMT。

### 规则 PS-GO-05：PowerShell `.Count`/`$null`/空集合判定向 Go `len`/`nil` 与 map 存在性映射
1. **源码触发条件**：源码对可能为空的取值做计数或存在性判定，例如 `if (($Result.ReturnValue -eq 0) -and ($Result.sValue))`、`[byte[]]$Data = @()` 之后 `if($Data.Length -eq 0){Start-Sleep -Milliseconds 100}` 与 `if($Data -ne $null){...}`、`if(($i -ne $null) -and (($r -ne "") -or ($e -ne "")))`、`if($Socket -eq $null){break}`、`if (($attr.Contains('|')))` 前后对集合/字符串的空值判定、`$null = $hostList.Add($iHostPart1)`、`Get-Random -Count 10` 返回单元素时的标量退化。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（MS-PS-ARRAY, MS-PS-OPERATORS）；目标语言 Go 1.27（GO-SPEC #Slice_types, GO-SPEC #Index_expressions）。
3. **原可观察行为**：null/空串/0 的布尔与 Count/Length 是不同操作。PowerShell 7 正常模式下 null.Count 为0，标量可有自动 Count=1，数组0项为假、1项取该项真值、多项为真；空 Hash 等非 IList 对象不按数组规则泛化。StrictMode/显式属性覆盖及管道解包另核，不能把 null 所有属性概括为 null。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Go 用 `len(data) == 0` 覆盖“空或未初始化”（nil 切片与空切片长度都为 0）；确实需要区分“缺失”与“存在但空”时使用带 `ok` 的 map 取值、`*T` 指针或显式的 `hasValue bool` 字段；从 JSON 反序列化时把 `null` 与 `[]` 分别处理，不要靠 `len` 区分；字符串空判定用 `s == ""`（`len(s) == 0` 等价）。
   - *不适用条件*：严禁把 `if ($x)` 机械写成 `if x != nil` 或 `if len(x) > 0` 后就不再区分两者（源中“无结果”与“结果为空”若在后续路径上可观察，用 `len` 会合并它们）；严禁用 `data == nil` 判断“空切片”（非 nil 的空切片会被判为存在）；严禁把 map 取值的零值当作“键存在且值为零”（须用 `v, ok := m[k]`）。
5. **错误机械替换反例**：
   ```go
   // 错误：用 nil 判断“空”，忽略非 nil 空切片；缺键的零值被当成有效值
   if data == nil { /* 源里 -eq $null 命中的分支 */ }
   val := m["sValue"] // 键缺失时是 ""，被当成“存在且为空”
   // 正确：长度判定 + 存在性判定分开
   if len(data) == 0 { /* 空或未初始化 */ }
   val, ok := m["sValue"]
   if !ok { /* 键缺失，与“存在但为空串”区分 */ }
   ```
6. **信息不足或实现相关时的处理**：源里“空集合”与“未赋值”在后续是否可区分、`.Count` 读取点是否可能作用于 `$null`、以及 map 的键是否必然存在，都必须先确认；确认不了就停下标注，不要默认用 `len` 一种判定覆盖两种语义。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Slice_types；MS-PS-ARRAY。

### 规则 PS-GO-06：PowerShell 字符串与字节/UTF-16/Base64 边界向 Go `string`/`[]byte` 显式编码映射
1. **源码触发条件**：源码在字符串与字节序列之间转换并跨进程/网络边界，例如 `$EncodedPayload = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($Payload))`、`$Payload = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Result.sValue))`、`[byte[]]$Data = $Encoding.GetBytes($i)` 与 `$Encoding.GetString($Data)` 用 `New-Object System.Text.AsciiEncoding`、`$CSVEntry` 以 `Out-File -Encoding unicode` 追加写盘、`[byte[]]$bytes = 0..65535|%{0}` 与 `$FileStream.Read($MZHeader,0,2)`、`[System.BitConverter]::GetBytes(...)`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（MS-PS-PIPE）；目标语言 Go 1.27（GO-SPEC #String_types, GO-PKG-UNICODE-UTF16, GO-PKG-ENCODING-BASE64）。
3. **原可观察行为**：`[Text.Encoding]::Unicode` 是 UTF-16 小端（每字符 2 字节，代理对 4 字节，`GetBytes` 不带 BOM），`-EncodedCommand` 一类消费方依赖该布局；`Out-File -Encoding unicode` 会写入 BOM；`ASCIIEncoding` 遇到非 ASCII 字符替换为 `?`（0x3F）而不是报错；`GetBytes` 结果长度是编码后的字节数，与 `.Length` 的 UTF-16 代码单元数不同；`0..65535|%{0}` 构造的是 65536 个元素的 `[byte[]]`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`string` 到字节用 `[]byte(s)`（UTF-8）或 `utf16.Encode([]rune(s))` 再按小端写出 `[]byte`（对应 `Encoding.Unicode`）；需要 BOM 时显式写 `0xFF, 0xFE`；Base64 用 `base64.StdEncoding.EncodeToString`/`DecodeString`；跨 C ABI 或需要 NUL 结尾时显式追加 `0`；缓冲区用 `make([]byte, n)` 而不是靠字符串拼接增长。
   - *不适用条件*：严禁把 `[Text.Encoding]::Unicode.GetBytes($s)` 机械替换为 `[]byte(s)`——UTF-8 与 UTF-16LE 的字节布局与长度都不同，消费方会解析失败；严禁把 `ASCIIEncoding.GetBytes` 换成 `[]byte(s)`（源会把非 ASCII 折叠为 `?`，UTF-8 会保留多字节，长度与内容都变）；严禁依赖 Go 字符串的 `len` 等于字符数（`len(s)` 是字节数，字符数用 `utf8.RuneCountInString`）。
5. **错误机械替换反例**：
   ```go
   // 错误：把 Encoding.Unicode 当成 UTF-8，解码端得到不同的字节序列
   payload := []byte(script)                       // UTF-8
   encoded := base64.StdEncoding.EncodeToString(payload)
   // 正确：按 UTF-16LE 显式编码，必要时补 BOM
   units := utf16.Encode([]rune(script))
   buf := make([]byte, 0, len(units)*2)
   for _, u := range units {
       buf = append(buf, byte(u), byte(u>>8))
   }
   encoded := base64.StdEncoding.EncodeToString(buf)
   ```
6. **信息不足或实现相关时的处理**：消费方期望的编码、是否需要 BOM、以及源里 `GetBytes`/`GetString` 所用的编码器实例（ASCII/Unicode/UTF8/默认）都必须逐点确认；确认不了就停下标注，不要假定默认编码，也不要把“字节数”和“字符数”互换使用。
7. **资料依据（名称/版本/章节）**：GO-SPEC #String_types；GO-PKG-UNICODE-UTF16。

### JSON 深度与集合形状的补充消费点

源使用 ConvertFrom-Json 时，按 [PowerShell L1-PS-08/09](../../references/languages/powershell.md#l1-ps-08-函数-success-流集合对象与泛型调用) 和 [Go L1-GO-15](../../references/languages/go.md#l1-go-15-encodingjson-的替换重复键与数值路径)分别保持输入深度、原数组对象／成功流、重复键和输出约定。Go 解码器能接受更深的文档不表示保持了源的 -Depth；nil slice 与空 slice 不一律互换。具体边界按源入口的失败时点和冻结预期核对，不新增解析驱动或统一硬编码某个用例的上限。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
