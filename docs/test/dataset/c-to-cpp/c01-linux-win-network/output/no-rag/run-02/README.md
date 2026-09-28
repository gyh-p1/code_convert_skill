# C01 · uhttpd · configured-model run-02

> 历史状态：原固定四例方案已[取消](../../../../../../../stages/four-case-cancellation.md)；本 run 的模型响应、修订与第三方回传保留，不能倒填为正式基线。

本目录保存 2026-09-26 通过仓库 `.env` 配置模型调度生成的第二份文本转换结果。它是独立于 `run-01` 的探索 run，不是正式 No-RAG 基线。

本 run 的产物已按[交付与移交契约 §2.2](../../../../../../../../references/framework/delivery-handoff-contract.md) 的阶段布局归位（run 根只放最终交付物，过程产物进阶段子目录）；此前的扁平命名（`target.pre-repair.cpp`、`model-self-review-*.json`、`third-party-evaluator-adapter/remote-*|pocc-*|repair-01-*` 等）已迁移到下表位置。

## 目录布局

| 位置 | 内容 |
|---|---|
| `target.cpp` | 当前交付稿（= repair-01 单行修订版本） |
| `result.md` | 交付说明：完成范围、模型自评、第三方 job 与有限行为结果 |
| `source-analysis.md` | 源码画像、标签、Skill 选择、目标分支选择与样例限制 |
| `evaluator_manifest.json` | 移交清单；路径指针已指向本布局实际落点 |
| `01-frozen/frozen-inputs.md` | 冻结输入记录 |
| `02-conversion/target.gen.cpp` | 配置模型 pre-eval 稿（含首次生成 + 同模型修订 + constness 决策；中间稿未单独快照），元数据见同 stem `target.gen.*.json` |
| `02-conversion/target.eval-repair-1.cpp` | 第三方诊断后的单行修复稿（已同步为当前 `target.cpp`），提案/元数据/来源见同 stem `target.eval-repair-1.*.json` |
| `03-self-review/self-review-1.*` | 结构化自评结论、澄清决策、调用元数据与失败尝试 |
| `04-evaluation/job-01-initial-probe/` | Job A `eval-…-b10a6e2f`：初次 `-D_MSC_VER` 探查（目标构建失败） |
| `04-evaluation/job-02-branch-diagnostic/` | Job B `eval-…-8c9beb3a`：`-D__POCC__` 单变量诊断（定位 `min` 未声明） |
| `04-evaluation/job-03-repair-verified/` | Job C `eval-…-e96bf2ee`：修复稿构建/运行成功、有限 oracle 匹配；含 `source/`、`target/`、`capsule.zip` |

## 角色边界

| 环节 | 当前责任 | 产物/状态 |
|---|---|---|
| 源码画像与 Skill 选择 | 转换 Agent 静态调度 | `source-analysis.md` |
| 模型转换 | `.env` 配置的外部模型 | `target.cpp`（历史稿见 `02-conversion/`） |
| 交付与移交 | 转换 Agent | `result.md`、`evaluator_manifest.json` |
| 编译、运行、oracle 判定 | 已在隔离第三方 VM 执行 | 当前 manifest `executionApproved=true`；历史模型请求元数据仍保留 `false` |

模型转换请求使用了 C→C++、长文件、网络 I/O、文件 I/O、并发和系统方向上下文。自评请求仅为判断是否建议 repair；RAG 关闭。自评不是第三方语法评估。

## 当前状态

- 当前 `target.cpp` 为 repair-01 单行修订版本；配置模型 pre-eval 原始稿见 `02-conversion/target.gen.cpp`。修订副本已由第三方 MinGW/UCRT64 C++17 探查 Runner 编译并运行。
- `source-analysis.md` 记录源码画像、标签、Skill 选择、目标分支选择和样例限制。
- `result.md` 记录模型自评、第三方 Job A/B/C 诊断、修订和有限行为结果；完整证据归档于 `04-evaluation/`。
- `02-conversion/target.gen.model.json`、`target.gen.revision.model.json`、`target.gen.constness.json` 记录 pre-eval 转换轮次；`03-self-review/self-review-1.attempt-1-failed.json` 记录无效模型名的首次失败。当前模型自评最终经同模型澄清为 `NO-REPAIR-IDENTIFIED`；原始自评、重试元数据、最终元数据与澄清分开保存在 `03-self-review/`。该结论不是第三方语法 verdict；不记录 API 密钥。
- 本机未编译、未运行源码、目标代码、构建脚本或服务；全部动态工作均由获授权的隔离第三方 VM 执行。
