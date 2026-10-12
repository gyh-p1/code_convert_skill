# Harness C 审阅发现（D2-161 .. D2-240）

> 状态：**IN_PROGRESS**（随各组完成追加；未完成范围不在此下全量结论）。
> 引用基准：`docs/dataset-2/dataset-2-copy/`。逐项证据见 `harness-c-cases-01..04.md`，文件清单见 `harness-c-coverage.md`。
> 口径：只登记有现存原件支持的观察；模型 reasoning 不作结论；不改写原 verdict、不把局部通过外推为全功能。

## A. 交付完整性类

| 编号 | 现象 | 证据定位 | 归因 |
|---|---|---|---|
| C-F-01 | **`result.md` 大面积缺失**：D2-161..173、175、178、179、182、189、190、191、192、193 等已到终态却无 `output/batch/result.md` | 各项目录 glob 穷举；交付契约 §1.1 要求每项收尾写 result.md | 装置/流程（交付门禁未逐件核对） |
| C-F-02 | `evaluator_manifest.json` 仅“已生成目标”的项存在；未生成项缺 | D2-161..173 等无；D2-174/176/177/180/181/183/194/199 有 | 未发生（不适用），但**不应在报告中与缺件混写** |
| C-F-03 | 预检 job 目录缺 `job-id.txt`、job 级 `batch-authorization.json`、`this-task-classification.json`、`controller.log`、`runners-*` | D2-161..166 七 job；对比 `c-to-cpp/D2-151`、`batch/platform-probes/*` 有这些件 | 装置/流程（预检 job 最小取证集偏薄） |
| C-F-04 | D2-162 `job-00b-source-buildability-blocker-isolation/` 缺 `evaluation_report.json` | 该目录仅 4 件 | 装置 |
| C-F-05 | D2-174 `job-00` 缺 `evidence-target.json` 与 `comparison.json`，而 report 称 target execution performed=true | 子审阅 C3 记录 | 装置（回执与落盘不一致） |
| C-F-06 | D2-175 `job-00` 缺 `comparison.json`（`comparisonRef` 指向它） | 同上 | 装置 |
| C-F-07 | D2-177 `job-00/returned-evidence/evaluation_report.json` 内容为 `{"detail":"job_report_not_found"}` | 同上 | 装置 |

## B. 冻结/分类/身份关联类

| 编号 | 现象 | 证据定位 | 归因 |
|---|---|---|---|
| C-F-08 | **D2-176 缺 `01-frozen/frozen-inputs.md` 与 `02-conversion/target.gen.model.json`，却 `disposition=CONVERTED/phase=CLOSED/lifecycle=DONE`；`result.md` 第17行仍链接不存在的 frozen 文件** | `c-to-python/D2-176-c-c-pwd.c/output/batch/` | 装置/流程（冻结落盘门禁与收尾核对失效） |
| C-F-09 | **item `classifier.cls` 与 `classification-1.json` 不符（D2-184..188 五例全部）**：item 写 `REVIEW_UNCERTAIN`，产物为 `REVIEW_NETWORK`/`REVIEW_SIDE_EFFECTS`/`REVIEW_SENSITIVE` | 各 `batch/items/<ID>.json` vs `01-frozen/classification-1.json` | 装置（item 生成器字段映射错误） |
| C-F-10 | **`frozen-inputs.md` 模板计数错误**：D2-185/186/187/188 称“覆盖 source/ 三件”，实际只列 2 件 | 各 frozen-inputs.md | 装置（模板） |
| C-F-11 | **分类输入清单与实际分类树不一致**：`classification-1.json.details.files` 含 Agent 加的 `run_case.py`，`classifier-input.json` 只登记源文件 | D2-184..188 等 | 流程（分类输入/输出范围不同源） |
| C-F-12 | **`batch-authorization.json` 逐项副本硬编码他项场景文案**：go-to-c 五例写“该项 **D2-088** 无网络…”，c-to-powershell 七例（14 个副本）写“该项 **D2-151** 无网络、无凭证，仅本地文件删除与只读遍历，使用合成 fixture (keep.txt/second.txt)”；`batch.json` 明示 `verify per item` 却无逐项核验痕迹 | 各 job 目录 `batch-authorization.json`（`contractHash=sha256:a9ed1445…`） | 装置（复制未替换；对 BLOCKED 的 D2-184、Windows 注入类的 D2-167/169 尤其不成立） |
| C-F-27 | **D2-169 伪 FAIL**：名为 `job-00-source-buildability` 的预检 job 实际运行了 **placeholder target**（`target/target.ps1 (placeholder)`，stdout=`D2-169 precheck placeholder`）并产出 `codeVerdict=failed`/`behaviorVerdict=mismatched`/`comparisonRef=comparison/result.json`；而 item 仍写 `targetBuild/execution/comparison=UNVERIFIED`，两者并存却不互指；源侧驱动自失败码 97 仍被判 `execution.status=completed` | `c-to-powershell/D2-169-.../job-00-source-buildability/returned-evidence/{evaluation_report.json,evaluation_report.md,evidence-target.json}` | 装置；不得计为转换或功能 FAIL |
| C-F-28 | **驱动声明与实物脱节**：`comparison_manifest.json` 声明 `runCommand=python run_case.py`、`target.buildCommand=pwsh -NoProfile -File build_case.ps1`，但磁盘上既无 `build_case.ps1`（D2-168/169 等），也无 `run_case.py`（仅分类器以 sha 记录过） | D2-167..173 `comparison_manifest.json` vs 目录 | 装置（事后无法判定驱动四要素是否满足） |
| C-F-29 | **`metadata.json` 占位符未替换**：D2-170 job-00 与 job-00b 均写 `sourceHash=sha256:PLACEHOLDER` | `c-to-powershell/D2-170-c-c-cmp.c/.../metadata.json` | 装置 |
| C-F-30 | **`events.jsonl` 与 items 不一致**：D2-168..173 无 `FROZEN` 事件却有 `01-frozen/frozen-inputs.md`；`DIRECTION_COMPLETE`（“all 7 items terminal”）与 D2-167/169 `lifecycle=WAITING` 冲突 | `batch/events.jsonl:301` 附近 | 装置 |
| C-F-13 | manifest `JobId` 与 `Evidence` 未随实际预检回填：D2-161..188 等 `JobId=""`、`Evidence=UNVERIFIED`，而磁盘已有源侧 build 诊断 | manifest.csv vs items/events | 流程（清单未更新） |
| C-F-14 | **行数不一致**：manifest `Lines` 与 `frozen-inputs.md` 记的行数在 D2-161(434/480)、162(260/300)、163(336/368)、164(347/371)、175(146/167)、176(109/123)、184(937/1086)、185(629/674) 不符 | manifest vs frozen/result | 待核（源已删，无法裁决；记录/装置侧口径不一） |

## C. 评估装置/响应完整性类

| 编号 | 现象 | 证据定位 | 归因 |
|---|---|---|---|
| C-F-15 | **预检 job 用 placeholder target 产生误导性 FAIL/MISMATCHED**：D2-174 job-00 `codeVerdict=failed/behaviorVerdict=mismatched`、D2-175 job-00（目标 stdout=`D2-175 placeholder`）、D2-176 job-00（3 条 diff 全来自 placeholder 文本）；这些负结论未在 item/result 中说明 | 各 job-00 `returned-evidence/evaluation_report.json` | 装置（历史占位形态；现行 source-only 源预检已可避开） |
| C-F-16 | **模型响应仅哈希**：D2-174/177 的 `target.gen.model.json`、D2-177 `target.self-repair-1.model.json` 只含 sha256 元数据，无 content 正文 ⇒ 生成/修复代码不可核验；“只含哈希的 model.json 不算完整响应” | 各 `02-conversion/*.model.json` | 装置（响应落盘形态） |
| C-F-17 | **单行 >2000 字符 JSON 被 read/grep 截断且不可分页**：大量 `returned-evidence/evidence-source.json` 尾部字段未读 | `read` 工具截断提示 | 装置（取证落盘应改多行 pretty JSON） |
| C-F-18 | **D2-177 job-01 假阳性 matched**：两侧 exit=1/stdout 空/stderr 均为 usage 文本，驱动未转发冻结 argv，核心 PATH 搜索未跑；`attribution.md` 已归因装置并保留原 verdict；job-02 修正后 matched | `c-to-python/D2-177.../job-01-dual-build/attribution.md` | 装置（驱动） |
| C-F-19 | **驱动换行转义装置故障（§16）**：D2-186 的 `run_case.py` 第13行 `SyntaxError: unterminated string literal`，被测目标从未运行 | D2-186 `evidence-source.json` execution.stderr | 装置 |
| C-F-20 | **D2-184 是 BLOCKED 却存在孤儿 `job-00`**：`job-id.txt=ERR`、`evidence-source.json={"detail":"evidence_not_found"}`、`metadata.targetHash=placeholder-precheck`，且该 metadata 写 `safetyClassification=ALLOWED`、`batch-authorization.scope=所有非BLOCKED任务`；frozen/result 却称“无 job-00” | `go-to-c/D2-184-go-gobound.go/output/batch/04-evaluation/job-00-source-buildability/` | 装置/流程 |

## D. 判定口径/知识类

| 编号 | 现象 | 证据定位 | 归因 |
|---|---|---|---|
| C-F-21 | **越界外推**：D2-164 frozen 断言 `__dead2` 在“已登记系统 linux/windows/macos × x64 均不提供”，但本项磁盘只有 1 个 linux job；`batch/pattern-note-bsd-userland-macos-correction.md:19/21` 指出 macOS 提供含 `__dead2` 的 `sys/cdefs.h`，并要求 BSD userland 候选必须含 macOS | D2-164 frozen；D2-162/163/165/166 同样只有 linux job | 历史说明/记录；不得作已核事实 |
| C-F-22 | **规范文件自身表述不准**：`pattern-note-bsd-userland-macos-correction.md:19` 称本 6 项“只实测 windows 与 linux（见 frozen 的实验 A/B/C）”，但 D2-161..166 无 windows/macos job、无 A/B/C（疑与 D2-027 混淆） | 同文件 vs 六项目录 | 记录/装置 |
| C-F-23 | **D2-186 未落实现行 `LIB_UNOBSERVABLE_COMPILE_ONLY`**：源 `completed/0` 但非 main 无入口，历史记 `PREPARATION_GAP`、0 模型调用跳过转换；`AGENTS.md`/根 SKILL 现行规则要求继续生成并只验目标语法/编译、收尾 `PARTIAL` | `go-to-c/D2-186-go-flag.go`；`optimization-inputs-2.md` §2.3 亦提出该档位“当时未落地” | 历史问题，现行规则已解决方向 |
| C-F-24 | **D2-176 自审 `REPAIR-RECOMMENDED` 未修**（2 条 conversion-introduced：未知选项缺 libc getopt 诊断行），item 仍 `CONVERTED/CLOSED/DONE`；且 item `codeRevisions=1` 与 `result.md` “0 轮自修”冲突 | D2-176 `03-self-review/`、item、result.md | 流程/记录冲突 |
| C-F-25 | **D2-178 判定可信**：编译器原文 `strnsubst.c:75:34: error: 'uintptr_t' undeclared` 且 note 指向补 `<stdint.h>`；frozen 明确“源自身缺陷、非平台不匹配”，禁用 `-include` 掩盖 | D2-178 item/frozen/job-00 | 源已有缺陷（记录准确） |

## E. 事件与产物交集

| 编号 | 现象 | 证据定位 | 归因 |
|---|---|---|---|
| C-F-26 | **D2-165、D2-166 缺 `FROZEN_AND_CLASSIFIED` event**，但 `01-frozen/frozen-inputs.md` 实存 | `batch/events.jsonl` 133–138 行 | 装置（§8 增量对账应把“event 缺失但产物存在”单列） |

## F. 后续组新增发现（D2-179..213）

| 编号 | 现象 | 证据定位 | 归因 |
|---|---|---|---|
| C-F-31 | **`self-review-*.json` 多为单行 >2000 字符**，被 read 截断且不可分页 ⇒ “自审全部条目”只能读到前缀，尾部条目未读 | D2-174 `self-review-1.json`；D2-177 `self-review-1/2.json` 等 | 装置（落盘形态） |
| C-F-32 | **target “build” 命令不能证明语法**：`pwsh … Parser::ParseFile('target.ps1',[ref]$null,[ref]$null)` 把解析错误写入 `$null` 且不抛异常 ⇒ 文件可读即 exit 0；`targetBuild PASSED`/`codeVerdict passed` 名不副实（按 PowerShell 语义推断，本机未运行） | D2-199 `comparison_manifest.json` | 装置 |
| C-F-33 | **D2-199 job-00 整目录缺 `returned-evidence/`**，而 result/item/events 引用其 `completed/0`、7083 ms、37 ms、920 B 基线 ⇒ 该基线摘要无本副本原件 | `go-to-powershell/D2-199-.../job-00-source-buildability/` | 装置 |
| C-F-34 | **行数矛盾扩大**：manifest `Lines` vs frozen/result 在 D2-199(194/219)、200(163/186)、201(163/203)、203(145/160)、211(87/106)、212(92/115)、213(96/116) 均不一致 | manifest vs 各 result/frozen | 待核（源已删） |
| C-F-35 | **D2-213 分类器信号行号越界**：`signals.sensitive=[…,98,101]` 超出冻结 96 行；manifest/冻结=96、result=116、信号至 101 三方矛盾 | `go-to-ruby/D2-213-.../01-frozen/classification-1.json` | 证据链自身不一致（装置/流程） |
| C-F-36 | **D2-210 第二次分类的输入清单未保存**：`classifier-input-2.json` 仍只有 1 条（`.cs`），而 `classification-2.json` 实测含 3 件（`.cs`+`program.csproj`+`run_case.py`） | `csharp-to-powershell/D2-210-.../01-frozen/` | 流程 |
| C-F-37 | **冻结后改 buildCommand 未回写冻结记录**：D2-210 frozen 写 `-o bin`，job-01 实际 `-o .` | D2-210 frozen vs job-01 `source_preflight_manifest.json` | 流程 |
| C-F-38 | **`metadata.json` 的 `cls=` 空值**：D2-201/202/203 写 `safetyClassification=…cls=(see classification-1)` | 各 job `metadata.json` | 装置 |
| C-F-39 | **`batch-authorization.json` 样板又换他项**：go-to-powershell / go-to-ruby 组写“该项 **D2-197** (Go stdlib sort.go) 无网络、无凭证、无文件写入, 为纯算法库代码”；对 shellcode/注入/键盘记录样本不实 | D2-199..203、209..213 各 job `batch-authorization.json` | 装置 |
| C-F-40 | **report 样板句不适配**：`evaluation_report.md` 在 `build failed`/oracle `NOT_APPLICABLE` 的报告里仍含 `PASS covers the supplied critical oracle assertions only` | D2-200/201/202/203 `evaluation_report.md` | 装置 |
| C-F-41 | **副本 README 与现状矛盾**：`README.md` 自陈“本目录只有清单与源码”“§4 校验 `source/<file>` 存在且哈希相符”，但整副本 **0 个代码文件**、无 `source/` | `docs/dataset-2/dataset-2-copy/README.md` vs glob | 装置/快照语义 |
| C-F-42 | **item `casePath` 大小写与磁盘不符**：D2-200 `…EarlyBird.go` vs 磁盘 `…earlybird.go`；D2-201 `…UuidFromString.go` vs `…uuidfromstring.go` | items vs 磁盘 | 装置（大小写敏感存储上失配） |
| C-F-43 | **平台回传件不钉被评估构件**：`evaluation_report.json`/`evidence-*` 中无 `artifactHash`、无 `target.ps1`、无源哈希 ⇒ “评估对象==冻结版本”仅由 Agent 侧声明支撑 | D2-199 平台件 | 装置 |
| C-F-44 | **D2-202 冻结静态画像被编译器否证**：frozen 预判 `small/nSmalls/formatBits` 不在文件内 ⇒ `SOURCE_DEPENDENCY_GAP`，实测 `completed/0`（四符号均在文件内）；已在 result 留痕纠正（冻结件按规则保留原样） | D2-202 frozen vs `evidence-source.json`/result | 流程（预判非证据） |
| C-F-45 | **D2-199 生成/自审响应仅哈希**：`target.gen.raw.json`、`request.body.json`、`self-review-1.raw.json`、`request.system.txt`、`review.system.txt` 正文全缺，只有 sha256 | D2-199 `02/03` 关联记录 | 装置 |
| C-F-46 | **D2-210 ORACLE_NOT_FREEZABLE 的另一泄漏源**：job-specific workspace 路径同时出现在 `dotnet build` 的 **stdout**（不止 stderr 异常栈） | D2-210 两 job `evidence-source.json` | 装置 |

| C-F-47 | **D2-175 冻结声明与实际提交矛盾**：`frozen-inputs.md` 写「不冻结 oracle、**不提交**」，但磁盘存在整套 `job-00`（源侧 `DRIVER-FAILURE: no runnable artifact`，exit 97，target 为 placeholder），并产出 `failed/mismatched` 报告 | `c-to-python/D2-175-.../01-frozen/frozen-inputs.md` vs `04-evaluation/job-00/` | 装置/流程 |
| C-F-48 | **D2-174 `evaluator_manifest.json` 声称 `hasReplayArtifact true` 且指向 `.../job-01-dual-build/capsule.zip`，该件不存在** | D2-174 `output/batch/evaluator_manifest.json` | 装置（不可核验声明） |
| C-F-49 | **D2-177 假阳性已留证并修正**：job-01 平台 `matched`/diffs=0，但两侧均走 usage 分支（驱动未转发冻结 argv）；`attribution.md` 归因装置、保留原判定；job-02 修正驱动后真正覆盖 PATH 搜索。⇒ 应把「驱动转发冻结 argv + 源侧观察非退化」纳入提交前评估就绪硬检查 | D2-177 `job-01/attribution.md`、job-02 证据 | 装置（已识别）；流程缺口（检查项未固化） |
| C-F-50 | **D2-178 是「源不可构建」的正确报告模板**：target `performed=false`、`preflight/cleanup=SKIPPED`、`comparisonRef=null`、`runVerdict=blocked`、`code/behaviorVerdict=inconclusive`、coverage 0、0 模型调用；未改源码、未用 `-include` 掩盖 | D2-178 `job-00/returned-evidence/evaluation_report.json` | 正面样板（对照 D2-174/175/176 的 placeholder mismatched） |
| C-F-51 | **D2-207 stderr 归因与批次内审存在分歧**：`result.md` 记为“装置/语言运行时（§14 同类）”，而 `full-review-self-reviews-02.md:45` 提出“stderr 外形可明确允许，但不能自动被当装置”；本会话认为绑定到**未冻结的比较策略**（job-01 `workspace_path_pairs=[]`）更准确 | D2-207 item/result vs 内审记录 | 未定（口径待收敛） |
| C-F-52 | **D2-174/175/176 的预检 placeholder 负结论未在 item/result 登记**（item 仍写 UNVERIFIED/无比较），只留在 `job-00` 回执里 | D2-174/175/176 `job-00/returned-evidence/` | 装置/流程 |
| C-F-53 | **D2-175 冻结 `sourceLines=167` vs manifest 146；D2-176 result「123 行」vs manifest 109**（行数口径冲突已并入 C-F-34/C-F-14） | 见各 frozen/result | 待核 |

<!-- FINDINGS-ANCHOR: append per-group findings as groups complete -->

## G. 第二轮（验收补读 + D2-232/233/235-240）新增发现

| 编号 | 现象 | 证据定位 | 归因 |
|---|---|---|---|
| C-F-54 | **D2-190 真错更正**：全文为 `OSError: [WinError 216] 该版本的 %1 与你运行的 Windows 版本不兼容`（EXE 机器类型不匹配）⇒ 程序**已产出但不可运行**，更正第一轮基于 grep 的“未产出文件/FileNotFoundError”推断 | `go-to-cpp/D2-190-.../job-00/returned-evidence/evidence-source.json`（778 B） | 装置/环境 |
| C-F-55 | **D2-194 `target.gen.model.json` 是完整响应（非仅哈希）**：含 `content`（完整 C# 代码）与 `reasoning_content`；其目标 exit 150 的确切原因是 runner 只有 .NET 10.0.10 而目标是 net8.0（SDK 10.0.110），**环境**而非转换 | `go-to-csharp/D2-194-.../02-conversion/target.gen.model.json`、job-01 `evidence-target.json` | 装置/环境（另说明 C-F-16 不能一概而论“只含哈希”） |
| C-F-56 | **D2-232 job-00 报告把驱动故障写成成功**：`evaluation_report` `executionAssessment=completed`/`failure=null`，而 `evidence-source.execution.exitCode=97` 且 stderr=`DRIVER-FAILURE: no runnable target found` | `powershell-to-ruby/D2-232-.../job-00/returned-evidence/` | 装置（报告层） |
| C-F-57 | **D2-232 冻结评估计划过期**：`frozen-inputs.md` 仍写 `runCommand=["python","run_case.py"]`/timeout 60，实际 job-00b 为 `pwsh -NoProfile -File build_run.ps1`/timeout 120，且无重冻结记录 | D2-232 frozen vs job-00b | 流程 |
| C-F-58 | **D2-232 分类输入/输出不一致**：`classifier-input*.json` 只列 1 件，而 `classification-1.json`/job-00 分类件列 2 件（含 `run_case.py`）；两版 `inputManifestSha256` 同为 `fc767c9b…`（文件集不同却同哈希） | D2-232 `01-frozen/`、job-00 | 流程/装置 |
| C-F-59 | **D2-233 `metadata.json` `cls=` 空值**；且 `result.md` 把未生成的目标写为“PowerShell 7.6→Ruby CRuby 3.4”（计划值） | D2-233 job-00 `metadata.json`、`result.md` | 装置/流程 |
| C-F-60 | **D2-236 去向口径待裁**：结果记 `PREPARATION_GAP`、生成前停止、0 模型调用；而 `AGENTS.md` §3 要求“源可构建但本轮无法合法评估”按 `LIB_UNOBSERVABLE_COMPILE_ONLY` 继续生成并只验目标语法/编译。本项 build `completed/0` 且 argv=[] 在 `parse_args()`(L6018) 退化、无合法驱动。**两口径是否互斥需按契约原文裁定**，影响“是否应生成目标”与批次计数 | `python-to-c/D2-236-.../result.md`、item；events L951 `CORRECTION` | 流程/契约 |
| C-F-61 | **python-to-c 5/5 行数冲突**：manifest `Lines` vs frozen/result＝D2-235 582/677、236 5640/6364、238 770/918、239 1007/1189、240 609/703 | manifest 217–221 vs 各 frozen | 待核（源已删） |
| C-F-62 | **closure.artifactDigests 引用件未回传（系统性）**：`evidence/source-call.json`、`source-identity.json`、`source-request.json`、`source-response.json/.body`、`request.json`、`staging-manifest.json`、`lifecycle.jsonl` 只列摘要，用例目录只有 `returned-evidence/` 数件 | D2-199/232/233/235/236/238/239/240 等 `closure.json` | 装置（“最小回传集”未定义） |
| C-F-63 | **重分类历史机读字段丢失**：D2-235/236 `classification-2.json` 的 `old_cls`/`old_reason` 均 `null`，首轮 `BLOCKED/public_network_unverified` 仅存于 events/item.note | D2-235/236 `01-frozen/classification-2.json` | 装置（重分类产物不可自证） |
| C-F-64 | **D2-194 自审遗漏已定位**：`CmdSwitch` 缺 `case "exec"` ⇒ `Ex` 死代码、`exec` 落 default；`codeRevisions=1` 已修但 repair 请求/响应原件缺失 | D2-194 `self-review-1.json`、item | 转换引入（已修，原件缺） |
| C-F-65 | **第一轮 2000 字符截断已在第二轮按官方提高后的上限解除**（c-to-go 7、c-to-powershell 15、go-to-c 4、go-to-cpp 5、go-to-csharp D2-194 3、c-to-python 自审 3、python-to-c 10、powershell-to-ruby 8）；**仍有未补读集合**（c-to-python 行为件、c-to-ruby、go-to-csharp 其余、go-to-powershell、go-to-python、go-to-ruby、csharp-to-powershell/go）见 `harness-c-coverage.md` §5 末 | 见 coverage §5 | 装置（读取上限） |
| C-F-66 | **D2-194 `target.gen.model.json` 含完整 reasoning_content**（非结论证据）：审阅只采信 `content`（目标代码）与元数据；模型 reasoning 不作自审/行为结论 | 同上 | 口径（已遵守） |
