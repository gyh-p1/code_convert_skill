# 全面重新部署方案

> 日期：2026-10-09
> 依据：用户裁定（2026-10-09）—— `56b32706…` 可能是其他开发者部署的，与本项目无关；
> **只需确认全部优化完成后，全部重新部署**。
> 性质：部署前方案与就绪度核查（历史）；用户已授权并完成 1.0.26 四角色部署、最终快照更新与 health-only 验收，见[执行记录](../reports/1.0.26部署与快照更新记录-2026-10-09.md)。以下待决策和未验证项保留部署前时点，不作为当前部署状态。

## 1. 裁定要点

用户明确：

1. 现役 Controller 报告的 `56b32706…` **不需要继续溯源**（可能是其他开发者所部署）；
2. 不采用"升级 Agent 去匹配现役 Controller"的路线；
3. 正确路线是：**确认优化全部完成 → 全部重新部署**（Controller + 三台 Agent 统一到同一发布）。

因此此前[根因定论](../reports/contract-mismatch-root-cause-2026-10-09.md)中"回执版≠运行版"的记录
**保留为事实证据**，但**不再作为阻塞项** —— 因为整机将被重新部署覆盖。

## 2. 重新部署就绪度核查（只读）

### 2.1 源码与发布清单

| 项 | 状态 |
|---|---|
| 候选工作树 | `E:\桌面文档\Code_Convert\.worktrees\evaluation-noise-v1`，HEAD `db2ccc0` |
| 工作区是否干净 | **是**（`git status --short` 无输出） |
| `release-files.json` 引用的文件 | **86 / 86 全部存在**（0 缺失） |

### 2.2 离线依赖（**关键**：决定能否离线重建）

位于 Controller `D:\CodeConvertRemote\DeployInput\noise-trial-20261009\release-deps\`：

| wheelhouse | 文件数 |
|---|---:|
| `windows-x64\agent` | 25 |
| `windows-x64\controller` | 24 |
| `linux-x64\agent` | 28 |
| `macos-x64\agent` | 25 |
| `windows-x64\python-runtime.zip` | 12,910,537 字节 |

**四组 wheelhouse + Windows Python runtime 均齐备**，满足 `release-files.json` 的
`dependencies` 声明（`windowsRuntime` + 四个 `wheelhouses`）。

### 2.3 构建与验证工具

| 工具 | 路径 | 作用 |
|---|---|---|
| 构建 | `tools/release/build_remote_stack.py` | 支持 `--verify`、`--repo-root`、`--release-version` |
| 依赖准备 | `tools/release/prepare_remote_stack_dependencies.py` | 从源码缓存/离线目录组装 wheelhouse 与 runtime |
| 契约优化 | `tools/contracts/optimize_evaluation_contracts.py` | 契约优化工具链 |
| 安装 | `bundle\...\install-controller.ps1`、`install-agent-{windows,linux,macos}` | 四角色安装器 |
| 验证 | `bundle\...\verify-stack.ps1`、`smoke-*` | 分层验收 |

### 2.4 既有可复用证据

| 材料 | 结论 |
|---|---|
| 四场景验收（`smoke-evidence/`） | **4/4 通过**，含 3 个负向对照，环境均 clean |
| 源码测试（`test-results.txt`） | **190 passed** |
| 回滚材料 | `rollback-controller.ps1`（带活动 job 扫描与版本校验） |

## 3. 重新部署前仍须完成的事项

按[平台优化完成度核查](../reports/platform-optimization-readiness-2026-10-09.md)，
以下属于"优化"范畴且**尚未完成**——用户要求"确认全部优化完成"后才部署：

| 项 | 状态 | 是否阻塞部署 |
|---|---|---|
| T02-b 就绪诊断 | 未实现（现役 health 6 字段） | 待用户确认 |
| T02-c 契约故障定位 | 未实现（本次排查困难的直接原因） | 待用户确认 |
| T02-d 观察义务预检 | **部分实现**（策略侧已有，能力侧缺） | 待用户确认 |
| T02-e 目标侧独立诊断 | 未实现（P1，条件进入） | 建议排除 |
| VM 网络隔离验证 | 未完成 | 不阻塞部署，**阻塞真实样本执行** |

用户此前表示"确认全部优化完成后一起发布"，因此**需要用户就上述各项给出取舍**。

## 4. 建议的部署流程

沿用部署指南分层顺序，**前一层失败即停止**：

1. **冻结业务状态**：确认无 active job / run；两 Runner 无污染；退出图形会话。
2. **构建发布**：以目标 `--release-version` 运行构建工具，产出三系统同一 ZIP，
   记录 ZIP SHA-256、`manifestHash`、`contractSetHash`。
3. **包内校验**：ZIP SHA → manifest → 逐文件 hash → contract hash。
4. **逐机 dry-run**：审查 `cleanup-plan.json`；`mutationsPlanned=false`。
5. **按序安装**：Windows Agent → Linux Agent → macOS Agent → **Controller 最后切换**。
6. **跨机 health-only**：四角色 receipt / health / contract 一致。
7. **Runner 前置检查**：三 Runner `READY`、`ready=true`、`contaminated=false`。
8. **固定无害验收**：用**发布包内** generator 生成 capsule，经 Controller 提交；
   复核 `codeVerdict`、`behaviorVerdict`、`environmentStatus=clean`。
9. **清理后检查**：两侧 cleanup `PASSED`，Runner 回到干净 `READY`，workspace=0。
10. **快照基线**：VM 干净关机后创建并恢复验证新 baseline。

**关键约束**（部署指南 §1）：
- 三台机器必须部署**同一个原始 ZIP 字节**，不能分别从工作树重打包；
- Controller 最后切换；
- `releaseVersion`、`/health.version`、`manifestHash`、`contractSetHash` 是四个不同概念；
- 真实远端失败后必须**递增** `releaseVersion`，不得修补后覆盖重打。

## 5. 本机安全边界（不因远程访问而改变）

- 本机**不执行**任何样本、构建脚本或转换产物；
- 允许：SSH 只读核查、读取回执/健康/证据文件；
- 部署动作需在获授权窗口内、按上述流程执行；**本文件不授权执行部署**。

## 6. 待用户决策

1. **优化取舍**：T02-b / T02-c / T02-d(补全) 是否纳入本次发布？（T02-e 建议排除）
2. **目标版本号**：本次发布的 `releaseVersion` 取值（须递增，不可复用失败版本）。
3. **执行窗口**：确认无 active job 的时间窗。
4. **权限**：当前 SSH 账户为 `dockeruser`，**无服务查询/安装权限**；
   部署需要管理员账户（部署指南记 `Administrator`）。

## 7. 尚未验证

- 未实际执行构建，未产出新 ZIP；
- 未计算候选构建产物的 SHA-256；
- 未验证 `prepare_remote_stack_dependencies.py` 在当前环境可运行（需 Python 与离线源）；
- 未取得 Windows/macOS Agent 的 receipt 与版本；
- 未做隔离探针。
