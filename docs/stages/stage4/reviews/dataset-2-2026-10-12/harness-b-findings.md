# DeepSeek harness B 发现汇总（D2-081–D2-160）

> 状态：**COMPLETE**（79/79 项逐项审阅完成；逐项文件清单见 `harness-b-coverage.md`〔COMPLETE〕）。所有发现均给出文件/行号或字段依据；未逐字读到的范围已标“已读(截断)”或“待核验”。本文件只做静态文本审阅，不构成任何编译、链接、启动或行为结论，也不改判任何平台 verdict。
> **重要更正（B-H6）**：分块会话自报的“现存文件数”有错（实测 D2-091 真值 42 而非 38、D2-093 真值 48 而非 53、D2-095 真值 32 而非 37），故覆盖计数一律以独立 `glob` 为准。
> 范围：`docs/dataset-2/dataset-2-copy/manifest.csv` 的 D2-081 至 D2-160。该 Id 区间在 manifest 中实际只有 **79 行**（**D2-113 不存在**）。
> 方法与边界：纯静态文本审阅；不编译/不运行/不调用模型/不提交/不访问 Controller；原源与目标已删除，不复原。逐项证据见 `harness-b-cases-01.md`…`harness-b-cases-04.md`，逐项文件清单与读取状态见 `harness-b-coverage.md`。
> 分类标签：`知识新增` / `已有规则落实` / `错误建议` / `源已有` / `环境` / `装置` / `未定`。历史问题若现行规则已解决，只列依据，不重复当新故障。

## 0. 本会话工具与环境限制（影响“已读”与若干“缺件”判读）

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-H1 | 本会话 `pwsh` 在授予工作区写权限时失败（`SetNamedSecurityInfoW failed (Win32 5)`），`danger-full-access` 升级无审批通道 ⇒ `Get-Content`/目录枚举不可用；已改用 `read`/`glob`/`grep` 完成同等的手工分段阅读 | 本会话实测两次；未做任何写权限变更 | 环境/装置 |
| B-H2 | `read` 与 `grep` 对**同一行**的输出都截断在约 2000 字符（`line truncated to 2000 chars`）。大量证据是**单行 JSON**，其第 2000 字符之后本会话不可读 | `evaluation_report.json`、`evidence-source.json`、`controller.log` 等实测 | 装置（工具能力），非原件缺件 |
| B-H3 | 因此凡**单行**超长文件，只登记“可见部分（工具2000字符/行截断）”，并用针对性 `grep` 取靠前字段；**不**把截断记为“已读全文”。**实测澄清**：`batch/items/*.json` 全部为**多行**美化 JSON（31–81 行），本区间 79/79 完整可读，**不受**该限制；单行超长件集中在 `evidence-source.json`/`evidence-target.json`/`comparison.json`/`evaluation_report.json`/`metadata.json`/`input_profile.json`/`comparison_manifest.json`/`classification-*.json`/`classifier-input.json`/`evaluator_manifest.json`/`this-task-classification.json`/`batch-authorization.json`/`controller-health-*.json`/`runners-before.json`/`result.json` 等 | 分块审阅逐项标注；events/items 专项核对 79/79 无截断 | 装置 |
| B-H4 | **`target.gen.model.json` 有两种互不兼容的形制，不能跨项套用**：① **调用元数据**（无 `content`）——如 D2-151 全文 24 行，仅 taskId/direction/stage/round/model/finishReason/requestBodyBytes/各 sha256/outputBytes/outputLines/usage/maxTokensFieldSent；② **原始模型响应正文** `{"role":"assistant","content":"```go…```"}`（**单行、含完整目标代码**）——已逐字核 D2-123，cases-03 记 D2-124/125/126/128/130 同形。故“`model.json` 只是元数据”**不是**普遍事实；逐项打开判定，不得由 D2-151 外推 | D2-151 全文；D2-123 实测 | **装置/形制缺陷（同名异物）**；直接影响“唯一保存下来的目标代码在哪里”的判读 |
| B-H5 | 本会话初始给分块会话的提示用了 “D2-0NN 在 manifest 第 NN+1 行”的公式，该公式对 NN≥027 **错误**：manifest 缺 D2-026、D2-113 两行，故 D2-027–112 的行号 = NN，D2-114 起 = NN−1（实测 D2-121 在第 120 行、D2-151 在第 150 行、D2-081 在第 81 行） | manifest 逐行读数；cases-03 独立发现同一差异 | 装置/方法（**本审查提示的缺陷**，非数据缺陷）：引用 manifest 行号必须按 Id 内容定位；分块会话已按内容定位 |
| B-H6 | **分块会话自报的“现存文件数”有错，不能作为覆盖统计的权威值**：本会话按 `glob` 实测复核三处——**D2-091 真值 42 件**（cases-01 写 38，少 4）、**D2-093 真值 48 件**（cases-01 写 53，多 5）、**D2-095 真值 32 件**（cases-01 写 37，多 5）。故 `harness-b-coverage.md` 的逐项文件清单与计数**一律按 glob 重新推导**，并把 glob 计数 ≠ cases 计数的项列入“审计差异”；这不改变各文件本身的读取事实 | 本会话对 `D2-091-*/**/*`（42）、`D2-093-*/**/*`（48）、`D2-095-*/**/*`（32）的完整 glob 输出逐层点数（`01-frozen`/`job-00`/`job-01`/`job-02`/`job-00b`/`03-self-review`/`02-conversion`/根层） | **装置/方法（本次审阅自身的方法缺陷）**：单一会话的汇总计数不可直接采信；覆盖清单必须由独立 glob 重建 |

## 1. 范围与身份核对

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-R1 | 用户口径“D2-081 至 D2-160 全部 80 项”与 manifest 实际不符：该区间只有 **79 行**，**D2-113 不在 manifest**（第 112 行 D2-112 之后直接是第 113 行 D2-114） | `manifest.csv` 逐行读数；`batch/items/` 亦无 `D2-113.json` | 未定（口径差异，非数据缺陷） |
| B-R2 | 该区间 79 项**均有** `batch/items/<taskId>.json`；批级记录声明 `items/` 覆盖 277/277 | `batch/README.md` §进度快照；`batch/summary.md` §11.1；逐项 `items/*.json` | 已有规则落实（任务状态 §2.2 逐项登记） |
| B-R3 | `items/*.json` 记录 `casePath` 指向 **`docs/test/dataset-2/...`**（历史数据集路径），与副本实际目录 `docs/dataset-2/dataset-2-copy/...` 不同；副本内不再有 `docs/test/dataset-2` | `items/D2-081.json` L7 等 | 装置（路径已迁移，属副本形态） |
| B-R4 | item 中 `sourceSha256` 为**小写**，manifest `Sha256` 为**大写**，逐项数值一致（非内容差异） | `items/D2-081.json` L12 vs manifest 行；现行分类准入 §3 明确“不能把十六进制大小写不同直接认定为文件字节不同” | 已有规则落实（分类准入 §3） |
| B-R5 | **manifest 的 `JobId`/`Evidence` 列在本区间 79/79 行均为空 / `"UNVERIFIED (not built, not run)"`**，而 `items/*.json` 记录真实 jobId 与实际 verdict（含 12 项 `matched`、6 项 `semantic_pass`）。批级 `README.md`/`summary.md` §3 把 `manifest.csv` 称为“**唯一权威索引**”，消费它会得到与 items 相反的印象 | manifest 逐行读数；`items/*.json` 逐项；`batch/README.md` L11、`batch/summary.md` L390 | 记录一致性缺口（装置/形制）：须明确 manifest 是**接收清单**而非终态索引，或同步其列；本审查不追改 manifest |

## 2. 冻结范围内 5 项**完全无过程材料**（D2-156–D2-160）

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-N1 | D2-156、D2-157、D2-158、D2-159、D2-160（全部 `c-to-csharp`）在副本中**没有任何用例目录**：`docs/dataset-2/dataset-2-copy/c-to-csharp/**` 为空，`*/D2-156*`…`*/D2-160*` 均 0 文件 | 多次 `glob` 实测（含 `**` 兜底）；对照其余项均有 `output/batch/` | 缺件（如实登记） |
| B-N2 | 5 项**只有** `batch/items/D2-156.json`…`D2-160.json`：`disposition=FROZEN`、`phase=NOT_STARTED`、`lifecycle=WAITING`、`blockingReasons=["BLOCKED_ENV"]`、`blockerRef=batch/platform-blocker-csharp-target.md`、`usage.requests=0`、全部 verdicts=UNVERIFIED | 5 份 item 全文（各 31 行） | 已有规则落实（任务状态 §4 “原因与恢复条件”保留 BLOCKED_ENV） |
| B-N3 | `dispositionNote` 明示：按 2026-10-11 用户裁决跳过 C#-目标方向；`disposition=FROZEN` 仅表示“已声明可转换、在队列中”，**没有跑冻结 job**，因平台缺陷已定性；**0 模型调用** | 同上 | 已有规则落实（C# 目标平台缺陷处置见 `platform-blocker-csharp-target.md`） |
| B-N4 | 该平台缺陷在 `platform-blocker-csharp-target.md` 顶部已标 **✅ 2026-10-11 修复**（复测 job `eval-20261011-122249-fe456bbe` 两侧 `completed/0`），恢复条件“平台修复后按原契约重提”**已具备**；而 5 项 item 仍为 `WAITING/NOT_STARTED`，属**可恢复但未恢复** | `platform-blocker-csharp-target.md` L3–L12；`batch/summary.md` §11.4 亦记“恢复条件已具备，恢复动作=逐项跑全链” | 已解决（平台侧）但**未落实**的恢复动作；不是转换失败 |

## 3. 交付完整性：本区间 **30/79 项缺 `result.md`**

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-D1 | `docs/dataset-2/**/result.md` 全副本共 **198** 份；本区间 **49 项有、30 项无** | 全量 result.md 清单（198 行）与本区间逐项比对 | 装置/流程（原件缺件） |
| B-D2 | 缺 `result.md` 的 30 项：D2-081、082、083、084、085、086、087、089、090、094、098、099、100、101、102、107、108、110、112、114、115、152、153、154、155、156、157、158、159、160 | 同上；D2-081 用例目录实测 11 件（`01-frozen` 3 + `job-00` 8），无根层 `result.md`/`evaluator_manifest.json`；D2-152、D2-110 实测同样无 | 缺件 |
| B-D3 | 这批缺 `result.md` 的项**多数仍是终态**：例如 `items/D2-081.json` 为 `phase=CLOSED`、`lifecycle=DONE`（去向 `SOURCE_DEPENDENCY_GAP`）；D2-100 为 `phase=SOURCE_PRECHECK_FAILED`、`lifecycle=DONE`；D2-152/154/155 为 `SOURCE_NOT_BUILDABLE`；D2-082/108 为 `WAITING`，D2-089/090/094/098/099/101 为 `PARTIAL` | 各 `items/*.json`；`batch/summary.md` §2 | 现状与现行规则不一致 |
| B-D4 | 现行规则要求**每一处理项**（含失败、阻断、非可转换、WAITING）都写 `result.md`，并逐件核对产物后**才**能记 DONE/PARTIAL/CLOSED；缺应有件不得记终态 | 交付契约 §1.1（L15–L21）；任务状态契约 §4（L110 “缺报告/核对记录不能记终态”） | **已有规则落实（规则已存在，历史记录未落实）**：这不是新缺口，而是现行门禁未被历史批次执行；本审查不追改状态，只登记缺件与判据 |
| B-D5 | 缺 `result.md` 的项同时**多数缺 `evaluator_manifest.json`**（如 D2-081、D2-110、D2-152 根层均无）；有 `result.md` 的项也需逐项核 manifest 是否存在 | 各用例 `glob` 清单（见 cases 文件） | 缺件（待 cases 回填逐项） |
| B-D6 | `items/` 与 `events.jsonl` 侧**没有为这些缺报告项追加 `REPORT_WRITTEN` 类事件**，`D2-081` 在 `events.jsonl` 仅 2 条（`CLASSIFIED`、`SOURCE_PRECHECK_SOURCE_DEPENDENCY_GAP`） | `grep D2-081 batch/events.jsonl` = 2 命中 | 已有规则落实（批量工作流 §8 双向对账要求；此处对账未覆盖报告义务） |

## 3bis. 代码正文与生成调用的系统性缺口

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-C1 | 副本内**没有任何 `source/` 树**（`**/source/*` 0 命中），也**没有任何最终目标代码**：`**/target.*` 全副本只命中 `target.gen.model.json`、`target.self-repair-*.model.json`、`target.self-repair-*.proposal.json` 等元数据/建议件。故“源/目标代码正文已删”是**全副本系统性事实**，不是单项缺件；任何实现事实都不能由摘要/哈希复原 | 两次 `glob` 实测；与 `full-review-cases-01.md` L3 记载一致 | 装置（副本形态） |
| B-C2 | 本区间至少有 **6 个已转换（平台原判 `matched`）项完全没有 `target.gen.model.json`**：D2-091、D2-092、D2-093、D2-095、D2-096、D2-097。其 `02-conversion/` 只保留 `request.system.txt`（D2-092 另有 `repair.system.txt`；D2-093 另有 `repair.system.txt`+`repair2.system.txt`），而同项 `03-self-review/self-review-1.model.json` **存在**。按 B-H4，其余 converted 项的 `target.gen.model.json` 往往正是**唯一保存下来的响应/目标正文**，所以这 6 项同时缺“调用元数据”和“响应正文” | 六项逐项完整 `glob` 清单；全副本 `**/target.*` 清单不含这 6 项；对照 D2-123 的响应形制 | 缺件（请求→响应→目标的关联链断在“响应”侧） |
| B-C3 | 现行规则要求保存完整脱敏请求/原始响应及实际模型名、参数、token、输入/输出哈希的关联记录（请求→响应→目标可回读）；只有请求正文不足以复核模型返回与目标来源 | 根 `SKILL.md` L104；任务状态契约 §2.1（L36–L41）；单项闭环 §2 | **已有规则落实（规则已存在）**：这 6 项历史记录不满足现行可复核要求；本审查不补造响应，也不据此改判 `matched` |
| B-C4 | `case.md`（骨架中的冻结契约）在副本中**仅 1 份**（`c-to-cpp/pwd-fs-posix-to-win/case.md`，**不在本区间**）；本区间冻结记录统一落在 `01-frozen/frozen-inputs.md` | `**/case.md` 全副本 1 命中 | 装置/形制（交付契约 §2.1.1 L45 允许“用户已约定其他合法落点，以冻结指针为准”）；须逐项核 `frozen-inputs.md` 是否完备 |
| B-C5 | `capsule.zip` 与 job 的 `source/`、`target/` 暂存树在副本中**不存在**（骨架 §2.1.1 L66/L71 列出） | 本区间逐项 `glob` 清单均为“input_profile / comparison_manifest / metadata / job-id + returned-evidence”，无 capsule 与树 | 装置（提交件未留存）；影响“提交 capsule 精确文件集合与分类 `details.files[]` 对应”的复核 |
| B-C6 | `evaluator_manifest.json` 全副本仅 **72** 份（本区间 **21** 份：D2-088、091、092、093、095、096、097、109、111、116、117、118、123、124、125、126、128、130、133、134、151） | 全副本 `**/evaluator_manifest.json` 清单 | 条件件：交付契约 §1 L9 明确“视消费方要求决定是否生成”，缺失**不单独判违规**；须与 `result.md` 缺失分列，不混算 |
| B-C7 | **响应形制的 `target.gen.model.json` 又缺现行契约要求的调用元数据**：cases-03 实测 D2-123/124/125/126/128/130 的该文件只有 `{"role":"assistant","content":…}`，**没有**模型名/参数/token/`finish_reason`/输入输出哈希；同项 `self-review-1.model.json` 只保存外层 `chat.completion` 封装，也没有 `usage`/`finish_reason`/哈希；调用级 token 用量只出现在 `batch/items/*.json` | cases-03 发现 #1、#15、#18；对照交付契约 §2.1.1 对 `<stem>.model.json` 的字段要求、根 `SKILL.md` L104 | 缺件（可追溯性）：请求/响应/用量/哈希不能互相替代，item 级汇总不等于调用级原件 |
| B-C8 | **`result.md` 自称“冻结记录齐备”而目录内并无 `frozen-inputs.md`**：D2-123/124/125/126 的 `result.md` 写“源/驱动/`.csproj`/目标/清单/冻结记录齐备”，但 `01-frozen/` 只有 `classification-1.json` 与 `classifier-input.json` | cases-03 发现 #4；本会话 `glob` 复核 D2-123 目录 | **已有规则落实（不实声明）**：交付契约要求逐件核对真实产物后才写结论；本审查只登记缺件与不实声明，不倒填、不复原 |

## 3ter. 冻结落盘门禁：本区间 **19/79 项缺 `frozen-inputs.md`**

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-F1 | 全副本 `frozen-inputs.md` 共 **223** 份；本区间 **60 项有、19 项无**。缺件 19 项：**D2-091、092、093、096、097、103、104、105、106、118、123、124、125、126、156、157、158、159、160** | 全副本 `**/frozen-inputs.md` 清单（223 行）与本区间逐项比对；并对 D2-091/096/103/118/123 做 `**/frozen*` 定点复核，均 0 命中 | 缺件 |
| B-F2 | 其中 **14 项**（091、092、093、096、097、103、104、105、106、118、123、124、125、126）在缺 `frozen-inputs.md` 的情况下**仍取得分类结果、源预检 job、生成/自评与（部分）评估证据**；`01-frozen/` 内只有 `classifier-input.json` 与 `classification-*.json` | 各用例完整 `glob` 清单；见 `harness-b-cases-01.md`…`04.md` | 现状与现行规则不一致 |
| B-F3 | 现行规则：正式转换须在**分类前**逐项写出并回读本 run 的 `01-frozen/frozen-inputs.md`；缺失、空白或错位**不得分类、不得推进**；该门禁是 Agent 手工 Markdown 约束，不是自动拦截器，因此**只有实际记录能证明该次已遵守** | 任务状态契约 §2.2（L45–L55）；分类准入 §1（L9）；根 `SKILL.md` L24 | **已有规则落实（规则已存在，历史记录缺件）**；本审查不追改状态，不据“没有文件”断言当时未做任何冻结判断 |
| B-F4 | 无法从副本判定这些项是否曾以**其他未留存落点**满足冻结（例如历史 run 的目录，或 D2-103–106 被批级记录归入“已在既有批次完成”）；原文已删，不能由摘要/哈希复原 | 交付契约 §2.1.1 L45 允许“用户已约定其他合法落点，以冻结指针为准”；等价限制见任务状态 §2.1 L41 | **未定**：只登记“副本内缺该必备件”，不下“当时未冻结”的结论 |
| B-F5 | D2-156–160 的缺件可由 `items/*.json` 的 `dispositionNote` 解释：**没有跑冻结 job**（按 2026-10-11 用户裁决，C# 目标平台缺陷已定性），0 模型调用 | `items/D2-156.json`…`D2-160.json` | 已有规则落实（但“未开始项不要求预建报告/阶段目录”与“FROZEN 去向”并存，须在总账中说明） |

## 3quater. 本区间证据缺失总账（“原源/目标已删”之外的应有件缺口）

| 应有件 | 本区间缺失 | 判据 | 备注 |
|---|---|---|---|
| `source/` 源树（含 `run_case.py`、fixture、`.csproj`/`Driver.cs`） | **79/79 全缺** | 全副本 `**/source/*` 0 命中 | 副本删码；使源集合/驱动/工程文件无法逐字节复核 |
| 最终目标代码（根级 `target.<ext>`） | 本区间**所有已生成项全缺** | `**/target.*` 仅命中 `*.model.json`/`*.proposal.json` | 目标实现事实不可复核；仅 `target.gen.model.json` 的响应形制保留了部分目标正文（B-H4） |
| 模型原始响应/生成元数据（`target.gen.model.json`） | **6 项全无**：D2-091/092/093/095/096/097 | B-C2 | 其余项该文件为**响应正文**或**调用元数据**两种形制（B-H4/B-C7） |
| `frozen-inputs.md` | **19 项**：091/092/093/096/097/103/104/105/106/118/123/124/125/126/156–160 | §3ter、cases | 其中 14 项仍完成了分类/预检/生成/评估 |
| `result.md` | **30 项**：081–087、089、090、094、098–102、107、108、110、112、114、115、152–155、156–160 | §3 | 现行交付契约 §1.1 要求每处理项都写 |
| `evaluator_manifest.json` | 58/79 无（条件件） | §3bis B-C6 | 交付契约 §1 L9“视消费方要求”，不单独判违规 |
| `case.md` | 本区间 **79/79 全缺**（全副本仅 1 份，在 c-to-cpp/pwd-fs-posix-to-win） | §3bis B-C4 | 骨架 §2.1.1 L45 允许其他合法落点；本批以 `01-frozen/frozen-inputs.md` 为冻结件 |
| `capsule.zip` 与 job 的 `source/`/`target/` 暂存树 | 本区间全缺 | §3bis B-C5 | 提交件精确文件集合不可复核（影响分类身份对应核对） |
| job 级 `controller-health-before/after`、`runners-before`、closure | **多项不齐**（cases-01 B-16、cases-02 B-AA10/B-AA11、cases-03 发现 35） | 各 cases | 平台终态标签不替代真实清理核对（任务状态 §4 L112） |
| 失败 attempt 原件 | **D2-114 的 403 无任何 attempt 原件**（D2-151 有 `attempt-1-403.json`） | cases-02 发现 26 | 同类失败证据留存不一致 |

## 4. 孤立原件形制缺陷

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-A1 | `c-to-cpp/D2-152-c-c-du.c/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/` 内报告文件名是 **`evaluation_report.md.md`**（双扩展名）；全副本 `**/*.md.md` **仅此 1 例** | 两次 `glob`（`**/*.md.md`、`**/evaluation_report.md.md`）均只命中该路径 | 装置（采集/落盘命名缺陷，非内容缺陷） |
| B-A2 | D2-152 同时存在 `job-00-source-buildability`（含 `evidence-target.json`、`comparison.json`、`runners-before.json`、`controller-health-before.json`）与 `job-00b-source-buildability-linux`（无 health/runners），属**同一源换候选 OS 的两次预检** | D2-152 用例 `glob` 清单 | 已有规则落实（构建前提 §0.1 L34 “一次候选预检失败只证明该 runner/命令，未测候选单列”） |
| B-A3 | **报告视图与原始证据措辞不一致（模板）**：D2-152 的 `job-00/returned-evidence/evaluation_report.md.md` 同时写 `Conversion result: INCONCLUSIVE`／`Reason: Source build failed; baseline cannot be established.`，却在 Runs 表把源侧 `Execution performed` 记为 **`yes`**、`Preflight PASSED`、`Cleanup PASSED`、`Runner state after READY`。源构建既已失败，则该“已执行”只可能是模板默认值，不能读成“源行为已执行” | 已逐字读该文件前 40 行（全文 75 行）；cases-04 异常 #3 | **装置/报告模板缺陷**：核 job-00 时必须同时看 outcome 与 raw evidence，不能只读 Runs 表的 `Execution performed` |

## 5. 批次级记录与本区间相关的事实（供对照，不替代逐项证据）

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-B1 | `batch/summary.md` §11.1 记 `events.jsonl` **1145 行**；本会话实测 **1148 行**。差异 3 行可能是快照后追加，不能据此判定缺档 | 实测 `events.jsonl` 总行数 1148；summary L504 | 未定（快照时点差异） |
| B-B2 | Abseil 簇 7 项（含本区间 D2-081、D2-084、D2-085、D2-086、D2-087）由逐项编译器诊断定案为 `SOURCE_DEPENDENCY_GAP`，0 模型调用；“不是系统接口、不是命令/契约缺陷”有明文判据 | `batch/pattern-note-abseil-library-units.md` L4–L26；各项 `items/*.json.sourcePrecheck` | 已有规则落实（构建前提 §0.1 三类分列） |
| B-B3 | 但该簇记录**没有**像 D2-100（`z85.h`）或 D2-161（`vary.h`）那样给出“旧 dataset + 全工作区穷举 0 命中”的证据；现行规则要求判 `SOURCE_DEPENDENCY_GAP` 前先核“仓库内是否存在可补齐来源” | 对照 `batch/pattern-note-bsd-userland.md` §追加（L58–L71）；构建前提 §0.1 L45/L50 | 已有规则落实（**证据记录缺口**）：不能据此断言头文件其实可得，只能说历史记录未展示该穷举 |
| B-B4 | BSD userland 在 **macOS** 可构建（D2-151 实测 `completed/0` 并最终 `matched`），既有 `SOURCE_NOT_BUILDABLE` 结论只实测过 windows+linux；本区间 D2-152/154/155 属该族 | `pattern-note-bsd-userland-macos-correction.md`；`batch/summary.md` §1-C5 | 已有规则落实（更正以追加方式，不改写历史判定） |
| B-B5 | C# 目标平台缺陷影响 38 项，已修复；修复后新增纪律 `artifactLanguage` 必须写 `csharp`（写 `dotnet` 会 403 `identity_mismatch`） | `platform-blocker-csharp-target.md` L11–L12 | 已有规则落实 |

## 5bis. `batch/items` × `events.jsonl` 交叉核对（79/79 项，专项会话独立复核）

覆盖：`events.jsonl` 实测 **1148 行**（`batch/summary.md` §11.1 写 1145，差 3 行，见 B-B1）；本区间命中 **303** 行；**79/79 项在 events 中至少 1 行**；79/79 的 `items/*.json` 完整可读（多行 JSON）。身份正面结论：79/79 的 `taskId`/`direction`/`sourceSha256` 与 manifest 行逐位相符（仅十六进制大小写差异）。

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-E1 | `admissionStatus` 出现值域外的 **`"NOT_TAKEN"`**（D2-094、098、099、101；`cls`/`sha256` 均 null），而 `D2-100` 为 `ALLOWED` 但 `cls=null`、`sha256=null`（note 指向 `01-frozen/classification-1.json`） | 各 `items/*.json` 的 `classifier` 块 | 装置/形制：机械按“ALLOWED 且 blockingReason=null”判门禁时会把 `NOT_TAKEN` 误读；现行分类准入 §2（L33）明确“未知状态/原因、损坏结果、缺项不得当作 ALLOWED”，故这些项本就不应推进，未擅自放行 |
| B-E2 | `disposition=FROZEN` **一值三义**：① 已生成且平台 `matched`（D2-103、104、105、106，`phase=CLOSED`）；② 未提交的评测未就绪（D2-089、090、094、098、099、101、108）；③ 排队未开始（D2-156–160，`phase=NOT_STARTED`）。同 disposition 下 `phase` 名分裂为 `CLOSED` / `SOURCE_PRECHECK_FAILED` / `CLOSED_SOURCE_DEPENDENCY_GAP` / `CLOSED_SOURCE_NOT_BUILDABLE` / `CLOSED_PREPARATION_GAP` / `CLOSED_ORACLE_NOT_FREEZABLE` 等 6+ 种 | 79 项 item 逐项；事件集合 | **已有规则落实（规则被违反）**：任务状态 §3（L87）定义 `FROZEN`＝“边界已落盘、仍须分类/预检才能生成”，把它用于**已转换并取得 matched** 的项（D2-103–106）与该词表冲突；本审查不追改状态，只登记语义漂移与统计风险 |
| B-E3 | 字段名/取值跨项漂移：目标哈希字段两套名（`finalTargetSha256`：D2-088/091/092/093/095/096/097/151；`targetSha256`：D2-103–106/109/111/116/117/118/123–126/128/130/133/134）；双构建 job 字段两套（`dualBuildJobId` vs `evaluation.jobId`：D2-103–106）；`D2-108.blockingReasons` 是**对象数组** `[{code,detail}]`（其余为字符串数组或 `[]`），且该件用 camelCase `networkMode/networkTargets`（同类件用 `network_mode`） | 各 `items/*.json` | 装置/形制：影响自动对账；本审查按实际字段逐项读，不做跨项假设 |
| B-E4 | **失败 attempt 计数自相矛盾**：`items/D2-151.json` 顶层 `failedAttempts` 有 1 条（403 `identity_mismatch`，原件 `attempt-1-403.json` 存在），而同文件 `usage.failedAttempts = 0`；events 确有 `SUBMISSION_REJECTED`。同类 403 另见 D2-114（陈旧 classification 导致） | `items/D2-151.json`；`attempt-1-403.json`；`events.jsonl` | 已有规则落实（根 `SKILL.md` L104 要求保留失败 attempt 记录）；两处计数不一致如实登记，**不擅自清零** |
| B-E5 | `items` 记录了更正而 `events` 缺记录：D2-140 记“首次 classify 误用错误 `sourceSha256` ⇒ `BLOCKED/input_error`；改用 classification-2，误生成的 classification-1 已删除”，但 events 对 D2-140 仅 `CLASSIFY/ALLOWED`、`SOURCE_PRECHECK`、`TERMINAL` 三行；D2-116（classification-1 因 cp 失败缺失）、D2-128/133（补 `source/Driver.cs` 后重分类为 classification-2）同型 | events 逐项命中集合 vs item 文本；对照 `batch/summary.md` 各条目 | 已有规则落实（批量工作流 §8 要求 items↔events 交集/双向差集对账）；本审查登记差集，不改写历史 |
| B-E6 | 本区间唯一补登件是 **D2-088**（`BACKFILLED_EVENT` + 补登 `TERMINAL`）；其 item 引用的两个 jobId（`eval-20261010-145337-41c8080e`、`eval-20261010-145923-8c852ab1`）在 `events.jsonl` 中**查不到** | events 逐项命中；`reconciliation-2` §3 曾记 D2-088 事件缺档 | 已有规则落实（只追加补登，不改写）；jobId 原件在 events 缺对应，属**可追溯性缺口** |
| B-E7 | D2-156–160 在 events 中**各只有 1 行 `DEFERRED`**（`events.jsonl:265–269`，`reason=BLOCKED_ENV`、`note` 仍写“platform evidence-bundle schema defect”、0 模型调用）、**无 `TERMINAL`**，而同因的区间外 D2-030 有 `TERMINAL lifecycle=WAITING`；覆盖这 20 项的恢复说明 NOTE 挂在 **`taskId="D2-007"`** 名下（**`events.jsonl:1148`**，本会话已逐字读；events/items 专项会话原先写“第 1151 行”，而文件共 1148 行，**已按实测更正为 1148**），该 NOTE 记“20 项恢复前提均已满足、需各自跑全链；D2-007 作试点、本轮保持 WAITING” | 已读 `events.jsonl` 265–269、555、634、1146–1148 行 | 已有规则落实（任务状态 §4 L110 终态须有报告/核对）；5 项终态只在 items、事件流无终态标记，属事件覆盖缺口；**NOTE 行号以实测 1148 为准** |
| B-E8 | 事件流的身份字段异常：存在 `taskId="PLATFORM-PROBE"`（非 D2 id）与一条**完全没有 `taskId`** 的 `CONTROLLER_BUSY_OBSERVED`（只有 batchId）；方向级事件被挂在具体 item 上（`D2-094`/`D2-101`/`D2-155` 的 `DIRECTION_COMPLETE`，区间外另有 `D2-016 SWEEP_BACKFILL`、`D2-047/060 DIRECTION_CLOSED`、`D2-051 DIRECTION_BLOCKED_RANGE_DONE`） | events 逐行 | 装置/形制：逐项统计时会把方向级/批次级事件计入某一项，需按事件语义分离 |
| B-E9 | 方向计数自相矛盾：`D2-135` 事件写 `csharp-to-powershell direction 6/6 complete`，紧接着 `D2-136` 写 `7/7 complete`（该方向实为 D2-130–136 共 7 项） | events 相邻两行 | 未定/记录错误：至少一条计数错误；不影响 item 去向，但影响按事件统计方向完成度 |
| B-E10 | 分类器版本混用：本区间 `v2.3`（sha `441b4d50…`）= D2-081–087、102、103、104、105、106、108；其余为 `v2.4`（sha `009a6f31…`）。v2.3 那批同时缺 `sourcePrecheck.os`、缺 `dualBuildJobId`、缺 `failedAttempts` | 各 item `classifier` 块；`batch/summary.md` §9 记“已提交项分类均为 v2.4” | **与批级声明不一致**：批级总述称已提交项分类均为 v2.4，但本区间 14 项为 v2.3；不能跨版本直接比较字段完备性 |
| B-E11 | 分类后源树被改动并重分类：D2-128、D2-133 在分类后由 Agent 补 `source/Driver.cs` 并重分类为 `classification-2`；D2-116 的 `classification-1` 缺失 | items 文本 + events；分类准入 §3 L50（源集合变化须重新分类） | 已有规则落实（重新分类是正确处置）；但“被冻结/被分类的树 ≠ 最初 source-only 树”要求逐项以最新 `classification-N` 为准 |
| B-E12 | 同名源文件跨项复用（易串项）：`ModifiableServices.cs`（D2-118/D2-131）、`ProcessDLLHijack.cs`（D2-116/D2-132）、`CachedGPPPassword.cs`（D2-117/D2-137）、`UnquotedServicePath.cs`（D2-119/D2-142）、`UnattendedInstallFiles.cs`（D2-130/D2-149）、`HijackablePaths.cs`（D2-125/D2-144）、`TokenPrivileges.cs`（D2-126/D2-141）、`RegistryAutoruns.cs`（D2-123/D2-148）、`AlwaysInstallElevated.cs`（D2-124/D2-222）等 | manifest `SourceFile`/`Origin` 与各 item | 已有规则落实（纪律 A5：目录名/文件名不是 taskId，须按 `taskId`+`sha256` 对账） |
| B-E13 | 平台 verdict 逐项复核（与批级记录一致）：`matched` 12（088/091/092/093/095/096/097/109/111/128/133/151）、`semantic_pass` 6（117/123/124/125/126/130）、原判 `mismatched` 3（116/118/134）、`PARTIAL` 9、`WAITING` 8；`codeRevisions`：D2-092=2、D2-093=3、D2-123=1、D2-088=1、D2-151=1，其余 0 | events/items 逐项 | 原件支持（逐项计数），不合成单一成功率 |
| B-E14 | D2-091 job-01 两侧 `execution.exitCode` 均为 **`4294967295`**（uint32 表示的 -1），两侧 stdout normalizedText 均为 `PID not found :( exiting...\n`（29 B / 29 B），平台 `behaviorVerdict=matched`，`comparison.json` 的 `output` 维度 `diffs=[]`、其余 4 维度 `not-applicable` | 已逐字读 `job-01/returned-evidence/evidence-source.json`、`evidence-target.json`（前 2000 字符窗口）、`comparison.json` 全文、`evaluation_report.json`（前 2000 字符） | **原件支持**：退出码语义两侧相同（同为 -1 的无符号表示），不构成差异；**限制**：源侧 stdout `digest` 位于工具 2000 字符窗口之外（B-H2），无法核对是否与目标 digest `b14a55be…` 逐字节相同，故只能说“比较器在 output 维度判 diffs=0”，不能说“原始字节已核实相同” |

## 5ter. 分块会话已回传的逐项发现（D2-121–D2-130、D2-141–D2-150）

> 逐条原始记录见 `harness-b-cases-03.md`、`harness-b-cases-04.md`。下列为跨项/高价值条目；其余逐项事实以 cases 文件为准。

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-T1 | **`batch-authorization.json` 授权事由模板残留 D2-088**：D2-141 的 `dataSource.confirmation` 写“该项 **D2-088** 无网络、无凭证、仅本地文件写入”，而该文件属 D2-141；本会话已逐字读该文件确认。cases-03 在 D2-123 等项见到同型残留 | 已读 `csharp-to-python/D2-141-…/job-00-source-buildability/batch-authorization.json` 全文 26 行；cases-03 发现 #6 | **装置/形制**：授权记录的“事由”字段不可作为单项网络/凭证事实的独立证据，须回源核对 |
| B-T2 | **D2-150 的 `01-frozen/` 只有 `classification-2.json`，没有 `classification-1.json`**（首轮 `BLOCKED/public_network_unverified` 的结果已被删除）；同一目录另有 `classifier-input.json`、`frozen-inputs.md` | 已 `glob` D2-150 用例全清单确认 | **已有规则落实（规则被违反）**：任务状态 §1 L9“不覆盖原记录”、§2.1 L41“保留旧证据”；批级 `summary.md` §11.3 把“删除误生成的 classification-1”写成纪律，与现行证据保留要求冲突。本审查不追改历史，只登记冲突 |
| B-T3 | **D2-150 以“无入口/纯程序集元数据”记 `PREPARATION_GAP` 并跳过生成**（0 模型调用）；现行规则明确：缺 main/可执行文件/stdout/合法入口**不得**直接记 `PREPARATION_GAP` 跳过生成，源可构建时应记 `LIB_UNOBSERVABLE_COMPILE_ONLY` 继续转换并验证目标语法/编译 | `items/D2-150.json`；任务状态 §3 L96；评估准备 §1.3 L43–L44；根 `SKILL.md` L25 | **已有规则落实（规则已存在，历史处置与现行口径冲突）**；边界：D2-150 的源预检是 `failed/1`（CS0579），若该失败确由构建外壳造成（见 B-T4），则“源可构建”前提本身需要重评，不能仅凭文本改判 |
| B-T4 | **D2-150 的 CS0579 被 cases-04 归因为构建外壳（probe `.csproj`）自动属性冲突**，而非源依赖缺失 | cases-04 发现 #9；`items/D2-150.json` 诊断 | **待核验/装置**：若属外壳缺陷，则 `SOURCE_*`/`PREPARATION_GAP` 归因需按构建前提 §5 责任表重核；副本内无 capsule 与源树，无法定案 |
| B-T5 | **job-00 证据完整性不一致**：D2-141–D2-150 的 `job-00/returned-evidence/` 只有 `evidence-source.json`，**没有** `evaluation_report.json`/`.md`、`controller.log`；而 D2-088、D2-109、D2-151 等的 job-00 有 report，D2-110 有 `evaluation_report.md`，D2-152 有全套（且 `.md.md` 双扩展名） | cases-04 发现 #3；本会话对 D2-110/D2-152/D2-088/D2-151 的 `glob` 清单 | 装置/缺件：引用“job-00 报告/清理”时不能假定各项目录形状相同（与 `full-review-cases-01.md` 对 D2-002 的结论同型） |
| B-T6 | **Agent 自写驱动**：D2-128、D2-133 的源侧无入口，由 Agent 新增 `source/Driver.cs` 后重分类（`classification-2`）并取得行为基线；批级记录显示 D2-109 亦“补最小中性 `.csproj`（net48）+ `Driver.cs`” | cases-03 发现 #5；`batch/summary.md` L84、L119、L125 | **已有规则落实（历史做法与现行规则冲突）**：评估准备 §2 L53–L55 明确“driver 须来自用户或获批平台已提供的精确版本；Agent 不编写、生成、保存新的辅助驱动/工具”。故 D2-109/128/133 的 `matched` 属**原件支持的局部比较**，但**驱动来源不符合现行规则**，不得计入现行“有效 matched”；且 D2-128 的 matched 仅覆盖该驱动的 5 行输出、`IsModifiableKey` 未驱动 |
| B-T7 | **manifest `Lines` 列与正文行数系统性不一致**：cases-03 在 9/9 可对照项发现差异；cases-04 记 D2-143 `Lines=62` 而 frozen/result 为 74 | cases-03 发现 #8；cases-04 发现 #10 | **未定**：源正文已删，无法定案哪一侧正确；不得据 manifest 行数推断版本，也不得据此判交付缺陷 |
| B-T8 | **请求/审阅正文里 Agent 自写的“行为摘要”含错误技术断言**：D2-123 的 `request.system.txt` 把 `LUID_AND_ATTRIBUTES` 写成 16 字节（正确 12，自审纠正）、把 autorun 位置写成“4+4 分组”（源为交替顺序） | cases-03 发现 #2、#3 | **已有规则落实**：任务状态 §2.3 L70“规则与精确源事实冲突时标出条目与影响，不能凭 Skill 标题覆盖源”；同时印证 `full-review-cases-01.md` 对 D2-003 的同类结论（人为摘要可能比源更严格并诱导错误转换）。**不能把 prompt 里的摘要当作源事实证据** |
| B-T9 | **非可转换去向的 item 仍提交了带占位 target 的 job-00**（cases-03 发现 #9），与 cases-01 对 D2-001/D2-002 的旧预检装置结论同型 | cases-03 发现 #9 | 已有规则落实（现行 source-only 预检形态可避开；见评估准备 §1.1 与 `batch/summary.md` L145） |
| B-T10 | **job-00 `metadata.json` 的 `safetyClassification` 指针指向已被取代的 classification**（cases-03 发现 #10） | cases-03 发现 #10 | 装置/可追溯性：与 B-T2 同源，引用分类版本须按 `this-task-classification.json` 与最新 `classification-N` |
| B-T11 | **D2-130 命中 Windows 260 字符路径上限**，落盘时需 `\\?\` 前缀（批级记录与 cases-03 均记） | cases-03 发现 #14；`batch/summary.md` L123 | 装置（平台/OS 限制） |
| B-T12 | **自审模型的响应正文未完整保留**（cases-03 记部分项无 usage/哈希字段） | cases-03 发现 #15 | 缺件：与 B-C2 同类，属可追溯性缺口 |
| B-T13 | **SharpUp 同项目依赖的“快照外 vs 数据集内未打包”未定案**：D2-127（及 D2-131/132/137–149）判 `SOURCE_DEPENDENCY_GAP`，但副本内无 capsule 文件清单，无法按构建前提 §0.1 L45/L50 的三问核实 | cases-03 发现 #11；cases-04 发现 #11 | **未定**：与 B-B3（Abseil 簇）同一证据缺口类型；不得据此断言是打包缺口，也不得断言依赖缺失已穷举 |
| B-T14 | **正面事实**：D2-121–130 与 D2-141–150 的 `taskId`/`direction`/`sourceSha256` 与 manifest 逐项对应，未发现串项 | cases-03 发现 #13；cases-04 发现 #13 | 原件支持 |

## 5quater. 分块会话已回传的逐项发现（D2-081–D2-090，cases-01 B-01..B-18）

> 原始记录见 `harness-b-cases-01.md` 的「发现汇总」。

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-U1 | **授权事由文本残留有三种变体**：D2-141 型写“该项 **D2-088**…”；D2-089/090 型写 **D2-151** 的文本（“本地文件删除…keep.txt/second.txt”）；cases-03 亦见 D2-088 型。同一模板被复制到不同项，逐项“事由”不可作本项事实依据 | cases-01 B-07；B-T1；已逐字核 D2-141 文件 | 装置/流程（模板化填写） |
| B-U2 | **多数“评估不可就绪”项未生成目标，与现行 `LIB_UNOBSERVABLE_COMPILE_ONLY` 分支不一致**：D2-082（`RUN_SAFETY_NOT_READY`）、D2-089/090（`ORACLE_NOT_FREEZABLE`）在源构建通过后 0 模型调用、无目标；items 显示 D2-094/098/099/101 亦为 `EVALUATION_NOT_READY`/PARTIAL 且无 sourcePrecheck、无生成 | cases-01 B-14；`items/D2-082/089/090/094/098/099/101.json`；现行评估准备 §1.3 L41–L47、任务状态 §3 L96、根 `SKILL.md` L25 | **已有规则落实（现行规则要求继续生成 + 目标语法/编译验证 + PARTIAL）**；历史按批内自设 E2 纪律（`batch/summary.md` §1-E2 L216「冻结阶段就判…0 模型调用跳过」）处置；两者冲突，现行文本优先用于“本轮应做什么”，**不追改历史状态** |
| B-U3 | **冻结记录是否含“知识与模型”组因项而异（形制不统一）**：D2-151 的 `frozen-inputs.md` L15–L20 明确列出 5 个 `selected skills` 路径+sha256，并记 `model/temp/RAG/outputBudget`（L14）；而 D2-081 的 30 行冻结记录**完全没有该组**，cases-01 记 D2-081–D2-090 中**仅 D2-082 有** | 已逐字读 D2-151 与 D2-081 的 `frozen-inputs.md`；cases-01 B-17；任务状态契约 §2 字段表 L20、§2.3 | 已有规则落实缺口（字段按模式填写、缺失须写理由；此处为**形制不统一**，使“知识可达/已读/注入”无法逐项回溯） |
| B-U4 | **job 环境与清理记录不齐**：D2-081/087/089/090 无 `controller-health-before.json`/`runners-before.json`，多数 job 无 `controller-health-after.json`，也没有 closure 字段；D2-086 提交前快照显示 windows runner `CLEANING`/`ready=false`，而该 job 仍成功且 cleanup PASSED | cases-01 B-16 | 装置 + 已有规则落实：任务状态 §4 L112 要求平台终态标签不替代真实清理核对；缺原件不得倒填“清理已确认” |
| B-U5 | **D2-088 的 job-01 `metadata.targetHash` 是 `"sha256:target-v2-self-repair-round-1"`（非哈希）**，且 `finalTargetSha256` 未在该 job 绑定；自修/交付落点在三处不一致（`target.v2.ps1` / `job-01/target/target.ps1` / `target.self-repair-1.*`），根级 `target.ps1` 缺失 | cases-01 B-08、B-09 | 装置/形制：版本关联不可由该字段回读（任务状态 §2.1 L37） |
| B-U6 | **D2-087（方向 `cpp-to-go`）的 job-00 `comparison_manifest.json`/`metadata.json` 把目标语言写成 C#**（`target.artifactLanguage="csharp"`、`dotnet build`、`target.cs (placeholder)`） | cases-01 B-18；`batch/platform-blocker-csharp-target.md` L12 要求 `artifactLanguage` 与方向自洽 | 装置（提交字段错误）；源构建失败、目标侧 SKIPPED，未影响 verdict，不得据此推断目标曾构建 |
| B-U7 | **分类输入/结果镜像错位**：D2-088 冻结引用的 `classifier-input-2files.json`/`classification-2.json`/`*-attempt1.json` 在副本不存在，现存 `classification-1.json` 只覆盖 1 个文件而 2 文件结果只存于 job 的 `this-task-classification.json`；D2-089 分类输入（1 文件）与结果（2 文件）错位 | cases-01 B-04、B-05 | 装置：分类准入 §3 要求按精确文件集合核对身份；镜像错位使身份链不可完整回读 |
| B-U8 | **D2-090 源执行 `timed-out`（30022 ms，stderr "command timed out"）被平台记为 `CODE_RESULT`/`code`** | cases-01 B-15 | **装置/环境**：不得据此反推代码缺陷（评估准备 §5 L103 先归因） |
| B-U9 | **知识候选（方向页缺条）**：CRLF/文本模式换行义务在 `cpp.md`、七语言共性、`file-io` 场景页与 `cpp-to-csharp` 方向页（`CPP-CS-07`）已有覆盖，但 `cpp-to-powershell` 方向页**缺“文件写入换行义务”专条** | cases-01 B-11 | **知识新增候选**（有条件、需按 Skill 编写规范核版本后由维护侧决定；本审查不改 Skill） |
| B-U10 | 正面事实：D2-082 首次预检失败被正确归因为**契约缺陷**（需 `-fpermissive` / `-DUNICODE` / `-D_UNICODE`）并修正命令后 `completed/0`，未改源码；D2-089 同型且 A/B 命令与诊断均留证 | cases-01 B-12、B-13；构建前提 §4.1 L142 | 已有规则落实（构建前提 §4.1：保留原命令、诊断与契约变更理由） |
| B-U11 | **`frozen-inputs.md` 在本区间多被当作“冻结 + 预检 + 终态”的合并备忘**：已逐字读 D2-081 的 30 行全文，含 `分类门禁：ALLOWED`、`源侧构建预检（硬门禁）：失败`、`归因`、`处置与终态`（disposition/lifecycle/UNVERIFIED/0 调用）。它**缺**任务状态 §2 字段表中的“知识与模型”组、“构建与源基线”中的环境/清理、“评估计划”、“授权与环境”、“恢复”各组，且未逐组写“不适用理由” | 已读 `cpp-to-csharp/D2-081-…/01-frozen/frozen-inputs.md` 全文；任务状态 §2 L16–L24、§2.2 L49 | 装置/形制：合并备忘使“冻结在先、结论在后”的时序无法从文件本身回读；**规则允许追加真实诊断**（§2 L21），故不判为倒填，但缺组与缺“不适用理由”属实 |
| B-U12 | 正面事实：D2-081 的归因写明“不是系统接口、不是命令/契约缺陷；是引用快照外文件 ⇒ SOURCE_DEPENDENCY_GAP”，并含编译器诊断原文与 jobId，符合构建前提 §0.1 的三类分列 | 同上 L13–L23；构建前提 §0.1 L40–L48 | 已有规则落实 |

## 5quinquies. 分块会话已回传的逐项发现（D2-101–D2-110，cases-02 发现 1–20）

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-V1 | **授权 confirmation 残留第四个来源**：D2-109、D2-110 的 `batch-authorization.json` 的 confirmation 复制自 **D2-088**（与 B-U1 的 D2-141/D2-089/090 变体并列） | cases-02 发现 #6 | 装置/流程（模板化填写，普遍） |
| B-V2 | **`target.gen.model.json` 双形制的第二个方向族**：D2-109 该文件**含目标代码正文与 reasoning**，不是“仅元数据” | cases-02 发现 #7 | 印证 B-H4；**知识新增候选**（“该文件名一律是元数据”这一前提应作废，改为逐项打开判定） |
| B-V3 | **job-00 在 D2-103/104/105/106/107 实际执行成双侧比较并返回 `mismatched`**（旧“占位 target”形态），非纯源侧预检 | cases-02 发现 #3、#19；与 cases-01 B-06、B-16 同型 | 环境/装置：不得把它当转换失败；现行 source-only 形态已可避开 |
| B-V4 | **D2-103 缺 `frozen-inputs.md` 与整个 `02-conversion/`，其 `result.md` 仍记“交付完整性完成”** | cases-02 发现 #11；`items/D2-103.json` | 已有规则落实（不实声明），与 B-C8/B-T2 同型；本审查只登记，不倒填 |
| B-V5 | **自审形制不统一**：D2-103/104/105/106 的 `self-review-*.json` 不是 `items[]` 结构化形制，D2-109 是正例 | cases-02 发现 #12 | 装置/形制：使“自审全条目”无法机械遍历，只能逐项人工读 |
| B-V6 | **D2-109 的覆盖窄于 `matched` 字面**：ACL/AES/XML 等义务仅编译未观察；两侧 `digest` 不同而 `normalized-text` 相同（CRLF/LF） | cases-02 发现 #8、#9；评估准备 §5 L99 | 已有规则落实（`digest`≠`normalizedText` 是不同对象；不得由“matched”外推完整覆盖） |
| B-V7 | **D2-102 的 `pch.h` 缺失经“0 命中”核实为非打包缺口**（两次 buildCommand 同报），属正例 | cases-02 发现 #18；构建前提 §0.1 L45/L50 三问 | 已有规则落实（正面） |
| B-V8 | **D2-107 `requiresSyntheticData=true` 由敏感词触发，与实际缺件（`pet.dll` 不存在）不符** | cases-02 发现 #20；`items/D2-107.json` | 装置/分类器启发式：与 `full-review-cases-01.md` 对 D2-002 的同型结论一致 |
| B-V9 | **D2-101 的 `admissionStatus="NOT_TAKEN"` 未列入 `blockingReasons`**；D2-101/107/108/110 无 `result.md`，以冻结记录“处置”节代偿 | cases-02 发现 #2、#17；交付契约 §1.1 L15–L21 | 已有规则落实缺口（与 B-E1、B-D1..D4 同源） |
| B-V10 | **D2-107 的 `classifier.version` 记 2.4 而 `classification-1.json` 实为 2.3**；D2-108 的 `casePath` 大小写与 `SourceFile` 不一致 | cases-02 发现 #4、#5 | 待核验：不影响去向，属元数据一致性 |
| B-V11 | **知识候选（消噪/装置）**：D2-106 与 D2-103 构成“fixture 对称性 vs 条目数纪律”的一对反例 | cases-02 发现 #13 | **知识新增候选**（需按 Skill 编写规范核版本后由维护侧决定；本审查不改 Skill） |
| B-V12 | **知识候选（去向词表叠合）**：D2-110 同时满足两种读法——(a) 引用快照外的运行时内部实现 ⇒ `SOURCE_DEPENDENCY_GAP`；(b) 真实诊断确认任何公开 TFM 都不可构建 ⇒ `SOURCE_NOT_BUILDABLE`；D2-107 甚至叠合三种去向（`PREPARATION_GAP`/`SOURCE_DEPENDENCY_GAP`/§1.3 仅编译）。cases-02 建议在任务状态 §3 去向表下补“判定顺序” | cases-02 发现 14/16 与 D2-110 记录第 302 行分析；任务状态 §3 L85–L96 | **知识新增候选**（现行词表确未给叠合情形的顺序；本审查不改真源） |
| B-V13 | **job 级 `metadata.json` 的分类记名措辞不一致**：D2-110 写 `safetyClassification="classifier-2.4 (pending)"`，而实际已 `ALLOWED`（措辞瑕疵，非流程违规——分类确在预检前完成）；D2-121/122/127/128/129/130 写 `(see classification-1)` 却指向已被取代的版本 | cases-02 发现与 D2-110 记录；cases-03 发现 #10 | 装置/可追溯性：引用分类版本须以 `this-task-classification.json` 与最新 `classification-N` 为准 |
| B-V14 | **知识候选（外部依赖型准备缺口）**：D2-110 的恢复条件写成“上游公开该实现后方可重试”，与 D2-107“需取得 `pet.dll`”构成一组“外部依赖型准备缺口”范例 | cases-02 D2-110 记录 | **知识新增候选**（用于区分“可补件恢复”与“需上游行为改变”的恢复条件写法） |
| B-V15 | **合法的 0 字节采集原件**：D2-109 与 D2-126 的 `02-conversion/observed-source-stderr.txt` 实测为 **0 行/0 字节**（源 stderr 确为空）；两者属“真实采集的空原件”，**不得与缺件混淆** | 本会话已 `read` 两个文件（均返回 `total 0 lines`）；交付契约 §1.1 L18 | 装置/记录（正面）：空原件须有对应采集记录；本审查按“空文件”单列，不计入缺件 |

## 5sexies. 批次自评文档（`batch/optimization-inputs-2.md`）与本区间事实的对照

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-W1 | **本区间两项 403 的根因不同**：D2-151 是 `caseId` 用旧前缀 ⇒ `identity_mismatch`；**D2-114 是提交时误用陈旧的 `this-task-classification.json`（旧的 BLOCKED `classification-1`）** ⇒ `403 public_network_unverified`，改用 `classification-2` 后通过 | 已逐字读 `events.jsonl` 第 658–662 行 | 已有规则落实（分类准入 §3 L47/L50；根 `SKILL.md` L24“每次提交再核冻结/分类”） |
| B-W2 | **装置故障类在区间内复现**：D2-111 的 `DEVICE_FAULT` 事件记“用 shell `printf` 生成 `job-01` 目标驱动 ⇒ `\n` 变真实换行 ⇒ `SyntaxError`，`target.c` 从未运行”，改写驱动后重提才得到 `matched`（0 次模型修复调用） | `events.jsonl` 第 650 行；`batch/summary.md` L40/L82；`optimization-inputs-2.md` §2.4 D-11 | 装置：D2-111 的 `matched` 是**修正装置后**的结果（有效），但该类故障（`operational-discipline` §16）在本区间确有发生，须在“有效 matched”判读时记录 |
| B-W3 | `optimization-inputs-2.md` 自称 **`events.jsonl` 有 2 行自身不可解析**（`:650` 含换行、`:915` 含未转义反斜杠路径，见其 §4.4 局限 3），而 §2.4 D-11 也记 D2-111 原始事件行含换行不可解析；但**本会话读到的 `events.jsonl:650` 是合法单行 JSON**（`\n` 为转义文本，内容为 D2-111 的 `DEVICE_FAULT`），`events.jsonl` 又被声明为只追加不改写 | 已读 `events.jsonl` 第 648–654 行；`batch/optimization-inputs-2.md` L210 与 L403；`summary.md` §1-H4 L326 | **未定**：可能该文档描述修正前状态，或该行曾被替换；本审查不据此断言事件流被改写，只登记“文档声称不可解析、当前文本可解析”的不一致 |
| B-W4 | **当时的 `PREPARATION_GAP` 处置与“只编译”档位的关系**：`optimization-inputs-2.md` §2.3 把 38 项（含 D2-107、D2-150）记为 `PREPARATION_GAP`，判据是“建入口即等于编造源行为”；同节**明确记载**多项 `coverageGaps` 请求“**per-item `LIB_UNOBSERVABLE_COMPILE_ONLY` 档位**（只编译不运行）作为合法终态” | 已读 `batch/optimization-inputs-2.md` L185–L201 | **已有规则落实（现行 §1.3 已提供当时所缺档位）**：这不是当年违反既有规则，而是当年缺该档位、批次自己提出需求、现行契约已实现；按现行规则，这些项应在源构建通过后继续生成并做目标语法/编译验证、记 PARTIAL（见 B-U2/B-T3） |
| B-W5 | **批次自设纪律 H7（“误生成的 `classification-1.json` 须删除”）与现行证据保留要求冲突** | `optimization-inputs-2.md` §2.7 H7 L250；`summary.md` §11.3 L514；现行任务状态 §1 L9、交付契约 §2.1.1 | 已有规则落实（历史纪律 vs 现行口径）；本审查不追改历史 |
| B-W6 | §2.4 D-12/D-13/D-15 记 D2-109（工具链/驱动夹带）、D2-116（`cp` 失败致 `probe.csproj`/`run_case.py` 未生成 ⇒ `MSB1009`）、D2-114（陈旧分类件）三项装置缺陷；与本区间已读事件一致 | `optimization-inputs-2.md` L211–L214；`events.jsonl` 658–660 | 装置：解释 D2-109/116 的 job 目录为何有缺失件（B-T5、cases-02 发现） |

## 5septies. 分块会话已回传的逐项发现（D2-151–D2-160，cases-04 发现 14–28）

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-X1 | **D2-151 的冻结记录被事后修订、且未记变体**：`frozen-inputs.md` L42 自注“方言依据（**冻结期修订，2026-10-11**）”，把目标标准从 `-std=c++17` 改为 `-std=gnu++17`；而它描述的两个 job 是 **2026-10-10**（`eval-20261010-155343…`、`eval-20261010-160404…`）。`result.md` L27 却称该命令“是冻结期就写明的命令，不是失败后的补救” | 已逐字读 D2-151 `frozen-inputs.md` 全文（82 行，含 L39–L44）；`result.md` L27；任务状态 §1 L9、§2.1 L43（改变实际契约须另记变体并重核受影响门槛） | **已有规则落实（规则要求变体记录；历史仅以行内注记标注）**；不得据此改判 `matched`，但“冻结条件与已执行 job 的对应”应记 UNVERIFIED/变体缺失 |
| B-X2 | **D2-151 job-00 的原判 `mismatched` 未在报告披露**：`job-00/returned-evidence/comparison.json` 显示 `behaviorVerdict="mismatched"`，`output` 为 `major changed`（源 `keep.txt\nsecond.txt\n` vs 目标空）、`filesystem` 两条 `major missing`（目标未删除 fixture）；`result.md` §4 只写该 job “源侧 build completed/0、execution completed/0”，item 的 `verdicts` 也只列 job-01 的 matched | 已逐字读该 `comparison.json` 全文；`result.md` §4；`items/D2-151.json` | **已有规则落实（评估准备 §5 L97：原平台 verdict 原样保留并与本项目结论分列）**；本次归因为旧占位 target 装置（非转换失败），但**未披露**属实 |
| B-X3 | **D2-152、D2-153、D2-154、D2-155 全缺 `result.md`** | cases-04 发现 14；与本会话全副本 198 份 result.md 清单一致 | 缺件（印证 B-D2 的 30 项） |
| B-X4 | **D2-152/153 的 manifest `Lines` 与冻结正文不一致**：D2-152 `502` vs frozen `561`；D2-153 `564` vs frozen `606`（另 8 项一致） | cases-04 发现 17；本会话已读 D2-152/D2-153 清单 | 未定（印证 B-T7；源正文已删，不能定案） |
| B-X5 | **D2-152–155 的 7 份 job 级 `batch-authorization.json` 逐项确认文本复写 D2-151**（“keep.txt/second.txt”） | cases-04 发现 18；与 B-U1/B-V1 并列 | 装置/流程（模板残留的**第五种**变体，普遍） |
| B-X6 | **D2-155 job-00b 的 `comparison_manifest.json` 目标构建命令拼写为 `gcc++`**（应为 `g++`；目标侧 SKIPPED 未执行） | cases-04 发现 19 | 装置（提交记录字段错误），未影响 verdict |
| B-X7 | **D2-155 分类 `cls=REVIEW_SENSITIVE`，但 job-00/00b `metadata.json` 写 `REVIEW_UNCERTAIN`**；该件 `signals.sensitive=[]`，由 `dynamic_code` 触发 | cases-04 发现 20 | 装置/可追溯性（与 B-T10/B-V13 同类） |
| B-X8 | **D2-153 分类 `has_network=true`/`network_mode=unresolved`，却 `requiresNetworkIsolation=false`**（`network_targets=[]`，未执行） | cases-04 发现 21；分类准入 §2 L38 | 装置/分类字段不一致（须回源核对，不手改分类 JSON） |
| B-X9 | **D2-151 item 内计数自相矛盾**：`usage.failedAttempts=0` 而顶层 `failedAttempts` 数组 1 条（403）；`codeRevisions=1` 而 `result.md` 记“无代码修订”、`selfRepairRounds=0`；`attempt-1-403.json` 原件**无 HTTP 状态码/时间字段** | cases-04 发现 24；本会话已读 `attempt-1-403.json`（仅 `detail.error/blockingReason/reason/action`） | 已有规则落实（根 `SKILL.md` L104 失败 attempt 记录）；计数不一致如实登记，**不擅自清零** |
| B-X10 | **D2-159（`utils.c`，c-to-csharp）引用仓库内不存在的 `extern.h`**（据 D2-153 的穷举结论），而其 `items/D2-159.json` 的 `disposition=FROZEN` 自述为“**declared convertible and in the queue**”，却**没有跑冻结 job、没有分类、没有源预检**（0 模型调用、`verdicts` 全 UNVERIFIED）。故该“可转换”断言是**计划标签而非经验证的结论**；同批 D2-156/157/158/160 同形 | 已逐字读 `items/D2-159.json`（31 行）；已 `glob` 确认 D2-159 无任何过程材料；cases-04 发现 26；任务状态 §3 L87（FROZEN 须先落盘 frozen-inputs.md） | **待核验 + 已有规则落实缺口**：恢复（平台已修）时应先跑源预检，而非沿用“declared convertible”；不得据此改判 disposition |
| B-X11 | 正面事实：D2-156–160 的 manifest `Sha256`（大写）↔ `classifier-input` ↔ `classification` details（小写）↔ item 逐项一致；D2-151 的 `this-task-classification.json` 与当前 `classification-1` 内容相同 | cases-04 发现 28 | 原件支持（身份核对通过） |

## 5octies. 分块会话已回传的逐项发现（D2-131–D2-140，cases-03 发现 19–31）

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-Z1 | **C# 源侧预检只用 `net48`，与项目基线 .NET 8 不符**：D2-131、D2-140 等的 `probe.csproj` 记 `net48`，而构建前提 §2.2 的项目基线是 **C# 12 / .NET 8**（`TargetFramework` 应冻结为本项目基线）；批次 §13 亦以 `net8.0` 为默认 | cases-03 发现 19；构建前提 §2.2 L82–L89；`summary.md` §13 L39 | 已有规则落实缺口（候选/TFM 选择未按现行基线；当时按 §13 的 net8.0 起步、后改 net48 的个案见 `summary.md` L84） |
| B-Z2 | **D2-136 的“无公开 TFM 可构建”超出已测证据**：本会话已逐字读 `items/D2-136.json`——`sourcePrecheck.buildCommand = "dotnet build -c Release probe.csproj (net48)"`、`diagnostics = ["CS0246 Index"]`，其**自己的 note** 写“System.Index **introduced in .NET Core 3.0**；absent from **net48**”，而 `coverageGaps` 却下结论“**no public TFM** can build it”。即：只实测了 `net48` 一个候选（且项目基线是 .NET 8），却外推到“所有公开 TFM”。（真正可能的 net8 失败原因——与 BCL `System.Range` 类型冲突——**未被测试也未记录**。）这与 C5（“BSD 断言必须覆盖 three 注册系统”）同型——**候选集合不足** | 已读 `items/D2-136.json` 全文 46 行；cases-03 发现 20；构建前提 §0.1 L34、§2.2 L82–L89；`pattern-note-bsd-userland-macos-correction.md` L21 | **已有规则落实缺口（方法）**：不得据单一候选否定“所有公开 TFM/系统”；本审查不改判历史 disposition，只登记该断言证据不足 |
| B-Z3 | **D2-133 的 `matched` 由 Agent 自写 `source/Driver.cs` 取得，且只覆盖 6 行常量/枚举输出**：本会话已逐字读其 `result.md`——L6 明写“按**纪律 §65** 补最小中性驱动 `source/Driver.cs`（**Agent 写**）”；L37 记该驱动“仅打印公开常量/枚举值 + 调用两个无副作用 API（`LocalFree(NULL)`、`CloseHandle(NULL)`）”；L54 自述 `ConvertSidToStringSid`/`GetTokenInformation`/`LookupPrivilegeName`/`QueryServiceObjectSecurity`/`OpenProcessToken` 的**运行期行为未被驱动**。其 `source/` 树因此变化并重分类（`classification-2`）。所引“纪律 §65”在现行 `operational-discipline.md`（§1–§17）**无对应条目**；现行评估准备 §1.3 L45 / §2 L53–L55 禁止 Agent 编写驱动，并已给出 `LIB_UNOBSERVABLE_COMPILE_ONLY` 替代路径 | 已读 D2-133 `result.md` 全文 55 行；cases-03 发现 21；评估准备 §1.3/§2 | **已有规则落实（历史做法与现行规则冲突）**：按现行规则，本项应在源构建通过后走 LIB 分支（生成 + `pwsh Parser` 语法验证 + PARTIAL、行为 UNVERIFIED），而不是自造驱动取得窄 `matched`。因此**不计入现行“有效 matched”**；原 verdict 照录、覆盖范围如实登记。D2-109、D2-128 同型 |
| B-Z4 | **D2-133、D2-140 重分类前的 `classification-1.json` 不在副本内**（D2-140 明记“已删除”） | cases-03 发现 22；交付契约 §2.1.1（重分类另存递增编号、不覆盖旧结果） | 缺件/已有规则落实冲突（同 B-T2/B-W5） |
| B-Z5 | **D2-131–140 全部 10 项的 `batch-authorization.json` 事由文本逐字写“该项 D2-088…”**（延续 cases-03 发现 6；与 B-U1/B-V1/B-X5 并列） | cases-03 发现 23 | 装置/流程（模板残留，**全区最普遍**） |
| B-Z6 | **D2-135 的诊断位置记录为 `L46/(46,…)`，原件为 `SharpCOM.cs(2,7)`** | cases-03 发现 24 | 装置/记录（定位信息不准确） |
| B-Z7 | **D2-134 的原判保留与报告一致性**：平台 `behaviorVerdict=mismatched`、`codeVerdict=failed`、`failure.type=CODE_RESULT(behavior)`，项目按装置态记 `PARTIAL`（保留原判）；且 `result.md` 对源 `stderr` 的描述**与原件不符**——本会话已逐字读 `02-conversion/observed-source-stderr.txt`（2 行，实际为“引发 Exception.ToString() 失败，因为无法打印异常字符串。”），而 `result.md` L39 写源 stderr 是 `.NET InvalidOperationException`（“控制台…无法读取键…”） | 已读 `observed-source-stderr.txt` 与 `result.md` 全文 59 行；cases-03 发现 25；评估准备 §5 L97–L99 | 已有规则落实（原 verdict 保留、装置归因）+ **报告与原件不一致**（登记，不改写：结论 `mismatched`/装置归因不变，但 stderr 描述应据原件更正） |
| B-Z8 | **D2-133/134 的 `target.gen.model.json` 仍是模型响应正文**（无调用级元数据/哈希；token 只在 item）；**D2-133 还缺 `02-conversion/request.system.txt`**（同类 D2-130/134 均有） | cases-03 发现 27、28 | 缺件/形制不一致（延续 B-H4、B-C7） |
| B-Z9 | **知识候选：`csharp-to-powershell` 方向页缺 P/Invoke / `Add-Type` 与 TFM 规则，且规则编号缺 `CS-PS-07`**（本批 D2-133/134 恰为互操作项） | cases-03 发现 29 | **知识新增候选**（需按 Skill 编写规范核版本后由维护侧决定；本审查不改 Skill） |
| B-Z10 | **方向收口计数矛盾再现**：D2-135 与 D2-136 都称“最后一项”，`6/6` vs `7/7` 不一致 | cases-03 发现 30；同 B-E9 | 未定/记录错误（跨事件与未定项口径） |
| B-Z11 | **长路径装置限制**（`Compress-Archive` 失败、须短临时目录打包、Python `open()` 须 `\\?\`）在 D2-139/140 再现；另 manifest 行数与 D2-131/133/134/135/136 冻结正文不一致（132/137–140 一致） | cases-03 发现 31；`optimization-inputs-2.md` §3.5 L334–L341 | 环境/装置 + 未定（延续 B-T7/B-T11） |
| B-Z12 | **D2-128 驱动问题第一手确认**：其 `result.md` L6 明写“按纪律 §65 补最小中性驱动 `source/Driver.cs`（**Agent 写**）”；首次 `job-00` 报 `CS5001`（无 Main，原件 `evidence-source-cs5001.json` 保留）后补驱动并重分类；`matched` 覆盖 5 行（`CurrentBuild=26200`、`.NETFramework` 子键名、计数 32、`[]`、`0`），`IsModifiableKey` **未驱动** | 已读 D2-128 `result.md`（前 45 行）；cases-03 发现 5；评估准备 §2 L53–L55 | 已有规则落实（历史做法与现行规则冲突，同 B-T6/B-Z3）；**另**：其匹配面含**宿主态值**（`CurrentBuild`），只对同一 VM 初态有效，属覆盖限制而非可复现 oracle 失败 |
| B-Z13 | **D2-109 驱动问题第一手确认**：其 `result.md` L25 自述“**我的驱动**”（Agent 写），L32 记装置**只**驱动 `FindFiles`；`CheckAccess`/`CheckModifiableAccess`（ACL）、`DecryptGPPPassword`（AES-256-CBC）、`ParseGPPPasswordFromXml`（GPP XML）**不在观察面**（仅编译）；`matched` 面为 `a.txt\nsub/c.txt\n`，两侧 `digest` 不同（`1f89460f…` vs `917995b3…`，CRLF vs LF）而 `normalized-text` 相同 | 已读 D2-109 `result.md` 全文 56 行 | 已有规则落实（同 B-T6）：`matched` 只覆盖 `FindFiles` 一条路径；ACL/AES/XML 业务义务**未验证**，不得计入完整功能覆盖 |
| B-Z14 | **驱动来源问题在本批次是系统性的（不只是 D2-109/128/133）**：本批的 job-01 驱动 `run_case.py` 均由 Agent 手工编写（`operational-discipline.md` §6–§8 正是为这些自写驱动立的规范）；D2-111 更实证“首次 job-01 驱动由 shell `printf` 生成致 `SyntaxError`、目标从未运行，**用文件写工具重写驱动**后同一 `target.c` 才 `matched`”。现行评估准备 §2 L53–L55 要求驱动来自用户或获批平台已提供的精确版本，Agent 不编写驱动 | `operational-discipline.md` §6 L32/§7 L45/§8 L55/§16 L561；`optimization-inputs-2.md` §2.4 D-11 L210；已读 D2-111 `result.md` L25–L35 | **已有规则落实（现行规则晚于批次，不能追溯改判）**：本审查**不**据此否定全部 matched，只把它记为**系统性限制**；其中 D2-109/128/133 另因**改动 `source/` 树**（新增 `Driver.cs`）而属更强的一类（B-T6/B-Z3） |
| B-Z15 | **D2-111 的 matched 覆盖极窄**：源自带入口（无需补驱动），但其“行为”仅实例化两个结构体并打印 3 行（2 个 magic 值）；`result.md` L39–L41 自述“**未解析任何 PE 文件**”“**结构体布局/大小不比较**”“除 3 行输出外的行为未被驱动” | 已读 D2-111 `result.md` 全文 45 行 | 已有规则落实（分层报告与覆盖缺口已如实登记）；**不得**把该 matched 说成 PE 结构体布局等价 |

## 5nonies. 分块会话已回传的逐项发现（D2-091–D2-100，cases-01 B-19..B-28）

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-19 | **6 项（D2-091/092/093/095/096/097）缺 `01-frozen/frozen-inputs.md`，其中 4 项仍有真实模型调用**（091 共 2 次、092 3 次、093 4 次、095/096/097 各 2 次）⇒ “分类前冻结回读”与“冻结→实际请求”关联**不可复核** | cases-01 B-19；与本会话 B-F1/B-F2 一致 | 缺件（冻结落盘门禁 §2.2）+ 请求/知识关联缺口（任务状态 §2.1） |
| B-20 | **同 6 项无 `02-conversion/target.gen.model.json`**（B-C2）⇒ **调用级原件**（模型名/参数/token/`finish_reason`/输入输出哈希、原响应）不可回读。**精化**：其中若干项的 `result.md` 自带**分轮用量表**（本会话已读 D2-092 `result.md` L36–L42：生成 3088/16987/15311、自审 4445/19427/17395、评估后修复 2099/1672/0），属**报告自述**而非原件，且无哈希可对账。**具体后果实例**：D2-097 的 item `usage` 三个 token 字段与 `result.md` 分轮表之和全部不符（4187 vs 2287+3829=6116 等），**无原件可定案** | cases-01 B-20 与异常 3；已读 D2-092 `result.md` | 缺件；本审查**不擅自改数**，只登记“报告自述 ≠ 调用级原件”与不可对账 |
| B-21 | D2-091 交付链末环**较完整**：`finalTargetSha256` 与 job-01 `targetHash`（`0aa47eb2…`）三处一致（优于 D2-088 的 B-08）；但生成轮原件缺失、`job-00b` 仍是占位目标 | cases-01 B-21 | 原件支持（正面）+ 缺件 |
| B-22 | D2-092/093 的**中间目标版本**只由 job `targetHash` 绑定（092 `2c6a07c3…`、093 `e75a403b…`），最终版三方一致 | cases-01 B-22 | 已有规则落实（版本关联 §2.1）；中间版本正文已删，不可复核 |
| B-23 | D2-091/092/093/095/096 沿用**旧“占位目标”预检装置**，job-00（091 含 job-00b）据此回传 `mismatched`/占位产物；对照 **D2-100** 已是 source-only 形态（目标侧 `SKIPPED`、`comparisonRef null`、`evidence_not_found`） | cases-01 B-23；评估准备 §1.1 L31 | 装置/形态断代：占位 mismatched **不得当转换失败**；D2-100 是现行形态的正面样本 |
| B-24 | **D2-092 的自审已给出 `REPAIR-RECOMMENDED`（risk 高）并定位到 `target.ps1:107` 的 `printf_pid:` 悬空标记**，目标仍被提交并取得 `mismatched`；修复发生在**评估后** | cases-01 B-24；`optimization-inputs.md` §F2 L110 | **已有规则落实（流程）**：自审找到有定位的转换引入缺陷时，现行单项闭环 §2/§4 允许有限修复后再提交；本项“先提交、后修复”多消耗一轮评估。缺陷本身已闭环（§6.1），此处只记流程差异 |
| B-25 | **D2-095 两侧原始字节数相差 1（源 58 B vs 目标 57 B）而平台判 `matched`**。本会话**已逐字读两侧 evidence**：`normalizedText` 完全相同（`{"case":"c2_advanced","state":"not_connected","resp":""}\n`），但 `sizeBytes` 58 vs 57、`digest` `7beba5e8…` vs `6ff6d91b…`。**人工点数**：该 JSON 文本本体为 **56 字符**，加 1 个 LF = **57 B**，加 CRLF = **58 B** ⇒ **源侧多出的 1 字节最合理解释是 CRLF，目标侧为 LF**，平台按 `normalized-text` 归一后判 matched。cases-01 原判读“目标是源合同字节、源侧采集少算末尾换行”**与本会话的字节计数不符**（若为少算，则源真实字节应为 57，与 `sizeBytes=58` 是原始字节计数的定义冲突），**该判读应记为未证实** | 已逐字读 `job-01/returned-evidence/evidence-source.json`、`evidence-target.json`（前 2000 字符窗口，`sizeBytes`/`digest`/`normalizedText` 均在窗口内）；对照 `full-review-comparison-and-statistics.md` §4.5（digest 生产者口径冲突） | **装置/平台口径实证**：`sizeBytes`/`digest` 与 `normalizedText` 是不同观察对象；本项是“原始字节不同而可比面相同”的具体实例，允许差异应登记为**行尾归一**，边界是“JSON 协议正文内容一致、仅行尾不同”；**不得**由 matched 反推原始字节一致，也**不得**由 1 字节差直接判转换失败（冻结策略为 `normalized-text`） |
| B-26 | **D2-093 的自审 `NO-REPAIR-IDENTIFIED` 未发现真实缺陷**，job-01 才由第三方暴露 payload hex 丢位（625 奇数位 vs 源 626 位，落点 `e8d00000` 后少一个 `0`）；其自审响应正文 JSON **损坏**（正则恢复、`reviewedScope` 缺失） | cases-01 B-26；`optimization-inputs.md` §F3 L111 | 已有规则落实（评估准备 §5：自审不代替第三方证据）；知识候选：hex 载荷逐位比对须量化后再交模型 |
| B-27 | **D2-096 的 fixture 声明与实际哈希不一致（本会话第一手确认）**：`01-frozen/classification-1.json` 为**多行可读** JSON，其 `details.files[]` 第 47–48 行声明 `"name":"a.txt"`、`"sha256":"5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"` —— 该哈希是 **`hello`（5 字节、无行尾）** 的 SHA-256；而 `request.system.txt` 按 cases-01 记录声明 fixture 内容为 `hello\n`（6 字节）。同时两份 `input_profile.json` 的 `fixtures` 为 `[]` | 已 `grep` 读 `classification-1.json` 第 47–48 行；cases-01 B-27；分类准入 §3 L48、评估准备 §4 L89 | 缺件/装置：**冻结声明的输入与胶囊实际输入不一致** ⇒ 该 `matched` 的输入身份不可完整回读；本审查**不改判 `matched`**，但把输入对应记 UNVERIFIED |
| B-30 | 修正说明：`classification-1.json` 在 D2-096 是**多行**文件（≥48 行），故“单行超长才截断”的分类必须逐文件判定（与 B-H2 澄清一致）；cases-01 对 D2-096 记 8 件截断，指的是其它单行证据件 | 本会话 `grep` 实测 | 装置（读取状态须逐件核） |
| B-28 | 本区间 **5 项自审响应非裸 JSON**（093 损坏、096 围栏+前言），按批次纪律 §2 用转义扫描/正则恢复；093/096 的条目字段不齐（无 `reviewedScope`/`location`/`evidence`） | cases-01 B-28；`optimization-inputs.md` §H2 L203 | 装置/模型输出格式：原文保留，恢复方式登记；**不据此报模型阻塞**，也不把恢复文本当完整结论 |
| B-29 | **D2-094/098/099 的方向差异同族**：三项均“0 模型调用、未提交、`sourceBuild UNVERIFIED`”；D2-094 的 unsafe 副作用与 D2-098 的 `WaitForSingleObject(...,-1)` 结构性不可终止属安全边界/驱动四要素的**正当阻断**，但“**未跑源构建**”仍与现行 §1.3「源可构建后继续生成」不符 | cases-01 异常 2；评估准备 §1.3 L41–L47、§2 | 已有规则落实（安全阻断正当）+ 现状与现行规则不一致（同 B-U2/B-T3） |

## 5decies. 分块会话已回传的逐项发现（D2-111–D2-120，cases-02 发现 21–41）

| 编号 | 事实 | 依据 | 分类 |
|---|---|---|---|
| B-AA1 | **D2-118 缺 `frozen-inputs.md`，其 `result.md` 却自称“冻结记录齐备”**（`01-frozen/` 实测仅 2 件） | cases-02 发现 21 | 已有规则落实（不实声明，同 B-C8/B-T2/B-V4） |
| B-AA2 | **D2-111 的 `frozen-inputs.md` 缺“授权与隔离”组** | cases-02 发现 22；交付契约 §2.1.1 L92 | 已有规则落实缺口（冻结字段不齐，同 B-U3） |
| B-AA3 | **同类 403 的证据留存不一致**：D2-151 留有 `attempt-1-403.json`；**D2-114 的 403 拒收没有任何 attempt 原件** | cases-02 发现 26；对照本会话已读 D2-151 `attempt-1-403.json` | 缺件：失败 attempt 应保留原文（根 `SKILL.md` L104）；不得据 item 记述单独定案 |
| B-AA4 | D2-116 job-00 有**两个 jobId 但只保留第二个的证据**，首个失败 job（`MSB1009`）诊断缺档（与 `optimization-inputs-2.md` §2.4 D-13 记载一致） | cases-02 发现 25；`optimization-inputs-2.md` L212 | 缺件（可追溯性） |
| B-AA5 | **D2-117 自审的 1 项“误判”拒绝在本副本内无法证伪**：其依据是“源第 87 行为小写 `Scheduledtasks.xml`”，而源正文已删；`full-review-knowledge-disposition.md` L47 已把该项列为“不能直接升级知识（未有大写路径精确源依据）” | cases-02 发现 29；`full-review-knowledge-disposition.md` §“已明确拒绝直接固化的建议” L47 | **未定/知识边界**：拒绝结论**方向正确**（源正文不可核，不能固化为知识），但**证伪本身也缺独立依据**；本审查两边都不采信为已证事实 |
| B-AA6 | **D2-116 的 `mismatched` 不止动态量**：结构段/结论行不同，且自审已定位 `AccessCheck` 首参（形参类型）缺陷；“oracle 不可冻结（停止该行为评估）”与“已定位转换引入缺陷应有限修复”两条规则**并存有张力** | cases-02 发现 30；评估准备 §4 L87、§5 L103 | **知识新增候选（口径顺序）**：建议明确“已定位转换引入”与“oracle 不可冻结”同时成立时的处置顺序；本审查不代为定案，原判保留 |
| B-AA7 | **D2-119 的 `result.md` L23 链接断链**：写 `../../../../../../SKILL.md`（指向不存在的 `docs/SKILL.md`），应上溯 7 级到仓库根 | cases-02 发现 32 | 装置（文档链接错误）；根 `SKILL.md` L10 等要求链接可达 |
| B-AA8 | **D2-118 的服务 `State` 差异归因合理**，可作“服务状态允许窗口”提案的正向实例 | cases-02 发现 31；`full-review-comparison-and-statistics.md` §2（主机/用户/进程/服务状态） | 原件支持（正向）；供比较策略侧参考，本审查不改平台配置 |
| B-AA9 | **分类器词法误判在本块复现 2 次**：D2-114 `requiresNetworkIsolation=true`（`using` 行）、D2-118 `network_mode=unresolved`+`has_network=true`，两者**仍 ALLOWED** | cases-02 发现 27；`optimization-inputs-2.md` §3.3 | 装置/分类器（与 §7 的“已解决出口”一致：回源核对 + 隔离证据重分类） |
| B-AA10 | **`evaluation_report` 留存形制不齐**：D2-116 job-01 只有 `.json`；D2-111/112 job-00 只有 `.md`；其余 7 项 job-00 两者皆无 | cases-02 发现 34 | 缺件/形制（同 B-T5） |
| B-AA11 | **D2-118 的 `timeoutSeconds=120`（其余 8 项 60）属正向按需冻结**（源执行约 15.8 s） | cases-02 发现 36 | 原件支持（正面：超时契约按实际需要冻结） |
| B-AA12 | **D2-111 的装置故障件与归因不一致**：存在 `job-1state-devicefault.json`，且 job-01 用 `job-id2.txt` 而非契约命名 `job-id.txt` | cases-02 发现 24 | 装置/形制（命名与归因不一致） |
| B-AA13 | **D2-111/116/117/118 的 `evaluator_manifest.json` 路径仍写 `docs/test/...` 旧路径**（与 B-R3 同源） | cases-02 发现 40 | 装置（历史指针） |
| B-AA14 | **manifest `Lines` 与项目记录不一致**：D2-117（206 vs 231）、D2-118（263 vs 301）、D2-119（256 vs 294）；D2-120 一致（309） | cases-02 发现 33 | 未定（延续 B-T7/B-X4/B-Z11） |
| B-AA15 | D2-112/114/115 与 D2-110 同型（.NET 运行时内部源文件 → `SOURCE_DEPENDENCY_GAP`）；D2-119（源语法残缺 → `SOURCE_NOT_BUILDABLE`）与 D2-120（`ApolloInterop` 快照外 → `SOURCE_DEPENDENCY_GAP`）的去向与诊断依据逐项相符 | cases-02 发现 37、38 | 已有规则落实（构建前提 §0.1 三类分列） |

## 6. 比较与统计（按 `full-review-comparison-and-statistics.md` 口径的**本区间**提案）

> 口径：**有效 matched + 有效 semantic_pass** 都计入“本项冻结观察范围和策略下的功能比较通过”小计；仍**分列两类数量**，并逐项列出未覆盖义务。原平台 verdict **一律原样保留**。本表数字已与 79 项 cases 记录逐项核对（`harness-b-cases-01..04.md`），并与 `batch/summary.md`、`optimization-inputs-2.md` §4.1 的批级计数一致；“有效”判定与未覆盖义务见各 cases 记录与 §6.3。

| 类别 | 本区间项数 | 项 | 前置有效性核对（摘要） |
|---|---:|---|---|
| 平台原判 `matched` | 12 | D2-088、091、092、093、095、096、097、109、111、128、133、151 | 原 verdict 一律照录 |
| 其中按现行规则可计“有效 `matched`”（提案） | **≤9\*** | D2-088、091、092、093、095、096、097、111、151 | 需逐项核“源侧非空非退化 + 输入实际送达 + 两侧对称 + 请求→响应→目标关联可回读”。**削减弱项**：D2-091/092/093/095/096/097 **缺 `target.gen.model.json`**（B-C2）⇒ 目标版本/响应关联 UNVERIFIED；D2-096 `comparison.json` 实测 `filesystem: not-applicable`（仅 `output` 一个适用维度），D2-095/097 同样只有 `output` 适用；D2-095 走“无监听 ⇒ not_connected”分支，D2-097 输出 `PID: 0`。**系统级限制**：本批 job-01 驱动均由 **Agent 编写**（B-Z14），现行评估准备 §2 不接受该来源；故此处“有效”只表示“**在冻结装置下的观察有效**”，驱动来源限制单列，**不追溯改判**原 verdict |
| `matched` 但**驱动来源不符合现行规则** | 3 | D2-109、D2-128、D2-133 | 源侧无入口，由 Agent 自写 `Driver.cs`（D2-109 另加最小 `.csproj`）后重分类取得（B-T6）。现行评估准备 §2 L53–L55 禁止 Agent 编写驱动 ⇒ **不计入现行“有效 matched”**；原 verdict 保留、覆盖范围如实登记（D2-128 仅覆盖该驱动 5 行输出） |
| 有效 `semantic_pass`（提案） | 6\* | D2-117、123、124、125、126、130 | 需逐项列被容忍差异与归因；已知多为 `执行时间`（`timestamps` 消噪）；D2-123 另有 1 次 `codeRevisions`；本块未见 Agent 自写驱动记载 |
| **比较通过小计（提案口径）** | **≤15\*** | 有效 matched ≤9 + semantic_pass 6 | 分母与“未覆盖义务”另列；**不是**全批转换成功率，也不覆盖未评估项；若某项“有效”判定不成立，继续下调并原标签照录 |
| 原判 `mismatched`（保留） | 3 | D2-116、118、134 | D2-116/118 为 `ORACLE_NOT_FREEZABLE`（主机态/PID/服务 State），D2-134 为 `PARTIAL_DEVICE`（`Console.ReadKey` 无控制台）；均**归因装置/环境**，非转换失败，**不自行改判** |
| `PARTIAL`（未评估/仅局部） | 9 | D2-089、090、094、098、099、101、116、118、134 | 089/090/094/098/099/101 为 `ORACLE_NOT_FREEZABLE`（0 输出/API 地址/动态 PID/会注入等）；0 模型调用 |
| `WAITING` | 8 | D2-082、083、108、156、157、158、159、160 | 082 `RUN_SAFETY_NOT_READY`；083 真实公网 `BLOCKED`；108 `RUN_SAFETY_NOT_READY`；156–160 `BLOCKED_ENV`（已修复，待恢复） |

\* 数字已按 79 项 cases 逐项核对；若某项“有效性”判定不成立，按提案移出通过小计、原标签照录并记 UNVERIFIED/策略疑点。**通过小计不是全批转换成功率**，分母（全部适用行为项、实际可判项、仅编译项）见 §6.2 归因与 §9 覆盖状态。

### 6.0 本会话第一手核实的生命周期/维度事实（抽样但逐字读原文）

- **D2-095 job-01**（`evaluation_report.json` 前 2000 字符）：源与目标两侧 `preflight=PASSED/attempts=1`、`cleanup=PASSED/attempts=1`、`contaminated=false`、`environmentStatus="clean"`、`runnerStateAfter="READY"`；`applicableDimensions=1 / observedDimensions=1 / matchedDimensions=1`、`behaviorVerdict=matched`；`comparison.json` 显式列出 `filesystem/processes/registry/network` 四个维度均 `not-applicable`。
- **D2-128 job-01**（`comparison.json` 全文）：`behaviorVerdict=matched`、`output` 唯一 `applicable/observed`、`diffs=[]`；其余四维 `not-applicable`。其驱动来源问题见 B-T6。
- **D2-091 job-01**：见 B-E14（两侧 `exitCode=4294967295`、stdout 均 29 B、`output` 维度 `diffs=[]`）。
- **D2-088 job-01**：`comparison.json` 全文中 `output` 唯一适用且 `diffs=[]`；其 `filesystem` 亦为 `not-applicable`（cases-01 B-10 记“文件字节义务仅静态支持”）。

### 6.1 本区间经第三方证据坐实并已闭环的转换缺陷（**历史事实，不作为现行故障**）

> 依据 `batch/optimization-inputs.md`（前篇）§F2/§F3 与各 item 的 `repairChain`/`selfRepairRounds`；本会话已抽查 D2-091/095/096/097/128 的 `comparison.json`/`evaluation_report.json` 作为对照。

| 项 | 缺陷（第三方观察坐实） | 定位/修复 | 复测 | 判读 |
|---|---|---|---|---|
| D2-092 | 目标第 107 行**悬空标记 `printf_pid:`** 被 PowerShell 当命令执行 ⇒ stderr 非空、退出码非 0（stdout 已匹配） | 删除该行（单行 diff） | job-02 `matched` | 转换引入的真实缺陷，已闭环；**不得**当作现行故障重复登记 |
| D2-093 | payload 十六进制**少一位**（目标 625 位奇数 vs 源 313 字节=626 位、以 `00` 结尾）⇒ `Substring` 越界 @`target.ps1:54`；第 1 轮修复未收敛 | 定位到 `e8d00000` 之后少的那个 `0` | job-02 `matched` | 同上；来源 `optimization-inputs.md` §F3 |
| D2-088 | **CRLF（行尾字节）**义务未保持 | 自修 1 轮补齐 CRLF（`selfRepairRounds=1`） | job-01 `matched` | 同上；其 `filesystem` 维度为 `not-applicable`（B-10），文件字节义务仅静态支持 |
| D2-123 | `REG_EXPAND_SZ` 未展开（自审发现，属“潜在漏报”型忠实性修复） | 按纪律机械应用模型补丁（`ExpandEnvironmentStringsW`），`codeRevisions=1` | **本环境未观察到该修复效果**（baseline 全为 `REG_SZ`） | 已如实记未验证（cases-03 发现 17，属正面例：未把未观察的修复标为“已验证解决”） |
| D2-116 | 目标 `AccessCheck` 形参类型疑似错误 ⇒ ACL 判定疑似不等价（源 98 行风险项 vs 目标 12 行 0 命中） | **未修复**（oracle 不可冻结，无从判收敛） | job-01 `mismatched`，原判保留 | **待核验，不记已证实缺陷**；不得据不可冻结下的 mismatched 判等价或不等价 |

### 6.2 归因结论（本区间）

- **转换引入（已闭环）**：D2-088、D2-092、D2-093。
- **转换引入（疑似、未定案）**：D2-116（ACL 谓词）。
- **环境/装置**：D2-090（源执行超时）、D2-111（printf 换行驱动故障）、D2-114（陈旧分类件 403）、D2-109/D2-116（工具链/驱动夹带）、D2-134（`ReadKey` 装置态）、D2-116/D2-118（主机运行态不可冻结）、D2-089/090/094/098/099/101（观察不可冻结/会注入或起进程）、D2-103/104/105/106/107（旧占位 target 双跑）、D2-152–160（长路径、C# 目标平台缺陷）。
- **源已有/源侧**：D2-110/112/114/115/121/122/129/136（.NET 运行时内部）、D2-119（源自身残缺）、D2-081/084–087（Abseil 头）、D2-120/127/131/132/135/137–149（外部/同项目依赖）、D2-152–155/161…（BSD 平台接口）。
- **未定**：Abseil/SharpUp 的“打包缺口 vs 快照外依赖”（B-B3、B-T13）、manifest 行数差异（B-T7/B-X4）、events 可解析性（B-W3）。

### 6.3 已可点名的未覆盖义务（不因 matched/semantic_pass 而消失）

- D2-151：仅覆盖 `argv=[-v,keep.txt,second.txt]`；`-i/-I` 交互、`-r/-R` fts 递归、目录参数、`-f` 幂等、`unlink` 别名、`-W/-d` 与全部错误路径未覆盖。
- D2-111：仅覆盖 3 行输出（2 个 magic 值）；**未解析任何 PE 文件**、**结构体布局/大小不比较**（B-Z15）。
- D2-109：仅驱动 `FindFiles`；ACL（`CheckAccess`/`CheckModifiableAccess`）、AES（`DecryptGPPPassword`）、GPP XML 解析未驱动，目标实现**仅编译**（B-Z13）。
- D2-128：`IsModifiableKey` 未驱动；匹配面含宿主态 `CurrentBuild`（只对同一 VM 初态有效）（B-Z12）。
- D2-133：仅常量/枚举 + 两个无副作用 API；`ConvertSidToStringSid`/`GetTokenInformation`/`LookupPrivilegeName`/`QueryServiceObjectSecurity`/`OpenProcessToken` 运行期行为未驱动（B-Z3）。
- D2-096：`filesystem` 维度未比较（manifest 含绝对路径）。
- D2-117：隔离 VM 无 GPP 缓存 ⇒ 只走到“未发现”分支。
- D2-124：VM 未设 `AlwaysInstallElevated` 策略 ⇒ 只覆盖非命中分支。
- D2-118：服务 `State` 为运行期环境量 ⇒ 21 个周期性服务差异不可冻结。
- D2-134：`ReadKey()` 无控制台 ⇒ 退出码/stderr 装置态不可比。
- 其余逐项覆盖缺口以 cases 文件为准。

## 7. 对照现行规则“已被解决”的历史问题（列具体依据，不沿用旧问题清单）

| 历史问题 | 现行依据 | 状态 |
|---|---|---|
| 分类 `caseId` 带批次/前缀导致 403 `identity_mismatch`（本区间 D2-151 的 `attempt-1-403.json` 即此） | 分类准入 §3（L47）明确平台按 `source/` 文件集合做 identity 门禁，`caseId` 必须等于分类 `case`；`items/D2-151.json` 已记录“重提 `caseId=D2-151` 后 202 通过” | 已解决（流程已固化） |
| 源侧驱动/源集合变化未重新分类 | 分类准入 §3 L50 列出四类重新分类触发项；本区间 D2-091（argv 重冻）、D2-092/093（评估后修复）、D2-109（net48）、D2-123（codeRevisions=1）均有 `classification-2` 迹象，须逐项核 | 已解决（规则存在），落实待逐项确认 |
| `source_hash_mismatch` 由十六进制大小写引起 | 分类准入 §3 L58：当前分类器比较时统一小写并处理 `sha256:` 前缀，**不能**把大小写不同直接认定为字节不同 | 已解决（实现与规则一致）；历史 A4 说法只适用其当时的实现 |
| 打包缺口被误判为 `SOURCE_DEPENDENCY_GAP` | 构建前提 §0.1 L45/L50；BSD 追加节给出“仓库内是否有可补齐来源”的第三问 | 已解决（规则存在）；本区间 Abseil 簇缺该穷举记录（见 B-B3） |
| BSD 源码被判 `SOURCE_NOT_BUILDABLE` 时未测 macOS | 构建前提 §0.1 L34；`pattern-note-bsd-userland-macos-correction.md` | 已解决（追加更正，不改写历史） |
| 从 item/平台标签外推功能通过 | 评估准备 §5 L97–L99；任务状态 §4 L108；根 SKILL.md L27 | 已解决（分层报告为现行要求） |
| 分类器把 `using` 行 / 版本号（`4.0.0.0`、`1.0.0.0`）/ 帮助文本示例 IP 当公网目标 | 分类准入 §2 L38：`public_network_unverified` 的正规出口是“取得真实隔离证据后**重新分类**”；`optimization-inputs-2.md` §3.3 已把该形态列为高频并给出排除建议 | 已解决（规则与处置一致）；本区间实例：D2-114、D2-121、D2-122、D2-140、D2-150（逐项见 cases） |
| `source/` 树变化后未重新分类 | 分类准入 §3 L50 四类触发项；`optimization-inputs-2.md` §2.7 H8 | 已解决；本区间 D2-091（argv 重冻）、D2-128/133（补 `Driver.cs`）均有 `classification-2` |
| 提交时使用陈旧分类件导致 403 | 分类准入 §3 L58 + `optimization-inputs-2.md` §2.7 H7（`this-task-classification.json` 必须写最新）；本区间 D2-114 实例已有事件原文 | 已解决（规则与事件一致）；但 H7 的“删除误生成 classification-1”与现行证据保留冲突（见 B-T2/B-W5） |
| 目标 `artifactLanguage` 与方向不一致 | `platform-blocker-csharp-target.md` L12（须写 `csharp`，写 `dotnet` 会 403）；本区间 D2-087 的 job-00 把 cpp-to-go 的目标写成 `csharp`（cases-01 B-18） | **部分解决**：方向自洽要求已明文；本区间仍见字段错误，属记录缺陷（源构建失败、目标侧 SKIPPED，未影响 verdict） |
| 把“快照外依赖”与“数据集内未打包/可补齐”混为一谈 | 构建前提 §0.1 L45/L50 三问；`pattern-note-bsd-userland.md` 追加节 | 已解决（规则存在）；本区间 D2-100、D2-102 有“穷举 0 命中”证据，**Abseil 簇（081/084–087）与 SharpUp 簇缺该证据记录**（B-B3、B-T13） |
| `Console.ReadKey()` 结尾的 C# 源其 `stderr` 无字节可比性、被判 `mismatched` | `operational-discipline.md` §14 L511；评估准备 §5 L95–L99 | 已解决（归因装置/运行时、保留原 verdict、只据 stdout 判定质量）；本区间 **D2-134** |
| 输出含真实耗时/主机运行态 ⇒ 不可复现 ⇒ 记 `ORACLE_NOT_FREEZABLE` | `operational-discipline.md` §15 L535、§10.16 L267；评估准备 §4 L87 | 已解决（PARTIAL + UNVERIFIED、不重复重提求变绿）；本区间 D2-116、D2-118、D2-134 |
| 任一侧非零退出且 stdout 为空时误归因转换 | `operational-discipline.md` §16 L561；评估准备 §5 L103 | 已解决（先排除驱动/装置）；本区间 D2-111 即该型（B-W2） |
| 分类器暂存目录常驻仓库根 | `operational-discipline.md` §11 L181；分类准入 §1 L13 | 已解决（暂存目录须在仓库外、取回即删）；本区间未见残留（副本内无 `.tmp-classify-*`） |

## 7bis. 批次自设纪律 ↔ 现行契约锚点对照（用于判断“历史问题是否已由现行规则解决”）

> 批次自设纪律在 `batch/operational-discipline.md`（§1–§17）与 `batch/optimization-inputs-2.md`（H7/H8、§65 等）。**它们是当时的执行底稿，不是当前真源**；下表给出当前真源位置与结论。

| 批次纪律（行号） | 主题 | 现行真源 | 关系 |
|---|---|---|---|
| §6 L32 / §7 L45 / §8 L55 / §10.13 L203 | 驱动原字节透传、按目标形态启动、argv 原样转发、两侧后处理一致 | 评估准备 §2 L57–L68 | **一致**，现行以“驱动必须来自用户/获批平台的精确版本”收紧了来源要求 |
| §9 L64 / §10.20 L431 | 判“快照外文件”前查旧数据集；分类输入哈希大小写敏感 | 构建前提 §0.1 L45/L50；分类准入 §3 L58 | 前半**一致**；后半**已更新**——现行分类器统一小写并处理 `sha256:`，且明确不得用当前实现反推历史 `source_hash_mismatch` |
| §10.6 L107 / §10.10 L159 | “两侧未观察”不构成 `matched` 证据；相同的失败输出也算 matched | 评估准备 §5 L95–L99 | **一致**（现行明确两侧空输出/同一驱动失败标记不能单独支持 matched） |
| §10.15 L245 | `semantic_pass` 独立档位 | 评估准备 §5 L97；比较提案 §3 | **一致**；现行另允许与 matched 合计入“比较通过小计”（本文件 §6 按该提案分列） |
| §10.16 L267 / §15 L535 | oracle 不可冻结（含 `duration_ms`） | 评估准备 §4 L87 | **一致** |
| §10.17 L309 | 契约缺陷（加标志）vs 真实缺陷（改代码）分离 | 构建前提 §4.1 L142 | **一致** |
| §12 L466 | `caseId` 必须等于分类 `case`（源自 **D2-151**） | 分类准入 §3 L47 | **一致**，已升为契约级 |
| §13 L490 | C# **源**须补最小中性 `.csproj` | 构建前提 §3 L109–L124 | **一致**（三条硬性要求） |
| §14 L511 | `Console.ReadKey()` 的 C# 源 stderr 无字节可比性（源自 D2-022/023；本区间 **D2-134** 同型） | 评估准备 §5 L95–L99 | **一致**（归因装置/运行时，保留原 verdict） |
| §16 L561 | 任一侧非零退出且 stdout 为空时先排除驱动/装置 | 评估准备 §5 L103 | **一致**（本区间 D2-111 即该型） |
| §17 L585 | 独立源预检走 source-only，`buildCommand` 为 argv token 数组 | 评估准备 §1.1 L18/L31；`batch/summary.md` L145 | **一致**（本区间 D2-152–155、D2-156–160 仍用旧双侧形态，属形态断代） |
| **批次 §65**（见 `optimization-inputs-2.md` §2.3 L199/L261） | “库单元建入口即编造源行为 ⇒ 记 `PREPARATION_GAP`、0 模型调用” | 评估准备 §1.3 L41–L47；任务状态 §3 L96 | **已被现行 `LIB_UNOBSERVABLE_COMPILE_ONLY` 分支取代**：现行要求在源构建通过后**继续生成**并验证目标语法/编译、记 PARTIAL。本区间受影响项见 B-U2/B-T3 |
| **批次 H7**（`optimization-inputs-2.md` §2.7 L250） | 误生成的 `classification-1.json` 须删除 | 任务状态 §1 L9；交付契约 §2.1.1 | **冲突**（现行要求保留已发生分类结果、重分类另存递增编号）。本区间实例：D2-114/121/122/140/150（见 B-T2、B-V?、B-X） |
| **批次 §16/`D-11`**（`optimization-inputs-2.md` §2.4 L210） | shell 生成驱动导致换行转义故障 | 评估准备 §2（Agent 不写驱动，故该类故障在现行下不应发生） | **已被规避**：现行禁止 Agent 编写驱动，故该故障类的根因消失 |

## 8. 知识候选（不直接固化错误自审）

- 本区间 49 项有 `result.md`、多数有 `self-review-1.json`（部分含 `self-review-1.model.json` 元数据）。逐条 scope/risk/unresolved/verdict/修订以 `harness-b-cases-01.md`…`04.md` 为准（待回填）。
- 批级知识去向见 `full-review-knowledge-disposition.md`；其中与本区间直接相关的判定：**D2-103**（“非 NULL 空串被说成 getenv 的 missing fallback”）与 **D2-123**（“以 `os.ExpandEnv` 等同 Windows 展开”）已列为**不能直接升级知识**；**D2-117**（“大写路径建议”）亦列为**未有精确源依据、不直接固化**。本审查不重复把这些错误自审当新故障，也不把它们固化为知识。
- 本审查**不**新增知识正文、不修改任何 Skill。

## 9. 覆盖完成状态

| 分块 | 状态 |
|---|---|
| cases-01：D2-081–D2-090、D2-091–D2-100（10+10） | ✅ 完成（925 行） |
| cases-02：D2-101–D2-110、D2-111–D2-120（10+9，无 D2-113） | ✅ 完成（557 行） |
| cases-03：D2-121–D2-130、D2-131–D2-140（10+10） | ✅ 完成（437 行） |
| cases-04：D2-141–D2-150、D2-151–D2-160（10+10） | ✅ 完成（434 行） |
| `batch/items` + `events.jsonl` 交叉核对（79 项） | ✅ 完成（专项会话） |
| `harness-b-coverage.md` 逐项文件清单（按 glob 重建） | ✅ 完成（**COMPLETE**；79 项逐项文件清单；现存 **1393** 件；审计差异 **19** 条；未读集合为空） |

**逐项审阅 79/79 项完成**（D2-081–D2-160，无 D2-113）；**未读集合：无**（分块会话逐件读入各自范围内的全部现存文件；单行超长件按 `已读(截断)` 登记）。
**已完成交付物**：`harness-b-coverage.md`（COMPLETE）、`harness-b-findings.md`（本文件）、`harness-b-cases-01.md`…`harness-b-cases-04.md`。
**注意（B-H6）**：coverage 的计数以独立 `glob` 为准，不以各 cases 文件自报的“现存文件数”为准（19 项存在差异，已逐条列入 coverage 的「审计差异」）。
