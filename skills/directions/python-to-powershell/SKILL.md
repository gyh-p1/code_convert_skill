---
name: python-to-powershell
description: Use when converting Python source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → PowerShell 语言转换规则

> **适用基线**：CPython 3.12 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Python](../../references/languages/python.md)与[目标语言 PowerShell](../../references/languages/powershell.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/python-to-powershell/README.md)；候选、冻结任务与第三方回传须分层记录。
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
