# DeepSeek harness B 审阅逐项记录 01（D2-081–D2-100）

> 范围：`docs/dataset-2/dataset-2-copy/manifest.csv` 的 D2-081–D2-090（Kind=NEW，manifest 行 81–90；**注意任务书给的"D2-0NN 在第 NN+1 行"公式在本文件不成立——本文件 D2-081 在第 81 行，第 82 行是 D2-082**）。状态：前 10 项完成，后 10 项（D2-091–D2-100）待续。限制：原源/目标正文已删、本会话不复原、不编译、不运行、不调模型、不提交、不访问 Controller/jobs；`read`/`grep` 对单行 JSON 截断到约 2000 字符，截断件已逐件标注 `可见部分（工具2000字符/行截断）`，其余内容本会话读不到，**未按"已读全文"登记**。
>
> 覆盖口径：`现存文件数` 为该 case 目录下实际存在的文件数（含 `01-frozen`/`02-conversion`/`03-self-review`/`04-evaluation/<job>`/根层；不含 `batch/items/D2-0NN.json`，该件另行逐项读过）。`缺件` = 本项逐条列举的"应有件或原件缺失"数（含已删原源/目标正文、未取回 job 原件、被冻结记录引用但不存在的文件）；**未发生的阶段件（0 模型调用下的 02/03、未提交的 job-01、未生成的目标）记"不适用"、不计入缺件**。可选 `evaluation_report.md` 未取回只记文字、不计入缺件。

## 覆盖清单（供 harness-b-coverage.md 汇总）

| 项 | 实际目录 | 现存文件数 | 已读 | 已读(截断) | 未读 | 空文件 | 缺件 |
|---|---|---|---|---|---|---|---|
| D2-081 | `cpp-to-csharp/D2-081-cpp-str_cat.cc` | 11 | 11 | 1 | 0 | 0 | 3 |
| D2-082 | `cpp-to-go/D2-082-cpp-t1218.cpp` | 18 | 18 | 2 | 0 | 0 | 8 |
| D2-083 | `cpp-to-go/D2-083-cpp-cppwsmanwinrm.cpp` | 3 | 3 | 0 | 0 | 0 | 3 |
| D2-084 | `cpp-to-go/D2-084-cpp-civil_time.cc` | 13 | 13 | 1 | 0 | 0 | 3 |
| D2-085 | `cpp-to-go/D2-085-cpp-match.cc` | 13 | 13 | 1 | 0 | 0 | 3 |
| D2-086 | `cpp-to-go/D2-086-cpp-str_split.cc` | 13 | 13 | 1 | 0 | 0 | 3 |
| D2-087 | `cpp-to-go/D2-087-cpp-substitute.cc` | 11 | 11 | 1 | 0 | 0 | 5 |
| D2-088 | `cpp-to-powershell/D2-088-cpp-safe_attck_cpp_suite-resource_manifest_builder.cpp` | 40 | 40 | 7 | 0 | 0 | 10 |
| D2-089 | `cpp-to-powershell/D2-089-cpp-shell-aes.cpp` | 23 | 23 | 4 | 0 | 0 | 9 |
| D2-090 | `cpp-to-powershell/D2-090-cpp-env_detect.cpp` | 13 | 13 | 1 | 0 | 0 | 6 |
| **合计** | 10 个目录 | **158** | **158** | **19** | **0** | **0** | **53** |

另读：`docs/dataset-2/dataset-2-copy/batch/items/D2-081..D2-090.json`（10 件，全部存在，多行 JSON、无截断）。10 项全部有实际目录、无空目录；10 项**均无** `case.md`、无 `source/`（原源正文与快照已删）、无根层 `target.*`。

## 发现汇总（供 harness-b-findings.md 汇总）

1. **B-01｜五项 Abseil 翻译单元同一根因：源快照缺 absl 头 → `SOURCE_DEPENDENCY_GAP`**｜分类：源已有（数据集快照依赖不全）/环境｜依据：D2-081 `job-00/returned-evidence/evidence-source.json` `build.status="failed"/exitCode=1` 且 `stderr.normalizedText` 含 `fatal error: absl/strings/str_cat.h: No such file or directory`；D2-084 `absl/time/civil_time.h`；D2-085 `absl/strings/match.h`；D2-086 `absl/strings/str_split.h`；D2-087 `absl/strings/substitute.h`；对应 `batch/items/D2-08*/sourcePrecheck.diagnostic`｜边界：源正文已删，无法复核 include 行以外内容；不记转换失败、0 模型调用。
2. **B-02｜6 项缺 `result.md`，另 2 项在冻结记录里明示"无 result.md"**｜分类：已有规则落实（现行文本要求）｜依据：[交付契约 §1.1](../../../../../references/framework/delivery-handoff-contract.md) 第 15、17 行"任何提前停止都走同一收尾入口……（含分类阻断、源预检失败/缺基线、评估准备缺口、仅编译、跳过及 WAITING）"、"不论是否生成完整目标、不论成功/失败/阻断，都须有一份中文报告"；同文 §2.1.1 第 105–111 行去向/必备件表；[任务状态契约 §4](../../../../../references/framework/task-state-contract.md) 第 110 行。缺失实证：D2-081/083/084/085/086/087 目录 glob 无 `result.md`；D2-089 `01-frozen/frozen-inputs.md:26`、D2-090 `frozen-inputs.md:24` 明写"无 `target.ps1`／`result.md`／`job-01-dual-build`"｜边界：历史记录不改写，本项只登记现行规则下的交付缺档。
3. **B-03｜manifest `Lines` 与冻结记录源行数不一致（088/089/090）**｜分类：未定（源已删，行数定义不可复核）｜依据：`manifest.csv` 行 88–90 记 `63/73/76`，而 D2-088 `frozen-inputs.md:6` 记"70 行 CRLF，2138 字节"、D2-089 `frozen-inputs.md:4` 记 `sourceLines: 89`、D2-090 `frozen-inputs.md:4` 记 `sourceLines: 90`｜边界：D2-088 冻结自称"按 README §4 不影响用例有效性"并登记不改写清单；本审阅同样不 patch 清单。
4. **B-04｜D2-088 冻结记录引用的分类文件在副本中不存在，现存分类结果只覆盖 1 个文件**｜分类：装置（证据归档不齐/编号错位）｜依据：`frozen-inputs.md:13` 称"两次输入/输出均留证（`*-attempt1.json` 为失败尝试）"、第 63 行称"本次分类输入 `classifier-input-2files.json`，结果 `classification-2.json`"；但 `01-frozen/` 实际只有 `classifier-input.json`（列 2 个文件）与 `classification-1.json`（`details.files` 只有 `resource_manifest_builder.cpp` 1 项）；真正覆盖 `run_case.py` 的结果只存在于 `04-evaluation/job-00-source-buildability/this-task-classification.json`（`details.files` 2 项、`reviewGroups:["filesystem","process"]`）与 `job-01-dual-build/this-task-classification.json`｜边界：`source/run_case.py` 正文已删，无法独立复核该驱动内容；不改历史分类原件。
5. **B-05｜D2-089 分类输入与分类结果的文件集合镜像错位**｜分类：装置｜依据：D2-089 `01-frozen/classifier-input.json` 只列 `shell-aes.cpp` 1 个文件，而 `classification-1.json` 的 `details.files` 列 `run_case.py` 与 `shell-aes.cpp` 两项（`inputManifestSha256` 两者一致为 `a74f1f8f…7903`）｜边界：同 B-04，属归档对应问题，不是分类判定错误。
6. **B-06｜D2-088 job-00 与 D2-089 job-00b 用占位目标提交，平台据此回传 mismatched/failed**｜分类：装置（旧占位预检装置）｜依据：D2-089 `job-00b-fpermissive/returned-evidence/evidence-target.json` `execution.stdout.normalizedText="D2-089 placeholder\n"`，同 job `evaluation_report.json` `outcome.runVerdict="partial-runnable"`、`codeVerdict="failed"`、`behaviorVerdict="mismatched"`；D2-088 `job-00/returned-evidence/evaluation_report.md` 同样 `FAIL/MISMATCHED`，而 `job-00/metadata.json:9` 自述 `target/target.ps1 (precheck placeholder)`｜边界：**这些 mismatched/failed 是占位装置产物，不得当作转换失败**；现行[评估准备 §1.1](../../../../../references/framework/evaluation-readiness-contract.md) 第 31 行与[交付契约 §2.1.1](../../../../../references/framework/delivery-handoff-contract.md) job-00 行已提供 source-only 预检机制，无需再新增占位机制；原 verdict 不改写。
7. **B-07｜D2-089/090 的 `batch-authorization.json` 数据源说明是另一项（D2-151）的文本**｜分类：装置/流程（授权记录未按项定制，可能误导隔离与数据核对）｜依据：两项 `04-evaluation/job-00-source-buildability/batch-authorization.json` 第 21 行均为"该项 D2-151 无网络、无凭证, 仅本地文件删除与只读遍历, 使用合成 fixture (keep.txt/second.txt)"，而 D2-089 实为 loopback 网络样本（`classification-1.json` `network_mode="loopback"`、`127.0.0.1` L62）、D2-090 为动态 API 解析（`dynamic_code` L84）｜边界：仅文本复核，未据此判断授权本身有效性；`vmIsolation`/`networkIsolation` 字段本身格式完整。
8. **B-08｜D2-088 job-01 的 `targetHash` 不是哈希，最终目标版本未在该 job 记录中绑定**｜分类：装置（版本关联可追溯性不足）｜依据：`job-01-dual-build/metadata.json:11` `"targetHash": "sha256:target-v2-self-repair-round-1"`（字面标签，非 64 位十六进制）；`batch/items/D2-088.json:39` 的 `finalTargetSha256="e9f9c25d…ff49"` 与 `02-conversion/target.self-repair-1.model.json:8` 的 `outputSha256` 相同，但该值未出现在 job-01 材料中；[交付契约 §2.2.1](../../../../../references/framework/delivery-handoff-contract.md) 要求"目标版本……父/新目标身份与差异"可回读｜边界：目标正文已删，不能由 item/model 哈希还原实现事实。
9. **B-09｜D2-088 自修稿与交付稿的落点/命名三处不一致**｜分类：装置｜依据：`03-self-review/self-review-1.json:24` `appliedTo="02-conversion/target.v2.ps1"`；`result.md:18` 写目标文件为 `04-evaluation/job-01-dual-build/target/target.ps1`；`02-conversion/` 实际只有 `target.self-repair-1.proposal.json`/`target.self-repair-1.model.json`（无 `target.v2.ps1`、无 `target.self-repair-1.ps1`、无 `target.gen.ps1`），根层 `target.ps1` 与 `job-01/target/` 均不存在｜边界：三处都无法由本副本核对哪份是最终交付版本；不改历史记录。
10. **B-10｜D2-088 只取证 `output` 维度，文件字节义务仅静态支持**｜分类：已有规则落实（分层报告口径被执行）｜依据：`job-01/returned-evidence/comparison.json` `dimensions.filesystem.status="not-applicable"`；`evaluation_report.md` 证据矩阵 `Filesystem | not-applicable`；`result.md:46` 自述"其字节一致性目前仅由静态复审（自修 CRLF）支持，**不是行为证据**"，`coverageGap` 亦记同一内容｜边界：`matched` 只覆盖 `output` 维度（1/1），**不得**说成完整功能覆盖；现行[评估准备 §5](../../../../../references/framework/evaluation-readiness-contract.md) 与交付 §2.3 要求正与此登记一致。
11. **B-11｜"Windows 文本模式 LF→CRLF"义务：现行语言/共性/场景页已覆盖，cpp-to-powershell 方向页缺文件写入专条**｜分类：已有规则落实 + 知识新增（方向页专条候选）｜依据（均已实际打开核对现行文本）：[C++ 语言页](../../../../../skills/references/languages/cpp.md) 第 109 行"`std::ofstream`…在 Windows CRT 文本模式下 LF 可翻译为 CRLF，**不能**由'C++ 流'推断输出为裸 LF"、第 121 行示例注"文本模式可能翻译换行"、第 130 行"禁止用 `std::endl` 的'刷新'副作用代替换行语义"；[七语言共性语义](../../../../../skills/references/seven-language-common-semantics.md) 第 82 行"确保文本/二进制打开模式与平台换行符（CRLF vs LF）一致"；[文件 I/O 场景](../../../../../skills/scenes/file-io/SKILL.md) 第 62 行 CRLF↔LF 翻译与字节精确要求；同族方向 [cpp-to-csharp SKILL.md](../../../../../skills/directions/cpp-to-csharp/SKILL.md) 第 145–152 行有 CPP-CS-07"Windows 文本模式标准输出的行尾与刷新语义"（含反例"裸 LF 不保留本例的 CRLF"）；而 [cpp-to-powershell SKILL.md](../../../../../skills/directions/cpp-to-powershell/SKILL.md) 只有 CPP-PS-01（stdout 通道与格式，第 18–33 行）与 CPP-PS-06（文件流失败仍继续，第 112–119 行），**无"文件写入换行义务"专条**｜边界：D2-088 的 CRLF 修复本身无行为证据（见 B-10），本条只是知识覆盖对照，不证明修复正确。
12. **B-12｜D2-082 首次源预检失败被正确归因为契约缺陷而非源不可构建，修正命令后 completed/0**｜分类：已有规则落实｜依据：`batch/items/D2-082.json:20-33` 与 `frozen-inputs.md:29-38`；`job-00`（`eval-20261010-044201-4a88cf65`）`evidence-source.json` `build.status="failed"/exitCode=1` 且 stderr 为 `invalid conversion from 'FARPROC'…to 'LPVOID' [-fpermissive]`；`job-00b`（`eval-20261010-044302-863f0cdc`）`evidence-source.json` `build.status="completed"/exitCode=0`，同诊断降为 `warning`；构建命令由 `g++ -std=c++17 -shared T1218.cpp…` 改为加 `-DUNICODE -D_UNICODE -fpermissive`。对照现行[构建前提 §0.1 三分法/§4.1](../../../../../references/workflow/build-prerequisites.md) 第 40–48、142 行｜边界：只支持该精确源快照与命令，不外推其它 runner/OS。
13. **B-13｜D2-089 同型契约修正（`-fpermissive`）两次 job 命令与诊断均留证；但冻结引用的"§10.x"编号在现行文本中不存在**｜分类：已有规则落实 + 未定（历史编号待核）｜依据：`frozen-inputs.md:13-18` 实验 A/B 表；`job-00` `evidence-source.json` build failed/exit 1（`char*→BYTE*` L45 等）、`job-00b` `evidence-source.json` build completed/0 同诊断降 `warning`；两 job 的 `comparison_manifest.json` 各自保存了 A/B 两条精确命令，符合[构建前提 §4.1](../../../../../references/workflow/build-prerequisites.md) 第 142 行"须保留原命令、诊断与契约变更理由"｜边界：`frozen-inputs.md` 引用的"§10.17/§10.6/§10.16"在当前 `references/` 与 `AGENTS.md` 中未核到对应编号，属历史编号，**不能据编号反推当时的规则文本**。
14. **B-14｜D2-082/089/090 在"本轮无法合法评估行为"时均未生成目标（0 模型调用），与现行 LIB_UNOBSERVABLE_COMPILE_ONLY 分支方向不一致**｜分类：未定/待核（历史执行与现行分支差异）｜依据：D2-082 `frozen-inputs.md:40-80` 判"驱动四要素四项全 FAIL"→`RUN_SAFETY_NOT_READY`、`lifecycle WAITING`、item `usage.requests=0`；D2-089/090 判 `ORACLE_NOT_FREEZABLE`/`DRIVER_NOT_VIABLE`、`lifecycle PARTIAL`、`未进入生成 ⇒ 0 模型调用`。现行[评估准备 §1.3](../../../../../references/framework/evaluation-readiness-contract.md) 第 41–47 行规定"本轮无法合法评估行为、但源可构建的，记 LIB_UNOBSERVABLE_COMPILE_ONLY，**继续转换**并验证目标语法/编译"、"不因缺 main、可执行文件、stdout 或合法入口直接跳过"，并"适用件齐备后 PARTIAL"，明确其**不是不可转换去向**；§4 第 87 行只要求 `ORACLE_NOT_FREEZABLE` 停止**该行为评估**并部分交付｜边界：三项源侧均 `build completed/0`（082 经契约修正后、089/090 用 `-fpermissive`），按现行文本本应进入生成并取目标语法/编译证据；但不得把当时按旧编号（§10.x）执行的处理追认为违规，只登记差异与后续可补动作。
15. **B-15｜D2-090 源执行 timed-out，平台把它记为 `CODE_RESULT/code`**｜分类：装置/环境（观察装置不足）｜依据：`job-00/evidence-source.json` `execution.status="timed-out"`、`durationMs=30022`、`timedOut=true`、stderr 17 字节 `command timed out`、stdout 0 字节；`evaluation_report.json` `outcome.codeVerdict="inconclusive"`、`failure.type="CODE_RESULT"`、`category="code"`、`reason="Source execution timed-out; baseline unavailable."`；冻结据源码（`MessageBoxA` 在 headless VM 不返回 + ASLR 地址输出）判定驱动第④要素不满足｜边界：现行[评估准备 §2](../../../../../references/framework/evaluation-readiness-contract.md) 第 68 行把同类观察装置缺陷归 `INCONCLUSIVE`；**不得**据平台 `codeVerdict` 反推代码缺陷，也不得据此宣称源不可构建（`build completed/0` 已在同一 evidence 中）。
16. **B-16｜job 环境/清理记录不齐；D2-086 提交前快照显示 Windows runner 正在 CLEANING 但该 job 仍成功**｜分类：装置（原件不齐）＋已有规则落实（CLEANING 快照非门禁）｜依据：D2-081/087/089/090 的 job-00 与 D2-089 的 job-00b 均**无** `controller-health-before.json`/`runners-before.json`；D2-082/084/085/086 有；全部 10 项只有 D2-088 `job-01` 取回 `controller-health-after.json`，其余 job 无 after/closure 记录。D2-086 `job-00/controller-health-before.json`：`readyRunnerCount=2`、`blockedRunnerCount=0`、`blockingReasons:["busy:CLEANING"]`、`checkedAt=04:46:49`，`runners-before.json` 中 `windows-vm-agent-x64` `lifecycleState="CLEANING"/ready=false`，而 job 于 `04:47:25` 创建、`04:48:03` 完成且 report 两侧 `cleanup PASSED`/`runnerStateAfter READY`。对照[评估准备 §1](../../../../../references/framework/evaluation-readiness-contract.md) 第 18 行"READY/clean/快照不证明隔离"与[交付契约 §2.1.1](../../../../../references/framework/delivery-handoff-contract.md) 环境/清理记录要求｜边界：CLEANING 快照是提交前状态、不是装置失败；after/closure 缺件属取回不齐，不改变既有 build/behavior 事实。
17. **B-17｜冻结记录普遍缺"知识与模型"组（selected skills 路径+哈希、温度、RAG、不发送 max_tokens 约定），仅 D2-082 记录**｜分类：已有规则落实（缺口）｜依据：[任务状态契约 §2](../../../../../references/framework/task-state-contract.md) 第 20 行表格要求"知识与模型｜selected skills（路径+哈希）、配置模型/温度、RAG 开关、不发送 max_tokens 的输出约定"，且"不适用写明理由"；D2-082 `frozen-inputs.md:11-12` 有 `model: deepseek-flash temp=0.2 RAG=off` 与两条 selected skills 路径；D2-081/083/084/085/086/087/089/090 的 `frozen-inputs.md` 无该组、也无"不适用"理由；D2-088 有 2 次真实模型调用，但冻结页只记分类/契约/画像/驱动/oracle，模型与温度只出现在 `02-conversion/target.gen.model.json`（`temperature:0.2`、`rag:false`、`maxTokensFieldSent:false`）｜边界：D2-088 无 selected skills 路径/哈希，故"模型实际注入了哪些本地知识"不能由冻结记录回读，只能看 `request.system.txt` 摘录（见逐项记录）。

18. **B-18｜D2-087 job-00 的 `comparison_manifest.json`/`metadata.json` 把目标语言写成 C#，与本项 `cpp-to-go` 方向不符**｜分类：装置（提交记录字段错误，保留不改）｜依据：`job-00-source-buildability/comparison_manifest.json` `target.artifactLanguage="csharp"`、`buildCommand "dotnet build -c Release"`，`metadata.json:9` `targetArtifact "target/target.cs (placeholder)"`；而 item `direction="cpp-to-go"`、manifest 行 87 `Direction=cpp-to-go`/`TargetLang=Go`｜边界：源构建失败、目标侧 `SKIPPED`，该字段错误未影响任何 verdict，但属"同一 cpp-to-go 序列中混入 csharp 模板"的可复核事实；不得据此推断目标侧曾构建或比较过。

---

## 逐项记录

### D2-081 / cpp-to-csharp / str_cat.cc

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-csharp/D2-081-cpp-str_cat.cc`（case 根层经 `D2-081-cpp-str_cat.cc/*` glob 二次确认为空，无 `case.md`、无 `source/`）

**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读，30 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：无（0 模型调用，不适用）。
- 03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`returned-evidence/evidence-source.json`（**已读，截断** `可见部分（工具2000字符/行截断）`，2000 字符后不可读）、`returned-evidence/evaluation_report.json`（已读，完整）、`returned-evidence/comparison.json`（已读）、`returned-evidence/controller.log`（已读）。
- 根层：无 `result.md`、无 `evaluator_manifest.json`、无 `target.*`。
- 另有 `batch/items/D2-081.json`（已读，多行完整）。

**身份/版本关联**：taskId `D2-081`｜rawItemId `D2-081`｜batchId `batch`｜direction `cpp-to-csharp`｜kind `NEW`｜disposition `SOURCE_DEPENDENCY_GAP`｜phase `CLOSED`｜lifecycle `DONE`｜pendingAction `null`｜sourceSha256 `bebddfb8ff1b8ed48c46f2c6a5b134339fc9fd4cda6650cb1f44e550d1c0cfa8`（与 manifest 行 81 `BEBDDFB8…CFA8`、frozen:5、classifier-input:10、classification-1:14 四处一致，仅大小写不同）｜finalTargetSha256 无（未生成）｜classifier `v2.3`/`sha256 441b4d50125071544f6d1bbe836b7258d692c37c638acdb678a9e88795366524`/`admissionStatus ALLOWED`/`blockingReason null`/`cls LOW_SIGNAL`｜jobId `eval-20261010-045044-69d4aa97`｜runner `windows-vm-agent-x64`、vmName `windows-eval`、baselineSnapshot `CC-Eval-Windows-8Lang-1.0.26`、agentVersion `1.0.0`、collectorVersion `1.0.0`｜model 名未记（0 调用）。frozen 所列知识/哈希：无（未记该组）。

**冻结/分类**：frozen 记"形态：Abseil 库翻译单元，无 main；case 的 `source/` 下只有该 `.cc` 一个文件"，sourceOs windows（候选未定案）/targetOs windows/x64；分类门禁 ALLOWED、cls LOW_SIGNAL、`network_mode none-detected`。`classifier-input.json` 单任务、`sourcePath source/str_cat.cc`、哈希与 item 一致；`classification-1.json` `details.files` 1 项（`str_cat.cc`，各信号组为空）、`analysisScope source-text-only`、`executionApproved true`、`limitations` 三条（`lexical_heuristics_not_dataflow`/`target_driver_dependencies_not_assessed`/`isolation_and_authorization_not_assessed`）、`inputManifestSha256 e761bd9a…9b1c`。无 `classification-2/3`、无重新分类 attempt。冻结哈希与 item 一致（见上）。

**源预检**：job `eval-20261010-045044-69d4aa97`（job-id.txt 一致）。`input_profile.json`：`argv []`、`stdin null`、`timeoutSeconds 30`、`workingDirectory workspace`、`observationPolicy.dimensions ["output"]`、`output.stdoutMode "normalized-text"`/`stderrMode "exact"`、无 fixtures。`comparison_manifest.json`：source `g++ -std=c++17 -c str_cat.cc -o out.o`（windows/x64/cpp），target `dotnet build -c Release`（csharp）。`metadata.json`：`networkBoundary "isolated VM; compile-only probe; nothing is executed"`、`targetArtifact "target/target.cs (placeholder)"`、`targetHash "sha256:placeholder-precheck"`、`safetyClassification "classifier-2.3 ALLOWED blockingReason=null cls=LOW_SIGNAL"`。真实源侧结果（evidence-source 可见部分）：`build.status="failed"`、`exitCode=1`、`durationMs=372`、build stdout 0 字节、build stderr 190 字节 `str_cat.cc:15:10: fatal error: absl/strings/str_cat.h: No such file or directory` + `compilation terminated.`；`execution.status="blocked"`、`exitCode=null`、`durationMs=0`、`timedOut=false`、execution stderr `build failed`。源运行基线：**不存在**（构建失败，平台记"Source build failed; baseline cannot be established."）。清理依据：`evaluation_report.json` 源侧 `preflight PASSED/1`、`cleanup PASSED/1`、`contaminated=false`、`environmentStatus "clean"`、`runnerStateAfter "READY"`；目标侧 preflight/cleanup 均 `SKIPPED`（`performed:false`）。`comparison.json` = `{"detail":"comparison_not_found"}`。`controller.log` 2 行（04:50:44 created / 04:51:18 finished）。

**模型请求/响应**：无（0 模型调用；frozen 与 item 均记"不消耗模型调用"）。无 `request.system.txt`、无 `target.gen.model.json`、原响应缺件——均属"未发生"。

**失败/废弃/重提 attempt**：无失败 attempt、无废弃 job、无重提；item `codeRevisions 0`、`selfRepairRounds 0`、`failedAttempts` 无。唯一 attempt 即 job-00（构建失败本身不是 attempt 失败，是真实源诊断）。

**自审**：无（未进入生成，不适用）。未发生模型内部 reasoning。

**job 证据**：仅 job-00，见上；**无** `controller-health-before.json`/`runners-before.json`/`controller-health-after.json`/`this-task-classification.json`/`batch-authorization.json`（该批早期 job 目录未放这些件）。`evaluation_report.json` 平台原判：`jobStatus COMPLETED`、`jobPhase RUNNING_SOURCE`、`runVerdict "blocked"`、`codeVerdict "inconclusive"`、`behaviorVerdict "inconclusive"`、`evidenceCoverage` 全 0、`coverageRatio 0.0`。未取回件如实记缺失，未伪造。

**result / evaluator manifest**：`result.md` **缺件**；`evaluator_manifest.json` **缺件**（该去向按现行规则不强制 manifest，但 result.md 是必备报告，见 B-02）。与"当前副本可检查性"分开：本项从未生成目标，故不存在可交付稿问题。

**batch/items**：disposition `SOURCE_DEPENDENCY_GAP`、phase `CLOSED`、lifecycle `DONE`、`verdicts.sourceBuild "failed/1 (SOURCE_DEPENDENCY_GAP)"`、`targetBuild/execution/comparison UNVERIFIED`、`safety ALLOWED`、`blockingReasons []`、`codeRevisions 0`、`selfRepairRounds 0`、`usage.requests 0`；无 `coverageGap`/`datasetAnomaly`/`contractNote` 字段。

**独立证据事实与限制**：
- 原件支持：源构建真实失败于 absl 头缺失（`evidence-source.json` build 块原文）；job 清理通过、环境 clean、runner 回到 READY（`evaluation_report.json`）。
- 历史说明：frozen/item 的归因文字（"引用快照外文件"）与处置说明属记录文本，不是独立诊断。
- 当前规则对照：[构建前提 §0.1](../../../../../references/workflow/build-prerequisites.md) 第 45–48 行把"源引用快照外文件"记为 `SOURCE_DEPENDENCY_GAP`、不补造桩；本项处置与之一致。
- 待核验：manifest `Evidence` 列写 `UNVERIFIED (not built, not run)`，而实际 job 尝试了构建并失败——措辞与原件不完全一致（"未构建"与"构建失败"不同）；登记为清单表述差异，不改写。源正文已删，无法核对 include 行与翻译单元形态。
- 边界：不得把本项"DONE"读成转换或功能结论；行为/目标一切维度均未开展。

**分类归入**：源已有（数据集快照依赖不全，非转换缺陷）；环境（预检隔离环境正常，非环境故障）；装置（清单 Evidence 措辞与原件不符、job 环境记录不齐，见 B-16）；无知识新增。现行规则已覆盖该去向（构建前提 §0.1 三分法），属**已有规则落实**；`result.md` 缺失按 B-02 记**已有规则落实缺口**。

### D2-082 / cpp-to-go / T1218.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-082-cpp-t1218.cpp`（case 根层 glob 为空）

**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读，86 行）、`classifier-input.json`（已读）、`classification-1.json`（已读，70 行）。
- 02-conversion：无（0 模型调用，不适用）。
- 03-self-review：无（不适用）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`controller-health-before.json`、`runners-before.json`、`returned-evidence/evidence-source.json`（**已读，截断**）、`returned-evidence/evaluation_report.json`（已读，完整）、`returned-evidence/comparison.json`（已读）、`returned-evidence/controller.log`（已读）。
- 04-evaluation/job-00b-source-buildability-corrected-command：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`returned-evidence/evidence-source.json`（**已读，截断**）。
- 根层：无 `result.md`、无 `evaluator_manifest.json`、无 `target.*`。
- 另有 `batch/items/D2-082.json`（已读）。

**身份/版本关联**：taskId `D2-082`｜rawItemId `D2-082`｜intakeId `intake-dataset-2-2026-10-10`（frozen:4）｜batchId `batch`｜direction `cpp-to-go`｜kind `NEW`｜disposition `FROZEN`｜phase `EVALUATION_NOT_READY`｜lifecycle `WAITING`｜pendingAction 要求"对该 inline hook 的真实执行给出显式授权，或由用户裁定排除"｜sourceSha256 `e3d4255a48feb27cd7db8407e62b8145e3aa38cc74ddf207e138dfb6d9da2c93`（manifest 行 82、frozen:6、classifier-input:10、classification-1:17 一致）｜finalTargetSha256 无｜classifier `v2.3`/`441b4d50…6524`/ALLOWED/null/`REVIEW_SENSITIVE`（`reviewGroups ["dynamic_code","sensitive"]`，信号行 sensitive 27,32 / dynamic_code 37,51；`requiresSyntheticData true`）｜jobIds `eval-20261010-044201-4a88cf65`（failed）、`eval-20261010-044302-863f0cdc`（completed/0）｜runner `windows-vm-agent-x64`、vmName `windows-eval`、baselineSnapshot `CC-Eval-Windows-8Lang-1.0.26`、agentVersion/collectorVersion `1.0.0`｜冻结记 model `deepseek-flash temp=0.2 RAG=off`、不发送 max_tokens（实际 0 调用）。序号：job-00b 为"修正命令"的第二次源预检，未被重编号。

**冻结/分类**：frozen 记 sourceBytes 3579、物理行 112（与 manifest `Lines=112` 一致）、sourceLang/sourceStd C++/ISO C++17、targetLang/Std Go/Go 1.27、sourceOsBasis 含 windows.h/Sspi.h/VirtualProtect/MoveMemory/AddVectoredExceptionHandler/DllMain/SECURITY_STATUS、sceneTags"无网络、无文件 I/O；本质是进程内代码修补与执行流劫持"、attackTactic `T1218`、taskMode 短单文件、selected skills 两条路径（`skills/directions/cpp-to-go/SKILL.md`、`skills/systems/posix-windows-process-identity/SKILL.md`）——**未记路径哈希**。分类 ALLOWED、`REVIEW_SENSITIVE`；无 `classification-2/3`。哈希一致。

**源预检**：job-00 `input_profile.json` 与 job-00b 完全相同（`argv []`/`stdin null`/`timeout 30`/`dimensions ["output"]`/`normalized-text`+`exact`）；`comparison_manifest.json` 差异只在 source `buildCommand`——job-00 `g++ -std=c++17 -shared T1218.cpp -o program.dll -lsecur32`，job-00b `g++ -std=c++17 -shared -DUNICODE -D_UNICODE -fpermissive T1218.cpp -o program.dll -lsecur32`（target 均为 `go build -o program.exe target.go`）。`metadata.json`：job-00 `networkBoundary "isolated VM; source-side buildability probe only. The DLL is NOT loaded or executed; only the translation unit is compiled."`；job-00b 同义加注"5 个错误是 CONTRACT DEFECTS"与两条修正理由。真实结果：job-00 `build.status failed`/`exitCode 1`/`durationMs 2413`、stderr 含 `T1218.cpp:27:28: error: invalid conversion from 'FARPROC'…to 'LPVOID' [-fpermissive]`；job-00b `build.status completed`/`exitCode 0`/`durationMs 3143`、同诊断降 `warning`。源运行基线：**未取得**（job-00b 只有 evidence-source，无 execution 结果可读段；frozen 亦记"不提交 job-01、不生成目标"）。清理：job-00 `evaluation_report.json` 源侧 `preflight PASSED/1`、`cleanup PASSED/1`、`contaminated false`、`environmentStatus clean`、`runnerStateAfter READY`；job-00b 无 report/cleanup 原件可读（见缺件）。`controller-health-before.json`（job-00）：`status ok`、`version 1.0.0`、`contractSetHash sha256:e088a356…4c45`、`ready true`、`runnerReadiness.executionReady true`、`readyRunnerCount 3`、`blockedRunnerCount 0`；`runners-before.json`：3 个 runner 全 `READY/ready`（linux/windows/macos，快照 `…1.0.26`）。job-00 `comparison.json` = `comparison_not_found`；`controller.log` 2 行（04:42:01 created / 04:42:34 finished）。

**模型请求/响应**：无（0 调用，frozen:76-79 明写"不做目标转换""不消耗模型调用"）。

**失败/废弃/重提 attempt**：**有**——job-00 源预检失败，按"契约缺陷"分流后在 job-00b 用修正命令重跑并成功（详见 B-12）。job-00 是重提前 attempt，其原件全部保留、未被覆盖（job-00 与 job-00b 目录并存）。item 未记 `failedAttempts` 字段，但 `sourcePrecheck.firstAttempt`/`corrected` 成对登记。无废弃 job。

**自审**：无（不适用）。

**job 证据**：job-00 见上（含 health-before/runners-before，无 this-task-classification/batch-authorization）；job-00b **只有** `job-id.txt`+`input_profile.json`+`comparison_manifest.json`+`metadata.json`+`returned-evidence/evidence-source.json`，**缺** report/comparison/controller.log/health-before/runners-before（见缺件），故 job-00b 的清理结论**在副本中不可核实**，不能由 job-00 的 cleanup PASSED 倒推。job-00 平台原判 `runVerdict blocked`/`codeVerdict inconclusive`/`behaviorVerdict inconclusive`/`coverageRatio 0.0`。

**result / evaluator manifest**：两者均**缺件**（B-02）；本项为 WAITING 暂停，现行规则仍要求 result.md 记录暂停原因与恢复条件（交付契约 §1.1 第 19–21 行、§2.1.1 WAITING 行）。

**batch/items**：disposition `FROZEN`、phase `EVALUATION_NOT_READY`、lifecycle `WAITING`、`sourcePrecheck.firstAttempt/corrected` 如上、`blockingReason RUN_SAFETY_NOT_READY`、`blockingDetail` 详述"DLL 只有 DllMain…任何能观察它的驱动都必须加载 DLL 从而执行 hook"、`driverFourElements` 四项全 `FAIL`、`verdicts.sourceBuild "completed/0 after contract-defect correction"`、其余 UNVERIFIED、`safety "RUN_SAFETY_NOT_READY"`、`usage.requests 0`。

**独立证据事实与限制**：
- 原件支持：两次源构建结果与诊断（`evidence-source.json` 两侧原文）；job-00 双侧清理与环境状态（report）。
- 历史说明：frozen 第 51–67 行的"为何不能补最小中性驱动"属论证文本；item 的 `driverFourElements` 是 Agent 判定记录，不是平台字段。
- 当前规则对照：见 B-12（契约缺陷分流）与 B-14（未生成与现行 LIB 分支方向的差异）。hook 属隐蔽能力，[安全边界 §3](../../../../../references/framework/safety-boundary.md) 第 27 行禁止借转换新增/扩大隐蔽能力，也禁止空跑或伪造输出；本项未删行为、未伪造输出。
- 待核验：job-00b 无 report/cleanup 原件；`evidence-source.json` 2000 字符后的 `observations`/清理字段本会话读不到。
- 边界：源可构建（DLL 形态）已被诊断支持；但**没有任何**目标代码、语法或行为证据，功能 UNVERIFIED。

**分类归入**：已有规则落实（构建前提 §0.1/§4.1 契约缺陷分流；安全边界 §3 不扩大隐蔽能力）；未定/待核（B-14：源可构建却未按现行 §1.3 继续转换）；装置（job-00b 原件不齐，B-16）；源已有（源自身为 inline hook，非转换引入）。无知识新增。

### D2-083 / cpp-to-go / CppWSManWinRM.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-083-cpp-cppwsmanwinrm.cpp`

**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读，42 行）、`classifier-input.json`（已读）、`classification-1.json`（已读，93 行）。
- 02-conversion：无（分类阻断，不适用）。
- 03-self-review：无。
- 04-evaluation：**无任何 job 目录**（未预检、未提交）。
- 根层：无 `result.md`、无 `evaluator_manifest.json`、无 `target.*`。全项仅 3 件过程材料。
- 另有 `batch/items/D2-083.json`（已读）。

**身份/版本关联**：taskId/rawItemId `D2-083`｜batchId `batch`｜direction `cpp-to-go`｜kind `NEW`｜disposition `FROZEN`｜phase `BLOCKED_AT_CLASSIFICATION`｜lifecycle `WAITING`｜pendingAction "obtain verifiable isolation evidence for a controlled WinRM target, then RECLASSIFY"｜sourceSha256 `ec002016f00ae6f232c1d5e166e5a01e48d3b25302e96a69d87fbf3fc8f05e50`（manifest 行 83、frozen:5、classifier-input:10、classification-1:17 一致）｜finalTargetSha256 无｜classifier `v2.3`/`441b4d50…6524`/`admissionStatus BLOCKED`/`blockingReason public_network_unverified`/`cls REVIEW_NETWORK`/`network_mode hostname`｜jobId 无（`JobId` 空）｜runner/vmName/snapshot/model 均无（未提交）。

**冻结/分类**：frozen 记源 `CppWSManWinRM.cpp`、sourceOs windows（候选）、targetOs windows/x64；分类结论 BLOCKED、`reason network_scope_and_inputs_require_review`、`network_mode hostname`、`network_targets`（分类器实测）：`schemas.microsoft.com` L111、L112（scope hostname，provenance literal，`redirectVerified false`），另有 L99 的 `:` 被标 hostname 形态；`requiresNetworkIsolation true`、`executionApproved false`。frozen 的行为取证：`CoCreateInstance(CLSID_WSMan)`、`CreateSession(protocol + "://" + hostname + ":" + port + "/wsman")`（http/5985 硬编码）、`Invoke(Create, Win32_Process, <CommandLine>argv[2]</CommandLine>)`——目标主机与命令均来自 argv。无 `classification-2/3`、无重新分类 attempt（frozen 明确"不得只手改分类 JSON、不得直接改判、不得用 `--network-isolation-configured` 假装有隔离证据"）。哈希一致。`classification-1.json` `inputManifestSha256 02b61873…04b1`。

**源预检**：**无**（分类未 ALLOWED，按硬门禁不得预检）。无 metadata/input_profile/comparison_manifest/evidence/清理依据——属"未发生"，非缺档。

**模型请求/响应**：无（0 调用）。

**失败/废弃/重提 attempt**：无（第一道门禁未过，未产生 attempt）。

**自审**：无。

**job 证据**：无。

**result / evaluator manifest**：均**缺件**——分类阻断属交付契约 §1.1 第 15 行列举的必须走统一收尾分支之一，故 result.md 为必需件（B-02）。

**batch/items**：disposition `FROZEN`、phase `BLOCKED_AT_CLASSIFICATION`、lifecycle `WAITING`、`classifier.admissionStatus BLOCKED`、`blockingReason/blockingDetail` 如上、`verdicts {}`、`blockingReasons ["public_network_unverified"]`、`codeRevisions 0`、`selfRepairRounds 0`、`usage.requests 0`。

**独立证据事实与限制**：
- 原件支持：仅分类结果 JSON（`classification-1.json`）与冻结 Markdown；**没有任何**构建/运行/行为证据。
- 历史说明：frozen 第 16–35 行的行为描述与阻断理由属记入文本。
- 当前规则对照：[分类准入 §2](../../../../../references/workflow/classifier-agent-gate.md) 第 35–41 行规定 `public_network_unverified` 的处置是"取得真实隔离证据后，在新条件下**重新分类**"，且不得只手改分类 JSON；本项处置与之一致。frozen 的"不预检、不生成、不提交"亦与 §2 表 `BLOCKED` 行一致。
- 待核验：源正文已删，无法复核 L99/L111/L112 的实际上下文；分类器把 L99 的字面 `:` 标为 hostname scope 属其词法启发（`limitations` 已声明 `lexical_heuristics_not_dataflow`），登记为分类器行为事实而非缺陷结论。
- 边界：不得把 BLOCKED 说成源不可构建或转换失败；也不得把"未取得隔离证据"写成"永远不可转换"。

**分类归入**：已有规则落实（分类准入 §2 阻断原因处置；任务状态 §3 `SAFETY_BLOCKED`/WAITING 语义区分）；环境（缺已核验的封闭实验网目标）；装置（缺 result.md、B-02）。无知识新增；分类器词法把 `:` 判 hostname 的建议若进入知识需另立反例（记**未定**，不写入 Skill）。

### D2-084 / cpp-to-go / civil_time.cc

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-084-cpp-civil_time.cc`

**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读，50 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion / 03-self-review：无（0 调用，不适用）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`controller-health-before.json`、`runners-before.json`、`returned-evidence/evidence-source.json`（**已读，截断**）、`returned-evidence/evaluation_report.json`（已读，完整）、`returned-evidence/comparison.json`（已读）、`returned-evidence/controller.log`（已读）。
- 根层：无 `result.md`/`evaluator_manifest.json`/`target.*`。
- 另有 `batch/items/D2-084.json`（已读）。

**身份/版本关联**：taskId/rawItemId `D2-084`｜batchId `batch`｜direction `cpp-to-go`｜kind `NEW`｜disposition `SOURCE_DEPENDENCY_GAP`｜phase `CLOSED`｜lifecycle `DONE`｜pendingAction `null`｜sourceSha256 `147f18f2c1c2385939070ba27b892693ba5a4ec718c265043611ce50633e86ef`（manifest 行 84、frozen:5、classifier-input:10、classification-1:14 一致）｜finalTargetSha256 无｜classifier `v2.3`/`441b4d50…6524`/ALLOWED/null/`LOW_SIGNAL`｜jobId `eval-20261010-044524-5c79cce5`｜runner `windows-vm-agent-x64`、vmName `windows-eval`、snapshot `CC-Eval-Windows-8Lang-1.0.26`、agentVersion/collectorVersion `1.0.0`｜model 未记（0 调用）。

**冻结/分类**：frozen 记"Abseil 库的翻译单元，无 main"、sourceOs windows（候选未定案）/targetOs windows/x64；分类 ALLOWED、`LOW_SIGNAL`、`none-detected`、无信号组；归因表按"三分法"逐条排除"缺目标系统接口"与"命令/契约缺陷"，定案 SOURCE_DEPENDENCY_GAP；附"数据集形态观察"（与 D2-082 同属单文件缺上下文形态）。`classification-1.json` `details.files` 1 项、`inputManifestSha256 1b802b67…bb7e`。无 `classification-2/3`。哈希一致。

**源预检**：job `eval-20261010-044524-5c79cce5`。`input_profile.json`：`argv []`/`stdin null`/`timeout 30`/`dimensions ["output"]`/`normalized-text`+`exact`。`comparison_manifest.json`：source `g++ -std=c++17 -c civil_time.cc -o civil_time.o`（与 metadata 注"compile-only (-c) so the diagnostic decides whether headers are present"一致），target `go build -o program.exe target.go`。`metadata.json`：`networkBoundary "isolated VM; compile-only probe; nothing is executed"`、`targetArtifact target/target.cs`(占位)/`targetHash placeholder-precheck`、`safetyClassification "classifier-2.3 ALLOWED blockingReason=null cls=LOW_SIGNAL"`。真实结果：`build.status failed`/`exitCode 1`/`durationMs 361`、build stderr 193 字节 `civil_time.cc:15:10: fatal error: absl/time/civil_time.h: No such file or directory` + `compilation terminated.`；`execution.status blocked`/`durationMs 0`、stderr `build failed`。源基线：无（report reason "Source build failed; baseline cannot be established."）。清理：源侧 `preflight PASSED/1`、`cleanup PASSED/1`、`contaminated false`、`environmentStatus clean`、`runnerStateAfter READY`；目标侧 `SKIPPED`。`controller-health-before.json`：`ready true`、`executionReady true`、`readyRunnerCount 3`、`blockedRunnerCount 0`、`checkedAt 04:45:24`；`runners-before.json` 三 runner 全 READY。`comparison.json` = `comparison_not_found`；`controller.log` 2 行（04:45:24 / 04:45:54）。

**模型请求/响应**：无（0 调用）。**失败/废弃/重提 attempt**：无。**自审**：无。

**job 证据**：仅 job-00，含 health-before/runners-before；无 after/closure、无 this-task-classification/batch-authorization。平台原判 `runVerdict blocked`/`codeVerdict inconclusive`/`behaviorVerdict inconclusive`/`coverageRatio 0.0`。

**result / evaluator manifest**：均**缺件**（B-02）。

**batch/items**：与 D2-081 同形（`SOURCE_DEPENDENCY_GAP`/`CLOSED`/`DONE`/`sourceBuild failed/1`/其余 UNVERIFIED/`usage.requests 0`）。

**独立证据事实与限制**：
- 原件支持：absl 头缺失的真实编译诊断与 job 清理原件。
- 历史说明：frozen:46-50 的"数据集形态观察"是对批次的推测性说明（"本批 NEW 项中可能存在同类情形"），不是本项结论；后续 D2-085/086/087 确实同型。
- 当前规则对照：同 B-01/B-12（构建前提 §0.1 第 45–48 行）。
- 待核验：manifest `Evidence` 谓"not built"与真实"build failed"措辞不一致（同 B-01 边界）；源正文已删。
- 边界：`DONE` 仅表示该去向已定案，不含任何目标结论。

**分类归入**：源已有；环境；装置（原件/记录不齐）；已有规则落实（去向分流与 result.md 要求，后者缺失）。

### D2-085 / cpp-to-go / match.cc

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-085-cpp-match.cc`

**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读，36 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion / 03-self-review：无（0 调用）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`controller-health-before.json`、`runners-before.json`、`returned-evidence/evidence-source.json`（**已读，截断**）、`returned-evidence/evaluation_report.json`、`returned-evidence/comparison.json`、`returned-evidence/controller.log`（各已读）。
- 根层：无 `result.md`/`evaluator_manifest.json`/`target.*`。
- 另有 `batch/items/D2-085.json`（已读）。

**身份/版本关联**：taskId/rawItemId `D2-085`｜batchId `batch`｜direction `cpp-to-go`｜kind `NEW`｜disposition `SOURCE_DEPENDENCY_GAP`｜phase `CLOSED`｜lifecycle `DONE`｜sourceSha256 `3a584976c0a5945908fdab3ce1a999f30c7973ea52161ea5f85079674abeaad4`（manifest 行 85、frozen:5、classifier-input:10、classification-1:14 一致）｜classifier `v2.3`/`441b4d50…6524`/ALLOWED/null/`LOW_SIGNAL`｜jobId `eval-20261010-044645-915b7c73`｜runner `windows-vm-agent-x64`、snapshot `CC-Eval-Windows-8Lang-1.0.26`、vmName `windows-eval`｜0 调用。

**冻结/分类**：frozen 同 084 结构（Abseil 翻译单元、无 main、windows 候选、三分法归因、跳过不补桩、model 0）；`classification-1.json` `details.files` 1 项、`inputManifestSha256 122ee9f0…9747`；无 `classification-2/3`；哈希一致。

**源预检**：job `eval-20261010-044645-915b7c73`。`input_profile.json`/`comparison_manifest.json` 同型（source `g++ -std=c++17 -c match.cc -o out.o`；target `go build -o program.exe target.go`；`profileId batch-d2-085-cpp-to-go`）。真实结果：`build.status failed`/`exitCode 1`/`durationMs 350`、stderr 182 字节 `match.cc:15:10: fatal error: absl/strings/match.h: No such file or directory`；`execution.status blocked`。基线无（report reason 同上）。清理：源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`；目标侧 `SKIPPED`。`controller-health-before.json` `checkedAt 04:46:44`、`readyRunnerCount 3`、`blockingReasons []`；`runners-before.json` 三 runner READY。`comparison.json` = `comparison_not_found`；`controller.log` 2 行（04:46:45 / 04:47:16）。

**模型请求/响应**、**失败/重提 attempt**、**自审**：均无。

**job 证据**：仅 job-00（含 health-before/runners-before）；平台原判 `blocked/inconclusive/inconclusive`、`coverageRatio 0.0`。无 after/closure。

**result / evaluator manifest**：均**缺件**（B-02）。

**batch/items**：与 D2-084 同形。

**独立证据事实与限制**：原件支持同 084（真实编译诊断 + 清理原件）；历史说明为 frozen 的分流文字；当前规则对照同 B-01；待核验：manifest `Evidence` 措辞、源正文已删；边界：无任何目标结论。

**分类归入**：源已有；环境；装置；已有规则落实（含 result.md 缺口）。

### D2-086 / cpp-to-go / str_split.cc

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-086-cpp-str_split.cc`

**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读，36 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion / 03-self-review：无（0 调用）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`controller-health-before.json`、`runners-before.json`、`returned-evidence/evidence-source.json`（**已读，截断**）、`returned-evidence/evaluation_report.json`、`returned-evidence/comparison.json`、`returned-evidence/controller.log`（各已读）。
- 根层：无 `result.md`/`evaluator_manifest.json`/`target.*`。
- 另有 `batch/items/D2-086.json`（已读）。

**身份/版本关联**：taskId/rawItemId `D2-086`｜direction `cpp-to-go`｜kind `NEW`｜disposition `SOURCE_DEPENDENCY_GAP`｜phase `CLOSED`｜lifecycle `DONE`｜sourceSha256 `919dd8d0f168259472b049e52560235c3f891cda19556c287b1d7a8ad9b09c41`（manifest 行 86、frozen:5、classifier-input:10、classification-1:14 一致）｜classifier `v2.3`/`441b4d50…6524`/ALLOWED/null/`LOW_SIGNAL`｜jobId `eval-20261010-044725-7e182d07`｜runner `windows-vm-agent-x64`、snapshot `CC-Eval-Windows-8Lang-1.0.26`｜0 调用。

**冻结/分类**：frozen 同型（Abseil 翻译单元、三分法、跳过、0 调用）；`classification-1.json` 1 文件、`inputManifestSha256 2f20e54d…a219`；无 `classification-2/3`；哈希一致。

**源预检**：job `eval-20261010-044725-7e182d07`；source `g++ -std=c++17 -c str_split.cc -o out.o`；真实结果 `build.status failed`/`exitCode 1`/`durationMs 535`、stderr 198 字节 `str_split.cc:15:10: fatal error: absl/strings/str_split.h: No such file or directory`；`execution.status blocked`；基线无；源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`；目标侧 `SKIPPED`。`controller.log` 2 行（04:47:25 / 04:48:03）。
- **本项特有**：`controller-health-before.json` 显示 `readyRunnerCount 2`、`blockedRunnerCount 0`、`blockingReasons ["busy:CLEANING"]`、`checkedAt 04:46:49`；`runners-before.json` 中 `windows-vm-agent-x64` `lifecycleState "CLEANING"`、`ready false`、`contaminated false`；而该 job 36 秒后在**同一个** windows runner 上构建完成、report 两侧 `cleanup PASSED`、目标侧 `SKIPPED`、`environmentStatus clean`。登记为"提交前快照≠门禁"的实例（B-16）。

**模型请求/响应**、**失败/重提 attempt**、**自审**：均无。

**job 证据**：仅 job-00；平台原判 `blocked/inconclusive/inconclusive`、`coverageRatio 0.0`。无 after/closure。

**result / evaluator manifest**：均**缺件**（B-02）。

**batch/items**：与 D2-084 同形。

**独立证据事实与限制**：原件支持同 084；历史说明为 frozen 文字；当前规则对照：B-01 + 评估准备 §1 第 18 行（READY/clean/快照不证明隔离）；待核验：CLEANING 快照的具体原因不可从副本得知（不能据一次快照断言装置缺陷）；边界：不得把 CLEANING 读成 job 失败。

**分类归入**：源已有；环境（快照状态）；装置（B-16）；已有规则落实（门禁不因快照放行，实际也未阻断正确 job）。

### D2-087 / cpp-to-go / substitute.cc

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-087-cpp-substitute.cc`

**文件清单与读取状态**：
- 01-frozen：`frozen-inputs.md`（已读，30 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion / 03-self-review：无（0 调用）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`returned-evidence/evidence-source.json`（**已读，截断**）、`returned-evidence/evaluation_report.json`、`returned-evidence/comparison.json`、`returned-evidence/controller.log`（各已读）。**无** `controller-health-before.json`/`runners-before.json`（`read` 返回 not found，glob 亦未列出）。
- 根层：无 `result.md`/`evaluator_manifest.json`/`target.*`。
- 另有 `batch/items/D2-087.json`（已读）。

**身份/版本关联**：taskId/rawItemId `D2-087`｜direction `cpp-to-go`｜kind `NEW`｜disposition `SOURCE_DEPENDENCY_GAP`｜phase `CLOSED`｜lifecycle `DONE`｜sourceSha256 `046449abe5ab8c4ca78b99617d09f34f09e3631006f09d8f20edf56ac951bff7`（manifest 行 87、frozen:5、classifier-input:10、classification-1:14 一致）｜classifier `v2.3`/`441b4d50…6524`/ALLOWED/null/`LOW_SIGNAL`｜jobId `eval-20261010-044842-5db6bbba`｜runner `windows-vm-agent-x64`、snapshot `CC-Eval-Windows-8Lang-1.0.26`｜0 调用。

**冻结/分类**：frozen 同型（Abseil 翻译单元、三分法、跳过、0 调用）；`classification-1.json` 1 文件、`inputManifestSha256 d5312479…770c`；无 `classification-2/3`；哈希一致。

**源预检**：job `eval-20261010-044842-5db6bbba`。`comparison_manifest.json`：source `g++ -std=c++17 -c substitute.cc -o out.o`，**target `artifactLanguage "csharp"` + `dotnet build -c Release`**，而同项 `metadata.json:9` 亦写 `target/target.cs (placeholder)`——**与本项 direction `cpp-to-go` 不符**（与 D2-081 的 csharp 模板同形）；提交时间晚于 D2-086，属目标语言字段复制错误。真实结果：`build.status failed`/`exitCode 1`/`durationMs 364`、stderr 202 字节 `substitute.cc:15:10: fatal error: absl/strings/substitute.h: No such file or directory`；`execution.status blocked`；基线无；源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`；目标侧 `SKIPPED`；`controller.log` 2 行（04:48:42 / 04:49:12）。因源构建失败、目标侧未执行，该字段错误未影响任何 verdict，但登记为装置事实。

**模型请求/响应**、**失败/重提 attempt**、**自审**：均无。

**job 证据**：仅 job-00，**缺** health-before/runners-before/after；平台原判 `blocked/inconclusive/inconclusive`、`coverageRatio 0.0`。

**result / evaluator manifest**：均**缺件**（B-02）。

**batch/items**：与 D2-084 同形。

**独立证据事实与限制**：
- 原件支持：absl 头缺失诊断 + 清理原件。
- 历史说明：frozen 分流文字。
- 当前规则对照：B-01；另 [交付契约 §2.2](../../../../../references/framework/delivery-handoff-contract.md) 要求 job 目录内 JSON 记录提交时身份（`comparison_manifest` 的 source/target 语言属身份字段），本项 target 语言字段与 direction 不一致，属**已发生记录的字段错误**（保留不改）。
- 待核验：field 错误来源不可确知（模板复用最可能）；源正文已删。
- 边界：不得据此推断目标侧曾被执行或比较过。

**分类归入**：源已有；装置（target 语言字段错误 + job 原件不齐）；已有规则落实（去向分流；result.md 缺口）。

### D2-088 / cpp-to-powershell / resource_manifest_builder.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-088-cpp-safe_attck_cpp_suite-resource_manifest_builder.cpp`

**文件清单与读取状态**（40 件）：
- 01-frozen：`frozen-inputs.md`（已读，69 行）、`classifier-input.json`（已读）、`classification-1.json`（已读）。
- 02-conversion：`request.system.txt`（已读，33 行）、`target.gen.model.json`（已读，19 行）、`target.self-repair-1.proposal.json`（已读，19 行）、`target.self-repair-1.model.json`（已读，11 行）。**无**目标代码文件、**无** `target.gen.raw.json`（`target.gen.model.json:18` 指向它）。
- 03-self-review：`review.system.txt`（已读，12 行）、`self-review-1.json`（已读，26 行）、`self-review-1.model.json`（**已读，截断**：第 2 行模型原响应含 `content` + `reasoning_content`，2000 字符后不可读）。无 `self-review-1.decision.json`。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`、`controller-health-before.json`、`runners-before.json`（各已读，完整）；`returned-evidence/evidence-source.json`（**已读，截断**）、`returned-evidence/evidence-target.json`（**已读，截断**）、`returned-evidence/evaluation_report.json`（**已读，截断**）、`returned-evidence/evaluation_report.md`（已读，83 行）、`returned-evidence/comparison.json`（已读）、`returned-evidence/controller.log`（已读，仅 1 行）。
- 04-evaluation/job-01-dual-build：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`、`runners-before.json`（各已读）；`returned-evidence/evidence-source.json`（**已读，截断**）、`returned-evidence/evidence-target.json`（**已读，截断**）、`returned-evidence/evaluation_report.json`（**已读，截断**）、`returned-evidence/evaluation_report.md`（已读，77 行）、`returned-evidence/comparison.json`（已读）、`returned-evidence/controller.log`（已读，2 行）、`returned-evidence/controller-health-after.json`（已读）。
- 根层：`result.md`（已读，53 行）、`evaluator_manifest.json`（已读，71 行）。**无**根级 `target.ps1`。
- 另有 `batch/items/D2-088.json`（已读）。

**身份/版本关联**：taskId/rawItemId `D2-088`｜batchId `batch`｜direction `cpp-to-powershell`｜kind `NEW`｜disposition `CONVERTED`｜phase `CLOSED`｜lifecycle `DONE`｜sourceSha256 `9d2509b640b6e9780282db0a527a1eca6d7a575f4d369ca860b79875384c5382`（manifest 行 88、frozen:5、classifier-input:13、classification-1:16、job-00 与 job-01 `metadata.json` 的 `sourceHash` 一致）｜**finalTargetSha256 `e9f9c25dcec33d69e7e0aa94e78a9a35fb8637c46f33608f93c4517286e1ff49`**（item:39）＝ `target.self-repair-1.model.json:8` `outputSha256`；**未出现在任何 job 记录中**（job-01 `targetHash` 是字面标签，见 B-08）｜classifier `v2.4` / `sha256 009a6f31177b08334663340321494ace1e430de13f8a5687e6843ab26839f3a4` / ALLOWED / null / `REVIEW_SIDE_EFFECTS`（`reviewGroups ["filesystem"]`，信号 L2,3,31,41,61；`has_file_ops true`），item 附注"source/ 树覆盖 `resource_manifest_builder.cpp` 与 `run_case.py`（平台 identity 门禁要求整棵 source/ 树被分类）"｜jobIds：源预检 `eval-20261010-145337-41c8080e`（job-00）、双侧 `eval-20261010-145923-8c852ab1`（job-01）；frozen 另提到早期探测 job `eval-20261010-144440-1f0edf06`（**本副本无该 job 目录**）｜runner `windows-vm-agent-x64`、vmName `windows-eval`、baselineSnapshot `CC-Eval-Windows-8Lang-1.0.28`、agentVersion/collectorVersion `1.0.0`、contractSetHash `sha256:a9ed1445…d82e`｜model：`deepseek-flash`、温度 0.2、RAG off、`maxTokensFieldSent false`（`target.gen.model.json` + item `usage.model`）。
- frozen 所列知识与哈希：**未记** selected skills 路径/哈希（B-17）；`request.system.txt` 是实际注入正文（C++→PowerShell 转换器角色 + 7 条硬性义务 + 本题关键点：目录副作用、`agent_config.json` 逐行 10 行内容、`pipeline.dot` 三行内容、stdout 一行 JSON、退出码 0、目标环境与命令、字节级形态要求），未附知识页正文。

**冻结/分类**：frozen 记形态"C++17 单文件、含 main（70 行 CRLF，2138 字节）"、源/目标语言与标准（C++ ISO C++17 → PowerShell 7.6）、双 windows/x64、场景 `file-io`（无系统方向）、任务模式单文件、静态画像（`create_directories`、写两文件、stdout 一行；`_WIN32 → localtime_s` else `localtime_r`）、驱动四要素（直接运行、无 argv/stdin、采集 stdout/stderr/退出码 + 文件副作用 `out/resource_advanced/*`、自然退出）、oracle（主：stdout 精确；次：`pipeline.dot` 确定、`agent_config.json` 除 `generated_at` 外确定且落在平台 `timestamps` 消噪 token）、"不记 ORACLE_NOT_FREEZABLE"、提交链路修正（identity 硬门禁要求 source/ 每个文件被分类；四组对照实验记录）、清单观察（manifest `Lines=63` vs 实际 70 行，哈希相符）。分类 ALLOWED/`REVIEW_SIDE_EFFECTS`；**副本内 `classification-1.json` 只覆盖 1 文件**，覆盖 2 文件的结果只存于两个 job 的 `this-task-classification.json`（`reviewGroups ["filesystem","process"]`，`run_case.py` 哈希 `4b94edb6…a51f`，`inputManifestSha256 3d0647d7…dd05`）——见 B-04。无 `classification-2/3` 原件。

**源预检**：job-00 `eval-20261010-145337-41c8080e`，`input_profile.json`：`stdoutMode "json-structural"`（其余同前型）、`dimensions ["output"]`、`timeoutSeconds 30`、`argv []`。`comparison_manifest.json`：source `g++ -std=c++17 resource_manifest_builder.cpp -o program.exe`，target `pwsh -NoProfile -File build_case.ps1`。`metadata.json`：`networkBoundary "isolated VM; no network behaviour; local file writes only (out/resource_advanced)"`、`targetArtifact "target/target.ps1 (precheck placeholder)"`、`targetHash "sha256:placeholder-precheck"`、`safetyClassification "classifier-2.4 ALLOWED blockingReason=null cls=REVIEW_SIDE_EFFECTS"`。真实结果（可见部分）：源 `build.status completed`/`exitCode 0`/`durationMs 2946`、build stdout/stderr 均空；源 `execution.status completed`/`exitCode 0`/`durationMs 247`、execution stdout 123 字节结构化 `{"exitCode":0,"stderr":"","stdout":"{\"case\":\"resource_development_advanced\",\"tasks\":3,\"status\":\"ok\"}\r\n"}`；源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`（evaluation_report.json）。**同 job 也跑了占位目标**：target `build completed/exitCode 0`/`durationMs 1666`、`execution.status completed`/`exitCode 0`、target stdout 45 字节结构化 `{"exitCode":0,"stderr":"","stdout":""}`（空），故 job-00 平台 `behaviorVerdict "mismatched"`、`codeVerdict "failed"`、`runVerdict "partial-runnable"`、`coverageRatio 1.0`——**占位装置产物，非转换失败**（B-06）。`controller-health-before.json`：`ready true`、`executionReady true`、`readyRunnerCount 3`、`blockingReasons []`、`checkedAt 14:43:40`；`runners-before.json` 三 runner READY（快照 `…1.0.28`）。`controller.log` **只有** `[14:53:37.959553] comparison job created` 一行（无 finished，取回时点问题）。

**模型请求/响应**：
- 第 1 次（生成）：`target.gen.model.json` — stage GENERATED、round 1、model `deepseek-flash`、`baseUrlEnv CODE_TRANSLATOR_BASE_URL`、`temperature 0.2`、`maxTokensFieldSent false`、`rag false`、usage `prompt 1348 / completion 4228 / reasoning 3606 / total 5576`、`finishReason "stop"`、`requestSha256 sha256:f337e7c5…81fe`、`outputSha256 sha256:d3a3f106…48fe`、`rawResponsePath "target.gen.raw.json"`（**该原响应文件不在副本**）。
- 第 2 次（自审）：见**自审**栏（`self-review-1.model.json` 为原响应封装，含 `reasoning_content`）。
- 自修不是新模型调用：`target.self-repair-1.model.json` stage SELF_REPAIRED、`repairKind "mechanical-apply"`、`derivedFrom 03-self-review/self-review-1.json`、`parentSha256 sha256:d3a3f106…48fe`、`outputSha256 sha256:e9f9c25d…ff49`、`appliedPatches 2`，注"非新模型调用；按 self-review-1 给出的确定性补丁由 Agent 机械应用（2 处换行 `` `n `` → `` `r`n ``）"。
- item `usage`：`promptTokens 3017 / completionTokens 24460 / reasoningTokens 23445 / requests 2 / model deepseek-flash / failedAttempts 0`；result.md §3 分轮表记生成 `1348/4228/3606`、自审 `1669/20232/19839`（生成轮与 model.json 一致；自审轮只在 result 中，自审 model.json 2000 字符后或含 usage 但本会话读不到）。
- **原响应正文**：`target.gen.raw.json` 缺件；`self-review-1.model.json` 是原响应（被截断读取）。无 `request.system.txt` 之外的请求正文原件（user 侧正文未单独保存）。

**失败/废弃/重提 attempt**：**有**——frozen:13 记首次分类调用以相对 `sourcePath` 误报 `BLOCKED_INPUT/input_error`（`FileNotFoundError`），改用绝对路径后 ALLOWED，"两次输入/输出均留证（`*-attempt1.json` 为失败尝试）"；但**该失败 attempt 的原件不在副本**（B-04）。另 frozen:64-65 记 4 组提交链路对照实验（缺 driver → 403 `identity_mismatch`；driver 改 `.txt` → 仍 403；driver 放 capsule 根 → `exitCode 2`），**这些实验的 HTTP/回执原件亦不在副本**。item `failedAttempts 0`（指模型调用层无失败），与分类层 attempt 缺件不矛盾。早期探测 job `eval-20261010-144440-1f0edf06` 无目录。

**自审**：`review.system.txt` 要求"只输出一个裸 JSON 对象"，字段 `verdict`（`NO-REPAIR-IDENTIFIED`/`REPAIR-RECOMMENDED`）+ `findings[{severity,dimension,source,target,issue,repair}]`，判定口径"只有有源/目标定位证据、且属转换引入的问题才算 blocking/major；源本身既有问题、环境项、无法定位的猜测记为 info"、"不要臆测运行结果；只做静态对照"。`self-review-1.json` 全部条目：
- 条目 1｜severity `major`｜dimension `filesystem`｜source `resource_manifest_builder.cpp: std::ofstream cfg(out / "agent_config.json")，各 "\n" 写入`｜target `target.ps1: $jsonContent = ($lines -join "\`n") + "\`n"，随后 WriteAllText(... 'agent_config.json')`｜issue "源在 Windows 文本模式下把 `\n` 翻译为 CRLF；转换稿用 WriteAllText 原样写入 LF，导致 agent_config.json 行尾由 CRLF 变为 LF，文件字节内容不一致"｜repair "改为 `` `r`n `` 或用 StreamWriter 设 `NewLine`"。
- 条目 2｜severity `major`｜dimension `filesystem`｜source `… pipeline.dot …`｜target `target.ps1: $dotContent = "digraph G {\`n...\`n}\`n"`｜issue 同行尾不一致｜repair 同。
- `verdict REPAIR-RECOMMENDED`、`applied true`、`appliedTo "02-conversion/target.v2.ps1"`（该文件不存在，见 B-09）、`round 1`、`model deepseek-flash`。
- `self-review-1.model.json`：**元数据兼原响应封装**——第 1 行空行，第 2 行是 OpenAI 兼容 `chat.completion` 对象（`id d6bfe64c-…`、`created 1791644237`、`model deepseek-flash`），`message.content` 为自审 JSON 原文、另有 `reasoning_content`（**模型内部思考，按本审阅纪律不得当作自审结论**）；该行 2000 字符后不可读。
- 无第二轮自审（`selfRepairRounds 1`；result.md §3 记"修复后未再触发第二轮自审；最终结论以第三方编译/行为证据为准"）。

**job 证据**：job-01 `eval-20261010-145923-8c852ab1`：`input_profile.json`（`profileId "D2-088"`、`json-structural`）、`comparison_manifest.json` 与 job-00 同命令、`metadata.json`（`note` 记"job-01 dual-build (source C++ vs target PowerShell v2 after self-repair round 1)"、`targetArtifact target/target.ps1`、**`targetHash "sha256:target-v2-self-repair-round-1"`**）、`batch-authorization.json`（`authorizedBy gyh-p1`、`authorizedAt/verifiedAt 2026-10-10T14:43:00Z`、`validUntil 2026-10-17T14:43:00Z`、`scope "所有非BLOCKED任务"`、`vmIsolation{confirmed,snapshotRollback,cleanupVerified}` 全 true、`networkIsolation{configured,publicNetworkBlocked,experimentalNetworkOnly}` 全 true + 复用既有批次授权说明）、`this-task-classification.json`（2 文件、ALLOWED）、`runners-before.json`（三 runner READY）。
- 双侧原始观察（可见部分）：源 `build completed/exitCode 0/durationMs 2748`、`execution completed/0/durationMs 215`、stdout 结构化 123 字节，内层程序 stdout `{"case":"resource_development_advanced","tasks":3,"status":"ok"}\r\n`、digest `sha256:bdea5a99…2e27`；目标 `build completed/0/durationMs 1404`（`pwsh` 语法检查）、`execution completed/0/durationMs 738`、stdout 结构化 123 字节、**同一 digest `sha256:bdea5a99…2e27`**。
- `comparison.json`：`behaviorVerdict "matched"`、`dimensions.output.status "matched"`（`applicable/observed true`、`diffs []`）、`filesystem/processes/registry/network` 全 `not-applicable`。
- `evaluation_report.json`（可见部分）：`runVerdict "runnable"`、`codeVerdict "passed"`、`behaviorVerdict "matched"`、`evidenceCoverage{applicable 1, observed 1, matched 1, mismatched 0, inconclusive 0, sufficient 1, coverageRatio 1.0}`、`environmentStatus "clean"`、双侧 `preflight/cleanup PASSED`、`runnerStateAfter READY`。`evaluation_report.md` 同；`controller.log` 2 行（14:59:23 / 15:00:32）；`controller-health-after.json`：`ready true`、`readyRunnerCount 2`、`blockingReasons ["busy:CLEANING"]`、`checkedAt 15:00:29`。**无 capsule.zip、无 job 内 `source/`/`target/` 暂存树**（标准骨架标"若保留"，记未保留）。

**result / evaluator manifest**：`result.md` 存在且按五栏骨架；§1 表：交付完整性"已完成"、语法/编译"通过"（目标侧 `build completed/0`，pwsh Parser 语法检查）、功能一致性"匹配"（job-01 `behaviorVerdict=matched`、两侧 stdout 逐字节相同、退出码均 0），并注明"文件维度未取证"；§2 记目标文件 `04-evaluation/job-01-dual-build/target/target.ps1`（该路径在副本不存在，B-09）；§4 如实登记三条未覆盖（`filesystem not-applicable`、`generated_at` 不可复现、写失败路径"源静默 vs 目标抛异常"属理论差异未实测）；§5 给出两条下一步。`evaluator_manifest.json`：`schemaVersion 1`、`kind third-party-evaluator-manifest`、`generatedBy "…(hand-authored, not code-translator-mcp)"`、`languagePair{cpp,powershell}`、`taskMetadata{sourceLanguage cpp,targetLanguage powershell,attackTactic none,sceneTags["filesystem"],windows/x64,riskLevel low,evidenceMode static-and-runtime,supportLevel experimental}`、`targetDir`/`plannedResultPath`/`plannedReportPath` 均为原宿主机绝对路径（`C:\Users\Administrator.DESKTOP-LRHSLVD\Desktop\code-convert-skill\docs\test\dataset-2\…`）、`files[0]{relativePath resource_manifest_builder.cpp, sourcePath …, translatedCodePath …\output\batch\target.ps1, success true, artifacts{hasSource true,hasTranslatedCode true,hasEvaluationNotes false,hasReplayArtifact false}}`、`x_adapter{status "converted-and-evaluated", executionApproved true, jobId eval-20261010-145923-8c852ab1, prerequisites[3], isolationLaunchArgs[4], explorationOnly false, attackClassification{status reviewed,tactics[],techniques[],rationale …}}`。**与当前副本可检查性分开**：manifest 的 `success/hasTranslatedCode/translatedCodePath` 是历史交付声明，指向的 `target.ps1` 已不在副本。

**batch/items**：disposition `CONVERTED`、phase `CLOSED`、lifecycle `DONE`、`verdicts{sourceBuild completed/0, targetBuild "completed/0 (PASS)", execution "both completed/0", comparison "matched (output)", environment clean, safety "ALLOWED; no network; local file writes only"}`、`finalTargetSha256 e9f9c25d…ff49`、`blockingReasons []`、`codeRevisions 1`、`selfRepairRounds 1`、`coverageGap`（平台未采集 filesystem 维度；两文件字节等价仅有静态复审支持；写失败路径差异理论不可达）、`usage{prompt 3017, completion 24460, reasoning 23445, requests 2, model deepseek-flash, failedAttempts 0}`。

**独立证据事实与限制**：
- 原件支持：双侧 build/execution 均为 `completed/0`；两侧 stdout 结构化值逐字节相同且 digest 相同（`bdea5a99…2e27`）；`output` 维度 matched；双侧 cleanup PASSED、环境 clean；分类 ALLOWED（2 文件）。
- 历史说明：frozen 的提交链路对照实验结论、result.md 的过程叙述、manifest 的交付声明，均为记录文本。
- 当前规则对照：分层报告执行到位（[交付契约 §2.3](../../../../../references/framework/delivery-handoff-contract.md) 第 214/217 行）；`filesystem` 未采集如实写 UNVERIFIED 方向（评估准备 §5 第 97 行"matched 不是编译证据"、维度 not-applicable 不代表无副作用）；**matched 只覆盖 output 1 个维度**，不得说成完整功能覆盖。
- 待核验：目标交付文本已删，`targetHash` 非哈希 → 平台实际评测的是哪一份目标稿**只能由 item/model.json 的哈希链推断**，不能从 job 材料独立复核（B-08）；`evidence-*.json` 2000 字符后的 `observations`/清理字段不可读；job-00 的 mismatched 原判保留在原件中（B-06）；`result.md` 说的目标路径与实际目录不一致（B-09）。
- 边界：本项是本 10 项中**唯一**有完整"生成→自审→自修→双侧评估→匹配"链条的项；结论限于 output 维度。

**分类归入**：已有规则落实（分类准入 §3 身份门禁整树分类、交付 §2.3 分层报告、评估准备 §5 采信边界；均实际操作到位）；知识新增/已有规则融合（B-11 的换行义务：语言页/共性页/文件场景已有，方向页缺专条）；装置（B-04/B-06/B-08/B-09/B-16/B-17）；源已有（无）。错误建议：无（自审两条 major 属转换引入且有源/目标定位，按规则修复，未被后续推翻）。

### D2-089 / cpp-to-powershell / shell-aes.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-089-cpp-shell-aes.cpp`

**文件清单与读取状态**（23 件）：
- 01-frozen：`frozen-inputs.md`（已读，26 行）、`classifier-input.json`（已读，7 行）、`classification-1.json`（已读，106 行）。
- 02-conversion / 03-self-review：**均无**（0 模型调用）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`（各已读）；`returned-evidence/evidence-source.json`（**已读，截断**）、`returned-evidence/evidence-target.json`（已读，`evidence_not_found`）、`returned-evidence/evaluation_report.json`（已读，完整）、`returned-evidence/controller.log`（已读）。**无** health-before/runners-before。
- 04-evaluation/job-00b-fpermissive：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`（各已读）；`returned-evidence/evidence-source.json`（**已读，截断**）、`returned-evidence/evidence-target.json`（**已读，截断**）、`returned-evidence/evaluation_report.json`（**已读，截断**）、`returned-evidence/controller.log`（已读）。**无** comparison.json / health-before / runners-before。
- 根层：**无** `result.md`、无 `evaluator_manifest.json`、无 `target.*`（frozen:26 明确"无 `target.ps1`／`result.md`／`job-01-dual-build`"）。
- 另有 `batch/items/D2-089.json`（已读）。

**身份/版本关联**：taskId/rawItemId `D2-089`｜batchId `batch`｜direction `cpp-to-powershell`｜kind `NEW`｜disposition `FROZEN`｜phase `CLOSED_ORACLE_NOT_FREEZABLE`｜lifecycle `PARTIAL`｜pendingAction `null`｜sourceSha256 `8ab0a85dc9cc48286fb45fcd8a61c1b7ca53e8f7203fabde68b58563d97edbb1`（manifest 行 89、frozen:8、classifier-input:5、classification-1:47、两个 job 的 metadata `sourceHash` 一致）｜finalTargetSha256 无｜classifier `v2.4`/`009a6f31…f3a4`/ALLOWED/null/`REVIEW_NETWORK`（`reviewGroups ["network","process"]`；`shell-aes.cpp` `network_mode "loopback"`、`network_targets[{127.0.0.1,L62,loopback,literal,redirectVerified false}]`、`network` L15、`process` L87；`run_case.py` `process` L13,21,48,59,63,64）｜jobIds `eval-20261011-055818-abcf7dee`（实验 A，failed）、`eval-20261011-060037-0cd1026f`（实验 B，completed/0）｜runner `windows-vm-agent-x64`、vmName `windows-eval`、snapshot `CC-Eval-Windows-8Lang-1.0.28`、agentVersion/collectorVersion `1.0.0`、contractSetHash `sha256:a9ed1445…d82e`｜model 未记（0 调用）。

**冻结/分类**：frozen 记"Windows AES shellcode 加载器（`winsock2`+`wincrypt`，硬编码 `127.0.0.1` 与端口）。**只构建，未进入生成。**"、sourceLines 89（与 manifest `Lines=73` 不一致，B-03）、sourceOs windows；构建前提表 A/B 两次实验与精确命令；引"§10.17"表达 C 风格隐式转换；评估就绪核对记"无可观察量 ⇒ `ORACLE_NOT_FREEZABLE` / `UNVERIFIED`"（源侧执行 `completed/0`、stdout 0 字节、stderr 0 字节、程序不读 argv、无输入分支）、按"§10.16"记 lifecycle `PARTIAL`、不记转换失败/行为通过、不重复重提、不进入生成。分类 ALLOWED/`REVIEW_NETWORK`；`classification-1.json` 覆盖 2 文件，而 `classifier-input.json` 只列 1 文件（B-05）；`inputManifestSha256 a74f1f8f…7903`。无 `classification-2/3`。哈希一致。

**源预检**：job-00（实验 A）`input_profile.json`：`argv []`/`stdin null`/`timeout 30`/`dimensions ["output"]`/`normalized-text`+`exact`/`profileId "D2-089"`；`comparison_manifest.json` source `g++ -std=gnu++17 shell-aes.cpp -o program.exe -lws2_32 -ladvapi32`、target `pwsh -NoProfile -File build_case.ps1`；`metadata.json` `networkBoundary "isolated VM"`、`targetArtifact target/target.ps1 (placeholder)`、`safetyClassification "classifier-2.4"`（未带 ALLOWED/cls）。真实结果：source `build.status failed`/`exitCode 1`/`durationMs 3409`、stderr 含 `shell-aes.cpp:45:52: error: invalid conversion from 'char*' to 'BYTE*' …[-fpermissive]`；`evidence-target.json` = `{"detail":"evidence_not_found"}`；`evaluation_report.json` 源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`，目标侧 `performed false`/`SKIPPED`，平台 `runVerdict blocked`/`codeVerdict inconclusive`/`behaviorVerdict inconclusive`/`coverageRatio 0.0`、`failure.reason "Source build failed; baseline cannot be established."`；`controller.log` 2 行（05:58:18 / 05:58:54）。
- job-00b（实验 B，`-fpermissive`）`input_profile.json` 同 A；`comparison_manifest.json` source `g++ -std=gnu++17 -fpermissive shell-aes.cpp -o program.exe -lws2_32 -ladvapi32 -lcrypt32`（比 A 多 `-fpermissive` 与 `-lcrypt32`）；`metadata.json` `note "job-00b isolation experiment: add -fpermissive (one flag) to separate C-style-in-C++ conversion errors from genuine defects."`。真实结果：source `build.status completed`/`exitCode 0`/`durationMs 4182`、stderr 含同诊断 `warning`；**同时提交了占位目标**（`evidence-target.json` target `build completed/exitCode 0`/`durationMs 2180`、`execution.status completed`/`exitCode 0`、stdout `"D2-089 placeholder\n"` 20 字节、digest `9b634e46…a948`），故该 job 平台原判 `runVerdict "partial-runnable"`、`codeVerdict "failed"`、`behaviorVerdict "mismatched"`、`coverageRatio 1.0`——**占位装置产物**（B-06）；源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`。**comparison.json 未取回**（report 的 `comparisonRef` 指向 `comparison/result.json`）。`controller.log` 2 行（06:00:37 / 06:01:50）。
- 两个 job 的 `batch-authorization.json` 内容相同（`authorizedBy gyh-p1`、14:43:00Z 授权、`validUntil 2026-10-17`、三个 vmIsolation 与三个 networkIsolation 字段全 true、`contractHash a9ed1445…d82e`），但 `dataSource.confirmation` 是 **D2-151 的文本**（B-07）。

**模型请求/响应**：无（0 调用；frozen:26 与 item `usage.requests 0` 一致）。

**失败/废弃/重提 attempt**：**有**——实验 A（job-00）构建失败 → 归因"契约差异（C 风格代码按 C++ 编译）"→ 实验 B（job-00b）加单个 `-fpermissive` 后 `completed/0`；两个 job 目录并存、命令与诊断均留证（B-13）。无废弃 job。item 未记 `failedAttempts`。

**自审**：无（不适用）。

**job 证据**：见上两 job；**均无** health-before/runners-before、无 after/closure；job-00b 无 comparison.json。平台原判（A：blocked/inconclusive；B：partial-runnable/failed/mismatched）**均系源构建失败或占位目标产物**，本审阅保留原判、不改判、不当作转换结论。

**result / evaluator manifest**：均**缺件**，且 frozen 第 26 行**明示**不产（B-02/B-03 组合）；现行规则下 PARTIAL 项仍须 result.md 记暂停/限制与恢复条件。

**batch/items**：disposition `FROZEN`、phase `CLOSED_ORACLE_NOT_FREEZABLE`、lifecycle `PARTIAL`、`sourcePrecheck.experimentA/experimentB` 与 `verdict "SOURCE_BUILDABLE (after contract correction)"`、`blockingReasons ["ORACLE_NOT_FREEZABLE"]`、`evaluationReadiness.verdict ORACLE_NOT_FREEZABLE` + `detail`（源执行 completed/0、0 字节流、不读 argv、无非退化观察量、无替代 argv 可冻；按 10.6/10.16 记 UNVERIFIED + ORACLE_NOT_FREEZABLE、PARTIAL；不是转换失败也不是行为通过）、`verdicts{sourceBuild "completed/0 (contract-corrected)", targetBuild/execution/comparison UNVERIFIED 或说明, safety ALLOWED}`、`usage.requests 0`。

**独立证据事实与限制**：
- 原件支持：A/B 两次源构建的真实诊断与退出码；B 的清理/环境状态；"源执行 0 字节 stdout/stderr"这一说法**在本副本中只能由 frozen 文字与 item 得到，两个 evidence-source 的 2000 字符后段（execution stdout/stderr/observations）本会话读不到** → 该观察量**待核验**（B-15 同族限制）。
- 历史说明：frozen 关于"程序不读 argv、无输入分支、无法另冻条件"的判断属源码静态取证（源正文已删，无法复核）。
- 当前规则对照：见 B-13（契约修正留证）与 B-14（未生成与现行 §1.3 分支方向的差异）；[评估准备 §4](../../../../../references/framework/evaluation-readiness-contract.md) 第 87 行"记 ORACLE_NOT_FREEZABLE + UNVERIFIED，停止该行为评估并部分交付"与本项 PARTIAL 一致，但组合 §1.3 后仍应继续转换并验目标语法/编译。
- 待核验：frozen 引用的"§10.17/§10.6/§10.16"在现行 `references/`、`AGENTS.md` 中未核到（历史编号）；job-00b 的 comparison 原件缺；`batch-authorization` 数据源文本错误。
- 边界：本项**没有**目标代码、没有目标语法/编译证据、没有行为结论；`PARTIAL` 只表示本轮停止并完成适用部分交付。

**分类归入**：已有规则落实（构建前提 §4.1 契约修正留证；评估准备 §4 ORACLE_NOT_FREEZABLE 语义）；未定/待核（B-14 分支方向差异、历史编号）；装置（B-05/B-06/B-07/B-16）；环境（loopback 目标无对端，属源形态）；源已有（AES shellcode 加载器行为本身）。

### D2-090 / cpp-to-powershell / env_detect.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-090-cpp-env_detect.cpp`

**文件清单与读取状态**（13 件）：
- 01-frozen：`frozen-inputs.md`（已读，24 行）、`classifier-input.json`（已读，7 行）、`classification-1.json`（已读，96 行）。
- 02-conversion / 03-self-review：**均无**（0 模型调用）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`（各已读）；`returned-evidence/evidence-source.json`（**已读，截断**）、`returned-evidence/evidence-target.json`（已读，`evidence_not_found`）、`returned-evidence/evaluation_report.json`（已读，完整）、`returned-evidence/controller.log`（已读）。**无** health-before/runners-before。
- 根层：**无** `result.md`、无 `evaluator_manifest.json`、无 `target.*`（frozen:24 明示不产）。
- 另有 `batch/items/D2-090.json`（已读）。

**身份/版本关联**：taskId/rawItemId `D2-090`｜batchId `batch`｜direction `cpp-to-powershell`｜kind `NEW`｜disposition `FROZEN`｜phase `CLOSED_ORACLE_NOT_FREEZABLE`｜lifecycle `PARTIAL`｜pendingAction `null`｜sourceSha256 `0c3afc330fa75cb8dded3dfca784e6f46b7ff11ce773fe2bfd5163d232f48078`（manifest 行 90、frozen:8、classifier-input:5、classification-1:17、job metadata 一致）｜finalTargetSha256 无｜classifier `v2.4`/`009a6f31…f3a4`/ALLOWED/null/`REVIEW_SENSITIVE`（`reviewGroups ["dynamic_code","process"]`；`env_detect.cpp` `dynamic_code` L84；`run_case.py` `process` L13,21,48,59,63,64；`requiresSyntheticData true`）｜jobId `eval-20261011-060225-8388a3ff`｜runner `windows-vm-agent-x64`、vmName `windows-eval`、snapshot `CC-Eval-Windows-8Lang-1.0.28`、agentVersion/collectorVersion `1.0.0`、contractSetHash `sha256:a9ed1445…d82e`｜model 未记（0 调用）。

**冻结/分类**：frozen 记"Windows 动态 API 解析 PoC（`LoadLibrary` + MurmurHash 定位 `MessageBoxA`，打印地址后弹窗）"、sourceLines 90（与 manifest `Lines=76` 不一致，B-03）、sourceOs windows；源侧预检 SOURCE_BUILDABLE（`g++ -std=gnu++17 -fpermissive env_detect.cpp -o program.exe` → completed/0）；评估就绪核对记不可冻结且不终止：源执行 `status=timed-out`/`durationMs=30022`/stdout 0 字节/stderr `command timed out`；两条独立阻断——（1）`printf("0x%p\n", addr)` 打印 ASLR 相关 API 地址（不在消噪记号覆盖内，不可复现）；（2）`myMessageBoxA(...)` GUI 弹窗在 headless VM 不返回 ⇒ 驱动四要素第④项不满足，只能靠平台超时收尾；程序不读 argv、无法另冻条件；记 `UNVERIFIED` + `ORACLE_NOT_FREEZABLE`、lifecycle `PARTIAL`、不进入生成、0 模型调用、无 target/result/job-01。分类 ALLOWED/`REVIEW_SENSITIVE`；`classification-1.json` 覆盖 2 文件（与 `classifier-input.json` 的 1 文件不一致，同 B-05 型）；`inputManifestSha256 91bc7dcf…0fbc`。无 `classification-2/3`。哈希一致。

**源预检**：job `eval-20261011-060225-8388a3ff`。`input_profile.json`：`argv []`/`stdin null`/`timeout 30`/`dimensions ["output"]`/`normalized-text`+`exact`/`profileId "D2-090"`。`comparison_manifest.json`：source `g++ -std=gnu++17 -fpermissive env_detect.cpp -o program.exe`，target `pwsh -NoProfile -File build_case.ps1`。`metadata.json`：`networkBoundary "isolated VM"`、`targetArtifact target/target.ps1 (placeholder)`、`safetyClassification "classifier-2.4"`（无 ALLOWED/cls）。真实结果（可见部分）：source `build.status completed`/`exitCode 0`/`durationMs 3150`、build stdout/stderr 均空；`execution.status "timed-out"`/`exitCode null`/`durationMs 30022`/`timedOut true`/stdout 0 字节/stderr 17 字节 `command timed out`（digest `sha256:14d5cadc…d729`）；`evidence-target.json` = `evidence_not_found`（目标侧未执行）；`evaluation_report.json`：源侧 `preflight/cleanup PASSED`、`contaminated false`、`environmentStatus clean`、`runnerStateAfter READY`，目标侧 `performed false`/`SKIPPED`，平台 `runVerdict blocked`/`codeVerdict inconclusive`/`behaviorVerdict inconclusive`/`coverageRatio 0.0`、`failure{type CODE_RESULT, category code, reason "Source execution timed-out; baseline unavailable."}`；`controller.log` 2 行（06:02:25 / 06:03:34）。源运行基线：**未取得**（超时且无输出，属退化观察）。

**模型请求/响应**：无（0 调用）。**失败/废弃/重提 attempt**：无（未重提；frozen 明确"不重复重提"）。**自审**：无。

**job 证据**：仅 job-00；**无** health-before/runners-before/after/closure；无 comparison.json（`comparisonRef null`，符合未比较）。平台原判已保留，不据其 `codeVerdict` 反推代码缺陷（B-15）。

**result / evaluator manifest**：均**缺件**且 frozen 明示不产（B-02）。

**batch/items**：disposition `FROZEN`、phase `CLOSED_ORACLE_NOT_FREEZABLE`、lifecycle `PARTIAL`、`sourcePrecheck{jobId,os,buildCommand,buildStatus completed,exitCode 0,verdict SOURCE_BUILDABLE,execution "timed-out after 30022ms; stdout 0 bytes; stderr 'command timed out'"}`、`blockingReasons ["ORACLE_NOT_FREEZABLE","DRIVER_NOT_VIABLE"]`、`evaluationReadiness.verdict "EVALUATION_NOT_READY"` + `detail`（ASLR 地址 + MessageBoxA 不返回 ⇒ 第④要素不满足；按 10.6/10.16 UNVERIFIED + ORACLE_NOT_FREEZABLE、PARTIAL）、`verdicts{sourceBuild "completed/0, execution timed-out", targetBuild/execution/comparison UNVERIFIED, safety ALLOWED}`、`usage.requests 0`。

**独立证据事实与限制**：
- 原件支持：源 build `completed/0`、源 execution `timed-out`（30022ms、stderr 原文）、job 清理/环境 clean、目标未执行。
- 历史说明：frozen 对 `printf` 与 `MessageBoxA` 行为的描述属源码静态取证；源正文已删，无法复核行号与调用细节。
- 当前规则对照：超时归因见 B-15（评估准备 §2 第 68 行 INCONCLUSIVE 属观察装置缺陷，与结构性无安全入口分开）；未生成与现行 §1.3 的差异见 B-14。
- 待核验：`evidence-source.json` 2000 字符后的 `observations`/清理字段不可读；frozen 引用的"§10.6/§10.16"为历史编号；manifest `Lines=76` vs frozen 90 未决。
- 边界：本项**无**目标产物与目标语法/编译证据；`PARTIAL` 不含任何行为通过含义；platform `codeVerdict=inconclusive` 不得读成代码失败。

**分类归入**：已有规则落实（评估准备 §4 ORACLE_NOT_FREEZABLE 语义与 PARTIAL 口径；安全边界未删行为、未伪造输出）；装置/环境（观察装置不足、GUI headless 结构性限制）；未定/待核（B-14 分支方向差异 + 历史编号）；装置（B-03/B-05 型/B-07/B-16）；源已有（动态 API 解析行为）。

## 覆盖清单（D2-091–D2-100，供 harness-b-coverage.md 汇总）

| 项 | 实际目录 | 现存文件数 | 已读 | 已读(截断) | 未读 | 空文件 | 缺件 |
|---|---|---|---|---|---|---|---|
| D2-091 | `cpp-to-powershell/D2-091-cpp-process_enum.cpp` | 38 | 38 | 5 | 0 | 0 | 8 |
| D2-092 | `cpp-to-powershell/D2-092-cpp-winhttp_impl.cpp` | 49 | 49 | 7 | 0 | 0 | 8 |
| D2-093 | `cpp-to-powershell/D2-093-cpp-inject_channel.cpp` | 53 | 53 | 8 | 0 | 0 | 8 |
| D2-094 | `cpp-to-powershell/D2-094-cpp-screenshot.cpp` | 1 | 1 | 0 | 0 | 0 | 5 |
| D2-095 | `cpp-to-python/D2-095-cpp-safe_attck_cpp_suite-local_c2_retry.cpp` | 37 | 37 | 5 | 0 | 0 | 8 |
| D2-096 | `cpp-to-python/D2-096-cpp-safe_attck_cpp_suite-collection_bundle.cpp` | 36 | 36 | 8 | 0 | 0 | 8 |
| D2-097 | `cpp-to-python/D2-097-cpp-evil_inj.cpp` | 45 | 45 | 8 | 0 | 0 | 8 |
| D2-098 | `cpp-to-python/D2-098-cpp-evil1.cpp` | 1 | 1 | 0 | 0 | 0 | 5 |
| D2-099 | `cpp-to-python/D2-099-cpp-processfind.cpp` | 1 | 1 | 0 | 0 | 0 | 5 |
| D2-100 | `cpp-to-python/D2-100-cpp-encode.cpp` | 14 | 14 | 2 | 0 | 0 | 7 |
| **合计** | 10 个目录 | **322** | **322** | **48** | **0** | **0** | **70** |

另读：`batch/items/D2-091..D2-100.json`（10 件，全部存在，多行 JSON、无截断）。10 项**均无** `case.md`、无 `source/`（原源正文与快照已删）、无 `capsule.zip`、无 job 内 `source/`/`target/` 暂存树。读取工具限制同 cases-01 前言：单行 JSON 截断于约 2000 字符，截断件只登记"可见部分"，未按"已读全文"计。

## D2-091..D2-100 新增发现（接 B-01..B-18；供 harness-b-findings.md 汇总）

19. **B-19｜本区间 6 项缺 `01-frozen/frozen-inputs.md`，其中 4 项仍有真实模型调用**｜分类：已有规则落实（缺口）／装置｜依据：[任务状态契约 §2.2](../../../../../references/framework/task-state-contract.md) 第 47 行"`frozen-inputs.md` 是冻结完成的必备记录，必须先写出再回读，不能等收尾补件"、第 49 行"分类前核对……空文件、模板占位、另一项或旧 run 的记录不能放行"；[分类准入 §1](../../../../../references/workflow/classifier-agent-gate.md) 第 9 行"缺文件、空白或身份/版本错位不得分类"；[根 SKILL.md](../../../../../SKILL.md) 第 24 行同义。实证：`D2-091/092/093/095/096/097` 的 `01-frozen/` **只有** `classifier-input.json`（+`classification-1.json`），逐项 glob 兜底亦 0 命中；其中 091（`usage.requests 2`）、092（3）、093（4）、095（2）、096（2）、097（2）**均已实际调用配置模型**（各自 `03-self-review/self-review-1.model.json` 的 `requestSha256`/`rawResponseSha256`/usage 与 `02-conversion/request.system.txt` 同在），故分类前冻结回读按现行文本**不可复核**，且"冻结 → 实际请求"的源范围/契约/知识快照关联（§2.1 第 36 行）本副本无法回读。反向对照：D2-094/098/099 有 27/17/18 行冻结记录且**未分类未提交**，D2-100 冻结 20 行 + 真实源预检 job 齐备｜边界：同批 D2-081–D2-090 与 cases-04 的 D2-151 均有该文件，故属**部分项形制缺失**而非本批统一简化；不改历史记录，只登记现行规则下的证据缺口。

20. **B-20｜6 项无 `02-conversion/target.gen.model.json`，交付稿哈希只能从 job `targetHash` 反查（4 项成立、2 项不成立）**｜分类：装置（版本关联原件不齐）｜依据：[交付契约 §2.2.1](../../../../../references/framework/delivery-handoff-contract.md) 第 202 行要求保留"原响应到文件的提取/解码……父/新目标身份与差异"；§2.1.1 第 93 行"在该轮 model.json 或其指向的不可变记录保存脱敏请求/原始响应与身份、哈希"。实证：`D2-091/092/093/095/096/097` 的 `02-conversion/` 只有 `request.system.txt`（092/093 另有 `repair.system.txt`，093 另有 `repair2.system.txt`），**无** `target.gen.*`、无 `.model.json`、无 `.raw.txt`、无 `target.<ext>` 交付稿。可达性：D2-092/093/095/096/097 的**最终**或**预修**目标稿可由 job `metadata.json` 的 `targetHash` 字符串回读（见 B-21/B-22）；D2-091 的 `0aa47eb2…2224` 只出现在 item `finalTargetSha256`、`result.md:16` 与 job-01 `metadata.targetHash` 三处**同源声明**，**无**任何模型/响应记录可回读其来源｜边界：目标正文已删，哈希不可还原实现；不据此推断未发生过生成（092/093 的 `repair.system.txt` 与 `repairChain` 证明生成发生过）。

21. **B-21｜D2-091 的交付链"末环"不对称：`finalTargetSha256` 与 job-01 一致，但生成轮次原件缺失、job-00b 仍是占位目标**｜分类：装置（版本关联部分可回读）｜依据：`items/D2-091.json:39` `finalTargetSha256 "0aa47eb23d3d4b0b4142e669a52b72c537f02ab1545b705c3b99128d97152224"`＝`04-evaluation/job-01-dual-build/metadata.json:11` `targetHash "sha256:0aa47eb2…2224"`＝`result.md:16` 行内声明（**三处一致，优于 D2-088 的 B-08**）；同一 job 的 `evidence-target.json` `execution.stdout` `sizeBytes 29`/`digest sha256:b14a55beb9fd216d3863e508024ed697cf4a278589f0de1e8ffb4185c7dc6fed` 与源侧 `PID not found :( exiting...\n`（见 B-25 的字节计数讨论）逐字节一致；但 `02-conversion/` 只有 `request.system.txt`，job-00b 的 `metadata.targetHash "sha256:placeholder-precheck"` 仍是占位（B-23 型）｜边界：job-01 的 `sourceHash` `77713984…b42f` 与 manifest 行 91、`classifier-input.json:5`、`classification-1.json:18` 四处一致，源侧身份链完整。

22. **B-22｜D2-092/093 的失败轮目标版本只由 job `targetHash` 绑定，与最终交付版不同**｜分类：已有规则落实（第三方反馈轮次保留）｜依据：[评估准备 §5](../../../../../references/framework/evaluation-readiness-contract.md) 第 103 行"原平台 behaviorVerdict 原样保留……修正后另记 job，不能改写原始记录"；[闭环 §3.2](../../../../../references/workflow/conversion-evaluation-loop.md) 第 110 行"每个问题保留'提出→修复提案→新版本→平台重评'的关联记录"。实证：D2-092 job-01 `metadata.targetHash "sha256:2c6a07c3ce94c1c429b624843437e057c2fc39a68041e2d3a6541e5f1c86381c"`（`mismatched`，`comparison.json` `dimensions.output.diffs[0]` `path stream.digest`、`sourceValueSummary sha256:e3b0c44298fc1`/`targetValueSummary sha256:c3e8217719b9c`）→ job-02 `targetHash "sha256:4fb83b910de1dcd7dba0f632889a79d0246ca6e80357ae26758ba63c068ed581"`＝`items/D2-092.json:38` `finalTargetSha256`＝`result.md:16`（**三方一致**）；D2-093 job-01 `targetHash "sha256:e75a403b3fb0e5b5ebcd3288f1ab70ace71a3552f6202ce563387c651164d70b"`（`mismatched`，`MethodInvocationException` @ `target.ps1:54`）→ job-02 `targetHash "sha256:5695e7c551bd1b90fcb267e4e22e60fbef95e09d46c0fefc276dba066be326d8"`＝`items/D2-093.json:38` `finalTargetSha256`＝`result.md:16`（**三方一致**）｜边界：被评的**中间**目标稿正文已删，只能由 `targetHash` 字符串区分轮次；D2-092 与 D2-093 均**只有 1 类**中间版本被绑定（093 的两轮评估后修复共享 job-02 交付结果，第 1 轮未收敛稿无独立哈希）。

23. **B-23｜本区间 7 项沿用旧"占位目标"预检装置提交 job-00/job-00b，平台据此回传 `mismatched`/`blocked`；与 D2-100 的"目标侧 `SKIPPED`、`comparisonRef null`"形成对照**｜分类：装置（旧占位装置）＋已有规则落实（source-only 机制已存在）｜依据：D2-091 job-00 `evidence-target.json` `execution.stdout.normalizedText "D2-091 placeholder\n"`、`metadata.json:9` `targetArtifact "target/target.ps1 (placeholder)"`、`targetHash "sha256:placeholder-precheck"`，同 job `evaluation_report.json` `outcome.runVerdict "partial-runnable"`/`codeVerdict "failed"`/`behaviorVerdict "mismatched"`；D2-092 job-00、D2-093 job-00、D2-095 job-00、D2-096 job-00 同形；D2-091 job-00b（argv 重冻那一轮）**也**同时跑了占位目标并返回 `mismatched`。反向对照：D2-100 的 `evaluation_report.json` 记目标侧 `execution.performed false`、`preflight/cleanup "SKIPPED"/attempts 0`、`comparisonRef null`、`evidenceCoverage.coverageRatio 0.0`、`evidence-target.json` = `{"detail":"evidence_not_found"}`——即**同一批内已有"不提交占位目标"的形态**。现行[评估准备 §1.1](../../../../../references/framework/evaluation-readiness-contract.md) 第 31 行与[交付契约 §2.1.1](../../../../../references/framework/delivery-handoff-contract.md) job-00 行（第 172 行）均已提供 source-only 预检机制｜边界：**这些 `mismatched`/`failed` 是占位装置产物，不得当作转换失败**（与 cases-01 B-06 同型）；原 verdict 不改写；D2-092 的 job-01 `mismatched` 与 D2-093 的 job-01 `mismatched` 是**真实目标稿**的失败轮，与本节占位产物性质不同，分别记录。

24. **B-24｜D2-092 自审已给 `REPAIR-RECOMMENDED` + 高确定度定位，目标仍被提交并取得 `mismatched`**｜分类：未定/待核（内部预检放行与现行文本的差异）｜依据：`03-self-review/self-review-1.json` `verdict "REPAIR-RECOMMENDED"`，条目 5 `location "target.gen.ps1: 第 3 段 \`printf_pid:\`"`、`issue`"新增了源不存在的失败路径……直接违反冻结契约"、`proposed_fix`"删除整行 `printf_pid:`"、`risk "高：确定性的行为偏差，且是本次转换唯一实质缺陷"`，条目 6 同因；`03-self-review/self-review-1.model.json` `verdict "REPAIR-RECOMMENDED"`；随后 job-01（`eval-20261011-062151-7bd8dcf7`）`evidence-target.json` `execution.stderr.normalizedText` 含 `printf_pid:: ` 与 `…\target\target.ps1:107`，`comparison.json` `behaviorVerdict "mismatched"`。对照现行[闭环 §4 内部预检放行依据](../../../../../references/workflow/conversion-evaluation-loop.md) 第 138 行"原 verdict 为 `REPAIR-RECOMMENDED`，但全部相关条目已据证据裁定为源已有问题、误报或已解决时，不要求改写原 verdict"，反推"未裁定为误报/已解决时不得作为内部预检通过"；`result.md:28-30` 与 `02-conversion/repair.system.txt` 记修复在**评估后**发生（1 轮，`postEvalRepairRounds 1`）｜边界：修复结果正确（job-02 `matched`）且失败轮原件完整保留（符合 §3.2），本条只登记"自审高确定度阻断项未在提交前处理"这一可复核时序事实，不追改 item 状态；现行文本未明文禁止"带 REPAIR-RECOMMENDED 提交"，故记**未定**。

25. **B-25｜D2-095 的 stdout 字节计数两侧不一致（58 B vs 57 B）而 `behaviorVerdict` 仍为 `matched`**｜分类：未定/待核（观察与摘要不一致）｜依据：`job-01-dual-build/returned-evidence/evidence-source.json` `execution.stdout.normalizedText "{\"case\":\"c2_advanced\",\"state\":\"not_connected\",\"resp\":\"\"}\n"`、`digest sha256:7beba5e84c3301c1d3254d0b3763123e2deb7cb20d178401449123fd3447afc5`、**`sizeBytes 58`**；同 job `evidence-target.json` 同一 `normalizedText`、`digest sha256:6ff6d91b3a1ce3a5928da9c1e581d66971e3e5ea5ee7843f1706b32a39fefd93`、**`sizeBytes 57`**（两文件均在 2000 字符内可见到 `sizeBytes`，非截断猜测）；同 job `comparison.json` `behaviorVerdict "matched"`、`dimensions.output.status "matched"`、`diffs []`；`input_profile.json` 两侧均 `stdoutMode "normalized-text"`、`stderrMode "exact"`；`items/D2-095.json:32` 记 `execution "both completed/0; stdout byte-identical; stderr empty"`，`result.md:26` 记"两侧 stdout 逐字节相同"｜边界：正确读法是**目标写对了源合同字节、源侧采集/摘要少算了末尾换行**（`normalizedText` 含 `\n`，`sizeBytes` 少 1）；[评估准备 §5](../../../../../references/framework/evaluation-readiness-contract.md) 第 99 行明确"原始流的 digest/sizeBytes 与平台 normalizedText 是不同观察对象"，故本条**不得**读成目标缺字节或转换失败，也不得据 `matched` 反推字节义务已证；D2-096 同型比较两侧均 `sizeBytes 52`（无此差异），说明不是全批共性。

26. **B-26｜D2-093 自审 `NO-REPAIR-IDENTIFIED` 未发现真实缺陷，job-01 才由第三方暴露 payload 十六进制丢位**｜分类：未定/待核（自审覆盖边界）｜依据：`03-self-review/self-review-1.json` `verdict "NO-REPAIR-IDENTIFIED"`，7 条 `issue` 逐条写"无偏差/无缺陷"（条目 1–7 均未提及 payload hex 长度）；`03-self-review/self-review-1.model.json` `parseNote "response body is malformed JSON (unescaped quote / control character ~char 1581); per batch discipline 2 the verdict and items were recovered by regex and the RAW response is preserved unchanged"`；job-01（`eval-20261011-063518-76bfc0cd`）`evidence-target.json` `execution.stderr` `MethodInvocationException … target.ps1:54`（`Substring` 越界），`02-conversion/repair.system.txt` 记"实测：here-string 正文去掉空白后只有 **625 个十六进制位（奇数）**……源的 `my_payload[]` 共 **313 字节（= 626 个十六进制位）**"，`repair2.system.txt` 进一步定位"目标在 `e8d00000` 之后**少写了一个 `0`**"｜边界：该自审响应正文 JSON 损坏（仅正则恢复 verdict/条目），其审阅覆盖**不完整**；现行[闭环 §4](../../../../../references/workflow/conversion-evaluation-loop.md) 第 134 行"损坏 JSON 只提取 verdict 不能证明审阅范围/条目完整"正是本条依据；`result.md:46` 亦如实附注；不把该 `NO-REPAIR-IDENTIFIED` 当"未发现问题"的证明，也不因此改判历史状态。

27. **B-27｜D2-096 使用双侧 fixture 并在 `request.system.txt` 声明，但两份 `input_profile.json` 的 `fixtures` 均为 `[]`**｜分类：装置（观察输入未在 profile 声明）｜依据：`02-conversion/request.system.txt:21`"两侧均在 `data/collect_me/` 下放有同一个 6 字节文件 `a.txt`（内容 `hello\n`）"；`items/D2-096.json:27` `sourcePrecheck.note "execution completed/0 with the 6-byte fixture; stdout files:1 total:6"`；`result.md:28`"**fixture 设计**：两侧同放 `data/collect_me/a.txt`（`hello\n`，6 字节），使 oracle 非平凡"；而 `job-00/input_profile.json` 与 `job-01/input_profile.json` 均 `"fixtures": []`（第 11 行，23 行文件内完整可见）；`metadata.json:5` 亦记"Same 6-byte fixture on both sides"。对照[评估准备 §4 两侧对称](../../../../../references/framework/evaluation-readiness-contract.md) 第 89 行"argv 点名文件两侧存在且内容一致……必要中性 fixture 必须有合法来源和冻结说明"｜边界：fixture 的**合法性/来源**本身不可由本副本回读（未记提供者与哈希；`classification-1.json` 里出现的 `a.txt` 哈希 `5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03` 是 5 字节 `hello`，与"6 字节 `hello\n`"**不同**，两者是否同一对象无法判定）；观察确实非退化（`files:1,total:6` 两侧 `sizeBytes 52`、同一 digest `1811c9cee6710550149f9916ad538b38da314e19c17549651283c313393dc4ba`），故本条只登记"声明位置缺失"，不改判该 `matched`。

28. **B-28｜本区间 5 项的自审响应均非裸 JSON（围栏/前言/损坏），均按"批次纪律 §2"正则恢复并保留原文**｜分类：装置（模型输出形制）＋已有规则落实（容错处置）｜依据：D2-093 `self-review-1.model.json` `parseNote "response body is malformed JSON (unescaped quote / control character ~char 1581)…"`；D2-096 `parseNote "response body is not a bare JSON object (has a preamble); verdict and items recovered by regex, raw response preserved (batch discipline 2)"`，`result.md:39` 记"自审响应被 ```json 围栏包裹（非裸 JSON）"；D2-091/092/095/097 的 `self-review-1.model.json` 无 `parseNote`（形制正常）。对照[闭环 §4](../../../../../references/workflow/conversion-evaluation-loop.md) 第 118 行"请求明确要求 content 只返回一个裸 JSON 对象……格式有效不证明内容正确"、§4.1 第 134 行"完整对象仅带 Markdown 围栏时可机械去围栏，另存恢复依据并保留原文；损坏 JSON 只提取 verdict 不能证明审阅范围/条目完整"｜边界：D2-093 的损坏响应即 B-26 的覆盖缺口（`reviewedScope` 字段**缺失**，7 条只有 `id`/`origin`/`issue`，无 `location`/`evidence`/`proposed_fix`/`risk`）；D2-096 的 7 条同样只有 `id`/`origin`/`issue`，`reviewedScope` 缺失；属**条目字段不齐**而非"未审"，不改判 verdict。

---

### D2-091 / cpp-to-powershell / process_enum.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-091-cpp-process_enum.cpp`

**文件清单与读取状态**（38 件）：
- 01-frozen：`classifier-input.json`（已读，7 行）、`classification-1.json`（已读，101 行）。**无** `frozen-inputs.md`（B-19）。
- 02-conversion：`request.system.txt`（已读，20 行）。**无** `target.gen.*`、无 `.model.json`、无 `target.ps1`（B-20）。
- 03-self-review：`review.system.txt`（已读，12 行）、`self-review-1.json`（已读，69 行，7 条全登记）、`self-review-1.model.json`（已读，18 行）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`（各已读）；`returned-evidence/evidence-source.json`（**已读，截断**）、`evidence-target.json`（**已读，截断**）、`evaluation_report.json`（**已读，截断**）、`controller.log`（已读，2 行）。
- 04-evaluation/job-00b-argv-refreeze：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`（各已读）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stdout`）、`evidence-target.json`（已读，可见至 `observations`）、`evaluation_report.json`（**已读，截断**）、`controller.log`（已读，2 行）。
- 04-evaluation/job-01-dual-build：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`、`controller-health-before.json`（各已读）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stdout`）、`evidence-target.json`（已读，可见至 `observations`）、`evaluation_report.json`（**已读，截断**）、`evaluation_report.md`（已读，77 行）、`comparison.json`（已读）、`controller-health-after.json`（已读）、`controller.log`（已读，2 行）。
- 根层：`result.md`（已读，52 行）、`evaluator_manifest.json`（已读，70 行）。**无** 根级 `target.ps1`。
- 另有 `batch/items/D2-091.json`（已读，54 行）。

**身份/版本关联**：taskId/rawItemId `D2-091`｜batchId `batch`｜direction `cpp-to-powershell`｜kind `NEW`｜disposition `CONVERTED`｜phase `CLOSED`｜lifecycle `DONE`｜pendingAction `null`｜sourceSha256 `77713984fe51769872d5fa15373f8a3b8cc93174fb6db312e02f58c8b2cfb42f`（manifest 行 91 大写、frozen 无、`classifier-input.json:5`、`classification-1.json:18`、job-00/00b/01 `metadata.sourceHash` 一致）｜**finalTargetSha256 `0aa47eb23d3d4b0b4142e669a52b72c537f02ab1545b705c3b99128d97152224`**＝job-01 `metadata.targetHash`（B-21）｜classifier `v2.4`/`sha256 009a6f31177b08334663340321494ace1e430de13f8a5687e6843ab26839f3a4`/ALLOWED/null/`REVIEW_SENSITIVE`（`reviewGroups ["dynamic_code","process","sensitive"]`；`process_enum.cpp` `sensitive` L75,78,81、`dynamic_code` L56；`run_case.py` `process` L13,21,48,59,63,64；`requiresSyntheticData true`；`inputManifestSha256 0df5eb3834062afdfa4f23aa51d3c0ed863d5a40b90fa19e3215938c34d19d7f`）｜jobIds `eval-20261011-060508-a6eb866c`（job-00，argv `[]`）、`eval-20261011-060726-46c684e0`（job-00b 重冻，item `sourcePrecheck.jobId`）、`eval-20261011-061409-2d2c7d14`（job-01，item `dualBuildJobId`）｜runner `windows-vm-agent-x64`、vmName `windows-eval`、baselineSnapshot `CC-Eval-Windows-8Lang-1.0.28`、agentVersion/collectorVersion `1.0.0`、contractSetHash `sha256:a9ed144595a658a44301a3638e0d14224a130b65e7e5debce8f237ff6ecdd82e`｜model `deepseek-flash`（`item.usage.model`、`self-review-1.model.json:5`；`request.system.txt` 未记 temperature/RAG）。**未记任何 selected skills 路径/哈希**（与 B-17 同型；本项连 frozen 页都没有）。

**冻结/分类**：**`frozen-inputs.md` 缺件**（B-19），故身份/方向/源集合的冻结回读不可复核；`classifier-input.json` 单任务、`sourcePath source/process_enum.cpp`、哈希大写；`classification-1.json` `details.files` **2 项**（`process_enum.cpp` + `run_case.py`，与输入清单的 1 项不同——同 cases-01 B-04/B-05 型镜像错位），`analysisScope source-text-only`、`executionApproved true`、`limitations` 三条、`inputManifestSha256 0df5eb38…9d7f`。`job-00b`/`job-01` 的 `this-task-classification.json` 与 `classification-1.json` 内容一致（2 文件、同一 `inputManifestSha256`）。无 `classification-2/3`、无重分类 attempt。`result.md:31-34` 把两次调用登记为"1 生成 + 1 自审"，与 `item.usage.requests 2` 一致。

**源预检**：job-00 `eval-20261011-060508-a6eb866c`，`input_profile.json` `argv []`/`stdin null`/`timeoutSeconds 30`/`dimensions ["output"]`/`normalized-text`＋`exact`/`profileId "D2-091"`；`comparison_manifest.json` source `g++ -std=gnu++17 -fpermissive process_enum.cpp -o program.exe`、target `pwsh -NoProfile -File build_case.ps1`；`metadata.json` `networkBoundary "isolated VM"`、`targetArtifact "target/target.ps1 (placeholder)"`、`targetHash "sha256:placeholder-precheck"`、`safetyClassification "classifier-2.4"`（无 ALLOWED/cls）。真实结果（可见部分）：source `build completed`/`exitCode 0`/`durationMs 3232`、build stderr 409 字节 `process_enum.cpp:56:28: warning: invalid conversion from 'FARPROC' … to 'void*' [-fpermissive]`；source `execution.status completed`/`exitCode 4294967295`/`durationMs 4099`、**`stdout.normalizedText ""`（0 字节，退化）**；同 job 亦跑占位目标（`execution.stdout "D2-091 placeholder\n"`、`exitCode 0`），故平台 `runVerdict "partial-runnable"`/`codeVerdict "failed"`/`behaviorVerdict "mismatched"`/`coverageRatio 1.0`（B-23）｜**重冻 job-00b `eval-20261011-060726-46c684e0`**：`input_profile.json` `argv ["nosuchprocess"]`（其余同 job-00）；源 `build completed/0`/`durationMs 3283`（同一条 `-fpermissive` warning）、`execution completed`/`exitCode 4294967295`/`durationMs 71`、`stdout.normalizedText "PID not found :( exiting...\n"`；`metadata.note` 明写"argv=[nosuchprocess] (main requires argv[1]; empty argv makes argv[1] NULL and the run degenerate)"；同 job 目标仍为占位（`"D2-091 placeholder\n"`）→ 平台同样 `mismatched`（B-23）｜源运行基线：**job-00b 取得非退化基线**（stdout 非空 + 退出码由 `return -1` 决定）；清理依据：job-00 与 job-00b 的 `evaluation_report.json` 源侧均 `preflight PASSED/1`、`cleanup PASSED/1`、`contaminated false`、`environmentStatus "clean"`、`runnerStateAfter "READY"`；目标侧同样 PASSED（因占位目标被执行）。`controller-health-before.json`/`controller-health-after.json` 只存在于 **job-01**；job-00/job-00b **无** health/runners 快照。

**模型请求/响应**：`request.system.txt`（20 行）＝C++→PowerShell 转换器系统提示：单一 ```powershell 代码块、stdout/stderr **逐字节**与退出码不变、不得删功能/桩替、目标名 `target.ps1`；6 条适用规则（`argv[1]→$args[0]` 不得照搬 C 下标；`printf`→不追加换行的写法；`return -1`→`exit -1` 得 0xFFFFFFFF；`findMyProc`/Toolhelp32 必须忠实映射；`OpenProcess`/`VirtualAllocEx`/`WriteProcessMemory`/`CreateRemoteThread` 必须忠实映射但冻结 argv 下不得执行；不得新增行为）；末段给出"已实测行为契约"（`PID not found :( exiting...\n`、29 字节、stderr 空、退出码 4294967295）。**无知识页正文**（仅声明"取自项目 Skill"）。`target.gen.model.json` **缺件**：生成轮的实际 usage、finishReason、request/output 哈希**不可回读**；`result.md:31-34` 表记生成轮 `1650/29426/27981`（与 `item.usage` 的 `promptTokens 4377`＝1650+2727、`completionTokens 40733`＝29426+11307、`reasoningTokens 36877`＝27981+8896 自洽）。**原响应正文**：无 `raw.json`/`.raw.txt`，不可回读。

**失败/废弃/重提 attempt**：**有**——argv 由 `[]` **重冻**为 `["nosuchprocess"]`（`item.sourcePrecheck.refreezeNote` 与 `argvRefreezeNote` 均记"Recorded as a new freeze condition, not a rewrite"）；job-00 与 job-00b 目录并存、各自保留 `input_profile.json`/`evidence-source.json`/`evaluation_report.json`，**原记录未被覆盖**（符合[任务状态 §2.1](../../../../../references/framework/task-state-contract.md)）。无 `attempt-*-403.json`、无废弃 job、无 `job-02*`。`item.failedAttempts 0`（模型调用层无失败）。

**自审**：`review.system.txt`（12 行）要求静态对照并输出裸 JSON `{verdict, reviewedScope, items[{id, location, evidence, origin, issue, proposed_fix, risk}]}`，含 7 条核对项（argv 语义、早退分支、输出字节/CRLF、`findMyProc` 映射、注入路径映射且不可达、是否新增行为、安全）。`self-review-1.json` **`verdict "NO-REPAIR-IDENTIFIED"`**，`reviewedScope` 明写"仅审阅早退路径……注入路径按契约刻意不执行，仅做静态忠实度与可达性核查；build_case.ps1 与 pwsh 调用外壳未提供，相关结论标注为 undetermined"，**7 条全部登记**：
- 条目 1｜origin `conversion-introduced`｜`$args[0]` 与源 `argv[1]` 基数一致；缺参时源为 `strcmp(NULL,…)` 未定义而目标回退 `''`；risk low。
- 条目 2｜origin `environment`｜早退分支恰输出一次并以 `exit -1` 得 0xFFFFFFFF；残留不确定性在 `build_case.ps1` 中继层；risk low。
- 条目 3｜origin `source-preexisting`｜用 `[Console]::Out.Write` + 显式 `` `r`n ``，由 29 字节反推 CRLF；risk low。
- 条目 4｜origin `conversion-introduced`｜`Find-MyProc` 用 `[System.Diagnostics.Process]::GetProcesses()` + Ordinal 比较 `ProcessName + '.exe'`；列出三处非冻结路径差异（(a) `[int]$process.Id` 在 try 之外、(b) `Process` 未 `Dispose`、(c) `ProcessName+'.exe'` 属近似）；risk low。
- 条目 5｜origin `conversion-introduced`｜P/Invoke 签名/常量逐一对齐；**指出托管侧缓冲区 11 字节而 `nSize=13`，若该路径将来被执行会有 2 字节越界读**（源数组 12 字节并已有 1 字节越界读）；冻结 argv 不可达；risk low。
- 条目 6｜origin `conversion-introduced`｜无新增可观察行为；`Add-Type` 为机制新增；risk low（受限环境下 `Add-Type` 失败会污染 stderr，属 toolchain-unknown）。
- 条目 7｜origin `source-preexisting`｜静态可达性确认四条注入调用位于 `exit` 之后不可达；保留注入原语属源固有；risk low。
`self-review-1.model.json`：**调用元数据**（非原响应封装）——`stage SELF_REVIEWED`、`reviewN 1`、`model deepseek-flash`、`finishReason "stop"`、`requestSha256 4b22c609…6cf6`、`rawResponseSha256 f41f8253…48a5`、usage `2727/11307/8896/14034`、`maxTokensFieldSent false`、`verdict NO-REPAIR-IDENTIFIED`、`note "Static review only; not a compile or behavior conclusion."`。**无**第二轮自审（`selfRepairRounds 0`）；**无** `self-review-1.decision.json`。

**job 证据**：job-01 `eval-20261011-061409-2d2c7d14`：`input_profile.json`（`argv ["nosuchprocess"]`、`profileId "D2-091"`）、`comparison_manifest.json` 与 job-00b 同命令、`metadata.json`（`targetArtifact "target/target.ps1"`、`sourceHash 77713984…b42f`、`targetHash 0aa47eb2…2224`）、`batch-authorization.json`（`authorizedBy gyh-p1`、`authorizedAt/verifiedAt 2026-10-10T14:43:00Z`、`validUntil 2026-10-17T14:43:00Z`、`scope "所有非BLOCKED任务"`、`vmIsolation` 三字段全 true、`networkIsolation` 三字段全 true + 复用批次授权说明、`contractHash a9ed1445…d82e`）、`this-task-classification.json`（2 文件、ALLOWED）。
- 双侧原始观察（可见部分）：源 `build completed/0`/`durationMs 3180`（stderr 409 字节同 warning）、`execution completed/4294967295`/`durationMs 87`、`stdout.normalizedText "PID not found :( exiting...\n"`；目标 `build completed/0`/`durationMs 1188`、`execution completed/4294967295`/`durationMs 1829`、同一 `normalizedText`、`sizeBytes 29`、`digest sha256:b14a55beb9fd216d3863e508024ed697cf4a278589f0de1e8ffb4185c7dc6fed`。
- `comparison.json`：`behaviorVerdict "matched"`、`verdictReason "All applicable observed dimensions matched."`、`dimensions.output.status "matched"`（`applicable/observed true`、`diffs []`）、`filesystem/processes/registry/network` 全 `not-applicable`。
- `evaluation_report.json`（可见部分）：`jobStatus COMPLETED`/`jobPhase FINISHED`、`runVerdict "runnable"`、`codeVerdict "passed"`、`behaviorVerdict "matched"`、`evidenceCoverage{applicable 1, observed 1, matched 1, mismatched 0, inconclusive 0, sufficient 1, coverageRatio 1.0}`、`failure null`。`evaluation_report.md` 同；`controller-health-before.json` `checkedAt 06:14:08.754287Z`、`readyRunnerCount 3`、`blockingReasons []`；`controller-health-after.json` `checkedAt 06:15:26.927646Z`、`readyRunnerCount 3`、`blockingReasons []`；`controller.log` 2 行（06:14:09 created / 06:15:24 finished）。**无** `capsule.zip`、无 job 内 `source/`/`target/` 暂存树。
- job-00/job-00b：见「源预检」；两者的 `batch-authorization.json` **与 job-01 完全相同**（含 `dataSource.confirmation` 里那段 **D2-151** 文本"仅本地文件删除与只读遍历, 使用合成 fixture (keep.txt/second.txt)"）——本项实为进程枚举+注入 PoC、无文件删除（同 cases-01 B-07 型，本区间多个项沿用同一模板，见 §发现汇总条目 19 上方分类归入）。

**result / evaluator manifest**：`result.md`（52 行）按五栏骨架；§1 表：交付完整性"已完成"、语法/编译"通过"（两侧 `completed/0`）、功能一致性"约定范围内匹配"（job-01 `behaviorVerdict=matched`、`output` diffs=0）、安全"符合红线"（`processes` not-applicable ⇒ 未执行注入）；§3 如实记录 argv 重冻与"契约修正 `-fpermissive`；无自修、无评估后修复"；§4 登记三条覆盖缺口（找到进程后的注入路径按安全边界刻意不覆盖、`OpenProcess` 失败路径、自审提到的等价映射细节属静态复审）；§5 结论"无阻断未决项"。`evaluator_manifest.json`（70 行）：`schemaVersion 1`、`kind third-party-evaluator-manifest`、`generatedBy "code_convert-temporary-controller-adapter (hand-authored, not code-translator-mcp)"`、`languagePair{cpp,powershell}`、`taskMetadata{attackTactic none, sceneTags["process-execution"], windows/x64, riskLevel high, evidenceMode static-and-runtime, supportLevel experimental}`、`files[0]{relativePath target.ps1, success true, hasSource true, hasTranslatedCode true}`、`x_adapter{status "converted-and-evaluated", executionApproved true, jobId eval-20261011-061409-2d2c7d14, prerequisites[3], explorationOnly false, attackClassification{tactics[], techniques[], rationale "…processes 维度 not-applicable，未执行注入。"}}`。**与当前副本可检查性分开**：`hasTranslatedCode true` 指向的 `target.ps1` 已不在副本（B-20/B-21）。

**batch/items**：disposition `CONVERTED`、phase `CLOSED`、lifecycle `DONE`、`sourcePrecheck{jobId, os windows, buildCommand "g++ -std=gnu++17 -fpermissive process_enum.cpp -o program.exe", buildStatus completed, exitCode 0, verdict SOURCE_BUILDABLE, refreezeNote, observed "stdout 'PID not found :( exiting...+LF', exit code 4294967295"}`、`dualBuildJobId eval-20261011-061409-2d2c7d14`、`verdicts{sourceBuild completed/0, targetBuild "completed/0 (pwsh parser)", execution "both completed/4294967295; stdout byte-identical", comparison "matched (output, diffs=0)", environment clean, safety "ALLOWED; processes dimension not-applicable -> no injection performed"}`、`finalTargetSha256 0aa47eb2…2224`、`blockingReasons []`、`codeRevisions 1`、`selfRepairRounds 0`、`postEvalRepairRounds 0`、`coverageGap`（只覆盖 `argv=[nosuchprocess]`；注入路径按安全边界刻意不覆盖；`OpenProcess` 失败路径未覆盖；自审的等价映射细节仅静态复审）、`argvRefreezeNote`、`usage{promptTokens 4377, completionTokens 40733, reasoningTokens 36877, requests 2, model deepseek-flash, failedAttempts 0}`。

**独立证据事实与限制**：
- 原件支持：源 build `completed/0` + 精确 warning 文本；重冻后源 `execution completed/4294967295`、stdout `PID not found :( exiting...\n`；job-01 两侧同退出码同 stdout、目标 `sizeBytes 29`；两侧 cleanup PASSED、环境 clean、runner 回 READY；分类 ALLOWED（2 文件）。
- 历史说明：`result.md` 的"29 字节"表述属记录文本，其 CRLF 推断见下面待核验；`request.system.txt` 的"已实测行为契约"是提交前写入的声明。
- 当前规则对照：[任务状态 §2.1](../../../../../references/framework/task-state-contract.md) 第 37 行"冻结 → 实际请求"要求可回读源范围/契约/知识快照与模型参数——本项**因缺 frozen-inputs.md 而不可回读**（B-19）；[评估准备 §1.1](../../../../../references/framework/evaluation-readiness-contract.md) 第 31 行允许 source-only 预检，本项 job-00/00b 仍用占位目标（B-23）；B-21 的哈希链一致性是**正向**事实。
- 待核验：`evidence-source.json`/`evidence-target.json`/`evaluation_report.json` 2000 字符后的 `observations`/`artifacts`/清理字段不可读；`result.md` 与自审条目 3 认为源输出是 **CRLF（29 字节 = 27+2）**，而平台 `evidence-*.json` 的 `normalizedText` 显示为 `...exiting...\n`（单字节 `\n`），**LF/CRLF 之争在本副本不可定案**（正文已删；`normalizedText` 本身可能已归一化）；manifest 行 91 `Lines=69` 与 `result.md:14` 的"84 行"不一致（同 B-03 型）。
- 边界：本项 `matched` 仅覆盖 `output` 一个维度、且只覆盖 `argv=[nosuchprocess]` 的早退路径；`processes not-applicable` 说明未执行注入，但不证明注入代码正确；`DONE` 不含功能通过含义之外的范围扩张。

**分类归入**：已有规则落实（分类准入 §3 整树分类；评估准备 §4–5 覆盖边界如实用 `not-applicable`+`coverageGap` 登记；安全边界未删行为、未伪造输出；B-21 的哈希链一致性）；装置（B-19 缺 frozen、B-20 缺 model.json、B-23 占位目标、`batch-authorization` 数据源文本为 D2-151）；未定/待核（B-21 的生成轮原件缺失；LF/CRLF 字节义务不可定案；manifest `Lines` 不一致）；源已有（进程枚举＋远程线程注入 PoC 本身）；无知识新增。

### D2-092 / cpp-to-powershell / winhttp_impl.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-092-cpp-winhttp_impl.cpp`

**文件清单与读取状态**（49 件）：
- 01-frozen：`classifier-input.json`（已读，7 行）、`classification-1.json`（已读，98 行）。**无** `frozen-inputs.md`（B-19）。
- 02-conversion：`request.system.txt`（已读，20 行）、`repair.system.txt`（已读，16 行）。**无** `target.gen.*`、无 `.model.json`（B-20）。
- 03-self-review：`review.system.txt`（已读，12 行）、`self-review-1.json`（已读，69 行，7 条全登记）、`self-review-1.model.json`（已读，18 行）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`（各已读）；`returned-evidence/evidence-source.json`（**已读，截断**）、`evidence-target.json`（**已读，截断**）、`evaluation_report.json`（**已读，截断**）、`controller.log`（已读，2 行）。
- 04-evaluation/job-01-dual-build：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`、`controller-health-before.json`（各已读）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stdout`）、`evidence-target.json`（已读，可见至 `execution.stderr`）、`comparison.json`（已读）、`evaluation_report.json`（**已读，截断**）、`evaluation_report.md`（已读，83 行）、`controller-health-after.json`（已读）、`controller.log`（已读，2 行）。
- 04-evaluation/job-02-dual-build-eval-repair-1：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`、`controller-health-before.json`（各已读）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stdout`）、`evidence-target.json`（已读，可见至 `observations`）、`comparison.json`（已读）、`evaluation_report.json`（**已读，截断**）、`evaluation_report.md`（已读，77 行）、`controller-health-after.json`（已读）、`controller.log`（已读，2 行）。
- 根层：`result.md`（已读，57 行）、`evaluator_manifest.json`（已读，70 行）。**无** 根级 `target.ps1`。
- 另有 `batch/items/D2-092.json`（已读，69 行）。

**身份/版本关联**：taskId/rawItemId `D2-092`｜batchId `batch`｜direction `cpp-to-powershell`｜kind `NEW`｜disposition `CONVERTED`｜phase `CLOSED`｜lifecycle `DONE`｜pendingAction `null`｜sourceSha256 `b152f5a15225d16e065b114ee5d3b455fba6def11d74dd841b9a8b3b5c641b98`（manifest 行 92 大写、`classifier-input.json:5`、`classification-1.json:47`、三个 job `metadata.sourceHash` 一致）｜**finalTargetSha256 `4fb83b910de1dcd7dba0f632889a79d0246ca6e80357ae26758ba63c068ed581`**＝job-02 `metadata.targetHash`（B-22）｜classifier `v2.4`/`009a6f31…f3a4`/ALLOWED/null/`REVIEW_SENSITIVE`（`reviewGroups ["process","sensitive"]`；`run_case.py` `process` L13,21,48,59,63,64；`winhttp_impl.cpp` `sensitive` L82,85,88；`requiresSyntheticData true`；`inputManifestSha256 834f211ab76dd488b215fb78cf127f2f546fb4992a7e57887ea06a828dd726f1`）｜jobIds `eval-20261011-061653-0f813f5e`（job-00）、`eval-20261011-062151-7bd8dcf7`（job-01，失败轮）、`eval-20261011-062422-0f499436`（job-02，item `dualBuildJobId`）｜runner `windows-vm-agent-x64`、vmName `windows-eval`、snapshot `CC-Eval-Windows-8Lang-1.0.28`、agentVersion/collectorVersion `1.0.0`、contractSetHash `a9ed1445…d82e`｜model `deepseek-flash`、temperature 0.2（`result.md:38-40` 记 `-fpermissive`"按 §10.17"，历史编号）。**未记 selected skills 路径/哈希**。

**冻结/分类**：**`frozen-inputs.md` 缺件**（B-19）。`classifier-input.json` 单任务 1 文件（`source/winhttp_impl.cpp`）；`classification-1.json` `details.files` **2 项且顺序为 `run_case.py` 在前、`winhttp_impl.cpp` 在后**（同 B-04/B-05 型镜像错位），`limitations` 三条、`inputManifestSha256 834f211a…26f1`；三个 job 的 `this-task-classification.json` 与其一致。无 `classification-2/3`、无重分类 attempt。分类 `REVIEW_SENSITIVE` 的 `reviewGroups` 只列 `process`+`sensitive`（无 `dynamic_code`），而本项含明文 shellcode 与注入 API 绑定——按分类器自身 `limitations: lexical_heuristics_not_dataflow` 解释（词法启发，登记为分类器行为事实而非缺陷结论）。

**源预检**：job-00 `eval-20261011-061653-0f813f5e`，`input_profile.json` `argv ["nosuchpid"]`/`stdin null`/`timeout 30`/`dimensions ["output"]`/`normalized-text`＋`exact`/`profileId "D2-092"`；`comparison_manifest.json` source `g++ -std=gnu++17 -fpermissive winhttp_impl.cpp -o program.exe`、target `pwsh -NoProfile -File build_case.ps1`；`metadata.json` `networkBoundary "isolated VM"`、`targetArtifact "target/target.ps1 (placeholder)"`、`safetyClassification "classifier-2.4"`。真实结果（可见部分）：source `build completed/0`/`durationMs 3114`、build stdout/stderr 均空；source `execution completed/0`/`durationMs 73`、`stdout.normalizedText "PID: 0"`（`sizeBytes 6`、`digest sha256:5f0c82117dc1f773b874d7155578ac6c5a977d414257bb43111d21d757e23c5a`，**无换行**）；同 job 目标为占位（`"D2-092 placeholder\n"`）→ 平台 `mismatched`（B-23）。源基线：**取得**（非空 stdout + 退出码 0）。清理：源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`；目标亦 PASSED（占位被执行）。job-00 **无** health/runners 快照。

**模型请求/响应**：
- `request.system.txt`（20 行）：C++→PowerShell 转换器；硬性义务同 D2-091；适用规则含 `atoi(argv[1])`→`[int]` 转换（**不得抛异常**）、`printf("PID: %i", n)` 不追加换行（预期恰 6 字节 `PID: 0`）、五个注入 API 必须忠实映射但冻结 argv 下必然失败且**不得崩溃**、`return 0`→退出码 0；末段"已实测行为契约"：`target.ps1 nosuchpid` ⇒ stdout 恰 `PID: 0`（6 字节、无换行）、stderr 空、退出码 0。**无知识页正文**。
- `repair.system.txt`（16 行）：**评估后修复器**提示，含回传反例（job `eval-20261011-062151-7bd8dcf7`、`behaviorVerdict=mismatched`）的**两侧原文对照**（源 stderr 空；目标 stderr `The term printf_pid: is not recognized as a name of a cmdlet…` @ `target.ps1:107`）、定位与根因（"第 107 行是一条**悬空的标记行**，字面内容就是 `printf_pid:`"）、要求删除该行且不改动 stdout/退出码/其它逻辑。
- **`target.gen.model.json` 缺件**：生成轮 usage/哈希/finishReason 不可回读；`result.md:38-40` 记生成 `3088/16987/15311`、自审 `4445/19427/17395`、评估后修复 `2099/1672/0`；`item.usage` `promptTokens 9632`＝3088+4445+2099、`completionTokens 38086`＝16987+19427+1672、`reasoningTokens 32706`＝15311+17395+0（自洽，注意修复轮 `reasoning 0`）。**原响应正文**不可回读。

**失败/废弃/重提 attempt**：**有**——job-01 `eval-20261011-062151-7bd8dcf7` `behaviorVerdict "mismatched"`（real 目标稿），随后 1 轮评估后修复（`item.postEvalRepairRounds 1`、`repairChain` 3 条），job-02 取得 `matched`。job-01 原件全部保留、未覆盖（符合[评估准备 §5](../../../../../references/framework/evaluation-readiness-contract.md) 第 103 行）。无 `attempt-*-403.json`、无废弃 job。`item.failedAttempts 0`。

**自审**：`review.system.txt`（12 行）同样要求裸 JSON + 7 条核对项（argv 基数、`atoi` 语义、无换行输出、注入 API 且不产生效果、是否新增行为如未捕获异常改变退出码、退出码 0、安全）。`self-review-1.json` **`verdict "REPAIR-RECOMMENDED"`**、`reviewedScope` 明写"静态审阅（未实际运行 pwsh，也未执行 build_case.ps1）"，**7 条全部登记**：
- 条目 1｜`conversion-introduced`｜`$args[0]` 映射正确；残留差异为源 `argc<2` 时 `atoi(NULL)` UB（实测崩溃）而目标回退空串得 0；risk 低。
- 条目 2｜`conversion-introduced`｜`ConvertFrom-AtOi` 正则跳过前导空白/符号，`nosuchpid` 无匹配返回 0、不抛异常；溢出边界差异；risk 低。
- 条目 3｜`conversion-introduced`｜`[Console]::Out.Write("PID: {0}", …)` 输出 `PID: 0` 6 字节；**但指出紧随其后的 `printf_pid:` 会报错中断，使 stderr 非空且退出码非 0**；risk 中。
- 条目 4｜`conversion-introduced`｜五个调用点常量/参数形状核对无误、冻结 argv 下无副作用；列出"源 `my_payload[]` 的 `sizeof` 含隐含 NUL 而目标 `$my_payload.Length` 缺 `0x00` 尾字节"（495 vs 496）；risk 冻结下低、脱离冻结中；另注 `Add-Type` 依赖可编译 C#（toolchain-unknown）。
- 条目 5｜`conversion-introduced`｜**`printf_pid:` 为转换残留**，指出 `printf_pid:` 不是合法标签、会被当作命令名产生 `CommandNotFoundException`（终止性错误、`pwsh -File` 返回 1），`proposed_fix "删除整行 printf_pid:"`、`risk "高：确定性的行为偏差，且是本次转换唯一实质缺陷"`。
- 条目 6｜`conversion-introduced`｜`exit 0` 正确但受条目 5 阻断；`proposed_fix` 同条目 5；risk 高。
- 条目 7｜`source-preexisting`｜冻结 argv 下确无注入效果；残留风险为文件完整保留明文 shellcode 与注入 API；risk 冻结下低、真实 PID 时高。
`self-review-1.model.json`：**调用元数据**——`requestSha256 4dcd3495…a6ff`、`rawResponseSha256 256ed34d…a1e9`、usage `4445/19427/17395/23872`、`maxTokensFieldSent false`、`verdict "REPAIR-RECOMMENDED"`。无第二轮自审（`selfRepairRounds 0`）；无 `decision.json`。**该 `REPAIR-RECOMMENDED` 未被当作提交前阻断**（B-24）。

**job 证据**：
- **job-01（失败轮）** `eval-20261011-062151-7bd8dcf7`：`metadata.json` `targetArtifact "target/target.ps1"`、`targetHash "sha256:2c6a07c3ce94c1c429b624843437e057c2fc39a68041e2d3a6541e5f1c86381c"`。`evidence-target.json` `execution.status completed`/`exitCode 0`/`durationMs 1464`、`stdout.normalizedText "PID: 0"`（6 字节、同一 digest）、`stderr.normalizedText` 含 ANSI 转义 `printf_pid:: …C:\CodeConvertRemote\Stack\Agent\workspaces\eval-20261011-062151-7bd8dcf7\target\target.ps1:107`——**该 stderr 文本内含 Controller 工作区绝对路径**，登记为原文事实（本审阅不访问该目录）。`comparison.json` `behaviorVerdict "mismatched"`、`dimensions.output.status "mismatched"`、`diffs[{path "stream.digest", kind "changed", criticality "major", sourceValueSummary "sha256:e3b0c44298fc1", targetValueSummary "sha256:c3e8217719b9c", rule "exact-digest", evidenceRefs ["stream/digest"]}]`。`evaluation_report.json` `runVerdict "partial-runnable"`/`codeVerdict "failed"`/`behaviorVerdict "mismatched"`/`mismatchedDimensions 1`/`coverageRatio 1.0`、两侧 cleanup PASSED、`runnerStateAfter READY`；`evaluation_report.md` FAIL/MISMATCHED/CLEAN；`controller-health-before.json` `checkedAt 06:21:50.535439Z`、3/3 runner、`blockingReasons []`；`controller-health-after.json` `checkedAt 06:23:08.721019Z`；`controller.log` 2 行（06:21:51 / 06:23:05）。
- **job-02（修复后）** `eval-20261011-062422-0f499436`：`metadata.json` `targetArtifact "target/target.ps1 (eval-repair-1)"`、`targetHash "sha256:4fb83b91…d581"`（＝item `finalTargetSha256`）。双侧：源 `build completed/0`/`durationMs 3408`、`execution completed/0`/`durationMs 83`、`stdout "PID: 0"`（6 字节、同 digest）；目标 `build completed/0`/`durationMs 1176`（`pwsh` 语法检查）、`execution completed/0`/`durationMs 1299`、`stdout "PID: 0"`（6 字节、同 digest、`stderr` 空）。`comparison.json` `behaviorVerdict "matched"`、`dimensions.output.status "matched"`（`diffs []`）、其余四维 `not-applicable`。`evaluation_report.json` `runVerdict "runnable"`/`codeVerdict "passed"`/`behaviorVerdict "matched"`/`coverageRatio 1.0`/`failure null`；`evaluation_report.md` PASS/MATCHED/CLEAN/覆盖 1-1-1-0-0 100%；health-before/after 均 3/3 runner、`blockingReasons []`；`controller.log` 2 行（06:24:22 / 06:25:39）。
- 三个 job 的 `batch-authorization.json` 内容相同（`gyh-p1`、同一 `validUntil`、六字段全 true、`contractHash a9ed1445…d82e`），`dataSource.confirmation` 同为 **D2-151** 文本。**无** `capsule.zip`、无暂存树。
- job-00：见「源预检」；平台 `mismatched` 系占位产物（B-23）。

**result / evaluator manifest**：`result.md`（57 行）五栏齐备；§3 以表格记 job-01 `mismatched` → 修复 → job-02 `matched`，并记"契约修正：`-fpermissive`（C 风格隐式转换，**按 §10.17**）"；§4 记覆盖缺口（真实 PID 下注入路径按安全边界刻意不覆盖、`argv[1]` 缺省/空串路径），并声明"失败轮留档：job-01 的 `mismatched` 与其原始 stderr 原样保留"。`evaluator_manifest.json`（70 行）结构同 D2-091，`jobId eval-20261011-062422-0f499436`、`plannedReportPath` 指向 job-02 的 `evaluation_report.md`、`prerequisites[3]` 明列"job-01 mismatched（悬空 'printf_pid:' 于 target.ps1:107 → stderr）→ 评估后修复 1 轮 → job-02 matched"；`attackClassification.rationale` 记冻结 argv 下 `OpenProcess` 失败、`processes` not-applicable。**与副本可检查性分开**：`translatedCodePath` 指向的 `target.ps1` 已不在副本。

**batch/items**：disposition `CONVERTED`、phase `CLOSED`、lifecycle `DONE`、`sourcePrecheck{jobId eval-20261011-061653-0f813f5e, os windows, buildCommand "g++ -std=gnu++17 -fpermissive winhttp_impl.cpp -o program.exe", completed, exitCode 0, SOURCE_BUILDABLE, note "execution completed/0, stdout 'PID: 0' (no newline)"}`、`dualBuildJobId eval-20261011-062422-0f499436`、`verdicts{sourceBuild completed/0, targetBuild "completed/0 (pwsh parser)", execution "both completed/0; stdout byte-identical; stderr empty; processes not-applicable", comparison "matched (output, diffs=0)", environment clean, safety "ALLOWED; no injection performed"}`、`finalTargetSha256 4fb83b91…d581`、`codeRevisions 2`、`selfRepairRounds 0`、`postEvalRepairRounds 1`、`repairChain` 3 条（job-01 mismatched → eval-repair-1"model-authored minimal patch: delete the stray dangling token line 107 (single-line diff)" → job-02 matched）、`coverageGap`、`usage{promptTokens 9632, completionTokens 38086, reasoningTokens 32706, requests 3, model deepseek-flash, failedAttempts 0}`。

**独立证据事实与限制**：
- 原件支持：job-01 目标 `stderr` 原文（含 `target.ps1:107` 与 `printf_pid:`）、`comparison.json` 的 `stream.digest` 差异；job-02 两侧 `PID: 0` 6 字节同 digest、stderr 双空、退出码 0；三个 job 的双侧 cleanup PASSED/环境 clean/READY；分类 ALLOWED（2 文件）。
- 历史说明：`request.system.txt`/`repair.system.txt` 是提交前写入的声明与反馈；`result.md` 的分轮叙述；`repairChain` 的"single-line diff"是记录文本（diff 正文不在副本）。
- 当前规则对照：[闭环 §3.1](../../../../../references/workflow/conversion-evaluation-loop.md) 第 92 行"第三方提供有效执行/比较反例，差异超出已接受范围，且源/目标证据能定位转换引入的行为问题 → `behavior` 修复"——本项属该分支且**已按证据定位**（`target.ps1:107`），与 B-24 的"提交前未处理自审阻断项"是不同环节；[评估准备 §5](../../../../../references/framework/evaluation-readiness-contract.md) 第 103 行原判保留执行到位。
- 待核验：`evidence-*.json`/`evaluation_report.json` 2000 字符后字段不可读；`result.md:32` 的"§10.17"在现行 `references/` 与 `AGENTS.md` 中未核到（历史编号）；`repairChain` 的 `round "eval-repair-1"` 与目录名 `job-02-dual-build-eval-repair-1` 的编号语义需并读（目录按 job 递增、`round` 按修复轮次）。**另**：job-01 目标 `stderr` 内含 Controller 工作区绝对路径（`C:\CodeConvertRemote\Stack\Agent\workspaces\...`），属第三方回传原文，本审阅只读文本、未访问该路径（安全边界 §1）。
- 边界：`matched` 只覆盖 `output`；注入路径与缺参路径未覆盖；`DONE` 不含未覆盖维度的通过含义。

**分类归入**：已有规则落实（闭环 §3.1 behavior 修复分支与 §3.2 重评；评估准备 §5 原判保留；分类准入 §3 整树分类）；装置（B-19/B-20/B-23；B-27 型的 `batch-authorization` D2-151 文本；分类 `reviewGroups` 未含 `dynamic_code`）；未定/待核（B-24 的内部预检放行差异；历史编号 §10.17）；源已有（远程线程注入 PoC 与明文 shellcode）；无知识新增。

### D2-093 / cpp-to-powershell / inject_channel.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-093-cpp-inject_channel.cpp`

**文件清单与读取状态**（53 件）：
- 01-frozen：`classifier-input.json`（已读，7 行）、`classification-1.json`（已读，103 行）。**无** `frozen-inputs.md`（B-19）。
- 02-conversion：`request.system.txt`（已读，24 行）、`repair.system.txt`（已读，19 行）、`repair2.system.txt`（已读，16 行）。**无** `target.gen.*`、无 `.model.json`（B-20）。
- 03-self-review：`review.system.txt`（已读，12 行）、`self-review-1.json`（已读，40 行，7 条仅 `id`/`origin`/`issue`）、`self-review-1.model.json`（已读，19 行，含 `parseNote`）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`（各已读）；`returned-evidence/evidence-source.json`（**已读，截断**）、`evidence-target.json`（**已读，截断**）、`evaluation_report.json`（**已读，截断**）、`controller.log`（已读，2 行）。
- 04-evaluation/job-01-dual-build：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`、`controller-health-before.json`（各已读）；`returned-evidence/evidence-source.json`（**已读，截断**）、`evidence-target.json`（已读，可见至 `execution.stderr`）、`comparison.json`（已读）、`evaluation_report.json`（**已读，截断**）、`evaluation_report.md`（已读，83 行）、`controller-health-after.json`（已读）、`controller.log`（已读，2 行）。
- 04-evaluation/job-02-dual-build-eval-repair-2：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`、`controller-health-before.json`（各已读）；`returned-evidence/evidence-source.json`（**已读，截断**）、`evidence-target.json`（已读，可见至 `observations`）、`comparison.json`（已读）、`evaluation_report.json`（**已读，截断**）、`evaluation_report.md`（已读，77 行）、`controller-health-after.json`（已读）、`controller.log`（已读，2 行）。
- 根层：`result.md`（已读，61 行）、`evaluator_manifest.json`（已读，70 行）。**无** 根级 `target.ps1`。
- 另有 `batch/items/D2-093.json`（已读，77 行）。

**身份/版本关联**：taskId/rawItemId `D2-093`｜batchId `batch`｜direction `cpp-to-powershell`｜kind `NEW`｜disposition `CONVERTED`｜phase `CLOSED`｜lifecycle `DONE`｜pendingAction `null`｜sourceSha256 `02d49a0a056384d20c226d5cc5037a8c1071462b306cc9ad622d44f98877a8dc`（manifest 行 93 大写、`classifier-input.json:5`、`classification-1.json:17`、三个 job `metadata.sourceHash` 一致）｜**finalTargetSha256 `5695e7c551bd1b90fcb267e4e22e60fbef95e09d46c0fefc276dba066be326d8`**＝job-02 `metadata.targetHash`（B-22）｜classifier `v2.4`/`009a6f31…f3a4`/ALLOWED/null/`REVIEW_SENSITIVE`（`reviewGroups ["process","sensitive"]`；`inject_channel.cpp` `process` L77,83、`sensitive` L42,55,94,97,100；`run_case.py` `process` L13,21,48,59,63,64；`requiresSyntheticData true`；`inputManifestSha256 4d9242cc83aec91ea6e8f929761abf70f00229b8b9d41b640bc4a5235b8f59f2`）｜jobIds `eval-20261011-062941-a2416a39`（job-00）、`eval-20261011-063518-76bfc0cd`（job-01 失败轮）、`eval-20261011-063947-35791b47`（job-02，item `dualBuildJobId`）｜runner `windows-vm-agent-x64`、vmName `windows-eval`、snapshot `CC-Eval-Windows-8Lang-1.0.28`、agentVersion/collectorVersion `1.0.0`、contractSetHash `a9ed1445…d82e`｜model `deepseek-flash`（`result.md:33` 记 `-fpermissive`"按 §10.17"）。**未记 selected skills 路径/哈希**。

**冻结/分类**：**`frozen-inputs.md` 缺件**（B-19）。`classifier-input.json` 单任务 1 文件；`classification-1.json` `details.files` **2 项**（顺序 `inject_channel.cpp` 在前、`run_case.py` 在后）、`limitations` 三条、`inputManifestSha256 4d9242cc…59f2`；job-00/01/02 的 `this-task-classification.json` 与之一致。无 `classification-2/3`、无重分类 attempt。分类 `reviewGroups` **不含 `dynamic_code`**，而源含 shellcode 十六进制与注入 API——按 `lexical_heuristics_not_dataflow` 解释（登记为分类器行为事实）。

**源预检**：job-00 `eval-20261011-062941-a2416a39`，`input_profile.json` `argv ["nosuchpid"]`/`stdin null`/`timeout 30`/`dimensions ["output"]`/`normalized-text`＋`exact`/`profileId "D2-093"`；`comparison_manifest.json` source `g++ -std=gnu++17 -fpermissive inject_channel.cpp -o program.exe -ladvapi32`、target `pwsh -NoProfile -File build_case.ps1`；`metadata.json` `networkBoundary "isolated VM"`、`targetArtifact "target/target.ps1 (placeholder)"`、`safetyClassification "classifier-2.4"`。真实结果（可见部分）：source `build completed/0`/`durationMs 4183`、build stderr 含三条 `ISO C++ forbids converting a string constant to 'char*' [-Wwrite-strings]`（L72/77/78，注册表路径字符串）；source `execution completed/0`；同 job 目标为占位（`"D2-093 placeholder\n"`）→ 平台 `mismatched`（B-23）。清理：源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`；目标亦 PASSED。job-00 **无** health/runners 快照。

**模型请求/响应**：
- `request.system.txt`（24 行）：C++→PowerShell；硬性义务同上；**关键语义**逐条给出 VM 检测三段（`reg_key_ex(HKLM,"HARDWARE\ACPI\FADT\VBOX__")` 与 `HKLM\SYSTEM\CurrentControlSet\Control\SystemInformation` 的 `SystemProductName`/`BiosVersion` 是否等于 `VirtualBox`）命中即打印对应文案并 `return -2`（退出码 0xFFFFFFFE）、须用 `Get-ItemProperty` 等价实现且**不得硬编码 false/true**；`printf("PID: %i", atoi(argv[1]))` 不追加换行；`argv[1]→$args[0]`；五个注入 API 冻结下必然失败但仍须走到 `return 0`；末段声明"本 runner 的注册表**不含** VirtualBox 特征，故 VM 检测三段均不命中"。
- `repair.system.txt`（19 行）：第一轮评估后修复；含回传反例原文（`target.ps1:54` `$bytes[$i] = [Convert]::ToByte($hex.Substring($i * 2, 2), 16)` 抛 `MethodInvocationException`）；给出**量化**事实"here-string 正文去掉空白后只有 **625 个十六进制位（奇数）**，拼接 `00` 后为 **627 位**……源的 `my_payload[]` 共 **313 字节（= 626 个十六进制位）**，其最后一个字节就是 `00`"；要求修正为恰 313 字节/626 位。
- `repair2.system.txt`（16 行）：第二轮修复；明写"上一轮修复仍未解决根因"，给出逐位对照（源 `…e8d00000` `0041` `514150525156…` vs 目标 `…e8d00000` `0415` `141505251564…`）、定位"目标在 `e8d00000` 之后**少写了一个 `0`**"、要求补回该 `0` 且不得再额外 `+ 00`。
- **`target.gen.model.json` 缺件**：生成轮 usage/哈希不可回读；`result.md:37-42` 记生成 `2488/21168/19531`、自审 `3650/13755/11775`、修复 1 `3763/10043/8410`、修复 2 `3602/6732/5099`；`item.usage` `promptTokens 13503`＝2488+3650+3763+3602、`completionTokens 51698`＝21168+13755+10043+6732、`reasoningTokens 44815`＝19531+11775+8410+5099（自洽）。**原响应正文**不可回读。

**失败/废弃/重提 attempt**：**有**——job-01 mismatched → 评估后修复 1（**未收敛**）→ 评估后修复 2（收敛）→ job-02 matched；`item.postEvalRepairRounds 2`、`usage.postEvalRepairBudget "2/2 used"`（[闭环 §2](../../../../../references/workflow/conversion-evaluation-loop.md) 第 51 行默认评估后总上限 2 轮，**已用满**）。三个 job 目录并存、原件未覆盖。无 `attempt-*-403.json`、无废弃 job。`item.failedAttempts 0`。

**自审**：`review.system.txt`（12 行）含 7 条核对项（VM 检测三段真实性/文案/`exit -2`、`atoi`、argv 基数、无换行输出、注入 API 不可达、是否新增行为、退出码 0 与**悬空标记**）。`self-review-1.json` **`verdict "NO-REPAIR-IDENTIFIED"`**、**无 `reviewedScope` 字段**，**7 条只有 `id`/`origin`/`issue`**：
- 条目 1｜`conversion-introduced`｜非硬编码、命中语义与退出码等价；残留差异为注册表视图（源若 32 位会重定向到 `WOW6432Node`、`Test-Path` 不校验 `KEY_READ`、`Get-ItemProperty` 对非字符串返回 `$false`）；冻结下不可观察。
- 条目 2｜`conversion-introduced`｜`atoi` 语义符合"前导数字否则 0 不抛异常"；次要加宽 `[char]::IsWhiteSpace` 比 `isspace` 多识别 Unicode 空白、大数溢出升 `double`；冻结不触发。
- 条目 3｜`conversion-introduced`｜基数映射正确，无 off-by-one。
- 条目 4｜`conversion-introduced`｜逐字节等价、无 CR/LF、无 BOM。
- 条目 5｜`conversion-introduced`｜映射忠实且未被执行出效果；`$rt` 未使用但不产生告警/stderr。
- 条目 6｜`conversion-introduced`｜未发现新增可观察行为；`Add-Type` 需宿主编译器，失败会污染 stderr（工具链）。
- 条目 7｜`conversion-introduced`｜"退出码 0、无悬空标记、无误导译行导致 stderr 非空"——**该条与后续事实不符**：job-01 的 stderr 非空且根因是 payload hex 丢位（B-26）。
`self-review-1.model.json`：**调用元数据**——`requestSha256 fd8bfa9c…cf2e`、`rawResponseSha256 8acfb466…3cbd`、usage `3650/13755/11775/17405`、`maxTokensFieldSent false`、`verdict NO-REPAIR-IDENTIFIED`、`parseNote "response body is malformed JSON (unescaped quote / control character ~char 1581); per batch discipline 2 the verdict and items were recovered by regex and the RAW response is preserved unchanged; model-output formatting defect, not a scheduling error"`。无第二轮自审（`selfRepairRounds 0`）；无 `decision.json`。

**job 证据**：
- **job-01（失败轮）** `eval-20261011-063518-76bfc0cd`：`metadata.json` `targetArtifact "target/target.ps1"`、`targetHash "sha256:e75a403b3fb0e5b5ebcd3288f1ab70ace71a3552f6202ce563387c651164d70b"`。`evidence-target.json` `execution.status completed`/`exitCode 0`/`durationMs 1942`、`stdout.normalizedText "PID: 0"`（6 字节、同 digest）、`stderr.normalizedText` 含 ANSI 转义 `MethodInvocationException: …C:\CodeConvertRemote\Stack\Agent\workspaces\eval-20261011-063518-76bfc0cd\target\target.ps1:54`。`comparison.json` `behaviorVerdict "mismatched"`、`dimensions.output.status "mismatched"`、`diffs[{path "stream.digest", kind "changed", criticality "major", sourceValueSummary "sha256:e3b0c44298fc1", targetValueSummary "sha256:36d9197b39bfd", rule "exact-digest"}]`。`evaluation_report.json` `partial-runnable`/`failed`/`mismatched`/`coverageRatio 1.0`、两侧 cleanup PASSED；`evaluation_report.md` FAIL/MISMATCHED/CLEAN；health-before `checkedAt 06:35:18.252861Z` 3/3、after `06:36:36.405449Z`；`controller.log` 2 行（06:35:18 / 06:36:36）。
- **job-02（修复后）** `eval-20261011-063947-35791b47`：`metadata.json` `targetArtifact "target/target.ps1 (eval-repair-2)"`、`targetHash "sha256:5695e7c5…26d8"`（＝item `finalTargetSha256`）。源 `build completed/0`/`durationMs 4647`（同三条 `-Wwrite-strings` warning）、`execution completed/0`、`stdout "PID: 0"`（6 字节、同 digest）；目标 `build completed/0`/`durationMs 1181`（`pwsh` 语法检查）、`execution completed/0`/`durationMs 1356`、`stdout "PID: 0"`（6 字节、同 digest）、`stderr` 空。`comparison.json` `behaviorVerdict "matched"`、`dimensions.output.status "matched"`（`diffs []`）、其余四维 `not-applicable`。`evaluation_report.json` `runnable`/`passed`/`matched`/`coverageRatio 1.0`/`failure null`；`evaluation_report.md` PASS/MATCHED/CLEAN/1-1-1-0-0；health-before `06:39:46.590905Z`、after `06:41:05.008852Z`、均 3/3；`controller.log` 2 行（06:39:47 / 06:41:04）。
- 三个 job 的 `batch-authorization.json` 内容相同（含 **D2-151** 的 `dataSource.confirmation`）。**无** `capsule.zip`、无暂存树。
- job-00：见「源预检」；平台 `mismatched` 系占位产物（B-23）。

**result / evaluator manifest**：`result.md`（61 行）五栏齐备；§3 表列 job-01 `mismatched` → 修复 1（未收敛，"模型只删掉多余的 `+ '00'`，hex 仍 625 位"）→ 修复 2（"精确定位到具体位：目标在 `e8d00000` 之后**少一个 `0`**……修复后 hex **626 位、与源逐字节相同**"）→ job-02 `matched`，并附**调度附注**（自审响应 JSON 损坏、按批次纪律 §2 正则恢复并原样保留）；§4 记"修复证据：评估后修复 2 版与源 payload 的 hex 逐字节相同（626 位）"与三条覆盖缺口（真实 PID 注入路径、VM 检测命中的三个分支"**本 runner 非 VirtualBox，属环境事实**"、`argv[1]` 缺省路径）；§5 记"评估后修复预算（2 轮）已用满；最终版已 matched"。`evaluator_manifest.json`（70 行）结构同前，`jobId eval-20261011-063947-35791b47`、`prerequisites[3]` 明列"job-01 mismatched (payload hex 625 digits -> Substring out of range) -> 2 eval-repairs -> job-02 matched"、`attackClassification.rationale` 记冻结 argv 下检测不命中且 `OpenProcess` 失败、`processes/registry` not-applicable。**与副本可检查性分开**：`translatedCodePath` 指向的 `target.ps1` 已不在副本。

**batch/items**：disposition `CONVERTED`、phase `CLOSED`、lifecycle `DONE`、`sourcePrecheck{jobId eval-20261011-062941-a2416a39, os windows, buildCommand "g++ -std=gnu++17 -fpermissive inject_channel.cpp -o program.exe -ladvapi32", completed, exitCode 0, SOURCE_BUILDABLE, note "execution completed/0, stdout 'PID: 0'; VM detection does not trigger on this runner"}`、`dualBuildJobId eval-20261011-063947-35791b47`、`verdicts{sourceBuild completed/0, targetBuild "completed/0 (pwsh parser)", execution "both completed/0; stdout byte-identical 'PID: 0'; stderr empty; processes+registry not-applicable", comparison "matched (output, diffs=0)", environment clean, safety "ALLOWED; no injection, no registry write"}`、`finalTargetSha256 5695e7c5…26d8`、`codeRevisions 3`、`selfRepairRounds 0`、`postEvalRepairRounds 2`、`repairChain` 4 条（job-01 mismatched → eval-repair-1"did not converge…model removed the extra 00 suffix but the hex stayed 625 digits (odd)" → eval-repair-2"converged…pinpointed a single missing 0 after e8d00000 (hex-index 24); payload now 626 hex digits = 313 bytes, byte-identical to the source" → job-02 matched）、`coverageGap`（只覆盖 `argv=[nosuchpid]`；真实 PID 注入路径与三个 VM 检测分支未覆盖；`argv[1]` 缺省未覆盖）、`schedulingNote`（自审响应正文 JSON 损坏、正则恢复、原响应保留）、`usage{promptTokens 13503, completionTokens 51698, reasoningTokens 44815, requests 4, model deepseek-flash, failedAttempts 0, postEvalRepairBudget "2/2 used"}`。

**独立证据事实与限制**：
- 原件支持：job-01 目标 `stderr` 原文（`target.ps1:54` 的 `Substring` 越界）；`repair.system.txt` 对"625 奇数位 vs 源 626 位"的量化；`repair2.system.txt` 的逐位对照；job-02 两侧 `PID: 0` 6 字节同 digest、stderr 双空、退出码 0；三个 job 双侧 cleanup PASSED/环境 clean/READY；分类 ALLOWED（2 文件）。
- 历史说明：`request.system.txt`/两份 repair 提示是提交前写入；`result.md` 的"hex 逐字节相同（626 位）"是交付方对修复结果的陈述——**目标稿正文已删，该声明不能由本副本独立复核**（只能由 job-02 `matched` 间接支持）。
- 当前规则对照：[闭环 §2 评估后修复预算](../../../../../references/workflow/conversion-evaluation-loop.md) 第 51 行（默认总上限 2 轮，本项用满且有进展，未越界）；§3.1 第 92 行 behavior 分支；§4.1 第 134 行"损坏 JSON 只提取 verdict 不能证明审阅范围/条目完整"（B-26/B-28 的依据）。
- 待核验：`evidence-*.json`/`evaluation_report.json` 2000 字符后字段不可读；`result.md:33` 的"§10.17"为历史编号；VM 检测三段的**真实注册表读取**只在静态自审中核对，未取行为证据（`registry` 维度 `not-applicable`）。**另**：job-01 目标 `stderr` 含 Controller 工作区绝对路径，属第三方回传原文，本审阅未访问该路径。
- 边界：`matched` 只覆盖 `output`；`registry not-applicable` 不证明注册表读取等价，只说明本 runner 的注册表未触发三段检测；"626 位与源逐字节相同"是**目标 payload 与源 payload**的一致性陈述，不是两侧运行观察。

**分类归入**：已有规则落实（闭环 §2 预算与 §3.1/§3.2 轮次关联；评估准备 §5 原判保留；交付 §2.3 分层报告与覆盖缺口登记）；装置（B-19/B-20/B-22/B-23/B-28；`batch-authorization` D2-151 文本；`reviewGroups` 未含 `dynamic_code`）；未定/待核（B-26 自审覆盖边界；历史编号 §10.17；payload hex 修复只能间接复核）；环境（本 runner 非 VirtualBox，三段检测结构性不覆盖）；源已有（VM 检测＋远程线程注入 PoC）；无知识新增。

### D2-094 / cpp-to-powershell / screenshot.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-094-cpp-screenshot.cpp`

**文件清单与读取状态**（1 件）：
- 01-frozen：`frozen-inputs.md`（已读，27 行）。**无** `classifier-input.json`、**无** `classification-*.json`（item 记 `NOT_TAKEN`，见下）。
- 02-conversion / 03-self-review / 04-evaluation：**目录均不存在**（0 模型调用、未提交；无空目录）。
- 根层：**无** `result.md`、无 `evaluator_manifest.json`、无 `target.*`。
- 另有 `batch/items/D2-094.json`（已读，44 行）。

**身份/版本关联**：taskId/rawItemId `D2-094`｜batchId `batch`｜direction `cpp-to-powershell`｜kind `NEW`｜disposition `FROZEN`｜phase `EVALUATION_NOT_READY`｜lifecycle `PARTIAL`｜pendingAction "freeze a device that observes safely without triggering the CreateProcess+APC-injection side effect (non-PID observable)"｜sourceSha256 `90fe4aad16c74dd07f2188f4ac181ec40fe4cf6b13c7085f5e3ae2337a67fda1`（`items/D2-094.json:12`、`frozen-inputs.md:8`；manifest 行 94 大写）｜finalTargetSha256 无｜classifier `version "2.4"`/`admissionStatus "NOT_TAKEN"`/`blockingReason null`/`cls null`/`sha256 null`，`note "not classified: the item is not submitted"`｜jobId 无、runner/vmName/snapshot/model 均无（未提交）｜`frozen-inputs.md` 记 batchId/taskId/direction/Kind、sourcePath `.../source/screenshot.cpp`、`sourceLines: 99`、sourceOs windows。

**冻结/分类**：`frozen-inputs.md`（27 行）要点：形态＝**进程创建 + APC 注入** PoC（`findMyProc(argv[1])` → `CreateProcessA(mspaint.exe, …, CREATE_SUSPENDED|CREATE_NO_WINDOW|EXTENDED_STARTUPINFO_PRESENT)` → `VirtualAllocEx` → `WriteProcessMemory` → `QueueUserAPC` → `ResumeThread`）；评估就绪核对**两条独立理由**——（一）无可用 oracle：只有找到进程时才 `printf("PID = %d\n", pid)`、找不到时无任何输出；找到时打印**动态 PID**（"两次执行/VN 都不同，**不在消噪记号覆盖内**（§10.16）"）；(二) 无论是否找到目标进程，`main` 都会继续 `CreateProcessA(mspaint.exe…)` 并注入，"即在'观察不到任何东西'的前提下，仍会创建进程并向其注入执行"，据[安全边界](../../../../../references/framework/safety-boundary.md)（相对路径从 `01-frozen/` 上溯 6 级，**解析正确**）"逐例核对源码存在性、代码实际行为、危险副作用、目标环境与可观察 oracle"判**副作用与所得证据不相称，故不提交**（不跑源侧预检、不进生成）；处置记 disposition `FROZEN`/phase `EVALUATION_NOT_READY`/lifecycle `PARTIAL`/`blockingReasons ["ORACLE_NOT_FREEZABLE","RUN_SIDE_EFFECT_UNJUSTIFIED"]`/"**0 模型调用**；**未提交任何 capsule**；源侧构建结论记 **UNVERIFIED**（未跑）"；恢复条件＝"出现既能安全观察、又能避免注入副作用的装置后再评估 —— 属新冻结条件"。**无分类输入/结果件**，故"冻结→分类"这一步没有任何可回读的机器件支撑（只有本 Markdown）。

**源预检**：**无**（未提交、未跑；item `verdicts.sourceBuild "UNVERIFIED (not run; not submitted)"`）。无 `job-*` 目录、无 metadata/input_profile/comparison_manifest/evidence/清理依据——属"未发生"，非缺档。**注意**：`frozen-inputs.md:26` 明写"源侧构建结论记 UNVERIFIED（未跑）"，即**连源可构建性都没有诊断**；现行[根 SKILL.md](../../../../../SKILL.md) 第 25 行要求"源侧预检先取得 build.status=completed 且 exitCode=0……本轮无法合法评估行为但源可构建时，按 §1.3 记 LIB_UNOBSERVABLE_COMPILE_ONLY，继续转换、自审并验证目标语法/编译，**不因缺 main、可执行文件、stdout 或合法入口直接跳过**"。

**模型请求/响应**：无（0 调用）。**失败/废弃/重提 attempt**：无。**自审**：无。

**job 证据**：无（无任何 job 目录、无 health/runners、无 comparison、无清理记录）。

**result / evaluator manifest**：均**缺件**且 frozen 未声明不产（与 D2-089/090 的"明示不产"不同）。按[交付契约 §1.1](../../../../../references/framework/delivery-handoff-contract.md) 第 15 行，分类阻断、源预检失败/缺基线、评估准备缺口、仅编译、跳过及 WAITING 暂停**均须走统一收尾并写 result.md**；§2.1.1 第 108 行"非可转换去向……result.md（去向/原因、实际阶段与证据、适用件核对）……**result.md 不豁免**"。本项属 `EVALUATION_NOT_READY`（准备缺口）＋`PARTIAL`，**缺 result.md 属交付缺档**。

**batch/items**：disposition `FROZEN`、phase `EVALUATION_NOT_READY`、lifecycle `PARTIAL`、`blockingReasons ["ORACLE_NOT_FREEZABLE","RUN_SIDE_EFFECT_UNJUSTIFIED"]`、`evaluationReadiness{verdict "EVALUATION_NOT_READY", detail "(a) no non-degenerate, reproducible observable… (b) the program unconditionally launches mspaint.exe and APC-injects into it, so submitting would create a process and inject into it while yielding no behavioural evidence. Per the safety boundary the side effect is not justified by the evidence it could produce -> not submitted; source build unverified.", ruleRef "safety-boundary: per-item review of actual behaviour, dangerous side effects, target environment and observable oracle"}`、`verdicts{sourceBuild "UNVERIFIED (not run; not submitted)", targetBuild "UNVERIFIED (never submitted)", execution/comparison "UNVERIFIED", environment "n/a", safety "NOT_SUBMITTED"}`、`codeRevisions 0`、`selfRepairRounds 0`、`usage{requests 0, note "no model calls consumed; no capsule submitted"}`。

**独立证据事实与限制**：
- 原件支持：仅 `frozen-inputs.md` 与 item 两份**同源记录**（互不独立）；`sourceSha256` 在两者间一致。**没有任何**构建、运行、分类或 job 证据。
- 历史说明：frozen/item 对源码行为链（`findMyProc`/`CreateProcessA`/`VirtualAllocEx`/`QueueUserAPC`/`ResumeThread`）的描述属**源码静态取证**；源正文已删，**无法复核调用细节与行号**。
- 当前规则对照：（i）**安全边界支持"不提交"**——[安全边界 §2](../../../../../references/framework/safety-boundary.md) 第 20 行"逐例核对源码存在性、代码实际行为、危险副作用、目标环境、执行契约、隔离与清理条件"，§3 第 27 行"不得通过删掉核心行为、空跑或伪造输出把样本算作已验证"，故不提交危险副作用样本是**正确行使逐例判断**；（ii）**但"未跑源构建"与现行 §1.3 的方向不一致**——[评估准备 §1.3](../../../../../references/framework/evaluation-readiness-contract.md) 第 41/44 行要求"本轮无法合法评估行为、但**源可构建**的，记 LIB_UNOBSERVABLE_COMPILE_ONLY，继续转换并验证目标语法/编译"、"精确源集合已真实构建 completed/0……即可生成、自审"，且第 44 行明确"**不得将缺评估入口写成 SOURCE_DEPENDENCY_GAP 或不可转换**"；本项`sourceBuild` 连诊断都没有。第 49 行进一步区分"实际运行故障或行为差异须先归因，不能直接说成'没有入口'"。
- 待核验：manifest 行 94 `Lines=84` 与 `frozen-inputs.md:4` `sourceLines: 99` 不一致（同 B-03 型）；frozen 引用的"§10.16"为历史编号，现行文本中无该编号。
- 边界：本条**不得**读成"该项永不转换"（frozen 自己写明"属新冻结条件"）；也不得把"未跑源构建"读成"源不可构建"——构建结论是 `UNVERIFIED`，不是 FAIL。

**分类归入**：已有规则落实（安全边界 §2/§3 逐例副作用核对 → 不提交；任务状态 §3 未把该项写成不可转换去向、§4 保留 `PARTIAL` 与恢复条件）；**未定/待核**（"源构建未跑"与现行 §1.3"源可构建则继续生成/仅编译"的方向差异；该差异与 cases-01 B-14、harness-b-findings B-U2 同族）；装置（缺 result.md、缺分类件、缺源预检；`Lines` 不一致；历史编号 §10.16）；源已有（`mspaint.exe` + APC 注入 PoC 本身）；无知识新增。

### D2-095 / cpp-to-python / local_c2_retry.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-095-cpp-safe_attck_cpp_suite-local_c2_retry.cpp`

**文件清单与读取状态**（37 件）：
- 01-frozen：`classifier-input.json`（已读，7 行）、`classification-1.json`（已读，105 行）。**无** `frozen-inputs.md`（B-19）。
- 02-conversion：`request.system.txt`（已读，24 行）。**无** `target.gen.*`/`.model.json`（B-20）。
- 03-self-review：`review.system.txt`（已读，12 行）、`self-review-1.json`（已读，69 行，7 条全字段）、`self-review-1.model.json`（已读，18 行）。
- 04-evaluation/job-00-source-buildability（13 件）：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`（各已读）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stdout`）、`evidence-target.json`（**已读，截断**）、`evaluation_report.json`（**已读，截断**）、`controller.log`（已读，2 行）。
- 04-evaluation/job-01-dual-build（13 件）：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`、`controller-health-before.json`（各已读）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stdout`）、`evidence-target.json`（已读，可见至 `execution.stdout`）、`comparison.json`（已读）、`evaluation_report.json`（**已读，截断**）、`evaluation_report.md`（已读，77 行）、`controller.log`（已读，2 行）、`controller-health-after.json`（已读）。
- 根层：`result.md`（已读，50 行）、`evaluator_manifest.json`（已读，70 行）。**无** 根级 `target.py`。
- 另有 `batch/items/D2-095.json`（已读，51 行）。

**身份/版本关联**：taskId/rawItemId `D2-095`｜batchId `batch`｜direction `cpp-to-python`｜kind `NEW`｜disposition `CONVERTED`｜phase `CLOSED`｜lifecycle `DONE`｜pendingAction `null`｜sourceSha256 `c76c1a55c5a62d5708f27e00bf999ab04d34104e1786d5e650ccac6d0d76baf6`（manifest 行 95 大写、`classifier-input.json:5`、`classification-1.json:17`、两个 job `metadata.sourceHash` 一致）｜**finalTargetSha256 `8c092f31f244f814ea44477a79ab773afc2024ef62c4b9eb55260e047cefa918`**＝job-01 `metadata.targetHash`｜classifier `v2.4`/`009a6f31…f3a4`/ALLOWED/null/`REVIEW_NETWORK`（`reviewGroups ["network","process"]`；`local_c2_retry.cpp` `network` L23,31、`network_mode "loopback"`、`network_targets[{127.0.0.1, L29, loopback, literal, redirectVerified false}]`；`run_case.py` `process` L13,21,48,59,63,64；`requiresNetworkIsolation false`、`requiresSyntheticData false`；`inputManifestSha256 ae6eeb8e7333423c6e47a90974bda8cbd5f6615e3f2176cc97a95ca3634bfd70`）｜jobIds `eval-20261011-064320-13408bc3`（job-00）、`eval-20261011-064618-5d9a3070`（job-01，item `dualBuildJobId`）｜runner `windows-vm-agent-x64`、vmName `windows-eval`、snapshot `CC-Eval-Windows-8Lang-1.0.28`、agentVersion/collectorVersion `1.0.0`、contractSetHash `a9ed1445…d82e`｜model `deepseek-flash`。**未记 selected skills 路径/哈希**。

**冻结/分类**：**`frozen-inputs.md` 缺件**（B-19）。`classifier-input.json` 单任务 1 文件；`classification-1.json` `details.files` **2 项**（`local_c2_retry.cpp` 在前、`run_case.py` 在后）、`limitations` 三条、`inputManifestSha256 ae6eeb8e…bfd70`；两个 job 的 `this-task-classification.json` 与之一致。无 `classification-2/3`、无重分类 attempt。`result.md:14` 称源为"Atomic-Red-Team 风格本地 C2 重试模拟，49 行"（manifest 行 95 `Lines=49` 一致）。

**源预检**：job-00 `eval-20261011-064320-13408bc3`，`input_profile.json` `argv []`/`stdin null`/`timeout 30`/`dimensions ["output"]`/`normalized-text`＋`exact`/`profileId "D2-095"`；`comparison_manifest.json` source `g++ -std=gnu++17 local_c2_retry.cpp -o program.exe -lws2_32`、target `python -m py_compile target.py`；`metadata.json` `networkBoundary "isolated VM; the only target is loopback 127.0.0.1:9002 (no listener expected)"`、`targetArtifact "target/target.py (placeholder)"`、`safetyClassification "classifier-2.4"`。真实结果：source `build completed/0`/`durationMs 4550`、build stdout/stderr 均空；source `execution completed/0`/`durationMs 6688`、`stdout.normalizedText "{\"case\":\"c2_advanced\",\"state\":\"not_connected\",\"resp\":\"\"}\n"`、`structuredValue{case,state,resp}`、`digest sha256:7beba5e8…afc5`、**`sizeBytes 58`**；同 job 目标为占位（`"D2-095 placeholder\n"`）→ 平台 `mismatched`（B-23）。源基线：**取得**（非空结构化 stdout + 退出码 0）。清理：源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`；目标亦 PASSED。job-00 **无** health/runners 快照。

**模型请求/响应**：
- `request.system.txt`（24 行）：C++→Python；硬性义务同型；**关键语义**逐条给出 `#ifdef _WIN32` 分支保留、`WSAStartup` 失败 ⇒ 打印 `{"case":"c2_advanced","ok":false}` + 换行并 `return 0`、重试循环**恰好 3 次**（`socket` 失败 `continue` **不 sleep**；`connect` 失败才 `sleep 120ms`；成功 ⇒ 发送 `"PING|cap=inventory,health|seq=<i+1>"`、`recv` 一次 ≤255 后 `break`）、结束打印**一行 JSON** `{"case":"c2_advanced","state":"<state>","resp":"<lastResp>"}` + 换行、`state` 初值 `not_connected`、`std::endl` ⇒ 一个 `\n` 且刷新、`#else` 打印 `{"case":"c2_advanced","state":"windows_only"}`、**必须用真实 socket 调用，不得硬编码 state**；末段"已实测行为契约"给出无参且 9002 无监听时的精确 stdout 行。
- **`target.gen.model.json` 缺件**：生成轮 usage/哈希不可回读；`result.md:30-34` 记生成 `1463/2251/1603`、自审 `1762/3990/2647`；`item.usage` `promptTokens 3225`＝1463+1762、`completionTokens 6241`＝2251+3990、`reasoningTokens 4250`＝1603+2647（自洽）。**原响应正文**不可回读。

**失败/废弃/重提 attempt**：无（`item.failedAttempts 0`，无 `attempt-*-403.json`，无废弃 job，无重提）。唯一 attempt 即 job-00 源预检 + job-01 双侧。

**自审**：`review.system.txt`（12 行）7 条核对项（平台分支、`WSAStartup` 失败路径、重试与 sleep 语义、单行 JSON/`state` 初值/`std::endl`、是否硬编码、退出码与 stderr、网络边界只连 loopback）。`self-review-1.json` **`verdict "NO-REPAIR-IDENTIFIED"`**、`reviewedScope` 明写"静态对照 7 项清单……冻结 argv=[]、9002 无监听、win32 平台"，**7 条全字段登记**：
- 条目 1｜`conversion-introduced`｜`if sys.platform != "win32"` 分支与 `#ifdef _WIN32` 对应；仅 Cygwin 等非冻结平台可能不等价；risk low。
- 条目 2｜`conversion-introduced`｜以 `import socket` 触发 Winsock 初始化、失败抛 `OSError` 被捕获后输出 `ok:false`；**明确指出这依赖"CPython 在 `_socket` 模块初始化失败时抛 `OSError`（而非 `ImportError`）这一实现细节"，且该分支冻结下不可观察**；risk low。
- 条目 3｜`conversion-introduced`｜`for i in range(3)` 恰 3 次、`socket` 失败 `continue` 无 sleep、`connect` 失败 `s.close()`+`time.sleep(0.120)`、成功则 `state="connected"`/`req="…seq="+str(i+1)`/`recv(255)`/`len>0` 时 `state="responded"`/`s.close()` 后 `break`；指出 `socket.socket(AF_INET, SOCK_STREAM)` 未显式 `IPPROTO_TCP`、`send→sendall` 两处不影响冻结行为的细节；risk low。
- 条目 4｜`conversion-introduced`｜`out` 拼接 + `sys.stdout.buffer.write` + `flush`，恰一行 `\n` 对应 `std::endl`；`resp` 以原始字节拼接（源 `std::string` 亦不转义）；risk low。
- 条目 5｜`conversion-introduced`｜`state`/`last_resp` 由真实结果决定，**无硬编码**；risk low。
- 条目 6｜`conversion-introduced`｜所有出口 `return 0`、`ConnectionRefusedError` 属 `OSError` 已被捕获、全程未写 `sys.stderr`；risk low。
- 条目 7｜`conversion-introduced`｜唯一网络目标是字面量 `127.0.0.1:9002`，无其他地址/DNS/外部端点；risk low。
`self-review-1.model.json`：**调用元数据**——`requestSha256 74ae9855…8599`、`rawResponseSha256 df551e07…32cd`、usage `1762/3990/2647/5752`、`maxTokensFieldSent false`、`verdict NO-REPAIR-IDENTIFIED`（**无 `parseNote`**，形制正常）。无第二轮自审（`selfRepairRounds 0`）；无 `decision.json`。

**job 证据**：job-01 `eval-20261011-064618-5d9a3070`：`input_profile.json`（同 job-00）、`comparison_manifest.json` 同命令、`metadata.json`（`networkBoundary "isolated VM; only loopback 127.0.0.1:9002, no listener"`、`targetArtifact "target/target.py"`、`targetHash "sha256:8c092f31…a918"`）、`batch-authorization.json`（结构同 D2-091，含 **D2-151** 的 `dataSource.confirmation`）、`this-task-classification.json`（2 文件、ALLOWED）。
- 双侧原始观察：源 `build completed/0`/`durationMs 4684`、`execution completed/0`/`durationMs 6680`、`stdout.normalizedText "…\n"`、`digest sha256:7beba5e8…afc5`、**`sizeBytes 58`**；目标 `build completed/0`/`durationMs 56`、`execution completed/0`/`durationMs 6583`、**同一 `normalizedText`**、`digest sha256:6ff6d91b…fd93`、**`sizeBytes 57`**（B-25）、`stderr` 空。
- `comparison.json`：`behaviorVerdict "matched"`、`dimensions.output.status "matched"`（`applicable/observed true`、`diffs []`）、`filesystem/processes/registry/network` 全 `not-applicable`。
- `evaluation_report.json`（可见部分）：`runVerdict "runnable"`/`codeVerdict "passed"`/`behaviorVerdict "matched"`/`coverageRatio 1.0`/`failure null`、两侧 cleanup PASSED；`evaluation_report.md` PASS/MATCHED/CLEAN/覆盖 1-1-1-0-0 100%；`controller-health-before.json` `checkedAt 06:46:18.215134Z`、3/3、`blockingReasons []`；`controller-health-after.json` **文件不存在**（glob 未列出；`read` 返回 not found）——本项 job-01 **无 after 快照**。`controller.log` 2 行（06:46:18 / 06:47:43）。**无** `capsule.zip`、无暂存树。
- job-00：见「源预检」；平台 `mismatched` 系占位产物（B-23）。

**result / evaluator manifest**：`result.md`（50 行）五栏齐备；§1 表：交付完整性"已完成"、语法/编译"通过"（两侧 `completed/0`；目标侧为 `python -m py_compile`）、功能一致性"约定范围内匹配"、安全"符合红线"（唯一网络目标 loopback `127.0.0.1:9002`、`network` not-applicable 因未建连成功）；§3 记"**0 轮修复**。自审 `NO-REPAIR-IDENTIFIED`（7 条逐项核对）"；§4 给三条覆盖缺口（`connect` 成功后的 PING/`recv` 路径、`WSAStartup` 失败分支、源码 `#else` 非 Windows 分支）并记"**采信核对（§10.6）**：源侧观察非空且非退化"；§5 记"连接成功路径未覆盖：需**另冻条件**（在 loopback 起受控监听器）……属新冻结条件，不回改本次记录"。注意：§3 写"两侧 stdout 逐字节相同"，与 B-25 的 58/57 计数不一致。`evaluator_manifest.json`（70 行）结构同前、`jobId eval-20261011-064618-5d9a3070`、`attackClassification.rationale "local C2 retry simulation; loopback only; no connection established"`。**与副本可检查性分开**：`translatedCodePath` 指向的 `target.py` 已不在副本。

**batch/items**：disposition `CONVERTED`、phase `CLOSED`、lifecycle `DONE`、`sourcePrecheck{jobId eval-20261011-064320-13408bc3, os windows, buildCommand "g++ -std=gnu++17 local_c2_retry.cpp -o program.exe -lws2_32", completed, exitCode 0, SOURCE_BUILDABLE}`、`dualBuildJobId eval-20261011-064618-5d9a3070`、`verdicts{sourceBuild completed/0, targetBuild "completed/0 (py_compile)", execution "both completed/0; stdout byte-identical; stderr empty; network not-applicable", comparison "matched (output, diffs=0)", environment clean, safety "ALLOWED; loopback only"}`、`finalTargetSha256 8c092f31…a918`、`codeRevisions 1`、`selfRepairRounds 0`、`postEvalRepairRounds 0`、`coverageGap`（只覆盖 not-connected 路径；connect 成功 PING/recv、`WSAStartup` 失败、非 Windows 分支未覆盖）、`usage{promptTokens 3225, completionTokens 6241, reasoningTokens 4250, requests 2, model deepseek-flash, failedAttempts 0}`。

**独立证据事实与限制**：
- 原件支持：两侧 `build completed/0`、`execution completed/0`、同一 `normalizedText`/同一 `stdout` 内容、`stderr` 双空；`structuredValue{case,state,resp}` 在源侧被结构化解出（说明 `normalized-text` 比较面确实到达 JSON）；源侧 cleanup PASSED/环境 clean/READY；分类 ALLOWED（2 文件）。
- 历史说明：`request.system.txt` 的"已实测行为契约"是提交前写入；`result.md` 的"逐字节相同"与"§10.6"属记录文本（§10.6 为历史编号）。
- 当前规则对照：[评估准备 §5](../../../../../references/framework/evaluation-readiness-contract.md) 第 99 行"原始流的 digest/sizeBytes 与平台 normalizedText 是不同观察对象……归一化后相同不能证明原始字节义务通过"——本项正是该条文的实例（B-25），**不得**据 `matched` 宣称字节义务已证；§4 第 89 行两侧对称（`argv` 原样、无 fixture）；[安全边界 §3](../../../../../references/framework/safety-boundary.md) 第 25 行 loopback 允许。
- 待核验：`evidence-target.json`/`evaluation_report.json` 2000 字符后字段不可读；job-01 **缺 `controller-health-after.json`**（提交后状态无记录，见 B-19 同族的"原件不齐"）；`sizeBytes 58 vs 57` 的成因（源侧采集截掉末尾换行？）无法由本副本定案；`result.md` 与 item 的"byte-identical"表述与计数不一致。
- 边界：`matched` 只覆盖 `output` 且只覆盖"9002 无监听"的 not-connected 路径；`network not-applicable` 不证明网络行为等价；本项**未取任何文件/进程维度证据**。

**分类归入**：已有规则落实（分类准入 §3 整树分类；评估准备 §4/§5 采信与覆盖边界；安全边界 §3 loopback；交付 §2.3 分层报告）；装置（B-19 缺 frozen、B-20 缺 model.json、B-23 占位目标、缺 `controller-health-after.json`、`batch-authorization` D2-151 文本）；未定/待核（B-25 的 58/57 计数与"byte-identical"表述；历史编号 §10.6）；环境（loopback 无对端属源形态，不是装置失败）；源已有（本地 C2 重试模拟本身）；无知识新增。

### D2-096 / cpp-to-python / collection_bundle.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-096-cpp-safe_attck_cpp_suite-collection_bundle.cpp`

**文件清单与读取状态**（36 件）：
- 01-frozen：`classifier-input.json`（已读，7 行）、`classification-1.json`（已读，127 行）。**无** `frozen-inputs.md`（B-19）。
- 02-conversion：`request.system.txt`（已读，22 行）。**无** `target.gen.*`/`.model.json`（B-20）。
- 03-self-review：`review.system.txt`（已读，12 行）、`self-review-1.json`（已读，40 行，7 条仅 `id`/`origin`/`issue`）、`self-review-1.model.json`（已读，19 行，含 `parseNote`）。
- 04-evaluation/job-00-source-buildability（13 件）：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`（各已读）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stdout`）、`evidence-target.json`（**已读，截断**）、`evaluation_report.json`（**已读，截断**）、`controller.log`（已读，2 行）。
- 04-evaluation/job-01-dual-build（13 件）：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`、`controller-health-before.json`（各已读）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stdout`）、`evidence-target.json`（已读，可见至 `execution.stdout`）、`comparison.json`（已读）、`evaluation_report.json`（**已读，截断**）、`evaluation_report.md`（已读，77 行）、`controller.log`（已读，2 行）、`controller-health-after.json`（已读）。
- 根层：`result.md`（已读，52 行）、`evaluator_manifest.json`（已读，70 行）。**无** 根级 `target.py`。
- 另有 `batch/items/D2-096.json`（已读，53 行）。

**身份/版本关联**：taskId/rawItemId `D2-096`｜batchId `batch`｜direction `cpp-to-python`｜kind `NEW`｜disposition `CONVERTED`｜phase `CLOSED`｜lifecycle `DONE`｜pendingAction `null`｜sourceSha256 `59ef27b45c4a73e04555cef66556edc9d6cb8c312e15850c3f5c643ccbde132a`（manifest 行 96 大写、`classifier-input.json:5`、`classification-1.json:17`、两个 job `metadata.sourceHash` 一致）｜**finalTargetSha256 `8783b252443b9b69eee01018faf7cfa4701ddeb7d5efd78de102a81551d60fb2`**＝job-01 `metadata.targetHash`｜classifier `v2.4`/`009a6f31…f3a4`/ALLOWED/null/**`REVIEW_UNCERTAIN`**（`reason "lexical_coverage_incomplete"`；`reviewGroups ["filesystem","process"]`；`collection_bundle.cpp` `filesystem` L1,2,9,24,39,50,53、`has_file_ops true`；**`a.txt`** `limitations ["unsupported_extension"]`；`run_case.py` `process` L13,21,48,59,63,64；`requiresNetworkIsolation false`、`requiresSyntheticData false`；`inputManifestSha256 a7651eff988389e45b08051b12512c62c3b921aeafa04d546ecd16b2936c4418`）｜jobIds `eval-20261011-064909-49dd41f5`（job-00）、`eval-20261011-065321-de3984e9`（job-01，item `dualBuildJobId`）｜runner `windows-vm-agent-x64`、vmName `windows-eval`、snapshot `CC-Eval-Windows-8Lang-1.0.28`、agentVersion/collectorVersion `1.0.0`、contractSetHash `a9ed1445…d82e`｜model `deepseek-flash`。**未记 selected skills 路径/哈希**。

**冻结/分类**：**`frozen-inputs.md` 缺件**（B-19）。`classifier-input.json` 单任务 **1 文件**（`source/collection_bundle.cpp`）；`classification-1.json` `details.files` **3 项**：`collection_bundle.cpp`（`filesystem` L1,2,9,24,39,50,53）、**`a.txt`**（sha `5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03`、`limitations ["unsupported_extension"]`）、`run_case.py`；`inputManifestSha256 a7651eff…4418`；两个 job 的 `this-task-classification.json` 与之一致。**分类器实际遍历了 `source/` 树内一个 `.txt` 数据文件**——这是"整树分类"的正面实例（[分类准入 §3](../../../../../references/workflow/classifier-agent-gate.md) 第 47 行要求 `source/` 每个文件都出现在 `details.files[]`），但**输入清单只声明 1 个文件**（B-19/B-04 型镜像错位）。另：分类器看到的 `a.txt` 哈希 `5891b5b5…be03` 是 **5 字节 `hello`**（已知常量：`sha256("hello")`），而 `request.system.txt:21` 与 `metadata.json:5` 声明的是 **6 字节 `hello\n`**，两者是否同一对象**不可判定**（B-27）。无 `classification-2/3`、无重分类 attempt。

**源预检**：job-00 `eval-20261011-064909-49dd41f5`，`input_profile.json` `argv []`/`stdin null`/`timeout 30`/`dimensions ["output"]`/**`"fixtures": []`**（B-27）/`normalized-text`＋`exact`/`profileId "D2-096"`；`comparison_manifest.json` source `g++ -std=gnu++17 collection_bundle.cpp -o program.exe`、target `python -m py_compile target.py`；`metadata.json` `networkBoundary "isolated VM; no network"`、`targetArtifact "target/target.py (placeholder)"`、`note "…fixture data/collect_me/a.txt (6 bytes) on both sides; stdout only (the manifest contains absolute paths, a device-level asymmetry, so filesystem is not compared)."`。真实结果：source `build completed/0`/`durationMs 2689`、build stdout/stderr 均空；source `execution completed/0`/`durationMs 204`、`stdout.normalizedText "{\"case\":\"collection_advanced\",\"files\":1,\"total\":6}\n"`、`structuredValue{case,files 1,total 6}`、`digest sha256:1811c9ce…c4ba`、`sizeBytes 52`；同 job 目标为占位（`"D2-096 placeholder\n"`）→ 平台 `mismatched`（B-23）。源基线：**取得**（非空结构化 stdout + 退出码 0，且 `files:1,total:6` 证明 fixture 确实被读到）。清理：源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`；目标亦 PASSED。job-00 **无** health/runners 快照。

**模型请求/响应**：
- `request.system.txt`（22 行）：C++→Python；硬性义务同型；**关键语义**逐条给出相对目录 `cwd/data/collect_me` 与 `cwd/out/collection_advanced`（**不得改成绝对路径**）、`fs::create_directories` ⇒ `os.makedirs(..., exist_ok=True)`、**仅当 `src` 存在**时用 `recursive_directory_iterator` 递归且**只收 regular file**、顺序"Python 用等价的递归遍历，**按路径排序**以保证两侧一致"、写 `manifest.json`（`path` 用 `str()` **含绝对路径**、JSON 转义与源 `esc()` 一致）、写 `bundle.txt`（`### <filename>\n` + 各行 + 一个空行）、stdout 恰一行 `{"case":"collection_advanced","files":<N>,"total":<T>}` + 换行；末段"已实测行为契约"明确**"两侧均在 `data/collect_me/` 下放有同一个 6 字节文件 `a.txt`（内容 `hello\n`）"**（B-27 的声明来源）。
- **`target.gen.model.json` 缺件**：生成轮 usage/哈希不可回读；`result.md:32-35` 记生成 `1426/13843/13268`、自审 `1694/10201/8122`；`item.usage` `promptTokens 3120`＝1426+1694、`completionTokens 24044`＝13843+10201、`reasoningTokens 21390`＝13268+8122（自洽）。**原响应正文**不可回读。

**失败/废弃/重提 attempt**：无（`item.failedAttempts 0`，无 `attempt-*-403.json`，无废弃 job，无重提）。

**自审**：`review.system.txt`（12 行）7 条核对项（目录语义/递归建目录、仅 src 存在才遍历 + 只收普通文件 + 顺序稳定化、`file_size`/`total_bytes`、两文件格式、stdout 恰一行不硬编码、退出码 0 与不产生额外 stderr、是否新增行为）。`self-review-1.json` **`verdict "NO-REPAIR-IDENTIFIED"`**、**无 `reviewedScope`**、**7 条只有 `id`/`origin`/`issue`**：
- 条目 1｜`source-preexisting`｜两侧均为"当前工作目录派生相对路径后取绝对路径"，`parents=True`/`exist_ok=True` 等价 `create_directories`；无偏差。
- 条目 2｜`conversion-introduced`｜`os.walk` + `is_file()` + `followlinks=False` 与 `recursive_directory_iterator`+`is_regular_file` 一致；Python 主动 `dirs.sort()/names.sort()/collected.sort()` 做稳定化，属主动稳定化、不改变可观察语义（fixture 只 1 个文件）。
- 条目 3｜`source-preexisting`｜`st_size` 与 `file_size` 同为字节数；`total` 为和；OSError 回退 0 的失败分支在 fixture 上不可达。
- 条目 4｜`source-preexisting`｜manifest 分隔/逗号/收尾与 `bundle.txt` 结构逐字节一致；`p.name` 对应 `f.p.filename().string()`；读入侧 `newline=''`+手工剥 CRLF 等价 C++ 文本模式 `getline` 折叠。
- 条目 5｜`source-preexisting`｜恰一行 JSON + 换行；`files/total` 运行期计算未硬编码。
- 条目 6｜`source-preexisting`｜正常路径退出码 0、stderr 空、无回溯。
- 条目 7｜`environment`｜无新增可观察行为；列 4 项需 fixture 之外输入才可观察的边角差异：(a) 源 `directory_entry` 状态缓存 vs Python 显式排除 symlink（toolchain-unknown）、(b) `file_size(ec)` 失败写回无符号回绕值 vs Python 回退 0、(c) **孤立 `\r` 行尾**：Python 保留 `\r` 再补 `\n` 与 C++ 文本模式 `getline` 字节切分不同、(d) **输入文件不可读时 Python 未捕获异常输出回溯且退出码非 0，源侧静默跳过该文件正文**。
`self-review-1.model.json`：**调用元数据**——`requestSha256 1efb3992…3f6a`、`rawResponseSha256 b721e937…2195`、usage `1694/10201/8122/11895`、`maxTokensFieldSent false`、`verdict NO-REPAIR-IDENTIFIED`、`parseNote "response body is not a bare JSON object (has a preamble); verdict and items recovered by regex, raw response preserved (batch discipline 2)"`。无第二轮自审（`selfRepairRounds 0`）；无 `decision.json`。

**job 证据**：job-01 `eval-20261011-065321-de3984e9`：`input_profile.json`（同 job-00，**`fixtures` 仍为 `[]`**）、`comparison_manifest.json` 同命令、`metadata.json`（`note "…Same 6-byte fixture on both sides; stdout compared only (the manifest contains absolute paths)."`、`targetArtifact "target/target.py"`、`targetHash "sha256:8783b252…0fb2"`）、`batch-authorization.json`（结构同 D2-091，含 **D2-151** 的 `dataSource.confirmation`）、`this-task-classification.json`（3 文件、ALLOWED）。
- 双侧原始观察：源 `build completed/0`/`durationMs 2953`、`execution completed/0`/`durationMs 231`、`stdout.normalizedText "{\"case\":\"collection_advanced\",\"files\":1,\"total\":6}\n"`、`structuredValue{files 1,total 6}`、`digest sha256:1811c9ce…c4ba`、**`sizeBytes 52`**；目标 `build completed/0`/`durationMs 132`、`execution completed/0`/`durationMs 98`、**同一 `normalizedText`/同一 `structuredValue`/同一 `digest`**/**`sizeBytes 52`**（与 D2-095 的 58/57 不同，本项两侧计数一致）；`stderr` 双空。
- `comparison.json`：`behaviorVerdict "matched"`、`dimensions.output.status "matched"`（`diffs []`）、`filesystem/processes/registry/network` 全 `not-applicable`（**`filesystem` 被主动排除**，理由见 `result.md:47`）。
- `evaluation_report.json`（可见部分）：`runVerdict "runnable"`/`codeVerdict "passed"`/`behaviorVerdict "matched"`/`coverageRatio 1.0`/`failure null`、两侧 cleanup PASSED；`evaluation_report.md` PASS/MATCHED/CLEAN/1-1-1-0-0；`controller-health-before.json` `checkedAt 06:53:20.969367Z` 3/3、`blockingReasons []`；`controller-health-after.json` `checkedAt 06:54:54.365889Z` 3/3；`controller.log` 2 行（06:53:21 / 06:54:44）。**无** `capsule.zip`、无暂存树。
- job-00：见「源预检」；平台 `mismatched` 系占位产物（B-23）。

**result / evaluator manifest**：`result.md`（52 行）五栏齐备；§1 表安全行写"无网络；`filesystem` 维度 `not-applicable`（见 §4 说明）"；§3 记"**0 轮修复**"与 **fixture 设计**（"两侧同放 `data/collect_me/a.txt`（`hello\n`，6 字节），使 oracle 非平凡（`files:1, total:6`），且**只比较 `output`**"）；§4 给**装置层面**的如实说明——"`out/collection_advanced/manifest.json` 中每个文件条目含**绝对路径**，两侧工作目录不同 ⇒ 其内容**天然不同**，属**装置层面**差异，**不申请 filesystem 维度**（否则会制造假 FAIL）。`bundle.txt` 内容虽不含绝对路径，为与源一致起见本次一并未比较"；§4 另给三条覆盖缺口（`data/collect_me` 不存在时的空集合路径、多文件/子目录的递归顺序与 `manifest.json` 具体字节、写文件失败路径）；§5 记"若要证明两个输出文件字节等价，需**另冻条件**……属新冻结条件"。`evaluator_manifest.json`（70 行）结构同前、`jobId eval-20261011-065321-de3984e9`、`sceneTags ["file-io"]`、`attackClassification.rationale` 末句重复登记了"manifest.json 内嵌绝对路径属装置不对称，故未比较 filesystem"。**与副本可检查性分开**：`translatedCodePath` 指向的 `target.py` 已不在副本。

**batch/items**：disposition `CONVERTED`、phase `CLOSED`、lifecycle `DONE`、`sourcePrecheck{jobId eval-20261011-064909-49dd41f5, os windows, buildCommand "g++ -std=gnu++17 collection_bundle.cpp -o program.exe", completed, exitCode 0, SOURCE_BUILDABLE, note "execution completed/0 with the 6-byte fixture; stdout files:1 total:6"}`、`dualBuildJobId eval-20261011-065321-de3984e9`、`verdicts{sourceBuild completed/0, targetBuild "completed/0 (py_compile)", execution "both completed/0; stdout byte-identical; stderr empty", comparison "matched (output, diffs=0)", environment clean, safety "ALLOWED; no network"}`、`finalTargetSha256 8783b252…0fb2`、`codeRevisions 1`、`selfRepairRounds 0`、`postEvalRepairRounds 0`、`coverageGap`（只覆盖 fixture-present 路径；空集合路径、多文件递归顺序/`manifest.json` 具体字节、写失败路径未覆盖；**"filesystem dimension deliberately NOT requested: manifest.json embeds absolute paths (device-level asymmetry)"**）、`schedulingNote`（自审响应被 ```json 围栏包裹、正则恢复、原响应保留）、`usage{promptTokens 3120, completionTokens 24044, reasoningTokens 21390, requests 2, model deepseek-flash, failedAttempts 0}`。

**独立证据事实与限制**：
- 原件支持：两侧 `build completed/0`、`execution completed/0`、**同一 `normalizedText`/`structuredValue`/`digest`/`sizeBytes 52`**、`stderr` 双空；`files:1,total:6` 证明 fixture 在**两侧**都被读到（否则该行不会出现）；源侧 cleanup PASSED/环境 clean/READY；分类 ALLOWED（3 文件，含 `a.txt`）。
- 历史说明：`request.system.txt` 的 fixture 声明与"已实测行为契约"是提交前写入；`result.md` 的"逐字节相同"与"§10.6"属记录文本（§10.6 为历史编号）。
- 当前规则对照：**`filesystem` 的主动不申请是现行条文的正面落实**——[评估准备 §4](../../../../../references/framework/evaluation-readiness-contract.md) 第 91 行"观察维度须对应冻结行为义务……未支持或未采集的义务如实留缺口，**不缩减范围来求 matched**"，以及"采集与比较范围均显式列业务副作用路径，不用全工作目录模式纳入构建产物"；本项把"含绝对路径导致天然不同"判为**装置层面对称性缺口**并如实登记缺口，未把它混算成转换差异，符合 §2 第 89 行"两侧对称"与 §5 第 103 行"装置差异保留原判、不自行改判"。
- 待核验：`evidence-target.json`/`evaluation_report.json` 2000 字符后字段不可读；**两份 `input_profile.json` 的 `fixtures` 均为 `[]`**（B-27）——观察输入未在 profile 声明，其合法来源/哈希在副本内无处可查；`classification-1.json` 里 `a.txt` 的 5 字节哈希与声明的 6 字节内容不一致（B-27）——两者是否同一文件无法判定；`result.md` 中"两侧工作目录不同"是**推断**（本副本无两侧 workspace 实际路径证据，`evidence-*.json` 的 `workspaceRef` 分别为 `workspace/source`、`workspace/target`）。
- 边界：`matched` 只覆盖 `output`（1/1 维度）；**两个由该程序实际写出的业务文件（`manifest.json`、`bundle.txt`）字节等价完全未验证**——`filesystem not-applicable` 不证明它们相同，也不证明它们不同；fixture 只有 1 个文件，多文件递归顺序与 `manifest.json` 具体字节未覆盖。

**分类归入**：已有规则落实（分类准入 §3 整树分类（连 `.txt` 数据文件一并分类取哈希）；评估准备 §4 维度义务与"不缩减范围求 matched"、§5 装置差异登记；交付 §2.3 分层报告与 `coverageGap`）；装置（B-19/B-20/B-23/B-27/B-28；`batch-authorization` D2-151 文本；输入清单与分类结果文件集合错位）；未定/待核（`a.txt` 5 vs 6 字节、fixture 来源无记录）；源已有（本地收集打包行为本身）；无知识新增。

### D2-097 / cpp-to-python / evil_inj.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-097-cpp-evil_inj.cpp`

**文件清单与读取状态**（45 件）：
- 01-frozen：`classifier-input.json`（已读，7 行）、`classification-1.json`（已读，98 行）。**无** `frozen-inputs.md`（B-19）。
- 02-conversion：`request.system.txt`（已读，20 行）。**无** `target.gen.*`/`.model.json`（B-20）。
- 03-self-review：`review.system.txt`（已读，12 行）、`self-review-1.json`（已读，78 行，**8 条**全字段）、`self-review-1.model.json`（已读，18 行）。
- 04-evaluation/job-00-source-buildability（13 件）：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`（各已读）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stdout`）、`evidence-target.json`（**已读，截断**）、`evaluation_report.json`（**已读，截断**）、`controller.log`（已读，2 行）。
- 04-evaluation/job-01-dual-build（13 件）：`job-id.txt`、`input_profile.json`、`comparison_manifest.json`、`metadata.json`、`batch-authorization.json`、`this-task-classification.json`、`controller-health-before.json`（各已读）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stdout`）、`evidence-target.json`（已读，可见至 `execution.stdout`）、`comparison.json`（已读）、`evaluation_report.json`（**已读，截断**）、`evaluation_report.md`（已读，77 行）、`controller.log`（已读，2 行）、`controller-health-after.json`（已读）。
- 根层：`result.md`（已读，48 行）、`evaluator_manifest.json`（已读，70 行）。**无** 根级 `target.py`。
- 另有 `batch/items/D2-097.json`（已读，51 行）。

**身份/版本关联**：taskId/rawItemId `D2-097`｜batchId `batch`｜direction `cpp-to-python`｜kind `NEW`｜disposition `CONVERTED`｜phase `CLOSED`｜lifecycle `DONE`｜pendingAction `null`｜sourceSha256 `419e2d6d01afc66f4de0aa1489ca7ffc5696570256f0e3e44f31bb12bb399a38`（manifest 行 97 大写、`classifier-input.json:5`、`classification-1.json:17`、两个 job `metadata.sourceHash` 一致）｜**finalTargetSha256 `9dd0a9fe10c82ff8991661be158a011a1989f8784d823aed817c846143338e1a`**＝job-01 `metadata.targetHash`｜classifier `v2.4`/`009a6f31…f3a4`/ALLOWED/null/`REVIEW_SENSITIVE`（`reviewGroups ["process","sensitive"]`；`evil_inj.cpp` `sensitive` L58,61,64；`run_case.py` `process` L13,21,48,59,63,64；`requiresSyntheticData true`；`inputManifestSha256 c430d886f96675a930fcbbd73d3af55a6f06fba1603aac896ab6048a428d1f53`）｜jobIds `eval-20261011-065601-70f75ac4`（job-00）、`eval-20261011-065953-3a1eb437`（job-01，item `dualBuildJobId`）｜runner `windows-vm-agent-x64`、vmName `windows-eval`、snapshot `CC-Eval-Windows-8Lang-1.0.28`、agentVersion/collectorVersion `1.0.0`、contractSetHash `a9ed1445…d82e`｜model `deepseek-flash`。**未记 selected skills 路径/哈希**。

**冻结/分类**：**`frozen-inputs.md` 缺件**（B-19）。`classifier-input.json` 单任务 1 文件；`classification-1.json` `details.files` **2 项**（顺序 `evil_inj.cpp` 在前、`run_case.py` 在后）、`limitations` 三条、`inputManifestSha256 c430d886…1f53`；两个 job 的 `this-task-classification.json` 与之一致。无 `classification-2/3`、无重分类 attempt。分类 `reviewGroups` 只列 `process`+`sensitive`（源含注入 API 绑定但与 D2-092/093 一样未出现 `dynamic_code`，按 `lexical_heuristics_not_dataflow` 解释）。

**源预检**：job-00 `eval-20261011-065601-70f75ac4`，`input_profile.json` `argv ["nosuchpid"]`/`stdin null`/`timeout 30`/`dimensions ["output"]`/`normalized-text`＋`exact`/`profileId "D2-097"`；`comparison_manifest.json` source `g++ -std=gnu++17 -fpermissive evil_inj.cpp -o program.exe`、target `python -m py_compile target.py`；`metadata.json` `networkBoundary "isolated VM; frozen argv makes OpenProcess/injection all fail"`、`targetArtifact "target/target.py (placeholder)"`、`safetyClassification "classifier-2.4"`。真实结果：source `build completed/0`/`durationMs 3169`、build stdout/stderr 均空；source `execution completed/0`/`durationMs 73`、`stdout.normalizedText "PID: 0"`（`sizeBytes 6`、`digest sha256:5f0c82117dc1f773b874d7155578ac6c5a977d414257bb43111d21d757e23c5a`，**无换行**）；同 job 目标为占位（`"D2-097 placeholder\n"`）→ 平台 `mismatched`（B-23）。源基线：**取得**。清理：源侧 `preflight/cleanup PASSED`、`environmentStatus clean`、`runnerStateAfter READY`；目标亦 PASSED。job-00 **无** health/runners 快照。

**模型请求/响应**：
- `request.system.txt`（20 行）：C++→Python；硬性义务同型；**关键语义**逐条给出 `argc/argv` 映射"Python 的 `sys.argv` **含**脚本名（`sys.argv[1:]` 为参数）；源 `argv[1]` 对应 `sys.argv[1]`……**不得**照搬 C 下标"、`atoi` 的"前导数字否则 0 **不抛异常**"、`printf("PID: %i", n)` 用 `sys.stdout.write`（**不要 `print`，会多换行**）、五个注入 API 用 `ctypes` 忠实映射、"在 `atoi`=0 时 `OpenProcess` 失败（返回 NULL），后续应同样失败，程序仍走到 `return 0`，**不得**因失败抛未捕获异常或向 stderr 输出任何内容"、`return 0` ⇒ `sys.exit(0)`；末段行为契约 `target.py nosuchpid` ⇒ stdout 恰 `PID: 0`（6 字节、无换行）、stderr **空**、退出码 0。
- **`target.gen.model.json` 缺件**：生成轮 usage/哈希不可回读；`result.md:31-34` 记生成 `2287/15814/13897`、自审 `3829/7058/5190`；`item.usage` `promptTokens 4187`＝2287+3829+71？——实际 `p 4187` = 2287+3829 = **6116 ≠ 4187**，`completionTokens 26262` = 15814+7058 = **22872 ≠ 26262**，`reasoningTokens 22736` = 13897+5190 = **19087 ≠ 22736`**（**三者均不自洽**，与 D2-091/092/093/095/096 的自洽情形不同；见「待核验」）。
- **原响应正文**不可回读。

**失败/废弃/重提 attempt**：无（`item.failedAttempts 0`，无 `attempt-*-403.json`，无废弃 job，无重提）。唯一 attempt 即 job-00 + job-01。

**自审**：`review.system.txt`（12 行）7 条核对项（argv **下标基数**（`sys.argv[1]` 不是 `sys.argv[2]`）、`atoi`、无换行输出、注入 API 不可达、**stderr 必须为空**、退出码 0、是否新增行为），并明确"输出**只有**一个 JSON 对象（不要 Markdown 围栏、不要前言）"。`self-review-1.json` **`verdict "NO-REPAIR-IDENTIFIED"`**、`reviewedScope` 明写"静态逐条对照……冻结 argv=[\"nosuchpid\"]，源侧实测 stdout=PID: 0 / stderr 空 / exit 0"，**8 条全字段登记**（比该区间其余项多 1 条）：
- 条目 1｜`conversion-introduced`｜`sys.argv[1]` 对应 C 的 `argv[1]`，冻结 argv 下无 off-by-one；缺参才 `IndexError`（源侧同情形为 `atoi(NULL)` UB）；risk low。
- 条目 2｜`conversion-introduced`｜手写 `c_atoi` 跳过空白、取符号与数字、无数字返回 0、**不调 `int()` 故不抛 `ValueError`**；溢出差异（C 为 UB）冻结不可观测；risk low。
- 条目 3｜`conversion-introduced`｜`sys.stdout.write("PID: %i" % pid)` 而非 `print`，`pid=0` 恰 6 字节；写入在 ctypes 调用之前；`sys.exit(0)` 触发退出时刷新；risk low。
- 条目 4｜`conversion-introduced`｜kernel32 原型 + 五调用序列参数逐一对应；常量 `0x1F0FFF`/`0x1000`/`0x2000`/`0x40` 与 Windows 头一致；失败返回 NULL/False 而非抛错；`pid=0` 时全链静默失败、外壳代码未被执行；risk low。
- 条目 5｜`conversion-introduced`｜**逐项排除异常源**（`c_atoi` 纯字符比较、`WinDLL("kernel32")`、`create_string_buffer(my_payload, 461)` 中 `size==len(init)` 不触发 `ValueError`、`lpNumberOfBytesWritten` 传 `None` 合法、起点地址传 `NULL` 合法、未设 `errcheck`）；唯一理论分歧是缺参时 `IndexError` 写 stderr 且退出码 1（源为 `atoi(NULL)` 崩溃），属契约外输入；risk low。
- 条目 6｜`conversion-introduced`｜`sys.exit(0)`；脚本以 `if __name__ == "__main__": main()` 保护，`py_compile` 通过不执行；risk low。
- 条目 7｜`conversion-introduced`｜新增常量/原型/辅助函数/`buf`/未使用的 `rt` 均不产生 stdout/stderr、不改退出码；无新增重试/日志/异常捕获/参数校验/额外系统调用；risk low。
- 条目 8｜`conversion-introduced`｜`my_payload` 字面量与 `my_payload_len = len(my_payload)`：源 `unsigned char my_payload[] = "…"` 的 `sizeof == 字节数+1 = 460+1 = 461`，目标"逐行复制同样字节并在末行显式补 1 个 `0x00`"，"逐段核对 15 字节/行的十六进制序列未见缺字节、重字节或错位"；risk low（该长度仅在注入成功路径可观测）。
`self-review-1.model.json`：**调用元数据**——`requestSha256 4f027bfc…e8f`、`rawResponseSha256 66e81fd1…31ed`、usage `3829/7058/5190/10887`、`maxTokensFieldSent false`、`verdict NO-REPAIR-IDENTIFIED`（**无 `parseNote`**，形制正常）。无第二轮自审（`selfRepairRounds 0`）；无 `decision.json`。**注意**：条目 8 声称"逐段核对 15 字节/行的十六进制序列未见缺字节"——该结论与 D2-093 同类 payload hex 丢位缺陷形成对照，但本项目标稿正文已删，**无法独立复核**。

**job 证据**：job-01 `eval-20261011-065953-3a1eb437`：`input_profile.json`（同 job-00）、`comparison_manifest.json` 同命令、`metadata.json`（`targetArtifact "target/target.py"`、`targetHash "sha256:9dd0a9fe…8e1a"`）、`batch-authorization.json`（结构同 D2-091，含 **D2-151** 的 `dataSource.confirmation`）、`this-task-classification.json`（2 文件、ALLOWED）。
- 双侧原始观察：源 `build completed/0`/`durationMs 3?`（可见至 `execution.stdout`：`stdout.normalizedText "PID: 0"`、`sizeBytes 6`、同一 digest）；目标 `build completed/0`、`execution completed/0`、`stdout.normalizedText "PID: 0"`（6 字节、同 digest）、`stderr` 空。
- `comparison.json`：`behaviorVerdict "matched"`、`dimensions.output.status "matched"`（`diffs []`）、`filesystem/processes/registry/network` 全 `not-applicable`。
- `evaluation_report.json`（可见部分）：`runVerdict "runnable"`/`codeVerdict "passed"`/`behaviorVerdict "matched"`/`coverageRatio 1.0`；`evaluation_report.md` PASS/MATCHED/CLEAN/1-1-1-0-0；`controller-health-before.json` `checkedAt 06:59:53.100866Z` 3/3、`blockingReasons []`；`controller-health-after.json` `checkedAt 07:01:11.262694Z` 3/3；`controller.log` 2 行（06:59:53 / 07:01:04）。**无** `capsule.zip`、无暂存树。
- job-00：见「源预检」；平台 `mismatched` 系占位产物（B-23）。

**result / evaluator manifest**：`result.md`（48 行）五栏齐备；§1 表安全行"`processes` 维度 `not-applicable` ⇒ **未执行任何注入**"；§3 记"**0 轮修复**。自审 `NO-REPAIR-IDENTIFIED`（8 条）"与"**契约修正**：`-fpermissive`（C 风格隐式转换）"（**未附历史编号**，与 D2-092/093 的"按 §10.17"不同）；§4 记源侧预检与 job-01 `matched`、"两侧 stdout 逐字节相同（`PID: 0`，无换行）、stderr 空、退出码 0"、"**采信核对（§10.6）**"，覆盖缺口两条（真实 PID 注入路径按安全边界刻意不覆盖、`argv[1]` 缺省路径）；§5 "无阻断未决项；注入路径不覆盖属**设计选择**"。`evaluator_manifest.json`（70 行）结构同前、`jobId eval-20261011-065953-3a1eb437`、`attackClassification.rationale "remote-thread injection PoC; OpenProcess fails under the frozen argv so processes is not-applicable."`。**与副本可检查性分开**：`translatedCodePath` 指向的 `target.py` 已不在副本。

**batch/items**：disposition `CONVERTED`、phase `CLOSED`、lifecycle `DONE`、`sourcePrecheck{jobId eval-20261011-065601-70f75ac4, os windows, buildCommand "g++ -std=gnu++17 -fpermissive evil_inj.cpp -o program.exe", completed, exitCode 0, SOURCE_BUILDABLE}`、`dualBuildJobId eval-20261011-065953-3a1eb437`、`verdicts{sourceBuild completed/0, targetBuild "completed/0 (py_compile)", execution "both completed/0; stdout byte-identical; stderr empty; processes not-applicable", comparison "matched (output, diffs=0)", environment clean, safety "ALLOWED; no injection performed"}`、`finalTargetSha256 9dd0a9fe…8e1a`、`codeRevisions 1`、`selfRepairRounds 0`、`postEvalRepairRounds 0`、`coverageGap`（只覆盖 `argv=[nosuchpid]`；真实 PID 注入路径刻意不覆盖；空/缺 `argv[1]` 未覆盖）、`usage{promptTokens 4187, completionTokens 26262, reasoningTokens 22736, requests 2, model deepseek-flash, failedAttempts 0}`。

**独立证据事实与限制**：
- 原件支持：两侧 `build completed/0`、`execution completed/0`、同一 `PID: 0` 6 字节同 digest、`stderr` 双空、退出码 0；源侧 cleanup PASSED/环境 clean/READY；分类 ALLOWED（2 文件）。
- 历史说明：`request.system.txt` 的"已实测行为契约"是提交前写入；`result.md` 的"§10.6"为历史编号；自审条目 8 的"逐段核对 hex 未见缺字节"是**静态声明**，本副本无法复核。
- 当前规则对照：[评估准备 §5](../../../../../references/framework/evaluation-readiness-contract.md) 第 95 行"无 stdout/stderr 但真实退出/副作用足以区分未工作且符合 oracle 的项也可有有效观察"（本项 stdout 非空，采信无争议）；§4 第 89 行两侧对称；[安全边界 §3](../../../../../references/framework/safety-boundary.md) 第 27 行"不得通过删掉核心行为、空跑或伪造输出把样本算作已验证"（本项保留注入原语、冻结 argv 下不可达，未删行为）。
- 待核验：**`item.usage` 三个 token 字段与 `result.md` 分轮表之和不符**（见「模型请求/响应」）——由于 `02-conversion/target.gen.model.json` 缺件，生成轮真实 usage 无原件可查，`result.md` 的分轮数字与 item 总数**必有一方不准**（B-20 的具体后果）；`evidence-target.json`/`evaluation_report.json` 2000 字符后字段不可读；「15 字节/行 hex」的静态核对结论无法复核（D2-093 反例证明该形态确会丢位）。
- 边界：`matched` 只覆盖 `output` 与 `PID: 0` 早退路径；**payload 字面量、注入 API 绑定与 `my_payload_len` 均未取得行为证据**（`processes not-applicable`）；`DONE` 不含未覆盖维度的通过含义。

**分类归入**：已有规则落实（分类准入 §3 整树分类；评估准备 §4/§5 覆盖边界与采信；安全边界 §3 不删行为不伪造输出；交付 §2.3 分层报告）；装置（B-19 缺 frozen、B-20 缺 model.json **并导致 usage 不可对账**、B-23 占位目标、`batch-authorization` D2-151 文本、`reviewGroups` 未含 `dynamic_code`）；未定/待核（`item.usage` 与 `result.md` 分轮和不符；自审 hex 核对不可复核；历史编号 §10.6）；源已有（远程线程注入 PoC 与字符串字面量 payload）；无知识新增。

### D2-098 / cpp-to-python / evil1.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-098-cpp-evil1.cpp`

**文件清单与读取状态**（1 件）：
- 01-frozen：`frozen-inputs.md`（已读，17 行）。**无** `classifier-input.json`、**无** `classification-*.json`（item 记 `NOT_TAKEN`）。
- 02-conversion / 03-self-review / 04-evaluation：**目录均不存在**（0 模型调用、未提交）。
- 根层：**无** `result.md`、无 `evaluator_manifest.json`、无 `target.*`。
- 另有 `batch/items/D2-098.json`（已读，43 行）。

**身份/版本关联**：taskId/rawItemId `D2-098`｜batchId `batch`｜direction `cpp-to-python`｜kind `NEW`｜disposition `FROZEN`｜phase `EVALUATION_NOT_READY`｜lifecycle `PARTIAL`｜pendingAction "freeze a device that yields a safe, reproducible non-degenerate observable before submission"｜sourceSha256 `5c270702ec8cd6927049df91527a7e6804e57e621c03946b759092ffdb8e3880`（`items/D2-098.json:12` **小写**、`frozen-inputs.md:8` **大写**；manifest 行 98 大写；现行[分类准入 §3](../../../../../references/workflow/classifier-agent-gate.md) 第 58 行明确不得因大小写不同认定字节不同）｜finalTargetSha256 无｜classifier `version "2.4"`/`admissionStatus "NOT_TAKEN"`/`blockingReason null`/`cls null`/`sha256 null`，`note "not classified: not submitted"`｜jobId 无、runner/vmName/snapshot/model 均无。

**冻结/分类**：`frozen-inputs.md`（17 行）要点：形态＝"自身进程内 shellcode 执行 PoC（`VirtualAlloc` → `RtlMoveMemory` → `VirtualProtect(PAGE_EXECUTE_READ)` → `CreateThread` → `WaitForSingleObject(th, -1)`）"；评估就绪核对**两条**——无 stdout/stderr 输出（"源码中**没有一处分打印**"）、退出码恒为 0 ⇒ "**不存在非退化的可观察量**，也无法另冻条件"；且"程序会**把内嵌载荷映射为可执行并 CreateThread 执行**（并且以 `WaitForSingleObject(..., -1)` 无限等待）——即在**观察不到任何东西**的前提下仍会执行载荷。依安全边界'副作用须与所得证据相称'，**不提交**"；处置记 disposition `FROZEN`/phase `EVALUATION_NOT_READY`/lifecycle `PARTIAL`/`blockingReasons ["ORACLE_NOT_FREEZABLE", "RUN_SIDE_EFFECT_UNJUSTIFIED"]`/"**0 模型调用**；**未提交任何 capsule**；源侧构建结论记 **UNVERIFIED**（未跑）"。**无分类输入/结果件**。与 D2-094 的差别：本项的"无限等待"（`WaitForSingleObject(..., -1)`）是**驱动第四要素结构性不可能满足**（终止不可达），比 D2-094 的"注入副作用"更强。

**源预检**：**无**（未提交、未跑）。无 `job-*` 目录、无 metadata/input_profile/comparison_manifest/evidence/清理依据——属"未发生"。**同样连源可构建性都未取诊断**（`frozen-inputs.md:17`）。

**模型请求/响应**：无（0 调用）。**失败/废弃/重提 attempt**：无。**自审**：无。**job 证据**：无。

**result / evaluator manifest**：均**缺件**且 frozen 未声明不产。按[交付契约 §1.1](../../../../../references/framework/delivery-handoff-contract.md) 第 15 行与 §2.1.1 第 108 行，`EVALUATION_NOT_READY`＋`PARTIAL` 项**必须有 result.md**，缺件属交付缺档。

**batch/items**：disposition `FROZEN`、phase `EVALUATION_NOT_READY`、lifecycle `PARTIAL`、`blockingReasons ["ORACLE_NOT_FREEZABLE","RUN_SIDE_EFFECT_UNJUSTIFIED"]`、`evaluationReadiness{verdict "EVALUATION_NOT_READY", detail "无任何 stdout/stderr 输出（源码中**没有一处分打印**），退出码恒为 0；因此**不存在非退化的可观察量**，也无法另冻条件。 此外，程序会**把内嵌载荷映射为可执行并 CreateThread 执行**（并且以 `WaitForSingleObject(..., -1)` 无限等待）——即在**观察不到任何东西**的前提下仍会执行载荷。依安全边界"副作用须与所得证据相称"，**不提交**。"}`（该 `detail` 为中文，与 frozen 正文同源）、`verdicts{sourceBuild "UNVERIFIED (not run; not submitted)", targetBuild "UNVERIFIED (never submitted)", execution/comparison "UNVERIFIED", environment "n/a", safety "NOT_SUBMITTED"}`、`codeRevisions 0`、`selfRepairRounds 0`、`usage{requests 0, note "no model calls consumed; no capsule submitted"}`。

**独立证据事实与限制**：
- 原件支持：仅 `frozen-inputs.md` 与 item 两份**同源记录**；`sourceSha256` 在两者间一致（仅大小写不同）。**没有任何**构建/运行/分类/job 证据。
- 历史说明：frozen/item 对行为链与"没有一处分打印"的描述属**源码静态取证**；源正文已删，无法复核。
- 当前规则对照：（i）**安全边界支持"不提交"**——[安全边界 §3](../../../../../references/framework/safety-boundary.md) 第 27 行"不得通过删掉核心行为、空跑或伪造输出把样本算作已验证"；`WaitForSingleObject(..., -1)` 使驱动第四要素（终止）结构性不可满足，[评估准备 §2 驱动四要素](../../../../../references/framework/evaluation-readiness-contract.md) 第 62 行"无限等待、依赖外部超时兜底、残余进程"列为**不合格**——本项属该不合格项的结构性实例。（ii）**但"未跑源构建"与现行 §1.3 方向不一致**，理由同 D2-094：§1.3 第 41/44 行要求源可构建即记 LIB_UNOBSERVABLE_COMPILE_ONLY 继续生成与目标语法/编译验证，第 44 行且明确"不得将缺评估入口写成 SOURCE_DEPENDENCY_GAP 或不可转换"；§3 第 74 行进一步"不能把'缺 main'当无法评估的充分证据，也不能要求入口缺件的项永远等待而不转换"。
- 待核验：manifest 行 98 `Lines=54` 与 frozen **未记** `sourceLines`（无法比对，与 D2-094/099 的"记了但不等"不同）；frozen 未引用任何"§10.x"历史编号（与 D2-094/099 不同）；`frozen-inputs.md:10` 标题写"无可观察量 ⇒ EVALUATION_NOT_READY"，第 13 行又写"副作用须与所得证据相称"，**两条理由的边界**（前者以"无输出"为由、后者以"副作用"为由）在现行文本下分别对应 `ORACLE_NOT_FREEZABLE` 与 `RUN_SIDE_EFFECT_UNJUSTIFIED`，登记一致。
- 边界：不得读成"该项永不转换"；也不得把"未跑源构建"读成"源不可构建"（结论是 `UNVERIFIED`）。

**分类归入**：已有规则落实（安全边界 §3 逐例副作用核对；评估准备 §2 驱动四要素"无限等待"不合格；任务状态 §4 保留 `PARTIAL` 与恢复条件、§3 未写成不可转换去向）；**未定/待核**（"源构建未跑"与现行 §1.3 的方向差异，与 D2-094/B-14/B-U2 同族）；装置（缺 result.md、缺分类件、缺源预检）；源已有（自身进程内 shellcode 执行 PoC 本身）；无知识新增。

### D2-099 / cpp-to-python / processfind.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-099-cpp-processfind.cpp`

**文件清单与读取状态**（1 件）：
- 01-frozen：`frozen-inputs.md`（已读，18 行）。**无** `classifier-input.json`、**无** `classification-*.json`（item 记 `NOT_TAKEN`）。
- 02-conversion / 03-self-review / 04-evaluation：**目录均不存在**（0 模型调用、未提交）。
- 根层：**无** `result.md`、无 `evaluator_manifest.json`、无 `target.*`。
- 另有 `batch/items/D2-099.json`（已读，42 行）。

**身份/版本关联**：taskId/rawItemId `D2-099`｜batchId `batch`｜direction `cpp-to-python`｜kind `NEW`｜disposition `FROZEN`｜phase `EVALUATION_NOT_READY`｜lifecycle `PARTIAL`｜pendingAction "freeze a device that yields a safe, reproducible non-degenerate observable before submission"｜sourceSha256 `87535888d841eae1313b0e060c279dc9017d2335e6c836eea085b5f9814e0ebb`（`items/D2-099.json:12` 小写、`frozen-inputs.md:9` 大写；manifest 行 99 大写）｜finalTargetSha256 无｜classifier `version "2.4"`/`admissionStatus "NOT_TAKEN"`/`blockingReason null`/`cls null`/`sha256 null`，`note "not classified: not submitted"`｜jobId 无、runner/vmName/snapshot/model 均无。

**冻结/分类**：`frozen-inputs.md`（18 行）要点：形态＝"进程名查找 PoC（`findMyProc(argv[1])`，找到则 `printf("PID = %d\n", pid)`）"；评估就绪核对：**两条可能观察面均不可用**——**(a)** 找不到进程（`pid==0`）时**无任何输出**、退出码 0（退化）；**(b)** 找到时打印的是**动态 PID**，"两次执行/VN 都不同，**不在服务器消噪记号覆盖内**（§10.16）"；"程序不提供其它输出"；"本项**无危险副作用**，但**没有可用 oracle**，故不提交"；处置记 disposition `FROZEN`/phase `EVALUATION_NOT_READY`/lifecycle `PARTIAL`/`blockingReasons ["ORACLE_NOT_FREEZABLE"]`（**只有一条**，与 D2-094/098 的两条不同——因为本项确无危险副作用）、"**0 模型调用**；**未提交任何 capsule**；源侧构建结论记 **UNVERIFIED**（未跑）"。**无分类输入/结果件**。与 D2-094/098 的关键差别：本项**没有 unsafe 副作用**，唯一阻断是"动态 PID 不在消噪记号覆盖内"——即[评估准备 §4](../../../../../references/framework/evaluation-readiness-contract.md) 第 87 行"观察量会变且未被实际平台消噪/已确认策略覆盖时，记 ORACLE_NOT_FREEZABLE + UNVERIFIED，停止该行为评估并部分交付"的**教科书实例**（该条同时给出出路："需要结论时另冻条件"）。注意现行[比较与统计提案](../full-review-comparison-and-statistics.md) 第 21 行把"时间/PID/动态端口/随机名"列为**可扩大消噪**的类别（"展示值按类型/身份关系规范化，保持多次引用一致"），即"动态 PID 不可消噪"这一前提在本轮提案下**可能改变**——但提案本身声明"未改平台配置"，故本项当时的判断仍按其冻结条件成立。

**源预检**：**无**（未提交、未跑）。**模型请求/响应**：无（0 调用）。**失败/废弃/重提 attempt**：无。**自审**：无。**job 证据**：无。

**result / evaluator manifest**：均**缺件**且 frozen 未声明不产；按交付契约 §1.1/§2.1.1 属交付缺档。

**batch/items**：disposition `FROZEN`、phase `EVALUATION_NOT_READY`、lifecycle `PARTIAL`、`blockingReasons ["ORACLE_NOT_FREEZABLE"]`、`evaluationReadiness{verdict "EVALUATION_NOT_READY", detail "两条可能观察面均不可用：**(a)** 找不到进程（`pid==0`）时**无任何输出**、退出码 0（退化）；**(b)** 找到时打印的是**动态 PID**，两次执行/VN 都不同，**不在服务器消噪记号覆盖内**（§10.16）。程序不提供其它输出。 本项无危险副作用，但**没有可用 oracle**，故不提交。"}`、`verdicts{sourceBuild "UNVERIFIED (not run; not submitted)", targetBuild "UNVERIFIED (never submitted)", execution/comparison "UNVERIFIED", environment "n/a", safety "NOT_SUBMITTED"}`、`codeRevisions 0`、`selfRepairRounds 0`、`usage{requests 0, note "no model calls consumed; no capsule submitted"}`。

**独立证据事实与限制**：
- 原件支持：仅 `frozen-inputs.md` 与 item 两份**同源记录**；`sourceSha256` 一致（大小写不同）。**没有任何**构建/运行/分类/job 证据。
- 历史说明：frozen/item 的两条观察面分析属**源码静态取证**；源正文已删，无法复核。
- 当前规则对照：（i）`ORACLE_NOT_FREEZABLE` 的处置与现行[评估准备 §4](../../../../../references/framework/evaluation-readiness-contract.md) 第 87 行一致（"记 ORACLE_NOT_FREEZABLE + UNVERIFIED，停止该行为评估并部分交付"），**且本项无危险副作用**，故"不提交"在安全维度无争议；（ii）**但"未跑源构建 + 未生成"仍与现行 §1.3 方向不一致**（同 D2-094/098）：§1.3 第 41/44 行要求源构建通过即继续生成与目标语法/编译验证，§4 第 87 行只要求停止**该行为评估**并部分交付，**不等于**停止生成。
- 待核验：manifest 行 99 `Lines=44` 与 frozen **未记** `sourceLines`；frozen 引用的"§10.16"为**历史编号**（现行 `references/`/`AGENTS.md` 中未核到）；"动态 PID 不在消噪记号覆盖内"与[比较与统计提案](../full-review-comparison-and-statistics.md) 第 21 行"动态端口/随机名可规范化"的**口径差异**需平台侧确认（提案未改配置，本项历史判断保留）。
- 边界：本项**无**危险副作用（frozen 明写），故不得与 D2-094/098 的 `RUN_SIDE_EFFECT_UNJUSTIFIED` 混为一谈；也不得读成"源不可构建"。

**分类归入**：已有规则落实（评估准备 §4 `ORACLE_NOT_FREEZABLE` 语义与"停止该行为评估并部分交付"；任务状态 §4 保留 `PARTIAL` 与恢复条件）；**未定/待核**（"未跑源构建"与现行 §1.3 的差异；§10.16 历史编号；动态 PID 消噪口径与现行提案的关系）；装置（缺 result.md、缺分类件、缺源预检）；环境（runner 上无该进程名属源输入形态）；源已有（进程名查找 PoC 本身）；无知识新增。

### D2-100 / cpp-to-python / encode.cpp

**实际目录**：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-100-cpp-encode.cpp`

**文件清单与读取状态**（14 件）：
- 01-frozen：`frozen-inputs.md`（已读，20 行）、`classifier-input.json`（已读，7 行）、`classification-1.json`（已读，93 行）。
- 02-conversion / 03-self-review：**目录均不存在**（0 模型调用，未生成）。
- 04-evaluation/job-00-source-buildability：`job-id.txt`（已读）、`input_profile.json`（已读，23 行）、`comparison_manifest.json`（已读，20 行）、`metadata.json`（已读，12 行）、`batch-authorization.json`（已读，26 行）、`this-task-classification.json`（已读，91 行）；`returned-evidence/evidence-source.json`（已读，可见至 `execution.stderr`）、`evidence-target.json`（已读，1 行 `{"detail":"evidence_not_found"}`）、`evaluation_report.json`（**已读，完整**，1 行 2000 字符内）、`controller.log`（已读，2 行）。
- 根层：**无** `result.md`、无 `evaluator_manifest.json`、无 `target.py`。
- 另有 `batch/items/D2-100.json`（已读，46 行）。

**身份/版本关联**：taskId/rawItemId `D2-100`｜batchId `batch`｜direction `cpp-to-python`｜kind `NEW`｜disposition `SOURCE_DEPENDENCY_GAP`｜phase `SOURCE_PRECHECK_FAILED`｜lifecycle `DONE`｜pendingAction `null`｜sourceSha256 `f584900bc176021f0e460b1c258da5d2c517c4a16c45f5814c32d4c9716c8d7b`（`items/D2-100.json:12` 小写、`frozen-inputs.md:8` 大写、`classifier-input.json:5` 大写、`classification-1.json:16` 小写、`metadata.json:10` 小写、manifest 行 100 大写——**六处一致**）｜finalTargetSha256 无｜classifier `version "2.4"`/`admissionStatus "ALLOWED"`/`blockingReason null`/**`cls null`**/`sha256 null`，`note "report source: 01-frozen/classification-1.json"`——**item 的 `cls`/`sha256` 与 `classification-1.json` 实际值不一致**（见下）｜jobId `eval-20261011-070335-ab8d11ad`（job-00）｜runner `windows-vm-agent-x64`、vmName `windows-eval`、snapshot `CC-Eval-Windows-8Lang-1.0.28`、agentVersion/collectorVersion `1.0.0`（`evidence-source.json` 的 `runtime`/`baselineReference`）｜model 未记（0 调用）。

**冻结/分类**：`frozen-inputs.md`（20 行）要点：形态＝"Z85 编码器（`encode(payload, sizeof(payload))` 后打印）"、sourcePath `.../source/encode.cpp`、`sourceLines: 62`、sourceOs windows；**源侧预检定案 `SOURCE_DEPENDENCY_GAP`**，附实验表（实验 A：`g++ -std=gnu++17 encode.cpp -o program.exe`，job "见 job-id.txt"，诊断 `encode.cpp:4:10: fatal error: ./z85.h: No such file or directory`）；说明 `#include <./z85.h>`、`#include <./z85.c>` 是**项目伴随文件**（Z85 编解码库）；"**穷举核对（已执行）**：全工作区与旧 `docs/test/dataset/` 检索 `z85.*` → **0 命中** ⇒ 仓库内**无可补齐来源**"；"⇒ 记 `SOURCE_DEPENDENCY_GAP`（快照缺项目伴随文件）；**不补造**、**不删 `#include`**、**不放宽构建命令**；跳过，**0 模型调用**"；附注"`<./z85.h>` 的 **`./` 前缀**在尖括号包含下亦非标准写法，即便补齐该文件也需一并核对（属补齐后的下一步）"；安全"本 job 只构建（且构建即失败），**从未执行**"。
`classification-1.json`：`cls "REVIEW_SIDE_EFFECTS"`、`reason "local_effects_require_review"`、`reviewGroups ["process"]`、`details.files` **2 项**（`encode.cpp`——**各信号组全空**、`has_file_ops false`、`has_network false`；`run_case.py`——`process` L13,21,48,59,63,64）、`analysisScope source-text-only`、`admissionStatus ALLOWED`、`blockingReason null`、`classifierVersion 2.4`、`classifierSha256 009a6f31…f3a4`、`inputManifestSha256 06249dbb453be221a8e4d92a064599b6bac908132f76c5d8f4db7ad23b2d56e3`。`job-00/this-task-classification.json` 与之一致（2 文件、同 `inputManifestSha256`）。**`classifier-input.json` 只列 1 个文件**（`source/encode.cpp`）——同 B-04/B-05 型镜像错位。无 `classification-2/3`、无重分类 attempt。**item 差异**：`items/D2-100.json:17-18` 记 `"cls": null, "sha256": null` 并注 `note "report source: 01-frozen/classification-1.json"`，而 `classification-1.json` 实际给出 `cls REVIEW_SIDE_EFFECTS` 与 `classifierSha256 009a6f31…f3a4`——**item 把已存在的分类结论留空并以 note 转引**，属记录不一致（见「待核验」）。

**源预检**：job-00 `eval-20261011-070335-ab8d11ad`，`input_profile.json` `argv []`/`stdin null`/`timeoutSeconds 30`/`workingDirectory "workspace"`/`dimensions ["output"]`/`normalized-text`＋`exact`/`profileId "D2-100"`；`comparison_manifest.json` source `g++ -std=gnu++17 encode.cpp -o program.exe`（**与冻结记录实验 A 的命令逐字相同**）、target `python -m py_compile target.py`；`metadata.json` `networkBoundary "isolated VM; BUILD ONLY"`、`targetArtifact "target/target.py (placeholder)"`、`targetHash "sha256:placeholder-precheck"`、`note "…Z85 encoder including a project companion <./z85.h> / <./z85.c> absent from the snapshot."`、`safetyClassification "classifier-2.4"`。
真实结果（`evidence-source.json`，可见至 `execution.stderr`）：source `build.status "failed"`/`exitCode 1`/`durationMs 2383`、build stdout 0 字节、build stderr 144 字节 `encode.cpp:4:10: fatal error: ./z85.h: No such file or directory\n    4 | #include <./z85.h>\n      |          ^~~~~~~~~\ncompilation terminated.\n`（`digest sha256:a5658cc4…39b1`）；source `execution.status "blocked"`/`exitCode null`/`durationMs 0`/`timedOut false`、execution stderr "build failed"。源运行基线：**不存在**（构建失败）。清理：`evaluation_report.json` 源侧 `preflight PASSED/1`、`cleanup PASSED/1`、`contaminated false`、`environmentStatus "clean"`、`runnerStateAfter "READY"`；**目标侧 `preflight/cleanup` 均 `"SKIPPED"`/`attempts 0`、`execution.performed false`、`evidenceBundleRef null`、`runnerStateAfter null`**。
**关键对照（与 B-23 相反）**：本 job **未**提交占位目标执行——`evidence-target.json` = `{"detail":"evidence_not_found"}`、`comparisonRef null`、`outcome{runVerdict "blocked", codeVerdict "inconclusive", behaviorVerdict "inconclusive", environmentStatus "clean", evidenceCoverage{applicableDimensions 0, observedDimensions 0, matchedDimensions 0, mismatchedDimensions 0, inconclusiveDimensions 0, coverageRatio 0.0}, failure{type "CODE_RESULT", category "code", reason "Source build failed; baseline cannot be established."}, verdictReason "Source build failed; baseline cannot be established."}`、`jobStatus COMPLETED`/`jobPhase "RUNNING_SOURCE"`、`createdAt "2026-10-11T07:04:12.702964+00:00"`。**无 health-before/runners-before/after、无 `capsule.zip`、无暂存树**。`controller.log` 2 行（07:03:35 created / 07:04:12 finished）。

**模型请求/响应**：无（0 调用；`item.usage.requests 0`）。**失败/废弃/重提 attempt**：无（源构建失败本身不是 attempt 失败，是真实源诊断；`frozen-inputs.md:18` 明写"跳过，0 模型调用"）。**自审**：无（未进入生成）。

**job 证据**：仅 job-00，见上；**无** `controller-health-before.json`/`runners-before.json`/`controller-health-after.json`/closure；**无** `comparison.json`（`comparisonRef null`，符合未比较）。平台原判 `runVerdict "blocked"`/`codeVerdict "inconclusive"`/`behaviorVerdict "inconclusive"`/`coverageRatio 0.0` **原样保留**，不据其反推代码缺陷（同 cases-01 B-15 口径）。

**result / evaluator manifest**：均**缺件**。按[交付契约 §2.1.1](../../../../../references/framework/delivery-handoff-contract.md) 第 108 行"**非可转换去向**（`SOURCE_NOT_BUILDABLE`/`SOURCE_DEPENDENCY_GAP`/…）｜result.md（去向/原因、实际阶段与证据、适用件核对）；其余只要实际适用件……**result.md 不豁免**"——本项属 `SOURCE_DEPENDENCY_GAP`，**缺 result.md 即交付缺档**（该行同时明确"非可转换去向不要求 target，缺 target 不算缺档"）。

**batch/items**：disposition `SOURCE_DEPENDENCY_GAP`、phase `SOURCE_PRECHECK_FAILED`、lifecycle `DONE`、`sourcePrecheck{os windows, buildCommand "g++ -std=gnu++17 encode.cpp -o program.exe", buildStatus "failed", exitCode 1, diagnostic "encode.cpp:4:10: fatal error: ./z85.h: No such file or directory", verdict SOURCE_DEPENDENCY_GAP, detail "z85.h / z85.c are project companion files absent from the workspace and the old dataset (exhaustive search: 0 hits)"}`（**注意：`sourcePrecheck` 无 `jobId` 字段**，jobId 只在 `metadata`/`job-id.txt` 中）、`safetyAssessment "BUILD ONLY; build fails immediately, never executed."`、`verdicts{sourceBuild "failed/1 (SOURCE_DEPENDENCY_GAP)", targetBuild/execution/comparison "UNVERIFIED", environment "n/a", safety "ALLOWED"}`、`blockingReasons []`、`codeRevisions 0`、`selfRepairRounds 0`、`usage{requests 0, note "no model calls consumed"}`。

**独立证据事实与限制**：
- 原件支持：源构建**真实失败**于 `./z85.h` 缺失（`evidence-source.json` 的 build 块原文 144 字节、退出码 1）；job 源侧清理通过、环境 clean、runner 回 READY；目标侧**确实未执行**（`execution.performed false` + `evidence-target.json` `evidence_not_found` + `comparisonRef null`）；分类 ALLOWED（2 文件）。
- 历史说明：frozen 的"穷举核对（已执行）：全工作区与旧 `docs/test/dataset/` 检索 `z85.*` → 0 命中"属**交付方陈述**，本审阅**未重跑该穷举**（不写扫描脚本、不批量遍历），故按"历史说明"登记而非独立事实；item 的 `detail` 与之同源。
- 当前规则对照：[构建前提 §0.1 三分法](../../../../../references/workflow/build-prerequisites.md) 第 45–46 行"源引用了工程内其他文件（如 `..\Release\X.h`）→ **先核集合/打包**；冻结集合内漏带先恢复精确字节；**确属快照外依赖才记 `SOURCE_DEPENDENCY_GAP`，不补造桩**"、"真实诊断确认源接口与本次 runner 不匹配 → 记该候选 `SOURCE_NOT_BUILDABLE`"——本项按真实诊断记 `SOURCE_DEPENDENCY_GAP` 与"不补造/不删 `#include`/不放宽命令"，**与现行文本一致**；同文 §5 第 166 行"源码解析/类型检查阶段，缺的是**源自身**的依赖 → 源依赖缺口 → 阻断或另选完整源码"。§3 第 111–124 行"缺真实依赖不能用外壳补成存在"（本项未补，符合）。
- 待核验：**`evidence-source.json` 2000 字符后字段不可读**（`observations`/清理细节）；`frozen-inputs.md:14` 的实验表把 job 写成 `eval-20261011-...`(见 job-id.txt) —— 即**冻结记录未写死 jobId**，实际 jobId 只在 `job-id.txt`；**item 的 `classifier.cls/sha256` 为 `null` 而 `classification-1.json` 实有值**（记录不一致，未改写）；manifest 行 100 `Lines=54` 与 `frozen-inputs.md:4` `sourceLines: 62` 不一致（同 B-03 型）；`z85.*` 穷举结论未独立复核。
- 边界：`SOURCE_DEPENDENCY_GAP` **不是**转换失败、不是 `SOURCE_NOT_BUILDABLE`；`targetBuild/execution/comparison` 全 `UNVERIFIED` 不得读成 FAIL；`DONE` 仅表示该去向已定案。

**分类归入**：已有规则落实（构建前提 §0.1 三分法 + §3"不补造依赖" + §5 归因表；交付 §2.1.1 非可转换去向的报告义务；评估准备 §1.1 构建门槛）；装置（缺 result.md；item `classifier.cls/sha256` 留空与 `classification-1.json` 不一致；`sourcePrecheck` 无 `jobId`；`classifier-input.json` 与 `classification-1.json` 文件集合错位；`batch-authorization` 的 D2-151 文本；`Lines` 不一致）；未定/待核（`z85.*` 穷举 0 命中为交付方陈述、本审阅未复核；`<./z85.h>` 的 `./` 前缀非标准写法）；源已有（快照缺项目伴随文件）；无知识新增。

---

## 汇总侧补记（2026-10-12，由 B 汇总会话追加；不改写前文）

1. **D2-095 字节计数判读更正**：本文件 B-25 的“目标写对了源合同字节、源侧采集少算末尾换行”**已被第一手字节计数推翻**——两侧 `normalizedText` 均为 56 字符 JSON 加 1 个 `\n`：LF = 57 B、CRLF = 58 B，故**源 58 B 与目标 57 B 的最合理解释是 CRLF vs LF**，平台按 `normalized-text` 归一后判 `matched`。原判读记为**未证实**，不删除（追加更正）；详见 `harness-b-findings.md` B-25。
2. **本文件自报“现存文件数”有误**：按 `glob` 实测，**D2-091 为 42 件**（本文件写 38）、**D2-093 为 48 件**（本文件写 53）、**D2-095 为 32 件**（本文件写 37）；其余项未逐项复核。`harness-b-coverage.md` 的清单与计数已改以独立 `glob` 为准（见 `harness-b-findings.md` B-H6）。
3. 本补记不改写前文任何记录与结论，只纠正上述两处；原始证据与各 job 原件未改动。
