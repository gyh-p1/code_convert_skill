# dataset-2 已完成用例：三类优化输入（自审 / 失败重转 / 评估平台）

> **用途**：为优化「转换系统（生成 + 自审）」与「评估平台」提供**可溯源**的输入材料。
> **编制时点**：2026-10-11，基于 `batch/items/` 的 **136 项**记录与 `events.jsonl` 的 **613 行**事件。
> **纪律**：本文每条结论均附出处（`文件 §节/行`、`items/<taskId>.json`、`events.jsonl:<行>` 或 `taskId → 字段`）。**无出处者不写入，未核实者标注「待核」。**
> **本文与 [`summary.md`](summary.md) 的关系**：summary 是**批次级问题台账**（§1 按 A–H 分类）；本文按「**自审 / 失败重转 / 评估平台**」三个**面向优化的视角**重组同一批事实，并补足 summary 之后的增量用例（D2-152~183）与逐项证据出处。二者互补，**不互相取代**。

---

## §0 口径与出处

### 0.1 覆盖范围（实测计数）

| 维度 | 分布 | 出处 |
|---|---|---|
| items 总数 | **136**（`batch/items/*.json`） | 实测 `ls batch/items` |
| lifecycle | `DONE 92` / `WAITING 28` / `PARTIAL 15` / `NOT_STARTED 1` | 逐项 `items/*.json` 统计 |
| disposition | `FROZEN 64` / `CONVERTED 36` / `SOURCE_NOT_BUILDABLE 20` / `SOURCE_DEPENDENCY_GAP 13` / `BLOCKED 2` / `BLOCKED_ENV 1` | 同上 |
| `verdicts.comparison` 首词 | `UNVERIFIED 65` / `matched 47` / `mismatched 7` / `inconclusive 6` / `semantic_pass 5`（+1 项 D2-024 为分路径描述） | 同上 |
| `evaluation.verdict`（有独立评估记录的 35 项） | `matched 24` / `semantic_pass 5` / `mismatched 6` | 同上 |
| events.jsonl | **613 行**、事件类型 **80+ 种** | 实测 |
| self-review 产物 | **67 份** `self-review-*.json`（含 2 份二轮） | `**/03-self-review/self-review-*.json` |

> **口径边界**：`SOURCE_NOT_BUILDABLE` / `SOURCE_DEPENDENCY_GAP` / `BLOCKED_ENV` **均非转换失败**；`WAITING` 不计入终态（终态 = `DONE` + `PARTIAL`）。本文**不合成单一「成功率」**（纪律见 `summary.md` §8）。

### 0.2 出处层级（本文引用格式）

| 层 | 路径 | 本文用于 |
|---|---|---|
| 调度层 | `items/<taskId>.json`（字段级） | 逐项去向、自审浓缩、失败归因、`pendingAction` |
| 调度层 | `events.jsonl`（事件名 + **行号**） | 失败 / 修复 / 更正事件流 |
| 证据层 | `<case>/output/batch/03-self-review/self-review-1.json` | **自审原因与建议的原始出处**（`verdict` + `items[].origin/issue/proposed_fix/risk`） |
| 证据层 | `<case>/output/batch/04-evaluation/job-*/returned-evidence/*` | 平台判据（`evaluation_report`、`comparison.json`、`evidence-source.json`） |
| 底稿层 | `summary.md`、`operational-discipline.md`、`reconciliation-1/2.md`、`pattern-note-*.md`、`platform-blocker-csharp-target.md` | 已固化的纪律与优化点（本文以「章节号」引用） |

---

## §1 自审原因与建议

> **第一类诉求**：自审（模型对生成目标的静态复核）给出了什么原因、什么建议，以及它们是否可信。
> **原始出处**：67 份 `<case>/output/batch/03-self-review/self-review-1.json`，结构为 `{verdict, reviewedScope, items:[{id, location, evidence, origin, issue, proposed_fix, risk}]}`。

### 1.1 自审产出规模与档次

| 指标 | 值 | 出处 |
|---|---:|---|
| self-review 文件总数 | 67（其中 `self-review-2.json` 二轮 2 份：`c-to-python/D2-177`、`cpp-to-c/handoff-d07-fake-cred-loader`） | 实测 glob |
| `NO-REPAIR-IDENTIFIED` | **55** | 逐份 `verdict` 统计 |
| `REPAIR-RECOMMENDED` | **11** | 同上（清单见 §1.2） |
| JSON 无法解析（格式缺陷） | **1**（= **D2-003**，`cpp-to-c/handoff-2026-10-02-d07-env-discovery-report-cpp`） | 实测：该文件 `verdict=NO-REPAIR-IDENTIFIED` 开头合法，但整体 `json.load` 失败；taskId 经 `manifest.csv:4` 核实 |

**关键观察**：绝大多数自审（55/67）结论为 `NO-REPAIR-IDENTIFIED`，且**只做静态对照**（`reviewedScope` 反复声明 "static … only / 仅静态阅读，未编译、未运行"）。这直接体现为 items 的 `coverageGap` 里大量 "static review only" 语（如 `items/D2-016.json`、`items/D2-176.json`）。→ 自审**不能替代行为验证**。

### 1.2 自审命中的「转换引入」缺陷（11 项 `REPAIR-RECOMMENDED` 的原始建议）

> 出处：各 case 的 `03-self-review/self-review-1.json`（`items[].origin=conversion-introduced` + `proposed_fix`）。「后续」列来自 `items/*.json` 的 `repairChain` 与 `events.jsonl`。

| case / taskId | 自审提出的差异（原因） | 自审建议（`proposed_fix`） | 后续处置（出处） |
|---|---|---|---|
| **D2-176** (c-to-python pwd) | 未知选项时目标**缺 libc `getopt` 诊断行**（源会先输出 `pwd: illegal option -- x`） | 捕获 `GetoptError` 后写平台相应诊断，或记为可接受的工具链差异 | **未修**：源侧该串尚未观察到，**不猜**（`items/D2-176.json` → `coverageGap`） |
| **D2-177** (c-to-python which) | ①字节长度 vs 字符长度（2 处）②未知选项 stderr 少一行 ③`which sh -a` 因 `getopt` 不重排而把 `-a` 当文件名 | 用 `len(os.fsencode(...))` 比字节；写 glibc 风格诊断；改用 `getopt.gnu_getopt` | **已修**（3 行），`self-review-2` 确认收敛（`events.jsonl:90`；`items/D2-177.json` → `repairSummary`） |
| **D2-180** (c-to-ruby rc4) | `argc` 守卫 off-by-one（照抄 `!= 3`，但 `ARGV` 不含程序名）；fallback 语义丢失 | `!= 3` → `!= 2`；用 `$PROGRAM_NAME` | **已修**（`events.jsonl:318`） |
| **D2-032**（c-to-ruby/d05-linux-c） | ①`Process.fork` 的 `nil`（子进程）被当成 C 的 `fork()==-1` ②`execve` 的 `envp=NULL` 语义（需 `unsetenv_others: true`）③exec 失败码 0→异常 | 按 Ruby 返回语义改写；用 `Kernel.exec(..., unsetenv_others: true)` | **已修**（`items/D2-032.json` → `repairChain`；但属**未被覆盖的反向 shell 路径**，仅静态） |
| **D2-004**（cpp-to-c/d07-fake-cred-loader） | 目标把文本模式 `ifstream` 改成 `fopen("rb")`，CRLF 空行**多计数** | `fopen(path, "rb")` → `fopen(path, "r")` | **已修**，`self-review-2` 确认（`events.jsonl:20`） |
| **D2-088** (cpp-to-powershell resource_manifest_builder) | CRLF（行尾字节） | 补齐 CRLF | **已修**（`items/D2-088.json` → `selfRepairRounds=1`） |
| **D2-092** (cpp-to-powershell winhttp_impl) | 第 107 行**悬空标记 `printf_pid:`** 被 PowerShell 当命令 → stderr 非空、退出码非 0 | **删除整行** `printf_pid:`（保留其后的 `[Console]::Out.Write`） | **评估后修复 1 轮 → `matched`**（`events.jsonl:403`；`items/D2-092.json` → `repairChain`） |
| **D2-016**（cpp-to-powershell/d12-loopback-send） | Windows 文本模式 `std::endl` 输出 CRLF，目标只写 LF | 写 `[Environment]::NewLine`（或 `` `r`n ``） | **未修**：被 `normalized-text` 消噪吸收（`items/D2-016.json` → `selfReviewNote`） |
| **D2-022**（csharp-to-python/d15-dump-cs） | ①`print` 在 Windows 把内嵌 `\n` 翻成 CRLF，C# `Console.WriteLine` 只对行尾补 CRLF ②`Enum` 被降级为类属性 | `sys.stdout.reconfigure(newline='')` + 显式 `\r\n`；用 `enum.Enum` | **已修**（`events.jsonl:459`） |
| **D2-023**（csharp-to-ruby/d17-describe-cs） | ①`WriteLine` 追加的 CRLF 被遗漏（字面量已以 `\r\n` 结尾）②`[X]` 分支终止符漏写 ③"读一键"仅近似（多等一个回车） | 各补 `\r\n`；TTY 分支改 `io/console` 的 `getch` | **已修**（`events.jsonl:466`） |
| **D2-061**（go-to-ruby/d29-inbox-batch-validate） | ①Ruby `[[:space:]]` 比 Go `unicode.IsSpace` 多去若干 Unicode 空白 ②只查 `TMPDIR`，Go 还查 `TMP`/`TEMP` | 用显式字符集 `/[\t\n\v\f\r  ]/`；`temp_dir` 依次查 `TMPDIR`/`TMP`/`TEMP` | **误判**：该 2 项实为**装置故障**所致（驱动 `\n` 写成真换行）；修正驱动后同一 `target.rb` **逐字节 `matched`**，`selfRepairRounds=0`（`events.jsonl:606,607`；`items/D2-061.json`） |

**汇总（可直接并入生成提示词的「高频误译模式」）**：
1. **行尾字节（CRLF/LF）**：4 例（D2-004、D2-088、D2-022、D2-023）。文本模式语义在跨语言映射时**最易错**。
2. **`argv`/`argc` 下标基数**：D2-180（C 含 `argv[0]`，Ruby `ARGV` 不含）。见 §2.1 F1。
3. **`getopt` 未知选项诊断**：3 例（D2-176、D2-177、D2-183）——目标普遍**不产出 libc 风格的 `illegal option` 行**。
4. **字节长度 vs 字符长度**：D2-177（非 ASCII 路径）。
5. **悬空标记 / 翻译残留行**：D2-092（`printf_pid:`）。见 §2.1 F2。
6. **临时目录环境变量语义**：D2-061（`TMPDIR` vs `TMP`/`TEMP`；该条为误判）。
7. **`fork` 返回语义与 `execve` 环境**：D2-032。

### 1.3 自审的盲区、误判与格式缺陷

| 类 | 事实 | 出处 |
|---|---|---|
| **误判（把装置故障当成转换缺陷）** | D2-061 自审报 `REPAIR-RECOMMENDED`（2 项：Unicode 空白、`TMPDIR`/`TMP`/`TEMP`，即 §1.2 表末行），实际根因是**驱动里 `\n` 写成真实换行**（target.rb 从未执行）——修正驱动后同一 `target.rb` **逐字节 `matched`**，**未消耗任何模型修复调用** | `events.jsonl:606`（`SELF_REVIEW`）、`events.jsonl:607`（`DEVICE_FAULT`） |
| **正确的"不猜"** | D2-176/D2-183 自审把"未知选项路径的中间词"标为 `toolchain-unknown`，**未提出改动**；D2-176 明确"源侧该串尚未观察到 ⇒ 不修" | `03-self-review/self-review-1.json`（D2-176 items #1、D2-183 #8） |
| **自审只做静态对照** | 55/67 份 `verdict=NO-REPAIR-IDENTIFIED`，且 `reviewedScope` 声明未编译/未运行 ⇒ 覆盖缺口只能靠 `coverageGap` 事后补充 | 各 `self-review-1.json` 的 `reviewedScope` |
| **自审响应格式缺陷** | `D2-093` 自审 JSON **损坏**（未转义引号/控制字符）；`D2-096` 被 ```json **围栏包裹**；`D2-181` **invalid JSON escapes**；`cpp-to-c/d07-env-discovery` 整份**不可解析** | `events.jsonl`（`items/D2-093.json` → `schedulingNote`、`items/D2-096.json` → `schedulingNote`、`items/D2-181.json` → `schedulingNote`） |

### 1.4 给「生成 + 自审」的优化建议（由 §1.2/§1.3 导出）

1. **提示词显式列出高频误译模式**：行尾字节、`argv` 下标基数、`getopt` 诊断、字节/字符长度、临时目录变量（§1.2 七类）。
2. **自审提示词增加"未观察即不猜"规则**：D2-176 的做法是**正确范式**——只在有源侧实测串时才提议改；否则登记为 `toolchain-unknown`（`self-review-1.json` D2-176 #1）。建议固化进自审 instruction。
3. **自审输出强制"只一个裸 JSON 对象"**：H2 型格式缺陷（D2-093/096/181）经提示词修正后显著减少。出处：`summary.md` §H2。
4. **自审必须声明"是否行为验证过"**：当前 `reviewedScope` 已含，但 `verdict` 未区分"静态无疑"与"已实测"⇒ 建议在自审结论中增加**证据等级**字段（静态 / 实测）。
5. **不可把自审 `REPAIR-RECOMMENDED` 当"确有缺陷"**：D2-061 实证装置故障会被自审误判 ⇒ 自审建议须先过**装置对称性核查**（§2.3）再采纳。

---

## §2 各类失败与重新转换建议

> **第二类诉求**：出现了哪些失败、如何归因、重转前要做什么检查。
> **总口径**：失败**必须分五类**，不得混算（`summary.md` §1 C/D/F/G），**源侧拦截与已评估项分列**。

### 2.1 真实转换缺陷（由第三方证据坐实，闭环 = 反例→定位→最小修复→复测）

| 编号 | taskId | 方向 | 缺陷 | 反例证据 | 修复 | 复测 |
|---|---|---|---|---|---|---|
| **F1** | D2-180 | c-to-ruby | `ARGV` 下标基数（C `argv` 含程序名、Ruby 不含） | `target.rb:113 undefined method 'bytesize' for nil`；源 `Plaintext`/0 vs 目标 空/1 | 2 行：`argv[1]→argv[0]`、`argv[2]→argv[1]` | job-02 `matched`（`items/D2-180.json` → `repairChain`；`events.jsonl:320`） |
| **F2** | D2-092 | cpp-to-powershell | 第 107 行**悬空标记 `printf_pid:`** 被当命令执行 | `The term 'printf_pid:' is not recognized…` @ `target.ps1:107`（stdout 已匹配） | 删除该行（单行 diff） | job-02 `matched`（`events.jsonl:403`） |
| **F3** | D2-093 | cpp-to-powershell | payload 十六进制**少一位**（625 奇数位 vs 源 626 位） | `MethodInvocationException` @ `target.ps1:54`（`Substring` 越界）；第 1 轮**未收敛** | 定位到 `e8d00000` 之后少一个 `0` | job-02 `matched`（`events.jsonl:409,410`） |
| **F4** | D2-022 | csharp-to-python | 文案**误译** `(All Users)`→`(Current User)` | stdout 逐字节比对抓出 | 恢复 `All Users` + 复现 stdin 非 TTY 首行 | job-02 stdout/stderr 首行逐字节一致（`events.jsonl:461`） |
| **F5** | D2-025 | c-to-cpp | `switch` 内**跨初始化跳转**（C 合法、C++ 非法） | `networking_quarks.cpp:540 jump to case label crosses initialization of 'int status'`（537 行）；首版与 C 源逐行相同 | `default:` 分支加花括号（逻辑未改） | `events.jsonl:190,191` |
| — | D2-004 | cpp-to-c | CRLF 空行**多计数**（`fopen` 二进制模式） | 自审命中 | 1 行：binary→text | `events.jsonl:20` |
| — | D2-177 | c-to-python | 字节/字符长度 + GNU `getopt` 重排 | 自审命中（3 项） | 3 行 | `events.jsonl:90` |

**优化点**（出处：`summary.md` §1 F、各 item `repairChain`）：
- C→解释型语言时，**`argv` 下标基数是首查项**（F1）。
- 脚本型目标提交前，**扫一遍"裸标记行"**（F2）。
- "少一位"型 hex/payload 错误**极隐蔽**：修复前必须先量化（位数/字节数/差异位点）再交模型，否则模型只"差不多"地改（F3）。
- 涉及**长文案**的转换，契约里给**逐字节基线**（F4 用了十六进制基线，效果最好）。
- C→C++ 的"契约差异（加标志）vs 真实缺陷（改代码）"必须**分离实验**（F5；判据见 `operational-discipline.md` §10.17）。

### 2.2 源侧拦截（**均非转换失败**，0 模型调用）

| 去向 | 数量 | 清单（taskId） | 出处 |
|---|---:|---|---|
| `SOURCE_NOT_BUILDABLE` | **20** | D2-027, 028, 073, 075, 152, 154, 155, 162, 163, 164, 165, 166, 168, 170, 171, 172, 173, 178, 179, 182 | 逐项 `disposition` |
| `SOURCE_DEPENDENCY_GAP` | **13** | D2-070, 071, 079, 080, 081, 084, 085, 086, 087, 100, 102, 153, 161 | 逐项 `disposition` |

**出口判据表**（出处：`pattern-note-bsd-userland.md`、`pattern-note-abseil-library-units.md`）：

| 诊断形态 | 性质 | 处置 |
|---|---|---|
| `fatal error: absl/...`（第三方库头） | 快照外文件 | `SOURCE_DEPENDENCY_GAP`（Abseil 簇 7 项：D2-079~081、084~087） |
| `fatal error: <项目伴随头> 且仓库内可找到` | **打包缺口**（可修） | 补回、重测（D2-025 `atoms.h`、D2-029 `arg.h`、D2-175/180 `WjCryptLib_Rc4.*`） |
| `fatal error: <项目伴随头> 且穷举不可找到` | 快照外文件 | `SOURCE_DEPENDENCY_GAP`（D2-161 `vary.h`，三重穷举 0 命中） |
| `implicit declaration of getopt`（严格 ISO C 下） | **契约缺陷** | 改用 `-std=gnu11` 后重跑 |
| `expected ... before '__dead2'` / Capsicum / libxo / sysctl | FreeBSD 专有接口 | `SOURCE_NOT_BUILDABLE`（D2-162~166） |
| `err.h 缺失于 windows 但存在 linux` | 平台差异 | **两个候选都实测**再定案（D2-027 实验 A/B/C） |

**优化点**（出处：`summary.md` §1 C）：
- `SOURCE_NOT_BUILDABLE` vs `SOURCE_DEPENDENCY_GAP` **必须分列**；判"快照外文件"前**先走三问**（旧 dataset 有吗？哈希吻合吗？仓库内能补吗？）——`operational-discipline.md` §9。
- **BSD/FreeBSD 源码的候选集合必须含 macOS**：D2-151/176/183 在 macOS 上**可构建**（`pattern-note-bsd-userland-macos-correction.md`）。
- **不补桩、不伪造宏、不删 `#include`、不放宽命令**（`pattern-note-bsd-userland.md` 反面纪律）。

### 2.3 装置 / 驱动缺陷（**假阳性 / 假阴性最大来源**）

> 一字总则：**驱动的唯一职责是「启动、等待、采集、终止」，采集 = 原样透传字节**（`operational-discipline.md` §6）。

| 编号 | taskId | 缺陷形态 | 后果 | 出处 |
|---|---|---|---|---|
| D-1 | D2-013 | 驱动把子进程 stdout **包进 JSON 字符串**，真实 CR 变转义序列 | 假 `mismatched`（改原样透传后 matched） | `operational-discipline.md` §6；`events.jsonl:38,39,40` |
| D-2 | D2-031 | 驱动只找 `program.exe/program`，**脚本型** `target.py` 找不到 | 假 FAIL（FileNotFound） | §7；`events.jsonl:81,82` |
| D-3 | D2-177 | 驱动**未把冻结 argv 转发**给被测程序 | **假阳性** `matched`（两侧都走 usage） | §8；`events.jsonl:91` |
| D-4 | D2-058 | 驱动**后处理只挂脚本分支**（不对称） | 假 `mismatched`（两侧程序 stdout 其实相同） | §10.13 |
| D-5 | D2-024 | 常驻服务在 `terminate()` **之后**才读流，全缓冲 stdout 丢失 | 两侧全空 → **假阳性** `matched` | §10.9；`events.jsonl:114` |
| D-6 | D2-029 | 空 argv 走进 stdin 空转分支；驱动 `stdin=PIPE`+`input=` 冲突 | 假 `matched` + 假 `mismatched` | §10.1、§10.2；`events.jsonl:106` |
| D-7 | D2-103 | 被观察量是**目录条目数**，`ruby -c` 不产出文件 ⇒ 3 vs 2 | 假 FAIL | §10.19；`events.jsonl:207` |
| D-8 | D2-003 | `filesystemInclude: **/*` 把**构建产物**扫进比较 | 假 FAIL | §1；`events.jsonl:14` |
| D-9 | D2-061 | **本次驱动**把 `\n` 写成真实换行（`SyntaxError`），target 从未执行 | 假 FAIL；**并致自审误判** | `events.jsonl:607` |
| D-10 | D2-062 | 驱动模板引用**未定义变量 `SIDE`** ⇒ `NameError` | `exec=1`（**非源缺陷**） | `events.jsonl:612` |

**优化点（重跑前必查的「装置对称性」五问，出处：`operational-discipline.md` §10.6/§10.13/§10.18/§10.19）**：
1. **输入送达**：驱动是否把冻结 argv 原样转发？（§8）
2. **两侧都跑到被观察状态**：源侧观察是否**非空且非退化**？（§10.6）
3. **引用对象两侧都在**：argv 点名的文件/目录在 source 与 target 树中**都存在且一致**？（§10.18）
4. **被统计量两侧相等**：目录条目数/文件数按**构建命令实际产出**推算（勿假设"两侧都生成可执行文件"）（§10.19）
5. **后处理两侧一致**：后处理（回显/拼接/归一化）不得只挂一侧（§10.13）

### 2.4 oracle 不可冻结（`PARTIAL`，**非失败、非通过**）

| taskId | 不可复现的可观察量 | 出处 |
|---|---|---|
| D2-017 | `scan_ms` + 统计工作目录内容（装置不对称） | `items/D2-017.json` → `evaluationReadiness` |
| D2-018 | `elapsed_ms` | `items/D2-018.json` |
| D2-066 | 网卡收发字节（活动计数器） | `items/D2-066.json` |
| D2-072 | PID + ASLR 指针 | `events.jsonl:353` |
| D2-089 | 源执行 0 字节 stdout/stderr（**完全无输出**） | `events.jsonl:386` |
| D2-090 | ASLR 指针 + `MessageBoxA` 阻塞 | `events.jsonl:390` |
| D2-094 / 098 / 099 / 101 | 无输出 / 动态 PID / 危险副作用 | `events.jsonl:413,431,433,439` |
| D2-167 / 169 / 175 | `MessageBox` 阻塞 / 无 main（需伪造 PE）/ 无 main | `events.jsonl:275,283,304` |
| D2-042 / 043 / 044 / 045 | `duration_ms`（+ 动态端口 / `archive_bytes` / `mod_time`） | `events.jsonl:516,523,530,538` |
| D2-054 | `duration_ms`（PowerShell 子进程启动开销） | `items/D2-054.json` |

**判据**（出处：`operational-discipline.md` §10.16、§15）：可观察量含**两次执行间不可复现**的成分，且**不在**服务器消噪记号（`temporary-paths`/`timestamps`/`ephemeral-ports`）覆盖内 ⇒ **该 oracle 不可冻结** ⇒ 记 `UNVERIFIED` + `ORACLE_NOT_FREEZABLE`，lifecycle `PARTIAL`，**保留平台原 verdict**、**不重复重提求变绿**。

**优化点**：**冻结阶段就判**可观察量是否可复现（本批 12+ 项因此 **0 模型调用**跳过）。需该路径结论时**另冻条件**使数值确定化（属**新冻结条件**，不回改历史）。

### 2.5 平台阻断（C# 目标）

| 项 | 事实 | 出处 |
|---|---|---|
| G1 | 所有 `targetLang=csharp` 的 job 以 `INFRA_ERROR`（`AGENT_UNAVAILABLE`；`EvaluationContractError: …collectorDiagnostics.0: Additional properties are not allowed ('detail' was unexpected)`）终止，目标侧 preflight **SKIPPED**；对照实验：仅把目标语言改为 `c` ⇒ `COMPLETED` | `platform-blocker-csharp-target.md`；`events.jsonl:32,33,34,35` |
| 影响面 | **38 项**（cpp-to-csharp 12 / go-to-csharp 9 / c-to-csharp 6 / python-to-csharp 6 / ruby-to-csharp 4 / powershell-to-csharp 1），占 13.7% | `platform-blocker-csharp-target.md` |
| 处置 | 不改目标代码、不自行改判；受影响项 `WAITING / BLOCKED_ENV`，**0 模型调用**（`events.jsonl:555,559,563,567`）；平台修复后按原契约重提 | 同上 |

### 2.6 流程 / 记录类

| 项 | 事实 | 出处 |
|---|---|---|
| H1 | `D2-088` 有 item 无事件 ⇒ 追加 `BACKFILLED_EVENT`（不改写历史） | `events.jsonl:435`；`reconciliation-2.md` §3 |
| H2 | 模型输出格式缺陷（D2-093/096/181）按纪律 §2 用转义扫描/正则恢复，保留原文 | `reconciliation-2.md` §4；`items/D2-093.json` |
| H3 | 用**方向级**判断会漏 REUSE `handoff-*` 形态用例（D2-016/E2-017 曾被漏）；须**从 manifest 逐行重推** | `events.jsonl:449`（`SWEEP_BACKFILL`） |
| H4 | 改记录只**追加**（`LOG_CORRECTION` 仅清理重复行，未改判定） | `events.jsonl:355` |
| H5 | `caseId` 必须等于分类的 `case`（= taskId），带前缀会 403 `identity_mismatch` | `operational-discipline.md` §12；`events.jsonl:571` |
| H6 | 分类器输入哈希**大小写敏感**，须原样取 manifest | `operational-discipline.md` §10.20；`events.jsonl:225,226` |

### 2.7 重转 / 重跑前检查清单（编号化，可直接并入转换 SOP）

**A. 冻结阶段**
1. 判可观察量是否**可复现**；含活动计数器/耗时/ASLR/PID/随机路径 ⇒ 记 `ORACLE_NOT_FREEZABLE`（§2.4）。
2. 冻结 argv 时确认"这条路径**真的会做事**"（空 argv 回落 stdin 要另行冻结 stdin）（`operational-discipline.md` §10.1）。
3. argv 引用文件，**两侧树都放同名同内容 fixture**（§10.18）。
4. oracle 须有**独立外部依据**（jobId + argv + 观察值）（§10.4）。

**B. 分类阶段**
5. `sourceSha256` **原样复制** manifest（大小写敏感）（§10.20）。
6. **任何 `source/` 树变更**（含 `run_case.py`、补 `.csproj`）⇒ **必须重新分类**（§12、§13）。

**C. 提交阶段**
7. `caseId` = taskId（四处一致）（§12）。
8. 请求体由**确定性 JSON 构造器**生成并 round-trip 校验（§3）。

**D. 驱动阶段**
9. 原样透传子进程 stdout/stderr **字节**（§6）。
10. 按目标**语言形态**选启动方式（编译型/脚本型都要有双侧同型实测）（§7）。
11. **转发冻结 argv**（§8）。
12. 后处理**两侧一致**（§10.13）。
13. 常驻服务在**存活期内**采集（§10.9）。
14. 目录条目数按**构建命令实际产出**推算（§10.19）。

**E. 归因阶段**
15. 归因"转换引入"前，**先排除**：输入不等价、文件不存在、路径不可写、环境差异、**装置故障**（§10.18）。
16. 两侧同时"空输出 + 非零退出" ⇒ **先判装置可疑**（§10.6）。
17. `mismatched` 未定位到**语句**时，先做单因素定位实验再交模型；**不连问同一模型同一句话**（§10.5）。
18. 同一路径**连续 2 次**装置失败即停，记 `UNVERIFIED`（§10.12）。

---

## §3 评估平台侧建议

> **第三类诉求**：平台（比较器 / 消噪 / 采集器 / 分类器 / 提交端）暴露的问题及可改进点。每条给**影响面**与**出处**。

### 3.1 消噪记号覆盖不足

| 问题 | 事实 | 影响面 | 出处 |
|---|---|---|---|
| **执行耗时未消噪** | `duration_ms` 属活动计数器类，平台显式 token **仅** `temporary-paths`/`timestamps`/`ephemeral-ports`，**不含耗时**；`tolerate_minor` **未吸收**（仍判 `major`） | D2-042/043/044/045/054（5 项 `PARTIAL`） | `operational-discipline.md` §15；`events.jsonl:516,523,530,538` |
| **源侧绝对路径未消噪** | 以 `Console.ReadKey()` 结尾的 C# 源，其 stderr 含 `.NET 栈帧 + 源侧工作目录绝对路径`，该路径**不属** `temporary-paths` 覆盖 | D2-022/023（2 项**永远无法 matched**） | `operational-discipline.md` §14 |
| **动态端口未被覆盖** | D2-044 的动态端口**本应**被 `ephemeral-ports` 覆盖，但与 `duration_ms` 组合后仍判 `major` | D2-044 | `items/D2-044.json` → `evaluation.onlyDiff` |
| **`archive_bytes` 未消噪** | 目标按简化许可用 STORED，`archive_bytes` 1441 vs 1907，**无对应 token** | D2-045 | `items/D2-045.json` |

**建议**：① 增加 `duration_ms`/耗时类消噪记号（或提供"忽略指定字段"档位）；② 扩展 `temporary-paths` 覆盖 **Windows 绝对工作目录**与 .NET 栈帧路径；③ 明确 `ephemeral-ports` 与其它 `major` 差异**组合**时的判定优先级。

### 3.2 C# 目标 evidence-bundle schema 缺陷

- 平台 agent 产出的 evidence bundle 含**schema 不允许**的 `$.collectorDiagnostics.0.detail` ⇒ `INFRA_ERROR`，目标侧 preflight 从未尝试。
- **建议**：修复 agent 的 evidence-bundle 序列化，使 `collectorDiagnostics` schema 与产出字段一致（或移除 `detail`）。
- 出处：`platform-blocker-csharp-target.md`（含 2/2 复现 + 对照实验）。

### 3.3 `matched` 假阳性（**比较器不区分"两侧相同"与"两侧都没观察到"**）

| 事实 | 出处 |
|---|---|
| D2-029：两侧**空输出** + 非零退出 ⇒ 平台判 `matched`、`coverageRatio=1.0` | `operational-discipline.md` §10.1、§10.6 |
| D2-024：两侧 stderr **逐字节相同**（同一条 `DRIVER-FAILURE`），`diffs=[]` ⇒ 判 `matched` | §10.10；`events.jsonl:114` |
| D2-177：两侧 exit 1 + usage，**核心行为一次没跑到** ⇒ 判 `matched` | §8；`events.jsonl:91` |

- **建议**：比较器在**两侧观察同时为空/退化**时，不应输出 `matched`，而应给出独立档位（如 `no_observation` / `inconclusive`）。**影响面**：本批 3 项已实证；`operational-discipline.md` §10.6 为此设了批次级**放行规则**（四问）。
- **建议**：比较器应能识别**驱动自失败标记**（如 `DRIVER-FAILURE:`），此类 job 整体作废。

### 3.4 `semantic_pass` 档位语义

- `semantic_pass` 时 `matchedDimensions = 0`、`mismatchedDimensions = 0`、`inconclusiveDimensions = 0`，差异落在 `diffs[]` 且 `criticality=minor`、`rule=noise-tolerant-v1:...`。
- **建议**：维度计数**不可**代替档位判定；文档应明确"**只能读 `behaviorVerdict` 本身**"。
- 影响面：D2-036、041、056、057、059（5 项）。
- 出处：`operational-discipline.md` §10.15；`items/D2-056.json`、`events.jsonl:165`。

### 3.5 `digest` 与 `normalizedText` 的差异语义

- D2-058：两侧 `stdout.digest` **不同**（`cdf9cbb6…` vs `bc967b26…`）、`sizeBytes` 117 vs 118，但 `normalizedText` **逐字节相等**（各 116 字节）⇒ 平台按 preset **先消噪再比较**，判 `matched`。
- **建议**：报告/API 应把"**已消噪的可比面**"与"未消噪的 digest"在**不同字段**呈现，避免使用者误读 digest。
- 出处：`operational-discipline.md` §10.14。

### 3.6 `stderrMode` 无"忽略"档位

- 平台 `stderrMode` 仅 `exact` / `normalized-text` / `json-structural`，**不支持忽略** ⇒ 以 `Console.ReadKey()` 结尾的 C# 源项**永无法 matched**。
- **建议**：增加"仅比较 stdout"或"忽略指定流"的口径（属新冻结条件）。
- 出处：`operational-discipline.md` §14；`comparison-policy-adapter.md` §2（经 §14 引用）。

### 3.7 分类器 `hostname` 误判

| 项 | 误判对象 | 出处 |
|---|---|---|
| D2-055 | 本地文件名 `demo.txt` 被当主机名 ⇒ `BLOCKED/public_network_unverified` | `events.jsonl:169`；`reconciliation-2.md` §6.1 |
| D2-074 | `std::cout` 里 JSON 字段分隔冒号 `":"`（L459）被判 hostname；唯一真实地址是 loopback `127.0.0.1`（L82） | `events.jsonl:360`；`items/D2-074.json` |

- **建议**：hostname 启发式应要求**含网段/可解析形式**；排除纯标点与文件名。**处置纪律**：遇 `public_network_unverified` 先**读 `details.files[].network_targets` 原值**，若为文件名/标点则按误判登记并请求重分类，**不手改分类 JSON**（`summary.md` §1 A2）。
- 注：`safety_classifier_v2.py` 版本 v2.4，SHA `009a6f31…f3a4`（`summary.md` §9）。

### 3.8 提交端 / 控制器

| 问题 | 事实 | 出处 |
|---|---|---|
| **提交端硬门禁 `caseId`** | `caseId` 必须等于分类 `case`；带 `batch-…` 前缀 ⇒ `403 identity_mismatch` | `operational-discipline.md` §12 |
| **控制器忙拒** | 前一个 job 未终态时提交返回 `{"detail":"controller_busy"}`（在 job 创建前拒绝），需待前 job 终态后重提 | `events.jsonl:139`（`CONTROLLER_BUSY_OBSERVED`） |
| **平台 freeze note 出错** | `items/D2-015.json` → `notes`：「Agent freeze note 关于输出顺序**有误**，目标正确，复核者对照源偏移确认」；`items/D2-014.json` 亦登记"源经 `_popen` 多一层嵌套 cmd，目标去掉了，无可观察差异" | `items/D2-014.json`、`items/D2-015.json` |

- **建议**：① `caseId` 校验规则应在提交 API 文档与错误信息中**前置说明**；② `controller_busy` 应返回**可重试时间/队列位置**；③ freeze note 若有误，平台应支持**更正记录**（当前只能"另记 job"）。

### 3.9 采集/比较的其它实测事实

- **`applicableDimensions` 是输入面声明，不是观测充分性**：D2-029 两侧都"什么都没测、exit 1"仍被 `coverageRatio=1.0`（`operational-discipline.md` §10.1）。
- **取证须等终态**：中途快照（`RUNNING/CLEANING`）不可作最终依据（§10.11）。

---

## §4 溯源索引与未决项

### 4.1 逐项去向索引（按 taskId，含出处指针）

> 全 136 项明细以 `items/<taskId>.json` 为准。下表给**摘要去向 + 关键出处**，便于回读。

| 去向分组 | taskId 范围 | 关键出处 |
|---|---|---|
| `matched`（含早期 6 项） | D2-001~006, 013~015, 020, 021, 025, 029, 033~035, 037~040, 046, 047, 052, 053, 058, 060, 061, 067, 068, 088, 091~093, 095~097, 103~106, 174, 176, 177, 180, 181, 183 | 各 `items/*.json` → `verdicts.comparison` |
| `semantic_pass` | D2-036, 041, 056, 057, 059 | `events.jsonl:165`；各 item `evaluation.onlyDiff` |
| `mismatched`（装置残留 / 不可冻结） | D2-022, 023, 042~045, 054, 066 | §2.4、§3.1 |
| 源侧拦截 `SOURCE_NOT_BUILDABLE` | D2-027, 028, 073, 075, 152, 154, 155, 162~166, 168, 170~173, 178, 179, 182 | §2.2；`pattern-note-bsd-userland.md` |
| 源侧拦截 `SOURCE_DEPENDENCY_GAP` | D2-070, 071, 079~081, 084~087, 100, 102, 153, 161 | §2.2；`pattern-note-abseil-library-units.md` |
| 分类器阻断 `BLOCKED` | D2-055, 074 | §3.7 |
| C# 目标阻断 `BLOCKED_ENV` | D2-007~012, 030, 048~051, 076~078, 156~160 | §3.2 |
| 评估不可就绪（`PARTIAL`/`WAITING`） | D2-017, 018, 066, 072, 082, 089, 090, 094, 098, 099, 101, 108, 167, 169, 175 | §2.4 |
| 进行中（下一项） | **D2-062**（`NOT_STARTED`/`ACTIVE`，装置故障待修复） | `events.jsonl:612,613`；`batch/README.md` |

### 4.2 未决项（承接 `summary.md` §10.2，**带进下一轮**）

| 项 | 状态 | 恢复条件 |
|---|---|---|
| D2-007~012, 030, 048~051, 076~078, 156~160 | `WAITING`/`BLOCKED_ENV` | 平台修 C# 目标 evidence-bundle schema 后按原契约重提（§3.2） |
| D2-055, 074 | `WAITING`/`public_network_unverified` | 分类器修正 hostname 启发式后**重新分类**（§3.7） |
| D2-083 | `WAITING`/`public_network_unverified` | 取得**真实隔离证据**后重新分类 |
| D2-069 | `WAITING`/`BLOCKED_ENV` | 新冻结条件（源写只读 `/usr`） |
| D2-082, D2-108 | `WAITING` | 建立合格驱动（DLL 无入口 / 安全边界） |
| D2-017, 018, 066, 072, 089, 090, 094, 098, 099, 101, 167, 169, 175 | `PARTIAL` | **另冻条件**使可观察量确定化且不触发不必要副作用（§2.4） |
| D2-022, 023 | `DONE`（`mismatched` 装置残留） | 平台消噪覆盖源侧绝对路径，或冻结"仅比较 stdout"口径（§3.1、§3.6） |
| D2-062 | `NOT_STARTED`/`ACTIVE` | 修驱动（定义 `SIDE`）→ **重新分类** → 重跑预检 → 继续（`events.jsonl:612`） |

### 4.3 本文的核对方式与局限

- **核对方式**：本文数字均来自只读解析（`items/*.json`、`events.jsonl`、`self-review-*.json` 的字段统计），引用章节来自对应底稿原文。出处格式统一为 `文件 §节` / `items/<id>.json → 字段` / `events.jsonl:<行>`。
- **局限**：
  1. 本文**不重复抄录** evidence 原文；`04-evaluation/.../evaluation_report.*`、`comparison.json` 等证据层的**逐字段**内容需回读对应 job 目录。
  2. `go-to-ruby/d29-inbox-batch-validate-go` 对应 **D2-061**（经 `manifest.csv:61` 核实）；其自审 2 项经复核为**装置故障所致的误判**。
  3. `cpp-to-c/handoff-2026-10-02-d07-env-discovery-report-cpp`（= **D2-003**，经 `manifest.csv:4` 核实）的自审 JSON **不可解析**，仅登记其 `verdict=NO-REPAIR-IDENTIFIED`。
  4. 本文基于 2026-10-11 的快照；批次仍在推进（`summary.md` 关闭时才定稿），新项会新增素材。
