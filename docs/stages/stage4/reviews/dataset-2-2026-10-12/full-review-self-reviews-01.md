# 全量自审审查第1组：C/C++源及C#→C

> 2026-10-12，范围为下表40份正式自审对象。人工读自审全部条目/风险/未定项；工具截断处单独补读。该组尚未逐件核模型外层响应和所有评估attempt，不能记该40项工程产物已全量审毕。
> 记录“没有修复建议”也不等于没有语义缺口。原verdict保留；下表是知识候选/审查意见，不是编译或功能改判。
> `sr1/sr2`为原`03-self-review/self-review-N.json`。路径按原manifest的方向和case定位。原始代码已删除，源/目标引用只作历史定位，不补造实现事实。

## 1. 逐文件/逐问题登记

| 序 | 方向 / case（taskId）/ 文件 | 原建议与未定问题（保留条目定位） | 本轮处理与知识落点 |
|---|---|---|---|
| 01 | c-to-cpp / c01-linux-win-network（024）sr1 | agent-static；realloc void*强转、char*字面量强转；无修复；1318行，网络未验证 | 已有C→C++类型/字面量规则；char*强转不证明写入安全。人工自审来源与配置模型来源分别核，超计划长文件范围不外推 |
| 02 | c-to-cpp / chain-reactor-network-linux（025）sr1 | agent-static；5文件唯一calloc强转；原CRLF输出LF、行为静态未验 | 已有转换/完整源集合规则；源文件换行与运行输出换行分开；需核五文件版本与语言门禁来源 |
| 03 | c-to-cpp / stest-fs-posix-to-win（029）sr1 | agent-static；new→newer三使用点；称“compiles as C++” | 关键词改名已有；没有独立build不能从这句取编译PASS；全部选项/隐藏文件/退出路径只有静态对照 |
| 04 | c-to-cpp / D2-151 rm sr1 | #1–10原样/无修复；#11 BSD声明/传递signal头可见性未知；多未覆盖分支 | 不因文本原样自动认为C++可编译；构建前提现有，补具体平台声明依据须真实诊断。source-preexisting被用于“没问题”是标签滥用，不生成源缺陷计数 |
| 05 | c-to-python / D2-174 FEAL sr1 | #1–11无修复；32位截断、读写顺序、小端、隐含NUL、填充、hex格式；未用移位UB | 已有整数/字节/NUL规则；保持计算次序与显式宽度，不因算法输出匹配改未使用UB路径。无新确定性规则 |
| 06 | c-to-python / environment（031）sr1 | #2 A/W/输出代码页/best-fit未知；#3 UTF-16步进；#5新增free；#6宽泛except吞失败/NULL静默；两项unresolved | **候选K-A**：环境块特殊=项、顺序、A/W与stdout编码分别冻结；不能从默认VM推定ASCII。#6即使无修复建议也登记错误路径变化，沿用已有错误传播规则补真实触发；新增free是否许可按源生命周期 |
| 07 | c-to-python / D2-176 pwd sr1 | #1/#7未知选项缺libc诊断，建议补；#2–6usage/逻辑cwd/PWD/失败顺序无差异 | getopt诊断规则已有；文案未知先待核，不照抄示例。stderr表现可以是允许差异但须保留错误类别/退出码/顺序。相同usage只验用法错误路径 |
| 08 | c-to-python / D2-177 which sr1 | #3/#4字节长度；#7诊断；#12GNU重排；其余8项无差异 | 四条分别登记：字节长度2处已有；GNU重排已有；libc精确文案待证。别把两处长度合并后漏一处源使用点 |
| 09 | 同项 sr2 | #1/#2长度修复、#3重排确认；POSIXLY_CORRECT断言称gnu_getopt始终重排；#8及unresolved诊断仍缺 | **需核自审技术断言**：当前Python语言页已说gnu_getopt受POSIXLY_CORRECT/选项串影响，后轮自审相反不能采作事实。#8surrogate输出失败另记覆盖缺口 |
| 10 | c-to-ruby / D2-180 rc4 sr1 | #1 argc守卫、#7程序名fallback建议修；#2–6/#8算法/原字节输出无差异 | argv基数规则已有；两建议均保留位置；不能把程序名差异一律豁免。RC4向量结果与公共API全覆盖分开 |
| 11 | c-to-ruby / D2-181 speck sr1 | #1–7无建议；64位环绕/旋转、更新顺序、LE64、sizeof NUL、padding、格式 | 已有宽度/字节规则；固定输入成功不证明所有轮函数边界。当前审查不增加新知识 |
| 12 | c-to-ruby / linux（032）sr1 | #4 fork nil误失败；#6空环境/exec失败码；#8同因退出；#5reopen细节未知；其余守卫/重试/默认路径 | fork/exec/环境规则已有；#4与#6各留一条，#8关联不重复计。#5fd复制/关闭生命周期候选待官方依据。仅默认guard不可用于验证连通分支 |
| 13 | c-to-ruby / D2-183 realpath sr1 | #3任务usage误写；#8libc非法选项文案；#9PATH_MAX限制缺失，无修复建议；其余无差异 | **候选K-B**：定长realpath缓冲与自动字符串长度界限/错误义务。文案未知已有规则；任务提示不能覆盖源；#1 argc示例自己有计数疑点，待原件，不当事实 |
| 14 | cpp-to-c / chunked-manifest（001）sr1 | #1–9无建议；#5partial send计数描述自相矛盾；#10 OOM源抛而目标发送部分数据 | **候选K-C**：分配失败的传播/输出/退出，不因“低概率环境”排除转换差异；网络场景已有部分发送规则，先确认源n>0真实语义，不能顺手修源算法 |
| 15 | cpp-to-c / elevation（002）sr1 | items=[]、无未定 | 记录已读；只有范围文字，不产生知识候选，不能推定各支路动态通过 |
| 16 | cpp-to-c / env-discovery（003）sr1 | #1递归mkdir失败源抛目标忽略；#3枚举上限；#4 getenv借用；#6ANSI/printf工具链 | **候选K-D**：fs错误传播、借用环境指针生命周期、Win32枚举编码。两级mkdir不支持“只有≥3级才失败”的一般结论；递归深度由具体逐级创建决定 |
| 17 | cpp-to-c / fake-cred-loader（004）sr1 | #1rb→r修复CRLF空行；#2EOF补行；#3/4exists/目录；#5格式；#6无其它 | 文本模式知识已有；仅换CRLF配对不能删除孤立CR；文件内容/loaded分支独立于无文件probe |
| 18 | 同项 sr2 | #1修复与#2/3反例确认；#4 EOF/失败；#5Ctrl-Z/竞态；无未定 | 仍是静态反例，不冒称第三方运行。Ctrl-Z文本EOF是候选平台细节，须具体运行时/版本后补到语言/文件页 |
| 19 | cpp-to-c / local-c2-ping（005）sr1 | #1固定inet_addr/inet_pton；#2NUL安全；#3–10长度/资源/条件编译，无修复 | 已有字节/网络事实；只适用合法固定IPv4，不能推广inet_addr等价。无监听分支不覆盖收发 |
| 20 | cpp-to-c / xor-codec（006）sr1 | #1–9符号/空分段/join/长度/别名/延时；#10OOM失败源抛目标0；#11无建议 | K-C再现；不能把OOM因不在探针里就降成“无风险”，保持未覆盖即可。空分段语义可与已有字符串分割知识对应 |
| 21 | cpp-to-go / inbox（013）sr1 | #1CRLF/LF/末尾CR/EOF；#2–7文件/失败/输出，无修复 | 读取终止符集合已有；不是泛化trim所有CR。路径对象为目录/权限失败仍需精确错误路径 |
| 22 | cpp-to-go / shell-output（014）sr1 | #1少一cmd层但固定命令无差异；#3读错当EOF；#6Wait/丢弃状态，重复proposed_fix键 | 进程场景已有；**候选K-E**：解析层数与元字符/引用，固定echo不证明所有shell替换等价。重复JSON键保留原件/格式疑点，不靠解析器最后值静默通过 |
| 23 | cpp-to-go / token inspector（015）sr1 | #1–6消息/API探测；#7 TOKEN_PRIVILEGES偏移4/步长12；#8–12读权限/LastError/defer/退出，无修复 | **候选K-F**：可变长结构头/元素步长、返回buffer长度核界；需ABI版本/官方依据；printf/API指针宽度已有基础但具体Win32结构缺正文 |
| 24 | cpp-to-powershell / D2-088 resource sr1 | findings两条：agent_config.json与pipeline.dot LF→CRLF；appliedTo v2，未复审 | 两文件分别保留修复定位；文件内容模式义务与stdout消噪分开。机械补丁/父版本与复审记录需全过程核 |
| 25 | cpp-to-powershell / D2-091 process_enum sr1 | #1缺参UB；#2退出中继未知；#4ProcessName+.exe/竞态/Dispose；#5源/目标越界长度变化；#6Add-Type | **候选K-G**：托管PInvoke缓冲容量与长度分开；源UB不能证明目标越界“效果等价”。进程枚举名字/资源/竞态待核，不只默认未命中。退出码中继属装置 |
| 26 | cpp-to-powershell / D2-092 winhttp sr1 | #5/#6删除printf_pid残留；#4隐含NUL缺1；#1/2atoi/缺参；其它无建议 | 残留控制流标签/NUL/atoi已有；#4未观察仍记。关于CommandNotFound一定终止的断言需结合ErrorAction/host核，不升级通则 |
| 27 | cpp-to-powershell / D2-093 inject sr1 | scope/location/evidence/proposed_fix/risk缺；#1注册表view/权限/类型；#2空白集扩大；其它称一致 | 记录7条均已读，必要记录缺失不能拿verdict放行。候选：32/64注册表视图、读取类型与KEY_READ；空白规则已有但具体C isspace/PS集合须按版本 |
| 28 | cpp-to-powershell / loopback-send（016）sr1 | #4LF→CRLF建议；#1加载DLL不等WSAStartup；#2宽catch；#3/5/6/7无差异 | 换行已规则；**候选K-H**：库加载与子系统初始化错误时机不可互代；默认拒连接成功不验证WSA失败 |
| 29 | cpp-to-python / D2-095 retry sr1 | #2_socket初始化异常类型未核；#3send→sendall；其余默认无监听无差异 | K-H/Python初始化候选；sendall是行为变化而非天然修复，即使本输入不触发。网络部分I/O规则已有 |
| 30 | cpp-to-python / D2-096 bundle sr1 | 必要字段缺；#2强制排序；#7symlink/is_file/错误0/孤立CR/不可读抛；其它无建议 | **候选K-I**：遍历、链接、错误与顺序的独立义务。未指定顺序不等于可无条件排序；file_size失败返回值、io异常须回源核。不能因output-only漏掉文件义务 |
| 31 | cpp-to-python / D2-097 evil sr1 | #1–8argv/atoi/流/ctypes/payload无修复；缺参UB/未用buffer路径 | 字节/NUL/atoi/API宽度已有；不能无效PIDprobe证明API成功路径。无新确定性规则 |
| 32 | cpp-to-python / startup-cycle（019）sr1 | #3读首行state；#4 stdout换行不确定；#5刷新等价断言；其余创建/CSV无问题 | 状态机初态/重复运行须覆盖；文本层换行事实需按准确启动/平台核，不能将逐行flush与退出时flush当服务时序等价 |
| 33 | cpp-to-ruby / D2-103 host_env sr1 | agent-static；称C getenv unset或empty都unknown；cwd集合/污染风险 | **需纠正/核原源**：C getenv指针非NULL但空串通常不触发?:fallback；该自审文字自行矛盾。当前真假/空串页已有，不新增错误规则 |
| 34 | cpp-to-ruby / D2-104 rename sr1 | agent-static；双向重命名/changed；状态初态、文件内容未比 | 文件场景已有；输出布尔不证明文件内容/重命名目标，记录未采filesystem |
| 35 | cpp-to-ruby / D2-105 rollback sr1 | agent-static；3seed、append日志、count；状态/内容未比 | 与34分别留文件级条目；不因同族跳过该项。append历史初态与副作用范围必需 |
| 36 | cpp-to-ruby / D2-106 manifest sr1 | agent-static；File.directory?不等exists；路径/枚举顺序未比 | K-I再现；exists/type/缺失/符号链接分别核；stdout count不能验证manifest正文 |
| 37 | cpp-to-ruby / kv-audit（020）sr1 | agent-static；split/重复键/hash缺省/优先级；只accept/日志未比/CRLF未验 | **候选K-J**：分隔符保留空字段/首个=/重复键覆盖/分支优先级。源map默认插入与Ruby Hash.new默认返回不自动同义，须消费者是否看成员集 |
| 38 | cpp-to-ruby / loopback-ack（021）sr1 | agent-static；Linux只windows_only；Win分支retry/收发未验 | 不产生新确定性规则；OS门控通过只证明未运行分支。不得把“实现形状存在”当Windows转换能力 |
| 39 | csharp-to-c / D2-109 FileUtils sr1 | #1递归异常层级；#3ASCII排序；#5fixture末清理未知；#6默认库链接；#7非驱动函数错误变化 | K-I/K-D；异常停止哪层决定兄弟遍历；工具链默认链接只凭实际命令/证据；动态输入/fixture来源必须后续全材料核 |
| 40 | csharp-to-c / D2-111 PE sr1 | #1–4输出/结构；#5删Console.ReadLine；#7静态宣称可编译；origin自由文本 | **候选K-K**：EOF默认输入不授权删除读取/交互义务；已有关键输入规则须补ReadLine触发。类型布局未观察不归ABI通过；自审编译断言不独立取信 |

## 2. 该组可回收的知识候选

候选不直接进入Skill正文；先与当前精确条目对照，再由维护侧核源语义/官方版本，避免把模型断言固化。

- K-A：原生环境块、空值/特殊项、A/W/best-fit与输出编码、异常吞掉。
- K-B：固定长度路径缓冲的错误义务与自动扩容表示。
- K-C：C++异常到C返回码时，OOM/读取部分结果与退出不能靠默认小输入免除。
- K-D：filesystem错误传播、递归创建、环境指针/枚举编码。
- K-E：子进程shell解析层数、引用/元字符、等待与退出转发。
- K-F：Win32可变长结构的头偏移、元素步长与界限。
- K-G：互操作缓冲区容量、长度、隐含NUL与源UB处理。
- K-H：加载动态库、语言模块初始化和WSAStartup不是相同失败阶段。
- K-I：目录遍历/符号链接/异常层次/文件类型/顺序分别保持。
- K-J：token分割/首个分隔/空字段/重复键覆盖及默认插入的消费者义务。
- K-K：源暂停/输入不能因冻结EOF而删除，接口保持与观察范围分开。

## 3. 全过程尚未核完的范围

本组没有把40份自审都认作模型独立产物：其中多份明确`agent-static`，外层请求/响应须另核。NO-REPAIR下存在真实候选、自由文本origin、无必要字段、静态编译断言及未覆盖风险；不能仅按verdict提取REPAIR文件。

尚需逐件：自审原响应和格式恢复；请求实际知识版本；最终/父目标删除造成的对应缺口；各评估attempt两侧真实流和副作用；分类/冻结/授权/清理；原item与events/result一致性。当前材料读完的40份自审不替代这些范围。
