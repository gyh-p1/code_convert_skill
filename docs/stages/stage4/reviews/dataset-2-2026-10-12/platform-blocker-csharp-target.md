# 平台阻断：C# 目标侧 evidence-bundle schema 缺陷（2026-10-10 发现，影响 38 项）

> ## ✅ 已修复（2026-10-11 复测）
>
> **该缺陷不再复现。C# 目标侧现在可正常构建与执行。**
>
> - 复测：`platform-probes/probe-csharp-target-2026-10-11/`（复用 D2-007 的 cpp→C# dual-build capsule 原样重提）
> - jobId `eval-20261011-122249-fe456bbe` → **`COMPLETED`**；**target build/exec 均 `completed/0`**（windows runner）；**target `collectorDiagnostics=[]`**（不再含非法 `detail`）；目标 preflight **完整通过**。
> - **恢复条件（"平台修复后按原契约重提"）已满足** ⇒ 38 项 C# 目标项可恢复为正常推进，**不必**再记 `WAITING/BLOCKED_ENV`。
>
> ### ⚠ 新纪律（本次复测实证）
> **C# 目标的 `comparison_manifest.json` 中 `target.artifactLanguage` 必须写 `csharp`（与 `dir` 后半一致），不得写 `dotnet`。** 写成 `dotnet` 会在现役 1.0.28 提交端触发 **403 `identity_mismatch`**（`"submitted content does not match the classified content"`）——分类身份本身无误，是 capsule 身份门禁要求 `artifactLanguage` 与方向自洽。runner 侧仍把 `csharp` 映射到 windows runner 的 dotnet 能力（runner `supportedLanguages` 列 `dotnet` 不影响）。`source.artifactLanguage` 同理（如 `cpp`）。

## 一句话

**当前 1.0.26 平台无法完成任何 targetLang=csharp 的评估**：平台 agent 产出的 evidence bundle 含 schema 不允许的字段，导致 job 以 INFRA_ERROR 终止于 CLEANING 阶段，目标侧 preflight **从未尝试**（SKIPPED）。

## 平台原诊断（保留不改写）

- jobStatus: `INFRA_ERROR` ｜ lastError.code: `AGENT_UNAVAILABLE` ｜ owner: **agent** ｜ retryable: true
- message: `agent /run failed: AGENT_EXECUTION_ERROR: EvaluationContractError: invalid codeconvert-evidence-bundle at $.collectorDiagnostics.0: Additional properties are not allowed ('detail' was unexpected)`

## 对照实验（手工，非脚本）

| # | 实验 | targetLang | 结果 |
|---|---|---|---|
| 1 | D2-007 job-00 | csharp | INFRA_ERROR |
| 2 | D2-007 job-00 同 capsule 重提 | csharp | INFRA_ERROR（逐字相同，可复现） |
| 3 | 对照探针：**同形 capsule**，仅目标语言改为已知可用的 c | c | **COMPLETED**（两侧均执行） |

实验 3 与实验 1/2 的源树、驱动、input_profile、manifest 形状**完全相同**，唯一差异是目标语言声明。故故障**专属** csharp 目标路径。

## 责任层

- `collectorDiagnostics` 由**平台侧采集器/agent 生成**；本仓库提交的 capsule **不含**该字段（只有 source/target 树、run_case.py、input_profile.json、metadata.json、comparison_manifest.json）。
- 目标 preflight = SKIPPED（从未尝试构建）→ **不是**编译失败、**不是**代码缺陷、**不是**转换问题。
- 归因：**环境/平台缺陷**。

## 影响面（按 manifest 精确统计）

以 C# 为目标的项共 **38 项**，占 277 项的 **13.7%**：

| 方向 | 项数 |
|---|---:|
| cpp-to-csharp | 12 |
| go-to-csharp | 9 |
| c-to-csharp | 6 |
| python-to-csharp | 6 |
| ruby-to-csharp | 4 |
| powershell-to-csharp | 1 |
| **合计** | **38** |

不受影响：其余 **239 项**（目标语言非 C#），其中 C# 作为**源**语言的方向（csharp-to-c/cpp/go/powershell/python/ruby）目标非 C#，**不受本缺陷影响**。

## 处置

1. **不改目标代码**：故障与代码无关。
2. **不自行改判**：受影响项保留平台原 INFRA_ERROR/blocked/inconclusive，目标侧结论记 UNVERIFIED。
3. **向平台反馈**：需修复 agent 的 evidence-bundle 序列化，使 collectorDiagnostics 的 schema 与产出字段一致（或移除 detail 字段）。
4. **推进顺序调整**：优先推进**非 C# 目标**的 239 项，避免在已知平台缺陷上持续消耗评估往返；受影响的 38 项保持 `WAITING / BLOCKED_ENV`，平台修复后按原契约重提。
5. 按批量规则，某项不满足时跳过并继续其他项，**不因此停整批**；本缺陷不会被计入转换失败或源侧平台不匹配。

## 受影响项的终态口径

- lifecycle: `WAITING`（可恢复，恢复条件 = 平台修复后重提原 capsule）
- blockingReason: `BLOCKED_ENV`
- 不消耗模型调用（D2-007 已确认：0 次模型请求）
- 不计入转换失败，不记源侧 `SOURCE_NOT_BUILDABLE`
