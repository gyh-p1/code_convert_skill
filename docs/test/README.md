# 测试与转换材料区

本目录集中保存候选/获批试验的源文件、转换产物和逐例检查记录，避免把测试代码放进项目根目录。四例矩阵与检查依据见 [four-case-matrix.md](four-case-matrix.md)。目前已归档一个 uhttpd 上游源快照，供 C01/C02 两个方向候选复用；它超过 700 物理行，只是超限探索候选。C01 已有 run-01 智能体文本探索稿与 run-02 配置模型文本探索稿及交付记录，但不是正式 No-RAG 基线，未编译/运行。C01/C02 复用同一源，不等于两份独立长例；C03/C04 仍只有场景规格，第二份独立长源尚未选定。

## 目录约定

```text
docs/test/
├── README.md
├── four-case-matrix.md
├── sources/<source-id>/       # 可复用、保留许可的上游源快照
└── cases/<case-id>/
    ├── case.md                  # 可通过 sourceRef 引用共享源快照
    └── output/
        ├── no-rag/           # 无检索目标代码及 result.md
        └── rag/              # RAG 目标代码及 result.md
```

保留源文件原名；目标代码命名为 `target.<ext>`，说明为 `result.md`；多轮运行使用 `run-01/` 等目录。No-RAG/RAG 两组引用同一份源，不复制后分别修改。不得存入凭证、个人信息、未经筛选的大型日志或构建产物。

## 状态与执行门槛

case 状态使用 `candidate`、`approved-for-trial`、`excluded` 或 `completed`。候选可以存放未验证草稿，但不得称为基线或通过结果。只有来源/许可、安全副作用、行为 oracle、隔离环境和清理方案逐项审阅后，才可批准编译/运行和冻结基线。RAG 组必须在 No-RAG 基线冻结后进行。
