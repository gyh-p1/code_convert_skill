# Chain Reactor 网络模块：Linux C → Linux C++

> 状态：CLOSED / EVALUATED（最终目标 Linux GNU C++17 build PASS；有限 loopback 输出匹配仅作信息记录）
> 阶段真源：[step-07 单例闭环](../../../../项目开发规范.md#当前开发阶段与退出条件)
> 源快照：上游来源说明已清理；冻结副本见当前 run 的 `source/` 目录；上游提交 `51c25c4c9dfdc73085c35882d6bbb58e56c006a7`，MIT。

## 任务范围

- 源：仅把完整 `networking_quarks.c` C 翻译单元转换为一个 `target.cpp`；伴随 `atoms.h`、`util.h`、`util.c` 保持上游原样。`util.c` 同时含其他行为但本 case 只通过 `urand` 与网络模块链接。
- 目标：Linux x64、C++17/GNU 扩展，同 OS 隔离语言变量。拟在第三方 Linux VM 使用 GNU C11/C++17 工具链；精确编译器版本与命令在评估前核对，第三方回传前只记 `UNVERIFIED`。
- 任务模式：主翻译单元 559 LF 物理行，加载 C→C++ 语言方向、网络 I/O 场景、长文件工作流及 C ABI/头文件专题。无跨 OS 系统迁移 Skill；不预设 ATT&CK 战术，仅按实际网络行为记录场景。RAG 关闭。
- [case 私有入口 `driver.c`](driver.c) 固定目标地址为 `127.0.0.1`，只接受端口参数；只调用 `quark_connect` 的 IPv4/TCP 普通 socket 分支一次。入口不是上游代码，保留单独哈希/来源；转换后的 `quark_connect` 需与同一 C 入口正确链接，不能由 Agent 手写目标实现。
- 下列正常、拒绝和源侧异常义务在转换前冻结；该受限入口的结果不代表 UDP/IPv6、监听、socketcall/fork 或完整攻击链等价。

## 来源选择与可观察义务

旧目录 `ApiSetMap.c`、改写的反射加载器与 HTTP 上传样例的准入问题见旧候选审阅（已清理，不再作为当前数据）。此处选 Chain Reactor，是因为[发布方](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/README.md)、固定提交与 MIT 许可可核，模块使用真实 Linux 网络 API；但它仍是对抗行为**模拟组件**，不是完整在野攻击链。对照的 [Atomic Red Team T1040 抓包 C 源](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1040/src/linux_pcapdemo.c)需要提权/原始套接字，本轮不选。上游示例 JSON 含公网目标，**未复制入本 case**。

| 义务 | 受控输入与源行为 | 必需观察与结论限制 |
|---|---|---|
| N-01 正常连接 | 私有 loopback TCP receiver、一次 `quark_connect`；源码从 `/dev/urandom` 尝试填充 512 字节并只调用一次 `send` | 记录 receiver 接受连接数、实际接收长度、函数返回值/退出及超时。不能预设写满 512 字节，也不逐字节比较随机 payload；仅对该配置报告有限匹配 |
| N-02 拒绝连接 | 同一 loopback 地址，使用受控且确认无监听的端口 | 记录错误类别、无 receiver 事件、按时结束。端口竞争或未能确认拒绝原因时记 `INCONCLUSIVE`；不以 stderr 字面值覆盖所有失败路径 |
| N-03 源侧异常 | `urand` 未检查 `open/read` 且 `int` 函数没有显式返回；单次 `send` 可能短写，套接字创建失败路径可能在 `err` 未更新时返回 0 | 保留源实际诊断。若源侧结果不满足正常样例的预设条件，标源基线异常/未判定，不把源既有问题计成转换引入缺陷 |

未来拟由两侧同结构的 case 私有 receiver/驱动在获批 VM 内输出有界 JSON，供 Controller 当前 `output` 维度比较。该 receiver 只观察自己收到的连接，**不是**完整 network Collector；额外连接、随机性质量、监听/socketcall 等未被证明。没有有效 receiver 记录时功能为 `INCONCLUSIVE`。源码除主文件外还需要原样 `util.c`；它含本 case 不调用的复制/删除函数，入口与打包时须审阅这一边界。

## 当前门槛

`.env` 配置模型产出完整文本并结构化自审；本机未编译或运行源/目标/驱动。Linux VM 无害同机 capsule job `eval-20260928-122644-d769c056` 先返回双侧 build/clean；随后**本案例** job `eval-20260928-123304-add87d9d` 源、目标 build 均 exit 0，环境 clean。两侧 case receiver 的正常与拒绝路径 JSON 一致，但当前阶段功能不计分。Windows Agent 的混合大小写哈希问题已本地修正但未部署，与本 Linux 案例分开。

本 run 的[最终目标](output/no-rag/run-01/target.cpp)、[结果报告](output/no-rag/run-01/result.md)及[移交清单](output/no-rag/run-01/evaluator_manifest.json)已按第三方真实回传更新。模型自审 `NO-REPAIR-IDENTIFIED` 仅是预检；编译 PASS 只来自目标 evidence bundle，不从自审或行为匹配推断。
