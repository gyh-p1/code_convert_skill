# C01 · uhttpd · configured-model run-02

本目录保存 2026-09-26 通过仓库 `.env` 配置模型调度生成的第二份文本转换结果。它是独立于 `run-01` 的探索 run，不是正式 No-RAG 基线。

## 角色边界

| 环节 | 当前责任 | 产物/状态 |
|---|---|---|
| 源码画像与 Skill 选择 | 转换 Agent 静态调度 | `source-analysis.md` |
| 模型转换 | `.env` 配置的外部模型 | `target.cpp` |
| 交付与移交 | 转换 Agent | `result.md`、`evaluator_manifest.json` |
| 编译、运行、oracle 判定 | 已在隔离第三方 VM 执行 | 当前 manifest `executionApproved=true`；历史模型请求元数据仍保留 `false` |

模型转换请求使用了 C→C++、长文件、网络 I/O、文件 I/O、并发和系统方向上下文。自评请求仅为判断是否建议 repair；RAG 关闭。自评不是第三方语法评估。

## 当前状态

- 当前 `target.cpp` 为 repair-01 单行修订版本；原始模型稿见 `target.pre-repair.cpp`。修订副本已由第三方 MinGW/UCRT64 C++17 探查 Runner 编译并运行。
- `source-analysis.md` 记录源码画像、标签、Skill 选择、目标分支选择和样例限制。
- `result.md` 记录模型自评、第三方 Job A/B/C 诊断、修订和有限行为结果；完整证据归档于 `third-party-evaluator-adapter/`。
- `model-request-metadata.json`、`model-revision-metadata.json`、`model-constness-decision.json` 记录转换轮次；`model-self-review-attempt.json` 记录无效模型名的首次失败。当前模型自评最终经同模型澄清为 `NO-REPAIR-IDENTIFIED`；原始自评、重试元数据、最终元数据与澄清分开保存。该结论不是第三方语法 verdict；不记录 API 密钥。
- 本机未编译、未运行源码、目标代码、构建脚本或服务；全部动态工作均由获授权的隔离第三方 VM 执行。
