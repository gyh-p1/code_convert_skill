# C01 · run-01 · 探索输入契约（未冻结基线）

> 用途：记录 C01 文本级探索使用的任务契约草稿。本项目没有独立转换运行时；本次由 Codex 生成静态目标文本，不编译/运行。
> 当前仍为 draft，尚未冻结成正式 No-RAG 基线。
> 状态：exploration draft（case 仍为 candidate；仅允许文本转换/静态审阅；oracle 未冻结；不是正式 No-RAG 基线）。

## 1. 源

- 文件：[`../../../../../sources/uhttpd/uhttpd.c`](../../../../../sources/uhttpd/uhttpd.c)
- 上游：`PJO2/uhttpd`，`uhttpd.c`
- Pinned commit：`59d17b86ec9f2a70ce1f4369b4c148824be55155`
- 许可：GPL-2.0-or-later（随附 `LICENSE`、`UPSTREAM-README.md`）
- 规模：1,317 LF 归一化物理行，≈1,092 LOC。**超过 700 行计划上限**，属用户确认的超限探索候选，不计入 ≤700 行边界验证。
- 快照只读，不得修改。

## 2. 转换画像（文本级探索稿；非冻结基线）

| 参数 | 值 |
|---|---|
| source_lang | c |
| target_lang | cpp |
| direction_id | c->cpp |
| source_os | linux |
| target_os | windows |
| source_arch | x64 |
| target_arch | x64 |
| target_toolchain | MSVC x64，C++17（本次探索假设，未批准/未验证） |
| scene | network-io + file-io + concurrency |
| attack_tactic | none（静态画像未发现支持 ATT&CK tactic/technique 的对抗行为） |
| retrieval / RAG | **off**（文本稿未使用 RAG；尚不是正式基线） |
| task mode | 长单文件（long-file） |

## 3. 按源码画像选定的 Skill（本仓库）

1. [`skills/workflows/long-file-conversion/SKILL.md`](../../../../../../../skills/workflows/long-file-conversion/SKILL.md) —— 长文件地图、分段/合并和覆盖核对。
2. [`skills/directions/c-to-cpp/SKILL.md`](../../../../../../../skills/directions/c-to-cpp/SKILL.md) —— C→C++ 类型/API/行为约束。
3. [`skills/scenes/network-io/SKILL.md`](../../../../../../../skills/scenes/network-io/SKILL.md) —— socket 生命周期、字节流与 HTTP I/O。
4. [`skills/scenes/file-io/SKILL.md`](../../../../../../../skills/scenes/file-io/SKILL.md) —— docroot 文件读取与资源清理。
5. [`skills/scenes/concurrency/SKILL.md`](../../../../../../../skills/scenes/concurrency/SKILL.md) —— 每连接线程、共享状态和清理时序。
6. [`skills/systems/posix-winsock/SKILL.md`](../../../../../../../skills/systems/posix-winsock/SKILL.md) —— socket API；本源已有 Windows 分支，目标稿选择该分支。
7. [`skills/systems/posix-windows-filesystem/SKILL.md`](../../../../../../../skills/systems/posix-windows-filesystem/SKILL.md) —— `realpath`/`GetFullPathName`、工作目录与窄字符路径差异。
8. [`skills/systems/posix-windows-threads/SKILL.md`](../../../../../../../skills/systems/posix-windows-threads/SKILL.md) —— `pthread`/`_beginthreadex` 生命周期差异。
9. [`skills/attack-tactic-index/SKILL.md`](../../../../../../../skills/attack-tactic-index/SKILL.md) —— 仅用于核对 ATT&CK 分类；当前记录 tactic/technique 为 `none`，不按 HTTP/socket 标签推断攻击行为。

以上系统和工作流 Skill 是知识初稿，未由本项目转换验证。完整事实地图、覆盖范围与风险见同目录 [`source-analysis.md`](source-analysis.md)。
## 4. 源侧关键事实（供转换器核对，非替代其自身盘点）

以下从源码静态读出，帮助转换器建立全文件地图，不表示已验证转换正确：

- 源文件自带**双平台可移植层**：`#if defined(_MSC_VER)||defined(__POCC__)`（Winsock/`_beginthreadex`/`Sleep`）与 `#ifdef UNIX`（BSD socket/`pthread`/`sleep`）。Linux→Windows 方向即「以 UNIX 分支为源行为，产出 Windows 目标」。
- HTTP 响应头格式为**仅 `\n` 换行**（非 `\r\n`），`Server: uhttpd-1.7`，`Connection: close`。oracle 若做字节比较必须保留此格式。见 `szHTTPDataFmt`、`szHTMLErrFmt`。
- 请求处理：仅 `GET`/`HEAD`；`GET /` 取 `DEFAULT_HTMLFILE`(index.html)；扩展名经 `sHtmlTypes[]` 大小写不敏感解析 content-type；错误类别 400/403/404/405/415/500。`HEAD` 只发头不发 body。
- 目录边界检查：`GetFullPathName` 后与当前目录前缀 `memcmp` 比较（Windows 为反斜杠路径）；这不是完整路径穿越防护证明。
- 资源生命周期：每连接一线程，`S_ThreadData` 持 socket/buf/FILE*；`HttpTransferThread` 的 `cleanup:` 分支按 socket→buf→hFile 顺序释放；`ManageTerminatedThreads` 回收退出线程并从链表摘除。
- 已知平台语义差异（转换器须显式处理并在交付说明标注，**不要静默"修好"**）：
  - 源 Windows 分支对 socket 错误用 `GetLastError()`+`strerror(errno)` 取文本，在 Windows 上不准确（应为 `WSAGetLastError`）。可能影响 stderr；oracle 草案拟排除易变错误细节，尚未冻结。
  - GET 发送循环对 `send` 返回值不校验部分发送（`__DUMMY(bytes_sent)`）；Winsock `send` 可能返回小于请求长度。保留源语义并标注。
  - C→C++ 严格性：`realloc` 结果赋给 `char*`、`getsockopt` 的 `optlen` 指针类型、`ERROR` 枚举与 windows.h 宏冲突（源用 `#undef ERROR` 规避，枚举定义须在包含 windows.h 之前）等，需最小改动使其作为 C++ 合法编译。

## 5. 目标产物落点

- 已生成 `./target.cpp`，是 C01 文本级探索稿；本次输出不表示语法/行为通过。
- 交付说明：`./result.md`；源码画像：`./source-analysis.md`；实际移交清单：`./evaluator_manifest.json`。`evaluator_manifest.example.json` 模板位于仓库 `references/`。

## 6. 行为 oracle 与执行边界

- oracle 草案见 [case.md](../../../case.md) 第「行为 oracle 草案」节；**尚未冻结**。冻结前不得据其判定通过。
- 执行边界（case.md）：仅一次性隔离环境；`-i 127.0.0.1 -p <隔离高位端口> -d <case 临时空 docroot>`；结束销毁临时目录。本仓库与本模型**不执行**编译/运行，交由远程 VM 控制器（见 `README.md` 与 `evaluator_manifest.json`）。

## 7. 变更记录

- 2026-09-25：按用户要求生成文本级探索稿与静态画像；source snapshot 未改。oracle 仍为草案，run-01 尚未冻结为正式 No-RAG 基线，编译/执行仍未获批。
