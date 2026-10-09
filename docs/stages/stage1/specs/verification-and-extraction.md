# Spec 03｜双侧验收、批次证据与完整剥离

> 更新：2026-10-09；状态：开发/验收规格，动态验收未完成
> 消费者：T03–T05 执行者与独立系统接收者

## 1. 准入所需记录

每项任务绑定 batch/task/case、源/目标文件哈希、工具链/OS/架构、构建命令、真实运行入口、最小中性驱动、输入和预期观察、允许差异与禁止副作用。分类器只是 source-text-only 的旁证，目标、驱动、构建步骤需独立审阅。

保存本次授权对象、runner、实际隔离配置及验证时间、允许实验网目标、合成数据、文件/进程/权限界限、资源限制和清理方案。硬编码外部目标须先在环境层阻断/重定向并验证；不使用真实凭据、生产网或外部 C2；不为取证删除核心行为。READY、私网地址和快照不代替这些记录。

批次输入缺失单列：本轮39项必须逐条核对（**24 条可在原始交接包中按 SHA-256 恢复，15 条本机未找到**）；
不能根据文件名猜测原因，不自动关闭防护。恢复动作须复制后复验 SHA-256 与字节数，同名但哈希不同的文件不得替代。
若需替换，建立新冻结版本与映射，旧任务和旧结果不回填。
逐条清单见[输入恢复性核查](../../../test/dataset/stage1-admission-recheck-2026-10-09/missing-input-recovery.md)。

## 2. 提交和恢复

复用[Controller 适配](../../../../references/adapter/controller/remote-controller-adapter.md)的 comparison capsule、multipart 接口和状态轮询，不提交分类列表作为 job。保存输入 manifest、capsule 哈希、请求时间、接收端和 jobId。

每次尝试独立记录；回执丢失记 SUBMISSION_UNKNOWN，查明接收/终止/清理状态前不重投。并发和队列以平台真实能力为准，不把40项批量需求解释为40并发。现有调度若缺恢复能力，应先修现有流程，不新增已取消的 T07 封装。

## 3. 逐侧证据与判定

| 证据 | 检查 | 结论边界 |
|---|---|---|
| job/report | jobId、caseId、任务输入与版本一致 | COMPLETED 只说明编排终态 |
| source/target evidence | role、artifactHash、inputProfileHash、runner、快照匹配 | 仅文件名相同不足以证明同版本 |
| build | status、exitCode、真实诊断、工具链及是否实际执行 | completed/0 在声明检查方式下通过；环境故障不算代码失败 |
| execution | performed、status、exitCode、timedOut、真实入口 | 缺失/跳过不算双侧完成；非零可属于冻结错误路径 |
| output/observations | 原始输出/digest、截断、适用维度及 limitation | 没采到不能写 matched |
| comparison | policy 与服务器配置、差异、规则来源、预期结果 | semantic_pass 不等于普遍等价 |
| lifecycle | 两侧 cleanup、污染标志、结束后的 runner 状态 | 失败隔离并停止环境复用 |

源侧失败的独立诊断若按 Spec02 实现，目标证据可单列，但无有效源基线时 behavior=inconclusive。当前尚未实现该模式，不按设计字段解释已有 job。

## 4. 最小验证矩阵与统计

先固定无害对照，保持输入/oracle不变，只改变发布版本。Windows→Linux、Linux→Windows及涉及macOS的源/目标角色须有实际取证；不要求笛卡尔积，但每个声称支持的角色/路线要有证据或明确未验证。

正向：确定性输出及文件一致；允许的临时路径/时间戳/临时端口噪声。负向：固定端口变化、业务文件缺失、显式 include 噪声文件缺失、退出码变化、截断流证据不足、重复资源关联不同。每例预先写预期，不能见结果后修改 oracle。

随后取3–5个准入通过的真实任务验证正常/错误路径，再单次提交≥40进入自动队列；每项必须有可追溯终态，无无声漏项和重复执行，环境阻断单列。分类全量复跑不能替代此步骤。

固定分母与去重键 batch/task/最终冻结版本；同项重试仅最终版本入主汇总，所有 attempt 保留。分别报告输入完整数、审阅通过数、提交数、源执行数、目标执行数、双侧执行数、目标 build PASS、比较分布、清理失败和未知状态。历史219项缺失仍留在历史分母；新批次必须显式标明筛选范围。75%覆盖目标未达就报告缺口。

## 5. 完整剥离清单

来源候选：`E:\桌面文档\Code_Convert\.worktrees\evaluation-noise-v1`；
目标：`E:\桌面文档\Agents System\third-party-evaluation-system`。
实际迁移以 T05 冻结并验收的版本为准，不把当前契约不匹配的候选当已验收成品。

### 5.1 实测来源结构（2026-10-09 只读核对）

**权威发布清单**：`infra/remote-stack/release-files.json`（schemaVersion、files、dependencies、roleEntrypoints）。
其 `files` 共 **86 项，全部存在**（0 缺失），构成为：

| 来源组 | 文件数 |
|---|---:|
| apps/remote-controller | 28 |
| packages/evaluation-contracts | 20 |
| infra/remote-stack | 17 |
| apps/vm-agent | 11 |
| packages/evaluation-core | 10 |
| **合计** | **86** |

`roleEntrypoints` 定义四个安装入口：`controller` → `install-controller.ps1`；
`agentWindows` → `install-agent-windows.ps1`；`agentLinux` → `install-agent-linux.sh`；
`agentMacos` → `install-agent-macos.sh`。

`dependencies` 定义发布必需的离线材料，**当前状态未核对**：

| 依赖键 | 期望路径 |
|---|---|
| windowsRuntime | `windows-x64/python-runtime.zip` |
| wheelhouses.controller-windows-x64 | `windows-x64/controller` |
| wheelhouses.agent-windows-x64 | `windows-x64/agent` |
| wheelhouses.agent-linux-x64 | `linux-x64/agent` |
| wheelhouses.agent-macos-x64 | `macos-x64/agent` |

完整来源树（含未列入发布清单的目录，供判断哪些不迁）：

```
evaluation-noise-v1/
├─ apps/
│  ├─ remote-controller/          ← 迁入（发布清单 28 项）
│  ├─ vm-agent/                   ← 迁入（11 项，Windows/Linux/macOS 共用）
│  └─ translator-mcp/             ← 排除（§5.3）
├─ packages/
│  ├─ evaluation-core/            ← 迁入（10 项）
│  └─ evaluation-contracts/       ← 迁入（20 项 schema）
├─ infra/remote-stack/            ← 迁入（17 项；含 install/uninstall/verify/smoke、
│  │                                 release-files.json、dependency-sources.json、
│  │                                 requirements-{controller,agent}.lock、
│  │                                 templates/、lib/、acceptance/）
├─ tools/
│  ├─ release/、state_paths.py    ← 迁入（发布/验证工具与状态路径）
│  ├─ contracts/、evaluation/、datasets/  ← 按 release-files.json 对账后决定
│  ├─ 文档/                        ← 迁入（并入目标 docs/）
│  ├─ audit_samples.py、generate_technical_manual.py
├─ tests/architecture/            ← 迁入
└─ pyproject.toml                 ← 迁入（剔除 translator 引用后记录差异）
```

### 5.2 映射与检查

| 来源 | 目标内路径 | 检查 |
|---|---|---|
| apps/remote-controller/ | 原路径 | 服务、配置模板、既有测试及 API |
| apps/vm-agent/ | 原路径 | Windows/Linux/macOS 共用 Agent 及测试 |
| packages/evaluation-core/ | 原路径 | 证据、比较、报告实现 |
| packages/evaluation-contracts/ | 原路径 | 所有 Schema、相对引用、契约哈希 |
| infra/remote-stack/ | 原路径 | 原生安装/卸载/验证、模板、发布清单、依赖锁 |
| tools/release/、tools/state_paths.py | 原路径 | 发布/验证工具的导入和状态路径 |
| tests/architecture/ | 原路径 | 架构约束回归 |
| pyproject.toml | 原路径，剔除无关引用后记录差异 | 不依赖 Translator 目录或旧绝对路径 |
| 分类器 v2.3 与 47 项回归 | `classifier/safety_classifier_v2.py`、`classifier/test_safety_classifier_v2.py` | 保留两个文件相邻，回归按新路径可读 |
| 提交端实现（T01-d） | 评估栈内（Spec05） | 不放进转换 Skill 仓库 |
| 发布材料与脱敏配置 | 按既有发布形态保存 | 安装回执、原 ZIP、哈希及三角色配置 |
| 系统说明/API/运行与恢复指引 | docs/ | 路径指向目标自身，安全与能力边界明确 |

以 `infra/remote-stack/release-files.json` 逐项对账，还须盘点离线 wheelhouse、Windows Python runtime、
各 OS 工具链及运行前提。**源码完整与离线可安装包完整分开验收**；缺失材料不能用空目录或下载说明冒充已带齐。

### 5.3 排除项

模型凭证、SSH 私钥、VM 口令、`.env`、`.git`、未知二进制、**原始攻防样本**、运行缓存和 job 工作区、
**apps/translator-mcp 与任何 Translator/RAG 依赖**。无害验收 fixture 保留已审阅版本。
独立系统需要测试的是**评估栈**，不迁入整个转换产品。

> **目标目录现状（2026-10-09 核对）**：`third-party-evaluation-system` 下只有 `README.md` 与
> `classifier/README.md` 两个文件，其余 `controller/`、`vm-agents/`、`evaluation-core/`、`deployment/`、
> `docs/`、`tools/`、`classifier/` 均为空目录。当前**不是**完整可部署系统；
> 且现有扁平目录名（`controller/`、`vm-agents/`）与 §5.2 要求保留的 `apps/`、`packages/`、`infra/`
> 相对结构**不一致**，迁移时须重建为目标结构，不能沿用现有空目录名。

## 6. 迁移步骤与恢复点

1. 冻结源 commit、dirty diff和验收发布/契约身份；共享工作区有新增变化先重新审阅。
2. 确認来源/目标绝对路径；先复制到目标受控暂存区域，记录每文件来源、目标和SHA-256，不删除旧部署。
3. 静态核对导入/Schema引用/发布清单/相对布局/脱敏配置；记录为独立化修改产生的新哈希。
4. 从新目录形成发布，仅在获批隔离环境做安装和双侧复验，回收相同验收矩阵的证据。
5. 通过后切换转换系统消费者文档/配置到新系统；清理旧分类器实现前检查引用并留回退材料。
6. 任一步失败保持旧部署，保留新目录为未验收状态；不删除证据，不把迁移前job算作新目录验收。

两项通过状态必须分开：迁移前双侧门槛通过才开始搬迁；迁移后独立部署复验通过才称完整交付。当前均未通过。

## 7. 最终交付单

接收者应得到版本/契约/文件清单、分类器及回归报告、当前支持的角色和观察维度、安装/回退入口、离线依赖清单、无害验收证据、能力限制和未覆盖项。安全/行为/编译/队列结果分开。单机链接检查、单元回归或历史作业不能替代这个交付单。
