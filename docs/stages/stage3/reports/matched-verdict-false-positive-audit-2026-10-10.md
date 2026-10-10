# `matched` 判定假阳性全量审计（2026-10-10）

> 文档类型：审计报告（report，**追加式，不改写原始证据**）
> 状态：**FINAL** ｜ 方法：read-only 搜索定位候选 + 逐项人工核对原始 bundle，无脚本
> 目的：核对 [C3 观测充分性](../specs/C3-observation-sufficiency.md) 之外是否还有被 `matched` 掩盖的假阳性

## 1. 范围与方法

- **范围**：dataset-2 全部 `behaviorVerdict:"matched"` 的 `comparison.json`，共 **33 份**。
- **候选特征**（取自 C3 的不足情形定义）：
  - **A**：两侧 `execution` 的 stdout **且** stderr 均为空（0 字节），且 `exitCode` 相同且**非 0**；
  - **B**：两侧 stderr 为**同一条驱动失败标记**（`DRIVER-FAILURE` / `readiness banner was never observed` 等）。
- **核对**：候选均打开 `evidence-source.json` / `evidence-target.json` 的 `execution` 原文逐字段确认，**不以摘要代替**。

## 2. 结论：假阳性仅集中在 **2 个用例**，但 D2-029 多一个受污染 job

| 用例 | job | 两侧 exit | 两侧 stdout | 两侧 stderr | 平台 verdict | 判定 |
|---|---|---|---|---|---|---|
| **D2-029**（`c-to-cpp/stest-fs-posix-to-win`） | `job-01-dual-build` | 1 / 1 | 空 / 空 | 空 / 空 | matched | **假阳性**（C3 已记） |
| **D2-029** 同用例 | `job-04-probe-dash-arg` | 1 / 1 | 空 / 空 | **空 / 空** | matched | **假阳性（本次新增）** |
| **D2-024**（`c-to-cpp/c01-linux-win-network`） | `job-04-loopback-listen-live-capture` | — | 空 / 空 | 同一条 driver-failure | matched | **假阳性**（C3 已记，特征 B） |

**新增发现**：D2-029 的 `job-04-probe-dash-arg` 与已记录的 `job-01` **同病同源**（空 argv／dash-arg 进入退化分支 → 两侧什么都没跑 → 两侧全空 → 判 matched）。
⇒ **污染在一个用例内跨多个 job**，C3 原先只列了 job-01，应把 job-04 一并纳入。

## 3. 核对为**真匹配**、明确不降级的样例（防矫枉过正）

| 用例 | job | 现象 | 为何**不是**假阳性 |
|---|---|---|---|
| **D2-177**（`c-to-python/D2-177-c-c-which.c`） | `job-01-dual-build` | 两侧 exit 1、stdout 空 | 两侧 stderr **逐字节相同且有实质内容**：`usage: which [-as] program ...`（31 B，digest `b0b305a2…`）。这是被测程序**自身**的用法输出，属真实可观察行为，**符合 matched** |

其余 **30 份** matched 均在两侧有实质且一致的 stdout/stderr，非退化，保持原判。

## 4. 处置

1. **原始 `comparison.json` 一律不改写**（证据保真，[安全边界](../../../references/framework/safety-boundary.md) / 开发规范 §6）。
2. 上表 **3 个 job** 的**行为结论**应读作 **`INCONCLUSIVE` / `UNVERIFIED`**，不得计入「行为一致」；涉及的 D2-029、D2-024 两用例的 `result.md` 与 item 记录按此口径更新（属转换系统侧交付，另交该侧处理）。
3. 本审计作为 **C3 的追加验收材料**：C3 实现后，这 3 个 job 复跑**均不得**再返回 `matched`；D2-177 job-01 复跑**仍须** `matched`（反向回归）。

## 5. 可复现指针（原文未改写）

```
D2-029 job-01 : docs/test/dataset-2/c-to-cpp/stest-fs-posix-to-win/output/batch/04-evaluation/job-01-dual-build/returned-evidence/
D2-029 job-04 : docs/test/dataset-2/c-to-cpp/stest-fs-posix-to-win/output/batch/04-evaluation/job-04-probe-dash-arg/returned-evidence/
D2-024 job-04 : docs/test/dataset-2/c-to-cpp/c01-linux-win-network/output/batch/04-evaluation/job-04-loopback-listen-live-capture/returned-evidence/
D2-177 job-01 : docs/test/dataset-2/c-to-python/D2-177-c-c-which.c/output/batch/04-evaluation/job-01-dual-build/returned-evidence/  （真匹配，留作反向回归）
```
