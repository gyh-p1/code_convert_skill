# harness-E 发现（D2-278 … D2-300，23 项）

> 状态：**COMPLETE**（D2-278…D2-300 共 23 项逐件读毕；读取覆盖与未读集合见[覆盖索引](harness-e-coverage.md)，逐项记录见[cases-01](harness-e-cases-01.md)/[cases-02](harness-e-cases-02.md)/[cases-03](harness-e-cases-03.md)）。本文件只覆盖该 23 项，**不**声明全数据集完成。
> 方法边界：纯静态只读，只用原生 read/glob/grep。**未**运行样本/目标/构建/分类器，**未**调用转换模型，**未**提交评估，**未**访问 `D:/CodeConvertRemote/Stack` 及 `jobs`，**未**读 `.env`/密钥/凭证，**未**改任何原始证据、items/events、旧报告、状态或自审，**未**恢复源码、**未**写目标代码。
> 判定分层：交付完整性 / 源侧语法·编译（**非目标结论**）/ 功能一致性 / 安全与授权 分列。**`result.md` 与自审都不是编译或行为证明**；本轮 23 项**无任何目标代码**，因此不存在目标编译、启动、行为或比较证据。
> 归因口径：源已有 / 转换引入 / 环境 / 装置 分别归因；**本批 23 项全部停在生成之前**，不存在“转换引入”差异，也不存在可归因的双侧观察。
> 引用符号：本文件用 `docs/dataset-2/dataset-2-copy/...`（相对本文件即 `../../../...`）。

## 1. 范围与口径事实

1. `../../../manifest.csv` 中 `D2-278`…`D2-300` 区间共 23 个编号，**全部在册**（无移除项落在该区间）：D2-278…D2-300 连续，`Kind` 全为 `NEW`，`JobId` 列全空，`Evidence` 列全为 `UNVERIFIED (not built, not run)`。这与用户给定的“23 项”一致。
2. 全数据集计数自洽：manifest 277 在册项 + README §5.2 记载的 23 项已移除 = 编号 001…300；本区间无缺口，故“区间宽度 23 = 实际 23”。其它会话区间（A 73 / B 79 / C 62 / D 34 / Codex 6）合计 254 + 本区间 23 = 277，无重复、无遗漏。
3. 本 23 项的实际目录为 `docs/dataset-2/dataset-2-copy/<direction>/D2-<nnn>-<slug>/`，每项只有 `output/batch/` 一层（`01-frozen/`、`04-evaluation/job-00-source-buildability/`、`result.md`）。**无 `source/`、无 `target/`、无 `02-conversion/`、无 `03-self-review/`、无 `comparison/`**。
4. `evaluation_report.json` 的 `kind` 全部是 `codeconvert-source-preflight-report`，`evaluationMode` 全部是 `build-and-run`。**本 23 项没有任何双侧 `codeconvert-evaluation-report`、没有 `comparison/result.json`**，所以不进入任何“冻结范围比较通过”小计。
5. **本 23 项全部 0 模型调用**：每个 `result.md` 自述“0 模型调用”，且目录中确无请求/响应/`.model.json`/`self-review-*.json` 任何一件。因此本轮对“每次模型请求与真实 content 和元数据 / 失败 attempt / 自审建议 scope·risk·unresolved / 修订与裁决”**均无对象可审**——不是缺档，而是未发生（与 `reconciliation-6.md` §4“未生成 ⇒ 无自审对象，属设计使然”一致）。
6. `closure.json` 的 `artifactDigests` 列出了 `evidence/source.json`、`evidence/source-call.json`、`evidence/source-identity.json`、`evidence/source-request.json`、`evidence/source-response.body`、`request.json`、`lifecycle.jsonl`、`staging-manifest.json` 等件的摘要，但**这些件并未随回传落到用例目录**；目录里只有 `evidence-source.json`（= `evidence/source.json`）与 `closure.json`。本审阅不据摘要推演未回传件的正文，登记为“未回传件”。

## 2. 逐项终态与证据支持事实（本人已逐件读到原件）

| Id | 方向 | cls | reviewGroups / 关键信号 | jobId | build | execution | cleanup | 终态 disposition | 模型调用 |
|---|---|---|---|---|---|---|---|---|---|
| D2-278 | ruby-to-c | REVIEW_UNCERTAIN | process 222,738 | `eval-20261012-054247-f8b64c8b` | completed/0（`Syntax OK`） | completed/0，stdout+stderr 0 字节 | passed | PREPARATION_GAP | 0 |
| D2-279 | ruby-to-cpp | LOW_SIGNAL | 无信号 | `eval-20261012-054408-bbd40bb6` | completed/0 | completed/0，空 | passed | PREPARATION_GAP | 0 |
| D2-280 | ruby-to-cpp | REVIEW_UNCERTAIN | dynamic_code 429,468 | `eval-20261012-054521-9ae80b6a` | completed/0 | completed/0，空 | passed | PREPARATION_GAP | 0 |
| D2-281 | ruby-to-cpp | REVIEW_UNCERTAIN | （reader 回填） | `eval-20261012-054636-272e9fdb` | completed/0 | completed/0，空 | passed | PREPARATION_GAP | 0 |
| D2-282 | ruby-to-cpp | REVIEW_UNCERTAIN | （reader 回填） | `eval-20261012-054749-05b85557` | completed/0 | completed/0，空 | passed | PREPARATION_GAP | 0 |
| D2-283 | ruby-to-csharp | REVIEW_UNCERTAIN | （reader 回填） | `eval-20261012-054909-0a352413` | completed/0 | completed/0，空 | passed | PREPARATION_GAP | 0 |
| D2-284 | ruby-to-csharp | REVIEW_UNCERTAIN | filesystem 155,167,184,226,229,238,279,326,403,411,417 | `eval-20261012-055025-5e5007b5` | completed/0 | completed/0，空 | passed | PREPARATION_GAP | 0 |
| D2-285 | ruby-to-csharp | REVIEW_DEPENDENCY | framework 6-9,101；process 15,17,379；`msf_dependent=true` | `eval-20261012-055142-80c0dc1f` | completed/0 | **completed/1**，stderr `uninitialized constant Msf (NameError)` | passed | SOURCE_DEPENDENCY_GAP | 0 |
| D2-286 | ruby-to-csharp | REVIEW_UNCERTAIN | （reader 回填） | `eval-20261012-055302-a2a4414e` | completed/0 | completed/0，空 | passed | PREPARATION_GAP | 0 |
| D2-287 | ruby-to-go | REVIEW_DEPENDENCY | framework 16,19-24,121；network 88,109,168,216；process 96；`requiresNetworkIsolation=true` | `eval-20261012-055500-d1e2f188` | completed/0 | **completed/1**，`Msf (NameError)` | passed | SOURCE_DEPENDENCY_GAP | 0 |
| D2-288 | ruby-to-go | REVIEW_DEPENDENCY | framework 80,135,201,202；process 70 | `eval-20261012-055640-8864a840` | completed/0 | **completed/1**，`Post is not a class (TypeError)` | passed | SOURCE_DEPENDENCY_GAP | 0 |
| D2-289 | ruby-to-go | REVIEW_DEPENDENCY | framework 6,7,8；process 103,104 | `eval-20261012-055759-172c133c` | completed/0 | **completed/1**，`Msf (NameError)` | passed | SOURCE_DEPENDENCY_GAP | 0 |
| D2-290 | ruby-to-go | REVIEW_DEPENDENCY | filesystem 128；framework 6,7；`network_mode=loopback`（localhost L128） | `eval-20261012-055913-2819c120` | completed/0 | **completed/1**，`Msf (NameError)` | passed | SOURCE_DEPENDENCY_GAP | 0 |
| D2-291 | ruby-to-go | LOW_SIGNAL | 无信号 | `eval-20261012-060050-c6153d88` | completed/0 | **completed/0**，两流空 | passed | PREPARATION_GAP | 0 |
| D2-292 | ruby-to-powershell | REVIEW_DEPENDENCY | framework×30；process 24,30,78；`requiresNetworkIsolation=true` | `eval-20261012-060238-52b478f8` | completed/0 | **completed/1**，`Msf (NameError)`，stderr 148B | passed | SOURCE_DEPENDENCY_GAP | 0 |
| D2-293 | ruby-to-powershell | REVIEW_DEPENDENCY | framework 8,115,137；`requiresNetworkIsolation=true` | `eval-20261012-060406-23765b7b` | completed/0 | **completed/1**，`LoadError: metasploit/framework/compiler/windows` | passed | SOURCE_DEPENDENCY_GAP | 0 |
| D2-294 | ruby-to-powershell | REVIEW_DEPENDENCY | framework 63,64,65,138；sensitive 124 | `eval-20261012-060527-04840085` | completed/0 | **completed/1**，`Post is not a class (TypeError)` | passed | SOURCE_DEPENDENCY_GAP | 0 |
| D2-295 | ruby-to-powershell | LOW_SIGNAL | 无信号；file limitations `[]` | `eval-20261012-060708-c93e8a19` | completed/0 | **completed/0**，两流空 | passed | PREPARATION_GAP | 0 |
| D2-296 | ruby-to-powershell | REVIEW_UNCERTAIN | 无信号；仅 `ruby_heredoc_or_block_comment_requires_review` | `eval-20261012-060825-115f4738` | completed/0 | **completed/0**，两流空 | passed | PREPARATION_GAP | 0 |
| D2-297 | ruby-to-python | LOW_SIGNAL | 无信号 | `eval-20261012-060948-53dbabf8` | completed/0 | **completed/0**，两流空 | passed | PREPARATION_GAP | 0 |
| D2-298 | ruby-to-python | REVIEW_DEPENDENCY | framework 6,7；process 15,32,33,37；`network_target`=`windows.antivirus` L48（`report_note` type 串）；`requiresNetworkIsolation=true` | `eval-20261012-061116-b7a4aa6d` | completed/0 | **completed/1**，`Msf (NameError)` | passed | SOURCE_DEPENDENCY_GAP | 0 |
| D2-299 | ruby-to-python | REVIEW_DEPENDENCY | framework 8,45；sensitive 59；`requiresSyntheticData=true` | `eval-20261012-061237-36d33e6a` | completed/0 | **completed/1**，`LoadError: metasploit/framework/compiler/windows` | passed | SOURCE_DEPENDENCY_GAP | 0 |
| D2-300 | ruby-to-python | REVIEW_DEPENDENCY | framework 6,7；sensitive 13；`requiresSyntheticData=true` | `eval-20261012-061356-ace57ce5` | completed/0 | **completed/1**，`Msf (NameError)`，stderr 144B | passed | SOURCE_DEPENDENCY_GAP | 0 |

已由本人直读覆盖的项：D2-278、279、280、283、284、285、286、287、288、289、290、300 的冻结/分类/结果关键件，以及 D2-279…291、297…300 的 `evaluation_report.json` 精简字段（grep 直读原行），D2-292/293 的分类件。其余字段由受命只读读者回填，回填后逐项列入 cases-02/03 并标注来源。

## 3. 已核实的内部矛盾与不一致（有原件支持）

### F1 `evaluation_report.json` 的字段名与真实结果相反（**最高优先**）

- 事实：以下项的 `execution.exitCode = 1` 且 stderr 是真实运行错误，但 `executionAssessment` 一律写 `completed`，`buildAssessment` 一律写 `passed`；`jobStatus=COMPLETED`、`failure=null`、`cleanup.status=passed`。
  已逐件核到 exit 1 的：**D2-285、D2-287、D2-288、D2-289、D2-290、D2-292、D2-293、D2-294、D2-298、D2-299、D2-300（11 项）**；
  已逐件核到 exit 0 且两流为空的：**D2-278、D2-279、D2-280、D2-281、D2-282、D2-283、D2-284、D2-286、D2-291、D2-295、D2-296、D2-297（12 项）**。合计 23 项。
- 同时 `result.md` 写的是“execution **completed but exitCode = 1**”，与证据一致。
- 判读：`executionAssessment=completed` 表示“运行阶段已执行完毕”，**不等于退出码为 0，也不等于行为通过**。PASS 类标签只覆盖“已提供的 critical oracle 断言”（报告正文原文），而本批 `baselineAssessment.status=UNVERIFIED`、`reasons=["independent-frozen-oracle-not-provided"]`。
- 风险：任何只读 `buildAssessment=passed` / `executionAssessment=completed` / `jobStatus=COMPLETED` / `cleanup.status=passed` 的下游消费者，会把“源语法通过 + 运行报错退出 1”误读为“源侧通过”。**建议**：报告与统计一律同时展示 `execution.exitCode`、stderr 摘要与 `baselineAssessment`；文案上避免用 `passed/completed` 代表整体结论。
- 对照：`result.md` 对两类区分正确、未粉饰（exit 1 的项都写出 `completed but exitCode = 1` 与 stderr）。**风险点在于报告层字段**：`evaluation_report.json` 只有 `buildAssessment/executionAssessment`，没有退出码字段，`failure` 又恒为 `null`（连 D2-300 的 `NameError` 也是 `failure:null`）。

### F2 `PREPARATION_GAP` 与评估准备契约 §1.3 的关系未写清

- 契约原文（`references/framework/evaluation-readiness-contract.md` §1.3，本人直读）：本轮无法合法评估行为但源可构建的，记 `LIB_UNOBSERVABLE_COMPILE_ONLY`，**继续转换并验证目标语法/编译**；且明确“不得将缺评估入口写成 `SOURCE_DEPENDENCY_GAP` 或不可转换”。
- 事实：以下 12 项“源可构建 `ruby -c` completed/0、运行 exit 0 但 stdout/stderr 全空、且无快照外加载失败”，**没有生成目标**，直接以 `PREPARATION_GAP` 终态：**D2-278、D2-279、D2-280、D2-281、D2-282、D2-283、D2-284、D2-286、D2-291、D2-295、D2-296、D2-297**。其 `result.md` 恢复条件写“提供合法来源的中性入口后重新冻结并取得有效基线，方可生成；或经逐项举证走 `LIB_UNOBSERVABLE_COMPILE_ONLY`”。
- 判读：这属于**规则空白**而非明显违规——契约对“无入口但源可构建”只写明“可走 LIB_UNOBSERVABLE_COMPILE_ONLY 继续转换”，未规定“必须继续转换”；停止并被记 `PREPARATION_GAP` 有历史依据（`reconciliation-6` §4 亦按“未生成 ⇒ 无自审对象”处理）。但**冻结记录里没有 §1.3 要求的“本轮仅验证语法/编译，行为未评估”声明**，因为本轮并未走该分支，而是停在准备缺口。
- 未定：应把“无入口、源可构建的 stdlib 项”统一归到 LIB_UNOBSERVABLE_COMPILE_ONLY（继续生成目标并验证语法/编译），还是保留 `PREPARATION_GAP` 停止？若口径变更，**属新冻结条件，不追改旧裁决**。

### F3 行数口径：冻结记录/result 与 manifest 系统性不一致

- 事实（本人直读）：D2-278 718→764、D2-279 415→444、D2-280 485→506、D2-281 449→477、D2-282 431→452、D2-283 302→321、D2-284 403→425、D2-285 342→399（**+57**）、D2-286 222→240、D2-287 212→240、D2-288 175→204、D2-289 172→208、D2-290 206→243、D2-300 100→117。**无一相等**，差值 +17…+57，且**非固定偏移**，也非单纯的 CRLF 差异（CRLF 差异只等于行数本身，不会随项变化）。
- 冻结记录的原话是“逐字节取自 manifest `Sha256` 列，大写；本地 `sha256sum` 实测一致”，但 sha256 与行数是两件事；源码已删，**无法回算**。
- 一项旁证（**双向都成立，故仍不能定案**）：D2-288 的 `result.md` 同时引用 `enum_services.rb` 的 **L79**（`Post is not a class` 报错行）与 **L42**（`module Msf` 存根）；manifest 声明 175 行时 L79/L42 仍在范围内，冻结/result 声明 204 行时也在范围内——因此引用行号**不能**判别两侧行数谁真谁假。D2-287 的 `result.md` 引用 L16/L52/L53/L54，同理两侧皆容。
- 判读：至少有一侧的 `Lines` 口径不可复现。manifest 是唯一权威索引（README §3），因此以 manifest 为声明值；冻结/result 的数值应视为**不可核验的旁证**。登记为待核 + 流程改进项（见 §5-O1）。

### F4 `casePath` 指向不存在的路径

- 事实：每项 `01-frozen/frozen-inputs.md` 的 `casePath` 都写 `docs/test/dataset-2/<direction>/D2-<nnn>-<slug>`；本仓库 `docs/test/dataset-2/` **不存在**（`glob docs/test/dataset-2/*` 无结果），实际路径是 `docs/dataset-2/dataset-2-copy/...`。同目录 `README.md` 正文也自称 `docs/test/dataset-2/`。
- 判读：属历史路径/副本迁移遗留，**不影响判定**，但会让按 `casePath` 定位原件的后续会话找不到目录。登记为流程改进项。

### F5 重分类记录与磁盘实存不一致（batch 台账 vs 用例目录）

- `reconciliation-6.md` §5 写：`D2-264`~`D2-294` 多项因分类器把 Metasploit 的 `'References'` URL、描述文本 URL、`report_note` type 串误判为网络目标，“加 `--network-isolation-configured` 重分类（`classification-2`），**误生成的 `classification-1.json` 已删除**”。
- 磁盘实况（本人直读 + 逐项 glob 核实）：本批 23 项中 `01-frozen` **只存 `-2` 件的是 5 项**——`ruby-to-go/D2-287`、`ruby-to-powershell/D2-292`、`ruby-to-powershell/D2-293`、`ruby-to-python/D2-298`（另 D2-295/296 等为 `-1`）；其余 **18 项只存 `-1` 件**。其中 `D2-288`（`-1`）、`D2-294`（`-1`）**明确保留 `classification-1.json` + `classifier-input-1.json`**，与其“首轮一次通过”的 result.md 自述一致，却与 `reconciliation-6` §5 的“`D2-264`~`D2-294` 多项……`classification-1.json` 已删除”概括**直接冲突**。
- 判读：该批注**概括过宽**。“已删除 classification-1”只对确有重分类的项成立，对 D2-288、D2-294 等“首轮即 ALLOWED、无需重分类”的项不成立——它们本来就该是 `classification-1`（与 `reconciliation-6` §5 另一行“`D2-262`/`D2-263`/`D2-265` 等首次分类一次通过，直接 `classification-1`”自相矛盾）。
- 附带证据：D2-287 的 `result.md` 自述首轮判 `BLOCKED`/`public_network_unverified` 后重分类；`D2-292`/`D2-293` 的 `classification-2.json` 仍保留 `network_targets`（`securelist.com`、`mp.weixin.qq.com`、`github.com`、`www.qualys.com`、`jxy-s.github.io` 等，全部 `redirectVerified=false`）并标 `requiresNetworkIsolation=true`。也就是说**“重分类”并没有把词法误判消掉，只是把它登记为需要网络隔离**。
- 未定：`network_targets.redirectVerified=false` 的项如何在提交前满足“硬编码外部地址须先阻断/重定向到封闭实验网并验证隔离”的安全前置；本批预检只做了 `ruby -c`，**未实际发起网络访问**，因此该风险未被触发，但也**未被验证**。

### F6 证据取回缺口：report 占位件 + `controller.log` 无 finished 行（**已核实**）

- 事实（本人直读复核）：以下 5 项的 `returned-evidence/evaluation_report.json` 与 `evaluation_report.md` **不是报告而是取回失败占位**：
  `{"detail":"job_report_not_found"}` / `{"detail":"job_human_report_not_found"}`。
  命中项：**D2-286、D2-287、D2-290、D2-291、D2-294**（5/23）。
- 同 5 项的 `returned-evidence/controller.log` **只有 `comparison job created` 一行，没有 `comparison job finished`**（本人直读 D2-286、D2-287、D2-290、D2-291、D2-294）。
- 但这 5 项的 `closure.json` 仍写 `complete=true`、`cleanupConfirmed=true`、`issues=[]`、`cleanupRecords.source.status=passed`、`runnerStateAfter=READY`、`attempts=1`，并且**记录了真实 `evaluation_report.json`/`.md` 的摘要**（如 D2-290 `e0024097…`、D2-294 `41fa6d51…`）。⇒ **底层 job 侧确实存在报告，本地件是取回失败**；但“closure 声明完成”与“本地报告缺件 + 无 finished 日志”并存，属**交付完整性层面的实际缺口**。
- 影响：这 5 项在本机**没有 report 级 `jobId`/`evaluationMode`/`buildAssessment`/`executionAssessment`/`baselineAssessment`/`cleanup`/`failure`/`createdAt`** 可核；只能靠 `source_preflight_manifest.json`（`evaluationMode`）、`evidence-source.json`（build/execution 两流）、`closure.json`（roles/cleanup）交叉。
- 判读：**不得**因 `closure.complete=true` 就认为报告已收到，也**不得**把占位 JSON 当成“报告内容为 not_found”。应按“报告未取回（有远端摘要为证）”登记，并把该项标为交付完整性存疑。**本审阅不改历史状态**。
- 附注：读者在 D2-297…300 组报告里提到 `items/D2-297.json`…`items/D2-300.json` 与 `events.jsonl` 行 1133-1145 的内容（jobId/disposition/0 模型调用一致）。这属**二手报告**，本人**未**打开 `items/` 与 `events.jsonl`（按任务约束不改不核），故仅登记为“读者观察”，不作为本审阅已验证事实。

### F7 **全部 23 项均无 `source/`、无 `target/`、无 `02-conversion/`、无 `03-self-review/`、无 capsule 归档**

- 事实：23 项目录均只有 `output/batch/01-frozen/`（3 件）、`output/batch/04-evaluation/job-00-source-buildability/`（6 件 + `returned-evidence/` 5 件）、`output/batch/result.md` = **15 件/项，合计 345 件**。源码 `.rb` 在本工作区**不存在**（多项 basename glob 均无结果），`casePath` 指向的 `docs/test/dataset-2/...` 亦不存在。
- 后果：冻结记录自称“本地 `sha256sum` 实测一致”**不可复核**；`result.md` 交付清单里写的 “capsule” 在目录内**没有对应归档**；`closure.json` 的 `artifactDigests` 记名为 `classification.json`，而磁盘上是 `classification-1.json`/`classification-2.json`（命名不一致）。
- 判读：这些属“历史已删 + 未回传”的记录边界，不改判定；但任何后续会话**不能**据 `casePath` 找源码，也不能据 `result.md` 的 “capsule” 字样认为归档存在。

### F8 长单行 JSON 的工具级截断（读取覆盖的真实边界）

- 事实：本批每项的 `returned-evidence/evidence-source.json` 与 `closure.json` 都是**单行长 JSON**，`read`/`grep` 输出在 **2000 字符**处截断（如 `evidence-source.json` 断在 `"observations":{"output":...,"filesystem":{"status":"not-applicable"...`；`closure.json` 断在 `"ora...`）。
- 判读：**这些件的尾部字段（`observations` 其余维度、`lifecycle`、`artifactDigests` 之后内容）在本机原生工具下不可读**，属“已读但截断”。本审阅**拒绝**用脚本/分块程序绕过，故如实登记为截断；不据截断处的残缺 JSON 推断未读字段。可复核的中段信息（build/execution 两流、digest、sizeBytes、snapshot、runner）已完整读到并可引用。

### F9 `requiresSyntheticData=true` 但未提供任何 fixture

- 事实：分类层标 `requiresSyntheticData=true` 的项（已逐件核到）：**D2-294、D2-299、D2-300**（另 D2-280 为 `true`，见 cases-01）；但全部 23 项 `input_profile.json` 均 `fixtures=[]`、`argv=[]`、`stdin=null`。
- 判读：因为全部 23 项**在源预检后即停**，没有进入“按 synthetic 数据驱动目标”的阶段，所以不构成“该提供而未提供”；但**若将来恢复这些项并做行为评估，必须先落实合成数据与合法入口**，不能沿用当前空 fixtures 的冻结。登记为恢复前置条件。

### F10 `batch-authorization.json` 是批次级一次性授权，被 23 项共用

- 事实：23 项的 `batch-authorization.json` 内容字面相同（`authorizedAt/validUntil/scope/contractHash` 一致），`validUntil=2026-10-17T14:43:00Z`，`scope="所有非BLOCKED任务"`。
- 判读：属“复用批次隔离授权”的既定做法，**不是**逐项新授权；`networkIsolation.verificationEvidence` 明确写“复用既有批次隔离授权 (user ruling 2026-10-10)”，并声明“网络固定 loopback/offline”“提交端宿主不承载样本执行”。本审阅不把它当成“每项已单独验证隔离”。安全边界仍以 `references/framework/safety-boundary.md` 为准，本文件不新增授权。

### F11 批次台账的窗口错位

- `reconciliation-6.md` §3 表格覆盖 `D2-255~294`（40 项窗口），而 `D2-295`~`D2-300` 的终态落在该窗口之后（`D2-294` 才触发 240 项）。`reconciliation-6` §1 的 disposition 合计 277 是对账时点全量值，而不是该表内 40 项之和。
- 判读：属**统计窗口错位**而非漏登；引用该表时必须注意“表内 40 项”与“全批 277 项”不是同一分母。

## 4. 逐项自审建议 / 知识补充（本轮结论）

- **本 23 项没有任何正式自审文件**（`self-review-*.json` 计 0），因此：①无“自审全部建议及 scope/risk/unresolved”可登记；②无“修订与裁决”可审；③`model.json`/哈希元数据问题在本批不适用（无模型响应）；④不存在“模型 reasoning 被当自审结论”的情形。
- 因此本轮**不产生新的知识补充候选**。可维护的知识线索只有批次台账里已存在的三条纪律（未在本批产生新建议）：
  1. “可构建性/可加载性只由真实诊断定案，冻结预判不代替证据”——本批 D2-278/280 的预判被实测定案推翻，**已有依据落实**（已写进 `reconciliation-6.md` 与 `batch/summary.md`，但**尚未在方向/语言知识页找到对应正文**，列为待核 K-E1）。
  2. “缺评估入口不得写成 `SOURCE_DEPENDENCY_GAP`”——契约 §1.3 已有正文；本批执行与之一致（无入口项写 `PREPARATION_GAP`，Metasploit 真依赖写 `SOURCE_DEPENDENCY_GAP`）。**已有落实**。
  3. “分类器词法误判 `'References'`/描述 URL” —— `reconciliation-6.md` §5 已记，但**无版本化规则正文**说明该误判的判定程序与 `classification-2` 的适用条件；列为待核 K-E2。
- **错误建议/被拒建议**：本批无可拒对象（无自审）。`full-review-knowledge-disposition.md` 中“已明确拒绝直接固化”的条目**均不属本批**（D2-247/254/061/067/177/103/123/194），本文件不重复引用。

## 5. 流程与评估优化建议（本轮提出，未改任何规则/配置/状态）

- **O1 统一 `Lines` 口径并写进冻结判据**：明确 manifest `Lines` = LF 归一化物理行，且冻结记录必须与该值一致或说明差异原因与测量方式；差异超过阈值时在冻结阶段登记为准备缺口。（对应 F3）
- **O2 报告字段语义拆名**：把“阶段已执行完”与“退出码/结果”分开命名（例如 `executionStage` 与 `executionExitCode`+`executionOutcome`），并在报告首屏固定展示 `execution.exitCode`、stderr 摘要、`baselineAssessment`；禁止用 `passed/completed` 单独代表整体结论。（对应 F1）
- **O3 `PREPARATION_GAP` 与 `LIB_UNOBSERVABLE_COMPILE_ONLY` 的适用边界成文**：给出“源可构建 + 无入口 + 无快照外依赖”这一类的唯一推荐去向，避免同类项在不同会话间分别落到两个去向。（对应 F2）
- **O4 缺失件与删件分别对账**：项级产出清单应把“未回传（closure 摘要里有、目录里没有）”“已删除（历史分类件）”“取回失败占位（`job_report_not_found`）”“从未发生（未生成/未自审）”四种状态分开登记，禁止用结果报告的自述或 closure 的 `complete=true` 替代目录实况核对。（对应 F6/F7）
- **O5 重分类台账按项列举**：批次对账中“某范围多项已重分类、已删除 -1 件”的概括应改为逐项列 ID 与最终保留文件名，避免概括与磁盘冲突。（对应 F5）
- **O6 长单行 JSON 的可读性**：原始证据若必须单行落盘，应在同目录提供等价的可读副本（或写路径时保留换行），否则原生只读工具下的覆盖只能到 2000 字符/行，形成**结构性未读**。（对应 F8）
- **O7 网络目标的提交前核对**：`network_targets` 非空且 `redirectVerified=false` 的项，应在提交前留下“该目标属于描述/元数据还是真实调用”的回源核对记录与隔离处置结论，不能只标 `requiresNetworkIsolation`。（对应 F5 末段）
- **O8 统计口径**：本 23 项全部为仅源预检终态，**不得**进入“冻结范围比较通过”（matched/semantic_pass）小计，也不得进入功能比较分母；`reconciliation-6` §6 已把 `D2-265`/`D2-294` 等与 matched 的边界分开，本批沿用该口径。（对应 §1.4/§1.5）

## 6. 未定与待核

1. **F2 的口径归属未定**：12 项“源可构建 `ruby -c` 通过、运行无可观察行为”应继续走 `LIB_UNOBSERVABLE_COMPILE_ONLY` 生成目标，还是保留 `PREPARATION_GAP` 停止。
2. **F3 的行数口径未定**：无法回算（源码已删），只能登记双侧声明不一致。
3. **F5 的 `redirectVerified=false` 项**：D2-287/292/293 的外部主机名是否在任何一次实际执行中被访问过——本批只做 `ruby -c`，**无网络访问证据**，但也**无“未访问”的独立证据**，故不能断定安全，也不能断定发生过外联。
4. **F6 的 5 项报告占位**：D2-286/287/290/291/294 的远端报告存在（closure 有摘要）但本地未取回；是取回失败、超时还是被覆盖，无法从现有原件区分。
5. **F8 的截断范围**：`evidence-source.json`/`closure.json` 的尾部字段（含 `observations` 其余维度、`lifecycle`）在本机不可读；是否可由原 job 目录核对未定（**本审阅不访问 `D:/CodeConvertRemote/Stack` 与 `jobs`**）。
6. **D2-298 的 `windows.antivirus` 目标**：分类件标为 `network_target`（L48，hostname，`redirectVerified=false`）并因此 `requiresNetworkIsolation=true`，而 result.md/metadata 称其为 `report_note` 的 type 字符串（词法误判）。**该字符串是否可能进入任何真实解析/求值路径，本机无法定案**；仅知本批只做 `ruby -c`。
7. 本批 23 项在 `batch/README.md` 的“未决项/WAITING 31 项”中**均不出现**（那份名单不含 278…300），可确认它们不属 WAITING；但**是否全部已同步 `items/`/`events.jsonl`** 只有 `result.md` 自述（“`items/D2-XXX.json` 与 `events.jsonl` 已同步”），本审阅**未**读 `events.jsonl`/`items/`（属旧状态原始证据，按任务约束不改不核），故该自述**仅作历史说明，未独立验证**（一名读者报告称其观察到 `items/D2-297…300.json` 与 `events.jsonl` 相应行，属二手观察，不作已验证事实）。
8. **报告占位 5 项的历史去向是否应维持 `DONE`**：D2-286/287/290/291/294 的终态在 result.md 写 `DONE`，但本地报告未取回、`controller.log` 无 finished 行。本审阅**不改**其历史状态；是否应下调为 PARTIAL/WAITING 属平台或用户裁决，见 F6 与 O4。
