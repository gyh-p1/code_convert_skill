---
name: network-io
description: Use alongside a matching conversion direction when source code performs socket or protocol I/O and the translation must preserve byte-stream, message, timeout, and connection semantics. This is not an independent language conversion direction.
---

# 网络 I/O 场景：转换语义

本场景只在源码确有网络 I/O 行为时与方向 Skill **共同阅读**。它不按关键字或 ATT&CK 标签单独判定行为，也不提供通信目标、隐蔽能力或攻击流程。先确认源/目标平台、流式或报文式接口、同步/非同步模式及调用方协议；未知时保留不确定性。

源码是网络攻防相关代码、且转换可能改变可观察安全行为（路径穿越、不可信输入解析、校验/认证、抗 DoS 上限、解码顺序）时，按需加载 [网络安全行为专题](references/security-behavior.md)：它讲如何在转换中保持源程序原有安全姿态，不新增攻防能力。

## 转换时保留的决策边界

| 源码依赖 | 应保留或确认 | 常见误改 |
|---|---|---|
| 二进制缓冲区、显式长度与帧格式 | 字节序、长度计算、分隔/长度前缀、编码、空字节处理 | 把任意字节转成文本、假设一次读取就是一条完整消息 |
| `send`/`recv` 等流式接口 | 返回的实际字节数、部分发送/接收、EOF、错误及重试条件 | 将一次调用等同于完整发送或完整消息；把 0 字节和错误混为一谈 |
| 连接与超时状态 | 阻塞/非阻塞设置、超时范围、连接关闭、半关闭、资源释放顺序 | 把持续会话变成单次请求，或静默增加无限重试 |
| 已有上层协议或 TLS | 原有字段、验证与失败条件、请求/响应时序 | 擅自去掉校验、改变协议，或添加源码没有的通信能力 |

TCP 提供字节流，不保证应用消息与一次 `send`/`recv` 一一对应；Winsock `send` 的成功返回值也可能小于请求长度。具体函数错误码、零长度语义和关闭行为必须按源平台 API 与目标平台分别核对，不能把 POSIX、Winsock 和 Python 的返回约定混写成同一条规则。见下方来源。

## 与方向 Skill 的组合

方向 Skill 负责语言/API 映射，本场景只补充网络可观察语义和不应丢失的条件。冲突时不要直接照搬某个示例：先保留源程序的协议/状态条件，指出平台差异及缺少的依据，再给出有条件的转换。ATT&CK 战术可以作为检索标签，但不能替代代码中实际的 I/O 行为分析。

源与目标跨越 Linux/POSIX 与 Windows 且源码含套接字调用时，再加载 [POSIX ↔ Winsock 套接字系统方向](../../systems/posix-winsock/SKILL.md)：本场景管字节流/协议语义，该系统方向管两平台套接字 API（句柄类型、初始化、关闭、错误模型、非阻塞、超时、信号）的差异与不可映射项。

不得运行来源不明的网络样本或连接真实服务；当前仅对规则和转换文本做静态工作。不能根据本文件宣称转换行为已验证。

## 依据

- [RFC 9293（TCP）](https://www.rfc-editor.org/rfc/rfc9293.html)：TCP 字节流与分段语义。
- [Microsoft Winsock `send`](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-send)：返回字节数、错误与平台特定行为。
- [Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)：流式 socket 的部分收发与消息边界。仅用于相关目标语言；其他平台要查各自的权威文档。
