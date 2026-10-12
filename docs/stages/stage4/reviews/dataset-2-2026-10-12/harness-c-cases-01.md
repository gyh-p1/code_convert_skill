# Harness C 逐项审阅记录 01（D2-161 .. D2-180）

> 状态：**IN_PROGRESS**（本文件覆盖 20 个编号位的 01 组；已完成部分在各项标注，未完成项在组末列出）。
> 引用基准：`docs/dataset-2/dataset-2-copy/`。文件清单纯文件名见 [harness-c-coverage.md](harness-c-coverage.md) §4；本文件记事实、证据、自审、归因与优化。
> 硬约束：只读静态审阅；未编译/运行/调用模型/改动任何原始证据。源与目标代码已删除，结论只引用现存记录。
> 读取限制：`read`/`grep` 对单行 >2000 字符 JSON 会截断且不可分页，相关件记 `⚠️截断`。

---

## D2-161 — c-to-go / date.c（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest 行 `D2-161, NEW, c-to-go, C→Go, date.c, 434 行, Origin=测试用例c\c测试用例\环境探测\date.c, JobId=(空), Sha256=B768…F77A`。item：`casePath=c-to-go/D2-161-c-c-date.c`、`disposition=SOURCE_DEPENDENCY_GAP`、`phase=SOURCE_PRECHECK_FAILED`、`lifecycle=DONE`、`usage.requests=0`、`codeRevisions=0`。classifier v2.3 `ALLOWED`/`LOW_SIGNAL`。
- **文件清单与读取**：8 件全部 ✅已读——`01-frozen/{frozen-inputs.md, classifier-input.json, classification-1.json}`；`04-evaluation/job-00-source-buildability-linux/{comparison_manifest.json, input_profile.json, metadata.json}`；`returned-evidence/{evaluation_report.json, evidence-source.json}`（后者 ⚠️截断，单行 >2000 字符）。`source/`、`02-conversion/`、`03-self-review/` 目录不存在。
- **版本关联**：源 sha `b768887a…6f77a` 在 manifest/item/classifier-input/classification/frozen 五处逐字符一致。job `eval-20261010-060516-bb95ac01`（`bundleId=evb-source-eval-…bb95ac01`，`inputProfileHash=3b81f3aa…`，`artifactHash=30eeff9e…`，`toolchainFingerprint={}`，agent/collector 1.0.0）。无模型元数据（0 请求）。
- **证据支持的事实**：源侧 `build.failed/1`，224 ms；stdout 空（digest=e3b0c442… 空串）；stderr 137 B，原文含 `date.c:61:10: fatal error: vary.h: No such file or directory`。`execution.status=blocked`。目标侧 `execution.performed=false`、`evidenceBundleRef=null`、preflight/cleanup=SKIPPED。源 cleanup `PASSED/1`、`contaminated=false`、`environmentStatus=clean`、`runnerStateAfter=READY`。`comparisonRef=null`、`runVerdict=blocked`、`codeVerdict=behaviorVerdict=inconclusive`、`coverageRatio=0.0`、`failure=CODE_RESULT/code`。
- **自审**：无产物（0 模型调用），无条目。
- **失败/重提**：仅 1 次源预检 attempt，无重提。events 116–119：FROZEN_AND_CLASSIFIED→SOURCE_PRECHECK(failed/1)→RECOVERY_CHECK(0 命中)→TERMINAL。
- **未定/缺件**：缺 `result.md`（应交未交）；`evaluator_manifest.json` 未发生。manifest `Lines=434` 与 frozen「480 行」不一致（源已删，待核）。
- **归因**：源构建失败=**源已有**（BSD `date(1)` 伴随模块缺失）＋**装置/打包**（快照不含 `vary.h`）；无转换引入。

## D2-162 — c-to-go / uname.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `uname.c, 260, Sha256=A10E…1D8B`。item `SOURCE_NOT_BUILDABLE`/`SOURCE_PRECHECK_FAILED`/`DONE`；classifier `ALLOWED`/`REVIEW_SIDE_EFFECTS`；`usage.requests=0`。
- **文件清单与读取**：12 件全部 ✅已读；两件 `evidence-source.json` ⚠️截断。job-00b 的 `evaluation_report.json` **✖缺件**（目录仅 4 件）。
- **版本关联**：job-00 `eval-20261010-060735-7c22a0a0`（`inputProfileHash=ce63ea18…`、`artifactHash=9a834217…`，failed/1，172 ms）；job-00b `eval-20261010-060904-6010be29` 的 `inputProfileHash`/`artifactHash`/stderr digest 与 job-00 **完全相同** ⇒ 盲区实验只换命令未换源。
- **证据支持的事实**：两侧 job 只报同一处 `uname.c:49:10: fatal error: sys/sysctl.h: No such file or directory`；stdout 空；execution blocked；target performed=false；cleanup PASSED/clean；comparisonRef=null。
- **自审**：无。
- **失败/重提**：job-00（正式）＋job-00b（**盲区隔离 attempt，非重提**）。events 120–124 含 BLINDSPOT_PROBE。
- **未定/缺件**：`result.md`、`evaluator_manifest.json`、两 job 的 `job-id.txt`/授权/分类副本/`controller.log`；manifest 260 vs frozen「300 行」不一致。
- **规则对照（重要）**：`batch/pattern-note-bsd-userland-macos-correction.md:21` 要求 BSD/FreeBSD userland 的候选 sourceOs **必须含 macOS**；本项磁盘上**只有 1 个 linux job**，而 item/frozen 断言 `sourceBuild=FAILED (FreeBSD-only system interfaces)` 属**超出证据范围的外推**（历史说明，非已核事实）。
- **归因**：`sysctl`/`osreldate.h` 缺失=源已有＋环境；无转换引入。

## D2-163 — c-to-go / wc.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `wc.c, 336, B206…8B9D2`。item `SOURCE_NOT_BUILDABLE`/`ALLOWED`/`LOW_SIGNAL`；`requests=0`。`classification-1.json.inputManifestSha256=c54429d6…`（item 无该字段）。
- **文件清单与读取**：8 件全部 ✅已读；`evidence-source.json` ⚠️截断。
- **版本关联**：job `eval-20261010-061128-01c56a83`（`inputProfileHash=17c9e268…`、`artifactHash=900aac94…`，failed/1，72 ms，stderr 159 B）。
- **事实**：`wc.c:45:10: fatal error: sys/capsicum.h: No such file or directory`；stdout 空；execution blocked；target performed=false；cleanup PASSED/clean；comparisonRef=null。
- **自审**：无。**失败/重提**：1 次，无重提。events 125–128 齐全。
- **未定/缺件**：`result.md` 等装置件缺；manifest 336 vs frozen「368 行」不一致；同 D2-162 的 macOS 候选缺测/外推（更正文件第 19/21 行点名 D2-163）。
- **归因**：Capsicum+libxo+libcasper=源已有 FreeBSD 依赖＋环境。

## D2-164 — c-to-go / ln.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `ln.c, 347, 4AB1…4221B`。item `SOURCE_NOT_BUILDABLE`/`REVIEW_SIDE_EFFECTS`（信号 317/338/345）；`diagnosticCounts={__dead2:4, err_h:0}`；`grouping.sameFamilyAs=[D2-027,D2-028]`；`requests=0`。
- **文件清单与读取**：8 件全部 ✅已读；`evidence-source.json` ⚠️截断（截点在 stderr 正文中段，`stderr.digest`/`sizeBytes` 未取得）。
- **版本关联**：job `eval-20261010-061317-6d426fd7`（`inputProfileHash=2e070a0d…`、`artifactHash=3cdf314a…`，failed/1，118 ms）；`input_profile.argv=["--help"]`。
- **事实**：`ln.c:70:34: error: expected declaration specifiers before '__dead2'` ＋4 处 `__dead2` 与 5 处级联语法错误；stdout 空；execution blocked；target performed=false；cleanup PASSED/clean。
- **自审**：无。**失败/重提**：1 次。events 129–132 记 `errHReported:false`（证伪「err.h 普遍缺失」）。
- **未定/错误建议（重点）**：frozen 第 36 行断言「`__dead2`…已登记系统 linux/windows/macos × x64 均不提供」，但磁盘只有 1 个 linux job；更正文件第 19 行指出 macOS 提供含 `__dead2` 的 `sys/cdefs.h` ⇒ **越界外推**。另 frozen 第 46–49 行记「未用 `-D__dead2=` 绕过」（正确，避免丢失 noreturn 语义）。
- **归因**：`__dead2` 未声明=源已有 BSD 依赖＋环境。

## D2-165 — c-to-go / tr.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `tr.c, 344, 439A…4244C`。item `SOURCE_NOT_BUILDABLE`/`LOW_SIGNAL`；`extraGap`：`cmap.h/cset.h/extern.h` 三伴随头不存在；`requests=0`。
- **文件清单与读取**：8 件全部 ✅已读；`evidence-source.json` ⚠️截断。
- **版本关联**：job `eval-20261010-061527-afeb6b01`（`inputProfileHash=13301db9…`、`artifactHash=f7963c6f…`，failed/1，71 ms，stderr 159 B）。
- **事实**：`tr.c:44:10: fatal error: sys/capsicum.h: No such file or directory`；stdout 空；execution blocked；target performed=false；cleanup 干净；comparisonRef=null。
- **自审**：无。**失败/重提**：1 次。
- **未定/缺件/装置**：events 133–135 **缺 `FROZEN_AND_CLASSIFIED`**（产物实存）⇒ events 与产物交集缺口；`cmap.h/cset.h/extern.h` 的「穷举 0 命中」为 frozen 自述，未独立复核。
- **归因**：Capsicum=源已有＋环境；伴随头缺失=源已有/打包；events 缺行=装置。

## D2-166 — c-to-go / uniq.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `uniq.c, 347, 93F4…3684B`。item `SOURCE_NOT_BUILDABLE`/`REVIEW_SIDE_EFFECTS`；`extraGap=no companion headers needed`；`requests=0`。
- **文件清单与读取**：8 件全部 ✅已读；`evidence-source.json` ⚠️截断。
- **版本关联**：job `eval-20261010-061656-d33517ea`（`inputProfileHash=fac27af5…`、`artifactHash=91e2c992…`，failed/1，118 ms，stderr 161 B）。
- **事实**：`uniq.c:47:10: fatal error: sys/capsicum.h: No such file or directory`；stdout 空；execution blocked；target performed=false；cleanup 干净。
- **自审**：无。**失败/重提**：1 次；events 139 记 `CONTROLLER_BUSY_OBSERVED`（提交期预创建拒绝后重提，未产生多余 job）＝装置。
- **未定/缺件**：events 136–138 **缺 `FROZEN_AND_CLASSIFIED`**；manifest 347 vs frozen 无行数对照。
- **归因**：Capsicum=源已有＋环境。

### 组级归因（D2-161..166）

| 维度 | 判定 | 依据 |
|---|---|---|
| 源已有 | 6/6 | 源为 FreeBSD userland；`vary.h`/sysctl/Capsicum/libxo/libcasper/`__dead2` 均为 BSD 侧既有依赖 |
| 转换引入 | 0/6 | 无 `02-conversion`、0 模型请求、无 target 产物 |
| 环境 | 6/6 | linux glibc 不提供上述接口；`err.h` 在 linux **存在**（D2-164 计数） |
| 装置 | 6/6 | 缺 `result.md`/`evaluator_manifest.json`/`job-id.txt`/job 级授权与分类副本/`controller.log`；D2-162 job-00b 缺 `evaluation_report.json`；D2-165/166 缺 `FROZEN_AND_CLASSIFIED` event；7 件单行 JSON 尾部截断 |

## D2-167 — c-to-powershell / byebyedll.c（FROZEN / WAITING / DRIVER_NOT_VIABLE）

- **身份**：manifest `byebyedll.c, 157, BC8E…2C4BF`。item `FROZEN`/`EVALUATION_NOT_READY`/`WAITING`、`blockingReasons=[DRIVER_NOT_VIABLE]`、`requests=0`、`codeRevisions=0`。
- **文件清单与读取**：22 件全部 ✅已读；`job-00` 与 `job-00b` 的 `evidence-source.json` ⚠️截断（2 件）。缺 `02-conversion/`、`03-self-review/`、`source/`、`result.md`、`evaluator_manifest.json`、`controller-health-*`、`runners-*`。
- **版本关联**：源 sha 一致；frozen `sourceLines=189` 与 manifest `157` **冲突**（待核）。job-00 `eval-20261011-040912-a8f16ccd`、job-00b `eval-20261011-041041-1b262367`（windows x64，snapshot `CC-Eval-Windows-8Lang-1.0.28`，runner `windows-vm-agent-x64`）。`metadata.targetHash=sha256:placeholder-precheck`；无模型响应。
- **证据事实**：job-00（原始契约）`build failed/1`（4652 ms），stderr 起于宏重定义告警、后 5 处 `-Wincompatible-pointer-types`（GCC 14 升级为 error）；job-00b 加一个 `-Wno-error=incompatible-pointer-types` 后 `completed/0`（4408 ms），但源执行在 argv=`["probe"]` 下**超时**（`evaluation_report` reason=`Source execution timed-out; baseline unavailable.`）。两侧 `preflight/cleanup=PASSED`、`clean`、`READY`。target `performed=false`。
- **自审**：空集（`03-self-review/` 缺件）。
- **失败/重提**：attempt A 编译失败 / attempt B 单标志隔离后编译通过但执行超时；均落盘。
- **归因**：源已有（Win64 32/64 位类型不匹配、`PROCESS_CREATION_MITIGATION_POLICY…` 重定义）；环境（GCC 14 严格化）；装置（`MessageBox` 无可观察输出 ⇒ DRIVER_NOT_VIABLE）；无转换引入。

## D2-168 — c-to-powershell / chmod.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `chmod.c, 236, BAA4…BC800`。item `SOURCE_NOT_BUILDABLE`/`DONE`、`requests=0`。
- **文件清单与读取**：25 件全部 ✅已读；两件 `evidence-source.json` ⚠️截断。缺 `result.md` 等；job-00b **无** `comparison.json`/`evaluation_report.md`；job-00 的 `comparison.json` 内容为 `{"detail":"comparison_not_found"}`。
- **版本关联**：源 sha 一致；`sourceLines=236`＝manifest。job-00 `eval-20261011-041249-879d80f5`（macos）、job-00b `eval-20261011-041453-0a8a9b6e`（linux）。`metadata.targetHash=placeholder-precheck`；`comparison_manifest` target 声明 `build_case.ps1`/`run_case.py`，但**磁盘无这两个驱动文件**。
- **证据事实**：macos `failed/1`（4754 ms）stderr `chmod.c:250:10: error: call to undeclared function 'lpathconf'`＋`_PC_ACL_NFS4` 未声明（3 errors）；linux `failed/1`（1835 ms）stderr `chmod.c:60:25: error: expected declaration specifiers before '__dead2'`＋`__unused` 级联。两侧 target `performed=false`、`runVerdict=blocked`、`coverageRatio=0.0`；清理 PASSED/clean。
- **自审**：空集。**失败/重提**：两平台各 1 次，均失败。
- **归因**：源已有（FreeBSD `lpathconf`/`_PC_ACL_NFS4`/`__dead2`/`__unused`）；装置（驱动声明与实物脱节、job-00b 缺件）。

## D2-169 — c-to-powershell / LoadLibraryR.c（FROZEN / WAITING / DRIVER_NOT_VIABLE）★本组最重要

- **身份**：manifest `LoadLibraryR.c, 248, AEDF…4B4C`。item `FROZEN`/`EVALUATION_NOT_READY`/`WAITING`、`blockingReasons=[DRIVER_NOT_VIABLE]`、`verdicts.targetBuild/execution/comparison` 全 `UNVERIFIED`、`requests=0`。
- **文件清单与读取**：14 件全部 ✅已读；`evaluation_report.json`、`evidence-source.json`、`evidence-target.json` ⚠️截断（3 件）。缺 `02-conversion/`、`03-self-review/`、`source/`、`result.md`、`evaluator_manifest.json`、`comparison.json`。
- **版本关联**：源 sha 一致；`sourceLines=248`＝manifest。job `eval-20261011-041912-86ccf27a`（windows x64，`CC-Eval-Windows-8Lang-1.0.28`）。`metadata.targetArtifact="target/target.ps1 (placeholder)"`。
- **证据事实（与 item 叙述存在实质张力）**：`evidence-source.json` 源 `build completed/0`（3459 ms，仅 `IMAGE_ORDINAL` 重定义告警），`execution.status=completed/exitCode=97`（驱动自失败码，截断区外未命中 `DRIVER-FAILURE`）。`evidence-target.json` 为**真实 bundle 而非 not_found**：target `build completed/0`、`execution completed/0`、stdout=`D2-169 precheck placeholder\n`（29 B）。`evaluation_report.json`：source 与 target **均** `execution.performed=true`、`comparisonRef=comparison/result.json`、`runVerdict=partial-runnable`、**`codeVerdict=failed`、`behaviorVerdict=mismatched`**，failure=`CODE_RESULT/behavior`。`evaluation_report.md` Evidence Matrix：`Output | mismatched | 3`。清理 PASSED/clean。
- **自审**：空集。
- **失败/重提 attempt**：无第二次 attempt；但 job-00 **本身含一次占位 target 的双侧比较**，其 `mismatched`/`failed` 未反映到 item/事件字段（item 仍写 UNVERIFIED）。
- **归因**：源已有（库 TU 无 `main`、导出函数须真实 PE 输入）；**装置**：(a) 名为 source-buildability 的 job 实跑占位 target 并产出**伪 FAIL 信号**；(b) 源侧驱动自失败码 97 仍判 `execution.status=completed` 并参与比较；(c) `comparisonRef` 指向的 `comparison/result.json` 盘上不存在。无转换引入。

## D2-170 — c-to-powershell / cmp.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `cmp.c, 251, 179A…6FB2`。item `SOURCE_NOT_BUILDABLE`/`DONE`、`requests=0`。
- **文件清单与读取**：23 件全部 ✅已读；两件 `evidence-source.json` ⚠️截断。缺 `result.md` 等；job-00 无 `evaluation_report.md`/`comparison.json`。
- **版本关联**：源 sha 一致；`sourceLines=251`＝manifest。job-00 `eval-20261011-042101-2a98a554`（macos）、job-00b `eval-20261011-042304-f758e1b5`（linux）。**`metadata.json` 两处 `sourceHash=sha256:PLACEHOLDER`**（占位未替换）。
- **证据事实**：macos `failed/1`（17632 ms）`cmp.c:48:10: fatal error: 'capsicum_helpers.h' file not found`；linux `failed/1`（122 ms）同头 `No such file or directory`。target `performed=false`、blocked/inconclusive/coverage 0.0；清理 PASSED/clean。
- **自审**：空集。**失败/重提**：两平台各 1 次失败。
- **归因**：源已有（Capsicum 头族、次要 `<libutil.h>`/`extern.h`）；装置（`sourceHash=PLACEHOLDER`）。

## D2-171 — c-to-powershell / head.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `head.c, 203, ED77…7C96`。item `SOURCE_NOT_BUILDABLE`/`DONE`、`requests=0`。
- **文件清单与读取**：23 件全部 ✅已读；两件 `evidence-source.json` ⚠️截断。缺 `result.md` 等；两侧均无 `evaluation_report.md`/`comparison.json`。
- **版本关联**：源 sha 一致；`sourceLines=203`＝manifest。job-00 `eval-20261011-042526-93843697`（macos）、job-00b `eval-20261011-042759-1ad9cc5d`（linux）。**`frozen-inputs.md` 缺 `casePath` 行**（另缺 `sourceLang/sourceStd`、`selected skills`）。
- **证据事实**：macos `failed/1`（10520 ms）`head.c:44:10: fatal error: 'sys/capsicum.h' file not found`；linux `failed/1`（293 ms）同头。target `performed=false`；清理 PASSED/clean。
- **自审**：空集。**失败/重提**：两平台各 1 次失败。
- **归因**：源已有（Capsicum 头族）；装置（frozen 字段缺失）。

## D2-172 — c-to-powershell / env.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `env.c, 229, 8FFD…97D4`。item `SOURCE_NOT_BUILDABLE`/`DONE`、`requests=0`。
- **文件清单与读取**：23 件全部 ✅已读；两件 `evidence-source.json` ⚠️截断。缺 `result.md` 等。
- **版本关联**：源 sha 一致；`sourceLines=229`＝manifest。job-00 `eval-20261011-042952-f8a1fca4`（macos）、job-00b `eval-20261011-043140-f2e550e0`（linux）。`frozen-inputs.md` 缺 `casePath`。
- **证据事实**：macos `failed/1`（6021 ms）`env.c:49:10: fatal error: 'login_cap.h' file not found`；linux `failed/1`（272 ms）同头。target `performed=false`；清理 PASSED/clean。
- **自审**：空集。**失败/重提**：两平台各 1 次失败。
- **归因**：源已有（FreeBSD `login_cap.h`、次要 `envopts.h`）；装置（frozen 字段缺失）。

## D2-173 — c-to-powershell / kill.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `kill.c, 192, 0E04…3FA1BD`。item `SOURCE_NOT_BUILDABLE`/`DONE`、`requests=0`。
- **文件清单与读取**：23 件全部 ✅已读；两件 `evidence-source.json` ⚠️截断。缺 `result.md` 等。
- **版本关联**：源 sha 一致；`sourceLines=192`＝manifest。job-00 `eval-20261011-043421-7d1f230d`（macos）、job-00b `eval-20261011-043609-243aa543`（linux）。`frozen-inputs.md` 缺 `casePath`。
- **证据事实**：macos `failed/1`（9005 ms）`kill.c:92:33: error: use of undeclared identifier 'sys_nsig'; did you mean 'sys_nerr'?`（L165/L190 同）；linux `failed/1`（171 ms）`kill.c:64:25: error: expected declaration specifiers before '__dead2'`。target `performed=false`；清理 PASSED/clean。
- **自审**：空集。**失败/重提**：两平台各 1 次失败。
- **文档矛盾**：job 两 `metadata.json` note 写阻断点是 `bltin/bltin.h`，而 `frozen-inputs.md` 明确 `bltin.h` 在 `#ifdef SHELL` 内、未包含、非阻断点（`events.jsonl:300` 采用 frozen 口径）。
- **归因**：源已有（`sys_nsig`、`__dead2`）；装置（note 与 frozen 冲突、frozen 字段缺失）。

### 组级汇总（D2-167..173）

- **去向**：5 项 `SOURCE_NOT_BUILDABLE`（168/170/171/172/173）＋2 项 `WAITING/DRIVER_NOT_VIABLE`（167/169）。**7/7 未发生转换**（`requests=0`、无 `02-conversion/`）。
- **归因**：源已有=阻断头/符号与无 main 库形态；转换引入=**0**；环境=macOS/Linux 无 BSD 头族、GCC 14 严格化；装置=placeholder target 参与比较（D2-169）、`sourceHash=PLACEHOLDER`（170）、per-item `batch-authorization.json` 串用他项场景文案（7 项，本组为 D2-151 文案）、驱动声明与实物脱节、frozen 字段缺失（171/172/173）、`result.md`/`evaluator_manifest.json` 全缺。
- **知识候选**：Capsicum/login_cap/BSD 私有符号三层判据＋“先穷举条件编译确认无回退分支”；`SOURCE_NOT_BUILDABLE` 与 `DRIVER_NOT_VIABLE` 必须分列；`-Wno-error=` 单标志隔离实验只用于分离工具链契约、降级后仍登记源缺陷；库 TU 缺合法 PE 输入不得补造驱动。
- **未定**：D2-169 placeholder 比较是否应计入“submitted”、其 3 条 Output diff 原文（盘上无）；D2-167 行数 157 vs 189。

## D2-174 — c-to-python / feal8_encrypt.c（FROZEN / CLOSED / DONE，matched）

- **身份**：manifest `feal8_encrypt.c, 103, 0551…49CE`。item `FROZEN`/`CLOSED`/`DONE`；`verdicts`：源 build `completed/0`、目标 build `completed/0（py_compile）`、execution `both completed/0`、comparison `matched（output, 24 bytes byte-identical, diffs=0）`、environment `clean`；`finalTargetSha256=630a865e…`；`requests=2`、`failedAttempts=0`、`codeRevisions=0`；`coverageGap`：payload remainder 分支不可达、`feal8_decrypt` 两侧均未调用。classifier v2.3 `ALLOWED`/`LOW_SIGNAL`。
- **文件清单与读取**：27 件全部 ✅已读。`01-frozen/` 3 件；`02-conversion/{request.system.txt, target.gen.model.json}`；`03-self-review/{review.system.txt, self-review-1.json, self-review-1.model.json}`；`job-00-source-buildability`（`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`；`returned-evidence/{evaluation_report.json, evidence-source.json}`）；`job-01-dual-build`（6 配置件＋`returned-evidence/{comparison.json, controller-health-after.json, controller.log, evaluation_report.json, evaluation_report.md, evidence-source.json, evidence-target.json}`）；`evaluator_manifest.json`、`result.md`。**⚠️截断**：`self-review-1.json` 单行 >2000 字符（item 7 之后未读）。
- **版本关联**：源预检 job `eval-20261010-050740-29701a1f`（`build completed/0`，note「VLA accepted at -std=c11」）；双侧 job `eval-20261010-051112-0696f12a`。`target.gen.model.json` **只含哈希、无 content 正文**⇒ 生成响应不完整、不可核验（回应任务口径「只含哈希的 model.json 不算完整响应」）。
- **证据事实**：job-01 两侧 build/execution `completed/0`，stdout 24 B 逐字节相同、diffs=0；env clean。job-00 为**占位 target 比较**：`codeVerdict=failed`、`behaviorVerdict=mismatched`、`runVerdict=partial-runnable`，且 report 称 target `execution.performed=true` 却**缺 `evidence-target.json` 与 `comparison.json`**。
- **自审**：`self-review-1.json` 裁决 `NO-REPAIR-IDENTIFIED`；可读条目 1–7：rotl 掩码、G 顺序、F、roundKey 小端、块切分、末尾 swap、key_schedule（item 7 起截断）。scope=冻结契约 Windows x64、argv 空、stdin null、stdoutMode=normalized-text、源基线 24 B。无可定位转换引入项。
- **失败/重提**：无失败 attempt（`failedAttempts=0`）。
- **归因**：无转换引入；占位比较与只哈希响应=装置。

## D2-175 — c-to-python / WjCryptLib_Rc4.c（FROZEN / EVALUATION_NOT_READY / WAITING）

- **身份**：manifest `WjCryptLib_Rc4.c, 146, 7556…C60D`。item `FROZEN`/`WAITING`、`blockingReasons=[DRIVER_NOT_VIABLE]`、`requests=0`、`codeRevisions=0`；`packagingGap`：伴随头 `WjCryptLib_Rc4.h` 从旧 dataset 还原（sha `f33d3a78…4f7c0`，依据「旧副本除行尾外逐字节相同」）；源预检 `completed/0`（macos `clang -c`）。
- **文件清单与读取**：13 件全部 ✅已读。`01-frozen/` 3 件；`job-00-source-buildability`（6 配置件＋`returned-evidence/{evaluation_report.json, evidence-target.json, controller.log, evidence-source.json}`）。**缺**：`result.md`、`evaluator_manifest.json`、`02-conversion/`、`03-self-review/`（后两者因 0 模型调用不适用）。
- **版本关联**：frozen `sourceLines=167` 与 manifest `146` **冲突**（待核）。classifier v2.4 `ALLOWED`/`REVIEW_SIDE_EFFECTS`，且**把驱动 `run_case.py`（sha `87470819…57bd`）纳入分类**并命中 process 信号（D2-177/178 未纳入 ⇒ 同方向包形制不一致）。
- **证据事实**：job-00 源侧 stderr=`DRIVER-FAILURE: no runnable artifact …`，目标 stdout=`D2-175 placeholder`；平台判 `failed`/`mismatched`——**装置占位比较，非转换差异**；target `performed=false`。
- **自审**：空集（`03-self-review/` 不适用）。
- **失败/重提**：仅 job-00；无重提。
- **归因**：无转换引入（未生成目标）；占位比较与驱动不可用=装置。

## D2-176 — c-to-python / pwd.c（CONVERTED / CLOSED / DONE，matched）★关键缺件

- **身份**：manifest `pwd.c, 109, F0C6…A653`。item `CONVERTED`/`CLOSED`/`DONE`；源预检 `completed/0`、`execution completed/1`（stderr 恰 `usage: pwd [-L | -P]\n`）；双侧 `both completed/1`、stderr 逐字节相同、comparison `matched（diffs=0）`；`finalTargetSha256=263a02f7…`；`requests=2`、`codeRevisions=1`、`selfRepairRounds=0`。classifier v2.4 `ALLOWED`/`REVIEW_SIDE_EFFECTS`。
- **文件清单与读取**：25 件全部 ✅已读。**✖缺 `01-frozen/frozen-inputs.md`** 与 **✖缺 `02-conversion/target.gen.model.json`**；其余：`01-frozen/{classification-1.json, classifier-input.json}`、`02-conversion/request.system.txt`、`03-self-review/{review.system.txt, self-review-1.json, self-review-1.model.json}`、`job-00-source-buildability`、`job-01-dual-build`、`evaluator_manifest.json`、`result.md`。
- **版本关联**：源预检 job `eval-20261011-044225-4bd3f741`；双侧 job `eval-20261011-044853-96b7b153`。`result.md:17` **仍链接不存在的 `01-frozen/frozen-inputs.md`**；`result.md` 记源「123 行」与 manifest `109` 冲突。
- **证据事实**：job-01 两侧 `build completed/0`、`execution exitCode=1`、stdout 空、stderr 逐字节相同（`usage: pwd [-L | -P]\n`）；本 argv=`["extra"]` 下 matched 成立。job-00 为占位比较（3 条 diff 全来自 placeholder 文本）。
- **自审**：`self-review-1.json` 裁决 `REPAIR-RECOMMENDED`，7 条：item 1 与 item 7 为 `conversion-introduced`（**同一处**：未知选项时目标未复现 libc `getopt` 诊断行），item 2–6 无差异。**未修**（result 称需先取得源侧实际文案、不臆测）。
- **失败/重提**：无失败 attempt；0 自修。
- **记录冲突**：item `codeRevisions=1` 与 `result.md`「0 轮自修」冲突；**冻结门禁物缺失却记 DONE**。
- **归因**：未知选项诊断差异属**转换引入但未修**（不在冻结 argv 覆盖内，待取证）；缺 frozen/响应=装置；无目标正文可核。

## D2-177 — c-to-python / which.c（FROZEN / CLOSED / DONE，matched after repair）

- **身份**：manifest `which.c, 123, 6BE7…D706`。item `FROZEN`/`CLOSED`/`DONE`；两次双侧 job：job-01 `eval-20261010-051930-786c50fc` **matched 但假阳性**（驱动未转发冻结 argv），job-02 `eval-20261010-052111-789721d1` matched（stdout `/usr/bin/sh`、exit 0）；`finalTargetSha256=602c57e6…`；`requests=4`、`codeRevisions=1`、`selfRepairRounds=1`、`driverCorrections=2`；`repairSummary`：3 行模型修复（`os.fsencode`×2 + `getopt.gnu_getopt`）。classifier v2.3 `ALLOWED`/`REVIEW_SIDE_EFFECTS`。
- **文件清单与读取**：29 件全部 ✅已读。`02-conversion/{repair1.system.txt, request.system.txt, target.gen.model.json, target.self-repair-1.model.json}`；`03-self-review/{review.system.txt, review2.system.txt, self-review-1.json, self-review-1.model.json, self-review-2.json, self-review-2.model.json}`；`job-00`、`job-01-dual-build`（含 `attribution.md`）、`job-02-argv-forwarding`；`evaluator_manifest.json`、`result.md`。**⚠️截断**：`self-review-1.json`、`self-review-2.json` 单行 >2000 字符；`target.gen.model.json`/`target.self-repair-1.model.json` **只含哈希**。
- **证据事实**：job-01 两侧 exit=1、stdout 空、stderr 均为 usage 文本 ⇒ 核心 PATH 搜索未跑；`attribution.md` 明确归因装置并**保留原 verdict**；job-02 修正驱动后两侧 stdout=`/usr/bin/sh\n`、exit 0、matched。`job-00/returned-evidence/evaluation_report.json` 内容为 `{"detail":"job_report_not_found"}`；job-01/job-02 均无 `controller-health-before.json`。
- **自审**：self-review-1 `REPAIR-RECOMMENDED`：item 3/4 `conversion-introduced`（`len()` 字符数 vs C `strlen` 字节数，边界 PATH_MAX/FILENAME_MAX），item 1/2/5/6 无差异（可读部分）；self-review-2 `NO-REPAIR-IDENTIFIED`：确认 3 项修复正确，残留环境依赖（`POSIXLY_CORRECT` 下 glibc 停止重排而 `gnu_getopt` 始终重排；冻结未设该变量，不触发）。
- **失败/重提**：job-01 假阳性 → 装置修正（driver 转发 argv）→ job-02 matched；**未消耗模型修复调用**。
- **归因**：转换引入=字符/字节长度换算（已修）；装置=驱动未转发 argv、`job_report_not_found`、缺 health-before。

## D2-178 — c-to-python / strnsubst.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `strnsubst.c, 101, 24FB…9D42`。item `SOURCE_NOT_BUILDABLE`/`CLOSED`/`DONE`、`requests=0`；`trueNature`：**源自身缺陷**（缺 `#include <stdint.h>`），非平台不匹配；禁 `-include` 掩盖。classifier v2.3 `ALLOWED`/`LOW_SIGNAL`。
- **文件清单与读取**：8 件全部 ✅已读。`01-frozen/{classification-1.json, classifier-input.json, frozen-inputs.md}`；`job-00-source-buildability-linux/{comparison_manifest.json, input_profile.json, job-id.txt, metadata.json, returned-evidence/{evaluation_report.json, evidence-source.json}}`。**缺**：`result.md`（应交未交）；`evaluator_manifest.json` 未发生。
- **版本关联**：源预检 job `eval-20261010-052315-ededa846`（`gcc -std=gnu11 -DTEST strnsubst.c -o program`）。
- **证据事实**：编译器原文 `strnsubst.c:75:34: error: 'uintptr_t' undeclared`，compiler note 指向补 `#include <stdint.h>`；job-00 `runVerdict=blocked`、code/behavior `inconclusive`、target preflight `SKIPPED`、`coverageRatio=0.0`。
- **自审**：空集（未发生）。
- **失败/重提**：仅 job-00；无重提。
- **归因**：**源已有缺陷**（记录准确，未用 `-include` 掩盖）。

## D2-179 — c-to-ruby / enumdesktopsa_hack.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `enumdesktopsa_hack.c, 25, 11DD…484C`。item `SOURCE_NOT_BUILDABLE`/`SOURCE_PRECHECK_FAILED`/`DONE`、`requests=0`、`codeRevisions=0`。classifier v2.4 `ALLOWED`/`REVIEW_SENSITIVE`。
- **文件清单与读取**：23 件全部 ✅已读。`01-frozen/` 3 件；`job-00-source-buildability`（6 配置＋4 evidence）；`job-00b-relaxed-implicit-decl`（6 配置＋4 evidence）。**缺**：`result.md`（应交未交）；`evaluator_manifest.json` 未发生。`evidence-source.json` 两件 ⚠️截断。
- **版本关联**：job-00 `eval-20261011-045311-56a7132e`（item/frozen 一致）；**job-00b 真实 id `eval-20261011-045411-7555050c` 仅存在于 `job-00b/job-id.txt`，item 与 frozen 均未登记**。
- **证据事实**：job-00 `build failed/1`，stderr 原文 `enumdesktopsa_hack.c:14:3: error: implicit declaration of function 'decrypt_payload'`（stdout 空）；job-00b 加 `-Wno-error=implicit-function-declaration` 后编译通过、链接报 `undefined reference to 'decrypt_payload'` ⇒ 符号确缺，非严格性假象。两 job `evidence-target.json` 均 `{"detail":"evidence_not_found"}`；`runVerdict=blocked`、`code/behaviorVerdict=inconclusive`、`preflight/cleanup=PASSED`、`clean`、`READY`、`comparisonRef=null`。
- **自审**：空集（无目标）。**失败/重提**：job-00 原命令失败＋job-00b 单标志隔离实验失败（保留，未改写）。
- **未定/错误建议**：**同一 stderr 还含未被 frozen 记录的源侧缺陷** `warning: 'free' called on unallocated object 'my_payload' [-Wfree-nonheap-object]`（L26）；**工具链不一致**：frozen 写「GCC 14 默认升级为 error」，job-00b 实测 stderr 路径为 `gcc/x86_64-w64-mingw32/16.1.0`（msys64/ucrt64）。
- **归因**：源已有（模板 PoC 未实现 `decrypt_payload`、`free` 非堆对象告警）；装置（job-00b id 未登记、工具链版本记录不一致）。

## D2-180 — c-to-ruby / rc4_decrypt_cli.c（CONVERTED / CLOSED / DONE，matched after 2 轮修复）★用量不自洽

- **身份**：manifest `rc4_decrypt_cli.c, 83, 528D…D679A`。item `CONVERTED`/`CLOSED`/`DONE`；`packagingGap`：`WjCryptLib_Rc4.h/.c` 由旧 dataset 还原；`finalTargetSha256=26c4c631…fd20`；`codeRevisions=3`、`selfRepairRounds=1`、`postEvalRepairRounds=1`、`requests=5`（item 合计 prompt 14347/completion 13008/reasoning 5555）。classifier v2.4 `ALLOWED`/`REVIEW_SIDE_EFFECTS`。
- **文件清单与读取**：48 件全部 ✅已读。`01-frozen/` 2 件（**✖缺 `frozen-inputs.md`**）；`02-conversion/{request.system.txt, repair.system.txt, repair2.system.txt}`（**无 `target.gen.model.json`/`target.self-repair-*.model.json` ⇒ 生成正文与原始响应缺失**）；`03-self-review/{review.system.txt, self-review-1.json, self-review-1.model.json}`（model.json **仅元数据**：`requestSha256=b0229b99…`、`rawResponseSha256=7eaabda5…`、usage、verdict）；`job-00` 10 件、`job-01` 14 件、`job-02` 14 件；`result.md`、`evaluator_manifest.json`。`job-00` **无 `comparison.json`/`evaluation_report.md`**（其 `comparisonRef` 指向未回传件）。`evidence-*.json`/`evaluation_report.json`/`comparison.json` 单行超长 ⚠️截断（job-01/job-02 的 `comparison.json` <2000 已全读）。
- **版本关联**：job-00 `eval-20261011-045639-ed953852`；job-01 `eval-20261011-050139-1e25c337`（metadata targetHash `9f8d3349…`＝失败版）；job-02 `eval-20261011-050629-0e00db17`（targetHash `26c4c631…`＝final）。两套哈希语义：metadata 的 `sourceHash/targetHash`＝文件 sha256；evidence `baselineReference.artifactHash`＝封装哈希（job-00 `461437d8…`、job-01 `74cd36f8…`、job-02 `76203aab…`；source bundle `757ab0e7…` 三 job 恒定）。
- **证据事实**：job-00 为 placeholder 双侧跑（target stdout `D2-180 placeholder\n`，`partial-runnable`/`failed`/`mismatched`）。job-01 **mismatched**：`comparison.json` diffs＝`execution.exitCode` 0→1（critical，exact-exit-code）、`stream.normalizedText` "Plaintext"→""（major）、`stream.digest`（major）；target stderr 原文 `.../target.rb:113:in 'hex_decode': undefined method 'bytesize' for nil:NilClass (NoMethodError)`。job-02 **matched**：`diffs=[]`，两侧 build `completed/0`（`Syntax OK\n`）、exec `completed/0`、stdout digest 均 `0707c5d9…`（9 B `Plaintext`）、stderr 空；cleanup PASSED/clean/READY。
- **自审**：`self-review-1.json` 裁决 `REPAIR-RECOMMENDED`，8 条（scope=冻结 argv `["4b6579","bbf316e8d940af0ad3"]`→stdout `Plaintext`）：① `argv.length != 3` argc 差一，`conversion-introduced`，risk **High**（“deterministic failure on the exact frozen input”）；② KSA/S-init/swap/drop 无误；③ Rc4Xor 字节流无误；④ `hex_decode` 边界与错误码无误；⑤ `$stdout.write(...pack("C*"))` 不加换行无误；⑥ 校验顺序与文案无误；⑦ `prog` 回退条件直译失真，`conversion-introduced`，Low（仅 usage 文本）；⑧ 无固定输出/无桩。**修订链**：self-repair-1（`!=3`→`!=2`、`prog`→`$PROGRAM_NAME`，2 行）→ job-01 mismatched（ARGV 下标基数）→ eval-repair-1（`argv[1]/argv[2]`→`argv[0]/argv[1]`，2 行）→ job-02 matched。
- **失败/重提**：3 个 job（00 占位 / 01 真实 mismatch / 02 matched）；两份修复提示词保留含 job-01 反例原文。
- **未定/错误建议**：**item 用量与 result.md 不自洽**——item `requests=5`（14347/13008/5555），`result.md` 只列 4 次调用（合计 12351/11273/5248）⇒ 多 1 次未登记请求。**`request.system.txt:22` 自带错误口径**「参数个数不等于 3（不含程序名）⇒ usage」，与源 `argc!=3`（＝2 个用户参数）自相矛盾，很可能是本次 off-by-one 的直接诱因。
- **归因**：转换引入（argc 守卫差一＋ARGV 下标基数，均被第三方反例坐实并最小修复）；装置（占位比较、只哈希 model.json、用量聚合不一致、提示词错误口径）。

---

## 组末说明（D2-161..180，20/20 编号位全部存在）

- 本组 20 个编号位**全部在 manifest 与磁盘存在**（161-180 无缺号）。
- 现存文件合计：161-166 共 52；167-173 共 155；174 27；175 13；176 25；177 29；178 8；179 23；180 48 ⇒ **380 件**（含大量重复结构件）。**已逐件读取**；被读取工具 2000 字符/行上限截断的件按项登记为 ⚠️截断。
- 总去向（21 世纪口径，不合成成功率）：`CONVERTED` 5（174 matched、176 matched、177 matched、180 matched、179 除外——179 为 SOURCE_NOT_BUILDABLE）；`SOURCE_NOT_BUILDABLE` 11（162/163/164/165/166/168/170/171/172/173/178/179 中扣 161）；`SOURCE_DEPENDENCY_GAP` 1（161）；`WAITING/DRIVER_NOT_VIABLE` 3（167/169/175）。**未发生转换 = 161-173、175、178、179（15 项，0 模型调用）**。
- 归因：转换引入仅见于已转换项（176 未知选项诊断未修、177 字符/字节长度已修、180 argc/ARGV 已修）；其余为源已有/环境/装置。
- 交付完整性：本组多项目缺 `result.md`（161-173、175、179 等），部分缺 `frozen-inputs.md`（176、180）；详见 [harness-c-findings.md](harness-c-findings.md) A/B 组。

<!-- CASES01-ANCHOR: GROUP-COMPLETE -->

