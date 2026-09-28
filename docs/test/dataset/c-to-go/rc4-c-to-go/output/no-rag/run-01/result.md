# rc4（WjCryptLib RC4）C → Go 转换结果报告（run-01）

## 结论速览

本次把 WjCryptLib RC4 模块（`WjCryptLib_Rc4.c` + `.h`）+ 自写薄 CLI 驱动 `rc4_decrypt_cli.c` 共 3 份 C 文件，由 `.env` 配置模型（`deepseek-flash`）一次性转换为单文件 `package main` 的 Go（`target.go`，196 行），并经模型一次结构化自审判为 `NO-REPAIR-IDENTIFIED`，无自修轮。**目标代码的第三方编译证据未取得**：same-OS 双侧 comparison capsule 于 2026-09-28 两次提交恒就绪且已授权的 Controller，**两次均终态 `INFRA_ERROR`**，目标侧从未构建。故本 run 的**语法/编译结论为 `INCONCLUSIVE`（阻断，既非通过也非失败）**，`thirdPartyCompileStatus=BLOCKED-INFRA-ERROR`。真实回传证据落于 [`04-evaluation/job-01-dual-build/returned-evidence/`](04-evaluation/job-01-dual-build/returned-evidence/)（首次）与 [`.../returned-evidence/retry-02/`](04-evaluation/job-01-dual-build/returned-evidence/retry-02/)（重试）。

| 问题 | 结论 | 依据与边界 |
|---|---|---|
| 最终代码是否交付完整 | **已完成（交付完整单文件）** | [`target.go`](target.go) 为完整单文件 `package main`，无截断/省略/Markdown 围栏；与生成稿 [`02-conversion/target.gen.go`](02-conversion/target.gen.go) 同一 sha256（`7629c790…`），无自修 |
| 语法/编译是否正确 | **INCONCLUSIVE（阻断，未取得证据）** | 目标侧 build 从未发生（`execution.performed=false`、`preflight=SKIPPED`）；Controller 在 build 之前于 same-runner baseline 交接阶段以环境类 `INFRA_ERROR` 阻断。无 target build 证据可判 PASS/FAIL |
| 功能是否一致 | **未计分且不可测（阻断）** | 双侧从未运行；本阶段本就不设行为 oracle、不计入功能率 |

## 编译/执行形态与真实回传

- 形态：same-OS 双侧 build（源与目标同在 Windows Agent `windows-eval`，隔离语言变量）。源侧对照基线 `gcc -std=c11 WjCryptLib_Rc4.c rc4_decrypt_cli.c -o program`；目标侧 `go build -o program.exe target.go`（单 `package main`，仅标准库，无需 `go.mod`）。
- 两次提交均 `POST /api/jobs`（`caseId=rc4-c-to-go-run-01`, `targetOs=windows`, `targetLang=go`），Controller 直连 HTTP `http://192.168.101.250:8443`：
  - 首次 jobId `eval-20260928-092052-390487e9` → `INFRA_ERROR`
  - 重试 jobId `eval-20260928-092721-a2e2311f` → `INFRA_ERROR`（恒就绪政策下相同输入单次重试，确定性复现）
- Controller 裁定 `executionStrategy=same-runner`（source/target 均 `windows/x64`，矩阵内仅一台 Windows runner），`runnerAssignments={source,target}=windows-vm-agent-x64`。
- 终态 failure：`type=AGENT_UNAVAILABLE`，`category=environment`，`retryable=false`，reason=`agent /run failed: INVALID_PACKAGE: baselineReference artifactHash does not match uploaded artifact`。
- 两侧 build 证据均缺：目标 `execution.performed=false`（从未构建）；源侧 `execution.performed=true` 但 `evidenceBundleRef=null` 且 `evidence/source` 端点返回 `404 evidence_not_found`。`environmentStatus=clean`、`runnerStateAfter=READY`、`contaminated=no`。

## 故障归因（先记事实，不倒填、不外推）

- 这是本项目**首个 same-OS / same-runner 提交**。此前 fe（C→C++）、du 等均为**跨 OS / different-runner**，走的是各 runner 独立取件路径，均 `COMPLETED`。
- 失败发生在 **same-runner 的同机 baseline 交接**：Controller 先跑源侧作 baseline，再向同一 runner 交接目标运行时，agent `/run` 以 `baselineReference.artifactHash` 校验上传 artifact 失败。
- 适配契约（[`remote-controller-adapter.md`](../../../../../../../../references/adapter/controller/remote-controller-adapter.md)）中**提交方 manifest 并无 `artifactHash`/`baselineReference` 字段**——该校验是 Controller/agent 在 same-runner 路径的内部机制，提交方无从设置。
- 结合 `failure.category=environment`、`jobStatus=INFRA_ERROR`、`environmentStatus=clean`、`retryable=false` 且**确定性复现**，判为 **same-runner 路径的基础设施缺陷**，**不归因于 capsule 内容、`target.go`、或 C→Go 转换本身**（源侧 baseline 运行 preflight/cleanup 均 PASSED，目标从未进入构建）。

## 转换过程（模型侧，已完成）

1. **生成（GENERATED）**：`.env` 模型一次生成，`finish_reason=stop` 未截断（[`02-conversion/target.gen.model.json`](02-conversion/target.gen.model.json)）。3 份 C 文件合并为一个 `package main`；`SwapBytes` 宏→元组交换；`uint8_t S[256]`→`[256]byte`、`void*` 缓冲→`[]byte`；`uint32`/`byte` 显式转换 + mod-256；返回码 `0/-1`→`error`；`main` 退出码 2/1/0 保留；`argv`→`os.Args`、hex→`encoding/hex`；仅导入 4 个使用到的标准库包。
2. **自审（SELF_REVIEWED）**：一次结构化自审报 0 处转换引入缺陷，`verdict=NO-REPAIR-IDENTIFIED`；列出的风险为运行期/OS 文本模式细节（Windows CRT text-mode stdout CRLF vs Go 二进制 `os.Stdout`），非编译/转换缺陷；测试向量明文无换行，不影响 liveness。无自修轮。
3. **注意**：模型自审 `NO-REPAIR-IDENTIFIED` **只是提交门槛，绝非语法结论**（C01 先例：自审通过仍被第三方工具链定位到未声明符号）。本 run 因 `INFRA_ERROR` 阻断，**语法结论仍为 `INCONCLUSIVE`**，不得据自审倒填 PASS。

## 未决问题与下一步

1. **编译门槛未达成（阻断于基础设施）**。本 run 停在 `EVALUATED`（终态为环境失败），**不进入 `CLOSED`**。按恒就绪政策已用相同输入重试一次并确定性复现；不改用本机编译、不放松命令、不伪造 build 结论。
2. **需上层决策**（超出本 Agent 自主可解范围）：
   - (a) 由 Controller 侧修复 same-runner 的 baseline 交接（`baselineReference.artifactHash` 校验），修复后按相同输入重提；或
   - (b) 判断是否接受一个**不触发 same-runner 路径**的合规配置取证（当前 Windows runner 仅一台，任何 same-OS Windows 双侧都会解析为 same-runner；跨 OS 取 Go build 会重新引入本 case 刻意规避的 OS 混淆变量，偏离既定 same-OS 设计，须先确认）。
3. **step-05 `skills/directions/c-to-go` 暂不创建（`BLOCKED`）**：新 Skill 须锚定**真实目标 build 证据**，本 run 未取得，故不搭空架子（AGENTS.md：新目录/机制须有当前消费者与真实证据）。待取得真实 build 证据后再据实反哺。
