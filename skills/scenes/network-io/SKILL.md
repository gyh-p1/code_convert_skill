---
name: network-io
description: Use alongside a matching conversion direction when source code performs socket or protocol I/O and the translation must preserve byte-stream, message, timeout, and connection semantics. This is not an independent language conversion direction.
---

# 网络 I/O 场景：转换语义

本场景只在源码确有网络 I/O 行为时与方向 Skill **共同阅读**。它不按关键字或 ATT&CK 标签单独判定行为，也不提供通信目标、隐蔽能力或攻击流程。先确认源/目标平台、流式或报文式接口、同步/非同步模式及调用方协议；未知时保留不确定性。

转换可能改变路径、解析、认证、上限或解码顺序时按需加载[跨场景安全行为](../../references/security-behavior.md)，保持源安全姿态，不新增能力。

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

**官方依据**：RFC 9110（HTTP 语义）、RFC 9112（HTTP/1.1 报文与连接管理）；Go `net/http`（头排序与默认头）；Python `BaseHTTPRequestHandler.send_response`。


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

**官方依据**：Python `requests`（重定向与 `TooManyRedirects`）、Python `ipaddress`（`is_private` 与特殊用途段）、IANA IPv4 特殊用途地址登记表；Ruby `Net::HTTPRedirection`、Ruby `IPAddr#private?`。



## 具体语言转换的高频陷阱

本节保留原导航锚点，具体 API 映射已归入方向页；只加载本项匹配方向，不同时加载全部语言对：

- [C→Python](../../directions/c-to-python/SKILL.md#网络-api-映射)、[C→Go](../../directions/c-to-go/SKILL.md#网络-api-映射)：字节、部分 I/O 与错误。
- [Python→C](../../directions/python-to-c/SKILL.md#网络-api-映射)：独立 C 实现与嵌入 Python 的边界。
- [Python→Go](../../directions/python-to-go/SKILL.md#网络-api-映射)、[Go→Python](../../directions/go-to-python/SKILL.md#网络-api-映射)：EOF、已收字节、Deadline 与关闭。
- [PowerShell→Python](../../directions/powershell-to-python/SKILL.md#网络-api-映射)、[C#→Python](../../directions/csharp-to-python/SKILL.md#网络-api-映射)：.NET 流/异常与 Python socket。

其他语言对缺成文细节时记缺口，不据邻近方向推断等价。平台 socket 细节仍由系统页维护。

## 与方向 Skill 的组合

方向 Skill 负责语言/API 映射，本场景只补充网络可观察语义和不应丢失的条件。冲突时不要直接照搬某个示例：先保留源程序的协议/状态条件，指出平台差异及缺少的依据，再给出有条件的转换。ATT&CK 战术可以作为检索标签，但不能替代代码中实际的 I/O 行为分析。

源与目标跨越 Linux/POSIX 与 Windows 且源码含套接字调用时，再加载 [POSIX ↔ Winsock 套接字系统方向](../../systems/posix-winsock/SKILL.md)：本场景管字节流/协议语义，该系统方向管两平台套接字 API（句柄类型、初始化、关闭、错误模型、非阻塞、超时、信号）的差异与不可映射项。

不得运行来源不明的网络样本或连接真实服务；当前仅对规则和转换文本做静态工作。不能根据本文件宣称转换行为已验证。

## 依据

- RFC 9293（TCP）：TCP 字节流与分段语义。
- Microsoft Winsock `send`：返回字节数、错误与平台特定行为。
- Python Socket Programming HOWTO：流式 socket 的部分收发与消息边界。仅用于相关目标语言；其他平台要查各自的权威文档。
- Go `net` 包：`Conn.Read`/`Write` 的返回值、`SetDeadline` 一次性绝对时刻与错误分类。
- Python `socket` 模块：`recv` 空字节、超时与异常类型。
- .NET `Socket.Receive`、`NetworkStream.Read`：返回 0 与异常的分工。
- PowerShell `about_Automatic_Variables` 与 .NET `TcpClient`：流包装、释放与原生调用边界。

---

**执行顺序受根入口三道硬门禁约束**（分类 `ALLOWED` → 源侧预检（构建 + 适用运行基线）→ 评估就绪核对），见 [AGENTS.md](../../../AGENTS.md) 执行约束 §3。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)；本场景 Skill **不替代门禁、不构成执行授权**。
