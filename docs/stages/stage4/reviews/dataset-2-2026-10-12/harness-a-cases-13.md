# Harness A — cases 13 (D2-042…D2-047) post-hoc static review

- Reviewer role: read-only static document reviewer (this report is the only artifact written).
- Scope root: `docs/dataset-2/dataset-2-copy/`.
- Assigned items: D2-042 … D2-047 (all under `go-to-cpp/`).
- Method: `glob` enumeration per item, then full `read` of every enumerated file; also `batch/items/<id>.json`, the `manifest.csv` row for each id, and (cross-check only) `batch/events.jsonl` lines 511–552. No scripts, no execution, no `D:\CodeConvertRemote\Stack` access, no secret files, no source reconstruction.
- Totals: 6 items × 41 files = **246 artifacts, all read** (no unreadable, no 0-byte, no directory-empty). Additionally 6 item-json files and `manifest.csv` (lines 1–2, 42–47) were read.

Tool limitation applied: single-line platform bundles (`evidence-*.json`, `evaluation_report.json`, `controller-health*.json`, `runners-before.json`) and the two long `content`/`reasoning_content` lines of `target.gen.model.json` exceed 2000 chars per line; `read` and `grep` truncate at 2000 chars and no byte-offset read exists in this session, so their tails are not retrievable. Those files are registered as `read(trunc>2000)`.

---

## 0. Cross-cutting facts (valid for all six items)

- Manifest (`manifest.csv` lines 42–47): all six are `Kind=REUSE`, `Direction=go-to-cpp`, `SourceLang=Go`, `TargetLang=C++`, `Evidence="dual-build-PASS (inherited)"`. The `JobId` column holds an **inherited 2026-10-06** job id (`eval-20261006-083723-cd1b5c2c`, `…-084324-56617693`, `…-084927-6d4a9826`, `…-090005-dbcce709`, `…-090937-116137c8`, `…-091535-096f0aed`) — none of them is the job actually used in this run.
- The `Lines` column (104 / 137 / 151 / 288 / 162 / 196) disagrees with `frozen-inputs.md` line counts (127 / 168 / 181 / 330 / 168 / 231) for every item. No header-level definition of that column was found in the reviewed scope → counted as a non-reconciling count.
- Three different path spellings coexist: item-json `casePath` = `docs/test/dataset-2/go-to-cpp/…`; manifest `Origin` = `dataset/go-to-cpp/…`; the actual copy directory = `docs/dataset-2/dataset-2-copy/go-to-cpp/…`.
- Declared source Sha256 matches in **all** records (frozen-inputs uppercase, manifest uppercase, classifier/classifier-input/item-json/metadata/this-task-classification lowercase). **No hash mismatch found in any of the six items.**
- Classifier: version 2.4, `classifierSha256 009a6f31…`, `admissionStatus=ALLOWED`, `blockingReason=null`, `executionApproved=true`, `analysisScope=source-text-only`, limitations `lexical_heuristics_not_dataflow` / `target_driver_dependencies_not_assessed` / `isolation_and_authorization_not_assessed`. All six classifications list `run_case.py` (sha `63f8aaf2…`) plus the Go source. `old_cls`/`old_reason` are `null`.
- **No reclassification occurred** in these six items (no `classification-2.json` exists).
- Item-json (`batch/items/…`): `disposition=CONVERTED`, `phase=CLOSED`, `blockingReasons=[]` for all six; `lifecycle` PARTIAL for D2-042…D2-045 and DONE for D2-046/D2-047.
- Absent everywhere in the six dirs: `target.cpp` / `target.gen.cpp` (source and target code were deleted), `capsule.zip`, `source-analysis.md`, `report.json`/`report.md`, `self-review-*.decision.json`, `*.proposal.json`, `*.provenance.json`, any `attempt-*` file.
- Every `job-00-*` “target” run is a placeholder: `build status=completed exitCode=0`, `execution status=completed exitCode=0`, stdout and stderr empty with digest `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (SHA-256 of empty input). Consequently **every job-00 `comparison.json` is `mismatched` with `targetValueSummary:""`**; job-00 is a source-buildability precheck only.
- All 12 job directories: `preflight PASSED`, `cleanup PASSED`, `contaminated=false`, `environmentStatus=clean`, `runnerStateAfter=READY`, runner `linux-vm-agent-x64`, snapshot `CC-Eval-Linux-8Lang-1.0.28`. Controller health (before/after) always `status:ok`, `preset noise-tolerant-v1`, `text_tokens [temporary-paths, timestamps, ephemeral-ports]`, `tolerate_minor:true`, `readyRunnerCount 3`, `blockedRunnerCount 0`.
- `batch-authorization.json` is byte-identical in all 12 job dirs (authorizedBy `gyh-p1`, validUntil 2026-10-17, `vmIsolation.confirmed=true`, `snapshotRollback=true`, `cleanupVerified=true`, `networkIsolation.publicNetworkBlocked=true`, contractHash `a9ed1445…`), and its `dataSource.confirmation` text names **“该项 D2-088”** — a wrong-item reference in every one of these six cases.
- `input_profile.json` (both jobs, all items): `argv []`, `stdin null`, `timeoutSeconds 30`, `workingDirectory "workspace"`, `observationPolicy.dimensions ["output"]`, `comparisonPolicy.output {ignoredJsonPaths: [], stderrMode: "exact", stdoutMode: "normalized-text"}` — **`ignoredJsonPaths` is empty in every item**, including the four whose known non-reproducible fields were identified before submission.
- `metadata.json` (both jobs): `kind=codeconvert-third-party-evaluation-metadata`, `sourceHash` = declared sha; `targetHash` = `sha256:placeholder-precheck` for job-00 and the real target hash for job-01; `safetyClassification` string citing classifier 2.4 ALLOWED.
- `comparison_manifest.json`: `caseId`, `inputProfileRef`, `source {arch x64, artifactLanguage go, buildCommand "go build -o program <file>.go", os linux, runCommand "python run_case.py"}`, `target {arch x64, artifactLanguage cpp, buildCommand "g++ -std=gnu++17 target.cpp -o program", os linux, runCommand "python run_case.py"}`.
- `evaluator_manifest.json` (one per item, 72–74 lines): `generatedBy "code_convert-temporary-controller-adapter (hand-authored, not code-translator-mcp)"`, `taskMetadata`, `targetDir`/`plannedResultPath`/`plannedReportPath` pointing at `C:\Users\Administrator.DESKTOP-LRHSLVD\Desktop\code-convert-skill\docs\test\dataset-2\…`, `summaryPath/batchReportPath/replayArtifactDir = null`, one `files[0]` entry (`relativePath target.cpp`, `success true`, `hasEvaluationNotes false`, `hasReplayArtifact false`), `x_adapter` block with `status converted-and-evaluated`, `executionApproved true`, real `jobId`, `prerequisites`, `isolationLaunchArgs`, `explorationOnly false`, `oracleFreezability`, `attackClassification {status reviewed, tactics [], techniques [], rationale}`.
- Repo-contract coverage note: the “§10.16 / §15” cited inside these items resolve to the **batch-local** `docs/dataset-2/dataset-2-copy/batch/operational-discipline.md` §10.16 (line 267, “可观察量必须可复现，否则 oracle 不可冻结”). The corresponding **repo-level** rule is `references/framework/evaluation-readiness-contract.md` §4 (line 87): non-reproducible, not-covered observables ⇒ `ORACLE_NOT_FREEZABLE + UNVERIFIED`, stop the behaviour evaluation, partial delivery, no repeated re-submission.

---

## 1. D2-042 — `go-to-cpp/imported-2026-10-04-c01-process-pipeline-capture`

### 1.1 IDENTITY
- taskId `D2-042`; kind `REUSE`; direction `go-to-cpp`; source file `process_pipeline_capture.go`.
- declared Sha256 `B099C6CED9EDE79FCC1B6C86BFDE74A4A39FD026E1ECD837900E275F11508D35` (manifest line 42 == frozen-inputs == classification-1 == classifier-input == item-json == job metadata).
- casePath `docs/test/dataset-2/go-to-cpp/imported-2026-10-04-c01-process-pipeline-capture`.
- item-json: `disposition CONVERTED`, `phase CLOSED`, `lifecycle PARTIAL`, `oracleFreezability ORACLE_NOT_FREEZABLE`, `pendingAction "另冻条件使可观察量确定化（如把 duration_ms 从比较面移除或改用固定值装置），或平台提供耗时消噪"`, `blockingReasons []`, `sourcePrecheck.jobId eval-20261011-091459-ca76af5e`, `evaluation.jobId eval-20261011-091852-e4ae88f2`, `targetSha256 51434d08464cbf4b03932072bf145506141d19fe66fd89bd1bb0c58c116ffc61`.
- item-json usage: `requests 2, promptTokens 8434, completionTokens 26092, reasoningTokens 20217, totalTokens 34526, model deepseek-flash, failedAttempts 0` (8434+26092=34526 ✔). Conversion remainder after the self-review call: prompt 2980, completion 7004.

### 1.2 FILE INVENTORY (41/41, exhaustive)
Prefixes: `F`=01-frozen, `C`=02-conversion, `S`=03-self-review, `J0`=04-evaluation/job-00-source-buildability, `J1`=04-evaluation/job-01-dual-build, `R`=returned-evidence.

```
F/classification-1.json=read
F/classifier-input.json=read
F/frozen-inputs.md=read
C/observed-source-stderr.txt=empty
C/target.gen.model.json=read(trunc>2000)
C/request.system.txt=read
C/observed-source-stdout.txt=read
S/self-review-1.json=read
S/self-review-1.model.json=read
S/review.system.txt=read
J0/R/evidence-source.json=read(trunc>2000)
J0/R/evidence-target.json=read(trunc>2000)
J0/R/comparison.json=read
J0/R/controller.log=read
J0/R/evaluation_report.md=read
J0/R/evaluation_report.json=read(trunc>2000)
J0/batch-authorization.json=read
J0/runners-before.json=read
J0/job-id.txt=read
J0/metadata.json=read
J0/comparison_manifest.json=read
J0/input_profile.json=read
J0/controller-health-before.json=read
J0/this-task-classification.json=read
J1/R/evaluation_report.md=read
J1/R/evidence-source.json=read(trunc>2000)
J1/R/evidence-target.json=read(trunc>2000)
J1/R/comparison.json=read
J1/R/controller.log=read
J1/R/controller-health-after.json=read
J1/R/evaluation_report.json=read(trunc>2000)
J1/batch-authorization.json=read
J1/this-task-classification.json=read
J1/comparison_manifest.json=read
J1/controller-health-before.json=read
J1/job-id.txt=read
J1/runners-before.json=read
J1/input_profile.json=read
J1/metadata.json=read
result.md=read
evaluator_manifest.json=read
```

### 1.3 FREEZE / CLASSIFY
- `frozen-inputs.md` (82 lines): Kind REUSE; `rawItemId D2-042`; `intakeId intake-dataset-2-2026-10-10`; `sourceBytes 4464`; `sourceLines 127`; Go 1.27 → ISO C++17; `sourceOs=targetOs=linux`, arch x64; runner `linux-vm-agent-x64`; snapshot `CC-Eval-Linux-8Lang-1.0.28`; model `deepseek-flash` temp 0.2 RAG off, **no max_tokens**; selected skills `go-to-cpp`, `languages/{go,cpp}`, `seven-language-common-semantics`, `scenes/process-execution`, `scenes/file-io`; `sceneTags process-execution`; `attackTactic none` (not symbol-proven; only a fixed built-in `echo`); taskMode long single file.
- Behaviour: banner → `/bin/sh -c "echo execution-benchmark-token-ok"` with 3 s `context.WithTimeout`, `WaitDelay=500ms`, separated stdout/stderr, `json.MarshalIndent` printed directly, exit 0 when `status=="PASS"` else 1.
- Declared risk: `duration_ms` is a non-reproducible activity counter not covered by the three explicit tokens; disposition = submit anyway, trust the platform verdict, and if the only difference is `duration_ms` record `ORACLE_NOT_FREEZABLE` + `UNVERIFIED`, `PARTIAL`, **not** a conversion failure.
- Build premises: `go build -o program process_pipeline_capture.go`; `g++ -std=gnu++17 target.cpp -o program`.
- Driver: one-shot program + natural exit; driver byte-identical on both sides; frozen `argv []`, `stdin null`, no readiness wait, `timeout=60` natural exit; oracle dimension `output`, `stdoutMode normalized-text`, `stderrMode exact`; **uncovered**: non-zero exit branch, timeout branch, child writing to stderr, Windows branch, file mode bits.
- `classification-1.json`: cls `REVIEW_SENSITIVE`, reason `sensitive_or_dynamic_operations`, reviewGroups `[dynamic_code, process]`; `process_pipeline_capture.go` signals process `[112]`, dynamic_code `[30]`; `run_case.py` process `[1,21,22]`; both `network_mode none-detected`, `has_process_exec true`, no credentials; `requiresSyntheticData true`; `inputManifestSha256 884c2e66…`.
- Reclassification: none.

### 1.4 SOURCE PRECHECK (job-00 `eval-20261011-091459-ca76af5e`)
- Exact build command `go build -o program process_pipeline_capture.go`; `build.status completed`, `exitCode 0`, `durationMs 5770`, stdout/stderr both empty (digest e3b0c442…, sizeBytes 0, truncated false).
- Execution `completed`, `exitCode 0`, `durationMs 33`, `timedOut false`; stdout 328 bytes, digest `sha256:d37f183c30d3d979dc4317553ca7ce627cb4647032a3547ae31ac8f30d0e6941`, content = banner + struct-ordered JSON with `duration_ms 1`, `status PASS`; stderr empty.
- Diagnostics: none (empty build stderr, no failure object).
- Cleanup: `preflight PASSED attempts 1`, `cleanup PASSED attempts 1`, `contaminated false`, `environmentStatus clean`, `runnerStateAfter READY`.
- `controller.log`: created 2026-10-11T09:14:59.756414+00:00, finished 09:16:04.884685+00:00.

### 1.5 REQUESTS / RESPONSES
- `C/request.system.txt` (33 lines): the full conversion contract — single ` ```cpp ` block, byte-exact stdout/stderr and exit code, no stubbing, fixed filename `target.cpp`, banner string, `/bin/sh -c` with 3 s timeout, separated pipes, real `steady_clock` measurement, `timed_out` semantics, `WEXITSTATUS`/`-1`, `status` predicate, `json.MarshalIndent(struct, "", "  ")` byte form (field-definition order, numbers vs bool, 2-space indent, `": "`, `,\n`, no JSON-internal trailing newline but `Println` adds one), Go HTML escaping, `platform` compile-time constant, no third-party libs, `g++ -std=gnu++17`.
- `C/target.gen.model.json`: real response content — `role assistant`, `content` = fenced C++ (≈275 lines per self-review; text beyond 2000 chars not retrievable), `reasoning_content` = the model's internal plan (also truncated). **No model name, no parameters, no usage/tokens, no `finish_reason`, no input/output SHA-256 inside the file** → conversion-call metadata absent.
- `S/self-review-1.model.json`: metadata-only record of the review call — `model deepseek-flash`, `finishReason stop`, prompt 5454 / completion 19088 / reasoning 15854 / total 24542, `maxTokensFieldSent false`, `verdict NO-REPAIR-IDENTIFIED`, note "Static review only; not a compile or behavior conclusion." No hashes.
- Failed attempts: none; `failedAttempts 0`; no attempt file.

### 1.6 SELF-REVIEW (`S/self-review-1.json`, 105 lines)
- Verdict `NO-REPAIR-IDENTIFIED`; scope = static line-by-line comparison of the 275-line target against the source; 11 items; every `issue` reads “未发现问题”.
- Origins used: `undetermined` ×9, `environment` ×2 — i.e., the model declined to attribute anything.
- Noteworthy risks registered (model assertions, not verified): exec-failure reporting `127` vs Go's `-1`; WaitDelay approximation; poll millisecond truncation may SIGKILL up to <1 ms early; `waitpid` error branch would yield exit 0; non-ASCII `TrimSpace` gap; U+2028/U+2029 and invalid-UTF-8 escaping gap; `platform` compile-time constant wrong on non-amd64; unreachable nil-result error branch; `duration_ms` jitter (labelled environment).
- No repair, no proposal file, no parent/final hash pair, no change note.

### 1.7 JOBS
- **job-00** as §1.4. Returned `comparison.json`: `behaviorVerdict mismatched`, one diff `path stream.normalizedText`, `kind changed`, `criticality major`, `sourceValueSummary` = banner line, `targetValueSummary ""`; `evaluation_report.json` (schemaVersion 3.0) job COMPLETED/FINISHED, run verdict `partial-runnable`, code verdict `failed`, behavior `mismatched`, coverage 1 applicable / 1 observed / 0 matched / 1 mismatched / ratio 1.0; `evaluation_report.md` FAIL / MISMATCHED / CLEAN with no reconciliation caveat.
- **job-01 `eval-20261011-091852-e4ae88f2`**: source build completed/0 (5934 ms, empty stdout/stderr); target build completed/0 (1633 ms, empty stdout/stderr); source exec completed/0 (35 ms, 328 B, digest `d37f183c…`, `duration_ms 1`); target exec completed/0 (76 ms, 328 B, digest `sha256:486157816b851e1fab9c476b99679d8ebf020b11d397a1e28c07e3d8f23e56bb`, `duration_ms 2`); both stderr empty; `comparison.json` verdict `mismatched` with **one** major `stream.normalizedText` diff whose `sourceValueSummary` and `targetValueSummary` are the *same* banner prefix (the real difference is `duration_ms`, outside the 240-char summary); report FAIL/MISMATCHED/CLEAN/partial-runnable; `controller.log` 09:18:52.582211 → 09:20:01.649570; `controller-health-after` ok (checkedAt 09:20:20.863648).
- Side effects: local `/bin/sh -c echo` only; no file writes; no network (classifier `none-detected`); no registry/process/network dimension observed (profile declares `output` only).
- Cleanup: PASSED on both sides, runner READY, not contaminated. No comparison/report retry file exists.
- job-01 metadata `targetHash sha256:51434d08…` matches item-json and `result.md`.

### 1.8 RESULT / DELIVERY (`result.md`, `evaluator_manifest.json`)
- `result.md`: terminal `PARTIAL / ORACLE_NOT_FREEZABLE`; layer table (delivery complete; target compile PASS via `g++ -std=gnu++17` completed/0; source baseline PASS; execution PASS; behaviour `mismatched` (platform verdict preserved) but the only difference is `duration_ms`; environment clean; safety ALLOWED); field-by-field table; explicit “保留平台原 verdict，不自行改判为 PASS”; 5 coverage gaps; both job ids.
- `evaluator_manifest.json`: `status converted-and-evaluated`, `executionApproved true`, `jobId eval-20261011-091852-e4ae88f2`, `files[0].relativePath target.cpp success true`, `oracleFreezability "ORACLE_NOT_FREEZABLE: duration_ms is a non-reproducible execution-time quantity not covered by explicit noise tokens; all OTHER observable fields are byte-identical"`, `attackClassification.tactics []`, rationale “fixed built-in echo, no network, no external target”.
- Claims reconcile with the accessible evidence prefix. The declared target hash cannot be recomputed here (no `target.cpp`).

### 1.9 ANOMALIES
- `target.cpp` absent ⇒ declared `targetSha256` unverifiable; no capsule/source tree; no `report.json`.
- `target.gen.model.json` carries no call metadata (model/params/tokens/finish_reason/hashes).
- 5 single-line bundles truncated >2000 chars (tails unrecoverable): both `evidence-*.json` sets and both `evaluation_report.json`.
- `duration_ms` (1 vs 2) produced a **major** diff despite `tolerate_minor: true`; `ignoredJsonPaths` was empty although the risk was known and documented pre-submission.
- `batch-authorization.json` names `D2-088`.
- Classifier maps `exec.CommandContext` into the `dynamic_code` review group (`dynamic_code:[30]`).
- `C/observed-source-stdout.txt` mirrors the **job-00** run (`duration_ms 1`); `result.md` quotes the job-01 pair (1 vs 2) — same value here, but the snapshot is unlabelled (a hazard for the sibling items where the two runs differ).

### 1.10 INDEPENDENT EVIDENCE FACTS (no model assertions)
- Two real Controller jobs exist with ids and wall-clock timestamps.
- `go build` exited 0 with zero diagnostics on both job-00 and job-01.
- Both binaries exited 0, both stderr streams empty.
- Source stdout 328 bytes digest `d37f183c…` (job-00 and job-01 identical); target stdout 328 bytes digest `48615781…`; **digests differ**.
- The comparison engine reports exactly one changed path (`stream.normalizedText`) with `criticality major`.
- Preflight/cleanup PASSED, environment clean, runner READY on both sides of both jobs.

### 1.11 ATTRIBUTION
- `duration_ms` → **environment / apparatus** (a genuinely measured value; the difference is run-to-run jitter).
- Everything else → identical, i.e. **conversion-introduced differences not evidenced**.
- Missing artifacts and empty `ignoredJsonPaths` → **apparatus / process**.

### 1.12 KNOWLEDGE
- Current contract **already covers** this class: `references/framework/evaluation-readiness-contract.md` §4 (line 87) requires `ORACLE_NOT_FREEZABLE + UNVERIFIED` and partial delivery when an observable varies and is not covered by confirmed denoising; the batch-local `docs/dataset-2/dataset-2-copy/batch/operational-discipline.md` §10.16 (line 267) is the source cited by `result.md`.
- Candidate rules (from evidence, not from model text): (a) treat activity counters such as `duration_ms` as non-oracle by default; (b) use the already-available `comparisonPolicy.output.ignoredJsonPaths` to exclude `/duration_ms` instead of relying on `tolerate_minor`; (c) require `target.gen.model.json` to carry `finish_reason`, usage and hashes (contract already requires it — see §"Cross-cutting" and the D2-045 discussion).
- Do-not-trust: the self-review's line-count and hash claims and its `undetermined` origins are model assertions, not evidence.

### 1.13 OPTIMIZATION
- Pretty-print or split bundle tails; emit an evidence-index file containing digest/sizeBytes/truncated.
- Populate `ignoredJsonPaths` for known non-reproducible fields.
- Label the `02-conversion` source snapshot with its source job id.
- De-duplicate the eight near-identical per-job sidecar files across items (48 files for six items).

### 1.14 UNKNOWNS
- Bundle tails (digest/sizeBytes/truncated/observations/cleanup events, target side effects).
- Target code content and the 275-line claim.
- Whether `capsule.zip` / source trees ever existed and were dropped by the copy.
- Whether `duration_ms` could be absorbed by any platform setting not visible in `controller-health*.json`.

---

## 2. D2-043 — `go-to-cpp/imported-2026-10-04-c05-tcp-loopback-scanner`

### 2.1 IDENTITY
- taskId `D2-043`; kind `REUSE`; direction `go-to-cpp`; source `tcp_loopback_scanner.go`; declared Sha256 `C5782998446EF3AA49353F991537C888441532DBA8B9BDECB059D0875CD3B503` (manifest line 43 == all records, lowercase elsewhere).
- casePath `docs/test/dataset-2/go-to-cpp/imported-2026-10-04-c05-tcp-loopback-scanner`.
- item-json: CONVERTED / CLOSED / `lifecycle PARTIAL` / `ORACLE_NOT_FREEZABLE` / `pendingAction "另冻条件使可观察量确定化（把 duration_ms 从比较面移除），或平台提供耗时消噪"` / `blockingReasons []` / `targetSha256 b93eb9b92335120b5e39f25731d1293c7f7bb3cfb2c113c57e1322d3eb218b6a`.
- usage: `requests 2, prompt 8825, completion 31769, reasoning 27415, total 40594` (sum ✔); conversion remainder prompt 2983, completion 8429; `failedAttempts 0`.

### 2.2 FILE INVENTORY (41/41, exhaustive)
```
F/classification-1.json=read
F/classifier-input.json=read
F/frozen-inputs.md=read
C/target.gen.model.json=read(trunc>2000)
C/observed-source-stdout.txt=read
C/request.system.txt=read
C/observed-source-stderr.txt=missing   (no such file; the other five items have an empty one)
S/self-review-1.model.json=read
S/self-review-1.json=read
S/review.system.txt=read
J0/R/evaluation_report.md=read
J0/R/evidence-source.json=read(trunc>2000)
J0/R/comparison.json=read
J0/R/evidence-target.json=read(trunc>2000)
J0/R/controller.log=read
J0/batch-authorization.json=read
J0/R/evaluation_report.json=read(trunc>2000)
J0/runners-before.json=read
J0/job-id.txt=read
J0/controller-health-before.json=read
J0/this-task-classification.json=read
J0/metadata.json=read
J0/comparison_manifest.json=read
J0/input_profile.json=read
J1/R/comparison.json=read
J1/R/controller.log=read
J1/R/controller-health-after.json=read
J1/R/evaluation_report.json=read(trunc>2000)
J1/R/evaluation_report.md=read
J1/R/evidence-source.json=read(trunc>2000)
J1/R/evidence-target.json=read(trunc>2000)
J1/batch-authorization.json=read
J1/this-task-classification.json=read
J1/comparison_manifest.json=read
J1/input_profile.json=read
J1/controller-health-before.json=read
J1/runners-before.json=read
J1/job-id.txt=read
J1/metadata.json=read
result.md=read
evaluator_manifest.json=read
```

### 2.3 FREEZE / CLASSIFY
- `frozen-inputs.md`: Kind REUSE; rawItemId + intakeId present; `sourceBytes 4999`; `sourceLines 168`; Go 1.27 → ISO C++17; linux/x64 both; skills `go-to-cpp`, `languages/{go,cpp}`, `seven-language-common-semantics`, `scenes/network-io`, `scenes/concurrency`; sceneTags `network-io` + `concurrency`; `attackTactic none` with the target hard-coded to `127.0.0.1`.
- Behaviour: banner; two mock listeners on 18081/18082 + 50 ms sleep; 4 workers scanning 18080–18084 with 300 ms timeouts and immediate close; ascending sort; `json.MarshalIndent(struct)`; PASS predicate; failure exit 2.
- Declared risk: `duration_ms` non-reproducible (Sleep + dials + 4-thread scheduling), not token-covered; disposal identical to D2-042. **Additional risk noted:** if 18081/18082 are already occupied on the runner the mock listeners fail and the **source** run fails — to be judged by the precheck.
- Driver: one-shot, `argv []`, `stdin null`, no external readiness wait (the program manages its own listeners), `timeout=60`; oracle `output` normalized-text/exact; uncovered: no-open/all-open forms, port-in-use path, 300 ms timeout branch, non-loopback target, file mode bits.
- `classification-1.json`: cls `REVIEW_NETWORK`, reason `network_scope_and_inputs_require_review`, reviewGroups `[network, process]`; `run_case.py` listed first; `tcp_loopback_scanner.go` network signals `[54,70,84]`, `network_mode loopback`, two literal targets `127.0.0.1` at lines 54 and 93, `redirectVerified false`; `has_network true`, `has_process_exec false`, `requiresSyntheticData false`; `inputManifestSha256 91dc0660…`.
- **Internal inconsistency:** `frozen-inputs.md` line 79 states “分类器 `network_mode=none-detected`” while the classification file records `network_mode: "loopback"`.
- Reclassification: none.

### 2.4 SOURCE PRECHECK (job-00 `eval-20261011-092138-6459c353`)
- Build `go build -o program tcp_loopback_scanner.go`: completed/0, 7279 ms, empty stdout/stderr.
- Execution completed/0, 121 ms; stdout 236 B digest `sha256:180acf3ed02f40141abb113b9f73a9596857d307c0fbd6fe99eb2e2b8dedd60c`; content = banner + JSON with `open_ports [18081,18082]`, `scanned_count 5`, `duration_ms 52`, `status PASS`; stderr empty.
- Cleanup PASSED, environment clean, runner READY. Controller log 09:21:38.101236 → 09:22:41.738604.

### 2.5 REQUESTS / RESPONSES
- `C/request.system.txt` (31 lines): full contract incl. loopback-only binding (no `0.0.0.0`), two mock listeners with accept-and-close threads, 4 workers, 300 ms per-port timeout, sorted integer array, `json.MarshalIndent` shape (numeric array with 4-space elements and 2-space closing bracket), exit 0/2.
- `C/target.gen.model.json`: real response content (fenced C++, 339 lines per self-review) + `reasoning_content`; again **no model/params/usage/finish_reason/hash fields**.
- `S/self-review-1.model.json`: metadata-only; `model deepseek-flash`, `finishReason stop`, prompt 5842 / completion 23340 / reasoning 21967 / total 29182; verdict `NO-REPAIR-IDENTIFIED`; static-only note.
- Failed attempts: none.

### 2.6 SELF-REVIEW (`S/self-review-1.json`, 96 lines)
- Verdict `NO-REPAIR-IDENTIFIED`; scope in English; 10 items, each `issue` = “未发现问题”.
- **All ten items are labelled `origin: source-preexisting`** — a semantically wrong use of the origin field for target-side implementation text (the contract asks for the attribution of the finding; several entries describe the target's own code or the environment).
- Risks registered: pipe-driven stop path, fd close on every `tryConnect` path, `nil` slice → `null`, `duration_ms` environment jitter, banner bytes. No repair, no proposal.

### 2.7 JOBS
- **job-00** as §2.4. `comparison.json`: mismatched, one major `stream.normalizedText` diff, source summary = banner + `{`, target summary `""`.
- **job-01 `eval-20261011-092557-3d1a2b12`**: source build completed/0 7423 ms; target build completed/0 2214 ms; source exec completed/0 119 ms stdout 236 B digest `sha256:33e63f593c3490247a5698d8ef7785e269e0a92c7c047278cab143b496d0dae4` (`duration_ms 57`); target exec completed/0 120 ms stdout 236 B digest `sha256:78f9543d052cc0a654a0cbc0c3c37bdb2a94a4573f154780b782585d85b12a32` (`duration_ms 51`); both stderr empty; `comparison.json` mismatched with a single major `stream.normalizedText` diff whose source and target summaries are the *same* banner prefix (the actual 57 vs 51 difference is not visible in the summary); report FAIL/MISMATCHED/CLEAN/partial-runnable; controller log 09:25:57.632127 → 09:27:08.570407; health-after ok.
- job-01 metadata `targetHash sha256:b93eb9b9…` matches item-json and `result.md`.
- Cleanup PASSED both sides; no retry artifacts.

### 2.8 RESULT / DELIVERY
- `result.md`: terminal `PARTIAL / ORACLE_NOT_FREEZABLE`; field table shows source `duration_ms 57` vs target `51`; preserves the platform verdict; records a **batch-level observation** that any output containing a genuinely measured elapsed time cannot be frozen under the current denoise configuration; 5 coverage gaps; both job ids.
- `evaluator_manifest.json`: `jobId eval-20261011-092557-3d1a2b12`, `oracleFreezability ORACLE_NOT_FREEZABLE…`, rationale about pure-loopback scanning, `tactics []`.

### 2.9 ANOMALIES
- `C/observed-source-stderr.txt` **missing** (asymmetry with the other five items; likely because the run produced no stderr file at all, but no record explains it).
- `C/observed-source-stdout.txt` shows `duration_ms 52` (job-00) while `result.md` cites 57 vs 51 (job-01) — unlabelled dual snapshots.
- Comparison summaries identical despite a major diff.
- Frozen-inputs text contradicts the classification's `network_mode`.
- `target.cpp` absent; 5 truncated bundles; `batch-authorization.json` names D2-088.

### 2.10 INDEPENDENT EVIDENCE FACTS
- The loopback scan genuinely discovered exactly two open ports `[18081,18082]` out of 5 scanned, on both sides, with `status PASS`.
- Both builds completed/0 (go 7279/7423 ms; g++ 2214 ms on job-01), both executions exited 0 with empty stderr.
- stdout digests differ (`180acf3e…`, `33e63f59…` source vs `78f9543d…` target) and the only accessible difference is `duration_ms`.
- Cleanup PASSED, runner READY, environment clean; wall time ≈71 s for job-01.

### 2.11 ATTRIBUTION
- `duration_ms` → **environment / apparatus**.
- Listener/scan/sort/PASS semantics → preserved (identical deterministic fields).
- Missing stderr file, contradictory frozen-inputs text, unlabelled snapshot → **apparatus / process**.

### 2.12 KNOWLEDGE
- Covered by `references/framework/evaluation-readiness-contract.md` §4 (line 87).
- Candidate rules: (a) a case whose deterministic fields all match but whose only diff is an activity counter should be recorded as `ORACLE_NOT_FREEZABLE` **before** submission (the frozen record already predicted it, so the risk was known); (b) make the presence/absence of `observed-source-stderr.txt` explicit in `result.md`; (c) keep classifier `network_mode` text and the classification JSON in sync.
- Do-not-trust: the self-review's `source-preexisting` origin labels and any inference that the missing stderr file is evidence of an empty stderr stream.

### 2.13 OPTIMIZATION
- Normalize counter/timestamp fields via `ignoredJsonPaths` or platform tokens.
- Standardize the source-snapshot file naming (`…-job-00.txt`).
- Record the classifier network_mode once, in one place, and reference it.

### 2.14 UNKNOWNS
- Which run `C/observed-source-stdout.txt` represents (inferred job-00; no header says so).
- Whether the missing stderr file means “no file was written” or “the file was dropped in the copy”.
- Bundle tails and target code.

---

## 3. D2-044 — `go-to-cpp/imported-2026-10-04-c06-smb-loopback-prober`

### 3.1 IDENTITY
- taskId `D2-044`; kind `REUSE`; direction `go-to-cpp`; source `smb_loopback_prober.go`; declared Sha256 `35D9DBDDB55B6787EEF9F4E77CCDD507523F61E27BAAA8D186FAAA9FC949E40E` (manifest line 44 == all records).
- casePath `docs/test/dataset-2/go-to-cpp/imported-2026-10-04-c06-smb-loopback-prober`.
- item-json: CONVERTED / CLOSED / PARTIAL / `ORACLE_NOT_FREEZABLE` / `pendingAction "另冻条件使可观察量确定化（移出 target 动态端口与 duration_ms），或平台提供覆盖"` / `blockingReasons []` / `targetSha256 15fa890d4872c24e488190dd09ede2a81ae75b1fef461135c1415bce8cec0e27`.
- usage: `requests 2, prompt 10786, completion 26424, reasoning 19011, total 37210` (sum ✔); conversion remainder prompt 3360, completion 14689; `failedAttempts 0`; `codeRevisions 0`, `selfRepairRounds 0`.

### 3.2 FILE INVENTORY (41/41, exhaustive)
```
F/classification-1.json=read
F/frozen-inputs.md=read
F/classifier-input.json=read
C/target.gen.model.json=read(trunc>2000)
C/observed-source-stderr.txt=empty
C/request.system.txt=read
C/observed-source-stdout.txt=read
S/self-review-1.json=read
S/self-review-1.model.json=read
S/review.system.txt=read
J0/R/evaluation_report.md=read
J0/R/comparison.json=read
J0/R/evidence-target.json=read(trunc>2000)
J0/R/controller.log=read
J0/R/evidence-source.json=read(trunc>2000)
J0/controller-health-before.json=read
J0/R/evaluation_report.json=read(trunc>2000)
J0/runners-before.json=read
J0/job-id.txt=read
J0/this-task-classification.json=read
J0/metadata.json=read
J0/input_profile.json=read
J0/batch-authorization.json=read
J0/comparison_manifest.json=read
J1/this-task-classification.json=read
J1/comparison_manifest.json=read
J1/input_profile.json=read
J1/metadata.json=read
J1/runners-before.json=read   (raw HTTP/1.1 response dump: uvicorn headers + content-length 1188 + body)
J1/job-id.txt=read
J1/controller-health-before.json=read
J1/R/evaluation_report.md=read
J1/R/evidence-source.json=read(trunc>2000)
J1/R/evidence-target.json=read(trunc>2000)
J1/R/comparison.json=read
J1/R/controller.log=read
J1/R/controller-health-after.json=read
J1/R/evaluation_report.json=read(trunc>2000)
J1/batch-authorization.json=read
result.md=read
evaluator_manifest.json=read
```

### 3.3 FREEZE / CLASSIFY
- `frozen-inputs.md` (71 lines; **no `rawItemId`/`intakeId` lines**, unlike D2-042/043): `sourceBytes 5695`, `sourceLines 181`, skills `go-to-cpp`, `languages/{go,cpp}`, `seven-language-common-semantics`, `scenes/network-io`; sceneTags `network-io`; `attackTactic none` with target `127.0.0.1:0`; `taskMode` long single file.
- Behaviour: banner; `net.Listen("tcp","127.0.0.1:0")` mock SMB2 responder thread with 1 s read/write deadlines; 30 ms sleep; 2 s dial; SMB2 negotiate magic header; read response; `json.MarshalIndent(LateralMoveReport)`; failure exits 1/2/3.
- Declared handling: `duration_ms` non-reproducible and not token-covered ⇒ `ORACLE_NOT_FREEZABLE` + `UNVERIFIED`, `PARTIAL`, platform verdict preserved (labelled “§15 适用”).
- Driver: one-shot, `argv []`, `stdin null`, no external wait, `timeout=60`; oracle `output` normalized-text/exact; uncovered: mock-responder failure path, dial/deadline branches, magic-mismatch branch, non-loopback target, file mode bits.
- `classification-1.json`: cls `REVIEW_NETWORK`, reason `network_scope_and_inputs_require_review`, reviewGroups `[network, process]`; `run_case.py` (sha 63f8aaf2…) first, then `smb_loopback_prober.go` with network signals `[60,70,102,116]`, `network_mode loopback`, one `127.0.0.1` literal at line 102, `has_network true`, `has_file_ops false`, `has_process_exec false`, `requiresSyntheticData false`; `inputManifestSha256 86e449f9…`.
- Reclassification: none.

### 3.4 SOURCE PRECHECK (job-00 `eval-20261011-092834-4368ba33`)
- `go build -o program smb_loopback_prober.go`: completed/0, 7185 ms, empty stdout/stderr.
- Execution completed/0, 68 ms; stdout 328 B digest `sha256:55f2279aacfb8a1e58a01d5d7d880811e182560e4b3a0bacfc3c671e0655d507`; content = banner + JSON `target "127.0.0.1:38809"`, `negotiated true`, `magic_check "MAGIC_TOKEN_VERIFIED"`, `duration_ms 31`, `status PASS`; stderr empty.
- Cleanup PASSED, clean, READY. Controller log 09:28:34.934379 → 09:29:36.576865.

### 3.5 REQUESTS / RESPONSES
- `C/request.system.txt` (29 lines): loopback-only dynamic-port listener with `getsockname`-recovered port, mock responder with 1 s deadlines, 30 ms readiness sleep, 2 s dial, magic verification driven by the real response, `json.MarshalIndent` struct order, exit 1/2/3, no third-party libs.
- `C/target.gen.model.json`: real content (fenced C++, 406 lines per self-review) + Chinese `reasoning_content`; **no metadata fields**.
- `S/self-review-1.model.json`: metadata-only; prompt 7426 / completion 11735 / reasoning 8474 / total 19161; `finishReason stop`; `model deepseek-flash`; `NO-REPAIR-IDENTIFIED`; static-only note.
- Failed attempts: none.

### 3.6 SELF-REVIEW (`S/self-review-1.json`, 105 lines)
- Verdict `NO-REPAIR-IDENTIFIED`; 11 items; **all labelled `origin: conversion-introduced` while every `issue` says “未发现问题”** — the origin field is used as “this is target-side code”, not as attribution of a defect; the contract expects origin to classify the finding.
- Substantive risks recorded: per-connection goroutine replaced by a serialized single-connection poll loop (argued unobservable for one client); `strerror` text differences on unreachable branches; SO_REUSEADDR parity; dynamic port claimed to be covered by `ephemeral-ports`; `duration_ms` environment jitter.
- Item 9 explicitly claims “两侧 target 中的临时端口必然不同，属平台消噪 token ephemeral-ports 覆盖范围，不构成行为偏差” — **this claim is contradicted by the later platform verdict**.
- No repair, no proposal.

### 3.7 JOBS
- **job-00** as §3.4; `comparison.json` mismatched with one major `stream.normalizedText` diff, source summary truncated at `…in Loopba`, target `""`.
- **job-01 `eval-20261011-093226-215ca109`**: source build completed/0 7438 ms; target build completed/0 1355 ms; source exec completed/0 66 ms stdout 328 B digest `sha256:d25e2ab2b2dd8063d7dfc1ad575b8759618f91da4b20e045bf8949c81b511734` (`127.0.0.1:35861`, `duration_ms 32`); target exec completed/0 67 ms stdout 328 B digest `sha256:ae5c66f842ac8d8c23b747029c6f2f1eb0a05980c4278fb9a977c6c5ab9f4329` (`127.0.0.1:46803`, `duration_ms 31`); both stderr empty; `comparison.json` mismatched with **one** major `stream.normalizedText` diff whose source and target summaries are the same banner prefix; report FAIL/MISMATCHED/CLEAN/partial-runnable; controller log 09:32:26.509764 → 09:33:36.847718; health-after ok (09:33:59.669282).
- job-01 `metadata.json` `targetHash sha256:15fa890d…` matches item-json/result.md.
- Side effects: local loopback listener + dial only; no files; no external network; only `output` observed.
- Cleanup PASSED both sides.

### 3.8 RESULT / DELIVERY
- `result.md` (51 lines): terminal `PARTIAL / ORACLE_NOT_FREEZABLE`; states both sides are byte-identical except the two non-reproducible quantities; table shows the `target` field `127.0.0.1:35861` vs `127.0.0.1:46803` and `duration_ms 32` vs `31`; explicitly says the dynamic port “本应” be covered by `ephemeral-ports` but that combined with `duration_ms` the platform still judged it major; notes both are non-conversion-introduced (the handshake values come from real bytes); preserves the platform verdict; 3 coverage gaps.
- `evaluator_manifest.json`: `jobId eval-20261011-093226-215ca109`; `oracleFreezability "ORACLE_NOT_FREEZABLE: target carries a dynamic port (ephemeral-ports) AND duration_ms (NOT covered by explicit noise tokens); all other fields byte-identical"`; rationale about a pure-loopback SMB2 magic probe.

### 3.9 ANOMALIES
- The platform's own `ephemeral-ports` token did **not** neutralize `127.0.0.1:<port>` embedded in JSON text (35861 vs 46803 stayed `criticality major`), while local metadata asserts that it is covered — a policy/verification mismatch and a wrong pre-submission assumption.
- The comparison collapses two differing quantities (port + duration) into one `stream.normalizedText` summary whose visible text is identical on both sides.
- `J1/runners-before.json` contains a **raw HTTP response dump** (status line + date + server + content-length + body) unlike the bare-JSON form in every other job — inconsistent evidence capture.
- `frozen-inputs.md` omits `rawItemId`/`intakeId`.
- `C/observed-source-stdout.txt` is the job-00 snapshot (port 38809, duration 31) while `result.md` quotes the job-01 pair (35861 vs 46803, 32 vs 31).
- `target.cpp` absent; 5 truncated bundles; `batch-authorization.json` names D2-088; classifier asserts `filesystem` group membership though the program only uses sockets.

### 3.10 INDEPENDENT EVIDENCE FACTS
- Three distinct kernel-assigned ports observed for the same program: `38809` (job-00 source), `35861` (job-01 source), `46803` (job-01 target) — direct proof the field is non-reproducible.
- Both sides performed a real handshake and returned `negotiated=true` and `magic_check="MAGIC_TOKEN_VERIFIED"`; both exited 0 with empty stderr.
- stdout digests differ (`55f2279a…`, `d25e2ab2…` source vs `ae5c66f8…` target).
- Both builds completed/0; preflight/cleanup PASSED; environment clean; runner READY.

### 3.11 ATTRIBUTION
- The `target` (host:port) field and `duration_ms` → **environment / apparatus** (kernel-allocated port; measured elapsed time).
- Handshake/verification semantics → preserved; **no conversion-introduced defect evidenced**.
- The token non-absorption and the raw-HTTP artifact → **apparatus**.

### 3.12 KNOWLEDGE
- Covered by `references/framework/evaluation-readiness-contract.md` §4 (line 87) and by `references/adapter/controller/comparison-policy-adapter.md` (line 55), which already warns that the token rules reduce recognized display differences and do **not** prove dynamic allocation.
- Candidate rules: (a) do not let a dynamic port enter the observable output, or add an explicit `127.0.0.1:\d+` token / `ignoredJsonPaths:["/target"]`; (b) verify token coverage empirically before freezing instead of asserting it (the self-review asserted and the platform disagreed); (c) standardize whether raw HTTP dumps are retained.
- Do-not-trust: self-review item 9's coverage claim and the `conversion-introduced` origin labels on defect-free items.

### 3.13 OPTIMIZATION
- Use `ignoredJsonPaths` for `/target`; add platform token coverage for `host:port`.
- Normalize sidecar capture format (bare JSON) or document the raw-dump exception.
- Split/pretty-print bundle tails.

### 3.14 UNKNOWNS
- Whether `ephemeral-ports` can ever absorb a `host:port` occurrence in this comparison engine.
- Whether the raw HTTP dump was an intentional capture or a fetch artifact.
- Bundle tails; target code.

---

## 4. D2-045 — `go-to-cpp/imported-2026-10-04-c07-tree-walk-zip-collector`

### 4.1 IDENTITY
- taskId `D2-045`; kind `REUSE`; direction `go-to-cpp`; source `tree_walk_zip_collector.go`; declared Sha256 `8CDBF9659540652D4E86B5F3F120672F0A8290F84AE39BB91B968C6DDD7799B8` (manifest line 45 == all records).
- casePath `docs/test/dataset-2/go-to-cpp/imported-2026-10-04-c07-tree-walk-zip-collector`.
- item-json: CONVERTED / CLOSED / PARTIAL / `ORACLE_NOT_FREEZABLE` / `pendingAction "另冻条件使可观察量确定化（移出 archive_bytes/mod_time/duration_ms 与随机路径），或平台提供覆盖"` / `blockingReasons []` / `targetSha256 36737a0f50141fe2ef48ebff4c60c4eb12086cfb6b245af4b0deb66bbeaabeaa`; `codeRevisions 1`, `selfRepairRounds 0`.
- `modelConversion`: `attempts 2`; attempt1 `finishReason length`, completion 65533, reasoning 62810, outcome “TRUNCATED - content had no main and an unclosed fence; kept as `02-conversion/attempt-1-truncated.raw.json` (NOT delivered)”; attempt2 `finishReason stop`, converted, retried after adding the relaxation, 828 lines complete.
- usage: `requests 3, prompt 11960, completion 100131, reasoning 87897, total 112091, failedAttempts 0` (total = 11960+100131 ✔, but see anomalies).

### 4.2 FILE INVENTORY (41/41, exhaustive)
```
F/classification-1.json=read
F/classifier-input.json=read
F/frozen-inputs.md=read
C/observed-source-stderr.txt=empty
C/observed-source-stdout.txt=read
C/target.gen.model.json=read(trunc>2000)
C/request.system.txt=read
S/self-review-1.json=read
S/review.system.txt=read
S/self-review-1.model.json=read
J0/R/evaluation_report.md=read
J0/R/evidence-source.json=read(trunc>2000)
J0/R/evidence-target.json=read(trunc>2000)
J0/R/comparison.json=read
J0/R/controller.log=read
J0/R/evaluation_report.json=read(trunc>2000)
J0/batch-authorization.json=read
J0/runners-before.json=read
J0/job-id.txt=read
J0/controller-health-before.json=read
J0/this-task-classification.json=read
J0/metadata.json=read
J0/comparison_manifest.json=read
J0/input_profile.json=read
J1/R/evidence-target.json=read(trunc>2000)
J1/R/comparison.json=read
J1/R/controller.log=read
J1/R/controller-health-after.json=read
J1/R/evidence-source.json=read(trunc>2000)
J1/R/evaluation_report.md=read
J1/batch-authorization.json=read
J1/R/evaluation_report.json=read(trunc>2000)
J1/this-task-classification.json=read
J1/comparison_manifest.json=read
J1/input_profile.json=read
J1/metadata.json=read
J1/controller-health-before.json=read
J1/job-id.txt=read
J1/runners-before.json=read
result.md=read
evaluator_manifest.json=read
```
**Missing (asserted but absent): `C/attempt-1-truncated.raw.json`. A `glob **/attempt*` under `go-to-cpp/` returns nothing.**

### 4.3 FREEZE / CLASSIFY
- `frozen-inputs.md` (63 lines; no rawItemId/intakeId): `sourceBytes 9657`, `sourceLines 330`; Go 1.27 with `archive/zip`, `crypto/sha256`, `encoding/{hex,json}`, `io/fs`, `path/filepath`, `time`; skills `go-to-cpp`, `languages/{go,cpp}`, `seven-language-common-semantics`, `scenes/file-io`; sceneTags `file-io`; `attackTactic none`.
- Behaviour: `os.MkdirTemp` random root + `defer RemoveAll`; `setupTestDirectoryTree`; `WalkDir` + extension filter `{.txt,.conf,.log}`; per-file sha256/size; ZIP with entries + `manifest.json`; read-back verification; `status=PASS` iff `zipVerified && len(metas)==5`; `json.MarshalIndent(CollectionReport)` printed directly; failures 1/2/3/4.
- Declared risk table (four quantities): `target_root`/`zip_path` (random, `temporary-paths` **should** cover), `files[].mod_time` (`timestamps` **should** cover), `archive_bytes` (depends on Go `flate`; **not** covered), `duration_ms` (**not** covered); disposition = `ORACLE_NOT_FREEZABLE` + `UNVERIFIED`, `PARTIAL`, platform verdict preserved.
- Build premises: `go build -o program tree_walk_zip_collector.go`; `g++ -std=gnu++17 target.cpp -o program`, with the note “**不引入第三方压缩库**；目标须自带 ZIP/DEFLATE 或仅生成等价归档”.
- Driver: one-shot, `argv []`, `stdin null`, no external wait, `timeout=60`; oracle `output` normalized-text/exact; uncovered: setup failure path, WalkDir error branch, ZIP write/verify failure, non-matching extensions, **cross-implementation equivalence of `archive_bytes` not attempted**.
- `classification-1.json`: cls `REVIEW_NETWORK`, reason `network_scope_and_inputs_require_review`, reviewGroups `[filesystem, network, process]`; `tree_walk_zip_collector.go` filesystem signals `[95,98,107,239,289,294]`, process `[]`, **`network_mode "loopback"`, `has_network true`, one `127.0.0.1` literal at line 85**; `run_case.py` process `[1,21,22]`; `requiresSyntheticData false`; `inputManifestSha256 447bacc1…`.
- **Classifier false positive:** the Go program has no network operations at all; the frozen record itself notes “源码无网络信号”. The classification and its REVIEW_NETWORK admission therefore rest on a lexical `127.0.0.1` occurrence (probably inside fixture content), not on a network call.
- Reclassification: none (the retry changed only the system prompt, not the source).

### 4.4 SOURCE PRECHECK (job-00 `eval-20261011-093510-5fa281fb`)
- `go build -o program tree_walk_zip_collector.go`: completed/0, 6702 ms, empty stdout/stderr.
- Execution completed/0, 34 ms; stdout (multi-line JSON, not truncated in `evidence`/`observed-source-stdout.txt`): `tactic TA0009`, `target_root /tmp/bench_collection_2186035838/target_files`, `zip_path …/evidence_bundle.zip`, `total_scanned 7`, `total_matched 5`, `archive_bytes 1441`, `zip_verified true`, `status PASS`, five `files[]` entries (`config/app.conf` 49 B `c34cd89e…`, `config/db.conf` 41 B `75c42b2a…`, `docs/engineering/notes.txt` 50 B `52de1f06…`, `docs/finance/summary.txt` 48 B `ef677a33…`, `logs/audit.log` 49 B `9f5a4ec3…`, each `mod_time 2026-10-11T09:35:21Z`), `duration_ms 0`.
- job-00 `comparison.json` source summary shows `"target_root": "<TEMP_PATH:1>"` — **direct evidence the `temporary-paths` token works**.
- Cleanup PASSED, clean, READY. Controller log 09:35:10.310550 → 09:36:11.529991.

### 4.5 REQUESTS / RESPONSES
- `C/request.system.txt` (32 lines) is the **retry** prompt. Compared with the other items it contains an extra section “**简化许可（重要）**”: because `archive_bytes` is not freezable, the target **may write ZIP entries as STORED (method 0)**, provided the ZIP, `manifest.json` and read-back verification are real; the rest of the deterministic contract is unchanged.
- **The relaxation appears only here.** `frozen-inputs.md` line 46 still says “不引入第三方压缩库；目标须自带 ZIP/DEFLATE 或仅生成等价归档” and nowhere records the STORED permission; there is no amended frozen record, no re-read note, and no new classification.
- `C/target.gen.model.json`: real attempt-2 content (828 lines per self-review: hand-written SHA-256, ZIP local/central/EOCD writers, `verifyZip`, JSON marshaller) + Chinese `reasoning_content`; **no model/params/usage/finish_reason/hash fields**, so the truncation event cannot be confirmed from the response record itself.
- `S/self-review-1.model.json`: metadata-only; prompt 14909 / completion 18523 / reasoning 15855 / total 33432; `finishReason stop`; `model deepseek-flash`; `NO-REPAIR-IDENTIFIED`; note “Static review only.” (shorter than the other five).
- Failed attempts: attempt 1 is documented in item-json/result.md/evaluator_manifest/events.jsonl, but the raw artifact is missing and the item-json `failedAttempts` is `0`.

### 4.6 SELF-REVIEW (`S/self-review-1.json`, 78 lines)
- Verdict `NO-REPAIR-IDENTIFIED`; described scope = static, line-by-line, 828-line target vs source; 8 items; all `origin: conversion-introduced`; issues all “None …”.
- Substantive content/risks: real `opendir`/`readdir`/`lstat` recursion (asserts WalkDir equivalence); a full FIPS 180-4 SHA-256 implementation (risk: “a single wrong constant or shift would silently flip `zip_verified` to false”; claims the five `files[].sha256` “should be reproducible”); STORED ZIP permitted; `verifyZip` note that the CRC check is **self-consistent** rather than an independent oracle, compensated by length/sha256/content/manifest comparisons; fixture byte-exactness (sizes 49/41/49/48/50/28/21); counts 7/5; JSON field order including `files` before `duration_ms`; environment quantities incl. the prediction that the temp suffix is a free-form `\d+` token and that `mod_time`/`archive_bytes`/`duration_ms` must be treated as variable.
- These are model assertions; only the counts/sizes are corroborated by the evidence prefix. No repair, no proposal, no parent/final hashes.

### 4.7 JOBS
- **job-00** as §4.4 (`eval-20261011-093510-5fa281fb`); comparison mismatched, one major `stream.normalizedText` diff, source summary `{"tactic":"TA0009","target_root":"<TEMP_PATH:1>","zip_path":"<TEMP_P…`, target `""`.
- **job-01 `eval-20261011-094351-b270d800`**: source build completed/0 12220 ms; target build completed/0 2578 ms; source exec completed/0 35 ms with temp `bench_collection_1072617542` and **`archive_bytes 1442`**; target exec completed/0 69 ms with temp `bench_collection_1634208872` and **`archive_bytes 1907`** (STORED); both `status PASS`, `zip_verified true`, 7 scanned / 5 matched; both stderr empty; `comparison.json` mismatched with **one** major `stream.normalizedText` diff whose source and target summaries are identical (`{"tactic": "TA0009", "target_root": "<TEMP_PATH:1>", "zip_path": "<TEMP_P…`); report FAIL/MISMATCHED/CLEAN/partial-runnable; controller log 09:43:51.238489 → 09:45:34.377313; health-after ok (09:46:57.559881).
- job-01 metadata `targetHash sha256:36737a0f…` matches item-json/result.md.
- Cleanup PASSED both sides; no comparison retry file.

### 4.8 RESULT / DELIVERY
- `result.md` (56 lines): terminal `PARTIAL / ORACLE_NOT_FREEZABLE`; deterministic fields listed as byte-identical (`total_scanned 7`, `total_matched 5`, `zip_verified true`, `status PASS`, `files[]` `relative_path`/`size_bytes`/`sha256`); table of the four non-freezable quantities with the note that `target_root`/`zip_path` were replaced by `<TEMP_PATH:n>` (“✓ token applied”) and that `archive_bytes` 1442 vs 1907 arises from the permitted STORED form; section “⚠ 响应完整性事件（本项首次触发）” records attempt 1 `finish_reason=length` (completion 65533, reasoning 62810) and asserts the truncated response was kept as `02-conversion/attempt-1-truncated.raw.json` and not delivered; 3 coverage gaps; 2 job ids.
- `evaluator_manifest.json` repeats the response-integrity event and the STORED relaxation as prerequisite 4, lists `oracleFreezability "ORACLE_NOT_FREEZABLE: FOUR non-reproducible quantities …"`, and carries `responseIntegrityEvent` text.

### 4.9 ANOMALIES
1. **Asserted-but-missing artifact:** `02-conversion/attempt-1-truncated.raw.json` does not exist, although item-json, `result.md`, `evaluator_manifest.json` and `events.jsonl` all state it was kept.
2. **Unfrozen contract change:** the STORED relaxation lives only in `request.system.txt`; `frozen-inputs.md` L46 still forbids it; no amended freeze/re-read.
3. **Non-reconciling usage:** `requests 3` with `failedAttempts 0`; `promptTokens 11960` is **smaller than the self-review call's own `promptTokens 14909`**; `completionTokens 100131` equals attempt-2 + self-review only (65533 for attempt 1 excluded); `totalTokens 112091` = 11960+100131.
4. Comparison collapses four differing quantities into one summary with identical visible text.
5. `C/observed-source-stdout.txt` is the job-00 snapshot (temp `2186035838`, `archive_bytes 1441`, `duration_ms 0`) while `result.md` cites job-01 values (1072617542 / 1442 vs 1634208872 / 1907).
6. Classifier network false positive (`REVIEW_NETWORK`, `network_mode loopback`) for a pure file-io program.
7. `target.cpp` absent; 5 truncated bundles; `batch-authorization.json` names D2-088.

### 4.10 INDEPENDENT EVIDENCE FACTS
- The `temporary-paths` token demonstrably normalized both paths to `<TEMP_PATH:1>` in the comparison summaries.
- Two source runs of the identical program produced **different** `archive_bytes` (1441 then 1442) — direct proof the field is non-reproducible.
- The target produced 1907 bytes with STORED entries, consistent with the relaxation.
- Both sides: exit 0, empty stderr, `zip_verified true`, `status PASS`, `total_scanned 7`, `total_matched 5`; the first target `files[]` sha256 equals the source's first (`c34cd89e…`), and the same five source hashes are visible (`c34cd89e…`, `75c42b2a…`, `52de1f06…`, `ef677a33…`, `9f5a4ec3…`).
- Both builds completed/0 (go 6702/12220 ms; g++ 2578 ms); preflight/cleanup PASSED; environment clean; runner READY.

### 4.11 ATTRIBUTION
- Random temp path, `mod_time`, `archive_bytes`, `duration_ms` → **environment / apparatus**.
- The 1441→1442 spread is environment; the 1442→1907 delta is **conversion-introduced but explicitly permitted** by the (unfrozen) relaxation and declared non-comparable.
- Missing attempt artifact and inconsistent usage accounting → **apparatus / process**.

### 4.12 KNOWLEDGE
- Truncated-response handling is **already covered**: `references/workflow/conversion-evaluation-loop.md` line 37 (GENERATED must check truncation), line 39 (truncation/budget exhaustion ⇒ partial delivery), and **line 55** (“同一冻结请求因传输、截断或解析失败可重试一次；两次尝试和用量均保存”).
- The artifact obligation is **already covered**: `references/framework/delivery-handoff-contract.md` §2.2 (line 156 requires `self-review-<N>.attempt-<k>-failed.json`; line 164 requires `<stem>.attempt-<k>-failed.json` for each code draft) and §2.2.1 (line 202 requires “模型请求与响应 … attempt、状态/finish_reason、真实用量、原响应；成功与失败均保留，不只保存最后一次”). **Therefore the missing file is a concrete contract violation, not a gap in the rules.**
- The frozen-contract/request divergence is covered by §2.2 line 154 (“行为需求与 capsule 的 `input_profile.json` 策略须一致”) and by `conversion-evaluation-loop.md` line 57 (record the actual request content against the frozen contract).
- The oracle class is covered by `evaluation-readiness-contract.md` §4 line 87.
- Candidate rules: (a) any mid-run relaxation that changes allowed output semantics must be written back into `frozen-inputs.md` and re-read **before** the retry; (b) usage must be recorded **per attempt** and must reconcile with the per-call `*.model.json`; (c) compressed byte counts must not enter the oracle.
- Do-not-trust: self-review item 2's “the five sha256 values should be reproducible” and item 4's compensation claim — both static assertions; only the source-side hashes and the first-entry equality are evidenced in the accessible prefix.

### 4.13 OPTIMIZATION
- Persist per-attempt model metadata (finish_reason/usage/hashes) inside `<stem>.model.json`; keep the failed attempt file.
- Record relaxations as frozen-input amendments and reference them from the comparison policy.
- Add `archive_bytes`/temp-suffix normalization or `ignoredJsonPaths` entries.
- Pretty-print or split the truncated bundles.

### 4.14 UNKNOWNS
- Whether attempt-1 raw JSON was ever written to disk or was lost during the copy/transfer.
- The target `files[]` hashes and the target's own `mod_time` values (bundle tails unreachable).
- Whether reconciliation rounds (batch `reconciliation-*.md`, out of scope) logged the missing artifact.
- Whether `archive_bytes` would ever be considered comparable under another policy.

---

## 5. D2-046 — `go-to-cpp/imported-2026-10-04-c08-loopback-c2-controller`

### 5.1 IDENTITY
- taskId `D2-046`; kind `REUSE`; direction `go-to-cpp`; source `loopback_c2_controller.go`; declared Sha256 `2AF034C380E61344BBF12021B7F30D085F892217F0EC9B07DF38F21EE97366D5` (manifest line 46 == all records).
- casePath `docs/test/dataset-2/go-to-cpp/imported-2026-10-04-c08-loopback-c2-controller`.
- item-json: CONVERTED / CLOSED / **`lifecycle DONE`** / **`pendingAction null`** / **`oracleFreezability FREEZABLE`** / `blockingReasons []` / `targetSha256 6694dee5efb8fdf5256adb3f8eae2bd25ed91547e4071f6f5d8fa37e42c87096`; `codeRevisions 0`, `selfRepairRounds 0`.
- usage: `requests 2, prompt 13436, completion 46845, reasoning 38902, totalTokens 75781, failedAttempts 0` — **see anomalies (totals do not reconcile)**.
- `evaluation`: verdict `matched`, `sourceStdoutDigest == targetStdoutDigest == sha256:af1c2feb3ef66e20f6072e47d2c492739bf8c2fc8823bb6194ed26391ad2e3c1`, `digestsIdentical true`, `oracleStrength` “byte-for-byte reproduction of the Go map-lexicographic COMPACT JSON (incl. the shutdown_clean < status ordering) plus the struct-ordered results array”, `oracleFreezability FREEZABLE - no non-reproducible quantity in the output`.

### 5.2 FILE INVENTORY (41/41, exhaustive)
```
F/classification-1.json=read
F/classifier-input.json=read      (single-line compact form, unlike the pretty form in the other five items)
F/frozen-inputs.md=read
C/observed-source-stdout.txt=read
C/observed-source-stderr.txt=empty
C/target.gen.model.json=read(trunc>2000)
C/request.system.txt=read
S/self-review-1.json=read
S/self-review-1.model.json=read
S/review.system.txt=read          (template corrupted: /task, /result, results, Encode and backticks dropped)
J0/R/evidence-target.json=read(trunc>2000)
J0/R/comparison.json=read
J0/R/controller.log=read
J0/R/evaluation_report.md=read
J0/R/evidence-source.json=read(trunc>2000)   (contains a parsed structuredValue of the JSON stdout)
J0/R/evaluation_report.json=read(trunc>2000)
J0/batch-authorization.json=read
J0/runners-before.json=read
J0/job-id.txt=read
J0/this-task-classification.json=read
J0/comparison_manifest.json=read
J0/input_profile.json=read
J0/metadata.json=read
J0/controller-health-before.json=read
J1/R/evaluation_report.md=read
J1/R/evidence-source.json=read(trunc>2000)
J1/R/evidence-target.json=read(trunc>2000)
J1/R/comparison.json=read
J1/R/controller.log=read
J1/R/controller-health-after.json=read
J1/R/evaluation_report.json=read(trunc>2000)
J1/batch-authorization.json=read
J1/this-task-classification.json=read
J1/comparison_manifest.json=read
J1/input_profile.json=read
J1/metadata.json=read
J1/controller-health-before.json=read
J1/runners-before.json=read
J1/job-id.txt=read
result.md=read
evaluator_manifest.json=read
```

### 5.3 FREEZE / CLASSIFY
- `frozen-inputs.md` (60 lines; no rawItemId/intakeId): `sourceBytes 7460`, `sourceLines 168`; Go 1.27 with `net/http`; skills `go-to-cpp`, `languages/{go,cpp}`, `seven-language-common-semantics`, `scenes/network-io`, `scenes/concurrency`; sceneTags `network-io` + `concurrency`; `attackTactic none`; target `127.0.0.1:0`.
- Behaviour: HTTP service on `127.0.0.1:0` (`/task` GET, `/result` POST), client polls at most 3 times, built-in `upper`/`reverse` transforms, POST results, `server.Shutdown` (2 s) + `serveDone`, validations (`processedCount==2`, `outputs_valid`, `remaining==0`, `shutdownErr==nil`, `serveErr==ErrServerClosed`), output `json.NewEncoder(os.Stdout).Encode(report)` where `report` is `map[string]interface{}`.
- Line 29 spells out the map-lexicographic key order (`error < mode < outputs_valid < results < status < shutdown_clean < tasks_expected < tasks_processed < tactic` — note `shutdown_clean` **before** `status` because `sh < st`), the struct order inside `results` (`task_id → output → status`), compact encoding, and the single trailing `\n` from `Encoder.Encode`.
- Lines 35–38: **“本项无非确定量（与 D2-042~045 不同）”**, oracle freezable, with the explicit warning that `/task` order must be deterministic or it is a conversion defect.
- Driver: one-shot, `argv []`, `stdin null`, no external wait, `timeout=60`; oracle `output` normalized-text/exact; uncovered: `/task` non-200/204 branch, 400 invalid-task/result branch, Shutdown-failure branch, non-loopback target, out-of-order stress.
- `classification-1.json`: cls `REVIEW_NETWORK`, reason `network_scope_and_inputs_require_review`, reviewGroups `[filesystem, network, process]`; `loopback_c2_controller.go` network `[100,107,118]`, filesystem `[92,121]`, `network_mode loopback`, one `127.0.0.1` literal at line 100; `run_case.py` process `[1,21,22]`; `requiresSyntheticData false`; `inputManifestSha256 62f0a4a6…`.
- Reclassification: none.

### 5.4 SOURCE PRECHECK (job-00 `eval-20261011-094756-951e126e`)
- `go build -o program loopback_c2_controller.go`: completed/0, 13006 ms, empty stdout/stderr.
- Execution completed/0, 34 ms; stdout = one compact line (digest captured in the bundle tail, not reachable in the prefix, but the visible content is) `{"error":"","mode":"loopback_task_channel_control","outputs_valid":true,"results":[{"task_id":"TASK-001","output":"HELLO-C2-CHANNEL","status":"SUCCESS"},{"task_id":"TASK-002","output":"daolyap-kramhcneb-eruces","status":"SUCCESS"}],"shutdown_clean":true,"status":"PASS","tactic":"TA0011","tasks_expected":2,"tasks_processed":2}` followed by `\n`, **parsed by the collector into `structuredValue`** (a collector capability not exercised in D2-042…045 where `structuredValue` is null).
- stderr empty; job-00 comparison mismatched (placeholder target); clean/READY. Controller log 09:47:56.981772 → 09:49:13.330417.

### 5.5 REQUESTS / RESPONSES
- `C/request.system.txt` (28 lines): real HTTP server on `127.0.0.1:0` (no `0.0.0.0`), `/task` GET returning queue tasks in order with 204 when empty, at most 3 polls, `command ∈ {upper, reverse}`, POST `/result` expecting 202, 2 s client timeout, `CheckRedirect`/`Proxy` semantics, real `Shutdown` + `ErrServerClosed`, the map-lexicographic compact JSON shape, exit codes 3/2/0.
- `C/target.gen.model.json`: real content (fenced C++, 684 lines per self-review) + `reasoning_content` (which discusses Go keep-alive semantics and how to emulate `http.Server.Shutdown`); **no metadata fields**.
- `S/self-review-1.model.json`: metadata-only; prompt 9738 / completion 19307 / reasoning 18121 / total 29045; `finishReason stop`; `model deepseek-flash`; `NO-REPAIR-IDENTIFIED`.
- Failed attempts: none.

### 5.6 SELF-REVIEW (`S/self-review-1.json`, 69 lines)
- Verdict `NO-REPAIR-IDENTIFIED`; 7 items; all `origin: conversion-introduced` with “No defect”.
- Noteworthy: item 1 states `shutdown()` **hardcodes** `serve_err_server_closed` instead of observing `Serve()`'s error and that it “matches the expected true”; item 7 asserts the reconstructed stdout line equals the oracle before any compile/run (“byte-for-byte match with the frozen oracle expected”).
- No repair, no proposal.
- The review prompt actually delivered to the model (`S/review.system.txt`) is damaged: identifiers/symbols (`/task`, `/result`, `results`, `Encode`) and backticks were stripped, leaving e.g. “。2.  200/204、 202 语义；轮询上限 3。” and a line break inside “**末尾一个 \n**”. The reviewer therefore saw a degraded checklist.

### 5.7 JOBS
- **job-00** as §5.4. `comparison.json`: mismatched, one major `stream.normalizedText` diff, source summary `{"error":"","mode":"loopback_task_channel_control","outputs_valid":true,"results`, target `""`.
- **job-01 `eval-20261011-095245-478f1ed5`**: source build completed/0 12247 ms; target build completed/0 1658 ms; source exec completed/0 36 ms stdout digest `sha256:af1c2feb…` (compact JSON, `structuredValue` parsed); target exec completed/0 71 ms stdout digest **`sha256:af1c2feb…` (identical)**; both stderr empty; `comparison.json` `behaviorVerdict "matched"`, `verdictReason "All applicable observed dimensions matched."`, all `diffs: []`, dimensions `output matched`, others `not-applicable`; `evaluation_report.md` records Conversion result **PASS**, Behavior **MATCHED**, Environment CLEAN, run verdict **runnable**, code verdict **passed**, coverage `1 | 1 | 1 | 0 | 0 | 100%`, and **no Failure section**; controller log 09:52:45.611243 → 09:53:56.513876; health-after ok (09:55:02.137981).
- job-01 metadata `targetHash sha256:6694dee5…` matches item-json/result.md.
- Cleanup PASSED both sides; no retry artifacts.

### 5.8 RESULT / DELIVERY
- `result.md` (50 lines): no “终态” banner line, but the layer table declares delivery complete, target compile PASS, source baseline PASS, execution PASS, **behaviour matched** (digests identical `sha256:af1c2feb…`, diffs 0, coverage 1.0), environment clean, safety ALLOWED; a dedicated section explains the map-lexicographic compact JSON reproduction difficulty (with the `shutdown_clean` before `status` ordering and the struct-ordered `results` array); states that `matched` was not accepted on its own but cross-checked (non-degenerate source observation, argv delivered, symmetric apparatus); lists 4 coverage gaps; both job ids.
- `evaluator_manifest.json`: `jobId eval-20261011-095245-478f1ed5`; `oracleFreezability "FREEZABLE: no non-reproducible quantity in the output (no duration/timestamp/random path)"`; rationale about a pure-loopback HTTP C2 channel with built-in safe transforms.

### 5.9 ANOMALIES
1. **Usage arithmetic does not reconcile:** `totalTokens 75781` ≠ `promptTokens 13436 + completionTokens 46845 = 60281` (off by 15500). The self-review call's own total is 29045, so the conversion remainder is 31236 and the correct sum is 60281 — the stored `totalTokens` is wrong.
2. **Review prompt template corrupted** (`S/review.system.txt`) — placeholders/identifiers dropped; the reviewer's checklist is degraded.
3. `F/classifier-input.json` is written in single-line compact form, unlike the pretty form in the other five items.
4. Only the `output` dimension is observed even though the program performs file (`os` usage) and network side effects; the profile declares `dimensions ["output"]`, so `filesystem/processes/registry/network` are all `not-applicable` in the comparison.
5. `target.cpp` absent; 5 truncated bundles; `batch-authorization.json` names D2-088.
6. Self-review item 1 documents a real semantic shortcut (hardcoded `serve_err_server_closed`) that no independent evidence contradicts but also does not verify.

### 5.10 INDEPENDENT EVIDENCE FACTS
- stdout digests are **byte-identical** on both sides (`af1c2feb…`) across two independent runner invocations, with exit 0 and empty stderr on both sides.
- The emitted report is compact, has no spaces after `:`, and ends with exactly one `\n`; the collector even parsed it into `structuredValue` on both sides.
- `tasks_processed == tasks_expected == 2`, `outputs_valid true`, `shutdown_clean true`, `status PASS`, `error ""`, and the two expected task outputs (`HELLO-C2-CHANNEL`, `daolyap-kramhcneb-eruces`) are present on both sides.
- Both builds completed/0 (go 13006/12247 ms; g++ 1658 ms); preflight/cleanup PASSED; environment clean; runner READY.

### 5.11 ATTRIBUTION
- Matched behaviour → **conversion-introduced differences not evidenced**; the observable contract was reproduced.
- Token-count mismatch and corrupted review template → **apparatus**.
- Narrow observation profile (output only) → **apparatus / process scope**.

### 5.12 KNOWLEDGE
- Already covered: `references/framework/evaluation-readiness-contract.md` §5 (lines 93–95) requires that a non-empty observation be separated from driver failure, that input delivery and symmetric apparatus be checked, and that an empty/identical-output artificial match not be accepted on its own; AGENTS.md §3 states that self-review is a progress signal, not a verification.
- Candidate rules (from evidence): (a) per-item usage totals must be derived from the per-call `*.model.json` records and validated at item-json assembly time (D2-046 total is arithmetically wrong; D2-045's prompt total is smaller than one of its own calls); (b) the review/request prompt templates need a placeholder-integrity check — D2-046 and D2-047 show dropped identifiers, so the reviewer's checklist is not what the template author wrote; (c) when a program has file/network side effects, the frozen record and profile should state explicitly why those dimensions are unobserved.
- Do-not-trust: self-review item 7's pre-run “byte-for-byte match” claim (true here, but asserted before any evidence existed) and item 1's claim that the hardcoded `serve_err_server_closed` is observationally equivalent.

### 5.13 OPTIMIZATION
- Add usage-arithmetic validation; store per-call usage in `target.gen.model.json`.
- Render review prompts from a checked template and diff the rendered text against the template.
- Standardize `classifier-input.json` formatting.
- Declare unobserved side-effect dimensions honestly rather than relying on `output`-only comparison.

### 5.14 UNKNOWNS
- Whether the token mismatch is a recording defect or a real service anomaly.
- Whether the damaged review template affected the other five items (only D2-046 shows visible damage; D2-047 shows a milder form).
- Bundle tails (cleanup events, side effects, target digests/sizes); target code content; the 684-line claim.

---

## 6. D2-047 — `go-to-cpp/imported-2026-10-04-c09-chunked-http-exfiltrator`

### 6.1 IDENTITY
- taskId `D2-047`; kind `REUSE`; direction `go-to-cpp`; source `chunked_http_exfiltrator.go`; declared Sha256 `18CFC88BF8C05AA1EFAD56D4087FB6F4BE57C645E735B667256A970C4075D745` (manifest line 47 == all records).
- casePath `docs/test/dataset-2/go-to-cpp/imported-2026-10-04-c09-chunked-http-exfiltrator`.
- item-json: CONVERTED / CLOSED / **DONE** / `pendingAction null` / **FREEZABLE** / `blockingReasons []` / `targetSha256 6c60e010b0ac2757cf642f74e7435bcf9c206b9d21e7b068d737ae6012a43bcf`; `codeRevisions 0`, `selfRepairRounds 0`.
- usage: `requests 2, prompt 15107, completion 53497, reasoning 43204, totalTokens 68604` (sum ✔); conversion remainder prompt 3976, completion 31510; `failedAttempts 0`.
- `evaluation`: verdict `matched`, `sourceStdoutDigest == targetStdoutDigest == sha256:f47ea175f0fe4898abb3402627c5eaf845c73b0b2d7e2673560353e938a1de78`, `digestsIdentical true`, `oracleStrength` “byte-for-byte reproduction of the banner plus the Go map-lexicographic COMPACT JSON”, `oracleFreezability FREEZABLE`.

### 6.2 FILE INVENTORY (41/41, exhaustive)
```
F/classifier-input.json=read     (single-line compact form)
F/classification-1.json=read
F/frozen-inputs.md=read
C/observed-source-stderr.txt=empty
C/observed-source-stdout.txt=read
C/target.gen.model.json=read(trunc>2000)
C/request.system.txt=read
S/self-review-1.json=read
S/self-review-1.model.json=read
S/review.system.txt=read         (template placeholders stripped, as in D2-046)
J0/R/evaluation_report.md=read
J0/R/evidence-source.json=read(trunc>2000)
J0/R/evidence-target.json=read(trunc>2000)
J0/R/comparison.json=read
J0/R/controller.log=read
J0/R/evaluation_report.json=read(trunc>2000)
J0/batch-authorization.json=read
J0/runners-before.json=read
J0/job-id.txt=read
J0/this-task-classification.json=read
J0/comparison_manifest.json=read
J0/input_profile.json=read       (written in a more compact style than the other items)
J0/metadata.json=read
J0/controller-health-before.json=read
J1/R/evaluation_report.md=read
J1/R/evidence-source.json=read(trunc>2000)
J1/R/evidence-target.json=read(trunc>2000)
J1/R/comparison.json=read
J1/R/controller.log=read
J1/R/controller-health-after.json=read
J1/R/evaluation_report.json=read(trunc>2000)
J1/batch-authorization.json=read
J1/this-task-classification.json=read
J1/comparison_manifest.json=read
J1/input_profile.json=read
J1/metadata.json=read
J1/controller-health-before.json=read
J1/runners-before.json=read
J1/job-id.txt=read
evaluator_manifest.json=read
result.md=read
```

### 6.3 FREEZE / CLASSIFY
- `frozen-inputs.md` (64 lines; no rawItemId/intakeId): `sourceBytes 7676`, `sourceLines 231`; Go 1.27 with `crypto/sha256`, `encoding/hex`, `net/http`; skills `go-to-cpp`, `languages/{go,cpp}`, `seven-language-common-semantics`, `scenes/network-io`, `scenes/concurrency`; sceneTags `network-io` + `concurrency`; `attackTactic none`; receiver strictly `127.0.0.1:0`.
- Behaviour: banner; receiver `/upload_chunk` POST validating `ChunkPacket{index,total,data_hex,chunk_bytes}` (`total` expected, `index ∈ [0,total)`, `chunk_bytes == len(decoded)`, `0 < len ≤ 4096`, duplicate index ⇒ **409**), success **200** + `{"received":true}`; sender chunks a built-in `sourceData` by 4096 and POSTs each (`client.Timeout 2s`, `Proxy:nil`, `CheckRedirect=ErrUseLastResponse`); `server.Shutdown` (2 s) + `serveDone`; reassembly + sha256 vs `sourceHash`; `json.NewEncoder(os.Stdout).Encode(report)` (map); failures 4/5/6.
- Line 34 gives the lexicographic key order (`hash_match < mode < reassembled_hash < shutdown_clean < source_hash < status < tactic < total_chunks < uploaded_chunks`); lines 39–42 declare **no non-reproducible quantity**; the dynamic port appears only in `serverURL` and never in the report.
- Driver: one-shot, `argv []`, `stdin null`, no external wait, `timeout=60`; oracle `output` normalized-text/exact; uncovered: 405/400/409 branches, Shutdown-failure branch, non-loopback target, broader `sourceData` boundaries.
- `classification-1.json`: cls `REVIEW_NETWORK`, reason `network_scope_and_inputs_require_review`, reviewGroups `[filesystem, network, process]`; `chunked_http_exfiltrator.go` network `[128,130,135]`, filesystem `[74,79,84,90,106]`, `network_mode loopback`, one `127.0.0.1` literal at line 128; `run_case.py` process `[1,21,22]`; `requiresSyntheticData false`; `inputManifestSha256 a9d2de25…`.
- Reclassification: none.

### 6.4 SOURCE PRECHECK (job-00 `eval-20261011-095602-6aee77b4`)
- `go build -o program chunked_http_exfiltrator.go`: completed/0, 13490 ms, empty stdout/stderr.
- Execution completed/0, 34 ms; stdout = banner line + one compact JSON line (`hash_match true`, `mode sender_chunked_http_control`, `reassembled_hash == source_hash == c26f69b07371e48480f38836899db68b764fe42bd82165346c5ef298febbaa22`, `shutdown_clean true`, `status PASS`, `tactic TA0010`, `total_chunks 4`, `uploaded_chunks 4`) + `\n`, digest `sha256:f47ea175…`; stderr empty; comparison mismatched (placeholder target); clean/READY. Controller log 09:56:02.827537 → 09:57:11.736742.

### 6.5 REQUESTS / RESPONSES
- `C/request.system.txt` (26 lines): banner bytes, loopback dynamic port with `getsockname`, receiver validation incl. duplicate ⇒ 409 and `{"received":true}`, 4096-byte chunking of the built-in `sourceData` (reproduce byte-for-byte), `json.Marshal(ChunkPacket)` POSTs, hex encode/decode, self-implemented SHA-256, Shutdown/ErrServerClosed, map-lexicographic compact JSON, exit 4/6/5/0, no third-party libs.
- `C/target.gen.model.json`: real content (fenced C++, 771 lines per self-review, with a self-contained `class SHA256`) + a long Chinese `reasoning_content` (chunk arithmetic: 32-byte line × 512 = 16384 bytes = 4 × 4096); **no metadata fields**.
- `S/self-review-1.model.json`: metadata-only; prompt 11131 / completion 21987 / reasoning 19502 / total 33118; `finishReason stop`; `model deepseek-flash`; `NO-REPAIR-IDENTIFIED`.
- Failed attempts: none.

### 6.6 SELF-REVIEW (`S/self-review-1.json`, 105 lines)
- Verdict `NO-REPAIR-IDENTIFIED`; scope in Chinese; 11 items; all `origin: conversion-introduced` with “未发现缺陷” except item 8, 10 and 11, which record substantive deviations:
  - item 8: the source's temp-file failure paths (1/2/3) are unreachable in the target because it builds the same fixture in memory; judged unobservable under the frozen oracle (exit 0 + stdout).
  - item 10: the target implements shutdown as `close` rather than a genuine graceful drain, and hardcodes `serveErrIsServerClosed = true`; judged unobservable in this request/response timing.
  - item 11: the hand-written HTTP/JSON layer lacks an equivalent of `http.MaxBytesReader(16384)`, has looser routing (method-only), and produces different error bodies; judged status-code-equivalent because the real body is ~8.3 KB and the client reads only the status code.
- No repair, no proposal. `S/review.system.txt` is again corrupted (backticks/identifiers stripped), so the reviewer saw a degraded checklist.

### 6.7 JOBS
- **job-00** as §6.4; `comparison.json` mismatched, one major `stream.normalizedText` diff, source summary = banner text, target `""`.
- **job-01 `eval-20261011-100151-7b330747`**: source build completed/0 14433 ms; target build completed/0 2421 ms; source exec completed/0 33 ms stdout digest `sha256:f47ea175…`; target exec completed/0 68 ms stdout **same digest `sha256:f47ea175…`**; both stderr empty; `comparison.json` `behaviorVerdict "matched"`, `diffs []`, `output matched`, others not-applicable; `evaluation_report.md` PASS / MATCHED / CLEAN / runnable / passed, coverage `1 | 1 | 1 | 0 | 0 | 100%`, no Failure section; controller log 10:01:51.317934 → 10:03:01.094542; health-after ok (10:03:23.071287).
- job-01 metadata `targetHash sha256:6c60e010…` matches item-json/result.md.
- Side effects: loopback HTTP receiver + sender only; synthetic built-in data; no files; only `output` observed.
- Cleanup PASSED both sides; no retry artifacts.

### 6.8 RESULT / DELIVERY
- `result.md` (57 lines): layer table (delivery complete, target compile PASS, source baseline PASS, execution PASS, behaviour **matched** with identical digest, environment clean, safety ALLOWED); explains the banner + map-lexicographic compact JSON; notes no non-reproducible quantity; gives both job ids; states that `matched` was cross-checked; lists 3 coverage gaps.
- The file ends with a **“方向收口：go-to-cpp 11/11”** table claiming D2-037/038/039/040 `DONE/matched` and D2-041 `DONE/semantic_pass` — cross-item claims **outside this review's scope and not verifiable from any file inside the assigned six directories**. The same claim exists in the batch-local `events.jsonl` (`DIRECTION_CLOSED`, line 552) and the batch `README.md`, both of which are batch-authored artifacts rather than independent evidence.
- `evaluator_manifest.json`: `jobId eval-20261011-100151-7b330747`; `oracleFreezability "FREEZABLE: no non-reproducible quantity in the output"`; rationale about a pure-loopback chunked HTTP transfer with hash-verified reassembly.

### 6.9 ANOMALIES
1. **Review prompt template corrupted** (`S/review.system.txt`), same class as D2-046 — the model's checklist lost identifiers and backticks.
2. **Direction-closure claims inside a per-item `result.md`** (11/11, D2-037…D2-041) are unverifiable in this scope; they also mix terminal states of other items into this item's delivery file.
3. `F/classifier-input.json` and `J0/input_profile.json` are written in a noticeably more compact style than the other items.
4. Only the `output` dimension is observed although the program writes files (`os` usage in the classifier) and performs network I/O; the profile declares `dimensions ["output"]`.
5. `target.cpp` absent; 5 truncated bundles; `batch-authorization.json` names D2-088.
6. The classifier tags `filesystem` signals for a program whose file activity is limited to a temp tree outside the comparison surface.

### 6.10 INDEPENDENT EVIDENCE FACTS
- stdout digests are **byte-identical** on both sides (`f47ea175…`) across two independent runner invocations; both sides exit 0 with empty stderr.
- `reassembled_hash == source_hash == c26f69b0…baa22`, `hash_match true`, `shutdown_clean true`, `total_chunks == uploaded_chunks == 4`, `status PASS`, `tactic TA0010` on both sides.
- The banner line is byte-identical and is followed by exactly one compact JSON line plus one `\n`.
- Both builds completed/0 (go 13490/14433 ms; g++ 2421 ms); preflight/cleanup PASSED; environment clean; runner READY; job wall time ≈70 s.

### 6.11 ATTRIBUTION
- Matched behaviour → **conversion-introduced differences not evidenced** for the frozen path.
- Template corruption, missing dimension coverage, cross-item closure claims → **apparatus / process scope**.
- The three self-review-noted deviations (in-memory fixture, `close`-based shutdown, missing body-size limit) are **conversion-introduced** but were judged unobservable under the frozen oracle; no independent evidence in this copy refutes or confirms that judgement, and none of them can alter the reproduced bytes here.

### 6.12 KNOWLEDGE
- Covered: `references/framework/evaluation-readiness-contract.md` §5 (lines 91–95) requires that observation dimensions correspond to the frozen behaviour obligations and explicitly states that counts, total length or stdout echo do not substitute for the file dimension; §4 (line 87) covers freezability. The `matched` acceptance discipline is in §5 (lines 93–95); the self-review-is-not-verification rule is in AGENTS.md §3.
- Candidate rules (from evidence): (a) when a program has observable file/network side effects but the submitted profile narrows to `output`, the frozen record must state that those dimensions were not observed (partially done in D2-045/D2-047); (b) fix the review-prompt template rendering (dropped placeholders in D2-046/D2-047); (c) per-item `result.md` should not carry direction-level closure arithmetic.
- Do-not-trust: the self-review's claim that `shutdown_clean`/`serveErrIsServerClosed` are equivalent to Go's graceful shutdown (item 10 itself admits it is a `close` simulation and a hardcoded flag); the direction-closure table.

### 6.13 OPTIMIZATION
- Repair the prompt template and add a rendered-template check.
- Standardize `classifier-input.json` / `input_profile.json` formatting.
- Require the profile to declare which side-effect dimensions are deliberately unobserved.
- Move direction-closure reporting to the batch summary instead of each item's `result.md`.

### 6.14 UNKNOWNS
- Whether 405/400/409 branches behave as documented (unexercised; model-asserted only).
- Bundle tails (digests/sizes/cleanup events/side effects); target code content; the 771-line claim.
- Whether the direction-closure table is accurate (outside scope).

---

## 7. Consolidated findings and next actions for the parent

1. **Missing required artifact — D2-045.** `02-conversion/attempt-1-truncated.raw.json` is asserted by `batch/items/D2-045.json`, `result.md`, `evaluator_manifest.json` and `events.jsonl` line 534, but no `attempt*` file exists anywhere under `go-to-cpp/`. Obligation is already written down: `references/framework/delivery-handoff-contract.md` §2.2 lines 156/164 and §2.2.1 line 202, plus `references/workflow/conversion-evaluation-loop.md` line 55.
2. **Conversion response records carry no metadata — all six items.** `target.gen.model.json` contains only `role`/`content`/`reasoning_content`: no model name, parameters, tokens, `finish_reason` or input/output SHA-256, although §2.2 line 164 / §2.2.1 line 202 require them. As a result the D2-045 truncation cannot be confirmed from the response record itself.
3. **Unfrozen contract change — D2-045.** The STORED/ZIP relaxation exists only in `request.system.txt`; `frozen-inputs.md` line 46 still forbids it; no amended frozen record, no re-read, no reclassification.
4. **Non-reconciling counts.** D2-045 `requests 3` / `failedAttempts 0` with `promptTokens 11960` smaller than one of its own calls (14909); D2-046 `totalTokens 75781` ≠ `13436 + 46845`; manifest `Lines` column differs from `frozen-inputs.md` line counts in all six items; D2-043's frozen-inputs contradicts its classification's `network_mode`.
5. **Denoising does not cover what the records claim.** `127.0.0.1:<ephemeral port>` still produced a `major` diff (D2-044: 35861 vs 46803) despite the self-review asserting `ephemeral-ports` coverage; `duration_ms` produced `major` diffs in D2-042/043/044; `comparisonPolicy.output.ignoredJsonPaths` is empty in every `input_profile.json`.
6. **Prompt-template corruption** in `S/review.system.txt` for D2-046 and D2-047 (identifiers/backticks dropped) degraded the reviewer's checklist.
7. **Evidence retention gaps.** No `target.cpp`, no `capsule.zip`, no source trees, no `report.json`/`report.md`; all 5 single-line bundles per item are truncated at 2000 chars, so bundle tails (digests, sizes, `truncated` flags, observation/cleanup events, target-side `files[]`) are unrecoverable in this copy.
8. **Classifier accuracy.** D2-045 is a false-positive `REVIEW_NETWORK` (`network_mode loopback`, `has_network true` with no network syscall; a `127.0.0.1` literal at line 85 — the frozen record itself says “源码无网络信号”); D2-042 maps `exec.CommandContext` into the `dynamic_code` group.
9. **Self-review fields are unreliable as attribution.** D2-043 labels all ten items `source-preexisting`; D2-044…D2-047 label all items `conversion-introduced` while reporting no defect. Origins must not be consumed as findings.
