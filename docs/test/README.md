# 测试与转换材料区

本目录集中保存候选/获批试验的源文件、转换产物和逐例检查记录，避免把测试代码放进项目根目录。四例矩阵与检查依据见 [four-case-matrix.md](four-case-matrix.md)。目前已归档一个 uhttpd 上游源快照，供 C01/C02 两个方向候选复用；它超过 700 物理行，只是超限探索候选。C01 有 run-01 智能体文本探索稿与 run-02 配置模型探索稿；run-02 经用户逐例授权完成隔离第三方探索性评估及一次修订，有限输出匹配只属于该修订稿，不是正式 No-RAG 基线。C01/C02 复用同一源，不等于两份独立长例；C03/C04 仍只有场景规格，第二份独立长源尚未选定。当前阶段方案见[最终交付编译质量与 Skill 拓展](../stages/final-output-compile/阶段方案.md)。

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

case 状态使用 `candidate`、`approved-for-trial`、`excluded` 或 `completed`。候选可以存放未验证草稿，但不得称为基线或通过结果。编译与运行须分别核对来源/许可、安全副作用、匹配的隔离环境、评估契约和清理方案并逐例批准；功能比较另须事先冻结行为 oracle。当前编译质量阶段不需要先完成四例功能 oracle 或 RAG 基线。RAG 组若重新启动，仍须在对应 No-RAG 基线冻结后进行。
