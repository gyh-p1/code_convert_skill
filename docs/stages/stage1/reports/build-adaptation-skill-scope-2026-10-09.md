# 构建适配能否由 Skill 承担？—— C8–C10 归属分析

> 日期：2026-10-09
> 性质：**归属分析**（静态阅读 skills/ 与 references/，只读）
> 问题（用户提出）：C8–C10 这些构建适配问题，能不能通过优化 Skill 完成？
> 结论：**能承担大部分，但不能全部**。三项应拆开处理，其中一项需要 Skill + 参考页，两项需要平台代码。

## 1. 先看现有 Skill 已经覆盖了什么

关键是：**知识其实已经写好了，只是没接到构建环节**。

`skills/systems/posix-winsock/SKILL.md` 第 43 行（核心差异映射表）**已经明确写着**：

| 主题 | POSIX/Linux | Windows/Winsock | 转换必须处理的点 |
|---|---|---|---|
| 头文件/链接 | `<sys/socket.h>`… | `<winsock2.h>`、`<ws2tcpip.h>`；**链接 `ws2_32.lib`**；须在 `<windows.h>` 前包含 | 包含顺序错误会与旧 `winsock.h` 冲突 |

即 **C8（Winsock 链接）的知识已经存在**。问题不在于"没写规则"，
而在于**构建命令是由平台 `buildCommand` 决定的，Skill 影响不到它**。

同时，`references/adapter/controller/runner-capability-matrix.md` §1.2 **已完整记录 P1 的修复证据**：

- 缺陷：`failed to initialize build cache at /home/d9lab/.cache/go-build: mkdir /home/d9lab: permission denied`
- 热修：提交 `8d4da68` 把 `HOME`/`XDG_CACHE_HOME`/`GOCACHE` 指向 `/var/lib/codeconvert-agent`
- 验证：无害作业 `eval-20261005-115047-f2cdbaec` **不使用 `GOCACHE` 前缀**即通过，R12 快照已生效

**因此 P1 应判定为"已修复并有取证"**，我此前列为"需核对"是保守过头。

## 2. 为什么 Skill 无法单独承担全部三项

Skill 的作用边界（由 `SKILL.md` 与安全边界共同决定）：

| Skill 能做 | Skill 不能做 |
|---|---|
| 影响**源码内容**（模型生成目标代码时遵守规则） | 影响**平台执行逻辑**（Agent 里的硬编码行为） |
| 决定**冻结契约里写什么**（含构建命令） | 改变已安装平台上运行的代码 |
| 提示**自审应检查什么** | 自动生成 Skill 未声明的文件 |

证据：`apps/vm-agent/vm_agent/app/main.py:199`

```python
build_command = manifest.get("buildCommand")
```

Agent **直接取 manifest 的 `buildCommand`**，自身不做任何按语言/平台的适配。

### 2.1 关键发现：`buildCommand` 是**契约字段**（决定 C8 可走 Skill）

`packages/evaluation-contracts/agent-run-request-1.1.schema.json` 中：

```json
"properties": {
  "buildCommand": { "$ref": "#/$defs/command" },
  "runCommand":   { "$ref": "#/$defs/command" },
  ...
}
```

**`buildCommand` 由提交方通过契约提供**。这意味着：

> **在 Skill 中规定"转换为 Windows/Winsock 时构建命令必须含 `ws2_32`"，
> 只要该规定落到冻结契约的构建命令里，就真的会被执行 —— 不需要改平台代码。**

这把 C8 从"平台功能缺口"重新归类为**可由 Skill + 契约解决**。

### 2.2 但 C9/C10 不同

- **C9**：补 `.csproj` 是**写文件**动作。契约里没有"生成工程文件"字段，
  Agent 也不会自动生成 —— 必须由 Agent 代码实现。
- **C10**：`GOCACHE` 属**运行环境**，不是 `buildCommand` 能表达的
  （虽然 batch-01 是把它拼进命令前缀临时绕过的）。
  版本策略可写进 Skill，但"结构化报错"属平台行为。

对照 batch-01 的两条事件，它们当时都是**人工改 job**：

```json
{"event":"BUILD_COMMAND_CORRECTED","taskId":"B07","reason":"source uses Winsock; added -lws2_32 link library"}
{"event":"ENV_WORKAROUND_RETRY","taskId":"B20","reason":"...retry same capsule with GOCACHE=/tmp/gocache"}
```

第一条**本来就应该由契约携带**，而不是事后人工补 —— 这是流程缺口，不是能力缺口。

## 3. 三项的归属判定

| 项 | 内容 | Skill 可承担 | 还需什么 | 建议归属 |
|---|---|---|---|---|
| **C8** | Winsock 补链 `-lws2_32` | **知识已有**（posix-winsock §核心映射表） | 需在**冻结契约**里按源特征声明链接库；或平台按特征自动补 | **Skill 侧可完成**（强化"构建前提"条款） |
| **C9** | C# `.csproj` 中性工程 | 可规定**何时补、补什么、如何留证** | Agent 需真的生成文件；且"中性"标准要可验证 | **Skill + Agent 代码**（缺一不可） |
| **C10** | Go 工具链/缓存 | P1 缓存**已修复**；工具链版本策略可写规则 | 平台需给出**结构化** `BLOCKED_ENV` 而非下载失败 | **Skill 定策略 + 平台做报错** |

## 4. 分项结论

### 4.1 C8：Skill 侧即可解决（推荐先做）

现有 `posix-winsock` Skill 已列出 `ws2_32.lib`，但**没有说"这属于构建前提，必须写进冻结契约/构建命令"**。
缺的是**把知识接到契约**的一步。

**建议改法**：在 `posix-winsock` 与相关方向 Skill 中增补一节
"**构建前提（链接与头文件顺序）**"，明确：

- 转换为 Windows/Winsock 后，**构建命令必须含 `ws2_32`**，否则链接失败；
- 头文件顺序要求（`winsock2.h` 必须在 `windows.h` 前）；
- 该前提应写入**冻结契约的构建前提字段**，不依赖每次人工发现。

这**不需要改平台代码**。

### 4.2 C9：Skill 能定规则，但必须有代码执行

`.csproj` 的问题在于：**补工程文件是"写文件"动作**，Skill 只能告诉 Agent"该补、补什么、要留证"，
真正生成仍需 Agent 执行。而 `AGENT_ADDED_CSPROJ` 出现 17 次，说明**当时是靠人手工补的**。

**风险（报告 §6#3 自己指出）**："C# 源/目标缺 `.csproj` 会掩盖真实缺失类型"。
所以 Skill 必须同时规定：

- 补齐工程文件时**必须记录原本缺什么**（否则掩盖真实缺口）；
- "最小中性"的判定标准（不引入源中不存在的依赖/类型）。

**建议**：Skill 增补规则 + 视需要由 Agent 实现生成。**若本次不改平台**，至少要让规则可执行、
且**强制留证**，避免下一位操作者把它当"环境已修好"。

### 4.3 C10：缓存部分已修复，工具链部分应写规则

- **P1（Linux Go 缓存）**：按 `runner-capability-matrix.md` §1.2，**已有修复与取证**（R12 + 无害作业验证）。
  我此前判为"需核对"过于保守，应更正为**已修复**。
- **C10（`go 1.27` vs runner `1.26.4`）**：这是**版本策略**问题，适合写进 Skill：
  基线与 runner 实际工具链不一致时应如何处理（明确报 `BLOCKED_ENV`，不静默降级）。
  但"给出结构化报错"属平台行为。

## 5. 给用户的建议

| 项 | 建议 |
|---|---|
| **C8** | **纳入本次，且落在 Skill + 契约**（非平台代码）：`buildCommand` 本就是契约字段，实测可执行 |
| **C9** | **Skill 规则先写**（含强制留证记录"原本缺什么"）；是否让 Agent 自动生成由你决定 |
| **C10** | Skill 写**工具链版本策略**；缓存项**标记为已修复**（附取证），不重复投入 |
| **P1** | **更正为已修复**（R12 快照 + 无害作业 `eval-20261005-115047-f2cdbaec` 不使用 `GOCACHE` 前缀即通过） |

### 5.1 对 C8 的具体建议（最小改动）

在 `skills/systems/posix-winsock/SKILL.md` 增补一节，例如"**构建前提（链接与头文件顺序）**"：

- 目标为 Windows/Winsock 时，**构建命令必须链接 `ws2_32`**，否则链接阶段失败；
- 头文件顺序：`winsock2.h` 必须在 `windows.h` **之前**；
- 该前提**必须写入冻结契约的构建命令**，不依赖每次人工发现；
- 若源未声明链接库而目标需要，须在契约中显式补齐并记录来源。

这样"知识"才真正接到"执行"。**是否要我实施这一改动，请指示。**

## 6. 本次分析未做

- 未修改任何 Skill 或参考文件（本文只是归属分析）。
- 未逐一核对 42 份方向 Skill 是否都已含构建前提说明（仅抽查 `posix-winsock`）。
- 未验证 C9 若由 Agent 实现，其"最小中性"判定标准如何自动保证。
- 未验证 P1 之外（Windows/macOS）的缓存路径现状。
