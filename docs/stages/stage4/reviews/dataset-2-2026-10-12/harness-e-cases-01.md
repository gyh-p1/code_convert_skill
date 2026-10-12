# harness-E 逐项记录 01（D2-278 … D2-287）

> 状态：**COMPLETE**。范围见[覆盖索引](harness-e-coverage.md)；汇总判读见[发现](harness-e-findings.md)。D2-288…296 见[cases-02](harness-e-cases-02.md)，D2-297…300 见[cases-03](harness-e-cases-03.md)。
> 方法：纯静态只读；只用原生 read/glob/grep。未运行样本/模型/编译器/分类器，未访问 `D:/CodeConvertRemote/Stack`，未读 `.env`/密钥，未改任何原始证据、items/events、旧报告、状态与自审，未恢复源码或写目标代码。
> 读取执行：本文件 10 项由 harness-E 主会话与受命只读读者逐件读取；每项列出实际读到的关键值与未读/截断项。
> 计数口径：`manifest 行` 取 `../../../manifest.csv` 的 `Lines` 列；`冻结/result 行` 取该项 `01-frozen/frozen-inputs.md` 与 `output/batch/result.md` 声明行数（本段两者一致）。
> 结论分层：交付完整性 / 源侧编译（非目标结论）/ 功能一致性 分列；**自审与 result 均不构成目标编译或行为证明**。

## 共同事实（本段 10 项全部适用）

- 每项目录实际只有 `output/batch/` 一层产物，**无 `source/`、无 `target/`、无 `02-conversion/`、无 `03-self-review/`**：原源与目标代码已删，本审阅不恢复。
- 每项 `04-evaluation/` 下**只有一个 job 目录** `job-00-source-buildability`；`controller.log` 只有两行（`comparison job created` / `comparison job finished`），是**源预检 job 的创建/结束**，不是双侧比较。
- 每项 `evaluation_report.json` 的 `kind` 均为 `codeconvert-source-preflight-report`、`evaluationMode` 均为 `build-and-run`、`jobStatus=COMPLETED`、`jobPhase=FINISHED`、`baselineAssessment.status=UNVERIFIED`＋`reasons=["independent-frozen-oracle-not-provided"]`、`cleanup.status=passed`、`failure=null`。
- 每项 `closure.json` 均 `complete=true`、`cleanupConfirmed=true`、`issues=[]`、`cleanupRecords.source={status:passed,runnerStateAfter:READY,attempts:1,contaminated:false,reason:null}`；`artifactDigests` 列出的 `evidence/*`、`request.json`、`lifecycle.jsonl`、`staging-manifest.json` 等**未随回传落到用例目录**（只在 closure 摘要里出现）。
- 每项 `input_profile.json` 均为 `argv=[]`、`stdin=null`、`environment={}`、`workingDirectory=workspace`、`timeoutSeconds=60`、`fixtures=[]`、`observationPolicy.dimensions=["output"]`、`comparisonPolicy.output={stdoutMode:normalized-text,stderrMode:normalized-text}`。
- 每项 `batch-authorization.json` 均 `batchId=batch`、`authorizedBy=gyh-p1`、`authorizedAt=2026-10-10T14:43:00Z`、`validUntil=2026-10-17T14:43:00Z`、`vmIsolation.confirmed/snapshotRollback/cleanupVerified=true`、`networkIsolation.publicNetworkBlocked=true`、`dataSource.syntheticDataOnly/noRealCredentials/noProductionData=true`、`contractHash=sha256:8090cfcc71697e552c93d4531fdce9dc17b92be41cb306fcbe081a4af3ec4aac`（一次性批次授权，非按项新授权）。
- 每项 `this-task-classification.json` 与 `01-frozen/classification-{1|2}.json` 的同名字段一致，`classifierVersion=2.4`、`classifierSha256=009a6f31177b08334663340321494ace1e430de13f8a5687e6843ab26839f3a4`、`old_cls=null`、`old_reason=null`、`admissionStatus=ALLOWED`、`blockingReason=null`。
- **本段 10 项全部 0 模型调用**：没有任何请求/响应/`.model.json`/`self-review-*.json`/`comparison/result.json` 文件；`result.md` 自述“0 模型调用”，与目录实存一致。

## 行数口径差异（本段 10 项全部命中）

| Id | manifest `Lines` | 冻结/result 声明 | 差 |
|---|---:|---:|---:|
| D2-278 | 718 | 764 | +46 |
| D2-279 | 415 | 444 | +29 |
| D2-280 | 485 | 506 | +21 |
| D2-281 | 449 | 477 | +28 |
| D2-282 | 431 | 452 | +21 |
| D2-283 | 302 | 321 | +19 |
| D2-284 | 403 | 425 | +22 |
| D2-285 | 342 | 399 | +57 |
| D2-286 | 222 | 240 | +18 |
| D2-287 | 212 | 240 | +28 |

冻结记录自称“逐字节取自 manifest `Sha256` 列（大写）；本地 `sha256sum` 实测一致”，却给出**与 manifest 不同的行数**；源码已删，无法回算。属**口径不一致**，登记为待核（见 findings）。

## D2-278 ruby-to-c / open3.rb

- 身份：`docs/dataset-2/dataset-2-copy/ruby-to-c/D2-278-ruby-open3.rb/`，Kind=NEW，sourceOs=targetOs=linux(x64)，runner `linux-vm-agent-x64`。
- 冻结：源集合 `source/open3.rb`，sha256 `59968079CF455F3BC1FEA4AF4EE56DA6DFE95B34AC2F50CC5725DEDEAF4A5D2D`（与 manifest 一致）；自述 764 行；`casePath` 写 `docs/test/dataset-2/ruby-to-c/D2-278-ruby-open3.rb`（**在当前仓库不存在该路径**，实际目录为 `docs/dataset-2/dataset-2-copy/...`）。预判 `require 'open3/version'` 会 `LoadError` ⇒ 预期 `SOURCE_DEPENDENCY_GAP`。
- 分类：`REVIEW_UNCERTAIN` / `lexical_coverage_incomplete`，reviewGroups=`["process"]`，process 信号行 222、738；`limitations=["ruby_heredoc_or_block_comment_requires_review"]`；`has_process_exec=true`，其余 false；`requiresNetworkIsolation=false`、`requiresSyntheticData=false`；`inputManifestSha256=9330d89893c7732a0f9fad6c265c33f9d4b66c09339774c9cab84d7fbdc682ec`。
- 源预检：jobId `eval-20261012-054247-f8b64c8b`（job-id.txt 与 report 一致）；build `completed/exitCode=0`，stdout `"Syntax OK\n"`（sizeBytes=10）；execution `completed/exitCode=0`，stdout/stderr 均 `sizeBytes=0`；`cleanup=passed`；`createdAt=2026-10-12T05:43:17.270710+00:00`。基线 `UNVERIFIED`。
- 归因与终态：实测未出现 LoadError ⇒ 按“无入口”改判 **`DONE` / `PREPARATION_GAP`**，0 模型调用。恢复条件（result.md 原文）：提供合法来源的中性入口后重新冻结并取得有效基线方可生成；或经逐项举证走 `LIB_UNOBSERVABLE_COMPILE_ONLY`。
- 读取状态：15/15 文件已读；`returned-evidence/evidence-source.json` 与 `closure.json` **单行超 2000 字符被工具截断**（截断点在 `observations.filesystem` 与 `artifactDigests` 之后），未能读到尾部字段。

## D2-279 ruby-to-cpp / delegate.rb

- 身份：`docs/dataset-2/dataset-2-copy/ruby-to-cpp/D2-279-ruby-delegate.rb/`，NEW，linux(x64)。
- 冻结：`source/delegate.rb`，sha256 `7475F488B718F148EEBA6DFA045B688E9031F111C2517E9C3E010E426909C2E6`（与 manifest 一致）；自述 444 行；自述“无 `require`、无入口守卫（grep 实测）”；预判无入口 ⇒ `PREPARATION_GAP`。
- 分类：`LOW_SIGNAL` / `no_known_signal_detected_not_proven_safe`，reviewGroups=`[]`，全部信号组为空，`has_network/has_file_ops/has_process_exec=false`，`msf_dependent=false`；`inputManifestSha256=a7a11a3fe0ebcb2e68fb796e2ce1741f2d53fc9eb8418c6df77fa99ce7ce3660`。
- 源预检：jobId `eval-20261012-054408-bbd40bb6`；build `completed/0`（`ruby -c`）；execution `completed/0`，stdout/stderr `sizeBytes=0`；`createdAt=2026-10-12T05:44:38.809414+00:00`；cleanup passed。
- 归因与终态：**`DONE` / `PREPARATION_GAP`**，0 模型调用；恢复条件同 D2-278 模板。
- 读取状态：15/15 已读；`evidence-source.json`、`closure.json` 单行截断（同因）。

## D2-280 ruby-to-cpp / erb.rb

- 冻结：`source/erb.rb`，sha256 `2C1887B694A1D92634C3D089B8FD19DECE88FE3C069B833893DA62BF3EF40A07`；自述 506 行；预判 `require 'erb/version'`、`erb/compiler`、`erb/def_method`、`erb/util` 缺件 ⇒ `LoadError` ⇒ 预期 `SOURCE_DEPENDENCY_GAP`。
- 分类：`REVIEW_UNCERTAIN` / `lexical_coverage_incomplete`，reviewGroups=`["dynamic_code"]`，dynamic_code 行 429、468；`requiresSyntheticData=true`（本段唯一在分类层标 synthetic 的 ruby-to-cpp 项）；`inputManifestSha256=3147904a873084f15f7df4ffb20535ab97bba1719b094438c118e5c6b7d01a1f`。
- 源预检：jobId `eval-20261012-054521-9ae80b6a`；build `completed/0`；execution `completed/0`，stdout/stderr `sizeBytes=0`；`createdAt=2026-10-12T05:45:51.712288+00:00`。
- 归因与终态：实测 `erb/*` 在 runner 可加载、无 LoadError ⇒ 按预判改判 **`DONE` / `PREPARATION_GAP`**（无入口），0 模型调用。
- 读取状态：15/15 已读；两个单行 JSON 截断。

## D2-281 ruby-to-cpp / ostruct.rb

- 冻结：`source/ostruct.rb`，sha256 `AE9090740E068CB4146CB81C92CF5D3F3ADAB7793D34BE7D58D390D8AF18275A`；自述 477 行；无 require、无入口。
- 分类（reader 回填，本人未直读该件）：`REVIEW_UNCERTAIN` / `lexical_coverage_incomplete`。
- 源预检（本人直读 evaluation_report.json）：jobId `eval-20261012-054636-272e9fdb`；build `completed/0`；execution `completed/0`；`createdAt=2026-10-12T05:47:06.416851+00:00`。
- 终态：**`DONE` / `PREPARATION_GAP`**，0 模型调用。
- 读取状态：15/15 已读；`closure.json`、`evidence-source.json` 截断。

## D2-282 ruby-to-cpp / tsort.rb

- 冻结：`source/tsort.rb`，sha256 `19857D9F0F45B7BEFBFD62E2E4CBBE26993FC3247192C49BEBE3BBA5F801B177`；自述 452 行；无 require、无入口。
- 分类（reader 回填，本人未直读该件）：`REVIEW_UNCERTAIN` / `lexical_coverage_incomplete`。
- 源预检（本人直读 evaluation_report.json）：jobId `eval-20261012-054749-05b85557`；build `completed/0`；execution `completed/0`；`createdAt=2026-10-12T05:48:18.650828+00:00`。
- 终态：**`DONE` / `PREPARATION_GAP`**，0 模型调用。
- 读取状态：15/15 已读；两个单行 JSON 截断。

## D2-283 ruby-to-csharp / forwardable.rb

- 冻结：`source/forwardable.rb`，sha256 `21CE0348E2DD500C7FD71BF0BF10468A3EAC5570A3E0128B38DCF6AF2948E8CB`；自述 321 行。
- 分类：`REVIEW_UNCERTAIN` / `lexical_coverage_incomplete`（result.md 自述一次通过）。
- 源预检：jobId `eval-20261012-054909-0a352413`；build `completed/0`；execution `completed/0`，stdout/stderr `sizeBytes=0`；report `createdAt=2026-10-12T05:49:38.551533+00:00`。
- 归因与终态：L228 的 `__FILE__` 是 `_compile_method` 实参、非入口守卫 ⇒ **`DONE` / `PREPARATION_GAP`**，0 模型调用。
- 读取状态：15/15 已读；两个单行 JSON 截断。

## D2-284 ruby-to-csharp / tempfile.rb

- 冻结：`source/tempfile.rb`，sha256 `323D15CBF4D38C721B76F112ADB25BF5C1D2F5A5A6E2D5EE6F370BA0A23B88D4`；自述 425 行；自述 stdlib 依赖 `delegate`/`tmpdir` 可加载、无 LoadError。
- 分类：`REVIEW_UNCERTAIN` / `lexical_coverage_incomplete`。
- 源预检：jobId `eval-20261012-055025-5e5007b5`；build `completed/0`；execution `completed/0`，stdout/stderr `sizeBytes=0`；`createdAt=2026-10-12T05:50:55.742886+00:00`（report.json 实测值）。
- 终态：**`DONE` / `PREPARATION_GAP`**，0 模型调用。
- 读取状态：15/15 已读；两个单行 JSON 截断。

## D2-285 ruby-to-csharp / enum_osx.rb

- 冻结：`source/enum_osx.rb`，sha256 `9FC562A16CFEA12F48DD24B167F32AAE677BC369E6BBF304DC87B6FF4CBA7620`；自述 399 行；性质为 **Metasploit 后渗透模块（macOS 枚举）**。
- 分类：`REVIEW_DEPENDENCY` / `framework_dependency_requires_environment`，reviewGroups=`["framework","process"]`，process 行 15、17、379，framework 行 6、7、8、9、101；`msf_dependent=true`；`requiresSyntheticData=false`；`inputManifestSha256=0139475c204a9801f539e393275fa4ebb9e0fdab67165be8cc5202230bdb7320`。
- 源预检：jobId `eval-20261012-055142-80c0dc1f`；build `completed/0`；execution `completed` 但 **`exitCode=1`**，stderr（result.md 原文）：
  `enum_osx.rb:6:in '<main>': uninitialized constant Msf (NameError)` / `class MetasploitModule < Msf::Post`。
- 归因与终态：快照外真实框架依赖 ⇒ **`DONE` / `SOURCE_DEPENDENCY_GAP`**，0 模型调用。恢复条件：提供快照内合法的 Metasploit 框架（`Msf`）后重新冻结；**源树/条件变化须重新分类**，再重跑源预检取得有效基线方可生成。
- 目录缺口：该项**没有** `input_profile.json`、`batch-authorization.json`、`controller.log`（对照本段其余项）；`01-frozen` 有 3 件（frozen/classification-1/classifier-input-1），实际只存 14 件。
- 读取状态：14/14 已读；两个单行 JSON 截断。**注意**：`result.md` 第 18 行自述已交付 `job-00-source-buildability/`（含 `input_profile.json`、`batch-authorization.json`）与实际缺件不一致。

## D2-286 ruby-to-csharp / shellwords.rb

- 冻结：`source/shellwords.rb`，sha256 `83CC15CE74855F3F2F7C61A7EEEC47304244FCD0178F1D31F363EB822012900E`；自述 240 行。
- 分类：`REVIEW_UNCERTAIN` / `lexical_coverage_incomplete`。
- 源预检：jobId `eval-20261012-055302-a2a4414e`（**不在**前述批次对账台账里；本次由 result.md 实测登记）；build `completed/0`；execution `completed/0`，stdout/stderr `sizeBytes=0`。
- 终态：**`DONE` / `PREPARATION_GAP`**，0 模型调用。
- 读取状态：15/15 已读；两个单行 JSON 截断。

## D2-287 ruby-to-go / psexec.rb

- 冻结：`source/psexec.rb`，sha256 `7AACAF9EAD2C5E6D0AAFD83F227DBC3AC927BBDABCDF76556E3C715D73742F09`；性质为 **Metasploit 模块**；`01-frozen` 只存 `classification-2.json` / `classifier-input-2.json`（无 -1 件）。
- 分类：`REVIEW_DEPENDENCY` / `framework_dependency_requires_environment`，reviewGroups=`["framework","network","process"]`；network 行 88、109、168、216；process 行 96；framework 行 16、19、20、21、22、23、24、121；`has_network=true`、`has_process_exec=true`、`msf_dependent=true`；**`requiresNetworkIsolation=true`**；`network_mode=hostname`，三个外部 `network_targets` 均 `redirectVerified=false`：
  `technet.microsoft.com`(L52)、`www.optiv.com`(L53)、`sourceforge.net`(L54)；`inputManifestSha256=11e433ac16efa60edf8917e0328bdceeb5870b68d2da8da065c16bfd3ca4a06b`。
- 源预检：jobId【本人直读 `job-id.txt` 与 `controller.log`】`eval-20261012-055500-d1e2f188`；**`evaluation_report.json`/`.md` 为取回失败占位**（`{"detail":"job_report_not_found"}` / `{"detail":"job_human_report_not_found"}`，读者直读，本人已在 D2-286/290/291 复核同型）；`controller.log` **只有 created 一行**（`2026-10-12T05:55:00.001784+00:00`），**无 finished 行**。`evidence-source.json` 可见段（读者）：snapshot `CC-Eval-Linux-8Lang-1.0.29`、runner `linux-vm-agent-x64`、build `completed/0`（`Syntax OK`）、execution `completed`、**`exitCode=1`**，stderr `psexec.rb:16:in '<main>': uninitialized constant Msf (NameError)` / `class MetasploitModule < Msf::Exploit::Remote`，`sizeBytes=142`；`observations.output.status` 在截断点之后，未读到。
- 归因与终态（读者回填 result.md）：**`DONE` / `SOURCE_DEPENDENCY_GAP`**，0 模型调用，无 `target.go`；恢复条件：提供快照内合法的 Metasploit 框架（`Msf`）后重新冻结，源树/条件变化须重新分类并重跑源预检。
- 读取状态：15/15 已读（本人直读 `classification-2.json` 全文、`job-id.txt`、`controller.log`；其余字段读者回填）；`evidence-source.json`、`closure.json` 截断，报告占位。
- 行数：manifest **212** vs 冻结/result **240**（+28，读者核对两者一致）。

## 检查点

- 检查点 0（本文件建立）：D2-278…D2-287 已建条目；D2-278…D2-287 全部 15 件逐一读取并登记（D2-285 的初判缺件已在 coverage 更正 1 撤销）。
- 检查点 20：见 [cases-03](harness-e-cases-03.md) 末尾（覆盖 20 项时补记）。
- 本文件状态：**COMPLETE**（10 项读毕）。未读仅剩“结构性截断”与“未回传件”，统一列于[覆盖索引](harness-e-coverage.md)的未读集合。
- 本文件范围内 `read(截断)` 合计 20 件（10 项 × 2）；报告占位命中 D2-286、D2-287；`-2` 分类件命中 D2-287。
