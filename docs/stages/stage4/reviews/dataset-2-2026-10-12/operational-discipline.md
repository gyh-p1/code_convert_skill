# batch 运行纪律（随项累积，供后续项复用）

本文件记录**在推进过程中由实测得出**的操作纪律，供后续项直接复用，避免重复踩坑。只追加，不改写历史条目。

## 1. filesystem 维度观察范围不得用全范围模式（源自 D2-003，2026-10-10）

- **现象**：D2-003 job-01 报 filesystem mismatched。读原始观察后确认，程序**实际写入的副作用文件逐字节相同**，唯一 major diff 落在 `program.exe`。
- **根因**：input_profile.json 的 filesystemInclude 设为 `**/*`，把**构建产物**（各自工具链编译出的可执行文件）扫进了比较范围。源侧 g++ 二进制与目标侧 gcc 二进制必然不同。
- **纪律**：含 filesystem 维度的项，filesystemInclude **必须**显式列出程序声明的副作用路径（如 `out/**`），**不得**使用 `**/*`、`**`、`*` 等全范围模式。
- **归因口径**：此类差异属**装置**，保留平台原 verdict、不自行改判、不进入模型代码修复；修正装置后在后续 job 重取证据。

## 2. 模型响应的 JSON 不可无条件信任（源自 D2-003 自审）

- **现象**：自审响应中 JSON.parse 失败（模型在 evidence 文本里写了未转义的引号）。
- **纪律**：解析模型响应前先定位 content 字段并按其转义规则解码，不要对整包 JSON.parse 后再取 choices[0]；同时仍保存原始响应文件供复核。

## 3. 请求体必须由确定性 JSON 构造器生成（源自 D2-001）

- **现象**：PowerShell ConvertTo-Json 破坏 UTF-8 中文正文并包成对象，请求体从 5 KB 膨胀到 777 KB，返回 invalid_request_error。
- **纪律**：请求体用能保证 UTF-8 与转义的构造方式生成，构造后回读校验（round-trip 相等）。该失败尝试不计入代码修复预算。

## 4. 一次性程序与常驻服务的驱动区分（源自规则库 D2-024 教训）

- 本批各项均为**一次性程序**（自带 main、所有路径 return、必然自行退出），驱动形态为启动→自然退出→采集，**不得**套用常驻服务的等监听就绪驱动。
- 判定口径：问这个驱动有没有可能在程序仍处于待观察状态时就去终止它、或等它自己退出——本项目前各项答不可能，故合格。

## 5. 目录创建语义（源自 D2-003，实测证实）

- 把 fs::create_directories（递归）降级为 CRT _mkdir 时，**先建父级再建子级**（_mkdir("out") 再 _mkdir("out/discovery")）在本契约下可成功；该判断已由双侧实测证实（两侧均产出 272 B 相同 digest 的文件）。
- 注意：_mkdir 是**单级**的，3 级以上嵌套仍会失败；遇到更深路径须改用递归实现或 CreateDirectoryA 逐级创建。

## 6. 驱动必须透传子进程原始 stdout/stderr 字节（源自 D2-013，2026-10-10，最重要的一条）

- **现象**：D2-013 job-01 报 output mismatched；改用 normalized-text 后 job-02 **仍然** mismatched。
- **根因**：驱动把子进程 stdout 捕获后**包进了一个 JSON 字符串**，于是 C++ 的真实 CR 字节变成转义序列（反斜杠 + r）出现在**载荷内部**；平台的消噪规则看不到真实 CR，无法归一化。
- **决定性对照**：job-03 改用「直接透传子进程原始 stdout 字节」的驱动后，**matched，diffs=0**。
- **纪律**：驱动的唯一职责是「启动、等待、采集、终止」，采集 = **原样透传字节**。
  - Python 用 sys.stdout.buffer.write(p.stdout)，**不要** json.dumps({... 'stdout': p.stdout.decode() ...})。
  - 退出码用 sys.exit(p.returncode) 传递。
- **为何重要**：包装会改变被观察对象的字节形态，把**装置缺陷伪装成行为差异**，并浪费多轮评估往返。
- **影响范围**：本批 D2-001..D2-006 的驱动**也**使用了包装形态。
  - 那六项**输出不含行内 CR**，包装未造成差异，结论**仍然有效**（matched）；但形态本身不合纪律。
  - 从 D2-013 起，所有后续项一律使用**原始字节透传**驱动。

## 7. 驱动必须按目标语言形态选择启动方式（源自 D2-031，2026-10-10）

- **现象**：D2-031 目标侧 build completed/0，但 execution exitCode=1、stdout 为空，平台报 mismatched（3 个 diff）。
- **根因**：驱动只查找 program.exe / program（编译型产物），而目标产物是**脚本** target.py，驱动找不到，抛 FileNotFoundError。
- **性质**：装置/驱动缺陷，**不是**转换问题；但规则要求驱动不合格不得提交，**提交不合格驱动是 Agent 的错误**。
- **纪律**：驱动须同时覆盖两类形态——
  - 编译型（c / cpp / go / csharp）：直接执行构建产物 program.exe / program；
  - 脚本型（python / ruby / powershell）：用解释器运行 target.py / target.rb / target.ps1。
- **不变式**：无论哪种形态，都要**透传子进程原始 stdout/stderr 字节**并用其退出码（纪律 §6）。

## 8. 驱动必须把冻结的 argv 转发给被测程序（源自 D2-177，2026-10-10）

- **现象**：D2-177 平台报 **matched、diffs=0**，但两侧 exitCode 均为 1、stdout 均空、stderr 均为 usage 文案。
- **根因**：平台的 input_profile.argv 是喂给**驱动**的，而驱动忽略了自己的 argv，从未把参数转发给被测程序；被测程序收到 0 个参数，两侧都走了 usage() 分支。
- **危害**：这是**假阳性**——平台说 matched，实际**核心行为一次都没跑到**。比 mismatched 更危险。
- **纪律**：驱动必须在启动被测程序时，把**同一份冻结 argv** 原样转发下去（ARGS 取自身 argv，拼到命令末尾）。
- **自检口径**：提交前问一句——「驱动跑起来后，被测程序收到的 argv 是否等于契约冻结的 argv？」答否即不合格。
- **与四要素的关系**：这属于②「到达被观察状态」不满足：程序启动了、也退出了，但从未进入要观察的状态。

## 9. 判「快照外文件」前必须先查旧 dataset 的完整源树（源自 D2-025 更正，2026-10-10）

- **现象**：D2-025 的 source/ 下只有 driver.c，含 `#include "atoms.h"` 与 `quark_connect` 声明；我据此判 SOURCE_DEPENDENCY_GAP。
- **错误**：没有去查该 case 在**旧 dataset** 里的完整源树。实际上旧 dataset 的 capsule 内同时存在 driver.c、atoms.h、networking_quarks.c、util.c、util.h，且 **driver.c 的哈希与 manifest 声明完全一致**，证明这套伴随文件确实属于本 case。
- **规则早已写明**：build-prerequisites **点名 D2-025** 作为「打包缺口 ≠ 源依赖缺口」的先例——伴随文件本在数据集内、只是提交时漏带，应**补齐组装后重测**，不记 SOURCE_DEPENDENCY_GAP、更不记 SOURCE_NOT_BUILDABLE。
- **纪律**：判「引用了快照外文件」之前，**必须**先在旧 dataset 里按 case 路径查该 case 的完整源树，并用**哈希**确认伴随文件属于同一次提交。
- **实测验证**：补齐后重跑预检，build **completed/0**，原判定被推翻。

---

## §10 驱动必须让被测程序**真正收到**冻结输入；"两侧都没有观察"是一个假阳性形态

**来源**：2026-10-10 D2-029（c-to-cpp stest）连续三次装置错误，每次都能骗过比较器。

### 10.1 空 argv 会把程序送进"读 stdin"的空转分支

- D2-029 冻结 argv = `[]`。而 `stest` 在无参数时进入 `while (getline(...))` **从 stdin 读文件列表**；驱动又把 stdin 设为 `DEVNULL` → 立刻 EOF → 一个文件都没测 → `return match ? 0 : 1` **必然返回 1**。
- 源与目标**都只做了"什么都没测，然后 exit 1"**，比较器看到两个空输出即判 `matched`、`coverageRatio=1.0`。
- **教训**：`applicableDimensions` 是**输入面声明**，不是**观测充分性**。两侧同时"无输出且非零退出"必须**先怀疑装置**，不得当作一致性证据。
- **规矩**：冻结 argv 时先确认"这条路径真的会做事"。若程序在空 argv 下回落到 stdin，要么冻结非空 argv，要么把 stdin 内容一并冻结。

### 10.2 包装层自己的失败会伪装成被测程序的行为

- D2-029 job-02 的驱动写了 `subprocess.run(stdin=subprocess.PIPE, input=b"")`。Python 直接抛 `ValueError: stdin and input arguments may not both be used.`——**被测程序一次都没运行**。
- 两侧 stderr 是同一条 traceback（只有工作区路径不同），于是平台报出一个 `mismatched`：**这个 FAIL 与被测代码毫无关系**。
- **规矩**：驱动必须把"包装层失败"与"被测程序的行为"在信号上分开。本次修法是驱动自失败时 `exit 97` 并打印 `DRIVER-FAILURE:` 标记。**看到两侧 stderr 形状相同、且含驱动自己的路径/函数名，先按装置缺陷处理。**

### 10.3 先读**预检**的 `input_profile.json`，再决定要不要转发 argv

- D2-029 我起初以为 harness 把冻结论元放在 `python run_case.py -- <args>` 之后，于是让驱动**转发 `sys.argv[1:]`**。
- 读预检 capsule 才发现：预检 `run_case.py` 用 `ARGS = sys.argv[1:]`，`input_profile.json` 里写的是 `["-f", "stest.c"]`，**那就是程序真实收到的 argv**。
- **规矩**：`run_case.py` 用 `sys.argv[1:]` 时，harness 的调用形态是 `python run_case.py <frozen argv...>`，`--` 之后的说法**不成立**；冻结论元**必须**原样转发（§8），并且**要拿预检的 `input_profile.json` 对照确认**，不要凭对平台调用方式的猜测。

### 10.4 oracle 必须有**独立外部依据**，不能从自己的装置推出来

- 我按"`prog stest.c` 应打印 `stest.c`"造 oracle；但预检真实跑的是 `prog -f stest.c`，两者都可能命中，我却把其中一次的观察当成了通用期望。
- **规矩**：冻结 oracle 时写出**它来自哪一次真实观察**（jobId + argv + 观察值）。若预检观测到的 argv 与我打算冻结的 argv 不同，**必须重新取得该 argv 下的源侧观察**，不得外推。

### 10.5 修复前必须先把差异**定位到语句**

- D2-029 第一轮功能修复：我把"源 exit 0 / 目标 exit 1"交给模型，模型返回**逐字节相同**的代码——它找不到可定位的差异，因为**我也没给出定位**。
- **规矩**：`mismatched` 但差异未定位到语句时，先做**单因素定位实验**（一次只改一个输入/一个条件，其余全部冻结），拿到"哪个分支不同"，再带定位证据交回模型。**不要连问同一个模型同一句话。**

### 10.6 **放行规则**：`matched` 在"两侧都没观察到东西"时不构成一致性证据（批次级适用）

**自本节生效起，本批（batchId=`batch`）剩余各项一律适用下列放行规则；已完成的项按 §10.7 追溯复核。**

**放行前必须逐项核对四问，任一不过即不得记 `matched` 行为结论：**

1. **驱动确实把冻结输入送到了吗**：argv 是否被原样转发；若冻结 argv 为空而程序会回落到 stdin，stdin 内容是否也一并冻结。
2. **两侧真的跑到了被观察状态吗**：源侧是否产生了**非空观察**（stdout 或 stderr 至少一项非空，或退出码能与"什么都没做成"区分开）。
3. **源侧观察与我冻结的 oracle 一致吗**：必须与**同一 argv 下**的既有真实观察逐字节对照；不同 argv 的观察**不得外推**。
4. **两侧同时"空输出 + 非零退出"吗**：若是，**先判装置可疑**，不得作为一致性证据，也不得作为转换失败证据。

**判定口径**：

- 源侧观察到**非空且非退化**的输出 ⇒ 该次 `matched` 可作为该 argv 路径下的行为证据（仍受覆盖缺口约束）。
- 源侧观察为**空 or 退化**（例如两侧同为 exit 1 + 零字节输出）⇒ 本次比较**不产生行为结论**，记 `UNVERIFIED`，另冻条件重测；**不得记 `matched`，也不得记转换失败**。
- 装置缺陷（驱动报错、包装层异常、输入未送达）⇒ 该次 job **整体作废**，其 `matched`/`mismatched` 一律不采信，另记新 job，原判定保留不改写。

**为什么放在纪律而不是某个 SKILL 页**：这是**放行判据**，属于三道硬门禁里"评估就绪核对"的组成部分，执行路径上的 Agent 必须读到；详见 §10 开头三例实证（D2-029 job-01/02/03）。

### 10.7 追溯复核范围

- **已完成的 22 项终态 + D2-029**：逐项回看 `returned-evidence/evidence-source.json` 的 `execution`，凡"源侧空输出且非零退出"或"源侧空输出且退出码与目标相同"者，按 §10.6 重新归类。
- 复核**只追加记录**，不改写已落盘的原判定。

### 10.8 §10.7 追溯复核结果（2026-10-10 执行）

复核范围：dataset-2 全树下**全部 55 份** `evidence-source.json`（含预检、探针、正式 job）。

| 类别 | 数量 | 处置 |
|---|---|---|
| 源侧观察非空、非退化 | 37 | 其 `matched` 可作为对应 argv 路径的行为证据 |
| `execution` 未执行（`exitCode=null`，纯构建预检 job） | 15 | 本不产生行为结论，不受影响 |
| 源侧空输出 + 非零退出 | 1 | **D2-029 job-01** —— 已按假阳性作废并另记 job-05 |
| 源侧空输出 + 非零退出（**已定性**） | 2 | D2-177 job-00/01 —— 早已按纪律 §8 判为假阳性并另记 job-02 |

**结论**：本批已完成的 22 项终态中，除 D2-029 与先前已知的 D2-177 外，**未发现其它"空输出对空输出"型假阳性**；已落盘的原判定一律保留不改写。

### 10.9 常驻服务的观察必须在**进程存活期内**采集（D2-024 实证）

**来源**：2026-10-10 D2-024（c-to-cpp uhttpd，常驻 HTTP 服务）服务路径连续两个 job 未取得任何观察。

- **job-03**（`eval-20261010-054915-86cb2697`）：驱动 `Popen(..., stdout=PIPE)` 后轮询端口，connect 成功后 `terminate()`，**之后**才 `communicate()` 取输出。
  子进程 stdout 是管道 ⇒ libc **全缓冲** ⇒ startup banner 还在子进程缓冲里就被 SIGTERM 杀掉 ⇒ 两侧观察**全空** ⇒ 平台判 **`matched`**。
- **job-04**（`eval-20261010-055115-367d73e1`）：改为存活期内用读线程持续 pump，但就绪条件仍**未达成**，驱动自己的 `DRIVER-FAILURE` 标记出现在两侧，平台**仍判 `matched`**。

**规矩**：

1. 常驻服务的 stdout/stderr **必须在存活期内持续读取**（读线程 pump），**不得**只在 `terminate()` 之后一次性 `communicate()`。
2. 就绪判据要用**oracle 明确要求的观察量**（如日志 banner），**不得**用"端口可连接"这类旁证替代。
3. 驱动自身失败必须**打显式标记并给专用退出码**（本项用 `DRIVER-FAILURE:` + 97），使"服务没起来"与"程序没输出"在信号上可区分。
4. **即使做了 3**，平台仍可能把"两侧同一条驱动失败标记"判成 `matched` ⇒ **§10.6 的源侧非空核对不可省**。

### 10.10 平台比较器的新事实：**两侧相同的失败输出也算 `matched`**

**来源**：D2-024 job-04。两侧 stderr **逐字节相同**（同一条 `DRIVER-FAILURE`），`diffs=[]`，`behaviorVerdict=matched`。

- 即比较器**不区分**"两侧行为相同"与"两侧都没观察到行为"。
- 与 D2-029 job-01（两侧空输出判 matched）同根因、不同表现。
- **规矩**：`matched` **永不单独采信**。必须同时满足 §10.6 四问，特别是第 2 问（源侧观察非空且非退化）。
- 本项据此把服务路径记为 `UNVERIFIED`，**不记** matched，**也不记**转换失败。

### 10.11 取证**必须等终态**

**来源**：D2-024 job-04 首次取证时 job 仍为 `RUNNING/CLEANING`，取回的是中途证据；终态复核后结论虽一致，但中途证据**不可作为最终依据**。

- **规矩**：轮询到 `COMPLETED`/`FAILED_*`/`TIMEOUT`/`INFRA_ERROR` 等终态**之后**再取 `report`/`evidence`/`comparison`/`logs`；中途快照只可用于进度判断。

### 10.12 不要在单一路径上连续试驱动（推进纪律）

- D2-024 服务路径已用 2 个 job 仍未取得观察。**继续在同一路径改驱动属于"在单个用例上死磕"**。
- **规矩**：同一路径连续 2 次装置失败后**停止**，如实记 `UNVERIFIED` 与覆盖缺口，转到其它项；需要时**另冻条件**（如改为"驱动内起客户端发起一次 loopback 请求"）并在后续批次处理。

---

## §11 分类器暂存目录必须是**暂存**：用完即清，且不得落在仓库根

**来源**：2026-10-10 清点发现仓库根残留 **27 个** `.tmp-classify-<id>/` 目录（D2-001…D2-178 的早期批次）。

### 事实

- 这些目录**本身合规**：[分类结果准入](../references/workflow/classifier-agent-gate.md) §1 要求分类器在"获准的外部环境临时目录"中调用，逐项建一个暂存目录是按规矩做的。
- **问题在位置与清理**：早期 27 项把暂存目录建在**仓库根**且**用完未删**；近期各项（D2-024、D2-161、D2-162）改用 `$env:TEMP` 并在命令末尾 `Remove-Item` 清理。
- **已核对无独有证据**：27 个目录中的 `classification-1.json` **逐个与已持久化的副本逐字节相同**（按内容哈希比对，27/27 命中，0 个独有）；`safety_classifier_v2.py` 是注册脚本的副本（31881B，与钉定 SHA `441B4D50…6524` 一致）。
- **副作用**：`.gitignore` 覆盖 `/docs/test/` 与 `.env`，但**未**覆盖 `.tmp-classify-*/` ⇒ 这 27 个目录产生 **112 条 untracked 条目**，`git add -A` 会被一并纳入。

### 规矩

1. 分类器暂存目录建在 `$env:TEMP`（或其它仓库外路径），**不得**建在仓库根。
2. 每个暂存目录在**取回并持久化 `classification-1.json` 之后立即删除**；持久化位是该项的 `output/batch/01-frozen/`。
3. 若因故必须在仓库内暂存，**先**把该模式加入 `.gitignore`，且当轮任务结束前删除。
4. 判断标准是行为：暂存目录**不该成为常驻物**。"临时"变成"常驻"即违反本条的意图。

### 待处理（未执行，需授权）

- 27 个仓库根暂存目录**尚未删除**；已确认删除不丢证据，但删除属破坏性操作，**等用户确认**。

### 10.13 驱动的**后处理必须对两侧完全一致**（不对称后处理会制造假 FAIL）

**来源**：2026-10-10 D2-058（go-to-python child_cmd_capture）job-01 判 `mismatched`，实为装置缺陷。

**现象**：source 侧 stdout 只有一行 `artifact: …`，target 侧多出一段 `--- captured ---\nsafe-exec`。

**根因**：驱动写成两条分支——

```
for name in ("target.py", "target.rb", "target.ps1"):  # 分支一：运行 + 回显 captured 文件
for name in ("program.exe", "program"):               # 分支二：运行，**不回显**
```

source/ 侧是 Go（产物 `program.exe`）⇒ 走分支二；target/ 侧是 Python ⇒ 走分支一。
**同一段后处理只挂在一条分支上** ⇒ 两侧观察面不同 ⇒ 比较器报 `mismatched`。
两个程序**自身的** stdout 行其实逐字节相同。

**与 §10.6 的关系**：§10.6 防的是"两侧都**没有**观察到东西"；
本条防的是相反的一类——装置给了一侧**更多**观察，制造**假 FAIL**。两者都是"观察面不对称"。

**规矩**：凡驱动对输出做**后处理**（回显文件、追加标记、归一化、拼接），

1. 该处理必须**对两侧完全一致地执行**；
2. 正确结构是**把"定位可执行体"与"后处理"解耦**：先统一 `resolve_command()` 得到启动 argv，运行，再走**同一条**后处理；
3. **不得**因为目标形态不同（脚本 / 编译产物 / 解释器启动）而在任一侧跳过或追加处理；
4. 因此**每一类分叉（脚本 vs 二进制）都必须至少有一次双侧同型的实测**，否则不对称不会被发现。

**为什么本次能发现**：源侧是 Go 编译产物、目标侧是 Python 脚本，**恰好构成一次天然的"分叉对照"**，
才把"回显只挂在一侧"暴露出来。若两侧同为脚本，该缺陷会**静默通过**——这是本条最需要警惕之处。

### 10.14 两侧 digest 不同但判 matched 时，必须逐项归因后才可引用

**来源**：D2-058 job-02 通过，但 `excution.stdout.digest` 两侧不同（`cdf9cbb6…` vs `bc967b26…`），`sizeBytes` 117 vs 118。

- 归因结果：`normalizedText` **逐字节相等（各 116 字节）**；
  `digest`/`sizeBytes` 覆盖的是**未消噪的原始流**，其中含**用户相关临时目录路径**；
  平台按 preset `noise-tolerant-v1` 的 `temporary-paths` 记号**先消噪再比较**，故判 matched；
  剩余 1 字节差来自捕获行行尾（CRLF/LF），属环境/装置层面。
- **规矩**：见到"digest 不同但 matched"，**不得**直接引用为"一致"，
  必须先核对 `normalizedText` 是否逐字节相等、并说明差异落在哪一类消噪记号内；
  不能归因到消噪类别的差异，**不得**算作转换一致。

### 10.15 `semantic_pass` 是**独立档位**，不得写成 `matched` / 行为一致

**来源**：2026-10-10 D2-056（go-to-powershell staged_config_build）。平台 `behaviorVerdict = semantic_pass`。

| 档位 | 含义 | 本批实例 |
|---|---|---|
| `matched` | 所有可适用维度**无差异**（diffs=0） | D2-033、D2-034、D2-058 |
| `semantic_pass` | 维度**匹配**，但存在**被显式配置容忍的次要差异** | **D2-056** |
| `mismatched` | 存在关键/重大差异 | D2-029（真实转换缺陷） |

**实测差异点**：

- `semantic_pass` 时 `coverage.matchedDimensions = 0`、`mismatchedDimensions = 0`、`inconclusiveDimensions = 0`；
  差异落在 `diffs[]` 且 `criticality = minor`，`rule = noise-tolerant-v1:text-tokens:…`。
- 因此**不能**用 `matchedDimensions` 计数代替 `matched` 判定；**只能读 `behaviorVerdict` 本身**。

**规矩**：

1. 报告与 item 记录中，`semantic_pass` **必须原样写**，不得简写为 matched/一致/通过；
2. `semantic_pass` **必须**逐条列出被容忍的差异（本项：第 10 行 `time` 字段）**并给出归因**；
3. 归因不属于消噪类别的差异，**不得**采信 `semantic_pass`（回到 §10.6 处理）。

### 10.16 **可观察量必须可复现**，否则 oracle 不可冻结 —— 记 `UNVERIFIED`，不记转换失败

**来源**：2026-10-10 D2-066（python-to-powershell 网卡计数监控）判 `mismatched`，根因是 **oracle 本身不可满足**。

| 侧 | stdout |
|---|---|
| source | `Sent: 0 bytes, Received: 0 bytes in the past 1 seconds` + `monitor finished` |
| target | `Sent: 6275 bytes, Received: 3123 bytes in the past 1 seconds` + `monitor finished` |

把数字替换为 `N` 后，**两侧文本逐字节相同**（行数、字段、单位、末行一致）。

### 判据：什么算"oracle 不可冻结"

若可观察量包含**两次执行之间不可复现**的成分，且该成分**不在服务器消噪记号覆盖内**，则该项**无法给出行为结论**。典型来源：

| 来源 | 例 | 是否被消噪覆盖 |
|---|---|---|
| 执行时刻 | `time.Now()` / 时间戳 | **是**（`timestamps`）—— D2-056 属此类，判 semantic_pass |
| 临时路径 | `/tmp/...` 用户相关路径 | **是**（`temporary-paths`）—— D2-058 属此类 |
| 端口号 | 临时端口 | **是**（`ephemeral-ports`） |
| **活动计数器** | 网卡收发字节、CPU 时间、内存占用 | **否** |
| **随机数** | `rand()`、随机文件名 | **否** |
| **并发/调度顺序** | 线程交错输出 | **否** |

### 规矩

1. **冻结 oracle 前先问**：这个可观察量在两次执行间会不会变？若会变，**是否落在消噪记号覆盖内**？
2. 会变且**不在**覆盖内 ⇒ **该 oracle 不可冻结**：
   - **不**记转换失败；
   - **不**记行为通过；
   - 记 **`UNVERIFIED`**，并登记 `ORACLE_NOT_FREEZABLE` 与具体原因；
   - lifecycle 记 **`PARTIAL`**（有交付与编译证据，无行为结论）。
3. **不重复重提**该类项以求变绿 —— 重提只是**重新掷骰子**，属纪律 §10.12 的"在同一项上死磕"。
4. 若确需该路径的结论，**另冻条件**使数值确定化（如由驱动固定输入），属**新的冻结条件**，不得回头改本次记录。
5. **结构一致 ≠ 行为一致**：本次归因记录"结构逐字节相同"**只用于归因**，
   **不得**当作行为通过的证据写进结论层。

### 与 §10.14 的分工

- §10.14：差异**落在消噪覆盖内** ⇒ 可采信平台的 `matched`/`semantic_pass`，但须逐项说明；
- §10.16：差异**不落在**消噪覆盖内 ⇒ **不可**采信任何"通过"，记 `UNVERIFIED`。

### 10.17 C→C++ 的两类构建失败必须分开：**契约差异**（加标志）vs **真实缺陷**（改代码）

**来源**：2026-10-10 D2-025（c-to-cpp chain-reactor，5 文件约 1000 行）首版 target 构建失败，两个根因混在一份诊断里。

### 分离手法：**一次只加一个标志，看剩下什么**

| 步骤 | 命令 | 结果 |
|---|---|---|
| 首版 | `g++ -std=gnu++17 …` | **7 个 error**：6 处 `cast from int* to int loses precision` + 1 处 `jump to case label` |
| 加 `-fpermissive` | `g++ -std=gnu++17 -fpermissive …` | 6 处**降级为 warning**，**只剩 1 个真 error** |

⇒ 前 6 个是**契约**，第 7 个是**真实缺陷**。**不分离就分不清该改命令还是改代码。**

### 判据：什么时候加 `-fpermissive` 是**契约修正**而非掩盖

**关键看源码有没有"自己声明过这个意图"**：

```c
// We do this when writing a 32bit mapped 64bit address to a four byte memory
// address. The compiler doesn't know this, but it's fine.
#pragma GCC diagnostic ignored "-Wpointer-to-int-cast"
#pragma GCC diagnostic ignored "-Wint-to-pointer-cast"
```

源码**自带**这两条 pragma ⇒ 这些 `指针→int` 转换是**有意为之**（32 位 socketcall ABI）。
该 pragma 在 C++ 下**不是合法警告名**，g++ 忽略之，于是"已声明忽略"退化为 hard error。
**用 `-fpermissive` 把同一意图表达出来，是等价替换，不是掩盖。**

**反面（不得加标志的情形）**：源码**没有**声明该意图、转换是模型改错引入的 —— 那就必须**改代码**。
另见 D2-178：源码缺 `#include <stdint.h>`，属**源码自身缺陷**，**不得**用 `-include` 掩盖。

### 真实缺陷的处理（本例）

`networking_quarks.cpp:540: error: jump to case label crosses initialization of 'int status'`（537 行）

- C 允许 `switch` 体内语句后声明变量并跳到后续 `case`；**C++ 不允许**跨过初始化。
- 首版 target 与 C 源**逐行相同** ⇒ 模型**漏做**了这项必需的适配（这正是 C→C++ 的转换工作）。
- 修复：给 `default:` 分支体**加一对花括号**作用域，`int status` 不再被跨越。**逻辑一字未改。**

### 规矩

1. C→C++ 构建失败**必须先做"加一个标志"的隔离实验**，把诊断**分成契约项与真实项**；
2. 只有当源码**自带证据**表明该转换是有意为之（pragma / 注释 / 既有 ABI 约定）时，才可用标志表达；
3. **真实项必须由模型改代码**，且按 §10.5 **先定位到语句**再交回模型（本例定位到 537/540 行）；
4. 隔离实验**另记 job**，保留首版的失败诊断，**不改写**；
5. 报告中**分开写**两者："`-fpermissive` 后 6 项降级为 warning"与"1 项真实缺陷已修复"**不得**合并成一句"编译通过"。

### 10.18 冻结 argv 引用文件时，**必须先确认该文件在两侧树中都存在**

**来源**：2026-10-10 D2-029。我连续 4 个 job 把 `mismatched` **误归因为转换缺陷**，实际是我的**打包不对称**。

### 事实

冻结 argv = `["stest.c"]`（**相对文件名**）。程序在自己的**工作目录**里 `stat()` 这个名字。
我按语言给两侧铺树：

| 侧 | 树内容 | `stat("stest.c")` | 结果 |
|---|---|---|---|
| source | `stest.c`, `arg.h`, `program` | **成功** | 命中，exit 0 |
| target | `target.cpp`, `arg.h`, `program` | **失败** | 未命中，exit 1（**行为正确**） |

⇒ 两侧**输入不等价**，比较自然不一致。**目标侧没有任何缺陷。**

### 我为什么没发现（这是本条的重点）

我核对了：编译诊断（逐条）、源码文本（逐行 diff）、驱动（两侧逐字节相同）、`arg.h` 哈希（相同）。
**唯独没有核对**："被 argv 点名的那个文件，在两侧都存在吗？"

⇒ 因为**诊断与源码都"看起来对"**，我误以为差异只能来自转换，于是写下"转换引入"的归因。
**这是最容易犯的一类错误**：把装置不对称当成被测对象的差异。

### 规矩

1. **冻结 argv 里出现文件/目录名（相对或绝对）时**，提交前**逐个确认**该路径在 **source/ 与 target/ 两侧树中都存在**，且**内容/权限一致**；
2. 两侧树放**各自语言的翻译单元**是自然的，但这会让"源文件名在目标侧不存在"——
   因此**不要**直接拿源文件名当冻结参数，而应**另放一份双方同名同内容的 fixture**；
3. 用**探针 job** 取证：让驱动打印**子进程实际收到的 argv**、**cwd 内容**、**`exists(<name>)`**、**exit code**。
   本次 (job `eval-20261010-071912-71faff81`) 一眼就看出根因；此前 4 个 job 都没看这些事实；
4. **在把 `mismatched` 归因为"转换引入"之前**，先排除：输入不等价、文件不存在、路径不可写、环境差异。
   排除不掉时，**不得**写"转换引入"。

### 与既有条目的关系

- §10.13：驱动**后处理**必须两侧一致；
- §10.18（本条）：驱动**输入面**必须两侧等价 —— 包括文件系统里被引用的对象。
两者合起来才是完整的"装置对称性"要求。

### 10.19 被观察量是**目录条目数**时，两侧运行时条目数必须相等（§10.18 的变体）

**来源**：2026-10-10 D2-103（cpp-to-ruby host_env_snapshot）。job-01 判 `mismatched`，`cwd_items` **3 vs 2**。

### 事实

程序统计**工作目录条目数**，而两条构建命令的**产出不同**：

| 侧 | 构建命令 | 产出文件 | 运行时条目数 |
|---|---|---|---|
| source | `g++ … -o program` | **是** | 3 |
| target | `ruby -c target.rb` | **否**（仅语法检查） | 2 |

差异恰为 1；`user`/`host`/`os` 三项两侧一致，**两个程序行为都正确**。

### 我的失误点（值得单列）

**我在提交前确实核对了条目数**——但**按"两侧都会生成 `program`"的假设**算的 +1。
⇒ **假设代替了核对**。真相是：**解释型语言的"构建"常常只做语法检查，不产出任何文件**。

### 规矩

1. 当被观察量是**目录条目数 / 文件数 / 路径列举**时，提交前必须**按每条构建命令的实际产出**推算两侧运行时条目数，
   **不得假设**"两侧都会生成可执行文件"；
2. 推算依据是**构建命令本身**：`-o <file>` 产出文件；`ruby -c` / `python -m py_compile` / `node --check` 之类**不产出**（或只产出缓存）；
3. 若两侧条目数天然不等，可在**侧别树中放中性占位文件**使条目数相等——
   该文件**不得被任何程序读取**，**不得改变源码或构建命令**，只用于让被观察量两侧可比；
4. 占位文件的存在与用途**必须**写进该 job 的 `metadata.json` 与被观察量说明，避免后人误以为是产物。

### 与 §10.18 的关系

- §10.18：argv 点名的**文件**须两侧都存在；
- §10.19（本条）：被统计的**目录条目**两侧数量须相等。
两者同属"输入面/被观察面必须对称"，但触发条件不同，**须分别核对**。

### 10.20 分类器输入哈希**大小写敏感**，必须从 manifest **原样读取**，不得手敲或转小写

**来源**：2026-10-10 D2-021。连续两次分类得到 `BLOCKED / input_error`（`ValueError: source_hash_mismatch`），
而实际文件哈希**完全正确**。

| 来源 | 值 |
|---|---|
| manifest（权威） | `B432966FC55671B2B5A71F12EBA2FB9EFE20C81424DD99559A217267E05F0C0` |
| 我用小写写入 `classifier-input.json` | `b432966f…0c0` |
| 分类器判定 | **不匹配** ⇒ `source_hash_mismatch` |

⇒ **分类器按字节比较，大小写敏感**；小写形式**不等于** manifest 的大写形式。
（文件本身的 SHA-256 是对的；错的是我在**清单里写的字符串形式**。）

### 与既有条目 D2-004 的关系

D2-004 的教训是"哈希要**从 manifest 读**，不要手敲"（我敲成了 63 位）。
本条是同一根因的**另一种表现**：**读了**但**改了大小写**，仍然不算原样。

### 规矩

1. `classifier-input.json` 的 `sourceSha256` **必须逐字节取自 manifest 的 `Sha256` 列**，
   包括大小写；**不得**手敲、**不得** `ToLower()`、**不得**重新格式化；
2. 若分类报 `source_hash_mismatch`，**先比对字符串形式**（长度、大小写），再怀疑文件内容；
3. `input_error` 的正规出口是**修复输入后重跑分类**（本例即如此），**不得**绕过分类门禁。

### 本条的另一面：**先确认 taskId 对应的是哪个源文件**

同一轮里我还把 `handoff-2026-10-02-d11-loopback-ack-probe-cpp` 误当作 **D2-182**，
而 manifest 中该目录对应的是 **D2-021**（D2-182 是另一个 `virtualallocex_hack.c`）。
⇒ **目录名与 taskId 不是一一对应关系**，必须**按 manifest 的 `Origin` 列**逐项确认后再落盘；
发现落错后，**已删除**错建的暂存目录并改建在正确 ID 下（未产生任何提交）。

---

## §12 提交端硬门禁：`caseId` 必须等于分类的 `case`（= taskId），带前缀的旧命名会 403（源自 D2-151，2026-10-11）

**现象**：D2-151 首提用 `caseId=batch-d2-151-c-to-cpp-rm`（沿用本批早期形制），服务端返回
`403 {"detail":{"error":"admission_blocked","blockingReason":"identity_mismatch","reason":"submitted content does not match the classified content","action":"re-classify the exact submitted sources (content/direction/case must match)"}}`；
改成 `caseId=D2-151`（与分类行 `case` 一致）后 **202 accepted**。

**根因**：平台 1.0.28 的 `admit_single()` 做**身份/哈希绑定**（[接入报告 §2.2 第 3 条](../../../docs/stages/stage1/reports/平台提交端准入闭环接入-2026-10-10.md)）：
"身份/哈希不符（**taskId/direction/caseId** 或源文件 sha256 与提交 capsule 不一致）→ `identity_mismatch`"。
提交侧能被平台读到的身份就是 `POST` 表单的 `caseId`（外加 capsule 内 `comparison_manifest.caseId`），
因此 `caseId` 必须等于分类行的 `case` 字段。

**为什么早期项没报错**：本批全部既有 job 都**早于硬门禁重新部署**（D2-001 03:37、D2-103 07:24、D2-088 14:59；1.0.28 部署 22:33）。
带 `batch-…` 前缀的 `caseId`（如 `batch-d2-001-cpp-to-c-chunked-manifest-exfil`、`batch-d2-103-cpp-to-ruby-precheck`）当时**无人校验**。
D2-088（14:59）用的是纯 `D2-088`，恰好与分类 `case` 相同——**它是唯一在硬门禁下通过命名巧合的样本**。

### 规矩

1. `caseId`（POST 表单）**一律取该项 taskId**；`comparison_manifest.caseId`、`metadata.caseId`、`input_profile.profileId` **同样取 taskId**，四处一致。
2. **不要把 `caseId` 再带批次前缀或用途后缀**（`-precheck`/`-dual-build` 之类）。
3. 收到 `403 identity_mismatch` 时，先比 `caseId` 与 `01-frozen/classification-1.json` 的 `case`（以及 `id`/`dir`），再怀疑文件哈希；**不要**重新分类来"凑"（分类源没变就不该重跑）。
4. 被拒的尝试**另存原始响应**（如 `attempt-1-403.json`）并在 item 记录里保留，计入 `failedAttempts`，**不消耗模型调用**。

---

## §13 C# **源**侧构建：runner 无 `csc`，必须补最小中性 `.csproj` 走 `dotnet build`（源自 D2-022，2026-10-11）

**现象**：D2-022（csharp-to-python，`Dump.cs`）首测用 `csc -out:program.exe Dump.cs` → `build failed`，stderr 仅 **`[WinError 2] 系统找不到指定的文件。`**（平台侧执行该命令时**找不到可执行体**）。

**根因**：Windows runner 上 **没有 `csc` 在 PATH**；C# 构建须经 .NET SDK。

**处置（依 [build-prerequisites §2.2/§3](../../../references/workflow/build-prerequisites.md)）**：为 C# 源补**最小中性 `.csproj`**（`AGENT_ADDED_CSPROJ`），并满足三条硬性要求——

1. **最小中性**：只声明 `OutputType=Exe`、`TargetFramework=net8.0`（本项目基线 C# 12/.NET 8）、`AssemblyName=program`、`RootNamespace`，以及**显式 `Compile Include="<源文件>"`**（配 `EnableDefaultCompileItems=false`，避免误纳其它文件）；**不得**引入源中不存在的包/命名空间/语言特性。
2. **记录"原本缺什么"**：在 `01-frozen/frozen-inputs.md` 写明 `原本无工程文件` / `补齐内容（含 .csproj 的 sha256）` / **`补齐后仍缺失的类型或符号`**（D2-022 为 **无**）。把"补了工程文件"写成"环境已就绪"是禁止的。
3. **随源码移交**：`.csproj` 属于**构建输入**，必须列入 capsule 的 `source/` 树。

**随之而来的两项强制动作**：

- **重新分类**：`.csproj` 进入 `source/` 树 ⇒ 源文件集合变化 ⇒ 必须**重跑分类**（`classification-1b.json`），并在提交时用**新**的那份 `this-task-classification.json`。
- **构建命令**：`dotnet build -c Release -o . <name>.csproj` ⇒ 产出 `program.exe`（apphost 名取自 `AssemblyName`），**driver 可直接定位**。

**反例警告**：**不得**用"补工程文件"掩盖**真实缺失的依赖**（如 `SharpUp` 缺类型、`pch.h`、`ICommand`）。若补齐后仍报"类型/命名空间不存在"，按**源依赖缺失**处理（阻断或另选完整源码），不用空桩冒充。判定依据是该次预检的**编译器诊断**。

---

## §14 以 `Console.ReadKey()` 结尾的 C# 源：`stderr` **无字节可比性**，平台判 `mismatched` 属**装置残留**（源自 D2-022/D2-023，2026-10-11）

**事实**：D2-022（`Dump.cs`）与 D2-023（`Describe.cs`）的 `Main` 末尾都有 `Console.ReadKey()`。平台驱动以**管道**（重定向）提供 stdin ⇒ .NET 抛：

```
Unhandled exception. System.InvalidOperationException: Cannot read keys when either application does not have a console or when console input has been redirected. Try Console.Read.
   at System.ConsolePal.ReadKey(Boolean intercept)
   at Program.Main(...) in C:\CodeConvertRemote\Stack\Agent\workspaces\eval-<jobid>\source\<file>.cs:line N
```

- 该 **stderr 非空**，且其中**含源侧工作目录绝对路径**（`...\source\...`）与 **.NET 运行时帧**；
- 平台**不支持** `stderrMode` 忽略（只有 `exact` / `normalized-text` / `json-structural`），而该绝对路径**不属于** `temporary-paths` 记号覆盖（只识 `/tmp`、`/var/tmp`、Windows `Temp`）；
- ⇒ 目标语言**不可能**逐字节复现 ⇒ 该类项**永远无法 `matched`**。

**处置（本轮采用的判据）**：

1. **仍走完整链路**（源侧预检 → 生成 → 自审 → 双侧评估），因为**转换质量主要由 stdout 判定**；
2. 目标须**同样失败**：stdin 非 TTY 时向 stderr 写出上文**首行**（**不伪造**栈帧）、并以源的退出码结束（本例 `4294967295`）；
3. **stdout 必须逐字节一致**——这是可修、也必须修的**真实转换缺陷**所在（D2-022 实证：目标曾把 `(All Users)` 误译为 `(Current User)`）；
4. `stderr` 的栈帧残留**归因为装置/运行时**，按纪律**保留平台原 `mismatched`、不自行改判**，在该项 `subject/attribution` 与 `result.md` 中如实分层登记；
5. 若需该类项也达到 `matched`，须**另冻条件**（平台把该路径类别纳入消噪，或冻结"仅比较 stdout"口径）——属新冻结条件，不回改历史记录。

**判据来源**：[`comparison-policy-adapter.md`](../../../references/adapter/controller/comparison-policy-adapter.md) §2「stdout、stderr 分别选择」与 §2.1「文本消噪的实际边界」。

## §15 输出含**真实执行耗时**的用例：oracle **不可冻结**，记 `ORACLE_NOT_FREEZABLE` + `PARTIAL`（源自 D2-042 / D2-043，2026-10-11）

### 事实

- D2-042（`process_pipeline_capture`）与 D2-043（`tcp_loopback_scanner`）都在 JSON 中输出 `duration_ms`（`time.Since(startTime).Milliseconds()`）。
- 两侧该字段**必然不同**（观测到 1 vs 2、57 vs 51），平台判 `output.status=mismatched`、`criticality=**major**`。
- 其余可观察量**逐字节相同**（D2-042：8 个字段全同；D2-043：`open_ports`/`scanned_count`/`status` 全同）。
- **关键**：平台显式消噪 token 仅 `temporary-paths`/`timestamps`/`ephemeral-ports`，**不含执行耗时**；`tolerate_minor=true` **未吸收**该差异（仍判 `major`）。

### 判据

- `duration_ms` 属 §10.16 所举的**活动计数器**类：**不可复现**（含调度抖动、`Sleep`、系统调用耗时），且**未被消噪覆盖**。
- ⇒ 该量**不能作为 oracle**；凡输出包含它的用例，其 oracle **不可冻结**。

### 规矩

1. **冻结阶段先判**：若输出含真实耗时/计数器类量，**在 `frozen-inputs.md` 的 oracle 可冻结性一节明确标注**，并写明"若平台判 mismatched 且差异**仅**为该字段 ⇒ 归因装置/环境，记 `ORACLE_NOT_FREEZABLE`"。
2. **终态**：记 `lifecycle=PARTIAL` + `oracleFreezability=ORACLE_NOT_FREEZABLE`；`verdicts.comparison` **保留平台原 verdict**（`mismatched`），**不自行改判**（§4.1）。
3. **确定性可观察量仍作证据单列**：`stdout`（除该字段外）/`exit_code`/`status`/排序结果等**照常核对并写入 `result.md`**，不得因一个不可冻结字段而放弃其余结论。
4. **恢复条件**：把该字段从比较面移除（另有冻结条件），或平台提供耗时消噪。

### 与既有条目的关系

- **§10.16 的具体实例**（"可观察量必须可复现"）：本条不新增原则，只补齐**执行耗时**这一类在**本平台消噪配置下不可容忍**的实测事实。
- 与 **§10.10**（两侧相同的失败输出也算 matched）相反方向：这里是"两侧**不同的**耗时不构成行为差异"，但平台按 `major` 处理，故必须由 Agent 归因、不得采信为转换失败。

## §16 装置优先：任一侧非零退出且 stdout 为空时，先排除驱动/装置故障（源自 D2-061 / D2-062，2026-10-11）

### 事实

同一会话内**两次**出现：**驱动（装置）自身崩坏**导致被测程序从未执行，而平台 verdict 与模型自审都指向"代码"。

- **D2-061**：`target/run_case.py` 用 `sed` 生成时把 `\n` 写成**真实换行** ⇒ `SyntaxError: unterminated string literal`；`target.rb` **从未运行**，平台判 `mismatched`（stdout 空，digest=`e3b0c442…`）；**模型自审此时误判 `REPAIR-RECOMMENDED`（2 项，均非真因）**。修正驱动后**同一 `target.rb` 逐字节 `matched`**，**未消耗任何模型修复调用**。
- **D2-062**：两侧驱动从先例复制后**未定义 `SIDE`**（`NameError: name 'SIDE' is not defined`，`run_case.py:38`）**且 source/target 两侧逻辑互换**；源程序**从未运行**，源侧 `build completed/0` 但 `exec=completed/1`、stdout 空。照 D2-061 可用形态重写驱动 ⇒ 需**重新分类**（驱动属 `source/` 树）⇒ 重跑预检 `build/exec` 均 `completed/0`。

### 判据与规矩

1. **任一侧非零退出且 stdout 为空 ⇒ 先排除驱动/装置故障**（驱动语法、路径、字节字面量、变量定义、两侧侧别是否互换），**再**归因转换。空输出（`digest=e3b0c442…`）是**装置故障的强信号**，不是代码结论。
2. **装置错误不记入转换失败**，也**不消耗模型修复调用**；先修装置、重跑后再判。
3. **改 `source/run_case.py` ⇒ 源树哈希变化 ⇒ 必须重新分类**（与 §12/§A1 同一硬约束）。
4. 模型自审的 `REPAIR-RECOMMENDED` 在**空 stdout** 情形下**不可信**：它针对"看起来可疑的代码"，而非实跑观测。
5. 重跑**保留原 job 目录**（故障证据），新增 `job-00b`/`job-01b` 等；`classification-1` 保留，重分类写 `classification-2`（分类器输出为**独占创建**，不覆盖历史）。

### 与既有条目的关系

- **§6 / §10.2** 的延伸：包装层自己的失败会伪装成被测程序的行为；本条把"装置先于转换"设为**首要分诊步骤**。
- **§12 / §A1** 的具体实例：驱动属 `source/` 树，改动即触发重分类。

---

## §17 独立源预检必须走 source-only 形态（`/api/source-preflights`），且 `buildCommand` 必须是 **argv token 数组**（源自 D2-197，2026-10-12）

### 事实

- 自 D2-197 起，本批源侧预检改走**当前协议**的独立源预检形态（此前 194 项沿用 1.0.28 时代的**旧双侧** `/api/jobs` + `comparison_manifest.json` + 占位 `target/`；那是**双侧 comparison**，不是独立源预检）。
- 正确形态（[platform-revision-adapter §2](../../../references/adapter/controller/platform-revision-adapter.md#2-独立源侧预检请求)）：
  - endpoint **`POST /api/source-preflights`**；multipart：`file`(source-only capsule.zip)、`caseId`、**`sourceOs`**、**`sourceLang=<源语言>`**、`classification`、`batchAuthorization`、（可选 `submissionId`）。
  - capsule **只含** `source_preflight_manifest.json`（kind=`codeconvert-source-preflight-manifest`）+ `input_profile.json` + `metadata.json` + **非空 `source/`**；**禁止 target 树 / 伪目标**。
  - **无入口库包**用 `evaluationMode=build-only`：**删除 `runCommand` 键**，InputProfile 1.0、`argv=[]`、`stdin=null`、`observationPolicy.dimensions=[]`、`comparisonPolicy={}`。
  - 报告为 **SourcePreflightReport 1.0**（kind=`codeconvert-source-preflight-report`）；取证走 `/report`、`/report.md`、`/evidence/source`、`/closure`、`/logs`；`runnerAssignments.target=null`、`executionStrategy="source-only"`。

### ⚠ 装置陷阱（D2-197 首次实证）

- `source.buildCommand` 是**数组**，平台按 **argv** 处理。首提误写**单元素整串**：
  ```json
  "buildCommand": ["go build -o program sort.go"]   // 错：整串被当可执行文件名
  ```
  ⇒ `build.status=failed`、`exitCode=None`、`durationMs=7`，`stderr` 仅
  `[Errno 2] No such file or directory: 'go build -o program sort.go'` ⇒ **源根本没被编译**，平台报 `buildAssessment=inconclusive`。
- **正确写法是 argv token 数组**：
  ```json
  "buildCommand": ["go", "build", "-o", "program", "sort.go"]
  ```
- 归因：**装置错误、非源缺陷**。修正后重提（`job-00b`），源真实编译（`exitCode=1`、377 ms），取得编译器原诊断。

### 规矩

1. 源预检一律 `POST /api/source-preflights`（`comparison` kind 只用于双侧 job-01）。
2. **`buildCommand` 逐 token 拆成数组元素**，不得写整串；`sourceLang` 写**源**语言。
3. source-only 形态**无驱动 `run_case.py`** ⇒ `source/` 树变化 ⇒ **必须重新分类**（分类结果另存递增编号，不覆盖旧的）；`this-task-classification.json` 同步更新为新版（残留旧版会 403 `identity_mismatch`）。
4. 装置失败另记 job（`job-00b`…），保留原 job 目录与拒绝/异常证据，不改写原记录（与 §16 一致）。
5. 首次提交前复核 `GET /api/health` 的 `supportedJobKinds` 含 `source-preflight`、`supportedEvaluationModes` 含 `build-only`。
