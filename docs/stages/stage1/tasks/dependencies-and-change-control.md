# Stage 1 依赖与变更控制

## 1. 外部依赖

| 依赖 | 当前状态 | Stage 1 要求 |
|---|---|---|
| Remote Controller | 有现役连接/提交文档，具体能力以实时接口为准 | 支持 contract discovery、profile、Attestation、Permit 或明确缺口 |
| Windows/Linux/macOS VM Agent | 文档记录 READY、快照和语言能力 | 每台 runner 必须现场证明 profile 能力；READY 不足以放行 |
| 快照/回滚 | 已有能力记录 | 必须把 profile、fixture、Agent 版本纳入基线 identity |
| 工具链/SDK | 存在 Go 版本、源依赖、宿主隔离历史问题 | 环境失败与代码失败分开归因，失败后可安全重提 |
| Fixture registry | 当前未形成统一契约 | 先实现合成数据、loopback、benign process；危险靶标另行批准 |
| 证据存储 | 现有 job/report/evidence 路径 | 增加不可覆盖的 evidence index 和 hash 绑定 |

## 2. 本仓库变更边界

本阶段在本仓库允许：

- 新增规划、规格、任务、验收和差异台账文档；
- 更新根入口对 Stage 1 的链接和状态说明；
- 增加静态示例 schema 或字段映射，但不得声称外部 Controller 已消费；
- 对历史数据做只读汇总，不改写历史第三方报告。

本阶段在本仓库禁止：

- 引入本地执行器、编译器、VM 控制器或网络隔离脚本；
- 运行任何源/目标代码、构建脚本或未知样本；
- 以本地 JSON 校验代替第三方证据；
- 修改历史 job、report、comparison 或回填不存在的动态结果。

## 3. 版本策略

- `stage1.*.v1` 是规划中的新契约版本；平台实现必须先做版本协商。
- 新字段采用追加方式；旧字段保留并记录其语义限制。
- profile、fixture、oracle、Agent 和 Controller contract 任一变化都产生新版本和新 run。
- 旧版报告只读；新诊断使用 `supersedes` / `relatedRunId` 关联。

## 4. 变更批准

以下变化必须重新过 Gate S0-S3：

- 允许的网络目标、DNS、代理或 Controller/artifact 例外变化；
- 新增 fixture/controlled target；
- 放宽进程、文件、权限或资源边界；
- 改变 Permit 绑定字段、过期时间或兼容模式；
- 把 `STATIC_ONLY/BLOCKED_UNMODELED` 改成任何可运行 disposition；
- 把 fixture 等价范围扩大到真实目标、真实凭据或真实系统表面。
