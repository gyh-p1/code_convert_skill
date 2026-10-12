# Harness A — cases 14 (D2-048 … D2-053) static document review

Reviewer: read-only static reviewer (native read/glob/grep only). No file except this one was written; nothing was executed.
Scope: 6 assigned items under `docs/dataset-2/dataset-2-copy/`. All artifacts of the assigned item directories were read.
Limitations:

- Single-line platform bundles (`evidence-*.json`, `comparison.json`, `evaluation_report.json`, `controller-health*.json`) are truncated at 2000 chars by the read/grep tools; there is no byte-offset read and pwsh is unavailable in this sandbox. Those files are registered `read(截断>2000)`; their tail (mostly `observations`, `artifacts[].digest`, `collectorDiagnostics`) is NOT retrievable.
- The reviewed trees contain **only** `output/batch/**`. `source/*.go`, `run_case.py` and `target.*` are not present in this copy, so declared source/target hashes could not be independently recomputed.
- Model internal reasoning is not treated as a self-review conclusion; a metadata-only `*.model.json` is not treated as a complete response.
- `docs/dataset-2/dataset-2-copy/go-to-*/…/output/batch/result.md` are the item-level reports; batch-level evidence was cross-checked against `batch/manifest.csv`, `batch/events.jsonl`, `batch/platform-blocker-csharp-target.md`, `batch/summary.md` only.

Counts: 6 items; 106 existing artifacts read (13 of them `read(截断>2000)`, 1 empty); 0 directories found empty-by-proof except two proved empty (`02-conversion`, `03-self-review` under D2-048) and one proved empty (`02-conversion` under D2-052).

---

## D2-048 — go-to-csharp / autorun_manifest_write.go

1) Identity

- taskId `D2-048` ｜ rawItemId `D2-048` ｜ batchId `batch` ｜ kind `REUSE` ｜ direction `go-to-csharp`
- sourceFile `autorun_manifest_write.go` ｜ declared Sha256 `320de55b2f4d0cc06d789809fa02a78777338f00ec9f7112ddbf45a1c6d7e2d2` (manifest.csv line 48: `320DE55B…E2D2`, identical, uppercase)
- casePath (item) `docs/test/dataset-2/go-to-csharp/handoff-2026-10-02-d27-autorun-manifest-write-go`; reviewed location `docs/dataset-2/dataset-2-copy/go-to-csharp/handoff-2026-10-02-d27-autorun-manifest-write-go`
- item-json: disposition `FROZEN`, phase `CLOSED`, lifecycle `WAITING`, pendingAction `"platform fix for csharp evidence-bundle schema; then resubmit same capsule"`, blockingReasons `["BLOCKED_ENV"]`, targetSha256 `null`
- usage: requests `1` ("classification + source-side precheck only; NO conversion model call"), codeRevisions `0`, selfRepairRounds `0`, evaluation `null`
- manifest.csv row 48: Kind REUSE, Origin `dataset/go-to-csharp/handoff-2026-10-02-d27-autorun-manifest-write-go`, JobId `eval-20261005-080811-e6b394d1`, Evidence `dual-build-PASS (inherited)`

2) File inventory (relative to the handoff dir)

```
output/batch/01-frozen/classifier-input.json = read
output/batch/01-frozen/classification-1.json = read
output/batch/01-frozen/frozen-inputs.md = read
output/batch/04-evaluation/job-00-source-buildability/job-id.txt = read
output/batch/04-evaluation/job-00-source-buildability/metadata.json = read
output/batch/04-evaluation/job-00-source-buildability/input_profile.json = read
output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json = read
output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json = read
output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json = read  (wrong-task-id text: names D2-088)
output/batch/04-evaluation/job-00-source-buildability/controller-health-before.json = read
output/batch/04-evaluation/job-00-source-buildability/runners-before.json = read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json = read(截断>2000)
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json = read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/controller.log = read
output/batch/02-conversion = dir-empty (read -> "not a regular file"; glob -> 0)
output/batch/03-self-review = dir-empty (read -> "not a regular file"; glob -> 0)
output/batch/result.md = missing
output/batch/evaluator_manifest.json = missing
output/batch/04-evaluation/job-01-dual-build = missing (absent)
target artifact (target.cs) = missing
source/*.go, run_case.py = missing in this copy
```

3) Condensed findings

- Freeze/classify: `frozen-inputs.md` (39 lines) is complete and self-consistent (taskId/direction/kind, sourcePath/sha/bytes 516/lines 18, `sourceLang/sourceStd Go/Go 1.27`, `targetLang/targetStd C#/C# 12 (.NET 8)`, sourceOs linux, targetOs windows x64, model `deepseek-flash` temp 0.2 RAG off, selected skills `go-to-csharp` + `languages/{go,csharp}` + seven-language-common-semantics + `scenes/file-io`, sceneTags file-io, taskMode short single file). `classifier-input.json` carries the same id/sha. `classification-1.json`: cls `REVIEW_SIDE_EFFECTS`, reason `local_effects_require_review`, `admissionStatus ALLOWED`, `blockingReason null`, classifier 2.4 sha `009a6f31…`; files `autorun_manifest_write.go` (fs signals lines 12,16; has_file_ops true) and `run_case.py` sha `63f8aaf2…` (process 1,21,22). `this-task-classification.json` is the same object with `inputManifestSha256 0d6c10ff…`.
- Source precheck (job-00 only): jobId `eval-20261011-100423-8bc77d85` ｜ os linux ｜ `comparison_manifest.json` source `buildCommand go build -o program autorun_manifest_write.go`, `runCommand python run_case.py`; target `artifactLanguage csharp`, `os windows`, `buildCommand dotnet build -c Release -o . target.csproj`. `input_profile.json`: argv `[]`, stdin null, timeout 30, wd `workspace`, dimensions `["output"]`, stdoutMode normalized-text / stderrMode exact.
- Evidence (`evidence-source.json`, bundle `evb-source-eval-20261011-100423-8bc77d85`): source build `completed/exitCode 0` 5887 ms, stdout/stderr empty (digest `e3b0c442…` = empty SHA-256); execution `completed/0` 33 ms, stdout `artifact: /tmp/safe-attck-go/05_persistence/autorun-manifest.json\n` (66 bytes, digest `13ff2818…`), stderr empty. `evaluation_report.json`: `jobStatus COMPLETED`/`jobPhase FINISHED`; source lifecycle preflight+cleanup `PASSED` attempts 1, `contaminated false`, `environmentStatus clean`, `runnerStateAfter READY`; target run `os windows`, runner `windows-vm-agent-x64`, `execution.performed true`; outcome `runVerdict not-runnable`, `codeVerdict failed`, `behaviorVerdict inconclusive`, failure `{type CODE_RESULT, reason "Target build failed."}`, coverage `applicableDimensions 0 / coverageRatio 0.0`.
- `controller.log`: job created 2026-10-11T10:04:23Z, finished 10:05:37Z (74 s).
- Requests/responses: **none** — no `02-conversion` artifacts at all (dir present but empty). Consistent with the item's "NO conversion model call".
- Self-review: **absent** (`03-self-review` dir exists, empty); no `self-review-*.json`, no model call.
- Jobs: only `job-00-source-buildability`; no `job-01-dual-build`, no target evidence bundle. Cleanup: preflight/cleanup PASSED on both runs, `contaminated false`.
- `result.md` absent ｜ `evaluator_manifest.json` absent.
- Anomalies: (a) item-json `verdicts.targetBuild = "UNVERIFIED (… preflight SKIPPED, never attempted)"` and frozen-inputs.md line 30/26 say the target is a placeholder/preflight skipped, but the returned `evaluation_report.json` shows the target **was performed** and failed with `"Target build failed."` and both target preflight/cleanup PASSED — label contradicts evidence; (b) `batch-authorization.json` `dataSource.confirmation` names **"该项 D2-088"** (wrong task id; same string in D2-049/050/051); (c) manifest.csv still records an inherited jobId `eval-20261005-080811-e6b394d1` and `dual-build-PASS (inherited)`, inconsistent with the current no-dual-build/WAITING state; (d) blocker is **stale**: `batch/platform-blocker-csharp-target.md` (updated 2026-10-11) declares the C# evidence-bundle defect fixed ("已修复…不必再记 WAITING/BLOCKED_ENV", retest job `eval-20261011-122249-fe456bbe` COMPLETED with target build/exec completed/0), and `batch/summary.md` line 527 lists `D2-007~012, 030, 048~051, 065, 076~078, 156~160` as "恢复条件已具备" with recovery = full chain re-run — not yet done for D2-048; (e) no `result.md` while `summary.md` §reconciliation requires per-item reporting.
- Independent evidence facts: source side is independently confirmed `build completed/0` and `exec completed/0` with non-empty stdout; no target-side fact of any kind exists beyond the placeholder failure.
- Attribution: source PASS = source-existing behavior on a clean apparatus; "Target build failed" and the absent target bundle = **apparatus** (placeholder target + retired platform schema defect), NOT conversion-introduced (no target code was ever generated); the meter/`artifact:` path is environment (linux `/tmp`).
- Knowledge / self-review suggestions: none (no self-review ran). The one rule this case touches — C# capsule identity requires `target.artifactLanguage = csharp` (not `dotnet`) — is **already covered** by `batch/platform-blocker-csharp-target.md` §新纪律, and this item's `comparison_manifest.json` already uses `csharp` (compliant).
- Optimization: re-open per summary.md:527 (re-classify → source precheck → generate → self-review → dual submit → evidence), then write `result.md` and update the manifest row jobId/Evidence; fix the `D2-088` copy-paste.
- Unknowns: whether the original job ever produced the documented INFRA_ERROR/CLEANING signature (the stored report shows a plain code failure instead); why item-json records "preflight SKIPPED".

---

## D2-049 — go-to-csharp / iface_env_inventory.go

1) Identity

- taskId `D2-049` ｜ kind `REUSE` ｜ direction `go-to-csharp` ｜ sourceFile `iface_env_inventory.go` ｜ declared Sha256 `671214506e1cbb6f9818d9936f6a484a026ea14f2d6bfede6f3126d626c450dd` (manifest.csv line 49 `671214506E1CBB6F…C450DD`, identical)
- casePath `docs/test/dataset-2/go-to-csharp/handoff-2026-10-02-d27-iface-env-inventory-go`
- item-json: disposition `FROZEN`, phase `CLOSED`, lifecycle `WAITING`, pendingAction "platform fix for csharp evidence-bundle schema; then resubmit same capsule", blockingReasons `["BLOCKED_ENV"]`, targetSha256 `null`, usage requests `1` (no conversion call), codeRevisions 0, selfRepairRounds 0
- manifest.csv row 49: REUSE, JobId `eval-20261009-034434-9a9f057f`, Evidence `dual-build-PASS (inherited)`

2) File inventory

```
output/batch/01-frozen/classifier-input.json = read
output/batch/01-frozen/classification-1.json = read
output/batch/01-frozen/frozen-inputs.md = missing (read -> "not found")
output/batch/04-evaluation/job-00-source-buildability/job-id.txt = read
output/batch/04-evaluation/job-00-source-buildability/metadata.json = read
output/batch/04-evaluation/job-00-source-buildability/input_profile.json = read
output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json = read
output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json = read
output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json = read  (wrong-task-id text: names D2-088)
output/batch/04-evaluation/job-00-source-buildability/controller-health-before.json = read
output/batch/04-evaluation/job-00-source-buildability/runners-before.json = read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json = read(截断>2000)
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json = read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/controller.log = read
output/batch/result.md = missing
output/batch/evaluator_manifest.json = missing
output/batch/04-evaluation/job-01-dual-build = missing
target artifact (target.cs) = missing
02-conversion / 03-self-review dirs = no files (glob); empty-vs-absent not proven for this item
```

3) Condensed findings

- Freeze/classify: **`01-frozen/frozen-inputs.md` is missing** (the §3 freeze gate requires it before classification) — the only C# item of the four that has it is D2-048. `classifier-input.json` (id/sha `671214506E1CBB6F…C450DD`) and `classification-1.json` are present: cls `REVIEW_SIDE_EFFECTS`, reason `local_effects_require_review`, ALLOWED, blockingReason null, classifier 2.4 sha `009a6f31…`; signals `iface_env_inventory.go` filesystem lines 34,74,84 + discovery line 56; `run_case.py` sha `63f8aaf2…`; `inputManifestSha256 8b11a983…`. `this-task-classification.json` matches (same inputManifestSha256).
- Source precheck (job-00): jobId `eval-20261011-100623-18067cda` ｜ os linux ｜ build `go build -o program iface_env_inventory.go` ｜ run `python run_case.py`; target manifest `csharp`/windows/`dotnet build -c Release -o . target.csproj`. `input_profile.json` argv `[]`, timeout 30, dimension output.
- Evidence: source build `completed/0` 7475 ms, empty stdout/stderr; execution `completed/0` 34 ms, stdout two artifact lines (`/tmp/safe-attck-go/01_recon/advanced-host-info.json`, `…/advanced-summary.txt`), 121 bytes, digest `52e1cb2b…`, stderr empty. `evaluation_report.json` identical in shape to D2-048: COMPLETED/FINISHED, source clean/READY, target performed (windows), `not-runnable` / `codeVerdict failed` / `behaviorVerdict inconclusive`, reason `"Target build failed."`, coverage 0.0. `controller.log`: created 10:06:23Z, finished 10:07:33Z.
- Requests/responses: none. Self-review: none.
- Jobs: only job-00; no job-01, no target bundle. Cleanup PASSED both sides, `contaminated false`.
- `result.md` absent ｜ `evaluator_manifest.json` absent.
- Anomalies: missing `frozen-inputs.md` (freeze-落盘 gate unmet for this item while classification proceeded); `D2-088` wrong id in `batch-authorization.json`; item-json "preflight SKIPPED / UNVERIFIED" vs returned report showing a performed target run that failed; manifest row still `dual-build-PASS (inherited)` with a 2026-10-09 jobId; stale `BLOCKED_ENV` (see D2-048 (d), summary.md:527 explicitly lists D2-049 in the recoverable set).
- Independent evidence facts: source build/exec completed/0 with two real artifact lines; no target fact.
- Attribution: source PASS source-existing/apparatus-clean; the target failure and missing target bundle = apparatus (placeholder target; retired platform defect).
- Knowledge: none from a self-review; the `artifactLanguage=csharp` rule is already in `platform-blocker-csharp-target.md` and is complied with.
- Optimization: write the missing `frozen-inputs.md` only if a genuine re-freeze is performed (do not back-fill a historical run), then run the recovery chain and write `result.md`.
- Unknowns: whether a frozen-inputs record exists elsewhere for D2-049; whether `02-conversion`/`03-self-review` dirs exist but are empty.

---

## D2-050 — go-to-csharp / tcp_port_scanner.go

1) Identity

- taskId `D2-050` ｜ kind `REUSE` ｜ direction `go-to-csharp` ｜ sourceFile `tcp_port_scanner.go` ｜ declared Sha256 `573b6071a4ce1793d6d5b34d77fe573d3acf6cb124282981cc7cf4c56e8b4a76` (manifest.csv line 50 `573B6071A4CE1793…8B4A76`, identical)
- casePath `docs/test/dataset-2/go-to-csharp/handoff-2026-10-02-d27-tcp-port-scanner-go`
- item-json: disposition `FROZEN`, phase `CLOSED`, lifecycle `WAITING`, blockingReasons `["BLOCKED_ENV"]`, targetSha256 `null`, usage requests `1` (no conversion call), codeRevisions 0, selfRepairRounds 0; classifier cls `REVIEW_NETWORK`
- manifest.csv row 50: REUSE, JobId `eval-20261006-094827-9c99e429`, Evidence `dual-build-PASS (inherited)`

2) File inventory

```
output/batch/01-frozen/classifier-input.json = read
output/batch/01-frozen/classification-1.json = read
output/batch/01-frozen/frozen-inputs.md = missing
output/batch/04-evaluation/job-00-source-buildability/job-id.txt = read
output/batch/04-evaluation/job-00-source-buildability/metadata.json = read
output/batch/04-evaluation/job-00-source-buildability/input_profile.json = read
output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json = read
output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json = read
output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json = read  (wrong-task-id text: names D2-088)
output/batch/04-evaluation/job-00-source-buildability/controller-health-before.json = read
output/batch/04-evaluation/job-00-source-buildability/runners-before.json = read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json = read(截断>2000)
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json = read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/controller.log = missing
output/batch/result.md = missing
output/batch/evaluator_manifest.json = missing
output/batch/04-evaluation/job-01-dual-build = missing
target artifact (target.cs) = missing
02-conversion / 03-self-review dirs = no files (glob); empty-vs-absent not proven
```

3) Condensed findings

- Freeze/classify: `frozen-inputs.md` missing again. `classification-1.json`: cls `REVIEW_NETWORK`, reason `network_scope_and_inputs_require_review`, ALLOWED, blockingReason null, classifier 2.4; `tcp_port_scanner.go` network signal line 69, `network_mode loopback`, `network_targets [{value 127.0.0.1, line 26, scope loopback, provenance literal, redirectVerified false}]`, has_network true; `run_case.py` sha `63f8aaf2…`; `inputManifestSha256 471982ed…`. `this-task-classification.json` matches.
- Source precheck (job-00): jobId `eval-20261011-100814-40f80e9b` ｜ build `go build -o program tcp_port_scanner.go` ｜ linux. Evidence: build `completed/0` 7724 ms, empty out/err; execution `completed/0` 37 ms, stdout `Scanning 127.0.0.1 (ports: 1-100) with 10 workers...\nPort 22 open\n\nOpen ports:\n  22\n` (84 bytes, digest `25a2bae7…`), stderr empty. `evaluation_report.json`: COMPLETED/FINISHED, source clean/READY, target windows performed, `not-runnable`/`failed`/`inconclusive`, reason `"Target build failed."`, coverage 0.0.
- `controller.log` is **missing** for this item's job-00 (present for D2-048/D2-049) — the only C# item without a job-level time log.
- Requests/responses: none. Self-review: none. Jobs: only job-00; no job-01, no target bundle. Cleanup PASSED both sides, `contaminated false`.
- `result.md` absent ｜ `evaluator_manifest.json` absent.
- Anomalies: missing `frozen-inputs.md`; missing `controller.log`; `D2-088` wrong id in `batch-authorization.json`; "preflight SKIPPED/UNVERIFIED" vs a performed failing target run in the returned report; inherited manifest jobId (`eval-20261006-…`) + `dual-build-PASS (inherited)` inconsistent with the current state; stale `BLOCKED_ENV` (summary.md:527 lists D2-050 as recoverable).
- Independent evidence facts: source build/exec completed/0 with genuine loopback scan output (port 22 open on the isolated runner); no target fact. Note: this is a loopback-only scan inside the isolated VM (`redirectVerified false`), i.e. no public-network evidence either way.
- Attribution: source PASS source-existing/apparatus-clean; target failure + absent target = apparatus.
- Knowledge: no self-review suggestions. The loopback-only target detail (`127.0.0.1`, lines 26/69) confirms the classifier's `REVIEW_NETWORK` classification, which matches the network-scene expectations; no knowledge gap identified.
- Optimization: same recovery chain as D2-048/049; restore the job-00 controller.log by re-submission (do not fabricate).
- Unknowns: why no controller.log was persisted for this job.

---

## D2-051 — go-to-csharp / workspace_env_discovery.go

1) Identity

- taskId `D2-051` ｜ kind `REUSE` ｜ direction `go-to-csharp` ｜ sourceFile `workspace_env_discovery.go` ｜ declared Sha256 `2e31be2e72a19a9fdd7327a51eb446d661dbf6f0ceb81e7272888a590a2eef7d` (manifest.csv line 51 `2E31BE2E72A19A9F…A2EEF7D`, identical)
- casePath `docs/test/dataset-2/go-to-csharp/handoff-2026-10-02-d27-workspace-env-discovery-go`
- item-json: disposition `FROZEN`, phase `CLOSED`, lifecycle `WAITING`, blockingReasons `["BLOCKED_ENV"]`, targetSha256 `null`, usage requests `1` (no conversion call), codeRevisions 0, selfRepairRounds 0
- manifest.csv row 51: REUSE, JobId `eval-20261006-095344-d18acf2d`, Evidence `dual-build-PASS (inherited)`

2) File inventory

```
output/batch/01-frozen/classifier-input.json = read
output/batch/01-frozen/classification-1.json = read
output/batch/01-frozen/frozen-inputs.md = missing
output/batch/04-evaluation/job-00-source-buildability/job-id.txt = read
output/batch/04-evaluation/job-00-source-buildability/metadata.json = read
output/batch/04-evaluation/job-00-source-buildability/input_profile.json = read
output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json = read
output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json = read
output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json = read  (wrong-task-id text: names D2-088)
output/batch/04-evaluation/job-00-source-buildability/controller-health-before.json = read
output/batch/04-evaluation/job-00-source-buildability/runners-before.json = read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json = read(截断>2000)
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json = read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/controller.log = missing
output/batch/result.md = missing
output/batch/evaluator_manifest.json = missing
output/batch/04-evaluation/job-01-dual-build = missing
target artifact (target.cs) = missing
02-conversion / 03-self-review dirs = no files (glob); empty-vs-absent not proven
```

3) Condensed findings

- Freeze/classify: `frozen-inputs.md` missing. `classification-1.json`: cls `REVIEW_SIDE_EFFECTS`, reason `local_effects_require_review`, ALLOWED, blockingReason null, classifier 2.4; reviewGroups discovery+filesystem+process; `workspace_env_discovery.go` filesystem lines 14,37 + discovery line 22; `run_case.py` sha `63f8aaf2…`; `inputManifestSha256 ea39d7d3…`; `this-task-classification.json` matches exactly.
- Source precheck (job-00): jobId `eval-20261011-101003-d84e5fe2` ｜ build `go build -o program workspace_env_discovery.go` ｜ linux. Evidence: build `completed/0` 7386 ms empty out/err; execution `completed/0` 34 ms, stdout `artifact: /tmp/safe-attck-go/09_discovery/discovery.json\n` (57 bytes, digest `9bfd7d32…`), stderr empty. `evaluation_report.json`: COMPLETED/FINISHED, source clean/READY, target windows performed, `not-runnable`/`failed`/`inconclusive`, reason `"Target build failed."`, coverage 0.0.
- `controller.log` missing for this item too. Requests/responses: none. Self-review: none. Jobs: only job-00; no job-01/target bundle. Cleanup PASSED both sides, `contaminated false`.
- `result.md` absent ｜ `evaluator_manifest.json` absent.
- Anomalies: missing `frozen-inputs.md`; missing `controller.log`; `D2-088` wrong id in `batch-authorization.json`; item-json metadata note in `comparison_manifest.json` absent while D2-049's metadata carried the SKIPPED wording — here only the item-json says `UNVERIFIED (csharp evidence-bundle platform defect)` while the returned report shows a performed failing target run; manifest row inherited jobId/`dual-build-PASS (inherited)`; stale `BLOCKED_ENV` (summary.md:527).
- Independent evidence facts: source build/exec completed/0 producing `discovery.json`; no target fact. `events.jsonl` line 569 records a direction-level event `DIRECTION_BLOCKED_RANGE_DONE` for D2-048/049/050/051.
- Attribution: source PASS source-existing/apparatus-clean; target failure + absent target = apparatus.
- Knowledge: no self-review suggestions; the "discovery" signal group is already represented in the classifier output, consistent with the frozen skills selection (sceneTags file-io).
- Optimization: recovery chain + `result.md`; write logs by re-running rather than reconstructing.
- Unknowns: same as D2-050 (missing job log), plus whether the C# item set was meant to be re-opened before this review round.

### Cross-cutting note for D2-048…D2-051 (applies to all four)

`events.jsonl` lines 553–569 record CLASSIFICATION → SOURCE_PRECHECK → BLOCKED_ENV → TERMINAL(lifecycle WAITING) for each, and line 569 closes the direction range with "source side PASS for each; C# target platform defect". The **authoritative current rule** (`platform-blocker-csharp-target.md`, banner updated 2026-10-11: defect fixed, retest `eval-20261011-122249-fe456bbe` COMPLETED with target build/exec `completed/0`; "38 项 C# 目标项可恢复为正常推进，不必再记 WAITING/BLOCKED_ENV") plus `summary.md:527` ("恢复条件已具备；恢复动作 = 逐项跑全链") **contradict** the four items' `WAITING/BLOCKED_ENV` terminal records. All four item-json `pendingAction` strings still say "platform fix …", i.e. they were written against the pre-fix state and were never updated. This is a rule-vs-record conflict, not a conversion failure, and it is the single most actionable finding in this batch of four.

---

## D2-052 — go-to-powershell / inbox_kv_parse.go

1) Identity

- taskId `D2-052` ｜ kind `NEW` (item-json, `result.md`, job-01 metadata) — but manifest.csv line 52 says `REUSE` ｜ direction `go-to-powershell`
- sourceFile `inbox_kv_parse.go` ｜ declared Sha256 `b8f6038844bad10eb0e1e17e27ddf9a55bd9c301161e25ee6093f39f4841bde7` (manifest.csv line 52 `B8F60388…41BDE7`, identical) ｜ targetSha256 `096dc10e75b29bcd2feebbb2e6b315a1a9d346da5ae1cb3968d989cda556078a`
- casePath `docs/test/dataset-2/go-to-powershell/handoff-2026-10-02-d30-inbox-kv-parse-go`
- item-json: disposition `FROZEN`, phase `CLOSED`, lifecycle `DONE`, blockingReasons `[]`, evaluation.verdict `matched`, `digestsIdentical true`, `sizeBytesBoth 196`, `outputDiffs 0`, `coverageRatio 1`, `matchedDimensions 1`, `accepted true`, gate "passes discipline 10.6"
- usage: requests `1` ("one conversion call; self-review NO-REPAIR-IDENTIFIED"), codeRevisions 0, selfRepairRounds 0; classifier version **2.3** sha `441b4d50…` (D2-048…051/053 use 2.4/`009a6f31…`)
- manifest.csv row 52: REUSE, JobId `eval-20261005-073327-f2280eff`, Evidence `dual-build-PASS (inherited)`

2) File inventory

```
output/batch/01-frozen/classifier-input.json = read
output/batch/01-frozen/classification-1.json = read
output/batch/03-self-review/self-review-1.json = read
output/batch/04-evaluation/job-00-source-buildability-linux/comparison_manifest.json = read  (target build parses 'placeholder.txt')
output/batch/04-evaluation/job-00-source-buildability-linux/input_profile.json = read
output/batch/04-evaluation/job-00-source-buildability-linux/metadata.json = read
output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evaluation_report.json = read(截断>2000)
output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evidence-source.json = read(截断>2000)
output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json = read
output/batch/04-evaluation/job-01-dual-build/input_profile.json = read
output/batch/04-evaluation/job-01-dual-build/metadata.json = read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json = read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json = read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log = read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json = read(截断>2000)
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md = read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json = read(截断>2000)
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json = read(截断>2000)
output/batch/result.md = read
output/batch/02-conversion = dir-empty (read -> "not a regular file"; glob -> 0)
output/batch/target.ps1 = missing (read -> "not found")
output/batch/evaluator_manifest.json = missing
output/batch/04-evaluation/job-00-…/{job-id.txt,this-task-classification.json,batch-authorization.json,controller-health-before.json,runners-before.json,controller.log,returned-evidence/evidence-target.json} = missing
output/batch/04-evaluation/job-01-…/{job-id.txt,this-task-classification.json,batch-authorization.json,controller-health-before.json,runners-before.json} = missing
source/*.go, run_case.py = missing in this copy
```

3) Condensed findings

- Freeze/classify: no `frozen-inputs.md`; `classifier-input.json` binds `source/inbox_kv_parse.go` sha `b8f60388…`; `classification-1.json`: cls `REVIEW_SIDE_EFFECTS`, reason `local_effects_require_review`, ALLOWED, blockingReason null, **classifierVersion 2.3** sha `441b4d50…`; single file classified (only `inbox_kv_parse.go`, filesystem signals lines 14,16,18,28, has_file_ops true) — **`run_case.py` is NOT in the classified file set** (unlike D2-048…051/053, where the driver is classified), while the jobs nonetheless ran `python run_case.py`; `inputManifestSha256 6ed4e691…`.
- Requests/responses: **none preserved**. There is no `02-conversion` directory content at all (dir exists, proved empty), yet item-json declares `requests: 1`, an actual conversion call, and a `targetSha256`; `events.jsonl` line 172 records `MODEL_CONVERSION outcome converted sha256 096dc10e…`. So the conversion request prompt and the raw model response (and any usage/finish_reason metadata) are **missing** for D2-052. Consequently the generated `target.ps1` is also absent from the reviewed tree; only its hash is declared.
- Self-review: `03-self-review/self-review-1.json` — `reviewer: agent-static`, verdict `NO-REPAIR-IDENTIFIED`; 7 named checks (payload-bytes UTF-8 no BOM; TrimSpace + `-split "\`n"`; `SplitN(line,"=",2)` → `-split '=', 2`; Go `map` key order → `StringComparer.Ordinal`; Go `encoding/json` HTML/control escaping; empty-map `{}`; no trailing newline; artifact line); `residualRisks` 3 (HTML/control escape branch implemented but unexercised; empty-map branch unexercised; utf8noBOM asserted by construction not observed); `limitations: "static review only; not compilation and not behaviour evidence"`; `decision: proceed to evaluation-ready check`. There is **no `*.model.json`** for this review, i.e. the self-review was not a model call (consistent with `requests: 1`).
- Jobs: job-00 dir `job-00-source-buildability-linux` — jobId (from bundles) `eval-20261010-064625-a126697d`; `comparison_manifest.json` caseId `batch-d2-052-go-to-powershell-inbox-kv-precheck`, source `go build -o program inbox_kv_parse.go` (linux), target `artifactLanguage powershell` (linux) with `buildCommand pwsh -NoProfile -Command "…ParseFile('placeholder.txt'…)"` — i.e. the "precheck" job actually ran a **placeholder** target. `evidence-source.json` (bundle `evb-source-eval-20261010-064625-a126697d`): source build `completed/0` 5724 ms empty out/err; execution `completed/0` 34 ms stdout `artifact: /tmp/safe-attck-go/03_initial_access/parsed.json\n` 59 bytes digest `96311aa3…`, stderr empty; snapshot `CC-Eval-Linux-8Lang-1.0.26`. `evaluation_report.json`: COMPLETED/FINISHED, both runs preflight/cleanup PASSED clean READY, but outcome `runVerdict partial-runnable`, `codeVerdict failed`, `behaviorVerdict mismatched` (placeholder target), `mismatchedDimensions 1`, coverage 1.0, failure `{category behavior, "At least one critical mismatch…"}`.
- job-01 `job-01-dual-build` — jobId `eval-20261010-064922-9ae5c05d`; metadata: kind NEW, sourceLang Go/targetLang PowerShell, `sourceSha256 B8F60388…`, `targetFile target.ps1`, `targetOrigin "deepseek-flash (project .env model); agent did not author target code"`, `sourcePrecheckJobId eval-20261010-064625-a126697d`, frozenArgv `[]`, frozenStdin null, oracleBasis = source-precheck artifact line, driverNote "driver resolves the artifact on one shared path and applies identical post-processing to both sides", deterministic true; `comparison_manifest.json` target build parses `target.ps1` (linux/powershell).
- job-01 evidence: `evidence-source.json` (bundle `evb-source-…9ae5c05d`, caseId `batch-d2-052-go-to-powershell-inbox-kv`): build `completed/0` 5459 ms; execution `completed/0` 36 ms stdout = artifact line + `--- inbox/payload.txt ---` + `operator=translator\nmode=controlled` + `--- parsed.json ---` + the two-key JSON, 196 bytes, digest `sha256:847d0ce68c7de0ac362c8380528868b91d2fe0b25ac5f7a2e147ea4d09a228ef`, stderr empty. `evidence-target.json`: build `completed/0` 4483 ms (pwsh parse), execution `completed/0` 671 ms, **byte-identical normalized stdout**, same digest, same 196 bytes, empty stderr, `artifactLanguage powershell`, `workspaceRef workspace/target`. `comparison.json`: `behaviorVerdict matched`, `dimensions.output {matched, applicable true, observed true, diffs []}`, filesystem/processes/registry/network all `not-applicable`. `evaluation_report.json`: `jobStatus COMPLETED`, `runVerdict runnable`, `codeVerdict passed`, `behaviorVerdict matched`, environment clean, coverage 1.0; `evaluation_report.md` (77 lines) renders the same ("Conversion result: PASS / Behavior: MATCHED / Environment: CLEAN") and states the JSON artifacts remain authoritative.
- `controller.log` (job-01): created 2026-10-10T06:49:22Z, finished 06:50:35Z. `controller-health-after.json`: status ok, `contractSetHash sha256:e088a356b48fd1c3f50e480ac24c2fd03319dc60a49b41de4d076219819c4c45`, runnerReadiness 3 ready/0 blocked at 06:51:01Z.
- `result.md` present (57 lines): matches the artifacts; layer table (delivery complete, target syntax/compile PASS via `pwsh` parse, source baseline PASS, execution PASS, behavior `matched` 0 diffs, environment clean, safety ALLOWED); lists the 5 coverage gaps (HTML/control escapes, empty map, line-without-`=`, read-failure/permission bits, linux runner only) and notes the digest+byte-count identity as the round's strongest evidence. `evaluator_manifest.json` absent.
- Anomalies: (a) **contract-set hash differs across rounds** — D2-052 job-01 health `e088a356…` (2026-10-10, snapshot 1.0.26) vs all D2-048…051/D2-053 records `a9ed1445…` (2026-10-11, snapshot 1.0.28); both are internally consistent per item, but the round-level contract hash changed; (b) kind mismatch manifest `REUSE` vs item `NEW`; (c) classifier version 2.3 vs 2.4 elsewhere and the driver `run_case.py` was not part of the classified set; (d) job-00 (labelled "source precheck") actually executed a placeholder target and its report says `mismatched` — that verdict must not be read as a conversion result, and it is stored inside the "source-buildability" evidence dir; (e) job-00 lacks job-id.txt/classification/authorization/health/runners/log; job-01 lacks job-id.txt/classification/authorization/health-before/runners; (f) **no conversion request/response artifacts** and **no target.ps1** in the reviewed tree; (g) manifest row still shows an inherited 2026-10-05 jobId and `dual-build-PASS (inherited)` while the real dual-build job is `eval-20261010-064922-9ae5c05d`; (h) coverage gaps are recorded (5) and honest, incl. "only the linux runner was covered".
- Independent evidence facts: both sides' stdout digests are identical and both are 196 bytes (strong oracle); both build statuses completed/0; both stderr empty; comparison has 0 diffs on the only applicable dimension (output). Not independently verifiable here: the declared `targetSha256` (no target file).
- Attribution: the matched behavior is a genuine conversion-level result for the covered path (target output reproduced byte-for-byte). The `mismatched` verdict in job-00 is **apparatus** (placeholder target). The missing conversion request/response and target artifact are **delivery-record gaps** (apparatus/process), not conversion defects. `filesystem` dimension `not-applicable` despite both sides really writing `inbox/payload.txt` and `parsed.json` is an **apparatus** observation-policy limitation (dimensions fixed to `["output"]`), not a code issue; side-effect equality is nevertheless visible inside stdout.
- Knowledge candidates: the model implemented Go `encoding/json` HTML escaping (`<`,`>`,`&` → `\u003c` etc.) unprompted — the self-review flags it as implemented-but-unexercised, which is the correct disposition. The "driver must resolve the artifact on one shared path and apply identical post-processing to both sides" rule is already applied here and already documented (job-01 metadata `driverNote`, discipline §10.13) — contract already covers it.
- Optimization: preserve the conversion request/response (or a hash+usage record) for every item; keep the `target.ps1` artifact with the batch output; align manifest kind/jobId; record the self-review as agent-static vs model explicitly in item-json.
- Unknowns: content of the conversion prompt/response; whether the model response included usage/finish_reason; whether `evaluation_report.md` for job-01 was produced by the platform or hand-rendered (the text says it is rendered from the canonical report).

---

## D2-053 — go-to-powershell / overwrite_rollback_check.go

1) Identity

- taskId `D2-053` ｜ kind `REUSE` ｜ direction `go-to-powershell` ｜ sourceFile `overwrite_rollback_check.go`
- source Sha256 `be92e03bf273500d1b2f28198ecf32834cf3d25eaf9a43dfca2d615b4f4e2b4c` (manifest.csv line 53 `BE92E03B…4E2B4C`, identical) ｜ target Sha256 `a796d4942509928adb486af9c8800657b9cd0118ff112d7e1b6bc68e602b644c` (matches `result.md`, `evaluator_manifest` jobId block, events line 573, job-01 metadata `targetHash`)
- casePath `docs/test/dataset-2/go-to-powershell/handoff-2026-10-02-d30-overwrite-rollback-check-go`
- item-json: disposition `CONVERTED`, phase `CLOSED`, lifecycle `DONE`, pendingAction null, blockingReasons `[]`, evaluation.verdict `matched`, `digestsIdentical true`, `accepted true`, `usage {requests 2, promptTokens 4444, completionTokens 35443, reasoningTokens 33795, totalTokens 39887, model deepseek-flash, failedAttempts 0}`; classifier version 2.4 sha `009a6f31…`, note "re-classified after correcting source/run_case.py"
- identityEvent in item-json: first POST `403 identity_mismatch` (source/run_case.py replaced after classification), fix = re-classify with corrected driver sha `aeba7540b11653a4…`, then POST returned 202; rejected attempt kept as `04-evaluation/job-00-source-buildability/attempt-1-403.json`
- manifest.csv row 53: REUSE, JobId `eval-20261006-095722-a3d116e8`, Evidence `dual-build-PASS (inherited)`

2) File inventory

```
output/batch/01-frozen/classifier-input.json = read
output/batch/01-frozen/classification-1.json = read
output/batch/01-frozen/frozen-inputs.md = missing
output/batch/02-conversion/observed-source-stderr.txt = empty (0 lines)
output/batch/02-conversion/observed-source-stdout.txt = read  (10-line report)
output/batch/02-conversion/request.system.txt = read
output/batch/02-conversion/target.gen.model.json = read(截断>2000)  (real body: assistant content + reasoning_content)
output/batch/03-self-review/review.system.txt = read
output/batch/03-self-review/self-review-1.json = read
output/batch/03-self-review/self-review-1.model.json = read  (metadata-only: no body)
output/batch/04-evaluation/job-00-source-buildability/attempt-1-403.json = read  (identical to submission-3.json)
output/batch/04-evaluation/job-00-source-buildability/submission-3.json = read  (403 identity_mismatch)
output/batch/04-evaluation/job-00-source-buildability/submission-4.json = read  (jobId + QUEUED)
output/batch/04-evaluation/job-00-source-buildability/job-id.txt = read
output/batch/04-evaluation/job-00-source-buildability/metadata.json = read
output/batch/04-evaluation/job-00-source-buildability/input_profile.json = read
output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json = read
output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json = read
output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json = read  (wrong-task-id text: names D2-088)
output/batch/04-evaluation/job-00-source-buildability/controller-health-before.json = read
output/batch/04-evaluation/job-00-source-buildability/runners-before.json = read
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json = read(截断>2000)
output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json = read(截断>2000)
output/batch/04-evaluation/job-01-dual-build/job-id.txt = read
output/batch/04-evaluation/job-01-dual-build/metadata.json = read
output/batch/04-evaluation/job-01-dual-build/input_profile.json = read
output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json = read
output/batch/04-evaluation/job-01-dual-build/this-task-classification.json = read
output/batch/04-evaluation/job-01-dual-build/batch-authorization.json = read  (wrong-task-id text: names D2-088)
output/batch/04-evaluation/job-01-dual-build/controller-health-before.json = read
output/batch/04-evaluation/job-01-dual-build/runners-before.json = read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json = read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json = read(截断>2000)
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json = read(截断>2000)
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json = read(截断>2000)
output/batch/result.md = read
output/batch/evaluator_manifest.json = read
output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md = missing (read -> "not found", yet evaluator_manifest.plannedReportPath points here)
output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json = missing
output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log = missing
output/batch/04-evaluation/job-00-…/returned-evidence/evidence-target.json = missing
output/batch/04-evaluation/job-00-…/{submission-1.json,submission-2.json} = missing
output/batch/target.ps1 = missing (evaluator_manifest references it on a foreign host path)
source/*.go, run_case.py = missing in this copy
```

3) Condensed findings

- Freeze/classify: no `frozen-inputs.md`. `classifier-input.json` binds `source/overwrite_rollback_check.go` sha `BE92E03B…`. `classification-1.json` (this is the *second*, corrected classification): cls `REVIEW_SIDE_EFFECTS`, reason `local_effects_require_review`, ALLOWED, blockingReason null, classifier 2.4 sha `009a6f31…`, `inputManifestSha256 684b52ed…`; files `overwrite_rollback_check.go` (filesystem lines 19,24,25,29,33,34,35,48) and `run_case.py` **sha `aeba7540b11653a469496da05cb1311de69b438343125e5f1355141051766d14`** (filesystem line 41, process 1,27,28). Both job dirs carry a `this-task-classification.json` identical to it (same inputManifestSha256) — so the re-classified identity is what was actually submitted. The failed first classification's own record is **not preserved** (only the 403 responses are).
- Requests: `02-conversion/request.system.txt` (25 lines) is the conversion system prompt — Go 1.27 → PowerShell 7.6 single file `target.ps1`; hard obligations (only a ```powershell block, byte-exact stdout/stderr + exit code, no stubs, real mkdir/write/read/SHA-256/rollback); explicit root path, file layout, sha256 lower-hex, rollback semantics, `artifact:` line via `Write-Output`; byte-shape spec for the JSON (map ⇒ lexicographic key order, 2-space indent, `": "` separator, `,\n` between items, **no trailing newline**, `rollback_ok` unquoted lowercase boolean); warns `ConvertTo-Json` order/indent differ; toolchain linux x64, syntax `pwsh parse`, run `pwsh -NoProfile -File target.ps1`. `02-conversion/observed-source-stdout.txt` = the 10-line source observation (artifact line + `--- report ---` + 6-key JSON). `observed-source-stderr.txt` = **empty**.
- Responses: `target.gen.model.json` is a **real body**, not metadata-only — `role: "assistant"`, `content` = the complete fenced ```powershell implementation (lines 3+ truncated at 2000 chars by the reader; visible: `$ErrorActionPreference='Stop'`, `Get-Sha256Hex` using `SHA256.HashData` + `StringBuilder` lowercase hex, `ConvertTo-JsonEscaped`, `Set-FileMode644` via `UnixFileMode`, root `Join-Path (Join-Path (GetTempPath) 'safe-attck-go') '14_impact'`, real `WriteAllBytes/ReadAllBytes` for target/backup, before/mutated hashes, rollback then read-back), plus `reasoning_content` (model internal reasoning, also truncated). It carries **no `model`, `finish_reason`, or `usage` fields** — the conversion call's metadata is therefore only recoverable by subtraction from item-json totals.
- Self-review: `review.system.txt` (1 line) is the static-review system prompt: compare Go 1.27 vs PowerShell 7.6 observable behavior, 5 named checks (real dir/file/SHA-256/rollback; map lexicographic key order `after_hash<backup<before_hash<mutated_hash<rollback_ok<target`; 2-space indent + no trailing newline + lowercase boolean; artifact line + exit 0; no added output), strict JSON-only output with an `origin` enum (`conversion-introduced|source-preexisting|toolchain-unknown|environment|undetermined`).
  - `self-review-1.model.json` is **metadata-only** (no body): `stage SELF_REVIEWED`, `reviewN 1`, `model deepseek-flash`, `finishReason stop`, `usage {prompt 2443, completion 29959, reasoning 29290, total 32402}`, `maxTokensFieldSent false`, `verdict NO-REPAIR-IDENTIFIED`, note "Static review only." Per the review rules this is **not** a complete response; it is a receipt.
  - `self-review-1.json` is the persisted conclusion: verdict `NO-REPAIR-IDENTIFIED`, `reviewedScope "target.gen.ps1 82行…"` (**naming inconsistency**: the scope text calls the target `target.gen.ps1` while item-json/metadata/job manifests call it `target.ps1`); 5 items (locations `:32-60`, `:67-76` ×2, `:82`, whole file), each with `origin: "undetermined"`, `issue` "no difference found", `proposed_fix null`, `risk 无`. No repairs were performed (0 repair rounds, `codeRevisions 0`).
- Jobs — job-00 `job-00-source-buildability`: jobId `eval-20261011-101525-d8f10193`; `comparison_manifest.json` source `go build -o program overwrite_rollback_check.go` (linux), target `pwsh …ParseFile('target.ps1'…)` (linux/powershell); `input_profile.json` argv `[]`, stdin null, timeout 30, wd workspace, dimension output; `evidence-source.json` (bundle `evb-source-eval-20261011-101525-d8f10193`, snapshot `CC-Eval-Linux-8Lang-1.0.28`): build `completed/0` 6464 ms empty out/err, execution `completed/0` 34 ms with the 10-line report stdout, empty stderr; `evaluation_report.json`: COMPLETED/FINISHED, source clean/READY, target (linux/powershell) performed, outcome `partial-runnable` / `codeVerdict failed` / `behaviorVerdict mismatched` (the placeholder target), `sufficientDimensions 1`, coverage 1.0, environment clean. `controller-health-before.json` at 10:12:19Z `contractSetHash a9ed1445…`; `runners-before.json` 3 READY. No target bundle stored for job-00 (missing).
- Jobs — job-01 `job-01-dual-build`: jobId `eval-20261011-101921-56b26056`; metadata `sourceHash be92e03b…`, `targetHash a796d494…` (= item targetSha256), note "driver starts it by language shape (`pwsh -File`, discipline 7) and echoes the produced advanced-impact-report.json on both sides"; `evidence-source.json`: build `completed/0` 6478 ms, execution `completed/0` 34 ms with the 10-line report; `evidence-target.json`: build `completed/0` 4463 ms (pwsh parse), execution `completed/0` 828 ms with **the same normalized stdout**, same digest; `comparison.json` `behaviorVerdict matched`, `dimensions.output matched obs diffs []`, other dimensions `not-applicable`; `evaluation_report.json`: `runVerdict runnable`, `codeVerdict passed`, `behaviorVerdict matched`, environment clean, `coverageRatio 1.0`, both preflight/cleanup PASSED, `contaminated false`, `runnerStateAfter READY`. `controller-health-before.json` at 10:19:20Z `contractSetHash a9ed1445…`; runners 3 READY. **job-01 has no `controller-health-after.json` and no `controller.log`** (contrast D2-052 job-01, which has both) → post-job runner/controller state and job timing are not evidenced for this item.
- Failed attempts / identity event: `attempt-1-403.json` and `submission-3.json` are **byte-identical** 403 bodies `{error admission_blocked, blockingReason identity_mismatch, "submitted content does not match the classified content", action "re-classify the exact submitted sources"}` → **two** distinct rejections were recorded (attempt-1 and submission-3), yet `submission-4.json` is the accepted `{jobId eval-20261011-101525-d8f10193, jobStatus QUEUED}`. `submission-1.json`/`submission-2.json` are **not preserved**, so the numbering starts at 3 with a gap. Item-json `usage.failedAttempts` is `0`, which **contradicts** the two preserved 403s (it counts model-call failures only — a definitional ambiguity worth flagging, not a false conversion claim). `events.jsonl` lines 570–571 record the wrong-driver first classification and the `IDENTITY_403` recovery.
- `result.md` present (39 lines), consistent with every artifact checked above: layer table (delivery complete, target syntax PASS `pwsh parse`, source baseline PASS, execution PASS exit 0/empty stderr, behavior `matched` digest `7d9ac0b5…`, environment clean, safety ALLOWED); "关键点" explains the map-lexicographic hand-built JSON, language-shape launch, and the 403/re-classification event; 2 coverage gaps (backup read/write error branches; single built-in fixture path). `evaluator_manifest.json` present (73 lines): `kind third-party-evaluator-manifest`, `generatedBy "code_convert-temporary-controller-adapter (hand-authored, not code-translator-mcp)"`, language pair go→powershell, `taskMetadata {sourceOs linux, targetOs linux, riskLevel low, evidenceMode static-and-runtime, supportLevel experimental}`, file entry `target.ps1` with `success true`, `x_adapter.status "converted-and-evaluated"`, jobId `eval-20261011-101921-56b26056`, prerequisites list (2.4 ALLOWED after re-classification; source precheck SOURCE_BUILDABLE; job-01 behaviorVerdict matched), `oracleFreezability "FREEZABLE: no non-reproducible quantity…"`, `responseIntegrityEvent` (first POST 403 → re-classify), `attackClassification {status reviewed, tactics [], techniques [], rationale local file overwrite/rollback check}`.
- Anomalies: (a) missing `evaluation_report.md` **at the exact path `evaluator_manifest.json` designates** (plannedReportPath `…job-01-dual-build\returned-evidence\evaluation_report.md`), i.e. the hand-off manifest points at a non-existent artifact; (b) missing job-01 `controller-health-after.json`/`controller.log`; (c) two identical 403 rejections preserved but `failedAttempts: 0` and no `submission-1/2`; (d) `reviewedScope` says `target.gen.ps1` while all other artifacts say `target.ps1`; (e) `target.ps1` itself is not in the reviewed tree (referenced only by `evaluator_manifest` on a foreign absolute host path `C:\Users\Administrator.DESKTOP-LRHSLVD\…\output\batch\target.ps1`) — the generated target is recoverable only from `target.gen.model.json`; (f) `batch-authorization.json` (both jobs) repeats the wrong `D2-088` task id; (g) manifest.csv row 53 still shows inherited JobId `eval-20261006-095722-a3d116e8` + `dual-build-PASS (inherited)` instead of the real `eval-20261011-101921-56b26056`; (h) no `frozen-inputs.md`; (i) job-00's report says `mismatched` because of the placeholder target and is stored under "source-buildability" — not a conversion verdict; (j) all 5 self-review items carry `origin: undetermined` (no item was attributed), which is acceptable for a no-repair conclusion but means the review adds no attribution evidence.
- Independent evidence facts: source and target stdout digests identical (item records `sha256:7d9ac0b5a5007dd264efe3ffe1d33947d095678a937afb50e3ffa6a41b50a8e3` for both); both builds `completed/0`; both executions `completed/0`; both stderr empty per the record; comparison 0 diffs on the single applicable dimension; both sides clean/READY in the job-01 report. Not independently verifiable here: `targetSha256` (no target file) and the truncated `observations`/`collectorDiagnostics` tails.
- Attribution: the matched behavior is a **conversion-level** result on the covered success path (real mkdir/write/read/SHA-256/rollback + byte-identical map-lexicographic JSON, 0 diffs). The job-00 `mismatched` verdict is **apparatus** (placeholder target). The 403 identity events are **apparatus/process** (classification identity vs edited driver), correctly recovered by re-classification and correctly not counted as a conversion failure. Missing logs/planned-report/target file are **delivery-record gaps**, not conversion defects. The `D2-088` string is a copy-paste **apparatus** defect.
- Knowledge candidates: the self-review's explicit guidance — hand-build Go `map[string]any` lexicographic JSON instead of relying on `ConvertTo-Json`, keep 2-space indent and no trailing newline, emit lowercase `true/false`, and start the target by language shape (`pwsh -NoProfile -File`) — is real, useful direction knowledge. Current contract coverage: the language-shape launch rule is already required (job-01 metadata cites discipline §7; `request.system.txt` line 25 states it) and the JSON-shape rule is already written into the item's own `request.system.txt` lines 18–21, but neither appears to be a generic `go-to-powershell` direction-skill rule in the reviewed tree at batch level (that skill was not part of this assignment, so coverage there is unverified). No **WRONG** self-review suggestion was found: all five claims are consistent with the artifacts.
- Optimization: store `target.ps1` with the batch output; emit the `evaluation_report.md` that `evaluator_manifest` promises, or drop the field; persist `submission-1/2` and count rejected submissions outside model-call counters (or document the distinction); fix the `target.gen.ps1` vs `target.ps1` name drift and the `D2-088` copy-paste; add `controller-health-after.json`/`controller.log` for job-01; update the manifest row.
- Unknowns: content of the conversion response tail beyond 2000 chars and of the `observations`/`collectorDiagnostics` sections; whether the conversion call recorded usage anywhere; why two 403s were issued for what the item describes as one rejected attempt; why job-01 lacks an after-health snapshot.

---

## Batch-level observations (apply across the assigned items)

- **Stale C# blocker (highest-impact).** `batch/platform-blocker-csharp-target.md` banner (2026-10-11) declares the evidence-bundle schema defect fixed (`eval-20261011-122249-fe456bbe` target build/exec completed/0) and states the 38 C# items need not remain `WAITING/BLOCKED_ENV`; `batch/summary.md` line 527 lists `D2-007~012, 030, 048~051, 065, 076~078, 156~160` with "恢复条件已具备" and mandates a full-chain re-run. D2-048/049/050/051 still carry `lifecycle WAITING`, `blockingReasons ["BLOCKED_ENV"]`, `pendingAction "platform fix …"` and no target/conversion artifacts. Their stored job reports also do **not** match the blocker's described mechanism (they show a performed, clean-environment target run failing with "Target build failed", not an INFRA_ERROR/SKIPPED-preflight at CLEANING). Recommended: do not treat these four as permanently blocked; re-open per summary.md:527 and update the item records afterwards.
- **Wrong task id `D2-088`** appears in every `batch-authorization.json` `dataSource.confirmation` under all six items (D2-048…053) — a copy-paste defect in the authorization record.
- **Manifest drift.** `manifest.csv` rows 48–53 all still carry inherited JobIds (2026-10-05/06/09) and `dual-build-PASS (inherited)`; row 52 says `REUSE` while the item/`result.md`/job metadata say `NEW`. Source hashes do match the items.
- **Contract-set hash changed between rounds:** `e088a356…` for the 2026-10-10 D2-052 job (snapshot `CC-Eval-Linux-8Lang-1.0.26`) vs `a9ed1445…` for all 2026-10-11 jobs (snapshot `…1.0.28`). Each item is internally consistent; the change is batch-level and should be reconciled explicitly rather than silently.
- **Four of six items lack `frozen-inputs.md`** (only D2-048 has one); only the two PowerShell items have `result.md`; only D2-053 has an `evaluator_manifest.json`; no item stores its generated target artifact (`target.cs`/`target.ps1`).
- **"Source-buildability" job dirs contain placeholder-target runs** whose reports say `failed`/`mismatched` (D2-052 job-00, D2-053 job-00, all four C# job-00). These verdicts are apparatus artifacts and must not be aggregated as conversion results; `events.jsonl` correctly reports only the source-side `completed/0` for them.
- Nothing in the reviewed files contains credentials or secrets; all jobs report `syntheticDataOnly`, `noRealCredentials`, isolated VM with no egress, and network fixed to loopback/offline.
