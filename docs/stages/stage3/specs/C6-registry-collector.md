# C6：`registry` 维度采集器

> 类型：能力扩充 ｜ 优先级：**P3（建议延后）** ｜ 状态：声明不支持，未实测

## 1. 现状

每份 evidence bundle 中：

```json
"registry": { "status": "not-applicable",
              "limitations": ["evidence dimension is outside the current release scope"] }
```

`runner-capability-matrix.md` §1.3 明写"不新增 network/registry Collector"。

⇒ **平台已明确声明不支持**，无需再探测确认。

## 2. 为什么建议延后：**本批无消费方**

registry 维度**只在 Windows 目标 + 注册表行为**时有意义。核对 dataset-2 manifest：

- 存在 Windows 相关用例（`*to-csharp`、部分 `go-to-*`），
- 但**没有**以"注册表读写"为核心行为、且该行为**必须**通过 registry 维度才能验证的用例。

按项目原则"**新目录、元数据和机制必须有当前消费者**"，
在出现真实消费方之前不应投产。

## 3. 若未来要做，最小设计

| 事件 | 字段 |
|---|---|
| `registry.create` / `registry.modify` / `registry.delete` | 键路径（归一化 HKCU/HKLM）、值名、值类型、值摘要 |

**归一化很重要**：`HKEY_CURRENT_USER\Software\X` 与 `HKU\<SID>\Software\X` 应视为同一键，
否则会产生大量无意义差异（与 C1 的 process id 问题同构）。

## 4. 验收判据（若实施）

1. Windows runner 上提交一个无害的注册表读写样例 ⇒ `observations.registry.status = "observed"`；
2. 键路径归一化正确（同一键的不同写法不产生 diff）；
3. **回归**：非 Windows runner 申请该维度时不应崩溃，应给出明确不支持信息（参考 network 的硬拒行为）。

## 5. 结论

**建议：暂不实施。** 等出现真实消费方（如一批以注册表持久化为核心行为的用例）再启动。
当前应把资源投给 C0/C3/C5/C1。
