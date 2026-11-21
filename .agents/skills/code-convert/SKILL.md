---
name: code-convert
description: Use for code conversion tasks in this repository. Load the project entry, mandatory task contracts, and matching language, direction, scene, system and workflow knowledge without claiming unverified coverage.
---

# Code Convert — 发现入口

执行代码转换、批量转换或评估任务前，先加载 [AGENTS.md](../../../AGENTS.md) 与根入口 [SKILL.md](../../../SKILL.md)，所有规则、契约与[知识路由清单](../../../skills/routing-manifest.json)以根入口及其指向的真源正文为准，不单独请求外部模型、不编写辅助脚本、本机不编译运行样本。

## 执行基线指针（单真源，不重复正文）

- **执行角色与红线**：执行本任务的当前智能体模型直接用原生工具手工、串行、逐项完成画像、冻结、生成、自审与有限修订；第三方智能体**不得编写**或运行任何辅助脚本/驱动（仅评估可达时可按[分类准入](../../../references/workflow/classifier-agent-gate.md)在获准外部临时目录手工逐项调用登记分类器）；[加载核对工具](../../../tools/README-loading.md)仅由系统维护侧运行，无系统接入时以原生工具手工全量核对并记录 manual 依据。
- **可达性分流与阶段链**：先按[评估准备 §1.0](../../../references/framework/evaluation-readiness-contract.md#10-转换前可达性检查与仅转换分支)只读检查评估系统可达性；可达走“冻结→分类 ALLOWED→源侧预检（正常行为或 §1.3 `LIB_UNOBSERVABLE_COMPILE_ONLY`）→生成→自审→就绪核对→提交→取证/归因→交付”，不可达记 `EVALUATOR_UNREACHABLE_CONVERSION_ONLY`，直接走“冻结→防御性生成→[闭环 §4.3](../../../references/workflow/conversion-evaluation-loop.md#43-不可达分支的双通道静态自审编译前端核对与行为推演)双通道静态自审→[交付契约 §1.1](../../../references/framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)部分交付”。
- **冻结与全维度防漏门禁**：推进前必须写出并回读 `01-frozen/frozen-inputs.md`，按[任务状态 §2.2/§2.3](../../../references/framework/task-state-contract.md#22-冻结落盘门禁)与根入口[一页式按需路由卡](../../../SKILL.md#一页式按需路由卡闭集防漏清单)逐项落实闭集勾选/排除（必读契约 + 共性导航 + 源/目标两语言页 + 一个方向及其随附子参考 + 4 场景 + 5 系统 + 2 专题），多项首项前读[批量工作流](../../../skills/workflows/batch-conversion/SKILL.md)，超 700 行或目标显著膨胀在建图前读[长单文件工作流](../../../skills/workflows/long-file-conversion/SKILL.md)。
- **离线消费与外部适配**：知识全部离线消费；使用 Controller 时先读连接检查正文，可达后再补[当前协议适配](../../../references/adapter/controller/platform-revision-adapter.md)。无论完成、阻断或 `WAITING` 暂停，均从统一收尾入口写 `result.md` 并核对实际产物，按[评估准备 §5.1](../../../references/framework/evaluation-readiness-contract.md#51-有效性消噪与功能分类的次序)分层报告且不合成单一成功率。
