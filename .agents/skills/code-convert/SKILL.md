---
name: code-convert
description: Use for code conversion tasks in this repository. Load the platform-neutral project guidance and matching language, scene, system, and task-workflow knowledge; do not claim unsupported coverage.
---

# Code Convert — Codex 发现入口

这是 Codex 的薄入口，不在这里维护第二份转换规则。先读取仓库根目录的 [通用 Skill 入口](../../../SKILL.md)，再依任务按需读取其中链接的语言方向、场景、系统方向和工作流 Skill。长单文件任务应读取长文件工作流；短片段不应强制加载它。

系统方向包括套接字层 POSIX ↔ Winsock、POSIX ↔ Windows 文件路径与线程初稿（均未经本项目转换验证）；进程等其余跨 OS 方向仍无 Skill。对未覆盖的 API 必须指出知识缺口，不把其他平台规则假定为等价。700 个 LF 归一化物理源代码行只是规划中的上限，长文件流程和转换效果均未经样例验证。

当前已批准未来做四例无 RAG/RAG 探索，但样例、安全和隔离准备完成之前不执行。显式调用本 Skill 本身不是运行源代码或转换产物的授权。
