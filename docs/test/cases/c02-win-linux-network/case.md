# C02：uhttpd Windows → Linux（同源反向任务候选）

> 状态：candidate（复用用户确认的源快照；未批准编译/执行）  
> 共享源样例：[`../../sources/uhttpd/uhttpd.c`](../../sources/uhttpd/uhttpd.c)  
> 上游来源与许可：[source.md](../../sources/uhttpd/source.md)

- 源：在 Windows/Pelles C 环境编译并观察原始 C 版本；目标：Linux C++。
- 场景、隔离约束、固定临时文档集和 GET/HEAD/404/415 oracle 与 [C01](../c01-linux-win-network/case.md) 共用，不复制或改动源快照。
- 仍为 1,317 个物理行，超过 700 行规划上限；此反向任务与 C01 共用同一源，不能算第二个独立长例。
- 在被批准前不编译/运行。Windows 源运行只允许 loopback 与 case 临时 docroot；不接受公网绑定或真实文档。
- 这是用同一独立源文件建立的**反向 OS 任务**，可比较 OS 方向条件；不等同于第二个独立长代码样例，不能满足“至少两份不同长源文件”的样本数量要求。

结果应写入本 case 的 `output/no-rag/`；RAG 结果仅在冻结相同源输入的 No-RAG 基线后写入 `output/rag/`。
