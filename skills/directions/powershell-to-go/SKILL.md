---
name: powershell-to-go
description: Use when converting PowerShell source to Go; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → Go 语言转换规则

> **适用基线**：PowerShell 7.6 → Go 1.27。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 PowerShell](../../references/languages/powershell.md)与[目标语言 Go](../../references/languages/go.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 PowerShell → Go 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PS-GO-01：PowerShell 弱类型管道数据向 Go 显式结构体与切片映射
1. **源码触发条件**：PowerShell 源码中通过动态哈希表或对象管道传递松散属性。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 Go 1.27（[GO-SPEC #Struct_types](https://go.dev/ref/spec)）。
3. **原可观察行为**：弱类型反射访问，属性缺失返回 `$null`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Go 中定义静态 `type Record struct`，属性定义为显式字段；通过结构体切片 `[]Record` 批量传递。
   - *不适用条件*：严禁全部使用 `map[string]interface{}` 替代，会丧失静态编译检查且必须频繁进行类型断言。
5. **错误机械替换反例**：
   ```go
   // 错误：在 Go 中大量使用 map[string]any，类型断言失败引发运行时 panic
   m := map[string]any{"id": 1}
   id := m["id"].(string) // panic: interface conversion: any is int, not string
   // 正确：定义明确结构体
   type Record struct { ID int }
   ```
6. **信息不足或实现相关时的处理**：若源数据来自未知外部 JSON，结合 `json.Unmarshal` 到结构体进行验证。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Struct_types](https://go.dev/ref/spec)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

### 规则 PS-GO-02：PowerShell 错误流重定向向 Go 显式 error 与 stderr 隔离映射
1. **源码触发条件**：PowerShell 源码中使用 `2>&1` 将错误流合并到标准输出，或判断 `$?`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables), [MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)）；目标语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec)）。
3. **原可观察行为**：PS 将错误记录混合进管道输出流。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Go 语言中严格区分数据返回与错误流！函数返回 `(Data, error)`；CLI 标准输出与标准错误分别写入 `os.Stdout` 和 `os.Stderr`。
   - *不适用条件*：严禁将普通业务错误信息直接格式化打印到标准输出而返回 `nil` error。
5. **错误机械替换反例**：
   ```go
   // 错误：将错误信息打印至 stdout 并返回 nil
   func Process() error {
       fmt.Println("Error: something failed")
       return nil // 调用方误以为成功！
   }
   // 正确：返回 error
   func Process() error {
       return errors.New("something failed")
   }
   ```
6. **信息不足或实现相关时的处理**：若原脚本调用了原生可执行程序并重定向输出，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Errors](https://go.dev/ref/spec)；[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

### 规则 PS-GO-03：PowerShell Start-ThreadJob 向 Go Goroutine 轻量并发与 WaitGroup 映射
1. **源码触发条件**：PowerShell 源码中使用 `Start-ThreadJob` 启动后台任务。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)）；目标语言 Go 1.27（[GO-SPEC #Go_statements](https://go.dev/ref/spec)）。
3. **原可观察行为**：在后台 Runspace 线程池中并发执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 `go worker()`，主线程使用 `sync.WaitGroup` 等待全部任务退出。
   - *不适用条件*：严禁在启动 Goroutine 时捕获循环迭代变量（Go 1.22 虽修正循环变量作用域，但保持显式传参是最佳防错实践）；共享数据必须同步。
5. **错误机械替换反例**：
   ```go
   // 错误：启动后台 Goroutine 未做同步等待，主函数提前退出导致后台任务被杀死
   func main() {
       go doBackground()
   } // main 退出，所有 Goroutine 立即终止！
   // 正确：使用 sync.WaitGroup
   func main() {
       var wg sync.WaitGroup
       wg.Add(1)
       go func() { defer wg.Done(); doBackground() }()
       wg.Wait()
   }
   ```
6. **信息不足或实现相关时的处理**：若需获取后台任务返回值，结合 Channel 传递。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Go_statements](https://go.dev/ref/spec)；[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)。

### 规则 PS-GO-04：PowerShell WMI/`Invoke-WmiMethod` 返回码与属性存在性向 Go error 值与类型断言映射
1. **源码触发条件**：源码调用 WMI 或同类返回“结果对象 + 返回码”的 .NET API，并检查其属性，例如 `$Result = Invoke-WmiMethod @WmiMethodArgs -Class 'StdRegProv' -Name 'CreateKey' -ArgumentList $Hive, $RegistryKeyPath` 后接 `if ($Result.ReturnValue -ne 0) { throw ... }`，以及 `$Result = ... -Name 'CheckAccess' ...` 后接 `if (-not $Result.bGranted)`、`$PowerShellPath = $Result.sValue`、`if (($Result.ReturnValue -eq 0) -and ($Result.sValue))`；还包括 `$Hive = 2147483650` 这类超出 32 位有符号范围的句柄常量与 `$RequiredPermissions` 的 `-bor` 组合。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-ERROR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）；目标语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec), [GO-PKG-FMT](https://pkg.go.dev/fmt)）。
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
   // 正确：双返回断言 + error 分支
   v, ok := res["sValue"].(string)
   if !ok { return fmt.Errorf("CreateKey failed: rc=%#x", res["ReturnValue"]) }
   _ = v
   ```
6. **信息不足或实现相关时的处理**：具体方法的返回码取值集合、属性名与是否可能缺失、以及返回码字段的符号宽度，都必须从目标 API 文档或调用方契约确认；确认不了就停下标注，不要假定“非 0 且非空即成功”或反推一个码表。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Errors](https://go.dev/ref/spec)；[GO-PKG-FMT](https://pkg.go.dev/fmt)。

### 规则 PS-GO-05：PowerShell `.Count`/`$null`/空集合判定向 Go `len`/`nil` 与 map 存在性映射
1. **源码触发条件**：源码对可能为空的取值做计数或存在性判定，例如 `if (($Result.ReturnValue -eq 0) -and ($Result.sValue))`、`[byte[]]$Data = @()` 之后 `if($Data.Length -eq 0){Start-Sleep -Milliseconds 100}` 与 `if($Data -ne $null){...}`、`if(($i -ne $null) -and (($r -ne "") -or ($e -ne "")))`、`if($Socket -eq $null){break}`、`if (($attr.Contains('|')))` 前后对集合/字符串的空值判定、`$null = $hostList.Add($iHostPart1)`、`Get-Random -Count 10` 返回单元素时的标量退化。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays), [MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)）；目标语言 Go 1.27（[GO-SPEC #Slice_types](https://go.dev/ref/spec), [GO-SPEC #Index_expressions](https://go.dev/ref/spec)）。
3. **原可观察行为**：PS 里 `$null`、空数组、空字符串与 0 在布尔化时都为假，但 `.Count`/`.Length` 只对已存在的集合/字符串有意义，对 `$null` 读取长度会得到 `$null`（不抛错）并再次布尔化为假；`$Data.Length -eq 0` 与 `$Data -ne $null` 是两个不同判定，前者对空数组为真、后者对空数组也为真；`@()` 与“未赋值”在源里常常承载不同意图但表现接近；单元素数组在管道中还会退化为标量，`.count` 随之变为 `1` 或不存在。
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
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Slice_types](https://go.dev/ref/spec)；[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)。

### 规则 PS-GO-06：PowerShell 字符串与字节/UTF-16/Base64 边界向 Go `string`/`[]byte` 显式编码映射
1. **源码触发条件**：源码在字符串与字节序列之间转换并跨进程/网络边界，例如 `$EncodedPayload = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($Payload))`、`$Payload = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Result.sValue))`、`[byte[]]$Data = $Encoding.GetBytes($i)` 与 `$Encoding.GetString($Data)` 用 `New-Object System.Text.AsciiEncoding`、`$CSVEntry` 以 `Out-File -Encoding unicode` 追加写盘、`[byte[]]$bytes = 0..65535|%{0}` 与 `$FileStream.Read($MZHeader,0,2)`、`[System.BitConverter]::GetBytes(...)`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 Go 1.27（[GO-SPEC #String_types](https://go.dev/ref/spec), [GO-PKG-UNICODE-UTF16](https://pkg.go.dev/unicode/utf16), [GO-PKG-ENCODING-BASE64](https://pkg.go.dev/encoding/base64)）。
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
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #String_types](https://go.dev/ref/spec)；[GO-PKG-UNICODE-UTF16](https://pkg.go.dev/unicode/utf16)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
