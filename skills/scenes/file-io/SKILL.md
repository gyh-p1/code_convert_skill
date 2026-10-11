---
name: file-io
description: Use alongside a matching conversion direction when source code creates, reads, writes, renames, or deletes files and the translation must preserve open-mode intent, exact bytes, atomicity, durability, locking, and error semantics. Cross-OS file API and path differences are large; this is not an independent language direction.
---

# 文件 I/O 场景：转换语义

本场景只在源码确有文件系统操作时与方向 Skill 共同阅读，维护文件可观察行为，不按文件名/扩展名推断用途。先确认 OS、文本/二进制、原子性/持久化和并发模型；未知标未知。路径穿越/规范化见[跨场景安全行为](../../references/security-behavior.md)。

## 转换时保留的决策边界

| 源码依赖 | 应保留或确认 | 常见误改 |
|---|---|---|
| 打开模式意图 | 创建/独占(`O_CREAT`+`O_EXCL`)、截断、追加、只读的语义与失败条件 | 把独占创建换成普通创建，悄悄允许覆盖；截断与追加混用 |
| 字节精确读写 | 实际读/写字节数、短读/部分写、EOF 与错误区分、二进制内容不被改写 | 假设一次 read 读满；文本模式 CRLF/EOF 翻译损坏二进制(见下) |
| 原子性 | 写临时文件 + `rename` 替换、`O_APPEND` 原子追加等模式 | 拆成非原子的写+移动；Windows 上 rename 覆盖已存在目标会失败 |
| 持久化 | 数据/目录项落盘时机(`fsync`/`fdatasync` vs `FlushFileBuffers`) | 删除 flush/sync 调用，改变崩溃后可见性 |
| 并发/锁 | 共享/独占访问、建议锁(`flock`/`fcntl`) vs Windows 强制共享模式 | 假设两平台锁语义相同；忽略打开态文件的删除/重命名差异 |
| 错误与清理 | 错误码分类、失败路径、句柄/描述符关闭顺序 | `errno` 与 `GetLastError` 混用；丢失部分成功状态 |

### L2-FILE-01 句柄/fd 的所有权与关闭条件必须逐条对应

**触发条件**：源码创建、传递或关闭文件句柄/描述符，尤其是关闭条件带判定的形态（`if (fd >= 0) close(fd)`、`CloseHandle(h) if h != INVALID_HANDLE_VALUE`），或把 fd 移交给子进程。


**义务**：

1. **关闭条件逐条对应**：源中“满足条件才关闭”的判定在目标必须保留同一条件集合。把 `h != 0 && h != INVALID_HANDLE_VALUE` 简化成 `h != 0` 会在哨兵值上误关；反向收紧会在合法句柄上泄漏。
2. **所有权移交要显式**：把 fd 交给子进程（`ForkExec` 的 `Files`、`posix_spawn` 的 file actions、`CreateProcess` 的句柄继承）后，**父进程是否仍负责关闭**必须按源语义确定；不得默认“创建者关闭”。
3. **关闭后立即失效**：目标语言若把关闭做成幂等，不得因此丢弃源里“重复关闭报错”或“关闭后再用即失败”的可观察行为；反之亦然。
4. **清理失败不得静默忽略**：关闭/删除/刷盘的失败在源里若会传播（返回非零、抛异常、写诊断），目标必须保留该传播路径；这与[并发场景](../concurrency/SKILL.md)的终止协议一致。

**错误机械替换反例**：

```text
源：if (h != 0 && h != INVALID_HANDLE_VALUE) CloseHandle(h);
目标（错误）：h.close() if h != 0          # 哨兵值上误关，或合法句柄上漏关
目标（错误之二）：把父进程的“关闭责任”一起移交给子进程，
                 导致父进程关闭已被子进程持有的 fd 编号（可能命中新打开的文件）。
```

**不适用条件**：源使用语言级确定性释放且所有权本就唯一（Python `with open(...)`、C# `using`、Ruby 块式 `File.open`）时，不需要手工所有权登记；但仍须核对 fd 移交场景。

**信息不足时的处理**：关闭条件或所有权链不清晰时，标为“关闭条件与所有权移交点待确认”，不得默认“谁创建谁关闭”。

**官方依据**：POSIX `close`、`posix_spawn` file actions；Microsoft `CloseHandle`、`CreateProcessW`（句柄继承）；Go `syscall.ForkExec`。


### L2-FILE-02 单层目录与递归建父目录不是同一操作

1. **触发/前提**：源码创建目录；冻结 API、OS、初始父目录存在性、权限及失败处理。判断依据是父目录是否存在，不是路径有几层。
2. **应保留行为**：POSIX mkdir 创建指定目录，缺父目录可失败；.NET Directory.CreateDirectory 会创建所需父目录，且已有目录可返回成功。失败条件、权限、已创建的中间目录与后续执行均可能可观察。
3. **映射条件**：源要求递归时目标明确保持递归；源只建末级时不能无条件选递归 API。若任务只在父目录已存在的冻结环境观察，仅据该前提说明候选映射范围，不宣称所有输入等价；缺等价 API 时明确差异，不用额外探测掩盖竞态与错误差异。
4. **反例**：父目录缺失时，源失败，目标自动建完整路径后成功；为匹配错误加临时父目录，改变冻结初始状态；忽略源 mkdir 返回错误而目标异常提前终止。
5. **未知处理**：初始目录、错误路径或权限未知时保持待确认；不能把观察准备问题归为转换代码失败，不在本机创建目录来验证样本行为。
6. **官方依据**：POSIX mkdir、Directory.CreateDirectory（.NET 8）。

## 跨 OS 关键差异（高频陷阱）

- **文本/二进制模式**：Windows C 运行时以文本模式(`"r"`/`"w"`)打开会做 CRLF↔LF 翻译并把 Ctrl-Z 视作 EOF；POSIX 无此翻译。内容为二进制或需字节精确时，转 Windows 必须用二进制模式(`"rb"`/`"wb"`、`_O_BINARY`)，否则静默损坏。
- **rename 覆盖**：POSIX `rename` 原子替换已存在目标；Windows `MoveFile` 目标存在会失败，需 `MoveFileEx(MOVEFILE_REPLACE_EXISTING)` 或 `ReplaceFile`。写临时文件再替换的原子性依赖此差异。
- **打开态文件的删除/重命名**：POSIX 可 `unlink` 已打开文件；Windows 默认共享模式下常被拒绝。转换涉及"边用边删/换"时须显式处理共享模式。
- **权限模型**：POSIX 模式位(`chmod`)与 Windows ACL 不是 1:1；不要把 `0644` 之类直接等同某个 Windows 权限。
- **路径语义**：分隔符、大小写、保留名、长度上限见[跨场景安全行为](../../references/security-behavior.md)。
- 源码确有 POSIX→Windows 文件系统迁移时，共同阅读 [POSIX→Windows 文件系统方向](../../systems/posix-windows-filesystem/SKILL.md)。该文件只在其列明的接口、前提与不可映射边界内适用，不代表任意双向迁移或行为已验收；仍须冻结具体工具链、API、文件系统及任务证据。未覆盖接口按缺口报告，不臆造等价。

## 归档内容与清单校验

源码递归收集文件并生成 ZIP、归档或 manifest 时，仅比较条目数量不足以保持可观察行为：

- 逐项回读归档内容，核对条目名称、大小和内容哈希；读取到 EOF 与 CRC/解压错误必须区分。
- 若源码生成 manifest，manifest 项与归档项要按同一排序/命名约定对应；重名、缺失、额外项应作为失败或按源码既有策略处理。
- 写入/关闭归档的错误要传播到任务结果；临时目录和部分写入归档的清理失败单独记录。
- 压缩包字节比较可能受时间戳、压缩实现和元数据影响；除非源码明确要求字节级归档同一，否则用内容 oracle 判断。
- 符号链接、路径分隔符、大小写碰撞和路径穿越属于独立观察项，不能由“条目数量相同”推断等价。

## 与方向 Skill 的组合

方向 Skill 负责语言/API 语法映射，本场景补充文件可观察语义与不可丢失条件。冲突时先保留源程序的模式意图、原子性与错误路径，指出平台差异与缺少的依据，再给有条件的转换。不运行来源不明样本、不触发未声明的文件副作用；本文件不证明转换行为已验证。

## 依据

- POSIX `open`、`rename`、`fsync`：打开模式、原子替换、落盘语义。
- Microsoft `CreateFileA`、`MoveFileExA`、`LockFile`、`FlushFileBuffers`：共享模式、替换、锁与落盘。
- Microsoft C 运行时 `fopen`（文本/二进制模式）：CRLF/EOF 翻译差异。

以上为语言/平台规则依据，不是特定编译器、SDK 或转换结果的验证记录；目标为具体版本/文件系统时须核对对应文档。同时遵守根入口和 [安全边界](../../../references/framework/safety-boundary.md)。**执行顺序受根入口三道硬门禁约束**（分类 `ALLOWED` → 源侧预检（构建 + 适用运行基线）→ 评估就绪核对），见 [AGENTS.md](../../../AGENTS.md) 执行约束 §3。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)；本场景 Skill **不替代门禁、不构成执行授权**。
