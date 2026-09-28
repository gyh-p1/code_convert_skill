# step-09：Chain Reactor 网络模块的候选任务契约

> 状态：已完成（候选任务与有限观察义务已写；未导入源码或开启转换 run）
> 归属：[阶段 index](index.md)

## 目标

把 step-08 选出的 Chain Reactor `networking_quarks.c` 从“真实行为线索”收敛为一份可审阅的**候选** C→C++ 单文件任务：明确原件与伴随依赖、Linux 同 OS 工具链假设、受控 loopback 正常/失败路径，以及 Controller 能观察和不能证明的事实。只有这些条件成立后，才考虑冻结源快照、修复同机取证并开启转换 run。

## 纳入与非目标

- 纳入：只读盘点固定上游提交的主文件、`atoms.h`、`util.h`、`util.c`、项目 Makefile 与一份网络配置示例；明确源码整体、拟观察的 `quark_connect` 分支和未覆盖分支的差别。
- 以 case 私有 loopback 接收端输出有限结构化摘要作为**拟议**观察方式；记录正常、拒绝连接及不充分证据时的判定条件。
- 修订 step-08 中对固定 512 字节与 Linux same-runner 的过强表述。
- 不复制上游 C 源到 `docs/test/sources/`，不写或运行 harness，不调用配置模型、不编译、不提交 Controller job、不修改远程 Controller。

## 依赖与前置

1. 上游固定提交 `51c25c4c9dfdc73085c35882d6bbb58e56c006a7`、MIT 许可及主文件 SHA-256 见[step-08 审阅](../../test/candidates/upstream-scenario-search.md)。临时检出仅供只读静态核对。
2. 本项目当前只统计最终目标 build，功能判据仍是设计草案。Windows RC4 真实复现了 same-runner 故障；Linux 同机是否同样失败尚无回传，不得写成实测。
3. 任何未来网络执行都需要可核对的 VM loopback/出网隔离条件与 case 私有端口，不能使用上游 JSON 中的公网地址。

## 预计改动文件

- `docs/test/candidates/chain-reactor-network-contract.md`：候选任务、源/依赖、行为地图、功能义务、观察与停止条件。
- `docs/test/candidates/upstream-scenario-search.md`：修正前轮结论中的未证表述。
- `docs/stages/final-output-compile/index.md` 与本步骤：进度、证据及下一动作。

## 验收依据

- 说明主文件及必要伴随头/实现各自承担什么；工具链、标准、入口/驱动与 C/C++ 链接边界哪些已知、哪些待 Controller 证据。
- 正常/拒绝路径各有可观察事实、比较规则、未观测信号和最小安全边界；不把单次 `send` 当作保证发送完整 512 字节，不逐字节比较随机内容。
- 明确当前 output harness 可覆盖的有限范围，以及 network Collector、额外 loopback 连接、随机性质量、listen/socketcall 等未覆盖范围。
- 文本/引用检查完成；没有执行不可信源码或把静态审阅写成转换效果验证。

## 风险与停止条件

- 若主文件不能与合理的伴随 C 实现/头文件组成可冻结的单文件转换单元，停在候选，不用大规模自造运行时补齐。
- 若出网隔离、同机 Controller 取证或 receiver 观察不成立，不发起动态评估；标环境/证据阻断，不归因模型。
- 若为可测性必须改变上游随机/网络行为，先单独登记原件与 case 适配及差异，再修订方案，不把修改稿冒称原件。

## 完成记录与未验证部分

- [候选任务契约](../../test/candidates/chain-reactor-network-contract.md)已固定四份源/伴随文件的提交身份、行数、哈希与职责，明确只拟转换 559 行网络翻译单元；C `util.c`、共享头和 case 私有入口是必要上下文，不将合计代码冒称 559 行完整程序。
- 对受控 IPv4/TCP 连接给出正常、明确连接拒绝和源短写/随机读取异常三类义务。源码 `urand` 未检查读取且无显式返回值、单次 `send` 可能短写、套接字创建失败可能返回 0，均记源既有风险；不据此宣称目标功能通过。
- 证据只拟由未来获批 VM 内的 case receiver 输出有限 JSON；现有 output 比较不能证明无其他连接或所有网络分支正确。Linux 同机 same-runner 故障范围未实测，下一步先用旧仓库无害固定 capsule 核对并制定修复/验收，再冻结具体 run。
- 静态检查扫描 487 个本地 Markdown 链接，除 fe 上游 README 原有四处缺链外没有新缺链；`git diff --check` 无空白错误。未编译、运行或提交任何 Chain Reactor 样本。
