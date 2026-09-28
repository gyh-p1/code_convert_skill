# step-03：为 fe 开 C → C++ 转换 run，取双侧 build 证据

> 状态：已生成并自审（`GENERATED` → `SELF_REVIEWED`=`NO-REPAIR-IDENTIFIED`，无自修轮）；编译 `UNVERIFIED`，待可达的获批隔离 VM 取双侧 build 证据（2026-09-28）
> 类型：转换 run 执行（含配置模型生成 + 有限修订；执行按**本项目既定的双侧执行授权**，确无隔离能力则停在文本交付标 `UNVERIFIED`）
> 归属阶段：[最终交付编译质量与 Skill 拓展](阶段方案.md)

## 目标

对已冻结的 [fe 源快照](../../test/sources/fe/source.md)（`fe.c` 879 行 + `fe.h`）按[转换—自审—第三方评估闭环](../../../references/conversion-evaluation-loop.md)产出**最终交付的 C++ 版本**，并取得**双侧 build 证据**：源侧按 C 编译作基线，目标侧按 C++ 编译，用于把失败归因为“源本身编不过”还是“转换引入”。本阶段只把 **build 证据**计入指标，只按最终交付版本记一个逐例编译结论（`pass` / `fail` / `inconclusive` / `UNVERIFIED`），不评功能、不设行为 oracle。

## 纳入范围

- **FROZEN**：登记源快照哈希、源 OS/ABI 假设、目标编译器/SDK/标准、所选 Skill 内容快照（含 step-01 的 header-macro 规则）、提示主体、`.env` 非敏感模型标识与参数、RAG=off、目标文件命名、隔离/授权范围。
- **已确认目标方向**：fe 无平台分支，为隔离“C→C++ 语言对”本身的编译信号，取**同一目标 OS**（不做跨 OS 迁移），源按 **C11** → 目标按 **C++17**。为统一走双侧执行且源默认翻译单元无 `main`，**采用形态 B：定义 `FE_STANDALONE` 补入 REPL `main`**，两侧链接为可运行程序。具体 OS/标准/编译器已在 [case.md](../../test/cases/fe-lisp-c-to-cpp/case.md) 与 [frozen-inputs.md](../../test/cases/fe-lisp-c-to-cpp/output/no-rag/run-01/01-frozen/frozen-inputs.md) 冻结。
- **GENERATED → SELF_REVIEWED → SELF_REPAIRED（≤2）**：用 `.env` 配置模型把 `fe.c` 转为单个 `.cpp`；模型自评/repair 预判只作提交门槛，**不是语法结论**，不贴 `syntaxPassed`。保存各稿与差异。
- **编译证据获取路径（统一双侧执行）**：交获批隔离 VM 的 comparison capsule，用 `-DFE_STANDALONE` 构建并运行源侧（C11 基线）与目标侧（C++17）；本阶段只读取其 **build 证据**，execution/comparison 结果不计入功能率、不设行为 oracle。capsule 内以固定无害输入启动（无参数 stdin 立即 EOF 或 case 私有无害脚本），结束即销毁。
- **EVALUATED**：按[三方结果分流](../../../references/conversion-evaluation-loop.md)（基础设施 / 工具链不匹配 / 源端 build 失败 / 目标 build 失败 / build 成功但运行 / 全匹配）读结论，优先读 build 证据；每个结论附到准确版本与工具链。
- **交付**：`result.md` 按[中文报告骨架](../../../references/delivery-handoff-contract.md)先答交付、语法/编译、功能三项结论；产物落点/命名按[交付契约 §2.2](../../../references/delivery-handoff-contract.md)（`01-frozen/`、`02-conversion/`、`03-self-review/`、`04-evaluation/`，`target.gen` / `target.self-repair-<N>` / `target.eval-repair-<N>`）。
- **回补 Skill**：把可归因的编译失败按类别转成有依据的规则（衔接 step-04），不把工具链噪音写成转换缺陷。

## 非目标

- 不在本机编译、运行、调用构建脚本或触发代码生成。
- 不评功能正确率、不设/不比对行为 oracle；不把 build 通过说成功能或安全正确。
- fe 不占四例跨 OS × 场景试点格子；不把本 run 结果倒填为 C01 或任何正式基线。
- 不为凑“通过”把修订稿成功回写成原始生成稿成功。

## 依赖与前置

- 已具备：step-02（fe 已冻结）、step-01（header-macro 规则可被模型/审阅引用）。
- **必须先取得**：确认的目标工具链 + 获批隔离 VM（本项目既定双侧执行授权）+ 匹配的 comparison capsule 契约。确无隔离能力 → 停在文本交付、标 `UNVERIFIED`，不本机编译或运行。
- 已知风险：C01 run-02 曾因 `.env` 当前模型名被 API 拒绝导致模型自评未完成；本 run 须先验证模型可用，不可用则如实记录、不伪造自评。

## 预计改动文件

- 新建 case 目录 `docs/test/cases/fe-lisp-c-to-cpp/`：`case.md`（冻结条件与目标声明）+ `output/no-rag/run-01/`（各稿、诊断、`result.md`）+ 按 §2.2 的子目录。
- `docs/test/four-case-matrix.md`：把 fe 关联到该 case（登记，不改其“非四例格子”定性）。
- `docs/stages/final-output-compile/index.md`：更新进度。

## 验收依据（人工检查）

- 最终交付版本有**唯一**逐例编译结论，且附目标标准/OS/架构/编译器/SDK 与命令；源侧 C 基线结论分开记录。
- 模型自评、第三方编译、（若有）行为证据分开存放分开汇报；无第三方结果处写 `AWAITING-THIRD-PARTY-COMPILE` / `UNVERIFIED`，未把自评写成语法通过。
- `result.md` 三项结论齐全，功能项明确写“未评估”；中间诊断在过程文件，不进正文结论。
- 若无授权/契约：全流程只到文本交付 + `UNVERIFIED`，仓库无本机编译/运行痕迹。

## 风险与停止条件

- 模型不可用或返回截断/空 → 记录，按相同输入最多重试一次，不换模型、不伪造自评。
- 自审 2 轮仍有可定位转换缺陷 → `SELF_REVIEW_UNRESOLVED`，停止，不无限循环。
- 确无隔离能力或无匹配 capsule 契约 → 停，标 `UNVERIFIED`，不改用本机编译，不在边界外擅自运行。
- 源侧 C 基线就编不过 → 记 `源端 build 失败`，先查源/环境/工具链，不算作转换引入缺陷。
- 工具链噪音（如为进入某分支伪造编译器宏）须单独记为探查，不写成 MSVC/其它工具链的成功或失败。
