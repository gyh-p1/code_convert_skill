# 平台问题全量清单（对照 总评估报告-2026-10-05）

> 日期：2026-10-09
> 性质：**全量问题清点**。来源为逐字挖掘 `总评估报告-2026-10-05.md` §4/§6/§8
> 与六批 `events.jsonl` 的机器可读事件；并对候选源码与现役平台逐项核对现状。
> 未部署、未修改、未提交 job。
> 结论：**此前只覆盖了其中一部分**。本清单补齐后共 **13 项平台问题**，其中 **5 项属于"每次任务都要人工绕"的自动化缺口**。

## 1. 为什么需要这份清单

用户提问："这些确认是目标发现的全部问题了吗？尤其是总评估报告。"

此前的变更清单（C1–C7）主要来自 Spec02，**没有系统挖掘总评估报告与批次事件**。
本次逐条提取后，发现 **5 项此前未记录的平台功能缺口**。

## 2. 问题总表

| # | 问题 | 来源 | 现状 | 类别 |
|---|---|---|---|---|
| P1 | Linux runner Go 构建缓存路径不可写 | batch-01 `ENV_WORKAROUND_RETRY` + §6#1 | **已修复并有取证**（R12 快照 + 无害作业不使用 `GOCACHE` 前缀即通过） | 已修复 |
| P2 | Windows C/C++ 用 Winsock 需手工加 `-lws2_32` | batch-01 `BUILD_COMMAND_CORRECTED` + §6#2 | **可由 Skill + 契约解决**（`buildCommand` 是契约字段） | **Skill 侧** |
| P3 | C# 缺 `.csproj` 会掩盖真实缺失类型 | 17× `AGENT_ADDED_CSPROJ` + §6#3 | **需 Skill 规则 + Agent 代码** | **两者兼需** |
| P4 | runner Go 1.26.4 与源码 `go 1.27` 不符 | batch-03 两条 `ENVIRONMENT_FINDING_RECORDED` + §6#4 | 版本策略可入 Skill；结构化报错属平台 | **Skill + 平台** |
| P5 | Go 源构建间歇 `command timed out` | batch-04 `ENVIRONMENT_FINDING_RECORDED`（E09/E16/E25/E27）+ §6#5 | 未修复 | 环境 |
| P6 | 宿主隔离导致约 12 份样本不可读 | batch-05 `ENVIRONMENT_FINDING_RECORDED`（F21/F22/F23）+ §6#6 | 未解决 | 环境 |
| P7 | **三台 VM 均有默认外网路由，隔离未验证** | batch-02 `ISOLATION_PROBE_COMPLETED status=NOT_VERIFIED` + §6#7 | **仍未验证** | **安全硬门槛** |
| P8 | 大文件 JSON 内嵌源码不可靠 | §6#8 | 已改 `<<<FILE: …>>>` 分块协议 | 已缓解 |
| P9 | 杀软隔离策略需明确 | §8 建议 | 已有精确 Defender 排除（Controller jobs / Agent workspaces） | 已缓解 |
| P10 | T02-b 就绪诊断未实现 | 现役 API 实测 | 未实现 | 功能缺口 |
| P11 | T02-c 契约故障定位未实现 | 现役 API 实测 | 未实现 | 功能缺口 |
| P12 | T02-d 观察义务预检仅部分实现 | 候选源码核对 | 部分实现 | 功能缺口 |
| P13 | 契约集合口径不一致（`rglob` vs `glob`） | 候选源码核对 | 未统一 | 功能缺口 |

## 3. 三项构建适配缺口的归属（2026-10-09 补充分析）

用户提问"C8–C10 能否通过优化 Skill 完成"。分析结论见
[构建适配能否由 Skill 承担](build-adaptation-skill-scope-2026-10-09.md)：

| 项 | 归属 | 关键依据 |
|---|---|---|
| **P2/C8** Winsock 补链 | **Skill + 契约即可** | `buildCommand` 是 `agent-run-request` 契约字段，提交方可提供 |
| **P3/C9** `.csproj` 生成 | **Skill 规则 + Agent 代码** | 契约无"生成工程文件"字段，需代码实现 |
| **P4/C10** Go 工具链 | **Skill 定策略 + 平台做报错** | `GOCACHE` 属运行环境，非命令可表达 |

**重要**：`posix-winsock/SKILL.md` 第 43 行**已经写明**"链接 `ws2_32.lib`" ——
知识本来就在，缺的是**把它落到冻结契约的构建命令**这一步。

### 3.1 三个原"人工绕行"缺口的实际性质

| 原判定 | 修正后 |
|---|---|
| P2 平台无自动处理 | **流程缺口**：应由契约携带，而非事后人工补 |
| P3 平台无自动生成 | **能力缺口**：确需 Agent 代码 |
| P4 靠手工下发 | **策略缺口**：Skill 该规定基线不符时如何处理 |

**P1 已更正为"已修复"**（见 §2 表），依据 `runner-capability-matrix.md` §1.2：
提交 `8d4da68` 把 `HOME`/`XDG_CACHE_HOME`/`GOCACHE` 指向可写目录，
R12 快照生效，无害作业 `eval-20261005-115047-f2cdbaec` **不使用 `GOCACHE` 前缀**即通过。


### P2 Winsock 链接

```json
{"event":"BUILD_COMMAND_CORRECTED","taskId":"B07",
 "reason":"source uses Winsock; added -lws2_32 link library"}
```

核对：候选源码全文检索 `ws2_32`，**零命中**。
即：Windows 上任何使用 Winsock 的 C/C++ 源，构建命令都需要人工补链接库。

### P3 `.csproj` 脚手架

事件计数：`AGENT_ADDED_CSPROJ` **17 次**（分布于 batch-01～04）。

报告 §6#3 原文："C# 源/目标缺 `.csproj` 会掩盖真实缺失类型 —— 补最小中性工程文件并留证。"

核对：候选源码全文检索 `csproj`，**零命中**。
即：C# 方向的工程文件仍需**每次由人补**，且"补什么"依赖个人判断。
这既影响可重复性，也可能掩盖真实缺失类型。

### P4 Go 工具链版本

```json
{"taskId":"D32","finding":"runner Go 1.26.4 vs model go.mod go1.27;
 also confirmed input_profile.environment can set env vars"}
{"taskId":"D35","finding":"Go target go.mod requires 1.27 but runner has 1.26.4;
 toolchain download refused"}
```

报告 §6#4 的处理是**经 `input_profile.environment` 下发 `GOTOOLCHAIN=local`**，
即逐任务手工注入环境变量。

核对：候选源码全文检索 `GOCACHE`/`GOTOOLCHAIN`/`GOFLAGS`，**零命中**。

**这三项（P2/P3/P4）此前未出现在任何变更清单中**，是本次挖掘的新发现。

## 4. 隔离仍未验证（P7，安全硬门槛）

机器可读证据：

```json
{"event":"ISOLATION_PROBE_COMPLETED","batchId":"batch-02",
 "status":"NOT_VERIFIED","finding":"default route on all three runners"}
```

报告 §6#7："三台 VM 均有默认外网路由，隔离未验证 —— 含硬编码外部地址的项一律未执行。"
§8 建议："完成 VM 网络隔离并用无害探针验证。"

**本轮未取得任何新的隔离证据**，该状态应视为**仍然成立**。

对分类器结果的影响：本次六批中 **26 条**因 `public_network_unverified` 阻断，正是这一项的直接后果。

## 5. 与既有变更清单的关系

[发布前变更清单](../specs/release-change-list.md) 的 C1–C7 只覆盖了 P10/P11/P12/P13/P7 与部署本身。
本清单补齐 P1–P6、P8、P9，其中 **P2/P3/P4 是全新项**。

## 6. 逐项现状核对方法（可复核）

| 项 | 核对方式 | 结果 |
|---|---|---|
| P2/P3/P4 | 候选源码全文检索关键词 | 均零命中 |
| P7 | 六批 `events.jsonl` 的 `ISOLATION_PROBE_COMPLETED` | `NOT_VERIFIED` |
| P10/P11 | 现役 `/api/health`、`/api/runners` 字段 | 无 Spec02 拟议字段 |
| P13 | 比对 `contract_manifest.py:75` 与 `evaluation_contracts.py:66` | `rglob`(20) vs `glob`(17) |
| 事件计数 | 六批 `events.jsonl` 解析 `event` 字段 | 见 §2 |

## 7. 本次核查未做

- **未验证 P1 是否已被 R12 修复**（需登录 Linux VM 查 `GOCACHE` 与路径权限；
  嵌套 SSH 超时，未取得结果）。
- **未验证 P5 Go 超时是否仍复现**（需实际构建，属执行面）。
- **未验证 P6 宿主隔离当前状态**。
- 未部署、未重启、未修改任何文件、未提交 job。
- 未取得 Windows/macOS Agent 的实时健康（Windows Agent `/health` 本轮两次探测均失败，
  而 Linux Agent 稳定返回 200 —— 该不稳定本身值得记录）。
