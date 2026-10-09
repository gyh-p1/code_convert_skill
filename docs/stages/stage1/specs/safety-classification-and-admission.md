# Spec 01｜静态分类与执行准入

> 版本：3.1；更新：2026-10-09
> 实现：tools/safety_classifier_v2.py 内部版本 2.3；静态回归及六批文本分析已完成
> 约束：[安全边界](../../../../references/framework/safety-boundary.md)
> 准入规则以 [Spec04](tiered-admission-policy.md) 为准；本文件描述分类与输入输出

## 1. 责任与消费方式

分类器只读源码文本，提供任务审阅分流，不导入样本、不执行源码、不联网、不提交 Controller。分类结果是线索，不是安全证明。输入中未包含目标代码、构建脚本或中性驱动时，它们也不在本次分析范围内，准入者必须补审。

保留 SafetyClassifierV2.classify(task_id, direction, case_id, source_path) 及三位置参数 CLI；保留 id/dir/case/cls/reason/details/executable 字段。原内部 BehaviorAnalysis/NetworkTarget 数据类和方法形状不再承诺兼容，未发现外部调用者。主类仍叫 V2 是为兼容既有调用名称，不表示算法未改。

重大语义变化：executable 恒为 false。`executionApproved` 自 v2.2 起不再恒为 false，而是与 `admissionStatus` 一致（Spec04 §5.1）；它表达“按 Spec04 未落入阻断项”，**不等于**平台执行许可。不得用分类 JSON 自动生成“安全任务队列”；消费者按 reviewGroups 分配审阅，再由独立的冻结/授权/隔离记录确定执行资格。

## 2. 输入与完整性

支持旧分类列表或含 tasks 的 batch 对象；正式六批使用 batch.json，taskCount 必须匹配。必需唯一 taskId/id 与 direction/dir；case 缺省可由 casePath 推得。缺失/重复身份保留 BLOCKED_INPUT，不跳行。

文件选择优先按 sourcePath/sourceSha256，或 sourceDir/sourceFiles{name,sha256}；旧列表回退到 `<manifest目录>/direction/case/source`。声明但缺失的文件仍检查；同时遍历源目录伴随文件，避免只看首文件。

**路径解析（v2.3）**：声明路径先相对**清单自身所在目录**解析，再依次在"清单目录"与 `source_base` 两个包含根内做包含检查。
两个根都经过完整 resolve，任一通过即可；`source_base` 始终参与，因此清单无法自行扩大读取范围。
越界、符号链接/junction、源哈希不符、无法读取、不支持编码、含 NUL、单文件超过2 MiB或文件数超过128均作为输入错误。
UTF-8/BOM 可读；不再 errors=ignore。这些上限用于约束静态扫描，不是语言容量或转换能力指标。

> v2.2 曾把声明路径仅按相对 `source_base` 解析，使相对清单自身的写法全部误判为 `BLOCKED_INPUT`。
> 六批因路径写法恰好与根相对等价而未暴露该缺陷；两种写法现由回归固定覆盖。

.text/.txt 仅在已声明 powershell 方向时按 PowerShell 基本词法读取，details 记录 languageBasis；其余不识别扩展名保留 REVIEW_UNCERTAIN。
不自动改名、不恢复杀软文件、不猜缺失源码替代品。39 条缺失的成因与逐条可恢复性见[恢复性核查](../../../test/dataset/stage1-admission-recheck-2026-10-09/missing-input-recovery.md)。

## 3. 分类、优先级与人工动作

按下表从上到下选一个主分类；reviewGroups 保留所有命中维度，所以主分类不是完整行为描述。

| 分类 | 判定线索 | 后续动作 |
|---|---|---|
| BLOCKED_INPUT | 文件缺失/不可读/身份或哈希问题/路径与资源限制 | 数据维护者恢复或重新冻结，保留旧记录 |
| REVIEW_DEPENDENCY | Metasploit 等已识别框架线索 | 核对真实入口与框架环境；有 main 不消除框架依赖 |
| REVIEW_UNCERTAIN | raw string、here-string、heredoc、编码/扩展名等基本词法覆盖不足 | 人工逐文件检查；不得推断安全 |
| REVIEW_SENSITIVE | 敏感系统 API、动态代码、可执行内存、凭据相关线索 | 核对合成对象、权限、环境及禁止副作用 |
| REVIEW_NETWORK | 字面目标或网络 API；可能未解析地址 | 冻结地址/输入、网络行为、允许目标及当前隔离证据 |
| REVIEW_SIDE_EFFECTS | 文件、进程或环境信息采集线索 | 核对工作目录、子进程、资源和数据范围 |
| LOW_SIGNAL | 未命中已知线索 | 仍需审阅入口、依赖和目标；不是 SAFE |

网络 scope 分为 loopback、wildcard、private、public、special、hostname、invalid-ip；无字面目标但有网络调用为 unresolved，无已知网络线索为 none-detected。私有地址仅指地址段，绝不表示封闭实验网。赋值中的地址仍是 literal；所有目标 redirectVerified=false。

## 4. 输出与溯源

输出为原有列表外形，每条保留身份、主分类、原因，并增加 classifierVersion、classifierSha256、inputManifestSha256、executionApproved、admissionStatus、blockingReason、requiresNetworkIsolation、requiresSyntheticData。details 中包含：

- reviewGroups：network/filesystem/process/discovery/sensitive/dynamic_code/framework 的命中集合；
- files：文件名、SHA-256、每类命中行号、目标地址/scope/行号、credentialFindings（脱敏摘录与长度）、解析局限、语言判定来源；
- inputErrors：缺失、读取或身份检查错误；
- analysisScope=source-text-only，及未分析目标/驱动/隔离/授权的统一限制。

只保留线索和位置，不复制整段源码到报告。凭证线索只输出脱敏摘录与长度，疑似密钥全文不落盘。多层目录中的同名文件仍须结合输入清单定位；当前输出只列 basename，人工审阅不能仅凭 basename 断定文件身份。原输入及完整路径保存在冻结清单中。

输出文件以独占创建写入，已有文件报错，不能覆盖冻结源、旧分类或已有报告。上层执行者为每次重跑分配独立目录；同一版本只按最终 accepted 目录计数。进程意外中断可能留下不完整的新文件，恢复时先核验 JSON/条目数，另记新运行，不把半文件当成功。

## 5. 本次执行与回归

用户明确要求修订并重跑分类工具，本次只运行该工具及合成单元回归；没有运行样本、构建脚本或转换产物。该授权不扩大其他本机执行边界。

从仓库根调用已存在的文件：

~~~powershell
python -I -B tools/test_safety_classifier_v2.py
python -I -B tools/safety_classifier_v2.py docs/test/dataset/batch-01/batch.json <新输出路径> docs/test/dataset
~~~

如需按 Spec04 §3.2 放行公网目标，须先取得真实隔离证据，再加 `--network-isolation-configured`：

~~~powershell
python -I -B tools/safety_classifier_v2.py <batch.json> <新输出路径> docs/test/dataset --network-isolation-configured
~~~

六批同样处理，输出不能沿用已存在文件。-I 避免加载同名模块，-B 避免生成 pyc；被分析的文件只经 read/decode/字符串扫描。

回归覆盖：硬编码赋值、动态网络、IPv4/IPv6及通配地址、行/块注释、字符串内 URL、文件名非域名、文件/进程/环境采集、可执行内存/注册表/内核线索、WMI、原生 PowerShell、框架依赖、缺失/解码/哈希/越界/重复身份、多文件、输入守恒及输出保护；v2.3 起另覆盖 Spec04 三条准入规则（含规则2优先于规则3）、隔离开关开闭、清单相对与父级相对两种路径风格、URL userinfo、标识符边界及凭证摘录脱敏。当前 **47/47** 通过，详情见[重跑报告](../reports/最高危阻断策略修订与六批复跑.md)。

## 6. 已知局限与下一轮实验

词法启发式无法覆盖别名、动态拼接、条件编译、反射、间接调用或所有多语言字符串语法；命中 API 名和 import 也可能不实际执行，不能提供完整行为可达性结论。框架检测当前主要覆盖 Metasploit，不是全依赖解析。

下一轮在冻结样本中独立标注真实线索位置及预期分流，再保持样本/标注不变只改规则；分别统计输入完整性、各类 precision/recall、未知比例与误漏案例。当前未取得独立全量标注，不能把45个测试通过或全量输出解释为准确率100%。

凭证规则（Spec04 §3.3）只识别凭证**格式**：私钥块、常见云/平台令牌前缀、JWT、带密码的 URL。它不识别自由文本密码、哈希口令或拼接构造，因此"0 条命中"不能读作"数据集中确无真实凭证"，仍需人工确认。

运行准入还需独立核对当前平台契约、入口、两侧产物、oracle、合成数据、网络/文件/进程边界与清理；T04消费这些记录，不消费一个“SAFE”布尔值。
