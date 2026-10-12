# Harness D — 发现与分层结论

> 范围：`manifest.csv` 的 **D2-241…D2-277** 区间（37 编号中实际存在 **34 项**）+ `dataset-2-copy` 根 README/manifest + `batch/` 层全部文本原件。
> 方法：只读、逐件、手工（read/glob/grep）；**未写脚本、未运行哈希/统计工具、未编译运行、未调用模型、未提交评估、未改任何原证据**。
> **本文严格分开**：① 原始事实（可核）② 历史说明（文件自述，未必可核）③ 当前规则（仓库现行契约）④ 未知/不可核。
> 参考稿：[full-review-knowledge-disposition.md](full-review-knowledge-disposition.md)、[full-review-comparison-and-statistics.md](full-review-comparison-and-statistics.md)（只读参考，未当作运行授权）。

---

## 0. 区间总账（原始事实）

- **34 项**逐项去向（来自 `items/*.json` + `result.md` + `events.jsonl`，三处一致）：

| 去向 | 数量 | taskId |
|---|---:|---|
| `CONVERTED` | **5** | D2-247、254、256、269、270 |
| `SOURCE_DEPENDENCY_GAP` | **15** | D2-243、249、250、253、255、259、260、264、266、267、268、271、273、274、275 |
| `SOURCE_NOT_BUILDABLE` | **1** | D2-251 |
| `PREPARATION_GAP` | **13** | D2-241、245、246、252、257、258、261、262、263、265、272、276、277 |

- **lifecycle**：34/34 均为 `DONE`（无 `ACTIVE`/`WAITING`/`PARTIAL`）。
- **模型调用**：进入生成的仅 5 项；其余 **29 项 0 模型调用**。5 项成功调用总计 **6+6+4+2+2 = 20 次**（247 六次、254 六次、256 四次、269/270 各两次）。
- **失败 attempt**：2 次，均在 D2-247（① 生成 attempt-1 被会话重置杀死、**无响应留存**；② `self-review-2` attempt-1 `finish_reason=length`、reasoning 65536、content 空，**已保留** `self-review-2.attempt-1-truncated.json`）。
- **job 数**：区间内共 **42 个 job 目录**（247 有 2、254 有 3、256 有 2、269/270 各 2，其余 29 项各 1）。
- **编号缺口**：D2-242 / D2-244 / D2-248 在磁盘与 manifest **均不存在**（`glob docs/dataset-2/**/D2-24{2,4}*`、`D2-248*` 全 0 命中），与数据集 [README §5.2](../../README.md)“已移除 22 项杀软拦截读回”名单一致 ⇒ 任务书所称“37 项”中的 3 项**不是漏读**。

---

## 1. 原始事实（可核，逐条带依据）

### F-1｜`manifest.csv` 的 `Lines` 列与冻结/结果记录**大面积不一致**（33/34）

| taskId | manifest `Lines` | frozen/result 行数 | 差 |
|---|---:|---:|---:|
| D2-241 | 495 | 495（**但 `result.md` 写 586**） | 0 / +91 |
| D2-243 | 471 | 543 | +72 |
| D2-245 | 408 | 456 | +48 |
| D2-246 | 394 | 443 | +49 |
| D2-247 | 418 | 491 | +73 |
| D2-249 | 351 | 413 | +62 |
| D2-250 | 381 | 427 | +46 |
| D2-251 | 380 | 451 | +71 |
| D2-252 | 312 | 356 | +44 |
| D2-253 | 296 | 339 | +43 |
| D2-254 | 320 | 345 | +25 |
| D2-255 | 214 | 246 | +32 |
| D2-256 | 230 | 269 | +39 |
| D2-257 | 255 | 309 | +54 |
| D2-258 | 260 | 313 | +53 |
| D2-259 | 251 | 285 | +34 |
| D2-260 | 210 | 236 | +26 |
| D2-261 | 219 | 251 | +32 |
| D2-262 | 207 | 253 | +46 |
| D2-263 | 179 | 219 | +40 |
| D2-264 | 203 | 256 | +53 |
| D2-265 | 168 | 185 | +17 |
| D2-266 | 173 | 197 | +24 |
| D2-267 | 166 | 204 | +38 |
| D2-268 | 172 | 208 | +36 |
| D2-269 | 56 | 66 | +10 |
| D2-270 | 114 | 122 | +8 |
| D2-271 | 104 | 120 | +16 |
| D2-272 | 144 | 166 | +22 |
| D2-273 | 119 | 138 | +19 |
| D2-274 | 144 | 167 | +23 |
| D2-275 | 642 | 748 | +106 |
| D2-276 | 531 | 582 | +51 |
| D2-277 | 508 | 556 | +48 |

- 多份 `frozen-inputs.md` **自称** “manifest `Lines` 列为旧口径 / 实测一致”（如 D2-251/254/256/258/259/260/261/275 等），但**没有任何文件说明该列是否/何时回填**。
- **源文件在工作区已不存在**（`source/` 全区间 0 命中）⇒ **哪一侧为真不可判定**（未知，见 §5）。

### F-2｜`JobId=""`、`Evidence="UNVERIFIED (not built, not run)"` 属**设计**，不是缺件

[README §3](../../README.md) 明定：`JobId`＝“REUSE 项的继承证据 job；**NEW 项为空**”；`Evidence`＝“dual-build-PASS (inherited) 或 **UNVERIFIED (not built, not run)**”。区间 34 项全为 `NEW` ⇒ 空/UNVERIFIED 是**清单对“数据集建库时状态”的描述**。
**但**：`manifest.csv` **不是批次台账**，批次侧的真实 jobId/证据状态只落在 `items/*.json`、`result.md`、`events.jsonl`、各 job 目录 ⇒ **全批没有一处“清单+条目+结果”三方一致的权威台账**（结构性事实，非缺件）。

### F-3｜路径口径三处并存且互不相符

- `frozen-inputs.md` 与 `items/*.json` 的 `casePath`：`docs/test/dataset-2/...` ⇒ `glob docs/test/**` **0 命中**。
- 实际磁盘：`docs/dataset-2/dataset-2-copy/...`。
- `manifest.csv` 的 `Origin`：`数据集python\...`；`batch.json` 的 `datasetRoot/manifest` 亦写 `docs/test/dataset-2`。
⇒ 三套路径写法并存；**任一时刻只有第二套可解析**。

### F-4｜根 `batch-authorization.json` 与各用例副本 `contractHash` 不同

- 根件：`contractHash=sha256:a9ed1445…d82e`，`confirmation` 写“该项 **D2-088**”。
- 34 个用例内副本：`contractHash=sha256:8090cfcc…4aac`，`confirmation` 逐项写本项。
⇒ **同一批次存在两个“合同哈希”**；副本是按项重写的。

### F-5｜**7 项**的 `evaluation_report.{md,json}` 为占位符，且同 job 的 `controller.log` 缺 `finished`

| 项 | 占位报告 | `controller.log` |
|---|---|---|
| D2-250（python-to-csharp） | `job_human_report_not_found` / `job_report_not_found` | 只有 `created 04:29:40Z` |
| D2-255（python-to-go） | 同上 | 只有 `created 04:48:00Z` |
| D2-257（python-to-go） | 同上 | 只有 `created 05:05:21Z` |
| D2-264（python-to-powershell） | 同上 | 只有 `created 05:14:44Z` |
| D2-274（python-to-ruby） | 同上 | 只有 `created 05:36:38Z` |
| D2-275（ruby-to-c） | 同上 | 只有 `created 05:38:27Z` |
| D2-277（ruby-to-c） | 同上 | 只有 `created 05:41:13Z` |

- 这 7 个 job 的 `closure.json` **仍记** `complete=true`、`cleanupConfirmed=true`、`issues=[]`、`attempts=1`，且 `closure.artifactDigests` 里**仍列出该报告件的正常 sha256**；对应 `result.md` 亦记“交付完整性：完成”。⇒ **“报告未取回 + 无完成时间戳”与“closure 已闭合 / 交付完整”并存**。
- 全数据集 grep 实测：`job_human_report_not_found` **16 次**、`job_report_not_found` **17 次**（区间内 7 项，其余在其它会话范围）。⇒ **非本项独有，是批次级/平台级现象**。

### F-6｜声明的交付物与实体不一致（区间 5 个转换项全部）

- 5 项的 `result.md` 与 `evaluator_manifest.json` 都声明根级目标（`target.cpp`/`target.cs`/`target.go`/`target.rb`）与 `replayArtifactPath=…/capsule.zip`、`hasReplayArtifact=true`、`success=true`；**全区间 `**/*.zip`、`**/capsule*` 0 命中**，`.cpp/.cs/.go/.rb` 0 命中。
- 同一交付物**路径口径不一**：`evaluator_manifest.json`（`target.go`/`target.cpp`，`targetDir="."`）vs `job-01/metadata.json`（`target/target.go`、`target/target.cpp`、`target/target.rb`）vs `result.md`（“根级 …”）。
- `evaluator_manifest.json` 的 `batchReportPath="../../../README.md"` 以 `targetDir="."` 解析为 `<direction>/README.md`，**不存在**（实际批次报告在 `batch/README.md`）。
- `result.md` 声称交付含 “capsule”（如 D2-255/257/258/261 的 §2），目录内**无任何 capsule 文件**。

### F-7｜`*.model.json` 引用的请求/响应主体文件全区间缺失

- 被引用但不存在的件：`request.body.json`、`target.gen.raw.json`、`target.gen.<ext>`、`target.self-repair-N.<ext>`、`self-repair-N.body/raw.json`、`self-review-N.body/raw.json`。
- 所有转换项的 `request.user.md` / `self-review-*.user.md` / `self-repair-*.user.md` 里，源/目标正文位置是 **`@SOURCE@` / `@TARGET@` 占位符（未替换）** ⇒ **实际送入模型的源/目标全文与知识正文无法复核**。
- 批次 README 的交付完整性审计**只登记**删除过 `submission-response.json`/`submission-2.json`/`job-state-final*.json`/`self-review-*.raw.json`；未提 `request.body.json`/`target.gen.raw.json` ⇒ 这些件的消失**是删除还是从未落盘，未定**（§5）。

### F-8｜`closure.json` 的 `artifactDigests` 指向 Controller 侧文件名，本地无法核对

- 反复出现的键名：`staging-manifest.json`、`lifecycle.jsonl`、`request.json`、`evidence/source-call.json`、`evidence/source-identity.json`、`evidence/source-request.json`、`evidence/source-response.json`、`evidence/source-response.body`、`evidence/target-response.body`、`classification.json`。
- 本地 `returned-evidence/` 用的是 `evidence-source.json`/`evidence-target.json`/`closure.json` 命名，`01-frozen/` 用 `classification-1.json`/`classification-2.json`。
⇒ **摘要值全部 UNVERIFIED**（不能核对，非缺件）。

### F-9｜closure 层自报 `oracleStatus` / `programOutputProvenance` = `UNVERIFIED`

- D2-246/247 的 `closure.json` grep 探针确认同时含 `"oracleStatus":"UNVERIFIED"` 与 `programOutputProvenance:"UNVERIFIED"`（字段名依 Controller 适配页）。
⇒ **连 `matched` 项的平台 closure 也把 oracle 与输出来源自报为 UNVERIFIED**；`matched` 只在“所配置的单一 output 维度”内成立。

### F-10｜`evaluator_manifest.json` 独缺与 metadata 链断裂（D2-246/247）

- **D2-247 缺 `03-self-review/self-review-2.model.json`**（同目录有 review-1/3 的 model.json）⇒ 该次成功调用的 `finish_reason`/usage/attempts 无本地记录（仅 `self-review-3.model.json` 的 `note` 交叉引用）。
- **D2-246 缺 `controller-health-before/after.json`、`runners-before.json`**（D2-247 job-00 齐备）。
- **D2-246 的 `batch-authorization.json` 内容错项**：`dataSource.confirmation` 写“该项 **D2-197 (Go stdlib sort.go)**”，与本项无关。

### F-11｜分类件层的“旧值留白”与“内部张力”

- **重分类项**（区间）：D2-241、246、252、253、256、275；均**删除了 `classification-1.json`**，且现存 `classification-2.json` 的 `old_cls`/`old_reason` **全为 null** ⇒ **首轮 BLOCKED 判定在产物内无留存**（只剩 `events.jsonl` 的 CLASSIFY 行与 `result.md`/`items`/README 的文字）。
- D2-252/253 连 `classifier-input-1.json` **也一并消失**，而 `events.jsonl` 只写“classification-1.json removed”。
- **内部张力**：`signals.network=[]` 但 `has_network=true`（D2-241、256）；`cls=REVIEW_SENSITIVE` 而 `signals.sensitive=[]`（D2-253、265）；`network_mode=wildcard`（0.0.0.0/::）或 `unresolved` 却 `requiresNetworkIsolation=false`（D2-273、274、259、260）；`batch-authorization.confirmation` 写“无网络”而分类判 `has_network=true`（D2-252、256）。
- **疑似词法漏检/误报**（源已删，不可定性）：D2-271 判 `LOW_SIGNAL`/signals 全空，而冻结自述为 Kerberos TGT 工具；D2-272 判 `process[3]` 而冻结称“仅数学常量与函数定义、无 import”；D2-265 判 `dynamic_code[10]`+`requiresSyntheticData=true` 而冻结称“纯标准库自包含”。

### F-12｜失败 attempt 的登记差集

- 已登记并保留：D2-247 `self-review-2.attempt-1-truncated.json`（`events.jsonl:958`、`README.md`、`optimization-inputs-2.md`、`items` 均记）。
- **只在 `items/D2-247.json` 的 `usage.note` 与 `02-conversion/target.gen.model.json` 的 `attempt_note` 记**：生成 attempt-1（后台 curl 被会话重置杀死、0 字节、**无响应留存**）。
  ⇒ `events.jsonl` / `README.md` / `summary.md` / `reconciliation-5`/`-6` / `optimization-inputs-2.md` **均只承认 1 个失败 attempt**，与 `items` 自称的 `failedAttempts=2` 构成**记载差集**。

### F-13｜`items/*.json` 全 277 份独立逐件复核：**批次汇总数字成立**，但 item 内部形制高度不一致

- **计数复核成立**（逐文件阅读计数，无脚本）：277 份 = 136（D2-001…138）+ 141（D2-139…300）；lifecycle `DONE 226 / PARTIAL 20 / WAITING 31 / ACTIVE 0`；disposition `CONVERTED 60 / SOURCE_DEPENDENCY_GAP 88 / SOURCE_NOT_BUILDABLE 22 / PREPARATION_GAP 38 / BLOCKED 4 / BLOCKED_ENV 1 / FROZEN 64` —— 与 [summary.md §11](../summary.md) 及 [reconciliation-6.md §1](../reconciliation-6.md) **逐项吻合**。编号缺口 **D2-026、D2-113** 在 items 与 manifest 双方均无。
- **形制不一致（原始事实）**：
  1. **缺 `classifier` 对象 10 项**：D2-008…012、030、065、076、077、078（从未分类）；D2-017/018/072/089/090/094/098/099/101 的 classifier 为 `NOT_TAKEN`。
  2. **`usage` 键不统一**：仅 D2-119…122、127、129、131、132、135…138 共 **12 项**用 `usage.modelCalls`；其余用 `usage.requests`（含 token 字段）。
  3. **`blockingReason`（串）与 `blockingReasons`（数组）并存**：D2-007、055、069、082、083、108；且数组元素类型有字符串 / `{code,detail}` 对象 / 空三种。
  4. **覆盖缺口字段三种写法**：`coverageGaps` 数组、`coverageGap` 单数字符串（D2-151、174、176、177、180、181、183）、仅写在 `verdicts.behaviorScope` 里（D2-001）。
  5. **`evaluation.verdict` 与 `behaviorVerdict` 两套**：仅 D2-194 用 `verdict`；D2-199/207/247/254/256/269/270 用 `behaviorVerdict`。
  6. **`classifier.version` 混用 2.3/2.4**：D2-161…166、174、177 为 **2.3**（sha `441b4d50…`），其余为 2.4（`009a6f31…`）。
  7. **`phase` 命名不一致**：多数预检失败用 `SOURCE_PRECHECK_FAILED`，但 D2-178 用 `CLOSED`、D2-251 用 `CLOSED_SOURCE_NOT_BUILDABLE`；D2-152/153/161…173 的 `phase=SOURCE_PRECHECK_FAILED` 而 `disposition` 分属两类。
  8. **`disposition=FROZEN` 的语义分裂**：18 项配 `WAITING`（D2-007…012、030、048…051、065、076…078、082、083、108）、10 项配 `PARTIAL`、**26 项配 `DONE/CLOSED`**（D2-174、177 等）——同一 disposition 值表示三种状态。
  9. **D2-083 `verdicts` 为空对象 `{}`**；另 **4 项完全缺 `verdicts` 键**（D2-103、104、105、106 —— 已由文件级 grep 逐个确认；全批 277 份中 **273 份**含 `"verdicts"`）；**D2-030 `casePath` 写 `docs/test/dataset/c-to-csharp/…`（缺 `-2`、且 `kind=NEW` 而 manifest 记 REUSE）**；**D2-100 `classifier admissionStatus=ALLOWED` 但 `cls/sha256=null` 且 `sourcePrecheck` 无 jobId**。
  10. **两个被截断的 hash 字面量**：D2-022 `finalTargetSha256="b2719673f00630dd"`（仅 16 hex）、`csprojSha256="c0c4571a683c..."`（省略号）；D2-007 `environment="INFRA_ERROR (agent/AST"` 括号不闭合。
- **敏感样式内容（合成，非真实凭证）**：D2-067 的 `independentComputation.password="P@ssw0rd!"`（源内硬编码、合成）**明文落在 item 文件**；D2-035 记掩码值 `de********23 / Pa*****d! / te**er`。**未见真实密钥/令牌**。
- **宿主路径出现于记录**：D2-116 的 `sourcePrecheck.observed` 提到 `C:\CodeConvertRemote\Stack\Agent\...`；D2-058 提到 `C:\Users\zj213\...`。**本会话未访问该目录**（仅读到记录文本）。

### F-14｜补读（read 单行上限提高至 1048576）后的**原文级**更正与新增事实

> 依据：官方 dsh 文本展示配置补丁 `harness-read-full-lines.patch.yml`。本会话同路径复读已确认生效。**未改权限/沙箱、未新增脚本、未编译/运行/调模型**。原被 2000 字符/行截断的 **34 项 × (evidence-source.json + closure.json) + 6 个 dual-build job × 4 件 + `attempt-1-truncated.json` + D2-247 job-00 health/runners 3 件**已**全部全文读到，0 件残留**。

**(a) 把「报告摘要」升级为「原件事实」的点**
1. `closure.json` 尾三字段 `oracleStatus="UNVERIFIED"`、`programOutputProvenance="UNVERIFIED"`、`checkedAt` 在 **34/34 项**成立（**含 5 个 `matched` 的 CONVERTED 项**）⇒ F-9 由「报告自报」升级为「closure 原件」。
2. `closure.artifactDigests` 键数两档：源预检 job **16 键**、dual-build job **23 键**（多 `comparison/result.json`、`comparison_manifest.json`、`evidence/target-*` 5 键，少 `source_preflight_manifest.json`）。
3. `closure.roles`：源侧恒 `{build:"passed", execution:"completed", frozenSourceObligations:"UNVERIFIED"}`；6 个 dual-build job 另有 `target{…"NOT_APPLICABLE"}`。
4. `evidence-source.json` 的 **`observations` 五维 `events` 全为空数组**、`registry`/`network` 的 `limitations` 恒为“outside the current release scope”、`toolchainFingerprint={}`、`collectorDiagnostics=[]`、`coverage.dimensions` 恒 **output-only** ⇒ 「有比较结论而无事件级观察」是**原件事实**。
5. 两侧 build/execution × stdout/stderr 的 `truncated` 字段 **恒为 `false`**。
6. D2-254 job-01 的 `exit 150` 环境归因有**原文**（stderr 606 B：`Framework 'Microsoft.NETCore.App' 8.0.0` 缺失、`10.0.12` 存在、`rid=ubuntu.26.04-x64`）。
7. D2-270 的 1178 B/digest `0fe7d9cf…62e5` 由直读确认，且 **job-00 源 / job-01 源 / job-01 目标三处相同** ⇒ 双侧逐字节一致（取代此前的“只有自述”）。
8. D2-247 `self-review-2.attempt-1-truncated.json` 元数据直读：`model="deepseek-flash"`、`finish_reason="length"`、`usage{prompt 12242, completion 65536, total 77778, reasoning_tokens 65536, cache_hit 256, cache_miss 11986}`、`system_fingerprint="aeb56401…b669"`（**其 `reasoning_content` 按用户要求不作结论**）。

**(b) 新增发现（补读才可见）**
9. **同项过程件不对称**：D2-247 `job-01-dual-build` **不存在** `controller-health-before.json`/`controller-health-after.json`/`runners-before.json`，而同项 `job-00` 三件齐备。
10. **平台自身也会截断**：D2-254 job-01 `comparison.json` 的 `targetValueSummary` 止于 `"…App: /var/lib/codeconv"`（≈120 字符）⇒ 「服务器端摘要截断」须与本机 read 截断分列。
11. **digest 与内容互斥的实例**：D2-264/274 的 `closure.artifactDigests` 列出 `evaluation_report.json`/`.md` 的正常 sha256，而本地同路径文件是 `{"detail":"…_not_found"}` 占位 ⇒ F-5 的“占位 vs 闭合”在 closure 层同样可见。
12. **重分类留痕的哈希级证据**：D2-275 `closure.artifactDigests.classification.json = bc97cf0e…c8e1` 对应**现存的 `classification-2.json`**（`-1` 已删）。

**(c) 补读 **未** 解除的不确定性（原判保持）**
13. F-1（行数三说，如 D2-241 的 495/586）、F-6（`target*`/`capsule.zip` 无实体）、F-7（`@SOURCE@`/`@TARGET@` 未替换、`request.body.json`/`target.gen.raw.json` 缺失）、F-3/F-4（路径与 contractHash 不一致）——**均与 read 上限无关**，仍属未决。
14. 本会话补读阶段 **`glob`/`grep` 已不可用** ⇒ 无法再对 667 件做机器枚举；[coverage](harness-d-coverage.md) §3.3 的逐文件名清单为**部分**（缺口如实登记）。

---

## 2. 分层结论（**不合成单一成功率**）

| 层 | 区间结论 | 依据 |
|---|---|---|
| **交付完整性** | **25/34 按去向成立**（非可转换项只要求冻结+分类+job-00）；**另 2 项**（D2-250/255/257/264/274/275/277 中的转换/预检项）**报告件为占位符且日志缺完成时间戳** ⇒ 这 7 项按 [交付契约 §2.1.1] 的“各 job 返回证据齐备”口径**不成立**；5 个转换项的目标实现与 capsule **无实体** | F-5、F-6 |
| **源侧语法/编译** | 34/34 源侧 `build` 均 `completed/exitCode=0`（`py_compile`/`ruby -c`/`py_compile`）；**这是源侧语法，不是目标结论** | 各 `evaluation_report.json` |
| **目标编译** | 仅 5 个转换项有目标；其中 D2-247（g++）、D2-254（dotnet job-02）、D2-256（go）、D2-269/270（ruby -c）均 `completed/0`；**实现件已删，无法本地复核** | 各 job-01 证据 |
| **功能一致性（行为）** | **有比较判词的 5 项全部 `matched`**（247/254/256/269/270），`diffs=0`；**0 项 `semantic_pass`、0 项 `mismatched`、0 项 `inconclusive`**；其余 **29 项从未进入功能比较**（源侧拦下/准备缺口） | `comparison.json`、`evaluation_report` |
| **安全** | 34/34 分类最终 `admissionStatus=ALLOWED`、`blockingReason=null`；无真实凭证命中；区间网络目标仅 loopback（269）或 wildcard/unresolved；批次隔离授权在有效期内 | 各 `classification-*`、`batch-authorization` |
| **环境/装置** | 区间内**未发现新增装置故障**；历史装置故障（§16 系列）出现在区间外（D2-186/189/190 等）；**D2-254 的 job-01 `exit 150` 归因环境**（runner 无 .NET 8 runtime，job-02 加 `RollForward` 后 matched） | `job-02/metadata.json` |

### 2.1 按 [比较与统计口径提案](full-review-comparison-and-statistics.md) 的口径计数（保留独立计数/未覆盖）

- **冻结范围比较通过小计（有效 matched + 有效 semantic_pass）＝ 5**（全部为 `matched`；`semantic_pass` = 0）。
- **独立计数**：`matched` 5 ｜ `semantic_pass` 0 ｜ `mismatched` 0 ｜ `inconclusive/partial` 0 ｜ **无比较件（未进入功能分母）29**。
- **未覆盖义务**（5 项各自 `coverageGaps` 原文要点）：
  - D2-247：仅冻结 `argv=[]` 单路径（33 B stdout）；wrap/fill/shorten/indent 未覆盖。
  - D2-254：仅冻结单 stdin（45 B stdout）；`posix=True`/`punctuation_chars`/文件参数/sourcehook 未覆盖。
  - D2-256：仅 `argv=[]` 帮助/错误路径（724 B + 73 B）；rip/add/checksig/sign/truncate 未覆盖。
  - D2-269：仅 connect-refused 路径（37 B）；连接成功后的 redirect/execute_shell 未覆盖。
  - D2-270：仅“无数据文件”路径（1178 B；**已于补读中直读确认：`digest sha256:0fe7d9cfff727fb156f35e4a202e1d33b93c1f7d831c014ac6ef5eaca66b62e5`，且 job-00 源/job-01 源/job-01 目标三处相同**——F-14(a)7）；有数据路径未覆盖。
- **不发布百分比**：本区间只是全批 277 项的一部分（34 项），且 29 项无比较件；按提案“全量核完前不发布本数据集百分比”。

### 2.2 跨系统消噪的可扩大范围（本区间实证）

- **有效 matched 内实际被消噪吸收的差异**：D2-247/254/256/269/270 的 `comparison.json` 均用 `preset=noise-tolerant-v1`（`text_tokens=[temporary-paths, timestamps, ephemeral-ports]`、`system_noise_patterns` 5 项、`tolerate_minor=true`、`workspace_path_pairs=[]`）；但 5 项的 `diffs=[]` ⇒ **本区间没有一处“靠消噪才通过”的例子**（即消噪未承担通过责任）。
- **D2-254 的 `mismatched`（job-01）不是业务差异**：diffs 为 `execution.exitCode`(0→150) 与两条 `stream.normalizedText`（目标为空 / 目标为 .NET 运行时报错），**归因环境**，job-02 仅改构建前提即 `diffs=[]`。⇒ 支持“装置/环境差异与业务差异分开报”，但**不据此扩大业务语义豁免**（原判保留）。
- **本区间可扩大的消噪候选**（有实证、但**本轮不改平台配置**）：
  1. **源侧 job 特定绝对路径**：D2-258 的 stderr traceback 含 `…/workspaces/eval-<jobId>/source/…`，被记为 `PREPARATION_GAP`（不可冻结）——若平台把该类路径纳入 `temporary-paths`，该项**可以**进入功能比较。
  2. **`error_report` 类占位**：不适用（本区间无）。

---

## 3. 知识层记录（新增 / 已有落实 / 错误自审 / 源已有 / 环境 / 装置 / 未定）

> 按用户要求分列。**本轮未修改任何知识真源**；下表只登记“本区间材料的可维护含义”。

### 3.1 知识新增候选（应由知识维护侧评估，**本区间不直接固化**）

| 编号 | 候选 | 本区间证据 |
|---|---|---|
| N-1 | **Python 源必须 `build-and-run` 才能暴露 import 缺口**（`py_compile` 不解析 import） | D2-243/249/253/255/259/260/264/266/267/268/271/273/274/275 的 execution `exitCode=1` 均为 `ModuleNotFoundError`/`LoadError` |
| N-2 | **`argv=[]` 回落读 stdin / 直接退出的“观察退化”反例**：冻结时必须冻非空 stdin 或非空 argv | D2-241（读 stdin 空转）、D2-257/261（无 `__main__`）、D2-236/241（区间外同型） |
| N-3 | **无入口库单元可走 `LIB_UNOBSERVABLE_COMPILE_ONLY`**（只编译不运行作为合法终态） | 13 个 `PREPARATION_GAP` 项的 `coverageGaps` 原文均提出该诉求 |
| N-4 | **Unicode 空白/行分隔符是跨语言最隐蔽差异**（`0x85`/`C2 85`、U+2028/29、`tabsize<=0` 保留 `\t`） | D2-247 自审 1/2 的 8 条建议 |
| N-5 | **容器 LIFO/FIFO 不能凭 `deque` 名推断**（源 `deque`+`appendleft`+`popleft` = LIFO） | D2-254 自审 1 误判 → 自审 2 回退 |
| N-6 | **`optparse` 长选项唯一前缀缩写**与缺参文案（`X option requires 1 argument`） | D2-256 自审 1 两条 |
| N-7 | **`stdout` digest 相同但 `stderr` 形态不同时的归因**（Go panic 栈 vs Python traceback） | D2-207（区间外，但 `optimization-inputs-2` 与 items 均引）；区间内 D2-256 的 stderr 逐字节相同 |
| N-8 | **Python `%prog` = `basename(argv[0])`**：目标以 `./program` 启动时不得用 `os.Args[0]` | D2-256 `request.user.md` L44-45 |

### 3.2 已有规则落实（本区间按现行契约落地的点）

- **分类门禁**：34/34 均先落 `frozen-inputs.md` + `classification-*`（ALLOWED/null）才推进 ✅。
- **`source/` 树变化即重分类**：D2-062/197（区间外）与本区间 D2-241/246/252/253/256/275 的 `-2` 分类件一致 ✅。
- **误生成的 `classification-1.json` 删除 + 最新分类写入 `this-task-classification.json`**：区间 6 个重分类项均照做 ✅（但见 F-11 的旧值留白）。
- **源构建失败不消耗转换调用**：29 项 `SOURCE_*`/`PREPARATION_GAP` 全部 0 模型调用 ✅。
- **不补造依赖/入口/桩**：区间无任何“补源/补入口”痕迹 ✅。
- **`buildCommand`/`runCommand` 用 argv token 数组**：区间 34 项全部为数组 ✅（对照 `optimization-inputs-2 §3.1` 的 D2-197 反例）。
- **显式相对路径**：`sourceOs=linux`，无 Windows 相对路径问题。

### 3.3 错误自审（模型自审给出但经复核**不成立**的条目）

| 项 | 自审断言 | 复核 | 后果 |
|---|---|---|---|
| D2-254 自审 1 `PB-01` | “源 `pushback` 是 FIFO，目标应改 `Queue<string>`” | **错误**：源 `shlex.py` L48 `deque()` + L76 `appendleft` + L104 `popleft` ⇒ **LIFO**；自审 2 自行推翻并回退为 `Stack<string>` | 多消耗 1 轮自修（`selfRepairRounds=2`）；**未污染最终目标**（回退后 matched） |
| D2-247 自审 1 item 6 | “`wrap/fill` 签名应改写” | 判为**语言层签名差异**（C++ 无 `**kwargs`），**拒绝采纳** | 未修（正确处置） |
| D2-256 自审 1 两条 | 长选项缩写 / 缺参文案 | **成立**（源 optparse 行为），两条 `risk` 均自述“冻结 argv=[] 不受影响” | 采纳并自修（`selfRepairRounds=1`） |
| （对照，区间外） | `D2-117` 大小写误判、`D2-123` 顺序误判、`D2-061` 装置故障误判 | 均已被批次记录登记为“自审误判、未采纳” | — |

- 区间内**未发现新的“错误自审已被采纳并落地”的实例**；D2-254 的错误自审在同项自审 2 已被纠正（**这是自审价值的一次正向实证，也说明“自审是推进信号而非防线”**）。

### 3.4 源已有 / 环境 / 装置

- **源已有**：D2-241 的“读 stdin 分支 + 空 argv”是**源自身语义**；D2-251 的 `_csv.__version__` 断言与 runner 的 `_csv` 不一致属**源接口与运行环境不匹配**（批次记为 `SOURCE_NOT_BUILDABLE`）；D2-246/252 等的 `json.org` 是**源 docstring/注释**。
- **环境**：D2-254 job-01 的 `exit 150`（runner 有 .NET SDK 10.0.112、无 .NET 8 runtime）；D2-251 的 `_csv` 接口差异。
- **装置**：区间内**无新增装置故障**；`controller.log` 缺 `finished` 与占位报告属**取证/平台侧**问题（F-5），按“装置/平台”分列，不计转换失败。

### 3.5 未定

- `Lines` 真值（F-1）、源/目标的真实 sha256（源件已删）。
- `@SOURCE@`/`@TARGET@` 实际替换内容、`request.body.json` 等是否存在过（F-7）。
- 区间内 6 个重分类项的**首轮 BLOCKED 原件**（F-11）。
- D2-271 的网络词法漏检、D2-272 的 `process[3]`、D2-265 的 `dynamic_code[10]`（源已删，F-11）。
- D2-270 的 stdout 1178 B / digest `0fe7d9cf…`（落在工具截断区，只有自述）。
- 全部 `closure.artifactDigests` 的摘要（F-8）。

---

## 4. 与**现行规则**的差异（历史说明 vs 当前规则，不改历史）

| 形态 | 批次当时（2026-10-10…12） | 现行根 `SKILL.md` 第 5 步 | 本区间影响 |
|---|---|---|---|
| 源可构建 + 无合法行为入口/观察不可冻结 | `PREPARATION_GAP`，**生成前停止、0 模型调用** | 记 **`LIB_UNOBSERVABLE_COMPILE_ONLY`**，**继续生成 + 自审 + 目标语法/编译验证**，`PARTIAL` | **13 项**（D2-241、245、246、252、257、258、261、262、263、265、272、276、277）按现行规则**本应继续转换** |
| 源构建失败（`SOURCE_NOT_BUILDABLE`/`SOURCE_DEPENDENCY_GAP`） | 跳过、0 模型调用 | **同** | 无差异（区间 **16 项** = 15 `SOURCE_DEPENDENCY_GAP` + 1 `SOURCE_NOT_BUILDABLE`） |
| oracle 不可冻结但可运行 | `PARTIAL`/`ORACLE_NOT_FREEZABLE`，保留平台 verdict | **同** | 区间内无此形态（0 项） |
| 纯文档审阅 | 不触发转换步骤 | **同** | 本轮即纯文档审阅 |

⇒ **规则版本差异，不追改原判定**；但这是本区间（乃至全批）**最大的口径落差**：38 项全批 `PREPARATION_GAP` 中有 13 项落在本区间。

---

## 5. 与两份参考稿的对照

- **[full-review-knowledge-disposition.md](full-review-knowledge-disposition.md)**：其 K-A…K-AA 27 簇与“已明确拒绝直接固化的建议”名单**完全不含 D2-241…277 的任何项**（该稿覆盖的是 96 份正式自审，主要落在 D2-001…240）。⇒ **本区间不构成对该稿结论的补充或反驳**；本区间的 N-1…N-8 属**新增候选**，须由知识维护侧另行评估，**本会话未写入任何知识真源**。
- **[full-review-comparison-and-statistics.md](full-review-comparison-and-statistics.md)**：本区间按其口径给出独立计数（§2.1）——**有效 matched + 有效 semantic_pass = 5**，并**保留** `matched`/`semantic_pass`/无比较件的独立计数与 5 项未覆盖义务。**未发布百分比**。该稿“§4 当前系统还须改的表达与能力”里第 2/5 条（`matchedDimensions` 不闭合、digest 生产者口径）在本区间**未获新证据**（5 项 `diffs=[]`，无 digest 冲突实例）。

---

## 6. 未读集合与工具限制（如实登记）

- **本会话（含派出的只读子会话）已逐件读完**：34 个用例目录下的**全部现存文件**（合计 **667** 件：python-to-cpp 113、python-to-csharp **139**〔见下〕、python-to-go 133、python-to-powershell 105、python-to-ruby 132、ruby-to-c 45）。
  - ⚠ **计数不一致**：`glob python-to-csharp/**` 报 **138** 条，而按目录逐项清点为 **139**（249–253 各 15 = 75，D2-254 = 64）⇒ **±1 未定**（可能是 glob 去重或某目录多一文件的写法差异），已在 [coverage](harness-d-coverage.md) 标注。
- **未逐件读**：`batch/items/*.json` 的 **001–240 与 278–300** 段（由本会话另派子会话清点，见 coverage 检查点）；区间外的用例目录。
- **非文本件未读**：`batch/platform-probes/` 下的 `capsule.zip` 等归档（用户口述“纯文档审阅”，且非文本）。
- **工具限制**：`pwsh` 全程不可用（沙箱 ACL 授予失败）；`read`/`grep` 对 **单行 >2000 字符**的 JSON 只能读前缀（区间内大量 `closure.json`/`evidence-source.json`/`evidence-target.json`/`evaluation_report.json`/`*.model.json`/`attempt-1-truncated.json`）。凡截断处均标“工具截断”，**未编造**；能用 grep 探针确认的键值已确认。
- **未做**：未运行哈希、未编译运行、未调用模型、未提交评估、未访问 `.env`/凭证/`D:/CodeConvertRemote/Stack`。

---

## 7. 发现清单（按可行动性排序）

| 编号 | 发现 | 类别 | 依据 |
|---|---|---|---|
| **D-1** | **13 项 `PREPARATION_GAP` 按现行规则应走 `LIB_UNOBSERVABLE_COMPILE_ONLY`（继续生成）** | 口径落差 | §4 |
| **D-2** | **7 项报告占位 + 日志缺 `finished`，却被 closure/result 记为已闭合/交付完整** | 证据完整性 | F-5 |
| **D-3** | **`manifest.csv` 的 `Lines` 33/34 与冻结/结果不符；源已删不可裁定** | 台账一致性 | F-1 |
| **D-4** | **5 个转换项的 `capsule.zip` 与目标实现无实体，且路径口径三说** | 交付实体 | F-6 |
| **D-5** | **实际注入模型的源/目标全文不可审**（`@SOURCE@`/`@TARGET@` 未替换 + 请求体缺失） | 可复核性 | F-7 |
| **D-6** | **6 个重分类项的首轮 BLOCKED 判定无原件留存**（`old_cls/old_reason=null`） | 溯源 | F-11 |
| **D-7** | **D2-247 的 2 个失败 attempt 只在 items/model.json 记，events/对账只承认 1 个** | 记载差集 | F-12 |
| **D-8** | **D2-247 缺 `self-review-2.model.json`；D2-246 缺 health/runners 件** | 元数据链 | F-10 |
| **D-9** | **D2-246 `batch-authorization` 误引 D2-197** | 记录错项 | F-10 |
| **D-10** | **根 `batch-authorization` 与用例副本 `contractHash` 不一致**；`batch.json` 的 `datasetRoot`/`manifest` 与实际路径不符 | 台账一致性 | F-3、F-4 |
| **D-11** | **闭包自报 `oracleStatus/programOutputProvenance=UNVERIFIED`**，与 `matched` 并存的语义需在报告层显式说明 | 分层表达 | F-9 |
| **D-12** | **`closure.artifactDigests` 引用 Controller 侧命名，本地全部 UNVERIFIED** | 可复核性 | F-8 |
| **D-13** | **分类件内部张力**（`signals.network=[]` vs `has_network=true`；`REVIEW_SENSITIVE` vs `sensitive=[]`；wildcard/unresolved 却 `requiresNetworkIsolation=false`；授权件“无网络”vs 分类判网络） | 分类口径 | F-11 |
| **D-14** | **D2-254 的自审 1 误判（FIFO）被自审 2 纠正**：自审数量/建议数不等于已证实缺陷数 | 自审治理 | §3.3 |
| **D-15** | **D2-247 有一条 `origin=source-preexisting` 的建议仍触发了修复**（`self-repair-2` 的 `feedback_source` 却写“both conversion-introduced”） | 归因一致性 | F-（见 cases-01） |
| **D-16** | `python-to-csharp` 文件计数 glob 138 vs 逐项清点 139（**±1 未定**） | 计数 | §6 |
| **D-17** | **items 全 277 份逐件复核与批次汇总逐项吻合**（226/20/31、60/88/22/38/4/1/64）——批次汇总数字可信 | 正向核实 | F-13 |
| **D-18** | **item 内部形制高度不一致**（10 项缺 classifier；`usage` 两套；`blockingReason(s)` 并存；覆盖字段三种；classifier 2.3/2.4 混用；`disposition=FROZEN` 表示三种状态；D2-083 `verdicts={}`；D2-030 casePath 缺 `-2`；D2-022 两个截断 hash） | 台账形制 | F-13 |
| **D-19** | **合成口令明文落盘**（D2-067 `P@ssw0rd!`）与**宿主/Controller 路径出现在 item 记录**（D2-116、D2-058） | 记录卫生 | F-13 |
| **D-20** | **原截断原件已全部补读**（34 项 evidence-source + closure、6 个 dual-build job × 4 件、`attempt-1-truncated.json`、health/runners 3 件），**0 件残留**；`oracleStatus/programOutputProvenance=UNVERIFIED` 与「`observations.events` 全空」升为原件事实 | 证据核读 | F-14 |
| **D-21** | **新增两项原件级发现**：同项 `job-01` 缺 health/runners 三件（过程件不对称）；平台自身截断 `targetValueSummary`（须与本机截断分列） | 证据完整性 | F-14(b) |
| **D-22** | **逐文件名机器枚举未完成**：补读阶段 `glob`/`grep` 不可用，667 件的完整名单无法再枚举；§2.3 已列实际 `read` 的文件名并登记缺口（**部分**） | 覆盖登记 | F-14(c)14 |
