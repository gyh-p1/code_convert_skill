---
name: process-execution
description: Use alongside a conversion direction when source launches child processes or shells, captures streams, waits, times out, or observes exit status. Preserve process-tree and cleanup behavior without granting execution authorization.
---

# 进程执行场景：转换语义

> **加载前置**：先读取根[转换入口](../../../SKILL.md)并完成其必读契约与语言/方向选择；本页补充行为义务，不单独推进转换。

源码实际创建子进程、调用 shell、捕获、等待或观察退出时与方向共同阅读。不按命令执行/C2 标签推断，不授权运行。普通打印、宿主通道和换行事实由语言页维护，无子进程源码不因输出行为加载本场景。

## 转换时保留的决策边界

| 源依赖 | 应保留/确认 | 常见误改 |
|---|---|---|
| 调用形态 | 显式 shell 与直接 argv、管道/展开/重定向 | 给直接 argv 套 shell 扩大解释面，或删源 shell 语义 |
| 参数/环境 | 参数边界、空参数、cwd、env 继承/覆盖、stdin | 字符串拼接重解释、静默重置 cwd/env |
| 流捕获 | 分离/合并、顺序、编码、缓冲与截断上限、并发排空 | 合并改变通道，只读一流堵塞，无限读取耗内存 |
| 等待/超时 | 直接进程退出、管道 EOF、取消后回收顺序与预算 | 退出当排空、无限等后代 EOF |
| 后代进程 | 是否杀树、进程组/作业及平台限制 | 仅杀直接进程却宣称整树终止 |
| 退出/错误 | 正常码、信号/异常、启动失败、超时和 I/O 故障 | 所有非零压成一类，丢部分输出 |
| 清理 | 管道/句柄/文件/线程/进程的顺序及失败传播 | 依赖 GC、忽略清理失败 |

## L2-PROC-01 宿主输出通道属于可观察行为，不得只图可用

旧锚点保留，普通语言事实归位至[PowerShell 通道](../../references/languages/powershell.md#宿主与输出通道)、[Ruby puts](../../references/languages/ruby.md#输出换行puts-与字节写入)和[C# WriteLine](../../references/languages/csharp.md#输出换行consolewriteline)。本场景只规定子进程观察：按源捕获/重定向方式保留通道与交错规则，不把退出码正确当作流内容正确，不新增提示文本。

## L2-PROC-02 父子分支、映像替换与环境契约

1. **触发/前提**：源创建、替换进程或指定环境；先冻结 OS/API、参数、父子失败出口、观察目标和初始环境，不从战术标签推定。
2. **保留义务**：区分父/子/创建失败；区分新子进程与替换自身；成功不返回、失败续行/退出、进程身份、等待和清理按源实际分支保持。环境区分继承、合并、完整替换、空集合，不能把省略参数与空集合合并。
3. **条件映射**：目标 API 返回值/异常/选项依两语言页和方向选；原生 fork/exec 事实即使同 OS 也读[系统页](../../systems/posix-windows-process-identity/SKILL.md#原生-forkexec-事实)。可表达全部义务才采用替代调用。
4. **反例**：只确认子程序启动，忽略父子分支或成功后的源语句是否执行；把显式空环境变成继承；为保持“不返回”而自行新增退出，均不能证明等价。
5. **未知/依据**：缺源分支、准确平台或允许差异时记缺口，不补造路径；事实依据见上述系统页与[Ruby 进程页](../../references/languages/ruby.md#九进程返回替换与环境)。本条不增加运行授权、自审轮数或辅助驱动。

## 语言与平台映射边界

具体 API 改写由方向页维护，例如[Go→C++ 的 os/exec](../../directions/go-to-cpp/SKILL.md#子进程-api-映射)。本场景只规定显式 shell 语义、并发排空、取消/回收和输出观察义务；目标解释器、杀树能力或管道关闭条件未知时记缺口，不按名称推断。

## 与方向 Skill 的组合

实际 fork/exec 或跨 POSIX/Linux 与 Windows 时读[进程创建/身份权限](../../systems/posix-windows-process-identity/SKILL.md)，同 OS 只消费适用事实，不套跨 OS 表；worker 协作读[并发](../concurrency/SKILL.md)，服务/注册表读[Windows 子系统](../../systems/windows-registry-service-subsystem/SKILL.md)。只设计合成输入与受控 cwd/env 的观察需求，实际驱动须[合法提供](../../../references/framework/evaluation-readiness-contract.md#2-驱动来源与四要素)，不编写或运行辅助程序。

## 依据

- Go os/exec：进程与管道等待边界。
- POSIX posix_spawn、waitpid：启动/状态/等待。
- CreateProcessW、WaitForSingleObject：Windows 句柄/等待。

规则是静态知识，不证明逐例行为。回到[根入口](../../../SKILL.md)、[AGENTS.md §3](../../../AGENTS.md)与[安全边界](../../../references/framework/safety-boundary.md)：分类 ALLOWED→源侧预检（构建 + 适用运行基线）→生成/自审→评估就绪→提交/取证→交付门禁，场景不替代门禁或授权。
