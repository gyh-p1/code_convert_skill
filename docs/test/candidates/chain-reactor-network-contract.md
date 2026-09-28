# Chain Reactor 网络模块：候选任务与功能义务

> 状态：候选契约（静态设计；**无源快照导入、无模型转换、无编译/运行证据**）
> 上游：Red Canary [Chain Reactor](https://github.com/redcanaryco/chain-reactor/tree/51c25c4c9dfdc73085c35882d6bbb58e56c006a7)，提交 `51c25c4c9dfdc73085c35882d6bbb58e56c006a7`，[MIT 许可](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/LICENSE)。这是实际 Linux 网络 API 构成的**对抗行为模拟组件**，不是完整在野攻击链。

## 1. 转换单元与身份

| 文件 | 静态作用 | LF 物理行 / SHA-256 |
|---|---|---|
| [`src/networking_quarks.c`](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/src/networking_quarks.c) | 拟转换的单个 C 翻译单元；含连接、发送、监听、`socketcall` 等分支 | 559 / `8b8c2f355b0382f19dda088ff2d32fadc9b7b22713df0e87dca2b2330851edf0` |
| [`src/atoms.h`](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/src/atoms.h) | `pconnect_t`、socket 方法/类型等共享声明；含 C flexible array 结构 | 116 / `6f453c9387fe3db65b090e6a4088a0be8e8e8108b8758bf51d9ddf26f30c0d33` |
| [`src/util.h`](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/src/util.h) | `urand` 声明与日志宏 | 81 / `5a412fa44ee28e1fc9ff1b9b12544069ffdeb6ced878e12627367492a49a1be7` |
| [`src/util.c`](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/src/util.c) | 原件伴随 C 实现；连接路径用其 `urand`。同文件还有复制/删除等**不应由本 case 调用**的函数 | 227 / `b20032a4f5f03822d3e13d610ddb25737e7195e8bb36a26094bd714680935391` |

计划只转换 `networking_quarks.c`，源侧与目标侧均保留同一份未改写 `util.c` 作为 C 伴随实现。需要 case 私有的**最小入口**才能只调用 `quark_connect`；这个驱动不是上游攻击链，必须单列身份与行为。目标 C++ 与 C 伴随实现之间的 `urand` 链接名称/声明是待第三方构建验证的 C ABI 边界，不由静态文档判定为通过。项目原 Makefile 构建全部源码并引用额外 `deps/` 路径，不作为本单元的冻结 build 命令。主翻译单元在 700 行计划上限以内，但**连同伴随代码和驱动不等于一份 559 行完整程序**，不能据此验收整体 700 行能力。

## 2. 本次只拟观察的源码路径

选择 Linux x64、C→C++、**同 OS**，先限定 `quark_connect` 的 IPv4/TCP、普通 socket 分支，地址由 case 私有入口固定为 `127.0.0.1` 和隔离 receiver 端口。上游仓库示例 JSON 含公网目标，不能进入 capsule；也不让任何用户字符串覆盖目标地址。源文件的 UDP、IPv6、监听、`fork`、x86 `int 0x80`/`socketcall` 分支仍被编译范围覆盖，但**不在本次行为通过范围**，逐项记 `UNVERIFIED`。若编译器/架构使这些未调用分支阻断全文件构建，记实际构建诊断，不靠删代码伪造通过。

本候选属于**单文件翻译单元 + 原样伴随依赖 + case 私有入口**。若项目以后需要完整 Chain Reactor 的 JSON 编排或组合攻击链效果，应另立任务，不能从本候选结果外推。

## 3. 转换前功能义务草案

| ID | 受控输入与源行为 | 必需观察 | 不可推出的结论 |
|---|---|---|---|
| N-01 正常连接 | case 内启动 loopback TCP receiver，调用 `quark_connect` 一次。源码尝试从 `/dev/urandom` 填充 512 字节缓冲区，并以**一次** `send` 发送；`send` 可能短写 | receiver 接受连接数、实际接收字节数；驱动记录函数返回值/退出类别、是否在时限内结束。只有源基线与目标均观察到同范围完整结果，才可对**该次配置**作有限匹配判断 | 不比较随机字节的逐字节值；不因成功连接证明随机性质量、所有网络方法或 C2 协议正确 |
| N-02 拒绝连接 | 相同 loopback 地址、受控且确认无监听的端口；函数应走连接失败与关闭路径 | 函数错误类别、receiver 无接受连接、进程按时结束；源/目标同口径比较。端口竞争或无法确认拒绝原因时记 `INCONCLUSIVE` | 不由 stderr 文本或单一退出码推断所有失败路径正确 |
| N-03 源异常/短发送 | 源 `urand` 未检查 `open/read` 结果且其 `int` 函数没有显式返回值；`send` 没有重试保证完整 512 字节。`create_socket` 失败时连接函数还可能在 `err` 未更新的情况下返回 0 | 若源侧实际接收长度与函数返回值不支持正常样例的预设条件，保留原始诊断并标源基线异常/范围内未判定；目标按源实际可观察义务审阅。N-02 只针对明确走到 `connect_socket` 的拒绝路径 | 不把源既有的短写、随机读取或错误码问题计成转换引入缺陷；不为凑通过修改源实现 |

**证据方式**：拟由两侧同结构的 case 私有 `run_case.py` 在获批远端 VM 内启动受控 receiver、驱动待构建程序，并各自打印有界 JSON；Controller 当前的 `output` 维度可比较事先选定的结构字段。端口、随机 payload 摘要与时间戳不进入严格相等字段；若保留摘要仅供诊断。receiver 日志是**这个 case 的局部观察**，不是 Controller 的完整 network Collector：它不能证明没有其他未观察连接、不能证明随机性质量或所有 socket 分支。没有 receiver 有效记录时功能结果为 `INCONCLUSIVE`，不从 liveness 或 build 推断通过。

## 4. 构建、环境与安全门槛

- **待冻结工具链**：源侧 Linux C（候选 GNU C11）、目标 Linux C++（候选 GNU C++17）以及未改写的 C 伴随翻译单元；实际编译器/命令/SDK、C flexible array 在 C++ 头的可用性、C ABI 声明与链接方式都要先写入 run 契约，再由 Controller build 证据判定。本机不编译。
- **同机取证**：RC4 Windows run 的 same-runner 错误已复现两次；Linux 同机是否重现**尚无实测**，但使用同一编排路径，须在旧仓库先用无害固定 capsule 明确故障范围并修复/验收，再提交本候选。不为绕过故障改成 Linux→Windows，因为那会混入进程/API 系统迁移。
- **网络隔离**：未来执行前须由远端配置/证据确认出网受限且 case 仅能触达 loopback；只用合成随机数据，不读取真实文件/凭证，不运行上游公网示例。`util.c` 的复制/删除函数和模块监听/fork 分支不由 case 入口调用；仍需静态审阅 packaging，结束清理 receiver、子进程与临时目录。
- **停止条件**：若源侧无法在已授权 Linux VM 建立可解释 build 基线、最小入口不可避免触发额外危险分支、receiver 无法提供必要观察或出网限制不可核实，停在候选，不发起模型转换或动态评估。

以上是**候选设计**，不代表用户已批准此具体 capsule 的运行，也不改变现阶段只统计最终目标编译结果的产品口径。下一步先决定源快照/入口范围与 Controller 无害故障复现，再单独冻结可执行 run。
