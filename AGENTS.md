# 项目协作指引

凡涉及代码转换、批量转换或转换评估，必须先读取 [code-convert Skill 发现入口](.agents/skills/code-convert/SKILL.md)，再按根 [SKILL.md](SKILL.md) 的执行顺序加载必读契约和适用知识并逐项推进。

本项目以轻量 Markdown 转换 Skill 为核心交付，不自建转换运行时或样本测试框架：转换由执行任务的智能体当前模型完成，样本编译与运行只在另行批准、与公网及生产网隔离的一次性外部环境（远端 Controller / 隔离 VM）进行。本机可执行已授权的系统文档工具及其文本回归，不承载样本源码、目标或构建运行。

- 按根 [SKILL.md](SKILL.md) 加载任务状态、评估准备、交付与安全真源；各契约的职责互不替代。
- 先核对当前文件和用户要求，能力结论须由本项精确版本的实际证据支持。
- 知识默认离线使用：正文和随附本地参考须包含必要语义，网页、资料标题和目录不能替代内容，不以调用者能联网为前提。
- 本机不编译、不运行源码／目标代码／构建脚本；编译与运行只在获批、与公网及生产网隔离的一次性环境进行，逐例核对隔离与网络/数据边界以[安全边界](references/framework/safety-boundary.md)为准（硬编码外部地址须先阻断/重定向到封闭实验网并验证隔离，`READY`/快照不等于已隔离，绝不触及公网、生产网或真实外部目标）。不运行未经隔离核对的样本，也不将静态审阅说成转换效果验证。
- 交付时说明文件变化、检查范围以及未经验证的部分。

---

## 转换任务执行约束（每一轮任务都适用）

> 本节的规则**逐条适用**于任何转换、批量、评估类任务。与本节冲突的临时便利一律不做。

### 1. 系统脚本与逐项调度边界

**只允许按各自登记边界执行系统脚本；第三方智能体不得编写、生成、保存或运行辅助脚本，必须用原生工具手工、串行、逐项调度。** 登记分类器的有限调用例外见下文。`tools/loading_preflight.py` 及其文本回归仍只由系统维护侧执行，职责限定为仓库结构、正文证据和加载前置核对；第三方智能体回读系统证据，不自行运行加载检查器。规则见[加载工具说明](tools/README-loading.md)，无系统加载支持时完整 manual 核对可继续核其余门禁。禁止通过 shell 内联程序或委托其他模型绕过辅助脚本禁令；加载工具不改任务状态、不自动推进转换。

本轮不建设转换调度框架；第三方智能体禁止的辅助行为包括：

- 批量/流程编排脚本：循环遍历用例、自动冻结、自动提交、自动轮询、自动取证的脚本；
- 打包与请求脚本：用代码生成 capsule、拼 JSON、发 HTTP 请求的封装；
- 模型请求封装：生成/自审/修订由当前模型在会话内完成，不另建 API 客户端、调用函数或 CLI；
- 批量扫描样本、批量冻结或以静态画像替代真实源构建结论。

已登记并钉 SHA 的[安全分类器](tools/safety_classifier_v2.py)就是分类系统；转换智能体可按[分类结果准入](references/workflow/classifier-agent-gate.md)使用原生工具，手工逐项在获准外部临时目录暂存、调用并取回原件，不要求另建分类服务。只允许精确登记脚本，不修改逻辑、不编写包装/批量程序；该例外不包含本机分类流程、样本编译运行、新增驱动、其他模型调用或 Controller 安装目录访问。加载工具的执行者限制不因此改变。

**怎么做**：每一步都用 Agent 的原生工具使用能力，**手动、单项地**执行——

| 步骤 | 手工做法 |
|---|---|
| 画像与选 Skill | 读文件、按源码事实判断，逐项记录依据 |
| 冻结 | 手工写出该项的冻结记录 |
| 分类 | 核登记分类器及获准外部临时目录，以原生工具手工逐项暂存、调用、取回原结果；按准入页核身份/SHA/ALLOWED，不需要额外分类服务 |
| 生成/自审/修订 | 当前智能体模型直接分阶段完成；用原生文件工具写产物，保存阶段输入/输出与父版本，不另请求模型 |
| 组装 capsule | 手工组织源/目标树与清单文件，用归档命令打包 |
| 提交与轮询 | 按[Controller 适配](references/adapter/controller/remote-controller-adapter.md)记录的 shell 命令逐条执行 |
| 取证与落盘 | 逐条取回原始证据，手工归位到该用例的产物目录 |
| 报告 | 手工撰写 `result.md` |

逐项语义判断和复核由 Agent 承担；加载工具提供可机械复核的材料，不以其 PASS 替代分类、构建、安全、功能或终态结论。

### 2. 逐项冻结、逐项推进，禁止批量冻结

冻结必须以**单项**为单位，冻一项就立即推进该项的转换与验证，再处理下一项。不得先把整批冻结完再统一转换。

### 3. 先检查评估系统可达性，再执行适用门禁

单文件（含片段、长文件）与批量每项转换前，先按[评估准备 §1.0](references/framework/evaluation-readiness-contract.md#10-转换前可达性检查与仅转换分支)手工检查第三方评估系统可达性并留原件。以下分类、源构建和动态评估门槛适用于系统可达的正常流程；确认不可达时记 `EVALUATOR_UNREACHABLE_CONVERSION_ONLY`，说明原因，只做冻结→当前智能体模型转换→自审/有限修订→交付门禁，不加载分类准入、不调用分类器、不要求分类产物，不编译、不运行、不提交评估。完整目标、自审记录和 result.md 仍必需，未开展编译/运行/功能为 UNVERIFIED，适用件齐备后 PARTIAL。可达但忙碌/未就绪不等于不可达；未知提交/活动或清理未确认 job 仍 WAITING，不能借分支关闭。

```
转换前可达性检查 → 可达：冻结（frozen-inputs.md 落盘并回读）→ 分类(ALLOWED) → 源侧预检（构建 + 适用运行基线）→ 生成 → 自审
  → 评估就绪核对（安全 + 驱动 + oracle）→ 提交 → 取证 → 先归因再分层报告
  → 交付完整性/终态门禁（记 DONE/PARTIAL 前）
```

- **冻结完成判据**：分类前必须已写出并回读本项本 run 的 `01-frozen/frozen-inputs.md`，核身份/方向、精确源集合/哈希和适用字段；缺失、空白、错项/错版本不得推进，不等收尾才补。源预检、每次生成/自审/修订、提交/重提及恢复新增动作前再次核对，留真实路径/版本与核对结果；不写检测脚本、不新增平台字段。完整判据、待准备条件、历史补录及已发生 job 的查询/取证/终止例外只见[任务状态 §2.2](references/framework/task-state-contract.md#22-冻结落盘门禁)。它是冻结完成的前置核对，不取代本分支适用门禁或收尾。
- **分类（评估可达分支）**：`admissionStatus=ALLOWED` 且 `blockingReason=null` 才可进入该分支下一步。未取得不得预检、不得转换、不得提交。不可达仅转换不适用分类，冻结后直接生成，文本安全边界仍适用。
- **源侧预检**：先取得源侧 `build.status=completed` 且 `exitCode=0` 及适用清理证据。能合法评估行为的，生成前再取得冻结条件下有效源运行基线；本轮行为无法合法评估但源可构建的，按[评估准备 §1.3](references/framework/evaluation-readiness-contract.md#13-lib_unobservable_compile_only-的转换与交付)记 LIB_UNOBSERVABLE_COMPILE_ONLY，继续转换、自审与目标语法/编译验证，不能因缺 main、可执行文件、stdout 或合法入口直接跳过。源构建失败按真实诊断处理，不消耗转换调用；运行/观察问题先归因，不冒充源不可构建或抹去真实失败。可构建性只由编译器诊断定案，源码画像只给候选 sourceOs，不设头文件探针。
- **评估就绪核对**：先核安全边界与本轮评估范围，行为分支再核合法驱动四要素、两侧对称、oracle 及观察有效性；LIB_UNOBSERVABLE_COMPILE_ONLY 核具体行为缺口、目标语法/编译命令和平台确实不运行的支持。所有适用条件通过才提交；判据见[评估准备契约](references/framework/evaluation-readiness-contract.md) §1.3/§2–4。
- **交付完整性/终态门禁**：开始处理每项时必读[交付契约 §1.1](references/framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)，每次正常结束、失败/阻断、非可转换或 WAITING 暂停都走该入口，不能提前返回省掉收尾。每项必须写 result.md 记录原因与覆盖，并按模式/已达阶段/停止原因逐件回读适用产物、版本和指针，将清单及核对结果保存；缺报告或其他应有件不得 DONE/PARTIAL/CLOSED，不等 §8 批次对账才检查。已生成项交完整 target，要求时 manifest；所有去向保留已发生模型/分类/预检/job 原件，未发生件不伪造。未知提交或活动/未确认清理的 job 保持 WAITING，有暂停报告也不解除。DONE 可含真实失败，PARTIAL 与 matched/mismatched 分开，语义只见[任务状态契约](references/framework/task-state-contract.md)。完整性不改功能判定，缺证据 UNVERIFIED，不合成成功率。

**驱动四要素（行为评估缺一不可提交）**：① 按冻结 argv/stdin **启动**；② **到达被观察状态**（服务须等就绪，如端口监听，不得启动即判）；③ **采集**真实 stdout/stderr/退出码/副作用；④ **终止**并收尾。"启动后等它自己退出"**不是**通用驱动——常驻服务会必然超时，白白浪费一轮评估并把结果变成 INCONCLUSIVE。仅编译分支不运行，按适用条件核安全及语法/编译命令，不强迫补驱动。

**驱动/中性入口只能引用用户或获批平台已提供的精确版本**，记录来源/哈希；Agent 不新写、生成、保存辅助驱动，也不委托智能体模型规避 §1。LIB_UNOBSERVABLE_COMPILE_ONLY 表示本轮缺合法入口/观察条件/平台支持或确无安全观察方式，仍在源构建通过后转换并验证目标语法/编译；逐项记录具体原因，不要求证明永远无入口。合法行为条件齐备的仍做行为评估，不为省事省略。目标验证在获批隔离环境以不运行形态完成；支持未知时保留已生成目标、目标验证 UNVERIFIED，收尾 PARTIAL，行为未评估/UNVERIFIED，不造 job 或 comparison。它属已转换项，非不可转换去向；判据见评估准备 §1.3/§3。

正式模型转换即使明确文本交付/片段也须先过冻结；系统可达时再过分类与适用源构建，本轮无法合法行为评估时按 LIB_UNOBSERVABLE_COMPILE_ONLY 明确范围后继续转换。系统不可达按评估准备 §1.0 不加载或调用分类器、不要求分类件、不做源/目标编译运行，仍自审并交 result.md。分类器服务评估运行验收，不作为仅转换前置；恢复评估前补分类准入。不删除源行为义务、不静默放宽比较策略，不把语法/编译通过说成功能通过。纯文档审阅/架构优化不触发转换动态步骤。

**自审是正常推进信号，不是防线**：`NO-REPAIR-IDENTIFIED` 表示本轮有限自审没有找到必须改的可定位转换问题，**即可推进**，不要求它在自审阶段预测编译结果，也不得为它加固而反复重审（那会变成在单个用例上死磕）。`REPAIR-RECOMMENDED` 也不自动触发修复：只有**有源/目标定位证据且属转换引入**的条目才修，待确认差异、源已有问题、环境项不修。真正决定成败的是第三方编译/行为证据。

已定位且依据适用语义确认的转换缺陷，处理与预算消费[单项闭环 §3.1/§4](references/workflow/conversion-evaluation-loop.md#31-语法与功能修复反馈分支)；`ORACLE_NOT_FREEZABLE`、LIB 范围或有限 `matched` 不关闭它。修复核源条件/调用/失败路径，不硬编码迎合当前观察；未修复或修后未验证按交付契约如实写入 `result.md`。这不要求额外自审或无限修复，不改平台原判，也不把疑点标签当缺陷证据。

### 4. 本机只读写文本（含远端同机 Controller 目录）

本机不编译、不运行样本源码、目标代码、构建脚本或其副作用；静态语法检查涉及的构建配置、编译器插件、代码生成同样不在本机触发。样本编译与运行只在获批的隔离环境进行；系统登记的文档工具与文本回归按 §1 执行。本约束同样覆盖与 Controller 共处的提交端宿主：第三方 Agent 在该宿主上只读写审阅文本，**不读写 Controller 安装目录及其 `jobs/`**（`D:\CodeConvertRemote\Stack\`），同机边界细则见 §11。

### 5. 结论分层，不合成单一成功率

功能比较的有效性→冻结允许差异消噪→功能分类→分层统计次序，统一按[评估准备§5.1](references/framework/evaluation-readiness-contract.md#51-有效性消噪与功能分类的次序)。有效matched与有效semantic_pass均可计本冻结范围比较通过小计，分别保留数量、策略与覆盖，不能据标签直接宣布完整功能等价。

交付完整性、语法/编译、功能一致性分别报告；编译、链接、启动、行为、安全分开写。缺独立证据写 `UNVERIFIED`。平台总 verdict 不能当成语法结论；`semantic_pass` 不等于 build PASS；模型自审不是编译或行为结论。**交付完整性既是报告维度、也是 §3 的终态门禁**：它核的是"交付物按去向齐备"，不是功能结论，二者分开——门禁通过不代表功能 PASS，功能 PASS 也不免交付物齐备核对。

### 6. 证据只从真实回传回填

目标代码与修订由执行任务的当前智能体模型直接完成并用原生工具落盘，不存在另一个“只调度不写代码”的 Agent 角色；不另请求外部模型或子智能体代写。生成/审阅记录来自实际阶段与写入，编译/行为证据只从隔离环境真实回传回填，不伪造、不倒填、不改原件。密钥不入日志、manifest、报告或交付文件。

### 7. 先核对再下结论

断言"通过/等价/已修复"前，先看该项**精确版本**的实际证据。读两侧原始观察，不只看摘要与标签；差异先归因（转换引入 / 源已有 / 环境 / 装置），再决定是否修复。装置差异不得与转换差异混算，也不得自行把平台 FAIL 改判为 PASS。

### 8. 每 40 项做一次增量对账

批次是**一个**（整批算一批，不按条数切分），但**不得**把对账压到批次关闭时一次做完。**每新增 40 项到达终态**（`DONE` + `PARTIAL` 合计）做一次增量对账：核对 `self-review-*.json`、阶段输入/产物/写入元数据、失败 attempt、`events.jsonl` 与 `items/<taskId>.json` 的交集与双向差集；历史真实模型请求/响应也按原件保留。**上一轮遗留的未决项必须带进下一轮**，直到解决或关闭时如实记未决；产出**追加式** `reconciliation-<序号>.md`，不改历史。发现缺档立即停止新增转换，先补齐或如实记缺；关闭前另核全部检查点。

### 9. 只手工编排，逐项推进

流水线编排、驱动组装、capsule 打包、提交轮询、取证归位、报告撰写仍手工逐步执行。登记的加载核对及其证据保存仅由系统侧执行；第三方智能体不得使用辅助脚本，详见 §1；不批量冻结或自动推进。

### 10. 加载路径与规则一致性

冻结、实际上下文/知识、模型产物/写入/目标、自审与 job 的版本关联统一消费[任务状态契约 §2.1](references/framework/task-state-contract.md#21-版本关联与复用边界)；源基线复用/失效消费[评估准备 §1.2](references/framework/evaluation-readiness-contract.md#12-源基线复用与失效)。批次阈值和统计单位由批量工作流 §4.1/§6 维护，恢复/重提不能重复计项；读取要求不增加样本执行授权，不扩张登记系统工具职责。

新项按根入口第 1 步先读六份通用契约及适用工作流、连接检查正文，检查可达性；仅可达分支在冻结前补读分类准入及评估专用适配。再画像、选择并读取知识、完成冻结；每项必读两语言页和一个方向，场景/系统及专题按源码触发。知识可达、实际读取、当前模型上下文已具备和效果验证按[任务状态 §2.3](references/framework/task-state-contract.md#23-知识加载与实际消费)分列，不互相替代；准备上下文不授权提前生成。

**加载路径**：

主干（每个转换任务都会走）：

```
.agents/skills/code-convert/SKILL.md   ← Codex 读到的第一个文件
  → AGENTS.md                          ← 自动加载
    → SKILL.md                         ← 根入口（"按以下顺序执行"的 6 步）
      → skills/workflows/{batch,long-file}-conversion/SKILL.md
      → references/framework/{task-state-contract,evaluation-readiness-contract}.md
      → references/workflow/{conversion-evaluation-loop,
             build-prerequisites}.md
          → references/framework/{delivery-handoff-contract,safety-boundary}.md
            → references/adapter/controller/remote-controller-adapter.md（连接检查正文）
              → 可达后补 references/workflow/classifier-agent-gate.md 及评估适配
```

行为保持指导按单文件目标/允许差异需要加载，评估门禁以评估准备契约为准；必读门禁不依赖可选指导。上述图展示依赖，不授权跳过根入口规定的逐项读取时点。

**分支（按源码事实加载）**：语言页和方向为每项必读，场景、系统、战术及随附专题按实际触发条件读取。

```
skills/directions/<源>-to-<目标>/SKILL.md   42 个方向 skill（按本次语言方向选一个）
  └── references/{type-abi,header-macro}.md 方向内专页（如 c-to-cpp；按需）
skills/references/languages/{c,cpp,csharp,go,powershell,python,ruby}.md
                                            源与目标语言页各一（按本次两个语言选）
skills/references/seven-language-common-semantics.md   共性语义导航
skills/references/security-behavior.md                 跨场景安全行为（按行为触发）
skills/scenes/{network-io,file-io,process-execution,concurrency}/SKILL.md
                                            4 个场景（按源码实际 I/O/并发行为多选）
skills/systems/{posix-winsock,posix-windows-filesystem,
    posix-windows-process-identity,posix-windows-threads,
    windows-registry-service-subsystem}/SKILL.md
                                            5 个系统方向（按触发的平台 API 多选）
skills/attack-tactic-index/SKILL.md         战术索引（仅核对分类，不生成规则）
```

方向、语言、场景和系统页只提供适用映射与语义依据，不替代门禁、不构成执行授权。短版规则与完整契约须一致；oracle 是行为评估的条件义务，仅编译分支不要求不存在的运行观察。遇到引用不可读或规则冲突，记录受影响条目，停止受影响动作，不自行放宽约束。

### 11. 同机共处纪律

提交端（转换 Agent 工作区）与评判端（Controller）同处远端宿主，**宿主本身可连公网**；样本的编译/运行与网络隔离只在 VM Agent 内，隔离由 VM 层施加，不由这台共处宿主提供。因此：

- Agent 不得读取、写入、枚举或修改 Controller 安装目录及其 `jobs/`（`D:\CodeConvertRemote\Stack\`），不借同机便利查看/改动 job 存储、证据或比较中间件；评判端与被评估端的物理共处不改变两者授权边界。
- 同机不构成隔离证明：宿主可连公网，回环可达 Controller、`READY`/`clean`/快照回滚均不等于网络已隔离。
- 该宿主不承载样本的编译/运行；一切编译与运行仍只在 VM Agent 内按[安全边界](references/framework/safety-boundary.md)逐例核对。连接坐标与同机边界细则见[Controller 适配](references/adapter/controller/remote-controller-adapter.md)。

本条真源为[安全边界](references/framework/safety-boundary.md) §1；此处为执行约束侧的操作纪律，二者口径一致。
