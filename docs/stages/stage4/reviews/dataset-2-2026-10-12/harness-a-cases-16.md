# Harness A — read-only static review, items D2-060 … D2-065

Reviewer: delegated read-only static reviewer. Method: native `read` / `glob` / `grep` only. No script, classifier, conversion, build or submission was run. `D:\CodeConvertRemote\Stack` not accessed; no `.env`/secret read; no source reconstruction.

Root examined: `docs/dataset-2/dataset-2-copy/`. Item records: `batch/items/<id>.json`. Manifest rows: `manifest.csv` lines 60–65.

**Inventory status vocabulary** (extension declared): `read` = read in full; `read(截断>2000)` = single-line file, tool truncated at 2000 chars, no byte-offset read available; `empty` = 0 lines; `present(unread)` = file exists per glob, not opened in this pass (context budget); `dir-empty` = directory exists (read → "not a regular file") and glob finds 0 files at any depth.

**Cross-item path convention note.** `manifest.csv` col-8 datasetPath (`dataset/go-to-ruby/...`) and `batch/items/*.json` `casePath` (`docs/test/dataset-2/...`) both differ from the actual copy root `docs/dataset-2/dataset-2-copy/`. All five processed cases are also **output-only in this copy**: `glob **/source/*` → 0 files and `glob **/target/*` → 0 files for every case, so the `source/` + `target/` trees that `result.md` calls "齐备" are not present here (unverifiable in this copy).

---

## D2-060

### 1. Identity
- taskId `D2-060`; kind `REUSE`; direction `go-to-python`; source `manifest_zip_collect.go`; manifest col-9 declared Sha256 `F978842FC7ED6E7C031BF225C6468D6FA35E069F8781BADA833867A1E3A408B6` (= item `sourceSha256` lowercased, consistent).
- casePath (item json) `docs/test/dataset-2/go-to-python/handoff-2026-10-02-d28-manifest-zip-collect-go`; dir reviewed `go-to-python/handoff-2026-10-02-d28-manifest-zip-collect-go`.
- item json: disposition `CONVERTED`, phase `CLOSED`, lifecycle `DONE`, pendingAction `null`, blockingReasons `[]`.
- targetSha256 `899a08e8…91d8a5`; classifier v2.4 `ALLOWED` / `blockingReason null` / cls `REVIEW_SIDE_EFFECTS` / sha `009a6f31…f3a4`.
- usage: 2 requests, prompt 3397, completion 9517, reasoning 8126, total 12914, model `deepseek-flash`, failedAttempts 0.

### 2. File inventory (33 files, case root `…-manifest-zip-collect-go/output/batch/`)
```
01-frozen/classifier-input.json=read
01-frozen/classification-1.json=read
02-conversion/observed-source-stderr.txt=empty
02-conversion/observed-source-stdout.txt=present(unread)
02-conversion/target.gen.model.json=read
02-conversion/request.system.txt=read
03-self-review/self-review-1.model.json=read
03-self-review/review.system.txt=present(unread)
03-self-review/self-review-1.json=read
04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json=present(unread)
04-evaluation/job-00-source-buildability/returned-evidence/evaluation_report.json=present(unread)
04-evaluation/job-00-source-buildability/{batch-authorization,job-id.txt,input_profile,metadata,controller-health-before,runners-before,comparison_manifest,this-task-classification}.json/.txt=present(unread)
04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json=read(截断>2000)
04-evaluation/job-01-dual-build/returned-evidence/comparison.json=read
04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json=read(截断>2000)
04-evaluation/job-01-dual-build/returned-evidence/evaluation_report.json=present(unread)
04-evaluation/job-01-dual-build/{batch-authorization,this-task-classification,comparison_manifest,input_profile,metadata,controller-health-before,runners-before}.json=present(unread)
04-evaluation/job-01-dual-build/job-id.txt=read
evaluator_manifest.json=read
result.md=read
```
No `01-frozen/frozen-inputs.md` (absent — see anomalies). No `source/`, `target/`.

### 3. Findings
- **Freeze/classify.** `classifier-input.json` is a 1-task batch (`taskId D2-060`, `sourcePath source/manifest_zip_collect.go`, uppercase hash matching the manifest verbatim). `classification-1.json`: cls `REVIEW_SIDE_EFFECTS`, reason `local_effects_require_review`, files `manifest_zip_collect.go` (fs signals only, `network_mode none-detected`) + `run_case.py` (fs+process), `inputErrors []`, `admissionStatus ALLOWED`, `blockingReason null`, `executionApproved true`, limitations `lexical_heuristics_not_dataflow` / `target_driver_dependencies_not_assessed` / `isolation_and_authorization_not_assessed`. **`frozen-inputs.md` is not present** — the freeze-writeback artifact that AGENTS.md §3 requires before classification cannot be verified in this copy.
- **Source precheck (job-00).** `eval-20261011-104148-384ef54e`, os linux, build `go build -o program manifest_zip_collect.go`, status `completed`/exit 0, execution `completed/0`, observed stdout non-empty ("artifact: …/advanced-bundle.zip" + zip entries + manifest). Diagnostic: none. Cleanup: no dedicated cleanup/reclaim artifact in the job dir ⇒ **UNVERIFIED**.
- **Requests/responses.** `request.system.txt` is a real 13-line Go→Python system prompt (declares Python 3.12 single file, byte-identical stdout/stderr, no stubbing, `python -m py_compile`). `target.gen.model.json` is a **real body**: role assistant, fenced `python` content (real `hashlib`/`json`/`os`/`zipfile` implementation, `ZIP_DEFLATED`, `metas.sort`, `json.dumps(indent=2)`), plus `reasoning_content` (truncated at 2000). `self-review-1.model.json` is a **metadata-only** record: taskId, stage `SELF_REVIEWED`, reviewN 1, model `deepseek-flash`, `finishReason stop`, usage (1761/7610/6659/9371), `maxTokensFieldSent false`, verdict `NO-REPAIR-IDENTIFIED`, "Static review only" — no review body (the body is the separate `self-review-1.json`). Failed attempts: 0.
- **Self-review.** `self-review-1.json` verdict `NO-REPAIR-IDENTIFIED`, 6 items, all `origin: undetermined`, `proposed_fix null`, risk 无. Scope: dir/file creation, SHA-256, ZIP entries, manifest.json serialization, sort, byte length, stdout/exit. No repairs; `codeRevisions 0` / `selfRepairRounds 0` consistent with `events.jsonl` 596–602.
- **Job-01 (dual build).** `eval-20261011-104405-14cb0e8e` (`job-id.txt` matches). Independent evidence: `evidence-source.json` `runRole source`, build `completed/0` dur 6375 ms, execution `completed/0` dur 65 ms, artifactLanguage `go`; `evidence-target.json` `runRole target`, build `completed/0` dur 467 ms, execution `completed/0` dur 246 ms, artifactLanguage `python`; both `snapshot CC-Eval-Linux-8Lang-1.0.28`, `selectedRunner linux-vm-agent-x64`, `inputProfileHash sha256:ad58455a…`. `comparison.json`: `behaviorVerdict matched`, output dimension `matched`, `diffs []`, all other dimensions `not-applicable`; comparator preset `noise-tolerant-v1` with tokens `temporary-paths`,`timestamps`,`ephemeral-ports`. Side effects: none observed beyond design. Cleanup: no cleanup artifact ⇒ UNVERIFIED.
- **result.md / evaluator_manifest.json.** Both present. `evaluator_manifest.json` (schemaVersion 1, hand-authored by the temporary controller adapter) declares go→python, sceneTags `[file-io]`, sourceOs/targetOs linux x64, `evidenceMode static-and-runtime`, `isolationLaunchArgs` includes `networkBoundary=isolated VM; no egress`, `oracleFreezability FREEZABLE`, jobId `eval-20261011-104405-14cb0e8e`. Its `targetDir`/`plannedResultPath` are absolute Windows paths on a **different host** (`C:\Users\Administrator.DESKTOP-LRHSLVD\Desktop\code-convert-skill\…`) — provenance, not this workspace.
- **Anomalies.** (a) `01-frozen/frozen-inputs.md` absent. (b) `source/`+`target/` trees absent in this copy, so `evaluator_manifest.json` `hasTranslatedCode true` and `result.md` "源/目标/驱动/清单齐备" are unverifiable here; the `targetDir` paths point to another host. (c) `result.md` §关键点 says fixture contents `alpha/gamma/delta` 6 bytes and `beta` 5 bytes — consistent with `evidence-source.json` manifest entries (`size 6`, `size 5`) read independently.
- **Independent evidence facts.** Source and target stdout digests are **byte-identical** in both bundles (item json digest `sha256:5b99a4e1…069b3`); the driver echoes the zip's `manifest.json` plus the 4 fixtures, i.e. the comparison face is broader than the program's single `artifact:` line. This is a genuine two-sided observation, not a §10.6 degenerate case.
- **Attribution.** Behavior match attributable to the conversion; no environment or device difference recorded. Design exclusion: ZIP binary bytes (entry mtime/compression) deliberately outside the oracle — a declared scope limit, not a defect.
- **Knowledge candidates + current-contract coverage.** (1) *Weak-oracle strengthening*: program prints one line, driver reads back artifact bytes so the comparison covers real metadata. Not covered by `batch/operational-discipline.md` §10.6 (line 107, only forbids degenerate two-side-empty `matched`); candidate new rule. (2) *Declared out-of-oracle surfaces* (zip bytes) vs `§10.4` (line 97, oracle needs independent external basis) — covered in spirit; no explicit "declare excluded surfaces" rule. (3) Freeze-writeback gate: `references/framework/task-state-contract.md` §2.2 (cited per AGENTS.md §3; not independently read this pass).
- **Optimization.** `result.md` could record the cleanup/reclaim evidence pointer and the `source/`/`target/` tree hashes per side, so the "齐备" claim is checkable without the other host.
- **Unknowns.** Whether `frozen-inputs.md` ever existed (absent here); cleanup outcome for both jobs; content of the 13 unread JSON artifacts; the source/target trees and their hashes.

---

## D2-061

### 1. Identity
- taskId `D2-061`; kind `REUSE`; direction `go-to-ruby`; source `inbox_batch_validate.go`; manifest declared Sha256 `9EB5E73874131073A050C5C7F941161AC192D9BC8791F96435089C29841D45DF` (= item `sourceSha256`, consistent).
- casePath `docs/test/dataset-2/go-to-ruby/handoff-2026-10-02-d29-inbox-batch-validate-go`; dir `go-to-ruby/handoff-2026-10-02-d29-inbox-batch-validate-go`.
- disposition `CONVERTED`, phase `CLOSED`, lifecycle `DONE`, pendingAction `null`, blockingReasons `[]`. targetSha256 `90d204a6…40606b`.
- classifier v2.4 `ALLOWED`, cls `REVIEW_SIDE_EFFECTS`, sha `009a6f31…f3a4`.
- usage: 2 requests, prompt 2990, completion 31650, reasoning 30399, total 34640, `deepseek-flash`, failedAttempts 0.

### 2. File inventory (36 files, case root `…-inbox-batch-validate-go/output/batch/`)
```
01-frozen/classifier-input.json=present(unread)
01-frozen/classification-1.json=present(unread)
02-conversion/observed-source-stdout.txt=present(unread)
02-conversion/observed-source-stderr.txt=empty
02-conversion/target.gen.model.json=read (lines 1-4; real body + reasoning)
02-conversion/request.system.txt=present(unread)
03-self-review/self-review-1.model.json=present(unread)
03-self-review/review.system.txt=present(unread)
03-self-review/self-review-1.json=read
04-evaluation/job-00-source-buildability/returned-evidence/{evaluation_report,evidence-source}.json=present(unread)
04-evaluation/job-00-source-buildability/{batch-authorization,job-id.txt,input_profile,metadata,controller-health-before,runners-before,this-task-classification,comparison_manifest}.json/.txt=present(unread)
04-evaluation/job-01-dual-build/returned-evidence/{evidence-source,evidence-target,comparison,controller-health-after,evaluation_report}.json=present(unread); returned-evidence/comparison.json=read; returned-evidence/controller.log=present(unread)
04-evaluation/job-01-dual-build/{batch-authorization,this-task-classification,comparison_manifest,input_profile,metadata,controller-health-before,runners-before}.json=present(unread)
04-evaluation/job-01-dual-build/job-id.txt=read
04-evaluation/job-01-dual-build/job-id2.txt=read
evaluator_manifest.json=present(unread)
result.md=read
```
No `01-frozen/frozen-inputs.md` (absent). No `source/`, `target/`.

### 3. Findings
- **Freeze/classify.** Classification artifact present (v2.4, ALLOWED, `REVIEW_SIDE_EFFECTS` — same classifier sha as D2-060). `frozen-inputs.md` **absent** ⇒ freeze writeback unverifiable, same gap as D2-060.
- **Source precheck (job-00).** `eval-20261011-104654-1456063c`, os linux, `go build -o program inbox_batch_validate.go`, `completed`/exit 0, execution `completed/0`; observed stdout non-empty (artifact line + `records`/`errors` JSON, key order `records` then `errors`). Diagnostic none. Cleanup evidence absent ⇒ UNVERIFIED.
- **Requests/responses.** `target.gen.model.json` is a **real body**: role assistant, fenced `ruby` content (real `JSON`/`FileUtils`, `temp_dir` reading only `ENV['TMPDIR']`, `trim_space` using `[[:space:]]`, `parse_kv`, `File.binwrite`, `JSON.pretty_generate`) plus `reasoning_content` where the model itself notes the `Dir.tmpdir` vs Go `os.TempDir` divergence and the 64 KB `bufio.Scanner` max-token question — i.e. the model rehearsed the exact concerns the self-review later raised. `self-review-1.model.json` present (unread). Failed attempts: 0 (`failedAttempts 0`).
- **Self-review.** `self-review-1.json` verdict **`REPAIR-RECOMMENDED`**, 2 items, both `origin: conversion-introduced`: (1) `target.gen.rb:10-12` `[[:space:]]` matches a wider Unicode whitespace set than Go `strings.TrimSpace`; (2) `target.gen.rb:6-9` `temp_dir` checks only `$TMPDIR`, Go `os.TempDir()` also checks `TMP`/`TEMP`. Proposed fixes are concrete regex-based fixes and an env-fallback chain. **No repair was applied** (`codeRevisions 0`), and `events.jsonl` line 606 explicitly records the self-review as a **misjudgment** relative to the real cause.
- **Device-fault event (recorded, not a conversion defect).** First dual job `eval-20261011-105036-13c25bc9` (`job-id.txt`) reported target exit 1 with empty stdout; `result.md` and `events.jsonl` 607 attribute it to the hand-written `target/run_case.py` containing a real newline inside a byte literal (`SyntaxError: unterminated string literal`, line 34) so `target.rb` never ran. After rewriting the driver only, resubmission `eval-20261011-105217-bb67e0b9` (`job-id2.txt`) produced byte-identical digests. **Two job-ids are retained** — good provenance.
- **Job-01 (final).** `eval-20261011-105217-bb67e0b9`. `comparison.json`: `behaviorVerdict matched`, output `matched`, `diffs []`, other dimensions `not-applicable`, bundleIds both `evb-{source,target}-eval-20261011-105217-bb67e0b9`, same comparator preset/tokens. Side effects: none beyond design. Cleanup: no dedicated artifact ⇒ UNVERIFIED (only `controller-health-after.json`).
- **result.md / evaluator_manifest.json.** Both present (manifest unread). `result.md` is unusually complete: it states the root cause, quotes the `SyntaxError`, states "target.rb 从未被执行", and states **"未消耗任何模型修复调用"** — i.e. the recorded failure was attributed to the device, not to the code.
- **Anomalies.** (a) `frozen-inputs.md` absent. (b) `source/`/`target/` trees absent in this copy. (c) The `job-id.txt`/`job-id2.txt` naming means the primary `job-id.txt` points at the **failed** job, not the accepted one — a reader taking only `job-id.txt` would pick the wrong job. This is not flagged in `result.md`.
- **Independent evidence facts.** The decisive fact is the digest equality in the second submission; the first submission's mismatch is not evidence about `target.rb` because the driver crashed before execution. `events.jsonl` 606–608 agree with `result.md` and item json.
- **Attribution.** Code-level claims in the self-review are plausible but **not causal** for the observed failure; the recorded cause is device. The two self-review items remain **open, unrepaired, and unexercised by the fixture** (Unicode whitespace and `TMP`/`TEMP` paths are outside the single 3-line fixture), so they are unresolved *risk*, not measured defects. Per instructions: model reasoning/self-review is not a conclusion, and the platform verdict is preserved.
- **Knowledge candidates + current-contract coverage.** (1) *Device-first discipline* — already registered as `batch/operational-discipline.md` **§16 "装置优先"** (line 561) and **explicitly sourced from D2-061/D2-062**: this item is the origin of an existing rule, so no new rule is needed; the only gap is that `job-id.txt` vs `job-id2.txt` is not part of §16's required writeback. (2) *`job-id2.txt` naming/pointer discipline* — candidate new rule: the accepted job id must be unambiguously named (or §16 must require recording both). (3) *Self-review items left unrepaired* maps to **§10.5** (line 102, locate before repairing) and **§10.12** (line 174, don't keep trying drivers on one path); coverage adequate.
- **Optimization.** Rename to `job-id-attempt1.txt` / `job-id-accepted.txt`, or add an explicit `acceptedJobId` field to `metadata.json`. Also record the driver-change only as a device item, and keep the two self-review items in `openIssues` rather than silently dropping them.
- **Unknowns.** `frozen-inputs.md` existence; cleanup outcome for both jobs; `evaluator_manifest.json` contents; whether the two self-review items hold on a fixture that exercises Unicode whitespace / `TMP` only.

---

## D2-062

### 1. Identity
- taskId `D2-062`; kind `REUSE`; direction `go-to-ruby`; source `loopback_ack_exchange.go`; manifest declared Sha256 `65E8CC61D25161543F6BBD5792AF6F508830B8D28F4438ECF1DBA3905B893259` (= item `sourceSha256`, consistent).
- casePath `docs/test/dataset-2/go-to-ruby/handoff-2026-10-02-d29-loopback-ack-exchange-go`; dir `go-to-ruby/handoff-2026-10-02-d29-loopback-ack-exchange-go`.
- disposition `CONVERTED`, phase `CLOSED`, **lifecycle `PARTIAL`**, `oracleFreezability ORACLE_NOT_FREEZABLE`, pendingAction (zh) "另冻条件使可观察量确定化（移出 report 中的动态回环端口 127.0.0.1:&lt;port&gt;），或平台 ephemeral-ports 覆盖该形态", blockingReasons `[]`.
- targetSha256 `05442627…75a4883a`; classifier v2.4 `ALLOWED` / cls `REVIEW_NETWORK` / note "RE-classified as classification-2.json after the driver fix … network_mode=loopback".
- usage: 2 requests, prompt 3092, completion 16478, reasoning 15445, total 19570, `deepseek-flash`, failedAttempts 0.

### 2. File inventory (51 files, case root `…-loopback-ack-exchange-go/output/batch/`)
```
01-frozen/classification-1.json=present(unread)
01-frozen/classifier-input.json=present(unread)
01-frozen/classification-2.json=present(unread)
01-frozen/frozen-inputs.md=present(unread)
02-conversion/observed-source-stderr.txt=empty
02-conversion/observed-source-stdout.txt=present(unread)
02-conversion/target.gen.model.json=present(unread)
02-conversion/request.system.txt=present(unread)
03-self-review/self-review-1.json=read
03-self-review/review.system.txt=present(unread)
03-self-review/self-review-1.model.json=present(unread)
04-evaluation/job-00-source-buildability/{batch-authorization,job-id.txt,input_profile,metadata,controller-health-before,runners-before,this-task-classification,comparison_manifest}.json/.txt=present(unread)
04-evaluation/job-00-source-buildability/returned-evidence/{evaluation_report,evidence-source}.json=present(unread)
04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json=present(unread)
04-evaluation/job-01-dual-build/returned-evidence/comparison.json=read
04-evaluation/job-01-dual-build/returned-evidence/evidence-source.json=read(截断>2000)
04-evaluation/job-01-dual-build/returned-evidence/{controller.log,evaluation_report.json,evaluation_report.md}=present(unread)
04-evaluation/job-01-dual-build/{batch-authorization,comparison_manifest,input_profile,this-task-classification,metadata,controller-health-after,job-id.txt}.json/.txt=present(unread)
04-evaluation/job-00b-source-buildability/{comparison_manifest,input_profile,batch-authorization,controller-health-before,controller-health-after,job-id.txt,runners-before,this-task-classification,metadata}.json/.txt=present(unread)
04-evaluation/job-00b-source-buildability/returned-evidence/{evaluation_report.md,evidence-source,comparison,evidence-target,controller.log,evaluation_report.json}=present(unread)
evaluator_manifest.json=present(unread)
result.md=read
```
`01-frozen/frozen-inputs.md` **present** (unique among the five: it is the only case here with a second classification and a freeze record, both consistent with the re-classification event). No `source/`, `target/`.

### 3. Findings
- **Freeze/classify.** Two classification artifacts: `classification-1.json` and `classification-2.json` (re-classified because `source/run_case.py` changed and is part of the source tree, so the classifier input hash changed). `frozen-inputs.md` present. `events.jsonl` 610–620 corroborates the sequence.
- **Source precheck (job-00 / job-00b).** First attempt `eval-20261011-105443-233ae732` (`job-00/job-id.txt`): build `completed`/exit 0 **but execution `completed/1` with empty stdout** — recorded root cause `NameError: name 'SIDE' is not defined` (run_case.py:38) plus swapped source/target sides, so the source program **never ran**. Fixed driver, re-classified, re-prechecked as `job-00b` = `eval-20261011-120321-e40bc9d7` (`job-00b/job-id.txt`), build **and** execution `completed/0`, non-empty report. Diagnostic: driver/device, not source. Cleanup: no dedicated artifact ⇒ UNVERIFIED.
- **Requests/responses.** `target.gen.model.json` present (unread); `events.jsonl` 617 records target `target.rb`, model `deepseek-flash`, `codeRevisions 0`, `finish_reason=stop`. Failed attempts: 0.
- **Self-review.** `self-review-1.json` verdict `NO-REPAIR-IDENTIFIED`, 6 items, all `origin undetermined`, `proposed_fix null`. Scope: dynamic ephemeral port binding, `Digest::SHA256.hexdigest`, frame build/parse/NACK path, report hash insertion order + `JSON.pretty_generate` (2-space, no trailing newline), `server.local_address.ip_port`, artifact line/exit 0. Notably **item 5 itself identifies the dynamic port as "no issue"** — the self-review explicitly *endorsed* the very quantity that later made the oracle unfreezable. No repairs (`codeRevisions 0`, `selfRepairRounds 0`).
- **Job-01 (dual build).** `eval-20261011-120717-7ef07194`. Independent evidence: `evidence-source.json` `runRole source`, build `completed/0` dur 8276 ms, execution `completed/0` dur 34 ms, artifactLanguage `go`, stdout 184 bytes, digest `sha256:c7216f41…81b3f3`, body `\"remote\": \"127.0.0.1:34487\"`. `evidence-target.json` `runRole target`, build `completed/0` dur 77 ms with **`Syntax OK`** on stdout (digest `bbafef10…4a1b`, 10 bytes), execution `completed/0` dur 220 ms, artifactLanguage `ruby`, digest `sha256:af8d30bd…2c5eef`, body `\"remote\": \"127.0.0.1:35553\"`. Both runs linux x64, same snapshot/runner, same `inputProfileHash sha256:4beda9aa…`.
- **Comparison verdict + diffs.** `comparison.json`: `behaviorVerdict mismatched`; output dimension `mismatched`, exactly **one** diff `stream.normalizedText`, `kind changed`, `criticality major`, `rule normalized-text`, evidenceRefs `["stream/normalizedText"]`; all other dimensions `not-applicable`. The two `*ValueSummary` prefixes are identical (`artifact: <TEMP_PATH:1>` then the same `client_ack`), so the divergence lies only in the `remote` port. This matches the item-json `onlyDiff` (`remote (dynamic loopback port 34487 vs 35553)`, criticality major, attribution "device/environment … NOT conversion-introduced") and the item's identicalFields list (artifact line, `client_ack=ACK|node-127`, `server_result=ok`, JSON structure/indent, top-level key order).
- **result.md / evaluator_manifest.json.** Both present. `result.md` records the incoherence explicitly: **不记转换失败**, platform verdict preserved, `PARTIAL` + `ORACLE_NOT_FREEZABLE`, "同 D2-044", and states the `ephemeral-ports` token did **not** absorb the `127.0.0.1:<port>` form.
- **Anomalies.** (a) A job directory named `job-00b-source-buildability` also carries a **full comparison** (`returned-evidence/comparison.json`, `evidence-target.json`) — i.e. a precheck slot was reused as a dual submission; job naming no longer describes job content. (b) The **first** job-00 failed for device reasons yet `result.md`/item json keep `pendingAction` scoped only to the oracle issue; the device fault is recorded only in `events.jsonl`/`result.md` prose, not as a field. (c) `source/`/`target/` trees absent in this copy.
- **Independent evidence facts.** Directly read: source stdout 184 bytes with port 34487 vs target 184 bytes with port 35553; both sides exit 0, both stderr empty; `Syntax OK` proves the Ruby file parsed. Therefore the *only* observed difference is an OS-assigned ephemeral port embedded in a JSON field. The target genuinely binds `127.0.0.1:0` and reads back the kernel-assigned port — it is not hard-coded.
- **Attribution.** Device/environment (non-reproducible OS-assigned quantity not absorbed by the comparator's `ephemeral-ports` token). Correctly **not** filed as conversion-introduced. Platform verdict not self-overturned; consistent with `batch/operational-discipline.md` §10.16 and §15.
- **Knowledge candidates + current-contract coverage.** (1) **§10.16** (`batch/operational-discipline.md` line 267 "可观察量必须可复现…记 UNVERIFIED，不记转换失败") covers the principle; its criterion list at line 278 enumerates "活动计数器"-type quantities but **does not name OS-assigned identifiers (`127.0.0.1:<ephemeral port>`, PID, temp file name)**. Candidate: enumerate this instance class explicitly, citing D2-044 and D2-062. (2) **§15** (line 535) covers *execution duration* specifically — the port case is a sibling, not a §15 instance; without the §10.16 amendment, a reviewer could misread §15 as the only non-reproducible class. (3) The **comparator-side** fix (make the `ephemeral-ports` token absorb `host:port`) is a platform capability, not a rule the skill can enforce — worth recording as a platform request with this case as evidence. (4) **Self-review cannot certify oracle freezability**: item 5 of the self-review marked the dynamic port as "no issue" while the same quantity sank the oracle. No current rule states that oracle freezability is *not* a self-review responsibility — candidate new rule (cite §10.16 as the place, since §10.16 already owns the verdict).
- **Optimization.** Rename job dirs by submission role rather than ordinal (`job-00b` → `job-02-reprecheck`) or store an explicit `submissionRole` in `metadata.json`; add a structured `deviceFaults: []` array to the item json instead of relying on prose; pre-screen frozen values for OS-assigned identifiers at freeze time (a checklist line, not a script).
- **Unknowns.** `evaluator_manifest.json`, `classification-2.json`, `frozen-inputs.md`, `request.system.txt`, `target.gen.model.json` contents (unread); whether the port diff was the *only* byte difference in the middle of the truncated `evidence-*` bodies (the comparison's `major` single diff says yes, but the summaries are truncated at 2000 chars); cleanup outcome for all three jobs.

---

## D2-063

### 1. Identity
- taskId `D2-063`; kind `REUSE`; direction `go-to-ruby`; source `loopback_tcp_receiver.go`; manifest declared Sha256 `86661C04073AC7746D795A3C0576EA34D7A350E9038C674A054BBCCB03A59882` (= item `sourceSha256`, consistent).
- casePath `docs/test/dataset-2/go-to-ruby/handoff-2026-10-02-d29-loopback-tcp-receiver-go`; dir `go-to-ruby/handoff-2026-10-02-d29-loopback-tcp-receiver-go`.
- disposition `CONVERTED`, phase `CLOSED`, lifecycle `DONE`, pendingAction `null`, blockingReasons `[]`. targetSha256 `3ba22893…cb42781`.
- classifier v2.4 `ALLOWED` / cls `REVIEW_NETWORK` / `network_mode=loopback` / sha `009a6f31…f3a4`.
- usage: 2 requests, prompt 2122, completion 13849, reasoning 12159, total 15971, `deepseek-flash`, failedAttempts 0.

### 2. File inventory (41 files, case root `…-loopback-tcp-receiver-go/output/batch/`)
```
01-frozen/classifier-input.json=present(unread)
01-frozen/classification-1.json=present(unread)
01-frozen/frozen-inputs.md=present(unread)
02-conversion/observed-source-stdout.txt=present(unread)
02-conversion/observed-source-stderr.txt=empty
02-conversion/target.gen.model.json=present(unread)
02-conversion/request.system.txt=present(unread)
03-self-review/self-review-1.json=read
03-self-review/self-review-1.model.json=present(unread)
03-self-review/review.system.txt=present(unread)
04-evaluation/job-00-source-buildability/{batch-authorization,comparison_manifest,input_profile,metadata,controller-health-after,controller-health-before,this-task-classification,runners-before,job-id.txt}=present(unread); metadata.json=read
04-evaluation/job-00-source-buildability/returned-evidence/{evaluation_report.json,evaluation_report.md,evidence-source.json,evidence-target.json,controller.log}=present(unread)
04-evaluation/job-00-source-buildability/returned-evidence/comparison.json=read
04-evaluation/job-01-dual-build/{comparison_manifest,batch-authorization,input_profile,metadata,this-task-classification,controller-health-after,job-id.txt}=present(unread)
04-evaluation/job-01-dual-build/returned-evidence/comparison.json=present(unread)
04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json=read(截断>2000)
04-evaluation/job-01-dual-build/returned-evidence/{evaluation_report.json,evaluation_report.md,evidence-source.json,controller.log}=present(unread)
evaluator_manifest.json=present(unread)
result.md=read
```
`01-frozen/frozen-inputs.md` present. No `source/`, `target/`.

### 3. Findings
- **Freeze/classify.** `classification-1.json` + `frozen-inputs.md` present; cls `REVIEW_NETWORK`, ALLOWED.
- **Source precheck (job-00).** `eval-20261011-121016-68bb60fc` (`job-00/job-id.txt`), os linux, build/execution `completed/0`, observed stdout = artifact line + `--- received ---` + `loopback transfer`. Diagnostic none. **But** `job-00/metadata.json` — read directly — declares `targetArtifact: "target/target.rb (placeholder)"` and `targetHash: "sha256:placeholder-precheck"`, i.e. a source-only precheck, while the same `job-00` directory holds a **full dual** `returned-evidence/` with `evidence-target.json`, `comparison.json` and `controller.log`. Those two readings contradict each other. Cleanup: no dedicated artifact ⇒ UNVERIFIED.
- **Requests/responses.** `target.gen.model.json` present (unread); `events.jsonl` 623 records `finish_reason=stop`, `codeRevisions 0`; `failedAttempts 0`.
- **Self-review.** `self-review-1.json` verdict `NO-REPAIR-IDENTIFIED`, **8 items**, 7 `origin undetermined` + **1 `origin conversion-introduced`** with `proposed_fix null` and `risk 低`: the Ruby acceptor's inner `rescue` also covers `conn.read` raising (→ `recv << nil`), whereas Go discards `io.ReadAll`'s error and only maps `ln.Accept()` failure to `nil`. The review itself states this branch is **never triggered by the fixed payload**, i.e. a boundary difference outside the exercised observation face. No repairs (`codeRevisions 0`, `selfRepairRounds 0`).
- **Job-01 (dual build).** `eval-20261011-121253-9a50db2d` (`job-01/job-id.txt`). Independently read `evidence-target.json`: `runRole target`, `artifactLanguage ruby`, build `completed/0` dur 181 ms stdout **`Syntax OK`** (digest `bbafef10…4a1b`, 10 bytes), execution `completed/0` dur 274 ms, stdout 98 bytes digest **`sha256:3a060f7a…df0c9f5`**, stderr empty, linux x64, `inputProfileHash sha256:225767ec…`. `comparison.json`: `behaviorVerdict matched`, output `matched`, `diffs []`, other dimensions `not-applicable`, bundleIds `evb-{source,target}-eval-20261011-121253-9a50db2d`. The target digest **equals** the source digest recorded in item json (`3a060f7a…`), so byte-identity is confirmed from real evidence. Side effects: received.txt write by design. Cleanup: no dedicated artifact ⇒ UNVERIFIED.
- **result.md / evaluator_manifest.json.** Both present. `result.md` explains the oracle is FREEZABLE because the listening port never appears in output, and contrasts explicitly with D2-062's `PARTIAL` — the diagnostic value of the pair.
- **Anomalies.** (a) **Stale/mixed artifacts in `job-00-source-buildability`**: `metadata.json` declares a placeholder target and a source-only precheck, yet the same directory's `returned-evidence/comparison.json` is a **dual-build comparison with `behaviorVerdict mismatched`**, diff `stream.normalizedText` (major) with `sourceValueSummary` = the correct `artifact: <TEMP_PATH:1>\n--- received ---\nloopback transfer\n\n` and **`targetValueSummary` = `--- received ---\nMISSING`**. That is an earlier failed dual attempt (target produced nothing) whose artifacts were retained inside the precheck directory. Nothing in `result.md` or `events.jsonl` 621–626 mentions this failed dual attempt — and `job-00`'s recorded precheck result (`completed/0`) is not the same event as the comparison stored beside it. This is the clearest documentation defect in the batch subset. (b) `source/`/`target/` trees absent in this copy.
- **Independent evidence facts.** Accepted dual job: both sides exit 0, both stderr empty, target `Syntax OK`, target stdout digest identical to source (`3a060f7a…`), single applicable dimension `output` with zero diffs. Non-accepted stale comparison: target side rendered `MISSING`, verdict `mismatched` — evidence of a device/driver failure at that time, not of the current `target.rb`.
- **Attribution.** Accepted result = conversion-consistent (matched, 0 diffs). The stale `job-00` comparison must **not** be attributed to the conversion; it is a device artifact. The single self-review `conversion-introduced` item is a genuine but **unexercised** narrowing of an error branch.
- **Knowledge candidates + current-contract coverage.** (1) *One job directory must contain exactly one submission and its own artifacts*: not covered by `batch/operational-discipline.md`; §10.11 (line 168, "取证必须等终态") and §10.13 (line 203, symmetric post-processing) are adjacent but do not forbid artifact mixing. Candidate new rule, with D2-063 `job-00` as the worked example. (2) *Unread/stale evidence must not be counted*: §10.6 (line 107) protects against degenerate `matched`; here the risk is the inverse — a stale `mismatched` left on disk could be mistaken for a real verdict. Candidate: require a per-job `supersededBy`/`superseded` marker. (3) The loopback `network` dimension is reported `not-applicable` even though cls is `REVIEW_NETWORK` and the program does real loopback I/O — a comparator scoping fact worth recording (no rule currently states when the network dimension is applicable).
- **Optimization.** Move failed-attempt evidence to a distinct `attempts/` subdirectory, or add `superseded: true` + `supersededBy: eval-…` to stale evidence; state in `result.md` every job directory that exists and what each contains.
- **Unknowns.** `evaluator_manifest.json`, `frozen-inputs.md`, `request.system.txt`, `target.gen.model.json`, and 4 `evidence-source.json` instances (unread); which job the stale `job-00` comparison was originally submitted under; cleanup outcome for both jobs.

---

## D2-064

### 1. Identity
- taskId `D2-064`; kind `REUSE`; direction `go-to-ruby`; source `notes_zip_bundle.go`; manifest declared Sha256 `A32CB8B0B356E43D62F1EFB1FA33EC33D5F5D7E7D6F50E2FA53D2E7C6E8C7AA3` (= item `sourceSha256`, consistent).
- casePath `docs/test/dataset-2/go-to-ruby/handoff-2026-10-02-d29-notes-zip-bundle-go`; dir `go-to-ruby/handoff-2026-10-02-d29-notes-zip-bundle-go`.
- disposition `CONVERTED`, phase `CLOSED`, lifecycle `DONE`, pendingAction `null`, blockingReasons `[]`. targetSha256 `d881c8dd…a6d87bb`.
- classifier v2.4 `ALLOWED` / cls `REVIEW_SIDE_EFFECTS` / note "no network" / sha `009a6f31…f3a4`.
- usage: 2 requests, prompt 2728, completion 24273, reasoning 22889, total 27001, `deepseek-flash`, failedAttempts 0.

### 2. File inventory (40 files, case root `…-notes-zip-bundle-go/output/batch/`)
```
01-frozen/classifier-input.json=present(unread)
01-frozen/classification-1.json=present(unread)
01-frozen/frozen-inputs.md=present(unread)
02-conversion/observed-source-stdout.txt=present(unread)
02-conversion/observed-source-stderr.txt=empty
02-conversion/target.gen.model.json=present(unread)
02-conversion/request.system.txt=present(unread)
03-self-review/review.system.txt=present(unread)
03-self-review/self-review-1.json=read
03-self-review/self-review-1.model.json=present(unread)
04-evaluation/job-00-source-buildability/{batch-authorization,comparison_manifest,input_profile,metadata,controller-health-after,controller-health-before,runners-before,this-task-classification,job-id.txt}=present(unread)
04-evaluation/job-00-source-buildability/returned-evidence/{evaluation_report.md,evidence-source.json,comparison.json,evidence-target.json,controller.log,evaluation_report.json}=present(unread)
04-evaluation/job-01-dual-build/{comparison_manifest,input_profile,batch-authorization,this-task-classification,controller-health-after,metadata,job-id.txt}=present(unread)
04-evaluation/job-01-dual-build/returned-evidence/{comparison.json,evaluation_report.json,evaluation_report.md,evidence-source.json,controller.log}=present(unread)
04-evaluation/job-01-dual-build/returned-evidence/evidence-target.json=read(截断>2000)
evaluator_manifest.json=present(unread)
result.md=read
```
`01-frozen/frozen-inputs.md` present. No `source/`, `target/`.

### 3. Findings
- **Freeze/classify.** `classification-1.json` + `frozen-inputs.md` present; cls `REVIEW_SIDE_EFFECTS`, ALLOWED, no network.
- **Source precheck (job-00).** `eval-20261011-121505-38125a96` (`job-00/job-id.txt`), os linux, build/execution `completed/0`, observed stdout = artifact line + sorted zip entry names + each `note*.txt` body + the `docs/` fixtures. Note this `job-00` directory carries a **dual** `returned-evidence/` set (same pattern as D2-063). Cleanup: no dedicated artifact ⇒ UNVERIFIED.
- **Requests/responses.** `target.gen.model.json` present (unread); `events.jsonl` 629 records that the target **self-implemented a minimal ZIP writer** (STORE + `Zlib.crc32` + hand-written LFH/central-directory/EOCD) rather than shelling out — a notable non-stub outcome; `codeRevisions 0`; `failedAttempts 0`.
- **Self-review.** `self-review-1.json` verdict **`REPAIR-RECOMMENDED`**, 1 item, `origin conversion-introduced`: `FileUtils.mkdir_p(docs)` (default mode) followed by explicit `File.chmod(0o755, docs/root)` is not fully equivalent to Go `os.MkdirAll(docs, 0o755)` — intermediate `/tmp/safe-attck-go` may not be 0755 under a non-022 umask, and pre-existing `docs`/`root` permissions get overwritten. Proposed fix: `FileUtils.mkdir_p(docs, mode: 0o755)` and drop the explicit chmods. `risk: 低`. **Not adopted**; item json records `selfReviewAdopted false` with the reasoning that the item lies **outside the observation face** (the driver reads file *contents*, not directory permissions) and the measured result was `matched`, diffs 0, per §10.5 and the D2-061 precedent. `codeRevisions 0` / `selfRepairRounds 0`.
- **Job-01 (dual build).** `eval-20261011-121818-85e2f9ef` (`job-01/job-id.txt`). Independently read `evidence-target.json`: `runRole target`, `artifactLanguage ruby`, build `completed/0` dur 125 ms stdout `Syntax OK` (digest `bbafef10…4a1b`), execution `completed/0` dur 278 ms, stdout 267 bytes digest **`sha256:88f460f7…e089ee77`**, stderr empty, linux x64, `inputProfileHash sha256:4866eaad…`. `comparison.json`: `behaviorVerdict matched`, output `matched`, `diffs []`, other dimensions `not-applicable`, bundleIds `evb-{source,target}-eval-20261011-121818-85e2f9ef`. item json source digest `88f460f7…` **equals** the target digest read here ⇒ byte-identity confirmed independently. Side effects: zip + docs files by design. Cleanup: no dedicated artifact ⇒ UNVERIFIED.
- **result.md / evaluator_manifest.json.** Both present. `result.md` states the entry-order nondeterminism (Go map iteration) is removed by sorted driver readback and that zip binary bytes are excluded by design; it explicitly documents why the self-review item was not adopted.
- **Anomalies.** (a) `job-00-source-buildability` again carries a full dual `returned-evidence/` set while `result.md` presents job-00 as a source-only precheck — same artifact-mixing pattern as D2-063; unlike D2-063 no contradicting `metadata.json` was read here, so the exact status is unverified. (b) The self-review's `conversion-introduced` finding is **recorded and consciously waived** — a permission-semantics difference that is real but unobservable in this harness; it is unresolved risk rather than a measured defect. (c) `source/`/`target/` trees absent in this copy.
- **Independent evidence facts.** Accepted dual job: both sides exit 0, both stderr empty, target `Syntax OK`, target stdout digest identical to the item-json source digest, single applicable dimension `output` with zero diffs. The comparison cannot see directory permissions, so the waived item is genuinely outside the measured face — the waiver is defensible on the recorded evidence, though it means the difference is untested rather than disproved.
- **Attribution.** Matched result attributable to the conversion; the permission-semantics item attributable to conversion but out of observation scope; no device fault recorded for this item.
- **Knowledge candidates + current-contract coverage.** (1) *Directory-creation semantics* is **already registered**: `batch/operational-discipline.md` **§5 "目录创建语义（源自 D2-003，实测证实）"** (line 27). D2-064's self-review item is exactly a §5 instance, and the non-adoption aligns with §5 + §10.5 (line 102). Coverage adequate — but §5 and the self-review reached opposite *dispositions* (D2-003 measured, D2-064 waived), so the current text may not make clear that a §5-class difference is only actionable when the observation face can see it. Candidate clarification, cite §5 + §10.4 (line 97). (2) *Observation-face boundary must be stated when waiving a finding*: partially covered by §10.7 (line 126, retrospective scope) and §10.13 (line 203); no rule requires the waiver rationale to name the driver's observation face. Candidate new rule. (3) *ZIP / archive determinism* (entry order, mtime, compression) is handled **only in this case's prose**, not registered in `operational-discipline.md`; candidate new §-entry (paired with D2-060), since two independent items hit the same "archive binary bytes are not an oracle" decision.
- **Optimization.** Register the archive-determinism rule once instead of re-deriving it per case; require each non-adopted `REPAIR-RECOMMENDED` item to carry a `notAdoptedBecause` + `observationFace` field so the waiver is machine-checkable; separate job-00 precheck artifacts from dual-build artifacts.
- **Unknowns.** `evaluator_manifest.json`, `frozen-inputs.md`, `request.system.txt`, `target.gen.model.json`, `job-00` `metadata.json`/`comparison.json` (unread, so the job-00 mixing status is inferred by pattern, not proven); cleanup outcome for both jobs.

---

## D2-065

### 1. Identity
- taskId `D2-065`; kind `REUSE`; direction `powershell-to-csharp`; `targetLang csharp`; source `Get-Information.text`; manifest declared Sha256 `0452B97187970D457223C678F95C3170C68B0375CE38F9F022569BCEEB544807` (= item `sourceSha256`, consistent).
- casePath (item json) `docs/test/dataset-2/powershell-to-csharp/handoff-2026-10-02-d39-get-information-text`; manifest col-8 datasetPath `dataset/powershell-to-csharp/handoff-2026-10-02-d39-get-information-text`; reviewed dir `powershell-to-csharp/handoff-2026-10-02-d39-get-information-text`.
- item json: disposition **`FROZEN`**, phase **`NOT_STARTED`**, lifecycle **`WAITING`**, `pendingAction` = "REOPEN: the C# target platform defect (evidence-bundle schema) was FIXED on 2026-10-11 (probe eval-20261011-122249-fe456bbe: target build/exec completed/0). Run the full chain for this item.", `blockingReasons []`, `blockerRef batch/platform-blocker-csharp-target.md`, `dispositionNote` (originally WAITING/BLOCKED_ENV, now reopened; source is a Windows-only entry-less Nishang function doing registry reads, so **the oracle may not be freezable — to be determined**).
- `verdicts` all `UNVERIFIED` except `environment n/a`, `safety not-classified`. usage: `requests 0`, "no model calls consumed; deferred by a known platform defect". No `classifier` block, no `sourcePrecheck`, no `evaluation`, no `coverageGaps`, no `codeRevisions`/`selfRepairRounds`.

### 2. File inventory
```
powershell-to-csharp/  -> dir-empty
```
- `read(powershell-to-csharp)` → `not a regular file` ⇒ the directory **exists**.
- `glob powershell-to-csharp/**/*` → **0 files**; `glob powershell-to-csharp/*` → **0 files**; `glob powershell-to-csharp/D2-065-*` → **0 files**.
- `read(powershell-to-csharp/handoff-2026-10-02-d39-get-information-text)` → `not a regular file` ⇒ the case directory **also exists** but holds **no files at any depth**.
- Therefore: **the direction dir is `dir-empty`, and the expected case dir is `dir-empty` (present-but-empty), not absent.** No `output/batch`, no `result.md`, no `evaluator_manifest.json`, no `01-frozen`, no jobs — nothing at all. There is no case to inventory.

### 3. Findings
- **Freeze/classify.** Neither performed: no `01-frozen/*`, no classifier artifact. This is consistent with `phase NOT_STARTED` / `lifecycle WAITING` / `usage.requests 0` and with `events.jsonl` line 633 (`DEFERRED`, `WAITING`, `BLOCKED_ENV`, `blockerRef batch/platform-blocker-csharp-target.md`, "no job run, 0 model calls; only powershell-to-csharp item in the dataset"). The item json's disposition `FROZEN` therefore denotes **admission-state labelling, not a completed freeze writeback** — no `frozen-inputs.md` exists to support it.
- **Source precheck.** None. No job-00*, no build command, no exit code, no diagnostic, no cleanup evidence.
- **Requests/responses.** None. `requests 0`; no `request.system.txt`, no `*.model.json`, no failed attempt.
- **Self-review.** None.
- **Jobs.** None. No job-NN directories, so no caseId/artifactLanguage/os, no source/target stdout/stderr/exit, no side effects, no comparison verdict/diffs, no report/closure/health artifact, no cleanup — all **UNVERIFIED by absence**, not by failure.
- **result.md / evaluator_manifest.json.** **Both absent.** Per the delivery contract cited in AGENTS.md §3 (交付完整性/终态门禁, `references/framework/delivery-handoff-contract.md` §1.1) a WAITING item still requires a `result.md` recording the reason and coverage; that is missing here. This is the substantive compliance gap for D2-065 (the batch-level note lives only in `batch/platform-blocker-csharp-target.md` and `events.jsonl`).
- **Anomalies.**
  1. **Direction directory empty.** `powershell-to-csharp` contains **no files at all**, yet `manifest.csv` row 65 and `batch/items/D2-065.json` both reference a concrete case path with a declared source hash. The declared source (`Get-Information.text`, sha `0452b971…`) is not present anywhere under the reviewed copy, so the declared hash **cannot be corroborated** and the "REUSE / dual-build-PASS (inherited)" manifest disposition is inherited-only.
  2. **Three-way path disagreement.** manifest datasetPath root is `dataset/…`; item json `casePath` root is `docs/test/dataset-2/…`; the reviewed copy root is `docs/dataset-2/dataset-2-copy/…`. None of the three matches for this item (nor for the five siblings), so path fields are not resolvable against the workspace as-is.
  3. **Reopen not reflected on disk.** `pendingAction` says REOPEN and the blocker file's own header says the defect is **fixed (2026-10-11)** and that the 38 affected C# items "不必再记 WAITING/BLOCKED_ENV", and `summary.md` line 527 agrees the recovery condition is met. Yet `lifecycle` remains `WAITING`, `phase NOT_STARTED`, `usage 0`, and no artifacts exist. The item json therefore describes a state its own `pendingAction` says should have advanced. `summary.md` line 527 also records that the pilot reopen (D2-007) was **stopped because the observation face was asymmetric (build artifacts included)** and honestly kept WAITING — so the reopen path is known to be blocked at the readiness gate, not merely unstarted. That D2-007 evidence directly predicts what D2-065 will hit.
  4. **`blockingReasons []` while `lifecycle WAITING`** with a `blockerRef` — the machine-readable blocker list is empty even though a named blocker file governs the item (the blocker is carried in `blockerRef`/`dispositionNote`/events instead).
- **Independent evidence facts.** From `batch/platform-blocker-csharp-target.md` (read in full): the C# target evidence-bundle defect (`collectorDiagnostics` extra `detail` property → `EvaluationContractError`, `INFRA_ERROR`/`AGENT_UNAVAILABLE`, target preflight SKIPPED) is marked **fixed 2026-10-11**, probe `eval-20261011-122249-fe456bbe` returned `COMPLETED` with target build/exec `completed/0` and `collectorDiagnostics=[]`. The file adds a **new discipline**: for C# targets `comparison_manifest.json` must set `target.artifactLanguage` to `csharp`, not `dotnet`, or the 1.0.28 submitter returns **403 `identity_mismatch`**; `source.artifactLanguage` likewise (e.g. `cpp`). This is a live, D2-065-relevant contract constraint that appears **only** in that blocker file (and not in `operational-discipline.md`'s §-list, which reaches §17).
- **Attribution.** Whole-item absence attributable to a previously known **platform/environment defect plus a deliberate deferral**, not to conversion or source defects. The original INFRA_ERROR was platform-side; the reopen blocker recorded for the pilot (D2-007) is **evaluation-readiness / observation-face asymmetry**, which is an apparatus matter. No conversion conclusion is possible or claimed. Correctly `UNVERIFIED` throughout.
- **Knowledge candidates + current-contract coverage.** (1) **`artifactLanguage=csharp` (not `dotnet`) identity rule** — currently lives only in `batch/platform-blocker-csharp-target.md` (lines 11–12). It is a submit-time hard gate that will 403 the item; it belongs in `batch/operational-discipline.md` next to **§12** (line 466, "提交端硬门禁：`caseId` 必须等于分类的 `case`…带前缀的旧命名会 403"), which is the analogous 403-identity rule. Candidate: promote it to a numbered §-entry and cross-link §12. (2) **`WAITING` items still owe `result.md`** — the requirement is stated in AGENTS.md §3 (交付完整性/终态门禁) pointing at `references/framework/delivery-handoff-contract.md` §1.1; D2-065 shows batch-level notes do not satisfy it per-item. Candidate: restate the per-item WAITING report obligation inside `operational-discipline.md` where batch operators actually read it. (3) **Observation-face asymmetry when build artifacts exist** (from D2-007, `summary.md` line 527) is not yet a numbered rule in `operational-discipline.md`; it is the concrete blocker for the C# reopen queue and deserves an entry, cite §10.4/§10.19 (line 396). (4) **`blockingReasons` empty under WAITING** — no rule requires the structured field to be populated when a `blockerRef` exists; candidate consistency rule.
- **Optimization.** (a) Give empty/deferred direction directories an explicit `DEFERRED.md` or per-item `result.md` stub so "no artifacts" is distinguishable from "artifacts lost"; (b) populate `blockingReasons` (e.g. `BLOCKED_ENV` / `EVAL_NOT_READY`) whenever `lifecycle=WAITING`; (c) reconcile the three path roots (`dataset/`, `docs/test/dataset-2/`, `docs/dataset-2/dataset-2-copy/`) to one canonical field; (d) before running the D2-065 chain, pre-check the two known gates: `artifactLanguage=csharp`, and the observation-face asymmetry of §D2-007.
- **Unknowns.** Whether `powershell-to-csharp` was ever populated and then emptied, or was never populated (no tombstone or note exists either way); whether the declared source hash `0452b971…` matches the real dataset source (source tree absent — uncorroborable here); whether the D2-065 oracle is freezable at all (item json itself defers this: entry-less Windows-only registry-reading Nishang function); whether `result.md` for this item exists anywhere outside the reviewed copy; the exact contents of `batch/items/D2-065.json`'s referenced `platform-probes/probe-csharp-target-2026-10-11/PROBE-RESULT.md` (referenced but not located in this pass).

---

## Batch-level observations (this subset)

1. **Empty direction directory.** `docs/dataset-2/dataset-2-copy/powershell-to-csharp/` is `dir-empty`; D2-065 has no artifacts, no `result.md`, no `evaluator_manifest.json`. `dir-missing` would be inaccurate — the directory exists.
2. **Source/target trees absent for all five processed cases.** `glob **/source/*` and `glob **/target/*` return 0 files across the whole copy, so every "交付完整性 完成 / 源/目标/驱动/清单齐备" claim in those `result.md` files is unverifiable from this copy; `evaluator_manifest.json` absolute paths point at a different host.
3. **Freeze writeback gap.** `01-frozen/frozen-inputs.md` exists for D2-062 and D2-064 (and D2-063, unread but globbed) but **not** for D2-060 and D2-061, which were nevertheless classified and driven to terminal state.
4. **Artifact mixing in precheck slots.** D2-062 `job-00b-source-buildability`, D2-063 `job-00-source-buildability` and D2-064 `job-00-source-buildability` all contain full dual-build evidence; in D2-063 the stored comparison is a **stale `mismatched`** ("target `MISSING`") that contradicts its own `metadata.json` placeholder declaration and is undocumented in `result.md`.
5. **Device faults are prose-only.** D2-061 and D2-062 both hit driver faults (`SyntaxError`, undefined `SIDE`) with the real cause in `result.md`/`events.jsonl` but no structured field in `batch/items/*.json`.
6. **Self-review ≠ verdict.** Across this subset the model self-review produced 2 `REPAIR-RECOMMENDED` verdicts that were both **not** the operative cause or **not** observable (D2-061 misjudgment; D2-064 out-of-face waiver), and 1 self-review item (D2-062, dynamic port) that marked as "no issue" the very quantity that made the oracle unfreezable. No self-review verdict in this subset was treated as a compilation or behavior conclusion.
7. **Rule coverage is partly already written.** D2-061/D2-062 are the *source* of `batch/operational-discipline.md` **§16** (line 561) and instantiate **§10.16** (line 267) / **§15** (line 535) and **§12** (line 466); D2-064 instantiates **§5** (line 27); D2-060/D2-064's archive-determinism decision and D2-063's stale-evidence hazard and D2-065's `csharp`-vs-`dotnet` identity gate are **not** yet registered.
