# 更正追加：BSD userland 源码在 **macOS** runner 上**可构建**（源自 D2-151，2026-10-11）

> 本文件**追加**于 [`pattern-note-bsd-userland.md`](pattern-note-bsd-userland.md)，不改写其历史判定。

## 事实

D2-151（`c-to-cpp`，`rm.c`，510 行）是 **BSD/FreeBSD userland** 源码：`#include <sys/cdefs.h>`、`<fts.h>`、`<err.h>`、`<sysexits.h>`，并使用 `SIGINFO`、`st_flags`/`UF_APPEND`/`SF_APPEND`、`lchflags`、`undelete`、`S_ISWHT`、`FTS_WHITEOUT`、`strmode`、`fflagstostr`、`user_from_uid`、`group_from_gid`、`__unused`。

按"判定只由编译器诊断定案、不得凭印象"的纪律，本项把候选 `sourceOs` 直接定为 **macos**（唯一 BSD 血统的已登记系统）并实测源侧预检：

| job | runner | 构建命令 | 结果 |
|---|---|---|---|
| `eval-20261010-155343-a0e19246` | `macos-vm-agent-x64` | `clang -std=gnu11 rm.c -o program` | **`build.status=completed`、`exitCode=0`**；源执行 `completed/0`，stdout `keep.txt\nsecond.txt\n` |

⇒ **该源码在 macOS 上可构建、可运行**，并随后取得双侧行为证据（job-01 `behaviorVerdict=matched`，`output` 与 `filesystem` 两维度 diffs=0）。

## 与既有判定的关系（不冲突，是**取证范围不同**）

既有 BSD 组判 `SOURCE_NOT_BUILDABLE` 的项（D2-027 `pwd.c`、D2-028 `realpath.c`、D2-162 `uname.c`、D2-163 `wc.c`、D2-164 `ln.c`、D2-165 `tr.c`、D2-166 `uniq.c`）**只实测了 windows 与 linux 两个候选**（见其 frozen-inputs 的"实验 A/B/C"）。`__dead2`／Capsicum／libxo／sysctl 在 **glibc / MinGW** 上确实缺失——那部分结论**仍然成立**；但**"已登记系统都没有"这一外推没有覆盖 macOS**，而 macOS 是 BSD 血统、提供 `sys/cdefs.h`（含 `__dead2`）、`libutil.h`、`fts.h`、`st_flags` 等。

> 结论：**"该接口在已登记系统上不存在"这一类断言，必须对 windows/linux/macos 至少给出实测依据**；只用 windows+linux 两个候选就外推到"所有已登记系统"属超出证据范围。

## 后续处置

1. **不改写**历史项判定与原始证据；本文件只作追加更正。
2. 后续遇到 BSD/FreeBSD userland 的 C 源码，**candidate 集合必须包含 macOS**，按 `sourceOsBasis` 记录依据，并实测后由编译器诊断定案。
3. 既有 `SOURCE_NOT_BUILDABLE` 项若需复核，属**新条件复用**（同一源、换候选 OS），应另记 job、保留累计预算与原结论——但这是**可选的复核**，不作为本轮强制重跑项（用户口径：优先推进未触及项）。
4. 对应的**构建契约**：BSD/POSIX 声明在严格方言下被隐藏，源侧用 `-std=gnu11`、目标侧对称用 `-std=gnu++17`（macOS 上 `-std=c++17` 会定义 `__STRICT_ANSI__` ⇒ `__DARWIN_C_LEVEL` 降级 ⇒ 隐藏 `strmode`/`fflagstostr`/`undelete`/`lchflags`）。
