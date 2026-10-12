# 2026-10-12：转换 Skill 的指导与引导静态演练

本轮按一个新进入工作区的 Agent 视角，沿发现入口、必读契约、适用知识、冻结、调度和收尾逐步推演，并修正发现的冲突。判断分两个维度：**指导**要求动作有前置条件、真实证据和停止出口；**引导**要求知识按源事实触发，候选写法不能误导模型改变源行为。

结论：本轮覆盖的加载路径和分支可以据文本判定下一动作、禁止动作和应留证据；发现的流程冲突与具体语义误导已修正。**这是静态演练，不证明任意 Agent 一定遵守，也不证明模型正确应用了全部知识。** Markdown 门禁仍需 Agent 实际回读和执行记录；没有新增自动检查器、辅助脚本或平台校验。

## 1. 范围与版本

- 审阅对象是当前工作区，包含前轮尚未提交的 LIB_UNOBSERVABLE_COMPILE_ONLY 调整；本报告不描述已部署转换 Agent 的加载状态。记录时 HEAD 为 `016af0e`，工作区内容与 HEAD 不同。
- 穷举 `skills/**/SKILL.md` 得到 54 页：42 个方向、4 个场景、5 个系统、1 个战术索引、2 个工作流。加发现入口、AGENTS.md、根入口，回查 57 个入口/路由节点；共享参考 9 页，方向随附参考当前为 c-to-cpp 的 2 页。
- 对上述节点核入口前置、源/目标语言选择、场景/系统触发与回根路径；主干核冻结、源预检、知识消费、模型调用、自审、评估、取证、恢复、收尾与对账。涉及改动的条目人工核目标标题/相对路径和上下游口径，代码样例不是链接检查对象。
- 语义精读和资料核对重点为 Go→PowerShell、C#→C、C#→PowerShell、Python→C，以及 Go/PowerShell 共享语言事实；其他方向做入口与相关措辞回查，**未完成全部 42 方向每条技术规则的事实复核**，不能宣布全库无误导或全部方向效果达标。
- 本轮只读写 Markdown 和使用原生只读命令。未运行分类器、配置转换模型、Controller 请求、源码/目标、语法解析或编译；未读写 Controller 安装目录。未编写审计/转换辅助脚本，未提交或推送。

关键正文 SHA256（本轮修订后原生单文件哈希）：

| 文件 | SHA256 |
|---|---|
| 根 SKILL.md | `4FA15D234C5EFBB90E72590F545F635A8E6AB4E45799A50FE4FDBECD6CA169A4` |
| evaluation-readiness-contract.md | `89A64E1BB3664DC24BDEAA67143A5F773DF0CCFF0716A490A675EA8E78762C68` |
| task-state-contract.md | `D50D4D91E90BF160D30970993ABDFDCBFB3FE938DB530F743EF8B36BBB3C0A0D` |

## 2. 模拟实际加载顺序

AGENTS.md 开头要求转换任务先读发现入口；发现入口再指向 AGENTS.md 与根入口。这是交叉引用，不要求反复读同一精确版本；接着按根入口的第 1–6 步推进，不能只看到链接或摘要就宣布全部正文已读。

| 时点 | Agent 应读什么 | 读后的确定动作与边界 |
|---|---|---|
| 进入任务 | `.agents/skills/code-convert/SKILL.md`、AGENTS.md、根 SKILL.md | 确认手工单项、模型来源、执行边界与统一收尾；纯文档审阅不触发转换动态步骤 |
| 根第 1 步 | 任务状态→安全边界→交付→分类准入→构建前提→评估准备→单项闭环 | 确定身份、run/报告落点及当前未知条件；不是直接生成 |
| 适用工作流 | 多项请求先读批量；长/复杂文件在地图/分段前读长文件；可同时加载 | 地图/分段是准备，不是绕过分类/源预检的模型授权 |
| Controller 渠道 | 渠道适配、能力矩阵、比较策略、当前协议适配 | 核当前实例和请求/报告形态；历史部署 READY 不证明本项隔离或工具链满足 |
| 根第 2–3 步 | 精确只读源及用户契约 | 按符号/使用点画像、形成方向/场景/系统标签；静态阅读不定案源不可构建 |
| 根第 4 步 | 共性索引→源语言页→目标语言页→一个方向；实际触发的场景/系统/安全行为/专题 | 两语言页必读；“按需”决定条目适用/注入范围，不能省读目标页，也不把无触发条目变成本轮义务 |
| 冻结完成 | 本 run 的 `01-frozen/frozen-inputs.md` | 写出后实际回读身份、精确源集合、哈希和适用字段；准备未知与就绪分别记录 |
| 根第 5 步 | 依下表逐步重核相应真源与原件 | 每个动作前核条件，动作后保存实际结果，再记阶段；不能把准备/已请求记作完成 |
| 根第 6 步 | 交付 §1.1、实际适用产物、任务状态、批量对账条件 | 任何正常结束、失败、阻断和暂停均写报告；收尾不反向补成前置门禁已过 |

直接进入任一方向、场景或系统页时，其开头要求先回根入口完成必读加载；战术索引不能单独推进转换。当前 42 个方向均列两语言页，9 个场景/系统页均有加载前置；两工作流仍消费根门禁。本轮未发现入口回链缺失，不能把这项结果扩展为全部正文正确。

## 3. 逐步调度的依据

本表是演练核对，不替代产品真源：[根调度表](../../../SKILL.md)、[任务状态 §2.2–2.4](../../../references/framework/task-state-contract.md)、[评估准备](../../../references/framework/evaluation-readiness-contract.md)、[单项闭环](../../../references/workflow/conversion-evaluation-loop.md)、[统一收尾](../../../references/framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)。

| 步骤 | 前置核对与动作 | 可支持继续的真实依据 | 不满足时 |
|---|---|---|---|
| 冻结 | 手工完成本项本 run 记录并回读；不批量冻结 | 有实质内容、身份/方向/源集合/版本匹配，当前动作的适用条件可核 | 停新增动作并按实际阶段报告；既有 job 查询/取证/终止不因此延误 |
| 5.1 分类 | 只在获准临时目录按登记版本分类完整源树，保存输入与原结果 | 精确源集合对应 ALLOWED、blockingReason=null | BLOCKED、缺失、损坏或失效不预检/生成/提交，不手改裁决 |
| 5.2 源预检 | 核实际源命令/工作目录/输入集合、工具链、授权隔离；按分支执行适用预检 | exact source build completed/0 及清理；正常行为分支另有有效源运行基线 | 源构建失败不调用转换；行为入口/观察缺口可按 §1.3 转 LIB，源声明/依赖或实现契约缺失仍停 |
| 5.3 生成 | 再回读冻结/源原件，核配置调用协议；手工准备实际源、契约和适用知识正文 | 实际脱敏请求、原响应、完整目标、实际模型/参数/用量及版本关联 | 空/截断/传输/解析失败保留原文；同冻结请求有限重试，仍失败部分交付，不代写目标 |
| 5.4 自审 | 配置模型对照当前源/目标/契约/知识审阅，Agent 定位和归因 | 必要记录和覆盖完整，无未解决可定位转换问题；有效 NO-REPAIR-IDENTIFIED 可推进 | 不反复求保证；有据的转换问题有限修订，源已有/环境/未定差异不盲修 |
| 5.5 准备与提交 | 核版本、安全/授权/隔离；行为分支核驱动四要素/对称/oracle，LIB 核不运行的目标解析/编译；POST 前保存精确 attempt/材料/适用恢复标识 | 当前接口确实支持适用形态，真实 HTTP 状态/body/传输诊断和回执分列 | 条件未知不试投；LIB 目标验证缺支持不反向阻止生成；可能已接收却无回执记 WAITING，禁止盲重投 |
| 5.6 轮询取证 | 逐条查原 job，按协议核终态、closure 与真实清理；把原件实际落盘 | 本 job/输入/源/目标版本对应的适用报告、evidence/logs；行为含真实观察/comparison | 中途快照不作结论；LIB 不要求不存在的 comparison；清理/接收/活动未知保持 WAITING |
| 5.7 判读修复 | 回读各适用侧 build/观察，先归因，再决定配置模型修订或收尾 | 具体源/目标定位与第三方证据支持转换引入问题；新稿有独立证据 | 总 FAIL、自审建议或环境差异不够；旧稿 PASS 不借给新稿；预算耗尽保留当前稿与未决项 |
| 第 6 步 | 每项 result.md，逐件读适用产物并记路径、版本、缺失/不适用及原因 | 报告/目标/已发生过程原件与核对结果齐备，无未决执行；状态与功能分列 | 缺应有件不得终态；暂停报告不解除 WAITING；LIB 为 PARTIAL、功能 UNVERIFIED |

自修与评估后修复默认各最多两轮，后者语法/行为/mixed 共用总预算；长文件整项累计，另开 run、分段、换反馈不重置。自审的 reviewN、模型传输 attempt、代码修复轮次和 job 不混作同一个计数。

## 4. 用 D2-202 推演分支

模拟输入仅取用户贴出的报告：Go stdlib strconv/itoa，179 行，非 main；报告宣称源 build completed/0、自包含、清理完成。本仓库未取得该源快照及原预检原件，**这些是本次条件假设，未独立核验**。不能由本报告替 D2-202 新增 ALLOWED、冻结、目标或 job。

1. 若实际源与契约确认是整数转字符串库，读 Go/PowerShell 两语言页和 go-to-powershell。重点为整数宽度、负值/边界、基数、缓冲/字符串和错误；没有实际 struct/管道、I/O、异步使用点，就不把相关候选规则注入为义务。Go→PowerShell 标题本身不能强迫返回 PSCustomObject。
2. 先核有没有**合法现成的**调用入口、输入与观察条件。没有 main/stdout 不等于没有函数行为；本轮缺合法入口则可冻结 LIB_UNOBSERVABLE_COMPILE_ONLY，不造 main、不改源包名、不造驱动。
3. 若原 run 已冻结为不同范围，保留历史并另记关联变体，使用 `<case>/output/<batchId>/runs/<runId>/`；同源旧构建是否可复用须核命令、实际输入、工具链与适用条件，不能只看摘要。范围变化不增加 taskId 数、不重置预算。
4. 回读新冻结→核分类当前适用→核精确源 build completed/0 与清理。这里要检查命令确实构建冻结的 itoa.go，而非机器上的另一个 strconv 包；缺 main 不要求链接可执行。
5. 满足上述条件后由配置模型转换完整库接口及行为，自审；仅编译改变评估范围，不授权删除函数、简化错误或改变整数算法。
6. 目标 PowerShell 在获批隔离 VM 按实际支持的“不执行脚本”的语法解析形态验证。普通执行脚本不能冒充解析；目标证据与源 build 分列。若平台暂缺该能力，先交完整模型目标，目标语法 UNVERIFIED、待补验证。
7. result.md 记录“已转换；目标语法/编译据实；行为未评估/UNVERIFIED”，适用件齐备且无未决执行才 PARTIAL。不能因比较空输出 matched 写功能通过；未实际生成时也不能只改标签宣布已转换。

因此，在这些假设经过真实核对后，D2-202 的推进出口是 **LIB 转换分支**；原来的“非 main ⇒ PREPARATION_GAP ⇒ 不生成”不足以成立。这份演练只证明新文本的决策路径，不重判历史 job 或代替实际转换。

## 5. 另外两种流程

**正常行为项**：合法入口和观察条件齐备，先冻结/classify，再取得源 build 与有效源基线、清理，然后生成/自审、核双侧驱动/oracle、提交取原件、归因。服务须等待观察状态并最终终止，不能“启动后等退出”；源预期错误路径可非零，空输出也须看是否符合冻结观察目标。已有合法路径不能为省事改 LIB；真实行为差异不能改成“未评估”来躲 FAIL。

**批量中的长文件项**：首项前加载批量，当前长项地图/分段前加载长文件；冻一项推进一项，完整源预检不由片段预检替代。各单元依赖/请求/目标版本可追，完整组装与适用审阅齐备才能提交。每新增 40 个此前未计入的唯一终态 taskId（DONE+PARTIAL）追加对账、带入遗留，缺档停新增；最后不足 40 项也在关闭前核。恢复、复审、重提、新 run 不重复充作新任务。

## 6. 本轮发现与修正

| 发现 | 影响 | 本轮处理 |
|---|---|---|
| 平台适配残留“任何缺口不消耗转换调用” | 把行为观察缺口当整个转换停止，与新 LIB 范围冲突 | 区分源 build 必需、正常行为基线必需与 LIB 可生成；源/目标证据分别报告 |
| 阶段表隐含“按计划推进”；局部 §1.1/§1.3 引用未指明评估准备 | 容易把请求动作当阶段完成，或找错章节 | 任务状态新增 §2.4 并由根调度消费；章节写明真源；EVALUATED 按适用原件与真实清理核，不要求 LIB 的不存在 comparison |
| 已冻条件变更要求新 run，但固定 batch 输出骨架缺变体落点 | 容易覆盖历史冻结/目标/报告 | 在现有交付骨架明确 runs/runId、父版本和当前指针，repair/retry 不重复开 run |
| POST 示例仅打印 JSON/带 --fail，HTTP/传输/回执未分列 | 错误 body 易丢，exit 0 易被当接收，未知提交易盲重试 | 示例保存 body 与 HTTP 状态；先记精确 attempt/适用 submissionId，原生错误/退出另存；GET 实际原件落盘并核身份。示例本轮未向服务试发 |
| 源 build PASS 未强调真实源覆盖；Go 表把 go.mod 当所有 build 必需 | 构建另一个同名包可被误作本源成功，合法文件构建形态被误阻断 | 核冻结命令/目录/文件覆盖、条件分支与实际诊断；模块/目录/具名文件依实际模式，不编造模块/依赖 |
| GO-PS-01 把对象返回当所有转换义务、禁 JSON/统一 PascalCase | 改源返回形态、JSON 文本与键名 | 候选对象映射只用于已冻对象边界；保留文本/字节/JSON 契约、集合形状、大小写和输出来源 |
| GO-PS-05 宣称 Runspace 不共享对象/每项新上下文，笼统排序 | 引导错误同步模型、破坏任务索引顺序 | 区分变量赋值与引用对象、池复用与全新上下文；按原索引恢复，不能按结果值替代；触发即读并发场景 |
| C#→C 与 C#→PowerShell 把阻塞/降级当普通 async 候选，超时等待混作取消 | 改调用者继续执行、完成/错误/取消与清理时机 | 标题及正文强调源完成语义；阻塞须源依据或用户允许，Wait-Job 超时不自动停止作业，缺条件不能仅“注明降级” |
| Python→C 默认用数组缓存生成器 | 改惰性求值、部分消费、副作用、异常与无限序列行为 | 保留求值时机/迭代状态，预计算须明确源依据或允许差异；补生成器章节来源 |
| Go/PowerShell 共享页有整数宽度、格式化、参数位置和转换事实误述 | 所有消费对应语言页的方向可能被误导 | 修正 int32/int 宽度假设、%d 与值域、普通 %v/%g 与精度、PS 默认位置绑定、数值 cast 非通用模回绕、插值与 ToString 文化边界 |
| “可选/近似/惯用”没有统一消费边界 | 已读/注入仍可能把候选当强制替换 | 任务状态 §2.3 明确源使用点→前提→范围再注入，事实/候选/允许差异分开；Skill 编写规范补指导/引导要求 |

这些语义修订的资料核对使用官方文档，只用于本轮维护溯源；必要语义已写回本地页，转换消费者不需要联网：

- PowerShell success 输出与集合展开、Go JSON 字段/tag 分别约束返回形态与序列化边界。[about_Return](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_return?view=powershell-7.6)、[encoding/json Marshal](https://pkg.go.dev/encoding/json#Marshal)。
- PowerShell 7.1 起默认复用并行 Runspace，7.6 可传引用对象，修改共享状态需线程安全；输出到达顺序不能替代源任务身份。[ForEach-Object](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/foreach-object?view=powershell-7.6)。
- C# await 未完成 Task 与已完成 Task 的等待路径不同；同步取值不是无条件等价。[Task asynchronous programming model](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/task-asynchronous-programming-model)。Wait-Job 超时只结束等待，任务仍可继续。[Wait-Job](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/wait-job?view=powershell-7.6)。
- Python 生成器主体延后求值，最左 iterable 则在建立生成器时求值，不能一概立即缓存。[Python 3.12 expressions §6.2.8](https://docs.python.org/3.12/reference/expressions.html#generator-expressions)。
- Go build 的文件/包/模块形态需与输入和实际工具链相符；non-main 构建不要求产出可执行文件。[cmd/go build](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies)。
- 普通浮点 %v 使用 %g；FormatFloat 的负精度用于可辨识的最小位数，仍须区分类型、指定精度与自定义格式化。[fmt](https://pkg.go.dev/fmt)、[strconv FormatFloat](https://pkg.go.dev/strconv#FormatFloat)。
- PowerShell 默认函数位置绑定、数值转换可表示范围与算术提升须分别核对；可展开字符串的数值转换使用 invariant culture，不等同于普通 ToString 的当前文化。[advanced parameters](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters?view=powershell-7.6)、[type conversion](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_type_conversion?view=powershell-7.6)、[arithmetic operators](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators?view=powershell-7.6)、[quoting rules](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-7.6)。

## 7. 门禁反例推演

下面改变单一条件，检查文本是否提供清晰出口。它们是静态输入假设，不是真实故障注入或已执行测试。

| 只改变的条件 | 文本要求的动作 | 本轮判读 |
|---|---|---|
| frozen-inputs.md 缺失/空白/错项 | 不分类、预检、请求模型或新增提交，先补真实冻结 | 前置停止明确，收尾不替代 |
| 既有 job 活动时冻结缺失 | 停新增动作，继续原身份查询/取证/终止清理，WAITING | 安全收尾例外明确 |
| 分类结果源集合不同或非 ALLOWED/null | 不预检/生成/提交；原诊断保留 | 不能借另一项 ALLOWED |
| 源 build 成功但实际构建的是系统同名包 | 该 PASS 不支持冻结源，修准备后重取适用预检 | 新增精确源覆盖指导 |
| 源 build 非零或源声明上下文缺失 | 按真实诊断分流，不调用转换，不造桩 | LIB 不能免源门槛 |
| 源 build 通过，仅缺合法行为驱动 | 明确冻 LIB 范围，继续生成/自审及目标验证 | 不误作源依赖缺口 |
| 合法行为路径已齐备 | 走有效源基线与双侧行为，不为省事 LIB | 行为义务仍保留 |
| 目标仅编译支持暂未知 | 不试投该验证；生成条件齐备则交目标、验证 UNVERIFIED | 不把平台缺口扩大成不转换 |
| 只有 READY/快照，没有逐例隔离证据 | 不开展受影响构建/运行；不改本机执行 | 安全门禁不被模式覆盖 |
| 规则已读，实际请求只列路径 | 不能记模型已注入，补正文再发受影响请求 | 加载证据层级明确 |
| itoa 源无 struct/异步/I/O 触发 | 不把方向页相关候选注入为义务 | 语义引导不会按标题套用 |
| 自审合法 NO-REPAIR-IDENTIFIED、覆盖完整 | 推进适用评估，仍无编译/行为保证 | 不反复审阅求保证 |
| 模型输出截断/缺文件 | 保留响应/attempt，有限重试，仍失败交部分稿 | 不由 Agent 猜补、不无限请求 |
| POST 超时/HTTP 000 但可能已接收 | 留 body/HTTP/传输诊断，按恢复查原 attempt，WAITING | 不把无回执当未发送 |
| 新目标版本只有旧目标 PASS | 新版本结论 UNVERIFIED，适用自审/准备/独立验证 | 不拼接跨版本成功 |
| job 标终态但清理未确认 | WAITING 并写暂停报告 | 不借终态标签 CLOSED |
| 功能通过却缺 result.md/完整目标/已发生原件 | 交付未齐，不能终态 | 前置与收尾都有效适用 |
| 同 taskId PARTIAL 恢复后 DONE | 进入结论/遗留对账，不重复算新增 40 项 | 统计单位明确 |

## 8. 能证明什么，以及后续最小验证

本轮证明的是：所查入口可回到根规则；覆盖的分支具备前提/动作/依据/停点；具体误导条目已被限于源事实和冻结范围。不能证明实际 Agent 已逐次读完、模型已收到正文、规则正确应用或目标效果有效。

加载状态须分别取证：**可达**看路径/正文；**Agent 已读**看完整读取范围与版本/适用理由；**模型已注入**看实际脱敏请求正文；**效果已验证**看精确目标的独立证据及对应观察。不能用任一层代替下一层。

可在后续授权任务中先做最小记录验证：同一输入和工具配置，只改变冻结文件“缺失/有效”一个变量；观察新窗口 Agent 是否在缺失时停止所有新增动作，并仍保留原 job 安全收尾。回收实际读取记录、动作顺序、冻结版本、停止原因与报告，而非只问 Agent 是否遵守。语义效果实验则固定精确源/契约/模型/工具链，仅改变被测条目的旧/新正文，回收真实请求、目标版本与第三方相关反例；两轮都保持全部安全门禁，不使用错误规则给危险动作授权。本轮没有执行这些实验。

全库无歧义仍需后续逐条语义复核及真实任务证据；本报告不把静态路线完成写成全面效果验证。当前修订已达到本轮覆盖范围内的具体、可审阅指导与引导要求。

收尾检查：人工回读本报告及改动条目，核新章节的消费者/引用、旧措辞残留和关联原件口径；`git diff --check` 与新增报告的 `git diff --no-index --check` 未报告空白错误。保留工作区其他部署/维护报告的原有改动，本轮没有编辑它们。上述检查不执行样本，不支持目标编译或功能结论。
