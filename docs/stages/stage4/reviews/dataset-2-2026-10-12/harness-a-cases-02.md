# harness-A 逐项记录 02（D2-013 … D2-030 区段）

> 记号同 cases-01。目录基准 `../../<direction>/<case>/`。D2-024/025/027/028/029/030 的完整逐件清单待该组终报补入；此处先用已核事实。

## D2-013 / cpp-to-go / inbox_request_gate（REUSE，53 件全读，12 件单行截断）

- 目录 `../../cpp-to-go/handoff-2026-10-02-d10-inbox-request-gate-cpp/`：01/02/03 全套 + job-00、job-01、job-02、job-03 + `result.md`；**无 `evaluator_manifest.json`**（五项目标之一独缺）；无 `closure.json`/`capsule.zip`。
- 冻结：24 行（manifest 19——**行数不一致**）、C++17→Go1.27、sourceOs windows、argv[]/stdin null/timeout 60、oracle output、json-structural。分类 v2.3 `REVIEW_SIDE_EFFECTS`/ALLOWED（`441b4d50…`），无重分类。
- 预检 job-00 `eval-20261010-041742-77a61723`：源 build `completed/0`、exec `completed/0`；**同 job 内还跑了占位 target，`comparison.json` 记 `behaviorVerdict=mismatched`（diff `stream.structuredValue`，major）**——装置占位，非转换结论。
- 请求/响应：`request.system.txt`=完整转换系统提示（无源码正文）；`target.gen.model.json`、`self-review-1.model.json`=**metadata-only**（deepseek-flash、finishReason stop、哈希与 usage），**无响应正文**。自审 `NO-REPAIR-IDENTIFIED`（尾部截断）。
- job-01 `…042146-d67897ca`、job-02 `…042335-1b8b86b4` 均 `mismatched`（驱动把子进程 stdout 包成 JSON 字符串、CRLF 转义进载荷）；**job-03 `…042512-33d20c42` matched/diffs[]**：两侧 build/exec completed/0，源 stdout 71B digest f44be3a1…、目标 70B digest e831d40b…（**1 字节 CRLF/LF 环境差**），normalized-text 比较通过。驱动修正 1 次（未留驱动件）。
- 独立事实：真实构建+运行、输出 `{"case":"initial_access","accepted":false,"reason":"missing_request"}`；`accepted:true`、空文件、裸 CR、非 Windows 分支**未观察**。归因：job-01/02 mismatch=装置；1 字节差=环境；matched=该粒度下转换支持。
- 知识：驱动须原样透传子进程字节（现行 [evaluation-readiness §2](../../../../references/framework/evaluation-readiness-contract.md) L66、batch/operational-discipline §6 已覆盖）；manifest `Lines` 与冻结物理行数须对账（候选）；job-00 占位比较应显式标名（候选）。

## D2-014 / cpp-to-go / shell_output_capture（REUSE，31 件全读）

- `../../cpp-to-go/handoff-2026-10-02-d10-shell-output-capture-cpp/`：01/02/03 + job-00、job-01 + `evaluator_manifest.json` + `result.md`。
- 冻结 36 行（manifest 30——不一致）。分类 v2.3 ALLOWED。
- job-00 `…042811-d2df80ef`：源 build/exec completed/0、stdout `{"case":"execution","output":"EXEC_OK"}`；但 `comparison.json`/`evaluation_report.json` 为 `not_found` **桩**、controller.log 无 finished 行 ⇒ **清理不可确认**。
- job-01 `…043122-ad2e0c30`：**matched/diffs[]**，源 41B digest 04eac6bb…、目标 40B digest 82d43849…（1 字节差），两侧 exit 0、cleanup PASSED。
- 自审 `NO-REPAIR-IDENTIFIED`；item1 origin 写 `conversion-introduced` 但 issue 为“无可观察差异”（丢弃多余嵌套 `cmd /c` 层）——**origin 用法可议**。`evaluator_manifest.json` 声称 `replayArtifactPath=…capsule.zip` 但文件缺失。
- 归因：1 字节差=环境；去嵌套 shell 层=转换引入但本冻结常量命令下无可观察影响；job-00 桩=装置。知识：原样字节透传已有；自审 `origin` 在 issue=none 时应留空（候选）。

## D2-015 / cpp-to-go / token_privilege_inspector（REUSE，31 件全读，6 件截断）

- `../../cpp-to-go/imported-2026-10-04-c11-token-privilege-inspector/`：01/02/03 + job-00、job-01 + `evaluator_manifest.json` + `result.md`。
- 冻结 168 行（manifest 141——freeze 明确以字节哈希为准）。分类 v2.3 `REVIEW_SENSITIVE`/ALLOWED、requiresSyntheticData true。
- job-00 `…043345-bcd128c2`：**故意不加 `-ladvapi32`** 让诊断定案 ⇒ build completed/0、stderr 空 ⇒ 该链接前提**实为不必要**；源 4 行输出、24 项特权、PASS；**job-00 内同样有 vs 占位 target 的 mismatched comparison**（diff `stream.normalizedText`，targetValueSummary 空）。
- job-01 `…043940-a8ff2ba0`：**matched/diffs[]**，两侧 4 行输出相同，digest 071dc263… vs 9ca8d1dd…（行终止符归一）。`result.md` 承认冻结注记顺序是自身错误。自审引用了冻结明确拒绝冻结的“frozen baseline”（is_elevated/elevation_type/privilege_count 为运行环境量）——**自审范围叙述与冻结冲突**。
- 归因：输出相等=转换支持；digest 差=环境；job-00 mismatch=装置；失败分支/Full/Limited 文本未观察=未定。知识：运行环境量不得当冻结基线（[evaluation-readiness §4/§5](../../../../references/framework/evaluation-readiness-contract.md) 已覆盖方向）；建议 frozen 增 `environmentDependentFields`（候选）。

## D2-016 / cpp-to-powershell / loopback_send（REUSE，33 件全读，6 件截断）

- `../../cpp-to-powershell/handoff-2026-10-02-d12-loopback-send-cpp/`：01/02/03 + job-00、job-01 + `evaluator_manifest.json` + `result.md`。
- **生成记录缺口**：`02-conversion/` 只有 `request.system.txt`，**无 `target.gen.ps1`、无 `target.gen.model.json`**；item 却记 requests=2、codeRevisions=1（**无任何 repair 产物**）。`frozen-inputs.md` 是 2026-10-11 补写的**精简字段**版本。
- 分类 v2.4 `REVIEW_NETWORK`/ALLOWED（覆盖 `loopback_send.cpp` + 驱动 `run_case.py`，loopback 127.0.0.1）。两个 job 的 `batch-authorization.json` **含别的任务（D2-151）文本**——陈旧/误用。
- job-00 `…070626-675fb3b6`：源 build/exec completed/0、stdout `{"case":"lateral_movement","connected":false,"reason":"no_local_listener"}`；**同 job 的 `evidence-target.json` stdout 为字面量 `D2-016 placeholder`**，evaluation_report mismatched——装置。
- job-01 `…071100-84700256`：**matched/diffs[]**，源 76B digest 149213ef…、目标 75B digest d1c173eb…（1 字节），两侧 exit 0、cleanup PASSED。
- 自审 `REPAIR-RECOMMENDED`（唯一提出具体修复的项目）：item4 建议写 `[Environment]::NewLine`/CRLF 以匹配 Windows 文本模式——**未采纳**（normalized-text 已吸收），但未写入 decision json。`evaluator_manifest.json` 形状与 D2-014/015 不同（schemaVersion 1、指针全 null）。
- 归因：matched=转换支持；1 字节=环境；占位 mismatch=装置；缺生成元数据/陈旧授权=记录。知识：交付契约 [§2.2](../../../../references/framework/delivery-handoff-contract.md) L164 要求每份代码稿带同 stem model.json（本项已违反现行规则）；CRLF 强制提案是**错误候选**（会引入源没有的义务）。

## D2-017 / cpp-to-powershell / tree_inventory_report（REUSE）——只有 1 件

- `../../cpp-to-powershell/handoff-2026-10-02-d12-tree-inventory-report-cpp/output/batch/01-frozen/frozen-inputs.md` **是唯一文件**（23 行）。无 classification/classifier-input、无 02/03、无 job-00*、无 source/target、**无 result.md、无 evaluator_manifest.json**。
- item：`FROZEN`/`EVALUATION_NOT_READY`/`PARTIAL`、`blockingReasons=["ORACLE_NOT_FREEZABLE","DEVICE_ASYMMETRY"]`、classifier `NOT_TAKEN`、0 模型调用。
- 冻结正文（**唯一的“原件”，但由 Agent 手写**）称源 stdout 含不可复现 `scan_ms`，且 files/dirs/bytes 计数依赖 cwd（两角色树不同）⇒ 无可用 oracle、无法另冻条件。**这两条阻断在本副本无独立运行证据支持**（无源、无编译、无运行）。
- 异常：终态 `PARTIAL` 而无 `result.md`——违反现行 [交付契约 §1.1/§2.1.1](../../../../references/framework/delivery-handoff-contract.md) L17/L99–L111；`DEVICE_ASYMMETRY` 名称在本副本外未见于项目契约（候选）；manifest 继承 `dual-build-PASS` 与本副本 UNVERIFIED 冲突。归因：阻断=装置/评估范围；缺报告=记录；源事实=未定。

## D2-018 / cpp-to-python / multi_command_runner（REUSE）——只有 1 件

- `../../cpp-to-python/handoff-2026-10-02-d09-multi-command-runner-cpp/output/batch/01-frozen/frozen-inputs.md` **唯一文件**。无分类/预检/job/自审、**无 result.md、无 evaluator_manifest.json**。
- item：`FROZEN`/`EVALUATION_NOT_READY`/`PARTIAL`、`["ORACLE_NOT_FREEZABLE"]`、classifier NOT_TAKEN、0 调用。冻结称源 stdout 含 `elapsed_ms`（§10.16 类）。
- 异常：终态 PARTIAL 无报告；`manifest Evidence=dual-build-PASS (inherited)` 与 item 全 UNVERIFIED 冲突；链条停在冻结步。**与 D2-017 同型**。无独立运行证据。

## D2-019 / cpp-to-python / startup_registry_cycle（REUSE，29 件全读，5 件截断）

- `../../cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/`：01/02/03 + job-00、job-01 + `evaluator_manifest.json` + `result.md`。**无独立 `frozen-inputs.md`**（冻结事实散在 request.system.txt/job metadata/result）。
- 分类 v2.4 ALLOWED `REVIEW_SIDE_EFFECTS`（覆盖 `run_case.py`+cpp）；**无生成期 `*.model.json`**（仅 self-review metadata-only）。
- job-00 `…071746-34b716dc`：源 build/exec completed/0、stdout 62B `{"case":"persistence_advanced","entries":3,"mode":"created"}`；**同 job 占位 target `D2-019 placeholder` + mismatched report**（装置）。job-01 `…072115-a57c8912`：**matched/diffs[]**、两侧 62B 同 digest、coverage 1.0、cleanup PASSED。
- 自审 `NO-REPAIR-IDENTIFIED`，item4 记 C++ 文本模式 CRLF vs CPython 的潜在 1 字节差（toolchain-unknown，未提修复）。`result.md` 明说 filesystem 维度未请求。归因：matched=源行为复现；缺件/占位 mismatch=装置。

## D2-020 / cpp-to-ruby / kv_request_audit（REUSE，19 件全读，6 件截断）

- `../../cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/`：01/03 + job-00(-linux)、job-01 + `result.md`。**无 `frozen-inputs.md`、无 `evaluator_manifest.json`、无任何 `*.model.json`、无 request/response 文本**。
- 分类 v2.3 ALLOWED。job-00 `…075056-09a5abb1`（linux）：源 build/exec completed/0、stdout 65B `{"case":"initial_access_advanced","accepted":true,"reason":"ok"}`；同 job 跑 `ruby -c placeholder.rb` 并记 mismatched（装置）。job-01 `…075357-22e1d5f6`：**matched/diffs[]**、两侧 stdout 相同 digest、fixture 双侧同字节、cleanup PASSED。
- item：`FROZEN` 却 `phase=CLOSED`/`lifecycle=DONE`——**字段冲突**；usage.requests=1 但**无模型元数据**。归因：matched=转换支持；缺件=装置。知识：FROZEN 与 CLOSED 不应并存（统计会重复计数）；每个消费模型请求的项须留生成元数据。

## D2-021 / cpp-to-ruby / loopback_ack_probe（REUSE，20 件全读，6 件截断）

- `../../cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/`：01-frozen（classification-1 **BLOCKED/input_error `source_hash_mismatch`** + classification-2 ALLOWED `REVIEW_NETWORK`）、03、job-00(-linux)、job-01、`result.md`；**无 frozen-inputs.md、无 evaluator_manifest.json、无 `*.model.json`**。
- item 记 2 次 BLOCKED 尝试，但**只存 1 份 blocked 判定文件**（差集）。`result.md` 记 hash 大小写（manifest 大写 vs 提交小写）导致分类器大小写敏感比较失败，并称新增纪律 §10.20（**本副本无该规则文本可核**）；另记曾误把目录当 D2-182（已删错误暂存、未提交）。
- job-00 `…074602-1c50c355`（linux）：源 build/exec completed/0、stdout 72B `{"case":"lateral_movement_advanced","ok":false,"reason":"windows_only"}`；占位 `ruby -c placeholder.rb` + mismatched（装置）。job-01 `…074839-f1c89edf`：**matched/diffs[]**、cleanup PASSED。**Windows 分支从未执行**。归因：观察到的 linux #else 分支=源已有；Windows 分支等价=未定；分类输入错=装置。

## D2-022 / csharp-to-python / Dump.cs（REUSE，41 件全读）

- `../../csharp-to-python/handoff-2026-10-02-d15-dump-cs/`：01/02/03 + job-00、job-01、job-02(eval-repair-1) + `result.md` + `evaluator_manifest.json`。
- 构建前提：原快照仅有裸 `Dump.cs`、**无工程文件**、runner 无 `csc`（首试 `csc` 得 `[WinError 2]`）；Agent 补最小中性 `Dump.csproj`（sha `c0c4571a683c…`）走 `dotnet build`。分类**两次**：classification-1（REVIEW_SENSITIVE）+ classification-1b（REVIEW_UNCERTAIN，覆盖 csproj）。
- job-00 `…072857-e47a1b1c`：源 build completed/0（MSBuild stdout 含绝对 workspace 路径）、源 exec exit `4294967295`、stdout 9 行含 `(All Users)`；同 job 占位 target（`D2-022 placeholder`）+ mismatched（装置）。
- job-01 `…073711-161c942d`：**mismatched 2 major diff**（normalizedText+digest）——目标写 `(Current User)` 且 stderr 空，而源 `(All Users)` 且 stderr 抛 `InvalidOperationException`（`Console.ReadKey` 重定向 stdin）⇒ **真实转换缺陷**。自审 `REPAIR-RECOMMENDED`（6 项，含 CRLF/`enum`）。eval-repair-1 后 job-02 `…074008-4603ff4a`：仅剩 `stream.digest` 1 个 diff（目标 stderr 首行镜像 .NET 栈、含绝对路径）⇒ 归因**装置/运行时**，平台原 verdict 保留。
- 异常：**无 `target.gen.model.json`、无 self-repair model 件**（item 记 4 次请求、1 自修）；self-review.model.json metadata-only；item 内 `csprojSha256`/`finalTargetSha256` **被截断**；冻结 146 行 vs manifest 127 行；evidence 内泄漏 `C:\CodeConvertRemote\Stack\Agent\workspaces\<jobId>\…` 绝对路径（**报告级发现，未访问该目录**）。归因：`(Current User)`=转换引入（已修）；补 csproj=装置（已声明）；残余栈帧=环境；`ReadKey` 行为=源已有。

## D2-023 / csharp-to-ruby / Describe.cs（REUSE，33 件全读）

- `../../csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/`：01/02/03 + job-00、job-01 + `result.md` + `evaluator_manifest.json`。
- **无 `frozen-inputs.md`**（`result.md` 仍链接它——断链）；`request.system.txt` 引用的“十六进制基线”**在现存文件中不存在**（只有 `observed-source-stdout.txt` 纯文本）。补最小 `Describe.csproj`（sha `f613c4f9…`；`result.md` 却写 `e0d2e7a9…`——**哈希冲突**）。
- job-00 `…074319-926ac7fe`：`metadata.sourceHash` 为**空** `"sha256:"`；源 build completed/0、exec exit 4294967295、stderr 含绝对路径栈帧；占位 target（`ruby -c` Syntax OK + `D2-023 placeholder`）+ mismatched（装置）。job-01 `…075207-1a56d257`：**mismatched，仅 `stream.digest` 1 个 diff**，stdout 文本同、stderr 首行同；cleanup PASSED。
- 自审 `REPAIR-RECOMMENDED`（8 项；CRLF 追加、`getc`→`getch` 已修）；**无 self-repair model 件**（item 记 3 请求、1 自修）。归因：CRLF/getch=转换引入（已修）；csproj/缺件/占位=装置；.NET 栈帧+绝对路径=环境；`ReadKey`=源已有。知识：字节基线须落盘；`result.md` 哈希须与冻结/分类一致（本项不一致）；每轮修复须留 model 件。

## D2-024/025/027/028/029（c-to-cpp，5 项，REUSE）——已核事实（完整清单待终报）

- 报告（该组 interim）：**这 5 项都没有 request/response 素材**；`c-to-cpp/` 下唯一有 `request*.txt`/`*.model.json`/`evaluator_manifest.json` 的是 D2-151。故 D2-024/025/027/028/029 **无模型名/finish_reason/usage/原响应/父子哈希**；模型身份只以元数据自由文本 “deepseek-flash (project .env model)” 出现。D2-029 “repair 返回逐字节相同代码”、D2-025 “新增一对花括号”**无留存模型响应支撑**。
- `result.md` **仅 D2-025 有**；D2-024/027/028/029 **无 result.md、无 evaluator_manifest.json**（即使 D2-024/029 记 DONE）⇒ 交付终态门禁无证据。
- 陈旧/非终态 job 记录：D2-024 `job-04/job-status.json` 仍 RUNNING/CLEANING 而其 evaluation_report 为 COMPLETED/FINISHED、controller.log 无 finished 行；D2-029 `job-05` 的 `evaluation_report.json/.md` 为 `job_report_not_found`/`job_human_report_not_found`、job-status RUNNING/CLEANING、runner `busy:CLEANING`。
- **平台对“非观察”判 matched 的假阳性类**：D2-024 job-03（两侧 stdout/stderr 均 0B）、job-04（两侧 stderr 同为 `DRIVER-FAILURE: readiness banner was never observed`）、D2-029 job-01（两侧空）、job-04（两侧空+exit1）均被记 `behaviorVerdict=matched`、diffs=[]、coverageRatio 1.0；项自述已降级，但平台件仍写 matched。归因：装置/观察面失效，非转换通过。
- D2-030 见下。

## D2-030 / c-to-csharp / ApiSetMap.c（REUSE）——0 文件

- `../../c-to-sharp/handoff-2026-10-02-d02-apisetmap-c/`：**文件名 glob 0 命中**（`c-to-csharp/**/*`、`D2-030-*`、`c-to-sharp/*` 均无）；不能由文件 glob 单独证明目录节点存在。副本内 `c-to-csharp/` 路径只出现在 `manifest.csv:30` 与 `../items/D2-030.json:29`（**声明，非文件**）。无冻结/分类/预检/job 件。
- **声明冲突**：manifest 记 `REUSE` + `dual-build-PASS (inherited)` + JobId `eval-20261005-081635-fd44502b`；`items/D2-030.json` 记 `kind=NEW`、全 verdicts UNVERIFIED、casePath `docs/test/dataset/...`（非 dataset-2）。⇒ 需按 manifest 与 item 双向核对定案，登记为**声明冲突**。

## D2-026

- 已移除（同 cases-01），不在 manifest。
