# 测试与转换材料区

本目录把**已产生转换 run 的数据集**、**未验证候选**和**可复用源快照**分开。逐例结果与证据入口见[按转换方向归档的数据集](dataset/README.md)。原固定四例测试已[取消](../stages/four-case-cancellation.md)，C01 的探索证据仅作为历史 run 保留。

```text
docs/test/
├── dataset/
│   ├── c-to-cpp/<case-id>/   # C → C++ 的完整 case/run/evidence
│   ├── c-to-go/<case-id>/    # C → Go 的完整 case/run/evidence
│   └── legacy-candidates.md # 外部旧用例的只读初筛，不复制源码
├── candidates/<candidate-id>/ # 尚未完成来源/授权/评估的候选
└── sources/<source-id>/       # 被已有 run 引用的共享上游源快照
```

源文件保留原名；目标代码为 `target.<ext>`，结果为 `result.md`，多轮使用 `run-01/` 等目录。同一上游源可由多个 case 引用，不复制后分别修改。归档按语言方向组织，**编译证据、功能证据和环境故障分栏**；未取得目标 build 的 run 仍可保存，但不得算编译通过。

当前有 C01 历史探索、fe 与四份 POSIX→Windows 文件系统案例，以及受 same-runner 基础设施故障阻断的 RC4 C→Go 案例。多数并非真实攻防链，不能据这些偏保守样例推断实用场景效果。现有共享快照与对应消费者见[源索引](sources/README.md)，未验证资料见[候选区](candidates/README.md)。以后从真实攻防源码选样时，先审上游身份/许可、原件与改写差异、实际行为、隔离副作用及可观察义务；旧目录战术标签只是线索，见[旧用例候选索引](dataset/legacy-candidates.md)和[功能判据草案](../stages/final-output-compile/functional-detection-criteria.md)。

转换与动态评估的安全边界仍按[项目安全边界](../安全边界.md)。本机不编译或运行测试样本、转换产物及构建脚本；Controller 回传前不写编译/功能通过。原始请求、capsule、第三方证据作为历史快照保留，迁移只修活动入口与引用。
