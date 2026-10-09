# references/

跨 Skill、跨阶段复用的**权威参考文档**。按作用分三类：

## workflow/ — 流程与工作流

转换任务从冻结到关闭的阶段编排与门槛。

| 文档 | 作用 |
|---|---|
| [workflow/conversion-evaluation-loop.md](workflow/conversion-evaluation-loop.md) | 转换—自审—第三方评估闭环：FROZEN→GENERATED→SELF_REVIEWED→SELF_REPAIRED(≤2)→EVALUATION_READY→EVALUATED→REPAIR_AFTER_EVAL(≤2)→CLOSED 各阶段门槛，以及语法/构建与功能反馈分流、有限修复和第三方重评 |
| [workflow/behavior-preservation-contract.md](workflow/behavior-preservation-contract.md) | 功能保持与第三方评估指导：行为目标、可接受差异、评估移交及第三方修复反馈；不自设功能裁决标准 |
| [workflow/build-prerequisites.md](workflow/build-prerequisites.md) | **构建前提与工具链适配**：链接库（Winsock `ws2_32`）、C# `.csproj`（含"必须记录原本缺什么"）、Go 工具链版本与构建缓存；核心原则是前提须写进任务契约的 `buildCommand`，不能等构建失败后人工补 |
| [workflow/classifier-agent-gate.md](workflow/classifier-agent-gate.md) | 分类结果准入：**ALLOWED 即准入通过、允许运行**，Agent 不作主观复核；仅核对提交内容与分类输入的身份/哈希一致性及独立授权/隔离记录。不改变现役部署，不宣称平台强制接入 |

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
| [adapter/controller/remote-controller-adapter.md](adapter/controller/remote-controller-adapter.md) | 远端 Controller 连接坐标、`/api/jobs` 契约、comparison capsule 组装、health/runner 留证、提交/轮询/取证与结论回填 |
| [adapter/controller/comparison-policy-adapter.md](adapter/controller/comparison-policy-adapter.md) | `1.0.25-noise.1` 的服务器/任务配置区分、文本与文件消噪接入、关键值保护、minor/semantic_pass 证据及回退边界 |
| [adapter/controller/runner-capability-matrix.md](adapter/controller/runner-capability-matrix.md) | 现役部署身份、runner 语言/快照/生命周期及实测范围；提交时按实时接口复核 |

> 移动文档后请保持相对链接可解析；根 `SKILL.md`、`docs/**`、各 `skills/**/SKILL.md` 及 case 产物均按 `references/<类别>/<文件>` 引用本目录。
