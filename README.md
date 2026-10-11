# Code Convert Skill

面向网络攻防相关代码的轻量 Markdown 转换知识项目。Agent 按源码事实选读语言方向、共享语言语义、实际场景、源/目标系统和工作流；具体代码转换由本工作区 `.env` 配置的外部模型生成，不建设本地转换或评测运行时。

## 项目入口

- [根 SKILL.md](SKILL.md)：任务模式、知识路由、模型调度和能力边界。
- [42 个语言方向](skills/directions/)与[共享语义导航](skills/references/seven-language-common-semantics.md)：静态规则，不是逐方向转换成功承诺。
- [场景](skills/scenes/)与[系统方向](skills/systems/)：只按源码实际行为和条目前提加载，不预生成维度组合。
- [长文件工作流](skills/workflows/long-file-conversion/SKILL.md)、[批次工作流](skills/workflows/batch-conversion/SKILL.md)与[评估闭环](references/workflow/conversion-evaluation-loop.md)：过程约束，不证明规模、队列或行为已验收。
- [参考总索引](references/README.md)：知识、工作流、契约和适配的职责与加载条件；[任务状态](references/framework/task-state-contract.md)、[评估准备](references/framework/evaluation-readiness-contract.md)、[交付契约](references/framework/delivery-handoff-contract.md)和[安全边界](references/framework/safety-boundary.md)分别维护真源。

Codex 发现入口 `.agents/skills/code-convert/SKILL.md` 只链接根入口；其他 Agent 按自身机制接入。项目知识内联索引可以保留，**不把一次性测试数据集、case/batch、历史 job 或回归位写进 Skill 索引**。

## 规范与当前边界

[业务文档](docs/项目业务文档和能力边界.md)维护需求/能力，[开发规范](docs/项目开发规范.md)维护产品阶段和证据口径，[Skill 编写规范](docs/Skill编写规范.md)维护内容职责。静态文档存在不等于编译、功能、42 方向、战术/OS 覆盖、长文件或批量评测已达标。

本机只读写/审阅文本，不编译、不运行源码、转换产物或构建脚本。已获准的动态评估只在逐例核对隔离的外部环境发生，READY/快照不证明无外联；编译与行为 oracle 分列，无对应证据为 UNVERIFIED。

测试是独立的任务活动；输入/输出/原证据在执行和验收期间可追溯，收尾后的保留期限由交付约定决定，**无需永久保留测试数据集**。一次性测试源码、压缩包、凭据、模型原文和案例索引不随产品提交，不因文件被忽略就删除本地资料。

## 工程规划

[Stage 1](docs/stages/stage1/README.md)包含开发期规格与部分部署记录，各功能状态须逐项核对；[Stage 3 平台能力补强](docs/stages/stage3/README.md)承接精确部署及能力验收；[Stage 4 转换 Skill 架构与评估证据修订](docs/stages/stage4/README.md)维护文本方案、实施清单与静态验收，本轮新增[证据与规则修订任务](docs/stages/stage4/tasks/evidence-quality-checklist.md)。这些是工程工作包，不改变产品阶段；产品状态只认开发规范，工程文档不是转换任务必读依赖。
