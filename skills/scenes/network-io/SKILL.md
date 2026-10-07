---
name: network-io
description: Use alongside a matching conversion direction when source code performs socket or protocol I/O and the translation must preserve byte-stream, message, timeout, and connection semantics. This is not an independent language conversion direction.
---

# 网络 I/O 场景：转换语义

本场景只在源码确有网络 I/O 行为时与方向 Skill **共同阅读**。它不按关键字或 ATT&CK 标签单独判定行为，也不提供通信目标、隐蔽能力或攻击流程。先确认源/目标平台、流式或报文式接口、同步/非同步模式及调用方协议；未知时保留不确定性。

源码是网络攻防相关代码、且转换可能改变可观察安全行为（路径穿越、不可信输入解析、校验/认证、抗 DoS 上限、解码顺序）时，按需加载 [网络安全行为专题](references/security-behavior.md)：它讲如何在转换中保持源程序原有安全姿态，不新增攻防能力。

## 转换时保留的决策边界

| 源码依赖 | 应保留或确认 | 常见误改 |
|---|---|---|
| 二进制缓冲区、显式长度与帧格式 | 字节序、长度计算、分隔/长度前缀、编码、空字节处理 | 把任意字节转成文本、假设一次读取就是一条完整消息 |
| `send`/`recv` 等流式接口 | 返回的实际字节数、部分发送/接收、EOF、错误及重试条件 | 将一次调用等同于完整发送或完整消息；把 0 字节和错误混为一谈 |
| 连接与超时状态 | 阻塞/非阻塞设置、超时范围、连接关闭、半关闭、资源释放顺序 | 把持续会话变成单次请求，或静默增加无限重试 |
| 已有上层协议或 TLS | 原有字段、验证与失败条件、请求/响应时序 | 擅自去掉校验、改变协议，或添加源码没有的通信能力 |

TCP 提供字节流，不保证应用消息与一次 `send`/`recv` 一一对应；Winsock `send` 的成功返回值也可能小于请求长度。具体函数错误码、零长度语义和关闭行为必须按源平台 API 与目标平台分别核对，不能把 POSIX、Winsock 和 Python 的返回约定混写成同一条规则。见下方来源。

## HTTP 响应生命周期

源码在循环中发出 HTTP 请求时，响应体属于必须显式管理的资源；它同时影响连接复用、内存上限和停机行为：

- 每个成功或失败分支都要关闭/释放响应体；不要依赖循环结束后才执行的延迟清理。
- 若目标库要复用连接，按库规则读取到 EOF 或受控上限；有界读取达到上限**不等于**已读到 EOF。
- 保留源码的响应大小预算、读取上限、超时和取消策略；不得为“清理方便”偷偷强加短超时或无限读取。
- 错误响应也属于可观察结果：状态码、响应头、错误体和解析失败要按源码语义分类。
- 循环内创建资源时，优先把“一次请求/响应”封装成有明确作用域的单元，使异常路径和提前返回同样释放资源。

上述规则适用于 Go `net/http`、C# `HttpClient`/`HttpResponseMessage`、Python `requests`/`http.client` 等高层客户端；具体目标库的关闭与复用条件仍须按其版本文档冻结。

## L2-NET-01 协议层默认附加内容属于义务

**触发条件**：源码生成或解析 HTTP（或等价文本协议）报文，且响应/请求头由**库默认行为**产生——状态行、`Server`/`Date`/`Content-Length`/`Content-Type`/`Connection` 等头，或依赖**头顺序**的可观察字节。


**义务**：

1. **库自动附加的头是义务**：不得把目标库无条件添加的头当成“实现细节”。典型：Python `BaseHTTPRequestHandler.send_response()` **无条件**附加 `Server: BaseHTTP/<ver> Python/<x.y>`，而 Go `net/http` 只写 `Date`（无 body 时另有 `Content-Length: 0`）。二者字节不同。
2. **`Connection:` 语义不得臆造**：HTTP/1.1 默认持久连接，是否发送 `Connection: close` 取决于源框架的决策；目标手写该头属**新增可观察行为**。反过来源若显式关闭连接，目标也必须关闭。
3. **头顺序可能是字节级差异**：某些库按**键排序**写头（如 Go `net/http` 会排序），某些按插入顺序。若下游对报文做字节比较或哈希，顺序差异即行为差异。
4. **解析侧的默认行为同样属义务**：是否跟随重定向、可接受的 3xx 集合、超时默认值、错误响应是否算失败，都属于可观察行为，不得按目标库默认值替代。见[容器/集合语义的方向侧规则](../../directions/)。

**错误机械替换反例**：

```python
# 源（Go）：net/http 只写 Date（无 body 时另有 Content-Length: 0），不写 Server 头
# 目标（错误）：直接继承 Python 标准库的默认行为
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)      # 无条件附加 Server: BaseHTTP/... Python/3.12
        self.end_headers()
        # 响应字节与源不同，且下游若做报文比较即失败
```
```cpp
// 目标（错误之二）：手写源里并不存在的 Connection 头
resp += "Connection: close\r\n";     // Go 源保持 HTTP/1.1 连接且不发该头
// 目标（错误之三）：按插入顺序写头，而源库按键排序
resp += "Date: ...\r\nContent-Type: ...\r\nContent-Length: ...\r\n";  // 顺序与源不同
```

**不适用条件**：源码使用裸字节构造报文且不依赖任何库默认行为时，头部集合完全由源码决定，此时只需保持源码写出的字节，不涉及“默认头”问题。源码显式设置的头也不属默认行为。

**信息不足时的处理**：无法确认源框架写出的完整头集合与顺序时，标为“协议默认头与头顺序待确认”，并把原始报文列入 oracle 观察点；不得用目标库默认输出充当依据。

**官方依据**：[RFC 9110（HTTP 语义）](https://www.rfc-editor.org/rfc/rfc9110.html)、[RFC 9112（HTTP/1.1 报文与连接管理）](https://www.rfc-editor.org/rfc/rfc9112.html)；[Go `net/http`（头排序与默认头）](https://pkg.go.dev/net/http)；[Python `BaseHTTPRequestHandler.send_response`](https://docs.python.org/3.12/library/http.server.html#http.server.BaseHTTPRequestHandler.send_response)。


## L2-NET-02 匹配集合与成员集合的扩大/收窄必须逐项对照

**触发条件**：源码用**库提供的集合语义**做判定，而不是显式枚举——如“响应是否属于重定向类”“该地址是否属内部/私有网段”“该协议/状态码是否可接受”。典型形态：对目标库的一个谓词或类判定直接替换源库的谓词。


**义务**：

1. **谓词不是等价物，集合才是**：目标库的同类谓词**很少**与源库的集合完全相同。必须把源库的集合**逐项列出**，再核对目标谓词覆盖的集合，而不是把两个谓词当作同一件事。
2. **扩大与收窄都要报告**：目标集合比源**大**（多接受）与比源**小**（少接受）都是行为差异，方向相反但同样必须登记。
3. **典型已知差异（必须逐项核对，不得默认一致）**：

   | 判定 | 源集合 | 目标谓词 | 差异 |
   |---|---|---|---|
   | HTTP 重定向 | Python `requests` 只跟随 **301/302/303/307/308** | Ruby `Net::HTTPRedirection` 匹配**全部 3xx** | 目标**扩大**：带 `Location` 的 300/304/305 会被目标跟随，源返回原响应 |
   | 私有/内部地址 | 按冻结的 CPython **补丁版本**读取 `is_private` 集合与例外；`100.64.0.0/10` 的 `is_private` 为 false | Ruby `IPAddr#private?` 主要是 RFC1918 与 IPv6 ULA；还须核对源码组合的 loopback/link-local | 部分特殊用途地址可能被收窄，但不能把全部 IANA 段都列为 private；`192.0.0.0/24` 还存在版本变化与地址例外 |

4. **两个方向都必须给出显式集合或登记差异**：能改成显式枚举的（`[301, 302, 303, 307, 308].include?(code)`）就改；不能改的必须写入已知差异清单并评估下游影响。

**错误机械替换反例**：

```ruby
# 错误：用目标库的类判定直接替换源库的显式集合
if response.is_a?(Net::HTTPRedirection)      # 覆盖全部 3xx，比源 requests 宽
  # 300/304/305 若带 Location，源不会走到这里
end
# 错误之二：用目标库的谓词替换源的谓词，未核对集合
internal = ip.private? || ip.loopback? || ip.link_local?
# 不得从“IANA 特殊用途”直接推断 private；100.64.0.1 不是差异正例

# 正确：显式枚举源的集合
if [301, 302, 303, 307, 308].include?(response.code.to_i)
```

**不适用条件**：源码本就以**显式枚举**表达判定（自己写出状态码列表、网段列表）时，集合由源码固定，只需逐项搬运，不存在“库谓词覆盖范围”问题。

**信息不足时的处理**：无法确定源库谓词覆盖的确切集合时，标为“匹配集合待逐项核对”，并把该判定列为 oracle 观察点；**不得**把“名字相近的谓词”当作同一集合。

**官方依据**：[Python `requests`（重定向与 `TooManyRedirects`）](https://requests.readthedocs.io/en/latest/user/quickstart/#redirection-and-history)、[Python `ipaddress`（`is_private` 与特殊用途段）](https://docs.python.org/3.12/library/ipaddress.html)、[IANA IPv4 特殊用途地址登记表](https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml)；[Ruby `Net::HTTPRedirection`](https://docs.ruby-lang.org/en/3.4/Net/HTTPRedirection.html)、[Ruby `IPAddr#private?`](https://docs.ruby-lang.org/en/3.4/IPAddr.html#method-i-private-3F)。



## 具体语言转换的高频陷阱

### C → Python 网络 I/O

- **字节与文本隔离**：C `recv(buf, len, ...)` 接收的是原始字节，必须映射为 Python `socket.recv(bufsize)` 返回 `bytes`，**严禁直接转为 `str`**；若需文本，显式 `.decode('utf-8')`，并处理 `UnicodeDecodeError`。
- **部分接收循环**：C 语言常用 `while (total < expected) { n = recv(...); total += n; }` 循环接收完整消息；Python 同样需要循环 `data = b''; while len(data) < expected: chunk = sock.recv(expected - len(data)); data += chunk`，不能假设一次 `recv` 读满。
- **错误码与异常**：C 的 `recv` 返回 `-1` 并设置 `errno`；Python `socket.recv` 抛出 `OSError` 或子类（如 `ConnectionResetError`、`TimeoutError`），必须用 `try/except` 捕获，不能检查返回值。

### C → Go 网络 I/O

- **`net.Conn` 接口与错误**：C 的 `send`/`recv` 返回字节数或 `-1`；Go 的 `conn.Read(buf)` 和 `conn.Write(buf)` 返回 `(n int, err error)`，**必须检查 `err != nil`**，即使 `n > 0` 也可能有错误（如部分写入后连接断开）。
- **EOF 语义**：C 的 `recv` 返回 `0` 表示对端关闭；Go 的 `Read` 返回 `io.EOF` 错误；转换时必须将 `recv() == 0` 映射为 `err == io.EOF` 的检查。
- **阻塞与超时**：C 用 `setsockopt(SO_RCVTIMEO)` 或 `select`/`poll` 设置超时；Go 用 `conn.SetReadDeadline(time.Now().Add(timeout))`；两者超时错误类型不同（C 返回 `EAGAIN`/`EWOULDBLOCK`，Go 返回 `os.ErrDeadlineExceeded`）。

### Python → C 网络 I/O

- **`bytes` 到 `char*` 与长度**：Python `socket.recv()` 返回的 `bytes` 可能含嵌入 `\0`，转 C 时必须传递显式长度 `(const char* data, size_t len)`，**严禁用 `strlen(data)` 计算长度**（会在首个 `\0` 处截断）。
- **异常到错误码**：Python 的 `socket.send(data)` 抛出异常；C 必须捕获异常并转为返回值 `int send_wrapper(...) { try { sock.send(data); return 0; } catch (...) { return -1; } }`（伪代码，实际需用 Python C API）。
- **GIL 与阻塞调用**：Python 的阻塞 socket 操作会释放 GIL；若用 C 扩展包装 Python socket，必须正确使用 `Py_BEGIN_ALLOW_THREADS` / `Py_END_ALLOW_THREADS` 避免死锁。

### Python → Go 网络 I/O

- **空 `bytes` 与 EOF**：Python `recv()` 返回 `b''` 表示对端有序关闭；Go 必须同时判定 `n == 0` 与 `err == io.EOF`。**不得只检查 `err != nil` 就当成错误**，也不得把 `io.EOF` 与 `net.Error` 归为同一类故障。
- **超时到 Deadline**：Python `settimeout(0)` 是非阻塞、`settimeout(None)` 是无限阻塞、正数是每次调用的超时；Go 对应概念只有绝对时刻的 `SetDeadline`/`SetReadDeadline`（`time.Time{}` 表示不设截止），且 Deadline 只对设置之后的操作生效、超时后不会自行重置——**必须在每次操作前重设**。
- **异常到错误返回值**：Python `ConnectionResetError`、`TimeoutError`、`socket.gaierror` 都源自异常；Go 侧需用 `errors.Is`/`errors.As` 对 `io.EOF`、`os.ErrDeadlineExceeded`、`*net.OpError` 分类，不要把名称相似者视为同一错误类别。

### Go → Python 网络 I/O

- **`io.Reader` 读语义**：Go `conn.Read` 可能在一次调用中读出少于请求的字节；映射为 Python `socket.recv` 时同样需要循环收满或按帧长解析，**不得把一次 `Read` 当成一条完整消息**。
- **`n > 0` 与 `err != nil` 并存**：Go 允许本次读/写返回正数字节数同时给出错误；拆解为 Python 时必须先处理已收到的字节，再按错误类型决定抛异常还是结束，避免丢弃有效数据。
- **`Close` 语义**：Go `net.Conn.Close` 可并发调用且第二次起返回错误；Python `socket.close()` 幂等且关闭后句柄失效。转换时不要把"重复关闭报错"当成需要保留的行为，也不要依赖 Go 的关闭唤醒阻塞读（Python 侧行为需按目标平台核对）。

### PowerShell → Python 网络 I/O

- **`TcpClient`/`NetworkStream` 到 `socket`**：`.Read()` 返回 `0` 表示已到流末尾（对端关闭），映射为 Python `recv()` 的 `b''` 并结束循环；`.Write()` 不返回已写字节数，而 Python `send()` 返回实际发送量——**短写的循环条件不能照抄**，且写超时/中断的异常类型两边不同。
- **流包装与文本层**：源码使用 `StreamReader`/`StreamWriter`（文本层，编码与换行按构造参数而定，例如 `new StreamWriter(path)` 在 .NET 8 下默认 UTF-8 无 BOM）时，转换必须保留文本层语义（含读取到行尾与编码）；**不能直接降级为裸字节读写**，反之裸流也不能被悄悄套上文本编码。
- **`.Dispose()` 到 `with`**：`TcpClient`/`NetworkStream`/`StreamReader` 在 PowerShell 中依赖显式 `.Dispose()`；Python 侧应使用 `with` 或 `try/finally` 保证在异常路径同样关闭，不得依赖 GC 时机。

### C# → Python 网络 I/O

- **`Receive` 返回 0 表示关闭**：`Socket.Receive` 返回 `0` 是正常的有序关闭，不是错误；对应 Python `recv()` 返回 `b''`。**不得映射为异常或无限重试**。
- **`NetworkStream.Read` 与 `Socket.Receive` 语差**：`NetworkStream.Read` 在远端关闭时返回 `0`，但在连接被重置等情况下抛出 `IOException`；Python 侧需分别对应 `b''` 与 `OSError` 子类，不能把两者合并成同一条错误路径。
- **异步到同步的取舍**：C# `BeginReceive`/`ReceiveAsync`/`Task` 形式若在 Python 中改为阻塞 `recv()`，只是调用形态改变；必须确认源程序是否依赖同时处理多个连接或取消。**不得把并发模型静默降级为串行**。

> 上述语言对只是当前有依据的高频差异；Ruby、C# ⇄ 其他方向的套接字细节尚未成文，遇到时按缺口报告，不据其他语言对推断等价。

## 与方向 Skill 的组合

方向 Skill 负责语言/API 映射，本场景只补充网络可观察语义和不应丢失的条件。冲突时不要直接照搬某个示例：先保留源程序的协议/状态条件，指出平台差异及缺少的依据，再给出有条件的转换。ATT&CK 战术可以作为检索标签，但不能替代代码中实际的 I/O 行为分析。

源与目标跨越 Linux/POSIX 与 Windows 且源码含套接字调用时，再加载 [POSIX ↔ Winsock 套接字系统方向](../../systems/posix-winsock/SKILL.md)：本场景管字节流/协议语义，该系统方向管两平台套接字 API（句柄类型、初始化、关闭、错误模型、非阻塞、超时、信号）的差异与不可映射项。

不得运行来源不明的网络样本或连接真实服务；当前仅对规则和转换文本做静态工作。不能根据本文件宣称转换行为已验证。

## 依据

- [RFC 9293（TCP）](https://www.rfc-editor.org/rfc/rfc9293.html)：TCP 字节流与分段语义。
- [Microsoft Winsock `send`](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-send)：返回字节数、错误与平台特定行为。
- [Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)：流式 socket 的部分收发与消息边界。仅用于相关目标语言；其他平台要查各自的权威文档。
- [Go `net` 包](https://pkg.go.dev/net)：`Conn.Read`/`Write` 的返回值、`SetDeadline` 一次性绝对时刻与错误分类。
- [Python `socket` 模块](https://docs.python.org/3.12/library/socket.html)：`recv` 空字节、超时与异常类型。
- [.NET `Socket.Receive`](https://learn.microsoft.com/en-us/dotnet/api/system.net.sockets.socket.receive)、[`NetworkStream.Read`](https://learn.microsoft.com/en-us/dotnet/api/system.net.sockets.networkstream.read)：返回 0 与异常的分工。
- [PowerShell `about_Automatic_Variables`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables) 与 [.NET `TcpClient`](https://learn.microsoft.com/en-us/dotnet/api/system.net.sockets.tcpclient)：流包装、释放与原生调用边界。
