# realpath：FreeBSD `realpath(1)` POSIX C → Windows C++（多系统 filesystem 子域，step-04 批次 2/4）

> 状态：FROZEN（step-04 批次第 2 例；跨 OS 双侧 build 形态沿用 stest——见 §3）
> 归属阶段：[最终交付编译质量与 Skill 拓展](../../../../项目开发规范.md#当前开发阶段与退出条件) · 执行真源 [index](../../../../项目开发规范.md#当前开发阶段与退出条件) step-04 · 批次文档 [step-04](../../../../项目开发规范.md#当前开发阶段与退出条件)
> 共享源样例：`当前 run 的 source/ 冻结副本`（共享源快照已清理；冻结副本见当前 run 的 `source/` 目录）（自包含，仅系统头，无本地 `""` 头）
> 上游来源与许可：上游来源说明已清理；冻结副本见当前 run 的 `source/` 目录 与随附 BSD-3-Clause `COPYRIGHT.freebsd`
> 前序：批次首例 [stest](../stest-fs-posix-to-win/case.md) 已 CLOSED（跨 OS 双侧 build 真实 PASS）；本例复用同一形态与调度政策。

## 1. 转换方向与标签（已确认）

- 源：C；按 **C11** 理解。**无平台 `#ifdef` 分支**（读+grep 确认无 `_WIN32`/`WIN32`/`windows.h`）。含 FreeBSD base 惯用法 `__dead2`（见 §3.1）。
- 目标：C++；**C++17**。**做跨 OS 迁移**——POSIX/Linux → Windows。step-04「多系统 = POSIX→Windows，filesystem 子域」维度第 2 个真实消费者。
- 任务模式：短单文件文本转换（82 物理行，**无伴随头**）。
- 系统方向 Skill：[`skills/systems/posix-windows-filesystem`](../../../../../skills/systems/posix-windows-filesystem/SKILL.md)——本例正中该 skill 的**头牌规则** `realpath(3)` ↔ `GetFullPathName`/`_fullpath`。语言方向沿用 [`skills/directions/c-to-cpp`](../../../../../skills/directions/c-to-cpp/SKILL.md)（含 header-macro、type-abi 专题）。
- 场景：只读路径规范化（解析 + 打印）；只读 `argv`；无网络、无文件写、无进程/命令执行。ATT&CK tactic/technique：`none`。RAG：关闭。
- 目标文件命名与落点：按[交付契约 §2.2](../../../../../references/framework/delivery-handoff-contract.md)。

## 2. POSIX→Windows filesystem 表面（本例真实考点）

`realpath.c` 表面薄但正对 skill 头牌规则，在 Windows/MinGW 侧**并非同名等价**：

- `realpath(path, buf)`（`<stdlib.h>`, POSIX）：解析符号链接得绝对路径。Windows 无同名 `realpath`；对应 `_fullpath`（MinGW `<stdlib.h>`）或 Win32 `GetFullPathName`——但二者**不解析符号链接、对不存在路径的存在性语义也不同**（`realpath` 对不存在路径返回 NULL+errno，`_fullpath` 仅做词法规范化、不校验存在性）。这是 skill 要坐实/纠错的核心差异。
- `PATH_MAX`（`<sys/param.h>`/`<limits.h>`）：Windows 无同名常量（`_MAX_PATH`=260 语义/取值不同）。
- `getopt`/`optind`（`<unistd.h>`, POSIX）：MSVC 无；MinGW-w64 经 `<getopt.h>`/`<unistd.h>` 提供。
- `warn`（`<err.h>`, BSD 扩展）：**glibc 有、MinGW-w64 无**——目标侧须自备 `warn` 等价（`fprintf(stderr,...)+strerror(errno)`）。
- `__dead2`（`<sys/cdefs.h>`, FreeBSD）：**glibc 与 MinGW 均不定义**（见 §3.1）。

这些是否成立、模型如何映射，均由第三方 build 证据裁定；本 case 不预判"通过"。

## 3. 编译/执行形态（已定 = 跨 OS 双侧 build，沿用 stest）

- **源侧（对照基线，POSIX）**：`cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__dead2= realpath.c -o program` 在 **Linux VM `linux-eval`（`192.168.195.129`）**。见 §3.1 说明为何需要这些宏。
- **目标侧（转换后 C++）**：`g++ -std=c++17 target.cpp -o program` 在 **Windows VM `windows-eval`（`192.168.195.128`）** MinGW/UCRT64。
- 源侧在 Linux、目标侧在 Windows，用以区分"POSIX 源本身能编（基线过）"与"转换到 Windows C++ 引入/暴露的编译失败"。
- **本阶段只读 build 证据**：capsule 的运行仅为迁就双侧执行契约；run/behavior 不计入功能率、不设行为 oracle。
- **运行边界（获批隔离 VM 内）**：liveness 驱动以无参数启动（`path = "."`，规范化当前目录并打印，`exit(0)`）；不联网、不执行外部命令、不读敏感文件、只读解析。结束即销毁临时件。

### 3.1 源侧 build 命令的平台宏说明（不改源，仅命令行提供）

- `realpath.c` 是 **FreeBSD base-system** 代码，其自然参考平台是 FreeBSD，非 Linux glibc。两处使 glibc 下严格 `-std=c11` 无法直接建立对照基线，均以**命令行宏**在源不变前提下迁就（沿用 stest 的特性测试宏教训）：
  1. **POSIX 特性测试宏**：strict `-std=c11`（`__STRICT_ANSI__`）下 glibc 隐藏 `realpath`/`getopt`/`optind`/`warn`/`PATH_MAX`。补 `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE` 暴露之（与 stest 同因）。
  2. **`__dead2`（FreeBSD `<sys/cdefs.h>` 惯用法，glibc 不定义）**：以 `-D__dead2=` 将其定义为空——`__dead2` 仅是 `noreturn` 属性提示，置空不改行为、不改可编译性，是 BSD 源在 Linux 的常见可移植 shim。
- **归因**：这是**源对 glibc 的可移植性事实**（FreeBSD-ism），以命令行宏建立可用对照基线，**不编辑源快照**。目标侧命令与 `target.cpp` 均不因此调整——目标侧 `realpath`/`warn`/`__dead2`/`getopt` 在 Windows 的等价性正是要测的数据点。
- 若源侧基线仍在其它符号上失败，如实记录真实回传、按 stest 先例（job-NN 递进、不倒填）处理。

## 4. 调度与模型输出约束

- 模型、API 地址、温度由根目录 `.env` 提供；密钥不写入任何交付文件、manifest 或请求正文。
- **提交前先验证 `.env` 模型可用**；不可用则如实记录、按相同输入最多重试一次，不换模型、不伪造自评或代写模型产物。
- 模型请求上下文：C→C++ 方向 + [header-macro 规则](../../../../../skills/directions/c-to-cpp/references/header-macro.md) + [type-abi 专题](../../../../../skills/directions/c-to-cpp/references/type-abi.md) + [posix-windows-filesystem 系统方向](../../../../../skills/systems/posix-windows-filesystem/SKILL.md)。不注入 long-file 工作流（本例短）。
- 输出约束：完整单文件 `target.cpp`，无 Markdown fence/解释/省略号；保留可观察行为（`-q` 抑制告警、每个路径解析成功打印规范化路径、失败 `warn` 且 `rval=1`、退出码 `rval`、`usage()` exit(1)、无参数时规范化 `"."`）；不新增进程执行/外联/权限；不把未编译结果说成通过或等价。

## 5. 授权与落点

- 执行形态按**本项目既定的双侧执行授权**：在获批隔离 VM 做跨 OS 双侧构建+运行，不再逐例询问形态。本 case 逐例安全前提已确认——源为低风险、纯只读路径规范化、无网络/无 exec/无文件写；隔离/工具链/清理随本 case 核对，确认不扩展到其它样例。`executionApproved` 仅在实际向隔离 VM 提交 capsule 后置 `true`。
- 产物落点按[交付契约 §2.2](../../../../../references/framework/delivery-handoff-contract.md)：`01-frozen/` + `02-conversion/target.gen.*` + `03-self-review/` + `04-evaluation/job-<NN>-<用途>/`；run 根 `target.cpp` = 最终交付版本。
- 无匹配契约/授权时停在文本交付并标 `UNVERIFIED`，不在本机编译或运行。

## 非目标

- 不在本机编译、运行、调用构建脚本或触发代码生成。
- 不评功能正确率、不设/不比对行为 oracle；build 通过不说成功能或安全正确。
- 不为凑"通过"把修订稿成功回写成原始生成稿成功；失败按"失败类别→Skill 规则"记录，供 step-05 更新 `posix-windows-filesystem`。
