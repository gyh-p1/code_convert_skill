# Code Convert Skill

面向网络攻防相关代码的轻量 Markdown 转换知识项目。Agent 按源码事实选读语言方向、共享语言语义、实际场景、源/目标系统和工作流；具体代码转换由本工作区 `.env` 配置的外部模型生成，不建设本地转换或评测运行时。

## 项目入口

- [根 SKILL.md](SKILL.md)：任务模式、知识路由、模型调度和能力边界。
- [42 个语言方向](skills/directions/)与[共享语义导航](skills/references/seven-language-common-semantics.md)：静态规则，不是逐方向转换成功承诺。
- [场景](skills/scenes/)与[系统方向](skills/systems/)：只按源码实际行为和条目前提加载，不预生成维度组合。
- [长文件工作流](skills/workflows/long-file-conversion/SKILL.md)、[批次工作流](skills/workflows/batch-conversion/SKILL.md)与[评估闭环](references/workflow/conversion-evaluation-loop.md)：过程约束，不证明规模、队列或行为已验收。
- [交付契约](references/framework/delivery-handoff-contract.md)与[安全边界](references/framework/safety-boundary.md)：字段来源、报告分层和执行红线。

Codex 发现入口 `.agents/skills/code-convert/SKILL.md` 只链接根入口；其他 Agent 按自身机制接入。项目知识内联索引可以保留，**不把一次性测试数据集、case/batch、历史 job 或回归位写进 Skill 索引**。

## 规范与当前边界

[业务文档](docs/项目业务文档和能力边界.md)维护需求/能力，[开发规范](docs/项目开发规范.md)维护产品阶段和证据口径，[Skill 编写规范](docs/Skill编写规范.md)维护内容职责。静态文档存在不等于编译、功能、42 方向、战术/OS 覆盖、长文件或批量评测已达标。

本机只读写/审阅文本，不编译、不运行源码、转换产物或构建脚本。已获准的动态评估只在逐例核对隔离的外部环境发生，READY/快照不证明无外联；编译与行为 oracle 分列，无对应证据为 UNVERIFIED。

测试是独立的任务活动；输入/输出/原证据在执行和验收期间可追溯，收尾后的保留期限由交付约定决定，**无需永久保留测试数据集**。一次性测试源码、压缩包、凭据、模型原文和案例索引不随产品提交，不因文件被忽略就删除本地资料。

## 工程规划

[Stage 1 评估平台升级包](docs/stages/stage1/README.md)是开发期 PLANNING_ONLY 方案，不表示外部 Controller/VM 已实现 Profile、Attestation、Permit 或 fixture runtime。工程工作包编号与产品阶段不同，产品状态只认开发规范。
