# pwd · run-01 · 配置模型转换输入记录（冻结）

> 状态：FROZEN；`.env` 配置模型生成目标；step-04 多系统 POSIX→Windows filesystem 批次第 3 例。本 run 属当前编译质量阶段，只把 **build 证据**计入指标，不评功能、不设行为 oracle。
> 归属：[case.md](../../../../case.md) · 阶段 [index step-04](../../../../../../../../stages/final-output-compile/index.md) · 批次 [step-04](../../../../../../../../stages/final-output-compile/step-04-multisystem-filesystem-batch.md)
> 前序：批次首二例 [stest run-01](../../../../../stest-fs-posix-to-win/output/no-rag/run-01/result.md)、[realpath run-01](../../../../../realpath-fs-posix-to-win/output/no-rag/run-01/result.md) 均已 CLOSED（跨 OS 双侧 build 真实 PASS）。

## 1. 输入与目标

- 源文件：`docs/test/sources/freebsd-pwd/pwd.c`（123 行）。**自包含，无伴随本地头**（仅系统头）。
- 源快照：FreeBSD `bin/pwd/pwd.c`，tag `release/14.2.0` = commit `89042d64c83ca92d90bd3d161eebc353d5edb3c6`；完整性以 sha256 固定：`pwd.c`=`cf8b57f4b95abf55f7c64446686126202756411b64370751ffb21f0de93d3f68`。
- 源语言/系统：C（**C11**）；POSIX/BSD，无平台 `#ifdef` 分支；含 FreeBSD base 惯用法 `__dead2`。
- 目标语言/系统：C++（**C++17**）；**跨 OS 迁移 POSIX/Linux → Windows**。
- 任务模式：短单文件文本转换。
- 场景：只读打印当前工作目录（`getcwd`/`getenv(PWD)`/`stat` 身份校验）；无网络、无文件写、无进程/命令执行。ATT&CK：`none`。RAG：**关闭**。

## 2. 编译/执行形态（决定 = 跨 OS 双侧 build，沿用 stest/realpath）

- **源侧在 Linux VM、目标侧在 Windows VM**，隔离"POSIX/BSD 源本身能编"与"转换到 Windows C++ 引入/暴露的失败"。
- 本 case 无需补写入口：`pwd.c` 自带 `main`，两侧均可直接链接为可执行 `program`。
- **本阶段只读 build 证据**：capsule 的运行仅迁就双侧执行契约；run/behavior 结果不计入功能率，本 run 不设行为 oracle。
- **运行边界（获批隔离 VM 内）**：liveness 驱动无参数启动（默认 `-P` 物理，打印当前工作目录后 `exit(0)`）；不联网、不执行外部命令、不读敏感文件、只读打印 cwd。结束即销毁临时件。

## 3. 目标工具链（冻结，具体版本以实际 Controller 为准）

- 源侧（对照基线，按 C，POSIX/BSD）：`cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__dead2= pwd.c -o program` 在 **Linux VM `linux-eval`（`192.168.195.129`）**。平台宏理由见 §3.1。
- 目标侧（按 C++）：`g++ -std=c++17 target.cpp -o program` 在 **Windows VM `windows-eval`（`192.168.195.128`）** MinGW/UCRT64。
- comparison_manifest 双侧 `os`：source=`linux`、target=`windows`；`arch`=`x64`；`artifactLanguage`：source=`c`、target=`cpp`。**Controller 须同时匹配到 READY 的 Linux runner 与 Windows runner**；若 Linux runner 未就绪，Controller 返回 `INFRA_ERROR`，如实记录、恢复后重提，不改本机编译。

### 3.1 源侧 build 命令的平台宏说明（不倒填、不改源）

- `pwd.c` 是 FreeBSD base-system 代码，其自然参考平台为 FreeBSD 而非 Linux glibc。两处令 glibc 严格 `-std=c11` 无法直接建立对照基线，均以**命令行宏**在源不变前提下迁就：
  1. **POSIX 特性测试宏 `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE`**：strict `-std=c11`（`__STRICT_ANSI__`）下 glibc 隐藏 `getcwd`/`getopt`/`optind`/`err`。这是 stest job-01 已用真实失败证实、realpath 已沿用的同一类 glibc 行为，故本例首次冻结即纳入，避免重复烧 job。
  2. **`__dead2`（FreeBSD `<sys/cdefs.h>` 惯用法，glibc 不定义）以 `-D__dead2=` 置空**：`__dead2` 仅是 `noreturn` 属性提示，置空不改运行行为与可编译性，是 BSD 源在 Linux 的常见可移植 shim。批次文档已预记该 FreeBSD-ism 会影响 Linux 源侧基线。
- **归因**：以上是**源对 glibc 的可移植性事实（FreeBSD-ism）**，用命令行宏建立可用对照基线，**不编辑源快照**。**目标侧命令与转换产物 `target.cpp` 均不改**——目标侧 `getcwd`/`err`/`__dead2`/`getopt`/`st_ino` 在 Windows C++ 的等价可编译性正是要测的数据点。
- 若源侧基线在其它符号上仍失败，按 stest/realpath 先例：如实记录真实回传、以 job-NN 递进修正命令，不倒填、不改目标产物。

## 4. 调度上下文与模型输出约束

- 模型、API 地址、温度由根目录 `.env` 提供；密钥不写入任何交付文件、manifest 或请求正文。
- **提交前先验证 `.env` 模型可用**；不可用则如实记录、按相同输入最多重试一次，不换模型、不伪造自评或代写模型产物。
- 模型请求上下文：C→C++ 方向 + [header-macro 规则](../../../../../../../../../skills/directions/c-to-cpp/references/header-macro.md) + [type-abi 专题](../../../../../../../../../skills/directions/c-to-cpp/references/type-abi.md) + [posix-windows-filesystem 系统方向](../../../../../../../../../skills/systems/posix-windows-filesystem/SKILL.md)。不注入 long-file 工作流（本例短）。
- 输出约束：完整单文件 `target.cpp`，无 Markdown fence/解释/省略号；保留可观察行为（`-L` 逻辑/`-P` 物理默认、`$PWD` 逻辑校验成功打印其值否则退回物理 `getcwd`、成功 `printf("%s\n", p)`、失败 `err(1,".")`、`exit(0)`、多余操作数或未知选项 `usage()` 输出 `usage: pwd [-L | -P]` 到 stderr 并 `exit(1)`）；不新增进程执行/外联/权限/隐蔽能力；不把未编译/未运行结果说成通过或等价。

## 5. 授权与落点

- 执行形态按**本项目既定的双侧执行授权**：在获批隔离 VM 做跨 OS 双侧构建+运行，不再逐例询问形态。本 case 逐例安全前提已确认——源低风险、纯只读打印 cwd、无网络/无 exec/无文件写；隔离/工具链/清理随本 case、本工具链核对，确认不扩展到其它样例。`executionApproved` 在实际向隔离 VM 提交 capsule 后才置 `true`。
- 产物落点按[交付契约 §2.2](../../../../../../../../../references/framework/delivery-handoff-contract.md)：本 `01-frozen/` + `02-conversion/target.gen.*` + `03-self-review/` + `04-evaluation/job-<NN>-<用途>/`；run 根 `target.cpp` = 最终交付版本。
- 无匹配契约/授权时停在文本交付并标 `UNVERIFIED`，不在本机编译或运行。
