# Runner 能力矩阵与运行条件

> 文档类型：外部评估基础设施能力与身份核对（reference）
> 状态：ACTIVE。每次提交以 Controller 实时接口、参与角色实现身份和本项回传为准。

平台提供独立 source-only、build-only、closure/原件导出、submissionId 与实现身份接口；请求和取证形状见[当前协议适配](platform-revision-adapter.md)。本页定义 runner 选型及运行条件，能力登记不代替本项构建、行为或隔离证据。

本页离线正文在连接准备时读取；实时 runner、快照和工具链证据用于可达时的适用源预检/评估。按[评估准备 §1.0](../../framework/evaluation-readiness-contract.md#10-转换前可达性检查与仅转换分支)确认不可达后，仅转换分支记录候选平台及未核验范围，不要求取得实时接口返回才生成、自审和交付。

## 1. Runner 与语言登记

| runnerId | os / arch | 支持语言（`supportedLanguages`） | 快照回滚 |
|---|---|---|---|
| `linux-vm-agent-x64` | linux / x64 | python、powershell、c、cpp、go、dotnet、ruby | 支持；本项核实际声明与恢复记录 |
| `windows-vm-agent-x64` | windows / x64 | python、powershell、c、cpp、go、dotnet、ruby | 支持；本项核实际声明与恢复记录 |
| `macos-vm-agent-x64` | macos / x64 | python、powershell、c、cpp、go、dotnet、ruby | 支持；本项核实际声明与恢复记录 |

C# 的平台语言标识使用 `dotnet`。提交前保存 `GET /api/runners`，逐项核 `supportedLanguages`、`lifecycleState`、`baselineSnapshot`、`contaminated`、失败原因及本项分配。只有 runner 就绪且未污染，并满足其余门槛时才提交；不把本表当作实时 READY/clean 证明。

基线快照名称、工具链版本、选择优先级与失败状态取自实际接口和参与角色资料，写入本项冻结及提交记录。源码画像给出候选 OS，源可构建性由对应候选环境的编译器诊断定案；不能仅因某一 OS 不支持就排除其余合法候选。

### 1.1 工具链与依赖

- 七语言登记不保证每个第三方模块、gem、程序集、系统 API、头文件或链接库就绪；逐项冻结实际版本、入口、依赖及命令。
- Ruby 的语法检查与运行分别取独立证据；framework 文件或库没有合法入口时按仅编译分支处理，不制造入口。
- Go 的 HOME、XDG_CACHE_HOME、GOCACHE 及构建目录须在隔离环境可写。缓存初始化、权限或工具链启动错误先按原诊断归因，不记作源代码或转换缺陷；提交方不在本机运行构建来替代证据。
- .NET 的 SDK、运行时、目标框架及程序集加载条件分别核对；工具链已登记不保证宿主查找或外部依赖满足。

### 1.2 观察与比较能力

平台观察范围为 `output`、`filesystem`、`processes`，逐项核实际采集与比较覆盖。`network`、`registry` 及事件级 oracle 不由语言登记或支持列表推定可用；缺对应支持时记录具体能力缺口，不能伪造字段或以 stdout 替代缺失维度。

stdout/stderr 模式、文件保护、服务器 token/目录映射与 minor 容忍按[比较策略适配](comparison-policy-adapter.md)冻结。服务器配置不属于任务输入字段，也不提供网络隔离、程序输出来源或驱动合法性证明。

### 1.3 实现与契约身份

保存 Controller 与参与 Agent 的 `contractSetHash`、`implementationIdentity`、发布身份及实际配置；与本项 schema、授权 contractHash 对应。`implementationIdentity.available=true`、`restartRequired=false` 及组件身份必须有实际资料支持。缺失、冲突或待重启时停止受影响的新执行。

组件 `version` 与 `releaseVersion` 分别记录；同一版本标签或契约 hash 不证明实现、依赖、工具链、快照及隔离相同。源文件与目标文件身份仍按本项精确哈希关联，不能用平台契约 hash 替代。

## 2. 对冻结契约与提交的要求

- 根据本项 source/target 的 OS、架构、语言与依赖选择 runner；`same-runner` / `dual-runner` 由实际 runnerId 决定。
- build-only 须 Controller 和参与 Agent 均声明支持，并核真实构建命令、未运行形态与清理；普通运行 job 不充作仅编译验证。
- 行为评估另核获批驱动的启动、到达状态、采集、终止四要素，以及两侧输入、初始状态、fixture 和恢复条件对称。
- 每次提交复核授权、精确输入、当前身份、配置及逐例隔离；状态或配置改变时按[任务状态契约](../../framework/task-state-contract.md)核复用/失效，不能继承不再适用的通过结论。

## 3. 生命周期与恢复

READY、clean 与快照恢复分别记录其实际依据，均不代表网络已隔离或已有 job 已清理。活动调用、提交结果未知、closureBlocked 或清理未确认时保持 WAITING，不借重启、快照名称或 runner 就绪解除未知状态。

恢复原回执、终止及取证按[Controller 适配](remote-controller-adapter.md#提交结果未知时的恢复)和[当前协议适配](platform-revision-adapter.md)进行。提交方不读取或修改 Controller 安装目录及 jobs；共享配置、部署和回退由获批平台处理，配置变化后重新核身份并建立对应条件记录。

## 4. 连接与提交坐标

| 角色 | 地址 |
|---|---|
| Controller HTTP API | `http://127.0.0.1:8443`（Controller 本机回环）；跨机位为 `http://192.168.101.250:8443` |
| 提交端 | 与 Controller 同机，经回环提交；宿主可连公网，样本执行只在 VM Agent |
| 各 VM Agent | 由 Controller 按 runnerId 编排，提交方不直连 Agent |

提交前读取 `GET /api/health` 与 `GET /api/runners`，保存完整原响应。连接可达不构成执行批准；源/目标程序及构建脚本均不在提交宿主执行。

## 5. 安全边界

- API 密钥、SSH 私钥、VMware 口令不写入仓库、capsule、日志、报告或聊天。
- 样本只在获批且已核网络/数据边界的隔离 VM 内构建或运行；不触及公网、生产网、真实外部目标、真实凭证或生产数据。
- 本页不产生执行授权，不替代[安全边界](../../framework/safety-boundary.md)；能力登记不构成本项编译通过、功能等价或转换效果证据。
