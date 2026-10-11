---
name: code-convert
description: Use for code conversion tasks in this repository. Load the project entry, mandatory task contracts, and matching language, direction, scene, system and workflow knowledge without claiming unverified coverage.
---

# Code Convert — Codex 发现入口

先读取 [AGENTS.md](../../../AGENTS.md) 和仓库根 [SKILL.md](../../../SKILL.md)。根入口维护必读契约与按事实加载的知识索引，本页不维护第二份规则。

正式转换必须手工、串行、逐项推进，不写任何辅助脚本/工具/驱动或自动化程序。顺序：冻结→分类 ALLOWED→源侧预检（构建 + 适用运行基线）→生成→自审→评估就绪→提交→取证→归因/分层报告→交付完整性门禁。需行为评估时，生成前须在获批隔离环境按冻结条件运行源并取得有效基线；明确文本交付/无行为评估片段和真正无安全入口的仅编译例外只按[评估准备 §1.1](../../../references/framework/evaluation-readiness-contract.md#11-生成前源侧预检)，不免分类与构建门槛。纯文档审阅不触发转换步骤。

按根入口加载任务状态、分类准入、构建前提、单项闭环、评估准备、交付与安全真源。驱动四要素和合法来源、无安全入口仅编译例外只按评估准备契约；收尾按模式/实际阶段核适用件，不伪造未发生 job。显式调用 Skill 不构成运行授权。

开始处理每项即必读[交付契约 §1.1](../../../references/framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)，不是等生成成功才加载。正常结束、提前失败/阻断、非可转换和 WAITING 暂停统一写本项 result.md，并按实际阶段逐件回读产物、版本及指针，保存核对结果；缺应有件不得终态，暂停报告不解除未知提交/活动或未确认清理。任何提前停止分支都回根步骤 6，不等批次对账才补报告。

冻结条件与实际请求/知识、原响应/目标、自审及 job 的版本关联按任务状态 §2.1 回查；源基线复用按评估准备 §1.2，自审格式恢复与有限计数按单项闭环。当前仓库内容不代历史快照，新稿无独立证据不继承旧稿 PASS；批次阈值按唯一 taskId，不将恢复/重提重复计项。

多项任务必须加载[批量工作流](../../../skills/workflows/batch-conversion/SKILL.md)，长文件加载[长单文件工作流](../../../skills/workflows/long-file-conversion/SKILL.md)，两者可以同时使用。语言/方向/场景/系统与 ATT&CK 索引按源码事实加载；行为指导用于目标与允许差异说明，不能替代必读准备契约或第三方裁决。

能力和证据边界由根入口说明。本入口不索引测试数据集、历史批次或工程阶段；规则应用不依赖一次性测试数据长期存在。

转换知识默认离线消费：只读取随仓库交付的正文和本地参考，网页/资料标题不能代替必需知识；缺语义或版本时记录具体缺口，不靠联网推定覆盖。按根入口加载适用正文，不把出处追溯变成联网步骤。
