# stest (dmenu) 转换结果报告（run-01）

## 结论速览

本次把 `stest.c`（suckless dmenu 的 stat 测试工具，109 行 + 编译必需的本地头 `arg.h` 49 行）由 `.env` 配置模型一次性从 **C（C11, 纯 POSIX）** 转换为单文件 **C++（C++17）**，并**跨 OS 迁移 POSIX/Linux → Windows**。模型一次结构化自审判为 `NO-REPAIR-IDENTIFIED`，无自修轮。**目标代码已由第三方 Controller 真实编译通过**：双侧 comparison capsule 于 2026-09-28 经直连 Controller HTTP（`http://192.168.101.250:8443`，`POST /api/jobs`）提交，jobId=`eval-20260928-053745-2a386af5`，`jobStatus=COMPLETED`；真实回传证据落于 [`04-evaluation/job-02-dual-build/returned-evidence/`](04-evaluation/job-02-dual-build/returned-evidence/)。目标侧 `g++ -std=c++17 target.cpp -o program`（Windows VM `windows-eval`，MinGW/UCRT64）build `status=completed, exitCode=0, durationMs=3059`、stderr 空——本阶段据此判**编译=通过（PASS）**。源侧 C11 对照基线（Linux VM `linux-eval`）build 亦 `exitCode=0`（durationMs=274，stderr 空）。Controller 另返回 `behaviorVerdict=matched`（output 维度，覆盖率 1/1），但编译质量阶段不评功能、不设 oracle，功能仅作信息记录。

> **本 run 是本批（step-04 多系统 POSIX→Windows 文件系统）首例，且是 `skills/systems/posix-windows-filesystem` 的首个真实消费者。** 关键数据点：模型对 POSIX 文件系统面（`lstat`/`access(X_OK)`/`S_IS*`/`getline`/`PATH_MAX`）所加的 `#ifdef _WIN32` 兼容 shim 在 MinGW g++ `-std=c++17` 下**干净编译**——自审预警的 `ssize_t`/`dirent` 可见性问题**未在 Windows 目标侧实际触发**。

| 问题 | 结论 | 依据与边界 |
|---|---|---|
| 最终代码是否交付完整 | **已完成（交付完整单文件）** | [`target.cpp`](target.cpp) 为完整单文件，无截断/省略/Markdown 围栏；与生成稿 [`02-conversion/target.gen.cpp`](02-conversion/target.gen.cpp) 同一 sha256（`40a86f68…`），无自修 |
| 语法/编译是否正确 | **通过（PASS）** | Controller 真实回传：目标 build `status=completed, exitCode=0, durationMs=3059, stderr 空`（[`returned-evidence/evidence-target.json`](04-evaluation/job-02-dual-build/returned-evidence/evidence-target.json)）；工具链 Windows x64 MinGW/UCRT64 `g++ -std=c++17`，runner `windows-vm-agent-x64`；源侧 C11 对照基线（Linux）亦 `exitCode=0` |
| 功能是否一致 | **未计分（信息记录：matched）** | 本阶段为编译质量阶段，不设行为 oracle、不计入功能率；Controller comparison 返回 `behaviorVerdict=matched`、`codeVerdict=passed`、覆盖率 1/1（[`returned-evidence/evaluation_report.json`](04-evaluation/job-02-dual-build/returned-evidence/evaluation_report.json)），仅作信息记录 |

## 任务与最终交付

- 源码：suckless dmenu 的 `stest.c`，commit `61e0072c3e6adfc67bafbc84e376cf26bc3680c0`（MIT/X），109 行；伴随 `arg.h`（49 行，编译必需的本地头）。**跨 OS：C（C11, 纯 POSIX）→ C++（C++17, Windows）**，RAG 关闭，ATT&CK none。
- 执行形态 **跨 OS 双侧 build**（区别于 fe 的同 OS）：源侧 C 在 **Linux VM `linux-eval`** 作对照基线；目标侧 C++ 在 **Windows VM `windows-eval`**。`stest.c` 自带 `main`，两侧均直接链接为可执行 `program`，无需补入口。本阶段只取 build 证据。
- 冻结编译命令：源侧 `cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE stest.c -o program`；目标侧 `g++ -std=c++17 target.cpp -o program`。
- 最终交付文件 [`target.cpp`](target.cpp)（sha256 `40a86f68bab9aa34e4608969e2a436aea4b922187b4b32e331446c6bd3f63ca3`）；冻结输入与哈希见 [`01-frozen/frozen-inputs.md`](01-frozen/frozen-inputs.md)。这是无 RAG 探索稿，非正式验收基线。

## 转换过程与关键问题

1. **生成（GENERATED）**：`.env` 模型（`deepseek-flash`）一次生成完整单文件 C++（260 行），`finish_reason=stop` 未截断（[`02-conversion/target.gen.model.json`](02-conversion/target.gen.model.json)）。保留 `#include "arg.h"` 不并入；保留 flag 语义、退出码 `match?0:1`、`usage()` 退出 2、只读遍历副作用。POSIX→Windows 迁移改动集中在文件系统面：为 `_WIN32` 补 `PATH_MAX`(260)、`F_OK/X_OK/W_OK/R_OK`、`S_ISUID/S_ISGID`、经 `_S_IFMT` 定义 `S_ISDIR/S_ISREG/S_ISCHR`、`S_ISBLK/S_ISFIFO/S_ISLNK→(0)`；静态 shim `stest_access`（Windows 下 `X_OK`→`EACCES`）、`stest_lstat`（Windows 下 →-1）、`stest_getline`（基于 `fgetc`）；重命名源变量 `new`→`newst`（C++ 关键字冲突）；补 `#include <sys/types.h>` 取 `ssize_t`。
2. **自审（SELF_REVIEWED）**：模型一次结构化自审，报 **0 处转换引入缺陷**，`verdict=NO-REPAIR-IDENTIFIED`；另列 3 项判为工具链未知、需第三方编译确认的风险——(a) `ssize_t` 在 MinGW `-std=c++17`/`__STRICT_ANSI__` 下的可见性；(b) `dirent` 在 MinGW 的可用性；(c) `PATH_MAX`=260 vs Linux 4096 的截断行为差异。均未臆造缺陷。无自修轮（`SELF_REPAIRED` 未触发）。见 [`03-self-review/self-review-1.json`](03-self-review/self-review-1.json)。

## 验证依据与覆盖范围

- **静态**：Agent 全文件核对 + 模型结构化自审已做，分别记录在本报告与 [`03-self-review/`](03-self-review/)。
- **编译**：`通过（PASS）`。双侧 comparison capsule 已于 2026-09-28 提交 Controller（jobId=`eval-20260928-053745-2a386af5`，`COMPLETED`），真实回传证据存于 [`04-evaluation/job-02-dual-build/returned-evidence/`](04-evaluation/job-02-dual-build/returned-evidence/)：目标侧 build `status=completed, exitCode=0, durationMs=3059`、stderr 空；源侧对照基线 build `status=completed, exitCode=0, durationMs=274`、stderr 空。工具链目标侧 Windows x64 MinGW/UCRT64 `g++ -std=c++17`（runner `windows-vm-agent-x64`，VM `windows-eval`，snapshot `CC-Eval-Windows-8Lang-R7`），源侧 Linux x64 `cc -std=c11 …`（runner `linux-vm-agent-x64`，VM `linux-eval`，snapshot `CC-Eval-Linux-8Lang-R7`）。本机未编译。
- **运行/功能**：`未计分`。本阶段无行为 oracle；双侧运行仅为迁就 comparison capsule 契约。liveness 无参数启动、stdin 立即 EOF（`getline` 立即 EOF → `match=0` → 返回 1），两侧 `run_case.py` 均返回 `{"exitCode":1,"stderrLen":0,"stdoutLen":0}`，Controller comparison `behaviorVerdict=matched`、覆盖率 1/1，仅作信息记录，不计入功能率、不外推等价。

## 源侧 build 命令修正（job-01 → job-02，不倒填）

- **job-01（`eval-20260928-053326-9a8ae00e`）源侧基线 build FAILED**：初次冻结命令 `cc -std=c11 stest.c -o program` 缺 POSIX 特性测试宏，glibc 在严格 `-std=c11` 下隐藏 `lstat`（第 35 行隐式声明）、`PATH_MAX`（第 63 行未声明）、`getline`（第 86 行隐式声明）。dual-runner 因"源基线无法建立"**未构建目标侧**（target=`evidence_not_found`、comparison=`comparison_not_found`）。
- **归因**：这是**冻结的源侧 build 命令规格缺陷**（我方 capsule 规格），非源本身不可移植、非转换质量问题——dmenu 上游 `config.mk` 本就带 `-D_DEFAULT_SOURCE -D_POSIX_C_SOURCE=200809L`。
- **修正**：源侧命令补 `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE`，**目标侧命令与 `target.cpp` 均不改**（目标可编译性正是要测的数据点），以 job-02 重取真实证据。job-01 的真实失败证据保留于 [`04-evaluation/job-01-dual-build/returned-evidence/`](04-evaluation/job-01-dual-build/returned-evidence/)，不删除、不倒填为通过。这不是 oracle 篡改：修正的是阻断目标评估的错误源基线调用，不是为让失败变通过而改。

## 未决问题与下一步

1. 编译门槛已达成（Controller 真实回传 build 通过），本 run 进入 `EVALUATED`/`CLOSED`。
2. 自审列出的 3 项工具链未知风险中，`ssize_t`（经 `<sys/types.h>`）与 `dirent` 在本次目标工具链（MinGW/UCRT64 `g++ -std=c++17`）下均**未触发编译错误**；`PATH_MAX`=260 vs 4096 的截断差异属运行期行为，不在本编译质量阶段判定。
3. 本次无编译失败，未触发 `REPAIR_AFTER_EVAL`。若将来重跑失败，仅将可定位诊断交回 `.env` 模型做 ≤2 轮修订，保留原始稿，不盲改。
4. 本例数据点（POSIX-fs shim 在 MinGW g++ `-std=c++17` 干净编译；strict-c11 源基线特性测试宏教训）反哺 `skills/systems/posix-windows-filesystem`（step-05）。
