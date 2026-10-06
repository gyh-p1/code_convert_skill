# Spec 02｜Execution Profile、Runner Capability、Attestation 与 Permit

## 1. 设计原则

`Execution Profile` 是安全策略，`Runner Capability` 是平台声明，`Attestation` 是现场证据，`Execution Permit` 是一次性授权。四者不能互相冒充：

```text
required profile
  ∩ runner capability
  ∩ fresh attestation
  ∩ fixture/oracle contract
  = permit eligible
```

## 2. Profile 定义

### 2.1 `SAFE_LOCAL`

- 网络：无出站或只允许 Controller 必要控制流量。
- 文件：只允许 capsule 工作区和临时目录。
- 进程：默认禁止非必要子进程。
- 数据：合成输入或公开固定数据。
- 清理：任务结束强制清理并 revert。

### 2.2 `NETWORK_ISOLATED`

- 在 `SAFE_LOCAL` 基础上允许 loopback 或封闭实验网。
- 必须声明 allowlist：目标身份、协议、端口、方向、时限。
- 禁止默认公网出口；Controller/artifact 例外必须有明确目的和审计。
- DNS 必须指向受控解析器或使用固定映射；不能悄悄回落公网 DNS。
- 连接、请求、响应摘要和拒绝事件纳入证据。

### 2.3 `PROCESS_RESTRICTED`

- 允许受控子进程，但绑定根进程、工作区、环境变量和资源预算。
- 记录 process tree、退出码、超时、被终止原因和资源峰值。
- 不允许子进程脱离 VM/fixture 边界；不能将宿主命令解释器、凭据目录或真实服务作为目标。
- 进程树未完整收集或清理失败，结果只能为 `INCONCLUSIVE`/`BLOCKED_ENV`。

### 2.4 `LOCAL_FIXTURE`

- 通过 fixture manifest 提供合成文件、合成配置、合成 credential/profile 或事务性持久化表面。
- fixture 必须可生成、可哈希、可重置、不可访问真实用户目录。
- 观察的是读取/写入路径、返回值、错误路径和状态变化，不是秘密内容本身。

### 2.5 `CONTROLLED_TARGET`

- 目标必须是登记过版本和 hash 的专用测试靶标/simulator。
- 不允许真实外部服务、真实高价值软件或不可回滚的系统对象。
- 目标行为只证明与该靶标的交互义务；不能外推到真实目标。

### 2.6 `STATIC_ONLY`

- 不授予执行 Permit。
- 允许保存转换、静态审阅和未验证义务；报告必须明确“未动态验证”。

## 3. Runner Capability 字段

建议 Controller 的 runner 返回以下可验证字段；未知字段不得默认为 true：

```json
{
  "runnerId": "linux-vm-agent-x64",
  "os": "linux",
  "arch": "x64",
  "baselineSnapshot": "CC-Eval-Linux-8Lang-R12",
  "agentBuildSha256": "sha256:...",
  "supportedProfiles": ["SAFE_LOCAL", "NETWORK_ISOLATED", "PROCESS_RESTRICTED", "LOCAL_FIXTURE"],
  "supportedFixtures": ["synthetic-credentials.v1", "loopback-http.v1"],
  "networkEnforcement": { "mode": "unknown|enforced|not-supported", "version": "..." },
  "processEnforcement": { "mode": "unknown|enforced|not-supported", "version": "..." },
  "snapshotRollback": true,
  "contaminated": false,
  "lifecycleState": "READY",
  "capabilityRecordSha256": "sha256:..."
}
```

`lifecycleState=READY` 只表示 runner 可接单，不证明任何 profile 已满足。

## 4. Attestation 要求

### 4.1 运行前 Attestation

必须由 Agent 现场生成，至少包含：

- runner、OS、架构、快照和 Agent build 身份；
- profile ID/version；
- 路由表、接口、默认路由和出口策略摘要；
- 防火墙/网络命名空间/虚拟交换配置摘要；
- DNS、代理、允许的 Controller/artifact/stub 目的地；
- 当前用户、权限/能力集、工作区和临时目录边界；
- 可用资源与本次预算；
- fixture 版本和生成 hash；
- nonce、生成时间、过期时间、job/capsule 绑定 hash；
- 清理策略和 revert 计划。

### 4.2 Attestation 成功条件

- 证据来自现场 probe，不是配置文件声明；
- 网络要求对应的每一条 deny/allow 都有结果；
- 默认路由存在但未证明出口阻断时，`NETWORK_ISOLATED` 不通过；
- 只要发现无法解释的代理、DNS 回落、宿主挂载、真实凭据目录或污染状态，就 fail closed；
- Attestation 过期、nonce 不匹配、runner/快照/hash 改变时自动失效。

### 4.3 运行后 Attestation

必须确认：

- capsule 工作区外无未声明文件变化；
- fixture、临时目录、子进程和网络连接已收束；
- runner 已回滚到基线，或明确报告回滚失败；
- 证据包已封存，之后不能被样本覆盖。

## 5. Execution Permit

Permit 必须绑定：

```text
permitId
  + taskId/caseId
  + sourceSha256/targetSha256
  + capsuleSha256
  + planSha256
  + profileId/profileVersion
  + runnerId/baselineSnapshot
  + attestationSha256/nonce
  + fixtureSetSha256
  + oracleSha256
  + resourceBudget
  + issuedAt/expiresAt
```

规则：

1. 只有 Planner `permitEligible=true` 且 Attestation 通过时才签发。
2. 只能使用一次；提交后状态为 `CONSUMED`，不因 HTTP 重试重复执行。
3. capsule、runner、profile、fixture、oracle 任一变动，Permit 失效。
4. Controller 旧的无 Permit 提交入口必须进入兼容模式且只允许 `STATIC_ONLY`/旧 build-only 范围；不得绕过新的安全 profile 执行高风险任务。
5. Permit 拒绝必须返回稳定 failure code 和补证据条件。

## 6. 推荐状态与失败码

| 状态/代码 | 含义 |
|---|---|
| `PLANNED` | 已生成安全计划，未做现场证明 |
| `ATTESTATION_PENDING` | 等待现场 probe |
| `ATTESTATION_FAILED` | 环境不满足 profile |
| `PERMIT_ISSUED` | 可一次性提交 |
| `PERMIT_REJECTED` | 策略或证据不足 |
| `SUBMITTED` | 已提交，不等于运行成功 |
| `EVIDENCE_INCOMPLETE` | 有 job 但证据不完整 |
| `BLOCKED_SAFETY` | 安全边界无法证明 |
| `BLOCKED_ENV` | 工具链/runner/fixture 环境故障 |
| `FAILED_CODE` | 有充分 build/runtime 证据指向代码 |
| `INCONCLUSIVE` | 证据冲突或 oracle 不足 |
| `CLEANUP_FAILED` | 清理/revert 未通过，禁止复用 runner |
