# DeepSeek harness 审阅任务 A

用户授权调用 DeepSeek harness 多会话并行，全量审阅此前版本的转换/评估过程材料，Codex负责验收。你只负责静态审阅文本，不执行转换或测试。

工作区：E:/桌面文档/Agents System/code_convert。先读取 AGENTS.md、.agents/skills/code-convert/SKILL.md、根SKILL.md及其纯文档审阅适用契约。本任务并行的是文档审阅，绝不调度转换。

范围：docs/dataset-2/dataset-2-copy 中 manifest.csv 对应 D2-007至D2-080全部74项。D2-001至006已由Codex逐件审阅，不属于你的范围。按manifest逐项定位实际目录，遍历全部现存文件和全部attempt，禁止抽样、只看摘要、只看失败项。原源与目标已删除，不恢复或补写代码。

硬约束：不得编写、生成、保存或运行任何辅助脚本/工具/批量分析程序。只能用原生只读文件工具和rg/Get-Content手工分段阅读。不得运行源码、目标、构建、分类器、模型转换、HTTP评估提交、样本副作用。不得访问 D:/CodeConvertRemote/Stack 或其jobs。不得读取任何.env、密钥、凭证或与本审查无关的私人资料。不得更改原始证据、items/events、原报告、自审与状态。不要复原源码。不要安装软件。审查报告不包含密钥。

每项完整审阅：冻结/分类、源预检、每次请求/响应元数据、失败attempt、自审正文/裁决/修订、所有job输入/接收/两侧原始流与副作用/比较/报告/清理、result/manifest以及对应batch/items记录。响应模型内部reasoning不作自审结论；核真正content、模型身份、finish_reason、用量和正文关联。不把model.json文件名当完整响应。工具输出截断必须补读。空文件/缺失件/只有元数据/已删代码分别登记。

统一逐项记录身份、文件清单及已读/未读/截断状态、独立证据事实、建议定位、当前契约是否已有解决、知识新增候选或错误自审建议、消噪/流程/评估优化和未知。知识侧检查所有建议、risk、scope、unresolved及NO-REPAIR中的疑点，不照信模型断言。来源与当前规则/技术事实分别记录，历史观察不证明当前版本效果。源已有/转换引入/环境/装置/未定分别归因。

消噪与统计提案：有效matched与有效semantic_pass都可进入冻结范围比较通过小计，分别保留数量和覆盖边界。允许扩大跨语言/系统规范化，但保护字段/退出/错误类别/协议/权限/副作用语义；原平台判定不追改，不能将有效局部路径通过误称全功能通过。参阅同目录full-review-comparison-and-statistics.md、full-review-knowledge-disposition.md；这些是审查提案，不是运行授权或新平台能力。

交付目录：docs/dataset-2/dataset-2-copy/batch/current-system-review-2026-10-12/。只新写你独占的harness-a-coverage.md与harness-a-findings.md，需要时按20项拆harness-a-cases-01.md等，勿编辑其它会话文件。coverage必须列74项各自实际目录、现存文件名及读取状态；有未读项明确标PENDING，全部读完才COMPLETE。开始先写进行中索引，每完成20项追加检查点。报告引用必须从本交付目录正确解析至真实材料。

不要为了速度牺牲全量覆盖。遇到上下文不足先保存精确停止点、文件/行号、未读集合，再继续；结束输出已完成项数、覆盖文件数、未读集合和报告路径。不能以“建议下次再看”冒充本轮任务完成。
