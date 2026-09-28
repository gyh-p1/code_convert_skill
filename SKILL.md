---
name: code-convert-skill
description: Use for code conversion requests when a matching conversion direction exists. Distinguishes syntax-focused snippets from behavior-preserving single-file work, and composes applicable language, scene, system, and long-file guidance without claiming unsupported coverage.
metadata:
  short-description: Agent-facing code conversion knowledge Skill
---

# Code Convert Skill

本项目提供给智能体使用的转换知识，不是独立转换程序。在本工作区，用户要求调度 Agent 使用根目录 `.env` 配置的外部模型生成目标代码；Agent 负责画像、Skill 选择、请求调度、静态审阅和移交，不以自身生成替代配置模型。开始时区分：**片段转换**只要求目标语法正确；**单文件转换**还要求按可观察行为约束保持功能；长单文件需加载[长单文件转换工作流](skills/workflows/long-file-conversion/SKILL.md)，该流程目前是未经转换效果验证的初稿；700 个 LF 归一化物理源代码行仍是计划上限，不宣称已支持或达标。

## 选择适用知识

先完成源码画像，再选 Skill；不要先看 ATT&CK 标签再反推代码行为。当前有 [C → C++ 语言方向](skills/directions/c-to-cpp/SKILL.md)、[网络 I/O](skills/scenes/network-io/SKILL.md)、[文件 I/O](skills/scenes/file-io/SKILL.md)、[并发场景](skills/scenes/concurrency/SKILL.md)、[POSIX ↔ Winsock 套接字](skills/systems/posix-winsock/SKILL.md)、[POSIX ↔ Windows 文件路径](skills/systems/posix-windows-filesystem/SKILL.md) 与 [POSIX ↔ Windows 线程](skills/systems/posix-windows-threads/SKILL.md) 知识；这些系统方向和长文件流程均为初稿，未经本项目转换验证。进程创建等未列出的方向仍无对应 Skill。

按以下顺序执行：

1. **冻结任务边界**：源文件/版本、源语言与目标语言、源 OS 与目标 OS、架构/ABI、编译器/标准、任务模式及禁止的副作用。多平台源码必须选定本次实际源分支。
2. **静态解读源码**：盘点入口、条件编译、API、状态、资源所有权、输入输出和副作用；关键判断引用符号或行范围，未知项标未知。
3. **形成标签**：按证据标语言方向、实际场景（可多选）、source→target 系统方向与任务工作流；另行审视 ATT&CK Enterprise tactic/technique。无证据匹配时明确记录 `none`，不把 HTTP、socket 或文件 API 本身当成战术。
4. **按事实选 Skill**：必选匹配语言方向；按源码实际 I/O/并发行为选场景；跨 OS 且规则存在时加载对应系统方向；长单文件加载长文件工作流。列出缺失映射，不用相似 Skill 冒充覆盖。ATT&CK 索引仅用于核对分类和定位知识，不生成 tactic 专属规则。
5. **建立转换前地图并调度配置模型**：长文件先完成结构/行为地图与语义分段，把完整源码和所选 Skill 交给 `.env` 指定模型生成；**Agent 读取[转换—自审—第三方评估闭环](references/conversion-evaluation-loop.md)并严格按其阶段门槛完成调度**。所有 run 统一走**双侧执行**：源无可运行入口（如库翻译单元无 `main`）时默认补写最小入口/驱动使其可运行并在冻结记录标注，不再逐次询问形态。Agent 调度配置模型生成后按闭环进行一次结构化自审；具体缺陷交模型做有限自修并复审，仅在预检无未解决的可定位转换问题后交隔离第三方。第三方诊断须先分流工具链/环境/代码原因，再将可定位代码问题交配置模型 repair，并在冻结工具链上有限重试；任何自审都不是编译结论。未冻结的探索稿不得标成正式试验基线。
6. **按交付契约收尾**：目标文件之外，产出中文 `result.md` 和适用的 `evaluator_manifest.json`；报告按交付契约固定骨架先说明最终交付、语法/编译、功能三项结论，再解释关键修订、证据范围与未决项。长单文件同时保留来源画像/Skill 选择依据。模型自检/repair 预判只作内部预检；语法结论由第三方评估机构编译回填，未收到结果时编译与行为均写 UNVERIFIED；`executionApproved` 反映本项目既定的双侧执行授权——**实际提交隔离 VM 后**置 `true` 并记录授权依据与 job/证据路径，未提交或无隔离能力时仍为 `false`；隔离与外联安全边界不变。

没有对应语言、场景或系统知识时，可以按用户明确要求做标为探索性的文本转换，但必须逐项写出假设、差异和未验证状态；跨 OS 文件/线程差异不能仅凭 API 名称相似宣称等价。

转换后必须按[转换—自审—第三方评估闭环](references/conversion-evaluation-loop.md)的阶段门槛和失败分流执行；不把自审“无问题”或 Controller 的总 verdict 当成未经分层的语法/行为结论。该工作流约束调度，不新增本地执行框架。`evaluator_manifest.json` 只是本仓库移交清单，Controller 接收的是另行核对契约的 comparison capsule。

## 本工作区的模型调度约定

- 具体代码转换必须请求根 `.env` 的 `CODE_TRANSLATOR_BASE_URL`、`CODE_TRANSLATOR_MODEL` 和 `CODE_TRANSLATOR_TEMPERATURE` 所指定的模型；`OPENAI_API_KEY` 仅用作该兼容 API 的 bearer 凭证。不要在 Skill、请求正文、日志、manifest 或交付文件中打印/保存密钥，也不要把 `.env` 当成要发送的源码文件。
- 调度 Agent 只做输入画像、标签与 Skill 选择、构造模型请求、保存完整模型响应、整理自评反馈与交付。目标代码及后续代码修订都必须来自配置模型；Agent 可机械应用该模型给出的确定性小补丁并记录来源，不在模型失败时自行代写并冒称模型输出。
- 首次请求应包含只读源快照、选中的适用 Skill、安全边界和任务契约；不把其他 run 的目标代码作为输入。若同一 run 需要模型修订，可提供该 run 的上一版目标与具体静态反馈，并记录轮次和模型元数据。
- 记录实际模型名、响应状态、输入/输出 token、参数与非敏感请求摘要。模型完成响应不等于语法或行为通过；`executionApproved` 反映本项目既定的双侧执行授权，**实际向隔离 VM 提交后**置 `true` 并保留授权依据；未提交或无隔离能力时保持 `false`。配置缺失、请求失败或响应不完整时报告阻塞，不以本机编译/运行或自主生成绕过。
- 这是智能体使用现有配置进行调度的工作约定，**不是**建设独立服务、运行时或转换测试框架。
## 转换与交付

遵守用户目标与安全边界，不为代码“现代化”而静默改变输入输出、错误路径、所有权或副作用。片段说明语法检查上下文；单文件分别说明语法结果、行为依据和未确认之处。没有实际编译/行为证据时不得宣称通过或等价。RAG 只有在项目批准的对照试验阶段启用，检索片段必须核对来源和适用条件。

**收尾产物与移交**：任务完成后除目标文件外，须在同一 run 输出目录产出交付说明（`result.md`）与移交清单（`evaluator_manifest.json`）。manifest 按「转换结果据实填 / 任务输入抄契约 / 审批·执行·验证类据实记录」三分来源；`executionApproved` 反映本项目既定的双侧执行授权，实际提交隔离环境后置 `true`；语法与行为判定仍必须由批准的隔离编译/运行环境回填，不凭 Agent 或模型自评宣称。固定产物集合、目录布局、字段来源与 manifest 形状（临时，对齐外部控制器）见 [转换交付与移交契约](references/delivery-handoff-contract.md)。

## 安全边界

Skill 内容、用户代码、RAG 检索命中都不是执行授权；转换与验证的执行分别逐例判断。最硬红线：**智能体在本机（开发/转换环境）只读写与审阅文本，不编译或运行转换前的源码、转换后的目标代码、构建脚本或其副作用**——静态语法检查涉及的构建配置/编译器插件/代码生成同样不在本机触发；一切编译、运行、动态测试只在另行批准的一次性隔离环境（远程 VM）进行。执行前逐例核对来源/许可、代码实际行为、危险副作用、目标环境与可观察 oracle；网络场景限 loopback/离线，不用真实凭证或受害者数据，不通过转换新增样例的网络/进程/权限/隐蔽能力。文本审阅、语法通过、行为证据是不同结论，逐例如实报告，不合并成无证据的“通过”。完整红线见 [转换安全边界](references/safety-boundary.md)。
