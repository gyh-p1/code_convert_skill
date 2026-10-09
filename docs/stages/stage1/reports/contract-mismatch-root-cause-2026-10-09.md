# CONTRACT_MISMATCH 根因定论（2026-10-09）

> 性质：**只读**核查。经 SSH 读取现役 Controller 磁盘与 API；未部署、未修改、未重启、未提交 job。
> 结论：现役 Controller 报告的契约哈希 `56b32706…` **在整台机器的磁盘上不存在**；
> 并且**回执声明的版本与进程实际运行的版本不是同一个目录**。

## 1. 决定性证据：逐版本契约哈希

对 Controller `releases\` 下**每一个已安装版本**，按其自身
`contracts\evaluation\*.schema.json`（递归、LF 归一化、NUL 分隔，复现 `contract_manifest.py`）重算：

| release | schema 数 | 重算出的 contractSetHash |
|---|---:|---|
| 1.0.7 | 15 | `11827caafd445033b8b38d8f111887c30a3b3c6a558c87cab4af84642003c0d0` |
| 1.0.12 | 15 | `11827caa…`（同上） |
| 1.0.13 | 15 | `11827caa…` |
| 1.0.14 | 15 | `11827caa…` |
| 1.0.18 | 15 | `11827caa…` |
| 1.0.19 | 20 | `18b47218fd18b5f014f12f1c3f73fd0a0e6107e6f75fa3c1cef72695f0a02d04` |
| 1.0.20 | 20 | `18b47218…`（同上） |
| 1.0.23 | 20 | `f4f58184ff971f0156054983dd23e5189425cc37310b059972d4dde7afaf3274` |
| 1.0.24 | 20 | `f4f58184…`（同上） |
| **1.0.25** | **32** | `281d356536db7a837bb2068f0a9e435fb3b5a03eb3035bdf056f774c81e1da15` |
| **1.0.25-noise.1** | **20** | `f4f58184…` |

**现役 `/api/health` 报告的是 `56b327067f84fb8a62c4d6feca4dff56533a78883b3404882c9c5d903d6c45ed`**，
**与上表任何一个都不相等。**

进一步：在 Controller 的 `releases` 目录下对 `*.json`/`*.py` 全文检索字符串 `56b32706`，
**零命中**。即该哈希**不是**由磁盘上任何已安装版本的文件集合算出的。

## 2. 第二个独立缺陷：回执版本 ≠ 运行版本

`start-controller.ps1`（现役启动脚本）内容节选：

```powershell
$env:REMOTE_HOST_CONTROLLER_CONFIG = 'D:\CodeConvertRemote\Stack\Controller\config\controller.yaml'
Set-Location -LiteralPath 'D:\CodeConvertRemote\Stack\Controller\releases\1.0.25'
& 'D:\CodeConvertRemote\Stack\Controller\releases\1.0.25\runtime\python.exe' -m remote_host_controller.serve
```

**它运行的是 `releases\1.0.25`**，而 `install-receipt.json` /
`.codeconvert-deployment.json` 声明的 releaseVersion 是 **`1.0.25-noise.1`**，
`installedAt` 为 `2026-10-09T03:10:14Z`。

两者是**不同目录、不同契约集合**：

| | 1.0.25 | 1.0.25-noise.1 |
|---|---:|---:|
| schema 数（递归） | **32** | 20 |
| 含 `agent-capabilities`、`evaluation-permit`、`execution-attestation`、`safety-plan` 等 | **是** | 否 |
| 契约哈希 | `281d3565…` | `f4f58184…` |

同时该目录下存在 `start-controller.ps1.bak-20261009132323` 与
`config\controller.yaml.bak-20261009132323` —— 说明 **2026-10-09 13:23 有一次启动配置改动**，
晚于 receipt 的 03:10。这解释了"回执说 noise.1、实际跑 1.0.25"的时间线。

## 3. 因此原先的升级计划前提不成立

用户原计划：**升级三台 Agent 以匹配 Controller 的 `56b32706…`**。

但本核查表明：

1. `56b32706…` **不对应磁盘上任何发布**，因此"匹配它"**无法通过安装任何现有 Agent 包达成**；
2. Controller 实际**运行**的是 `1.0.25`（32 schema，`281d3565…`），
   而非回执声明的 `1.0.25-noise.1`（20 schema，`f4f58184…`）；
3. 因此**先要确定 Controller 到底应该跑哪一版**，才谈得上让 Agent 去匹配。

**在解释清 `56b32706…` 的来源之前，升级 Agent 有很高概率是白做一轮。**

## 4. 尚未解释的问题（需进一步取证）

| # | 问题 | 需要的证据 |
|---|---|---|
| Q1 | `56b32706…` 从哪来？ | 运行进程（PID 3968）的实际 cwd、环境变量、加载的模块路径 |
| Q2 | 为何 `start-controller.ps1` 指向 `1.0.25` 而非 `1.0.25-noise.1`？ | 13:23 那次改动的原因与操作者记录 |
| Q3 | `1.0.25` 是否就是"最新适配"？ | 用户确认目标版本 |
| Q4 | 三台 Agent 各自跑的是哪一版？ | 各 Agent receipt 与 `/health`（Windows/macOS 尚未取得） |

**当前 `dockeruser` 账户无法读取 PID 3968 的 `StartTime`/`Path`（返回 Null），
也不能查询服务**，因此 Q1 无法用现有凭据回答。

## 5. 建议的下一步（按优先级）

1. **用有管理员权限的账户**读取 PID 3968 的命令行、cwd 与环境变量，
   定位 `56b32706…` 的来源（Q1）。这是唯一的"硬阻塞"。
2. 确认**目标发布版本**（Q3）：是 `1.0.25`（32 schema，功能更全）还是 `1.0.25-noise.1`（20 schema，消噪试用）。
   注意 `1.0.25` 的 schema 集**明显更全**（含 permit/attestation/profile 等），
   但本文件**不据此推荐**，需用户判断哪个才是"最新适配"。
3. 在目标版本确定后，再统一 Controller 与三台 Agent 到同一版本（Q4）。

## 6. 本次核查未做

- 未部署、未回滚、未重启、未修改任何远端文件或配置。
- 未提交 job；只读 `GET /api/health`（与早先的 `GET /api/runners`）。
- 未读取运行进程的环境变量（权限不足）。
- 未取得 Windows/macOS Agent 的版本与契约哈希。
- 本文件**不对** `56b32706…` 的成因下结论，只给出可验证的事实与假设清单。
