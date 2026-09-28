# step-07：真实网络场景单例闭环

> 状态：已完成（同一案例从筛选、转换到隔离第三方 build 取证已闭环；功能只作有限信息记录）
> 归属：[阶段 index](index.md)
> 记录方式：同一案例的筛选、契约、基础设施诊断、转换与评估**在本步骤续写**。原 step-07/08/09 的拆分已合并，不再为这些子动作新建步骤。

## 目标、边界与交付

以 Red Canary Chain Reactor 的真实 Linux 网络调用模块作为一份 C→C++ 单文件转换案例，先解决可判定证据链，再由本工作区配置模型转换并交已授权隔离 Controller 取得**最终目标 build 证据**。行为比较仅按本案例冻结的有限义务报告，不计入当前功能正确率。本项目不建设本地运行时或通用评测框架。

已确认主源 [`networking_quarks.c`](https://github.com/redcanaryco/chain-reactor/blob/51c25c4c9dfdc73085c35882d6bbb58e56c006a7/src/networking_quarks.c) 的提交为 `51c25c4c9dfdc73085c35882d6bbb58e56c006a7`，MIT 许可，559 LF 物理行；伴随 `atoms.h`、`util.h`、`util.c`。源码已冻结于[源目录](../../test/sources/chain-reactor-network/source.md)，筛选与功能义务收在[case.md](../../test/dataset/c-to-cpp/chain-reactor-network-linux/case.md)。原件含其他方法与监听/fork 分支，不以一个受控连接的结果外推全文件功能。

## 已完成：筛选与契约

1. **旧资料筛选**：`ApiSetMap.c`、改写的 `ReflectiveLoader.c`、`http_upload.c` 各有来源、改写或观察阻断；结论见[旧候选审阅](../../test/candidates/real-scenario-source-review.md)。没有把它们直接纳入数据集。
2. **联网核源**：固定 Chain Reactor 发布方提交、许可证与四份文件哈希；与需要提权抓包的 Atomic T1040 作对照。选中的是具有真实 socket/syscall 行为的**攻击模拟组件**，不是完整在野攻击链。
3. **功能义务**：候选契约限定 Linux 同 OS 的 IPv4/TCP loopback `quark_connect`，写明正常、拒绝连接及源侧异常路径；单次 `send` 可能短写，`urand` 不完整检查，不能预设收到完整 512 字节或逐字节比较随机值。拟用获批 VM 内的 case receiver 输出有界 JSON，仅证明该 receiver 可见的行为。

## 基础设施诊断与无害预检

- **为何先处理它**：RC4 Windows 双侧任务两次返回 `baselineReference.artifactHash` 不匹配，目标未构建；Linux 同机是否同样受影响**未实测**。当前选 Linux C→Linux C++ 是为了隔离语言变量，不能为绕过故障临时改为跨 OS。
- **已定位的静态原因（2026-09-28）**：旧仓库 Controller 的 `job_staging.artifact_tree_hash` 按**相对 POSIX 路径字符串**排序；Windows Agent 的 `_workspace_digest` 按 `Path` 对象排序，Windows 路径比较忽略大小写。对 RC4 已归档源文件静态重算：Controller 顺序为 `WjCryptLib_Rc4.c`、`.h`、`rc4_decrypt_cli.c`、`run_case.py`，哈希 `9173ebe0…`；Agent 顺序从小写文件开始，哈希 `3c61a5e0…`。二者不同，且报错发生在 Agent 身份校验、源证据落盘之前；“same-runner 必然故障”是过宽归因。这只证明这一具体哈希不一致机制，仍须用无害工程测试验证修正。
- **选定修复及本地结果**：不改公共 hash 格式或放松校验，只让 Agent 按相对 POSIX 路径字符串排序，与 Controller 共用既有顺序语义。旧仓库已在 `codex/controller-path-hash` 独立短期 Worktree 加入仅含无害文本的 mixed-case 回归：修前 RED（Agent `/run` 400，同 RC4 错误），修后 GREEN；错误 hash 仍拒绝。相关 Agent/Controller/Job Staging/Orchestrator 工程测试 **67/67 通过**。本机未运行红队源码或转换产物。
- **部署边界**：本地测试通过不等于 VM Agent 已升级或远端 RC4/Chain Reactor 已验收；须按旧仓库部署/回滚程序一次性安排远端升级，并用无害 capsule 核对两侧 build/证据后才重提实际案例。功能检测维度扩充仍基于本案例义务单独审阅，不与此排序修复捆绑。
- **Linux 无害远端实测（2026-09-28）**：仅含固定 `hello.py` 的 Linux→Linux 双侧 capsule 于现役 Controller 提交，jobId `eval-20260928-122644-d769c056`，`COMPLETED`；源/目标 build 均 `completed/exitCode=0`，output `matched`、环境 `clean`。这证明该无害输入的 Linux 同机取证链路可走通，**不证明 Chain Reactor 能编译或功能正确**。与 Windows RC4 的混合大小写排序问题分开报告。
- **停止条件**：无法取得无害重现、根因不在当前仓库、变更牵涉未审的公共契约或运行中远程任务时，停下修订本步骤；不靠换 OS、放松哈希校验或本机编译样本绕过。

## 本案例转换与远端评估

1. 已冻结[上游源快照](../../test/sources/chain-reactor-network/source.md)、伴随依赖和**仅能指向 loopback** 的最小入口；上游公网示例 JSON 未入 capsule。主翻译单元 559 行不等于完整程序 559 行；伴随代码另计。
2. `.env` 配置模型一次生成 568 行完整 `target.cpp`（HTTP 200/`finish=stop`，机械去围栏），一次结构化自审 `NO-REPAIR-IDENTIFIED`/0 issue；原始响应、非敏感请求、token 与哈希均留在[run-01](../../test/dataset/c-to-cpp/chain-reactor-network-linux/output/no-rag/run-01/result.md)。无自修轮，模型自审不是编译结论。
3. 仅含 loopback `driver.c` 与 case receiver 的 capsule SHA-256 `6ffacb58…` 于 2026-09-28 提交授权 Linux VM Controller，jobId `eval-20260928-123304-add87d9d`，终态 `COMPLETED`/环境 clean。源 GNU C11、目标 GNU C++17 + 原样 C 伴随对象均 build `completed/exitCode=0`，最终目标编译判 **PASS**。目标有一条 C 专用 GCC pragma 在 C++ 中无效的非致命警告。
4. 两侧 `run_case.py` 的正常路径均接受一次连接、实际收到 512 字节、`sendResult=512`/退出 0；拒绝路径均 `sendResult=-1`/退出 1，两个 `validObservation=true`。Controller 仅 output 维度 `matched` 1/1；这是**有限行为信息**，不计当前功能率，也不证明未观测网络/进程分支或完整攻击链。真实原始证据见[返回目录](../../test/dataset/c-to-cpp/chain-reactor-network-linux/output/no-rag/run-01/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json)。Windows RC4 重评仍等 Windows Agent 升级。

## 预计改动与验收

- 本仓库：本步骤续写进度，[case.md](../../test/dataset/c-to-cpp/chain-reactor-network-linux/case.md)维护任务契约，[源说明](../../test/sources/chain-reactor-network/source.md)维护原件身份；run 产物按现有 `dataset/c-to-cpp/` 布局归档，不预建空壳。
- 旧 `E:/桌面文档/Code_Convert` 仓库：仅在无害复现与变更范围明确后修改 Controller/Agent/公共契约及相应工程测试；原项目 `master` 当前有一条未推送提交，动手前核对其工作树与分支边界，避免混入本案例。
- 本案例验收：无害同机 probe 及真实 Chain Reactor job 均取得两侧 build 证据；最终稿目标 build exit 0。功能逐义务报告为 N-01/N-02 在 receiver 范围内匹配，N-03 未触发，其余分支未覆盖。目标样本未在本机执行。

## 最近证据与恢复位置

截至 2026-09-28：本案例最终目标 build 以 Controller job `eval-20260928-123304-add87d9d` 真实证据 **PASS**；有限 loopback 两输入的 output JSON 匹配，功能不计分。完整生成/自审、capsule、两侧证据与局限见[run-01 result](../../test/dataset/c-to-cpp/chain-reactor-network-linux/output/no-rag/run-01/result.md)。Windows Agent 本地修复 `7d77158` 的 67 项工程测试已过但**未远端部署**，RC4 仍 `INCONCLUSIVE`，作为另一条基础设施后续事项。本步骤已闭环，无需为本例继续新开准备步骤。恢复时读阶段[index](index.md) → 本步骤 → run-01 result。
