# du：FreeBSD `du(1)` POSIX C → Windows C++（多系统 filesystem 子域，step-04 批次 4/4，预期硬数据点）

> 状态：CLOSED（step-04 批次第 4 例 = 最后一例）。**§2.1/§6 预记的"失败类别数据点"已由真实证据坐实**：job-01 `eval-20260928-073929-e89be213`（COMPLETED）——源侧 C11 基线在 plain-glibc Linux VM `FAILED_COMPILE`（首个硬阻断 `du.c:55:10 libutil.h: No such file or directory`），据双 runner 定序目标侧被跳过（`execution.performed=false`）、无目标 build 证据；runVerdict=blocked、syntaxVerdict=INCONCLUSIVE。目标 C++ 稿经 2 轮自修（预算用尽，1 项 fnmatch 残留已登记）。证据见 [run-01/result.md](output/no-rag/run-01/result.md) 与 [job-01-dual-build](output/no-rag/run-01/04-evaluation/job-01-dual-build/README.md)。冻结预记原文保留于 §2.1（不倒填）；全程不改源、不放松命令、不伪造目标通过。
> 归属阶段：[最终交付编译质量与 Skill 拓展](../../../../项目开发规范.md#当前开发阶段与退出条件) · 执行真源 [index](../../../../项目开发规范.md#当前开发阶段与退出条件) step-04 · 批次文档 [step-04](../../../../项目开发规范.md#当前开发阶段与退出条件)
> 共享源样例：`当前 run 的 source/ 冻结副本`（共享源快照已清理；冻结副本见当前 run 的 `source/` 目录）（自包含，仅系统头，无本地 `""` 头）
> 上游来源与许可：上游来源说明已清理；冻结副本见当前 run 的 `source/` 目录 与随附 BSD-3-Clause `COPYRIGHT.freebsd`
> 前序：批次前三例 [stest](../stest-fs-posix-to-win/case.md)、[realpath](../realpath-fs-posix-to-win/case.md)、[pwd](../pwd-fs-posix-to-win/case.md) 均已 CLOSED（跨 OS 双侧 build 真实 PASS）；本例复用同一形态与调度政策，但**源画像远重**。

## 1. 转换方向与标签（已确认）

- 源：C；按 **C11** 理解。**无平台 `#ifdef` 分支**（读+grep 确认无 `_WIN32`/`WIN32`/`windows.h`）。含大量 FreeBSD base 惯用法（`__unused`、`SIGINFO`、`UF_NODUMP`、`<libutil.h>`、`<sys/queue.h>`、`fts(3)`——见 §2）。
- 目标：C++；**C++17**。**做跨 OS 迁移**——POSIX/Linux → Windows。step-04「多系统 = POSIX→Windows，filesystem 子域」维度第 4 个（最后一个）真实消费者。
- 任务模式：单文件文本转换（561 物理行，批次中最大最复杂；**无伴随头**）。
- 系统方向 Skill：[`skills/systems/posix-windows-filesystem`](../../../../../skills/systems/posix-windows-filesystem/SKILL.md)——本例考**递归目录遍历 `fts(3)` ↔ `FindFirstFile`/`FindNextFile`**、块计量 `st_blocks`/`st_size`、硬链接去重 `(st_dev,st_ino)`、`fnmatch` 忽略掩码这一组在 Windows 无直接等价、须整体重写的表面。语言方向沿用 [`skills/directions/c-to-cpp`](../../../../../skills/directions/c-to-cpp/SKILL.md)（含 header-macro、type-abi 专题）。
- 场景：只读——递归遍历目录、累加块用量并打印；读环境变量 `BLOCKSIZE`；无网络、无文件写/删、无进程/命令执行。ATT&CK tactic/technique：`none`。RAG：关闭。
- 目标文件命名与落点：按[交付契约 §2.2](../../../../../references/framework/delivery-handoff-contract.md)。

## 2. POSIX→Windows filesystem 表面（本例真实考点）

`du.c` 依赖一片**远宽于前三例的 FreeBSD-base 表面**，其中多数在 Linux glibc 与 Windows/MinGW **均缺失**：

- **`<fts.h>` `fts_open`/`fts_read`/`fts_set`（递归遍历核心）**：Windows 无等价，须以 `FindFirstFile`/`FindNextFile`（或 `std::filesystem::recursive_directory_iterator`）整体重写；物理/逻辑遍历（`FTS_PHYSICAL`/`FTS_LOGICAL`/`FTS_COMFOLLOW`/`FTS_XDEV`）语义须自行维护。本例**核心映射边界**。
- **`<libutil.h>` `humanize_number`/`expand_number`/`getbsize`**：**BSD-only，glibc 无（需 libbsd）、MinGW 无**——目标侧须自备等价（人类可读单位换算、阈值解析、块大小）。
- **`signal(SIGINFO, …)` 与 `__unused`**：`SIGINFO` 是 **BSD 专有信号，Linux 与 Windows 均无**（Windows 更无 POSIX 信号语义）——目标侧须删除/保守化该交互式进度报告；`__unused` 是 BSD `<sys/cdefs.h>` 属性宏，两平台名义均无。
- **`st_flags & UF_NODUMP`（`-n` 忽略 nodump）**：BSD inode 标志，**Linux 与 Windows `struct stat` 均无 `st_flags`**——`-n` 在目标侧无等价语义，须保守处理（如置为 no-op 并注释登记为已知差异）。
- **`st_blocks`（块计量）**：Windows `struct stat` **无 `st_blocks`**——须以 `st_size` 近似或用 Win32 分配大小 API，属可观察数值差异边界。
- `<sys/queue.h>` `SLIST_*`、`<fnmatch.h>` `fnmatch`、`<getopt.h>` `getopt_long`、`DEV_BSIZE`、`howmany`、`EX_USAGE`（`<sysexits.h>`）、`<err.h>` `err`/`warn`/`warnx`/`errx`：glibc 可用性混杂，**MinGW 上大多缺失**（`getopt_long` 经 libmingwex 可用；`err`/`warn` 家族与 `fnmatch` 须自备；`sys/queue.h` 须自备或用 STL）。

这些是否成立、模型如何映射/重写，均由第三方 build 证据裁定；本 case **不预判"通过"，并已在 §2.1 预记预期失败面**。

### 2.1 预期硬/失败面（先记预期，再取真实证据，绝不倒填）

- **源侧 C 对照基线预期在 plain-glibc Linux VM 编不过**：`SIGINFO`（Linux 无此信号宏，`signal(SIGINFO,…)` 处 `SIGINFO` 未声明）、`UF_NODUMP` 与 `st_flags`（glibc `struct stat` 无）、`humanize_number`/`expand_number`/`getbsize`（glibc 无，须 libbsd 且改 include 路径——源冻结不改）为硬阻断。命令行特性测试宏只能暴露 POSIX 符号、中和 `__unused`，**无法补齐 BSD 专有信号/inode 标志/libutil**。故源基线预期 `FAILED_COMPILE`，属**源对 glibc 的可移植性事实（FreeBSD-ism）**，非转换缺陷。
- **双 runner 定序后果**：Controller 先建源侧基线，源侧失败则**不再构建目标侧**（stest job-01 已证该定序）。故本例**很可能拿不到目标 build 数据点**，回传即为"源基线 FAILED_COMPILE → 目标跳过"——这本身就是本例要记录的失败类别数据点，不因此改源、不伪造目标通过。
- 目标侧 C++ 即使被构建，也是一次近乎完整的重写（fts/libutil/SIGINFO/UF_NODUMP 全部重来），其可编译性以真实回传为准，不预判。

## 3. 编译/执行形态（已定 = 跨 OS 双侧 build，沿用 stest/realpath/pwd）

- **源侧（对照基线，POSIX/BSD）**：`cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__unused= du.c -o program` 在 **Linux VM `linux-eval`（`192.168.195.129`）**。见 §3.1；**预期失败**（§2.1）。
- **目标侧（转换后 C++）**：`g++ -std=c++17 target.cpp -o program` 在 **Windows VM `windows-eval`（`192.168.195.128`）** MinGW/UCRT64。目标侧不假定源侧命令行宏，须在 C++ 内自足所有符号。
- 源侧在 Linux、目标侧在 Windows，用以区分"POSIX/BSD 源本身能否编（基线）"与"转换到 Windows C++ 引入/暴露的编译结果"。
- **本阶段只读 build 证据**：capsule 的运行仅为迁就双侧执行契约；run/behavior 不计入功能率、不设行为 oracle。
- **运行边界（获批隔离 VM 内）**：liveness 驱动以固定只读参数启动（对 case 私有临时目录做 `du -s .` 语义的遍历+汇总打印后退出）；不联网、不执行外部命令、不读敏感文件、不写/删文件。结束即销毁临时件。

### 3.1 源侧 build 命令的平台宏说明（不改源，仅命令行提供）

- `du.c` 是 **FreeBSD base-system** 代码，其自然参考平台是 FreeBSD，非 Linux glibc。以**命令行宏**在源不变前提下尽量迁就（沿用 stest/realpath/pwd 的特性测试宏教训）：
  1. **POSIX 特性测试宏 `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE`**：暴露 glibc 在 strict `-std=c11`（`__STRICT_ANSI__`）下隐藏的 `getcwd`/`getopt_long`/`err` 等 POSIX/BSD 符号。
  2. **`__unused`（FreeBSD `<sys/cdefs.h>` 属性宏，glibc 不定义）以 `-D__unused=` 置空**：仅是"未使用"属性提示，置空不改行为与可编译性。
- **归因与预期**：以上命令行宏**无法**补齐 `SIGINFO`/`UF_NODUMP`/`st_flags`/`humanize_number`/`expand_number`/`getbsize`（BSD 专有信号、inode 标志、libutil），故源基线**预期仍失败**（§2.1）。这是源对 glibc 的可移植性事实，**不编辑源快照**、不为凑基线通过而改源或改命令到失真。
- 若源侧基线如预期失败，按 stest/realpath/pwd 先例：**如实记录真实回传**，作失败类别数据点，不倒填、不改目标产物、不伪造目标通过。

## 4. 调度与模型输出约束

- 模型、API 地址、温度由根目录 `.env` 提供；密钥不写入任何交付文件、manifest 或请求正文。
- **提交前先验证 `.env` 模型可用**；不可用则如实记录、按相同输入最多重试一次，不换模型、不伪造自评或代写模型产物。
- 模型请求上下文：C→C++ 方向 + [header-macro 规则](../../../../../skills/directions/c-to-cpp/references/header-macro.md) + [type-abi 专题](../../../../../skills/directions/c-to-cpp/references/type-abi.md) + [posix-windows-filesystem 系统方向](../../../../../skills/systems/posix-windows-filesystem/SKILL.md)。本例 561 行，接近但未超放宽后的 ~900 物理行上限，仍按单文件转换；不注入 long-file 工作流。
- 输出约束：完整单文件 `target.cpp`，无 Markdown fence/解释/省略号；尽力保留 du(1) 可观察行为（选项集、递归遍历累加、`-h`/`-k`/`-m`/`-g` 单位、`-s`/`-a`/`-d` 深度、`-c` 总计、`-I` 忽略掩码、`-x` 不跨设备、硬链接去重、`usage()` 到 stderr 并 `exit(EX_USAGE)`）；平台缺失能力（`SIGINFO` 进度、`UF_NODUMP`、`st_blocks`）按保守、可观察行为尽量一致的方式处理并在文件顶部注释登记为已知差异；不新增进程执行/外联/文件写/权限；不把未编译结果说成通过或等价。

## 5. 授权与落点

- 执行形态按**本项目既定的双侧执行授权**：在获批隔离 VM 做跨 OS 双侧构建+运行，不再逐例询问形态。本 case 逐例安全前提已确认——源为低风险、纯只读遍历+汇总打印、无网络/无 exec/无文件写删；隔离/工具链/清理随本 case 核对，确认不扩展到其它样例。`executionApproved` 仅在实际向隔离 VM 提交 capsule 后置 `true`。
- 产物落点按[交付契约 §2.2](../../../../../references/framework/delivery-handoff-contract.md)：`01-frozen/` + `02-conversion/target.gen.*` + `03-self-review/` + `04-evaluation/job-<NN>-<用途>/`；run 根 `target.cpp` = 最终交付版本。
- 无匹配契约/授权时停在文本交付并标 `UNVERIFIED`，不在本机编译或运行。

## 6. 非目标与数据点用途

- 不在本机编译、运行、调用构建脚本或触发代码生成。
- 不评功能正确率、不设/不比对行为 oracle；build 通过不说成功能或安全正确。
- **不为凑"通过"改源、放松命令到失真，或把修订稿成功回写成原始生成稿成功。** 本例的**预期结果是失败类别数据点**（源基线 FreeBSD-ism 失败、目标可能因定序未被构建，或目标重写不完整而失败），如实记录后反哺 step-05 更新 `posix-windows-filesystem`（fts→Find* 重写、libutil 自备、SIGINFO/UF_NODUMP/st_blocks 无等价的保守处理与已知差异登记）与 `c-to-cpp`。
