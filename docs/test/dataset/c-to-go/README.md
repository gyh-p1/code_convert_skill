# C → Go 转换记录

| case / run | 场景 | 来源性质 | 编译结论 | 功能证据 | 记录 |
|---|---|---|---|---|---|
| RC4 run-01 | 字节解密模块 + 薄 CLI | 上游 WjCryptLib RC4 + 本项目驱动 | **INCONCLUSIVE / BLOCKED-INFRA-ERROR**：Windows Agent 对混合大小写文件的身份哈希排序与 Controller 不一致，两次提交均无目标 build | 未计分、未运行 | [case](rc4-c-to-go/case.md) · [result](rc4-c-to-go/output/no-rag/run-01/result.md) |

这是探索性文本转换数据点，尚不足以宣称 C → Go 方向已验证。后续 Controller 修复前，保留原输入和两次环境失败证据，不以模型自审替代编译结论。

## 2026-10-02 external source allocations (not frozen)

6 allocated case records: 6 local source files present, 0 missing; source directories are Git-ignored. Linked `case.md` files record assignments and hashes; none has target code, a frozen task contract, or evaluation evidence. Do not count these in historical build results.

| Allocation | Source | Case | Local source |
|---|---|---|---|
| D04 | `Inject.c` | [handoff-2026-10-02-d04-inject-c](handoff-2026-10-02-d04-inject-c/case.md) | HASH_MATCHED |
| D04 | `CVE-2021-3493_exploit.c` | [handoff-2026-10-02-d04-cve-2021-3493-exploit-c](handoff-2026-10-02-d04-cve-2021-3493-exploit-c/case.md) | HASH_MATCHED |
| D04 | `bind.c` | [handoff-2026-10-02-d04-bind-c](handoff-2026-10-02-d04-bind-c/case.md) | HASH_MATCHED |
| D04 | `registry_run.c` | [handoff-2026-10-02-d04-registry-run-c](handoff-2026-10-02-d04-registry-run-c/case.md) | HASH_MATCHED |
| D04 | `windows.c` | [handoff-2026-10-02-d04-windows-c](handoff-2026-10-02-d04-windows-c/case.md) | HASH_MATCHED |
| D04 | `client.c` | [handoff-2026-10-02-d04-client-c](handoff-2026-10-02-d04-client-c/case.md) | HASH_MATCHED |
