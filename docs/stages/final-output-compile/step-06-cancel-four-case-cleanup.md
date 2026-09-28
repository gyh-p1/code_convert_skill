# step-06：取消四例专项并整理测试资料

> 状态：已完成（用户明确取消四例任务；活动文档与测试目录已整理，C01 历史证据保留）
> 归属：[阶段 index](index.md)

## 目标

撤销原 C01–C04 四例无 RAG/RAG 配对测试计划，清除“暂缓、将来重启”的活动措辞和不再使用的候选规格；保留已经发生的 C01 探索 run 及所有真实证据。让 `docs/test/` 只展示当前数据集、仍有用途的候选和被现有 run 引用的源快照。

## 纳入与非目标

- 纳入：阶段路线、业务能力、开发规范、安全边界、Skill 入口及转换闭环中与四例计划相关的状态；测试目录入口、C01/fe 文档引用；`cases/` 与 `sources/` 结构。
- 将原四例设计浓缩为一份**取消记录**，删除没有转换 run 的 C02–C04 规格和冗余的四例阶段方案/矩阵，不把 C01 的历史探索稿改称正式基线。
- 将仍有用的长文件结构候选移到 `docs/test/candidates/`；`sources/` 保持共享快照目录并建立用途索引。七份现有源均被已有 run 引用，不删源码或许可证。
- 不修改任何目标代码、模型原始响应、Controller 回传、capsule、上游源快照或 Skill 的转换规则；不运行测试样本。
- 本步骤只取消**固定四例任务**，不推断用户要求永久禁止未来任何 RAG 研究或长文件验证；未来若要新试验须另立方案，不能恢复本次四例。

## 依赖与前置

1. 核对当前工作树和用户既有未提交迁移；保留 `docs/test/dataset/c-to-cpp/c01-linux-win-network/` 的 run-01/run-02 原样。
2. 核实 C02–C04 各只有 `case.md`、没有源码或转换 run；核实 `sources/` 七份快照仍有 dataset case 消费。
3. 移动 `long-file-structure-candidate` 前验证源/目标绝对路径都在本仓库 `docs/test/` 内；不覆盖目标。

## 预计改动

- 增加 `docs/stages/four-case-cancellation.md`，记录取消决定、四个任务状态、C01 已有探索证据的存留位置、不得继续配对的边界。
- 删除旧 `stage-02-pilot-preparation.md`、`stage-03-no-rag-baseline.md`、`stage-04-rag-comparison.md`、`stage-05-follow-up.md` 和 `docs/test/four-case-matrix.md`；其仍有效的事实迁入取消记录、现有数据集索引或源资料。
- 删除 `docs/test/cases/c02-win-linux-network/`、`c03-linux-win-filesystem/`、`c04-win-linux-process/` 三个仅规格目录；移动 `long-file-structure-candidate/` 至 `docs/test/candidates/`，移除空的 `cases/`。
- 增加 `docs/test/sources/README.md`，逐一标明七份快照的来源说明、消费者与当前用途；修改 uhttpd/fe 的 `source.md` 中依赖旧矩阵或 C02 的叙述。
- 更新相关活动入口与 Markdown 引用；历史 run 的冻结输入和原始第三方证据保持原样。若历史文本仍提“四例”，标为当时任务语境而非当前计划。

## 验收依据

1. 活动路线与能力文档明确写“四例专项已取消”，不存在“暂缓、准备重启四例”的行动项。
2. `docs/test/candidates/` 只有长文件结构候选；`docs/test/sources/` 七份原始快照和许可保持，索引能定位各自 dataset 消费者。
3. C02–C04 规格目录与旧四例矩阵/阶段方案不再是当前文件；C01 探索 run 的源码、目标与第三方证据仍可由数据集索引访问。
4. 活动 Markdown 本地链接静态检查无因本次改动新引入的失效项；保留的上游 README 自有缺链单独说明。`git diff --check` 无空白错误。
5. 仅报告文本/目录检查；没有编译或运行样本，不把静态整理称为转换效果验证。

## 风险与停止条件

- 若发现 C02–C04 目录有未盘点的源、run 或外部消费者，停止删除并回到本方案修订。
- 若某份 `sources/` 快照无现有消费者，先记录为历史资料再决定去留；不为整洁直接删来源或许可。
- 若移动候选导致冻结证据哈希或不可修复的路径依赖变化，停止该移动；保留原数据并在入口标识状态。

## 完成记录与未验证部分

- [取消记录](../four-case-cancellation.md)已建立；旧阶段 02–05 四份专项文件、四例矩阵和 C02–C04 三个仅规格目录已移除。当前路线、业务/开发/安全文档、Codex 薄入口及转换闭环已改为“固定四例已取消”，不保留重启行动项。
- 长文件结构候选移至[`docs/test/candidates/`](../../test/candidates/long-file-structure-candidate/case.md)，其 C 源与 C++ 草稿相对移动前 Git blob 相同；说明文件只改取消语境。`docs/test/sources/` 七份源快照及许可证均保留，新增[源索引](../../test/sources/README.md)逐一指向已有数据集消费者。
- C01 run-01/run-02 的目标代码、第三方 job 与原始证据仍在[数据集](../../test/dataset/c-to-cpp/c01-linux-win-network/case.md)。其活动说明加了历史状态，未倒填为基线或改变原始回传。
- 静态检查：扫描 463 个本地 Markdown 链接，除未改动的 fe 上游 README 自带四个缺失 `doc/`/`scripts/` 链接外，没有失效项；`git diff --check` 无空白错误。未编译/运行任何源、目标或旧测试用例，未验证功能效果。
