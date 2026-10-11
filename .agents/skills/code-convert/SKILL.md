---
name: code-convert
description: Use for code conversion tasks in this repository. Load the project entry, mandatory task contracts, and matching language, direction, scene, system and workflow knowledge without claiming unverified coverage.
---

# Code Convert — Codex 发现入口

先读取 [AGENTS.md](../../../AGENTS.md) 和仓库根 [SKILL.md](../../../SKILL.md)。根入口维护必读契约与按事实加载的知识索引，本页不维护第二份规则。

正式转换必须手工、串行、逐项推进，不写任何辅助脚本/工具/驱动或自动化程序。顺序：冻结→分类 ALLOWED→源侧预检（构建 + 适用运行基线）→生成→自审→评估就绪→提交→取证→归因/分层报告→交付完整性门禁。需行为评估时，生成前须在获批隔离环境按冻结条件运行源并取得有效基线；明确文本交付/无行为评估片段和真正无安全入口的仅编译例外只按[评估准备 §1.1](../../../references/framework/evaluation-readiness-contract.md#11-生成前源侧预检)，不免分类与构建门槛。纯文档审阅不触发转换步骤。

冻结完成必须先写出并回读本项本 run 的 `01-frozen/frozen-inputs.md`；缺失、空白、错项/错版本不分类、不推进，不能等收尾补写。源预检、每次正式模型请求、提交/重提及恢复新增动作前再核，完整规则只消费[任务状态 §2.2](../../../references/framework/task-state-contract.md#22-冻结落盘门禁)；已发生 job 的查询/取证/终止不因缺件延后。不新增检测脚本或平台校验。

按根入口加载任务状态、分类准入、构建前提、单项闭环、评估准备、交付与安全真源。驱动四要素和合法来源、无安全入口仅编译例外只按评估准备契约；收尾按模式/实际阶段核适用件，不伪造未发生 job。显式调用 Skill 不构成运行授权。

开始处理每项即必读[交付契约 §1.1](../../../references/framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)，不是等生成成功才加载。正常结束、提前失败/阻断、非可转换和 WAITING 暂停统一写本项 result.md，并按实际阶段逐件回读产物、版本及指针，保存核对结果；缺应有件不得终态，暂停报告不解除未知提交/活动或未确认清理。任何提前停止分支都回根步骤 6，不等批次对账才补报告。

冻结条件与实际请求/知识、原响应/目标、自审及 job 的版本关联按任务状态 §2.1 回查；源基线复用按评估准备 §1.2，自审格式恢复与有限计数按单项闭环。当前仓库内容不代历史快照，新稿无独立证据不继承旧稿 PASS；批次阈值按唯一 taskId，不将恢复/重提重复计项。

按根入口六步执行：先读全部必读契约，再画像、选知识、完成冻结，随后按第 5 步调度表逐行推进。多项任务在处理首项前加载[批量工作流](../../../skills/workflows/batch-conversion/SKILL.md)，长文件在地图/分段前加载[长单文件工作流](../../../skills/workflows/long-file-conversion/SKILL.md)，两者可以同时使用。每项必读源/目标两语言页与一个方向 Skill，场景/系统/安全行为和 ATT&CK 索引按源码事实加载；加载阶段只准备材料，不提前发送模型请求。知识可达、Agent 已读、模型已注入与效果已验证分别记录，判据见任务状态 §2.3。

能力和证据边界由根入口说明。本入口不索引测试数据集、历史批次或工程阶段；规则应用不依赖一次性测试数据长期存在。

转换知识默认离线消费：只读取随仓库交付的正文和本地参考，网页/资料标题不能代替必需知识；缺语义或版本时记录具体缺口，不靠联网推定覆盖。按根入口加载适用正文，不把出处追溯变成联网步骤。
