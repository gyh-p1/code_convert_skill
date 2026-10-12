# Harness D — 逐项审阅记录 04（python-to-powershell：D2-262 … D2-268）

> 7 例 × **15 件** = 105 件，由本会话派出的只读子会话逐件读取，本会话与 batch 层交叉核对。
> **结构一致**：每例仅 `01-frozen/`（frozen-inputs.md、classification-1.json、classifier-input-1.json）+ `04-evaluation/job-00-source-buildability/`（6 契约件 + returned-evidence 5 件）+ `result.md`；**无** `02-conversion`、`03-self-review`、`job-01`、`evaluator_manifest.json`、`source/`、`target/`、任何 capsule。
> **口径**：`manifest.csv` 对 NEW 项 `JobId=""`、`Evidence="UNVERIFIED (not built, not run)"` 属**数据集设计**（[README §3](../../README.md)），不计缺件；真问题是 **`Lines` 列 7/7 与 frozen/result 不符**。

| taskId | 源文件 | manifest Lines | frozen/result 行数 | cls | 源预检 job | build | execution | 去向 |
|---|---|---|---|---|---|---|---|---|
| D2-262 | hashlib.py | 207 | **253** | REVIEW_SIDE_EFFECTS | `eval-20261012-051223-c5963ae3` | completed/0 (35ms) | completed/**0** (19ms)，两流 0 B | PREPARATION_GAP |
| D2-263 | hmac.py | 179 | **219** | LOW_SIGNAL | `eval-20261012-051333-466816ff` | completed/0 (68ms) | completed/**0** (19ms)，两流 0 B | PREPARATION_GAP |
| D2-264 | samrdump.py | 203 | **256** | REVIEW_NETWORK | `eval-20261012-051444-b1edede1` | completed/0 (36ms) | completed/**1** (119ms)，stderr=impacket L29 | SOURCE_DEPENDENCY_GAP |
| D2-265 | fnmatch.py | 168 | **185** | REVIEW_SENSITIVE | `eval-20261012-051611-a22ac1ba` | completed/0 (66ms) | completed/**0** (16ms)，两流 0 B | PREPARATION_GAP |
| D2-266 | GetADUsers.py | 173 | **197** | REVIEW_NETWORK | `eval-20261012-051720-a9778618` | completed/0 (66ms) | completed/**1** (116ms)，stderr=impacket L32 | SOURCE_DEPENDENCY_GAP |
| D2-267 | lookupsid.py | 166 | **204** | REVIEW_NETWORK | `eval-20261012-051846-432d9645` | completed/0 (67ms) | completed/**1** (118ms)，stderr=impacket L27 | SOURCE_DEPENDENCY_GAP |
| D2-268 | rpcdump.py | 172 | **208** | REVIEW_NETWORK | `eval-20261012-052014-dd83f90f` | completed/0 (67ms) | completed/**1** (117ms)，stderr=impacket L27 | SOURCE_DEPENDENCY_GAP |

## 逐项要点

### D2-262 hashlib.py — PREPARATION_GAP
- frozen（28 行）：sha256 `F0C890…A013`、253 行；CPython stdlib 副本、**无 `__main__`**；依赖 `_sha1/_md5/_sha2/_blake2/_sha3`(L89-113)、`_hashlib`(L170/182/190)。
- 分类 `classification-1.json`（65 行）：`REVIEW_SIDE_EFFECTS`、`ALLOWED`/null、2.4、`009a6f31…f3a4`、`requiresNetworkIsolation=false`；signals filesystem=[199]；`inputManifestSha256=f19449d5…cca8`。**首轮 ALLOWED，无重分类、无旧件删除**。
- job：build-and-run；`py_compile hashlib.py` / `python hashlib.py`；build completed/0(35ms)、execution **completed/0**(19ms)、**stdout/stderr 均 0 B**（`e3b0c442…` 空串摘要）。`closure`：`complete/cleanupConfirmed=true`、`issues=[]`、`attempts=1`、`READY`（截断于 `"ora…`）。`controller.log` created `05:12:23.584956Z` → finished `05:12:53.548454Z`；两报告件正常。
- `items/D2-262.json`：`PREPARATION_GAP`/`DONE`、`usage.modelCalls=0`、`coverageGaps` 提出“合法中性入口或逐项 `LIB_UNOBSERVABLE_COMPILE_ONLY` 举证”。
- **与现行规则对照**：属 `LIB_UNOBSERVABLE_COMPILE_ONLY` 形态 ⇒ 现行规则下应继续生成 + 目标语法/编译验证（本项 0 模型调用停止）。

### D2-263 hmac.py — PREPARATION_GAP
- frozen（27 行）：sha256 `C9FC1D…C72C`、219 行；CPython stdlib 副本、无 `__main__`。
- 分类（61 行）：`LOW_SIGNAL`、`ALLOWED`、**`reviewGroups=[]`、signals 全空**、`inputManifestSha256=eda3da09…6a0b`。
- job：build completed/0(68ms)、execution completed/0(19ms)、**两流 0 B**；closure 同型；log `05:13:33.970778Z → 05:14:04.279280Z`；报告正常。

### D2-264 samrdump.py — SOURCE_DEPENDENCY_GAP（**本组唯一证据残缺项**）
- frozen（31 行）：sha256 `83CA34…0C83`、256 行；Impacket 工具有入口；外部依赖 `impacket.*`(L29-33)。
- 分类（70 行）：`REVIEW_NETWORK`、`ALLOWED`、signals network=[145,146,219]、process=[204]、`network_mode=unresolved`。
- job：build completed/0(36ms)、execution completed/**1**(119ms)、stdout 0 B、stderr = `Traceback … samrdump.py", line 29, in <module>\n from impacket.examples import logger\nModuleNotFoundError: No module named 'impacket'`（**stderr 的 sizeBytes/digest 落在工具截断区，不可读**）。
- **⚠ 报告缺件**：`evaluation_report.md` = `{"detail":"job_human_report_not_found"}`；`evaluation_report.json` = `{"detail":"job_report_not_found"}`；`controller.log` **只有 created `05:14:44.604345Z`，无 finished**。而 `closure.json` 仍记 `complete=true`、`cleanupConfirmed=true`、`issues=[]`、`attempts=1`，`result.md` 亦写“交付完整性 完成”。
  ⇒ **同一 job 内“报告未取回”与“closure 已闭合/交付完整”并存**（与本区间 D2-250/274/275/277 同类）。

### D2-265 fnmatch.py — PREPARATION_GAP
- frozen（27 行）：sha256 `146D27…0425`、185 行；CPython stdlib 副本、无 `__main__`；**纯标准库自包含**（os/posixpath/re/functools）。
- 分类（68 行）：`REVIEW_SENSITIVE`、`reason=sensitive_or_dynamic_operations`、`ALLOWED`、**`requiresSyntheticData=true`**；signals **dynamic_code=[10]**、process=[31]、sensitive=[]、network=[]。
  ⇒ **冻结画像（纯标准库、无动态代码）与该 signals 不一致**；`optimization-inputs-2.md §3.3` 把这类归为分类器词法口径问题（记录，不改判；源已删无法定性）。
- job：build 0(66ms)、execution 0(16ms)、**两流 0 B**；报告正常；log `05:16:11.516471Z → 05:16:40.613001Z`。

### D2-266 GetADUsers.py — SOURCE_DEPENDENCY_GAP
- frozen（31 行）：sha256 `A7A882…B543`、197 行；Impacket、有入口 L143；`impacket.*`(L32-36)。
- 分类（65 行）：`REVIEW_NETWORK`、`ALLOWED`、network=[149]、unresolved。
- job：build 0(66ms)、execution **1**(116ms)、stderr=impacket L32；closure/log/报告正常（log `05:17:20.316710Z → 05:17:49.642117Z`）。

### D2-267 lookupsid.py — SOURCE_DEPENDENCY_GAP
- frozen（31 行）：sha256 `1D3C3E…38C5`、204 行；Impacket、有入口；`impacket.*`(L27-32)。
- 分类（68 行）：`REVIEW_NETWORK`、`ALLOWED`、network=[86,95,167,168]、unresolved。
- job：build 0(67ms)、execution **1**(118ms)、stderr=impacket L27；报告正常（log `05:18:46.410891Z → 05:19:15.572244Z`）。

### D2-268 rpcdump.py — SOURCE_DEPENDENCY_GAP
- frozen（31 行）：sha256 `C6BA4A…072E`、208 行；Impacket、有入口 L167；`impacket.*`(L27-32)。
- 分类（67 行）：`REVIEW_NETWORK`、`ALLOWED`、network=[107,155,181]、unresolved。
- job：build 0(67ms)、execution **1**(117ms)、stderr=impacket L27；报告正常（log `05:20:14.598813Z → 05:20:43.858990Z`）。

## 本组共性（原始事实 / 判定 / 未定）

**原始事实**
- 7/7 只有**源侧预检**（`evaluationMode=build-and-run`），**无 comparison、无 `matched|semantic_pass|mismatched`、无 `diffs`**（`items` 亦写 `comparison:"n/a"`、`targetBuild:"not attempted"`）。
- 7/7 `closure.complete=true`、`cleanupConfirmed=true`、`issues=[]`、`cleanupRecords.source.attempts=1`、`contaminated=false`、`runnerStateAfter=READY`；`evaluation_report.json` 7/7（除 264）为 `COMPLETED/FINISHED`、`buildAssessment=passed`、`executionAssessment=completed`、`baselineAssessment=UNVERIFIED`、`failure=null`。
- 7/7 无重分类、无旧件删除、无失败 attempt、无 WAITING。
- 运行时坐标一致：`CC-Eval-Linux-8Lang-1.0.29`、`linux-vm-agent-x64`、collector/agent `1.0.0`。

**判定（本会话）**
- 262/263/265 的“无入口库模块 + 空输出”与 `PREPARATION_GAP` 自洽；按现行规则应走 `LIB_UNOBSERVABLE_COMPILE_ONLY`（继续生成 + 目标语法/编译验证）。
- 264/266/267/268 的 `ModuleNotFoundError: impacket` 与 `SOURCE_DEPENDENCY_GAP` 自洽（`py_compile` 通过、运行才暴露，属“Python 源须 build-and-run”纪律）。
- **264 的报告占位 + log 缺 finished 是真实证据缺口**；`closure`/`result.md` 的“已完成”与该缺口并存。
- **`Lines` 7/7 不一致**（manifest 偏小 17–53 行）；源件不存在 ⇒ 无法定案哪一侧为真。

**未定**
- 各例真实行数与 sha256：源件均不在工作区，**不可复核**（子会话亦未获授权算哈希）。
- D2-265 的 dynamic_code/process 信号与冻结画像的矛盾：源已删，**不可定性**。
- 全部单行超长 JSON（7×`evidence-source.json` + 7×`closure.json`）被工具 2000 字符/行截断；`closure` 的 `"ora…"` 段与部分 stderr 尺寸/digest **未读到，不臆测**。
- `closure.artifactDigests` 引用的 `evidence/source-call.json`、`source-identity.json`、`source-request.json`、`source-response.json/.body`、`lifecycle.jsonl`、`request.json`、`staging-manifest.json` 在本地目录**均不存在**（Controller 侧 job 目录命名），无法据本地件核对哈希。
- 7/7 `frozen-inputs.md` 写 `sourceOs=targetOs=linux`，但无 target 件、`targetBuild: not attempted` ⇒ **targetOs 无证据**。

---

## 补读（read 单行上限提高至 1048576 后，2026-10-12）

**本组原截断件（14 件：7×`evidence-source.json` + 7×`closure.json`）已全部全文读到**，第 76 条所列的“未读到，不臆测”部分**全部解除**。

**补读新增的原文事实（本组）**
1. **closure 尾段（7/7）**：`artifactDigests` **16 键**；尾三字段 `"oracleStatus":"UNVERIFIED"`、`"programOutputProvenance":"UNVERIFIED"`、`"checkedAt"`——与报告摘要一致，但现在是原文依据。
2. **此前不可读的 stderr size/digest 全部取得**：D2-264 `sha256:cb3fb313f015e6206b67e1ed9e0639bc5268485fbf4dec7214fbcc6d05d7ca30`/242 B（samrdump.py L29 impacket）；D2-266 `sha256:dcd6367dbadb7b4e8488db4a07f9d4e7587d8e74cd8cdd3997151da2274cef4f`/236 B（GetADUsers.py L32）；D2-267 `sha256:30a9e2cca0fa9008267683115d61ce7f1c2ed142895058b99774be1c88b0cd50`/243 B（lookupsid.py L27）；D2-268 `sha256:1f25a26c0de7e7169a3c86179379793c5ad51bbba5bfe22f876232f5fb78e65d`/240 B（rpcdump.py L27）。
3. **262/263/265 的“两流 0 B”现为原文**：`sizeBytes 0`、`digest sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`（空串摘要）、`truncated:false`、`encoding:"utf-8"`。
4. **D2-264 的报告占位与 closure 的原文并置**：`closure.json` 全文含 `"complete":true, "cleanupConfirmed":true, "issues":[], "cleanupRecords":{"source":{"status":"passed","runnerStateAfter":"READY","attempts":1,"contaminated":false,"reason":null}}`，且其 `artifactDigests` 仍列出 `evaluation_report.json` 的 `sha256:d5725433…` 与 `evaluation_report.md` 的 `sha256:3b64a48f…`——**这两个哈希对应的文件在本地却是 `{"detail":"job_report_not_found"}` 占位**（digest 与内容互斥）。
5. `evidence-source.json` 全结构与 cases-01 补读第 3 条同型：`baselineReference.snapshot="CC-Eval-Linux-8Lang-1.0.29"`、`toolchainFingerprint {}`、`runtime.workspaceRef="workspace/source"`、`observations.*.events` 全空、`coverage.dimensions.output="observed"` 其余 `not-applicable`、`collectorDiagnostics:[]`。

**未解除**：`Lines` 7/7 不一致；D2-265 的 `dynamic_code/process` 信号与冻结画像矛盾（源已删）；7×`closure.artifactDigests` 所列 `evidence/*`、`request.json`、`staging-manifest.json` 等**在本地目录仍不存在**（Controller 侧命名）——补读只解除了“本机 read 截断”，**未解除“本地缺件”**。
