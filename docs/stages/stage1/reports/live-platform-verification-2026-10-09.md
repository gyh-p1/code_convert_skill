# 现役平台实时核查（2026-10-09，经 SSH）

> 性质：**实时只读核查**。已连接 Controller 与其转发的 Linux Agent 只读接口；
> 未提交 job、未部署、未回滚、未修改任何远端状态、未执行任何样本。
> 本文件记录的是**当前**事实，取代此前文档中的时点不明表述。

## 1. 连接路径

| 项 | 值 |
|---|---|
| 跳板/Controller | `codeconvert-remote` = `192.168.101.250`（SSH 22，API 8443 均开放） |
| SSH 账户 | `dockeruser`（**非** `Administrator`；无服务查询权限） |
| Controller 主机名 | `DESKTOP-LRHSLVD` |
| VM 网段 `192.168.195.x` | **本机不可直达**；经 Controller 端口转发后可达 |

> 注意：部署指南第 2 节记 Controller 账户为 `Administrator@192.168.101.250`，
> 本次实际登录账户为 `dockeruser`。该差异已如实记录，未据此推断权限模型。

## 2. Controller 实时状态

`GET http://192.168.101.250:8443/api/health`：

```json
{
  "status": "ok",
  "service": "remote-host-controller",
  "version": "1.0.0",
  "contractSetHash": "sha256:56b327067f84fb8a62c4d6feca4dff56533a78883b3404882c9c5d903d6c45ed",
  "runnerMode": "agent",
  "ready": true
}
```

注意：**响应中没有 `comparison` 字段**。候选源码的 `health()` 会返回该字段，
说明现役服务运行的不是候选工作树的代码。

`install-receipt.json`（经 SSH 读取 `D:\CodeConvertRemote\Stack\Controller\install-receipt.json`）：

| 字段 | 值 |
|---|---|
| releaseVersion | **`1.0.25-noise.1`** |
| manifestHash | `sha256:026a8da844cc43ade9b925d9b34d1167e877b02033a1e784f522bb4aac25fbe9` |
| installRoot | `D:\CodeConvertRemote\Stack\Controller` |
| launchName | `CodeConvert-Remote-Controller` |
| installedAt | `2026-10-09T03:10:14.1055124+00:00` |
| Defender 排除 | `…\Controller\jobs`，`addedByInstaller=true` |

**与 `.codeconvert-state/noise-trial/deployed-receipt.json` 完全一致**，且 `releaseVersion` 与
`installedAt` 吻合，说明该部署**至今仍在服役**，未被回滚或覆盖。

## 3. Runner 实时状态（`GET /api/runners`）

| runner | lifecycleState | ready | contaminated | lastFailureType |
|---|---|---|---|---|
| linux-vm-agent-x64 | `QUARANTINED` | false | true | `CONTRACT_MISMATCH` |
| windows-vm-agent-x64 | `QUARANTINED` | false | true | `CONTRACT_MISMATCH` |
| macos-vm-agent-x64 | `QUARANTINED` | false | true | `CONTRACT_MISMATCH` |

三者 `lastFailureReason` 均为 `Agent contract set does not match Controller contract set`。
三者 `supportedLanguages` 均为 python/powershell/c/cpp/go/dotnet/ruby，`supportsSnapshotRollback=true`。
快照基线分别为 `CC-Eval-Linux-8Lang-R12`、`CC-Eval-Windows-8Lang-R11`、`CC-Eval-Mac-7Lang-R2`。

**该阻断在本次核查时点仍然存在** —— 这与 03:16 的历史 READY 快照不矛盾：那时服务刚装好且契约一致，
之后 Agent 侧的契约集合发生了变化。

## 4. Agent 可达性与契约（决定性证据）

### 4.1 三台 VM 均在运行

Controller 上有 **3 个 `vmware-vmx` 进程**；`arp -a` 显示三台 guest 均有动态条目：

| guest IP | MAC |
|---|---|
| `192.168.195.128` | `00-0c-29-cc-6f-05` |
| `192.168.195.129` | `00-0c-29-78-8a-27` |
| `192.168.195.130` | `00-0c-29-12-36-26` |

`.128` 与 `.129` 均**响应 ICMP**。

> **方法学更正**：本轮最初用 `Test-NetConnection`/PS `Test-Connection` 判断可达性，
> 得到"Windows Agent 不可达"的结论，随后被证伪 —— 同一命令在重试中返回
> `connect=True`，而 `cmd ping` 与 `.NET TcpClient` 也均成功。
> 该工具的间歇性误报不应作为停机依据。**结论以多次交叉验证为准**。

### 4.2 Agent `/health` 实测

经 Controller 转发（`-L 29000:192.168.195.129:9000`）与 Controller 内部 `curl`：

| 目标 | `/health` 结果 |
|---|---|
| Linux Agent `192.168.195.129:9000` | **正常返回 JSON** |
| Windows Agent `192.168.195.128:9000` | TCP 端口可连接，但 **HTTP 无响应体（空）** |

Linux Agent `/health`：

```json
{
  "status": "ok",
  "version": "1.0.0",
  "contractSetHash": "sha256:e088a356b48fd1c3f50e480ac24c2fd03319dc60a49b41de4d076219819c4c45",
  "os": "linux", "arch": "x64",
  "languages": ["python","powershell","c","cpp","go","dotnet","ruby"],
  "supportedEvidenceDimensions": ["output","filesystem","processes"]
}
```

Windows Agent 的 HTTP 无响应与 Controller 报出的 `CONTRACT_MISMATCH` 是其被隔离的原因之一，
但**其契约哈希本轮未取得**（SSH 22 开放但本机密钥未获授权：`Permission denied (publickey,password)`），
故不声称其三台差异完全相同。

### 4.3 端口与进程事实

- Controller `8443`：`0.0.0.0:8443 LISTENING`，PID `3968`。
- Controller 到 Linux Agent：`192.168.195.1:57583 -> 192.168.195.129:9000 TIME_WAIT`（说明确有连接活动）。
- 本机无法直达 `192.168.195.x`，必须经 Controller 转发。

## 5. 根因（已确证）

**契约哈希对照：**

| 主体 | contractSetHash | 来源 |
|---|---|---|
| **现役 Controller** | `sha256:56b327067f84fb8a62c4d6feca4dff56533a78883b3404882c9c5d903d6c45ed` | 实时 `/api/health` |
| **现役 Linux Agent** | `sha256:e088a356b48fd1c3f50e480ac24c2fd03319dc60a49b41de4d076219819c4c45` | 实时 Agent `/health` |
| 候选工作树（当前检出） | `sha256:f4f58184ff971f0156054983dd23e5189425cc37310b059972d4dde7afaf3274` | 本轮按 `contract_manifest.py` 重算（20 schema） |

**Controller 与 Agent 的契约集合不同**，这正是 runner 被隔离的直接原因。
`e088a356…` 同时也是历史试用版 `health.json` 记录的哈希。

修复方向（不在此文件实施）：使三方契约集合一致。可行路径：

1. 将 Agent 升级/回退到与 Controller `56b32706…` 一致的发布；
2. 或将 Controller 部署到与 Agent `e088a356…` 一致的发布。

**候选工作树的 `f4f58184…` 与两者都不同**，因此**不能直接把当前工作树打包部署**去"修"这个不匹配 ——
那会引入第三种契约集合。必须先确认目标发布版本（这需要用户决策）。

## 6. 其他实时事实

- Windows Agent（`192.168.195.128`）：VM 在运行、ICMP 通、22 与 9000 端口可连接，
  但 **9000 的 HTTP `/health` 无响应体**；SSH 22 开放但本机密钥未获授权
  （`Permission denied (publickey,password,keyboard-interactive)`），故未取得其契约哈希与 receipt。
- macOS Agent（`192.168.195.130`）：VM 在运行（ARP 有条目），本轮**未探测**其 9000 端口。
- Controller 上的 3 个 `vmware-vmx` 进程与三台 guest 的 ARP 条目相互印证。

## 7. 本次核查未做与不能声称

- **未提交任何 job**，未调用 `/api/jobs` 等写接口；只读 `/api/health` 与 `/api/runners`。
- **未部署、未回滚、未重启**任何服务；未修改远端任何文件。
- **未执行任何样本、capsule、构建脚本或测试**。
- 未取得 Windows/macOS Agent 的契约哈希，不能声称三者差异完全相同。
- 不能声称"平台当前可用"：三 runner 均 `QUARANTINED`，**当前不具备执行条件**。
- 不能声称部署指南中的 `Administrator` 权限模型仍然成立 —— 本次登录的是 `dockeruser`，
  且该账户**无服务查询权限**（`Get-Service` 返回权限不足）。

## 8. 对任务台账的影响

| 任务 | 变化 |
|---|---|
| T02-a 部署身份/契约恢复 | 由"待输入"变为**已取得实时身份**：Controller `1.0.25-noise.1` / `56b32706…`；Linux Agent `e088a356…`。**根因已确证**，待用户决策修复路线（升级 Agent 还是回退 Controller） |
| T03-c 隔离及数据核对 | 仍缺隔离证据；本次未做隔离探针 |
| T04-a | 当前 runner 全部隔离，**不能执行** |

## 9. 未决问题（需用户决策）

1. **目标发布版本是哪一版？** 候选工作树 `f4f58184…`、Controller `56b32706…`、
   Agent `e088a356…` 三者互不相同。直接部署当前工作树会产生第三种契约集合。
2. **Windows Agent 的 `/health` 为何无响应体？** 需在其 VM 内查看服务状态与日志
   （需该 VM 的 SSH 授权或 Controller 管理通道）。
3. **是否先做契约对齐**，还是直接把三方一起升级到某个统一发布？

---

> **2026-10-10 追加批注（不改写以上原始记录）**：以上记录的提交端机位（`192.168.101.101`，与 Controller 同 `192.168.101.0/24` 段、经 SSH/直连）是 2026-10-09 核查时点的事实。此后转换流程迁至远端宿主，提交端（转换 Agent 工作区）与 Controller 同处一机，现改走回环 `http://127.0.0.1:8443`；样本执行与网络隔离仍只在 VM Agent 内，宿主本身可连公网、同机不构成隔离证明。现役连接坐标与同机边界以[Controller 适配](../../../../references/adapter/controller/remote-controller-adapter.md)和[安全边界](../../../../references/framework/safety-boundary.md)为准。本节仅追加说明，上方原始核查结论保持不动。
