---
name: posix-winsock-sockets
description: Use as the source-OS -> target-OS layer when converting socket code between POSIX/Linux and Windows/Winsock, together with a language-direction Skill and the network-io scene. Covers handle-type, init, close, error-model, non-blocking, multiplexing, timeout and signal differences that are not 1:1. Not a language mapping and not a portability or behavior guarantee.
---

# POSIX ↔ Winsock 套接字系统方向

本 Skill 是**系统方向**知识（源 OS → 目标 OS）中套接字层的一份，仅覆盖 POSIX/Linux 与 Windows/Winsock 之间的套接字 API 差异。它与语言方向 Skill（如 [C → C++](../../directions/c-to-cpp/SKILL.md)）和 [网络 I/O 场景](../../scenes/network-io/SKILL.md) **共同阅读**：语言方向负责语法/类型映射，网络场景负责协议与字节流语义，本 Skill 只负责两个平台套接字接口的差异与不可映射项。它是静态的规则与风险说明，不保证目标代码可编译、可移植或行为等价。

## 触发条件与前提

- **触发**：源码确有套接字调用（`socket`/`bind`/`listen`/`accept`/`connect`/`send`/`recv`/`select` 等），且源 OS 与目标 OS 跨越 POSIX/Linux 与 Windows 边界。同平台转换不使用本 Skill。
- **前提**：先确认源/目标 OS、目标工具链与 SDK 版本、目标 Winsock 版本（通常 Winsock 2）、是否 IPv6、是否非阻塞/多路复用、是否多线程。这些不明且影响决策时先询问或标记为待确认，不用"看起来相近"的 API 直接替换。
- 方向必须区分：POSIX → Windows 与 Windows → POSIX 的补全项不同，见下方不对称陷阱。

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

### L2-SOCK-01 句柄类型与位宽常量必须按目标架构取值

**触发条件**：源码在 POSIX 与 Windows 之间搬运套接字句柄或其无效值常量，或在目标侧硬编码句柄/描述符宽度。


**义务**：

1. **无效值比较必须用平台宏**：POSIX 的 fd 无效值是 `-1`（有符号），Windows 的 `SOCKET` **无符号**且无效值是 `INVALID_SOCKET`。因此 `sock < 0` 在 Windows 上**恒为假**，该判错分支会被静默跳过。必须改用 `sock == INVALID_SOCKET` 或 `sock == SOCKET_ERROR`（按函数分别适用）。
2. **不得硬编码句柄宽度**：`INVALID_HANDLE_VALUE`、`INVALID_SOCKET` 等的实际位模式随**目标架构**变化（32 位 vs 64 位）。硬编码单一宽度在另一架构上失效。必须使用平台宏或按 `_WIN64`/`_WIN32` 分支。
3. **签名中的长度类型可能变窄**：Winsock `recv`/`send` 的缓冲区参数是 `char*`、长度是**有符号 `int`**（有上限），而 POSIX 用 `size_t`。把超过 `INT_MAX` 的 `size_t` 直接传入会在目标侧截断或失败，须显式检查。
4. **错误来源不可混用**：Winsock 失败**不设置 `errno`**；转换后继续读 `errno` 会读到过期或无关值。错误必须在产生点用 `WSAGetLastError()` 捕获（参见[并发场景 §L2-CONC-01](../../scenes/concurrency/SKILL.md) 的 last-error 线程局部性义务）。

**错误机械替换反例**：

```cpp
// 错误一：把 POSIX 的有符号判错直接搬进 Windows（恒为假）
SOCKET s = socket(AF_INET, SOCK_STREAM, 0);
if (s < 0) { /* 永远不会进入 */ }

// 错误二：硬编码句柄哨兵值的单一宽度
#define MY_INVALID_HANDLE 0xFFFFFFFFFFFFFFFFULL   // 32 位目标上应为 0xFFFFFFFF

// 错误三：把 size_t 直接传给 int 长度参数
size_t n = huge;
recv(s, buf, n, 0);              // 隐式收窄，可能变成负数或截断

// 正确
if (s == INVALID_SOCKET) { /* 检查 WSAGetLastError() */ }
if (h == INVALID_HANDLE_VALUE) { /* 使用平台宏，不硬编码宽度 */ }
if (n > INT_MAX) { /* 分段或报错，不静默收窄 */ }
```

**不适用条件**：源码始终通过平台宏获取无效值、且长度参数在源侧已知不超过 `INT_MAX` 时，不存在硬编码与收窄问题；同平台转换不适用本 Skill。

**信息不足时的处理**：无法确认目标架构（32/64 位）或目标 Winsock 版本时，标为“目标架构与句柄语义待确认”，并把无效值比较列为 oracle 观察点；不得假定与源侧同宽。

**官方依据**：[Microsoft `SOCKET`/`INVALID_SOCKET`/`SOCKET_ERROR`](https://learn.microsoft.com/en-us/windows/win32/winsock/socket-data-type-2)、[`recv`](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-recv)、[`WSAGetLastError`](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-wsagetlasterror)、[Porting Socket Applications to Winsock](https://learn.microsoft.com/en-us/windows/win32/winsock/porting-socket-applications-to-winsock)；[The Open Group `recv`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/recv.html)。


## 方向不对称的陷阱
这些不是对称替换，按转换方向单独处理：

- **POSIX → Windows**：新增 `WSAStartup`/`WSACleanup`；`int` 套接字改为 `SOCKET` 并改判错方式；`close`→`closesocket`；`errno`→`WSAGetLastError`。POSIX 的 `SIGPIPE`/`MSG_NOSIGNAL` 处理在 Windows 无对应；对已断开连接 `send` 的目标错误路径须按实际 API 结果映射，不得直接删除。
- **Windows → POSIX**：删去 `WSAStartup`/`WSACleanup`；`SOCKET`→`int`。**必须评估 `SIGPIPE`**：POSIX 上向已关闭连接 `send` 默认可能以 `SIGPIPE` 终止进程，源 Windows 代码没有该路径，转换后须按目标 OS 支持情况选择 `MSG_NOSIGNAL`、`SO_NOSIGPIPE` 或信号处理，否则可能引入源程序没有的终止路径。`WSAGetLastError`→`errno`，错误名按类别映射。
- **`select` 的 `fd_set`**：POSIX 中 `fd_set` 是按 fd 数值索引的位集，受 `FD_SETSIZE`（最大 fd 值）限制；Windows 中 `fd_set` 是 `SOCKET` 句柄数组，`FD_SETSIZE` 限制的是句柄个数。两侧对大量连接的行为不同，不能假设同样的 `select` 循环规模安全。
- **`WSAPoll` 与 `poll`**：接口相近但 `WSAPoll` 历史上对非阻塞 connect 失败的上报存在已知差异；不要假定逐字段等价。

## 构建前提（链接与头文件顺序）

本 Skill 的映射表已列出 Windows 侧头文件与 `ws2_32.lib`。**这属于构建前提，必须落到任务契约**：
平台侧的构建命令直接取自契约的 `buildCommand`，不会按语言或平台自动适配，
因此"缺 `ws2_32`"不会自动修正，只会在链接阶段失败。

转换为 Windows/Winsock 时，冻结阶段必须一并确定：

| 前提 | 要求 |
|---|---|
| **链接库** | 构建命令**必须链接 `ws2_32`**（MSVC `ws2_32.lib`；MinGW/GCC `-lws2_32`）。缺失时源内套接字符号无法解析 |
| **头文件顺序** | `<winsock2.h>` **必须在 `<windows.h>` 之前**；顺序错误会与旧 `<winsock.h>` 冲突 |
| **条件编译分支** | 若源用 `#ifdef _WIN32` 分隔平台实现，须确认本次实际编译的分支确实包含套接字实现（否则补链无意义） |
| **其他系统库** | 源同时使用注册表/服务/加密等 API 时，按实际 API 逐项补库，不整包塞入 |

**禁止**：把"源用了 Winsock"当成环境问题记 `BLOCKED_ENV`。它属可事先声明的构建前提，
应在契约中补齐并留证；仅当目标侧**确实没有**该库时才记环境阻断。

**证据边界**：本节来自真实运行中已发生的链接失败（构建命令事后被人工补 `-lws2_32`），
不是对某个 MSVC/MinGW 版本的验证记录。目标工具链为具体版本时须核对其文档。

完整规则（含 C# `.csproj`、Go 工具链版本、构建缓存）见
[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

## 不在本 Skill 覆盖范围

以下与套接字相邻但属其它维度，须另有知识或显式标注缺口，不在此默认映射：

- 线程/进程 API（`pthread` ↔ Windows 线程、进程创建）属进程/并发系统知识，本 Skill 不覆盖。
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

以上为语言/平台规则依据，不是特定编译器、SDK 版本或转换结果的验证记录；目标为具体版本时须核对对应文档。同时遵守根入口和 [安全边界](../../../references/framework/safety-boundary.md)。**执行顺序受根入口三道硬门禁约束**（分类 `ALLOWED` → 源侧构建预检 → 评估就绪核对），见 [AGENTS.md](../../../AGENTS.md) 执行约束 §3。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)；本系统方向 Skill **不替代门禁、不构成执行授权**。
