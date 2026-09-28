# C01 · uhttpd · 文本级转换探索稿交付说明

> 状态：EXPLORATORY DRAFT — 非正式 No-RAG 基线；语法与行为均 **UNVERIFIED**。

## 1. 任务画像

- 源：[`../../../../../sources/uhttpd/uhttpd.c`](../../../../../sources/uhttpd/uhttpd.c)，PJO2/uhttpd commit `59d17b86ec9f2a70ce1f4369b4c148824be55155`，GPL-2.0-or-later。
- 源配置：C / Linux x64，按 POSIX `UNIX` 分支理解；原文件本身还包含 Windows 分支。
- 目标：C++ / Windows x64；MSVC-compatible C++17 是本次探索假设，不是已冻结工具链。
- 场景标签：`network-io`、`file-io`、`concurrency`。
- ATT&CK：tactic/technique `none`；不因 HTTP/socket 服务自动推断攻击战术。
- 任务模式：长单文件文本转换。源 1,317 LF 物理行，目标 1,218 LF 物理行；超出 700 行规划上限，不能作为该上限达标证据。

完整源码地图、Skill 选择依据和已知风险见同目录 [`source-analysis.md`](source-analysis.md)。

## 2. 实际生成范围

已生成完整单文件 [`target.cpp`](target.cpp)。它保留服务器主体及既有 Windows socket/CRT-thread/file API 实现，移除了源文件的 POSIX 兼容层，并做了最低限度的 C++ 兼容改写：

- 明确包含 Windows 头并保持 Winsock 头顺序；增加 `stdarg.h`；
- 使用 C++ 显式转换处理 `_beginthreadex` 句柄、`void*` 参数以及 `malloc`/`calloc`/`realloc` 返回值；
- 将 Windows `getsockopt` 的 `optlen` 局部变量改为 `int`，匹配目标 API 参数类型；
- 将无效 Windows 线程句柄标记为 `nullptr`。

没有有意增加 HTTP 方法、命令执行、出网目标、权限或隐蔽能力；没有按“现代 C++”重写资源模型或线程拓扑。

**样例限制：**上游源文件已经带有 Windows 分支。本稿主要选择并整理该既有实现，而不是独立从 POSIX 实现推导所有 Win32 API；因此它不能证明模型完成了独立的 Linux→Windows 网络/线程/文件系统移植。

## 3. 未解决差异与源代码既有风险

- POSIX 包装的 `realpath` 与目标 `GetFullPathName` 不等价；目标路径检查仍是字符串前缀比较，不能宣称完整防止目录穿越。
- `ThStatus` 跨线程读写未见同步；`StartHttpThread` 失败分支释放状态对象后仍在函数末尾读取该对象，存在 use-after-free 风险。
- `InitSocket` 覆盖了 `WSAStartup` 的原始返回值；GET 发送循环不处理部分 `send`；`main` 的无限循环使后置 `Cleanup()` 不可达。
- Windows socket 错误文本路径调用 `GetLastError()`/`strerror(errno)`，并非一致的 Winsock 错误报告；本稿未改写该源行为。
- 文件路径 ANSI/Unicode 规则、目标 SDK/CRT 精确版本、错误路径与线程回收语义仍需正式任务契约和隔离评估确认。

以上为静态观察，不是完整安全审计。此探索稿保留这些问题并禁止据此直接运行；若未来决定修复，需作为显式行为变更另行记录，不能伪装成纯转换。

## 4. 检查状态

| 检查 | 状态 | 说明 |
|---|---|---|
| 源快照未修改 | 静态检查完成 | 转换只读 `docs/test/sources/uhttpd/uhttpd.c` |
| 目标文件存在/覆盖 | 静态检查完成 | 已生成完整单文件；按源结构与函数地图人工对照，未做 AST/编译器核验 |
| 目标 C++ 语法/编译 | **UNVERIFIED** | 未调用编译器、构建系统或代码生成器 |
| HTTP 行为 oracle | **UNVERIFIED** | oracle 仍为草案，未运行源或目标服务 |
| 安全性/竞态/路径边界 | **未完成审计** | 已记录重点风险，不代表源码安全 |
| 隔离/执行审批 | **未批准** | `executionApproved=false`；不得在本机执行 |

## 5. 继续前必须补齐

1. 正式转换/基线的目标编译器、SDK、CRT/C++ 标准和 Windows x64 环境；
2. C01 静态风险审阅、可判定的 HTTP oracle、临时 docroot 与清理条件；
3. 获批的一次性隔离 VM、出网限制和逐例执行审批；
4. 决定是否接受上游已含目标 Windows 分支的样例泄漏；若要评估独立跨 OS 迁移能力，应另做不泄漏目标实现的输入设计。

目前没有生成语法通过、行为通过或等价结论。移交模板为 `references/framework/evaluator_manifest.example.json`；当前 run 状态见 [`evaluator_manifest.json`](evaluator_manifest.json)。
