---
name: posix-windows-threads
description: Map the POSIX pthread lifecycle used by a source file to Windows CRT/Win32 thread APIs without assuming identical cancellation, handles, or synchronization semantics.
---

# POSIX ↔ Windows 线程系统方向（初稿）

适用于 Linux/POSIX 的 `pthread_*` 与 Windows CRT/Win32 线程 API 之间的迁移。这里聚焦线程 API 与生命周期；共享状态、顺序和资源归属还须加载[并发场景](../../scenes/concurrency/SKILL.md)。规则以对应 API 契约为依据，未经本项目转换样例验证。

## 适用映射与边界

| POSIX | Windows 常见对应 | 必须核对 |
|---|---|---|
| `pthread_create` | 使用 C/C++ CRT 时优先核对 `_beginthreadex` | 入口调用约定、返回值、参数生命周期、失败值 |
| `pthread_join` | `WaitForSingleObject`，必要时再读退出码 | 等待结果、超时、线程完成与句柄回收的先后 |
| `pthread_t` | Windows 线程 `HANDLE` / CRT 返回的句柄 | 两者不是可互换的整数 ID；目标句柄需在生命周期结束时关闭 |
| `pthread_exit` / 返回值 | 线程入口返回值与 Windows 退出码 | 类型、截断、谁负责读取；不要假定 POSIX `void*` 结果可原样映射 |
| `pthread_cancel` | 无通用等价物 | 取消点、清理处理器和线程状态不能用 `TerminateThread` 机械替代 |

MSVC CRT 文档说明 `_beginthreadex` 的入口/返回类型、失败值与返回句柄；POSIX `pthread_create`/`pthread_join` 规范分别定义线程创建及 join 语义。按具体目标 SDK、CRT 与 POSIX 实现核对。

## 保持行为的规则

- 当线程使用 C/C++ CRT 时，不要仅因 `CreateThread` 名称相似便替换 `_beginthreadex`；核对 CRT 初始化要求及现有运行库。
- 成功创建后，明确哪个路径等待线程、读取退出状态并释放 Windows 线程句柄。等待已完成不自动等同于句柄已释放。
- 创建失败时使用目标 API 的直接错误返回约定，不假设 `errno` 或 `GetLastError()` 一定承载该 API 的错误。
- 不把 `TerminateThread` 当作 POSIX 可取消线程的等价实现；强制终止可能跳过线程内清理。若源码中仅定义而未调用，不要把它虚构成活跃路径。
- 共享普通变量的读写同步属于并发语义，不能仅靠 API 名称映射解决；需要同步改造时，标为有意差异并单独说明。

## 已有目标平台分支

源码若已有 `_beginthreadex`、`WaitForSingleObject`、`CloseHandle` 的 Windows 分支，先确认转换选择的是已有分支还是从 POSIX 线程 API 独立移植。仅复用已有分支不能作为后者的验证；普通状态字段的跨线程同步另按[并发场景](../../scenes/concurrency/SKILL.md)核对。

## 依据

- Microsoft Learn, [`_beginthread`, `_beginthreadex`](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/beginthread-beginthreadex?view=msvc-170)
- The Open Group, [`pthread_create`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_create.html) 与 [`pthread_join`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_join.html)
