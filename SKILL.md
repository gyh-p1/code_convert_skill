---
name: code-convert-skill
description: Use for code conversion with an existing language direction. Routes language, direction, scene, system and workflow knowledge, then applies manual per-item gates and layered delivery without claiming unverified coverage.
metadata:
  short-description: Agent-facing code conversion knowledge Skill
---

# Code Convert Skill

本项目提供 Agent 使用的 Markdown 转换知识，不是独立转换运行时。Agent 画像、选知识、手工调度根 .env 配置模型、静态审阅、提交与取证；目标代码及修订来自配置模型。执行约束见 [AGENTS.md](AGENTS.md)，红线只以[安全边界](references/framework/safety-boundary.md)为准；本机只读写文本，不承载或触发源码/目标/构建运行。

**知识按离线消费**：读取本仓库正文与本地参考，不依赖访问官方网页或下载资料。来源名称/版本只用于追溯；必要语义缺失或准确版本无法确定时，记录知识缺口，不要求联网补全后才能使用其余适用规则。维护规则见[Skill 编写规范 §5.1](docs/Skill编写规范.md#51-本地引用与网页资料)；知识读取不授权外部联网或执行。

片段以声明上下文的语法为范围，只引用用户或获批平台已提供的精确中性上下文并记录来源/版本；缺件待准备，不由 Agent/模型新造桩、入口或依赖。单文件保持约定可观察行为；长单文件加载专用工作流。700 个 LF 归一化物理源代码行是计划上限，长文件流程与全部方向尚无全面效果验证，不能据知识页数量宣称达标。

## 必经执行链与契约

```text
冻结 → 分类(ALLOWED) → 源侧预检（构建 + 适用运行基线）→ 生成 → 自审
  → 评估就绪核对（安全 + 驱动 + oracle）→ 提交 → 取证 → 先归因再分层报告
  → 交付完整性/终态门禁（记 DONE/PARTIAL 前）
```

1. 每项先冻结，再取得 admissionStatus=ALLOWED 且 blockingReason=null，才能预检、正式模型生成或提交；不主观改判，不以文本交付绕过分类。
2. 源侧预检先取得 build.status=completed 且 exitCode=0；需行为评估时还须在获批隔离环境按冻结条件运行源，取得有效基线后才能生成。合法源驱动、观察目标、终止/清理及文本/仅编译例外见[评估准备 §1.1](references/framework/evaluation-readiness-contract.md#11-生成前源侧预检)。候选 sourceOs 来自源码事实，是否可构建只由真实编译器诊断定案；不设头文件探针。源平台/依赖/运行基线缺口不消耗转换模型调用、不算目标转换失败。
3. 提交前核安全/独立授权/逐例隔离、合法来源驱动四要素（启动→到达被观察状态→采集→终止）、两侧对称及 oracle 适用状态。ALLOWED、READY、clean、快照均不替代这些条件。
4. 开始处理该项就读取[统一收尾入口](references/framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)；正常结束、任何提前失败/阻断及暂停都必须走它。每项写 result.md 并逐件核实际适用产物、版本/内容/指针，将清单及核对结果留在报告，缺应有件不得记终态。未发生 job 不伪造；未知提交/活动或未确认清理的 job 保持 WAITING，即使已有暂停报告也不例外。DONE 可包含真实失败，PARTIAL 与 matched/mismatched 分开。

| 必读真源 | 负责什么 | 何时消费 |
|---|---|---|
| [任务状态契约](references/framework/task-state-contract.md) | 身份、冻结、版本关联/复用、接入去向、phase/lifecycle 与变体 | 正式任务冻结前及恢复/收尾 |
| [分类准入](references/workflow/classifier-agent-gate.md) | 分类输入、ALLOWED、重新分类与精确身份 | 源预检前及每次提交/重提 |
| [构建前提](references/workflow/build-prerequisites.md) | 冻结构建条件及真实源诊断分流 | 冻结前、源预检与目标评估 |
| [单项闭环](references/workflow/conversion-evaluation-loop.md) | 生成、自审、有限修复、取证分流 | 每项正式模型转换 |
| [评估准备契约](references/framework/evaluation-readiness-contract.md) | 源预检适用运行基线、驱动来源、四要素、oracle、仅编译、观察采信 | 冻结评估计划、源预检前、生成前及双侧提交/证据判读 |
| [交付契约](references/framework/delivery-handoff-contract.md) | 统一收尾入口、全去向 result.md、适用件核对、目录及移交清单 | 开始处理每项时必读；结束/失败/阻断/暂停前再次核对 |
| [安全边界](references/framework/safety-boundary.md) | 本机/同机/VM、网络和数据红线 | 全程 |

[行为指导](references/workflow/behavior-preservation-contract.md)用于单文件目标/允许差异说明，不自设裁决标准；其旧门禁章节仅转引评估准备契约。[Controller 适配](references/adapter/controller/remote-controller-adapter.md)只在使用该渠道时加载，维护外部字段与命令；它和开发阶段文档不产生执行授权。

## 选择适用知识

先按源码事实画像再选知识，不由 ATT&CK 标签反推行为。[知识总索引](references/README.md)说明各层消费者与边界。

**语言事实**：每次加载源、目标两页，由[七语言共性语义索引](skills/references/seven-language-common-semantics.md)导航。基线为 C11、C++17、C# 12/.NET 8、CPython 3.12、Go 1.27、PowerShell 7.6、Ruby 3.4；实际工具链仍须证据核验。

**语言方向（42 个）**：每项选择一个源→目标方向。方向只维护映射，语言内事实不在 42 页重复。

| 源语言 | 目标语言方向 Skill |
|---|---|
| **C** | [C → C++](skills/directions/c-to-cpp/SKILL.md) ｜ [C → C#](skills/directions/c-to-csharp/SKILL.md) ｜ [C → Python](skills/directions/c-to-python/SKILL.md) ｜ [C → Go](skills/directions/c-to-go/SKILL.md) ｜ [C → PowerShell](skills/directions/c-to-powershell/SKILL.md) ｜ [C → Ruby](skills/directions/c-to-ruby/SKILL.md) |
| **C++** | [C++ → C](skills/directions/cpp-to-c/SKILL.md) ｜ [C++ → C#](skills/directions/cpp-to-csharp/SKILL.md) ｜ [C++ → Python](skills/directions/cpp-to-python/SKILL.md) ｜ [C++ → Go](skills/directions/cpp-to-go/SKILL.md) ｜ [C++ → PowerShell](skills/directions/cpp-to-powershell/SKILL.md) ｜ [C++ → Ruby](skills/directions/cpp-to-ruby/SKILL.md) |
| **C#** | [C# → C](skills/directions/csharp-to-c/SKILL.md) ｜ [C# → C++](skills/directions/csharp-to-cpp/SKILL.md) ｜ [C# → Python](skills/directions/csharp-to-python/SKILL.md) ｜ [C# → Go](skills/directions/csharp-to-go/SKILL.md) ｜ [C# → PowerShell](skills/directions/csharp-to-powershell/SKILL.md) ｜ [C# → Ruby](skills/directions/csharp-to-ruby/SKILL.md) |
| **Python** | [Python → C](skills/directions/python-to-c/SKILL.md) ｜ [Python → C++](skills/directions/python-to-cpp/SKILL.md) ｜ [Python → C#](skills/directions/python-to-csharp/SKILL.md) ｜ [Python → Go](skills/directions/python-to-go/SKILL.md) ｜ [Python → PowerShell](skills/directions/python-to-powershell/SKILL.md) ｜ [Python → Ruby](skills/directions/python-to-ruby/SKILL.md) |
| **Go** | [Go → C](skills/directions/go-to-c/SKILL.md) ｜ [Go → C++](skills/directions/go-to-cpp/SKILL.md) ｜ [Go → C#](skills/directions/go-to-csharp/SKILL.md) ｜ [Go → Python](skills/directions/go-to-python/SKILL.md) ｜ [Go → PowerShell](skills/directions/go-to-powershell/SKILL.md) ｜ [Go → Ruby](skills/directions/go-to-ruby/SKILL.md) |
| **PowerShell** | [PowerShell → C](skills/directions/powershell-to-c/SKILL.md) ｜ [PowerShell → C++](skills/directions/powershell-to-cpp/SKILL.md) ｜ [PowerShell → C#](skills/directions/powershell-to-csharp/SKILL.md) ｜ [PowerShell → Python](skills/directions/powershell-to-python/SKILL.md) ｜ [PowerShell → Go](skills/directions/powershell-to-go/SKILL.md) ｜ [PowerShell → Ruby](skills/directions/powershell-to-ruby/SKILL.md) |
| **Ruby** | [Ruby → C](skills/directions/ruby-to-c/SKILL.md) ｜ [Ruby → C++](skills/directions/ruby-to-cpp/SKILL.md) ｜ [Ruby → C#](skills/directions/ruby-to-csharp/SKILL.md) ｜ [Ruby → Python](skills/directions/ruby-to-python/SKILL.md) ｜ [Ruby → PowerShell](skills/directions/ruby-to-powershell/SKILL.md) ｜ [Ruby → Go](skills/directions/ruby-to-go/SKILL.md) |

**场景（按行为多选）**：[网络 I/O](skills/scenes/network-io/SKILL.md)、[文件 I/O](skills/scenes/file-io/SKILL.md)、[进程执行](skills/scenes/process-execution/SKILL.md)、[并发](skills/scenes/concurrency/SKILL.md)。场景维护跨语言行为义务，不承载普通单线程控制流或单一语言 API 改写表。

**系统（按实际 API/子系统多选）**：[POSIX ↔ Winsock](skills/systems/posix-winsock/SKILL.md)、[文件路径](skills/systems/posix-windows-filesystem/SKILL.md)、[进程创建/身份权限](skills/systems/posix-windows-process-identity/SKILL.md)、[线程](skills/systems/posix-windows-threads/SKILL.md)、[Windows 注册表/服务](skills/systems/windows-registry-service-subsystem/SKILL.md)。同 OS 的专有子系统也适用；双向标题不证明全面映射或验证。macOS 当前只含文件位置约定；PE、ptrace/seccomp、Keychain/launchd/CoreFoundation 无对应系统 Skill。

**工作流**：[长单文件](skills/workflows/long-file-conversion/SKILL.md)按复杂度/长度加载；[批量](skills/workflows/batch-conversion/SKILL.md)按任务集合加载，两者可同时使用。批量只手工串行，整批一个 batchId，每新增 40 项 DONE+PARTIAL 增量对账并带入遗留项，缺档立即停新增转换，关闭前终局核对。

[ATT&CK 战术索引](skills/attack-tactic-index/SKILL.md)仅核对标签与定位知识，不生成战术规则，不参与授权；无证据记 none。HTTP/socket/文件 API 本身不构成战术。

## 按以下顺序执行

以下是知识选择和推进步骤，不能替代上方门禁链。

1. **确认边界并逐项冻结**：读任务状态、安全、分类、构建前提及交付契约 §1.1，确定本项报告落点；记录版本、模式、方向、候选源分支、依赖、模型、知识、授权、驱动合法来源及输入/oracle 适用状态；按[任务状态 §2.1](references/framework/task-state-contract.md#21-版本关联与复用边界)关联实际请求、原响应/组装稿、自审、job 和最终交付。变更冻结条件另记变体，不以当前知识回填历史请求。
2. **静态画像**：盘入口、条件编译、API、状态、所有权、输入输出和副作用；参数计数/下标/消费范围、文本或字节单位、固定常量、控制流出口、进程替换/环境、枚举消费者、键或行输入、空白谓词与临时目录选择按实际使用点定位。引用符号/位置，未知标未知，不执行样本。
3. **形成标签**：语言方向、实际场景、系统与工作流按证据标；ATT&CK 单独核对，不由标签决定转换。
4. **加载知识**：必读两语言页与方向，按[共性索引的易错语义导航](skills/references/seven-language-common-semantics.md#易错语义导航)将画像中的参数、字节/换行、固定常量、标签/作用域、文件失败、进程/环境、枚举、键输入、空白及临时目录对应到适用正文；将实际适用正文交给配置模型，不只列规则名。枚举与键输入不依赖进程/并发场景；实际 fork/exec 即使同 OS 也加载进程系统页的适用事实，不套跨 OS 表。按触发读场景、系统、长文件/批量。缺映射记探索假设，不以相似 Skill 冒充覆盖。方向/场景/系统不替代门禁或授权。
5. **调度配置模型及适用评估**：先分类 ALLOWED，再按评估准备 §1.1 完成隔离源预检（build completed/0；需行为评估时还取得冻结条件下的有效运行基线），然后生成、自审和有限修复。源基线缺口先停生成；可观察但缺合法入口待准备，真正无安全入口才仅编译 PARTIAL/功能 UNVERIFIED。文本/片段不适用运行须记理由。驱动不得由 Agent 新写或委托模型生成。双侧提交前重新核评估准备；oracle 无法冻结时停止受影响阶段，按已达阶段交付，不假 matched。取得终态原始证据，按[评估准备 §4–5](references/framework/evaluation-readiness-contract.md#5-原始观察采信与归因)核冻结路径与实际观察：非空输出、相同 usage/驱动标记或 coverage 满额不单独证明有效；文件义务取真实文件证据。先归因再报告/修复。
6. **统一收尾或暂停**：前述任一步骤停止都跳转[交付契约 §1.1](references/framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)，成功/失败/非可转换/WAITING 均写 result.md。逐件回读适用产物，记录已取得/缺失/不适用、路径/版本、原因与核对结果；交付、编译、功能及安全分别报告，无证据 UNVERIFIED。缺应有件不得终态；未知提交/活动或未确认清理保持 WAITING，暂停报告不等于已收尾。批次逐项核对，40 项与终局对账另做；带遗留及真实补登依据，按同快照汇总，不用总 verdict 或条数证明成功。

纯文档审阅/架构优化不属于代码转换，不触发分类、模型转换、构建或运行。明确文本交付不触发后续行为 job，但正式目标代码生成仍须生成前门禁。无对应知识的探索转换保留假设、差异和未验证范围。

自审裸 JSON 与格式恢复、请求/修复计数见单项闭环 §2/§4，保留原文且不追加无限审阅。恢复时先核源基线适用性及未知提交；批次 40 项阈值按此前未计入的唯一终态 taskId，PARTIAL 恢复、复审和重提不重复计项，统计单位与快照按批量工作流 §4.1/§6。

## 本工作区的模型调度约定

- 使用根 .env 的 CODE_TRANSLATOR_BASE_URL、CODE_TRANSLATOR_MODEL、CODE_TRANSLATOR_TEMPERATURE，OPENAI_API_KEY 仅作 bearer 凭证；不将 .env 或密钥发送/写入提示、日志、清单与产物。
- 首次请求包含当前只读源快照、冻结契约、实际适用知识正文和安全义务；不以标题/路径替代内容，不引用其他 run 的目标。修订提供同 run 父版本与定位反馈。
- 目标及修订必须来自配置模型；Agent 仅机械应用其确定性补丁并核对父版本、保存来源，不在模型失败时自主代写。
- 保存完整脱敏请求/原始响应的关联记录、实际模型名、状态、参数、token、输入/输出哈希及失败 attempt。模型完成不是编译或行为通过。
- 请求不发送 max_tokens；截断先按闭环响应完整性/分块协议处理，仍计用量，不据截断擅自换模型。配置缺失、请求失败或不完整时如实阻断。
- 全程用原生工具手工单项操作，不写可复用或临时辅助脚本。唯一许可常驻脚本是登记钉 SHA 的分类器，且仅按准入页在获准外部临时目录调用。
