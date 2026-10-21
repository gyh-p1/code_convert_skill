# Controller 当前协议适配：源侧预检、收尾与恢复

> 状态：ACTIVE，转换系统对评估平台协议的适配。任务按本页选择请求、报告、取证与恢复形状，并保存实际 health/回传身份；支持声明不替代本项构建、行为、驱动合法性或网络隔离证据。

本页随转换仓库离线交付，定义需消费的字段与形状，不要求读取相邻评估仓库。评估提交前核实际平台身份与声明能力；字段/路由缺失或版本不符时记录准备缺口，不猜填 capability。连接与普通双侧请求沿用[Controller 适配](remote-controller-adapter.md)，门禁分别消费[任务状态](../../framework/task-state-contract.md)、[评估准备](../../framework/evaluation-readiness-contract.md)、[交付](../../framework/delivery-handoff-contract.md)、[安全边界](../../framework/safety-boundary.md)。适配文本不产生样本执行授权。

## 1. 启用前核对版本与能力

先按[评估准备 §1.0](../../framework/evaluation-readiness-contract.md#10-转换前可达性检查与仅转换分支)及[连接适配](remote-controller-adapter.md#转换前可达性检查)检查第三方评估系统可达性。不可达仅转换、自审及报告，不要求虚填本页实时平台/runner 证据或源构建，不发评估 job；可达后才落实本页动态提交条件。服务可达但版本/能力/就绪不足仍按原准备规则，不当不可达。未决 job 不因健康检查失败解除 WAITING。

手工保存实际 `/api/health`、`/api/runners` 和平台提供的参与 Agent health/发布身份资料；不读取 Controller 安装目录或 jobs。当前字段：

| 字段/事实 | 消费方式 |
|---|---|
| `supportedJobKinds` | Controller 含 comparison/source-preflight；按本项任务选择入口，支持声明不代替独立执行授权 |
| `supportedEvaluationModes` | Controller/参与 Agent 对应 build-and-run 或 build-only；仅编译须两端明确支持 |
| `contractSetHash` | Controller、参与 Agent、batchAuthorization.contractHash 与本项所用 schema 集合对应；集合改变即重新核全哈希，不沿用不适用数值 |
| `implementationIdentity.available/components/restartRequired` | 保存 Controller/Agent 产品启动身份及 evaluationCore 身份；available=true、restartRequired=false，并与部署材料对应。不存在/不明记身份缺口；同一版本标签或契约 hash 不替代实现身份 |
| `ready`、runner readiness、快照、clean | 只核当前调度/恢复状态；另核逐项网络/数据边界、合法入口、观察四要素与真实清理 |
| `comparison` | 保存实际 preset、token、目录映射与容忍配置；按[比较适配](comparison-policy-adapter.md)冻结，不在 capsule 内伪造服务器配置 |

模块启动 hash 不证明所有已加载内存、依赖、工具链或隔离；产品文件改变须重启，Controller/Agent 拒绝新执行。普通组件 version 仍可能为 1.0.0，不能凭这个标签认定新包已生效。支持列表不增加 network/registry collector 或事件级 oracle。

保存本项现场 health，核 Controller、参与 Agent、授权及所用 schema 的 contractSetHash 相符，不沿用其他任务的数值。releaseVersion、manifestHash 和产品启动身份分别关联，不把“同一契约 hash”当成实现、工具链或隔离证明。

### 1.1 提交前身份、时刻与启动路径对齐

在既有冻结／attempt 材料中手工对齐以下内容，不另建请求校验脚本、探针或新平台字段：

| 对象 | 核对内容及错误分流 |
|---|---|
| case 与方向 | POST caseId、manifest caseId、分类 case 及其源→目标方向逐项对应；本地 taskId、目录显示名不代替平台 case 身份 |
| 文件集合 | 提交 source/ 的完整相对路径与字节哈希按分类准入双向核对；403 identity_mismatch 不一律通过重分类解决，先分清文件变化还是请求字段错位 |
| C# 语言身份 | 源／目标 manifest 和表单采用与分类／本接口一致的身份；runner supportedLanguages 中的 dotnet 能力别名不能直接覆盖 csharp，见[能力矩阵](runner-capability-matrix.md#1-runner-与语言登记) |
| 授权／时刻 | 同时核真实授权、有效期、contractHash、UTC 与隔离核验时刻；时间修正有原事实依据，不伪造更早时间 |
| 构建／启动 | 工作目录、工程配置、产物名／扩展名和真实入口一致；Windows 当前目录中的 exe 采用该执行契约支持的显式相对路径（如 `.\program.exe`），不假定当前目录已在 PATH |
| 观察／独立断言 | 输入确实传入合法入口；作者断言材料与平台支持的 functionalProfile 形状分别核对，不用 1.0 受理结果冒充独立 oracle 已消费 |

拒收按 HTTP 数字、原 body、传输状态及是否建 job 分流；000／超时仍按未知提交处理，不能当作确定拒收。字段错误修正后另记真实 attempt，已有失败不覆盖。成功受理不证明启动、输入送达或功能通过。

## 2. 独立源侧预检请求

先回读本项本 run 的 `01-frozen/frozen-inputs.md`，完成分类 ALLOWED/独立授权与本次准备核对，再用 `POST /api/source-preflights`。multipart 字段为：

| 字段 | 内容 |
|---|---|
| file | 本项 source-only capsule.zip |
| caseId / sourceOs / sourceLang | 与 manifest、classification、冻结条件一致；sourceLang 是源语言，不填写目标语言 |
| classification / batchAuthorization | 对应本项的单个 JSON 分类对象及有效授权 JSON，每次必附；沿用普通 job 服务端准入 |
| submissionId（可选） | 按 §5 保存并传入的精确提交标识，用于恢复原请求回执 |

Capsule 只包含 `source_preflight_manifest.json`、`input_profile.json`、`metadata.json`、非空 `source/` 树及适用既有 `fixtures/`。禁止 target 树、伪目标、重复 ZIP 项、路径穿越、符号链接和额外根文件。classification 覆盖 source 树全部实际文件，包括合法来源入口/声明配置；保留完整相对路径的冻结身份，不以同名覆盖或漏分类来补包。

源 manifest 形状如下；占位值必须替换为实际冻结事实，不执行示例命令：

```json
{
  "schemaVersion": "1.0",
  "kind": "codeconvert-source-preflight-manifest",
  "caseId": "frozen-case",
  "conversionDirection": "cpp-to-python",
  "evaluationMode": "build-and-run",
  "inputProfileRef": "input_profile.json",
  "source": {
    "os": "windows", "arch": "x64", "artifactLanguage": "cpp",
    "buildCommand": ["the-approved-build-command"],
    "runCommand": ["the-approved-existing-entry"],
    "timeoutSeconds": 20
  }
}
```

方向字段仅记录拟转换目标用于准入，预检没有目标执行/比较。source buildCommand 必需；build-and-run 还需真实合法 runCommand，超时 1–3600 秒。完整 InputProfile 沿用已支持 1.0/1.1 字段；1.1 携带 functionalProfile，需匹配 caseId 与申请维度。行为预检必须核约定状态、原观察和清理，不能因未填 oracle 的示例结构可受理就认为有效基线。

`input_profile.json` 的完整 1.0 最小形状如下。profileId、argv/stdin、environment、工作目录、超时、fixture 和观察/比较条件必须取自本项冻结记录；这里的空数组/null/空对象只展示形状，不能覆盖实际输入或静默取消观察义务。InputProfile 的 timeoutSeconds 范围为 **1–900**，与源 manifest 的 1–3600 分开核对。

```json
{
  "schemaVersion": "1.0",
  "kind": "codeconvert-input-profile",
  "profileId": "frozen-case-source-baseline",
  "argv": [],
  "stdin": null,
  "environment": {},
  "workingDirectory": "workspace",
  "timeoutSeconds": 20,
  "fixtures": [],
  "observationPolicy": {"dimensions": ["output"]},
  "comparisonPolicy": {
    "output": {"stdoutMode": "exact", "stderrMode": "exact"}
  }
}
```

此 1.0 形状不携带独立 functionalProfile，因此平台 baselineAssessment 为 UNVERIFIED；行为任务还须有冻结观察目标及独立可复核的实际源观察依据，不能用示例受理或 build 成功代替有效基线。需要平台判定已支持的独立断言时，使用本项已冻结的完整 InputProfile 1.1/functionalProfile，不能只改 schemaVersion；没有合法断言材料则先准备，不倒填 PASS。

`metadata.json` 是必需的 JSON 对象；无附加元数据时完整内容为 `{}`，不能省文件、写空文本或 null。它不代替 manifest、冻结记录、classification 或授权。存在 fixture 时，每项声明含 relativePath、真实 contentDigest、sizeBytes、mediaType 和可空 sourceArtifactRef，并携带对应既有 fixture 原件；没有 fixture 才使用 `fixtures=[]`。不填写假 hash 或新造 fixture/驱动。

明确仅编译时：mode 改 `build-only`，**删除 runCommand 键**，采用 InputProfile **1.0**，argv=[]、stdin=null、observationPolicy.dimensions=[]、comparisonPolicy={}，无 functionalProfile。InputProfile 1.1 强制 functionalProfile，与仅编译冲突，不能直接套用或静默降版本。本项无法合法行为评估时，按[评估准备 §1.3](../../framework/evaluation-readiness-contract.md#13-lib_unobservable_compile_only-的转换与交付)明确冻结 LIB_UNOBSERVABLE_COMPILE_ONLY，再采用上述形状取得源构建及目标语法/编译证据；不改平台 schema、不新增 capability、不补造入口。仅编译支持未知阻止该验证提交，不把已满足条件的生成也停掉。

源侧 `buildCommand` 的外壳解释与解析结果采信同样消费[构建命令传递与解析证据](remote-controller-adapter.md#构建命令传递与解析证据)，不因 source-only 或 build-only 而省略；合法解析入口及实际文件消费须对应本项冻结版本。

手工打包与提交形状（满足本项前置门槛后使用；有 fixture 时把既有 fixture 树纳入本项归档）：先按[ZIP 条目与打包核对](remote-controller-adapter.md#zip-条目与打包核对)使用已核验原生工具、回读正斜杠条目和完整集合，再提交；下例从本项组装目录执行。

```powershell
& "$env:SystemRoot\System32\tar.exe" -c --format=zip -f source-preflight-capsule.zip source source_preflight_manifest.json input_profile.json metadata.json
& "$env:SystemRoot\System32\tar.exe" -tf source-preflight-capsule.zip > source-preflight-capsule-entries.txt
# 回读条目清单，确认本项归档形态与冻结集合后再提交
curl.exe -sS -o source-preflight-submission-body.json -w "%{http_code}" -X POST "http://127.0.0.1:8443/api/source-preflights" `
  -F "file=@source-preflight-capsule.zip;type=application/zip" `
  -F "caseId=<frozen-case-id>" -F "sourceOs=<frozen-source-os>" -F "sourceLang=<frozen-source-lang>" `
  -F "classification=<classification.json" -F "batchAuthorization=<batch-authorization.json" `
  -F "submissionId=<saved-exact-submission-id>" > source-preflight-submission-http-status.txt
```

这是一项一命令的参考形状，不写辅助脚本、循环、打包/请求程序或新驱动。先保存本 attempt 的精确材料和 submissionId，再发送；body 与 HTTP 数字分别落盘，并在既有记录记原生工具实际退出码/传输错误。POST 不使用会丢弃错误 body 的 --fail；工具退出码为 0 不证明 HTTP 受理。受理可为 202/QUEUED，同步形态可为 200/当前状态，不假定只有 202 才受理。403/409 等保留原文按实际契约判读；000/超时不证明未接收，转 §5 恢复，不手改分类或盲重投。

本节是获授权任务使用的请求契约，不是某一项的执行批准。classification 和 batchAuthorization 必须来自该项真实分类及适用人工授权，源文件集合、授权有效期/contractHash、当前平台身份和逐例隔离分别核对；已有适用授权可复用，不因本页补充示例重复申请。缺任一适用件时记具体 PREPARATION_GAP/WAITING 并写 result.md，不先生成目标凑包。

## 3. 报告 kind 与分层判读

source-only 的 `/api/jobs/{jobId}/report` 返回 **SourcePreflightReport 1.0**，kind=`codeconvert-source-preflight-report`；不是双侧 EvaluationReport。通过相同 job 状态、report.md、evidence/source、closure 路由取证；没有 target bundle 或 comparison，不要求伪造它们。源预检全部原件仍归既有 `job-00-source-buildability/returned-evidence/`。

源原件采信及生成前/双侧提交前的逐项落实消费[评估准备 §1.4](../../framework/evaluation-readiness-contract.md#14-源预检采信与双侧对齐核对)。采用占位目标的源预检 job 保留原标签，其 comparison 不当转换结论；不将 source-only 缺 target/comparison 误判为缺档。

| 字段 | 判读 |
|---|---|
| sourceRuntime | 源 os/arch/artifactLanguage，不是目标身份 |
| buildAssessment | 单个 passed/failed/inconclusive；passed 须原 build.completed/实际整数 0。语法/依赖/链接原因仍读编译器原诊断 |
| executionAssessment | completed 仅表示执行完成、真实整数退出码且未超时；not-requested 用于仅编译。非零可为冻结预期错误路径 |
| baselineAssessment.status/reasons | PASS 仅支持的关键独立期望断言；缺 oracle/不符/未支持为 UNVERIFIED，仅编译为 NOT_APPLICABLE。PASS 不单独证明驱动转发、程序输出来源或完整业务覆盖 |
| evidenceBundleRef | evidence/source.json 或 null；没有实际编译/运行不补造 bundle |
| cleanup.status/reason | passed/failed/unknown/not-started，必须关联原清理记录；READY 不替代 |
| jobStatus/jobPhase | 编排/收尾事实，不等于源可构建或可进入转换模型 |

系统可达的正常流程生成前仍核精确源 build completed/0、授权隔离与适用清理；正常行为分支还须有效源基线，缺口先停该分支。源构建已过而本轮无法合法行为评估时，按评估准备 §1.3 记录 LIB_UNOBSERVABLE_COMPILE_ONLY 后继续生成与目标语法/编译验证，不能把“任何观察缺口”写成禁止转换调用。不可达仅转换按评估准备 §1.0 回读检查原件，不要求未发生源预检。没有独立 oracle 的平台 UNVERIFIED 不改 PASS，实际观察无有效依据不假称基线通过。

双侧普通报告沿用 3.0/3.1；双侧仅编译为 EvaluationReport **3.2**，kind 不变，逐侧 buildAssessment，execution.performed=false、comparisonRef=null、功能 UNVERIFIED。不能按 source-only 标量读双侧对象，也不能硬把 source-only 报告转成双侧 3.x。旧消费者遇未知 kind/version 停受影响判读。

InputProfile 1.0 未提供独立 functionalProfile 时，baselineAssessment 的 UNVERIFIED／independent-frozen-oracle-not-provided 只表示该独立断言层缺依据，不自动推断源执行失败或装置无效。正常行为基线仍按评估准备核冻结期望与真实源观察；确有依据时说明有限采信范围，平台标签原样保留，缺观察不补 PASS。反之 codeVerdict=inconclusive 不抹去双侧 build 中真实编译失败；编译结果、解析／执行有效性与独立 oracle 分层判读，具体情形见[评估故障分诊](evaluation-failure-triage.md)。

## 4. 平台收尾与原件取回

状态 API 提供 jobKind、sourceOs/sourceLang、closureBlocked；source-only 的 target 坐标为空，runnerAssignments.target=null，不推定同机双侧。**不能只因 jobStatus 属终态枚举就停止等待/记 DONE**：closureBlocked=true、jobPhase=CLEANING、提交/调用未知或清理未确认时保持 WAITING，照常写暂停 result.md。

`GET /api/jobs/{jobId}/closure` 返回 JobClosure 1.0（kind=`codeconvert-job-closure`）：complete、cleanupConfirmed、cleanupRecords、issues、artifactDigests、roles、oracleStatus、programOutputProvenance、checkedAt。complete/cleanupConfirmed 要与当前阶段原件及本项清理一致；平台完整性通过仍不能免转换端交付核对，也不是功能 PASS。programOutputProvenance 当前恒为 UNVERIFIED，不把它当已经采到来源证明。

原件通过 `GET /api/jobs/{jobId}/artifacts/{artifactPath}` 单项下载，保持原字节；白名单为：manifest/profile/metadata/request、classification、batch-authorization、staging-manifest、lifecycle、functional_assessment、comparison/result，以及 evidence 下各侧 `.json`、`-request.json`、`-response.json`、`-response.body`、`-identity.json`、`-call.json`。例如：

```powershell
curl.exe --fail -sS "http://127.0.0.1:8443/api/jobs/<job-id>/closure" -o closure.json
curl.exe --fail -sS "http://127.0.0.1:8443/api/jobs/<job-id>/artifacts/evidence/source-response.body" -o source-response.body
```

先核 HTTP 状态和白名单身份再归位，不把错误页面存成合法原件。未发生件 404、非白名单 400，不请求任意路径或目录枚举。API 返回的是原 HTTP body 字节，并不增加程序 stdout 原字节采集保证；bundle 的流表示/截断仍按实际证据判读。

**适用件逐件就绪**：RUNNING／CLEANING 期间 evidence 可先返回 200，而 report 仍 404；一件就绪不推出其余已持久化，单次 404 也不证明 job 不存在或未执行。手工保存实际响应、核 kind/mode 与调用阶段，再按原轮询节奏取本阶段适用件，不盲目请求不存在的 target/comparison。终态后应有件仍缺失时保留原响应并记具体证据／持久化缺口，按交付契约处理；不自动归因代码、不补造文件，不因 READY 解开清理未知。接口不支持与暂未就绪分别记录，不靠无限重试或访问 jobs 补证。

按真实阶段取回适用件：

- 未调用：冻结/授权/staging、失败 JSON/Markdown 报告；不造编译 bundle。
- PREPARING：角色身份和调用记录；请求尚未组装成功不造请求。
- SENDING：请求已发、结果未知，阻断收尾；不盲重发。
- RESPONSE_RECEIVED：实际 HTTP 状态和原 body（真实空 body 允许为空），解析成功才有 response.json；坏响应不冒充合法 bundle。
- TRANSPORT_ERROR：保留已发生请求/错误/清理；只有真实终止清理已确认、适用原件齐备才按真实失败收尾，标签本身不证明可结束。
- 成功取证：request 的冻结命令/输入/源树身份、原 body、解析响应与 canonical bundle 对应；已比较/独立断言/清理的记录一并保留。

artifactDigests 是派生核对摘要，不替代原件；逐件原生取回/核对到转换输出目录，按[交付 §1.1](../../framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)记录适用清单。原 report、comparison 和观察不因归因不同而覆写。

collectorDiagnostics 的 `DOTNET_HOST_LOOKUP_FAILURE_REPORTED` 与 `DRIVER_SYNTAX_ERROR_REPORTED` 分别提示流中出现宿主查找失败或被调用驱动位置的 SyntaxError 特征。按实际回传消费提示，并核精确入口/版本、原 stderr/退出和输出来源；警告不证明根因、未运行范围或已修复，不改变原平台判定。接口未提供或没有警告均不证明这些问题不存在。

最低适用回传面按真实 kind/mode/已发生阶段选择；下表只消费现有接口，不建设取证脚本。实例缺适用路由时保留原记录和缺口，不访问安装目录/jobs 来补件。

| 实际分支/阶段 | 取回并核对的适用面 |
|---|---|
| source-only | 源预检 manifest/profile/metadata、分类/授权与真实接收身份，原 source-preflight 报告、源实际角色调用/请求/body/解析响应/bundle（发生才有）、适用状态/日志/清理/closure。没有 target/comparison 不作缺档 |
| 双侧 build-only | 双侧精确构建请求/原诊断/bundle、3.2 报告及实际清理/closure；核 execution.performed=false、不运行形态。没有行为 comparison/程序输出不补造 |
| 正常双侧行为 | 精确提交/配置、两侧实际请求及返回原件、有效源与目标 build/execution/观察、comparison/result 与实际适用独立断言、日志/清理/closure；各维度须有真实范围，不拿总 report 代两侧流 |
| 启动/传输/HTTP/解析失败 | 按已发生阶段保留 call/request/identity、HTTP 状态/实际 body/错误及可生成的失败报告和清理；没有成功解析就不伪造 response.json/bundle。真实空 body 与错误页/占位分列 |
| 未调用或调用/清理未知 | 保存已发生冻结/接收/失败材料；未知部分继续 WAITING 并查询/取证/终止原 job，不从 closure 摘要推正文存在或从缺 bundle 推定未执行 |

逐件取得状态、原件读取范围与可读副本边界按[交付 §2.3](../../framework/delivery-handoff-contract.md#23-resultmd面向读者的中文报告骨架)记录。report.md 的人读展示不替代 report JSON、实际退出/超时或程序来源；collectorDiagnostics/output.events 为空也不补足缺失流。

## 5. 提交标识、busy 与恢复

当前两种 POST 支持可选 submissionId（非空、最多 128 字符）。首次提交前保存本项尝试标识和精确材料；相同 ID、相同 case/系统/语言/入口类型、capsule 原字节及分类/授权身份，返回原 jobId/当前状态，不重新执行。重新打包 ZIP 字节不同也可能不匹配；复用须原 capsule，不靠同名或内容印象。

相同 ID 配不同冻结材料为 400；存在 request 但缺 state 返回 RECOVERY_REQUIRED，保持未知并移交获批平台核对，不补造新 job。恢复取回原 job 与申请新执行分开；前者仍保留原失败/清理记录。无 ID 的旧未知提交不天然幂等，不从 caseId/capsule hash 猜找 job，也没有通用列举/查询端点。

request-only、请求/状态/manifest 损坏或报告持久化失败时，按实际可查询状态和失败原件判读。原接收材料不可读或状态缺失时保持恢复阻断并移交获批平台处理，不保证所有孤立记录可自动收尾或解除 busy，不借重启或 runner READY 推清理完成。

409 busy 的 detail 对象包含 error=controller_busy、jobCreated=false、retryAfterSeconds=null、action 时，表示本次未建 job，不承诺排队或 ETA；字符串 detail 保留原文按实际解释，不推定具有同一保证。503 不由标签推断已提交/未提交，按回执事实处理。Controller 只支持单进程共享作业存储，不据提交锁宣称多进程或分布式去重。

不能因接口支持幂等而对未知或活动 job 盲重投；只用精确 ID/材料恢复原回执，或按[Controller 恢复规则](remote-controller-adapter.md#提交结果未知时的恢复)取得原接收/终止/清理证据后另记尝试。任务输入、驱动、配置或授权变化须另冻版本、按需重新分类与源预检，不借旧 ID 消除差异。

持久化 busy、孤立／损坏作业需要维护时，另读[Controller 作业恢复适配](controller-job-recovery-adapter.md)，核实际部署、管理者授权、plan／reviewToken 与精确 VM scope。具有适用授权的智能体可执行维护，不必改由管理员亲自操作；尚无对应接口或权限时保留具体缺口，不造路由或令牌。调度释放不改原 closure／功能结果，不自动满足转换端终态门禁。

## 6. 追加归因与比较配置

`POST /api/jobs/{jobId}/annotations` 仅接收 author/reason/note/可选 supersedes；GET 同路径读取追加记录。返回 JobAnnotation 1.0，annotationId、createdAt、originalVerdictUnchanged=true；supersedes 只能指该 job 已有 annotationId。说明不修改原 verdict/比较/证据，也不是平台重评或放行；author 是声明，不是签名。只在已授权向评估平台补充记录时使用，不向其他人/服务发送消息；注释内容不含敏感信息或执行指令。

服务器 preset=`noise-tolerant-v2` 可配置 workspace_path_pairs：最多 16 对精确绝对目录前缀，带尾分隔符、足够具体、无根目录/父穿越/重复路径。映射只处理已声明前缀，剩余相对路径/文件名与计时值继续比较。`text_tokens=[]`、`system_noise_patterns=[]` 明确禁用其他规则；省略时可能继承 v1 默认，冻结时须读实际完整配置。strict/v1 不接受非空目录对。

目录映射是平台服务器配置，不能放进 input_profile 冒充任务字段，不能失败后自动放宽。例外与冻结允许差异及实际配置/实现身份关联。JSON ignoredJsonPaths 在副本上移除精确字段，不增加计时通配、浮点容差或新 oracle。有效 matched 与有效 semantic_pass 均可计冻结范围功能比较通过，分别保留两类和原始/规范化差异，不外推完整业务分子；口径见[评估准备§5.1](../../framework/evaluation-readiness-contract.md#51-有效性消噪与功能分类的次序)及[比较策略适配](comparison-policy-adapter.md)。

ignoredJsonPaths 的 schema 声明、结构比较与输出入口传递分别核实，见[比较适配§2.2](comparison-policy-adapter.md#22-json-字段忽略的声明与消费)。类型化 token 的范围及保护项见该页 §2.3；按实际实现/配置支持选择，不据字段可填写推定消噪成功。source-only/驱动有效性按评估准备判读，专用退出码只是定位线索，不据此改写原 verdict。

### 6.1 2026-10-20 候选协议扩展（部署后条件消费）

本轮平台源码开发新增以下能力，已取得本机模拟回归，**未发布／部署／真实 VM 复验**。它们不覆盖本页前文的现役形状；先核服务实际声明、产品身份与契约集合，缺支持不发送新字段或猜路由。候选集合 hash 为 `sha256:0397516d5317a0d4b6c1fd51df19889bfd79da7d1f73d28689974008ce2a2283`；不是现役数值或隔离证明，后续版本仍以当次完整集合为准。

- Controller health 新增 supportedComparisonManifestVersions、supportedSourcePreflightManifestVersions（均含 1.0/1.1）和 supportedArtifactReadinessVersions（含 1.0）；参与 Agent health 新增 supportedAgentRunRequestVersions（含 1.3）。只有相应声明和实际版本证据齐备才使用新协议。
- 源预检 manifest 1.1 与 comparison manifest 1.1 的角色可显式冻结 buildTimeoutSeconds/runTimeoutSeconds，整数 1–3600；每阶段优先级为该字段→旧角色 timeoutSeconds→InputProfile.timeoutSeconds→20 s。build-only 禁止 runCommand/runTimeoutSeconds，仍不提供 argv/stdin/行为观察或独立 oracle。旧 manifest 1.0 不接受新阶段字段；不自动升级冻结输入。Controller 将适用请求转成 AgentRunRequest 1.3，HTTP 等待覆盖实际请求阶段预算之和及原 60 s 回传宽限；传输超时仍不代表程序超时或未提交。
- GET /api/jobs/{jobId}/artifact-readiness 返回 JobArtifactReadiness 1.0：jobId/caseId、jobStatus/jobPhase、closureBlocked、closureComplete/cleanupConfirmed（null 表示没有有效记录）、checkedAt，及 artifacts 中的 name/path/applicable/status/reason。status 为 available/pending/missing/not-applicable/invalid；available 只表示原件可读并通过适用结构核对。清理中 evidence 可以 available、report/closure 仍 pending；source-only 的 target/comparison 及 build-only 的 comparison 不适用。missing 不直接证明某阶段应当生成该件；仍回读原失败、报告与 closure，库存不是跨文件原子快照或新终态门禁。job 不存在 404，状态不可读 409；维护恢复路径不变。
- 准入错误新增有界字段／文件差集 details 与 serverTimeUtc（本次授权校验所用 UTC），别名只归一化已登记语言；真实方向、case、源摘要与数量仍核对。原 manifest／分类名称不改写，文件内容多重集兼容不免本地完整路径冻结。未来／过期授权不放宽，校验时间不供伪造授权使用。
- Agent 通过原可扩展 collectorDiagnostics 提供 PHASE_TIMEOUT_BUDGETS、BUILD_TIMEOUT、COMMAND_INVOCATION 和 COMMAND_LAUNCH_FAILED；argv 摘要只定位调用边界，inputConsumption=UNVERIFIED 不证明已消费预期文件。缺少程序原字节／驱动来源证据时仍保留 UNVERIFIED；不以诊断存在认定语法或功能通过。

可选工具版本库存及 v3 路径策略分别见[能力矩阵](runner-capability-matrix.md#11-工具链与依赖)和[比较适配](comparison-policy-adapter.md#候选-v3-临时路径保护)。旧报告、闭环状态和已知转换缺陷不因候选升级改判。

### 6.2 2026-10-20 续轮开发收口（仍须核实际部署）

§6.1 的 039751… 是首批候选快照。续轮继续修订尚未发布的 AgentRunRequest 1.3、SourcePreflightManifest/comparison manifest 1.1，最新集合为 `sha256:53a6cb1bb7be5377fb3fdcc19754ec7a48badb58e1d143c16885cafc0693fad7`；旧已发布 schema 原字节不改。最终平台维护回归 857 项、分类器维护 79 项通过，**不代表已部署、真实 VM 验收或 D4 新结果**。已有未决 job／清理未知状态仍按原恢复流程处理。

Controller health 新增 supportedRawStreamCaptureVersions、supportedBuildValidations、supportedOracleConsumptionVersions、acceptedClassifierSha256；Agent 同时宣告 supportedPowerShellParserInterpreters。现场实际缺相应声明／实现身份时不使用这些扩展。

角色可显式冻结 captureRawOutput=true（默认 false）。原始字节由 VM Agent 经原响应信封回传，Controller 在恢复 VM 前校验并留存；RAW_STREAM_CAPTURE 1.0 关联 phase/channel、固定 artifactRef、Base64、保留字节 digest/size、全流 digest/size、EOF 与截断状态。每流原字节上限 4 MiB，采集上限更小时依原限；完整流才给 rawArtifactRef，前缀使用 .prefix.bin 并保留完整引用为 null。下载沿既有 artifacts 接口，只使用真实回传的固定引用；readiness 与 closure 校验同一字节，空 stdout/stderr 的零字节原件合法。转换端可保留 JSON 原响应与平台引用，不在本机执行／重建程序或取证脚本，不借原字节接口访问安装目录/jobs；原件留存不等于业务输出来源已认证。

角色可改用 buildValidation={kind:powershell-parser,schemaVersion:1.0,files:[精确相对路径],interpreter:pwsh或powershell}，与 buildCommand 互斥；省略 interpreter 只用 pwsh，不自动退回旧 PowerShell。files 为 1–128 个源树文件，覆盖全部已暂存 .ps1/.psm1/.psd1，可显式列入声明为 PowerShell 的 .txt/.text；不得越界、重复或只引用 fixture。单文件 2 MiB、总 16 MiB 是该后端范围，不改转换规模规则。平台用固定产品解析器解析而不执行提交脚本；这是发布后获批平台提供的语法能力，不授权转换 Agent 生成临时驱动。build-only 的业务 argv/stdin、运行及 oracle 禁令不变，解析器自身控制输入不属业务输入。

PLATFORM_PARSER_WITNESS 记录限定解释器、产品程序摘要、精确文件 SHA、错误总数及每文件最多 32 个错误位置；Controller 在比较前与收尾再次核文件／原始构建流。退出 0 缺见证不算语法 PASS，BUILD_VALIDATION_INVALID 保留实际退出并记 inconclusive，先归平台验证问题，不据此修目标代码。此见证只证明限定文件的语法解析，不证明模块加载、运行或业务输入消费；普通 buildCommand 没有见证时仍按真实条件核观察，不以 argv 摘要认证消费。

识别到的旧式 PowerShell -Command/-EncodedCommand 或 Parser.ParseFile/ParseInput 构建调用会附 LEGACY_POWERSHELL_PARSER_UNVERIFIED，保留 raw completed/0，但独立语法/code 结论 inconclusive；Controller 接收／比较前／closure 同样核限定。缺真实文件消费依据时不能借旧路径 0 退出绕过源预检，改用已证实支持的固定平台后端或补适用真实材料，不新增临时驱动、不把它归为源／目标代码缺陷。

GET /api/jobs/{jobId}/oracle-consumption 返回 OracleConsumption 1.0：inputProfileHash/functionalProfileHash、consumptionStatus=NOT_REQUESTED/NOT_EVALUATED/ASSESSED/UNVERIFIED、原 assessmentStatus、assessmentRef、义务／关键义务／断言计数及声明维度；inputCoverage/branchCoverage 固定 UNVERIFIED。它核已有原件的精确关联，不重算或改判历史结果。JSON Pointer 的 /errors/0/field 与忽略 JSON 字段的点路径分开，非零退出可作为已冻结独立期望，不默认失败。

工具及离线库存见[能力矩阵](runner-capability-matrix.md#11-工具链与依赖)。分类器最终 2.6 精确 SHA 为 9a74610cbd293dea2280002a43edf71f28be3fc4e64ea866dcd2224b1c34d28d，维护登记见[准入页](../../workflow/classifier-agent-gate.md)；未部署中间稿 42a935… 不再受信。受信列表要以实际 Controller 为准，未升级不假定接受。进程 OS 可观察指纹／offered stdin 摘要也不证明程序确实读取输入或管道中每段输出的写入者，global programOutputProvenance 保持 UNVERIFIED。

### 6.3 2026-10-21 审查修订（候选，未部署）

原件指纹与维护审阅令牌分开；新 reviewToken 绑定 job／原件及精确当前恢复 scope，GET→POST、排队后及恢复前后均核对配置变化。POST 仍为原四字段。新成功回执使用记录中的已审阅 scope 验证，旧成功回执仍按原格式核原件，不因未来配置变化重新恢复历史 VM；不从旧 runnerId 推定历史物理身份。完整操作条件见[恢复适配](controller-job-recovery-adapter.md)。

进程指纹改为有数量／尽力时间限制的后台观察，不等待它才启动输出采集／阶段超时；未及时完成或失败时留 UNVERIFIED，不延长程序预算。v3 默认关闭临时路径和端口 token，仅保留 timestamps；动态端口须明确冻结／显式配置，范围数值本身不证明动态性。v1/v2 旧默认及历史原判保留，详见[比较适配](comparison-policy-adapter.md#候选-v3-临时路径保护)。本修订不改 schema 集合、分类器 SHA 或样本业务字节；仍须以实际部署实现／配置为准。

## 7. 适用边界

本页定义请求与判读契约，不替代实际 API、schema、实现身份、任务授权及逐例隔离核对。实例与本页所需协议不符时记录具体准备缺口，暂停受影响提交或判读；已发生 job 的原报告、观察及身份不回写。不以支持声明、示例受理或平台自检代替精确版本的源/目标构建和适用行为证据。
