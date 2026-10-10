# Stage 3：评估平台侧能力补强

> 文档类型：阶段定位与范围（stage hub）
> 状态：**ACTIVE** ｜ 建立：2026-10-10 ｜ 依据来源：dataset-2 实测（batchId=`batch`）
> 上游：[Stage 1](../stage1/README.md)（1.0.26 统一部署）｜ 本阶段只处理**评估平台侧**，转换系统侧由另一智能体负责

## 1. 为什么单独立阶段

dataset-2 推进到 46/277 项终态的过程中，**所有真实转换缺陷只有 1 项**（D2-025 的 C++ `case` 跨初始化，已修复并通过），
而阻断与返工**绝大部分来自评估平台侧与我们的对接口径**。
因此需要把平台侧的能力缺口**集中定案**，而不是继续在逐项转换里逐个撞到。

## 2. 本阶段要回答的两个问题（用户 2026-10-10 指定）

| # | 问题 | 本阶段的产出 |
|---|---|---|
| **A** | **B 类：平台现有能力到底能不能用？** | 实测结论 + 复现命令 + 原始证据（`reports/`） |
| **B** | **C 类：能力扩充要做什么、能不能做？** | 逐项可执行规格（`specs/`） |

用户已明确授权：**这些能力可以开放**。因此 `specs/` 下按"可施工"标准写，不写"建议考虑"。

## 3. B 类实测结论（**已完成，2026-10-10**）

四个观察维度逐一实测，方法与原始证据见 [`reports/platform-dimension-capability-2026-10-10.md`](reports/platform-dimension-capability-2026-10-10.md)。

| 维度 | 采集 | 比较（打分） | 结论 |
|---|---|---|---|
| `output` | ✅ 实时可用 | ✅ | **完整支持** |
| `filesystem` | ✅ 事件 + 内容 digest | ✅ **applicable / matched** | **完整支持** |
| `processes` | ✅ `process.lifecycle` 事件 | ❌ `not-applicable` | **软缺口：采了但不比** |
| `network` | ❌ **提交即在 QUEUED 被拒** | n/a | **硬缺口：完全不支持** |
| `registry` | 平台自陈 out of scope | n/a | 未实测（声明不支持） |

### 最重要的一条更正

**我此前报告"平台缺 filesystem 维度"是错的。**
实测与证据双向确认：`filesystem` **完整可用**（采集 + 打分 + 内容 digest 比对 + 能检出真实差异）。
dataset-2 中 **105/106 份** `input_profile.json` 只申请了 `dimensions: ["output"]`，
平台的 `not-applicable` **反映的是我的申请，不是它的能力**。

⇒ 这条**反转了对 C 类优先级的判断**：文件类用例的行为验证**现在就能做**，
  不需要等平台扩充能力；需要改的是**我方的冻结口径**。

## 4. C 类能力扩充（本阶段主要施工项）

| # | 项目 | 文档 | 类型 | 可行性 |
|---|---|---|---|---|
| C1 | `processes` 维度接入比较器 | [specs/C1-processes-comparison.md](specs/C1-processes-comparison.md) | **软缺口补全**，证据已在手 | **高** |
| C2 | `network` 维度采集器 | [specs/C2-network-collector.md](specs/C2-network-collector.md) | 新采集器 + 隔离问题 | **中**，受安全边界约束 |
| C3 | 比较器"两侧均无观察"判定 | [specs/C3-observation-sufficiency.md](specs/C3-observation-sufficiency.md) | 正确性缺陷，防假阳性 | **高** |
| C4 | 观测充分性报告字段 | 并入 C3 | 让调用方看到"观察够不够" | **高** |
| C5 | 分类器 hostname 启发式修正 | [specs/C5-classifier-false-positive.md](specs/C5-classifier-false-positive.md) | 假阳性阻断 | **高** |
| C6 | `registry` 维度 | [specs/C6-registry-collector.md](specs/C6-registry-collector.md) | 仅 Windows 有意义 | **低**（本批无用例，可延后） |
| C7 | 网络隔离 Attestation/Permit | [specs/C7-isolation-attestation.md](specs/C7-isolation-attestation.md) | 解封硬编码外联类用例 | **中**，安全相关，需谨慎 |

## 5. 优先级建议（按"解封用例数 ÷ 成本"）

| 顺序 | 项目 | 理由 |
|---|---|---|
| **1** | **C3 + C4** 观测充分性 | 直接消除**假阳性**这一类最危险的结果——它会让"什么都没验证"看起来像"验证通过"。dataset-2 已实测 2 例（D2-029 job-01、D2-024 job-04） |
| **2** | **平台 C# 阻断修复** | 一行 schema 问题，解封 **38 项（13.7%）**；详见 [specs/C0-csharp-evidence-schema.md](specs/C0-csharp-evidence-schema.md) |
| **3** | **C5** 分类器假阳性 | 低成本，避免整项被误阻断（D2-055） |
| **4** | **C1** `processes` 比较 | 采集已通，只差比较器接入；对进程行为类用例直接增益 |
| **5** | **C7** 隔离证明 | 解封 D2-083、D2-108 这类硬编码外联用例；**需与安全边界一并设计** |
| **6** | **C2** `network` 采集 | 成本最高；且**本批实测并未成为主要瓶颈**（多数网络用例是 loopback，stdout 已足够） |
| 延后 | **C6** `registry` | 本批无 registry 类用例，投产收益为零 |

## 5.1 实施进展（2026-10-10，平台仓库 `third-party-evaluation-system`）

> 平台仓库改动均在本机**编辑并运行其单元测试验证**（本机只是不运行**转换测试用例/样本**，不等于不能跑平台自身的 pytest）；
> 全套件 **466 passed**（evaluation-core 196 + vm-agent 86 + remote-controller 184）。涉及真实样本的最终验收仍须在平台获批环境进行。

| 项目 | 状态 | 验证 |
|---|---|---|
| **审计**：33 份 matched 全量复查 | ✅ 完成 | 新增 1 例假阳性（D2-029 job-04）；见 [reports/](reports/matched-verdict-false-positive-audit-2026-10-10.md) |
| **C0** C# schema | ✅ 已修（schema + producer `dimension:null` + fallback + 测试） | 发现并修正了「仅放宽 schema」不足以修复的隐藏缺陷 |
| **C3** 观测充分性（判定） | ✅ 已修（空/空→inconclusive，不再 matched） | 真实证据复跑 D2-029 两 job 由 matched→inconclusive，D2-177 保持 matched |
| **C4** coverage 报告字段 | ✅ 已做（`sufficientDimensions` + `insufficiencyReasons`，两 schema 可选属性） | 空/空用例 sufficient=0、coverageRatio=0 |
| **C5** 分类器 hostname 假阳性 | ✅ **完成**（classifier **v2.4** SHA `009a6f31…f3a4`；回归 +3 用例、测试 SHA `45faa8e4…b372`，**50/50 通过**） | `_looks_like_filename`（扩展名形态）+ 上下文排除修正 D2-055；真实主机名（+net API）与硬编码 IP 仍判网络目标（反例/回归已锁进套件）。本机只跑分类器自测，不跑转换样本 |
| **C1** `processes` 接入比较器 | ✅ **已做**（比较器实现 §4 语义 + 单元 + 集成测试） | `_compare_process_dimension`：先按 `normalizedImagePath`+`normalizedCommandLine`+拓扑深度配对，只有**配对成功且两侧 exit 非 null、termination≠unknown、退出码冲突**才判 `mismatched`；presence/absence（两个方向）降为 `info`→喂 C3，无可配对对象判 `inconclusive`。单元 6 例（配对/退出码冲突/双向抖动/仅未配对→inconclusive/unknown 不计差异）；集成改写 `test_phase1_scenarios.py`：源侧独有子进程不再判 mismatch（原 `missing→mismatched` 测试已按 §4 作废），新增退出码冲突→mismatch。**本机只跑平台 pytest，真实 probe 验收（判据 1/3/4 的采样物理前提）仍须隔离环境** |
| **C7** 网络隔离 Attestation/Permit | 🟡 **逻辑层已做**（attestation 门禁 + 一致性告警 + report `isolation` 块 + schema 3.0/3.1） | `evaluation_core/isolation.py`：`evaluate_isolation_attestation` 门禁——`verifiedBy` 必须含运行时可核对的 `sha256:<64hex>`（防火墙规则哈希），缺失/布尔/口头声明一律 `permitted=False`（负例落实「`READY`/`clean`/快照不等于已隔离」）；`check_egress_consistency`——声明 deny-all 但观察到非许可目标 connect **成功**则 `EGRESS_POLICY_VIOLATION` 告警（观察优先，refused 不算突破）；report 新增可选 `isolation` 块并在 markdown 渲染。单元 12 例。**真实防火墙规则采集、提交流程门禁接线、D2-108 真样本放行仍须隔离环境** |
| **C2** `network` 维度 | 🟡 **比较/分类已做**（比较器 + 地址分类；采集器留运行时） | `evidence_comparator`：`classify_network_target`（loopback/private/public/special/unknown，供安全边界与 C7 共用）+ `_compare_network_events`（按 eventType+分类+端口集合比对，公网目标 presence/result 冲突判 `major`→mismatched，loopback/private 差异降 `minor`，源短命 ephemeral 端口不入 connect 目标故不假 FAIL）。单元 17 例（13 分类 + 4 比较）。**本机不实现 VM 内真实 syscall 网络采集器，故不虚报 `network` 能力位——现网仍按既有口径硬拒 network 作业，直到隔离环境内落地采集器** |
| **C6** `registry` 维度 | ⬜ 未做（建议延后，本批无消费方） | 见 [specs/C6](specs/C6-registry-collector.md) |

> C7/C2 为什么标 🟡：平台**逻辑层**（分类、比较、门禁、一致性、契约、报告块）已在本机编辑并跑平台 pytest 通过；**运行时层**（VM 内网络采集、防火墙规则哈希采集、提交门禁接线、真实外联样本放行）**只能在平台获批隔离环境落地与验收**。两者边界即「采集能力 ≠ 隔离能力」。

## 6. 与本阶段无关的事项（明确排除）

- **转换系统侧的纪律与骨架缺口**：用户已交付其他智能体处理。
- **已发现的 20 项缺 `result.md`**：属转换系统侧交付完整性，不在本阶段。
- **27 个 `.tmp-classify-*` 残留**：属转换系统侧清理，不在本阶段。

## 7. 证据与可复现性

- 所有实测均通过正式 `POST /api/jobs` 提交，capsule 与原始回传保存在
  [`docs/test/dataset-2/batch/platform-probes/`](../../test/dataset-2/batch/platform-probes/)。
- 探测程序均为**无害合成样例**：无外部网络、无真实凭据、无破坏性操作。
- 平台原始诊断（含 `INFRA_ERROR` 原文）**保留不改写**。