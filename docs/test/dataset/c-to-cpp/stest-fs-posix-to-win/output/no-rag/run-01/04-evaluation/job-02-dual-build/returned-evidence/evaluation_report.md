# CodeConvert Evaluation Report

## Outcome

- **Conversion result:** PASS
- **Behavior:** MATCHED
- **Environment:** CLEAN
- **Reason:** All applicable observed dimensions matched.

## Result

| Item | Value |
| --- | --- |
| Job | `eval-20260928-053745-2a386af5` |
| Case | `stest-fs-posix-to-win-run-01` |
| Job status | `COMPLETED` |
| Run verdict | `runnable` |
| Code verdict | `passed` |
| Behavior verdict | `matched` |
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
| 1 | 1 | 1 | 0 | 0 | 100% |

## Evidence Matrix

| Dimension | Status | Applicable | Observed | Diffs |
| --- | --- | --- | --- | ---: |
| Output | matched | yes | yes | 0 |
| Filesystem | not-applicable | no | no | 0 |
| Processes | not-applicable | no | no | 0 |
| Registry | not-applicable | no | no | 0 |
| Network | not-applicable | no | no | 0 |

---
This Markdown view is rendered from the persisted canonical report and comparison result. The JSON artifacts remain authoritative.
