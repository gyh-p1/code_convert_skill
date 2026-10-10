# C3 + C4（最高优先）："两侧均无观察"判定与观测充分性报告

> 类型：**正确性缺陷修复** ｜ 优先级：**P0**（与 C0 并列）
> 依据：dataset-2 实测 **2 例假阳性**

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
