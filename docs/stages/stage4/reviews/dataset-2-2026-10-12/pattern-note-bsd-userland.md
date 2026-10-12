# BSD userland 组记录：c-to-cpp 的 *-fs-posix-to-win 三项

## 结论

D2-027 / D2-028 / D2-029 同属 c-to-cpp 的 BSD 组（目录名 `*-fs-posix-to-win`），但**根因与出口各不相同**，三项均逐项预检、逐项定案，**0 模型调用**。

| 项 | 源 | 缺什么 | 性质 | 出口 | 证据 job |
|---|---|---|---|---|---|
| D2-027 | pwd.c | __dead2 | 系统未登记接口（BSD 专有宏） | **SOURCE_NOT_BUILDABLE** | 三次实验 A/B/C |
| D2-028 | realpath.c | __dead2 | 系统未登记接口（BSD 专有宏） | **SOURCE_NOT_BUILDABLE** | eval-20261010-045637-b2605908 |
| D2-029 | stest.c | arg.h | **快照外**项目伴随头（suckless） | **SOURCE_DEPENDENCY_GAP** | eval-20261010-045728-9a8f152a |

## 为什么不能按组套用结论

- D2-027 与 D2-028 缺的是 **FreeBSD sys/cdefs.h 提供的 __dead2 宏**，那是**系统**接口，已登记系统（windows / linux / macos × x64）都没有；
- D2-029 缺的是 **suckless 项目自带的 arg.h**，那是**项目文件**，本应随源码一起提供；
- 两者一个是平台不匹配、一个是快照不完整，**处置与归因完全不同**，混算会污染汇总。

## 关键方法证据：不得凭印象

D2-027 是本批第一次需要做该区分，用了**三次实验**：

1. **实验 A（windows）**：报 err.h 缺失；
2. **实验 B（linux，-std=c11）**：**没有**报 err.h 缺失，证明 err.h 在 linux 上**存在**；同时暴露 getopt / optind 隐式声明，属**契约缺陷**；
3. **实验 C（linux，-std=gnu11 修正契约）**：前两条消失，**只剩 __dead2**，且非命令可补，至此才定案。

**若在实验 A 后凭印象收工，就会把结论建在 err.h 在已登记系统上都不存在这个错误事实上。**
D2-028 沿用先修正契约缺陷再观察的做法（直接用 -std=gnu11），其诊断**全部**由 __dead2 引发，同样未报 err.h 缺失，与实验 B 互相印证。

## 可复用的判据（后续同类项直接沿用）

| 诊断形态 | 性质 | 处置 |
|---|---|---|
| fatal error: 第三方库头 No such file（absl 等） | 快照外文件 | SOURCE_DEPENDENCY_GAP |
| fatal error: 项目伴随头 No such file（arg.h、atoms.h 等） | 快照外文件 | SOURCE_DEPENDENCY_GAP |
| implicit declaration of getopt / optind undeclared（严格 ISO C 下） | **契约缺陷** | 改用 -std=gnu11 或特性宏后**重跑** |
| expected ... before BSD 专有宏（__dead2 等） | 系统未登记接口 | SOURCE_NOT_BUILDABLE |
| err.h 缺失于 windows 但存在 linux | 平台差异 | **必须两个候选都实测**再定案 |

## 对批次汇总的意义

- 三项均计入**接入去向分布**，**不计入转换失败**；
- 三项都**未消耗模型调用**（预检在生成之前拦下），符合不通过即跳过、不投入生成的门禁要求；
- 原始诊断已逐项落盘于各自 job 的 returned-evidence/evidence-source.json。

---

## 追加（2026-10-10）：BSD userland 的**伴随模块缺失**可以有两种完全不同的出口

D2-161（c-to-go，FreeBSD `date.c`）暴露了 \"BSD 源码缺伴随文件\" 这一类里的第二次细分。

| 项 | 源 | 缺什么 | 仓库内是否有可补齐来源 | 出口 |
|---|---|---|---|---|
| D2-029 | stest.c | `arg.h`（suckless 项目伴随头） | **有**（旧 dataset capsule 内含，哈希吻合） | 打包缺口 → **可修复** → 已取得行为证据 |
| D2-025 | driver.c | `atoms.h` 等 4 个伴随文件 | **有**（旧 dataset 内含） | 打包缺口 → **可修复** → 已取得行为证据 |
| **D2-161** | date.c | `vary.h`（FreeBSD date 伴随模块） | **无**（穷举 0 命中） | **SOURCE_DEPENDENCY_GAP** → 不可修复 |

### 判据（在 §9 之外新增的一问）

原 §9 只要求\"先核对旧 dataset 的完整源树\"。本项补充：

**即使确认是伴随文件缺失，还须再问一句：仓库内是否存在可补齐的来源？**

- 若存在且哈希吻合 → 按打包缺口补回，重测，**不**记 SOURCE_DEPENDENCY_GAP（纪律 §9 原意）；
- 若不存在（穷举确认） → 记 **SOURCE_DEPENDENCY_GAP**，**不得补造**伴随头，**不得**删 `#include`，**不得**放宽构建命令。

### D2-161 的穷举证据（三重核对，缺一不可）

1. 旧 dataset 全树搜 `vary.h` / `vary.c` → 0 命中；
2. 全工作区（排除 `node_modules`）搜 `vary.h` / `vary.c` → 0 命中；
3. 全工作区对 `vary_apply` / `vary_append` / `vary_destroy` 做**内容**搜索 → 仅命中本用例自己的两份 `date.c` 副本，**无任何实现**。

### 与 Abseil 组的区别

Abseil 组缺的是**第三方库头**（`absl/...`），本项缺的是**项目自带模块**；两者都归 `SOURCE_DEPENDENCY_GAP`，但**成因不同**，汇总时应能分开说明。

---

## 追加（2026-10-10）：`c-to-go` 的 FreeBSD userland 组六项全部定案

| 项 | 源 | 阻断点 | 出口 | 证据 job |
|---|---|---|---|---|
| D2-161 | date.c | `vary.h`（项目伴随模块，**仓库内不可恢复**） | SOURCE_DEPENDENCY_GAP | eval-20261010-060516-bb95ac01 |
| D2-162 | uname.c | sysctl 接口族 + `osreldate.h` + `__FreeBSD_version` + `__dead2` | SOURCE_NOT_BUILDABLE | eval-20261010-060735-7c22a0a0 |
| D2-163 | wc.c | Capsicum + libxo + libcasper | SOURCE_NOT_BUILDABLE | eval-20261010-061128-01c56a83 |
| D2-164 | ln.c | `__dead2` | SOURCE_NOT_BUILDABLE | eval-20261010-061317-6d426fd7 |
| D2-165 | tr.c | Capsicum（**另有** cmap.h/cset.h/extern.h 缺失） | SOURCE_NOT_BUILDABLE | eval-20261010-061527-afeb6b01 |
| D2-166 | uniq.c | Capsicum | SOURCE_NOT_BUILDABLE | eval-20261010-061656-d33517ea |

**六项同目录、同 BSD 血统，出口却分成两类，且阻断点各不相同。**
**全部 0 模型调用**（预检在生成前拦下）。

### 新增可复用判据

| 诊断形态 | 性质 | 处置 |
|---|---|---|
| `fatal error: sys/capsicum.h` / `capsicum_helpers.h` | FreeBSD Capsicum 子系统 | SOURCE_NOT_BUILDABLE |
| `fatal error: libxo/xo.h` / `libcasper.h` / `casper/cap_fileargs.h` | FreeBSD 专有库 | SOURCE_NOT_BUILDABLE |
| `fatal error: sys/sysctl.h` | FreeBSD 专有头 | SOURCE_NOT_BUILDABLE |
| `error: expected ... before '__dead2'` + 级联 `expected '{'` | BSD 专有宏 | SOURCE_NOT_BUILDABLE |
| `fatal error: <项目伴随头>` 且仓库内**可**找到 | 打包缺口 | 补齐后**重测** |
| `fatal error: <项目伴随头>` 且仓库内**穷举不可**找到 | 快照外文件 | SOURCE_DEPENDENCY_GAP |

### 判定的通用三步（本组六项全部走完）

1. **看诊断**，不凭 `#include` 列表下结论；
2. **清点全文件接口**，确认阻断点是单一头文件还是**整族依赖**；
3. **查条件编译**：若只有 `#ifndef lint` / `#if 0` 之类版权守卫，则**不存在**平台回退分支，任何构建命令改动都无效 ⇒ 才可定 SOURCE_NOT_BUILDABLE。

### 反面纪律

- **不**用 `-D__dead2=` 之类的伪造宏绕过；
- **不**补造 capsicum / libxo / sysctl 桩；
- **不**删 `#include` 或改写调用；
- **不**把"缺伴随文件"与"缺系统接口"混算为同一个出口。
