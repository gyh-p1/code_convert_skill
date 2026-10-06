# Spec 04｜证据模型、Controller 兼容与迁移

## 1. 证据分层

第三方返回必须把以下四层分开，禁止以一个总 verdict 覆盖：

```text
SafetyEvidence
  -> EnvironmentEvidence
  -> BuildEvidence
  -> Execution/ComparisonEvidence
```

### 1.1 SafetyEvidence

说明任务是否被允许进入某个 profile：Planner hash、required capabilities、Attestation hash、Permit ID、阻断码、人工 override。

### 1.2 EnvironmentEvidence

说明 runner、快照、工具链、依赖、路由/防火墙、DNS、资源、fixture、清理和 revert 的现场状态。

### 1.3 BuildEvidence

保存 source/target 两侧命令、工具链、退出码、诊断、产物 hash、重试和归因。环境错误不能写成代码失败。

### 1.4 Execution/ComparisonEvidence

保存输入 profile、事件摘要、stdout/stderr 摘要、网络/进程/文件观察、oracle 结果、差异位置和未覆盖义务。comparison `matched` 只有在 oracle 完整且安全证据通过时才形成有限行为结论。

## 2. 推荐结果结构

```json
{
  "schemaVersion": "stage1.evaluation-report.v1",
  "taskId": "...",
  "caseId": "...",
  "disposition": "FIXTURE_EQUIVALENCE",
  "safety": {
    "planSha256": "sha256:...",
    "profileId": "LOCAL_FIXTURE",
    "attestationSha256": "sha256:...",
    "permitId": "permit-...",
    "status": "PASSED|BLOCKED|EXPIRED|OVERRIDDEN"
  },
  "environment": {
    "runnerId": "...",
    "baselineSnapshot": "...",
    "toolchain": {},
    "fixtureSetSha256": "sha256:...",
    "cleanup": "PASSED|FAILED|UNKNOWN",
    "revert": "PASSED|FAILED|UNKNOWN"
  },
  "source": { "build": {}, "execution": {} },
  "target": { "build": {}, "execution": {} },
  "comparison": {
    "oracleId": "...",
    "status": "PASSED|LIMITED|UNVERIFIED|INCONCLUSIVE|FAILED",
    "obligations": [],
    "uncovered": []
  },
  "finalDisposition": "...",
  "failureClassification": "NONE|CODE|ENV|SAFETY|FIXTURE|ORACLE|INFRA",
  "evidenceRefs": []
}
```

## 3. 与现有 `/api/jobs` 的兼容策略

### 3.1 不改变旧 capsule 的历史解释

已有 `comparison_manifest.json`、`input_profile.json`、`metadata.json`、source/target 树和历史 report 原样保留。新系统不得回写旧报告，也不得用新 fixture 结果倒填旧 run。

### 3.2 版本协商

建议在 Controller 增加能力发现，而非假定接口已支持：

- `GET /api/capabilities`：Controller contract set、supported plan/profile/evidence schema。
- `GET /api/runners`：保留现有字段，追加 profile/capability/attestation 支持声明。
- `POST /api/preflight`：提交 plan、profile、fixture、capsule 摘要，返回 preflight/attestation 要求。
- `POST /api/permits`：在 preflight 通过后签发一次性 Permit。
- `POST /api/jobs`：新增可选 `permitId`、`planSha256`、`profileId`；无新字段时仅允许兼容范围。
- `GET /api/jobs/{id}/evidence`：返回分层 evidence index，不替换现有 report/logs 路径。

真实现役接口若与此不同，以平台实际 contract discovery 为准；本文不把建议路径当成已存在能力。

### 3.3 Compatibility Mode

| 模式 | 允许 | 禁止 |
|---|---|---|
| `legacy-build-only` | 历史安全范围内的 source/target build | 高风险 execution、未验证网络运行 |
| `stage1-profiled` | 有 plan + attestation + Permit 的新任务 | 绕过 profile 的提交 |
| `stage1-fixture` | 登记 fixture/target 且 oracle 完整的受控运行 | 把 fixture 结果当真实系统结果 |
| `static-only` | 转换、自审、契约审阅 | 任何样本编译/运行 |

## 4. 旧概念迁移表

| 旧概念 | Stage 1 处理 |
|---|---|
| `evaluation-case.gateMode` | 保留历史字段；新增 `disposition/profile/permitPolicy`，不再用二值 gate 表达复杂安全条件 |
| `expectedObligations` | 迁移为带 source evidence、expected observations、negative observations 的 oracle |
| `conversion-result.verification` | 拆为 safety/environment/build/execution/comparison 五个维度 |
| `skillTrace` | 保持；新增 planner/contract hash，说明平台证据不是 Skill 规则 |
| `UNVERIFIED` | 保持；增加具体 `failureClassification` 和恢复条件 |
| `READY` | 仅表示服务生命周期；不能替代 Attestation |
| `comparison.matched` | 仅作 oracle 通过后的局部结论，不作为总正确率 |

## 5. 证据完整性和存储

- 每个证据对象有 `sha256`、产生时间、job/permit 绑定和来源角色；
- 原始 Controller/Agent 输出只追加不覆盖；诊断写在新文件或新事件中；
- 证据包分为 `safety/`、`environment/`、`source/`、`target/`、`comparison/`、`cleanup/`；
- 任何缺失关键证据的任务为 `EVIDENCE_INCOMPLETE` 或 `INCONCLUSIVE`，不自动降级为通过；
- 重新提交必须产生新 run ID、新 Permit 和新 evidence refs，并保留与旧 run 的 `supersedes` 关系。

## 6. 最低可审计事件

```text
PLAN_CREATED
RUNNER_SELECTED
PREFLIGHT_REQUESTED
ATTESTATION_RETURNED
PERMIT_ISSUED | PERMIT_REJECTED
JOB_SUBMITTED
SOURCE_BUILD_RECORDED
TARGET_BUILD_RECORDED
SOURCE_EXECUTION_RECORDED
TARGET_EXECUTION_RECORDED
ORACLE_EVALUATED
CLEANUP_RECORDED
REVERT_RECORDED
FINAL_DISPOSITION_RECORDED
```

事件必须带 `taskId`、`runId`、`atUtc`、`schemaVersion`、相关 hash 和幂等键；恢复流程根据事件判断已提交/已完成，禁止无依据重复执行。
