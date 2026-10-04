---
name: go-to-powershell
description: Use when converting Go source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → PowerShell 语言转换规则

> **适用基线**：Go 1.27 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/go-to-powershell/README.md)；候选、冻结任务与第三方回传须分层记录。
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
