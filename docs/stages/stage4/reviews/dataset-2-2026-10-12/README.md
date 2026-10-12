# 本批审查产物长期归档

> 2026-10-12：从原审查目录完整复制 89 份文件，另存 original-readme.md 与两份 optimization-inputs 汇总。本目录是工程归档，不是产品 Skill 加载入口。

当前状态以[阶段知识收尾](../../knowledge-closeout-2026-10-12.md)、[R11–R16 收尾](../../r11-r16-closeout-2026-10-12.md)和[阶段任务清单](../../tasks/evidence-quality-checklist.md#12-r-11r-16-全部修订完成2026-10-12)为准：R-01–R-16 本批维护完成；全量回归等待用户确认。

提交前状态续接：[全量静态模拟回归§7](../../skill-guidance-loading-regression-2026-10-12.md#7-u01u07-收齐与提交前复查2026-10-12)的U01–U07已文本收齐；[发布准备](../../revision-release-handoff-2026-10-12.md)承接两仓提交与打包。纯Markdown历史审阅资料随工程记录提交，原始harness事件/日志、路径清单和退役副本只保本地，未备份完整案例/源码；旧正文的等待/停止按其原时点理解，不作为新动作指令。

2026-10-12 清理续接：另保存五份旧批次说明，归档共 97 件。旧数据集中的对应七份文档及 89 件审查目录已移出到同级 retired 目录；正式读取从本归档及阶段收尾续接，不从 retired 取现行规则。永久删除命令被安全策略拒绝，当前采用可恢复迁移；详见[清理记录](../../r11-r16-closeout-2026-10-12.md#5-已应用文档的清理2026-10-12)。

- [旧操作说明](operational-discipline.md)：含已废弃/被纠正的要求，只保留历史出处，不授权 JSON 构造器、驱动脚本或改判。
- [Abseil 库单元记录](pattern-note-abseil-library-units.md)、[BSD 原记录](pattern-note-bsd-userland.md)与[后续更正](pattern-note-bsd-userland-macos-correction.md)：有限历史诊断，不外推当前平台或强制所有项遍历 OS。
- [旧 C# 平台阻断记录](platform-blocker-csharp-target.md)：历史问题与回归需求，维护完成不证明新实例已验收。

[上一批问题汇总](optimization-inputs.md)及[剩余问题汇总](optimization-inputs-2.md)已随归档保存。除本导航外，复制报告/事件保持原时点；原 README 另存 original-readme.md。旧数据集路径、外部用例链接及 original-artifact-paths.txt 仅作历史定位；这里没有备份全部用例证据或已删除源码/目标。dataset-2-copy 最终不保留不影响现行知识读取和修订续接，但不能据此宣称旧案例可以复验或原始证据已全部归档。本轮未删除数据集。

## 历史审查导航（状态以阶段记录为准）

审查历史dataset-2-copy工程产物，对照现行转换知识、流程/契约与评估系统。**本轮已阶段收尾，全量逐件验收未完成**。用户2026-10-12确认现有大部分案例的读取归纳已经足够，本轮不再继续补读；不把旧版本问题或有限观察当当前已证实缺陷。

- [本轮收尾、三类优化建议与保留事项](phase-close-2026-10-12.md)
- [优化修订交付与静态回查记录](revision-result-2026-10-12.md)：定向修订已落盘，未验证/回归/部署，等待用户确认全量回归
- [R10完成核对与停止记录](R10-completion-audit-2026-10-12.md)：R1–R10知识维护完成；R10七个子项具体正文与依据已齐，到此停止，未执行验证回归
- [知识归档状态与下一轮修订清单](revision-backlog-2026-10-12.md)：可开始定向修订，优先纠正两处现行方向示例；候选与正式采纳分开

- [全量审查索引及已读范围](full-review-index-2026-10-12.md)
- [DeepSeek harness分工与Codex验收](harness-acceptance-index.md)
- [全部96份正式自审：第1组40份](full-review-self-reviews-01.md)、[第2组56份](full-review-self-reviews-02.md)
- [知识候选的27类维护去向及当前规则问题](full-review-knowledge-disposition.md)
- [消噪、功能比较与matched/semantic_pass统计提案](full-review-comparison-and-statistics.md)
- [D2-001至006完整过程文件审查](full-review-cases-01.md)
- [此前按问题索引抽查的初步报告](optimization-review-current-2026-10-12.md)：保留其有限覆盖说明，不代全量结论

Harness每组任务、真实事件、stderr、逐件覆盖与发现集中存本目录。原optimization-inputs/续篇、batch账本和用例证据留原位，不修改历史原件。

2026-10-12移动原7份审查文件至本目录，初步报告受影响相对链接已逐个修正；34个本地目标用原生Test-Path人工列举核对均存在（含同目录新增索引链接）。只核路径存在，不将其当技术结论验证。未编译、运行或重评样本。
