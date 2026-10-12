# Harness D — 逐项审阅记录 03（python-to-go：D2-255 … D2-261）

> 7 例共 **133 件**（255/257/258/259/260/261 各 15；**256 为 43**，含 02-conversion 6、03-self-review 8、job-00/job-01 与 `evaluator_manifest.json`），由本会话派出的只读子会话逐件读取，本会话与 batch 层交叉核对。

| taskId | 源文件 | manifest Lines | frozen/result | 分类 | 源预检 job | build | execution | 去向 |
|---|---|---|---|---|---|---|---|---|
| D2-255 | wmipersist.py | 214 | **246** | REVIEW_SIDE_EFFECTS | `eval-20261012-044800-1b775738` | completed/0 (67ms) | completed/**1** (116ms)，stderr=impacket L56 | SOURCE_DEPENDENCY_GAP |
| D2-256 | sigthief.py | 230 | **269** | REVIEW_NETWORK（重分类） | job-00 `eval-20261012-044951-48701ab3`；job-01 `eval-20261012-050231-6348d449` | 两侧 completed/0 | 两侧 completed/**2**，stdout 724 B + stderr 73 B | **CONVERTED / matched** |
| D2-257 | string.py | 255 | **309** | LOW_SIGNAL | `eval-20261012-050521-4ddbf73e` | completed/0 (67ms) | completed/**0** (17ms)，两流 0 B | PREPARATION_GAP |
| D2-258 | filecmp.py | 260 | **313** | REVIEW_SIDE_EFFECTS | `eval-20261012-050650-1ff01dcb` | completed/0 (67ms) | completed/**1** (119ms)，stderr=含 job 特定路径的 traceback | PREPARATION_GAP |
| D2-259 | findDelegation.py | 251 | **285** | REVIEW_NETWORK | `eval-20261012-050823-b2e16fcf` | completed/0 (65ms) | completed/**1** (118ms)，stderr=impacket L28 | SOURCE_DEPENDENCY_GAP |
| D2-260 | GetADComputers.py | 210 | **236** | REVIEW_NETWORK | `eval-20261012-050949-e0457310` | completed/0 (68ms) | completed/**1** (119ms)，stderr=dns L32 | SOURCE_DEPENDENCY_GAP |
| D2-261 | glob.py | 219 | **251** | REVIEW_SIDE_EFFECTS | `eval-20261012-051100-656520ab` | completed/0 (67ms) | completed/**0** (34ms)，两流 0 B | PREPARATION_GAP |

## D2-255 — wmipersist.py（SOURCE_DEPENDENCY_GAP；**报告缺件**）
- 冻结（31 行）：sha256 `30A5AE…C502`、**246 行**；Impacket、入口 L166、`impacket.*` L56-61。
- 分类（65 行）：`REVIEW_SIDE_EFFECTS`、`ALLOWED`/null、2.4、`009a6f31…f3a4`、`requiresNetworkIsolation=false`；signals filesystem[190]；`inputManifestSha256=bd643a4c…b087`。
- job-00：build `completed/0`(67ms)、execution `completed/**1**`(116ms)、stdout 0 B、stderr = `Traceback … wmipersist.py", line 56 … from impacket.examples import logger\nModuleNotFoundError: No module named 'impacket'`。
- **⚠ 报告缺件**：`evaluation_report.json` = `{"detail":"job_report_not_found"}`；`.md` = `{"detail":"job_human_report_not_found"}`；`controller.log` **只有 created `04:48:00.092054Z`，无 finished**。`closure.json` 仍 `complete/cleanupConfirmed=true`、`issues=[]`、`attempts=1`。
- `result.md`（43 行）：**DONE / `SOURCE_DEPENDENCY_GAP`**、0 模型调用。

## D2-256 — sigthief.py（**CONVERTED / matched**）
- 冻结（33 行）：sha256 `E982DB…B6D8`、**269 行**（明记 manifest 230 为旧口径）；纯标准库 `sys/struct/shutil/io/optparse`(L5-9)、入口 L215；argv=[] ⇒ `print_help()`(stdout)+`parser.error("You must do something!")`(stderr) ⇒ exit 2。
- 分类（重分类）：`events.jsonl:994` 首轮 `BLOCKED`/`public_network_unverified`（`github.com` 在 L217 `print()` sponsor banner 字符串内 ⇒ 词法误判）；`:995` 重分类 ⇒ `classification-2.json`（85 行）`REVIEW_NETWORK`、`ALLOWED`、`requiresNetworkIsolation=true`、`network_targets=[{github.com, L217, hostname, literal, redirectVerified=false}]`、`old_cls/old_reason=null`；`classification-1.json` 已删（`01-frozen` 只剩 `-2` 两件）。
  - **内部张力**：同文件 `files[0].signals.network=[]` 但 `has_network=true`；job 内 `batch-authorization.json` 的 confirmation 写“无网络”，与 `requiresNetworkIsolation=true` 冲突。
- `02-conversion`（6 件）：`request.system.txt`（9 行，义务含“argv=[] 下 stdout/stderr 逐字节一致、exit 2、真实实现选项解析、不得固定字符串绕过”）；`request.user.md`（66 行，**知识注入声明处**：python.md L1-PY-01/02/04、go.md L1-GO-01…07、方向规则 1-4；源基线 stdout **724 B** digest `c0ee18c0…856a`、stderr **73 B**、exit 2；`@SOURCE@` 占位“共 269 行”）。
  - `target.gen.model.json`：`deepseek-flash`、http 200、**`finish_reason=stop`**、usage `{prompt 4581, completion 55000, reasoning 48423, total 59581}`、attempts 1、`truncated=false`；`knowledge_injected` 4 条；产物 **`target.gen.go` 907 行** sha256 `660aa81e…7a4c`。
  - `self-repair-1.model.json`：`SELF_REPAIRED` turn 1；**finish=stop**、usage `{7086,11926,5138,19012}`、`truncated=false`；产物 **`target.self-repair-1.go` 930 行** sha256 **`989f7e74…3553`**（＝`result.md` 声明的最终 `target.go` sha）；`appliedFixes` 2 项。
- `03-self-review`（8 件）：`self-review-1.json` **`REPAIR-RECOMMENDED`、2 项**（`opt-abbrev` 长选项唯一前缀缩写；`opt-missing-arg-msg` 缺参文案），**均 `minor`/`conversion-introduced`**，两条 `risk` 均自述“冻结 argv=[] 不受影响”；`self-review-2.json` **`NO-REPAIR-IDENTIFIED`、items=[]**，`decision="internal pre-check passed …; proceed to dual-side submission"`。两轮 model.json 均 `finish=stop`、`truncated=false`。**采纳 2/2、拒绝 0**。
- **job-00** `eval-20261012-044951-48701ab3`：build `completed/0`(65ms)、execution `completed/**2**`(32ms)、stdout **724 B**、stderr **73 B**（`Usage: sigthief.py [options]\n\nsigthief.py: error: You must do something!\n`）；报告两件正常；log `04:49:51.713029Z → 04:50:20.753322Z`。
- **job-01** `eval-20261012-050231-6348d449`：`comparison_manifest.json` source python `py_compile`/`python sigthief.py`，target go `["go","build","-o","program","target.go"]`/`["./program"]`；源 build `completed/0`(70ms)、exec `completed/**2**`(34ms)，目标 build `completed/**0**`(7947ms)、exec `completed/**2**`(4ms)；`comparison.json` **`behaviorVerdict=matched`、`diffs=[]`**（output matched；其余四维 not-applicable）；`evaluation_report.json/.md`：**PASS / MATCHED / CLEAN**、`runVerdict=runnable`、`codeVerdict=passed`、coverage 1/1；`closure`：`complete/cleanupConfirmed=true`、两侧 attempts 1、`issues=[]`；log `05:02:31.105211Z → 05:03:38.878365Z`。
  - 子会话用 grep 探针确认：`"sizeBytes":724`、`"sizeBytes":73`、`c0ee18c0…856a`、`a68beb9d…4a60` 在 **job-00 源 / job-01 源 / job-01 目标**三份 evidence 中**均命中**；`"truncated":true` **无命中**。
- `result.md`（43 行）：**DONE / matched**；`evaluator_manifest.json`（47 行）：`languagePair python→go`、`sceneTags=[]`、`files[0].relativePath=target.go`、`hasReplayArtifact=true`、`replayArtifactPath=04-evaluation/job-01-dual-build/capsule.zip`、`x_adapter{jobId=…6348d449, sourcePreflightJobId=…48701ab3, syntaxVerdict=PASS, behaviorVerdict=matched}`。
- **实体缺失**：`**/*.go`、`**/capsule*`、`**/source/**`、`request.body.json`、`target.gen.raw.json`、`target.gen.go`、`target.self-repair-1.go`、`self-review-*.body/raw.json` **全部 0 命中** ⇒ 声明的交付物与原始请求/响应**无实体**；`request.user.md`/`self-review-*.user.md` 的 `@SOURCE@`/`@TARGET@` **仍是占位符** ⇒ **实际注入模型的源/目标全文不可审**。
- **目标路径三说**：`evaluator_manifest.json`=`target.go`（根级）/ `job-01/metadata.json`=`target/target.go` / `result.md`=“根级 target.go”。
- **`batchReportPath="../../../README.md"`** 以 `targetDir="."` 解析得 `python-to-go/README.md`（**不存在**）。
- **覆盖边界**：仅 `argv=[]` 帮助/错误路径；`rip/add/checksig/sign/truncate` 未验证。
- **未定**：`target.gen.model.json` 的 `completion_tokens=55000`（整千，疑似触顶）但 `finish_reason=stop`/`truncated=false` — 无证据判为截断，仅登记。

## D2-257 — string.py（PREPARATION_GAP；**报告缺件**）
- 冻结（27 行）：**frozen-inputs.md 未写出 sha256 值**（只写“见 manifest `Sha256` 列，大写”）——本区间唯一如此；**309 行**；CPython `Lib/string.py` 副本、无 `__main__`；依赖 `_string` L21 / `re` L52 / `collections.ChainMap` L53。
- 分类（61 行）：`LOW_SIGNAL`、`ALLOWED`、`reviewGroups=[]`、**signals 全空**；`inputManifestSha256=ade486f9…1ffb`。
- job-00：build `completed/0`(67ms)、execution `completed/**0**`(17ms)、**两流 0 B**、digest `e3b0c442…`；`observations.output={status:observed, events:[], limitations:[]}`。
- **⚠ 报告缺件**：两份 report 均为 `job_*_not_found` 桩；`controller.log` **只有 created `05:05:21.256824Z`，无 finished**；`closure` 仍 `complete/cleanupConfirmed=true`、`issues=[]`。
- `result.md`（36 行）：**DONE / `PREPARATION_GAP`**、0 模型调用；恢复条件明列“合法中性入口或 `LIB_UNOBSERVABLE_COMPILE_ONLY` 举证” ⇒ 属现行 LIB 分支形态。

## D2-258 — filecmp.py（PREPARATION_GAP）
- 冻结（33 行）：sha256 `AA9E25…198F`、**313 行**；CPython `Lib/filecmp.py` 副本、**有入口 L312 `demo()`**；`demo()` L300-310 用 `getopt.getopt(sys.argv[1:],'r')`，位置参数≠2 ⇒ `raise getopt.GetoptError('need exactly two args')`；**预判 traceback 含 job 特定绝对路径 ⇒ 观察不可冻结**。
- 分类（65 行）：`REVIEW_SIDE_EFFECTS`、`ALLOWED`、signals filesystem[77]；`inputManifestSha256=28b55a53…fe85`。
- job-00：build `completed/0`(67ms)、execution `completed/**1**`(119ms)、stdout 0 B、stderr = `Traceback … File "/var/lib/codeconvert-agent/workspaces/eval-20261012-050650-1ff01dcb/source/filecmp.py", line 313 … demo() … File "…filecmp.py", line 30…`（**含 jobId 的绝对路径**）。
- `evaluation_report.json/.md` **正常**；`controller.log` created `05:06:50.462677Z` → finished `05:07:19.671435Z`。
- `result.md`（45 行）：**DONE / `PREPARATION_GAP`**、0 模型调用；恢复条件=合法两目录 fixture 或改冻结条件。
- **与同类对照**：`optimization-inputs-2.md §2.3②` 把 D2-258 与 D2-210/232/233 同列“观察含 job 特定绝对路径”类。

## D2-259 — findDelegation.py（SOURCE_DEPENDENCY_GAP）
- 冻结（31 行）：sha256 `BD69A6…4167`（自称“本地 sha256sum 实测一致”）、**285 行**；Impacket、入口 L224、`impacket.*` L28-33。
- 分类（65 行）：`REVIEW_NETWORK`、`ALLOWED`、`requiresNetworkIsolation=false`、signals network[236]、`network_mode=unresolved`；`inputManifestSha256=3c462c50…98b3`。
- job-00：build `completed/0`(65ms)、execution `completed/**1**`(118ms)、stderr=impacket L28；报告正常；log `05:08:23.569985Z → 05:08:52.760399Z`。
- `result.md`（40 行）：**DONE / `SOURCE_DEPENDENCY_GAP`**、0 模型调用。

## D2-260 — GetADComputers.py（SOURCE_DEPENDENCY_GAP）
- 冻结（31 行）：sha256 `723F68…EF84`、**236 行**；Impacket、入口 L181；`impacket.*` L35-39 + `dns.resolver`(dnspython) L32。
- 分类（65 行）：`REVIEW_NETWORK`、`ALLOWED`、signals network[187]、unresolved；`inputManifestSha256=efcf2d75…c0fc`。
- job-00：build `completed/0`(68ms)、execution `completed/**1**`(119ms)、stderr=`import dns.resolver → ModuleNotFoundError: No module named 'dns'`(L32)；报告正常；log `05:09:49.340380Z → 05:10:18.127730Z`。
- `result.md`（40 行）：**DONE / `SOURCE_DEPENDENCY_GAP`**、0 模型调用。

## D2-261 — glob.py（PREPARATION_GAP）
- 冻结（27 行）：sha256 `C99EF5…0BE0`、**251 行**；CPython `Lib/glob.py` 副本、无 `__main__`；依赖 contextlib/os/re/fnmatch/itertools/stat/sys。
- 分类（65 行）：`REVIEW_SIDE_EFFECTS`、`ALLOWED`、signals filesystem[147]；`inputManifestSha256=0ffffb09…ef46`。
- job-00：build `completed/0`(67ms)、execution `completed/**0**`(34ms)、**两流 0 B**；`observations.output={status:observed, events:[], limitations:[]}`；报告正常；log `05:11:00.708864Z → 05:11:29.843220Z`。
- `result.md`（34 行）：**DONE / `PREPARATION_GAP`**、0 模型调用 ⇒ 属现行 LIB 分支形态。

## 本组共性

**原始事实**
- 8 个 job（256 有 2 个）全部有 `job-id.txt`、`closure.json`；`closure` 均 `complete=true`、`cleanupConfirmed=true`、`issues=[]`、`attempts=1`、`contaminated=false`、`runnerStateAfter=READY`。
- 7 例 items 全 `lifecycle=DONE`；`events.jsonl:991–1017` 与 items 逐项一致；**无 WAITING、无未知提交**。
- 7/7 均无失败模型 attempt（`.model.json` attempts 全 1、`truncated=false`、`finish_reason=stop`；closure attempts 全 1）。
- **`manifest Lines` 7/7 与 frozen/result 不符**（差 32/39/54/53/34/26/32，manifest 一律偏小）。

**判定（本会话）**
- 256 的 `matched` 有**三份原始 evidence + comparison.json + 报告 + items + events** 支撑（源/目标 stdout 724 B、stderr 73 B digest 相同、exit 2 相同、diffs=[]）；**但交付物与原始请求/响应无实体**，`@SOURCE@/@TARGET@` 未替换 ⇒ “知识实际注入”与“交付完整性”**在本地不可复核**。
- 257/258/261 的 `PREPARATION_GAP` 与其真实源侧观察自洽（257/261 无入口空输出；258 job 特定路径不可冻结）；其中 257/261 属现行 `LIB_UNOBSERVABLE_COMPILE_ONLY` 形态。
- 255/259/260 的 impacket/dns 缺件与 `SOURCE_DEPENDENCY_GAP` 自洽。
- **255 与 257 的报告占位 + log 缺 finished 是真实证据缺口**（与 250/264/274/275/277 同型；本区间合计 **7 项**）。

**未定**
- 真实行数/sha256：源件均不在工作区（`**/source/**` 0 命中），**不可复核**。
- `closure.json`/`evidence-source.json` 单行 >2000 字符 ⇒ `closure` 的 `"ora…"` 段、`observations` 尾部、部分 stderr 尺寸/digest **未读到，不臆测**（产品侧 `truncated` 字段在可读区均为 `false`）。
- 256 的三处目标路径口径与 `batchReportPath` 失效：**记录不改**。

---

## 补读（read 单行上限提高至 1048576 后，2026-10-12）

**本组原截断件（19 件）已全部全文读到**：`255/257/258/259/260/261` 各 `{evidence-source.json, closure.json}`（12）、`256 job-00` 同两件、`256 job-01` 的 `{evidence-source.json, evidence-target.json, comparison.json, evaluation_report.json, closure.json}`（5）。第 89 条的“未读到，不臆测”**全部解除**。

**补读新增的原文事实（本组）**
1. **closure 尾段**：六个源预检 job + `256 job-00` 均 **16 键**、尾三字段 `oracleStatus/programOutputProvenance="UNVERIFIED"`、`checkedAt`；`256 job-01` **23 键**、`roles` 多 `target{…"NOT_APPLICABLE"}`。
2. **D2-256 的 724 B / 73 B 由直读确认（grep 探针退役）**：job-00 源、job-01 源、job-01 目标三份 evidence 的 `execution.stdout{normalizedText:"…Usage: sigthief.py [options]…", sizeBytes:724, digest:"sha256:c0ee18c0627a466c8ff9051d3e0573712cdeb1a5045ce1e515e8eacaecaa856a", truncated:false}`、`stderr{normalizedText:"Usage: sigthief.py [options]\n\nsigthief.py: error: You must do something!\n", sizeBytes:73, digest:"sha256:a68beb9d2dc980b1a64c6c2140f5c97398324bc994f150b2a826170003154a60"}`、`exitCode 2` **三处逐字段相同**。
   - 顺带定位词法误判来源：stdout 首行含 `https://github.com/sponsors/secretsquirrel`（L217 sponsor banner）。
3. **此前不可读的 stderr digest**：D2-255 `sha256:8dd4cd20cab26f1325e2a8caa48411154f7113fc613c97c5e0a8e7d2d246d15a`/244 B（wmipersist.py L56）；D2-258 `sha256:83ff27398abb328dc08787ebf85eb82668a16c89aefc55507d2c2ee993dd37a4`/391 B（**`filecmp.py` L313 `demo()` → L305 `raise getopt.GetoptError`**，全文含 `/var/lib/codeconvert-agent/workspaces/eval-20261012-050650-1ff01dcb/source/filecmp.py` job 特定路径）；D2-259 `d808c50d…`/240 B；D2-260 `e4f26606510275d5cb0be7c83f7ed1968ab6ba84db877c9408ac4acf636d01d7`/226 B（`import dns.resolver` L32）。
4. **257/261 的“两流 0 B”现为原文**（`sizeBytes 0`、空串 digest `e3b0c442…b855`、`truncated:false`）。
5. `evidence-source.json` 结构与 cases-01 补读第 3 条同型（`observations.*.events` 全空、`coverage` output-only、`toolchainFingerprint {}`）。

**未解除**：`Lines` 7/7 不一致；256 的 `target.go`/`capsule.zip`/请求响应体无实体且 `@SOURCE@` 未替换；255/257 报告占位与 closure 闭合并存——**均不因补读改变**。
