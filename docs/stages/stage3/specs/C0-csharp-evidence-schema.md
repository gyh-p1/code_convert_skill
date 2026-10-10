# C0（最高优先）：修复 C# 目标 evidence-bundle schema 不一致

> 类型：缺陷修复 ｜ 优先级：**P0** ｜ 解封用例：**38 项（13.7%）**
> 状态：**已被实测确证为平台侧缺陷** ｜ 依据：dataset-2 D2-007

## 1. 问题

任何 `targetLang=csharp` 的 job 都以 `INFRA_ERROR` 终止，**目标侧 preflight 从未尝试（SKIPPED）**。

平台原始诊断（**保留不改写**）：

```
jobStatus   : INFRA_ERROR
lastError   : { code: AGENT_UNAVAILABLE, owner: agent, retryable: true }
message     : agent /run failed: AGENT_EXECUTION_ERROR: EvaluationContractError:
              invalid codeconvert-evidence-bundle at $.collectorDiagnostics.0:
              Additional properties are not allowed ('detail' was unexpected)
```

## 2. 归因：平台自己的产出违反自己的 schema

- `collectorDiagnostics` 由**平台侧采集器/agent 生成**；
- 本仓库提交的 capsule **不含**该字段（只有 `source/`、`target/`、`run_case.py`、`input_profile.json`、`metadata.json`、`comparison_manifest.json`）；
- 即：**产出方**写入了 `detail`，**校验方**的 schema 不接受 `detail`。

⇒ 责任层：**平台侧**（`owner: agent` 亦如此标注）。

## 3. 复现证据

| # | 实验 | targetLang | 结果 |
|---|---|---|---|
| 1 | D2-007 job-00 | `csharp` | `INFRA_ERROR` |
| 2 | 同 capsule 重提 | `csharp` | `INFRA_ERROR`（逐字相同，可复现） |
| 3 | **对照探针**：同形 capsule，仅改目标语言 | `c` | **`COMPLETED`**（两侧均执行） |

实验 3 与 1/2 的源树、驱动、`input_profile`、manifest 形状**完全相同**，唯一差异是目标语言声明。
⇒ 故障**专属** csharp 目标路径。

## 4. 影响面（按 manifest 精确统计）

| 方向 | 项数 |
|---|---:|
| cpp-to-csharp | 12 |
| go-to-csharp | 9 |
| c-to-csharp | 6 |
| python-to-csharp | 6 |
| ruby-to-csharp | 4 |
| powershell-to-csharp | 1 |
| **合计** | **38** |

不受影响：其余 **239 项**。**C# 作为源语言**的方向（csharp-to-*）目标非 C#，**不受影响**。

## 5. 建议修法（二选一，均属小改动）

| 方案 | 做法 | 评价 |
|---|---|---|
| **A（推荐）** | 放宽 `codeconvert-evidence-bundle` schema，允许 `collectorDiagnostics[]` 含 `detail` | 保留诊断信息，不丢证据 |
| B | 采集器序列化时不再写 `detail`，或把它并入既有允许字段 | 改动更小，但**丢失诊断细节** |

**倾向 A**：`detail` 是有用的诊断载荷，删掉会让后续排障更难。

> **重要更正（2026-10-10 平台仓库实测）：方案 A「仅放宽 schema」并不足以修复。**
> `diagnostic` def 不仅 `additionalProperties:false` 挡掉 `detail`，还**必填 `dimension`**，
> 而 build-prerequisite producer(`PrerequisiteFinding.to_dict()` 与 main.py 的 preflight fallback)
> **既写 `detail`、又完全不写 `dimension`**。只放宽 schema 允许 `detail` 后，校验会在**下一步**改报
> `'dimension' is a required property`。两处都得改才真修好。

### 5.1 实际已实施的修法（平台仓库 `third-party-evaluation-system`）

1. **schema**（`packages/evaluation-contracts/evidence-bundle.schema.json` 的 `diagnostic` def）：
   新增可选属性 `"detail": {"type":"object"}`；**保留** `additionalProperties:false` 与 `dimension` 必填（不弱化其它诊断）。
2. **producer**（`apps/vm-agent/vm_agent/app/build_prerequisites.py` 的 `to_dict()`）：补 `"dimension": None`（build 级发现不属任何观察维度，enum 允许 null）。
3. **fallback**（`apps/vm-agent/vm_agent/app/main.py` 的 preflight 异常分支手搓的诊断 dict）：同样补 `"dimension": None`。
4. **回归测试**：`tests/test_build_prerequisites.py::test_findings_serialise_to_plain_json_types` 增断言，锁定 `dimension` 存在且 `detail` 为 dict。

> 平台仓库**本机只改文本、未运行**其 pytest(遵守安全边界的「本机不运行」)；上述改动需在平台**获批环境**跑 vm-agent 测试 + 用 D2-007 原始 capsule 重提 csharp 验收。

## 6. 验收判据

1. 用 **D2-007 的原始 capsule** 重提，`targetLang=csharp`，应返回 `COMPLETED` 或**代码层**结果（`FAILED_COMPILE` / `FAILED_RUNTIME` 均可）；
2. **不得**再出现 `INFRA_ERROR` + `AGENT_UNAVAILABLE` + `$.collectorDiagnostics.0` 类报文；
3. 目标侧 preflight 状态**不得**为 `SKIPPED`；
4. 回归：非 C# 目标（如 `c`）仍 `COMPLETED`。

## 7. 我方现状（不改动）

受影响的 38 项保持 `WAITING / BLOCKED_ENV`，**不消耗模型调用**，平台修复后按原契约重提。
已落盘记录见 `docs/test/dataset-2/batch/platform-blocker-csharp-target.md`。
