# Spec 05｜提交端准入消费与批次授权

> 版本：1.0；更新：2026-10-09
> 状态：**已实现（2026-10-10）**。平台 `evaluation_core/submission_admission.py` 落地 `prepare_submission()`/`validate_batch_authorization()`，并接成 `POST /api/jobs` 服务端硬门禁（未准入 403，不可绕过）；详见[平台提交端准入闭环接入记录](../reports/平台提交端准入闭环接入-2026-10-10.md)。本机只编辑并跑平台 pytest（新增 20+11 条，三套件 497 passed），真实样本提交与部署在隔离环境。
> **§3.3 伪代码已按修正逻辑实现**（见该节注记）：平台**不 lift 任何 BLOCKED**、带凭证线索一律拒绝、未知态默认拒绝。
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

### 2.4 单文件任务 = 批次为一（every submission carries authorization）

`classification` 与 `batchAuthorization` 是 `POST /api/jobs` 的**固定必附字段**，**单项提交同样必附**。单文件任务按**"批次为一"**产出一份覆盖该单项的最小 `batch-authorization.json`：同一 schema、同一 §2.2 校验，`batchId` 取该项所属批次 id、`scope` 覆盖该单项——**不再把单项授权只写进冻结记录**。服务端对单项与批量走**同一** `admit_single()` 校验，无单项豁免。

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

> **`admissionStatus="APPROVED"` 是提交计划层（SubmissionPlan）字段**，表示"本次提交准备已通过"，与分类器输出的 `admissionStatus="ALLOWED"` 是**不同对象、不同层**：ALLOWED 来自分类器读源码，APPROVED 来自提交端消费"分类 + 授权"的结果。两者都不表示已运行或已通过（见 [分类结果准入 §4](../../../../references/workflow/classifier-agent-gate.md)）。

### 3.3 判定顺序（按 Spec04 §5.1）

> ⚠ **下面这段伪代码是 Spec04 的原始形态，有缺陷、已被平台实现取代，仅作存档对照**；实际落地逻辑以本节末「实现修正（2026-10-10，已落地）」为准，**不要照抄本伪代码**。

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

> **⚠ 实现修正（2026-10-10，已落地）**：上面这段伪代码有缺陷——`configured=true` 时它跳过规则2，若主 `blockingReason=public_network_unverified` 又非 credential，会落入 `else: allowed`，**漏掉同时命中的凭证线索**；`else` 也不拒绝未知状态。平台 `submission_admission.admit_task()` **不照此实现**，而是：
> 1. **不 lift 任何 BLOCKED**：`admissionStatus!=ALLOWED` 或 `blockingReason!=null` 一律阻断（原因取分类器给的 `blockingReason`，缺失记 `unknown_status`）。公网阻断的解除**只能靠重新分类**产出新的 ALLOWED（§3.4），不在提交端翻案。
> 2. **凭证纵深**：任一 `details.files[].credentialFindings` 非空即阻断 `real_credential_suspected`，即便状态被误置 ALLOWED。
> 3. **身份/哈希绑定**：提交内容 `source/` 树的**每个文件**（含源侧驱动 `run_case.py`）的 sha256 必须与分类输入一致——**按 `source/` 文件集合校验、非按扩展名过滤**，缺任一 source/ 文件即 `identity_mismatch`（2026-10-10 实测）；分类器 SHA 必须在许可集合，否则 `untrusted_classifier`。
> 4. **隔离假设一致（仅公网目标）**：带**公网/hostname** 网络目标（`details.files[].network_targets[].scope ∈ {public,hostname}`）的 ALLOWED 项，批次授权必须 `networkIsolation.configured=true`，否则 `public_network_unverified`。**private/loopback 不设此门**——准则是"证明危险才阻断"，敏感/副作用/私网代码默认 ALLOWED，安全由 VM 隔离兜底（见 [tiered-admission-policy.md](tiered-admission-policy.md) 二元 3 规则）。
>
> 因此 §4 **用例4 重解释**为「**重新分类后得到 ALLOWED**（requiresNetworkIsolation 仍 true）+ 授权 configured 且证据齐全 → allowed」，并新增负向回归「**BLOCKED/public + configured 授权 → 仍 blocked**（不 lift）」。两条均有回归：`test_submission_admission.py::test_case4_...` 与 `test_bypass_blocked_public_with_configured_isolation_is_still_blocked`。

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
| 4 | 重新分类后得到 ALLOWED（`requiresNetworkIsolation` 仍 true）+ 授权 `configured=true` 且证据齐全 | 该项 allowed（**不是在提交端 lift 旧 BLOCKED，而是凭新的 ALLOWED 分类**，见 §3.3 实现修正） |
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
  **已实现于** `packages/evaluation-core/evaluation_core/submission_admission.py`（`prepare_submission`/`admit_single`/`validate_batch_authorization` + 数据模型），门禁接线在 `apps/remote-controller/.../services/job_service.py::_enforce_admission_gate`，端点 `app/api/jobs.py` 增 `classification`/`batchAuthorization` 两个必需表单字段。§2.2 字段校验为**代码内校验**（即 `validate_batch_authorization` 本身），不另立无消费方的 JSON schema。

## 6. 已知限制

- 批次授权字段校验只能证明"证据被填写"，**不能证明隔离真实存在**；
  证据的实质正确性依赖人工签署与现场复核（T03-c）。
- `contractHash` 一致性检查需读取提交时的实际契约哈希；1.0.26 四角色目前已一致，T02-a 健康验收已完成。
  该事实不替代批次授权、现场隔离证据或平台侧准入消费者。
- 本规格不定义平台侧网络/文件/进程清理机制，那些由 Controller 强制（Spec03 §3 lifecycle）。
