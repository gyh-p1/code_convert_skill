# harness-A 逐项证据（D2-024 / D2-025 / D2-027 / D2-028 / D2-029 / D2-030）

> 只读静态审阅。未创建/修改其他文件，未运行任何脚本/命令/分类器/转换/提交，未访问 `D:/CodeConvertRemote/Stack`，未读 `.env`/密钥，未重建源码。
> 工具限制（影响全体平台回传件）：平台回传的 `evidence-*.json`、`comparison.json`、`evaluation_report.json`、`job-status.json`、`controller-health*.json` 多为**单行 JSON**；`read` 与 `grep` 均把单行截断在约 2000 字符，且无字节偏移读取手段 ⇒ 2000 字符之后的尾巴（`cleanupRecords`、`artifactDigests`、`collectorDiagnostics`、diff 明细）**无法补读**，已逐件记 `read(trunc>2000)`，不据不可读尾部推断通过。
> 文件清单路径基准：`docs/dataset-2/dataset-2-copy/<dir>/`；`<dir>` 在每项给出。状态取值：`read` / `read(trunc>2000)` / `empty` / `missing` / `dir-empty`。
> 事实分层：**原件支持的事实** / **历史说明（旧 run 记录）** / **当前规则对照** / **待核验** 分开写；模型自述与归因文字不作为结论，历史观察不证明当前版本效果。

---

## D2-024 ｜ dir=`c-to-cpp/c01-linux-win-network` ｜ 46 件

### IDENTITY
- taskId `D2-024`；direction `c-to-cpp`；源文件 `uhttpd.c`（1318 LF 行）；manifest 声明 Sha256 `81400C369E02FFD116AAFD2922CA4266F8C826F06FAD20AA4D1A6F41A04E8583`（manifest 大写、item/frozen 小写，同值）。
- manifest：Kind `REUSE`；Origin `dataset/c-to-cpp/c01-linux-win-network`；JobId `eval-20260926-052820-e96bf2ee`；Evidence `dual-build-PASS (inherited)`。
- item json `batch/items/D2-024.json`：kind `REUSE`；casePath `docs/test/dataset-2/c-to-cpp/c01-linux-win-network`；disposition `FROZEN`；phase `CLOSED`；lifecycle `DONE`；**无 `pendingAction` 键**；`blockingReasons: []`；`usage.requests: 1`（"single conversion call; no repair needed"）；`codeRevisions: 0`；`selfRepairRounds: 0`；另含 `classifier.inputManifestSha256`、`verdicts`、`behaviorEvidence`、`coverageGaps`、`instrumentDefects`。

### FILE INVENTORY（全部 46 件；基准 `docs/dataset-2/dataset-2-copy/c-to-cpp/c01-linux-win-network/`）
```
output/batch/01-frozen/classification-1.json=read
output/batch/01-frozen/classifier-input.json=read
output/batch/01-frozen/evaluation-freeze.md=read
output/batch/01-frozen/frozen-inputs.md=read
output/batch/03-self-review/self-review-1.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/input_profile.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/comparison_manifest.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/metadata.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/job-status.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evaluation_report.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-01-version-and-usage/input_profile.json=read
output/batch/04-evaluation/job-01-version-and-usage/comparison_manifest.json=read
output/batch/04-evaluation/job-01-version-and-usage/metadata.json=read
output/batch/04-evaluation/job-01-version-and-usage/job-status.json=read
output/batch/04-evaluation/job-01-version-and-usage/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-01-version-and-usage/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-01-version-and-usage/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-01-version-and-usage/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-02-unknown-option/input_profile.json=read
output/batch/04-evaluation/job-02-unknown-option/comparison_manifest.json=read
output/batch/04-evaluation/job-02-unknown-option/metadata.json=read
output/batch/04-evaluation/job-02-unknown-option/job-status.json=read
output/batch/04-evaluation/job-02-unknown-option/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-02-unknown-option/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-02-unknown-option/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-02-unknown-option/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-03-loopback-listen/attribution.md=read（装置缺陷/假阳性归因）
output/batch/04-evaluation/job-03-loopback-listen/input_profile.json=read
output/batch/04-evaluation/job-03-loopback-listen/comparison_manifest.json=read
output/batch/04-evaluation/job-03-loopback-listen/metadata.json=read
output/batch/04-evaluation/job-03-loopback-listen/job-status.json=read
output/batch/04-evaluation/job-03-loopback-listen/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-03-loopback-listen/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-03-loopback-listen/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-03-loopback-listen/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-04-loopback-listen-live-capture/attribution.md=read
output/batch/04-evaluation/job-04-loopback-listen-live-capture/input_profile.json=read
output/batch/04-evaluation/job-04-loopback-listen-live-capture/comparison_manifest.json=read
output/batch/04-evaluation/job-04-loopback-listen-live-capture/metadata.json=read
output/batch/04-evaluation/job-04-loopback-listen-live-capture/job-status.json=read（仍为 RUNNING/CLEANING，非终态）
output/batch/04-evaluation/job-04-loopback-listen-live-capture/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-04-loopback-listen-live-capture/returned-evidence/controller.log=read（只有 created 行，无 finished 行）
output/batch/04-evaluation/job-04-loopback-listen-live-capture/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-04-loopback-listen-live-capture/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-04-loopback-listen-live-capture/returned-evidence/evidence-target.json=read(trunc>2000)
```
- `result.md`=missing；`evaluator_manifest.json`=missing；无任何 `request*.txt` / `*.model.json` / `repair*`。

### FREEZE/CLASSIFY
- `frozen-inputs.md` L4-5：sourcePath `docs/test/dataset-2/c-to-cpp/c01-linux-win-network/source/uhttpd.c`；sourceSha256 `81400c36…8583`（与 manifest 逐字符一致）；形态 "uhttpd 1.7 单文件最小 Web 服务器，1318 行，含 main，带 Windows/Unix 两套可移植层"。
- sourceOs 候选 `linux`（由 `#ifdef UNIX` L150 + 预检诊断定案）；targetOs `linux`；arch x64；sourceRunnerId/targetRunnerId `linux-vm-agent-x64`。
- 模型：仅 `evaluation-freeze.md` L5 散文 "`.env` 模型 deepseek-flash 生成，非 Agent 代写"；目标声明 sha256 `acdebe45b27e18a6e168e3e41af1480bb7bf1d4c03cc97d05d8e7ca76c9a1d1f`（`target.cpp`，代码已删除，无法校验）。
- **选中知识/skill：全部现存件均无该字段**（未记录）。
- driver/oracle：`comparison_manifest.runCommand = python run_case.py`；oracle 表见 `evaluation-freeze.md` L36-44（三条 argv 的 stdout/exit/就绪证据）；驱动四要素核对见 L46-53。
- 冻结 cwd `workspace`；argv 见各 job；`timeoutSeconds` 30（job-00/01/02）、60（job-03/04）；`stdin: null`；`fixtures: []`；`environment: {}`；未冻结项：skill 选择、网络隔离批次级证据。
- `classification-1.json`：classifierVersion `2.3`；cls `REVIEW_NETWORK`；admissionStatus `ALLOWED`；blockingReason `null`；classifierSha256 `441b4d50125071544f6d1bbe836b7258d692c37c638acdb678a9e88795366524`；inputManifestSha256 `1979d5e4e0c6dbcefee44911a8f4001534fdf183be2cab6463d7bafb96d90e8e`；network_mode `mixed`；网络目标 `::`（L731，wildcard）、`255.255.255.255`（L732，special），均 `redirectVerified: false`；limitations 含 `isolation_and_authorization_not_assessed`、`target_driver_dependencies_not_assessed`。
- 无重分类尝试（只有 `classification-1.json`）。

### SOURCE PRECHECK
- job-00 `eval-20261010-054246-913f050b`（`job-status.json`）：os `linux`；构建命令 `gcc -std=gnu11 -DUNIX -pthread uhttpd.c -o program`；build `completed`/exit 0（178ms），stderr 空（空串 digest `e3b0c442…`）⇒ **无编译器诊断**（零警告零错误）；execution `completed`/exit 0，stdout `uhttpd version 1.7\n`（19B，digest `e6100429…`），stderr 空；argv `["-V"]`。
- 清理证据：`evaluation_report.json` 两侧 preflight/cleanup `PASSED`（attempts 1，failure null）、`contaminated: false`、`environmentStatus: clean`、`runnerStateAfter: READY`。
- 注意：job-00 的 `comparison_manifest.target.buildCommand` 是占位命令（`g++ … placeholder.txt -o program`），故 `job-status.json.lastError = {code CODE_RESULT, message "Target build failed."}`；`evaluation_report` 记 `runVerdict not-runnable`、`codeVerdict failed`、`behaviorVerdict inconclusive`。

### REQUESTS/RESPONSES
- **本项不存在任何 `request*.txt` / `repair*.txt` / `*.model.json`**（对整棵 `c-to-cpp` 树 glob 证实：这些文件仅 D2-151 拥有）。
- ⇒ 无可核对的 model name 字段、`finish_reason`、token usage、响应正文、parent/final hash；**没有真实响应体留存**。模型身份只出现在 `job-01/metadata.json` L12 与 `evaluation-freeze.md` L5 的散文里。
- 失败尝试只存在于 job 层：job-00 占位目标构建失败；job-03 空观察被判 matched（作废）；job-04 驱动失败被判 matched（作废）。

### SELF-REVIEW
- `self-review-1.json`：round 1，reviewer `agent-static`，verdict **`NO-REPAIR-IDENTIFIED`**。
- scope：与冻结源逐行 diff（1318 → 1316 行）；仅 2 处实质变更，均为 C++ 强制转换：L926 `pData->buf = realloc(...)` → `(char *) realloc(...)`；L1237 聚合初始化 `DEFAULT_PORT` 与 `"."` 外包 `(char *)`；另有尾随空行移除。
- risks/limitations：原文 "static review only; does not predict compilation and is not behaviour evidence. The network/listening behaviour is NOT verifiable by static review."
- unresolved：未列。
- knowledge suggestions：**无**（文件无相关字段）。
- repair：**无**（无 `target.self-repair-N.model.json`、无 proposal json）。

### JOBS
- job-00（见 SOURCE PRECHECK）：目标占位、未执行；返回 `evidence-source.json`（截断）+ `evaluation_report.json`；无 `comparison.json`。
- job-01 `eval-20261010-054621-4ceacc42`，argv `["-V"]`，timeout 30：source build `completed`/0，exec `completed`/0，stdout `uhttpd version 1.7\n`（digest `e6100429…`）；target build `completed`/0，exec `completed`/0，stdout **同一 digest**；`comparison.json` `behaviorVerdict=matched`，output `matched`/`applicable`/`observed`/`diffs: []`，其余维度 `not-applicable`；`evaluation_report` `runnable/passed/matched`，coverage 1/1，ratio 1.0；清理 PASSED、未污染、READY；`job-status` lastError null。
- job-02 `eval-20261010-054747-08be4dc8`，argv `["-z"]`：两侧 build `completed`/0；两侧 exec `completed`/**exit 1**，stdout 为 `uhttpd: Usage …` SYNTAX 文本（前 2000 字符可见，尾部/`sizeBytes` 不可读）；`comparison` `matched`，`diffs: []`；report `runnable/passed/matched` coverage 1.0。
- job-03 `eval-20261010-054915-86cb2697`，argv `["-i","127.0.0.1","-p","18080","-d","."]`，timeout 60：两侧 build `completed`/0；两侧 exec `completed`/**exit 0**，**stdout 0B（sizeBytes 0，空串 digest `e3b0c442…`）、stderr 0B**；平台 `comparison` 仍 `behaviorVerdict=matched`、`diffs: []`、coverage 1.0；`attribution.md` 判定为**装置缺陷假阳性**：驱动 `Popen(stdout=PIPE,stderr=PIPE)` → 轮询端口 → `sleep(1)` → `terminate()` → **之后**才 `communicate()`，服务非 tty 下全缓冲 stdout 未 flush 而永久丢失；并指出"端口可连接"不能替代 oracle 要求的日志行；本次 job 作废、记 UNVERIFIED；清理 PASSED、未污染。
- job-04 `eval-20261010-055115-367d73e1`，argv 同 job-03：`metadata.supersedes` 指向 job-03；驱动改为存活期后台读线程、就绪判据为字面 banner、失败 exit 97 打 `DRIVER-FAILURE`。实测两侧 exec `completed`/exit 0，stdout 0B，**stderr 均为 `DRIVER-FAILURE: readiness banner was never observed\n`（52B，两侧同一 digest `c777f9f2…`）**；平台 `comparison` 仍 `matched`、`diffs: []`、coverage 1.0；`evaluation_report` `COMPLETED/FINISHED`、`runnable/passed/matched`、cleanup PASSED、未污染、READY；但 `job-status.json` 仍 `RUNNING/CLEANING`（message "comparison evaluation starting"），`controller.log` 缺 finished 行。`attribution.md` 记 UNVERIFIED，并记一条平台行为事实：比较器无法区分"两侧行为相同"与"两侧都没观察到行为"。
- 计数核对：5 个 job 目录（00/01/02/03/04）；item json `usage.requests = 1`（仅 job-01 之前的 1 次转换调用），repair 0。

### RESULT/DELIVERY
- `result.md`：**不存在**。`evaluator_manifest.json`：**不存在**。
- 因此本项没有交付层自述可对照；唯一收口记录是 `batch/items/D2-024.json`（lifecycle DONE / phase CLOSED）+ 各 job 证据。item json 的 `verdicts` 声称 "targetBuild PASS / execution both sides executed on all three frozen paths / comparison version matched, usage matched, listen UNVERIFIED"，其中 "all three paths executed" 与本项 JSON 自身 `behaviorEvidence[2].accepted=false`（loopback UNVERIFIED）**互相矛盾**。

### ANOMALIES
- DONE 项缺 `result.md` 与 `evaluator_manifest.json`（交付完整性门禁在本副本无落盘证据）。
- job-04 `job-status.json` 停在 `RUNNING/CLEANING`，`controller.log` 无 finished 行 ⇒ **未确认终态清理**；其 report 却称 cleanup PASSED。
- 平台在 job-03（两侧全空）、job-04（两侧同一驱动失败标记）均记 `matched`、`diffs: []`、coverage 1.0 ⇒ **空观察/装置失败产物被判一致**；case 自身归因将其降为 UNVERIFIED（平台原判定保留未改写，符合纪律）。
- item json 内部矛盾：`verdicts.execution` 全路径已执行 vs `behaviorEvidence` loopback UNVERIFIED。
- job-00 因占位目标构建失败而带 `CODE_RESULT`/not-runnable，但 item json `sourcePrecheck` 只记源侧 `completed/0`，未提目标占位失败。
- 目标 sha256 `acdebe45…` 无法校验（目标代码已删除）。
- "847B SYNTAX" 只在 item json 出现，证据前缀不含 sizeBytes（不可读尾部）。
- job-00 无 `job-id.txt`（jobId 仅存于 `job-status.json`），而 chain-reactor 同类 job 有 `job-id.txt` ⇒ 跨项形制不一致。
- 单行 bundle 截断（17 件 `read(trunc>2000)`）。

### INDEPENDENT EVIDENCE FACTS
- 原件支持：源与目标在 linux 上均 build `completed`/exit 0（源 `gcc -std=gnu11 -DUNIX -pthread`，目标 `g++ -std=gnu++17 -DUNIX -pthread`）；argv `-V` 两侧 stdout 逐字节同 digest `e6100429…`、exit 0；argv `-z` 两侧 exit 1 且 SYNTAX 文本前缀相同；loopback argv 两侧 stdout/stderr 为 0B（job-03）或仅含驱动自身 `DRIVER-FAILURE`（job-04，两侧同 digest）；所有终态 report 的 preflight/cleanup `PASSED`、`contaminated:false`、`runnerStateAfter: READY`；`controller-health`/`runners` 显示 3 个 runner 均 READY。
- 原件**不支持**："服务监听正常"、"真实网络等价"、"两个网络目标不是连接目标"（源文本已删除，属模型断言）、"目标代码正确"（目标文本已删除）。

### ATTRIBUTION
- **conversion-introduced**：未确立（无任何目标侧缺陷证据）。
- **environment**：平台比较器在空观察/装置失败产物上给出 `matched`（平台行为，非代码行为）。
- **apparatus**：驱动在 `terminate()` 之后才读流（全缓冲 stdout 丢失）；就绪判据未采到 banner；job-00 使用占位目标树。
- **source-existing**：分类器两条网络字面量是源事实；但"它们是日志格式化常量、全文无 connect()"是对**已删除源文本**的断言 ⇒ 本审阅**undetermined**。
- **undetermined**：loopback 监听路径的真实等价性（从未取得合法观察）。

### KNOWLEDGE
- 候选规则：（a）常驻服务必须在存活期读取 stdout/stderr；就绪判据必须是冻结 oracle 声明的观察量，不得以"端口可连接"代替；全缓冲 C stdout 不得在 `terminate()` 后再 `communicate()`。（b）平台 `matched` 只有在**源侧观察非空且非退化**时才可用作证据；两侧同时空输出或两侧同为装置失败标记时必须降级。（c）项记录一致性检查：`verdicts.execution` 不得与 `comparison` 的 UNVERIFIED 自相矛盾。
- 当前契约是否已覆盖：（a）**已覆盖原则**——`AGENTS.md` 转换任务执行约束 §3「驱动四要素」（按冻结 argv 启动／到达被观察状态／采集真实 stdout-stderr-退出码-副作用／终止并收尾）并明确"启动后等它自己退出不是通用驱动"。（b）相邻——`AGENTS.md` §5「结论分层，不合成单一成功率」；case 引用的具体条目是批次纪律 `batch/operational-discipline.md` §10.6，**本审阅未读该文件 ⇒ 覆盖情况未核**。（c）**未覆盖**（本审阅所读文件中无对应条款）。
- 自审错误建议：**无**（self-review 判 NO-REPAIR-IDENTIFIED 且自限范围恰当，无可指摘之处；不存在需要否定的 knowledge 建议）。

### OPTIMIZATION
- 去噪/统计：把 4 个字段完全相同的 job 头（input_profile/metadata/comparison_manifest）集中，减少逐件重复；把作废 job（03/04）与有效 job 分区，避免 coverage 把作废件计入"已取得事件"。
- 过程：每个 job 目录强制 `job-status.json` 收敛到终态并保留 finished 日志行；目标占位预检应显式标 `precheck` 且与其 `CODE_RESULT` 分开记账。
- 评估：提交前加"源侧观察非空且非退化"机器可检门禁；对常驻服务强制"存活期采集"驱动形态并记录驱动版本/哈希。
- 交付：对单行 >2000 字符的证据件在 coverage 标注"尾部不可读"，避免下游把缺失字段当作不存在。

### UNKNOWNS
- 目标 `target.cpp` 文本与 sha `acdebe45…` 的真实内容（已删除）。
- 所有单行 bundle 2000 字符之后的字段（cleanupRecords、artifactDigests、collectorDiagnostics、`-z` 的 sizeBytes/digest）。
- 是否曾真实覆盖任何 HTTP 请求—响应路径（否）。
- "847B SYNTAX" 是否准确。
- 本项是否曾选择/加载任何知识页（全部现存件均无记录）。

---

## D2-025 ｜ dir=`c-to-cpp/chain-reactor-network-linux` ｜ 49 件

### IDENTITY
- taskId `D2-025`；direction `c-to-cpp`；源文件 `driver.c`（40 行）；Sha256 `FF710E0E6689D84FA4E1C8789270AAC1339D121BAAD097B240669BCFEB6B1DA6`。
- manifest：Kind `REUSE`；Origin `dataset/c-to-cpp/chain-reactor-network-linux`；JobId `eval-20260928-123304-add87d9d`；Evidence `dual-build-PASS (inherited)`。
- item json：kind `REUSE`；casePath `docs/test/dataset-2/c-to-cpp/chain-reactor-network-linux`；disposition `FROZEN`；phase `CLOSED`；lifecycle `DONE`；`pendingAction: null`；`blockingReasons: []`；`usage.requests: 2`（1 次初始转换 + 1 次定位后定向修复，"no blind re-asking"）；`codeRevisions: 2`；`selfRepairRounds: 1`；含 `targetSha256` 五文件映射、`evaluation`（matched/0 diffs/sourceStdoutDigest sha256:bcc282e5）、`correction`、`coverageGaps`。

### FILE INVENTORY（全部 49 件；基准 `docs/dataset-2/dataset-2-copy/c-to-cpp/chain-reactor-network-linux/`）
```
output/batch/01-frozen/classification-1.json=read
output/batch/01-frozen/CORRECTION-D2-025.md=read（更正记录，保留原判）
output/batch/01-frozen/classifier-input.json=read
output/batch/01-frozen/frozen-inputs.md=read（仍载原始 SOURCE_DEPENDENCY_GAP 判定）
output/batch/03-self-review/self-review-1.json=read
output/batch/04-evaluation/job-00-source-buildability/input_profile.json=read
output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json=read
output/batch/04-evaluation/job-00-source-buildability/metadata.json=read
output/batch/04-evaluation/job-00-source-buildability/job-id.txt=read
output/batch/04-evaluation/job-00-source-buildability/controller-health-before.json=read
output/batch/04-evaluation/job-00-source-buildability/runners-before.json=read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/comparison.json=read（comparison_not_found）
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/controller.log=read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json=read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/input_profile.json=read
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/comparison_manifest.json=read（目标命令 .c/.cpp 混写）
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/metadata.json=read
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/job-id.txt=read
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/returned-evidence/evaluation_report.json=read
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-02-dual-build/input_profile.json=read
output/batch/04-evaluation/job-02-dual-build/comparison_manifest.json=read
output/batch/04-evaluation/job-02-dual-build/metadata.json=read
output/batch/04-evaluation/job-02-dual-build/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-02-dual-build/returned-evidence/controller-health-after.json=read
output/batch/04-evaluation/job-02-dual-build/returned-evidence/controller.log=read
output/batch/04-evaluation/job-02-dual-build/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-02-dual-build/returned-evidence/evaluation_report.md=read
output/batch/04-evaluation/job-02-dual-build/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-02-dual-build/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-02b-contract-corrected/input_profile.json=read
output/batch/04-evaluation/job-02b-contract-corrected/comparison_manifest.json=read
output/batch/04-evaluation/job-02b-contract-corrected/metadata.json=read
output/batch/04-evaluation/job-02b-contract-corrected/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-02b-contract-corrected/returned-evidence/evaluation_report.json=read
output/batch/04-evaluation/job-02b-contract-corrected/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-02b-contract-corrected/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-03-dual-build-self-repair-1/input_profile.json=read
output/batch/04-evaluation/job-03-dual-build-self-repair-1/comparison_manifest.json=read
output/batch/04-evaluation/job-03-dual-build-self-repair-1/metadata.json=read
output/batch/04-evaluation/job-03-dual-build-self-repair-1/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-03-dual-build-self-repair-1/returned-evidence/controller-health-after.json=read
output/batch/04-evaluation/job-03-dual-build-self-repair-1/returned-evidence/controller.log=read
output/batch/04-evaluation/job-03-dual-build-self-repair-1/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-03-dual-build-self-repair-1/returned-evidence/evaluation_report.md=read
output/batch/04-evaluation/job-03-dual-build-self-repair-1/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-03-dual-build-self-repair-1/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/result.md=read
```
- 无 `evaluator_manifest.json`；无任何 `request*.txt` / `*.model.json` / `repair*` / `target.self-repair-*.model.json` / proposal json。

### FREEZE/CLASSIFY
- `frozen-inputs.md` L4-5：sourcePath `docs/test/dataset-2/c-to-cpp/chain-reactor-network-linux/source/driver.c`；sha `ff710e0e…1da6`；形态 "带 main 的 C 程序（40 行），argv 收端口并连接硬编码 loopback"，并引源注释 "Case-private loopback-only entry. This is not an upstream Chain Reactor file."。
- sourceOs `linux`（候选）/ targetOs `linux` / arch x64；runner `linux-vm-agent-x64`（两侧）。
- **L17 起的源侧预检结论为 `SOURCE_DEPENDENCY_GAP`（后经 `CORRECTION-D2-025.md` 判为错误，实为打包缺口）**；L36-37 原终态为"跳过、0 模型调用、UNVERIFIED"，与实际后续（2 次模型调用、matched）冲突。
- 模型：仅散文，`job-02/metadata.json` L12 `"deepseek-flash (project .env model); agent did not author target code"`；`result.md` L5 同述。**未记录 skill 选择。**
- driver/oracle：`run_case.py`；oracle 依据 `job-02/metadata.json` L30（源侧预检观察到 exit 1 + ANSI 红字 + `CASE_SEND_RESULT=-1`）；cwd `workspace`；argv `["1"]`（全部 input_profile）；stdin null；timeout 30；`fixtures: []`；`environment: {}`。
- `classification-1.json`：v2.3；cls `REVIEW_NETWORK`；admissionStatus `ALLOWED`；blockingReason `null`；classifierSha256 `441b4d50…6524`；inputManifestSha256 `c8875b82…01e6`；network_mode `loopback`；唯一目标 `127.0.0.1`（L13）。无重分类文件。

### SOURCE PRECHECK
- job-00 `eval-20261010-045206-ef979ba3`：`gcc -std=c11 driver.c -o program` → build `failed`/exit 1，诊断原文 `driver.c:3:10: fatal error: atoms.h: No such file or directory`（stderr 141B，digest `33b59403…`）；exec `blocked`，stderr `build failed`；`evaluation_report` `COMPLETED` 但 `jobPhase RUNNING_SOURCE`、`runVerdict blocked`、`codeVerdict inconclusive`、target `execution.performed:false`/preflight SKIPPED；cleanup PASSED、未污染、READY。
- job-01b `eval-20261010-052456-b9ec0f0e`（补齐 5 件伴随文件后重跑）：`gcc -std=gnu11 driver.c networking_quarks.c util.c -o program` → build `completed`/exit 0（271ms，无诊断）；exec `completed`/**exit 1**，stdout 78B，digest `4377a481…`，内容为 `\u001b[31m\t\tconnect_socket failed: 111, Connection refused\n\u001b[0mCASE_SEND_RESULT=-1\n`（ANSI 红/复位保留）；stderr 空。report：`not-runnable` / `codeVerdict failed` / target build failed（目标树当时为占位）；cleanup PASSED、未污染、READY。

### REQUESTS/RESPONSES
- **不存在任何请求/响应件** ⇒ 2 次模型调用（初始转换 + 修复）**没有** model name 字段、`finish_reason`、token usage、响应正文、parent/final hash。
- 修复的 provenance（模型产出、"仅新增一对花括号"）仅存在于散文：`job-03/metadata.json` L6、`result.md` L61-77、`batch/items/D2-025.json` 的 `evaluation.repair`。
- 失败尝试（job 层）：job-02 目标构建失败（6 处 `cast … loses precision` + 1 处 `jump to case label crosses initialization`）；job-02b 加 `-fpermissive` 后 6 处降为 warning，真错误仍在；另有流程层错误判定 `SOURCE_DEPENDENCY_GAP`（见 `CORRECTION-D2-025.md`）。

### SELF-REVIEW
- `self-review-1.json`：verdict **`NO-REPAIR-IDENTIFIED`**；basis "line-by-line diff of all five emitted files against the frozen complete source tree"。
- perFile：`driver.cpp` 40 行 0 diff；`atoms.h` 116 行 0 diff；`networking_quarks.cpp` 559 行 0 diff；`util.cpp` 227 行 **1 diff**（`argv = calloc(...)` → `argv = (char**)calloc(...)`）；`util.h` 81 行 0 diff。
- risks/limitations：原文 "static review only; not compilation and not behaviour evidence"；`byteDifferenceExplanation` 归因于 CRLF→LF。
- unresolved：未列。knowledge suggestions：**无**。
- repair：**无任何 repair 模型/提案文件**；修复后的目标文本亦不在本副本。

### JOBS
- job-02 `eval-20261010-070936-3a96928e`（`job-02-dual-build`）：source build `completed`/0、exec exit 1、stdout 78B digest `4377a481…`；target build **failed**/exit 1，stderr 含 `warning: option '-Wpointer-to-int-cast' is valid for C/ObjC but not for C++ [-Wpragmas]` + 6 处 `error: cast from … loses precision [-fpermissive]` + `jump to case label … crosses initialization`；`comparison.json`：全部维度 `not-applicable`，`behaviorVerdict inconclusive`；`evaluation_report`：`not-runnable`/`failed`/`inconclusive`，coverage 0，failure `CODE_RESULT → Target build failed`；`controller.log` created+finished；`controller-health-after` 3/3 READY，`evaluation_report.md` = FAIL/INCONCLUSIVE/CLEAN。
- job-02b `eval-20261010-071140-e3dbc38e`（契约分离实验，加 `-fpermissive`）：source build 0/exec exit 1 同 digest；target build 仍 **failed**/exit 1，但 6 处 cast 降为 `warning`，仅剩 case-label 错误；comparison 全 `not-applicable`/inconclusive；report `not-runnable/failed/inconclusive`。
- job-03 `eval-20261010-071402-4648fac9`（修复后）：source build 0/exec exit 1、stdout 78B digest `4377a481…`；target build **completed/0**（971ms，仅 warnings）；`comparison.json` `behaviorVerdict matched`，output applicable/observed/matched，`diffs: []`；`evaluation_report` `runnable/passed/matched`，coverage 1/1，ratio 1.0；`evaluation_report.md` PASS/MATCHED/CLEAN；cleanup PASSED、未污染、READY；`controller-health-after` 3/3 READY。
- 计数核对：5 job 目录；item json 记 requests 2 / codeRevisions 2 / selfRepairRounds 1；result.md 记 4 个 jobId（含预检）。

### RESULT/DELIVERY
- `result.md` 存在（96 行）。claims：交付完整性"完成（五个文件 + 驱动 + 清单齐备，证据 7 份落盘）"；目标侧语法/编译 PASS（经 1 轮修复，`g++ -std=gnu++17 -fpermissive …` → completed/0）；源侧基线 PASS（`gcc -std=gnu11 …` → completed/0、exec 1）；执行两侧 exit 1；行为一致性 `matched`（output diffs=0，stdout digest 两侧相同，含 ANSI）；环境 clean；安全 ALLOWED。
- 与证据对照：`matched`/0 diffs/同 digest/双侧 exit 1/cleanup PASSED **有原件支持**；"五个文件 + 驱动 + 清单齐备、证据 7 份"**在本副本不可验证**（目标与驱动已删除，且无 `evaluator_manifest.json`）；`-fpermissive` 属契约修正的判断基于**已删除的源 pragma 文本**，本审阅不可复核。
- `evaluator_manifest.json`：**不存在**。

### ANOMALIES
- `frozen-inputs.md` 保留已被推翻的 `SOURCE_DEPENDENCY_GAP` 终态（跳过/0 调用/UNVERIFIED），与 item json（已更正、2 次调用、matched）并存 ⇒ 同一项内两套终态叙述。
- **哈希冲突**：item json `targetSha256` 记 `atoms.h F3CA4EC8…47F8`、`util.h 9E104B20…BC04`；`CORRECTION-D2-025.md` 表记 `atoms.h 6F453C93…0D33`、`util.h 5A412FA4…1BE7`；而 `driver.c`/`networking_quarks.c`/`util.c` 两处一致 ⇒ `atoms.h`/`util.h` 存在未解释的哈希不一致（原件不可得，无法定案）。
- `job-01b/comparison_manifest.json` 目标构建命令混写 `.c`/`.cpp`（`driver.cpp networking_quarks.c util.c`）。
- `job-00/evaluation_report.json` 为 `COMPLETED` 但 `jobPhase RUNNING_SOURCE`（非终态字面）。
- 无请求/响应/修复件 ⇒ 修复链不可审计。
- `result.md` 的交付完整性断言不可验证；单行 bundle 截断 13 件。

### INDEPENDENT EVIDENCE FACTS
- 源侧在补齐伴随文件后 `gcc -std=gnu11 driver.c networking_quarks.c util.c` build `completed`/0，运行 exit 1 且 stdout 78B digest `4377a481…`（ANSI 红字 + `CASE_SEND_RESULT=-1`）。
- 目标首版构建失败诊断真实存在：C++ 下 `-Wpointer-to-int-cast` pragma 无效（warning），6 处指针→int 转换成为 **error**，并另有 `jump to case label crosses initialization` 错误。
- 加 `-fpermissive` 后 6 处降为 warning，**真错误仍在** ⇒ 该标志未掩盖 case-label 缺陷（这一因果由两份 target stderr 原文支持）。
- 修复后目标 build `completed`/0；最终 `comparison` matched、`diffs: []`，源/目标 stdout digest 相同；所有终态 report cleanup PASSED、未污染、READY。
- **不支持**：socketcall 路径行为、成功连接路径、argv 非 1 的路径（均未执行）；目标与修复后文本（已删除）。

### ATTRIBUTION
- **conversion-introduced**：`networking_quarks.cpp` 的 `int status` 被 `case -1:` 跨越初始化（真实 C→C++ 适配缺陷，由编译器诊断定位后由模型修复）。
- **source-existing**：源自带 pragma 与 ANSI 颜色输出。
- **environment**：本项未观察到环境失败（两侧 runner READY、未污染）。
- **apparatus**：首次打包缺口（5 件伴随文件未随 capsule 携带）；job-00 占位目标预检；`job-01b` 命令混写。
- **undetermined**：`atoms.h`/`util.h` 哈希不一致的成因；socketcall 路径等价性。

### KNOWLEDGE
- 候选规则：（1）C→C++ 中 `switch` 体内声明、后续 `case` 标签跨初始化 ⇒ 必须加花括号作用域；"jump to case label crosses initialization" 是**代码缺陷**，不得用 `-fpermissive` 掩盖。（2）当 C 源自带 `#pragma GCC diagnostic ignored "-Wpointer-to-int-cast"`（C++ 下非法警告名）时，用 `-fpermissive` 表达同一意图属**契约修正**；但必须验证"真错误仍在"以证明未掩盖。（3）宣布"快照外文件"前必须先查该 case 在旧 dataset 中的完整源树。
- 当前契约覆盖情况：（3）**规则早已存在且被违反**——`CORRECTION-D2-025.md` L9-11 引 `references/workflow/build-prerequisites.md` 原文，其中**以 D2-025 本身为打包缺口先例** ⇒ 属执行违规而非规则缺失；`AGENTS.md` §3 源侧预检（"源构建失败按真实诊断处理"）覆盖诊断定案与 SOURCE_DEPENDENCY_GAP / SOURCE_NOT_BUILDABLE 分列。（1）（2）属方向知识，本审阅未读 `skills/directions/c-to-cpp/SKILL.md`，覆盖未核。
- 需**否定的自审建议**：无（self-review 未提出建议；其 NO-REPAIR 判定与"缺陷只由编译器暴露"的事实一致，符合 `AGENTS.md` §3「自审是正常推进信号，不是防线」）。

### OPTIMIZATION
- 过程：修复必须落盘请求/响应（本项缺失），并记目标提交哈希清单以供交叉校验。
- 数据一致性：统一 `frozen-inputs.md` 的终态与 item 终态（或明确标注"原始记录，已由 CORRECTION 取代"），避免同一项两套终态。
- 统计：把"作废/中间 job"与"终态 job"分列；把预检 job 的占位目标失败与源侧结论分开计数。
- 交付：`result.md` 的"证据 7 份"类计数应由 `evaluator_manifest.json` 机读支撑。

### UNKNOWNS
- 修复请求/响应原文与修复 diff（未留存）。
- `atoms.h`/`util.h` 两套哈希孰为真（原件不可得）。
- socketcall/成功连接/非 1 argv 路径行为。
- 本项 skill 选择是否发生（无记录）。

---

## D2-027 ｜ dir=`c-to-cpp/pwd-fs-posix-to-win` ｜ 28 件

### IDENTITY
- taskId `D2-027`；direction `c-to-cpp`；源文件 `pwd.c`；manifest `Lines=124`；Sha256 `CF8B57F4B95ABF55F7C64446686126202756411B64370751FFB21F0DE93D3F68`。
- manifest：Kind `REUSE`；Origin `dataset/c-to-cpp/pwd-fs-posix-to-win`；JobId `eval-20260928-064021-653f5ee9`；Evidence `dual-build-PASS (inherited)`。
- item json：kind `REUSE`；casePath `docs/test/dataset-2/c-to-cpp/pwd-fs-posix-to-win`；disposition `SOURCE_NOT_BUILDABLE`；phase `CLOSED`；lifecycle `DONE`；`pendingAction: null`；`blockingReasons: []`；`usage.requests: 0`（"skipped at the source-precheck gate"）；`codeRevisions: 0`；`selfRepairRounds: 0`；`sourcePrecheck` 含 experimentA/B/C 三段。

### FILE INVENTORY（全部 28 件；基准 `docs/dataset-2/dataset-2-copy/c-to-cpp/pwd-fs-posix-to-win/`）
```
case.md=read（自称 FROZEN，内容与实测相左）
output/batch/01-frozen/classification-1.json=read
output/batch/01-frozen/classifier-input.json=read
output/batch/01-frozen/frozen-inputs.md=read
output/batch/04-evaluation/job-00-source-buildability/input_profile.json=read
output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json=read
output/batch/04-evaluation/job-00-source-buildability/metadata.json=read
output/batch/04-evaluation/job-00-source-buildability/job-id.txt=read
output/batch/04-evaluation/job-00-source-buildability/controller-health-before.json=read
output/batch/04-evaluation/job-00-source-buildability/runners-before.json=read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/comparison.json=read（comparison_not_found）
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/controller.log=read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json=read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-00b-source-buildability-linux/input_profile.json=read
output/batch/04-evaluation/job-00b-source-buildability-linux/comparison_manifest.json=read
output/batch/04-evaluation/job-00b-source-buildability-linux/metadata.json=read
output/batch/04-evaluation/job-00b-source-buildability-linux/job-id.txt=read
output/batch/04-evaluation/job-00b-source-buildability-linux/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-00b-source-buildability-linux/returned-evidence/controller.log=read
output/batch/04-evaluation/job-00b-source-buildability-linux/returned-evidence/evaluation_report.json=read
output/batch/04-evaluation/job-00b-source-buildability-linux/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-00c-source-buildability-linux-posix-macro/input_profile.json=read
output/batch/04-evaluation/job-00c-source-buildability-linux-posix-macro/comparison_manifest.json=read
output/batch/04-evaluation/job-00c-source-buildability-linux-posix-macro/metadata.json=read
output/batch/04-evaluation/job-00c-source-buildability-linux-posix-macro/job-id.txt=read
output/batch/04-evaluation/job-00c-source-buildability-linux-posix-macro/returned-evidence/evaluation_report.json=read
output/batch/04-evaluation/job-00c-source-buildability-linux-posix-macro/returned-evidence/evidence-source.json=read(trunc>2000)
```
- `03-self-review/`=missing；`result.md`=missing；`evaluator_manifest.json`=missing；无 `request*.txt`/`*.model.json`/`controller.log`（job-00c）。

### FREEZE/CLASSIFY
- `frozen-inputs.md` L4-5：sourcePath `…/source/pwd.c`；sha `cf8b57f4…3f68`；形态 "BSD userland pwd 实现（124 行，带 main，使用 getopt 与 err/warn）"；L7 "sourceOs 候选：windows 与 linux 两个候选都实测过"。
- sourceOs：两候选均实测（windows 失败于 err.h；linux 失败于 `__dead2`）；targetOs 未取得（未提交）。
- 模型：**全件未命名**（0 次调用）；`case.md` 声明 sourceOs linux / targetOs windows x64、源侧命令 `gcc -std=gnu11 -D_GNU_SOURCE -D_DEFAULT_SOURCE source.c -o program`、目标 `g++ -std=c++17 target.cpp -o program.exe`（**均未实际使用**）。
- **未记录 skill 选择。**
- driver/oracle：`run_case.py`；cwd `workspace`；argv `[]`；stdin null；timeout 30（三份 input_profile 相同）。
- `classification-1.json`：v2.3；cls `REVIEW_SIDE_EFFECTS`；admissionStatus `ALLOWED`；blockingReason `null`；classifierSha256 `441b4d50…6524`；inputManifestSha256 `6461a3b0…76cd`；network_mode `none-detected`；reviewGroups `["discovery"]`（信号行 114）。无重分类文件。

### SOURCE PRECHECK
- 实验 A `job-00` / `eval-20261010-045333-613b447e`（windows runner `windows-vm-agent-x64`，snapshot `CC-Eval-Windows-8Lang-1.0.26`）：`gcc -std=c11 pwd.c -o program.exe` → build `failed`/exit 1；诊断 `pwd.c:48:10: fatal error: err.h: No such file or directory`（134B，digest `ed3617f8…`）；exec `blocked`；report `COMPLETED`/`jobPhase RUNNING_SOURCE`/`runVerdict blocked`，target preflight SKIPPED；cleanup PASSED、未污染、READY；`comparison.json`=`{"detail":"comparison_not_found"}`。
- 实验 B `job-00b` / `eval-20261010-045427-cbdbe0d2`（linux）：`gcc -std=c11 pwd.c -o program` → build `failed`/exit 1；3 条诊断：`pwd.c:65:22 implicit declaration of 'getopt'`、`pwd.c:77:17 'optind' undeclared`、`pwd.c:97:1 expected '=', ',', ';', 'asm' or '__attribute__' before 'usage'`（627B，digest `371fe5a7…`）；**未报 err.h 缺失**；cleanup PASSED、未污染、READY。
- 实验 C `job-00c` / `eval-20261010-045513-56eaab84`（linux，改用 `-std=gnu11`）：`gcc -std=gnu11 pwd.c -o program` → build `failed`/exit 1；仅剩 `pwd.c:97:1: error: expected '=', ',', ';', 'asm' or '__attribute__' before 'usage'`（141B，digest `9979ad84…`）；结论 `SOURCE_NOT_BUILDABLE`（`__dead2` 为 FreeBSD 专有宏）；cleanup PASSED、未污染、READY。
- 三份 report 均为 `jobPhase RUNNING_SOURCE`（非终态字面）但 `jobStatus COMPLETED`；`job-00c` **无 `controller.log`、无 `comparison.json`**。

### REQUESTS/RESPONSES
- **无任何请求/响应件**（0 次模型调用）⇒ 无 model name、`finish_reason`、usage、正文、hash。失败尝试即三次构建实验（A/B/C），均按真实诊断记。

### SELF-REVIEW
- **不存在**（无 `03-self-review` 目录/文件）；与 `usage.requests 0` 一致。

### JOBS
- 3 个 job 目录，全部为源侧预检，目标从未构建/运行：
  - job-00：windows、err.h 缺失、构建失败；controller.log created+finished。
  - job-00b：linux `-std=c11`、POSIX 声明契约缺陷（getopt/optind）+ `__dead2`；controller.log created+finished。
  - job-00c：linux `-std=gnu11`、仅剩 `__dead2`；无 controller.log。
- 无 comparison 结果（三次均为 `comparison_not_found`），无目标侧证据（`evidence-target.json` 全部 missing）。

### RESULT/DELIVERY
- `result.md`：**不存在**。`evaluator_manifest.json`：**不存在**。
- 唯一收口记录为 `batch/items/D2-027.json`（`SOURCE_NOT_BUILDABLE` / DONE / requests 0）与 `frozen-inputs.md`。

### ANOMALIES
- `case.md` L12 "LF 物理行 123"、3278 字节 vs manifest `Lines=124` vs `frozen-inputs.md` "124 行" ⇒ **行数/字节口径不一致**。
- `case.md` L26-27 声明的构建命令（`-D_GNU_SOURCE -D_DEFAULT_SOURCE source.c`、`target.cpp -o program.exe`）与实际预检命令（`pwd.c`、`-std=c11`/`-std=gnu11`）**不一致**；`case.md` L37 "源侧 Linux 可构建（待预检验证）" 与本项 `SOURCE_NOT_BUILDABLE` 终态**相左**（陈旧契约）。
- `case.md` 预先判定 sourceOs=linux/targetOs=windows，与"只由编译器诊断定案、画像只给候选"的口径相冲突，也与实际双候选实验相左。
- `job-00c` 缺 `controller.log`/`comparison.json`（同批 job-00/00b 均有）⇒ 取证形制不一致。
- 三份 report 的 `jobPhase RUNNING_SOURCE` 与 `jobStatus COMPLETED` 并存。
- 三件 `evidence-source.json` 单行截断。
- **macOS 未实测**（已登记系统含 macos × x64），故"__dead2/err.h 在所有已登记系统均缺"未被本项诊断覆盖。

### INDEPENDENT EVIDENCE FACTS
- windows runner 上 `gcc -std=c11 pwd.c` 在 `#include <err.h>` 处致命失败 ⇒ 该 runner 无 `err.h`。
- linux runner 上 `gcc -std=c11 pwd.c` 报 getopt/optind 未声明 + `usage` 声明破坏；换 `-std=gnu11` 后前两条消失，**仅剩第 3 条**（`__dead2` 未定义导致的声明破坏）。
- 目标侧从未构建或运行；所有 report cleanup PASSED、未污染、READY。
- **不支持**：macOS 行为；任何目标侧结论；任何"可构建"结论。

### ATTRIBUTION
- **source-existing**：BSD userland 源依赖未登记系统接口（`__dead2`、`err.h`）。
- **environment**：windows/linux 工具链缺 `err.h`/`__dead2`；`-std=c11` 严格模式不暴露 POSIX 声明（属命令契约，已修正）。
- **apparatus**：`case.md` 陈旧契约（行数、命令、OS 预判、可构建结论）；`job-00c` 缺 controller.log；`RUNNING_SOURCE` 相位标签。
- **conversion-introduced**：无（未转换，0 调用）。
- **undetermined**：macOS 是否可构建。

### KNOWLEDGE
- 候选规则：判 `SOURCE_NOT_BUILDABLE` 前应遍历**全部已登记候选 sourceOs（含 macos）**，不得只测 windows/linux 就断言"所有已登记系统均缺该接口"；`case.md` 的契约字段（行数/命令/OS）应由实测证据生成并回写，避免陈旧断言与被自身证据推翻的结论并存。
- 当前契约覆盖：`AGENTS.md` 执行约束 §3 源侧预检明确"可构建性只由编译器诊断定案，源码画像只给候选 sourceOs，不设头文件探针"，已覆盖"诊断定案"与"画像只给候选"；但**未显式要求穷举全部候选 OS** ⇒ 属可补强点。`docs/dataset-2/dataset-2-copy/README.md` §8.2 已登记"部分 C 源为 BSD/FreeBSD userland … 在源侧预检会因缺少对应接口而不可构建，属源侧平台不匹配"⇒ 类别本身已在项目文档中。
- 需否定的自审建议：无（本项无自审）。

### OPTIMIZATION
- 过程：`case.md` 由证据反向生成（行数/命令/OS 均取实测值）；每次作业都产出 `controller.log`。
- 评估：决策树显式记录"已测 OS / 未测 OS"两列，使"未覆盖"不被读成"已覆盖"。
- 统计：把契约缺陷（命令可补齐）与平台不匹配（不可补齐）分列计数（本项已按 A/B/C 做到）。

### UNKNOWNS
- macOS 可构建性。
- `err.h`/`__dead2` 在其他已登记系统的实际可用性（仅 windows/linux 有实测）。
- 目标侧任何结论（从未尝试）。
- 124 vs 123 行、3278 字节的真实口径。

---

## D2-028 ｜ dir=`c-to-cpp/realpath-fs-posix-to-win` ｜ 9 件

### IDENTITY
- taskId `D2-028`；direction `c-to-cpp`；源文件 `realpath.c`（83 行）；Sha256 `179EC5EA1F7E6197C9ACF9785C4933A379FED0839FB788BE376EA8CAFF4DE889`。
- manifest：Kind `REUSE`；Origin `dataset/c-to-cpp/realpath-fs-posix-to-win`；JobId `eval-20260928-060834-49b1a302`；Evidence `dual-build-PASS (inherited)`。
- item json：kind `REUSE`；casePath `docs/test/dataset-2/c-to-cpp/realpath-fs-posix-to-win`；disposition `SOURCE_NOT_BUILDABLE`；phase `CLOSED`；lifecycle `DONE`；`pendingAction: null`；`blockingReasons: []`；`usage.requests: 0`；`codeRevisions: 0`；`selfRepairRounds: 0`；`sourcePrecheck.jobId = eval-20261010-045637-b2605908`。

### FILE INVENTORY（全部 9 件；基准 `docs/dataset-2/dataset-2-copy/c-to-cpp/realpath-fs-posix-to-win/`）
```
output/batch/01-frozen/classification-1.json=read
output/batch/01-frozen/classifier-input.json=read
output/batch/01-frozen/frozen-inputs.md=read
output/batch/04-evaluation/job-00-source-buildability-linux-contract-corrected/input_profile.json=read
output/batch/04-evaluation/job-00-source-buildability-linux-contract-corrected/comparison_manifest.json=read
output/batch/04-evaluation/job-00-source-buildability-linux-contract-corrected/metadata.json=read
output/batch/04-evaluation/job-00-source-buildability-linux-contract-corrected/job-id.txt=read
output/batch/04-evaluation/job-00-source-buildability-linux-contract-corrected/returned-evidence/evaluation_report.json=read
output/batch/04-evaluation/job-00-source-buildability-linux-contract-corrected/returned-evidence/evidence-source.json=read(trunc>2000)
```
- `case.md`=missing；`03-self-review/`=missing；`result.md`=missing；`evaluator_manifest.json`=missing；`controller.log`=missing；`comparison.json`=missing；无 `request*.txt`/`*.model.json`。

### FREEZE/CLASSIFY
- `frozen-inputs.md` L4-5：sourcePath `…/source/realpath.c`；sha `179ec5ea…e889`；形态 "BSD userland realpath 实现（83 行，带 main，使用 getopt/err/warn）"；L14 候选 sourceOs = `linux`。
- 模型：**未命名**（0 次调用）；**未记录 skill 选择**。
- driver/oracle：`run_case.py`；cwd `workspace`；**argv `["."]`**（虽然二进制从未构建成功）；stdin null；timeout 30；`fixtures: []`；`environment: {}`；L15 说明命令已预先采用 `-std=gnu11` 规避 D2-027 确认的 POSIX 特性宏契约缺陷。
- `classification-1.json`：v2.3；cls `LOW_SIGNAL`；reason `no_known_signal_detected_not_proven_safe`；admissionStatus `ALLOWED`；blockingReason `null`；classifierSha256 `441b4d50…6524`；inputManifestSha256 `751e4d05…4f18`；network_mode `none-detected`；reviewGroups `[]`。无重分类文件。

### SOURCE PRECHECK
- `job-00` / `eval-20261010-045637-b2605908`（linux，contract-corrected）：`gcc -std=gnu11 realpath.c -o program` → build `failed`/exit 1；诊断原文（519B，digest `e6d418cc…`）：
  `realpath.c:40:25: error: expected declaration specifiers before '__dead2'`（上下文 `static void usage(void) __dead2;`）、
  `realpath.c:44:1: error: expected '=', ',', ';', 'asm' or '__attribute__' before '{' token`、
  `realpath.c:78:1` 同型错误、
  `realpath.c:83: error: expected '{' at end of input`。
- **未报 `err.h` 缺失** ⇒ 该 linux runner 上 `err.h` 存在（与 D2-027 实验 B 一致）。
- report：`COMPLETED`、`jobPhase RUNNING_SOURCE`、`runVerdict blocked`、`codeVerdict inconclusive`，target `execution.performed:false`/preflight SKIPPED；cleanup PASSED、未污染、READY。

### REQUESTS/RESPONSES
- **无**（0 次模型调用）⇒ 无 model name/`finish_reason`/usage/正文/hash。失败尝试即这一次构建实验。

### SELF-REVIEW
- **不存在**（无自审文件）。

### JOBS
- 仅 1 个 job 目录（job-00，源侧预检）；目标从未构建/运行；无 `comparison.json`、无 `controller.log`、无 `evidence-target.json`。

### RESULT/DELIVERY
- `result.md`：**不存在**。`evaluator_manifest.json`：**不存在**。唯一收口记录为 item json（`SOURCE_NOT_BUILDABLE` / DONE / requests 0）。

### ANOMALIES
- 唯一 job 目录缺 `controller.log` 与 `comparison.json`（对比 D2-027 同型 job）。
- `evaluation_report` 为 `COMPLETED` 但相位字面 `RUNNING_SOURCE`。
- 在源码从未构建成功的情况下冻结了 argv `["."]`（无效契约字段）。
- 只测 linux 一个候选（无第二次实验），"__dead2 在所有已登记系统均无"的结论**未被 macOS 证据覆盖**。
- 单行 `evidence-source.json` 截断。

### INDEPENDENT EVIDENCE FACTS
- linux 上 `gcc -std=gnu11 realpath.c` 在 `static void usage(void) __dead2;` 处致命失败，并连带 3 条级联语法错误；无 `err.h` 缺失报错。
- 目标侧从未构建、从未运行；cleanup PASSED、未污染、READY。
- **不支持**：macOS 行为；任何目标侧结论；`-std=gnu11` 之外的契约变体是否可行（未测）。

### ATTRIBUTION
- **source-existing**：BSD 专有 `__dead2`（FreeBSD `<sys/cdefs.h>`）。
- **environment**：linux glibc 无该宏。
- **apparatus**：非终态相位标签；缺 controller.log；构建成功前即冻结 argv；未测 macOS。
- **conversion-introduced**：无。
- **undetermined**：macOS 是否可构建。

### KNOWLEDGE
- 候选规则：与 D2-027 同——穷举全部已登记候选 OS 后再断"平台不匹配"；构建成功前不得冻结运行 argv；单条宏导致的级联错误应归一为单一根因（本项已做到）。
- 当前契约覆盖：`AGENTS.md` §3 源侧预检（诊断定案、候选 sourceOs、失败不消耗调用）已覆盖；"穷举候选 OS"与"构建前不冻结 argv"未显式覆盖 ⇒ 补强点。`README.md` §8.2 已登记该类别。

### OPTIMIZATION
- 统一每个 job 必须含 `controller.log`；把 argv 冻结置于源构建成功之后；在记录中显式写出"未测 OS"清单。

### UNKNOWNS
- macOS 可构建性。
- 其他已登记系统上 `err.h`/`__dead2` 的实际可用性。
- 目标侧任何结论。

---

## D2-029 ｜ dir=`c-to-cpp/stest-fs-posix-to-win` ｜ 108 件

### IDENTITY
- taskId `D2-029`；direction `c-to-cpp`；源文件 `stest.c`（110 行）；Sha256 `BB943C3E2C228398C592E873BB31ABF18EFBA5C0F06C3BC39220443A7C7696BD`。
- manifest：Kind `REUSE`；Origin `dataset/c-to-cpp/stest-fs-posix-to-win`；JobId `eval-20260928-053745-2a386af5`；Evidence `dual-build-PASS (inherited)`。
- item json：kind `REUSE`；casePath `docs/test/dataset-2/c-to-cpp/stest-fs-posix-to-win`；disposition `FROZEN`；phase `CLOSED`；lifecycle `DONE`；`pendingAction: null`；`blockingReasons: []`；`usage.requests: 2`（"1 initial conversion + 1 functional-repair attempt that returned byte-identical code; the repair was unnecessary because there was no defect"）；`codeRevisions: 0`；`selfRepairRounds: 0`；含 `correction`（SOURCE_DEPENDENCY_GAP → 打包缺口）、`evaluation`（matched/0 diffs/frozenArgv `["fixture.txt"]`/supersededJobs 4 条）、`coverageGaps`、`corrections`（hit-predicate 缺陷判定为 WRONG）。

### FILE INVENTORY（全部 108 件；基准 `docs/dataset-2/dataset-2-copy/c-to-cpp/stest-fs-posix-to-win/`）
```
output/batch/01-frozen/classification-1.json=read
output/batch/01-frozen/CORRECTION-D2-029.md=read（更正：SOURCE_DEPENDENCY_GAP→打包缺口）
output/batch/01-frozen/classifier-input.json=read
output/batch/01-frozen/evaluation-freeze.md=read（评估条件冻结）
output/batch/01-frozen/frozen-inputs.md=read（保留首次错误判定 + 追加更正）
output/batch/03-self-review/self-review-1.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/comparison_manifest.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/input_profile.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/job-id.txt=read
output/batch/04-evaluation/job-00-source-buildability-linux/metadata.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evaluation_report.json=read
output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-01-dual-build/attribution.md=read（空观察 matched 假阳性）
output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json=read
output/batch/04-evaluation/job-01-dual-build/controller-health-before.json=read
output/batch/04-evaluation/job-01-dual-build/input_profile.json=read
output/batch/04-evaluation/job-01-dual-build/job-id.txt=read
output/batch/04-evaluation/job-01-dual-build/metadata.json=read
output/batch/04-evaluation/job-01-dual-build/runners-before.json=read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json=read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log=read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md=read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/comparison_manifest.json=read
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/input_profile.json=read
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/job-id.txt=read
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/metadata.json=read
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-01b-source-precheck-complete-tree/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-02-argv-exercised/comparison_manifest.json=read
output/batch/04-evaluation/job-02-argv-exercised/controller-health-before.json=read
output/batch/04-evaluation/job-02-argv-exercised/input_profile.json=read
output/batch/04-evaluation/job-02-argv-exercised/metadata.json=read
output/batch/04-evaluation/job-02-argv-exercised/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-02-argv-exercised/returned-evidence/controller-health-after.json=read
output/batch/04-evaluation/job-02-argv-exercised/returned-evidence/controller.log=read
output/batch/04-evaluation/job-02-argv-exercised/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-02-argv-exercised/returned-evidence/evaluation_report.md=read
output/batch/04-evaluation/job-02-argv-exercised/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-02-argv-exercised/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/attribution.md=read（"转换引入"归因，后被作废）
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/comparison_manifest.json=read
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/controller-health-before.json=read
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/input_profile.json=read
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/metadata.json=read
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/returned-evidence/controller-health-after.json=read
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/returned-evidence/controller.log=read
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/returned-evidence/evaluation_report.md=read
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-03-argv-exercised-fixed-driver/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-04-probe-dash-arg/comparison_manifest.json=read
output/batch/04-evaluation/job-04-probe-dash-arg/input_profile.json=read
output/batch/04-evaluation/job-04-probe-dash-arg/job-status.json=read
output/batch/04-evaluation/job-04-probe-dash-arg/metadata.json=read（自述"diagnostic probe, NOT a verdict job"）
output/batch/04-evaluation/job-04-probe-dash-arg/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-04-probe-dash-arg/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-04-probe-dash-arg/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-04-probe-dash-arg/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-05-precheck-path-reproduced/attribution.md=read（"转换引入"归因 + 未决现象）
output/batch/04-evaluation/job-05-precheck-path-reproduced/comparison_manifest.json=read
output/batch/04-evaluation/job-05-precheck-path-reproduced/input_profile.json=read
output/batch/04-evaluation/job-05-precheck-path-reproduced/job-status.json=read（仍 RUNNING/CLEANING）
output/batch/04-evaluation/job-05-precheck-path-reproduced/metadata.json=read
output/batch/04-evaluation/job-05-precheck-path-reproduced/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-05-precheck-path-reproduced/returned-evidence/controller-health-after.json=read（readyRunnerCount 2/3，busy:CLEANING）
output/batch/04-evaluation/job-05-precheck-path-reproduced/returned-evidence/controller.log=read（无 finished 行）
output/batch/04-evaluation/job-05-precheck-path-reproduced/returned-evidence/evaluation_report.json=read（job_report_not_found）
output/batch/04-evaluation/job-05-precheck-path-reproduced/returned-evidence/evaluation_report.md=read（job_human_report_not_found）
output/batch/04-evaluation/job-05-precheck-path-reproduced/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-05-precheck-path-reproduced/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-06-probe-bare-arg/attribution.md=read
output/batch/04-evaluation/job-06-probe-bare-arg/comparison_manifest.json=read
output/batch/04-evaluation/job-06-probe-bare-arg/input_profile.json=read
output/batch/04-evaluation/job-06-probe-bare-arg/job-status.json=read
output/batch/04-evaluation/job-06-probe-bare-arg/metadata.json=read
output/batch/04-evaluation/job-06-probe-bare-arg/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-06-probe-bare-arg/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-06-probe-bare-arg/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-06-probe-bare-arg/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-07-probe-flag-a/comparison_manifest.json=read
output/batch/04-evaluation/job-07-probe-flag-a/input_profile.json=read
output/batch/04-evaluation/job-07-probe-flag-a/job-status.json=read
output/batch/04-evaluation/job-07-probe-flag-a/metadata.json=read
output/batch/04-evaluation/job-07-probe-flag-a/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-07-probe-flag-a/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-07-probe-flag-a/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-08-probe-argc-argv/comparison_manifest.json=read
output/batch/04-evaluation/job-08-probe-argc-argv/input_profile.json=read
output/batch/04-evaluation/job-08-probe-argc-argv/metadata.json=read
output/batch/04-evaluation/job-08-probe-argc-argv/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-08-probe-argc-argv/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-08-probe-argc-argv/returned-evidence/evidence-target.json=read(trunc>2000)
output/batch/04-evaluation/job-09-fixture-both-sides/attribution.md=read（最终更正 + §10.18 纪律）
output/batch/04-evaluation/job-09-fixture-both-sides/comparison_manifest.json=read
output/batch/04-evaluation/job-09-fixture-both-sides/input_profile.json=read
output/batch/04-evaluation/job-09-fixture-both-sides/metadata.json=read
output/batch/04-evaluation/job-09-fixture-both-sides/returned-evidence/comparison.json=read
output/batch/04-evaluation/job-09-fixture-both-sides/returned-evidence/controller-health-after.json=read
output/batch/04-evaluation/job-09-fixture-both-sides/returned-evidence/controller.log=read
output/batch/04-evaluation/job-09-fixture-both-sides/returned-evidence/evaluation_report.json=read(trunc>2000)
output/batch/04-evaluation/job-09-fixture-both-sides/returned-evidence/evaluation_report.md=read
output/batch/04-evaluation/job-09-fixture-both-sides/returned-evidence/evidence-source.json=read(trunc>2000)
output/batch/04-evaluation/job-09-fixture-both-sides/returned-evidence/evidence-target.json=read(trunc>2000)
```
- `result.md`=missing；`evaluator_manifest.json`=missing；无任何 `request*.txt`/`*.model.json`/`repair*`/proposal json。

### FREEZE/CLASSIFY
- `frozen-inputs.md` L4-5：sourcePath `…/source/stest.c`；sha `bb943c3e…96bd`；形态 "suckless stest（110 行，含 main，用 ARGBEGIN/ARGEND 与 arg.h）"。L12-41 原始判定 `SOURCE_DEPENDENCY_GAP`（0 调用/跳过）；**L43-53 追加裁决更正**：属打包缺口，终态由 `SOURCE_DEPENDENCY_GAP` 改为 `FROZEN`、lifecycle 由 DONE 改为 **ACTIVE**、phase `SOURCE_PRECHECK_PASSED`（**与 item json 的 CLOSED/DONE 冲突**）。
- `evaluation-freeze.md`：源 `gcc -std=gnu11 stest.c -o program`；目标 `g++ -std=gnu++17 target.cpp -o program`；两侧 linux/x64；冻结 argv `[]`（后续按 job 变更）、stdin null；oracle：stdout `stest.c` 一行 / stderr 空 / exit 0 / 无侧效；驱动 `run_case.py`（`sys.argv[1:]` 原样追加、原始字节透传、`timeout=60`）；比较策略 `dimensions:["output"]`、`stdoutMode normalized-text`、`stderrMode exact`；覆盖缺口（-a、-d/-f/-s/-x、-l、-n/-o、-q、stdin 列表、未知选项）明列。
- `classification-1.json`：v2.3；cls `LOW_SIGNAL`；admissionStatus `ALLOWED`；blockingReason `null`；classifierSha256 `441b4d50…6524`；inputManifestSha256 `6d4b9e47…517f`；network_mode `none-detected`；reviewGroups `[]`。无重分类文件。
- `CORRECTION-D2-029.md`：旧 dataset `job-02` capsule 含 `stest.c`（3333B，`BB943C3E…96BD`）+ `arg.h`（1060B，`99CA0B68…21B0`），stest.c 哈希与 manifest 逐字符一致 ⇒ 属组装不完整。
- 模型：仅散文（各 `metadata.json` L12 `"deepseek-flash (project .env model); agent did not author target code"`）。**未记录 skill 选择。**

### SOURCE PRECHECK
- `job-00` / `eval-20261010-045728-9a8f152a`：`gcc -std=gnu11 stest.c -o program` → build `failed`/exit 1；诊断 `stest.c:11:10: fatal error: arg.h: No such file or directory`（135B，digest `cd680247…`）；exec `blocked`；report `COMPLETED`/`jobPhase RUNNING_SOURCE`/blocked；cleanup PASSED、未污染、READY。
- `job-01b` / `eval-20261010-052639-012888ea`（补齐 `arg.h` 后重跑）：同命令 → build `completed`/exit 0（171ms，无诊断）；exec `completed`/**exit 0**，stdout `stest.c\n`（8B，digest `ab350772…`），stderr 空；report：`runVerdict partial-runnable`、`codeVerdict failed`、`behaviorVerdict mismatched`，coverage 1/1 ⇒ **与 item json 的 recheck（completed/0 + stdout stest.c）在行为结论上不一致**；`comparisonRef` 指向 `comparison/result.json`、target 指向 `evidence/target.json`，而这两件**未回传**（job-01b 只有 evaluation_report.json + evidence-source.json）。cleanup PASSED、未污染、READY。

### REQUESTS/RESPONSES
- **两件均不存在**（无 `request*.txt`、无 `*.model.json`）⇒ 2 次模型调用（初始转换 + 一次"功能修复"）**没有** model name 字段、`finish_reason`、token usage、响应正文、parent/final hash。
- "修复返回与首版逐字节相同（仅 `new`→`newer` 3 行）"只见于 `job-05/attribution.md` L42-45 与 item json，**无响应原件支撑**。
- 失败/作废尝试（job 层）：job-01（空 argv 进 stdin 分支，两侧空输出被判 matched）、job-02（驱动 `stdin=PIPE` + `input=` 触发 Python `ValueError`，两侧 stderr 为同一条 run_case.py traceback，程序从未运行）、job-03/job-05/job-06/job-07（两侧输入不等价导致的 exit/stdout 不一致）、job-05（终态报告未落盘）。

### SELF-REVIEW
- `self-review-1.json`：verdict **`NO-REPAIR-IDENTIFIED`**；basis "diff of **target.gen.cpp** against the frozen stest.c (whitespace-normalized) shows the only delta is the documented C++ keyword rename of the static struct stat variable `new` -> `newer`, applied consistently at all 3 use sites"。
- checks：结构一致；可观察行为（选项 a,b,c,d,e,f,g,h,l,n,o,p,q,r,s,u,v,w,x；`name[0] != '.'`；`-q` → exit(0)；usage 文本与 exit(2) 逐字节一致；stdin getline；`-l` opendir/readdir；`return match ? 0 : 1`）保持不变；目标无 std::/iostream/placement new/残留 C++ 关键字；仅 POSIX 标准头。
- limitations：原文 "static review only. It does not predict compilation and is not behaviour evidence."
- unresolved：未列。knowledge suggestions：**无**。
- repair：**无任何 repair 件**（无 `target.self-repair-N.model.json`、无 proposal json）；自审文件的目标文件名 `target.gen.cpp` 与其余全件使用的 `target.cpp` **不一致**。

### JOBS
- `job-01` `eval-20261010-053037-1d8e7d08`（argv `[]`）：两侧 build `completed`/0；两侧 exec `completed`/**exit 1**，stdout **0B**（空串 digest `e3b0c442…`）、stderr **0B**；平台 `comparison` `matched`、`diffs: []`、coverage 1.0；`attribution.md` 判为**假阳性（装置缺陷）**：无参数时 stest 进入 `while (getline(...))` 读 stdin，而驱动固定 `stdin=DEVNULL` ⇒ 两侧"什么也没测"后 `return match ? 0 : 1` 恒为 1；记 UNVERIFIED。
- `job-02` `eval-20261010-053219-3465ab19`（argv `["stest.c"]`）：两侧 exec exit 1，stdout 空，**stderr 为 Python traceback**（`File "…/run_case.py", line 49, in <module> main()`；驱动器 `subprocess.run(stdin=PIPE, input=…)` 非法）；平台 `mismatched`（`stream.digest` `a0b0f51f…` vs `915d9698…`）；程序从未运行。
- `job-03` `eval-20261010-053340-c4f66916`（argv `["stest.c"]`，驱动修正后）：source exec `completed`/exit 0，stdout `stest.c\n`；target exec `completed`/**exit 1**，stdout 空，stderr 空；`comparison` `mismatched`：`execution.exitCode` changed/**critical**（0 vs 1）、`stream.normalizedText` changed/major（`stest.c\n` vs 空）；`attribution.md` 断言"**转换引入**"并列 4 条待定假设（后被 job-09 作废）。
- `job-04` `eval-20261010-053631-1290ccc3`（argv `["."]`，定位探针）：两侧 exec exit 1、stdout/stderr 全空；平台 `matched`、`diffs: []`；metadata 自述"diagnostic probe, NOT a verdict job"。
- `job-05` `eval-20261010-053749-41e2fafa`（argv `["-f","stest.c"]`，复现预检路径）：source exec exit 0、`stest.c\n`；target exec exit 1、空；`comparison` `mismatched`（exitCode critical、text major）；`job-status.json` 仍 `RUNNING/CLEANING`；`evaluation_report.json`=`{"detail":"job_report_not_found"}`、`.md`=`{"detail":"job_human_report_not_found"}`；`controller-health-after` 2/3 READY、`busy:CLEANING`；`controller.log` 只有 created 行；`attribution.md` 记"驱动把冻结论元经 py `--` 传入"的误判纠正过程，并留下未决现象（预检 stdout `stest.c` 与 `test(*argv,*argv)` 读法冲突）。
- `job-06` `eval-20261010-053909-9873e2a1`（argv `["stest.c"]`）：source exit 0、`stest.c\n`；target exit 1、空；`mismatched`；`job-status` COMPLETED/FINISHED + `lastError CODE_RESULT`；`attribution.md` 结论"差异不在选项解析路径"。
- `job-07` `eval-20261010-054021-68d31103`（argv `["-a","stest.c"]`）：source exit 0、`stest.c\n`；target exit 1、空；`mismatched`；无 attribution.md。
- `job-08` `eval-20261010-071912-71faff81`（argv `["stest.c"]`，探针）：两侧 stdout 均含探针横幅（子进程实收 argv、cwd、cwd 条目、`exists()`）；**source**：cwd 条目 `['arg.h','program','run_case.py','stest.c']`、`exists('stest.c') = True`、exit 0；**target**：cwd 条目 `['arg.h','program','run_case.py','target.cpp']`、`exists('stest.c') = False`、exit 1；`comparison` `mismatched`。
- `job-09` `eval-20261010-072112-9aeda8d5`（argv `["fixture.txt"]`，两侧同铺同一 fixture）：两侧 exec `completed`/**exit 0**，stdout `fixture.txt\n`（12B，两侧同 digest `9a44cc97…`），stderr 空；`comparison` `matched`、`diffs: []`、coverage 1.0；`evaluation_report` `runnable/passed/matched`；cleanup PASSED、未污染、READY；`attribution.md` 更正此前 4 次 `mismatched` 全为**打包不对称**（argv 指向只存在于源树的相对文件名），新增纪律 §10.18。
- 计数核对：11 个 job 目录（00/01/01b/02/03/04/05/06/07/08/09）；item json 记 requests 2；其 `evaluation.supersededJobs` 列 4 条；`job-09/attribution.md` 表列 4 条作废判定。

### RESULT/DELIVERY
- `result.md`：**不存在**。`evaluator_manifest.json`：**不存在**（尽管 lifecycle DONE）。claims 仅存于 item json 与各 `attribution.md`。
- item json 的 `evaluation` 声称最终 job `eval-20261010-072112-9aeda8d5` `matched`/0 diffs/accepted，`conversionDefect: "NONE - an earlier attribution claiming a hit-predicate defect was WRONG and is corrected here"`，`instrumentDefect` 描述冻结 argv 命名了只在源树存在的相对文件并把 4 个 job 列作 superseded — **这些与 job-08/job-09 原件一致**；但同项的 job-03/job-05 `attribution.md` 仍保留相反结论（未改写，仅追加更正）。

### ANOMALIES
- DONE 项缺 `result.md` 与 `evaluator_manifest.json`。
- 无请求/响应件：2 次模型调用的模型身份、`finish_reason`、token usage、响应正文、parent/final hash **均无原件**；"修复返回逐字节相同"不可审计。
- `job-01b/evaluation_report.json` 引用的 `comparison/result.json` 与 `evidence/target.json` **未回传**；其 `behaviorVerdict mismatched` 与 item json recheck 的"completed/0 + stdout stest.c"叙述不一致。
- `job-05` 为**中途快照**：`job_report_not_found`、`RUNNING/CLEANING`、`busy:CLEANING`、controller.log 无 finished 行 ⇒ 终态取证缺失。
- 平台 `matched` 出现在 `job-01`（两侧全空）与 `job-04`（两侧空输出 + exit 1）⇒ 空观察被判一致。
- 同一项内**两套相反归因并存**：job-03/job-05 写"转换引入命中谓词缺陷"，job-09 更正为"无转换缺陷、是我的打包不对称"。
- `job-04`/`job-07` metadata 自述"NOT a verdict job"，却留下 `comparison.json` 判定件。
- 自审文件名 `target.gen.cpp` vs 全件 `target.cpp`。
- `frozen-inputs.md` 更正后终态（ACTIVE / SOURCE_PRECHECK_PASSED）与 item json（DONE / CLOSED）冲突。
- 单行 bundle 截断 37 件。

### INDEPENDENT EVIDENCE FACTS
- 源侧在补齐 `arg.h` 后 `gcc -std=gnu11 stest.c` build `completed`/0，运行 exit 0、stdout `stest.c\n`（8B，digest `ab350772…`）——**该 digest 在 job-03/05/06/07/08 反复出现，源行为可复现**。
- 目标侧每个 job 都 build `completed`/0；目标在 job-03/05/06/07 输出空且 exit 1，在 job-09 输出 `fixture.txt\n` 且 exit 0。
- `job-08` 原件直接给出**两侧输入不等价**的机制：源树含 `stest.c`，目标树含 `target.cpp`，故目标 `stat("stest.c")` 必败。
- `job-02` 的 stderr 是 `run_case.py` 的 Python traceback（驱动崩溃），不是被测程序输出。
- `job-05` 的终态报告从未落盘；`job-09` report 为 `runnable/passed/matched`、cleanup PASSED、未污染、READY。
- **不支持**：目标相对于冻结源是否只有 `new`→`newer` 一处差异（目标文本已删除）；-l/-n/-o/-q/stdin 列表等路径的任何等价性；模型侧任何事实。

### ATTRIBUTION
- **apparatus（主导）**：驱动 `stdin=DEVNULL` 把"无参数"送进 stdin 分支；`subprocess.run(stdin=PIPE, input=…)` 非法；`job-05` 中途取证；冻结 argv 命名只在源树存在的相对文件（打包不对称）。
- **conversion-introduced**：**未确立**（job-03/job-05 的相反归因已被 job-08/job-09 推翻）。
- **environment**：平台比较器在空观察/驱动崩溃产物上给 `matched`（job-01/job-04）。
- **source-existing**：无。
- **undetermined**：是否存在 rename 之外的任何 C++ 行为差异（无有效反例）。

### KNOWLEDGE
- 候选规则（均有原件支撑）：（1）冻结 argv 引用文件时，必须确认**两侧树中都有同一份内容相同的 fixture**，否则两侧输入不等价（job-08 探针 + job-09 更正；case 自记为 `operational-discipline.md` §10.18）。（2）必须记录 harness 实际传递 argv 的通道（`python run_case.py <frozen argv…>`）；预检驱动用 `--` 分隔符导致程序实收 argv 不同、oracle 被建错。（3）`subprocess.run(stdin=PIPE, input=…)` 非法；驱动自身失败必须用**互异标记/退出码**（DRIVER-FAILURE / exit 97）表达，绝不能与程序输出一起比较。（4）平台 `matched` 只有在源侧观察非空且非退化时才可用。
- 当前契约覆盖：（2）（3）（4）的原则已见于 `AGENTS.md` 转换任务执行约束 §3「驱动四要素」（按冻结 argv 启动／到达被观察状态／采集真实 stdout-stderr-退出码-副作用／终止并收尾）及其"启动后等它自己退出不是通用驱动"的说明；§3 还明确"自审是正常推进信号，不是防线"、真正定案靠**第三方编译/行为证据**——与本项实测历史一致。（1）**未见于** `AGENTS.md` §3；本项自记为批次纪律 `operational-discipline.md` §10.18（**该文件本审阅未读 ⇒ 覆盖未核**），建议上提到 `references/framework/evaluation-readiness-contract.md` 的冻结/对称性要求。
- 需**否定**的自审建议：本项 `self-review-1.json` 无 knowledge 建议、无修复建议，其 NO-REPAIR 判定与最终"无转换缺陷"结论**一致**，不需否定；真正错误的自审式结论在 job-03/job-05 的 `attribution.md`（"命中谓词缺陷/转换引入"），**不得采信**。

### OPTIMIZATION
- 过程：每个 job 必须落盘**驱动脚本版本/哈希**（本项全部事故都在驱动侧）；修复必须落盘请求与响应；禁止把中途快照（`job_report_not_found` + RUNNING/CLEANING）当作 job 记录保留，或强制标注"快照"。
- 去噪/统计：把"探针 job"移入 `probes/` 子区，避免其 `comparison.json` 判定与正式 verdict job 混算；superseded job 与有效 job 分列计数（本项 11 个 job 中至少 4 个作废）。
- 评估：提交前加两条机器可检门禁——(a) argv 引用的每个文件在两侧树中存在且同哈希；(b) 源侧观察非空且非退化。
- 交付：DONE 项强制 `result.md` 与 `evaluator_manifest.json`。

### UNKNOWNS
- 目标文本是否只有 `new`→`newer` 一处差异（已删除）。
- `job-05/attribution.md` 记的未决现象（预检 stdout 与 `test(*argv,*argv)` 读法冲突）的机制——job-09 的结果使其不影响结论，但机制在现存件中仍未解释。
- -l/-n/-o/-q/stdin 列表/未知选项等路径的等价性（从未覆盖）。
- 本项是否曾选择/加载知识（无记录）。

---

## D2-030 ｜ 期望 dir=`c-to-csharp/handoff-2026-10-02-d02-apisetmap-c` ｜ 0 件

### IDENTITY
- taskId `D2-030`。
- manifest.csv 第 30 行：Kind `REUSE`；Direction `c-to-csharp`；SourceLang `C`；TargetLang `C#`；SourceFile `ApiSetMap.c`；Lines `394`；Origin `dataset/c-to-csharp/handoff-2026-10-02-d02-apisetmap-c`；JobId `eval-20261005-081635-fd44502b`；Sha256 `13346B48F8B5C7211FD43CE2D954F1398AD9574065316564634D1CC9FA9747D8`；Evidence `dual-build-PASS (inherited)`。
- item json `batch/items/D2-030.json`：kind **`NEW`**（与 manifest `REUSE` 冲突）；direction `c-to-csharp`；targetLang `csharp`；disposition `FROZEN`；phase `NOT_STARTED`；lifecycle `WAITING`；`pendingAction` "re-submit original contract after the platform fixes the C# target evidence-bundle schema"；`blockingReasons: ["BLOCKED_ENV"]`；`blockerRef: batch/platform-blocker-csharp-target.md`；`dispositionNote` 记 "Recorded as WAITING/BLOCKED_ENV per user ruling 2026-10-11 … no freeze job was run because the defect is already characterised. 0 model calls."；`verdicts` 全 `UNVERIFIED`、`safety: not-classified`；`usage.requests: 0`；casePath **`docs/test/dataset/c-to-csharp/handoff-2026-10-02-d02-apisetmap-c`**（旧 dataset 路径）；`sourceSha256` `13346b48…47d8`（小写，同值）。

### FILE INVENTORY（0 件）
```
c-to-csharp/handoff-2026-10-02-d02-apisetmap-c/**/* = dir-empty 或 absent（0 文件）
c-to-csharp/D2-030-*                          = dir-empty 或 absent（0 文件）
c-to-csharp/*                                 = dir-empty 或 absent（0 文件）
```
- 说明：三种 glob 均返回 0 文件；对 `docs/dataset-2/dataset-2-copy/c-to-csharp` 的**内容 grep 亦无匹配**。`glob` 只返回文件、不返回目录节点 ⇒ **无法用现役工具判定该目录节点本身是"存在但空"还是"不存在"**，只能确定为"**无任何文件**"。
- 全副本范围内 `c-to-csharp/` 路径字符串仅出现于：`manifest.csv:30`（Origin）、`batch/items/D2-030.json:29`（casePath）；另有他处对 `c-to-csharp/D2-159 utils.c` 的**文字提及**（`c-to-cpp/D2-153-c-c-cp.c/output/batch/01-frozen/frozen-inputs.md:59`，为源码搜索命中描述，非本项材料）。
- 既有但未完成的历史审阅件 `batch/current-system-review-2026-10-12/harness-a-coverage.md:43` 把该路径登记为 `待核 / PENDING`（**不构成存在性证据**）。
- **不存在**：`frozen-inputs.md`、`classification-N.json`、`classifier-input.json`、任何 `job-NN/`、`request*.txt`、`*.model.json`、`self-review-*.json`、`result.md`、`evaluator_manifest.json`、`comparison.json`、`*evidence*.json`。

### FREEZE/CLASSIFY
- **无任何冻结或分类产物**（无目录、无文件）。item json 中亦**无 `classifier` 字段**。
- `blockerRef` 指向的 `batch/platform-blocker-csharp-target.md`（已读全文）：记录平台缺陷 `INFRA_ERROR` / `lastError.code AGENT_UNAVAILABLE` / owner agent / retryable true，message `EvaluationContractError: invalid codeconvert-evidence-bundle at $.collectorDiagnostics.0: Additional properties are not allowed ('detail' was unexpected)`；2/2 复现（D2-007 job-00 原提与同 capsule 重提，逐字相同）；对照实验（同形 capsule 仅目标语言改为 `c`）⇒ `COMPLETED`；影响面 38 项（c-to-csharp 6 项之一即本项）；处置为保留 `WAITING/BLOCKED_ENV`、目标侧记 UNVERIFIED、0 模型调用。**该文件顶部有 2026-10-11 标注"✅ 已修复"**（探测 `platform-probes/probe-csharp-target-2026-10-11/`，jobId `eval-20261011-122249-fe456bbe` → `COMPLETED`，target build/exec `completed/0`，`collectorDiagnostics=[]`），并新增纪律"`comparison_manifest.target.artifactLanguage` 必须写 `csharp`，写 `dotnet` 会触发 403 `identity_mismatch`"。
- `batch/summary.md:377` 仍把 `D2-030` 列在 14 项 C# 目标 `BLOCKED_ENV` 清单中。

### SOURCE PRECHECK
- **无**（无任何 job 目录）；`usage.requests: 0`。

### REQUESTS/RESPONSES
- **无**（无 `request*.txt` / `*.model.json`）⇒ 无 model name、`finish_reason`、usage、正文、hash；无失败 attempt 文件。

### SELF-REVIEW
- **无**（无 `self-review-*.json`、无 repair 件、无 proposal json）。

### JOBS
- **无任何 job 目录**；无 `input_profile.json`、`comparison_manifest.json`、`metadata.json`、`job-id*.txt`、任何 returned-evidence。

### RESULT/DELIVERY
- `result.md`：**不存在**。`evaluator_manifest.json`：**不存在**。无 job 产物。
- 唯一收口记录：`batch/items/D2-030.json`（WAITING / BLOCKED_ENV / requests 0）与 `batch/events.jsonl` 两条事件：`:264` `DEFERRED`（reason `BLOCKED_ENV`，"c-to-csharp (C# target); platform evidence-bundle schema defect; per user ruling 2026-10-11; 0 model calls"）、`:270` `TERMINAL`（lifecycle `WAITING`，"blocked at the evaluation gate by the C# target platform defect"）。

### ANOMALIES
- **身份冲突**：manifest `Kind=REUSE` + `Evidence=dual-build-PASS (inherited)` + 继承 `JobId`，而 item json `kind=NEW` 且 `verdicts` 全 `UNVERIFIED` ⇒ 同一项"是否有继承的编译 PASS"两说。
- **casePath 冲突**：item json 指向 `docs/test/dataset/...`（旧 dataset），既不同于 manifest 的 `Origin`，也不同于同批 REUSE 项的约定（`docs/test/dataset-2/...`，如 D2-024/025/027/028/029）。
- **目录为空**：manifest 声明了具体源文件名、394 行、具体字节哈希与继承 PASS，但本副本 `c-to-csharp/` 下**无任何文件**（既无 source，也无任何过程材料）。
- **阻断状态陈旧**：item 记 `BLOCKED_ENV` / pendingAction "after the platform fixes …"，而 `platform-blocker-csharp-target.md` 顶部已声明 2026-10-11 修复；D2-065 展示了应有的 REOPEN 写法（`pendingAction: "REOPEN: … FIXED on 2026-10-11 …"`），本项**未随之更新**。
- **本项自身无缺陷命中证据**：平台缺陷的复现证据（2/2 + 对照实验）全部属于 D2-007；D2-030 无 job、无错误日志 ⇒ "被该缺陷阻断"是**批次政策推定**，非本项实测。
- `events.jsonl` 中本项**无 `FROZEN` / `CLASSIFIED` / `SOURCE_PRECHECK` 事件** ⇒ 从未冻结、从未分类、从未预检。
- 0 模型调用、无目标侧任何产物。

### INDEPENDENT EVIDENCE FACTS
- 原件仅支持：manifest 行存在并声明源文件/哈希/Origin/继承 job 与 `dual-build-PASS (inherited)`；item 记录存在且为 `WAITING/BLOCKED_ENV`、请求 0；`events.jsonl` 恰有 2 条事件（DEFERRED → TERMINAL）且**无冻结/分类/预检事件**；批次级存在一份"平台 C# 目标缺陷"文档且已被标注修复；同方向其余 5 项（D2-156~160）在 manifest 中也无任何目录/材料（其 item 记录同为 `WAITING/BLOCKED_ENV`）。
- **原件不支持**：本项源文件是否存在、是否为 394 行、字节哈希是否成立、继承的 `eval-20261005-081635-fd44502b` 是否存在或 PASS、任何构建/运行/转换/比较事实。

### ATTRIBUTION
- **apparatus/process**：无任何材料；item 与 manifest 的 Kind/casePath 冲突；阻断状态未随平台修复更新；"被阻断"为批次推定。
- **environment/platform**：C# 目标 evidence-bundle schema 缺陷是**有据的平台问题**，但其对本项的**直接命中未经本项证据证实**。
- **source-existing / conversion-introduced**：不适用（未转换、未预检）。

### KNOWLEDGE
- 候选规则：（1）批次级平台阻断被宣布修复后，受影响项必须**显式重开或追注**，使"仍被阻断"与"记录陈旧"可区分（D2-065 有 REOPEN 形态，D2-030 无）。（2）manifest 的 `Kind/Origin/casePath` 与 item 的 `kind/casePath` 必须作为**同一身份集**交叉核对（本项三处不一致）。（3）0 材料项应带显式"无材料"标记，避免缺档被读成丢失。
- 当前契约覆盖：该身份交叉核对属交付/状态契约要防的双源不一致，但本审阅**未读** `references/framework/delivery-handoff-contract.md` 与 `references/framework/task-state-contract.md` ⇒ **覆盖情况未核**；`platform-blocker-csharp-target.md` 本身已写明"恢复后按原契约重提"与终态口径，但**未规定"修复后必须回写受影响项状态"** ⇒ 属可补强点。
- 需否定的自审建议：无（本项无自审）。

### OPTIMIZATION
- 数据一致性：Kind/casePath 以 manifest 为单一真源，item 只引用不重述；或加双向一致性检查。
- 过程：平台阻断解除时生成"需重开项清单"，并逐项要求 REOPEN 或显式"仍阻断"结论。
- 评价：延后项应记录**阻断依据的粒度**（"本项实测" vs "批次政策推定"），避免把 D2-007 的证据当成 38 项的实测证据。
- 统计：无材料项在统计中单列，避免与"材料缺失"混算。

### UNKNOWNS
- `c-to-csharp` 目录节点是否存在（现役工具只能确认"无任何文件"）。
- D2-030 是否有过程材料被移除、或从未产生。
- 真实 Kind（REUSE 还是 NEW）。
- 继承的 `eval-20261005-081635-fd44502b` 证据是否可达（旧 dataset 在本副本之外，本次未访问）。
- 源文件 `ApiSetMap.c`（394 行、哈希 `13346B48…47D8`）是否存在。

---

## 附：跨项装置与统计事实
- **请求/响应层整体缺失**：六项中 `request*.txt`、`repair*.txt`、`*.model.json`、`evaluator_manifest.json`、`closure.json`、`report-retry*.json` 全部不存在；全 `c-to-cpp` 树内仅 **D2-151** 拥有 `02-conversion/request.system.txt`、`target.gen.model.json`、`03-self-review/self-review-1.model.json` 与 `evaluator_manifest.json`。故本批**无法**核对模型身份、`finish_reason`、token usage、响应正文与 parent/final hash。
- **单行截断**：`read` 与 `grep` 均把单行截断在约 2000 字符；受影响的 71 件已逐件标 `read(trunc>2000)`（D2-024 17 / D2-025 13 / D2-027 3 / D2-028 1 / D2-029 37）。
- **平台 `matched` 假阳性类**：本批至少 4 例（D2-024 job-03、job-04；D2-029 job-01、job-04），特征为两侧观察同为空或同为装置失败产物，平台仍给 `diffs: []` 与 `coverageRatio 1.0`。
- **非终态记录被当作 job 记录**：D2-024 job-04、D2-029 job-05（另有 D2-024 job-00、D2-025 job-00、D2-027 job-00/00b/00c、D2-028 job-00、D2-029 job-00 的 `jobPhase RUNNING_SOURCE` 与 `jobStatus COMPLETED` 并存）。
- **文件计数**：D2-024 46 + D2-025 49 + D2-027 28 + D2-028 9 + D2-029 108 = **240 件全部读取**；D2-030 **0 件**。
