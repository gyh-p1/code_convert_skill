# dataset-4：八类跨语言安全仿真样本

当前入口：本批八例已完成目标转换及正常／异常两个核心情景的隔离评测，原比较共 16 个 matched；只支持这些精确版本与情景的结论。最终目标及 job 导航见 [批次索引](batch/README.md) 和 [批次汇总](batch/summary.md)，交付限制及用户确认的当前能力口径见 [交付审计](CLIENT-DELIVERY-AUDIT-2026-10-20.md)。

本批反馈用于 [优化方案](OPTIMIZATION-PLAN-2026-10-20.md)，已实施内容与检查范围见 [优化实施记录](OPTIMIZATION-RESULT-2026-10-20.md)，评估产品待办见 [评估侧优化建议](EVALUATOR-IMPROVEMENTS-2026-10-20.md)。以下样本准备说明及各原始类别目录的 result.md 记录准备阶段历史；当前转换结果以方向目录的 output/batch/result.md 为准。

评估方案已结合用户补充的 dataset-3 两份归因报告和 Controller 恢复文档扩展为 E1–E16，新增本地分诊／超时／比较保护及管理者授权智能体维护的规则，实施与未部署范围见 [评估增补实施记录](EVALUATOR-OPTIMIZATION-IMPLEMENTATION-2026-10-20.md)。

评估产品源码的首批及续轮开发现已完成本方案可独立开发部分，最终维护回归 857 项及分类器 79 项通过，见[最新开发收口](../../../../third-party-evaluation-system/docs/evaluator-optimization-completion-2026-10-20.md)。真实部署、离线供给及隔离环境复验仍待进行；这些维护测试没有重评本批 D4，不增加或升级上述 16 个 matched 的结论。

准备阶段交付 **8 个原创安全仿真源程序、16 份核心输入、8 份预期断言、逐例测试说明和分流验收设计**。来源为本会话直接编写，未从外部攻击工具复制。前四例延续已有 Python 样本，后四例使用 Go、C#、Ruby、PowerShell。

样本准备阶段只交源代码和测试说明，当时转换／评测尚未开始。`fixtures/expected.json` 是按源文本推导的测试预期，**不是运行结果或评测证据**；之后取得的动态证据、有限通过和未决项见上方当前入口，不能用历史准备状态覆盖后续结果。

## 样本与方向

下表保留样本准备时的方向配置；实际已验系统／工具链及覆盖以批次索引和精确 job 为准，不能外推整个方向。系统采用 x64 Windows 与 x64 Linux；macOS 未纳入。源码均只处理 stdin 中的合成数据，在内存中改变虚拟状态，不读取宿主资产、凭证或文件，不监听或连接网络。

| 编号／类别 | 源程序 | 方向 | 源系统 → 目标系统 | 主要非直接映射 |
|---|---|---|---|---|
| [01 持久化](01-persistence/README.md) | `persistence_lab.py` | Python → Go | Windows → Linux | `contextmanager` + 深复制事务 → 显式快照／恢复 |
| [02 提权](02-privilege-escalation/README.md) | `privilege_lab.py` | Python → C# | Linux → Windows | 生成器上下文作用域 → `try/finally` 或 `IDisposable` |
| [03 防御规避](03-defense-evasion/README.md) | `encoding_lab.py` | Python → C++ | Windows → Linux | 负步长切片及省略边界 → 显式索引归一化 |
| [04 环境探测](04-discovery/README.md) | `discovery_lab.py` | Python → Ruby | Linux → Windows | 生成器 `close()` → 显式关闭／块作用域清理 |
| [05 凭证访问](05-credential-access/README.md) | `credential_lab.go` | Go → Python | Linux → Windows | `defer` + 多返回值错误 → `try/finally` + 异常 |
| [06 信息收集](06-collection/README.md) | `collection_lab.cs` | C# → PowerShell | Windows → Linux | `yield return` 枚举器释放 → 显式枚举和 `finally` |
| [07 命令和控制](07-command-and-control/README.md) | `command_lab.rb` | Ruby → C | Linux → Windows | block／`ensure` → 状态码与统一清理出口 |
| [08 数据外传](08-exfiltration/README.md) | `exfiltration_lab.ps1` | PowerShell → Go | Windows → Linux | 管道数组解包／空数组 → 有类型字节切片 |

共 8 个不同方向，源侧 5 种语言，源／目标合计覆盖 C、C++、C#、Go、PowerShell、Python、Ruby 7 种语言。这里只选取 8 个方向，未覆盖全部 42 个有向组合。系统迁移测试覆盖启动方式、编码、换行、整数／集合和资源清理语义；不覆盖注册表、真实令牌、原生服务、驱动或系统漏洞利用。

## 文件使用方式

每例的 `source/` 是正式源输入，`fixtures/normal.json`、`fixtures/exception.json` 是两次**独立启动**的 stdin，`fixtures/expected.json` 使用 JSON Pointer 指定关键字段预期。原类别目录的 `README.md` 和 `result.md` 保留准备阶段观察设计／计划命令及状态；实际目标、命令与证据从上方批次索引进入。

一次进程仅消费一份 JSON 文档，EOF 后退出。操作内部的预期异常通常写入 `outcomes`／`history` 并继续，进程退出码仍为 0；文档或初始化错误返回根级 `error`，退出码为 2。不能把业务错误对象误判为进程崩溃，也不能把退出码 0 误判为转换等价。

逐例核心断言只是诊断辅助。正式比较还应检查两侧完整解析 JSON、stdout 文档数量、stderr、退出码和副作用，执行 [统一验收](ACCEPTANCE.md)。语言映射说明允许实现差异，不免除行为义务。

## 后续评测前提

仅在另行获批、断开公网和生产网的一次性隔离 VM 中执行逐例 README 中的命令。本机不运行这些程序、构建命令、解析器或自动测试脚本。本集不带调度脚本、评测驱动或批量转换工具。

建议冻结 CPython 3.12、C# 12/.NET 8、C11、C++17、Ruby 3.4；Go 和 PowerShell 采用平台实际提供并留证的版本。Go 源使用 `any`，至少需要 Go 1.18；PowerShell 源采用 `-AsHashtable`、`-NoEnumerate`、.NET 十六进制 API，计划用 PowerShell 7.4+，不适用于 Windows PowerShell 5.1。版本可用性尚未核验。

C/C++ 目标必须提交完整可构建工程及依赖锁定／清单：JSON、Unicode、压缩功能不能用未提交的占位函数替代。依赖提前放入隔离环境，禁止构建时临时联网下载。解释型目标也须通过其对应语法检查与实际启动；不把“没有编译步骤”写成编译 PASS。

继续转换或扩展评测前重新读取仓库 Skill，按真实文件、当前能力和既有版本逐项核冻结、分类准入及适用源侧预检。本批已有记录见方向目录和批次索引；不能用本目录的战术标签代替分类器准入，也不能从已关闭批次直接继承新版本 PASS。

## 分类和覆盖边界

战术标记沿用仓库 [ATT&CK 本地索引](../../../skills/attack-tactic-index/SKILL.md) 的分类口径，不宣称外部最新标准。第 03 例保留用户“防御规避”类别，源中标为 `Defense Evasion (legacy category) / Stealth`；它仅模拟惰性字节变换，不包含 Defense Impairment 行为。

第一例按持久化组织。初始访问／非初始访问分流与等价性通过／不通过组合见 [routing-cases.json](routing-cases.json)。这部分是待实现系统的受控输入验收设计；8 个主样本均非真实初始访问代码，因而**不能据此宣布初始访问识别正样本已验证**。正向分流可用获批平台注入的分类结果测试；真实识别正向能力仍需另补经授权样本和分类证据。

文件行数、静态回读范围及剩余限制见 [交付记录](DELIVERY.md)。`docs/` 默认被仓库 `.gitignore` 忽略；本数据集按用户后续明确授权单独纳入版本控制。`outputs/` 保持本地，不随数据集提交。
