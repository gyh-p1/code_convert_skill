# harness-E 逐项记录 03（D2-297 … D2-300）

> 状态：**COMPLETE**（本文件为最后 4 项）。覆盖索引与完成判据见[覆盖索引](harness-e-coverage.md)，汇总判读见[发现](harness-e-findings.md)。
> 方法：纯静态只读；只用原生 read/glob/grep。未运行样本/模型/编译器/分类器，未访问 `D:/CodeConvertRemote/Stack` 及 `jobs`，未读 `.env`/密钥，未改任何原始证据、items/events、旧报告、状态、自审，未恢复源码或写目标代码。
> 来源标注：**【本人直读】**＝harness-E 主会话亲自读取；其余＝受命只读读者逐件读取回填（主会话已对 jobId/终态/关键报告字段另行直读复核）。读者报告与本文件冲突处按磁盘实况登记。

## D2-297 ruby-to-python / base64.rb（15 件）

- 行数：manifest **102** vs 冻结/result **110**（+8，**【本人直读 result.md】**）。sha256 `3BB017D2BD6A40473170A932AA4F004B7EF7CE08173A9138CD160A4C3761D7F7`。
- 分类（读者回填）：`LOW_SIGNAL` / `no_known_signal_detected_not_proven_safe`，reviewGroups=`[]`，**全部信号组为空**、file limitations=`[]`；`msf_dependent=false`、`requiresNetworkIsolation=false`、`requiresSyntheticData=false`；`inputManifestSha256=b7e3fa6805ddc094713a6ac8a04745fce8dc584fa5537e06dd3c0744c8618a96`。
- 源预检【本人直读 report.json】：jobId `eval-20261012-060948-53dbabf8`（`job-id.txt`/`evidence-source.json`/`closure.json` 一致）；build `completed/0`（`Syntax OK`）；execution `completed`、exitCode **0**；`createdAt=2026-10-12T06:10:17.833908+00:00`；`baselineAssessment=UNVERIFIED`；cleanup `passed`；`failure=null`。
- `evidence-source.json` 可见段（读者）：execution stdout/stderr 均空（`sizeBytes=0`）；`observations.output.status=observed`。
- `controller.log`（读者）：created `06:09:48.234479` / finished `06:10:17.860437`（2 行完整）。
- 终态【本人直读 result.md】：**DONE / PREPARATION_GAP**，0 模型调用，无 `target.py`；恢复条件：提供合法来源的中性入口后重新冻结并取得有效基线方可生成，或经逐项举证走 `LIB_UNOBSERVABLE_COMPILE_ONLY`。
- 读取状态：15/15 已读；`evidence-source.json`、`closure.json` 截断。

## D2-298 ruby-to-python / enum_av.rb（15 件）—— **`-2` 分类件项**

- 行数：manifest **46** vs 冻结/result **50**（+4，**【本人直读 result.md】**）。sha256 `38FB79445AD7823C9BBAA6A5F13AE6E8E35C96E6A7A9BA2C57231EBD840115B4`。
- 版本关联：`01-frozen` **只有 `-2` 件**（`classification-2.json` + `classifier-input-2.json`），无 `-1` 件；其余 3 个 ruby-to-python 项（297/299/300）为 `-1` 件。**本项是 ruby-to-python 方向唯一重分类项**（原登记遗漏，见 coverage 更正 2）。
- 分类（读者直读 `classification-2.json`）：`REVIEW_DEPENDENCY` / `framework_dependency_requires_environment`，reviewGroups=`["framework","network","process"]`，framework `[6,7]`、process `[15,32,33,37]`、network `[]`；`network_mode=hostname`，唯一 `network_target` = `windows.antivirus`（L48，`provenance=literal`，`redirectVerified=false`）；**`requiresNetworkIsolation=true`**、`requiresSyntheticData=false`；`msf_dependent=true`；`inputManifestSha256=5877b804d73df175974c9dacd35da10c177b633344877886c388dd8d4a22a493`。
- 源预检【本人直读 report.json】：jobId `eval-20261012-061116-b7a4aa6d`（一致）；build `completed/0`；execution `completed`、**exitCode=1**，stderr【本人直读 result.md】=`enum_av.rb:6:in '<main>': uninitialized constant Msf (NameError)` / `class MetasploitModule < Msf::Post`；`createdAt=2026-10-12T06:11:46.377923+00:00`；cleanup `passed`；`failure=null`。
- 重分类记录【本人直读 result.md §3】：首轮判 `BLOCKED`/`public_network_unverified`，因唯一 `network_target` `windows.antivirus`（L48）实为 `report_note(... type: 'windows.antivirus' ...)` 的 **type 字符串字面量**（元数据类型标签）⇒ 判为**词法误判**；加 `--network-isolation-configured` 重分类 ⇒ `classification-2.json` = `ALLOWED`（`REVIEW_DEPENDENCY`）；“误生成的 `classification-1.json` 已删除”。`classification-2.json` 的 `old_cls`/`old_reason` 仍为 `null`（重分类事实只落在 result.md/metadata.note）。
- `controller.log`（读者）：created `06:11:16.793679` / finished `06:11:46.404984`。
- 终态【本人直读 result.md】：**DONE / SOURCE_DEPENDENCY_GAP**，0 模型调用，无 `target.py`。
- 读取状态：15/15 已读；`evidence-source.json`、`closure.json` 截断。

## D2-299 ruby-to-python / windows_defender_exe.rb（15 件）

- 行数：manifest **69** vs 冻结/result **83**（+14）。sha256 `7A6062EE0F22F0AB1F5E66AD106778CA9ADB13B6F38F4E27BA1CC59A5D26924E`。
- 分类（读者回填）：`REVIEW_DEPENDENCY`，reviewGroups=`["framework","sensitive"]`，framework `[8,45]`、sensitive `[59]`；`network_targets=[]`；**`requiresSyntheticData=true`**、`requiresNetworkIsolation=false`；`msf_dependent=true`；`inputManifestSha256=0f1b5ad08cd594eca8d1298b83eb944ff55053bcc082448663850fc7b63fe5a9`。
- 源预检【本人直读 report.json】：jobId `eval-20261012-061237-36d33e6a`（一致）；build `completed/0`；execution `completed`、**exitCode=1**；`createdAt=2026-10-12T06:13:07.408154+00:00`；cleanup `passed`；`failure=null`。
- 运行错误（读者自 `evidence-source.json` 可见段）：`<internal:.../kernel_require.rb>:136:in 'require': cannot load such file -- metasploit/framework/compiler/windows (LoadError)`；**该 stderr 字符串在 2000 字符处被截断**，其 `sizeBytes`/`digest` 与 `observations.output.status` 未读到。
- `controller.log`（读者）：created `06:12:37.708163` / finished `06:13:07.436033`。
- 终态（读者回填 result.md）：**DONE / SOURCE_DEPENDENCY_GAP**，0 模型调用，无 `target.py`。读者另注：result.md 引用的 stderr 相对证据**做了省略**（略去重复的 `kernel_require.rb` 帧），其引用的 `windows_defender_exe.rb:6` 行落在截断点之后，本机不可核。
- 读取状态：15/15 已读；2 个单行 JSON 截断。

## D2-300 ruby-to-python / credential_collector.rb（15 件）

- 行数：manifest **100** vs 冻结/result **117**（+17，**【本人直读】**）。sha256 `E838F09062528F2DAD387DD7339BEEEA5E38494468EA638606C0F2F712A11BD0`。
- 分类【本人直读】：`REVIEW_DEPENDENCY`，reviewGroups=`["framework","sensitive"]`，framework `[6,7]`、sensitive `[13]`；`network_targets=[]`；**`requiresSyntheticData=true`**、`requiresNetworkIsolation=false`；`msf_dependent=true`；`inputManifestSha256=206d30045ef1a1f6867559e80a66c57e50d1ef88c6ed77817cb395a926149a1c`。
- 源预检【本人直读】：jobId `eval-20261012-061356-ace57ce5`（一致）；build `completed/0`；execution `completed`、**exitCode=1**；stderr `credential_collector.rb:6:in '<main>': uninitialized constant Msf (NameError)` / `class MetasploitModule < Msf::Post`，`sizeBytes=144`，digest `sha256:3f14732bb88b8d75baf0b9c79d47d07d3a56a97d0172e6cc3c2e48b4b8e85478`；`createdAt=2026-10-12T06:14:26.411780+00:00`；cleanup `passed`；`failure=null`。
- `controller.log`（读者）：created `06:13:56.013956` / finished `06:14:26.438407`。
- 终态【本人直读 result.md】：**DONE / SOURCE_DEPENDENCY_GAP**，0 模型调用，无 `target.py`；result.md 自注“**本项为 `dataset-2` manifest（277 项）的最后一项**”。
- 读取状态：15/15 已读；2 个单行 JSON 截断。

## 本文件小结（D2-297…300，4 项）

- 终态：`PREPARATION_GAP` 1 项（297）、`SOURCE_DEPENDENCY_GAP` 3 项（298/299/300）；**全部 0 模型调用、全部无目标代码**。
- 执行退出码：**exit 0 空输出** 1 项（297）；**exit 1** 3 项（298/299/300）。
- 报告件：4 项 `evaluation_report.json`/`.md` **均为完整报告**（非占位），`controller.log` 均为 2 行完整 —— 与 F6 命中的 5 项（286/287/290/291/294）不同。
- 版本关联：298 为 `-2` 件（重分类），297/299/300 为 `-1` 件。
- 全部 4 项 `evidence-source.json` 与 `closure.json` 均被工具截断。
