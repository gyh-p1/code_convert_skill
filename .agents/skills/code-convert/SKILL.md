---
name: code-convert
description: Use for code conversion tasks in this repository. Load the project entry, mandatory task contracts, and matching language, direction, scene, system and workflow knowledge without claiming unverified coverage.
---

# Code Convert — Codex 发现入口

先读取 [AGENTS.md](../../../AGENTS.md) 和仓库根 [SKILL.md](../../../SKILL.md)。必读契约与按事实加载的知识索引以根入口为准。当前智能体模型直接分阶段生成、自审和修订，不单独请求模型。第三方智能体不使用辅助脚本；只可按[分类准入](../../../references/workflow/classifier-agent-gate.md)用原生工具手工逐项调用已登记的 tools/safety_classifier_v2.py，限定获准外部临时目录、精确版本及只读文本分类，不要求额外分类服务。[加载工具](../../../tools/README-loading.md)仍仅由系统维护侧执行；无系统加载支持但完整 manual 核对齐备时可继续核其余门禁，不把强证据不可用当作手工加载未完成。

已确认转换缺陷与评估范围/阻塞分别处理：依根入口及[单项闭环](../../../references/workflow/conversion-evaluation-loop.md)有限修复并核源行为保持；oracle 不可冻结、仅编译或有限 matched 不关闭已定位误译。停止时按交付契约明示未修复/修后未验证，不以 residualRisk 替代。知识与观察范围按源码触发选择，比较能力只据现役适配，不新增驱动、比较器或无限自审。

正式转换必须手工、串行、逐项推进，不写任何辅助脚本/工具/驱动或自动化程序。单文件和批量每项在冻结评估计划前，先按[评估准备 §1.0](../../../references/framework/evaluation-readiness-contract.md#10-转换前可达性检查与仅转换分支)检查第三方评估系统可达性并留原件，首次生成前回读。可达：冻结→分类 ALLOWED→源侧预检（构建 + 适用运行基线）→生成→自审→适用评估→取证/归因→交付门禁。不可达：记 EVALUATOR_UNREACHABLE_CONVERSION_ONLY，冻结→生成→自审/有限修订→交付门禁，不加载分类准入、不调用分类器、不要求分类产物，不编译运行、不提交评估；仍交完整目标、自审记录及 result.md，未开展维度 UNVERIFIED、适用件齐备后 PARTIAL。忙碌/未就绪不是不可达，未决 job 仍 WAITING。可达但本轮无法合法评估行为、源构建通过的，按[评估准备 §1.3](../../../references/framework/evaluation-readiness-contract.md#13-lib_unobservable_compile_only-的转换与交付)记 LIB_UNOBSERVABLE_COMPILE_ONLY，继续生成、自审与目标语法/编译验证，行为未评估/UNVERIFIED。不因缺 main、可执行文件、stdout 或合法入口直接跳过，不补造 main/驱动；冻结和安全边界始终适用，分类只服务评估运行准入。纯文档审阅不触发转换步骤。

冻结完成必须先写出并回读本项本 run 的 `01-frozen/frozen-inputs.md`；缺失、空白、错项/错版本不分类、不推进，不能等收尾补写。源预检、每次生成/自审/修订、提交/重提及恢复新增动作前再核，完整规则只消费[任务状态 §2.2](../../../references/framework/task-state-contract.md#22-冻结落盘门禁)；已发生 job 的查询/取证/终止不因缺件延后。加载工具只检查本项加载条件，不新增平台字段。

按根入口先加载任务状态、构建前提、单项闭环、评估准备、交付与安全六份通用契约；确认评估可达后才补读分类准入。行为评估的驱动四要素和合法来源、本轮行为无法评估时的语法/编译分支只按评估准备契约；收尾按模式/实际阶段核适用件，不伪造未发生 job。显式调用 Skill 不构成运行授权。

开始处理每项即必读[交付契约 §1.1](../../../references/framework/delivery-handoff-contract.md#11-统一收尾入口与报告义务)，不是等生成成功才加载。正常结束、提前失败/阻断、非可转换和 WAITING 暂停统一写本项 result.md，并按实际阶段逐件回读产物、版本及指针，保存核对结果；缺应有件不得终态，暂停报告不解除未知提交/活动或未确认清理。任何提前停止分支都回根步骤 6，不等批次对账才补报告。

冻结条件与实际上下文/知识、当前模型产物/写入、目标、自审及 job 的版本关联按任务状态 §2.1 回查；不要求不存在的模型请求/响应，旧 run 真实调用原件仍保留。源基线复用按评估准备 §1.2，自审格式恢复与有限计数按闭环。当前仓库内容不代历史快照，新稿无独立证据不继承旧稿 PASS；批次阈值按唯一 taskId，不将恢复/重提重复计项。

按根入口六步执行：先读全部必读契约，再画像、选知识、完成冻结，随后按第 5 步调度表逐行推进。多项首项前加载[批量工作流](../../../skills/workflows/batch-conversion/SKILL.md)，长文件建图/分段前加载[长单文件工作流](../../../skills/workflows/long-file-conversion/SKILL.md)，两者可并存。每项必读两语言页与一个方向，场景/系统/安全行为和 ATT&CK 索引按源码事实加载；加载阶段只准备上下文，不提前生成目标。知识可达、实际读取、当前模型上下文已具备和效果验证分别记录，判据见任务状态 §2.3。

能力和证据边界由根入口说明。规则应用不依赖一次性测试数据长期存在。

功能判读及统计按根入口转引的[评估准备§5.1](../../../references/framework/evaluation-readiness-contract.md#51-有效性消噪与功能分类的次序)消费有效性、消噪与分类次序，不只按平台标签计通过；知识映射是按源使用点选择的引导，不追加审阅或动态验证步骤。

使用 Controller 时按根步骤 1 先加载离线连接坐标与健康检查正文，再检查可达性；可达后补分类准入及[当前协议适配](../../../references/adapter/controller/platform-revision-adapter.md)等评估专用正文，在适用源预检/提交前核实际平台身份与能力。不可达仅转换不加载分类准入、不要求实时平台证据；恢复评估前补加载和分类。平台终态标签不免本项适用原件与清理核对。

系统可达的生成前及正常双侧提交前，按[评估准备 §1.4](../../../references/framework/evaluation-readiness-contract.md#14-源预检采信与双侧对齐核对)回读源预检、核输入实际送达与两侧条件；不可达仅转换分支回读 §1.0 原件，不要求源构建。历史占位目标比较不支持转换结论；合法空输出、空参数或预期非零退出按冻结观察判断，不增加非空门槛。

转换知识默认离线消费：只读取随仓库交付的正文和本地参考，网页/资料标题不能代替必需知识；缺语义或版本时记录具体缺口，不靠联网推定覆盖。按根入口加载适用正文，不把出处追溯变成联网步骤。
