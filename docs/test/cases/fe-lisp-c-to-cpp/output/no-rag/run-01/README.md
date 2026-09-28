# fe · rxi Lisp · configured-model run-01

本目录保存 2026-09-28 通过仓库 `.env` 配置模型（`deepseek-flash`）调度生成的 `fe.c` → C++ 文本转换结果。这是无 RAG 探索 run，不是正式 No-RAG 基线。产物按[交付与移交契约 §2.2](../../../../../../../references/framework/delivery-handoff-contract.md) 的阶段布局归位（run 根只放最终交付物，过程产物进阶段子目录）。

## 目录布局

| 位置 | 内容 |
|---|---|
| `target.cpp` | 最终交付稿（= `02-conversion/target.gen.cpp`，同 sha256，无自修轮） |
| `result.md` | 交付说明：完成范围、模型自审、编译状态与未决项 |
| `evaluator_manifest.json` | 移交清单；路径指针指向本布局实际落点；`executionApproved=true`（已提交并回传真实证据） |
| `01-frozen/frozen-inputs.md` | 冻结输入记录（源快照哈希、形态 B、工具链、模型参数） |
| `02-conversion/target.gen.*` | 配置模型生成稿及其请求/原始响应/元数据 |
| `03-self-review/self-review-1.*` | 一次结构化自审的请求、原始响应、结构化结论与调用元数据 |
| `_orchestration/` | 本 run 的调度脚本（`generate.py`、`self_review.py`）；密钥不写入任何文件 |

## 角色边界

| 环节 | 当前责任 | 产物/状态 |
|---|---|---|
| 冻结输入与形态决定 | 转换 Agent | `01-frozen/frozen-inputs.md`（形态 B，`FE_STANDALONE`） |
| 模型转换 | `.env` 配置的外部模型 | `02-conversion/target.gen.cpp` → run 根 `target.cpp` |
| 结构化自审 | `.env` 配置的外部模型 | `03-self-review/self-review-1.json`（`NO-REPAIR-IDENTIFIED`） |
| 交付与移交 | 转换 Agent | `result.md`、`evaluator_manifest.json` |
| 编译、运行、oracle 判定 | 已获批隔离第三方 VM Controller | 双侧 capsule 已提交（jobId `eval-20260928-033750-71724720`，`COMPLETED`），真实证据存于 `04-evaluation/job-01-dual-build/returned-evidence/`；`executionApproved=true`，编译 `THIRD-PARTY-COMPILE-PASSED` |

模型转换与自审请求使用了 C→C++、长单文件、头文件/宏、类型/ABI 的知识上下文；RAG 关闭。自审不是第三方语法评估。

## 当前状态

- 阶段进度：`FROZEN` → `GENERATED` → `SELF_REVIEWED`(`NO-REPAIR-IDENTIFIED`) → `EVALUATION_READY` → `EVALUATED`(`THIRD-PARTY-COMPILE-PASSED`) 已完成；`SELF_REPAIRED` 与 `REPAIR_AFTER_EVAL` 均未触发（无编译失败）。双侧 comparison capsule 已于 2026-09-28 经直连 Controller HTTP（`http://192.168.101.250:8443`，`POST /api/jobs`）提交，jobId=`eval-20260928-033750-71724720`，`COMPLETED`，真实回传证据存于 `04-evaluation/job-01-dual-build/returned-evidence/`。
- 生成稿与源逐行 diff 仅 6 处，全部为 C++ 所需 `void*` 显式转换；解释器语义保留。详见 `result.md`。
- 模型自审覆盖 30 个公开函数、`FE_STANDALONE` 入口与全部分支，0 转换引入缺陷，另列 6 项需第三方编译确认的风险——本次目标工具链编译**未触发**其中任何一项的编译错误。该自审结论不是语法 verdict；语法 verdict `PASS` 从 Controller 真实 build 证据回填。
- 本机未编译、未运行源码/目标代码/构建脚本；编译与运行由已授权隔离第三方 VM Controller 执行并回传证据。不记录 API 密钥。
