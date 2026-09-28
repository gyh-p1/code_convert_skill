# stest · run-01 · 配置模型转换输入记录（冻结）

> 状态：FROZEN；`.env` 配置模型生成目标；step-04 多系统 POSIX→Windows filesystem 批次首例。本 run 属当前编译质量阶段，只把 **build 证据**计入指标，不评功能、不设行为 oracle。
> 归属：[case.md](../../../../case.md) · 阶段 [index step-04](../../../../../../../../stages/final-output-compile/index.md) · 批次 [step-04](../../../../../../../../stages/final-output-compile/step-04-multisystem-filesystem-batch.md)

## 1. 输入与目标

- 源文件：`docs/test/sources/dmenu-stest/stest.c`（109 行）+ 同目录 `arg.h`（49 行，编译必需的本地头）。
- 源快照：suckless dmenu，commit `61e0072c3e6adfc67bafbc84e376cf26bc3680c0`；完整性以 sha256 固定：`stest.c`=`bb943c3e2c228398c592e873bb31abf18efba5c0f06c3bc39220443a7c7696bd`、`arg.h`=`99ca0b684fa83f2d21899345ccc33ec357cbbe48d09c56794e3292c2e28f21b0`。
- 源语言/系统：C（**C11**）；纯 **POSIX**，无平台 `#ifdef` 分支。
- 目标语言/系统：C++（**C++17**）；**跨 OS 迁移 POSIX/Linux → Windows**。
- 任务模式：短单文件文本转换。
- 场景：只读文件系统遍历（`stat`/`lstat`/`access`/`opendir`/`readdir`/`getline`/`S_IS*`）；无网络、无文件写、无进程/命令执行。ATT&CK：`none`。RAG：**关闭**。

## 2. 编译/执行形态（决定 = 跨 OS 双侧 build）

- 与 fe 的同 OS 双侧不同：**源侧在 Linux VM、目标侧在 Windows VM**，隔离"POSIX 源本身能编"与"转换到 Windows C++ 引入/暴露的失败"。
- 本 case 无需补写入口：`stest.c` 自带 `main`，两侧均可直接链接为可执行 `program`。
- **本阶段只读 build 证据**：capsule 的运行仅迁就双侧执行契约；run/behavior 结果不计入功能率，本 run 不设行为 oracle。
- **运行边界（获批隔离 VM 内）**：liveness 驱动无参数启动、stdin 立即 EOF（`getline` 立即 EOF → `match=0` → 返回 1，正常退出）；不联网、不执行外部命令、不读敏感文件、只读遍历工作目录。结束即销毁临时件。

## 3. 目标工具链（冻结，具体版本以实际 Controller 为准）

- 源侧（对照基线，按 C，POSIX）：`cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE stest.c -o program`（`arg.h` 同目录）在 **Linux VM `linux-eval`（`192.168.195.129`）**。纯 POSIX，预期**干净通过**。
- 目标侧（按 C++）：`g++ -std=c++17 target.cpp -o program`（`arg.h` 同目录）在 **Windows VM `windows-eval`（`192.168.195.128`）** MinGW/UCRT64。
- 编译器/SDK 精确版本、目标架构在提交获批 Controller 时补录本节；若实际能力非上述则按实际改写，不倒填。
- comparison_manifest 双侧 `os`：source=`linux`、target=`windows`；`arch`=`x64`；`artifactLanguage`：source=`c`、target=`cpp`。**Controller 须同时匹配到 READY 的 Linux runner 与 Windows runner**；若 Linux runner 未就绪，Controller 返回 `INFRA_ERROR`，如实记录、恢复后重提，不改本机编译。

### 3.1 源侧 build 命令修正记录（2026-09-28，不倒填）

- **初次冻结命令有误**：`cc -std=c11 stest.c -o program`（无 POSIX 特性测试宏）。job-01（`eval-20260928-053326-9a8ae00e`）真实回传：**源侧 build FAILED, exitCode=1**，glibc 在严格 `-std=c11` 下隐藏 POSIX 符号——`lstat`（第 35 行隐式声明）、`PATH_MAX`（第 63 行未声明）、`getline`（第 86 行隐式声明）。dual-runner 因"源基线无法建立"**未构建目标侧**（`evidence-target`=`evidence_not_found`、`comparison`=`comparison_not_found`），本 job 无目标 build 证据。
- **归因**：这是**冻结的源侧 build 命令规格缺陷**（我方 capsule 规格），非源本身不可移植、非转换质量问题。dmenu 上游 `config.mk` 本就带 `-D_DEFAULT_SOURCE -D_POSIX_C_SOURCE=200809L` 等宏。
- **修正**：源侧命令改为上方 `cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE stest.c -o program`（暴露 `lstat`/`getline`/`PATH_MAX`/`S_ISLNK`）。**目标侧命令与转换产物 `target.cpp` 均不改**——目标 `g++ -std=c++17` 的可编译性正是要测的数据点。
- 以 job-02 重提取真实目标 build 证据；job-01 的真实失败证据保留于 `04-evaluation/job-01-dual-build/returned-evidence/`，不删除、不倒填为通过。

## 4. 调度上下文与模型输出约束

- 模型、API 地址、温度由根目录 `.env` 提供；密钥不写入任何交付文件、manifest 或请求正文。
- **提交前先验证 `.env` 模型可用**；不可用则如实记录、按相同输入最多重试一次，不换模型、不伪造自评或代写模型产物。
- 模型请求上下文：C→C++ 方向 + [header-macro 规则](../../../../../../../../../skills/directions/c-to-cpp/references/header-macro.md) + [type-abi 专题](../../../../../../../../../skills/directions/c-to-cpp/references/type-abi.md) + [posix-windows-filesystem 系统方向](../../../../../../../../../skills/systems/posix-windows-filesystem/SKILL.md)。不注入 long-file 工作流（本例短）。
- 输出约束：完整单文件 `target.cpp`，无 Markdown fence/解释/省略号；保留可观察行为（flag 语义、退出码 `match?0:1`、`usage()` 退出 2、stdout 内容与副作用）；**保持 `#include "arg.h"` 不变、不把 arg.h 并入输出**；不新增进程执行/外联/权限/隐蔽能力；不把未编译/未运行结果说成通过或等价。

## 5. 授权与落点

- 执行形态按**本项目既定的双侧执行授权**：在获批隔离 VM 做跨 OS 双侧构建+运行，不再逐例询问形态。本 case 逐例安全前提已确认——源低风险、纯只读遍历、无网络/无 exec/无文件写；隔离/工具链/清理随本 case、本工具链核对，确认不扩展到其它样例。`executionApproved` 在实际向隔离 VM 提交 capsule 后才置 `true`。
- 产物落点按[交付契约 §2.2](../../../../../../../../../references/framework/delivery-handoff-contract.md)：本 `01-frozen/` + `02-conversion/target.gen.*` + `03-self-review/` + `04-evaluation/job-<NN>-<用途>/`；run 根 `target.cpp` = 最终交付版本。
- 无匹配契约/授权时停在文本交付并标 `UNVERIFIED`，不在本机编译或运行。
