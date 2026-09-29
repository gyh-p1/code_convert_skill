# rc4 · run-01 · 配置模型转换输入记录（冻结）

> 状态：FROZEN；`.env` 配置模型生成目标；**语言方向维度**首例，方向 **C → Go**，**同 OS**（Windows Agent，隔离语言变量）。本 run 属当前编译质量阶段，只把 **build 证据**计入指标，不评功能、不设行为 oracle。
> 归属：[case.md](../../../../case.md) · 阶段 [index](../../../../../../../../项目开发规范.md#当前开发阶段与退出条件)
> 共享源：上游来源说明已清理；冻结副本见当前 run 的 `source/` 目录（上游 RC4 模块逐字 + 自写薄 CLI 驱动；公有领域；sha256 为完整性锚）
> 与 du 的关键差异：du 是**跨 OS**、预记为失败类；本例是**同 OS 语言方向**、预期双侧可干净 build（但不预判，见 §2.1）。

## 1. 输入与目标

- 源文件（3 份，均在 `当前 run 的 source/ 冻结副本`）：
  - `WjCryptLib_Rc4.c`（167 行，sha256 `9c77e9b3f45dfe6162b1694b57bda665a3b24490841fa5ef95952dd1a73a72c6`）——**上游逐字，被评译主体**。
  - `WjCryptLib_Rc4.h`（94 行，sha256 `f33d3a78e2f0642ad0c99d226f29eaaac844c82a0eaaae42a377b4222984f7c0`）——**上游逐字，被评译主体**。
  - `rc4_decrypt_cli.c`（94 行，sha256 `9ab3ebbb8926bf580162ba2307401f8b1bb923e5ba944ef85a0a508ef5789083`）——**本项目自写薄驱动**（非上游，按"可执行时默认补入口"政策补入，无自有密码学逻辑）。
- 源自包含：仅系统头（`<stdint.h>`/`<stdlib.h>`/`<stdio.h>`/`<string.h>`）+ 一个本地 `#include "WjCryptLib_Rc4.h"`。**无平台 `#ifdef` 分支**。
- 源语言/系统：C（**C11**）；纯可移植 ANSI/C11，无 POSIX/Win 专有面。
- 目标语言/系统：**Go**（当前稳定 `go` 工具链，`package main`）；**同 OS**（Windows），隔离语言变量。
- 任务模式：单方向多文件文本转换——把 3 份 C 文件整体转换为**一个 `package main` 的 `target.go`**。
- 场景：只读——按 hex key 解密一段 RC4 混淆 blob（恶意软件配置/字符串提取、CTF crypto 的真实任务）；无网络、无文件写/删、无进程/命令执行。ATT&CK：`none`。RAG：**关闭**。

## 2. 编译/执行形态（决定 = 同 OS 双侧 build，均在 Windows Agent）

- **源侧与目标侧同在 Windows Agent `windows-eval`（`192.168.195.128`，已确认支持 `c`+`go`）**，用以隔离"C 源本身能否编"与"转换到 Go 引入/暴露的编译结果"，把变量收敛到语言本身。
- 源侧无需补写入口：驱动 `rc4_decrypt_cli.c` 自带 `main`，与 `WjCryptLib_Rc4.c` 两个翻译单元链接为可执行 `program`。
- **本阶段只读 build 证据**：capsule 的运行仅迁就双侧执行契约；run/behavior 结果不计入功能率，本 run 不设行为 oracle。
- **运行边界（获批隔离 VM 内）**：liveness 以固定只读参数启动 `program 4b6579 bbf316e8d940af0ad3`（公开 RC4 测试向量 → 明文 `Plaintext`）后退出；不联网、不执行外部命令、不读敏感文件、不写/删文件。结束即销毁临时件。

### 2.1 预期面（先记预期，绝不倒填）

- **与 du 不同，本例预期双侧均可干净 build**：源为纯可移植 C、目标 runner 已确认支持 `c`+`go`、同 OS 无跨系统面。故若失败，多半可归因到**转换本身**（Go 语法/未用 import/无符号显式转换/退出码），而非源可移植性——正是语言维度想要的、可归因到转换的数据点。
- 但**不预判通过**：模型产物可编译性以真实回传为准。可能的目标失败：未使用 import（Go 编译错误）、`byte`/`uint32` 显式转换缺失、`void*`→`[]byte` 映射不当、`package` 声明缺失、`os.Exit` 退出码语义偏移等，如实记录为失败类别。
- 源侧 C 基线预期 `COMPLETED`（两个 C 翻译单元链接成 `program`）；若意外失败亦如实记录，不改源、不放松命令到失真。

## 3. 目标工具链（冻结，具体版本以实际 Controller 为准）

- 源侧（对照基线，C11）：`gcc -std=c11 WjCryptLib_Rc4.c rc4_decrypt_cli.c -o program` 在 **Windows Agent `windows-eval`（`192.168.195.128`）**。两个翻译单元，无需任何平台宏。
- 目标侧（Go）：`go build -o program.exe target.go`（单 `package main`；命名单文件构建，仅标准库、无需 `go.mod`）在 **同一 Windows Agent**。
- comparison_manifest 双侧 `os` 均 `windows`；`arch`=`x64`；`artifactLanguage`：source=`c`、target=`go`。**Controller 只须匹配到 READY 的 Windows runner**（同 OS，无需 Linux runner）；若 runner 未就绪，Controller 返回 `INFRA_ERROR`，如实记录、恢复后重提，不改本机编译。

## 4. 调度上下文与模型输出约束

- 模型、API 地址、温度由根目录 `.env` 提供；密钥不写入任何交付文件、manifest 或请求正文。
- **提交前先验证 `.env` 模型可用**；不可用则如实记录、按相同输入最多重试一次，不换模型、不伪造自评或代写模型产物。
- 模型请求上下文：C→Go 方向 + **system 消息内联的 C→Go 显式映射指引**（头/预处理→包与导出、`#define` 宏→函数/元组交换、指针/字节缓冲/`void*`→`[]byte`、定宽无符号与 mod-256 语义→`byte`/`uint32` 显式转换、错误返回码→`error`+`os.Exit` 退出码、`argv`/hex 解析→`os.Args`+`encoding/hex`、**未用 import/变量即编译错误**）。**不注入尚不存在的 `c-to-go` Skill**（该 Skill 由本 run 真实证据在 step-05 反哺创建，非本 run 输入），不注入 long-file 工作流。
- 输出约束：**完整单文件 `target.go`**（把 3 份 C 文件整体转换为一个 `package main` 的 Go 源），无 Markdown fence/解释/省略号；第一行即源码第一行、最后一行即源码最后一行。保留可观察行为（用法 `program <hex-key> <hex-ciphertext>`、错误退出码 2/1、成功把明文写 stdout、RC4 KSA/PRGA 语义与上游一致）；不新增进程执行/外联/文件写删/权限/隐蔽能力；不把未编译/未运行结果说成通过或等价。

## 5. 授权与落点

- 执行形态按**本项目既定的双侧执行授权**：在获批隔离 VM 做同 OS 双侧构建+运行，不再逐例询问形态。本 case 逐例安全前提已确认——源低风险、纯只读 RC4 解密（公开测试向量输入）、无网络/无 exec/无文件写删；隔离/工具链/清理随本 case 核对，确认不扩展到其它样例。`executionApproved` 在实际向隔离 VM 提交 capsule 后才置 `true`。
- 产物落点按[交付契约 §2.2](../../../../../../../../../references/framework/delivery-handoff-contract.md)：本 `01-frozen/` + `02-conversion/target.gen.*` + `03-self-review/` + `04-evaluation/job-<NN>-<用途>/`；run 根 `target.go` = 最终交付版本。
- 无匹配契约/授权时停在文本交付并标 `UNVERIFIED`，不在本机编译或运行。
