# 历史批次问题对当前转换与评估系统的优化审查

> 日期：2026-10-12。性质：静态审查与优化建议，未实施产品修订、未开展转换效果验证。
> 输入：[前篇](../optimization-inputs.md)、[续篇](../optimization-inputs-2.md)及按问题索引回读的过程原件。它们来自此前版本，不能直接充作当前故障清单。
> 对照基线：转换仓库 HEAD `016af0e` 加当前未提交工作区；相邻评估系统源码 HEAD `a908e0b`。部署材料登记 1.0.29；本轮未连接现役服务，不宣称源码审阅等于现场复验。
> 独立源/目标代码已删除。本轮不恢复代码、不改历史 item/事件/报告；自审中引用的代码只是历史定位材料，不能代替完整版本复核。

## 1. 审查结论与范围

三侧划分成立，但每条优化还须分清：**规则缺失、规则已有但历史执行未落实、平台能力缺口、历史汇总本身失准**。把这四种情况都改成更长的 prompt，会增加负担并继续误归因。

当前最有价值的工作按顺序是：纠正会污染知识的错误语义；收紧构建与运行故障的归因边界；处理平台孤立请求恢复；补 Unicode/容器/Win32 的具体映射；验证知识适用性、输出来源与修复覆盖。已有门禁主要需要真实执行证据，不宜再复制一套。

本轮分三组审阅：

| 审阅组 | 实际读取 | 覆盖与限制 |
|---|---|---|
| 历史问题与现行规则 | 两篇汇总；summary §11、reconciliation-6、运行纪律的相关段落；根入口/发现入口、业务与开发规范、Skill 编写规范、任务状态/评估准备/交付/安全、分类准入、构建前提、自审闭环和 Controller 适配 | 覆盖汇总中各问题类别；未重新逐项统计 277 项，也未逐件验收全部交付目录 |
| 语义与归因抽查 | D2-247、254、116 的自审原件；247、254 的双侧流与 comparison；251 的完整源 evidence；186、118、065 的 item；207 的 comparison；247、254 的请求正文保留部分 | 能核修复建议、有限观察及归因；不能重新确认被删除目标的具体实现或全部源码事实 |
| 当前平台与部署材料 | 相邻评估仓库 source-preflight、comparator、functional assessment、job service/closure、VM 字节采集及相关已有测试文本；1.0.29 部署/持续 busy 记录；C# 探针报告 | 只读产品源码和已有证据，未运行任何测试/样本，未访问 Controller 安装目录/jobs |

下文“已解决”均附范围：文本已补、源码已实现、已有局部探针，三者不能互换。建议优先级 P0 表示会导致错误推进、错误归因或证据不可用；P1 表示有实质价值但可逐项维护。

## 2. 已解决或已有规则：不重复立项

| 历史问题 | 当前对照 | 本轮结论 |
|---|---|---|
| 无入口/无 main 就停止生成 | 评估准备 §1.3、根步骤 5、任务状态 §3 已允许源构建通过后走 LIB_UNOBSERVABLE_COMPILE_ONLY | **规则已解决**；续篇的 31 项无入口停止是历史结果。恢复须有原源快照/构建对应，不能凭现在的文字倒填为已转换 |
| 源预检需要占位目标 | 当前协议适配 §2、平台 source-preflight manifest/report 与接口 | **实现与适配已有**；新预检不再造目标。续篇“D2-197 起全部 build-only”也不能照搬：D2-247/251 item 明确为 build-and-run |
| C# bundle schema 拒收 | [C# 局部探针](../platform-probes/probe-csharp-target-2026-10-11/PROBE-RESULT.md)返回 target build/exec completed/0；平台修订记录说明 producer/fallback 修订 | **该探针不再复现**，不等于所有 C# 用例恢复完成；38 个受影响候选与20个已登记 WAITING 是不同统计集合 |
| 源树变化却沿用分类、误引旧 BLOCKED | 分类准入 §3、任务状态 §2.1 已核精确集合/版本；保留旧原件，使用当前适用分类引用 | **规则已有**；优化对象是实际引用落实，不能采纳续篇“删除 classification-1 原件” |
| 驱动吞输入、包 JSON、启动形态不符、构建产物污染观察 | 评估准备 §2/§4/§5、比较适配 §3 已规定来源、四要素、原流、对称与业务文件范围 | **规则已有**；不采纳历史“Agent 新写驱动并本机语法自检”建议。需要修正装置时由合法提供者交付精确版本 |
| 空流/相同 usage 自动证明业务通过 | 当前 comparator 有退化观察处理，报告明确不证明路径覆盖/输出来源；评估准备 §5 区分预期错误路径与空跑 | **部分实现并有明确边界**；剩余是独立路径/来源证据，不能重复要求“一切空输出都失败” |
| 只有终态标签、缺原件/清理也收尾 | 当前协议 §4、交付 §1.1 和平台 closure 门禁 | **实现与规则已有**；真实任务是否遵守仍须单项原件 |
| POST 超时盲重投、归因覆盖原 verdict | 当前协议 §5/§6：submissionId 精确幂等、未知恢复、追加 annotation | **实现已有**；旧提交没有 ID 不因此获得可恢复性；annotation 不等于改判 |
| 工作目录绝对路径噪声 | noise-tolerant-v2 的精确 workspace_path_pairs | **有限实现已有**；不自动处理所有路径、耗时、stderr 差异或服务状态，历史 v1 结果不追改 |
| 自审围栏/损坏/截断、追加审阅失控 | 闭环 §2/§4、长文件 §4.1：原件保留、有限恢复/重试、语义单元与跨单元覆盖 | **规则已有**；D2-247 的长度截断不是新增无限审阅预算的理由 |
| argv/getopt、CRLF、枚举、读键、临时目录 | 两语言正文、方向条目、共性导航已覆盖前篇多数问题 | **已有实质知识**；按具体源使用点检验，不能以条目存在或旧 matched 宣称效果 |

## 3. 转换知识侧：仍值得补充的具体规则

### K1｜P0：先阻断错误自审建议进入知识

D2-247 自审2的 `expandtabs-tabsize-le0` 声称“tabsize≤0 保留制表符”，标为 `source-preexisting`，续篇又记为采纳修复。**这条技术前提错误。** CPython 3.12 `unicode_expandtabs_impl` 的制表符分支只在 tabsize>0 写空格；否则不写该字符。因此 `"a\tb".expandtabs(0)` 的官方实现语义为 `"ab"`，不是保留 tab。这是官方实现静态核验，未在本机执行。

同项最终 comparison 是 matched，但 item 明确只观察 dedent 的33字节输出；该输入没有验证 tabsize≤0。不能据此宣称这条建议已被验证，也不能在没有目标正文时断言最终目标一定存在此缺陷。

**建议**：在本次工程审查材料追加更正，保留原自审和原 verdict；后续知识维护先核具体 API 的版本/实现，不能把“采纳过 + 最终 matched”升级为规则。当前闭环 §4.1 已有这种证据分层，不必再造自审判定器。Python 语言页补相应退化入参事实时，同时列正常值、0、负值及实际字符单位。

依据：[原自审2](../../python-to-cpp/D2-247-python-textwrap.py/output/batch/03-self-review/self-review-2.json)、[item](../items/D2-247.json)、[comparison](../../python-to-cpp/D2-247-python-textwrap.py/output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json)；[CPython 3.12 实现](https://raw.githubusercontent.com/python/cpython/3.12/Objects/unicodeobject.c)，函数 `unicode_expandtabs_impl`。外部依据仅属维护核验资料，运行 Skill 仍须有自足本地正文。

### K2｜P1：Unicode 规则须按具体谓词与字符单位细化

当前 Python/C++ 语言页有 str/bytes、编码与长度事实，但没有提供足够具体的 strip/isspace/splitlines/expandtabs 跨语言映射。D2-247 首轮补裸0x85、次轮再改UTF-8，说明缺的是统一表示及逐谓词规则。

**建议落点**：Python 语言页维护实际 API 集合/版本与返回边界；C++ 语言页明确 byte/码点处理前提；python-to-cpp 维护如何组合这些事实；共性导航提供触发项。不能只加一句“支持 Unicode”。

必要区分：U+0085 的 UTF-8 编码为 C2 85，不可把任意0x85尾字节删为空白；splitlines 的行边界不等于 strip 的空白集合；textwrap 内部的 ASCII 空白替换集合也不等于所有 Unicode 空白。官方 textwrap 3.12 将该集合单独定义，不能把所有调用统一成一个宽泛 is_blank。

依据：D2-247 [自审1](../../python-to-cpp/D2-247-python-textwrap.py/output/batch/03-self-review/self-review-1.json)/自审2；[Python字符串方法](https://docs.python.org/3.12/library/stdtypes.html)、[textwrap 3.12.0 实现](https://raw.githubusercontent.com/python/cpython/v3.12.0/Lib/textwrap.py)。此官方版本不代替已删除的该项源副本。

### K3｜P1：容器按“操作端点与消费顺序”映射

D2-254 的原自审2给出 `appendleft` 后 `popleft`，多次 push A、B 后先取B；目标 Queue 的 Enqueue/Dequeue 则先取A。当前适用语言/方向页缺这种具体组合映射。

**建议落点**：Python 页维护 deque/list 的端点操作与顺序；C# 页维护 Stack/Queue 的对应操作；python-to-csharp 给出候选映射。不能将“deque 一律转 Stack”写成规则：两端混合操作可能需要真正的双端表示。映射也须保持空容器异常与返回形态。

依据：[D2-254 自审2](../../python-to-csharp/D2-254-python-shlex.py/output/batch/03-self-review/self-review-2.json)、最终45字节双侧流/comparison；[deque 官方语义](https://docs.python.org/3.12/library/collections.html#collections.deque)。该45字节输入不证明多次 push_token 路径已验证。

### K4｜P1：Win32 结构体身份与返回层次比 API 名称更关键

D2-116 自审指出 AccessCheck 首参传 pDacl 而非 pSD；[官方契约](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-accesscheck)要求安全描述符，并另有调用成功与 AccessStatus 两层结果。当前文件权限/身份知识没有这一具体条目。注册表页只简述 REG_EXPAND_SZ 是否展开不同，也尚缺读取调用的具体选择依据。

**建议**：在既有文件权限/进程身份知识位置补安全描述符、DACL、token、generic mask、调用成功/访问允许、缓冲长度和释放配对；注册表系统页补按源读取选项保持展开行为与环境快照。csharp-to-cpp/go 只维护对应映射/互操作边界，不再复制整套 Win32 事实。

D2-116 item 还记录了源98行命中、目标12行无命中的结构差异，不能仅说“全是动态PID噪声”。不过缺完整源目标与受控反例，当前只能保留可定位疑点。oracle 不可冻结不否定静态 API 证据；能确认转换引入时可走有限模型修订，但修订后仍不能宣称行为PASS。

### K5｜P1：清理仍残留的“惯用写法硬禁令”

当前 python-to-csharp 的 PY-CS-01 因性能/强类型理由笼统禁止 Dictionary 模拟 kwargs；PY-CS-02 禁用 System.Tuple，超过4项建议改 record。它们与当前任务状态 §2.3、Skill 编写规范 §2“接口和返回形态优先”仍有张力。D2-254 保留请求确实注入了前一条硬禁令。

**建议**：只有键集合闭合、默认值/未知键/类型错误及调用方式能保留时，才用 Options；tuple 表示选择依据应是值/别名/消费者与接口义务，不能用项数或分配偏好裁决。D2-247 的 wrap/fill 签名也不能被“语言不同”一概豁免：应核调用者是否可表达同样的缺省/参数/错误行为。

这是当前规则质量问题，**不据此断言它造成了历史失败**。修改时按实际加载链检查相关方向/语言正文，不扩展为新运行时。

## 4. 转换流程与契约侧：修正口径，验证执行

### F1｜P0：源构建与运行接口不匹配必须分开

[D2-251原始源 evidence](../../python-to-csharp/D2-251-python-csv.py/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json)明确 build completed/0，execution completed/1，stderr 为 `_csv.__version__` ImportError；[item](../items/D2-251.json)却是 SOURCE_NOT_BUILDABLE。

当前根入口与评估准备已说“不把运行问题记源不可构建”，但**构建前提 §0.1 表格仍笼统将“源接口与runner不匹配”记 SOURCE_NOT_BUILDABLE**，任务状态 §3“平台/接口不可构建”也需按构建阶段限定。这是现行文档中的具体歧义。

**建议**：仅编译器诊断确认不可构建时采用该去向；构建通过后的 import/LoadLibrary/初始化错误分列源运行基线和依赖/环境原因。py_compile 不解析运行期 import，语法PASS不是依赖齐备证明；也不能为补依赖验证强迫运行所有仅编译项。影响实现的真实源接口/依赖缺口未明时仍停止，不能自动用 LIB 分支掩掉。

变更消费者：构建前提→任务状态/评估准备→根入口/单项闭环→批量/长文件；方向分支涉及构建结论处一并回查。历史D2-251只能追加更正，不删除原记录或伪造新预检。

### F2｜P1：已有知识适用性门禁需要用真实请求检验

D2-247 请求正文保留部分写“TextWrapper._split 是生成器”并注入 PY-CPP-01；官方 textwrap 3.12.0 的该函数返回 chunks 列表。该项源副本已删，不能断言其与官方版完全相同，但这是一条**必须回源核实的画像疑点**。

当前任务状态 §2.3 已要求“源使用点→前提→正文→实际请求”对应，方向规则也明确只在yield触发时使用。问题不应通过给每个prompt加入全部规则解决。

**建议**：后续小规模任务回收已选条目的源符号/范围与实际发送正文，核是否发生“没触发却强行注入”“路径列过但没注入”“手工改写正文误导”。记录用既有冻结/请求元数据，不增检查脚本、通用台账或多轮自审。

### F3｜P1：将修复条目与“实际覆盖”连接起来

D2-247 的33字节dedent、D2-254 的45字节正常token、D2-194 的空argv路径都不足以验证全部修订。当前闭环 §3.2 已要求原失败反例及相关回归；覆盖义务也已存在。

**建议**：每个采纳条目在现有裁决/result中明确对应“已受控观察/仅静态修订/未验证”及原件。待合法提供者给出边界输入、入口或向量后再验证，不能由 Agent 新写库驱动；仅编译项仍交目标，行为保持UNVERIFIED。分派漏臂的静态完整性核对与动态单路径比较分别写，help/helper存在不能代替分派可达性。

### F4｜P1：动态量及运行时差异不能一概归为装置

续篇建议“含主机运行态直接ORACLE_NOT_FREEZABLE”“stderr/退出码差异先判语言运行时”，都太粗。D2-118 支持状态漂移是解释候选，但218项相同不能单独证明其余映射均正确；D2-116有结构差异；D2-207的Go panic与Python traceback是语言诊断差异，并非都属于采集装置。

**建议**：先区分主机状态、工作目录、运行时诊断、输入/驱动失败与转换引入。有合法平台提供的受控状态或独立断言时可以另冻条件；没有则本轮行为缺口据实记，不推断永远不可验证。退出码是独立观察量，不能与stderr一起忽略；允许的诊断差异必须事前明确，当前未知就保留原mismatched。

### F5｜P1：历史材料需要按版本与分母引用

续篇“CONVERTED23项”与“有自审21项、余下120项全是非转换”在同一口径下不能同时成立。应先查是统计漏项、去重/恢复口径还是材料缺失，不能据此宣称自审覆盖完全。summary与续篇事件行数来自不同截止点，也不混成同一快照。

源码/目标删除是已知材料保留决定，**不因此将历史DONE改成当前交付验收失败**；但旧路径、哈希或原result也不能证明现在仍可重放。恢复需要重新取得精确合法原件，并另核规则、平台及授权。禁止仅按旧taskId直接继续模型调用。

建议保留两篇为历史汇总，以本报告追加纠偏；不将运行纪律里“请求构造器、新写驱动、删除旧分类”等反例转为当前SOP。当前记录只有277项，下一增量阈值280不是必须等待的收尾条件；批次关闭前仍按已有规则做不足40项的终局核对。本轮没有关闭批次或改31项WAITING。

## 5. 转换评估系统侧：当前仍有价值的改进

### E1｜P0：孤立请求导致永久busy，缺可消费的恢复诊断

当前平台 `JobService._has_active_job()` 对有request无state立即返回true；`reconcile_interrupted_jobs()`仅遍历state，并跳过不可解析状态。普通提交因此被busy挡住，重启也不能恢复孤立请求。409的action仍要求“等活动job结束”，却没有给出真正的孤立阻断原因。

[1.0.29追加维护记录](../../../../stages/stage1/reports/1.0.29部署与快照更新记录-2026-10-12.md)已经实证：两个旧request无state、API404、health正常，迁出后busy解除。**现场阻塞已在该次维护解除，当前源码防复发缺口仍在**，不是建议再次迁目录。

**平台建议**：提交门禁和启动对账使用同一请求/状态集合；将活动执行、清理未确认、孤立/损坏记录区分为可查询的受限诊断。恢复保持不重放、不删原件、不合成成功，不确认旧调用/清理时继续保守阻断，由获批维护入口处理。健康中的服务可达与可接收新job分列。恢复原件不等于通用job目录枚举权限。

验收需覆盖request无state、坏state、closure_blocked、已终态正常项和并发提交；先用平台获批环境的合成存储记录，不需要危险转换样本。本轮只读已有源码，未编写或运行测试。

### E2｜P1：同一digest字段有两种生产语义，适配不能笼统定义

当前 evaluation-core 的 `compute_digest/build_stream_evidence` 先把CRLF归一为LF再哈希；VM Agent `BoundedStream.consume`则对实际读取字节哈希，`main._bounded_stream_evidence`会用该digest覆盖通用builder结果。comparator的exact直接比较digest。

所以**生产调用路径不同，digest语义可能不同**。当前比较适配 §2“digest已规范化CRLF→LF”的笼统说明不能覆盖真实VM采集路径。已有测试分别保护归一化builder与全流原字节digest，说明不能只改文案后假定所有路径一致。

**建议**：平台明确统一生产契约，保留原字节/文本规范化对象及转换版本；转换适配按实际producer身份解读，不从字段名猜。历史证据不重算覆盖。优先验收只差CRLF、不同编码/非法字节、截断全流digest和普通文本相等四种条件，走实际VM产出链；不只测通用builder。

另外，当前comparison的diff仍使用`stream.normalizedText`、`stream/normalizedText`，未标明stdout/stderr角色。可改善证据定位为精确侧/流/对象引用，减少人工反查；这不改变比较规则或原verdict。

### E3｜P1：程序输出来源与关键路径覆盖仍没有独立证明

当前closure的programOutputProvenance恒为UNVERIFIED；source baseline和comparison均声明不能证明外部driver转发与业务路径。655项平台回归、bundle完整、diff空都不填补这个缺口。

**平台建议**：由获批平台入口采集可关联的启动对象/输入送达/到达观察状态/程序流与装置流来源，而不是靠匹配`DRIVER-FAILURE`字符串判真伪。程序可以合法打印该字符串；静默文件程序也可以工作。先支撑CLI真实入口与可提供的库向量，不立刻建设通用全场景运行时。

现有functional assessment主要验证stdout/stderr结构值和退出码；source baseline对关键非output维度返回unsupported-event-oracle。network/registry能力也未因此出现。需要这些义务时仍按当前缺口分支，不能只请求output后宣称其他行为已通过。

### E4｜P1：分类器精化必须保持保守，不能靠开关掩掉误判

当前分类器v2.4已有裸文件名弱上下文过滤，D2-055旧建议不必重复做；但URL/IP扫描仍缺足够的语句类型/实际使用点归属，Python三引号等内容仍可能作为字符串保留并命中。

续篇建议“排除字符串字面量所有URL”会漏掉真实下载硬编码地址；4.0.0.0形式也可能是合法IPv4地址，不能仅凭四段数字排除。Metasploit References、XML namespace、程序集版本与网络API实参要按上下文区别；动态网络目标继续记未知。

**建议**：逐语言识别资料/元数据与真实网络消费，保留值、原源行及语句/使用点依据；更改分类器需登记新版本/SHA并在获批临时环境验收。仅“回源看像误报”不是`--network-isolation-configured`的事实依据；该开关须真实隔离配置支持，结果变化仍重分类，保留全部原件。当前分类准入§2已规定这一点。

### E5｜P1：小范围诊断可改善，宽泛消噪暂不建议

argv token数组、Windows显式相对入口、csharp语言身份已经在适配中说明，可进一步让拒收/启动错误指出具体字段与值类型。不要自动将单元素含空格字符串拆成命令：它也可能是真实含空格的可执行路径。

长路径归档主要是提交端组装问题，不是样本转换或比较器缺陷。可在现有手工流程选择获准短临时目录，逐件核对应内容后用原生命令打包，不写打包工具或修改源码路径语义。

不建议为求绿增加通用“忽略stderr/耗时/服务状态/archive_bytes”。压缩算法或许可变更属于真实行为/允许差异边界，未必是环境噪声；诊断中相对路径、错误类型和退出码也可能是业务义务。确有需要时另冻精确策略、保留原流及受保护字段，再由平台支持，不事后扩宽旧job规则。

## 6. 建议推进批次与最小验证

| 顺序 | 负责侧与具体交付 | 完成信号 | 本轮状态 |
|---|---|---|---|
| 第一组：纠偏 | 转换契约：限定SOURCE_NOT_BUILDABLE到真实构建失败；工程材料：追加D2-247 tabsize和覆盖纠偏；平台：孤立阻断诊断/安全恢复方案 | 各加载位置口径一致；旧记录保留；孤立存储可被识别且不会自动重放 | 本报告已定位，产品未改 |
| 第二组：补知识 | K2/K3/K4/K5的具体规则，维护在语言/方向/系统真源，根导航按触发可达 | 源触发、版本、行为、反例、未知和本地依据完整；不以测试集当Skill依赖 | 建议待维护 |
| 第三组：检验实际消费 | 既有知识对应和修复覆盖记录；E2 producer契约；E3来源证据 | 精确请求/目标/原件能关联；匹配范围与未覆盖项清楚；原字节与规范化对象可辨 | 未开展动态验证 |
| 第四组：平台体验 | 分类器上下文精化、错误诊断；有实际消费者才扩事件oracle | 真实地址不漏判，资料串误报下降，错误不再被当源编译失败 | 建议待实现与验证 |

最小验证方案均为后续计划，本轮未执行，Agent不新写驱动/辅助程序：

1. **Unicode/容器规则效果**：固定合法源、配置模型、工具链、输入向量及修复预算，只改变被测本地规则正文版本。由合法平台已有入口观察U+0085、Å、行边界、tabsize≤0或两次push后取值；成功信号是相关反例保持源语义，失败信号是只通过默认示例。回收实际请求、目标身份和对应独立证据。
2. **知识适用性落实**：固定任务与工具，只改变一条确有源使用点的规则是否进入本轮适用材料；观察实际请求和定位结果。不能用错误语义或变更安全门禁充当实验变量。
3. **digest生产语义**：固定生产路径、编码与策略，只改变换行字节CRLF/LF。分别核原字节digest与规范化文本结果，再单独做截断/编码条件；成功信号是语义与契约一致、两对象可回读，失败信号是同名字段随producer改变含义而未声明。
4. **孤立请求恢复**：固定合成平台存储，只改变request对应state是否存在。成功信号是API/调度诊断区分孤立与活动、记录保持、不重放且清理未知继续阻断；失败信号是health正常、永久busy且仅提示等活动job。

## 7. 当前文件定位索引

以下仅供本次工程审查按需回读，不进入产品Skill加载链：

| 发现 | 当前依据/建议消费者 |
|---|---|
| F1 构建与运行归因 | [构建前提](../../../../../references/workflow/build-prerequisites.md) §0.1；[任务状态](../../../../../references/framework/task-state-contract.md) §3；[评估准备](../../../../../references/framework/evaluation-readiness-contract.md) §1.1/§1.3 |
| K5 目标惯用写法硬禁令 | [python-to-csharp](../../../../../skills/directions/python-to-csharp/SKILL.md) PY-CS-01/02；任务状态 §2.3 |
| F2/F3 实际知识与修复覆盖 | 任务状态 §2.1/§2.3；[闭环](../../../../../references/workflow/conversion-evaluation-loop.md) §3.2/§4/§6；[长文件](../../../../../skills/workflows/long-file-conversion/SKILL.md) §4.1 |
| E1 孤立请求/状态 | [job_service.py](../../../../../../third-party-evaluation-system/apps/remote-controller/remote_host_controller/app/services/job_service.py) `_has_active_job`、`reconcile_interrupted_jobs`；[jobs.py](../../../../../../third-party-evaluation-system/apps/remote-controller/remote_host_controller/app/api/jobs.py) 两个POST的busy响应 |
| E2 digest生产语义 | [evidence_builder.py](../../../../../../third-party-evaluation-system/packages/evaluation-core/evaluation_core/evidence_builder.py) `compute_digest`/`build_stream_evidence`；[bounded_capture.py](../../../../../../third-party-evaluation-system/apps/vm-agent/vm_agent/app/bounded_capture.py) `BoundedStream`；[VM main.py](../../../../../../third-party-evaluation-system/apps/vm-agent/vm_agent/app/main.py) `_bounded_stream_evidence`；[比较适配](../../../../../references/adapter/controller/comparison-policy-adapter.md) §2 |
| E3 来源与oracle边界 | [job_closure.py](../../../../../../third-party-evaluation-system/apps/remote-controller/remote_host_controller/app/services/job_closure.py) `programOutputProvenance`；[source_preflight.py](../../../../../../third-party-evaluation-system/packages/evaluation-core/evaluation_core/source_preflight.py) `assess_source_baseline`；[functional_assessment.py](../../../../../../third-party-evaluation-system/packages/evaluation-core/evaluation_core/functional_assessment.py) `_read_assertion` |
| E4 分类上下文 | [分类器](../../../../../tools/safety_classifier_v2.py) `strip_comments`、`analyze_behavior`、`_determine_admission`；[分类准入](../../../../../references/workflow/classifier-agent-gate.md) §2/§3 |

## 8. 本轮交付与未验证部分

仅新增本审查报告。既有产品规则、分类器、相邻平台代码、历史汇总/item/events以及其他未提交修改均未编辑。使用原生文件读取、rg定位、单项JSON字段读取及官方资料核验，未编写辅助脚本，未调用转换模型、分类器、编译器或样本；未操作远端Controller/VM。

本报告可作为下一轮按三侧维护的依据，不能充作转换准确率、现役平台通过或批次终态验收。完整目标已删除的项，最终实现和可重放性仍待合法原件；本轮没有伪造或补造这些材料。
