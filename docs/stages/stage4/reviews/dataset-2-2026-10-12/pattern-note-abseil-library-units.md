# 批次形态观察：Abseil 库翻译单元簇（7 项，2026-10-10 全部由诊断定案）

## 结论

dataset-2 中共 **7 个 .cc 源文件**，全部是 **Abseil 库的翻译单元**（无 main、依赖未随附的 absl 头）。
七项**全部**经源侧构建预检的编译器诊断定案为 **SOURCE_DEPENDENCY_GAP**，均**未消耗模型调用**。

## 逐项证据（每项一条独立诊断）

| taskId | direction | 源文件 | 预检 jobId | 编译器诊断（原文） |
|---|---|---|---|---|
| D2-079 | cpp-to-csharp | ascii.cc | eval-20261010-044920-7f22e2a1 | ascii.cc:15:10: fatal error: absl/strings/ascii.h: No such file or directory |
| D2-080 | cpp-to-csharp | charconv_bigint.cc | eval-20261010-045012-f4b36f9c | charconv_bigint.cc:15:10: fatal error: absl/strings/internal/charconv_bigint.h: No such file or directory |
| D2-081 | cpp-to-csharp | str_cat.cc | eval-20261010-045044-69d4aa97 | str_cat.cc:15:10: fatal error: absl/strings/str_cat.h: No such file or directory |
| D2-084 | cpp-to-go | civil_time.cc | eval-20261010-044524-5c79cce5 | civil_time.cc:15:10: fatal error: absl/time/civil_time.h: No such file or directory |
| D2-085 | cpp-to-go | match.cc | eval-20261010-044645-915b7c73 | match.cc:15:10: fatal error: absl/strings/match.h: No such file or directory |
| D2-086 | cpp-to-go | str_split.cc | eval-20261010-044725-7e182d07 | str_split.cc:15:10: fatal error: absl/strings/str_split.h: No such file or directory |
| D2-087 | cpp-to-go | substitute.cc | eval-20261010-044842-5db6bbba | substitute.cc:15:10: fatal error: absl/strings/substitute.h: No such file or directory |

## 判据（未凭印象）

- **不是**缺少目标系统接口（absl 是第三方库头，不是系统接口）-> 不是 SOURCE_NOT_BUILDABLE；
- **不是**命令或契约缺陷（不是缺链接库或分支宏）-> 不修正命令重跑；
- **是**引用了快照外的文件 -> SOURCE_DEPENDENCY_GAP。

每项都单独跑了预检、单独取了诊断；**没有**因为同族就跳过验证。

## 处置纪律（后续同类项直接沿用）

1. 跳过，**不补造桩**（不得伪造 absl 头、不得下载 Abseil、不得删 include）；
2. **不消耗模型调用**；
3. **不记为目标转换失败**，与 SOURCE_NOT_BUILDABLE 分列；
4. 目标侧结论一律 **UNVERIFIED**。

## 对数据集口径的影响

- 这**不影响** dataset-2 清单的自足性：README 明确本目录只声明源码存在与契约字段齐全，**不**声明可编译或可运行。
- 但它确实说明：**NEW 项中存在一部分库翻译单元形态**，它们在转换评估阶段会稳定地落到 SOURCE_DEPENDENCY_GAP。
- 该比例应计入批次汇总的**接入去向分布**，**不得**计入转换失败，也**不得**从交付基线里抹掉。
