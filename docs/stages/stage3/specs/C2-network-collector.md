# C2：`network` 维度采集器

> 类型：能力扩充 ｜ 优先级：**P2（可延后）** ｜ 状态：**硬缺口**，提交即被拒
> 依据：`docs/test/dataset-2/batch/platform-probes/probe-network/`（job `eval-20261010-082922-edde923c`）

## 1. 现状：完全不支持，且平台**正确地硬拒**

提交 `observationPolicy.dimensions: ["output","network"]` 后立即返回：

```json
{ "jobStatus": "INFRA_ERROR",
  "message": "observation obligations cannot be met: source,target",
  "lastError": { "code": "RUNTIME_UNAVAILABLE",
                  "message": "observation obligations cannot be met: source,target",
                  "owner": "runner", "phase": "QUEUED", "retryable": false } }
```

**这个处理方式是对的**：在 QUEUED 阶段拒绝，不浪费执行，责任层标注正确，
且**没有**静默接受然后报 `not-applicable`（那样会让调用方把"没观察"误当"等价"）。

平台自陈（`runner-capability-matrix.md` §1.3）：
> 本次不新增 network/registry Collector，也不提供网络隔离 Attestation/Permit

## 2. 先问：真的需要吗？

在投入成本前，应先确认**收益**。dataset-2 的网络类用例复盘：

| 项 | 网络行为 | 缺 network 维度是否真的挡住验证 | 实际瓶颈 |
|---|---|---|---|
| D2-021 | loopback 探测，且 linux 走 windows_only 分支 | **没有**。stdout 已足够 | 无 |
| D2-024 | 常驻监听服务 | **部分是**，但真正失败原因是**我的驱动** | 驱动 |
| D2-025 | loopback 连接被拒 | **没有**。stdout 含 ANSI + 结果码 | 无 |
| D2-083 | WinRM 远程执行 | **是** | **C7 才是关键** |
| D2-108 | 硬编码外联反向 shell | **是** | **C7 才是关键** |

⇒ **关键洞察**：挡路的**不是"采集不到网络事件"，而是"没有隔离证明"**。
  这两者**不是同一件事**，且 **C7 成本远低于 C2**。

**结论：C2 优先级应低于 C7。**

## 3. 若要做，建议的采集范围（最小可用集）

按"能证明什么"设计，而非"能抓多全"：

| 事件 | 字段 | 用途 |
|---|---|---|
| `network.connect` | 目标地址、端口、结果、进程 ref | 证明"是否连出、连到哪" |
| `network.listen` | 绑定地址、端口 | 证明监听面 |
| `network.accept` | 对端地址 | 证明实际建立了连接 |
| 目标地址**分类** | `loopback` / `private` / `public` / `special` | **直接支撑安全边界判定** |

最后一项**价值最高**：它能自动回答"这次运行有没有触碰非实验目标"，
这正是安全边界最关心的问题，也是当前**完全靠人工**判断的部分。

## 4. 与安全边界的耦合（必须在设计阶段解决）

**风险**：一旦平台"能采集网络事件"，容易被误读为"平台已隔离网络"。
但采集能力 **不等于** 隔离能力。

设计要求：
1. 文档必须明确：**观察到 loopback ≠ 网络已隔离**；
2. **不得**因新增 network 维度而让`网络隔离 Attestation` 的缺失显得已解决；
3. 采集器本身**不得**引入新的外联能力（只观察，不主动连接）。

## 5. 验收判据（若实施）

1. 提交 `dimensions: ["output","network"]` 的 loopback 样本 ⇒ 不再 `INFRA_ERROR`，且 `observations.network.status = "observed"`；
2. 事件中能正确标出 `127.0.0.1` 属于 `loopback`；
3. **回归**：非网络样本申请 network 维度时，不应产生噪声事件；
4. 文档同步更新，明确"采集 ≠ 隔离"。

## 6. 我方现状

D2-083（WinRM）与 D2-108（反向 shell）保持 `WAITING`，
**解除条件以 C7（隔离证明）为主，C2 为辅**。
