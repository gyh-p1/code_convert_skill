# references/

跨 Skill、跨阶段复用的**权威参考文档**。按作用分三类：

## workflow/ — 流程与工作流

转换任务从冻结到关闭的阶段编排与门槛。

| 文档 | 作用 |
|---|---|
| [workflow/conversion-evaluation-loop.md](workflow/conversion-evaluation-loop.md) | 转换—自审—第三方评估闭环：FROZEN→GENERATED→SELF_REVIEWED→SELF_REPAIRED(≤2)→EVALUATION_READY→EVALUATED→REPAIR_AFTER_EVAL(≤2)→CLOSED 各阶段门槛 |

## framework/ — 契约、模式与安全边界

交付物必须满足的结构性契约、manifest 模式与安全策略。

| 文档 | 作用 |
|---|---|
| [framework/delivery-handoff-contract.md](framework/delivery-handoff-contract.md) | 交付与移交契约：中文报告骨架、§2.2 阶段产物落点与命名 |
| [framework/evaluator_manifest.example.json](framework/evaluator_manifest.example.json) | `third-party-evaluator-manifest` 完整占位模板（照抄结构、只改值） |
| [framework/safety-boundary.md](framework/safety-boundary.md) | 隔离/外联/凭据/样本运行的安全边界 |

## adapter/controller/ — 外部评估基础设施适配

对接已授权隔离第三方 VM Controller 的连接与提交方式。

| 文档 | 作用 |
|---|---|
| [adapter/controller/remote-controller-adapter.md](adapter/controller/remote-controller-adapter.md) | 远端 Controller 连接坐标、`/api/jobs` 契约、comparison capsule 组装、curl 提交/轮询/取证流程、结论回填规则、安全边界 |

> 移动文档后请保持相对链接可解析；根 `SKILL.md`、`docs/**`、各 `skills/**/SKILL.md` 及 case 产物均按 `references/<类别>/<文件>` 引用本目录。
