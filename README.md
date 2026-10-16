# Code Convert Skill

面向网络攻防相关代码的 Markdown 转换知识与执行契约。Agent 按源码事实加载语言方向、语言语义、场景、系统和工作流，由执行任务的智能体当前模型生成目标代码及修订，不依赖 `.env` 模型配置，并通过隔离评估系统取得独立证据。

## 使用入口

- [根 SKILL.md](SKILL.md)：必读契约、知识选择与逐项执行顺序。
- [执行约束](AGENTS.md)：手工调度、门禁、安全和交付要求。
- [42 个语言方向](skills/directions/)与[七语言语义导航](skills/references/seven-language-common-semantics.md)：每项必读源/目标语言页和一个方向。
- [场景](skills/scenes/)与[系统方向](skills/systems/)：按源码实际行为和条目前提加载。
- [长文件工作流](skills/workflows/long-file-conversion/SKILL.md)、[批次工作流](skills/workflows/batch-conversion/SKILL.md)与[单项闭环](references/workflow/conversion-evaluation-loop.md)：规定准备、推进、恢复与收尾。
- [参考总索引](references/README.md)：任务状态、评估准备、交付、安全和 Controller 适配。

Codex 从 `.agents/skills/code-convert/SKILL.md` 进入；其他 Agent 从根入口进入。所有入口均执行相同门禁，不以单独加载方向页代替必读契约。

## 转换与评估

单文件和批量每项转换前先按[评估准备 §1.0](references/framework/evaluation-readiness-contract.md#10-转换前可达性检查与仅转换分支)检查第三方评估系统可达性。可达时逐项冻结并回读，再分类 ALLOWED、源侧预检、生成、自审、评估准备、提交、取证及归因；缺合法行为入口但源可构建时，按 LIB_UNOBSERVABLE_COMPILE_ONLY 转换并验证目标语法/编译。不可达时说明原因，仍冻结、分类、转换和自审，不编译运行，交完整目标与 `result.md`，未开展维度 UNVERIFIED、适用件齐备后 PARTIAL。所有已处理项均核对应产物后才记终态，未知提交/未决执行仍 WAITING。

本机只读写和审阅文本，不编译或运行源码、转换产物及构建脚本。动态评估只在获批且逐例核实隔离的环境进行；READY、快照和分类 ALLOWED 不替代授权或网络隔离证据。

交付完整性、语法/编译、行为和安全分别报告。规则、模型自评及编译通过不替代行为证据；没有对应版本和冻结条件的证据，记 UNVERIFIED。实际能力与比较策略按现役 Controller/Runner 身份和适配核对。

任务源码、凭据、模型原文、一次性测试数据和案例索引按任务交付范围保存，不并入可复用知识索引。规则使用不依赖一次性数据集长期存在。
