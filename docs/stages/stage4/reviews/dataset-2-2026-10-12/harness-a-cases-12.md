# Harness A — Full Case Review: D2-018 … D2-023

Read-only static document review. No source/target code exists in `docs/dataset-2/dataset-2-copy` (deleted by design); only process artifacts remain. No files were modified except this report. No secret/key value was observed in any read file. No script, classifier, conversion or submission was run.

**Tool limits (apply to every item below).** All job evidence bundles (`evidence-*.json`, `comparison.json`, `evaluation_report.json`, `controller-health*.json`) are single-line JSON; the read and grep tools truncate a line at 2000 characters and there is no byte-offset read, so the suffix is not retrievable. Status `read(trunc>2000)` means the registerable prefix was read and the tail (observations / artifacts / cleanup blocks) is unverifiable with the current tools. The sandbox denies PowerShell (`SetNamedSecurityInfoW failed (Win32 5): grantWrite`), so `read`/`glob`/`grep` were the only instruments. Paths in inventories are relative to `docs/dataset-2/dataset-2-copy/`. Every file that exists under the six case directories was enumerated and read — 143 files total (D2-018: 1, D2-019: 29, D2-020: 19, D2-021: 20, D2-022: 41, D2-023: 33) — plus `batch/items/D2-018..D2-023.json`, the six matching `manifest.csv` rows, `batch/batch.json` and `README.md`.

**Cross-cutting fact used repeatedly below.** The surviving `*.model.json` files in this dataset are metadata-only: `taskId`, stage/round, `model`, `finishReason`, request/raw-response (and sometimes output) SHA-256 values, `usage` counters, `maxTokensFieldSent`, a verdict and a note — never a response body. Verified both on the assigned items (D2-019/D2-022/D2-023 self-review metadata) and on sibling cases outside the assignment (`cpp-to-c/handoff-2026-10-02-d07-chunked-manifest-exfil-cpp/output/batch/02-conversion/target.gen.model.json`; `c-to-python/D2-177-c-c-which.c/output/batch/02-conversion/target.self-repair-1.model.json`). Therefore a metadata-only `*.model.json` is **not** a complete response record, and no assigned item retains a real response body.

---

## D2-018 — cpp-to-python/handoff-2026-10-02-d09-multi-command-runner-cpp

### IDENTITY
- taskId `D2-018`; kind `REUSE`; direction `cpp-to-python`; source file `multi_command_runner.cpp` (manifest `Lines`=53).
- declared Sha256 (manifest, uppercase): `7C279224F3E1CEFDC5FFB8545F3D440385737CAD73B3E9EA072B6112A7573AF9`.
- casePath (item json): `docs/test/dataset-2/cpp-to-python/handoff-2026-10-02-d09-multi-command-runner-cpp`; manifest `Origin`: `dataset/cpp-to-python/handoff-2026-10-02-d09-multi-command-runner-cpp`; manifest `JobId` `eval-20261005-164244-f03ed52a`; manifest `Evidence` `dual-build-PASS (inherited)`.
- item json disposition `FROZEN`; phase `EVALUATION_NOT_READY`; lifecycle `PARTIAL`; pendingAction "freeze a condition that removes elapsed_ms from the observation before submission"; blockingReasons `["ORACLE_NOT_FREEZABLE"]`; classifier `{version 2.4, admissionStatus NOT_TAKEN, blockingReason null, cls null, sha256 null, note "not classified: not submitted"}`; verdicts sourceBuild "UNVERIFIED (not run; not submitted)", targetBuild/execution/comparison `UNVERIFIED`, environment `n/a`, safety `NOT_SUBMITTED`; codeRevisions 0; selfRepairRounds 0; usage `{requests 0, note "no model calls consumed; no capsule submitted"}`.

### FILE INVENTORY
```
cpp-to-python/handoff-2026-10-02-d09-multi-command-runner-cpp/output/batch/01-frozen/frozen-inputs.md = read
```
Descriptor (notable): the only artifact — a hand-authored freeze record; there is no classification file, no job directory, no result.md, no evaluator manifest.
Directory-state checks: `cpp-to-python/D2-018-*` does not exist; the direction-level listing has no other D2-018 artifact. The case directory **exists** and contains exactly the one file above (not empty, not absent).

### FREEZE / CLASSIFY
- frozen-inputs.md declares sourcePath `.../source/multi_command_runner.cpp`, sourceOs **windows**, the same uppercase hash, shape "runs 3 shell commands sequentially and aggregates output".
- Blocking recorded in the file: source stdout is `{"case":"execution_advanced","ok_count":3,"result":"STEP1|STEP2|STEP12","elapsed_ms":MS}`; `elapsed_ms` is wall-clock, not reproducible between runs, and **not** covered by the server noise tokens (`timestamps`/`temporary-paths`/`ephemeral-ports`) ⇒ §10.16; the program has no other output and no argv branch ⇒ no alternative condition can be frozen.
- The note also logs, as non-blocking, that the program executes shell commands (`cmd /c echo …`, `cmd /c set /a 7+5`) which it judges neutral.
- NOT declared anywhere: model, selected skills, driver/oracle identity, declared cwd/argv/stdin/timeout, targetOs, unfrozen-items list.
- No `classification-N.json` and no `classifier-input.json`; no reclassification attempt. `admissionStatus=NOT_TAKEN` matches the absence of any classifier artifact.

### SOURCE PRECHECK
- No `job-00*` directory exists. Consequently: no exact build command, no build status, no exitCode, no compiler diagnostic, no execution/observation, no cleanup evidence.
- The item json asserts sourceBuild `UNVERIFIED (not run; not submitted)`, consistent with the absence.

### REQUESTS / RESPONSES
- None. No `request*.txt`, no `repair*.txt`, no `*.model.json` of any kind. No failed attempt is recorded (and usage says zero requests).

### SELF-REVIEW
- None. No `self-review-N.json`, no review prompt.

### JOBS
- None. No `job-NN` directory, therefore no `input_profile.json`, `comparison_manifest.json`, `metadata.json`, `job-id*.txt`, returned evidence, `comparison.json`, `evaluation_report.json/.md`, `controller.log`, `closure.json`, `controller-health*.json`, `report-retry*.json`, and no cleanup evidence.

### RESULT / DELIVERY
- `result.md` **absent**. `evaluator_manifest.json` **absent**. Exactly that: neither file exists for this item.

### ANOMALIES
- Only 1 of the expected artifact classes exists; the case is `FROZEN`/`PARTIAL` with no closure report.
- The freeze→classify→precheck chain stopped at step 1: there is no classification artifact, so the "ALLOWED before precheck/submission" gate was never engaged (consistent with `NOT_TAKEN`).
- The item json asserts `ORACLE_NOT_FREEZABLE` while the freeze note documents only stdout-based reasoning; no run exists to support the claim.
- `manifest.csv` Evidence column says `dual-build-PASS (inherited)` while every item-level verdict is `UNVERIFIED` — an inherited claim with nothing in this copy to support it.

### INDEPENDENT EVIDENCE FACTS
A hand-authored Markdown freeze note supports exactly: an intended cpp-to-python conversion of `multi_command_runner.cpp`, a declared uppercase source hash, and a claimed stdout shape containing a non-reproducible `elapsed_ms`. Nothing in the copy supports any build, run, classification, model call or comparison.

### ATTRIBUTION
- apparatus: missing classification, precheck, job, result and manifest artifacts.
- undetermined: the source facts (hash, stdout shape) cannot be verified because the source file is deleted.

### KNOWLEDGE
- Candidate rule: a case recorded `FROZEN`/`PARTIAL` with a `blockingReason` must still carry the closure artifact set (a result/report plus a freeze record), otherwise it is indistinguishable from an abandoned case. The current contract already requires this: `AGENTS.md` §3 "交付完整性/终态门禁" and `references/framework/delivery-handoff-contract.md` §1.1 (unified closing entry and reporting obligation) — the rule exists and was not applied here.
- Do NOT trust the freeze note's model-style assertion that no alternative condition can be frozen; there is no run evidence.

### OPTIMIZATION
- Give the freeze record the full field set used elsewhere (model, targetOs, cwd/argv/stdin/timeout, classification pointer) so a not-ready item remains auditable.
- Do not put `dual-build-PASS (inherited)` in the manifest Evidence column for an item whose item-json verdicts are all `UNVERIFIED`.

### UNKNOWNS
Whether a build was ever attempted; whether the declared hash matches the deleted source; whether model calls were truly zero; whether `docs/test/...` ever existed in this copy.

---

## D2-019 — cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp

### IDENTITY
- taskId `D2-019`; kind `REUSE`; direction `cpp-to-python`; source `startup_registry_cycle.cpp` (39).
- declared Sha256: `65DAADD88B4BD8BE34E012F11FE716DACCA770693F14D1FEFD03F9D4BC9CFDCF`.
- casePath: `docs/test/dataset-2/cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp`; manifest JobId `eval-20261005-164525-67f1d5c2`; Evidence `dual-build-PASS (inherited)`.
- item json disposition `CONVERTED`; phase `CLOSED`; lifecycle `DONE`; pendingAction `null`; classifier `{2.4, ALLOWED, blockingReason null, cls REVIEW_SIDE_EFFECTS, sha256 009a6f31177b08334663340321494ace1e430de13f8a5687e6843ab26839f3a4}`; sourcePrecheck `{jobId eval-20261011-071746-34b716dc, os windows, buildCommand "g++ -std=gnu++17 startup_registry_cycle.cpp -o program.exe", completed, exitCode 0, SOURCE_BUILDABLE, note "execution completed/0, stdout mode=created"}`; dualBuildJobId `eval-20261011-072115-a57c8912`; verdicts source `completed/0`, target `completed/0 (py_compile)`, execution "both completed/0; stdout byte-identical; stderr empty", comparison "matched (output, diffs=0)", environment `clean`, safety "ALLOWED; no network"; finalTargetSha256 `9bc29c070ebc6f03473aa2c09cf21789de7482117ea90fd54be1c574e1957c5f`; blockingReasons `[]`; codeRevisions 1; selfRepairRounds 0; postEvalRepairRounds 0; coverageGap "only the fresh-tree single-run path (mode=created) is covered; the second-run mode=updated branch, the out/-exists-but-state.txt-missing path and the write-failure path are uncovered; filesystem was not requested"; usage `{promptTokens 2396, completionTokens 13008, reasoningTokens 11187, requests 2, model deepseek-flash, failedAttempts 0}`.

### FILE INVENTORY (29)
```
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/01-frozen/classifier-input.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/01-frozen/classification-1.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/02-conversion/request.system.txt = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/03-self-review/review.system.txt = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/03-self-review/self-review-1.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/03-self-review/self-review-1.model.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-00-source-buildability/input_profile.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-00-source-buildability/metadata.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-00-source-buildability/job-id.txt = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/controller.log = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json = read(trunc>2000)
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json = read(trunc>2000)
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-target.json = read(trunc>2000)
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/input_profile.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/metadata.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/job-id.txt = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/batch-authorization.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/this-task-classification.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/controller-health-before.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json = read(trunc>2000)
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json = read(trunc>2000)
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json = read(trunc>2000)
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/evaluator_manifest.json = read
cpp-to-python/handoff-2026-10-02-d09-startup-registry-cycle-cpp/output/batch/result.md = read
```
(29 entries: 12 in job-00 including `returned-evidence`, 12 in job-01 including `controller-health-before.json` and `returned-evidence`, plus 5 at `01-frozen`/`02-conversion`/`03-self-review` and 2 at batch level.)
Notable files: `self-review-1.model.json` — metadata-only, no response body; `evidence-target.json` (job-00) — placeholder target run; `evaluator_manifest.json` — hand-authored adapter manifest.

### FREEZE / CLASSIFY
- No dedicated `frozen-inputs.md`; freeze facts appear in `02-conversion/request.system.txt`, `04-evaluation/job-01-dual-build/metadata.json` and `result.md`.
- sourcePath `source/startup_registry_cycle.cpp`; sourceSha256 `65daadd8…` (lower in classifier files) / `65DAADD8…` (upper in manifest and classifier-input); sourceOs **windows**; targetOs **windows**; model `deepseek-flash`; cwd `workspace`; argv `[]`; stdin `null`; timeoutSeconds 30; observation dimensions `["output"]`; comparisonPolicy stdoutMode `normalized-text`, stderrMode `exact`.
- NOT declared anywhere: selected skills, driver identity, explicit oracle object (the oracle is only evidenced by the source-precheck stdout), unfrozen-items list.
- `classification-1.json`: classifierVersion 2.4, cls `REVIEW_SIDE_EFFECTS`, reason `local_effects_require_review`, reviewGroups `[filesystem, process]`, files `run_case.py` (sha `87470819…`, process signals) and `startup_registry_cycle.cpp` (sha `65daadd8…`, filesystem signals), admissionStatus **ALLOWED**, blockingReason `null`, requiresNetworkIsolation false, requiresSyntheticData false, classifierSha256 `009a6f31177b08334663340321494ace1e430de13f8a5687e6843ab26839f3a4`, inputManifestSha256 `5ff4e4d47ff94216246f1e36d60872822a90b48c487eeb54694fa4b1f674e2b7`, old_cls/old_reason null. `executable: false` while `executionApproved: true`.
- No reclassification attempt.

### SOURCE PRECHECK
- job-00 dir; job id `eval-20261011-071746-34b716dc` (job-id.txt).
- Exact build command: `g++ -std=gnu++17 startup_registry_cycle.cpp -o program.exe` on `windows-vm-agent-x64`, snapshot `CC-Eval-Windows-8Lang-1.0.28`.
- Build status `completed`, exitCode 0, durationMs 2845; compiler stdout and stderr both empty (digest `sha256:e3b0c442…` = the empty-string SHA-256) ⇒ no diagnostic text.
- Execution: `completed`, exitCode 0, durationMs 249, timedOut false; stdout exactly `{"case":"persistence_advanced","entries":3,"mode":"created"}\n` (62 bytes, digest `fd55bb68…`), structuredValue `{case: persistence_advanced, entries: 3, mode: created}`; stderr empty (empty digest).
- Cleanup evidence: `evaluation_report.json` records for both run roles `preflight {status PASSED, attempts 1, failure null}`, `cleanup {status PASSED, attempts 1, failure null}`, `contaminated false`, `environmentStatus clean`, `runnerStateAfter READY`.
- Same job also executed a **target placeholder** and its outcome block reads runVerdict `partial-runnable`, codeVerdict `failed`, behaviorVerdict `mismatched`, evidenceCoverage matchedDimensions 0 / mismatchedDimensions 1. This is an apparatus placeholder mismatch, not a conversion finding.

### REQUESTS / RESPONSES
- `request.system.txt` holds the **full** converter instruction text (Chinese): target Python 3 single file, output only a ```python block, byte-exact stdout/stderr + exit code, `out = cwd/out/persistence_advanced` with recursive mkdir, the CSV header `name,command,trigger,enabled` + 3 rows, the `state.txt` mode state machine (default `created`; existing file first line `created` ⇒ `updated`, else `created`; truncate-write `<mode>\n`), stdout exactly one line `{"case":"persistence_advanced","entries":3,"mode":"<mode>"}`, `return 0`, toolchain `python -m py_compile target.py`, run `python run_case.py`. Not source code, not an excerpt, not redacted.
- `review.system.txt` holds the **full** reviewer instruction text (6 numbered checks) and the required JSON output shape.
- `self-review-1.model.json` is **metadata-only** — `taskId D2-019`, `stage SELF_REVIEWED`, `reviewN 1`, `model "deepseek-flash"`, `finishReason "stop"`, `requestSha256 633b5f2fc66470edf6f670d85e5f37ad521e762eb412ee9e1a72ab89ef2856f5`, `rawResponseSha256 c9c55fb7887139630619a55337d67816f0a70b54a56a6e7d0649eac10176902d`, `usage {promptTokens 1223, completionTokens 11646, reasoningTokens 10155, totalTokens 12869}`, `maxTokensFieldSent false`, `verdict NO-REPAIR-IDENTIFIED`, `note "Static review only; not a compile or behavior conclusion."`. **No response body is present**; the parsed review text lives in `self-review-1.json`.
- There is **no conversion-stage `*.model.json`**, so the generation call has neither metadata artifact nor body. Parent/final hash linkage for the generation is therefore unavailable.
- Failed attempts: none recorded (`usage.failedAttempts 0`).

### SELF-REVIEW
- `self-review-1.json`: verdict `NO-REPAIR-IDENTIFIED`; reviewedScope = static comparison of `startup_registry_cycle.cpp` (C++17) with `target.gen.py` (Python 3, windows, `py_compile` passed) under frozen argv `[]`, fresh role tree (`out/` absent), source-observed stdout `{"case":"persistence_advanced","entries":3,"mode":"created"}` + newline, empty stderr, exit 0; checks 1–6.
- Items: (1) directory/file paths — no difference, origin `undetermined`, risk low; (2) CSV header + 3 rows byte-identical — no difference; (3) `state.txt` state machine incl. empty-file and no-newline edges — no difference; (4) stdout one line with `mode` interpolated not hardcoded — no difference, but origin `toolchain-unknown`, risk low, with the one genuine unresolved technical observation: on Windows C++ `std::cout` text mode converts `'\n'` to CRLF whereas CPython stdout is normally opened with `newline='\n'`, so a strict un-normalized raw-byte comparison could differ by one CR; the review explicitly declines to propose a change; (5) `return 0`/`sys.exit(0)`, empty stderr, no traceback — no difference; (6) nothing added beyond the source's three behaviours — no new behaviour.
- Knowledge/rule suggestions: none. `proposed_fix` is `null` in all six items.
- No repair artifacts: no `target.self-repair-*.model.json`, no proposal json, no parent/final hashes, no changed-line note (none were triggered).

### JOBS
- **job-00** (`job-00-source-buildability`): `input_profile.json` (argv `[]`, stdin null, cwd `workspace`, timeout 30, dimensions `["output"]`, comparisonPolicy output stdoutMode normalized-text / stderrMode exact, no fixtures, profileId `D2-019`); `comparison_manifest.json` (caseId `D2-019`; source arch x64, artifactLanguage cpp, buildCommand `g++ -std=gnu++17 startup_registry_cycle.cpp -o program.exe`, os windows, runCommand `python run_case.py`; target x64/python/`python -m py_compile target.py`/windows); `metadata.json` (sourceHash `sha256:65daadd8…`, targetArtifact `target/target.py (placeholder)`, targetHash `sha256:placeholder-precheck`); `job-id.txt`; `batch-authorization.json`; `this-task-classification.json` (same classification 2.4 ALLOWED); `returned-evidence/{controller.log, evaluation_report.json, evidence-source.json, evidence-target.json}`. Observed: source real build 0 / real run 0 with the 62-byte stdout; target placeholder `D2-019 placeholder\n` (20 bytes) exit 0. **No controller-health files for job-00.**
- **job-01** (`job-01-dual-build`): configs as listed; `metadata.json` sourceHash `sha256:65daadd8…`, targetHash `sha256:9bc29c07…`; `job-id.txt` `eval-20261011-072115-a57c8912`; `controller-health-before.json` and `returned-evidence/controller-health-after.json` both `{status ok, service remote-host-controller, version 1.0.0, contractSetHash sha256:a9ed1445…, ready true, runnerMode agent, runnerReadiness {executionReady true, readyRunnerCount 3, blockedRunnerCount 0, runnerCount 3, blockingReasons []}}`; `controller.log` `[2026-10-11T07:21:15.366488+00:00] comparison job created` → `[2026-10-11T07:22:35.951330+00:00] comparison job finished`; `evidence-source.json` and `evidence-target.json` both show execution `completed`, exitCode 0, stderr empty, and **identical** stdout 62 bytes / digest `fd55bb68…`; `comparison.json` `sourceBundleId evb-source-eval-20261011-072115-a57c8912`, `targetBundleId evb-target-…`, `behaviorVerdict "matched"`, dimensions.output `{status matched, applicable true, observed true, diffs []}`, all other dimensions `not-applicable`; `evaluation_report.json` `jobStatus COMPLETED`, `jobPhase FINISHED`, runVerdict `runnable`, codeVerdict `passed`, behaviorVerdict `matched`, environmentStatus `clean`, coverageRatio 1.0, failure null; `evaluation_report.md` PASS / MATCHED / CLEAN, 1/1/1/0/0 coverage 100%, both runs windows/x64 with preflight+cleanup PASSED, contaminated no, runner state after READY.
- No `closure.json` and no `report-retry*.json` anywhere. Cleanup evidence exists only as the lifecycle blocks (preflight/cleanup PASSED, contaminated false, READY) — there is no separate cleanup artifact.

### RESULT / DELIVERY
- `result.md` present: four-row summary (delivery complete "root target.py + five stage dirs + two job evidence"; syntax/compile PASS both sides; functional consistency "matched within the agreed scope" via job-01; safety compliant, no network, filesystem not compared). It records the freeze (argv `[]`, fresh role trees on both sides), zero repair rounds, final state (byte-identical stdout, empty stderr, exit 0), a round/usage table (generation prompt 1173 / completion 1362 / reasoning 1032; self-review 1223/11646/10155; no `max_tokens`), the two jobs, the §10.6 acceptance check (non-empty, non-degenerate source observation), the explicit statement that the **filesystem dimension was not requested** and byte-equality of the produced files is **not** claimed, three uncovered paths, and one open item (the `mode=updated` branch needs a new frozen condition).
- `evaluator_manifest.json` present: hand-authored (`generatedBy "code_convert-temporary-controller-adapter (hand-authored)"`), languagePair cpp→python, taskMetadata `{attackTactic none, sceneTags [file-io], sourceOs windows, targetOs windows, x64/x64, riskLevel low, evidenceMode static-and-runtime, supportLevel experimental}`, targetDir and plannedResultPath under `docs/test/dataset-2/...`, `files[0]` relativePath `target.py` with hasSource/hasTranslatedCode true, x_adapter `{status "converted-and-evaluated", executionApproved true, jobId eval-20261011-072115-a57c8912, explorationOnly false}`.
- Claims vs evidence: the matched comparison, both builds' exit 0 and the clean environment are corroborated by the returned bundles. The "delivery complete" claim cannot be checked against `target.py` because the target file is deleted in this copy.

### ANOMALIES
- No conversion-stage `*.model.json` although result.md reports a round-1 generation with real token counts — the generation response metadata/body is missing.
- job-00's report asserts `behaviorVerdict mismatched` with `sufficientDimensions 1` against an explicitly labelled placeholder target; this could be misread as a real failure.
- Five single-line bundles truncated at 2000 characters (tails unverifiable).
- `result.md` and `evaluator_manifest.json` point at `output/batch/target.py`, which does not exist in this copy.
- job-00 has no `controller-health-before.json` (job-01 has both before and after).

### INDEPENDENT EVIDENCE FACTS
A real Windows `g++` build of `startup_registry_cycle.cpp` exited 0 with empty compiler output (two runs: durationMs 2845 and 14030). A real Windows execution exited 0 and produced exactly the 62-byte stdout `{"case":"persistence_advanced","entries":3,"mode":"created"}` with empty stderr. A second job produced the same 62-byte stdout on both sides with matching digests and comparison output `diffs []`. All lifecycle fields report preflight/cleanup PASSED, contaminated false, environment clean, runner READY. No filesystem comparison was ever performed.

### ATTRIBUTION
- source-existing: the matched stdout behaviour and exit code (the target reproduced the observed source behaviour).
- apparatus: missing generation metadata, the placeholder-mismatch in job-00, absent closure/report-retry artifacts, absent `target.py`.
- environment/toolchain: the CRLF-versus-LF stdout question raised in self-review item 4 — undetermined until negotiated; in fact the comparator used normalized text.

### KNOWLEDGE
- Candidate rule: every item that consumed a model request must persist the generation-stage response metadata (`target.gen.model.json`), otherwise the conversion call is unauditable. Current contract: `references/framework/task-state-contract.md` §2.1 (version linkage) and §2.3 (knowledge loading vs actual consumption) require the request/response/version association; `AGENTS.md` §8 requires the per-40-item reconciliation to intersect self-review, request/response metadata, failed attempts, events and item json.
- Candidate practice: a precheck job whose report reads `behaviorVerdict=mismatched` against a labelled placeholder should be labelled apparatus-only wherever quoted; `AGENTS.md` §5 (layer separation, do not synthesize a single success rate) and §7 (check before concluding) support this.
- Do NOT treat self-review item 4 (CRLF) as a defect: no counterexample exists and the comparator normalizes text. `AGENTS.md` §7 requires evidence before declaring a defect.

### OPTIMIZATION
- Add `controller-health-before.json` to precheck jobs for symmetry.
- Record the classifier version→SHA mapping once centrally; v2.4 appears with SHA `009a6f31…` here.
- Keep the placeholder run out of the same job as the source precheck where possible, or mark it in the job folder name.

### UNKNOWNS
Whether `target.py` really hadhes to `9bc29c07…` (file deleted); the truncated tails of the five bundles (observations / artifacts / cleanup); whether a closure record exists outside this copy.

---

## D2-020 — cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp

### IDENTITY
- taskId `D2-020`; kind `REUSE`; direction `cpp-to-ruby`; source `kv_request_audit.cpp` (42).
- declared Sha256: `D290C4BA44991587EADEDC4092CAE15503C45729844160860C4C338281CFE9A0`.
- casePath: `docs/test/dataset-2/cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp`; manifest JobId `eval-20261005-164858-bd15731f`; Evidence `dual-build-PASS (inherited)`.
- item json disposition `FROZEN`; phase `CLOSED`; lifecycle `DONE`; targetSha256 `ed455bbcf108fbdd22c1627c65c498922fa1a3fbcd0950b778226d1ad09ea579`; classifier `{version 2.3, ALLOWED, blockingReason null, cls REVIEW_SIDE_EFFECTS, networkMode "none-detected", sha256 441b4d50125071544f6d1bbe836b7258d692c37c638acdb678a9e88795366524}`; sourcePrecheck `{jobId eval-20261010-075056-09a5abb1, os linux, buildCommand "g++ -std=gnu++17 kv_request_audit.cpp -o program", completed, exitCode 0, execution completed/0, observed argv [] exit 0 stdout "{\"case\":\"initial_access_advanced\",\"accepted\":true,\"reason\":\"ok\"}"}`; evaluation `{jobId eval-20261010-075357-22e1d5f6, verdict matched, outputDiffs 0, accepted true, stdoutDigestsIdentical true, gate "passes discipline 10.6: source observation non-empty and non-degenerate"}`; verdicts sourceBuild `completed/0`, targetBuild `PASS (ruby -c, completed/0)`, execution both exit 0, comparison `matched (output, 0 diffs)`, environment clean, safety ALLOWED; fixtureSymmetry "data/inbox/request_v2.txt is byte-identical on both sides. All values are synthetic; no real credential is present."; coverageGaps list of 7; codeRevisions 0; selfRepairRounds 0; usage `{requests 1, note "one conversion call; self-review NO-REPAIR-IDENTIFIED"}`; blockingReasons `[]`.

### FILE INVENTORY (19)
```
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/01-frozen/classification-1.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/01-frozen/classifier-input.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/03-self-review/self-review-1.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-00-source-buildability-linux/input_profile.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-00-source-buildability-linux/comparison_manifest.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-00-source-buildability-linux/metadata.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evaluation_report.json = read(trunc>2000)
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evidence-source.json = read(trunc>2000)
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-01-dual-build/input_profile.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-01-dual-build/metadata.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json = read(trunc>2000)
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md = read
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json = read(trunc>2000)
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json = read(trunc>2000)
cpp-to-ruby/handoff-2026-10-02-d11-kv-request-audit-cpp/output/batch/result.md = read
```
Missing and notable: `01-frozen/frozen-inputs.md` = **missing**; `02-conversion/request*.txt`, `repair*.txt` = **missing**; every `*.model.json` = **missing**; both job dirs lack `job-id.txt`; job-00 lacks `controller.log` and any target bundle; job-01 lacks `controller-health-before.json`; `evaluator_manifest.json` = **missing**. The comparison bundle `evidence-target.json` (job-01) is present and real (not a placeholder).

### FREEZE / CLASSIFY
- No `frozen-inputs.md`. Reconstructed freeze facts: sourcePath `source/kv_request_audit.cpp`; hash `D290C4BA…` uppercase in manifest/classifier-input/job-01-metadata and lowercase `d290c4ba…` in classification-1; sourceOs/targetOs **linux**; model `deepseek-flash`; cwd `workspace`; argv `[]`; stdin null; timeout 30; dimensions `["output"]`; stdoutMode `normalized-text`, stderrMode `exact`; oracleBasis = source-precheck exit 0 and its stdout (job-01 metadata); fixture `data/inbox/request_v2.txt` byte-identical both sides (`token=ALLOW_TEST;version=2;source=lab_vm` plus newline).
- `classification-1.json`: version **2.3**, cls `REVIEW_SIDE_EFFECTS`, reason `local_effects_require_review`, reviewGroups `[filesystem]`, single file `kv_request_audit.cpp` (sha `d290c4ba…`, filesystem signals), admissionStatus **ALLOWED**, blockingReason null, requiresNetworkIsolation false, requiresSyntheticData false, classifierSha256 `441b4d50125071544f6d1bbe836b7258d692c37c638acdb678a9e88795366524`, inputManifestSha256 `1d794f79fb70dd4251e6705bc0f06c57e0abbf15d10288f34a04c6073b638320`, limitations `lexical_heuristics_not_dataflow`, `target_driver_dependencies_not_assessed`, `isolation_and_authorization_not_assessed`.
- No reclassification attempt. Selected skills / driver identity / unfrozen-items list undeclared.

### SOURCE PRECHECK
- job-00 dir; job id `eval-20261010-075056-09a5abb1` (from the report; no `job-id.txt`).
- Build command `g++ -std=gnu++17 kv_request_audit.cpp -o program` on `linux-vm-agent-x64`, snapshot `CC-Eval-Linux-8Lang-1.0.26`; status `completed`, exitCode 0, durationMs 724; compiler stdout/stderr empty (empty digest).
- Execution `completed`, exitCode 0, durationMs 33; stdout `{"case":"initial_access_advanced","accepted":true,"reason":"ok"}\n` (65 bytes, digest `e17e9eb3…`), stderr empty.
- Cleanup: report shows source and target `preflight {PASSED, 1, null}` and `cleanup {PASSED, 1, null}`, contaminated false, environmentStatus clean, runnerStateAfter READY.
- The same job also ran a **ruby placeholder** (`ruby -c placeholder.rb`) and its outcome block reads runVerdict `partial-runnable`, codeVerdict `failed`, behaviorVerdict `mismatched` — apparatus.

### REQUESTS / RESPONSES
- No `request*.txt` and no `repair*.txt`: the converter instruction text that produced `target.rb` is **not in this copy**.
- No `*.model.json` at all — neither conversion-stage nor self-review metadata. Model identity, `finish_reason`, token usage, parent/final hashes and any response body are therefore absent; only result.md and the item json assert `deepseek-flash` and `requests 1`. No failed-attempt artifact.
- The parsed review survives as text in `self-review-1.json` even though its metadata file does not.

### SELF-REVIEW
- `self-review-1.json`: `taskId D2-020`, `round 1`, `reviewer "agent-static"`, verdict `NO-REPAIR-IDENTIFIED`.
- `checks` (quoted keys): `first-line-only` (Ruby `f.gets` matches `std::getline`, trailing LF stripped by `sub(/\n\z/,'')`), `missing-key-default` (`Hash.new("")` reproduces `std::map::operator[]` default-constructing an empty string), `duplicate-keys` (later assignment overwrites, as `std::map`), `split-rules` (`split(';')` then `index('=')` with a nil guard vs `getline(iss, part, ';')` + `find('=')` + npos skip), `reason-precedence` (bad_token → bad_version → bad_source → ok), `accepted-expression` (`token_ok && version_ok && source_ok`), `audit-line` ("appended in exactly 'raw=<raw> accepted=<1|0> reason=<reason>' plus newline, with the ternary rendering 1/0 as the C++ does"), `stdout` (the JSON line with true/false and the reason), `dependency` ("fileutils only, which is stdlib").
- `residualRisks`: only the accept path is exercised by the shipped fixture; bad_token/bad_version/bad_source implemented but unverified; the req-absent path implemented but not exercised; the audit log is appended so repeated runs accumulate lines and its content is not compared (output-only observation); CRLF input not considered — `std::getline` strips only LF and Ruby does the same, so they agree but neither was tested.
- `limitations`: "static review only; not execution evidence". `decision`: "proceed to evaluation-ready check". No knowledge/rule suggestions; no repair artifacts.

### JOBS
- **job-00** (`job-00-source-buildability-linux`): `input_profile.json` (profileId `batch-d2-020-cpp-to-ruby-precheck`; argv `[]`, stdin null, cwd workspace, timeout 30, dimensions `["output"]`, stdoutMode normalized-text / stderrMode exact); `comparison_manifest.json` (caseId `batch-d2-020-cpp-to-ruby-precheck`; source linux/cpp `g++ -std=gnu++17 kv_request_audit.cpp -o program`; target linux/ruby `ruby -c placeholder.rb`); `metadata.json` (batchId batch, taskId D2-020, purpose "source precheck only", note about the identical fixture); `returned-evidence/evaluation_report.json` and `evidence-source.json`. Observed: real source build 0 / real run 0 with the 65-byte stdout. **No `job-id.txt`, no `controller.log`, no controller-health, no target bundle.**
- **job-01** (`job-01-dual-build`): `input_profile.json` (profileId `batch-d2-020-cpp-to-ruby-kv-audit`); `comparison_manifest.json` (source linux/cpp same g++ line; target linux/ruby `ruby -c target.rb`); `metadata.json` (sourceLang C++, targetLang Ruby, sourceSha256 uppercase, targetFile `target.rb`, `targetOrigin "deepseek-flash (project .env model); agent did not author target code"`, classification `{ALLOWED, blockingReason null, cls REVIEW_SIDE_EFFECTS}`, sourcePrecheckJobId, `frozenArgv []`, `frozenStdin null`, oracleBasis, fixtureSymmetry, note "No credentials included. The fixture values are synthetic."); `returned-evidence/comparison.json` (`behaviorVerdict matched`, `dimensions.output {matched, applicable, observed, diffs []}`, other dimensions not-applicable); `controller-health-after.json` (`status ok`, `ready true`, `contractSetHash sha256:e088a356b48fd1c3f50e480ac24c2fd03319dc60a49b41de4d076219819c4c45`, 3/3 runners, checkedAt 2026-10-10T07:55:40.328797+00:00); `controller.log` (`07:53:57.282056` created → `07:54:52.320622` finished); `evaluation_report.json` (COMPLETED/FINISHED, runVerdict runnable, codeVerdict passed, behaviorVerdict matched, environmentStatus clean, coverageRatio 1.0, failure null); `evaluation_report.md` (PASS/MATCHED/CLEAN, linux/x64, preflight+cleanup PASSED on both runs, contaminated no, runner state after READY, coverage 1/1/1/0/0 100%, matrix Output matched, everything else not-applicable); `evidence-source.json` and `evidence-target.json` (observed stdout both sides).
- No `closure.json`, no `report-retry*.json`. Cleanup evidence exists only as the report's lifecycle blocks.
- **No `job-id.txt` in either job dir**, so the job ids come only from the reports and metadata.

### RESULT / DELIVERY
- `result.md` present and layered: delivery completeness "完成 — 证据 7 份落盘"; target syntax/compile PASS (`ruby -c target.rb` → `completed/0`); source baseline PASS (`g++ -std=gnu++17` → `completed/0`, exec 0); execution PASS; functional consistency **matched** (output diffs 0, identical stdout digest); environment clean (both preflight/cleanup PASSED); safety ALLOWED under `REVIEW_SIDE_EFFECTS` / `network_mode=none-detected`. It asserts the fixture is byte-identical on both sides and all values synthetic, presents a table of seven easily-mistaken semantics correctly handled (missing key, duplicate key, first-line only, part without `=`, split on the first `=`, reason precedence, `accepted` as 1/0), a two-job evidence table, and seven coverage gaps, concluding that the behaviour result holds only for "linux, no args, valid fixture" and does not mean the rejection-path logic is equivalent.
- `evaluator_manifest.json` **absent** — exactly that: D2-020 has no evaluator manifest file.

### ANOMALIES
- **No `frozen-inputs.md`** despite disposition `FROZEN` and despite request/review prompt files being required reading for the freeze step.
- Field contradiction: item json disposition `FROZEN` with phase `CLOSED` / lifecycle `DONE`.
- **No `*.model.json` at all** although `usage.requests = 1`: no model identity, finish reason, token usage or failed-attempt record; result.md's `deepseek-flash` claim is uncorroborated in this copy.
- No `job-id.txt` in either job dir; no `evaluator_manifest.json`; job-00 lacks `controller.log` and target evidence; job-01 lacks `controller-health-before.json`.
- Six single-line bundles truncated at 2000 characters.
- job-00's report reads `failed` / `mismatched` against a placeholder.

### INDEPENDENT EVIDENCE FACTS
A real Linux `g++` build exited 0 with empty diagnostics; a real Linux execution exited 0 and produced exactly the 65-byte stdout `{"case":"initial_access_advanced","accepted":true,"reason":"ok"}` with empty stderr; a second job produced matched output on both sides with `diffs []` and identical stdout digests; both jobs report preflight/cleanup PASSED, contaminated false and runner READY; controller health ok with 3/3 runners. The three rejection branches, the req-absent path, duplicate keys, a part without `=`, the appended audit-log content and CRLF input were never observed.

### ATTRIBUTION
- source-existing: the build/execution/compare evidence (the target reproduced the observed accept-path behaviour).
- apparatus: the `FROZEN`-versus-`DONE` field conflict, every missing freeze/model/job-id/manifest artifact, the placeholder run.
- undetermined: any finer source-versus-conversion distinction, because the target code is deleted.

### KNOWLEDGE
- Candidate rule: `phase CLOSED` must be mutually exclusive with disposition `FROZEN`; otherwise "frozen" statistics over-count finished items. Current contract: `references/framework/task-state-contract.md` (lifecycle/disposition semantics) and `AGENTS.md` §3 (terminal-state gate) already keep these notions distinct; the item violates the intended separation.
- Candidate rule: whenever `usage.requests >= 1`, a model-metadata artifact must exist. Current contract: `AGENTS.md` §8 (reconciliation must cover request/response metadata and failed attempts) and task-state-contract §2.1.
- Do NOT accept `dependency: fileutils only, which is stdlib` as validated — it is an unverified static claim.

### OPTIMIZATION
- Put the runner OS in metadata rather than a `-linux` suffix on the job directory (job-00 has the suffix, job-01 does not).
- Write `job-id.txt` in every job dir so the id is not buried in reports.

### UNKNOWNS
Model identity/usage for the single conversion call; the converter prompt content; whether an evaluator manifest ever existed; the truncated tails of six bundles.

---

## D2-021 — cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp

### IDENTITY
- taskId `D2-021`; kind `REUSE`; direction `cpp-to-ruby`; source `loopback_ack_probe.cpp` (49).
- declared Sha256: `B432966FC55671B2B5A71F12EBA2FB9EFE20C81424DDD99559A217267E05F0C0`.
- casePath: `docs/test/dataset-2/cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp`; manifest JobId `eval-20261005-165326-2bc85611`; Evidence `dual-build-PASS (inherited)`.
- item json disposition `FROZEN`; phase `CLOSED`; lifecycle `DONE`; targetSha256 `bc684f5f10903a789f1a27127f636f582be53022151a546a6043ea2ad0ef1796`; classifier `{version 2.3, ALLOWED, blockingReason null, cls REVIEW_NETWORK, networkMode loopback, networkTargets [{value 127.0.0.1, line 31, scope loopback, provenance literal, redirectVerified false}], sha256 441b4d50125071544f6d1bbe836b7258d692c37c638acdb678a9e88795366524, blockedAttempts [{attempt 1, BLOCKED, input_error, source_hash_mismatch}, {attempt 2, BLOCKED, input_error, source_hash_mismatch}], resolution "the sha256 had been submitted in lowercase while the manifest records it in uppercase; the classifier compares case-sensitively. Resubmitted verbatim from the manifest."}`; `misidentifiedAs {wrongId D2-182, note "D2-182 is virtualallocex_hack.c (c-to-ruby); the loopback probe directory is D2-021. The wrongly created staging directory was deleted and no submission was made under the wrong id."}`; sourcePrecheck `{jobId eval-20261010-074602-1c50c355, os linux, buildCommand "g++ -std=gnu++17 loopback_ack_probe.cpp -o program", completed, exitCode 0, execution completed/0, observed argv [] exit 0 stdout "{\"case\":\"lateral_movement_advanced\",\"ok\":false,\"reason\":\"windows_only\"}"}`; evaluation `{jobId eval-20261010-074839-f1c89edf, verdict matched, outputDiffs 0, accepted true, stdoutDigestsIdentical true, gate "passes discipline 10.6: source observation non-empty and non-degenerate"}`; verdicts targetBuild `PASS (ruby -c, completed/0)`, comparison matched, environment clean, safety "ALLOWED (loopback only, and the branch is not taken on linux)"; coverageGaps list of 4; codeRevisions 0; selfRepairRounds 0; usage `{requests 1, note "one conversion call; self-review NO-REPAIR-IDENTIFIED"}`; blockingReasons `[]`.

### FILE INVENTORY (20)
```
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/01-frozen/classification-1.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/01-frozen/classification-2.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/01-frozen/classifier-input.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/03-self-review/self-review-1.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-00-source-buildability-linux/input_profile.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-00-source-buildability-linux/comparison_manifest.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-00-source-buildability-linux/metadata.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evaluation_report.json = read(trunc>2000)
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-00-source-buildability-linux/returned-evidence/evidence-source.json = read(trunc>2000)
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-01-dual-build/input_profile.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-01-dual-build/metadata.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json = read(trunc>2000)
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md = read
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json = read(trunc>2000)
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json = read(trunc>2000)
cpp-to-ruby/handoff-2026-10-02-d11-loopback-ack-probe-cpp/output/batch/result.md = read
```
Notable: `classification-1.json` — the BLOCKED/input_error attempt; `classification-2.json` — the ALLOWED attempt. Missing: `01-frozen/frozen-inputs.md`; `02-conversion/request*.txt`, `repair*.txt`; every `*.model.json`; `job-id.txt` in both job dirs; job-00's `controller.log` and target bundle; job-01's `controller-health-before.json`; `evaluator_manifest.json`.

### FREEZE / CLASSIFY
- No `frozen-inputs.md`. Reconstructed: sourcePath `source/loopback_ack_probe.cpp`; hash `B432966F…` upper (manifest, classifier-input, job-01 metadata, classifier-2 nested file entry is lowercase) vs `b432966f…` lower in classification-2; sourceOs/targetOs **linux**; model `deepseek-flash`; cwd `workspace`; argv `[]`; stdin null; timeout 30; dimensions `["output"]`; stdoutMode normalized-text / stderrMode exact; oracleBasis = source-precheck exit 0 + the `windows_only` stdout; safety note "the only network target is loopback 127.0.0.1:9001 and on linux the branch is not even taken; no external target is reachable".
- **Reclassification pair survives.** `classification-1.json`: cls `BLOCKED_INPUT`, reason `source_incomplete_or_invalid`, reviewGroups `[]`, files `[]`, inputErrors `[{file loopback_ack_probe.cpp, type ValueError, reason source_hash_mismatch}]`, executionApproved false, admissionStatus **BLOCKED**, blockingReason `input_error`, classifierVersion 2.3, classifierSha256 `441b4d50…`, inputManifestSha256 `d8bbc6e311ea6ff176eb8fffb2ea2a7b69a8eccd145ab058d1323ad685cba813`. `classification-2.json`: cls `REVIEW_NETWORK`, reason `network_scope_and_inputs_require_review`, reviewGroups `[network]`, file `loopback_ack_probe.cpp` with network signals [22, 33] and target `127.0.0.1` line 31 scope loopback provenance literal `redirectVerified false`, executionApproved true, admissionStatus **ALLOWED**, blockingReason null, classifierVersion 2.3, classifierSha256 `441b4d50…`, inputManifestSha256 `f31196125716d993c6c688324f955f998e555c775ca5d553b7641105b74295d5`.
- The item json records **two** BLOCKED attempts; only **one** BLOCKED-verdict file exists, so at least one attempt has no artifact.
- Selected skills / driver identity / unfrozen-items list undeclared.

### SOURCE PRECHECK
- job-00 dir; job id `eval-20261010-074602-1c50c355` (from report/metadata; no `job-id.txt`).
- Build `g++ -std=gnu++17 loopback_ack_probe.cpp -o program` on `linux-vm-agent-x64`, snapshot `CC-Eval-Linux-8Lang-1.0.26`; status `completed`, exitCode 0, durationMs 636; compiler stdout/stderr empty.
- Execution `completed`, exitCode 0, durationMs 35; stdout `{"case":"lateral_movement_advanced","ok":false,"reason":"windows_only"}\n` (72 bytes, digest `8eb1d5b0…`), stderr empty.
- Cleanup: preflight/cleanup PASSED on both run roles, contaminated false, clean, READY.
- Same job also ran a **ruby placeholder** (`ruby -c placeholder.rb`) with outcome `failed` / `mismatched` — apparatus. The job metadata notes "on linux the source hits the #else branch and prints windows_only without any network access".

### REQUESTS / RESPONSES
- No `request*.txt`, no `repair*.txt`, and no `*.model.json` — identical gap to D2-020. Model identity, finish reason, usage, parent/final hashes and any body are absent; the failed classification attempts likewise have no metadata artifact. Only the parsed review survives as text.

### SELF-REVIEW
- `self-review-1.json`: `taskId D2-021`, `round 1`, `reviewer "agent-static"`, verdict `NO-REPAIR-IDENTIFIED`.
- `checks`: `platform-branch` (RUBY_PLATFORM inspected for mingw/mswin; on linux the non-Windows branch runs exactly as the C++ `#else`), `non-windows-output` (prints exactly `{"case":"lateral_movement_advanced","ok":false,"reason":"windows_only"}` and performs no socket work), `windows-branch-shape` ("3 attempts, 150 ms backoff, connect to 127.0.0.1:9001, payload SAFE_HELLO;attempt=<n>, recv, then ok/detail"), `reason-values` ("all five reason strings preserved: wsa_startup_failed, socket_failed, no_listener, connected_no_ack, ack:<data>, plus windows_only"), `key-order`, `exit` ("explicit exit 0").
- `residualRisks`: the Windows branch is implemented but CANNOT be exercised on the linux runner, so it is unverified; C++ ignores `send()`'s return while the Ruby rescues write errors and ignores them — same practical effect; C++ treats a non-positive `recv` as `connected_no_ack` while Ruby rescues a recv error to an empty string, giving the same reason string.
- `limitations`: "static review only; not execution evidence. Only the non-Windows branch is reachable on this runner." `decision`: "proceed to evaluation-ready check". No knowledge suggestions; no repair artifacts.

### JOBS
- **job-00**: `input_profile.json` (profileId `batch-d2-021-cpp-to-ruby-precheck`), `comparison_manifest.json` (source linux/cpp g++ line; target linux/ruby `ruby -c placeholder.rb`), `metadata.json` (purpose "source precheck only (linux)"; note "on linux the source hits the #else branch and prints windows_only without any network access"), `returned-evidence/evaluation_report.json` + `evidence-source.json`. Observed real source build 0 / run 0 with the 72-byte stdout. No `job-id.txt`, no `controller.log`, no controller-health, no target bundle.
- **job-01**: `input_profile.json` (profileId `batch-d2-021-cpp-to-ruby-loopback-ack`), `comparison_manifest.json` (target `ruby -c target.rb`, both sides linux), `metadata.json` (sourceSha256 uppercase; targetFile `target.rb`; targetOrigin "deepseek-flash (project .env model); agent did not author target code"; classification `{ALLOWED, null, REVIEW_NETWORK, networkMode loopback, target "127.0.0.1 line 31"}`; sourcePrecheckJobId; `frozenArgv []`; `frozenStdin null`; oracleBasis; safety; `classificationNote` retelling the lowercase/uppercase hash story; note "No credentials included."), `returned-evidence/comparison.json` (`behaviorVerdict matched`, output diffs `[]`, other dimensions not-applicable), `controller-health-after.json` (ok/ready, contractSetHash `sha256:e088a356…`, 3/3 runners, checkedAt 2026-10-10T07:50:23.859058+00:00), `controller.log` (`07:48:39.651462` created → `07:49:34.039732` finished), `evaluation_report.json` (COMPLETED/FINISHED, runnable/passed/matched/clean), `evaluation_report.md` (PASS/MATCHED/CLEAN, linux/x64, preflight+cleanup PASSED, coverage 1/1/1/0/0 100%), `evidence-source.json` and `evidence-target.json`.
- No `closure.json`, no `report-retry*.json`; cleanup only as lifecycle blocks. **No `job-id.txt` in either job dir.**

### RESULT / DELIVERY
- `result.md` present: delivery "完成 — 证据 7 份落盘"; target syntax PASS (`ruby -c target.rb` → `completed/0`); source baseline PASS (`g++` → completed/0, exec 0); execution PASS; functional consistency matched (output diffs 0, identical stdout digest); environment clean; safety ALLOWED under `REVIEW_NETWORK` / `network_mode=loopback` (127.0.0.1, line 31). It documents a safety-boundary check (the only network target is `127.0.0.1:9001` loopback and the branch is inside `#ifdef _WIN32`, so on Linux no socket is opened), a table of the two `BLOCKED / input_error` classification attempts and the resolution, the root cause (manifest `Sha256` uppercase vs submitted lowercase, classifier case-sensitive; "文件本身的哈希一直是对的，错的是清单里的字符串形式") with a claim of a new discipline **§10.20**, the taskId misidentification (`D2-021`, not `D2-182`, whose source is `virtualallocex_hack.c`; the wrongly created staging directory was deleted and no submission occurred), a two-job evidence table, four coverage gaps, and the conclusion that the result holds only for "linux, no args, non-Windows branch".
- `evaluator_manifest.json` **absent** — exactly that.

### ANOMALIES
- **No `frozen-inputs.md`** despite `FROZEN`, and no `D2-021`-specific freeze artifact.
- `FROZEN` with phase `CLOSED` / lifecycle `DONE`.
- Two BLOCKED classification attempts recorded but only one BLOCKED file; the second attempt's input is unrecoverable.
- **No `*.model.json`** at all (no generation metadata, no body, no usage).
- No `job-id.txt` in either job dir; no `evaluator_manifest.json`; job-00 lacks `controller.log`/target bundle; job-01 lacks `controller-health-before.json`.
- Six single-line bundles truncated at 2000 characters.
- `result.md` asserts a new discipline "§10.20" and a hash-case rule; no such rule text is verifiable inside these six directories — the claim is an agent assertion, not evidence.
- job-00's report reads `failed` / `mismatched` against a placeholder.

### INDEPENDENT EVIDENCE FACTS
A real Linux `g++` build exited 0 with empty diagnostics; a real Linux execution exited 0 with exactly the 72-byte stdout `{"case":"lateral_movement_advanced","ok":false,"reason":"windows_only"}` and empty stderr; a second job produced matched output with `diffs []` on both sides; all lifecycle fields PASSED/clean/READY; controller health ok with 3/3 runners. Nothing was ever executed on Windows, no socket was opened, and no listener existed.

### ATTRIBUTION
- source-existing: the observed behaviour is the source's own `#else` path (the `#ifdef _WIN32` gate and the loopback target are in the source; on Linux the branch is compiled out).
- undetermined: equivalence of the entire Windows branch.
- apparatus: the classification input-case mismatch, all missing freeze/model/job-id/manifest artifacts, the placeholder run.

### KNOWLEDGE
- Candidate rule: classification attempts must be persisted one-to-one (here two blocked plus one allowed should yield three files; only two exist) — exactly what `AGENTS.md` §8 (incremental reconciliation of self-review, request/response metadata, failed attempts, events and item json) is intended to detect.
- Candidate rule: require the freeze record before classification at dispatch time (`AGENTS.md` §3 freeze gate: `01-frozen/frozen-inputs.md` written and read back before classifying).
- Technical fact, not a rule to change blindly: classifier v2.3 compares the submitted hash case-sensitively; either normalize the comparison or treat the manifest as the single source of the exact hash string.
- Do NOT accept result.md's assertion that a new rule (§10.20) was added unless the rule text is located. Current contract: `AGENTS.md` §3 (classification gate `admissionStatus=ALLOWED` and `blockingReason=null`), §8; `references/framework/safety-boundary.md` §1 for the network handling.

### OPTIMIZATION
- Kept a per-attempt naming convention (`classification-1/2/…`) and always write the blocked verdicts.
- Central classifier version→SHA mapping (v2.3 appears with SHA `441b4d50…`).
- Write `job-id.txt` in all job dirs; record the Windows-branch gap as an explicit unfrozen/untested item so it is not folded into `DONE`.

### UNKNOWNS
The second blocked attempt's exact input; model identity/usage; whether the hash-case rule was ever written into the repository (outside these six directories); the truncated tails of six bundles.

---

## D2-022 — csharp-to-python/handoff-2026-10-02-d15-dump-cs

### IDENTITY
- taskId `D2-022`; kind `REUSE`; direction `csharp-to-python`; source `Dump.cs` (127).
- declared Sha256: `02F6A38324CC7A4AEC01D4AD626494C160763CC44899B6F71D7E4BD688FCFB81`.
- casePath: `docs/test/dataset-2/csharp-to-python/handoff-2026-10-02-d15-dump-cs`; manifest JobId `eval-20261005-090913-2c78c08a`; Evidence `dual-build-PASS (inherited)`.
- item json disposition `CONVERTED`; phase `CLOSED`; lifecycle `DONE`; pendingAction `null`; classifier `{version 2.4, ALLOWED, blockingReason null, cls REVIEW_UNCERTAIN, sha256 009a6f31177b08334663340321494ace1e430de13f8a5687e6843ab26839f3a4, note "re-classified after adding the minimal Dump.csproj to the source tree; the second classification covers Dump.cs + Dump.csproj + run_case.py"}`; buildPrerequisite `{agentAddedCsproj true, csprojSha256 "c0c4571a683c..." (truncated), originalMissing "no project file at all", firstAttempt "csc -out:program.exe Dump.cs (build failed, [WinError 2], no csc on the runner)", stillMissingAfter "none - the file is self-contained (ICommand/Helpers/LSA/Dump all in one file)", buildCommand "dotnet build -c Release -o . Dump.csproj"}`; sourcePrecheck `{jobId eval-20261011-072857-e47a1b1c, os windows, completed, exitCode 0, SOURCE_BUILDABLE, note "execution completed/4294967295"}`; dualBuildJobId `eval-20261011-074008-4603ff4a`; verdicts source `completed/0`, target `completed/0 (py_compile)`, execution "both completed/4294967295; stdout now byte-identical after eval-repair-1", comparison "mismatched (platform verdict preserved; residual attributed to device/runtime)", environment clean, safety ALLOWED; finalTargetSha256 `"b2719673f00630dd"` (truncated); codeRevisions 4; selfRepairRounds 1; postEvalRepairRounds 1; repairChain (self-repair-1 "stdout newline bytes (reconfigure(newline='') + explicit CRLF) and enum.Enum"; job-01 `eval-20261011-073711-161c942d` mismatched with counterexample target wrote `(Current User)` instead of `(All Users)` and target stderr empty while the source raised `InvalidOperationException` from `Console.ReadKey` with redirected stdin; eval-repair-1 restored the `All Users` text and mirrored the ReadKey failure first line when stdin is not a TTY; job-02 `eval-20261011-074008-4603ff4a` mismatched with only the .NET runtime stack-trace lines remaining); attribution "…the residual mismatch is entirely the source runtime's stack trace… device difference, not a conversion difference. Platform verdict left unchanged."; coverageGap; usage `{promptTokens 8707, completionTokens 33689, reasoningTokens 28782, requests 4, model deepseek-flash, failedAttempts 0, postEvalRepairBudget "1/2 used"}`; blockingReasons `[]`.

### FILE INVENTORY (41)
```
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/01-frozen/classifier-input.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/01-frozen/classification-1.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/01-frozen/classification-1b.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/01-frozen/frozen-inputs.md = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/02-conversion/request.system.txt = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/02-conversion/repair.system.txt = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/03-self-review/review.system.txt = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/03-self-review/self-review-1.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/03-self-review/self-review-1.model.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-00-source-buildability/input_profile.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-00-source-buildability/metadata.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-00-source-buildability/job-id.txt = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/controller.log = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json = read(trunc>2000)
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json = read(trunc>2000)
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-target.json = read(trunc>2000)
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/input_profile.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/metadata.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/job-id.txt = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/batch-authorization.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/this-task-classification.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/controller-health-before.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json = read(trunc>2000)
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json = read(trunc>2000)
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json = read(trunc>2000)
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/input_profile.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/comparison_manifest.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/metadata.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/job-id.txt = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/batch-authorization.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/this-task-classification.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/controller-health-before.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/returned-evidence/comparison.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/returned-evidence/controller-health-after.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/returned-evidence/controller.log = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/returned-evidence/evaluation_report.json = read(trunc>2000)
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/returned-evidence/evaluation_report.md = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/returned-evidence/evidence-source.json = read(trunc>2000)
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/04-evaluation/job-02-dual-build-eval-repair-1/returned-evidence/evidence-target.json = read(trunc>2000)
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/evaluator_manifest.json = read
csharp-to-python/handoff-2026-10-02-d15-dump-cs/output/batch/result.md = read
```
Notable: `frozen-inputs.md` — the full freeze + build-prerequisite record; `classification-1b.json` — the second classification; `repair.system.txt` — post-eval repair prompt quoting the real counterexamples; `self-review-1.model.json` — metadata-only; `evidence-target.json` (job-01) — the `(Current User)` defect; `evidence-target.json` (job-02) — the repaired target.
Missing: `target.gen.model.json` = **missing**; `target.self-repair-1.model.json` / proposal json = **missing**.

### FREEZE / CLASSIFY
- `frozen-inputs.md`: taskId D2-022, direction csharp-to-python, REUSE; sourcePath `.../source/Dump.cs`; `sourceLines: 146` (manifest/item json say **127** — unreconciled); sourceOs **windows**; source hash `02F6A383…` uppercase; shape "Rubeus-style `Dump` command (`Main()` no args; prints a header, enumerates LSA tickets, ends with `Press any key to exit...`)".
- Build-prerequisite section: the snapshot had only a bare `Dump.cs` and **no project file**; the first measured attempt `csc -out:program.exe Dump.cs` produced `build failed` with stderr `[WinError 2] 系统找不到指定的文件` (no `csc` on the runner); the agent added a minimal neutral `Dump.csproj` with sha256 `C0C4571A683CCEA7A3C2DEEB21041D36B3ED7D516B775C91617723CAAC49FEC1` declaring only `OutputType=Exe`, `TargetFramework=net8.0`, `AssemblyName=program`, `RootNamespace=Rubeus` and `EnableDefaultCompileItems=false` with an explicit `Dump.cs` compile item, introducing no package/namespace/language feature absent from the source; nothing missing after the addition (the file is self-contained: `ICommand` L7, `Helpers` L12, `lib.Interop.LSA` L63, `Commands.Dump` L108); the csproj ships inside the capsule `source/` tree and is classified with the source; build command `dotnet build -c Release -o . Dump.csproj`. It cites `references/workflow/build-prerequisites.md` §2.2/§3 and states the three hard requirements (minimal-neutral / record what was originally missing / hand over with the source).
- Source precheck recorded as `SOURCE_BUILDABLE` after the csproj: job `eval-20261011-072857-e47a1b1c`, `build completed/0`, `execution completed/4294967295`; the frozen source stdout is the 9-line block (header / `Action: …` / `[*] Enumerating real tickets from LSA (native Windows logic)` / blank / `[*] Dumping Kerberos tickets:` / blank / `Press any key to exit...` + newline) with empty stderr.
- Evaluation readiness: argv `[]`; stdin null (the driver starts with an empty input pipe so `Press any key` hits EOF immediately and does not block); output text is deterministically reproducible (a clean VM has no LSA tickets) and the exit code 4294967295 is deterministic ⇒ freezable; uncovered: the per-ticket dump path when tickets exist, and the LSA-unavailable path.
- Classification pair: `classification-1.json` — version 2.4, cls `REVIEW_SENSITIVE`, reason `sensitive_or_dynamic_operations`, reviewGroups `[process, sensitive]`, files `Dump.cs` (process signals 1/2/3, sensitive 18/28) and `run_case.py`, ALLOWED, requiresSyntheticData true, classifierSha256 `009a6f31…`, inputManifestSha256 `cdc781dc3890b92ee748982192ec9025fdc6dd18e2b5e22e7122a87d4666e574`. `classification-1b.json` — version 2.4, cls `REVIEW_UNCERTAIN`, reason `lexical_coverage_incomplete`, reviewGroups `[dynamic_code, process, sensitive]`, files `Dump.cs`, `Dump.csproj` (sha `c0c4571a…`, limitation `unsupported_extension`, dynamic_code signal 21) and `run_case.py`, ALLOWED, requiresSyntheticData true, same classifierSha256 and same inputManifestSha256 (the input manifest did not change even though the file set grew).
- Selected skills / driver identity / unfrozen-items list undeclared.

### SOURCE PRECHECK
- job-00 dir; `job-id.txt` `eval-20261011-072857-e47a1b1c`; metadata marks the target as `target/target.py (placeholder)` with `targetHash sha256:placeholder-precheck`.
- Build `dotnet build -c Release -o . Dump.csproj` on `windows-vm-agent-x64`, snapshot `CC-Eval-Windows-8Lang-1.0.28`; status `completed`, exitCode 0, durationMs 17711. Compiler stdout is **real MSBuild output** (353 bytes, Chinese) including the absolute path `C:\CodeConvertRemote\Stack\Agent\workspaces\eval-20261011-072857-e47a1b1c\source\Dump.csproj` and `…\source\program.dll`, plus "已成功生成。/ 0 个警告 / 0 个错误"; stderr empty.
- Execution: `completed`, exitCode **4294967295**, durationMs 6482, stdout starting `=== Rubeus Dump (Real Ticket Logic, No NuGet) ===\n\nAction: Dump Kerberos Ticket Data (All Users)\n\n[*] Enumerating real tickets from LSA (native Windows logic)\n\n[*] Du…` (tail truncated); stderr empty (empty digest).
- Cleanup: preflight/cleanup PASSED on both run roles, contaminated false, environmentStatus clean, runnerStateAfter READY.
- The same job also ran the **python placeholder** (`D2-022 placeholder\n`, 20 bytes, exit 0) and its outcome block reads runVerdict `partial-runnable`, codeVerdict `failed`, behaviorVerdict `mismatched` — apparatus.
- `controller.log` for job-00: created `07:28:57.731331`, finished `07:30:28.851428`. No controller-health files for job-00.

### REQUESTS / RESPONSES
- `request.system.txt` — the **full** converter instruction text (Chinese): C#→Python single file, only a ```python block, byte-exact stdout/stderr/exit code, `Console.WriteLine(x)` ⇒ write + `\n` equivalently (`print`), the `Press any key to exit...` key read must use `sys.stdin.read(1)` and must not block or throw on a closed pipe, every source method/type (`ICommand`, `Helpers.IsHighIntegrity`, `LSA.EnumerateRealTickets`, `Commands.Dump.Invoke`) must be faithfully mapped without deletion or empty stubs, the exact `Main()` text/order, exit code **4294967295** via `sys.exit(-1)`, platform branches preserved; toolchain `python -m py_compile target.py`; run `python run_case.py`; and the measured 9-line stdout block with the note "(末行后接换行) stderr 空；退出码 4294967295".
- `repair.system.txt` — the **full** post-eval repair prompt: it quotes the real job `eval-20261011-073711-161c942d` counterexample, states difference 1 (source line 3 `Action: Dump Kerberos Ticket Data (All Users)` vs target `(Current User)`) as a real conversion error to fix, states difference 2 (source stderr non-empty: `Unhandled exception. System.InvalidOperationException: Cannot read keys when either application does not have a console or when console input has been redirected. Try Console.Read.` plus `at System.ConsolePal.ReadKey(Boolean intercept)` and `at Program.Main() in <workdir>source\Dump.cs:line 145`) and instructs the target to fail the same way on non-TTY stdin by writing that first line, explicitly says the stack-frame lines contain the absolute working directory and .NET frames and must not be forged, requires preserving `sys.stdout.reconfigure(newline="")` and the explicit `\r\n` writing, and requires output of the complete repaired file in one ```python block.
- `self-review-1.model.json` is **metadata-only**: `taskId D2-022`, `stage SELF_REVIEWED`, `reviewN 1`, `model "deepseek-flash"`, `finishReason "stop"`, `requestSha256 2f3e7bffe48886bfac16999846a344996f5386088b08270dff22d905571af840`, `rawResponseSha256 576376a05844c1a166aa4cbcdf0157a77e2c36d957ab367a19e862d99b0b15ad`, `usage {promptTokens 3287, completionTokens 36471, reasoningTokens 35681, totalTokens 39758}`, `maxTokensFieldSent false`, `verdict REPAIR-RECOMMENDED`, `note "Static review only; not a compile or behavior conclusion."`. **No body**; the parsed review is in `self-review-1.json`.
- There is **no `target.gen.model.json`** (generation response) and **no `target.self-repair-1.model.json`/proposal json** even though the item records `selfRepairRounds 1` and `codeRevisions 4`; result.md implies generation, self-repair-1 and eval-repair-1 model calls. No failed-attempt artifact (`failedAttempts 0`).

### SELF-REVIEW
- `self-review-1.json`: verdict `REPAIR-RECOMMENDED`; reviewedScope "target.gen.py vs Dump.cs, frozen argv=[], Windows, byte-exact stdout, exit code, stdin key read, type mapping, stderr."; 6 items.
- Item 1 (`conversion-introduced`, the substantive finding): C# `Console.WriteLine` writes literal embedded `\n` as LF and appends CRLF on Windows, while Python `print` on Windows translates every `\n` to `os.linesep` (CRLF), so the target emits CRLF for embedded newlines where the source emits LF; issue = byte-level stdout mismatch; proposed_fix = disable newline translation (`sys.stdout.reconfigure(newline='')`) and write exact terminators, or write bytes via `sys.stdout.buffer`; risk = extra `0x0D` bytes before embedded LF.
- Item 2: `sys.exit(-1)` maps to 4294967295 on Windows — no issue. Item 3: `try: sys.stdin.read(1) except Exception: pass` — returns immediately or raises-and-is-caught, no blocking, no traceback — no issue. Item 4 (`conversion-introduced`): `class TicketDisplayFormat(object): Full = "Full"` replaces the source enum `TicketDisplayFormat { Full }`, not a faithful type mapping though not observable under the frozen argv; proposed_fix `class TicketDisplayFormat(enum.Enum): Full = "Full"`; risk low. Item 5: no extra output, `EnumerateTickets` returns `[]` as the source does, no hardcoded ticket data or debug prints — no issue. Item 6: all likely exceptions in `Helpers` and the stdin read are caught, no traceback/warnings, `sys.exit(-1)` is silent — no issue.
- No knowledge/rule suggestions. **No repair artifact survives** (no `target.self-repair-*.model.json`, no proposal json, no parent/final hashes, no changed-line note).

### JOBS
- **job-00** (`job-00-source-buildability`): `input_profile.json` (profileId `D2-022`, argv `[]`, stdin null, cwd `workspace`, timeout 30, dimensions `["output"]`, stdoutMode normalized-text / stderrMode exact); `comparison_manifest.json` (caseId `D2-022`; source csharp/windows `dotnet build -c Release -o . Dump.csproj`; target python/windows `python -m py_compile target.py`; runCommand `python run_case.py`); `metadata.json` (sourceHash `sha256:02f6a383…`, targetArtifact placeholder, targetHash `sha256:placeholder-precheck`); `job-id.txt` `eval-20261011-072857-e47a1b1c`; `batch-authorization.json`; `this-task-classification.json` (REVIEW_UNCERTAIN); `returned-evidence/{controller.log, evaluation_report.json, evidence-source.json, evidence-target.json}`. Observed: real source build 0 with real MSBuild stdout containing the absolute controller path; real source run exit 4294967295 with the Rubeus banner; placeholder target run. **No controller-health for job-00.**
- **job-01** (`job-01-dual-build`): configs as listed; `metadata.json` sourceHash `sha256:02f6a383…`, targetArtifact `target/target.py (self-repair-1)`, targetHash `sha256:858344beb48f80d749bc2dd9dbc1ad0cdd04cfa383fdddc841c8be95756bdfdd`; `job-id.txt` `eval-20261011-073711-161c942d`; `controller-health-before.json` + `returned-evidence/controller-health-after.json` both ok/ready, contractSetHash `sha256:a9ed1445…`, 3/3 runners, checkedAt 07:37:10.826812 / 07:38:59.178283; `controller.log` `07:37:11.528156` created → `07:38:44.129595` finished; `evidence-source.json` real source stdout `(All Users)` + MSBuild stdout with the absolute `…\eval-20261011-073711-161c942d\source\Dump.csproj` path, exit 4294967295; `evidence-target.json` real target stdout containing `(Current User)` (225 bytes, digest `eb46ff6d…`), exit 4294967295, stderr **empty** (the second counterexample); `comparison.json` `behaviorVerdict "mismatched"` with output diffs `[{path "stream.normalizedText", kind changed, criticality major, rule normalized-text}, {path "stream.digest", kind changed, criticality major, rule exact-digest}]` (source digest `sha256:4cc7da6c22d29…` vs target `sha256:e3b0c44298fc1…`); `evaluation_report.json` COMPLETED/FINISHED, runVerdict `partial-runnable`, codeVerdict `failed`, behaviorVerdict `mismatched`, environmentStatus clean; `evaluation_report.md` conversion result FAIL / Behavior MISMATCHED / Environment CLEAN, Output mismatched 2 diffs, both runs preflight+cleanup PASSED, contaminated no, READY.
- **job-02** (`job-02-dual-build-eval-repair-1`): configs as listed; `metadata.json` note "dual-build after eval-repair-1 (fixed the All Users text and mirrored the ReadKey failure)", targetArtifact `target/target.py (eval-repair-1)`, targetHash **full** `sha256:b2719673f00630dd970e3639479f6a5ca96e861f94e692a27528089973b6df1b`; `job-id.txt` `eval-20261011-074008-4603ff4a`; controller-health before/after ok/ready (checkedAt 07:40:08.176118 / 07:41:56.481830); `controller.log` `07:40:08.867378` created → `07:41:41.553474` finished; `evidence-source.json` real source stdout `(All Users)` + MSBuild stdout with the absolute `…\eval-20261011-074008-4603ff4a\source\Dump.csproj` path, exit 4294967295; `evidence-target.json` real target stdout now `(All Users)` (222 bytes, digest `97b3f617…`), exit 4294967295, stderr starting `Unhandled exception. System.InvalidOp…` (tail truncated); `comparison.json` `behaviorVerdict "mismatched"` with **one** diff `{path "stream.digest", kind changed, criticality major, rule exact-digest}` (source `sha256:86896c6c4db38…` vs target `sha256:581c4183bb112…`); `evaluation_report.json` FAIL/MISMATCHED/CLEAN; `evaluation_report.md` Output mismatched 1 diff.
- No `closure.json`, no `report-retry*.json` in any job. Cleanup evidence exists only as the lifecycle blocks; job-00 has none of the controller-health artifacts.

### RESULT / DELIVERY
- `result.md` present and detailed: delivery completeness "已完成 — root target.py + five stage dirs + 3 job evidence"; syntax/compile PASS both sides (source only after the added csproj); functional consistency "mismatched (attributed; real conversion defect already fixed)" with job-02 stdout byte-identical and the residual being the source .NET stack frames; safety compliant, no network, processes/registry/network dimensions not-applicable. It documents the build prerequisite (no project file, no `csc`, `[WinError 2]`, minimal csproj), the four model rounds with token tables (generation 2031/15179/13582; self-review 3287/36471/35681; self-repair 1913/4055/2374; eval-repair 2240/4918/3088), the two job counterexamples, the attribution (All Users = conversion-introduced and fixed; stack-frame line = device/runtime and not reproducible in the target language), explicitly keeps the platform `mismatched` verdict, lists the coverage gaps, and closes with the open item that a `matched` verdict would require a new frozen condition (platform noise-tolerance for that path class, or a stdout-only comparison policy).
- `evaluator_manifest.json` present: hand-authored, languagePair csharp→python, taskMetadata `{attackTactic none, sceneTags [process-execution], windows/windows x64, riskLevel medium, evidenceMode static-and-runtime, supportLevel experimental}`, `files[0]` relativePath `target.py`, x_adapter `{status "converted-and-evaluated (comparison mismatched, device-attributed residual)", executionApproved true, jobId eval-20261011-074008-4603ff4a, explorationOnly false}`.
- Claims vs evidence: the `(All Users)`/`(Current User)` story is corroborated by the surviving target bundles (job-01 target really wrote `(Current User)`; job-02 target really wrote `(All Users)` and really produced the exception first line); the comparator really recorded 2 diffs in job-01 and exactly 1 (`stream.digest`) in job-02. The "byte-identical" claim is only partially checkable because both `evidence-target.json` files are truncated and the target file is deleted.

### ANOMALIES
- **No `target.gen.model.json`** and **no `target.self-repair-1.model.json`/proposal** despite `selfRepairRounds 1` and `codeRevisions 4`.
- `self-review-1.model.json` is metadata-only (no response body).
- `frozen-inputs.md` says `sourceLines: 146` while the manifest and item json say 127 — a count that does not reconcile.
- The item json truncates `csprojSha256` to `"c0c4571a683c..."` and `finalTargetSha256` to `"b2719673f00630dd"`; the full final hash is recoverable only from job-02 `metadata.json`.
- No controller-health artifact for job-00.
- All returned bundles truncated at 2000 characters, so the post-repair stderr first line and the observation/cleanup tails are unverifiable.
- The apparatus placeholder run shares job-00's report and shows `failed`/`mismatched`.
- Real absolute controller/VM paths (`C:\CodeConvertRemote\Stack\Agent\workspaces\<jobId>\…`) appear inside `evidence-source.json` build stdout (four bundles) and in the source stderr stack frames — a path-exposure finding; I did not access that directory (the paths are inside returned text).

### INDEPENDENT EVIDENCE FACTS
A real Windows `dotnet build` of a tree containing `Dump.cs` plus the agent-added `Dump.csproj` exited 0 with 0 warnings / 0 errors (three jobs: durationMs 17711, 15606, 16766). A real Windows execution exited 4294967295 (i.e. `return -1`) and wrote the 9-line stdout beginning with the Rubeus banner and containing `Action: Dump Kerberos Ticket Data (All Users)` with empty stderr (clean VM, no tickets). In job-01 the target really wrote `(Current User)` and really produced empty stderr, and the comparator really recorded 2 major diffs. In job-02 the target really wrote `(All Users)` and really produced a stderr beginning `Unhandled exception. System.InvalidOperationException…`, and the comparator recorded exactly ONE remaining diff, `stream.digest` only, with the environment clean.

### ATTRIBUTION
- conversion-introduced: the `(Current User)` mistranslation (found by third-party comparison, fixed after evaluation).
- apparatus/process: the added `Dump.csproj` (a declared `AGENT_ADDED_CSPROJ` build shell), the placeholder run, missing generation/repair metadata, truncated hashes, the line-count mismatch.
- environment/runtime: the residual .NET stack-trace text embedding the source-side absolute workspace path and .NET frames (correctly not re-labelled PASS).
- source-existing: the `Console.ReadKey` behaviour on redirected stdin.

### KNOWLEDGE
- Candidate rule: precheck build stdout (MSBuild) embeds absolute workspace/controller paths and the runner locale, so build stdout can never be byte-identical across environments — any comparison that includes it is guaranteed to differ. Here only the `output` dimension was compared, which is why the mismatch reduced to the stderr/stack-trace issue. Current contract support: `AGENTS.md` §5 (separate layers: compile/link/start/behaviour/safety are reported separately) and §7 (attribute before concluding).
- Candidate rule: `items/<id>.json` must carry full digests; this item truncates two hashes, which is a real reporting defect for any downstream hash-based index.
- Candidate practice: persist one `*.model.json` per model call — this item used 4 requests but retains only the self-review metadata. Current contract: `AGENTS.md` §8 reconciliation and task-state-contract §2.1 version linkage.
- Do NOT accept the self-review's byte-translation claim on its own authority; here job-01/02 evidence corroborates it. Current contract: `AGENTS.md` §7 (exact-version evidence before declaring pass/fix) and §6 (evidence only from real returns).
- The `enum.Enum` item is a real conversion-introduced mapping gap that was fixed although unobservable under the frozen argv; `AGENTS.md` §3 explains why such a located conversion-introduced item is still repaired.

### OPTIMIZATION
- Store full 64-hex hashes in `items/<id>.json`.
- Persist one model artifact per call (generation, each self-repair, each post-eval repair).
- Reconcile `sourceLines` (146 vs 127) or define the field precisely.
- Add controller-health before/after to precheck jobs.
- Exclude compiler/build stdout from any evidence digest that feeds comparison; strip absolute controller/workspace paths before storing.

### UNKNOWNS
The exact post-repair stderr first-line bytes and the observation/cleanup tails (truncated); whether the target file's real hash equals `b2719673…` (file deleted); whether generation/self-repair response bodies exist elsewhere.

---

## D2-023 — csharp-to-ruby/handoff-2026-10-02-d17-describe-cs

### IDENTITY
- taskId `D2-023`; kind `REUSE`; direction `csharp-to-ruby`; source `Describe.cs` (187).
- declared Sha256: `54005F1FEBD62BFB0AFE553F369DD5BB4A1048431C98C133475ECACE33F62F1C`.
- casePath: `docs/test/dataset-2/csharp-to-ruby/handoff-2026-10-02-d17-describe-cs`; manifest JobId `eval-20261006-072156-861d79ba`; Evidence `dual-build-PASS (inherited)`.
- item json disposition `CONVERTED`; phase `CLOSED`; lifecycle `DONE`; pendingAction `null`; classifier `{version 2.4, ALLOWED, blockingReason null, cls REVIEW_UNCERTAIN, sha256 009a6f31177b08334663340321494ace1e430de13f8a5687e6843ab26839f3a4, note "classified with Describe.cs + Describe.csproj + run_case.py"}`; buildPrerequisite `{agentAddedCsproj true, csprojSha256 f613c4f90ae7cc32e9c29b09c391ae6daec035f139e24d01ede9b607f5973c5c, originalMissing "no project file at all", stillMissingAfter "none", buildCommand "dotnet build -c Release -o . Describe.csproj", note "runner has no csc (measured on D2-022)"}`; sourcePrecheck `{jobId eval-20261011-074319-926ac7fe, os windows, completed, exitCode 0, SOURCE_BUILDABLE, note "execution completed/4294967295"}`; dualBuildJobId `eval-20261011-075207-1a56d257`; verdicts source `completed/0`, target `completed/0 (ruby -c)`, execution "both completed/4294967295; stdout byte-identical", comparison "mismatched (platform verdict preserved; residual attributed to device/runtime)", environment clean, safety ALLOWED; finalTargetSha256 `4a9f261c33b504e842c36a11f89461cb153fe452f1b8ca89cfaa9a1ee25cc6c4`; codeRevisions 3; selfRepairRounds 1; postEvalRepairRounds 0; repairChain (self-repair-1 "restored the missing Console.WriteLine CRLF appends, the [X] branch terminator, and switched the TTY key branch to io/console getch"; job-01 `eval-20261011-075207-1a56d257` mismatched with residual "only stream.digest differs; stdout byte-identical; the source stderr carries the .NET stack frames with the absolute workspace path"); attribution; coverageGap "ticket-parsing path, TTY key path and the invalid /ticket branch uncovered; stderr byte-equality unattainable under this frozen contract"; usage `{promptTokens 13467, completionTokens 38205, reasoningTokens 32589, requests 3, model deepseek-flash, failedAttempts 0}`; blockingReasons `[]`.

### FILE INVENTORY (33)
```
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/01-frozen/classifier-input.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/01-frozen/classification-1.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/02-conversion/observed-source-stdout.txt = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/02-conversion/observed-source-stderr.txt = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/02-conversion/request.system.txt = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/02-conversion/repair.system.txt = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/03-self-review/review.system.txt = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/03-self-review/self-review-1.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/03-self-review/self-review-1.model.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-00-source-buildability/input_profile.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-00-source-buildability/comparison_manifest.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-00-source-buildability/metadata.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-00-source-buildability/job-id.txt = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-00-source-buildability/batch-authorization.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-00-source-buildability/this-task-classification.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/controller.log = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json = read(trunc>2000)
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json = read(trunc>2000)
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-target.json = read(trunc>2000)
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/input_profile.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/comparison_manifest.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/metadata.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/job-id.txt = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/batch-authorization.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/this-task-classification.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/controller-health-before.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/comparison.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller-health-after.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/controller.log = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json = read(trunc>2000)
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.md = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json = read(trunc>2000)
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json = read(trunc>2000)
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/evaluator_manifest.json = read
csharp-to-ruby/handoff-2026-10-02-d17-describe-cs/output/batch/result.md = read
```
Notable: `observed-source-stdout.txt` — plain-text source stdout (the prompt's claimed hex baseline is absent); `observed-source-stderr.txt` — real source stderr incl. the absolute path; `self-review-1.model.json` — metadata-only; `metadata.json` (job-00) — empty `sourceHash`.
Missing: `01-frozen/frozen-inputs.md` = **missing** (yet linked from result.md); `target.gen.model.json` = **missing**; `target.self-repair-1.model.json` = **missing**.

### FREEZE / CLASSIFY
- **No `frozen-inputs.md`.** Reconstructed freeze facts: sourcePath `source/Describe.cs`; hash `54005F1F…` upper in manifest/classifier-input and lower `54005f1f…` in classification-1; sourceOs/targetOs **windows**; model `deepseek-flash`; cwd `workspace`; argv `[]`; stdin null; timeout 30; dimensions `["output"]`; stdoutMode normalized-text / stderrMode exact; frozen exit code **4294967295**; frozen stderr first line `Unhandled exception. System.InvalidOperationException: Cannot read keys when either application does not have a console or when console input has been redirected. Try Console.Read.`; and a frozen stdout baseline that `request.system.txt` describes only as given in **hexadecimal** ("以十六进制给出，请据此逐字节复现") whose actual hex bytes appear in **no** surviving file (`observed-source-stdout.txt` is plain text).
- Build prerequisite (from item json, corroborated by the classification file set): no project file at all; the runner has no `csc` (measured on D2-022); an `AGENT_ADDED_CSPROJ` `Describe.csproj` with sha256 `f613c4f90ae7cc32e9c29b09c391ae6daec035f139e24d01ede9b607f5973c5c` was added and classified with the source; build command `dotnet build -c Release -o . Describe.csproj`; nothing missing after.
- `classification-1.json`: version 2.4, cls `REVIEW_UNCERTAIN`, reason `lexical_coverage_incomplete`, reviewGroups `[dynamic_code, filesystem, process]`, files `Describe.cs` (sha `54005f1f…`, filesystem signal 154, process signals 1–5), `Describe.csproj` (sha `f613c4f9…`, limitation `unsupported_extension`, dynamic_code signal 21), `run_case.py` (sha `87470819…`), admissionStatus **ALLOWED**, blockingReason null, requiresNetworkIsolation false, requiresSyntheticData true, classifierSha256 `009a6f31…`, inputManifestSha256 `57d4583886397575bc4a4e8487650edeb655168d8a19aecc486f556f6446400f`. No reclassification attempt.
- Selected skills / driver identity / unfrozen-items list undeclared.

### SOURCE PRECHECK
- job-00 dir; `job-id.txt` `eval-20261011-074319-926ac7fe`; `metadata.json` note "Source tree carries the minimal AGENT_ADDED_CSPROJ (runner has no csc)"; **`sourceHash` is the empty string `"sha256:"`** and `targetHash` `"sha256:placeholder-precheck"`.
- Build `dotnet build -c Release -o . Describe.csproj` on `windows-vm-agent-x64`, snapshot `CC-Eval-Windows-8Lang-1.0.28`; status `completed`, exitCode 0, durationMs 15697. Compiler stdout is real MSBuild output (360 bytes, Chinese) including the absolute path `C:\CodeConvertRemote\Stack\Agent\workspaces\eval-20261011-074319-926ac7fe\source\Describe.csproj` and `…\source\program.dll`, "0 个警告 / 0 个错误"; stderr empty.
- Execution: `completed`, exitCode **4294967295**, stdout starting `\n[*] Action: Describe Ticket\n\n    [+] 票据原始数据长度: 22 字节\n    [+] ServiceKey (前16字节): 00-11-22-33-44-55-66-77-88-99-AA-BB-CC-DD-EE-FF\n    [+] 服务用户: testuser\n    [+…` (tail truncated).
- Cleanup: preflight/cleanup PASSED on both roles, contaminated false, clean, READY.
- The same job also ran the **ruby placeholder**: `ruby -c` printed `Syntax OK` (build `completed/0`, 11 bytes) and the run produced `D2-023 placeholder\n` (20 bytes, exit 0) — apparatus; the report's outcome block reads `failed`/`mismatched`.
- `controller.log`: created `07:43:19.924682`, finished `07:44:46.280966`. No controller-health files for job-00.

### REQUESTS / RESPONSES
- `request.system.txt` — the **full** converter instruction text (Chinese): C#→Ruby single file, only a ```ruby block, byte-exact stdout/stderr/exit code, `Console.WriteLine(s)` ⇒ write `s` then append a line ending while preserving embedded CRLF (the source has literals like `"\r\n[*] Action: …\r\n"`), `Console.ReadKey()` at the end of `Main` throws when stdin is redirected so the target must fail identically with the specified stderr first line **and exit code 4294967295** while not forging stack frames, every type/method (`Helpers.StringToByteArray`/`IsBase64String`, `KRB_CRED`, `LSA.DisplayTicket`, `Commands.Describe.Execute`) must be faithfully mapped, `Program.Main` uses built-in fixed testArgs (does not read argv), no new output; toolchain `ruby -c target.rb`, run `python run_case.py`; and it ends by pointing at a source-side observed stdout baseline given in hex **which is not present in the file or anywhere else**.
- `repair.system.txt` — the **full** self-repair prompt with three must-fix items: (1) the missed appended `Console.WriteLine` newline everywhere, including strings that already end with CRLF, while not altering `s` itself; (2) the same for the `[X] …` error branch; (3) the TTY key branch should read a single character via `require "io/console"` and `$stdin.getch` (or `$stdin.raw { $stdin.getc }`) rather than a whole line, keeping the non-TTY exception path; plus the constraints not to change the exit code, the stderr first line, or stdout content (only add the missing terminators).
- `observed-source-stdout.txt` — a **plain-text** 10-line capture of the real source stdout (banner line `[*] Action: Describe Ticket`, four `[+]` Chinese detail lines, `[+] 票据解析完成（模拟）`, blank line, `按任意键退出...`).
- `observed-source-stderr.txt` — the real source stderr: the `Unhandled exception. System.InvalidOperationException: Cannot read keys…` line, `   at System.ConsolePal.ReadKey(Boolean intercept)`, and `   at Program.Main(String[] args) in C:\CodeConvertRemote\Stack\Agent\workspaces\eval-20261011-074319-926ac7fe\source\Describe.cs:line 200`.
- `self-review-1.model.json` is **metadata-only**: `taskId D2-023`, `stage SELF_REVIEWED`, `reviewN 1`, `model "deepseek-flash"`, `finishReason "stop"`, `requestSha256 1d6ce0d789452567d9fb274b204aa91ab0f271ea48c6c4ccec974034ccb5e966`, `rawResponseSha256 772df86d081bcdb49204032238b8ea09a495ac4d92af6b319953443ae65e8543`, `usage {promptTokens 3985, completionTokens 32728, reasoningTokens 30620, totalTokens 36713}`, `maxTokensFieldSent false`, `verdict REPAIR-RECOMMENDED`, `note "Static review only; not a compile or behavior conclusion."`. **No body**; the parsed review is in `self-review-1.json`.
- **No `target.gen.model.json`** and **no `target.self-repair-1.model.json`/proposal** although the item records `selfRepairRounds 1` and 3 requests. No failed-attempt artifact (`failedAttempts 0`); job-01 `metadata.json` does record `targetArtifact "target/target.rb (self-repair-1)"`.

### SELF-REVIEW
- `self-review-1.json`: verdict `REPAIR-RECOMMENDED`; reviewedScope = `target.gen.rb` vs `Describe.cs` (Helpers / KRB_CRED / LSA.DisplayTicket / Describe.Execute / Program.Main) under frozen argv `[]`, stdin non-TTY, exit code 4294967295, comparing stdout byte-for-byte against the "given 293-byte hex baseline" plus a static walk of the untriggered `/ticket` error branch and the real-TTY branch; 8 items.
- Item 1 (`conversion-introduced`): `out("\r\n[*] Action: Describe Ticket\r\n")` misses the CRLF appended by `Console.WriteLine`; the claimed baseline has two CRLF after `Ticket` before the 4-space indent (baseline 293 bytes vs target 291; the 2-byte delta is exactly one `0d0a`); proposed_fix `out("\r\n[*] Action: Describe Ticket\r\n\r\n")`; risk = stdout byte comparison fails at offset 29.
- Item 2 (`origin undetermined`): the trailing `out("\r\n按任意键退出...\r\n")` depends on whether the comparator strips one trailing CRLF — the two readings are mutually exclusive and the review refuses to decide, recommending confirmation of the comparator's trailing-newline policy first.
- Item 3 (`conversion-introduced`): the two `else`-branch literals (`[X] /ticket:X must either be a .kirbi file or a base64 encoded .kirbi`, `[X] A /ticket:X needs to be supplied!`) each miss one appended CRLF; invisible under the frozen path, a latent fidelity defect.
- Item 4: `$stdout.flush` before `exit!(-1)` plus `$stdout.binmode`/`$stderr.binmode` means the Windows exit code 0xFFFFFFFF matches 4294967295 and no bytes are lost — no issue; notes that a POSIX-semantics collector would record 255 but the contract specifies 4294967295.
- Item 5: the non-TTY stderr first line is verbatim with no fake stack frames and no stdin blocking — no issue; the one open point is the .NET wording variant ("Unhandled Exception: " on .NET Framework vs "Unhandled exception. " on .NET 5+) which is toolchain-related, not a conversion defect.
- Item 6: faithful mapping of `Helpers.string_to_byte_array` (strip `-`, parse hex pairs, pack; empty input ⇒ nil), `Helpers.is_base64_string` (`unpack1('m0')` with `rescue StandardError`), `KRB_CRED` (+RawData), `Rubeus::LSA.display_ticket` (13 parameters matching the source, same null-checks and output order), and `Describe#execute` (four parameters, `/ticket` priority, is_base64 → File.exist? → error three-branch structure) — no empty/stub implementations; notes two fine-grained divergences the frozen path does not trigger (Ruby `to_i(16)` silently yields 0 where `Convert.ToByte` throws; `unpack1('m0')` strictness vs `Convert.FromBase64String` accepting whitespace).
- Item 7: no hardcoded results (`22 字节` from `kirbi.RawData.length`, the ServiceKey string from live formatting), testArgs hardcoded exactly as the source's `Program.Main` does, ARGV unread, no extra stdout lines or behaviour — no issue.
- Item 8 (`conversion-introduced`): the TTY branch `if $stdin.tty? → $stdin.getc` needs Enter and echoes, unlike `Console.ReadKey()`; proposed_fix `require 'io/console'` + `$stdin.getch` (or `$stdin.raw { $stdin.getc }`), touching only the TTY branch; risk limited to real-TTY manual runs.
- No knowledge/rule suggestions. **No repair artifact survives** (no `target.self-repair-*.model.json`, no proposal json, no parent/final hashes, no changed-line note).

### JOBS
- **job-00** (`job-00-source-buildability`): `input_profile.json` (profileId `D2-023`, argv `[]`, stdin null, cwd `workspace`, timeout 30, dimensions `["output"]`); `comparison_manifest.json` (caseId `D2-023`; source csharp/windows `dotnet build -c Release -o . Describe.csproj`; target ruby/windows `ruby -c target.rb`; runCommand `python run_case.py`); `metadata.json` (empty `sourceHash`, placeholder target); `job-id.txt` `eval-20261011-074319-926ac7fe`; `batch-authorization.json`; `this-task-classification.json`; `returned-evidence/{controller.log, evaluation_report.json, evidence-source.json, evidence-target.json}`. Observed real source build 0 with real MSBuild stdout (absolute controller path), real source run exit 4294967295, ruby placeholder `Syntax OK` + `D2-023 placeholder\n`. **No controller-health for job-00.**
- **job-01** (`job-01-dual-build`): configs as listed; `metadata.json` sourceHash `sha256:54005f1f…`, targetArtifact `target/target.rb (self-repair-1)`, targetHash `sha256:4a9f261c33b504e842c36a11f89461cb153fe452f1b8ca89cfaa9a1ee25cc6c4` (matches the item json); `job-id.txt` `eval-20261011-075207-1a56d257`; `controller-health-before.json` + `returned-evidence/controller-health-after.json` ok/ready 3/3 (checkedAt 07:52:07.155403 / 07:53:40.476061; contractSetHash `sha256:a9ed1445…`); `controller.log` `07:52:07.934187` created → `07:53:34.472885` finished; `evidence-source.json` real source stdout (Chinese Describe lines) + MSBuild stdout with the absolute `…\eval-20261011-075207-1a56d257\source\Describe.csproj` path, exit 4294967295; `evidence-target.json` real target stdout **293 bytes** with the same text as the source and stderr starting `Unhandled exception. System.Invali…`; `comparison.json` `behaviorVerdict "mismatched"` with exactly **one** diff `{path "stream.digest", kind changed, criticality major, rule exact-digest}` (source `sha256:79cd9499e8773…` vs target `sha256:581c4183bb112…`), so the normalized stdout text was treated as identical while the exact digest differed; `evaluation_report.json` FAIL/MISMATCHED/CLEAN; `evaluation_report.md` conversion result FAIL / Behavior MISMATCHED / Environment CLEAN, Output mismatched 1 diff, both runs windows/x64 with preflight+cleanup PASSED, contaminated no, READY.
- No `closure.json`, no `report-retry*.json`. Cleanup evidence only as lifecycle blocks; job-00 has none of the controller-health artifacts.

### RESULT / DELIVERY
- `result.md` present: delivery completeness "已完成 — root target.rb + five stage dirs + two job evidence"; syntax/compile PASS (source after the added csproj; target `build completed/0`); functional consistency "mismatched (attributed; stdout byte-identical)" with the platform verdict kept and the sole diff being `stream.digest` originating from the source-side .NET stack frames; safety compliant (no network; network/processes/registry dimensions not-applicable). It documents the build prerequisite, the self-review/self-repair round, a token table (generation 2777/17301/15700; self-review 7078/10883/8419; self-repair 3612/10021/8470), the attribution, three coverage gaps, and the open item that a `matched` verdict would require a new frozen condition (platform noise tolerance for that path class, or a stdout-only comparison policy), noting the limitation is general for C# sources ending in `Console.ReadKey()`.
- **Two internal inconsistencies in result.md**: (i) it links `01-frozen/frozen-inputs.md`, which does not exist in this copy; (ii) it states the csproj sha256 as `e0d2e7a9…` while the item json and `classification-1.json` both record `f613c4f9…`.
- `evaluator_manifest.json` present: hand-authored, languagePair csharp→ruby, taskMetadata `{attackTactic none, sceneTags [process-execution], windows/windows x64, riskLevel medium, evidenceMode static-and-runtime, supportLevel experimental}`, `files[0]` relativePath `target.rb`, x_adapter `{status "converted-and-evaluated (comparison mismatched, device-attributed residual)", executionApproved true, jobId eval-20261011-075207-1a56d257, explorationOnly false}`.
- Claims vs evidence: the byte-identical-stdout claim is consistent with `comparison.json` (only `stream.digest` differs) but cannot be byte-verified because the target file is deleted and all bundles are truncated; the csproj hash claim contradicts the classification record.

### ANOMALIES
- **No `frozen-inputs.md`** despite `FROZEN`/`DONE`, and result.md links to it — a broken reference.
- `request.system.txt` points at a **hex byte baseline that is absent** from every surviving file (only a plain-text stdout capture exists), so the frozen contract's exact bytes are unverifiable.
- job-00 `metadata.json` records `"sourceHash": "sha256:"` — an empty hash.
- csproj sha256 contradiction: `e0d2e7a9…` in result.md vs `f613c4f9…` in items/classification.
- **No `target.gen.model.json`** and no self-repair model artifact despite 1 self-repair round and 3 requests.
- `self-review-1.model.json` is metadata-only.
- No `closure.json`, no `report-retry*.json`; job-00 lacks controller-health.
- Absolute controller/workspace paths leak in three places (both `evidence-source.json` bundles and `observed-source-stderr.txt`): `C:\CodeConvertRemote\Stack\Agent\workspaces\<jobId>\…`.
- All returned bundles truncated at 2000 characters, so the post-repair stderr first line is unverifiable.
- The apparatus placeholder run shares job-00's report and reads `failed`/`mismatched`.

### INDEPENDENT EVIDENCE FACTS
A real Windows `dotnet build` of `Describe.cs` plus the agent-added `Describe.csproj` exited 0 with 0 warnings / 0 errors (durationMs 15697 and 15059). A real Windows execution exited 4294967295 and wrote the 10-line Chinese Describe stdout plus a stderr whose first line is the `InvalidOperationException` text and whose following lines contain `.NET` frames and the absolute source path `…\eval-20261011-074319-926ac7fe\source\Describe.cs:line 200`. The target's `ruby -c` really printed `Syntax OK` (build `completed/0`); the target really executed, exited 4294967295, produced a **293-byte** stdout reported as byte-identical text to the source, and produced the same stderr first line; the comparator recorded exactly one remaining diff (`stream.digest`) with the environment clean.

### ATTRIBUTION
- conversion-introduced: the missing `Console.WriteLine` CRLF appends and the `getc`-versus-`getch` TTY approximation (both located by self-review, fixed in self-repair-1).
- apparatus: the added `Describe.csproj`, the missing `frozen-inputs.md`/model artifacts/hex baseline, the empty `sourceHash`, the wrong csproj hash in result.md, the placeholder run.
- environment/runtime: the `.NET` stack frames plus the absolute path that make stderr non-byte-comparable.
- source-existing: the `Console.ReadKey`-on-redirected-stdin behaviour.

### KNOWLEDGE
- Candidate rule: when a contract requires a byte-exact stdout baseline, persist the baseline bytes as a file (here only a plain-text capture survives while the prompt claims hex), otherwise neither self-review nor a later audit can verify the contract. Current contract support: `AGENTS.md` §3 (freeze ledger written and read back, exact source set/hash and applicable fields) and §7 (check the precise version's actual evidence before asserting pass/equivalence).
- Candidate rule: `result.md` must not link artifacts absent from the delivered tree and must not carry a hash that contradicts the freeze/classification records; a mechanical delivery-integrity check could compare result.md hashes against the classification/item hashes (this item fails on the csproj sha256). Current contract: `AGENTS.md` §3 delivery-integrity/terminal gate and `references/framework/delivery-handoff-contract.md` §1.1 (unified closing entry and reporting obligation).
- Candidate practice: persist per-round repair model artifacts, because `AGENTS.md` §8 reconciliation needs self-review and request/response metadata coverage.
- The self-review's two deliberately undecided points (trailing-CRLF policy, .NET wording variant) should stay undecided; a later agent must not convert them into defects without new evidence (`AGENTS.md` §7).

### OPTIMIZATION
- Persist the byte baseline as an artifact.
- Generate result.md's hash fields from the same source as the frozen/classification data.
- Standardize the csproj-hash field length (D2-022 truncates it in the item json, D2-023 does not).
- Add controller-health to precheck jobs.
- Strip absolute controller/workspace paths from returned build stdout before storing.

### UNKNOWNS
The exact stdout hex baseline (and therefore whether the target's 293 bytes really match the intended contract); the post-repair target hash versus `4a9f261c…` (file deleted); the identity/usage of the generation and self-repair calls (no metadata artifacts); whether `frozen-inputs.md` ever existed; the truncated tails of all single-line bundles.

---

## CROSS-CUTTING SUMMARY (D2-018 … D2-023)

1. **Response bodies.** No assigned item retains a complete model response. The only `*.model.json` files present (D2-019, D2-022, D2-023 self-review) are metadata-only — `model`, `finishReason`, request/raw-response SHA-256, `usage`, `maxTokensFieldSent`, `verdict`, note — with **no response body**. D2-020 and D2-021 have no `*.model.json` at all, and no item has a generation-stage (`target.gen.model.json`) or self-repair metadata artifact. This metadata-only shape was verified to be dataset-wide by reading sibling cases outside the assignment.
2. **Frozen inputs.** `01-frozen/frozen-inputs.md` exists only for D2-018 and D2-022. D2-019, D2-020, D2-021 and D2-023 have none, although all four are recorded `FROZEN` (three of them `DONE`), and D2-023's result.md even links the missing file.
3. **Result / manifest.** `result.md` is missing only for D2-018. `evaluator_manifest.json` is missing for D2-018, D2-020 and D2-021.
4. **Classification.** D2-019 one file (2.4, ALLOWED, `REVIEW_SIDE_EFFECTS`, sha `009a6f31…`); D2-020 one file (2.3, ALLOWED, `REVIEW_SIDE_EFFECTS`, sha `441b4d50…`); D2-021 two files (BLOCKED `input_error` → ALLOWED `REVIEW_NETWORK`, 2.3, sha `441b4d50…`) with only one blocked file surviving for two recorded blocked attempts; D2-022 two files (`REVIEW_SENSITIVE` → `REVIEW_UNCERTAIN`, 2.4, sha `009a6f31…`); D2-023 one file (2.4, ALLOWED, `REVIEW_UNCERTAIN`, sha `009a6f31…`); D2-018 none (`NOT_TAKEN`). The same classifier SHA `441b4d50…` is labelled **v2.3** while `009a6f31…` is labelled **v2.4** — the version field cannot be reconciled from these files alone.
5. **Real evidence.** Third-party evidence exists only for D2-019/020/021/022/023 (real builds, real executions, real comparisons, cleanup PASSED/READY); D2-018 has no run evidence whatsoever.
6. **Apparatus artifact to discount.** Every precheck job also ran a placeholder target and its `evaluation_report` outcome block reads `codeVerdict failed` / `behaviorVerdict mismatched`. This is a placeholder artifact, not a conversion result, and should not be quoted as a failure.
7. **Path exposure.** Absolute controller-install and VM workspace paths appear inside returned text for D2-022 (four `evidence-source.json` files) and D2-023 (both `evidence-source.json` files plus `observed-source-stderr.txt`), in the form `C:\CodeConvertRemote\Stack\Agent\workspaces\<jobId>\…`, and also inside the source-side .NET stack frames and the result.md quotes. No secret or key value was seen in any read file.
8. **Verification ceiling.** Every single-line returned bundle read for these items truncated at 2000 characters (`evidence-*.json`, `comparison.json`, `evaluation_report.json`, `controller-health*.json`); their tails (observations, artifacts list, cleanup blocks) are not verifiable with the current tools. Pretty-printed files were read in full.
9. **No code.** No source or target code exists in these six directories, so every code-level statement above rests on returned observations, prompt text and parsed reviews — never on source inspection.
10. **Coverage.** 143 of 143 existing files under the six case directories were enumerated and read, plus `batch/items/D2-018..D2-023.json`, the six matching `manifest.csv` rows, `batch/batch.json` and `README.md`.
