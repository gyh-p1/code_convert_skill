# step-04：多系统 POSIX→Windows 文件系统方向拓展批次

> 状态：已完成（4 例依次执行完毕；例 1 stest、例 2 realpath、例 3 pwd 编译 PASS 已 CLOSED；例 4 du 源基线 FAILED_COMPILE→目标跳过，为预记失败类别数据点，已 CLOSED）
> 归属：阶段 [index.md](index.md) · [阶段方案 step 5](阶段方案.md)
> 决策：用户 2026-09-28 拍板——「4 例都采用，然后依次执行转换和评估，现在已经证明流程顺利了，可以不必一例一例尝试了」。故本批不再逐例征询执行形态与是否评估。

## 维度与边界

- **新增维度**：系统方向 = **POSIX/Unix → Windows**，filesystem 子域；语言方向仍 C→C++。这是"每次只开一维"下的**一维（多系统）内的 4 份真实样例**，不是同时铺多语言/多战术三轴。
- **首个真实消费者**：`skills/systems/posix-windows-filesystem`（此前为未验证初稿）——本批为它提供首批真实源以坐实或按失败纠错。语言方向沿用 `skills/directions/c-to-cpp`（含 header-macro、type-abi 专题）。
- **为何这 4 份**：均为**单 OS(POSIX-only) 真实 C 源、无 `_WIN32` 分支**（无目标分支泄漏，规避 uhttpd 的缺陷），许可清晰，物理行 ≤~900，只读文件系统行为、无外联/无 exec/无恶意。经候选筛选核验后选入。

## 选入源（已冻结，`docs/test/sources/`）

| 源目录 | 文件/行数 | 许可 | commit/tag | 主要 POSIX-fs 表面 | 备注 |
|---|---|---|---|---|---|
| `dmenu-stest` | `stest.c` 109 (+`arg.h` 49) | MIT/X | `61e0072c…3680c0` | `stat`/`lstat`/`access`(F_OK/R_OK/W_OK/X_OK)/`opendir`/`readdir`/`getline`/`S_IS*` | **最干净、API 面最丰富 → 首例** |
| `freebsd-realpath` | `realpath.c` 82 | BSD-3 | tag `release/14.2.0`=`89042d64…` | `realpath` ↔ `GetFullPathName`/`_fullpath` | 表面薄；含 `__dead2` 一处 |
| `freebsd-pwd` | `pwd.c` 123 | BSD-3 | 同上 | `getcwd`/`getenv(PWD)`/`st_dev`+`st_ino` 身份 | 含 `__dead2` 一处 |
| `freebsd-du` | `du.c` 561 | BSD-3 | 同上 | `fts_*` 递归遍历/`st_blocks`/`fnmatch` | ⚠️ 见下"预期硬数据点" |

各源 sha256、完整 API 清单、安全边界见对应 `source.md`。

## ⚠️ 已记录的源画像风险（先记预期，再取真实证据，不倒填）

- **`du.c` 预期为硬/失败数据点**：依赖 `fts`、`libutil`(`humanize_number`/`getbsize`/`expand_number`)、`SIGINFO`、`st_flags & UF_NODUMP`、`sys/queue`、`getopt_long` 等 —— 其中 libutil/SIGINFO/UF_NODUMP **Linux glibc 与 MinGW 均缺**。故其 **C 源侧基线在 Linux VM 上预期编不过**，Windows 目标侧近乎完全重写。按阶段方案 step 5，其价值是"失败类别 → Skill 规则"，不是干净通过。**已由真实证据坐实**（job-01 `eval-20260928-073929-e89be213`）：源基线 `FAILED_COMPILE`（首个硬阻断 `du.c:55:10 libutil.h: No such file or directory`），据双 runner 定序目标侧被跳过、无目标 build 证据；syntaxVerdict=INCONCLUSIVE。不改源、不放松命令、不伪造目标通过。
- **`realpath.c`/`pwd.c`**：`__dead2`(BSD `<sys/cdefs.h>`，glibc 不定义) 一处会影响 Linux 源侧基线；`<err.h>` 在 glibc 存在。属源可移植性归因，源冻结不改。
- **`dmenu-stest`**：纯 POSIX，源侧基线在 Linux 预期干净；作首例。

## 执行形态与顺序

- **跨 OS 双侧 build**（区别于 fe 的同 OS）：源侧 = C 在 **Linux VM**（`linux-eval`, `192.168.195.129`）作对照基线；目标侧 = 转换后的 C++ 在 **Windows VM**（`windows-eval`, `192.168.195.128`）。本阶段只把 build 证据计入指标，execution/comparison 仅信息记录、不评功能、不设 oracle。
- **闭环**：每例 `FROZEN→GENERATED(.env 模型)→SELF_REVIEWED→(SELF_REPAIRED≤2)→EVALUATION_READY→EVALUATED→(REPAIR_AFTER_EVAL≤2)→CLOSED`，双侧 capsule 直连 Controller `http://192.168.101.250:8443` 提交（见 [remote-controller-adapter](../../../references/adapter/controller/remote-controller-adapter.md)）。
- **顺序**：`stest`（最干净，先跑通形态）→ `realpath` → `pwd` → `du`（最难，放最后）。
- **落点**：各例 case 已按 step-05 迁至 `docs/test/dataset/c-to-cpp/<case-id>/`，run 产物仍按[交付契约 §2.2](../../../references/framework/delivery-handoff-contract.md)。原始 capsule/Controller 证据中的旧路径保留为历史快照。

## 逐例状态

| 顺序 | case | 源 | 状态 | jobId / 证据 |
|---|---|---|---|---|
| 1 | `stest-fs-posix-to-win` | `dmenu-stest` | **CLOSED**（编译 PASS；behaviorVerdict matched 仅信息） | job-02 `eval-20260928-053745-2a386af5`（目标 build exitCode=0）；job-01 `eval-20260928-053326-9a8ae00e` 源基线命令缺特性测试宏 FAILED，已修正、证据保留 |
| 2 | `realpath-fs-posix-to-win` | `freebsd-realpath` | **CLOSED**（编译 PASS；1 轮自修；behaviorVerdict mismatched 仅信息，属按设计跨 OS 路径文本差异） | job-01 `eval-20260928-060834-49b1a302`（目标 build exitCode=0/stderr 空；源基线 exitCode=0）；自审 REPAIR-RECOMMENDED→自修→复审 NO-REPAIR-IDENTIFIED |
| 3 | `pwd-fs-posix-to-win` | `freebsd-pwd` | **CLOSED**（编译 PASS；1 轮自修；behaviorVerdict mismatched 仅信息，属按设计跨 OS 路径文本差异） | job-01 `eval-20260928-064021-653f5ee9`（目标 build exitCode=0/stderr 空；源基线 exitCode=0）；自审 REPAIR-RECOMMENDED（声明顺序阻断点+st_ino 守卫）→自修→复审 NO-REPAIR-IDENTIFIED |
| 4 | `du-fs-posix-to-win` | `freebsd-du` | **CLOSED**（失败类别数据点：源基线 FAILED_COMPILE→目标跳过；2 轮自修预算用尽，1 项残留已登记；syntaxVerdict=INCONCLUSIVE，目标未构建） | job-01 `eval-20260928-073929-e89be213`（源 build failed/exitCode=1，`libutil.h: No such file or directory`；目标 execution.performed=false/SKIPPED；runVerdict=blocked） |

安全边界不变：loopback/无真实外联/可回滚快照；`executionApproved` 仅在实际向隔离 VM 提交后置 `true`；语法/行为结论只从 Controller 真实报告回填，不由自审臆造；凭据永不入库/入 zip/入日志；不在本机编译或运行。
