# stest：dmenu `stest.c` POSIX C → Windows C++（多系统 filesystem 子域，step-04 批次 1/4）

> 状态：FROZEN（step-04 批次首例；跨 OS 双侧 build 形态已定——见 §4）
> 归属阶段：[最终交付编译质量与 Skill 拓展](../../../../stages/final-output-compile/阶段方案.md) · 执行真源 [index](../../../../stages/final-output-compile/index.md) step-04 · 批次文档 [step-04](../../../../stages/final-output-compile/step-04-multisystem-filesystem-batch.md)
> 共享源样例：[`../../sources/dmenu-stest/stest.c`](../../../sources/dmenu-stest/stest.c)（配 [`arg.h`](../../../sources/dmenu-stest/arg.h)）
> 上游来源与许可：[source.md](../../../sources/dmenu-stest/source.md) 与随附 MIT/X `LICENSE`

## 1. 转换方向与标签（已确认）

- 源：C；按 **C11** 理解。**无平台 `#ifdef` 分支**（纯 POSIX：`<sys/stat.h>`/`<dirent.h>`/`<unistd.h>`/`<limits.h>` + 本地 `arg.h`）。
- 目标：C++；**C++17**。**做跨 OS 迁移**——POSIX/Linux → Windows。这是 step-04「多系统 = POSIX→Windows，filesystem 子域」维度的首个真实消费者。
- 任务模式：短单文件文本转换（109 物理行 + `arg.h` 49 行）。
- 系统方向 Skill（首个真实消费者）：[`skills/systems/posix-windows-filesystem`](../../../../../skills/systems/posix-windows-filesystem/SKILL.md)（此前未验证初稿；本 run 为它提供首批真实源以坐实或按失败纠错）。语言方向沿用 [`skills/directions/c-to-cpp`](../../../../../skills/directions/c-to-cpp/SKILL.md)（含 header-macro、type-abi 专题）。
- 场景：只读文件系统（`stat`/`lstat`/`access`/`opendir`/`readdir`/`getline`/`S_IS*`）；无网络、无文件写、无进程/命令执行。ATT&CK tactic/technique：`none`。RAG：关闭。
- 目标文件命名与落点：按[交付契约 §2.2](../../../../../references/framework/delivery-handoff-contract.md)（`01-frozen/`、`02-conversion/target.gen.*`、`03-self-review/`、`04-evaluation/`）。

## 2. POSIX→Windows filesystem 表面（本例真实考点）

`stest.c` 的 POSIX 文件系统表面在 Windows/MinGW 侧**并非同名等价**，正是 `posix-windows-filesystem` 要坐实/纠错的地方：

- `struct stat` / `stat` / `lstat`：MSVCRT/MinGW 无 `lstat`（无符号链接 stat）；`st_mode` 位宏差异。
- `S_ISBLK`/`S_ISCHR`/`S_ISFIFO`/`S_ISLNK`：Windows CRT `<sys/stat.h>` **不定义** block/char/fifo/symlink 判定宏。
- `access(path, X_OK)`：Windows `_access` **不支持 `X_OK`（值 1）**，传入即 `EINVAL`。
- `<dirent.h>`/`opendir`/`readdir`：MinGW 提供兼容层，MSVC 不提供。
- `getline`：POSIX；MinGW 视版本可能缺，MSVC 无。
- `PATH_MAX`（`<limits.h>`）：Windows 无同名常量（`MAX_PATH` 语义不同）。

这些是否成立、模型如何映射，均由第三方 build 证据裁定；本 case 不预判"通过"。

## 3. 编译/执行形态（已定 = 跨 OS 双侧 build）

- **源侧（对照基线，POSIX）**：`cc -std=c11 stest.c -o program`（`arg.h` 同目录）在 **Linux VM `linux-eval`（`192.168.195.129`）**。纯 POSIX，源侧基线预期**干净通过**。
- **目标侧（转换后 C++）**：`g++ -std=c++17 target.cpp -o program`（`arg.h` 同目录）在 **Windows VM `windows-eval`（`192.168.195.128`）** MinGW/UCRT64。
- 与 fe 的**同 OS** 双侧不同：本例源侧在 Linux、目标侧在 Windows，用以区分"POSIX 源本身能编（基线过）"与"转换到 Windows C++ 引入/暴露的编译失败"。
- **本阶段只读 build 证据**：capsule 的运行仅为迁就双侧执行契约；run/behavior 不计入功能率、不设行为 oracle。
- **运行边界（获批隔离 VM 内）**：liveness 驱动以无参数 + stdin 立即 EOF 启动（`getline` 立即 EOF → 无匹配 → 返回 1，正常退出）；不联网、不执行外部命令、不读敏感文件、只读遍历。结束即销毁临时件。

## 4. 调度与模型输出约束

- 模型、API 地址、温度由根目录 `.env` 提供；密钥不写入任何交付文件、manifest 或请求正文。
- **提交前先验证 `.env` 模型可用**；不可用则如实记录、按相同输入最多重试一次，不换模型、不伪造自评或代写模型产物。
- 模型请求上下文：C→C++ 方向 + [header-macro 规则](../../../../../skills/directions/c-to-cpp/references/header-macro.md) + [type-abi 专题](../../../../../skills/directions/c-to-cpp/references/type-abi.md) + [posix-windows-filesystem 系统方向](../../../../../skills/systems/posix-windows-filesystem/SKILL.md)（跨 OS filesystem）。不注入 long-file 工作流（本例短）。
- 输出约束：完整单文件 `target.cpp`，无 Markdown fence/解释/省略号；保留可观察行为（flag 语义、退出码 `match?0:1`、`usage` 退出 2、stdout 内容）；**保持 `#include "arg.h"` 不变、不把 arg.h 并入输出**；不新增进程执行/外联/权限；不把未编译结果说成通过或等价。

## 5. 授权与落点

- 执行形态按**本项目既定的双侧执行授权**：在获批隔离 VM 做跨 OS 双侧构建+运行，不再逐例询问形态。本 case 逐例安全前提已确认——源为低风险、纯只读遍历、无网络/无 exec/无文件写；隔离/工具链/清理随本 case 核对，确认不扩展到其它样例。`executionApproved` 仅在实际向隔离 VM 提交 capsule 后置 `true`。
- 产物落点按[交付契约 §2.2](../../../../../references/framework/delivery-handoff-contract.md)：`01-frozen/` + `02-conversion/target.gen.*` + `03-self-review/` + `04-evaluation/job-<NN>-<用途>/`；run 根 `target.cpp` = 最终交付版本。
- 无匹配契约/授权时停在文本交付并标 `UNVERIFIED`，不在本机编译或运行。

## 非目标

- 不在本机编译、运行、调用构建脚本或触发代码生成。
- 不评功能正确率、不设/不比对行为 oracle；build 通过不说成功能或安全正确。
- 不为凑"通过"把修订稿成功回写成原始生成稿成功；失败按"失败类别→Skill 规则"记录，供 step-05 更新 `posix-windows-filesystem`。
