# Chain Reactor 网络模块源码画像（run-01）

> 证据等级：人工静态审阅，不是编译/行为验证。源与契约见[case.md](../../../case.md)及[冻结输入](01-frozen/frozen-inputs.md)。

## 文件、方向与知识选择

- 拟转换单元：上游 `networking_quarks.c` 559 LF 物理行，固定提交 `51c25c4c9dfdc73085c35882d6bbb58e56c006a7`、MIT；完整哈希见[源快照](../../../../../../sources/chain-reactor-network/source.md)。伴随 `atoms.h`、`util.h`、原样 C `util.c` 与本 case `driver.c` 不并入目标单文件。
- 方向与场景：Linux x64 C → Linux x64 GNU C++17，网络 I/O；同 OS，无跨 OS 映射。ATT&CK 不能仅由 socket/API 推断，记录 `none`。按需读取 C→C++ 方向、网络 I/O 场景、长单文件工作流、头文件/宏与类型/C ABI 专题；监听分支使用 `fork`，但本 case 不调用，进程系统方向仍无项目 Skill。

## 结构与行为地图

| 部分 | 源范围/关键符号 | 任务关系 |
|---|---|---|
| 网络方法包装 | `x86_int0x80`、`socketcall_*`、`create_socket`、`connect_socket` | 完整翻译单元必须保留；case 只走普通 socket IPv4/TCP，x86 `socketcall` 分支未做行为验证 |
| 发送与资源 | `send_data` → `urand`（`util.c`）→ 单次 `send`/`sendto` | 从 `/dev/urandom` 尝试填 512 字节；没有完整读取/短写重试。输出比较记录实际接收长度，不比随机字节 |
| 受控入口 | `quark_connect` | case `driver.c` 固定 127.0.0.1、一次调用；地址解析→建 socket→连接→发送→释放 addrinfo/关闭 socket；正常/拒绝/源异常义务见 case.md |
| 其它分支 | `quark_listen`、`fork`、accept/recv 等 | 存在于完整目标文件，但本 case 不运行；不能用受控连接的结果外推完整攻击链 |

`util.c` 还定义复制/删除等行为，case 入口不调用；目标仍需与其 `urand` C 符号正确链接。`atoms.h` 含 C flexible array，GNU C++17 兼容性及目标 `quark_connect` 的 C 链接待第三方编译。源的 `urand` 无显式返回/读取检查、`quark_connect` 的 socket 创建失败返回值风险均属原件现状，不因转换“顺手修复”。

## 生成稿静态核对

配置模型首次稿保留连接、监听与 `socketcall` 函数及主要控制分支；相对原件主要增加 `<stdint.h>`/`<limits.h>`、原样 `util.h` 的 C 链接声明、`quark_connect`/`quark_listen` 的 `extern "C"`、指针经 `intptr_t` 到 `int` 的显式转换，以及 C++ `switch` 作用域花括号。模型自审 `NO-REPAIR-IDENTIFIED`、0 个可定位 issue，仅是预检；它同时登记其它全局 `socketcall_*` 名称链接变化、C flexible array 与原有整数截断等风险。冻结入口只从 C 调用 `quark_connect`，其它外部 C 调用者及完整网络功能**未验证**。首次稿与交付稿同一 SHA-256 `d8b539ab65057befecc5620ee5b79fda7bbadf81356712adaa804034d99159fd`。
