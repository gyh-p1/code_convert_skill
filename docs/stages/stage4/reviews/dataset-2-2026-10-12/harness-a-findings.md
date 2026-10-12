# harness-A 审阅发现（D2-007 … D2-080）

> 状态：**IN_PROGRESS**（D2-048…069 逐件核验未完成，见 [harness-a-coverage.md](harness-a-coverage.md) 停止点）。逐项证据事实见 `harness-a-cases-01/02/04.md` 及读者 case 文件（11-20）。
> 来源分层：**原件支持的事实** / **历史说明（旧 run 记录或 batch 索引叙事）** / **当前规则对照** / **待核验** 分开；历史观察不证明当前版本效果。
> 红线：纯静态只读；未运行/编译/提交/转换；未写或运行辅助脚本；未访问 `D:/CodeConvertRemote/Stack`；未读 `.env`/密钥；未改原始证据、items/events、旧报告、自审与状态；未恢复源码。

## 1. 方法与工具限制（对全体适用）

- 只用原生 read/glob/grep；本机 pwsh 因沙箱 ACL 失败（`SetNamedSecurityInfoW … grantWrite`）不可用。
- **平台回传件多为单行 JSON**（`evidence-*.json`/`comparison.json`/`evaluation_report.json`/`closure.json`/`controller-health*.json`），read 与 grep 均把单行截断在约 2000 字符且无字节偏移读取 ⇒ **尾部不可补读**。多行件（`metadata.json`、`input_profile.json`、`comparison_manifest.json`、`source_preflight_manifest.json`、`frozen-inputs.md`、`*.md`、`controller.log`、pretty JSON、item json）已完整读取。凡结论依赖不可读尾部者记 UNKNOWN；**不得据不可读尾部推断通过**。
- 读取由 harness-A 会话内并行读者执行（同模型、同只读约束），逐件状态见 coverage 与 case 文件。

## 2. 全局事实（原件支持）

1. `../items/` 共 277 个 JSON（= manifest 行数）；`../README.md`/`summary.md` 是导航/汇总叙事，本轮只作**历史说明**。
2. **C# 目标平台缺陷**：`../platform-blocker-csharp-target.md` 记 2026-10-10 起 targetLang=csharp 因 `collectorDiagnostics.detail` schema 而 `INFRA_ERROR/BLOCKED_ENV`；2026-10-11 探针 `eval-20261011-122249-fe456bbe` 记已修复（target build/exec `completed/0`、`collectorDiagnostics=[]`），并新增“C# 目标 `target.artifactLanguage` 须写 `csharp`（写 `dotnet` 得 403 `identity_mismatch`）”纪律。**本审阅只登记历史落盘状态，不追改，也不把探针声明当作范围内新评估能力或运行授权。**
3. 原源/目标代码已从副本删除；`evidence-target.json` 在源侧预检失败项常为占位（如 `{"detail":"evidence_not_found"}`），不构成目标证据。

## 3. 跨项发现（D2-007…047 已核；048-069 待核）

### 3.1 目录仅存索引、无任何工程件（`dir-empty`/`dir-missing`）
- **dir-empty（存在但 0 文件）**：D2-008/009/010/011/012（cpp-to-csharp）、D2-030（c-to-csharp；文件 glob 0 命中，目录节点存在性无法由文件 glob 证明）。各项仅存 `../items/<id>.json`、manifest 行与 `../events.jsonl` 两条（DEFERRED `BLOCKED_ENV` + TERMINAL `WAITING`）。
- **目录缺失**：D2-065（`powershell-to-csharp/` 下 grep 无任何文件）、D2-076/077/078（`cpp-to-csharp/D2-07x-*` glob 0 命中）。三者 item 均 `FROZEN`/`NOT_STARTED`/`WAITING`/`blockingReasons=["BLOCKED_ENV"]`，`dispositionNote` 明示 “no freeze job was run…0 model calls”。
- 归因=装置/副本级 + 记录。**继承证据不在副本**：这些项 manifest 声明 `dual-build-PASS (inherited)` 与继承 JobId，副本无对应原件。

### 3.2 `disposition=FROZEN` 与缺 `frozen-inputs.md`、与 `phase=CLOSED/DONE` 并存
- 缺 `frozen-inputs.md` 却记 FROZEN：D2-008…012、D2-030、D2-065、D2-076…078、D2-019/020/021、D2-023（D2-016 为事后补写的精简版）。**现行 [任务状态 §2.2/§3](../../../../references/framework/task-state-contract.md) 已要求 FROZEN 以本 run `frozen-inputs.md` 落盘且回读为前提**——属**已违反的现行规则**，非缺规则。
- `FROZEN` 与 `phase=CLOSED`/`lifecycle=DONE` 并存：D2-020、D2-021（另有 D2-024/029/033 item 亦以 FROZEN 起头）。字段语义冲突会造成“冻结项”统计虚高。

### 3.3 `result.md` / `evaluator_manifest.json` 系统性缺口
- 全量 glob `**/result.md`（198 件）与 `**/evaluator_manifest.json`（约 78 件）逐目录比对，范围内**缺 `result.md`** 的含：D2-007…012、016、017、018、024、027、028、029、030、031…（030 起多项）；**缺 `evaluator_manifest.json`** 的含 D2-013、020、021、024、025、027、028、029、033、034、036 等。当前 [交付契约 §1.1/§2.1.1](../../../../references/framework/delivery-handoff-contract.md) 要求所有已处理项（含非可转换/WAITING）写 `result.md`，非可转换去向亦不豁免 ⇒ **交付完整性缺档**；历史项状态不改。
- 典型：**D2-017 仅 1 件**（`01-frozen/frozen-inputs.md`），却记 `PARTIAL` 终态而无报告；**D2-018 亦然**；D2-024/029 记 DONE 而无 result/manifest。

### 3.4 模型请求/响应原件：普遍 metadata-only 或缺失
- 范围内**没有任何一项保留完整模型响应正文**。`target.gen.model.json` 分两类：
  - **metadata-only**（D2-031、D2-007 类型）：仅 `model`/`finishReason`/`requestSha256`/`rawResponseSha256`/usage，**无正文**；
  - **仅内容无元数据**（D2-037…047 六项）：含 `content`（截断）+ `reasoning_content`，但**无 model/finish_reason/usage/hash**（违反 [交付契约 §2.2](../../../../references/framework/delivery-handoff-contract.md) “每份代码稿配同 stem 元数据”）。
- **生成/自修 model 件缺失**：D2-016（无 `target.gen.ps1`/无 model 元数据，item 却记 requests=2、codeRevisions=1）、D2-019（无生成 model 件）、D2-032（3 次请求无生成/修复 model 件）、D2-022/023（4/3 次请求与 1 自修，仅 self-review metadata-only）、D2-033/034/020/021/024/025（无任何 `*.model.json`）。**`usage.failedAttempts=0` 与“截断/重试”叙事在 D2-045 冲突**（见 3.5）。
- `model.json` 文件名/元数据**不能当完整响应**；自审结论只存在于 `self-review-N.json`（部分截断，尾部不可读）。

### 3.5 响应截断与“未落盘的失败 attempt”
- **D2-045**：item json/result.md/evaluator_manifest 均记 attempt-1 `finish_reason=length`（正文无 main、围栏未闭合）并“保留为 `02-conversion/attempt-1-truncated.raw.json`”，但**该文件在副本不存在**（glob `**/attempt*` 0 命中）。现行 [交付契约 §2.2/§2.2.1](../../../../references/framework/delivery-handoff-contract.md) 与 [闭环 §2 L55](../../../../references/workflow/conversion-evaluation-loop.md) 已要求保留失败 attempt 与用量 ⇒ **已违反的现行规则**。
- D2-045 另有**未冻结的契约变更**：`request.system.txt` 内含“简化许可：ZIP 用 STORED(method 0)”，而 `frozen-inputs.md` L46 仍要求“不引第三方压缩库”且未记该放宽；无修订后的冻结记录或回读 ⇒ 请求与冻结契约分歧（[交付契约 §2.2 L154](../../../../references/framework/delivery-handoff-contract.md) 要求行为需求与 capsule 策略一致）。

### 3.6 “job-00 源预检”目录内混入占位 target 的真实比较（装置污染，重复类）
- **D2-013/015**：job-00 内 `comparison.json` 记 `behaviorVerdict=mismatched`，target 侧为空/占位（D2-015 `targetValueSummary=""`、D2-013 无 `evidence-target.json` 但其 comparison 引 targetBundleId）。
- **D2-016**：job-00 `evidence-target.json` stdout 为字面量 `D2-016 placeholder`，evaluation_report 记 mismatched（真实源 vs 占位）。
- **D2-072**：`job-00b-unicode-macro` 记**两侧 preflight PASSED、两侧 execution performed、behaviorVerdict=mismatched、codeVerdict=failed、comparisonRef=comparison/result.json**，而项记录明示 target 为 `placeholder`、未生成、0 调用；`comparison/result.json` **未落盘**（引用件缺失）。
- **D2-037…041**：每项 job-00 双侧真跑、target 为 `int main(){return 0;}` 占位，报告一律 FAIL/MISMATCHED 且**无“占位件”标注**；result.md 正确只采信 source 字段。
- **D2-024/029/031/032/033/034/035/036**：job-00 均出现占位 target 的 mismatched/not-runnable 报告。
- 现行 [评估准备 §1.3/§5](../../../../references/framework/evaluation-readiness-contract.md) 已要求“不造 target 补预检”“空输出/占位 matched 不采信”，但**历史装置仍留下可被误读为转换失败的 verdict**；建议源预检统一 source-only 或显式标注 placeholder。

### 3.7 平台对“非观察”判 `matched`（假阳性类）
- **D2-024** job-03（两侧 stdout/stderr 均 0B）、job-04（两侧 stderr 同为 `DRIVER-FAILURE: readiness banner was never observed`）；**D2-029** job-01（两侧空）、job-04（两侧空+exit1）——均被记 `behaviorVerdict=matched`、`diffs=[]`、`coverageRatio=1.0`。项 attribution 已降级，但平台件仍写 matched。当前 [评估准备 §5 L95/L97](../../../../references/framework/evaluation-readiness-contract.md) 明确“两侧空输出/同一驱动失败标记不能单独支持 matched” ⇒ **违反现行规则**，且说明统计不能直接采信平台 matched 标签。

### 3.8 平台标签与消噪范围的实现差距
- **D2-044**：`127.0.0.1:<动态端口>` 与 `duration_ms` 同现，平台仍判 major（`ephemeral-ports` 未吸收 JSON 文本中的 `host:port`）；三次运行观测到 38809/35861/46803 三个不同端口 ⇒ 直接证明该字段不可复现。
- **D2-042/043/045**：唯一 major diff = `duration_ms`（1 vs 2、57 vs 51）；`input_profile.json` 的 `comparisonPolicy.output.ignoredJsonPaths` **为空**，未用现成字段排除，属冻结/配置可改进项。
- **D2-041/036**：唯一 minor diff = `timestamp`/`time`，被 `timestamps` 覆盖 ⇒ 平台判 `semantic_pass`（非 matched）；result.md 正确分档。

### 3.9 真实第三方找出的转换缺陷（原件支持，非模型断言）
- **D2-022**：job-01 目标写 `(Current User)`、stderr 空，源写 `(All Users)`、stderr 抛 `InvalidOperationException`（`Console.ReadKey` 重定向 stdin）⇒ **真实转换缺陷**（自审定位 + 评估后修复 `eval-repair-1`）；job-02 仅剩 `stream.digest` 1 个 diff（源 .NET 栈帧+绝对路径）⇒ 归因装置/运行时，平台原 verdict 保留。
- **D2-025**：目标 C++ 出现 `jump to case label crosses initialization` 真错误（初版 build failed/1）；序言式 `-fpermissive` 只把 `-Wpointer-to-int-cast` 降级而真错误仍在；最终 `self-repair-1` 修复后 build completed/0、matched。
- **D2-023**：自审定位缺 `Console.WriteLine` CRLF 追加与 `getc`→`getch`，`self-repair-1` 修复；job-01 仅 `stream.digest` 1 diff、stdout 文本相同。
- 对照：D2-037/038/039/040/046/047/019/031(经 job-02)/035 等两侧 stdout digest 逐字节相同 ⇒ 该冻结路径下转换一致。

### 3.10 哈希/行数/路径/身份漂移与冲突（可机械对账）
- **行数**：冻结物理行数与 manifest `Lines` 普遍不符（D2-007 25 vs 19、013 24 vs 19、014 36 vs 30、015 168 vs 141、016/017 有、022 146 vs 127、029 57 vs 51、031…047 多项、033/034/035/036 均不符）。
- **哈希**：D2-004 类“冻结正文漏字符”在本范围未复现，但 D2-025 的 `atoms.h`/`util.h` 在 item 与 `CORRECTION-D2-025.md` 两张表**值不同**；D2-022 item json **截断** `csprojSha256`/`finalTargetSha256`；D2-023 `result.md` 的 csproj sha（`e0d2e7a9…`）与 item/classification（`f613c4f9…`）**冲突**、job-00 metadata `sourceHash="sha256:"`（空）。
- **分类版本/SHA**：同一 `classifierSha256=441b4d50…` 被标 v2.3（D2-020/021/031/032/033/034）而 `009a6f31…` 标 v2.4（D2-019/022/023/035/036/037-047）；D2-007 的 `classification-1`（2.3）与 `classification-2`（2.4）并存、`metadata.json` 仍写 2.3、item json 用 2.3。**版本无法由文件自洽推定**。
- **caseId/路径**：同项 `casePath`（`docs/test/dataset-2/...`）、manifest `Origin`（`dataset/...`）、实际目录（`docs/dataset-2/dataset-2-copy/...`）、`evaluator_manifest.targetDir`（另一主机绝对路径 `C:\Users\Administrator…`）**四种根**；D2-007 job-00 caseId `batch-d2-007-…` vs job-00b/c `D2-007`。
- **身份冲突**：**D2-030** manifest 记 `REUSE`+继承 PASS+JobId，item 记 `kind=NEW`+全 UNVERIFIED+`casePath` 指向旧 `docs/test/dataset/...`——直接冲突，需以 manifest 为唯一身份源核对。
- **stale 状态**：C# 目标项（D2-008…012/030/065/076…078）在 blocker 文件已声明“修复”后仍 `WAITING/BLOCKED_ENV`（D2-065 为唯一 REOPEN 形态）；D2-007 item 未更新（仍 EVALUATION_BLOCKED、未记 job-00b/00c）。
- **非终态 job 记录留存**：D2-024 job-04 `job-status.json` 仍 RUNNING/CLEANING（report COMPLETED、controller.log 无 finished 行）；D2-029 job-05 `evaluation_report.json/.md` 为 `job_report_not_found`/`job_human_report_not_found`、runner `busy:CLEANING`。

### 3.11 分类器误判与准入
- `public_network_unverified` 词法误判：**D2-074**（JSON 文本冒号 `":"` 被当 hostname；唯一真实地址 L82 `127.0.0.1`）判 BLOCKED/WAITING、0 调用；同类历史见 batch 记 D2-055/D2-184/D2-191/D2-217。处置正确（不手改分类 JSON，待隔离证据后重分类）。
- **D2-021** 分类 `source_hash_mismatch`（大小写敏感比较，manifest 大写 vs 提交小写）⇒ 两次 BLOCKED 后重提 ALLOWED；item 记 2 次 blocked 尝试但**只存 1 份 blocked 判定**（差集）。
- **D2-044/045** 分类把纯文件/回环用例标 `REVIEW_NETWORK`/`has_network=true`（D2-045 源被自述“无网络信号”）⇒ 词法误报；D2-045 同时被标 `filesystem[95,98,…]`。

### 3.12 路径泄漏（报告级发现，未访问该目录）
- 多个 `evidence-source.json`/`observed-source-stderr.txt`/源 .NET 栈帧含 `C:\CodeConvertRemote\Stack\Agent\workspaces\<jobId>\…` 绝对路径（D2-022 四个 bundle、D2-023 三处、D2-031 stderr/traceback 等）。**本轮仅阅读回传文本，未访问该目录**；建议存储前剥离绝对路径，避免路径暴露与噪声。

### 3.13 用量/模板/命名一致性
- **D2-046** `totalTokens 75781` ≠ prompt 13436 + completion 46845 = 60281（差 15500）；**D2-045** `requests=3`/`failedAttempts=0` 而 attempt-1 usage 未计入、`promptTokens 11960` 小于自审单次 14909。项 usage 与逐调用 model 记录不自洽。
- **D2-046/047** 的 `review.system.txt` 模板占位符/标识符被剥离（reviewer 拿到残缺清单）。
- **batch-authorization.json** 在 D2-016、D2-032、D2-035、D2-036、D2-037…047 等 10+ 份中**误引别的任务号 `D2-088`**（"该项 D2-088 无网络、无凭证…"），对 loopback 项自相矛盾。
- `job-00b` 同用途名被复用于 toolchain-probe 与 source-preflight（D2-007）；job 目录命名与用途需逐件核。

## 4. 知识侧（候选 / 已有规则落实 / 错误建议）

### 4.1 已有现行规则、属“应落实/已违反”而非新规则
1. 冻结落盘门禁与 FROZEN 定义（[任务状态 §2.2/§3](../../../../references/framework/task-state-contract.md)）— D2-008…012/019/020/021/023/030 等违反。
2. 失败/截断 attempt 与逐次用量必须保留（[交付契约 §2.2/§2.2.1](../../../../references/framework/delivery-handoff-contract.md)、[闭环 §2 L55](../../../../references/workflow/conversion-evaluation-loop.md)）— D2-045 违反；每份代码稿须配同 stem `.model.json` — D2-016/032 等违反。
3. 两侧空输出/同一驱动失败标记不能支持 matched（[评估准备 §5 L95/§5 L97](../../../../references/framework/evaluation-readiness-contract.md)）— D2-024/029 平台仍 matched。
4. 运行环境量不得当冻结基线；不可复现量记 `ORACLE_NOT_FREEZABLE` + UNVERIFIED 并部分交付（[评估准备 §4 L85-87/§5](../../../../references/framework/evaluation-readiness-contract.md)）— D2-015 自审误引“冻结基线”，D2-042…045/054/062/072 走该分支。
5. 驱动须按目标语言形态启动、原样透传子进程字节（[评估准备 §2 L66](../../../../references/framework/evaluation-readiness-contract.md)；batch/operational-discipline §6/§7）— D2-013/031/061/062 历史装置故障。
6. 交付终态门禁与 result.md 全覆盖（[交付契约 §1.1/§2.1.1](../../../../references/framework/delivery-handoff-contract.md)）— 见 §3.3。

### 4.2 候选新增规则（现有正文未覆盖，逐条待维护）
- **K-A1 源预检占位 target 隔离**：源侧预检应统一 source-only，或对占位 target 比较显式标注；否则 `behaviorVerdict=mismatched/codeVerdict=failed` 可被误读为转换失败（证据 D2-013/015/016/019/024/029/031…041/072）。现行 §1.3 原则相近，但**标准骨架仍允许 job-00 携带 target 树**。
- **K-A2 平台 matched 的最小有效性门**：matched 须以非空且非退化的源观察为前提（§5 L95 已表述原则，建议在统计/验收处显式机械校验；D2-024/029 反例）。
- **K-A3 manifest 与冻结/证据的可机械对账字段**：`Lines`↔物理行数、`JobId`↔实际 job、`Kind/casePath`↔item、sha 全 64 位、usage 合计 = 逐调用之和（D2-022/025/030/045/046 反例）。
- **K-A4 构建/编译 stdout 不应入比较面**：MSBuild/gcc 输出含绝对路径与本地化文本，永不可能逐字节相同（D2-022/023/033…036 的 `-Wformat-truncation` 警告即例）。
- **K-A5 活动计数器/动态端口默认非 oracle**：`duration_ms`/`mod_time`/`archive_bytes`/`host:port` 应经 `ignoredJsonPaths` 或冻结前验证排除，而非依赖 `tolerate_minor`（D2-042/043/044/045 反例）。
- **K-A6 运行中契约变更须回写冻结**：D2-045 的 STORED 放宽未回写 `frozen-inputs.md`。
- **K-A7 分类器 hostname 启发式**：排除 JSON/文本字面量的 `:`（D2-074）；hash 比较大小写（D2-021）；纯文件/回环误标网络（D2-044/045）。
- **K-A8 提示模板完整性**：review/request 模板占位符须渲染校验（D2-046/047 残缺）。
- **K-A9 路径脱敏**：存储前剥离 `C:\CodeConvertRemote\Stack\…` 绝对路径（§3.12）。
- **K-A10 方向映射候选（go-to-cpp）**：Go `json.Marshal` 的 **map 字典序 vs struct 字段序**（D2-038 最清晰、D2-039 三重键序、D2-046/047）；`runtime.GOOS` 编译期短路须以 `#ifdef _WIN32` 保留（D2-041）；`compress/flate` 字节不保证与 zlib 一致且禁止第三方压缩库，等价性只在特定输入类成立并须记不可外推边界（D2-040）；C→C++ 变量跨 `case` 标签须加花括号作用域（D2-025）；C `format_rfc3339` 手写 UTC 偏移与 Go `time.RFC3339` 的等价性限于零偏移分支（D2-033/036）；Ruby `Process.fork` 返回 nil 与 C `fork()==-1` 语义映射（D2-032）。这些在 `skills/` 未逐条定位，属**候选**，未经本轮效果验证。
- **K-A11 对称装置扩展到 cwd/env/被统计集合**（D2-039 强形式；batch §10.18/§10.19 只覆盖 argv 文件与目录条目数）。

### 4.3 错误/不可采信的自审建议
- 未发现“错误修复建议被采纳”的实例：D2-016 的 CRLF 强制提案、D2-064 的目录权限提案均**未采纳**（在观察面之外），处理正确。
- **不可信断言**：D2-015 自审把冻结明确拒绝冻结的环境量当“frozen baseline”；D2-043 自审把 target 侧实现文本标 `origin=source-preexisting`；D2-044 自审把 `origin=conversion-introduced` 与“未发现问题”并列（origin 语义混用）；D2-046 item7 在未编译前断言“逐字节相同”；D2-035 request 与 review 对“MarshalIndent 末尾是否追加 \n”自相矛盾；D2-029 job-03/05 曾断言“conversion-introduced hit-predicate defect”后被 job-09 retract。**均不作为结论**。

## 5. 消噪与统计提案的应用（审查口径，非运行授权）

- 采用 [full-review-comparison-and-statistics.md](full-review-comparison-and-statistics.md)：**有效 matched + 有效 semantic_pass** 均可进入“冻结范围比较通过”小计，**分列数量与覆盖边界**。
- 本范围可按该口径计入“比较通过”的**候选**（仅限其冻结路径，且须减去 3.6/3.7 的占位与空观察反例）：D2-013(job-03 matched)、D2-014、D2-015、D2-016、D2-019、D2-020、D2-021、D2-025、D2-031(job-02)、D2-032、D2-035、D2-037、D2-038、D2-039、D2-040、D2-041(**semantic_pass**)、D2-046、D2-047、D2-036(**semantic_pass**)、D2-022/023（`mismatched` 但缺陷已修、残余归因装置——**按原 verdict 不入通过小计**）。
- 单列：`PARTIAL/ORACLE_NOT_FREEZABLE` = D2-042/043/044/045、D2-054、D2-062、D2-072 等；`mismatched` 未定 = D2-022/023（残余）；仅源预检/非可转换 = D2-017/018/024/027/028/029/030/065/070…080 等。**不合成单一成功率。**

## 6. 流程/评估优化（建议）

1. 源预检统一 source-only；占位 target 比较加显式标注或移出 verdict 目录。
2. 每份代码稿/自修/评估后修复均落 `.model.json`（含 model/finish_reason/usage/输入输出 sha）；失败/截断 attempt 必落盘。
3. 平台回传单行 JSON 另存 pretty/`.md` 伴侣，或提供字节区间读取；否则尾部不可验收。
4. item/result/manifest 的哈希取全 64 位，且与 classification/frozen 同源生成；机械对账 `Lines`/`JobId`/`Kind`/`casePath`。
5. 冻结超时与 `input_profile.timeoutSeconds` 同源；运行中契约变更回写冻结并回读。
6. 模板渲染校验；`batch-authorization` 按项生成 taskId；存储前剥离绝对路径。
7. `job-status`/`controller.log` 与非终态记录同步（禁止以 RUNNING/CLEANING 记录替代终态）；探针 job 与 verdict job 分列。

## 7. 未知与停止点

- **不可读**：所有单行平台件的 2000 字符后尾部（diff 明细、`cleanupRecords`、`artifactDigests`、`observations`）；已删源/目标/驱动/请求/响应/自审正文。
- **未完成**：D2-048…069（22 项现存）逐件核验与逐件清单；读者 case 文件 11-20 落盘确认。**未读集合 = {D2-048,049,050,051,052,053,054,055,056,057,058,059,060,061,062,063,064,065,066,067,068,069}**（D2-065 已确认 dir-missing，仍是现存项）。
- **已读项**：D2-007…047（41 项，含 D2-026 移除）+ D2-070…075、D2-079、D2-080 = **48 项现存**。
- 停止点：见 [harness-a-coverage.md](harness-a-coverage.md) “本轮结束时的精确停止点”。下轮先确认读者 case 文件，再补 048-069，最后把 coverage 转 COMPLETE。
