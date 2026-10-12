# Harness C 逐项审阅记录 04（D2-221 .. D2-240）

> 状态：**COMPLETE**（本组 8 个存在项 222、232、233、235、236、238、239、240 均已逐项记录；另 12 个缺号见 coverage §2）。
> 引用基准：`docs/dataset-2/dataset-2-copy/`。文件清单纯文件名见 [harness-c-coverage.md](harness-c-coverage.md) §4。
> 硬约束：只读静态审阅；未编译/运行/调用模型/改动原始证据。源与目标代码已删除。
> 读取限制：第一轮单行 >2000 字符截断的部分，已在验收补读轮（上限 1048576）用原生 read 读到全文，见 coverage §5。

## 编号位（221-240，共 20 位）

- 存在 8 项：D2-222（csharp-to-go）、D2-232/233（powershell-to-ruby）、D2-235/236/238/239/240（python-to-c）。
- 缺号 12 个：D2-221、223、224、225、226、227、228、229、230、231、234、237（见 coverage §2）。

## D2-222 — csharp-to-go / AlwaysInstallElevated.cs（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `AlwaysInstallElevated.cs, 31, FEFF…CFEB`。item `SOURCE_DEPENDENCY_GAP`/`CLOSED_SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-031507-036dd624`（`/api/source-preflights`、linux、`build-only`、`failed/1`）。classifier v2.4 `ALLOWED`；`agentAddedCsproj{path:source/program.csproj, originalState:"no .csproj existed", stillMissingSymbols:"SharpUp.Classes.VulnerabilityCheck, SharpUp.Utilities.RegistryUtils"}`。
- **文件清单与读取**：15 件全部 ✅已读。`01-frozen/` 3；`job-00-source-buildability/`（6 配置＋`source_preflight_manifest.json`＋`returned-evidence/{evidence-source.json, controller.log, closure.json, evaluation_report.json, evaluation_report.md}`）；`result.md`。`evidence-source.json`、`closure.json` ⚠️截断。
- **版本关联**：源 sha `feff0325…cfeb`；job `eval-20261012-031507-036dd624`；快照 `CC-Eval-Linux-8Lang-1.0.29`；runner `linux-vm-agent-x64`；**实测 .NET SDK 10.0.112**（`net8.0` TFM 仍可构建）。
- **证据事实**：`evaluation_report.json`（完整）`kind=codeconvert-source-preflight-report`、`buildAssessment=failed`、`executionAssessment=not-requested`、`baselineAssessment=NOT_APPLICABLE ["sample-execution-not-requested"]`、`cleanup=passed`、`failure=null`。编译器诊断**输出在 stdout**（非 stderr）：`AlwaysInstallElevated.cs(1,15): error CS0234: 'Classes' does not exist in namespace 'SharpUp'` / `(6,22) 'Utilities'` / `(10,42) CS0246 'VulnerabilityCheck'`。
- **自审**：空集（未生成）。**失败/重提**：无。
- **归因**：源已有（SharpUp 多文件工程，快照只含单文件 ⇒ 缺同项目类型）；`program.csproj`＝Agent 按 §13 补的最小中性构建外壳（未引入源中不存在的包）。
- **知识候选/流程**：C# 源侧 runner 无 `csc` ⇒ 必须补最小中性 `.csproj`；补入后**源文件集合变化须重新分类**；`dotnet build` **诊断可能在 stdout**，判读须两侧都读。

## D2-232 — powershell-to-ruby / build_run.ps1（PREPARATION_GAP / ORACLE_NOT_FREEZABLE）

- **身份**：manifest `build_run.ps1, 53, EB16…0450`。item `PREPARATION_GAP`/`DONE`、`blockingReasons=[PREPARATION_GAP, ORACLE_NOT_FREEZABLE]`、`requests=0`。classifier v2.4 `ALLOWED`/`REVIEW_SIDE_EFFECTS`。
- **文件清单与读取**：28 件全部 ✅已读（含首轮 6 件超长单行 JSON 已补读全文）。`01-frozen/` 5 件（含 `classification-2.json`/`classifier-input-2.json`）；`job-00-source-buildability` 11 件；`job-00b-source-buildability` 11 件；`result.md`。**✖缺** `source/**`、`02-conversion/`、`03-self-review/`、`evaluator_manifest.json`。
- **版本关联**：源 sha 一致；job-00 `eval-20261012-031718-de6efa94`（失败）、job-00b `eval-20261012-031849-e7e2fd79`（现行＝item `sourcePrecheck.jobId`）；`contractHash 8090cfcc…`。
- **证据事实**：**job-00 失败 attempt**：`runCommand=["python","run_case.py"]`，exec `exitCode=97`、stdout 空、stderr `"DRIVER-FAILURE: no runnable target found"`（42 B）——驱动不识别源脚本名。**job-00b**：`runCommand=["pwsh","-NoProfile","-File","build_run.ps1"]`、timeout 120；exec `completed/0 (2589 ms)`，stdout **1614 B**（14 行 `Built: C:\...\workspaces\eval-20261012-031849-e7e2fd79\source\bin\NN_*.exe` + `Build finished.`）、stderr **2591 B**（14 条 `cc1plus.exe: fatal error: ...\<case>\main.cpp: No such file or directory`）；`closure.oracleStatus=UNVERIFIED`、`programOutputProvenance=UNVERIFIED`。
- **自审**：空集（0 模型调用）。**失败/重提**：job-00（装置）→修装置并**重新分类**（去驱动 ⇒ 源树变化）→ job-00b。
- **错误建议/未定（★）**：① **job-00 报告把驱动故障写成 `executionAssessment=completed`/`failure=null`**，与 `evidence-source.exitCode=97`+DRIVER-FAILURE 矛盾；② `frozen-inputs.md` 评估计划仍是 python 驱动/timeout 60，与 job-00b `pwsh` 直启/timeout 120 不符且**无重冻结记录**；③ `classifier-input*.json` 只列 1 件而 `classification-1.json`/job-00 分类件列 2 件（含 `run_case.py`），两版 `inputManifestSha256` 却同为 `fc767c9b…`；④ `batch-authorization.confirmation` 残留 D2-197 文案；⑤ `closure.artifactDigests` 列出的 `request.json`/`lifecycle.jsonl`/`staging-manifest.json`/`evidence/source-*.json` **未回传**；⑥ manifest `Lines 53` vs frozen/result `60`；`JobId` 空、`Evidence` 未更新。
- **归因**：驱动 DRIVER-FAILURE 与 job 绝对路径＝装置；14 个 `main.cpp` 缺失＝源侧快照残缺；转换引入＝**0**。

## D2-233 — powershell-to-ruby / build_run_advanced.ps1（PREPARATION_GAP / ORACLE_NOT_FREEZABLE）

- **身份**：manifest `build_run_advanced.ps1, 57, B8ED…CFE1`。item `PREPARATION_GAP`/`DONE`、`blockingReasons=[PREPARATION_GAP, ORACLE_NOT_FREEZABLE]`、`requests=0`。
- **文件清单与读取**：15 件全部 ✅已读、**无截断**。`01-frozen/` 3 件；`job-00-source-buildability` 11 件；`result.md`。✖缺 `source/**`、`02-conversion/`、`03-self-review/`、`evaluator_manifest.json`。
- **版本关联**：job `eval-20261012-032851-72110e15`（四方一致）；`contractHash 8090cfcc…`；`inputProfileHash 09c7e38a…`。
- **证据事实**：build `completed/0`；exec `completed/0 (629 ms)`、`timedOut=false`；stdout **1819 B**（14 行 `Skip (missing): C:\...\workspaces\eval-20261012-032851-72110e15\source\<case>\advanced.cpp` + `Advanced build finished.`）、**stderr 空**（脚本 `Test-Path` 守卫，避免 g++ 调用）；`closure.oracleStatus/programOutputProvenance=UNVERIFIED`；`baselineAssessment=UNVERIFIED`。
- **自审**：空集。**失败/重提**：无（一次到位，沿用 D2-232 教训不用 python 驱动）。
- **错误建议/未定**：① `metadata.json` `safetyClassification` 写 `cls=(see classification-1)`（**值缺失**）；② manifest `Lines 57` vs frozen/result `65`；③ `result.md` 写目标“Ruby（CRuby 3.4）”但**目标从未生成**，属计划值；④ closure 引用件未回传；⑤ `batch-authorization` 残留 D2-197 文案。
- **知识候选**：同为构建编排脚本，`Test-Path` 守卫使缺失兄弟件成 stdout 行、stderr 空（D2-233），无守卫则成编译器致命错误（D2-232）——**两者 stderr 面相反，不得互相类推**。
- **归因**：job 绝对路径＝装置；兄弟件缺失＝源侧快照残缺；转换引入＝**0**。

## D2-235 — python-to-c / psexec.py（SOURCE_DEPENDENCY_GAP；含重分类链）

- **身份**：manifest `psexec.py, 582, 396A…6279`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`。classifier v2.4 `REVIEW_NETWORK`→重分类 `ALLOWED`。
- **文件清单与读取**：15 件全部 ✅已读（`closure.json`/`evidence-source.json` 已补读全文）。`01-frozen/{frozen-inputs.md, classification-2.json, classifier-input-2.json}`；`job-00-source-buildability` 6 配置＋5 evidence；`result.md`。✖缺 `source/psexec.py`（已删）、`02/03`、`evaluator_manifest.json`。
- **版本关联**：job `eval-20261012-033113-40e1bdcf`（五处一致）；`contractHash` 跨 5 项同 digest `8026a8a7…`。
- **证据事实**：build `completed/0`（`py_compile`）；exec `completed/1`，stderr `ModuleNotFoundError: No module named 'impacket'`（`psexec.py:34`，240 B）；`baselineAssessment UNVERIFIED`、`oracleStatus/programOutputProvenance UNVERIFIED`。
- **自审**：空集。**失败/重提**：无。
- **重分类链**：events L920 `CLASSIFY BLOCKED/public_network_unverified` → L921 `RECLASSIFY --network-isolation-configured => classification-2; 误生成的 classification-1.json removed`；`classification-2.network_targets` 仍列 `docs.python.org` L321/420/608（`literal`/`redirectVerified:false`，实为日志/help 字面量）。
- **归因**：`ModuleNotFoundError`＝源已有外部依赖＋环境；首轮 BLOCKED＝分类器词法误判。

## D2-236 — python-to-c / pwncat.py（PREPARATION_GAP；去向口径待裁）

- **身份**：manifest `pwncat.py, 5640, 1352…B9C2`。item `PREPARATION_GAP`/`DONE`、`requests=0`、`requiresNetworkIsolation=true`。classifier `REVIEW_SENSITIVE`→重分类 `ALLOWED`。
- **文件清单与读取**：15 件全部 ✅已读（两件长单行补读全文）。`01-frozen/{frozen-inputs.md, classification-2.json(503 行), classifier-input-2.json}`；`job-00` 6 配置＋5 evidence；`result.md`（60 行）。✖缺 `source/pwncat.py`、`02/03`、`evaluator_manifest.json`。
- **版本关联**：job `eval-20261012-033314-bdd0431f`（五处一致）；events L925 记 `classification-1.json removed`，磁盘仅存 classification-2。
- **证据事实**：build `completed/0`（`py_compile`）；exec `completed/2`、stderr 348 B（argparse 六行 usage + `pwncat.py: error: the following arguments are required: port`，digest `31e1b11b…`）；`closure.oracleStatus/programOutputProvenance=UNVERIFIED`。`result.md` 定位入口链：`__main__`(L6363)→`main()`(L6061)→`get_args()`(L6064)→`parser.parse_args()`(**L6018**) ⇒ argv=[] 在 L6018 即退出 2，**从未进入 `main()`**，usage 文本不构成合法观察面。events L951 `CORRECTION` 取代 L926 的 “baseline valid and freezable”。
- **自审**：空集。**失败/重提**：无；1 条记录更正（非重跑）。
- **未定（★ 去向口径）**：`result.md` 记 `PREPARATION_GAP`、生成前停止、0 模型调用；而 `AGENTS.md` §3 规定“源可构建但本轮行为无法合法评估”应按 `LIB_UNOBSERVABLE_COMPILE_ONLY` **继续生成并只验目标语法/编译**。本项有 `main`、build `completed/0`，却因 argv=[] 退化且无合法来源驱动而停生成。两种口径是否互斥、本项应归 `PREPARATION_GAP` 还是 `LIB_UNOBSERVABLE_COMPILE_ONLY`，**需按契约原文裁定**，直接影响“是否应生成目标”与批次计数。
- **归因**：argparse usage/exit 2＝源行为正确；停生成＝装置/流程（缺合法驱动）；转换引入＝**0**。

## D2-238 — python-to-c / getST.py（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `getST.py, 770, D1BA…DFFE`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`。classifier `REVIEW_SENSITIVE`（`network_signals []`、`network_mode none-detected`）。
- **文件清单与读取**：15 件全部 ✅已读。`01-frozen/` 3；`job-00` 6 配置＋5 evidence；`result.md`。✖缺 `source/getST.py`、`02/03`、`evaluator_manifest.json`。
- **版本关联**：job `eval-20261012-033515-2281f648`（五处一致）；`inputManifestSha256 a48701bd…`。
- **证据事实**：build `completed/0`（`py_compile`）；exec `completed/1`，stderr `ModuleNotFoundError: No module named 'impacket'`（`getST.py:66`，231 B，digest `2810b845…`）；`baselineAssessment UNVERIFIED`。
- **自审**：空集。**归因**：源已有依赖＋环境。

## D2-239 — python-to-c / ticketer.py（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `ticketer.py, 1007, 6AC9…1B2B`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`。classifier `REVIEW_NETWORK`（`network [1065]`、`network_targets []`）。
- **文件清单与读取**：15 件全部 ✅已读。`01-frozen/` 3；`job-00` 6 配置＋5 evidence；`result.md`。✖缺 `source/ticketer.py`、`02/03`、`evaluator_manifest.json`。
- **版本关联**：job `eval-20261012-033645-b7d2aa3a`（五处一致）；`inputManifestSha256 5fcabb3d…`。
- **证据事实**：build `completed/0`；exec `completed/1`，stderr `ModuleNotFoundError: No module named 'impacket'`（`ticketer.py:63`，234 B，digest `f8fc3890…`）。
- **自审**：空集。**归因**：源已有依赖＋环境。

## D2-240 — python-to-c / reg.py（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `reg.py, 609, 0C5B…D593`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`。classifier `REVIEW_SENSITIVE`（`network [76,77,…]`、`network_targets 192.168.0.2 L624/628 (private)`、`requiresNetworkIsolation true`）。
- **文件清单与读取**：15 件全部 ✅已读。`01-frozen/{frozen-inputs.md(9 行), classification-1.json(97 行), classifier-input.json}`；`job-00` 6 配置＋5 evidence；`result.md`。✖缺 `source/reg.py`、`02/03`、`evaluator_manifest.json`。
- **版本关联**：job `eval-20261012-033814-374dc7f2`（五处一致）；`inputManifestSha256 69d8c256…`。
- **证据事实**：build `completed/0`；exec `completed/1`，stderr `ModuleNotFoundError: No module named 'impacket'`（`reg.py:39`，229 B，digest `5254495e…`）。
- **自审**：空集。**归因**：源已有依赖＋环境；`192.168.0.2` 为 private 字面量，`admissionStatus ALLOWED`。

### 组末说明（D2-221..240）

- 本组 20 个编号位：存在 8 项（222、232、233、235、236、238、239、240），缺号 12 个（221、223–231、234、237）。
- 去向：`SOURCE_DEPENDENCY_GAP` 5（222/235/238/239/240）、`PREPARATION_GAP` 3（232/233/236）。**8/8 未生成目标、0 模型调用、无自审、无比较**。
- 跨项：**manifest `Lines` 与 frozen/result 行数 7/7 有数据项全部不一致**（232 53/60、233 57/65、235 582/677、236 5640/6364、238 770/918、239 1007/1189、240 609/703；222 为待核）；`batch-authorization.confirmation` 残留 D2-197 文案；`closure.artifactDigests` 引用件未回传；缺 `evaluator_manifest.json`。
- 归因：源已有依赖/快照残缺/环境（离线）/装置（驱动、消噪、报告层）；**转换引入 0**。

<!-- CASES04-ANCHOR: GROUP-COMPLETE (8 existing items; 12 missing IDs 221,223-231,234,237) -->


