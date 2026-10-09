# 发布前变更清单（待用户确认）

> 日期：2026-10-09
> 性质：**待确认清单**。本文件只列出"要改什么"，不包含已实施的改动。
> 现状：尚未修改任何平台代码，尚未部署。
> 依据：[Spec02](controller-agent-improvements.md)、[平台优化完成度核查](../reports/platform-optimization-readiness-2026-10-09.md)、
> [现役平台实时核查](../reports/live-platform-verification-2026-10-09.md)、
> [CONTRACT_MISMATCH 根因定论](../reports/contract-mismatch-root-cause-2026-10-09.md)、总评估报告-2026-10-05

## 0-A. 前提更正（2026-10-09 用户裁定）

**原计划作废**。用户裁定：现役 Controller 报告的 `56b32706…` **可能是其他开发者部署的，
与本项目无关**，不需要继续溯源；也不采用"升级 Agent 去匹配现役 Controller"的路线。

**新路线**：确认全部优化完成 → **全部重新部署**（Controller + 三台 Agent 统一到同一发布）。
方案见[全面重新部署方案](full-redeployment-plan.md)。

因此本清单的 C5（Agent 升级）**改为整体重部署**；C1–C4 仍需用户取舍是否纳入本次发布。

## 0. 背景：为什么需要这次发布

现役 Controller 报告契约 `56b32706…`（该值在磁盘上不存在，疑为他人部署），
三台 Agent 为 `e088a356…`，导致**三 runner 全部 `QUARANTINED`**，平台当前不具备执行条件。
整体重部署将覆盖这一混合状态。

## 1. 变更总览

| 编号 | 变更 | 类型 | 是否阻塞升级 | 用户裁定 |
|---|---|---|---|---|
| **C1** | T02-c 契约故障定位 | Controller 代码 | **建议阻塞** | 待确认 |
| **C2** | T02-b 就绪诊断 | Controller 代码 | 不阻塞 | 待确认 |
| **C3** | T02-d 能力侧预检补全 | Controller + Agent 代码 | 不阻塞 | 待确认 |
| **C4** | 契约集合口径不一致修复 | evaluation-core 代码 | **需确认** | 待确认 |
| **C5** | **整体重新部署**（Controller + 三台 Agent 同一发布） | 发布/部署 | — | **已裁定** |
| **C6** | VM 网络隔离验证 | 环境配置 | 不阻塞本次部署 | 待确认 |
| **C7** | T02-e 目标侧独立诊断 | Controller + core | 明确不阻塞 | 建议排除 |
| **C8** | Winsock 补链（`-lws2_32`） | **Skill + 契约** | 不阻塞 | **新增·建议纳入** |
| **C9** | C# `.csproj` 中性工程生成 | Skill 规则 + Agent 代码 | 不阻塞 | **新增·待确认** |
| **C10** | Go 工具链版本策略（`GOTOOLCHAIN`） | **Skill**；缓存已修复 | 不阻塞 | **新增·待确认** |

> **C8–C10 为本次新增**，来自逐字挖掘总评估报告 §6 与六批 `events.jsonl`。
> **归属分析见[构建适配能否由 Skill 承担](../reports/build-adaptation-skill-scope-2026-10-09.md)**：
> - **C8 可由 Skill + 契约解决**（`buildCommand` 是 `agent-run-request` 契约字段，实测可执行）；
> - **C9 需 Skill 规则 + Agent 代码**（契约无"生成工程文件"字段）；
> - **C10 版本策略入 Skill，缓存项已修复**（R12 取证，不重复投入）。

---

## 2. C1｜T02-c 契约故障定位（建议纳入本次发布）

**问题**：现役 `/api/runners` 在 `CONTRACT_MISMATCH` 时**不报告 expected/actual 契约哈希**。
本次排查只能靠 SSH 旁路逐个取 Agent 契约，Windows Agent 至今取不到 —— 这正是 Spec02 §4 要消除的痛点。

**改哪里**：

| 文件 | 现状 | 拟改 |
|---|---|---|
| `apps/remote-controller/.../services/agent_client.py`（547 行） | 约 :43 比较哈希；:46 抛裸 `CONTRACT_MISMATCH` | 抛错时携带 `expectedContractSetHash`、`actualContractSetHash`（缺失为 null） |
| `apps/remote-controller/.../services/runner_registry.py`（101 行） | 只记 `lastFailureType`/`lastFailureReason` | 增 `checkPhase`、`checkedAt`、`reasonCode` |
| `apps/remote-controller/.../api/runners.py`（39 行） | 透传 registry 快照 | 输出新增诊断字段 |

**约束**：沿用现有拒绝/隔离逻辑，**不得跳过校验**；不把 Agent URL、token、完整配置写进公开错误；
若返回类型被严格 schema 消费，需同步契约，不能只改服务端。

**验收**：匹配/不同/缺失/格式非法/不可达分别给出正确原因；不匹配仍零执行；日志无凭据。

**为什么建议阻塞升级**：本次升级后若仍不匹配，没有 C1 就仍要重复今天的旁路排查。
且 C1 是 P0、无外部依赖、入口已核实存在。

---

## 3. C2｜T02-b 就绪诊断

**问题**：现役 `/api/health` 只有 6 个字段（`status/service/version/contractSetHash/runnerMode/ready`），
`ready=true` 在三 runner 全隔离时**仍为 true**，容易被误读为"可提交"。

**改哪里**：

| 文件 | 拟改 |
|---|---|
| `apps/remote-controller/.../app/main.py`（175 行，`health()` 在 :153） | 新增 `executionReady`、`readyRunnerCount`、`blockedRunnerCount`、`checkedAt`、`blockingReasons` |
| `.../services/runner_registry.py` | 提供聚合快照供 health 只读 |

**约束**：**保留 `ready` 原语义与 HTTP 存活响应**；health 内只读 registry 快照，
不轮询 VM、不回滚快照、不取执行锁；`BUSY` 与 `QUARANTINED` 分开。

**验收**：全隔离时 `ready` 可仍 true 而 `executionReady=false`；旧客户端仍能读现有字段。

---

## 4. C3｜T02-d 能力侧预检补全（部分实现 → 完整）

**现状**：`job_service.py` 约 :117–135 **已实现策略侧校验** ——
从 `functionalProfile.obligations[].requiredDimensions` 汇总必需维度，
校验其已被 `observationPolicy.dimensions` 请求、且非 output 维度已配置比较策略，否则抛具名错误。

**仍缺**：Spec02 §5 要求的**能力侧**语义 —— 某侧 Agent 实际支持哪些维度、
必需维度在哪一侧缺失，应在执行前以结构化结果报告。

**改哪里**：

| 文件 | 拟改 |
|---|---|
| `apps/vm-agent/vm_agent/app/observations.py` | `network`/`registry` 仍为固定 out-of-scope；需给出可解释的能力声明 |
| `apps/vm-agent/vm_agent/app/capabilities.py` | 能力清单与 obligation 对齐 |
| `apps/remote-controller/.../services/runner_resolver.py` | 解析 runner 能力时校验必需维度 |
| `apps/remote-controller/.../services/comparison_manifest.py` | 缺失必需维度时不标 matched |

**约束**：先核对现有 InputProfile/FunctionalProfile 能否表达 required obligation，
**不新造平行总 schema**；若需改契约，Controller/Agent 必须同版本一起升级。

**验收**：output-only 正常；必需 network/registry 不被标 matched；可选缺失有明确 limitation。

---

## 5. C4｜契约集合口径不一致（**需要你注意**）

**发现的真实不一致**：

| 位置 | 方法 | 计入的 schema 数 |
|---|---|---|
| `evaluation_core/contract_manifest.py:75` | `rglob("*.schema.json")` | **20**（含 `governance/`） |
| `evaluation_core/evaluation_contracts.py:66` | `glob("*.schema.json")` | **17**（不含 `governance/`） |

即：**契约哈希把 `governance/` 下 3 份 schema 算进去了，但 JSON Schema 校验注册表没有加载它们**。

**影响**：两份代码对"契约集合"的定义不同。若 `governance/` 下 schema 发生增删，
哈希会变、校验行为不变；反之亦然。这会让"契约不匹配"更难判断。

**需要你决定**：

- **选项 A**：统一为 `rglob`（校验也加载 governance）—— 覆盖更完整，但扩大校验面；
- **选项 B**：统一为 `glob`（哈希不計 governance）—— 变更最小，但 governance schema 不参与身份；
- **选项 C**：本次不动，仅记录为已知问题，留待后续专项。

**注意**：本项**尚未验证**是否会实际影响 `56b32706…` 与 `e088a356…` 的差异 ——
我没有两个已部署版本各自的实际 schema 集合，无法证明因果。**不声称它就是本次不匹配的原因。**

---

## 6. C5｜整体重新部署（已裁定）

**目标**：把 Controller 与三台 Agent **统一到同一发布**，覆盖当前混合/他人部署状态。

**不采用**"匹配 `56b32706…`" —— 用户裁定该值疑为他人部署，无需溯源。

**就绪度（已核查）**：

- 候选工作区干净，HEAD `db2ccc0`；
- `release-files.json` 的 **86/86 文件存在**；
- 离线依赖齐备：四组 wheelhouse（25/24/28/25 个文件）+ `python-runtime.zip`（12.9 MB）；
- 构建工具 `tools/release/build_remote_stack.py` 支持 `--release-version`；
- 已有 4/4 四场景验收与 190 项源码测试历史证据。

**执行顺序**（部署指南 §1 第 4 条）：Windows Agent → Linux Agent → macOS Agent → **Controller 最后切换**。

详见[全面重新部署方案](full-redeployment-plan.md)。

---

## 7. C6｜VM 网络隔离验证（安全硬门槛）

总评估报告记：三台 VM 均有默认外网路由，**隔离未验证**；含硬编码外部地址的任务一律未执行。
本轮亦未取得新的隔离证据。

**本项不阻塞重新部署**（部署本身不执行样本），但**阻塞 T04 真实样本执行**。

---

## 8. C7｜T02-e 目标侧独立诊断（建议本次排除）

P1、条件进入、影响状态机与生命周期。Spec02 §9.5 明确"不作为一个'小配置'立即部署"。
**建议不纳入本次发布**，待真实任务出现"源失败后需目标证据"时再排期。

---

## 8-A. C8–C10｜三项构建适配缺口（新增）

这三项来自逐字挖掘总评估报告 §6 与六批 `events.jsonl`，**此前未出现在任何清单中**。

共同点：`apps/vm-agent/vm_agent/app/main.py:199` 的 `build_command` **直接取自 manifest**，
Agent 侧没有任何按语言/平台适配构建命令的逻辑。

### C8｜Winsock 自动补链

| 项 | 内容 |
|---|---|
| 证据 | batch-01 `BUILD_COMMAND_CORRECTED`：`source uses Winsock; added -lws2_32 link library` |
| 报告 | §6#2："按源码特征自动补链" |
| 现状 | 候选源码检索 `ws2_32`/`winsock` **零命中** |
| 拟改 | Windows C/C++ 构建时按源特征（如 `#include <winsock2.h>`）自动追加 `-lws2_32` |
| 风险 | 需避免误加；建议仅在确有 Winsock 符号引用时追加 |

### C9｜C# `.csproj` 中性工程自动生成

| 项 | 内容 |
|---|---|
| 证据 | `AGENT_ADDED_CSPROJ` **17 次**（batch-01～04） |
| 报告 | §6#3："C# 源/目标缺 `.csproj` 会掩盖真实缺失类型 —— 补最小中性工程文件并留证" |
| 现状 | 候选源码检索 `csproj` **零命中** |
| 拟改 | Agent 检测到 C# 源缺工程文件时，生成**最小中性** `.csproj` 并留证 |
| 风险 | **"中性"必须可验证**：补齐工程文件会掩盖真实缺失类型，需同时记录"原本缺什么" |

### C10｜Go 工具链与缓存自动适配

| 项 | 内容 |
|---|---|
| 证据 | batch-03 D32/D35：`runner Go 1.26.4 vs model go.mod go1.27`；`toolchain download refused`<br>batch-01：`linux runner go build cache path unwritable` |
| 报告 | §6#1、§6#4 |
| 现状 | 检索 `GOCACHE`/`GOTOOLCHAIN`/`GOFLAGS` **零命中**；靠逐任务在 `input_profile.environment` 手工下发 |
| 拟改 | Agent 侧自动设置可写 `GOCACHE`；工具链版本不符时给出**结构化** `BLOCKED_ENV` 而非下载失败 |
| 风险 | 自动设 `GOTOOLCHAIN=local` 会改变语义；建议只做"可写缓存 + 明确报错"，版本策略交人工 |

**是否纳入本次发布由用户决定**。若不纳入，则仍维持"逐任务人工绕行"，
但应在部署文档中**显式记录**为已知限制，而非让下一位操作者重新发现。

---

---

## 9. 本次发布建议包含的最小集合

若以"整体重部署恢复三 runner 可用 + 不再重复排查困境"为目标：

```
必需：C5（整体重新部署）
建议：C1（T02-c）—— 否则下次契约问题仍无法从 API 定位
建议：C8/C9/C10（构建适配）—— 否则每次遇 C#/Go/Winsock 仍要人工改 job
可选：C2（T02-b）、C3（T02-d 能力侧补全）
待定：C4（契约口径不一致）—— 需你选统一为 rglob 还是 glob
排除：C7（T02-e）
环境：C6（隔离）独立于本次部署推进
```

**若只做 C5**：能恢复执行，但契约诊断能力与现役一致，且 C#/Go/Winsock 仍需逐任务人工绕行。
**若做 C1+C5+C8–C10**：恢复执行，且三类构建适配与契约诊断都不再依赖人工。

## 10. 尚未做的验证（诚实声明）

- 未执行构建，未产出新 ZIP；未计算任何新产物的 SHA-256。
- 未取得 Windows/macOS Agent 的 receipt 与版本。
- C4 的因果影响未证明（只证明了两处代码口径不同）。
- 未运行任何平台测试、未部署、未回滚、未提交 job。
- 未验证 `prepare_remote_stack_dependencies.py` 在当前环境可运行。
