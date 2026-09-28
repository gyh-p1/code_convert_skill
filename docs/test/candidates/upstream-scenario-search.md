# 联网上游攻防场景候选：首轮静态结论

> 审阅：2026-09-28。只读查看发布方仓库并在系统临时目录检查文本；**未将代码导入本项目、未编译或运行样本、未发 Controller job**。
> 选择：Red Canary Chain Reactor 的网络模块作为**下一步功能契约设计候选**，尚未获准转换或评估。

## 候选对照

| 上游候选 | 来源、行为与许可 | 当前结论 |
|---|---|---|
| [Red Canary Chain Reactor](https://github.com/redcanaryco/chain-reactor) 的 [`src/networking_quarks.c`](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/src/networking_quarks.c) | 固定提交 `51c25c4c9dfdc73085c35882d6bbb58e56c006a7`；[MIT 许可](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/LICENSE)。源文件 559 LF 物理行，SHA-256 `8b8c2f355b0382f19dda088ff2d32fadc9b7b22713df0e87dca2b2330851edf0`；有 `atoms.h`、`util.h` 等伴随依赖。模块真正调用 Linux socket/syscall 路径执行连接、发送、监听等对抗模拟行为 | **优先设计候选，未冻结 run**。真实 OS 行为比玩具文件例更接近使用场景，但它仍是攻击模拟框架组件，不能代表完整在野植入体；需先确定构建单位、仅 loopback 的输入、观察判据及 same-runner 修复 |
| [Atomic Red Team T1040 `linux_pcapdemo.c`](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1040/src/linux_pcapdemo.c) | 发布方[测试定义](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1040/T1040.md)将其用于 Linux 网络流量抓取，要求提权/原始套接字；网页显示约 219 行 | **本轮不选**。真实包捕获路径有代表性，但权限与网络观察需求超出当前最小安全/评估范围；未固定该文件提交或导入 |
| [Stephen Fewer ReflectiveLoader](https://github.com/stephenfewer/ReflectiveDLLInjection/blob/178ba2a6a9feee0a9d9757dcaa65168ced588c12/dll/src/ReflectiveLoader.c) | 上游许可可核，真实反射加载行为；用户旧目录副本与上游不同且达 750 行，见[前轮审阅](real-scenario-source-review.md) | **不作首例**。Windows 同机双侧取证、改写身份及内存行为观察均未解决 |

Chain Reactor 发布方将项目描述为用于 Linux 端点检测覆盖的对抗行为模拟器；这是**真实系统调用组成的模拟场景**，其真实性边界应在数据集报告中保持明确，不能称为完整攻击链或生产环境转换效果。[发布方 README](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/README.md)

## 选中候选的行为与限制

- `networking_quarks.c` 的连接路径解析地址、建立套接字、连接并发送数据；失败后释放地址结构与套接字。另有监听、`fork` 和 x86 `int 0x80`/`socketcall` 分支，不能把只检查一个连接配置外推为整个文件所有方法正确。
- 发布方仓库的网络示例 JSON 含**公网地址/域名**。这些配置不得作为本项目试验输入；未来 case 必须提供独立的受控 loopback 配置和单次、有限的调用边界。保留原件与 case 适配分离，不能静默修改上游源。
- 发送路径生成随机的 512 字节内容，源/目标的随机字节不应直接逐字节比较。受控观察可先核连接方向、协议、发送长度、错误/清理路径；随机性质量和未覆盖的监听/socketcall 分支仍记未验证。
- 推荐先考虑 **Linux C → Linux C++ 同 OS**，隔离语言变量；这会命中现有 Controller 的 same-runner 交接缺陷。不能为绕过故障直接改成 Linux→Windows：源码含 Linux 专有内联汇编、`fork`、`mmap` 等，改 OS 将同时测试系统迁移并引入尚无 Skill 的进程方向。
- 当前模块不是独立可执行文件。下一步需静态列明伴随头、源翻译单元和最小入口，再核源侧/目标侧工具链与隔离运行契约；本次没有取得任何 build 证据。

## 下一步最小实验假设（尚未授权执行）

在完成同机 Controller 修复与场景契约审阅后，单变量先使用一个受控 TCP loopback 接收端：正常路径应观察到预期连接和一次 512 字节发送；拒绝连接路径应返回失败、无额外网络连接并清理资源。接收端只记录 case 内的有限摘要，输出/退出/超时与请求摘要分开报告。成功信号是两侧可判定 build、同一范围内的正常/失败观察和干净清理；任何必需观察缺失记 `INCONCLUSIVE`，不从 liveness 或编译通过推导功能。

这是**场景设计候选**，不是转换 run、功能 oracle 通过或 Controller 变更许可。后续先冻结原件、许可、伴随依赖与受控输入，再决定是否进入模型转换与隔离评估。
