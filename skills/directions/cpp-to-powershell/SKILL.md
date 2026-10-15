---
name: cpp-to-powershell
description: Use when converting C++ source to PowerShell; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → PowerShell 语言转换规则

> **适用基线**：ISO C++17 → PowerShell 7.6。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C++](../../references/languages/cpp.md)与[目标语言 PowerShell](../../references/languages/powershell.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 C++ → PowerShell 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-PS-01：C++ 格式化文本输出须保持源通道与格式
1. **源码触发条件**：C++ 源码中遍历结构体列表并通过 `std::cout` 格式化打印制表符分隔文本。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 PowerShell 7.6；冻结宿主、输出通道、编码、locale 和换行义务。通道事实见[PowerShell 语言页 §八](../../references/languages/powershell.md#八宿主输出)。
3. **原可观察行为**：源向 stdout 输出按约定字段、顺序、分隔符与换行组织的文本；源内部结构体不等于外部对象管道接口。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按源格式显式构造文本，使用符合冻结宿主/通道的输出 API；例如 .NET Console 写文本时另核编码与换行，不能以屏幕显示相似证明原始字节相同。
   - *不适用条件*：任务未允许改变输出接口时，不把源文本改成 `[PSCustomObject]` 或依赖默认表格格式化。只有调用方明确要求对象接口且已冻结该变化时才对象化；`Write-Host` 的宿主/information 通道也不能直接当作源 stdout。
5. **错误机械替换反例**：
   ```powershell
   # 错误：源为 id + TAB + name + LF；对象格式化改变外部输出
   [PSCustomObject]@{ Id = $id; Name = $name } | Out-String
   # 候选：显式保持上述文本格式；编码/数值格式仍按冻结契约核对
   [Console]::Write("{0}`t{1}`n", $id, $name)
   ```
6. **信息不足或实现相关时的处理**：未知编码、数值/日期格式或宿主捕获方式时逐项标注待确认；`Out-String` 可带格式化空白、标题、尾部换行并受宽度影响，不是源字节保持保证。保持源行为优先于新增下游属性过滤方式。
7. **资料依据（名称/版本/章节）**：about_Pipelines；Out-String；Console.Write（实际 .NET 宿主版本按任务核验，API 示例不是宿主效果证据）。

### 规则 CPP-PS-02：C++ 异常分类捕获向 PowerShell 终止错误提升与 catch 分流映射
1. **源码触发条件**：C++ 源码中包含多个派生异常的 `catch (const SpecificException& e)`。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 PowerShell 7.6（MS-PS-ERROR）。
3. **原可观察行为**：根据抛出异常的运行时类型精准命中对应的 `catch` 块。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 PowerShell 中使用 `try { ... } catch [System.IO.IOException] { ... } catch { ... }` 精确捕获对应 .NET 异常类型。
   - *不适用条件*：必须注意 PowerShell `try/catch` 默认仅捕获终止错误；若调用的 Cmdlet 抛出非终止错误，必须显式附加 `-ErrorAction Stop` 才能被捕获。
5. **错误机械替换反例**：
   ```powershell
   # 错误：未配置 ErrorAction Stop，非终止错误跳过 catch 块继续向下执行
   try {
       Remove-Item -Path $file # 若文件不存在抛出非终止错误，直接跳过 catch！
   } catch {
       Write-Error "Clean failed"
   }
   # 正确：提升为终止错误
   try {
       Remove-Item -Path $file -ErrorAction Stop
   } catch {
       Write-Error "Clean failed: $_"
   }
   ```
6. **信息不足或实现相关时的处理**：若源异常为自定义非标准类，在 PS 中捕获基类 `[Exception]` 并检查消息。
7. **资料依据（名称/版本/章节）**：MS-PS-ERROR。

### 规则 CPP-PS-03：C++ 互斥锁与临界区向 PowerShell Monitor 同步包装映射
1. **源码触发条件**：C++ 源码中使用 `std::mutex` 保护多线程共享的全局状态。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 PowerShell 7.6（MS-PS-THREADJOB）。
3. **原可观察行为**：确保同一时刻仅一个线程进入临界区执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `[System.Threading.Monitor]::Enter($syncObj)` 与 `[System.Threading.Monitor]::Exit($syncObj)`，或使用 `[System.Collections.Concurrent]` 线程安全集合。
   - *不适用条件*：严禁在多 Runspace 并发下直接操作非同步哈希表，会导致数据损坏或死循环。
5. **错误机械替换反例**：
   ```powershell
   # 错误：未在 finally 块中释放锁导致死锁
   [System.Threading.Monitor]::Enter($lock)
   Do-Work # 若发生异常，$lock 永远不被释放，导致全进程死锁！
   [System.Threading.Monitor]::Exit($lock)
   # 正确：使用 try-finally 确保释放
   [System.Threading.Monitor]::Enter($lock)
   try { Do-Work } finally { [System.Threading.Monitor]::Exit($lock) }
   ```
6. **信息不足或实现相关时的处理**：若涉及跨进程同步，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **资料依据（名称/版本/章节）**：MS-PS-THREADJOB。

### 规则 CPP-PS-04：原始 argv 文本解析不得被强类型参数绑定提前终止

> **归属说明**：实参绑定的**共享事实**（位置/命名/默认值/缩写）归语言层，见 [C++ 语言页 §五](../../references/languages/cpp.md)、[PowerShell 语言页 §一](../../references/languages/powershell.md)。本规则**只写 C++→PowerShell 方向特有**的绑定差异。

1. **源码触发条件**：C++ 源码从 argv 接收文本并在函数体内解析、允许数字前缀或捕获解析失败后兜底；目标拟用 `param([int]...)`。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 PowerShell 7.6（about_Functions_Advanced_Parameters）。
3. **原可观察行为**：
   - `std::stoi` 可消费数字前缀，是否拒绝尾部字符取决于源码是否检查 pos；invalid/out-of-range 抛异常，源码可能捕获并继续。
   - `[int]` 参数转换发生在脚本体之前；绑定失败时函数体里的 catch/兜底没有执行机会。忽略输入差异会改变文件输出、stdout 和退出码。
4. **目标可选写法和不适用条件**：
   - *可选映射*：先承接原始文本，再显式重建源的空白/符号/数字前缀、范围、异常兜底与负值钳制。普通 `TryParse` 全串检查不能直接替代允许 `3abc` 的 stoi。
   - *不适用条件*：源明确严格全串校验并在无效输入时终止，且绑定错误的输出/退出码符合契约时，才可采用强类型绑定；不能仅因正常数字输入相同就认等价。
5. **错误机械替换反例**：
   ```powershell
   # 错误：源 try { stoi(argv[1]); } catch (...) { depth = 2; }
   # 在 "abc" 时继续；这里则在脚本体之前绑定失败
   param([Parameter(Position=0)][int]$Depth = 2)
   # 选择文本参数，具体解析必须另按源 stoi 行为重建
   param([Parameter(Position=0)][string]$DepthArg)
   ```
6. **信息不足或实现相关时的处理**：核对源码是否检查 pos、实际整数范围/locale 和异常分支；未知时标为待确认。源码不区分显式默认值时不引入新的业务分支。
7. **资料依据（名称/版本/章节）**：C++17 N4659 §21.3.5 stoi；about_Parameter_Binding。

### 规则 CPP-PS-05：C++ 语句标签不能残留为 PowerShell 命令

1. **触发/前提**：C++17 → PowerShell 7.6；源码含语句标签/goto。共享目标事实见 [PowerShell §九](../../references/languages/powershell.md#九普通控制流)。
2. **应保留行为**：标签的到达条件、跳转目的地、后续执行与清理顺序，合法目标循环标签与未知源引用分开。
3. **映射条件**：未引用的 C++ 标签确认只是同一语句的名称时可去掉；有引用时结构化重建，不能残留为 PS 命令，也不能直接改为 `:name` 就宣称支持源 goto。
4. **反例**：保留 `report_ready:` 导致调用不存在的命令；删标签却漏掉 goto 出口；删除目标合法的 `:outer while (...)` 改变嵌套退出。
5. **未知处理**：未定位全部引用与清理范围时记录待核；不为本规则反复自审、运行语法探测或新增驱动。
6. **官方依据**：C++17 N4659（stmt.label、stmt.jump）、about_Break。

### 规则 CPP-PS-06：文件流未抛错且继续的路径不能变成目标异常终止

1. **触发/前提**：C++17 → PowerShell 7.6；源码忽略文件流失败并继续。共享事实见 [C++ §五](../../references/languages/cpp.md#五异常错误退出码与可观察失败)、[PowerShell §五](../../references/languages/powershell.md#五异常错误退出码与可观察失败)；实际文件行为加载文件场景。
2. **应保留行为**：失败后是否继续、诊断通道、退出码、部分文件与清理顺序。
3. **映射条件**：先核源 API/重载、异常掩码及后续状态使用；确认源无异常且继续时，目标以状态或仅处理对应 I/O 失败重建。不能全局 Stop，也不能让对应 .NET I/O 异常逃逸。源本会抛错/失败退出时按 CPP-PS-02 保留捕获/传播。
4. **反例**：源打开失败仍输出既有提示，目标未经处理异常就提前终止；反过来宽泛 catch 所有异常、伪造写入成功。
5. **未知处理**：未检查返回值不等于不抛错；正常 fixture 不足以证明失败路径一致。缺定位/原证据时只登记待核，不修历史目标或改原 verdict。
6. **官方依据**：Microsoft basic_ios（异常掩码与状态）、about_Try_Catch_Finally。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
