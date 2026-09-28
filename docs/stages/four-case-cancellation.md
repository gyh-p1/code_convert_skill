# 原四例专项取消记录

> 状态：已取消（用户于 2026-09-28 明确决定不再进行固定 C01–C04 四例测试）
> 范围：原阶段 02 四例准备、阶段 03 无 RAG 基线、阶段 04 RAG 配对和依赖这四例的后续决策。

原方案拟以 C01–C04 做固定四格跨 OS/场景的无 RAG 与 RAG 对照。该方案**不再排期、不继续补四格、也不以其完成情况作为当前 Skill 拓展或功能检测的门槛**。旧阶段方案、四格矩阵和没有转换 run 的候选规格已从活动文档与 `docs/test/` 移除；这里只保留取消决定与历史事实，不提供重启入口。

| 原任务 | 取消时事实 | 保留的历史材料 |
|---|---|---|
| C01：uhttpd Linux C → Windows C++ | 有 run-01 文本探索和 run-02 配置模型探索；run-02 修订稿曾在 MinGW 探查工具链编译，并取得五个固定 loopback 请求的有限输出匹配。源自带 Windows 分支，1,317 行超 700 上限，均非正式四例基线 | [C→C++ 数据集中的 C01](../test/dataset/c-to-cpp/c01-linux-win-network/case.md)及 run/evidence；[uhttpd 源快照](../test/sources/uhttpd/source.md) |
| C02：同一 uhttpd 源的 Windows → Linux 反向任务 | 只有候选规格，无转换 run、编译或功能证据 | 规格已移除；uhttpd 源仍因 C01 使用而保留 |
| C03：Linux → Windows 文件 I/O | 只有拟议 fixture 与 oracle 文字，无源代码或 run | 规格已移除；另有已完成的 stest/realpath/pwd/du 文件系统批次，见[数据集](../test/dataset/c-to-cpp/README.md)，不倒填为 C03 |
| C04：Windows → Linux 进程调用 | 只有拟议 helper/oracle 文字，无源代码或 run | 规格已移除；本项目进程系统方向仍无 Skill |

fe 与 uhttpd 是两份独立长源，但都超过计划的 700 物理行上限；fe 的编译证据属于独立的[当前编译质量阶段](final-output-compile/index.md)，不填入原四例格子。长文件结构 fixture 仍只是[未验证候选](../test/candidates/long-file-structure-candidate/case.md)。

未来如果需要新的真实攻防场景、长文件或检索效果试验，应围绕当时的明确问题重新定义样本、来源/许可、行为义务、目标环境和证据口径；**不能以此取消的四例方案或 C01 旧探索稿直接恢复基线**。现有原始模型响应、转换产物、第三方回传和许可证均保留，取消不改变既有证据等级。
