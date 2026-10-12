# harness-A 覆盖索引（D2-007 … D2-080）

> 状态：**IN_PROGRESS（未全部 COMPLETE）**。范围：`../../../manifest.csv` 中 Id `D2-007`…`D2-080` 的**全部现存项**。
> 计数：编号区间 74 个，`D2-026` 已移除（[README §5.2](../../../README.md)），**现存 73 项**。
> 方法/红线：纯静态只读；原生 read/glob/grep；本机 pwsh 因沙箱 ACL 失败不可用；未写/运行任何辅助脚本；不运行/编译/提交；不访问 `D:/CodeConvertRemote/Stack`；不读 `.env`/密钥；不改原始证据。读取由 harness-A 会话内的逐项读者（同模型、同只读工具约束）执行，逐件状态见各 case 文件。
> 工具限制（全体平台回传件）：`evidence-*.json`/`comparison.json`/`evaluation_report.json`/`closure.json`/`controller-health*.json` 多为**单行 JSON**，read/grep 在约 2000 字符处截断且无字节偏移读取 ⇒ 尾部不可补读，逐件标 `read(截断>2000)`；**不为通过而据不可读尾部推断**。

## 项 → 实际目录 / 件数 / 读取状态

目录基准：`../../<direction>/<case>/`。件数 = 该项目录下现存文件总数（读者逐件清单）；状态 `READ` = 全部现存件已读（含标注的截断件）；`dir-empty` = 目录存在但 0 文件；`dir-missing` = 目录未发现。

| Id | Kind | Direction | 实际目录 | 件数 | 状态 |
|---|---|---|---|---|---|
| D2-007 | REUSE | cpp-to-csharp | `handoff-2026-10-02-d08-dir-sample-discovery-cpp` | 45 | READ（6 件截断；02/03 目录空） |
| D2-008 | REUSE | cpp-to-csharp | `handoff-2026-10-02-d08-elevation-branch-report-cpp` | 0 | dir-empty |
| D2-009 | REUSE | cpp-to-csharp | `handoff-2026-10-02-d08-fake-cred-summary-cpp` | 0 | dir-empty |
| D2-010 | REUSE | cpp-to-csharp | `handoff-2026-10-02-d08-manifest-upload-cpp` | 0 | dir-empty |
| D2-011 | REUSE | cpp-to-csharp | `handoff-2026-10-02-d08-startup-marker-write-cpp` | 0 | dir-empty |
| D2-012 | REUSE | cpp-to-csharp | `handoff-2026-10-02-d08-xor-decode-demo-cpp` | 0 | dir-empty |
| D2-013 | REUSE | cpp-to-go | `handoff-2026-10-02-d10-inbox-request-gate-cpp` | 53 | READ（12 截断） |
| D2-014 | REUSE | cpp-to-go | `handoff-2026-10-02-d10-shell-output-capture-cpp` | 31 | READ |
| D2-015 | REUSE | cpp-to-go | `imported-2026-10-04-c11-token-privilege-inspector` | 31 | READ（6 截断） |
| D2-016 | REUSE | cpp-to-powershell | `handoff-2026-10-02-d12-loopback-send-cpp` | 33 | READ（6 截断） |
| D2-017 | REUSE | cpp-to-powershell | `handoff-2026-10-02-d12-tree-inventory-report-cpp` | 1 | READ |
| D2-018 | REUSE | cpp-to-python | `handoff-2026-10-02-d09-multi-command-runner-cpp` | 1 | READ |
| D2-019 | REUSE | cpp-to-python | `handoff-2026-10-02-d09-startup-registry-cycle-cpp` | 29 | READ（5 截断） |
| D2-020 | REUSE | cpp-to-ruby | `handoff-2026-10-02-d11-kv-request-audit-cpp` | 19 | READ（6 截断） |
| D2-021 | REUSE | cpp-to-ruby | `handoff-2026-10-02-d11-loopback-ack-probe-cpp` | 20 | READ（6 截断） |
| D2-022 | REUSE | csharp-to-python | `handoff-2026-10-02-d15-dump-cs` | 41 | READ |
| D2-023 | REUSE | csharp-to-ruby | `handoff-2026-10-02-d17-describe-cs` | 33 | READ |
| D2-024 | REUSE | c-to-cpp | `c01-linux-win-network` | 46 | READ（17 截断） |
| D2-025 | REUSE | c-to-cpp | `chain-reactor-network-linux` | 49 | READ（13 截断） |
| D2-026 | — | — | **已移除（无源，不在 manifest）** | — | N/A |
| D2-027 | REUSE | c-to-cpp | `pwd-fs-posix-to-win` | 28 | READ（3 截断） |
| D2-028 | REUSE | c-to-cpp | `realpath-fs-posix-to-win` | 9 | READ（1 截断） |
| D2-029 | REUSE | c-to-cpp | `stest-fs-posix-to-win` | 108 | READ（37 截断） |
| D2-030 | REUSE(manifest)/NEW(item) | c-to-csharp | `handoff-2026-10-02-d02-apisetmap-c` | 0 | dir-empty 或 dir-missing（声明冲突，见 findings） |
| D2-031 | REUSE | c-to-python | `handoff-2026-10-02-d03-environment-c` | 41 | READ |
| D2-032 | REUSE | c-to-ruby | `handoff-2026-10-02-d05-linux-c` | 34 | READ |
| D2-033 | REUSE | go-to-c | `handoff-2026-10-02-d25-admin-presence-probe-go` | 19 | READ |
| D2-034 | REUSE | go-to-c | `handoff-2026-10-02-d25-b64-hash-transform-go` | 19 | READ |
| D2-035 | REUSE | go-to-c | `handoff-2026-10-02-d25-cred-mask-fixture-go` | 41 | READ |
| D2-036 | REUSE | go-to-c | `handoff-2026-10-02-d25-host-net-enum-go` | 41 | READ |
| D2-037 | REUSE | go-to-cpp | `handoff-2026-10-02-d26-chunk-upload-rehash-go` | 40 | READ |
| D2-038 | REUSE | go-to-cpp | `handoff-2026-10-02-d26-cred-redact-quality-go` | 41 | READ |
| D2-039 | REUSE | go-to-cpp | `handoff-2026-10-02-d26-ext-loopback-inventory-go` | 41 | READ |
| D2-040 | REUSE | go-to-cpp | `handoff-2026-10-02-d26-gzip-xor-replay-go` | 41 | READ |
| D2-041 | REUSE | go-to-cpp | `handoff-2026-10-02-d26-token-priv-probe-go` | 41 | READ |
| D2-042 | REUSE | go-to-cpp | `imported-2026-10-04-c01-process-pipeline-capture` | 41 | READ |
| D2-043 | REUSE | go-to-cpp | `imported-2026-10-04-c05-tcp-loopback-scanner` | 41 | READ（1 件 missing：observed-source-stderr.txt） |
| D2-044 | REUSE | go-to-cpp | `imported-2026-10-04-c06-smb-loopback-prober` | 41 | READ |
| D2-045 | REUSE | go-to-cpp | `imported-2026-10-04-c07-tree-walk-zip-collector` | 41 | READ（1 件 missing：attempt-1-truncated.raw.json） |
| D2-046 | REUSE | go-to-cpp | `imported-2026-10-04-c08-loopback-c2-controller` | 41 | READ |
| D2-047 | REUSE | go-to-cpp | `imported-2026-10-04-c09-chunked-http-exfiltrator` | 41 | READ |
| D2-048 | REUSE | go-to-csharp | `handoff-2026-10-02-d27-autorun-manifest-write-go` | 待核 | **PENDING**（读者进行中） |
| D2-049 | REUSE | go-to-csharp | `handoff-2026-10-02-d27-iface-env-inventory-go` | 待核 | PENDING |
| D2-050 | REUSE | go-to-csharp | `handoff-2026-10-02-d27-tcp-port-scanner-go` | 待核 | PENDING |
| D2-051 | REUSE | go-to-csharp | `handoff-2026-10-02-d27-workspace-env-discovery-go` | 待核 | PENDING |
| D2-052 | REUSE | go-to-powershell | `handoff-2026-10-02-d30-inbox-kv-parse-go` | 待核 | PENDING |
| D2-053 | REUSE | go-to-powershell | `handoff-2026-10-02-d30-overwrite-rollback-check-go` | 待核 | PENDING |
| D2-054 | REUSE | go-to-powershell | `handoff-2026-10-02-d30-parallel-cmd-runner-go` | 待核 | PENDING |
| D2-055 | REUSE | go-to-powershell | `handoff-2026-10-02-d30-recoverable-overwrite-go` | 待核 | PENDING |
| D2-056 | REUSE | go-to-powershell | `handoff-2026-10-02-d30-staged-config-build-go` | 待核 | PENDING |
| D2-057 | REUSE | go-to-python | `handoff-2026-10-02-d28-autorun-manifest-backup-go` | 待核 | PENDING |
| D2-058 | REUSE | go-to-python | `handoff-2026-10-02-d28-child-cmd-capture-go` | 待核 | PENDING |
| D2-059 | REUSE | go-to-python | `handoff-2026-10-02-d28-concurrent-pipeline-go` | 待核 | PENDING |
| D2-060 | REUSE | go-to-python | `handoff-2026-10-02-d28-manifest-zip-collect-go` | 待核 | PENDING |
| D2-061 | REUSE | go-to-ruby | `handoff-2026-10-02-d29-inbox-batch-validate-go` | 待核 | PENDING |
| D2-062 | REUSE | go-to-ruby | `handoff-2026-10-02-d29-loopback-ack-exchange-go` | 待核 | PENDING |
| D2-063 | REUSE | go-to-ruby | `handoff-2026-10-02-d29-loopback-tcp-receiver-go` | 待核 | PENDING |
| D2-064 | REUSE | go-to-ruby | `handoff-2026-10-02-d29-notes-zip-bundle-go` | 待核 | PENDING |
| D2-065 | REUSE | powershell-to-csharp | `handoff-2026-10-02-d39-get-information-text` | 0 | dir-missing（该 direction 目录下 grep 无任何文件） |
| D2-066 | REUSE | python-to-powershell | `handoff-2026-10-02-d24-11-10-py` | 待核 | PENDING |
| D2-067 | REUSE | python-to-powershell | `handoff-2026-10-02-d24-16-28-py` | 待核 | PENDING |
| D2-068 | REUSE | python-to-powershell | `handoff-2026-10-02-d24-23-27-py` | 待核 | PENDING |
| D2-069 | REUSE | python-to-powershell | `handoff-2026-10-02-d24-6-28-py` | 待核 | PENDING |
| D2-070 | NEW | cpp-to-c | `D2-070-cpp-atombombing.cpp` | 13 | READ |
| D2-071 | NEW | cpp-to-c | `D2-071-cpp-bcd.cpp` | 13 | READ |
| D2-072 | NEW | cpp-to-c | `D2-072-cpp-wnfcallbackinjection.cpp` | 22 | READ |
| D2-073 | NEW | cpp-to-c | `D2-073-cpp-attack_chain.cpp` | 13 | READ |
| D2-074 | NEW | cpp-to-c | `D2-074-cpp-exfiltration.cpp` | 13 | READ |
| D2-075 | NEW | cpp-to-c | `D2-075-cpp-movement.cpp` | 22 | READ |
| D2-076 | NEW | cpp-to-csharp | `D2-076-cpp-edrsilencer.cpp` | 0 | dir-missing |
| D2-077 | NEW | cpp-to-csharp | `D2-077-cpp-xbin.cpp` | 0 | dir-missing |
| D2-078 | NEW | cpp-to-csharp | `D2-078-cpp-lsass_clone_dump.cpp` | 0 | dir-missing |
| D2-079 | NEW | cpp-to-csharp | `D2-079-cpp-ascii.cc` | 12 | READ |
| D2-080 | NEW | cpp-to-csharp | `D2-080-cpp-charconv_bigint.cc` | 12 | READ |

## 逐件文件清单与读取状态（去哪看）

- D2-007…012：见 [harness-a-cases-01.md](harness-a-cases-01.md)（含 D2-007 的 45 件逐项登记与 5 个 dir-empty 说明）。
- D2-013…030：见 [harness-a-cases-02.md](harness-a-cases-02.md)（D2-030 声明冲突、目录 0 件）。
- D2-031…047：逐件详尽清单与状态见本会话内读者将写入的 `harness-a-cases-11.md`（024-030）、`harness-a-cases-12.md`（018-023）、`harness-a-cases-13.md`（042-047）、`harness-a-cases-17.md`（037-041）、`harness-a-cases-18.md`（031-036）、`harness-a-cases-19.md`（013-017）；**这些件在本轮结束时尚未确认落盘，故 D2-042…069 的逐件清单仍标 PENDING。**
- D2-048…069：见 `harness-a-cases-14.md`（048-053）、`harness-a-cases-15.md`（054-059）、`harness-a-cases-16.md`（060-065）、`harness-a-cases-20.md`（066-069）——读者进行中，未落盘 ⇒ PENDING。
- D2-070…080：见 [harness-a-cases-04.md](harness-a-cases-04.md)。

## 检查点与续轮更新

- 检查点 0：映射建立。
- 检查点 20：**已达**（007-030 读取完成）。
- 检查点 40：**已达**（031-047 读取完成）。
- **续轮更新（覆盖上表 D2-048…059 的 PENDING）**：
  - D2-048/049/050/051/052/053 — **READ**，共 106 件；逐件清单见 `harness-a-cases-14.md`（读者已落盘）。
  - D2-054/055/056/057/058/059 — **READ**，共 95 件；逐件清单见 `harness-a-cases-15.md`（读者已落盘）。
  - D2-060/061/062/063/064/065 — **READ**，共 51 件；逐件清单见 `harness-a-cases-16.md`（读者已落盘）；D2-065 确认为 `dir-missing`（0 件）。
- **仍未完成**：D2-066…069（读者 4d8c43bf 进行中 → `harness-a-cases-20.md`）。
- 逐件清单落盘状态：01/02/04 已写；11（024-030）、13（042-047）、14（048-053）、15（054-059）、16（060-065）已写；12（018-023）、17（037-041）、18（031-036）、19（013-017）、20（066-069）待确认。

## 精确停止点

- 已读完并留证的现存项：D2-007…047（40 项；D2-026 已移除）+ D2-048…065（18 项）+ D2-070…075、D2-079、D2-080（8 项）= **66 项现存**。
- **未读/PENDING 集合 = {D2-066,067,068,069}**（4 项现存）。
- 停止点文件/集合：本节 + 上表 `状态=PENDING` 行 + findings §7。
- 复核方法：下轮先 glob `harness-a-cases-*.md`，确认 12、17、18、19、20 落盘，再补 066-069；完成后把本文件与 findings 转 COMPLETE。
