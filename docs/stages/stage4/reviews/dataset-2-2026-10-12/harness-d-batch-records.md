# Harness D — batch 层原始材料记录（只读审阅）

> 状态：**COMPLETE**（本文件覆盖 `batch/` 全部文本原件；`items/*.json` 全 277 份已由本会话另派的两个只读子会话逐件读完并与 `summary.md §11` 核对吻合，见 [coverage](harness-d-coverage.md) §3.1）。
> 审阅对象：`docs/dataset-2/dataset-2-copy/batch/` 下的**全部原始文本材料**（不含本轮新建的 `current-system-review-2026-10-12/` 审查件，也不含非文本 `capsule.zip`）。
> 口径：**原始事实 / 历史说明 / 当前规则 / 未知**分开记；不改原账、不重算、不用脚本。

---

## 一、批次身份与状态快照（原始事实）

### 1.1 身份件

| 件 | 事实 | 备注 |
|---|---|---|
| `batch.json` | batchId `batch`；intakeId `intake-dataset-2-2026-10-10`；`manifestRows=277`；`rawItems{total:277,received:277,unreadable:0,hashMismatch:0}`；model `deepseek-flash` temp 0.2、`maxTokensFieldSent=false`、`rag=off`；预算 `selfRepair≤2`、`postEvalRepairTotal≤2`；`pollingIntervalSeconds=15`；`createdAt=2026-10-10` | `datasetRoot`/`manifest` 写 `docs/test/dataset-2`，与本副本实际路径不一致；`manifestSha256=null` |
| `batch-authorization.json`（根） | 授权人 `gyh-p1`，`authorizedAt=2026-10-10T14:43:00Z`，`validUntil=2026-10-17T14:43:00Z`；vmIsolation 三项 true；networkIsolation 四项 true；`contractHash=sha256:a9ed1445…d82e` | `dataSource.confirmation` 写“该项 **D2-088**…” |
| `batch-authorization.json`（各用例内副本） | 与根件**逐字不同**：confirmation 写“该项 D2-197 / D2-241…”；`contractHash=sha256:8090cfcc…4aac` | 全案 34 项目内副本一致用 `8090cfcc…`；根件用 `a9ed1445…` — **两个 contractHash 并存** |

### 1.2 状态快照随时间（原始事实，均取自文件自身声明）

| 时点/件 | 已建 items | 终态(DONE+PARTIAL) | WAITING | events 行数 | 出处 |
|---|---:|---:|---:|---:|---|
| reconciliation-1（2026-10-10） | 45 已触及 | 40 | 5 | 202 | `reconciliation-1.md §1–2` |
| reconciliation-2（2026-10-11） | 104 已触及 | 80 | 24 | 434 | `reconciliation-2.md §1–2` |
| reconciliation-3（2026-10-11） | 149 已触及 | 120 | 29 | 684 / 150 ids | `reconciliation-3.md §1–2` |
| reconciliation-4（2026-10-11） | 190 已触及 | 160 | 30 | 830 / 191 ids | `reconciliation-4.md §1–2` |
| reconciliation-5（2026-10-12） | 231 已触及 | 200 | 31 | 990 / 231 ids | `reconciliation-5.md §1–2` |
| reconciliation-6（2026-10-12） | **277 全部** | **246** | 31 | **1145 / 277 ids** | `reconciliation-6.md §1–2` |
| `summary.md §4–§5`（更早草稿） | 112 | 88 | 24 | — | `summary.md §4/§5` |
| `summary.md §11`（收尾快照 2026-10-12） | **277** | **246** | 31 | 1145 / 277 ids | `summary.md §11.1` |
| **`events.jsonl` 实测（本会话）** | — | — | — | **1148 行** | `read` 报 total=1148；末 3 行为 `D2-007` REOPEN/NOTE（2026-10-12） |

`summary.md §11.1` 的 lifecycle/disposition：

- lifecycle `{"DONE":226, "PARTIAL":20, "WAITING":31, "ACTIVE":0}`（终态 246）
- disposition `{"CONVERTED":60, "SOURCE_DEPENDENCY_GAP":88, "SOURCE_NOT_BUILDABLE":22, "PREPARATION_GAP":38, "BLOCKED":4, "BLOCKED_ENV":1, "FROZEN":64}`（合计 277）

### 1.3 唯一 taskId 统计（手工核对，不重算）

- `items/` 现存 **277** 份（`glob batch/items/*` 实测 "277 paths"），与 manifest 277 行一致。
- `events.jsonl` 的 taskId 除 D2-* 外，还有 **1 个非 manifest 标识 `PLATFORM-PROBE`**（C# 目标平台探针，`events.jsonl:634`）。
  ⇒ 事件流的 distinct taskId = 277（D2-*）+ 1（PLATFORM-PROBE）= **278**。
- 对账口径变化（**需注意**）：
  - #3/#4/#5 把 `PLATFORM-PROBE` 明确列为 “events-only(1) 非缺口”；
  - #6 改为“宽松模式下（只匹配 `"taskId"\s*:\s*"D2-NNN"`）双向差集归零”，`PLATFORM-PROBE` 因此不再出现在差集里。
  - ⇒ **“差集归零”是 D2-* 过滤后的结论**，不是“事件流里没有非 manifest 标识”。
- 行内写法不一致（原始事实）：#5 记 `events.jsonl` 存在 `"taskId": "D2-xxx"`(295) 与 `"taskId":"D2-xxx"`(693) 两种空格写法；#6 与本会话读到的行同样两种写法并存。

### 1.4 编号缺口（原始事实）

- 数据集 `README.md §5.2`：**23 项已移除、编号保留不再使用**——D2-113、214、215、216、218、219、220、221、223、224、225、226、227、228、229、230、231、234、237、**242**、**244**、**248**（22 项“杀软拦截读回”）+ D2-026（无源码）。
- 本会话独占区间内的缺口即 **D2-242 / D2-244 / D2-248**。
- `optimization-inputs-2.md §0.1` 亦称这些编号“无 item 文件（manifest 编号缺口，非本任务遗漏）”。

---

## 二、全部增量对账与遗留项是否带入（逐轮核对）

| 轮 | 触发 | 本轮结论 | 遗留项是否带入下一轮 | 依据 |
|---|---|---|---|---|
| #1 | 终态 40 | 双向差集 0；17 项无自审属设计使然；D2-029 归因更正 | ✅ §8 列 D2-007/055/069/082/083/066/029；§7 新增纪律 §10.9–§10.18 | `reconciliation-1.md §6–§8` |
| #2 | 终态 80 | 发现 `D2-088` 有 item 无事件 ⇒ 追加 `BACKFILLED_EVENT`（`events.jsonl:435`） | ✅ §6.1/§6.2/§6.3 全部带出（含 D2-074 新增、D2-088 待下轮确认） | `reconciliation-2.md §3/§6` |
| #3 | 终态 120 | 转换项双向差集归零；`D2-088` 缺口闭合；C# 目标缺陷平台侧修复 ⇒ 21 项具备重开条件 | ✅ §6.1（21 项待重开）/§6.2（6 项 WAITING）/§6.3（3 项评估不可就绪）带出；并注明 #2 的 D2-066/072/089/090/094/098/099 已收口 | `reconciliation-3.md §3/§6` |
| #4 | 终态 160 | 差集维持 0；7 个方向收口 | ✅ §6.1（新增 D2-184 真实公网）/§6.2（21 项待重开）/§6.3（D2-069/082/108/167/169/175）带出 | `reconciliation-4.md §6` |
| #5 | 终态 200 | 差集维持 0；新增 `D2-247`/`D2-254` 两个 matched | ✅ §7 明列：未触及 46 项、WAITING 31 项、D2-247/254 覆盖边界 | `reconciliation-5.md §7` |
| #6 | 终态 240 | 全批 277/277；差集 0 | ✅ §6 明列 WAITING 31 项全名单与 D2-247/256/269/270 覆盖边界 | `reconciliation-6.md §6` |

**带入性结论（原始事实）**：六轮均**显式**把上一轮未决项写进“带进下一轮/遗留项”小节，并保留原判定不改写（D2-029 的更正以追加方式记录）。
**未带入/降级的点（原始事实）**：
1. `#2 §6.2` 列的 7 项“评估不可就绪”在 `#3 §6.3` 只剩 3 项，其余 4 项（D2-066/072/089/090 等）以“已收口为 PARTIAL”一句话带过，**未逐项给收口证据指针**（`reconciliation-3.md §6` 末尾注）。
2. `#5 §7` 留“未触及 46 项 = D2-255~D2-300”，但 `#6` 覆盖的是 D2-255~D2-294（40 项窗口），D2-295~D2-300 的终态落在 `#6` 之后（`events.jsonl:1127–1145`），**#6 的“本段（200→240）”表内不含它们**；`summary.md §11` 把它们计入全批 246。属**窗口错位**而非漏登。

---

## 三、失败模型 attempt 与 items↔events 差集

### 3.1 事件流/文件层可确认的失败与异常 attempt（原始事实）

| taskId | 失败/异常形态 | 证据 | 是否改写历史 |
|---|---|---|---|
| D2-045 | 生成 attempt-1 `finish_reason=length`（completion 65533 / reasoning 62810）⇒ `attempt-1-truncated.raw.json`，attempt-2 成功 | `events.jsonl:534,535` | 保留 |
| D2-247（本区间） | `self-review-2` attempt-1 `finish_reason=length`（reasoning 65536 tok、content 空）⇒ `self-review-2.attempt-1-truncated.json`，聚焦重试成功 | `events.jsonl:958`；`README.md` D2-247 条 | 保留 |
| D2-121/122/150/191/235/236/241/246/252/253/256/275/287/292/293/298 | 分类器词法误判 ⇒ 加 `--network-isolation-configured` 重分类 | `events.jsonl:691,694,802,825,920,924,937,947,972,976,994,1063,1100,1116,1120,1136` | 追加 `classification-2`；`classification-1` 已删 |
| D2-114/021/140 | 提交/分类输入缺陷（陈旧分类件 403；小写哈希 input_error；字段偏移取错 sha） | `events.jsonl:660,225,226,772` | 保留原拒绝 |
| D2-151 | 首提 403 `identity_mismatch`（caseId 带前缀） | `events.jsonl:239` | 另记 job |
| D2-053 | 误用 D2-052 驱动 ⇒ 源树变化 ⇒ 403，重分类后 202 | `events.jsonl:571` | 追加 |
| D2-061/062/111/186/109/116 | 装置故障（驱动 `\n` 真换行 / 未定义 `SIDE` / `csc` 缺失 / 打包链断裂） | `events.jsonl:607,612,650,811,640,666` | 另记新 job，原记录保留 |
| D2-197 | 首提 `buildCommand` 整串 ⇒ `[Errno 2]`、inconclusive、7ms | `events.jsonl:847` | 另记 job-00b |
| D2-254 | 首提 job-01 target exec exit 150（runner 有 SDK 10.0.112、无 .NET 8 runtime）⇒ job-02 加 `RollForward=LatestMajor` | `events.jsonl:988,989` | 另记 job-02 |
| D2-210 | 先 `PAUSED(ACTIVE)`，后 `BASELINE` 失败 ⇒ `PREPARATION_GAP` | `events.jsonl:896,915,916` | 追加 supersede |

> 说明：`optimization-inputs-2.md §4.4` 称“`events.jsonl` 有 2 行自身不可解析（`:650` 含换行、`:915` 含未转义反斜杠路径）”。本会话手工核对：**`:915` 确含未转义反斜杠**（`'C:\Users\zj213\AppData\Local\Apps\2.0'`，单反斜杠 ⇒ 非法 JSON 转义）；**`:650` 在 `read` 输出中为单一物理行**，其 `\n` 呈现为转义序列，未观察到裸换行 ⇒ 该半句缺独立证据（见 findings）。

### 3.2 items ↔ events 双向差集（各轮声明 vs 原始事实）

| 轮 | events-only | items-only | 处置 |
|---|---|---|---|
| #1 | 0 | 0 | — |
| #2 | 0 | **1（D2-088）** | 追加 `BACKFILLED_EVENT`（`:435`） |
| #3 | 1（`PLATFORM-PROBE`，非转换项） | 0 | 判非缺口 |
| #4 | 1（同上） | 0 | 判非缺口 |
| #5 | 1（同上） | 0 | 判非缺口 |
| #6 | 0（改宽松模式后） | 0 | 口径变更见 §一.3 |

**原始事实**：`events.jsonl` 里确有 `PLATFORM-PROBE` 这一非 manifest 标识；“events-only=0”仅在“只统计 D2-* 形式”时成立。

---

## 四、用量口径、修复与 job 关联（原始事实）

### 4.1 用量口径

- 模型 `deepseek-flash`，temp 0.2，**不发送 `max_tokens`**，RAG off（`batch.json`、`summary.md §6`）。
- `summary.md §6`（**早期草稿，112 项口径**）：prompt **170,104** ｜ completion **836,942** ｜ reasoning **739,937** ｜ 请求数 **91**；并注明 reasoning 已含在 completion 内、不重复累加。
- `optimization-inputs-2.md §0.1/§1.1` 给出增量口径：增量 141 项中 **120 项 0 模型调用**；有自审的仅 21 项/26 份。
- **未见全批 277 项的最终用量总表**：`summary.md §11` 只有 lifecycle/disposition，没有 prompt/completion/requests 的 277 项合计 ⇒ 全批用量口径**未闭合**（见 findings）。

### 4.2 预算与修复轮次关联

- 预算（`batch.json`）：`selfRepair≤2`、`postEvalRepairTotal≤2`。
- 实测修复（事件层可确认）：
  - `D2-004` 自修 1 轮（`events.jsonl:20`）
  - `D2-025` 自修 1 轮 + `-fpermissive` 契约分离实验（`:188–193`）
  - `D2-177` 自修 1 轮（`:90`）
  - `D2-180` 自修 1 + 评估后修 1（`:318,320,321`）
  - `D2-088` 自修 1（`:436`）
  - `D2-092` 评估后修 1（`:403`）
  - `D2-093` 评估后修 **2**（预算用尽；第 1 轮未收敛，`:409,410`）
  - `D2-123` 采纳 1 项机械补丁（`:699`）
  - `D2-194` 自修 1（`:836`）
  - `D2-207` 自修 1（`:884`）
  - `D2-247` 自修 2（`:957,959`）
  - `D2-254` 自修 2（`:984,986`）
  - `D2-256` 自修 1（`:999`）
- **job 关联**：每项 `04-evaluation/job-*/job-id.txt` 与对应 `events.jsonl` 的 jobId 一一对应（本会话在 34 项逐项记录中核对到 `job-00-source-buildability`/`job-01-dual-build` 等）。`D2-247` 的 `job-01` = `eval-20261012-042524-39e03f4a`，与 `events.jsonl:961` 一致。

### 4.3 宣称“全知识注入”的依据

- 批次层**没有**任何“知识注入覆盖率 100%”的统计件；可核依据只有逐项请求件：
  - `02-conversion/request.system.txt`、`request.user.md`（首次请求正文）
  - `02-conversion/self-repair-*.system.txt` / `*.user.md`（修订请求正文）
  - `03-self-review/self-review-N.system.txt` / `.user.md`（自审请求正文）
- 事件层只记 `GENERATED`/`SELF_REVIEW`（模型、finish_reason、行数），**不记知识条目清单**。
- ⇒ “知识可达 / Agent 已读 / 模型已注入 / 效果已验证”四层在 batch 层**只有第一、二层的间接痕迹**（请求件本身）；**没有**逐条知识路径→注入位置的映射记录。逐项请求件的实际内容见 `harness-d-cases-*.md`（本区间 5 个进入生成的项）。

---

## 五、WAITING / 清理 / 未知提交去向

### 5.1 WAITING 31 项（`summary.md §11.4`、`reconciliation-6.md §6`）

| 类 | 项 | 恢复条件（文件声明） |
|---|---|---|
| C# 目标 `BLOCKED_ENV`（20） | D2-007~012、030、048~051、065、076~078、156~160 | 平台缺陷 2026-10-11 已修复 ⇒ 恢复条件已具备；D2-007 已重开试点但因观察面不对称保持 WAITING |
| 真实公网 `BLOCKED`（5） | D2-055、074、083、184、217 | 可验证网络阻断/重定向后重分类 |
| `RUN_SAFETY_NOT_READY`（2） | D2-082、108 | 硬编码非 loopback 目标，须隔离证据/受控输入 |
| `DRIVER_NOT_VIABLE`（3） | D2-167、169、175 | 须合法来源驱动 |
| 只读 FS 环境缺口（1） | D2-069 | 源写只读 `/usr`，须新冻结条件 |

### 5.2 清理

- 本会话读到的**全部** `returned-evidence/closure.json` 均为 `complete=true`、`cleanupConfirmed=true`、`issues=[]`、`cleanupRecords.<role>.status=passed`、`runnerStateAfter=READY`、`contaminated=false`（D2-241/243/245 与子会话报告的其余项）。
- `operational-discipline.md §11` **另记未清理项**：仓库根残留 **27 个 `.tmp-classify-*/` 目录**（早期 D2-001…D2-178），当时“**尚未删除**，等用户确认”。
  ⇒ **批次层存在“分类器暂存目录未清理”的已登记例外**，与 job 的 `cleanupConfirmed=true`（VM 侧）不是同一层。

### 5.3 未知提交去向

- 各轮对账均称 `items`↔`events` 双向差集归零（D2-* 口径），故**未见“已提交但无回执”的登记项**。
- 已登记的“未受理/被拒”均有明确 HTTP 结果与处置：D2-151（403）、D2-053（403）、D2-114（403）、D2-197（job-00 inconclusive 后 job-00b）、D2-210（PAUSED 后 BASELINE 失败）、D2-236（PAUSED 后 CORRECTION）。
- **未知项**：`summary.md §1 D12` 记“PowerShell `ConvertTo-Json` 破坏请求体 ⇒ `invalid_request_error`（从 5 KB 膨胀到 777 KB）”，**未登记该失败请求属哪一项/job**（无 taskId 指针）⇒ 属**去向未明的失败 attempt**。

---

## 六、“仅编译/旧停止”与现行 `LIB_UNOBSERVABLE_COMPILE_ONLY` 分支的差异

### 6.1 批次当时的处理（历史说明）

- 批次把“源可构建、但**无合法可观察入口/观察不可冻结**”的项一律记为：
  - `PREPARATION_GAP`（38 项，`summary.md §11.1`；`optimization-inputs-2.md §2.3` 细分四类：非入口库单元 31、job 特定路径 4、观察退化 2、关键外部依赖致无入口 1）；
  - 或 `PARTIAL` / `ORACLE_NOT_FREEZABLE`（早期 10 项：D2-017/018/066/072/089/090/094/098/099/101，见 `summary.md §2.3`）。
  - 共同点：**生成前停止、0 模型调用**（`optimization-inputs-2.md §0.1` 明确“全部 0 模型调用”）。

### 6.2 现行规则（当前规则）

- 根 `SKILL.md` 第 5 步 / `.agents/skills/code-convert/SKILL.md`：
  “本轮无法合法评估行为但源构建通过的，按评估准备 §1.3 记 **LIB_UNOBSERVABLE_COMPILE_ONLY**，**继续生成、自审与目标语法/编译验证**，行为未评估/UNVERIFIED、PARTIAL。”
- 即：同一形态（源可构建 + 无合法行为入口）在**现行规则**下**不停止**，而是**继续转换**并只做目标语法/编译验证。

### 6.3 差异（对照结论，不追改历史）

| 维度 | 批次当时（2026-10-10…12） | 现行规则 | 差异性质 |
|---|---|---|---|
| 无入口库单元（Go 非 main / Python 无 `__main__` / Ruby 无 `$0` 守卫 / 纯元数据） | `PREPARATION_GAP`，**0 模型调用** | `LIB_UNOBSERVABLE_COMPILE_ONLY`：**继续生成 + 目标语法/编译验证** + PARTIAL | **规则版本差异**（当时规则未含该分支） |
| 观察退化（argv=[] 空转 / stdout·stderr 全空且退出 0） | `PREPARATION_GAP`（D2-241、D2-236） | 先按 §1.1 判“冻结输入是否足以产生非退化观察”；不足则**另冻条件**；确无合法条件 ⇒ 同上 LIB 分支继续生成 | 规则版本差异 |
| 观察含 job 特定绝对路径 | `PREPARATION_GAP`（D2-210/232/233/258） | 同上：记范围后仍生成、目标语法/编译验证 | 规则版本差异 |
| 源侧构建失败（`SOURCE_NOT_BUILDABLE` / `SOURCE_DEPENDENCY_GAP`） | 跳过、0 模型调用 | 现行规则**同**：源构建失败不消耗转换调用 | **无差异** |
| oracle 不可冻结但可运行（`duration_ms` 等） | `PARTIAL` / `ORACLE_NOT_FREEZABLE`，保留平台 verdict | 现行规则同（`UNVERIFIED`，不记失败/通过） | **无差异** |

### 6.4 影响面（本会话独占区间内，原始事实）

- 本区间 34 项中（逐件复核后的准确计数）：`PREPARATION_GAP` **13 项**（D2-241、245、246、252、257、258、261、262、263、265、272、276、277）、`SOURCE_DEPENDENCY_GAP` **15 项**、`SOURCE_NOT_BUILDABLE` **1 项**（D2-251）、`CONVERTED` **5 项**（D2-247、254、256、269、270）——合计 34 ✓。
- ⇒ 若按**现行** LIB 分支，这 **13 项**中有相当部分（无入口库单元 / 观察退化 / job 特定路径）应**继续生成并做目标语法/编译验证**，而非停在 0 模型调用。
- **本会话不做追改**：原判定、原事件、原 result 一律保留，仅登记该口径差异。

---

## 七、本文件未覆盖/未闭合项

1. `batch/items/*.json`（277 份）逐件读原文：**已完成**（136 + 141 = 277/277，无读取失败；编号缺口 D2-026/D2-113；逐文件计数与 `summary.md §11` 完全吻合，详见 [coverage](harness-d-coverage.md) §3.4 与 [findings](harness-d-findings.md) F-13）。
2. 全批 277 项的**最终用量合计**未见任何汇总件（§四.1）。
3. `summary.md §1 D12` 的 `invalid_request_error` 失败请求**无 taskId 指针**（§五.3）。
4. 根 `batch-authorization.json` 与各用例副本的 `contractHash` 不一致（§一.1）；补读进一步证实：**用例内 `batch-authorization.json` 的 `contractHash=sha256:8090cfcc…4aac` 与 `controller-health-*.json` 的 `contractSetHash` 同值**，根件为 `a9ed1445…d82e`（F-14(a)）。
5. **batch 层无截断件**（补读结论）：`items/*.json` 为多行缩进 JSON、单行远小于 2000 字符（抽读 `items/D2-247.json` 67 行验证）；`events.jsonl` 为逐行短 JSON（抽读行 1–3 验证）；`summary.md`/`optimization-inputs*.md` 等为多行文本 ⇒ 本会话对 batch 层的阅读**不存在**“单行截断未读”问题。
6. **逐文件名机器枚举未完成**：补读阶段 `glob`/`grep` 不可用，无法再对 34 项目录的 667 件做完整文件名单枚举；[coverage](harness-d-coverage.md) §3.3 已按实际 `read` 的文件逐个列名并登记缺口（**部分**，不虚报）。
