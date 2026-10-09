# 部署前置：平台优化完成度核查

> 日期：2026-10-09
> 性质：**实时只读核查**（现役 API）+ 候选源码静态核对；未部署、未修改、未提交 job
> 依据：`controller-agent-improvements.md`（Spec02）、`总评估报告-2026-10-05.md`
> 结论：**平台优化尚未全部完成** —— Spec02 的 T02-b/T02-c 在现役版本与候选源码中**均未实现**，
> T02-d 仅部分实现；**建议先补 T02-c 再升级 Agent**（理由见 §7）

## 1. 为什么必须先核查

用户裁定：Controller `1.0.25-noise.1` 是最新基线，**可以升级 Agent**，
但前提是"确定优化工作全部完成"。

因此必须先回答：**优化工作到底完成没有？** 下面用现役 API 与候选源码两侧交叉验证，
不依据任务台账的自我声明。

## 2. 现役 Controller（1.0.25-noise.1）实测字段

`GET /api/health` 返回字段：

```
status, service, version, contractSetHash, runnerMode, ready
```

`GET /api/runners` 每项返回字段：

```
id, backend, os, arch, supportedLanguages, supportsSnapshotRollback,
selectionPriority, lifecycleState, ready, contaminated, baselineSnapshot,
lastFailureType, lastFailureReason
```

## 3. 逐项完成度（对照 Spec02）

| Spec02 项 | 要求 | 现役 Controller | 候选源码 | 判定 |
|---|---|---|---|---|
| **T02-b** 就绪诊断 | health 增 `executionReady`、`readyRunnerCount`、`blockedRunnerCount`、`checkedAt`、`blockingReasons` | **无**（仅 6 个字段） | **无**；`health()` 仅比现役多一个 `comparison` 字段 | **未实现** |
| **T02-c** 契约故障定位 | 诊断含 `runnerId`、`expectedContractSetHash`、`actualContractSetHash`、`checkedAt`、`checkPhase`、`reasonCode` | **无**（runners 无任何 expected/actual 字段） | **无**；`agent_client.py` 抛错仍是裸 `CONTRACT_MISMATCH`，不带哈希对照 | **未实现** |
| **T02-d** 观察义务预检 | 明确 required/optional；缺必需维度在执行前报能力不足 | 未验证 | **已有部分实现**：`job_service.py` 从 `functionalProfile.obligations[].requiredDimensions` 计算必需维度，并校验其已请求、已配置比较，否则拒绝并给出明确错误 | **部分实现** |
| **T02-e** 目标侧独立诊断 | 显式诊断模式，无源基线时 inconclusive | 未验证 | `dual_run_orchestrator.py` 源失败仍早返回（约 :173） | **未实现** |
| 比较策略反例回归 | 保留负向对照 | 已有（四场景含 3 个负向） | 已有 | **已具备** |

**关键交叉验证**：现役 `/api/health` **没有 `comparison` 字段**，而候选源码的 `health()` **有**。
这证明现役运行的代码**不是**候选工作树的代码；同时也说明候选工作树相对现役的改动很小
（仅一个字段），**但 Spec02 的 T02-b/c/d 在两边都还没有**。

### 3.1 对 T02-d 的修正（本核查中自我更正）

初次静态检索时曾把 T02-d 判为"完全未实现"。进一步阅读 `job_service.py`（约 :117–135）后确认
**已有部分实现**：`_prepare_job` 会校验 functional profile 的必需观察维度是否被请求、
是否配置了对应比较策略，不满足则抛出具名错误。

仍缺的是 Spec02 §5 要求的**能力侧**语义：Agent 支持哪些维度、哪些必需维度在某一侧缺失，
应在执行前以结构化方式报告（而非仅校验策略声明）。因此判定为**部分实现**，不是"无"。

### 3.2 对 T02-c 的说明

仓库中存在 `reasonCode` 字样，但出现在 `evaluation_core/functional_assessment.py:94`，
属**功能评估**的失败原因码，**不是** Spec02 §4 要求的契约诊断字段。
现役 `/api/runners` 与候选 `agent_client.py` 均无 `expectedContractSetHash` / `actualContractSetHash` /
`checkPhase`，故 T02-c 判定为**未实现**。

## 4. 直接后果：当前无法精确定位契约差异

现役 Controller 报出 `CONTRACT_MISMATCH`，但由于缺 T02-c 的诊断字段，
`/api/runners` **不含 Agent 的实际契约哈希与期望哈希**。

本次只能通过旁路取得 Linux Agent 的契约（`e088a356…`），
而 **Windows Agent 的契约哈希根本无法取得** —— 其 `/health` 返回空响应体，
且缺少 expected/actual 诊断使 Controller 也无法报告差异明细。

这正是 Spec02 §4 想解决的问题：**"减少反复猜测/重装"**。

## 5. 总评估报告提出的环境改进项

`总评估报告-2026-10-05.md` §6 记录的 8 项环境发现，其中平台侧待办（§8 建议）：

| # | 报告建议 | 现状 |
|---|---|---|
| 1 | 修复 Go 构建超时 | 未验证 |
| 2 | 工具链版本一致性（Go 1.26.4 vs `go 1.27`） | 未验证 |
| 3 | 明确杀软隔离策略 | 已有 Defender 精确排除（Controller jobs / Agent workspaces） |
| 4 | **完成 VM 网络隔离并用无害探针验证** | **未完成** —— 报告记三台 VM 均有默认外网路由，隔离未验证；本轮亦未取得新隔离证据 |
| 5 | Windows C/C++ Winsock 自动补链 | 未验证 |
| 6 | C# 缺 `.csproj` 补最小中性工程 | 未验证 |
| 7 | 大文件 JSON 改 `<<<FILE: …>>>` 分块协议 | 未验证 |
| 8 | 宿主隔离导致约 12 份样本不可读 | 与 batch 输入缺失相关，另有核查 |

**其中第 4 项是硬门槛**：在隔离未验证前，含硬编码外部地址的任务不能执行。

## 6. 结论

**优化工作未全部完成。** 具体状态：

| 项 | 状态 |
|---|---|
| T02-a 部署身份 | **已完成**（本次实时取得三方身份与根因） |
| T02-b 就绪诊断 | **未实现**（现役 health 6 字段；候选仅多一个 `comparison`） |
| T02-c 契约故障定位 | **未实现** —— **且它正是本次契约排查困难的直接原因** |
| T02-d 观察义务预检 | **部分实现**（策略侧校验已有；能力侧结构化预检缺） |
| T02-e 目标侧独立诊断 | **未实现**（P1，条件进入） |
| 比较策略负向对照 | **已具备**（四场景含 3 个负向） |
| VM 网络隔离验证 | **未完成**（安全硬门槛；报告记默认外网路由，隔离未验证） |

## 7. 因此对 Agent 升级的建议顺序

用户已同意"升级 Agent 去匹配 Controller"。但按上述核查，建议**先补 T02-c 再做升级**，理由是：

- T02-c 会让升级后的契约核对（以及万一再次不匹配时的排查）具备 expected/actual 对照；
- 否则本次升级若不成功，仍会退回到"只能靠旁路逐个猜 Agent 契约"的处境；
- T02-b/c 均为 P0 且**无外部依赖、可立即开发**（Spec02 §9.6 已确认入口存在）。

**但最终顺序由用户决定**：若希望尽快恢复三 runner 可用，也可先升级 Agent 恢复执行能力，
再补 T02-b/c/d。两条路都需要一次新的发布与部署，建议合并到同一次发布以节省一轮窗口。

## 8. 本核查未做与不能声称

- 未部署、未回滚、未重启任何服务；未修改任何远端文件。
- 未提交 job；只读 `GET /api/health` 与 `GET /api/runners`。
- T02-d/e 的"未实现"判断基于候选源码静态阅读与现役字段比对，**未运行平台测试**。
- 未验证 Go 构建超时、工具链一致性等运行时项（需在获批环境执行）。
- 不能声称"平台已就绪可升级"；本文结论恰恰相反：升级前仍有未完成项。
