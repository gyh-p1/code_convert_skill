# Spec 02｜Controller 与 VM Agent 开发改进

> 更新：2026-10-09；状态：可开发规格，以下改动尚未实现/部署
> 候选根：E:\桌面文档\Code_Convert\.worktrees\evaluation-noise-v1
> commit：db2ccc0379e9d9281c1578b91745b1e3b1ca9452；当前线上契约与候选源码不同。

## 1. 共同约束

以下路径相对候选根。先冻结实际开发 commit 与部署回执，不能把候选源码的函数行为当作当前线上行为。不得跳过契约检查、自动解封 QUARANTINED 或以 READY 代替隔离。新增字段是拟议设计，消费者仅在实际部署支持后使用。

工程实现放在评估仓库；不要在转换 Skill 仓库创建 Controller 或框架。本轮只完成源码评估和开发规格，没有实施以下平台改动。

## 2. T02-a：发布/契约一致性核对（P0，运维门槛）

回收 Controller 与各 Agent 的不可变发布版本、安装回执、contractSetHash、文件身份、基线快照及检查时间；比较启动配置所引用的契约目录，而非只看源码目录。先确认是否有活动 job 和正在进行的升级，不能覆盖他人的发布进程。

输出一张角色→发布→契约→快照→实时状态表。若当前 Controller 被错误升级，评估回退到已验收发布；若新契约是目标版本，则按同一发布升级适用 Agent 和快照。路线必须由实际升级状态决定，不硬编码选择旧包。

恢复门槛：契约相符、能力匹配、清理成功、所需 runner READY/clean、快照恢复后仍匹配。恢复不自动证明网络隔离，后续仍逐例核查。

## 3. T02-b：健康与调度就绪分离（P0，可立即开发）

入口：apps/remote-controller/remote_host_controller/app/main.py 的 health()；services/runner_registry.py 的状态快照；api/runners.py。

当前 ready 主要表示 JobService/契约 manifest 初始化成功，可能在三 runner 全隔离时仍为 true。保留该字段语义和 HTTP 存活响应，新增诊断摘要（拟议）：executionReady、readyRunnerCount、blockedRunnerCount、checkedAt、blockingReasons。executionReady 只说明至少存在可用 runner，不代替每项源/目标语言/OS解析和隔离检查。

实现约束：请求读取 registry 快照，不在 health 中轮询 VM、回滚快照或获取执行锁；BUSY 与 QUARANTINED 分开；更新时间可见。字段若严格 schema 消费需同步契约和适配，不能只改服务端。

验收：全隔离时 ready 可仍true但 executionReady=false；一台 ready 时仅摘要变true，任务不匹配仍拒绝；BUSY 不显示成永久损坏；并发状态更新读取一致；旧客户端继续读取现有字段。使用受控 registry fixture，不能为健康接口启动样本。

## 4. T02-c：契约不匹配的可定位诊断（P0，可立即开发）

入口：services/agent_client.py 的 validate_agent_identity、services/vm_lifecycle.py 的隔离分支、runner_registry.py 和 api/runners.py；同步相应既有测试。

拟议诊断至少给 runnerId、expectedContractSetHash、actualContractSetHash（缺失为 null）、checkedAt、checkPhase、reasonCode；发布版本只有 Agent/回执确有提供时才填，不能从业务 version=1.0.0 推断。沿用 CONTRACT_MISMATCH 的拒绝/隔离逻辑。

不把 Agent URL、完整原始配置、token 或响应体写进公开错误。恢复后重新核对实际值；禁止管理员强置 READY 绕过检查。当前返回类型若不容纳新诊断，先按既有结构提供明确 message 或在明确版本的附加诊断字段实现，不能向严格 schema 塞未知键。

验收：匹配、不同、缺失、格式非法、Agent 不可达分别返回正确原因；不匹配仍零执行；故障可关联实际角色；日志无凭据。故障与后续恢复证据分别保存。

## 5. T02-d：观察能力与真实义务预检（P0）

入口：Agent app/observations.py（output/filesystem/processes；network/registry 当前 out-of-scope）、app/capabilities.py；Controller services/runner_resolver.py、comparison_manifest.py 及相关能力契约。

增加可解释的“需要哪些观察、哪些支持、哪些缺失”检查。先核对现有 InputProfile/FunctionalProfile 能表达的 required obligation，不新造与它们平行的总 schema。若缺少必需/可选区分，先提交契约变更并携带 Controller/Agent 一起升级，禁止只改一侧。

规则：必需维度不支持时在执行前报告能力不足；仅用于诊断的可选维度不支持时允许其他观察，但明确不确定及覆盖缺口；不得静默移除 policy 维度或伪造事件。网络/注册表功能不能因为有 stdout 就宣称匹配。

验收：output-only 正常；必需 network/registry 不被标为 matched；可选缺失仍有明确 limitation；三系统能力不同能分流；源/目标任一侧缺维度保留缺口。现有 comparator 已对未观察维度给 inconclusive，须保留此保护，不重复开发。

## 6. T02-e：源失败后的目标侧诊断（P1，有条件进入）

入口：services/dual_run_orchestrator.py 的 source_exec_status 早返回分支；evaluation-core 的 report_builder.py、证据/报告契约及现有编排测试。

当前流程是源→清理→目标，源侧 blocked/launch-failed/timed-out 会提前回报，不能称“双侧独立执行”。拟议新增显式的诊断执行模式，默认保持原行为；模式承载字段必须走现有契约扩展/兼容评审，不假定当前 capsule 支持新字段。

仅当源失败可归因于已执行的代码构建/启动问题、源侧清理成功、目标自身已获得准入且输入不依赖失败源的产物时，继续目标诊断。契约/隔离/资源/证据身份失败、源超时原因未知、清理失败均停止；不能把“不知道源为何失败”当作继续条件。

输出保留两侧各自 build/execution 与失败；缺源有效基线时 behaviorVerdict=inconclusive，目标编译成功可以单独报告，但不能算等价。源失败、目标成功也不能把整个转换任务改成 passed。

最低回归：源编译失败/目标成功；源代码启动失败/目标失败；源超时；源清理失败；目标不准入；共享 runner 与跨 runner；目标依赖源输出；正常双侧路径不回归。此项影响状态机和生命周期，不作为一个“小配置”立即部署。

## 7. 比较策略：先验证已有保护，再有据修改

已存在：strict/noise-tolerant-v1、动态 token、JSON 路径忽略、文件显式 include 保护、截断流不确定处理、进程签名。保留原始差异与规则来源；不能泛化忽略 **/tmp_* 或 host/user/cwd 等业务字段。

必须保留负向对照：固定端口改变、业务文件遗漏、显式 include 的 .DS_Store 遗漏、退出码变化、截断但摘要不同、重复资源关系改变。先以固定样例验证策略，发现具体误判才改对应规则。回归比较不只看正向 matched 数量。

后续 network/registry Collector 需真实消费者、合成 fixture、覆盖限制和权限设计。注册表副作用、网络握手等若是任务核心 oracle，现有维度不足就是该任务验收阻断，不能统一说“可选、不影响”。

## 8. 部署与回退

每项改动提交独立差异与对应测试，在获准环境形成不可变发布。若修改正式契约，部署 Controller/Agent/快照作为一个一致性单元；不得只升级一边。保存旧发布、安装回执与匹配快照，确认无活动 job 后变更。失败恢复旧版本并重新验证，不改写原 job。

## 9. 开发就绪清单（可领取）

本节把 §2–§6 的规格收敛为可开发任务卡。**代码入口已在候选源码中逐条核对存在**（2026-10-09 只读）；
行号以候选 commit `db2ccc03…` 为准，实际开发前须先冻结 commit。

### 9.1 公共前置

| 项 | 要求 |
|---|---|
| 开发位置 | 评估仓库 `E:\桌面文档\Code_Convert\.worktrees\evaluation-noise-v1`；**不在转换 Skill 仓库创建 Controller** |
| 冻结 | 先记录开发 commit 与当前部署回执；不得把候选源码行为当作线上行为 |
| 契约一致性 | 若改动正式契约，Controller/Agent/快照须作为一致性单元升级，禁止只改一侧 |
| 测试 | 用受控 fixture 做工程测试；**不得为健康/诊断接口启动样本** |
| 本机边界 | 本机不编译、不运行、不部署；工程测试在获批环境执行 |

### 9.2 T02-b 就绪诊断（P0）

| 项 | 内容 |
|---|---|
| 入口 | `apps/remote-controller/remote_host_controller/app/main.py` 的 `health()`（约 :153）；`app.state.contract_manifest_error`（约 :160）；`services/runner_registry.py` 的 `snapshot()`（:19）、`set_state()`（:25） |
| 现状（已核对） | `health()` 返回 `version`/`ready`；`ready = job_service.ready and contract_manifest_error is None`，**不含 runner 可调度摘要** |
| 拟议新增字段 | `executionReady`、`readyRunnerCount`、`blockedRunnerCount`、`checkedAt`、`blockingReasons` |
| 实现约束 | 只读 registry 快照；不在 health 内轮询 VM、回滚快照或取执行锁；`BUSY` 与 `QUARANTINED` 分开；保留 `ready` 原语义 |
| 产出 | 代码改动 + 受控 registry fixture 测试 + 兼容说明 |
| 验收 | 全隔离时 `ready` 可仍 true 而 `executionReady=false`；一台 ready 时仅摘要变 true，任务不匹配仍拒绝；BUSY 不显示成永久损坏；旧客户端继续可读现有字段 |
| 停止条件 | 若字段被严格 schema 消费，须同步契约与适配，不能只改服务端 |

### 9.3 T02-c 契约故障定位（P0）

| 项 | 内容 |
|---|---|
| 入口 | `services/agent_client.py` 的 `validate_agent_identity`（比较点约 :43，`code="CONTRACT_MISMATCH"` 约 :46，OS/arch 校验约 :57–67、:89–97）；`services/vm_lifecycle.py` 隔离分支；`runner_registry.py`、`api/runners.py` |
| 现状（已核对） | 已在哈希不符时产出 `CONTRACT_MISMATCH` 并隔离，但**未保留 expected/actual 对照** |
| 拟议新增诊断 | `runnerId`、`expectedContractSetHash`、`actualContractSetHash`（缺失为 `null`）、`checkedAt`、`checkPhase`、`reasonCode` |
| 实现约束 | 沿用现有拒绝/隔离逻辑，**不得跳过校验**；发布版本只在 Agent/回执确有提供时填写，不从 `version=1.0.0` 推断；不把 Agent URL、完整配置、token 或响应体写进公开错误 |
| 产出 | 代码改动 + 既有测试同步 + 无凭据日志断言 |
| 验收 | 匹配/不同/缺失/格式非法/不可达分别返回正确原因；不匹配仍零执行；故障可关联实际角色；日志无凭据 |
| 停止条件 | 返回类型不容纳新字段时，先按既有结构给明确 message 或在明确版本的附加诊断字段实现，不向严格 schema 塞未知键 |

### 9.4 T02-d 观察义务预检（P0）

| 项 | 内容 |
|---|---|
| 入口 | `apps/vm-agent/vm_agent/app/observations.py` 的 `build_observations()`（:38）；`registry`/`network` 的 `_out_of_scope_result()`（:58–59）；`OUT_OF_SCOPE_LIMITATION`（:13）；`app/capabilities.py`；Controller `services/runner_resolver.py`、`comparison_manifest.py` |
| 现状（已核对） | `registry`、`network` 明确为 out-of-scope，返回固定 limitation 字符串 |
| 目标 | 增加可解释的"需要哪些观察、哪些支持、哪些缺失"检查 |
| 实现约束 | 先核对现有 InputProfile/FunctionalProfile 能否表达 required obligation，**不新造平行总 schema**；若缺 required/optional 区分，先提契约变更并携带两侧一起升级 |
| 产出 | 能力预检改动 + 三系统能力差异测试 |
| 验收 | output-only 正常；必需 network/registry 不被标为 matched；可选缺失仍有明确 limitation；三系统能力不同能分流；源/目标任一侧缺维度保留缺口 |
| 须保留 | 现有 comparator 对未观察维度给 `inconclusive` 的保护，不重复开发 |

### 9.5 T02-e 目标侧独立诊断（P1，有条件进入）

| 项 | 内容 |
|---|---|
| 入口 | `services/dual_run_orchestrator.py` 的 `execute()`（:94）、`source_exec_status` 早返回分支（**已核对 :170–173**，条件为 `("launch-failed","timed-out","blocked")`） |
| 目标 | 新增**显式**诊断执行模式，默认保持原行为 |
| 进入条件 | 源失败可归因于已执行的构建/启动问题 **且** 源侧清理成功 **且** 目标自身已获准入 **且** 输入不依赖失败源产物 |
| 立即停止 | 契约/隔离/资源/证据身份失败、源超时原因未知、清理失败 |
| 输出语义 | 缺源有效基线时 `behaviorVerdict=inconclusive`；目标编译成功可单独报告但不算等价；源失败+目标成功不得把任务改成 passed |
| 最低回归 | 源编译失败/目标成功；源启动失败/目标失败；源超时；源清理失败；目标不准入；共享 runner 与跨 runner；目标依赖源输出；正常双侧路径不回归 |
| 停止条件 | 影响状态机与生命周期，**不作为一个"小配置"立即部署**；模式承载字段须走契约扩展/兼容评审 |

### 9.6 状态与依赖

T02-b/c/d 三条目**无外部依赖、可立即开发**；T02-e 依赖 T02-a 完成且真实任务出现源失败场景。
T02-a 受现场状态阻断（需发布回执与无活动 job 窗口），本机无法推进。

源码级依据见[平台功能评估](../reports/Controller-VM-Agent功能评估.md)；任务状态见[任务台账](../tasks/task-execution-checklist.md)。
