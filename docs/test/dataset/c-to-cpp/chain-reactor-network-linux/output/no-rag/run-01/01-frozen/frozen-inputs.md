# Chain Reactor 网络模块 run-01：冻结输入

> 状态：FROZEN（仅文本转换输入；未编译/运行）
> 归属：[case.md](../../../../case.md) · [阶段 step-07](../../../../../../../../stages/final-output-compile/step-07-chain-reactor-network-case.md)

## 身份与目标

- 主源：[`networking_quarks.c`](../../../../../../../sources/chain-reactor-network/networking_quarks.c)，上游 Red Canary Chain Reactor commit `51c25c4c9dfdc73085c35882d6bbb58e56c006a7`，SHA-256 `8b8c2f355b0382f19dda088ff2d32fadc9b7b22713df0e87dca2b2330851edf0`，559 LF 物理行。
- 伴随原件：[`atoms.h`](../../../../../../../sources/chain-reactor-network/atoms.h)、[`util.h`](../../../../../../../sources/chain-reactor-network/util.h)、[`util.c`](../../../../../../../sources/chain-reactor-network/util.c)；完整哈希、MIT 许可见[源说明](../../../../../../../sources/chain-reactor-network/source.md)。
- case 私有非上游入口：[`driver.c`](../../../../driver.c)，SHA-256 `ff710e0e6689d84fa4e1c8789270aac1339d121baad097b240669bcfeb6b1da6`；唯一网络目标固定 loopback，端口由未来受控 receiver 给定。任何修改另起版本。
- 目标：`target.cpp`，Linux x64 C++17（GNU 扩展）。源与目标同 OS。只翻译主源完整翻译单元，不改写伴随 C 实现或新增网络/进程/权限能力；保持 `quark_connect` 与 C 入口的调用 ABI、整数/结构语义和原有错误/清理路径。
- 任务工作流：根 Skill + C→C++ 方向 + 网络 I/O 场景 + 长文件工作流 + header-macro/type-abi 专题；ATT&CK 无源代码证据时 `none`；RAG 关闭。

## 编译与行为范围

源侧拟以 GNU C11 编译网络主源、`util.c` 与 `driver.c`；目标侧拟以 GNU C++17 编译目标翻译单元，并与**原样 C 编译**的 `util.c`、`driver.c` 链接。精确命令、编译器版本及 C/C++ 名称链接条件在第三方评估准备时冻结；当前没有本机语法检查或 build 结果。

未来 case receiver 只监听 VM 内 `127.0.0.1` 的一次性端口。正常路径记录接受连接数、实际接收长度、驱动 `CASE_SEND_RESULT`、退出/超时；拒绝路径记录无监听时的错误类别与清理。源码尝试一次发送从 `/dev/urandom` 读取的 512 字节，不保证读满或短写重试；不逐字节比较源/目标随机 payload。完整未覆盖范围见[案例契约](../../../../case.md)。

## 执行门槛

本机只读写文本并调度 `.env` 配置模型，**不编译/运行**源、目标或 `driver.c`。远端提交前须取得 Linux VM 出网限制、loopback receiver、伴随依赖与清理的可复核条件，并用无害 capsule 核对 Linux 同机 source/target 取证。Windows RC4 的哈希修复本地测试不等于 Linux 路径或远端部署已验收。第三方目标 build 回传前编译状态 `UNVERIFIED`，行为也 `UNVERIFIED`。
