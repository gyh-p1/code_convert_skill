# CodeConvert Evaluation Report

## Outcome

- **Conversion result:** INCONCLUSIVE
- **Behavior:** INCONCLUSIVE
- **Environment:** CLEAN
- **Reason:** agent /run failed: INVALID_PACKAGE: baselineReference artifactHash does not match uploaded artifact

## Result

| Item | Value |
| --- | --- |
| Job | `eval-20260928-092052-390487e9` |
| Case | `rc4-c-to-go-run-01` |
| Job status | `INFRA_ERROR` |
| Run verdict | `blocked` |
| Code verdict | `inconclusive` |
| Behavior verdict | `inconclusive` |
| Environment | `clean` |

## Runs

### Source

| Item | Value |
| --- | --- |
| Runtime | `windows/x64` |
| Artifact language | `c` |
| Runner | `windows-vm-agent-x64` |
| Provider | `agent` |
| VM | `windows-eval` |
| Baseline snapshot | `CC-Eval-Windows-8Lang-R7` |
| Execution performed | `yes` |
| Evidence bundle | `not available` |
| Preflight | `PASSED` |
| Cleanup | `PASSED` |
| Environment | `clean` |
| Runner state after | `READY` |
| Contaminated | `no` |

### Target

| Item | Value |
| --- | --- |
| Runtime | `windows/x64` |
| Artifact language | `go` |
| Runner | `windows-vm-agent-x64` |
| Provider | `agent` |
| VM | `windows-eval` |
| Baseline snapshot | `CC-Eval-Windows-8Lang-R7` |
| Execution performed | `no` |
| Evidence bundle | `not available` |
| Preflight | `SKIPPED` |
| Cleanup | `SKIPPED` |
| Environment | `clean` |
| Runner state after | `READY` |
| Contaminated | `no` |

## Evidence Coverage

| Applicable | Observed | Matched | Mismatched | Inconclusive | Coverage |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 | 0% |

## Failure

- Type: `AGENT_UNAVAILABLE`
- Category: `environment`
- Reason: agent /run failed: INVALID_PACKAGE: baselineReference artifactHash does not match uploaded artifact

---
This Markdown view is rendered from the persisted canonical report and comparison result. The JSON artifacts remain authoritative.
