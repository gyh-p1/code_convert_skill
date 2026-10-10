# C5：修正分类器 hostname 启发式的假阳性

> 类型：假阳性阻断修复 ｜ 优先级：**P1** ｜ 依据：dataset-2 D2-055

## 1. 问题

分类器把**本地文件名字符串**误判为**网络主机名**，导致整项在**未做任何转换**的情况下被 `BLOCKED`。

### 实测（D2-055，`go-to-powershell/recoverable_overwrite.go`）

分类结果：

```json
{ "cls": "REVIEW_NETWORK",
  "admissionStatus": "BLOCKED",
  "blockingReason": "public_network_unverified",
  "details": { "files": [ { "network_mode": "hostname",
    "network_targets": [ { "value": "demo.txt", "line": 13,
                           "scope": "hostname", "provenance": "literal",
                           "redirectVerified": false } ] } ] } }
```

被引为网络目标的 `demo.txt`，在源码 **第 13 行**的实际上下文是：

```go
target := filepath.Join(root, "demo.txt")
```

即 `filepath.Join` 的**本地文件名参数**。

独立核对该文件：**没有任何网络调用**（无 `net.`、`Dial`、`Listen`、`http`、`url`、`socket`）。
程序行为仅为：建临时目录 → 写 `demo.txt`/`demo.bak` → 覆写 → 写 JSON 报告 → 打印路径。

⇒ **分类器假阳性**，性质为**规则缺陷**（不是"能力不足"）。

## 2. 影响

- 该项**0 模型调用**即被阻断（好的一面：没浪费转换）；
- 但**无法推进**，只能 `WAITING`，且需人工判断——**每次出现都要人介入**；
- 更糟的是方向性错误：**假阳性会掩盖真阴性**，让人对分类结果整体信任下降。

## 3. 建议修法

| 方向 | 做法 |
|---|---|
| **上下文排除** | hostname 候选若出现在**文件路径构造上下文**（如 `filepath.Join`、`path.Join`、`os.path.join`、字符串拼接成路径、`open(...)` 参数）中，**不应**计为网络目标 |
| **扩展名/形态启发** | 含常见**文件扩展名**（`.txt`/`.json`/`.log`/`.bak`/`.py` 等）且无 `://`、无端口、无 `@` 的裸串，**降级**为低置信 |
| **置信度分档** | 引入 confidence；仅高置信网络目标可触发 `BLOCKED`，低置信应记为**待复核**而非**阻断** |
| **区分"目标"与"字面量"** | 真正的网络目标通常经 socket/DNS/HTTP API 消费；仅出现在路径或字符串拼接中的，不应等同 |

> 建议**优先做"上下文排除 + 扩展名形态"**：改动局部、规则可解释、回归风险低。
> **置信度分档**是更彻底的方案，但会改动准入语义，需另行评估。

## 4. 验收判据

1. **正例**：D2-055 的源文件重跑分类 ⇒ **不得**再出现 `network_targets: [demo.txt]`，应为 `LOW_SIGNAL` 或其它非网络类；
2. **反例（防矫枉过正）**：构造一个**真的硬编码外部主机名**的样本（如 `Dial("tcp", "10.9.1.6:4444")`）⇒ 仍应识别为网络目标并 `BLOCKED`；
3. **既有正例回归**：D2-108（`Shell.cpp` 硬编码 `10.9.1.6` 且真实 `WSAConnect`）⇒ 必须**仍**判为网络目标；
4. 分类器的 `classifierSha256` 应随规则更新而变化，并在产物中登记。

## 5. 我方现状

D2-055 保持 `WAITING / BLOCKED_CLASSIFIER`。
**平台原判定未改写**，假阳性事实已记录于：
`docs/test/dataset-2/batch/items/D2-055.json` 的 `classifierObservation` 字段。

## 6. 实施状态（2026-10-10，classifier v2.4）

| 验收判据（§4） | 状态 |
|---|---|
| 1. 正例 D2-055 不再出现 `network_targets:[demo.txt]` | ✅ **回归锁定**：用例 `test_filename_literal_in_path_context_is_not_a_network_target`（`filepath.Join(root,"demo.txt")` → 非网络、ALLOWED） |
| 2. 反例：真实硬编码主机名仍 `BLOCKED` | ✅ **回归锁定**：用例 `test_real_hostname_with_network_api_is_still_a_target`（`net.Dial`+真实主机名 → `public_network_unverified`） |
| 3. 回归 D2-108（`10.9.1.6` + `WSAConnect`）仍判网络目标 | ✅ **回归锁定**：用例 `test_hardcoded_ip_with_wsaconnect_is_still_a_target`（IP 仍入 `network_targets`、REVIEW_NETWORK） |
| 4. `classifierSha256` 随规则更新变化并登记 | ✅ 已变化并登记：v2.3 `441b4d50125071544f6d1bbe836b7258d692c37c638acdb678a9e88795366524` → **v2.4 `009a6f31177b08334663340321494ace1e430de13f8a5687e6843ab26839f3a4`**（33840 B） |

**完成（2026-10-10）**：3 条回归用例（正例/反例/D2-108 回归）已补入 `test_safety_classifier_v2.py`，全套件 **50/50 通过**（47→50）；测试 SHA `02bbee966da5ae10d6fa504a99636fb887d31bdd2248ffe9dec1673f48901771` → **`45faa8e41de58e405cd52e4eb633dbe2743a0c2b3541be9375e0bc4dacd2b372`**（20311 B）。本机仅运行分类器自带回归（非转换样本），符合 stage3 §5.1 口径。D2-055 条目 `items/D2-055.json` 可由该项下一轮按新分类器重分类放行；平台原判定在重分类前不改写。
