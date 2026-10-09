---
name: code-convert
description: Use for code conversion tasks in this repository. Load the platform-neutral project guidance and matching language, scene, system, and task-workflow knowledge; do not claim unsupported coverage.
---

# Code Convert — Codex 发现入口

这是 Codex 的薄入口，不在这里维护第二份转换规则。先读取仓库根目录的 [通用 Skill 入口](../../../SKILL.md)，再依任务按需读取其中链接的语言方向、场景、系统方向和工作流 Skill。长单文件任务应读取长文件工作流；单文件可按需参考根入口链接的功能保持与第三方评估指导；它只帮助准备行为目标、可接受差异及评估移交，不作功能裁决。短片段不应强制加载单文件指导。**一次提交包含多项任务**（项目基线为单批不少于 40 项、允许排队、自动逐项评测）时，还应读取[批量转换工作流](../../../skills/workflows/batch-conversion/SKILL.md)：它只规定原始数据集接入、Agent 派生冻结、排队限流、持久化与恢复、失败分层和批次汇总，不重复单项转换规则。

适用知识与未覆盖能力由根入口说明。本发现入口不维护测试数据集索引、历史批次统计或第二份规则。项目知识的内联路由可以保留；规则使用不依赖一次性测试数据长期存在。显式调用本 Skill 不是运行源码或转换产物的授权。
