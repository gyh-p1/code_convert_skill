# 七语言共性语义索引

> **职责**：这里仅维护七语言共享事实的导航、事实分类口径与场景/系统分流；实质语义事实按语言各维护一处，不把相同事实复制到 42 个方向 Skill。方向专向映射仍以[根入口](../../SKILL.md)选择的方向 Skill 为准。
> **知识基线**：C11、C++17、C# 12/.NET 8、CPython 3.12、Go 1.27、PowerShell 7.6、CRuby 3.4。它是知识版本，不证明实际目标工具链已安装。
> **证据边界**：既有内容源于静态重组；2026-10-11 易错语义导航对应的新增/修订事实已按所列官方依据复核，但未完成全部旧事实复核或转换效果验证。若不同来源冲突，回到适用版本的官方标准/运行时文档核对，不因本索引存在便宣称等价。

## 按语言加载

画像确定源→目标方向后，只加载对应的两个语言页，再加载方向专向 Skill；涉及系统行为时按下文加载场景/系统 Skill。

离线使用本地正文与下列相对引用；语言页的资料名称/版本/API 标识用于追溯，不要求访问网页。事实不足、来源未核或实际版本不明时，按具体规则的未知处理记录缺口；不以资料标题替代语义，也不以离线可读声明全部技术事实已验收。

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

| 源码触发 | 应读正文 |
|---|---|
| 命令行守卫、参数下标、shift/解析后剩余范围 | 源/目标语言页 §一的参数规则；[C](languages/c.md)、[C++](languages/cpp.md)、[Ruby](languages/ruby.md)补计数与全部使用点联合映射；[Python L1-PY-07](languages/python.md#l1-py-07-getopt-的顺序策略由源解析器决定)区分扫描策略 |
| 字节计数、非 ASCII 路径、文本流行尾 | 两语言页 §三；[Python L1-PY-03](languages/python.md#三字符串字节nulunicode-与编码)、[C++ L1-CPP-03](languages/cpp.md#三字符串字节nulunicode-与编码)；实际文件操作还读文件场景 |
| 固定文本、长字节常量、拼接/转义 | [C L1-C-06](languages/c.md#l1-c-06-字面量内容终止-nul-与显式长度分别保持)、C++ §三、Python L1-PY-06、[PowerShell L1-PS-06](languages/powershell.md#l1-ps-06-固定文本须区分字面值插值与输出终止符)；另一语言正文同时读取 |
| 标签/goto、case 跳转跨局部初始化 | [PowerShell §九](languages/powershell.md#九普通控制流)；按方向读 [CPP-PS-05](../directions/cpp-to-powershell/SKILL.md)、[C→C++ 规则 9](../directions/c-to-cpp/SKILL.md)；不因普通控制流加载并发场景 |
| 文件失败仍继续、创建目录 | 两语言页 §五及 [file-io L2-FILE-02](../scenes/file-io/SKILL.md)；C++→PowerShell 另读该方向的文件错误映射 |
| fork 返回分支、exec 替换/失败及环境 | [进程场景 L2-PROC-02](../scenes/process-execution/SKILL.md#l2-proc-02-父子分支映像替换与环境契约)、[原生 fork/exec](../systems/posix-windows-process-identity/SKILL.md#原生-forkexec-事实)；涉及 Ruby 另读 [L1-RB-06/07](languages/ruby.md#九进程返回替换与环境)，C→Ruby 读 C-RB-07；同 OS 的原生 API 事实也适用 |
| 枚举值、类型、未知数值、Flags 或名称输出 | [C# L1-CS-06](languages/csharp.md#l1-cs-06-enum-的类型值域与显示分别保持)、[Python L1-PY-08](languages/python.md#l1-py-08-enumintenum-与普通常量的身份不同)及实际两语言页；C#→Python 读 CS-PY-07；不因枚举加载并发 |
| 读键/读字符/整行、回显与终端模式 | [C# L1-CS-07](languages/csharp.md#l1-cs-07-readkey-不是-readline-或普通流字符读取)、[Python L1-PY-09](languages/python.md#l1-py-09-流读取一个字符不等于读取一个终端键事件)、[Ruby L1-RB-10](languages/ruby.md#l1-rb-10-getchgetc-与-gets-的输入单位不同)；按方向读 CS-PY-08/CS-RB-07；无子进程也读取 |
| 去空白集合、nil/空串/全空白判定 | 两语言实际谓词；[Ruby L1-RB-08](languages/ruby.md#l1-rb-08-strip-不是通用-unicode-空白删除)、[Go L1-GO-06](languages/go.md#l1-go-06-unicode-空白不等于其他语言的-strip-集合)、C# L1-CS-01；Ruby→Go 读 RB-GO-07 |
| 临时目录候选、校验/回退及环境优先级 | [Ruby L1-RB-09](languages/ruby.md#l1-rb-09-dirtmpdir-的候选顺序与有效性)、[Go L1-GO-07](languages/go.md#l1-go-07-ostempdir-选路径不检查目录可用性)，另一语言按实际 API；Ruby→Go 读 RB-GO-08，实际文件副作用还读文件场景 |

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
   - *源码触发条件*：源码中实际使用原生线程、语言级 goroutine/Task/thread、异步任务、共享状态或同步/取消/背压机制；不要求出现原生 OS API。
   - *必须加载的既有 B 类规则*：
     - 通用并发场景：[`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)
     - 涉及 Linux 与 Windows 跨系统转换时：[`skills/systems/posix-windows-threads/SKILL.md`](../systems/posix-windows-threads/SKILL.md)
   - *语言层核心职责*：管理线程生命周期与同步所有权契约，具体 OS 调度与同步原语映射由 B 类规则裁定。

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
