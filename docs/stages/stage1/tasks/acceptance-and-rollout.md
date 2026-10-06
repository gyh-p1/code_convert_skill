# Stage 1 验收、最小实验与灰度发布

## 1. 最小可证伪实验

### Experiment E1｜只读网络 Attestation

**目的：** 验证 Controller 能否区别“runner READY”与“网络 profile 已证明”。

**固定项：** runner、无害 probe、Controller contract、快照、输出协议不变。
**唯一变量：** 是否启用 `NETWORK_ISOLATED` 的现场 Attestation 和 Permit。

**步骤：**

1. 三台 runner 恢复基线快照。
2. 提交只读取路由、接口、代理、DNS 和防火墙状态的无害 probe；不向外部地址发包。
3. Controller 生成现场 Attestation，绑定 runner、profile、nonce 和 job。
4. 对一个不需要网络的安全样本和一个需要 stub 的样本分别请求 Permit。
5. 读取拒绝原因、证据 hash 和清理/revert 状态。

**成功信号：**

- `READY=true` 但缺隔离证明时，网络样本不能拿到 Permit；
- 已证明的 loopback/stub profile 可以得到 Permit；
- profile、runner、capsule 或 fixture hash 改变会使 Permit 失效；
- 证据中明确记录默认路由、允许目标、拒绝目标和清理状态。

**失败信号：**

- 只看 `READY` 或快照就放行；
- `networkMode` 只存在 metadata，不影响执行；
- Permit 可被复制或跨 capsule 使用；
- probe 结果缺失但 job 仍被报告为可安全执行。

### Experiment E2｜受限子进程

**目的：** 验证 `PROCESS_RESTRICTED` 的真实执行路径，而不是只增加标签。

**样本：** benign parent → child → grandchild，所有程序为一次性无害 fixture。

**成功信号：** 父子树、argv 摘要、退出码、资源和超时完整；无法收束时任务失败并锁定 runner，不形成 PASS。

### Experiment E3｜合成数据/本地表面

**目的：** 验证 `FIXTURE_EQUIVALENCE` 的输入、观察和清理闭环。

**样本：** 读取 synthetic profile、写入 transactional local surface、走成功/缺失/格式错误三条路径。

**成功信号：** 只访问 fixture 声明的路径；证据能匹配行为义务；无真实凭据；清理后状态恢复。

### Experiment E4｜不可建模样本的 fail-closed

**目的：** 验证没有安全 fixture 或必须依赖真实危险目标时不会被“为了凑覆盖”强行执行。

**成功信号：** Planner 生成 `BLOCKED_UNMODELED` 或 `STATIC_ONLY`，Permit 拒绝，报告包含解除条件；没有删除核心行为后的伪通过。

## 2. 分层验收标准

### Gate 1｜口径与数据

- 87 项主清单冻结；
- 每项有源码/目标 hash 和分类证据；
- 与 batch-02..06 现有 179 项数据的映射可解释；
- 旧结果未被重写。

### Gate 2｜Planner

- 规则版本化；
- 同输入重复规划稳定；
- 风险原子化；
- 无法建模的 case 默认阻断；
- planner trace 可复核。

### Gate 3｜平台安全门

- profile 真正进入 Controller/Agent 执行路径；
- Attestation 是现场证据、带有效期和 job 绑定；
- Permit 一次性、不可跨输入复用；
- 网络、进程、数据和清理条件缺一不可时 fail closed。

### Gate 4｜证据

- source/target build、execution、comparison、environment、safety 分层；
- `matched` 受 oracle 限制；
- 失败归因不混淆；
- 证据 hash、事件、job/run/permit 链完整。

### Gate 5｜灰度

- E1-E4 先完成；
- 至少 3–5 项通过真实平台闭环；
- 无安全越界、无未解释重复执行、无清理失败遗留；
- 才能扩大到 87 项。

### Gate 6｜阶段结束

- 87/87 有唯一 disposition；
- 可运行 disposition 中实际提交比例、证据完整率和行为 oracle 覆盖率分别统计；
- `BLOCKED_UNMODELED`、`BLOCKED_ENV`、`BLOCKED_SOURCE` 分开列出；
- 未达标项有责任方、恢复条件和是否进入下一阶段的决策。

## 3. 灰度顺序

```text
3–5 item canary
  -> SAFE_LOCAL
  -> NETWORK_ISOLATED
  -> PROCESS_RESTRICTED
  -> LOCAL_FIXTURE
  -> CONTROLLED_TARGET（如获批）
  -> remaining cases
```

每一层完成后冻结报告，再进入下一层；不因某一层成功而推断其他层能力。

## 4. 回滚

触发下列任一条件立即停止新提交：

- 发现公网/生产网出站或真实凭据读取；
- Attestation 与现场状态不一致；
- Permit 可绕过、复用或错误绑定；
- runner 未回滚或清理失败；
- evidence index 丢失或原始报告被覆盖；
- 受控 fixture 结果被报告为真实危险行为成功。

回滚动作：停止队列、撤销未消费 Permit、禁用新增 profile、恢复上一版 Agent/Controller snapshot、封存失败证据、重新跑无害 health/preflight probe。回滚本身也必须有事件和证据。

## 5. 交付清单

- [ ] 87 项 inventory 与差异台账
- [ ] 现役 Controller/Agent capability snapshot
- [ ] Planner schema/rules/trace
- [ ] Profile/capability/attestation/permit schema
- [ ] fixture registry 和 oracle contract
- [ ] 分层 evidence/report schema
- [ ] E1-E4 实验记录
- [ ] 3–5 项 canary report
- [ ] 87 项 disposition matrix
- [ ] compatibility/rollback rehearsal
- [ ] stage closure 与未达标项清单
