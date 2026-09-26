# C01 · uhttpd · configured-model run-02 · 转换交付说明

> 状态：EXPLORATORY DRAFT；原始目标代码由 `deepseek-v4-pro` 首次生成并修订；第三方探查发现原始稿存在编译错误，`repair-01` 单行修复已应用到当前 `target.cpp`，并在 MinGW/UCRT64 C++17 探查工具链上通过并匹配有限 HTTP oracle。该结果不外推为 MSVC/Pelles 编译或完整行为等价。

## 1. 任务与实际完成范围

- 源：PJO2/uhttpd `uhttpd.c`，commit `59d17b86ec9f2a70ce1f4369b4c148824be55155`，GPL-2.0-or-later；源 1,317 个 LF 物理行。
- 源画像：C / Linux x64，按 POSIX `UNIX` 分支理解。
- 目标画像：C++ / Windows x64；MSVC-compatible C++17 是探索假设，工具链未冻结。
- 场景：`network-io`、`file-io`、`concurrency`；ATT&CK tactic/technique 为 `none`；RAG 关闭。
- 目标：`target.cpp`，1,212 个 LF 物理行。模型首轮返回完整文本；Agent 静态审阅后把具体疑点交回同一模型，模型返回完整修订稿；随后模型对设置字段的 constness 作出决策，Agent 机械应用该决策。第三方诊断后，repair-01 单行修复已应用到当前 `target.cpp`，pre-eval 原始稿保存在 `02-conversion/target.gen.cpp`。
- 没有把 `run-01/target.cpp` 作为模型输入。上游源文件自身已有 Windows 分支，当前转换选择并整理该分支，不证明模型独立完成 POSIX→Win32 的移植。

完整源码画像、选用 Skill 和源代码风险见 [`source-analysis.md`](source-analysis.md)。模型请求/响应元数据及自评/决策记录见 `02-conversion/target.gen.model.json`、`02-conversion/target.gen.revision.model.json`、`02-conversion/target.gen.constness.json`、`03-self-review/self-review-1.json`、`03-self-review/self-review-1.decision.json`；这些文件不包含密钥。

## 2. 配置模型自评与 repair 决策（非客观语法结论）

- 自评模型：当前 `.env` 配置的 `deepseek-flash`；RAG 关闭。输入包括源文件与 run-02 目标文本。
- 第一次请求遇到无效模型名；更正 `.env` 后，较长请求两次未完整返回（一次 JSON 不完整，一次 `finish_reason=length`，reasoning 用尽输出预算）；这些不构成自评结论。
- 精简请求成功返回 4 条发现，但顶层写 `REPAIR-RECOMMENDED` 与每条“无需修复”、空 replacements 矛盾。随后同一模型澄清：正确决策是 `NO-REPAIR-IDENTIFIED`，没有发现需要代码修改的、明确的 target-introduced issue。
- 模型归类的关注点主要是源代码已有风险（如 `StartHttpThread` 失败路径使用已释放对象、`StringCchPrintf` 格式处理）和 Windows-only 目标范围；它认为这些不是本轮转换引入的问题或不需要因此改代码。自评指出的目标 SDK/类型点未构成明确修订建议。
- 第三方诊断后，模型明确建议修复未限定的 `min()`；该单行修复已应用到当前 `target.cpp`。此前 `NO-REPAIR-IDENTIFIED` 只表示模型自评未建议修复，已被第三方编译证据纠正；它不表示原始稿语法正确或行为等价。

模型自评原始结果、重试元数据和矛盾澄清分别保存在 `03-self-review/self-review-1.json`、`03-self-review/self-review-1.model.json`、`03-self-review/self-review-1.attempt-2-truncated.json`、`03-self-review/self-review-1.decision.json` 及失败尝试记录 `03-self-review/self-review-1.attempt-1-failed.json` 中。
## 3. 保留的风险与未决问题

- 源 POSIX 包装 `realpath` 与目标 `GetFullPathName` 不是同义 API。目标路径边界仍依赖字符串前缀比较，不能据此声称完整目录穿越防护。
- `ThStatus` 被不同线程读写而未见显式同步；`StartHttpThread` 创建线程失败分支释放对象后仍在函数末尾读取该对象；本次没有静默修复。
- `InitSocket` 覆盖 `WSAStartup` 返回值；GET 的 `send` 返回值未处理部分发送；`main` 无限循环后的 `Cleanup()` 实际不可达。
- Windows socket 诊断路径仍混用 `GetLastError()` 与 CRT `errno` 文本。目标 SDK/CRT 的精确版本、`TCP_MAXSEG` 可用性、路径字符编码、线程/文件句柄边界及错误分支均需后续审阅。
- 目标头部保留上游历史注释称单文件可在多个平台编译，但当前目标只选择 Windows 分支；该注释不应被理解为本次 C++ 目标仍支持 Linux/macOS。

## 4. 第三方远程评估结果

用户明确授权在独立虚拟机执行。旧仓库 Remote Controller `http://192.168.101.250:8443` 的健康检查返回 `status=ok`、`runnerMode=agent`；Linux/Windows x64 C/C++ runners 均为 READY 并支持快照回滚。Controller 的comparison契约会**构建并运行 source 与 target 两侧**，所以按此真实范围提交；它不是 compile-only 接口。Controller 原始报告、两侧证据、比较结果、capsule 和请求记录保存在 `04-evaluation/`，每个 job 一个子目录（`job-01-initial-probe/`、`job-02-branch-diagnostic/`、`job-03-repair-verified/`），目录内统一为 `report.json`/`report.md`、`comparison.json`、`evidence-source.json`、`evidence-target.json`、`logs.json`、`capsule.zip`。

### Job A：原始 target 初次探查

- Job：`eval-20260926-052137-b10a6e2f`；双 Runner：Linux x64 与 Windows x64；两侧清理通过、Runner 回到 READY。
- Linux 原始 C 源成功编译并运行固定 loopback 请求。Windows 目标构建失败，target 没有执行，因此行为 verdict 为 `inconclusive`。
- 当时命令强行向 MinGW g++ 定义 `_MSC_VER`，导致 MinGW Windows 系统头额外出现 `__uuidof` 错误；同时源代码 `target.cpp:718` 的 `min` 未声明。这次不能简单概括为“MSVC 编译失败”。

### Job B：编译分支诊断

- Job：`eval-20260926-052507-8c9beb3a`；唯一变量是将 `-D_MSC_VER` 改为 `-D__POCC__`，未改 source/target。
- `__uuidof` 头文件噪音消失，剩余明确诊断为 `target.cpp:718:23: error: 'min' was not declared in this scope`。Linux 源端成功；目标仍未执行。

### Job C：模型修订副本

- 将上述第三方诊断交给 `.env` 配置的 `deepseek-flash`；Agent 仅按模型明确建议机械应用一处单行补丁，保留 pre-eval 原始稿快照 `02-conversion/target.gen.cpp`，修订文件为 `02-conversion/target.eval-repair-1.cpp`，并已同步到当前 `target.cpp`。补丁把未限定 `min()` 改为等价边界选择三元表达式，未增加头文件。首个模型响应因 token 上限截断，未应用（见 `02-conversion/target.eval-repair-1.attempt-1-failed.json`）；禁用 reasoning 后重试得到完整建议，元数据与 provenance 见 `02-conversion/target.eval-repair-1.model.json`、`target.eval-repair-1.proposal.json`、`target.eval-repair-1.provenance.json`。
- Job：`eval-20260926-052820-e96bf2ee`。源端 Linux C 与修订目标 Windows C++ 均 build 成功、运行成功。Controller canonical outcome：`runVerdict=runnable`、`codeVerdict=passed`、`behaviorVerdict=matched`、`environmentStatus=clean`；源与目标 cleanup 均 PASSED，runner 未污染。
- 该次 Windows 命令是 `g++ -D__POCC__ -std=c++17 ... -lws2_32`，从诊断路径可确认 MinGW/UCRT64。它支持“修订副本在该探查工具链上可编译”，**不证明目标原始文件通过，不是 MSVC/Pelles/Windows SDK 语法结论**。

### 受测行为范围与限制

helper 仅连接 `127.0.0.1`，使用临时 docroot，依次请求 GET `/`、GET 已知文件、HEAD 已知文件、GET 缺失文件和 GET 未知扩展。比较只观察 stdout JSON，结果为 1/1 个适用维度匹配。文件系统、并发、路径边界、安全属性、进程树和网络遥测均未评估；这不构成广义行为等价或安全结论。Controller 的公开 job evidence 没有报告 VM OS 级外网出口策略，因此不额外声称网络出口已被验证。

## 5. 当前判定

| 项目 | 状态 | 证据/边界 |
|---|---|---|
| 模型原始自评 | `NO-REPAIR-IDENTIFIED` | 发生在第三方编译之前，不能代替独立评估；该次确实漏掉了编译器可定位的 `min` 问题 |
| 原始 run-02 target 编译 | `FAILED-EXPLORATORY-MINGW-PROBE` | Job B 报告 `min` 未声明；原文件未被修改 |
| repair-01 target 编译 | `PASSED-EXPLORATORY-MINGW-UCRT64-GXX-C++17` | Job C Windows Runner build exit 0；不外推为 MSVC/Pelles |
| 有界 HTTP output oracle | `MATCHED` | 仅五个固定请求、stdout JSON 结构；1/1 applicable dimensions |
| 完整行为/安全等价 | `UNVERIFIED` | 未覆盖的场景、安全与副作用见上 |
| 当前转换稿状态 | `EXPLORATORY DRAFT / REPAIRED` | 当前 `target.cpp` 为 repair-01；`02-conversion/target.gen.cpp` 保留 pre-eval 原始失败稿，不构成正式 baseline |
| 虚拟机执行与清理 | `COMPLETED / CLEAN` | 三个 job 的 source/target lifecycle 清理均成功，Runner 回到 READY |

## 6. 后续建议

如果需要形成正式 C01 基线，应先决定本例 Windows 目标的权威工具链（MSVC、Pelles 或 MinGW-w64）；固定编译器/SDK版本与命令后，在同一版本下提交最终冻结稿。再扩充并审阅 oracle，特别是错误路径、并发、文件系统证据与路径行为。现有一次 `matched` 仅说明这五个样例请求在指定 exploratory runner 环境中匹配；不得升级为转换准确率、全功能等价或安全验证。

