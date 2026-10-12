# Harness A — cases 17：D2-037 ~ D2-041 静态审阅报告

- 审阅者：只读静态文档审阅 Agent（未编译、未运行、未调用分类器/转换/提交）。
- 范围：`docs/dataset-2/dataset-2-copy` 下 5 个用例目录 + `batch/items/D2-037..041.json` + `manifest.csv` 行 37–41。
- 代码（`source/`、`target.cpp`、`run_case.py`）已删除，仅流程产物留存。
- 工具限制（已核实）：平台 bundle（`evidence-*.json`、`comparison.json`、`evaluation_report.json`、`controller-health*.json`）为单行且 read/grep 在 2000 字符截断、无字节偏移补读手段；此类一律登记 `read(截断>2000字符, 现役工具无法补读)`，并以 md 伴侣交叉核对。
- 本报告不含任何密钥；未重构源码；未访问 `D:/CodeConvertRemote/Stack`。

---

## 0. 跨项共同事实（SHARED，逐项不再重复）

- **批量级**：`batch/items/D2-037..041.json` 全部读取；`manifest.csv` 行 37–41 读取。manifest 的 casePath=`dataset/go-to-cpp/...`，item JSON 与 frozen-inputs 用 `docs/test/dataset-2/go-to-cpp/...`，`evaluator_manifest.json.targetDir`=`C:\Users\Administrator.DESKTOP-LRHSLVD\Desktop\code-convert-skill\docs\test\dataset-2\...` ⇒ 同一用例存在三个路径根。
- **目录形制一致**：`01-frozen`(3) + `02-conversion`(3 或 4) + `03-self-review`(3) + `04-evaluation/job-00-source-buildability`(14) + `04-evaluation/job-01-dual-build`(15) + `result.md` + `evaluator_manifest.json`。D2-037 无 `observed-source-stderr.txt`（40 文件），其余 4 项有该 0 字节文件（各 41 文件）。
- **`.model.json` 语义**：`target.gen.model.json` 是**真实响应**（含 `content`=完整 target.cpp、`reasoning_content`），但单行 JSON，read 截断于 2000 字符 ⇒ 全文不可得；该文件**无 model / finish_reason / usage 字段**。`self-review-1.model.json` 是**纯元数据**（taskId/stage/reviewN/model/finishReason/usage/maxTokensFieldSent/verdict/note），无正文 ⇒ 元数据 ≠ 完整响应；自审结论正文只存在于 `self-review-1.json`。
- **平台 bundle 截断**：每项 6–7 个 `evidence-*.json`/`comparison.json`/`evaluation_report.json` 及 2 个 `controller-health*.json` 均为单行 >2000 字符；`evaluation_report.md` 可读，verdict 与其 JSON 一致。
- **`batch-authorization.json`（10 份，5 项 × job-00/job-01）逐字节相同**，其中 `dataSource.confirmation` 写 **“该项 D2-088 无网络、无凭证、仅本地文件写入”**：错项号 + 模板残留；对 D2-037（REVIEW_NETWORK/loopback）自相矛盾。authorizedBy=gyh-p1、authorizedAt=2026-10-10T14:43:00Z、validUntil=2026-10-17T14:43:00Z、contractHash=sha256:a9ed1445…d82e、cleanupVerified=true。
- **`input_profile.json`（每 job 各 1）**：argv=[]、stdin=null、fixtures=[]、environment={}、workingDirectory="workspace"、kind=codeconvert-input-profile、profileId=任务号、timeoutSeconds=**30**、observationPolicy.dimensions=["output"]、comparisonPolicy.output={stdoutMode:normalized-text, stderrMode:exact, ignoredJsonPaths:[]}。**所有 frozen-inputs.md 写“`subprocess.run(..., timeout=60)`” ⇒ 冻结与平台不一致。**
- **job-00 设计**：target 为占位件（frozen 声明 `int main(){return 0;}`），平台仍执行双侧比较，故 job-00 的 `evaluation_report.md`/`comparison.json` 一律 `Conversion result: FAIL` / `Behavior: MISMATCHED` / 1 条 `major` diff (`stream.normalizedText`)，target stdout = `--- report ---\nMISSING\n`（23 B，digest `717f4742…3ebd`）。job-00 的**源侧观察即源基线**；job-00 与 job-01 的 `source.baselineReference.artifactHash` 相同（基线复用），`target.artifactHash` 不同（占位 vs 真目标）。result.md 正确只采信 job-00 的源侧字段。
- **未出现**：`closure.json`、report-retry、`attribution.md`、任何 reclassification（`old_cls`/`old_reason`=null）、失败 attempt（`failedAttempts`=0）、修复轮（`codeRevisions`=0、`selfRepairRounds`=0）。
- **所有 job**：status COMPLETED、jobPhase FINISHED、两侧 preflight/cleanup=PASSED、contaminated=false、runnerStateAfter=READY、environmentStatus=clean；`controller-health-before/after` 均 status=ok、runnerMode=agent、readyRunnerCount=3/blockedRunnerCount=0、contractSetHash 同 batch-authorization；comparison preset=noise-tolerant-v1、text_tokens=[temporary-paths,timestamps,ephemeral-ports]、system_noise_patterns=[**/.DS_Store,**/Thumbs.db,**/desktop.ini,**/__pycache__/**,**/*.pyc]、tolerate_minor=true。`runners-before.json`（每 job）列出 linux/windows/macos 三个 READY、supportsSnapshotRollback、baselineSnapshot=CC-Eval-Linux-8Lang-1.0.28 / CC-Eval-Windows-8Lang-1.0.28 / CC-Eval-Mac-7Lang-1.0.28-AutoLogin。
- **requests=2**（1 转换 + 1 自审），model=deepseek-flash；item JSON 的 usage 总数 = 转换调用 + 自审调用，可按 `self-review-1.model.json.usage` 差集还原转换 token。
- **共同覆盖缺口**：仅 `output` 维度 applicable；filesystem / processes / registry / network 全部 `not-applicable` ⇒ 真实副作用（本地文件写入、回环 socket、子进程有无）**未被独立观察**；文件模式位从未比较；错误分支基本未覆盖。
- **归因总表**：037/038/039/040 两侧 stdout digest **逐字节相同**（无差异可归因）；041 唯一 `minor` diff=timestamp ⇒ 环境/装置；5 项 job-00 的 FAIL ⇒ 装置（占位件）。未发现需归因“转换引入”的已证差异；所有 self-review items 的 origin 均非 conversion-introduced。
- **当前契约覆盖（供 KNOWLEDGE 引用）**：GO-CPP-07 见 `skills/directions/go-to-cpp/SKILL.md:152`（go-to-cpp 方向规则共 GO-CPP-01..07，见 18/35/59/81/101/128/152 行）；§10.15 semantic_pass 独立档位见 `docs/dataset-2/dataset-2-copy/batch/operational-discipline.md:245–265`；§10.14 消噪归因见同文件 284/306；§10.18/§10.19 装置对称见同文件 356/396；semantic_pass 不代功能验收见 `references/adapter/controller/comparison-policy-adapter.md:99–108` 与 `references/framework/evaluation-readiness-contract.md:97`；分层报告/不合成成功率见 `AGENTS.md` §5/§6。

---

## 1. D2-037（go-to-cpp / handoff-2026-10-02-d26-chunk-upload-rehash-go）

### IDENTITY
- taskId=D2-037；rawItemId=D2-037；batchId=batch；kind=**REUSE**；direction=go-to-cpp。
- source file=`chunk_upload_rehash.go`；declared Sha256（manifest.csv 行 37，大写原样）=`2D7D95936ED7BB5E98B5B4A9DB83059F9B58F4A41962B70FDA826211442150B1`，item JSON 小写 `2d7d9593…150b1`，二者一致；classification-1.json 内 files[].sha256 亦一致。
- casePath=`docs/test/dataset-2/go-to-cpp/handoff-2026-10-02-d26-chunk-upload-rehash-go`（item JSON/frozen）；manifest 写作 `dataset/go-to-cpp/handoff-2026-10-02-d26-chunk-upload-rehash-go`。
- item JSON：disposition=`CONVERTED`、phase=`CLOSED`、lifecycle=`DONE`、pendingAction=null、blockingReasons=[]、codeRevisions=0、selfRepairRounds=0、targetSha256=`23c4e7722441a8a0f8a2ab939d314a9089bba5a9fbfb8f4d219b86249547ab9a`。
- usage：requests=2、promptTokens=8395、completionTokens=39625、reasoningTokens=31509、totalTokens=48020、model=deepseek-flash、failedAttempts=0。
- evaluator id=`eval-20261005-075714-01c8bdb5`（manifest）；job-00=`eval-20261011-083355-1f723f1a`；job-01=`eval-20261011-083929-99e38b7f`。

### FILE INVENTORY（前缀 `P`=`go-to-cpp/handoff-2026-10-02-d26-chunk-upload-rehash-go/output/batch/`）
| 路径 | 状态 | 备注 |
|---|---|---|
| P01-frozen/classification-1.json | read | cls=REVIEW_NETWORK |
| P01-frozen/classifier-input.json | read | 单任务输入 |
| P01-frozen/frozen-inputs.md | read | 冻结契约 |
| P02-conversion/observed-source-stdout.txt | read | 源基线 stdout |
| P02-conversion/request.system.txt | read | 转换请求 system |
| P02-conversion/target.gen.model.json | read(trunc>2000字符, 现役工具无法补读) | 真实响应，正文+reasoning 截断 |
| P03-self-review/review.system.txt | read | 自审清单 |
| P03-self-review/self-review-1.json | read | NO-REPAIR-IDENTIFIED |
| P03-self-review/self-review-1.model.json | read | metadata-only |
| P04-evaluation/job-00-source-buildability/batch-authorization.json | read | D2-088 模板残留 |
| P04-evaluation/job-00-source-buildability/comparison_manifest.json | read | go/cpp build+run |
| P04-evaluation/job-00-source-buildability/controller-health-before.json | read | ok |
| P04-evaluation/job-00-source-buildability/input_profile.json | read | timeout 30 |
| P04-evaluation/job-00-source-buildability/job-id.txt | read | eval-…1f723f1a |
| P04-evaluation/job-00-source-buildability/metadata.json | read | targetHash=placeholder-precheck |
| P04-evaluation/job-00-source-buildability/runners-before.json | read | 3 runner READY |
| P04-evaluation/job-00-source-buildability/this-task-classification.json | read | 与 classification-1 一致 |
| P04-evaluation/job-00-source-buildability/returned-evidence/comparison.json | read(截断>2000字符, 现役工具无法补读) | mismatched(占位) |
| P04-evaluation/job-00-source-buildability/returned-evidence/controller.log | read | 08:33:55→08:35:10 |
| P04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json | read(截断>2000字符, 现役工具无法补读) | FAIL/mismatched |
| P04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.md | read | FAIL/mismatched |
| P04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json | read(截断>2000字符, 现役工具无法补读) | 源基线（real） |
| P04-evaluation/job-00-source-buildability/returned-evidence/evidence-target.json | read(截断>2000字符, 现役工具无法补读) | 占位件 MISSING |
| P04-evaluation/job-01-dual-build/batch-authorization.json | read | 同上 |
| P04-evaluation/job-01-dual-build/comparison_manifest.json | read | go/cpp |
| P04-evaluation/job-01-dual-build/controller-health-before.json | read | ok |
| P04-evaluation/job-01-dual-build/input_profile.json | read | timeout 30 |
| P04-evaluation/job-01-dual-build/job-id.txt | read | eval-…99e38b7f |
| P04-evaluation/job-01-dual-build/metadata.json | read | targetHash=23c4e772… |
| P04-evaluation/job-01-dual-build/runners-before.json | read | 3 runner READY |
| P04-evaluation/job-01-dual-build/this-task-classification.json | read | 一致 |
| P04-evaluation/job-01-dual-build/returned-evidence/comparison.json | read(截断>2000字符, 现役工具无法补读) | matched, diffs=[] |
| P04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json | read | ok |
| P04-evaluation/job-01-dual-build/returned-evidence/controller.log | read | 08:39:29→08:40:45 |
| P04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json | read(截断>2000字符, 现役工具无法补读) | runnable/passed/matched |
| P04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md | read | PASS/MATCHED |
| P04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json | read(截断>2000字符, 现役工具无法补读) | 236 B, ec1af781… |
| P04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json | read(截断>2000字符, 现役工具无法补读) | 236 B, 同 digest |
| Pevaluator_manifest.json | read | 移交清单 |
| Presult.md | read | 分层结论 |

**共 40 个文件（本项无 `observed-source-stderr.txt`）**；另读 `batch/items/D2-037.json` 与 manifest.csv 行 37。

### FREEZE/CLASSIFY
- frozen-inputs.md（81 行）：sourcePath=`…/source/chunk_upload_rehash.go`；sourceSha256 大写原样；sourceBytes=1596、sourceLines=64；sourceLang/std=Go/Go 1.27（标准库 bytes, crypto/sha256, encoding/hex, encoding/json, fmt, io, net, net/http, os, path/filepath, sort, strconv, sync）；targetLang/std=C++/ISO C++17；sourceOs=**linux**、targetOs=**linux**、arch=x64；source/targetRunnerId=`linux-vm-agent-x64`；snapshots=CC-Eval-Linux-8Lang-1.0.28；model=`deepseek-flash` @ CODE_TRANSLATOR_BASE_URL temp=0.2 RAG=off、outputBudget 不设 max_tokens；selected skills=go-to-cpp/SKILL.md、languages/go.md（sha256 4962198a…de97）、languages/cpp.md、seven-language-common-semantics.md（sha256 eb15af4c…79a5）、scenes/network-io、scenes/concurrency、scenes/file-io；sceneTags=network-io+concurrency+file-io；attackTactic=none（未逐符号取证）；taskMode=短单文件(64 行)。
- driver：一次性程序+自然退出，argv=`[]`、stdin=`null`、cwd=驱动所在目录（workspace）、terminate=`subprocess.run(..., timeout=60)`；oracle=需要功能评估、维度 `output`、比较策略 stdoutMode=normalized-text / stderrMode=exact；oracle 可冻结性前置检查（§10.16）逐条给出（chunks/rebuild/sha256 确定可复现、随机端口不入输出、无时间戳/计数器/并发顺序暴露）。
- sourceOsBasis：纯 Go 标准库（net/http + net.Listen）、无 syscall/#cgo，选 linux；可构建性只由编译器诊断定案。
- 网络与安全边界：classifier 判 `cls=REVIEW_NETWORK`、network_mode=loopback、network_targets=[{value:"127.0.0.1", scope:"loopback"}]、requiresNetworkIsolation=false、admissionStatus=ALLOWED；只绑 127.0.0.1（端口 0）；目标侧必须同样限定 127.0.0.1，不得绑 0.0.0.0。
- targetBuild=`g++ -std=gnu++17 target.cpp -o program`；C++ 须自行实现回环 HTTP/1.1 服务端与客户端，**不得用固定字符串/桩函数代替真实工作**；job-00 目标为占位件、只读源侧 build 字段。
- **未冻结/待确认**：精确工具链版本；C++ HTTP 实现形态；若无法建立等价可观察入口则记 PREPARATION_GAP。未覆盖 5 项：错误分支、并发竞态、乱序/重复/空 body、server.Close 异常路径、HTTP 202 未观察。
- classification-1.json：version=2.4、cls=REVIEW_NETWORK、reason=network_scope_and_inputs_require_review、admissionStatus=ALLOWED、blockingReason=null、executionApproved=true、executable=false、requiresNetworkIsolation=false、requiresSyntheticData=false、classifierSha256=`009a6f31177b08334663340321494ace1e430de13f8a5687e6843ab26839f3a4`、inputManifestSha256=`181c41418a5e0eae1c8f4bb0235cbeb60f2b2670cc2a1982896d9639ce667673`、old_cls=null、old_reason=null；reviewGroups=[filesystem,network,process]；files=chunk_upload_rehash.go（sha256 一致，network 行 32/34/42、filesystem 行 21/27/62，network_mode=loopback，network_targets 行 32 redirectVerified=false，has_network/has_file_ops=true，has_process_exec=false）、run_case.py（sha256=`8fb0b9d8ec139bcf67d39a7eb54c3d658be680476c063e63ddb282b4596f4c1d`，filesystem 行 42、process 行 1/28/29）；limitations=lexical_heuristics_not_dataflow / target_driver_dependencies_not_assessed / isolation_and_authorization_not_assessed。
- **无 reclassification**（old_cls/old_reason=null）。job-00 与 job-01 的 `this-task-classification.json` 与 01-frozen/classification-1.json 逐字段一致。

### SOURCE PRECHECK（job-00）
- jobId=`eval-20261011-083355-1f723f1a`（job-id.txt）；exact build command=`go build -o program chunk_upload_rehash.go`（源，linux x64）。
- build status=`completed`、exitCode=0、durationMs=12912、stdout/stderr 均空（digest=e3b0c442…b855 即空串 sha256）。
- diagnostic：无（evidence-source.json 无诊断字段，stderr 空）。
- execution/observation：status=completed、exitCode=0、durationMs=34、timedOut=false；stdout sizeBytes=236、digest=`sha256:ec1af78101c5f5012431b9723342526f38ec87de4722bbf11618382ceca1edec`，内容=`artifact: /tmp/safe-attck-go/13_exfiltration/advanced-exfil-report.json\n--- report ---\n{\n  "chunks": 3,\n  "rebuild": "demo exfil payload split by chunks",\n  "sha256": "7a5adaae3767b14588fce307c420da09971cf1cde0c40c5f55da84cb45392ab8"\n}\n`；stderr 空。
- cleanup：evidence/report 记 lifecycle.cleanup=PASSED（attempts=1）、preflight=PASSED、contaminated=false、runnerStateAfter=READY。
- target（占位）build completed/0（durationMs 604）、exec completed/0（126ms）、stdout=`--- report ---\nMISSING\n`、stderr 空 ⇒ job-00 comparison=mismatched（预期的占位效应）。

### REQUESTS/RESPONSES
- `request.system.txt`（21 行）：**完整语义契约文本，不含源码全文**；规定输出只有 ```cpp 代码块、逐字节 stdout/stderr 与退出码不变、不得删功能、**必须真实完成**回环监听+3 分片接收+按索引重组+SHA-256、目标文件名 target.cpp；逐条给 `fmt.Println` 换行、`json.MarshalIndent` 键序 chunks<rebuild<sha256 与数值/字符串类型、`net.Listen("tcp","127.0.0.1:0")` 端口 0、`/upload?i=N` 回 202、三段 payload[:10]/[10:20]/[20:]、关闭顺序（**停止标志+有界 poll，不得裸 close 唤醒 accept**）、自实现 SHA-256（禁 OpenSSL）、路径 /tmp/safe-attck-go/13_exfiltration、错误忽略但退出码 0/stderr 空。未见脱敏处理，也无凭证内容。
- `target.gen.model.json`：role=assistant；`content`=真实 C++ 目标（```cpp…，含自实现 SHA-256、真实 socket/bind/listen 于 INADDR_LOOPBACK、sin_port=0、getsockname、停止标志+poll(50ms)、std::map<int> 重组、手写 JSON），**单行截断于 2000 字符** ⇒ 全文不可得；`reasoning_content` 亦截断（中文推理，描述实现计划）。**未记录 model/finish_reason/usage；未记录 parent/final hash**（targetSha256 仅见于 item JSON、result.md、job-01 metadata）。
- `self-review-1.model.json`：**metadata-only**；taskId=D2-037、stage=SELF_REVIEWED、reviewN=1、model=deepseek-flash、finishReason=`stop`、usage{prompt 6127, completion 22444, reasoning 18730, total 28571}、maxTokensFieldSent=false、verdict=NO-REPAIR-IDENTIFIED、note=“Static review only; not a compile or behavior conclusion.”。
- 失败 attempt：**无**（failedAttempts=0，无 repair*.txt）。

### SELF-REVIEW
- `self-review-1.json`：verdict=`NO-REPAIR-IDENTIFIED`；reviewedScope=对 target.gen.cpp（368 行，C++17/POSIX）与源逐行对照，覆盖真实监听/SHA-256/HTTP 收发/有序重组/JSON 形态/并发关闭/输出与退出码共 11 项；**未执行编译或运行**。
- 11 项 issue 全为“未发现问题”，proposed_fix 全 null；origin：多为 conversion-introduced、2 项 environment（路径 os.TempDir 硬编码 /tmp；文件权限）、1 项 error-path（目标静默/源 panic）。
- 已登记风险/未决：json_escape 未实现 Go 的 HTML 转义（< > &）与 U+2028/2029（本用例 rebuild 纯 ASCII，不可达）；bind/listen 返回值未检查；并发时序未压测；`getsockname`/前缀无涉及。
- **无修复**（无 self-repair model json/proposal、无 change note、codeRevisions=0）。

### JOBS
- **job-00 `eval-20261011-083355-1f723f1a`**（`04-evaluation/job-00-source-buildability/`）：
  - input_profile：profileId=D2-037、argv=[]、stdin=null、fixtures=[]、environment={}、cwd=workspace、timeoutSeconds=30、dimensions=["output"]、stdoutMode=normalized-text、stderrMode=exact。
  - comparison_manifest：caseId=D2-037、kind=codeconvert-comparison-manifest、schemaVersion=1.0、inputProfileRef=input_profile.json；source{arch x64, artifactLanguage **go**, os **linux**, buildCommand `go build -o program chunk_upload_rehash.go`, runCommand `python run_case.py`}；target{arch x64, artifactLanguage **cpp**, os **linux**, buildCommand `g++ -std=gnu++17 target.cpp -o program`, runCommand `python run_case.py`}。
  - metadata：caseId=D2-037、kind=codeconvert-third-party-evaluation-metadata、schemaVersion=1.0、networkBoundary=“isolated VM; loopback only (127.0.0.1, ephemeral port). No egress to public/production networks; no DNS. classifier network_mode=loopback, requiresNetworkIsolation=false”、sourceHash=sha256:2d7d9593…、targetHash=sha256:**placeholder-precheck**、targetArtifact=`target/target.cpp (placeholder)`。
  - job-id.txt=eval-20261011-083355-1f723f1a。
  - returned-evidence：evidence-source.json（上述源基线；build 12912ms、exec 34ms；baselineReference.artifactHash=`f2b8754c8b8d2745f127c828cf6c7b187af85ceaccd098263a0eb1c37e67a6c1`；inputProfileHash=`0c5d2d5698d1587b9f86c051a575e003c5eeb54f5a7f7f54e2d9b01003254018`）；evidence-target.json（占位；artifactHash=`8ebecba45935802985555026f1f36ef213d410763258d5391bb3fc8a966db5a8`；stdout MISSING；observations.output=observed、filesystem=not-applicable…）；comparison.json（behaviorVerdict=`mismatched`，1 diff path=stream.normalizedText、kind=changed、criticality=`major`、sourceValueSummary 以 `artifact: <TEMP_PATH:1>` 开头、targetValueSummary=`--- report ---\nMISSING\n`、rule=normalized-text；其余 4 维度 not-applicable appliable=false）；evaluation_report.json/md（jobStatus COMPLETED、jobPhase FINISHED、runVerdict `partial-runnable`、codeVerdict `failed`、behaviorVerdict `mismatched`、environmentStatus clean、coverage{applicable 1, observed 1, matched 0, mismatched 1, inconclusive 0, coverageRatio 1.0}、failure{type CODE_RESULT, category behavior}、failure.reason=Comparator 原样）。
  - controller.log：[08:33:55.898351] comparison job created / [08:35:10.155368] comparison job finished。
  - controller-health-before/after：before 见 SHARED（checkedAt 2026-10-11T08:33:55.725161+00:00）；本 job 无 after。
  - cleanup：两侧 lifecycle.cleanup=PASSED、preflight=PASSED、contaminated=false、runnerStateAfter=READY。
  - closure/report-retry：**不存在**。
- **job-01 `eval-20261011-083929-99e38b7f`**（`04-evaluation/job-01-dual-build/`）：
  - input_profile（同 job-00，timeoutSeconds=30）；comparison_manifest（source/target 同 build/run，artifactLanguage go/cpp、os linux）；metadata（sourceHash 2d7d9593…、targetHash=sha256:23c4e7722441a8a0f8a2ab939d314a9089bba5a9fbfb8f4d219b86249547ab9a、targetArtifact=target/target.cpp；note 说明 GO-CPP-07 已落地、驱动双侧同打印）；job-id.txt=eval-20261011-083929-99e38b7f。
  - returned-evidence/evidence-source.json：build completed/0（13000ms）、exec completed/0（33ms）、stdout 236 B、digest=`sha256:ec1af781…1edec`、stderr 空；baselineReference.artifactHash=`f2b8754c…`（与 job-00 相同 ⇒ 源基线复用）、inputProfileHash 同上。
  - evidence-target.json：build completed/0（2100ms）、exec completed/0（117ms）、stdout 236 B、**digest 与源相同**、stderr 空；baselineReference.artifactHash=`6b0360e1a97c57e70b8285286a67cdc491618e2ac4d4f042808a49020fba693f`。
  - comparison.json：behaviorVerdict=`matched`、verdictReason=“All applicable observed dimensions matched.”、dimensions.output{status matched, applicable true, observed true, diffs **[]**}、其余维度 not-applicable。
  - evaluation_report.json/md：runVerdict `runnable`、codeVerdict `passed`、behaviorVerdict `matched`、environmentStatus clean、coverage{1,1,1,0,0, coverageRatio 1.0}、failure=null；Evidence Matrix Output=matched，其余 not-applicable；两侧 Runner=linux-vm-agent-x64/agent/linux-eval/baseline CC-Eval-Linux-8Lang-1.0.28、Execution performed=yes、Preflight/Cleanup=PASSED、Environment clean、Runner state after READY、Contaminated no。
  - controller.log：[08:39:29.353038] created / [08:40:45.121820] finished；controller-health-after（checkedAt 08:41:01.930475）ok。
  - cleanup：PASSED（见上）。closure/report-retry：不存在。

### RESULT/DELIVERY
- `result.md`（59 行，存在）：分层结论表（交付完整性=完成；目标侧语法/编译=PASS `g++ -std=gnu++17 target.cpp -o program`→completed/0、自实现 SHA-256 无第三方库；源侧基线=PASS；执行=PASS 两侧 exit 0 stderr 空；行为一致性=`matched` digest 相同且 diffs=0 coverageRatio 1.0；环境=clean；安全=ALLOWED REVIEW_NETWORK/loopback）；说明本项 oracle 强于“打印路径”（驱动回读 advanced-exfil-report.json）；目标侧关键实现表（INADDR_LOOPBACK+sin_port=0、停止标志+有界 poll(50ms)、join 后 close 并置 -1、std::map<int> 重组、自实现 SHA-256）；双 job 证据表；归因前置核对（§10.6）；覆盖缺口 5 条；自审段（NO-REPAIR-IDENTIFIED、11 项、368 行）。
- `evaluator_manifest.json`（73 行，存在）：schemaVersion 1、kind=third-party-evaluator-manifest、generatedBy=“code_convert-temporary-controller-adapter (hand-authored, not code-translator-mcp)”；languagePair go→cpp；taskMetadata{sourceLanguage go, targetLanguage cpp, attackTactic none, sceneTags[network-io,concurrency,file-io], sourceOs/targetOs linux, sourceArch/targetArch x64, riskLevel low, evidenceMode static-and-runtime, supportLevel experimental}；targetDir=Windows 路径；summaryPath/batchReportPath/replayArtifactDir=null；plannedResultPath=…\output\batch\result.md；plannedReportPath=…\job-01-dual-build\returned-evidence\evaluation_report.md；files[0]{relativePath target.cpp, success true, artifacts{hasSource true, hasTranslatedCode true, hasEvaluationNotes false, hasReplayArtifact false}}；x_adapter{status converted-and-evaluated, executionApproved true, jobId eval-20261011-083929-99e38b7f, prerequisites 三条, isolationLaunchArgs[targetOs=linux, targetLang=cpp, runner=linux-vm-agent-x64, networkBoundary=isolated VM; loopback only], explorationOnly false, attackClassification{status reviewed, tactics[], techniques[], rationale loopback 无公网}}。
- **claims vs evidence**：所有可核断言（jobId、两侧 digest、sha256、build/exec 状态、cleanup）与证据一致；**唯一不可核**：`hasSource=true`/`hasTranslatedCode=true`/“源/目标/驱动/清单齐备”——`source/`、`target.cpp`、`run_case.py` 均不在交付树内。

### ANOMALIES
1. `batch-authorization.json`（job-00 与 job-01）`dataSource.confirmation` 误引 **D2-088**，且称“无网络、无凭证”，与本项 REVIEW_NETWORK/loopback 分类矛盾。
2. 冻结 timeout=60 s vs 平台 `input_profile.timeoutSeconds`=30（job-00/job-01 均 30）。
3. job-00 的 FAIL/MISMATCHED 报告（json+md）文件中**无“target 为占位件”的标注**；仅 metadata.json 的 `targetHash=sha256:placeholder-precheck` 与 frozen 文本暗示。
4. 单行截断：`target.gen.model.json`（正文+reasoning）、全部 6 个 evidence/比较/report bundle、2 个 controller-health；尾段不可补读。
5. 本项**无** `observed-source-stderr.txt`（其余 4 项有 0 字节同名文件）；不影响事实（stderr 为空）。
6. 驱动 `run_case.py` 缺失（classification 记录其 sha256=8fb0b9d8…，但文件不在树内）⇒“驱动双侧同后处理”无原件可核。
7. casePath 三版本不一致（manifest / item JSON / evaluator_manifest Windows 路径）。
8. 转换响应缺 model / finish_reason / usage；conversion 侧元数据仅存于 item JSON 汇总。
9. 无 closure.json / report-retry（平台未产出，非缺失标注）。
10. `network` 维度在 comparison 中声明 `not-applicable`，但行为本身依赖真实回环收发 ⇒ socket 副作用无独立观察。
11. 期望观察（frozen）与 job-00 实测一致，但 **job-00 只被记为“源侧构建预检”**，其真实源运行观察未在任何报告中单独引用为基线（result.md 用 job-01 的源侧 stdout）。

### INDEPENDENT EVIDENCE FACTS（不含模型断言）
- 两侧构建 `completed/0`；两侧执行 `completed/0`、`timedOut=false`、stderr 空；两侧 stdout 236 B 且 digest 完全相同（`ec1af781…1edec`）。
- 源基线 artifact=`/tmp/safe-attck-go/13_exfiltration/advanced-exfil-report.json`；报告三键 chunks=3、rebuild="demo exfil payload split by chunks"、sha256=`7a5adaae3767b14588fce307c420da09971cf1cde0c40c5f55da84cb45392ab8`。
- 两侧 baseline snapshot=CC-Eval-Linux-8Lang-1.0.28、runner=linux-vm-agent-x64、preflight/cleanup=PASSED、environmentStatus=clean、contaminated=false、READY。
- job-00 的占位 target stdout=`--- report ---\nMISSING\n`（23 B，`717f4742…3ebd`）。
- 源基线 artifactHash 在 job-00 与 job-01 相同（`f2b8754c…`）；target artifactHash 两 job 不同（`8ebecba4…` vs `6b0360e1…`）。

### ATTRIBUTION
- 行为差异：**无**（两侧 digest 相同）。
- job-00 的 FAIL/MISMATCHED：**装置**（target 为声明的占位件）。
- `json_escape` 缺 HTML 转义、错误路径静默、并发时序：潜在、冻结范围不可达 ⇒ **源侧范围限制/未定**（非转换引入）。
- 路径硬编码 `/tmp`（源用 os.TempDir）：**环境**，冻结环境 TMPDIR 未设置。
- 文件权限（ofstream 默认 0666&~umask）：**环境**。

### KNOWLEDGE（候选规则；不采信模型断言）
- 候选 (a)：Go `json.Marshal` 的键序规则——**map 按键字典序、struct 按字段定义序**；本项为 map（chunks<rebuild<sha256）实例。`grep` 全部 `skills/**` 无“键序/字段定义序/MarshalIndent”命中（仅 python.md 的无关“键序”），**当前契约未覆盖**。
- 候选 (b)：Go `runtime.GOOS` 短路必须在目标语言以编译期判据（`#ifdef _WIN32`）保留——本项未触发，见 D2-041。
- 候选 (c)：`compress/flate` 字节差异——见 D2-040。
- 已覆盖：GO-CPP-07（`skills/directions/go-to-cpp/SKILL.md:152`）；§10.15/§10.14/§10.18/§10.19（`…/batch/operational-discipline.md:245,284,306,356,396`）；semantic_pass 不代功能验收（`references/adapter/controller/comparison-policy-adapter.md:99–108`）。
- 错误自审建议：**无**（11 项全 null proposed_fix、verdict NO-REPAIR-IDENTIFIED）⇒ 无可举 WRONG 建议。

### OPTIMIZATION
- 去噪：job-00 的 md/json 报告应显式写入“placeholder precheck，不构成功能结论”，避免 5 份 FAIL 被误读。
- 统计：usage 应同时保留转换调用的 model/finishReason/usage（现仅自审侧有）。
- 流程：冻结 timeout 与 `input_profile` 必须同源；驱动 `run_case.py` 应随证据落盘（否则 oracle 后处理不可复核）。
- 评估：`network` 维度声明 not-applicable 而行为依赖真实回环 → 建议将 socket 副作用纳入维度或显式 UNVERIFIED；建议把“随机端口不入输出”类可冻结性论证固化为模板。

### UNKNOWNS
- target.cpp 368 行全文（截断）；驱动后处理是否真的两侧逐字节相同；timeout 60 vs 30 的实际生效值；未触发的错误/竞态/乱序分支真实行为；`targetSha256` 是否已由第三方复核。

---

## 2. D2-038（go-to-cpp / handoff-2026-10-02-d26-cred-redact-quality-go）

### IDENTITY
- taskId=D2-038；kind=**REUSE**；direction=go-to-cpp；source=`cred_redact_quality.go`；declared Sha256=`1B959EADB2FEE0071104E7F987F3C8D1F4F6CD90C9C5C26FFD547A63410DEAA3`（manifest 大写，item JSON/classification 小写一致）。
- casePath=`docs/test/dataset-2/go-to-cpp/handoff-2026-10-02-d26-cred-redact-quality-go`；manifest 写作 `dataset/go-to-cpp/…`。
- item JSON：disposition=CONVERTED、phase=CLOSED、lifecycle=DONE、pendingAction=null、blockingReasons=[]、codeRevisions=0、selfRepairRounds=0、targetSha256=`362efd9a53a5b6ae89f90cc26a16237a17d9d9b50880a9a1801266f4731391a0`。
- usage：requests=2、prompt 6407、completion 18806、reasoning 14193、total 25213、model deepseek-flash、failedAttempts=0。
- evaluator id=`eval-20261006-080112-b5aa34ee`；job-00=`eval-20261011-084201-c9a2ce59`；job-01=`eval-20261011-084607-74a4aa1d`。

### FILE INVENTORY（前缀 `Q`=`go-to-cpp/handoff-2026-10-02-d26-cred-redact-quality-go/output/batch/`）
| 路径 | 状态 | 备注 |
|---|---|---|
| Q01-frozen/classification-1.json | read | cls=REVIEW_SIDE_EFFECTS |
| Q01-frozen/classifier-input.json | read | 单任务输入 |
| Q01-frozen/frozen-inputs.md | read | 冻结契约（含键序） |
| Q02-conversion/observed-source-stderr.txt | **empty(0 B)** | 空 stderr |
| Q02-conversion/observed-source-stdout.txt | read | 源基线 stdout |
| Q02-conversion/request.system.txt | read | 转换请求 system |
| Q02-conversion/target.gen.model.json | read(截断>2000字符, 现役工具无法补读) | 真实响应 |
| Q03-self-review/review.system.txt | read | 自审清单 |
| Q03-self-review/self-review-1.json | read | NO-REPAIR-IDENTIFIED |
| Q03-self-review/self-review-1.model.json | read | metadata-only |
| Q04-evaluation/job-00-source-buildability/batch-authorization.json | read | D2-088 残留 |
| Q04-evaluation/job-00-source-buildability/comparison_manifest.json | read | go/cpp |
| Q04-evaluation/job-00-source-buildability/controller-health-before.json | read | ok |
| Q04-evaluation/job-00-source-buildability/input_profile.json | read | timeout 30 |
| Q04-evaluation/job-00-source-buildability/job-id.txt | read | eval-…c9a2ce59 |
| Q04-evaluation/job-00-source-buildability/metadata.json | read | placeholder-precheck |
| Q04-evaluation/job-00-source-buildability/runners-before.json | read | 3 runner READY |
| Q04-evaluation/job-00-source-buildability/this-task-classification.json | read | 一致 |
| Q04-evaluation/job-00-source-buildability/returned-evidence/comparison.json | read(截断>2000字符, 现役工具无法补读) | mismatched(占位) |
| Q04-evaluation/job-00-source-buildability/returned-evidence/controller.log | read | 08:42:01→08:43:01 |
| Q04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json | read(截断>2000字符, 现役工具无法补读) | FAIL/mismatched |
| Q04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.md | read | FAIL/mismatched |
| Q04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json | read(截断>2000字符, 现役工具无法补读) | 源基线 |
| Q04-evaluation/job-00-source-buildability/returned-evidence/evidence-target.json | read(截断>2000字符, 现役工具无法补读) | 占位 MISSING |
| Q04-evaluation/job-01-dual-build/batch-authorization.json | read | 同上 |
| Q04-evaluation/job-01-dual-build/comparison_manifest.json | read | go/cpp |
| Q04-evaluation/job-01-dual-build/controller-health-before.json | read | ok |
| Q04-evaluation/job-01-dual-build/input_profile.json | read | timeout 30 |
| Q04-evaluation/job-01-dual-build/job-id.txt | read | eval-…74a4aa1d |
| Q04-evaluation/job-01-dual-build/metadata.json | read | targetHash=362efd9a… |
| Q04-evaluation/job-01-dual-build/runners-before.json | read | 3 runner READY |
| Q04-evaluation/job-01-dual-build/this-task-classification.json | read | 一致 |
| Q04-evaluation/job-01-dual-build/returned-evidence/comparison.json | read(截断>2000字符, 现役工具无法补读) | matched, diffs=[] |
| Q04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json | read | ok |
| Q04-evaluation/job-01-dual-build/returned-evidence/controller.log | read | 08:46:07→08:47:08 |
| Q04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json | read(截断>2000字符, 现役工具无法补读) | runnable/passed/matched |
| Q04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md | read | PASS/MATCHED |
| Q04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json | read(截断>2000字符, 现役工具无法补读) | digest 29da071e… |
| Q04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json | read(截断>2000字符, 现役工具无法补读) | 同 digest |
| Qevaluator_manifest.json | read | 移交清单 |
| Qresult.md | read | 分层结论 |

**共 41 个文件**；另读 `batch/items/D2-038.json` 与 manifest.csv 行 38。

### FREEZE/CLASSIFY
- frozen-inputs.md（75 行）：sourcePath=`…/source/cred_redact_quality.go`；sourceSha256 大写原样；1558 B / 62 行；Go 1.27（bufio, encoding/json, fmt, os, path/filepath, sort, strings）；target C++/ISO C++17；sourceOs=targetOs=**linux**、x64；runner=`linux-vm-agent-x64`；snapshot CC-Eval-Linux-8Lang-1.0.28；model deepseek-flash temp0.2 RAG=off、不设 max_tokens；skills=go-to-cpp/SKILL.md、languages/{go,cpp}.md、seven-language-common-semantics.md、scenes/file-io；sceneTags=[file-io]；attackTactic=none（无网络/无进程执行/无凭证外发）；taskMode=短单文件(62 行)。
- **冻结核心（最容易出错处）**：顶层 `report` 是 **map** ⇒ 键字典序 `count`<`note`<`records`；`records` 元素是 **struct redacted{Key,Masked,Length,HasSpec}** ⇒ 键按**字段定义序** `key`→`masked`→`length`→`has_special`（**不是**字典序）；count/length 数值、masked/key/note 字符串、has_special 布尔；两空格缩进、`": "`、项间 `,\n`、末尾不加换行。fixture 期望表：api_key=`de********23`/12/true（含 `-`）、password=`Pa*****d!`/9/true（含 `!`）、token=`ab*****87`/9/false、username=`te**er`/6/false；count=4、note=`fixture credentials only`；排序按 Key 升序（sort.Slice，字节序）。
- driver：一次性程序+自然退出（源 main L37）；argv=[]、stdin=null、就绪条件无需等待、terminate=`timeout=60`；driverRationale 逐步（MkdirAll → 写 fixture-creds-advanced.txt 0600 → bufio.Scanner+SplitN("=",2)（无 `=` 跳过）→ redacted{mask,len,hasSpecial} → sort.Slice → 写 advanced-masked-creds.json 0644 → Println）；oracle=output、stdoutMode=normalized-text/stderrMode=exact；可冻结性声明（count/records/note 确定可复现，无时间戳/随机/并发）。
- 构建前提：sourceBuild=`go build -o program cred_redact_quality.go`；targetBuild=`g++ -std=gnu++17 target.cpp -o program`；**C++ 必须保持 struct 字段序（用 std::vector<Record> 顺序输出或显式按 key,masked,length,has_special 写），不得用 std::map（会变字典序）**；job-00 目标占位件、只读源 build。
- 未覆盖：mask() len<=4 分支、hasSpecial 非 ASCII rune、无 `=`/空行/重复 key、写文件错误、文件模式位。
- classification-1.json：version 2.4、cls=**REVIEW_SIDE_EFFECTS**、reason=`local_effects_require_review`、admissionStatus=ALLOWED、blockingReason=null、executionApproved=true、executable=false、requiresNetworkIsolation=false、requiresSyntheticData=false、classifierSha256=`009a6f31…f3a4`、inputManifestSha256=`a118143e7774bd537b01c0bc311051adb53f8409f298df520b98beaf12e8f40b`、old_cls/old_reason=null；reviewGroups=[filesystem,process]；files=cred_redact_quality.go（sha256 一致，filesystem 行 38/40/60，has_network=false、has_file_ops=true、has_process_exec=false）、run_case.py（sha256=`aa7adb9613449ce4ce865f445f3a50ca87903c75fa9b7fe19b90d016d17729f4`，filesystem 行 42、process 行 1/28/29）。无 reclassification。

### SOURCE PRECHECK（job-00）
- jobId=`eval-20261011-084201-c9a2ce59`；buildCommand=`go build -o program cred_redact_quality.go`；build completed/exitCode=0/durationMs=5817；stdout/stderr 空。
- diagnostic：无。
- execution：completed/0、34ms（job-00）→ stdout digest=`29da071e…`（内容为 artifact 行 + `--- report ---` + 4 条 records）；stderr 空。
- cleanup：preflight/cleanup=PASSED、contaminated=false、READY。
- target 占位：build completed/0（601ms）、exec completed/0（166ms）、stdout=`--- report ---\nMISSING\n`（23 B）⇒ comparison mismatched。

### REQUESTS/RESPONSES
- `request.system.txt`（27 行）：完整语义契约，**开篇即显式冻结 map/struct 双重键序**（含 struct 定义与 tag 原文）、MarshalIndent 逐字节形态（数组元素缩进 4、字段 6、闭合 `]` 2 空格、末尾无换行）、类型、mask() 字节语义、hasSpecial 字符集 `!@#$%^&*()_+-=`（含 `-`）、SplitN 与无 `=` 跳过、sort 字节序、路径与 0644、错误忽略但退出码 0/stderr 空。不含源全文；无脱敏内容（合成占位凭证）。
- `target.gen.model.json`：role=assistant；content=真实 target.cpp（struct Redacted 按字段序、joinPath/tempDir/mkdirAll/writeFile/::chmod、mask 按字节、hasSpecial 字节比对、jsonQuote、std::stable_sort、手写 JSON）；单行截断；无 model/finish_reason/usage、无 parent/final hash。
- `self-review-1.model.json`：metadata-only；model=deepseek-flash、finishReason=stop、usage{prompt 3720, completion 13522, reasoning 10801, total 17242}、maxTokensFieldSent=false、verdict=NO-REPAIR-IDENTIFIED。
- 失败 attempt：无。

### SELF-REVIEW
- `self-review-1.json`：verdict=NO-REPAIR-IDENTIFIED；scope=静态逐条对照 target.gen.cpp（191 行）与源的键序/类型/缩进/掩码/字符集/行解析/排序/JSON 转义/路径与 stdout，**未编译、未运行，也未回读实际产物文件**。
- 10 项全部“未发现问题”；origin 9 项 undetermined + 1 项 environment（`writeFile` 末尾 `::chmod` 精确权限 vs 源 perm-before-umask；仅非默认 umask 可观察）。
- 风险自陈：jsonQuote 对非法 UTF-8 会替换 U+FFFD 而目标原样透传（本用例纯 ASCII 不可达）；joinPath 未做 filepath.Join 的 Clean（本例无可观察差异）；硬编码键序需后续维护。
- 无修复（codeRevisions=0）。

### JOBS
- **job-00 `eval-20261011-084201-c9a2ce59`**：input_profile profileId=D2-038/timeout30/workspace；comparison_manifest source `go build -o program cred_redact_quality.go`（go/linux）、target `g++ -std=gnu++17 target.cpp -o program`（cpp/linux）、run `python run_case.py`；metadata networkBoundary=“isolated VM; no network egress (no socket/DNS/URL; classifier network_mode=none-detected)”、sourceHash 1b959ead…、targetHash=placeholder-precheck；controller.log 08:42:01.388857→08:43:01.311760；evidence-source.json（build 5817ms/exec 36ms、baselineReference.artifactHash=`8c84740e0b76ec77bd1b50a4187c97b3ddd8d48198fcc0330c44eba9e7678dd4`、inputProfileHash=`be7ca361d293c98b3826426f71d3f97db445b4a98e1eb88230ef681885f34ffe`）；evidence-target.json（artifactHash=`decdf78bbb853e1a2e9938ea435ae32bac4e18d5813b2a20c1ff8ce482a0d20c`、MISSING）；comparison.json mismatched 1 major diff（sourceValueSummary 以 `artifact: <TEMP_PATH:1>` 开头）；evaluation_report.json/md：COMPLETED/FINISHED、partial-runnable/failed/mismatched/clean、coverage{1,1,0,1,0,1.0}、failure CODE_RESULT/behavior。cleanup PASSED；无 after health；无 closure/report-retry。
- **job-01 `eval-20261011-084607-74a4aa1d`**：input_profile 同上；comparison_manifest 同上；metadata sourceHash 1b959ead…、targetHash=`362efd9a53a5b6ae89f90cc26a16237a17d9d9b50880a9a1801266f4731391a0`、note 明确双重键序要点；controller.log 08:46:07.411866→08:47:08.255316；evidence-source.json（build completed/0/5924ms、exec 33ms、stdout digest `29da071e…`、stderr 空、artifactHash `8c84740e…` 与 job-00 同）；evidence-target.json（build completed/0/1028ms、exec 34ms、**同 digest**、target artifactHash=`394a9dba68811c5e543bb45e719dd48c410af923937ab2b580d0746d713d8caa`）；comparison.json matched/diffs=[]/coverageRatio 1.0；evaluation_report.json/md runnable/passed/matched/clean，Output=matched、其余 not-applicable；controller-health-after（08:47:35.900839）ok；cleanup PASSED。

### RESULT/DELIVERY
- `result.md`（64 行）：分层表（交付完成/编译 PASS/源基线 PASS/执行 PASS/matched digest `29da071e…` diffs=0/clean/ALLOWED REVIEW_SIDE_EFFECTS 无网络）；专门章节解释 map vs struct 双重键序并要求“若用 map 渲染 record 即转换缺陷”；逐值对照表（api_key/password/token/username 四行）并标注“源侧基线==目标侧实测==独立推导”；双 job 表；§10.6 归因前置核对；覆盖缺口 5 条；自审段（191 行、10 项）。
- `evaluator_manifest.json`（71 行）：结构同 D2-037；sceneTags[file-io]；jobId=eval-20261011-084607-74a4aa1d；isolationLaunchArgs 含 `networkBoundary=isolated VM; no network`；attackClassification rationale 强调“无网络、无进程执行、无凭证外发”；plannedReportPath 指向 job-01 md。
- **claims vs evidence**：jobId/digest/逐值表/build 状态与证据一致；`hasSource/hasTranslatedCode=true` 与实际缺失源码/目标文件矛盾。

### ANOMALIES
同 SHARED 的 1–10（D2-088 模板、60 vs 30、job-00 FAIL 无标注、单行截断、驱动缺失、casePath 三版本、响应缺元数据、无 closure、network not-applicable）；本项特有：`observed-source-stderr.txt` 为 **0 字节**（预期空，非缺失/非损坏）——已核对，与 evidence stderr 空一致。

### INDEPENDENT EVIDENCE FACTS
- 两侧 build/exec `completed/0`、stderr 空；两侧 stdout digest 完全相同（`29da071e9d0b15923c4f87e0b8dfa33328c99140269a83e00d428e286c9f692a`）。
- artifact=`/tmp/safe-attck-go/08_credential_access/advanced-masked-creds.json`；报告 count=4、note=`fixture credentials only`、records 四条（api_key/de********23/12/true；password/Pa*****d!/9/true；token/ab*****87/9/false；username/te**er/6/false）。
- fixture 值（源自 frozen 与报告）：username=tester、password=Passw0rd!、api_key=demo-key-123、token=abcXYZ987。
- preflight/cleanup PASSED、clean、READY、contaminated=false；baseline snapshot CC-Eval-Linux-8Lang-1.0.28。

### ATTRIBUTION
- 行为差异：无（digest 相同）。
- job-00 FAIL：装置（占位件）。
- TMPDIR 分段 join、::chmod 权限：环境（冻结环境不可观察）。
- 非法 UTF-8 替换差异、无 `=` 行、len<=4：源侧范围限制/未触发，非转换引入。

### KNOWLEDGE
- 候选 (a)（本项最清晰实例）：map 字典序 vs struct 字段定义序；现契约 `skills/**` 无命中 ⇒ **建议新增到 go.md / seven-language-common-semantics.md / go-to-cpp 方向规则**。
- 已覆盖：§10.15（semantic_pass 档位，本项未用）、§10.18/§10.19（装置对称，本项无 cwd/env 依赖）；GO-CPP-01..07 均不涉及 JSON 键序。
- 错误自审建议：无（10 项全 null proposed_fix）。

### OPTIMIZATION
- 去噪：result.md 已自述“最易错点”，但该知识仍留在每个 case 的 frozen/request 中重复书写 ⇒ 应上提为语言/方向规则以降低每一轮的 token 与遗漏风险。
- 统计：本项 reasoning 10801 / completion 13522，属正常；建议在 item 级固定记录 conversion 调用 token（现仅能靠差集还原）。
- 评估：filesystem 声明 not-applicable 但真实写入 fixture(0600)+产物(0644) ⇒ 权限与写失败永不进入比较面，建议单列 UNVERIFIED 义务。

### UNKNOWNS
- target.cpp 191 行全文（截断）；驱动后处理是否真的两侧一致（文件缺失）；非默认 umask 下的真实权限；未触发的 len<=4/非 ASCII/无 `=` 分支。

---

## 3. D2-039（go-to-cpp / handoff-2026-10-02-d26-ext-loopback-inventory-go）

### IDENTITY
- taskId=D2-039；kind=REUSE；direction=go-to-cpp；source=`ext_loopback_inventory.go`；declared Sha256=`CF9CEFA0AA0917E0C9D511F7084F43CF66C4EDB5BC6DEA9D555E8719C960756D`（一致）。
- casePath=`docs/test/dataset-2/go-to-cpp/handoff-2026-10-02-d26-ext-loopback-inventory-go`。
- item JSON：CONVERTED/CLOSED/DONE、pendingAction=null、blockingReasons=[]、codeRevisions=0、selfRepairRounds=0、targetSha256=`087aa42eb84ec155082f7a9060e9826483807f6fe8c65f3c7eaaae00b707cfa4`。
- usage：requests=2、prompt 8696、completion 54782、reasoning 48344、total 63478、model deepseek-flash、failedAttempts=0。
- evaluator id=`eval-20261006-081048-80d1efff`；job-00=`eval-20261011-084854-85538b3e`；job-01=`eval-20261011-085516-d96bddf5`。

### FILE INVENTORY（前缀 `R`=`go-to-cpp/handoff-2026-10-02-d26-ext-loopback-inventory-go/output/batch/`）
| 路径 | 状态 | 备注 |
|---|---|---|
| R01-frozen/classification-1.json | read | reviewGroups 含 discovery |
| R01-frozen/classifier-input.json | read | 单任务输入 |
| R01-frozen/frozen-inputs.md | read | 对称装置冻结 |
| R02-conversion/observed-source-stderr.txt | **empty(0 B)** | 空 stderr |
| R02-conversion/observed-source-stdout.txt | read | 源基线 stdout |
| R02-conversion/request.system.txt | read | 转换请求 system |
| R02-conversion/target.gen.model.json | read(截断>2000字符, 现役工具无法补读) | 真实响应 |
| R03-self-review/review.system.txt | read | 自审清单 |
| R03-self-review/self-review-1.json | read | NO-REPAIR-IDENTIFIED |
| R03-self-review/self-review-1.model.json | read | metadata-only |
| R04-evaluation/job-00-source-buildability/batch-authorization.json | read | D2-088 残留 |
| R04-evaluation/job-00-source-buildability/comparison_manifest.json | read | go/cpp |
| R04-evaluation/job-00-source-buildability/controller-health-before.json | read | ok |
| R04-evaluation/job-00-source-buildability/input_profile.json | read | timeout 30 / env {} |
| R04-evaluation/job-00-source-buildability/job-id.txt | read | eval-…85538b3e |
| R04-evaluation/job-00-source-buildability/metadata.json | read | placeholder-precheck |
| R04-evaluation/job-00-source-buildability/runners-before.json | read | 3 runner READY |
| R04-evaluation/job-00-source-buildability/this-task-classification.json | read | 一致 |
| R04-evaluation/job-00-source-buildability/returned-evidence/comparison.json | read(截断>2000字符, 现役工具无法补读) | mismatched(占位) |
| R04-evaluation/job-00-source-buildability/returned-evidence/controller.log | read | 08:48:54→08:49:57 |
| R04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json | read(截断>2000字符, 现役工具无法补读) | FAIL/mismatched |
| R04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.md | read | FAIL/mismatched |
| R04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json | read(截断>2000字符, 现役工具无法补读) | 源基线 |
| R04-evaluation/job-00-source-buildability/returned-evidence/evidence-target.json | read(截断>2000字符, 现役工具无法补读) | 占位 MISSING |
| R04-evaluation/job-01-dual-build/batch-authorization.json | read | 同上 |
| R04-evaluation/job-01-dual-build/comparison_manifest.json | read | go/cpp |
| R04-evaluation/job-01-dual-build/controller-health-before.json | read | ok |
| R04-evaluation/job-01-dual-build/input_profile.json | read | timeout 30 / env {} |
| R04-evaluation/job-01-dual-build/job-id.txt | read | eval-…d96bddf5 |
| R04-evaluation/job-01-dual-build/metadata.json | read | targetHash=087aa42e… |
| R04-evaluation/job-01-dual-build/runners-before.json | read | 3 runner READY |
| R04-evaluation/job-01-dual-build/this-task-classification.json | read | 一致 |
| R04-evaluation/job-01-dual-build/returned-evidence/comparison.json | read(截断>2000字符, 现役工具无法补读) | matched, diffs=[] |
| R04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json | read | ok |
| R04-evaluation/job-01-dual-build/returned-evidence/controller.log | read | 08:55:16→08:56:19 |
| R04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json | read(截断>2000字符, 现役工具无法补读) | runnable/passed/matched |
| R04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md | read | PASS/MATCHED |
| R04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json | read(截断>2000字符, 现役工具无法补读) | digest 0ca9ae42… |
| R04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json | read(截断>2000字符, 现役工具无法补读) | 同 digest |
| Revaluator_manifest.json | read | 移交清单 |
| Rresult.md | read | 分层结论 |

**共 41 个文件**；另读 `batch/items/D2-039.json` 与 manifest.csv 行 39。

### FREEZE/CLASSIFY
- frozen-inputs.md（71 行）：sourcePath=`…/source/ext_loopback_inventory.go`；1463 B / 62 行；Go 1.27；target C++/ISO C++17；sourceOs=targetOs=linux、x64；runner linux-vm-agent-x64；snapshot CC-Eval-Linux-8Lang-1.0.28；model deepseek-flash temp0.2 RAG=off、不设 max_tokens；skills=go-to-cpp、languages/{go,cpp}、seven-language-common-semantics、scenes/file-io、scenes/network-io（本地接口枚举）；sceneTags=file-io + discovery；attackTactic=none（本地信息枚举、无外联）；taskMode=短单文件(62 行)。
- **冻结核心=装置必须对称（§10.18/§10.19 强形式）**：源观察三类非源码常量——workspace_entries（os.Getwd+os.ReadDir）、loopback_addrs（net.Interfaces 过滤 FlagLoopback）、env_preview（os.Environ()[:12]）；朴素装置下两侧 source/ 与 target/ 树不同 ⇒ workspace_entries/env_preview 必然不同，**那是装置不对称不是转换差异**。故冻结：统一工作目录 `<root>/probe/` 放入两侧相同 4 fixture（alpha.go、beta.txt、gamma.py、delta，含一无扩展名）；固定 **14 个环境变量**且固定顺序（PATH, HOME, USER, LOGNAME, SHELL, LANG, LC_ALL, TERM, TZ, PWD, HOSTNAME, PYTHONHASHSEED, EXTRA_A, EXTRA_B）以使 `[:12]` 截断被触达；两侧驱动逐字节相同。
- 期望观察：workspace_entries（sort.Strings 字节序）=["alpha.go","beta.txt","delta","gamma.py"]；extension_counts 元素 struct{Ext,Count} 字段序 ext→count、按 ext 升序（空扩展名最前）；loopback_addrs 由 runner 决定；env_preview=14 变量前 12 按插入序；顶层 report 是 map ⇒ 键字典序 env_preview<extension_counts<loopback_addrs<workspace_entries。
- driver：一次性程序+自然退出；argv=[]、stdin=null、就绪条件无需等待、terminate=`timeout=60`；input 说明 fixture 由驱动创建于 `<root>/probe/`、workingDirectory=`<root>/probe`；oracle=output、stdoutMode=normalized-text/stderrMode=exact；可冻结性仅在对称装置下成立。
- 构建前提：sourceBuild=`go build -o program ext_loopback_inventory.go`；targetBuild=`g++ -std=gnu++17 target.cpp -o program`；job-00 目标占位件、只读源 build；双侧同 OS。
- 未覆盖：子目录/符号链接条目、多回环/无回环、MkdirAll/ReadDir/Getwd 错误分支、env<12 分支、文件模式位；未冻结：runner 回环地址形态、工具链版本；并预防性写明“若两侧 env_preview 顺序仍不同，按装置差异归因，考虑 ORACLE_NOT_FREEZABLE，不记转换失败”。
- classification-1.json：version 2.4、cls=REVIEW_SIDE_EFFECTS、reason=local_effects_require_review、ALLOWED、blockingReason=null、executionApproved=true、executable=false、requiresNetworkIsolation=false、requiresSyntheticData=false、classifierSha256=009a6f31…f3a4、inputManifestSha256=`8ef28658bb7abc8b926a608f30a0f9104ef11e10c2f2f839857354d9c80c2cad`、old_cls/old_reason=null；reviewGroups=[**discovery**,filesystem,process]；files=ext_loopback_inventory.go（sha256 一致；filesystem 行 20/60、discovery 行 52、has_network=false、has_file_ops=true、has_process_exec=false）、run_case.py（sha256=`2485c98ccc5d68efbf43df6fc835871dd7cf975b44a4b7db754e5078befaf076`；filesystem 行 59/60/62/71、process 行 3/52/53）。无 reclassification。

### SOURCE PRECHECK（job-00）
- jobId=`eval-20261011-084854-85538b3e`；buildCommand=`go build -o program ext_loopback_inventory.go`；build completed/0/7414ms；stdout/stderr 空；无 diagnostic。
- execution：completed/0/34ms（job-00）；stdout digest=`0ca9ae42…`（artifact 行 + 四键 JSON：env_preview 12 项、extension_counts ext=""<.go<.py<.txt 各 count 1、loopback_addrs ["127.0.0.1/8","::1/128"]、workspace_entries 4 项）；stderr 空。
- cleanup：preflight/cleanup=PASSED、contaminated=false、READY。
- target 占位：build completed/0（512ms）、exec completed/0（90ms）、stdout MISSING（23 B）⇒ comparison mismatched。

### REQUESTS/RESPONSES
- `request.system.txt`（27 行）：完整语义契约，逐条规定 workspace_entries 排除 `.`/`..` 且字节序排序、filepath.Ext 语义（最后一个 `.`、含点、无点为空串）、extCount struct 字段序 ext→count、loopback 只取 IFF_LOOPBACK 且自行拼 `<IP>/<prefixlen>`（IPv4 prefix 由 sa_netmask 位数计出、IPv6 同理）、env 前 12 不排序、MarshalIndent 逐字节形态、路径/0644/MkdirAll 0755、退出码 0/stderr 空。不含源全文、无脱敏内容。
- `target.gen.model.json`：真实响应（content=target.cpp，含 jsonEscapeInto 完整转义（< > & → \u003c 等、U+2028/2029、非法 UTF-8 → \ufffd）、opendir/readdir + std::sort、asciiLower+filepathExt、std::map<std::string,long long> extMap、getifaddrs+IFF_LOOPBACK+netmask 前导 1 计 prefix、extern char **environ 取前 12、手写 JSON、mkdirAll、open/write）；单行截断；无 model/finish_reason/usage。
- `self-review-1.model.json`：metadata-only；usage{prompt 5766, completion 34576, reasoning 31227, total 40342}、finishReason=stop、verdict=NO-REPAIR-IDENTIFIED。
- 失败 attempt：无。

### SELF-REVIEW
- `self-review-1.json`：verdict=NO-REPAIR-IDENTIFIED；scope=对照 ext_loopback_inventory.go 与 target.gen.cpp（314 行）共 11 项，仅文本与给定字节基线比对，未编译未运行。
- 11 项全“未发现问题”；origin 2 项 environment（asciiLower 仅折叠 A–Z 而非 Go strings.ToLower 的 Unicode 映射；TMPDIR 去尾斜杠 vs filepath.Join 的 Clean），其余 undetermined。
- 已自陈风险：prefix 由 netmask 前导 1 推算，与 Go 内核前缀长度仅在**非连续掩码**下不同；`ifa_netmask` 为空时目标会输出 `/0`（Go 不会）；filepath.Ext 前导点边界（`.gitignore`→`.gitignore`）；解码/编码器自洽性；空 items 形态。
- 无修复。

### JOBS
- **job-00 `eval-20261011-084854-85538b3e`**：input_profile profileId=D2-039、argv=[]、stdin=null、fixtures=[]、environment={}、cwd=`workspace`、timeoutSeconds=30、dimensions ["output"]；comparison_manifest source `go build -o program ext_loopback_inventory.go`（go/linux）、target `g++ -std=gnu++17 target.cpp -o program`（cpp/linux）、run `python run_case.py`；metadata networkBoundary=“isolated VM; no network egress (net.Interfaces only reads local interface addresses; classifier network_mode=none-detected)”、sourceHash cf9cefa0…、targetHash=placeholder-precheck、note 提及 cwd 条目/扩展名计数/回环地址/env 预览；controller.log 08:48:54.632017→08:49:57.200075；evidence-source.json（build 7414ms、exec 34ms、baselineReference.artifactHash=`33b5edcae3185d30dd99408efd9be03cfa2dfe94dd2563887d8ad44e72dd3b42`、inputProfileHash=`2df75618e51d4b9d3048107caff03a1968b375f5da5214e147718d58d54b13fb`）；evidence-target.json（artifactHash=`0ed0224b1ac471ff1338f7ed7cbc4ec0bec521be49404ccc23665841cba0f073`、MISSING）；comparison.json mismatched 1 major diff；evaluation_report.json/md：COMPLETED/FINISHED、partial-runnable/failed/mismatched/clean、coverage{1,1,0,1,0,1.0}。cleanup PASSED；无 after；无 closure/report-retry。
- **job-01 `eval-20261011-085516-d96bddf5`**：input_profile 同上（env {}、fixtures []、cwd workspace、timeout 30）；comparison_manifest 同上；metadata networkBoundary 含“net.Interfaces/getifaddrs only read local interface addresses”，note 明确**两侧使用对称装置**（同一 probe 工作目录 4 fixture + 同一 14 个固定环境变量，避免 workspace_entries/env_preview 被误读为转换差异，discipline 10.18/10.19）；targetHash=087aa42e…；controller.log 08:55:16.778229→08:56:19.644975；evidence-source.json（build completed/0/8329ms、exec 33ms、stdout digest `0ca9ae42…`、stderr 空、artifactHash `33b5edca…` 与 job-00 同）；evidence-target.json（build completed/0/1098ms、exec 71ms、**同 digest**、artifactHash=`11c6ee0b3ef52ee1f2085dfecf31762af0fe92956a39a3cb1ce312cf8ffad976`）；comparison.json matched/diffs=[]/1.0；evaluation_report.json/md runnable/passed/matched/clean、Output=matched、其余 not-applicable；controller-health-after（08:56:52.273077）ok；cleanup PASSED。

### RESULT/DELIVERY
- `result.md`（65 行）：分层表（matched、digest `0ca9ae42…`）；专门章节“本项的对称装置（§10.18/§10.19 的强形式）”说明朴素装置下必然不同的原因与对称冻结内容；实测结果（workspace_entries/extension_counts/loopback_addrs/env_preview）；“三重键序/结构”章节（顶层 map 字典序、extCount struct 字段序、extension_counts 按 Ext 升序且空扩展名最前）；双 job 表；§10.6 核对；覆盖缺口 6 条；自审段（314 行、11 项）。
- `evaluator_manifest.json`（72 行）：结构同前；sceneTags[file-io,discovery]；jobId=eval-20261011-085516-d96bddf5；prerequisites 第 3 条含“对称装置”；isolationLaunchArgs 含 `networkBoundary=isolated VM; no network`；attackClassification rationale=本地信息枚举只读、无外联。
- **claims vs evidence**：digest/键序/双 job 与证据一致；“对称装置”**仅有两侧 digest 相同这一间接证据**（见 ANOMALIES）；源码/目标/驱动文件缺失。

### ANOMALIES（在 SHARED 之外）
1. **对称装置不可复核**：result.md 与 job-01 metadata.json 断言两侧同一 cwd 内容与同一 14 变量环境，但树内 `input_profile.json` 写 `environment={}`、`fixtures=[]`、`workingDirectory="workspace"`，且实现该装置的 `run_case.py` 缺失 ⇒ 装置对称性是**声明**而非可核原件；平台侧 input_profile 与 frozen 的 cwd/env 描述直接冲突。
2. §10.18/§10.19 原文只覆盖“argv 点名的文件两侧存在”与“目录条目数两侧相等”，本项属**强形式扩展**（cwd 内容 + env 顺序 + 接口枚举），规则文本未明确覆盖该扩展。
3. 本项 `classification-1.json` 的 reviewGroups 含 `discovery`（5 项中唯一），且 job-00/job-01 的 this-task-classification 均一致，无异常漂移。
4. 其余同 SHARED（D2-088 模板、60 vs 30、job-00 FAIL 无标注、单行截断、驱动缺失、casePath 三版本、响应缺元数据、无 closure、network/process not-applicable）。

### INDEPENDENT EVIDENCE FACTS
- 两侧 build/exec `completed/0`、stderr 空；两侧 stdout digest 完全相同（`0ca9ae423f0a42a3151393e1198a8f3eba68933029bc3138b48e8ead943abf81`）。
- artifact=`/tmp/safe-attck-go/09_discovery/advanced-discovery.json`；env_preview 前 12 项实测顺序=PATH=/usr/local/bin:/usr/bin:/bin, HOME=/root, USER=root, LOGNAME=root, SHELL=/bin/sh, LANG=C, LC_ALL=C, TERM=dumb, TZ=UTC, PWD=/tmp, HOSTNAME=probe-host, PYTHONHASHSEED=0；extension_counts=("",1)/(.go,1)/(.py,1)/(.txt,1)；loopback_addrs=["127.0.0.1/8","::1/128"]；workspace_entries=["alpha.go","beta.txt","delta","gamma.py"]。
- 两侧 preflight/cleanup=PASSED、environmentStatus=clean、contaminated=false、runnerStateAfter=READY、snapshot CC-Eval-Linux-8Lang-1.0.28。
- 源 artifactHash 两 job 相同（`33b5edca…`）；target artifactHash 不同（`0ed0224b…` 占位 vs `11c6ee0b…` 真目标）。

### ATTRIBUTION
- 行为差异：无（digest 相同）。
- job-00 FAIL：装置（占位件）。
- “对称装置”成立性：**装置/未定**（驱动与 input_profile 无法佐证）。
- asciiLower 的 Unicode 折叠、TMPDIR 去尾斜杠：环境，冻结不可达。
- 非连续 netmask / 空 netmask：源—内核前缀长度语义边界，未触发 ⇒ 未定。

### KNOWLEDGE
- 候选 (a)(b)：同前。
- 候选 (e)（本项最重要）：**被观察量包含 cwd/env/接口等非源码常量时，必须冻结“输入面等价”（argv/fixture/cwd/env/被统计集合）并在证据中留下可复核驱动**；现契约 §10.18/§10.19（`…/batch/operational-discipline.md:356,396`）只覆盖 argv 文件与目录条目数。
- 已覆盖：§10.6 归因前置核对、§10.15 档位、GO-CPP 方向规则（均不涉及 cwd/env 对称强形式）。
- 错误自审建议：无（11 项全 null proposed_fix）。

### OPTIMIZATION
- 流程（最高优先）：把对称装置的实现（driver 或 input_profile 的 cwd/env 字段）随证据落盘，否则第三方无法区分“真等价”与“两侧恰好相同”。
- 去噪：job-00 报告补 placeholder 标注；`batch-authorization.json` 清理 D2-088 模板并让 dataSource.confirmation 与实际分类一致（本项与 D2-037 同文件互相矛盾）。
- 评估：network 维度 not-applicable 而实际读取本机接口/回环地址 ⇒ 接口状态变化不会进入比较面。
- 统计：把“装置对称性声明是否有可核原件”作为一项对账检查项。

### UNKNOWNS
- `run_case.py` 是否真的删除两侧树差异、是否以固定顺序注入 14 变量；target.cpp 314 行全文；非连续掩码/空 mask 行为；非 ASCII 文件名扩展名折叠。

---

## 4. D2-040（go-to-cpp / handoff-2026-10-02-d26-gzip-xor-replay-go）

### IDENTITY
- taskId=D2-040；kind=REUSE；direction=go-to-cpp；source=`gzip_xor_replay.go`；declared Sha256=`7EB6F3C85C12BF25D01427AC174E47633F831C446F11B7D803F9F22B9A6A7D97`（一致）。
- casePath=`docs/test/dataset-2/go-to-cpp/handoff-2026-10-02-d26-gzip-xor-replay-go`。
- item JSON：CONVERTED/CLOSED/DONE、pendingAction=null、blockingReasons=[]、codeRevisions=0、selfRepairRounds=0、targetSha256=`00510f1d8524d0206270ebc22fbaa67eb8b7c1b73eb39dfb7655e686ebe71057`。
- usage：requests=2、prompt 8216、completion 96278、reasoning 88135、total 104494、model deepseek-flash、failedAttempts=0（**本批 token 最高**）。
- evaluator id=`eval-20261006-081745-d214c001`；job-00=`eval-20261011-085809-24ae80a4`；job-01=`eval-20261011-090555-6add3f70`。

### FILE INVENTORY（前缀 `S`=`go-to-cpp/handoff-2026-10-02-d26-gzip-xor-replay-go/output/batch/`）
| 路径 | 状态 | 备注 |
|---|---|---|
| S01-frozen/classification-1.json | read | REVIEW_SIDE_EFFECTS |
| S01-frozen/classifier-input.json | read | 单任务输入 |
| S01-frozen/frozen-inputs.md | read | 含 raw_len=22 错误 |
| S02-conversion/observed-source-stderr.txt | **empty(0 B)** | 空 stderr |
| S02-conversion/observed-source-stdout.txt | read | 源基线 stdout |
| S02-conversion/request.system.txt | read | 含完整 gzip hex |
| S02-conversion/target.gen.model.json | read(截断>2000字符, 现役工具无法补读) | 真实响应 |
| S03-self-review/review.system.txt | read | 自审清单 |
| S03-self-review/self-review-1.json | read | NO-REPAIR-IDENTIFIED |
| S03-self-review/self-review-1.model.json | read | metadata-only |
| S04-evaluation/job-00-source-buildability/batch-authorization.json | read | D2-088 残留 |
| S04-evaluation/job-00-source-buildability/comparison_manifest.json | read | go/cpp |
| S04-evaluation/job-00-source-buildability/controller-health-before.json | read | ok |
| S04-evaluation/job-00-source-buildability/input_profile.json | read | timeout 30 |
| S04-evaluation/job-00-source-buildability/job-id.txt | read | eval-…24ae80a4 |
| S04-evaluation/job-00-source-buildability/metadata.json | read | placeholder-precheck |
| S04-evaluation/job-00-source-buildability/runners-before.json | read | 3 runner READY |
| S04-evaluation/job-00-source-buildability/this-task-classification.json | read | 一致 |
| S04-evaluation/job-00-source-buildability/returned-evidence/comparison.json | read(截断>2000字符, 现役工具无法补读) | mismatched(占位) |
| S04-evaluation/job-00-source-buildability/returned-evidence/controller.log | read | 08:58:09→08:59:10 |
| S04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json | read(截断>2000字符, 现役工具无法补读) | FAIL/mismatched |
| S04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.md | read | FAIL/mismatched |
| S04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json | read(截断>2000字符, 现役工具无法补读) | 源基线 314 B |
| S04-evaluation/job-00-source-buildability/returned-evidence/evidence-target.json | read(截断>2000字符, 现役工具无法补读) | 占位 MISSING |
| S04-evaluation/job-01-dual-build/batch-authorization.json | read | 同上 |
| S04-evaluation/job-01-dual-build/comparison_manifest.json | read | go/cpp |
| S04-evaluation/job-01-dual-build/controller-health-before.json | read | ok |
| S04-evaluation/job-01-dual-build/input_profile.json | read | timeout 30 |
| S04-evaluation/job-01-dual-build/job-id.txt | read | eval-…6add3f70 |
| S04-evaluation/job-01-dual-build/metadata.json | read | targetHash=00510f1d… |
| S04-evaluation/job-01-dual-build/runners-before.json | read | 3 runner READY |
| S04-evaluation/job-01-dual-build/this-task-classification.json | read | 一致 |
| S04-evaluation/job-01-dual-build/returned-evidence/comparison.json | read(截断>2000字符, 现役工具无法补读) | matched, diffs=[] |
| S04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json | read | ok |
| S04-evaluation/job-01-dual-build/returned-evidence/controller.log | read | 09:05:55→09:06:57 |
| S04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json | read(截断>2000字符, 现役工具无法补读) | runnable/passed/matched |
| S04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md | read | PASS/MATCHED |
| S04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json | read(截断>2000字符, 现役工具无法补读) | 314 B, c2b0ecd2… |
| S04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json | read(截断>2000字符, 现役工具无法补读) | 314 B, 同 digest |
| Sevaluator_manifest.json | read | 移交清单 |
| Sresult.md | read | 分层结论 |

**共 41 个文件**；另读 `batch/items/D2-040.json` 与 manifest.csv 行 40。

### FREEZE/CLASSIFY
- frozen-inputs.md（68 行）：sourcePath=`…/source/gzip_xor_replay.go`；1413 B / 64 行；Go 1.27（bytes, compress/gzip, crypto/sha256, encoding/{base64,hex,json}, fmt, io, os, path/filepath）；target C++/ISO C++17；sourceOs=targetOs=linux、x64；runner linux-vm-agent-x64；snapshot CC-Eval-Linux-8Lang-1.0.28；model deepseek-flash temp0.2 RAG=off、不设 max_tokens；skills=go-to-cpp、languages/{go,cpp}、seven-language-common-semantics、scenes/file-io；sceneTags=[file-io]；attackTactic=none；taskMode=短单文件(64 行)。
- **冻结核心风险**：`base64`/`compressed_len`/`sha256` 全部取决于 gzip 字节流；Go `compress/flate` 是自研 DEFLATE，**不保证与 zlib 逐字节相同**（同级别块划分/匹配策略不同）⇒ 目标若用 zlib 可能 mismatched。处置：照常提交、不预判目标；目标须**真实完成** gzip/xor/base64/sha256（不得桩化）；**若差异仅源于压缩实现（环境/工具链：zlib vs Go flate）则按环境差异登记、保留平台原 verdict、不自行改判 PASS**；若桩化或语义错（XOR key/base64 表/对 raw 而非 b64 求哈希）则属转换引入。目标自行实现与 Go 一致的 gzip 更佳但不强制。
- **不引入第三方压缩库**（构建命令只有 g++，无 -lz）⇒ 目标须自带实现。
- 期望观察：`raw_len`=**22**（冻结原文，与实测 23 冲突）；compressed_len/base64/sha256 以源侧预检实测为准；`sha256` 对 **base64 文本**求哈希；`recover_ok`=true；顶层 map 键字典序 base64<compressed_len<raw_len<recover_ok<sha256；raw_len/compressed_len 数值、recover_ok 布尔。
- driver：一次性程序+自然退出（源 main L39）；argv=[]、stdin=null、terminate=`timeout=60`；driverRationale 逐步（MkdirAll → gz(raw) → xor(0x5A) → base64.StdEncoding → sha256.Sum256([]byte(b64)) → 回放 gunz(xor(decode(b64),0x5A)) → 写 advanced-transforms.json → Println）；oracle=output、stdoutMode=normalized-text/stderrMode=exact；可冻结性说明“跨实现复现性是目标能力问题，不影响冻结”。
- 未覆盖：gzip 各级别/策略、空输入、解压错误分支、recover_ok=false、文件模式位。
- classification-1.json：version 2.4、cls=REVIEW_SIDE_EFFECTS、reason=local_effects_require_review、ALLOWED、blockingReason=null、executionApproved=true、executable=false、requiresNetworkIsolation=false、requiresSyntheticData=false、classifierSha256=009a6f31…f3a4、inputManifestSha256=`7d075fbfd5bab06bb6fafc1b3c75647d0f50a4d7036a4f98819c2118105153d8`、old_cls/old_reason=null；reviewGroups=[filesystem,process]；files=gzip_xor_replay.go（sha256 一致；filesystem 行 35/41/62；has_network=false、has_file_ops=true、has_process_exec=false）、run_case.py（sha256=`6032e408a6cd37b84ec4ef66693d0ce8384256b61852dcda0f9d9dc3f1747a5f`；filesystem 行 41、process 行 1/27/28）。无 reclassification。

### SOURCE PRECHECK（job-00）
- jobId=`eval-20261011-085809-24ae80a4`；buildCommand=`go build -o program gzip_xor_replay.go`；build completed/0/6727ms；stdout/stderr 空；无 diagnostic。
- execution：completed/0/35ms（job-00）；stdout digest=`c2b0ecd2…`、sizeBytes=314（artifact 行 + 五键 JSON）；stderr 空。
- cleanup：preflight/cleanup=PASSED、contaminated=false、READY。
- target 占位：build completed/0（355ms）、exec completed/0（66ms）、stdout MISSING（23 B）⇒ comparison mismatched。

### REQUESTS/RESPONSES
- `request.system.txt`（28 行）：完整语义契约；规定管线 raw="safe-transform-pipeline" → gzip → XOR 0x5A → StdEncoding base64（带 `=` 填充）→ 对 base64 字节求 SHA-256（小写 hex）→ 回放校验；**给出完整 47 字节 gzip hex 供核对**（`1f8b08000000000000ff2a4e4c4bd52d294acc2b4ecb2fcad52dc82c48cdc9cc4b05040000ffff37cb111617000000`）、说明 header/deflate BTYPE=01/尾部空 stored 块 `00 00 ff ff`/CRC32+ISIZE；**明确“不得直接输出上面这串字节”“不得引入第三方压缩库”“严禁把已知 base64/sha256 字面量硬编码”**；给 base64 表、SHA-256 自实现、JSON 字典序与类型。不含源全文、无脱敏内容。
- `target.gen.model.json`：真实响应（content=target.cpp，含 CRC32 表、BitWriter/BitReader、fixed-Huffman literal 编码器、gzip header 常量、DEFLATE 解码器用于 recover_ok、自实现 base64、自实现 SHA-256、std::filesystem/create_directories/chmod）；单行截断；无 model/finish_reason/usage。
- `self-review-1.model.json`：metadata-only；usage{prompt 6120, completion 42508, reasoning 38520, total 48628}、finishReason=stop、verdict=NO-REPAIR-IDENTIFIED。
- 失败 attempt：无。

### SELF-REVIEW
- `self-review-1.json`：verdict=NO-REPAIR-IDENTIFIED；scope=对 target.gen.cpp（344 行）与源逐段对照 12 项：gz() 是否复现 Go fixed-Huffman gzip 字节流、XOR/base64/SHA-256、回放解码器自洽性、JSON 键序与形态、路径与 stdout/退出码；未运行、未做行为验证。
- 12 项全“未发现问题”；origin 2 项 environment（TMPDIR 写死 `/tmp`；显式 `::chmod` 精确权限），其余 undetermined；proposed_fix 仅第 11 项给出“可选（非冻结契约必需）”的 getenv("TMPDIR") 建议。
- **风险自陈充分**：CRC32 数值仅做算法等价性核对、未两次数值重算；SHA-256 摘要未离线复算（上游取决于 gzip 是否一致）；回放解码器只覆盖 stored+fixed-Huffman literal 子集（长度/距离码空处理、dynamic Huffman 直接 break）；“全-literal 仅在无长重复输入时等价”。
- 无实际修复（codeRevisions=0）。

### JOBS
- **job-00 `eval-20261011-085809-24ae80a4`**：input_profile profileId=D2-040/timeout30/workspace；comparison_manifest source `go build -o program gzip_xor_replay.go`（go/linux）、target `g++ -std=gnu++17 target.cpp -o program`（cpp/linux）、run `python run_case.py`；metadata networkBoundary=“isolated VM; no network egress”，note 明确“observable base64/compressed_len depend on Go compress/flate exact bytes”，sourceHash 7eb6f3c8…、targetHash=placeholder-precheck；controller.log 08:58:09.508944→08:59:10.910013；evidence-source.json（build 6727ms、exec 35ms、baselineReference.artifactHash=`92f75fa86197c2415fb7e93758c8feacfcbb58e67497140db740f3947af865b3`、inputProfileHash=`28cd193fc5deca9cd1971dec5a5ae2f96d9fb23312a5ff4555ec26f9088bbb00`）；evidence-target.json（artifactHash=`32ab84987caed02cec2f91fd5d705ac3e13445f031c1e6349d0d07f17fd2be9c`、MISSING）；comparison.json mismatched 1 major diff（sourceValueSummary 以 base64 值开头）；evaluation_report.json/md：COMPLETED/FINISHED、partial-runnable/failed/mismatched/clean、coverage{1,1,0,1,0,1.0}。cleanup PASSED；无 after；无 closure/report-retry。
- **job-01 `eval-20261011-090555-6add3f70`**：input_profile 同上；comparison_manifest 同上；metadata note 说明目标自实现 fixed-Huffman DEFLATE+CRC32+base64+SHA-256（无第三方压缩库）且可观察量依赖 Go flate 字节；targetHash=00510f1d…；controller.log 09:05:55.264124→09:06:57.871632；evidence-source.json（build completed/0/7136ms、exec 33ms、stdout 314 B digest `c2b0ecd2…`、stderr 空、artifactHash `92f75fa8…` 与 job-00 同）；evidence-target.json（build completed/0/1782ms、exec 41ms、stdout 314 B **同 digest**、artifactHash=`ef546b921b9366aff56424e561b21d6ade9d853d6d27fb511eb794180e21a19e`）；comparison.json matched/diffs=[]/1.0；evaluation_report.json/md runnable/passed/matched/clean、Output=matched、其余 not-applicable；controller-health-after（09:07:29.044178）ok；cleanup PASSED。

### RESULT/DELIVERY
- `result.md`（59 行）：分层表（编译 PASS 无第三方压缩库、matched digest `c2b0ecd2…` 314 B diffs=0）；专门章节说明“本项难点：可观察量依赖 Go compress/flate 的确切字节”，逐段注释 gzip 结构（header(10) / deflate BTYPE=01 fixed Huffman / `00 00 ff ff` sync / CRC32 / ISIZE），并声明目标自实现与 Go 逐字节一致；声明“未硬编码”（请求已明令禁止，自审逐段核对）；双 job 表；§10.6 核对；覆盖缺口 5 条；自审段（344 行、12 项）。
- `evaluator_manifest.json`（71 行）：结构同前；sceneTags[file-io]；jobId=eval-20261011-090555-6add3f70；isolationLaunchArgs 含 `networkBoundary=isolated VM; no network`；attackClassification rationale=本地变换管线。
- **claims vs evidence**：jobId/digest/314 B/compressed_len=47/base64/sha256 与证据一致；源码/目标/驱动缺失使“未硬编码”只能靠截断的 content 前缀与自审陈述支撑（不可完全复核）。

### ANOMALIES（在 SHARED 之外）
1. **frozen-inputs.md 期望 `raw_len`=22 与实测 23 冲突**（源字符串 "safe-transform-pipeline" 为 23 字节）；result.md、item JSON、request.system.txt 均用 23 ⇒ 冻结文档的单点笔误。
2. **request.system.txt 给出完整 47 字节期望 gzip hex**：虽同文禁止直接输出并说明“供核对”，但这等于把期望字节流交给模型，与“不得硬编码”的核验目标存在张力；自审只能静态确认字面量清单（已确认无 base64/sha256/gzip hex 字面量）。
3. **等价性不可外推**：目标“全 literal”fixed-Huffman 实现只在输入无 ≥3 字节重复子串时与 Go flate 一致；含长重复输入会分歧 ⇒ 平台 `matched` 的语义范围极窄，result.md 已明确“结论不外推”，但 item JSON 的 `verdicts.comparison` 仅写 matched。
4. CRC32 与 SHA-256 数值**未被任何独立来源复算**（自审明言），仅由两侧 digest 相同反推。
5. 其余同 SHARED（D2-088 模板、60 vs 30、job-00 FAIL 无标注、单行截断、驱动缺失、casePath 三版本、响应缺元数据、无 closure、network not-applicable）。

### INDEPENDENT EVIDENCE FACTS
- 两侧 build/exec `completed/0`、stderr 空、timedOut=false；两侧 stdout sizeBytes=**314** 且 digest 完全相同（`c2b0ecd2042b87fa7b0d143695808e74de0722c0805a49749eb7439a67d3acc8`）。
- artifact=`/tmp/safe-attck-go/07_defense_evasion/advanced-transforms.json`；报告五键：base64=`RdFSWlpaWlpapXAUFhGPd3MQlnEUkXWQj3eSdhKXk5YRX15aWqWlbZFLTE1aWlo=`、compressed_len=47、raw_len=23、recover_ok=true、sha256=`be5295b11541c552ca627dfac9dcaabbbbcb5969a8ab901a8455c07ea17ac5b8`。
- 两侧 preflight/cleanup=PASSED、environmentStatus=clean、contaminated=false、READY、snapshot CC-Eval-Linux-8Lang-1.0.28、runner=linux-vm-agent-x64。
- 源 artifactHash 两 job 相同（`92f75fa8…`）；target artifactHash 不同（`32ab8498…` 占位 vs `ef546b92…` 真目标）。

### ATTRIBUTION
- 行为差异：无（digest 相同）。
- job-00 FAIL：装置（占位件）。
- TMPDIR 硬编码 `/tmp`、`::chmod` 权限：环境。
- 全-literal 与 Go flate 的等价边界：**技术事实**（Go flate 对该输入选择 literal；目标实现复现该选择），非转换引入缺陷；但属**源实现/实现选择**层面的范围限制。
- 动态 Huffman、长重复输入：未定（未触发）。

### KNOWLEDGE
- 候选 (c)（本项核心）：**当目标语言无 Go `compress/flate` 等价物且禁止第三方库时，压缩字节级一致性只在特定输入类成立；必须显式冻结并记录“不可外推边界”，平台 matched 不得当作普遍等价。** `grep skills/**` 无 flate/deflate/gzip 相关规则（仅各语言页泛化的“字节读写/Base64/压缩”触发条件）⇒ 当前契约未覆盖。
- 候选 (f)：**请求材料不应给出期望输出字节/摘要**（若必须给，应移到冻结文档并由自审显式核字面量清单）。
- 候选 (d)：需自实现 SHA-256/base64/DEFLATE 时禁用硬编码期望值——现由 `AGENTS.md` §6（证据只从真实回传、不伪造）与请求文本部分覆盖，但 skills/ 无具体条目。
- 已覆盖：§10.6 归因、§10.15 档位、GO-CPP 方向规则。
- 错误自审建议：无（12 项 proposed_fix 全 null，唯一条为“可选建议”且非强制）。

### OPTIMIZATION
- 流程：期望字节流若必须在契约中出现，应放在 frozen-inputs（不在请求中）并加自审“字面量清单”硬性核对项；否则“未硬编码”只能靠内容不可得的前缀判断。
- 评估：压缩/哈希类用例应把“含长重复子串输入”列为必测形态，否则 matched 只能证明极窄路径；建议在 item JSON 单列 `nonExtrapolation` 字段（本项已在 `evaluation.nonExtrapolation` 写过，是良好先例）。
- 统计：本项 reasoning 88135 vs completion 8193，token 效率异常，建议在优化提案中单列“推理 token 占比”。
- 去噪：job-00 报告补 placeholder 标注。

### UNKNOWNS
- target.cpp 344 行全文；CRC32/SHA-256 数值是否真由算法算出（仅由 digest 相同反推）；动态 Huffman 与长重复输入的实测行为；驱动后处理的一致性。

---

## 5. D2-041（go-to-cpp / handoff-2026-10-02-d26-token-priv-probe-go）

### IDENTITY
- taskId=D2-041；kind=REUSE；direction=go-to-cpp；source=`token_priv_probe.go`；declared Sha256=`EABD827068C6675EDA5F7431FB2D49838E3693D40CE7A0BCC2EA25F310B18E6E`（一致）。
- casePath=`docs/test/dataset-2/go-to-cpp/handoff-2026-10-02-d26-token-priv-probe-go`。
- item JSON：CONVERTED/CLOSED/DONE、pendingAction=null、blockingReasons=[]、codeRevisions=0、selfRepairRounds=0、targetSha256=`cdeae6ce169ec4e24cd2ba5b2b3ddcf90d6d2f9b430fbc620132ae23450778c9`；classifier 字段额外含 `requiresSyntheticData: true`。
- usage：requests=2、prompt 6916、completion 22787、reasoning 18900、total 29703、model deepseek-flash、failedAttempts=0。
- evaluator id=`eval-20261006-083117-ac76f01d`；job-00=`eval-20261011-090837-e2b647a2`；job-01=`eval-20261011-091207-682b2dd2`。

### FILE INVENTORY（前缀 `T`=`go-to-cpp/handoff-2026-10-02-d26-token-priv-probe-go/output/batch/`）
| 路径 | 状态 | 备注 |
|---|---|---|
| T01-frozen/classification-1.json | read | cls=REVIEW_SENSITIVE |
| T01-frozen/classifier-input.json | read | 单任务输入 |
| T01-frozen/frozen-inputs.md | read | GOOS 短路冻结 |
| T02-conversion/observed-source-stderr.txt | **empty(0 B)** | 空 stderr |
| T02-conversion/observed-source-stdout.txt | read | 源基线 stdout（含 timestamp） |
| T02-conversion/request.system.txt | read | 转换请求 system |
| T02-conversion/target.gen.model.json | read(截断>2000字符, 现役工具无法补读) | 真实响应（#ifndef _WIN32） |
| T03-self-review/review.system.txt | read | 自审清单 |
| T03-self-review/self-review-1.json | read | NO-REPAIR-IDENTIFIED |
| T03-self-review/self-review-1.model.json | read | metadata-only |
| T04-evaluation/job-00-source-buildability/batch-authorization.json | read | D2-088 残留 |
| T04-evaluation/job-00-source-buildability/comparison_manifest.json | read | go/cpp |
| T04-evaluation/job-00-source-buildability/controller-health-before.json | read | ok |
| T04-evaluation/job-00-source-buildability/input_profile.json | read | timeout 30 |
| T04-evaluation/job-00-source-buildability/job-id.txt | read | eval-…e2b647a2 |
| T04-evaluation/job-00-source-buildability/metadata.json | read | placeholder-precheck |
| T04-evaluation/job-00-source-buildability/runners-before.json | read | 3 runner READY |
| T04-evaluation/job-00-source-buildability/this-task-classification.json | read | 一致 |
| T04-evaluation/job-00-source-buildability/returned-evidence/comparison.json | read(截断>2000字符, 现役工具无法补读) | mismatched(占位) |
| T04-evaluation/job-00-source-buildability/returned-evidence/controller.log | read | 09:08:37→09:09:43 |
| T04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json | read(截断>2000字符, 现役工具无法补读) | FAIL/mismatched |
| T04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.md | read | FAIL/mismatched |
| T04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json | read(截断>2000字符, 现役工具无法补读) | 源基线 timestamp 09:08:48Z |
| T04-evaluation/job-00-source-buildability/returned-evidence/evidence-target.json | read(截断>2000字符, 现役工具无法补读) | 占位 MISSING |
| T04-evaluation/job-01-dual-build/batch-authorization.json | read | 同上 |
| T04-evaluation/job-01-dual-build/comparison_manifest.json | read | go/cpp |
| T04-evaluation/job-01-dual-build/controller-health-before.json | read | ok |
| T04-evaluation/job-01-dual-build/input_profile.json | read | timeout 30 |
| T04-evaluation/job-01-dual-build/job-id.txt | read | eval-…682b2dd2 |
| T04-evaluation/job-01-dual-build/metadata.json | read | targetHash=cdeae6ce… |
| T04-evaluation/job-01-dual-build/runners-before.json | read | 3 runner READY |
| T04-evaluation/job-01-dual-build/this-task-classification.json | read | 一致 |
| T04-evaluation/job-01-dual-build/returned-evidence/comparison.json | read(截断>2000字符, 现役工具无法补读) | semantic_pass, 1 minor diff |
| T04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json | read | ok |
| T04-evaluation/job-01-dual-build/returned-evidence/controller.log | read | 09:12:07→09:13:18 |
| T04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json | read(截断>2000字符, 现役工具无法补读) | runnable/semantic_pass |
| T04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md | read | PASS/SEMANTIC_PASS |
| T04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json | read(截断>2000字符, 现役工具无法补读) | digest 3a8379a2… |
| T04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json | read(截断>2000字符, 现役工具无法补读) | digest 944f6f31…（仅 timestamp 不同） |
| Tevaluator_manifest.json | read | 移交清单 |
| Tresult.md | read | 分层结论 |

**共 41 个文件**；另读 `batch/items/D2-041.json` 与 manifest.csv 行 41。

### FREEZE/CLASSIFY
- frozen-inputs.md（75 行）：sourcePath=`…/source/token_priv_probe.go`；1642 B / 54 行；Go 1.27（encoding/json, fmt, os, os/exec, path/filepath, runtime, strings, time）；target C++/ISO C++17；sourceOs=targetOs=linux、x64；runner linux-vm-agent-x64；snapshot CC-Eval-Linux-8Lang-1.0.28；model deepseek-flash temp0.2 RAG=off、不设 max_tokens；skills=go-to-cpp、languages/{go,cpp}、seven-language-common-semantics、scenes/file-io、scenes/process-execution；sceneTags=process-execution（exec.Command 文本存在但 linux 下短路）+ file-io；attackTactic=none（linux 上不执行任何命令、不做提权尝试，只写本地报告）。
- **冻结核心：linux 下 `runtime.GOOS != "windows"` 短路**。两 probe 首行均为 `if runtime.GOOS != "windows" { return … }`：`probeAdminLike()` ⇒ `{Method:"admin-check", OK:false, Detail:"non-windows or unsupported"}`（**不执行 `cmd /C net session`**）；`probePrivilegesText()` ⇒ `{Method:"whoami-priv", OK:false, Detail:"non-windows"}`（**不执行 `cmd /C whoami /priv`**）⇒ linux runner 上**无进程执行、无提权行为**；os/exec 仅存在于文本。
- 期望观察：顶层 map 键字典序 `note`<`probes`<`timestamp`；probes 元素是 struct `privilegeProbe{Method,OK,Detail}` ⇒ 字段序 `method`→`ok`→`detail`（**不是**字典序）；ok 布尔、其余字符串；**timestamp=time.Now().Format(time.RFC3339) 是不可复现量，但被 `noise-tolerant-v1` 的 `text_tokens` 显式含 `timestamps` 覆盖 ⇒ 不构成不可冻结**；两空格缩进、末尾不加换行。
- driver：一次性程序+自然退出（源 main L36）；argv=[]、stdin=null、terminate=`timeout=60`；driverRationale 逐步（MkdirAll → 组装 map{timestamp,note,probes:[probeAdminLike(),probePrivilegesText()]} → MarshalIndent → 写 advanced-privilege-report.json → Println）；oracle=output、stdoutMode=normalized-text/stderrMode=exact；可冻结性说明 note/probes 确定、timestamp 已被消噪覆盖。
- 未覆盖：**windows 分支完全未覆盖**（net session / whoami /priv / SeDebugPrivilege / _popen；本批无 windows runner 参与本项）、exec 失败分支、非 UTC 时区 RFC3339 偏移分支、文件模式位。
- 未冻结/待确认：**目标若误实现在 linux 上也执行 cmd（照搬 windows 分支而未保留 GOOS 判据）将产生转换引入缺陷——已显式标注**；精确工具链版本以 runner 实测为准。
- classification-1.json：version 2.4、cls=**REVIEW_SENSITIVE**、reason=`sensitive_or_dynamic_operations`、ALLOWED、blockingReason=null、executionApproved=true、executable=false、requiresNetworkIsolation=false、**requiresSyntheticData=true**、classifierSha256=009a6f31…f3a4、inputManifestSha256=`ff78f906e717c55c1150d3821b54e94767878cd27abdbb4f9b8f99ca1ced2107`、old_cls/old_reason=null；reviewGroups=[dynamic_code,filesystem,process]；files 顺序为 run_case.py 在前（sha256=`601db0bcfb190e8a121aa73dbedad5c716b62d2d3e76bcb2c151299c1918798f`；filesystem 行 41、process 行 1/27/28）、token_priv_probe.go 在后（sha256 一致；filesystem 行 42/52、process 行 24/32、**dynamic_code 行 7**；has_network=false、has_file_ops=true、has_process_exec=true）。无 reclassification。

### SOURCE PRECHECK（job-00）
- jobId=`eval-20261011-090837-e2b647a2`；buildCommand=`go build -o program token_priv_probe.go`；build completed/0/5757ms；stdout/stderr 空；无 diagnostic。
- execution：completed/0/35ms（job-00）；stdout digest=`97565872…`、内容=artifact 行 + `--- report ---` + 三键 JSON（note/probes[2]/timestamp="2026-10-11T09:08:48Z"）；stderr 空。
- cleanup：preflight/cleanup=PASSED、contaminated=false、READY。
- target 占位：build completed/0（683ms）、exec completed/0（182ms）、stdout MISSING（23 B）⇒ comparison mismatched。

### REQUESTS/RESPONSES
- `request.system.txt`（29 行）：完整语义契约；**开篇即“本项关键：必须保留 GOOS 判据，linux 下不得执行任何命令”**，给出 `#ifdef _WIN32`/`#if defined(_WIN32)` 方案与“linux 构建下不执行任何子进程、只有 windows 构建才走 exec.Command 分支”；逐条给两 probe 的 non-windows 返回值、timestamp RFC3339（**偏移为 0 时输出 `Z`，不是 +00:00/+0000**）、note 字面量、JSON 形态（顶层 map 字典序、probes struct 字段序、ok 布尔、缩进）、Go 默认 escapeHTML、路径/0644/MkdirAll 0755、退出码 0/stderr 空。不含源全文、无脱敏内容。
- `target.gen.model.json`：真实响应（content=target.cpp；注释明确 linux 可观察行为“GOOS guard short-circuits both probes -> NO subprocess is ever spawned”；两个 probe 用 `#ifndef _WIN32` 直接返回，#else 才含 `std::system("cmd /C net session >nul 2>&1")` 与 `_popen("cmd /C whoami /priv …")`；含 rfc3339Now、jsonString 转义、tempDir/joinPath/writeFile）；单行截断；无 model/finish_reason/usage。
- `self-review-1.model.json`：metadata-only；usage{prompt 4615, completion 13039, reasoning 11687, total 17654}、finishReason=stop、verdict=NO-REPAIR-IDENTIFIED。
- 失败 attempt：无。

### SELF-REVIEW
- `self-review-1.json`：verdict=NO-REPAIR-IDENTIFIED；scope=静态对照 token_priv_probe.go 与 target.gen.cpp 的 **linux 可观察行为**，覆盖清单 1–9；共 9 项。
- 9 项全“未发现问题”、proposed_fix 全 null；**第 1 项即核 linux 无子进程执行路径**（`#ifndef _WIN32` 下 system/popen 编译掉，risk=“无：linux 下无子进程执行路径”）；第 3/4/5 项核 struct 字段序、顶层键序、JSON 形态；第 6 项 timestamp（依赖 localtime_r/timegm，风险低，“现代时区偏移为整分钟”）；第 7 项转义；第 8 项路径/stdout/退出码；第 9 项无新增输出/副作用。
- **未在自审内登记“windows 分支不可评估”**（该缺口写在 result.md 与 item JSON coverageGaps）。
- 无修复（codeRevisions=0）。

### JOBS
- **job-00 `eval-20261011-090837-e2b647a2`**：input_profile profileId=D2-041/timeout30/workspace；comparison_manifest source `go build -o program token_priv_probe.go`（go/linux）、target `g++ -std=gnu++17 target.cpp -o program`（cpp/linux）、run `python run_case.py`；metadata networkBoundary=“isolated VM; no network egress (classifier network_mode=none-detected)”，safetyClassification 含 `cls=REVIEW_SENSITIVE requiresSyntheticData=true`、“no command executed on linux”，sourceHash eabd8270…、targetHash=placeholder-precheck；controller.log 09:08:37.959795→09:09:43.550749；evidence-source.json（build 5757ms、exec 35ms、baselineReference.artifactHash=`36402d7727a79a723e12678ba2b806d25e96a764296ff393a7dd343c029d08bc`、inputProfileHash=`3ab4a609026fb7e6750595c56e047404ca43c1181619b181ae387b473a4869cc`）；evidence-target.json（artifactHash=`d699ce834ddf15f058f46ae8c686ae4b13752e1e48c748d876813377e9d92d67`、MISSING）；comparison.json mismatched 1 major diff；evaluation_report.json/md：COMPLETED/FINISHED、partial-runnable/failed/mismatched/clean、coverage{1,1,0,1,0,1.0}。cleanup PASSED；无 after；无 closure/report-retry。
- **job-01 `eval-20261011-091207-682b2dd2`**：input_profile 同上；comparison_manifest 同上；metadata note 说明源 linux 短路、目标用 `#ifndef _WIN32` 保留、windows-only 路径被编译掉，“timestamp is covered by the platform noise token 'timestamps'”；targetHash=cdeae6ce…；controller.log 09:12:07.677128→09:13:18.030628；evidence-source.json（build completed/0/5824ms、exec 33ms、stdout digest `3a8379a28b23b8…251e`、timestamp=**2026-10-11T09:12:17Z**、stderr 空、artifactHash `36402d77…` 与 job-00 同）；evidence-target.json（build completed/0/994ms、exec 252ms、stdout digest `944f6f31423ef…ecee`、timestamp=**2026-10-11T09:12:44Z**、stderr 空、artifactHash=`3ce77df90a89eeab96a30bbbdc7bf41a60146c8dfdbf2a3046f883016e5d5a89`）；comparison.json behaviorVerdict=`semantic_pass`、verdictReason=“Applicable dimensions match with only explicitly configured minor differences.”、dimensions.output{status=`semantic-match`, applicable true, observed true, diffs=[{path stream.normalizedText, kind changed, **criticality minor**, rule=`noise-tolerant-v1:text-tokens:temporary-paths,timestamps,ephemeral-ports`, evidenceRefs[stream/normalizedText]}]}、其余 not-applicable；evaluation_report.json/md：runVerdict `runnable`、codeVerdict `semantic_pass`、behaviorVerdict `semantic_pass`、environmentStatus clean、coverage{applicable 1, observed 1, matched **0**, mismatched **0**, inconclusive 0, sufficient 1, coverageRatio 1.0}、failure=null；Evidence Matrix Output=`semantic-match`、diffs=1；controller-health-after（09:13:35.628004）ok；cleanup PASSED。

### RESULT/DELIVERY
- `result.md`（64 行）：分层表（编译 PASS；行为一致性=**`semantic_pass`（非 matched，§10.15 独立档位）**；唯一 minor 差异=timestamp 被 timestamps 消噪 token 覆盖；环境 clean；安全 ALLOWED REVIEW_SENSITIVE/无网络/linux 无进程执行）；引用块强调“平台判 semantic_pass，按 §10.15 不得写成 matched”；专章“linux 下必须保留 GOOS 判据、不得执行命令”（`#ifndef _WIN32` 使 system/_popen 仅在 Windows 分支）；唯一差异与归因（§10.14）逐字段对照表（note/probes[0]/probes[1] 一致、timestamp 不同；digest 不同只源于该时间戳）；双 job 表；§10.6 核对；覆盖缺口 4 条（Windows 分支完全未覆盖、exec 失败、非 UTC 偏移、文件模式位）；自审段（259 行、9 项）。
- `evaluator_manifest.json`（72 行）：结构同前；sceneTags[process-execution,file-io]；jobId=eval-20261011-091207-682b2dd2；prerequisites 第 3 条“behaviorVerdict=semantic_pass，唯一 minor diff 为被消噪覆盖的 timestamp”；isolationLaunchArgs 含 `networkBoundary=isolated VM; no network; no command executed on linux`；attackClassification rationale=只在 windows 试图执行 net session/whoami，linux 因 GOOS 短路不执行任何命令、不做提权。
- **claims vs evidence**：semantic_pass/唯一 minor diff/timestamp 值/逐字段一致性与证据完全对应，且**未把 semantic_pass 误写为 matched**（合规）；源码/目标/驱动缺失。

### ANOMALIES（在 SHARED 之外）
1. **平台 `codeVerdict` 与 `behaviorVerdict` 均为 `semantic_pass`**，且 coverage `matchedDimensions=0`/`mismatchedDimensions=0`/`inconclusiveDimensions=0`、仅 `diffs=1 criticality=minor` ⇒ 与 §10.15 描述完全一致，本项处理正确（作为“档位纪律”正例）。
2. **Windows 分支完全未评估**：`net session`、`whoami /priv`、`SeDebugPrivilege` 检测、`_popen` 均不在本批观察范围（无 windows runner 参与本项），而分类为 REVIEW_SENSITIVE + requiresSyntheticData=true；这是 4 条覆盖缺口中最重要的一条，行为结论不可外推到 Windows。
3. 同一份 `batch-authorization.json` 的 dataSource 文本“无网络、无凭证”对本项成立，但对 D2-037 不成立（同批同文件矛盾）。
4. 其余同 SHARED（D2-088 模板、60 vs 30、job-00 FAIL 无标注、单行截断、驱动缺失、casePath 三版本、响应缺元数据、无 closure、network/process not-applicable）。

### INDEPENDENT EVIDENCE FACTS
- 两侧 build/exec `completed/0`、stderr 空、timedOut=false；artifact=`/tmp/safe-attck-go/06_privilege_escalation/advanced-privilege-report.json`。
- 两侧 note=`no escalation attempt`、probes[0]=`admin-check`/false/`non-windows or unsupported`、probes[1]=`whoami-priv`/false/`non-windows` **逐字节相同**；唯一差异 timestamp（源 2026-10-11T09:12:17Z vs 目标 2026-10-11T09:12:44Z，相隔 27 s）。
- 两侧 stdout digest **不同**（`3a8379a28b23b8b6773ec09a0b85ffb96db33f24ca11446bd5c7e61b14c2251e` vs `944f6f31423ef0a217890f74aa37e223fe86ad2d4e5ff09e7e924033f27fcece`）；平台判 `semantic_pass`（非 matched），diffs 1 条 minor。
- 两侧 preflight/cleanup=PASSED、environmentStatus=clean、contaminated=false、READY、snapshot CC-Eval-Linux-8Lang-1.0.28、runner=linux-vm-agent-x64、runnerCount=3/blocked=0。
- 源 artifactHash 两 job 相同（`36402d77…`）；target artifactHash 不同（`d699ce83…` 占位 vs `3ce77df9…` 真目标）。

### ATTRIBUTION
- 唯一差异（timestamp）：**环境/装置**，且落在显式消噪 token（`timestamps`）覆盖内；**非转换引入**。
- job-00 FAIL：装置（占位件）。
- Windows 分支、exec 失败分支、非 UTC 偏移、文件模式位：**未定/未触发**（冻结范围限制）。
- linux 下无子进程执行：由源码语义（GOOS 短路）与目标 `#ifndef _WIN32` 决定，属**源已有行为 + 目标保留**，非差异。

### KNOWLEDGE
- 候选 (b) 最强实例：**Go `runtime.GOOS` 编译期 OS 判据必须映射为 `#ifdef _WIN32`（或等价编译期判定），且在源会短路的平台上不得落地子进程/提权动作。** `grep skills/**` 仅命中 `go.md:202`“冻结 Go 工具链、GOOS 与环境”的一般说明，**无映射规则** ⇒ 当前契约未覆盖，建议写入 go-to-cpp 方向规则与 go.md。
- 候选 (g)：**输出含时间戳时，冻结阶段须核对消噪 token 是否覆盖并写清档位语义（semantic_pass ≠ matched）。** 现契约已覆盖：§10.15（`…/batch/operational-discipline.md:245–265`，含 matchedDimensions=0 的判读与“必须原样写”）、§10.14（同文件 284/306）、`references/adapter/controller/comparison-policy-adapter.md:99–108`、`references/framework/evaluation-readiness-contract.md:97`。
- 已覆盖：§10.6 归因前置核对；AGENTS.md §5（编译/行为/安全分层，semantic_pass 不等于 build PASS）。
- 错误自审建议：**无**（9 项 proposed_fix 全 null，无 WRONG 建议）。

### OPTIMIZATION
- 评估：对 `requiresSyntheticData=true` 或含 process/dynamic_code 线索的项，只有 linux runner 会**系统性漏掉 windows 分支**；建议在收尾时强制记录“平台/OS 未覆盖”并禁止把该行为结论计入跨平台功能分母。
- 去噪：`batch-authorization.json` 的“D2-088”模板语句在 5 项 10 个文件中全部出现，应一次性清理并让 dataSource.confirmation 随实际分类生成。
- 统计：本项应作为 §10.15 的规范正例写入对账（matchedDimensions=0 但 behaviorVerdict=semantic_pass，只能读 behaviorVerdict）。
- 流程：驱动 `run_case.py` 应随证据落盘；“两侧同后处理”是 oracle 强度的关键前提，目前不可复核。

### UNKNOWNS
- target.cpp 259 行全文；windows 分支语义是否真的保留（仅靠 `#ifndef _WIN32` 前缀片段与自审陈述）；linux 上是否存在隐藏子进程路径（无 strace 类运行时证据）；非 UTC 时区偏移格式；`_popen` 的 `CombinedOutput` 等价实现细节。

---

## 6. 跨 5 项汇总结论（供上层归并）

1. **状态一致性**：5 项全部 `CONVERTED`/`CLOSED`/`DONE`、`blockingReasons=[]`、pendingAction=null、codeRevisions=0、selfRepairRounds=0、failedAttempts=0、无 reclassification。平台行为 verdict：D2-037/038/039/040 = `matched`；D2-041 = `semantic_pass`（§10.15 独立档位，未误写 matched）。
2. **独立证据支持**：5 项两侧 build/exec 均 `completed/0`、stderr 空、timedOut=false；037–040 两侧 stdout digest 逐字节相同、diffs=0、coverageRatio 1.0；041 仅 timestamp 为 `minor` diff。行为结论**仅**成立于各自冻结的单一正常路径；D2-039（对称装置）与 D2-040（全-literal 等价）最明确地自陈不可外推。
3. **交付完整性**：每项 40/41 个文件齐备，result.md 与 evaluator_manifest.json 均存在且与证据一致；**但 `source/`、`target.cpp`、`run_case.py` 全部缺失**，`hasSource/hasTranslatedCode=true` 与 `evaluator_manifest` 的 planned 路径指向 Windows 主机（`C:\Users\Administrator.DESKTOP-LRHSLVD\Desktop\code-convert-skill\...`）。
4. **系统性缺陷（本批最值得修）**：
   - `batch-authorization.json`（10 份）的 “该项 **D2-088** 无网络、无凭证” 模板残留，且与 D2-037 的 REVIEW_NETWORK/loopback 分类自相矛盾；
   - 冻结 driver `timeout=60 s` vs 平台 `input_profile.timeoutSeconds=30`（5 项 10 个 profile）；
   - job-00 的 FAIL/MISMATCHED 报告（json+md，5 项）无“target 为占位件”标注；
   - 全部 `evidence-*.json`/`comparison.json`/`evaluation_report.json`/`controller-health*.json` 与 `target.gen.model.json` 为单行 >2000 字符，现役工具无法补读尾部；
   - `casePath` 三版本不一致（manifest.csv / item JSON / evaluator_manifest）；
   - 转换响应缺 model / finish_reason / usage（仅自审侧有元数据）；
   - `filesystem`/`network`/`processes` 维度声明 not-applicable，而真实副作用（文件写入、回环收发、子进程有无）无独立观察。
5. **归因**：无“转换引入”已证项；job-00 FAIL=装置；D2-041 唯一差异=环境（时间戳，消噪覆盖）；其余仅潜在且冻结范围不可达（源侧范围限制）。
6. **知识候选（当前 `skills/**` grep 无命中，尚非契约）**：(a) Go `json.Marshal` 键序 map 字典序 vs struct 字段定义序；(b) `runtime.GOOS` 短路须映射为编译期判据；(c) `compress/flate` 字节级差异与不可外推边界；(e) 装置对称性强形式（cwd/env/被统计集合）；(f) 请求材料不应给出期望输出字节/摘要。**已覆盖**：GO-CPP-07、§10.14/§10.15/§10.18/§10.19、comparison-policy-adapter §5、evaluation-readiness-contract、AGENTS.md §5/§6。**无 WRONG 自审建议**：5 项共 50 项自审条目，proposed_fix 仅 D2-040 第 11 项给出“可选非必需”TMPDIR 建议，其余全 null。

（报告结束；未写其他文件，未运行任何程序，未访问 Controller 目录，未读取任何密钥。）