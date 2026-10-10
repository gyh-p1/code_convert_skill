# C1：把 `processes` 维度接入比较器

> 类型：**软缺口补全** ｜ 优先级：**P1** ｜ 状态：采集已通，仅差比较
> 依据：`docs/test/dataset-2/batch/platform-probes/probe-processes/`（job `eval-20261010-082649-4a384b16`）

## 1. 现状（实测）

| 层 | 状态 |
|---|---|
| **采集** | ✅ **已可用**。提交 `dimensions:["output","filesystem","processes"]` 后，双侧 bundle 均出现 `observations.processes.status = "observed"` |
| **比较** | ❌ **未实现**。`comparison.json` 中 `dimensions.processes = { applicable: false, status: "not-applicable" }` |

⇒ **证据已经在 bundle 里，但比较器不看它。** 这不是采集器缺失，是**比较器未接入**。

## 2. 已有的证据结构（可直接消费）

```json
{ "eventType": "process.lifecycle",
  "sequence": 0,
  "timestampOffsetMs": 1,
  "data": { "imageName": "python",
            "normalizedImagePath": "python",
            "commandLine": "python run_case.py",
            "normalizedCommandLine": "python run_case.py",
            "startOffsetMs": 1,
            "endOffsetMs": 92,
            "exitCode": 0,
            "terminationReason": "exited",
            "processIdRef": "p0",
            "parentProcessIdRef": null } }
```

字段已足够做**结构化比较**：镜像名、命令行、退出码、终止原因、父子关系。

## 3. 必须先解决的语义问题：这是**采样**，不是完整轨迹

平台自陈（`observations.processes.limitations` 原文）：

> `Process descendants are sampled every 20ms; shorter-lived descendants may be missed.`

实测佐证：同一份探测，**source 侧只见 `p0`，target 侧见 `p0` + `p1`**——
两侧都确实 fork 了子进程，但短命子进程被采样窗口漏掉。

### 关键：采样丢失是**双向**的，不是"target 多、source 少"的单向偏置

本探测里被漏掉的恰恰是 **source 侧**的 C 子进程（`probe.c` 的 `fork` + `/bin/echo` 全部没进采样，只剩外层驱动 `p0`），
而 target 侧的 `python target.py` 因存活够长被采到。**丢失发生在哪一侧取决于子进程寿命，与转换正确性无关**。

⇒ 任何"一侧有、另一侧无"的事件差异——**无论哪个方向**——都可能只是采样抖动。

### 因此比较规则**不能**是"事件条数必须相等"，也**不能**是单纯的"单向包含"

若按条数或集合相等比较，会产生**大量假 FAIL**：完全正确的转换也会因采样抖动被判不一致。
而"单向包含（source ⊆ target）"同样不成立——当某条 **source 事件在 target 侧被漏采**时，包含关系被破坏，会反向制造假 FAIL。

## 4. 建议的比较语义（按"该维度能证明什么"设计）

> **总原则：进程维度只能靠"正面冲突"定 `mismatched`，不能靠"有/无"。**
> 既然采样丢失**双侧都会发生**（§3），那么 presence/absence 的差异**无论哪个方向**都不是可靠判据。
> 只有**两侧都观察到、能互相配对**的进程出现**实质字段冲突**（主要是 `exitCode`）才算行为差异；
> 事件只在一侧出现而无法互证时，按 [C3 观测充分性](C3-observation-sufficiency.md) 记为**证据不足**，既不判 matched 也不判 mismatched。

| 规则 | 说明 | 理由 |
|---|---|---|
| **先配对再比字段**：按 `normalizedImagePath` + `normalizedCommandLine` + 拓扑角色在两侧配对进程 | 比较的单位是"同一个进程"，不是事件集合 | 用平台已有的 normalized 字段，路径/参数差异可容忍 |
| **只有配对成功的进程才比字段**；`exitCode` 两侧都非 null 时**必须严格相等**，不等 ⇒ `mismatched` | 退出码是**实质行为** | 与采样无关 |
| **配不上的事件（任一侧多出或缺失，两个方向都算）不单独判 FAIL** | 降为 `minor`/`info`，并计入观测充分性 | 采样丢失是**双侧**噪声，presence/absence 不可作判据 |
| **`parentProcessIdRef` 只校验拓扑形状**，不校验具体 id | `p0→p1` 与 `p2→p3` 视为同形 | id 是采样分配的，无业务含义 |
| **`terminationReason == "unknown"` 不计差异** | 采样未捕获终止 | 信息缺失非行为差异 |

## 5. 验收判据

1. **正例**：提交一个**两侧都产生子进程**的无害样例（如 `probe-processes`），`comparison.dimensions.processes.applicable` 应为 **`true`**；
2. **比较真生效——用"正面冲突"验证，不用"有/无"**：提交一个两侧都产生**可配对**子进程、但**退出码不同**的样例（如一侧子进程 `exit 0`、另一侧 `exit 3`），应判 `mismatched`。
   **不要**用"只有一侧有子进程"来做这条验收——那条子进程可能被 20ms 采样漏掉导致测试不稳定，且按 §4 原则 presence/absence 本就不该单独判 FAIL；
3. **采样抖动不假 FAIL**：任一侧多出/缺少一条短命子进程（**两个方向都要测**）**不得**判 `mismatched`，应按 [C3](C3-observation-sufficiency.md) 记为证据不足或仅 `minor`；
4. **可观测前提**：验收样例中需要被比较的子进程必须**存活明显 > 20ms** 以稳定越过采样窗口，否则结论本身不可复现——这一条是前几条能成立的物理前提；
5. `output`/`filesystem` 维度的既有行为**不得**回归。

## 6. 我方准备

`platform-probes/probe-processes/` 已是一个**现成的正向样例**（两侧都有子进程），
可直接作为**验收判据 1** 的输入复用。
判据 2（退出码冲突）需另造一个两侧子进程退出码不同的无害样例；
判据 3/4 需另造采样抖动样例与"长存活子进程"样例——这三个样例**本机只写、不运行**，提交到隔离环境执行。
