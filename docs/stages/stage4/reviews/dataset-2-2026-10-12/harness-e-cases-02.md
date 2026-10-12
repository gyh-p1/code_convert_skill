# harness-E 逐项记录 02（D2-288 … D2-296）

> 状态：**COMPLETE**（D2-297…300 见[cases-03](harness-e-cases-03.md)）。范围与读取状态见[覆盖索引](harness-e-coverage.md)；汇总判读见[发现](harness-e-findings.md)。
> 方法：纯静态只读；只用原生 read/glob/grep。未运行样本/模型/编译器/分类器，未访问 `D:/CodeConvertRemote/Stack` 及 `jobs`，未读 `.env`/密钥，未改任何原始证据、items/events、旧报告、状态、自审、未恢复源码或写目标代码。
> 来源标注：本文件条目中凡标 **【本人直读】** 的字段由 harness-E 主会话亲自读取；其余字段由受命**只读读者**逐件读取回填，并由主会话对其中的高信号件另行直读复核（如各项 `evaluation_report.json`、`controller.log`、分类件）。读者报告与本人复核冲突处按**磁盘实况**登记并标出。
> 计数口径：`manifest 行` 来自 `../../../manifest.csv` 的 `Lines` 列；`冻结/result 行` 来自该项 `01-frozen/frozen-inputs.md` 与 `output/batch/result.md`（读者核对：两者**彼此一致**，但与 manifest **全部不等**）。

## D2-288 ruby-to-go / enum_services.rb（15 件）

- 行数：manifest **175** vs 冻结/result **204**（+29）。sha256 `3FF4D191FF6251F73B245A3320D25C474B93C51A1BE4D2B28D02C1318487C2A4`。
- 分类【本人直读】：`REVIEW_DEPENDENCY` / `framework_dependency_requires_environment`，reviewGroups=`["framework","process"]`，process `[70]`，framework `[80,135,201,202]`；`msf_dependent=true`、`has_process_exec=true`、`requiresNetworkIsolation=false`、`requiresSyntheticData=false`；`inputManifestSha256=711fe58d89f0f1939e1fb95916be9cc3c643adb838bff65af8860573f77101cb`；`old_cls=null`。
- 源预检【本人直读 evaluation_report.json】：jobId `eval-20261012-055640-8864a840`（`job-id.txt` 一致）；build `completed/0`（stdout `Syntax OK`）；execution `completed`、**exitCode=1**；`createdAt=2026-10-12T05:57:10.639357+00:00`；`baselineAssessment=UNVERIFIED`；`cleanup=passed`；`failure=null`。
- 运行错误（读者自 `evidence-source.json` 读到，未截断段）：`enum_services.rb:79:in '<module:Msf>': Post is not a class (TypeError)` / `enum_services.rb:43: previous definition of Post was here` / `from enum_services.rb:42:in '<main>'`。
- `controller.log`：created `2026-10-12T05:56:40.943350+00:00` / finished `2026-10-12T05:57:10.664314+00:00`（2 行，完整）。
- `metadata.json` note 关键句：`inline Rex/Msf stubs; class MetasploitModule < Msf::Post at L135; $0==__FILE__ entry at L200`。
- 终态：**DONE / SOURCE_DEPENDENCY_GAP**，0 模型调用，无 `target.go`。恢复条件：提供快照内合法的 Metasploit 框架（`Msf`/`Rex`）后重新冻结；源树/条件变化须重新分类，再重跑源预检取得有效基线方可生成。
- 归因：源依赖与快照内联存根语义冲突（源已有/环境），**非转换引入**。
- 读取状态：15/15 已读；`evidence-source.json`、`closure.json` 截断（工具 2000 字符/行）。

## D2-289 ruby-to-go / enum_shares.rb（15 件）

- 行数：manifest **172** vs 冻结/result **208**（+36）。sha256 `74CFCCF1759A33420D95EC4D93CD485538CC8E0A45840746A0844530EDD4ABBC`。
- 分类【本人直读】：`REVIEW_DEPENDENCY`，reviewGroups=`["framework","process"]`，process `[103,104]`，framework `[6,7,8]`；`msf_dependent=true`；`inputManifestSha256=0c45689e94b6e0e21578f012f1f56547ce828341756955123f840b8af220d2f1`。
- 源预检【本人直读】：jobId `eval-20261012-055759-172c133c`（一致）；build `completed/0`；execution `completed`、**exitCode=1**；`createdAt=2026-10-12T05:58:28.937644+00:00`；cleanup `passed`；failure `null`。
- 运行错误：`enum_shares.rb:6:in '<main>': uninitialized constant Msf (NameError)` / `class MetasploitModule < Msf::Post`；stderr sizeBytes 135。
- `controller.log`：created `05:57:59.211091` / finished `05:58:28.961619`。
- 终态：**DONE / SOURCE_DEPENDENCY_GAP**，0 模型调用，无 `target.go`。
- 读取状态：15/15 已读；2 个单行 JSON 截断。

## D2-290 ruby-to-go / chrome_cookies.rb（15 件）—— **证据缺件项**

- 行数：manifest **206** vs 冻结/result **243**（+37）。sha256 `881C804E55AC52424CC406B8A99206C4D745DACCE80A6CFF86B80551742A0859`。
- 分类【本人直读】：`REVIEW_DEPENDENCY`，reviewGroups=`["filesystem","framework","network"]`，filesystem `[128]`，framework `[6,7]`；`network_mode=loopback`，唯一 `network_target` = `localhost` L128（scope `loopback`，`redirectVerified=false`）；`has_network=true`、`has_file_ops=true`；`requiresNetworkIsolation=false`（**与 has_network=true 并存**）。
- **`returned-evidence/evaluation_report.json` 与 `evaluation_report.md` 是取回失败占位**【本人直读复核】：`{"detail":"job_report_not_found"}` / `{"detail":"job_human_report_not_found"}`。因此本项**本地没有 report 级 jobId / evaluationMode / buildAssessment / executionAssessment / baselineAssessment / cleanup / failure / createdAt**；`evaluationMode` 只能从 `source_preflight_manifest.json` 得到（`build-and-run`）。
- 源预检（仅 `evidence-source.json` 可见段，读者读到）：jobId `eval-20261012-055913-2819c120`；snapshot `CC-Eval-Linux-8Lang-1.0.29`；runner `linux-vm-agent-x64`；build `completed/0`（`Syntax OK`）；execution `completed`、**exitCode=1**；stderr `chrome_cookies.rb:6:in '<main>': uninitialized constant Msf (NameError)`；`observations.output.status` **在截断点之后，未读到**。
- `controller.log`【本人直读】：**只有 1 行** `[2026-10-12T05:59:13.565779+00:00] comparison job created`，**无 finished 行**。
- `closure.json` 仍写 `complete=true`/`cleanupConfirmed=true`，且 `artifactDigests` 记录了一个真实 `evaluation_report.json` 摘要（读者读到 `e0024097…`）⇒ **本地占位是取回失败，不是“报告不存在”**；但 closure 的完成声明与本地报告缺件**并存不一致**。
- 终态（result.md）：**DONE / SOURCE_DEPENDENCY_GAP**，0 模型调用，无 `target.go`。
- 读取状态：15/15 已读；`evidence-source.json`、`closure.json` 截断。

## D2-291 ruby-to-go / observer.rb（15 件）—— **证据缺件项 + 去向争议**

- 行数：manifest **220** vs 冻结/result **229**（+9）。sha256 `05FF80534E118FB9E07C35A21688D5922F6406F5985C8B359CBE2D7ADC85D9FB`。
- 分类【本人直读】：`LOW_SIGNAL` / `no_known_signal_detected_not_proven_safe`，reviewGroups=`[]`，**全部信号组为空**，`msf_dependent=false`；`inputManifestSha256=9a998d4cea11f86071c6922f11b127e31685660a85d9f88127567b21e541d154`。
- **报告占位件**【本人直读复核】：`evaluation_report.json` = `{"detail":"job_report_not_found"}`；`evaluation_report.md` = `{"detail":"job_human_report_not_found"}`。job-id.txt【本人直读】= `eval-20261012-060050-c6153d88`（**与 `evidence-source.json`/`closure.json` 内的 jobId 一致**；读者报告里出现的另一个 jobId 字样与磁盘不符，按磁盘登记）。
- 源预检（`evidence-source.json` 可见段）：build `completed/0`；execution `completed`、**exitCode=0**、stdout/stderr 均空；`observations.output.status=observed`（读者读到该字段在截断点之前）。
- `controller.log`【本人直读】：**只有 1 行** `[2026-10-12T06:00:50.517055+00:00] comparison job created`，**无 finished 行**。
- 终态（result.md）：**DONE / PREPARATION_GAP**，0 模型调用，无 `target.go`。恢复条件：提供合法来源的中性入口后重新冻结并取得有效基线，方可生成；或经逐项举证走 `LIB_UNOBSERVABLE_COMPILE_ONLY`。
- **去向争议（未定）**：源可构建（`ruby -c` 0）且可运行（exit 0、空输出），属“本轮无法合法评估行为但源可构建”一类；契约 §1.3 该类应记 `LIB_UNOBSERVABLE_COMPILE_ONLY` 并**继续生成、验证目标语法/编译**。本项却以 `PREPARATION_GAP` 停止且 0 模型调用。与 D2-278…284、D2-286 同属一类，口径见 [findings F2](harness-e-findings.md)。
- 读取状态：15/15 已读；`evidence-source.json`、`closure.json` 截断。

## D2-292 ruby-to-powershell / cve_2021_40449.rb（15 件）

- 行数：manifest **142** vs 冻结/result **153**（+11）。sha256 `DB55B2EFD23C9FD4B045D17231514CC022BEA69424C3A2DDE1B9311930723277`。
- 分类【本人直读】：`REVIEW_DEPENDENCY`，reviewGroups=`["framework","network","process"]`，process `[24,30,78]`，framework 30 项（6,9-14,82-84,89,91,93,…,147）；`network_mode=hostname`，5 个外部目标 `securelist.com` L58、`mp.weixin.qq.com` L59、`github.com` L60/L61、`www.qualys.com` L88，全部 `redirectVerified=false`；**`requiresNetworkIsolation=true`**；file limitations `["unterminated_or_unsupported_string"]`。
- 版本关联：`01-frozen` **只有 `-2` 件**（`classification-2.json` + `classifier-input-2.json`），无 `-1` 件；`result.md` 自述首轮判 `BLOCKED`/`public_network_unverified` 后加 `--network-isolation-configured` 重分类、“误生成的 `classification-1.json` 已删除”。但 `classification-2.json` 的 `old_cls`/`old_reason` 仍为 `null`，**重分类事实不落在分类件字段里**（只在 result.md 与 metadata.note）。
- 源预检【本人直读】：jobId `eval-20261012-060238-52b478f8`（一致）；build `completed/0`；execution `completed`、**exitCode=1**；`createdAt=2026-10-12T06:03:07.822090+00:00`；cleanup `passed`。
- 运行错误：`cve_2021_40449.rb:6:in '<main>': uninitialized constant Msf (NameError)` / `class MetasploitModule < Msf::Exploit::Local`。
- `controller.log`：created `06:02:38.028214` / finished `06:03:07.847198`。
- 终态：**DONE / SOURCE_DEPENDENCY_GAP**，0 模型调用，无 `target.ps1`。
- 读取状态：15/15 已读；2 个单行 JSON 截断。

## D2-293 ruby-to-powershell / process_herpaderping.rb（15 件）

- 行数：manifest **167** vs 冻结/result **192**（+25）。sha256 `8D819CD0B6B889A4FC54C134A1AF9717226BAD86AE17E4E01782299AEB9FBA3B`。
- 分类【本人直读】：`REVIEW_DEPENDENCY`，reviewGroups=`["framework","network"]`，framework `[8,115,137]`，network 信号列表为空；`network_mode=hostname`，4 个外部目标 `jxy-s.github.io` L25/L51、`github.com` L43/L52，全部 `redirectVerified=false`；`requiresNetworkIsolation=true`；file limitations `["ruby_heredoc_or_block_comment_requires_review","unterminated_or_unsupported_string"]`。
- 版本关联：只有 `-2` 件；`result.md` 记“首轮判 `BLOCKED`… `classification-1.json` 已删除”。
- 源预检【本人直读】：jobId `eval-20261012-060406-23765b7b`（一致）；build `completed/0`；execution `completed`、**exitCode=1**（读者读到 stderr 为 `cannot load such file -- metasploit/framework/compiler/windows (LoadError)`，**注意这与其它 Metasploit 项的 `Msf` NameError 不同**）；`createdAt=2026-10-12T06:04:36.894526+00:00`；cleanup `passed`。
- `controller.log`：created `06:04:06.379807` / finished `06:04:36.922590`。
- 终态：**DONE / SOURCE_DEPENDENCY_GAP**，0 模型调用，无 `target.ps1`。
- 读者登记的小不一致：framework 信号列表从 L8 起、**不含 L6**，而 metadata/frozen 都把 L6 的 `require 'metasploit/framework/compiler/windows'` 作为依赖来源；`closure.json` 的 `artifactDigests` 记名为 `classification.json`，而磁盘上实际是 `classification-2.json`；result.md 交付清单写有“capsule”，但目录内无 capsule 归档。
- 读取状态：15/15 已读；2 个单行 JSON 截断。

## D2-294 ruby-to-powershell / docker_creds.rb（15 件）—— **证据缺件项**

- 行数：manifest **121** vs 冻结/result **140**（+19）。sha256 `7C4A83452CF5B10D71C6BA5B6BAADFD882C487547BDF24AB80F79EF9B5E3A754`。
- 分类【本人直读】：`REVIEW_DEPENDENCY`，reviewGroups=`["framework","sensitive"]`，sensitive `[124]`，framework `[63,64,65,138]`；`network_targets=[]`、`network_mode=none-detected`；`requiresSyntheticData=true`；`requiresNetworkIsolation=false`；`inputManifestSha256=9e7561539b667c0fdaaf6bd5d199505a08c7c75096649543afbfbf63c425f61a`。
- 版本关联：**只有 `-1` 件**（与 `../reconciliation-6.md` §5“D2-264~294 多项 -1 已删除”的概括冲突；见 [findings F5](harness-e-findings.md)）。
- **报告占位件**（读者直读）：`evaluation_report.json` = `{"detail":"job_report_not_found"}`；`evaluation_report.md` = `{"detail":"job_human_report_not_found"}` ⇒ 本地无 report 级字段。`job-id.txt` = `eval-20261012-060527-04840085`，与 `evidence-source.json`/`closure.json` 的 jobId 一致。
- 源预检（`evidence-source.json` 可见段）：build `completed/0`（`Syntax OK`）；execution `completed`、**exitCode=1**；stderr `docker_creds.rb:42:in '<module:Msf>': Post is not a class (TypeError)` / `docker_creds.rb:13: previous definition of Post was here` / `from docker_creds.rb:12:in '<main>'`；`observations.output.status` 在截断点之后，未读到。
- `controller.log`（读者+本人复核）：**只有 1 行** created `[2026-10-12T06:05:27.795727+00:00]`，**无 finished 行**。
- `closure.json` 仍写 `complete=true`/`cleanupConfirmed=true` 并记录 `evaluation_report.json`/`.md` 摘要（读者读到 `41fa6d51…`/`cc7cc277…`）⇒ 同 D2-290：**本地占位 ≠ 报告不存在**，但完成声明与本地缺件并存不一致。
- 终态：**DONE / SOURCE_DEPENDENCY_GAP**，0 模型调用，无 `target.ps1`。
- 读取状态：15/15 已读；2 个单行 JSON 截断。

## D2-295 ruby-to-powershell / abbrev.rb（15 件）

- 行数：manifest **120** vs 冻结/result **132**（+12）。sha256 `C0A070CCE23C9F76D8E423037AC2B7DF165088F93A2AE4844ED32BC2E66ECACB`。
- 分类（读者直读）：`LOW_SIGNAL` / `no_known_signal_detected_not_proven_safe`，reviewGroups=`[]`，全部信号为空，file limitations=`[]`（空）；`msf_dependent=false`；`inputManifestSha256=bc720ec654ac949bd3fd3bc89b3b09211a042ce0c8fd422fd672ee5bb200ad1a`。
- 源预检【本人直读 report.json】：jobId `eval-20261012-060708-c93e8a19`（一致）；build `completed/0`；execution `completed`；`createdAt=2026-10-12T06:07:38.580183+00:00`；cleanup `passed`；`baselineAssessment=UNVERIFIED`。
- `evidence-source.json`（读者读到）：execution `exitCode=0`，stdout/stderr 均空；`observations.output.status=observed`。
- `controller.log`：created `06:07:08.977611` / finished `06:07:38.607267`（2 行完整）。
- 终态：**DONE / PREPARATION_GAP**，0 模型调用，无 `target.ps1`。
- 读取状态：15/15 已读；2 个单行 JSON 截断。

## D2-296 ruby-to-powershell / singleton.rb（15 件）

- 行数：manifest **160** vs 冻结/result **177**（+17）。sha256 `51F22A15586DB82994BF33E613B4213BC4ED696D642F74A35732C48A03A2FCB1`。
- 分类（读者直读）：`REVIEW_UNCERTAIN` / `lexical_coverage_incomplete`，reviewGroups=`[]`，全部信号为空；file limitations=`["ruby_heredoc_or_block_comment_requires_review"]`（**唯一触发“uncertain”的因素**）；`inputManifestSha256=e1d2a4f8b18d56ac2d1449f9516dd2e2de1c4c12bada2a13b7084fd5d9bddf59`。
- 源预检【本人直读 report.json】：jobId `eval-20261012-060825-115f4738`（一致）；build `completed/0`；execution `completed`；`createdAt=2026-10-12T06:08:55.087793+00:00`；cleanup `passed`。
- `evidence-source.json`（读者读到）：execution `exitCode=0`，两流空；`observations.output.status=observed`。
- `controller.log`：created `06:08:25.885912` / finished `06:08:55.109920`。
- 终态：**DONE / PREPARATION_GAP**，0 模型调用，无 `target.ps1`。
- 读取状态：15/15 已读；2 个单行 JSON 截断。

## 本文件小结（D2-288…D2-296，9 项）

- 终态分布：`SOURCE_DEPENDENCY_GAP` 7 项（288/289/290/292/293/294 及 285，其中 285 在 cases-01）、`PREPARATION_GAP` 3 项（291/295/296）。**全部 0 模型调用、全部无目标代码。**
- 执行退出码：**exit 1** 共 6 项（288/289/290/292/293/294）；**exit 0 空输出** 3 项（291/295/296）。
- 证据缺件（report 占位 + `controller.log` 无 finished 行）：**D2-290、D2-291、D2-294**（另 D2-286/287 同类，见 cases-01/01）。
- 全部 9 项 `evidence-source.json` 与 `closure.json` 均被工具截断。
