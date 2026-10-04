---
name: powershell-to-go
description: Use when converting PowerShell source to Go; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → Go 语言转换规则

> **适用基线**：PowerShell 7.6 → Go 1.27。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/powershell-to-go/README.md)；候选、冻结任务与第三方回传须分层记录。
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
