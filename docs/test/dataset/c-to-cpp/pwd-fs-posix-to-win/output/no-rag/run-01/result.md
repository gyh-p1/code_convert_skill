# pwd (FreeBSD) 转换结果报告（run-01）

## 结论速览

本次把 FreeBSD `bin/pwd/pwd.c`（123 行，BSD-3-Clause，无伴随本地头）由 `.env` 配置模型从 **C（C11, POSIX/BSD）** 转换为单文件 **C++（C++17）**，并**跨 OS 迁移 POSIX/Linux → Windows**。模型首轮结构化自审判 `REPAIR-RECOMMENDED`（2 项 transform-introduced），经**一轮自修（SELF_REPAIRED round 1）**后复审判 `NO-REPAIR-IDENTIFIED`，交付件为自修稿。**目标代码已由第三方 Controller 真实编译通过**：双侧 comparison capsule 于 2026-09-28 经直连 Controller HTTP（`http://192.168.101.250:8443`，`POST /api/jobs`）提交，jobId=`eval-20260928-064021-653f5ee9`，`jobStatus=COMPLETED`；真实回传证据落于 [`04-evaluation/job-01-dual-build/returned-evidence/`](04-evaluation/job-01-dual-build/returned-evidence/)。目标侧 `g++ -std=c++17 target.cpp -o program`（Windows VM `windows-eval`，MinGW/UCRT64）build `status=completed, exitCode=0, durationMs=3418`、stderr 空——本阶段据此判**编译=通过（PASS）**。源侧 C11 对照基线（Linux VM `linux-eval`）build 亦 `exitCode=0`（durationMs=549，stderr 空）。

> **诚实标注：Controller 综合报告的 `codeVerdict=failed`、`behaviorVerdict=mismatched` 不是编译失败。** 它完全来自唯一被观测的 output 维度：两侧 liveness 均无参数、无操作数运行（默认物理模式打印当前工作目录），退出码同为 0、stderr 同为空，仅 **stdout 长度不同**（源侧 Linux 路径 75 字节 vs 目标侧 Windows 路径 82 字节）。这正是本 case 冻结时即写明的**按设计的跨 OS 差异**——当前工作目录的绝对路径文本与分隔符（`/…/workspace/source` vs `C:\…\workspace\target`）本就随 OS 不同。编译质量阶段**不设行为 oracle、不计功能**，该 mismatch 仅作信息记录，不改变编译=PASS 的结论，也不表示转换缺陷。

| 问题 | 结论 | 依据与边界 |
|---|---|---|
| 最终代码是否交付完整 | **已完成（交付完整单文件）** | [`target.cpp`](target.cpp) 为完整单文件，无截断/省略/Markdown 围栏；内容与自修稿 [`02-conversion/target.repair-1.cpp`](02-conversion/target.repair-1.cpp) 同一 sha256（`8690433e…`）。**非生成稿**：生成稿 `02-conversion/target.gen.cpp` 经一轮自修 |
| 语法/编译是否正确 | **通过（PASS）** | Controller 真实回传：目标 build `status=completed, exitCode=0, durationMs=3418, stderr 空`（[`returned-evidence/evidence-target.json`](04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json)）；工具链 Windows x64 MinGW/UCRT64 `g++ -std=c++17`，runner `windows-vm-agent-x64`；源侧 C11 对照基线（Linux）亦 `exitCode=0` |
| 功能是否一致 | **未计分（信息记录：mismatched，属已知平台差异）** | 本阶段为编译质量阶段，不设行为 oracle、不计入功能率；Controller comparison 返回 `behaviorVerdict=mismatched`、`codeVerdict=failed`、覆盖率 1/1（[`returned-evidence/evaluation_report.json`](04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json)）。唯一 diff 为 output 维度的 stdout 长度（75 vs 82），源于打印当前工作目录的绝对路径文本随 OS 不同（分隔符 + 路径），退出码与 stderr 均一致；仅作信息记录 |

## 任务与最终交付

- 源码：FreeBSD `bin/pwd/pwd.c`，tag `release/14.2.0`（commit `89042d64c83ca92d90bd3d161eebc353d5edb3c6`，BSD-3-Clause），123 行；**无伴随本地头**。**跨 OS：C（C11, POSIX/BSD）→ C++（C++17, Windows）**，RAG 关闭，ATT&CK none。
- 执行形态 **跨 OS 双侧 build**：源侧 C 在 **Linux VM `linux-eval`** 作对照基线；目标侧 C++ 在 **Windows VM `windows-eval`**。`pwd.c` 自带 `main`，两侧均直接链接为可执行 `program`，无需补入口。本阶段只取 build 证据。
- 冻结编译命令：源侧 `cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__dead2= pwd.c -o program`；目标侧 `g++ -std=c++17 target.cpp -o program`。
- 最终交付文件 [`target.cpp`](target.cpp)（sha256 `8690433e84a87eab984eb9e29d8e554b3e64a615285d441e7e265f43051e19d6`）；冻结输入与哈希见 [`01-frozen/frozen-inputs.md`](01-frozen/frozen-inputs.md)。这是无 RAG 探索稿，非正式验收基线。

## 转换过程与关键问题

1. **生成（GENERATED）**：`.env` 模型（`deepseek-flash`）一次生成完整单文件 C++（299 行），`finish_reason=stop` 未截断（`reasoning_tokens=29964`，印证高 token 上限必要）。POSIX/BSD→Windows 迁移改动：`__dead2`→`[[noreturn]]`；`getcwd(NULL,0)`→`_getcwd(NULL,0)`（`<direct.h>`，附 malloc+ERANGE 增长回退 `getcwd_physical()`）；`<err.h>`/`err` 缺失 → 本地 `err_exit` shim（"progname: fmt: strerror(errno)"，保 errno 纪律）；`getopt`/`optind` → 自包含 `pwd_getopt`/`pwd_optind`/`pwd_optpos`；`set_progname` 取 basename。见 [`02-conversion/target.gen.cpp`](02-conversion/target.gen.cpp)。
2. **自审（SELF_REVIEWED，round 1）**：模型结构化自审报 **2 项 transform-introduced 缺陷**，`verdict=REPAIR-RECOMMENDED`（[`03-self-review/self-review-1.json`](03-self-review/self-review-1.json)）：(1)【声明顺序阻断点】main 在 `argc -= pwd_optind; argv += pwd_optind;` 处引用 `pwd_optind`，而 `static int pwd_optind = 1;`（及 `pwd_optpos`）定义在 main 之后——C++ 无隐式声明，必然编译失败（可机械上移修复）；(2) `getcwd_logical()` 加入的 `lg.st_ino != 0 &&` 守卫改变源可观察行为（Windows 上 stat() 恒 st_ino==0，源式身份比较会误判同卷任意 $PWD 为一致；守卫使 -L 保守回落物理 getcwd，本工具链无可机械修复的等价，记为已知差异）。
3. **自修（SELF_REPAIRED，round 1）**：把自审 + 源 + 生成稿回喂 `.env` 模型产出修正单文件 [`02-conversion/target.repair-1.cpp`](02-conversion/target.repair-1.cpp)：(1) 把 `static int pwd_optind = 1;`/`static int pwd_optpos = 1;` 上移到 main 之前的前向声明区，全文件仅一处定义（无重复、无 main 之后残留）；(2) 保留 `st_ino != 0` 守卫，并在文件顶部注释显式登记为 KNOWN PLATFORM DIFFERENCE（-L 在 Windows 恒回落物理路径），不臆造 GetFileInformationByHandle 等未验证等价。
4. **复审（SELF_REVIEWED，round 2 = 修复后复审）**：模型复审判两项前置缺陷分别 `resolved`（声明顺序）/`accepted-known-difference`（st_ino 守卫），且自修动作未引入新的可定位缺陷，`verdict=NO-REPAIR-IDENTIFIED`（[`03-self-review/self-review-2.json`](03-self-review/self-review-2.json)）。据此进入 EVALUATION_READY。

## 验证依据与覆盖范围

- **静态**：Agent 全文件核对 + 模型两轮结构化自审（首轮定位 + 修复后复审）已做，记录于本报告与 [`03-self-review/`](03-self-review/)。
- **编译**：`通过（PASS）`。双侧 comparison capsule 已于 2026-09-28 提交 Controller（jobId=`eval-20260928-064021-653f5ee9`，`COMPLETED`），真实回传证据存于 [`04-evaluation/job-01-dual-build/returned-evidence/`](04-evaluation/job-01-dual-build/returned-evidence/)：目标侧 build `status=completed, exitCode=0, durationMs=3418`、stderr 空；源侧对照基线 build `status=completed, exitCode=0, durationMs=549`、stderr 空。工具链目标侧 Windows x64 MinGW/UCRT64 `g++ -std=c++17`（runner `windows-vm-agent-x64`，VM `windows-eval`，snapshot `CC-Eval-Windows-8Lang-R7`），源侧 Linux x64 `cc -std=c11 …`（runner `linux-vm-agent-x64`，VM `linux-eval`，snapshot `CC-Eval-Linux-8Lang-R7`）。本机未编译。声明顺序阻断点经自修后目标侧一次即干净编译通过。
- **运行/功能**：`未计分`。本阶段无行为 oracle；双侧运行仅为迁就 comparison capsule 契约。liveness 无参数、无操作数启动、stdin 立即 EOF（默认物理模式打印当前工作目录），源侧 `run_case.py` 返回 `{"exitCode":0,"stderrLen":0,"stdoutLen":75}`、目标侧 `{"exitCode":0,"stderrLen":0,"stdoutLen":82}`，Controller comparison `behaviorVerdict=mismatched`（唯一 diff：output 维度 stdout 长度，`stream.structuredValue`，criticality major）、覆盖率 1/1。**该 mismatch 是冻结时即预告的跨 OS 路径文本差异（分隔符 + 绝对路径），非转换缺陷，仅作信息记录，不计入功能率、不外推等价。**

## 关键数据点（反哺 Skill，step-05）

1. **自定义 getopt 状态变量的声明顺序是真实的 transform-introduced 编译阻断点**：源用 `<unistd.h>` 的 `optind`（翻译单元外声明），转换替换为自定义 `static int pwd_optind`/`pwd_optpos` 时若定义留在 main 之后，C++ 无隐式声明 → main 引用点 `'pwd_optind' was not declared in this scope` 硬错误。把两个静态计数器上移到 main 之前、单次定义后，目标侧干净编译通过（exitCode=0）——印证"替换外部符号为自定义全局态时必须前置声明/定义"规则。
2. **`getcwd(NULL,0)`→`_getcwd(NULL,0)`（`<direct.h>`）在 MinGW/UCRT64 `g++ -std=c++17` 下可用**：附 malloc+ERANGE 增长回退，目标 build+run 均 exitCode=0；self-review 列作 toolchain-unknown 的 `_getcwd(NULL,0)` 自动分配语义、`<sys/stat.h>` 在 `__STRICT_ANSI__` 下暴露 `struct stat`/`st_ino` 实测均未触发编译错误。
3. **Windows `stat()` 恒 `st_ino==0` 是不可机械修复的身份校验平台边界**：源 `getcwd_logical()` 靠 `(st_dev, st_ino)` 判定 `$PWD` 与 `.` 同一；Windows 上 st_ino 恒 0、st_dev 仅卷号，(dev,ino) 会对同卷任意 $PWD 误判一致。自修保留保守 `st_ino != 0` 守卫使 -L 安全回落物理 getcwd，并在注释登记为已知差异；真实等价需 `GetFileInformationByHandle()`（卷序列号+文件索引），未臆造引入。
4. **`__dead2` 源可移植教训**（与 realpath 一致）：FreeBSD `<sys/cdefs.h>` 的 `__dead2` glibc 不定义；源侧基线以 `-D__dead2=` 中和（源不改），与 `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE` 一并在命令行满足，源基线一次即 build 通过。

## 未决问题与下一步

1. 编译门槛已达成（Controller 真实回传 build 通过），本 run 进入 `EVALUATED`/`CLOSED`。
2. `behaviorVerdict=mismatched` 已归因为按设计的跨 OS 路径文本差异（stdout 长度 75 vs 82），不在本编译质量阶段判定，不触发 `REPAIR_AFTER_EVAL`（该门槛只针对编译失败）。
3. 本例数据点（自定义 getopt 状态声明顺序、`getcwd`→`_getcwd(NULL,0)`、`err`→`err_exit` shim、`st_ino==0` 身份校验边界、`__dead2` 源基线中和）反哺 `skills/systems/posix-windows-filesystem` 与 `c-to-cpp`（step-05）。
4. 批次继续：下一例 `du`（走完整环路，预告为预期偏难/失败数据点：fts/libutil/SIGINFO/UF_NODUMP 在 glibc 与 MinGW 均缺失）。
