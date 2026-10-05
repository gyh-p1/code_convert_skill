---
name: posix-windows-filesystem
description: Identify POSIX-to-Win32 path, current-directory, canonicalization, directory-traversal, stat/inode, and BSD-portability differences when converting file I/O behavior.
---

# POSIX ↔ Windows 文件系统系统方向

适用于确有文件系统行为、且从 POSIX/Linux 转向 Windows 的 C→C++ 源码。聚焦路径、当前目录、规范化、目录遍历、stat/inode 计量与 BSD-base 可移植性边界；不提供完整文件系统移植保证。

**真实消费者与证据基础（step-04 多系统批次，2026-09-28）**：本方向已由 4 份真实单文件 POSIX 源坐实——

| 例 | 源 | 目标编译（Controller 真实回传） | 用途 |
|---|---|---|---|
| stest | `dmenu-stest/stest.c` | **PASS**（job `eval-20260928-053745-2a386af5`，目标 build exitCode=0） | `stat`/`lstat`/`access`/`opendir`/`readdir`/`S_IS*` 映射坐实 |
| realpath | `freebsd-realpath/realpath.c` | **PASS**（job `eval-20260928-060834-49b1a302`） | `realpath` 命名冲突 + getopt 语义坐实 |
| pwd | `freebsd-pwd/pwd.c` | **PASS**（job `eval-20260928-064021-653f5ee9`） | `getcwd`/`getenv(PWD)`/`st_dev`+`st_ino` 身份坐实 |
| du | `freebsd-du/du.c` | **源基线 FAILED_COMPILE → 目标跳过**（job `eval-20260928-073929-e89be213`，无目标 build 证据） | 失败类别：FreeBSD-base 表面不可移植 |

**证据口径**：前 3 例目标 C++ 在 Windows VM 真实编译通过（编译级坐实）；`realpath`/`pwd` 的 `behaviorVerdict=mismatched` 仅信息记录，属**按设计的跨 OS 路径文本差异**，本阶段不计功能率、不设 oracle。du 例源侧 C 基线在 plain-glibc Linux 即 `FAILED_COMPILE`（首个硬阻断 `libutil.h` 缺失），据 Controller 双 runner 定序目标侧被跳过，**故 du 相关的目标映射未取得 build 证据，下文 du 条目均为源可移植性预筛与保守重写指引，非已验证编译结论。**

## 1. 关键 API 差异

| POSIX 源 API / 语义 | Windows 侧常见 API | 不可直接假定等价 |
|---|---|---|
| `realpath` | `GetFullPathNameA/W` / `_fullpath` | `realpath` 解析符号链接并要求路径存在；`GetFullPathName` 只构造绝对路径，不验证存在性/最终对象，不提供相同符号链接语义。**另注**：`realpath` 作标识符在 C++ 中会与声明冲突/被库符号遮蔽，转换须重命名本地包装（realpath 例坐实） |
| `getcwd` | `GetCurrentDirectoryA/W` | 返回类型、缓冲区长度单位与错误报告不同；A/W 影响路径字符/编码 |
| `getenv("PWD")` 逻辑路径 | 无直接等价（`GetCurrentDirectory` 返回物理路径） | POSIX `pwd -L` 依赖 shell 维护的 `PWD`；Windows 无同义环境约定，逻辑/物理路径策略须显式决定（pwd 例坐实） |
| `chdir` | `SetCurrentDirectoryA/W` | 均改进程当前目录（进程共享状态，勿在工作线程随意改） |
| `stat`/`lstat` + `S_IS*` | `stat`/`_wstat` 或 `GetFileAttributesEx` + `std::filesystem::status`/`symlink_status` | `lstat`（不跟随）↔ `symlink_status`；`stat`（跟随）↔ `status`。`st_mode` 位与 `S_ISLNK` 在 Windows CRT 上残缺，符号链接/reparse 判定须用 Win32/`std::filesystem`（stest 例坐实） |
| `access(F_OK/R_OK/W_OK/X_OK)` | `_access`/`_waccess`（仅 `00/02/04/06`）或 `std::filesystem::status` + 权限位 | Windows `_access` **无 X_OK 语义**（可执行性不由文件位决定）；X_OK 须保守处理并登记（stest 例坐实） |
| `opendir`/`readdir` | `FindFirstFileA/W`/`FindNextFile` 或 `std::filesystem::directory_iterator` | 遍历返回顺序、`.`/`..` 是否出现、错误报告不同；`d_type` 非可移植，须回退 `stat`（stest 例坐实） |
| `getline` | 无 CRT 等价 | 须自备或用 `std::getline`（stest 例坐实） |
| `fopen`/`fread`/`fclose` | 同名 CRT 接口 | 路径编码、窄字符代码页、长路径、CRT 版本可能不同；同名不保证 Unicode 路径一致 |

必须先确定目标用 ANSI(`A`) 还是宽字符(`W`) API、源路径编码、目标 CRT。缺失则标待确认；不要仅把斜杠换反斜杠就宣称等价。

## 2. 源可移植性预筛：FreeBSD-base 表面（du 例，失败类别，先记预期）

FreeBSD base-system 源常含一批 **glibc 与 MinGW 均缺**的接口。转换前应静态预筛；命中即预记源侧对照基线可能 `FAILED_COMPILE`，并规划目标侧整体重写。**du 例真实证据**：源在 plain-glibc Linux `cc -std=c11 …` 失败于首个硬阻断 `du.c:55:10: fatal error: libutil.h: No such file or directory`；其后尚有多处不可补齐面。命令行特性测试宏（`-D_POSIX_C_SOURCE`/`-D_DEFAULT_SOURCE`/`-D__unused=`）只能暴露 POSIX 符号、中和属性宏，**无法**补齐下列 BSD 专有面：

| BSD 专有面 | 现象 | 目标侧保守处理（未取得 du build 证据） |
|---|---|---|
| `<libutil.h>` `humanize_number`/`expand_number`/`getbsize` | glibc 需 libbsd、MinGW 无 —— **首个硬阻断** | 目标 C++ 内自备单位换算/阈值解析/块大小换算 |
| `signal(SIGINFO, …)` | `SIGINFO` 为 BSD 专有信号，Linux/Windows 均无 | 删除/保守化交互式进度报告，注释登记 |
| `st_flags & UF_NODUMP`（`-n`） | Linux/Windows `struct stat` 无 `st_flags` | `-n` 无等价 → no-op 并登记为已知差异 |
| `st_blocks`（块计量） | Windows `struct stat` 无 `st_blocks` | 以 `st_size`/512 近似或 Win32 分配大小 API；属可观察数值差异 |
| `<fts.h>` `fts_open`/`fts_read`/`fts_set` | Windows 无等价 | 以 `std::filesystem::recursive_directory_iterator` 或 `FindFirstFile`/`FindNextFile` 重写；`FTS_PHYSICAL`/`FTS_LOGICAL`/`FTS_COMFOLLOW`/`FTS_XDEV` 语义自维护 |
| `<sys/queue.h>`/`<fnmatch.h>`/`getopt_long`/`DEV_BSIZE`/`EX_USAGE`/`<err.h>` | glibc/MinGW 可用性混杂 | STL/自备替代；`getopt_long` MinGW 经 libmingwex 可用 |

**定序后果（Controller 已证）**：源侧基线失败即**不再构建目标侧**（`execution.performed=false`、preflight/cleanup SKIPPED、无目标 build 证据、`comparison_not_found`）。此时 syntaxVerdict = **INCONCLUSIVE**（目标未构建，非 PASS、非转换引入 FAIL）。这是**源对 glibc 的可移植性事实**，不改源、不放松命令到失真、不伪造目标通过。

## 3. C→C++ 机械与语义要点（由 4 例坐实）

- **`off_t` 等类型别名冲突**：源里 `typedef long long off_t;` 会与系统 `off_t` 冲突而编译阻断，须改独立别名（如 `using du_off_t = long long;`）。（du 转换自修 round-1 坐实为编译阻断项。）
- **自定义 getopt 状态的声明顺序**：把源里散布的 getopt 状态（如 `optind`/`optpos` 之类自定义副本）上移集中声明，消除 C++ 更严声明顺序下的阻断。（pwd 例坐实：目标 build PASS 后此项成立。）
- **`std::filesystem` 符号链接跟随须显式决策**：`directory_iterator`/`recursive_directory_iterator` 默认不跟随目录符号链接，需要时显式 `directory_options::follow_directory_symlink`；目录尺寸/跟随策略登记为平台差异。
- **`fnmatch` 字符类边角是高风险改写点**：手工替换 `fnmatch` 时，首字符 `]`、范围 `[]-a]` 语义极易过度限制。（du 转换 round-2 残留：修复过度限制了首字符 `]` 的范围语义，因自修预算 ≤2 用尽，如实登记为已接受限制，未强判 NO-REPAIR。）
- **跨 OS 路径文本差异属按设计**：`realpath`/`pwd` 目标 build PASS，但 `behaviorVerdict=mismatched` —— 因盘符/分隔符/大小写等路径文本天然不同，本阶段仅信息记录、不计功能率。转换应在文件顶部登记这类已知差异，勿当缺陷修复或当等价宣称。

## 4. 路径安全与行为保留

- 记录源是检查词法路径、绝对路径还是解析后的最终文件对象；`realpath` 与 `GetFullPathName` 语义差异会改变符号链接、相对路径、失败路径结果。
- 字符串前缀比较不自动证明路径在 docroot 内；还需考虑分隔符边界、大小写、卷、UNC、reparse point 与竞态。未经授权不在转换中静默引入或宣称完整修复。
- 错误来源与 API 对齐：Win32 错误码、CRT `errno`、POSIX `errno` 不能混用或在后续调用后读取。
- 动态验证只在获批隔离 VM、case 私有临时目录、无敏感 fixture 下进行；只读遍历+汇总，不联网/不 exec/不写删。

## 5. uhttpd 适用提示（网络方向遗留，仅路径检查部分相关）

uhttpd 的 POSIX 兼容层以 `realpath()` 包装 `GetFullPathName`；`DecodeHttpRequest` 先开路径再规范化并用 `memcmp` 做 docroot 前缀检查。这些源/目标差异列为行为待审项；本转换不把该检查描述为完整路径穿越防护。

## 6. macOS 作为源或目标 OS 时的路径与位置约定（有限覆盖）

本节是**有限**补充：本仓库当前只有两个真实的 macOS 平台路径消费者（`ruby-to-c/…/chrome_cookies.rb`、`ruby-to-python/…/firefox_creds.rb`，均为凭据/配置路径发现），因此只写有源码依据的位置与路径差异；Keychain、IOKit、launchd、CoreFoundation 等 macOS 专有子系统**仍无 Skill**，遇到按缺口报告。

| 主题 | macOS | Linux | Windows | 转换必须处理的点 |
|---|---|---|---|---|
| 用户主目录 | `/Users/<name>` | `/home/<name>` | `C:\Users\<name>` | 不得把 `~/` 展开成硬编码前缀；`~` 的展开由 shell 或语言库完成，路径拼接要用目标平台的组合 API |
| 应用数据位置 | `~/Library/Application Support/<Vendor>/<App>` | `~/.config/<app>`、`~/.<app>` | `%APPDATA%\<Vendor>\<App>` | 同一应用的三平台默认位置不同，属**可观察行为差异**（源里硬编码 macOS 路径时须显式改写并登记） |
| 应用包结构 | `/Applications/<App>.app/Contents/MacOS/<bin>`（`.app` 是目录） | 无此结构 | `Program Files` 下的普通目录 | 不能把 `.app` 当普通文件；在目标平台须按实际安装布局重写 |
| 密钥/凭据位置 | `~/Library/Keychains/*.keychain-db` | 取决于实现（文件/内核密钥环/桌面密钥环） | 凭据管理器/DPAPI | 路径差异之外还有**存储格式与保护机制**差异，不能只改路径就宣称等价 |
| 大小写敏感性 | 默认卷通常大小写不敏感（可配制为敏感） | 通常敏感 | 不敏感 | 与 Windows 一样，大小写敏感性不能假定；比较路径时保留源语义 |

**边界**：本节只覆盖"位置与路径文本"的可观察差异，覆盖方向为 macOS ↔ Linux 与 macOS ↔ Windows 的对应行；文件 API（`open`/`stat`/`opendir` 等）在 macOS 上大部分与 POSIX 一致，但仍需按目标 SDK 核对（例如 `st_birthtimespec` 等专有字段）。macOS 专有子系统与工具链（`security`、`codesign`、`launchctl`、CoreFoundation）没有项目内证据，**不在此建立映射**。

## 依据

- The Open Group：[`realpath`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/realpath.html)、[`opendir`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/opendir.html)、[`fnmatch`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fnmatch.html)、[`access`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/access.html)
- Microsoft Learn：[`GetFullPathNameA`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfullpathnamea)、[`FindFirstFileA`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-findfirstfilea)、[`_access`](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/access-waccess)、[`GetCurrentDirectoryA`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getcurrentdirectorya)
- cppreference：[`std::filesystem::recursive_directory_iterator`](https://en.cppreference.com/w/cpp/filesystem/recursive_directory_iterator)、[`std::filesystem::directory_options`](https://en.cppreference.com/w/cpp/filesystem/directory_options)
- FreeBSD：[`humanize_number(3)`](https://man.freebsd.org/cgi/man.cgi?humanize_number)、[`fts(3)`](https://man.freebsd.org/cgi/man.cgi?fts)、[`SIGINFO`（signal(3)）](https://man.freebsd.org/cgi/man.cgi?signal)