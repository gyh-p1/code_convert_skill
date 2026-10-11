# 转换任务身份、冻结与状态契约

本页维护项目任务记录的语义，不新增 Controller schema。由[根入口](../../SKILL.md)、[单项闭环](../workflow/conversion-evaluation-loop.md)、批次工作流和交付契约消费。执行红线仍以[安全边界](safety-boundary.md)及 [AGENTS.md](../../AGENTS.md) 为准；状态不是执行授权或验证结论。

## 1. 身份与变体

- 原始材料用 intakeId/rawItemId；派生任务用 batchId+taskId 唯一定位，一个任务固定一个源→目标方向。caseId/路径是关联信息，不代替 taskId。
- 同一数据集的持续任务保持一个 batchId；新增材料分配新的 intakeId，追加原始去向和派生任务，已完成项不重编号。batch.json 保留集合版本/追加依据；已关闭批次追加前先记录重开与新范围，不把 ACTIVE 项静默放进 CLOSED。单项仍逐项冻结、立即推进，不批量冻结。
- 修改已冻结源码、方向、模型、知识正文快照、OS、工具链、输入/oracle 或比较条件时创建有父版本关联的变体/新 run，不覆盖原记录。新变体仍关联原批次；是否重新分类按[分类准入](../workflow/classifier-agent-gate.md)核对分类输入和条件，不能用新 run 重置既有问题的累计修复预算。只是补齐记录或恢复原冻结字节不改变这些条件，但须有原件对应依据。
- 源未变的目标代码 repair 在同一 run 内另存目标版本；环境恢复的原条件重提另记 attempt/job，不计新任务。

## 2. 冻结记录

正式转换在首次模型调用前逐项冻结。冻结不等于准入、可构建、评估就绪或已授权。记录字段按任务模式填写；不适用写明理由，未知事实写待准备，不伪填已核验。

| 组 | 内容 |
|---|---|
| 身份 | batchId/taskId/direction、caseId、casePath+caseSha256、源文件集合、sourcePath+sourceSha256 |
| 源/目标配置 | sourceOs/targetOs、候选 sourceOsBasis、架构/ABI、实际条件分支、语言标准、工具链/SDK、依赖及检查上下文 |
| 知识与模型 | selected skills（路径+哈希）、配置模型/温度、RAG 开关、不发送 max_tokens 的输出约定 |
| 构建与源基线 | 两侧 buildCommand/环境/工程输入；源预检适用运行条件与观察目标；真实构建诊断及适用运行/清理证据取得后追加引用，不倒填成冻结前已知 |
| 评估计划 | driver（形态、来源、argv/stdin、就绪条件、终止）、driverRationale、input/初始状态、oracle 是否适用及其来源/观察范围/比较策略 |
| 授权与环境 | 授权来源/范围/有效期、计划与已核验 runner/快照分开、实际网络/数据边界及清理条件；外部表单按适配页填写 |
| 恢复 | 原始/分类/冻结快照对应、父版本、有限修复预算、超时/轮询计划和待补项 |

片段的源侧预检只引用用户或获批平台已提供的精确中性声明上下文并记录来源/版本；缺合法上下文待准备，不由 Agent/模型新造桩、入口或依赖。无行为评估时不强迫链接或运行完整程序。明确文本交付不开展后续行为评估，driver/input/oracle 可写不适用；**正式模型转换仍先过分类 ALLOWED 和适用源侧预检**。需行为评估时，生成前须取得源可构建及冻结条件下有效运行基线，判据、合法源驱动与仅编译例外见[评估准备 §1.1](evaluation-readiness-contract.md#11-生成前源侧预检)。纯文档审阅不属于转换，不触发这些动态步骤。

需要动态评估时，驱动/输入/oracle 的适用状态和构建前提在冻结阶段确定；缺实际驱动、工具链或隔离证据不伪称就绪。无安全观察入口按[评估准备契约](evaluation-readiness-contract.md)仅编译；可安全观察但缺合法来源驱动时记准备缺口，不能为省事降级。

### 2.1 版本关联与复用边界

下列关系记录在既有冻结、模型元数据、provenance、decision 和 job 记录中；可用实际路径/已有身份表达，不要求新增文件或平台字段：

| 关系 | 必须能回读的对应内容 |
|---|---|
| 冻结 → 实际请求 | 本 run 的源范围/依赖、契约版本、所选本地知识正文及章节/快照、模型参数；分段注明实际注入范围。读取过文件或列过路径不等于已交给模型 |
| 请求 → 响应 → 目标 | 请求/attempt、实际返回模型、原响应、解码/取文件或机械补丁依据、父目标及新目标版本；HTTP 封装、解码正文和目标文件的哈希分别标明对象，不能互换 |
| 目标 → 自审/裁决 | 被审版本及范围、reviewN/attempt、原条目、追加裁决依据和仍未覆盖部分；不把旧稿审阅自动移到新稿 |
| 提交 → 证据 → 最终交付 | attempt/capsule、分类与授权引用、jobId、双侧实际输入/构建/运行/策略及原始证据、根级交付版本；“最新 job”不能代替版本对应 |

关联缺失只说明不可复核，不能据此补造请求正文、目标来源或 PASS。原条件重提仅在源集合、构建/运行条件、输入/初始状态、oracle/策略、环境及授权仍适用且无未决执行时成立；源预检证据复用按[评估准备 §1.2](evaluation-readiness-contract.md#12-源基线复用与失效)核对。冻结知识后来被修改时，已有 run 继续指向原快照；拿不到原正文就记缺口，不能以仓库当前页回填历史注入。

冻结说明的事实/表述有误时，对照精确源码、原请求和实际条件追加更正及其依据。仅注释更正不伪装成改变过输入或重新执行；如果更正会改变实际契约、允许差异或准备条件，则另记变体并重新核受影响门槛，原说明及原结果保留。

## 3. 接入去向

每个 rawItemId 的每个候选方向必须有一个当前去向，变化以追加记录保留历史。以下是封闭词表：

| 去向 | 含义 |
|---|---|
| FROZEN | 转换边界已记录；仍须逐项分类/源侧预检才能生成 |
| PREPARATION_GAP | 方向/平台/模式、快照或所需合法准备件不足，待补 |
| DUPLICATE | 同源同向同契约且非显式独立试验；指向复用任务 |
| EXCLUDED | 不在任务范围，记依据 |
| SOURCE_NOT_BUILDABLE | 源侧预检真实诊断确认源平台/接口不可构建，非转换失败 |
| SOURCE_DEPENDENCY_GAP | 源引用快照外真实依赖；快照内文件漏打包不属此项 |
| SAFETY_BLOCKED | 安全文本处理/交付也不允许；不外发凭证 |
| SKIPPED | 本机无法读取/校验源字节且未取得可复核快照；能读能校验的项不能用此去向 |

已冻结项的分类阻断保存原 admissionStatus/blockingReason，并用 lifecycle/pendingAction 记录等待或停止，不新增第二准入裁决。LIB_UNOBSERVABLE_COMPILE_ONLY 是已转换项的仅编译原因，不是接入去向。

## 4. 阶段、生命周期与验证结论

| 字段 | 语义 |
|---|---|
| phase | 最近有完整记录的单项闭环阶段；已分类/源侧预检是生成前条件，不把动作开始写成完成 |
| pendingAction | 当前进行或等待的动作，关联请求/attempt/job 身份 |
| lifecycle | NOT_STARTED / ACTIVE / WAITING / DONE / PARTIAL |
| 原因与恢复条件 | 分类阻断、准备缺口、SELF_REVIEW_UNRESOLVED、RUN_SAFETY_NOT_READY、BLOCKED_ENV（有真实环境诊断）、SUBMISSION_UNKNOWN、LIB_UNOBSERVABLE_COMPILE_ONLY、ORACLE_NOT_FREEZABLE 等；保留解除历史 |
| 验证结论 | 按精确版本分列 source/target build、execution、comparison、环境与安全；原平台 verdict 与本项目覆盖判断分列 |

DONE 表示契约所要求的工作、取证和交付已收尾，**可有真实失败**；PARTIAL 表示本轮已停止并完成适用的部分交付，仍缺工作/证据。两者都须先过[交付完整性门禁](delivery-handoff-contract.md#211-单文件任务的标准骨架2026-10-09-冻结按-docstestdataset-实测形制)，对应闭环 CLOSED。matched/mismatched 不决定 lifecycle，缺证据为 UNVERIFIED。

每个已处理项结束/暂停时按[统一收尾入口](delivery-handoff-contract.md#11-统一收尾入口与报告义务)保留 result.md 及实际产物核对，成功、失败、生成前阻断和非可转换去向均不豁免。WAITING 报告说明暂停与恢复条件，不表示 CLOSED；缺报告/核对记录不能记终态，报告存在也不能解除未决执行。

仅编译项固定 PARTIAL、功能 UNVERIFIED，编译据实。源不可构建/依赖缺口不回填目标 FAIL；非可转换去向按适用件收尾，不纳入转换失败。可能已接收但缺回执，或 job 仍活动/未确认清理时保持 WAITING，不能用 PARTIAL 绕过未决执行。恢复 PARTIAL 追加重入依据，从最近适用阶段继续且保留预算。
