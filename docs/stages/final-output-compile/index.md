# 阶段执行：最终交付编译质量与 Skill 拓展

> 状态：ACTIVE（本阶段执行进度唯一真源）
> 更新：2026-09-28
> 关系：阶段目标见[阶段方案](阶段方案.md)；步骤约束见[项目开发规范 §6](../../项目开发规范.md)。

## 已确认前提

1. 当前只统计**最终交付目标代码**在声明工具链下的 build 证据。双侧 comparison capsule 在已授权隔离 VM 运行；源 build 用于归因，行为 comparison 目前不计功能率。本机不编译或运行样本。
2. 实样须有来源、许可、冻结的源/目标语言与 OS、工具链、隔离边界。允许真实攻防行为作为候选，但真实目标、真实凭证和未受控外联不进入试验。
3. 700 个物理源代码行仍是计划上限，fe 879 行和 uhttpd 1,317 行都是超限探索，不能据其编译结果宣称计划上限已验收。

## 步骤清单

| 步骤 | 状态 | 证据与结果 |
|---|---|---|
| [step-01 头文件/宏可用性规则](step-01-header-macro-rule.md) | 已完成 | C→C++ header-macro 专题已落盘，C01 单例和语言依据分层 |
| [step-02 选定并冻结第二份独立 C 源](step-02-source-freeze.md) | 已完成 | rxi/fe 879 行源快照及来源/许可已冻结 |
| [step-03 fe C→C++ run](step-03-fe-conversion-run.md) | 已完成 | 最终目标 Windows C++17 build PASS，源基线 PASS；功能未计分 |
| [step-04 POSIX→Windows 文件系统批次](step-04-multisystem-filesystem-batch.md) | 已完成 | stest、realpath、pwd 最终目标 build PASS；du 源基线缺 `libutil.h`，目标跳过、INCONCLUSIVE。该**文件系统批次**的四个 run 均已记录终态，功能未计分；与已取消的 C01–C04 固定四例专项不同 |
| [step-05 数据集归档与真实攻防样例筛选](step-05-dataset-and-realistic-cases.md) | 已完成 | 七个有 run 的 case 已移入 `docs/test/dataset/`；方向索引、旧候选索引和[功能判据草案](functional-detection-criteria.md)已建立。445 个本地 Markdown 链接扫描与 16 份活动 JSON 解析完成，原始证据未执行或改写；范围与限制见步骤记录 |
| [step-06 取消固定四例并整理资料](step-06-cancel-four-case-cleanup.md) | 已完成 | 用户已取消 C01–C04 固定四例无 RAG/RAG 专项；[取消记录](../four-case-cancellation.md)已建立。C02–C04 仅规格目录及旧专项阶段文档/矩阵已移除，长文件 fixture 移至 `docs/test/candidates/`，七份共享源的[用途索引](../../test/sources/README.md)已建立；463 个本地链接扫描无新增缺链，C01 历史证据保留 |
| [step-07 真实网络场景单例闭环](step-07-chain-reactor-network-case.md) | 已完成 | 筛选、契约、转换、取证**在同一步骤续写并闭环**：配置模型完整稿/自审已落盘，Chain Reactor 最终目标 GNU C++17 build **PASS**（Controller job `eval-20260928-123304-add87d9d`，源侧亦 PASS、环境 clean）；受控正常/拒绝两输入的 output 匹配仅信息记录。旧仓库 Windows Agent 排序修复 `7d77158` 本地工程测试 67/67，未部署，RC4 仍 `INCONCLUSIVE` |

后续候选：按 step-04 的可归因事实审阅现有 filesystem 与 C→C++ Skill 改动；为可追溯真实攻防样例冻结行为义务与隔离条件。RC4 的 Windows 文件树哈希排序缺陷在旧仓库独立分支本地修正，远端仍待验收；不在本阶段建设本地运行时。

## 当前证据边界

- **目标编译已证**：fe、stest、realpath、pwd，分别只适用于其记录的最终文件和工具链。C01 run-02 修订稿仅在 MinGW 探查工具链编译通过，非正式 No-RAG 基线。
- **目标编译未知**：du 源基线在 Linux VM 首先失败于缺失 `libutil.h`，Controller 跳过目标；RC4 C→Go 的 Windows 源包两次遇到混合大小写文件身份哈希不匹配，源侧无 bundle、目标从未构建。两者都不是目标代码编译失败。
- **功能未知**：本阶段不计功能率。C01 的五个固定 loopback 请求匹配仅限该探索稿与已观测输出；其他 case 的 liveness matched/mismatched 不证明场景功能。
- **样例代表性缺口**：当前编译 PASS 案例偏保守；不能外推到命令控制、外传、持久化、凭证访问等真实攻防流程。旧测试用例先作为候选池，逐文件核来源/许可与可观察性。

## 下一动作与中断恢复

**当前执行项**：无（step-07 单例已闭环；下一动作按真实失败/知识缺口继续 Skill 拓展）。

三个准备步骤已合并为 step-07，Chain Reactor 的最终目标编译与有限 receiver 观察已由第三方回传，详见[run-01 结果](../../test/dataset/c-to-cpp/chain-reactor-network-linux/output/no-rag/run-01/result.md)。下一动作按本阶段方案审阅 filesystem/C→C++ 与网络 Skill 的证据等级、选下一份真实消费者；Windows Agent 修复的远端部署/RC4 重评属单独基础设施后续，不能因 Chain Linux PASS 倒填。恢复时读本 index → step-07 → run-01 result。
