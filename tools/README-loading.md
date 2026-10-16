# 系统加载核对工具

## 1. 执行者、登记与边界

本页命令仅供转换系统维护侧执行。第三方智能体加载本 Skill 后仍不得编写、生成、保存或运行辅助脚本，含 Python/PowerShell/JavaScript 内联程序和委托生成形式；只能通过原生工具手工、串行、逐项调度，读取、核对和引用系统提供的结果。把工具放在仓库中不构成第三方智能体执行许可。

登记组件为 `loading_preflight.py` 1.0.0 和其文本回归 `test_loading_preflight.py`；精确摘要见 [登记文件](loading-registration.json)。系统维护侧更新脚本后须重新回归、核对并更新登记摘要，不自动信任所有 tools/ 文件。原安全分类器的版本/SHA 和外部临时目录约束继续按[准入契约](../references/workflow/classifier-agent-gate.md)，加载工具不修改它。

工具只处理指定 Markdown、读取返回和本项加载依据，不运行样本或构建、不调用转换模型、不提交评估、不改 phase/lifecycle。所有 PASS 都仅在 `scope=loading-only` 或报告声明的结构范围内有效，不是安全、分类、冻结完成或功能许可。它是流程检查，未安装不可绕过的宿主 hook 或 Controller 门禁。

## 2. 系统侧安装与结构检查

Python 3.11+，依赖 [requirements-loading.txt](requirements-loading.txt)；可在联网维护环境安装，也可由系统分发离线 wheel。运行时不需要联网。测试沿用标准库 unittest，不建立样本运行框架。

```powershell
python -m pip install -r tools/requirements-loading.txt
python -B tools/loading_preflight.py check-repo --repo . --out <evidence>/structure-001.json
python -B -m unittest discover -s tools -p test_loading_preflight.py -v
```

根 SKILL 表是加载清单；程序内精确身份是验收约束，不是另一条知识入口。解析 CommonMark 加表格扩展，识别真实 Markdown 链接，代码块与行内代码不算链接。标题锚点采用已标明的 Unicode 类别规则：小写、保留字母/数字/组合符及 `-`/`_`、空格转 `-`、重复标题递增后缀；不声称兼容所有站点的 HTML 锚点。外部和范围外链接列为 skipped，不递归抓取，不用关键词检查自然语言语义。

首版精确范围为发现/AGENTS/根三个入口、7 份契约、两个条件工作流，共 12 份 Markdown。语言、方向、场景、系统、Controller 和模型注入不在本工具覆盖内，其原有加载义务继续生效。

## 3. 系统提供正文与关联真实返回

系统读取操作分两次调用，不能在一次调用中把尚未返回的正文标为已提供。先返回片段，待宿主保存该次返回后，再关联原件：

```powershell
python -B tools/loading_preflight.py record-read --emit --repo . --document references/framework/safety-boundary.md --start-line 1 --end-line 12 --out <evidence>/offer-001.json
python -B tools/loading_preflight.py record-read --offer <evidence>/offer-001.json --transcript <this-session-rollout.jsonl> --call-id <actual-call-id> --out <evidence>/receipt-001.json
```

第一条的 stdout 必须原样通过系统读取工具返回正文，不能重定向后只向智能体发送文件名或摘要。每次只返回一个片段，范围太大时先拆分，不设置会截断结果的展示预算。offer 保存精确 UTF-8 原字节快照（含 BOM/CRLF 身份），实际正文分片含行范围与字节范围。offer 只是材料准备成功，不能用于通过下一动作核对。

第二条仅支持实际验证过的 Codex JSONL 返回适配：`session_meta`、`response_item` 中的 exec/exec_command call 与同 call_id 的 output；支持实际返回对象的 text/content/output 包装。适配器确认最终日志内含完整、精确的片段 JSON，不接受调用参数里的正文、后台文件、部分 JSON 或自填 complete。保存调用/输出关联、日志前缀摘要、输出摘要和上下文标识，验证时回读原日志；日志可追加，已引用前缀不得改变。现场 log 字段变化或其他宿主返回形制不明时结果为 UNAVAILABLE，需维护侧适配，第三方智能体不编写脚本补接口。

证据等级 `HOST_RETURN_OBSERVED` 只表示该日志记录了正文提供，不是理解、持续保有、模型注入或防篡改认证。工具无法证明未被日志暴露的额外截断/上下文丢失；检测到 compacted/context_compacted/context_reset 时更换 epoch，重新提供所需正文。历史/自填声明只能作为 manual 依据，不能通过修改 evidenceGrade 冒充系统证据。

## 4. 下一动作的加载核对

在既有 frozen-inputs.md 准备草稿或阶段记录内放一个 `loading-preflight` fenced block。它是加载依据片段，不是新增 state.json；起始阶段可用尚未记 FROZEN 的准备草稿。以下是形制示例，摘要、身份、适用事实和指针须替换为真实值：

````markdown
```loading-preflight
{
  "taskId": "actual-task",
  "runId": "actual-run",
  "context": {"sessionId": "actual-host-session", "epoch": 0},
  "workflows": {
    "batch": {"applies": false, "basis": "本请求只有一个任务"},
    "long-file": {"applies": false, "basis": "本项单文件短且无跨单元复杂依赖"}
  },
  "structure": {"path": "structure-001.json", "sha256": "actual-file-sha256"},
  "reads": [{"path": "receipt-001.json", "sha256": "actual-file-sha256"}]
}
```
````

指针相对该 Markdown 所在目录解析，也支持绝对路径。每个原件 SHA-256 必须与实际字节相符；reads 须覆盖适用正文全部范围，可跨片段、可重叠，但不能缺中段或混用版本。工具核当前提供的仓库/只读快照与结构报告一致；已有 run 要继续旧正文时用原不可变仓库快照作为 `--repo`，不要拿当前工作树补改旧记录。

```powershell
python -B tools/loading_preflight.py check-next --repo . --record <run>/01-frozen/frozen-inputs.md --action freeze --transcript <this-session-rollout.jsonl> --out <evidence>/next-freeze-001.json
```

动作名：start（画像前，批量含 batch）、map（建图/分段前，含适用 long-file）、freeze、classify、source-precheck、generate、review（自审/修订）、submit、resume、close。start 时 long-file 可尚未加载；源码复杂度待画像确定时可用 applies=null 并说明待定依据，map/freeze 及后续动作前必须定案，适用则需要完整正文。报告不检查其他冻结字段；Agent 仍须按任务状态 §2.2 回读冻结正文并核全部字段。写 result.md 和保留停止原因不以加载 PASS 为前置条件；close 只核加载记录，不代替全去向交付及终态判据。

### 4.1 可达与不可达两条路径的加载动作

两条路径都先加载同一组 7 份核心契约及实际适用的 batch/long-file 工作流。不可达改变编译运行步骤的适用性，不减少冻结、分类、模型/知识、自审与交付规则的读取；build 契约仍用于声明平台/依赖和待验证计划，不要求本轮有构建原件。Controller 连接适配在健康检查前读取；现场平台/runner 证据仅在后续正常评估动作适用时核。Controller/语言/方向/场景/系统仍在本工具覆盖外，由 Agent 按根入口手工加载和留依据。

| 本轮路径 | 调用既有加载动作的时点 | 不要求的动作/原件 |
|---|---|---|
| 可达正常流程 | `start` 后按已加载连接适配检查可达性；长文件建图前 `map`；随后 `freeze`、`classify`、`source-precheck`、`generate`、`review`、适用 `submit`、`close`，恢复新增动作前 `resume` | 不要求未发生的额外修复或 job；LIB 分支的行为件按评估准备契约不适用 |
| 不可达仅转换 | 同样 `start`/适用 `map`、`freeze`、`classify`，再直接 `generate`、`review` 和 `close`；恢复前 `resume`，重新检查可达性后决定后续适用动作 | 不调用本轮未发生的 `source-precheck`/`submit`，不提供源构建/job/比较原件；仍必须有自审及 result.md |

`check-next` 不要求先调用过某个动作，不消费源预检/分类/job 结果或网络诊断，不根据任意 `evaluationMode` 声明放宽正文覆盖；每次 PASS 仅表示该动作的加载条件满足，`executionAuthorized=false`。因此无需给加载记录增加不可达开关，不新增网络探测或自动跳步功能。业务分流及其证据由评估准备 §1.0 和 Agent 手工核对，产物按[交付骨架](../references/framework/delivery-handoff-contract.md#2111-不可达仅转换的产物骨架)。缺必要契约、工作流、版本或时序仍失败，不能借不可达免加载。

默认检查当前日志末尾的前置条件。审计已发生动作时传 `--before-call <actual-action-call-id>`，只采信该动作之前的正文返回；补读不能追认历史合规。系统在每次动作前保存本次 next 原件并由 Agent 核对引用；未留历史检查原件时，当前 PASS 不能外推此前动作已合规。跨来源顺序不可比较时不合并，跨会话或已知 epoch 变化须重新提供。

query/collect/terminate/cleanup 是已发生 job 的加载缺件例外：可不提供 record/transcript，工具返回 exception，同时 `executionAuthorized=false`；这只说明加载缺件不阻止查询取证/终止清理，操作仍按原 job、授权和安全契约执行。

## 5. 原件、失败与人工回退

输出采用同卷临时文件写完后原子发布且禁止覆盖已有路径；系统使用新编号/唯一身份，批次共享件放既有批次位置，单项件放 01-frozen/。写入失败返回 UNAVAILABLE，不假装落盘成功。失败 finding 保留原文，不覆盖旧证据；冻结/阶段记录和 result.md 引用原件。

纳入 Git 的证据目录须设置 `-text` 保持精确字节，避免 checkout 换行转换使原件摘要失效；本次验收目录已设置。登记脚本与依赖清单固定 LF。运行时始终以实际字节核对，不能在摘要失败后静默归一化放行。

退出码 0：本次记录或限定范围检查成功；1：已知结构/覆盖/版本/时序缺项；2：用法、证据格式、读取/解析能力或输出保存不可用。结构报告内的已知文件缺失按 FAIL 记录；缺宿主日志不能生成强读取凭证。记录成功不等于完整加载。

无系统接入时第三方智能体用原生读取工具手工核同范围：根表身份、路径/锚点和路由，7 份及适用工作流正文、精确版本、分段覆盖、消费时点和缺口。保存 `manual` 说明及实际工具依据，未完成则 UNAVAILABLE；人工记录不升级为 HOST_RETURN_OBSERVED。自填声明不证明理解或独立提供。加载回退不省略适用分类/源构建/评估门禁；第三方评估系统不可达的仅转换分支独立按[评估准备 §1.0](../references/framework/evaluation-readiness-contract.md#10-转换前可达性检查与仅转换分支)留证和分流，加载工具不检查网络或决定该分支。

本工具及其回归与示例属于系统维护设施，所有测试输入均为文本 fixture；不得将说明中的系统命令作为第三方智能体辅助脚本许可。
