# Stage 3 任务清单（平台侧）

> 状态：**ACTIVE** ｜ 建立 2026-10-10 ｜ 依据：dataset-2 实测
> 本清单只列**平台侧**工作。转换系统侧由另一智能体负责，见 README §6。

## 优先级总览

| # | 任务 | 优先级 | 类型 | 解封/收益 | 成本 |
|---|---|---|---|---|---|
| T1 | 修复 C# evidence-bundle schema 不一致 | **P0** | 缺陷 | 38 项（13.7%） | 小 |
| T2 | 新增"观测充分性"判定 + coverage 字段 | **P0** | 正确性 | 消除**假阳性**类 | 中 |
| T3 | 修正分类器 hostname 假阳性 | P1 | 缺陷 | 解封误阻断项 | 小-中 |
| T4 | `processes` 维度接入比较器 | P1 | 软缺口补全 | 进程行为类用例 | 中 |
| T5 | 网络隔离 Attestation / Permit | P1 | 能力扩充 | 解封硬编码外联类 | 中（安全相关） |
| T6 | `network` 维度采集器 | P2 | 能力扩充 | 见 C2 §2：本批非主要瓶颈 | 高 |
| T7 | `registry` 维度采集器 | P3 | 能力扩充 | **本批无消费方** | 中 |

## T1 —— C# evidence-bundle schema

- [ ] 选择修法：放宽 schema（推荐，保留 `detail`）或停写 `detail`
- [ ] 用 D2-007 原始 capsule 重提，`targetLang=csharp`
- [ ] 验收：不再 `INFRA_ERROR / AGENT_UNAVAILABLE / $.collectorDiagnostics.0`
- [ ] 验收：目标侧 preflight 不得为 `SKIPPED`
- [ ] 回归：非 C# 目标仍 `COMPLETED`

规格：[specs/C0-csharp-evidence-schema.md](../specs/C0-csharp-evidence-schema.md)

## T2 —— 观测充分性（**最高价值**）

- [ ] 定义不足情形：双侧观察均为空；或双侧 exit 相同且非 0 且输出均空；或观察与驱动失败标记同形
- [ ] 不足以支撑结论时**不得**输出 `matched`（新增 `inconclusive` 或等价标注）
- [ ] `coverage` 增加 `sufficientDimensions` / `insufficiencyReasons`
- [ ] 验收正例：D2-029（job-01 **+** job-04-probe-dash-arg）、D2-024 job-04 **不得**再判 matched
- [ ] 验收反向回归：两侧有实质且相同输出时**仍**判 matched（锚点 D2-177 `which.c` job-01：stderr 同为 `usage: which …`）

规格：[specs/C3-observation-sufficiency.md](../specs/C3-observation-sufficiency.md)

## T3 —— 分类器 hostname 假阳性

- [x] 路径构造上下文中的字符串不计为网络目标（如 `filepath.Join`、`os.path.join`）——v2.4 已实现（`_looks_like_filename` + 上下文排除）
- [x] 含常见文件扩展名且无 `://`／无端口／无 `@` 的裸串降级——v2.4 已实现（`FILENAME_EXTENSIONS`）
- [x] 验收正例：D2-055 形态（`filepath.Join(root,"demo.txt")`）不再判网络目标——回归 `test_filename_literal_in_path_context_is_not_a_network_target`
- [x] 验收反例/回归：真实主机名（+`net.Dial`）仍 `BLOCKED`、硬编码 IP（D2-108 `10.9.1.6`+`WSAConnect`）仍判网络目标——回归 `test_real_hostname_with_network_api_is_still_a_target`、`test_hardcoded_ip_with_wsaconnect_is_still_a_target`
- [x] 回归用例已补入 `test_safety_classifier_v2.py`，**50/50 通过**（本机仅跑分类器自测，非转换样本）

> v2.4 落地：classifier SHA `441b4d50…6524`（v2.3）→ `009a6f31…f3a4`（v2.4，33840 B）；回归 SHA `02bbee96…`→`45faa8e4…b372`（20311 B，47→50 用例）。

规格：[specs/C5-classifier-false-positive.md](../specs/C5-classifier-false-positive.md)

## T4 —— processes 接入比较

- [x] `comparison.dimensions.processes.applicable` 改为 `true`（`_compare_process_dimension` 对 observed/observed 返回 `applicable=true`）
- [x] 比较语义按**正面冲突**定 `mismatched`：先配对再比字段，**presence/absence 两个方向都不单独判 FAIL**（降为 `info`，`rule=process-sampling-unpaired`）
- [x] `exitCode` 两侧非 null 时严格比对（`rule=process-exit-code-conflict`）；`processIdRef` 只比拓扑形状（`_process_depth`）；`terminationReason=unknown` 不计差异
- [x] 验收（单元）：配对正例 `matched`、退出码冲突 `mismatched`、双向抖动不 mismatch、仅未配对→`inconclusive`、unknown termination 不计差异（`test_evidence_comparator.py` 6 例）
- [x] 验收（集成）：改写 `test_phase1_scenarios.py`——源侧独有子进程不再判 mismatch（原 `missing→mismatched` 已按 §4 作废），新增退出码冲突→mismatch
- [ ] 真实 probe 验收（判据 1 probe-processes applicable=true；判据 3/4 采样抖动 + >20ms 存活样例）须在平台获批隔离环境运行——**本机只跑平台 pytest，不跑转换样本**

> 落地：`evidence_comparator.py` 旧 `_compare_process_events`（走通用 presence/absence 判定、会假 FAIL）→ 新 `_compare_process_dimension`（§4 配对语义，自带 status）。平台全套件 **433 passed**。

规格：[specs/C1-processes-comparison.md](../specs/C1-processes-comparison.md)

## T5 —— 隔离 Attestation / Permit（🟡 逻辑层已做，运行时层待隔离环境）

- [x] 报告增加 `isolation` 块（report schema 3.0/3.1 可选属性 + `build_isolation_section` + markdown 渲染）
- [x] `verifiedBy` 必须是**运行时可核对的实证**：`evaluate_isolation_attestation` 要求含 `sha256:<64hex>`，否则 `permitted=False`
- [x] 负例：attestation 缺失/布尔/口头声明 ⇒ `permitted=False`（单元覆盖缺失、非证据串、裸布尔、未知 egressPolicy、缺 verifiedAt）
- [x] 一致性检查：`check_egress_consistency`——声明 deny-all 却观察到非许可目标 connect **成功** ⇒ `EGRESS_POLICY_VIOLATION`（refused 不算突破）
- [x] 文档明确：**采集能力 ≠ 隔离能力**（README §5.1 🟡 注 + `isolation.py` 模块注释）
- [ ] 运行时层：VM 内防火墙规则哈希采集、提交流程门禁接线（拒绝无可核对 attestation 的外联作业）、D2-108/D2-083 真样本放行与验收 ⇒ **隔离环境**

> 落地：`evaluation_core/isolation.py`（门禁 + 一致性 + 报告块装配）+ 契约 schema `isolation`/`isolationAlarm` + `field-registry.md` 登记。单元 12 例。

规格：[specs/C7-isolation-attestation.md](../specs/C7-isolation-attestation.md)

## T6 —— network 维度（🟡 比较/分类已做，采集器待运行时）

- [x] `classify_network_target`：loopback/private/public/special/unknown（供安全边界判定与 C7 一致性共用）
- [x] `_compare_network_events`：connect/listen/accept 按 eventType+分类+端口集合比对；公网目标 presence/result 冲突 `major`→mismatched，loopback/private 差异 `minor`；ephemeral 源端口不入 connect 目标故不假 FAIL
- [x] 单元 17 例（13 分类 + identical/public-only/loopback-minor/result-conflict）
- [ ] 运行时层：VM 内真实 syscall 网络采集器 + 能力位上报 + 观测义务预检放行 ⇒ **隔离环境**；**在采集器落地前不虚报 `network` 能力，现网仍按既有口径硬拒**，避免「接受了却采不到」比诚实硬拒更糟

> 口径：C2 §2 已论证本批 network 主要瓶颈是**隔离证明（C7）而非采集**；故本机优先交付分类/比较逻辑以支撑 C7，采集器留运行时。

规格：[specs/C2-network-collector.md](../specs/C2-network-collector.md)

## T7 —— registry（延后项）

- T7（`registry`）：见 [specs/C6-registry-collector.md](../specs/C6-registry-collector.md) §2，**本批无消费方，建议暂不实施**

## 我方（转换侧）配合事项

以下**不是**平台任务，但需与平台改动同步，否则收益无法落地：

1. **冻结口径修正**：后续用例应申请 `dimensions: ["output","filesystem"]`（必要时加 `processes`），
   而不是一律只申请 `output`。dataset-2 的 105/106 份只申请了 output，
   导致文件类用例只能靠"驱动回显"代偿。
2. **filesystem 保护范围**：按业务需要写 `comparisonPolicy.filesystem.include`，
   避免 `**/*` 这类全范围模式把编译产物也纳入比较。
3. **oracle 可冻结性前置检查**：含活动计数器／随机数／并发顺序的可观察量，
   应改由驱动固定输入后再冻结，而不是指望消噪 token 覆盖。
