# 远端 Controller 适配与连接

> 文档类型：外部评估基础设施的连接与提交适配（reference）
> 状态：ACTIVE（本项目对接已授权隔离第三方 VM Controller 的唯一连接说明）
> 更新：2026-09-28
> 首次验证：fe run-01 双侧 build，jobId `eval-20260928-033750-71724720`，`COMPLETED`（本会话直连 HTTP 8443 提交并回传真实证据）

本项目**不建设**运行时或评测平台；编译/运行证据一律由已授权的隔离第三方 VM Controller 返回。本文只记录**如何连接该 Controller、如何组装并提交 comparison capsule、如何回传证据**，供转换 Agent 在评估步骤直接复用。凭据不入库（见“安全边界”）。

## 拓扑与连接坐标

| 角色 | 地址 | 说明 |
|---|---|---|
| Controller（FastAPI HTTP API） | `http://192.168.101.250:8443` | 接收 job、编排 VM Agent、回传证据 |
| 本机（开发/提交端） | `192.168.101.105` | 与 Controller 同 `/24` 段，**可直达 8443**，无需 SSH 隧道 |
| Windows VM Agent | `http://192.168.195.128:9000` | VM `windows-eval`，支持 c/cpp/python/powershell/go/dotnet |
| Linux VM Agent | `http://192.168.195.129:9000` | VM `linux-eval`（按需启用） |

- **首选：直连 HTTP 8443**。本机与 Controller 同网段时，所有 `POST /api/jobs`、轮询、取证据均直接走 HTTP。
- **回退：SSH 端口转发**。若本机不在同段（无法直达 8443），用 `ssh -L 8443:127.0.0.1:8443 Administrator@192.168.101.250` 建隧道后按同样契约连本地 `http://127.0.0.1:8443`。SSH 私钥只在操作者本机 `~/.ssh`，永不入库/入 zip/入 VM 配置/入日志。
- **恒就绪政策**：远端 Controller/隔离 VM 恒就绪且已授权；到评估步骤直接提交执行，不逐次确认可达性、不询问是否评估。仅当 Controller 真实返回基础设施/环境故障（`INFRA_ERROR`）才记环境失败并在恢复后重提，任何情况不改用本机编译或在边界外运行样本。

## API 契约

| 方法 | 路径 | 作用 |
|---|---|---|
| `POST` | `/api/jobs` | multipart 提交 job：`file=<capsule.zip>`、`caseId`、`targetOs`、`targetLang`。返回 `202 {jobId, jobStatus:"QUEUED"}` |
| `GET` | `/api/jobs/{jobId}` | 轮询状态，直到终态：`COMPLETED` / `FAILED_COMPILE` / `FAILED_RUNTIME` / `TIMEOUT` / `INFRA_ERROR` |
| `GET` | `/api/jobs/{jobId}/report` | 结构化评估报告（schema 3.0 JSON） |
| `GET` | `/api/jobs/{jobId}/report.md` | 人读报告 |
| `GET` | `/api/jobs/{jobId}/evidence/source` | 源侧 evidence bundle（build/execution） |
| `GET` | `/api/jobs/{jobId}/evidence/target` | 目标侧 evidence bundle（build/execution） |
| `GET` | `/api/jobs/{jobId}/comparison` | 双侧比较结果 |
| `GET` | `/api/jobs/{jobId}/logs` | Controller 编排日志 |

## comparison capsule 组装

capsule 是提交给 Controller 的 zip，根部必须含以下文件（Controller 会校验必需文件齐全、source/target 树非空、无符号链接/不安全路径）：

```
capsule.zip
├── comparison_manifest.json   # kind=codeconvert-comparison-manifest, schemaVersion "1.0"
├── input_profile.json         # 校验于 input-profile.schema.json（argv/stdin/observationPolicy/comparisonPolicy/timeout/workingDirectory）
├── metadata.json
├── source/                    # 源侧：源文件 + 依赖头 + run_case.py（非空）
│   └── ...
└── target/                    # 目标侧：目标文件 + 依赖头 + run_case.py（非空）
    └── ...
```

- **`comparison_manifest.json`** 关键字段（Controller `validate_comparison_identity` 逐项校验）：`caseId`（与 POST 表单 `caseId` 一致）、`source`/`target` 各自的 `os`、`arch`、`artifactLanguage`、`runCommand`、`buildCommand`。双侧 os/arch/language 必须能被 `resolve_runner_assignments` 匹配到 READY 的 runner。
- **`input_profile.json`** 通过 `validate_evaluation_contract` 校验：`argv`、`stdin`、`observationPolicy.dimensions`（如 `["output"]`）、`comparisonPolicy`（如 `output.stdoutMode="json-structural"`）、`timeoutSeconds`、`workingDirectory`。
- **`run_case.py`**（两侧各一份）：无害 liveness 驱动——定位构建出的 `program.exe`/`program`，`subprocess.run(stdin=DEVNULL, timeout=…)`，打印 JSON（`exitCode`/`stdoutLen`/`stderrLen`）。不联网、不调外部命令、不读敏感文件。
- 源无可运行入口（库翻译单元无 `main`）时，默认按冻结记录补写最小入口/驱动（fe 用形态 B：`-DFE_STANDALONE` 编入 REPL `main`），并在 `frozen-inputs.md` 标注补写内容。
- 组装临时目录里**不要**留 `__pycache__`/`*.pyc`；打包前清理，避免污染 zip 与 git。

fe run-01 的实样落于 `docs/test/cases/fe-lisp-c-to-cpp/output/no-rag/run-01/04-evaluation/job-01-dual-build/`，回传证据落于其 `returned-evidence/`，可作组装与回填模板。

## 提交—轮询—取证流程（本会话实测）

PowerShell 5.1 无 `Invoke-RestMethod -Form`；用 `curl.exe -F` 做 multipart。以下为已跑通的形态（占位处按实际替换）：

```powershell
# 1) 打包（先清 __pycache__）
Compress-Archive -Path source,target,comparison_manifest.json,input_profile.json,metadata.json -DestinationPath capsule.zip -Force

# 2) 提交 → 202 {jobId, jobStatus}
curl.exe -sS -X POST "http://192.168.101.250:8443/api/jobs" `
  -F "file=@capsule.zip;type=application/zip" `
  -F "caseId=fe-lisp-c-to-cpp-run-01" `
  -F "targetOs=windows" `
  -F "targetLang=cpp"

# 3) 轮询到终态
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>"

# 4) 取证据（分别保存到 returned-evidence/）
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/report"          # evaluation_report.json
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/report.md"       # evaluation_report.md
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/evidence/source" # evidence-source.json
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/evidence/target" # evidence-target.json
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/comparison"      # comparison.json
curl.exe -sS "http://192.168.101.250:8443/api/jobs/<jobId>/logs"            # controller.log
```

## 回传证据布局与结论回填规则

- 全部真实回传落于该 run 的 `04-evaluation/<job-dir>/returned-evidence/`（`job-id.txt`、`state.json`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`、`comparison.json`、`controller.log`）。
- **结论只从真实回传证据回填**，不得伪造：
  - `syntaxVerdict`：仅据**目标侧** evidence bundle 的 `build.status=completed` 且 `exitCode=0` 判 `PASS`；非零/`failed` 判 `FAIL`。源侧 build 作对照基线，用于区分“源本身编不过”与“转换引入”。
  - `thirdPartyCompileStatus`：`THIRD-PARTY-COMPILE-PASSED` / `FAILED_COMPILE` / 未提交时 `AWAITING-THIRD-PARTY-COMPILE`。
  - `executionApproved`：仅在**实际提交并回传证据后**置 `true`。
  - `behaviorVerdict`：Controller `comparison` 的结果仅作**信息记录**；本编译质量阶段不计入功能率、不设行为 oracle、不外推等价。
- 模型自审 `NO-REPAIR-IDENTIFIED` 只是提交门槛，**绝非语法结论**（C01 先例：自审通过仍被 MinGW 定位到 `min` 未声明）。

## 安全边界

- **凭据永不入库**：API 密钥（仅 `.env` 模型凭证）、SSH 私钥、VMware 密码一律不写入任何文件、zip、VM 配置、报告、日志或聊天。
- SSH 私钥只留操作者本机 `~/.ssh`；加密 VM 的 VMware 口令只经远端 host 环境变量 `CODECONVERT_VMWARE_PASSWORD` 提供，不入 YAML/job 输入/报告/源码控制/聊天。
- 提交的 capsule 不含 `.env`、不含任何密钥；`run_case.py` 无联网、无外部命令、不读敏感文件。
- 隔离运行：网络固定 loopback/实验网，不打真实外部目标、不用真实凭证、不通过转换新增攻击能力；VM 可回滚快照兜底，结束即销毁临时件。
- 本机不编译、不运行源/目标/构建脚本；一切编译与运行由 Controller + VM Agent 执行并回传证据。
