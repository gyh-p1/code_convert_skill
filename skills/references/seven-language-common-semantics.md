# 七语言共性语义索引

> **职责**：这里仅维护七语言共享事实的导航、事实分类口径与场景/系统分流；实质语义事实按语言各维护一处，不把相同事实复制到 42 个方向 Skill。方向专向映射仍以[根入口](../../SKILL.md)选择的方向 Skill 为准。
> **知识基线**：C11、C++17、C# 12/.NET 8、CPython 3.12、Go 1.27、PowerShell 7.6、CRuby 3.4。它是知识版本，不证明实际目标工具链已安装。
> **证据边界**：本次仅重组既有静态文本；未经逐条技术复核或转换效果验证。若不同来源冲突，回到适用版本的官方标准/运行时文档核对，不因本索引存在便宣称等价。

## 按语言加载

画像确定源→目标方向后，只加载对应的两个语言页，再加载方向专向 Skill；涉及系统行为时按下文加载场景/系统 Skill。

| 语言 | 共享事实 |
|---|---|
| C（ISO C11） | [c](languages/c.md) |
| C++（ISO C++17） | [cpp](languages/cpp.md) |
| C#（C# 12 / .NET 8） | [csharp](languages/csharp.md) |
| Python（CPython 3.12） | [python](languages/python.md) |
| Go（Go 1.27） | [go](languages/go.md) |
| PowerShell（PowerShell 7.6） | [powershell](languages/powershell.md) |
| Ruby（CRuby 3.4） | [ruby](languages/ruby.md) |

## 事实分类

- `[语言规范保证]`：由冻结语言标准、语言规范或官方定义保证的确定性语义。
- `[指定运行时的实现相关事实]`：仅适用于所列运行时/实现的行为，不外推到其他实现。
- `[待专题核验，不可用于确定转换规则]`：缺乏足够的适用版本一手依据，不能作为确定性转换前提。

## 场景与系统分流（何时加载 B 类规则）

> [!IMPORTANT]
> **A 类与 B 类职责边界律**：
> 若源码实际涉及线程、socket、文件或跨 OS API，加载对应 B 类场景/系统 Skill；A 类规则仅说明需要保留的语言层错误、资源、并发、文本或所有权契约。

1. **套接字与网络通信行为**：
   - *源码触发条件*：源码中出现系统网络套接字调用，或各高级语言等价网络库调用（如 Go `net.Dial`, Python `socket.socket`, C# `Socket` / `TcpClient`）。
   - *必须加载的既有 B 类规则*：
     - 通用网络场景：[`skills/scenes/network-io/SKILL.md`](../scenes/network-io/SKILL.md)
     - 涉及 Linux/POSIX 与 Windows 跨系统转换时：[`skills/systems/posix-winsock/SKILL.md`](../systems/posix-winsock/SKILL.md)
   - *语言层核心职责*：保持连接生命周期、错误返回时机、缓冲区所有权与同步/异步阻塞语义；具体 API 结构体填充与平台头文件全部由上述 B 类规则裁定。

2. **文件系统与路径操作行为**：
   - *源码触发条件*：源码中出现底层文件句柄操作、路径拼接分隔符与驱动器解析，或语言层文件读写（如 Go `os.Open`, Python `open()`, C# `FileStream`）。
   - *必须加载的既有 B 类规则*：
     - 通用文件场景：[`skills/scenes/file-io/SKILL.md`](../scenes/file-io/SKILL.md)
     - 涉及 Linux/POSIX 与 Windows 跨系统转换时：[`skills/systems/posix-windows-filesystem/SKILL.md`](../systems/posix-windows-filesystem/SKILL.md)
   - *语言层核心职责*：保证文件句柄在各分支及异常下确定性关闭；确保文本/二进制打开模式与平台换行符（CRLF vs LF）一致；具体路径规范化与目录遍历由 B 类规则裁定。

3. **原生系统线程与并发同步行为**：
   - *源码触发条件*：源码中直接调用底层操作系统原生线程创建、系统事件等待、信号量与进程级同步原语。
   - *必须加载的既有 B 类规则*：
     - 通用并发场景：[`skills/scenes/concurrency/SKILL.md`](../scenes/concurrency/SKILL.md)
     - 涉及 Linux 与 Windows 跨系统转换时：[`skills/systems/posix-windows-threads/SKILL.md`](../systems/posix-windows-threads/SKILL.md)
   - *语言层核心职责*：管理线程生命周期与同步所有权契约，具体 OS 调度与同步原语映射由 B 类规则裁定。
