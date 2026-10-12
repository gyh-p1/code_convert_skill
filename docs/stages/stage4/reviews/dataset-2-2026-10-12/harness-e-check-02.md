# E后半补读验收（D2-290–D2-300，独立小范围）— harness-e-check-02

- 范围：**仅** D2-290 至 D2-300 共 11 项，实际目录以根 `docs/dataset-2/dataset-2-copy/manifest.csv` 为准。
- 工具：仅原生 `read`/`glob`/`grep`（本会话实际用 `read`+`glob`），报告 `write`。未用 shell、未算哈希、未改原 verdict、未跑样本/提交/辅助工具、未碰 Controller/jobs、`.env`/密钥、ACL/权限、其它组范围。
- 基线：工作区根 `E:\桌面文档\Agents System\code_convert`。单行读取上限已解除（1048576），旧 E 的“源证据/closure 长单行截断、不能信旧 COMPLETE”在本会话按真实 read 回执重核。
- 本报告为**新写**，不改动旧报告；旧结论不继承。

---

## 1. 读取总览

| 项 | 三件要求件 | 三件读取结果 | 截断 |
|---|---|---|---|
| D2-290…D2-300（11 项） | evidence-source.json / closure.json / batch/items/&lt;Id&gt;.json | 33/33 全部读回 | 0 件截断 |

- 11 项 × 3 件 = **33 件全部亲读**；`evidence-source.json`、`closure.json` 均为单行 JSON，`read` 返回 `total 1 lines`、无“omitted/truncated”标记；`items/<Id>.json` 为 52–53 行多行 JSON，完整返回。
- 结论：本范围 **COMPLETE（已读 33/33，未读/截断集合为空，缺件为空）**。
- 保留限制：本次只审本地副本，**不证明远端原件仍可取**；closure 所列摘要只支持“平台曾记录过该制品”，不恢复正文、不证明远端正文存在；源/目标文件可能已删，此限制不因本地有副本而解除。所有结论为静态审读事实，不含任何转换/编译/行为结论。

---

## 2. 逐项三件实录

路径根 = `E:\桌面文档\Agents System\code_convert\docs\dataset-2\dataset-2-copy`
（下称 `…`；`ES`=evidence-source.json，`CL`=closure.json，`IT`=batch/items/&lt;Id&gt;.json）

### D2-290 · ruby-to-go · chrome_cookies.rb
- ES：`…\ruby-to-go\D2-290-ruby-chrome_cookies.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 读取成功，1 行，完整无截断
- CL：同目录 `closure.json` — 读取成功，1 行，完整无截断
- IT：`…\batch\items\D2-290.json` — 读取成功，52 行，完整无截断
- `build`：status=completed，exitCode=0，durationMs=20；stdout `"Syntax OK\n"`（size=10，digest `sha256:bbafef10c22b9323fa5589564990f57fbf57f9a632381d5e765dc5a3b25b4a1b`，truncated=false）；stderr 空（size=0，digest `e3b0c442…b7852b855`，truncated=false）
- `execution`：status=completed，exitCode=**1**，durationMs=116，timedOut=false；stdout 空（size=0，digest `e3b0c442…`，truncated=false）；stderr=`chrome_cookies.rb:6:in \`<main>': uninitialized constant Msf (NameError)\n\nclass MetasploitModule < Msf::Post\n                         ^^^\n`（size=138，digest `sha256:9aea925db84e6e065a5ae2587caaab683ce09321ff18d31fee54ebeffde36dd3`，truncated=false）
- `output`：status=observed，events=[]，limitations=[]；filesystem/processes=not-applicable；registry/network=not-applicable 且 limitations=[“evidence dimension is outside the current release scope”]；coverage 五维同上
- `collectorDiagnostics`：`[]`（空——仅表示未记录诊断，**不能**证明采集器无失败）
- baseline/身份：bundleId `evb-source-eval-20261012-055913-2819c120`，jobId `eval-20261012-055913-2819c120`，runRole=source；bundle `inputProfileHash=sha256:3a523be3a7a31da6591650662cc8775e80030f830d2a3b9920d1eee225d7266b` 与 baselineReference `inputProfileHash` **一致**；baseline artifactHash `sha256:43124b88636e91a208496abd595cb3c58e9eab883cf21df3b48f1b8657ab8cff`，artifactLanguage=ruby，os=linux/arch=x64，snapshot=`CC-Eval-Linux-8Lang-1.0.29`，toolchainFingerprint={}（空），collectorVersion/agentVersion=1.0.0
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{status=passed,runnerStateAfter=READY,attempts=1,contaminated=false,reason=null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 共 16 键（本地现存 6：batch-authorization.json、evaluation_report.json、evaluation_report.md、input_profile.json、metadata.json、source_preflight_manifest.json；本地未见 10：classification.json、evidence/source-call.json、evidence/source-identity.json、evidence/source-request.json、evidence/source-response.body、evidence/source-response.json、evidence/source.json、lifecycle.jsonl、request.json、staging-manifest.json）；checkedAt=2026-10-12T05:59:47.220841+00:00
- IT：disposition=SOURCE_DEPENDENCY_GAP，phase=CLOSED_SOURCE_DEPENDENCY_GAP，lifecycle=DONE；sourceSha256 `881c804e…42a0859` 与 manifest `881C804E…42A0859` **一致**；jobId 与 ES/CL 一致；classifier 2.4 ALLOWED/cls=REVIEW_DEPENDENCY/blockingReason=null；sourcePrecheck buildStatus=completed/exitCode=0、execution=completed/executionExitCode=**1**、diagnostics=[NameError…Msf(L6)]；evaluation=null；targetBuild=not attempted；comparison=n/a；codeRevisions=0；selfRepairRounds=0；usage.modelCalls=0
- 一致性：IT 与 ES/CL 的 jobId、build、execution 退出码、诊断文本**一致**；仅源 build/run，**不构成转换完成**。

### D2-291 · ruby-to-go · observer.rb
- ES：`…\ruby-to-go\D2-291-ruby-observer.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 成功，1 行，完整
- CL：同目录 `closure.json` — 成功，1 行，完整
- IT：`…\batch\items\D2-291.json` — 成功，53 行，完整
- `build`：completed/0，durationMs=34；stdout `"Syntax OK\n"`（10，digest `bbafef10…`，truncated=false）；stderr 空
- `execution`：status=completed，exitCode=**0**，durationMs=115，timedOut=false；stdout 空（0，digest `e3b0c442…`，truncated=false）；stderr 空（0，digest `e3b0c442…`，truncated=false）
- `output`：observed，events=[]，limitations=[]；其余四维 not-applicable（registry/network 带同一条范围外 limitations）；coverage 同
- `collectorDiagnostics`：`[]`
- baseline/身份：bundleId `evb-source-eval-20261012-060050-c6153d88`，jobId 同；bundle inputProfileHash `sha256:43daef718d2220fabd88e9ba83a17dce072aea5bb9f85871c7ef7b361c2ff46e` 与 baseline **一致**；baseline artifactHash `sha256:68f1a73a1ae70a8174458b61cf568238c48cb768429fd10aea99998b69f8e63a`；snapshot `CC-Eval-Linux-8Lang-1.0.29`；toolchainFingerprint={}
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{passed,READY,1,false,null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 16 键（现存/未见同 D2-290 模式：6/10）；checkedAt=2026-10-12T06:01:24.152381+00:00
- IT：disposition=**PREPARATION_GAP**，phase=CLOSED_PREPARATION_GAP，lifecycle=DONE；sourceSha256 `05ff8053…c85d9fb` 与 manifest 一致；classifier 2.4 ALLOWED/cls=LOW_SIGNAL；sourcePrecheck execution=completed/executionExitCode=**0**、diagnostics=[]，note=“stdout and stderr both empty, exit 0: no entry guard => non-entry library module => degenerate observation”；usage.modelCalls=0
- 一致性：一致。`output.events=[]` 在本项对应**真实空 stdout**（size=0、空内容 digest），但这是逐项核对结果，不能由 events=[] 反推。

### D2-292 · ruby-to-powershell · cve_2021_40449.rb
- ES：`…\ruby-to-powershell\D2-292-ruby-cve_2021_40449.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 成功，1 行，完整
- CL：同目录 `closure.json` — 成功，1 行，完整
- IT：`…\batch\items\D2-292.json` — 成功，52 行，完整
- `build`：completed/0，durationMs=18；stdout `"Syntax OK\n"`（10，`bbafef10…`）；stderr 空
- `execution`：completed，exitCode=**1**，durationMs=116，timedOut=false；stdout 空；stderr=`cve_2021_40449.rb:6:in \`<main>': uninitialized constant Msf (NameError)\n\nclass MetasploitModule < Msf::Exploit::Local\n                         ^^^\n`（size=148，digest `sha256:3d3347152e9fee23634583d71af390bcdf0e839c7cf86f8bcd91b09466057b24`，truncated=false）
- `output`：observed，events=[]，limitations=[]；其余四维 not-applicable；`collectorDiagnostics`=[]
- baseline/身份：bundleId `evb-source-eval-20261012-060238-52b478f8`；bundle inputProfileHash `sha256:362837264280884ff105d997e6f6b917fbb773d3b7b26a909638de61a1e7d66a` 与 baseline **一致**；baseline artifactHash `sha256:f23fd25f96f640cf7dee4ce7674afcfc3dd7f58c6c2d225fa36563592b4e4914`；snapshot `CC-Eval-Linux-8Lang-1.0.29`
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{passed,READY,1,false,null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 16 键（6/10 同模式）；checkedAt=2026-10-12T06:03:07.845043+00:00
- IT：disposition=SOURCE_DEPENDENCY_GAP，phase=CLOSED_SOURCE_DEPENDENCY_GAP，DONE；sourceSha256 `db55b2ef…30723277` 与 manifest 一致；classifier 2.4 ALLOWED/cls=REVIEW_DEPENDENCY/**requiresNetworkIsolation=true**，note 记：classification-2.json（以 `--network-isolation-configured` 重分类），初次 classification-1.json 因词法误报（L58–61 References URL、L88 注释 URL）被判 BLOCKED/public_network_unverified，**classification-1.json 已按纪律移除**；sourcePrecheck executionExitCode=**1**，diagnostics=[NameError…Msf::Exploit::Local(L6)]；usage.modelCalls=0
- 一致性：IT/ES/CL 的 jobId、退出码、诊断一致；冻结目录现为 classification-2.json + classifier-input-2.json（无 classification-1.json），与 note 相符。

### D2-293 · ruby-to-powershell · process_herpaderping.rb
- ES：`…\ruby-to-powershell\D2-293-ruby-process_herpaderping.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 成功，1 行，完整
- CL：同目录 `closure.json` — 成功，1 行，完整
- IT：`…\batch\items\D2-293.json` — 成功，52 行，完整
- `build`：completed/0，durationMs=18；stdout `"Syntax OK\n"`（10，`bbafef10…`）；stderr 空
- `execution`：completed，exitCode=**1**，durationMs=269，timedOut=false；stdout 空；stderr=`<internal:/usr/lib/ruby/vendor_ruby/rubygems/core_ext/kernel_require.rb>:136:in \`require': cannot load such file -- metasploit/framework/compiler/windows (LoadError)\n\tfrom …\n\tfrom process_herpaderping.rb:6:in \`<main>'\n`（size=306，digest `sha256:9456f896f60afe8bd9c5c596f0f99d22df2825f309572ff7f631452a59fe9626`，truncated=false）
- `output`：observed，events=[]，limitations=[]；其余四维 not-applicable；`collectorDiagnostics`=[]
- baseline/身份：bundleId `evb-source-eval-20261012-060406-23765b7b`；inputProfileHash `sha256:0f87b0ddf0e8cbd1517b6c81813adeb07a5a9283126bad80eca73a2f2b9cc803` bundle 与 baseline 一致；baseline artifactHash `sha256:d06351a5007bafa01b0cca7ffbd9635a626ac068902230ea5e754825afcb8a9a`；snapshot `CC-Eval-Linux-8Lang-1.0.29`
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{passed,READY,1,false,null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 16 键（6/10 同模式）；checkedAt=2026-10-12T06:04:36.920597+00:00
- IT：disposition=SOURCE_DEPENDENCY_GAP，phase=CLOSED_SOURCE_DEPENDENCY_GAP，DONE；sourceSha256 `8d819cd0…b9fba3b` 与 manifest 一致；classifier 2.4 ALLOWED/REVIEW_DEPENDENCY/requiresNetworkIsolation=true，note 记 classification-2.json 重分类（初次因 L25/L43 描述 URL、L51/L52 References URL 词法误报 BLOCKED，classification-1.json 已移除）；sourcePrecheck executionExitCode=**1**，diagnostics=[LoadError metasploit/framework/compiler/windows(L6)]；usage.modelCalls=0
- 一致性：一致；冻结目录为 classification-2.json + classifier-input-2.json。

### D2-294 · ruby-to-powershell · docker_creds.rb
- ES：`…\ruby-to-powershell\D2-294-ruby-docker_creds.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 成功，1 行，完整
- CL：同目录 `closure.json` — 成功，1 行，完整
- IT：`…\batch\items\D2-294.json` — 成功，52 行，完整
- `build`：completed/0，durationMs=17；stdout `"Syntax OK\n"`（10，`bbafef10…`）；stderr 空
- `execution`：completed，exitCode=**1**，durationMs=116，timedOut=false；stdout 空；stderr=`docker_creds.rb:42:in \`<module:Msf>': Post is not a class (TypeError)\ndocker_creds.rb:13: previous definition of Post was here\n\tfrom docker_creds.rb:12:in \`<main>'\n`（size=164，digest `sha256:09f413f174dd0a9560074ae31fc0afdcf05c466bdcd8a159fcc31e7f8ed955f9`，truncated=false）
- `output`：observed，events=[]，limitations=[]；其余四维 not-applicable；`collectorDiagnostics`=[]
- baseline/身份：bundleId `evb-source-eval-20261012-060527-04840085`；inputProfileHash `sha256:4858659863bca870c13ab73b4c169427c6a5b4a512d3f51a479a09ff7571665b` 一致；baseline artifactHash `sha256:a73065142645da36821ce747e01976841272f57005fb5fc4cc002cdab3fecc8c`；snapshot `CC-Eval-Linux-8Lang-1.0.29`
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{passed,READY,1,false,null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 16 键（6/10 同模式）；checkedAt=2026-10-12T06:06:01.478088+00:00
- IT：disposition=SOURCE_DEPENDENCY_GAP，phase=CLOSED_SOURCE_DEPENDENCY_GAP，DONE；sourceSha256 `7c4a8345…b5e3a754` 与 manifest 一致；classifier 2.4 ALLOWED/REVIEW_DEPENDENCY，note=classification-1.json 首过 ALLOWED；sourcePrecheck executionExitCode=**1**，diagnostics=[TypeError Post is not a class(L42; previous L13)]；usage.modelCalls=0
- 一致性：一致。

### D2-295 · ruby-to-powershell · abbrev.rb
- ES：`…\ruby-to-powershell\D2-295-ruby-abbrev.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 成功，1 行，完整
- CL：同目录 `closure.json` — 成功，1 行，完整
- IT：`…\batch\items\D2-295.json` — 成功，53 行，完整
- `build`：completed/0，durationMs=18；stdout `"Syntax OK\n"`（10，`bbafef10…`）；stderr 空
- `execution`：completed，exitCode=**0**，durationMs=117，timedOut=false；stdout 空（0，`e3b0c442…`）；stderr 空（0，`e3b0c442…`）
- `output`：observed，events=[]，limitations=[]；其余四维 not-applicable；`collectorDiagnostics`=[]
- baseline/身份：bundleId `evb-source-eval-20261012-060708-c93e8a19`；inputProfileHash `sha256:189bae2fd64dd6784ebc7d0f392094deac71a96fe0db56c8e5ced2873cc906dc` 一致；baseline artifactHash `sha256:3f50e46f0ab27dfff084c1cd933af894f99257086683057c6b88ce5806a5915b`；snapshot `CC-Eval-Linux-8Lang-1.0.29`
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{passed,READY,1,false,null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 16 键（6/10 同模式）；checkedAt=2026-10-12T06:07:38.605159+00:00
- IT：disposition=**PREPARATION_GAP**，phase=CLOSED_PREPARATION_GAP，DONE；sourceSha256 `c0a070cc…e66ecacb` 与 manifest 一致；classifier 2.4 ALLOWED/LOW_SIGNAL；sourcePrecheck execution=completed/executionExitCode=**0**、diagnostics=[]，note 同“无 entry guard => 退化观察”；usage.modelCalls=0
- 一致性：一致；真实 stdout/stderr 均空，非由 events=[] 推断。

### D2-296 · ruby-to-powershell · singleton.rb
- ES：`…\ruby-to-powershell\D2-296-ruby-singleton.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 成功，1 行，完整
- CL：同目录 `closure.json` — 成功，1 行，完整
- IT：`…\batch\items\D2-296.json` — 成功，53 行，完整
- `build`：completed/0，durationMs=18；stdout `"Syntax OK\n"`（10，`bbafef10…`）；stderr 空
- `execution`：completed，exitCode=**0**，durationMs=116，timedOut=false；stdout 空；stderr 空
- `output`：observed，events=[]，limitations=[]；其余四维 not-applicable；`collectorDiagnostics`=[]
- baseline/身份：bundleId `evb-source-eval-20261012-060825-115f4738`；inputProfileHash `sha256:9c03063264f702f64559d40f45f3023cc244c84652dafc86560e1467f50dec1e` 一致；baseline artifactHash `sha256:71f3373cb92e83a10040cefff4960a5a731fc08c41e2c1bf7fc7f7cf591a3bb1`；snapshot `CC-Eval-Linux-8Lang-1.0.29`
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{passed,READY,1,false,null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 16 键（6/10 同模式）；checkedAt=2026-10-12T06:08:55.109920+00:00
- IT：disposition=**PREPARATION_GAP**，phase=CLOSED_PREPARATION_GAP，DONE；sourceSha256 `51f22a15…a03a2fcb1` 与 manifest 一致；classifier 2.4 ALLOWED/cls=**REVIEW_UNCERTAIN**；sourcePrecheck executionExitCode=**0**、diagnostics=[]，note 同退化观察；usage.modelCalls=0
- 一致性：一致。

### D2-297 · ruby-to-python · base64.rb
- ES：`…\ruby-to-python\D2-297-ruby-base64.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 成功，1 行，完整
- CL：同目录 `closure.json` — 成功，1 行，完整
- IT：`…\batch\items\D2-297.json` — 成功，53 行，完整
- `build`：completed/0，durationMs=18；stdout `"Syntax OK\n"`（10，`bbafef10…`）；stderr 空
- `execution`：completed，exitCode=**0**，durationMs=138，timedOut=false；stdout 空；stderr 空
- `output`：observed，events=[]，limitations=[]；其余四维 not-applicable；`collectorDiagnostics`=[]
- baseline/身份：bundleId `evb-source-eval-20261012-060948-53dbabf8`；inputProfileHash `sha256:1c5ebc1c9327d68bc665c0b2f3172957adb66ba268ad9a4ec1c1ba6c7b36bde0` 一致；baseline artifactHash `sha256:6ba9472f2b9d79a02a79d4eb5162b5c7ac81a1fa99f90b274dee20c15256aaf0`；snapshot `CC-Eval-Linux-8Lang-1.0.29`
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{passed,READY,1,false,null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 16 键（6/10 同模式）；checkedAt=2026-10-12T06:10:17.858436+00:00
- IT：disposition=**PREPARATION_GAP**，phase=CLOSED_PREPARATION_GAP，DONE；sourceSha256 `3bb017d2…61d7f7` 与 manifest 一致；classifier 2.4 ALLOWED/LOW_SIGNAL；sourcePrecheck executionExitCode=**0**、diagnostics=[]，note 同退化观察；usage.modelCalls=0
- 一致性：一致。

### D2-298 · ruby-to-python · enum_av.rb
- ES：`…\ruby-to-python\D2-298-ruby-enum_av.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 成功，1 行，完整
- CL：同目录 `closure.json` — 成功，1 行，完整
- IT：`…\batch\items\D2-298.json` — 成功，52 行，完整
- `build`：completed/0，durationMs=17；stdout `"Syntax OK\n"`（10，`bbafef10…`）；stderr 空
- `execution`：completed，exitCode=**1**，durationMs=115，timedOut=false；stdout 空；stderr=`enum_av.rb:6:in \`<main>': uninitialized constant Msf (NameError)\n\nclass MetasploitModule < Msf::Post\n                         ^^^\n`（size=131，digest `sha256:c89474d3171427b7ab2df0aab9754380bd78915cb12ce298fc8bec5e0b32fbd8`，truncated=false）
- `output`：observed，events=[]，limitations=[]；其余四维 not-applicable；`collectorDiagnostics`=[]
- baseline/身份：bundleId `evb-source-eval-20261012-061116-b7a4aa6d`；inputProfileHash `sha256:5dff715546dac63195f7a9e54c597496594c3445dc265ebf694c53630fd954ea` 一致；baseline artifactHash `sha256:cd7347b0d66783e37eedf81359d5c27090e3c01c91e784d1221b0cdc9d24f971`；snapshot `CC-Eval-Linux-8Lang-1.0.29`
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{passed,READY,1,false,null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 16 键（6/10 同模式）；checkedAt=2026-10-12T06:11:46.403918+00:00
- IT：disposition=SOURCE_DEPENDENCY_GAP，phase=CLOSED_SOURCE_DEPENDENCY_GAP，DONE；sourceSha256 `38fb7944…840115b4` 与 manifest 一致；classifier 2.4 ALLOWED/REVIEW_DEPENDENCY/requiresNetworkIsolation=true，note 记 classification-2.json 重分类（初次因 `'windows.antivirus'` 字面量（L48 report_note 类型串）词法误报 BLOCKED，classification-1.json 已移除）；sourcePrecheck executionExitCode=**1**，diagnostics=[NameError…Msf::Post(L6)]；usage.modelCalls=0
- 一致性：一致；冻结目录为 classification-2.json + classifier-input-2.json。

### D2-299 · ruby-to-python · windows_defender_exe.rb
- ES：`…\ruby-to-python\D2-299-ruby-windows_defender_exe.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 成功，1 行，完整
- CL：同目录 `closure.json` — 成功，1 行，完整
- IT：`…\batch\items\D2-299.json` — 成功，52 行，完整
- `build`：completed/0，durationMs=18；stdout `"Syntax OK\n"`（10，`bbafef10…`）；stderr 空
- `execution`：completed，exitCode=**1**，durationMs=167，timedOut=false；stdout 空；stderr=`<internal:/usr/lib/ruby/vendor_ruby/rubygems/core_ext/kernel_require.rb>:136:in \`require': cannot load such file -- metasploit/framework/compiler/windows (LoadError)\n\tfrom …\n\tfrom windows_defender_exe.rb:6:in \`<main>'\n`（size=306，digest `sha256:7e23dc7a88d8eb0a25295d9b8c5adf38b22981d9713f99d6067b35118f899545`，truncated=false）
- `output`：observed，events=[]，limitations=[]；其余四维 not-applicable；`collectorDiagnostics`=[]
- baseline/身份：bundleId `evb-source-eval-20261012-061237-36d33e6a`；inputProfileHash `sha256:085ff85d5c5b021e02037c2ce5b2e95bb64a21b092a19f6f250ad93df75590be` 一致；baseline artifactHash `sha256:b285b824b1b5547db65bf1001cc0beadbe6378b733534a78a2e235ce5ce8826b`；snapshot `CC-Eval-Linux-8Lang-1.0.29`
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{passed,READY,1,false,null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 16 键（6/10 同模式）；checkedAt=2026-10-12T06:13:07.433893+00:00
- IT：disposition=SOURCE_DEPENDENCY_GAP，phase=CLOSED_SOURCE_DEPENDENCY_GAP，DONE；sourceSha256 `7a6062ee…d26924e` 与 manifest 一致；classifier 2.4 ALLOWED/REVIEW_DEPENDENCY，note=classification-1.json 首过；sourcePrecheck executionExitCode=**1**，diagnostics=[LoadError metasploit/framework/compiler/windows(L6)]；usage.modelCalls=0
- 一致性：一致。

### D2-300 · ruby-to-python · credential_collector.rb
- ES：`…\ruby-to-python\D2-300-ruby-credential_collector.rb\output\batch\04-evaluation\job-00-source-buildability\returned-evidence\evidence-source.json` — 成功，1 行，完整
- CL：同目录 `closure.json` — 成功，1 行，完整
- IT：`…\batch\items\D2-300.json` — 成功，52 行，完整
- `build`：completed/0，durationMs=34；stdout `"Syntax OK\n"`（10，`bbafef10…`）；stderr 空
- `execution`：completed，exitCode=**1**，durationMs=116，timedOut=false；stdout 空；stderr=`credential_collector.rb:6:in \`<main>': uninitialized constant Msf (NameError)\n\nclass MetasploitModule < Msf::Post\n                         ^^^\n`（size=144，digest `sha256:3f14732bb88b8d75baf0b9c79d47d07d3a56a97d0172e6cc3c2e48b4b8e85478`，truncated=false）
- `output`：observed，events=[]，limitations=[]；其余四维 not-applicable；`collectorDiagnostics`=[]
- baseline/身份：bundleId `evb-source-eval-20261012-061356-ace57ce5`；inputProfileHash `sha256:933c15b2f75aca14993e1ac66aaf76769861d28335002e25a68e1a33d8471091` 一致；baseline artifactHash `sha256:a9bb348a7d5385fecb09a4ca9771f1f8a475898af33123bdfa20b3d4edb72a5c`；snapshot `CC-Eval-Linux-8Lang-1.0.29`
- CL：complete=true，cleanupConfirmed=true，issues=[]；cleanupRecords.source{passed,READY,1,false,null}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED；artifactDigests 16 键（6/10 同模式）；checkedAt=2026-10-12T06:14:26.436546+00:00
- IT：disposition=SOURCE_DEPENDENCY_GAP，phase=CLOSED_SOURCE_DEPENDENCY_GAP，DONE；sourceSha256 `e838f090…2a11bd0` 与 manifest 一致；classifier 2.4 ALLOWED/REVIEW_DEPENDENCY，note=classification-1.json 首过；sourcePrecheck executionExitCode=**1**，diagnostics=[NameError…Msf::Post(L6)]；usage.modelCalls=0
- 一致性：一致。旧 E 争议的“D2-300 closure 已读/未读并存”在本会话以真实 read 回执消除：closure.json 单行完整读回。

---

## 3. 汇总

- 读取：33/33 件成功、0 截断、0 必备缺件。
- 每项只有 **1 个 job**：`job-00-source-buildability`（无 dual-build、无 generation、无 target、无 comparison）。
- disposition 分布：SOURCE_DEPENDENCY_GAP = 7（D2-290/292/293/294/298/299/300）；PREPARATION_GAP = 4（D2-291/295/296/297）；均 lifecycle=DONE、phase=CLOSED_*。
- build：11/11 status=completed、exitCode=0、stdout 均为 `"Syntax OK\n"`（size=10，同一 digest `bbafef10…`）、stderr 空、truncated=false。
- execution：exitCode=0 共 4（291/295/296/297，stdout+stderr 全空）；exitCode=1 共 7（290/292/293/294/298/299/300，stdout 空、stderr 非空且逐项 digest 不同）；无 timedOut=true。
- output：11/11 status=observed、events=[]、limitations=[]；filesystem/processes 全 not-applicable；registry/network 全 not-applicable（带同一条“outside the current release scope”限制）；coverage 与 observations 一致。
- collectorDiagnostics：11/11 = `[]`。
- 身份关联：11/11 的 bundle `inputProfileHash` 与 baselineReference `inputProfileHash` 完全一致；baseline artifactHash 逐项唯一；runtime 固定 linux/x64/`CC-Eval-Linux-8Lang-1.0.29`/`linux-vm-agent-x64`；collectorVersion=agentVersion=1.0.0。
- closure：11/11 complete=true、cleanupConfirmed=true、issues=[]、cleanupRecords.source{passed,READY,attempts=1,contaminated=false}；roles.source{build=passed,execution=completed,frozenSourceObligations=UNVERIFIED}；oracleStatus=UNVERIFIED；programOutputProvenance=UNVERIFIED。
- item 记录：11/11 的 jobId、build、execution 退出码、诊断文本、sourceSha256（对 manifest）与原件**相互一致**。
- 平台 matched/semantic_pass：**本 11 项均无**（evaluation=null、targetBuild=not attempted、comparison=n/a），不得计入任何真实冻结范围的 matched/semantic_pass 统计。
- 转换完成度：**11/11 未转换**（只有源 build + 一次源 run），源 build/run 通过**不等于**转换完成。

---

## 4. 新事实与发现（不改原 verdict）

1. **closure 的 `roles.source.execution="completed"` 不等于成功**：D2-290/292/293/294/298/299/300 实际 `execution.exitCode=1`。`completed` 只表示进程跑完（未超时）；成功与否须看 `execution.exitCode` 与 items `executionExitCode`。读 closure 摘要易被误读。
2. **closure 的 artifactDigests 逐项列出 16 个制品摘要，但本地仅有 6 个对应文件**：本地现存 batch-authorization.json、evaluation_report.json、evaluation_report.md、input_profile.json、metadata.json、source_preflight_manifest.json；本地**未见** classification.json、evidence/source-call.json、evidence/source-identity.json、evidence/source-request.json、evidence/source-response.body、evidence/source-response.json、evidence/source.json、lifecycle.jsonl、request.json、staging-manifest.json（11 项同模式）。这些“声明摘要”不证明远端原件仍可取，也不恢复正文。
3. **closure 的 artifactDigests 未涵盖本次主证据 `returned-evidence/evidence-source.json` 与 `closure.json` 自身**（其列的是 `evidence/source.json` 等另一路径）；两处 digest 不可互证。本次按只读原文记录，未算哈希。
4. **空 `collectorDiagnostics` 只表示“未记录诊断”**：11/11 均为 `[]`，不能据此推断采集器无失败或采集完整。
5. **`output.events=[]` 与真实 stdout 分开核**：本 11 项逐项核了 stdout 的 sizeBytes/digest/truncated，确认 11/11 的 stdout 真实为空（size=0、空内容 digest `e3b0c442…`）；stdout 无内容，实际失败信息在 7 项的 stderr 中。不能由 events=[] 直接断言 stdout 空。
6. **PREPARATION_GAP（4 项）与策略分支口径**：D2-291/295/296/297 源可 build、run 退出 0 但无任何可观察行为（无 entry guard 的库模块），items 自述“需要合法中性入口或逐项 LIB_UNOBSERVABLE_COMPILE_ONLY 理由”，但实际以 PREPARATION_GAP 关闭、`usage.modelCalls=0`（未生成目标）。按项目口径，LIB_UNOBSERVABLE_COMPILE_ONLY 应在源构建通过后**继续转换**并做目标语法/编译验证；这 4 项停在源预检，属“未转换”，其 DONE 是生命周期终态而非转换完成。此处仅记录事实，不改原 verdict。
7. **重分类历史（3 项）**：D2-292/293/298 初次 classification-1 因词法误报（URL 串/`'windows.antivirus'` 字面量）被判 BLOCKED/public_network_unverified，随后以 `--network-isolation-configured` 重分类为 REVIEW_DEPENDENCY（requiresNetworkIsolation=true），并**移除 classification-1.json**（冻结目录现为 classification-2.json + classifier-input-2.json，佐证一致）。属已记录的口径处理，非缺档。
8. **路径口径**：items `casePath` 写作 `docs/test/dataset-2/…`，而实际证据目录为 `docs/dataset-2/dataset-2-copy/…`；manifest `Origin` 又记为 `测试用例ruby\…` 源路径。三者是同一逻辑项的不同路径口径，按用户指定“实际目录按根 docs/dataset-2/dataset-2-copy/manifest.csv”核读。
9. **cleanup/隔离**：11/11 `runnerStateAfter=READY`、`cleanupConfirmed=true`、`contaminated=false`。按项目口径，`READY`/本地清理确认**不等于**网络已隔离；本次不据此推断隔离。
10. **baseline `toolchainFingerprint={}` 为空**：11/11 baseline 的工具链指纹字段为空对象，运行时仅由 snapshot 名标识。
11. **stdout 内容为 rubric 校验串**：全部 build stdout 为 `"Syntax OK\n"`（各语言中仅 Ruby 用例；这正是 `ruby -c` 的产物），其 digest 在 11 项完全相同。

---

## 5. 已读 / 未读 / 缺件清单（分开如实列）

- **要求件已读**：33/33（D2-290…D2-300 × evidence-source.json、closure.json、batch/items/&lt;Id&gt;.json）。
- **实际未读（要求件）**：无。
- **实际截断（要求件）**：无。
- **缺失（要求件）**：无。

- **现存但未读（本地其它件）**：每项现存 15 件（3 件 01-frozen + 1 件 batch/result.md + 6 件 job 目录 + 5 件 returned-evidence），11 项共 **165 件现存**；本次已读 33 件，**现存未读 132 件**，逐项未读包括：`01-frozen/frozen-inputs.md`、`01-frozen/classification-{1|2}.json`、`01-frozen/classifier-input-{1|2}.json`、`job-00-source-buildability/this-task-classification.json`、`…/metadata.json`、`…/input_profile.json`、`…/source_preflight_manifest.json`、`…/batch-authorization.json`、`…/job-id.txt`、`returned-evidence/evaluation_report.md`、`returned-evidence/evaluation_report.json`、`returned-evidence/controller.log`、`output/batch/result.md`。这些属现存未读，不是缺件。
- **closure 声明但本地未见的制品（10 类/项，11 项同）**：classification.json、evidence/source-call.json、evidence/source-identity.json、evidence/source-request.json、evidence/source-response.body、evidence/source-response.json、evidence/source.json、lifecycle.jsonl、request.json、staging-manifest.json。按项目口径，closure 摘要只支持平台记录，**不证明远端原件仍可取**；本报告不将其计入“要求件缺件”，但从本地取证完整性看属“声明未落地”。
- 未读判定说明：本次未发现占位/版本/回执异常到必须逐项再读 `result.md`/`metadata.json` 才能定性的程度；逐项三件的退出码、jobId、sourceSha256、诊断文本已能互相印证。上述未读保持 PENDING，未以“打开过文件”充抵全文。

---

## 6. 结论

- 本独立补读范围（D2-290–D2-300，11 项 33 件主证据）**全部亲读、完整、无截断、无缺件**，满足“11 项 33 件全读才 COMPLETE”的判据 → **COMPLETE（限此 11 项 33 件）**。
- 同时不解除的边界：其它范围未碰；远端原件可取性未证；未算哈希、未改原 verdict；11 项均为**未转换**的源侧预检终态；不得把本范围的源 build/run 记作转换完成，也不得产生任何 matched/semantic_pass 计数。
