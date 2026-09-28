# 阶段执行：最终交付编译质量与 Skill 拓展

> 状态：ACTIVE（本阶段执行步骤与进展的唯一真源）
> 更新：2026-09-28
> 关系：阶段 WHAT / 为什么见 [阶段方案](阶段方案.md)；本目录只承载“每一步怎么做、做到哪了”。步骤规则见 [项目开发规范 §6](../../项目开发规范.md)。

## 已确认前提（2026-09-27 讨论决定）

1. **编译证据用 comparison capsule 双侧 build**：同时构建源侧与目标侧，源侧 build 作基线，用于归因“源本身就编不过”与“转换引入的编译失败”。本阶段只把 **build 证据**计入指标；execution/comparison 的行为结果不计入功能率（功能 oracle 仍暂缓）。跑双侧属运行代码，按**本项目既定的双侧执行授权**在隔离 VM（已确认有 VM + 可回滚快照）进行，不再逐例询问执行形态；源无可运行入口时默认补写最小入口/驱动。
2. **计分样源放宽**：物理行放宽到 ~900、许可清晰、必须是真正的 C 源（C→C++ 方向）。允许攻击性行为（VM + 快照兜住运行安全），但网络固定 loopback/实验网，不打真实外部目标、不用真实凭证——快照回滚不了已外发的包。
3. **uhttpd 不作首例判据**：1,317 行仍超 ~900 且源自带 Windows 分支（目标分支泄漏），只当超限探索例，不作干净的编译判据首例；仍需一份新的独立 C 源。

## 步骤清单

| 步骤 | 方向 | 状态 | 依赖 | 当前证据 / 下一步 |
|---|---|---|---|---|
| [step-01 头文件/宏可用性规则](step-01-header-macro-rule.md) | c-to-cpp Skill 增补 | 已完成 | 无（用 C01 已有证据） | 已新增 `skills/directions/c-to-cpp/references/header-macro.md` 并在 SKILL「按需专题」加入口；依据分层标注 C01 单例 + 语言标准 |
| [step-02 选定并冻结第二份独立 C 源](step-02-source-freeze.md) | 样例 / 冻结 | 已完成 | 与 step-01 无强依赖 | 用户选定 rxi/fe（`src/fe.c`，879 行，MIT，零平台分支），已冻结于 `docs/test/sources/fe/`（source.md + LICENSE + UPSTREAM-README + fe.c/fe.h），四例矩阵已登记 |
| [step-03 为 fe 开 C→C++ 转换 run，取双侧 build 证据](step-03-fe-conversion-run.md) | 转换 run 执行 | 进行中（已生成+自审，编译 `UNVERIFIED`） | step-01、step-02 | 已完成 `GENERATED`（`.env`=`deepseek-flash` 一次生成，`finish=stop`；与源 diff 仅 6 处 `void*` 显式转换）与 `SELF_REVIEWED`（`NO-REPAIR-IDENTIFIED`，无自修）；已交付 run 根 `target.cpp`、`result.md`、`evaluator_manifest.json`（`executionApproved=false`）。下一步：取得可达的获批隔离 Controller → 提交双侧 build capsule 回填编译结论 |

候选后续步骤（未建文件，进入执行时再创建）：

- step-04：按失败类别更新 Skill，再逐次拓展语言/场景/系统维度。

## 当前状态

- **当前执行项**：step-03 进行中（**已生成 + 自审，编译 `UNVERIFIED`**）。形态 = **B（`FE_STANDALONE` 可运行）**；`GENERATED` 与 `SELF_REVIEWED`(`NO-REPAIR-IDENTIFIED`) 已完成，`SELF_REPAIRED` 未触发。
- **已完成 / 剩余**：step-01、step-02 已完成；step-03 已完成 冻结→生成→自审并交付文本产物，剩第三方双侧 build 证据（`EVALUATION_READY`→`EVALUATED`）。
- **本会话已做（2026-09-28）**：按既定政策由本会话按 `.env` 发起出站调用——`generate.py` 生成 `02-conversion/target.gen.cpp`（`finish=stop`，与源 diff 仅 6 处 C++ 必需 `void*` 显式转换），`self_review.py` 取一次结构化自审（`03-self-review/self-review-1.json`，`NO-REPAIR-IDENTIFIED`，覆盖 30 公开函数+入口+分支，另列 6 项待编译确认风险）；run 根已落 `target.cpp`（= gen 稿同 sha256）、`result.md`、`README.md`、`evaluator_manifest.json`。密钥未写入任何文件。
- **下一动作**：取得可达的获批隔离 Controller（MinGW/UCRT64，`-DFE_STANDALONE`，同目录带 `fe.h`）→ 提交 comparison capsule 双侧构建并运行 → 优先读 build 证据回填 `thirdPartyCompileStatus`、`executionApproved`、`syntaxVerdict`。无匹配契约/授权则保持文本交付并标 `UNVERIFIED`，不本机编译。
- **中断恢复位置**：读本 `index.md` → step-03「已生成+自审，编译 `UNVERIFIED`」→ 读 [result.md](../../test/cases/fe-lisp-c-to-cpp/output/no-rag/run-01/result.md) 与 [evaluator_manifest.json](../../test/cases/fe-lisp-c-to-cpp/output/no-rag/run-01/evaluator_manifest.json)，从第三方双侧 build 这步继续。
