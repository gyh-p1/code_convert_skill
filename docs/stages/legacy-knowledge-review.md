# 旧知识库审阅记录

> 状态：工作记录；候选知识不等于已迁移或已验证  
> 记录：2026-09-24  
> 来源：`E:\桌面文档\Code_Convert\apps\translator-mcp\knowledge`（只读盘点，非新项目运行依赖）

## 盘点

共 114 个文件，约 1.16 MB：`skills/` 36、`api_mappings/` 21、`golden_examples/` 16、`auto_generated/` 38，另有 dataset、schema 和根 `CONTRIBUTING.md`。该贡献指南自述部分规则/示例为人工编写，但此处未据此认定其语义正确。旧库的 Markdown 原本由 `skill_composer.ts` 按 frontmatter、触发词、优先级和 token 预算装配，不是可直接移入本项目的独立智能体 Skill。

| 候选 | 可吸收的思想 | 处理 |
|---|---|---|
| `skills/lang/c-to-cpp.md` | 默认保守兼容；不随意改接口、错误路径、文件字节和资源生命周期；`void*`、初始化与标准流边界 | 对照语言标准重写为方向规则，不复制旧的分段/FilePlan/验证流程 |
| `skills/scene/network-c2.md`、`process-execution.md` | 状态、消息/字节边界、超时、参数、退出与清理等语义检查点 | 抽象为可跨方向复用的场景规则；不复制 C2 命令分发或 VM Agent 依赖 |
| `api_mappings/common/c_to_cpp.json` | 所有权、文件 I/O、接口兼容的条件判断 | 逐条核对后吸收。其“转为流/容器/命名空间”的建议不能覆盖保守转换与旧 ABI |
| `golden_examples/`、`datasets/` | 暴露需要解释的边界案例与风险标签 | 仅作候选资料；示例不等于行为证明，不整包导入 |
| `skills/tactic/` | 为检索和适用范围提供研究分类 | 作为标签候选，先核对 ATT&CK 当前名称和语义，不为每个战术复制方向规则 |
| `skills/runtime/`、`evidence/`、`risk/` | 提醒不可运行不可信样本、不伪造验证结果 | 已由当前安全边界覆盖；不恢复远程执行和固定结果契约 |
| `auto_generated/` | 提供待排查的问题线索 | 暂不进入现行 Skill 或未来 RAG 的权威知识库 |

## 系统迁移与旧产品文档的可用信息

- `skills/os/` 有 Windows、Linux、common、cross-platform 四个目标平台片段；`src/config/platform_mappings.ts` 明确列出六个 Windows/Linux/macOS 源→目标组合，说明系统方向应独立于语言方向，而非只记录 `targetOS`。
- `api_mappings/systems/` 有 7 个目标系统下的语言映射 JSON，主要是某个语言对在目标系统上的补充，不等于完整的源 OS → 目标 OS 迁移规则。`arch_mappings.ts` 提醒架构也是附加前提，不能与 OS 混为一个标签。
- 旧 `docs/product/产品范围.md` 和 `docs/architecture/当前实现架构.md` 描述的是旧 Translator + Remote Controller + VM Agent 产品，曾记录无害跨 OS 验收；后续 `docs/product/后续产品能力路线图.md` 又把 C → C++ 的一个同平台样例与跨 OS 失败分别界定。它们有助于识别风险，不把旧产品通过状态继承给新 Skill。
- 旧 `skills/os/common.md` 默认改用 UTF-8、`cross-platform.md` 默认把注册表映射成配置文件、`platform_mappings.ts` 允许权限简化或结构替身，均可能改变源行为。作为**待审候选或显式降级案例**，不能复制为通用“等价”规则。目标系统 API 文档、权限/路径语义和用户容忍的差异都必须先核对。
## 已观察到的质量风险

- `auto_generated/rule_candidates/systems/linux/c_to_cpp.json` 有 6 条、5 个唯一 ID；对应自动生成示例文件也有 6 条、5 个唯一 ID。候选的 `quality_status=passed`，但 `validatedBy=structure`；不能推断编译、动态行为或语义正确。
- 旧库战术文件为 9 个，而本项目已决定跟随 ATT&CK Enterprise 完整当前分类；`defense-evasion.md` 仍标 `TA0005`。当前 [ATT&CK TA0005](https://attack.mitre.org/tactics/TA0005/) 页面名称为 Stealth，不能不核对就沿用旧标签。
- `api_mappings/common/c_to_cpp.json` 的“改为容器/流/命名空间函数”属于条件建议，不是普适等价规则；尤其需检查外部 ABI、字节内容、错误模型和所有权。

## 模型自评、repair 预判与旧仓库经验（2026-09-26 追加）

只读检查了旧仓库 `.cline/skills/convert-code-unit/docs/quality-checklist.md`、转换状态机/移交文档及既有 `local-conversion-artifacts` 汇总；未运行旧工具或样例。可吸收的规则是：**转换前盘点语言/任务单元、入口/数据/控制流/副作用/错误契约；把语法与行为证据分开；C++ 语法检查必须绑定目标标准、编译器、SDK 与平台分支；单纯静态文本扫描不能冒充编译结果**。旧流程中的 VM repair 状态机、detector、自动评分和项目产物机制属于旧运行时，本项目不搬入。

旧仓库报告中 C→C++ 的语法切片在若干批次只有单例，且结果有 syntax=0 与 syntax=1 两种；回归报告出现由 0 到 1 的变化，但这些摘要没有给出足以证明普遍模式的编译诊断上下文。它们只能提示应保留“实际隔离工具链反馈 → 针对性修订 → 再验证”的分层流程，不能把旧样本的通过率或修复结论迁移为本项目能力声明。

此前将模型按自身规则检查代码写成“静态语法预检”是不准确的。模型检查只属于非客观的**自评/repair 预判**，不是独立静态语法检查或 `TEXT-REVIEWED` 证据。语法正确率按用户要求由第三方评估机构编译判定；模型自评不得写成 syntax pass/fail。

据此新增/强化：

- `skills/directions/c-to-cpp/SKILL.md` 的“模型转换后自检与 repair 预判”：覆盖预处理/平台头顺序、C/C++ 指针及初始化规则、声明与调用签名、宏/库声明、长文件完整性和风险分类；模型只建议是否 repair。第三方编译才回填语法结论。
- `skills/workflows/long-file-conversion/SKILL.md` 收尾流程：长文件先由模型自评决定是否建议 repair，再把语法判定交第三方评估机构按目标标准/SDK 编译。
- 当前 run-02 `result.md`：明确模型自评请求因 `.env` 当前模型名被 API 拒绝而未完成；目标疑点仅是先前人工阅读列出的待核风险，不是模型自评或语法结论。
## 结论

采用**选择性提炼 → 查一手依据 → 写明前提 → 人工审阅**，不复制旧索引、优先级、token 预算、整包样例或自动生成状态。当前只有网络 I/O 场景初稿；系统迁移规则与四例试验样本仍待筛选。现已批准后续在安全审阅和隔离条件满足后做无 RAG/RAG 探索比较；截至本记录未运行旧仓库代码或转换样本。
