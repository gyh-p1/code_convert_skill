# CodeConvert Evaluation Report

## Outcome

- **Conversion result:** FAIL
- **Behavior:** INCONCLUSIVE
- **Environment:** CLEAN
- **Reason:** Target build failed.

## Result

| Item | Value |
| --- | --- |
| Job | `eval-20260926-052137-b10a6e2f` |
| Case | `c01-uhttpd-run-02` |
| Job status | `COMPLETED` |
| Run verdict | `not-runnable` |
| Code verdict | `failed` |
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

### Target

| Item | Value |
| --- | --- |
| Runtime | `windows/x64` |
| Artifact language | `cpp` |
| Runner | `windows-vm-agent-x64` |
| Provider | `agent` |
| VM | `windows-eval` |
| Baseline snapshot | `CC-Eval-Windows-8Lang-R7` |
| Execution performed | `yes` |
| Evidence bundle | `evidence/target.json` |
| Preflight | `PASSED` |
| Cleanup | `PASSED` |
| Environment | `clean` |
| Runner state after | `READY` |
| Contaminated | `no` |

## Evidence Coverage

| Applicable | Observed | Matched | Mismatched | Inconclusive | Coverage |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 | 0% |

## Evidence Matrix

| Dimension | Status | Applicable | Observed | Diffs |
| --- | --- | --- | --- | ---: |
| Output | not-applicable | no | no | 0 |
| Filesystem | not-applicable | no | no | 0 |
| Processes | not-applicable | no | no | 0 |
| Registry | not-applicable | no | no | 0 |
| Network | not-applicable | no | no | 0 |

## Failure

- Type: `CODE_RESULT`
- Category: `code`
- Reason: Target build failed.

---
This Markdown view is rendered from the persisted canonical report and comparison result. The JSON artifacts remain authoritative.
