# C01 · run-02 · 配置模型转换输入记录

> 状态：exploration draft；`.env` 配置模型生成目标；用户于 2026-09-26 明确授权在独立 VM 进行第三方 comparison 运行。该 run 不是正式 No-RAG 基线。

## 1. 输入与目标

- 源文件：`docs/test/sources/uhttpd/uhttpd.c`
- 源快照：PJO2/uhttpd，commit `59d17b86ec9f2a70ce1f4369b4c148824be55155`
- 源语言/系统：C / Linux x64，按 POSIX `UNIX` 分支理解
- 目标语言/系统：C++ / Windows x64
- 目标工具链假设：MSVC-compatible C++17；未编译验证
- 任务模式：长单文件文本转换探索
- 场景：`network-io`、`file-io`、`concurrency`
- ATT&CK tactic/technique：`none`
- RAG：关闭

## 2. 调度上下文

模型、API 地址和温度由根目录 `.env` 提供；密钥不写入任何交付文件。模型请求上下文包括：

1. 长单文件转换工作流；
2. C → C++ 语言方向；
3. 网络 I/O、文件 I/O、并发场景；
4. POSIX ↔ Winsock、POSIX ↔ Windows 文件路径、POSIX ↔ Windows 线程系统方向；
5. ATT&CK 分类索引和安全边界；
6. C01 run-01 的 `source-analysis.md` 静态画像（不含 run-01 目标代码）；
7. 原始 `uhttpd.c` 源码。

请求没有把 `run-01/target.cpp` 作为输入；生成目标位于本目录 `target.cpp`。

## 3. 模型输出约束

- 输出完整单文件 `target.cpp`，不输出 Markdown fence、解释或省略号；
- 选择上游源码已有的 Windows 目标分支；
- 保留 HTTP、socket、文件读取、错误和线程行为；
- 不新增进程执行、外联目标、权限或隐蔽能力；
- 不把未编译/未运行的结果描述为通过或等价。

## 4. 交付状态

- 模型首次和完整修订均返回完整文本，`finish_reason=stop`；随后同一模型确认 C++ constness 修订；
- 目标文本、请求摘要和 token 元数据见本目录；
- 原始目标在 MinGW 探查构建失败；repair-01 变体后来在同类 Runner 构建成功，有限 output 行为 oracle 匹配；完整行为/安全仍 `UNVERIFIED`；
- `executionApproved=true` 仅记录用户对独立 VM 第三方执行的授权；不在本机编译或运行。
