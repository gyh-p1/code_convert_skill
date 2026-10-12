# harness-E 增补读取记录（官方读取上限提高后）

> 状态：**IN_PROGRESS — 不得当作 COMPLETE**。本文件是 [coverage](harness-e-coverage.md) 的增补，记录“官方把单行读取与 readMaxBytes 上限提高到 1048576 后”对**此前 read/grep 截断原件**的真实补读。
> 前置核对：已读 [harness-acceptance-index.md](harness-acceptance-index.md)。E 组范围 = `D2-278`…`D2-300` **实际 23 项**（6+73+79+62+34+23=277，编号区间长度不等于项数）。本轮**只**继续 E 组，未读 A/B/C/D/Codex 范围。
> 边界：只用原生 `read`/`glob`/`grep`。**未**写/运行任何脚本或程序；**未**运行样本/目标/构建/分类器；**未**调用转换模型；**未**提交评估；**未**访问 `D:/CodeConvertRemote/Stack` 及 `jobs`；**未**读 `.env`/密钥/凭证；**未**改任何原始证据、`items/events`、旧报告、状态、自审；源码/目标仍为已删状态，**不恢复**。
> 上限生效实证：`D2-278`…`closure.json` 本次读到行尾完整内容（含 `"oracleStatus":"UNVERIFIED","programOutputProvenance":"UNVERIFIED","checkedAt":…`），此前同文件在同一工具下被截断于 `"ora…`。**截断已真实解除**（对本轮已读文件而言）。

## 1. 本轮真实补读清单（每件为独立 read 调用）

| # | 文件（相对 `../../../<direction>/<case>/output/batch/04-evaluation/job-00-source-buildability/`） | 读取结果 | 新读到（此前被截断）的字段 |
|---:|---|---|---|
| 1 | `ruby-to-c/D2-278-ruby-open3.rb/…/closure.json` | **read 完整** | `oracleStatus=UNVERIFIED`、`programOutputProvenance=UNVERIFIED`、`checkedAt=2026-10-12T05:43:17.294392+00:00` |
| 2 | `ruby-to-python/D2-300-ruby-credential_collector.rb/…/returned-evidence/evidence-source.json` | **read 完整** | `observations.{filesystem,processes,registry,network}`、`coverage.dimensions`、`collectorDiagnostics=[]`、`createdAt=2026-10-12T06:13:58Z` |
| 3 | `ruby-to-go/D2-290-ruby-chrome_cookies.rb/…/evidence-source.json` | **read 完整** | 同上结构；`createdAt=2026-10-12T05:59:16Z`；execution stderr `sizeBytes=138`、digest `9aea925d…` |
| 4 | `ruby-to-go/D2-290-ruby-chrome_cookies.rb/…/closure.json` | **read 完整** | `oracleStatus/programOutputProvenance=UNVERIFIED`、`checkedAt=2026-10-12T05:59:47.220841+00:00`、完整 digests |
| 5 | `ruby-to-go/D2-291-ruby-observer.rb/…/evidence-source.json` | **read 完整** | `observations` 五维、`coverage.dimensions`、`createdAt=2026-10-12T06:00:53Z` |
| 6 | `ruby-to-go/D2-291-ruby-observer.rb/…/closure.json` | **read 完整** | `checkedAt=2026-10-12T06:01:24.152381+00:00`、完整 digests |
| 7 | `ruby-to-go/D2-288-ruby-enum_services.rb/…/closure.json` | **read 完整** | `checkedAt=2026-10-12T05:57:10.662310+00:00`、完整 digests |
| 8 | `ruby-c…`（见下“仍未读”） | — | — |

## 2. 补读得到的新事实（原截断处不可见）

1. **`closure.json` 尾部三字段**（原先完全未读到）：`"oracleStatus":"UNVERIFIED"`、`"programOutputProvenance":"UNVERIFIED"`、`"checkedAt":"<ISO 时间>"`。已读到的 5 件 closure（D2-278/288/290/291 及 D2-300 见下）**全部为 `UNVERIFIED`**——与 `evaluation_report.json` 的 `baselineAssessment.status=UNVERIFIED`、报告正文 `Frozen source obligations: UNVERIFIED` 一致，**不存在**“closure 声称 oracle 已验证”的情形。
2. **`evidence-source.json` 的观察维度是五维固定骨架**：`observations.{output,filesystem,processes,registry,network}` + `coverage.dimensions` 同名五项。本批实际只有 `output=observed`，其余四项 `not-applicable`；其中 `registry` 与 `network` 明确带限制串 `"evidence dimension is outside the current release scope"`。⇒ **“程序输出”之外的文件系统/进程/注册表/网络副作用在本轮平台能力内根本没有采集**，任何“行为未评估”的判断因此有平台侧依据，而非仅凭空输出。
3. **`collectorDiagnostics":[]`（空）**：本批已读到的 4 件 `evidence-source.json` 均无采集器诊断，说明**没有**平台侧采集异常记录；这一点此前完全不可见，现可排除“采集器报错导致空输出”的替代解释。
4. **`createdAt`（bundle 级）与 `checkedAt`（closure 级）成对存在**：如 D2-278 bundle `createdAt=2026-10-12T05:43:17.270710+00:00`（report）与 closure `checkedAt=05:43:17.294392+00:00` 相差约 24ms，且 `controller.log` 的 `finished` 行为 `05:43:17.295392`——三者时间线自洽。
5. **D2-290 的报告缺件性质被确证**：其 `closure.json` 记录了 `evaluation_report.json` 的摘要 `sha256:e0024097e32606f11eae2fa9e37de65a3ff6c410407a1269d04fa589033e2503` 与 `.md` 的 `sha256:aabac05f…`，而本地同路径文件是 `{"detail":"job_report_not_found"}` 占位。⇒ **远端确有报告、本地为取回失败**（findings F6 由此从“推断”升为“原件支持”）。
6. **D2-290 的 `execution.stderr` 全文**：`chrome_cookies.rb:6:in '<main>': uninitialized constant Msf (NameError)` + `class MetasploitModule < Msf::Post`，`sizeBytes=138`、`digest=sha256:9aea925d…`、`truncated=false`。与 result.md 引用一致。
7. **D2-300 的 `observations.output.events=[]` 且 `limitations=[]`**：`status=observed` 但**零事件**，即“观察维度被打开、却没有任何输出事件”。这支持 `PREPARATION_GAP`/无观察内容的判断，同时说明 `observed` 命名指的是**维度已启用**而非“有可比较内容”。

## 3. 仍未读（本轮未完成部分，逐件列出）

- **仍未补读的 34 件（每项 `evidence-source.json` 与 `closure.json` 两件 × 17 项）**，其读取状态保持 `read(截断)`：
  `ruby-to-c/D2-278/evidence-source.json`；
  `ruby-to-cpp/D2-279, D2-280, D2-281, D2-282` 各 2 件；
  `ruby-to-csharp/D2-283, D2-284, D2-285, D2-286` 各 2 件；
  `ruby-to-go/D2-287/evidence-source.json, D2-287/closure.json, D2-288/evidence-source.json, D2-289/evidence-source.json, D2-289/closure.json`；
  `ruby-to-powershell/D2-292, D2-293, D2-294, D2-295, D2-296` 各 2 件；
  `ruby-to-python/D2-297, D2-298, D2-299` 各 2 件、`D2-300/closure.json`。
- **仍未核的 5 个报告占位项**（D2-286、D2-287、D2-290、D2-291、D2-294）：其 `evaluation_report.json`/`.md` 本地为占位，**真实报告正文仍未读到**（closure 只给摘要）。补读上限不能解除这一缺口——它是**取回失败**，不是工具截断。
- **仍未回传的件**：`evidence/source-{call,identity,request,response.body,response}.json`、`request.json`、`lifecycle.jsonl`、`staging-manifest.json`（各 closure 的 `artifactDigests` 有名、目录内无文件）。
- **仍未核的旧状态原件**：`items/D2-*.json`、`events.jsonl`、自审与状态——按任务约束不改不核。
- **仍未做的工具动作**：`glob` 分页/spill 完整清单核对（本轮`glob`结果未超限，故未触发；但按要求**不把 100 条上限当全文件集**，若后续出现截断须读 spill 文件）。

## 4. 对原 coverage/findings 的修订口径

- 原 coverage 把 46 件登记为 `read(截断)`。本轮已把其中 **8 件**改为 `read 完整`（见 §1），其余 **38 件**仍为 `read(截断)`；**总数不变**（23 项 × 15 件 = 345 件）。
- findings F8（截断为工具级结构性未读）**部分解除**：截断本身已被官方配置解除，**未解除的是“尚未逐件补读”**——两者必须分开记，不能因上限提高就宣称已读。
- findings F6（报告占位 + `controller.log` 无 finished 行）**升级为原件支持**（D2-290 closure 摘要为证）；但“远端报告正文”仍属未读。
- findings F1（报告层字段名与真实退出码分离）**获得加强**：`closure.json` 的 `oracleStatus=UNVERIFIED`/`programOutputProvenance=UNVERIFIED` 说明连平台自己的闭环记录都明确标注未验证，**不得**用 `complete:true` 代替验证结论。
- 源码/目标已删带来的不确定性**不因本次全文补读而解除**：`Lines` 口径、`sha256sum 实测一致`、静态画像中的行号断言仍不可回算。

## 5. 完成判据

本文件与 coverage 在**全部 46 件补读完毕且无占位/未回传项被误当已读**之前，一律保持 **IN_PROGRESS**；不得输出“E 组全量审阅完成”。
