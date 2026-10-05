---
name: process-execution
description: Use alongside a matching conversion direction when source code starts a child process, invokes a shell, captures stdout/stderr, waits with a timeout, or observes exit status. Preserves process-tree, stream, timeout, and cleanup semantics across languages; it is not an independent conversion direction or execution authorization.
---

# 进程执行场景：转换语义

本场景只在源码确有子进程启动、shell 调用、输出捕获、等待或退出状态观察时与方向 Skill **共同阅读**。它不按“命令执行”“C2”等标签推断行为，也不授权运行样本。先确认源码是显式 shell 调用还是直接可执行文件、参数边界、工作目录/环境继承、流捕获方式、超时/取消和后代进程策略。

## 转换时保留的决策边界

| 源码依赖 | 应保留或确认 | 常见误改 |
|---|---|---|
| 调用形态 | 显式 shell 与直接 `argv` 的差异；shell 管道、展开、重定向是否属于源行为 | 给直接 `argv` 额外套 shell，扩大解释面；把显式 shell 改成参数数组而丢失管道/展开 |
| 参数与环境 | 参数边界、空参数、工作目录、环境变量继承/覆盖、stdin 来源 | 用字符串拼接重新解释参数；静默重置 cwd/env |
| stdout/stderr | 是否分离、合并顺序、文本解码、截断上限、读取线程/非阻塞策略 | 合并两条流改变顺序；无上限读取导致内存耗尽；只读一条流导致管道阻塞 |
| 等待与超时 | 直接进程退出、管道 EOF、超时预算、取消后的回收顺序 | 把“进程已退出”与“输出管道已排空”混为一谈；超时后无限等待后代 EOF |
| 后代进程 | 是否要求杀进程树、作业/进程组、平台限制 | 只杀直接子进程却宣称全树终止；改变源程序没有的强制终止语义 |
| 退出与错误 | 正常退出码、信号/异常终止、启动失败、超时、I/O 错误的可观察分类 | 把所有非零结果压成一个错误；丢失退出码或部分输出 |
| 资源清理 | 管道、句柄、临时文件、线程和进程对象的关闭顺序与失败传播 | 依赖 GC/析构时机；清理失败静默忽略 |

## 语言与平台映射边界

- **Go `os/exec` → C++**：`exec.CommandContext` 只保证向直接进程发送 Kill；`WaitDelay` 限制的是等待 I/O 管道关闭的额外时间，不承诺回收整个进程树。C++ 目标须用具体平台 API 分别实现启动、管道读取、等待和超时，不能把 Go 的 `Cmd` 行为逐字段臆造到 `std::system` 或 `popen`。
- **shell 语义**：Windows `cmd /C`、PowerShell、POSIX `/bin/sh -c` 的引用、展开、内建命令和退出码不同。只有源码明确调用 shell 时才保留解释语义；目标解释器不明时标为缺口。
- **输出捕获**：stdout/stderr 分离需要两个独立管道和并发排空，否则子进程可能因管道写满而阻塞。捕获上限、解码方式和截断行为属于可观察契约。
- **超时/取消**：超时后需要区分“直接进程已回收”“管道已关闭”“后代仍存活”三种状态；目标平台若只能杀直接子进程，应在交付中明确限制。

## 与方向 Skill 的组合

方向 Skill 负责语言 API 与错误模型映射，本场景负责进程可观察语义。跨 POSIX/Linux 与 Windows 边界时，须共同加载 [POSIX ↔ Windows 进程创建与身份/权限](../../systems/posix-windows-process-identity/SKILL.md)（进程创建/替换/等待/终止与令牌特权的平台差异）；涉及并发 worker 时另读[并发场景](../concurrency/SKILL.md)；服务与注册表行为加读 [Windows 注册表与服务子系统](../../systems/windows-registry-service-subsystem/SKILL.md)。跨 OS 的进程/权限 API 若无对应条目，应列缺口，不把 POSIX 与 Win32 进程模型当成同名等价。

不运行来源不明的命令或构建脚本；只以固定合成命令、受控 cwd/env 和隔离环境设计行为 oracle。本文件不证明任何进程样例已获运行许可或已完成验证。

## 依据

- [Go `os/exec`](https://pkg.go.dev/os/exec)：`Cmd`、`WaitDelay`、`StdoutPipe`/`StderrPipe` 与进程回收边界。
- [POSIX `posix_spawn`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/posix_spawn.html)、[`waitpid`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/waitpid.html)：启动、状态宏与等待语义。
- [Microsoft `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)、[`WaitForSingleObject`](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)：Windows 进程创建、句柄与等待语义。
