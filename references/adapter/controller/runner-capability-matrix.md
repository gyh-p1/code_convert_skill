# Runner 能力矩阵（2026-10-05 Ruby 适配实测）

> 文档类型：外部评估基础设施事实（reference）
> 状态：ACTIVE（以 Controller 实时接口为准的唯一 runner 能力口径）
> 取值方式：2026-10-05 读取 Controller `GET /api/runners` 与 Agent `/health`，并以无副作用 Ruby 双侧 job 核对 build、运行及清理；提交时仍以实时接口为准
> 服务与契约身份：`service=remote-host-controller`、`version=1.0.0`、`ready=true`、
> `contractSetHash=sha256:e088a356b48fd1c3f50e480ac24c2fd03319dc60a49b41de4d076219819c4c45`、`runnerMode=agent`

## 1. 现役 runner

| runnerId | os / arch | 支持语言（`supportedLanguages`） | 快照回滚 | 基线快照 | 实测状态 |
|---|---|---|---|---|---|
| `linux-vm-agent-x64` | linux / x64 | python、powershell、c、cpp、go、dotnet、ruby | `true` | `CC-Eval-Linux-8Lang-R11` | READY、`contaminated=false` |
| `windows-vm-agent-x64` | windows / x64 | python、powershell、c、cpp、go、dotnet、ruby | `true` | `CC-Eval-Windows-8Lang-R11` | READY、`contaminated=false` |
| `macos-vm-agent-x64` | macos / x64 | python、powershell、c、cpp、go、dotnet、ruby | `true` | `CC-Eval-Mac-7Lang-R2` | READY、`contaminated=false` |

三个 runner 的 `selectionPriority` 均为 100，`lastFailureType`/`lastFailureReason` 均为 `null`。

## 1.1 Ruby 适配证据（2026-10-05）

- **适配前探测**：Controller 与 Windows/Linux Agent 的语言列表均缺 `ruby`，但隔离探针 job `eval-20261005-053322-b85dce16` 在 Linux 与 Windows 分别找到 Ruby 3.3.8、Ruby 4.0.3；两侧 `ruby -c` 均返回 `Syntax OK`、退出码 0。版本是运行环境事实，不作测试用例来源校验。
- **配置与基线**：Windows、Linux Agent 的 `capabilities.languages` 均已添加 `ruby`，Controller 两个 runner 的 `supported_languages` 同步更新；新建 `CC-Eval-Windows-8Lang-R11` 与 `CC-Eval-Linux-8Lang-R11` 快照并设为当前基线。原 R10 快照仍可用于回退。macOS 继续使用 `CC-Eval-Mac-7Lang-R2`。
- **快照恢复后的整链路验证**：无副作用 job `eval-20261005-055954-f055ab5b` 将 Linux Ruby 作为 source、Windows Ruby 作为 target。两侧 `ruby -c run_case.rb` 均 build `completed`、退出码 0、输出 `Syntax OK`；两侧运行退出码 0、输出相同的固定 JSON；Controller 报 `COMPLETED`、代码结论 `passed`、两侧清理 `PASSED`。该证据只证明本例的 Ruby 工具链、runner 分配、快照恢复与回传可用，不代表任一攻防转换案例通过。
- **当前部署**：Controller `GET /api/runners` 与两台 Agent `/health` 均登记 `ruby`；复核时三台 runner 为 READY、`contaminated=false`。任何新 job 仍须读取实时状态，并核对其特定依赖与入口。

## 2. 对冻结契约与提交的影响

- 七种目标语言已在 Windows、Linux、macOS 三台 runner 登记；Ruby 在 Windows/Linux 的最小语法与运行路径已有上述实测证据。冻结契约中按三台支持 Ruby 选型的决定现有部署依据。
- 三台 runner 均支持快照回滚。Ruby framework 模块、第三方 gem、系统 API 与具体转换产物仍须按逐例契约检查；本页的小样例不能替代这些证据。
- `same-runner` / `dual-runner` 仍由源侧与目标侧实际选定的 runnerId 决定，不由语言工具链数量决定。

## 3. 已被本页取代的旧描述（不得再引用）

- 本仓库旧版 `remote-controller-adapter.md`（2026-09-28）只列两个 agent、快照 `CC-Eval-*-8Lang-R7`、控制器 `192.168.101.250`（该地址仍正确）与 VC 名称 `windows-eval`/`linux-eval`；runner 能力与快照身份已过时。
- 旧仓库工作副本 `apps/remote-controller/remote_host_controller/configs/vm_profiles.yaml` 写的 `linux.enabled=false`、`macos.enabled=false`、`linux` 仅四语言、macOS `supports_snapshot_rollback:false`、快照 `CC-WinEval-RC2`，均与现役部署不符；该文件是平台侧开发工作副本，不是本项目的能力真源。
- 任何"Linux 不支持 PowerShell/.NET"、"macOS 不支持快照回滚"、"Ruby 无 runner"的表述都已作废。

## 4. 连接与提交坐标（沿用适配文档）

| 角色 | 地址 |
|---|---|
| Controller HTTP API | `http://192.168.101.250:8443` |
| 本机提交端 | `192.168.101.101`（与 Controller 同 `192.168.101.0/24` 段，实测 HTTP 200 直达） |
| 各 VM Agent | 由 Controller 按 runnerId 编排，提交方不直连 Agent |

健康检查：`GET /api/health`（实测 200，`ready=true`）。只有 runner `ready=true` 且 `contaminated=false` 才接受新任务；当前三者均满足。

## 5. 安全边界

- 本页只记录连接与能力坐标，**不包含任何凭据**；API 密钥、SSH 私钥、VMware 口令一律不入库。
- 本机不编译、不运行源/目标/构建脚本；一切编译与运行由 Controller + VM Agent 执行并回传证据。
- 本页是**能力事实**，不是转换效果、编译通过或功能等价的证据。
