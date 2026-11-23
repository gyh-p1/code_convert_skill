# 系统加载核对工具

## 1. 执行者、登记与边界

本页的加载工具及文本回归命令仅供系统维护侧执行。第三方智能体不得编写、生成、保存或运行辅助脚本，含内联程序和委托形式；以原生工具手工逐项调度、回读加载证据。登记分类器的有限调用例外由[分类准入](../references/workflow/classifier-agent-gate.md)单独规定，不受本页“加载工具仅维护侧执行”替代；也不能反过来用分类许可执行本页加载工具或任意仓库脚本。

登记组件为 `loading_preflight.py` 和其文本回归 `test_loading_preflight.py`；当前版本、验证状态及精确摘要见 [登记文件](loading-registration.json)。系统维护侧更新脚本后须重新回归、核对并更新登记摘要；待回归候选不冒称已验收，不自动信任所有 tools/ 文件。评估运行分类器的版本/SHA 和外部临时目录约束继续按准入契约；不可达仅转换不加载该契约或分类器。

工具只处理指定 Markdown、读取返回和本项加载依据，不运行样本或构建、不调用转换模型、不提交评估、不改 phase/lifecycle。所有 PASS 都仅在 `scope=loading-only` 或报告声明的结构范围内有效，不是安全、分类、冻结完成或功能许可。它是流程检查，未安装不可绕过的宿主 hook 或 Controller 门禁。

## 2. 系统侧安装与结构检查

Python 3.11+，依赖 [requirements-loading.txt](requirements-loading.txt)；可在联网维护环境安装，也可由系统分发离线 wheel。运行时不需要联网。测试沿用标准库 unittest，不建立样本运行框架。

```powershell
python -m pip install -r tools/requirements-loading.txt
python -B tools/loading_preflight.py check-repo --repo . --out <evidence>/structure-001.json
python -B -m unittest discover -s tools -p test_loading_preflight.py -v
```

根 SKILL 表是加载清单；程序内精确身份是验收约束，不是另一条知识入口。解析 CommonMark 加表格扩展，识别真实 Markdown 链接，代码块与行内代码不算链接。标题锚点采用已标明的 Unicode 类别规则：小写、保留字母/数字/组合符及 `-`/`_`、空格转 `-`、重复标题递增后缀；不声称兼容所有站点的 HTML 锚点。外部和范围外链接列为 skipped，不递归抓取，不用关键词检查自然语言语义。

首版（v1.0.1）精确范围为 12 份治理/工作流 Markdown。v1.1.0 起配合 [skills/routing-manifest.json](../skills/routing-manifest.json) 将 `check-repo` 与 `record-read` 扩展至**全库 76 份 Markdown**（3 个入口、7 份核心契约、2 份工作流、1 份共性导航、7 份语言页、42 个方向 + 2 份 `c-to-cpp` 子参考、4 个场景 + 1 份网络安全导航、5 个系统页、2 份专题）。含知识目录或清单引用的仓库缺失清单时报告 `manifest-missing`，`skills/` 下的 Markdown 须全部登记。Controller 适配及模型上下文注入由人工和专门契约约束。

## 3. 系统提供正文与关联真实返回

系统读取操作分两次调用，不能在一次调用中把尚未返回的正文标为已提供。先返回片段，待宿主保存该次返回后，再关联原件：

```powershell
python -B tools/loading_preflight.py record-read --emit --repo . --document references/framework/safety-boundary.md --start-line 1 --end-line 12 --out <evidence>/offer-001.json
python -B tools/loading_preflight.py record-read --offer <evidence>/offer-001.json --transcript <this-session-rollout.jsonl> --call-id <actual-call-id> --out <evidence>/receipt-001.json
```

第一条的 stdout 必须原样通过系统读取工具返回正文，不能重定向后只向智能体发送文件名或摘要。每次只返回一个片段，范围太大时先拆分，不设置会截断结果的展示预算。offer 保存精确 UTF-8 原字节快照（含 BOM/CRLF 身份），实际正文分片含行范围与字节范围。offer 只是材料准备成功，不能用于通过下一动作核对。

宿主日志支持 `codex-rollout-v1` 和 `generic-read-tool-v1`。前者要求 `exec`/`exec_command` 与同 `call_id` 的输出包含完整 offer payload。后者把 `read_file`/`Read`/`view_file` 的调用与工具输出配对，核对请求路径、行范围和最终返回的精确正文或完整行号序列。两类适配器检查结果记录、payload 外层和承载正文的结果容器中的 `truncated`/`is_truncated`/`isTruncated` 标志。参数回显、改写文本及标记为截断的结果无效。

v1.1.2 的 offer 记录选定工作树中文档的绝对路径 `documentPath`。通用读取调用须记录该绝对路径，或以调用参数中的绝对 `cwd`/`workdir` 解释相对路径。路径按生成 offer 的宿主格式精确匹配，另一工作树中的同路径后缀及同正文也不能提供本项读取证据。`check-next` 同时核对工作树内的当前文档路径及字节哈希。升级时保留旧通用读取原件，缺少 `documentPath` 的旧通用读取凭证不再作为当前 `reads` 的证据，须重新读取并生成凭证。历史 Codex marker 原件保留原有读取格式。

适配器保存调用/输出关联、日志前缀摘要、输出摘要和上下文标识，并在验证时回读原日志。日志可追加，已引用前缀保持原样。日志字段或路径身份无法核实时结果为 UNAVAILABLE，由系统维护侧适配。

证据等级 `HOST_RETURN_OBSERVED` 只表示该日志记录了正文提供，不是理解、持续保有、模型注入或防篡改认证。工具无法证明未被日志暴露的额外截断/上下文丢失；检测到 compacted/context_compacted/context_reset 时更换 epoch，重新提供所需正文，并在 `reads` 中保留已验证旧 epoch 历史凭证的同时追加覆盖全部必需范围的新 epoch 凭证（以当前 epoch 完整覆盖为准，记 `supersededReceipts` 而不因保留历史凭证误阻断）。历史/自填声明只能作为 manual 依据，不能通过修改 evidenceGrade 冒充系统证据。

## 4. 下一动作的加载核对

在既有 frozen-inputs.md 准备草稿或阶段记录内放一个 `loading-preflight` fenced block。它是加载依据片段，不是新增 state.json；起始阶段可用尚未记 FROZEN 的准备草稿。v1.1.0 在存在 `skills/routing-manifest.json` 时要求 `freeze` 及后续常规动作附带 `routing` 全维度闭集路由对象（`start`/`map` 前可先省略或仅在就绪时填写）；以下形制中的摘要、身份、适用事实和指针须替换为真实值：

````markdown
```loading-preflight
{
  "taskId": "actual-task",
  "runId": "actual-run",
  "context": {"sessionId": "actual-host-session", "epoch": 0},
  "workflows": {
    "batch": {"applies": false, "basis": "本请求只有一个任务"},
    "long-file": {"applies": false, "basis": "本项单文件<=700行且预期目标不膨胀超700行"}
  },
  "routing": {
    "direction": "python-to-cpp",
    "directionReferences": {},
    "scenes": {
      "network-io": {"applies": false, "basis": "无 socket/HTTP 调用"},
      "file-io": {"applies": false, "basis": "无真实文件 I/O 调用"},
      "process-execution": {"applies": false, "basis": "无子进程调用"},
      "concurrency": {"applies": false, "basis": "单线程顺序逻辑"}
    },
    "systems": {
      "posix-winsock": {"applies": false, "basis": "无 Winsock/POSIX socket API"},
      "posix-windows-filesystem": {"applies": false, "basis": "无平台底层文件 API"},
      "posix-windows-process-identity": {"applies": false, "basis": "无 fork/CreateProcess/令牌 API"},
      "posix-windows-threads": {"applies": false, "basis": "无 pthread/Win32 线程同步 API"},
      "windows-registry-service-subsystem": {"applies": false, "basis": "无注册表或 Windows 服务 API"}
    },
    "topics": {
      "security-behavior": {"applies": true, "basis": "含不可信 JSON 解码与深度校验"},
      "attack-tactic-index": {"applies": false, "basis": "不带战术标签"}
    }
  },
  "structure": {"path": "structure-001.json", "sha256": "actual-file-sha256"},
  "reads": [{"path": "receipt-001.json", "sha256": "actual-file-sha256"}]
}
```
````

指针相对该 Markdown 所在目录解析，也支持绝对路径。每个原件 SHA-256 必须与实际字节相符；reads 须覆盖全部必读契约、适用工作流、共性导航、源/目标两语言页、所选方向及其适用子参考、以及 `applies=true` 场景/系统/专题的全部行范围，可跨片段、可重叠，但不能缺中段或混用版本。工具核当前提供的仓库/只读快照与结构报告一致；已有 run 要继续旧正文时用原不可变仓库快照作为 `--repo`，不要拿当前工作树补改旧记录。

```powershell
python -B tools/loading_preflight.py check-next --repo . --record <run>/01-frozen/frozen-inputs.md --action freeze --transcript <this-session-rollout.jsonl> --source <source-file> --strict-signals --out <evidence>/next-freeze-001.json
```

`check-next` 支持可重复参数 `--source <path>` 与开关 `--strict-signals`：系统维护侧仅以只读文本扫描源码对照 `skills/routing-manifest.json` 的行数阈值与 `triggerSignals`，将疑似误标 `applies=false`（`SKIP`）的槽位记录在 `signalConflicts`；传 `--strict-signals` 时直接阻断（`FAIL`/退出码 1）。该扫描不编译、不导入、不执行源码。

动作名：start（画像前，批量含 batch）、map（建图/分段前，含适用 long-file）、freeze、classify、source-precheck、generate、review（自审/修订）、submit、resume、close。start 时 long-file 可尚未加载；源码复杂度待画像确定时可用 applies=null 并说明待定依据，map/freeze 及后续动作前必须定案，适用则需要完整正文。报告不检查其他冻结字段；Agent 仍须按任务状态 §2.2 回读冻结正文并核全部字段。写 result.md 和保留停止原因不以加载 PASS 为前置条件；close 只核加载记录，不代替全去向交付及终态判据。

### 4.1 可达与不可达两条路径的加载动作

两条路径先加载 task-state、safety、delivery、build、evaluation、loop 六份通用契约及实际适用的 batch/long-file 工作流；v1.1.0 起同时经 `routing` 闭集检查语言、方向（及子参考）、场景、系统与专题知识覆盖。连接坐标与健康检查正文在检查前读取；确认可达后、冻结前才补分类准入及评估适配。不可达仅转换不加载分类准入或分类器、不执行分类、不要求分类产物；build 契约仍用于声明平台/依赖和待验证计划，不要求本轮有构建原件。Controller 适配及模型注入仍在本工具覆盖外，由 Agent 与专门契约约束。

| 本轮路径 | 调用既有加载动作的时点 | 不要求的动作/原件 |
|---|---|---|
| 可达正常流程 | `start` 后按已加载连接适配检查可达性；长文件建图前 `map`；随后 `freeze`、`classify`、`source-precheck`、`generate`、`review`、适用 `submit`、`close`，恢复新增动作前 `resume` | 不要求未发生的额外修复或 job；LIB 分支的行为件按评估准备契约不适用 |
| 不可达仅转换 | `start`/适用 `map`、`freeze`，直接 `generate`、`review` 和 `close`；恢复前 `resume`，重新检查可达性后决定后续适用动作 | 不调用 `classify`/`source-precheck`/`submit`，不要求分类准入正文、分类输入/结果或源构建/job/比较原件；仍必须有自审及 result.md |

`check-next` 按动作核加载范围：`classify`、`source-precheck`、`submit` 要求七份（含分类准入）；其他非恢复例外动作只要求六份通用契约及适用工作流，并自 `freeze` 起（及 `map` 已填写时）强制核全维度 `routing` 闭集知识覆盖。结构检查仍保留完整七契约与全知识清单，不能把“路径已登记”当分类或知识正文已加载。工具不判断网络分支，不消费分类/job 结果，不要求此前调用顺序，也不添加 evaluationMode 开关；每次 PASS 仅为 `loading-only`、`executionAuthorized=false`。可达分支生成前的分类及源预检仍由 Agent 按根入口核真实原件，加载 PASS 不能代替它们。业务分流及交付按评估准备 §1.0 和[交付骨架](../references/framework/delivery-handoff-contract.md#2111-不可达仅转换的产物骨架)。缺适用契约、工作流、知识、版本或时序仍失败。

默认检查当前日志末尾的前置条件。审计已发生动作时传 `--before-call <actual-action-call-id>`，只采信该动作之前的正文返回；补读不能追认历史合规。系统在每次动作前保存本次 next 原件并由 Agent 核对引用；未留历史检查原件时，当前 PASS 不能外推此前动作已合规。跨来源顺序不可比较时不合并，跨会话或已知 epoch 变化须重新提供。

query/collect/terminate/cleanup 是已发生 job 的加载缺件例外：可不提供 record/transcript，工具返回 exception，同时 `executionAuthorized=false`；这只说明加载缺件不阻止查询取证/终止清理，操作仍按原 job、授权和安全契约执行。

## 5. 原件、失败与人工回退

输出采用同卷临时文件写完后原子发布且禁止覆盖已有路径；系统使用新编号/唯一身份，批次共享件放既有批次位置，单项件放 01-frozen/。写入失败返回 UNAVAILABLE，不假装落盘成功。失败 finding 保留原文，不覆盖旧证据；冻结/阶段记录和 result.md 引用原件。

纳入 Git 的证据目录须设置 `-text` 保持精确字节，避免 checkout 换行转换使原件摘要失效；本次验收目录已设置。登记脚本与依赖清单固定 LF。运行时始终以实际字节核对，不能在摘要失败后静默归一化放行。

退出码 0：本次记录或限定范围检查成功；1：已知结构/覆盖/版本/时序缺项；2：用法、证据格式、读取/解析能力或输出保存不可用。结构报告内的已知文件缺失按 FAIL 记录；缺宿主日志不能生成强读取凭证。记录成功不等于完整加载。

无系统加载接入或新候选待系统维护侧回归时，第三方智能体用原生读取工具手工核同范围：根表身份、路径/锚点和路由，六份通用契约、可达分支适用的分类准入及工作流正文、精确版本、分段覆盖、消费时点和缺口。手工核对完整即可保存 manual 依据并继续核其余门禁；系统强证据不可用不等于手工加载未完成。实际正文/核对仍缺失才停止受影响新增动作；人工记录不升级为 HOST_RETURN_OBSERVED。加载回退不省略可达分支的分类/源构建/评估，不可达仅转换按[评估准备 §1.0](../references/framework/evaluation-readiness-contract.md#10-转换前可达性检查与仅转换分支)留证且分类不适用；加载工具不检查网络或决定分支。

本工具及其回归与示例属于系统维护设施，所有测试输入均为文本 fixture；不得将说明中的系统命令作为第三方智能体辅助脚本许可。
