# Harness D — 逐项审阅记录 06（ruby-to-c：D2-275 / D2-276 / D2-277）

> 本文件由本会话派出的只读子会话逐件读取（read/glob/grep，未写文件、未运行脚本），并由本会话与 batch 层交叉核对后写成。
> 每例目录 **15 个文件**（glob 无 spill）；三例均**无** `source/`、`target*`、`capsule`、`02-conversion`、`03-self-review`、`evaluator_manifest.json`。
> 三例共同点：均为 **build-and-run 源侧预检**（`/api/source-preflights`）、**0 模型调用**、`lifecycle=DONE`。

---

## D2-275 — ruby-to-c / firefox_creds.rb

**manifest 行（第 253 行）**：`"D2-275","NEW","ruby-to-c","Ruby","C","firefox_creds.rb","642","测试用例ruby\凭证访问\firefox_creds.rb","","2CA3183303982868FB70970BF477BB3F071A25A01F974309D4181B953D56CE19","UNVERIFIED (not built, not run)"`。

### 冻结 / 分类
- `01-frozen/frozen-inputs.md`（30 行）：sourceOs=targetOs=`linux`(x64)；源 `source/firefox_creds.rb`、sha256 `2CA318…CE19`（大写，取自 manifest）、**748 行**；`casePath` 写 `docs/test/dataset-2/...`（与实际目录不符）；预判 `SOURCE_DEPENDENCY_GAP`；argv=[]、stdin=null；buildCommand `ruby -c firefox_creds.rb`、runCommand `ruby firefox_creds.rb`；分类器 v2.4 钉 SHA；`contractHash=sha256:8090cfcc…`。
- 分类：**重分类**。`events.jsonl:1063` 首轮 `BLOCKED`/`public_network_unverified`（`cls=REVIEW_DEPENDENCY`）；`:1064` 加 `--network-isolation-configured` ⇒ `classification-2.json` `ALLOWED`，note 明写“`classification-1.json removed`”。
- `01-frozen/classification-2.json`（102 行）：`cls=REVIEW_DEPENDENCY`、`reason=framework_dependency_requires_environment`、`ALLOWED`/`blockingReason=null`、classifierSha256 `009a6f31…f3a4`、`requiresNetworkIsolation=true`、`requiresSyntheticData=true`、`executionApproved=true`、`executable=false`、`old_cls=null`/`old_reason=null`；signals：filesystem[168]、process[245,256,381,728]、discovery[728,741]、sensitive[18]、framework[9,10,11,12]；`network_targets`：`github.com`(L33/L34, hostname, redirectVerified=false)；`limitations=["ruby_heredoc_or_block_comment_requires_review"]`。
- `classifier-input-2.json`（1 行）：sourceSha256 大写 = manifest ✅。
- job 内 `this-task-classification.json` 与 classification-2 **逐字段一致**（对象 vs 数组之别）✅。

### job（唯一）
`eval-20261012-053827-33b3309a`（`job-id.txt`、`events.jsonl:1065` 一致）。
`source_preflight_manifest.json`：`build-and-run`、`["ruby","-c","firefox_creds.rb"]` / `["ruby","firefox_creds.rb"]`、linux/x64/ruby。
`input_profile.json`：argv `[]`、stdin null、timeout 60、维度 `["output"]`、stdout/stderr 均 `normalized-text`。
真实回传（`evidence-source.json`，**单行超长 ⇒ 工具截断**）：
- build `completed` / exitCode **0** / 34 ms；stdout `"Syntax OK\n"`（10 B）；stderr 0 B；
- execution `completed` / exitCode **1** / 268 ms；stdout 0 B；stderr 起于 `<internal:/usr/lib/ruby/vendor_ruby/rubygems/core_ext/kernel_require.rb>:136:in 'require': cannot load such file -- zip (LoadError)` … `from firefox_creds.rb:7:in '<main>'`（**该处被 2000 字符行上限截断**，其后的 sizeBytes/digest/truncated/encoding 与 observations 未读到）。
`closure.json`（**工具截断**）：`complete=true`、`cleanupConfirmed=true`、`issues=[]`、`cleanupRecords.source={passed, READY, attempts:1, contaminated:false}`、`roles.source={build:passed, execution:completed, frozenSourceObligations:UNVERIFIED}`；截断点落在 `,"ora`（其后存在 `"oracleStatus"`）；全文**不含** comparison/verdict/matched/mismatch/semantic。
`controller.log`：**只有 `created 2026-10-12T05:38:27.751723+00:00`，无 `finished` 行**。
`evaluation_report.md` = `{"detail":"job_human_report_not_found"}`；`evaluation_report.json` = `{"detail":"job_report_not_found"}` ⇒ **两份报告件均为占位符**（而 `closure.artifactDigests` 仍列 `evaluation_report.json/md` 的 sha256）。

### 结果与去向
`result.md`（41 行）：**DONE / `SOURCE_DEPENDENCY_GAP`**；源 748 行；job 同上；build `completed/0`、execution `completed/1`（stderr=L7 `require 'zip'`）；closure true/true；0 模型调用；声明交付含“capsule”。
`items/D2-275.json` 与 `events.jsonl:1063–1066` 一致（`usage.modelCalls=0`）。

### 缺口
1. **无实现树**：`source/`、`target.c` glob 0 命中 ⇒ frozen 自称的 sha256/748 行**无法本地复核**；“交付含 capsule”而全区间无任何 `.zip`。
2. **manifest 三列失真**：`JobId=""`、`Evidence="UNVERIFIED (not built, not run)"`（实际已预检）、`Lines=642`（frozen/result 均 748）。
3. **报告占位** + `controller.log` 无 finished，与 `closure.complete=true` 并存 ⇒ 证据不一致。
4. `classification-1.json` 已删，原始 BLOCKED 件**不可读**（仅存 events/items/result/metadata 记述）。

---

## D2-276 — ruby-to-c / benchmark.rb

**manifest 行（第 254 行）**：`…"benchmark.rb","531","测试用例ruby\收集\benchmark.rb","","F05E8ACCBC88DB94A9F7CF01A43E5F19B6B649B204D9925B07872CFE945CAFF5","UNVERIFIED (not built, not run)"`。

- `frozen-inputs.md`（27 行）：sha256 `F05E8ACC…AFF5`、**582 行**；CRuby stdlib 副本、无 require、无入口守卫；预判 `PREPARATION_GAP`；`ruby -c`/`ruby`。
- `classification-1.json`（67 行）：`cls=REVIEW_UNCERTAIN`、`reason=lexical_coverage_incomplete`、`ALLOWED`/null、v2.4、`requiresNetworkIsolation=false`；signals 仅 `process[398]`；`network_mode=none-detected`；`old_cls=null`。**无重分类**（initial pass）。
- job `eval-20261012-054000-721689a3`：build `completed`/exit **0**/17 ms、stdout `"Syntax OK\n"`(10 B)；execution `completed`/exit **0**/116 ms、**stdout/stderr 均 0 B**；`evaluation_report.json` 完整可读（`jobStatus=COMPLETED`、`jobPhase=FINISHED`、`evaluationMode=build-and-run`、`buildAssessment=passed`、`executionAssessment=completed`、`baselineAssessment.status=UNVERIFIED`、`cleanup.status=passed`、`failure=null`、`createdAt 2026-10-12T05:40:29.622759Z`）；`evaluation_report.md` 23 行完整。
- `controller.log`：**created 05:40:00.438854Z + finished 05:40:29.647544Z**（完整）。
- `closure.json`（工具截断）：`complete=true`、`cleanupConfirmed=true`、`issues=[]`、`cleanupRecords.source={passed, READY, 1, false}`；全文不含 comparison/verdict/matched。
- `result.md`（34 行）：**DONE / `PREPARATION_GAP`**，0 模型调用。
- **缺口**：manifest `JobId=""`、`Evidence=UNVERIFIED`、**`Lines=531` vs frozen/result 582**；无实现树（sha256/行数不可复核）。

---

## D2-277 — ruby-to-c / prettyprint.rb

**manifest 行（第 255 行）**：`…"prettyprint.rb","508",…,"7850E31159491131A85A9A3D98B980EFB62DF0F8F8297DFA6AC767035428D279","UNVERIFIED (not built, not run)"`。

- `frozen-inputs.md`（27 行）：sha256 `7850E311…D279`、**556 行**；CRuby stdlib 副本；预判 `PREPARATION_GAP`。
- `classification-1.json`（63 行）：`cls=REVIEW_UNCERTAIN`、`ALLOWED`/null、v2.4、`requiresNetworkIsolation=false`；**`reviewGroups=[]`、全部 signals 空**、`network_mode=none-detected`。
- job `eval-20261012-054113-34e6e416`：build `completed`/exit **0**/17 ms、stdout `"Syntax OK\n"`(10 B)；execution `completed`/exit **0**/66 ms、**两流 0 B**。
- `controller.log`：**只有 created 05:41:13.438236Z，无 finished**。
- `evaluation_report.md` / `.json` **均为占位符**（`job_human_report_not_found` / `job_report_not_found`）。
- `closure.json`（工具截断）：`complete=true`、`cleanupConfirmed=true`、`issues=[]`。
- `result.md`（34 行）：**DONE / `PREPARATION_GAP`**，0 模型调用。
- **缺口**：同 276（`JobId` 空、`Evidence` 未回填、`Lines=508` vs 556）；报告占位 + log 无 finished 与 closure complete 并存。

---

## 三例共同结论（原始事实 / 判定 / 未定分开）

**原始事实**
- 三例都只做了 **source-only 源预检**（`build-and-run`），没有任何目标生成、没有双侧 job、没有 comparison 判词；closure/evidence 中不含 `matched`/`mismatched`/`semantic` 键。
- 三例 `closure.complete=true`、`cleanupConfirmed=true`、`issues=[]`、`attempts=1`、`contaminated=false`、`runnerStateAfter=READY`。
- 三例均无失败 attempt、无 WAITING。
- manifest 三行（253/254/255）的 `JobId` 为空、`Evidence` 仍为 `UNVERIFIED (not built, not run)`；`Lines` 分别为 642/531/508，与 frozen+result 的 748/582/556 不符。
- 用例目录下**无源文件、无目标、无 capsule**；`frozen-inputs.md` 与 `items` 的 `casePath` 均写 `docs/test/dataset-2/...`（与实际 `docs/dataset-2/dataset-2-copy/...` 不一致）。

**判定（本会话）**
- 三例的**非可转换去向**（1×`SOURCE_DEPENDENCY_GAP` + 2×`PREPARATION_GAP`）与其**真实源侧诊断**自洽（D2-275 = `LoadError: zip`；276/277 = 无入口库模块、运行空输出）。
- 按现行根 `SKILL.md` 第 5 步，276/277 属 **`LIB_UNOBSERVABLE_COMPILE_ONLY`** 形态：**应继续生成并做目标语法/编译验证**，而非停在 0 模型调用（规则版本差异）。
- 276 的 job 证据最完整（报告 + log finished）；**275/277 的报告占位与 log 缺 finished 是真实的证据件缺口**（不是工具问题）。

**未定**
- 三例真实行数（642/531/508 还是 748/582/556）：源已删，**无法定案**。
- 275 首轮 BLOCKED 分类原件：已删，**不可读**。
- 工具截断处（275 与 277 的 `evidence-source.json`/`closure.json` 尾部）未被读到，**不臆测**。

---

## 补读（read 单行上限提高至 1048576 后，2026-10-12）

**本组原截断件（6 件：三例各 `evidence-source.json` + `closure.json`）已全部全文读到**，上列“未读到，不臆测”**全部解除**。

**补读新增的原文事实（本组）**
1. **D2-275 完整 stderr**：`sizeBytes 265`、`digest sha256:6130ae76dc7be57be0df35dd529ea2966f8008e825baa7374175f2edfb8f8b83`、`exitCode 1`（`<internal:…kernel_require.rb>:136:in 'require': cannot load such file -- zip (LoadError)` → `from firefox_creds.rb:7:in '<main>'`）；build stdout `"Syntax OK\n"` 10 B（`bbafef10…4a1b`）、exit 0。
2. **D2-276 / D2-277** 现为原文：build `completed/exitCode 0/17 ms`、stdout `"Syntax OK\n"` 10 B；execution `completed/exitCode 0`（276 = 116 ms、277 = 66 ms），**两侧流 `sizeBytes 0`、空串 digest `e3b0c442…b855`、`truncated:false`**。
3. **closure 尾段（三例）**：`artifactDigests` 均 **16 键**；尾三字段 `"oracleStatus":"UNVERIFIED"`、`"programOutputProvenance":"UNVERIFIED"`、`"checkedAt"`（275 `05:39:09.597627+00:00`、276 `05:40:29.645961+00:00`、277 `05:41:46.947671+00:00`）；`roles.source={build:"passed", execution:"completed", frozenSourceObligations:"UNVERIFIED"}`。
4. **D2-275 的重分类留痕（哈希级）**：其 `closure.artifactDigests.classification.json = sha256:bc97cf0e0a3dd423aecb5b0a414ab5f619dde2e498ab1c0ba2d86668b659c8e1`，对应**现存的 `classification-2.json`**（`classification-1.json` 已删）⇒ 「旧判原件不可复核」在 closure 层也成立。
5. `evidence-source.json` 结构与本区间同型（`baselineReference.snapshot="CC-Eval-Linux-8Lang-1.0.29"`、`toolchainFingerprint {}`、`runtime.workspaceRef="workspace/source"`、`observations.*.events` 全空、`coverage` output-only、`collectorDiagnostics:[]`、`truncated:false`）。

**未解除**：`Lines` 3/3 不一致（642/531/508 vs 748/582/556）；275/277 报告占位 + `controller.log` 缺 `finished` 与 `closure.complete=true` 并存；三例无源/目标/capsule 实体——**均不因补读改变**。
