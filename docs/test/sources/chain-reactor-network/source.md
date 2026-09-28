# Chain Reactor 网络模块源快照

> 状态：上游原件已冻结；**未在本机编译/运行**。当前消费者：[Chain Reactor Linux C→C++ case](../../dataset/c-to-cpp/chain-reactor-network-linux/case.md)。

- 上游：[redcanaryco/chain-reactor](https://github.com/redcanaryco/chain-reactor)，固定提交 `51c25c4c9dfdc73085c35882d6bbb58e56c006a7`；只读检出后逐文件复制，未改写 C 源或头文件。
- 许可：[MIT](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/LICENSE)，本目录保留原 `LICENSE`。
- 主翻译单元：`networking_quarks.c`，559 LF 物理行。伴随 `atoms.h`、`util.h` 和原样 `util.c`；主文件之外的依赖不计入 559 行，不能据此声称完整程序在 700 行内。

| 文件 | SHA-256 | 用途 |
|---|---|---|
| `networking_quarks.c` | `8b8c2f355b0382f19dda088ff2d32fadc9b7b22713df0e87dca2b2330851edf0` | 拟转换的完整 C 翻译单元 |
| `atoms.h` | `6f453c9387fe3db65b090e6a4088a0be8e8e8108b8758bf51d9ddf26f30c0d33` | 参数结构/网络方法常量 |
| `util.h` | `5a412fa44ee28e1fc9ff1b9b12544069ffdeb6ced878e12627367492a49a1be7` | `urand` 与日志宏声明 |
| `util.c` | `b20032a4f5f03822d3e13d610ddb25737e7195e8bb36a26094bd714680935391` | 原样 C 伴随实现；本 case 仅调用其 `urand` |
| `LICENSE` | `5164c453026562b69c32d919cd2ff63d967f097a021390d0d615a09d66aaed2b` | 上游许可文本 |

## 使用边界

上游模块有连接、监听、`fork`、x86 内联汇编与 `socketcall` 分支；本 case 的私有入口只传 loopback IPv4/TCP 普通 socket 路径。上游网络示例含公网目标，**没有复制进本目录，也不得作为运行输入**。`util.c` 含复制/删除函数，入口不得调用。随机缓冲来自 `/dev/urandom`，源码没有完整检查读取；单次 `send` 不保证写满。详细有限行为义务见[case.md](../../dataset/c-to-cpp/chain-reactor-network-linux/case.md)。

本快照不是“已验证转换”或执行授权。未来如需修补上游行为，须另存 case 适配版本并记录 diff；不得直接改本目录原件。正常/拒绝路径义务见[case.md](../../dataset/c-to-cpp/chain-reactor-network-linux/case.md)。
