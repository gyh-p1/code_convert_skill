# 四例跨 OS × 场景候选与检查依据

> 状态：已选入一个公开上游长源候选；C01 run-02 经逐例授权完成隔离探索评估，四例正式比较暂缓；C02 复用该源，C03/C04 仍为规格。第二份独立长源已为**当前编译质量阶段**选入并冻结：rxi/fe（见下 §1）
> 更新：2026-09-27
> 共同语言方向：C → C++；四例试点计划为 ≥600 有效 LOC、物理文件 ≤700 行；uhttpd 是已确认的超限探索例。当前编译质量阶段将物理行放宽到 ~900（见[阶段方案](../stages/final-output-compile/阶段方案.md)）

## 1. 旧仓库筛选结果与当前选择

只读盘点旧仓库 `E:\桌面文档\Code_Convert` 的 `.codeconvert-state/datasets/`、`benchmark-cases/c_cpp_fixed/cases/c/` 和知识库。**未找到四个同时满足 C 源文件、长单文件、跨 OS 场景、可授权且有安全行为 oracle 的现成样例。**唯一明确的长 C 源 `harmless_long_fixture.c` 为 640 行，同平台内存聚合和有限文件写入；它另存于 [同平台候选](cases/long-file-structure-candidate/case.md)，有效 LOC 低于本轮长例门槛，不占名额。下面四格是 C01/C02 使用同一 uhttpd 源快照的方向任务，加上两个待准备短场景。

| 旧资产 | 初筛结论 |
|---|---|
| Windows `http_upload.c`（93 行） | 涉及向指定主机发送数据；不满足长文件，真实外联目标/授权不明，排除 |
| `attack_chain.cpp`（438 行） | 已是 C++，包含持久化、混淆和其他复合副作用；排除 |
| `speck_encrypt.c`（75 行） | 外部 malware 教程衍生的 payload 处理，许可证/必要性不明；排除 |
| `T1566_001.c`（25 行） | 含隐藏命令/进程启动，不满足试点安全边界；排除 |
| `environment.c`（12 行） | 枚举主机环境，可能输出敏感信息，且非长文件；排除 |
| 名称带 scanner/vulnerability-checker 的旧 artifact | 是转换产物而非获审源—目标基准，外部网络风险未厘清；排除 |



### 当前选入：uhttpd（只归档源候选）

用户确认采用 [PJO2/uhttpd 的 uhttpd.c](cases/c01-linux-win-network/case.md)。固定源快照位于 [`sources/uhttpd/`](sources/uhttpd/source.md)，Commit `59d17b86ec9f2a70ce1f4369b4c148824be55155`，保留 GPL-2.0-or-later `LICENSE` 和对应 `UPSTREAM-README.md`。它是可独立启动的单文件跨平台 HTTP 服务，可在明确 loopback 与临时 docroot 后观察 HTTP 响应。文件 1,317 物理行，超过 700 行计划上限；仅作为用户确认的**超限探索候选**，不证明 700 行范围。

同一个源快照可用于 C01 Linux C → Windows C++ 和 C02 Windows C → Linux C++ 两个方向任务，但这只是一个独立长源样例；“至少两份不同长源”的要求仍未满足。C01 现有 run-01 智能体稿与 run-02 配置模型稿两份探索性 C++ 输出；run-02 后续经用户逐例授权完成隔离探索评估和一次修订，仅修订稿在有限 oracle 下匹配。它们都不是正式冻结的基线，也不代表其他样例获批。

### 当前编译质量阶段选入：fe（第二份独立长源，已冻结）

用户为[最终交付编译质量与 Skill 拓展](../stages/final-output-compile/阶段方案.md)阶段选定 rxi/fe 的 `src/fe.c` 作为第二份独立长源，源快照冻结于 [`sources/fe/`](sources/fe/source.md)，Commit `3efa075`（2020-04-05；40 位全 SHA 因 API 限流未解析，改以文件 sha256 固定完整性），MIT 许可，保留 `LICENSE` 与 `UPSTREAM-README.md`。它是一个自包含的小型 Lisp 解释器：`fe.c` 879 物理行（配 `fe.h` 61 行），**无任何平台 `#ifdef` 分支**，仅含 `<string.h>` + 标准头，无 `system`/`exec`/`socket`/`unlink`/`remove`，无网络（唯一 `fopen` 在可选的 `#ifdef FE_STANDALONE` REPL 中读取脚本路径）。

fe 与 uhttpd 是两份**不同的独立长源**，就此满足此前记录的“第二份独立长源”缺口（uhttpd 只算一份且超 700 行）。fe 的用途是当前阶段的**编译证据**（本阶段只读 build 证据，不要求运行、不设行为 oracle）；它尚未纳入四例跨 OS × 场景试点的某个格子。默认按翻译单元编译（无 `FE_STANDALONE`），双侧 build 命令与目标工具链/标准/隔离授权在开具体转换 run 时冻结，`sources/fe/source.md` 只记快照，不代表已获编译授权或已验证。

## 2. 四格候选与执行状态

| Case ID | 源→目标 OS | 场景 | 拟议无害源行为 | 状态 |
|---|---|---|---|---|
| [`c01-linux-win-network`](cases/c01-linux-win-network/case.md) | Linux → Windows | 网络 I/O | 复用 uhttpd 单文件服务；C01 为 Linux C → Windows C++，固定 loopback/docroot oracle | 已选候选；1,317 物理行，超限 |
| [`c02-win-linux-network`](cases/c02-win-linux-network/case.md) | Windows → Linux | 网络 I/O | 复用同一 uhttpd 源快照；C02 为 Windows C → Linux C++ | 方向任务候选；不构成第二份独立长例 |
| [`c03-linux-win-filesystem`](cases/c03-linux-win-filesystem/case.md) | Linux → Windows | 文件 I/O | 只在 case 私有临时目录对固定文件做创建、覆盖、追加、读取及失败路径 | 规格候选 |
| [`c04-win-linux-process`](cases/c04-win-linux-process/case.md) | Windows → Linux | 受限进程调用 | 仅启动 case 自带、可审阅的固定无害 helper，检查参数/环境/退出与清理 | 规格候选 |

C01 已关联用户确认的 uhttpd 源；C02 计划复用同一源作反向 OS 任务。uhttpd 超过 700 物理行，是本次显式选择的超限探索例，不能用于声称达到既定 ≤700 行目标。C03/C04 仍为待写源码的规格。另加的同平台 fixture 只作结构控制例；长例必须记录物理行、有效 LOC 与 token 数并审查逻辑密度，不得填充凑数。四例覆盖两个 OS 方向、网络/文件/受限进程三个场景；不要求覆盖全部 ATT&CK 战术。语义场景已有网络 I/O、文件 I/O 与并发初稿（未经转换验证）；系统方向已有套接字层 [POSIX ↔ Winsock](../../skills/systems/posix-winsock/SKILL.md)、[POSIX ↔ Windows 文件路径](../../skills/systems/posix-windows-filesystem/SKILL.md) 与[线程](../../skills/systems/posix-windows-threads/SKILL.md)初稿。进程（C04）场景/系统方向仍无 Skill；所有系统方向初稿在验证前都不能称为已验证能力。
## 3. 共同检查依据

**转换前冻结**每例的输入、源码版本、工具链/标准、OS/架构、可观察行为义务、允许的跨 OS 差异和安全停止条件。冻结后无 RAG 与 RAG 组读取同一份源文件；只改变检索/知识注入，不因失败事后修改 oracle。

- **语法/编译**：分别在声明的源/目标工具链记录命令、标准、错误类别与结果 `pass/fail/inconclusive`。缺编译器、缺平台依赖不能写成语法失败；编译成功不能写成功能等价。
- **全文件完整性**：对照源文件地图核对类型、函数、入口、全局状态、调用关系、条件编译、跨段符号、错误和资源清理；记录遗漏、重复、截断及未映射项。
- **行为**：预先固定同一组抽象输入，分别在对应隔离 OS 环境观察 stdout、stderr、退出状态和场景结果。平台原生错误码不同，预先定义语义类别映射；除预先定义的规范化外，默认字节精确比较。
- **安全**：逐例只允许声明的文件、loopback 连接或固定 helper；观察到未知目标、真实凭证、未声明进程/文件写入时停止。没有经批准的隔离环境时，只能完成静态材料审阅。

这四例仅构成探索性试点，不能推导总体功能准确率或 700 个物理源代码行的支持能力。阶段 03 的无 RAG 和阶段 04 的 RAG 结果须逐例并排报告通过、失败和不确定。


## 在线候选搜索记录（2026-09-25）

为满足“可独立启动、转换后易观察”，用户选定 uhttpd。其他公开长文件仍仅作比较：Sandbird 约 800 SLOC 但由 `.c`/`.h` 多文件组成；Git `http-backend.c` 约 829 物理行、695 LOC 且依赖 Git 内部运行时并有仓库写入口；libevent `bufferevent.c` 是依赖库组件且超过 700 物理行。它们不如 uhttpd 适合作为首个可直接启动观察的候选。上述搜索结果只用于筛选，不把外部项目的运行/测试结论继承到本项目。
