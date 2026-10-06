# Stage 1 升级计划｜从安全阻断到可控验证路径

## 1. 背景与问题定义

### 1.1 旧架构留下的可复用基础

旧仓库已经形成一条清晰的第三方评估分层：

```text
Agent / adapter
  -> Skill 与任务契约
  -> behavior obligations
  -> source/target comparison capsule
  -> Remote Controller
  -> VM Agent 双侧 build / execution / comparison
  -> canonical report
```

旧仓库的 `schemas/`、`behavior-obligations`、`conversion-result`、`skill-trace` 和 Gate A-E 仍可作为上层转换闭环的契约基础。它们已经明确区分：

- 静态语义义务链与动态证据链；
- 代码失败、环境失败、未验证和不支持；
- source/target 双侧构建；
- 证据引用、快照、重试和回滚；
- `not-observed` 不等于 `preserved`。

旧架构没有正式解决的，是第三方平台安全能力的机器可验证表达：

- 网络模式没有成为 Controller 的强制执行字段；
- Runner 能力矩阵没有声明“可证明的隔离能力”；
- `READY` / `clean` / snapshot rollback 不能证明默认路由已断开；
- 缺少 preflight 证明、attestation 过期时间和 Permit；
- 不能把网络、进程、凭据、持久化、注入、漏洞利用等行为映射到不同的执行配置；
- synthetic fixture / controlled target 没有统一输入、观察面、生命周期和证据协议；
- 阻断原因多为人工文本，难以恢复、重提、统计和审计。

### 1.2 当前轮次的可观测阻断

当前仓库已有记录表明：

- 三台现役 runner（Windows、Linux、macOS）已登记并支持快照回滚；Linux 基线为 R12，Windows 为 R11，macOS 为 R2。
- 2026-10-05 的无害探针在三台 VM 均观察到默认路由 `192.168.195.2`，而 Controller / runner 能力字段没有给出隔离证明；因此硬编码外部地址的 case 不能仅凭 `READY` 提交。
- `batch-01` 中安全未验证阻断占 27/40；`batch-02` 中逐例放行 13、阻断 27；后续批次仍有大量 `UNVERIFIED`，且另有 Go 工具链、源依赖和宿主隔离等环境阻断。
- 现有评估接口以 `capsule.zip`、`comparison_manifest.json`、`input_profile.json`、`metadata.json` 和 `/api/jobs` 为中心，尚未定义本文的 `SafetyPlan`、`Attestation`、`ExecutionPermit` 和 `FixtureManifest`。

### 1.3 设计判断

升级的关键不是“再增加 VM”，而是把执行前链路固定为：

```text
Task
  -> source behavior / safety facts
  -> Safety Planner
  -> required profile + fixture plan
  -> runner capability match
  -> fresh environment attestation
  -> execution permit
  -> capsule submission
  -> evidence validation
  -> disposition result
  -> snapshot revert + post-run attestation
```

## 2. 本阶段目标与非目标

### 2.1 目标

1. 给每个候选任务生成唯一、可审计、可重放的 `EvaluationDisposition`。
2. 将 `UNSAFE_NET`、`REVIEW_SUBPROC`、`UNSAFE_LOCAL` 从粗粒度阻断标签变为可组合的安全要求集合。
3. 为 Controller/Agent 增加逻辑 Execution Profile，而不改变三台 VM 的物理拓扑：
   - `SAFE_LOCAL`
   - `NETWORK_ISOLATED`
   - `PROCESS_RESTRICTED`
   - `LOCAL_FIXTURE`
   - `CONTROLLED_TARGET`
   - `STATIC_ONLY`
4. 让网络、数据、进程、资源、清理和证据要求真正进入提交和执行路径。
5. 任何运行前置条件不满足时，机器可判定为 `BLOCKED_*`，并能在环境修复后安全重提，不丢失也不重复执行。
6. 为 87 项建立“可控验证路径覆盖率”指标，而不是只统计真实运行 PASS。

### 2.2 非目标

- 不允许真实公网、生产网、真实 C2、真实凭据、个人资料、真实高价值目标。
- 不把注入、漏洞利用、内核/服务改写、真实持久化等行为默认转成可执行；只能在安全边界内建立受控靶标或观察替代。
- 不建设通用本地评测框架；Controller/Agent 的实现属于外部平台项目。
- 不改变转换 Skill 的语言规则来掩盖平台不能验证的问题。
- 不使用 comparison `matched`、模型自审或目标 build PASS 单独证明功能等价。

## 3. 目标状态模型

### 3.1 Evaluation Disposition

| Disposition | 适用条件 | 可报告内容 |
|---|---|---|
| `DIRECT_SAFE_RUN` | 无外部网络、无危险本机副作用、只读或一次性临时文件 | 双侧 build / execution / comparison（按 oracle） |
| `ISOLATED_NET_RUN` | 网络语义必须保留，但目标可替换为封闭实验网或 loopback | 连接、请求、错误路径和观察面证据；不报告公网成功 |
| `RESTRICTED_PROCESS_RUN` | 需启动子进程，但可限制树、资源、目标和时长 | process tree、argv 摘要、退出码、资源和清理证据 |
| `FIXTURE_EQUIVALENCE` | 凭据、浏览器资料、持久化表面、受控目标等可安全建模 | fixture 上的行为义务/观察面匹配；不报告真实系统效果 |
| `CONTROLLED_TARGET_RUN` | 需要专门的无真实数据、无出网靶标，且可证明生命周期隔离 | 靶标交互和结果状态；不报告真实漏洞/真实攻击成功 |
| `STATIC_ONLY` | 只能完成转换、自审和契约检查，动态义务没有安全替代 | 静态覆盖与未验证项；不能写 `passed` |
| `BLOCKED_UNMODELED` | 无法证明边界、无安全 fixture、依赖真实危险目标或 Permit 拒绝 | 阻断原因、恢复条件、责任方；保持未验证 |

### 3.2 结论与指标

本阶段必须同时报告：

- `dispositionCoverage = 有唯一 disposition 的任务数 / 87`；
- `permitEligibility = 满足 profile + attestation + fixture 约束的任务数 / 87`；
- `submitted = 实际提交到 Controller 的任务数 / 87`；
- `evidenceComplete = 获得完整证据包的任务数 / submitted`；
- `behaviorVerified = 在冻结 oracle/fixture 观察面上通过的任务数 / 有效 oracle 任务数`；
- `blockedUnmodeled` 单独列出，不允许并入 `UNVERIFIED` 后隐藏。

## 4. 分阶段路线

### Phase 0｜基线冻结与差异校准

**输出：** 87 项清单、分类映射、现役 Controller/Agent 能力快照、协议版本和风险台账。

**门槛：** 87 项每项都有源码/契约哈希、真实行为证据位置、当前阻断理由和候选 disposition。若数量或分类无法与仓库数据对齐，先形成差异记录，不得进入灰度执行。

### Phase 1｜只读 Safety Planner

**输出：** planner 输入/输出 schema、确定性规则、冲突处理、人工 override 记录和 dry-run 报告。

**门槛：** 不提交样本；同一输入重复规划得到同一 plan/hash；危险能力被拆成可解释的原子要求；不能规划的任务明确 `BLOCKED_UNMODELED`。

### Phase 2｜Runner Capability 与 Attestation

**输出：** runner 能力字段、网络隔离探针、进程/资源/文件清理证明、Attestation 签名或哈希链、过期策略。

**门槛：** 用无害 fixture 验证三台 runner 的 capability claim 与现场状态一致；默认路由、DNS、代理、出站防火墙和 Controller/artifact 例外均有证据。`READY` 只表示服务可用，不再表示可安全运行。

### Phase 3｜Execution Profile 与 Permit

**输出：** profile policy、Permit 签发/拒绝接口、capsule 绑定关系、撤销和过期机制。

**门槛：** 未持有与 task/case/source/target/profile/attestation 绑定的 Permit，Controller 不接受执行；修改 capsule 哈希、runner、网络模式或 fixture 版本后 Permit 失效。

### Phase 4｜Fixture/Controlled Target Runtime

**输出：** fixture registry、fixture manifest、数据生成、观察适配器、前后置清理、oracle 映射。

**门槛：** 先从合成凭据、临时文件、loopback HTTP/TCP 和受限子进程开始；注入/漏洞利用/真实持久化保持 `BLOCKED_UNMODELED`，直到有独立批准的安全靶标和最小实验。

### Phase 5｜87 项分层灰度

**顺序：** `SAFE_LOCAL` → `NETWORK_ISOLATED` → `PROCESS_RESTRICTED` → `FIXTURE_EQUIVALENCE` → `CONTROLLED_TARGET_RUN`。

**门槛：** 每一层先做 3–5 项最小实验，再扩大到该层完整集合；任何环境失败不倒填历史结果，修复后生成新 run/version。

### Phase 6｜迁移、回归与封版

**输出：** 新旧 Controller 报告对照、87 项 disposition 汇总、未达标项、回滚点和运维手册。

**门槛：** 旧 capsule 在 compatibility mode 下仍可获得原有 build 结果；新 profile 只增加安全前置，不改变已冻结代码/目标输入；所有差异可追溯。

## 5. 主要风险与取舍

| 风险 | 取舍 | 控制措施 |
|---|---|---|
| 误把默认路由当成隔离失败而停掉所有安全样本 | 保留逐例放行 | profile 绑定；仅网络需求任务强制网络 Attestation |
| 为了“87/87”过度构造空桩 | 宁可 `STATIC_ONLY/BLOCKED` | Fixture 必须覆盖真实行为义务，不能删核心路径 |
| Controller 协议升级破坏旧 capsule | 先 compatibility mode | 版本协商、旧 schema 原样留证、双报告校验 |
| 隔离声明与现场状态漂移 | Attestation 有效期短且绑定 runner/快照 | 提交前和运行后均核验；异常自动撤销 Permit |
| fixture 通过被误读成真实攻击成功 | 分开 `evidenceMode` 和 `outcome` | 报告模板禁止使用 ambiguous `passed` |
| 长时间运行、子进程或资源耗尽 | 统一预算和 kill/revert | PID tree、CPU/memory/wall clock、强制回滚 |
| 真实凭据泄露到日志 | 只生成合成数据并做内容扫描 | fixture 版本、secret scan、artifact allowlist |

## 6. 决策门

- **Gate S0：** 87 项口径一致，或者差异被正式登记并明确不纳入本阶段。
- **Gate S1：** Safety Planner 只读结果稳定、可解释、不可绕过。
- **Gate S2：** 网络/进程/数据 Attestation 能证明 profile 条件，而不是只报 READY。
- **Gate S3：** Permit 对输入和环境绑定，旧 API 不可绕过新安全门。
- **Gate S4：** fixture 证据能回指行为义务和观察面，不能只返回字符串 matched。
- **Gate S5：** 3–5 项灰度完成后才扩展；失败分为代码、环境、fixture、policy 四类。
- **Gate S6：** 87 项全有 disposition，剩余 `BLOCKED_UNMODELED` 的原因和解除条件可审计。
