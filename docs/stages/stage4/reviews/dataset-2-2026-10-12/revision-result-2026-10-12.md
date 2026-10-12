# 本批优化修订交付

> 后续目标收尾：当前R1–R10知识维护完成，R10概览已补为七子项的具体正文，详见[完成核对](R10-completion-audit-2026-10-12.md)。本次按最新目标到R10停止；以下保留原修订范围记录，不新增R11以后动作，不执行回归。

> 状态：本轮定向修订完成；转换效果、评估回归和部署均未验证。
> 2026-10-12用户确认依次修订，知识以引导为主，只补充、不做验证回归，最终由用户另行确认全量回归。本轮按此执行；没有启动下一轮转换/回归。

## 修订结果

| 修订队列 | 最终落点与结果 | 范围 |
|---|---|---|
| R-01/R-02 | Python→PowerShell PY-PS-06修正Base64编码结果写盘和FromBase64String输入类型；PY-PS-05区分启动异常、子退出、等待和取码渠道。相邻PY-PS-03限定源静默/输出路径，消除与05冲突 | 纠正已定位的旧示例，其余知识以补充选择引导为主；无运行证明 |
| R-03/R-04 | Go语言页§九补JSON/终止符、构建平台分支；C++§八补case/goto、隐式分配/借用；Ruby§十二衔接fork/exec返回与已有§九事实 | 不从惯用API或当前平台猜等价 |
| R-05/R-06/R-07 | Python§九补optparse接受域/程序名、Unicode分行和制表位置、deque同端/两端操作；共性索引可达 | 拒绝tabsize≤0保留TAB和appendleft+popleft为FIFO两条错误建议 |
| R-08/R-09/R-10 | 七语言页、文件/网络/进程场景、进程身份/注册表/文件系统页补容量、编码、结构/权限、展开、归档、扫描边界、排序、部分结果、时间/后端、超时、双流和临时目录选择 | 给条件/反例/未知，不新增SDK偏移猜测、驱动、强测或反复自审 |
| R-11/R-12/R-13 | 评估准备、构建前提、任务状态、分类准入、交付及开发规范补观察有效性、构建/加载分层、LIB适用范围、模板/实际条件对应、分类原件保留和取回状态分列 | 已有门禁保留；不强制非空argv/stdin/stdout，不把import失败当构建失败，不删除初次分类 |
| R-14/R-15/R-16 | 评估准备§5.1、入口/批量/行为/适配同步“有效性→消噪→功能分类→分层统计”，有效matched+semantic_pass计冻结范围比较通过，分列两类/覆盖/编译/交付 | 宽泛消噪保护行为；旧原判与冻结策略不回改，不外推完整业务或全批转换成功率 |
| 评估源码 | 相邻第三方评估系统5个现有模块定向修改；一条已有摘要测试同步新口径但未执行；说明已落盘 | 未运行pytest/解析器/编译器/发布工具，未构建、部署、触发Controller/VM或样本 |

## 27类知识维护去向落盘

此表说明候选的维护去向，不把所有历史自审断言或全部SDK/API细节宣布已验证。原96份登记、27簇裁决及DeepSeek原报告保持可追溯；错误建议仍保留。

| 既有簇 | 本轮补充或沿用的正文 |
|---|---|
| K-A/F/G/H/L/M | C§九、C#§十、PowerShell§十；进程身份新增环境块/令牌/缓冲引导、注册表原始/展开及枚举引导；Winsock初始化沿用原页，不扩展成模块加载保证 |
| K-B/C/D/I | C容量/借用、C++库替换与异常/创建/枚举引导、文件系统容量/创建模式；原错误和资源规则继续消费 |
| K-E/K/U/W | 进程场景等待/错误/双流、语言页与PY-PS-05；终端输入/公开接口的原规则沿用，不因冻结EOF删调用 |
| K-J/N/R/S/Z | Python解析器/文本/容器/解码、Go标准库消费点、C/C++/C#/Ruby的分割/默认插入/排序引导；错误的FIFO、TAB、missing/empty和环境展开等建议不固化 |
| K-O/P/Q/AA | Go标准库消费点的时间、计数器、Scanner、身份后端与平台分支；语言/文件页的创建模式引导，不把采样值放宽当定义等价 |
| K-T/V/X/Y | 文件变换/归档与清理结果、网络部分结果/deadline、Ruby临时目录既有事实与部分读取引导、Python临时目录选择点；源传播/忽略按使用点保持 |

未知精确库版本、ABI、接口接受域和源消费者，仍由未来实际项按本文引导定位；这是知识边界，不新增知识修订回归门禁。并未穷尽每条历史发现的实现细节或恢复删除的源码。

## 评估系统的实际修改

实际仓库：`E:/桌面文档/Agents System/third-party-evaluation-system`，不是部署安装目录。

- evidence_builder：摘要与size对应同一未比较归一化的编码字节；normalizedText另存，字节采集producer仍以真实完整流覆盖。exact的旧隐含CRLF容忍不再来自文本builder。
- evidence_comparator：diff.path与evidenceRefs分stdout/stderr并定位两侧，原比较分类未擅自放宽。
- report_builder：人读报告列matched+semantic-match的通过维度小计及两类数量，已发布JSON的matchedDimensions原义保留；没有造新的功能任务数。
- job_closure：独立证据层显示实际exitCode/timedOut，不把completed当成功；provenance仍不伪造PASS。
- job_service：request-only接受记录生成可查询的恢复故障；缺身份、损坏manifest/报告材料时保留阻断与原件，不重放，不虚构清理。此改动改善恢复/取证，不宣称所有孤立请求自动解除busy。

平台[源码优化说明](../../../../../../third-party-evaluation-system/docs/dataset-2-guided-optimization-2026-10-12.md)列兼容边界及未来回归范围。现有服务器比较配置未修改；没有新增InputProfile/schema字段或广泛忽略stderr/所有端口/所有构建后缀。关系型集合/诊断映射等尚无现役实现支持的需求只在引导中说明，不冒称已经上线。

## 实际加载路径静态回查

先原生rg穷举磁盘上的skills Markdown及根/发现入口，再按文件回查本轮规则的读取路径。没有写辅助检查脚本，没有将代码块类型转换当链接。

| 路径 | 人工检查范围与结果 |
|---|---|
| .agents发现入口→AGENTS→根SKILL | 新口径转引评估准备§5.1；语义知识仍按源触发及两语言/一个方向加载，不增加动态步骤 |
| 主干契约/闭环/构建/分类/交付→适配 | 核冻结不回写、重分类不删旧件、构建与运行分层、LIB与安全例外、先有效性再消噪及统计；修正开发规范旧“只有永久无安全入口才仅编译”措辞 |
| 42方向 | 分C/C++、Python/Go、C#/PowerShell/Ruby逐文件读入口/语言引用/安全与评估相关段；全部仍要求回根加载，能触达新增语言正文和评估准备；不是全库旧规则技术验证 |
| 4场景+5系统+战术索引 | 逐文件核入口/安全/门禁与oracle条件措辞；新增场景/系统引导不构成执行授权，其余页沿用对应根契约 |
| 2工作流 | 批量统计明确小计；长文件仍回根和评估准备，不以分段绕过新口径或追加审阅次数 |
| 7语言+共性索引/安全专题及随附参考 | 新语义放语言/场景/系统本体，共性只导航；另读C→C++专页与网络随附页有关门禁/边界，不增加测试目录依赖 |
| 相对路径/锚点 | 新导航的7语言章节和评估准备§5.1逐项对照实际标题；12个关键目标路径原生Test-Path为True；新章节编号已修正，不继承工具输出截断为已读 |
| 文本差异 | 两仓git diff --check无空白错误；这是静态文本检查，不是语法/编译/回归 |

工作区在本轮前已有大量未提交修改；未撤销、提交或推送它们，未把全部git diff统计当本轮改动数。原始dataset过程证据及旧平台标签未更改。新状态记录与本轮成果都在本审查目录，不加入产品加载依赖。

## 资料核对记录

以下地址仅用于维护追溯，不进入转换知识必读路径；产品正文已有必要语义与资料名称。资料阅读不是动态验证。

- [Python3.12 Base64](https://docs.python.org/3.12/library/base64.html)、[subprocess](https://docs.python.org/3.12/library/subprocess.html)、[optparse](https://docs.python.org/3.12/library/optparse.html)、[Built-in Types](https://docs.python.org/3.12/library/stdtypes.html)、[deque](https://docs.python.org/3.12/library/collections.html)。
- [CPython v3.12.0 unicode_expandtabs_impl](https://raw.githubusercontent.com/python/cpython/v3.12.0/Objects/unicodeobject.c)：TAB、列及CR/LF处理的实现依据，未执行。
- [PowerShell7.6 Start-Process](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process?view=powershell-7.6)、[Automatic Variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables?view=powershell-7.6)。
- [Go encoding/json](https://pkg.go.dev/encoding/json)：map键排序与Encoder.Encode终止符；项目Go基线不证明目标安装，具体标准库变更不外推。
- [TOKEN_PRIVILEGES](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_privileges)、[AccessCheck](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-accesscheck)、[GetEnvironmentStrings](https://learn.microsoft.com/en-us/windows/win32/api/processenv/nf-processenv-getenvironmentstrings)、[RegistryKey.GetValue](https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.registrykey.getvalue)。精确SDK/架构及.NET8适用条件仍写在知识正文。

## 下一步

本轮优化已落盘。按用户安排等待明确确认全量回归；本次没有验证通过数，也不宣布旧问题全部动态已修复。届时再核当前源/目标版本、隔离/工具链/合法入口及平台源码/发布身份，分别回收编译、功能、覆盖和清理证据。未获确认不启动回归或部署。
