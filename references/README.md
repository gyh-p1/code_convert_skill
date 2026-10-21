# 项目知识与执行参考索引

从[根入口](../SKILL.md)进入。索引只负责路由；规范以表中对应契约为准，短摘要不产生第二份规则。

## 知识：按源码事实加载

| 层 | 入口 | 触发/消费者 | 只负责 |
|---|---|---|---|
| 语言事实 | [七语言共性语义索引](../skills/references/seven-language-common-semantics.md) | 每项源、目标各一页 | 语言自身类型、控制流、资源和通道语义 |
| 方向映射 | [42 方向表](../SKILL.md#选择适用知识) | 每项一个源→目标 | 两种语言差异与映射 |
| 场景 | [根入口场景表](../SKILL.md#选择适用知识) | 实际网络/文件/进程/并发行为，可多选 | 跨语言行为义务 |
| 系统 | [根入口系统表](../SKILL.md#选择适用知识) | 实际平台 API/子系统，可多选 | 平台差异，不由语言方向限定平台 |
| 安全行为共性 | [跨场景安全行为](../skills/references/security-behavior.md) | 网络、文件或认证/边界行为 | 保留源防护语义，不负责执行准入 |
| ATT&CK | [战术索引](../skills/attack-tactic-index/SKILL.md) | 有行为证据需核分类 | 标签和知识定位，不生成规则或授权 |

## 工作流：按任务形态加载

| 文档 | 触发 | 职责 |
|---|---|---|
| [单文件入口](../SKILL.md#按以下顺序执行) | 独立普通单文件；无需批量工作流 | 根入口六步与单项闭环；共享可达性分流/冻结/适用门禁及单项收尾，长/复杂时加读长文件工作流 |
| [单项闭环](workflow/conversion-evaluation-loop.md) | 每项正式转换必读 | 先按可达性分流；可达走分类/源预检/评估，不可达冻结后直接生成/自审/有限修订/收尾；计数与反馈分流 |
| [批量工作流](../skills/workflows/batch-conversion/SKILL.md) | 请求含多项 | 手工串行、接入/恢复、每 40 终态增量对账及终局核对 |
| [长文件工作流](../skills/workflows/long-file-conversion/SKILL.md) | 独立或批次中的长/复杂单文件，建图前加载 | 全文件地图、按容量选择整体或分段、跨单元核对及分支收尾/恢复；两语言页和一个方向仍必读，不重置单项预算 |
| [行为指导](workflow/behavior-preservation-contract.md) | 单文件行为目标/差异说明 | 目标与允许差异建议；提交门禁引用准备契约 |
| [构建前提](workflow/build-prerequisites.md) | 冻结前及源/目标构建必读 | 冻结构建命令、工程/依赖/工具链条件，真实诊断分流 |
| [分类准入](workflow/classifier-agent-gate.md) | 确认评估可达后、冻结/分类前、源预检前、提交/重提必读；不可达仅转换不加载 | 评估运行验收的分类输入、ALLOWED、精确身份及重新分类；不作为仅转换前置，不替代授权/隔离 |

## 契约：所有入口共享的真源

| 文档 | 消费者/时点 | 职责 |
|---|---|---|
| [任务状态](framework/task-state-contract.md) | 开始处理每项即读；冻结/分类、生成/自审/修订与新提交、恢复及收尾核对 | 身份、冻结落盘、当前模型上下文/产物、版本关联、接入去向、变体、phase/lifecycle；验证结论独立 |
| [评估准备](framework/evaluation-readiness-contract.md) | 转换前可达性检查、冻结计划、源预检前、生成前、恢复及双侧提交/取证判读 | 可达正常流程/不可达仅转换自审交付、源构建/适用基线及复用失效、合法来源驱动、四要素、两侧对称、oracle、仅编译和原始/归一化观察 |
| [交付移交](framework/delivery-handoff-contract.md) | 开始处理每项时必读；结束/失败/阻断/暂停前核对 | 统一收尾入口、全去向 result.md、逐件核对/记录、适用件、布局与移交字段来源 |
| [移交模板](framework/evaluator_manifest.example.json) | 消费方要求 manifest 时 | 本仓库清单占位形状，不是 Controller capsule |
| [安全边界](framework/safety-boundary.md) | 全程必读 | 本机/同机/VM、网络、数据及辅助程序红线 |

## 外部适配：使用对应评估渠道时加载

| 文档 | 职责 |
|---|---|
| [Controller 适配](adapter/controller/remote-controller-adapter.md) | 连接、外部 schema、classification/batchAuthorization、手工提交/轮询/取证与未知提交恢复 |
| [Controller 当前协议适配](adapter/controller/platform-revision-adapter.md) | 使用该渠道时随主适配读取；独立源预检/报告 kind、closure/原件、精确 submissionId 与比较配置，提交前核实际平台身份与能力 |
| [比较策略适配](adapter/controller/comparison-policy-adapter.md) | 平台实际字段、策略/维度能力与已知缺口；不承诺通用语义 oracle |
| [评估故障分诊](adapter/controller/evaluation-failure-triage.md) | 拒收、阶段超时、解析空跑、原始观察与归一化疑点的按证据归因；引用现有契约，不新增状态／脚本或必经实验 |
| [Controller 作业恢复适配](adapter/controller/controller-job-recovery-adapter.md) | busy／孤立作业的诊断、管理者授权智能体维护、plan／恢复资格／实际 VM scope、结果与中断核对；不因授权方式增加安装目录访问或样本运行许可 |
| [Runner 能力矩阵](adapter/controller/runner-capability-matrix.md) | 登记组合、能力和组件身份；任务核实际接口/证据 |

语言/方向/场景/系统只提供事实和映射，不替代门禁、工作流或授权；能力与结果以实际接口和精确版本证据为准。
