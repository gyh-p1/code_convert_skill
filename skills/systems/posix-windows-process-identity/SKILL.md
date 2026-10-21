---
name: posix-windows-process-identity
description: Use as the source-OS -> target-OS layer when source code starts child processes, replaces its own image, waits with a timeout, kills descendants, or checks/raises its own identity and privileges across POSIX/Linux and Windows. Covers process-information, token/privilege, error-model and cleanup differences that are not 1:1. Not a language mapping, not the thread layer, and not a portability or behavior guarantee.
---

# POSIX ↔ Windows 进程创建与身份/权限系统方向

> **加载前置**：先读取根[转换入口](../../../SKILL.md)并完成其必读契约与语言/方向选择；本页补充系统映射，不单独推进转换。

本 Skill 是**系统方向**知识（源 OS → 目标 OS）中的进程与身份层，只覆盖 POSIX/Linux 与 Windows 之间的进程创建/替换/等待/终止、以及进程自身的身份与特权差异。它与语言方向 Skill（如 [C → C++](../../directions/c-to-cpp/SKILL.md)）、[进程执行场景](../../scenes/process-execution/SKILL.md) **共同阅读**：语言方向负责语法/类型/错误模型映射，进程执行场景负责子进程树、管道、超时与输出语义，本 Skill 只负责两个平台系统接口的差异与不可映射项。它是静态规则与风险说明，**不保证**目标代码可编译、可移植或行为等价。

线程生命周期（`pthread_*` ↔ CRT/Win32 线程）不在本 Skill，见 [POSIX ↔ Windows 线程](../posix-windows-threads/SKILL.md)。

## 触发条件与前提

- **触发**：源码确有进程级行为——创建子进程（`fork`/`exec*`/`posix_spawn`/`system`/`popen`/`CreateProcess*`/`ShellExecute*`/`WinExec`）、等待或观测退出状态（`waitpid`/`WaitForSingleObject`/退出码）、终止（`kill`/`TerminateProcess`/`TerminateJobObject`）、改变自身身份或特权（`setuid`/`seteuid`/`setgid` ↔ 令牌与特权 API）、查询进程/身份信息（`getuid`/`geteuid` ↔ `OpenProcessToken`/`GetTokenInformation`/`LookupPrivilegeValue`）。
- **前提**：先冻结源/目标 OS 与版本、目标工具链与 SDK、目标 CRT（MSVC 还是 MinGW/UCRT64）、目标子系统（控制台/窗口/服务）、是否要求进程树语义、是否需要提权或降权、以及目标语言运行时是否已封装进程 API。这些不明且影响判断时先询问或标为待确认。
- **方向必须区分**：POSIX → Windows 与 Windows → POSIX 的补全项不对称（见"方向不对称的陷阱"），不能按同一张表双向套用。
- 若目标语言运行时自带进程抽象（Go `os/exec`、Python `subprocess`、.NET `System.Diagnostics.Process`、PowerShell 原生命令），本 Skill 只用于核对**该抽象是否保持了源程序的可观察义务**；具体 API 选择由语言方向 Skill 决定。

## 应始终保留的可观察行为

只换平台接口，不改这些语义；无法保持时须显式说明，不静默降级：

- **进程树与启动归属**：创建了几个进程、父子关系、谁先退出、后代是否随父终止。
- **等待时机与退出状态**：等待的是"直接进程退出"还是"输出管道排空"；退出码的实际取值与截断（POSIX 可观察的只有低 8 位，见下）；信号/异常终止与正常退出的区分。
- **标准流与重定向**：三个标准流是否被继承、重定向或管道化；管道缓冲区写满会阻塞子进程。
- **身份与特权**：进程以谁的身份运行、能否恢复原身份、哪些特权被启用；特权不足时的失败类别（是启动失败还是运行中失败）。
- **错误分类与来源**：POSIX `errno`、CRT `errno`、Win32 `GetLastError()`、`LONG`/`BOOL` 返回是不同来源，不能混读或在后续调用后读取。
- **资源清理顺序**：句柄/文件描述符、作业对象、临时文件的关闭与删除顺序，以及失败路径上的清理。

## 原生 fork/exec 事实

同 OS 的语言转换也按实际 fork/exec API 读取本节；下面跨系统映射表仅在对应 OS 分支适用。C11/C++17 本身不定义这些 API，不能把 POSIX/Linux 事实归为语言标准保证。

- **fork**：成功在父进程返回子 PID、在子进程返回 0；失败在父返回 -1 并设 errno，不产生子进程。目标语言返回形态另读其语言页；保留父、子、失败三个出口，不能以通用真值判断替代。
- **exec**：通常成功替换当前映像而不返回，PID 保持；失败返回 -1 并设 errno，后续续行/退出依源代码。准确 API 的极端失败、继承资源与多线程限制依冻结 OS 核，不把异常退出一概判为目标转换差异。
- **环境**：execve 显式 envp 描述新环境，不是增量覆盖；execv/execvp 等无 envp 形式依其 API 继承环境。Linux 接受 NULL envp 并按空环境处理，这是非标准、不可移植行为；其他 OS 不得默认空环境或继承。完整替换、空环境、继承、合并覆盖是不同契约。
- **条件映射与反例**：仅在实际源 API、平台及调用参数确定后选择目标；Ruby 空环境 hash 默认仍继承，spawn/system 也不等于 exec 的替换模型。失败返回改成异常时须保持源可观察续行，不盲目补 exit 或吞掉整个函数的错误。
- **未知处理**：OS、envp 形态、失败出口或映像替换义务不明则记缺口；不从“子程序同样运行”推断进程身份与生命周期等价。
- **官方依据**：POSIX fork、exec；Linux fork(2)、execve(2)、exec(3)。

## 原生环境块、令牌与缓冲的选择引导

Windows同OS的语言转换涉及这些API时也适用；只据精确SDK/架构和调用点选择，不增加执行或自审门禁。

- **环境块**：GetEnvironmentStrings返回NUL分隔、双NUL终止的块，使用后按对应FreeEnvironmentStrings释放。块中可有以`=`开头的驱动器当前目录项，按首个等号直接split成普通字典可能丢掉名称；A/W及具体窄字符编码不能凭ASCII样例推定。先看源是否枚举、过滤或原样转交，再选目标环境抽象，复制内容与保持借用生命周期分开。
- **可变长令牌结构**：TOKEN_PRIVILEGES含PrivilegeCount与LUID_AND_ATTRIBUTES数组；数组实际长度由返回信息决定，SDK声明的占位元素不是长度上限。DWORD、LONG、BOOL及LUID字段不会因为进程指针位宽变化就自动变成指针宽度。目标可采用精确布局/封装，但须对应头部、元素、对齐和返回缓冲长度，不将某结构的偏移数值推广到所有结构。
- **有效权限**：成员SID、enabled/deny-only属性、线程模拟与进程令牌不同。AccessCheck的安全描述符、模拟令牌、desired access及generic mapping决定结果；BOOL调用结果与AccessStatus输出也不同。先定位源检查对象，再选成员查询或访问判定，不以组名存在替代有效权限，不从“管理员”一词推出全部权限。
- **描述符与ACL身份**：Windows SDK的AccessCheck首参要求完整安全描述符，不是其DACL地址；即使底层声明容许void指针，编译通过也不证明对象正确。GetNamedSecurityInfo返回的DACL等指针指向其安全描述符内相应部分，按实际请求标志/成功状态核有效性；返回描述符缓冲用LocalFree释放后，这些内部指针不能继续使用，也不分别释放。调用失败与AccessStatus拒绝分别按源路径传播，不能合成“检查恒假”。此规则只用于保持已有访问检查，不改变访问权或扩张权限。
- **缓冲与初始化**：区分容量、有效长度、NUL和字节/字符单位；语言模块或DLL加载不等于对应系统API的初始化成功。源固定容量、初始化失败时机及后续错误路径按原调用保持，原代码越界风险单列，不因源UB省略目标容量分析。

依据：Microsoft Win32 GetEnvironmentStrings/FreeEnvironmentStrings、TOKEN_PRIVILEGES/LUID_AND_ATTRIBUTES、AccessCheck及Access Tokens；布局和编码的精确版本不明时记录缺口，不猜数值。此处只补转换选择知识，不提供权限扩张方法。

## 核心差异映射表

每行给出必须动手改的点，而不是"名字相近即可"。

| 主题 | POSIX/Linux | Windows | 转换必须处理的点 |
|---|---|---|---|
| 创建进程 | `fork` + `exec*`；`posix_spawn` | `CreateProcessA/W`（可同时创建挂起进程） | CreateProcess 无内存副本/双返回语义；只有源子分支的全部义务可由启动配置保持时才考虑整体映射，否则明确缺口 |
| 不替换映像的创建 | `fork` 后不 `exec` | 无直接等价；`CreateProcess` 会加载新映像 | 子分支继续执行源状态不等于加载新映像；仅能表达在启动参数/环境中的配置不能代表整个子分支 |
| 替换自身映像 | `execv`/`execvp`/`execve`（成功不返回） | Win32 CreateProcess 无此语义；CRT `_exec*` 另核其具体契约 | 创建子进程、等待或返回不能保持原 PID/映像生命周期；无法保持时报告映射缺口，仅在任务明确允许对应差异时采用替代设计 |
| 多线程进程内 fork | `fork` 只允许在子进程内调用 async-signal-safe 函数，直到 `exec` | 不适用 | 源程序若有工作线程，`fork` 目标侧的等价语义须显式评估；不要假设 C 运行时锁状态在子进程内可用 |
| shell 调用 | `system`/`popen` 走 `/bin/sh -c` | `system`/`_popen` 走 `cmd.exe /C`；`ShellExecute*` 走 shell 关联 | 解释器不同（引用、展开、内建命令、退出码）；`ShellExecute` 是返回值语义完全不同的 shell 关联 API，不能当 `system` 用 |
| 直接可执行 + argv | `execvp`/`posix_spawn` | `CreateProcess` 的 `lpApplicationName` + `lpCommandLine` | Windows 命令行是**单个字符串**且由被调方自行解析；参数必须按目标程序的解析规则引用，不能直接把 argv 数组拼空格 |
| 等待 | `waitpid`/`wait` | `WaitForSingleObject`/`WaitForMultipleObjects` + `GetExitCodeProcess` | 等待成功不代表句柄已关闭、也不代表输出已读完；`WaitForSingleObject` 不返回退出码 |
| 退出码读取 | `waitpid` 输出参数 + `WIFEXITED`/`WEXITSTATUS` | `GetExitCodeProcess` 的 `DWORD` | POSIX 退出状态是编码值（信号终止时 `WEXITSTATUS` 无意义）；Windows 是被截断的 32 位值；`WIFEXITED` 等宏在 Windows CRT 上不可用 |
| 退出码可观察范围 | 只有低 8 位对 shell/父进程可观察 | 完整 32 位可被父进程读取 | 源若依赖"退出码 256 会变成 0"，目标侧行为不同，属可观察差异 |
| 终止直接进程 | `kill(pid, SIGTERM/SIGKILL)` | `TerminateProcess`（无信号、不执行目标进程清理） | 信号是"可被捕获的请求"，`TerminateProcess` 是强制终止；两者不能互称等价 |
| 终止进程树 | 进程组 + `kill(-pgid, sig)` | 作业对象（job object）+ `TerminateJobObject`，或 `taskkill /T` | 只终止直接子进程不构成进程树终止；子进程自己再创建进程时必须有作业对象等机制才能全树回收 |
| 控制台信号 | `SIGINT`/`SIGTERM` 处理函数 | `SetConsoleCtrlHandler`；`GenerateConsoleCtrlEvent` 只能发给进程组 | 处理函数可被调用的时机与线程不同；无同构的"给单个进程发 SIGTERM" |
| 标准流 | `pipe`/`dup2` + 文件描述符 | `SECURITY_ATTRIBUTES` 可继承句柄 + `STARTUPINFO` 的 `hStdInput/hStdOutput/hStdError` | 继承是句柄属性，需显式设置可继承；父进程读完后须关闭自己那一端，否则读端不会见 EOF |
| 句柄继承与关闭 | fd 默认继承（取决于 `FD_CLOEXEC`/`O_CLOEXEC`） | 句柄默认不可继承（取决于安全描述符）；`bInheritHandles` 影响整批 | 机械照搬会造成句柄泄漏到子进程或子进程拿不到流 |
| 自身身份 | 真实/有效 uid/gid（`getuid`/`geteuid`/`setuid`/`seteuid`） | 访问令牌 + 特权（`OpenProcessToken`/`AdjustTokenPrivileges`/`GetTokenInformation`） | 不是同一模型：uid 决定"是谁"，特权决定"额外能做什么"；Windows 上"不以管理员身份运行"与"未启用某特权"是两件事 |
| 提权/降权 | `seteuid` 可在真实/有效 id 间切换；降权后通常不可逆（除非有 `seteuid` 回切能力） | 提权靠令牌中的特权是否需要启用、是否高完整性；`ImpersonateLoggedOnUser` 是线程级模拟 | 语义与作用域都不同（进程级 vs 线程级）；不要把 `setuid(0)` 直接映射成"启用 SeDebugPrivilege" |
| 身份查询 | `getuid`/`geteuid`/`getgid` | 令牌的 user SID 与组 SID、TokenElevation/TokenElevationType | 返回结构与比较方式不同；SID 比较不能用字符串相等 |
| 权限常量 | `uid` 数值 | 特权名字符串（`SeDebugPrivilege` 等）+ `LUID` | 须用 `LookupPrivilegeValue`/`LookupPrivilegeName` 转换，不能硬编码数值 |
| 错误获取 | `errno` + `strerror` | `GetLastError()`（Win32）、`_doserrno`/`errno`（CRT）、`LONG`（注册表式 API） | 同一程序里 CRT 与 Win32 错误来源并存；一个 API 失败后读另一个来源会读到过期值 |
| 挂起/恢复 | `SIGSTOP`/`SIGCONT` 或 `ptrace` | `SuspendThread`/`NtSuspendProcess`（非文档化常规接口） | 无同构的进程级挂起；远程线程挂起与目标工具的可用性须单独评估 |
| 进程信息查询 | `/proc`、`sysctl`、`getpid`/`getppid` | 工具帮助 API（`CreateToolhelp32Snapshot`/`Process32First` 等）、`GetCurrentProcessId` | 遍历 API 的成功/失败与快照一致性不同；`/proc` 无等价物 |
| 特权升降的失败时机 | `setuid` 失败返回 -1 并设 `errno`，调用点即失败 | 令牌操作可能"成功但特权未生效" | 必须读回校验（如 `GetTokenInformation`/权限检查），不能只看返回值 |

## 方向不对称的陷阱

- **POSIX → Windows**：fork 的内存副本/双返回与 exec 的自身替换义务先按上表核可表达性；不能通过整体改写、创建子进程或新增 exit 自动宣称等价，无法保持则记缺口/明确允许差异。kill 的进程组语义另核作业对象；错误来源按实际 CRT/Win32 API 区分 errno 与 GetLastError，不全局替换；setuid/seteuid 的降权不可用令牌机械替代。
- **Windows → POSIX**：`CreateProcess` 的"命令行单字符串"在 POSIX 侧是 argv 数组，**参数边界必须重新切分**（直接拼串会改变参数语义，也是命令注入面）；`TerminateProcess` 改信号后，目标进程可能捕获信号并继续运行——源的"立即终止"义务可能无法保持，须显式标注；`SECURITY_ATTRIBUTES` 式继承在 POSIX 侧默认继承，**须主动考虑 `O_CLOEXEC`/`FD_CLOEXEC`**，否则子进程会多拿到源程序没有的 fd；Windows 令牌特权在 POSIX 侧无对应，须按实际能力（uid 切换、`capset`）逐项评估并标缺口。
- **提权路径不对称**：Windows 上"以管理员启动"通常由父进程/Shell 决定（`ShellExecute` 的 `runas` 动词、清单文件），不是进程内 API；POSIX 上 `setuid` 位或 sudo 由文件权限与调用方决定。两边都不能靠进程内一次调用改变启动身份。
- **退出码可观察性不对称**：源码若把退出码当"业务状态码"传递，Windows 侧完整、POSIX 侧低 8 位——跨 OS 时源里大于 255 的状态码语义会丢失，属应显式登记的差异。

## 等价不可用（须停标，不得伪造映射）

- Linux 内核接口：`ptrace`（调试/注入范式）、`seccomp`、`prctl` 各种进程属性、`/proc/<pid>/*` 的具体文件语义、`clone` 的命名空间参数。Windows 侧无同名同语义接口，涉及时列为缺口并说明目标平台需要重设计，不写"等价实现"。
- 信号集合：`SIGKILL`/`SIGSTOP` 的不可捕获语义、`SIGCHLD` 回收范式在 Windows 上无对应；`SIGPIPE` 属套接字场景，见 [POSIX ↔ Winsock](../posix-winsock/SKILL.md)。
- 进程优先级的跨平台映射（POSIX nice 值与 Windows 优先级类的可用组合）不是一一对应，须按目标 API 允许的离散取值重新选择并登记差异。
- 平台专有防护（如 Windows 的 PPL/进程缓解策略）没有 POSIX 等价物，不能因为"源有 raise/降低权限的调用"就宣称目标侧可复现同等约束。

## 与其它 Skill 的组合

- 语言方向 Skill：负责 API 语法、类型、错误模型（返回码 vs 异常 vs `(T, error)`）的映射，本 Skill 不重复。
- [进程执行场景](../../scenes/process-execution/SKILL.md)：负责子进程的管道排空、输出捕获上限、超时预算与后代回收策略，本 Skill 只给平台接口差异。
- [并发场景](../../scenes/concurrency/SKILL.md) 与 [POSIX ↔ Windows 线程](../posix-windows-threads/SKILL.md)：源码同时创建线程与进程时共同加载；`fork` 与多线程并存的语义风险须显式记录。
- 涉及文件路径、权限位与目录遍历的部分属 [POSIX ↔ Windows 文件路径](../posix-windows-filesystem/SKILL.md)。
- 冲突时先保留源程序的可观察义务，写出平台差异与缺少的依据，再给有条件的转换；不以相似名称宣称等价。

## 依据

- The Open Group Base Specifications Issue 7 / IEEE Std 1003.1（POSIX）：`fork`、`exec`、`posix_spawn`、`waitpid`、`setuid`、`kill`：创建、替换、等待状态编码、身份切换与信号发送语义。
- Microsoft Learn：`CreateProcessW`、`WaitForSingleObject`、`GetExitCodeProcess`、`TerminateProcess`：创建、命令行、等待与终止语义。
- Microsoft Learn：Job Objects、`TerminateJobObject`：进程树回收边界。
- Microsoft Learn：`OpenProcessToken`、`AdjustTokenPrivileges`、`LookupPrivilegeValueW`、`GetTokenInformation`：令牌、特权启用与身份查询语义。
- Microsoft Learn：`ShellExecuteW` 与 `_popen`：shell 关联与 CRT 管道语义（与 POSIX `system`/`popen` 不同）。
- Microsoft Learn：`SetConsoleCtrlHandler`、`GenerateConsoleCtrlEvent`：控制台信号处理与进程组限制。

以上为语言/平台规则依据，不是特定编译器、SDK 版本或转换结果的验证记录；目标为具体版本时须核对对应文档。本项编译和行为结论须依据精确版本的独立证据。同时遵守根入口和[安全边界](../../../references/framework/safety-boundary.md)。**执行顺序与适用门禁统一按根入口分流**：先检查评估系统可达性，可达走分类、源预检及适用评估；不可达仅冻结、转换、自审和交付报告，不加载或调用分类器、不要求分类产物，不编译运行；见 [AGENTS.md](../../../AGENTS.md) 执行约束 §3。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)；本系统方向 Skill **不替代门禁、不构成执行授权**。
