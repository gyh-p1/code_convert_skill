# 全量自审审查第2组：其余56份正式自审

> 2026-10-12。与[第1组](full-review-self-reviews-01.md)合计96份正式对象正文，按磁盘完整清单逐份读取，包括NO-REPAIR文件的风险、scope、未定项；输出截断处补读。D2-247 sr1/sr2和D2-254 sr2沿用本会话前轮已完整读取原件，其余在本轮读完。
> 这里只完成正式自审对象的语义审查。模型响应封装/失败attempt的追溯、277项所有过程材料尚未全量审毕。原目标已删，不把自审转述当精确实现事实。
> 序号接第1组；taskId按manifest/自审自身定位。SR=原self-review轮次。没有proposed_fix的真实疑点也登记，历史原verdict不改。

## 1. 逐文件与条目登记

| 序 | 方向 / case / SR | 建议、风险与未知项 | 本轮处理/知识候选 |
|---|---|---|---|
| 41 | csharp→cpp / D2-116 SR1 | 1条AccessCheck首参DACL/SD错误，建议两处改pSD、LocalFree配对；origin自由文本 | Win32结构身份/返回层次候选已有首轮报告；oracle不确定不否定静态API疑点，但完整版本缺失不宣称已验证缺陷 |
| 42 | csharp→cpp / D2-117 SR1 | 1条Scheduledtasks改大写；凭“通常包含”推源 | 历史说明已拒误报；原源缺失不重新验证大小写。新增事实核验义务已有，不补错误规则 |
| 43 | csharp→cpp / D2-118 SR1 | items空；scope声称SCM稳定顺序、Allow ACE、SID组、状态/StartMode/默认链接等价 | **候选K-L**：权限实际判定与令牌组属性，枚举/服务运行态。顺序/映射须官方与原源；218项相同不证明全部。无自审建议不等于全功能覆盖 |
| 44 | csharp→go / D2-123 SR1 | #1重排autorun位置；#2REG_EXPAND_SZ展开，提os.ExpandEnv或WinAPI | #1历史拒误报；#2展开候选保留，但Go os.ExpandEnv的$VAR形式不能直接替代Windows%VAR%。数组顺序与环境展开分别维护 |
| 45 | csharp→go / D2-124 SR1 | #3仅组SID包含代IsInRole，deny-only说理论；#4null→空串；#10expandSZ未展开；其余9项无修复 | K-L：组存在与有效管理员权限不是天然同义；源真实实现/规格授权需核。null/空串、字符串化、注册表展开与view分别保留；不要因通常DWORD自动豁免公开API |
| 46 | csharp→go / D2-125 SR1 | #2取时点移后；#4Trim/引号/展开顺序改变；#6权利掩码、ACE类型子集；其余无建议 | **候选K-M**：环境展开结果含空白/引号时顺序可变语义；K-L ACE/掩码需官方。计时值可允许不同，操作时点变化是否属于义务另核 |
| 47 | csharp→go / D2-126 SR1 | 1条纠正prompt步长16→12、头count+4、Flags字符串顺序/未知位在scope | K-F可变长结构候选；已知错误提示不能推翻实际ABI。enum显示规则已有，未定义位数字与Flags组合需精确核 |
| 48 | csharp→go / D2-128 SR1 | #7null/空集合/各注册表类型字符串；#8Allow ACL、未驱动；scope写Agent-authored中性main | 记录合法来源/原件需全流程核；注册表GetValue/GetValues/GetSubkeys不同hive默认必须各自保持，不能统一。公共权限函数与5行探针分开 |
| 49 | csharp→PS / D2-130 SR1 | #3源??到IsNullOrEmpty称规格指定；#4Test-Path非法值错误；其余无建议 | 真假/空串/文件类型规则已有；是否获准更改空串行为必须看冻结/请求原件，不能仅信自审“符合规格” |
| 50 | csharp→PS / D2-133 SR1 | #5吞Add-Type错误；#8剪枚举尾/造SecurityInfos shim称无影响；其余6行常量探针 | 公共接口/类型完整性与6值观察分开；shim/缺依赖合法来源待核，不能因未调用而造声明或裁剪源成员 |
| 51 | csharp→PS / D2-134 SR1 | items空；scope覆盖AMSI API、补丁、ReadKey，声明stderr/退出不计 | 当前合法观察不免源副作用/诊断。该声明必须与冻结策略及真实job一致；不据字面“not counted”自行改判/豁免安全 |
| 52 | csharp→python / Dump（022）SR1 | #1嵌入LF与WriteLine CRLF；#4Enum类属性→enum.Enum；#3/#6吞输入异常；其它无建议 | 换行/enum/键输入知识已有；建议enum Full='Full'不自动保留源数值0，类型、数值与显示三层分列。捕获缺控制台异常不能称读键等价 |
| 53 | csharp→ruby / Describe（023）SR1 | #1遗漏WriteLine换行；#2基线尾CRLF疑点；#3错误分支换行；#8getch；#6hex/to_i/base64空白差异 | 四建议逐条保留。#2先核采集，不能反向改源语义求贴基线；**候选K-N**：严格数值/base64空白与异常接受域。Ruby to_i与Integer区别已有，具体Base64仍需核 |
| 54 | go→c / admin-presence（033）SR1 | agent-static；RFC3339 mktime偏移不稳；fopen权限与Go0644 | **候选K-O**：时间取值/时区/格式分开；文件create mode与umask/已存在权限分开。output-only未验元数据 |
| 55 | go→c / b64-hash（034）SR1 | agent-static算法模拟；24字节只mod0；多字节reverse未验；TMPDIR尾/JSON排序 | Base64补位/摘要输入对象/真实行为分列，不把模拟当运行。无确定性新缺陷 |
| 56 | go→c / cred-mask（035）SR1 | #1NUL截断；#2JSON转义缺；#4Join Clean缺；#7Scanner64KiB/目标MAX_MAP100；#9fdopen/关闭时点 | **候选K-P**：扫描器容量/停止与容器容量改变；JSON编码接受域；C字符串显式长度。defer到块末不能一律等时机，源生命周期规则已有 |
| 57 | go→c / host-net（036）SR1 | #2U+2028/非法UTF8未实现；#4CGO/NSS；#7时区负小偏移；#8路径Clean；其余正常 | K-O/JSON候选；**候选K-Q**：用户查询CGO/NSS与环境依赖。源码默认构建不能证明CGO实际开关，须平台原件 |
| 58 | go→cpp / chunk-upload（041）SR1 | #3极简HTTP子集；#7HTML/Unicode转义缺；#8半写互等；#9写死/tmp；#10权限；#11源panic目标0 | K-C/K-P/K-O再现；硬编码/tmp是实现改变而非纯环境根因。冻结默认有效仍保留公共义务未覆盖。服务关闭及partial IO知识已有 |
| 59 | go→cpp / redact-quality（039）SR1 | #7不稳定→stable排序；#8非法UTF8；#9Join Clean；#10chmod替代create mode | **候选K-R**：稳定性/同键记录的次序，不用唯一键fixture外推。chmod会修改既有权限，是源目标映射问题，不能只记环境 |
| 60 | go→cpp / ext-inventory（040）SR1 | #3Unicode lowercase→ASCII；#5mask/地址prefix；#8DEL/JSON；#10路径；其它无建议 | **候选K-S**：Unicode大小写精确集合、网络地址/prefix表示。DEL转义真假须官方；“Ä.TXT”中非ASCII不在扩展名，原例证不能证明提出差异 |
| 61 | go→cpp / gzip-replay（037）SR1 | #2固定gzip码流；#6解码仅stored/fixed子集；#11/tmp可选修；#12chmod；其它自洽 | **候选K-T**：压缩同字节与解压同语义分开；编码/解码同源自洽不是独立正确性。子集解码保留真实缺口，不用固定输入匹配宣布完整库等价 |
| 62 | go→cpp / token-probe（038）SR1 | 9条无建议；Linux只nonwindows；map/struct序、时间、JSON、路径 | 已有知识；平台分支与完整接口覆盖分列。Windows声明/子进程路径未验证 |
| 63 | go→cpp / process-pipeline（042）SR1 | #1exec失败127/-1；#2WaitDelay近似/超时<1ms；#3waitpid错→0；#4UnicodeTrim；#6JSON；#8平台；#9耗时 | **候选K-U**：启动/执行/等待失败、信号退出/超时、双管道/截止值不可混同。耗时可消噪不授权消去timed_out或状态差异 |
| 64 | go→cpp / tcp-scanner（043）SR1 | 10条无建议；非阻塞connect/poll300ms、四worker、stop-pipe、真实耗时 | 网络/并发规则已有；deadline和就绪必须真实证据，值噪声与控制超时义务分开 |
| 65 | go→cpp / smb-prober（044）SR1 | #3并发→串行；#4单次SO超时对总deadline；#8耗时；#9端口认消噪；其它无建议 | K-U：每次socket超时不自动等绝对deadline；并发变串行仅单client未露。端口动态先关联资源，不信自审“本平台已覆盖” |
| 66 | go→cpp / tree-zip（045）SR1 | #3允许STORED/顺序；#4共同CRC实现；#7nil→[]；#8随机目录/时间/大小；828目标行 | K-T/JSON候选；许可是否真实冻结待全流程。ZIP有效性需独立读取/成员语义而非单看archive_bytes；超计划长例不冒称范围内验收 |
| 67 | go→cpp / c2-controller（046）SR1 | #1shutdown值硬赋“expected true”；#7ASCII字节reverse代rune；其它7条无建议 | **候选K-V**：清理/关闭状态不能靠常量模拟测量；rune/字节反转知识需实际输入。源内部值被写死是候选转换问题，不仅输出相同就免 |
| 68 | go→cpp / chunked-http（047）SR1 | #8删临时文件往返/错误1–3；#10关闭恒true；#11路由/限制/JSON子集 | K-V/K-P：删除文件副作用与输入限制真实改变，不因stdout-only豁免。包内归因需核允许改动，不直接修原源码 |
| 69 | go→csharp / D2-194 SR1 | exec漏臂建议；risk又说未看原源“implausible” | 分派完整性知识已有；原建议没有精确源臂证据时不能只由help/helper反推。历史汇总的确定性措辞需降到证据支持范围 |
| 70 | go→PS / D2-199 SR1 | items空；-f hex默认host/port下输出；非冻结参数未覆盖 | 记录已读；无知识候选，生成的载荷字节/端口patch边界需后续过程证据 |
| 71 | go→PS / inbox（052）SR1 | agent-static；Trim/SplitN、序数排序、JSON转义、empty未触发 | 空白/分割规则已有；.Trim与GoTrimSpace集合不自动一致。BOM/文件内容须实际证据 |
| 72 | go→PS / overwrite（053）SR1 | 5条无建议；真实SHA读回、JSON/布尔/唯一输出 | 状态初态、目标/备份文件原件核后方可计行为，不把声明“真实”当采集证明 |
| 73 | go→PS / parallel-cmd（054）SR1 | #1stdout/stderr分别取再拼代CombinedOutput；#4顺序收集计时 | **候选K-W**：流交错顺序与拼接不同，默认无stderr隐藏变化；计时包括前序等待是实现时点改变，可允许展示值不同但需保留定义 |
| 74 | go→PS / staged-config（056）SR1 | agent-static；UTC Z/RFC3339未全；文件无BOM；time需消噪 | K-O；精确时区非零/零分支分别核；消噪允许时间值不代表格式/时区表达可随意改 |
| 75 | go→python / D2-207 SR1 | 空索引panic2与IndexError1；建议改码、可保留traceback | 错误退出映射已有；stderr外形可明确允许，但不能自动被当装置。缺“issue”字段须来源与格式核 |
| 76 | go→python / autorun-backup（057）SR1 | 6条无建议；map序与entry序、RFC3339Z、双文件 | K-O/JSON已有基础；Pythonjson与Go转义接受域、错误处理仍需源使用点，不只ASCII默认 |
| 77 | go→python / child-cmd（058）SR1 | agent-static CombinedOutput中继；错误替换文案；tempfile.gettempdir=GoTempDir断言 | **候选K-X**：临时目录候选/有效性/缓存机制，两个API不因默认目录相同天然等价。启动错误文案可模式化，错误类型/状态必须保留 |
| 78 | go→python / concurrent（059）SR1 | #1声称并发收集但只推统计；#2/3/4struct序/omitempty/nil；#5时间 | JSON字段省略/null/空集合候选；并发时序未被6项内容证明，需实际流程原件 |
| 79 | go→python / manifest-zip（060）SR1 | 6条无建议；DeflateZIP/文件hash、manifest；不要求archive同字节 | K-T：可接受压缩字节不同但核成员/内容/重复/路径；已核许可才可以消archive差异，不推成全ZIP豁免 |
| 80 | go→ruby / inbox（061）SR1 | 两建议：缩Go空白集、加TMP/TEMP候选 | **两条技术前提错误**：Go IsSpace含非Latin1Unicode空白；UnixTempDir主要TMPDIR fallback，不是三环境变量顺序。不能把driver修复matched当这两条正确性裁决；当前语言页已有事实 |
| 81 | go→ruby / ack（062）SR1 | 6条无建议；strip/split3、checksum、Queue、动态端口、JSON序 | 空白/分割/校验不同接受域仍需精确源，不从ASCII报文外推；端口关系可以消噪，消息checksum/ACK义务受保护 |
| 82 | go→ruby / tcp-receiver（063）SR1 | #8conn.read异常→nil而Go保留部分bytes；其余7项无建议 | **候选K-Y**：部分读取结果与error分别处理；不要扩大rescue范围吞部分数据。错误路径保持规则已有但具体read语义需补 |
| 83 | go→ruby / notes-zip（064）SR1 | 1条mkdir_p(mode755)去chmod，既有权限不改 | 属真实转换疑点，即使正常umask下match。权限初态/创建/修改义务在文件知识维护，不只“未观察就误报” |
| 84 | python→cpp / D2-247 SR1 | 6条hyphen+1、condC反、indent predicate、NEL、splitlines、wrap/fill签名 | 6条分别登记；前5候选，裸0x85建议不充分；签名差异须核调用能力/默认值/kwargs，不一概豁免 |
| 85 | 同项 SR2 | 2条统一UTF8、tabsize<=0保留tab；后者标source-preexisting | UTF8候选；tabsize建议已官方核错，保留原条目+更正，origin不改原件 |
| 86 | 同项 SR3 | items空；scope再次错误称tab保留正确；Unicode全集/非ASCIIwidth未审 | **连续两轮重复错误前提**，说明复审不独立；matched dedent不验证这项。空items文件也留纠偏条目 |
| 87 | python→csharp / D2-254 SR1 | PB-01 Stack→Queue；EX-01异常类型；API-01string入口 | **PB-01误报导致回退**：appendleft+popleft是LIFO；异常/输入重载候选须保持catch消费者和空参义务 |
| 88 | 同项 SR2 | Queue错，改Stack/头插 | 正确方向候选；同一问题反向建议原理由须裁决，不能只信后轮标签。已有请求来源/修复预算要继续核 |
| 89 | 同项 SR3 | items空；pushback/_pushback_chars/filestack顺序；非BMP/并发未覆盖 | 容器端点、token字符与stack生命周期分开；45字节正常parse不证明多次pushback反例 |
| 90 | python→go / D2-256 SR1 | opt-abbrev、opt-missing-arg-msg，argv[]未触发 | 当前argparse/getopt不等optparse；**候选K-Z**：具体optparse唯一前缀/歧义/缺参规则，词条按解析器而非语言泛化 |
| 91 | 同项 SR2 | items空；两修静态确认，未复算PE偏移 | 不借usage匹配宣布PE读写正确。将两反例与目标修复版本关联，不需额外无限自审 |
| 92 | python→PS / 11_10（066）SR1 | agent-static；网络counter delta；psutil/.NET接口集合不同 | **候选K-AA**：计数定义/接口筛选是源目标语义，不能一概消为主机噪声；可允许采样值变化，但时间窗/集合/增量关系须核 |
| 93 | python→PS / 16_28（067）SR1 | agent-static；称[int]小数截断等floor，score13；文化/xrandr | **整数转换断言错误**：PS实数→整数nearest-even，不是截断；正数也会与floor不同。候选补“整除/强转/四舍”明确区分，保留xrandr输入/子进程义务 |
| 94 | python→PS / 23_27（068）SR1 | agent-static；Create无权限gate，其他3臂有；正常只Create | 分派/权限门控结构检查已有；3个未触发分支记录UNVERIFIED，不按“都写了”称全行为保持 |
| 95 | python→ruby / D2-269 SR1 | items空；只拒绝连接路径；fd重定向/恢复/交互未验 | 进程/网络/标准流规则已有；当前拒绝路径match可算该范围比较通过，不代表连接成功路径 |
| 96 | python→ruby / D2-270 SR1 | items空；只无index数据1178B；有数据推荐/解析未验 | JSON/文件规则按实际源触发；无数据错误路径可有效，但不代数据处理功能 |

## 2. 三个新增的错误自审断言

这部分是维护核验，运行Skill所需事实仍要落本地正文；本轮未运行样本。

1. D2-067认为PowerShell `[int]($score/10)`对正数等价Python floor。官方说明实数转整数使用nearest-even；score13/10碰巧一致，不能外推。例如1.5到整数是2，而floor是1。[PowerShell类型转换](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_type_conversion?view=powershell-7.6)。
2. D2-061认为Go的IsSpace只覆盖Latin-1八字符。官方区分Latin-1专用集合与更大Unicode集合；当前Go语言页也已说明White_Space。候选建议不能缩集合。[Go IsSpace](https://pkg.go.dev/unicode#IsSpace)。Unix临时目录候选的错误断言与该项driver故障应分开归因。
3. D2-177 SR2认为Pythongnu_getopt不受POSIXLY_CORRECT影响。Python3.12官方明确环境变量与前导+控制是否停止；当前Python语言页已有正确规则。[Python getopt](https://docs.python.org/3.12/library/getopt.html)。

另外两类已在前轮核：D2-247 tabsize≤0建议错误；D2-254首次pushback建议与其自己引用的端点操作矛盾。均不能靠后轮NO-REPAIR或默认matched洗掉。

## 3. 知识侧审查结果的边界

**96份正式自审对象中的建议、scope、风险和未定项已浏览并在两组登记。** “记录为知识候选”不等于全部应新增正文，更不等于历史转换缺陷已经坐实。需补充的具体API事实、已有规则没落实、错误建议、版本/来源缺口分别处理。

下步仍是全量工程审查：每一项全部请求/响应、分类/冻结、所有job与失败attempt、两侧观察/副作用/比较/清理和result，再将每个知识候选与当前正文及原始独立证据逐条对照。模型内部reasoning正文不作为自审结论；响应封装核真实content、finish_reason、模型/用量/attempt及正文关联，空content截断不能转成有效自审。
