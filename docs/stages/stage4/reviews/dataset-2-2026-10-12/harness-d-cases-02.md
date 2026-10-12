# Harness D — 逐项审阅记录 02（python-to-csharp：D2-249 / 250 / 251 / 252 / 253 / 254）

> 逐件只读审阅（read/glob/grep）；单行超长 JSON 只能读 2000 字符前缀，逐处标“工具截断”。
> **重要口径更正**：`manifest.csv` 对 **NEW** 项按数据集设计就是 `JobId=""`、`Evidence="UNVERIFIED (not built, not run)"`（[README §3](../../README.md)：`JobId`=“REUSE 项的继承证据 job；**NEW 项为空**”；`Evidence`=“dual-build-PASS (inherited) 或 **UNVERIFIED (not built, not run)**”）。故“JobId 空/Evidence 未回填”**不是缺件**，而是**清单只描述数据集建库时状态、不是批次台账**这一事实。真正的不一致在 **`Lines` 列**（见下）。

---

## D2-249 — python-to-csharp / GetNPUsers.py（15 件）

- **冻结** `01-frozen/frozen-inputs.md`（37 行）：源 `source/GetNPUsers.py`、sha256 `985E70…41E0`（大写，取自 manifest）、**413 行**；`casePath` 写 `docs/test/dataset-2/...`（与实际目录不符）；预判 `SOURCE_DEPENDENCY_GAP`；`build-and-run`、argv `[]`、stdin null、timeout 60。
- **分类** `classification-1.json`（69 行）：`cls=REVIEW_NETWORK`、`ALLOWED`、`blockingReason=null`、`classifierVersion=2.4`、`classifierSha256=009a6f31…f3a4`、`requiresNetworkIsolation=false`；signals network[340]、filesystem[311,318]、`network_mode=unresolved`、`network_targets=[]`；`old_cls/old_reason=null`（首轮即 ALLOWED）。`classifier-input-1.json` sha 与 manifest 一致 ✅；job 内 `this-task-classification.json` 同值 ✅。
- **job** `eval-20261012-042806-0427a43e`（`job-id.txt`＝`events.jsonl:964`✅）：`build-and-run`；`py_compile GetNPUsers.py`/`python GetNPUsers.py`。
  - build `completed/exitCode 0`（66 ms，两流 0 B，`truncated=false`）；execution `completed/exitCode 1`（118 ms，stdout 0 B），stderr = impacket `ModuleNotFoundError`（L39）。
  - `closure.json`（**工具截断**）：`complete=true`、`cleanupConfirmed=true`、`issues=[]`、`attempts=1`、`runnerStateAfter=READY`、`roles.source={build:passed, execution:completed, frozenSourceObligations:UNVERIFIED}`；尾段 `"ora…` 未见。
  - `controller.log`：created `04:28:06.553307Z` → finished `04:28:37.319392Z`（两份都全）。
  - `evaluation_report.json`：`jobStatus=COMPLETED`、`jobPhase=FINISHED`、`buildAssessment=passed`、`executionAssessment=completed`、`baselineAssessment=UNVERIFIED`(`independent-frozen-oracle-not-provided`)、`cleanup=passed`、`failure=null`；`.md` 23 行，明示“source evidence only…no target build or equivalence claim”。
- **结果**：`result.md`（44 行）**DONE / `SOURCE_DEPENDENCY_GAP`**、0 模型调用、未生成 target；`items/D2-249.json` 一致。
- **manifest**：Id/Kind/Direction/SourceFile/Sha256 ✅；**`Lines=351` vs frozen/result 413 ✗**；JobId 空 / Evidence UNVERIFIED 属设计。
- **无 comparison.json / 无 `matched|semantic_pass|mismatched` / 无 diffs**（源侧预检型）。

## D2-250 — python-to-csharp / laZagne.py（15 件）

- **冻结**（36 行）：源 `source/laZagne.py`、sha256 `604ECA…CC4E`、**427 行**；内容实为 **PurpleArsenal/BrowserDump `chrome_extract.py`**（文件名与内容不符，`items` 的 `coverageGaps` 亦记此）；依赖 `Cryptodome`(L35) + 同项目 `lib.dpapi`(L38)/`lib.chromium`(L45)。
- **分类** `classification-1.json`（80 行）：`cls=REVIEW_SIDE_EFFECTS`、`ALLOWED`、null、2.4、`009a6f31…f3a4`；signals filesystem[147,344]、process[19,21,23,71,90,93,209,277,279,296,299,411]、`network_mode=none-detected`、`has_network=false`、`has_process_exec=true`；首轮 ALLOWED。
- **job** `eval-20261012-042940-6241af6c`（`events.jsonl:967`✅）：build `completed/0`（66 ms，两流 0 B）；execution `completed/**1**`（117 ms），stderr = `ModuleNotFoundError: No module named 'Cryptodome'`（L35）。
- **⚠ 报告缺件**：`evaluation_report.json` = `{"detail":"job_report_not_found"}`；`evaluation_report.md` = `{"detail":"job_human_report_not_found"}`；`controller.log` **只有 created `04:29:40.979216Z`，无 finished**。而 `closure.json` 仍 `complete=true`、`cleanupConfirmed=true`、`issues=[]`、`attempts=1`，且其 `artifactDigests` 列了 `evaluation_report.json`(`f93f47da…`)/`.md`(`6c520068…`) 的**正常摘要**。⇒ 同 job 内“报告未取回”与“closure 已闭合”并存。
- **结果**：`result.md`（44 行）**DONE / `SOURCE_DEPENDENCY_GAP`**、0 模型调用；`items/D2-250.json` 一致（并记 `file name laZagne.py but content is PurpleArsenal/BrowserDump chrome_extract.py`）。
- **manifest**：Sha256 ✅；**`Lines=381` vs 427 ✗**；JobId/Evidence 属设计。
- 全数据集范围内该类“占位报告”共 **16 份 md / 17 份 json**（grep `job_human_report_not_found` / `job_report_not_found` 实测），本区间涉及 **D2-250、255、257、264、274、275、277**。

## D2-251 — python-to-csharp / csv.py（15 件）

- **冻结**（33 行）：源 `source/csv.py`、sha256 `8486CB…F018`、**451 行**；CPython stdlib `Lib/csv.py` 副本、**无 `__main__`**；预判 `PREPARATION_GAP`（被实测改判为 `SOURCE_NOT_BUILDABLE`）。
- **分类** `classification-1.json`（65 行）：`cls=REVIEW_SIDE_EFFECTS`、`ALLOWED`、null、2.4、signals 仅 filesystem[337]、`network_mode=none-detected`。
- **job** `eval-20261012-043108-7989b469`（`events.jsonl:970`✅）：build `completed/0`（66 ms，两流 0 B）；execution `completed/**1**`（116 ms，stdout 0 B），stderr = `ImportError: cannot import name '__version__' from '_csv' (unknown location)`（L8；`result.md` 记 stderr 350 B）。
- `closure.json`（**工具截断**）：`complete/cleanupConfirmed=true`、`issues=[]`、`attempts=1`。
- `controller.log`：created `04:31:08.602488Z` → finished `04:31:39.087686Z`；`evaluation_report.json` 正常（`passed/completed/UNVERIFIED/passed/null`），`.md` 23 行正常。
- **结果**：`result.md`（46 行）**DONE / `SOURCE_NOT_BUILDABLE`**、0 模型调用；理由 = 源 L8 `from _csv import __version__` 与 runner 的 `_csv` C 扩展**接口不匹配**。
- **口径张力（记录，不改判）**：本项 `SOURCE_NOT_BUILDABLE`，而其 job 的 `buildStatus=completed`、`exitCode=0`、`buildAssessment=passed`——失败发生在 **import 运行期**。`optimization-inputs-2.md §2.2.2` 把它与 D2-119 并列为“源缺陷/接口不符”一类。
- **manifest**：**`Lines=380` vs 451 ✗**。

## D2-252 — python-to-csharp / json_decoder.py（15 件）

- **冻结**（33 行）：源 `source/json_decoder.py`、sha256 `B719FB…4F80`、**356 行**；CPython `Lib/json/decoder.py` 副本、无 `__main__`。
- **分类（重分类）**：`events.jsonl:972` 首轮 `BLOCKED`/`public_network_unverified`（`json.org` docstring L255 词法误判）；`:973` 加 `--network-isolation-configured` ⇒ `classification-2.json`（71 行）`cls=REVIEW_NETWORK`、`ALLOWED`、null、2.4、`requiresNetworkIsolation=true`；`network_targets=[{json.org, L255, hostname, literal, redirectVerified=false}]`；**signals 六类全空**。
- **磁盘核对**：`01-frozen/` 只剩 `classification-2.json` + `classifier-input-2.json`，**`classification-1.json` 与 `classifier-input-1.json` 均已删**（事件只写 “classification-1.json removed”，**未提 classifier-input-1.json**）。
- **旧值未留痕**：`classification-2.json` 的 `old_cls` / `old_reason` **仍为 null**，`classifier-input-2.json` 也未记录隔离开关 ⇒ 重分类的“旧值”在产物内无留存。
- **job** `eval-20261012-043239-f7868264`（`events.jsonl:974`✅）：build `completed/0`（66 ms，两流 0 B）；execution `completed/**0**`（33 ms，**stdout/stderr 均 0 B，`truncated=false`**）；`observations.output={status:observed, events:[], limitations:[]}`。
- `closure.json`（**工具截断**）：`complete/cleanupConfirmed=true`、`issues=[]`、`attempts=1`。`controller.log` created `04:32:39.573678Z` → finished `04:33:09.534606Z`；报告两件正常。
- **结果**：`result.md`（36 行）**DONE / `PREPARATION_GAP`**、0 模型调用；`items/D2-252.json` 的 `coverageGaps` 明确提出 “a legitimate-source neutral entrypoint (**or a per-item `LIB_UNOBSERVABLE_COMPILE_ONLY` justification**) is required”。
- **manifest**：**`Lines=312` vs 356 ✗**。
- **字段张力**：`job/batch-authorization.json` 的 `dataSource.confirmation` 写“**无网络**、无凭证”，而分类判 `has_network=true`/`requiresNetworkIsolation=true`。

## D2-253 — python-to-csharp / atexec.py（15 件）

- **冻结**（31 行）：源 `source/atexec.py`、sha256 `0FEAFF…2F3C`、**339 行**；Impacket atexec（via TSCH）、有入口 L260；依赖 `impacket.*`(L32-39)+`six`(L40)。
- **分类（重分类）**：`events.jsonl:976` 首轮 `BLOCKED`/`public_network_unverified`（`docs.python.org` argparse help L90/L282 + `schemas.microsoft.com` XML xmlns L143）；`:977` 重分类 ⇒ `classification-2.json`（97 行）`cls=REVIEW_SENSITIVE`、`ALLOWED`、null、2.4、`requiresNetworkIsolation=true`、`requiresSyntheticData=true`；signals network[116,118]、process[125,267,269]、dynamic_code[178,181]、**sensitive 为空**；`old_cls/old_reason=null`；`classification-1.json`/`classifier-input-1.json` 均已删。
- **job** `eval-20261012-043403-4b101636`（`events.jsonl:978`✅）：build `completed/0`（66 ms）；execution `completed/**1**`（117 ms），stderr = `ModuleNotFoundError: No module named 'impacket'`（L32）。
- `closure.json`（**工具截断**）：`complete/cleanupConfirmed=true`、`issues=[]`、`attempts=1`；`controller.log` created `04:34:03.413635Z` → finished `04:34:33.170124Z`；报告两件正常。
- **结果**：`result.md`（43 行）**DONE / `SOURCE_DEPENDENCY_GAP`**、0 模型调用；`items/D2-253.json` 一致。
- **manifest**：**`Lines=296` vs 339 ✗**。

## D2-254 — python-to-csharp / shlex.py（**64 件**，唯一进入转换的本组项）

### 目录构成
`01-frozen` 3 件 + `02-conversion` 9 件 + `03-self-review` 12 件 + `04-evaluation` 38 件（job-00 12 / job-01 13 / job-02 13）+ batch 根 2 件（`evaluator_manifest.json`、`result.md`）= **64**（两次 glob 一致，无 spill）。

### 冻结 / 分类
- `frozen-inputs.md`（34 行）：源 `source/shlex.py`、sha256 `78CF96…0683`、**345 行**，并**明确写 “manifest `Lines` 列 320 为旧口径”**；CPython stdlib `Lib/shlex.py` 副本、有入口 L339；冻结 **argv `[]` + stdin `foo 'bar baz' qux\n`**（理由：空 stdin 会观察退化，引 D2-241 教训）；目标 `target.cs`（dotnet net8.0）。
- 分类：`classification-1.json`（66 行）`cls=REVIEW_SIDE_EFFECTS`、`ALLOWED`、null、2.4、`009a6f31…f3a4`、`requiresNetworkIsolation=false`；signals filesystem[286,344]；`old_cls/old_reason=null`。**四份副本（01-frozen + job-00/01/02 的 this-task-classification）逐字段完全一致，无重分类**；job-02 metadata 明示 “No source/target source-tree change => no re-classification required”。

### 生成 / 自修 / 自审（全部有 model.json 与请求正文）
| 阶段 | 文件 | 关键值 |
|---|---|---|
| 生成 | `request.system.txt`（9 行）+`request.user.md`（40 行）+`target.gen.model.json`（35 行） | system 规定：只输出一个 ```csharp 块、目标名 `target.cs`、`dotnet build -c Release`(net8.0)、运行 `dotnet bin/Release/net8.0/probe.dll`、**stdout 逐字节一致**、严禁硬编码、不新增网络/文件/进程能力；user 正文含冻结契约、源侧实测基线（stdout 3 行 **45 B**，digest `sha256:4e43f68e4bf29b92a7e26698cf23348a8ccf9a5a31234ac8f9dbebe5d7be7b0e`）、**适用知识条目清单**（python.md L1-PY-01/02/04；csharp.md L1-CS-01..04+输出换行；python-to-csharp/SKILL.md PY-CS-01..06）、`# 源（shlex.py，完整，共 345 行）`+`@SOURCE@`。model.json：`model_requested=deepseek-flash`、temp 0.2、`max_tokens_sent=false`、endpoint `https://api.deepseek.com/chat/completions`、**`knowledge_injected`(4 条)**、http 200、`model_actual=deepseek-flash`、**`finish_reason=stop`**、usage `{prompt 4455, completion 26232, reasoning 22308, total 30687}`、attempts 1、`truncated=false`；产物 `target.gen.cs` sha256 `e65a4020…e63d`、**595 行** |
| 自审 1 | `self-review-1.{system.txt,user.md,model.json,json}` | verdict **REPAIR-RECOMMENDED**，**3 条**：`PB-01`[major] pushback 顺序（**误判**：要求把 Stack 改 `Queue`）、`EX-01`[minor] 异常类型、`API-01`[minor] 便利入口；`reviewedScope` 明写“静态通读、未编译未运行”；response finish=stop、`truncated=false`、usage `{7628,13282,12714,20910}` |
| 自修 1 | `self-repair-1.*`（4 件） | 3 项全落地 ⇒ `target.self-repair-1.cs` sha256 `3f74cd7a…15fb`、**601 行**；model.json 的 `appliedFixes[0]` **自注 “(SUBSEQUENTLY REVERTED in turn 2 — the round-1 FIFO judgement was wrong)”**；finish=stop、usage `{4463,9233,5249,13696}` |
| 自审 2 | `self-review-2.*` | verdict **REPAIR-RECOMMENDED**，**1 条**（回退）：引源 **L48 `deque()`、L76 `appendleft`、L104 `popleft` ⇒ LIFO**；`decision` 原文 “accept: the round-1 'source is FIFO' judgement was wrong…Revert pushback to LIFO.”；finish=stop、`truncated=false` |
| 自修 2 | `self-repair-2.*` | 恢复 `Stack<string>` ⇒ `target.self-repair-2.cs` sha256 `f916178a…4db11`、**601 行**；finish=stop、usage `{4535,4118,134,8653}` |
| 自审 3 | `self-review-3.*` | verdict **NO-REPAIR-IDENTIFIED**，**items=[]**；`reviewedScope` 记“回退已正确落地（push_token `Stack.Push`~L117 / get_token `Stack.Pop`~L140，与源 L76→L104 同为 LIFO）…未编译运行”；finish=stop |

采纳/拒绝小结：自审 1 三条**全采纳**（其中 1 条后被推翻）；自审 2 一条采纳（回退）；自审 3 零条；**无“拒绝”条目**，3 条 origin 全为 `conversion-introduced`。

### 三个 job
| job | job-id | 内容 | 结果 |
|---|---|---|---|
| `job-00-source-buildability` | `eval-20261012-043520-4747ca62` | `source_preflight_manifest.json`：`build-and-run`、`["python","-m","py_compile","shlex.py"]`/`["python","shlex.py"]`；`input_profile.json` argv `[]`、stdin 非空；build `completed/0`(67ms, 两流 0B)；execution `completed/0`(16ms)、stdout **45 B** digest `4e43f68e…`；`evaluation_report.json` 正常 | 源侧基线有效 |
| `job-01-dual-build` | `eval-20261012-044255-50f0362b` | `comparison_manifest.json`：source python `py_compile`/`python shlex.py`；target csharp `dotnet build -c Release`/`dotnet bin/Release/net8.0/probe.dll`；`evidence-source.json` execution `completed/0`、stdout 45 B 同 digest；`evidence-target.json` build `completed/0`(19541ms, stdout 343 B 含 “Build succeeded. 0 Warning(s) 0 Error(s)”)，build stderr 含 “Welcome to .NET 10.0! SDK Version: 10.0.112”；`comparison.json` **behaviorVerdict=`mismatched`、diffs=3**：①`execution.exitCode` 0→**150**（critical, `exact-exit-code`）②源 stdout 3 行→目标**空** ③源空→目标 “You must install or update .NET to run this application…”；`evaluation_report.*`：**Conversion result FAIL / Behavior MISMATCHED / Environment CLEAN**、codeVerdict `failed`、runVerdict `partial-runnable`；`closure.json` complete/cleanupConfirmed true、两侧 attempts 1、issues [] | **环境失败**（runner 无 .NET 8 runtime） |
| `job-02-rollforward` | `eval-20261012-044456-e91a4c2f` | `metadata.json` 明示＝重提 job-01，**唯一变更** `probe.csproj` 加 `<RollForward>LatestMajor</RollForward>`；归因 “target build completed/0 但 exec exit 150，因 runner 有 .NET SDK 10.0.112 且无 .NET 8 runtime…**environment/toolchain cause, NOT a conversion defect; the target source is identical**”；`evidence-target.json` build `completed/0`(14447ms, stdout 342 B)；`comparison.json` **behaviorVerdict=`matched`、diffs=[]**；`evaluation_report.*`：**PASS / MATCHED / CLEAN**、codeVerdict `passed`、runVerdict `runnable`；`closure.json` complete/cleanupConfirmed true、两侧 attempts 1 | **通过** |

### 交付件声明与实体
- `evaluator_manifest.json`（49 行）：`languagePair python→csharp`；`files[0]` 声明 `relativePath=target.cs`、`sourcePath=../../source/shlex.py`、`replayArtifactPath=04-evaluation/job-02-rollforward/capsule.zip`、`artifacts={hasSource:true, hasTranslatedCode:true, hasEvaluationNotes:false, hasReplayArtifact:true}`、`success:true`；`x_adapter`：`jobId=…e91a4c2f`、`priorJobId=…50f0362b`、`sourcePreflightJobId=…4747ca62`、`syntaxVerdict=PASS`、`behaviorVerdict=matched`、`unexecuted=[]`、`preconditions=[]`。
- `result.md`（46 行）：`DONE / matched`；根级 `target.cs`（601 行，sha256 `f916178a…4db11`）+ `probe.csproj`（net8.0、AssemblyName=probe、RollForward=LatestMajor）；无驱动（两侧原生入口）。
- **实体核对**：用例目录下 **无任何 `.cs`/`.py`/`.csproj`/`.zip`**（多次 glob 0 命中）⇒ `target.cs`、`source/shlex.py`、`probe.csproj`、`capsule.zip` **均无实体**，`hasSource/hasTranslatedCode/hasReplayArtifact=true` 与 `success=true` **无本地实体支撑**（属“已删/未落盘”与“声明-文件不一致”两类，分别登记）。

### manifest 核对
`manifest.csv` 第 232 行：Id/Kind/Direction/SourceFile/Sha256 ✅；**`Lines=320` vs frozen/result 345 ✗**（frozen 自称 320 为旧口径）；JobId 空 / Evidence UNVERIFIED 属设计；`Origin=数据集python\执行\shlex.py` 与 `casePath=docs/test/dataset-2/...` 及实际目录三者互不相同。

### 覆盖边界
两侧 stdout 45 B 逐字节相同、diffs=0，但**仅覆盖冻结单输入**；`posix=True`、`punctuation_chars`、文件参数、sourcehook 等路径未覆盖（`self-review-1.json` 的 `reviewedScope` 明列）。

---

## 本组共性结论

- **六个 job（249–253 各 1 个 + 254 的 3 个）全部留存回执**；`closure` 6/6 为 `complete=true`、`cleanupConfirmed=true`、`issues=[]`、`attempts=1`、`contaminated=false`、`runnerStateAfter=READY`。
- **无失败 attempt**（`attempts` 全 1）；**无 WAITING**；`events.jsonl:964–990` 与 `items/D2-249..254.json` 逐项一致。
- **无“未知提交去向”**：254 的三 job 由 `evaluator_manifest.json.x_adapter` 的 `sourcePreflightJobId/priorJobId/jobId` 串成一条完整链。
- **工具截断**：`evidence-source.json`（5×）+ `closure.json`（5×）+ 254 的 `evidence-target.json`/`closure.json` 等单行 >2000 字符；target execution 的 exitCode 150/0 分别由 `comparison.json` 的 diff 与 `matched` 判定交叉佐证（未凭截断内容臆测）。
- **manifest `Lines` 6/6 与 frozen/result 不一致**（差值 +62/+46/+71/+44/+43；254 为 320 vs 345）。
- **`Lines` 无法复核**：六例源件均不在工作区（源/目标已删）。

---

## 补读（read 单行上限提高至 1048576 后，2026-10-12）

**本组原截断件（22 件）已全部全文读到**：`249/250/251/252/253` 各 `returned-evidence/{evidence-source.json, closure.json}`（10）；`254 job-00` 同两件；`254 job-01` 与 `job-02` 各 `{evidence-source.json, evidence-target.json, comparison.json, evaluation_report.json, closure.json}`（10）。

**补读新增的原文事实（本组）**
1. **closure 尾段**：五个源预检 job 均 **16 键**、尾三字段 `oracleStatus/programOutputProvenance="UNVERIFIED"`、`checkedAt`；`254 job-01/job-02` 均 **23 键**，`roles` 多 `target{…frozenSourceObligations:"NOT_APPLICABLE"}`。
2. **此前不可读的 stderr digest/size 全部取得**：D2-249 `sha256:b2af1858ad9744ebf5fb8a3b34ce2f51438b9d563309c7105c7c945f74c1458d`/236 B（impacket L39）；D2-250 `sha256:a2828a6dc3bab135856ad6cf90d934565909dcdcdb85b9bd00709fb1e50e630b`/240 B（`Cryptodome` L35）；D2-251 `sha256:435851a32c0119997d4975a6c1997f48a32654b7b062aad99d70e5c507fc22f2`/350 B（`cannot import name '__version__' from '_csv'` L8）；D2-253 `sha256:ad1360ba85182d1dd1d5dc211a5b76a01225cc8004d6ca88ee60e1a3c07ecd71`/240 B（impacket L32）。
3. **D2-254 job-01 目标侧全文**：build stdout 343 B 含 “Build succeeded. 0 Warning(s) 0 Error(s)”；build stderr **670 B** 含 “Welcome to .NET 10.0! / SDK Version: 10.0.112” 与 `aka.ms`/`github.com` 提示；execution exit **150**、stdout 0 B，stderr **606 B** 全文（`Framework: 'Microsoft.NETCore.App', version '8.0.0'`；`The following frameworks were found: 10.0.12`；`rid=ubuntu.26.04-x64`）⇒ 「缺 .NET 8 运行时」为环境归因，**原文可见**。
4. **`comparison.json` 的 `diffs` 全文（job-01）**：3 条——`execution.exitCode` 0→150（critical，`exact-exit-code`）、`stream.normalizedText` 源 3 行→目标空、目标 err 文本。**其 `targetValueSummary` 被截成 `"…App: /var/lib/codeconv"`（≈120 字符）——这是平台服务器端的摘要截断**，与本机 read 上限无关（单列）。
5. **D2-254 job-02 全文**：两侧 build `completed/0`（源 67 ms / 目标 14 447 ms）、两侧 execution `completed/0`（源 34 ms / 目标 35 ms）、**两侧 stdout 45 B、同一 digest `sha256:4e43f68e4bf29b92a7e26698cf23348a8ccf9a5a31234ac8f9dbebe5d7be7b0e`**、`comparison.json` `behaviorVerdict="matched"`、`diffs=[]`、coverage 1/1、`failure=null`；closure 23 键。
6. `evidence-source.json` 结构与 cases-01 补读第 3 条同型（`observations.*.events` 全空、`toolchainFingerprint {}`、`truncated=false`）。

**未解除**：`Lines` 6/6 不一致；254 的 `target.cs`/`probe.csproj`/`capsule.zip` 无实体；250 的报告占位与 `closure.complete=true` 并存——**均不因补读而改变**。
