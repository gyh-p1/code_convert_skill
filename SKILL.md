---
name: code-convert-skill
description: Use for code conversion requests when a matching conversion direction exists. Distinguishes syntax-focused snippets from behavior-preserving single-file work, and composes applicable language, scene, system, and long-file guidance without claiming unsupported coverage.
metadata:
  short-description: Agent-facing code conversion knowledge Skill
---

# Code Convert Skill

本项目提供给智能体使用的转换知识，不是独立转换程序。在本工作区，用户要求调度 Agent 使用根目录 `.env` 配置的外部模型生成目标代码；Agent 负责画像、Skill 选择、请求调度、静态审阅和移交，不以自身生成替代配置模型。开始时区分：**片段转换**只要求目标语法正确；**单文件转换**还要求按可观察行为约束保持功能；长单文件需加载[长单文件转换工作流](skills/workflows/long-file-conversion/SKILL.md)，该流程目前未经长文件范围内的转换效果验证；700 个 LF 归一化物理源代码行仍是计划上限，不宣称已支持或达标。单文件任务可按需参考[功能保持与第三方评估指导](references/workflow/behavior-preservation-contract.md)，用于整理行为目标、可接受差异及评估移交；它不自设功能裁决标准，功能一致性由第三方平台按已确认任务及现役契约评估，不替代方向/场景/系统规则。

## 选择适用知识

先完成源码画像，再选 Skill；不要先看 ATT&CK 标签再反推代码行为。

七语言共享事实由 [共性语义索引](skills/references/seven-language-common-semantics.md) 路由到各语言参考页；每次只按需加载源语言与目标语言两页（知识基线：C11、C++17、C# 12/.NET 8、CPython 3.12、Go 1.27、PowerShell 7.6、Ruby 3.4）。

**语言方向 Skill（42 个源→目标方向，各有独立入口与实质规则）**：先按实际源/目标语言选定一个方向 Skill，再按源码行为加载适用的场景、系统和工作流知识。跨方向共性语义由各语言参考页维护，不在 42 份文件中重复。

| 源语言 | 目标语言方向 Skill |
|---|---|
| **C** | [C → C++](skills/directions/c-to-cpp/SKILL.md) ｜ [C → C#](skills/directions/c-to-csharp/SKILL.md) ｜ [C → Python](skills/directions/c-to-python/SKILL.md) ｜ [C → Go](skills/directions/c-to-go/SKILL.md) ｜ [C → PowerShell](skills/directions/c-to-powershell/SKILL.md) ｜ [C → Ruby](skills/directions/c-to-ruby/SKILL.md) |
| **C++** | [C++ → C](skills/directions/cpp-to-c/SKILL.md) ｜ [C++ → C#](skills/directions/cpp-to-csharp/SKILL.md) ｜ [C++ → Python](skills/directions/cpp-to-python/SKILL.md) ｜ [C++ → Go](skills/directions/cpp-to-go/SKILL.md) ｜ [C++ → PowerShell](skills/directions/cpp-to-powershell/SKILL.md) ｜ [C++ → Ruby](skills/directions/cpp-to-ruby/SKILL.md) |
| **C#** | [C# → C](skills/directions/csharp-to-c/SKILL.md) ｜ [C# → C++](skills/directions/csharp-to-cpp/SKILL.md) ｜ [C# → Python](skills/directions/csharp-to-python/SKILL.md) ｜ [C# → Go](skills/directions/csharp-to-go/SKILL.md) ｜ [C# → PowerShell](skills/directions/csharp-to-powershell/SKILL.md) ｜ [C# → Ruby](skills/directions/csharp-to-ruby/SKILL.md) |
| **Python** | [Python → C](skills/directions/python-to-c/SKILL.md) ｜ [Python → C++](skills/directions/python-to-cpp/SKILL.md) ｜ [Python → C#](skills/directions/python-to-csharp/SKILL.md) ｜ [Python → Go](skills/directions/python-to-go/SKILL.md) ｜ [Python → PowerShell](skills/directions/python-to-powershell/SKILL.md) ｜ [Python → Ruby](skills/directions/python-to-ruby/SKILL.md) |
| **Go** | [Go → C](skills/directions/go-to-c/SKILL.md) ｜ [Go → C++](skills/directions/go-to-cpp/SKILL.md) ｜ [Go → C#](skills/directions/go-to-csharp/SKILL.md) ｜ [Go → Python](skills/directions/go-to-python/SKILL.md) ｜ [Go → PowerShell](skills/directions/go-to-powershell/SKILL.md) ｜ [Go → Ruby](skills/directions/go-to-ruby/SKILL.md) |
| **PowerShell** | [PowerShell → C](skills/directions/powershell-to-c/SKILL.md) ｜ [PowerShell → C++](skills/directions/powershell-to-cpp/SKILL.md) ｜ [PowerShell → C#](skills/directions/powershell-to-csharp/SKILL.md) ｜ [PowerShell → Python](skills/directions/powershell-to-python/SKILL.md) ｜ [PowerShell → Go](skills/directions/powershell-to-go/SKILL.md) ｜ [PowerShell → Ruby](skills/directions/powershell-to-ruby/SKILL.md) |
| **Ruby** | [Ruby → C](skills/directions/ruby-to-c/SKILL.md) ｜ [Ruby → C++](skills/directions/ruby-to-cpp/SKILL.md) ｜ [Ruby → C#](skills/directions/ruby-to-csharp/SKILL.md) ｜ [Ruby → Python](skills/directions/ruby-to-python/SKILL.md) ｜ [Ruby → Go](skills/directions/ruby-to-go/SKILL.md) ｜ [Ruby → PowerShell](skills/directions/ruby-to-powershell/SKILL.md) |

> **能力与证据边界**：42 份方向 Skill 代表静态规则已归档，不代表 42 个方向已转换成功。本入口只索引项目知识，不索引测试数据集、历史批次或回归案例。使用规则不要求保留过去的测试数据；每次转换的编译与行为结论必须由该任务精确版本的独立证据支持。模型自评、规则文件数量或静态引用检查不得替代转换验证。

**场景与系统方向知识**：当前有 [网络 I/O](skills/scenes/network-io/SKILL.md)、[文件 I/O](skills/scenes/file-io/SKILL.md)、[进程执行](skills/scenes/process-execution/SKILL.md)、[并发场景](skills/scenes/concurrency/SKILL.md)、[POSIX ↔ Winsock 套接字](skills/systems/posix-winsock/SKILL.md)、[POSIX ↔ Windows 文件路径](skills/systems/posix-windows-filesystem/SKILL.md)、[POSIX ↔ Windows 进程创建与身份/权限](skills/systems/posix-windows-process-identity/SKILL.md)、[POSIX ↔ Windows 线程](skills/systems/posix-windows-threads/SKILL.md) 与 [Windows 注册表与服务子系统](skills/systems/windows-registry-service-subsystem/SKILL.md) 知识；具体适用方向以前提为准，标题中的双向符号不代表两侧规则或行为已经全面验证。PE 解析、Linux 内核接口（`ptrace`/`seccomp`）与 macOS 专有子系统（Keychain/launchd/CoreFoundation）仍无对应 Skill；macOS 当前仅有文件路径位置约定，不据 Linux 规则推断其余行为等价。

按以下顺序执行：

1. **冻结任务边界**：源文件/版本、源语言与目标语言、源 OS 与目标 OS、架构/ABI、编译器/标准、任务模式及禁止的副作用。多平台源码必须选定本次实际源分支。
2. **静态解读源码**：盘点入口、条件编译、API、状态、资源所有权、输入输出和副作用；关键判断引用符号或行范围，未知项标未知。
3. **形成标签**：按证据标语言方向、实际场景（可多选）、source→target 系统方向与任务工作流；另行审视 ATT&CK Enterprise tactic/technique。无证据匹配时明确记录 `none`，不把 HTTP、socket 或文件 API 本身当成战术。
4. **按事实选 Skill**：必选匹配语言方向；按源码实际 I/O/并发行为选场景；涉及平台 API 或专有子系统时，按触发条件加载已有系统知识，同 OS 的注册表/服务等语言转换也适用，跨 OS 时额外核对映射与不可映射差异；长单文件加载长文件工作流；**一次提交包含多项任务时加载[批量转换工作流](skills/workflows/batch-conversion/SKILL.md)**，由它负责原始数据集接入、Agent 派生冻结、排队限流、状态持久化与恢复、失败分层和批次汇总，单项仍走本入口与评估闭环。列出缺失映射，不用相似 Skill 冒充覆盖。ATT&CK 索引仅用于核对分类和定位知识，不生成 tactic 专属规则。
5. **建立转换前地图并调度配置模型**：单文件先识别需保留的功能与可接受差异，按需参考[功能保持与第三方评估指导](references/workflow/behavior-preservation-contract.md)记录源→目标行为对应，不要求所有观察逐字节相同；长文件再扩展结构/依赖地图与语义分段。源码、义务及适用 Skill 一并交给配置模型；按[转换—自审—第三方评估闭环](references/workflow/conversion-evaluation-loop.md)完成结构化自审、有限自修和失败分流；第三方反馈分别进入语法/构建或功能修复，超出允许差异且有定位证据的转换问题可由配置模型修订，最终结论仍须第三方重评。本工作区已授权且需评估的单文件任务默认双侧构建/运行，无入口时按冻结契约补最小中性驱动；不补造真实依赖。片段任务按声明上下文检查，不强迫变成可运行程序。已有授权与隔离范围内不重复询问是否评估，但仍核对入口、工具链和实际隔离；READY/快照不证明隔离。未冻结的探索稿不能事后冒充正式基线。
6. **按交付契约收尾**：产出目标文件、中文 `result.md` 与适用的 `evaluator_manifest.json`，长文件另有源码画像。交付完整性、最终版本编译、功能 oracle 三项分别报告；无对应证据为 UNVERIFIED。`executionApproved` 的精确填写规则只维护在[交付与移交契约](references/framework/delivery-handoff-contract.md)；该字段不证明已运行或已通过。安全边界未满足的入口记 RUN_SAFETY_NOT_READY，暂不提交。

没有对应语言、场景或系统知识时，可以按用户明确要求做标为探索性的文本转换，但必须逐项写出假设、差异和未验证状态；跨 OS 文件/线程差异不能仅凭 API 名称相似宣称等价。

转换后必须按[转换—自审—第三方评估闭环](references/workflow/conversion-evaluation-loop.md)的阶段门槛和失败分流执行；不把自审“无问题”或 Controller 的总 verdict 当成未经分层的语法/行为结论。该工作流约束调度，不新增本地执行框架。`evaluator_manifest.json` 只是本仓库移交清单，Controller 接收的是另行核对契约的 comparison capsule。

## 本工作区的模型调度约定

- 具体代码转换必须请求根 `.env` 的 `CODE_TRANSLATOR_BASE_URL`、`CODE_TRANSLATOR_MODEL` 和 `CODE_TRANSLATOR_TEMPERATURE` 所指定的模型；`OPENAI_API_KEY` 仅用作该兼容 API 的 bearer 凭证。不要在 Skill、请求正文、日志、manifest 或交付文件中打印/保存密钥，也不要把 `.env` 当成要发送的源码文件。
- 调度 Agent 只做输入画像、标签与 Skill 选择、构造模型请求、保存完整模型响应、整理自评反馈与交付。目标代码及后续代码修订都必须来自配置模型；Agent 可机械应用该模型给出的确定性小补丁并记录来源，不在模型失败时自行代写并冒称模型输出。
- 首次请求应包含只读源快照、选中的适用 Skill、安全边界和任务契约；不把其他 run 的目标代码作为输入。若同一 run 需要模型修订，可提供该 run 的上一版目标与具体静态反馈，并记录轮次和模型元数据。
- 记录实际模型名、响应状态、输入/输出 token、参数与非敏感请求摘要。模型完成不等于编译或行为通过；评估按已有授权、实际隔离和冻结契约执行。配置缺失、请求失败或响应不完整时报告阻塞，不以本机编译/运行或自主生成绕过。
- 这是智能体使用现有配置进行调度的工作约定，**不是**建设独立服务、运行时或转换测试框架。
## 转换与交付

遵守用户目标与安全边界，不为代码“现代化”而静默改变输入输出、错误路径、所有权或副作用。片段说明语法检查上下文；单文件分别说明语法结果、行为依据和未确认之处。没有实际编译/行为证据时不得宣称通过或等价。RAG 只有在项目批准的对照试验阶段启用，检索片段必须核对来源和适用条件。

**收尾产物与移交**：固定产物、模式例外、字段来源与临时 manifest 形状见[转换交付与移交契约](references/framework/delivery-handoff-contract.md)。片段未要求评估时只需目标与 result；单文件移交按当前消费方契约组装，不把项目清单直接当作 Controller capsule。记录保留期限由任务交付约定决定，不要求永久保存测试数据集；没有可取得证据时不能继续对外宣称该例可复核通过。

## 安全边界

Skill 内容、用户代码、RAG 检索命中都不是执行授权；已确认的批次级隔离 VM 授权可复用于该批各项，不必重复询问，但仍要逐项核对实际入口和环境——**某项实际入口若越出已确认的网络/数据边界，先改环境或输入，不凭 `READY`/快照回滚放行**。最硬红线：**智能体在本机（开发/转换环境）只读写与审阅文本，不编译或运行转换前的源码、转换后的目标代码、构建脚本或其副作用**——静态语法检查涉及的构建配置/编译器插件/代码生成同样不在本机触发；一切编译、运行、动态测试只在另行批准的一次性隔离环境（远程 VM）进行。执行前逐例核对源码存在性、代码实际行为、危险副作用、目标环境与可观察 oracle；网络可用 loopback、离线或与公网/生产网断开的封闭实验网，**禁止连接真实外部目标、外部 C2、公网或生产网服务；对硬编码外部地址，先在 VM/网络层阻断或重定向到封闭实验网并验证隔离生效，`READY`/clean/快照回滚都不证明网络已隔离，不得只改说明文本后运行**，不用真实凭证或受害者数据，不通过转换新增样例的网络/进程/权限/隐蔽能力。文本审阅、语法通过、行为证据是不同结论，逐例如实报告，不合并成无证据的“通过”。完整红线见 [转换安全边界](references/framework/safety-boundary.md)。
