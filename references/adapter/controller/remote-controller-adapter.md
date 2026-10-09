# 远端 Controller 适配与连接

> 文档类型：外部评估基础设施的连接与提交适配（reference）
> 状态：ACTIVE（本项目对接已授权隔离第三方 VM Controller 的唯一连接说明）
> 更新：2026-10-05（**runner 能力口径已迁出**：改用[Runner 能力矩阵](runner-capability-matrix.md)作为唯一事实来源；本页只保留连接、capsule 组装、提交流程与回填规则）
> 本页列出已登记的连接坐标和提交契约；实际可用性须在每次评估前核对。

本项目**不建设**运行时或评测平台；编译/运行证据一律由已授权的隔离第三方 VM Controller 返回。本文只记录**如何连接该 Controller、如何组装并提交 comparison capsule、如何回传证据**，供转换 Agent 在评估步骤直接复用。凭据不入库（见“安全边界”）。

## 拓扑与连接坐标

| 角色 | 地址 | 说明 |
|---|---|---|
| Controller（FastAPI HTTP API） | `http://192.168.101.250:8443` | 接收 job、编排 VM Agent、回传证据；2026-10-05 复核 `/api/health` 返回 200、`ready=true` |
| 本机（开发/提交端） | `192.168.101.101` | 与 Controller 同 `192.168.101.0/24` 段，**可直达 8443**，无需 SSH 隧道 |
| VM Agent（三个现役 runner） | 由 Controller 按 `runnerId` 编排 | 提交方**不直连** Agent |

**现役 runner 速查（2026-10-05 由 `GET /api/runners` 实测；完整说明见 [Runner 能力矩阵](runner-capability-matrix.md)）**：

| runnerId | os/x64 | supportedLanguages | 基线快照 | 快照回滚 | 状态 |
|---|---|---|---|---|---|
| `linux-vm-agent-x64` | linux | python、powershell、c、cpp、go、dotnet、**ruby** | `CC-Eval-Linux-8Lang-R12` | true | READY/clean |
| `windows-vm-agent-x64` | windows | python、powershell、c、cpp、go、dotnet、**ruby** | `CC-Eval-Windows-8Lang-R11` | true | READY/clean |
| `macos-vm-agent-x64` | macos | python、powershell、c、cpp、go、dotnet、**ruby** | `CC-Eval-Mac-7Lang-R2` | true | READY/clean |

**Ruby runner 实测**：Windows、Linux、macOS 三台均已登记 `ruby`。Windows/Linux Agent 与 Controller 配置已对齐至各自 R11 快照；无副作用双侧 Ruby job `eval-20261005-055954-f055ab5b` 的两侧语法检查、运行与清理均通过。逐例依赖和具体转换结果仍须单独取证，详见 [Runner 能力矩阵](runner-capability-matrix.md) §1.1。

> 提交前用 `GET /api/runners` 复核 `supportedLanguages`、`lifecycleState`、`baselineSnapshot`、`contaminated`；不要引用其它文档里的历史 runner 清单。

- **首选：直连 HTTP 8443**。本机与 Controller 同网段时，所有 `POST /api/jobs`、轮询、取证据均直接走 HTTP。
- **回退：SSH 端口转发**。若本机不在同段（无法直达 8443），用 `ssh -L 8443:127.0.0.1:8443 Administrator@192.168.101.250` 建隧道后按同样契约连本地 `http://127.0.0.1:8443`。SSH 私钥只在操作者本机 `~/.ssh`，永不入库/入 zip/入 VM 配置/入日志。
- **提交门槛**：已确认的任务/批次授权可复用，到评估步骤逐项核对实际 runner、入口、工具链和隔离后直接提交；历史 READY/健康记录不等于当前可达或已隔离。实际环境故障凭返回诊断归因并在恢复后重提，不改用本机编译或在边界外运行样本。

## API 契约

| 方法 | 路径 | 作用 |
|---|---|---|
| `POST` | `/api/jobs` | multipart 提交 job：`file=<capsule.zip>`、`caseId`、`targetOs`、`targetLang`。返回 `202 {jobId, jobStatus:"QUEUED"}` |
| `GET` | `/api/jobs/{jobId}` | 轮询状态，直到终态：`COMPLETED` / `FAILED_COMPILE` / `FAILED_RUNTIME` / `TIMEOUT` / `INFRA_ERROR` |
| `GET` | `/api/jobs/{jobId}/report` | 结构化评估报告（schema 3.0 JSON） |
| `GET` | `/api/jobs/{jobId}/report.md` | 人读报告 |
| `GET` | `/api/jobs/{jobId}/evidence/source` | 源侧 evidence bundle（build/execution） |
| `GET` | `/api/jobs/{jobId}/evidence/target` | 目标侧 evidence bundle（build/execution） |
| `GET` | `/api/jobs/{jobId}/comparison` | 双侧比较结果 |
| `GET` | `/api/jobs/{jobId}/logs` | Controller 编排日志 |

### 提交结果未知时的恢复

当前登记的接口支持凭 `jobId` 查询；**按客户端提交标识/caseId/capsule 哈希查找已接收 job，以及服务端幂等去重的能力尚未在本说明中核实**。不能据此断言平台不支持，也不能假设 `caseId` 天然幂等。本地提交尝试记录用于追溯，不是服务端去重保证；使用额外查询或幂等能力前须取得现役契约及其匹配范围/保留期限依据，不自造端点或请求字段。

提交可能已被接收但缺回执/jobId 时，保留任务与目标版本、capsule 哈希、本地尝试标识、接收端、请求时间范围和可取得的传输记录，标记 `SUBMISSION_UNKNOWN`。暂停该项重投与相关环境复用，继续不受影响的项；客户端超时、断连或查询暂未命中均不证明服务端没有接收。

恢复只走有证据的出口：

- **找到对应 job**：通过已核实的查询能力或平台提供的接收/作业记录，核对接收端、任务、提交内容/哈希与尝试的对应关系，追加保存 jobId 后继续查询/取证；有多个候选或身份不符时仍保持未知。
- **证明原请求未接收且不会继续入队**：由覆盖该次尝试的平台接收记录或平台明确处置确认支持，再重新核对评估门槛，记录新尝试后提交原 capsule；仅凭空查询结果不能重投。
- **原请求已接收但需重提**：先取得原 job 的身份、终止状态与环境清理/恢复证据，再按原条件另记尝试。取消操作只使用实际支持且在授权范围内的能力，不假设存在取消端点。
- **暂不能确定**：明确待平台补充的接收状态、job 映射或终止/清理证据，保持等待，不记代码失败、不盲重投，也不将可能仍运行的任务标为已收尾。

以上是恢复规则，不表示查询、去重或自动恢复能力已部署/验收；本仓库不为此建设服务端实现。

## comparison capsule 组装

capsule 是提交给 Controller 的 zip，根部必须含以下文件（Controller 会校验必需文件齐全、source/target 树非空、无符号链接/不安全路径）：

```
capsule.zip
├── comparison_manifest.json   # kind=codeconvert-comparison-manifest, schemaVersion "1.0"
├── input_profile.json         # 校验于 input-profile.schema.json（argv/stdin/observationPolicy/comparisonPolicy/timeout/workingDirectory）
├── metadata.json
├── source/                    # 源侧：源文件 + 依赖头 + run_case.py（非空）
│   └── ...
└── target/                    # 目标侧：目标文件 + 依赖头 + run_case.py（非空）
    └── ...
```

- **`comparison_manifest.json`** 关键字段（Controller `validate_comparison_identity` 逐项校验）：`caseId`（与 POST 表单 `caseId` 一致）、`source`/`target` 各自的 `os`、`arch`、`artifactLanguage`、`runCommand`、`buildCommand`。双侧 os/arch/language 必须能被 `resolve_runner_assignments` 匹配到 READY 的 runner。
- **Windows Winsock 构建命令预检**：源侧和目标侧分别检查是否调用 Winsock API；使用 MinGW-w64/UCRT64 的 `gcc`/`g++` 时，若依赖 `WSAStartup`、`socket`、`sendto` 等符号，须在对应构建命令的目标文件之后显式链接 `-lws2_32`。源码中的 MSVC `#pragma comment(lib, "ws2_32.lib")` 不能替代该链接参数。其他编译器按其工具链语法冻结对应库名。
- **评估移交预检**：参考[功能保持与第三方评估指导](../../workflow/behavior-preservation-contract.md)，按已确认任务与当前 Controller 契约移交行为目标、可接受差异和精确/结构/语义比较需求；本仓库不新增比较器或验收标准。核对平台实际支持的用例/维度/策略；若不能表达允许差异或只能观察 output 而任务需其他维度，记录缺口并请求平台调整/用户确认，不静默降级或声称功能 PASS。双侧初始状态与恢复/清理由平台在执行环境中保证，Agent 核对可取得证据。策略与任务不符时保留平台原判定并请求重评，不自行将 FAIL 改 PASS；驱动/输入/比较配置变更另冻条件并重新取证。
- **`input_profile.json`** 通过 `validate_evaluation_contract` 校验：`argv`、`stdin`、`observationPolicy.dimensions`（如 `["output"]`）、`comparisonPolicy`（如 `output.stdoutMode="json-structural"`）、`timeoutSeconds`、`workingDirectory`。
- **`run_case.py`**（若该次契约采用 Python 驱动，两侧各一份）：定位实际构建出的程序，按冻结输入调用并记录输出、退出状态和所需副作用。驱动不得空跑或只输出固定值；`stdoutLen`/`stderrLen` 摘要不能替代行为 oracle。网络、进程和文件权限按安全边界核对。
- 源无可运行入口（库翻译单元无 `main`）时，按冻结记录补写最小中性入口/驱动，并在 `frozen-inputs.md` 标注补写内容和哈希。
- 组装临时目录里**不要**留 `__pycache__`/`*.pyc`；打包前清理，避免污染 zip 与 git。

项目清单 `evaluator_manifest.json` 是移交记录，**不可直接当作**本接口所需的 comparison capsule；以当前 Controller 的实际 schema 组装，原输入与回传证据落于任务输出位置。

## 提交—轮询—取证流程（本会话实测）

PowerShell 5.1 无 `Invoke-RestMethod -Form`；用 `curl.exe -F` 做 multipart。以下为已跑通的形态（占位处按实际替换）：

```powershell
# 1) 打包（先清 __pycache__）
Compress-Archive -Path source,target,comparison_manifest.json,input_profile.json,metadata.json -DestinationPath capsule.zip -Force

# 2) 提交 → 202 {jobId, jobStatus}
curl.exe -sS -X POST "http://192.168.101.250:8443/api/jobs" `
  -F "file=@capsule.zip;type=application/zip" `
  -F "caseId=<frozen-task-id>" `
  -F "targetOs=windows" `
  -F "targetLang=cpp"

# 3) 轮询到终态
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>"

# 4) 取证据（分别保存到 returned-evidence/）
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/report"          # evaluation_report.json
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/report.md"       # evaluation_report.md
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/evidence/source" # evidence-source.json
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/evidence/target" # evidence-target.json
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/comparison"      # comparison.json
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/logs"            # controller.log
```

## 回传证据布局与结论回填规则

- 全部真实回传落于该 run 的 `04-evaluation/<job-dir>/returned-evidence/`（`job-id.txt`、`state.json`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`、`comparison.json`、`controller.log`）。
- **结论只从真实回传证据回填**，不得伪造：
  - `syntaxVerdict`：仅据**目标侧** evidence bundle 的 `build.status=completed` 且 `exitCode=0` 判 `PASS`；只有已实际构建且有代码相关非零退出/编译诊断才判 `FAIL`；未构建、跳过、环境/权限/缓存初始化失败、身份不符或证据不足均为 `UNVERIFIED`，不能仅凭 `failed` 状态归因代码。源侧 build 作对照基线，用于区分“源本身编不过”与“转换引入”。
  - `thirdPartyCompileStatus`：`THIRD-PARTY-COMPILE-PASSED` / `FAILED_COMPILE` / 未提交时 `AWAITING-THIRD-PARTY-COMPILE`。
  - `executionApproved`：本次 capsule 被 Controller 接收并取得回执后置 `true`；证据未返回时编译/行为仍为 `UNVERIFIED`。
  - `behaviorVerdict`：Controller `comparison` 的结果仅按已冻结的行为 oracle 与实际观察范围解释；本编译质量阶段不计入功能率、不外推等价。
- **功能反馈移交**：行为 FAIL/不一致可按[闭环 §3.1](../../workflow/conversion-evaluation-loop.md#31-语法与功能修复反馈分支)进入模型功能修复，但先核对 `report`、双侧 `evidence` 与 `comparison` 的版本身份、输入/状态、预期/实际观察及已接受差异。仅有总 verdict 或缺可定位反例时记待补证据，不假设平台已有字段，也不据此盲修；接口不足向平台反馈。修订后提交新目标版本并取新 job 证据，旧报告不回改，本机不执行比较。
- 自审放行统一按[闭环 §2、§4.1](../../workflow/conversion-evaluation-loop.md)核对原始审阅、追加裁决和剩余阻断项，不以 `NO-REPAIR-IDENTIFIED` 标签单独决定提交；内部预检**不是语法结论**，授权、隔离与评估就绪仍须分别满足。

## 身份哈希故障分流

若 Controller 报 `baselineReference artifactHash does not match uploaded artifact`，先核对提交包和 runner 对相对路径的排序/大小写处理，以及原始 Controller 与 Agent 日志。无 source/target build evidence 时两侧均不能判为编译失败；源侧未落证据不证明故障发生在源→目标交接。任何本地修订或测试记录都不能代替目标 runner 的部署状态核验，也不能倒填到该次原始报告。

## 安全边界

- **凭据永不入库**：API 密钥（仅 `.env` 模型凭证）、SSH 私钥、VMware 密码一律不写入任何文件、zip、VM 配置、报告、日志或聊天。
- SSH 私钥只留操作者本机 `~/.ssh`；加密 VM 的 VMware 口令只经远端 host 环境变量 `CODECONVERT_VMWARE_PASSWORD` 提供，不入 YAML/job 输入/报告/源码控制/聊天。
- 提交的 capsule 不含 `.env`、不含任何密钥；`run_case.py` 仅按冻结契约启动待测程序与获批的中性驱动步骤，不执行任意额外命令、不读敏感文件；网络行为仅在已核验的封闭实验边界内观察，不能连接公网、生产网或真实外部目标。
- 隔离运行：网络固定 loopback/实验网，不打真实外部目标、不用真实凭证、不通过转换新增攻击能力；VM 可回滚快照兜底，结束即销毁临时件。
- 本机不编译、不运行源/目标/构建脚本；一切编译与运行由 Controller + VM Agent 执行并回传证据。
