---
name: file-io
description: Use alongside a matching conversion direction when source code creates, reads, writes, renames, or deletes files and the translation must preserve open-mode intent, exact bytes, atomicity, durability, locking, and error semantics. Cross-OS file API and path differences are large; this is not an independent language direction.
---

# 文件 I/O 场景：转换语义

本场景只在源码确有文件系统操作时与方向 Skill **共同阅读**。它讲转换时必须保留的文件可观察行为，不按文件名或扩展名推断用途。先确认源/目标 OS、内容是文本还是二进制、是否要求原子性/持久化、并发访问模型；未知时保留不确定性。路径穿越/规范化等安全语义见 [网络安全行为专题](../network-io/references/security-behavior.md)，其中的路径规则同样适用于本地文件路径。

## 转换时保留的决策边界

| 源码依赖 | 应保留或确认 | 常见误改 |
|---|---|---|
| 打开模式意图 | 创建/独占(`O_CREAT`+`O_EXCL`)、截断、追加、只读的语义与失败条件 | 把独占创建换成普通创建，悄悄允许覆盖；截断与追加混用 |
| 字节精确读写 | 实际读/写字节数、短读/部分写、EOF 与错误区分、二进制内容不被改写 | 假设一次 read 读满；文本模式 CRLF/EOF 翻译损坏二进制(见下) |
| 原子性 | 写临时文件 + `rename` 替换、`O_APPEND` 原子追加等模式 | 拆成非原子的写+移动；Windows 上 rename 覆盖已存在目标会失败 |
| 持久化 | 数据/目录项落盘时机(`fsync`/`fdatasync` vs `FlushFileBuffers`) | 删除 flush/sync 调用，改变崩溃后可见性 |
| 并发/锁 | 共享/独占访问、建议锁(`flock`/`fcntl`) vs Windows 强制共享模式 | 假设两平台锁语义相同；忽略打开态文件的删除/重命名差异 |
| 错误与清理 | 错误码分类、失败路径、句柄/描述符关闭顺序 | `errno` 与 `GetLastError` 混用；丢失部分成功状态 |

## 跨 OS 关键差异（高频陷阱）

- **文本/二进制模式**：Windows C 运行时以文本模式(`"r"`/`"w"`)打开会做 CRLF↔LF 翻译并把 Ctrl-Z 视作 EOF；POSIX 无此翻译。内容为二进制或需字节精确时，转 Windows 必须用二进制模式(`"rb"`/`"wb"`、`_O_BINARY`)，否则静默损坏。
- **rename 覆盖**：POSIX `rename` 原子替换已存在目标；Windows `MoveFile` 目标存在会失败，需 `MoveFileEx(MOVEFILE_REPLACE_EXISTING)` 或 `ReplaceFile`。写临时文件再替换的原子性依赖此差异。
- **打开态文件的删除/重命名**：POSIX 可 `unlink` 已打开文件；Windows 默认共享模式下常被拒绝。转换涉及"边用边删/换"时须显式处理共享模式。
- **权限模型**：POSIX 模式位(`chmod`)与 Windows ACL 不是 1:1；不要把 `0644` 之类直接等同某个 Windows 权限。
- **路径语义**：分隔符、大小写、保留名、长度上限——见 [安全行为专题](../network-io/references/security-behavior.md)，本地文件路径同样适用。
- 目前**没有专门的 POSIX↔Win32 文件系统方向 Skill**：以上是场景层必须提示的行为差异，更完整的文件 API 逐项映射属系统方向，尚是缺口，须按缺口报告、不臆造等价。

## 与方向 Skill 的组合

方向 Skill 负责语言/API 语法映射，本场景补充文件可观察语义与不可丢失条件。冲突时先保留源程序的模式意图、原子性与错误路径，指出平台差异与缺少的依据，再给有条件的转换。不运行来源不明样本、不触发未声明的文件副作用；本文件不证明转换行为已验证。

## 依据

- [POSIX `open`](https://pubs.opengroup.org/onlinepubs/9699919799/functions/open.html)、[`rename`](https://pubs.opengroup.org/onlinepubs/9699919799/functions/rename.html)、[`fsync`](https://pubs.opengroup.org/onlinepubs/9699919799/functions/fsync.html)：打开模式、原子替换、落盘语义。
- [Microsoft `CreateFileA`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)、[`MoveFileExA`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexa)、[`LockFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfile)、[`FlushFileBuffers`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers)：共享模式、替换、锁与落盘。
- [Microsoft C 运行时 `fopen`（文本/二进制模式）](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/fopen-wfopen)：CRLF/EOF 翻译差异。

以上为语言/平台规则依据，不是特定编译器、SDK 或转换结果的验证记录；目标为具体版本/文件系统时须核对对应文档。同时遵守根入口和 [安全边界](../../../references/safety-boundary.md)。
