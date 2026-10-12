# dataset-2 增量用例：三类优化输入（自审 / 失败重转 / 评估平台）—— 续篇

> **用途**：承 [`optimization-inputs.md`](optimization-inputs.md)（下称「前篇」），为优化「转换系统（生成 + 自审）」与「评估平台」**续记前篇未覆盖的增量事实**。
> **编制时点**：2026-10-12，基于 `batch/items/` 的 **277 项**记录与 `events.jsonl` 的 **1148 行**事件。
> **纪律**：与前篇一致——本文每条结论均附出处（`文件 §节`、`items/<taskId>.json`、`events.jsonl:<行>` 或 `taskId → 字段`）。**无出处者不写入，未核实者标注「待核」。**
> **与前篇的关系**：**前篇覆盖 136 项 / 事件 1~613 行**（上限 `D2-183`）；**本文只覆盖其后的 141 项 / 事件 614~1148 行**，**不重复**前篇已展开的七类误译（前篇 §1.2）与平台结论（前篇 §3.1/§3.3/§3.4/§3.5/§3.6）——凡已固化者，本文**只回指、不整段复刻**。
> 逐项明细仍以 [`summary.md`](summary.md) §11（收尾快照）与 [`reconciliation-3/4/5/6.md`](reconciliation-6.md) 为权威；本文按「自审 / 失败重转 / 评估平台」三视角重组增量。

---

## §0 口径与出处

### 0.1 覆盖范围（实测计数）

> **口径边界**：`SOURCE_NOT_BUILDABLE` / `SOURCE_DEPENDENCY_GAP` / `PREPARATION_GAP` / `BLOCKED*` **均非转换失败**；`WAITING` 不计入终态（终态 = `DONE` + `PARTIAL`）。本文**不合成单一「成功率」**（纪律同前篇 §0.1 与 `summary.md` §8）。

| 维度 | 前篇快照（2026-10-11） | 当前（2026-10-12） | **本文增量** | 出处 |
|---|---:|---:|---:|---|
| `items/` 总数 | 136 | **277** | **141** | 实测 `ls batch/items`；增量 = `events.jsonl` 前后段 taskId 差集 |
| `events.jsonl` 行数 | 613 | **1148** | **535** | 实测 `wc -l` |
| events 段内 distinct taskId | 136 | 277 | 143（含 2 项重触） | 同上 |

**增量 taskId 清单（141 项）**——出处：`events.jsonl:1~613` 的 taskId 集合与 `:614~1148` 之差（只读解析，非估计）：

```
D2-063~D2-065, D2-107, D2-109~D2-112, D2-114~D2-150,
D2-184~D2-213, D2-217, D2-222, D2-232~D2-233, D2-235~D2-236,
D2-238~D2-241, D2-243, D2-245~D2-247, D2-249~D2-300
```

> **缺口说明**：`D2-108`（前篇已覆盖）、`D2-113` 及 `D2-214~216 / 218~221 / 223~231 / 234 / 237 / 242 / 244 / 248` **无 item 文件**（manifest 编号缺口，非本任务遗漏）。写作时逐个 `ls` 核实，**不臆造条目**。

**增量终态分布（实测）**：

| 维度 | 分布（增量 141 项） | 出处 |
|---|---|---|
| lifecycle | `DONE 134` / `PARTIAL 4` / `WAITING 3` | 逐项 `items/*.json` 统计 |
| disposition | **`SOURCE_DEPENDENCY_GAP 75`** / **`PREPARATION_GAP 38`** / `CONVERTED 23` / `SOURCE_NOT_BUILDABLE 2` / `BLOCKED 2` / `FROZEN 1` | 同上 |
| `verdicts.comparison` 首词 | `matched 12` / `semantic_pass 6` / `mismatched 5` / `UNVERIFIED 6` / `n/a 112`（非转换去向） | 同上 |
| self-review（`self-review-N.json`） | **21 项有自审、26 份**：`NO-REPAIR-IDENTIFIED 16` / `REPAIR-RECOMMENDED 10` | 逐份 `verdict` 统计（**排除 `.model.json`/`.raw.json`/`.body.json`/`.attempt-*`**，口径同前篇） |

> **本增量最重要的口径转折**：前篇的「失败」主体是**转换缺陷**；本文的「失败」主体**转为源侧拦截与准备缺口**——`SOURCE_DEPENDENCY_GAP + PREPARATION_GAP` 合计 **113/141 = 80%**，且**全部 0 模型调用**。真实转换缺陷仅落在 5 个方向段的少量 `CONVERTED` 项上（`matched 12` / `semantic_pass 6` / `mismatched 5`）。

### 0.2 出处层级（本文引用格式）

| 层 | 路径 | 本文用于 |
|---|---|---|
| 调度层 | `items/<taskId>.json`（字段级） | 逐项去向、`disposition`、`coverageGap`、`repairChain`、`codeRevisions`/`selfRepairRounds` |
| 调度层 | `events.jsonl`（事件名 + **行号**） | 失败 / 修复 / 更正 / 重分类事件流 |
| 证据层 | `<case>/output/batch/03-self-review/self-review-N.json` | **自审原因与建议的原始出处**（`verdict` + `items[].origin/issue/proposed_fix/risk`） |
| 证据层（**新增**） | `/api/source-preflights` 的 **source-only capsule**：`source_preflight_manifest.json` + `input_profile.json` + `metadata.json`；`evaluationMode=build-only` | **源侧预检**（本增量期起的主形态，见 §0.3） |
| 底稿层 | `reconciliation-3/4/5/6.md`、`summary.md §11`、`platform-probes/probe-csharp-target-2026-10-11/PROBE-RESULT.md`、`operational-discipline.md` §13~§16、`pattern-note-*.md` | 已固化的纪律与增量优化点（本文以「章节号」引用） |

### 0.3 形态断代声明（**引用前必读**）

> 本增量期发生**评估形态切换**。凡引用 `buildCommand` / capsule / 双侧提交相关事实，**必须标明属哪种形态**：

| 形态 | 适用区间 | 特征 | 出处 |
|---|---|---|---|
| **旧双侧形态** | `D2-194` 及之前（前篇全程） | 双侧 `comparison_manifest` + 占位 `target/` 树；源侧驱动 `source/run_case.py` 随源一同提交 | 前篇 §0.2；`events.jsonl:836`（D2-194） |
| **新 source-only 形态** | **`D2-197` 起**（批次首例） | `/api/source-preflights` + **source-only capsule**（无 target 树）+ `evaluationMode=build-only`；`source.buildCommand` **必须 argv token 数组**；去掉驱动 ⇒ `source/` 树变化 ⇒ **必须重新分类** | `README.md` D2-197 条目；`reconciliation-5.md`；`summary.md §11.3` |

> **歧义提示**：前篇 §2.3 的 D-1~D-10 装置缺陷、§3.8 的 `caseId`/`identity_mismatch` 均属**旧双侧形态**；本文 §2.4/§3.1 中的"驱动"若已消失（source-only），相关纪律**不再适用**，须按新形态重述。

---

## §1 自审原因与建议

> **第一类诉求**：自审（模型对生成目标的静态复核）在增量期给出了什么原因、什么建议，以及它们是否可信。
> **原始出处**：增量的 26 份 `<case>/output/batch/03-self-review/self-review-N.json`（结构同前篇：`{verdict, reviewedScope, items:[{id, location, evidence, origin, issue, proposed_fix, risk}]}`）。

### 1.1 自审产出规模与档次

| 指标 | 值 | 出处 |
|---|---:|---|
| 增量有自审的项 / 自审份数 | **21 项 / 26 份** | 逐份 glob（排除 `.model.json`/`.raw.json`/`.body.json`/`.attempt-*`） |
| `NO-REPAIR-IDENTIFIED` | **16** | 逐份 `verdict` 统计 |
| `REPAIR-RECOMMENDED` | **10** | 同上（清单见 §1.2） |
| 多轮自审项 | `D2-247`（3 轮）、`D2-254`（3 轮）、`D2-256`（2 轮） | 逐项文件名 |
| 增量**无自审**的项 | **120 / 141** | 余下项均为**非转换去向**（`SOURCE_*`/`PREPARATION_GAP`/`BLOCKED`），**0 模型调用** ⇒ 不产生自审 |

**关键观察**：**自审只在 `CONVERTED` 路径产生**——141 项中 120 项（85%）因未进入转换而**无任何自审产物**。这与前篇 §1.1「绝大多数自审为 `NO-REPAIR-IDENTIFIED` 且只做静态对照」互补：本增量进一步说明**自审的覆盖面 = 转换面，而非批次面**。凡 `SOURCE_*`/`PREPARATION_GAP` 类结论，**均不由自审给出，而由编译器诊断 / 源行为基线独立定案**（见 §2.2/§2.3）。

### 1.2 自审命中的「转换引入」缺陷（增量 10 份 `REPAIR-RECOMMENDED` 的原始建议）

> 出处：各 case 的 `03-self-review/self-review-N.json`（`items[].origin` + `proposed_fix`）。「后续」列来自 `items/*.json` 的 `codeRevisions`/`selfRepairRounds` 与 `events.jsonl`。

| case / taskId | 方向 | 自审提出的差异（原因） | 自审建议（`proposed_fix`） | 后续处置（出处） |
|---|---|---|---|---|
| **D2-194** | go-to-csharp | Go→C# **命令分派臂丢失**：源 `case "exec": ex(argv)` 的本地执行分支未译出，helper 与 help 条目却已译（`exec` 静默降级为未知命令） | 在 `CmdSwitch` 补 `case "exec": Ex(input.argv); break;` | **已修**（`codeRevisions=1`、`selfRepairRounds=1`；`events.jsonl:836`） |
| **D2-207** | go-to-python | 空 payload 取下标 panic 的**退出码 2 vs 目标 1**（转换引入） | 异常路径 `sys.exit(2)`（并避 traceback 差异） | **已修**（`self-repair-1.py`；`codeRevisions=1`；`events.jsonl:884`） |
| **D2-247**（sr1） | python-to-cpp | **6 项**：连字符回偏移 `j+1`、`condC` `is_blank` 反转、`indent` 缺 predicate、`is_py_space` 缺 `0x85`(NEL)、`splitlines` 缺 Unicode 分隔符、`wrap/fill` 签名 | 逐项对照源逻辑修正 | **采纳 5、拒 1**（`wrap-fill-signature` 属**语言层签名差异**，非缺陷）；`selfRepairRounds=1`（`events.jsonl:957`） |
| **D2-247**（sr2） | python-to-cpp | **2 项**：`0x85` 与 UTF-8 统一（`C2 85`）、`expandtabs` 当 `tabsize<=0` 应保留 `\t`（标 `source-preexisting`） | 统一为 UTF-8 字节；`tabsize<=0` 保留制表符 | **采纳 2**（`selfRepairRounds=2`；`events.jsonl:959`） |
| **D2-254**（sr1/sr2） | python-to-csharp | sr1 **3 项**（`push_token` 调用方 token 顺序颠倒 等）＋ sr2 **1 项**（`pushback/_pushback_chars` 应为 **`Stack<string>` LIFO**） | 恢复 LIFO 语义 | **已修**（`selfRepairRounds=2`；`events.jsonl:986`） |
| **D2-256** | python-to-go | **2 项**：选项缩写解析、缺参消息（均不影响冻结 `argv=[]` 路径） | 补缩写与缺参分支 | **已修**（`selfRepairRounds=1`；`events.jsonl:999`） |
| **D2-123** | csharp-to-go | **2 项**（详见 §1.3）：① `autorunLocations` 顺序 **（误判）** ② `REG_EXPAND_SZ` 未用 `ExpandEnvironmentStringsW` 展开 **（成立）** | ① 改顺序 ② 展开环境变量 | **采 1 拒 1**：②按纪律**机械应用 `proposed_fix`** ⇒ `codeRevisions=1`；①**误判未采纳**（`events.jsonl:699`） |
| **D2-116** | csharp-to-cpp | **1 项**：`AccessCheck` 首形参应传 `pSD`（`SECURITY_DESCRIPTOR*`）而非 `pDacl`（`ACL*`） | 改传 `GetNamedSecurityInfoW` 返回的 `pSD`，末 `LocalFree` | **未采纳 / 未修复**：oracle 不可冻结，**无法据此定案**（`items/D2-116.json`）；`codeRevisions=0` |
| **D2-117** | csharp-to-cpp | **1 项**：声称源用大写 `ScheduledTasks.xml`，目标 `Contains` 区分大小写 | 把 `Scheduledtasks.xml` 改为 `ScheduledTasks.xml` | **误判未采纳**：实测**源第 87 行即小写** `"Scheduledtasks.xml"` ＝ 目标第 562 行，**差异不存在**（`README.md` D2-117 条目）；`codeRevisions=0` |

**汇总（可直接并入生成提示词的「增量高频误译模式」）**：
1. **命令分派枚举漏臂**：D2-194（`switch` 中某 `case` 未译出，但 helper/help 已译 ⇒ **不可达**）。
2. **`argv` 语义差别下的"顺序/栈语义"**：D2-254（`Stack<string>` LIFO）、D2-123（源交替排列的注册表位置）。
3. **字符集边界（Unicode 空白 / NEL / 行分隔符）**：D2-247（`0x85`、U+2028/29、UTF-8 `C2 85`；与前篇 §1.2 第 2 类"行尾字节"同族）。
4. **异常路径退出口径**：D2-207（panic→退出码 2）。
5. **`tabsize<=0` 等"退化入参"的边界保留**：D2-247（保留 `\t`）。

### 1.3 自审的盲区、误判与格式缺陷

| 类 | 事实 | 出处 |
|---|---|---|
| **误判（大小写 / 符号顺序，静态对照最易错）** | ① `D2-117` 声称源用大写 `ScheduledTasks.xml`，**实测源第 87 行即小写**（与目标一致）⇒ 差异不存在；② `D2-123` 声称目标 `autorunLocations` 顺序与源不一致，**实测源 L45–54 本身即交替排列 ＝ 目标 L75–84** | `README.md` D2-117/D2-123 条目；各 `self-review-1.json` |
| **不可定案（不做修复）** | `D2-116` `AccessCheck` 首形参断言**看似合理**，但该项 oracle 不可冻结（输出含主机态 PID + 进程/DLL 表）⇒ **无法据此判收敛**，**未做修复**、保留平台 verdict | `items/D2-116.json`；`README.md` D2-116 条目 |
| **正确的"不猜" / 部分采纳** | ① `D2-247` 拒 `wrap-fill-signature`（**语言层签名差异，非缺陷**——自审把语言语义差异误列为"候选修复"）；② `D2-123` 采纳项按纪律**机械应用**模型 `proposed_fix`（`ExpandEnvironmentStringsW`） | `03-self-review/self-review-1.json`（D2-247 sr1 #6、D2-123 #2） |
| **自审反向纠正使用者事实** | `D2-126` 自审**纠正了我 prompt 中的错误提示**：我写"步进 16 字节"，正确为 **12**（＝`Marshal.SizeOf`；16 实为含 count 的 `sizeof(TOKEN_PRIVILEGES)`） | `README.md` D2-126 条目 |
| **自审落在观察面之外** | `D2-064` 自审报"目录权限语义"，但该差异**落在冻结观察面之外**，实测 `matched` ⇒ **未采纳**（同前篇 D2-061 型） | `README.md` D2-064 条目 |
| **自审只做静态对照** | 增量 16/26 份 `NO-REPAIR-IDENTIFIED`；`reviewedScope` 亦声明未编译/未运行（同前篇 §1.3） | 各 `self-review-N.json` |
| **输出截断（新形态的格式缺陷）** | `D2-247` 自审 2 首次 **`finish_reason=length`**（reasoning 65536 tok 耗尽、content 空）⇒ 保留为 `self-review-2.attempt-1-truncated.json` 后**聚焦重试成功**（与前篇 H2 的"围栏/转义"型不同，属**长度截断**型） | `03-self-review/self-review-2.attempt-1-truncated.json`；`README.md` D2-247 条目 |

### 1.4 给「生成 + 自审」的增量优化建议（由 §1.2/§1.3 导出）

1. **提示词增补本轮高频误译模式**：命令分派漏臂（D2-194）、`Stack` LIFO / 交替顺序（D2-254/123）、Unicode 空白与行分隔符（D2-247）。**与前篇 §1.2 的七类并列**，勿合并。
2. **自审须区分「语言层签名差异」与「转换缺陷」**：`D2-247` 把 `wrap/fill` 签名列为候选修复被正确拒绝 ⇒ 建议自审 instruction **显式豁免"因目标语言参数约定不同"的签名差异**。
3. **自审可反用于"生成前事实核查"**：`D2-126` 证明自审能纠正**使用者 prompt 中的事实错误** ⇒ 建议把自审的"回源行号核对"结论**回流为生成侧的事实基线**。
4. **对"大小写 / 符号顺序"类断言强制回源行号**：`D2-117`/`D2-123` 两处误判**均属此类** ⇒ 建议自审对这类断言**必须给出源侧行号 + 原文片段**，否则不予采纳。
5. **自审不可作为"确有缺陷"的证据**：`D2-116` 的合理断言因 oracle 不可冻结而**无法定案** ⇒ 自审建议须先过**可判性核查**（该观察面能否冻结），再决定是否修复（增补前篇 §1.4 第 5 条）。
6. **长文件自审须容忍截断**：`D2-247` 的 `finish_reason=length` 表明**长输出会耗尽 reasoning 预算** ⇒ 建议对长文件自审**分段或聚焦**，并**保留截断稿**（已有实践）。

---

## §2 各类失败与重新转换建议

> **第二类诉求**：增量期出现了哪些失败、如何归因、重转前要做什么检查。
> **总口径**：失败**必须分列**（纪律同前篇 §2）；**源侧拦截与已评估项分列**。
> **本增量的重心变化（贯穿全节）**：失败主体从「转换缺陷」转为「**源侧拦截 + 准备缺口**」——`SOURCE_DEPENDENCY_GAP 75` + `PREPARATION_GAP 38` = **113 / 141（80%）**，且**全部 0 模型调用**；真实转换缺陷仅落在 5 个方向的少量 `CONVERTED` 项上。

### 2.1 真实转换缺陷（由第三方证据坐实，闭环 = 反例→定位→最小修复→复测）

| 编号 | taskId | 方向 | 缺陷 | 反例 / 证据 | 修复 | 复测 |
|---|---|---|---|---|---|---|
| **F6** | D2-194 | go-to-csharp | Go `switch` 中**本地执行分派臂丢失**（`case "exec"` 未译，helper/help 已译 ⇒ `exec` 静默降级为未知命令） | 自审定位 `CmdSwitch` 缺臂（`03-self-review/self-review-1.json`） | 补 `case "exec": Ex(input.argv); break;`（`codeRevisions=1`） | 平台 `mismatched`——但**因 oracle 不可冻结**（stdout 嵌 job-specific 绝对路径），**不据此定案**（`events.jsonl:836`） |
| **F7** | D2-207 | go-to-python | 空 payload 取下标 panic 的**退出码 2 vs 目标 1** | 自审 1 项（`conversion-introduced`） | 异常路径 `sys.exit(2)`（`self-repair-1.py`） | **stdout + 退出码均匹配**；唯一 diff = stderr 形态（Go panic 栈 vs Python traceback，各含本侧绝对路径）⇒ **归因装置/语言运行时**（`events.jsonl:884,885`） |
| **F8** | D2-247 | python-to-cpp | **多轮 8 项**：`j+1` 回偏移、`condC` `is_blank` 反转、`indent` 缺 predicate、`is_py_space` 缺 `0x85`、`splitlines` 缺 Unicode 分隔符、`0x85` 与 UTF-8 统一（`C2 85`）、`expandtabs tabsize<=0` 保留 `\t` | 自审 1（6 项）＋自审 2（2 项） | **2 轮自修**（`selfRepairRounds=2`；拒 `wrap-fill-signature` 语言层差异） | ✅ **`matched`**（diffs=0；双侧 stdout 33 B 逐字节相同，digest `b8cb8f10…`）（`events.jsonl:957,959`） |
| **F9** | D2-254 | python-to-csharp | `push_token` 调用方 **token 顺序颠倒**；`pushback/_pushback_chars` 应为 **`Stack<string>` LIFO** 被改为 FIFO | 自审 1（3 项）＋自审 2（1 项） | **2 轮自修**（`selfRepairRounds=2`） | ✅ **`matched`**（diffs=0；双侧 stdout 45 B 逐字节相同）（`events.jsonl:986`） |
| **F10** | D2-256 | python-to-go | 选项**缩写**解析、**缺参消息**缺失 | 自审 1（2 项） | **1 轮自修**（`selfRepairRounds=1`） | ✅ **`matched`**（diffs=0；stdout 724 B + stderr 73 B 双侧逐字节相同）（`events.jsonl:999`） |
| — | D2-123 | csharp-to-go | `REG_EXPAND_SZ` 未用 `ExpandEnvironmentStringsW` 展开 ⇒ 命中行与源不一致 | 自审 1 项（成立） | **机械应用 `proposed_fix`**（`codeRevisions=1`） | `semantic_pass`（唯一 `minor` diff = 时间戳，被 `timestamps` 消噪）（`events.jsonl:699`） |

**优化点**（出处：各 item `repairChain`/`codeRevisions`、`events.jsonl`）：
- **`switch` 分派臂必须"逐臂清点"**：F6 的漏臂**不影响冻结的 `argv=[]` 探针**（EOF panic 先触发），若只看"当前探针 matched"则**永难发现** ⇒ 契约应要求**逐臂核对**，而非只验一条路径。
- **异常路径的退出码是合同面的一部分**：F7 中源以 `panic` 退出 2 ⇒ 目标须**显式** `sys.exit(2)`，不能依赖解释器默认 1。
- **Unicode 空白/行分隔符是跨语言最隐蔽的差异**：F8 的 `0x85`/U+2028/29 仅在**非 ASCII 输入**下显形 ⇒ 与前篇 §1.2 第 1、2 类同族，**并入提示词**。
- **容器语义（LIFO/FIFO）**：F9 的 `Stack<string>` 语义在**多 token 回溯**场景才暴露 ⇒ 建议契约对目标语言**容器类型显式指定语义**。
- **修复轮次与冻结路径无关的部分**：F10、F6 的缺陷项**均落在冻结 `argv` 之外**（不影响当次 verdict）⇒ **不可因 verdict 绿而当作已覆盖**（覆盖边界须显式登记）。

### 2.2 源侧拦截（**均非转换失败**，0 模型调用）

#### 2.2.1 `SOURCE_DEPENDENCY_GAP`（增量 **75 项**）——按"依赖缺口类型"细分八类

| 类 | 数量 | 清单（taskId） | 判据（出处） |
|---|---:|---|---|
| ① **.NET 运行时内部文件**（`System.*` 内部，无公开 TFM） | 8 | D2-110, 112, 114, 115, 121, 122, 129, 136 | 编译器诊断 `CS0246`/`CS0234`（`System.Private.CoreLib` 内部类型）；`items/D2-110.json → coverageGaps[0]` |
| ② **同项目多文件**（SharpUp：`Checks/*` 依赖 `Classes`/`Utilities`/`Native`） | 17 | D2-127, 131, 132, 137, 138, 139, 140, 141, 142, 143（`Native.Win32`）, 144, 145, 146, 147, 148, 149, 222 | `CS0234 SharpUp.Classes/Utilities/Native`；`items/D2-131.json` |
| ③ **Go 标准库同包文件缺失**（`sort`/`strconv`/`bytes`/`strings`/`filepath`… 缺 `zsortfunc.go` 等同包文件） | 6 | D2-185, 187, 192, 195, 197, 208 | `undefined: pdqsort`/`Quote`/`IndexByte`/…；`items/D2-185.json → coverageGaps[0]` |
| ④ **Go 内部包禁止包外导入** | 1 | D2-196 | `import "internal/bytealg"`；`items/D2-196.json` |
| ⑤ **外部 Go 模块未 vendored**（`golang.org/x/sys/windows` 等） | 11 | D2-188, 191, 200, 201, 204, 205, 206, 209, 211, 212, 213 | `no required module provides package …`（隔离环境无网络不可还原）；`items/D2-200.json` |
| ⑥ **外部 Python 第三方包**（`impacket`/`six`/`dnspython`/`pyasn1`/`Cryptodome`） | 18 | D2-235, 238, 239, 240, 243, 249, 250, 253, 255, 259, 260, 264, 266, 267, 268, 271, 273, 274 | `py_compile` 通过但**运行** `ModuleNotFoundError`；`items/D2-235.json → coverageGaps[0]` |
| ⑦ **外部 NuGet 包** | 1 | D2-135（`NDesk.Options`） | `CS0246 "NDesk"`；`items/D2-135.json` |
| ⑧ **外部程序集 / 框架 / gem**（Apollo `ApolloInterop`；Metasploit `Msf::*`；Ruby gem `zip`） | 13 | D2-120（Apollo）, 275（gem `zip`）, 285, 287, 288, 289, 290, 292, 293, 294, 298, 299, 300（Metasploit） | `CS0246 "ApolloInterop"`；`LoadError`/`Msf::Post` 基类缺失；`items/D2-285.json → coverageGaps[0]` |

> **合计 8+17+6+1+11+18+1+13 = 75 ✓**

**关键新纪律（增量新增）**：
- **Python 源必须 build-and-run 才暴露 import 缺口**：`py_compile`（语法检查）**不解析 import**、**必须运行**才暴露缺口（原文 "py_compile does not resolve imports; running is required to expose the gap"）⇒ 目标侧 `ModuleNotFoundError`（`events.jsonl:922`，D2-235）；**仅语法预检不足以判可转换性**。
- **Go 标准库"看着自包含"实则缺同包文件**：单文件 `go build` 常报 `undefined: …` ⇒ 同包生成文件（如 `zsortfunc.go`）不在快照内 ⇒ **不可作独立翻译单元**。
- **"非 main"与"不可构建"是两回事**：`D2-186`/`189`/`193`/`202`/`203` 等 Go stdlib 包 / Python stdlib 模块**编译 `completed/0`**（自包含）但**非 main ⇒ 无产物/无入口** ⇒ **归 `PREPARATION_GAP`（§2.3）**，**不得记 `SOURCE_DEPENDENCY_GAP`**（`events.jsonl:811`）。

#### 2.2.2 `SOURCE_NOT_BUILDABLE`（增量 **2 项**）

| taskId | 事实 | 出处 |
|---|---|---|
| **D2-119** | 源 `UnquotedServicePath.cs` **数据集残缺**：第 225–274 行为**孤立初始化块**（无函数签名的裸块，引用未定义 `currentSids`/`identity`/`rules`/`allowWrite`）⇒ 编译器诊断 `CS1519`(L225)/`CS0116`(L229)/`CS1022`/`CS1026`/`CS8124` | `items/D2-119.json` |
| **D2-251** | 源 L8 `from _csv import __version__`，但本 runner 的 `_csv` **不暴露该名字**（C 扩展接口不匹配）⇒ 源接口与本 runner 不符，无有效运行时基线 | `items/D2-251.json → coverageGaps[0]` |

> **判据统一**：`SOURCE_NOT_BUILDABLE`（源自身缺陷/接口不符）与 `SOURCE_DEPENDENCY_GAP`（**快照外**依赖）**必须分列**（前篇 §2.2 出口判据表**继续有效**）。

### 2.3 全新去向 `PREPARATION_GAP`（增量 **38 项**，本增量最大的新故事）

> **定义**：源**可构建且非"依赖缺口"**，但**无可用的可观察入口**或**观察不可冻结** ⇒ **无法在冻结条件下产生行为结论** ⇒ 记 `PREPARATION_GAP`，**0 模型调用**（纪律 `§1.1 生成前停止`）。**非转换失败**。

| 类 | 数量 | 清单（taskId） | 判据（出处） |
|---|---:|---|---|
| ① **非入口 / 库单元**（无 `__main__`、非 main 包、无 `__FILE__==$0` 入口守卫、纯元数据） | 31 | D2-150, 186, 189, 190, 193, 198, 202, 203, 245, 246, 252, 257, 261, 262, 263, 265, 272, 276, 277, 278, 279, 280, 281, 282, 283, 284, 286, 291, 295, 296, 297 | "no observable behaviour of its own; establishing an entry would**发明源所没有的行为**"（`items/D2-186.json → coverageGaps[0]`） |
| ② **观察含 job 特定绝对路径 ⇒ oracle 不可冻结** | 4 | D2-210, 232, 233, 258 | stderr/stdout 嵌 `…\workspaces\eval-<jobId>\…`，**不在平台 `temporary-paths` 覆盖内**（`items/D2-232.json → coverageGaps[0]`；`events.jsonl:912,913`） |
| ③ **观察退化（冻结输入不足）** | 2 | D2-236, 241 | `argv=[]` 即退出 / 回落读 stdin 且 stdin 为空 ⇒ **stdout/stderr 全空、退出 0**（`events.jsonl:951`；`items/D2-241.json`） |
| ④ **关键外部依赖缺失致可观察入口不存在** | 1 | D2-107（`pet.dll` 缺失 ⇒ `LoadLibrary` 返 NULL、**静默退出**） | `items/D2-107.json → coverageGaps[0]` |

> **合计 31+4+2+1 = 38 ✓**

**优化点 / 新纪律**：
- **冻结阶段就判「是否有合法可观察入口」**：库单元/纯元数据（①）**在建入口即等于编造源行为**（`§65` 反面纪律）⇒ **生成前停止**，本批次 **31 项因此 0 模型调用**。
- **冻结输入必须"真的会做事"**（③ 强化前篇 §2.7-A2）：Python 源若在 `argv=[]` **回落读 stdin**（如 `base64.py` 的 `func(sys.stdin.buffer, …)`），必须**冻结非空 stdin 或非空 argv（含 fixture）**；否则观察退化。`D2-236`（`pwncat.py`）另证：`argv=[]` 在 `parser.parse_args()`(**L6018**) 即报 `required: port` 退出 2，**从未进入 `main()`(L6061)** ⇒ **从未到达任何工具状态**（`events.jsonl:951`）。
- **lib-only 项需要"合法中性入口"或专用档位**：多项 `coverageGaps` 提出同一诉求——**per-item `LIB_UNOBSERVABLE_COMPILE_ONLY` 档位**（`items/D2-252.json`、`D2-276.json` 等），即"**只编译不运行**"作为合法终态，避免每一项都靠人工判"编不编入口"。
- **②与 `SOURCE_NOT_BUILDABLE` 的区分**：②是**观察面**不可冻结（源能构建、能运行），不是源缺陷。

### 2.4 装置 / 驱动缺陷（增量新增，编号续前篇 D-1..D-10）

> 一字总则不变：**驱动的唯一职责是「启动、等待、采集、终止」，采集 = 原样透传字节**（`operational-discipline.md` §6）。**本增量期该纪律又被违反 4 次**。

| 编号 | taskId | 缺陷形态 | 后果 | 出处 |
|---|---|---|---|---|
| **D-11** | D2-111（另 D2-062、D2-186 同型） | **换行转义故障（`§16`）**：用 shell `printf`/`sed` 生成 `run_case.py` 时，`\n` 变成**真实换行** ⇒ 驱动 `SyntaxError` | target **从未执行**；假 FAIL | `events.jsonl:650`（D2-111 原始行含换行、**自身 JSON 不可解析**）、`:614`（D2-062 重写驱动）、`:811`（D2-186） |
| **D-12** | D2-109（另 D2-116） | **工具链/驱动夹带缺陷**：①`net8.0` 下静态 `Directory.GetAccessControl` 报 `CS1929`（**工具链契约不匹配**，非源缺陷）；②我补的 `Driver.cs` 用了 **Core-only `Path.GetRelativePath`** | 假 `build failed` | `events.jsonl:640`（"two non-source failures cleared first… Discipline 16"） |
| **D-13** | D2-116 | **打包链断裂**：一次 bash 链中 `cp` 失败 ⇒ `probe.csproj`/`run_case.py` **从未生成** ⇒ `MSB1009`（project file missing） | 假 FAIL | `events.jsonl:666` |
| **D-14** | D2-232（另 D2-007） | **驱动形态不匹配 / 观察面含构建产物**：①批内 python 驱动只解析 `target.py/.rb/.ps1` 或 `program(.exe)`，源脚本名 `build_run.ps1` ⇒ `DRIVER-FAILURE exit 97`、stdout 空；②源遍历 cwd ⇒ 观察含 `program.exe`，与目标树**不对称** | 假 FAIL / 假对比面 | `events.jsonl:912`（D2-232）；`summary.md §11.3.4`（D2-007） |
| **D-15** | D2-114 | **提交端用陈旧分类件**：首次提交误用**旧的 BLOCKED `this-task-classification.json`**（`classification-1`）而非新 `classification-2` | `403`（`blockedReason=public_network_unverified`） | `events.jsonl:660` |

**优化点（重跑前必查，**在**前篇「装置对称性五问」之上**增补）**：
1. **先查换行转义**（D-11）：凡用 shell 生成**含转义**的驱动/Python 源码，**必须**用文件写工具或写 `\\n`；生成后**先做语法自检**再提交。**增量期 §16 又被触发 3 次**（D2-062/111/186）——**该纪律尚未固化入 `operational-discipline.md`，属高优先待办**。
2. **"两侧观察面文件集合是否同源"**（D-14②）：源遍历 cwd 的用例，须改用**共享中性 fixture cwd**（前篇五问之 3 的**强形式**）。
3. **提交前核对分类件版本**（D-15）：`this-task-classification.json` 必须是**最新**一次分类结果；`classification-1`（误生成）**须删除**（见 §2.7 H7）。
4. **驱动须按目标**形态**选择**（D-14①）：脚本型源要能直接被 `runCommand` 启动（须去驱动 ⇒ `source/` 树变化 ⇒ **重分类**，见 §2.7 H8）。

### 2.5 oracle 不可冻结（`PARTIAL`，**非失败、非通过**）

| taskId | 不可复现的可观察量 | 出处 |
|---|---|---|
| D2-116 | 主机态 **PID + 机器进程/DLL 表**（命中 `C:\CodeConvertRemote\Stack\Agent\...`） | `items/D2-116.json`；`README.md` D2-116 条目 |
| D2-118 | **21 个周期性服务的 `State`**（源 `Running`↔目标 `Stopped`；`BITS`/`W32Time`/`WSearch`…）；其余 218 服务逐字节相同 | `items/D2-118.json` |
| D2-134 | `execution.exitCode`（源 -1 vs 目标 0）+ `stream.digest`，**均由 `ReadKey()` 无控制台时的装置态产生** | `items/D2-134.json` |
| D2-194 | stderr/stdout 嵌 **job-specific 绝对路径** | `items/D2-194.json` |

**判据不变**（前篇 §2.4）：可观察量含**两次执行间不可复现**成分，且**不在** `temporary-paths`/`timestamps`/`ephemeral-ports` 覆盖内 ⇒ 记 `UNVERIFIED` + `ORACLE_NOT_FREEZABLE`，lifecycle `PARTIAL`，**保留平台原 verdict、不重复重提求变绿**。

**优化点**：`D2-118` 是本类**最强实例**——**两侧均 245 行、服务集合与枚举顺序完全一致、唯一 `major` diff 是 21 个服务的运行态**；已核验目标 `QueryServiceStatusEx.dwCurrentState` 映射**未反转**（218 项逐字节相同）⇒ **差异纯属运行期环境量**。建议冻结阶段**对"输出含主机运行态"的用例**直接预判 `ORACLE_NOT_FREEZABLE`（本增量 4 项因此不消耗评估后修复）。

### 2.6 C# 目标平台阻断（**G1 → 已修复**）

| 项 | 事实 | 出处 |
|---|---|---|
| **修复确认** | 前篇 §2.5 的 G1（`csharp` 目标 `INFRA_ERROR`/evidence-bundle schema 缺限）已于 **2026-10-11 复测修复**：复用 D2-007 capsule 的探针 job `eval-20261011-122249-fe456bbe` **`COMPLETED`**、`target build/exec completed/0`、`collectorDiagnostics=[]` | `platform-probes/probe-csharp-target-2026-10-11/PROBE-RESULT.md` |
| **恢复面** | **20 项** C# 目标 `BLOCKED_ENV`（`D2-007~012, 030, 048~051, 065, 076~078, 156~160`）**恢复条件已具备**；`D2-007` 已**重开试点** | `events.jsonl:1146,1148` |
| **重开试点实况（如实记录）** | `D2-007` 重分类 `2.4 ALLOWED`；新源预检 `eval-20261012-061842-037c6549` build/exec `completed/0`；**因观察面含构建产物（`program.exe`）两侧不对称、未继续生成** ⇒ **如实保持 `WAITING`** | `memory`/`README.md`；`events.jsonl:1148` |
| **新纪律** | C# 目标 `artifactLanguage` **必须写 `csharp`**（非 `dotnet`），否则 `403 identity_mismatch` | `README.md`（C# 目标修复条目） |

> **重开动作口径**：当年这些项**只做了 job-00 源预检**（`target.cs` 为占位 stub）、**从未生成真实目标** ⇒ 重开 = **从生成开始**跑全链（重分类 → 源预检 → 生成 → 自审 → 双侧提交 → 取证）。

### 2.7 流程 / 记录类（续前篇 H1..H6）

| 项 | 事实 | 出处 |
|---|---|---|
| **H7** | **误生成的 `classification-1.json` 须删除**；`this-task-classification.json` 必须写入**最新** `classification-2`（残留旧版 ⇒ `403`） | `events.jsonl:660`（D2-114）；`summary.md §11.3.1` |
| **H8** | **`source/` 树任何变化 ⇒ 必须重新分类**：去掉/新增驱动（source-only 形态）、补 `.csproj`/`Driver.cs` 均触发（增量多项实证） | `events.jsonl:615`（D2-062）、`:846`（D2-197）；前篇 §2.7-B6 |
| **H9** | **`cp`/打包链失败静默致文件缺失**（D2-116 的 `MSB1009`）⇒ 打包步骤须**逐步校验产物存在** | `events.jsonl:666` |
| **H10** | **更正只追加**：`D2-236` 用 `CORRECTION` 事件**显式 supersede** 既有 `SOURCE_PRECHECK` 的"baseline valid and freezable"结论（**不改写历史**） | `events.jsonl:951` |
| **H11** | **平台条件解除须显式记录**：`D2-007` 用 `REOPEN` + `NOTE` 事件把"平台已修复"落盘，供 20 项批量重开引用 | `events.jsonl:1146,1148` |

### 2.8 重转 / 重跑前检查清单（以**前篇 §2.7** 为基线，**追加增量条目**）

> **仅列增量**；前篇 A1–A4 / B5–B6 / C7–C8 / D9–D14 / E15–E18 **继续有效**。

**A. 冻结阶段（追加）**
- A5. **判有无"合法可观察入口"**：库单元/纯元数据/非 main 包 ⇒ 记 `PREPARATION_GAP`，**不编造入口**（§2.3①；`§65`）。
- A6. **冻结输入须"真的会做事"**：`argv=[]` 回落读 stdin 的源 ⇒ 冻结**非空 stdin/argv + fixture**，否则观察退化（§2.3③）。
- A7. **预判"输出是否含主机运行态/job 特定路径"**：是 ⇒ 直接记 `ORACLE_NOT_FREEZABLE`（§2.5）。

**B. 分类阶段（追加）**
- B7. **回源逐处核对分类器报出的网络目标**（Metasploit URL/`report_note` type/版本号形似 IP）⇒ 若非真实调用，加 `--network-isolation-configured` 重分类（§3.3）。
- B8. **`source/` 树任何变化后**：删旧 `classification-1.json`、把新结果写入 `this-task-classification.json`（H7/H8）。

**C. 提交阶段（追加）**
- C9. **源预检 `buildCommand` 用 argv token 数组**（整串 ⇒ `[Errno 2]`）（§3.1）。
- C10. **Windows `runCommand` 用显式相对路径** `[".\\program.exe"]`（否则 `[WinError 2]`）（§3.1）。
- C11. **C# 目标 `artifactLanguage` 写 `csharp`**（§2.6）。

**D. 驱动阶段（追加）**
- D15. **生成含转义的驱动后先做语法自检**（D-11；**本增量 3 次实证**）。
- D16. **两侧观察面文件集合须同源**（共享中性 fixture cwd）（D-14②）。
- D17. **脚本型源可直接 `runCommand` 启动**；去驱动 ⇒ 重分类（D-14①）。

**E. 归因阶段（追加）**
- E19. **先查换行转义**（`SyntaxError` ⇒ 装置，非源缺陷）（D-11）。
- E20. **`mismatched` 的唯一 diff 若在 stderr 形态/退出码**，先判**语言运行时差异**（Go panic vs Python traceback；`ReadKey()` 装置态）（§2.1 F7、§2.5）。

---

## §3 评估平台侧建议

> **第三类诉求**：平台（源预检 / 分类器 / 提交端 / 比较器）在增量期暴露的问题及可改进点。每条给**影响面**与**出处**。**前篇已固化的结论（§3.1 消噪、§3.3 假阳性、§3.4 `semantic_pass`、§3.5 digest、§3.6 `stderrMode`）本文只回指，不重复。**

### 3.1 `source-only` 源侧预检形态（**新增**）

| 问题 | 事实 | 影响面 | 出处 |
|---|---|---|---|
| **新接口 `evaluationMode=build-only`** | `D2-197` 起改走 **`/api/source-preflights` + source-only capsule**（`source_preflight_manifest.json` + `input_profile.json` + `metadata.json` + 非空 `source/`，**无 target 树**）；`evaluationMode` 可为 `build-only` / `build-and-run` | 本增量 **D2-197 起全部** | `events.jsonl:846`；`items/D2-250.json → sourcePrecheck` |
| **`buildCommand` 必须是 argv token 数组** | 误写**单元素整串** `["go build -o program sort.go"]` ⇒ 平台按 argv 处理、把整串当可执行名 ⇒ `[Errno 2] No such file or directory`、`inconclusive`、7 ms（**源未被编译**）；改 argv token 数组后正常 | 首提即触发（D2-197） | `events.jsonl:847` |
| **Windows `runCommand` 须显式相对路径** | `["program.exe"]` ⇒ `exec launch-failed`（`[WinError 2]`）；改 `[".\\program.exe"]` ⇒ `completed/0` | Windows 源侧预检 | `summary.md §11.3.3`（D2-007） |
| **无驱动 ⇒ `source/` 树变化 ⇒ 必须重新分类** | source-only 形态去掉 `run_case.py` 后须重新分类（`classification-2`） | 本增量多项 | `events.jsonl:846`（D2-197）、`:615`（D2-062） |

- **建议**：① `buildCommand`/`runCommand` 的 **argv 数组**要求在 API 文档与错误信息中**前置说明**（现只能由 `[Errno 2]`/`[WinError 2]` 反推）；② `source-only` 与旧双侧形态**并存**，应在响应中**显式标注形态**，避免 §0.3 的引用歧义。

### 3.2 C# 目标 evidence-bundle 缺陷（**前篇 §3.2 → 已修复**）

- 前篇 §3.2 的 schema 缺限（`$.collectorDiagnostics.0.detail` 不被允许 ⇒ `INFRA_ERROR`）**已于 2026-10-11 复测修复**（`PROBE-RESULT.md`）。
- **新纪律**：C# 目标 `artifactLanguage` **须写 `csharp`**（非 `dotnet`），否则 `403 identity_mismatch`。
- **影响面**：前篇 §2.5 的 **38 项** C# 目标项**恢复可推进**（见本文 §2.6）。

### 3.3 分类器词法误判（**增量高频**，前篇 §3.7 的扩展）

> **本增量期最高频的平台侧问题**：**至少 18 项**因**词法误判**被判 `BLOCKED/public_network_unverified`，**全部**经**回源核对**确认非真实调用后加 `--network-isolation-configured` 重分类。**处置纪律**：回源逐处核对 → 重分类 `classification-2` → **删除误生成的 `classification-1.json`** → 新结果写入 `this-task-classification.json`（残留旧版 ⇒ `403`）。

| 误判形态 | 实例（taskId） | 出处 |
|---|---|---|
| **`using` 行**被当网络目标 | D2-114 | `events.jsonl:658,659` |
| **版本号形似公网 IP**（`TypeForwardedFrom`/`AssemblyVersion`） | `4.0.0.0`→D2-121, D2-122；`1.0.0.0`→D2-150 | `events.jsonl:691,694,802` |
| **usage/帮助文本里的示例 IP + 裸 `:`** | `192.168.1.10`（L541 帮助文本）→ D2-191 | `events.jsonl:825` |
| **docstring / 注释里的文档 URI** | `docs.python.org`→D2-235/241/253；`json.org`→D2-246/252；`zgp.org`→D2-241；`github.com`→D2-275 | `events.jsonl:920,937,947,972,976,1063` |
| **常量 / 打印串里的域名** | `github.com`（`APPREPO` 常量）→D2-236；`github.com`（`print()` sponsor banner, L217）→D2-256 | `events.jsonl:924,994` |
| **XML namespace** | `schemas.microsoft.com`（`xmlns`）→D2-253 | `events.jsonl:976` |
| **Metasploit `'References'` / 描述 URL / `report_note` type 串** | D2-287/292/293（References/描述 URL）、D2-298（`windows.antivirus` type 串 L48） | `events.jsonl:1100,1116,1120,1136` |
| **（对照）真实公网目标，非误判** | D2-184（L56 硬编码 `github.com` 下载）、D2-217（`aka.ms`/`githubusercontent.com` 真实下载） | `events.jsonl:805`；`README.md` D2-217 条目 |

- **建议**：hostname/网络目标启发式应**排除**：① 位于**字符串字面量/docstring/注释**中的 URL；② **版本号形式**（`\d+\.\d+\.\d+\.\d+` 且**非**合法网段）；③ **XML namespace**；④ **标识符型**串（如 `windows.antivirus`）。**并**在 `details.files[].network_targets` 中**保留原值 + 所在语句类型**，便于人快速判定（前篇 §3.7 处置纪律的延伸）。
- **另一类分类缺陷**：`D2-140` **首次分类用错 `sourceSha256`**（manifest 字段偏移）⇒ `BLOCKED/input_error`；修正后通过（`events.jsonl:772`）。

### 3.4 提交端 / 控制器（前篇 §3.8 的扩展）

| 问题 | 事实 | 出处 |
|---|---|---|
| **`controller_busy`** | 约 **10 分钟**忙拒；`jobCreated=false`；`/api/jobs` 列举返回 **405** | `README.md` D2-197 条目 |
| **陈旧分类件 ⇒ `403`** | 提交用旧 `this-task-classification.json`（`classification-1` 的 BLOCKED 版）⇒ `403`；须写最新 `classification-2` | `events.jsonl:660`（D2-114） |
| **`caseId`/`identity_mismatch`** | 前篇 §3.8 结论**继续有效**（C# 目标 `artifactLanguage` 为新触发点，见 §3.2） | 前篇 §3.8；§3.2 |

- **建议**：① `controller_busy` 应返回**可重试时间 / 队列位置**，并提供**只读的 job 列举接口**（当前 `/api/jobs` 405）；② `caseId` 与 `artifactLanguage` 的校验规则**前置说明**。

### 3.5 长路径（>260 字符）

| 问题 | 事实 | 影响面 | 出处 |
|---|---|---|---|
| **`Compress-Archive` 在长路径失败** | 用例目录全路径 **>260 字符** ⇒ `ZipArchiveHelper: 未找到路径…的一部分` ⇒ **改在系统临时短目录组装并打包** | SharpUp 簇（D2-139~149 等多项） | `events.jsonl:770`（D2-139）；`README.md` D2-139 条目 |
| **Python `open()` 须加 `\\?\` 前缀** | 超长路径下 Python `open()` 失败，须加 `\\?\`（bash/curl/Write 工具正常） | D2-130 首次遇到 | `README.md` D2-130 条目 |

- **建议**：平台/工作流层**统一在短临时目录组装 capsule**（已在实践中生效）；或**支持 Windows 长路径模式**。

### 3.6 `digest` 与 `normalizedText` 的差异语义（前篇 §3.5 **再证**）

- `D2-109`：两侧 `normalized-text` **逐字节相同**、`diffs=0`，但 **digest 不同**（CRLF vs LF 被**归一**吸收）⇒ 平台按 preset **先消噪再比较**。**结论同前篇 §3.5**：报告/API 应把「**已消噪的可比面**」与「未消噪的 digest」在**不同字段**呈现。

### 3.7 本文**未新增**、沿用前篇的结论（**回指，不重复**）

- **消噪记号覆盖不足**（`duration_ms`/源侧绝对路径/`archive_bytes`）——见前篇 §3.1；增量期**无新增实例**（增量 `mismatched` 均由 `ORACLE_NOT_FREEZABLE`/装置态解释，见 §2.5）。
- **`matched` 假阳性 / `stderrMode` 无"忽略"档 / `semantic_pass` 档位语义**——见前篇 §3.3/§3.4/§3.6；增量 `semantic_pass` 6 项（D2-117/123/124/125/126/130）**均**唯一 `minor` diff = `执行时间`（`timestamps` 覆盖），**不引入新问题**。

---

## §4 溯源索引与未决项

### 4.1 增量逐项去向索引（141 项，含出处指针）

> 明细以 `items/<taskId>.json` 为准。下表按去向分组给**摘要 + 关键出处**，便于回读。

| 去向分组 | 数量 | taskId | 关键出处 |
|---|---:|---|---|
| **`matched`** | 12 | D2-063, 064, 109, 111, 128, 133, 199, 247, 254, 256, 269, 270 | 各 item `verdicts.comparison` |
| **`semantic_pass`** | 6 | D2-117, 123, 124, 125, 126, 130 | 各 item `evaluation.onlyDiff`（唯一 `minor` = 时间戳） |
| **`mismatched`（装置残留 / 不可冻结）** | 5 | D2-116, 118, 134, 194, 207 | §2.1 F7、§2.5 |
| **`SOURCE_DEPENDENCY_GAP`** | 75 | ①(8) D2-110, 112, 114, 115, 121, 122, 129, 136；②(17) D2-127, 131, 132, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 222；③(6) D2-185, 187, 192, 195, 197, 208；④(1) D2-196；⑤(11) D2-188, 191, 200, 201, 204, 205, 206, 209, 211, 212, 213；⑥(18) D2-235, 238, 239, 240, 243, 249, 250, 253, 255, 259, 260, 264, 266, 267, 268, 271, 273, 274；⑦(1) D2-135；⑧(13) D2-120, 275, 285, 287, 288, 289, 290, 292, 293, 294, 298, 299, 300 | §2.2.1 |
| **`PREPARATION_GAP`** | 38 | ①(31) D2-150, 186, 189, 190, 193, 198, 202, 203, 245, 246, 252, 257, 261, 262, 263, 265, 272, 276, 277, 278, 279, 280, 281, 282, 283, 284, 286, 291, 295, 296, 297；②(4) D2-210, 232, 233, 258；③(2) D2-236, 241；④(1) D2-107 | §2.3 |
| **`SOURCE_NOT_BUILDABLE`** | 2 | D2-119, 251 | §2.2.2 |
| **`BLOCKED`（真实公网）** | 2 | D2-184, 217 | §3.3 末行 |
| **`WAITING`/`FROZEN`（唯一）** | 1 | D2-065（`powershell-to-csharp`，C# 目标平台，见 §2.6） | `items/D2-065.json` |

> **`PREPARATION_GAP` ① 的 31 项**（完整）：D2-150, 186, 189, 190, 193, 198, 202, 203, 245, 246, 252, 257, 261, 262, 263, 265, 272, 276, 277, 278, 279, 280, 281, 282, 283, 284, 286, 291, 295, 296, 297。

### 4.2 旧项增量更新（前篇快照内、增量期发生变化的项）

| taskId | 增量事实 | 指向 |
|---|---|---|
| **D2-007** | **C# 目标平台缺陷修复后重开试点**：重分类 `2.4 ALLOWED`；新源预检 `eval-20261012-061842-037c6549` build/exec `completed/0`；**因观察面含构建产物（`program.exe`）两侧不对称、未继续生成** ⇒ **如实保持 `WAITING`** | `events.jsonl:1146,1148`；前篇 §2.5/§3.2；本文 §2.6 |
| **D2-062** | **装置故障修正后收口**：`DRIVER_FIX`（重写两侧驱动，去除未定义 `SIDE`、修正互换两侧）→ 重分类 → `job-00b`/`job-01`；终态 **`PARTIAL`/`ORACLE_NOT_FREEZABLE`**（唯一 `major` diff = 动态回环端口 `127.0.0.1:34487` vs `:35553`，`ephemeral-ports` 未吸收）⇒ 同 D2-044（纪律 §15/§10.16） | `events.jsonl:614,615,619,620`；前篇 §2.3 D-10 的续篇 |

> **不重复**：`D2-063`/`D2-064`/`D2-065` 已计入 §4.1 增量（`matched`/`matched`/`WAITING`），前篇未覆盖，故**不属旧项更新**。

### 4.3 未决项（承接 `summary.md §11.4`，**带进下一轮**）

**31 项 `WAITING`**：

| 类 | 项 | 恢复条件 |
|---|---|---|
| **C# 目标 `BLOCKED_ENV`（20）** | `D2-007~012, 030, 048~051, 065, 076~078, 156~160` | **平台缺陷已于 2026-10-11 修复 ⇒ 恢复条件已具备**；恢复动作 = **逐项跑全链**（重分类 → 源预检 → 生成 → 自审 → 双侧提交 → 取证）；`D2-007` 试点须**先解决观察面/装置对称性**（§2.6） |
| **真实公网 `BLOCKED`（5）** | `D2-055, 074, 083, 184, 217` | 取得**可验证的网络阻断/重定向**证据后**重新分类**（`D2-074` 另属分类器 hostname 误判待修，§3.3） |
| **`RUN_SAFETY_NOT_READY`（2）** | `D2-082, 108` | 硬编码非 loopback 目标，须隔离证据 / 受控输入 |
| **`DRIVER_NOT_VIABLE`（3）** | `D2-167, 169, 175` | 须**合法来源驱动** |
| **只读 FS 环境缺口（1）** | `D2-069` | 源写只读 `/usr`，须新冻结条件 |

- **下一轮增量对账**：`reconciliation-7.md` 在**终态 280** 触发（当前 246）。
- **批次状态**：**未 `CLOSED`**（存在 31 项 `WAITING`）。

### 4.4 本文的核对方式与局限

- **核对方式**：本文数字均来自**只读解析**（`items/*.json`、`events.jsonl`、`self-review-N.json` 的字段统计），出处格式统一为 `文件 §节` / `items/<id>.json → 字段` / `events.jsonl:<行>`。**增量边界**由 `events.jsonl:1~613` 与 `:614~1148` 的 taskId 差集**精确划定**（141 项）。
- **局限**：
  1. 本文**不重复抄录** evidence 原文；`04-evaluation/.../evaluation_report.*`、`comparison.json` 等证据层的**逐字段**内容需回读对应 job 目录。
  2. **形态断代**（§0.3）造成的引用歧义：前篇 §2.3 装置缺陷 / §3.8 提交端纪律**仅适用于旧双侧形态**；source-only 形态下"驱动"已消失，相关纪律须按 §3.1 重述。
  3. **`events.jsonl` 有 2 行自身不可解析**（`events.jsonl:650` 含换行、`:915` 含未转义反斜杠路径）——**内容已单独读出并引用**（D-11、§2.3②），但其 JSON 格式缺陷**本身就是一处平台/记录缺陷**（建议平台侧对 note 做转义）。
  4. 本文基于 2026-10-12 的快照；批次**未关闭**，新项会新增素材。前篇 §4.3 的局限**继续有效**。
