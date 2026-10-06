# Spec 01｜Safety Planner、风险原子化与 Evaluation Disposition

## 1. 目的

将当前人工使用的 `SAFE_CANDIDATE`、`UNSAFE_NET`、`REVIEW_SUBPROC`、`UNSAFE_LOCAL` 转为确定性的安全要求和评估路径。Planner 只做计划，不执行代码、不改变源码、不自动放宽边界。

## 2. 输入契约

```json
{
  "planVersion": "stage1.safety-plan.v1",
  "taskId": "string",
  "caseId": "string",
  "sourceSha256": "sha256:...",
  "targetSha256": "sha256:...",
  "sourceLanguage": "string",
  "targetLanguage": "string",
  "sourceOs": "string",
  "targetOs": "string",
  "sourceArch": "string|null",
  "targetArch": "string|null",
  "observedBehaviors": [
    {
      "id": "BHV-001",
      "kind": "network|filesystem|process|credential|persistence|injection|exploit|platform|other",
      "sourceEvidence": ["path:line-or-symbol"],
      "required": true,
      "notes": "string"
    }
  ],
  "oracle": {
    "mode": "none|output|event|trace|fixture",
    "obligations": ["OBL-001"],
    "allowedObservations": ["..."],
    "forbiddenObservations": ["real-credential", "public-egress"]
  }
}
```

`observedBehaviors` 必须来自源码/任务契约的静态审阅；ATT&CK 标签、文件名、模型自评和历史总 verdict 不能单独形成安全事实。

## 3. 原子安全要求

| 要求 ID | 含义 | 典型满足方式 |
|---|---|---|
| `NET_NO_PUBLIC_EGRESS` | 禁止公网/生产网出站 | 网络命名空间、出口防火墙、路由和 DNS 证据 |
| `NET_STUB_ONLY` | 只允许 loopback 或封闭实验网 stub | allowlist、stub identity、连接审计 |
| `NET_CONTROLLER_ONLY` | 只允许 Controller/artifact 必要流量 | 明确目的、端口、方向和时限 |
| `DATA_SYNTHETIC_ONLY` | 所有输入为合成数据 | fixture manifest、生成种子、内容扫描 |
| `PROC_TREE_RESTRICTED` | 子进程只能在受限树内运行 | root PID、argv 摘要、资源预算、kill/revert |
| `NO_PRIVILEGE_ESCALATION` | 不允许改变真实系统权限/服务/内核状态 | 运行身份、能力集、系统策略证明 |
| `LOCAL_SURFACE_TRANSACTIONAL` | 本机副作用必须落在一次性表面 | 临时目录/虚拟注册表/虚拟持久化表面 |
| `CONTROLLED_TARGET_ONLY` | 目标必须是专用无真实数据靶标 | fixture/target registry、版本 hash、回滚 |
| `NO_REAL_EXPLOIT_TARGET` | 不对真实软件/真实服务触发利用 | 受控 simulator 或 `STATIC_ONLY` |
| `CLEAN_REVERT_REQUIRED` | 运行后恢复干净状态 | snapshot/revert、artifact 清单、post-run probe |

Planner 输出的 requirement 是集合，不能用一个 `riskLevel=high` 替代具体边界。

## 4. 规划规则

1. 纯本地计算、一次性临时目录、无危险权限的任务 → `DIRECT_SAFE_RUN`。
2. 只需要 loopback/封闭 stub 的网络任务 → `ISOLATED_NET_RUN` + `NET_STUB_ONLY` + `NET_NO_PUBLIC_EGRESS`。
3. 只启动受控子进程的任务 → `RESTRICTED_PROCESS_RUN` + `PROC_TREE_RESTRICTED` + 资源预算。
4. 凭据、浏览器 profile、配置、持久化表面可替换为合成 fixture → `FIXTURE_EQUIVALENCE` + `DATA_SYNTHETIC_ONLY`。
5. 必须与专用靶标交互，但不接触真实服务/数据 → `CONTROLLED_TARGET_RUN` + `CONTROLLED_TARGET_ONLY`。
6. 无法将行为映射到安全观察面，或必须依赖真实危险目标 → `STATIC_ONLY` 或 `BLOCKED_UNMODELED`。
7. 同时命中多个 profile 时取满足全部要求的最小安全交集；找不到兼容 Runner/fixture 时阻断，不得自动降级到更弱 profile。
8. 任务中任何一条入口超出允许边界，planner 输出 `permitEligible=false`。

## 5. 输出契约

```json
{
  "planVersion": "stage1.safety-plan.v1",
  "taskId": "string",
  "planSha256": "sha256:...",
  "disposition": "DIRECT_SAFE_RUN|ISOLATED_NET_RUN|RESTRICTED_PROCESS_RUN|FIXTURE_EQUIVALENCE|CONTROLLED_TARGET_RUN|STATIC_ONLY|BLOCKED_UNMODELED",
  "requiredProfiles": ["NETWORK_ISOLATED"],
  "requiredCapabilities": ["NET_NO_PUBLIC_EGRESS", "NET_STUB_ONLY"],
  "fixtureRefs": [],
  "oracleRef": "oracle-v1",
  "permitEligible": false,
  "blockingReasons": [
    { "code": "ISOLATION_ATTESTATION_MISSING", "evidenceNeeded": "..." }
  ],
  "humanReview": false,
  "plannerTrace": [
    { "rule": "...", "inputEvidence": ["..."], "decision": "..." }
  ]
}
```

## 6. 不允许的决策

- 用 `READY`、`clean`、snapshot 存在替代 Attestation。
- 把下载改为“什么都不下载”后宣称网络行为通过。
- 把注入/利用路径删掉，只运行打印或初始化路径后宣称行为匹配。
- 以 synthetic fixture 的通过写成真实凭据读取、真实持久化或真实漏洞利用成功。
- 以缺少证据为由自动放行；缺证据只能保持 `permitEligible=false`。

## 7. 可重复性要求

相同的 task、源码/目标 hash、Skill/契约版本和 planner 版本必须得到相同的 `planSha256`。人工 override 必须记录操作者、理由、范围、过期时间和新增证据，不可修改原始 planner 输出。
