# 转换交付与移交契约：收尾产物与 evaluator_manifest.json

本文件在开始处理单项任务时必读，每次结束或暂停该项前再次按 §1.1 核对；只维护适用产物、布局、报告和 evaluator_manifest.json 的字段来源。身份/冻结/状态见[任务状态契约](task-state-contract.md)，评估准备与观察采信见[评估准备契约](evaluation-readiness-contract.md)，批次节奏见批量工作流。本机不编译或运行；实际语法与行为结论只能来自获批隔离环境的精确版本证据。evaluator_manifest.json 是本仓库移交清单，Controller 的 capsule schema 只见适配页，二者不能等同。

它与转换本身的维度分开：语言方向/场景/系统方向 Skill 管映射与应保留行为，长单文件工作流管防偏移，本契约只管**收口与移交**，不重复它们的内容。

## 1. 何时适用

- 片段、单文件、长单文件任一模式的转换完成后都走本收尾；片段任务若无后续评测需求，根级可只交目标文件与 result.md，已发生过程记录仍按 §2.1 保留；evaluator_manifest.json 视消费方要求决定是否生成。
- 收尾包括正常完成与在某阶段停止的部分交付；不要求所有停止项先有目标或评估。阶段、停止原因和适用件分别记录，不代表已验证语法或行为。
- 进入编译或运行前逐项核对源码存在、工具链、代码行为与隔离环境；显式加载本契约不是执行授权。许可正文、版本号、上游 commit、仓库 URL 不作测试用例冻结或提交校验。

### 1.1 统一收尾入口与报告义务

从开始处理该项起，正常完成和任何提前停止都走同一收尾入口，包括分类阻断、源预检失败/缺基线、配置或生成失败、自审/修复停止、评估准备缺口、平台故障、仅编译、排除/重复/跳过及 WAITING 暂停。不能在某个分支写完停止原因后直接返回，不能等到批次每 40 项对账才补单项报告；尚未开始处理的清单候选不要求预建报告。纯文档审阅不属于这里的转换任务。

1. **写本项 result.md**：不论是否生成完整目标、不论成功/失败/阻断，都须有一份中文报告。沿用 §2.3 五栏目，写实际阶段/状态、原因、已有证据、未完成/不适用义务与恢复条件；无目标明确“未生成”，未开展维度写“未执行/UNVERIFIED”，不编造 target、job 或 PASS。报告不包含凭证、危险载荷或不必要的源码。
2. **逐件核对真实产物**：按 §2.1.1 的模式、已达阶段和停止原因列适用清单，人工读取实际文件并核内容符合形制、可复核、版本/指针相符；逐件记“已取得/缺失/不适用”、真实路径与理由。目录存在、文件名齐、空报告或占位文件均不算齐备；真实采集的空 stdout/stderr 等原件可为空，须有对应采集记录，不能与缺文件/占位混淆。有完整目标才要求完整 target，实际发生的模型/分类/预检/提交/原始证据不能因失败漏掉。
3. **保存核对结果再决定状态**：在 result.md 的“验证依据与覆盖范围”记录核对时间、适用清单及通过/未通过，缺件与责任/补件条件写“未决问题与下一步”；批次 item/event 引用本报告及核对记录，不复制成第二份证据。缺应有件不能记 DONE/PARTIAL/CLOSED；未知提交、活动或未确认清理的 job 保持 WAITING，已有报告不解除它们。

result.md 在该项约定的 run 输出根保存；尚无 run 目录时只创建合法约定的输出目录与报告，不为报告伪建冻结或评估阶段。非可转换去向同样交报告，但不要求目标或未发生的动态产物。WAITING 报告明确“暂停记录，尚未终态”；恢复后在同项报告更新当前速览并保留原停止说明/依据，不覆盖原始证据或裁决。报告自身未写出、无法回读或缺原因/核对记录时，收尾核对未完成，保持实际非终态并登记补件动作，不能宣布收尾。

这是 Markdown 对 Agent 的必经操作要求，不是自动执行的检查器。加载路径与人工核对记录支持静态可达性；只有实际任务记录能证明该次已遵守，不据文本宣称任意 Agent 一定执行。

Controller 的收尾字段与原件下载消费[当前协议适配 §4](../adapter/controller/platform-revision-adapter.md#4-平台收尾与原件取回)。closureBlocked/CLEANING 或清理/调用未知保持 WAITING，不能只按 jobStatus 终态标签收尾；closure 通过也不能免本契约的 result.md 与转换端适用件核对。历史 job 缺 closure 则按真实原件和逐项清理核对，不补造“完整性通过”。报告 kind/source-only/仅编译不同，按实际阶段核件，不强制无适用 comparison/target。

## 2. 固定产物集合与目录布局

一次转换 run 的输出落在任务契约指定的同一 run 目录。**run 根目录只放"最终交付物"**，过程产物按阶段归入子目录（见 2.2），使消费方一眼区分"当前交付稿 / 过程记录 / 评估证据"，不必在扁平目录里猜哪份是第几轮转换、哪份是评估证据。

### 2.1 run 根目录：最终交付物

| 产物 | 内容 | 备注 |
|---|---|---|
| `target.<ext>`（可多个） | **最终交付版本**的目标语言文件；是否编译通过由证据另判 | 多文件逐一列入 manifest `files[]`；历史版本进 `02-conversion/`，不在根目录堆叠 |
| `source-analysis.md`（长单文件） | 源/目标画像、证据化标签、ATT&CK 判断、Skill 选择、源码地图与未决项 | 为 Skill 选择及全文件核对提供可审阅依据；短片段可省 |
| `result.md` | 中文结果报告：先给结论速览，再解释转换过程、验证依据与未决问题 | 按 2.3 的固定骨架；模型预检不得充当语法结论，未收到第三方编译结果时标记 `UNVERIFIED` |
| `evaluator_manifest.json` | 移交清单：告知编译/运行环境文件位置、任务元数据、待批准状态 | 形状见第 4 节，临时适配；其中路径指针须指向本布局的实际落点 |
| `README.md`（可选） | run 概览与状态 | 说明 run 类型（探索/基线）、当前状态与阶段目录导航 |

短片段任务若无后续评测需求，根级可只产出 `target.<ext>` 与 `result.md`；正式模型生成已经发生的冻结、分类、适用源预检、模型请求/响应及自审等追溯件仍保留在实际记录位置，不以根级简化免除生成前门禁和证据。目录不必为空阶段预建。

### 2.1.1 单文件任务的标准骨架（2026-10-09 冻结，按 `docs/test/dataset/` 实测形制）

**每个用例的落点与完整骨架如下，后续转换一律照此产出**：

```text
<direction>/<case-id>/
├── case.md                        # 冻结契约（FROZEN 阶段写入）
├── source/<源文件>                 # 只读源快照，不随转换改写
└── output/<batchId>/
    ├── 01-frozen/
    │   ├── frozen-inputs.md       # 冻结输入，Markdown
    │   ├── classifier-input.json  # 分类器输入清单快照
    │   └── classification-1.json  # 分类结果（须 ALLOWED 才可提交）
    ├── 02-conversion/
    │   ├── target.gen.<ext>       # 首个完整模型稿
    │   ├── target.gen.model.json  # 该次调用元数据
    │   └── target.gen.raw.txt     # 模型原始响应
    ├── 03-self-review/
    │   ├── self-review-1.json
    │   └── self-review-1.model.json
    ├── 04-evaluation/
    │   ├── job-00-source-buildability/   # 分类后源预检：构建及适用运行基线
    │   └── job-01-dual-build/            # 双侧构建与行为比较
    │       ├── capsule.zip
    │       ├── comparison_manifest.json
    │       ├── input_profile.json
    │       ├── metadata.json
    │       ├── job-id.txt
    │       ├── source/  target/          # 该 job 暂存的源/目标树
    │       └── returned-evidence/
    │           ├── evaluation_report.json
    │           ├── evaluation_report.md
    │           ├── evidence-source.json
    │           ├── evidence-target.json
    │           ├── comparison.json
    │           └── controller.log
    ├── evaluator_manifest.json    # 移交清单，见第 4 节
    ├── result.md                  # 中文结果报告，见 2.3
    └── target.<ext>               # 最终交付版本（run 根级）
```

**关于"不多不少"的硬性约束**（本次实测反复踩到，逐一固化）：

| 规则 | 说明 |
|---|---|
| `01-frozen/` | 分类前已完成冻结的项即须有 frozen-inputs.md，并按[任务状态 §2.2](task-state-contract.md#22-冻结落盘门禁)写出且回读通过；不等生成或收尾才要求。已发生分类保留 classifier-input.json 与原分类结果；重分类另存递增编号并指明当前版本，不覆盖旧结果。不写 frozen-inputs.json；冻结前停止的项只要求实际适用件，不伪建冻结记录 |
| **提交前必须有当前适用的 `classification-<N>.json` 且 ALLOWED/null** | 首次通常为 classification-1.json；重分类引用实际新编号。每次进入评估准备/提交/重提核该结果与完整源集合、身份/条件对应；是否重分类只按[分类准入](../workflow/classifier-agent-gate.md)，不能因原编号有 ALLOWED 沿用失效结果 |
| `frozen-inputs.md` 必须记录授权与隔离 | 含授权来源、范围、有效期，源/目标 VM 与 runnerId、网络边界、清理条件；**不得只靠事后 evidence 的 `clean` 代替提交前记录** |
| 请求/响应追溯 | 不另堆 prompt.txt；在该轮 model.json 或其指向的不可变记录保存脱敏请求/原始响应与身份、哈希。哈希不能还原正文；raw.txt 是实际响应，不是请求替代品。自审原始响应也须保留，不能只保存解析结论 |
| 提交与状态记录 | 不另建重复 state.json；job-id.txt 记录已知 jobId，拒收/丢回执/传输诊断在该 job/attempt 的实际记录中保留。不得以没有 submission-response.json 为由丢弃未知提交证据；轮询中间快照不当作终态证据 |
| 已有完整交付稿时根级须有 `target.<ext>` | 等于所指最终完整版本；没有后续目标修订时才等于 target.gen。自修、评估后修复或有依据的组装恢复后指向实际新稿，不把不完整生成充作交付版 |
| 阶段目录按实际产生创建 | 未发生的阶段不建空目录 |
| `04-evaluation/` 下只有 `job-*` | 不建 `_probes`、`logs` 等旁支目录 |

**交付完整性自检（终态前门禁，2026-10-10 实测补入）**：把某项记为终态（`DONE`/`PARTIAL`）前，必须按 §1.1 逐件人工核对该项约定 run 输出及实际过程记录位置，确认**交付物按其去向齐备**，缺必备件即**不得**记终态。该核对同时是批次增量对账（[批量工作流 §4.1](../../skills/workflows/batch-conversion/SKILL.md)）的固定项，也在执行主干（[AGENTS.md](../../AGENTS.md) §3、根 [SKILL.md](../../SKILL.md) 第 6 步）作为收尾相位门禁出现。曾出现 20 项缺 `result.md` 的反例，故单列为门禁。

**门禁覆盖所有需收尾的条目，按模式、已达阶段与停止原因要求适用件**。完整评估的标准骨架不能倒用于尚未生成或提交的项；缺应有件不能记终态，未发生件不能伪造：

| 去向 | 必备交付物 | 不要求 |
|---|---|---|
| **已生成目标且完成适用评估** | 根级 target、result.md（含功能结论）、manifest（契约要求时）、冻结/分类、全部实际模型/自审/裁决与版本来源记录、每个实际 job 的回执及原始返回证据 | 不要求未发生的额外修复 job；仅编译不伪造 comparison |
| **已生成但评估前停止/明确文本交付** | 根级 target、result.md（功能 UNVERIFIED 及停止/不适用原因）、manifest（要求时）、冻结/分类/job-00、已发生模型与自审记录；明确未完成义务及恢复条件 | 未提交的 job-01；不能据此免除应做评估或把安全缺口写成功 |
| **生成尝试失败，无完整目标** | result.md（无目标、真实失败原因、已发生件核对、功能 UNVERIFIED）；冻结/分类/适用源预检、已发生请求/响应/失败 attempt | 不完整代码不能充当最终 target；不要求未发生自审/双侧 job |
| **非可转换去向**（`SOURCE_NOT_BUILDABLE`/`SOURCE_DEPENDENCY_GAP`/`PREPARATION_GAP`/`EXCLUDED`/`DUPLICATE`/`SAFETY_BLOCKED`/`SKIPPED`） | result.md（去向/原因、实际阶段与证据、适用件核对）；其余只要实际适用件：冻结/去向记录、已取得分类输入/结果、已发生预检 attempt/回执/原始证据。未发生不造 | 完整 target、未发生双侧 job、未开展维度的 PASS；result.md 不豁免 |
| **WAITING 暂停/未知提交/活动或未确认清理的 job** | result.md（暂停原因、当前已达阶段、已有/缺失件、接收/终止/清理待核及恢复条件）、全部实际发生记录与指针 | 不要求未发生件或未回传证据的伪文件；有报告也不得记终态 |

非可转换去向不要求 target，缺 target 不算缺档；result.md 是所有已处理项的报告义务，缺报告算交付缺档，不能写成目标转换失败。门禁核的是该去向该有的件是否齐备，报告义务不证明产出目标或功能通过。

LIB_UNOBSERVABLE_COMPILE_ONLY 是已转换项的仅编译原因，不是非可转换去向。实际完成仅编译提交的项须有 target/result、冻结/分类、真实双侧编译 job 证据，PARTIAL、功能 UNVERIFIED。因平台不支持仅编译而尚未提交的项按“评估前停止”行交付并写编译 UNVERIFIED，不能假称已完成仅编译取证。判据见[评估准备 §3](evaluation-readiness-contract.md#3-无安全可观察入口)。未知提交或仍活动/未确认清理的 job 保持 WAITING，不能靠适用件豁免记 PARTIAL。

### 2.1.2 批次索引骨架（2026-10-09 冻结，按 `docs/test/dataset/batch-01/` 实测形制）

**批次索引与单文件骨架是两层，不是一个**：批次索引记录"这批有哪几项、各自去向与终态"，落在数据集根的 `<batchId>/`，与方向目录**平级**；每项的转换产物仍落在 `<direction>/<case-id>/output/<batchId>/`（§2.1.1）。**禁止**把逐项状态文件再塞进批次根，也**禁止**把批次索引摊到每个 case 下——两层的落点不可互换。

**批次口径：一个数据集 = 一个批次。** `batchId` 取固定值（dataset-2 用 `batch`），**不再按固定条数切分多个批次**；后续新增条目并入同一批次，保留已完成项身份与证据。此规则维护集合身份，不证明队列或自动化能力已达标。单次不少于 40 项、无需人工逐项触发的业务目标仍未验收，现行手工逐项链路不能替代它；见[批量工作流](../../skills/workflows/batch-conversion/SKILL.md)及[业务基线](../../docs/项目业务文档和能力边界.md#交付目标冻结2026-09-29)。

```text
<dataset-root>/<batchId>/           # 例如 docs/test/dataset-2/batch/
├── batch.json                      # 批次身份、任务清单、两侧前提、模型/知识快照、授权与恢复条件
├── items/<taskId>.json             # 逐项调度状态与结论（每项一个文件）
├── events.jsonl                    # 追加式事件日志，只追加不改写
├── README.md                       # 本批状态与目录导航；**建批次索引时即建、全程保持最新**（导航件，不是关闭时才产）
├── summary.md                      # 批次汇总：按[批量工作流 §6](../../skills/workflows/batch-conversion/SKILL.md) 分列、不合成单一成功率；**关闭时须存在且定稿**（可作运行草稿，关闭前完成）
├── reconciliation-<序号>.md         # 增量对账记录，每 40 项一次；只追加不改写
└── <按实际发生的批次级记录>.md        # 冻结清单、提交计划、问题审计等；未发生不建
```

**`README.md` 与 `summary.md` 触发时点不同，不可混为一谈**：`README.md` 是**导航/状态件**，建批次索引时就建、随批次推进保持最新（它回答"这批现在在哪、各目录怎么走"）；`summary.md` 是**关闭时的汇总件**，按批量工作流 §6 分列各维度，关闭前须存在并定稿。二者都属批次索引的必备件，缺任一在[终态门禁 §2.1.1](#211-单文件任务的标准骨架2026-10-09-冻结按-docstestdataset-实测形制) 的批次级核对与关闭终局核对中记缺档；但**不得**用"summary 关闭时才产"的理由连带省掉本该早建的 `README.md`。

**对账频率**：批次是**一个**，但对账按**每新增 40 项终态一次**做增量检查点，关闭前再做一次覆盖全部检查点的终局核对。规则见[批量工作流 §4.1](../../skills/workflows/batch-conversion/SKILL.md)。

| 规则 | 说明 |
|---|---|
| 批次索引**必须**建 | 逐项骨架只记"这项自己怎样"，回答不了"这批有哪几项、哪些没跑完"。[批量工作流 §4](../../skills/workflows/batch-conversion/SKILL.md) 要求可追溯的接入、去向、冻结与恢复边界，本目录是它的落点 |
| **批次索引完整性受终态门禁核对** | `README.md`（导航件，须在且最新）、`summary.md`（关闭时须在且定稿）、`items/` 去向齐全、`events.jsonl` 齐备——在每次 40 项增量对账与关闭终局核对（[批量工作流 §4.1/§6](../../skills/workflows/batch-conversion/SKILL.md)）中逐项核。缺件按缺档处理，不因"未发生不建"省掉导航件 |
| **不另设逐项状态文件** | 逐项阶段、版本、哈希、用量、回执与终态一律落在该 case 的 `output/<batchId>/`（§2.1.1）；批次根不再复制一份 |
| `items/<taskId>.json` 只放调度语义 | `phase`/`lifecycle`/`pendingAction`/阻断原因/终态，按[批量工作流 §5](../../skills/workflows/batch-conversion/SKILL.md) 分列。它是索引指针，不是第二份证据；结论以该 case 的 `04-evaluation/` 实际回传为准 |
| `events.jsonl` 只追加 | 每行一个 JSON 对象；身份用 `batchId`+`taskId`（+轮次/job）。已写行不改写，更正以新事件追加 |
| **原始条目去向必须齐全** | 每个 rawItemId/候选方向按[任务状态 §3](task-state-contract.md#3-接入去向)记录当前去向，含 SOURCE_NOT_BUILDABLE / SOURCE_DEPENDENCY_GAP；不得只列已冻结项 |
| 批次索引**不是**证据 | 它不是编译、行为或安全结论，不替代 `04-evaluation/` 的真实回传；`summary.md` 的计数不能当验收通过率 |

### 2.2 阶段子目录：过程产物与命名

过程产物按[转换—自审—第三方评估闭环](../workflow/conversion-evaluation-loop.md)的阶段归入固定子目录，命名用确定性的**轮次/job 编号**，不用 `remote`/`pocc`/`final`/`retry` 等临时词，使"第几轮转换、第几次自审、第几个 job"直接从文件名读出。只创建当前 run 实际产生的目录与文件；未产生的阶段不建空目录。

编号是本地记录身份，不保证每个阶段只有一个请求或 job。首次源预检沿用 job-00；它若失败后重取，新增实际 job 并注明源预检用途/父记录。job-01-dual-build 是常见首次双侧落点，已有其他 job 占用序号时按实际递增，不覆盖或重编号历史。拒收/未知提交先保存 attempt，不能给未知 job 编造 jobId。文件名中的序号、修复轮次与平台 jobId 分别关联。

| 子目录 | 阶段 | 产物与命名 |
|---|---|---|
| `01-frozen/` | `FROZEN` · `CLASSIFIED` | frozen-inputs.md 是冻结事实正文，字段按[任务状态 §2](task-state-contract.md#2-冻结记录)；分类输入与递增结果 JSON 按分类准入留存，不属于第二份冻结正文。行为需求与 capsule 的 input_profile.json 策略须一致，字段见[比较策略适配](../adapter/controller/comparison-policy-adapter.md) |
| `02-conversion/` | `GENERATED`·`SELF_REPAIRED`·`REPAIR_AFTER_EVAL` | 各版本目标稿及其模型元数据（见下） |
| `03-self-review/` | `SELF_REVIEWED` | `self-review-<N>.json`（结构化结论与逐项证据）、`self-review-<N>.model.json`（该次调用元数据）、`self-review-<N>.decision.json`（结论经澄清时）、`self-review-<N>.attempt-<k>-failed.json`（无效/截断/矛盾的失败尝试） |
| `04-evaluation/` | `SOURCE_BUILDABLE`·`EVALUATED`·`REPAIR_AFTER_EVAL` | 每个第三方 job 一个子目录 `job-<NN>-<用途>/`（见下） |

**`02-conversion/` 版本命名**（同一 run 内按先后，`<ext>` 为目标扩展名）：

- `target.gen.<ext>`：首个完整模型稿（GENERATED）。任何改变代码语义的后续修订都另存版本及差异；原稿与原始响应不改写。
- `target.self-repair-<N>.<ext>`：第 N 次结构化自修稿（SELF_REPAIRED，默认 ≤2）。
- `target.eval-repair-<N>.<ext>`：第三方反馈后第 N 次修复稿（REPAIR_AFTER_EVAL，语法/构建与功能分支共用默认总上限 ≤2）；同轮元数据记录 `repairKind`、来源 job/反例、父版本哈希、诊断/允许差异、修复目标及新版本重评结果。它是本仓库记录，不新增平台必需字段或另设两套版本编号。
- 每份代码稿配同 stem 元数据：`<stem>.model.json`（模型名、参数、token、finish_reason、输入/输出 SHA-256）、`<stem>.proposal.json`（机械应用时模型给出的补丁/建议）、`<stem>.provenance.json`（差异与来源哈希，若适用）、`<stem>.attempt-<k>-failed.json`（该轮失败/截断尝试及原因）。
- 功能反馈与修复过程按[闭环 §3.1–3.2](../workflow/conversion-evaluation-loop.md#31-语法与功能修复反馈分支)关联保存；语法已通过但行为未解决时不能合并成整体通过，修复完成/模型自审不等于平台确认解决。
- run 根 `target.<ext>` 始终等于本次最终交付版本，即使编译失败或尚未验证也不得暗示其已通过；不在根目录堆叠历史稿。

**`04-evaluation/` 目录内的 job 编号与用途**（2026-10-09 冻结，按 dataset-2 实测固化）：

| 编号 | 用途名 | 何时产生 |
|---|---|---|
| `job-00-source-buildability` | 源侧预检（目录名沿用） | 冻结与分类 ALLOWED 后，取源 build completed/exitCode=0 及适用有效运行基线；通过后才生成，文本/仅编译例外见评估准备 §1.1 |
| `job-01-dual-build` | 双侧评估（仅编译分支注明） | 目标生成/自审及适用评估就绪门禁通过后才提交，不要求未提交项伪造此目录 |
| `job-02-…` 起 | 后续诊断/修复重评 | 按实际发生递增；用途名用简短英文连字符（`branch-diagnostic`、`repair-verified` 等） |

**源侧预检必须落在 `04-evaluation/` 内并单独命名**，不得另建同级目录、不得混入 batch 根。
理由：它是该用例的一次真实 Controller 提交，其回执与证据同属该 run 的评估记录；
放在别处会与"每个第三方 job 一个子目录"的口径冲突，也无法与后续 job 按序对账。
预检读取**源侧** `build`，需行为评估时还读取适用 `execution`、原始观察及终止/清理记录，按[评估准备 §1.1](evaluation-readiness-contract.md#11-生成前源侧预检)核源基线；不以 build 成功代替源运行正常，不据源运行推定目标功能一致。源侧不可构建时按真实诊断记 `SOURCE_NOT_BUILDABLE`（平台不匹配）或 `SOURCE_DEPENDENCY_GAP`（引用快照外文件）；运行/观察缺口另记原因与恢复条件，不混为源不可构建。上述缺口均不是转换失败，此时不产生转换目标或 `job-01-dual-build`、不消耗转换模型调用。不适用源运行的文本/片段/仅编译分支须留理由，未发生的 execution 不伪造。

每个 job 目录内统一 stem：

- `job-id.txt`：Controller job ID。
- `report.json` / `report.md`：Controller canonical report。
- `returned-evidence/`：按分支和现役接口保存实际返回的原 report、适用侧 evidence、comparison、logs、状态与环境/清理记录；源预检不要求目标/comparison，仅编译不要求不存在的 execution/comparison。接口缺件/下载失败保留诊断及缺口，不造空文件充完整；必需原件未取得仍按门禁处理。规范落点见[Controller 适配](../adapter/controller/remote-controller-adapter.md)。
- `capsule.zip`：实际提交输入；source/、target/ 为暂存树（若保留）。实际采用的合法来源驱动随 capsule 留存，记录来源/哈希，供复核观察；不强制 Python，不授权新写辅助程序。仅编译不得混入执行入口。
- **驱动记录**：`frozen-inputs.md` 的 `driver` 字段须写明该驱动器形态、冻结的 argv/stdin、等待的就绪条件与终止方式，使"驱动是否满足四要素"可被独立复核。未记录驱动形态的双侧提交视为评估就绪核对未通过。
- job 内 JSON 是第三方返回或提交时的**记录**：重命名文件不改其内部内容；内部出现的旧文件名是当时提交名的历史事实，不回改。

上述目录与 run 根、`01-frozen/`、`03-self-review/` 同属一次 run；`evaluator_manifest.json` 的路径指针须指向这些实际落点。

长文件分段时，在现有阶段目录内按单元标识保存实际产生的模型输出与请求元数据，避免不同单元覆盖同名文件；单元/跨单元审阅仍使用 run 内唯一递增的 `self-review-<N>`，注明范围、所审代码与依赖哈希。整文件版本继续使用上述 stem；同轮分段修订尚未合并完整时只保留单元产物并注明部分完成，不冒称完整版本。`source-analysis.md` 关联最终整文件哈希、单元对应与审阅记录；预算统一按[闭环 §2](../workflow/conversion-evaluation-loop.md#2-阶段及门槛)，不因单元命名另计默认预算。

上述产物同目录，便于消费方按清单定位；长单文件多一份 `source-analysis.md`。命名细节以任务契约为准，但阶段归位与轮次/job 编号规则不因契约省略。

#### 2.2.1 来源记录与最终版本核对

记录使用既有 model/provenance/decision/job 文件或其不可变引用，不另建通用台账或工具。适用时须能逐项回读：

| 对象 | 必须保留/核对 |
|---|---|
| 模型请求与响应 | 脱敏实际请求正文、源范围/契约/本地知识快照、参数、配置/实际模型、attempt、状态/finish_reason、真实用量、原响应；成功与失败均保留，不只保存最后一次 |
| 目标版本 | 原响应到文件的提取/解码、机械合并或补丁依据、父/新目标身份与差异；缺完整正文不能靠哈希回填。修复轮次与请求次数分别记录 |
| 自审与裁决 | 被审版本/范围、reviewN/attempt、原响应及有效性、实际条目、格式恢复依据或追加裁决；不能拿可见 verdict 当完整审阅 |
| 提交与返回 | 发送前 attempt/实际 capsule 及源目标/驱动/fixture/配置身份、分类/授权引用、回执/拒收/未知诊断、jobId、原始证据及取得时间；清理未确认不记终态 |
| 根级交付与报告 | 根级文件等于所指最终版本；每项结论指向支持该版本及条件的原件。新稿无证据就 UNVERIFIED，不能借旧稿 PASS 或从最新目录猜版本 |

职责与复用判据见[任务状态 §2.1](task-state-contract.md#21-版本关联与复用边界)及[评估准备 §1.2](evaluation-readiness-contract.md#12-源基线复用与失效)。字段名可沿用当前消费者的实际记录，不新增 Controller schema；缺历史字段只登记缺口/有依据的追加说明，不倒填曾发生的请求或执行。

### 2.3 `result.md`：面向读者的中文报告骨架

result.md 是所有已处理项的结果阅读入口，成功、失败、生成前阻断/非可转换及 WAITING 暂停均适用，不以目标已产出为前提。它不把日志、manifest 字段或模型逐轮回复按时间堆在一起。沿用以下相同标题与顺序；无材料的栏目保留标题，简写“未执行／未验证／不适用”及原因。正文用中文和短句，先说结论与影响，再给可追溯证据；工具链命令、job ID、模型原话和完整诊断放在链接指向的过程文件中，只有决定结论的关键细节进入正文。§1.1 的实际产物核对写入第 4 栏，失败/暂停原因与恢复条件写入第 3/5 栏，不能只留一句“失败”。

1. **结论速览**：一句话说明阶段目标及主要限制，随后三行表分别回答交付完整性、最终语法/编译、功能覆盖。交付写已完成/部分完成/未完成；编译写通过/失败/未验证/无法判定；功能写约定范围内匹配/发现差异/未验证/无法判定并列覆盖范围。实际平台 behaviorVerdict 在报告/item 中原样保留，另列本项目覆盖结论；允许差异逐条给依据和归因，不以维度计数替代档位。采信条件统一见[评估准备 §5](evaluation-readiness-contract.md#5-原始观察采信与归因)。缺证据写未验证，不只写“转换成功”或引用总 verdict。
2. **任务与最终交付**：列源/目标语言和系统、任务模式、目标文件链接、目标标准/工具链与必要上下文。只写影响结论的范围约束，例如长文件超限、已有目标平台分支或尚未冻结的编译器；其余画像链接到 `source-analysis.md`。
3. **转换过程与关键问题**：按“发生了什么 → 证据指向哪里 → 如何修订 → 最终怎样”叙述 1–3 个真正影响交付的事项。说明是否有修订、主要问题类别及最后处理结果；区分模型自评、编译器诊断、源已有问题和转换引入问题。中间轮数、请求失败及 token 等只作开发追溯，不作为质量结论；无实质修订时写“无修订”及依据。
4. **验证依据与覆盖范围**：把最终交付版本的编译证据写清目标文件版本、工具链、命令或记录链接和结论；中间稿证据只用于解释问题，不替代最终稿结果。若做过功能比较，写明输入、观察维度、匹配/差异和未覆盖项；未做则写 `未验证`，不引用有限旧例证明本次功能。静态审阅、自评、编译、运行与行为比较分开说。
5. **未决问题与下一步**：只列会影响使用或下一轮决策的未确认项，按影响排序；给出下一项具体可执行动作。已解决的诊断、完整日志与冗长风险清单留在证据文件，避免重复正文。

结论速览建议采用固定表头：`问题 | 结论 | 依据与边界`。例如：`语法/编译 | 通过 | 最终 target.cpp 在指定 Windows x64、C++17 工具链下编译通过；见 job 链接`，`功能一致性 | 未验证 | 该任务未冻结功能 oracle`（或 `功能一致性 | 未验证 | 无安全可观察入口（LIB_UNOBSERVABLE_COMPILE_ONLY），只取双侧编译证据`）。功能结论以第三方平台在已确认任务、可接受差异和现役评估契约下回传的实际证据为依据；参考[评估指导](../workflow/behavior-preservation-contract.md)报告目标→已接受差异/比较策略→平台最终版本证据及未覆盖项。本页不额外要求整组回归或统一字节比较；缺该项约定的证据时报告部分覆盖/未验证，平台配置疑点保留原判定并请求重评，不由 Agent 自行改判。有限输入的输出匹配只报告被实际观察的输入与维度；其他行为未验证。报告可随任务复杂度增减每节长度，不能更换上述五个栏目或将证据等级混写。

## 3. `evaluator_manifest.json` 字段来源纪律（三分）

填写时按来源分三类，不得混淆或自创：

- **(A) 转换结果类——据实填**：`files[].relativePath`、`sourcePath`、`translatedCodePath`、`artifacts.hasTranslatedCode`、`files[].success`。其中 `success` 表示“该文件转换产物已就绪可交评测”，**不表示验证通过**；目标代码未产出前为 `false`。
- **(B) 任务输入类——从冻结输入/任务契约抄**：`languagePair`、`taskMetadata`（`sourceLang`/`targetLang`/`sourceOs`/`targetOs`/`sourceArch`/`targetArch`/`sceneTags`/`attackTactic`/`riskLevel`）、`targetDir`、隔离启动参数。不凭函数名或战术标签推断；契约未给的标为待确认。
- **(C) 审批·执行·验证类——据实记录，不凭自评宣称**：已有授权与本次实际提交分开记录。`executionApproved` 默认 `false`；只有本次 comparison capsule 被获批隔离 Controller 接收并取得回执后置 `true`，记录 job ID。返回证据到达后再填写证据路径及语法/行为结论；提交未返回证据不回退授权状态，也不填 PASS。`plannedResultPath`/`plannedReportPath`/`plannedEvaluatorOutputPath` 只是计划落点；`evidenceMode`/`supportLevel` 按契约填，缺省 `experimental`。

## 4. manifest 形状（临时，对齐外部控制器）

核心字段沿用项目移交清单的 `third-party-evaluator-manifest` 形状；它不是当前 Controller `/api/jobs` 可直接提交的 capsule。**占位模板见同目录 [`evaluator_manifest.example.json`](evaluator_manifest.example.json)，填写前核对消费方契约。**

- 顶层：`schemaVersion`、`kind: "third-party-evaluator-manifest"`、`generatedBy`、`languagePair{sourceLang,targetLang}`、`taskMetadata`、`targetDir`、`summaryPath`、`batchReportPath`、`replayArtifactDir`、`plannedResultPath`、`plannedReportPath`、`files[]`。
- `taskMetadata`：`sourceLanguage`、`targetLanguage`（**注意**：控制器 schema 在此用长名，与 `languagePair` 的 `sourceLang`/`targetLang` 短名并存且冗余——照它保留，不要“修正”成一致）、`attackTactic`、`sceneTags[]`、`sourceOs`、`targetOs`、`sourceArch`、`targetArch`、`riskLevel`、`evidenceMode`、`supportLevel`。
- `files[]` 每项：`relativePath`、`sourcePath`、`translatedCodePath`、`evaluationNotesPath`（可为 null）、`replayArtifactPath`（可为 null）、`success`、`artifacts{hasSource,hasTranslatedCode,hasEvaluationNotes,hasReplayArtifact}`、`plannedEvaluatorOutputPath`。
- 本项目专用附加段 `x_adapter`：承载“未执行 / 未批准 / 前置条件 / 隔离启动参数”等**本仓库临时状态**，不污染核心 schema，控制器不消费；长单文件可加 `sourceAnalysisPath` 指向同目录画像；`generatedBy` 标为 hand-authored（非控制器 MCP 产出）。

现役控制器 schema 与本形状不一致时，**以控制器实际契约为准**；本节属临时适配，控制器更新后同步或废弃。

## 5. UNVERIFIED 与移交

- `result.md` 可记录模型自检发现与 repair 决定，但不得把它当作独立静态语法评估。语法结论由用户指定的第三方评估机构按匹配工具链编译后回填；未收到结果时写 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`。行为 oracle 单独报告；编译成功不证明行为正确。
- 不得用语法通过、代码相似度或模型自评替代行为 oracle，也不得据静态核对宣称“功能等价”。
- 移交即把与实际 Controller 契约匹配的 capsule 和记录清单交给编译/运行环境；本项目不在本机执行。获授权的第三方结果返回后，回填 source/target build、execution、comparison、清理和环境状态，但仍将语法、行为和安全覆盖分层报告。
