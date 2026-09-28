# step-05：按转换方向归档数据集与真实攻防样例筛选

> 状态：已完成（用户 2026-09-28 指定“直接迁移并修复引用”；七个 case 已归档，静态校验完成）
> 归属：[阶段 index](index.md)

## 目标

把已经产生转换 run 的 case 按源语言→目标语言归档，使每个方向的样例、最终交付版本、证据等级和限制可直接查找；为后续选取**真实攻防行为**样例建立准入规则与旧用例候选索引。先审阅旧 Controller 的功能证据能力与缺口，形成后续功能判据的设计输入。

## 纳入与非目标

- 纳入：迁移现有 case 的完整目录，修复项目内活动文档与移交清单引用；建立轻量 Markdown 数据集索引；只读盘点用户提供的旧用例目录与旧 `Code_Convert` 仓库；更新未来样例选择规则。
- 本步骤当时仅保留规格 C02–C04 与长文件 fixture；其后用户取消固定四例，C02–C04 规格已移除，长文件 fixture 迁至 `docs/test/candidates/`，见[step-06](step-06-cancel-four-case-cleanup.md)。
- RC4 的 run 已取得两次基础设施错误终态，归入 C→Go 方向但标 `BLOCKED-INFRA-ERROR`，不计编译通过。
- 不执行旧用例、现有源码、转换产物或构建脚本；不修改 Controller、Agent、Evaluation Core；不扩充正式功能正确率，不把旧报告继承为本项目证据。
- 不删除原始请求/响应、capsule 或第三方证据；冻结输入 Markdown 仅修迁移造成的路径链接，不改任务契约、源/目标代码或原始第三方证据。

## 依赖与前置

1. 先核对工作树现有未提交内容，保留全部用户资产与原始结果。
2. 移动前核对源/目标绝对路径均在本仓库 `docs/test/` 内；记录迁移映射。
3. 对旧候选先核来源、许可、是否上游原件或单文件改写、依赖、真实行为、可控副作用和所需证据；目录战术名及聚合来源说明不足以证明逐文件可用。
4. 本阶段仍以最终交付编译结果为当前计分口径；功能判据只作下一阶段设计输入。

## 预计改动

| 原 case | 新目录 | 说明 |
|---|---|---|
| `c01-linux-win-network` | `docs/test/dataset/c-to-cpp/c01-linux-win-network/` | run-01 文本探索、run-02 第三方探索，均保留原身份 |
| `fe-lisp-c-to-cpp` | `docs/test/dataset/c-to-cpp/fe-lisp-c-to-cpp/` | 同 OS 编译 PASS |
| `stest-fs-posix-to-win` | `docs/test/dataset/c-to-cpp/stest-fs-posix-to-win/` | 跨 OS 编译 PASS |
| `realpath-fs-posix-to-win` | `docs/test/dataset/c-to-cpp/realpath-fs-posix-to-win/` | 跨 OS 编译 PASS |
| `pwd-fs-posix-to-win` | `docs/test/dataset/c-to-cpp/pwd-fs-posix-to-win/` | 跨 OS 编译 PASS |
| `du-fs-posix-to-win` | `docs/test/dataset/c-to-cpp/du-fs-posix-to-win/` | 源基线失败，目标未构建 |
| `rc4-c-to-go` | `docs/test/dataset/c-to-go/rc4-c-to-go/` | same-runner 基础设施错误，目标未构建 |

本步骤新增 `docs/test/dataset/README.md` 作为数据集入口、每个方向一个索引和旧用例候选索引；更新 `docs/test/README.md`、当时仍存在的四例矩阵、项目业务文档、阶段 index 与受影响的 Markdown 引用及 `evaluator_manifest.json` 路径。四例矩阵在后续取消步骤中移除。冻结输入 Markdown 仅调整导航链接；原始模型请求/响应、Controller JSON、capsule 内的历史路径保持原样，并由迁移映射解释。

## 真实攻防样例准入规则

- 以**真实行为与来源**双轴筛选：优先可追溯上游版本的攻防代码或清楚标记的改写件；另记攻击链环节、实际 API/协议、输入、输出、副作用和依赖。不能只凭 ATT&CK 目录名、文件名或“红队”描述判断真实度。
- 允许高风险样例作只读静态候选；进入转换/隔离评估前，逐例确定许可、授权、无真实凭证/目标、网络去向和可回滚边界。优先用隔离网络、假数据与受控服务保留真实决策路径，而非把行为改成空桩。
- 每个拟作功能评估的 case 在转换前写出至少一条可观察成功义务、一条关键失败/拒绝路径、平台允许差异和证据缺口；若 Collector 观测不到关键行为，标 `UNVERIFIED`，不得用 stdout 长度或编译结果替代。
- 先维持编译质量数据与功能候选数据分栏，不混算通过率。

## 旧 Controller 静态审阅与后续判据设计

旧仓库 `E:/桌面文档/Code_Convert` 的 `input-profile` 契约列出 output、filesystem、processes、registry、network；当前 Agent 实现仅采集前三类，registry/network 返回超出当前版本范围。下一阶段先为**实际选入的场景**冻结输入、正常/错误路径、可观察副作用、比较规则、不可观测处理和跨 OS 差异，再决定 Controller/Collector 的最小变更。same-runner `artifactHash` 交接错误作为独立基础设施缺陷记录；不在本步骤修改或部署 Controller。

## 验收依据与人工检查

1. 迁移表所列 case 在新目录存在且旧 case 目录不再保留副本；候选区只剩未归档规格/fixture。
2. 数据集索引逐例标明方向、攻防场景、来源、运行状态、编译证据、功能证据与结果链接；阻断样例不算通过。
3. 活动 Markdown 相对链接可定位，活动移交清单指向新目录；原始证据字节及已冻结源码/目标代码 hash 不因迁移改变。
4. 旧用例候选索引注明目录规模、初筛候选与逐文件来源/许可/行为/隔离条件的待核项，不把未审旧例当作已获批测试。
5. 记录只做静态检查；没有本机编译或运行任何样本。

## 风险与停止条件

- 迁移可能使历史请求正文、报告、zip 内的旧绝对/相对路径失效；这些是历史快照，不改写其内容。活动入口必须给出旧→新映射。若发现当前消费者直接依赖不可重定向的旧路径，暂停该项迁移并更新方案。
- 旧目录有真实攻击行为、聚合来源说明且少量 C 文件带单独来源/许可线索；未逐文件核实前只可列候选。若含真实凭证或外部目标，停止导入该文件。
- Controller 修改可能改变证据契约和部署包；先完成代表场景判据与契约影响审阅，再另立实施步骤。

## 完成记录与未验证部分

- 七个 case 已迁至 `docs/test/dataset/c-to-cpp/`（六个）和 `c-to-go/`（一个）。**在本步骤完成时**，`docs/test/cases/` 还留 C02–C04 规格与长文件结构候选；随后 step-06 取消 C02–C04，并将长文件候选移到 `docs/test/candidates/`。本步骤建立了[方向索引](../../test/dataset/README.md)、[旧候选索引](../../test/dataset/legacy-candidates.md)和[功能判据草案](functional-detection-criteria.md)。
- 人工/静态校验：扫描 445 个本地 Markdown 链接，活动项目文档无失效链接；余下四个失效链接均在**未改的 fe 上游 README 快照**中，指向其未归档的上游 `doc/`、`scripts/`。解析 16 份活动 manifest/Controller report JSON 无错误；抽查 C01、fe 的目标代码与 C01 capsule 三份文件，移动前后 Git blob 相同。`git diff --check` 无空白错误。
- 未做：旧用例逐文件上游/许可核验、任何样本编译或运行、功能 oracle 实证、Controller 修复或部署。旧仓库审阅和功能判据只能作为后续设计输入，不能宣称真实攻防转换效果已验证。
