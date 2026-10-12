# Harness C 逐项审阅记录 03（D2-201 .. D2-220）

> 状态：**IN_PROGRESS**（缺 D2-217，待子审阅返回后补；其余已完成）。
> 引用基准：`docs/dataset-2/dataset-2-copy/`。文件清单纯文件名见 [harness-c-coverage.md](harness-c-coverage.md) §4。
> 硬约束：只读静态审阅；未编译/运行/调用模型/改动原始证据。源与目标代码已删除。
> 读取限制：`read`/`grep` 对单行 >2000 字符 JSON 截断且不可分页（本组大量 `evidence-source.json`/`closure.json`/`self-review*.json` 属此类），记 ⚠️截断。

---

## D2-201 — go-to-powershell / UuidFromString.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `UuidFromString.go, 163, 3EF7…C48A`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-024527-c7e6b462`（windows，`build-only`，`failed/1`）。classifier `LOW_SIGNAL`（**signals 七类全空**）。
- **文件清单与读取**：15 件全部 ✅已读；`evidence-source.json`、`closure.json` ⚠️截断。
- **证据事实**：stderr 原文两条：`UuidFromString.go:31:2: no required module provides package github.com/google/uuid: go.mod file not found …` 与 `:28:2 … golang.org/x/sys/windows`（350 B，digest `b9b71d07…`）；report `buildAssessment failed`、`cleanup passed`。
- **自审**：空集。**归因**：源已有（两个外部模块未 vendor）＋环境（离线）。
- **错误建议/未定**：`metadata.json` `safetyClassification="…cls=(see classification-1)"`（`cls=` 空值）；**分类事实与静态画像不一致**——`classification-1.json` 判 `LOW_SIGNAL`、全空 signals，而 `frozen-inputs.md` 自述源码含 Win32 进程/内存 API 与 shellcode 执行链（`HeapCreate/HeapAlloc→UuidFromStringA→EnumSystemLocalesA`）。该分类未影响本项去向（被依赖缺口拦下），但同类可转换项会受影响。

## D2-202 — go-to-powershell / itoa.go（PREPARATION_GAP；冻结预判被编译器否证）

- **身份**：manifest `itoa.go, 179, 5923…85D4`。item `PREPARATION_GAP`/`DONE`、`requests=0`；job `eval-20261012-024648-18adc304`（linux，`build-only`，`completed/0`）。
- **文件清单与读取**：15 件全部 ✅已读；`evidence-source.json`、`closure.json` ⚠️截断。
- **证据事实**：build `completed/0`、574 ms；`execution unavailable`；report `buildAssessment=passed`、`cleanup passed`；`evaluation_report.md` `source: build=passed; execution=unavailable.`。manifest 179 行＝frozen/result 179（一致）。
- **自审**：空集。
- **规则事实（★）**：`frozen-inputs.md` L15/L18–20 **预判**「`small/nSmalls/formatBits` 不在本文件内 ⇒ `SOURCE_DEPENDENCY_GAP`」，实测 `completed/0`；`result.md` §3 逐字纠正「四个符号均在 `itoa.go` 本文件内定义（`small` L59、`nSmalls` L66、`smallsString` L68、`formatBits` L88）⇒ 源自包含。判决以编译器诊断为准」。⇒ 单读冻结件会得到**错事实**，冻结件按规则保留原样（正确）。
- **归因**：源已有（非 main 库包无入口）；冻结静态画像误判=流程（已由编译器纠正并留痕）。

## D2-203 — go-to-powershell / reader.go（PREPARATION_GAP）

- **身份**：manifest `reader.go, 145, B217…65FA9`。item `PREPARATION_GAP`/`DONE`、`requests=0`；job `eval-20261012-024821-9faefecb`（linux，`build-only`，`completed/0`）。
- **文件清单与读取**：15 件全部 ✅已读；`evidence-source.json`、`closure.json` ⚠️截断。
- **证据事实**：build `completed/0`、4394 ms；`execution unavailable`；`buildAssessment passed`；`source: build=passed; execution=unavailable.`
- **自审**：空集。
- **规则事实**：`frozen-inputs.md` 采用**主预判＋备选**并显式引用前项教训（L21 原文「（D2-202 教训：冻结预判不代替证据。）」）：主预判 `PREPARATION_GAP`、备选 `SOURCE_DEPENDENCY_GAP`；实测落主预判，`result.md` 记“无需改记”。
- **归因**：源已有（非 main 库包无入口）；`metadata.json` `cls=` 空值=装置。
- **未定**：manifest 145 行 vs frozen/result 160 行。

## D2-204 — go-to-python / CreateRemoteThread.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `CreateRemoteThread.go, 103, 43E1…45B2`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-024959-8277857c`（windows，`build-only`，`failed/1`）。classifier v2.4 `REVIEW_SENSITIVE`。
- **文件清单与读取**：15 件全部 ✅已读；`closure.json`、`evidence-source.json` ⚠️截断。
- **证据事实**：stderr 原文 `CreateRemoteThread.go:25:2: no required module provides package golang.org/x/sys/windows: go.mod file not found …`（180 B）；stdout 空；execution `blocked`；report `buildAssessment failed`、`cleanup passed`；closure `complete/cleanupConfirmed/issues:[]`。
- **自审**：空集。**归因**：源已有（外部模块未 vendor）＋环境（离线）。

## D2-205 — go-to-python / CreateRemoteThreadNative.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `CreateRemoteThreadNative.go, 110, 8BEC…D6A1`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-025122-029ffba8`（windows，`failed/1`）。
- **文件清单与读取**：15 件全部 ✅已读；2 件 ⚠️截断。
- **证据事实**：stderr `CreateRemoteThreadNative.go:26:2: no required module provides package golang.org/x/sys/windows …`（186 B）；execution `blocked`。
- **自审**：空集。
- **知识候选**：源码注释自称“直接 LoadLibrary 而不用 windows 包”**不等于实际不依赖**——依赖判定必须看 `import` 与编译器诊断，不采信注释自述。
- **归因**：源已有；`casePath` 目录名大小写与磁盘不符=装置。

## D2-206 — go-to-python / EtwpCreateEtwThread.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `EtwpCreateEtwThread.go, 107, 0589…B207`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-025250-f78b0bbd`（windows，`failed/1`）。
- **文件清单与读取**：15 件全部 ✅已读；2 件 ⚠️截断。
- **证据事实**：stderr `EtwpCreateEtwThread.go:26:2: no required module provides package golang.org/x/sys/windows …`（181 B）；execution `blocked`。
- **自审**：空集。**归因**：源已有。

## D2-207 — go-to-python / ProcessInjection.go（CONVERTED / DONE；mismatched 归因存分歧）

- **身份**：manifest `ProcessInjection.go, 124, FFFF…EC31`。item `CONVERTED`/`CLOSED`/`DONE`、`codeRevisions=1`、`selfRepairRounds=1`、`requests=3`（1 生成＋1 自审＋1 修复）；平台 `behaviorVerdict=mismatched`、`platformVerdictPreserved=true`，唯一 diff=`stream.normalizedText`（major，attribution 写“language-runtime failure-trace form … NOT conversion-introduced”）；两侧 stdout 均为 `Processo Explorer.exe not found\n`（32 B）、退出码均 2。
- **文件清单与读取**：32 件全部 ✅已读。`01-frozen/` 3；`02-conversion/{target.gen.model.json, target.self-repair-1.model.json}`；`03-self-review/{self-review-1.json, self-review-1.model.json}`；`job-00`（11）；`job-01-dual-build`（13）；`result.md`。**✖缺 `evaluator_manifest.json`、`case.md`、全部 raw request/response 正文、`target.gen.raw.json`**（后件按 batch README 属应保留）。6 件 ⚠️截断。
- **版本关联**：`target.gen.py` sha `2a7f15cb…`（94 行）→ `target.self-repair-1.py` sha `491db781…`＝item `conversion.targetSha256`＝job-01 `metadata.targetHash`＝events ⇒ **自修稿即被评估稿**，一致。job-00 `eval-20261012-025454-99104a84`（build-and-run，windows），job-01 `eval-20261012-025857-578506a3`（source windows→target linux）。
- **证据事实**：源 job-00 build `completed/0`、exec `completed/2`、stdout 32 B（digest `2c4ea463…`）、stderr Go panic 栈（`source/ProcessInjection.go:72`，空 payload 取下标）。job-01 两侧 stdout digest 完全相同、退出码均 2；`comparison.json` 唯一条 `stream.normalizedText`（`rule=normalized-text`，`workspace_path_pairs=[]`）；`evaluation_report.md` `Conversion result FAIL / Behavior MISMATCHED`、`Frozen oracle assertions: UNVERIFIED / not requested`；两侧 cleanup PASSED/clean/READY。
- **自审**：`self-review-1.json` `REPAIR-RECOMMENDED` 1 条 `exit-code-panic-vs-indexerror`：源 Go panic 退出码 2，目标未捕获 `IndexError` 默认 1 ⇒ `origin=conversion-introduced`，`proposed_fix` 显式 `sys.exit(2)`，`risk` 低（stderr 栈无法逐字节复现）。已由配置模型最小修复；**新稿未发起独立复审**，仅 Agent 静态 diff 核对（`target.self-repair-1.model.json` `review_of_new_version.method="static diff inspection by Agent (not a separate model review request)"`），`result.md` §3.3 如实登记偏离。self-review model.json 记 `finish_reason=stop`、usage 1949/10417/10006。
- **失败/重提**：无失败/废弃 attempt（两 job 各 attempts=1）。
- **未定/错误建议（★）**：① `batch-authorization.json` 的 `confirmation` 仍写“该项 D2-197 (Go stdlib sort.go)”；② `casePath` 大小写与磁盘不符；③ **job-00 与 job-01 的 `input_profile.json` 比较策略不一致**：job-00 `stderrMode=exact`，job-01 `stderrMode=normalized-text` + `ignoredJsonPaths:[]`；④ `classifier-input.json` 只声明 `source/ProcessInjection.go`，而实际分类树含 `run_case.py`；⑤ 自审记录缺独立 `unresolved` 字段；⑥ 批次内审（`full-review-self-reviews-02.md:45`）对“stderr 外形可明确允许，但不能自动被当装置”提出保留意见 ⇒ **本项 stderr 归因（装置/语言运行时 vs 未冻结比较策略）存在分歧，列为未定**。
- **归因**：唯一平台 diff＝语言运行时失败痕迹形态＋各侧工作区绝对路径，属环境/装置（比较策略未预设消噪），**非转换逻辑引入**（stdout+退出码一致）；退出码 1≠2＝转换引入，已修。

## D2-208 — go-to-python / search.go（SOURCE_DEPENDENCY_GAP；行数元数据矛盾）

- **身份**：manifest `search.go, 139, 3C95…4060`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-030204-7d751ee7`（linux，`build-only`，`failed/1`）。classifier `LOW_SIGNAL`。
- **文件清单与读取**：15 件全部 ✅已读；2 件 ⚠️截断。
- **证据事实**：stderr 原文 `# command-line-arguments\n./search.go:144:9: undefined: IntSlice\n./search.go:147:9: undefined: Float64Slice\n./search.go:150:9: undefined: StringSlice\n`（149 B）；execution `blocked`。
- **自审**：空集。
- **错误建议（★）**：**manifest `Lines=139` 与 frozen/result 的“139 行”均与编译器诊断矛盾**——诊断引用 `:144/:147/:150` ⇒ 文件至少 150 行。源码已删无法复核。属数据集元数据 vs 源文件层面的不一致，不应与转换归因混算。
- **归因**：源已有（同包伴随文件不在快照）；行数矛盾=元数据/装置。

## D2-209 — go-to-ruby / gpersist.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `gpersist.go, 49, 7570…FFBB`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-030334-046013de`（windows，`build-only`，`failed/1`）。classifier v2.4 `ALLOWED`。
- **文件清单与读取**：15 件全部 ✅已读；`closure.json`、`evidence-source.json` ⚠️截断。
- **证据事实**：stderr `gpersist.go:4:2: no required module provides package golang.org/x/sys/windows/registry: go.mod file not found …`（178 B）；execution `blocked`；closure `complete/cleanupConfirmed/issues:[]`、cleanup `passed/READY/attempts 1/contaminated false`。
- **自审**：空集。**归因**：源已有（外部模块未 vendor）。

## D2-210 — csharp-to-powershell / MaliciousClickOnceMSBuild.cs（PREPARATION_GAP / ORACLE_NOT_FREEZABLE）

- **身份**：manifest `MaliciousClickOnceMSBuild.cs, 27, A32D…AD1A`。item `PREPARATION_GAP`/`DONE`、`blockingReasons=[PREPARATION_GAP, ORACLE_NOT_FREEZABLE]`、`requests=0`；`agentAddedCsproj`（源原无 `.csproj`，Agent 补 `program.csproj` sha `1408f895…`）；build-only job `eval-20261012-030557-2960dfc1`、baseline job `eval-20261012-032623-28601af7`。
- **文件清单与读取**：27 件全部 ✅已读。`01-frozen/` 5 件（含 `classification-2.json`/`classifier-input-2.json`）；两个 job 各 9 配置＋5 evidence；`result.md`。2 件 ⚠️截断。
- **证据事实**：job-00 build `passed`（`dotnet build … -o bin`，stdout 中文“已成功生成。0 个警告 0 个错误”）；job-01 build `passed`（`-o .`），execution `completed`、**exitCode 4294967295**、**stdout 0 B**、stderr 为 .NET 异常栈（尾部截断）；`baselineAssessment UNVERIFIED (independent-frozen-oracle-not-provided)`。
- **自审**：空集（未生成目标）。
- **流程缺陷（★）**：① **冻结声明的 buildCommand 与实际不一致**（frozen 写 `-o bin`，job-01 实际 `-o .`，未回写冻结记录）；② **第二次分类的输入清单未保存**——`classifier-input-2.json` 仍只有 1 条（`.cs`），而 `classification-2.json` 含 3 件（`.cs`+`program.csproj`+`run_case.py`，`inputManifestSha256=5914be27…`）；③ **ORACLE_NOT_FREEZABLE 的另一泄漏源**：job-specific workspace 路径同时出现在 `dotnet build` 的 **stdout**（不止 stderr 异常栈）。
- **归因**：`DirectoryNotFoundException` 指向 `C:\Users\zj213\AppData\Local\Apps\2.0` 不存在＝环境/观察条件；job 特定路径＝装置；`program.csproj`＝Agent 补齐的构建外壳。

## D2-211 — go-to-ruby / bypassUACgo.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `bypassUACgo.go, 87, 8B6C…659B`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-030800-5e021db8`（windows，`failed/1`）。classifier `REVIEW_SENSITIVE`。
- **文件清单与读取**：15 件全部 ✅已读；2 件 ⚠️截断。
- **证据事实**：stderr `bypassUACgo.go:10:2: no required module provides package golang.org/x/sys/windows/registry …`（182 B）；execution `blocked`；cleanup `passed`。
- **自审**：空集。
- **错误建议**：`result.md` L5 写“106 行”与 manifest `Lines=87`、`frozen-inputs.md` L8「87 行」**不一致（差 19）**。
- **归因**：源已有（外部模块未 vendor）。

## D2-212 — go-to-ruby / keylogger.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `keylogger.go, 92, 6CD9…0183`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-030924-01d03ec3`（windows，`failed/1`）。classifier `LOW_SIGNAL`（`reviewGroups:[]`）。
- **文件清单与读取**：15 件全部 ✅已读；2 件 ⚠️截断。
- **证据事实**：stderr `keylogger.go:9:2: no required module provides package github.com/TheTitanrain/w32: go.mod file not found …`（173 B）；execution `blocked`。
- **自审**：空集。
- **错误建议/知识候选**：`result.md` L5 写“115 行” vs manifest/冻结「92 行」；分类器对 Windows 键盘记录库判 `LOW_SIGNAL`、`requiresSyntheticData:false`——**词法分类器未捕捉键盘钩子语义**（`limitations` 自陈 `lexical_heuristics_not_dataflow`）。
- **归因**：源已有（第三方模块 + 非 main）。

## D2-213 — go-to-ruby / Syscall.go（SOURCE_DEPENDENCY_GAP；分类信号行号越界）

- **身份**：manifest `Syscall.go, 96, B472…0FF9`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-031047-4ea00cf9`（windows，`failed/1`）。classifier `REVIEW_SENSITIVE`。
- **文件清单与读取**：15 件全部 ✅已读；2 件 ⚠️截断。
- **证据事实**：stderr `Syscall.go:24:2: no required module provides package golang.org/x/sys/windows: go.mod file not found …`（169 B）；execution `blocked`。
- **自审**：空集。
- **错误建议（★硬证据链）**：`classification-1.json` 的 `signals.sensitive=[33,56,58,59,63,65,68,72,92,96,98,101]` —— **98、101 超出被冻结的 96 行**；manifest/冻结写 96 行、`result.md` L5 写“116 行” ⇒ 分类器实际读到比“冻结 96 行”更长的文本。三处互相矛盾且源码已删，**无法裁决**。
- **归因**：`golang.org/x/sys/windows` 缺失＝源已有；行数/版本矛盾＝证据链自身不一致（流程/装置）。

---

## D2-217 — powershell-to-cpp / install-powershell.ps1（BLOCKED / WAITING / public_network_unverified）

- **身份**：manifest `install-powershell.ps1, 444, A462…2955`。item `BLOCKED`/`CLASSIFIED`/`WAITING`、`blockingReasons=[public_network_unverified]`、`requests=0`。classifier v2.4 `cls=REVIEW_SENSITIVE`、`admissionStatus=BLOCKED`、`blockingReason=public_network_unverified`、`requiresNetworkIsolation=true`。
- **文件清单与读取**：**4 件全部 ✅已读**。`01-frozen/{classification-1.json, classifier-input.json, frozen-inputs.md}`；`output/batch/result.md`。`02/03/04` **未发生（不适用）**。
- **证据事实**：`classification-1.json`（180 行，多行 JSON，**完整可读**）登记 6 个 `network_targets`（`aka.ms` L269、`pscoretestdata.blob.core.windows.net` L301、`raw.githubusercontent.com` L346、`github.com` L369、`System.Security.SecurityException` L227、`pwsh.exe` L274，全部 `provenance=literal`、`redirectVerified=false`）；`network_mode=hostname`、`has_network/has_file_ops/has_process_exec=true`。`frozen-inputs.md` L14–17 列真实下载调用（`Invoke-RestMethod`/`Invoke-WebRequest -Uri … -OutFile`，L269/301/312/346/369/380）并明确**不适用** `--network-isolation-configured` 重分类路径（非注释误判）。`result.md` 结论：BLOCKED ⇒ 不预检、不生成、不提交、0 模型调用，未伪造 job 证据。
- **自审**：空集（未生成）。**失败/重提**：无（未进入预检）。
- **错误建议/未定**：`result.md` 写源「507 行」与 manifest `Lines=444` **不一致**（C-F-14 家族）；`result.md` 末尾「继续 D2-222（manifest 跳过 D2-218~D2-221 或按实际清单核实）」表述含糊，实际 manifest 缺号含 214–216/218–221/223–231/234/237（coverage §2）。
- **归因**：硬编码公网目标＋真实下载调用＝**源已有**；按安全边界 BLOCKED 属**门禁正确执行**；无装置/转换引入。



## 组末说明（D2-201..220 缺号与进度）

- 本组编号位 201-220 共 20 位：存在 14 项（201-213＋217），缺号 6 个（D2-214、215、216、218、219、220，见 coverage §2）。
- 已完成 14 项（201-213＋217）：去向＝`SOURCE_DEPENDENCY_GAP` 9（201/204/205/206/208/209/211/212/213）、`PREPARATION_GAP` 3（202/203/210）、`CONVERTED` 1（207）、`BLOCKED/WAITING` 1（217）。本组 14/14 完成。
- 归因：转换引入仅 207（退出码 1≠2，已修）；其余为源已有/环境/装置。

<!-- CASES03-ANCHOR: GROUP-COMPLETE (14 existing items; 6 missing IDs 214-216,218-220) -->
