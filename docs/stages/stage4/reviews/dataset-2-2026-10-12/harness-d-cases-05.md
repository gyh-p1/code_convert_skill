# Harness D — 逐项审阅记录 05（python-to-ruby：D2-269 … D2-274）

> 6 例共 **132 件**（269/270 各 36 件含转换与自审；271–274 各 15 件仅源预检），由本会话派出的只读子会话逐件读取，本会话与 batch 层交叉核对。
> 口径同前：`manifest` 的 NEW 项 `JobId=""`/`Evidence="UNVERIFIED (not built, not run)"` 属**设计**；真问题是 **`Lines` 6/6 不一致**。

| taskId | 源文件 | manifest Lines | frozen/result | 件数 | 分类 | 去向 | 判定 |
|---|---|---|---|---|---|---|---|
| D2-269 | 10_28.py | 56 | **66** | 36 | REVIEW_NETWORK（loopback） | **CONVERTED** | **matched** |
| D2-270 | analyze_tactics.py | 114 | **122** | 36 | REVIEW_SIDE_EFFECTS | **CONVERTED** | **matched** |
| D2-271 | getTGT.py | 104 | **120** | 15 | LOW_SIGNAL（**signals 全空**） | SOURCE_DEPENDENCY_GAP | 0 模型调用 |
| D2-272 | colorsys.py | 144 | **166** | 15 | REVIEW_SIDE_EFFECTS（process[3]） | PREPARATION_GAP | 0 模型调用 |
| D2-273 | smbserver.py | 119 | **138** | 15 | REVIEW_NETWORK（wildcard） | SOURCE_DEPENDENCY_GAP | 0 模型调用 |
| D2-274 | mssqlclient.py | 144 | **167** | 15 | REVIEW_NETWORK（unresolved） | SOURCE_DEPENDENCY_GAP | 0 模型调用 |

## D2-269 — 10_28.py（**CONVERTED / matched**）
- **冻结**（34 行）：sha256 `CF40C8…3AC2`、**66 行**；loopback `127.0.0.1:5389`；`casePath` 写 `docs/test/dataset-2/...`（不存在）。
- **分类** `classification-1.json`（82 行）：`REVIEW_NETWORK`、`ALLOWED`/null、2.4、`009a6f31…f3a4`、`requiresNetworkIsolation=false`；reviewGroups [network,process]；signals network[1,14,16,21]、process[2,7,47,64]；`network_mode=loopback`、target `127.0.0.1` L62 scope=loopback；`inputManifestSha256=58b80434…24d7`；**首轮 ALLOWED，无重分类**。
- `02-conversion`（3 件）：`request.system.txt`（9 行，义务含“loopback 地址不得改、stdout/退出码逐字节一致、保留 `ReverseShell` 公开方法”）、`request.user.md`（33 行，规则 L1-PY-01/04、L1-RB-01/03/04/05、PY-RB-01/03；**`@SOURCE@` 未替换**）、`target.gen.model.json`（25 行）：`deepseek-flash`、http 200、**`finish_reason=stop`**、usage `{prompt 1644, completion 5665, reasoning 5160, total 7309}`、attempts 1、**`truncated=false`**；产物 `target.gen.rb` sha256 `45bb2514…c77e9`、**72 行**。
- `03-self-review`（4 件）：`self-review-1.json`（5 行）verdict **`NO-REPAIR-IDENTIFIED`**、items **[]**；`reviewedScope` 明示“仅静态比对，未运行”，未覆盖连接成功后的 redirect/execute_shell；`self-review-1.model.json`：finish=stop、`truncated=false`、usage `{1706,7252,7124,8958}`、parsed items 0。
- **job-00** `eval-20261012-052138-e7160efa`：build-and-run；`py_compile 10_28.py`/`python 10_28.py`；build `completed/0`(66ms，两流 0 B)；execution `completed/**1**`(34ms)，**stdout 37 B** = `Connection to 127.0.0.1:5389 refused\n`、digest `sha256:8296cc0ca8d913d66157a565af8eac0cee9c80b41929e4977dafa04aa38cd8f2`、stderr 0 B；报告件正常；log `05:21:38.777851Z → 05:22:08.448114Z`。
- **job-01（双侧）** `eval-20261012-052412-b91e8f7c`：`comparison_manifest.json` source python / target `ruby -c target.rb`+`ruby target.rb`；两侧 build `completed/0`（源 65ms / 目标 212ms，目标 build stdout `Syntax OK\n` 10 B）、两侧 execution `completed/**1**`（源 36ms / 目标 225ms）；**目标 stdout 37 B、digest 与源相同**；`comparison.json` **`behaviorVerdict=matched`、`diffs=[]`**（output matched，其余四维 not-applicable）；`evaluation_report.md/.json`：**PASS / MATCHED / CLEAN**、`runVerdict=runnable`、`codeVerdict=passed`、coverage 1/1；`closure`：`complete/cleanupConfirmed=true`、两侧 attempts 1、`issues=[]`；log `05:24:12.354870Z → 05:25:16.912822Z`。
- `result.md`（40 行）：**DONE / matched**；交付“根级 `target.rb` 72 行 sha256 `45bb2514…c77e9`”；`evaluator_manifest.json`（47 行）：`sceneTags=[network-io]`、`files[0].relativePath=target.rb`、`hasReplayArtifact=true`、`replayArtifactPath=04-evaluation/job-01-dual-build/capsule.zip`、`x_adapter` 三 job 串联、`syntaxVerdict=PASS`、`behaviorVerdict=matched`。
- **实体缺失**：`**/*.rb` **0 命中**、`**/capsule*` 0 命中 ⇒ 声明的 `target.rb` 与 `capsule.zip` **无实体**（“已删实现”与“声明-文件不一致”分列）。
- **覆盖边界**：仅 `argv=[]` 的 connect-refused 路径；连接成功后的 redirect/execute_shell 未覆盖（自审 `reviewedScope` 明列）。

## D2-270 — analyze_tactics.py（**CONVERTED / matched**）
- **冻结**（33 行）：sha256 `0EF3A4…D047`、**122 行**；纯标准库 json/os/glob/re、**无 `__main__`**；L6 chdir、L33 glob；argv=[] 无数据文件 ⇒ 确定性“共找到 0 个文件”。
- **分类**（65 行）：`REVIEW_SIDE_EFFECTS`、`ALLOWED`、signals filesystem[39]、`inputManifestSha256=3b3cc74d…160e`；首轮 ALLOWED。
- `02-conversion`：`request.user.md`（32 行，规则 L1-PY-01/02/04、L1-RB-01/02/03/04、PY-RB-01/03/06）；`target.gen.model.json`：`deepseek-flash`、http 200、**finish=stop**、usage `{2394,6582,5326,8976}`、attempts 1、`truncated=false`；`target.gen.rb` sha256 `24f71313…f71e`、**139 行**。
- `03-self-review`：`self-review-1.json` verdict **`NO-REPAIR-IDENTIFIED`**、items []；system.txt 多一条“重点核对输出逐字节（空行、`=` 分隔线长度、顺序）”；`self-review-1.model.json`：finish=stop、`truncated=false`、usage `{3074,24547,24426,27621}`、items 0。
- **job-00** `eval-20261012-052643-e7e0b395`：build `completed/0`(66ms)；execution `completed/**0**`(33ms)，stdout 起于 `共找到 0 个文件…`（`sizeBytes`/`digest` 落在**工具截断区**，不可读）；log `05:26:43.256265Z → 05:27:12.530437Z`。
- **job-01** `eval-20261012-053042-e58aef72`：两侧 build `completed/0`（源 69ms / 目标 248ms，目标 `Syntax OK\n` 10 B）、两侧 execution `completed/**0**`（源 34ms / 目标 565ms）；`comparison.json` **`matched`、`diffs=[]`**；报告 **PASS / MATCHED / CLEAN**、coverage 1/1；closure 同型；log `05:30:42.220226Z → 05:31:43.552300Z`。
- `result.md`（39 行）：**DONE / matched**；交付根级 `target.rb` 139 行 sha `24f71313…f71e`；`evaluator_manifest.json`：`sceneTags=[file-io]`、`hasReplayArtifact=true`。
- **实体缺失**：`target.rb`、`capsule.zip` 均无实体。
- **未定**：两侧 1178 B / digest `0fe7d9cf…` 目前只有 `self-review-1.user.md` L5、`job-01/metadata.json` L5、`result.md` 的自述；原始字段落在**工具截断区**，未逐字复核。
- **覆盖边界**：仅“无数据文件”路径；有真实 `index*_30_codes_full.json` 数据的路径未覆盖。

## D2-271 — getTGT.py（SOURCE_DEPENDENCY_GAP）
- 冻结（31 行）：sha256 `98240F…7ABA`、**120 行**；Impacket L27-32。
- 分类（61 行）：**`LOW_SIGNAL`、`reviewGroups=[]`、signals 全空、`has_network=false`、`network_mode=none-detected`**；`inputManifestSha256=5a15cf0c…7f12`。
  ⇒ 与冻结自述“Kerberos TGT 获取、网络到目标”**不一致**（词法漏检；源已删，无法定性）。
- job-00 `eval-20261012-053259-5d21dc36`：build `completed/0`(66ms)；execution `completed/**1**`(118ms)，stderr = `Traceback … getTGT.py", line 27 … from impacket import version\nModuleNotFoundError: No module named 'impacket'`；`evaluation_report.json` 记 `buildAssessment=passed`、`executionAssessment=completed`、**`failure=null`**（**运行失败未登记为 failure**）；closure `complete/cleanupConfirmed=true`、`issues=[]`；log `05:32:59.928355Z → 05:33:29.210028Z`；报告两件正常。
- `result.md`（40 行）：**DONE / `SOURCE_DEPENDENCY_GAP`**、0 模型调用；恢复条件=快照内合法 impacket 后重新冻结并重分类。

## D2-272 — colorsys.py（PREPARATION_GAP）
- 冻结（27 行）：sha256 `B5F4CA…B8D2`、**166 行**；CPython 标准库副本、**无 `__main__`**。
- 分类（65 行）：`REVIEW_SIDE_EFFECTS`、`ALLOWED`、signals **process[3]**、`inputManifestSha256=b3a4d414…619a`；而冻结称“仅含数学常量与函数定义/无 import 语句” ⇒ **L3 的 process 命中疑似词法误报**（源已删，不可确证）。
- job-00 `eval-20261012-053412-fa4080ba`：build `completed/0`(66ms)；execution `completed/**0**`(19ms)、**stdout 0 B（digest `e3b0c442…b855` 空串）与 stderr 0 B**；报告正常；log `05:34:12.622771Z → 05:34:41.721399Z`。
- `result.md`（34 行）：**DONE / `PREPARATION_GAP`**、0 模型调用；恢复条件明列“合法中性入口或 `LIB_UNOBSERVABLE_COMPILE_ONLY` 逐项举证”。
- **与现行规则对照**：属 `LIB_UNOBSERVABLE_COMPILE_ONLY` 形态 ⇒ 现行规则下应继续生成 + 目标语法/编译验证。

## D2-273 — smbserver.py（SOURCE_DEPENDENCY_GAP）
- 冻结（31 行）：sha256 `4AA5E4…303B`、**138 行**；Impacket L23-25、有入口 L27。
- 分类（95 行）：`REVIEW_NETWORK`、`ALLOWED`、`requiresNetworkIsolation=false`；`network_mode=**wildcard**`、targets `0.0.0.0`(L51/L79)、`::`(L51/L79)（`redirectVerified=false`）；`inputManifestSha256=8bb268db…0dd08`。
  ⇒ **wildcard 绑定却 `requiresNetworkIsolation=false`**（依赖批次层隔离；记录不改判）。
- job-00 `eval-20261012-053525-f21ec868`：build `completed/0`(67ms)；execution `completed/**1**`(123ms)、stderr impacket L23；`failure=null`；closure/report 正常；log `05:35:25.609030Z → 05:35:55.586450Z`。
- `result.md`（40 行）：**DONE / `SOURCE_DEPENDENCY_GAP`**、0 模型调用。

## D2-274 — mssqlclient.py（SOURCE_DEPENDENCY_GAP；**报告缺件**）
- 冻结（31 行）：sha256 `F17A05…8F90`、**167 行**；Impacket L26-29、有入口 L32。
- 分类（66 行）：`REVIEW_NETWORK`、`ALLOWED`、`requiresNetworkIsolation=false`；`network_mode=unresolved`、`network_targets=[]`、signals network[41,129]；`inputManifestSha256=e968a931…f2ec`。
- job-00 `eval-20261012-053638-17057036`：build `completed/0`(66ms)；execution `completed/**1**`(117ms)、stderr impacket L26。
- **⚠ 报告缺件**：`evaluation_report.md` = `{"detail":"job_human_report_not_found"}`；`evaluation_report.json` = `{"detail":"job_report_not_found"}`；`controller.log` **只有 created `05:36:38.165702Z`，无 finished**。而 `closure.json` 记 `complete=true`、`cleanupConfirmed=true`、`issues=[]`、`attempts=1`；`result.md`（40 行）仍写“交付完整性 完成（按去向适用件齐备）”。
  ⇒ **同一 job 内“报告未取回/无完成时间戳”与“closure 已闭合 + result 记完成”并存**。
- `events.jsonl:1061–1062` 仍写入 SOURCE_PRECHECK 与 TERMINAL ⇒ **终态事件独立于 job 报告落盘**。
- 去向：**DONE / `SOURCE_DEPENDENCY_GAP`**、0 模型调用。

## 本组共性

**原始事实**
- 269/270 为唯一进入转换者：生成 1 次 + 自审 1 次（各 2 次模型调用），`finish_reason=stop`、`truncated=false`、`attempts=1`；两侧 `matched`、`diffs=[]`、coverage 1/1、closure `complete/cleanupConfirmed=true`、`issues=[]`。
- 271–274 只有 `job-00` 源侧预检，**无 comparison、无判词、无 diffs**；`closure` 均 `complete/cleanupConfirmed=true`、`attempts=1`。
- 6 例均**无重分类、无旧件删除、无失败 attempt、无 WAITING**；`classifierVersion=2.4`、`classifierSha256=009a6f31…f3a4`、`contractHash=8090cfcc…` 全同。
- `manifest Lines` 6/6 与 frozen/result 不符（差 10/8/16/22/19/23，manifest 一律偏小）。

**判定（本会话）**
- 269/270 的 `matched` 只在“冻结单输入 + output 单维度”范围内成立（报告自述 oracle `UNVERIFIED / not requested`、provenance `UNVERIFIED`），**不等于功能等价**。
- 271/273/274 的 `SOURCE_DEPENDENCY_GAP`（impacket 快照外）与 272 的 `PREPARATION_GAP`（无入口）与其真实源侧诊断自洽。
- **274 的报告占位 + log 缺 finished 是真实证据缺口**；与 250/264/275/277 同型，本区间合计 **7 项**（见 [findings](harness-d-findings.md)）。
- **271/273 的 `failure=null` 与 `execution.exitCode=1` 并存**：平台报告层未把源运行失败登记为 `failure`，去向系人工归因。
- 272 属现行 `LIB_UNOBSERVABLE_COMPILE_ONLY` 形态。

**未定**
- 各例真实行数与 sha256：源件、目标件、capsule 均不在工作区，**不可复核**（`**/*.rb`、`**/source/**`、`**/capsule*` 全 0 命中）。
- 271 的网络词法漏检、272 的 process[3]：源已删，**不可定性**。
- 269/270 的 `request.body.json`、`target.gen.raw.json`、`self-review-1.body/raw.json` 均**缺失**；`request.user.md`/`self-review-1.user.md` 的 `@SOURCE@`/`@TARGET@` **仍是未替换占位符** ⇒ **实际注入模型的源/目标全文不可审**（只有 `.model.json` 的 usage/finish_reason 元数据）。
- 270 的 1178 B/digest 落在工具截断区，未逐字复核。

---

## 补读（read 单行上限提高至 1048576 后，2026-10-12）

**本组原截断件（22 件）已全部全文读到**：`269/270` 各 `job-00` 两件（4）、`269 job-01` 五件、`270 job-01` 五件、`271/272/273/274` 各两件（8）。上述第 35、86 条的“未逐字复核/未读到”**全部解除**。

**补读新增的原文事实（本组）**
1. **D2-270 的 1178 B / digest 直读**：`execution.stdout{sizeBytes:1178, digest:"sha256:0fe7d9cfff727fb156f35e4a202e1d33b93c1f7d831c014ac6ef5eaca66b62e5", truncated:false}`，且 **job-00 源、job-01 源、job-01 目标三处完全相同**（job-01 `evidence-target.json` 亦为 1178 B / 同 digest）⇒ 双侧 stdout **逐字节一致**由原件确认；stderr 两侧 0 B；两侧 exit 0。
2. **D2-269**：源/目标 stdout 均 `"Connection to 127.0.0.1:5389 refused\n"`、`sizeBytes 37`、`digest sha256:8296cc0ca8d913d66157a565af8eac0cee9c80b41929e4977dafa04aa38cd8f2`，两流 stderr 均 0 B，两侧 exit 1；目标 build stdout `"Syntax OK\n"` 10 B（digest `bbafef10…4a1b`）。
3. **此前不可读的 stderr digest**：D2-271 `sha256:95c43b55f55b66a674a122e0901dd17f186686909576c4e20f64131b1235e41d`/232 B（getTGT.py L27）；D2-273 `sha256:87fb784e5c318a5fb4da0534cc6c813140bc6a6b8797d52bc184c43c752335a9`/243 B（smbserver.py L23）；D2-274 `sha256:f56ef6048c1ab10b3c283a3265604b0f01e289d14ffe6056056f808b9e31c1c4`/245 B（mssqlclient.py L26）；D2-272 两流 0 B（空串摘要）。
4. **D2-274 的“报告占位 vs closure 闭合”原文并置**：`closure.json` 全文为 `"complete":true, "cleanupConfirmed":true, "issues":[], "cleanupRecords":{"source":{"status":"passed","runnerStateAfter":"READY","attempts":1,"contaminated":false,"reason":null}}, "checkedAt":"2026-10-12T05:37:11.660542+00:00"`，同时 `artifactDigests` 仍列 `evaluation_report.json` `sha256:d5725433…` 与 `.md` `sha256:3b64a48f…`，而本地同路径文件是 `{"detail":"…_not_found"}` 占位。
5. **closure 键数与 roles**：`269/270/271/272/273/274 job-00` 均 **16 键**；`269 job-01`、`270 job-01` 均 **23 键**且 `roles.target={…"NOT_APPLICABLE"}`；六项的尾三字段均为 `UNVERIFIED/UNVERIFIED/checkedAt`。
6. `evidence-source.json` 全结构与 cases-01 补读第 3 条同型。

**未解除**：`Lines` 6/6 不一致；269/270 的 `target.rb`/`capsule.zip` 无实体、`@SOURCE@` 占位；274 报告占位；源已删导致的行数/哈希不可裁定——**均不因补读改变**。
