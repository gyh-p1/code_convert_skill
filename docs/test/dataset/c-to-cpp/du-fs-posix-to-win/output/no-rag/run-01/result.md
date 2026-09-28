# du POSIX->Windows filesystem 转换评估结果（run-01, no-rag）

- **案例**：`du-fs-posix-to-win`（step-04 多系统 POSIX→Windows filesystem 批次第 4 例，最大最复杂，源 561 行）
- **caseId**：`du-fs-posix-to-win-run-01`
- **jobId**：`eval-20260928-073929-e89be213`（真实远端 Controller 回传，jobStatus=COMPLETED）
- **本阶段口径**：最终交付编译质量阶段——只据 build 证据判语法结论；不设行为 oracle、不计功能正确率；Controller 的 `behaviorVerdict`/`codeVerdict` 仅供参考。

## 一句话结论

**源侧 C 对照基线在 plain-glibc Linux VM `FAILED_COMPILE`（首个硬阻断 `libutil.h` 缺失），据双 runner 定序目标侧构建被跳过、无目标 build 证据 —— 这与冻结 §2.1 的预记完全一致，本身即失败类别数据点。** 非转换缺陷；未改源、未放松命令到失真、未伪造目标通过。目标 C++ syntaxVerdict = **INCONCLUSIVE**（目标未构建，既非 PASS 亦非转换引入的 FAIL）。

## 真实回传证据（returned-evidence/）

| 维度 | 值（源自 evaluation_report.json / evidence-source.json） |
| --- | --- |
| jobStatus | `COMPLETED` |
| runVerdict | `blocked` |
| codeVerdict | `inconclusive` |
| behaviorVerdict | `inconclusive` |
| environment | `clean`（两侧 contaminated=no，runner 复位） |
| failure | `CODE_RESULT` / category `code`：Source build failed; baseline cannot be established. |
| evidenceCoverage | 0 applicable / 0 observed / 0 matched / 0 mismatched（0%） |

### 源侧（Linux x64, runner `linux-vm-agent-x64`, snapshot CC-Eval-Linux-8Lang-R7）

- build `status = failed`，`exitCode = 1`，`durationMs = 1057`
- 首个致命错误（stderr，144 bytes）：

  ```
  du.c:55:10: fatal error: libutil.h: No such file or directory
     55 | #include <libutil.h>
        |          ^~~~~~~~~~~
  compilation terminated.
  ```

- 编译命令（源码不改，仅命令行宏）：`cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__unused= du.c -o program`
- execution `status = blocked`（build failed，未启动执行）。
- 观测覆盖：output=blocked、filesystem/processes=not-applicable、registry/network=not-applicable（超出当前发布范围）。

### 目标侧（Windows x64, runner `windows-vm-agent-x64`, snapshot CC-Eval-Windows-8Lang-R7）

- `execution.performed = false`；preflight = SKIPPED、cleanup = SKIPPED；evidence bundle **not available**；`comparison_not_found`。
- 原因：Controller 双 runner 先建源基线，**源基线失败即不再构建目标侧**（dual-runner ordering）。故本例目标 C++ 未构建、无 build 证据。

## 为什么源基线在 glibc 上失败（BSD 专有面）

FreeBSD du 依赖一批 glibc/MinGW 上不存在或语义不同的接口，命令行宏无法补齐：

- `#include <libutil.h>` → `humanize_number` / `expand_number` / `getbsize`（**首个硬阻断**）
- `signal(SIGINFO, ...)`（BSD 专有信号）
- `st.st_flags & UF_NODUMP`（BSD inode flags，Linux `struct stat` 无 `st_flags`）
- `<fts.h>` FTS 遍历族、`<sys/queue.h>`、`<fnmatch.h>`、`getopt_long`、`DEV_BSIZE`、`EX_USAGE`

即使中和 `<sys/cdefs.h>` 属性宏（`-D__unused=`）并暴露 POSIX/BSD 符号（`-D_POSIX_C_SOURCE`/`-D_DEFAULT_SOURCE`），libutil/SIGINFO/UF_NODUMP/st_flags 仍不可得，故源基线预期且实测 `FAILED_COMPILE`。这是**源对 glibc 的可移植性事实**，非我方转换产物问题。

## 目标 C++ 稿状态（未被 Controller 构建，仅静态说明）

- run 根 `target.cpp` = `02-conversion/target.repair-2.cpp`（sha256 `cefe0aa7…`），经两轮自修，预算（≤2）已用尽。
- 自审轨迹：GENERATED → SELF_REVIEWED(REPAIR-RECOMMENDED，12 项) → SELF_REPAIRED r1 → 复审(REPAIR-RECOMMENDED，3 项) → SELF_REPAIRED r2 → 终审(REPAIR-RECOMMENDED，1 项残留)。
- **终审残留（已接受/已登记限制）**：round2 的 `fnmatch` 修复过度限制了首字符 `]` 的范围语义（形如 `[]-a]` 丢失范围匹配）。因自修预算用尽，如实记录，未强判 NO-REPAIR。
- 目标稿顶部保留“已知差异”块：fts→`<filesystem>`、SIGINFO 不安装、`-n`/UF_NODUMP no-op、`st_blocks` 缺失→按文件大小/512、硬链接去重移除、`-x` 仅按盘符、humanize 边角、目录尺寸→0、符号链接不跟随→0、路径编码差异、构建命令 `g++ -std=c++17 target.cpp -o program`。
- **重要**：因目标未被 Controller 构建，以上仅为静态设计说明，**未**取得目标 build 证据；不得据此声称目标可编译或行为一致。

## 对 Skill 的反哺（step-05 输入）

1. **可移植性预筛**：源码出现 `libutil.h`/`fts.h`/`SIGINFO`/`UF_NODUMP`/`st_flags`/`st_blocks` 即判定“非 plain-glibc 可移植”，应在冻结阶段预记源基线可能 `FAILED_COMPILE`。
2. **双 runner 定序后果**：源基线失败→目标跳过，属正常失败类别，评估不得视为流程错误、不得伪造目标通过。
3. **C→C++ 机械项**：`typedef long long off_t` 会与系统 `off_t` 冲突，应改用独立别名（`using du_off_t = long long`）。
4. **`std::filesystem` 语义**：`directory_iterator` 需显式 `follow_directory_symlink` 决策；目录尺寸/符号链接跟随策略需登记为平台差异。
5. **`fnmatch` 字符类边角**：首字符 `]`、范围 `[]-a]` 的手工替换易过度限制，属高风险改写点，应在 Skill 明列反例。

---

真实证据以 `04-evaluation/job-01-dual-build/returned-evidence/` 下的 JSON 为准；本 Markdown 为其派生视图。