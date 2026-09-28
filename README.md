# Code Convert Skill

一个面向网络攻防相关代码、以转换知识为中心的轻量 Skill 项目。智能体按**语言方向 × 实际语义场景 × 源/目标系统方向**选读知识，并使用 ATT&CK Enterprise 分类作索引。当前有 **C → C++**、网络/文件/并发场景、POSIX ↔ Winsock、POSIX ↔ Windows 文件路径/线程初稿与长文件工作流；进程场景和系统方向仍缺。fe、stest、realpath、pwd 已取得逐例目标编译证据，但功能保持、真实攻防场景效果及 700 行上限均未验收；C → Go 仅有受基础设施故障阻断的探索稿。

## 使用方式

- 平台无关的知识入口：[根 SKILL.md](SKILL.md)；按任务读取 [C → C++](skills/directions/c-to-cpp/SKILL.md)、[网络 I/O](skills/scenes/network-io/SKILL.md)、[文件 I/O](skills/scenes/file-io/SKILL.md)、[并发场景](skills/scenes/concurrency/SKILL.md)，以及适用的 [POSIX ↔ Winsock](skills/systems/posix-winsock/SKILL.md)、[POSIX ↔ Windows 文件路径](skills/systems/posix-windows-filesystem/SKILL.md)、[POSIX ↔ Windows 线程](skills/systems/posix-windows-threads/SKILL.md)；ATT&CK 分类入口见 [战术索引](skills/attack-tactic-index/SKILL.md)。
- 在 Codex 中，本仓库通过 [发现入口](.agents/skills/code-convert/SKILL.md) 暴露 `$code-convert`。它只指向上述知识文件，不复制转换规则。新建 Codex 会话后可显式使用 `$code-convert`；其他智能体平台需要按其自身的 Skill 加载方式接入根入口。
- 处理 C → C++ 请求时阅读方向 Skill；涉及网络 I/O 再读对应场景；套接字代码跨 Linux/Windows 时加读套接字系统方向。源 OS 与目标 OS 不同且落在已有系统方向之外（尤其进程等）时必须指出迁移知识缺失；文件系统方向仅有部分逐例编译证据，线程方向仍为初稿，均不能宣称功能已验证；其他语言方向不宣称专项支持。
- 长单文件按需阅读[长文件转换工作流](skills/workflows/long-file-conversion/SKILL.md)。默认只阅读、编辑代码和说明，不运行来源不明的源代码或转换产物。

## 本工作区的模型调度

后续具体代码转换由 Agent 读取根目录 `.env` 的 `CODE_TRANSLATOR_BASE_URL`、`CODE_TRANSLATOR_MODEL`、`CODE_TRANSLATOR_TEMPERATURE` 和 `OPENAI_API_KEY`，将只读源码与按画像选中的 Skill 发送给配置模型；Agent 只负责调度、静态审阅、交付和必要的同模型修订。不得把密钥写入文档、manifest 或请求正文；配置模型不可用时不得自行代写并冒称模型产物。本项目不增加独立转换运行时或测试框架。

C01 已有独立的 [run-02 配置模型探索稿](docs/test/dataset/c-to-cpp/c01-linux-win-network/output/no-rag/run-02/README.md)，与先前 run-01 区分；修订稿通过有限的五个 loopback HTTP 请求输出比较，不是正式 No-RAG 基线。现有 run 的逐例状态见[按语言方向归档的数据集](docs/test/dataset/README.md)。
## 当前边界

Skill 给出转换决策依据，不替代编译器、隔离环境或人工确认。当前实施[最终交付编译质量与 Skill 拓展](docs/stages/final-output-compile/阶段方案.md)：只把最终交付代码在声明的目标工具链下编译通过作为本阶段“语法正确”的操作性判据，中间失败/修订用于开发诊断，功能正确性暂不统计。原固定四例无 RAG/RAG 专项已[取消](docs/stages/four-case-cancellation.md)；C01 探索稿及证据仅作历史材料。Codex 入口只是发现适配，不是独立代码转换程序。

业务与能力真源：[项目业务文档和能力边界](docs/项目业务文档和能力边界.md)。协作规范：[项目开发规范](docs/项目开发规范.md) · [Skill 编写规范](docs/Skill编写规范.md) · [安全边界](docs/安全边界.md)。阶段安排见 [docs/stages](docs/stages/README.md)。旧仓库是候选资料，不代表本项目已实现同样能力。测试材料见 [docs/test](docs/test/README.md)：已有 run 按语言方向归档，旧攻防用例仅静态候选。**标准执行形态统一为双侧执行**：交获批隔离 VM 的 comparison capsule 构建并运行源、目标两侧，源侧作对照基线，本阶段只读取其 **build 证据**作为当前编译结论，execution/comparison 不计入功能率；源无可运行入口时默认补写最小入口/驱动。远端 Controller/隔离 VM 恒就绪且已授权，到评估步骤直接提交执行；仅当 Controller 真实返回基础设施故障才记环境失败，任何情况不在本机编译或运行。
