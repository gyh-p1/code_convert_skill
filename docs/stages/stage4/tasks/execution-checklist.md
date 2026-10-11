# Stage 4 任务与静态验收记录

> 状态：TEXT_COMPLETE / STATIC_REVIEWED ｜ 更新：2026-10-11
> 方案：[architecture-plan.md](../plans/architecture-plan.md)；工作包：[README](../README.md)。规范/能力分别以[开发规范](../../../项目开发规范.md)、[业务边界](../../../项目业务文档和能力边界.md)及[安全边界](../../../../references/framework/safety-boundary.md)为准。

> **2026-10-11 追加更正**：§1–4 保留此前架构优化的静态记录。其中“源侧预检只构建/不运行”的收紧已由用户确认撤回，不能作为现行执行要求；恢复内容与本次回查见 §5。原静态通过不证明该语义改变获得用户认可，也不证明历史批次违规。

| 任务 | 状态 | 本轮结果 |
|---|---|---|
| T1 契约和执行链收口 | PASS_STATIC | 新增任务状态/评估准备真源；入口与单项闭环有分类/源预检；状态不由行为标签决定，交付按实际阶段 |
| T2 知识归属与索引 | PASS_STATIC | 普通输出/控制流归语言，具体 API 映射归方向，场景保留行为；共享安全专题归共性参考，索引注明触发/消费者 |
| T3 平台适配与开发期解耦 | PASS_STATIC | Agent 所需授权字段在适配页；当前部署路由能力矩阵，历史规格仅作来源，不充运行依赖 |
| T4 全加载路径静态回查 | PASS_STATIC | 原生 rg 穷举与定向搜索、逐类人工审阅、实际路径/标题核对、纸面走查、git diff --check |

本轮只编辑 Markdown。未运行源码/目标/构建脚本、分类器或任何验证/辅助脚本，未调配置模型、未连接 Controller、未触其安装目录；未改历史证据、提交或推送。原有工作区修改在当前文本上保留，未重置。静态通过不证明转换效果或外部能力。

## 1. 改动与职责回收

- 根/发现入口与 references 总索引：必经契约和按需知识分开，完整门禁可达，ATT&CK 有实际路由。
- task-state-contract：身份、冻结字段、封闭接入去向（补齐 SOURCE_DEPENDENCY_GAP）、变体/新增 intake、phase/lifecycle 与验证结论。
- evaluation-readiness-contract：合法来源驱动、四要素、oracle 状态、对称性、非退化观察、仅编译；补出生成前源预检的适用准备分支。
- 单项闭环：补 CLASSIFIED/SOURCE_BUILDABLE，保留有限自修/评估后预算、结构化自审及响应完整性；准备判据引用契约。
- 批次：手工串行、逐项冻结、恢复/未知提交、40 项增量对账/遗留携带、终局核对；不复制状态词表或驱动判定表。
- 交付：冻结 Markdown 与分类 JSON 不再互斥；保留不可变请求/原响应；生成失败/评估前停止/已评估按适用件收尾，未知提交不能终态。
- 行为指导：目标与允许差异保留，旧 §4.1 章节转引真源，不维护另一套门禁/生命周期。
- 网络场景的 7 对语言 API 细节归对应方向；进程场景的 os/exec 细节归 Go→C++。
- Ruby/C#/PowerShell 输出语义与 C 一次性块归语言页；C#→Ruby、C→Ruby 维护映射，并发仅保留并发移交责任。
- 文件系统系统页按 API/平台触发，说明主要 POSIX→Windows 与有限 macOS 范围；语言层内容转 C→C++ 参考，不把只读样例限制套全部任务。
- 跨场景 security-behavior 在 skills/references 单一维护，旧路径保留薄跳转与标题；网络、文件和战术索引更新链接。
- 业务自动化目标不降级；现行手工操作及未验收差距明确，产品阶段未改变。

## 2. 加载路径回查

用 rg --files 穷举实际磁盘，未用脚本生成检查器。skills/ 共 54 个 SKILL.md；主干之外 52 个为 42 方向+4 场景+5 系统+战术索引。另核发现入口、根入口、AGENTS、共享参考与契约/适配消费者。

| 范围 | 逐类核对结果 |
|---|---|
| 发现入口 / AGENTS / 根入口 | 必读真源、完整门禁、文本/片段与纯文档边界一致；收尾依适用件 |
| 42 方向 | 每页共性语义行逐一核源/目标链接，7×6 无遗漏；全部有根入口与安全回链；补掉 C→C++ 的无入口“补驱动即可”旧口径 |
| 4 场景 | network-io / file-io / process-execution / concurrency 均回根/安全；迁移内容保留对应路由，触发不再靠错误场景 |
| 5 系统 | posix-winsock / posix-windows-filesystem / posix-windows-process-identity / posix-windows-threads / windows-registry-service-subsystem 均回根/安全；评估语言遵守条件义务 |
| 2 工作流 | batch-conversion / long-file-conversion 消费新契约，串行/分段不改变生成前门禁或预算 |
| ATT&CK 索引 | 根入口显式路由，索引回根/安全；安全行为链接已指共享专题 |
| 7 语言+共性导航 | c/cpp/csharp/go/powershell/python/ruby 文件均在，两语言页由方向链接，共性导航回根；单语言事实不当系统映射 |
| 其他参考 | 共享安全新页/旧兼容页、C→C++ type-abi/header-macro 的路径与本轮新增标题人工核对 |
| 工作流/契约/适配 | 冻结→分类→源预检→生成顺序、合法驱动、终态适用件、授权字段消费者一致；只读构建需求不假称接口已支持 |

原生 files-without-match 检查方向/场景/系统/工作流的根与安全回链无缺项；42 页语言导航逐行看过。新增/迁移链接的相对层级、目标路径用 Resolve-Path 核存在，锚点对照实际标题；代码块和行内源码的方括号表达式不作为链接错误。原有外部链接未逐条联网复核，没有运行自动链接扫描器，因此不宣称全仓所有链接已经机器验证。

旧“BLOCKED 可文本转换”“matched 就 DONE / 差异就 PARTIAL”“01-frozen 禁全部 JSON”“冻结唯一产物”“平台仍不消费分类”“新增默认换 batch”等定向搜索无执行性残留；AGENTS 的反例/历史教训保留，不作为现行规则。git diff --check 通过；它只检查文本差异格式。

## 3. 纸面走查（不是动态试验）

保持源事实不变，仅改变任务形态，核加载路径、下一步与适用件：

| 情形 | 预期路由/结果 | 静态结果 |
|---|---|---|
| 普通输出，无子进程 | 两语言页+方向即可获得通道/换行；不因打印加载进程场景 | 一致 |
| 单线程 do-while(0) | C 事实+方向保持一次执行及源清理条件；不加载并发取规则 | 一致 |
| 可观察库缺合法入口 | 准备缺口/WAITING，由合法提供者补件；不降仅编译、不自写驱动 | 一致 |
| 真正无安全入口 | 分类/源预检后生成，平台支持时仅编译；PARTIAL、功能 UNVERIFIED | 一致；平台支持待核 |
| 生成前源预检 | ALLOWED/安全/工具链/源构建齐备；不要求目标或自审，不运行入口补证据 | 一致；预检外部形态待核 |
| 生成后自审/安全停止 | target/result/适用记录齐备后部分交付，无未提交 job 的虚构要求 | 一致 |
| 源依赖缺口 | 由真实源诊断分流，不耗模型、不要求 target/job-01，原因及已发生件保留 | 一致 |
| 已发送缺回执 | WAITING+SUBMISSION_UNKNOWN，保留 attempt，不盲重投、不以 PARTIAL 关闭 | 一致 |
| 同批新增条目 | 新 intake/集合版本追加，同 batch、已有身份不变；关闭批次先记录重开 | 一致 |
| 第 40 个终态 | 增量对账带上一轮遗留，缺档停新增；终局另核全部检查点 | 一致 |

失败信号是下一步冲突、规范不可达或必须伪造产物才能终态。本轮纸面未再发现上述冲突；它不证明模型会正确加载/遵循规则。

## 4. 保留的未验证事项

- 42 方向技术正确性、长文件/批次效果、所有技术来源的适用版本没有全面复验；本轮是架构归位，规则仍有自身证据边界。
- Controller 能否安全表达源侧只构建预检、双侧仅编译、不运行/不链接可执行的具体接口仍须合法外部证据；未知时待准备，不造请求或偷偷运行。
- 实际工具链、逐例隔离、合法来源驱动效果、oracle 覆盖、平台拒收/无法绕过等仍需隔离环境逐项验证。
- 原 ≥40 无需人工操作目标保留未验收，手工链路/静态收口不能替代该目标；本轮未建设自动编排。
- 原始响应留证、部分交付门禁等纸面规则是否被未来 Agent 正确执行，须回收真实任务记录；不回改旧 evidence 来满足新形制。

## 5. 源侧运行预检口径恢复（2026-10-11 追加）

**依据**：用户指出源侧预检用于确认源正常、取得转换有意义的基线，并在追溯修改来源后明确确认“恢复一下”。此前架构优化把“构建通过是生成门槛”收紧成“源预检一律不运行”，属于不应混入架构整理的执行语义变化；本节撤回该限制，不用它倒判历史批次。§1–4 的原记录保留，涉及只构建源预检的条目以本节和现行契约为准。

### 5.1 恢复内容与文件变化

- [评估准备 §1.1](../../../../references/framework/evaluation-readiness-contract.md#11-生成前源侧预检)维护完整判据：先源构建，需行为评估时在正式模型生成前按冻结输入/初始状态真实运行源，取得有效观察并终止/清理。build 成功、退出码 0 或非空 banner 不单独证明源基线有效；预期错误路径和服务不强制正常退出码/自行退出。
- 发现入口、AGENTS、根 SKILL 的门禁摘要与实际执行步骤同步；单项闭环、批量和长文件工作流在生成前消费源基线核对，源运行/装置缺口不误记为源不可构建或目标失败。
- 分类准入、构建前提、任务状态、交付契约、安全边界、Controller 适配及 references 索引同步适用时点和字段职责。预检保留源 build、适用 execution、原始观察与清理记录；沿用 SOURCE_BUILDABLE 阶段名和 job-00-source-buildability 目录，不新增平台 schema 或虚构接口能力。
- 明确文本交付/无行为评估片段、逐项举证成立的 LIB_UNOBSERVABLE_COMPILE_ONLY 保留适用构建预检与不运行例外，功能 UNVERIFIED；可安全观察而缺入口不能用例外绕过。
- 原有门禁短链涉及源构建预检的 6 个方向页、3 个场景页、5 个系统页同步为“源侧预检（构建 + 适用运行基线）”；进程场景已有短链同样同步。其余方向/战术/共享语义页通过根入口与安全边界消费规则，未复制第二套判据。
- 业务流程概览、开发规范和本阶段方案同步摘要；本记录追加更正，保留原静态记录。工作区原有修改保留；未改转换产物、历史 item/event 或原始 evidence。

### 5.2 实际加载路径回查

原生 rg --files 重新穷举得到 skills 下 54 个 SKILL.md，并列出 7 语言页、2 共享参考、2 个 C→C++ 方向内专页及网络安全兼容页；另核发现入口、根 SKILL、AGENTS。回查聚焦本次改变的预检语义、适用例外、门禁时点和链接，不声称全面复验各语言技术规则。

| 实际文件范围 | 本次逐项核对 |
|---|---|
| .agents/skills/code-convert/SKILL.md → AGENTS.md → 根 SKILL.md | 首读入口和根“按以下顺序执行”均明确需行为评估的生成前源运行基线，链接准备契约 §1.1；纯文档审阅不启动动态步骤 |
| batch-conversion、long-file-conversion | 冻一项推进一项；任何生成/分段前完成适用源基线；不重置预算，不自写驱动 |
| task-state、evaluation-readiness、conversion-evaluation-loop、classifier-agent-gate、build-prerequisites | 身份/冻结、分类先行、源构建与适用运行、缺口分流和生成门槛一致 |
| delivery-handoff、safety-boundary、remote-controller-adapter | job-00 的真实源运行/观察与清理一起留证；只在获批隔离 VM，宿主/Controller 安装目录边界仍适用；外部形态未知如实待准备 |
| C 方向：c-to-cpp、c-to-csharp、c-to-go、c-to-powershell、c-to-python、c-to-ruby | 六页逐一核根入口/安全回链及相关执行表述；三页显式门禁短链已同步 |
| C++ 方向：cpp-to-c、cpp-to-csharp、cpp-to-go、cpp-to-powershell、cpp-to-python、cpp-to-ruby | 六页逐一核回链及相关执行表述；cpp-to-c 短链已同步 |
| C# 方向：csharp-to-c、csharp-to-cpp、csharp-to-go、csharp-to-powershell、csharp-to-python、csharp-to-ruby | 六页逐一核回链及相关执行表述，无本次预检限制残留 |
| Go 方向：go-to-c、go-to-cpp、go-to-csharp、go-to-powershell、go-to-python、go-to-ruby | 六页逐一核回链及相关执行表述；go-to-c 短链已同步 |
| PowerShell 方向：powershell-to-c、powershell-to-cpp、powershell-to-csharp、powershell-to-go、powershell-to-python、powershell-to-ruby | 六页逐一核回链及相关执行表述，无本次预检限制残留 |
| Python 方向：python-to-c、python-to-cpp、python-to-csharp、python-to-go、python-to-powershell、python-to-ruby | 六页逐一核回链及相关执行表述；python-to-go 短链已同步 |
| Ruby 方向：ruby-to-c、ruby-to-cpp、ruby-to-csharp、ruby-to-go、ruby-to-powershell、ruby-to-python | 六页逐一核回链及相关执行表述，无本次预检限制残留 |
| network-io、file-io、process-execution、concurrency | 四页逐一核回链与短链；均保留场景不授权执行的边界 |
| posix-winsock、posix-windows-filesystem、posix-windows-process-identity、posix-windows-threads、windows-registry-service-subsystem | 五页逐一核回链与短链；本次源预检语义与根入口一致 |
| attack-tactic-index | 回根入口/安全边界；战术不替代门禁或授权 |
| languages/c、cpp、csharp、go、powershell、python、ruby；seven-language-common-semantics、security-behavior | 逐页核相关执行表述与共享路由；语言事实不维护源预检的第二判据 |
| c-to-cpp/references/type-abi、header-macro；scenes/network-io/references/security-behavior | 按磁盘实际专页/兼容页核相关表述与路由，无源预检只构建限制 |

本次对新增/调整的真实 Markdown 链接逐一看目标与相对层级，同层同深度回链按各页实际字符串核对；用 Resolve-Path 确认目标存在，并对照 §1.1 标题核锚点。代码块和行内源码的方括号表达式不作链接，不运行链接扫描脚本。不改原标题，既有章节锚点继续有效。

### 5.3 反例残留与纸面走查

“只消费源 build”“预检只读取源 build”“源预检形态须支持不运行”“不以预检形态运行入口”“只构建源的预检”等本次禁止运行的执行性表述已清除。§1–4 的旧静态结论明确标为已更正历史；仅编译分支和本机禁止执行仍适用，不能把这些例外反推成所有源预检禁止运行。

| 单一变化的纸面情形 | 现行下一步 |
|---|---|
| 源 build 已通过，但需行为评估且未取得源运行基线 | 停在生成前，记录基线准备缺口；不能因 build=0 放行 |
| 同一源/输入取得有效原始观察并完成终止/清理 | 其余适用门槛齐备后进入生成；源运行不是目标功能证据 |
| 冻结目标是预期错误路径，源非零退出符合该观察目标 | 据真实观察核基线，不因非零退出单独判源不可用 |
| 同一服务仍存活但已就绪、取得约定响应并由合法驱动终止/清理 | 不要求服务自行退出，不以超时充当通用驱动 |
| 任务确为文本交付/无行为评估片段，或举证成立的无安全入口仅编译 | 分类和适用源构建仍必经，记录运行不适用与功能 UNVERIFIED |
| 缺合法驱动、隔离、真实观察或运行接口支持 | 待准备，不新写驱动、不提前生成目标补预检包，不虚构源正常 |

本次仅做文本与引用回查，git diff --check 通过；没有运行源码/目标/构建脚本、分类器、验证/辅助脚本，没有调转换模型、提交新 job 或连接 Controller。实际平台形态、源基线有效性和转换效果仍须逐项取得隔离环境原始证据；本次不宣称已动态验证。

## 6. 评估证据与规则修订（2026-10-11 后续任务）

用户提供新的问题/对账/更正材料并要求开始修订、判断是否需要阶段任务。本轮继续归属 Stage 4，方案见[评估证据与规则修订](../plans/evidence-quality-revision.md)，新任务与回查记录见[修订任务清单](evidence-quality-checklist.md)。平台部署和适用能力验收仍由 Stage 3 承接；不增加 Stage 5、不覆盖 §1–5 的历史记录。
