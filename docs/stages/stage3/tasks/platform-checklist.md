# Stage 3 任务清单（平台侧）

> 状态：**ACTIVE** ｜ 建立 2026-10-10 ｜ 依据：dataset-2 实测
> 本清单只列**平台侧**工作。转换系统规则/证据任务见 [Stage 4](../../stage4/tasks/evidence-quality-checklist.md)。2026-10-11 更新：已勾选的历史实现/测试记录不等于已部署或样本验收；本轮只做文本修订，不执行平台测试、部署或 job。

## 优先级总览

### R15/R16 源码候选收尾（2026-10-12）

- [x] 本批流摘要/双通道引用候选回读；报告展示实际构建与退出/超时、配置比较通过维度及 matched/semantic-match 两类，不反算缺明细统计或改 JSON 原义。
- [x] 幂等/启动恢复补不可读和非对象请求/状态、损坏 manifest 角色/分配以及报告失败的阻断；不重放、不删除原材料、不推清理成功。具体当前文件和边界见[六项收尾](../../stage4/r11-r16-closeout-2026-10-12.md)。
- [x] SOURCE_TEXT_COMPLETE / STATIC_REVIEWED；独立源码仓库说明已追加，原生 Git 空白检查。没有运行测试/解析器/平台/VM，未构建部署，不访问 Controller 安装目录/jobs。
- [ ] 全量回归与实际发布身份/部署/真实恢复验收，待用户确认及合法材料/适用隔离。

此小节只关闭本批 R15/R16 源码维护，原 T1–T8、C3 及历史验收状态分别保留，不宣称全部平台能力已通过。

| # | 任务 | 优先级 | 类型 | 解封/收益 | 成本 |
|---|---|---|---|---|---|
| T1 | 修复 C# evidence-bundle schema 不一致 | **P0** | 缺陷 | 38 项（13.7%） | 小 |
| T2 | 新增"观测充分性"判定 + coverage 字段 | **P0** | 正确性 | 消除**假阳性**类 | 中 |
| T3 | 修正分类器 hostname 假阳性 | P1 | 缺陷 | 解封误阻断项 | 小-中 |
| T4 | `processes` 维度接入比较器 | P1 | 软缺口补全 | 进程行为类用例 | 中 |
| T5 | 网络隔离 Attestation / Permit | P1 | 能力扩充 | 解封硬编码外联类 | 中（安全相关） |
| T6 | `network` 维度采集器 | P2 | 能力扩充 | 见 C2 §2：本批非主要瓶颈 | 高 |
| T7 | `registry` 维度采集器 | P3 | 能力扩充 | **本批无消费方** | 中 |
| T8 | 精确部署身份与能力验收 | **P0** | 验收 | 区分已实现、已部署和可消费 | 中 |

## T1 —— C# evidence-bundle schema

- [x] 规格已记录 schema 接受 `detail`，producer 与 fallback 均补 `dimension:null`（C0 §5.1）；不再仅按“放宽 schema”验收
- [x] 2026-10-11 静态核对独立平台仓库实际 producer/fallback；在原 Agent 测试中补 source/target 两侧实际产出路径的 schema 回归**文本**，未执行测试。维护资料定位为独立仓库 `third-party-evaluation-system/docs/observation-quality.md`，不随转换仓库交付
- [ ] 取得精确部署身份、实际 schema/producer/fallback 对应版本后，用 D2-007 原始 capsule 在获批隔离环境重提，`targetLang=csharp`；保留原失败与新 job 关联
- [ ] 验收：不再 `INFRA_ERROR / AGENT_UNAVAILABLE / $.collectorDiagnostics.0`
- [ ] 验收：目标侧 preflight 不得为 `SKIPPED`
- [ ] 回归：非 C# 目标仍 `COMPLETED`

规格：[specs/C0-csharp-evidence-schema.md](../specs/C0-csharp-evidence-schema.md)

## T2 —— 观测充分性（**最高价值**）

- [x] 规格已记录全空观察退化判定及 `sufficientDimensions` / `insufficiencyReasons` 实现；这两个字段不证明冻结路径已经执行
- [x] 2026-10-11 平台本地代码文本补双侧构建/执行、维度采集与内容缺口核对；明确文件范围及真实完整 digest 可补充静默输出比较；报告显示不足原因和统计边界。已有 schema 保持，**未测试、未部署**；维护资料定位为独立仓库 `third-party-evaluation-system/docs/observation-quality.md`，不随转换仓库交付
- [ ] 在获批外部验收环境执行该交接的现有套件及单变量正反例，保留精确版本和完整输出；未取得证据不把本地实现记为功能通过
- [ ] 扩充验收：核冻结输入实际送达、预期状态到达、程序输出与合法来源驱动诊断区分；不足以支撑结论时不得把原始字节相同采信为业务一致
- [ ] 验收正例：D2-029（job-01 **+** job-04-probe-dash-arg）、D2-024 job-04 **不得**再判 matched
- [ ] 反向回归须限定冻结路径：usage 错误路径明确为观察目标且输入确已送达时可比较；有业务 argv 却只取得 usage 的任务覆盖不足。D2-177 原 job 保留，不在本清单倒改历史 verdict
- [ ] 负例：纯驱动失败标记不作程序观察；服务只有端口就绪、没有约定响应/日志时不能满足更强观察义务；合法静默程序有符合 oracle 的实际退出/副作用时不因 stdout/stderr 空一律判未工作
- [ ] 验收不能只看 coverage 字段；逐项保留双侧原始观察、驱动来源/精确版本、冻结路径与项目采信结论

规格：[specs/C3-observation-sufficiency.md](../specs/C3-observation-sufficiency.md)

## T3 —— 分类器 hostname 假阳性

- [x] 路径构造上下文中的字符串不计为网络目标（如 `filepath.Join`、`os.path.join`）——v2.4 已实现（`_looks_like_filename` + 上下文排除）
- [x] 含常见文件扩展名且无 `://`／无端口／无 `@` 的裸串降级——v2.4 已实现（`FILENAME_EXTENSIONS`）
- [x] 验收正例：D2-055 形态（`filepath.Join(root,"demo.txt")`）不再判网络目标——回归 `test_filename_literal_in_path_context_is_not_a_network_target`
- [x] 验收反例/回归：真实主机名（+`net.Dial`）仍 `BLOCKED`、硬编码 IP（D2-108 `10.9.1.6`+`WSAConnect`）仍判网络目标——回归 `test_real_hostname_with_network_api_is_still_a_target`、`test_hardcoded_ip_with_wsaconnect_is_still_a_target`
- [x] 回归用例已补入 `test_safety_classifier_v2.py`，**50/50 通过**（本机仅跑分类器自测，非转换样本）

> v2.4 落地：classifier SHA `441b4d50…6524`（v2.3）→ `009a6f31…f3a4`（v2.4，33840 B）；回归 SHA `02bbee96…`→`45faa8e4…b372`（20311 B，47→50 用例）。

- [ ] 核登记分类器、回归套件与实际消费版本的完整 SHA，不以 v2.4 标签或上述缩略值代替
- [ ] 增补纯分隔符/标点字符串的假阳性验收，并与真实 hostname、IP、端口和网络 API 上下文反例成对核对；只改变字面值或上下文一个变量，不为解封真实外联放宽安全准入

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
   先核是否有合法来源、精确版本的入口可固定输入/初始状态；缺来源记准备缺口，不让 Agent 新写或委托模型生成驱动。需改变条件时记录关联变体，不覆盖原冻结，不指望消噪 token 覆盖。

## T8 精确部署身份与能力验收

- [x] 已定位平台仓库 `E:\桌面文档\Agents System\third-party-evaluation-system`，完成独立 source-only、build-only 及收尾/取证/恢复协议修订，相关路径纳入本地产品回归；沿用本阶段，不新增 Stage 5。维护者按精确版本取证，不以同级目录存在作为转换知识依赖
- [x] 已补源侧预检的可照做请求契约与强制加载路径：[当前协议适配 §2](../../../../references/adapter/controller/platform-revision-adapter.md#2-独立源侧预检请求)给出字段、源侧 capsule、manifest/profile/metadata、分类/授权要求及手工命令；不要求或接受 target 树
- [x] 已完成本轮 P0/P1 修订发布前审查：平台 655 项完整套件在 3.12.13 和精确嵌入式 3.12.10 均通过；安装器契约 pin 与源预检 oracle 摘要一致性已修正，转换适配按 1.0.29 当前协议同步；静态收口见[适配审查](../../stage4/evaluation-adaptation-review-2026-10-11.md)，真实 VM 验收仍另列
- [ ] 保存平台已提供的精确发布/部署标识，以及 Controller、VM Agent、比较器、报告 schema 和分类器的对应关系；不读取 Controller 安装目录或 jobs 取巧
- [ ] 分别核 C0/C3/C4/C1 的真实回传是否能消费；实现代码、单元测试记录和报告字段存在不替代真实 job 验收
- [ ] 按当前独立源预检/双侧仅编译协议取得真实 VM/job 验收：源构建、适用有效运行基线、仅编译未运行、原件与清理分别核对；缺件记准备缺口，不生成目标凑预检包
- [ ] C7 须有运行时隔离实证和实际提交门禁，C2 须有真实采集能力；采集与隔离分别验收，`READY`、快照或同机共处不替代隔离
- [ ] 每个验收项先核授权/逐例隔离与合法来源输入，再按原生工具手工单项推进，回收精确版本原始证据及清理记录；未通过不解除原 WAITING，不以旧 schema 拒收当作新转换失败

此任务是 Stage 3 的验收补充，不新增发布权限或平台能力。完成信号为相关能力在精确部署/合法输入下取得适用原始证据；版本未知、准备缺件或隔离不足即停止该项。历史测试数字不在本轮重验。
