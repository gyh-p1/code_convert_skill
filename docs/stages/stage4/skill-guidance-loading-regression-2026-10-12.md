# Skill 指导、引导与加载的全量模拟回归（2026-10-12）

> 当前状态：全量静态审阅与本轮已定位修订 COMPLETE / STATIC_REVIEWED；§6 的首次 NOT_PASSED 保留历史，U01–U07 的收齐与复查见§7。没有进行转换效果验证，不宣称全域语义正确或动态通过。
> “指导”检查严格的次序、前置条件、动作、依据、停止/恢复和收尾；“引导”检查源事实/适用版本/行为义务与候选映射的关系，不以惯用写法或示例覆盖源。

## 1. 范围与记录方式

入口为发现页→AGENTS→根 SKILL，再依根第 1 步读取必读契约，按模式/渠道加载工作流/适配，按事实加载两语言、方向及场景/系统/专题。重新按磁盘穷举，不从旧演练报告继承本轮覆盖；工程/历史测试资料不作为产品加载入口。

范围含实际全部 54 个 Skill（42 方向、4 场景、5 系统、2 工作流、战术索引）、发现/根/AGENTS、7 语言/共性/安全语义、方向随附页与网络兼容页，以及主干契约/工作流参考/Controller 适配。读取与判读进度逐组登记；工具展示截断的范围补读后才计覆盖。全文阅读不等于所有技术事实已独立验证。

本次模拟采用文字条件与下一动作，不生成示例源码、辅助脚本/驱动或模拟平台 JSON。条件中的 ALLOWED/build/基线等是明确假设，不声称本次取得了该证据。真正取得的是当前产品文件的读取与静态判读；模型实际注入、编译/行为、服务端拦截和任意 Agent 遵守均未验证。

## 2. 读取覆盖（完成）

| 组 | 本轮覆盖 |
|---|---|
| 发现/根/AGENTS | 三页已全文回读，根补指导/引导显式使用边界 |
| 必读主干 | 任务状态、评估准备、交付、安全、闭环、分类、构建前提七页全部正文 |
| 批量/长文件及适配 | 两工作流及远端/协议/比较/[Runner 能力矩阵](../../../references/adapter/controller/runner-capability-matrix.md)四适配全部正文；可选行为指导、参考导航与 manifest 示例另读 |
| 七语言与共享/随附知识 | 七语言、共性导航、安全行为、C→C++ 两专页与网络兼容页全部正文 |
| 42 方向 | 42/42 正文及回链，源/目标语言页与场景触发一并审查，明细见§4 |
| 4 场景/5 系统/战术 | 10/10 正文；并发/安全/注册表部分冲突已修，其他待核见§6 |

原生 rg 穷举实际 54 个 Skill，逐页手工读取；截断区间补读。另读业务、开发、编写规范及薄导航，不以工程历史充当前产品加载链。知识可达、Agent 已读、模型实际注入、效果分别验收：本轮只证明前两层。

## 3. 严格指导修订与逐步调度演练

| ID | 当前定位与影响 | 处置 |
|---|---|---|
| S01 | case.md 与唯一必备冻结正文容易混同 | 已改接入说明；状态契约补实际来源/N/A，不造第二冻结；F05 复走 |
| S02 | 根入口未显式汇合指导/引导使用边界 | 已补严格流程、有条件候选及冲突停受影响请求；F02/F20/F42 复走 |
| S03 | 分类页“核对通过即提交”可能跳过源预检 | 已明确仅满足本节，仍按根顺序源预检→生成→自审→就绪才双侧提交；F08 复走 |
| S04 | 远端适配固定 classification-1，返回件清单未区分分支 | 已改当前适用编号、job-id 落点及 source-only/build-only/双侧行为适用原件；F32 复走 |

正常行为路径：加载→画像/适用知识→单项冻结落盘/回读→分类→源构建及有效基线→配置模型生成→有限自审→评估就绪→提交/回执→状态/清理与原件→观察有效性→消噪/归因/功能分类→适用修订或报告→逐件交付核对→终态。

每行独立改变条件；结论“明确”是当前文字可解释，不是平台动态拦截证据。状态=task-state-contract，准备=evaluation-readiness-contract，交付=delivery-handoff-contract；均位于 references/framework。分类/闭环/构建位于 references/workflow。

| 条件 | 下一动作、禁止动作和记录 / 真源 | 静态结果 |
|---|---|---|
| F01 纯文档审阅 | 不触发正式模型/动态转换门禁，不伪造 run / 根、AGENTS | 明确 |
| F02 直接进方向 | 回根及必读契约再动作，不凭映射开始转换 / 全部方向入口 | 明确 |
| F03 缺两语言正文 | 补源/目标语言与实际场景，记录已读 / 根、状态§2.3 | 明确 |
| F04 冻结缺/空/错项 | 停新增分类/预检/模型/提交，手工补并回读；原 job 查询/取证/清理可继续 / 状态§2.2 | 明确 |
| F05 无独立 case.md | 记录实际输入来源与精确源集合，字段有理由 N/A，不造第二冻结 / S01 | 明确 |
| F06 源/冻结条件变 | 关联新版本，核重分类/基线失效，不借旧摘要 / 状态§2.1、准备§1.2 | 明确 |
| F07 非 ALLOWED/null 或缺原件 | 不预检、不生成、不提交，保留阻断 / 分类 | 明确 |
| F08 分类引用核过 | 先源预检，不能直接双侧提交 / S03 | 明确 |
| F09 READY/clean/快照 | 仍逐例核隔离、外部地址和清理，未核不执行 / 安全 | 明确 |
| F10 共处宿主可联网 | 样本只入获准 VM，不访问安装目录/jobs / 安全、AGENTS§11 | 明确 |
| F11 源构建真实失败 | 分源/依赖/命令装置原因，不调用模型修源 / 构建、准备 | 明确 |
| F12 源构建过但启动失败 | 保留失败并归因，不冒充源不可构建 / 准备 | 明确 |
| F13 只 banner/usage/参数未生效 | 不作有效所需状态基线，先处理准备或行为缺口 / 准备§2–4 | 明确 |
| F14 输出空但退出/副作用有效 | 按冻结观察核，不一律判失败/无效 / 准备、比较适配 | 明确 |
| F15 源能构建、本轮缺合法入口 | LIB：继续生成/自审及目标不运行验证，功能 UNVERIFIED / 准备§1.3 | 明确 |
| F16 目标仅编译支持未知 | 保留完整目标，目标 UNVERIFIED，适用件齐后 PARTIAL，不造 job / 准备、交付 | 明确 |
| F17 源预检支持未知 | 缺源构建证据不能生成，不借 F16 绕源门禁 / 准备§1.1 | 明确 |
| F18 片段缺合法上下文 | 仅用用户/获批平台精确上下文，不造入口/驱动 / 构建、准备 | 明确 |
| F19 模型协议未知 | PREPARATION_GAP，不猜接口、不泄漏凭证 / 根、闭环 | 明确 |
| F20 仅索引/截断/请求无正文 | 分开可达、已读与实际注入；补必要语义 / 状态§2.3 | 明确 |
| F21 模型响应不完整 | 留原 attempt，有限补调；不代写目标/伪造完整 / 根、闭环 | 明确 |
| F22 NO-REPAIR-IDENTIFIED | 有效有限自审即可推进，不反复重审或要求预测编译 / 闭环 | 明确 |
| F23 建议只有环境/源已有问题 | 不自动修；修需定位且转换引入 / 闭环 | 明确 |
| F24 多段/重入/两类修复 | 保留单任务预算，不借段/run 重置 / 根、长文件、状态 | 明确 |
| F25 常驻服务只等退出 | 行为不就绪；核现有合法驱动启动/到达/采集/终止，不造驱动 / 准备 | 明确 |
| F26 双侧初始条件不同 | 不形成可比较行为结论，修对称准备或记缺口 / 准备、比较适配 | 明确 |
| F27 适用 oracle 无法冻结 | 不从目标反推，不伪造；按真实原因处理行为缺口 / 准备 | 明确 |
| F28 消噪遇业务值/类型/null/顺序/码 | 先有效性与冻结允许差异，保护业务数据 / 比较适配 | 明确 |
| F29 差异超出现役策略表达 | 记准备缺口，不造 comparator 字段或自行改 verdict / 比较适配 | 明确 |
| F30 matched/semantic_pass | 有效精确版本去重后 M+S 可计功能一致，不能填编译 PASS / 批量§6 | 明确 |
| F31 body/字节/解码/视图 | 分对象留来源，截断/缺件/未发生分开 / 交付、适配 | 明确 |
| F32 source-only/build-only | 按 kind/mode 核适用件，不造 target/execution/comparison / S04 | 明确 |
| F33 超时可能已接收 | WAITING，原身份查询，禁盲重发；候选恢复不当已部署 / 状态、协议适配 | 明确 |
| F34 终态但清理/closure 未过 | WAITING，不以 PARTIAL 绕未决执行 / 交付、协议适配 | 明确 |
| F35 改目标想借旧功能结果 | 源基线仅按不变条件复用，新目标要新证据 / 状态、准备 | 明确 |
| F36 停止或缺交付件 | 仍统一收尾；缺应有件不终态，报告不解除活动 job / 交付§1.1 | 明确 |
| F37 真实 FAIL 且工作齐备 | 可 DONE；交付、编译、功能分开 / 状态 | 明确 |
| F38 批量先冻结/辅助程序 | 只冻一项立即推进，手工串行；分类器例外不扩大 / AGENTS、批量 | 明确 |
| F39 第40个唯一终态 | 追加对账并带旧未决；重试/重入不重复计，缺档停新增 / 批量、闭环 | 明确 |
| F40 余数或少于40 | 仍做关闭前终局核对 / 批量 | 明确 |
| F41 长文件分段 | 同一冻结/源基线、完整最终目标、跨段契约与预算 / 长文件 | 明确 |
| F42 源与知识冲突 | 停受影响请求、记定位与影响；其他有依据项可继续 / 根、状态§2.3 | 明确 |

## 4. 42 方向逐项覆盖

全部已读正文、两语言、跨场景触发及根/安全回链。R 是本轮修订主题（§5），U 是未决主题（§6）。无新增定位不等于技术正确性 PASS。

| 方向 | 正文重点与处置 |
|---|---|
| [C→C++](../../../skills/directions/c-to-cpp/SKILL.md) | 类型/ABI、宏、COM；U06 |
| [C→C#](../../../skills/directions/c-to-csharp/SKILL.md) | 返回码 R01；结构体/长度/回调 U02 |
| [C→Go](../../../skills/directions/c-to-go/SKILL.md) | 强制 error R01；释放候选 U01 |
| [C→PowerShell](../../../skills/directions/c-to-powershell/SKILL.md) | 指针、argv/退出；无新增定位 |
| [C→Python](../../../skills/directions/c-to-python/SKILL.md) | 返回码/资源/NUL/线程 R01/R02/R09/R14 |
| [C→Ruby](../../../skills/directions/c-to-ruby/SKILL.md) | IO/pack/释放 U01/U03 |
| [C++→C](../../../skills/directions/cpp-to-c/SKILL.md) | 析构/异常/多态；无新增定位 |
| [C++→C#](../../../skills/directions/cpp-to-csharp/SKILL.md) | map/空 catch R12；future U04 |
| [C++→Go](../../../skills/directions/cpp-to-go/SKILL.md) | RAII/泛型/容器；无新增定位 |
| [C++→PowerShell](../../../skills/directions/cpp-to-powershell/SKILL.md) | 对象/异常/参数/字节；无新增定位 |
| [C++→Python](../../../skills/directions/cpp-to-python/SKILL.md) | 所有权/并发/求值；无新增定位 |
| [C++→Ruby](../../../skills/directions/cpp-to-ruby/SKILL.md) | 比较器/数值/IO；U03 |
| [C#→C](../../../skills/directions/csharp-to-c/SKILL.md) | 委托/UTF-16/wchar/索引；U02 |
| [C#→C++](../../../skills/directions/csharp-to-cpp/SKILL.md) | COM 所有权 R16；取消/异常 U04 |
| [C#→Go](../../../skills/directions/csharp-to-go/SKILL.md) | defer 参数 R03；块级释放 U01 |
| [C#→PowerShell](../../../skills/directions/csharp-to-powershell/SKILL.md) | LINQ R10、CIM R15；索引/out U05 |
| [C#→Python](../../../skills/directions/csharp-to-python/SKILL.md) | async 启动/循环/线程 R14；其他 U04 |
| [C#→Ruby](../../../skills/directions/csharp-to-ruby/SKILL.md) | Task 错误 R14；真假/捕获 U04/U07 |
| [Go→C](../../../skills/directions/go-to-c/SKILL.md) | 数组保活/defer/锁内分配 R03/R05 |
| [Go→C++](../../../skills/directions/go-to-cpp/SKILL.md) | 状态/defer/C++17/panic R01/R03/R04/R05 |
| [Go→C#](../../../skills/directions/go-to-csharp/SKILL.md) | 值复制/nil/cap/字节/排序 R01/R05/R06/R12 |
| [Go→PowerShell](../../../skills/directions/go-to-powershell/SKILL.md) | JSON/原生结果/并发；无新增定位 |
| [Go→Python](../../../skills/directions/go-to-python/SKILL.md) | 元组/真值/无缓冲队列 R01/R07/R11 |
| [Go→Ruby](../../../skills/directions/go-to-ruby/SKILL.md) | nil/defer/退出/编码 R03/R07/R09；channel U04 |
| [PowerShell→C](../../../skills/directions/powershell-to-c/SKILL.md) | 管道/属性/null；U07 |
| [PowerShell→C++](../../../skills/directions/powershell-to-cpp/SKILL.md) | 收窄 R13；闭包 U04 |
| [PowerShell→C#](../../../skills/directions/powershell-to-csharp/SKILL.md) | 数组旧别名 R08；属性/流 |
| [PowerShell→Go](../../../skills/directions/powershell-to-go/SKILL.md) | WMI 属性 R15；流/Job/null U05/U07 |
| [PowerShell→Python](../../../skills/directions/powershell-to-python/SKILL.md) | 消费/单元素真值；U07 |
| [PowerShell→Ruby](../../../skills/directions/powershell-to-ruby/SKILL.md) | 流交错/消费 R10；静默错误 U01 |
| [Python→C](../../../skills/directions/python-to-c/SKILL.md) | 生成器/整数/字节；无新增定位 |
| [Python→C++](../../../skills/directions/python-to-cpp/SKILL.md) | 裁剪/生成器 R07/R10；pack/异常 U03/U04 |
| [Python→C#](../../../skills/directions/python-to-csharp/SKILL.md) | 负边界/空索引/顺序 R07/R12；pack U03 |
| [Python→Go](../../../skills/directions/python-to-go/SKILL.md) | 切片/逆序/吞错误 R01/R07/R08 |
| [Python→PowerShell](../../../skills/directions/python-to-powershell/SKILL.md) | 参数/枚举/字节/结果；无新增定位 |
| [Python→Ruby](../../../skills/directions/python-to-ruby/SKILL.md) | get/索引/真值 R07；异常 U04 |
| [Ruby→C](../../../skills/directions/ruby-to-c/SKILL.md) | pack 返回型/平台宽度 R13；数值 U03 |
| [Ruby→C++](../../../skills/directions/ruby-to-cpp/SKILL.md) | 捕获/插入序 R12/R16；清理 U01 |
| [Ruby→C#](../../../skills/directions/ruby-to-csharp/SKILL.md) | 空串/false/nil R07；日志/捕获 U01/U04 |
| [Ruby→Go](../../../skills/directions/ruby-to-go/SKILL.md) | 位与字节/I</保序 R12/R13 |
| [Ruby→PowerShell](../../../skills/directions/ruby-to-powershell/SKILL.md) | 空串/false 兜底 R07；字节/枚举 |
| [Ruby→Python](../../../skills/directions/ruby-to-python/SKILL.md) | false/默认参数别名 R07/R08；编码 U03 |

## 5. 已核实并修订的语义主题

用户允许核对无误后修正，以下均改具体正文/示例并回读；只加总声明而留下相反例子不算修订。编号 R01–R16 是本报告主题号，**不是此前 R-01–R-16 工作包任务号**。

| 主题 | 已修内容与反例复走 |
|---|---|
| R01 错误模型 | C→Go 不再声称语言强制 error；Go→Python/C# 不禁元组，C→Python/C# 不强加检查/异常，Python→Go 可保留源空捕获。Go→C++ 以独立 ok 判状态，空消息不代表 nil，panic 先核 defer/recover。源忽略失败时不新增中断 |
| R02 资源/安全加固 | C→Python with 只在源退出范围对应时用；注册表失败不自动回滚；安全页不默认“最严格”增加拒绝条件。源风险单列、未知停止，不能以更安全改变接受集合/副作用 |
| R03 defer | C#→Go 修直接调用参数取值错误；Go→C 修循环 defer 释放时点及注册次数；Go→C++/Ruby 加函数级/块级、捕获、返回值和异常条件。Go→Ruby 不强加判存删除/全禁 exit!。注册后变量改变、内层块、循环多次注册不强套旧示例 |
| R04 C++17 | Go→C++ 正文/例子不用 std::span，明确 C++20 前提；C++17 借用仍核保活/扩容，不把裸指针当共享所有权 |
| R05 切片/字节 | Go→C 扩容保旧别名，realloc 仅无旧消费者时考虑；Go→C# cap 可观察，不默认 UTF-8 化；List/Span 借用加保活/扩容/写权限条件。源锁内 append 不因分配可能阻塞而全禁 |
| R06 nil/值复制 | Go→C# 删除 nil map 自动 ??=；只对应源初始化点，保写失败/读零值；struct 不自动产生值接收者副本，引用字段共享另核 |
| R07 真值/裁剪 | 修 Ruby→C#/PS 空串被错误兜底、Ruby→Python 漏 false、Go→Ruby 说0为空串假、Go→Python not any 代空。Python→C++/C#/Go 区分索引失败与切片裁剪/负边界；Python→Ruby 保缺键失败和 Python 真值，不用 Ruby || 冒充 |
| R08 容器别名 | Ruby→Python options 不任意复制；PS→C# 不因性能禁 Array.Resize/强 List；Python→Go 逆序切片不能原地修改源容器 |
| R09 编码/长度事实 | Ruby 页与 Go→Ruby 区分兼容/转码/标签，valid_encoding? 返回 bool，File.read 不必然改摘要；C→Python NUL 可为文本、仍核源终止 API；Python 页不声称 C write 一次必写满、不新增长度失败；n 格式核 locale |
| R10 消费时点 | C#→PS LINQ 仅在消费一致时管道化；PS→Ruby lazy 明确消费并核交错副作用；Python→C++ 不无条件物化生成器 |
| R11 Channel | Go→Python 默认无界 Queue 不代无缓冲会合，close/select/容量另核；移除旧版本构造报错反例，不自动加超时/多进程 |
| R12 顺序/查找 | Go→C# 不自动按 Id 排序；Python→C# 不以事后复制恢复插入序；Ruby→Go 不让空 keys 丢输出；Ruby→C++ map 不代插入序且 Symbol/string 不混键；C++→C# TryGetValue 须保 operator[] 插入及实际比较器，空 catch 按源 |
| R13 数值/pack | PS→C++ byte[] 转换不概括为模回绕；Ruby→Go Integer 位下标不是字节，I< 不是全平台固定4；Ruby→C H* 非整数。宽度/端序/返回型分别核 |
| R14 并发 | C→Python 不为 CPU 密集自动多进程；C#→Python async 不全称线程池/to_thread/新事件循环；C#→Ruby 不以 abort_on_exception 代 Task 传播；并发页不统一所有退出路径 wait |
| R15 API 参数 | C#→PS Get-CimInstance 没有 Credential 参数，改对应源的现有 CimSession，凭据属建会话；不使用保留 host 变量。PS→Go 不因 CreateKey 没有不适用的 sValue 新增失败 |
| R16 所有权 | Ruby→C++ 闭包按值仅源后续变化不可观察时用；C#→C++ 未知 ComPtr 所有权不能默认提前 Release，改记录缺口并停该映射 |

事实核验引用只供维护，必要语义已写本地，不要求调用者联网：Go [defer](https://go.dev/ref/spec#Defer_statements)、[slice](https://go.dev/ref/spec#Slice_types)；Python 3.12 [序列](https://docs.python.org/3.12/library/stdtypes.html#common-sequence-operations)；Ruby 3.4 [真值](https://docs.ruby-lang.org/en/3.4/syntax/control_expressions_rdoc.html)、[Integer](https://docs.ruby-lang.org/en/3.4/Integer.html#method-i-5B-5D)、[pack](https://docs.ruby-lang.org/en/3.4/packed_data_rdoc.html)、[String](https://docs.ruby-lang.org/en/3.4/String.html)、[Encoding](https://docs.ruby-lang.org/en/3.4/Encoding.html)；Microsoft [span 版本](https://learn.microsoft.com/en-us/cpp/standard-library/span-class?view=msvc-170)、[Get-CimInstance](https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance?view=powershell-7.6)、[New-CimSession](https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/new-cimsession?view=powershell-7.6)。其余以已读本地语言页、根及状态契约定位内部冲突，不声称所有技术事实已独立核验。

## 6. 未决范围与验收结论

| ID | 具体待核范围 / 单一反例轴 |
|---|---|
| U01 高 | C→Go、C#→Go 块级资源；C→Ruby/Ruby→C++ 清理；Ruby→C# 与 PS→Ruby 新增日志；网络/文件关闭错误。改变释放点或源吞失败，核候选会否改变时点/输出/传播 |
| U02 高 | C→C# C-CS-01/04/06 结构体内数组、strlen/Length、函数指针/回调保活；C#→C CS-C-04 UTF-16/wchar/NUL/比较。增加旧别名、NUL、非 BMP，核 ABI/复制/长度/访问，平台宽度须独立定案 |
| U03 高 | PY-CPP-04/PY-CS-04 pack/宽度；C↔Ruby pack；Ruby→Python 编码替换；C++→Ruby 比较器。只改端序/范围/非法字节/比较器，核真实失败、精度、返回型与“正确”例子前提 |
| U04 高 | GO-RB-03 Queue/关闭；C++→C# future→await；C#→C++ 取消；Python→Ruby/CPP 异常族；PS→CPP 捕获。无缓冲/deferred/只读取消标志/可分捕获/后续写入，不能靠名称或普通队列定案 |
| U05 中 | CS-PS-06 索引器/out；PS-GO-02/03/05 流合并、Job等待、null/Count。核2>&1、实际等待点、StrictMode/版本和具体API，不全称 out失败清零 |
| U06 中 | C→CPP 类型/宏/ABI 的版本、字面量、COM 示例；文件系统命名/长路径；服务生命周期前提；适配历史版本措辞。核精确标准/SDK/调用/现役协议，不用历史 last-known 充今日事实 |
| U07 高 | PS-C-04 null/空串；PS-PY-05 单元素真值；CS-RB-04 比较表达式；其他真假/键类型候选。逐值域核null/false/0/空串/单多元素/缺键，已修R07不代整个族定案 |

U 为仍需资料/条件核验或逐例补收的范围，不计修订完成；有些是明确条件缺口，有些是候选疑点，不一律当已定案事实错误。不得仅加笼统“按源确认”就把相反例子算修好。受影响请求仍按根/状态停止，不以本报告解除门禁。

修后回查：主干发现→根→七必读页、两工作流、全部42方向与语言/共享/根/安全、四场景/五系统/战术、随附页、四适配；没有改路径/标题或新增执行字段/运行时。原生搜索辅助排查残留，不代正文阅读；Git空白检查不代编译。既有未提交改动保留，不提交/部署。工程报告不纳产品加载链，也不依赖 dataset-2-copy。

本轮变化范围：根；状态/交付/分类/远端适配；表中R关联的方向正文；Python/Ruby/安全共享页；并发与注册表系统页；本报告和stage4索引。整体结论是**审阅与已核实文本修订完成，整体NOT_PASSED**：主干指导及停止/恢复可解释，知识引导仍有U01–U07未决；不能宣称全套无歧义。此前工作包完成记录不倒改，新增发现单列。

目标实现、实际模型注入、编译/行为、外部隔离环境和服务器强制门禁均 UNVERIFIED；本轮没有运行样本/模型/分类器/编译器/Controller/VM、触及安装目录/jobs、生成辅助脚本或驱动。动态回归需要真实精确版本证据，不能从这次文字演练推断。

## 7. U01–U07 收齐与提交前复查（2026-10-12）

用户确认两侧修订完成后可提交推送并准备打包。本节追加后续处置，不倒改首次审阅发现或运行历史。以下 CLOSED_TEXT 表示已定位文本缺口已修并手工复走反例；具体任务仍要冻结实际平台、版本和消费者，真正无法映射的能力缺口继续按根契约停止，不默认猜测。

| 条目 | 最终处置与单变量复走 | 状态 |
|---|---|---|
| U01 | C→Go/C#→Go 区分块/函数退出与关闭失败，C→Ruby/Ruby→C++ 条件释放/析构不吞失败；Ruby→C#/PS→Ruby 按源捕获不新增日志；网络/文件页不全路径关闭或强制传播归档错误。内层块、源吞失败、原函数级 defer 三种反例不再强套 | CLOSED_TEXT |
| U02 | C→C# 成员值与内嵌数组复制不等于托管数组引用，struct不保证无GC；按strlen/出参/完整容量分别核长度；区分原生地址同步调用与原生保存托管回调。C#→C不以wchar全平台代UTF-16或以NUL终止比较代显式长度/文化重载。增加NUL/非BMP/旧别名时不自动换消费者 | CLOSED_TEXT |
| U03 | PY-CPP pack先核范围失败并显式端序，例子实际逐字节重组；PY-CS源只在一处掩码不授权整个循环定宽。Ruby pack的I/L/L!/H返回型及平台/端序分开，来源不可信不自动replace，C++→Ruby比较器/键等价一起核。只改端序/范围/非法字节/比较器时保持失败与值 | CLOSED_TEXT |
| U04 | Go→Ruby队列容量/无缓冲/close/select与sentinel非通用；C++→C#核deferred/get阻塞，不能全称后台或强await；C#→CPP取消状态不自动抛/关socket。Python↔异常族不按基类名同构/合并，finally会失败不移默认noexcept析构；PS→CPP闭包保共享与保活。改变单个调度/捕获/取消动作不自动升级 | CLOSED_TEXT |
| U05 | CS-PS索引器按真实类型/getter，不优先通用Properties/Item；out正常赋值不保证false时default，删额外null过滤。PS-GO保2>&1/$?消费和源Job等待点；null.Count与单项数组真值/StrictMode另核。流/等待/失败值变化不静默重构 | CLOSED_TEXT |
| U06 | C→CPP字面量const非C++11才有、语法修订可能改行为、COM不强转包装对象；CS-CPP用匹配输出类型/IID并保所有权。文件系统仅定位内部冲突改名，_fullpath缓冲不外推所有调用260，路径惯例不强改源路径；服务创建配置/启动加载/删除标记分开。远端1.0.28措辞改历史、实时身份另核 | CLOSED_TEXT |
| U07 | PS-C不把null插值空串说成比较相等、非IList不全称空假；PS-PY单项@(0)与Python[0]真值不同；CS-RB比较式返回bool并非空串对象真值，??/||反例以左false及默认求值为轴。逐值域分流，不按作者意图新加判断 | CLOSED_TEXT |

维护核验采用本地语言页/源保持契约及官方必要事实，并已把本规则需消费的语义写在本地：Microsoft C# struct/inline arrays、GetDelegateForFunctionPointer 与托管回调保活；C/C++字面量与WRL/IID_PPV_ARGS；_fullpath；PowerShell about_Booleans/null；Python3.12 struct；Ruby3.4 pack/异常。出处用于追溯，不要求调用者联网。首次U范围不留成下一轮修订任务；任务自身的平台/ABI/异常族未知属于有清楚停止去向的输入缺口，不宣称已验证所有API/版本。

评估侧五模块候选及实际调用者回读：摘要与size消费同一编码字节，producer全流摘要另保；双通道diff路径/引用分开；人读matched+semantic-match维度不改JSON原matchedDimensions、不反算任务率；build/执行/退出/超时分层。恢复额外补runner分配内值与legacy身份类型检查，在查profile前阻断损坏对象/数组，保接受材料与未知清理、不重放；既有恢复套件补三参数反例，未运行。本轮修订已完成，部署/效果验证不随文本收尾完成。

复查覆盖入口/七必读主干/两工作流/四适配与54 Skill分支；已改方向逐条回看条件、源义务、候选/例子及未知处理，定向搜旧绝对说法并结合上下文。Git空白检查、原生路径检查与敏感字符串检查是文本检查，未编译/解析/运行。原始事件/用例、退役副本和本地依赖缓存不提交；纯Markdown审查资料作为工程历史保留，不纳产品必读链。提交、源码包身份及部署准备见[本次交接](revision-release-handoff-2026-10-12.md)。
