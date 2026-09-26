# 转换交付与移交契约：收尾产物与 evaluator_manifest.json

本文件在**任一转换任务收尾时**读取，规定交付产物集合、目录布局，以及交给编译/运行环境的 `evaluator_manifest.json` 如何填写。它是**过程纪律与字段来源规则**，不是“转换正确”或“功能等价”的证明。本项目不在本机编译或运行；经用户逐例授权后，可以把 comparison capsule 交给隔离第三方评估环境，语法与行为结论仍只能由该环境的真实证据回填。manifest 形状对齐外部控制器、属**临时适配**，权威 schema 以现役控制器为准。

它与转换本身的维度分开：语言方向/场景/系统方向 Skill 管映射与应保留行为，长单文件工作流管防偏移，本契约只管**收口与移交**，不重复它们的内容。

## 1. 何时适用

- 片段、单文件、长单文件任一模式的转换完成后都走本收尾；片段任务若无评测需求，可只产出目标文件与 `result.md`，`evaluator_manifest.json` 视消费方要求决定是否生成。
- “完成”至少指目标代码已产出、结构化模型自审/有限自修门槛已完成、静态全文件核对已做；不代表已验证语法或行为。若用户批准动态评估，还须遵循[转换—自审—第三方评估闭环](conversion-evaluation-loop.md)。
- 未经来源/许可、工具链、隔离环境逐项批准，不得编译或运行任何产物；显式加载本契约不是执行授权。

## 2. 固定产物集合与目录布局

一次转换 run 的输出落在任务契约指定的同一目录，至少包含：长单文件还须保留 `source-analysis.md`，记录源码事实、任务标签和 Skill 选择；短片段无需强制生成该文件。

| 产物 | 内容 | 备注 |
|---|---|---|
| `target.<ext>`（可多个） | 目标语言文件 | 多文件逐一列入 manifest `files[]` |
| `source-analysis.md`（长单文件） | 源/目标画像、证据化标签、ATT&CK 判断、Skill 选择、源码地图与未决项 | 为 Skill 选择及全文件核对提供可审阅依据 |
| `result.md` | 交付说明：完成范围、待确认假设、模型自检/repair、第三方编译与行为结果 | 模型预检不得充当语法结论；未收到第三方编译结果时明确标记 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED` |
| `evaluator_manifest.json` | 移交清单：告知编译/运行环境文件位置、任务元数据、待批准状态 | 形状见第 4 节，临时适配 |

上述产物同目录，便于消费方按清单定位；长单文件多一份 `source-analysis.md`。命名与落点以任务契约为准。

## 3. `evaluator_manifest.json` 字段来源纪律（三分）

填写时按来源分三类，不得混淆或自创：

- **(A) 转换结果类——据实填**：`files[].relativePath`、`sourcePath`、`translatedCodePath`、`artifacts.hasTranslatedCode`、`files[].success`。其中 `success` 表示“该文件转换产物已就绪可交评测”，**不表示验证通过**；目标代码未产出前为 `false`。
- **(B) 任务输入类——从冻结输入/任务契约抄**：`languagePair`、`taskMetadata`（`sourceLang`/`targetLang`/`sourceOs`/`targetOs`/`sourceArch`/`targetArch`/`sceneTags`/`attackTactic`/`riskLevel`）、`targetDir`、隔离启动参数。不凭函数名或战术标签推断；契约未给的标为待确认。
- **(C) 审批·执行·验证类——智能体无权自行授予**：`executionApproved` 默认是 `false`；只有用户逐例明确授权并确实向隔离环境提交后，才可改为 `true`，同时记录授权上下文、job ID 和证据路径。语法与行为结果必须按第三方真实报告回填，不能凭 Agent 或模型自评宣称；`plannedResultPath`/`plannedReportPath`/`plannedEvaluatorOutputPath` 只是“计划落点”而非已有结果；`evidenceMode`/`supportLevel` 按契约填，缺省 `experimental`。

## 4. manifest 形状（临时，对齐外部控制器）

核心字段对齐外部控制器既有的 `third-party-evaluator-manifest` 形状（已核对旧仓库真实样例，如 `reverse_http_evaluator_manifest.json`），便于其直接消费。**完整占位模板见同目录 [`evaluator_manifest.example.json`](evaluator_manifest.example.json)，填写时照抄结构、只改值。**

- 顶层：`schemaVersion`、`kind: "third-party-evaluator-manifest"`、`generatedBy`、`languagePair{sourceLang,targetLang}`、`taskMetadata`、`targetDir`、`summaryPath`、`batchReportPath`、`replayArtifactDir`、`plannedResultPath`、`plannedReportPath`、`files[]`。
- `taskMetadata`：`sourceLanguage`、`targetLanguage`（**注意**：控制器 schema 在此用长名，与 `languagePair` 的 `sourceLang`/`targetLang` 短名并存且冗余——照它保留，不要“修正”成一致）、`attackTactic`、`sceneTags[]`、`sourceOs`、`targetOs`、`sourceArch`、`targetArch`、`riskLevel`、`evidenceMode`、`supportLevel`。
- `files[]` 每项：`relativePath`、`sourcePath`、`translatedCodePath`、`evaluationNotesPath`（可为 null）、`replayArtifactPath`（可为 null）、`success`、`artifacts{hasSource,hasTranslatedCode,hasEvaluationNotes,hasReplayArtifact}`、`plannedEvaluatorOutputPath`。
- 本项目专用附加段 `x_adapter`：承载“未执行 / 未批准 / 前置条件 / 隔离启动参数”等**本仓库临时状态**，不污染核心 schema，控制器不消费；长单文件可加 `sourceAnalysisPath` 指向同目录画像；`generatedBy` 标为 hand-authored（非控制器 MCP 产出）。

现役控制器 schema 与本形状不一致时，**以控制器实际契约为准**；本节属临时适配，控制器更新后同步或废弃。

## 5. UNVERIFIED 与移交

- `result.md` 可记录模型自检发现与 repair 决定，但不得把它当作独立静态语法评估。语法结论由用户指定的第三方评估机构按匹配工具链编译后回填；未收到结果时写 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`。行为 oracle 单独报告；编译成功不证明行为正确。
- 不得用语法通过、代码相似度或模型自评替代行为 oracle，也不得据静态核对宣称“功能等价”。
- 移交即把与实际 Controller 契约匹配的 capsule 和记录清单交给编译/运行环境；本项目不在本机执行。获授权的第三方结果返回后，回填 source/target build、execution、comparison、清理和环境状态，但仍将语法、行为和安全覆盖分层报告。
