# 七语言共性语义索引

> **职责**：这里仅维护七语言共享事实的导航、事实分类口径与场景/系统分流；实质语义事实按语言各维护一处，不把相同事实复制到 42 个方向 Skill。方向专向映射仍以[根入口](../../SKILL.md)选择的方向 Skill 为准。
> **知识基线**：C11、C++17、C# 12/.NET 8、CPython 3.12、Go 1.27、PowerShell 7.6、CRuby 3.4。它是知识版本，不证明实际目标工具链已安装。
> **证据边界**：本索引按源码触发条件引导读取语言事实与方向规则。若本地事实冲突或必要版本事实缺失，记录涉及版本、条目和影响，停止受影响映射；不得猜测规则。编译与功能结论须依据本项精确版本的独立证据。

## 按语言加载

画像确定源→目标方向后，只加载对应的两个语言页，再加载方向专向 Skill；涉及系统行为时按下文加载场景/系统 Skill。

离线使用本地正文与下列相对引用；语言页的资料名称/版本/API 标识用于追溯，不要求访问网页。事实不足、来源未核或实际版本不明时，按具体规则的未知处理记录缺口；不以资料标题替代语义。

| 语言 | 共享事实 |
|---|---|
| C（ISO C11） | [c](languages/c.md) |
| C++（ISO C++17） | [cpp](languages/cpp.md) |
| C#（C# 12 / .NET 8） | [csharp](languages/csharp.md) |
| Python（CPython 3.12） | [python](languages/python.md) |
| Go（Go 1.27） | [go](languages/go.md) |
| PowerShell（PowerShell 7.6） | [powershell](languages/powershell.md) |
| Ruby（CRuby 3.4） | [ruby](languages/ruby.md) |

## 资料标识的本地读法

语言页和方向页保留的资料标识仅用于出处追溯，不是需要继续访问的链接。适用事实、条件和反例以本地正文为使用内容，未核版本/路径按规则记缺口。常用标识的资料名称如下；具体章节/API 随条目保留：

| 标识 | 资料名称与版本范围 |
|---|---|
| WG14-N1570 | ISO C11 委员会草案 N1570；按标注章节定位语言、库与入口语义 |
| WG21-N4659 | ISO C++17 工作草案 N4659；按标注条款/库接口定位 |
| MS-CS-* | Microsoft C# 语言参考及 .NET API/运行时资料；本项目 C# 12/.NET 8 基线，具体 API/实现版本按条目 |
| MS-PS-* | Microsoft PowerShell 语言/命令参考（本项目 7.6 基线）；宿主 .NET/平台版本另核，不由引用标识推定 |
| PY-REF-* / PY-LIB-* | Python 3.12 Language Reference / Library Reference；DATA 为 Data model，表达式、序列或具体模块按标识/条目 |
| CPY-DEV-GC | CPython 开发者资料的垃圾收集器说明；实现相关事实按解释器版本处理 |
| GO-SPEC / GO-MEM / GO-PKG-* / GO-RT-DOC | Go Language Specification / Memory Model / 所标标准库包 / runtime 资料；1.27 为项目知识基线，实际版本未核不外推 |
| RB-DOC-* / RB-DEV-GC | Ruby 3.4 官方核心/标准库类与方法说明、CRuby GC 实现资料；具体类、方法/库版本按条目 |
| POSIX、Linux 手册、Microsoft Win32/CRT、RFC、CWE | 所标标准/手册/API/协议或弱点编号；具体平台/版本和必要语义在本地场景、系统或共享参考中说明 |

## 易错语义导航

此表只定位正文，不复制语言事实、不以测试编号选规则。根执行步骤 2/4 消费：按源码使用点加载本次源/目标正文；单文件也适用，不依赖长文件、子进程或并发场景。

### 1. 算术、数值精度与真值判定

| 源码触发 | 应读正文 |
|---|---|
| 动态返回对象的停止判定、空容器/浮点零、__bool__/__len__、`0`/`""`/`[]` 真值 | [Python L1-PY-01](languages/python.md#l1-py-01-假值集合不等于判空)、[CPP-RB-06](../directions/cpp-to-ruby/SKILL.md) 及目标语言实际值域；Python→C#同读[PY-CS-07](../directions/python-to-csharp/SKILL.md#规则-py-cs-07停止判定与容器数值真值按实际值域对应)，不通过枚举求默认真值 |
| DWORD 下溢、全一哨兵、乘法中间值与多行表达式 | [PS L1-PS-10/11](languages/powershell.md#l1-ps-10-定宽模运算先确定中间值范围再掩码)；中间类型按范围选，解析通过不代对象数/输出一致 |
| 向零截断除法 vs 向下取整 `//`/`%`、定宽溢出回绕、`checked`/`unchecked` | [CPP-PY-06](../directions/cpp-to-python/SKILL.md)、[CPP-RB-05](../directions/cpp-to-ruby/SKILL.md)、[CS-CPP-07](../directions/csharp-to-cpp/SKILL.md)、[PY-C-06](../directions/python-to-c/SKILL.md)；区分有符号 UB（C/C++）与确定性二补码/位掩码 |

### 2. 字符串、编码、JSON 与定界

| 源码触发 | 应读正文 |
|---|---|
| 字节计数、非 ASCII 路径、文本流行尾 | 两语言页 §三；[Python L1-PY-03](languages/python.md#三字符串字节nulunicode-与编码)、[C++ L1-CPP-03](languages/cpp.md#三字符串字节nulunicode-与编码)、[PY-C-08](../directions/python-to-c/SKILL.md)、[CPP-PY-07](../directions/cpp-to-python/SKILL.md)、[CPP-GO-07](../directions/cpp-to-go/SKILL.md)、[CPP-RB-07](../directions/cpp-to-ruby/SKILL.md)；实际文件操作还读文件场景 |
| 原生宽字符串/注册表缓冲与代码单元长度、UTF-16 `string.Length` | [Go L1-GO-16](languages/go.md#l1-go-16-utf-16-代码单元不能直接转换成-string)、[C# L1-CS-09](languages/csharp.md#l1-cs-09-lengthrune-与文本元素的单位不同)、[CS-CPP-06](../directions/csharp-to-cpp/SKILL.md) 及两语言 §三；解码、原始 uint16/bytes、终止 NUL 与容量分开 |
| NFC/NFD/NFKC/NFKD、casefold、大小写键及码点限长 | [Python L1-PY-16](languages/python.md#l1-py-16-unicode-规范化折叠与文本长度分别保持)、[Go L1-GO-14](languages/go.md#l1-go-14-大小写映射不提供完整规范化与-casefold)、[C++ L1-CPP-07](languages/cpp.md#l1-cpp-07-文本容器与-locale-不等于-unicode-规范化)、[C# L1-CS-09](languages/csharp.md#l1-cs-09-lengthrune-与文本元素的单位不同)；按源实际调用，不把缺离线库变成语义等效 |
| JSON 重复键、孤立代理项、内嵌 NUL、数值和深度 | [Python L1-PY-17](languages/python.md#l1-py-17-json-接受域不由输出长得相同决定)、[Go L1-GO-15](languages/go.md#l1-go-15-encodingjson-的替换重复键与数值路径)、[C L1-C-07](languages/c.md#l1-c-07-json-解码字符串的长度须保留到校验与输出)、[PowerShell L1-PS-09](languages/powershell.md#l1-ps-09-json-解析深度与序列化深度是不同约束)；同时读另一语言实际解析 API，区分 raw 字节校验与 JSON 转义解码，核 `object_pairs_hook` 后序优先级与 `ensure_ascii=True` 对 `U+007F` 转义 |
| JSON 游标跳空白、空结构、闭括号与尾逗号 | [C++ L1-CPP-10](languages/cpp.md#l1-cpp-10-解析循环须在跳过空白后按语法状态判闭合)；按源解析 API 的接受域和当前语法状态，不统一先判结束而接受尾逗号 |
| 源正则/路径移入注释、Doxygen 文档字符串、Ruby 换行字面量 | [Go L1-GO-18](languages/go.md#l1-go-18-源文本放入目标注释仍须满足目标定界)、[Python L1-PY-18](languages/python.md#l1-py-18-文档字符串也是受转义规则约束的字符串)、[Ruby L1-RB-11](languages/ruby.md#l1-rb-11-单引号中的反斜杠不表示协议换行)；按本项语言选择，不把三种定界/转义层互套 |
| 固定文本、长字节常量、拼接/转义 | [C L1-C-06](languages/c.md#l1-c-06-字面量内容终止-nul-与显式长度分别保持)、C++ §三、Python L1-PY-06、[PowerShell L1-PS-06](languages/powershell.md#l1-ps-06-固定文本须区分字面值插值与输出终止符)；另一语言正文同时读取 |
| 去空白集合、nil/空串/全空白判定 | 两语言实际谓词；[Ruby L1-RB-08](languages/ruby.md#l1-rb-08-strip-不是通用-unicode-空白删除)、[Go L1-GO-06](languages/go.md#l1-go-06-unicode-空白不等于其他语言的-strip-集合)、C# L1-CS-01；Ruby→Go 读 RB-GO-07 |
| 环境变量未设置/空串、默认回退与继承 | [C §九](languages/c.md#九容量借用与默认值的选择引导)、[C++ §八](languages/cpp.md#八库抽象替换的选择引导)、[Ruby §十二](languages/ruby.md#十二标准库替换的选择引导)；环境profile语义另核评估准备契约，不用真假值合并缺失/空值 |

### 3. 参数、入口、控制流与异常清理

| 源码触发 | 应读正文 |
|---|---|
| 命令行守卫、参数下标、shift/解析后剩余范围 | 源/目标语言页 §一的参数规则；[C](languages/c.md)、[C++](languages/cpp.md)、[Ruby](languages/ruby.md)补计数与全部使用点联合映射；[Python L1-PY-07](languages/python.md#l1-py-07-getopt-的顺序策略由源解析器决定)区分扫描策略 |
| 程序名、托管程序集位置与进程映像回显 | [C# L1-CS-05](languages/csharp.md#l1-cs-05-程序实参不含程序名参数绑定与默认值必须显式重建)，同读源 argv 事实与冻结启动形态；ProcessPath 不普遍等同原始 argv[0] |
| 读键/读字符/整行、回显与终端模式 | [C# L1-CS-07](languages/csharp.md#l1-cs-07-readkey-不是-readline-或普通流字符读取)、[Python L1-PY-09](languages/python.md#l1-py-09-流读取一个字符不等于读取一个终端键事件)、[Ruby L1-RB-10](languages/ruby.md#l1-rb-10-getchgetc-与-gets-的输入单位不同)；按方向读 CS-PY-08/CS-RB-07；无子进程也读取 |
| except/catch 顺序、基类/派生匹配、不可达处理器与 C 错误码异常链 | [Python L1-PY-20](languages/python.md#l1-py-20-except-的-first-match-与异常继承共同决定有效分支)、[PY-C-07](../directions/python-to-c/SKILL.md) 及实际目标语言；诊断标签不当异常类型，不能为目标可编译而激活源被遮蔽分支 |
| 标签/goto、case 跳转跨局部初始化 | [PowerShell §九](languages/powershell.md#九普通控制流)、[C L1-C-11](languages/c.md#l1-c-11-特性测试宏位置隐式声明禁令与-goto-跨-vla-初始化边界)；按方向读 [CPP-PS-05](../directions/cpp-to-powershell/SKILL.md)、[C→C++ 规则 9](../directions/c-to-cpp/SKILL.md)；不因普通控制流加载并发场景 |
| RAII 析构作用域、块级/循环内 `defer`、`with`/`ensure`/`finally` 异常边界 | [CPP-PY-04](../directions/cpp-to-python/SKILL.md)、[CPP-GO-04](../directions/cpp-to-go/SKILL.md)、[CPP-RB-04](../directions/cpp-to-ruby/SKILL.md)、[CS-CPP-08](../directions/csharp-to-cpp/SKILL.md)；不依赖 `__del__`/GC finalizer，不在循环内放函数级 `defer`，不在默认 `noexcept` C++ 析构中抛异常 |

### 4. 容器、值/引用、枚举与标准库契约

| 源码触发 | 应读正文 |
|---|---|
| 值类型/按值拷贝 vs 引用共享、slice/map 底层共享、双向 `shared_ptr` 环 | [CPP-PY-05](../directions/cpp-to-python/SKILL.md)、[CPP-GO-06](../directions/cpp-to-go/SKILL.md)、[CS-CPP-05](../directions/csharp-to-cpp/SKILL.md) 及对应方向拷贝构造规则；区分按值隔离拷贝与共享别名 |
| `std::map` 有序遍历/缺键插入 vs Go 随机 `map`、函数返回嵌套集合 | [CPP-GO-05](../directions/cpp-to-go/SKILL.md)、[CPP-RB-03](../directions/cpp-to-ruby/SKILL.md)、[PowerShell L1-PS-08](languages/powershell.md#l1-ps-08-函数-success-流集合对象与泛型调用)；C#→PowerShell 同读方向 CS-PS-01/04，不用 @() 假定保留容器类型 |
| 具名元组的 Rest/Item 位置与解构消费者 | [C# L1-CS-10](languages/csharp.md#l1-cs-10-元组元素名有独立的上下文限制)；元素名、普通变量、位置/值与元数据分别核，不当通用关键字 |
| 枚举值、类型、未知数值、Flags 或名称输出 | [C# L1-CS-06](languages/csharp.md#l1-cs-06-enum-的类型值域与显示分别保持)、[Python L1-PY-08](languages/python.md#l1-py-08-enumintenum-与普通常量的身份不同)及实际两语言页；C#→Python 读 CS-PY-07；不因枚举加载并发 |
| path::extension、std::string 键序与 .NET API 候选 | [C++ L1-CPP-08/09](languages/cpp.md#l1-cpp-08-pathextension-取的是最后文件名的扩展部分)、[PS L1-PS-12](languages/powershell.md#l1-ps-12-net-扩展名与字符串比较器按实际规则选择)；C++→PS 同读 [CPP-PS-07](../directions/cpp-to-powershell/SKILL.md#规则-cpp-ps-07参数扩展名键序和续行按各自消费者映射)，Ordinal 有编码/值域条件 |
| optparse、Unicode分行/制表、deque操作组合与解析接受域 | [Python §九](languages/python.md#九解析器文本边界与容器的选择引导)；不套其他解析器或同名容器默认 |
| JSON编码/终止符、Scanner上限、稳定排序、时间/计数器及用户后端 | [Go §九](languages/go.md#九标准库消费点的选择引导)，另一语言同读；对象键序与文本义务分开 |
| 扫描停止/部分结果、用户后端、同键顺序、截止预算、合流与n/error | [Go L1-GO-08至12](languages/go.md#l1-go-08-scanner-的停止边界与已取得结果)；按源使用点读相应条目及网络/进程场景。Go→Ruby读[GO-RB-08](../directions/go-to-ruby/SKILL.md) |
| 容量/借用、可变长结构、托管或对象管道替换 | [C §九](languages/c.md#九容量借用与默认值的选择引导)、[C++ §八](languages/cpp.md#八库抽象替换的选择引导)、[C# §十](languages/csharp.md#十互操作与公开返回形态的选择引导)、[PowerShell §十](languages/powershell.md#十对象管道与外部状态的选择引导)、[Ruby §十二](languages/ruby.md#十二标准库替换的选择引导)；原生ABI/权限另读实际系统页 |

### 5. 编译器前端、头文件/ABI 与工程输入

| 源码触发 | 应读正文 |
|---|---|
| 外部函数/完整类型、特性测试宏位置、隐式声明禁令、Go 零值迁入 C | [C L1-C-08/09/10](languages/c.md#l1-c-08-外部函数与完整类型都须有声明来源)、[L1-C-11](languages/c.md#l1-c-11-特性测试宏位置隐式声明禁令与-goto-跨-vla-初始化边界)；源对应语言及 SDK 同读，目标漏声明不套源侧诊断放宽，初始化不等于业务成功 |
| C→C++ 隐式宏/缺系统头、`NOMINMAX`、C ABI 布局与符号消歧 | [头文件与宏](../directions/c-to-cpp/references/header-macro.md)、[类型/接口与 C ABI](../directions/c-to-cpp/references/type-abi.md)（[c-to-cpp](../directions/c-to-cpp/SKILL.md) 随附子参考）；不凭同名头文件推定兼容 |
| C++ 可空辅助指针、右值临时对象取地址与系统宏冲突 | [C++ L1-CPP-11](languages/cpp.md#l1-cpp-11-右值临时对象不得取地址与系统宏冲突防护)；按目标标准选 `std::optional` 或具名左值，避开 POSIX/Windows 系统宏同名常量 |
| C++ 字符串原地替换、只读参数与调用方写回 | [C++ L1-CPP-12](languages/cpp.md#l1-cpp-12-字符串原地修改取决于接收者的可变性)，区分只需返回新结果和调用方须观察修改的路径 |
| Go 未用导入/局部变量、短声明 `:=` 遮蔽、包入口与 `GOOS` 构建标签 | [Go L1-GO-20](languages/go.md#l1-go-20-未用导入变量短声明遮蔽与包入口编译红线)；不以 `_ = err` 吞错，库包不擅自改 `main` |
| C# SDK `Compile` 输入排除、顶级语句冲突与隐式 `using`/可空配置 | [C# L1-CS-08](languages/csharp.md#l1-cs-08-磁盘上的入口声明不等于本次编译实际包含它)、[L1-CS-11](languages/csharp.md#l1-cs-11-顶级语句冲突显式命名空间与-nullablesdk-默认配置边界)；配置未明时优先显式 `using` 与清晰入口 |
| C# 新增线程、原子操作、取消与任务类型的导入 | [C# L1-CS-12](languages/csharp.md#l1-cs-12-新增线程类型须对应实际命名空间)，区分 `System.Threading` 与 `System.Threading.Tasks` 的实际可见范围 |
| PowerShell `#requires` 版本锁定与 .NET 值类型枚举器装箱 | [PowerShell L1-PS-13](languages/powershell.md#l1-ps-13-版本锁定指令与可变值类型枚举器绑定边界)；未核验目标小版本不硬锁次版本，惰性迭代避开值类型枚举器装箱绑定 |
| 类内名称碰撞、抽象成员、源文本迁入注释 | [PowerShell §十](languages/powershell.md#十对象管道与外部状态的选择引导)、[C# §十](languages/csharp.md#十互操作与公开返回形态的选择引导)、[C L1-C-06](languages/c.md#l1-c-06-字面量内容终止-nul-与显式长度分别保持)；所有引用点、成员契约和目标文本定界分别保持 |

### 6. 计时、临时目录与系统/并发原语

| 源码触发 | 应读正文 |
|---|---|
| `perf_counter`/`process_time`、计时选项、进程/线程/子进程CPU | [Python L1-PY-21](languages/python.md#l1-py-21-perf_counter-与-process_time-测量不同对象)、[Go L1-GO-19](languages/go.md#l1-go-19-进程-cpu-时间不是-timesince)；Python→Go同读[规则5](../directions/python-to-go/SKILL.md#规则-5墙钟与进程-cpu-计时器分别映射)，源失败回退与动态数值消噪分别核 |
| Windows 输出模式、`filepath.Join`、路径拼接与裸 LF 写入 | [C L1-C-10](languages/c.md#l1-c-10-windows-crt-输出模式与行尾义务分开)、[Go L1-GO-17](languages/go.md#l1-go-17-路径拼接与原样写入有不同消费者)，另一语言的路径/CRT/writer 事实同读；实际文件操作读文件场景 |
| 文件失败仍继续、创建目录、路径存在/目录/普通文件守卫 | [C++ L1-CPP-06](languages/cpp.md#l1-cpp-06-存在性谓词不能收窄为目录谓词)、[Ruby §十二](languages/ruby.md#十二标准库替换的选择引导)与两语言页 §五及 [file-io L2-FILE-02](../scenes/file-io/SKILL.md)；C++→PowerShell 另读该方向的文件错误映射 |
| 临时目录候选、校验/回退、缓存及环境优先级 | [Python L1-PY-14](languages/python.md#l1-py-14-tempfile-的候选可用性与缓存)、[Ruby L1-RB-09](languages/ruby.md#l1-rb-09-dirtmpdir-的候选顺序与有效性)、[Go L1-GO-07](languages/go.md#l1-go-07-ostempdir-选路径不检查目录可用性)；Ruby→Go 读 RB-GO-08，实际文件副作用还读文件场景 |
| 关闭后的资源元数据与 Windows/Ruby 路径表示 | [Ruby L1-RB-12/13](languages/ruby.md#l1-rb-12-关闭后的资源元数据不保证仍可查询)；Go→Ruby 同读 [GO-RB-09](../directions/go-to-ruby/SKILL.md#规则-go-rb-09资源元数据临时目录加载与路径表示分别对应)，不猜动态地址或全局替换分隔符 |
| Win32 API 包成员、输出指针、`StartupInfo`/`ProcessInformation`、`ctypes` | [Go L1-GO-13](languages/go.md#l1-go-13-windows-api-的包归属与导出边界)、[Python L1-PY-15](languages/python.md#l1-py-15-ctypes-的-abi-声明与业务判定分别保持)、[进程身份系统页](../systems/posix-windows-process-identity/SKILL.md#原生环境块令牌与缓冲的选择引导)；按实际 ABI/源 A-W 接口另读系统页 |
| Windows `_popen`/cmd 外壳层、`fork` 返回分支、`exec` 替换/失败及环境 | [Python L1-PY-19](languages/python.md#l1-py-19-windows-子进程的外壳层argv-与捕获编码分开)、[进程场景 L2-PROC-02](../scenes/process-execution/SKILL.md#l2-proc-02-父子分支映像替换与环境契约)、[原生 fork/exec](../systems/posix-windows-process-identity/SKILL.md#原生-forkexec-事实)；涉及 Ruby 另读 [L1-RB-06/07](languages/ruby.md#九进程返回替换与环境)，C→Ruby 读 C-RB-07；同 OS 的原生 API 事实也适用 |
| POSIX ↔ Win32 线程、非递归锁与 `CRITICAL_SECTION`、绝对/相对条件变量超时与 TLS 析构 | [线程系统页](../systems/posix-windows-threads/SKILL.md#同步原语与超时易错边界)与[并发场景](../scenes/concurrency/SKILL.md)；虚假唤醒循环重等须扣减剩余超时，TLS 析构回调区分 `TlsAlloc`/`FlsAlloc` |
| 网卡枚举/流量累计与逐接口统计 | [网络场景的测量范围](../scenes/network-io/SKILL.md#网络统计的测量范围)；对象、范围、单位与采样先对应，不能用消噪代替语义映射 |

实际工具链、诊断文本或未覆盖错误路径未知时维持待核，不从语法相似/相同显示推断行为等价。规则技术依据与转换效果证据分开。

## 事实分类

- `[语言规范保证]`：由冻结语言标准、语言规范或官方定义保证的确定性语义。
- `[指定运行时的实现相关事实]`：仅适用于所列运行时/实现的行为，不外推到其他实现。
- `[待专题核验，不可用于确定转换规则]`：缺乏足够的适用版本一手依据，不能作为确定性转换前提。

## 场景与系统分流（何时加载 B 类规则）

> [!IMPORTANT]
> **A 类与 B 类职责边界律**：
> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

1. **套接字与网络通信行为**：
   - *源码触发条件*：源码中出现系统网络套接字调用，或各高级语言等价网络库调用（如 Go `net.Dial`, Python `socket.socket`, C# `Socket` / `TcpClient`）。
   - *必须加载的既有 B 类规则*：
     - 通用网络场景：[`skills/scenes/network-io/SKILL.md`](../scenes/network-io/SKILL.md)
     - 涉及 Linux/POSIX 与 Windows 跨系统转换时：[`skills/systems/posix-winsock/SKILL.md`](../systems/posix-winsock/SKILL.md)
   - *细节归属*：语言 API 返回形态/异常映射由本项方向维护；场景维护部分 I/O、协议、连接/资源义务；OS 句柄、初始化、结构体和错误来源见系统页，语言事实不能单独裁定平台映射。

2. **文件系统与路径操作行为**：
   - *源码触发条件*：源码中出现底层文件句柄操作、路径拼接分隔符与驱动器解析，或语言层文件读写（如 Go `os.Open`, Python `open()`, C# `FileStream`）。
   - *必须加载的既有 B 类规则*：
     - 通用文件场景：[`skills/scenes/file-io/SKILL.md`](../scenes/file-io/SKILL.md)
     - 涉及 Linux/POSIX 与 Windows 跨系统转换时：[`skills/systems/posix-windows-filesystem/SKILL.md`](../systems/posix-windows-filesystem/SKILL.md)
   - *语言层核心职责*：保证文件句柄在各分支及异常下确定性关闭；确保文本/二进制打开模式与平台换行符（CRLF vs LF）一致；具体路径规范化与目录遍历由 B 类规则裁定。

3. **语言级或原生线程/任务与并发同步行为**：
   - *源码触发条件*：源码中实际使用原生线程、互斥锁/条件变量/读写锁/TLS/InitOnce、语言级 goroutine/Task/thread、异步任务、共享状态或同步/取消/背压机制；不要求出现原生 OS API。
   - *必须加载的既有 B 类规则*：
     - 通用并发场景：[`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)
     - 涉及 POSIX `pthread_*` 与 Windows CRT/Win32 线程、互斥锁、条件变量、TLS 或 InitOnce 跨系统/原生转换时：[`skills/systems/posix-windows-threads/SKILL.md`](../systems/posix-windows-threads/SKILL.md)
   - *语言层核心职责*：管理线程生命周期与同步所有权契约，具体 OS 调度、锁递归性、超时基准与 TLS 回调语义由 B 类规则裁定。

4. **进程创建、替换、等待与身份/特权行为**：
   - *源码触发条件*：源码创建子进程、替换自身映像、等待或观测退出状态、终止进程（树），或查询/切换自身身份与特权。
   - *必须加载的既有 B 类规则*：
     - 通用进程执行场景：[`skills/scenes/process-execution/SKILL.md`](../scenes/process-execution/SKILL.md)
     - 实际 fork/exec 或涉及 POSIX/Linux 与 Windows 跨系统转换时：[`skills/systems/posix-windows-process-identity/SKILL.md`](../systems/posix-windows-process-identity/SKILL.md)；同 OS 仅读适用事实，不套跨 OS 表。
   - *语言层核心职责*：保持进程生命周期、退出状态传递与错误模型；`fork`/`exec`/`CreateProcess` 的模型差异、令牌与特权映射由 B 类规则裁定。

5. **Windows 注册表与服务控制行为**：
   - *源码触发条件*：源码读写 Windows 注册表键值，或通过 SCM 创建、配置、启动、停止、删除服务（含目标语言/脚本对同一子系统的封装调用）。
   - *必须加载的既有 B 类规则*：[`skills/systems/windows-registry-service-subsystem/SKILL.md`](../systems/windows-registry-service-subsystem/SKILL.md)
   - *语言层核心职责*：保持键/值类型与长度约定、服务状态机与配置回滚义务；POSIX 侧没有等价子系统，须按不可映射项处理，不得用配置文件替代注册表并宣称等价。
