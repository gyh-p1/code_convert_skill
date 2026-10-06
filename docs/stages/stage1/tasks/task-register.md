# Stage 1 任务台账

> 任务状态均为 `PLANNED`，不表示外部 Controller/Agent 已完成。外部平台任务须在获批且隔离的环境执行；本仓库只维护契约、计划、证据索引和审阅记录。

## 1. 任务总表

| ID | 任务 | 负责人建议 | 依赖 | 交付物 | 优先级 |
|---|---|---|---|---|---:|
| S1-T01 | 冻结 87 项主清单与当前仓库映射 | 项目负责人/数据负责人 | 无 | inventory、差异台账、源码/目标 hash | P0 |
| S1-T02 | 现役 Controller/Agent contract discovery | 平台负责人 | T01 | capability snapshot、API 差异表 | P0 |
| S1-T03 | Safety Planner 规则与输出 | 转换/安全负责人 | T01 | planner schema、规则表、dry-run | P0 |
| S1-T04 | Execution Profile 与 Runner Capability | 平台负责人 | T02/T03 | profile schema、capability schema | P0 |
| S1-T05 | 网络隔离 Attestation 探针 | 平台负责人/安全审阅 | T02/T04 | 三 runner 现场证明、失败码 | P0 |
| S1-T06 | Permit 签发、绑定、过期和幂等 | Controller 负责人 | T03/T04/T05 | permit contract、拒绝测试 | P0 |
| S1-T07 | benign process profile | Agent 负责人 | T04/T06 | 进程树/资源/清理证据 | P1 |
| S1-T08 | synthetic data / local surface fixture | Fixture 负责人 | T03/T04/T06 | fixture registry、manifest、generator | P1 |
| S1-T09 | loopback/isolated stub fixture | Fixture/网络负责人 | T05/T06 | stub、网络事件适配器、oracle | P1 |
| S1-T10 | controlled target simulator 评估 | 安全负责人 | T08/T09 | simulator 设计、限制和批准记录 | P2 |
| S1-T11 | evidence index 与结果归因 | Controller/评估负责人 | T06-T10 | 分层 report、failure taxonomy | P0 |
| S1-T12 | 3–5 项最小可证伪灰度 | 项目负责人 | T01-T11 | canary report、阻断/修复清单 | P0 |
| S1-T13 | 分层扩大到 87 项 | 批次负责人 | T12 通过 | 批次 run、汇总和未达标清单 | P1 |
| S1-T14 | compatibility / rollback rehearsal | 平台负责人 | T06/T11 | 旧 capsule 对照、新旧报告差异 | P1 |
| S1-T15 | 阶段封版与运维移交 | 项目负责人 | T13/T14 | stage closure、runbook、风险接受记录 | P0 |

## 2. 任务详情

### S1-T01｜冻结 87 项清单与数据差异

**目的：** 解决用户口径 `87 = 48 UNSAFE_NET + 10 REVIEW_SUBPROC + 29 UNSAFE_LOCAL` 与当前仓库 `batch-02..06` 分类文件不一致的问题。

**步骤：**

1. 以用户确认的 87 项 ID 为主键，不以目录序号或文件名推断。
2. 为每项登记 source/target、源码 hash、转换产物 hash、当前 case/batch、当前状态和安全事实。
3. 显式记录与当前 179 项分类池的关系：纳入、排除、重复、待确认。
4. 多标签行为拆成原子要求，保留原始分类和分类理由。
5. 任何无法定位源码或安全边界的项进入 `BLOCKED_INVENTORY`，不删除。

**完成信号：** 87 行主表无重复 taskId；每行至少一个 source evidence、一个当前状态和一个 disposition 候选；差异表可解释剩余 92 项。

### S1-T02｜现役能力盘点

**目的：** 不直接沿用旧仓库 Controller worktree 的配置；以现役 Controller 的 contract discovery 和三台 runner 现场返回为准。

**要求：**

- 记录 Controller 服务版本、contractSet hash、API 可用接口和 schema 版本；
- 记录每台 runner 的 baseline、Agent build hash、supported languages、snapshot/revert、清理状态；
- 单独确认当前是否支持 `networkMode`、network evidence、profile enforcement、fixture injection、Permit；
- 把“字段存在”与“字段真正进入执行路径”分开记录；
- 若只能得到 `READY=true`，明确标记为“无安全能力证明”。

**完成信号：** 形成 `capability-snapshot-YYYYMMDD.md/json`；所有未知字段列入实现缺口，不通过猜测补齐。

### S1-T03｜Safety Planner

**目的：** 将静态审阅结果稳定映射到 profile/fixture/oracle 要求。

**完成信号：** 同一输入至少重复规划 10 次结果 hash 一致；多标签规则不会自动覆盖更高风险约束；人工 override 有独立审计记录。

### S1-T04/T05/T06｜Profile、Attestation、Permit

**共同约束：** 三者必须串联验证，不能分别做“看起来存在”的字段改造。

**完成信号：**

- profile 不支持时 job 被拒绝；
- Attestation 缺默认路由/出口/fixture/清理证明时不签 Permit；
- capsule hash、runner、profile、fixture 或 oracle 任一变化时 Permit 失效；
- 网络 profile 只允许声明的 Controller/artifact/stub 目的地；
- HTTP 重试不会导致同一 Permit 重复运行。

### S1-T07｜受限子进程

**最小范围：** 只验证 benign child 的父子关系、退出码、超时和资源边界。不能以此放行注入、提权、服务改写或任意命令通道。

**完成信号：** 源/目标两侧 process tree 均可取证；超时和孤儿进程会 fail closed；revert 后 runner clean。

### S1-T08/T09｜合成数据与网络 stub

**最小范围：** 合成 credential/profile、临时文件、loopback HTTP/TCP、固定成功/失败/超时响应。

**完成信号：** 观察面能回指行为义务；日志不含秘密明文；网络 trace 能区分允许 stub、拒绝出站和未观测；清理失败不会被标为通过。

### S1-T10｜受控靶标

**前置条件：** 先完成风险评审和独立批准。没有批准的 simulator 不得进入执行队列。

**完成信号：** 目标只有测试状态机，无真实外部入口；报告用 `CONTROLLED_TARGET_BEHAVIOR_OBSERVED`，不使用真实 exploit/persistence 结论。

### S1-T11｜证据归因

**完成信号：** 每个结论同时列出 safety、environment、build、execution/comparison；`INFRA/ENV` 不被重写成 `FAILED_CODE`；`comparison matched` 没有 oracle 时保持 `UNVERIFIED`。

### S1-T12｜最小灰度

**建议样本：**

1. 一项纯本地安全样本；
2. 一项 loopback/isolated stub 网络样本；
3. 一项 benign subprocess 样本；
4. 一项 synthetic data/local surface 样本；
5. 一项无法建立 fixture 的样本，验证阻断路径。

**单一变量：** 第一轮只引入 Stage 1 profile/attestation/permit，固定转换产物、工具链、oracle 和 runner 选择。

**成功信号：** 每项都有确定 disposition；可运行项实际提交并有完整证据；不可运行项被稳定拒绝；无重复 job、无静默丢失、无跨边界连接。

### S1-T13｜扩大到 87 项

只在 T12 通过后执行。按 profile 分层，逐层封批，不允许把所有 `UNSAFE_LOCAL` 一次性转为 fixture。每项保留原始阻断和升级后结论。

### S1-T14/T15｜兼容、回滚和封版

**回滚条件：**

- 新 profile 可能放大出网或真实数据访问；
- Attestation/Permit 绑定可绕过；
- 清理/revert 失败；
- 旧安全样本结果被不解释地改变；
- 证据包不能复核。

回滚到上一版 Controller/Agent snapshot，保留新版本失败证据，不恢复为“假通过”。
