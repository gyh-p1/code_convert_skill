---
name: code-convert-skill
description: Use for code conversion with an existing language direction. Routes language, direction, scene, system and workflow knowledge, then applies manual per-item gates and layered delivery without claiming unverified coverage.
metadata:
  short-description: Agent-facing code conversion knowledge Skill
---

# Code Convert Skill

本项目提供 Agent 使用的 Markdown 转换知识，不是独立转换运行时。Agent 画像、选知识、手工调度根 .env 配置模型、静态审阅、提交与取证；目标代码及修订来自配置模型。执行约束见 [AGENTS.md](AGENTS.md)，红线只以[安全边界](references/framework/safety-boundary.md)为准；本机只读写文本，不承载或触发源码/目标/构建运行。

**指导与引导**：下方执行顺序、门禁和契约是必须遵守的指导，每步核前置条件与原件、实际行动后留证再推进；缺依据按对应停止/暂停路径处理。语言事实及方向/场景/系统知识用于引导映射选择，先核源码触发、版本与行为消费者，再选择适用正文。应保持的源行为和已冻结允许差异仍须严格遵守；“可选映射”、惯用 API 或示例不是无条件替换命令。存在冲突/关键语义未知时记录条目和影响，停止受影响请求，不强套规则、改行为或新增反复自审。加载及实际注入按任务状态 §2.3 分别留依据。

**知识按离线消费**：读取本仓库正文与本地参考，不依赖访问官方网页或下载资料。来源名称/版本只用于追溯；必要语义缺失或准确版本无法确定时，记录知识缺口，不要求联网补全后才能使用其余适用规则。维护规则见[Skill 编写规范 §5.1](docs/Skill编写规范.md#51-本地引用与网页资料)；知识读取不授权外部联网或执行。

片段以声明上下文的语法为范围，只引用用户或获批平台已提供的精确中性上下文并记录来源/版本；缺件待准备，不由 Agent/模型新造桩、入口或依赖。单文件保持约定可观察行为；长单文件加载专用工作流。700 个 LF 归一化物理源代码行是计划上限，长文件流程与全部方向尚无全面效果验证，不能据知识页数量宣称达标。

## 必经执行链与契约

```text
冻结（frozen-inputs.md 落盘并回读）→ 分类(ALLOWED) → 源侧预检（构建 + 适用运行基线）→ 生成 → 自审
  → 评估就绪核对（安全 + 驱动 + oracle）→ 提交 → 取证 → 先归因再分层报告
  → 交付完整性/终态门禁（记 DONE/PARTIAL 前）
```

1. 每项先按[任务状态 §2.2](references/framework/task-state-contract.md#22-冻结落盘门禁)写出并回读本 run 的 `01-frozen/frozen-inputs.md`，才能分类；缺失、空白、错项/错版本不得推进，不能等收尾补写。源预检、每次正式模型请求、提交/重提及恢复新增动作前再次核对；待准备条件按当前阶段处理。再取得 admissionStatus=ALLOWED 且 blockingReason=null，才能预检、正式模型生成或提交；不主观改判，不以文本交付绕过分类。
2. 源侧预检先取得 build.status=completed 且 exitCode=0；正常行为分支还须先取得冻结条件下的有效源运行基线。本轮无法合法评估行为但源可构建时，按[评估准备 §1.3](references/framework/evaluation-readiness-contract.md#13-lib_unobservable_compile_only-的转换与交付)记 LIB_UNOBSERVABLE_COMPILE_ONLY，继续转换、自审并验证目标语法/编译，不因缺 main、可执行文件、stdout 或合法入口直接跳过。源构建失败不消耗转换调用；源与目标证据分列，不把源 PASS 当目标 PASS。
3. 提交前核安全/独立授权/逐例隔离及评估范围；行为分支核合法驱动四要素、两侧对称和 oracle，LIB_UNOBSERVABLE_COMPILE_ONLY 核具体行为缺口与不运行的目标语法/编译命令。ALLOWED、READY、clean、快照不替代适用条件。
4. 开始处理该项就读取[统一收尾入口](references/framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)；正常结束、任何提前失败/阻断及暂停都必须走它。每项写 result.md 并逐件核实际适用产物、版本/内容/指针，将清单及核对结果留在报告，缺应有件不得记终态。未发生 job 不伪造；未知提交/活动或未确认清理的 job 保持 WAITING，即使已有暂停报告也不例外。DONE 可包含真实失败，PARTIAL 与 matched/mismatched 分开。

| 必读真源 | 负责什么 | 何时消费 |
|---|---|---|
| [任务状态契约](references/framework/task-state-contract.md) | 身份、冻结落盘门禁、版本关联/复用、接入去向、phase/lifecycle 与变体 | 冻结/分类前；源预检、每次模型请求、提交/重提及恢复/收尾 |
| [分类准入](references/workflow/classifier-agent-gate.md) | 分类输入、ALLOWED、重新分类与精确身份 | 冻结/分类前、源预检前及每次提交/重提 |
| [构建前提](references/workflow/build-prerequisites.md) | 冻结构建条件及真实源诊断分流 | 冻结前、源预检与目标评估 |
| [单项闭环](references/workflow/conversion-evaluation-loop.md) | 生成、自审、有限修复、取证分流 | 开始处理该项时；正式生成、自审/修订和证据判读前 |
| [评估准备契约](references/framework/evaluation-readiness-contract.md) | 源预检适用运行基线、驱动来源、四要素、oracle、仅编译、观察采信 | 冻结评估计划、源预检前、生成前及双侧提交/证据判读 |
| [交付契约](references/framework/delivery-handoff-contract.md) | 统一收尾入口、全去向 result.md、适用件核对、目录及移交清单 | 开始处理每项时必读；结束/失败/阻断/暂停前再次核对 |
| [安全边界](references/framework/safety-boundary.md) | 本机/同机/VM、网络和数据红线 | 全程 |

[行为指导](references/workflow/behavior-preservation-contract.md)用于单文件目标/允许差异说明，不自设裁决标准；其旧门禁章节仅转引评估准备契约。[Controller 适配](references/adapter/controller/remote-controller-adapter.md)只在使用该渠道时加载，维护外部字段与命令；它和开发阶段文档不产生执行授权。

## 选择适用知识

先按源码事实画像再选知识，不由 ATT&CK 标签反推行为。[知识总索引](references/README.md)说明各层消费者与边界。

**语言事实**：每项必读源、目标两页，由[七语言共性语义索引](skills/references/seven-language-common-semantics.md)导航；“按需”只用于选择适用规则和正文注入范围，不能省掉任一语言页。基线为 C11、C++17、C# 12/.NET 8、CPython 3.12、Go 1.27、PowerShell 7.6、Ruby 3.4；实际工具链仍须证据核验。

**语言方向（42 个）**：每项选择一个源→目标方向。方向只维护映射，语言内事实不在 42 页重复。

| 源语言 | 目标语言方向 Skill |
|---|---|
| **C** | [C → C++](skills/directions/c-to-cpp/SKILL.md) ｜ [C → C#](skills/directions/c-to-csharp/SKILL.md) ｜ [C → Python](skills/directions/c-to-python/SKILL.md) ｜ [C → Go](skills/directions/c-to-go/SKILL.md) ｜ [C → PowerShell](skills/directions/c-to-powershell/SKILL.md) ｜ [C → Ruby](skills/directions/c-to-ruby/SKILL.md) |
| **C++** | [C++ → C](skills/directions/cpp-to-c/SKILL.md) ｜ [C++ → C#](skills/directions/cpp-to-csharp/SKILL.md) ｜ [C++ → Python](skills/directions/cpp-to-python/SKILL.md) ｜ [C++ → Go](skills/directions/cpp-to-go/SKILL.md) ｜ [C++ → PowerShell](skills/directions/cpp-to-powershell/SKILL.md) ｜ [C++ → Ruby](skills/directions/cpp-to-ruby/SKILL.md) |
| **C#** | [C# → C](skills/directions/csharp-to-c/SKILL.md) ｜ [C# → C++](skills/directions/csharp-to-cpp/SKILL.md) ｜ [C# → Python](skills/directions/csharp-to-python/SKILL.md) ｜ [C# → Go](skills/directions/csharp-to-go/SKILL.md) ｜ [C# → PowerShell](skills/directions/csharp-to-powershell/SKILL.md) ｜ [C# → Ruby](skills/directions/csharp-to-ruby/SKILL.md) |
| **Python** | [Python → C](skills/directions/python-to-c/SKILL.md) ｜ [Python → C++](skills/directions/python-to-cpp/SKILL.md) ｜ [Python → C#](skills/directions/python-to-csharp/SKILL.md) ｜ [Python → Go](skills/directions/python-to-go/SKILL.md) ｜ [Python → PowerShell](skills/directions/python-to-powershell/SKILL.md) ｜ [Python → Ruby](skills/directions/python-to-ruby/SKILL.md) |
| **Go** | [Go → C](skills/directions/go-to-c/SKILL.md) ｜ [Go → C++](skills/directions/go-to-cpp/SKILL.md) ｜ [Go → C#](skills/directions/go-to-csharp/SKILL.md) ｜ [Go → Python](skills/directions/go-to-python/SKILL.md) ｜ [Go → PowerShell](skills/directions/go-to-powershell/SKILL.md) ｜ [Go → Ruby](skills/directions/go-to-ruby/SKILL.md) |
| **PowerShell** | [PowerShell → C](skills/directions/powershell-to-c/SKILL.md) ｜ [PowerShell → C++](skills/directions/powershell-to-cpp/SKILL.md) ｜ [PowerShell → C#](skills/directions/powershell-to-csharp/SKILL.md) ｜ [PowerShell → Python](skills/directions/powershell-to-python/SKILL.md) ｜ [PowerShell → Go](skills/directions/powershell-to-go/SKILL.md) ｜ [PowerShell → Ruby](skills/directions/powershell-to-ruby/SKILL.md) |
| **Ruby** | [Ruby → C](skills/directions/ruby-to-c/SKILL.md) ｜ [Ruby → C++](skills/directions/ruby-to-cpp/SKILL.md) ｜ [Ruby → C#](skills/directions/ruby-to-csharp/SKILL.md) ｜ [Ruby → Python](skills/directions/ruby-to-python/SKILL.md) ｜ [Ruby → PowerShell](skills/directions/ruby-to-powershell/SKILL.md) ｜ [Ruby → Go](skills/directions/ruby-to-go/SKILL.md) |

**场景（按行为多选）**：[网络 I/O](skills/scenes/network-io/SKILL.md)、[文件 I/O](skills/scenes/file-io/SKILL.md)、[进程执行](skills/scenes/process-execution/SKILL.md)、[并发](skills/scenes/concurrency/SKILL.md)。场景维护跨语言行为义务，不承载普通单线程控制流或单一语言 API 改写表。

**系统（按实际 API/子系统多选）**：[POSIX ↔ Winsock](skills/systems/posix-winsock/SKILL.md)、[文件路径](skills/systems/posix-windows-filesystem/SKILL.md)、[进程创建/身份权限](skills/systems/posix-windows-process-identity/SKILL.md)、[线程](skills/systems/posix-windows-threads/SKILL.md)、[Windows 注册表/服务](skills/systems/windows-registry-service-subsystem/SKILL.md)。同 OS 的专有子系统也适用；双向标题不证明全面映射或验证。macOS 当前只含文件位置约定；PE、ptrace/seccomp、Keychain/launchd/CoreFoundation 无对应系统 Skill。

**工作流**：[长单文件](skills/workflows/long-file-conversion/SKILL.md)按复杂度/长度加载；[批量](skills/workflows/batch-conversion/SKILL.md)按任务集合加载，两者可同时使用。批量只手工串行，整批一个 batchId，每新增 40 项 DONE+PARTIAL 增量对账并带入遗留项，缺档立即停新增转换，关闭前终局核对。

[ATT&CK 战术索引](skills/attack-tactic-index/SKILL.md)仅核对标签与定位知识，不生成战术规则，不参与授权；无证据记 none。HTTP/socket/文件 API 本身不构成战术。

**跨场景安全语义**：源码有网络、文件、认证或边界校验行为时，读取[安全行为共性](skills/references/security-behavior.md)的适用正文；它维护源防护语义，不替代执行安全边界。

## 按以下顺序执行

以下六步适用于每个实际处理项，不能替代上方门禁链。先完成第 1–4 步的准备与知识选择，再记 FROZEN；第 5 步严格按下方调度表逐行推进，不把整段概述当成一次操作。任一步停止均转第 6 步。从方向/场景/系统页直接进入时，也须先返回本入口完成必读加载，不能只读映射页开始生成。

1. **确认边界与加载必读规则**：开始处理每项即依次读取任务状态、安全边界、交付契约（先落实 §1.1 的报告落点，再读适用布局）、分类准入、构建前提、评估准备、单项闭环；表中的消费时点还要求后续在相应阶段再次核对。请求含多项时，在处理首项前加载批量工作流；长/复杂单文件在建立地图和分段前加载长文件工作流；二者可同时使用。使用 Controller 时，冻结提交/比较计划前读其适配、能力矩阵、比较策略及[当前协议适配](references/adapter/controller/platform-revision-adapter.md)，按当前协议选择接口、报告、原件与收尾规则，并核实际平台身份与能力；版本不符或支持未知先记准备缺口。确定本项身份、模式、报告与冻结落点，先记录准备草稿，未完成第 2–4 步不记 FROZEN。变更已冻结条件另记变体，版本关联按任务状态 §2.1。
2. **静态画像**：盘入口、条件编译、API、状态、所有权、输入输出和副作用；参数计数/下标/消费范围、文本或字节单位、固定常量、控制流出口、进程替换/环境、枚举消费者、键或行输入、空白谓词与临时目录选择按实际使用点定位。引用符号/位置，未知标未知，不执行样本。
3. **形成标签**：语言方向、实际场景、系统与工作流按证据标；ATT&CK 单独核对，不由标签决定转换。
4. **加载知识并完成冻结**：先读共性索引与源/目标两语言页，再读一个方向 Skill；按源码触发读场景、系统、安全行为及方向随附专题。按[易错语义导航](skills/references/seven-language-common-semantics.md#易错语义导航)将参数、字节/换行、常量、作用域、文件失败、进程/环境、枚举、键输入、空白和临时目录对应到实际正文；枚举/键输入不依赖进程/并发，原生 fork/exec 同 OS 也加载适用系统事实。记录“源符号/范围→规则路径/章节/精确版本→适用理由”，缺映射写缺口/探索假设。此步只准备非敏感请求材料，不发送模型请求；将确定的身份/源集合、模式、模型/知识、构建/评估/授权计划写入本 run 的 `01-frozen/frozen-inputs.md`，按[任务状态 §2.2](references/framework/task-state-contract.md#22-冻结落盘门禁)回读后才记 FROZEN。各组字段按模式记录，不适用有理由、未知写待准备；当前动作所需条件另核，不能因记录齐而视为就绪。
5. **调度配置模型及适用评估**：先回读冻结并分类 ALLOWED；源预检、每次模型请求和提交/重提前再核冻结。按评估准备 §1.1/§1.3 分支：能合法评估行为的先取源 build completed/0 与有效运行基线，再生成、自审和有限修复；本轮缺合法入口/观察条件或无安全观察方式但源 build completed/0 的，冻结 LIB_UNOBSERVABLE_COMPILE_ONLY，继续生成、自审及目标语法/编译验证，行为未评估/UNVERIFIED、PARTIAL。库可沿用单文件模式，不补 main、改源包名或造驱动；不因暂缺目标验证能力反向跳过生成，未取得目标证据据实 UNVERIFIED。实际运行失败先归因，不借分支抹掉失败。每次双侧提交核适用准备及安全，仅编译不运行、不造 comparison；正常行为取证按评估准备 §4–5 核真实观察，先归因再报告/修复。
6. **统一收尾或暂停**：前述任一步骤停止都跳转[交付契约 §1.1](references/framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)，成功/失败/非可转换/WAITING 均写 result.md。逐件回读适用产物，记录已取得/缺失/不适用、路径/版本、原因与核对结果；交付、编译、功能及安全分别报告，无证据 UNVERIFIED。缺应有件不得终态；未知提交/活动或未确认清理保持 WAITING，暂停报告不等于已收尾。批次逐项核对，40 项与终局对账另做；带遗留及真实补登依据，按同快照汇总，不用总 verdict 或条数证明成功。

比较与统计统一消费[评估准备§5.1](references/framework/evaluation-readiness-contract.md#51-有效性消噪与功能分类的次序)：先核有效观察，再按冻结允许差异宽泛消噪，最后功能分类；有效matched与有效semantic_pass均可计本冻结范围功能比较通过，仍分列两类、策略/覆盖及交付/编译/安全，不外推普遍等价或合成全批转换成功率。映射知识是选择引导，不增加自审轮次或动态验证步骤。

### 第 5 步的单项调度顺序

下表只展开既有门禁及消费时点，不新增平台接口。所有动作手工逐项执行；每次正式模型请求和新提交仍先回读冻结文件。按[任务状态 §2.4](references/framework/task-state-contract.md#24-有依据的阶段推进)核前置原件、保存真实动作结果再记 phase，不能按计划宣布阶段通过。涉及外部动作前核对应授权，原授权适用时直接沿用。

| 顺序 | 调度前读什么、做什么 | 允许继续的依据；不足时的去向 |
|---|---|---|
| 5.1 分类 | 分类准入 §1–3；检查已落盘冻结及完整源树，手工准备分类输入，在获准临时目录调用登记分类器并保存原文 | 本项身份/源集合匹配且 ALLOWED/null；缺件不调用，BLOCKED/损坏结果不预检、不生成，转第 6 步 |
| 5.2 源预检与分支 | 评估准备 §1.1/§1.3，并逐项落实[§1.4 核对清单](references/framework/evaluation-readiness-contract.md#14-源预检采信与双侧对齐核对)；读构建前提和渠道适配，核支持形态、安全/授权/隔离及精确源构建；先辨本轮合法行为入口/观察条件 | 源 build completed/0 和适用清理是必需；正常行为分支还需有效源基线；本轮行为无法评估则记录 LIB_UNOBSERVABLE_COMPILE_ONLY 继续生成。不造目标凑源预检，源构建未过不生成 |
| 5.3 正式生成 | 单项闭环 §2；回读冻结/源预检原件，核配置模型调用协议和脱敏请求正文、源范围、适用知识与行为义务 | 生成前条件均适用且响应完整、来源与目标版本可回读；实际发送后才记知识已注入。失败/截断按有限重试留原文，仍失败转第 6 步 |
| 5.4 自审与有限修订 | 单项闭环 §2/§4；独立请求审当前目标，提供源/目标及适用知识正文，逐条归因 | 覆盖/必要记录完整且无未解决可定位转换问题；有限有效 NO-REPAIR-IDENTIFIED 可推进，不反复求保证。有依据的转换问题由配置模型有限修订，新稿关联父版本并复审 |
| 5.5 评估就绪与提交 | 评估准备 §1–4（按 §1.4 回读源原件并对齐目标条件）、分类准入 §3及渠道适配；核精确版本、安全/授权/隔离及范围；行为分支核驱动/对称/oracle，LIB 核不运行命令；先保存本 attempt 精确材料与适用 submissionId，再 POST | 适用条件通过才提交并保留 HTTP 状态/body/传输诊断；LIB 只验目标语法/编译。支持未知只停该验证，交已有目标并记 UNVERIFIED，不伪造 job，不盲重投 |
| 5.6 回执、轮询与取证 | 渠道适配；取得 jobId 后查原 job，终态后手工逐件取真实报告、各适用侧 evidence、comparison/logs及清理依据 | 无回执且可能已接收则 WAITING/SUBMISSION_UNKNOWN，不盲重投；不适用/未返回件不伪造，中途快照不作最终证据 |
| 5.7 归因、必要修复或收尾 | 评估准备 §5（含 §5.1 消噪/分类及[§5.2 统计单位](references/framework/evaluation-readiness-contract.md#52-功能比较统计的集合与单位)）、单项闭环 §3；按分支回读精确版本原件。正常行为分支核两侧原始观察，LIB 分支核源构建与目标语法/编译，不要求运行观察或 comparison | 只将可定位转换引入问题交配置模型有限修复；新稿重核自审/准备并取得新证据，不借旧稿 PASS。停止或无修复需求均转第 6 步 |

纯文档审阅/架构优化不属于代码转换，不触发分类、模型转换、构建或运行。明确文本交付不触发后续行为 job，但正式目标代码生成仍须生成前门禁。无对应知识的探索转换保留假设、差异和未验证范围。

自审裸 JSON 与格式恢复、请求/修复计数见单项闭环 §2/§4，保留原文且不追加无限审阅。恢复时先核源基线适用性及未知提交；批次 40 项阈值按此前未计入的唯一终态 taskId，PARTIAL 恢复、复审和重提不重复计项，统计单位与快照按批量工作流 §4.1/§6。

## 本工作区的模型调度约定

- 使用根 .env 的 CODE_TRANSLATOR_BASE_URL、CODE_TRANSLATOR_MODEL、CODE_TRANSLATOR_TEMPERATURE，OPENAI_API_KEY 仅作 bearer 凭证；不将 .env 或密钥发送/写入提示、日志、清单与产物。
- 首次请求包含当前只读源快照、冻结契约、实际适用知识正文和安全义务；不以标题/路径替代内容，不引用其他 run 的目标。修订提供同 run 父版本与定位反馈。
- 调用前核配置服务实际采用的请求路径/协议、正文形状、响应与错误封装及调用工具可用性，记录非敏感依据；BASE_URL/模型名本身不能证明协议。缺少依据记 PREPARATION_GAP，先补调用契约，不猜端点、不写请求封装脚本。请求正文由 Agent 手工组织，实际发送只在第 5 步门禁通过后发生。
- 目标及修订必须来自配置模型；Agent 仅机械应用其确定性补丁并核对父版本、保存来源，不在模型失败时自主代写。
- 保存完整脱敏请求/原始响应的关联记录、实际模型名、状态、参数、token、输入/输出哈希及失败 attempt。模型完成不是编译或行为通过。
- 请求不发送 max_tokens；截断先按闭环响应完整性/分块协议处理，仍计用量，不据截断擅自换模型。配置缺失、请求失败或不完整时如实阻断。
- 全程用原生工具手工单项操作，不写可复用或临时辅助脚本。唯一许可常驻脚本是登记钉 SHA 的分类器，且仅按准入页在获准外部临时目录调用。
