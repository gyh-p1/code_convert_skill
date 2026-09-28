# CodeConvert Evaluation Report

## Outcome

- **Conversion result:** INCONCLUSIVE
- **Behavior:** INCONCLUSIVE
- **Environment:** CLEAN
- **Reason:** Source build failed; baseline cannot be established.

## Result

| Item | Value |
| --- | --- |
| Job | `eval-20260928-073929-e89be213` |
| Case | `du-fs-posix-to-win-run-01` |
| Job status | `COMPLETED` |
| Run verdict | `blocked` |
| Code verdict | `inconclusive` |
| Behavior verdict | `inconclusive` |
| Environment | `clean` |

## Runs

### Source

| Item | Value |
| --- | --- |
| Runtime | `linux/x64` |
| Artifact language | `c` |
| Runner | `linux-vm-agent-x64` |
| Provider | `agent` |
| VM | `linux-eval` |
| Baseline snapshot | `CC-Eval-Linux-8Lang-R7` |
| Execution performed | `yes` |
| Evidence bundle | `evidence/source.json` |
| Preflight | `PASSED` |
| Cleanup | `PASSED` |
| Environment | `clean` |
| Runner state after | `READY` |
| Contaminated | `no` |

> Source failure: `CODE_RESULT` — Source build failed; baseline cannot be established.

### Target

| Item | Value |
| --- | --- |
| Runtime | `windows/x64` |
| Artifact language | `cpp` |
| Runner | `windows-vm-agent-x64` |
| Provider | `agent` |
| VM | `windows-eval` |
| Baseline snapshot | `CC-Eval-Windows-8Lang-R7` |
| Execution performed | `no` |
| Evidence bundle | `not available` |
| Preflight | `SKIPPED` |
| Cleanup | `SKIPPED` |
| Environment | `clean` |
| Runner state after | `not available` |
| Contaminated | `no` |

## Evidence Coverage

| Applicable | Observed | Matched | Mismatched | Inconclusive | Coverage |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 | 0% |

## Failure

- Type: `CODE_RESULT`
- Category: `code`
- Reason: Source build failed; baseline cannot be established.

---
This Markdown view is rendered from the persisted canonical report and comparison result. The JSON artifacts remain authoritative.
