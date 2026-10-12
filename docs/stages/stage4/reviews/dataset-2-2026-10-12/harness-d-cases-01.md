# Harness D — 逐项审阅记录 01（python-to-cpp：D2-241 / 243 / 245 / 246 / 247）

> 本文件由本会话逐件只读审阅写成（D2-246/247 由本会话派出的只读子会话逐件读取后并入）；`READ` 依据 = 对该用例目录 `glob` 出的**每一个现存文件**逐个执行 `read`（单行超长 JSON 只能读前缀，逐项标注“工具截断”）。
> **件数（glob 实测）**：D2-241 **15**、D2-243 **15**、D2-245 **15**、D2-246 **15**、D2-247 **53** —— 计 **113**，与 `python-to-cpp/**` glob 的 113 条一致（241+243+245+246 = 15×4 = 60，加 247 的 53 = 113）。
> 源/目标实现已删（目录下无 `source/`、无 `target*`），故不对实现正文作任何结论。
> manifest 行核对对象：`docs/dataset-2/dataset-2-copy/manifest.csv`。
> **口径**：NEW 项在 manifest 里 `JobId=""`、`Evidence="UNVERIFIED (not built, not run)"` 属**数据集设计**（[README §3](../../README.md)）；真冲突在 **`Lines` 列**。

---

## D2-241 — python-to-cpp / base64.py

**身份**：manifest `"D2-241","NEW","python-to-cpp","Python","C++","base64.py","495","数据集python\防御规避\base64.py","","9E685425290C771DF1A277B5C7787AD5D4CF0312F2C4B042CE44756DF6A3D112","UNVERIFIED (not built, not run)"`。
用例目录现存 **15 件**（01-frozen 3；job-00 11；`result.md`）——无 `02-conversion`、`03-self-review`、`evaluator_manifest.json`、`target*`。

### 冻结
`01-frozen/frozen-inputs.md`（8 行）：taskId `D2-241`、direction `python-to-cpp`、Kind NEW、casePath **写作 `docs/test/dataset-2/python-to-cpp/D2-241-python-base64.py`**（与实际路径不符）；sourceOs=targetOs=`linux` x64；源 sha256 `9E6854…D112`、**495 行**；评估计划 `POST /api/source-preflights` + source-only capsule + `build-and-run`，`argv=[]`、`stdin=null`；分类器 v2.4 钉 SHA；`contractHash=sha256:8090cfcc…`。
- 与 manifest：`Lines=495` ✅、`Sha256` ✅、`SourceFile` ✅、`JobId` 空 ✅（设计）、`Evidence` ✅（设计）。

### 分类
- 首轮（`events.jsonl:937`）`BLOCKED`/`public_network_unverified`，因 `zgp.org`（注释 L27）与 `docs.python.org`（docstring L81）**词法误判**。
- 重分类（`:938`）⇒ `classification-2.json`：`cls=REVIEW_NETWORK`、`ALLOWED`、`blockingReason=null`、`classifierVersion=2.4`、`classifierSha256=009a6f31…f3a4`、`requiresNetworkIsolation=true`、`inputManifestSha256=39dc13b0…82d8`。
- `classifier-input-2.json` 的 sha 与 manifest 大写一致 ✅；`this-task-classification.json` 与 `classification-2.json` 同值 ✅；`classification-1.json` 已删（目录内确实不存在；`old_cls/old_reason=null`）。

### 源侧预检（唯一 job）
`job-id.txt` = `eval-20261012-034133-5a01c9f5`（与 `events.jsonl:939`、`evaluation_report.json` 一致）。
`source_preflight_manifest.json`：`build-and-run`；`["python","-m","py_compile","base64.py"]` / `["python","base64.py"]`；linux/x64/python；timeout 60。
`input_profile.json`：`argv=[]`、`stdin=null`、维度 `["output"]`、stdout/stderr 均 `normalized-text`。
回传：build `completed/0`（66 ms，两流 0 B，digest `e3b0c442…`）；execution `completed/0`（33 ms，**两流均 0 B**）；`baselineAssessment=UNVERIFIED`；`cleanup=passed`；`jobStatus=COMPLETED`。
`closure.json`：`complete/cleanupConfirmed=true`、`issues=[]`、`cleanupRecords.source={passed, READY, attempts:1, contaminated:false}`、`roles.source={build:passed, execution:completed, frozenSourceObligations:UNVERIFIED}`（**工具截断**）。
`controller.log`：`03:41:33Z → 03:42:02Z`。

### 结果与去向
`result.md`：**`PREPARATION_GAP`**（冻结输入不足 ⇒ 源观察退化）；源 `main`(L558) 在无参数且 `args` 为空时走读 stdin；`argv=[]`+EOF ⇒ 无输出退出 0 ⇒ 按纪律 §10.1/§10.6 不产生行为结论 ⇒ 生成前停止、0 模型调用。
`items/D2-241.json` 与之一致（`usage 0`、`coverageGaps` 1 条）。
**矛盾**：`result.md` 称源 **“586 行”**，而 `frozen-inputs.md` 与 manifest 均 **495** ⇒ 同项内行数两说（源已删，不可复核）。
**与现行规则对照**：属 `LIB_UNOBSERVABLE_COMPILE_ONLY` 形态（[batch 记录 §六](harness-d-batch-records.md)）。

---

## D2-243 — python-to-cpp / GetUserSPNs.py

**身份**：manifest `…"GetUserSPNs.py","471",…"70C09A…CB0",…`。用例目录现存 **15 件**。

### 冻结 / 分类
`frozen-inputs.md`（8 行）：sha256 `70C09A…CB0`、**543 行**；Impacket `GetUserSPNs.py`、有入口 CLI；预判 `SOURCE_DEPENDENCY_GAP`。
- **`Lines` manifest 471 vs frozen 543 ⇒ 不一致**（源已删）。
`classification-1.json`：`cls=REVIEW_NETWORK`、`ALLOWED`/null、2.4、`inputManifestSha256=b74c531d…f47c`；signals network[466,469,472]、filesystem[360,392,399]、`network_mode=unresolved`。`classifier-input.json` 大写 sha ✅；`this-task-classification.json` 同值 ✅。**首轮 ALLOWED，无重分类**。

### 源侧预检
`eval-20261012-034321-248c6906`（`job-id.txt`＝`evaluation_report.json`＝`events.jsonl:942` ✅）。
回传：build `completed/0`（66 ms，两流 0 B）；execution `completed/**1**`（116 ms，stdout 0 B）；stderr（前缀可见）：
```
Traceback (most recent call last):
  File "/var/lib/codeconvert-agent/workspaces/eval-20261012-034321-248c6906/source/GetUserSPNs.py", line 40, in <module>
    from impacket import version
ModuleNotFoundError: No module named 'impacket'
```
（含 **job 特定绝对路径**；`evidence-source.json` 被工具截断于 digest 附近。）
`closure`：`complete/cleanupConfirmed=true`、`issues=[]`、`attempts=1`（截断）。`controller.log` `03:43:21Z → 03:43:50Z`。

### 结果
`result.md`：**`SOURCE_DEPENDENCY_GAP`**、0 模型调用；`items/D2-243.json` 一致（`executionExitCode=1`、diagnostics 同上）。

---

## D2-245 — python-to-cpp / html_parser.py

**身份**：manifest `…"html_parser.py","408",…"ED37C8…5017",…`。用例目录现存 **15 件**。

- `frozen-inputs.md`（9 行）：sha256 `ED37C8…5017`、**456 行**（manifest 408 ⇒ **不一致**）；`__all__=['HTMLParser']`、**无 `__main__`/`main`**；imports `re`、`_markupbase`、`html.unescape`；预判 `PREPARATION_GAP`；明示“**不补造入口**”。
- `classification-1.json`：`LOW_SIGNAL`、`no_known_signal_detected_not_proven_safe`、`ALLOWED`/null、2.4、`requiresNetworkIsolation=false`、signals 全空、`inputManifestSha256=afb8c672…efcd`；`this-task-classification.json` 同值。
- job `eval-20261012-034746-9518a96b`：build `completed/0`（66 ms，两流 0 B）；execution `completed/0`（32 ms，**两流 0 B**）；closure `complete/cleanupConfirmed=true`、`issues=[]`；log `03:47:46Z → 03:48:15Z`。
- `result.md`：**`PREPARATION_GAP`**（无入口库模块）、0 模型调用；`items/D2-245.json` 一致，`coverageGaps` 原文即提出“a per-item **LIB_UNOBSERVABLE_COMPILE_ONLY** justification is required”。

---

## D2-246 — python-to-cpp / json_encoder.py（15 件）

**身份**：manifest **L225** `"D2-246","NEW","python-to-cpp","Python","C++","json_encoder.py","394","数据集python\收集\json_encoder.py","","366A611E210EAB51067773E1012B692A9B5C90DC5695BEDBEB3A3FCCEC039E39","UNVERIFIED (not built, not run)"`。

- **冻结**（8 行）：sha256 `366A611E…E39`（大写，取自 manifest）、**443 行**（manifest 394 ⇒ **不一致**）；CPython `json.encoder` 副本、**无入口库模块**；预判 `PREPARATION_GAP`、**0 模型调用**、不补造入口；`build-and-run`、argv `[]`、stdin `null`。
- **分类（重分类）**：`classification-2.json`（71 行）：`cls=REVIEW_NETWORK`、`ALLOWED`/null、2.4、`009a6f31…f3a4`、`requiresNetworkIsolation=true`；`network_targets=[{json.org, L75, hostname, literal, redirectVerified=false}]`；`inputManifestSha256=a2bd9dbe…2a53`；`old_cls=null`/`old_reason=null`。
  - `result.md`(L22) 称首轮 `BLOCKED/public_network_unverified` 且“误生成的 `classification-1.json` 已删除”；`01-frozen/` 确无 `classification-1.json`；但 `old_cls/old_reason` 为 null ⇒ **旧判无从复核**（重分类只由 `-2` 序号 + result/README 文字自证）。
- `classifier-input-2.json`（1 行）大写 sha ✅；job 内 `this-task-classification.json`（69 行）与 `classification-2.json` **逐字段一致**。
- **job** `eval-20261012-034921-cc0dac83`：`build-and-run`；`py_compile`/`python json_encoder.py`；build `completed/0`（66 ms，两流 0 B）；execution `completed/**0**`（18 ms，**两流 0 B**）；`observations.output={status:observed, events:[], limitations:[]}`；`evaluation_report.json` 正常（`buildAssessment=passed`、`executionAssessment=completed`、`baselineAssessment=UNVERIFIED`、`cleanup=passed`、`failure=null`）；`closure.json`（工具截断）`complete/cleanupConfirmed=true`、`issues=[]`、`attempts=1`，grep 探针确认含 `"oracleStatus":"UNVERIFIED"`、`programOutputProvenance:"UNVERIFIED"`、`"checkedAt"`；`controller.log` `03:49:21Z → 03:49:50Z`。
- **⚠ 授权文件错项**：job-00 `batch-authorization.json` 的 `dataSource.confirmation` 写 “该项 **D2-197 (Go stdlib sort.go)** 无网络…”，与本项不符（模板复用未改净）。
- **缺过程件**：本项无 `controller-health-before/after.json`、无 `runners-before.json`（D2-247 job-00 齐备）。
- **结果**：`result.md`（34 行）**`PREPARATION_GAP`**、0 模型调用；`items/D2-246.json` 一致（`coverageGaps` 明列“合法中性入口或 `LIB_UNOBSERVABLE_COMPILE_ONLY` 举证”）。

---

## D2-247 — python-to-cpp / textwrap.py（53 件，**CONVERTED / matched**）

**身份**：manifest **L226** `"D2-247","NEW","python-to-cpp","Python","C++","textwrap.py","418",…,"CAD00069B2A25A585604D2FA774C288CF5ED70D4464AFAC16EDF821F3A4AFD5F","UNVERIFIED (not built, not run)"`。
目录构成：`01-frozen` 3 + `02-conversion` 9 + `03-self-review` 12 + `04-evaluation` 27（job-00 **14**：6 契约件 + `controller-health-before/after` + `runners-before` + returned-evidence 5；job-01 **13**）+ 根 2（`evaluator_manifest.json`、`result.md`）= **53**。

### 冻结 / 分类
- `frozen-inputs.md`（44 行）：sha256 `CAD00069…4AFD5F`、**491 行**（自注“manifest `Lines` 418 为旧口径”）；唯一 import `re`(L8)；**入口 L488 `if __name__=="__main__"` → L491 `print(dedent(...))`**；argv `[]`、stdin `null`；基线 stdout **33 B**、digest `sha256:b8cb8f102e7973c21ef001ce2df376711ad7f01c683c71afd3218c77fd0edc9b`；**冻结预判更正**：实测 `dedent` 公共前导空白为 0 ⇒ 次行保留 2 空格。
- `classification-1.json`（61 行）：`LOW_SIGNAL`、`ALLOWED`/null、2.4、`requiresNetworkIsolation=false`、signals 7 组全空、`network_mode=none-detected`、`inputManifestSha256=42a51d51…2f0b`；三份副本（01-frozen + job-00/01 的 this-task-classification）**逐字段一致**，`old_cls/old_reason=null` ⇒ **无重分类**。

### 生成 / 自修 / 自审
| 阶段 | 关键值 |
|---|---|
| 生成 | `request.system.txt`（10 行，7 条义务：单 ```cpp 块、`g++ -std=c++17 -o program target.cpp`、stdout 逐字节一致、**严禁硬编码**、仅 C++17、保持公开语义）；`request.user.md`（33 行，**知识注入声明**：`python.md` L1-PY-01/02/04、`cpp.md` L1-CPP-01..04、方向规则 PY-CPP-01/02/05/06；源以 `@SOURCE@` 占位）；`target.gen.model.json`：`deepseek-flash`、http 200、**`finish_reason=stop`**、usage `{prompt 6104, completion 34224, reasoning 27755, total 40328, cache_hit 5888, cache_miss 216}`、**`attempts=2`**（`attempt_note`：attempt 1 后台 curl 被会话重置杀死、本地 0 字节、**无响应留存**；attempt 2 前台重发 byte-identical 成功）、`truncated=false`；`knowledge_injected` 4 条（含“source textwrap.py full text (**491 lines**) embedded in the user message”）；产物 **`target.gen.cpp` 700 行** sha256 `651da617…920b` |
| 自审 1 | `self-review-1.json`（72 行）**`REPAIR-RECOMMENDED`、6 条**：`split-hyphen-return-offset`(major)、`wrap-condC-inverted`(major)、`indent-lacks-predicate`(minor)、`is-py-space-missing-x85`(minor)、`splitlines-missing-unicode-separators`(minor)、`wrap-fill-signature`(minor)；`self-review-1.model.json`：finish=stop、`truncated=false`、usage `{12064,42688,41270,54752}`；`decision`=**采纳 1–5，拒 6**（C++ 无 `**kwargs`，属语言层映射） |
| 自修 1 | `self-repair-1.model.json`：`SELF_REPAIRED` turn 1；finish=stop、usage `{7151,12182,5562,19333}`、attempts 1、`truncated=false`；产物 `target.self-repair-1.cpp` sha `7671abc5…6e3a`、**709 行**；appliedFixes 5 条含行号 |
| 自审 2 | `self-review-2.json`（28 行）**`REPAIR-RECOMMENDED`、2 条**：`ws-0x85-vs-utf8`(minor, `conversion-introduced`)、`expandtabs-tabsize-le0`(minor, **`origin=source-preexisting`**)。**⚠ 首次 attempt 截断**：`self-review-2.attempt-1-truncated.json` 保留原始 `chat.completion`（id `61587caf-…`、`model=deepseek-flash`、`content=""`），grep 探针确认 **`"finish_reason":"length"`**、**`"reasoning_tokens":65536`**；`self-review-3.model.json` 的 `note` 记此事并说明“以聚焦限长提示重发”。**⚠ 目录内独缺 `self-review-2.model.json`** ⇒ 该次成功调用的 `finish_reason`/usage/attempts **无本地记录**（元数据链断裂） |
| 自修 2 | `self-repair-2.model.json`：turn 2；finish=stop、usage `{7272,13284,6326,20556}`、attempts 1、`truncated=false`；`feedback_source` 写 “both items accepted as **conversion-introduced** with located evidence”（**与 self-review-2.json 第 2 条 `source-preexisting` 口径矛盾**）；产物 `target.self-repair-2.cpp` sha **`5fe6651e…b2ab`**、**748 行** |
| 自审 3 | `self-review-3.json`（5 行）**`NO-REPAIR-IDENTIFIED`、items=[]**；`reviewedScope` 逐项给目标行号（is_py_space_char L24-28、py_space_len_at L33-41 `C2 85`、rstrip_ws L86-90、is_blank L101-108、splitlines_keepends L374-403、expandtabs L142-159/L148），声明未重审 Unicode 空白全集；`self-review-3.model.json` finish=stop、`truncated=false` |

### 两个 job
- **job-00** `eval-20261012-035553-823264e4`：build `completed/0`(66 ms)；execution `completed/0`(36 ms)、**stdout 33 B** `"Hello there.\n  This is indented.\n"` digest `b8cb8f10…`、stderr 0 B；报告正常；`controller-health-before/after.json` 与 `runners-before.json` 齐备（3 个 runner 均 `READY`/`ready=true`/`contaminated=false`；`controller-health` 的 `contractSetHash=sha256:8090cfcc…`、`supportedEvaluationModes=["build-and-run","build-only"]`、`supportedJobKinds=["comparison","source-preflight"]`）；closure grep 探针确认含 `"oracleStatus":"UNVERIFIED"`、`programOutputProvenance:"UNVERIFIED"`、`"checkedAt"`；log `03:55:53Z → 03:56:26Z`。
- **job-01** `eval-20261012-042524-39e03f4a`：`comparison_manifest.json` target `["g++","-std=c++17","-o","program","target.cpp"]`/`["./program"]`；源 build `completed/0`(119 ms) / exec `completed/0`(36 ms)、stdout 33 B；目标 build `completed/0`(2088 ms) / exec `completed/0`(7 ms)、**stdout 33 B 同 digest**；`comparison.json` **`behaviorVerdict=matched`、`diffs=[]`**（output matched；其余四维 not-applicable）；`evaluation_report.json`（schema 3.0）：`runVerdict=runnable`、`codeVerdict=passed`、`behaviorVerdict=matched`、`environmentStatus=clean`、coverage `1/1/1/0/0`、`failure=null`；closure（工具截断）`complete/cleanupConfirmed=true`、两侧 attempts 1、`issues=[]`，探针含 `oracleStatus/programOutputProvenance = UNVERIFIED`；log `04:25:24Z → 04:26:33Z`。

### 结果与交付声明
`result.md`（42 行）：**`DONE` / 平台原判 `matched`**；最终交付 = **根级 `target.cpp` 748 行 sha256 `5fe6651e…b2ab`**；`evaluator_manifest.json`（47 行）：`languagePair python→cpp`、`sceneTags=[]`、`targetDir="."`、`files[0].relativePath="target.cpp"`、`hasReplayArtifact=true`、`replayArtifactPath=04-evaluation/job-01-dual-build/capsule.zip`、`batchReportPath="../../../README.md"`、`x_adapter{jobId=…39e03f4a, sourcePreflightJobId=…823264e4, syntaxVerdict=PASS, behaviorVerdict=matched}`。
- **实体缺失**：`**/*.cpp`、`**/*.py`、`**/source/**`、`**/target/**`、`**/capsule*`、`**/*.body.json`、`**/*.raw.json` **全部 0 命中**；`request.user.md`/`self-review-*.user.md` 的 `@SOURCE@`/`@TARGET@` **仍是占位符**。
- **路径口径不一**：`evaluator_manifest.json`=`target.cpp`（根级）/ `job-01/metadata.json`=`target/target.cpp` / `result.md`=“根级 `target.cpp`”。
- **`batchReportPath` 断链**：以 `targetDir="."` 解析得 `python-to-cpp/README.md`，**不存在**（实际批次报告在 `dataset-2-copy/batch/README.md`）。
- **失败 attempt 计**：成功模型调用 **6 次**（生成、自修 1、自修 2、自审 1、自审 3 + 自审 2 成功那次无 `.model.json`）；失败 attempt **2 次**（`target.gen` attempt 1 被会话重置杀死且**无响应留存**；`self-review-2` attempt 1 截断且**已保留**）——与 `batch/README.md` 的“6 次成功模型调用 + 2 次失败尝试”一致；但**事件流 `events.jsonl` 只记了截断那一次**，curl 被杀那次只见于 `target.gen.model.json` 的 `attempt_note`。
- **覆盖边界**：仅冻结 `argv=[]` 单路径（33 B stdout）；`TextWrapper/wrap/fill/shorten/indent` 其余行为未覆盖。

---

## 本组结论摘要

| taskId | 件数 | `Lines`(manifest vs frozen) | 分类 | job 数 | 去向 | 判定 |
|---|---|---|---|---|---|---|
| D2-241 | 15 | 495 vs 495（**result 写 586** ✗） | 重分类→REVIEW_NETWORK | 1 | PREPARATION_GAP | 0 模型调用 |
| D2-243 | 15 | 471 vs **543** ✗ | REVIEW_NETWORK（首轮） | 1 | SOURCE_DEPENDENCY_GAP | 0 模型调用 |
| D2-245 | 15 | 408 vs **456** ✗ | LOW_SIGNAL | 1 | PREPARATION_GAP | 0 模型调用 |
| D2-246 | 15 | 394 vs **443** ✗ | 重分类→REVIEW_NETWORK | 1 | PREPARATION_GAP | 0 模型调用 |
| D2-247 | 53 | 418 vs **491** ✗ | LOW_SIGNAL（首轮） | 2 | **CONVERTED** | **matched** |

- 5/5 无失败 job 提交、无 WAITING、无未确认清理（closure `complete/cleanupConfirmed=true`、`issues=[]`、`attempts=1`）。
- 工具截断：本组 8 个单行超长 JSON（241 的 closure/evidence-source；243 的 evidence-source/closure；245 的 evidence-source/closure；246 的 evidence-source/closure；247 的 4 份）只能读前缀；247 的 `self-review-2.attempt-1-truncated.json` 的 `reasoning_content` 正文亦被截断（其 `finish_reason`/`reasoning_tokens` 由 grep 探针确认）。
- **源码/目标/capsule/请求体全部不在工作区** ⇒ 行数与 sha256 只能核对“文本互洽”，不能独立复核。

---

## 补读（read 单行上限提高至 1048576 后，2026-10-12）

**本组原截断件 = 12 个单行超长 JSON + 1 个 attempt 件 + 3 个 health/runners 件，现已全部全文读到**：
`241/243/245/246` 各 `returned-evidence/{evidence-source.json, closure.json}`；`247 job-00` 同两件；`247 job-01` 的 `{evidence-source.json, evidence-target.json, comparison.json, evaluation_report.json, closure.json}`；`247` 的 `03-self-review/self-review-2.attempt-1-truncated.json`；`247 job-00` 的 `controller-health-before.json`、`controller-health-after.json`、`runners-before.json`。

**补读新增的原文事实（本组）**
1. **closure 尾段**（此前截在 `,"ora` 处）：四例源预检 job 与 247 job-00 均为 **`artifactDigests` 16 键**（`batch-authorization.json`、`classification.json`、`evaluation_report.json`、`evaluation_report.md`、`evidence/source-call|source-identity|source-request|source-response.body|source-response.json|source.json`、`input_profile.json`、`lifecycle.jsonl`、`metadata.json`、`request.json`、`source_preflight_manifest.json`、`staging-manifest.json`），尾三字段 `"oracleStatus":"UNVERIFIED"`、`"programOutputProvenance":"UNVERIFIED"`、`"checkedAt"`。
2. **247 job-01 closure = 23 键**：在 16 键基础上换成 comparison 形态——多 `comparison/result.json`、`comparison_manifest.json`、`evidence/target-call|target-identity|target-request|target-response.body|target-response.json|target.json`，**少** `source_preflight_manifest.json`；`roles` 多 `target:{build:"passed", execution:"completed", frozenSourceObligations:"NOT_APPLICABLE"}`。
3. **evidence-source.json 全结构**：`baselineReference{…, snapshot:"CC-Eval-Linux-8Lang-1.0.29", toolchainFingerprint:{}, collectorVersion:"1.0.0", agentVersion:"1.0.0"}`、`runtime{selectedRunner:"linux-vm-agent-x64", workspaceRef:"workspace/source"}`、`coverage.dimensions{output:"observed", 其余 "not-applicable"}`、`collectorDiagnostics:[]`；**`observations` 五维 `events` 全为 `[]`**，`registry`/`network` 的 `limitations` 恒为 `["evidence dimension is outside the current release scope"]`。⇒ 本项目在本地持有的**行为证据只有 output 维度的文本+digest，无事件级观察**。
4. **D2-243 完整 stderr**：`digest sha256:5d78a66d39a9d2a2bf492205a2d0b6f735908c048928ee353fd8a527fcdd59a6`、`sizeBytes 237`（此前不可读）。
5. **D2-247 `self-review-2.attempt-1-truncated.json` 全文**：`id=61587caf-30ea-4387-bd20-c7bb273d718e`、`object="chat.completion"`、`created=1791778165`、`model="deepseek-flash"`、`finish_reason="length"`、`content=""`、`usage{prompt_tokens 12242, completion_tokens 65536, total_tokens 77778, reasoning_tokens 65536, cached_tokens 256, prompt_cache_hit 256, prompt_cache_miss 11986}`、`system_fingerprint="aeb56401ca74e127821c4f9126dcb669"`。`reasoning_content` 为思维链，**不作审阅结论**（仅登记存在与元数据）。
6. **D2-247 job-00 health/runners 全文**：`contractSetHash=sha256:8090cfcc71697e552c93d4531fdce9dc17b92be41cb306fcbe081a4af3ec4aac`（= **各用例内 `batch-authorization.json` 的 contractHash**，而非根 `batch-authorization.json` 的 `a9ed1445…d82e`——为 F-4 提供了原文级依据）、`supportedEvaluationModes=["build-and-run","build-only"]`、`supportedJobKinds=["comparison","source-preflight"]`、`implementationIdentity{controller:"sha256:45ddcc75…7eca", evaluationCore:"sha256:96e4bf4d…7921", restartRequired:false}`、`runnerReadiness{executionReady:true, readyRunnerCount:3, blockedRunnerCount:0}`；`runners-before` 3 runner 均 `READY`/`ready=true`/`contaminated=false`/`lastFailureType=null`。
7. **新发现（补读才可见）**：`247 job-01-dual-build` **不存在** `controller-health-before.json`/`controller-health-after.json`/`runners-before.json`（`read` 报 not found）⇒ **同一用例两个 job 的过程件不对称**，此前只记“job-00 齐备”。

**未因此解除的不确定性（保持原判）**：F-1（241 的 495 vs 586 行三说）、F-6（`target.cpp`/capsule 无实体）、`@SOURCE@` 占位导致注入正文不可审、`request.body.json`/`target.gen.raw.json` 缺失——**均与 read 上限无关，仍属未决**。
