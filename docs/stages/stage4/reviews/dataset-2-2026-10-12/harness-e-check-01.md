# Harness E 补读验收 01 — D2-278 至 D2-289（ruby 方向，独文件）

- 会话角色：独立补读会话（非旧 E 会话）。只负责 D2-278…D2-289 共 12 项。
- 工作区根：`E:\桌面文档\Agents System\code_convert`。
- 方式：只用原生 `read` / `glob` / `grep`；纯文档审阅，不转换、不运行、不写辅助脚本、不做 ACL/权限/`.env`、不触碰 Controller/jobs、不改写原证据、不计算哈希、不改任何 verdict。
- 读取上限：单行 1,048,576 字节；本次 36 件强制件中，`evidence-source.json` 与 `closure.json` 均为**单行 JSON**，长度约 2–4 KB，远低于上限，`read` 均返回完整原文且 JSON 括号闭合；`items/<Id>.json` 为多行美化 JSON（52–53 行）。**36/36 件成功、0 件截断**（详见末尾“已读/未读/截断”）。
- 每项实际目录（源自 manifest 的 `Id` + `Origin`，落到 `docs/dataset-2/dataset-2-copy/<direction>/D2-NNN-<lang>-<file>/`），目录内**没有 source/target 文件**，只有 `output/` 树；三件强制件为：
  1. `.../output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`
  2. `.../output/batch/04-evaluation/job-00-source-buildability/returned-evidence/closure.json`
  3. `docs/dataset-2/dataset-2-copy/batch/items/D2-NNN.json`
- 声明：`collectorDiagnostics=[]` 只作字面记录，**不据此推断“无采集问题”**；`observations.output.events=[]` 只作字面记录，**不当作 stdout 为空的证据**（stdout 是否为空只看 `execution.stdout` 字段）；closure 摘要**不用于证明远端所列制品仍然存在**。
- 源/目标已删的限制保留：12 项均未找到源文件与目标文件；原始用例路径 `docs/test/dataset-2/...`（见各 item `casePath`）在磁盘上不存在（`glob docs/test/dataset-2/**/*.rb` = 0 命中）；manifest `Origin`（如 `测试用例ruby\执行\open3.rb`）也不存在（`glob 测试用例ruby/**/open3.rb` = 0 命中）。只有源 build/run 记录，**不等于转换完成**。

---

## D2-278 — ruby-to-c / open3.rb

- 三件真实路径（根相对；磁盘绝对前缀 `E:\桌面文档\Agents System\code_convert\`）：
  - `docs/dataset-2/dataset-2-copy/ruby-to-c/D2-278-ruby-open3.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`
  - `docs/dataset-2/dataset-2-copy/ruby-to-c/D2-278-ruby-open3.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/closure.json`
  - `docs/dataset-2/dataset-2-copy/batch/items/D2-278.json`
- 读取：三件全文成功，均未截断（1 行 / 1 行 / 53 行）。
- build：`status=completed`，`exitCode=0`，`durationMs=35`；stdout 实际内容 `"Syntax OK\n"`，`sizeBytes=10`，`digest=sha256:bbafef10c22b9323fa5589564990f57fbf57f9a632381d5e765dc5a3b25b4a1b`，`truncated=false`；stderr 内容 `""`，`sizeBytes=0`，`digest=sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`，`truncated=false`。
- execution：`status=completed`，`exitCode=0`，`durationMs=122`，`timedOut=false`；stdout `""`/0/`sha256:e3b0…b855`/`truncated=false`；stderr `""`/0/`sha256:e3b0…b855`/`truncated=false`。（stdout 为空系 `execution.stdout` 字段为 0 字节，非由 `events=[]` 推断。）
- observations/coverage：`output.status=observed`、`events=[]`、`limitations=[]`；`filesystem/processes.status=not-applicable`、`events=[]`、`limitations=[]`；`registry/network.status=not-applicable`、`events=[]`、`limitations=["evidence dimension is outside the current release scope"]`。`coverage.dimensions` 同此（output=observed，其余 not-applicable）。`createdAt=2026-10-12T05:42:50Z`。
- collectorDiagnostics：`[]`（字面）。
- baseline 身份/profile 关联：bundle `inputProfileHash=sha256:a7e757cb125ffeb017bb9576ad7c50fc58371fe43f2f11c72aedf2e750370350`；`baselineReference.artifactHash=sha256:ce76fb7ce70e2237d2b1a84c820aaef008f012610e73760d9c643f292900df7c`，`artifactLanguage=ruby`，`os=linux`，`arch=x64`，`snapshot=CC-Eval-Linux-8Lang-1.0.29`，`toolchainFingerprint={}`，`collectorVersion=1.0.0`，`agentVersion=1.0.0`，且 baseline 内 `inputProfileHash` 与 bundle 一致。`runtime.selectedRunner=linux-vm-agent-x64`，`workspaceRef=workspace/source`。job 级 `input_profile.json`：`profileId=D2-278`，`argv=[]`（与 item `frozenArgv=[]` 一致），`stdin=null`，`environment={}`，`workingDirectory=workspace`，`timeoutSeconds=60`，`fixtures=[]`，`observationPolicy.dimensions=["output"]`，`comparisonPolicy.output` 为 normalized-text。job 级 `metadata.json`：`sourceArtifact=source/open3.rb`，`sourceHash=sha256:59968079cf455f3bc1fea4af4ee56da6dfe95b34ac2f50cc5725dedeaf4a5d2d`，`networkBoundary=isolated VM`。
- closure：`complete=true`，`cleanupConfirmed=true`，`issues=[]`；`cleanupRecords.source={status:passed, runnerStateAfter:READY, attempts:1, contaminated:false, reason:null}`；`roles.source={build:passed, execution:completed, frozenSourceObligations:UNVERIFIED}`；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:43:17.294392+00:00`；`artifactDigests` 共 16 键：batch-authorization.json、classification.json、evaluation_report.json、evaluation_report.md、evidence/source-call.json、evidence/source-identity.json、evidence/source-request.json、evidence/source-response.body、evidence/source-response.json、evidence/source.json、input_profile.json、lifecycle.jsonl、metadata.json、request.json、source_preflight_manifest.json、staging-manifest.json。其中本机实际存在：batch-authorization.json、evaluation_report.json、evaluation_report.md、input_profile.json、metadata.json、source_preflight_manifest.json；**本地不存在**：evidence/ 下 6 件、lifecycle.jsonl、request.json、staging-manifest.json（名 `classification.json` 本地无同名文件，对应 `01-frozen/classification-1.json`）。远端制品是否仍在，本报告不作为结论。
- item 与原件一致性：`jobId=eval-20261012-054247-f8b64c8b` 三件一致；item `buildStatus=completed`/`exitCode=0`/`execution=completed`/`executionExitCode=0` 与 evidence 一致；`sourceSha256=5996…5d2d` 与 metadata `sourceHash`、manifest `Sha256`（大写形式）一致；`lifecycle=DONE`、`disposition=PREPARATION_GAP`、`phase=CLOSED_PREPARATION_GAP`、`evaluation=null`、`usage={requests:0, modelCalls:0}`、`blockingReasons=["PREPARATION_GAP"]`、classifier v2.4 `ALLOWED`/`blockingReason=null`/`cls=REVIEW_UNCERTAIN`。**不一致（新事实）**：manifest 该行 `Evidence="UNVERIFIED (not built, not run)"` 且 `JobId` 为空，与本项已有 build/run 且 `DONE` 的 items 记录矛盾；manifest `Lines=718` 与 `output/batch/result.md` 正文所称“764 行/引用 L764”不一致。

---

## D2-279 — ruby-to-cpp / delegate.rb

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-cpp/D2-279-ruby-delegate.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-279.json`。
- 读取：全文成功，均未截断（1/1/53 行）。
- build：`completed`/0，`durationMs=17`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/`truncated=false`；stderr `""`/0/`sha256:e3b0…b855`/false。
- execution：`completed`/0，`durationMs=116`，`timedOut=false`；stdout `""`/0/`sha256:e3b0…b855`/false；stderr `""`/0/`sha256:e3b0…b855`/false。
- observations：output `observed`/`events=[]`/`limitations=[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/`["evidence dimension is outside the current release scope"]`。`createdAt=2026-10-12T05:44:11Z`。
- collectorDiagnostics：`[]`。
- baseline/profile：bundle `inputProfileHash=sha256:3aea6d082cfec4d3192178b33adc4162e1015cea8f7db1b032a7faa93426e4b6`；`artifactHash=sha256:9a19c8ee8ba7a2e7561aac3beb63a03da843eb30823f96ce3bdbbff4fdb94c94`；其余同构（ruby/linux/x64/CC-Eval-Linux-8Lang-1.0.29/`toolchainFingerprint={}`/collector 1.0.0/agent 1.0.0），baseline 内 profileHash 与 bundle 一致；runner `linux-vm-agent-x64`，`workspaceRef=workspace/source`。`input_profile.json`：`profileId=D2-279`，`argv=[]`，dims `["output"]`，timeout 60。`metadata.json`：`sourceArtifact=source/delegate.rb`，`sourceHash=sha256:7475f488b718f148eeba6dfa045b688e9031f111c2517e9c3e010e426909c2e6`，`networkBoundary=isolated VM`，note 记 `cls=LOW_SIGNAL`（与 item 一致）。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/`attempts=1`/`contaminated=false`/`reason=null`；roles.source build `passed`、execution `completed`、frozenSourceObligations `UNVERIFIED`；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:44:38.836113+00:00`；artifactDigests 同 16 键结构（本地存在/缺失集合同上）。
- item 一致性：jobId 三件一致（`eval-20261012-054408-bbd40bb6`）；build/execution 字段一致；`sourceSha256=7475…c2e6` 与 metadata/manifest 一致；`DONE`/`PREPARATION_GAP`/`evaluation=null`/0 模型调用；cls `LOW_SIGNAL`。manifest 行同样 `Evidence="UNVERIFIED (not built, not run)"`、`JobId` 空（与 items 矛盾）。

---

## D2-280 — ruby-to-cpp / erb.rb

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-cpp/D2-280-ruby-erb.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-280.json`。
- 读取：全文成功，未截断（1/1/53 行）。
- build：`completed`/0，`durationMs=18`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/false；stderr 空/`sha256:e3b0…b855`/false。
- execution：`completed`/0，`durationMs=116`，`timedOut=false`；stdout/stderr 均空/0/`sha256:e3b0…b855`/false。
- observations：output `observed`/`[]`/`[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/[scope limitation]。`createdAt=2026-10-12T05:45:24Z`。
- collectorDiagnostics：`[]`。
- baseline/profile：`inputProfileHash=sha256:46ae0287738788b8e549a094ce5db0709114d08312a07be3e39704ce12eb84aa`；`artifactHash=sha256:8ef2030c5a3ecf6ff66ba0df2f5158551b156a0c06a27d1587459bd08210945f`；其余同构。`input_profile.json`：`profileId=D2-280`，`argv=[]`，dims `["output"]`。`metadata.json`：`sourceArtifact=source/erb.rb`，`sourceHash=sha256:2c1887b694a1d92634c3d089b8fd19dece88fe3c069b833893da62bf3ef40a07`，note 记 `cls=REVIEW_UNCERTAIN`。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/1/false/null；roles.source build `passed`、execution `completed`、frozenSourceObligations `UNVERIFIED`；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:45:51.736395+00:00`；artifactDigests 16 键。
- item 一致性：jobId `eval-20261012-054521-9ae80b6a` 三件一致；build/execution 一致；`sourceSha256=2c18…0a07` 一致；`DONE`/`PREPARATION_GAP`/`evaluation=null`/0 调用；cls `REVIEW_UNCERTAIN`。manifest 行 `Evidence` 未更新、`JobId` 空。

---

## D2-281 — ruby-to-cpp / ostruct.rb

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-cpp/D2-281-ruby-ostruct.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-281.json`。
- 读取：全文成功，未截断（1/1/53 行）。
- build：`completed`/0，`durationMs=35`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/false；stderr 空/`sha256:e3b0…b855`/false。
- execution：`completed`/0，`durationMs=66`，`timedOut=false`；stdout/stderr 空/0/`sha256:e3b0…b855`/false。
- observations：output `observed`/`[]`/`[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/[scope limitation]。`createdAt=2026-10-12T05:46:39Z`。
- collectorDiagnostics：`[]`。
- baseline/profile：`inputProfileHash=sha256:0076c536e95a2914b2efd34562458d4ef95ecb7ceb105d61c661c4ef23fa1562`；`artifactHash=sha256:de03eae6b19b7c41c4ca4523312c7de9b4584337b948b1df17de60deb5559e17`；其余同构。`input_profile.json`：`profileId=D2-281`，`argv=[]`，dims `["output"]`。`metadata.json`：`sourceArtifact=source/ostruct.rb`，`sourceHash=sha256:ae9090740e068cb4146cb81c92cf5d3f3adab7793d34be7d58d390d8af18275a`。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/1/false/null；roles.source build `passed`、execution `completed`、frozenSourceObligations `UNVERIFIED`；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:47:06.438483+00:00`；artifactDigests 16 键。
- item 一致性：jobId `eval-20261012-054636-272e9fdb` 三件一致；build/execution 一致；`sourceSha256=ae90…275a` 一致；`DONE`/`PREPARATION_GAP`/`evaluation=null`/0 调用。manifest 行 `Evidence` 未更新、`JobId` 空。

---

## D2-282 — ruby-to-cpp / tsort.rb

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-cpp/D2-282-ruby-tsort.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-282.json`。
- 读取：全文成功，未截断（1/1/53 行）。
- build：`completed`/0，`durationMs=34`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/false；stderr 空/`sha256:e3b0…b855`/false。
- execution：`completed`/0，`durationMs=116`，`timedOut=false`；stdout/stderr 空/0/`sha256:e3b0…b855`/false。
- observations：output `observed`/`[]`/`[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/[scope limitation]。`createdAt=2026-10-12T05:47:52Z`。
- collectorDiagnostics：`[]`。
- baseline/profile：`inputProfileHash=sha256:b81199057f542e7757328853aabac5190bf2cfcf83947541a7a29fff03ccdd2c`；`artifactHash=sha256:e9552a1b51c20356a2a53b2946661f6c0c2a45b902f8f7154ef683f231912bbd`；其余同构。`input_profile.json`：`profileId=D2-282`，`argv=[]`，dims `["output"]`。`metadata.json`：`sourceArtifact=source/tsort.rb`，`sourceHash=sha256:19857d9f0f45b7befbfd62e2e4cbbe26993fc3247192c49bebe3bba5f801b177`。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/1/false/null；roles.source build `passed`、execution `completed`、frozenSourceObligations `UNVERIFIED`；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:48:18.676540+00:00`；artifactDigests 16 键。
- item 一致性：jobId `eval-20261012-054749-05b85557` 三件一致；build/execution 一致；`sourceSha256=1985…b177` 一致；`DONE`/`PREPARATION_GAP`/`evaluation=null`/0 调用。manifest 行 `Evidence` 未更新、`JobId` 空。

---

## D2-283 — ruby-to-csharp / forwardable.rb

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-csharp/D2-283-ruby-forwardable.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-283.json`。
- 读取：全文成功，未截断（1/1/53 行）。
- build：`completed`/0，`durationMs=68`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/false；stderr 空/`sha256:e3b0…b855`/false。
- execution：`completed`/0，`durationMs=115`，`timedOut=false`；stdout/stderr 空/0/`sha256:e3b0…b855`/false。
- observations：output `observed`/`[]`/`[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/[scope limitation]。`createdAt=2026-10-12T05:49:12Z`。
- collectorDiagnostics：`[]`。
- baseline/profile：`inputProfileHash=sha256:6b605fc2bd4b6bf64bb86fa9cf7de21e5451afdcf09fa5b749823db83f29e5c4`；`artifactHash=sha256:7283f036fe82b18668e8c656dadee46fe2ee2fb608b28f04fa3f208b5d41abe0`；其余同构。`input_profile.json`：`profileId=D2-283`，`argv=[]`，dims `["output"]`。`metadata.json`：`sourceArtifact=source/forwardable.rb`，`sourceHash=sha256:21ce0348e2dd500c7fd71bf0bf10468a3eac5570a3e0128b38dcf6af2948e8cb`，note 明确 `L228 __FILE__ 是 _compile_method 的实参、不是 __FILE__==$0 守卫`。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/1/false/null；roles.source build `passed`、execution `completed`、frozenSourceObligations `UNVERIFIED`；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:49:38.575679+00:00`；artifactDigests 16 键。
- item 一致性：jobId `eval-20261012-054909-0a352413` 三件一致；build/execution 一致；`sourceSha256=21ce…e8cb` 一致；`DONE`/`PREPARATION_GAP`/`evaluation=null`/0 调用。manifest 行 `Evidence` 未更新、`JobId` 空。

---

## D2-284 — ruby-to-csharp / tempfile.rb

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-csharp/D2-284-ruby-tempfile.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-284.json`。
- 读取：全文成功，未截断（1/1/53 行）。
- build：`completed`/0，`durationMs=25`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/false；stderr 空/`sha256:e3b0…b855`/false。
- execution：`completed`/0，`durationMs=119`，`timedOut=false`；stdout/stderr 空/0/`sha256:e3b0…b855`/false。
- observations：output `observed`/`[]`/`[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/[scope limitation]。`createdAt=2026-10-12T05:50:28Z`。
- collectorDiagnostics：`[]`。
- baseline/profile：`inputProfileHash=sha256:f181dbcec514f6b770e69c8195980970f6e6583b3d9e5656f3255f34a1134f6f`；`artifactHash=sha256:1e6e23c6af0ac834eefe93b8512affad331eb70bf3281fd465c0624ea987b884`；其余同构。`input_profile.json`：`profileId=D2-284`，`argv=[]`，dims `["output"]`。`metadata.json`：`sourceArtifact=source/tempfile.rb`，`sourceHash=sha256:323d15cbf4d38c721b76f112adb25bf5c1d2f5a5a6e2d5ee6f370ba0a23b88d4`（note 记 require stdlib `delegate`+`tmpdir`）。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/1/false/null；roles.source build `passed`、execution `completed`、frozenSourceObligations `UNVERIFIED`；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:50:55.767177+00:00`；artifactDigests 16 键。
- item 一致性：jobId `eval-20261012-055025-5e5007b5` 三件一致；build/execution 一致；`sourceSha256=323d…88d4` 一致；`DONE`/`PREPARATION_GAP`/`evaluation=null`/0 调用。manifest 行 `Evidence` 未更新、`JobId` 空。

---

## D2-285 — ruby-to-csharp / enum_osx.rb（本组首个执行非 0 退出）

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-csharp/D2-285-ruby-enum_osx.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-285.json`。
- 读取：全文成功，未截断（1/1/52 行）。
- build：`completed`/0，`durationMs=33`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/false；stderr 空/`sha256:e3b0…b855`/false。
- execution：`status=completed`，`exitCode=1`，`durationMs=116`，`timedOut=false`；stdout `""`/0/`sha256:e3b0…b855`/false；stderr **实际内容** `"enum_osx.rb:6:in `<main>': uninitialized constant Msf (NameError)\n\nclass MetasploitModule < Msf::Post\n                         ^^^\n"`，`sizeBytes=131`，`digest=sha256:2f9ce1733f0cfbaedf3347f99965577fa56092a4815c04b53280b133359a0151`，`truncated=false`。
- observations：output `status=observed`、`events=[]`、`limitations=[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/[scope limitation]。**注意：本项 stderr 有 131 字节真实错误，而 `output.events` 仍为 `[]`** ⇒ `events=[]` 不能当“无输出/无问题”。`createdAt=2026-10-12T05:51:45Z`。
- collectorDiagnostics：`[]`（字面；对应 stderr 的真实运行时错误，不能据此说“采集无问题”）。
- baseline/profile：`inputProfileHash=sha256:034c68969029d5a48a032d589b9b7916e2ea0adc470997d88779d5d2fa2666e9`；`artifactHash=sha256:bfcb868d21f74a897479f23f5fb6b752315d07647c77b0fff28cc099f7d8c508`；其余同构。`input_profile.json`：`profileId=D2-285`，`argv=[]`，dims `["output"]`。`metadata.json`：`sourceArtifact=source/enum_osx.rb`，`sourceHash=sha256:9fc562a16cfea12f48dd24b167f32aae677bc369e6bbf304dc87b6ff4cba7620`，note 记 `cls=REVIEW_DEPENDENCY`、no entry guard。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/1/false/null；`roles.source={build:"passed", execution:"completed", frozenSourceObligations:"UNVERIFIED"}`（**`execution=completed` 只表示进程已结束，不代表成功；实际 exit=1**）；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:52:11.707959+00:00`；artifactDigests 16 键。
- item 一致性：jobId `eval-20261012-055142-80c0dc1f` 三件一致；item `execution=completed`、`executionExitCode=1` 与 evidence `exitCode=1` 一致；`diagnostics=["NameError: uninitialized constant Msf (L6, 'class MetasploitModule < Msf::Post')"]`；`sourceSha256=9fc5…7620` 一致；`disposition=SOURCE_DEPENDENCY_GAP`、`phase=CLOSED_SOURCE_DEPENDENCY_GAP`、`lifecycle=DONE`、`evaluation=null`、0 模型调用；`coverageGaps` 记 Metasploit 框架在快照外。manifest 行 `Evidence` 未更新、`JobId` 空。
- 原件 vs 报告口径：item 无 result.md 复核要求；本报告不改判。**本组唯一与 closure 摘要措辞易混之处**：closure/roles 的 `execution:"completed"` 与 exit 1 并存，不能读成执行成功。

---

## D2-286 — ruby-to-csharp / shellwords.rb

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-csharp/D2-286-ruby-shellwords.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-286.json`。
- 读取：全文成功，未截断（1/1/53 行）。
- build：`completed`/0，`durationMs=17`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/false；stderr 空/`sha256:e3b0…b855`/false。
- execution：`completed`/0，`durationMs=116`，`timedOut=false`；stdout/stderr 空/0/`sha256:e3b0…b855`/false。
- observations：output `observed`/`[]`/`[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/[scope limitation]。`createdAt=2026-10-12T05:53:04Z`。
- collectorDiagnostics：`[]`。
- baseline/profile：`inputProfileHash=sha256:98fa1591b74a91e1f5b46f86a90b97cb61fccc7b6797c70ed35ac99da16a28f8`；`artifactHash=sha256:245d3b6b614033e4a6db882fca1b42db77eb18bea5630b02d677fe26f522d180`；其余同构。`input_profile.json`：`profileId=D2-286`，`argv=[]`，dims `["output"]`。`metadata.json`：`sourceArtifact=source/shellwords.rb`，`sourceHash=sha256:83cc15ce74855f3f2f7c61a7eeec47304244fcd0178f1d31f363eb822012900e`。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/1/false/null；roles.source build `passed`、execution `completed`、frozenSourceObligations `UNVERIFIED`；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:53:35.624597+00:00`；artifactDigests 16 键。
- item 一致性：jobId `eval-20261012-055302-a2a4414e` 三件一致；build/execution 一致；`sourceSha256=83cc…900e` 一致；`DONE`/`PREPARATION_GAP`/`evaluation=null`/0 调用。manifest 行 `Evidence` 未更新、`JobId` 空。

---

## D2-287 — ruby-to-go / psexec.rb（含分类 1→2 重分类与删除）

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-go/D2-287-ruby-psexec.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-287.json`。
- 读取：全文成功，未截断（1/1/52 行）。
- build：`completed`/0，`durationMs=17`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/false；stderr 空/`sha256:e3b0…b855`/false。
- execution：`status=completed`，`exitCode=1`，`durationMs=116`，`timedOut=false`；stdout `""`/0/`sha256:e3b0…b855`/false；stderr **实际内容** `"psexec.rb:16:in `<main>': uninitialized constant Msf (NameError)\n\nclass MetasploitModule < Msf::Exploit::Remote\n                         ^^^\n"`，`sizeBytes=142`，`digest=sha256:6fe63d5cc50803342d5025b27470d2e9d3ec0b33b1e2e0e5258de2c2053a8404`，`truncated=false`。
- observations：output `observed`/`events=[]`/`limitations=[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/[scope limitation]。**stderr 142 字节真实错误而 `output.events=[]`**。`createdAt=2026-10-12T05:55:02Z`。
- collectorDiagnostics：`[]`。
- baseline/profile：`inputProfileHash=sha256:4f304b0c504015a94e59324087b6e3adf4815918a759fb0872536ad5aa3a9501`；`artifactHash=sha256:9f7b42e0716be54f600b2e9698c4c870e13bb76c7ea06586b8d09bc51ac0ac3e`；其余同构。`input_profile.json`：`profileId=D2-287`，`argv=[]`，dims `["output"]`。`metadata.json`：`sourceArtifact=source/psexec.rb`，`sourceHash=sha256:7aacaf9ead2c5e6d0aafd83f227dbc3ac927bbdabcdf76556e3c715d73742f09`；note 记“以 `--network-isolation-configured` 重分类，L52–L54 URL 是 Metasploit `References` 元数据（词法误报）”“see classification-2”。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/1/false/null；`roles.source={build:"passed", execution:"completed", frozenSourceObligations:"UNVERIFIED"}`（exit 1 并存，同上）；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:55:33.600861+00:00`；artifactDigests 16 键（键名 `classification.json` 对应远端最终分类）。
- item 一致性：jobId `eval-20261012-055500-d1e2f188` 三件一致；item `executionExitCode=1` 与 evidence 一致；`sourceSha256=7aac…2f09` 一致；`disposition=SOURCE_DEPENDENCY_GAP`、`phase=CLOSED_SOURCE_DEPENDENCY_GAP`、`lifecycle=DONE`、`evaluation=null`、0 模型调用；`classifier.requiresNetworkIsolation=true` 且 note 说明 `classification-2.json`、`classification-1.json` 已按纪律删除。**本地 `01-frozen/` 只有 `classification-2.json` 与 `classifier-input-2.json`（无 classification-1.json）**，与该删除说明一致（删除限制保留）。manifest 行 `Evidence` 未更新、`JobId` 空。

---

## D2-288 — ruby-to-go / enum_services.rb

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-go/D2-288-ruby-enum_services.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-288.json`。
- 读取：全文成功，未截断（1/1/52 行）。
- build：`completed`/0，`durationMs=16`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/false；stderr 空/`sha256:e3b0…b855`/false。
- execution：`status=completed`，`exitCode=1`，`durationMs=115`，`timedOut=false`；stdout `""`/0/`sha256:e3b0…b855`/false；stderr **实际内容** `"enum_services.rb:79:in `<module:Msf>': Post is not a class (TypeError)\nenum_services.rb:43: previous definition of Post was here\n\tfrom enum_services.rb:42:in `<main>'\n"`，`sizeBytes=167`，`digest=sha256:75e8cb0511ef39cceb3ba3eba2aa83dec6dca103bc8065b08427e3dd20215f3b`，`truncated=false`。
- observations：output `observed`/`events=[]`/`limitations=[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/[scope limitation]。**stderr 167 字节真实错误而 `output.events=[]`**。`createdAt=2026-10-12T05:56:43Z`。
- collectorDiagnostics：`[]`。
- baseline/profile：`inputProfileHash=sha256:c2d966cc75e84cccbc764a9fc0f63980ae4ecde946133244e3b26492309fe748`；`artifactHash=sha256:67c0cb6a69db7a58af1a21f0435687b56c102b520e2ba80146e0df5bede265c0`；其余同构。`input_profile.json`：`profileId=D2-288`，`argv=[]`，dims `["output"]`。`metadata.json`：`sourceArtifact=source/enum_services.rb`，`sourceHash=sha256:3ff4d191ff6251f73b245a3320d25c474b93c51a1be4d2b28d02c1318487c2a4`；note 记内联 Rex/Msf stub、`L135 class MetasploitModule < Msf::Post`、`L200 $0==__FILE__` 入口。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/1/false/null；`roles.source={build:"passed", execution:"completed", frozenSourceObligations:"UNVERIFIED"}`；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:57:10.662310+00:00`；artifactDigests 16 键。
- item 一致性：jobId `eval-20261012-055640-8864a840` 三件一致；item `executionExitCode=1` 与 evidence 一致；`diagnostics=["TypeError: Post is not a class (L79, inside module:Msf; previous definition of Post at L43)"]`；`sourceSha256=3ff4…c2a4` 一致；`SOURCE_DEPENDENCY_GAP`/`CLOSED_SOURCE_DEPENDENCY_GAP`/`DONE`/`evaluation=null`/0 调用。manifest 行 `Evidence` 未更新、`JobId` 空。
- 备注：metadata 称 L200 存在 `$0==__FILE__` 入口，但执行在加载期 L79 即 TypeError 失败；即“有入口”不代表可取得有效运行基线。

---

## D2-289 — ruby-to-go / enum_shares.rb

- 三件路径：`docs/dataset-2/dataset-2-copy/ruby-to-go/D2-289-ruby-enum_shares.rb/output/batch/04-evaluation/job-00-source-buildability/returned-evidence/evidence-source.json`、同目录 `closure.json`、`docs/dataset-2/dataset-2-copy/batch/items/D2-289.json`。
- 读取：全文成功，未截断（1/1/52 行）。
- build：`completed`/0，`durationMs=33`；stdout `"Syntax OK\n"`/10/`sha256:bbafef10…4a1b`/false；stderr 空/`sha256:e3b0…b855`/false。
- execution：`status=completed`，`exitCode=1`，`durationMs=116`，`timedOut=false`；stdout `""`/0/`sha256:e3b0…b855`/false；stderr **实际内容** `"enum_shares.rb:6:in `<main>': uninitialized constant Msf (NameError)\n\nclass MetasploitModule < Msf::Post\n                         ^^^\n"`，`sizeBytes=135`，`digest=sha256:64678eb91e8e260e0635e03ab3212bd1600e0fda2487f3df3f45c851d5d43582`，`truncated=false`。
- observations：output `observed`/`events=[]`/`limitations=[]`；filesystem、processes `not-applicable`/`[]`/`[]`；registry、network `not-applicable`/`[]`/[scope limitation]。**stderr 135 字节真实错误而 `output.events=[]`**。`createdAt=2026-10-12T05:58:01Z`。
- collectorDiagnostics：`[]`。
- baseline/profile：`inputProfileHash=sha256:3ba3134c151a1d022edfca4dc5034d1cc1dc625a7c3312dde2958c4c5bcb59c2`；`artifactHash=sha256:867322b4b097a8b3729350ac07f8d52098c4d1462945c5e15d0653cb8546a662`；其余同构。`input_profile.json`：`profileId=D2-289`，`argv=[]`，dims `["output"]`。`metadata.json`：`sourceArtifact=source/enum_shares.rb`，`sourceHash=sha256:74cfccf1759a33420d95ec4d93cd485538cc8e0a45840746a0844530edd4abbc`；note 记 `L6 class MetasploitModule < Msf::Post`。
- closure：`complete=true`/`cleanupConfirmed=true`/`issues=[]`；cleanupRecords.source `passed`/`READY`/1/false/null；`roles.source={build:"passed", execution:"completed", frozenSourceObligations:"UNVERIFIED"}`；`oracleStatus=UNVERIFIED`；`programOutputProvenance=UNVERIFIED`；`checkedAt=2026-10-12T05:58:28.960621+00:00`；artifactDigests 16 键。
- item 一致性：jobId `eval-20261012-055759-172c133c` 三件一致；item `executionExitCode=1` 与 evidence 一致；`diagnostics=["NameError: uninitialized constant Msf (L6, ...)"]`；`sourceSha256=74cf…abbc` 一致；`SOURCE_DEPENDENCY_GAP`/`CLOSED_SOURCE_DEPENDENCY_GAP`/`DONE`/`evaluation=null`/0 调用。manifest 行 `Evidence` 未更新、`JobId` 空。

---

## 横向汇总（只记录，不合成成功率）

| 项 | 方向/文件 | jobId | build | exec status/exit/timedOut | exec stdout | exec stderr | collectorDiag | closure | item |
|---|---|---|---|---|---|---|---|---|---|
| D2-278 | ruby-to-c / open3.rb | eval-…054247-f8b64c8b | completed/0 | completed/0/false | 空 0B | 空 0B | [] | complete/cleanup true，oracle & provenance UNVERIFIED | DONE / PREPARATION_GAP / eval null / 0 calls |
| D2-279 | ruby-to-cpp / delegate.rb | eval-…054408-bbd40bb6 | completed/0 | completed/0/false | 空 0B | 空 0B | [] | 同上 | DONE / PREPARATION_GAP / eval null / 0 calls |
| D2-280 | ruby-to-cpp / erb.rb | eval-…054521-9ae80b6a | completed/0 | completed/0/false | 空 0B | 空 0B | [] | 同上 | DONE / PREPARATION_GAP / eval null / 0 calls |
| D2-281 | ruby-to-cpp / ostruct.rb | eval-…054636-272e9fdb | completed/0 | completed/0/false | 空 0B | 空 0B | [] | 同上 | DONE / PREPARATION_GAP / eval null / 0 calls |
| D2-282 | ruby-to-cpp / tsort.rb | eval-…054749-05b85557 | completed/0 | completed/0/false | 空 0B | 空 0B | [] | 同上 | DONE / PREPARATION_GAP / eval null / 0 calls |
| D2-283 | ruby-to-csharp / forwardable.rb | eval-…054909-0a352413 | completed/0 | completed/0/false | 空 0B | 空 0B | [] | 同上 | DONE / PREPARATION_GAP / eval null / 0 calls |
| D2-284 | ruby-to-csharp / tempfile.rb | eval-…055025-5e5007b5 | completed/0 | completed/0/false | 空 0B | 空 0B | [] | 同上 | DONE / PREPARATION_GAP / eval null / 0 calls |
| D2-285 | ruby-to-csharp / enum_osx.rb | eval-…055142-80c0dc1f | completed/0 | completed/**1**/false | 空 0B | 131B NameError | [] | 同上 | DONE / SOURCE_DEPENDENCY_GAP / eval null / 0 calls |
| D2-286 | ruby-to-csharp / shellwords.rb | eval-…055302-a2a4414e | completed/0 | completed/0/false | 空 0B | 空 0B | [] | 同上 | DONE / PREPARATION_GAP / eval null / 0 calls |
| D2-287 | ruby-to-go / psexec.rb | eval-…055500-d1e2f188 | completed/0 | completed/**1**/false | 空 0B | 142B NameError | [] | 同上 | DONE / SOURCE_DEPENDENCY_GAP / eval null / 0 calls |
| D2-288 | ruby-to-go / enum_services.rb | eval-…055640-8864a840 | completed/0 | completed/**1**/false | 空 0B | 167B TypeError | [] | 同上 | DONE / SOURCE_DEPENDENCY_GAP / eval null / 0 calls |
| D2-289 | ruby-to-go / enum_shares.rb | eval-…055759-172c133c | completed/0 | completed/**1**/false | 空 0B | 135B NameError | [] | 同上 | DONE / SOURCE_DEPENDENCY_GAP / eval null / 0 calls |

- 12/12 的 build stdout 内容与摘要均为 `"Syntax OK\n"`（10B，`sha256:bbafef10…4a1b`，`truncated=false`）——同一内容产生同一 digest，属正常，非复制粘贴迹象。
- 12/12 的空值 digest 均为 `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`（0B）。
- 12/12 `snapshot=CC-Eval-Linux-8Lang-1.0.29`、`os=linux`、`arch=x64`、`artifactLanguage=ruby`、`selectedRunner=linux-vm-agent-x64`、`toolchainFingerprint={}`、`collectorVersion=agentVersion=1.0.0`；`input_profile.json` 均为 `argv=[]`、`observationPolicy.dimensions=["output"]`、`timeoutSeconds=60`；`metadata.networkBoundary="isolated VM"`。
- 12/12 `closure.complete=true`、`cleanupConfirmed=true`、`issues=[]`、`cleanupRecords.source={passed, READY, attempts:1, contaminated:false, reason:null}`、`oracleStatus=UNVERIFIED`、`programOutputProvenance=UNVERIFIED`、`roles.source.frozenSourceObligations=UNVERIFIED`。
- 12/12 `item.lifecycle=DONE`、`evaluation=null`、`usage={requests:0, modelCalls:0}`、classifier `admissionStatus=ALLOWED`、`blockingReason=null`、`classifier.version=2.4`、program hash `sha256:009a6f31…f3a4`；8 项 `PREPARATION_GAP`（278–284、286），4 项 `SOURCE_DEPENDENCY_GAP`（285、287、288、289）。

## 已读 / 未读 / 截断（补读完成声明）

- 强制三件（每项 evidence-source.json、closure.json、batch/items/<Id>.json）：**36/36 已亲读全文，36/36 成功，0 截断**。逐项件数：278=3、279=3、280=3、281=3、282=3、283=3、284=3、285=3、286=3、287=3、288=3、289=3。
- 因证据指针/占位异常而额外亲读（每项均存在）：`job-00-source-buildability/metadata.json` 与 `input_profile.json`，**24/24 已读，0 截断**。
- 另亲读 `ruby-to-c/D2-278-ruby-open3.rb/output/batch/result.md`（34 行）用于核对报告口径，1/1 成功。
- **本会话未读但确实存在**（为避免重复消费长报告而有意未读；非缺失）：每项的 `returned-evidence/controller.log`、`returned-evidence/evaluation_report.json`、`returned-evidence/evaluation_report.md`（12×3=36 件）；每项的 `04-evaluation/job-00-source-buildability/{batch-authorization.json, this-task-classification.json, source_preflight_manifest.json, job-id.txt}`；每项的 `01-frozen/{frozen-inputs.md, classification-*.json, classifier-input-*.json}`；除 D2-278 外其余 11 项的 `output/batch/result.md`。
- **缺失/未落地件（如实记录）**：
  - 12 项均无源文件与目标文件（item 目录下只有 `output/`，无 `source/`、无 `target*`）；
  - item `casePath` 所指 `docs/test/dataset-2/...` 在磁盘不存在（`glob docs/test/dataset-2/**/*.rb` 0 命中）；
  - manifest `Origin` 所指原始用例路径（`测试用例ruby\...` 等）在磁盘不存在（已用 `glob 测试用例ruby/**/open3.rb` 验证 0 命中，其余同类路径未逐个展开，属“未验证缺失”而非“确认存在”）；
  - closure `artifactDigests` 所列 `evidence/source-call.json`、`evidence/source-identity.json`、`evidence/source-request.json`、`evidence/source-response.body`、`evidence/source-response.json`、`evidence/source.json`、`lifecycle.jsonl`、`request.json`、`staging-manifest.json` 在各项本机目录中均**不存在**（远端侧摘要，不能据此断言其现状）；
  - D2-287 的 `01-frozen/classification-1.json` 已按纪律删除（本地仅 `classification-2.json`）。

## 新事实（本次亲读得到，不改变任何原 verdict）

1. `observations.output.events=[]` 在 12/12 全部为空，**包括 4 项 stderr 有 131–167 字节真实运行时错误的情况** ⇒ `events=[]` 不能代表“无输出”，也不能代表 stdout 为空；stdout 是否为空只能看 `execution.stdout`。
2. `collectorDiagnostics=[]` 在 12/12 全部为空，而其中 4 项实际发生加载期错误（NameError/TypeError）⇒ 该字段为空**不能**推断“采集无问题”或“运行干净”。
3. `closure.roles.source.execution="completed"` 在 exitCode=1 的 4 项（285/287/288/289）中照旧出现 ⇒ “completed” 仅表示进程已结束；`closure.complete=true`/`cleanupConfirmed=true` 也**不**等于功能验证（`oracleStatus`/`programOutputProvenance`/`frozenSourceObligations` 均为 `UNVERIFIED`）。
4. `observations.output.status="observed"` 在 12/12 出现，但 8 项 stdout+stderr 全空、exit 0（无入口/退化观察），4 项加载即失败 ⇒ “observed” 不等于取得有效行为基线；12 项均无有效运行基线、`evaluation=null`。
5. 12 项 `coverage.dimensions` 一致为 output=observed、filesystem/processes/registry/network=not-applicable；`input_profile.observationPolicy.dimensions=["output"]` 与之对应；registry/network 另带 limitation `"evidence dimension is outside the current release scope"`。
6. 三件契约链在 12/12 一致：`items` 的 `sourcePrecheck.jobId` = evidence `jobId` = closure `jobId`；`buildStatus/exitCode/execution/executionExitCode` 与 evidence 的 build/execution 字段逐一吻合；`items.sourceSha256` = `metadata.sourceHash` = manifest `Sha256`（大小写换算）。
7. **manifest 索引未随项更新**：D2-278…D2-289 的 manifest 行 `JobId` 列全为空、`Evidence` 列仍为 `UNVERIFIED (not built, not run)`，而 `items/<Id>.json` 已达到 `DONE` 并有 build/run 证据（8 项 PREPARATION_GAP、4 项 SOURCE_DEPENDENCY_GAP）。这是索引与 items 的直接矛盾（只记录，不据此改判）。
8. **manifest `Lines` 与项内报告不一致（已亲读一件为证）**：D2-278 manifest `Lines=718`，而 `output/batch/result.md` 正文称“764 行”并引用 `L764`；其余 11 项的行数声明未逐项核对（属未读项，不猜）。
9. D2-287 是唯一发生分类重做与原件删除的项：本地 `01-frozen/` 仅存 `classification-2.json` + `classifier-input-2.json`，item note 与 metadata note 均说明 `classification-1.json` 因词法误报（Metasploit References 中的 URL 字符串）重分类后被删除；item `classifier.requiresNetworkIsolation=true`。
10. D2-288 的 metadata 记录了 `L200 $0==__FILE__` 入口，但执行在加载期 L79 因内联 `Msf` stub 的 `Post` 重定义冲突 TypeError 失败 ⇒ 存在入口并不等于取得有效源运行基线。
11. 比对 `input_profile.json` 文件 digest（closure 内，如 D2-278 `sha256:e85d41…`）与本项 bundle `inputProfileHash`（`sha256:a7e757…`）**不是同一值**，二者不是同一算法/对象，不能相互代替；profile 归属只能靠内容（`profileId` 与项一致、`argv=[]` 与 `frozenArgv=[]` 一致）确认。

## 未做的事（边界）

- 未计算任何哈希（仓库内未落地新哈希；所引 digest 均为原件字段原文照录）。
- 未更改任何 verdict、disposition、lifecycle、closure 或原始证据文件；未改写 manifest。
- 未读取其他组（非 D2-278…289）及其他 harness 报告；未触碰 Controller/jobs、`.env`、权限。
- 未运行、未编译、未生成目标；未把源 build/run 记录当作转换完成。
