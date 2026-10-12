# DeepSeek harness B 审阅逐项记录 04（D2-141–D2-160）

> 范围：dataset-2-copy manifest D2-141–D2-150（本块 10 项）；状态：前 10 项完成，后 10 项（D2-151–D2-160）待续。
> 限制：原源/目标正文已删，不复原、不恢复、不编译/运行、不调模型/分类器、不发评估提交；只用原生 read/glob/grep，未用 pwsh。
> 工具限制：单行 JSON 的 read/grep 输出约 2000 字符截断，本块 `evidence-source.json` 全部落在截断区，已逐项标「可见部分（工具2000字符/行截断）」，不记为已读全文。
> 本块共同事实：D2-141–D2-150 均为「冻结 + 分类 ALLOWED + job-00 源预检后终止」的非转换去向；9 项 `SOURCE_DEPENDENCY_GAP`（源构建编译器诊断失败）、1 项 `PREPARATION_GAP`（D2-150）；全部 **0 模型调用**，无 `02-conversion`、无 `03-self-review`、无根 `target.*`、无 `job-01`、无 `evaluator_manifest.json`。

## 覆盖清单（供 harness-b-coverage.md 汇总）

| 项 | 实际目录 | 现存文件数 | 已读 | 已读(截断) | 未读 | 空文件 | 缺件 |
|---|---|---|---|---|---|---|---|
| D2-141 | csharp-to-python/D2-141-…-tokenprivileges.cs | 11 | 10 | 1 | 0 | 0 | 3 |
| D2-142 | csharp-to-python/D2-142-…-unquotedservicepath.cs | 11 | 10 | 1 | 0 | 0 | 3 |
| D2-143 | csharp-to-python/D2-143-…-identityutils.cs | 11 | 10 | 1 | 0 | 0 | 3 |
| D2-144 | csharp-to-ruby/D2-144-…-hijackablepaths.cs | 11 | 10 | 1 | 0 | 0 | 3 |
| D2-145 | csharp-to-ruby/D2-145-…-mcafeesitelistfiles.cs | 11 | 10 | 1 | 0 | 0 | 3 |
| D2-146 | csharp-to-ruby/D2-146-…-modifiableservicebinaries.cs | 11 | 10 | 1 | 0 | 0 | 3 |
| D2-147 | csharp-to-ruby/D2-147-…-registryautologons.cs | 11 | 10 | 1 | 0 | 0 | 3 |
| D2-148 | csharp-to-ruby/D2-148-…-registryautoruns.cs | 11 | 10 | 1 | 0 | 0 | 3 |
| D2-149 | csharp-to-ruby/D2-149-…-unattendedinstallfiles.cs | 11 | 10 | 1 | 0 | 0 | 3 |
| D2-150 | csharp-to-ruby/D2-150-…-assemblyinfo.cs | 11 | 10 | 1 | 0 | 0 | 3 |

**列口径**：「已读」= 逐行正文完整可读；「已读(截断)」= `returned-evidence/evidence-source.json`（单行 >2000 字符，只可读前 2000 字符）；「缺件」= job-00 应有而未落盘的 `report.json`、`report.md`、`controller.log`（各 1 件，共 3）。source-only 预检不要求 `evidence-target.json`/`comparison.json`/`job-01`（评估准备 §1.1）；0 模型调用不产生 `02-conversion`/`03-self-review`/根 `target`；非可转换去向按交付契约不要求 `evaluator_manifest.json`。本副本 10 项均无 `case.md`（该数据集未采用）且 `source/` 树已删（当前副本整体限制），不计入本列。

## 发现汇总（供 harness-b-findings.md 汇总）

1. **manifest 行号偏移与 23 个 ID 缺口** — 环境/装置｜依据：`docs/dataset-2/dataset-2-copy/manifest.csv` 共 278 行（表头 1 + 数据 277），ID 覆盖 D2-001…D2-300 但少 23 个号；D2-141 在第 140 行（≠任务书的 NN+1=142 行），D2-150 在第 149 行｜边界：只影响按号定位行，本块 10 个 ID 均存在、无缺行，未逐一枚举缺号。
2. **本块去向与 0 模型调用一致** — 已有规则落实｜依据：`items/D2-141..149.json` `disposition=SOURCE_DEPENDENCY_GAP`、`D2-150.json=PREPARATION_GAP`，全部 `usage.modelCalls=0`/`codeRevisions=0`/`selfRepairRounds=0`；`references/workflow/build-prerequisites.md` §5 行161-172（缺源自身依赖→源依赖缺口）；`AGENTS.md` §3「源构建失败…不消耗转换调用」｜边界：仅为去向与调用数一致性，不代表依赖判定/清理证据已核实。
3. **job-00 缺 Controller canonical report 与 controller.log** — 装置/缺件｜依据：10 项 `04-evaluation/job-00-source-buildability/` 无 `report.json`/`report.md`/`controller.log`/`controller-health-*.json`/`attribution.md`/`evidence-target.json`/`comparison.json`；对照 `references/framework/delivery-handoff-contract.md` §2.2 行181-188｜边界：source-only 预检不要求 target 证据/comparison（评估准备 §1.1 行31）；report/log 属应有件，未返回不伪造。
4. **evidence-source.json 单行截断致执行/清理不可读** — 装置/工具限制｜依据：10 份 `evidence-source.json` 单行 >2000 字符，可见仅到 `build` + stdout 前缀，`stderr`/`execution`/`cleanup`/`observations` 在截断区｜边界：`items.verdicts.environment="clean"` 无法由可见证据核对（待核验），不得据截断记为已读全文。
5. **batch-authorization 模板残留 D2-088** — 装置/记录｜依据：10 份 `batch-authorization.json` 行21 `dataSource.confirmation` 均写「该项 D2-088…」，与本项身份不符；对照 `references/workflow/classifier-agent-gate.md` §3 行59 要求按项记录授权｜边界：批次级授权复用本身合规（AGENTS §3），问题在逐项确认文本残留。
6. **D2-150 重分类后仍保留 public network target** — 装置/分类器｜依据：`D2-150/…/classification-2.json` 行31-51 仍 `network_mode:"public"`/`has_network:true`/`network_targets=[1.0.0.0(行35),1.0.0.0(行36)]`/`redirectVerified:false`，行115/127 `requiresNetworkIsolation:true`，同时行113/125 `admissionStatus:"ALLOWED"`；对照 `classifier-agent-gate.md` §2 行38｜边界：该项最终 PREPARATION_GAP、未执行，未消费该 ALLOWED；词法误判应由分类器侧修，不由 Agent 手改分类 JSON。
7. **D2-150 删除 BLOCKED classification-1** — 现行规则与历史处置不符｜依据：`frozen-inputs.md` 行20、`result.md` 行23、`items/D2-150.json` 行18 均记「误生成的 classification-1.json 已删除」；批次自设纪律见 `batch/optimization-inputs-2.md` §2.7 H7（行250）与 `batch/README.md` 行135；对照 `delivery-handoff-contract.md` §2.1.1 行90「已发生分类保留…原分类结果；重分类另存递增编号…不覆盖旧结果」、`task-state-contract.md` §1 行9｜边界：历史轮次已删，本会话无法读取该文件，只登记原件缺失与现行口径。
8. **D2-150 以「无入口」记 PREPARATION_GAP 与现行口径冲突** — 已有规则（现行文本）/知识候选｜依据：`frozen-inputs.md` 行15、`result.md` 行19、`items/D2-150.json` 行40 以「无入口/无自身可观察行为」记 PREPARATION_GAP 并跳过（引数据集自设「纪律 §65」，见 `batch/optimization-inputs-2.md` §2.3 行185-201、行261）；对照 `references/framework/task-state-contract.md` §3 行96「不因缺 main/可执行文件/stdout/合法评估入口直接记 PREPARATION_GAP 并跳过生成」与 `evaluation-readiness-contract.md` §1.3 行43-44｜边界：现行 LIB 分支要求「源可构建」，本项源构建 failed（见发现9），正确去向还取决于外壳修正或真实不可构建诊断，不能仅凭现行文本改判。
9. **D2-150 CS0579 属构建外壳归因** — 已有规则落实/环境-装置｜依据：`evidence-source.json` 可见 stdout 报 `error CS0579` 重复程序集属性，路径为 `source/obj/Release/net48/probe.AssemblyInfo.cs`，即 SDK 风格 `probe.csproj` 自动生成属性与手写 `AssemblyInfo.cs` 冲突；`items/D2-150.json` 行28 同述；对照 `references/workflow/build-prerequisites.md` §3 行109-124、§5 行161-172｜边界：`probe.csproj` 正文已随 source/ 树删除，无法复核；不得把外壳冲突的 failed 直接当作源字节不可构建。
10. **D2-143 行数不一致** — 待核验/原件不一致｜依据：`manifest.csv` D2-143 行（第142行）`Lines=62`，而 `frozen-inputs.md` 行7 与 `result.md` 行5 均记 74 行；源正文已删；D2-141=55、D2-142=63、D2-144=34 与 frozen 一致｜边界：只记不一致，不改 manifest，不单方面定案。
11. **SharpUp 依赖「快照外」与「数据集内未打包」需区分** — 未定/需核验｜依据：D2-141/142/144–149 依赖 `SharpUp.Classes`/`SharpUp.Utilities`/`VulnerabilityCheck`；D2-143 依赖 `SharpUp.Native.Win32` 且注明其源码在数据集内为另一独立项 D2-133（`frozen-inputs.md` 行18）；对照 `references/workflow/build-prerequisites.md` §0.1 行40-50 与 D2-025 打包完整性段 行50｜边界：按「本项单文件快照」口径成立，但被依赖源在数据集内存在，需 manifest 层明确快照根后再复核；不补造依赖、不直接改判。
12. **items casePath 旧路径 + manifest Evidence/JobId 未更新** — 装置/记录一致性｜依据：`items/D2-141..150.json` `casePath` 均为 `docs/test/dataset-2/...`，实际副本为 `docs/dataset-2/dataset-2-copy/...`；`manifest.csv` D2-141–150 的 `Evidence` 仍 "UNVERIFIED (not built, not run)"、`JobId` 空，而 items 已记 `buildStatus=failed`/`exitCode=1`/jobId｜边界：历史指针/旧标签不改，只登记可检查性与终态记录不一致。
13. **身份/哈希逐项对应可核（正面事实）** — 原件支持｜依据：10 项 manifest `Sha256` 与 `classifier-input.json` 的 `sourceSha256`（大写）、`classification-*`/`this-task-classification.json` 的 `details.files[].sha256`（小写）、item `sourceSha256`（小写）逐项一致；`this-task-classification.json` 等于该 job 目录当前分类件（D2-150 为 classification-2）｜边界：只证身份/哈希对应，不代表源已构建、可评估或清理已确认。

## 逐项记录

### D2-141 / csharp-to-python / TokenPrivileges.cs

**实际目录**：`docs/dataset-2/dataset-2-copy/csharp-to-python/D2-141-cs-.upstream-sharpup-sharpup-checks-tokenprivileges.cs`
**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读，35 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：无（不适用，0 模型调用）。
- 03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`batch-authorization.json`（已读）、`comparison_manifest.json`（已读）、`input_profile.json`（已读）、`metadata.json`（已读）、`this-task-classification.json`（已读）、`job-id.txt`（已读）、`returned-evidence/evidence-source.json`（**已读(截断)**）。
- 根层：`result.md`（已读）；`evaluator_manifest.json` 缺（非可转换去向不要求）。
**身份/版本关联**：taskId/rawItemId `D2-141`；batchId `batch`；direction `csharp-to-python`；kind NEW；disposition `SOURCE_DEPENDENCY_GAP`；phase `CLOSED_SOURCE_DEPENDENCY_GAP`；lifecycle `DONE`；sourceSha256 `883a7865…3721`（=manifest）；finalTargetSha256 无（未生成 target）；classifier.version `2.4`、sha256 `009a6f31…f3a4`；jobId `eval-20261011-150834-4ee3438c`；model 无（0 调用）；runner `windows-vm-agent-x64`；snapshot `CC-Eval-Windows-8Lang-1.0.28`；agentVersion/collectorVersion `1.0.0`；`toolchainFingerprint={}`；frozen 未列 selected skills/知识哈希（缺）。
**冻结/分类**：frozen 记 direction、sourceOs=targetOs=`windows`(x64)、源 55 行、sha `883A7865…`；分类 `admissionStatus=ALLOWED`、`blockingReason=null`、`cls=REVIEW_UNCERTAIN`、`reason=lexical_coverage_incomplete`、`reviewGroups=[process]`，覆盖 `source/` 三文件（TokenPrivileges.cs/probe.csproj/run_case.py）；`executionApproved=true`（兼容字段，未复制到 manifest）。无 classification-2/3。冻结哈希与 item/manifest 一致。
**源预检**：job-00 `eval-20261011-150834-4ee3438c`；`comparison_manifest.source.buildCommand="dotnet build -c Release probe.csproj"`（item 记 net48）；`evidence-source`（可见部分）`build.status=failed`、`exitCode=1`、`durationMs=9637`，stdout 报 `CS0234 SharpUp.Classes`、`CS0234 SharpUp.Native`、`CS0246 VulnerabilityCheck`；无运行基线（execution=blocked）；清理依据在截断区，不可读。
**模型请求/响应**：无 `request.system.txt`、无 `target.gen.*`/`.model.json`（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无 `attempt-*`、无 `job-00b/c`；唯一失败事实是源 build failed（CS0234/CS0246）。
**自审**：无 `review.system.txt`、无 `self-review-*.json`（未生成）；不适用。
**job 证据**：job-00 仅 7 件（见清单）；无 `report.json`/`report.md`/`controller.log`/`controller-health`/`attribution.md`/`evidence-target.json`/`comparison.json`；`metadata.json` 记 `targetArtifact="target/target.py (placeholder)"`、`targetHash="sha256:placeholder-precheck"`。
**result / evaluator manifest**：`result.md` 记去向 `SOURCE_DEPENDENCY_GAP`、未生成目标、0 模型调用、编译器诊断与长路径装置注意；`evaluator_manifest.json` 缺（非可转换去向不要求）。
**batch/items**：`batch/items/D2-141.json`：disposition `SOURCE_DEPENDENCY_GAP`、phase `CLOSED_SOURCE_DEPENDENCY_GAP`、lifecycle `DONE`、sourcePrecheck{jobId, buildStatus failed, exitCode 1, execution blocked}、verdicts{sourceBuild FAILED, targetBuild not attempted, comparison n/a, environment clean, safety ALLOWED}、coverageGaps 1 条、codeRevisions 0、selfRepairRounds 0、usage{requests 0, modelCalls 0}、blockingReasons[SOURCE_DEPENDENCY_GAP]；无 failedAttempts/datasetAnomaly/contractNote。
**独立证据事实与限制**：原件支持 = 源 build failed/exitCode 1 与 CS0234/CS0246（可见 stdout）；历史说明 = SOURCE_DEPENDENCY_GAP（result/item）；当前规则对照 = build-prerequisites §0.1/§5；待核验 = execution/cleanup/observations（截断）、`environment:"clean"`。
**分类归入**：已有规则落实（build-prerequisites §5 行161-172）；未定/需核验（发现11）。

### D2-142 / csharp-to-python / UnquotedServicePath.cs

**实际目录**：`docs/dataset-2/dataset-2-copy/csharp-to-python/D2-142-cs-.upstream-sharpup-sharpup-checks-unquotedservicepath.cs`
**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读 34 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：无（不适用）。03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`metadata.json`、`this-task-classification.json`、`job-id.txt`（均已读）、`returned-evidence/evidence-source.json`（**已读(截断)**）。
- 根层：`result.md`（已读）；`evaluator_manifest.json` 缺（不要求）。
**身份/版本关联**：taskId `D2-142`；batchId `batch`；direction `csharp-to-python`；kind NEW；disposition `SOURCE_DEPENDENCY_GAP`；phase `CLOSED_SOURCE_DEPENDENCY_GAP`；lifecycle `DONE`；sourceSha256 `e872763c…ae9b`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`；jobId `eval-20261011-150939-016fff9f`；runner `windows-vm-agent-x64`；snapshot `CC-Eval-Windows-8Lang-1.0.28`；agentVersion `1.0.0`；`toolchainFingerprint={}`；frozen 未列知识哈希（缺）。
**冻结/分类**：源 63 行、sha `E872763C…`；分类 `ALLOWED`/`null`、`cls=REVIEW_UNCERTAIN`、`reviewGroups=[process, sensitive]`、`requiresSyntheticData=true`（sensitive 命中）；覆盖 `source/` 三文件；无重分类。哈希与 manifest/item 一致。
**源预检**：job-00 `eval-20261011-150939-016fff9f`；build failed/exitCode 1/durationMs 10885；stdout 报 `CS0234 SharpUp.Classes`、`CS0234 SharpUp.Utilities`、`CS0246 VulnerabilityCheck`；execution blocked；清理不可读。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无 attempt 文件；唯一失败为源 build failed。
**自审**：无（未生成）；不适用。
**job 证据**：job-00 7 件；无 report.json/report.md/controller.log/health/attribution/证据 target/comparison；`metadata.targetArtifact="target/target.py (placeholder)"`。
**result / evaluator manifest**：`result.md` 记 SOURCE_DEPENDENCY_GAP、未生成、0 调用、诊断；manifest 缺（不要求）。
**batch/items**：`D2-142.json` 同 D2-141 结构（disposition/phase/lifecycle、sourcePrecheck jobId、verdicts、coverageGaps、codeRevisions 0、selfRepairRounds 0、usage 0/0、blockingReasons[SOURCE_DEPENDENCY_GAP]）；无 failedAttempts/datasetAnomaly/contractNote。
**独立证据事实与限制**：原件支持 = build failed/exitCode 1 + 上述 CS 诊断；历史说明 = 依赖缺口；当前规则对照 = build-prerequisites §0.1/§5；待核验 = execution/cleanup（截断）、`requiresSyntheticData=true` 未被消费（未执行）。
**分类归入**：已有规则落实；装置（`batch-authorization` 的 D2-088 残留，发现5）。

### D2-143 / csharp-to-python / IdentityUtils.cs

**实际目录**：`docs/dataset-2/dataset-2-copy/csharp-to-python/D2-143-cs-.upstream-sharpup-sharpup-utilities-identityutils.cs`
**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读 37 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：无（不适用）。03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`metadata.json`、`this-task-classification.json`、`job-id.txt`（均已读）、`returned-evidence/evidence-source.json`（**已读(截断)**）。
- 根层：`result.md`（已读）；`evaluator_manifest.json` 缺（不要求）。
**身份/版本关联**：taskId `D2-143`；direction `csharp-to-python`；kind NEW；disposition `SOURCE_DEPENDENCY_GAP`；phase `CLOSED_SOURCE_DEPENDENCY_GAP`；lifecycle `DONE`；sourceSha256 `3f969d27…1a1b`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`；jobId `eval-20261011-151051-ed22bd5a`；runner `windows-vm-agent-x64`；snapshot `CC-Eval-Windows-8Lang-1.0.28`；agentVersion `1.0.0`；`toolchainFingerprint={}`；frozen 未列知识哈希（缺）。
**冻结/分类**：frozen 行7 记源 **74 行**（manifest 记 62，见发现10）、sha `3F969D27…`；分类 `ALLOWED`/`null`、`cls=REVIEW_UNCERTAIN`、`reviewGroups=[process]`；覆盖 `source/` 三文件；无重分类。分类哈希与 manifest/item 一致。
**源预检**：job-00 `eval-20261011-151051-ed22bd5a`；build failed/exitCode 1/durationMs 8944；stdout 仅 1 个错误 `CS0234 SharpUp.Native`（IdentityUtils.cs(7,22)），`sizeBytes=888`、`truncated=false`；execution blocked；清理不可读。根因记 `using static SharpUp.Native.Win32`，并注明 `SharpUp.Native.Win32` 源码在数据集内为另一独立项 `D2-133`（`frozen` 行18）——见发现11。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无。
**自审**：无（未生成）；不适用。
**job 证据**：job-00 7 件；无 report/log/health/attribution/证据 target/comparison；`metadata.targetArtifact` placeholder。
**result / evaluator manifest**：`result.md` 记 SOURCE_DEPENDENCY_GAP、未生成、0 调用、诊断，并记方向收口「csharp-to-python 7/7（D2-137~D2-143）全部 SOURCE_DEPENDENCY_GAP」；manifest 缺（不要求）。
**batch/items**：`D2-143.json` 结构同前；coverageGaps 记依赖 `SharpUp.Native.Win32`；无 failedAttempts/datasetAnomaly/contractNote。
**独立证据事实与限制**：原件支持 = build failed/exitCode 1 + `CS0234 SharpUp.Native`（可见 stdout，含 sizeBytes/digest）；历史说明 = 依赖缺口、方向收口；当前规则对照 = build-prerequisites §0.1；待核验 = 行数 62/74、execution/cleanup。
**分类归入**：待核验/原件不一致（行数，发现10）；未定/需核验（快照外 vs 数据集内，发现11）；已有规则落实（去向）。

### D2-144 / csharp-to-ruby / HijackablePaths.cs

**实际目录**：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-144-cs-.upstream-sharpup-sharpup-checks-hijackablepaths.cs`
**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读 34 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：无（不适用）。03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`metadata.json`、`this-task-classification.json`、`job-id.txt`（均已读）、`returned-evidence/evidence-source.json`（**已读(截断)**）。
- 根层：`result.md`（已读）；`evaluator_manifest.json` 缺（不要求）。
**身份/版本关联**：taskId `D2-144`；direction **`csharp-to-ruby`**；kind NEW；disposition `SOURCE_DEPENDENCY_GAP`；phase `CLOSED_SOURCE_DEPENDENCY_GAP`；lifecycle `DONE`；sourceSha256 `40b15b03…bfd0`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`；jobId `eval-20261011-151223-dc21347d`；runner `windows-vm-agent-x64`；snapshot `CC-Eval-Windows-8Lang-1.0.28`；agentVersion `1.0.0`；`toolchainFingerprint={}`；frozen 未列知识哈希（缺）。target build 声明为 `ruby -c target.rb`（未执行）。
**冻结/分类**：源 34 行、sha `40B15B03…`；分类 `ALLOWED`/`null`、`cls=REVIEW_UNCERTAIN`、`reviewGroups=[process]`；覆盖 `source/` 三文件；无重分类。哈希一致。
**源预检**：job-00 `eval-20261011-151223-dc21347d`；build failed/exitCode 1/durationMs 3578；stdout 报 `CS0234 SharpUp.Classes`、`CS0234 SharpUp.Utilities`×2 起；execution blocked；清理不可读。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无。
**自审**：无（未生成）；不适用。
**job 证据**：job-00 7 件；`comparison_manifest.target.artifactLanguage="ruby"`、`buildCommand="ruby -c target.rb"`（前向声明，未执行）；无 report/log/health/attribution/证据 target/comparison。
**result / evaluator manifest**：`result.md` 记 SOURCE_DEPENDENCY_GAP、未生成、0 调用、诊断（临时短目录打包）；manifest 缺（不要求）。
**batch/items**：`D2-144.json` 结构同前；coverageGaps 1 条；无 failedAttempts/datasetAnomaly/contractNote。
**独立证据事实与限制**：原件支持 = build failed/exitCode 1 + CS 诊断；历史说明 = 依赖缺口；当前规则对照 = build-prerequisites §0.1/§5；待核验 = execution/cleanup（截断）、target 从未生成。
**分类归入**：已有规则落实；装置（D2-088 残留、缺 report/log）。

### D2-145 / csharp-to-ruby / McAfeeSitelistFiles.cs

**实际目录**：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-145-cs-.upstream-sharpup-sharpup-checks-mcafeesitelistfiles.cs`
**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读 27 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：无（不适用）。03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`metadata.json`、`this-task-classification.json`、`job-id.txt`（均已读）、`returned-evidence/evidence-source.json`（**已读(截断)**）。
- 根层：`result.md`（已读）；`evaluator_manifest.json` 缺（不要求）。
**身份/版本关联**：taskId `D2-145`；direction `csharp-to-ruby`；disposition `SOURCE_DEPENDENCY_GAP`；phase `CLOSED_SOURCE_DEPENDENCY_GAP`；lifecycle `DONE`；sourceSha256 `0ecb98a1…c0be`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`；jobId `eval-20261011-151329-9b5ce315`；runner `windows-vm-agent-x64`；snapshot `CC-Eval-Windows-8Lang-1.0.28`；agentVersion `1.0.0`；`toolchainFingerprint={}`；frozen 未列行数与知识哈希（缺）。
**冻结/分类**：源 sha `0ECB98A1…`（frozen 未记行数）；分类 `ALLOWED`/`null`、`cls=REVIEW_UNCERTAIN`、`reviewGroups=[discovery, process]`、signals.discovery=[12]、process=[2,3,4,5,12]；覆盖 `source/` 三文件；无重分类。哈希一致。
**源预检**：job-00 `eval-20261011-151329-9b5ce315`；build failed/exitCode 1/durationMs 4288；stdout 报 `CS0234 SharpUp.Classes`、`CS0234 SharpUp.Utilities`、`CS0246 VulnerabilityCheck`；execution blocked；清理不可读。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无。
**自审**：无（未生成）；不适用。
**job 证据**：job-00 7 件；无 report/log/health/attribution/证据 target/comparison。
**result / evaluator manifest**：`result.md` 记 SOURCE_DEPENDENCY_GAP、未生成、0 调用、诊断；manifest 缺（不要求）。
**batch/items**：`D2-145.json` 结构同前；coverageGaps 1 条；无 failedAttempts/datasetAnomaly/contractNote。
**独立证据事实与限制**：原件支持 = build failed/exitCode 1 + CS 诊断；历史说明 = 依赖缺口；当前规则对照 = build-prerequisites §0.1/§5；待核验 = execution/cleanup（截断）。
**分类归入**：已有规则落实；装置（frozen 未记行数、D2-088 残留）。

### D2-146 / csharp-to-ruby / ModifiableServiceBinaries.cs

**实际目录**：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-146-cs-.upstream-sharpup-sharpup-checks-modifiableservicebinaries.cs`
**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读 27 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：无（不适用）。03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`metadata.json`、`this-task-classification.json`、`job-id.txt`（均已读）、`returned-evidence/evidence-source.json`（**已读(截断)**）。
- 根层：`result.md`（已读）；`evaluator_manifest.json` 缺（不要求）。
**身份/版本关联**：taskId `D2-146`；direction `csharp-to-ruby`；disposition `SOURCE_DEPENDENCY_GAP`；phase `CLOSED_SOURCE_DEPENDENCY_GAP`；lifecycle `DONE`；sourceSha256 `45be4bf3…8ce69`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`；jobId `eval-20261011-151435-4332e13d`；runner `windows-vm-agent-x64`；snapshot `CC-Eval-Windows-8Lang-1.0.28`；agentVersion `1.0.0`；`toolchainFingerprint={}`；frozen 未列行数与知识哈希（缺）。
**冻结/分类**：源 sha `45BE4BF3…`（frozen 未记行数，manifest 42）；分类 `ALLOWED`/`null`、`cls=REVIEW_UNCERTAIN`、`reviewGroups=[process]`；覆盖 `source/` 三文件；无重分类。哈希一致。
**源预检**：job-00 `eval-20261011-151435-4332e13d`；build failed/exitCode 1/durationMs 12733；stdout 报 `CS0234 SharpUp.Classes`、`CS0234 SharpUp.Utilities`、`CS0246 VulnerabilityCheck`；execution blocked；清理不可读。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无。
**自审**：无（未生成）；不适用。
**job 证据**：job-00 7 件；无 report/log/health/attribution/证据 target/comparison。
**result / evaluator manifest**：`result.md` 记 SOURCE_DEPENDENCY_GAP、未生成、0 调用、诊断；manifest 缺（不要求）。
**batch/items**：`D2-146.json` 结构同前；coverageGaps 1 条；无 failedAttempts/datasetAnomaly/contractNote。
**独立证据事实与限制**：原件支持 = build failed/exitCode 1 + CS 诊断；历史说明 = 依赖缺口；当前规则对照 = build-prerequisites §0.1/§5；待核验 = execution/cleanup（截断）。
**分类归入**：已有规则落实；装置（D2-088 残留、缺 report/log）。

### D2-147 / csharp-to-ruby / RegistryAutoLogons.cs

**实际目录**：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-147-cs-.upstream-sharpup-sharpup-checks-registryautologons.cs`
**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读 27 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：无（不适用）。03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`metadata.json`、`this-task-classification.json`、`job-id.txt`（均已读）、`returned-evidence/evidence-source.json`（**已读(截断)**）。
- 根层：`result.md`（已读）；`evaluator_manifest.json` 缺（不要求）。
**身份/版本关联**：taskId `D2-147`；direction `csharp-to-ruby`；disposition `SOURCE_DEPENDENCY_GAP`；phase `CLOSED_SOURCE_DEPENDENCY_GAP`；lifecycle `DONE`；sourceSha256 `0c9d8ae7…8e0b`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`；jobId `eval-20261011-151542-70fef793`；runner `windows-vm-agent-x64`；snapshot `CC-Eval-Windows-8Lang-1.0.28`；agentVersion `1.0.0`；`toolchainFingerprint={}`；frozen 未列行数与知识哈希（缺）。
**冻结/分类**：源 sha `0C9D8AE7…`（frozen 未记行数，manifest 45）；分类 `ALLOWED`/`null`、`cls=REVIEW_UNCERTAIN`、`reviewGroups=[process]`；覆盖 `source/` 三文件；无重分类。哈希一致。
**源预检**：job-00 `eval-20261011-151542-70fef793`；build failed/exitCode 1/durationMs 9671；stdout 报 `CS0234 SharpUp.Classes`、`CS0234 SharpUp.Utilities`、`CS0246 VulnerabilityCheck`；execution blocked；清理不可读。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无。
**自审**：无（未生成）；不适用。
**job 证据**：job-00 7 件；无 report/log/health/attribution/证据 target/comparison。
**result / evaluator manifest**：`result.md` 记 SOURCE_DEPENDENCY_GAP、未生成、0 调用、诊断；manifest 缺（不要求）。
**batch/items**：`D2-147.json` 结构同前；coverageGaps 1 条；无 failedAttempts/datasetAnomaly/contractNote。
**独立证据事实与限制**：原件支持 = build failed/exitCode 1 + CS 诊断；历史说明 = 依赖缺口；当前规则对照 = build-prerequisites §0.1/§5；待核验 = execution/cleanup（截断）。
**分类归入**：已有规则落实；装置（frozen 未记行数、D2-088 残留）。

### D2-148 / csharp-to-ruby / RegistryAutoruns.cs

**实际目录**：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-148-cs-.upstream-sharpup-sharpup-checks-registryautoruns.cs`
**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读 27 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：无（不适用）。03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`metadata.json`、`this-task-classification.json`、`job-id.txt`（均已读）、`returned-evidence/evidence-source.json`（**已读(截断)**）。
- 根层：`result.md`（已读）；`evaluator_manifest.json` 缺（不要求）。
**身份/版本关联**：taskId `D2-148`；direction `csharp-to-ruby`；disposition `SOURCE_DEPENDENCY_GAP`；phase `CLOSED_SOURCE_DEPENDENCY_GAP`；lifecycle `DONE`；sourceSha256 `27182c93…aee5`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`；jobId `eval-20261011-151648-bec8fa68`；runner `windows-vm-agent-x64`；snapshot `CC-Eval-Windows-8Lang-1.0.28`；agentVersion `1.0.0`；`toolchainFingerprint={}`；frozen 未列行数与知识哈希（缺）。
**冻结/分类**：源 sha `27182C93…`（frozen 未记行数，manifest 45）；分类 `ALLOWED`/`null`、`cls=REVIEW_UNCERTAIN`、`reviewGroups=[process]`；覆盖 `source/` 三文件；无重分类。哈希一致。
**源预检**：job-00 `eval-20261011-151648-bec8fa68`；build failed/exitCode 1/durationMs 11899；stdout 报 `CS0234 SharpUp.Classes`、`CS0234 SharpUp.Utilities`×2 起；execution blocked；清理不可读。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无。
**自审**：无（未生成）；不适用。
**job 证据**：job-00 7 件；无 report/log/health/attribution/证据 target/comparison。
**result / evaluator manifest**：`result.md` 记 SOURCE_DEPENDENCY_GAP、未生成、0 调用、诊断；manifest 缺（不要求）。
**batch/items**：`D2-148.json` 结构同前；coverageGaps 1 条；无 failedAttempts/datasetAnomaly/contractNote。
**独立证据事实与限制**：原件支持 = build failed/exitCode 1 + CS 诊断；历史说明 = 依赖缺口；当前规则对照 = build-prerequisites §0.1/§5；待核验 = execution/cleanup（截断）。
**分类归入**：已有规则落实；装置（frozen 未记行数、D2-088 残留）。

### D2-149 / csharp-to-ruby / UnattendedInstallFiles.cs

**实际目录**：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-149-cs-.upstream-sharpup-sharpup-checks-unattendedinstallfiles.cs`
**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读 27 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：无（不适用）。03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`metadata.json`、`this-task-classification.json`、`job-id.txt`（均已读）、`returned-evidence/evidence-source.json`（**已读(截断)**）。
- 根层：`result.md`（已读）；`evaluator_manifest.json` 缺（不要求）。
**身份/版本关联**：taskId `D2-149`；direction `csharp-to-ruby`；disposition `SOURCE_DEPENDENCY_GAP`；phase `CLOSED_SOURCE_DEPENDENCY_GAP`；lifecycle `DONE`；sourceSha256 `a294822f…de96`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`；jobId `eval-20261011-151754-9448ffb7`；runner `windows-vm-agent-x64`；snapshot `CC-Eval-Windows-8Lang-1.0.28`；agentVersion `1.0.0`；`toolchainFingerprint={}`；frozen 未列行数与知识哈希（缺）。
**冻结/分类**：源 sha `A294822F…`（frozen 未记行数，manifest 36）；分类 `ALLOWED`/`null`、`cls=REVIEW_UNCERTAIN`、`reviewGroups=[discovery, process]`、signals.discovery=[11]、process=[2,3,4,5,11,30]；覆盖 `source/` 三文件；无重分类。哈希一致。
**源预检**：job-00 `eval-20261011-151754-9448ffb7`；build failed/exitCode 1/durationMs 10702；stdout 报 `CS0234 SharpUp.Classes`、`CS0246 VulnerabilityCheck`；execution blocked；清理不可读。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无。
**自审**：无（未生成）；不适用。
**job 证据**：job-00 7 件；无 report/log/health/attribution/证据 target/comparison。
**result / evaluator manifest**：`result.md` 记 SOURCE_DEPENDENCY_GAP、未生成、0 调用、诊断；manifest 缺（不要求）。
**batch/items**：`D2-149.json` 结构同前；coverageGaps 1 条；无 failedAttempts/datasetAnomaly/contractNote。
**独立证据事实与限制**：原件支持 = build failed/exitCode 1 + CS 诊断；历史说明 = 依赖缺口；当前规则对照 = build-prerequisites §0.1/§5；待核验 = execution/cleanup（截断）。
**分类归入**：已有规则落实；装置（frozen 未记行数、D2-088 残留）。

### D2-150 / csharp-to-ruby / AssemblyInfo.cs

**实际目录**：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-150-cs-.upstream-sharpup-sharpup-properties-assemblyinfo.cs`
**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读 29 行）、`classifier-input.json`（已读）、**`classification-2.json`（已读；无 classification-1，已删，见发现7）**。
- 02-conversion：无（不适用）。03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`metadata.json`、`this-task-classification.json`、`job-id.txt`（均已读）、`returned-evidence/evidence-source.json`（**已读(截断)**）。
- 根层：`result.md`（已读）；`evaluator_manifest.json` 缺（不要求）。
**身份/版本关联**：taskId `D2-150`；direction `csharp-to-ruby`；kind NEW；disposition **`PREPARATION_GAP`**；phase `CLOSED_PREPARATION_GAP`；lifecycle `DONE`；sourceSha256 `3b11406a…ea29f`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`；jobId `eval-20261011-151917-5aa4c0b3`；runner `windows-vm-agent-x64`；snapshot `CC-Eval-Windows-8Lang-1.0.28`；agentVersion `1.0.0`；`toolchainFingerprint={}`；frozen 未列知识哈希（缺）。
**冻结/分类**：源 sha `3B11406A…`（纯程序集元数据，无类型/方法）；`classification-2.json` `admissionStatus=ALLOWED`/`blockingReason=null`、`cls=REVIEW_UNCERTAIN`，但保留 `network_mode:"public"`、`has_network:true`、`network_targets=[1.0.0.0(行35),1.0.0.0(行36)]`、`requiresNetworkIsolation:true`（发现6）；`this-task-classification.json` = classification-2（一致）。frozen 行20 记「误生成的 classification-1.json 已删除」（发现7）。哈希与 item/manifest 一致。
**源预检**：job-00 `eval-20261011-151917-5aa4c0b3`；build failed/exitCode 1/durationMs 7715；stdout 报 `error CS0579` 重复程序集属性（来自 `source/obj/Release/net48/probe.AssemblyInfo.cs`，即 SDK 风格 probe.csproj 自动属性与手写 AssemblyInfo.cs 冲突，发现9）；execution blocked；清理不可读。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无 `attempt-*`；重分类以 `--network-isolation-configured` 加 `classification-2.json` 落盘（旧 classification-1 删除）。
**自审**：无（未生成）；不适用。
**job 证据**：job-00 7 件；`metadata.json` 行6 `safetyClassification="…(see classification-1)"`（指向已删文件，发现7/12 类）；`targetArtifact` placeholder；无 report/log/health/attribution/证据 target/comparison。
**result / evaluator manifest**：`result.md` 记 PREPARATION_GAP（无入口 + 无自身可观察行为）、未生成、0 调用、CS0579 诊断与词法误判附注、方向收口（csharp-to-ruby 7/7：6 SOURCE_DEPENDENCY_GAP + 1 PREPARATION_GAP）；manifest 缺（不要求）。
**batch/items**：`D2-150.json`：disposition `PREPARATION_GAP`、phase `CLOSED_PREPARATION_GAP`、lifecycle `DONE`、classifier.note 记词法误判与删除 classification-1、sourcePrecheck{jobId, buildStatus failed, exitCode 1, diagnostics[CS0579 duplicate assembly attributes]}、verdicts{sourceBuild FAILED, targetBuild not attempted, comparison n/a, environment clean, safety ALLOWED}、coverageGaps 1 条、codeRevisions 0、selfRepairRounds 0、usage{requests 0, modelCalls 0}、blockingReasons[PREPARATION_GAP]；无 failedAttempts/datasetAnomaly/contractNote。
**独立证据事实与限制**：原件支持 = build failed/exitCode 1 + CS0579（可见 stdout）；历史说明 = 无入口 ⇒ PREPARATION_GAP；当前规则对照 = task-state §3 行96、evaluation-readiness §1.3 行43-44（无入口不应直接记 PREPARATION_GAP）、build-prerequisites §3/§5（外壳归因）、delivery §2.1.1 行90（分类保留）；待核验 = 已删 classification-1、execution/cleanup（截断）、`safetyClassification` 旧指针。
**分类归入**：装置/分类器（词法误判、public target 残留，发现6）；现行规则与历史处置不符（删除分类件 发现7；无入口去向 发现8）；已有规则落实/环境-装置（CS0579 外壳归因，发现9）；知识候选（分类器版本号误判 IP，宜与 D2-121/D2-122 型合并核验，本会话未读那两项，标待核验）。

---

## 覆盖清单（D2-151–D2-160）

> 前文第 3 行的「后 10 项待续」由本段取代（追加式，不回改前文）。manifest 按内容定位：D2-151 在 manifest 第 150 行、D2-156 在第 155 行（行号 = Id−1；manifest 缺 23 个编号，不能用 Id+1 猜行）。

| 项 | 实际目录 | 现存文件数 | 已读 | 已读(截断) | 未读 | 空文件 | 缺件 |
|---|---|---|---|---|---|---|---|
| D2-151 | c-to-cpp/D2-151-c-c-rm.c | 41 | 35 | 6 | 0 | 0 | 3 |
| D2-152 | c-to-cpp/D2-152-c-c-du.c | 27 | 25 | 2 | 0 | 0 | 1 |
| D2-153 | c-to-cpp/D2-153-c-c-cp.c | 18 | 17 | 1 | 0 | 0 | 1 |
| D2-154 | c-to-cpp/D2-154-c-c-sort.c | 25 | 23 | 2 | 0 | 0 | 1 |
| D2-155 | c-to-cpp/D2-155-c-c-xargs.c | 23 | 21 | 2 | 0 | 0 | 1 |
| D2-156 | 无目录/无过程材料 | 0 | 0 | 0 | 0 | 0 | 2 |
| D2-157 | 无目录/无过程材料 | 0 | 0 | 0 | 0 | 0 | 2 |
| D2-158 | 无目录/无过程材料 | 0 | 0 | 0 | 0 | 0 | 2 |
| D2-159 | 无目录/无过程材料 | 0 | 0 | 0 | 0 | 0 | 2 |
| D2-160 | 无目录/无过程材料 | 0 | 0 | 0 | 0 | 0 | 2 |

**列口径**：「已读(截断)」= 单行 JSON >2000 字符，只读到前 2000 字符（本块全部为 `returned-evidence/evidence-source.json`、`evidence-target.json`、`evaluation_report.json`；截断点均在 `build`/`execution` 之后，`observations`/`cleanup` 在不可见区）。「缺件」：D2-151 = 根级 `target.cpp`、`02-conversion/target.gen.cpp`（模型稿正文）、`02-conversion/target.gen.raw.txt`（原始响应）——副本已删正文，`evaluator_manifest.json` 仍声明 `hasTranslatedCode=true`；D2-152–155 = `result.md`（交付契约 §2.1.1 行108/111 明确非可转换去向也须 result.md）；D2-156–160 = `frozen-inputs.md`（disposition=FROZEN 的必备件）与 `result.md`（WAITING 必备件）。10 项均无 `case.md`、无 `source/` 树、无根 `target`（D2-152+ 未生成），属当前副本整体限制；`docs/dataset-2/dataset-2-copy/c-to-csharp/**` glob **0 文件**，D2-156–160 在全副本内只有 `batch/items/*.json`。

## 发现汇总（本块，续前文编号）

14. **D2-152–155 全部缺 `result.md`** — 已有规则（现行文本）未落实｜依据：4 项 `output/batch/` 只有 `01-frozen/` 与 `04-evaluation/`；`*/D2-15*/output/batch/result.md` 只命中 D2-150/151；四份 `frozen-inputs.md` 明写「无 `result.md`（非可转换去向只要求适用件）」（D2-152 行73、D2-153 行63、D2-154 行46、D2-155 行39）；对照 `delivery-handoff-contract.md` §2.1.1 行108「非可转换去向…`result.md`（去向/原因、实际阶段与证据、适用件核对）」、行111「result.md 是所有已处理项的报告义务…不能写成目标转换失败」及 §1.1 行15｜边界：不补写历史报告，只登记缺档与现行口径冲突。
15. **D2-156–160 仍记 WAITING/BLOCKED_ENV，而 blocker 文件已宣告修复** — 现行规则/记录与历史处置不符｜依据：`batch/platform-blocker-csharp-target.md` 行3–9「✅ 已修复（2026-10-11 复测）…jobId `eval-20261011-122249-fe456bbe` → `COMPLETED`…恢复条件已满足 ⇒ 38 项 C# 目标项可恢复为正常推进，**不必**再记 `WAITING/BLOCKED_ENV`」；而 `items/D2-156..160.json` 仍 `disposition=FROZEN`/`phase=NOT_STARTED`/`lifecycle=WAITING`/`blockingReasons=[BLOCKED_ENV]`/`pendingAction="re-submit…after the platform fixes…"`、`dispositionNote` 记「user ruling 2026-10-11（skip C#-target directions）」｜边界：不代行恢复、不改历史标签；恢复须另按任务状态 §2.2 重核冻结/分类/预检。
16. **D2-156–160 `disposition=FROZEN` 无 `frozen-inputs.md`** — 已有规则未落实｜依据：`task-state-contract.md` §3 行87「FROZEN 转换边界已在本 run 的 `frozen-inputs.md` 落盘且回读通过」、`delivery-handoff-contract.md` §2.1.1 行90；`c-to-csharp/**` glob 0 文件；item `dispositionNote` 自述「no freeze job was run」｜边界：FROZEN 标签与实物不符，本块不改标签，只记缺件。
17. **D2-152/D2-153 manifest 行数与 frozen 不一致** — 待核验/原件不一致｜依据：manifest 第151行 D2-152 `Lines=502`、第152行 D2-153 `Lines=564`；对应 `frozen-inputs.md` 记 `sourceLines` 561（D2-152 行7）、606（D2-153 行7）；而同块 D2-151=510、D2-154=1151、D2-155=742 三处 manifest 与 frozen 一致｜边界：源正文已删，不能定案哪个准确，也不改 manifest。
18. **D2-152–155 的 job 级 `batch-authorization.json` 逐项确认文本复写 D2-151** — 装置/记录｜依据：7 份（D2-152 job-00/job-00b、D2-153 job-00、D2-154 job-00/job-00b、D2-155 job-00/job-00b）`dataSource.confirmation` 行21 均写「该项 **D2-151** 无网络、无凭证, 仅本地文件删除与只读遍历, 使用合成 fixture (keep.txt/second.txt)」；对照 `classifier-agent-gate.md` §3 行59「复用已有合法授权，记录来源、范围、有效期…按项记录授权」｜边界：批次授权复用本身合规（AGENTS §3），问题在逐项身份文本残留。
19. **D2-155 job-00b 目标构建命令拼写错误 `gcc++`** — 装置/契约｜依据：`job-00b-source-buildability-linux/comparison_manifest.json` 行16 `"buildCommand": "gcc++ -std=gnu++17 target.cpp -o program"`（D2-154 job-00b 同位置为 `g++`；D2-152 job-00b 亦为 `g++`）｜边界：该项源构建先失败、目标侧 `preflight=SKIPPED`（未执行），故未造成实际影响；仍属提交 capsule 的目标契约笔误。
20. **D2-155 分类为 `REVIEW_SENSITIVE`，其 job metadata 仍写 `REVIEW_UNCERTAIN`** — 装置/记录不一致｜依据：D2-155 `classification-1.json` 行6/`this-task-classification.json` 行5/item 均 `cls=REVIEW_SENSITIVE`、`reason=sensitive_or_dynamic_operations`；而 job-00 与 job-00b 的 `metadata.json` 行6 均 `"safetyClassification":"classifier-2.4 ALLOWED blockingReason=null cls=REVIEW_UNCERTAIN"`（D2-151/152/153/154 的 metadata 与其 cls 一致）｜边界：ALLOWED 判定未变；另该项 `signals.sensitive=[]`，标签由 `dynamic_code=[597,604]` 触发，措辞与实际信号不符，标待核验。
21. **D2-153 分类 `has_network=true`/`network_mode="unresolved"` 但 `requiresNetworkIsolation=false`** — 分类器/待核验｜依据：`classification-1.json` 行19–39 `signals.network=[574]`、`network_mode:"unresolved"`、`has_network:true`、`network_targets:[]`、`requiresNetworkIsolation:false`；`metadata.json` 与 item 均称「no network」｜边界：无目标地址且未执行；词法命中是否误报不能由本次静态审阅定案，不改分类 JSON。
22. **D2-151 job-00 用占位 target 全量双跑，其 `codeVerdict=failed`/`behaviorVerdict=mismatched` 未在 result/item 披露** — 原件支持/报告缺口｜依据：`job-00/returned-evidence/evaluation_report.json` `outcome.runVerdict="partial-runnable"`、`codeVerdict="failed"`、`behaviorVerdict="mismatched"`；`comparison.json` output（target stdout 空）与 filesystem（target 未删 fixture）均 mismatched；`metadata.json` 记 `targetArtifact="target/target.cpp (placeholder)"`、`targetHash="sha256:placeholder-precheck"`；而 `result.md` §4 只写源侧 completed/0，item.verdicts 只记 job-01｜边界：占位件不是转换交付，该 mismatched 不记转换失败（同前文 D2-001 型旧预检装置）；但历史 job 结论未进入本项报告，属披露缺口。
23. **D2-151 生成期目标方言（`c++17`）与冻结/评估方言（`gnu++17`）不一致，且 frozen 方言注记时间晚于两个 job** — 原件支持/待核验｜依据：`02-conversion/request.system.txt` 行21 写「目标工具链…`clang++ -std=c++17 target.cpp -o program`」，`job-00/comparison_manifest.json` target 同为 `c++17`；`frozen-inputs.md` 行41–43 与 `job-01/comparison_manifest.json` target 为 `gnu++17`，frozen 行42 注「方言依据（冻结期修订，**2026-10-11**）」；而两个 job 回执时间为 2026-10-10T15:53/16:04（`controller.log`）｜边界：`gnu++17` 是 `c++17` 超集、本次目标与源逐字节相同（`job-01/metadata.json` targetHash `2a54532c…c1e81`），影响面小；「冻结期即写明、非失败后补救」与请求正文/时间线不符，标待核验，不据此改结论。
24. **D2-151 item 内部计数不一致** — 待核验/记录｜依据：`items/D2-151.json` `usage.failedAttempts=0` 而顶层 `failedAttempts` 数组 1 条（403 `identity_mismatch`）；`codeRevisions=1` 而 `selfRepairRounds=0`、`result.md` §3 记「**无代码修订**」、`02-conversion/` 只有一份 `target.gen.model.json` 且无 `target.self-repair-*`｜边界：`attempt-1-403.json` 只有 `detail`（无 HTTP 状态码/时间/提交 caseId），「403」与 legacy caseId 归因来自 item 记述，原件不可核。
25. **D2-151 的 403 `identity_mismatch` 印证现行身份门禁（正面事实）** — 已有规则落实｜依据：`attempt-1-403.json` `blockingReason:"identity_mismatch"`、action「re-classify the exact submitted sources (content/direction/case must match)」；item 记原 caseId `batch-d2-151-c-to-cpp-rm`，改 `D2-151` 后接受（202）；对照 `classifier-agent-gate.md` §3 行47「`caseId` 必须等于 classification `case`」｜边界：只证身份引用修正，不代隔离或构建结论。
26. **D2-159 `utils.c` 引用仓库内不存在的 `extern.h`（跨项历史说明）** — 未定/需核验｜依据：D2-153 `frozen-inputs.md` 行59 记穷举核对结果「引用它的源文件…c-to-csharp/D2-159 utils.c…**无任何 extern.h 实体**」；而 `items/D2-159.json` 记 `disposition=FROZEN`（declared convertible）｜边界：D2-159 源正文已删，本次无法复核；若恢复推进，源预检预期落在 `SOURCE_DEPENDENCY_GAP`（`build-prerequisites.md` §0.1 行40–50）。
27. **manifest `JobId` 空、`Evidence` 旧标签 + item `casePath` 旧路径（D2-151–160）** — 装置/记录一致性｜依据：manifest 第150–159行 JobId 列全空、Evidence 均 `UNVERIFIED (not built, not run)`，而 D2-151 item 已记 jobId 且 result 记 completed/matched；10 份 item `casePath` 均为 `docs/test/dataset-2/...`，副本实际为 `docs/dataset-2/dataset-2-copy/...`｜边界：沿用前文发现12，不改历史指针/标签。
28. **身份/哈希逐项对应可核（正面事实）** — 原件支持｜依据：D2-151–160 manifest `Sha256`（大写）与 `classifier-input.json`（D2-151–155）、`classification-1.json` `details.files[].sha256`（小写）、item `sourceSha256`（小写）逐项一致；`this-task-classification.json` 与该 job 目录当前 `classification-1.json` 内容一致（D2-151/152/153/154/155 逐项比对相同）；D2-151 的两个 jobId 与 result/item 对应｜边界：只证身份/哈希对应，不代表源可构建、可评估或清理已确认。

## 逐项记录

### D2-151 / c-to-cpp / rm.c（BSD userland）

**实际目录**：`docs/dataset-2/dataset-2-copy/c-to-cpp/D2-151-c-c-rm.c`
**文件清单与读取状态（41）**：
- 01-frozen：`frozen-inputs.md`（已读 82 行）、`classifier-input.json`（已读）、`classification-1.json`（已读 169 行）。
- 02-conversion：`request.system.txt`（已读 29 行）、`target.gen.model.json`（**已读，24 行；形制①调用元数据，无 content**）。
- 03-self-review：`review.system.txt`（已读 25 行）、`self-review-1.json`（已读 105 行，11 条）、`self-review-1.model.json`（已读 19 行，元数据）。
- 04-evaluation/job-00-source-buildability（16）：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`、`attempt-1-403.json`（均已读）、`returned-evidence/` 内 `comparison.json`、`controller.log`、`controller-health-after.json`、`evaluation_report.md`（均已读）、`evidence-source.json`、`evidence-target.json`、`evaluation_report.json`（**已读(截断)**）。
- 04-evaluation/job-01-dual-build（15）：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`（均已读）、`returned-evidence/` 内 `comparison.json`、`controller.log`、`controller-health-after.json`、`evaluation_report.md`（均已读）、`evidence-source.json`、`evidence-target.json`、`evaluation_report.json`（**已读(截断)**）。
- 根层：`result.md`（已读 59 行）、`evaluator_manifest.json`（已读 71 行）。
- 缺件：`target.cpp`、`02-conversion/target.gen.cpp`、`02-conversion/target.gen.raw.txt`（副本已删正文）。

**身份/版本关联**：taskId/rawItemId `D2-151`；batchId `batch`；direction `c-to-cpp`；kind NEW；disposition `CONVERTED`；phase `CLOSED`；lifecycle `DONE`；sourceSha256 `6471c9ff…68ba7`（=manifest 大写）；finalTargetSha256 `2a54532c16f0…c1e81`；classifier.version `2.4`、sha256 `009a6f31…f3a4`、cls `REVIEW_UNCERTAIN`、admission `ALLOWED`/`blockingReason=null`；jobId `eval-20261010-155343-a0e19246`（job-00）、`eval-20261010-160404-3a944b0d`（job-01）；model `deepseek-flash` temp=0.2、RAG off、不送 `max_tokens`；runner `macos-vm-agent-x64`；vmName `macos-eval`；baselineSnapshot `CC-Eval-Mac-7Lang-1.0.28-AutoLogin`；agentVersion/collectorVersion `1.0.0`、`toolchainFingerprint={}`；frozen 列 5 份知识及哈希（c-to-cpp 方向 `025e27f2…`、c `a170e963…`、cpp `e58e55a9…`、共性语义 `eb15af4c…`、scenes/file-io `3c326db4…`）。
**冻结/分类**：frozen 记 direction、sourceOs=targetOs=`macos`(x64)、源 510 行/13109 B、sha 大写、casePath/sourcePath 旧 `docs/test/...`；sourceBuild `clang -std=gnu11 rm.c -o program`、targetBuild `clang++ -std=gnu++17 target.cpp -o program`；driver 一次性程序 + 自然退出、冻结 argv `["-v","keep.txt","second.txt"]`、stdin null、fixture 两侧同名同内容、oracle 需功能评估（output+filesystem，`filesystem.include` 显式列举）、异常登记未声明的 `Invoke-CredentialPhisher.ps1`（38225 B）按用户裁决排除。分类覆盖 `source/` 四文件（keep.txt、rm.c、run_case.py、second.txt），reviewGroups=[discovery,dynamic_code,filesystem,process]，`requiresSyntheticData=true`、`requiresNetworkIsolation=false`、`executionApproved=true`（兼容字段）。无 classification-2/3。哈希与 item/manifest 一致。
**源预检（job-00）**：jobId `eval-20261010-155343-a0e19246`；`comparison_manifest.source.buildCommand="clang -std=gnu11 rm.c -o program"`，target 为 `clang++ -std=c++17`（占位件）；`evidence-source`（可见部分）`build.status=completed`、`exitCode=0`、`durationMs=12991`、stdout/stderr 空；`execution.status=completed`、`exitCode=0`、`durationMs=2393`、stdout `keep.txt\nsecond.txt\n`（20 B、digest `329fd412…`）；`evidence-target`（截断可见）占位件 build/execution 均 completed/0、stdout 空；`comparison.json` `behaviorVerdict=mismatched`（output/filesystem 各 major diffs）；report `runVerdict="partial-runnable"`、`codeVerdict="failed"`、`behaviorVerdict="mismatched"`、`environmentStatus="clean"`、两侧 lifecycle preflight/cleanup PASSED（见发现22）。清理依据在截断区（`observations`/`cleanup` 不可读）。
**模型请求/响应**：`request.system.txt` 为 C→C++ 转换系统提示（含 21 行「目标工具链…`-std=c++17`」）；`target.gen.model.json` 记 stage GENERATED、round 1、finishReason stop、requestSha256 `3002c816…`、systemPromptSha256 `666d0970…`、userPromptSha256 `51d5b42c…`、rawResponseSha256 `f8f98792…`、outputSha256 `2a54532c…`、outputBytes 12561、outputLines 550、usage prompt 6335/completion 46713/reasoning 42285/total 53048、`maxTokensFieldSent=false`；**无原响应正文文件（`target.gen.raw.txt` 缺）**，不能从哈希还原。
**失败/废弃/重提 attempt**：`job-00/attempt-1-403.json` 仅 `{"detail":{"error":"admission_blocked","blockingReason":"identity_mismatch",…}}`（无 HTTP 状态/时间戳）；item 记 attempt 1 http 403、cause = legacy caseId `batch-d2-151-c-to-cpp-rm`、resolution 改 `D2-151` 后接受；无 `job-00b/00c`、无 repair attempt。
**自审**：`review.system.txt` 为独立静态审阅提示（10 项清单 + 裸 JSON 输出约定）；`self-review-1.json` `verdict="NO-REPAIR-IDENTIFIED"`，11 条逐条：id1–10 origin `source-preexisting`「未发现问题」（目标与源逐字相同、选项串/usage/checkdot/rm_file/check/rm_tree/check2/错误形态均一致），id11 origin `toolchain-unknown`（`-std=c++17` 下 macOS 是否暴露 `strmode`/`fflagstostr`/`undelete`/`lchflags`/`SIGINFO`）→ 无 `conversion-introduced` 条目；`self-review-1.model.json` 记 reviewN 1、requestSha256 `6f7d56c6…`、rawResponseSha256 `f3c656cc…`、reviewSha256 `14fe46a2…`、usage prompt 10244/completion 33752/reasoning 29174、verdict 同上。
**job 证据（job-01）**：jobId `eval-20261010-160404-3a944b0d`；source/target build、execution 均 completed/0（source build 7832 ms/exec 1639 ms、target build 3478 ms/exec 798 ms）；两侧 stdout normalizedText `keep.txt\nsecond.txt\n`、digest `329fd412…`、20 B、stderr 空；`comparison.json` `behaviorVerdict="matched"`、output/filesystem 均 matched、diffs=0、processes/registry/network not-applicable；report `runVerdict="runnable"`、`codeVerdict="passed"`、coverage 2/2、`environmentStatus="clean"`、两侧 preflight/cleanup PASSED、runnerStateAfter READY、contaminated false；`controller.log` created 16:04:04 / finished 16:07:16；health before/after 均 `status=ok`、`contractSetHash=sha256:a9ed1445…`、3 runner READY。
**result / evaluator manifest**：`result.md` 五栏齐；结论速览记「交付完整性=已完成 / 语法编译=通过 / 功能一致性=约定范围内匹配」；§3 记 BSD userland 判定口径更正（macOS 可构建，旧 `SOURCE_NOT_BUILDABLE` 仅实测 windows+linux）；§4 记覆盖缺口 4 类；§5 列口径更正、覆盖缺口、数据集异常。`evaluator_manifest.json` kind `third-party-evaluator-manifest`、generatedBy hand-authored、languagePair c→cpp、taskMetadata macos/macos x64、sceneTags [file-io]、riskLevel low、`files[0].success=true`/`artifacts.hasTranslatedCode=true`、`x_adapter.executionApproved=true`、jobId、status `converted-and-evaluated`；路径指针指向 `docs/test/...` 旧绝对路径（该机 `Administrator.DESKTOP-LRHSLVD`）。
**batch/items**：`items/D2-151.json` 全字段：disposition `CONVERTED`、phase `CLOSED`、lifecycle `DONE`、classifier{version,admissionStatus,blockingReason,cls,sha256,note}、sourcePrecheck{jobId,os,buildCommand,buildStatus completed,exitCode 0,verdict SOURCE_BUILDABLE,note}、dualBuildJobId、verdicts{sourceBuild `completed/0`、targetBuild `completed/0 (PASS…)`、execution、comparison `matched`、environment clean、safety ALLOWED}、finalTargetSha256、blockingReasons[]、codeRevisions 1、selfRepairRounds 0、coverageGap、datasetAnomaly、contractNote、failedAttempts[1]、usage{promptTokens 16579、completionTokens 80465、reasoningTokens 71459、requests 2、model deepseek-flash、failedAttempts 0}。
**独立证据事实与限制**：原件支持 = job-01 两侧 build/execution completed/0、stdout 逐字节相同、comparison matched、cleanup PASSED、coverage 2/2；job-00 源侧 completed/0；403 身份拒收原件；历史说明 = item/result 记 `CONVERTED`/匹配与覆盖缺口；当前规则对照 = `classifier-agent-gate` §3 行47（identity）、`evaluation-readiness` §1.1/§5、`delivery` §2.1.1；待核验 = 6 份截断 JSON 的 `observations`/`cleanup`、`target.cpp`/原响应缺失、403 原件缺状态码、frozen 方言注记日期与 job 时间线（发现23）、item 计数（发现24）。
**分类归入**：已有规则落实（身份门禁 发现25）；装置/记录（job-00 占位 mismatched 未披露 发现22；item 计数/403 原件 发现24；manifest 旧标签 发现27）；待核验（方言时间线 发现23）；知识候选 = 无（自审 id11 属工具链可见性，非新增知识规则）。
**去向**：`CONVERTED`（matched，冻结 argv 路径）。

### D2-152 / c-to-cpp / du.c（BSD userland）

**实际目录**：`docs/dataset-2/dataset-2-copy/c-to-cpp/D2-152-c-c-du.c`
**文件清单与读取状态（27）**：
- 01-frozen：`frozen-inputs.md`（已读 73 行，含追加的「源侧预检定案」节）、`classifier-input.json`（已读）、`classification-1.json`（已读 143 行）。
- 02-conversion / 03-self-review / 根层：无（0 模型调用、非可转换去向）。
- 04-evaluation/job-00-source-buildability（14）：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`（均已读）、`returned-evidence/` 内 `comparison.json`、`controller.log`、`evaluation_report.md.md`（**双扩展名**）、`evaluation_report.json`、`evidence-target.json`（均已读）、`evidence-source.json`（**已读(截断)**）。
- 04-evaluation/job-00b-source-buildability-linux（10）：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`（均已读）、`returned-evidence/` 内 `controller.log`、`evaluation_report.json`、`evidence-target.json`（均已读）、`evidence-source.json`（**已读(截断)**）。
- 缺件：`result.md`（发现14）。

**身份/版本关联**：taskId/rawItemId `D2-152`；batchId `batch`；direction `c-to-cpp`；kind NEW；disposition `SOURCE_NOT_BUILDABLE`；phase `SOURCE_PRECHECK_FAILED`；lifecycle `DONE`；sourceSha256 `0a769a7f…2a6f3e`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`、cls `REVIEW_UNCERTAIN`、admission `ALLOWED`/null；jobIds `eval-20261010-160959-ad9b9812`（macos）、`eval-20261010-161200-73e6da10`（linux）；model 无（0 调用）；runner `macos-vm-agent-x64` / `linux-vm-agent-x64`；vmName `macos-eval` / `linux-eval`；snapshot `CC-Eval-Mac-7Lang-1.0.28-AutoLogin` / `CC-Eval-Linux-8Lang-1.0.28`；agentVersion `1.0.0`、`toolchainFingerprint={}`；frozen 列 5 份知识及哈希（同 D2-151）。
**冻结/分类**：frozen 记 sourceOs 候选 macos（后追加 linux 实验）、targetOs macos、源 561 行/13637 B、sha 大写、sourceBuild `clang -std=gnu11 du.c`、targetBuild `clang++ -std=gnu++17`；driver 一次性程序、argv `["-A","-s","tree"]`、fixture `tree/one.txt`+`tree/two.txt`、oracle 需功能评估（仅 output；`-A` 用 `st_size` 避免块分配差异）；追加节定案两个候选均因 `libutil.h` 失败。分类覆盖 `source/` 四文件（du.c、run_case.py、one.txt、two.txt），reviewGroups=[process]，`requiresSyntheticData=false`、`requiresNetworkIsolation=false`、`executionApproved=true`。哈希与 item/manifest 一致；**manifest Lines 502 vs frozen 561（发现17）**。
**源预检**：job-00（macos，`clang -std=gnu11 du.c -o program`）`evidence-source`（可见）`build.status=failed`、`exitCode=1`、`durationMs=2888`、stderr `du.c:55:10: fatal error: 'libutil.h' file not found`（113 B、digest `ce440e38…`）；`execution.status=blocked`、stderr `build failed`；`comparison.json={"detail":"comparison_not_found"}`、`evidence-target.json={"detail":"evidence_not_found"}`；report `jobStatus=COMPLETED`、`jobPhase=RUNNING_SOURCE`、`runVerdict="blocked"`、`codeVerdict/behaviorVerdict="inconclusive"`、coverage 0/0、target preflight/cleanup SKIPPED、environment clean。job-00b（linux，`gcc -std=gnu11`）`build.status=failed`、`exitCode=1`、`durationMs=410`、stderr `du.c:55:10: fatal error: libutil.h: No such file or directory`（144 B、digest `637c1fff…`）；execution blocked；report 同形 blocked/inconclusive、jobPhase RUNNING_SOURCE。清理依据在截断区，不可读。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无 `attempt-*`；两次候选预检即两候选 job（非重提）。
**自审**：无 `review.system.txt`、无 `self-review-*`；不适用。
**job 证据**：job-00 仅 14 件（无 job 根 `report.json`/`report.md`）；job-00b 10 件（无 `runners-before.json`/health）；两份 `controller.log` 记 created/finished（16:09:59→16:11:33；16:12:00→16:12:38）；`comparison.json` 为 `comparison_not_found`、`evidence-target.json` 为 `evidence_not_found`（真错误占位，非证据）。
**result / evaluator manifest**：两者均缺（非可转换去向不要求 target/evaluator manifest；但 `result.md` 按现行交付契约仍是报告义务，见发现14）。
**batch/items**：`items/D2-152.json`：disposition `SOURCE_NOT_BUILDABLE`、phase `SOURCE_PRECHECK_FAILED`、lifecycle `DONE`、classifier{…}、sourcePrecheck{experimentA{jobId,os macos,buildCommand,buildStatus failed,exitCode 1,diagnostic `'libutil.h' file not found`},experimentB{jobId,os linux,buildCommand gcc,buildStatus failed,exitCode 1,diagnostic},verdict,detail}、verdicts{sourceBuild `failed/1 (SOURCE_NOT_BUILDABLE)`、targetBuild/execution/comparison `UNVERIFIED`、environment n/a、safety ALLOWED}、blockingReasons[]、codeRevisions 0、selfRepairRounds 0、usage{requests 0,note}。
**独立证据事实与限制**：原件支持 = 两候选 build failed/1 与 `libutil.h` 诊断（macos 113 B、linux 144 B）；job-00 report blocked/inconclusive、coverage 0、target SKIPPED；历史说明 = item/frozen 记 SOURCE_NOT_BUILDABLE（非转换失败）；当前规则对照 = `build-prerequisites` §0.1/§5、`task-state` §3 行91、`evaluation-readiness` §1.1 行31（source-only 不要求 target 证据）；待核验 = manifest/frozen 行数差（发现17）、截断区 cleanup/observations、`batch-authorization` 身份残留（发现18）。
**分类归入**：已有规则落实（两候选实测 → SOURCE_NOT_BUILDABLE）；装置/记录（缺 result.md 发现14；行数 发现17；authorization 残留 发现18；`evaluation_report.md.md` 双扩展名）。

### D2-153 / c-to-cpp / cp.c（BSD userland）

**实际目录**：`docs/dataset-2/dataset-2-copy/c-to-cpp/D2-153-c-c-cp.c`
**文件清单与读取状态（18）**：
- 01-frozen：`frozen-inputs.md`（已读 63 行，含追加定案节）、`classifier-input.json`（已读）、`classification-1.json`（已读 126 行）。
- 02-conversion / 03-self-review / 根层：无。
- 04-evaluation/job-00-source-buildability（15）：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`（均已读）、`returned-evidence/` 内 `comparison.json`、`controller.log`、`controller-health-after.json`、`evaluation_report.json`、`evaluation_report.md`、`evidence-target.json`（均已读）、`evidence-source.json`（**已读(截断)**）。
- 缺件：`result.md`（发现14）。

**身份/版本关联**：taskId/rawItemId `D2-153`；direction `c-to-cpp`；kind NEW；disposition `SOURCE_DEPENDENCY_GAP`；phase `SOURCE_PRECHECK_FAILED`；lifecycle `DONE`；sourceSha256 `f0a176d9…3a30`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`、cls `REVIEW_UNCERTAIN`；jobId `eval-20261010-161342-140dff76`；runner `macos-vm-agent-x64`、vmName `macos-eval`、snapshot `CC-Eval-Mac-7Lang-1.0.28-AutoLogin`；agentVersion `1.0.0`；0 模型调用；frozen 未逐条列知识哈希（写「同 D2-151」5 份）。
**冻结/分类**：frozen 记源 606 行/16923 B、sha 大写、sourceBuild `clang -std=gnu11 cp.c`、targetBuild `clang++ -std=gnu++17`；driver 一次性程序、argv `["-v","src.txt","dst.txt"]`、fixture `src.txt`、oracle output+filesystem（`include=["dst.txt"]`）；追加定案：`cp.c:76 #include "extern.h"` 缺失，按 §9 穷举（`find -name extern.h` 全工作区 0 命中，内容搜仅命中引用者 cp.c、c-to-csharp/D2-159 utils.c、c-to-powershell/D2-170 cmp.c、c-to-go/D2-165 tr.c），旧 `docs/test/dataset` 亦 0 → SOURCE_DEPENDENCY_GAP。分类覆盖 `source/` 三文件（cp.c、run_case.py、src.txt）；reviewGroups=[filesystem,network,process]；**cp.c `signals.network=[574]`、`network_mode="unresolved"`、`has_network=true`、`network_targets=[]`、`requiresNetworkIsolation=false`（发现21）**；`requiresSyntheticData=false`。哈希与 item/manifest 一致；**manifest Lines 564 vs frozen 606（发现17）**。
**源预检**：job-00 `evidence-source`（可见）`build.status=failed`、`exitCode=1`、`durationMs=4313`、stderr `cp.c:76:10: fatal error: 'extern.h' file not found`（110 B、digest `0061a7db…`）；`execution.status=blocked`；`comparison.json={"detail":"comparison_not_found"}`、`evidence-target.json={"detail":"evidence_not_found"}`；report `jobStatus=COMPLETED`、`jobPhase=RUNNING_SOURCE`、runVerdict blocked、code/behavior inconclusive、coverage 0/0、target preflight/cleanup SKIPPED、environment clean；`controller.log` 16:13:42→16:15:17；health before/after `status=ok` 3 runner READY。
**模型请求/响应**：无（0 模型调用）；不适用。
**失败/废弃/重提 attempt**：无 `attempt-*`；唯一失败为源 build failed（extern.h）。
**自审**：无；不适用。
**job 证据**：job-00 15 件；无 job 根 `report.json`/`report.md`；`evaluation_report.md` 记 Source「Execution performed: yes」而 evidence `execution.status=blocked`，措辞与底层证据不符（报告视图与原始证据差异，记录不改）。
**result / evaluator manifest**：两者均缺（报告义务见发现14）。
**batch/items**：`items/D2-153.json`：disposition `SOURCE_DEPENDENCY_GAP`、phase `SOURCE_PRECHECK_FAILED`、lifecycle `DONE`、classifier{…}、sourcePrecheck{jobId,os,buildCommand,buildStatus failed,exitCode 1,diagnostic `'extern.h' file not found`,verdict,detail（含 §9 穷举结果与 D2-159/170/165 交叉引用）}、verdicts{sourceBuild failed/1、targetBuild/execution/comparison UNVERIFIED、environment n/a、safety ALLOWED}、blockingReasons[]、codeRevisions 0、selfRepairRounds 0、usage{requests 0}。
**独立证据事实与限制**：原件支持 = build failed/1 + `extern.h` 引号包含诊断（110 B）；历史说明 = item/frozen 记依赖缺口与 §9 穷举；当前规则对照 = `build-prerequisites` §0.1 行45–50（快照内漏打包 ≠ 快照外依赖；引号包含属项目伴随文件）、§5；待核验 = 行数差（发现17）、cp.c 网络信号（发现21）、截断区 cleanup、穷举过程的执行方式（历史说明，无法复核命令本体）。
**分类归入**：已有规则落实（依赖缺口分列）；分类器/待核验（has_network/unresolved 与 requiresNetworkIsolation=false，发现21）；装置/记录（缺 result.md 发现14、行数 发现17、authorization 残留 发现18）；未定/需核验（D2-159 交叉引用 发现26）。

### D2-154 / c-to-cpp / sort.c（BSD userland，>700 行）

**实际目录**：`docs/dataset-2/dataset-2-copy/c-to-cpp/D2-154-c-c-sort.c`
**文件清单与读取状态（25）**：
- 01-frozen：`frozen-inputs.md`（已读 47 行，含追加定案节）、`classifier-input.json`（已读）、`classification-1.json`（已读 128 行）。
- 02-conversion / 03-self-review / 根层：无。
- 04-evaluation/job-00-source-buildability（11）：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`（均已读）、`returned-evidence/` 内 `controller.log`、`evaluation_report.json`、`evidence-target.json`（均已读）、`evidence-source.json`（**已读(截断)**）。无 `controller-health-*`。
- 04-evaluation/job-00b-source-buildability-linux（11）：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`（均已读）、`returned-evidence/` 内 `controller.log`、`evaluation_report.json`、`evidence-target.json`（均已读）、`evidence-source.json`（**已读(截断)**）。无 `controller-health-*`。
- 缺件：`result.md`（发现14）。

**身份/版本关联**：taskId/rawItemId `D2-154`；direction `c-to-cpp`；kind NEW；disposition `SOURCE_NOT_BUILDABLE`；phase `SOURCE_PRECHECK_FAILED`；lifecycle `DONE`；sourceSha256 `86dc5d29…e8d43f`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`、cls `REVIEW_UNCERTAIN`；jobIds `eval-20261010-161605-c5701444`（macos）、`eval-20261010-161745-8485dc6a`（linux）；runner `macos-vm-agent-x64` / `linux-vm-agent-x64`；vmName `macos-eval` / `linux-eval`；snapshot Mac/Linux 1.0.28；0 模型调用；frozen 记 selected skills 同 D2-151。
**冻结/分类**：frozen 记源 1151 行（**>700 计划上限**）、sha 大写、sourceBuild `clang -std=gnu11 sort.c`、targetBuild `clang++ -std=gnu++17`；driver 一次性程序、argv `["in.txt"]`、fixture `in.txt`、oracle output（本项未走到该步）；追加定案：A macos `md5.h` 缺失、B linux `sys/sysctl.h` 缺失，两候选均 FreeBSD 专有接口 ⇒ SOURCE_NOT_BUILDABLE。分类覆盖 `source/` 三文件（in.txt、run_case.py、sort.c）；reviewGroups=[discovery,filesystem,process]；sort.c signals.filesystem=[227,926,1322,1323]、discovery=[336,369]；`requiresSyntheticData=false`。哈希与 item/manifest 一致（manifest Lines 1151 = frozen）。
**源预检**：job-00（macos）`build.status=failed`、`exitCode=1`、`durationMs=4503`、stderr `sort.c:41:10: fatal error: 'md5.h' file not found`（103 B、digest `25d9aa9b…`）、`execution.status=blocked`；job-00b（linux）`build.status=failed`、`exitCode=1`、`durationMs=121`、stderr `sort.c:32:10: fatal error: sys/sysctl.h: No such file or directory`（155 B、digest `a7ae2bd7…`）、`execution.status=blocked`；两 job `evidence-target.json={"detail":"evidence_not_found"}`、report 均 `jobPhase=RUNNING_SOURCE`、runVerdict blocked、code/behavior inconclusive、coverage 0/0、target SKIPPED、environment clean；`controller.log` 16:16:05→16:17:40、16:17:45→16:18:14。
**模型请求/响应 / 失败重提 / 自审**：均无（0 模型调用、0 自审、无 attempt）。
**job 证据**：两 job 均无 job 根 `report.json`/`report.md`、无 `controller-health-*`；cleanup/observations 在截断区。
**result / evaluator manifest / batch/items**：`result.md`、`evaluator_manifest.json` 缺；`items/D2-154.json`：disposition `SOURCE_NOT_BUILDABLE`、phase `SOURCE_PRECHECK_FAILED`、lifecycle `DONE`、classifier{…}、sourcePrecheck{experimentA/experimentB + verdict + detail}、verdicts{sourceBuild failed/1、其余 UNVERIFIED、environment n/a、safety ALLOWED}、blockingReasons[]、codeRevisions 0、selfRepairRounds 0、`note`（1151 行超 700、长文件流程未触发）、usage{requests 0}。
**独立证据事实与限制**：原件支持 = 两候选 build failed/1 与 `md5.h`/`sys/sysctl.h` 诊断；历史说明 = item/frozen 记 SOURCE_NOT_BUILDABLE 与「长文件能力未验证」；当前规则对照 = `build-prerequisites` §0.1/§5、`task-state` §3 行91；待核验 = 截断区 cleanup、无 health 快照、长文件流程的说明只属未触发。
**分类归入**：已有规则落实（两候选实测）；装置/记录（缺 result.md 发现14、authorization 残留 发现18、无 health 快照）；正面边界 = 未把「阻塞于源预检」说成长文件能力已验证。

### D2-155 / c-to-cpp / xargs.c（BSD userland，含 exec）

**实际目录**：`docs/dataset-2/dataset-2-copy/c-to-cpp/D2-155-c-c-xargs.c`
**文件清单与读取状态（23）**：
- 01-frozen：`frozen-inputs.md`（已读 39 行，含追加定案节）、`classifier-input.json`（已读）、`classification-1.json`（已读 106 行）。
- 02-conversion / 03-self-review / 根层：无。
- 04-evaluation/job-00-source-buildability（10）：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`（均已读）、`returned-evidence/` 内 `controller.log`、`evaluation_report.json`、`evidence-target.json`（均已读）、`evidence-source.json`（**已读(截断)**）。无 `runners-before.json`/`controller-health-*`。
- 04-evaluation/job-00b-source-buildability-linux（10）：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`（均已读）、`returned-evidence/` 内 `controller.log`、`evaluation_report.json`、`evidence-target.json`（均已读）、`evidence-source.json`（**已读(截断)**）。无 `runners-before.json`/`controller-health-*`。
- 缺件：`result.md`（发现14）。

**身份/版本关联**：taskId/rawItemId `D2-155`；direction `c-to-cpp`；kind NEW；disposition `SOURCE_NOT_BUILDABLE`；phase `SOURCE_PRECHECK_FAILED`；lifecycle `DONE`；sourceSha256 `ef921dd8…c4d963`（=manifest）；finalTargetSha256 无；classifier.version `2.4`、sha `009a6f31…f3a4`、cls **`REVIEW_SENSITIVE`**（reason `sensitive_or_dynamic_operations`）、admission `ALLOWED`/null；jobIds `eval-20261010-161844-877305b4`（macos）、`eval-20261010-162032-5bd1e07e`（linux）；runner macos/linux；vmName `macos-eval`/`linux-eval`；snapshot Mac/Linux 1.0.28；0 模型调用；frozen 记 selected skills 加 `scenes/process-execution`。
**冻结/分类**：frozen 记源 742 行、sha 大写、sourceBuild `clang -std=gnu11 xargs.c`、targetBuild `clang++ -std=gnu++17`；sceneTags [file-io, process-execution]；driver 一次性程序、argv `["echo","probe"]`、stdin null、oracle output（可能加 processes，未走到）；追加定案：A/B 同在 L52 缺 FreeBSD 专有 `<sys/limits.h>`。分类覆盖 `source/` 两文件（run_case.py、xargs.c）；reviewGroups=[discovery,dynamic_code,filesystem,process]；xargs.c signals.filesystem=[612,615,790]、discovery=[100,128]、**dynamic_code=[597,604]**、`signals.sensitive=[]`；`requiresSyntheticData=true`。哈希与 item/manifest 一致（manifest Lines 742 = frozen）。
**源预检**：job-00（macos）`build.status=failed`、`exitCode=1`、`durationMs=4172`、stderr `xargs.c:52:10: fatal error: 'sys/limits.h' file not found`（125 B、digest `881f0470…`）；job-00b（linux）`build.status=failed`、`exitCode=1`、`durationMs=118`、stderr `xargs.c:52:10: fatal error: sys/limits.h: No such file or directory`（156 B、digest `1b17941a…`）；两 job `execution.status=blocked`、`evidence-target.json={"detail":"evidence_not_found"}`、report `jobPhase=RUNNING_SOURCE`、blocked/inconclusive、coverage 0/0、target SKIPPED；`controller.log` 16:18:44→16:20:19、16:20:32→16:21:01；**job-00b `comparison_manifest.target.buildCommand="gcc++ …"`（发现19）**；两 job `metadata.safetyClassification` 写 `REVIEW_UNCERTAIN`（发现20）。
**模型请求/响应 / 失败重提 / 自审**：均无（0 模型调用、0 自审、无 attempt）。
**job 证据**：两 job 均无 job 根 `report.json`/`report.md`、无 `runners-before.json`/`controller-health-*`；cleanup/observations 截断不可见。
**result / evaluator manifest / batch/items**：`result.md`、`evaluator_manifest.json` 缺；`items/D2-155.json`：disposition `SOURCE_NOT_BUILDABLE`、phase `SOURCE_PRECHECK_FAILED`、lifecycle `DONE`、classifier{version,admissionStatus,blockingReason,cls `REVIEW_SENSITIVE`,sha256}、sourcePrecheck{experimentA/experimentB+verdict+detail}、verdicts{sourceBuild failed/1、其余 UNVERIFIED、environment n/a、safety ALLOWED}、blockingReasons[]、codeRevisions 0、selfRepairRounds 0、usage{requests 0}。
**独立证据事实与限制**：原件支持 = 两候选 build failed/1 与同点 `sys/limits.h` 诊断；历史说明 = item/frozen 记 SOURCE_NOT_BUILDABLE；当前规则对照 = `build-prerequisites` §0.1/§5（FreeBSD 专有头属系统接口缺失）；待核验 = 截断区 cleanup、`gcc++` 笔误的实际影响（目标侧 SKIPPED）、`REVIEW_SENSITIVE` 与空 sensitive 信号。
**分类归入**：已有规则落实（两候选实测）；装置/记录（`gcc++` 发现19、cls 文本不一致 发现20、缺 result.md 发现14、authorization 残留 发现18）；分类器/待核验（敏感标签触发面）。

### D2-156 / c-to-csharp / mv.c（无过程材料）

**实际目录**：glob `docs/dataset-2/dataset-2-copy/**/D2-156*` 只命中 `batch/items/D2-156.json`；`docs/dataset-2/dataset-2-copy/c-to-csharp/**` **0 文件**；无法由 glob 区分「空目录」与「无目录」，如实记**无过程材料**。
**文件清单与读取状态**：过程材料 0 件；已读 `batch/items/D2-156.json`（31 行）与 manifest 第155行。
**身份/版本关联**：taskId/rawItemId `D2-156`；batchId `batch`；direction `c-to-csharp`；targetLang `csharp`；kind NEW；disposition `FROZEN`；phase `NOT_STARTED`；lifecycle `WAITING`；pendingAction「re-submit original contract after the platform fixes the C# target evidence-bundle schema」；blockingReasons `[BLOCKED_ENV]`；blockerRef `batch/platform-blocker-csharp-target.md`；sourceSha256 `af0e7c1c…b2f273`（=manifest 小写）；finalTargetSha256 无；无 classifier/jobId/model/runner（0 调用）；`verdicts` 全 UNVERIFIED、`safety="not-classified"`。
**冻结/分类 / 源预检 / 模型请求 / 失败 attempt / 自审 / job 证据 / result**：均无对应实物（`frozen-inputs.md`、`classification-*`、`04-evaluation/*` 全缺）；`dispositionNote` 自述「no freeze job was run because the defect is already characterised」。
**batch/items 与 manifest**：见上；manifest 记 `c-to-csharp`、`mv.c`、Lines 477、Origin `测试用例c\c测试用例\持久化\mv.c`、JobId 空、Evidence `UNVERIFIED (not built, not run)`。`casePath` 为旧 `docs/test/dataset-2/...`。
**独立证据事实与限制**：原件支持 = item 字段（FROZEN/NOT_STARTED/WAITING/BLOCKED_ENV）与 blocker 文件；历史说明 = blocker 文件行3–9 记「✅ 已修复（2026-10-11）…恢复条件已满足，不必再记 WAITING/BLOCKED_ENV」（发现15）；当前规则对照 = `task-state` §3 行87（FROZEN 须有 frozen-inputs.md）、`delivery` §2.1.1 行109（WAITING 须 result.md）；待核验 = 目录是否存在、源正文已删。
**分类归入**：现行规则/记录与历史处置不符（发现15）；已有规则未落实（FROZEN 无冻结件 发现16、缺 result.md 发现14）；装置/记录（manifest/casePath 旧指针 发现27）。

### D2-157 / c-to-csharp / cat.c（无过程材料）

**实际目录/文件清单**：过程材料 0 件（同 D2-156 口径）；已读 `batch/items/D2-157.json`（31 行）与 manifest 第156行。
**身份/版本关联**：taskId/rawItemId `D2-157`；direction `c-to-csharp`；kind NEW；disposition `FROZEN`；phase `NOT_STARTED`；lifecycle `WAITING`；blockingReasons `[BLOCKED_ENV]`；blockerRef 同上；sourceSha256 `6cb897bf…aed8f7`（=manifest）；pendingAction 同 D2-156；无 classifier/job/model；0 模型调用、`safety="not-classified"`。
**冻结/分类 / 源预检 / 模型 / attempt / 自审 / job / result**：均无实物。
**batch/items 与 manifest**：manifest 第156行 `cat.c`、Lines 483、Origin `测试用例c\c测试用例\信息收集\cat.c`、JobId 空、Evidence 未更新；`casePath` 旧路径。
**独立证据事实与限制 / 分类归入**：与 D2-156 同（发现14/15/16/27）；无该项独有差异可核。

### D2-158 / c-to-csharp / cut.c（无过程材料）

**实际目录/文件清单**：过程材料 0 件；已读 `batch/items/D2-158.json`（31 行）与 manifest 第157行。
**身份/版本关联**：taskId/rawItemId `D2-158`；direction `c-to-csharp`；kind NEW；disposition `FROZEN`；phase `NOT_STARTED`；lifecycle `WAITING`；blockingReasons `[BLOCKED_ENV]`；sourceSha256 `f0e9f6f3…8c45dea`（=manifest）；其余同 D2-156（无 classifier/job/model；0 调用；safety 未分类）。
**冻结/分类 / 源预检 / 模型 / attempt / 自审 / job / result**：均无实物。
**batch/items 与 manifest**：manifest 第157行 `cut.c`、Lines 456、Origin `测试用例c\c测试用例\信息收集\cut.c`、JobId 空、Evidence 未更新；`casePath` 旧路径。
**独立证据事实与限制 / 分类归入**：同 D2-156（发现14/15/16/27）。

### D2-159 / c-to-csharp / utils.c（无过程材料）

**实际目录/文件清单**：过程材料 0 件；已读 `batch/items/D2-159.json`（31 行）与 manifest 第158行。
**身份/版本关联**：taskId/rawItemId `D2-159`；direction `c-to-csharp`；kind NEW；disposition `FROZEN`；phase `NOT_STARTED`；lifecycle `WAITING`；blockingReasons `[BLOCKED_ENV]`；sourceSha256 `228774b8…982cf25`（=manifest）；其余同 D2-156。
**冻结/分类 / 源预检 / 模型 / attempt / 自审 / job / result**：均无实物。
**batch/items 与 manifest**：manifest 第158行 `utils.c`、Lines 501、Origin `测试用例c\c测试用例\信息收集\utils.c`、JobId 空、Evidence 未更新；`casePath` 旧路径。
**独立证据事实与限制**：同 D2-156；**另**：D2-153 `frozen-inputs.md` 行59 记 utils.c 引用 `extern.h` 且仓库内无实体（发现26），若恢复推进预期先在源预检落 `SOURCE_DEPENDENCY_GAP`，与本项 `FROZEN`「declared convertible」相矛盾——源正文已删，标待核验。
**分类归入**：同 D2-156（发现14/15/16/27）；未定/需核验（发现26）。

### D2-160 / c-to-csharp / envopts.c（无过程材料）

**实际目录/文件清单**：过程材料 0 件；已读 `batch/items/D2-160.json`（31 行）与 manifest 第159行。
**身份/版本关联**：taskId/rawItemId `D2-160`；direction `c-to-csharp`；kind NEW；disposition `FROZEN`；phase `NOT_STARTED`；lifecycle `WAITING`；blockingReasons `[BLOCKED_ENV]`；sourceSha256 `f50db1b1…2d60c09`（=manifest）；其余同 D2-156。
**冻结/分类 / 源预检 / 模型 / attempt / 自审 / job / result**：均无实物。
**batch/items 与 manifest**：manifest 第159行 `envopts.c`、Lines 445、Origin `测试用例c\c测试用例\执行\envopts.c`、JobId 空、Evidence 未更新；`casePath` 旧路径。
**独立证据事实与限制 / 分类归入**：同 D2-156（发现14/15/16/27）。

**本块停止点**：D2-151–D2-160 共 10 项完成逐项静态审阅（134 件现存文件正文，其中 13 件受工具 2000 字符/行截断），下一项从 manifest D2-161 继续。未编译/运行/调用模型/分类器，未恢复已删源/目标正文，未修改除本追加段以外的任何内容。
