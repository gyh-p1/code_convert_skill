# fe：rxi/fe Lisp 解释器 C → C++（当前编译质量阶段）

> 状态：CLOSED（step-03 已取得源、目标双侧 build PASS；功能未计分）
> 归属阶段：[最终交付编译质量与 Skill 拓展](../../../../项目开发规范.md#当前开发阶段与退出条件) · 执行真源 [index](../../../../项目开发规范.md#当前开发阶段与退出条件) step-03
> 共享源样例：`当前 run 的 source/ 冻结副本`（共享源快照已清理；冻结副本见当前 run 的 `source/` 目录）（配 `fe.h`（共享源快照已清理；冻结副本见当前 run 的 `source/` 目录））
> 上游来源与许可：上游来源说明已清理；冻结副本见当前 run 的 `source/` 目录 与随附 MIT `LICENSE`

## 1. 转换方向与标签（已确认）

- 源：C；按 **C11** 理解，**无平台 `#ifdef` 分支**（仅 `<string.h>` + `fe.h`；`fe.h` 含 `<stdlib.h>`/`<stdio.h>`）。
- 目标：C++；**C++17**。**不做跨 OS 迁移**——源侧与目标侧在同一目标 OS 编译，隔离“C→C++ 语言对”本身的编译信号。
- 任务模式：长单文件文本转换（879 物理行，在本阶段 ~900 行放宽范围内）。
- 场景：无网络、无文件系统写、无进程/命令执行；`fe.c` 逻辑密集（`union`、函数指针、宏、指针算术、聚合初始化）——这些是最可能暴露 C→C++ 编译差异的构造。
- ATT&CK tactic/technique：`none`。
- RAG：关闭。
- 目标文件命名与落点：按[交付契约 §2.2](../../../../../references/framework/delivery-handoff-contract.md)（`01-frozen/`、`02-conversion/target.gen.*`、`03-self-review/`、`04-evaluation/`）。

## 2. 目标工具链（拟冻结，待确认具体能力）

- **拟用现有隔离能力**：Windows x64 MinGW/UCRT64（C01 run-02 使用过的第三方 Controller）。形态 B（`FE_STANDALONE`）两侧链接为可执行程序：
  - 源侧（对照基线，按 C）：`gcc -std=c11 -DFE_STANDALONE fe.c -o program`（`fe.h` 同目录）。
  - 目标侧（按 C++）：`g++ -std=c++17 -DFE_STANDALONE target.cpp -o program`。
- 目标 OS/架构、编译器/SDK 精确版本以实际获批 Controller 为准，提交前写入 `01-frozen/frozen-inputs.md`。
- 若实际可用能力不是 MinGW/UCRT64，按实际值改写本节，不倒填。

## 3. 调度与模型输出约束

- 模型、API 地址、温度由根目录 `.env` 提供；密钥不写入任何交付文件。
- 已知风险：C01 run-02 曾因 `.env` 当前模型名被 API 拒绝导致自评失败。本 run **先验证模型可用**；不可用则如实记录、按相同输入最多重试一次、不换模型、不伪造自评或代写模型产物。
- 模型请求上下文：长单文件工作流 + C→C++ 方向 + [header-macro 规则](../../../../../skills/directions/c-to-cpp/references/header-macro.md) + type-abi 专题；无网络/文件/并发场景（fe 不触发）。
- 输出约束：完整单文件、无 Markdown fence/省略号；保留解释器语义（GC、tagged union、宏求值次数）；不新增进程执行/外联/权限；不把未编译结果说成通过或等价。

## 4. 编译/执行形态（已定 = B）

用户 2026-09-28 选 **B：定义 `FE_STANDALONE`，两侧链接为可运行 REPL 程序**，为后续统一走 comparison capsule 双侧执行做准备。`fe.c` 默认翻译单元无 `main`、不可运行，与“双侧执行”冲突；B 编入 `#ifdef FE_STANDALONE` 的 REPL `main`，使 capsule 有可构建+运行的程序。**本阶段仍只读 build 证据**，run/behavior 不计入功能率、不设行为 oracle；capsule 内以固定无害输入启动（无参数 stdin 立即 EOF，或 case 私有无害脚本），结束即销毁。冻结细节见 [`01-frozen/frozen-inputs.md`](output/no-rag/run-01/01-frozen/frozen-inputs.md)。

（被否决的选项 A：不定义 `FE_STANDALONE`、翻译单元只取双侧 build 证据，需 compile-only 契约、comparison capsule 不适用——因用户要与后续统一走双侧执行而不采用。）

## 非目标

- 不在本机编译、运行、调用构建脚本或触发代码生成。
- 不评功能正确率、不设/不比对行为 oracle；build 通过不说成功能或安全正确。
- fe 是独立编译质量 run；不把它倒填为 C01 或正式功能基线。原固定四例专项已[取消](../../../../项目开发规范.md#当前开发阶段与退出条件)。
- 不为凑“通过”把修订稿成功回写成原始生成稿成功。
