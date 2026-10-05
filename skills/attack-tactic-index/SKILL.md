---
name: attack-tactic-index
description: Retrieval/classification index mapping ATT&CK Enterprise tactics to the conversion knowledge that tends to apply, for offense/defense code. It is an index only — it does not create per-tactic conversion rules, does not decide which API/OS/behavior a given source uses, and never overrides analysis of the code's actual behavior. Also serves as a coverage/gap map.
---

# ATT&CK 战术检索索引

本文件是**检索/分类入口**,不是转换规则。它把 ATT&CK Enterprise 战术映射到本项目已有的语言/场景/系统知识,方便"按攻防用途思考"的人找到对应的转换知识。它**不**为每个战术建独立转换 Skill,**不**由战术标签推断代码用了哪个 API、哪个 OS 或哪种行为,也**不**凌驾于对源码实际行为的分析之上。战术只是缩小"该找什么",不决定"该产出什么"。

> 战术名称与 ID 以 [MITRE 官方 Enterprise 战术列表](https://attack.mitre.org/tactics/enterprise/) 为准。下表按 2026-09-25 核对的 MITRE 官方 Enterprise 列表记录 15 个战术（TA0005 为 Stealth，并包含 TA0112 Defense Impairment）;使用前仍须核对官方列表;引用本索引不代表该战术已有专属转换能力。

> 外部样本目录与旧资料中的战术缩写只作线索；逐例分类须按当前官方 ID/名称和源码实际行为核对。七语言转换知识仍位于根入口、`skills/directions/` 与 `skills/references/`。

## 如何使用

1. 从战术只用于**定位关注点**:知道代码大致用途后,仍必须从源码**实际行为**判断语义场景,不按战术标签假定隐藏行为(判断口径见根 [通用 Skill 入口](../../SKILL.md) §选择适用知识)。
2. 再加载与真实行为匹配的知识:语言方向 + 语义场景(+ 系统方向,若跨 OS)。战术标签本身不进入转换产出。
3. 表中标"暂无对应 Skill"的,说明该行为维度当前没有知识,须按缺口处理并在交付中报告,不用相近规则冒充。
4. 严守 [安全边界](../../references/framework/safety-boundary.md):索引用于组织知识,不用于新增监听/外联、规避、凭证窃取等能力。

## 战术 → 转换知识映射（含覆盖缺口）

"当前可用知识"仅指本项目已有的转换知识;"—/缺口"表示该行为维度目前无 Skill,须按实际行为分析并报告缺口。同一战术常跨多个场景,同一场景也服务多个战术(多对多)。

| 战术 (ID) | 代码层常见语义场景 / 关注点 | 当前可用知识 / 缺口 |
|---|---|---|
| Reconnaissance (TA0043) | 主机/网络信息收集 | 涉及网络时用 [网络 I/O](../scenes/network-io/SKILL.md);主机/环境枚举场景缺口 |
| Resource Development (TA0042) | 多为工具/基础设施准备,常不在被转换目标代码内 | 通常无直接代码场景;按实际行为判断 |
| Initial Access (TA0001) | 投递、入口利用,常含网络 I/O 与文件写入 | 网络部分用 [网络 I/O](../scenes/network-io/SKILL.md) + [安全行为](../scenes/network-io/references/security-behavior.md);文件写入用 [文件 I/O](../scenes/file-io/SKILL.md) |
| Execution (TA0002) | 命令/进程启动、脚本解释 | [进程执行](../scenes/process-execution/SKILL.md)；按 shell/argv、输出、超时与后代回收边界选择 |
| Persistence (TA0003) | 服务/计划任务/启动项/文件落地 | 文件落地用 [文件 I/O](../scenes/file-io/SKILL.md);服务与启动项写注册表时用 [Windows 注册表与服务子系统](../systems/windows-registry-service-subsystem/SKILL.md);计划任务本身仍缺口 |
| Privilege Escalation (TA0004) | 令牌/权限/提权系统 API | 跨 POSIX↔Windows 的身份与特权差异用 [进程创建与身份/权限](../systems/posix-windows-process-identity/SKILL.md);具体提权漏洞利用链不属现有知识 |
| Stealth (TA0005) | 隐匿/隐藏操作、呈现为正常活动 | 按源码实际行为选场景;文件行为可读 [文件 I/O](../scenes/file-io/SKILL.md);不因普通网络/文件功能自动归类;注意安全边界 |
| Defense Impairment (TA0112) | 直接削弱、关闭或篡改防御机制 | 需识别具体系统/进程行为;进程终止用 [进程执行](../scenes/process-execution/SKILL.md) 与 [进程创建与身份/权限](../systems/posix-windows-process-identity/SKILL.md);服务篡改用 [Windows 注册表与服务子系统](../systems/windows-registry-service-subsystem/SKILL.md);PE 解析/驱动与安全产品交互仍缺口;不把普通服务/日志差异推断为该战术 |
| Credential Access (TA0006) | 凭证读取与比较 | 校验/恒定时间比较见 [安全行为](../scenes/network-io/references/security-behavior.md);凭证存储涉及文件时用 [文件 I/O](../scenes/file-io/SKILL.md) |
| Discovery (TA0007) | 本地/网络发现 | 网络部分用 [网络 I/O](../scenes/network-io/SKILL.md);进程与身份查询用 [进程创建与身份/权限](../systems/posix-windows-process-identity/SKILL.md);注册表读取用 [Windows 注册表与服务子系统](../systems/windows-registry-service-subsystem/SKILL.md);其余主机/环境枚举场景缺口 |
| Lateral Movement (TA0008) | 远程服务、跨主机网络 | [网络 I/O](../scenes/network-io/SKILL.md) + 跨 OS 时 [POSIX↔Winsock](../systems/posix-winsock/SKILL.md);无横向移动专门场景 |
| Collection (TA0009) | 文件/输入/剪贴板采集 | 文件采集用 [文件 I/O](../scenes/file-io/SKILL.md);输入/剪贴板场景缺口 |
| Command and Control (TA0011) | 网络通信、自定义/伪装协议 | 最贴合现有知识:[网络 I/O](../scenes/network-io/SKILL.md) + [安全行为](../scenes/network-io/references/security-behavior.md) + [POSIX↔Winsock](../systems/posix-winsock/SKILL.md) |
| Exfiltration (TA0010) | 通过网络外传数据 | [网络 I/O](../scenes/network-io/SKILL.md) + 跨 OS 时 [POSIX↔Winsock](../systems/posix-winsock/SKILL.md);本地暂存用 [文件 I/O](../scenes/file-io/SKILL.md) |
| Impact (TA0040) | 加密/删除/篡改、拒绝服务 | 文件加密/删除用 [文件 I/O](../scenes/file-io/SKILL.md);抗 DoS 相关约束见 [安全行为](../scenes/network-io/references/security-behavior.md) |

## 覆盖现状

当前转换知识含网络、文件、进程执行和并发场景；系统方向含 POSIX ↔ Winsock、POSIX ↔ Windows 文件路径（含 macOS 路径位置约定）、进程创建与身份/权限、线程，以及 Windows 注册表与服务子系统。仍属缺口的是:**PE 解析**、**Linux 内核接口**（`ptrace`/`seccomp`）与 **macOS 专有子系统**（Keychain/launchd/CoreFoundation），以及系统信息/枚举类行为中的其余未建模部分。ATT&CK 15 战术均仅作分类入口，不代表本项目为每个战术提供了转换能力。本表既是检索入口,也是缺口地图;补齐要按"有真实行为消费者才建"的规则推进,不为凑满战术预建空 Skill。

## 依据

- [MITRE ATT&CK Enterprise 战术](https://attack.mitre.org/tactics/enterprise/):战术名称与 ID 的权威来源;本表为快照,须以官方为准。
- ATT&CK 是分类/检索维度,不代替代码行为判断;组合原则与能力边界见根 [通用 Skill 入口](../../SKILL.md) §选择适用知识。
