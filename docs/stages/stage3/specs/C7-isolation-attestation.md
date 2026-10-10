# C7：网络隔离 Attestation / Permit

> 类型：能力扩充（**安全相关**） ｜ 优先级：**P1** ｜ 解封用例：硬编码外联类
> 依据：dataset-2 D2-083、D2-108

## 1. 问题：安全边界要求"阻断并**验证**"，但平台不提供验证凭据

安全边界原文要求：

> 禁止连接真实外部目标、外部 C2、公网或生产网服务。
> **runner 的 `READY`、`clean` 和快照回滚状态不证明网络已隔离**；
> 对**硬编码外部地址**的样本，**先在 VM/网络层阻断或重定向到封闭实验网并验证**，
> 不能只改说明文本后运行。

现实：
- 平台**确实**在封闭实验网内运行，但**不提供机器可读的隔离凭据**；
- 调用方因此**无法证明**"该地址已被阻断"，只能凭 `READY`/`clean`；
- 而安全边界**明确否定**了 `READY`/`clean` 作为隔离证明。

⇒ **死锁**：安全边界要求证明，平台不签发证明，调用方只能阻断该项。

## 2. 受影响的实测用例

| 项 | 行为 | 当前处置 |
|---|---|---|
| D2-108 | 硬编码 `10.9.1.6:4444`，`WSAConnect` 连出后把 `cmd.exe` 标准流绑到 socket | `WAITING / RUN_SAFETY_NOT_READY` |
| D2-083 | WinRM 远程执行客户端，目标来自 argv | `WAITING / public_network_unverified` |
| D2-055 | （分类器假阳性，非真实外联） | 见 C5 |

## 3. 建议实现：签发**可验证的隔离声明**

### 3.1 Attestation（网络隔离声明）

在 job 报告中增加一个机器可读、**可被独立核对**的块，例如：

```json
"isolation": {
  "networkMode": "closed-lab",
  "egressPolicy": "deny-all-except-loopback",
  "blockedRanges": ["0.0.0.0/0"],
  "allowedRanges": ["127.0.0.0/8", "::1/128"],
  "verifiedBy": "iptables-save | sha256:...",
  "verifiedAt": "2026-10-10T08:29:02Z",
  "verificationMethod": "post-run ruleset hash captured from inside the VM"
}
```

**关键**：`verifiedBy` 必须是**运行时可核对的实证**（防火墙规则哈希、路由表快照），
而不是一个布尔标志或人工填写的字段。否则等于把"只改说明文本"合法化。

### 3.2 Permit（逐例放行）

对硬编码外部地址的样本，允许在**满足隔离声明**的前提下放行，并记录：

- 被访问的目标地址（由 C2 采集，或由静态画像登记）；
- 该地址**实际是否可达**（运行时应观察到 connect 失败或重定向成功）；
- 放行依据与隔离声明的关联。

### 3.3 重要边界

1. **不得**因为有了 Attestation 就默认放行**所有**外联样本；
2. Attestation 只证明"**该环境**阻断了非允许流量"，**不证明**样本本身安全；
3. **不得**用 Attestation 替代"不新增攻击能力"的判定（那是转换侧责任）；
4. 声明若与**实际观察**矛盾（如声称 deny-all 却观察到 connect 成功），应以**实际观察为准**并告警。

## 4. 验收判据

1. 提交 D2-108 的 capsule，在具备隔离声明的环境 ⇒ 应能执行并回传**两侧行为证据**；
2. 回传中应包含 `isolation` 块且 `verifiedBy` 指向**运行时可核对的实证**；
3. **负例**：若隔离声明缺失或不可核对 ⇒ 仍应拒绝执行（**不得**因有字段就放行）；
4. **一致性检查**：声明 `deny-all-except-loopback` 时，若观察到对外 connect 成功 ⇒ 应报**一致性告警**。

## 5. 我方现状

D2-108、D2-083 保持 `WAITING`，**不消耗模型调用**，不降级分类结论。

## 6. 同机共处对本声明的影响（2026-10-10 追加，不改写以上）

转换流程迁至远端宿主后，转换 Agent 工作区与 Controller 同处一台**可连公网**的宿主；样本执行仍在 VM Agent 内。本节澄清对本声明的影响——**不是**“两侧物理分离前提塌了”：本声明的“两侧”指源/目标侧 VM 执行，其隔离讲的是 **VM 的出网策略**，并不建立在“转换 Agent 与 Controller 分处两机”的假设上，故 Agent 与 Controller 同机**不使本声明的前提失效**。真正受影响的是下面两点：

- `allowedRanges: 127.0.0.0/8` / loopback 的语义收紧。VM 若与一台**和 Agent、公网共享的宿主**共处，loopback / 宿主可达范围不再是“隔离”的安全代名词：`verifiedBy` 的运行时实证须覆盖“VM→宿主、宿主→公网”方向，不能只证明 VM 内部 egress。
- 共处宿主本身不提供隔离。`networkMode: "closed-lab"` 的声明须明确它约束的是 VM 层；宿主的公网可达性不被该声明覆盖，须单独核对或在网络层阻断 VM→宿主→公网路径。

本声明仍是平台侧规格，由平台实现与签发；本项目只记录前提变更，不自行改判。相关红线见[安全边界](../../../../references/framework/safety-boundary.md) §1、§3 与 [AGENTS.md](../../../../AGENTS.md) §11。
D2-108 的完整安全判定（含"为何不能靠改输入约束"）见：
`docs/test/dataset-2/cpp-to-ruby/D2-108-cpp-shell.cpp/output/batch/01-frozen/frozen-inputs.md`
