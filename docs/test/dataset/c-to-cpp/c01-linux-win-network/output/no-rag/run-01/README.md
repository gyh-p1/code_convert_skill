# C01 · uhttpd · exploration run-01 说明

> 历史状态：本 run 属原固定四例方案的文本探索；该方案已[取消](../../../../../../../stages/four-case-cancellation.md)。下文“后续顺序”是当时记录，不是当前待执行任务。

本目录现在保存一份**文本级探索转换稿**，不是正式冻结的 No-RAG 基线，也没有编译/运行授权。

## 角色边界

| 环节 | 当前责任 | 产物/状态 |
|---|---|---|
| 源码画像与 Skill 选择 | 当前转换 Agent，按项目 Skill 顺序静态审阅 | `source-analysis.md` |
| 任务输入与 oracle | 项目 case 维护；当前仅为草案 | `frozen-inputs.md`、`case.md` |
| 文本转换 | 当前 Codex Agent | `target.cpp`，文本探索稿 |
| 交付说明与移交 | 当前 Codex Agent | `result.md`、`evaluator_manifest.json` |
| 编译、运行、oracle 判定 | 尚未批准/执行 | 只能在之后获批的一次性隔离 VM 完成 |

本目录不提供运行时或转换框架。本机仅做文本读取、编辑和静态检查；不编译或运行源代码、目标代码、构建脚本或其副作用。

## 状态与后续顺序

1. 目前已有 profile、source-analysis、目标文本和未批准 manifest；`executionApproved=false`。
2. 当前稿仅用于探索阅读源码、选 Skill、分段与 C++ 文字改写。由于 oracle 未冻结，它**不得作为 No-RAG 基线或评分结果**。
3. 正式基线前，先冻结源/任务参数、工具链、oracle、隔离启动与清理条件；需要时重新生成正式 No-RAG 输出。
4. 逐例获批后才可交给远程隔离 VM。未审批时不得编译/运行。
5. 正式 No-RAG 基线冻结后，才考虑以相同条件开启 RAG 作比较。

## 本例已知限制

- 源文件本身包含 POSIX 和 Windows 两个平台实现。当前目标稿复用其现成 Windows 分支，存在目标实现泄漏，不足以证明独立 POSIX→Win32 移植能力。
- `pthread`/Win32 thread 与 POSIX/Win32 path 的对应规则现已有专门初稿，但均未经过本项目转换验证。
- `source-analysis.md` 列出的路径检查、共享线程状态、创建失败路径等风险仍未解决；不静默修复，也不据此授权执行。
- `evaluator_manifest.example.json` 的通用模板位于仓库 `references/framework/evaluator_manifest.example.json`；当前 run 的实际清单是本目录 `evaluator_manifest.json`。
