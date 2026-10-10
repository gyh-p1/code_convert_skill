---
name: code-convert
description: Use for code conversion tasks in this repository. Load the platform-neutral project guidance and matching language, scene, system, and task-workflow knowledge; do not claim unsupported coverage.
---

# Code Convert — Codex 发现入口

这是 Codex 的薄入口，不在这里维护第二份转换规则。先读取仓库根目录的 [通用 Skill 入口](../../../SKILL.md)，再依任务按需读取其中链接的语言方向、场景、系统方向和工作流 Skill。长单文件任务应读取长文件工作流；单文件可按需参考根入口链接的功能保持与第三方评估指导；它只帮助准备行为目标、可接受差异及评估移交，不作功能裁决。短片段不应强制加载单文件指导。

**一次提交包含多项任务时**（项目基线为单批不少于 40 项、允许排队、逐项评测），必须读取[批量转换工作流](../../../skills/workflows/batch-conversion/SKILL.md)：它规定原始数据集接入、Agent 派生冻结、排队、持久化与恢复、失败分层和批次汇总，不重复单项转换规则。

**执行约束以仓库 [AGENTS.md](../../../AGENTS.md) 为准，且优先于任何"自动化"字面理解**：Agent **只手工、依次地调度每一项**，**严禁编写、生成、保存或运行任何辅助脚本、工具或自动化程序**（唯一豁免是钉 SHA 的安全分类器）。"允许排队 / 逐项评测"指的是**逐项提交后由隔离平台给出评估证据**，**不指** Agent 用脚本跑批。

**动手前先看根入口的三道硬门禁**（[SKILL.md](../../../SKILL.md) 与 [AGENTS.md](../../../AGENTS.md) 执行约束 §3；本薄入口不复制其内容）：顺序固定为 **冻结 → 分类 `ALLOWED` → 源侧构建预检 → 生成 → 自审 → 评估就绪核对（安全 + 驱动 + oracle）→ 提交 → 取证 → 先归因再分层报告**，**不得颠倒或省略**。其中**驱动必须满足四要素**（按冻结 argv/stdin 启动、**到达被观察状态**、采集真实观察、终止收尾）；"启动后等它自己退出"**不是**通用驱动。**任一环未通过即不得进入下一环，更不得提交。**

适用知识与未覆盖能力由根入口说明。本发现入口不维护测试数据集索引、历史批次统计或第二份规则。项目知识的内联路由可以保留；规则使用不依赖一次性测试数据长期存在。显式调用本 Skill 不是运行源码或转换产物的授权。
