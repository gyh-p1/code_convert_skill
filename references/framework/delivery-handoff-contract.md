# 转换交付与移交契约：收尾产物与 evaluator_manifest.json

本文件在**任一转换任务收尾时**读取，规定交付产物集合、目录布局，以及交给编译/运行环境的 `evaluator_manifest.json` 如何填写。它是**过程纪律与字段来源规则**，不是“转换正确”或“功能等价”的证明。本项目不在本机编译或运行；按**本项目既定的双侧执行授权**，把 comparison capsule 交给获批隔离 VM 构建并运行源、目标两侧，本阶段只读取其 build 证据，语法与行为结论仍只能由该环境的真实证据回填。manifest 形状对齐外部控制器、属**临时适配**，权威 schema 以现役控制器为准。

它与转换本身的维度分开：语言方向/场景/系统方向 Skill 管映射与应保留行为，长单文件工作流管防偏移，本契约只管**收口与移交**，不重复它们的内容。

## 1. 何时适用

- 片段、单文件、长单文件任一模式的转换完成后都走本收尾；片段任务若无评测需求，可只产出目标文件与 `result.md`，`evaluator_manifest.json` 视消费方要求决定是否生成。
- “完成”至少指目标代码已产出、结构化模型自审/有限自修门槛已完成、静态全文件核对已做；不代表已验证语法或行为。动态评估按已有任务授权与[转换—自审—第三方评估闭环](../workflow/conversion-evaluation-loop.md)推进。
- 进入编译或运行前逐项核对源码存在、工具链、代码行为与隔离环境；显式加载本契约不是执行授权。许可正文、版本号、上游 commit、仓库 URL 不作测试用例冻结或提交校验。

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

短片段任务若无评测需求，可只产出 `target.<ext>` 与 `result.md`，不强制建阶段子目录。

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
    │   ├── job-00-source-buildability/   # 源侧可构建性预检（固定第一步）
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
| `01-frozen/` 固定三件套 | `frozen-inputs.md`（冻结事实，Markdown）+ `classifier-input.json`（分类输入快照）+ `classification-1.json`（分类结果）。**不写 `frozen-inputs.json`** |
| **提交前必须已有 `classification-1.json` 且 `admissionStatus=ALLOWED`** | 这是[分类结果准入](../../references/workflow/classifier-agent-gate.md)的强制门禁：**每次进入 EVALUATION_READY、提交或重提之前都必须消费**；没有有效结果**不得** POST `/api/jobs`。分类源未变的修复稿不需重复分类 |
| `frozen-inputs.md` 必须记录授权与隔离 | 含授权来源、范围、有效期，源/目标 VM 与 runnerId、网络边界、清理条件；**不得只靠事后 evidence 的 `clean` 代替提交前记录** |
| **不写 `prompt.txt`** | 请求正文属于过程，不进 run 目录；提示词可从 `*.model.json` 的请求哈希与 `raw.txt` 追溯 |
| **不写 `*-raw.txt` 到 `03-self-review/`** | 自审只需要 `self-review-<N>.json` 与 `.model.json` 两份 |
| **不写 `state.json` / `submission-response.json`** | 提交回执体现在 `job-id.txt`；轮询中间态不留档 |
| 根级必须有 `target.<ext>` | 与 `02-conversion/target.gen.<ext>` 内容相同（无自修时），但**根级才是交付版** |
| 阶段目录按实际产生创建 | 未发生的阶段不建空目录 |
| `04-evaluation/` 下只有 `job-*` | 不建 `_probes`、`logs` 等旁支目录 |

**交付完整性自检（终态前门禁，2026-10-10 实测补入）**：把某项记为终态（`DONE`/`PARTIAL`）前，必须机械核对该项 `output/<batchId>/` 下**最终交付物齐备**——根级 `target.<ext>`、`result.md`、`evaluator_manifest.json`（契约要求时）、`01-frozen/` 三件套，以及实际发生过的每个 `04-evaluation/job-*` 的 `returned-evidence/`。缺任一必备件即**不得**记终态；该核对同时是批次增量对账（[批量工作流 §4.1](../../skills/workflows/batch-conversion/SKILL.md)）的固定项。曾出现 20 项缺 `result.md` 的反例，故单列为门禁。

### 2.1.2 批次索引骨架（2026-10-09 冻结，按 `docs/test/dataset/batch-01/` 实测形制）

**批次索引与单文件骨架是两层，不是一个**：批次索引记录"这批有哪几项、各自去向与终态"，落在数据集根的 `<batchId>/`，与方向目录**平级**；每项的转换产物仍落在 `<direction>/<case-id>/output/<batchId>/`（§2.1.1）。**禁止**把逐项状态文件再塞进批次根，也**禁止**把批次索引摊到每个 case 下——两层的落点不可互换。

**批次口径：一个数据集 = 一个批次。** `batchId` 取固定值（dataset-2 用 `batch`），**不再按固定条数切分多个批次**。交付基线要求的是"单批不少于 40 项的持续转换能力"，队列本身已满足，故一个批次承载全部条目；后续新增条目并入同一批次，保留已完成项身份与证据。理由见[批量工作流](../../skills/workflows/batch-conversion/SKILL.md)开篇。

```text
<dataset-root>/<batchId>/           # 例如 docs/test/dataset-2/batch/
├── batch.json                      # 批次身份、任务清单、两侧前提、模型/知识快照、授权与恢复条件
├── items/<taskId>.json             # 逐项调度状态与结论（每项一个文件）
├── events.jsonl                    # 追加式事件日志，只追加不改写
├── summary.md                      # 批次汇总，按 §6 分列，不合成单一成功率
├── README.md                       # 本批状态与目录导航
├── reconciliation-<序号>.md         # 增量对账记录，每 40 项一次；只追加不改写
└── <按实际发生的批次级记录>.md        # 冻结清单、提交计划、问题审计等；未发生不建
```

**对账频率**：批次是**一个**，但对账按**每新增 40 项终态一次**做增量检查点，关闭前再做一次覆盖全部检查点的终局核对。规则见[批量工作流 §4.1](../../skills/workflows/batch-conversion/SKILL.md)。

| 规则 | 说明 |
|---|---|
| 批次索引**必须**建 | 逐项骨架只记"这项自己怎样"，回答不了"这批有哪几项、哪些没跑完"。[批量工作流 §4](../../skills/workflows/batch-conversion/SKILL.md) 要求可追溯的接入、去向、冻结与恢复边界，本目录是它的落点 |
| **不另设逐项状态文件** | 逐项阶段、版本、哈希、用量、回执与终态一律落在该 case 的 `output/<batchId>/`（§2.1.1）；批次根不再复制一份 |
| `items/<taskId>.json` 只放调度语义 | `phase`/`lifecycle`/`pendingAction`/阻断原因/终态，按[批量工作流 §5](../../skills/workflows/batch-conversion/SKILL.md) 分列。它是索引指针，不是第二份证据；结论以该 case 的 `04-evaluation/` 实际回传为准 |
| `events.jsonl` 只追加 | 每行一个 JSON 对象；身份用 `batchId`+`taskId`（+轮次/job）。已写行不改写，更正以新事件追加 |
| **原始条目去向必须齐全** | 每个 `rawItemId` 在 `batch.json` 里有明确去向（`FROZEN`/`PREPARATION_GAP`/`DUPLICATE`/`EXCLUDED`/`SAFETY_BLOCKED`/`SKIPPED`）；不得只列已冻结项，让未跑的条目无声消失 |
| 批次索引**不是**证据 | 它不是编译、行为或安全结论，不替代 `04-evaluation/` 的真实回传；`summary.md` 的计数不能当验收通过率 |

### 2.2 阶段子目录：过程产物与命名

过程产物按[转换—自审—第三方评估闭环](../workflow/conversion-evaluation-loop.md)的阶段归入固定子目录，命名用确定性的**轮次/job 编号**，不用 `remote`/`pocc`/`final`/`retry` 等临时词，使"第几轮转换、第几次自审、第几个 job"直接从文件名读出。只创建当前 run 实际产生的目录与文件；未产生的阶段不建空目录。

| 子目录 | 阶段 | 产物与命名 |
|---|---|---|
| `01-frozen/` | `FROZEN` | `frozen-inputs.md`（**唯一产物，用 Markdown 不用 JSON**）：源快照哈希、语言/OS/ABI、条件编译分支、目标编译器/SDK、模型标识与参数、知识快照、RAG 开关、单文件行为目标/已确认可接受差异、第三方评估移交条件与初始状态/输入/oracle 来源/比较策略（适用时）、隔离/授权范围；较长地图可引用同目录文本。**必填字段行（与[批量工作流 §0 第 5 步](../../skills/workflows/batch-conversion/SKILL.md)的冻结表一致，缺任一项即冻结未完成）**：`batchId`、`taskId`、`direction`、`casePath`+`caseSha256`、`sourcePath`+`sourceSha256`、`sourceOs`/`targetOs` + `sourceOsBasis`、`arch`、`sourceRunnerId`/`targetRunnerId`、`snapshots`、`model`（含 temp 与 RAG 开关）、`outputBudget`（声明不设上限）、`selected skills`（逐条相对路径+sha256）、`sourceBuild`、`targetBuild`、`execution`；**驱动与评估四项**：`driver`（形态、冻结 argv/stdin、**等待的就绪条件**、终止方式）、`driverRationale`（为何该形态能观察到本程序行为）、`input`（argv/stdin/fixture 与工作目录初始状态）、`oracle`（是否需要功能评估；需要则写观察维度/比较策略/来源（**有可观察文件副作用申请 `["output","filesystem"]`，不要只 `output`**），不需要则写理由。**此处的"比较策略"是冻结记录里的描述，其可执行形态落在 capsule 的 `input_profile.json`（`observationPolicy.dimensions` / `comparisonPolicy`，见 [比较策略适配](../adapter/controller/comparison-policy-adapter.md)）；两者须一致，不得只写其一**） |
| `02-conversion/` | `GENERATED`·`SELF_REPAIRED`·`REPAIR_AFTER_EVAL` | 各版本目标稿及其模型元数据（见下） |
| `03-self-review/` | `SELF_REVIEWED` | `self-review-<N>.json`（结构化结论与逐项证据）、`self-review-<N>.model.json`（该次调用元数据）、`self-review-<N>.decision.json`（结论经澄清时）、`self-review-<N>.attempt-<k>-failed.json`（无效/截断/矛盾的失败尝试） |
| `04-evaluation/` | `EVALUATED`·`REPAIR_AFTER_EVAL` | 每个第三方 job 一个子目录 `job-<NN>-<用途>/`（见下） |

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
| `job-00-source-buildability` | 源侧可构建性预检 | **每个用例的固定第一步**；只读源侧 build 结果，通过才投入模型转换 |
| `job-01-dual-build` | 双侧构建与行为比较 | 源侧预检通过后，提交最终目标版本 |
| `job-02-…` 起 | 后续诊断/修复重评 | 按实际发生递增；用途名用简短英文连字符（`branch-diagnostic`、`repair-verified` 等） |

**源侧预检必须落在 `04-evaluation/` 内并单独命名**，不得另建同级目录、不得混入 batch 根。
理由：它是该用例的一次真实 Controller 提交，其回执与证据同属该 run 的评估记录；
放在别处会与"每个第三方 job 一个子目录"的口径冲突，也无法与后续 job 按序对账。
预检只读取**源侧** `build` 字段；源侧不可构建时记 `SOURCE_NOT_BUILDABLE`（平台不匹配）
或 `SOURCE_DEPENDENCY_GAP`（引用快照外文件），**两者都不是转换失败**，
且此时不产生 `job-01-dual-build`、不消耗模型调用。

每个 job 目录内统一 stem：

- `job-id.txt`：Controller job ID。
- `report.json` / `report.md`：Controller canonical report。
- `returned-evidence/`：保存原始 `evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`、`comparison.json`、`controller.log` 及取回的状态；与[Controller 适配](../adapter/controller/remote-controller-adapter.md)一致。
- `capsule.zip`：提交的输入 capsule；`source/`、`target/`：该 job 暂存的源/目标树（若保留）。其中 `source/run_case.py` 与 `target/run_case.py` 即**驱动**，必须随 capsule 留存，供复核"它观察到什么"。
- **驱动记录**：`frozen-inputs.md` 的 `driver` 字段须写明该驱动器形态、冻结的 argv/stdin、等待的就绪条件与终止方式，使"驱动是否满足四要素"可被独立复核。未记录驱动形态的双侧提交视为评估就绪核对未通过。
- job 内 JSON 是第三方返回或提交时的**记录**：重命名文件不改其内部内容；内部出现的旧文件名是当时提交名的历史事实，不回改。

上述目录与 run 根、`01-frozen/`、`03-self-review/` 同属一次 run；`evaluator_manifest.json` 的路径指针须指向这些实际落点。

长文件分段时，在现有阶段目录内按单元标识保存实际产生的模型输出与请求元数据，避免不同单元覆盖同名文件；单元/跨单元审阅仍使用 run 内唯一递增的 `self-review-<N>`，注明范围、所审代码与依赖哈希。整文件版本继续使用上述 stem；同轮分段修订尚未合并完整时只保留单元产物并注明部分完成，不冒称完整版本。`source-analysis.md` 关联最终整文件哈希、单元对应与审阅记录；预算统一按[闭环 §2](../workflow/conversion-evaluation-loop.md#2-阶段及门槛)，不因单元命名另计默认预算。

上述产物同目录，便于消费方按清单定位；长单文件多一份 `source-analysis.md`。命名细节以任务契约为准，但阶段归位与轮次/job 编号规则不因契约省略。

### 2.3 `result.md`：面向读者的中文报告骨架

`result.md` 是交付结果的阅读入口，不是把日志、manifest 字段或模型逐轮回复按时间堆在一起。所有转换任务使用以下**相同标题与顺序**；无材料的栏目保留标题，简写“未执行／未验证／不适用”及原因。正文用中文和短句，先说结论与影响，再给可追溯证据；工具链命令、job ID、模型原话和完整诊断放在链接指向的过程文件中，只有决定结论的关键细节进入正文。

1. **结论速览**：开头用一句话说明本次阶段目标是否达成及最重要的限制。紧接三行表格，分别回答“最终代码是否交付完整”“在什么工具链和上下文下语法/编译是否通过”“功能在什么可观察范围内是否一致”。建议状态：交付 `已完成／部分完成／未完成`；语法 `通过／失败／未验证／无法判定`；功能 `约定范围内匹配／发现差异／未验证／无法判定`。功能只在实际 oracle 覆盖范围内判断；行为一致性现为必收必报产物，按冻结 oracle 与实际观察逐例给出，无 oracle 或平台未观察到对应维度时写 `未验证`。平台 `behaviorVerdict` 分三档，报告与 item 记录中必须**原样写**，不得简写为"一致/通过"：`matched`（所有可适用维度 diffs=0）、`semantic_pass`（维度匹配但有被显式配置容忍的次要差异，须逐条列出被容忍差异并给出归因，归因不属于消噪类别的差异不得采信）、`mismatched`（关键/重大差异）。**注意**：`semantic_pass` 时 `matchedDimensions`/`mismatchedDimensions`/`inconclusiveDimensions` 可能全为 0，**不能用维度计数代替档位判定，只能读 `behaviorVerdict` 本身**；`matched` 也不单独采信，须核源侧产生过非空非退化观察（见[行为保持 §4.1](../workflow/behavior-preservation-contract.md)）。不得只写“转换成功”或引用 Controller 总 verdict 代替三项结论。
2. **任务与最终交付**：列源/目标语言和系统、任务模式、目标文件链接、目标标准/工具链与必要上下文。只写影响结论的范围约束，例如长文件超限、已有目标平台分支或尚未冻结的编译器；其余画像链接到 `source-analysis.md`。
3. **转换过程与关键问题**：按“发生了什么 → 证据指向哪里 → 如何修订 → 最终怎样”叙述 1–3 个真正影响交付的事项。说明是否有修订、主要问题类别及最后处理结果；区分模型自评、编译器诊断、源已有问题和转换引入问题。中间轮数、请求失败及 token 等只作开发追溯，不作为质量结论；无实质修订时写“无修订”及依据。
4. **验证依据与覆盖范围**：把最终交付版本的编译证据写清目标文件版本、工具链、命令或记录链接和结论；中间稿证据只用于解释问题，不替代最终稿结果。若做过功能比较，写明输入、观察维度、匹配/差异和未覆盖项；未做则写 `未验证`，不引用有限旧例证明本次功能。静态审阅、自评、编译、运行与行为比较分开说。
5. **未决问题与下一步**：只列会影响使用或下一轮决策的未确认项，按影响排序；给出下一项具体可执行动作。已解决的诊断、完整日志与冗长风险清单留在证据文件，避免重复正文。

结论速览建议采用固定表头：`问题 | 结论 | 依据与边界`。例如：`语法/编译 | 通过 | 最终 target.cpp 在指定 Windows x64、C++17 工具链下编译通过；见 job 链接`，`功能一致性 | 未验证 | 该任务未冻结功能 oracle`。功能结论以第三方平台在已确认任务、可接受差异和现役评估契约下回传的实际证据为依据；参考[评估指导](../workflow/behavior-preservation-contract.md)报告目标→已接受差异/比较策略→平台最终版本证据及未覆盖项。本页不额外要求整组回归或统一字节比较；缺该项约定的证据时报告部分覆盖/未验证，平台配置疑点保留原判定并请求重评，不由 Agent 自行改判。有限输入的输出匹配只报告被实际观察的输入与维度；其他行为未验证。报告可随任务复杂度增减每节长度，不能更换上述五个栏目或将证据等级混写。

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
