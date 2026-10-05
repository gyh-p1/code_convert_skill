---
name: code-convert
description: Use for code conversion tasks in this repository. Load the platform-neutral project guidance and matching language, scene, system, and task-workflow knowledge; do not claim unsupported coverage.
---

# Code Convert — Codex 发现入口

这是 Codex 的薄入口，不在这里维护第二份转换规则。先读取仓库根目录的 [通用 Skill 入口](../../../SKILL.md)，再依任务按需读取其中链接的语言方向、场景、系统方向和工作流 Skill。长单文件任务应读取长文件工作流；短片段不应强制加载它。**一次提交包含多项任务**（项目基线为单批不少于 40 项、允许排队、自动逐项评测）时，还应读取[批量转换工作流](../../../skills/workflows/batch-conversion/SKILL.md)：它只规定批次冻结、排队限流、持久化与恢复、失败分层和批次汇总，不重复单项转换规则。

场景包括网络 I/O、文件 I/O、进程执行与并发。系统方向包括套接字层 POSIX ↔ Winsock、POSIX ↔ Windows 文件路径（含 macOS 路径位置约定）、POSIX ↔ Windows 进程创建与身份/权限、POSIX ↔ Windows 线程，以及 Windows 注册表与服务子系统；其中文件系统 POSIX→Windows 已有三份逐例目标编译证据，但功能未验证，du 目标未构建。PE 解析、Linux 内核接口与 macOS 专有子系统仍无 Skill，未经本项目转换验证。对未覆盖的 API 必须指出知识缺口，不把其他平台规则假定为等价。700 个 LF 归一化物理源代码行只是规划中的上限，长文件范围内的转换效果未经验收。

原固定四例无 RAG/RAG 测试已取消；现有 C01 探索证据保留但不作为正式基线。显式调用本 Skill 本身不是运行源代码或转换产物的授权。
