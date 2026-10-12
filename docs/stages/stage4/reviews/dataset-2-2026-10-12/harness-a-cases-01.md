# harness-A 逐项记录 01（D2-007 … D2-026 区段）

> 覆盖：本文件登记 D2-007 … D2-026 区段（20 个编号，其中 D2-026 已移除）。逐项文件清单与全局读取状态另见 [harness-a-coverage.md](harness-a-coverage.md)；跨项发现与知识/优化汇总见 [harness-a-findings.md](harness-a-findings.md)。
> 读取状态记号：`read` 正文已读；`read(截断>2000)` 单行件超工具上限、尾部无法补读；`empty` 0 字节；`dir-empty` 目录存在但 0 文件；`missing` 预期件不在。未写到的项以 coverage 的 Read 列为准（本文件随分组追加）。

## D2-007 / cpp-to-csharp / dir_sample_discovery（REUSE）

- 实际目录：`../../cpp-to-csharp/handoff-2026-10-02-d08-dir-sample-discovery-cpp/`。目录存在，共 **45 件**，全部读取；其中 6 件单行 JSON 超 2000 字符截断（`job-00/returned-evidence/{evidence-source,evaluation_report,report-retry1}.json`、`job-00c/returned-evidence/{evidence-source,closure}.json`、`job-00b-source-preflight/returned-evidence/evidence-source.json`）。`02-conversion/`、`03-self-review/` **目录存在但为空**（0 文件）；`source/`、`job-01-dual-build`、`result.md`、`evaluator_manifest.json` **缺失**。
- 冻结/分类：`01-frozen/frozen-inputs.md` 记 source `dir_sample_discovery.cpp`（743B、25 行，manifest 记 19 行——**行数不一致**）、C++17→C#12/.NET8、sourceOs windows（候选、非编译器鉴别）、model `deepseek-flash` temp0.2 RAG off、三份 selected skills（方向 cpp-to-csharp、系统 posix-windows-filesystem、场景 file-io）、driver=一次性自然退出 argv[] stdin null、`subprocess.run(timeout=60)`、oracle 需 output、stdoutMode `json-structural`/stderrMode `exact`、上限语义 push_back 后 `size()>=10` break、枚举顺序未定义为义务。`classification-1.json`（v2.3）与 `classification-2.json`（v2.4）均 `REVIEW_SIDE_EFFECTS`/`ALLOWED`/`blockingReason=null`，同 `inputManifestSha256`、`classifierSha256` 不同（2.3 `441b4d50…`、2.4 `009a6f31…`）；各 job 内 `this-task-classification.json` 为 v2.4 副本。metadata.json 仍写 `classifier-2.3` 与 item json 用 2.3——**分类版本记录不一致**。
- 源侧预检（4 个 job）：
  - `job-00-source-buildability`（`eval-20261010-041257-43cc8366`）：源 build `completed/0`（`g++ -std=c++17 … -o program.exe`，2397ms，空 stdout/stderr），源 execution `completed/0`（201ms），stdout `{"case":"discovery","sample_count":3,"items":["dir_sample_discovery.cpp","program.exe","run_case.py"]}`；target preflight **SKIPPED**（从未尝试）、无 target 证据；job `INFRA_ERROR`/runVerdict blocked，failure `AGENT_UNAVAILABLE`/environment，原因 `…invalid codeconvert-evidence-bundle at $.collectorDiagnostics.0 …('detail' was unexpected)`；`comparison.json` = `{"detail":"comparison_not_found"}`；源 preflight/cleanup PASSED、target cleanup SKIPPED、contaminated false、READY。同目录 `job-id-retry1.txt`（`eval-20261010-041421-c44a0da4`）与 `report-retry1.json` 记同 capsule 重提**逐字复现**同一 INFRA_ERROR。
  - `job-00b-toolchain-probe`（`eval-20261010-041537-2ce9feed`）：对照探针，manifest target `artifactLanguage=c`、`gcc -std=c11`；metadata 明示 “CONTROL PROBE… Not a conversion task”、targetHash `sha256:probe`。**无 returned-evidence** ⇒ “COMPLETED 且双侧执行”只有 attribution.md/PLATFORM_BLOCKER.md/batch 叙事，**本副本不可独立证实**。
  - `job-00b-source-preflight`（`eval-20261012-061720-7d77385a`）：source-only `source_preflight_manifest.json`（build argv `g++…`、runCommand `.\program.exe`、timeout 60）；build `completed/0`（5064ms），execution **launch-failed**、exitCode null、stderr `[WinError 2] 系统找不到指定的文件。`（46B）；`evaluation_report.json` = `job_report_not_found`、`.md` = `job_human_report_not_found`、`closure.json` = `closure_not_found`、controller.log 仅 “created”一行 ⇒ **清理未确认**。装置/路径缺陷。
  - `job-00c-source-preflight`（`eval-20261012-061842-037c6549`）：同 manifest；build `completed/0`（3010ms）、execution `completed/0`（199ms）、stdout `{"case":"discovery","sample_count":2,"items":["dir_sample_discovery.cpp","program.exe"]}`（90B）、snapshot `1.0.29`；`evaluation_report.json` COMPLETED、`buildAssessment=passed`、`executionAssessment=completed`、`baselineAssessment=UNVERIFIED`（reason `independent-frozen-oracle-not-provided`）、cleanup passed；`closure.json` `complete=true/cleanupConfirmed=true/issues=[]`、源 cleanup passed/READY/contaminated false。**清理已确认（仅源角色）**。
- 请求/响应：**无**任何 `request*.txt`/`*.model.json`（02-conversion 空）；无法核模型身份/finish_reason/用量/正文。`self-review`：**无**。`result.md`/`evaluator_manifest.json`：**缺失**。
- 关键异常：① 同项 `caseId` 漂移（job-00 用 `batch-d2-007-cpp-to-csharp-dir-sample-discovery`，job-00b/c 用 `D2-007`）；② snapshot 漂移 1.0.26→1.0.28→1.0.29；③ timeout 漂移（frozen 60 / job-00 profile 30 / job-00b/c 60）；④ runCommand 漂移（job-00 `python run_case.py` vs 重开 `.\program.exe`；且重开 metadata 明示 “Source tree = … only (no driver)”）；⑤ item json **未更新**（仍 EVALUATION_BLOCKED，未记 job-00b/00c）；⑥ `environment` 字段值被截断成 `"INFRA_ERROR (agent/AST"`；⑦ closure 列出 9 个本副本不存在的 artifact digest（`evidence/source-call.json`、`source-response.body`、`request.json`、`lifecycle.jsonl`、`staging-manifest.json`、`classification.json` 等）⇒ 保留/覆盖缺口；⑧ 未确认清理的 job-00b-source-preflight 未登记于 item/events。
- 原件支持的独立事实：源在 windows/x64 两次真实构建并运行成功（job-00 `sample_count:3`、job-00c `sample_count:2`）；两次输出差异源于 cwd 工作区条目不同（job-00 含驱动 `run_case.py`）——**观察面不对称**，先于任何转换；job-00b 真实 launch-failed（装置，非源缺陷）；两次 csharp 提交被平台在证据封装校验处拒绝（target preflight SKIPPED、coverage 0）；2026-10-11 探针 `eval-20261011-122249-fe456bbe` 返回 COMPLETED、target build/exec `completed/0`、`behaviorVerdict=mismatched`，唯一 major diff `stream.normalizedText` 源 104B vs 目标 103B。源侧义务从未独立认证（job-00c `baselineAssessment=UNVERIFIED`）。
- 归因：csharp 封装拒绝=环境/平台；launch-failed=装置；cwd 依赖观察=装置/设计；104 vs 103 字节差异=**未定**（源/目标已删，且枚举顺序未定义）；转换引入缺陷：**无法判定**（无 target、无自审、无 job-01）。记录不一致=流程。
- 知识候选（当前契约对照）：① 源预检 `runCommand` 须用显式相对路径 `.\program.exe`（裸 `program.exe` 得 `[WinError 2]`）——批次已记，框架契约是否已写**未核**；② 观察面不得含构建产物/exe/cwd 清单，cwd 枚举型须用共享中性 fixture；③ C# 目标 `artifactLanguage` 必须 `csharp`（写 `dotnet` 得 403），已见 blocker/probe 文本；④ 重开后须刷新 item 索引（现仍 stale）；⑤ 对照探针引用其 COMPLETED 前须先保留 returned-evidence。**无自审正文可引，故无错误自审建议可评**。
- 优化：单行 JSON 另存可读副本；保留对照探针返回证据并按实际用途命名目录；同项统一 caseId/snapshot/timeout/runCommand；REOPEN/重试失败写入 item；02/03 目录若有意清空须在记录中标注。
- 未知：6 件截断尾部；已删源码/驱动/目标/请求/响应/自审正文；探针是否真 COMPLETED；job-00b-source-preflight 是否他处有报告；manifest 继承 JobId 的证据是否存在于副本外。

## D2-008 / D2-009 / D2-010 / D2-011 / D2-012 / cpp-to-csharp（REUSE）——目录存在但 0 文件

- 五个实际目录均**存在但 0 文件**（`dir-empty`）：`handoff-2026-10-02-d08-elevation-branch-report-cpp`、`-fake-cred-summary-cpp`、`-manifest-upload-cpp`、`-startup-marker-write-cpp`、`-xor-decode-demo-cpp`。无 `source/`、无 `output/`；`**/*` glob 0 命中。
- 每项仅存：`../items/D2-0NN.json`、manifest.csv 对应行、`../events.jsonl` 两条（DEFERRED `BLOCKED_ENV`/0 model calls + TERMINAL `WAITING`，日期 2026-10-11）。item 记 `disposition=FROZEN`、`phase=NOT_STARTED`、`lifecycle=WAITING`、`blockingReasons=["BLOCKED_ENV"]`、`blockerRef=../../batch/platform-blocker-csharp-target.md`、`dispositionNote` 明示 “no freeze job was run… 0 model calls”；manifest 声明 `dual-build-PASS (inherited)` 与继承 JobId（D2-008 `eval-20261005-140505-ab82d384`、D2-009 `…141822-14580e05`、D2-010 `…142450-bdc91e2f`、D2-011 `…140747-363b7c8b`、D2-012 `…140948-fc76880b`），**均无对应证据件**。
- 冻结/分类/预检/请求/自审/Job/result/manifest：**全部不存在**（不是 metadata-only，而是零件）。
- 关键异常：① `disposition=FROZEN` 却无 `frozen-inputs.md`（当前契约 [任务状态 §3/§2.2](../../../../references/framework/task-state-contract.md) 定义 FROZEN 以落盘回读为前提；属**记录缺口**，非缺规则）；② 自身 `blockerRef` 文件头部已声明 2026-10-11 修复且恢复条件满足，item 仍 `WAITING/BLOCKED_ENV`（**stale**）；③ 声明源 SHA/行数但无源文件可核；④ `casePath` 指向 `docs/test/dataset-2/...`，在副本内不解析；⑤ 无 `result.md`（当前契约对生成前阻断/非可转换去向仍要求报告）；⑥ 分类版本/批次计数快照不一致（blocker 文件称 38 项，summary 称 14 项，optimization-inputs-2/events 称 20 项——**历史快照差异**，引用须带日期与口径字段）。
- 原件支持的事实：仅 manifest 行、item 索引、两条事件；**无任何构建/运行/比较事实**。继承 PASS 为**跨副本声明**，本副本不可核。
- 归因：缺件=装置/副本级（按用户裁决跳过）；BLOCKED_ENV=环境/平台；FROZEN 无冻结件=记录；源事实=未定；无转换引入可判。
- 知识候选（当前已覆盖）：stale WAITING 重开、FROZEN 定义与落盘门禁、去向变化追加记录——均已有现行契约；缺的是**逐项 REOPEN_ELIGIBLE 事件**与冻结件标志，属流程/记录落实，不新增规则。
- 优化：coverage 词汇区分 “目录存在 0 文件” 与 “目录缺失”；item 加 `freeze.artifact=none` 或仅在 `frozen-inputs.md` 存在时记 FROZEN；分别出 disposition 与 blockingReasons 直方图；阻塞消除时逐项发 REOPEN 事件；REUSE 项存继承证据指针。
- 未知：源字节是否与声明 SHA 相符（源根不在副本）；继承 JobId 是否真 dual-build PASS；空目录是否曾有件；2026-10-11 修复在**当前**平台版本是否仍成立（历史观察不证当前）；重开时点。

## D2-013 … D2-025（本区段其余项）

> 待逐项读者回报后追加（见 [harness-a-coverage.md](harness-a-coverage.md) 的 Read 列）。

## D2-026

- **已移除**（[README §5.2](../../../README.md)：无可取源文件），不在 manifest；不审、不补编号。
