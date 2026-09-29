# C01 uhttpd 源码画像与 Skill 选择

> 状态：静态探索画像（2026-09-25）；不是安全审计、冻结 oracle、编译结果或行为验证。

## 1. 任务契约与系统画像

| 维度 | 本次选择 | 依据/状态 |
|---|---|---|
| 输入 | `当前 run 的 source/ 冻结副本`，PJO2/uhttpd commit `59d17b86ec9f2a70ce1f4369b4c148824be55155` | 源快照只读；GPL-2.0-or-later 许可证随附 |
| 任务模式 | 单文件、长文件文本级探索 | 输入为 1,317 LF 物理行，超过项目 700 行规划边界；不计入该边界验证 |
| 源语言 → 目标语言 | C → C++ | C 方向知识可用；本次仅做保持行为的最小 C++ 兼容改写 |
| 源系统 → 目标系统 | Linux x64 → Windows x64 | 输入源侧按 `UNIX` 分支理解；目标稿按 `_MSC_VER` Windows 实现分支选择 |
| 编译器/标准 | MSVC-compatible C++17，x64（探索假设） | 源/目标具体编译器、SDK、CRT 版本未冻结，未经编译验证 |
| RAG | 关闭 | 只是本次文本草稿属性，不表示它已成为正式 No-RAG 基线 |

**重要适用性限制：**上游同一 `.c` 文件已经同时包含 POSIX 与 Windows 两套实现。目标稿删除 POSIX 兼容段并使用其现成 Windows 分支，而非从零将 Linux socket/线程/路径实现独立移植到 Windows。因此此例适合探索长文件解读、分支选择与 C→C++ 改写，不适合据此声称验证了模型独立完成 POSIX→Win32 移植的能力；这属于样例构造的目标实现泄漏。

## 2. 证据化场景标签

- **`network-io`（主要）：**`InitSocket`、`BindServiceSocket`、`doLoop` 涉及 socket 初始化、地址解析、bind/listen/select/accept；`HttpTransferThread` 接收 HTTP 请求、发送响应并关闭连接。
- **`file-io`（次要）：**请求路径解析会读取 docroot 内文件；`fopen`、`fread`、`fseek`、`ftell`、`fclose` 实现静态文件服务。源码不创建/覆盖 fixture 文件。
- **`concurrency`：**每个 accepted client 创建一个线程；线程状态登记/回收通过全局链表和 `ThStatus` 协作。
- **未发现进程执行场景：**静态搜索未发现 `system()`、`exec*`、`fork()` 或 `CreateProcess` 调用。`system` 仅出现在 “system library” 注释；`_killthread` 定义中调用 `TerminateThread`，但本文件中未见该包装函数的调用点。

### ATT&CK Enterprise 分类

- **Tactic：`none`；Technique：`none`。**静态观察到的是常规 HTTP 静态文件服务、文件读取和并发处理；没有足够的对抗性用途/行为证据将“HTTP/socket”本身标成 C2、Web Shell 或其他 ATT&CK 技术。
- ATT&CK 索引仅用于分类核对；若后续获得具体威胁场景/调用链证据，应重新审查，不从本次 `none` 外推到其他配置。
- 参考：MITRE [Web Protocols (T1071.001)](https://attack.mitre.org/techniques/T1071/001/) 描述的是对手使用 Web 协议通信的行为；[Web Shell (T1505.003)](https://attack.mitre.org/techniques/T1505/003/) 也不是“程序是 web server”即可匹配。

## 3. 按标签选择的 Skill

| Skill | 选择原因 | 使用边界 |
|---|---|---|
| `skills/workflows/long-file-conversion/SKILL.md` | 1,317 行单文件，需全文件地图和合并核对 | 工作流初稿，未由本项目转换验证 |
| `skills/directions/c-to-cpp/SKILL.md` | C → C++ | 只给映射约束，不证明编译 |
| `skills/scenes/network-io/SKILL.md` | socket/HTTP 收发 | 只按实际 I/O 加载，不因 ATT&CK 标签选择 |
| `skills/scenes/file-io/SKILL.md` | docroot 文件读取和关闭路径 | 不把读取改成写入或扩展 docroot |
| `skills/scenes/concurrency/SKILL.md` | per-connection worker 与共享状态 | 明确指出 `ThStatus` 的同步未见保障 |
| `skills/systems/posix-winsock/SKILL.md` | POSIX socket ↔ Winsock | 目标稿复用源内 Windows 实现，不代表独立映射验证 |
| `skills/systems/posix-windows-filesystem/SKILL.md` | `realpath`/`GetFullPathName` 与当前目录差异 | 路径语义不等价风险须保留为未决项 |
| `skills/systems/posix-windows-threads/SKILL.md` | `pthread`/`_beginthreadex` 生命周期 | 目标稿复用源内 Windows 实现，不代表线程迁移能力已验证 |
| `skills/attack-tactic-index/SKILL.md` | 核对分类和覆盖 | 输出 `none`；不触发 tactic 专属转换规则 |

## 4. 全文件结构与转换覆盖地图

以下位置以只读源 `uhttpd.c` 的 1-based 行号为准；输出 `target.cpp` 保留 HTTP 服务主体并选择 Windows 平台层。

| 源位置 | 符号/职责 | 应保持的行为/主要核对点 |
|---|---|---|
| 1–94 | 许可/版本、CLI 帮助、公共常量与声明 | GPL 头、版本、选项文本 |
| 99–143 | Windows portability layer | Winsock、CRT 线程包装、`Sleep`；目标稿保留 |
| 150–249 | POSIX compatibility layer | `pthread`、POSIX socket/path 包装；目标 Windows 稿移除该段，不改只读源 |
| 262–376 | Settings、HTTP 参数、MIME 映射表 | 默认端口 8080、默认 index、最大线程数等 |
| 382–396 | `LOG` | 日志级别、stderr/stdout 选择与格式 |
| 401–475 | HTTP 状态、请求类型、线程状态、`S_ThreadData` 与全局链表 | 状态与 socket/buffer/FILE* 所有权 |
| 486–510 | `LastErrorText`、socket 初始化辅助 | 错误文本当前混用 Win32/CRT 状态 |
| 510–680 | `InitSocket`、MSS/IPv6 检查、`BindServiceSocket` | WSA 初始化、地址解析、socket 选项、bind/listen |
| 682–710 | `HTTPSendError` | 错误状态/响应头/响应正文 |
| 711–787 | `LogTransfer`、MIME 查询等 | 传输日志、大小写不敏感扩展名查找 |
| 788–899 | `ExtractFileName`、`DecodeHttpRequest` | 只接受 GET/HEAD；URL 到相对文件名；docroot 检查 |
| 904–1027 | `HttpTransferThread` | 请求、读文件、发头/body、错误处理及 cleanup |
| 1043–1078 | `ManageTerminatedThreads` | 等待已退出线程、释放 handle/buffer/file、摘除链表节点 |
| 1081–1136 | `StartHttpThread` | 并发上限、分配每连接状态、启动线程 |
| 1144–1196 | `doLoop` | select 超时、accept、启动 worker |
| 1202–1233 | `Setup`/`Cleanup` | socket 初始化、设置当前目录、资源收尾 |
| 1237–1315 | settings 初始值、`ParseCmdLine`、`main` | 配置入口和无限服务循环 |

## 5. 可观察行为与未决风险

- 服务默认使用 TCP 8080、当前目录、最多 1,024 个连接线程；命令行允许配置监听地址、端口与内容目录。真实运行时必须使用 case 的 loopback、临时高位端口和空白临时 docroot。
- HTTP 仅处理 GET/HEAD；`GET /` 使用 `index.html`；文件按扩展名确定 Content-Type；读取文件并发送内容。响应格式字符串使用 LF (`\n`) 而非标准 CRLF，探索稿不自行“修复”。
- 错误响应包含 400/403/404/405/415/500 等路径。case 的具体 oracle 仍是草案，尤其 415、HEAD、stderr 稳定字段、失败路径和清理条件未冻结。
- 源 POSIX 包装的 `GetFullPathName` 使用 `realpath`；Windows 分支调用 Win32 `GetFullPathName`。后者不是等价的最终文件对象/符号链接验证。`DecodeHttpRequest` 以字符串前缀比较 docroot，不能据此宣称完整路径穿越防护；保留并标风险，不扩大本次改写。
- `ThStatus` 是普通枚举字段，工作线程写、主线程读，静态未发现同步原语；这是源代码既有并发风险。
- `InitSocket` 在 `WSAStartup` 之后把 `iResult` 无条件改写为 `1`，其失败判断因此无法反映真实启动结果；保留源控制流并报告。
- `StartHttpThread` 创建线程失败分支释放 `pCur` 后，函数结尾仍读取 `pCur->ThreadId`；是源代码既有 use-after-free 风险。本次不静默修复，不能据此进入执行验证。
- `main` 是无限循环，后面的 `Cleanup()` 实际不可达；GET 的 `send` 返回值也未校验部分发送。两项均保留并列为差异/风险。
- 未做完整安全审计；没有执行任何代码、构建脚本或编译器。

## 6. 转换前假设与后续验证

1. 探索目标固定为 Windows x64、MSVC-compatible C++17；SDK/CRT 的具体版本后续需在正式 case 契约中冻结。
2. 目标只支持本次选定的 Windows 构建分支；不宣称目标稿仍支持 Linux/macOS。
3. 本稿仅做静态文本改写，不改变服务能力，不新增监听/进程/权限/隐蔽能力；任何运行仍须另行逐例批准。
4. 正式 baseline 前要冻结源和工具链、行为 oracle、隔离启动参数及清理方案；当前 `target.cpp` 不得计作基线结果。
