# Spec 05｜提交端准入消费与批次授权

> 版本：1.0；更新：2026-10-09
> 状态：**待实现规格**（T01-d、T03-d 可领取）
> 当前可用路径：用户要求今晚先用[分类结果准入](../../../../references/workflow/classifier-agent-gate.md)，现役部署不改。**分类 `ALLOWED` 即准入通过、允许运行**，Agent 不作主观复核。此页定义后续平台目标，§3.3 旧结果解除阻断的伪代码不可直接用作今晚放行规则；问题与验证见[接入审查](../reports/分类器一致性审查与Agent暂行接入-2026-10-09.md)。
> 依据：[Spec04 最高危阻断准入策略](tiered-admission-policy.md) §5.2、§5.3
> 约束：[安全边界](../../../../references/framework/safety-boundary.md) §2 批次授权与逐例核对

本文件把 Spec04 §5.2 的批次授权记录与 §5.3 的提交端逻辑写成**可实现的接口契约**。
Spec04 给出策略与伪代码，本文件给出字段、校验规则、错误分支与验收用例。

**本机不实现也不运行提交端**：提交端在评估平台侧实现与部署，本文件只定义契约。

## 1. 职责边界

```
分类器(v2.3)                批次授权(人工)              提交端(评估平台)
─────────────               ──────────────              ──────────────
输出 admissionStatus   ──┐
输出 blockingReason    ──┼──►  batch-authorization.json ──► prepare_submission()
输出 reviewGroups      ──┘     （隔离/合成数据证据）          ↓
                                                        allowed / blocked 清单
                                                              ↓
                                                        平台提交（不在本机）
```

- 分类器只产出**线索与阻断判定**，不产出执行许可（Spec01 §1）。
- 批次授权是**人工**签署的隔离与数据证据，不由分类器生成、不由提交端推断。
- 提交端只做**规则消费**：读分类结果 + 读批次授权 → 产出清单。它不重新分类、不修改证据。

## 2. 批次授权记录 `batch-authorization.json`

位置：`docs/test/dataset/{batch-id}/batch-authorization.json`

### 2.1 完整字段

```json
{
  "batchId": "batch-02",
  "authorizedAt": "2026-10-09T18:30:00Z",
  "authorizedBy": "human-reviewer",

  "vmIsolation": {
    "confirmed": true,
    "snapshotRollback": true,
    "cleanupVerified": true
  },

  "networkIsolation": {
    "configured": true,
    "publicNetworkBlocked": true,
    "experimentalNetworkOnly": true,
    "verificationEvidence": "iptables 规则已配置，curl 8.8.8.8 超时，仅 192.168.101.0/24 可达",
    "verifiedAt": "2026-10-09T17:45:00Z"
  },

  "dataSource": {
    "syntheticDataOnly": true,
    "noRealCredentials": true,
    "noProductionData": true,
    "confirmation": "所有输入已审阅，使用占位符凭证"
  },

  "scope": "所有非BLOCKED任务",
  "validUntil": "2026-10-16T23:59:59Z",
  "contractHash": "sha256:e088a356..."
}
```

### 2.2 字段校验规则

| 字段 | 类型 | 必填 | 校验 |
|---|---|---|---|
| `batchId` | string | 是 | 必须与冻结清单中声明的 batchId 一致；目录名只是存储位置，不作为授权身份 |
| `authorizedAt` | ISO-8601 UTC | 是 | 不得晚于当前时间 |
| `authorizedBy` | string | 是 | 非空；应为可追责的人工身份 |
| `vmIsolation.confirmed` | bool | 是 | 必须为 `true` 才可提交 |
| `vmIsolation.snapshotRollback` | bool | 是 | 必须为 `true` |
| `vmIsolation.cleanupVerified` | bool | 是 | 必须为 `true` |
| `networkIsolation.configured` | bool | 是 | 决定规则2是否放行 |
| `networkIsolation.publicNetworkBlocked` | bool | `configured=true` 时必填 | 必须为 `true` |
| `networkIsolation.experimentalNetworkOnly` | bool | `configured=true` 时必填 | 必须为 `true` |
| `networkIsolation.verificationEvidence` | string | `configured=true` 时必填 | 非空；须描述可复核的验证方式与结果 |
| `networkIsolation.verifiedAt` | ISO-8601 UTC | `configured=true` 时必填 | 不得晚于当前时间 |
| `dataSource.syntheticDataOnly` | bool | 是 | 必须为 `true` |
| `dataSource.noRealCredentials` | bool | 是 | 必须为 `true` |
| `dataSource.noProductionData` | bool | 是 | 必须为 `true` |
| `dataSource.confirmation` | string | 是 | 非空 |
| `scope` | string | 是 | 非空；当前仅支持 `"所有非BLOCKED任务"` |
| `validUntil` | ISO-8601 UTC | 是 | 必须晚于 `authorizedAt`，且提交时未过期 |
| `contractHash` | string | 是 | 须与提交时平台契约哈希一致 |

### 2.3 校验失败即整批阻断

任一必填字段缺失、为假或过期 → **拒绝整批提交**，不逐项降级。
这与 Spec04 §7.1"未配置则整批阻断该类任务"一致：授权是批次级前置条件，不是逐项开关。

## 3. 提交端接口 `prepare_submission()`

### 3.1 签名与输入

```python
def prepare_submission(
    batch: Batch,                 # 含 tasks，每项有 taskId
    classifications: dict[str, Classification],  # taskId -> 分类结果
    batch_auth: BatchAuthorization,
    now: datetime,                # 显式注入，便于测试
) -> SubmissionPlan:
    ...
```

**输入约束**：

- `classifications` 必须覆盖 `batch.tasks` 的每个 taskId；缺项按 `input_error` 阻断，
  不得静默跳过（Spec01 §2"缺失不漏项"）。
- `batch_auth.batchId` 必须等于 batch 标识。
- `now` 显式传入，不读系统时钟，保证可测试与可追责。

### 3.2 输出结构

```python
@dataclass
class SubmissionPlan:
    allowed: list[AllowedTask]
    blocked: list[BlockedTask]
    summary: dict          # total / allowed / blocked / allowedRate / byBlockingReason

@dataclass
class AllowedTask:
    taskId: str
    admissionStatus: str = "APPROVED"
    batchAuthRef: str      # batch_auth.batchId
    classification: str    # 主分类
    reviewGroups: list[str]

@dataclass
class BlockedTask:
    taskId: str
    reason: str            # 人类可读
    action: str            # 解除条件
    blockingReason: str    # input_error | public_network_unverified | real_credential_suspected | missing_classification
```

### 3.3 判定顺序（按 Spec04 §5.1）

```python
# 前置：批次授权必须整体有效
if not validate_batch_authorization(batch_auth, batch, now):
    return SubmissionPlan(allowed=[], blocked=all_tasks, summary=...)

for task in batch.tasks:
    cls = classifications.get(task.taskId)
    if cls is None:                                    # 分类缺项
        blocked(task, "missing_classification")
    elif cls.admissionStatus == "BLOCKED" and cls.blockingReason == "input_error":
        blocked(task, "input_error")                   # 规则1
    elif cls.blockingReason == "public_network_unverified" \
         and not batch_auth.networkIsolation.configured:
        blocked(task, "public_network_unverified")     # 规则2
    elif cls.blockingReason == "real_credential_suspected":
        blocked(task, "real_credential_suspected")     # 规则3
    else:
        allowed(task)
```

**顺序不可交换**：规则1→2→3 短路，与分类器一致。同时命中"公网未隔离"与"疑似凭证"时
报 `public_network_unverified`，让审查者先修隔离。

### 3.4 关键行为约束

| 约束 | 理由 |
|---|---|
| 不修改 `classification` 字段 | 分类结果是证据，提交端只消费不改写 |
| 不因规则2解除而放行规则1/3 | 三类阻断互相独立 |
| 规则2 解除后必须重新分类 | 隔离条件变化改变了分类输入条件，不能直接复用旧 BLOCKED 结果 |
| 批次授权过期 → 全批阻断 | 授权有有效期，Spec04 §5.2 |
| 不自动放行 `real_credential_suspected` | 必须人工确认是示例数据后**修正分类输入**再重跑 |
| `allowed` 不等于已执行 | 提交仍需平台侧隔离与清理；本清单只是准备结果 |
| 输出不含源码正文与凭证原文 | 遵循 Spec01 §4 |

## 4. 验收用例

| # | 场景 | 期望 |
|---|---|---|
| 1 | 全批 ALLOWED + 有效授权 | 全部 allowed，`allowedRate=100%` |
| 2 | 含 `input_error` 项 | 该项 blocked/`input_error`，其余不受影响 |
| 3 | 含 `public_network_unverified`，授权 `configured=false` | 该项 blocked/`public_network_unverified` |
| 4 | 同上，但授权 `configured=true` 且证据齐全 | 该项 allowed（规则2 解除） |
| 5 | 含 `real_credential_suspected` | 该项 blocked；**即使授权隔离也不放行** |
| 6 | 同一项同时公网未隔离 + 疑似凭证 | blocked 原因为 `public_network_unverified`（顺序） |
| 7 | 分类结果缺某个 taskId | 该项 blocked/`missing_classification`，不静默跳过 |
| 8 | 授权缺 `verificationEvidence` 但 `configured=true` | 整批拒绝，非逐项降级 |
| 9 | 授权 `validUntil` 已过期 | 整批拒绝 |
| 10 | 授权 `batchId` 与批次不符 | 整批拒绝 |
| 11 | 授权 `vmIsolation.confirmed=false` | 整批拒绝 |
| 12 | 输出序列化 | 不含源码正文、不含凭证原文 |

负向用例（5、6、8、9、10、11）必须有对应回归；不能只测正向放行。

## 5. 与既有实现的衔接

- 分类器已实现并测试：`admissionStatus`、`blockingReason`、`requiresNetworkIsolation`、
  `requiresSyntheticData`（Spec01 §4）。
- 分类器的 `--network-isolation-configured` 只影响**分类输出**，不改写证据；
  提交端仍须独立校验 `batch-authorization.json`。两者不可互相替代。
- 提交端在评估平台侧实现，位于剥离清单（Spec03 §5）中的评估栈内，不放进转换 Skill 仓库。

## 6. 已知限制

- 批次授权字段校验只能证明"证据被填写"，**不能证明隔离真实存在**；
  证据的实质正确性依赖人工签署与现场复核（T03-c）。
- `contractHash` 一致性检查需读取提交时的实际契约哈希；1.0.26 四角色目前已一致，T02-a 健康验收已完成。
  该事实不替代批次授权、现场隔离证据或平台侧准入消费者。
- 本规格不定义平台侧网络/文件/进程清理机制，那些由 Controller 强制（Spec03 §3 lifecycle）。
