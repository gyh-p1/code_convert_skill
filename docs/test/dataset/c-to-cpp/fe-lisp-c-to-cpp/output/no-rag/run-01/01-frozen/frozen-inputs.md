# fe · run-01 · 配置模型转换输入记录（冻结）

> 状态：FROZEN；`.env` 配置模型生成目标；用户 2026-09-28 确认目标方向并选 **B（FE_STANDALONE 可运行）**，为后续统一走 comparison capsule 双侧执行做准备。本 run 属当前编译质量阶段，只把 **build 证据**计入指标，不评功能、不设行为 oracle。
> 归属：[case.md](../../../../case.md) · 阶段 [index step-03](../../../../../../../../stages/final-output-compile/index.md)

## 1. 输入与目标

- 源文件：`docs/test/sources/fe/fe.c`（879 行）+ 同目录 `fe.h`（61 行，编译必需）。
- 源快照：rxi/fe，commit `3efa075`（2020-04-05）；完整性以 sha256 固定：`fe.c`=`3fc7466e9ae2c114e6fdf36410fc8804a20c83d5c21babcaf664567af6276807`、`fe.h`=`4b30a0f26a8a3c186047a5f6ff60779811de5dfa596c2ea9942398cc0034a69e`。
- 源语言/系统：C（**C11**）；**无平台 `#ifdef` 分支**。
- 目标语言/系统：C++（**C++17**）；**同一目标 OS，不做跨 OS 迁移**。
- 任务模式：长单文件文本转换。
- 场景：无网络、无文件系统写、无进程/命令执行。ATT&CK：`none`。RAG：**关闭**。

## 2. 编译/执行形态（决定 = B）

- **定义 `FE_STANDALONE`**：编入 REPL `main`（`fe.c:851`），两侧链接成真实可执行程序，可提交现有 comparison capsule 双侧构建+运行。额外表面：`<setjmp.h>`（`fe.c:839`）与 `main` 中 `fopen(argv[1],"rb")` 读脚本路径（`fe.c:859`）。
- **本阶段只读 build 证据**：capsule 的运行仅为迁就双侧执行契约并为后续统一流程铺路；run/behavior 结果不计入功能率，本 run 不设行为 oracle。
- **运行边界（获批隔离 VM 内）**：以固定无害输入启动——无参数（stdin 立即 EOF，REPL 空跑后 `EXIT_SUCCESS`）或一份 case 私有的无害 Lisp 脚本；不联网、不执行外部命令、不读敏感文件（fe 静态无 `system`/`exec`/`socket`/`unlink`/`remove`）。结束即销毁临时件。

## 3. 目标工具链（冻结，具体版本以实际 Controller 为准）

- 隔离能力：Windows x64 MinGW/UCRT64（沿用 C01 run-02 的第三方 Controller）。
- 源侧（对照基线，按 C）：`gcc -std=c11 -DFE_STANDALONE fe.c -o program`（`fe.h` 同目录）。
- 目标侧（按 C++）：`g++ -std=c++17 -DFE_STANDALONE target.cpp -o program`。
- 编译器/SDK 精确版本、目标架构在提交获批 Controller 时补录本节；若实际能力非 MinGW/UCRT64 则按实际改写，不倒填。

## 4. 调度上下文与模型输出约束

- 模型、API 地址、温度由根目录 `.env` 提供；密钥不写入任何交付文件、manifest 或请求正文。
- **提交前先验证 `.env` 模型可用**（已知风险：C01 run-02 曾因当前模型名被 API 拒绝）；不可用则如实记录、按相同输入最多重试一次，不换模型、不伪造自评或代写模型产物。
- 模型请求上下文：长单文件工作流 + C→C++ 方向 + [header-macro 规则](../../../../../../../../../skills/directions/c-to-cpp/references/header-macro.md) + [type-abi 专题](../../../../../../../../../skills/directions/c-to-cpp/references/type-abi.md)；无网络/文件/并发场景（fe 不触发）。
- 输出约束：完整单文件 `target.cpp`，无 Markdown fence/解释/省略号；保留解释器语义（mark-sweep GC、tagged `union`、宏求值次数、指针算术、聚合初始化）；`FE_STANDALONE` 入口保留；不新增进程执行/外联/权限/隐蔽能力；不把未编译/未运行结果说成通过或等价。

## 5. 授权与落点

- 执行形态按**本项目既定的双侧执行授权**：在获批隔离 VM 做双侧构建+运行，不再逐例询问形态。本 case 的逐例安全前提已确认——源为低风险、无网络/无 exec、无文件写；隔离/工具链/清理仍随本 case、本工具链核对，安全前提确认不扩展到其它样例。`executionApproved` 在实际向隔离 VM 提交 capsule 后才置 `true`。
- 产物落点按[交付契约 §2.2](../../../../../../../../../references/framework/delivery-handoff-contract.md)：本 `01-frozen/` + `02-conversion/target.gen.*` + `03-self-review/` + `04-evaluation/job-<NN>-<用途>/`；run 根 `target.cpp` = 最终交付版本。
- 无匹配契约/授权时停在文本交付并标 `UNVERIFIED`，不在本机编译或运行。
