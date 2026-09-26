---
name: posix-windows-filesystem
description: Identify POSIX-to-Win32 path, current-directory, canonicalization, and narrow-path differences when converting file I/O behavior.
---

# POSIX ↔ Windows 文件路径系统方向（初稿）

适用于确有文件系统行为、且从 POSIX/Linux 转向 Windows 的源码。它聚焦本项目当前遇到的路径与 C 运行库边界，不提供完整文件系统移植保证；转换效果未经样例验证。

## 关键 API 差异

| POSIX 源 API / 语义 | Windows 侧常见 API | 不可直接假定等价 |
|---|---|---|
| `realpath` | `GetFullPathNameA/W` | `realpath` 会解析符号链接并要求路径解析成功；`GetFullPathName` 主要构造绝对路径，不等于文件存在性/最终对象验证，也不自动提供相同的符号链接语义 |
| `getcwd` | `GetCurrentDirectoryA/W` | 返回类型、缓冲区长度单位与错误报告不同；Windows 路径字符/编码还受 A/W 选择影响 |
| `chdir` | `SetCurrentDirectoryA/W` | 都会改变进程当前目录；当前目录是进程共享状态，不应在工作线程中任意更改 |
| `fopen` / `fread` / `fclose` | 同名 C 运行库接口 | 路径编码、窄字符代码页、长路径及 CRT 版本仍可能不同；同名函数不保证 Unicode 路径一致 |

必须先确定目标使用 ANSI (`A`) 还是宽字符 (`W`) API、源码路径编码和目标 CRT。若缺失，标为待确认；不要仅把斜杠替换成反斜杠后宣称等价。

## 路径安全与行为保留

- 记录源代码是检查词法路径、绝对路径还是解析后的最终文件对象；`realpath` 与 `GetFullPathName` 的语义差异可能改变符号链接、相对路径及失败路径结果。
- 用字符串前缀比较目录边界并不自动证明路径位于 docroot 内；还需考虑路径分隔符边界、大小写、卷、UNC、符号链接/reparse point 与竞态。未经授权，不在转换中静默引入或宣称完整修复。
- 对受控静态服务，仅允许 case 私有临时 docroot 与无敏感 fixture；任何动态验证都必须遵守项目隔离规则。
- 错误来源要与 API 对齐：Win32 API 错误码、CRT `errno` 和 POSIX `errno` 不能混用或在后续调用后读取。

## uhttpd 适用提示

源码 POSIX 兼容层以 `realpath()` 实现 `GetFullPathName` 包装；Windows 分支调用 Win32 `GetFullPathName`。`DecodeHttpRequest` 先尝试打开请求路径，再规范化并用 `memcmp` 做 docroot 字符串前缀检查。C01 目标复用 Windows 分支，因此这些源/目标差异必须列为行为待审项；本转换不把该检查描述为完整路径穿越防护。

## 依据

- The Open Group, [`realpath`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/realpath.html)
- Microsoft Learn, [`GetFullPathNameA`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfullpathnamea), [`GetCurrentDirectoryA`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getcurrentdirectorya), [`SetCurrentDirectoryA`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setcurrentdirectorya)
