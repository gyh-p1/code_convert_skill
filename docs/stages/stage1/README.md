# Stage1：开发方案与证据导航

> 版本：v4.0；更新：2026-10-09
> 分类器：v2.3（47 项合成回归通过）；准入策略：Spec04 v2.1 已实施
> 当前平台：1.0.26 部署与健康验收通过；当前版本双侧样本复验：未执行；独立交付：未完成；转换测验：按用户今晚要求准备 Agent 暂行路径，具体任务与现场证据仍须核对

本工作包按"计划、规格、任务、证据"四类组织。主线为 **分类分流 → 输入与环境准备 → 批次提交 → 双侧取证 → 完整剥离**。
T06–T08 保持取消：不新增分类器 HTTP 服务、Agent 调度封装或 Docker 路线。

## 1. 两份标准文档

本工作包以以下两份为准，其余文档不得与它们冲突：

| 标准 | 内容 |
|---|---|
| [分类器 v2.3](../../../tools/safety_classifier_v2.py) | 实际实现：词法线索、输入完整性、二元准入判定、CLI |
| [Spec04 最高危阻断准入策略](specs/tiered-admission-policy.md) | 准入规则真源：三条阻断规则、批次授权、零容忍项 |

回归入口：[test_safety_classifier_v2.py](../../../tools/test_safety_classifier_v2.py)（47 项）。

## 2. 计划

- [Stage1 开发方案](Stage1-双侧运行覆盖率提升方案-最终版.md)：范围、基线、开发顺序、依赖、退出条件与剥离边界。

产品阶段和能力承诺仍以[业务边界](../../项目业务文档和能力边界.md)、[开发规范](../../项目开发规范.md)
及[安全边界](../../../references/framework/safety-boundary.md)为准；"最终版"是既有文件名，不表示已验收或已交付。

## 3. 规格

- [分类器与准入](specs/safety-classification-and-admission.md)：v2.3 的实际输入输出、分类含义、兼容迁移与局限。
- [最高危阻断准入策略（Spec04）](specs/tiered-admission-policy.md)：**标准**。三条阻断规则、批次授权记录、回退与应急。
- [Controller/Agent 开发规格](specs/controller-agent-improvements.md)：T02 各项的可开发入口、拟议字段、兼容与回归。
- [双侧验收与完整剥离](specs/verification-and-extraction.md)：证据字段、指标、回归矩阵、迁移清单和回退。

## 4. 任务与证据

- [任务执行台账](tasks/task-execution-checklist.md)：**任务状态唯一入口**。T01–T05 的产物、验收、依赖与停止条件。
- [分类器一致性审查与 Agent 暂行接入](reports/分类器一致性审查与Agent暂行接入-2026-10-09.md)：已接入根入口、批量、闭环和提交适配；47 项远端回归与 5 条合成结果消费通过，现役部署不变，平台强制接入仍待实施。
- [平台问题全量清单](reports/platform-issue-inventory-2026-10-09.md)：逐字挖掘总评估报告与批次事件得到的 **13 项平台问题**（P1 已更正为已修复）。
- [构建适配能否由 Skill 承担](reports/build-adaptation-skill-scope-2026-10-09.md)：**C8–C10 归属分析** —— C8 可走 Skill+契约，C9 需代码，C10 部分已修复。
- [构建前提规则落地记录](reports/build-prerequisites-skill-implementation-2026-10-09.md)：**已实施**。全量盘点 54 份 SKILL.md（仅 1 份有构建前提），新建共享规则页并接入 42 方向 Skill + 根入口 + 批量工作流。
- [全面重新部署方案](specs/full-redeployment-plan.md)：**当前路线**。就绪度核查（源码/离线依赖/工具齐备）与分层部署流程。
- [1.0.26 部署与快照记录](reports/1.0.26部署与快照更新记录-2026-10-09.md)：四角色原包健康验收通过，三 Runner READY/clean；最终快照已生效，macOS 冷启动自动登录通过。
- [发布前变更清单](specs/release-change-list.md)：待确认的 C1–C10 变更项与优化取舍。
- [CONTRACT_MISMATCH 根因定论](reports/contract-mismatch-root-cause-2026-10-09.md)：逐版本重算证据（保留为事实记录，已非阻塞项）。
- [平台优化完成度核查](reports/platform-optimization-readiness-2026-10-09.md)：逐项判定 Spec02 各项是否已完成。
- [平台部署事实核查](reports/platform-deployment-facts-2026-10-09.md)：已部署回执、发布包、回滚脚本与四场景验收证据。
- [平台功能与优化评估](reports/Controller-VM-Agent功能评估.md)：源码级能力、现场状态、优化收益与限制。
- [准入策略修订与六批复跑](reports/最高危阻断策略修订与六批复跑.md)：对照 Spec04 的差距清单、v2.3 修订、恢复前 219 条准入结果。
- [输入恢复与恢复后复跑](../../test/dataset/stage1-admission-recheck-2026-10-09/post-recovery-report.md)：**最新**，24 条恢复记录、恢复后 178/219 允许。
- [输入恢复性核查](../../test/dataset/stage1-admission-recheck-2026-10-09/missing-input-recovery.md)：39 条缺失的成因与逐条可恢复性。

## 5. 当前事实基线

| 项 | 事实 | 不能推导 |
|---|---|---|
| 分类器 | v2.3；47/47 合成回归通过 | 全量准确率达标 |
| 分类器接入 | Agent 提交前暂行消费者已接入；身份/哈希、阻断、独立授权/隔离分别核对 | 现役平台已强制拒收，或 ALLOWED 即可执行 |
| 输入恢复 | 39 条缺失中 **24 条已按 SHA-256 逐字节恢复**；15 条仍缺失 | 恢复等于可放行 |
| 六批准入 | 恢复后 ALLOWED **178/219（81.3%）**；BLOCKED 41 | 允许项已具执行许可 |
| 阻断构成 | 输入错误 15 + 公网未隔离 26；凭证 0 | 凭证规则过窄或数据集无凭证 |
| 当前平台 | 四角色 `1.0.26`，manifestHash `5b252c4d…`，契约 `e088a356…`；三 Runner READY/clean，Controller ready=true | 健康通过等于样本执行、功能或隔离验收通过 |
| 平台部署 | **整体重新部署与健康验收完成**，三台最终基线和 Controller 引用已更新；macOS 自动登录通过 | 旧 R11/R12/R2 仍是现役基线 |
| 隔离 | 历次核查未建立批次级网络隔离证据 | 快照/私网地址等于已隔离 |
| 独立目录 | `third-party-evaluation-system` 仅占位 README 与空目录 | 已是完整可部署系统 |

> **时点纪律**：本表混有"源码级事实"与"历史部署证据"。2026-10-09 03:16 的 runner READY 快照
> 与另一次 GET 的 `CONTRACT_MISMATCH` **时点不同**，不得并列成"当前状态"。
> 详见[平台部署事实核查](reports/platform-deployment-facts-2026-10-09.md)。

## 6. 下一步

1. **T02-a 已收口**：1.0.26 四角色 health-only 校验通过，三 Runner READY/clean，
   最终基线生效；本次没有提交样本，后续评估仍须核对隔离与授权。
2. **今晚 Agent 路径**：T01-d-agent 已接入；为实际测验范围核对任务、真实隔离证据及授权记录。
   网络条件补齐后重分类，重新检查所有阻断；不直接把原 26 条公网阻断项改成允许。平台 T01-d 留待后续，不阻断符合暂行门槛的测验。
3. **T04/T05**：固定无害对照（**已有四场景历史证据可复用**）→ 真实小切片 → 单批 ≥40 →
   双侧验收 → 完整剥离到 `third-party-evaluation-system`。
4. 在用户已确认的测验范围内，逐项条件齐全即可开始，不重复索取已有授权；本机不执行样本，管理接口传输不代表允许样本外联。

**数据集裁定**（2026-10-09 用户）：batch-01 剩余 15 条缺失输入**不恢复**，它们是部分测试用例，
后续由用户另行提供其他测试用例。这 15 条保持 `BLOCKED_INPUT`，不阻断分类器优化与平台升级。
