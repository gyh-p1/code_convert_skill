> 2026-10-09 19:59（北京时间）部署更新：四角色统一 1.0.26，原包 health-only 验收通过。Controller ready=true，三 Runner READY/clean、blockedRunnerCount=0，契约一致。最终快照已生效，macOS 冷启动自动登录通过，见[部署与快照记录](../../../docs/stages/stage1/reports/1.0.26部署与快照更新记录-2026-10-09.md)。样本执行与网络隔离未在本次验收，提交仍须逐例核对。

# Runner 能力矩阵与 Controller 部署事实（2026-10-09 复核）

> 文档类型：外部评估基础设施事实（reference）
> 状态：ACTIVE（以 Controller 实时接口为准的唯一 runner 能力口径）
> 取值方式：2026-10-09 19:59 原包四角色健康验收、Controller `GET /api/health`、`GET /api/runners` 与部署回执；旧 Ruby/Go/消噪 job 证据保留原适用范围，提交时仍以实时接口为准
> 服务与契约身份：`service=remote-host-controller`、`version=1.0.0`、`ready=true`、
> `contractSetHash=sha256:e088a356b48fd1c3f50e480ac24c2fd03319dc60a49b41de4d076219819c4c45`、`runnerMode=agent`
>
> **历史契约冲突**：当日部署前 Controller 曾报告 `56b32706…`、Agent 为 `e088a356…`，导致 CONTRACT_MISMATCH。
> 1.0.26 统一部署后四角色均为上方契约集合，冲突已消除。旧逐版本证据保留于[根因定论](../../../docs/stages/stage1/reports/contract-mismatch-root-cause-2026-10-09.md)，不作为当前状态。

## 1. 现役 runner

| runnerId | os / arch | 支持语言（`supportedLanguages`） | 快照回滚 | 基线快照 | 实测状态 |
|---|---|---|---|---|---|
| `linux-vm-agent-x64` | linux / x64 | python、powershell、c、cpp、go、dotnet、ruby | `true` | `CC-Eval-Linux-8Lang-1.0.26` | READY、`contaminated=false` |
| `windows-vm-agent-x64` | windows / x64 | python、powershell、c、cpp、go、dotnet、ruby | `true` | `CC-Eval-Windows-8Lang-1.0.26` | READY、`contaminated=false` |
| `macos-vm-agent-x64` | macos / x64 | python、powershell、c、cpp、go、dotnet、ruby | `true` | `CC-Eval-Mac-7Lang-1.0.26-AutoLogin` | READY、`contaminated=false` |

三个 runner 的 `selectionPriority` 均为 100，`lastFailureType`/`lastFailureReason` 均为 `null`。

## 1.1 Ruby 适配证据（2026-10-05）

- **适配前探测**：Controller 与 Windows/Linux Agent 的语言列表均缺 `ruby`，但隔离探针 job `eval-20261005-053322-b85dce16` 在 Linux 与 Windows 分别找到 Ruby 3.3.8、Ruby 4.0.3；两侧 `ruby -c` 均返回 `Syntax OK`、退出码 0。版本是运行环境事实，不作测试用例来源校验。
- **配置与基线（Ruby 适配当时）**：Windows、Linux Agent 的 `capabilities.languages` 均已添加 `ruby`，Controller 两个 runner 的 `supported_languages` 同步更新；当时新建 `CC-Eval-Windows-8Lang-R11` 与 `CC-Eval-Linux-8Lang-R11` 快照。Linux 后按 §1.2 曾升为 R12；macOS 当时使用 R2。这些是历史基线，现役见 §1。
- **快照恢复后的整链路验证**：无副作用 job `eval-20261005-055954-f055ab5b` 将 Linux Ruby 作为 source、Windows Ruby 作为 target。两侧 `ruby -c run_case.rb` 均 build `completed`、退出码 0、输出 `Syntax OK`；两侧运行退出码 0、输出相同的固定 JSON；Controller 报 `COMPLETED`、代码结论 `passed`、两侧清理 `PASSED`。该证据只证明本例的 Ruby 工具链、runner 分配、快照恢复与回传可用，不代表任一攻防转换案例通过。
- **当前部署**：Controller `GET /api/runners` 与两台 Agent `/health` 均登记 `ruby`；复核时三台 runner 为 READY、`contaminated=false`。任何新 job 仍须读取实时状态，并核对其特定依赖与入口。

## 1.2 batch-01 发现的 Linux Go 缓存路径缺陷

- B20 首提 job `eval-20261005-075546-2bffe862` 的源侧 `go build` 在源码编译前失败：`failed to initialize build cache at /home/d9lab/.cache/go-build: mkdir /home/d9lab: permission denied`。Controller 报 `CODE_RESULT`，但按 stderr 归因是 runner 的 HOME/默认构建缓存不可写，不能计作源代码或转换失败；目标侧未得到 build 证据。
- 同一案例补 `GOCACHE=/tmp/gocache` 后，重提 job `eval-20261005-075714-01c8bdb5` 的源、目标 build 均 `completed` 且退出码 0。绕行只证明这个 job 在该缓存位置可用，**不证明 runner 默认 HOME/缓存权限已修好**。
- **2026-10-05 单机热修已取证**：旧仓库 `codex/linux-go-cache-home` 提交 `8d4da68` 将 Linux Agent 的 `HOME`、`XDG_CACHE_HOME`、`GOCACHE` 指向 `/var/lib/codeconvert-agent` 下的可写目录。当前 VM 的 unit SHA-256 为 `8d87a7d016bf979a8d829ef62dd0c6e9cbb8f72a4de8c4dc75deca4c0f5ade84`；新快照 `CC-Eval-Linux-8Lang-R12` 已设置为 Controller 的 Linux 基线，R11 保留。无害 Go 作业 `eval-20261005-115047-f2cdbaec` 使用直接的 `go build -o program hello.go`（没有 `GOCACHE` 前缀），源/目标 build 与运行均 `completed/0`，comparison `matched`、环境 `clean`、两侧清理 `PASSED`。作业结束后核对 Linux unit 仍为新哈希，三台 runner 均 `READY/clean`；Controller 契约哈希保持 `sha256:e088a356b48fd1c3f50e480ac24c2fd03319dc60a49b41de4d076219819c4c45`。该证据只证明无害 fixture 与当前环境，不回填 B20 原始作业或其它转换样本。

## 1.3 Controller 消噪部署（2026-10-09，**历史**）

> **当前状态提示**：本节记录当日 `1.0.25-noise.1` 消噪试用部署。该版本已被 **1.0.26 统一部署取代**，当前 releaseVersion 与 manifestHash 见[部署与快照记录](../../../docs/stages/stage1/reports/1.0.26部署与快照更新记录-2026-10-09.md)。**消噪能力本身沿用**（`preset=noise-tolerant-v1` 等在 1.0.26 健康验收中一致），但本节的身份与回退材料均为历史值，不得作为现役基线引用。

2026-10-09 用户授权保留文本消噪、文件消噪与次要差异容忍并部署试用成品。平台使用新不可变发布包，只升级 Controller 比较实现与配置；Agent、三 VM 基线、执行路线及 Schema 集合没有随本次变更改动。

| 身份/能力 | 已核对事实（**历史值，现役见 1.0.26 记录**） |
|---|---|
| Controller releaseVersion | `1.0.25-noise.1`（读取服务器安装回执；不从 health.version 推断）。**已由 1.0.26 取代** |
| 发布 manifestHash | `sha256:026a8da844cc43ade9b925d9b34d1167e877b02033a1e784f522bb4aac25fbe9`（1.0.25-noise.1 值） |
| 原始 ZIP SHA-256 | `d32227b6e0e9a8575de407c39c9c74363ce87f0e98678948e4648d142dbfe502`（同上） |
| API/契约 | 组件 `1.0.0`，InputProfile 1.0 / ComparisonResult 1.0 / EvaluationReport 3.0 的既有入口保持可用；contractSetHash 与该次部署一致，现役值见本页顶部 |
| 比较配置（能力沿用至 1.0.26） | health.comparison.preset=`noise-tolerant-v1`；text_tokens=`temporary-paths,timestamps,ephemeral-ports`；tolerate_minor=`true`；五种文件噪声模式见[比较策略适配](comparison-policy-adapter.md#1-区分服务器配置与任务输入)。该配置在 1.0.26 健康验收中复核一致 |
| 历史试用复核 | 该次 HTTP 200、ready=true；三 Runner READY/clean，基线为 R12/R11/R2；当前统一部署的基线见 §1 |
| 观察范围 | 沿用现有 output/filesystem/processes；本次不新增 network/registry Collector，也不提供网络隔离 Attestation/Permit |

部署时四个固定无害 Windows→Linux 双侧对照均完成并符合预期：

| 验证内容 | Job ID | 实际 behaviorVerdict / codeVerdict |
|---|---|---|
| 允许的临时路径、时间戳、动态端口及 .DS_Store 噪声 | `eval-20261009-031236-75c4d3a4` | semantic_pass / semantic_pass；output/filesystem 均留下 minor diff |
| 固定端口 8080→9090 | `eval-20261009-031400-5e00bf76` | mismatched / failed |
| 目标遗漏业务文件 required.txt | `eval-20261009-031457-2e193c03` | mismatched / failed |
| 显式 include .DS_Store，目标遗漏该文件 | `eval-20261009-031613-c515a05d` | mismatched / failed |

四例源/目标 execution.performed=true、cleanup=PASSED、environmentStatus=clean；负向例的 failed 是预置差异被检出。第一例的实际 comparison 在本轮再次经 API 读取。它们只证明这组无害对照的策略、执行与清理接入，**不证明新版本编译质量、普通转换功能率、macOS 消噪效果、网络隔离升级或正式批量能力**。本轮适配只读复核已有证据，没有新提交作业。

平台发布、测试及回退材料位于服务器 `D:\CodeConvertRemote\DeployInput\noise-trial-20261009`；保留原 `1.0.24` 启动/配置/回执于 `rollback-1.0.24`，恢复入口为该材料根的 `rollback-controller.ps1`。回退脚本仅做过语法解析，未实际演练。调整共享配置或回退由平台在无活动 job 的窗口处理，提交 Agent 不在普通评估中执行部署/回退；恢复后重新核对实时能力，原任务证据不改写。

## 2. 对冻结契约与提交的影响

- 七种目标语言已在 Windows、Linux、macOS 三台 runner 登记；Ruby 在 Windows/Linux 的最小语法与运行路径已有上述实测证据。冻结契约中按三台支持 Ruby 选型的决定现有部署依据。
- 三台 runner 均支持快照回滚。Ruby framework 模块、第三方 gem、系统 API 与具体转换产物仍须按逐例契约检查；本页的小样例不能替代这些证据。
- `same-runner` / `dual-runner` 仍由源侧与目标侧实际选定的 runnerId 决定，不由语言工具链数量决定。
- 本版服务器比较配置与任务输入字段分别冻结，策略选择、文件保护、原始差异与 semantic_pass 的解读按[比较策略适配](comparison-policy-adapter.md)。健康/快照与消噪都不能代替逐例安全隔离核对。

## 3. 已被本页取代的旧描述（不得再引用）

- 本仓库旧版 `remote-controller-adapter.md`（2026-09-28）只列两个 agent、快照 `CC-Eval-*-8Lang-R7`、控制器 `192.168.101.250`（该地址跨机位仍可达；现役提交端与 Controller 同机、走回环 `http://127.0.0.1:8443`，见 §4）与 VC 名称 `windows-eval`/`linux-eval`；runner 能力与快照身份已过时。
- 旧仓库工作副本 `apps/remote-controller/remote_host_controller/configs/vm_profiles.yaml` 写的 `linux.enabled=false`、`macos.enabled=false`、`linux` 仅四语言、macOS `supports_snapshot_rollback:false`、快照 `CC-WinEval-RC2`，均与现役部署不符；该文件是平台侧开发工作副本，不是本项目的能力真源。
- 任何"Linux 不支持 PowerShell/.NET"、"macOS 不支持快照回滚"、"Ruby 无 runner"的表述都已作废。

## 4. 连接与提交坐标（沿用适配文档）

| 角色 | 地址 |
|---|---|
| Controller HTTP API | `http://127.0.0.1:8443`（Controller 本机回环；跨机位仍可 `http://192.168.101.250:8443`） |
| 提交端 | 与 Controller 同机（转换 Agent 工作区），经回环提交；同机不代表隔离（宿主可连公网），样本执行仍只在 VM Agent |
| 各 VM Agent | 由 Controller 按 runnerId 编排，提交方不直连 Agent |

健康检查：`GET /api/health`（实测 200，`ready=true`）。只有 runner `ready=true` 且 `contaminated=false` 才接受新任务；当前三者均满足。

## 5. 安全边界

- 本页只记录连接与能力坐标，**不包含任何凭据**；API 密钥、SSH 私钥、VMware 口令一律不入库。
- 本机不编译、不运行源/目标/构建脚本；一切编译与运行由 Controller + VM Agent 执行并回传证据。
- 本页是**能力事实**，不是转换效果、编译通过或功能等价的证据。
