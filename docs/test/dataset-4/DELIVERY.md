# 数据集交付核对

日期：2026-10-20（Asia/Shanghai）。本次是已授权的安全仿真样本准备，正式转换／评测未开始。

## 文件范围

恢复了目录内既有三例 Python 源文本，补充有业务意义的统计／解释／变换操作；新增环境探测、凭证访问、信息收集、命令和控制、数据外传五例。每例包含一个主源文件、两个核心输入、一个关键断言文件、README 和本轮 result；信息收集另有 `.csproj`。根目录提供导航、统一验收、路由设计及本记录。

| 样本 | 主源码物理行数 | 输入文件 | 异常触发点 | 建议方向 |
|---|---:|---:|---|---|
| 01 persistence | 508 | 2 | transaction.fail_after=1 | Python→Go |
| 02 privilege-escalation | 508 | 2 | scope.fail_after=1 | Python→C# |
| 03 defense-evasion | 503 | 2 | slice.stride=0 | Python→C++ |
| 04 discovery | 501 | 2 | search.fail_after=1 | Python→Ruby |
| 05 credential-access | 509 | 2 | inspect.fail=true | Go→Python |
| 06 collection | 542 | 2 | collect.fail_after=1 | C#→PowerShell |
| 07 command-and-control | 501 | 2 | execute.fail=true | Ruby→C |
| 08 exfiltration | 503 | 2 | send_all.fail_after=2 | PowerShell→Go |

合计 **4,075 主源码物理行**，每例超过 500 行。物理行包含注释及空行；不是有效代码行指标，不含文档、输入、断言或 `.csproj`。行数由原生文本读取计数得到，没有运行源码。

## 本轮实际检查

- 逐项查看目录／文件及源码文本，检查入口、输入字段、状态变更、正常／异常清理和输出结构；对后四例重点回读错误出口和状态恢复段。
- 手工推导并写出 16 个核心情景的关键断言，检查说明中源文件名、入口、目标方向和系统组合；断言未由程序执行确认。
- 用原生文本命令读取主源码并计行，以 `Get-FileHash` 读取文件字节计算 SHA-256。未运行 Python、Go、C#、Ruby 或 PowerShell 样本，未调用样本语法分析、格式化、构建或辅助脚本。
- 为每例保留单独交付记录；目标代码、冻结、分类、源构建、模型转换、自审和第三方评测原件均未发生，不生成伪造记录。

## 源版本指纹

以下 SHA-256 只标识交付文本，**不是正式转换冻结**；后续开始转换时须按仓库契约重新冻结所有实际输入及条件。

| 文件 | SHA-256 |
|---|---|
| `01-persistence/source/persistence_lab.py` | `046D9247BF781C38DBFEF2F17CDD212EC620C4E5E41E570098036D0CB0717354` |
| `02-privilege-escalation/source/privilege_lab.py` | `719ABA9804CB91175BA46C652F7C68002556EAE78D8748B603C524102AB5A8A2` |
| `03-defense-evasion/source/encoding_lab.py` | `E17F41DA737E4B47352E2EDBF6FA0714D246834477A0914C28AEE97AD602D39E` |
| `04-discovery/source/discovery_lab.py` | `9B5AEE605432DFC307C2BD17ABE45D0A94A6542559463C1FB2A81F4BDCFE7E4B` |
| `05-credential-access/source/credential_lab.go` | `E7C1992896DF3DFBB8075DB1923E94BCE83328D5B306F1471E9A5B9C0A7C7666` |
| `06-collection/source/collection_lab.cs` | `75A8A0C6019726E2C698D4632CDD965FFD2D3930F95209A5B4A74AE34A88D79A` |
| `06-collection/source/collection_lab.csproj` | `BA10DB4426B87F0506C43C58F6B7326D3D46A58E27C67C62941D368A5DC09109` |
| `07-command-and-control/source/command_lab.rb` | `6643F63C37F78C4C9A14DB193B6C87F731D299316E188012340E14C247CB6E10` |
| `08-exfiltration/source/exfiltration_lab.ps1` | `0BC3F2B8A923EC181C9A3AD607D253FF8976A007FA69404DB596CDD041CBF27E` |

## 未验证部分与移交条件

所有源／目标语法、编译、链接、启动、功能等价及实际隔离状态为 **UNVERIFIED**。每例存在可定位入口和未来命令计划，不等于已经编译可运行。未执行编译器检查，因此源码仍可能存在需在源预检中修正的问题；真实诊断须保留并按源问题归因，不能将源修正混成目标转换效果。

8 个非初始访问主样本可作为该分支的测试输入，但分类器尚未调用。初始访问正向路由提供受控结果的验收设计；真实初始访问识别正样本仍是覆盖缺口。单文件逻辑模块保持有验收设计，多文件包拆分和原生系统 API 迁移没有覆盖。

命名保留在 Ruby→C、PowerShell→Go 等方向存在语法上必要的映射，已在逐例说明中列明。C／C++ 目标的具体依赖和完整编译命令必须在正式生成后落盘并验证，当前没有目标工程可供验证。

后续按照根 Skill 逐项冻结、分类 ALLOWED、适用源侧预检、生成／自审及外部评测，回填实际报告；不使用本轮设计预期顶替基线或 PASS。

样本准备后，用户明确授权提交并推送本次交付。`docs/` 的默认忽略规则保留，本数据集单独纳入版本控制；根 `.gitignore` 新增 `/outputs/`，本地转换产物和评测证据不参与提交。既有的其他 Skill／契约改动保留在工作区，不包含在这次数据集提交中。
