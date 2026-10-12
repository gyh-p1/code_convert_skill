# Harness-A cases 15 — static review of D2-054 … D2-059

Reviewer: read-only static document reviewer (native `read` / `glob` / `grep` only; no script, no classifier, no conversion, no submission; D:/CodeConvertRemote/Stack never touched; no `.env`/secrets read; source code not reconstructed).
Root of reviewed copies: `docs/dataset-2/dataset-2-copy/`. Note: every item's `casePath` field declares `docs/test/dataset-2/...`, but the artefacts actually present (and reviewed here) live under `docs/dataset-2/dataset-2-copy/...`; the `docs/test/` trees were not inspected.
Read-status legend: `read` = fully read (multi-line); `read(>2000)` = single-line bundle, harness truncated at 2000 chars (no byte-offset read available); `empty` = 0 bytes; `missing` = not present (proved by exhaustive `**/*` glob returning 0 paths); `unread` = exists per exhaustive glob, not opened in this pass.
Harness note: all platform bundles (`evidence-*.json`, `comparison.json`, `evaluation_report.json`, `controller-health*.json`, `*.gen.model.json`, several `metadata.json`/`input_profile.json`) are single-line; they register as `read(>2000)`.

## Cross-item summary

| ID | dir | kind (item / manifest) | declared src sha256 | declared tgt sha256 | disposition / lifecycle / phase | platform behaviour verdict | jobId(s) |
|---|---|---|---|---|---|---|---|
| D2-054 | go-to-powershell | REUSE / REUSE | e6d7db03…f794 | cefd65aa…f633e | CONVERTED / PARTIAL / CLOSED | `mismatched` (only `duration_ms`) → ORACLE_NOT_FREEZABLE | 00 eval-20261011-102132-e8e48715; 01 eval-20261011-102634-45fea1ea |
| D2-055 | go-to-powershell | NEW / REUSE | dac89bc5…92863 | (none) | BLOCKED / WAITING / CLASSIFIER_BLOCKED | not run | none |
| D2-056 | go-to-powershell | NEW / REUSE | f5899aab…2c0f0 | d045b9ca…e5a6aad | FROZEN / DONE / CLOSED | `semantic_pass` (1 minor ts diff) | 00 eval-20261010-064127-9c819595; 01 eval-20261010-064348-e56519fc |
| D2-057 | go-to-python | REUSE / REUSE | 82acc1d8…ae87e | 387733ea…c2ec58 | CONVERTED / DONE / CLOSED | `semantic_pass` (`updated_at`) | 00 eval-20261011-102915-865ebf4f; 01 eval-20261011-103209-dc5a0ab0 |
| D2-058 | go-to-python | NEW / REUSE | 4a50d482…b3277 | acc8f0ba…f8380 | FROZEN / DONE / CLOSED | `matched` (job-02; job-01 void device defect) | 00 eval-20261010-063415-c8015df5; 01 eval-20261010-063644-4b47b02c (void); 02 eval-20261010-063850-22f1de85 |
| D2-059 | go-to-python | REUSE / REUSE | 49971df1…bbef | ede9434a…45ec67 | CONVERTED / DONE / CLOSED | `semantic_pass` (temporary-paths/timestamps) | 00 eval-20261011-103428-3ff1ddf1; 01 eval-20261011-103847-6a80a3bf |

manifest.csv rows (quoted, beginning `"D2-05x",`) — all six declare `"dual-build-PASS (inherited)"` and an *older* eval jobId (2026-10-05/06), plus a column-8 integer (52 / 22 / 19 / 37 / 19 / 171):
- L54 `"D2-054","REUSE","go-to-powershell","Go","PowerShell","parallel_cmd_runner.go","52",…,"eval-20261006-100522-95e51dd6","E6D7…","dual-build-PASS (inherited)"`
- L55 `"D2-055","REUSE",…,"recoverable_overwrite.go","22",…,"eval-20261006-100829-8e2dd404","DAC8…","dual-build-PASS (inherited)"`
- L56 `"D2-056","REUSE",…,"staged_config_build.go","19",…,"eval-20261006-101150-285d4cce","F589…","dual-build-PASS (inherited)"`
- L57 `"D2-057","REUSE","go-to-python","Go","Python","autorun_manifest_backup.go","37",…,"eval-20261005-081016-ae8370bb","82AC…","dual-build-PASS (inherited)"`
- L58 `"D2-058","REUSE",…,"child_cmd_capture.go","19",…,"eval-20261006-101422-6a55da20","4A50…","dual-build-PASS (inherited)"`
- L59 `"D2-059","REUSE",…,"concurrent_pipeline.go","171",…,"eval-20261006-102014-982014bd","4997…","dual-build-PASS (inherited)"`

Manifest sha values are uppercase, item-JSON values lowercase — same digests, case-only difference. Manifest `kind` disagrees with item JSON for D2-055/056/058 (see anomalies).

---

## D2-054 → go-to-powershell/handoff-2026-10-02-d30-parallel-cmd-runner-go

**(1) Identity.** taskId D2-054; kind REUSE; direction go-to-powershell; source `parallel_cmd_runner.go`; sourceSha256 e6d7db03b996f5cb0d0a4f5fb77d1bc715e2fea9f3c6adde88ee45e6a8b8f794; target `target.ps1` sha256 cefd65aa7de26892aa6acf20a321d10fa28581be9a2861cadcfd54d6c83f633e; casePath `docs/test/dataset-2/go-to-powershell/handoff-2026-10-02-d30-parallel-cmd-runner-go`.
Item-JSON: disposition CONVERTED; phase CLOSED; lifecycle PARTIAL; oracleFreezability ORACLE_NOT_FREEZABLE; pendingAction “另冻条件使可观察量确定化（移出 duration_ms），或平台提供覆盖”; sourcePrecheck job eval-20261011-102132-e8e48715 (linux, `go build -o program parallel_cmd_runner.go`, completed/0, execution completed/0); evaluation job eval-20261011-102634-45fea1ea verdict mismatched, platformVerdictPreserved true, digests not identical, accepted true, gate “passes discipline 10.6”, onlyDiff `duration_ms` source [3,4] target [60,58] criticality major rule normalized-text attribution environment, identicalFields name/exit_ok/output; blockingReasons []; usage requests 2, prompt 4590, completion 50112, reasoning 47677, total 54702, model deepseek-flash, failedAttempts 0, note “one conversion call + one model self-review call; NO-REPAIR-IDENTIFIED”.

**(2) File inventory** (33 files, all glob-confirmed; no dir-empty subtrees, no unexpected missing piece):
- `output/batch/01-frozen/classifier-input.json`=read
- `output/batch/01-frozen/classification-1.json`=read
- `output/batch/02-conversion/observed-source-stderr.txt`=empty
- `output/batch/02-conversion/observed-source-stdout.txt`=read
- `output/batch/02-conversion/request.system.txt`=read
- `output/batch/02-conversion/target.gen.model.json`=read(>2000)
- `output/batch/03-self-review/self-review-1.json`=read
- `output/batch/03-self-review/self-review-1.model.json`=read
- `output/batch/03-self-review/review.system.txt`=unread
- `output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json`=read(>2000)
- `output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/job-id.txt`=unread
- `output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/input_profile.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/metadata.json`=read
- `output/batch/04-evaluation/job-00-source-buildability/controller-health-before.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/runners-before.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json`=read
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json`=read
- `output/batch/04-evaluation/job-01-dual-build/batch-authorization.json`=read
- `output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json`=read
- `output/batch/04-evaluation/job-01-dual-build/this-task-classification.json`=read
- `output/batch/04-evaluation/job-01-dual-build/input_profile.json`=read
- `output/batch/04-evaluation/job-01-dual-build/metadata.json`=read
- `output/batch/04-evaluation/job-01-dual-build/controller-health-before.json`=read
- `output/batch/04-evaluation/job-01-dual-build/runners-before.json`=read
- `output/batch/04-evaluation/job-01-dual-build/job-id.txt`=read (eval-20261011-102634-45fea1ea)
- `output/batch/evaluator_manifest.json`=read; `output/batch/result.md`=read
- `result.md` present? yes. `evaluator_manifest.json` present? yes.

**(3) Facts.**
- Freeze/classify: classifier v2.4, cls REVIEW_SENSITIVE, admissionStatus ALLOWED, blockingReason null, classifierSha256 009a6f31…f3a4, note “classified with parallel_cmd_runner.go + run_case.py”; inputManifestSha256 2085dc51…2245; reviewGroups dynamic_code/filesystem/process; requiresSyntheticData true, executionApproved true.
- Source precheck job-00: build cmd `go build -o program parallel_cmd_runner.go`, build completed/exit 0 (8948→6331 ms), stderr empty, execution completed/exit 0, stdout artifact report with duration_ms 1/4 (differs run-to-run), cleanup PASSED, contaminated false, runnerStateAfter READY, snapshot CC-Eval-Linux-8Lang-1.0.28. job-00 target is a placeholder (`targetHash: sha256:placeholder-precheck`); its `evaluation_report.json` still carries `behaviorVerdict=mismatched` / codeVerdict failed against that placeholder — precheck artefact, not a conversion verdict.
- Requests/responses: `request.system.txt` = Go→PowerShell converter system prompt (PowerShell 7.6 single file, byte-identical stdout/stderr/exit, real concurrency, filename `target.ps1`). `target.gen.model.json` = a **real body** (`role: assistant`, full `content` PowerShell code block, long `reasoning_content`) but carries **no model / finish_reason / usage / hash fields** — it is body-only, not a complete response envelope. No failed attempts recorded (failedAttempts 0).
- Self-review: `self-review-1.json` verdict NO-REPAIR-IDENTIFIED, reviewedScope “target.gen.ps1 (167 lines)”, 5 items all “未发现差异”, origins “undetermined”, risk 低; `self-review-1.model.json` model deepseek-flash, finishReason stop, usage prompt 2881 / completion 24429 / reasoning 23608 / total 27310, note “Static review only.” No repairs → no parent/final hash divergence.
- Jobs: job-01 caseId D2-054, source artifactLanguage go / target powershell, os linux x64, snapshot 1.0.28; source execution stdout = two records name `sh -c echo exec-safe-1` / `sh -c uname -s`, exit_ok true, output `exec-safe-1` / `Linux`, duration_ms 3/4; target stdout identical except duration_ms 60/58; both exit 0, both stderr empty; side effect = JSON report under `/tmp/safe-attck-go/04_execution/`; comparison verdict `mismatched`, sole diff path `stream.normalizedText`, criticality major; evidenceCoverage applicable/observed 1, matched 0, mismatched 1; lifecycle preflight/cleanup PASSED, environment clean, runnerStateAfter READY; controller-health-before status ok, ready true, 3 runners; device/environment attribution for `duration_ms` is NOT conversion-introduced.
- Anomaly inside job-01 `batch-authorization.json`: the `dataSource.confirmation` text says “该项 **D2-088** 无网络、无凭证…”, i.e. a cross-case copy-paste reference; authorization metadata otherwise generic (batch scope “所有非BLOCKED任务”, validUntil 2026-10-17, contractHash a9ed1445…).
- Independent evidence facts: source and target raw-stream digests differ (source b42fe9b1…f076cb3, target bf8ed9c3…b09948) and sizeBytes differ (308 vs 310) solely through `duration_ms` digits; count fields/order identical. Attribution: environment/device (PowerShell subprocess start-up overhead), NOT conversion-introduced; platform `mismatched` preserved, not re-judged.
- Knowledge candidates: (a) “active-counter / real-measurement field (`duration_ms`, `time.Since`) is not freezeable by noise tokens” → current contract coverage: `references/framework/evaluation-readiness-contract.md` §4 (oracle 与两侧对称) and §5 (原始观察、采信与归因); counterpart cluster K-O in `docs/dataset-2/dataset-2-copy/batch/current-system-review-2026-10-12/full-review-knowledge-disposition.md` (“时间值消噪与格式/取值定义分开”).
- Optimization: item is DONE-worthy as PARTIAL; the only open lever is freezeability of `duration_ms` (e.g. drop the counter from the oracle, or platform-provided tolerance), exactly as `pendingAction` states.
- Unknowns: job-00 comparison/authorization/health/input_profile and `review.system.txt` not opened; the actual `target/` tree is outside the reviewed copy.

---

## D2-055 → go-to-powershell/handoff-2026-10-02-d30-recoverable-overwrite-go

**(1) Identity.** taskId D2-055; kind NEW; direction go-to-powershell; source `recoverable_overwrite.go`; sourceSha256 dac89bc57cd1c876c45baebe4b73aac152cbeddc00013da1001d1f55ddc92863; no targetSha256 (never converted); casePath `docs/test/dataset-2/go-to-powershell/handoff-2026-10-02-d30-recoverable-overwrite-go`.
Item-JSON: disposition BLOCKED; phase CLASSIFIER_BLOCKED; lifecycle WAITING; blockingReason `public_network_unverified`; pendingAction “obtain real isolation evidence, then reclassify (do not hand-edit the classification JSON)”; classifier v2.3, admissionStatus BLOCKED, cls REVIEW_NETWORK, networkMode hostname, networkTargets [{value demo.txt, line 13, scope hostname, provenance literal, redirectVerified false}], classifierSha256 441b4d50…6524; classifierObservation suspectedFalsePositive true, basis “no network call whatsoever … demo.txt appears on line 13 as a local filename argument to filepath.Join”, handling “recorded as fact only; admissionStatus=BLOCKED remains authoritative”, caveat “Agent must not re-judge or downgrade a classifier verdict”; usage requests 0; blockingReasons [{code public_network_unverified, detail classifier admissionStatus=BLOCKED; requires reclassification after isolation evidence}].

**(2) File inventory** (3 files; this subtree is *not* empty, it has no 02-conversion / 03-self-review / 04-evaluation / result.md at all):
- `output/batch/01-frozen/classification-1.json`=read
- `output/batch/01-frozen/classifier-input.json`=read
- `output/batch/01-frozen/frozen-inputs.md`=read
- Missing: `output/batch/02-conversion/` (0 files), `output/batch/03-self-review/` (0 files), `output/batch/04-evaluation/` (0 files), `output/batch/result.md`, `output/batch/evaluator_manifest.json` — all proved absent by exhaustive `**/*` glob.
- `result.md` present? **no**. `evaluator_manifest.json` present? **no**.

**(3) Facts.**
- Freeze/classify: `frozen-inputs.md` records batchId batch, taskId D2-055, direction, Kind NEW, sourcePath `source/recoverable_overwrite.go`, sourceSha256 matching manifest character-for-character; classification table cls REVIEW_NETWORK / admissionStatus BLOCKED / blockingReason public_network_unverified / reason network_scope_and_inputs_require_review / network_mode hostname / network_targets demo.txt line 13. The page both (a) stops per classifier-agent-gate §2 and (b) independently records the heuristic false positive (no `net.`/`Dial`/`Listen`/`http`/`url`/`socket`; `demo.txt` is a `filepath.Join` argument; the file only makes a temp dir, writes `demo.txt`/`demo.bak`, overwrites `demo.txt`, writes a JSON report, prints paths). Final state WAITING / BLOCKED_CLASSIFIER; 0 model calls; target UNVERIFIED.
- `classification-1.json` corroborates: details.files[0].signals.network `[]` but `has_network: true` with `network_mode: hostname`; fs signals lines 12,16,17,18,23; requiresNetworkIsolation true; inputManifestSha256 8c37daa8…a9dc.
- Source precheck: **none** (correctly not attempted). Requests/responses: **none** (0 model calls). Self-review: none. Jobs: none. Independent evidence facts: the classification JSON itself shows `"network": []` while asserting a hostname target — the reproducible heuristic defect, recorded but not acted on. Attribution: classifier heuristic (device/tooling), not source behaviour, not conversion.
- Knowledge candidates: reproducible false positive “local filename literal captured as `network_mode: hostname`” → current coverage: `references/workflow/classifier-agent-gate.md` §2 (cited by `frozen-inputs.md`; rule that the classifier verdict is authoritative and not re-judged by the Agent) plus the classifier SHA-pinning rule. This belongs in classifier tuning knowledge, not in language pages.
- Optimization: item is correctly parked; no progress possible without real isolation evidence + reclassification. Delivery completeness: **missing `result.md`** despite the delivery contract requiring a per-item report for every terminal/paused outcome (`references/framework/delivery-handoff-contract.md` §1.1, header verified at line 13).
- Unknowns: the source file itself is not in this copy, so the “no network” claim is taken from the frozen-inputs note and the classifier `network: []` signal, not re-derived.

---

## D2-056 → go-to-powershell/handoff-2026-10-02-d30-staged-config-build-go

**(1) Identity.** taskId D2-056; kind NEW; direction go-to-powershell; source `staged_config_build.go`; sourceSha256 f5899aabc9a90ffa27eec6e89bcdb9da12d94fd50f78d891612727f0af62c0f0; target `target.ps1` sha256 d045b9cab80eef5ec4224a83cbceecc5815e5b110cd8bdc52a0bed9d0e5a6aad; casePath `docs/test/dataset-2/go-to-powershell/handoff-2026-10-02-d30-staged-config-build-go`.
Item-JSON: disposition FROZEN; phase CLOSED; lifecycle DONE; classifier v2.3 ALLOWED cls REVIEW_SIDE_EFFECTS blockingReason null, classifierSha256 441b4d50…6524; sourcePrecheck job eval-20261010-064127-9c819595 (linux, `go build -o program staged_config_build.go`, completed/0, execution completed/0, stdout artifact line only); evaluation job eval-20261010-064348-e56519fc verdict `semantic_pass`, verdictIsNotMatched true, note on matchedDimensions 0 / mismatchedDimensions 0, soleDifference line 10 `"time"` source 06:43:58Z vs target 06:44:27Z, attribution run-time clock / environment; accepted true; blockingReasons []; usage requests 1, note “one conversion call; self-review NO-REPAIR-IDENTIFIED”.

**(2) File inventory** (19 files):
- `output/batch/01-frozen/classification-1.json`=read
- `output/batch/01-frozen/classifier-input.json`=unread
- `output/batch/03-self-review/self-review-1.json`=read
- `output/batch/04-evaluation/job-00-source-buildability-linux/comparison_manifest.json`=read
- `output/batch/04-evaluation/job-00-source-buildability-linux/input_profile.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability-linux/metadata.json`=read
- `output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evaluation_report.json`=read(>2000)
- `output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json`=read
- `output/batch/04-evaluation/job-01-dual-build/input_profile.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/metadata.json`=read
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json`=read
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json`=read
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log`=read (2 lines)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md`=unread
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json`=read(>2000)
- `output/batch/result.md`=read
- Missing (proved 0 paths by exhaustive glob): whole `output/batch/02-conversion/` (no `request.system.txt`, no `target.gen.model.json`, no observed-source-*), `output/batch/evaluator_manifest.json`, `output/batch/03-self-review/self-review-1.model.json`, `output/batch/03-self-review/review.system.txt`.
- `result.md` present? yes. `evaluator_manifest.json` present? **no**.

**(3) Facts.**
- Freeze/classify: v2.3, cls REVIEW_SIDE_EFFECTS, reason local_effects_require_review, reviewGroups [filesystem], fs signals lines 14/15/20, has_network false, executionApproved true, requiresSyntheticData false, inputManifestSha256 604d5b32…3d98a.
- Source precheck job-00: metadata caseId `batch-d2-056-go-to-powershell-staged-config-precheck`, purpose “source precheck only”; build completed/0 (6738 ms), stderr empty, execution completed/0 (67 ms), stdout `artifact: /tmp/safe-attck-go/02_resource_development/bootstrap-config.json` size 75 bytes digest 696b9826…eb197; snapshot CC-Eval-Linux-8Lang-1.0.26. Its `comparison_manifest.json` target is a placeholder (`pwsh … Get-Content placeholder.txt | Out-Null`) yet the paired `evaluation_report.json` records `behaviorVerdict=mismatched`, codeVerdict failed — placeholder-precheck noise, not a conversion verdict.
- Requests/responses: **no request/response capture at all** in this item (no request.system.txt, no model json) even though item-JSON usage asserts requests 1. Failed attempts: not recorded.
- Self-review: `self-review-1.json` shape differs from the other items — taskId, round 1, reviewer agent-static, verdict NO-REPAIR-IDENTIFIED, `checks` (json-shape, json-array, json-no-trailing-newline, sample-txt, utf8-encoding, mkdir, printed-line), `residualRisks` (time-field value by construction; RFC3339 offset construction not proven byte-identical for every offset; UTC-only `Z` branch under non-UTC zone), limitations “static review only”, decision “proceed to evaluation-ready check”. No `self-review-1.model.json` → no model/finish_reason/usage metadata file for this self-review.
- Jobs: job-01 caseId `batch-d2-056-go-to-powershell-staged-config`, metadata carries source/target sha, frozenArgv [], frozenStdin null, oracleBasis = source-precheck observation, driverNote “resolves the artifact on one shared path and applies identical post-processing to both sides (discipline 10.13); echoes both side-effect files”, expectedDifference timestamp. Source build completed/0 (5680 ms), execution completed/0 (33 ms), stdout 275 B digest 09087670…914e1 including the `--- staged-resources/sample.txt ---` / `--- bootstrap-config.json ---` echo, `"time": "2026-10-10T06:43:58Z"`. Target build completed/0 (3278 ms), execution completed/0 (268 ms), stdout 275 B digest 21acc962…185d6, `"time": "2026-10-10T06:44:27Z"`. Comparison `semantic_pass`, verdictReason “Applicable dimensions match with only explicitly configured minor differences”, output status `semantic-match`, 1 diff path `stream.normalizedText` criticality minor rule `noise-tolerant-v1:text-tokens:temporary-paths,timestamps,ephemeral-ports`; filesystem/processes/registry/network all not-applicable. Side effects compared through driver echo: `staged-resources/sample.txt` = `safe fixture\n`, `bootstrap-config.json` key order campaign/targets/time, 2-space indent, no trailing newline. Cleanup: preflight/cleanup PASSED both sides, contaminated false, environment clean, runnerStateAfter READY; controller-health-after status ok ready true 3 runners; controller.log “comparison job created 06:43:48 / finished 06:44:56”.
- Independent evidence facts: only line 10 differs; equal 275-byte payloads after denoising; `sed`-style line-by-line per `result.md`. Attribution: environment/clock, NOT conversion-introduced; `semantic_pass` kept distinct from `matched` (matchedDimensions 0).
- Knowledge candidates: RFC3339 offset construction byte-identity and the UTC-only coverage gap → current coverage `references/framework/evaluation-readiness-contract.md` §4 (oracle 与两侧对称) / §5 (归因), plus cluster K-O (“时间值消噪与格式/取值定义分开”) in the knowledge-disposition file. `filesystem: not-applicable` while the program demonstrably writes files is a candidate for “side-effect comparison must go through a platform filesystem dimension, not only driver echo”.
- Optimization: delivery-integrity lever — restore the missing conversion capture + `evaluator_manifest.json` (delivery contract §2.1/§3) before treating this as a complete DONE artefact; a UTC vs `±hh:mm` runner pair would close the timestamp-format gap.
- Unknowns: `classifier-input.json`, both `input_profile.json`, `evaluation_report.md` not opened; `target/` tree not in copy.

---

## D2-057 → go-to-python/handoff-2026-10-02-d28-autorun-manifest-backup-go

**(1) Identity.** taskId D2-057; kind REUSE; direction go-to-python; source `autorun_manifest_backup.go`; sourceSha256 82acc1d874a0b586a0b852bd0b7bc51a28fb4b9dc454a72b03897626398ae87e; target `target.py` sha256 387733eab1edbdb388f6df49be39715f9568d182fa94d5f92573d0a8d1c2ec58; casePath `docs/test/dataset-2/go-to-python/handoff-2026-10-02-d28-autorun-manifest-backup-go`.
Item-JSON: disposition CONVERTED; phase CLOSED; lifecycle DONE; pendingAction null; classifier v2.4 ALLOWED cls REVIEW_SIDE_EFFECTS blockingReason null, classifierSha256 009a6f31…f3a4, note “…+ run_case.py”; sourcePrecheck job eval-20261011-102915-865ebf4f (linux, `go build -o program autorun_manifest_backup.go`, completed/0, execution completed/0 with two artifact lines + JSON report); evaluation job eval-20261011-103209-dc5a0ab0 verdict `semantic_pass`, digests not identical, accepted true, gate “passes discipline 10.6”, verdictTier “semantic_pass is its own tier (discipline 10.15); NOT recorded as matched”, onlyDiff entries[].updated_at minor rule noise-tolerant-v1:text-tokens:timestamps attribution environment; blockingReasons []; usage requests 2, prompt 4078, completion 18586, reasoning 17419, total 22664, model deepseek-flash, failedAttempts 0.

**(2) File inventory** (33 files):
- `output/batch/01-frozen/classifier-input.json`=read
- `output/batch/01-frozen/classification-1.json`=read
- `output/batch/02-conversion/observed-source-stdout.txt`=unread
- `output/batch/02-conversion/observed-source-stderr.txt`=unread
- `output/batch/02-conversion/target.gen.model.json`=read(>2000)
- `output/batch/02-conversion/request.system.txt`=read
- `output/batch/03-self-review/self-review-1.json`=read
- `output/batch/03-self-review/review.system.txt`=unread
- `output/batch/03-self-review/self-review-1.model.json`=read
- `output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/job-id.txt`=unread
- `output/batch/04-evaluation/job-00-source-buildability/input_profile.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/metadata.json`=read
- `output/batch/04-evaluation/job-00-source-buildability/controller-health-before.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/runners-before.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json`=read
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/batch-authorization.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/this-task-classification.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json`=read
- `output/batch/04-evaluation/job-01-dual-build/input_profile.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/metadata.json`=read
- `output/batch/04-evaluation/job-01-dual-build/controller-health-before.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/runners-before.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/job-id.txt`=unread
- `output/batch/evaluator_manifest.json`=read
- `output/batch/result.md`=read
- `result.md` present? yes. `evaluator_manifest.json` present? yes.

**(3) Facts.**
- Freeze/classify: v2.4, REVIEW_SIDE_EFFECTS, reviewGroups filesystem/process, fs lines 20/38/41, process line 33, run_case.py sha 883d3535…7b34, has_network false, requiresSyntheticData false, inputManifestSha256 394ce8f0…7f5b.
- Source precheck job-00: metadata caseId D2-057, note “output contains RFC3339 timestamps (covered by the timestamps noise token)”; evidence-source snapshot 1.0.28, build completed/0 (6487 ms), execution completed/0 (35 ms), stdout two artifact lines + report with updated_at 2026-10-11T10:29:26Z / …:28Z; digest/raw path `/tmp/safe-attck-go/05_persistence/`.
- Requests/responses: `request.system.txt` = Go→Python converter prompt (Python 3.12 single file, `target.py`, real dir+2 file writes, RFC3339 with `Z` for offset 0, byte-identical `advanced-autorun-manifest.json` + `.bak.json`, no trailing newline, two artifact lines). `target.gen.model.json` = real body (role assistant, full content, reasoning_content) but again **no model/finish_reason/usage/hash envelope fields**. Failed attempts 0.
- Self-review: `self-review-1.json` verdict NO-REPAIR-IDENTIFIED, reviewedScope “…target.gen.py…”, 6 items, all “No issue identified”, origin “undetermined”, risk None. `self-review-1.model.json` model deepseek-flash, finishReason stop, usage 2106/15818/15245/17924, “Static review only.” No repairs.
- Jobs: job-01 caseId D2-057, metadata sourceHash 82acc1d8… targetHash 387733ea…; source build completed/0 (5639 ms), execution completed/0 (33 ms), stdout 2 artifact lines + report, updated_at 2026-10-11T10:32:19Z / …:21Z; target build completed/0 (294 ms), execution completed/0 (474 ms), same two artifact lines, updated_at …10:32:45Z / …:47Z; both stderr empty, both exit 0; comparison `semantic_pass` with 1 minor diff path `stream.normalizedText` rule noise-tolerant-v1:text-tokens:temporary-paths,timestamps,ephemeral-ports; filesystem/processes/registry/network not-applicable; evidenceCoverage applicable/observed 1, matched 0, mismatched 0, coverageRatio 1.0; cleanup PASSED both sides, environment clean, runnerStateAfter READY, snapshot 1.0.28. `evaluator_manifest.json`: languagePair go→python, sceneTags [file-io], sourceOs/targetOs linux x64, evidenceMode static-and-runtime, status converted-and-evaluated, jobId eval-20261011-103209-dc5a0ab0, oracleFreezability “FREEZABLE: only updated_at is non-reproducible and it IS covered by the timestamps noise token”, networkBoundary “isolated VM; no egress”.
- Independent evidence facts: digests source 5880148d…6ba3b vs target 349f45cd…5a215d (not identical) yet behaviour verdict semantic_pass; attribution environment/timestamps, NOT conversion-introduced. `rfc3339()` correctly renders UTC offset as `Z` (not `+00:00`) per result.md line 27.
- Knowledge candidates: RFC3339 `Z`-vs-`+00:00` mapping and timestamp noise coverage → current coverage `resources` cited above; cluster K-O (“时间值消噪与格式/取值定义分开”) + the Go→Python time rule noted there (“Go→Python时间规则已有”).
- Optimization: only the non-UTC offset branch and write-failure branches remain; a TZ-shifted runner run would close them.
- Unknowns: observed-source stdout/stderr txt, job-00 evaluation_report/comparison_manifest/input_profile/classification/authorization/health, job-01 input_profile/classification/authorization/health, `review.system.txt` not opened.

---

## D2-058 → go-to-python/handoff-2026-10-02-d28-child-cmd-capture-go

**(1) Identity.** taskId D2-058; kind NEW; direction go-to-python; source `child_cmd_capture.go`; sourceSha256 4a50d482cb62c42d3e17a74ea6cc95c05dd8a7634707efb34a0cc92f62ab3277; target `target.py` sha256 acc8f0ba397cf35ca80eb3c60684ba6c0d2907a14be6fac678caf5f0e3ff8380; casePath `docs/test/dataset-2/go-to-python/handoff-2026-10-02-d28-child-cmd-capture-go`.
Item-JSON: disposition FROZEN; phase CLOSED; lifecycle DONE; classifier v2.3 ALLOWED cls REVIEW_SENSITIVE blockingReason null, classifierSha256 441b4d50…6524; sourcePrecheck job eval-20261010-063415-c8015df5 (windows, `go build -o program.exe child_cmd_capture.go`, completed/0, execution completed/0, stdout `artifact: C:\Users\zj213\AppData\Local\Temp\safe-attck-go\04_execution\child-output.txt`); evaluation job eval-20261010-063850-22f1de85 verdict `matched`, accepted true, outputDiffs 0, gate “passes discipline 10.6”, normalizedTextByteEqual true, digestNote “raw-stream digests differ … sizeBytes differ by 1 from a CRLF/LF difference … comparator applied the server preset temporary-paths token”; instrumentDefects [job eval-20261010-063644-4b47b02c “the driver attached the captured-file echo only in the script branch …fixed by resolving the artifact and applying post-processing on one shared path”]; blockingReasons []; usage requests 1, note “one conversion call; self-review NO-REPAIR-IDENTIFIED”.

**(2) File inventory** (30 files):
- `output/batch/01-frozen/classification-1.json`=read
- `output/batch/01-frozen/classifier-input.json`=read
- `output/batch/03-self-review/self-review-1.json`=read
- `output/batch/04-evaluation/job-00-source-buildability-windows/comparison_manifest.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability-windows/input_profile.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability-windows/metadata.json`=read
- `output/batch/04-evaluation/job-00-source-buildability-windows/returned-evidence/evaluation_report.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability-windows/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/attribution.md`=read
- `output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json`=read
- `output/batch/04-evaluation/job-01-dual-build/input_profile.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/metadata.json`=read
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json`=read
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log`=unread
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md`=unread
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json`=read(>2000)
- `output/batch/04-evaluation/job-02-dual-build-symmetric-driver/comparison_manifest.json`=read
- `output/batch/04-evaluation/job-02-dual-build-symmetric-driver/input_profile.json`=unread
- `output/batch/04-evaluation/job-02-dual-build-symmetric-driver/metadata.json`=read
- `output/batch/04-evaluation/job-02-dual-build-symmetric-driver/returned-evidence/comparison.json`=read
- `output/batch/04-evaluation/job-02-dual-build-symmetric-driver/returned-evidence/controller-health-after.json`=unread
- `output/batch/04-evaluation/job-02-dual-build-symmetric-driver/returned-evidence/controller.log`=unread
- `output/batch/04-evaluation/job-02-dual-build-symmetric-driver/returned-evidence/evaluation_report.json`=read(>2000)
- `output/batch/04-evaluation/job-02-dual-build-symmetric-driver/returned-evidence/evaluation_report.md`=unread
- `output/batch/04-evaluation/job-02-dual-build-symmetric-driver/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-02-dual-build-symmetric-driver/returned-evidence/evidence-target.json`=read(>2000)
- `output/batch/result.md`=read
- Missing (exhaustive glob = 0): whole `output/batch/02-conversion/`, `output/batch/evaluator_manifest.json`, `output/batch/03-self-review/self-review-1.model.json`, `output/batch/03-self-review/review.system.txt`.
- `result.md` present? yes. `evaluator_manifest.json` present? **no**.

**(3) Facts.**
- Freeze/classify: v2.3, REVIEW_SENSITIVE, reviewGroups dynamic_code/filesystem/process, fs lines 12/20, process line 15, dynamic_code line 6, has_network false, has_process_exec true, requiresSyntheticData true, inputManifestSha256 dd13e268…c7cda.
- Source precheck job-00: metadata caseId `batch-d2-058-go-to-python-child-cmd-precheck`, purpose “source precheck only (windows)”, note “spawns cmd /C echo safe-exec and captures combined output”; evidence-source snapshot CC-Eval-Windows-8Lang-1.0.26, build completed/0 (12526 ms), execution completed/0 (99 ms), stdout `artifact: C:\Users\zj213\…\child-output.txt\n` size 88 digest 8bf33901…b2f4, stderr empty.
- Requests/responses: **no request/response capture** present (no request.system.txt, no model json) despite item-JSON usage requests 1. failedAttempts 0.
- Self-review: `self-review-1.json` shape like D2-056 — taskId, round 1, reviewer agent-static, verdict NO-REPAIR-IDENTIFIED, `checks` (combined-output, error-fallback, path, mkdir-all, printed-line, file-mode, stdlib-only), `residualRisks` (launch-failure OSError text differs from Go err.Error(); raw captured CRLF content), limitations “static review only”, decision “proceed to evaluation-ready check”. No model-json/usage file for this self-review.
- Jobs — three, one void:
  - job-00 (precheck) eval-20261010-063415-c8015df5: see above.
  - job-01 eval-20261010-063644-4b47b02c: caseId `batch-d2-058-go-to-python-child-cmd`, windows x64, snapshot 1.0.26; source build completed/0 (12339 ms) execution completed/0 (99 ms) stdout 88 B digest 8bf33901…b2f4; target build completed/0 (59 ms) execution completed/0 (125 ms) stdout 118 B digest bc967b26…6523 including `--- captured ---\nsafe-exec`; comparison verdict `mismatched` major, diff path `stream.normalizedText`, source summary one line vs target line+captured. `attribution.md` documents the root cause: driver had two branches, the script branch (`target.py/.rb/.ps1`) echoed the captured file while the compiled branch (`program.exe/program`) did not; source (Go) took the compiled branch, target (Python) the script branch → length-different streams → **spurious FAIL from the device**. Job voided, recorded UNVERIFIED; both raw observations preserved.
  - job-02 eval-20261010-063850-22f1de85 (symmetric driver): caseId `batch-d2-058-go-to-python-child-cmd-v2`; metadata `supersedes` job-01 with reason, `driverFix` “artifact resolution and post-processing now run on one shared code path for both sides”; comparison_manifest source `go build -o program.exe child_cmd_capture.go` windows, target `python -m py_compile target.py`; source build completed/0 (15475 ms) execution completed/0 (110 ms) stdout 117 B digest cdf9cbb6…a156 with captured echo; target build completed/0 (135 ms) execution completed/0 (175 ms) stdout 118 B digest bc967b26…6523 with captured echo; comparison `matched` (diffs []), codeVerdict passed, matchedDimensions 1, coverageRatio 1.0; preflight/cleanup PASSED, environment clean, runnerStateAfter READY.
- Independent evidence facts: after normalisation both sides are 116 bytes and byte-equal; raw streams differ (117 vs 118 B) and raw digests differ, attributed to CRLF/LF in the captured line plus user-specific temp path, both covered by `temporary-paths`; NOT conversion-introduced. Side effect = `child-output.txt` echoed through the driver, not through a platform filesystem dimension.
- Knowledge candidates: (a) “any driver post-processing (file echo, marker, normalisation) must run identically on both sides; form-based branch divergence manufactures false FAILs (discipline 10.13)” → current coverage `references/framework/evaluation-readiness-contract.md` §2 (驱动来源与四要素) and §4 (oracle 与两侧对称); cluster K-W (“进程场景流捕获表明确分离/合并/顺序/双流排空”). (b) Go `CombinedOutput` interleaving vs Python `stderr=STDOUT` capture. (c) launch-failure wording divergence (Go `err.Error()` vs Python `OSError`) and non-zero exit-status wording → clusters K-U and K-E.
- Optimization: add a platform-level filesystem dimension instead of driver echo; trigger the launch-failure and non-zero-exit branches with a legal driver; restore the missing conversion capture + `evaluator_manifest.json` (delivery contract §2.1/§3).
- Unknowns: job-00 evaluation_report/input_profile/comparison_manifest, job-01/02 `input_profile.json`, `controller.log`, `controller-health-after.json`, `evaluation_report.md`, `evaluation_report.json` (job-01) not opened; run_case.py / target tree not in copy.

---

## D2-059 → go-to-python/handoff-2026-10-02-d28-concurrent-pipeline-go

**(1) Identity.** taskId D2-059; kind REUSE; direction go-to-python; source `concurrent_pipeline.go`; sourceSha256 49971df1cf49160a4a6e7f91b03769af670decf93e01dcea49961d72640bbbef; target `target.py` sha256 ede9434a9eb67594927b87e9fb2c1603c2856f105b8aeb3bc91956a0a845ec67; casePath `docs/test/dataset-2/go-to-python/handoff-2026-10-02-d28-concurrent-pipeline-go`.
Item-JSON: disposition CONVERTED; phase CLOSED; lifecycle DONE; pendingAction null; classifier v2.4 ALLOWED cls REVIEW_SIDE_EFFECTS blockingReason null, classifierSha256 009a6f31…f3a4, note “…+ run_case.py”; sourcePrecheck job eval-20261011-103428-3ff1ddf1 (linux, `go build -o program concurrent_pipeline.go`, completed/0, execution completed/0, stdout artifact+input lines and `{ total=283 valid=280 invalid=3, 283 records }`); evaluation job eval-20261011-103847-6a80a3bf verdict `semantic_pass`, digests not identical, accepted true, gate “passes discipline 10.6”, verdictTier “semantic_pass (discipline 10.15); NOT matched”, onlyDiff criticality minor rule `noise-tolerant-v1:text-tokens:temporary-paths,timestamps,ephemeral-ports` attribution environment; blockingReasons []; usage requests 2, prompt 6504, completion 40090, reasoning 37528, total 46594, model deepseek-flash, failedAttempts 0.

**(2) File inventory** (34 files):
- `output/batch/01-frozen/classifier-input.json`=read
- `output/batch/01-frozen/classification-1.json`=read
- `output/batch/02-conversion/observed-source-stderr.txt`=unread
- `output/batch/02-conversion/observed-source-stdout.txt`=unread
- `output/batch/02-conversion/target.gen.model.json`=read(>2000)
- `output/batch/02-conversion/request.system.txt`=read
- `output/batch/03-self-review/review.system.txt`=unread
- `output/batch/03-self-review/self-review-1.json`=read
- `output/batch/03-self-review/self-review-1.model.json`=read
- `output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-00-source-buildability/job-id.txt`=unread
- `output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/input_profile.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/metadata.json`=read
- `output/batch/04-evaluation/job-00-source-buildability/controller-health-before.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/runners-before.json`=unread
- `output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json`=read
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log`=unread
- `output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json`=read(>2000)
- `output/batch/04-evaluation/job-01-dual-build/batch-authorization.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/this-task-classification.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json`=read
- `output/batch/04-evaluation/job-01-dual-build/input_profile.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/metadata.json`=read
- `output/batch/04-evaluation/job-01-dual-build/controller-health-before.json`=unread
- `output/batch/04-evaluation/job-01-dual-build/job-id.txt`=unread
- `output/batch/04-evaluation/job-01-dual-build/runners-before.json`=unread
- `output/batch/evaluator_manifest.json`=read
- `output/batch/result.md`=read
- `result.md` present? yes. `evaluator_manifest.json` present? yes.

**(3) Facts.**
- Freeze/classify: v2.4, REVIEW_SIDE_EFFECTS, reviewGroups filesystem/process, fs lines 155/166/186, run_case.py sha 992c286a…0585, has_network false, has_process_exec false, requiresSyntheticData false, inputManifestSha256 1d13d9b8…c177.
- Source precheck job-00: metadata caseId D2-059, note “Records carry Created (RFC3339) timestamps covered by the timestamps noise token”; evidence-source snapshot 1.0.28, build completed/0 (6067 ms), execution completed/0 (34 ms), stdout artifact+input lines and full report beginning `{"name":"long-safe-pipeline","stats":{"total":283,"valid":280,"invalid":3}, "records":[{"id":"","mode":"","fields":null,"digest":"","valid":false,"error":"bad token: broken-token","created":"2026-10-11T10:34…`.
- Requests/responses: `request.system.txt` = Go→Python converter prompt (Python 3.12 single file, no stubbing, full generate/parse/digest/stats logic, exact struct key order name→stats→records, total→valid→invalid, id→mode→fields→digest→valid→error→created with `error` `omitempty`, `fields` map lexicographic and `null` for invalid, 2-space indent, no trailing newline, RFC3339 with `Z`). `target.gen.model.json` = real body (role assistant, full content, long reasoning_content) but **no model/finish_reason/usage/hash envelope**. Failed attempts 0.
- Self-review: `self-review-1.json` verdict NO-REPAIR-IDENTIFIED, reviewedScope “target.gen.py vs concurrent_pipeline.go…”, 6 items, all “未发现差异/正确”, origin “source-preexisting”, risk none. `self-review-1.model.json` model deepseek-flash, finishReason stop, usage 3896/25559/24636/29455, “Static review only.” No repairs.
- Jobs: job-01 caseId D2-059, metadata sourceHash 49971df1… targetHash ede9434a…; source build completed/0 (6431 ms), execution completed/0 (32 ms), target build completed/0 (373 ms), execution completed/0 (558 ms); both stdout artifact+input and report with stats total 283 / valid 280 / invalid 3 and record list, both exit 0, both stderr empty; comparison `semantic_pass` with 1 minor diff `stream.normalizedText` rule `noise-tolerant-v1:text-tokens:temporary-paths,timestamps,ephemeral-ports`; filesystem/processes/registry/network not-applicable; coverage applicable/observed 1, matched 0, mismatched 0, coverageRatio 1.0; preflight/cleanup PASSED, environment clean, runnerStateAfter READY, snapshot 1.0.28. `evaluator_manifest.json`: languagePair go→python, sceneTags [file-io, concurrency], linux x64, status converted-and-evaluated, jobId eval-20261011-103847-6a80a3bf, oracleFreezability “FREEZABLE: only timestamps/paths non-reproducible and both covered by noise tokens”, networkBoundary “isolated VM; no egress”.
- Independent evidence facts: source stdout digest e1f8b2de…0296 vs target 79c53ea0…7f8e (not identical) with behaviour verdict semantic_pass; `semantic_pass` kept separate from `matched`. Attribution environment (temp paths/timestamps), NOT conversion-introduced.
- Knowledge candidates: (a) omitempty / map-sort / nil-map→null JSON shape fidelity for Go→Python (self-review items 3–4) → current coverage `skills/references/languages/python.md` and `go.md` (language pages named in the root load path; not re-opened here) plus cluster K-J. (b) RFC3339 `Z` mapping (K-O). (c) concurrency ordering not stress-tested (K-R sort/stability; K-AA counters).
- Optimization: add a TZ-shifted run and an ordering-stress fixture; keep `semantic_pass` out of any matched statistic.
- Unknowns: observed-source stdout/stderr txt, job-00 evaluation_report/comparison_manifest/input_profile/classification/authorization/health, job-01 input_profile/classification/authorization/health/controller.log, `review.system.txt`, `evaluation_report.md` (none listed for D2-059) not opened.

---

## Cross-cutting anomalies (source facts, no re-judging)

1. **Manifest vs item `kind` mismatch** — manifest.csv says `REUSE` for D2-055, D2-056, D2-058; their item JSONs say `NEW`. D2-054/057/059 agree (`REUSE`).
2. **Stale inherited verdict in manifest** — all six rows carry `"dual-build-PASS (inherited)"` with 2026-10-05/06 eval jobIds, yet D2-054's current verdict is `mismatched`, D2-055 is BLOCKED/WAITING with 0 model calls, and the rest are `semantic_pass`/`matched` from 2026-10-10/11 jobs. The column is not evidence of the current state.
3. **Missing conversion capture + `evaluator_manifest.json` for D2-056 and D2-058** — both lack the entire `02-conversion/` subtree (no request system prompt, no model response body, no observed-source streams) and lack `output/batch/evaluator_manifest.json`, while item JSON asserts `usage.requests` 1 and CONVERTED/FROZEN DONE dispositions. D2-058 additionally lacks `self-review-1.model.json` and `review.system.txt`; D2-056 lacks `self-review-1.model.json`.
4. **Missing `result.md` for D2-055** — only `01-frozen/{frozen-inputs.md, classification-1.json, classifier-input.json}` exist. Delivery contract §1.1 requires a report at every terminal/blocked/WAITING exit.
5. **Precheck reports carry a `mismatched` behaviourVerdict against a placeholder target** (D2-054 job-00 and D2-056 job-00, target buildCommand `Get-Content placeholder.txt`). These are precheck artefacts; item JSON correctly cites only build/execution. Risk: a reader scanning `evaluation_report.json` alone could misread the precheck as a behaviour FAIL.
6. **Cross-case copy-paste in D2-054 job-01 `batch-authorization.json`** — `dataSource.confirmation` refers to “该项 **D2-088**”, not D2-054.
7. **caseId naming drift** — D2-056 uses `batch-d2-056-go-to-powershell-staged-config[-precheck]`; D2-058 uses `batch-d2-058-go-to-python-child-cmd[-precheck]` and `…-child-cmd-v2`; D2-054/057/059 use bare `D2-0xx`. Job-02 of D2-058 additionally supersedes job-01 by an explicit `supersedes` block.
8. **`target.gen.model.json` bodies lack envelope metadata** — for D2-054/057/059 the model file has only `role`/`content`/`reasoning_content`; `model`, `finish_reason`, `usage` and hashes live only in `self-review-*.model.json` and the item JSON. So "metadata-only vs real body" resolves to: real body, but not a complete response envelope.
9. **Classifier false positive left unactioned (D2-055)** — `classification-1.json` shows `network: []` while asserting `network_mode: hostname` on `demo.txt` line 13 (a `filepath.Join` filename). Correctly recorded as fact and not downgraded; it remains a reproducible heuristic defect worth a classifier-tuning knowledge entry.
10. **`casePath` vs actual copy path** — every item's `casePath` points at `docs/test/dataset-2/...`; the reviewed artefacts live under `docs/dataset-2/dataset-2-copy/...`.

## Knowledge candidates + current-contract coverage (path + section)

| Candidate (from these items) | Current-contract coverage (verified header present) | Disposition-file cluster |
|---|---|---|
| Driver post-processing must be symmetric across both sides; branch-by-target-form manufactures false FAILs (D2-058 job-01) | `references/framework/evaluation-readiness-contract.md` §2 驱动来源与四要素; §4 oracle 与两侧对称 | K-W |
| A real-measurement/active-counter field (`duration_ms`, `time.Since`) cannot be frozen by text noise tokens (D2-054) | `references/framework/evaluation-readiness-contract.md` §4; §5 原始观察、采信与归因 | K-O |
| Timestamp value noise vs timestamp *format* semantics must be separated; RFC3339 `Z` for zero offset (D2-056/057/059) | `references/framework/evaluation-readiness-contract.md` §5; language pages (go/python) | K-O |
| Launch-failure and non-zero-exit branches need legal drivers; wording differs by language (D2-058/054) | `references/framework/evaluation-readiness-contract.md` §2; `references/framework/delivery-handoff-contract.md` §2.3 `result.md` | K-U / K-E |
| Classifier `hostname` heuristic captures local filename literals → false positive (D2-055) | `references/workflow/classifier-agent-gate.md` §2 (verdict authoritative) | — (classifier tuning) |
| Every terminal/blocked/WAITING item still owes a `result.md` (D2-055) | `references/framework/delivery-handoff-contract.md` §1.1 统一收尾入口与报告义务 (header line 13) | — |
| Freeze record version/reuse boundaries consumed by requests/jobs (all items) | `references/framework/task-state-contract.md` §2.1 版本关联与复用边界; §2.2 冻结落盘门禁 (lines 30, 45) | — |
| `evaluator_manifest.json` field-source discipline / skeleton (D2-054/057/059 only) | `references/framework/delivery-handoff-contract.md` §2.1.1 (line 43); §3 (line 222) | — |

I did not edit any knowledge source; the disposition file (`…/current-system-review-2026-10-12/full-review-knowledge-disposition.md`) already records the K-A…K-AA clusters and explicitly says it added review docs only.

## Optimization observations (reviewer opinion)

- Batch hygiene: reconcile manifest `kind`/status columns with item JSON before any statistics (anomalies 1–2). A stale “inherited PASS” is the same failure mode the project notes for a single source-side contract error copied across a batch.
- Delivery integrity: restore or explicitly mark as UNVERIFIED the missing `02-conversion/` captures and `evaluator_manifest.json` for D2-056/D2-058, and the missing `result.md` for D2-055 (per delivery contract §1.1/§2.1/§3), before those items are counted DONE.
- Evidence strength: prefer a platform filesystem dimension over driver echo for side-effect files (D2-056, D2-058); keep behaviour verdicts (`semantic_pass` vs `matched`) in separate counters, as all three semantic-pass items already state.
- Precheck artefacts should be visually distinguishable from dual-build reports to prevent the placeholder-target `mismatched` being read as a behaviour result (anomaly 5).

## Unknowns / limits of this pass

- No source tree, no `target/` tree, no `run_case.py` and no `batch/events.jsonl` / reconciliation files were read; `casePath` (`docs/test/...`) was not followed.
- All single-line platform bundles are truncated at 2000 chars by the harness; the tail of each (e.g. `artifacts[]`, trailing `obse…`, longest `normalizedText`) is unread, so no claim is made about fields beyond the visible prefix.
- Job-root health/authorization/input-profile files and `review.system.txt` for several items remain `unread`; absence claims rely on exhaustive `**/*` glob per item directory.
- 2 attempted reads returned “not found”: D2-054 job-01 `returned-evidence/controller-health-before.json` and `…/controller-health-after.json` (the actual files live at the job root, which were then read).
