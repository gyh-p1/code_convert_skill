# harness-A 逐项记录 04（D2-068 … D2-080 区段）

> 覆盖：D2-068 … D2-080（13 个编号，其中 D2-026 不在本区段）。D2-068/069 待追加；D2-076/077/078 目录缺失；其余为本会话首读记录。记号同 cases-01。

## D2-070 .. D2-075 / cpp-to-c（NEW，均 0 模型调用、无 target/result.md）

实际目录：`../../cpp-to-c/D2-07N-cpp-*.cpp/`。每项 `01-frozen/`（`frozen-inputs.md`、`classifier-input.json`、`classification-1.json`）齐全；`04-evaluation/job-00*` 及 `returned-evidence/` 存在；**无 02-conversion/03-self-review/result.md/evaluator_manifest.json**。

- **D2-070 AtomBombing.cpp（1519 行，超 700 计划上限）**：分类 v2.4 `REVIEW_SENSITIVE`/ALLOWED。job-00 `eval-20261011-054318-eb6cb709`：build **failed/1**，诊断 `AtomBombing.cpp:6:10: fatal error: ..\Release\AtomBombingShellcode.h: No such file or directory`（引号包含=项目伴随头，全库 0 命中）⇒ **SOURCE_DEPENDENCY_GAP**、lifecycle DONE、0 调用。job `jobStatus=COMPLETED` 但 `runVerdict=blocked`/`codeVerdict=inconclusive`、target preflight SKIPPED、`comparison.json` 无（本次未读该 job 的 comparison；evidence-target.json = `{"detail":"evidence_not_found"}`）、源 build stderr 227B 原文、cleanup PASSED/clean。item json 记 `phase=SOURCE_PRECHECK_FAILED`、`lifecycle=DONE`。
- **D2-071 bcd.cpp（842 行）**：v2.4 `REVIEW_SIDE_EFFECTS`/ALLOWED。job-00 `eval-20261011-054449-8457c62f`：build failed/1，缺 Process Hacker 头 `ph.h`（`bcd.h`/`mapldr.h`）⇒ **SOURCE_DEPENDENCY_GAP**、0 调用；只构建未执行。
- **D2-072 WnfCallbackInjection.cpp（446 行）**：v2.4 `REVIEW_SENSITIVE`/ALLOWED。**两实验**：A `eval-20261011-054554-4206ca8a` 加 `-DUNICODE -D_UNICODE` 前 build failed/1（`cannot convert 'const wchar_t*' to 'LPCSTR'`，属**契约缺陷**）；B `eval-20261011-054653-c5ee41a3` 加分支宏后 **build completed/0**。判定 **ORACLE_NOT_FREEZABLE**（源 stdout 含 PID 与 ASLR 指针地址，仅 `timestamps/temporary-paths/ephemeral-ports` 消噪、无法另冻 argv）⇒ 冻结阶段停止、**0 模型调用**、lifecycle **PARTIAL**、phase `CLOSED_ORACLE_NOT_FREEZABLE`。
  - **关键异常（原件支持）**：`job-00b-unicode-macro` 的 `evaluation_report.json` 记 `jobPhase=FINISHED`、**source+target 两侧 preflight PASSED、两侧 execution performed**、`behaviorVerdict=mismatched`、`codeVerdict=failed`、`comparisonRef=comparison/result.json`；`evidence-target.json`（target=c、build completed/0 1305ms、exec completed/0、**stdout 空**）存在。而项记录明示 target 为 **placeholder**（metadata：`target/target.c (placeholder)`、targetHash `placeholder-precheck`）、未生成目标、0 模型调用。⇒ 该 mismatched 是**占位 target 的比较**，非转换结论；项未计入失败是对的，但 job 目录保留可误读的 comparisonRef/behaviorVerdict。**`comparison/result.json` 未落盘**（引用件缺失）。同 job-00（A）target preflight SKIPPED。
- **D2-073 attack_chain.cpp（387 行）**：v2.4 `REVIEW_SENSITIVE`/ALLOWED。job-00 `eval-20261011-054849-9259fd78`：build failed/1，三类 C++ 硬错误——L176 窄 `std::string` + `WCHAR[260]` 类型不匹配；L217/L263 `xorEncryptDecrypt` 先用后定义（L363 才定义、无前置声明；C++ 无隐式声明）⇒ **SOURCE_NOT_BUILDABLE**（源码自身缺陷，任何编译标志无法补齐）、0 调用、只构建未执行。
- **D2-074 Exfiltration.cpp（436 行）**：分类 v2.4 **BLOCKED / `public_network_unverified`**，命中 `network_targets[1] = {"value":":","line":459,"scope":"hostname"}`；frozen 与 item 均记 L459 实为 `std::cout` 里 JSON 字段分隔冒号，唯一网络地址是 L82 `127.0.0.1`（loopback）⇒ **分类器误判**，与 D2-055 同类。处置：不手改分类 JSON、不绕过；lifecycle **WAITING**、phase `CLASSIFIER_BLOCKED`、**未预检/未转换/0 调用**；恢复条件=隔离证据后重分类或分类器修正启发式。附注：即便解除，源依赖 Crypto++（全库 0 命中）预计仍 `SOURCE_DEPENDENCY_GAP`。
- **D2-075 Movement.cpp（418 行）**：v2.4 `REVIEW_NETWORK`/ALLOWED。两实验：A `eval-20261011-055439-4d197ddd`（带 `-DUNICODE`）失败含窄/宽不匹配 + `count_if` 未声明；B `eval-20261011-055651-903e4810`（去宏）窄/宽错误消失、仅剩 6 处 `'count_if' is not a member of 'std'`（L344/345/346/430/431/432：用 `std::count_if` 无 `#include <algorithm>`）⇒ **契约修正（去 UNICODE 宏）+ 源码自身缺陷** ⇒ **SOURCE_NOT_BUILDABLE**、0 调用、只构建未执行。

- 归因：A 的窄/宽与 UNICODE 宏=**构建契约**（装置/契约层，非源缺陷，已在 B 分离）；`xorEncryptDecrypt` 先用后定义、缺 `<algorithm>`=**源已有**；缺伴随/第三方头=**源侧依赖缺口**（非转换失败）；D2-074 BLOCKED=**分类器误判/装置**；D2-072 job-00b 的 mismatched=**装置（占位 target）**。
- 知识候选（当前契约对照）：① 可构建性只由编译器诊断定案（D2-075 的 A/B 分离实验实证；[evaluation-readiness §1.1](../../../../references/framework/evaluation-readiness-contract.md) 与 [build-prerequisites](../../../../references/workflow/build-prerequisites.md) 已覆盖原则）；② `-DUNICODE/-D_UNICODE` 等分支宏属构建契约，不得据此判源不可构建（同上）；③ 源预检 job 不得携带可编译运行的占位 target，或须显式标注（[evaluation-readiness §1.3/§5](../../../../references/framework/evaluation-readiness-contract.md) 方向已覆盖“不造 target 补预检”“空输出 matched 不采信”）；④ `ORACLE_NOT_FREEZABLE` 的完整出处（frozen 引用 “§10.16”“§10.15”）在本副本未定位到规则真源，属**待核**；⑤ 分类器 hostname 误判需规则细化（见 findings §3.5）。
- 优化：占位 target 隔离；`comparisonRef` 与 evidence 同步取回；把 `-DUNICODE` 类契约修正作为独立 `sourceBuild` 变体登记（现行 [task-state §1](../../../../references/framework/task-state-contract.md) 变体机制覆盖）。
- 未知：各 job 单行件 2000 字符后的 diff/cleanup 尾部；已删源码正文；`comparison.json` 在 D2-070/071/073/075 的实际内容（本次未逐件读取其 `returned-evidence/comparison.json`，若存在）。

## D2-076 / D2-077 / D2-078 / cpp-to-csharp（NEW）——目录缺失

- `../../cpp-to-csharp/D2-076-cpp-edrsilencer.cpp/`、`D2-077-cpp-xbin.cpp/`、`D2-078-cpp-lsass_clone_dump.cpp/`：**目录未发现**（glob `cpp-to-csharp/D2-076*`/`D2-077*`/`D2-078*` 均 0 命中）。
- 仅存 `../items/D2-076..078.json`：`FROZEN`/`NOT_STARTED`/`WAITING`/`blockingReasons=["BLOCKED_ENV"]`/`blockerRef=../../batch/platform-blocker-csharp-target.md`；`dispositionNote` 明示 “no freeze job was run because the defect is already characterised. **0 model calls**”；verdicts 全 UNVERIFIED。
- 异常：`disposition=FROZEN` 无任何冻结件；blockerRef 头部已声明 2026-10-11 修复，item 仍 WAITING/BLOCKED_ENV（stale）。归因=装置/记录；无转换事实可判。

## D2-079 / cpp-to-csharp / ascii.cc（NEW，Abseil 翻译单元）

- 实际目录 `../../cpp-to-csharp/D2-079-cpp-ascii.cc/`；共 12 件（01-frozen 3、job-00 8、无 02/03/result/manifest）。
- `frozen-inputs.md`：source `ascii.cc`（无 main，Abseil 库翻译单元）、sourceOs windows（候选未定案）；分类 `LOW_SIGNAL`/ALLOWED/null（v2.3）；job `eval-20261010-044920-7f22e2a1`：build **failed/1**、`ascii.cc:15:10: fatal error: absl/strings/ascii.h: No such file or directory` ⇒ **SOURCE_DEPENDENCY_GAP**、跳过、不改源/不放宽命令、**0 模型调用**、lifecycle DONE、目标 UNVERIFIED。
- 其他件：`classifier-input.json`（source/ascii.cc，hash 一致）、`classification-1.json`（v2.3，`441b4d50…`，`inputManifestSha256 2a207744…`）、`metadata.json`（`compile-only probe; nothing is executed`、sourceHash 一致、targetHash `placeholder-precheck`）、`input_profile.json`（argv[]/stdin null/timeout 30/dims output）、`comparison_manifest.json`（source `g++ -std=c++17 -c ascii.cc -o out.o`、target `dotnet build -c Release`、runCommand 两侧 `python run_case.py`——**注意源树无驱动但 manifest 仍引 run_case.py**）、`job-id.txt`、`controller.log`（created/finished 两行）、`returned-evidence/evaluation_report.json`（jobStatus COMPLETED、源 build failed/1、target preflight SKIPPED、runVerdict blocked、coverage 0）、`returned-evidence/evidence-source.json`（build failed/1、stderr 182B 原文、execution blocked）`read(截断>2000)`、`returned-evidence/comparison.json` = `{"detail":"comparison_not_found"}`。
- 归因=源侧依赖缺口（非源不可构建、非转换失败）；无请求/响应/自审/job-01。未知：截断尾部、源正文。

## D2-080 / cpp-to-csharp / charconv_bigint.cc（NEW，Abseil 翻译单元）

- 结构与 D2-079 同型：`frozen-inputs.md` 记 job `eval-20261010-045012-f4b36f9c` build failed/1、`charconv_bigint.cc:15:10: fatal error: absl/strings/internal/charconv_bigint.h: No such file or directory` ⇒ **SOURCE_DEPENDENCY_GAP**、0 调用、DONE。
- `classification-1.json` v2.3 `LOW_SIGNAL`/ALLOWED（`inputManifestSha256 7366d7b3…`）；`metadata.json` 同 placeholder-precheck；`comparison_manifest.json` source `g++ -std=c++17 -c charconv_bigint.cc -o out.o`、target `dotnet build -c Release`；`returned-evidence/evaluation_report.json` COMPLETED/build failed/1/target SKIPPED/blocked；`comparison.json` = `comparison_not_found`。
- 归因/未知同 D2-079。

## D2-068 / D2-069

> 待追加（python-to-powershell 组回报后）。
