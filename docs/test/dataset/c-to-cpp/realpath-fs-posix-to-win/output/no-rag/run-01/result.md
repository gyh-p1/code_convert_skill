# realpath (FreeBSD) 转换结果报告（run-01）

## 结论速览

本次把 FreeBSD `usr.bin/realpath/realpath.c`（82 行，BSD-3-Clause，无伴随本地头）由 `.env` 配置模型从 **C（C11, POSIX/BSD）** 转换为单文件 **C++（C++17）**，并**跨 OS 迁移 POSIX/Linux → Windows**。模型首轮结构化自审判 `REPAIR-RECOMMENDED`（3 项 transform-introduced），经**一轮自修（SELF_REPAIRED round 1）**后复审判 `NO-REPAIR-IDENTIFIED`，交付件为自修稿。**目标代码已由第三方 Controller 真实编译通过**：双侧 comparison capsule 于 2026-09-28 经直连 Controller HTTP（`http://192.168.101.250:8443`，`POST /api/jobs`）提交，jobId=`eval-20260928-060834-49b1a302`，`jobStatus=COMPLETED`；真实回传证据落于 [`04-evaluation/job-01-dual-build/returned-evidence/`](04-evaluation/job-01-dual-build/returned-evidence/)。目标侧 `g++ -std=c++17 target.cpp -o program`（Windows VM `windows-eval`，MinGW/UCRT64）build `status=completed, exitCode=0, durationMs=3442`、stderr 空——本阶段据此判**编译=通过（PASS）**。源侧 C11 对照基线（Linux VM `linux-eval`）build 亦 `exitCode=0`（durationMs=1224，stderr 空）。

> **诚实标注：Controller 综合报告的 `codeVerdict=failed`、`behaviorVerdict=mismatched` 不是编译失败。** 它完全来自唯一被观测的 output 维度：两侧 liveness 均无参数运行、规范化当前目录 `"."`，退出码同为 0、stderr 同为空，仅 **stdout 长度不同**（源侧 Linux 路径 75 字节 vs 目标侧 Windows 路径 82 字节）。这正是本 case 冻结时即写明的**按设计的跨 OS 差异**——规范化绝对路径的文本与分隔符（`/…/workspace/source` vs `C:\…\workspace\target`）本就随 OS 不同。编译质量阶段**不设行为 oracle、不计功能**，该 mismatch 仅作信息记录，不改变编译=PASS 的结论，也不表示转换缺陷。

| 问题 | 结论 | 依据与边界 |
|---|---|---|
| 最终代码是否交付完整 | **已完成（交付完整单文件）** | [`target.cpp`](target.cpp) 为完整单文件，无截断/省略/Markdown 围栏；内容与自修稿 [`02-conversion/target.repair-1.cpp`](02-conversion/target.repair-1.cpp) 同一 sha256（`460303a4…`）。**非生成稿**：生成稿 `02-conversion/target.gen.cpp` 经一轮自修 |
| 语法/编译是否正确 | **通过（PASS）** | Controller 真实回传：目标 build `status=completed, exitCode=0, durationMs=3442, stderr 空`（[`returned-evidence/evidence-target.json`](04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json)）；工具链 Windows x64 MinGW/UCRT64 `g++ -std=c++17`，runner `windows-vm-agent-x64`；源侧 C11 对照基线（Linux）亦 `exitCode=0` |
| 功能是否一致 | **未计分（信息记录：mismatched，属已知平台差异）** | 本阶段为编译质量阶段，不设行为 oracle、不计入功能率；Controller comparison 返回 `behaviorVerdict=mismatched`、`codeVerdict=failed`、覆盖率 1/1（[`returned-evidence/evaluation_report.json`](04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json)）。唯一 diff 为 output 维度的 stdout 长度（75 vs 82），源于规范化路径文本随 OS 不同（分隔符 + 路径），退出码与 stderr 均一致；仅作信息记录 |

## 任务与最终交付

- 源码：FreeBSD `usr.bin/realpath/realpath.c`，tag `release/14.2.0`（commit `89042d64c83ca92d90bd3d161eebc353d5edb3c6`，BSD-3-Clause），82 行；**无伴随本地头**。**跨 OS：C（C11, POSIX/BSD）→ C++（C++17, Windows）**，RAG 关闭，ATT&CK none。
- 执行形态 **跨 OS 双侧 build**：源侧 C 在 **Linux VM `linux-eval`** 作对照基线；目标侧 C++ 在 **Windows VM `windows-eval`**。`realpath.c` 自带 `main`，两侧均直接链接为可执行 `program`，无需补入口。本阶段只取 build 证据。
- 冻结编译命令：源侧 `cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__dead2= realpath.c -o program`；目标侧 `g++ -std=c++17 target.cpp -o program`。
- 最终交付文件 [`target.cpp`](target.cpp)（sha256 `460303a47c2eb5f5a40c5e30cdab021f8d1c19a1adc01eb2b1b4d343ab9ff72a`）；冻结输入与哈希见 [`01-frozen/frozen-inputs.md`](01-frozen/frozen-inputs.md)。这是无 RAG 探索稿，非正式验收基线。

## 转换过程与关键问题

1. **生成（GENERATED）**：`.env` 模型（`deepseek-flash`）一次生成完整单文件 C++（198 行），`finish_reason=stop` 未截断（`reasoning_tokens=21753`，印证高 token 上限必要）。POSIX/BSD→Windows 迁移改动：`__dead2`→`[[noreturn]]`；`#ifndef PATH_MAX`→`_MAX_PATH`(260) 回退；`<err.h>`/`warn` 缺失 → 本地 `warn` shim（"progname: msg: strerror(errno)"，保 errno 纪律）；`realpath(3)` 无等价 → `_fullpath`+`_access` shim；`getopt` 初版以手写 `-q` 解析替代；`set_progname` 取 basename。见 [`02-conversion/target.gen.cpp`](02-conversion/target.gen.cpp)。
2. **自审（SELF_REVIEWED，round 1）**：模型结构化自审报 **3 项 transform-introduced 缺陷**，`verdict=REPAIR-RECOMMENDED`（[`03-self-review/self-review-1.json`](03-self-review/self-review-1.json)）：(1) 自定义全局 `realpath` 与 mingw-w64 `<stdlib.h>` 可能声明的 `realpath` 冲突（可机械改名 `x_realpath`，影响编译）；(2) 手写选项解析丢失 getopt 的参数置换与未知选项诊断；(3) `realpath`→`_fullpath`+`_access` 丢失符号链接解析/分隔符/260 长度（本工具链不可机械修复，记为已知差异）。
3. **自修（SELF_REPAIRED，round 1）**：把自审 + 源 + 生成稿回喂 `.env` 模型产出修正单文件 [`02-conversion/target.repair-1.cpp`](02-conversion/target.repair-1.cpp)：(1) `realpath` shim 与调用点改名 `x_realpath`（消歧，零语义风险）；(2) 改用 `<getopt.h>`（libmingwex 提供 getopt/optind）恢复参数置换与无效选项诊断；(3) 在文件顶部注释显式列明符号链接/分隔符/260 长度/诊断本地化为已知平台差异。
4. **复审（SELF_REVIEWED，round 2 = 修复后复审）**：模型复审判三项前置缺陷分别 `resolved`/`resolved`/`accepted-known-difference`，且自修动作未引入新的可定位缺陷，`verdict=NO-REPAIR-IDENTIFIED`（[`03-self-review/self-review-2.json`](03-self-review/self-review-2.json)）。据此进入 EVALUATION_READY。

## 验证依据与覆盖范围

- **静态**：Agent 全文件核对 + 模型两轮结构化自审（首轮定位 + 修复后复审）已做，记录于本报告与 [`03-self-review/`](03-self-review/)。
- **编译**：`通过（PASS）`。双侧 comparison capsule 已于 2026-09-28 提交 Controller（jobId=`eval-20260928-060834-49b1a302`，`COMPLETED`），真实回传证据存于 [`04-evaluation/job-01-dual-build/returned-evidence/`](04-evaluation/job-01-dual-build/returned-evidence/)：目标侧 build `status=completed, exitCode=0, durationMs=3442`、stderr 空；源侧对照基线 build `status=completed, exitCode=0, durationMs=1224`、stderr 空。工具链目标侧 Windows x64 MinGW/UCRT64 `g++ -std=c++17`（runner `windows-vm-agent-x64`，VM `windows-eval`，snapshot `CC-Eval-Windows-8Lang-R7`），源侧 Linux x64 `cc -std=c11 …`（runner `linux-vm-agent-x64`，VM `linux-eval`，snapshot `CC-Eval-Linux-8Lang-R7`）。本机未编译。
- **运行/功能**：`未计分`。本阶段无行为 oracle；双侧运行仅为迁就 comparison capsule 契约。liveness 无参数启动、stdin 立即 EOF（无操作数 → 规范化 `"."`），源侧 `run_case.py` 返回 `{"exitCode":0,"stderrLen":0,"stdoutLen":75}`、目标侧 `{"exitCode":0,"stderrLen":0,"stdoutLen":82}`，Controller comparison `behaviorVerdict=mismatched`（唯一 diff：output 维度 stdout 长度）、覆盖率 1/1。**该 mismatch 是冻结时即预告的跨 OS 路径文本差异（分隔符 + 绝对路径），非转换缺陷，仅作信息记录，不计入功能率、不外推等价。**

## 关键数据点（反哺 Skill，step-05）

1. **`realpath` 命名冲突是真实的 transform-introduced 编译风险**：mingw-w64 `<stdlib.h>` 声明了外部链接 `realpath`，自定义 `static realpath` 会触发 `static declaration follows non-static declaration` 硬错误。改名 `x_realpath` 后目标侧干净编译通过（exitCode=0）——印证"自定义同名 POSIX 符号须改名消歧"这一规则。
2. **`<getopt.h>`/getopt/optind 在 MinGW/UCRT64 `g++ -std=c++17` 下可用**：改用系统 getopt（libmingwex）既恢复参数置换/诊断语义、又通过编译，未出现 `extern "C"` 名字修饰导致的未定义引用。
3. **`__dead2` 源可移植教训**：FreeBSD `<sys/cdefs.h>` 的 `__dead2` glibc 不定义；源侧基线以 `-D__dead2=` 中和（源不改），与 `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE` 一并在命令行满足，源基线一次即 build 通过。
4. **`realpath`→`_fullpath`+`_access` 的符号链接/260 长度差异**是本工具链不可机械修复的平台差异，已在交付件顶部注释与本报告如实记录，未臆造等价实现。

## 未决问题与下一步

1. 编译门槛已达成（Controller 真实回传 build 通过），本 run 进入 `EVALUATED`/`CLOSED`。
2. `behaviorVerdict=mismatched` 已归因为按设计的跨 OS 路径文本差异（stdout 长度 75 vs 82），不在本编译质量阶段判定，不触发 `REPAIR_AFTER_EVAL`（该门槛只针对编译失败）。
3. 本例数据点（`realpath`/`x_realpath` 消歧、`_fullpath`+`_access`、`warn` shim、`getopt` via `<getopt.h>`、`__dead2` 源基线中和）反哺 `skills/systems/posix-windows-filesystem` 与 `c-to-cpp`（step-05）。
4. 批次继续：下一例 `pwd`，再 `du`（各走完整环路）。
