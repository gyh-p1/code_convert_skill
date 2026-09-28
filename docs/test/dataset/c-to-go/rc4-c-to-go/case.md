# rc4：WjCryptLib RC4（公有领域 C）→ Go（同 OS）——语言方向维度首例（攻防 crypto 切片）

> 状态：FROZEN。本项目在完成 step-04「多系统 POSIX→Windows/filesystem」批次（stest/realpath/pwd CLOSED、du 失败类数据点 CLOSED）后，**新开「语言方向」维度**：约束在攻防语言域内取最常见转换。工具链约束下（Windows Agent 支持 `c/cpp/python/powershell/go/dotnet`，**无 rust**）选 **C → Go**，**同 OS**（隔离语言变量，避免 du 式跨 OS/源基线失败导致取不到目标证据）。本 run 属编译质量阶段，只把 **build 证据**计入指标，不评功能、不设行为 oracle。
> 归属阶段：[最终交付编译质量与 Skill 拓展](../../../../stages/final-output-compile/index.md)（语言方向为该阶段新拓展维度）
> 共享源样例：[`../../sources/wjcryptlib-rc4/`](../../../sources/wjcryptlib-rc4/source.md)——上游 RC4 模块（逐字）+ 薄 CLI 驱动（自写 harness）
> 上游来源与许可：见 [source.md](../../../sources/wjcryptlib-rc4/source.md)（公有领域，文件头奉献声明；sha256 为完整性锚）

## 1. 转换方向与标签（已确认）

- 源：C（按 **C11** 理解）。**无平台 `#ifdef` 分支**（纯可移植 ANSI/C11，仅 `<stdint.h>`/`<stdlib.h>`/`<stdio.h>`/`<string.h>`）。
- 目标：**Go**（按当前稳定 `go` 工具链，`package main`）。**同 OS**——源与目标均在 **Windows Agent `windows-eval`（`192.168.195.128`）** 构建运行，用以**隔离语言变量**：本例考的是「C 语言习惯 → Go 语言习惯」的映射，不掺入跨 OS 系统面。
- 任务模式：单方向多文件文本转换（上游 `WjCryptLib_Rc4.c` 167 行 + `.h` 94 行 + 驱动 `rc4_decrypt_cli.c` 94 行；均自包含，仅系统头 + 一个本地 `""` 头）。
- 语言方向 Skill：**本例是 `skills/directions/c-to-go` 的首个真实数据点——该 Skill 尚不存在，将由本 run 的真实证据在 step-05 反哺创建，而非本 run 的输入**（新 Skill 须锚定真实证据，不搭空架子）。故本 run 模型请求上下文用 system 消息内联 C→Go 显式指引，不注入尚不存在的 c-to-go Skill 文件。
- 场景：只读——按 key 解密一段 RC4 混淆的 blob（恶意软件配置/字符串提取、CTF 的真实任务）；无网络、无文件写/删、无进程/命令执行。ATT&CK tactic/technique：`none`。RAG：关闭。
- 目标文件命名与落点：按[交付契约 §2.2](../../../../../references/framework/delivery-handoff-contract.md)；run 根 `target.go` = 最终交付版本。

## 2. C → Go 语言转换表面（本例真实考点）

RC4 模块 + 驱动在 C 里的以下习惯，在 Go 里**没有机械一一对应**，须换用 Go 习惯，是本数据点要坐实的映射面：

- **头文件/预处理 → 包与导出**：C 的 `.h` 原型 + `#include "WjCryptLib_Rc4.h"` 在 Go 里无对应——须并入同一 `package main`（或拆包），以**首字母大小写**表达导出/私有；无预处理器。
- **`#define SwapBytes(...)` 宏 → 函数/内联交换**：Go 无宏；须换成小函数或直接 `a, b = b, a` 元组交换。
- **手工字节缓冲/指针 → 切片**：`uint8_t S[256]`、`(uint8_t*)Buffer`、`((uint8_t*)Key)[i % KeySize]`、`void const*`/`void*` 泛型缓冲 → Go `[]byte`/定长数组 `[256]byte`；`void*` 无 Go 等价，须用 `[]byte`。
- **定宽无符号与 mod-256 语义**：`uint32_t i,j` + `% 256`、`(uint8_t)i`、`(uint8_t)((hi<<4)|lo)` → Go 的 `byte`/`uint32`，**无隐式整型转换**（须显式 `byte(...)`/`uint32(...)`），`byte` 天然模 256。
- **错误返回码 → `error`**：`Rc4Initialise`/`Rc4XorWithKey` 返回 `0`/`-1`（KeySize==0）、`main` 的 `return 2/1/0` → Go 惯用 `error` 返回 + `os.Exit(code)`；须保持相同退出码语义（用法错误、初始化失败、成功）。
- **`argv` 与十六进制解析 → `os.Args` + `encoding/hex`**：驱动的 `nibble`/`hex_decode` 手写循环在 Go 可用 `encoding/hex`，或保留手写；`argc/argv` → `os.Args`。
- **`struct` 布局**：`Rc4Context{ i,j uint32; S [256]byte }` 在 Go 无 ABI/布局保证需求（本例不依赖布局），但正是「C struct 无脑映射」须警惕之处。
- **导入即用**：Go 未使用的 import/变量是**编译错误**——模型若引入 `encoding/hex` 却未用、或反之，会直接 build 失败。这是 C→Go 的高频真实失败点，正是本数据点的观察重点之一。

这些是否成立、模型如何映射，均由第三方 build 证据裁定；本 case **不预判「通过」**。

### 2.1 预期面（先记预期，再取真实证据，绝不倒填）

- **与 du 不同，本例预期双侧均可干净 build**：源为纯可移植 C、目标 runner 已确认支持 `c`+`go`、同 OS 无跨系统面。故若失败，多半来自**转换本身**（Go 语法/未用 import/无符号处理/退出码），而非源可移植性——这正是语言维度想要的、可归因到转换的数据点。
- 但**不预判通过**：模型产物可编译性以真实回传为准。可能的目标失败：未使用 import、`byte`/`uint32` 显式转换缺失、`void*`→`[]byte` 映射不当、包声明缺失等，如实记录。
- 源侧 C 基线预期 `COMPLETED`（两个 C 翻译单元链接成 `program`）；若意外失败亦如实记录，不改源。

## 3. 编译/执行形态（已定 = 同 OS 双侧 build，Windows Agent）

- **源侧（对照基线，C11）**：`gcc -std=c11 WjCryptLib_Rc4.c rc4_decrypt_cli.c -o program`（两个翻译单元；无需任何平台宏）——在 **Windows Agent `windows-eval`（`192.168.195.128`）**。
- **目标侧（转换后 Go）**：`go build -o program.exe target.go`（单 `package main`；命名单文件构建，仅用标准库、无需 `go.mod`）——**同一 Windows Agent**。
- 源与目标同 OS 同机，用以区分「C 源本身能否编」与「转换到 Go 引入/暴露的编译结果」，且把变量收敛到语言本身。
- **本阶段只读 build 证据**：capsule 的运行仅迁就双侧执行契约；run/behavior 不计入功能率、不设行为 oracle。
- **运行边界（获批隔离 VM 内）**：liveness 以固定只读参数启动 `program 4b6579 bbf316e8d940af0ad3`（公开 RC4 测试向量 → 明文 `Plaintext`）后退出；不联网、不执行外部命令、不读敏感文件、不写/删文件。结束即销毁临时件。

## 4. 调度与模型输出约束

- 模型、API 地址、温度由根目录 `.env` 提供；密钥不写入任何交付文件、manifest 或请求正文。
- **提交前先验证 `.env` 模型可用**；不可用则如实记录、按相同输入最多重试一次，不换模型、不伪造自评或代写模型产物。
- 模型请求上下文：C→Go 方向 + system 消息内联的 C→Go 显式映射指引（头/预处理→包与导出、宏→函数、指针/缓冲/`void*`→`[]byte`、定宽无符号与显式转换、错误码→`error`+退出码、未用 import 即编译错误）。**不注入尚不存在的 c-to-go Skill**，不注入 long-file 工作流。
- 输出约束：**完整单文件 `target.go`**（把三份 C 文件整体转换为一个 `package main` 的 Go 源），无 Markdown fence/解释/省略号；保留可观察行为（用法 `program <hex-key> <hex-ciphertext>`、错误退出码 2/1、成功把明文写 stdout、RC4 语义与上游一致）；不新增进程执行/外联/文件写删/权限/隐蔽能力；不把未编译结果说成通过或等价。

## 5. 授权与落点

- 执行形态按**本项目既定的双侧执行授权**：在获批隔离 VM 做同 OS 双侧构建+运行，不再逐例询问形态。本 case 逐例安全前提已确认——源为低风险、纯只读的 RC4 解密（公开测试向量输入）、无网络/无 exec/无文件写删；隔离/工具链/清理随本 case 核对，确认不扩展到其它样例。`executionApproved` 仅在实际向隔离 VM 提交 capsule 后置 `true`。
- 产物落点按[交付契约 §2.2](../../../../../references/framework/delivery-handoff-contract.md)：`01-frozen/` + `02-conversion/target.gen.*` + `03-self-review/` + `04-evaluation/job-<NN>-<用途>/`；run 根 `target.go` = 最终交付版本。
- 无匹配契约/授权时停在文本交付并标 `UNVERIFIED`，不在本机编译或运行。

## 6. 非目标与数据点用途

- 不在本机编译、运行、调用构建脚本或触发代码生成。
- 不评功能正确率、不设/不比对行为 oracle；build 通过不说成功能或安全正确。
- **不为凑「通过」改源、放松命令到失真，或把修订稿成功回写成原始生成稿成功。**
- 本例数据点反哺 step-05 **新建 `skills/directions/c-to-go`**（头/预处理→包与导出、指针/缓冲/`void*`→`[]byte`、定宽无符号与显式转换、宏→函数、错误码→`error`+退出码、未用 import 即编译错误等真实坐实项）。**cgo 边界、goroutine/并发**不属本例（并发属场景维度，保持在外）。
