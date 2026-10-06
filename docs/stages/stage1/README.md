# Stage 1｜第三方评估平台升级方案

> 状态：`PLANNING_ONLY`  
> 计划冻结日期：2026-10-06  
> 适用对象：现役 Remote Controller + Windows/Linux/macOS VM Agent 评估链路  
> 目标：把“安全阻断”从一次性人工判断升级为可复核的 Evaluation Disposition、分级 Execution Profile、环境 Attestation、Execution Permit 和证据归档闭环。

## 本阶段不是什么

- 不是在本仓库实现 Controller、VM Agent 或本地评测运行时。
- 不是授权在本机编译/运行源码、目标代码、构建脚本或第三方样本。
- 不是承诺 87 项都执行真实危险行为，也不是把 synthetic fixture 的通过写成真实攻击成功。
- 不是把现役 R11/R12 runner 状态、`READY`、快照回滚或已有 comparison 报告当成网络隔离证明。

## 文档导航

| 目录 | 文档 | 用途 |
|---|---|---|
| `plans/` | [stage1-upgrade-plan.md](plans/stage1-upgrade-plan.md) | 目标、现状、分阶段路线、决策门、风险和回滚 |
| `specs/` | [safety-planner-and-disposition.md](specs/safety-planner-and-disposition.md) | 风险分类、Disposition、Safety Plan 和规划器契约 |
| `specs/` | [execution-profile-and-attestation.md](specs/execution-profile-and-attestation.md) | Runner Profile、网络/进程/数据边界、Attestation、Permit |
| `specs/` | [fixture-and-observation-contract.md](specs/fixture-and-observation-contract.md) | synthetic fixture、受控靶标、行为观察面和等价验证边界 |
| `specs/` | [evidence-and-controller-compatibility.md](specs/evidence-and-controller-compatibility.md) | 证据模型、状态机、失败码、旧 Controller 兼容和迁移 |
| `tasks/` | [task-register.md](tasks/task-register.md) | 任务分解、依赖、交付物、验收信号 |
| `tasks/` | [acceptance-and-rollout.md](tasks/acceptance-and-rollout.md) | 阶段验收、最小实验、灰度、回滚和未达标处理 |

## 关键口径

1. 87 项是用户提出的升级目标集合；当前仓库的 `batch-02` 至 `batch-06` 分类文件合计为 179 项，其中 `UNSAFE_NET=66`、`REVIEW_SUBPROC=10`、`UNSAFE_LOCAL=30`、`SAFE_CANDIDATE=73`。因此不能把 87 直接等同于仓库内全部阻断项。T0 任务必须先冻结 87 项清单、源码哈希、分类理由和与既有 batch/case 的映射。
2. 目标验收不是 `87/87 REAL_RUN_PASS`，而是 `87/87` 都有唯一的 `Evaluation Disposition`：`DIRECT_SAFE_RUN`、`ISOLATED_NET_RUN`、`RESTRICTED_PROCESS_RUN`、`FIXTURE_EQUIVALENCE`、`STATIC_ONLY` 或 `BLOCKED_UNMODELED`。
3. 只有 `DIRECT_SAFE_RUN`、`ISOLATED_NET_RUN`、`RESTRICTED_PROCESS_RUN` 中确实提交并获得证据的任务，才可报告真实执行证据；`FIXTURE_EQUIVALENCE` 只能报告“受控观察面上的义务匹配”，不能报告真实目标、真实凭据、真实漏洞或真实持久化成功。
4. 任何入口越过已证明的网络、数据、进程或权限边界，Permit 必须拒绝；不能通过删掉核心行为、空跑、伪造输出或只运行转换后的安全子集来制造 PASS。
5. 本仓库只产出规划、契约、任务和静态一致性审阅；Controller/Agent 的编译、运行、网络探针和样本评估须在另行批准且与公网/生产网隔离的一次性环境完成。

