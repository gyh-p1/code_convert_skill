# Chain Reactor 网络模块 C→C++ 结果（run-01）

## 结论速览

已由根 `.env` 指定的配置模型生成并自审完整 `target.cpp`，随后在授权隔离 Linux VM 获得**源、目标双侧真实 build PASS**。受控 loopback 的正常与拒绝路径在两侧产生相同的 case receiver JSON；这只是本例两个输入的有限行为匹配，本阶段不计功能正确率，也不证明其它网络/进程分支等价。

| 问题 | 结论 | 依据与边界 |
|---|---|---|
| 最终代码是否交付完整 | 已交付文本候选 | [target.cpp](target.cpp) 与[首次模型稿](02-conversion/target.gen.cpp) SHA-256 同为 `d8b539ab…`，568 行、`finish_reason=stop`；模型输出的 Markdown 围栏已机械去除并记录 |
| 语法/编译是否正确 | **PASS** | Controller job [`eval-20260928-123304-add87d9d`](04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json)：最终 `target.cpp` 在 Linux x64 GNU C++17 与原样 C 伴随对象链接，目标 build `completed/exitCode=0`；源侧 GNU C11 build 亦 exit 0。目标 stderr 有一条 C 专用 GCC pragma 在 C++ 下无效的警告，不影响本次 build |
| 功能是否一致 | **约定范围内匹配（信息记录，不计分）** | 两侧 receiver JSON 均显示一次连接、实际接收 512 字节、`sendResult=512`、正常退出；拒绝路径两侧均 `sendResult=-1`/退出 1，两个 `validObservation=true`。Controller 仅 output 维度 matched 1/1，network Collector 仍不可用；其它分支与随机性质量未验证 |

## 任务与最终交付

- [上游源快照](../../../../../../sources/chain-reactor-network/source.md)：Red Canary Chain Reactor commit `51c25c4c9dfdc73085c35882d6bbb58e56c006a7`、MIT。主文件 559 物理行；原样 C 伴随实现和[case 私有 loopback 入口](../../../driver.c)另计，不把它称作 559 行完整程序。
- Linux x64 C → Linux x64 GNU C++17，RAG 关闭。目标是完整转换主翻译单元，保留源网络/进程分支和外部 C 调用边界，不新增源无能力。任务范围、选中知识与安全边界见[冻结输入](01-frozen/frozen-inputs.md)和[源码画像](source-analysis.md)。
- run 根[最终目标稿](target.cpp)是配置模型首次稿的原样副本；其它请求、响应与模型元数据在[`02-conversion/`](02-conversion/)，结构化自审与请求在[`03-self-review/`](03-self-review/)。没有自修轮或评估后 repair；第三方编译结果只归属该最终稿。

## 转换过程与关键问题

1. **生成**：配置模型 `deepseek-flash`、温度 0.2，一次请求返回 HTTP 200、`finish_reason=stop`；目标 568 行。生成稿与源的静态 diff 集中在显式头、指针转换、C 链接和 `switch` 作用域；完整响应及 token/哈希见[模型元数据](02-conversion/target.gen.model.json)。
2. **自审**：同一配置模型一次结构化审阅为 `NO-REPAIR-IDENTIFIED`，`issues=[]`；明确保留对未调用 `socketcall_*` 的潜在 C ABI 名称变化、GNU flexible array、`intptr_t` 截断及源既有 `urand`/短发送风险。此结论只说明模型未建议可定位修订，**不是**编译器或功能判定，见[自审结果](03-self-review/self-review-1.json)。
3. **人工静态核对与远端评估**：主源的函数、宏、连接与监听分支未见文本级遗漏；`quark_connect` 和 `urand` 的 C 链接已在目标文本声明。授权隔离 Controller 的双侧 build 随后验证本次目标/伴随/入口链接实际通过。其它全局符号 ABI 不在当前入口消费范围内，保留为未来扩展风险；本机没有运行语法检查或编译。

## 验证依据与覆盖范围

已做：来源/许可和 SHA-256 核对、冻结输入、配置模型生成与自审、文本 diff/函数覆盖阅读；[同一 capsule](04-evaluation/job-01-dual-build/capsule.zip)在 Linux x64 Runner `linux-vm-agent-x64`（snapshot `CC-Eval-Linux-8Lang-R7`）分别构建并运行源、目标，job `eval-20260928-123304-add87d9d` 终态 `COMPLETED`、环境 clean。源 build `completed/exitCode=0`，目标 build `completed/exitCode=0`（[源证据](04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json) · [目标证据](04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json)）。两侧 execution 均 completed/exit 0，receiver 输出结构相同，Controller [`comparison.json`](04-evaluation/job-01-dual-build/returned-evidence/comparison.json) 为 output matched；文件系统、进程、registry、network 维度均 `not-applicable`。本机未编译或运行。

未做：随机 payload 字节/熵质量比较、额外连接探测、UDP/IPv6、监听/fork、`socketcall` 分支、其它 C 调用者 ABI、广泛错误路径与完整攻击链功能验证。目标编译 PASS 仅适用于本次冻结的 GNU C++17/Linux x64 命令及代码版本。

## 未决问题与下一步

1. 本例编译门槛已达成，但目标 build 有 GCC 诊断 pragma 的非致命警告；若将来使用更严格工具链，须单独复验。模型自审列出的其它全局 `socketcall_*` C ABI 风险不由本 case 的 C 入口消费，不能据本次链接通过宣称其对所有 C 调用者兼容。
2. N-01/N-02 两个受控 loopback 输入在 case receiver 可见范围内匹配；N-03 源异常/短写未触发。不能将 `1/1 output` 解释为完整网络行为或真实攻击链功能正确率。
3. 旧仓库 Windows Agent 的混合大小写文件哈希排序本地修复（`7d77158`，无害工程测试 67/67）**尚未远端部署**，RC4 C→Go 仍 `INCONCLUSIVE`；它与本 Linux 案例已取得的 build 证据是两项独立事实。
