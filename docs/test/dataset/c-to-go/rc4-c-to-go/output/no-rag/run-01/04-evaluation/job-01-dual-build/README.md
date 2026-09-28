# job-01-dual-build — rc4 C→Go same-OS 双侧 build capsule 与真实回传

## capsule 组成（9 entries，sha256 `b48b136b…`）

- `comparison_manifest.json`（kind=codeconvert-comparison-manifest, schemaVersion 1.0）
- `input_profile.json`（argv `["4b6579","bbf316e8d940af0ad3"]`, dimensions `["output"]`, timeout 30）
- `metadata.json`
- `source/`：`WjCryptLib_Rc4.c`、`WjCryptLib_Rc4.h`、`rc4_decrypt_cli.c`、`run_case.py`
- `target/`：`target.go`、`run_case.py`
- 无 `__pycache__`/`.pyc`/符号链接；不含 `.env`/任何密钥。

## 提交与真实回传（两次，均 INFRA_ERROR）

| # | jobId | 终态 | 证据落点 |
|---|---|---|---|
| 首次 | `eval-20260928-092052-390487e9` | `INFRA_ERROR` | [`returned-evidence/`](returned-evidence/) |
| 重试 | `eval-20260928-092721-a2e2311f` | `INFRA_ERROR` | [`returned-evidence/retry-02/`](returned-evidence/retry-02/) |

- 提交：`curl.exe -F "file=@capsule.zip;type=application/zip" -F caseId=rc4-c-to-go-run-01 -F targetOs=windows -F targetLang=go http://192.168.101.250:8443/api/jobs` → 202 QUEUED；轮询至终态。
- 终态 failure（两次一致）：`type=AGENT_UNAVAILABLE`，`category=environment`，`retryable=false`，reason=`agent /run failed: INVALID_PACKAGE: baselineReference artifactHash does not match uploaded artifact`。
- `executionStrategy=same-runner`，`runnerAssignments={source,target}=windows-vm-agent-x64`。
- 源侧 `execution.performed=true` 但 `evidenceBundleRef=null`、`evidence/source`=404；目标侧 `execution.performed=false`、`preflight/cleanup=SKIPPED`（**从未构建**）。`environmentStatus=clean`、`runnerStateAfter=READY`。
- `evidence/source`、`evidence/target`、`comparison` 端点均 404（两次）。

## 判读（据真实回传，不倒填）

- **无目标 build 证据 → 语法结论 `INCONCLUSIVE`（阻断）**，`thirdPartyCompileStatus=BLOCKED-INFRA-ERROR`。
- 归因：项目首个 same-OS/same-runner 提交，failure 落在**同机 baseline 交接**（Controller/agent 内部 `baselineReference.artifactHash` 校验），**非** capsule 内容/`target.go`/C→Go 转换缺陷（fe/du 跨 OS/different-runner 均 COMPLETED）。
- 处置：恒就绪政策下已用相同输入重试一次，确定性复现；**不改用本机编译、不放松命令、不伪造 build 结论**。详见 run 根 [`result.md`](../../result.md) 与 [`evaluator_manifest.json`](../../evaluator_manifest.json)。
