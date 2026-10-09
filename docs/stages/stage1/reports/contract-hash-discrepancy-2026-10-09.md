# 契约哈希差异溯源（2026-10-09）

> 性质：**只读**核查。取现役 Controller 已安装的契约文件与候选工作树逐字节比对；
> 未部署、未修改、未提交 job。
> 结论：现役 Controller 的 `/api/health` **报告值与它自己磁盘上的契约文件不符**

## 1. 三个哈希

| 主体 | 报告的 contractSetHash | 来源 |
|---|---|---|
| 现役 Controller | `sha256:56b327067f84fb8a62c4d6feca4dff56533a78883b3404882c9c5d903d6c45ed` | 实时 `GET /api/health` |
| 现役 Linux Agent | `sha256:e088a356b48fd1c3f50e480ac24c2fd03319dc60a49b41de4d076219819c4c45` | 实时 Agent `/health` |
| 候选工作树 | `sha256:f4f58184ff971f0156054983dd23e5189425cc37310b059972d4dde7afaf3274` | 本地按 `contract_manifest.py` 规则重算 |

## 2. 关键实验：从 Controller 磁盘重算

取现役 Controller 已安装目录
`D:\CodeConvertRemote\Stack\Controller\releases\1.0.25-noise.1\contracts\evaluation`
（20 份 `*.schema.json`），按 `contract_manifest.py` 的规则复现：

- 路径：`rglob("*.schema.json")`，按相对路径 POSIX 形式排序；
- 内容：UTF-8 解码后 `\r\n`→`\n`、`\r`→`\n` 归一化；
- 摘要：对每个文件依次 update `relative_path` + `\0` + `canonical_bytes` + `\0`。

**重算结果：`sha256:f4f58184ff971f0156054983dd23e5189425cc37310b059972d4dde7afaf3274`**

即：**Controller 磁盘上的契约集合 = 候选工作树的契约集合**（同一哈希），
**但 Controller 经 `/api/health` 报告的是 `56b32706…`**。

## 3. 逐文件比对

现役 Controller 的 20 份 schema 与候选工作树逐一同名文件比对：

| 结果 | 数量 |
|---|---|
| 归一化后内容完全一致 | **20 / 20** |
| 差异 | 0 |

> **方法学说明**：最初按**原始字节**比对时 20/20 全部"不同" —— 这是伪差异。
> 原因是候选工作树文件为 CRLF，而 `contract_manifest.py` 在哈希前会做 LF 归一化。
> 按归一化口径重比后 20/20 一致。**逐字节比对必须与哈希口径一致，否则会得出相反结论。**

## 4. 由此可确定的结论

1. **现役 Controller 的契约文件与候选工作树完全相同**（`f4f58184…`）。
   因此"候选工作树与现役不一致"这一先前判断**不成立**。
2. **现役 Controller 报告的 `56b32706…` 与其自身磁盘内容不符**。
   这是一个**报告值/计算口径**问题，而非文件内容差异。
3. 因此，三 runner 的 `CONTRACT_MISMATCH` **不能简单归因于"Agent 契约文件旧"** ——
   至少 Controller 侧的报告值本身就需要先解释清楚。

## 5. 可能解释（**未证**，仅列出以指导下一步）

| 假设 | 说明 | 如何验证 |
|---|---|---|
| H1 报告的哈希来自**另一目录** | Controller 进程可能从别的路径（如 `current` 指向的 release、或 `CODECONVERT_*` 环境变量指定的目录）计算 | 查 Controller 进程的 cwd、env、`current` 指向 |
| H2 报告值来自**运行中的旧进程** | 磁盘已更新为 1.0.25-noise.1，但监听 8443 的进程是更早版本启动的 | 比对 PID 3968 的启动时间与 receipt 的 `installedAt` |
| H3 契约集合口径不同 | 现役进程用的 manifest 实现与候选不同（如未做 LF 归一化、或用 `glob` 而非 `rglob`） | 取现役进程实际加载的模块版本 |

**本文不为任何一种假设背书**，尚未取得验证所需信息（进程环境、启动时间、实际加载模块）。

## 6. 附带发现：口径不一致（已在候选源码确认）

| 位置 | 方法 | schema 数 |
|---|---|---|
| `contract_manifest.py:75`（算哈希） | `rglob("*.schema.json")` | 20（含 `governance/`） |
| `evaluation_contracts.py:66`（建校验注册表） | `glob("*.schema.json")` | 17（不含 `governance/`） |

同一代码库内两处对"契约集合"的定义不同。若现役进程用的是某种混合口径，
可能解释 H3。**但这仍是假设，未验证。**

## 7. 对升级决策的影响

用户原计划"升级 Agent 以匹配 Controller"。基于本核查，**该前提需重新确认**：

- 若 H1/H2 成立（报告值来自旧进程或别的目录），则真正需要做的是**让 Controller 以正确路径重载/重启**，
  而不是升级三台 Agent；
- 若 H3 成立，则需要先统一口径，再判断谁与谁不一致；
- 无论哪种，**在解释清 `56b32706…` 的来源之前升级 Agent 都可能白做一轮**。

**建议**：先验证 H1/H2（只读，无副作用），再决定升级范围。

## 8. 本次核查未做

- 未读取 Controller 进程的环境变量、cwd 或启动时间（需更高权限账户；
  当前 `dockeruser` 无法查询服务）。
- 未重启、未部署、未修改任何文件。
- 未取得 Windows/macOS Agent 的契约哈希。
- 未验证 §5 的任何假设。
