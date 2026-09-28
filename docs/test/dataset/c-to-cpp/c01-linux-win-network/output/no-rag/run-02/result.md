# C01 uhttpd 转换结果报告（run-02）

> 历史状态：原固定四例方案已[取消](../../../../../../../stages/four-case-cancellation.md)。下文“若要形成正式 C01”是当时的未决记录，不再是当前行动项。

## 结论速览

本次**探索**已交付修订后的 Windows C++ 代码：它在 MinGW/UCRT64 C++17 探查工具链上编译通过，五个固定 loopback HTTP 请求的输出与源端匹配。目标工具链尚未正式冻结，其他功能和安全属性未验证，因此不能宣称正式转换通过或完整行为等价。

| 问题 | 结论 | 依据与边界 |
|---|---|---|
| 最终代码是否交付完整 | **已完成探索稿** | 当前 [`target.cpp`](target.cpp) 是模型修订后的单文件；原始稿保存在 [`02-conversion/target.gen.cpp`](02-conversion/target.gen.cpp) |
| 语法/编译是否正确 | **探索工具链通过；正式目标未验证** | 修订稿在 Windows x64 MinGW/UCRT64 `g++ -D__POCC__ -std=c++17 ... -lws2_32` 下 build 成功；不能外推为 MSVC/Pelles 通过 |
| 功能是否一致 | **约定范围内匹配；总体未验证** | 仅五个固定请求的 `stdout JSON` 匹配（1/1 个已观察维度）；并发、文件系统、路径边界、进程树、网络遥测和安全属性均未覆盖 |

## 任务与最终交付

- 源码为 PJO2/uhttpd 的 `uhttpd.c`，commit `59d17b86ec9f2a70ce1f4369b4c148824be55155`，GPL-2.0-or-later。按 Linux x64 的 POSIX `UNIX` 分支理解；目标是 Windows x64 C++17 单文件，RAG 关闭。
- 源文件有 1,317 个 LF 物理行，超过计划的 700 行上限。它自身已有 Windows 实现分支，本次主要选择并整理该分支，不能用来证明独立 POSIX→Win32 移植能力。
- 最终交付文件为 [`target.cpp`](target.cpp)；源码画像、Skill 选择和静态风险见 [`source-analysis.md`](source-analysis.md)。这是探索稿，不是冻结的 No-RAG 基线。

## 转换过程与关键问题

1. 配置模型生成并修订了最初目标稿。模型后来自评为 `NO-REPAIR-IDENTIFIED`，没有发现必须修改的转换问题；这只是模型判断，未能发现实际编译错误。自评和此前无效、截断、矛盾的响应均保存在 [`03-self-review/`](03-self-review/) 供开发追溯。
2. 首次第三方探查未能构建目标稿。探查命令向 MinGW g++ 人为定义 `_MSC_VER`，引入 Windows 头文件的 `__uuidof` 噪音；更换为 `-D__POCC__` 并保持源/目标代码不变后，目标稿仍报 `target.cpp:718` 的 `min` 未声明。由此把工具链分支问题与可定位的目标代码问题分开，见 [Job A](04-evaluation/job-01-initial-probe/report.md) 和 [Job B](04-evaluation/job-02-branch-diagnostic/report.md)。
3. 将 `min` 诊断交给配置模型后，模型给出一处单行修订；Agent 机械应用并保留原稿。修订稿保存为 [`02-conversion/target.eval-repair-1.cpp`](02-conversion/target.eval-repair-1.cpp)，同时成为当前 `target.cpp`。它在同一 MinGW/UCRT64 探查条件下编译、运行并通过有限输出比较，见 [Job C](04-evaluation/job-03-repair-verified/report.md)。原始稿的失败不能回写成原稿通过。

## 验证依据与覆盖范围

- **编译**：最终修订稿在 Job C 的 Windows x64 Runner 上 build exit 0；Linux 原始 C 源也 build 成功。Windows 结论只适用于该次 MinGW/UCRT64 C++17 命令，目标 MSVC/Pelles、SDK/CRT 精确版本尚未验证。Job A/B 的编译失败仅解释中间稿和探查条件。
- **运行与功能**：经用户逐例授权，隔离第三方 VM 对源端与目标端请求 `GET /`、`GET /known.txt`、`HEAD /known.txt`、`GET /missing.txt`、`GET /unknown.zz`。helper 使用 `127.0.0.1` 和临时 docroot；比较的是 `stdout JSON` 中的状态、选定头部与 body 摘要/长度，Job C 报告一个适用输出维度匹配。它没有观测并发、文件系统变化、路径边界、进程树、网络遥测或安全属性。
- **环境**：Job A/B/C 的报告均记录清理通过、Runner 返回 READY。Controller 公开证据未给出 VM 的 OS 级外网出口策略，不能据此声称已验证出网限制。完整 capsule、两侧证据和原始报告留在 [`04-evaluation/`](04-evaluation/)。

## 未决问题与下一步

1. 若要形成正式 C01 编译结论，先确定并冻结权威 Windows 工具链、SDK/CRT、编译命令和最终稿版本，再在获批隔离环境中检查。当前阶段可只依据该版本的 build 证据报告语法结果。
2. 源与目标仍有路径规范化和 docroot 前缀检查、`ThStatus` 跨线程读写、线程创建失败后的对象生命周期、Winsock 错误报告与部分发送处理等未决风险；静态观察见 [`source-analysis.md`](source-analysis.md)。本次没有把这些源已有或未确认问题静默改为新的功能。
3. 如日后重启功能正确性评估，应先冻结更广的行为 oracle，再分别报告覆盖范围和差异；本次五个请求的匹配不承担该结论。
