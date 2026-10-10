---
name: posix-windows-filesystem
description: Identify POSIX-to-Win32 path, current-directory, canonicalization, directory-traversal, stat/inode, and BSD-portability differences when converting file I/O behavior.
---

# POSIX ↔ Windows 文件系统系统方向

适用于确有文件系统行为、且从 POSIX/Linux 转向 Windows 的 C→C++ 源码。聚焦路径、当前目录、规范化、目录遍历、stat/inode 计量与 BSD-base 可移植性边界；不提供完整文件系统移植保证。

本页是可复用的路径与文件系统映射约束。每次转换须以该任务的源/目标版本、目标工具链诊断和独立行为 oracle 判定结果；历史个例不构成其他任务的编译或等价结论。

## 1. 关键 API 差异

| POSIX 源 API / 语义 | Windows 侧常见 API | 不可直接假定等价 |
|---|---|---|
| `realpath` | `GetFullPathNameA/W` / `_fullpath` | `realpath` 解析符号链接并要求路径存在；`GetFullPathName` 只构造绝对路径，不验证存在性/最终对象，不提供相同符号链接语义。若本地包装名与目标头文件声明冲突，按实际诊断改内部名；外部 ABI 名不能静默改。 |
| `getcwd` | `GetCurrentDirectoryA/W` | 返回类型、缓冲区长度单位与错误报告不同；A/W 影响路径字符/编码 |
| `getenv("PWD")` 逻辑路径 | 无直接等价 | POSIX 逻辑路径可能依赖 shell 维护的 `PWD`；Windows 当前目录 API 不承诺相同约定，逻辑/物理路径策略须显式决定。 |
| `chdir` | `SetCurrentDirectoryA/W` | 均改进程当前目录（进程共享状态，勿在工作线程随意改） |
| `stat`/`lstat` + `S_IS*` | `stat`/`_wstat` 或 `GetFileAttributesEx` + `std::filesystem::status`/`symlink_status` | `lstat`（不跟随）↔ `symlink_status`；`stat`（跟随）↔ `status`。目标 CRT 对模式位的支持须按实际版本核对，符号链接/reparse 判定需单独检查。 |
| `access(F_OK/R_OK/W_OK/X_OK)` | `_access`/`_waccess`（仅 `00/02/04/06`）或 `std::filesystem::status` + 权限位 | Windows `_access` **无 X_OK 语义**（可执行性不由文件位决定）；X_OK 须按任务契约单独处理并登记差异。 |
| `opendir`/`readdir` | `FindFirstFileA/W`/`FindNextFile` 或 `std::filesystem::directory_iterator` | 遍历返回顺序、`.`/`..` 是否出现、错误报告不同；`d_type` 非可移植，必要时另查文件状态。 |
| `getline` | 无直接同义 Win32 CRT 接口 | 须按换行、缓冲增长和错误语义选目标实现；`std::getline` 只在契约吻合时使用。 |
| `fopen`/`fread`/`fclose` | 同名 CRT 接口 | 路径编码、窄字符代码页、长路径、CRT 版本可能不同；同名不保证 Unicode 路径一致 |

必须先确定目标用 ANSI(`A`) 还是宽字符(`W`) API、源路径编码、目标 CRT。缺失则标待确认；不要仅把斜杠换反斜杠就宣称等价。

## 2. 源可移植性预筛：BSD 专有接口

FreeBSD 等平台的源码可能使用目标工具链缺少的头、类型或符号。冻结时逐项检查实际包含链、依赖包、编译分支与目标 SDK；静态预筛只形成待验证清单，只有真实构建失败才能记 build FAIL。特性测试宏不能代替未安装的头或库。

| 接口类别 | 须核对的语义 |
|---|---|
| `libutil.h` 的 `humanize_number`/`expand_number`/`getbsize` | 单位、舍入、缓冲容量和错误返回；目标依赖是否提供同义实现 |
| `SIGINFO`、`st_flags`/`UF_NODUMP` | 信号与跳过规则是否属于可观察行为；不能默认删除或改为 no-op |
| `st_blocks` | 分配块计量与逻辑字节大小不同，不能直接用 `st_size/512` 宣称等价 |
| `fts_*`、`fnmatch`、`getopt_long` | 遍历顺序、跟随链接、文件系统边界、模式边角与参数解析；按目标 SDK 核对可用性 |

源基线失败时应保存源诊断；若 Controller 因此跳过目标 build，目标编译结论为 `UNVERIFIED`。若目标 build 独立产生，仍按该目标版本和命令判读，不能从源侧失败推定目标失败或通过。

## 3. C→C++ 机械与语义要点

- 自定义 `off_t` 等别名与目标头文件冲突时，先核对是否内部符号；内部名可改，外部 ABI 名不能静默变更。
- `std::filesystem` 迭代默认的符号链接跟随、错误及目录顺序与源遍历 API 未必相同，须按源路径策略映射。
- 手工替换 `fnmatch` 时核对字符类、首字符 `]`、转义和范围语义；无独立 oracle 不宣称匹配。
- 跨 OS 路径文本可能因盘符、分隔符或大小写而不同；是否允许由冻结行为契约决定，不能一概标为“按设计匹配”。

### L2-FS-01 与目标平台 CRT/SDK 同名符号必须消歧

**触发条件**：源码在 POSIX 侧定义了与目标平台头文件/CRT **同名**的函数、类型或宏（自写 `realpath` shim、`typedef ... off_t`、自定义 `getopt` 状态），或把 POSIX 专有常量直接搬进目标代码。


**义务**：

1. **同名 shim 必须改名**：`static char * realpath(...)` 这类自写实现与平台声明冲突，GCC 会报 `static declaration of 'realpath' follows non-static declaration`。**不得依赖“当前头文件恰好没声明它”**——该假设随 SDK/CRT 版本变化。改用独立内部名（如 `poc_realpath`）。
2. **类型别名不得与平台类型重定义**：`typedef long long off_t;` 在 MinGW/UCRT64 下常与 `<sys/stat.h>` 已定义的 `off_t`（通常为 `long`）冲突而编译阻断。须改用独立别名（如 `using du_off_t = long long;`），而不是假定平台没有该 typedef。
3. **位宽常量必须按目标架构分别取值**：`INVALID_HANDLE_VALUE` 在 32 位 Windows 上是 `0xFFFFFFFF`、64 位上是 `0xFFFFFFFFFFFFFFFF`。把它硬编码成单一宽度会在另一架构上判错失效。**必须**使用平台宏或按目标架构分支，不得硬编码。
4. **POSIX 专有常量不可直接搬运**：`st_flags`/`UF_NODUMP`、`DEV_BSIZE`、`SIGINFO`、`EX_USAGE` 等在 Windows 侧可能不存在或无同义语义，须按本文件 §2 核对其行为义务与目标替代方案；未经契约允许不删除为 no-op。

**错误机械替换反例**：

```cpp
// 错误一：自写 shim 沿用平台名
static char * realpath(const char *path, char *resolved) { /* ... */ }
// → error: static declaration of 'realpath' follows non-static declaration

// 错误二：重定义平台已有的类型
typedef long long off_t;        // MinGW/UCRT64 的 <sys/stat.h> 已定义 off_t(long)

// 错误三：把句柄哨兵值硬编码成 64 位宽度
#define INVALID_HANDLE_VALUE_LOCAL 0xFFFFFFFFFFFFFFFFULL   // 32 位目标上应为 0xFFFFFFFF

// 正确：改名、独立别名、用平台宏
static char * poc_realpath(const char *path, char *resolved) { /* ... */ }
using du_off_t = long long;
if (h == INVALID_HANDLE_VALUE) { /* 使用平台宏 */ }
```

**不适用条件**：源码的符号名与目标平台**不冲突**（如自写的 `poc_*` 前缀函数、无同名 typedef）时，不需要改名；位宽常量若源码已通过平台宏获取，也不存在硬编码问题。

**信息不足时的处理**：无法确认目标 CRT/SDK 是否已声明某符号或类型时，标为“符号/类型冲突待按目标 SDK 核对”，并**默认改名以规避**（改名不改变行为），而不是假定不冲突。

**官方依据**：[Microsoft `INVALID_HANDLE_VALUE`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)、[`_access`](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/access-waccess)；[cppreference `off_t`](https://en.cppreference.com/w/cpp/types/off_t)；[The Open Group `realpath`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/realpath.html)。


### L2-FS-02 替代物语义被削弱时必须列为已知差异

**触发条件**：目标平台没有与源 API 等价的接口，必须选用**替代物**（`realpath` → `_fullpath`、`fts` → `recursive_directory_iterator`、`humanize_number` → 自备换算）。


**义务**：

1. **先核实目标 SDK 是否真存在该 API**，再决定是否需要替代物。**不得**凭名字相似假定存在（如假定某重载/属性存在而实际不存在）。
2. **替代物不得默认等价**：选定时必须逐项列出**语义被削弱的方面**并登记为已知差异。例如 `_fullpath` 相对 `realpath`：**不解析符号链接**、分隔符形式变化、受 `_MAX_PATH`（260）长度上限约束。
3. **削弱项要么补齐、要么登记**：能在目标侧补齐的（如自行解析符号链接）补齐；不能补齐的必须写入交付说明的已知差异清单，并评估下游影响。
4. **不得用“桩函数”冒充等价**：返回固定值或空实现的桩不构成替代物，属未映射项。

**错误机械替换反例**：

```cpp
// 错误：直接假定 _fullpath 等价于 realpath，未登记任何削弱项
char buf[_MAX_PATH];
_fullpath(buf, path, sizeof buf);      // 不解析符号链接、不校验存在性、260 上限
// 交付说明却写“已映射为 realpath 等价实现” → 虚假等价

// 正确：逐项登记差异，并在需要符号链接语义时显式补齐
// 已知差异：(1) 不解析符号链接 (2) 分隔符形式不同 (3) _MAX_PATH=260 长度上限
char resolved[PATH_MAX];
if (GetFinalPathNameByHandleA(h, resolved, sizeof resolved, 0) == 0) { /* 需要链接解析时 */ }
```

**不适用条件**：源 API 与目标 API **确实等价**（同一标准、同一语义，如 `htons`/`htonl` 在 Winsock 上可用）时，不属替代物，无需登记削弱项；但仍应核对目标 SDK 确实提供该符号。

**信息不足时的处理**：无法确认替代物是否削弱的方面时，标为“替代物语义待按目标 SDK 核对”，并把它列为 oracle 观察点；**不得**默认等价。

**官方依据**：[Microsoft `_fullpath`](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/fullpath-wfullpath)、[`GetFinalPathNameByHandle`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfinalpathnamebyhandlea)；[The Open Group `realpath`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/realpath.html)；[cppreference `recursive_directory_iterator`](https://en.cppreference.com/w/cpp/filesystem/recursive_directory_iterator)、[`directory_options`](https://en.cppreference.com/w/cpp/filesystem/directory_options)；[FreeBSD `fts(3)`](https://man.freebsd.org/cgi/man.cgi?fts)。


## 4. 路径安全与行为保留
- 记录源是检查词法路径、绝对路径还是解析后的最终文件对象；`realpath` 与 `GetFullPathName` 语义差异会改变符号链接、相对路径、失败路径结果。
- 字符串前缀比较不自动证明路径在 docroot 内；还需考虑分隔符边界、大小写、卷、UNC、reparse point 与竞态。未经授权不在转换中静默引入或宣称完整修复。
- 错误来源与 API 对齐：Win32 错误码、CRT `errno`、POSIX `errno` 不能混用或在后续调用后读取。
- 动态验证只在获批隔离 VM、case 私有临时目录、无敏感 fixture 下进行；只读遍历+汇总，不联网/不 exec/不写删。

## 5. macOS 作为源或目标 OS 时的路径与位置约定（有限覆盖）

本节只写路径与位置差异；具体应用的路径须以该次任务源码和目标系统配置核对。Keychain、IOKit、launchd、CoreFoundation 等 macOS 专有子系统**仍无 Skill**，遇到按缺口报告。

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

以上为语言/平台规则依据，不是特定编译器、SDK 或转换结果的验证记录；目标为具体版本/文件系统时须核对对应文档。**路径与文件系统的行为结论须由获批隔离环境中匹配的驱动经第三方平台实际运行后回填**；`READY`/快照不证明隔离，也不证明行为等价。

**执行顺序受根入口三道硬门禁约束**（分类 `ALLOWED` → 源侧构建预检 → 评估就绪核对），见 [AGENTS.md](../../../AGENTS.md) 执行约束 §3。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)；本系统方向 Skill **不替代门禁、不构成执行授权**。
