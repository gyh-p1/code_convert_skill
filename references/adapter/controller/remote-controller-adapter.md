> 现场部署更新（2026-10-12 09:46，北京时间）：四角色统一 1.0.29，原包 health-only 验收通过；Controller ready=true，三 Runner READY/clean，契约 `8090cfcc…` 一致，四角色实现身份可用且 restartRequired=false。新快照已实际恢复，macOS 自动登录通过；comparison/source-preflight 两入口缺字段 422、非法 JSON 400，零新 job。见[部署与快照记录](../../../docs/stages/stage1/reports/1.0.29部署与快照更新记录-2026-10-12.md)。版本/哈希是本次现场事实，样本执行与网络隔离仍逐例核对。

# 远端 Controller 适配与连接

> 文档类型：外部评估基础设施的连接与提交适配（reference）
> 状态：ACTIVE（本项目对接已授权隔离第三方 VM Controller 的唯一连接说明）
> 更新：2026-10-11（当前协议适配；历史部署与 runner 记录只见[能力矩阵](runner-capability-matrix.md)，当前扩展接口见[当前协议适配](platform-revision-adapter.md)，比较字段见[比较策略适配](comparison-policy-adapter.md)）
> 本页列出已登记的连接坐标和提交契约；实际可用性须在每次评估前核对。

本项目**不建设**运行时或评测平台；编译/运行证据一律由已授权的隔离第三方 VM Controller 返回。本文只记录**如何连接该 Controller、如何组装并提交 comparison capsule、如何回传证据**，供转换 Agent 在评估步骤直接复用。凭据不入库（见“安全边界”）。

## 拓扑与连接坐标

| 角色 | 地址 | 说明 |
|---|---|---|
| Controller（FastAPI HTTP API） | `http://127.0.0.1:8443`（Controller 本机回环） | 接收 job、编排 VM Agent、回传证据；2026-10-09 复核 `/api/health` 返回 200、`ready=true`、comparison.preset=noise-tolerant-v1。跨机位仍可经 `http://192.168.101.250:8443` |
| 提交端（转换 Agent 工作区） | 与 Controller **同机** | 经回环直达 8443，不设隧道；**同机不代表隔离**（宿主可连公网），样本执行与网络隔离仍只在 VM Agent，见下《同机共处的边界》 |
| VM Agent（三个现役 runner） | 由 Controller 按 `runnerId` 编排 | 提交方**不直连** Agent |

runnerId、语言与当前快照只在 [Runner 能力矩阵](runner-capability-matrix.md)维护，避免本页重复历史清单。已登记 windows/linux/macos × x64 七语言不等于逐例依赖就绪；C# 的平台语言标识按接口使用 dotnet。历史 Ruby job 仅支持其精确版本，不证明本项转换。

> 提交前用 `GET /api/runners` 复核 `supportedLanguages`、`lifecycleState`、`baselineSnapshot`、`contaminated`；不要引用其它文档里的历史 runner 清单。

- **现役：回环直连**。提交端与 Controller 同机，一律走 `http://127.0.0.1:8443`；`POST /api/jobs`、轮询、取证据均经回环完成。
- **其他机位的回退**：提交端不在 Controller 本机时，跨网段经 `http://192.168.101.250:8443` 直连；同机上的 `ssh -L 8443:127.0.0.1:8443 <self>` 是自转发、**不成立**，不得使用。SSH 私钥只在操作者本机 `~/.ssh`，永不入库/入 zip/入 VM 配置/入日志。
- **提交门槛**：已确认的任务/批次授权可复用，到评估步骤逐项核对实际 runner、入口、工具链和隔离后直接提交；历史 READY/健康记录不等于当前可达或已隔离。实际环境故障凭返回诊断归因并在恢复后重提，不改用本机编译或在边界外运行样本。

## API 契约

Agent 在新提交（含源预检及重提）前，须先按[任务状态 §2.2](../../framework/task-state-contract.md#22-冻结落盘门禁)回读本项本 run 的 `01-frozen/frozen-inputs.md` 并核身份/版本、适用内容与当前条件；缺失、空白或错位不 POST。此检查是提交端的手工前置要求，未新增 multipart 字段或服务端 frozen-inputs 校验，不把文件塞入 source/ 树冒充源码。未知提交的恢复查询、已发生 job 的取证及终止/清理不因缺件延后。

**提交前消费者的引用核对**：Agent 调用 POST /api/jobs 前，按[分类准入](../../workflow/classifier-agent-gate.md)核 ALLOWED、精确源集合/哈希和独立授权/隔离，并保存逐项提交记录。classification 与 batchAuthorization 每次提交均随附，单项亦按最小同形授权；这不免现役身份/协议核验。2026-10-10 的[接入记录](../../../docs/stages/stage1/reports/平台提交端准入闭环接入-2026-10-10.md)记录1.0.28拒收及403 blockingReason，1.0.26忽略额外字段仅属历史；页首最后已知部署为1.0.29，实时能力仍按[当前协议适配](platform-revision-adapter.md)核。不得把旧版本结论或分类器 executionApproved 当当前服务器许可，不从本次文本修订推定服务端运行验证。

| 方法 | 路径 | 作用 |
|---|---|---|
| `GET` | `/api/health` | 服务/组件版本、contractSetHash、ready 与服务器 comparison 配置；字段形状见[比较策略适配 §1](comparison-policy-adapter.md#1-区分服务器配置与任务输入) |
| `GET` | `/api/runners` | 当前 runner、工具链登记、快照与生命周期；不构成网络隔离证明 |
| `POST` | `/api/jobs` | multipart 的 file/caseId/targetOs/targetLang 及必附 classification/batchAuthorization 按当前协议核；identity 按完整 source/ 树覆盖（含实际源侧驱动），不是按扩展名过滤。2026-10-10 的 identity_mismatch/403 与202/QUEUED记录属原版本证据，现役响应/提交身份按协议及本次原回执保存 |
| `GET` | `/api/jobs/{jobId}` | 轮询状态；`COMPLETED` / `FAILED_COMPILE` / `FAILED_RUNTIME` / `TIMEOUT` / `INFRA_ERROR` 标签须联合 closureBlocked、phase 和真实清理核收尾，阻断/未知保持 WAITING |
| `GET` | `/api/jobs/{jobId}/report` | 按 jobKind/evaluationMode 判读：普通双侧 3.0/3.1、双侧仅编译 3.2、独立源预检 SourcePreflightReport 1.0；不能仅按 InputProfile 版本选择报告 |
| `GET` | `/api/jobs/{jobId}/report.md` | 人读报告 |
| `GET` | `/api/jobs/{jobId}/evidence/source` | 源侧 evidence bundle（build/execution） |
| `GET` | `/api/jobs/{jobId}/evidence/target` | 目标侧 evidence bundle（build/execution） |
| `GET` | `/api/jobs/{jobId}/comparison` | 双侧比较结果 |
| `GET` | `/api/jobs/{jobId}/logs` | Controller 编排日志 |

### 仅编译机制（2026-10-11）

当前平台的显式 build-only 复用 `POST /api/jobs` 及原 capsule/分类/批次授权；comparison manifest 设 `evaluationMode=build-only`，两侧必须有真实 buildCommand、不得出现 runCommand，InputProfile 显式无行为观察/运行输入。平台内部使用 AgentRunRequest 1.2，报告为 EvaluationReport 3.2：逐侧 buildAssessment、原始 build evidence、执行未进行、功能 UNVERIFIED，不产 comparison。普通 job 保持原路径。维护资料定位为独立仓库 `third-party-evaluation-system/docs/build-only.md`，不随本仓库交付，不作为转换 Agent 的必读依赖。

仅编译使用 InputProfile 1.0；1.1 强制 functionalProfile，与仅编译冲突，不能静默降级。提交前核实际 health 声明 supportedEvaluationModes 含 build-only、参与角色 contractSetHash/实现身份匹配，再逐项核授权、隔离和构建命令；返回后核双侧原始编译、未运行与清理证据。支持未知或身份不符按[评估准备 §3](../../framework/evaluation-readiness-contract.md#3-无安全可观察入口)记准备缺口，不把普通运行 job 当仅编译。独立 source-only 预检的完整字段、请求与原件/closure 判读见[当前协议适配](platform-revision-adapter.md)；不能先造目标补预检。仅编译不产 comparison，按实际件取证。

### 当前协议的强制适配核对

使用 Controller 渠道时必读[当前协议适配](platform-revision-adapter.md)，按当前协议选择适用形状，并核实际平台身份与能力。该页登记 source-preflights、SourcePreflightReport 1.0、EvaluationReport 3.2、closure/原件导出、submissionId/busy/恢复、追加归因与 v2 配置。`closureBlocked=true` 或 `jobPhase=CLEANING` 不能因 jobStatus 属终态枚举就收尾；平台 closure 不免转换端 result.md 与适用产物门禁。历史 job 缺 closure 时沿用真实原件/清理核对，不造成功记录。

### 提交结果未知时的恢复

当前接口支持凭 `jobId` 查询，以及可选 submissionId 对精确请求的原 job 恢复/去重，见[当前协议适配 §5](platform-revision-adapter.md#5-提交标识busy-与恢复)。没有按 caseId/capsule 哈希通用搜索的接口，不假设 caseId 天然幂等。本地尝试记录不替代服务端保证；首次提交保存 ID/原材料，没有 ID 的历史未知提交不补造 ID 后盲重发。

提交可能已被接收但缺回执/jobId 时，保留任务与目标版本、capsule 哈希、本地尝试标识、接收端、请求时间范围和可取得的传输记录，标记 `SUBMISSION_UNKNOWN`。暂停该项重投与相关环境复用，继续不受影响的项；客户端超时、断连或查询暂未命中均不证明服务端没有接收。

恢复只走有证据的出口：

- **找到对应 job**：通过已核实的查询能力或平台提供的接收/作业记录，核对接收端、任务、提交内容/哈希与尝试的对应关系，追加保存 jobId 后继续查询/取证；有多个候选或身份不符时仍保持未知。
- **证明原请求未接收且不会继续入队**：由覆盖该次尝试的平台接收记录或平台明确处置确认支持，再重新核对评估门槛，记录新尝试后提交原 capsule；仅凭空查询结果不能重投。
- **原请求已接收但需重提**：先取得原 job 的身份、终止状态与环境清理/恢复证据，再按原条件另记尝试。取消操作只使用实际支持且在授权范围内的能力，不假设存在取消端点。
- **暂不能确定**：明确待平台补充的接收状态、job 映射或终止/清理证据，保持等待，不记代码失败、不盲重投，也不将可能仍运行的任务标为已收尾。

以上按当前接口恢复原回执；不提供自动重放、通用搜索或取消端点，本仓库不为此建设服务端实现。

### batchAuthorization 字段与来源

以下摘出已登记提交契约中 Agent 必须消费的字段；开发期 Spec05 仅作来源记录，不是运行时加载依赖。实际服务端 schema/回执优先，本轮未连接验证。授权只能据真实人工授权与现场证据填写，不把布尔占位或字段校验当隔离证明。

| 字段 | 登记的类型/校验 |
|---|---|
| batchId | 非空 string，与任务批次身份一致，目录名不替代身份 |
| authorizedAt / authorizedBy | UTC ISO-8601 时间，不晚于提交；可追责人工身份，非空 |
| vmIsolation.confirmed / snapshotRollback / cleanupVerified | bool，须为 true；各自须有真实依据 |
| networkIsolation.configured | bool；公网/hostname 目标的 ALLOWED 项须 true。private/loopback 的接口豁免不免项目逐例隔离 |
| networkIsolation.publicNetworkBlocked / experimentalNetworkOnly | configured=true 时须 true |
| networkIsolation.verificationEvidence / verifiedAt | configured=true 时非空可复核证据与 UTC 时间，时间不晚于提交 |
| dataSource.syntheticDataOnly / noRealCredentials / noProductionData | bool，须 true |
| dataSource.confirmation | 非空说明真实数据审阅依据 |
| scope | 登记的唯一字符串为“所有非BLOCKED任务”；不自造 taskId 范围字段。单项以最小单项批次关联覆盖 |
| validUntil | UTC 时间，晚于 authorizedAt，提交时未过期 |
| contractHash | 与实际 health 的 contractSetHash 对应，不替代源码/目标哈希 |

任一必填/条件必填缺失、无效或授权过期，覆盖该授权的提交暂停，不逐项降级放行；只阻断独立分类的项则记录该项原因。每次提交单项 classification 对象与授权 JSON，单项也必附。服务端不 lift 旧 BLOCKED，不以 configured=true 改判；条件解除后重新分类取得 ALLOWED。

来源：[Spec05 字段与实现修正](../../../docs/stages/stage1/specs/submission-and-batch-authorization.md)。历史规格中的旧伪代码与允许率不是本项目的执行规则或质量指标。

## 批量提交（单批 ≥40 项，允许排队）

批量编排规则见[批量转换工作流](../../../skills/workflows/batch-conversion/SKILL.md)；本节只记录**适配层**已知事实，不重复编排语义。批量任务与单项走同一个 `POST /api/jobs`，**没有**批量提交端点。

| 事项 | 已核实事实 | 未核实/须现场核对 |
|---|---|---|
| 提交粒度 | 每项一个 capsule、一次 `POST /api/jobs`，逐项取 jobId | 平台是否提供批量端点（当前无，不自造） |
| 并发 | 项目默认串行 1 路；`GET /api/runners` 现役 3 个 READY runner 是**容量事实，不是并发许可** | 平台级并发上限、队列深度、单批是否被限流 |
| 排队状态 | 提交返回 `202 {jobId, jobStatus:"QUEUED"}`，说明存在排队阶段 | 队列位置/预估等待字段 |
| 轮询间隔 | 无平台声明值 | **须按契约记录实际轮询间隔**；批量流程 §2 要求"轮询间隔按契约记录"，而平台未提供该值，故由本任务冻结时自定并留证 |
| 忙碌/未就绪 | 历史审阅提及 409/controller_busy、503/controller_not_ready，曾记录在创建 job 前拒收 | 当前部署未经本轮复核；只有覆盖该次请求的契约/接收证据证明未创建才可重提，不外推到任意错误/超时 |
| 幂等 | submissionId 支持精确材料恢复原 job，不支持通用 caseId/capsule 搜索 | 按当前协议适配核原 ID/材料；没有 ID 的历史未知提交沿用未知提交门禁，不盲重投 |
| 隔离 | 三 Runner 均 READY/clean；**READY 与快照回滚都不是网络隔离证明** | 批次级网络隔离证据（`batch-authorization.json`）仍待现场 |

**批量提交的引用核对**：逐项核 ALLOWED、精确输入、独立授权/隔离，再提交。字段只见本页 batchAuthorization 节；分类逐项消费。单项条件不足记原因，可继续独立未受影响项；共享批次授权无效则暂停其全部覆盖项，不把等待记目标失败。

**批量取证**：逐项按"回传证据布局与结论回填规则"落盘到该 run 的 `04-evaluation/<job-dir>/returned-evidence/`；批次汇总按批量流程 §6 分列各维度，**不合成单一"转换成功率"**。

> 1.0.28 健康验收只覆盖四角色 health-only（另已完成接口必填/解析拒收检查）：**未提交任何样本、未验证批次链路、未取得批次隔离证据**。上述"未核实"列是真实缺口，不得因三 Runner READY 就当已具备批量能力。

## 比较 capsule 组装

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

- **`source/`、`target/` 必须携带冻结构建命令消耗的每个文件**（声明的翻译单元 + 同目录伴随头/源），不是只带主文件；缺伴随文件导致的构建错误是**打包缺口**，按[构建前提 §0.1](../../workflow/build-prerequisites.md)补齐组装后重测，不作源侧判定（2026-10-09 D2-025 实证）。
- **`comparison_manifest.json`** 关键字段（Controller `validate_comparison_identity` 逐项校验）：`caseId`（与 POST 表单 `caseId` 一致）、`source`/`target` 各自的 `os`、`arch`、`artifactLanguage`、`runCommand`、`buildCommand`。双侧 os/arch/language 必须能被 `resolve_runner_assignments` 匹配到 READY 的 runner。
- **Windows Winsock 构建命令预检**：源侧和目标侧分别检查是否调用 Winsock API；使用 MinGW-w64/UCRT64 的 `gcc`/`g++` 时，若依赖 `WSAStartup`、`socket`、`sendto` 等符号，须在对应构建命令的目标文件之后显式链接 `-lws2_32`。源码中的 MSVC `#pragma comment(lib, "ws2_32.lib")` 不能替代该链接参数。其他编译器按其工具链语法冻结对应库名。
- **评估移交预检**：参考[功能保持与第三方评估指导](../../workflow/behavior-preservation-contract.md)，按已确认任务与当前 Controller 契约移交行为目标、可接受差异和精确/结构/语义比较需求；本仓库不新增比较器或验收标准。核对平台实际支持的用例/维度/策略；若不能表达允许差异或只能观察 output 而任务需其他维度，记录缺口并请求平台调整/用户确认，不静默降级或声称功能 PASS。双侧初始状态与恢复/清理由平台在执行环境中保证，Agent 核对可取得证据。策略与任务不符时保留平台原判定并请求重评，不自行将 FAIL 改 PASS；驱动/输入/比较配置变更另冻条件并重新取证。
- **`input_profile.json`** 通过 `validate_evaluation_contract` 校验：`argv`、`stdin`、`observationPolicy.dimensions`（如 `["output"]`）、`comparisonPolicy`（如 `output.stdoutMode="json-structural"`）、`timeoutSeconds`、`workingDirectory`。
- **本版比较策略接入**：按[比较策略适配](comparison-policy-adapter.md)分别冻结 stdout/stderr 模式、文件采集与比较范围以及服务器实际 comparison 配置。`normalized-text` 会采用服务器启用的消噪规则，关键值需选择适当的严格模式/文件保护；服务器 preset、token 或容忍开关不是任务输入字段。
- **`run_case.py`**（若该次契约采用 Python 驱动，两侧各一份）：定位实际构建出的程序，按冻结输入调用并记录输出、退出状态和所需副作用。驱动不得空跑或只输出固定值；`stdoutLen`/`stderrLen` 摘要不能替代行为 oracle。网络、进程和文件权限按安全边界核对。**源侧驱动 `source/run_case.py` 位于 `source/` 树，须随源文件一同提交给分类器并被 `classification.details.files[]` 覆盖**——平台 identity 门禁按 `source/` 文件集合校验（非按扩展名），未覆盖即 `403 identity_mismatch`（见[分类结果准入 §3](../../workflow/classifier-agent-gate.md)）。驱动改名为非源扩展名（如 `.txt`）不绕过门禁；**驱动放 capsule 根不生效**——平台只解压 `source/`、`target/`，根级文件不落盘、执行 `exitCode=2`（2026-10-10 实测）。
- 驱动/中性入口仅引用合法提供版本，不由 Agent 或模型新造。本轮无法合法行为评估但源构建通过时，按[评估准备 §1.3](../../framework/evaluation-readiness-contract.md#13-lib_unobservable_compile_only-的转换与交付)记 LIB_UNOBSERVABLE_COMPILE_ONLY，继续转换并验证目标语法/编译；本轮缺入口与结构性无安全观察分别记原因。不以带 runCommand 的普通运行 job 冒充仅编译，支持未知只停受影响验证。
- 组装临时目录里**不要**留 `__pycache__`/`*.pyc`；打包前清理，避免污染 zip 与 git。

项目清单 `evaluator_manifest.json` 是移交记录，**不可直接当作**本接口所需的 comparison capsule；以当前 Controller 的实际 schema 组装，原输入与回传证据落于任务输出位置。

**生成前源侧预检**：使用现役平台已支持、获授权的预检提交形态，分类/授权随附规则相同；不提前生成转换目标来补包，也不自造平台字段。需行为评估时，源侧须按冻结条件真实构建、运行、观察与终止/清理，回传源 build、execution 和原始观察供[评估准备 §1.1](../../framework/evaluation-readiness-contract.md#11-生成前源侧预检)判读，不能只读 build 摘要。实际 job 的回执与证据归入 `job-00-source-buildability/`，目录名不禁止源运行；不适用运行的文本/片段/仅编译任务须核对应安全构建形态并记录理由。接口支持未知时待准备；本页的普通双侧 capsule 示例不构成源预检形态或仅编译能力已验收的证明。

独立源预检按[当前协议适配 §2](platform-revision-adapter.md#2-独立源侧预检请求)使用 source-only 请求；实际平台身份不符、能力或本项前置条件缺失时记 PREPARATION_GAP，按统一收尾入口暂停，不发送普通双侧示例或伪 target。已有适用授权与精确契约依据沿用，不重复请求授权。

## 提交—轮询—取证流程（本会话实测）

PowerShell 5.1 无 `Invoke-RestMethod -Form`；用 `curl.exe -F` 做 multipart。以下基于已有请求形态补充手工保存回执，保存参数未在本轮实测；占位处按本项冻结事实替换。正常双侧用例按下例，仅编译按当前协议删 runCommand、核实际不运行支持；本例的运行/比较件不强加给 LIB 分支。

```powershell
# 0) 只读取证，保存服务器比较配置与 runner；同时按安全边界逐例核对授权/隔离
curl.exe --fail -sS "http://127.0.0.1:8443/api/health" -o controller-health-before.json
curl.exe --fail -sS "http://127.0.0.1:8443/api/runners" -o runners-before.json
# 核对 ready、comparison、契约与本次任务策略；配置不适用时先处理受影响项

# 1) 核完整源/目标树和清单，仅归档冻结输入，不修改只读源来清缓存
Compress-Archive -Path source,target,comparison_manifest.json,input_profile.json,metadata.json -DestinationPath capsule.zip -Force

# 2) 提交 → 202 {jobId, jobStatus}
#    每次提交**必附**两份已准备好的 JSON（重新部署后服务端强制，之前被忽略）：
#    - classification：本项（单个 taskId）的分类器输出行——从该项 01-frozen 的
#      当前适用的 classification-<N>.json 中取出**对应这一 taskId 的那一个对象**（不是整个数组；不固定沿用编号 1），
#      其 id/dir/case 必须与本 capsule 一致，details.files[].sha256 必须覆盖
#      **本 capsule source/ 树的每个文件（含源侧驱动 run_case.py）**——
#      identity 门禁按文件集合校验，缺任一 source/ 文件即 403 identity_mismatch；
#    - batchAuthorization：本批人工签署的 batch-authorization.json（本页字段节）；
#      **单文件任务按"批次为一"附一份覆盖该单项的最小 batch-authorization.json**。
#    curl 的 `=<文件名` 形态把文件内容作为该表单字段的文本值发送。
#    未准入时返回 403 {detail:{blockingReason,...}}，据原因修复，不手改 JSON 绕过。
curl.exe -sS -o submission-body.json -w "%{http_code}" -X POST "http://127.0.0.1:8443/api/jobs" `
  -F "file=@capsule.zip;type=application/zip" `
  -F "caseId=<frozen-task-id>" `
  -F "targetOs=windows" `
  -F "targetLang=cpp" `
  -F "classification=<this-task-classification.json" `
  -F "batchAuthorization=<batch-authorization.json" `
  -F "submissionId=<saved-exact-submission-id>" > submission-http-status.txt

# 3) 轮询并核 closureBlocked/phase/清理；阻断或未知继续 WAITING
curl.exe -sS "http://127.0.0.1:8443/api/jobs/<jobId>"
curl.exe --fail -sS "http://127.0.0.1:8443/api/jobs/<jobId>/closure" # closure.json

# 4) 取证据（分别保存到 returned-evidence/）
curl.exe -sS "http://127.0.0.1:8443/api/jobs/<jobId>/report"          # evaluation_report.json
curl.exe -sS "http://127.0.0.1:8443/api/jobs/<jobId>/report.md"       # evaluation_report.md
curl.exe -sS "http://127.0.0.1:8443/api/jobs/<jobId>/evidence/source" # evidence-source.json
curl.exe -sS "http://127.0.0.1:8443/api/jobs/<jobId>/evidence/target" # evidence-target.json
curl.exe -sS "http://127.0.0.1:8443/api/jobs/<jobId>/comparison"      # comparison.json
curl.exe -sS "http://127.0.0.1:8443/api/jobs/<jobId>/logs"            # controller.log
curl.exe --fail -sS "http://127.0.0.1:8443/api/health" -o controller-health-after.json
```

POST 前保存本 attempt 精确材料/版本及适用 submissionId；回读 submission-http-status.txt 与原 body，并记实际工具退出码/传输诊断，不能把 curl 退出码 0 当 HTTP 成功。错误 body 同样保留；无有效回执、000/超时等按当前协议恢复原尝试，不盲重投。上方取证命令展示路由，每件用该命令的 `-o` 保存到 returned-evidence 的实际落点并核 HTTP/正文身份；仅在屏幕打印不算落盘，不把错误页面充作原件。

## 回传证据布局与结论回填规则

- 全部真实回传落于该 run 的 `04-evaluation/<job-dir>/returned-evidence/`；`job-id.txt` 留在 job 目录。按实际 jobKind/evaluationMode 保存报告、适用侧 evidence、logs、closure 及 health/runner 留证：源预检不要求目标件，双侧仅编译不要求 execution/comparison，不能按普通双侧清单造件。
- **结论只从真实回传证据回填**，不得伪造：
  - `syntaxVerdict`：仅据**目标侧** evidence bundle 的 `build.status=completed` 且 `exitCode=0` 判 `PASS`；只有已实际构建且有代码相关非零退出/编译诊断才判 `FAIL`；未构建、跳过、环境/权限/缓存初始化失败、身份不符或证据不足均为 `UNVERIFIED`，不能仅凭 `failed` 状态归因代码。源侧 build 作对照基线，用于区分“源本身编不过”与“转换引入”。
  - `thirdPartyCompileStatus`：`THIRD-PARTY-COMPILE-PASSED` / `FAILED_COMPILE` / 未提交时 `AWAITING-THIRD-PARTY-COMPILE`。
  - `executionApproved`：复用已有授权并逐例通过隔离核对，本次 capsule 被获批 Controller 接收且取得回执后置 `true`；接收回执本身不创建运行授权，证据未返回时编译/行为仍为 `UNVERIFIED`。
  - `behaviorVerdict`：正常双侧行为 job 取回源/目标两侧的 `execution` 与 `comparison`，按已冻结的行为 oracle 与实际观察范围解释一致/差异；双侧仅编译分支不要求这些未发生件，功能 `UNVERIFIED`。源预检只支持源基线，不产生目标功能结论。无冻结 oracle、平台未观察到对应维度或证据不足时写 `UNVERIFIED`。始终分层（build / execution / comparison 分开），不合成单一功能率、不外推普遍等价、不以编译或自审推断功能。
- **消噪证据**：按[比较策略适配 §4–5](comparison-policy-adapter.md#4-次要差异容忍与结果解释)保存平台原 `semantic_pass`、minor diff、原始观察及实际配置；job COMPLETED 不等于代码通过，semantic_pass 不等于 build PASS，配置不适用不自动进入模型修复。

功能统计消费[评估准备§5.1](../../framework/evaluation-readiness-contract.md#51-有效性消噪与功能分类的次序)：有效matched和semantic_pass都计冻结范围比较通过，仍保留两类、允许差异与未覆盖。候选评估源码的原始摘要/通道引用/人读小计修订不证明在线版本已更新；先核部署/producer身份。缺state的接受记录属于恢复故障，不据查不到状态判断未提交；清理未知仍等待，不触及Controller安装目录手改原件或自动重投。
- **功能反馈移交**：行为 FAIL/不一致可按[闭环 §3.1](../../workflow/conversion-evaluation-loop.md#31-语法与功能修复反馈分支)进入模型功能修复，但先核对 `report`、双侧 `evidence` 与 `comparison` 的版本身份、输入/状态、预期/实际观察及已接受差异。仅有总 verdict 或缺可定位反例时记待补证据，不假设平台已有字段，也不据此盲修；接口不足向平台反馈。修订后提交新目标版本并取新 job 证据，旧报告不回改，本机不执行比较。
- 自审放行统一按[闭环 §2、§4.1](../../workflow/conversion-evaluation-loop.md)核对原始审阅、追加裁决和剩余阻断项，不以 `NO-REPAIR-IDENTIFIED` 标签单独决定提交；内部预检**不是语法结论**，授权、隔离与评估就绪仍须分别满足。

## 身份哈希故障分流

若 Controller 报 `baselineReference artifactHash does not match uploaded artifact`，先核对提交包和 runner 对相对路径的排序/大小写处理，以及原始 Controller 与 Agent 日志。无 source/target build evidence 时两侧均不能判为编译失败；源侧未落证据不证明故障发生在源→目标交接。任何本地修订或测试记录都不能代替目标 runner 的部署状态核验，也不能倒填到该次原始报告。

## 同机共处的边界

提交端（转换 Agent 工作区）与评判端（Controller）现同处一台远端宿主，**宿主本身可连公网**；样本的编译/运行仍只在 VM Agent 内进行，网络隔离由 VM 层施加，**不由这台宿主提供**。因此：

- 该宿主上的 Agent **不得读取、写入、枚举或修改** Controller 安装目录及其 `jobs/`（`D:\CodeConvertRemote\Stack\`）——不借同机便利直接查看/改动 job 存储、证据或比较中间件。评判端与被评估端的物理共处**不改变**两者的授权边界。
- 同机**不构成隔离证明**：宿主可连公网，`READY`/`clean`/快照回滚仍不等于网络已隔离；回环可达 Controller 也不等于样本已与公网断开。
- 双角色共用宿主资源；该宿主**不承载**样本的编译/运行，样本执行与网络隔离仍只在 VM Agent 内，按本页《安全边界》与[安全边界](../../framework/safety-boundary.md)逐例核对。

## 安全边界

- **凭据永不入库**：API 密钥（仅 `.env` 模型凭证）、SSH 私钥、VMware 密码一律不写入任何文件、zip、VM 配置、报告、日志或聊天。
- SSH 私钥只留操作者本机 `~/.ssh`；加密 VM 的 VMware 口令只经远端 host 环境变量 `CODECONVERT_VMWARE_PASSWORD` 提供，不入 YAML/job 输入/报告/源码控制/聊天。
- 提交的 capsule 不含 `.env`、不含任何密钥；`run_case.py` 仅按冻结契约启动待测程序与获批的中性驱动步骤，不执行任意额外命令、不读敏感文件；网络行为仅在已核验的封闭实验边界内观察，不能连接公网、生产网或真实外部目标。
- 隔离运行：网络固定 loopback/实验网，不打真实外部目标、不用真实凭证、不通过转换新增攻击能力；VM 可回滚快照兜底，结束即销毁临时件。
- 本机不编译、不运行源/目标/构建脚本；一切编译与运行由 Controller + VM Agent 执行并回传证据。
