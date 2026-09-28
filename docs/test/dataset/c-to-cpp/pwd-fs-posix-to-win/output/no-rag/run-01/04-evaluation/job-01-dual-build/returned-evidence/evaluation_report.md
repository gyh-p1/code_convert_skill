# CodeConvert Evaluation Report

## Outcome

- **Conversion result:** FAIL
- **Behavior:** MISMATCHED
- **Environment:** CLEAN
- **Reason:** At least one applicable observed dimension is mismatched.

## Result

| Item | Value |
| --- | --- |
| Job | `eval-20260928-064021-653f5ee9` |
| Case | `pwd-fs-posix-to-win-run-01` |
| Job status | `COMPLETED` |
| Run verdict | `partial-runnable` |
| Code verdict | `failed` |
| Behavior verdict | `mismatched` |
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
| 1 | 1 | 0 | 1 | 0 | 100% |

## Evidence Matrix

| Dimension | Status | Applicable | Observed | Diffs |
| --- | --- | --- | --- | ---: |
| Output | mismatched | yes | yes | 1 |
| Filesystem | not-applicable | no | no | 0 |
| Processes | not-applicable | no | no | 0 |
| Registry | not-applicable | no | no | 0 |
| Network | not-applicable | no | no | 0 |

## Failure

- Type: `CODE_RESULT`
- Category: `behavior`
- Reason: At least one applicable observed dimension is mismatched.

---
This Markdown view is rendered from the persisted canonical report and comparison result. The JSON artifacts remain authoritative.
