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

### 2.2 阶段子目录：过程产物与命名

过程产物按[转换—自审—第三方评估闭环](../workflow/conversion-evaluation-loop.md)的阶段归入固定子目录，命名用确定性的**轮次/job 编号**，不用 `remote`/`pocc`/`final`/`retry` 等临时词，使"第几轮转换、第几次自审、第几个 job"直接从文件名读出。只创建当前 run 实际产生的目录与文件；未产生的阶段不建空目录。

| 子目录 | 阶段 | 产物与命名 |
|---|---|---|
| `01-frozen/` | `FROZEN` | `frozen-inputs.md`：源快照哈希、语言/OS/ABI、条件编译分支、目标编译器/SDK、模型标识与参数、RAG 开关、oracle、隔离/授权范围 |
| `02-conversion/` | `GENERATED`·`SELF_REPAIRED`·`REPAIR_AFTER_EVAL` | 各版本目标稿及其模型元数据（见下） |
| `03-self-review/` | `SELF_REVIEWED` | `self-review-<N>.json`（结构化结论与逐项证据）、`self-review-<N>.model.json`（该次调用元数据）、`self-review-<N>.decision.json`（结论经澄清时）、`self-review-<N>.attempt-<k>-failed.json`（无效/截断/矛盾的失败尝试） |
| `04-evaluation/` | `EVALUATED`·`REPAIR_AFTER_EVAL` | 每个第三方 job 一个子目录 `job-<NN>-<用途>/`（见下） |

**`02-conversion/` 版本命名**（同一 run 内按先后，`<ext>` 为目标扩展名）：

- `target.gen.<ext>`：首个完整模型稿（GENERATED）。任何改变代码语义的后续修订都另存版本及差异；原稿与原始响应不改写。
- `target.self-repair-<N>.<ext>`：第 N 次结构化自修稿（SELF_REPAIRED，默认 ≤2）。
- `target.eval-repair-<N>.<ext>`：第三方评估失败后第 N 次修复稿（REPAIR_AFTER_EVAL，默认 ≤2）。
- 每份代码稿配同 stem 元数据：`<stem>.model.json`（模型名、参数、token、finish_reason、输入/输出 SHA-256）、`<stem>.proposal.json`（机械应用时模型给出的补丁/建议）、`<stem>.provenance.json`（差异与来源哈希，若适用）、`<stem>.attempt-<k>-failed.json`（该轮失败/截断尝试及原因）。
- run 根 `target.<ext>` 始终等于本次最终交付版本，即使编译失败或尚未验证也不得暗示其已通过；不在根目录堆叠历史稿。

**`04-evaluation/job-<NN>-<用途>/`**：`<NN>` 按提交顺序（`01`、`02`…），`<用途>` 用简短英文连字符描述（如 `initial-probe`、`branch-diagnostic`、`repair-verified`）。每个 job 目录内统一 stem：

- `job-id.txt`：Controller job ID。
- `report.json` / `report.md`：Controller canonical report。
- `returned-evidence/`：保存原始 `evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`、`comparison.json`、`controller.log` 及取回的状态；与[Controller 适配](../adapter/controller/remote-controller-adapter.md)一致。
- `capsule.zip`：提交的输入 capsule；`source/`、`target/`：该 job 暂存的源/目标树（若保留）。
- job 内 JSON 是第三方返回或提交时的**记录**：重命名文件不改其内部内容；内部出现的旧文件名是当时提交名的历史事实，不回改。

上述目录与 run 根、`01-frozen/`、`03-self-review/` 同属一次 run；`evaluator_manifest.json` 的路径指针须指向这些实际落点。

上述产物同目录，便于消费方按清单定位；长单文件多一份 `source-analysis.md`。命名细节以任务契约为准，但阶段归位与轮次/job 编号规则不因契约省略。

### 2.3 `result.md`：面向读者的中文报告骨架

`result.md` 是交付结果的阅读入口，不是把日志、manifest 字段或模型逐轮回复按时间堆在一起。所有转换任务使用以下**相同标题与顺序**；无材料的栏目保留标题，简写“未执行／未验证／不适用”及原因。正文用中文和短句，先说结论与影响，再给可追溯证据；工具链命令、job ID、模型原话和完整诊断放在链接指向的过程文件中，只有决定结论的关键细节进入正文。

1. **结论速览**：开头用一句话说明本次阶段目标是否达成及最重要的限制。紧接三行表格，分别回答“最终代码是否交付完整”“在什么工具链和上下文下语法/编译是否通过”“功能在什么可观察范围内是否一致”。建议状态：交付 `已完成／部分完成／未完成`；语法 `通过／失败／未验证／无法判定`；功能 `约定范围内匹配／发现差异／未验证／无法判定`。功能只在实际 oracle 覆盖范围内判断；当前编译质量阶段未做功能评估时直接写 `未验证`。不得只写“转换成功”或引用 Controller 总 verdict 代替三项结论。
2. **任务与最终交付**：列源/目标语言和系统、任务模式、目标文件链接、目标标准/工具链与必要上下文。只写影响结论的范围约束，例如长文件超限、已有目标平台分支或尚未冻结的编译器；其余画像链接到 `source-analysis.md`。
3. **转换过程与关键问题**：按“发生了什么 → 证据指向哪里 → 如何修订 → 最终怎样”叙述 1–3 个真正影响交付的事项。说明是否有修订、主要问题类别及最后处理结果；区分模型自评、编译器诊断、源已有问题和转换引入问题。中间轮数、请求失败及 token 等只作开发追溯，不作为质量结论；无实质修订时写“无修订”及依据。
4. **验证依据与覆盖范围**：把最终交付版本的编译证据写清目标文件版本、工具链、命令或记录链接和结论；中间稿证据只用于解释问题，不替代最终稿结果。若做过功能比较，写明输入、观察维度、匹配/差异和未覆盖项；未做则写 `未验证`，不引用有限旧例证明本次功能。静态审阅、自评、编译、运行与行为比较分开说。
5. **未决问题与下一步**：只列会影响使用或下一轮决策的未确认项，按影响排序；给出下一项具体可执行动作。已解决的诊断、完整日志与冗长风险清单留在证据文件，避免重复正文。

结论速览建议采用固定表头：`问题 | 结论 | 依据与边界`。例如：`语法/编译 | 通过 | 最终 target.cpp 在指定 Windows x64、C++17 工具链下编译通过；见 job 链接`，`功能一致性 | 未验证 | 本阶段没有功能 oracle`。有限输入的输出匹配只报告被实际观察的输入与维度；其他行为未验证。报告可随任务复杂度增减每节长度，不能更换上述五个栏目或将证据等级混写。

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
