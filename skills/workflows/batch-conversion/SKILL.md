---
name: batch-conversion
description: Use when one submission contains multiple code conversion tasks. Defines freezing, queueing, persistence/resume, bounded repairs, evidence reconciliation, and rollup without replacing the single-task workflow or establishing batch evaluation capability.
---

# 批量转换工作流

一次提交多项任务时加载；项目交付基线为单批不少于 40 项、允许排队的自动逐项评测，不要求 40 路并发。小批次也可使用本流程，不为凑数复制任务。本页只约束批次编排，不索引历史测试批次/数据集，不证明能力已验收。

## 1. 准入与冻结

单项转换知识由[根入口](../../../SKILL.md)选择，长文件另读[长文件流程](../long-file-conversion/SKILL.md)；阶段/自修/分流复用[闭环](../../../references/workflow/conversion-evaluation-loop.md)，产物和字段复用[交付契约](../../../references/framework/delivery-handoff-contract.md)。安全以[红线](../../../references/framework/safety-boundary.md)为准，只有使用对应评估渠道才读[Controller 适配](../../../references/adapter/controller/remote-controller-adapter.md)。

批次冻结稳定 batchId、逐项 taskId/方向/契约路径/源快照哈希、任务数量、两侧 OS/架构/工具链、实际 runner/同台异台策略、模型/知识快照、证据义务、授权与隔离、并发/超时/恢复条件。身份至少由 batchId+taskId 唯一定位，不因重排改变。

- 每项已有可读取源码及冻结契约；无源、占位、未知关键边界的项不能冒充已冻结。
- 一项只计一个语言方向；同源可转多目标，不把同源冒充多种源语言。
- 有源码是必要条件，不免除快照、工具链、实际入口与隔离核对；许可正文/上游 commit/URL 不作测试冻结校验，对外分发另核。
- 无 main/工程外壳时按契约补中性入口/最小工程并冻结；不补造缺失框架/业务实现，不把依赖缺失当作目标转换失败。
- 已有批次运行授权可复用，但每项的网络、数据、进程范围仍要核对；READY/快照不是隔离证明。

批次记录不改写原契约。更换任务集合、模型、工具链、方向或 oracle 属新条件，另冻批次/变体并记录关联；环境恢复的原条件重提不计新任务。

## 2. 队列与用量

默认串行 1 路；显式要求并发时冻结上限、互斥记录与模型/评估两类资源限制，不把排队深度当并发能力。单项自修与评估后 repair 默认各两次，允许任务预先冻结其他有限预算；reviewN 不等于修复次数。单项墙钟、批次时限和轮询间隔按契约记录。

当前工作区不另设批次请求/token/费用派发预算；这是调度约定，不是无限循环许可。每次实际请求含失败/截断/重试均记实际用量；reasoning 若已包含在 completion/total 中不重复累加。核对按**请求/响应身份**，不能仅因响应内容哈希相同就抹掉两次真实计费请求。记录累计消耗与限流/时限事实，不偷偷换模型。

## 3. 单项推进

逐项加载适用知识→配置模型生成→完整性检查→自审/有限自修→运行安全核对→按已有授权和冻结评估契约提交→取真实证据→分层报告/终态。文本-only 任务不因此执行动态步骤；运行安全阻断也不自动把自修预算改为零。

确认可定位转换问题未解时保留部分交付/SELF_REVIEW_UNRESOLVED，不标预检通过；预算耗尽本身不等于编译失败。安全门槛未满足记 RUN_SAFETY_NOT_READY 并继续其他项。驱动须实际观察应验证的程序行为，不能用空跑、固定输出或 stdoutLen 摘要冒充原始字节/oracle。

## 4. 持久化与恢复

记录落于该任务指定的输出区，不要求常驻测试数据目录。最小语义集合可用 `batch.json`、`items/<task-id>.json`、追加 `events.jsonl` 与 `summary.md`，或同等可追溯格式：冻结输入、阶段/版本/哈希、请求身份与用量、提交回执、诊断/evidence 路径、终态/原因。

1. 恢复先读冻结清单、单项状态和事件，核对任务身份、已完成/进行中/未开始及记录差异。
2. 已提交未收尾的项按已保存 jobId 查询，不直接重投；提交可能已接收但回执丢失时先核查，无法证明未接收则暂停该项。
3. 已生成未提交从最近完整阶段继续，不重复成功模型请求；环境故障恢复后保留原契约/capsule 重提。
4. 提交前持久化待提交身份/capsule 哈希，接收后立即存 jobId；重复执行须有明确原因，终态前不得无声离队。

### 4.1 结论与事件对账

关闭前对**全部 verdict**的自审结论及事件核对，不只 REPAIR 子集。结论本体 `self-review-N.json` 与请求/响应元数据、失败 attempt、追加裁决分开；按 batchId/taskId/reviewN 或实际声明的同等唯一身份求交集、双向差集，并分列重复事件、重复文件、解析错误和无法映射身份。

事件有而文件无是缺档；文件有而事件无是未登记，不能净额抵消。移出、未落盘、失败尝试各有具体记录，不默认归因为合法移出；无事件源的历史文件单列不可对账，不计零缺档。未知 verdict 不冒充 NO-REPAIR，缺失 origin 不猜填。

对账不足不能将该批次标为 `CLOSED` 或记录完整；以“未决/部分收尾”报告差异并继续不受影响的其他项，不能把缺档补成无问题。自审完整性不证明内容正确，原始记录不为对账而改写。

## 5. 状态与结论分列

| 状态/诊断 | 条件 |
|---|---|
| NOT_STARTED | 本项尚未开展 |
| 准备缺口 | 源/依赖/工具链/输入/oracle 未齐，写具体待补项 |
| SELF_REVIEW_UNRESOLVED | 有确认可定位转换问题未解，不能当独立 compiler FAIL |
| RUN_SAFETY_NOT_READY | 实际入口/隔离超过已确认授权边界，暂不提交 |
| BLOCKED_ENV | 实际 Controller/runner/工具链/清理故障有诊断 |
| FAILED_CODE | 指定目标版本有代码相关 build/运行失败证据，按阶段注明 |
| FAILED_BEHAVIOR | 实际观察与冻结 oracle 不符，注明覆盖范围 |
| DONE | 已完成该项契约要求的证据收集和交付，不自动等于代码/行为 PASS |

source/target build、execution、comparison、环境和安全结论仍分别填写；缺独立证据为 UNVERIFIED。源基线失败不回填目标失败；综合 verdict 不覆盖实际 build；compiler 处理源码前的权限/缓存初始化故障先归因环境，不让模型改代码绕过。

## 6. 收尾

逐项清单/终态及事件对账完成后才关闭批次；不得有无声丢失或未解释的重复执行。汇总调度完成度、请求/用量、编译、oracle/行为、安全、方向/OS/战术实际覆盖与未决项，不合成单一“转换成功率”。一次提交后自动逐项评测是否完成需实际记录证明，队列 CLOSED/40 条记录或大量未评估阻断不能满足该能力验收。

原始证据在执行和验收期间保留，收尾后保留/移交/清理由任务约定决定；数据可不永久保留，但不得删除尚需恢复的记录或在证据不可得时继续宣称可复核 PASS。Skill 不存测试 case/batch 索引，也不因某次试验未保存就无法应用规则。
