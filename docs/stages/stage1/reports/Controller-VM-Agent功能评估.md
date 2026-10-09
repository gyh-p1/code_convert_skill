# Controller / VM Agent 功能评估与近期优化

> 更新：2026-10-09
> 结论：已有双侧编排及比较基础；**曾完成一次成功部署（1.0.25-noise.1）与四场景双侧验收（4/4）**；
> 当前服务实时状态待复核；诊断和能力预检仍值得立即开发。
> 本报告替代原“无需任何优化、生产验证充分、分类器即可达到75%”结论。
>
> **时点区分（重要）**：本报告混有两类事实，使用前必须分清：
> ① **源码级**：读候选源码所得，不代表线上行为；
> ② **历史部署证据**：2026-10-09 03:10–03:16 时段留下的回执与验收材料，
> 证明**当时**系统可用，不代表**当前**仍可用。
> 三 runner `CONTRACT_MISMATCH` 是某次 GET 复核的时点观测，与 03:16 的 READY 快照**时点不同**，
> 两者不得并列成"当前状态"。详见[平台部署事实核查](platform-deployment-facts-2026-10-09.md)。

## 0. 已存在的部署与验收证据（2026-10-09 只读核查）

在候选源码树 `.codeconvert-state/noise-trial/` 中发现：

| 材料 | 内容 |
|---|---|
| `deployed-receipt.json` | Controller 发布 **1.0.25-noise.1**，安装于 `D:\CodeConvertRemote\Stack\Controller`，03:10:14Z |
| `release/*.zip` | 发布包 `codeconvert-remote-stack-1.0.25-noise.1-windows-linux-macos-x64.zip`（34.1 MB） |
| `rollback-controller.ps1` | 回滚脚本，带活动 job 扫描与版本校验保护 |
| `smoke-evidence/` | **四场景验收 4/4 通过**，含 3 个负向对照；每场景 9 件证据 |
| `runners-after.json` | 03:16 时三 runner 全部 `READY`、`contaminated=false` |
| `test-results.txt` | 源码测试 **190 passed** |

`noise-allowed` 场景显示双侧均真实执行（Windows source / Linux target），
preflight 与 cleanup 均 PASSED，runner 执行后回到 READY。

**这不是本轮运行的**：本轮只读取已有日志与回执，未连接服务、未执行任何脚本。

## 1. 源码与现场分开

候选源码为 `E:\桌面文档\Code_Convert\.worktrees\evaluation-noise-v1`，HEAD为db2ccc0379e9d9281c1578b91745b1e3b1ca9452
（提交信息为"snapshot: 评估消噪试用版 WIP 起点（可回退检查点）"，位于 `codex/evaluation-noise-upgrade` 分支）；
读取时工作区无未提交改动，本轮未修改它。

| 项目 | 事实 | 时点/来源 |
|---|---|---|
| **候选工作树当前契约** | `sha256:f4f58184ff971f0156054983dd23e5189425cc37310b059972d4dde7afaf3274`（20 份 schema） | 本轮按 `contract_manifest.py` 规则独立重算 |
| 历史试用版所装契约 | `sha256:e088a356b48fd1c3f50e480ac24c2fd03319dc60a49b41de4d076219819c4c45` | `health.json`，2026-10-09 03:12 时段 |
| 某次 GET 观测到的现役契约 | `sha256:56b327067f84fb8a62c4d6feca4dff56533a78883b3404882c9c5d903d6c45ed` | 该次只读 GET，时点记于审查材料 |
| health | 历史证据：HTTP 可达、`ready=true`、含 `comparison` 字段 | `health.json` |
| runner（03:16 快照） | 三 runner 全部 `READY`、`contaminated=false`、`lastFailureType=null` | `runners-after.json` |
| runner（另一次 GET） | 三个均 `QUARANTINED`、`CONTRACT_MISMATCH` | 该次 GET，时点不同 |
| 已部署发布 | Controller **1.0.25-noise.1**，`D:\CodeConvertRemote\Stack\Controller` | `deployed-receipt.json`，03:10:14Z |

> **三个契约哈希互不相同**，且 `f4f58184…` 在仓库内检索不到。这说明候选工作树当前检出的契约集合
> 既不等于历史试用版所记录的集合，也不等于曾观测到的现役集合。
> **在未取得现役服务实时 `/api/health` 与 `/api/runners` 之前，不能断言当前契约是否仍不匹配。**

`health.version=1.0.0` 不是不可变发布版本（发布版本是 `1.0.25-noise.1`）；候选源码提交与已部署事实不得混写。
默认路由历史核查仍为隔离未验证，没有本轮新隔离证据。

## 2. 源码级能力评估

以下路径相对候选根；为静态源码证据，不是本轮运行效果。

| 能力 | 实际实现与证据入口 | 评估 |
|---|---|---|
| 双侧编排 | apps/remote-controller/remote_host_controller/app/services/dual_run_orchestrator.py | 源→清理→目标；源blocked/launch-failed/timed-out约第178行起提前结束，并非双侧独立运行 |
| 契约与生命周期 | services/agent_client.py:43、vm_lifecycle.py、runner_registry.py | 会因身份不符隔离；保护应保留，错误信息还可补实际身份 |
| 健康 | app/main.py的health函数 | 当前候选ready是服务就绪，未给整体runner可调度摘要 |
| 输出/文件/进程 | apps/vm-agent/vm_agent/app/observations.py:54及collectors | 已有实现与限制记录，不证明所有源码行为可观测 |
| 网络/注册表 | 同文件:58–59及_out_of_scope_result | 当前未采集；不能称可由文件/进程替代 |
| 文本/JSON/文件比较 | packages/evaluation-core/evaluation_core/evidence_comparator.py | exact、normalized-text、json-structural、noise-tolerant-v1及minor差异机制已存在 |
| 截断与显式文件保护 | 同文件:_stream_comparison_incomplete、_is_noise_event（约355/476行） | 已有保护，先补回归，不重复提案“从零新增” |
| 进程签名 | 同文件:_compare_process_events、causal_signature | 是有限事件签名比较，不能推广为任意API实现路径语义等价 |

源码没有证明“快照=网络隔离”，也未证明对任意任务提供批准/隔离attestation。能力是否足够取决于每个任务的核心oracle，而非预估“大部分场景”。

## 3. 可以立即开发的优化

| 优先级 | 优化 | 最小改动与验收 | 收益 |
|---|---|---|---|
| P0 | 服务/执行就绪分开 | 保留ready，添加registry摘要；全隔离时执行就绪为false，旧客户端兼容 | 避免存活被误读为可提交 |
| P0 | 契约不匹配详情 | 在现有错误路径记录expected/actual、角色、时间和阶段；仍拒绝不匹配 | 减少反复猜测/重装 |
| P0 | 必需观察能力预检 | 按真实profile义务核对两侧能力，不支持的必需维度给明确缺口 | 避免运行后才发现无法回答oracle |
| P1 | 独立目标诊断 | 源代码失败且清理/目标准入通过才继续；无源基线保持inconclusive | 获取目标编译证据，增加生命周期复杂度 |
| P1 | 比较策略反例回归 | 保持固定正负对照，核对截断、固定端口、业务文件/显式include | 防止扩大消噪导致假匹配 |

这些项目均有现有消费者和具体代码入口，可进入开发；本轮没有改平台源码或部署。粗估前三项各0.5–1开发日，独立侧1–2开发日，不含现场等待和三系统回归。详细拟议字段、兼容路径、测试与停止条件见[Spec02](../specs/controller-agent-improvements.md)。

先复核现役服务实时契约与 runner 状态（T02-a）；不能靠新增健康字段或错误日志本身解除 runner 阻断。
升级/回退路线需依据现场回执 —— **现已有回执**（1.0.25-noise.1）与回滚脚本，
但不得据此直接覆盖服务，须先确认当前装的是哪一版。

## 4. 不建议马上扩张的方向

- 不扩大默认文件噪声到 **/tmp_*，不无条件忽略host/user/cwd/timestamp。它们可能是业务义务；每项容忍须有冻结依据。
- 不立即建设通用network/registry采集平台。先挑确有这些核心义务的任务，定义最小合成fixture和观测范围；需要而未实现的任务应阻断或不确定，不能说“可选不影响验收”。
- 不把函数存在、论文机制名称、semantic_pass样例或旧生产描述当成覆盖保证。
- 不恢复已取消的T06–T08；平台已有Controller HTTP接口，不需要再包一层分类HTTP或Docker路线。

## 5. 开发与动态验收结论

平台开发方向评审通过。**动态验收的历史状态已改变**：2026-10-09 03:10–03:16 时段存在一次成功的
Controller 部署（1.0.25-noise.1）与四场景双侧验收（4/4，含 3 个负向对照，环境均 clean）。
因此不能再笼统写"平台未形成"。

但这**不等于当前可用**：现役服务的实时契约与 runner 状态尚未复核，
且候选工作树当前契约哈希（`f4f58184…`）与历史值均不同。下一步：

1. **T02-a**：实时复核 `/api/health` 与 `/api/runners`，确定现役版本与 runner 状态。
2. 确认"最新"是哪一版：候选 HEAD `db2ccc0` 是 WIP 检查点提交，需判断是否应部署更新版本。
3. 补 T03 边界记录，再做固定无害正负对照、小切片和批次。
4. 完成后按 [Spec03](../specs/verification-and-extraction.md) 剥离完整系统。

本轮证据来自源码阅读、状态文件与回执读取；**未执行**平台测试/构建/安装/回退，未连接服务，未修改网络或快照，未新增 job。
`190 passed` 是**读取已有日志**，不是本次运行结果。
