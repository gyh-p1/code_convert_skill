# harness-E 覆盖索引（D2-278 … D2-300）

> 状态：**IN_PROGRESS**（原“COMPLETE”结论**已被官方读取上限提高后的补读要求取代**，见[增补读取记录](harness-e-supplement-reread.md)：46 件曾被截断的单行原件中已补读 **8 件**，**38 件仍为 `read(截断)`**，另有 5 项报告占位与未回传件未解除，故**不得**声明本组完成）。
> 读取覆盖：23 项、每项 15 件、合计 **345 件**均已用 read 打开并登记状态（表与逐项清单见下）。**截断、占位、未回传三类均不计为“已读”**。
> 声明边界：本文件**只**声明 D2-278…D2-300 共 23 项的文档审阅覆盖；**不**声明全数据集 277 项已完成，也不与其它会话（A/B/C/D/Codex）重复作全量完成声明。
> 范围：`../../../manifest.csv`（= `docs/dataset-2/dataset-2-copy/manifest.csv`）中 Id 从 `D2-278` 到 `D2-300` 的**全部 23 个在册项**。该区间连续、无移除编号，故区间宽度 23 = 实际待审 23（与用户给定的独占范围一致）。
> 计数对账：manifest 277 在册项；本会话 23 项 + 会话 A 73 + 会话 B 79 + 会话 C 62 + 会话 D 34 + Codex 6 = 277，无重叠、无遗漏。本文件**不作**全数据集完成声明。
> 方法：纯静态、只读；**只用原生 read/glob/grep 手工分段读**。未写/生成/保存/运行任何辅助脚本、分析程序、工具或循环扫描；本机 PowerShell 在该沙箱下不可用（`SetNamedSecurityInfoW failed (Win32 5)`），故全程未用 shell 分析。**未**运行样本/目标代码/构建/分类器，**未**调用转换模型，**未**提交评估，**未**访问 `D:/CodeConvertRemote/Stack` 及 `jobs`，**未**读 `.env`/密钥/凭证/无关个人材料，**未**安装软件，**未**改任何原始证据、`items/events`、旧报告、状态、自审；**原源与目标已删，未恢复、未写目标代码**。
> 分工声明：本文件与 [findings](harness-e-findings.md)、[cases-01](harness-e-cases-01.md)/cases-02/cases-03 为 harness-E **新写**文件，未改其它会话文件。逐项读取由 harness-E 主会话与其受命的**只读读者**共同完成；凡由读者回填的字段在 cases 中标注“reader 回填”，本人另行直读高信号原件复核。
> 判定分层：交付完整性 / 源侧语法·编译（**非目标结论**）/ 功能一致性 分列；**无目标代码即无目标编译/行为/比较证据**，本批 23 项全部如此。

## 全局判定前置事实（对 23 项全部适用，来源为本副本现存正文）

- **均无门槛缺口外的动态步骤**：23 项 `Kind=NEW`、`JobId` 列空、`Evidence=UNVERIFIED (not built, not run)`，均为“源侧预检后即停”的去向。
- **均无模型调用、无自审、无比较**：目录内无 `02-conversion/`、`03-self-review/`、`self-review-*.json`、`comparison/`、`*.model.json`、目标代码。故“每次模型请求与真实 content/元数据”“失败/废弃/重提 attempt”“自审全部建议及 scope/risk/unresolved”“修订与裁决”在本批**无对象**（未发生，非缺档）。
- **每项只有一个 job**：`04-evaluation/job-00-source-buildability/`，其 `controller.log` 只有 `comparison job created` / `comparison job finished` 两行，是**源预检 job 生命周期**，不是双侧比较。
- **`closure.json` 的 `artifactDigests` 含未回传件**：`evidence/source-call.json`、`evidence/source-identity.json`、`evidence/source-request.json`、`evidence/source-response.body`、`request.json`、`lifecycle.jsonl`、`staging-manifest.json` 只在摘要中出现，**未落到用例目录**；本审阅不据摘要推演其正文，登记为“未回传件”。
- **长单行 JSON 截断**：每项 `returned-evidence/evidence-source.json` 与 `closure.json` 都是单行长 JSON，原生 read/grep 在 **2000 字符**处截断；中段（build/execution 两流、digest、sizeBytes、snapshot、runner）已完整读到，**尾部字段未读**，逐项状态记 `read(截断)`。
- 路径事实：各 `frozen-inputs.md` 的 `casePath` 写 `docs/test/dataset-2/...`，该路径在本仓库**不存在**（实际为 `docs/dataset-2/dataset-2-copy/...`）；见 [findings F4](harness-e-findings.md)。
- 口径差异：各项冻结记录/`result.md` 声明行数与 manifest `Lines` **全部不等**；见 [findings F3](harness-e-findings.md)。

## 更正登记（本人先前登记的读取错误，已按磁盘实况撤销）

- **更正 1（撤销“D2-285 缺 3 件”）**：本人初次 `glob` 输出被截断，据以写成“D2-285 缺 `input_profile.json`/`batch-authorization.json`/`controller.log`，件数 14”。**重新逐件 `glob` 证实 D2-285 共有 15 件，上述三件均存在**（`input_profile.json` 已直读 22 行正文）。因此**全部 23 项件数一致，均为 15 件，合计 345 件**；`../reconciliation-6.md` 与 `result.md` 关于该项“适用件齐备”的表述**成立**，findings 原 F6 撤销。
- **更正 2（`-2` 分类件的项数）**：本人先前写 4 项（287/292/293/298 之外的判断）不准确。按磁盘实况，`01-frozen` 只存 `-2` 件的是 **5 项**：D2-287、D2-292、D2-293、**D2-298**（原登记漏记）；其余 **18 项**只存 `-1` 件。
- **更正 3（D2-285 读取状态）**：其 `controller.log`、`input_profile.json`、`batch-authorization.json` 均为 `read`（非 missing）；D2-285/286/287 的 `evidence-source.json` 与 `closure.json` 仍为 `read(截断)`。
- 本文件其余计数与结论不变（23 项、无模型调用、无目标代码、每项只有一个源预检 job）。
## 项 → 实际目录映射与整体状态

目录基准：`../../../<direction>/<case>/`（相对本文件）。件数 = 该用例目录下现存普通文件数（含 `returned-evidence/`）。终态取自 `result.md` 与批次台账 `../reconciliation-6.md`。

| Id | Kind | Direction | 源文件 | manifest 行 | 实际目录（相对本目录） | 件数 | jobId | 终态 | Read |
|---|---|---|---|---|---:|---|---|---|---|
| D2-278 | NEW | ruby-to-c | open3.rb | 718 | `../../../ruby-to-c/D2-278-ruby-open3.rb/` | 15 | eval-20261012-054247-f8b64c8b | DONE / PREPARATION_GAP | 已读（2 件截断） |
| D2-279 | NEW | ruby-to-cpp | delegate.rb | 415 | `../../../ruby-to-cpp/D2-279-ruby-delegate.rb/` | 15 | eval-20261012-054408-bbd40bb6 | DONE / PREPARATION_GAP | 已读（2 件截断） |
| D2-280 | NEW | ruby-to-cpp | erb.rb | 485 | `../../../ruby-to-cpp/D2-280-ruby-erb.rb/` | 15 | eval-20261012-054521-9ae80b6a | DONE / PREPARATION_GAP | 已读（2 件截断） |
| D2-281 | NEW | ruby-to-cpp | ostruct.rb | 449 | `../../../ruby-to-cpp/D2-281-ruby-ostruct.rb/` | 15 | eval-20261012-054636-272e9fdb | DONE / PREPARATION_GAP | 已读（2 件截断） |
| D2-282 | NEW | ruby-to-cpp | tsort.rb | 431 | `../../../ruby-to-cpp/D2-282-ruby-tsort.rb/` | 15 | eval-20261012-054749-05b85557 | DONE / PREPARATION_GAP | 已读（2 件截断） |
| D2-283 | NEW | ruby-to-csharp | forwardable.rb | 302 | `../../../ruby-to-csharp/D2-283-ruby-forwardable.rb/` | 15 | eval-20261012-054909-0a352413 | DONE / PREPARATION_GAP | 已读（2 件截断） |
| D2-284 | NEW | ruby-to-csharp | tempfile.rb | 403 | `../../../ruby-to-csharp/D2-284-ruby-tempfile.rb/` | 15 | eval-20261012-055025-5e5007b5 | DONE / PREPARATION_GAP | 已读（2 件截断） |
| D2-285 | NEW | ruby-to-csharp | enum_osx.rb | 342 | `../../../ruby-to-csharp/D2-285-ruby-enum_osx.rb/` | 15 | eval-20261012-055142-80c0dc1f | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断） |
| D2-286 | NEW | ruby-to-csharp | shellwords.rb | 222 | `../../../ruby-to-csharp/D2-286-ruby-shellwords.rb/` | 15 | eval-20261012-055302-a2a4414e | DONE / PREPARATION_GAP | 已读（2 件截断；报告占位） |
| D2-287 | NEW | ruby-to-go | psexec.rb | 212 | `../../../ruby-to-go/D2-287-ruby-psexec.rb/` | 15 | eval-20261012-055500-d1e2f188 | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断；报告占位；`-2` 件） |
| D2-288 | NEW | ruby-to-go | enum_services.rb | 175 | `../../../ruby-to-go/D2-288-ruby-enum_services.rb/` | 15 | eval-20261012-055640-8864a840 | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断） |
| D2-289 | NEW | ruby-to-go | enum_shares.rb | 172 | `../../../ruby-to-go/D2-289-ruby-enum_shares.rb/` | 15 | eval-20261012-055759-172c133c | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断） |
| D2-290 | NEW | ruby-to-go | chrome_cookies.rb | 206 | `../../../ruby-to-go/D2-290-ruby-chrome_cookies.rb/` | 15 | eval-20261012-055913-2819c120 | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断） |
| D2-291 | NEW | ruby-to-go | observer.rb | 220 | `../../../ruby-to-go/D2-291-ruby-observer.rb/` | 15 | eval-20261012-060050-c6153d88 | DONE / PREPARATION_GAP | 已读（2 件截断；报告占位） |
| D2-292 | NEW | ruby-to-powershell | cve_2021_40449.rb | 142 | `../../../ruby-to-powershell/D2-292-ruby-cve_2021_40449.rb/` | 15 | eval-20261012-060238-52b478f8 | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断） |
| D2-293 | NEW | ruby-to-powershell | process_herpaderping.rb | 167 | `../../../ruby-to-powershell/D2-293-ruby-process_herpaderping.rb/` | 15 | eval-20261012-060406-23765b7b | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断） |
| D2-294 | NEW | ruby-to-powershell | docker_creds.rb | 121 | `../../../ruby-to-powershell/D2-294-ruby-docker_creds.rb/` | 15 | eval-20261012-060527-04840085 | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断；报告占位） |
| D2-295 | NEW | ruby-to-powershell | abbrev.rb | 120 | `../../../ruby-to-powershell/D2-295-ruby-abbrev.rb/` | 15 | eval-20261012-060708-c93e8a19 | DONE / PREPARATION_GAP | 已读（2 件截断） |
| D2-296 | NEW | ruby-to-powershell | singleton.rb | 160 | `../../../ruby-to-powershell/D2-296-ruby-singleton.rb/` | 15 | eval-20261012-060825-115f4738 | DONE / PREPARATION_GAP | 已读（2 件截断） |
| D2-297 | NEW | ruby-to-python | base64.rb | 102 | `../../../ruby-to-python/D2-297-ruby-base64.rb/` | 15 | eval-20261012-060948-53dbabf8 | DONE / PREPARATION_GAP | 已读（2 件截断） |
| D2-298 | NEW | ruby-to-python | enum_av.rb | 46 | `../../../ruby-to-python/D2-298-ruby-enum_av.rb/` | 15 | eval-20261012-061116-b7a4aa6d | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断；`-2` 件） |
| D2-299 | NEW | ruby-to-python | windows_defender_exe.rb | 69 | `../../../ruby-to-python/D2-299-ruby-windows_defender_exe.rb/` | 15 | eval-20261012-061237-36d33e6a | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断） |
| D2-300 | NEW | ruby-to-python | credential_collector.rb | 100 | `../../../ruby-to-python/D2-300-ruby-credential_collector.rb/` | 15 | eval-20261012-061356-ace57ce5 | DONE / SOURCE_DEPENDENCY_GAP | 已读（2 件截断） |

**合计件数**：15 × 23 = **345** 件（各项结构一致，见上方更正 1）。

## 逐项文件清单与读取状态

状态口径：`read` 正文已读；`read(截断)` 读到但因单行超 2000 字符被工具截断；`missing` 预期件不在（该项目的实测目录）；`未回传` 仅在 `closure.json` 摘要中出现、目录内无此文件。所有路径省略前缀 `../../../<direction>/<case>/output/batch/`。

### D2-278 `ruby-to-c/D2-278-ruby-open3.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（31 行）
- `01-frozen/classification-1.json` — read（68 行）
- `01-frozen/classifier-input-1.json` — read（1 行）
- `result.md` — read（34 行）
- `04-evaluation/job-00-source-buildability/job-id.txt` — read
- `04-evaluation/job-00-source-buildability/metadata.json` — read（10 行）
- `04-evaluation/job-00-source-buildability/input_profile.json` — read（22 行）
- `04-evaluation/job-00-source-buildability/this-task-classification.json` — read（66 行）
- `04-evaluation/job-00-source-buildability/batch-authorization.json` — read（26 行）
- `04-evaluation/job-00-source-buildability/source_preflight_manifest.json` — read（16 行）
- `04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.md` — read（23 行）
- `04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json` — read（1 行）
- `04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json` — read(截断)
- `04-evaluation/job-00-source-buildability/returned-evidence/closure.json` — read(截断)
- `04-evaluation/job-00-source-buildability/returned-evidence/controller.log` — read（2 行）
- 未回传件（仅 closure 摘要）：`evidence/source-call.json`、`evidence/source-identity.json`、`evidence/source-request.json`、`evidence/source-response.body`、`request.json`、`lifecycle.jsonl`、`staging-manifest.json`

### D2-279 `ruby-to-cpp/D2-279-ruby-delegate.rb/`（15 件，同名 15 件）

- `01-frozen/frozen-inputs.md` — read（27 行）
- `01-frozen/classification-1.json` — read（61 行）
- `01-frozen/classifier-input-1.json` — read
- `result.md` — read（34 行）
- `04-evaluation/job-00-source-buildability/{job-id.txt, metadata.json, input_profile.json, this-task-classification.json, batch-authorization.json, source_preflight_manifest.json}` — read
- `04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.md` — read（23 行）
- `04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json` — read
- `…/returned-evidence/evidence-source.json` — read(截断)
- `…/returned-evidence/closure.json` — read(截断)
- `…/returned-evidence/controller.log` — read（2 行）
- 未回传件同 D2-278（各项相同，以下不再重复）

### D2-280 `ruby-to-cpp/D2-280-ruby-erb.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（31 行）
- `01-frozen/classification-1.json` — read（68 行）
- `01-frozen/classifier-input-1.json` — read
- `result.md` — read（34 行）
- `04-evaluation/job-00-source-buildability/*`（6 件）— read
- `…/returned-evidence/{evaluation_report.md, evaluation_report.json}` — read
- `…/returned-evidence/evidence-source.json` — read(截断)
- `…/returned-evidence/closure.json` — read(截断)
- `…/returned-evidence/controller.log` — read

### D2-281 `ruby-to-cpp/D2-281-ruby-ostruct.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（27 行）
- `01-frozen/classification-1.json` — read（reader 回填）
- `01-frozen/classifier-input-1.json` — read（reader 回填）
- `result.md` — read（34 行）
- `04-evaluation/job-00-source-buildability/*`（6 件）— read
- `…/returned-evidence/{evaluation_report.md, evaluation_report.json}` — read
- `…/returned-evidence/evidence-source.json` — read(截断)
- `…/returned-evidence/closure.json` — read(截断)
- `…/returned-evidence/controller.log` — read

### D2-282 `ruby-to-cpp/D2-282-ruby-tsort.rb/`（15 件）

- 同上 15 件结构；`01-frozen/frozen-inputs.md` read（27 行）、`result.md` read（34 行）；`classification-1.json` / `classifier-input-1.json` reader 回填；`evaluation_report.*` read；`evidence-source.json` / `closure.json` read(截断)；`controller.log` read。

### D2-283 `ruby-to-csharp/D2-283-ruby-forwardable.rb/`（15 件）

- `01-frozen/{frozen-inputs.md, classification-1.json, classifier-input-1.json}` — read
- `result.md` — read（34 行）
- `04-evaluation/job-00-source-buildability/*`（6 件）— read
- `…/returned-evidence/{evaluation_report.md, evaluation_report.json, controller.log}` — read
- `…/returned-evidence/evidence-source.json` — read(截断)
- `…/returned-evidence/closure.json` — read(截断)

### D2-284 `ruby-to-csharp/D2-284-ruby-tempfile.rb/`（15 件）

- `01-frozen/{frozen-inputs.md, classification-1.json, classifier-input-1.json}` — read（classification 77 行，本人直读）
- `result.md` — read（34 行）
- `04-evaluation/job-00-source-buildability/*`（6 件）— read
- `…/returned-evidence/{evaluation_report.md, evaluation_report.json, controller.log}` — read
- `…/returned-evidence/evidence-source.json` — read(截断)
- `…/returned-evidence/closure.json` — read(截断)

### D2-285 `ruby-to-csharp/D2-285-ruby-enum_osx.rb/`（15 件）

- `01-frozen/{frozen-inputs.md, classification-1.json, classifier-input-1.json}` — read
- `result.md` — read（41 行）
- `04-evaluation/job-00-source-buildability/{job-id.txt, metadata.json, this-task-classification.json, source_preflight_manifest.json, input_profile.json, batch-authorization.json}` — read（`input_profile.json` 本人直读 22 行）
- `…/returned-evidence/{evaluation_report.md, evaluation_report.json, controller.log}` — read
- `…/returned-evidence/evidence-source.json` — read(截断)
- `…/returned-evidence/closure.json` — read(截断)

### D2-286 `ruby-to-csharp/D2-286-ruby-shellwords.rb/`（15 件）

- 同 D2-283 结构；`frozen-inputs.md` / `classification-1.json` / `classifier-input-1.json` read（reader 回填其中部分）；`result.md` read（34 行）；job 6 件 read；`evaluation_report.md`/`.json`/`controller.log` read；`evidence-source.json` / `closure.json` read(截断)。

### D2-287 `ruby-to-go/D2-287-ruby-psexec.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（reader 回填）
- `01-frozen/classification-2.json` — read（103 行，本人直读）
- `01-frozen/classifier-input-2.json` — read（reader 回填）
- `result.md` — read（42 行）
- `04-evaluation/job-00-source-buildability/*`（6 件）— read
- `…/returned-evidence/{evaluation_report.md, evaluation_report.json, controller.log}` — read
- `…/returned-evidence/evidence-source.json` — read(截断)
- `…/returned-evidence/closure.json` — read(截断)
- 版本关联：`01-frozen` 只有 `-2` 件（无 `-1`）；`result.md` 自述首轮 `BLOCKED`/`public_network_unverified` 后重分类。

### D2-288 `ruby-to-go/D2-288-ruby-enum_services.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（reader 回填）
- `01-frozen/classification-1.json` — read（73 行，本人直读）
- `01-frozen/classifier-input-1.json` — read（reader 回填）
- `result.md` — read（41 行）
- job 6 件 + `evaluation_report.md`/`.json`/`controller.log` — read
- `evidence-source.json` — read(截断)；`closure.json` — read(截断)
- 版本关联：**只有 `-1` 件**，与 `../reconciliation-6.md` §5“D2-264~294 已重分类、-1 已删除”**冲突**（见 findings F5）。

### D2-289 `ruby-to-go/D2-289-ruby-enum_shares.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（reader 回填）
- `01-frozen/classification-1.json` — read（73 行，本人直读）
- `01-frozen/classifier-input-1.json` — read（reader 回填）
- `result.md` — read（41 行）
- job 6 件 + `evaluation_report.md`/`.json`/`controller.log` — read
- `evidence-source.json` — read(截断)；`closure.json` — read(截断)

### D2-290 `ruby-to-go/D2-290-ruby-chrome_cookies.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（reader 回填）
- `01-frozen/classification-1.json` — read（80 行，本人直读）
- `01-frozen/classifier-input-1.json` — read（reader 回填）
- `result.md` — read（41 行）
- job 6 件 + `evaluation_report.md`/`.json`/`controller.log` — read
- `evidence-source.json` — read(截断)；`closure.json` — read(截断)

### D2-291 `ruby-to-go/D2-291-ruby-observer.rb/`（15 件）

- `01-frozen/{frozen-inputs.md, classifier-input-1.json}` — read（reader 回填）
- `01-frozen/classification-1.json` — read（61 行，本人直读；`LOW_SIGNAL`，全信号为空）
- `result.md` — read（reader 回填）
- job 6 件 + `evaluation_report.md`/`.json`/`controller.log` — read
- `evidence-source.json` — read(截断)；`closure.json` — read(截断)

### D2-292 `ruby-to-powershell/D2-292-ruby-cve_2021_40449.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（reader 回填）
- `01-frozen/classification-2.json` — read（138 行，本人直读）
- `01-frozen/classifier-input-2.json` — read（reader 回填）
- `result.md` — read（reader 回填）
- job 6 件 + `evaluation_report.md`/`.json`/`controller.log` — read
- `evidence-source.json` — read(截断)；`closure.json` — read(截断)
- 版本关联：只有 `-2` 件；`requiresNetworkIsolation=true`，`network_targets` 5 个外部主机名（`securelist.com` L58、`mp.weixin.qq.com` L59、`github.com` L60/L61、`www.qualys.com` L88），全部 `redirectVerified=false`。

### D2-293 `ruby-to-powershell/D2-293-ruby-process_herpaderping.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（reader 回填）
- `01-frozen/classification-2.json` — read（100 行，本人直读）
- `01-frozen/classifier-input-2.json` — read（reader 回填）
- `result.md` — read（reader 回填）
- job 6 件 + `evaluation_report.md`/`.json`/`controller.log` — read
- `evidence-source.json` — read(截断)；`closure.json` — read(截断)
- 版本关联：只有 `-2` 件；`requiresNetworkIsolation=true`，`network_targets`：`jxy-s.github.io` L25/L51、`github.com` L43/L52，全部 `redirectVerified=false`。

### D2-294 `ruby-to-powershell/D2-294-ruby-docker_creds.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（reader 回填）
- `01-frozen/classification-1.json` — read（73 行，本人直读）
- `01-frozen/classifier-input-1.json` — read（reader 回填）
- `result.md` — read（reader 回填）
- job 6 件 + `evaluation_report.md`/`.json`/`controller.log` — read
- `evidence-source.json` — read(截断)；`closure.json` — read(截断)
- 版本关联：**只有 `-1` 件**（与 `reconciliation-6` §5 的概括冲突，见 F5）；`framework` 63/64/65/138、`sensitive` 124。

### D2-295 `ruby-to-powershell/D2-295-ruby-abbrev.rb/`（15 件）

- 15 件结构同 D2-296；读取状态见 cases-03（reader 回填）。`evaluation_report.json` 已由本人直读：jobId `eval-20261012-060708-c93e8a19`、build `completed/0`、execution `completed`、cleanup passed。

### D2-296 `ruby-to-powershell/D2-296-ruby-singleton.rb/`（15 件）

- `01-frozen/{frozen-inputs.md, classification-1.json, classifier-input-1.json}` — read（reader 回填）
- `result.md` — read（reader 回填）
- job 6 件 + `evaluation_report.md`/`.json`/`controller.log` — read
- `evidence-source.json` — read(截断)；`closure.json` — read(截断)
- `evaluation_report.json`（本人直读）：jobId `eval-20261012-060825-115f4738`、build `completed/0`、execution `completed`、cleanup passed。

### D2-297 `ruby-to-python/D2-297-ruby-base64.rb/`（15 件）

- 结构同 D2-296；reader 回填。`evaluation_report.json`（本人直读）：jobId `eval-20261012-060948-53dbabf8`、build `completed/0`、execution `completed`、cleanup passed。

### D2-298 `ruby-to-python/D2-298-ruby-enum_av.rb/`（15 件）

- 结构同 D2-296；reader 回填。`evaluation_report.json`（本人直读）：jobId `eval-20261012-061116-b7a4aa6d`、build `completed/0`、execution `completed`、cleanup passed。

### D2-299 `ruby-to-python/D2-299-ruby-windows_defender_exe.rb/`（15 件）

- 结构同 D2-296；reader 回填。`evaluation_report.json`（本人直读）：jobId `eval-20261012-061237-36d33e6a`、build `completed/0`、execution `completed`、cleanup passed。

### D2-300 `ruby-to-python/D2-300-ruby-credential_collector.rb/`（15 件）

- `01-frozen/frozen-inputs.md` — read（30 行）
- `01-frozen/classification-1.json` — read（69 行）
- `01-frozen/classifier-input-1.json` — read（reader 回填）
- `result.md` — read（42 行）
- `04-evaluation/job-00-source-buildability/*`（6 件）— read（metadata.json 直读）
- `…/returned-evidence/{evaluation_report.md, evaluation_report.json}` — read
- `…/returned-evidence/evidence-source.json` — read(截断)（**已读到 execution.exitCode=1 与 stderr**）
- `…/returned-evidence/closure.json` — read(截断)
- `…/returned-evidence/controller.log` — read

## 检查点

- **检查点 0（初建）**：23 项目录与完整文件清单已定位并登记；D2-278…D2-300 的 jobId / 关键终态 / 件数已入表。
- **检查点 1（本人直读复核）**：本人直读 D2-278/279/280/283/284/285/287/288/289/290/291/300 的冻结/分类/result 关键件，并对 D2-279…291、295、297…300 的 `evaluation_report.json` 精简字段做定向原行读取；直读 D2-292/293/294/298 的分类件与 D2-297/298/300 的 result.md。发现 F1–F11 见 [findings](harness-e-findings.md)。
- **检查点 20**：截至第 20 项（D2-297）时，21 项已由本人或受命只读读者逐件读取；D2-298/299/300 在随后一组读者报告中完成。**无 `unread` 项**。
- **完成（本检查点）**：23 项 × 15 件 = **345 件全部以 `read` 打开并登记状态**；其中 23×2 = **46 件为 `read(截断)`**（每项的 `evidence-source.json` 与 `closure.json` 单行超 2000 字符）；**0 件 0 字节；0 件缺失**（D2-285 的初判缺件已撤销，见更正 1）。本文件转 **COMPLETE**。
- **不构成完成的部分**（如实保留）：① 46 件的截断尾部；② `closure.json` 摘要列出但目录内不存在的未回传件；③ D2-286/287/290/291/294 五项的 report 占位（报告未取回）；④ `items/`、`events.jsonl` 等旧状态原始证据按任务约束未核。以上均**不**因本文件 COMPLETE 而被视为已读或已验。

## 增补读取检查点（2026-10-12 续接；原“完成”检查点已作废）

> 上面“检查点/未读集合”两节记的是**单行上限 2000 字符时期**的状态，**不再代表当前完成度**；其“46 件截断”与“items 未核”两项均已进入本轮补读。

### A. 单行原件补读（`evidence-source.json` / `closure.json` 共 46 件）

- 上限已提高至 1048576，本人已**逐件真实补读**下列文件（每件独立 read 回执，非 grep 存在性）：
  1. `ruby-to-c/D2-278-ruby-open3.rb/…/returned-evidence/closure.json` → **FULL**
  2. `ruby-to-python/D2-300-ruby-credential_collector.rb/…/returned-evidence/evidence-source.json` → **FULL**
  3. `ruby-to-go/D2-290-ruby-chrome_cookies.rb/…/evidence-source.json` → **FULL**
  4. `ruby-to-go/D2-290-ruby-chrome_cookies.rb/…/closure.json` → **FULL**
  5. `ruby-to-go/D2-291-ruby-observer.rb/…/evidence-source.json` → **FULL**
  6. `ruby-to-go/D2-291-ruby-observer.rb/…/closure.json` → **FULL**
  7. `ruby-to-go/D2-288-ruby-enum_services.rb/…/closure.json` → **FULL**
- 由只读子会话分担的 39 件（D2-278/evidence-source 及 D2-279…D2-300 其余）→ 状态见 [增补读取记录](harness-e-supplement-reread.md) §1；**回收回执后逐件登记 FULL/TRUNCATED**，未回收者不得计已读。
- **真实排除的一项**：`ruby-to-go/D2-289-ruby-enum_shares.rb/…/returned-evidence/closure.json` 的首次读取返回 `not found`，原因是**我漏写了 `returned-evidence/` 一层**；正确路径为 `…/job-00-source-buildability/returned-evidence/closure.json`（已由子会话补读）。此处如实记录为**路径笔误**，不是缺件。

### B. `items/` 原件（原任务要求核，本轮补做）

- 已核实存在：`batch/items/D2-278.json` … `batch/items/D2-300.json`（每项一件，`kind=codeconvert-batch-item` 风格的 pretty JSON，约 52–53 行）。
- 本人直读：`D2-278.json`、`D2-291.json`、`D2-300.json` 全文。三者与既有结论一致，并**新增可交叉字段**：`phase`（`CLOSED_PREPARATION_GAP` / `CLOSED_SOURCE_DEPENDENCY_GAP`）、`evaluation=null`、`codeRevisions=0`、`selfRepairRounds=0`、`usage={requests:0,modelCalls:0}`、`blockingReasons`、`verdicts.{sourceBuild,targetBuild,execution,comparison,environment,safety}`、`coverageGaps[]`。
- 其余 20 件由只读子会话逐件读取回执后登记（不写“同结构”代枚举）。
- **`items/` 与本审阅范围的边界**：只读 `D2-278…300` 共 23 件；**未**读 `events.jsonl`，**未**读其它组用例目录。

### C. 本轮口径修正（验收指出的三处）

1. **原文数字矛盾**：原 [增补记录](harness-e-supplement-reread.md) §3 写“34 件”、§4 写“38 件”，我为计数前后不一致道歉并作废该二数。**唯一以 read 回执为准**：46 件需补读，已补 **7 件（本人）** ＋ 子会话回执若干，剩余以回收结果逐件登记。
2. **D2-300 `closure.json` 已读/未读并存**：该件**尚未补读**（本人只补读了其 `evidence-source.json`），原表中把它混入“已读”的写法作废。
3. **两个不能外推的推断**：`collectorDiagnostics=[]` **只支持“未记录诊断”**，**不能**证明采集器没有失败；`observations.output.events=[]` **不等于 stdout 无内容**——真实 stdout 内容须看 `execution.stdout.normalizedText` 与 `sizeBytes`（D2-278/291/300 等已核为 `""`/0）。`closure.json` 摘要只证明**平台记录过制品摘要**，**不证明远端正文仍存在**，也**不能恢复报告内容**。

