# 平台观察维度能力实测（2026-10-10）

> 文档类型：实测报告（report）
> 状态：**FINAL** ｜ 方法：正式 `POST /api/jobs` + 原始回传取证 ｜ 无脚本，逐项手工提交
> 目的：回答"平台现有观察维度到底哪些能用"（B 类问题）

## 1. 背景：一次需要更正的判断

2026-10-10 我向用户提交的分析中称："平台 filesystem/processes/registry/network 全部不可用，
大批文件类用例结构性无法验证"。

**该结论错误。** 核对 dataset-2 全部 `input_profile.json` 后发现：**106 份中 105 份只申请了 `output`**。

```
105 x {"dimensions":["output"]}
  1 x {"dimensions":["output","filesystem"],"filesystemInclude":["**/*"]}
  1 x {"dimensions":["output","filesystem"],"filesystemInclude":["out/**"]}
```

平台的 `not-applicable` **反映的是调用方的申请**，不是平台能力。
两个早期 job（D2-003）已证明 filesystem 可用，其中一个还**检出了真实差异**。

⇒ 因此改为**主动探测**：逐一申请各维度，读取平台的真实响应。

## 2. 探测方法

三个无害合成样例，全部 loopback/本地、无外部目标、无真实凭据：

| 探测 | capsule | 申请维度 | jobId |
|---|---|---|---|
| P1 | `platform-probes/probe-processes` | `output`,`filesystem`,`processes` | `eval-20261010-082649-4a384b16` |
| P2 | `platform-probes/probe-network` | `output`,`network` | `eval-20261010-082922-edde923c` |
| — | D2-003（既有证据复核） | `output`,`filesystem` | `…054357…` 等 2 个 |

程序行为：P1 为 C `fork`+`/bin/echo`+写一个文件，对照 Python 等价实现；P2 为 loopback 自连（`127.0.0.1:19099`）。

## 3. 逐维度结论

| 维度 | 采集（evidence bundle） | 比较（comparison） | 判定 |
|---|---|---|---|
| `output` | `observed` | `applicable:true` | **完整支持** |
| `filesystem` | `observed`，含 `digestAfter` | **`applicable:true`，`matched`，diffs=0** | **完整支持** |
| `processes` | **`observed`**（1–2 条 `process.lifecycle`） | **`applicable:false`，`not-applicable`** | **软缺口** |
| `network` | **提交即被拒** | n/a | **硬缺口** |
| `registry` | 平台自陈 out of scope | n/a | 声明不支持（未实测） |

## 4. 关键区分：**采集能力 ≠ 比较能力**

`processes` 的实测结果最能说明问题——**同一维度在证据与比较两处给出不同状态**：

```
evidence-source.json  ->  observations.processes.status = "observed"   (1 event)
evidence-target.json  ->  observations.processes.status = "observed"   (2 events)
comparison.json       ->  dimensions.processes = { applicable: false, status: "not-applicable" }
```

⇒ 分两层看：

| 层 | processes 现状 |
|---|---|
| **采集**：runner 能否录到事件 | **能**。事件含 `imageName`、`commandLine`、`exitCode`、`terminationReason`、`processIdRef`、`parentProcessIdRef` |
| **比较**：比较器是否给该维度打分 | **不能**。标记为 `not-applicable` |

**含义**：`processes` 不需要新采集器，**只需要把已有证据接进比较器**。这是低成本高收益项。

## 5. 平台自陈的采样限制（重要）

`processes` 维度的 `limitations` 原文：

> `Process descendants are sampled every 20ms; shorter-lived descendants may be missed.`

实测吻合：P1 的 **source 侧只看到 `p0`**（外层 `python run_case.py`），
**target 侧看到 `p0` + `p1`**（子 `python <workspace>/target.py`）。
两侧都确实产生了子进程，但采样窗口使短命子进程**可能漏掉**。

⇒ 若将来把 processes 接入比较，**必须把它当"采样证据"而非"完整轨迹"**，
  不能用"某侧少了 N 条进程事件"直接判转换失败。

## 6. `network` 是**硬**缺口，且平台的处理方式是**正确的**

提交 `dimensions: ["output","network"]` 后立即返回：

```json
{ "jobStatus": "INFRA_ERROR",
  "message": "observation obligations cannot be met: source,target",
  "lastError": { "code": "RUNTIME_UNAVAILABLE",
                  "message": "observation obligations cannot be met: source,target",
                  "owner": "runner", "phase": "QUEUED", "retryable": false } }
```

**为什么这是好行为**：

1. 在 **QUEUED** 阶段就拒绝，**没有浪费一次执行**；
2. `owner: runner` + `retryable: false`，责任层与稳定性标注正确；
3. **没有**静默接受再报 `not-applicable` —— 若那样，调用方会把"没观察"误当"等价"。

这与 §7 的假阳性问题恰好相反：**该硬的地方硬了**。

## 7. `filesystem` 实测细节（可直接用于后续冻结）

事件结构（P1，两侧**逐字节相同**）：

```json
{ "eventType": "filesystem.created",
  "sequence": 0, "timestampOffsetMs": 0,
  "data": { "relativePath": "probe-artifact.txt",
            "objectType": "file",
            "sizeBefore": null, "sizeAfter": 14,
            "digestBefore": null,
            "digestAfter": "sha256:db70daba8d2b849c8f2d18fb51842eb893af6bbe2c3b350a74a90107392a7ac1",
            "contentKind": "text", "structuredSummary": null } }
```

另有 D2-003 的既有证据显示该维度**能检出真实差异**：

```
filesystem: mismatched
  path: observations.filesystem.program.exe
  source digest: sha256:fedbd584128676703b579a0aabf75837aff15f553412c9e6703239de357b9297
  target digest: sha256:d14fd755767fd712fb65b6fdd3e53358e6941aff64eeca985ea6cd03c3517a94
```

⇒ 该维度**不是摆设**：采集、摘要、比对、检出差异，四件事都成立。

## 8. 对转换侧的直接含义（须与转换系统侧同步）

dataset-2 中以下用例的**核心行为就是文件系统副作用**，本可用该维度直接验证，
但我只申请了 `output`，只好靠"驱动回显文件内容"把副作用塞进 output：

| 项 | 行为 | 当时做法 | 本可做法 |
|---|---|---|---|
| D2-020 | 写 `access_audit.log` | 未比较（记为缺口） | filesystem 维度比对 |
| D2-056 | 写 `sample.txt`、`bootstrap-config.json` | 驱动回显 | filesystem 维度比对 |
| D2-058 | 写 `child-output.txt` | 驱动回显 | filesystem 维度比对 |
| D2-104 | 改名 `sample.txt`→`sample.locked` | 未比较 | filesystem 维度比对 |
| D2-105 | 批量改名 + 追加 `impact.log` | 未比较 | filesystem 维度比对 |
| D2-106 | 写 `manifest.txt` | 未比较 | filesystem 维度比对 |

⇒ **这是冻结口径问题，不是平台能力问题**，应在下一批次的标准做法中修正。

## 9. 复现方式

两个 capsule 与其原始回传完整保存在：

```
docs/test/dataset-2/batch/platform-probes/probe-processes/   (PROBE-RESULT.md + returned-evidence/)
docs/test/dataset-2/batch/platform-probes/probe-network/     (PROBE-RESULT.md + 平台原诊断)
```

原始 `evaluation_report.json` / `evidence-source.json` / `evidence-target.json` / `comparison.json`
**原样落盘、未改写**。