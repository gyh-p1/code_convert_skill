# C3 + C4（最高优先）："两侧均无观察"判定与观测充分性报告

> 类型：**正确性缺陷修复** ｜ 优先级：**P0**（与 C0 并列）
> 依据：dataset-2 实测 **2 例假阳性**

> **2026-10-11 更正**：§1–7 保留问题、建议与实施历史；其中“非空实质输出即真匹配”、D2-177 无条件回归 matched 和从字段即可看出充分性的措辞，不作为当前业务路径验收判据。当前更正见 §8；原始 verdict、证据和历史测试数字不改写。

## 1. 问题：比较器不区分"一致"与"都没观察到"

### 实例 1 —— D2-029 job-01（`eval-20261010-053037-1d8e7d08`）

| 侧 | exit | stdout | stderr |
|---|---|---|---|
| source | 1 | **空**（0 字节） | 空 |
| target | 1 | **空**（0 字节） | 空 |

平台判定：`behaviorVerdict = **matched**`，`coverageRatio = 1.0`，`diffs = []`。

**真相**：两侧都因**我的驱动缺陷**（空 argv 进了 stdin 分支）而"什么都没做"。
这是**两个空输出相等**，不是行为一致。

### 实例 2 —— D2-024 job-04（`eval-20261010-055115-367d73e1`）

| 侧 | stdout | stderr |
|---|---|---|
| source | 空 | `DRIVER-FAILURE: readiness banner was never observed` |
| target | 空 | **同一条文本**（逐字节相同，52 B） |

平台判定：**`matched`**，`diffs = []`。

**真相**：两侧都**没起来**，stderr 是**我驱动自己的失败标记**，不是被测程序输出。

## 2. 根因

比较器对"已观察维度"做**相等性比较**。当两侧的观察都是**空/退化**时，相等性成立 ⇒ matched。
**缺少"这次观察是否足以支撑结论"的判定。**

注意：`coverageRatio = 1.0` **不能**作为充分性证据——
它衡量的是"**申请**的维度里有多少被比较了"，不是"**观察到的东西够不够**"。
实例 1 中 `applicableDimensions = 1`，那是**输入面声明**，不是观测充分性。

## 3. 建议实现（两层）

### C3：新增充分性判定

在生成 verdict **之前**，对每个 applicable 且 observed 的维度做最小充分性检查：

| 检查 | 判定 |
|---|---|
| 双侧该维度观察**均为空**（无事件、无字节） | **不足以判 matched** |
| 双侧 **exitCode 相同且非 0**，且 stdout/stderr **均为空** | **不足以判 matched**（同 D2-029） |
| 观察内容与**驱动自身的失败标记**同形（如同一条 stderr 双方都有） | **不足以判 matched** |

不满足时**不应**输出 `matched`，而应输出一个**新档位**，例如：

```json
{ "behaviorVerdict": "inconclusive",
  "inconclusiveReason": "no-observable-behaviour: both sides produced empty output with equal exit codes" }
```

> 若不便新增档位，退一步也要在 `verdictReason` 与 `coverage` 中**显式标注**，
> 且 `matchedDimensions` **不得**计入这种情形。

### C4：观测充分性报告字段

在 `comparison.json` 的 `coverage` 中补充（命名可由平台定）：

```json
"coverage": {
  "applicableDimensions": 1,
  "observedDimensions": 1,
  "matchedDimensions": 1,
  "sufficientDimensions": 0,
  "insufficiencyReasons": [
    "output: both sides empty, exit codes equal and non-zero"
  ]
}
```

价值：调用方**一眼能看出"这次比较其实没证明什么"**，而不必去翻原始字节。

## 4. 为什么这是**最高**优先级

其他缺口（C1/C2/C5/C6）造成的是"**验证不了**"，调用方知道要写 `UNVERIFIED`。
本缺口造成的是"**看起来验证过了**"——**假阳性会被写进结论**，
污染的不只是一项，而是**整批的可信度**。

dataset-2 已因此产生 2 例假阳性，且**都是我事后逐字节核对原始证据才发现的**；
若只读平台 verdict，会直接把"什么都没验证"记成"行为一致"。

## 5. 验收判据

1. **实例 1 复现**：两侧空输出 + 相同非零退出码 ⇒ **不得**再返回 `matched`（D2-029 的 `job-01` **与** `job-04-probe-dash-arg` 同形,两者都要覆盖）；
2. **实例 2 复现**：两侧 stderr 为同一条驱动失败标记 ⇒ **不得**再返回 `matched`；
3. **反向回归**：两侧都有**实质且相同**的输出 ⇒ 仍返回 `matched`（不得矫枉过正把所有匹配判成 inconclusive）。
   具体锚点：**D2-177 `which.c` job-01**——两侧 exit 1、stdout 空,但 stderr 均为被测程序自身的 `usage: which [-as] program ...`(31 B,同一 digest),属真匹配,复跑**仍须** `matched`；
4. `coverage` 新增字段在正常匹配时 presence 正确、数值合理。

## 6. 我方已有的可复现材料

两个实例的 capsule 与原始回传均在：

```
docs/test/dataset-2/c-to-cpp/stest-fs-posix-to-win/output/batch/04-evaluation/job-01-dual-build/
docs/test/dataset-2/c-to-cpp/c01-linux-win-network/output/batch/04-evaluation/job-04-loopback-listen-live-capture/
```

原始 `comparison.json` 均**保留未改写**，可直接作为验收输入。

> 全量审计（33 份 matched 逐项核对）见 [reports/matched-verdict-false-positive-audit-2026-10-10.md](../reports/matched-verdict-false-positive-audit-2026-10-10.md)：
> 假阳性确认仅集中于 D2-029（job-01 + job-04）与 D2-024（job-04），其余 30 份为真匹配；D2-177 job-01 列为反向回归锚点。

## 7. 实施状态（2026-10-10，平台仓库 `third-party-evaluation-system`）

**C3 核心（判定正确性）已实施并验证**；**C4（coverage 报告字段）尚未实施**。

### 已做（C3）

- `evidence_comparator.py`：新增 `_stream_is_empty` / `_output_is_degenerate`，在 `compare_output_dimension` 的「无 diff 即 matched」分支前加**退化判定**——当**两侧 stdout 与 stderr 全空**时，返回 `status:"inconclusive"`、`observed:false`，不再 `matched`。
  - 复用既有的 `inconclusive` 维度状态与 behaviorVerdict，**未动任何 schema**（`dimensionStatus`/`behaviorVerdict` 本就含 `inconclusive`）。
- 回归测试 3 条（`test_evidence_comparator.py`）：空/空→inconclusive、D2-177 实质 stderr→仍 matched、端到端 bundle→inconclusive 且 schema 合法。
- **真实证据复跑验证**（用 dataset-2 原始回传）：

  | 用例 | 平台原判 | 修复后 |
  |---|---|---|
  | D2-029 job-01 | `matched` | **`inconclusive`** |
  | D2-029 job-04-probe-dash-arg | `matched` | **`inconclusive`** |
  | D2-177 job-01（反向回归） | `matched` | `matched`（保持） |

- 平台三套件全绿：**431 passed**。

### 一个诚实的边界：D2-024 **不**被此修法捕获

D2-024 两侧 stderr 是**同一条实质文本**（我方驱动的 `DRIVER-FAILURE` 标记），exit 相同。从平台视角这是「两侧输出逐字节一致」——**真匹配**。它之所以是假阳性，依赖的是「那条 stderr 是驱动失败标记」这一**领域知识**，平台无从得知。
⇒ 平台侧只负责「**两侧全空**」这一可泛化的不足情形；**驱动标记型假阳性属转换/驱动侧责任**（见优先级建议第 2 条：驱动四要素 + 不让驱动标记冒充程序输出）。

### C4 已实施（2026-10-10）

`report_builder.summarize_evidence_coverage` 新增两字段：

- `sufficientDimensions`：仅统计**达成确定比较**（matched / mismatched / semantic-match）的 applicable 维度；observed-but-empty（inconclusive）**不计入**。
- `insufficiencyReasons`：逐条列出「哪个维度为何不足」，让调用方**一眼看出「这次其实没证明什么」**，不必翻原始字节。

两字段在 `evaluation-report-3.0.schema.json` 与 `-3.1.schema.json` 均以**可选属性**加入（不进 required，旧 fixture 不破）。关键回归：空/空输出用例的 `matchedDimensions=0`、`sufficientDimensions=0`、`coverageRatio=0.0`、`insufficiencyReasons=["output: inconclusive — …"]`。全套件 **432 passed**。

## 8. 冻结路径与部署验收更正（2026-10-11）

这是当前验收判据补充，不是新平台实现或原始 evidence 的重判。依据本轮提供的对账/结果复核材料及[评估准备契约 §5](../../../../references/framework/evaluation-readiness-contract.md#5-原始观察采信与归因)：字节一致、维度可比较和冻结业务路径有效是三个不同问题。

1. **非空不等于充分**：确认冻结 argv/stdin 实际送达且程序到达预期状态。非空 usage 只能支持已冻结的用法错误路径；业务 argv 被吞而仅打印 usage，仍缺业务路径证据。D2-177 原 job 原判保留，后续验收先核它对应的精确冻结输入，不能从 stderr 同形直接认定业务一致。
2. **驱动诊断须区分来源**：D2-024 相同 DRIVER-FAILURE 可作为两侧诊断字节相同的事实，不足以支持程序业务 matched。只凭标记文本或退出码也不能建立来源；必须有合法来源驱动的精确版本、启动/状态/观察/清理证据。平台如何表达来源由它的正式契约决定，Agent 不自行新增 schema 或比较器。
3. **静默不是通用失败信号**：只有空输出不能区分“工作完成”和“未工作”时才不足。若有真实退出/副作用证据，足以满足冻结 oracle，可形成有效观察；不能从旧全空退化实现反推所有静默程序均无效。
4. **字段统计不是路径证明**：coverageRatio / sufficientDimensions 按实际部署定义解释；仍逐项阅读原始观察、输入送达和状态到达证据。not-applicable 不证明行为不存在或隔离有效，不能只看字段不看 evidence。
5. **已实现与已部署分开**：§7 的测试与证据复算记录只说明对应历史版本。新验收保存精确部署身份、原/新 job 关联和原始回传；失败原因分装置、源、环境、转换，不在项目报告把平台 FAIL 自改 PASS。

最小验收在获批隔离环境由合法提供者的既有精确输入/入口完成，Agent 不写驱动。本轮只登记任务，不执行：

| 保持不变 | 单一变化 | 预期信号 | 回收证据 |
|---|---|---|---|
| 程序/驱动/部署 | 冻结 argv 从合法 usage 错误路径改为有效业务参数 | usage 不能继续支撑业务路径结论，须采实际业务观察 | 冻结变体、参数送达、双侧原始输出/副作用 |
| 冻结目标与部署 | 合法提供者的入口从可达状态版本换为故障版本 | 同一失败标记不支持业务 matched | 两版入口来源/哈希、状态与清理记录 |
| 同一服务/部署/输入 | 观察目标从端口就绪扩到既定响应/日志 | 只见端口不满足扩展义务；需实际响应/日志 | oracle 变体、实际流/响应、终止记录 |
| 静默程序/输入/部署 | 采集增加已声明的业务文件维度 | 不再以空 stdout 推定未工作，仍核文件实际内容 | include 范围、原始文件证据/比较结果 |

有明确转换定位证据才进入有限模型修复。装置连续失败、缺合法来源或缺隔离实证时停止相应项，保留覆盖不足与恢复条件，不反复求 matched。

## 9. 独立平台仓库本地修订（2026-10-11，待验收）

用户提供 `third-party-evaluation-system` 后，比较器已在本地代码文本补双侧有效构建/执行、维度 coverage/诊断/limitations、输出及文件内容可用性核对；静默输出可由明确 include 范围内已完整采集并匹配的实际文件 digest 补充。汇总结论和 sufficientDimensions 均核 observed，报告及成功 reason 明确不独立证明冻结路径覆盖或输出来源。usage 单测注释也已更正为原始输出比较的回归，不能证明 D2-177 业务路径。

这不是对 §7 历史 job 的重判。当前仍不能靠比较器自动识别同形驱动诊断、业务 argv 被吞或服务只就绪；须按 §8 逐项采信。仅退出码相同、纯进程副作用和无副作用静默路径未由本次文件补充判据解封。已有 20ms 进程采样限制下的正面配对语义保留。

精确修改文件、待执行正反例与发布/回退边界的维护资料定位为独立仓库 `third-party-evaluation-system/docs/observation-quality.md`，不随转换仓库交付；平台维护者须另取精确版本。只完成代码/测试文本与静态审阅，没有 Python/pytest/服务/编译或样本执行，没有部署或真实验收；T1/T2/T8 的动态验收项继续未勾选。
