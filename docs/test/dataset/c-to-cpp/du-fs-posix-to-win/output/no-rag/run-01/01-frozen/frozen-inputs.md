# du · run-01 · 配置模型转换输入记录（冻结）

> 状态：FROZEN；`.env` 配置模型生成目标；step-04 多系统 POSIX→Windows filesystem 批次第 4 例（最后一例）。本 run 属当前编译质量阶段，只把 **build 证据**计入指标，不评功能、不设行为 oracle。**本例冻结时即预记为预期硬/失败类数据点**（见 §2.1）。
> 归属：[case.md](../../../../case.md) · 阶段 [index step-04](../../../../../../../../项目开发规范.md#当前开发阶段与退出条件) · 批次 [step-04](../../../../../../../../项目开发规范.md#当前开发阶段与退出条件)
> 前序：批次前三例 [stest run-01](../../../../../stest-fs-posix-to-win/output/no-rag/run-01/result.md)、[realpath run-01](../../../../../realpath-fs-posix-to-win/output/no-rag/run-01/result.md)、[pwd run-01](../../../../../pwd-fs-posix-to-win/output/no-rag/run-01/result.md) 均已 CLOSED（跨 OS 双侧 build 真实 PASS）。

## 1. 输入与目标

- 源文件：`当前 run 的 source/ 冻结副本`（561 行）。**自包含，无伴随本地头**（仅系统头）。
- 源快照：FreeBSD `usr.bin/du/du.c`，tag `release/14.2.0` = commit `89042d64c83ca92d90bd3d161eebc353d5edb3c6`；完整性以 sha256 固定：`du.c`=`d7ba9521006f876879a8e181c13547cf385184aa620fe7600518fd566197ae41`。
- 源语言/系统：C（**C11**）；POSIX/BSD，无平台 `#ifdef` 分支；含大量 FreeBSD base 惯用法（`__unused`/`SIGINFO`/`UF_NODUMP`/`<libutil.h>`/`<sys/queue.h>`/`fts(3)`）。
- 目标语言/系统：C++（**C++17**）；**跨 OS 迁移 POSIX/Linux → Windows**。
- 任务模式：单文件文本转换（批次中最大最复杂，561 行）。
- 场景：只读——递归遍历目录、累加块用量并打印（`fts_*`/`stat`/`fnmatch`/`getenv(BLOCKSIZE)`）；无网络、无文件写/删、无进程/命令执行。ATT&CK：`none`。RAG：**关闭**。

## 2. 编译/执行形态（决定 = 跨 OS 双侧 build，沿用 stest/realpath/pwd）

- **源侧在 Linux VM、目标侧在 Windows VM**，隔离"POSIX/BSD 源本身能否编"与"转换到 Windows C++ 引入/暴露的结果"。
- 本 case 无需补写入口：`du.c` 自带 `main`，两侧均可直接链接为可执行 `program`。
- **本阶段只读 build 证据**：capsule 的运行仅迁就双侧执行契约；run/behavior 结果不计入功能率，本 run 不设行为 oracle。
- **运行边界（获批隔离 VM 内）**：liveness 驱动以固定只读参数启动（对 workspace 私有临时目录做 `du -s .` 语义遍历+汇总后退出）；不联网、不执行外部命令、不读敏感文件、不写/删文件。结束即销毁临时件。

### 2.1 预期硬/失败面（先记预期，绝不倒填）

- **源侧 C 基线预期在 plain-glibc Linux VM `FAILED_COMPILE`**：`SIGINFO`（Linux 无该信号宏）、`UF_NODUMP`/`st_flags`（glibc `struct stat` 无）、`humanize_number`/`expand_number`/`getbsize`（glibc 无 libutil，须 libbsd 且改 include——源冻结不改）为硬阻断。命令行宏只能暴露 POSIX 符号并中和 `__unused`，**无法补齐 BSD 专有信号/inode 标志/libutil**。属源对 glibc 的可移植性事实，非转换缺陷。
- **双 runner 定序后果**：Controller 先建源侧基线，源侧失败则**不再构建目标侧**。故本例很可能拿不到目标 build 数据点；回传即"源基线 FAILED_COMPILE → 目标跳过"，本身即失败类别数据点。**不改源、不放松命令到失真、不伪造目标通过**。
- 目标侧 C++ 即使被构建也是近乎完整重写，其可编译性以真实回传为准，不预判。

## 3. 目标工具链（冻结，具体版本以实际 Controller 为准）

- 源侧（对照基线，按 C，POSIX/BSD）：`cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__unused= du.c -o program` 在 **Linux VM `linux-eval`（`192.168.195.129`）**。平台宏理由见 §3.1；**预期失败**（§2.1）。
- 目标侧（按 C++）：`g++ -std=c++17 target.cpp -o program` 在 **Windows VM `windows-eval`（`192.168.195.128`）** MinGW/UCRT64。
- comparison_manifest 双侧 `os`：source=`linux`、target=`windows`；`arch`=`x64`；`artifactLanguage`：source=`c`、target=`cpp`。**Controller 须同时匹配到 READY 的 Linux runner 与 Windows runner**；若 runner 未就绪，Controller 返回 `INFRA_ERROR`，如实记录、恢复后重提，不改本机编译。

### 3.1 源侧 build 命令的平台宏说明（不倒填、不改源）

- `du.c` 是 FreeBSD base-system 代码，参考平台为 FreeBSD 而非 Linux glibc。以**命令行宏**在源不变前提下尽量迁就：
  1. **POSIX 特性测试宏 `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE`**：暴露 glibc 在 strict `-std=c11` 下隐藏的 POSIX/BSD 符号（沿用前三例已证实的同类行为）。
  2. **`__unused`（FreeBSD `<sys/cdefs.h>` 属性宏，glibc 不定义）以 `-D__unused=` 置空**：仅属性提示，置空不改行为与可编译性。
- **归因与预期**：以上命令行宏**无法**补齐 `SIGINFO`/`UF_NODUMP`/`st_flags`/libutil（BSD 专有），故源基线**预期仍失败**（§2.1）。不为凑基线通过而改源或把命令放松到失真。目标侧命令与 `target.cpp` 均不因此调整。
- 若源侧基线如预期失败，按前三例先例：如实记录真实回传，作失败类别数据点，不倒填。

## 4. 调度上下文与模型输出约束

- 模型、API 地址、温度由根目录 `.env` 提供；密钥不写入任何交付文件、manifest 或请求正文。
- **提交前先验证 `.env` 模型可用**；不可用则如实记录、按相同输入最多重试一次，不换模型、不伪造自评或代写模型产物。
- 模型请求上下文：C→C++ 方向 + [header-macro 规则](../../../../../../../../../skills/directions/c-to-cpp/references/header-macro.md) + [type-abi 专题](../../../../../../../../../skills/directions/c-to-cpp/references/type-abi.md) + [posix-windows-filesystem 系统方向](../../../../../../../../../skills/systems/posix-windows-filesystem/SKILL.md)。不注入 long-file 工作流。
- 输出约束：完整单文件 `target.cpp`，无 Markdown fence/解释/省略号；尽力保留 du(1) 可观察行为（选项集、递归遍历累加、单位换算、深度/总计/忽略掩码/不跨设备、硬链接去重、`usage()` 到 stderr 并退出）；平台缺失能力（`SIGINFO` 进度、`UF_NODUMP`、`st_blocks`）按保守、可观察行为尽量一致处理并在文件顶部注释登记为已知差异；不新增进程执行/外联/文件写删/权限/隐蔽能力；不把未编译/未运行结果说成通过或等价。

## 5. 授权与落点

- 执行形态按**本项目既定的双侧执行授权**：在获批隔离 VM 做跨 OS 双侧构建+运行，不再逐例询问形态。本 case 逐例安全前提已确认——源低风险、纯只读遍历+汇总打印、无网络/无 exec/无文件写删；隔离/工具链/清理随本 case、本工具链核对，确认不扩展到其它样例。`executionApproved` 在实际向隔离 VM 提交 capsule 后才置 `true`。
- 产物落点按[交付契约 §2.2](../../../../../../../../../references/framework/delivery-handoff-contract.md)：本 `01-frozen/` + `02-conversion/target.gen.*` + `03-self-review/` + `04-evaluation/job-<NN>-<用途>/`；run 根 `target.cpp` = 最终交付版本。
- 无匹配契约/授权时停在文本交付并标 `UNVERIFIED`，不在本机编译或运行。
