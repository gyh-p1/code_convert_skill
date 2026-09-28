# rc4（WjCryptLib RC4）C → Go 转换结果报告（run-01）

## 结论速览

本次把 WjCryptLib RC4 模块（`WjCryptLib_Rc4.c` + `.h`）+ 自写薄 CLI 驱动 `rc4_decrypt_cli.c` 共 3 份 C 文件，由 `.env` 配置模型（`deepseek-flash`）一次性转换为单文件 `package main` 的 Go（`target.go`，196 行），并经模型一次结构化自审判为 `NO-REPAIR-IDENTIFIED`，无自修轮。**目标代码的第三方编译证据未取得**：same-OS 双侧 comparison capsule 于 2026-09-28 两次提交恒就绪且已授权的 Controller，**两次均终态 `INFRA_ERROR`**，目标侧从未构建。故本 run 的**语法/编译结论为 `INCONCLUSIVE`（阻断，既非通过也非失败）**，`thirdPartyCompileStatus=BLOCKED-INFRA-ERROR`。真实回传证据落于 [`04-evaluation/job-01-dual-build/returned-evidence/`](04-evaluation/job-01-dual-build/returned-evidence/)（首次）与 [`.../returned-evidence/retry-02/`](04-evaluation/job-01-dual-build/returned-evidence/retry-02/)（重试）。

| 问题 | 结论 | 依据与边界 |
|---|---|---|
| 最终代码是否交付完整 | **已完成（交付完整单文件）** | [`target.go`](target.go) 为完整单文件 `package main`，无截断/省略/Markdown 围栏；与生成稿 [`02-conversion/target.gen.go`](02-conversion/target.gen.go) 同一 sha256（`7629c790…`），无自修 |
| 语法/编译是否正确 | **INCONCLUSIVE（阻断，未取得证据）** | 目标侧 build 从未发生（`execution.performed=false`、`preflight=SKIPPED`）；Agent 报身份哈希不匹配，源侧也无 evidence bundle。后续无害回归定位到 Windows 混合大小写文件排序差异；无 target build 证据可判 PASS/FAIL |
| 功能是否一致 | **未计分且不可测（阻断）** | 双侧从未运行；本阶段本就不设行为 oracle、不计入功能率 |

## 编译/执行形态与真实回传

- 形态：same-OS 双侧 build（源与目标同在 Windows Agent `windows-eval`，隔离语言变量）。源侧对照基线 `gcc -std=c11 WjCryptLib_Rc4.c rc4_decrypt_cli.c -o program`；目标侧 `go build -o program.exe target.go`（单 `package main`，仅标准库，无需 `go.mod`）。
- 两次提交均 `POST /api/jobs`（`caseId=rc4-c-to-go-run-01`, `targetOs=windows`, `targetLang=go`），Controller 直连 HTTP `http://192.168.101.250:8443`：
  - 首次 jobId `eval-20260928-092052-390487e9` → `INFRA_ERROR`
  - 重试 jobId `eval-20260928-092721-a2e2311f` → `INFRA_ERROR`（恒就绪政策下相同输入单次重试，确定性复现）
- Controller 裁定 `executionStrategy=same-runner`（source/target 均 `windows/x64`，矩阵内仅一台 Windows runner），`runnerAssignments={source,target}=windows-vm-agent-x64`。
- 终态 failure：`type=AGENT_UNAVAILABLE`，`category=environment`，`retryable=false`，reason=`agent /run failed: INVALID_PACKAGE: baselineReference artifactHash does not match uploaded artifact`。
- 两侧 build 证据均缺：目标 `execution.performed=false`（从未构建）；源侧 `execution.performed=true` 但 `evidenceBundleRef=null` 且 `evidence/source` 端点返回 `404 evidence_not_found`。`environmentStatus=clean`、`runnerStateAfter=READY`、`contaminated=no`。

## 故障归因（真实回传与后续诊断分开）

- **当时回传事实**：这是本项目首个同 OS、`executionStrategy=same-runner` 提交；两次 `INFRA_ERROR` 均报 `baselineReference.artifactHash` 不匹配。源侧 `performed=true` 只表示尝试调用 Agent，`evidenceBundleRef=null` 且取证接口 404，不能据此说源程序已构建或运行；目标侧完全跳过。
- **后续定位（2026-09-28，本地无害工程回归）**：Controller 按相对 POSIX 路径字符串排序哈希，Windows Agent 原按忽略大小写的 `Path` 对象排序。源包 `WjCryptLib_Rc4.c/.h` 与小写文件并存，静态重算两种顺序得到不同 hash；同结构的无害 `/run` 请求修前报同一 400，Agent 统一排序后通过，错误 hash 仍被拒绝。见[适配记录](../../../../../../../../references/adapter/controller/remote-controller-adapter.md)。这是源侧身份校验前的环境/实现问题，**不能归因于目标 `target.go`**，也不能泛化为所有 same-runner 任务失败。
- **证据等级**：上述是本地代码诊断与工程测试，不是已部署 VM 的新回传。原 Controller JSON/日志不变，RC4 的语法和功能仍为 `INCONCLUSIVE`。

## 转换过程（模型侧，已完成）

1. **生成（GENERATED）**：`.env` 模型一次生成，`finish_reason=stop` 未截断（[`02-conversion/target.gen.model.json`](02-conversion/target.gen.model.json)）。3 份 C 文件合并为一个 `package main`；`SwapBytes` 宏→元组交换；`uint8_t S[256]`→`[256]byte`、`void*` 缓冲→`[]byte`；`uint32`/`byte` 显式转换 + mod-256；返回码 `0/-1`→`error`；`main` 退出码 2/1/0 保留；`argv`→`os.Args`、hex→`encoding/hex`；仅导入 4 个使用到的标准库包。
2. **自审（SELF_REVIEWED）**：一次结构化自审报 0 处转换引入缺陷，`verdict=NO-REPAIR-IDENTIFIED`；列出的风险为运行期/OS 文本模式细节（Windows CRT text-mode stdout CRLF vs Go 二进制 `os.Stdout`），非编译/转换缺陷；测试向量明文无换行，不影响 liveness。无自修轮。
3. **注意**：模型自审 `NO-REPAIR-IDENTIFIED` **只是提交门槛，绝非语法结论**（C01 先例：自审通过仍被第三方工具链定位到未声明符号）。本 run 因 `INFRA_ERROR` 阻断，**语法结论仍为 `INCONCLUSIVE`**，不得据自审倒填 PASS。

## 未决问题与下一步

1. **编译门槛未达成（阻断于基础设施）**。本 run 停在 `EVALUATED`（终态为环境失败），**不进入 `CLOSED`**。按恒就绪政策已用相同输入重试一次并确定性复现；不改用本机编译、不放松命令、不伪造 build 结论。
2. 旧仓库已在独立分支作 Agent 哈希排序的最小本地修正，相关无害工程测试 67/67 通过；仍需按旧仓库流程评审、部署 Windows VM Agent，并以无害 capsule 验证两侧证据。完成远端验收后，才能以**相同 RC4 输入**重提；不通过换 OS、改目标或放松哈希校验绕过。
3. **step-05 `skills/directions/c-to-go` 暂不创建（`BLOCKED`）**：新 Skill 须锚定**真实目标 build 证据**，本 run 未取得，故不搭空架子（AGENTS.md：新目录/机制须有当前消费者与真实证据）。待取得真实 build 证据后再据实反哺。
