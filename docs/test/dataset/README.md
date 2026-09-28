# 转换数据集

这里按**源语言 → 目标语言**归档已有转换 run。数据集是本项目的导航和逐例证据记录，不是训练集、正式准确率基线或新评测框架。共享源快照见[源索引](../sources/README.md)；未验证的长文件结构材料见[候选区](../candidates/long-file-structure-candidate/case.md)。原固定四例任务已[取消](../../stages/four-case-cancellation.md)，C01 只保留历史探索身份。

| 方向 | 当前 case | 已取得的目标编译证据 | 入口 |
|---|---:|---|---|
| C → C++ | 6 | fe、stest、realpath、pwd 在各自声明的工具链下 PASS；C01 仅探索工具链 PASS；du 目标未构建 | [C → C++](c-to-cpp/README.md) |
| C → Go | 1 | RC4 因 Controller same-runner 环境故障未构建 | [C → Go](c-to-go/README.md) |

**状态分层**：`编译 PASS` 只认对应最终交付文件的第三方目标 build；`探索工具链 PASS` 不等于正式目标工具链验收；`INCONCLUSIVE`、源基线阻断和环境故障不计作目标通过或失败。功能结果另列，未观测写 `UNVERIFIED`。不能把这几个不同任务、模型/Skill 版本和工具链条件混算成总体准确率。

## 目录与迁移

```text
docs/test/
├── dataset/
│   ├── c-to-cpp/<case-id>/
│   └── c-to-go/<case-id>/
├── candidates/<id>/          # 尚未形成可归档转换 run 的候选材料
└── sources/<source-id>/      # 上游源快照和来源/许可
```

2026-09-28 按用户选择把七个已有转换 case 的完整目录从当时的 `cases/<case-id>/` 移到 `dataset/<方向>/<case-id>/`，case/run/job 身份及原始源码、目标代码、请求响应、第三方证据和 capsule 字节不因移动改变。活动 Markdown 链接和移交清单改为新路径；冻结请求、原始第三方回传和 capsule 内出现的旧路径仍是**当时的历史路径**，不要将其误认为新增的一份测试。旧路径映射见[step-05 记录](../../stages/final-output-compile/step-05-dataset-and-realistic-cases.md)。

## 下一轮样例

当前样例以语法/编译探索和较保守的文件系统行为为主，尚不足以代表真实攻防使用效果。下一轮优先从可追溯的真实攻防源码中选择场景，逐例记录上游身份、许可、原件/改写、真实行为和隔离可观测性。用户提供的旧资料先列[候选索引](legacy-candidates.md)，不直接继承其“已验证”标签。功能检测的前置判据见[设计草案](../../stages/final-output-compile/functional-detection-criteria.md)。
