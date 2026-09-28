# step-01：头文件 / 宏可用性规则（c-to-cpp）

> 状态：方案待确认
> 类型：Skill 内容增补（不需要编译能力，用 C01 已有证据）
> 归属阶段：[最终交付编译质量与 Skill 拓展](index.md)

## 目标

把 C01 已记录的一条可归因失败落成 c-to-cpp 的一条有依据规则：模型自评给出 `NO-REPAIR-IDENTIFIED`，但第三方 MinGW/UCRT64 `g++ -std=c++17` 后来定位到 `min` 未声明（见 [conversion-evaluation-loop §4](../../../references/workflow/conversion-evaluation-loop.md)）。这属于“头文件/宏可用性”缺口：C 侧隐式可见的名字，到 C++ 侧需要显式包含或改写。

## 纳入范围

- C 经 `<sys/param.h>` 等间接获得的 `min` / `max` **宏**，在 C++ 侧要显式 `<algorithm>` + `std::min` / `std::max`。
- 宏 `min` / `max` 的重复求值与副作用问题（`min(a++, b)`），说明改 `std::min` 后求值语义的差异与边界。
- 与 `<windows.h>` 的 `min` / `max` 宏冲突及 `NOMINMAX` 的取舍（跨 OS 目标时）。
- 归纳“C 隐式可见、C++ 需显式包含/限定”的头依赖模式作为触发提示，而非逐一穷举头文件。

每条规则写明：触发条件、版本/平台前提、映射边界、反例、依据。

## 非目标

- 不堆砌尚无证据支持的其他宏/头类别。
- 不改行为语义，不把规则写成“语法通过”声明。
- 不与现有 `SKILL.md`“宏与回调”行、`references/type-abi.md` 内容重复；先核对落点。

## 依赖与前置

- 无外部依赖；证据已在库内（C01 记录 + 语言标准）。
- 落点二选一或新建：优先在 `skills/directions/c-to-cpp/SKILL.md` 增一条“头文件/宏可用性”专题指引（表行或小节）；内容超出 type-abi 主题时新建 `skills/directions/c-to-cpp/references/header-macro.md` 小专题并从 SKILL 链接。

## 预计改动文件

- `skills/directions/c-to-cpp/SKILL.md`（新增专题入口/规则）。
- 可能新增 `skills/directions/c-to-cpp/references/header-macro.md`（若单列更清晰）。
- 依据链接指向语言标准（open-std）与 C01 记录，不新增指向 `docs/` 的运行时链接。

## 验收依据（人工检查，不需编译）

- 规则含触发/前提/边界/反例/依据五要素。
- 入口与链接一致；产品树（`skills/`、根 `SKILL.md`）不出现指向 `docs/` 的链接。
- 与安全边界、诚实边界一致；不宣称转换结果正确。
- 证据仅 C01 单例时，明确标注“依据 C01 单例 + 语言标准”，不外推为普遍通过率。

## 风险与停止条件

- 若复核发现该 `min` 失败其实是工具链噪音而非可归因转换缺陷，停止并回到方案。
- 只写有依据的规则；无把握的类别记为待补，不凑数。
