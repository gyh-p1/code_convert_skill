# 全部自审建议的知识维护去向

> 维护续接：2026-10-12本轮定向修订已落盘，C-K1/C-K2及引导补充的当前结果见[修订交付](revision-result-2026-10-12.md)。下文保留初审时点的定位/候选和“未修改”说明，不将其改写为当时已经修订；未进行动态验证。

> 读取覆盖：96/96份正式自审正文，逐文件/逐条记录见[40份](full-review-self-reviews-01.md)和[56份](full-review-self-reviews-02.md)。本表汇总维护去向，不代替原条目。
> 当前对照只在本轮实际读到的语言/方向/场景/系统正文上判断；“仍需核”不表示穷举全库证明不存在。原源/目标已删，未经全过程和版本化依据支持的模型断言不直接写入Skill。
> 本轮只新增审查文档，未修改知识真源，未运行测试。

## 候选逐项去向

| 编号 | 建议簇 | 当前已读正文/规则的覆盖 | 维护去向 |
|---|---|---|---|
| K-A | 原生环境块/特殊=项、A/W、best-fit、编码、异常 | C→Python字节规则、C#/PS UTF-16基础和错误保持已有 | 通用规则已有；Win32环境块特殊项/精确编码/指针生命周期需补版本化API事实，不按默认ASCII猜 |
| K-B | realpath固定缓冲与自动字符串错误界限 | POSIX-Windows文件系统替代接口/长度上限有规则 | 先核C/POSIX源函数容量和错误；补同OS高层替代时的固定容量义务，不能将跨OS页面当全API覆盖 |
| K-C | C++分配异常→C部分成功/零退出 | C++ L1-CPP-04、C++→C规则2已要求异常/错误传播 | 优先落实已有规则；补隐式库分配失败触发和“资源不足不决定origin”反例，勿另造全局OOM强测门禁 |
| K-D | mkdir、filesystem失败/环境借用/枚举编码 | FILE-02、C++ L1-CPP-04有失败条件；借用/Win32枚举具体事实待核 | 递归/末级创建已有，补具体接口及生命周期；纠正“路径层数决定能否创建”的错误泛化 |
| K-E | shell解析层、元字符、等待和退出转发 | 进程场景与进程系统页明确直接argv/shell、解释器、双流和等待 | 落实；只有具体解释层丢失的源/目标证据才添方向例，不把固定echo扩为通则 |
| K-F | TOKEN_PRIVILEGES/可变长原生结构布局 | 系统页有令牌语义，但已读正文未提供该结构详细布局 | 补精确SDK/架构/字段宽度/数组边界；4+12等数值不能脱离本结构版本泛化为所有结构 |
| K-G | 互操作缓冲容量/长度/NUL、源UB | C字节/NUL、Winsock长度收窄规则已覆盖基础 | 具体托管PInvoke和nSize/容量关系仍需核；源UB既不证明目标等价，也不授权改源功能 |
| K-H | DLL加载、语言模块初始化、WSAStartup失败时机 | Winsock页明确使用前初始化及WSANOTINITIALISED | 补方向侧运行时初始化/加载与API初始化区别；非Windows或同OS只消费实际触发事实 |
| K-I | 遍历/链接/异常层次/文件类型/顺序 | 文件场景、文件系统系统页及C++错误页已有 | 优先落实；补消费者需要的细节，不凭无序枚举推出可无条件排序/扩大跟随链接 |
| K-J | 分割端点/空项/首个=/重复键/默认插入 | 已有容器/真假/字符串基础；确切split API仍需逐源使用点核 | 保持默认插入是否改变成员集等细节；多轮pushback错误单列裁决，勿因建议次数多提高可信度 |
| K-K | ReadLine/暂停与EOF、公开接口 | C# ReadKey、Python终端页已有输入单位；通用契约禁止删功能 | 落实；补“冻结EOF不授权删除调用”反例，缺合法输入条件走现行仅编译分支 |
| K-L | AccessCheck/有效令牌组/deny-only/ACE/服务枚举 | 进程身份与Windows子系统页有模型、权限/状态义务 | API级有效权限判定、结构身份与枚举映射仍需补；不能用组SID包含代实际IsInRole/AccessCheck |
| K-M | REG_EXPAND_SZ、引用/Trim/展开顺序 | Windows子系统页区分展开与原始类型 | 需要具体.NET/Win32行为与方向；Go os.ExpandEnv不直接当%VAR%展开替代；保留展开前后顺序 |
| K-N | 数值/Base64解析严格性、空白/异常域 | Python/Ruby字节与数值基础已有 | 补精确函数的接受集合；Python b64decode默认discard、validate=true与Ruby各解码API不能同名套用 |
| K-O | 时区/格式/取时点/时间间隔、create mode/umask | Go→Python时间规则已有；文件场景区分权限模型 | 时间值消噪与格式/取值定义分开；同OS创建权限与修改既有权限的API细节需补 |
| K-P | Scanner停止上限/容器上限、JSON编码、生命周期 | Go error/Scanner.Err与defer、C显式长度已有 | 补token长度限制、部分扫描结果、固定100项容量等具体边界；JSON转义/非法UTF8独立维护 |
| K-Q | os/user、CGO/NSS、环境 | 已读身份系统页不等Go os/user后端规则 | 补真实后端与构建开关依据；不同查询来源是否影响用户结果须任务事实支持 |
| K-R | stable与unstable同键顺序 | 现有通用集合/顺序义务不能代具体sort事实 | 核具体排序函数稳定性/相同比较键消费者，再补小例；只有冻结唯一键不能证明所有输入 |
| K-S | Unicode大小写/非法字节、网络prefix表达 | Go/Python/C#字节与字符单位已有 | 补具体lowercase API和地址表示；原例扩展名不含非ASCII时不能证明差异 |
| K-T | gzip/ZIP合法性、独立解码、成员/CRC、字节vs内容 | 文件场景归档清单/EOF/CRC/内容oracle已有 | 优先落实；补只实现stored/fixed子集的能力边界；不要求压缩包同字节，也不以同源编解码自洽代合法性 |
| K-U | 启动/等待失败、截止时间、SO每调用超时 | 进程场景、Go→C++ WaitDelay和网络页基础已有 | 补每操作超时vs绝对deadline的具体方向例，允许展示耗时不同但保持取消/超时/退出状态 |
| K-V | 清理/关闭结果硬编码、删除文件往返 | 资源清理/失败和禁止删功能已有 | 属落实/定位证据问题；不能靠常量true通过oracle，不因stdout-only免原副作用 |
| K-W | CombinedOutput交错vs先分别采再拼 | 进程场景流捕获表明确分离/合并/顺序/双流排空 | 已有义务；补语言方向具体API与两流交错反例即可，不新增装置脚本 |
| K-X | TempDir候选/检查/缓存 | Go L1-GO-07与Ruby L1-RB-09有正文 | 纠正Go→Ruby错误建议，已有正确事实不能被后轮“匹配”推翻；Python tempfile缓存/校验仍需版本核 |
| K-Y | 部分bytes与error不丢失 | 网络页部分读取/EOF已有，Python→Go方向明确n与err同时处理 | 补Go→Ruby读取异常下部分结果细节，不能横跨方向机械套；不扩大rescue范围 |
| K-Z | optparse缩写、歧义、缺参 | Python参数页仅有通用解析器义务 | 补optparse特定接受域/退出/诊断，不把argparse/getopt事实当optparse；PE部分另核不借usage通过 |
| K-AA | 系统/接口计数器集合与增量窗口 | 战术索引明确其余主机/环境枚举仍缺口 | 补实际psutil/.NET API的数据定义与接口筛选；采样值可容忍，计数定义/时间窗变化不自动消噪 |

## 已明确拒绝直接固化的建议

- D2-247：tabsize≤0“保留TAB”错误；默认dedent matched没有验证此反例。
- D2-254：appendleft+popleft推FIFO并将Stack改Queue错误；后轮纠正不是对首次建议的独立动态证明。
- D2-061：把Go IsSpace缩为Latin1集合、UnixTempDir增加TMP/TEMP的建议与现有正确知识冲突。
- D2-067：PowerShell `[int](a/b)`被当作floor/截断错误；当前PY-PS-04已明确nearest-even及15/10反例，应落实而非重复新增。
- D2-177：gnu_getopt“不受POSIXLY_CORRECT影响”与当前语言页和官方依据冲突。
- D2-103：非NULL空串被说成getenv的missing fallback；D2-123以os.ExpandEnv等同Windows展开；均不能直接升级知识。
- D2-194：help/helper存在不足以证明源有exec分派臂；D2-117大写路径建议未有精确源依据。

这些原件保留，不删除错误条目。裁决记录说明技术前提、来源与允许采信范围；自审数量/建议数量不等于已证实缺陷数量。

## 对照时发现的现行知识问题

### C-K1：PY-PS-06的“正确”示例实际删除Base64转换

`skills/directions/python-to-powershell/SKILL.md:125`源原型是对encode结果做b64encode后写盘，132行计算b64，133行却WriteAllBytes原始bytes；源写ASCII Base64字节，例子写转换前字节，内容不同。122/129行把“写Base64文本”本身说成错误，也会误导。

建议纠正为：源写哪层结果，目标就写哪层字节；编码后的ASCII串须转为相应字节并保持无新增BOM/换行。文本cmdlet的默认编码/终止符可以有问题，**Base64内容本身正是源意图**。[Python 3.12 Base64文档](https://docs.python.org/3.12/library/base64.html)明确b64encode返回编码后的bytes。本轮未编辑规则正文。

### C-K2：PY-PS-05混淆Start-Process、LASTEXITCODE与源忽略状态

`skills/directions/python-to-powershell/SKILL.md:99`将`& exe`与Start-Process一并要求用LASTEXITCODE判断并throw；108行示例把忽略返回码写成错误，甚至源触发条件包含“调用外部命令而忽略其返回码”。读取状态和传播状态必须由源决定，不能为显式检查而新增异常。Start-Process默认异步，PassThru返回Process对象，与直接执行外部程序的LASTEXITCODE渠道分别核。[Start-Process](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process?view=powershell-7.5)、[自动变量](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables?view=powershell-7.5)。

建议分开启动失败、子进程非零退出、源是否忽略/传播，以及准确等待/取码API；保留现有非终止错误与try/catch区别。规则基线7.6，网页此处7.5核验支持API区别，7.6的修订内容仍应按精确版本回核，不据网页代运行证据。

## 最小验证假设（待合法提供/隔离环境，未执行）

| 单一变量 | 预期成功/失败信号 | 要回收的原件 |
|---|---|---|
| D2-004从无文件改为提供合成CRLF空行文件；其它条件不变 | 真实源/修复目标loaded都3；不是仅默认loaded=0相同 | 提供者fixture版本、两侧程序原流/退出、目标版本、清理 |
| D2-254连续pushback第二个token；其它输入不变 | 第二个先返回，再第一个；Queue形态反例应暴露 | 两侧API真实观察、调用入口版本，不能新造Agent驱动 |
| D2-067 score13改15；其它条件不变 | 源floor得到1，错误PS强转得到2 | 源输入关联、两侧输出/退出、请求知识注入记录 |
| 同一合法JSON输出只改变键顺序/CRLF | 按冻结语义规则通过，同时保留原始不同字节 | 已提供驱动的协议/版本、外层及内层观察、消噪规则命中 |
| 同一目标仅将业务JSON loaded数值改变 | 必须失败；不得被广泛消噪吞掉 | 原流、保护字段、比较diff及策略版本 |

这些是观察设计，不是运行请求、不增加运行授权、不生成任何辅助程序。当前已删实现不可直接回放，待提供准确历史版本或未来正式新项才可验证。
