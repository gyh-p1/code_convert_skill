---
name: posix-winsock-sockets
description: Use as the source-OS -> target-OS layer when converting socket code between POSIX/Linux and Windows/Winsock, together with a language-direction Skill and the network-io scene. Covers handle-type, init, close, error-model, non-blocking, multiplexing, timeout and signal differences that are not 1:1. Not a language mapping and not a portability or behavior guarantee.
---

# POSIX ↔ Winsock 套接字系统方向

本 Skill 是**系统方向**知识（源 OS → 目标 OS）中套接字层的一份，仅覆盖 POSIX/Linux 与 Windows/Winsock 之间的套接字 API 差异。它与语言方向 Skill（如 [C → C++](../../directions/c-to-cpp/SKILL.md)）和 [网络 I/O 场景](../../scenes/network-io/SKILL.md) **共同阅读**：语言方向负责语法/类型映射，网络场景负责协议与字节流语义，本 Skill 只负责两个平台套接字接口的差异与不可映射项。它是静态的规则与风险说明，不保证目标代码可编译、可移植或行为等价。

## 触发条件与前提

- **触发**：源码确有套接字调用（`socket`/`bind`/`listen`/`accept`/`connect`/`send`/`recv`/`select` 等），且源 OS 与目标 OS 跨越 POSIX/Linux 与 Windows 边界。同平台转换不使用本 Skill。
- **前提**：先确认源/目标 OS、目标工具链与 SDK 版本、目标 Winsock 版本（通常 Winsock 2）、是否 IPv6、是否非阻塞/多路复用、是否多线程。这些不明且影响决策时先询问或标记为待确认，不用"看起来相近"的 API 直接替换。
- 方向必须区分：Linux C → Windows C++（C01）与 Windows C → Linux C++（C02）的补全项不同，见下方不对称陷阱。

## 应始终保留的可观察行为

转换只改平台接口，不改这些语义；无法在目标平台保持时须显式说明，不静默降级：

- 连接生命周期：`accept`/`connect` 的时序、半关闭（`shutdown` 方向）、关闭顺序与资源释放点。
- 每次 `send`/`recv` 的**实际字节数**、部分收发、EOF（`recv` 返回 0）与错误的区分（见网络场景）。
- 阻塞/非阻塞模式、超时范围与单位、重试条件；不得把有限重试改成无限重试或反之。
- 错误分类：连接被对端重置、拒绝、超时、被中断等类别在目标平台的对应表现；错误码数值与名称不同，须按类别映射而非按数字照抄。
- 监听地址/端口绑定约束、`SO_REUSEADDR` 等选项的实际效果（同名选项跨平台语义可能不同）。

## 核心差异映射表

转换时按此表落地；每行给出必须动手改的点，而非"相近即可"。

| 主题 | POSIX/Linux | Windows/Winsock | 转换必须处理的点 |
|---|---|---|---|
| 库初始化 | 无需初始化 | 使用前 `WSAStartup`，结束 `WSACleanup` | → Windows 须补初始化并检查失败；缺失时调用返回 `WSANOTINITIALISED` |
| 句柄类型 | 文件描述符 `int`，无效值 `-1` | `SOCKET`（无符号整型），无效值 `INVALID_SOCKET` | `SOCKET` 无符号，`sock < 0` 判错在 Windows 恒为假；须比较 `INVALID_SOCKET`/`SOCKET_ERROR` |
| 关闭 | `close(fd)` | `closesocket(s)`；`close` 不适用于套接字 | 机械保留 `close` 在 Windows 无法关闭套接字，句柄泄漏 |
| 关闭方向常量 | `SHUT_RD`/`SHUT_WR`/`SHUT_RDWR` | `SD_RECEIVE`/`SD_SEND`/`SD_BOTH` | 数值可能相同但名称不同；按语义映射 |
| 取错误码 | `errno` + `strerror` | `WSAGetLastError()`；不设置 `errno` | Winsock 不写 `errno`；转换后继续读 `errno` 会读到过期/无关值 |
| 典型错误名 | `EWOULDBLOCK`/`EAGAIN`、`EINTR`、`ECONNRESET`、`EINPROGRESS` | `WSAEWOULDBLOCK`、（无同义 `EINTR`）、`WSAECONNRESET`、`WSAEWOULDBLOCK`（非阻塞 connect） | 非 1:1；`EINTR` 式信号中断在 Windows 不出现，非阻塞 connect 进行中用 `WSAEWOULDBLOCK` 而非 `EINPROGRESS` |
| recv/send 签名 | `ssize_t recv(int, void*, size_t, int)` | `int recv(SOCKET, char*, int, int)` | 缓冲区 `char*`、长度为有符号 `int`（有上限）；`size_t` 大缓冲区须检查截断 |
| 错误返回值 | 返回 `-1` | 多数返回 `SOCKET_ERROR`(=-1)，`socket()` 失败返回 `INVALID_SOCKET` | 判错分两类：`INVALID_SOCKET` 与 `SOCKET_ERROR` 各有适用函数 |
| 非阻塞设置 | `fcntl(fd,F_SETFL,O_NONBLOCK)` 或 `ioctl` | `ioctlsocket(s,FIONBIO,&mode)`；套接字上 `fcntl` 不可用 | 保持模式切换时机；不要丢失其他 `fcntl` 标志位处理 |
| 多路复用 | `select`/`poll`/`epoll`(Linux) | `select`/`WSAPoll`（无 `epoll`） | `fd_set` 结构不同（见不对称）；`epoll` 无直接等价，须重新设计或标注缺口，IOCP 是不同范式 |
| 收/发超时 | `SO_RCVTIMEO`/`SO_SNDTIMEO` 取 `struct timeval` | 同名选项取 `DWORD` 毫秒 | 选项名相同，参数类型与单位不同；机械复制会改变超时值 |
| 头文件/链接 | `<sys/socket.h>`,`<netinet/in.h>`,`<arpa/inet.h>`,`<unistd.h>`,`<netdb.h>` | `<winsock2.h>`,`<ws2tcpip.h>`；链接 `ws2_32.lib`；须在 `<windows.h>` 前包含 | 包含顺序错误会与旧 `winsock.h` 冲突 |
| 字节序/地址转换 | `htons`/`htonl`/`inet_pton`/`inet_ntop` | 同名可用（`winsock2.h`/`ws2tcpip.h`） | 通常可保留；仍按目标 SDK 确认可用性 |

## 方向不对称的陷阱

这些不是对称替换，按转换方向单独处理：

- **POSIX → Windows（如 C01）**：新增 `WSAStartup`/`WSACleanup`；`int` 套接字改为 `SOCKET` 并改判错方式；`close`→`closesocket`；`errno`→`WSAGetLastError`。POSIX 的 `SIGPIPE`/`MSG_NOSIGNAL` 处理在 Windows 无对应——Windows 上对已断开连接 `send` 不产生信号而是返回 `WSAECONNRESET`/`WSAECONNABORTED`，须把原信号路径改写成返回值检查，而非直接删除。
- **Windows → POSIX（如 C02）**：删去 `WSAStartup`/`WSACleanup`；`SOCKET`→`int`。**必须评估 `SIGPIPE`**：POSIX 上向已关闭连接 `send` 默认可能以 `SIGPIPE` 终止进程，源 Windows 代码没有该路径，转换后须补 `MSG_NOSIGNAL`、`SO_NOSIGPIPE` 或忽略信号，否则引入源程序没有的崩溃行为。`WSAGetLastError`→`errno`，错误名按类别映射。
- **`select` 的 `fd_set`**：POSIX 中 `fd_set` 是按 fd 数值索引的位集，受 `FD_SETSIZE`（最大 fd 值）限制；Windows 中 `fd_set` 是 `SOCKET` 句柄数组，`FD_SETSIZE` 限制的是句柄个数。两侧对大量连接的行为不同，不能假设同样的 `select` 循环规模安全。
- **`WSAPoll` 与 `poll`**：接口相近但 `WSAPoll` 历史上对非阻塞 connect 失败的上报存在已知差异；不要假定逐字段等价。

## 不在本 Skill 覆盖范围

以下与套接字相邻但属其它维度，须另有知识或显式标注缺口，不在此默认映射：

- 线程/进程 API（`pthread` ↔ Windows 线程、进程创建）——uhttpd 等多线程服务会用到，但属进程/并发系统知识，本 Skill 不覆盖。
- `epoll`/`kqueue` ↔ IOCP 的可扩展 I/O 范式差异：不是 API 换名，是模型重设计，须单独评估并向用户说明。
- TLS/加密库、地址解析策略（`getaddrinfo` 行为细节）、平台特定 socket 选项的完整清单。

## 未知与冲突处理

- 目标 Winsock 版本、SDK、是否 IPv6、并发模型不明时，标为待确认并保留源行为，不预设默认。
- 同名选项/常量跨平台语义冲突时，写清各自边界与依据，保留源程序可观察行为，不把"名字相同"当等价。
- 无法在目标平台保持某行为（如 `epoll` 规模、信号语义）时，明确列为未映射/需重设计，交付说明中标注"未验证"，不制造虚假等价。

## 依据

- [The Open Group Base Specifications Issue 7 / IEEE Std 1003.1（POSIX）](https://pubs.opengroup.org/onlinepubs/9699919799/)：`socket`、`send`/`recv`、`shutdown`、`fcntl`、`select`、`<sys/socket.h>` 与 `errno` 语义。
- [Microsoft Winsock 参考](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/)：`WSAStartup`、`SOCKET`/`INVALID_SOCKET`/`SOCKET_ERROR`、`closesocket`、`ioctlsocket`、`WSAGetLastError`、`recv`/`send` 签名、`setsockopt`（`SO_RCVTIMEO`）。
- [Porting Socket Applications to Winsock](https://learn.microsoft.com/en-us/windows/win32/winsock/porting-socket-applications-to-winsock) 与 [WSAPoll](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-wsapoll)：跨平台移植差异与 `WSAPoll` 行为说明。

以上为语言/平台规则依据，不是特定编译器、SDK 版本或转换结果的验证记录；目标为具体版本时须核对对应文档。同时遵守根入口和 [安全边界](../../../references/safety-boundary.md)。
