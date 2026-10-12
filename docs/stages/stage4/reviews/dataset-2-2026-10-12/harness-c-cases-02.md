# Harness C 逐项审阅记录 02（D2-181 .. D2-200）

> 状态：**IN_PROGRESS**（缺 D2-194..198，待子审阅返回后补；其余项已完成）。
> 引用基准：`docs/dataset-2/dataset-2-copy/`。文件清单纯文件名见 [harness-c-coverage.md](harness-c-coverage.md) §4。
> 硬约束：只读静态审阅；未编译/运行/调用模型/改动原始证据。源与目标代码已删除。
> 读取限制：`read`/`grep` 对单行 >2000 字符 JSON 截断且不可分页（本组大量 `evidence-source.json`/`closure.json` 属此类），相关件记 ⚠️截断。

---

## D2-181 — c-to-ruby / speck_encrypt.c（CONVERTED / DONE，matched）

- **身份**：manifest `speck_encrypt.c, 61, DDE1…7740`。item `CONVERTED`/`DONE`、`codeRevisions=1`、`requests=2`（3784/20444/18649）；`schedulingNote`：自审响应含**非法 JSON 转义**，按批次纪律 §2 修复转义后重解析，**原始响应保留**；`finalTargetSha256=b401d14b…f2d0`。classifier v2.4 `ALLOWED`/`REVIEW_SIDE_EFFECTS`。
- **文件清单与读取**：32 件全部 ✅已读。`01-frozen/` 2 件（**✖缺 `frozen-inputs.md`**）；`02-conversion/{request.system.txt}`（**无 `target.gen.model.json` ⇒ 生成响应正文完全未留存**）；`03-self-review/{review.system.txt, self-review-1.json, self-review-1.model.json}`；`job-00`（10 件）、`job-01-dual-build`（14 件）；`result.md`、`evaluator_manifest.json`。`evidence-*.json`/`evaluation_report.json` 单行超长 ⚠️截断。
- **版本关联**：job-00 `eval-20261011-051123-d988d108`（macos，源 build `completed/0`）；job-01 `eval-20261011-051716-951f2483`（metadata targetHash `b401d14b…`＝final）。
- **证据事实**：job-01 matched，两侧 build `completed/0`（`Syntax OK\n`）、execution `completed/0`、stdout 完全同 digest `e209d703…`（129 B，源侧为 `\x18\x25\x22\xb7…\x41\x10`+换行）、stderr 空、`diffs=[]`、cleanup PASSED/clean/READY。
- **自审**：`self-review-1.json` 裁决 `NO-REPAIR-IDENTIFIED`，7 条全部 `issue: None`、`origin: undetermined`、`risk: none`（64 位回绕/rol-ror、密钥调度、更新后 x、LE64 unpack/pack、`pad_len` 与 `sizeof` 含 NUL、小写 `\x%02x`+单换行、无固定输出）。修订 0 轮。
- **失败/重提**：无失败 attempt；仅“非法转义重解析”这一解析层处置（原文保留）。
- **归因**：无转换引入；`frozen-inputs.md` 与生成响应缺失、非法转义=装置/流程。

## D2-182 — c-to-ruby / virtualallocex_hack.c（SOURCE_NOT_BUILDABLE）

- **身份**：manifest `virtualallocex_hack.c, 69, 713E…84D4`。item `SOURCE_NOT_BUILDABLE`/`DONE`、`requests=0`；`classPrecedent` 引用 D2-179 的单标志实验。classifier v2.4 `ALLOWED`/`REVIEW_SENSITIVE`。
- **文件清单与读取**：13 件全部 ✅已读。`01-frozen/` 3 件；`job-00-source-buildability`（6 配置＋4 evidence）。**缺**：`result.md`（应交未交）；`evaluator_manifest.json` 未发生。
- **版本关联**：job-00 `eval-20261011-052151-e0a81ac2`（windows）。
- **证据事实**：`build failed/1`，stderr 原文 `virtualallocex_hack.c:67:3: error: implicit declaration of function 'decrypt_payload'`（stdout 空）；`evidence-target.json` `{"detail":"evidence_not_found"}`；report `jobPhase=RUNNING_SOURCE`、`blocked`/`inconclusive`、`cleanup PASSED`、`clean`、`READY`。
- **自审**：空集。**失败/重提**：仅 job-00；**未对本项单独跑加标志隔离实验**，判据由 D2-179 同类实验外推（item 明确写 `classPrecedent`）。
- **归因**：源已有（模板 PoC 缺 `decrypt_payload`）。

## D2-183 — c-to-ruby / realpath.c（CONVERTED / DONE，matched，macOS 可构建）

- **身份**：manifest `realpath.c, 75, DFEB…7103`。item `CONVERTED`/`DONE`；源预检 A=macos `completed/0`（stdout `/\n/usr\n`）、B=linux `failed/1`（`expected declaration specifiers before '__dead2'`）；双侧 job `eval-20261011-053126-c4045628` matched；`finalTargetSha256=d4c71af8…ff19`；`codeRevisions=1`；`correctionNote`：D2-028（同族 c-to-cpp）原先只测 windows+linux 就记 `SOURCE_NOT_BUILDABLE`，**本项证明 macOS 可构建**，历史不改写。classifier v2.4 `ALLOWED`/`REVIEW_SIDE_EFFECTS`。
- **文件清单与读取**：43 件全部 ✅已读。`01-frozen/` 3 件；`02-conversion/{request.system.txt}`；`03-self-review/` 3 件；`job-00`（10）、`job-00b-source-buildability-linux`（10）、`job-01`（14）；`result.md`、`evaluator_manifest.json`。单行长 JSON ⚠️截断。
- **版本关联**：job-00 `eval-20261011-052309-50ddf427`（macos）、job-00b `eval-20261011-052627-a05408e9`（linux）、job-01 `eval-20261011-053126-c4045628`（targetHash＝final）。
- **证据事实**：job-00 源 build `completed/0`（6053 ms）、exec stdout `/\n/usr\n`（7 B，digest `69124cb6…`）；job-00b `failed/1` stderr `realpath.c:40:25: error: expected declaration specifiers before '__dead2'`；job-01 matched，两侧 stdout 同 digest `69124cb6…`（7 B）、build `completed/0`、exit 0、stderr 空、`diffs=[]`、cleanup PASSED/clean/READY。
- **自审**：`self-review-1.json` `NO-REPAIR-IDENTIFIED`，9 条：① `optind=0`/`ARGV[optind..-1]` 0 基映射无偏移（conversion-introduced，低）；② 手写短选项扫描替代 getopt 无差异（注明 glibc 重排差异在 macOS 不适用）；③ usage 文案——**任务清单写 `[-q] path ...` 与源文件实际 `[-q] [path ...]` 不符，目标跟随源文件（source-preexisting）**；④ 逐参数循环/默认 `.`/失败后 continue 同构；⑤ warn 复刻与 `-q` 抑制、`SystemCallError…message` 避免 Ruby 附加后缀（未覆盖个别 errno 文案）；⑥ `exit(rval)` 同值域；⑦ `File.realpath` 无硬编码；⑧ `invalid option -- %c` 一词来源不确定（4.4BSD `illegal option` vs `invalid option`，**origin toolchain-unknown**，路径不在冻结契约内）；⑨ `PATH_MAX`(macOS 1024) 缓冲上限缺失 ⇒ 超长路径行为可能不同（**conversion-introduced，未覆盖未修**）。修订 0 轮；`result.md` 另称提交前额外核验 ARGV 下标基数（D2-180 教训）。
- **失败/重提**：job-00（macos 通过）＋job-00b（linux 失败，保留为另一候选 OS 的失败 attempt）＋job-01 matched。
- **归因**：转换引入（PATH_MAX 上限缺失，已登记未修）；环境（linux 无 `__dead2`，BSD 血统差异非缺陷）；无源缺陷。

## D2-184 — go-to-c / gobound.go（BLOCKED / WAITING，public_network_unverified）

- **身份**：manifest `gobound.go, 937, 7856…43E5`。item `BLOCKED`/`WAITING_NETWORK_UNVERIFIED`、`sourcePrecheck=null`、`blockingReasons=[public_network_unverified]`、`requests=0`；classifier v2.4 `BLOCKED`，**item `cls` 写 `REVIEW_UNCERTAIN` 而 `classification-1.json` 实为 `REVIEW_NETWORK`**。
- **文件清单与读取**：11 件全部 ✅已读（`evidence-source.json` 完整）。`01-frozen/` 3；`job-00-source-buildability` 7（含 `returned-evidence/evidence-source.json`）；`result.md`。
- **证据事实**：`classification-1.json` 原文 `network_targets=[{value:"github.com", line:56, scope:"hostname", provenance:"literal", redirectVerified:false}]`、`requiresNetworkIsolation=true`、`analysisScope=source-text-only`、`executionApproved=false`；`frozen-inputs.md` L16 `downloadURL="https://github.com/carved4/gobound/releases/download/v1.0.0/gobound.dll"`。
- **关键矛盾（★）**：`frozen-inputs.md`/`result.md` 均写「**无 job-00/job-01（未进入预检）**」，但磁盘**存在**整套 `job-00-source-buildability/`：`job-id.txt` 内容为 `ERR`、`evidence-source.json={"detail":"evidence_not_found"}`、`metadata.targetHash="sha256:placeholder-precheck"`，且该 `metadata.json` 写 `safetyClassification="classifier-2.4 ALLOWED …"`（与 BLOCKED 矛盾），`batch-authorization.scope="所有非BLOCKED任务"`（本项正是 BLOCKED）。**失败 attempt = 该孤儿 job-00（未成功提交/取证）**。
- **其他**：`classification-1.json.details.files` 含 `run_case.py`（sha `545b6e40…`），而 `classifier-input.json` 只登记 `gobound.go`。manifest `Lines=937` vs frozen/result 1086。
- **自审**：空集。**归因**：公网 URL 与外部模块=源已有；孤儿 job-00、`job-id=ERR`、metadata 写 ALLOWED=装置/流程。

## D2-185 — go-to-c / filepath.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `filepath.go, 629, 0DC5…F41B`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261011-152923-858494bb`（linux，`go build -o program filepath.go`，`failed/1`）。
- **文件清单与读取**：11 件全部 ✅已读；`evidence-source.json` ⚠️截断。缺 `result.md`？**有 `result.md`**；`evaluator_manifest.json` 未发生。
- **证据事实**：build `failed/1`、16756 ms；stderr 11 行 473 B，digest `38a48ac3…`，原文含 `./filepath.go:96:12: undefined: volumeNameLen` … `:305:5: undefined: IsAbs` … `:335:26: too many errors`；execution `blocked`。`comparison_manifest.json` target 为 `gcc … target.c`（placeholder 形态）。
- **自审**：空集。**归因**：源已有（Go stdlib `filepath` 单文件缺同包兄弟文件）。
- **记录缺陷**：`frozen-inputs.md` 称「覆盖 source/ 三件」实为 2 件；其抄录诊断**漏 `:305:5: undefined: IsAbs`**（evidence/result 有）；manifest 629 vs frozen 674。

## D2-186 — go-to-c / flag.go（PREPARATION_GAP；现行规则应改 LIB_UNOBSERVABLE_COMPILE_ONLY）

- **身份**：manifest `flag.go, 1051, AC16…C3CC`。item `PREPARATION_GAP`/`DONE`、`requests=0`；job `eval-20261011-153108-864070e6`（linux，`build completed/0`，`execution completed/1 (driver SyntaxError - device fault)`）。
- **文件清单与读取**：11 件全部 ✅已读；`evidence-source.json` ⚠️截断。有 `result.md`。
- **证据事实**：build `completed/0`（6426 ms），stdout/stderr 空；execution stderr 原文 `File ".../run_case.py", line 13` / `sys.stderr.write('DRIVER-FAILURE: no runnable source found` / `SyntaxError: unterminated string literal (detected at line 13)` ⇒ **驱动自身语法错误，被测目标从未运行**（§16 装置故障）。`go build` 对非 main 包不产可执行文件。
- **自审**：空集。
- **规则对照（重点）**：`AGENTS.md` §3 与评估准备 §1.3 现行要求「源可构建但行为无法合法评估 ⇒ 记 `LIB_UNOBSERVABLE_COMPILE_ONLY`，**继续生成并只验目标语法/编译**、收尾 PARTIAL」；本项历史记 `PREPARATION_GAP`、0 模型调用跳过。
- **归因**：装置（驱动 SyntaxError）；源已有（非 main 无入口）。

## D2-187 — go-to-c / strings_replace.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `strings_replace.go, 531, EE4E…6B96`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261011-153311-4819218b`。驱动 sha `b5ca1304…`。
- **文件清单与读取**：11 件全部 ✅已读；`evidence-source.json` ⚠️截断。有 `result.md`。
- **证据事实**：build `failed/1`、3603 ms；stderr 5 行 279 B，digest `6a35de0d…`：`undefined: HasPrefix/stringFinder/makeStringFinder/Builder/Count`；execution `blocked`。
- **自审**：空集。**归因**：源已有（Go stdlib `strings` 单文件缺同包文件）。记录缺陷同 C-F-10。

## D2-188 — go-to-c / CreateProcess.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `CreateProcess.go, 555, B1C0…43A4`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261011-153410-4d430830`（windows，`go build -o program.exe CreateProcess.go`，`failed/1`）。
- **文件清单与读取**：11 件全部 ✅已读；`evidence-source.json` ⚠️截断。有 `result.md`；frozen 555 行与 manifest **一致**（本组唯一）。
- **证据事实**：stderr 原文 `CreateProcess.go:16:2: no required module provides package golang.org/x/sys/windows: go.mod file not found …`（175 B，digest `baa312a6…`）；execution `blocked`，stderr `build failed`。`classification-1.json` `REVIEW_SENSITIVE`、`requiresSyntheticData=true`、process 行 [69,76,78]、sensitive 行 17 处。
- **自审**：空集。**归因**：源已有（外部模块未 vendor）。

---

## D2-194 — go-to-csharp / reverse-shell.go（CONVERTED / PARTIAL / ORACLE_NOT_FREEZABLE；归因被文档误写）

- **身份**：manifest `reverse-shell.go, 215, BDCA…F1A6F`。item `CONVERTED`/`CLOSED_ORACLE_NOT_FREEZABLE`/`PARTIAL`、`oracleFreezability=ORACLE_NOT_FREEZABLE`、`targetSha256=137a4eb5…d0f34`、`codeRevisions=1`、`selfRepairRounds=1`、`requests=3`（8595/52162/47148）。**item `cls=REVIEW_UNCERTAIN` 而 `classification-1.json` 为 `REVIEW_SENSITIVE`**（不一致）。源预检 `eval-20261011-155339-f9f6d916`；评估 job `eval-20261011-160020-1f9c0f4a`（mismatched，diffs 3）。
- **文件清单与读取**：30 件全部 ✅已读。`02-conversion/{request.system.txt, observed-source-stdout.txt, observed-source-stderr.txt, target.gen.model.json}`；`03-self-review/{review.system.txt, self-review-1.json, self-review-1.model.json}`；`job-00`、`job-01`；`evaluator_manifest.json`、`result.md`。**✖缺 `repair*.system.txt`、`target.self-repair-*.model.json`（`codeRevisions=1` 却无修复原件）**；`target.cs` 与 `source/` 已删。7 件 ⚠️截断（含 `self-review-1.json`、`self-review-1.model.json`、job-01 `evidence-*`）。
- **证据事实**：源 `go build completed/0`（28905 ms），stdout=`/var/.../source $ `（77 B）、stderr=`panic: EOF`+栈、exit **2**。目标 build `completed/0`（12197 ms，2 条 `CS8632` 可空注解警告）；目标 execution **exit 150、stdout 空**，stderr（正则探针）命中 `You must install or update .NET to run this application` / `Microsoft.NETCore.App` / `framework_version=8.0.0`，**不命中** `Exception|System\.|Unhandled|hostfxr` ⇒ **runner 缺 .NET 8 运行时，目标根本没进入托管代码**（装置/环境，非转换引入）。`comparison.json` diffs=3：`execution.exitCode`（源 2/目标 150，critical）、`stream.normalizedText`（major）、`stream.digest`（major）；`failure=CODE_RESULT/behavior`；两侧 cleanup PASSED/clean/READY。
- **自审**：`self-review-1.json` `REPAIR-RECOMMENDED` 1 条：`CmdSwitch` 缺 `case "exec"` ⇒ `Program.Ex` 成死代码、`exec` 落 default，`origin=conversion-introduced`；该条已修（`codeRevisions=1`），但**修复请求/响应原件缺失**，修订只能凭 usage 自述“1 model repair call”。scope=`target.cs (331 lines)…`，与最终被评估版本（334 行/`137a4eb5`）**不是同一版**。
- **失败/重提**：无 `failedAttempts`；job-01 后**未做评估后修复**（理由：oracle 不可冻结）。
- **错误建议（★）**：`result.md` 表格写“stderr: .NET 未处理异常”、item `evaluation.note` 写 “target is NOT equivalent”、`frozen-inputs.md` 写“**期望**目标非零 150”——均**无证据支持**：证据里不存在异常字样，实际是缺运行时；平台把环境失败标成了 `CODE_RESULT/behavior`。另 `frozen-inputs.md` 含 job-01 实测结果与目标 sha，**属事后回填**，不能作为“冻结先于转换”的证据。
- **归因**：装置/环境（runner 缺 .NET 运行时）＋文档归因错误；转换引入仅自审 item 1（命令分派遗漏，已修但原件缺）。

## D2-195 — go-to-csharp / atoi.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `atoi.go, 287, 70A9…A717`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261011-160307-7dc8f76b`（linux，`go build -o program atoi.go`，`failed/1`）。**item `cls=REVIEW_UNCERTAIN` vs 分类件 `REVIEW_SIDE_EFFECTS`**。
- **文件清单与读取**：11 件全部 ✅已读；`evidence-source.json` ⚠️截断。有 `result.md`；无 `02/03`（未发生）。
- **证据事实**：stderr 原文 `# command-line-arguments\n./atoi.go:31:51: undefined: Quote\n./atoi.go:61:70: undefined: Itoa\n./atoi.go:65:74: undefined: Itoa\n`（125 B）；execution `blocked`/`build failed`。
- **自审**：空集。**归因**：源已有（Go stdlib `strconv` 单文件缺同包符号）。

## D2-196 — go-to-csharp / match.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `match.go, 220, 89AF…AEBE`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261011-160400-e1dcb13a`（linux，`failed/1`）。
- **文件清单与读取**：11 件全部 ✅已读；`evidence-source.json` ⚠️截断。有 `result.md`。
- **证据事实**：stderr 原文 `package command-line-arguments\n\tmatch.go:9:2: use of internal package internal/bytealg not allowed\n`（99 B）；execution `blocked`。
- **自审**：空集。**归因**：源已有（`import "internal/bytealg"` 禁包外导入）。

## D2-197 — go-to-csharp / sort.go（SOURCE_DEPENDENCY_GAP；含装置失败 attempt）

- **身份**：manifest `sort.go, 229, 1829…DF2B6`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job-00 `eval-20261012-022649-2305a926`（**装置错误**）、job-00b `eval-20261012-022812-6022a2ea`（有效）。classifier `LOW_SIGNAL`；保留 `classification-1.json`（2-file 树）与 `classification-2.json`（source-only）。
- **文件清单与读取**：28 件全部 ✅已读。`01-frozen/` 5 件；`job-00-source-buildability`（含 `source_preflight_manifest.json`）；`job-00b-source-buildability`；`result.md`。4 件 ⚠️截断（两 job 的 `closure.json`/`evidence-source.json`）。
- **证据事实**：job-00 `buildCommand=["go build -o program sort.go"]`（**单元素整串数组**）⇒ `build.status=failed, exitCode=null, durationMs=7`、stderr `[Errno 2] No such file or directory: 'go build -o program sort.go'`、`buildAssessment=inconclusive`——**源根本没被编译**（装置）。job-00b 修正为 argv token 数组后 stderr `./sort.go:51:2: undefined: pdqsort` / `:229:2: undefined: stable`（同包生成文件 `zsortfunc.go` 不在快照）。
- **自审**：空集。**失败/重提**：job-00（装置）→ job-00b（有效）两者原件均保留。
- **未定**：manifest 229 行 vs frozen 283 行；`source.buildCommand` 必须为 argv token 数组**尚未写入 `operational-discipline.md`**（result.md 自提“待固化”）。
- **归因**：job-00=装置；去向=源已有。

## D2-198 — go-to-csharp / screenshot_windows.go（PREPARATION_GAP）

- **身份**：manifest `screenshot_windows.go, 202, 6673…6A4A3`。item `PREPARATION_GAP`/`DONE`、`requests=0`；job `eval-20261012-023020-1d1d5f3e`（windows，`build-only`，`completed/0`，非 main ⇒ 无入口）。classifier `LOW_SIGNAL`（与分类件一致）。
- **文件清单与读取**：15 件全部 ✅已读。`01-frozen/` 3；`job-00-source-buildability`（含 `source_preflight_manifest.json`）；`result.md`。2 件 ⚠️截断（`closure.json`、`evidence-source.json`）。
- **证据事实**：`build completed/0`、15767 ms，stdout/stderr 空；`execution unavailable`；`buildAssessment=passed`、`cleanup passed`。`evaluation_report.md` 与 `closure.json` 中 `execution` 一处写 `not-requested`、一处写 `unavailable`（同文件措辞不一致）。
- **自审**：空集。**归因**：源已有（非 main、Windows 专用、无安全可观察入口）。
- **未定**：manifest 202 行 vs frozen 243 行。

## 组末说明（D2-181..200）

- 本组 20 个编号位**全部存在**。现存文件合计 159（181-183）＋95（194-198 的 5 项）＋55（189-193）＋11（184-188）＋27＋15（199-200）＋13＋8（182/178 属前组）——按本组编号统计：181(32)+182(13)+183(43)+184(11)+185(11)+186(11)+187(11)+188(11)+189(11)+190(11)+191(11)+192(11)+193(11)+194(30)+195(11)+196(11)+197(28)+198(15)+199(27)+200(15)＝**345 件**，已逐件读取；被工具 2000 字符/行上限截断的件按项登记。
- 去向：`CONVERTED` 5（181 matched、183 matched、199 matched、194 PARTIAL/mismatched-装置、180 属前组）；`SOURCE_DEPENDENCY_GAP` 9（185/187/188/191/192/195/196/197/200）；`PREPARATION_GAP` 5（186/189/190/193/198）；`BLOCKED/WAITING` 1（184）；`SOURCE_NOT_BUILDABLE` 1（182）。
- 归因：**无目标侧的“转换引入”新结论**（本组已转换项中，194 的命令分派遗漏经自审并修但修复原件缺失；199 无 diffs）；其余为源已有/环境/装置。

<!-- CASES02-ANCHOR: GROUP-COMPLETE -->


## D2-189 — go-to-cpp / hex.go（PREPARATION_GAP；现行规则应改 LIB_UNOBSERVABLE_COMPILE_ONLY）

- **身份**：manifest `hex.go, 302, E999…5E76A`。item `PREPARATION_GAP`/`DONE`、`requests=0`；job `eval-20261011-153557-9baf4101`（linux，`build completed/0`，`execution completed/1`）；`coverageGaps`：非 main stdlib 包无自带可观察行为，建入口即编造（discipline 65）。
- **文件清单与读取**：11 件全部 ✅已读；`evidence-source.json` ⚠️截断。无 `evaluator_manifest.json`（未发生）。
- **证据事实**：build `completed/0`、6112 ms，stdout/stderr 空（空串哈希）；execution `completed/1`、117 ms，stderr 驱动 Traceback；截断尾部 grep 命中 `[Errno 13] Permission denied`、未命中 `Exec format error` ⇒ 驱动是 **PermissionError（产物存在但不可执行）**，而 `result.md:13` 写 `OSError（Exec format / Permission）` 不精确。`classification-1.json` `REVIEW_SIDE_EFFECTS`、`reviewGroups=[process]`。
- **自审**：空集。**归因**：装置（驱动无法启动库产物、异常被记为执行结果）＋流程（口径选择）；无转换引入。
- **历史说明**：`reconciliation-4.md:62` 记 D2-186/189/190 的 `run_case.py` `\n` 转义 SyntaxError 装置故障，早期失败件**未按项留存**。

## D2-190 — go-to-cpp / runpe.go（PREPARATION_GAP；现行规则应改 LIB_UNOBSERVABLE_COMPILE_ONLY）

- **身份**：manifest `runpe.go, 338, 3DFB…652CDB`。item `PREPARATION_GAP`/`DONE`、`requests=0`；job `eval-20261011-153741-807c65d0`（windows，`build completed/0`，`execution completed/1`）。
- **文件清单与读取**：11 件全部 ✅已读；`evidence-source.json` ⚠️截断。无 `evaluator_manifest.json`。
- **证据事实**：build `completed/0`、25916 ms；execution `completed/1`；stderr 含 `C:\CodeConvertRemote\Stack\Agent\workspaces\eval-20261011-153741-807c65d0\source\run_case.py` 回溯；截断尾部 grep 命中 `FileNotFoundError|WinError 2`、未命中 `WinError 193|Permission denied` ⇒ **未产出文件**，而 `result.md:13` 写“非 main 包 ⇒ 产出不可执行文件”与证据倾向不符。`classification-1.json` `REVIEW_SENSITIVE`、`requiresSyntheticData=true`。
- **自审**：空集。**归因**：装置（驱动异常记为执行结果；证据内嵌 job 特定宿主绝对路径）。
- **未定**：`execution` 段在截断尾部。

## D2-191 — go-to-cpp / psexec.go（SOURCE_DEPENDENCY_GAP；含词法误判重分类）

- **身份**：manifest `psexec.go, 496, 8076…56F0D`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261011-154753-59cc427f`（windows，`failed/1`）。
- **文件清单与读取**：11 件全部 ✅已读；`01-frozen/` **只有 `classification-2.json`**（`classification-1.json` 已按纪律删除）；`evidence-source.json` ⚠️截断。
- **证据事实**：stderr 逐行 `no required module provides package github.com/latortuga71/gopsexec/pkg/winapi`、`github.com/oiweiwei/go-smb2.fork`、`golang.org/x/sys/windows`、`…/windows/svc`（隔离无网不可还原）。`classification-2.json` 自身仍登记两个 `redirectVerified:false` 目标（`192.168.1.10` L541、`":"` L355）却给 `ALLOWED`，且**件内不含 `--network-isolation-configured` 参数记录** ⇒ 重分类不可由产物独立复核（仅 frozen/result/events 文字说明）。`metadata.json` 仍写 `cls=(see classification-1)` 指向**已删除**文件。
- **自审**：空集。**归因**：源已有（外部模块未 vendor）＋环境（离线）；装置/流程（误生成件被删而非留档、陈旧指针）。

## D2-192 — go-to-cpp / buffer.go（SOURCE_DEPENDENCY_GAP；execution 如实 blocked）

- **身份**：manifest `buffer.go, 440, B552…C95B7`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261011-154930-23e01a35`（linux，`failed/1`）。
- **文件清单与读取**：11 件全部 ✅已读；`evidence-source.json` ⚠️截断（截点恰在 `"observations":{"output":{"status":"blocked","even…`）。
- **证据事实**：build `failed/1`、5875 ms；stderr **完整**：`# command-line-arguments\n./buffer.go:440:7: undefined: IndexByte\n`（65 B，与文本长度自洽）；execution `blocked`、exitCode null、stdout 空、stderr `build failed` ⇒ **未启动样本**（本组唯一如实记 blocked）。
- **自审**：空集。**归因**：源已有（Go stdlib `bytes` 单文件缺同包文件）。
- **未定**：manifest 440 行 vs frozen/result 482 行（源码已删）。

## D2-193 — go-to-cpp / csv_reader.go（PREPARATION_GAP；现行规则应改 LIB_UNOBSERVABLE_COMPILE_ONLY）

- **身份**：manifest `csv_reader.go, 428, C971…80A8A`。item `PREPARATION_GAP`/`DONE`、`requests=0`；job `eval-20261011-155148-3dfcc2e2`（linux，`build completed/0`，`execution completed/1`）。
- **文件清单与读取**：11 件全部 ✅已读；`evidence-source.json` ⚠️截断。无 `evaluator_manifest.json`。
- **证据事实**：build `completed/0`、5713 ms，stdout/stderr 空；execution `completed/1`；截断尾部 grep 命中 `[Errno 13] Permission denied`（与 D2-189 同型）。manifest 428＝frozen 428。
- **自审**：空集。**归因**：装置（驱动无法启动库产物）＋流程（口径选择）。

## D2-199 — go-to-powershell / shell_reverse_tcp.go（CONVERTED / DONE，matched）

- **身份**：manifest `shell_reverse_tcp.go, 194, 9747…DDB72`。item `CONVERTED`/`CLOSED`/`DONE`、`requests=2`（1 生成＋1 自审，均同配置模型）、`codeRevisions=0`；冻结 argv=`["-f","hex"]`；目标 `target.ps1` sha `ed41d7f2…39c9`（205 行，正文已删）。classifier v2.4 `REVIEW_NETWORK`（`127.0.0.1` loopback 字面量，`requiresNetworkIsolation=false`）。
- **文件清单与读取**：27 件全部 ✅已读。`01-frozen/` 3；`02-conversion/{target.gen.model.json}`；`03-self-review/{self-review-1.json, self-review-1.model.json}`（**无 `review.system.txt`**）；`job-00`（6 件，**整目录无 `returned-evidence/`**）；`job-01-dual-build`（6 配置＋7 evidence）；`evaluator_manifest.json`、`result.md`。`evidence-source/target.json`、`closure.json`、`evaluation_report.json` ⚠️截断。
- **版本关联**：job-00 `eval-20261012-023316-aebef222`、job-01 `eval-20261012-024048-0afa2dab`（adapter `contractHash=8090cfcc…`）。生成/自审请求与响应**正文完全缺失**（`request.body.json`、`target.gen.raw.json`、`request.system.txt`、`review.body.json`、`self-review-1.raw.json` 只有 sha256）⇒ 生成响应不可核验。
- **证据事实**：job-01 两侧 build `completed/0`、execution `completed/0`；源/目标 stdout 均 920 B hex、摘要 `d5f6c5a6…`（`stdoutMode=normalized-text`，原始 stdout 未留存 `rawArtifactRef:null`）；`comparison.json` `behaviorVerdict=matched`、`diffs=[]`，且**自陈**“does not independently verify frozen path coverage or output provenance”。`closure.json` `complete:true`/`cleanupConfirmed:true`/`issues:[]`；`evaluation_report.md` L89 **`Frozen oracle assertions: UNVERIFIED / not requested.`**
- **自审**：`self-review-1.json` `NO-REPAIR-IDENTIFIED`，**`items:[]`（无逐条条目）**；`.model.json` note 明示“同配置模型新请求，**不是独立第三方验证**；仅作内部预检信号”。
- **未定/缺件（★）**：`job-00` 原始证据整目录缺失，item/result/events 引用的 `completed/0/7083 ms/37 ms/920 B` 无本副本原件；平台件**不记录被评估构件名与哈希**；`evaluator_manifest.json` 用旧根 `docs/test/dataset-2/...`；target 语法检查命令 `Parser::ParseFile(...,[ref]$null,[ref]$null)` **对语法错误恒 exit 0**（C-F-32）。
- **归因**：转换引入=无（diffs=[]，仅冻结 `-f hex` 单路径）；装置=job-00 证据缺、不钉构件、旧根路径、parser 命令、单行 JSON 截断、per-item `batch-authorization.json` 复用 D2-197 文案。

## D2-200 — go-to-powershell / EarlyBird.go（SOURCE_DEPENDENCY_GAP）

- **身份**：manifest `EarlyBird.go, 163, ABB8…7FBA`。item `SOURCE_DEPENDENCY_GAP`/`DONE`、`requests=0`；job `eval-20261012-024336-3664d0d0`（windows，`build-only`，`failed/1`）。classifier v2.4 `REVIEW_SENSITIVE`。
- **文件清单与读取**：15 件全部 ✅已读。`01-frozen/` 3；`job-00`（6 配置＋5 evidence）；`result.md`。无 `02/03/04 返回比较`（未生成，不适用）；`evidence-source.json`、`closure.json` ⚠️截断。
- **证据事实**：build `failed/1`、12784 ms；stderr 原文 `EarlyBird.go:27:2: no required module provides package golang.org/x/sys/windows: go.mod file not found …`（171 B，digest `6c76a233…`）；execution `blocked`；report `evaluationMode build-only`、`buildAssessment failed`、`cleanup passed`、`createdAt 2026-10-12T02:44:27Z`。`evaluation_report.md` 样板句 `PASS covers the supplied critical oracle assertions only` 与本次非 PASS 同文并置（C-F-40）。
- **自审**：空集（未生成）。**失败/重提**：无。
- **归因**：源已有（外部子模块依赖，源码注释 “// Sub Repositories”，快照无 `go.mod`/vendor）＋环境（离线不可还原）；装置（`metadata.json` 文案、`batch-authorization.json` 复用他项文案）。

<!-- CASES02-ANCHOR: end (D2-194..198 pending) -->
