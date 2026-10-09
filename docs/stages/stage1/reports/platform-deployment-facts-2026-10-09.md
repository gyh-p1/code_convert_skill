# 平台当前部署事实核查（只读）

> 日期：2026-10-09
> 性质：只读核查部署回执、发布产物与历史验收证据；**未连接任何服务、未执行任何脚本、未部署**
> 来源：`E:\桌面文档\Code_Convert\.worktrees\evaluation-noise-v1\.codeconvert-state\noise-trial\`

## 1. 为什么需要本核查

此前文档把平台状态记为"三 runner `CONTRACT_MISMATCH`、动态验收 BLOCKED_ENV"。
本次在候选源码树内发现了**完整的部署回执、发布包、回滚脚本与四场景验收证据**。
这些材料改变了"平台尚未形成"的判断，必须先核实再更新文档。

## 2. 已部署回执（`deployed-receipt.json`）

| 字段 | 值 |
|---|---|
| product | `codeconvert-remote-stack` |
| role | `controller` |
| releaseVersion | **`1.0.25-noise.1`** |
| manifestHash | `sha256:026a8da844cc43ade9b925d9b34d1167e877b02033a1e784f522bb4aac25fbe9` |
| installRoot | `D:\CodeConvertRemote\Stack\Controller` |
| launchName | `CodeConvert-Remote-Controller` |
| installedAt | `2026-10-09T03:10:14.1055124+00:00` |
| Defender 排除 | `D:\CodeConvertRemote\Stack\Controller\jobs`（安装器配置，本次未新增） |

**发布产物存在**：`release/codeconvert-remote-stack-1.0.25-noise.1-windows-linux-macos-x64.zip`
（34,135,893 字节，2026-10-09 11:15）。

**回滚材料存在**：`rollback-controller.ps1`，带三重保护 ——
必须显式传 `-ConfirmNoActiveJobs`、校验当前安装确为本试用版、扫描活动 job 后才允许回滚。

## 3. 已记录的运行时健康（`health.json`）

| 字段 | 值 |
|---|---|
| service | `remote-host-controller` |
| version | `1.0.0`（**非**不可变发布版本） |
| contractSetHash | **`sha256:e088a356b48fd1c3f50e480ac24c2fd03319dc60a49b41de4d076219819c4c45`** |
| runnerMode | `agent` |
| ready | `true` |
| comparison.preset | `noise-tolerant-v1`（含 3 类文本噪声 + 5 类系统噪声模式，`tolerate_minor: true`） |

## 4. 已取得的四场景验收证据（`smoke-evidence/`）

`summary.json` 显示 **4/4 通过**，含 3 个负向对照：

| caseId | 预期 | 实际 | codeVerdict | 环境 | 通过 |
|---|---|---|---|---|---|
| `noise-allowed` | semantic_pass | semantic_pass | semantic_pass | clean | ✓ |
| `fixed-port-change` | mismatched | mismatched | failed | clean | ✓ |
| `required-file-missing` | mismatched | mismatched | failed | clean | ✓ |
| `explicit-noise-file-missing` | mismatched | mismatched | failed | clean | ✓ |

每个场景含 9 件证据：`capsule.zip`、`submission.json`、`receipt.json`、`state.json`、
`report.json`、`comparison.json`、`source.json`、`target.json`、`runners-after.json`。

`noise-allowed` 的 `report.json` 显示双侧均真实执行：

- source：`windows` / `windows-vm-agent-x64` / 快照 `CC-Eval-Windows-8Lang-R11`，
  `execution.performed=true`，preflight 与 cleanup 均 `PASSED`，`contaminated=false`，runner 回到 `READY`。
- target：`linux` / `linux-vm-agent-x64` / 快照 `CC-Eval-Linux-8Lang-R12`，同上。

`runners-after.json` 显示三 runner 当时**全部 `READY`、`contaminated=false`、`lastFailureType=null`**，
各自支持 7–8 种语言且 `supportsSnapshotRollback=true`。

## 5. 源码测试

`test-results.txt`：**190 passed**（`1.85s`）。

## 6. 与既有文档结论的冲突

| 既有文档结论 | 本次实测 | 处置 |
|---|---|---|
| 三 runner `CONTRACT_MISMATCH` | 该状态是**某次 GET 复核的时点值**；`runners-after.json` 显示 2026-10-09 03:16 时三 runner 均 READY | 两者不矛盾但**时点不同**，必须分别标注时点，不能并列成"当前状态" |
| 动态验收 BLOCKED_ENV、平台未形成 | 已有 1.0.25-noise.1 部署回执、发布包、回滚脚本与 4/4 验收证据 | 需改为"**曾完成一次成功部署与四场景验证**；当前服务状态需重新复核" |
| 目标目录不是完整系统 | 仍然成立（目标目录只有占位 README） | 保持 |

**关键区分**：`health.json` 里的 `contractSetHash = e088a356…` 是**该次部署所装版本的**契约哈希；
我在当前候选工作树上按 `contract_manifest.py` 的规则（`rglob("*.schema.json")`、按相对路径排序、
LF 归一化、NUL 分隔）独立重算得到 **`sha256:f4f58184ff971f0156054983dd23e5189425cc37310b059972d4dde7afaf3274`**（20 份 schema）。

`f4f58184…` 与 `e088a356…`、`56b32706…` **均不相同**，且仓库内检索不到 `f4f58184…`。
因此候选工作树当前检出的契约集合，**既不等于**历史试用版所记录的集合，**也不等于**曾观测到的现役 Controller 集合。
在未取得现役服务实时 `/api/health` 与 `/api/runners` 之前，**不能断言当前是否仍不匹配**。

## 7. 本核查未做与不能声称

- **未连接任何服务**，未调用 `/api/health` 或 `/api/runners`，未提交 job。
- **未执行**任何脚本、安装器、回滚脚本或测试；`190 passed` 是**读取已有日志**，不是本次运行。
- **未部署、未回滚、未修改**候选源码工作树（`git status` 干净）。
- 不能据本核查声称"当前平台可用"或"当前三 runner 已恢复"；那需要一次新的实时复核。

## 8. 对目标的意义

原目标中"形成并部署最新第三方评估平台"**已部分达成且留有证据**：
至少存在一次成功的 Controller 部署（1.0.25-noise.1）与四场景双侧验收（4/4，含 3 个负向对照）。

尚缺的是：

1. **现役服务实时状态复核**（T02-a）：当前是否仍是该发布、runner 是否可用。
2. **该试用版是否即"最新"**：候选工作树 HEAD `db2ccc0` 是"WIP 起点（可回退检查点）"，
   需确认是否有更新的、应部署的版本。
3. **剥离到目标目录**（T05-b/c）：目标目录仍只有占位 README。
