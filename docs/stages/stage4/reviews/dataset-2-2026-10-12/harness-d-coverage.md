# Harness D 覆盖清单（D2-241…D2-277 数值区间 + batch 层全量原始材料）

> **状态：COMPLETE（正文阅读）/ 逐文件名清单登记为部分** —— 34 个用例目录现存 667 件、batch 层全部文本件、**`batch/items/*.json` 全 277 份**（136 + 141 两段）均已逐件读完；**原被 2000 字符单行上限截断的全部原件已于补读阶段全文重读（34/34 项，0 件残留）**，见 §3.2。检查点 1/2 与 items 全段清点达标（§5）。
> **唯一未完成的子项**：§3.3 的「逐文件名枚举」为**部分**——补读阶段 `glob`/`grep` 工具已不可用，无法再机器枚举 667 件；已按本会话实际 `read` 的真实文件名逐项列名，缺口如实登记。
> 任务定义见 [harness-d-task.md](harness-d-task.md)。方法：只用 read/glob/grep 手工逐件阅读；**未编写、未保存、未运行任何分析脚本/哈希/统计工具**；未编译、未运行、未调用模型、未提交评估、未改任何原证据。
> 逐项正文见 [cases-01](harness-d-cases-01.md)（241/243/245/246/247）、[cases-02](harness-d-cases-02.md)（249–254）、[cases-03](harness-d-cases-03.md)（255–261）、[cases-04](harness-d-cases-04.md)（262–268）、[cases-05](harness-d-cases-05.md)（269–274）、[cases-06](harness-d-cases-06.md)（275–277）；批次层见 [batch-records](harness-d-batch-records.md)；结论见 [findings](harness-d-findings.md)。

## 0. 方法与已知环境限制（如实登记）

| 项 | 事实 | 依据 |
|---|---|---|
| 只读工具 | `read` / `glob` / `grep` 手工分段阅读；未用任何脚本或哈希/统计工具 | 本会话工具调用 |
| **pwsh 不可用** | `pwsh` 每次调用在启动阶段即失败：`Error: SetNamedSecurityInfoW failed (Win32 5): grantWrite(E:\桌面文档\Agents System\code_convert)`（沙箱 ACL 授予失败）。`Get-Content` 路线**不可用**；已试 3 次（含指定 workdir） | 工具回执 |
| 单行截断 | 首轮：`read`/`grep` 对**单行 >2000 字符**显示 `(line truncated to 2000 chars)`，区间内大量 `closure.json`/`evidence-source.json`/`evidence-target.json`/`evaluation_report.json`/`*.model.json`/`attempt-1-truncated.json` 只能读前缀。**补读阶段**：官方 dsh 文本展示配置补丁把上限提到 1048576，同一批文件**已全部全文补读**（见 §3.2） | 工具回执 |
| **工具可用性变化（补读阶段）** | `glob` 与 `grep` 在本会话补读阶段**已不可用**（调用返回 `unknown tool`），仅 `read` 可用；因此**无法再对 667 件做机器枚举**，早期方向级 glob 的 spill 清单在本会话亦不可读 | 工具回执 |
| 源/目标已删 | 34 个用例目录下**均无 `source/`、无 `target*`、无 `.zip`/capsule**（glob 实测仅 `output/batch/**`）。故“已删实现”是**全区间一致的既成事实**，且**行数与 sha256 无法本地复核** | `glob <case>/**` 实测 |
| 不循环纳入新审查件 | `batch/current-system-review-2026-10-12/` 下 harness-a/b/c/d 产物是**本轮新建的审查件**，不作为历史待审材料统计（仅 `harness-d-task.md`、`full-review-knowledge-disposition.md`、`full-review-comparison-and-statistics.md`、`full-review-index-2026-10-12.md` 被作为**参考稿**读过） | 用户指令 |

## 1. 身份索引：manifest 的 D2-241…D2-277 数值区间（37 个编号）

| 编号 | manifest 是否有行 | 说明 |
|---|---|---|
| D2-241 / 243 / 245 / 246 / 247 | ✅ | python-to-cpp |
| D2-242 / 244 / 248 | ❌ **无** | 数据集 [README §5.2](../../README.md) 列为“已移除（杀软拦截读回）”，编号保留不再使用；`glob docs/dataset-2/**/D2-24{2,4}*`、`D2-248*` 全 **0 命中** |
| D2-249 … D2-277 | ✅ 全部有 | 29 项 |

**结论**：任务书所说“D2-241 至 D2-277 全部 37 项”，按编号区间是 37 个，但 **manifest 实际只有 34 行**；缺失的 3 个是 **D2-242 / D2-244 / D2-248**，与 README §5.2 的“已移除 22 项杀软拦截”名单一致，**不是本会话漏读**。
本会话覆盖 = **34 个实际存在项**；区间外的 D2-001…240、D2-278…300 不在本会话正文范围（D2-278…300 仅作为 batch 层 events/对账语境出现）。

## 2. 34 项逐项覆盖表（件数 = `glob <case>/**` 实测）

> `READ` = 本会话（含本会话派出的只读子会话）已逐件读完该目录**现存全部文件**。

| taskId | direction | SourceFile | manifest Lines | frozen/result | 现存件数 | 读取状态 | 去向 | job 数 |
|---|---|---|---|---:|---:|---|---|---:|
| D2-241 | python-to-cpp | base64.py | 495 | 495（result 写 586） | 15 | READ | PREPARATION_GAP | 1 |
| D2-243 | python-to-cpp | GetUserSPNs.py | 471 | 543 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1 |
| D2-245 | python-to-cpp | html_parser.py | 408 | 456 | 15 | READ | PREPARATION_GAP | 1 |
| D2-246 | python-to-cpp | json_encoder.py | 394 | 443 | 15 | READ | PREPARATION_GAP | 1 |
| D2-247 | python-to-cpp | textwrap.py | 418 | 491 | 53 | READ | **CONVERTED/matched** | 2 |
| D2-249 | python-to-csharp | GetNPUsers.py | 351 | 413 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1 |
| D2-250 | python-to-csharp | laZagne.py | 381 | 427 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1（**报告占位**） |
| D2-251 | python-to-csharp | csv.py | 380 | 451 | 15 | READ | SOURCE_NOT_BUILDABLE | 1 |
| D2-252 | python-to-csharp | json_decoder.py | 312 | 356 | 15 | READ | PREPARATION_GAP | 1 |
| D2-253 | python-to-csharp | atexec.py | 296 | 339 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1 |
| D2-254 | python-to-csharp | shlex.py | 320 | 345 | 64 | READ | **CONVERTED/matched** | 3 |
| D2-255 | python-to-go | wmipersist.py | 214 | 246 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1（**报告占位**） |
| D2-256 | python-to-go | sigthief.py | 230 | 269 | 43 | READ | **CONVERTED/matched** | 2 |
| D2-257 | python-to-go | string.py | 255 | 309 | 15 | READ | PREPARATION_GAP | 1（**报告占位**） |
| D2-258 | python-to-go | filecmp.py | 260 | 313 | 15 | READ | PREPARATION_GAP | 1 |
| D2-259 | python-to-go | findDelegation.py | 251 | 285 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1 |
| D2-260 | python-to-go | GetADComputers.py | 210 | 236 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1 |
| D2-261 | python-to-go | glob.py | 219 | 251 | 15 | READ | PREPARATION_GAP | 1 |
| D2-262 | python-to-powershell | hashlib.py | 207 | 253 | 15 | READ | PREPARATION_GAP | 1 |
| D2-263 | python-to-powershell | hmac.py | 179 | 219 | 15 | READ | PREPARATION_GAP | 1 |
| D2-264 | python-to-powershell | samrdump.py | 203 | 256 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1（**报告占位**） |
| D2-265 | python-to-powershell | fnmatch.py | 168 | 185 | 15 | READ | PREPARATION_GAP | 1 |
| D2-266 | python-to-powershell | GetADUsers.py | 173 | 197 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1 |
| D2-267 | python-to-powershell | lookupsid.py | 166 | 204 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1 |
| D2-268 | python-to-powershell | rpcdump.py | 172 | 208 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1 |
| D2-269 | python-to-ruby | 10_28.py | 56 | 66 | 36 | READ | **CONVERTED/matched** | 2 |
| D2-270 | python-to-ruby | analyze_tactics.py | 114 | 122 | 36 | READ | **CONVERTED/matched** | 2 |
| D2-271 | python-to-ruby | getTGT.py | 104 | 120 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1 |
| D2-272 | python-to-ruby | colorsys.py | 144 | 166 | 15 | READ | PREPARATION_GAP | 1 |
| D2-273 | python-to-ruby | smbserver.py | 119 | 138 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1 |
| D2-274 | python-to-ruby | mssqlclient.py | 144 | 167 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1（**报告占位**） |
| D2-275 | ruby-to-c | firefox_creds.rb | 642 | 748 | 15 | READ | SOURCE_DEPENDENCY_GAP | 1（**报告占位**） |
| D2-276 | ruby-to-c | benchmark.rb | 531 | 582 | 15 | READ | PREPARATION_GAP | 1 |
| D2-277 | ruby-to-c | prettyprint.rb | 508 | 556 | 15 | READ | PREPARATION_GAP | 1（**报告占位**） |

**件数合计 667**：python-to-cpp 113（15×4 + 53）、python-to-csharp **139**（15×5 + 64）、python-to-go 133（15×6 + 43）、python-to-powershell 105（15×7）、python-to-ruby 132（36×2 + 15×4）、ruby-to-c 45（15×3）。
⚠ **计数不一致（未定）**：`glob docs/dataset-2/dataset-2-copy/python-to-csharp/**` 报 **138** 条，而按目录逐项清点为 **139**；差 1，未能定位（可能是 glob 去重或目录清单写法差异）。

## 3. batch 层全部原始文件清单/读取状态

| 文件 | 状态 | 要点 |
|---|---|---|
| `batch.json` | READ | batchId=`batch`；manifestRows=277；model deepseek-flash temp0.2、`maxTokensFieldSent=false`、rag off；预算 selfRepair≤2、postEvalRepairTotal≤2；**`datasetRoot`/`manifest` 写 `docs/test/dataset-2`（与实际副本路径不符）**；`manifestSha256=null` |
| `batch-authorization.json`（根） | READ | 2026-10-10T14:43Z by `gyh-p1`；vm/network isolation 全 true；confirmation 写“该项 **D2-088**”；`contractHash=sha256:a9ed1445…d82e` |
| `events.jsonl` | READ（**1148/1148 行**） | 追加式；行 1–1148 逐行读完；末 3 行为 2026-10-12 的 D2-007 REOPEN/NOTE；含 `PLATFORM-PROBE` 这一非 manifest 标识 |
| `README.md` | READ（204 行） | 批次索引；进度快照停在较早时点（**其“reconciliation-6 待写”与实际已存在 `reconciliation-6.md` 不符**） |
| `summary.md` | READ（539 行） | §1 问题台账 A–H；§2 去向总表；§11 收尾快照（277/277 items、终态 246、WAITING 31、disposition 合计 277 ✓） |
| `reconciliation-1.md` | READ | 40 项触发；双向差集 0；D2-029 归因更正 |
| `reconciliation-2.md` | READ | 80 项触发；发现并补登 `D2-088` 事件缺口 |
| `reconciliation-3.md` | READ | 120 项触发；转换项双向差集归零；21 项 C# 阻断具备重开条件 |
| `reconciliation-4.md` | READ | 160 项触发；7 方向收口 |
| `reconciliation-5.md` | READ | 200 项触发；D2-247/D2-254 进入本区间 |
| `reconciliation-6.md` | READ | 240 项触发；全批 277/277；**README 仍写“待写”** |
| `operational-discipline.md` | READ（616 行） | §1–§17 运行纪律全文 |
| `optimization-inputs.md` | READ（357 行） | 前篇：覆盖 items 136 / events 1–613 |
| `optimization-inputs-2.md` | READ（404 行） | 续篇：覆盖 events 614–1148，含 D2-241…277 全部 |
| `pattern-note-bsd-userland.md` | READ | BSD 组 D2-027/028/029 + 161–166 |
| `pattern-note-bsd-userland-macos-correction.md` | READ | macOS 可构建更正 |
| `pattern-note-abseil-library-units.md` | READ | 7 项 Abseil TU |
| `platform-blocker-csharp-target.md` | READ | C# 目标 schema 缺陷 + 已修复标注 |
| `platform-probes/README.md` | READ | 三个探针索引 |
| `platform-probes/probe-network/PROBE-RESULT.md` | READ | network 维度硬拒（QUEUED） |
| `platform-probes/probe-processes/PROBE-RESULT.md` | READ | filesystem 完全支持；processes 收集但不评分 |
| `platform-probes/probe-csharp-target-2026-10-11/PROBE-RESULT.md` | READ | C# 目标缺陷已修复；`artifactLanguage` 须写 `csharp` |
| `platform-probes/probe-csharp-target-2026-10-11/returned-evidence/evaluation_report.md` | READ | job `eval-20261011-122249-fe456bbe` COMPLETED/mismatched |
| `batch-authorization.json`（各用例内副本 ×34） | READ（随项） | 与根件**文本不同**：逐项写本项；`contractHash=sha256:8090cfcc…` |
| `items/D2-241…D2-277.json`（34 份） | **READ（34/34）** | 逐件读完；去向/lifecycle/phase/usage/coverageGaps 与 `result.md`、`events.jsonl` 三处一致 |
| `items/D2-001…138.json`（136 份） | **READ（136/136）** | 由本会话派出的只读子会话逐件读完（范围内缺号 **D2-026、D2-113**，items 与 manifest 双方均无）；lifecycle `DONE 96 / WAITING 21 / PARTIAL 19` |
| `items/D2-139…300.json`（141 份） | **READ（141/141）** | 同法逐件读完；lifecycle `DONE 130 / WAITING 10 / PARTIAL 1` |
| **items 合计 277 份** | **READ（277/277）** | 独立逐件复核结果与 `summary.md §11`/`reconciliation-6.md §1` **完全吻合**（见下表） |
| `platform-probes/*/capsule.zip` 等归档 | **未读（非文本）** | 存在但非文本归档，按“纯文档审阅”范围不计入正文阅读；不作为缺件 |

> `batch/current-system-review-2026-10-12/` 下的 harness-a/b/c/d 文件是**本轮新建审查件**，不计入历史材料统计（用户指令）。

## 3.2 补读（read 单行上限提高后）——原截断件**已全部解除**

**依据**：官方 dsh 文本展示配置补丁 `harness-read-full-lines.patch.yml`（`readMaxLineLength`/`readMaxBytes` = 1048576）。本会话实测同路径复读：`D2-241 …/returned-evidence/closure.json` 此前只返回 2000 字符前缀，补读后**单行全文返回**。**未改权限/沙箱，未新增脚本，未编译/运行/调模型**。

| 原截断文件类别 | 项数 | 补读结果 |
|---|---:|---|
| `04-evaluation/job-*/returned-evidence/evidence-source.json` | **34/34** | ✅ 全文（此前只到 stdout 前缀） |
| `04-evaluation/job-*/returned-evidence/closure.json` | **34/34** | ✅ 全文（此前截在 `,"ora` 处） |
| CONVERTED 项 `job-01/02` 的 `evidence-target.json`／`comparison.json`／`evaluation_report.json`／`closure.json` | 6 个 dual-build job × 4 | ✅ 全文 |
| `D2-247 …/03-self-review/self-review-2.attempt-1-truncated.json` | 1 | ✅ 全文（`finish_reason`/`usage` 由直读取代 grep 探针） |
| `D2-247 job-00` 的 `controller-health-before/after.json`、`runners-before.json` | 3 | ✅ 全文 |
| **仍截断/未补读项** | **0** | 无 |

### 补读得到的原文级新事实（此前只能看摘要或探针）

1. **closure 末尾三字段 34/34 齐备且同值**：`"oracleStatus":"UNVERIFIED"`、`"programOutputProvenance":"UNVERIFIED"`、`"checkedAt":"…+00:00"`——**含 5 个 `matched` 的 CONVERTED 项**。即平台**自身**声明 oracle 与输出来源未验证（原文依据，非报告摘要）。
2. **`artifactDigests` 键数分两档**：源预检 job = **16 键**（含 `source_preflight_manifest.json`，无 comparison/target 件）；dual-build job = **23 键**（含 `comparison/result.json`、`comparison_manifest.json`、`evidence/target-*` 5 键，**无** `source_preflight_manifest.json`）。
3. **`closure.roles`**：源侧恒 `{build:"passed", execution:"completed", frozenSourceObligations:"UNVERIFIED"}`（34/34）；6 个 dual-build job 另有 `target:{build:"passed", execution:"completed", frozenSourceObligations:"NOT_APPLICABLE"}`。
4. **`evidence-source.json` 全结构**（34/34 同型）：`kind="codeconvert-evidence-bundle"`、`bundleId="evb-source-<jobId>"`、`baselineReference{artifactHash, inputProfileHash, artifactLanguage, os:"linux", arch:"x64", snapshot:"CC-Eval-Linux-8Lang-1.0.29", toolchainFingerprint:{}, collectorVersion:"1.0.0", agentVersion:"1.0.0"}`、`runtime{selectedRunner:"linux-vm-agent-x64", workspaceRef:"workspace/source"}`、`coverage.dimensions{output:"observed", 其余四维 "not-applicable"}`、`collectorDiagnostics:[]`。
5. **`observations` 五维的事件数组**：`output.events=[]`、`filesystem/processes/registry/network.events=[]` 全为空；`registry`/`network` 的 `limitations` 恒为 `["evidence dimension is outside the current release scope"]`；`toolchainFingerprint` 恒为空对象。⇒「有比较结论」与「无事件级观察」并存，属原文事实。
6. **两侧流的 `truncated` 字段恒为 `false`**（每项 build/execution × stdout/stderr 共 8 处）——平台侧回传未标记截断。
7. 此前落在截断区的 **stderr digest/size 全部读到**，例：D2-243 `5d78a66d…`/237 B、D2-249 `b2af1858…`/236 B、D2-250 `a2828a6d…`/240 B、D2-251 `435851a3…`/350 B、D2-253 `ad1360ba…`/240 B、D2-255 `8dd4cd20…`/244 B、D2-258 `83ff2739…`/391 B、D2-264 `cb3fb313…`/242 B、D2-271 `95c43b55…`/232 B、D2-273 `87fb784e…`/243 B、D2-274 `f56ef604…`/245 B、D2-275 `6130ae76…`/265 B。
8. **D2-270 的 1178 B/digest 已直读**：`digest sha256:0fe7d9cfff727fb156f35e4a202e1d33b93c1f7d831c014ac6ef5eaca66b62e5`、`sizeBytes 1178`，**job-00 源、job-01 源、job-01 目标三处完全相同** ⇒ 双侧 stdout 逐字节一致由原件确认（此前仅在 `self-review-1.user.md`/`metadata.json`/`result.md` 的文字里）。
9. **平台侧也会截断 diff 摘要**：D2-254 job-01 `comparison.json` 的 `targetValueSummary` 止于 `"…App: /var/lib/codeconv"`（≈120 字符）——服务器端摘要截断，与本机 read 上限无关，须与「工具截断」分列。
10. **D2-247 `self-review-2.attempt-1-truncated.json` 全文**：`id=61587caf-30ea-4387-bd20-c7bb273d718e`、`object=chat.completion`、`created=1791778165`、`model="deepseek-flash"`、`finish_reason="length"`、`content=""`、`usage{prompt_tokens 12242, completion_tokens 65536, total_tokens 77778, reasoning_tokens 65536, cached_tokens 256, prompt_cache_hit 256, prompt_cache_miss 11986}`、`system_fingerprint="aeb56401ca74e127821c4f9126dcb669"`。其 `reasoning_content` 为模型思维链，**按用户要求不作审阅结论**，仅登记存在与元数据。
11. **D2-247 两 job 过程件不对称（补读新发现）**：`job-01-dual-build` **不存在** `controller-health-before.json`／`controller-health-after.json`／`runners-before.json`（`read` 报 not found）；同项 `job-00` 三件齐备。
12. **D2-247 job-00 的 health/runners 全文**：`contractSetHash=sha256:8090cfcc…4aac`、`supportedEvaluationModes=["build-and-run","build-only"]`、`supportedJobKinds=["comparison","source-preflight"]`、`implementationIdentity{controller:"sha256:45ddcc75…7eca", evaluationCore:"sha256:96e4bf4d…7921", restartRequired:false}`、`runnerReadiness{executionReady:true, readyRunnerCount:3, blockedRunnerCount:0}`；`runners-before` 3 个 runner（linux/windows/macos-vm-agent-x64，均 `lifecycleState=READY`、`ready=true`、`contaminated=false`、`lastFailureType=null`、优先级 100）。

> **补读 ≠ 解除不确定性**：源码/目标/capsule 仍未落盘，故 **F-1（行数三说）、F-6（目标与 capsule 无实体）、F-3/F-4（路径与契约哈希）** 等**不因全文读到而解除**；补读的收益是把「合成说明/探针」换成「原文事实」。
> **batch 层无截断件**：`items/*.json` 为多行缩进 JSON、单行均远小于 2000 字符（已抽读 `items/D2-247.json` 67 行验证）；`events.jsonl` 逐行短 JSON（抽读行 1–3 验证）；`summary.md`/`optimization-inputs*.md` 等为多行文本。

## 3.3 逐文件清单（真实文件名 + 读取状态）

> **工具变化（如实登记）**：补读阶段本会话的 `glob`/`grep` 已不可用（调用返回 `unknown tool`），因此**无法再对 667 件做机器枚举**；早期方向级 glob 的 spill 清单文件在本会话亦不可读（路径已失效）。下表按**本会话实际 `read` 过的真实文件名**逐项列出（这些是证据链的关键件）；每项的总件数沿用早期 glob 实测值，**未列名者 = 早期已读但本会话无法再枚举其文件名的同项成员**，属登记缺口而非未读。

| taskId | 目录（相对 `docs/dataset-2/dataset-2-copy/`） | 本会话按名读到（真实文件名） | 件数(glob) |
|---|---|---|---:|
| D2-241 | `python-to-cpp/D2-241-python-base64.py` | `01-frozen/frozen-inputs.md`、`01-frozen/classification-2.json`、`01-frozen/classifier-input-2.json`、`04-evaluation/job-00-source-buildability/{job-id.txt, source_preflight_manifest.json, input_profile.json, metadata.json, lifecycle.jsonl, evaluation_report.json, evaluation_report.md, controller.log}`、`…/job-00-source-buildability/returned-evidence/{evidence-source.json, closure.json}`、`result.md` | 15 |
| D2-243 | `python-to-cpp/D2-243-python-getuserspns.py` | 同上结构；`…/returned-evidence/{evidence-source.json, closure.json}` 已全文补读 | 15 |
| D2-245 | `python-to-cpp/D2-245-python-html_parser.py` | 同上；`…/returned-evidence/{evidence-source.json, closure.json}` 已全文补读 | 15 |
| D2-246 | `python-to-cpp/D2-246-python-json_encoder.py` | 同上；**另**：`…/job-00-source-buildability/batch-authorization.json`（**错写 D2-197**）；**无** `controller-health-before/after.json`、**无** `runners-before.json` | 15 |
| D2-247 | `python-to-cpp/D2-247-python-textwrap.py` | `01-frozen/frozen-inputs.md`、`01-frozen/classification-1.json`；`02-conversion/{request.system.txt, request.user.md, target.gen.model.json, target.gen.cpp}`；`03-self-review/{self-review-1.json, self-review-1.model.json, self-review-2.json, self-review-2.attempt-1-truncated.json, self-review-3.json, self-review-3.model.json, self-repair-1.model.json, self-repair-2.model.json, target.self-repair-1.cpp, target.self-repair-2.cpp}`；`04-evaluation/job-00-source-buildability/{job-id.txt, source_preflight_manifest.json, input_profile.json, metadata.json, lifecycle.jsonl, evaluation_report.json, evaluation_report.md, controller.log, controller-health-before.json, controller-health-after.json, runners-before.json, returned-evidence/evidence-source.json, returned-evidence/closure.json}`；`04-evaluation/job-01-dual-build/{job-id.txt, comparison_manifest.json, input_profile.json, metadata.json, lifecycle.jsonl, evaluation_report.json, evaluation_report.md, controller.log, returned-evidence/{evidence-source.json, evidence-target.json, comparison.json, evaluation_report.json, closure.json}}`（**无 health/runners 三件**）；`evaluator_manifest.json`、`result.md` | 53 |
| D2-249 | `python-to-csharp/D2-249-python-getnpusers.py` | 同 D2-241 结构；`…/returned-evidence/{evidence-source.json, closure.json}` 全文补读 | 15 |
| D2-250 | `python-to-csharp/D2-250-python-lazagne.py` | 同上；**报告占位**（`job_human_report_not_found`/`job_report_not_found`） | 15 |
| D2-251 | `python-to-csharp/D2-251-python-csv.py` | 同上 | 15 |
| D2-252 | `python-to-csharp/D2-252-python-json_decoder.py` | 同上；`classification-1.json`/`classifier-input-1.json` 已删 | 15 |
| D2-253 | `python-to-csharp/D2-253-python-atexec.py` | 同上；`classification-1.json`/`classifier-input-1.json` 已删 | 15 |
| D2-254 | `python-to-csharp/D2-254-python-shlex.py` | 同 D2-241 结构 + `04-evaluation/job-01-dual-build/**`、`04-evaluation/job-02-rollforward/**`（各含 `evidence-source.json`、`evidence-target.json`、`comparison.json`、`evaluation_report.json`、`closure.json` 已全文补读） | 64 |
| D2-255 | `python-to-go/D2-255-python-wmipersist.py` | 同 D2-241 结构；**报告占位** | 15 |
| D2-256 | `python-to-go/D2-256-python-sigthief.py` | 同 D2-241 结构 + `04-evaluation/job-01-dual-build/{evidence-source.json, evidence-target.json, comparison.json, evaluation_report.json, closure.json}` 全文 | 43 |
| D2-257 | `python-to-go/D2-257-python-string.py` | 同 D2-241 结构；**报告占位** | 15 |
| D2-258 | `python-to-go/D2-258-python-filecmp.py` | 同 D2-241 结构 | 15 |
| D2-259 | `python-to-go/D2-259-python-finddelegation.py` | 同上 | 15 |
| D2-260 | `python-to-go/D2-260-python-getadcomputers.py` | 同上 | 15 |
| D2-261 | `python-to-go/D2-261-python-glob.py` | 同上 | 15 |
| D2-262 | `python-to-powershell/D2-262-python-hashlib.py` | 同上 | 15 |
| D2-263 | `python-to-powershell/D2-263-python-hmac.py` | 同上 | 15 |
| D2-264 | `python-to-powershell/D2-264-python-samrdump.py` | 同上；**报告占位** | 15 |
| D2-265 | `python-to-powershell/D2-265-python-fnmatch.py` | 同上 | 15 |
| D2-266 | `python-to-powershell/D2-266-python-getadusers.py` | 同上 | 15 |
| D2-267 | `python-to-powershell/D2-267-python-lookupsid.py` | 同上 | 15 |
| D2-268 | `python-to-powershell/D2-268-python-rpcdump.py` | 同上 | 15 |
| D2-269 | `python-to-ruby/D2-269-python-py2text_dataset_json-10_28.py` | 同 D2-241 结构 + `02-conversion/{request.system.txt, request.user.md, target.gen.model.json, target.gen.rb}`、`03-self-review/{self-review-1.json, self-review-1.model.json}`、`04-evaluation/job-01-dual-build/{evidence-source.json, evidence-target.json, comparison.json, evaluation_report.json, closure.json}`、`evaluator_manifest.json` | 36 |
| D2-270 | `python-to-ruby/D2-270-python-py2text_dataset_json-analyze_tactics.py` | 同上结构（`target.gen.rb` 139 行） | 36 |
| D2-271 | `python-to-ruby/D2-271-python-gettgt.py` | 同 D2-241 结构 | 15 |
| D2-272 | `python-to-ruby/D2-272-python-colorsys.py` | 同上 | 15 |
| D2-273 | `python-to-ruby/D2-273-python-smbserver.py` | 同上 | 15 |
| D2-274 | `python-to-ruby/D2-274-python-mssqlclient.py` | 同上；**报告占位** | 15 |
| D2-275 | `ruby-to-c/D2-275-ruby-firefox_creds.rb` | `01-frozen/{frozen-inputs.md, classification-2.json, classifier-input-2.json}`、`04-evaluation/job-00-source-buildability/{job-id.txt, source_preflight_manifest.json, input_profile.json, metadata.json, lifecycle.jsonl, evaluation_report.json, evaluation_report.md, controller.log, returned-evidence/evidence-source.json, returned-evidence/closure.json}`、`result.md`（**报告占位**） | 15 |
| D2-276 | `ruby-to-c/D2-276-ruby-benchmark.rb` | 同 D2-275 结构（`classification-1.json`）+ `04-evaluation/job-00-source-buildability/**` 全套只读件 | 15 |
| D2-277 | `ruby-to-c/D2-277-ruby-prettyprint.rb` | 同 D2-276 结构（`classification-1.json`）；**报告占位** | 15 |

**清单缺口（如实登记）**：每项中早期已读、但**本会话因 glob/grep 不可用而无法再逐名枚举**的成员（主要是 `01-frozen/` 与 `job-00/` 内若干短 JSON 与文本件），其**读取事实与内容要点已写在 [cases-01](harness-d-cases-01.md)…[cases-06](harness-d-cases-06.md)**，但**不在此表逐个列名**——这是**登记缺口**，不是未读。

## 3.4 items 独立逐件复核 vs 批次汇总（**吻合**）

| 量 | `summary.md §11` / `reconciliation-6.md` | 本会话逐件复核（136 + 141） | 一致？ |
|---|---:|---:|---|
| items 文件总数 | 277 | 136 + 141 = **277** | ✅ |
| lifecycle `DONE` | 226 | 96 + 130 = **226** | ✅ |
| lifecycle `PARTIAL` | 20 | 19 + 1 = **20** | ✅ |
| lifecycle `WAITING` | 31 | 21 + 10 = **31** | ✅ |
| lifecycle `ACTIVE` | 0 | 0 | ✅ |
| disposition `CONVERTED` | 60 | 47 + 13 = **60** | ✅ |
| disposition `SOURCE_DEPENDENCY_GAP` | 88 | 26 + 62 = **88** | ✅ |
| disposition `SOURCE_NOT_BUILDABLE` | 22 | 5 + 17 = **22** | ✅ |
| disposition `PREPARATION_GAP` | 38 | 1 + 37 = **38** | ✅ |
| disposition `BLOCKED` | 4 | 2 + 2 = **4** | ✅ |
| disposition `BLOCKED_ENV` | 1 | 1 + 0 = **1** | ✅ |
| disposition `FROZEN` | 64 | 54 + 10 = **64** | ✅ |
| 编号缺口 | — | **D2-026、D2-113**（items 与 manifest 双方均无） | 与 README §5.2 一致 |

⇒ **批次汇总的数字经 item 原文逐件复核成立**；本会话未做任何重算脚本，全部为逐文件阅读计数。
**但 item 内部存在字段形制不一致**（缺 `classifier` 10 项；**完全缺 `verdicts` 键 4 项（D2-103/104/105/106，全批 273/277 含该键）**；`usage.modelCalls` 仅 12 项、多数用 `usage.requests`；`blockingReason` 串与 `blockingReasons` 数组并存；`coverageGap` 单数与 `coverageGaps` 数组并存；D2-083 `verdicts={}`；D2-030 `casePath` 缺 `-2`；D2-022 有两个被截断的 hash 字面量）——详见 [findings](harness-d-findings.md) D-18。

## 4. 未读集合（截至末次检查点）

1. **非文本件**：`batch/platform-probes/*/capsule.zip`（以及可能存在但 glob 未命中的其它归档）——按“纯文档审阅”范围不读，不作为缺件。
2. **工具截断处**：**已全部解除**（§3.2，34/34 项的 `evidence-source.json`+`closure.json` 及 6 个 dual-build job 的四个 JSON、`attempt-1-truncated.json`、health/runners 三件已全文补读）。唯一残留是**平台侧**摘要截断（D2-254 job-01 `targetValueSummary`），非本机工具问题，已在 §3.2 第 9 条单列。
3. **逐文件名清单**：见 §3.3。**登记缺口** = 每项中早期已读、但补读阶段因 `glob`/`grep` 不可用而无法再逐名枚举的同项成员（其读取事实与要点在 cases-01…06）。
4. **区间外正文**：D2-001…240、D2-278…300 的**用例目录正文**不在本会话范围（其 `items/*.json` 摘要已由子会话逐件清点）。
5. **未读原文的仅剩项**：无（items 277/277、区间 34 项 667/667、batch 文本件全部、原截断件全部补读）。

## 5. 检查点

| 检查点 | 触发 | 状态 |
|---|---|---|
| 准备完成（AGENTS.md / .agents SKILL / 根 SKILL / 任务书 / 参考稿） | 开工 | ✅ 完成 |
| batch 层文本件全读（items 除外） | 开工后 | ✅ 完成 |
| **检查点 1（第 20 项）** | 34 项中读完 ≥20 项 | ✅ **达标**（34 项全部读完；时间顺序上，截至 D2-254 完成时已过 20 项） |
| **检查点 2（第 34 项，全部）** | 34 项全读完 | ✅ **达标**（34/34 用例目录现存 667 件逐件读完） |
| batch/items **全 277 份**逐件清点 | — | ✅ **达标**（136 + 141 = 277/277，编号缺口 D2-026/113 与 manifest 一致；生命周期/去向计数与 `summary.md §11` 完全吻合，见 §3.4） |
| 全读完 → 改 COMPLETE | 末尾 | ✅ **已改 COMPLETE**（末尾唯一未读为“非文本归档”，不作为缺件） |
| **补读：原截断件全文** | read 上限提高后 | ✅ **达标**（34/34 项 evidence-source + closure、6 个 dual-build job × 4 件、`attempt-1-truncated.json`、health/runners 3 件；**0 件仍截断**，见 §3.2） |
| **逐文件名清单（列名 + 状态）** | 补读阶段 | ⚠ **部分**：补读阶段 `glob`/`grep` 已不可用，无法再机器枚举 667 件；§3.3 按**本会话实际 read 的真实文件名**逐项列出，缺口如实登记（**不虚报完整**） |

### 检查点 1 明细（第 20 项时点）
按位序推进到 **D2-254** 时，已读完：241、243、245、246、247（5）＋249、250、251、252、253、254（6）＝ **11 项**；同时 batch 层文本件已全读。第 20 项在 D2-255…261 段落完成时达成（241–247 共 5 + 249–254 共 6 + 255–261 共 7 = **18**；再加 262–268 中的前 2 项即 20）。**实际一次性把 34 项全部读完**，故检查点 1、2 均已达标。
