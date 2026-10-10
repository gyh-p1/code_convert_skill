# 分类结果准入与 Agent 执行位置

适用于当前工作区的单文件与批量转换。**分类 `ALLOWED` 即准入通过，允许运行**；Agent 不再对分类结论作主观复核、降级或推翻，也不产出 `agentGateDecision` 一类的第二裁决。本页只规定引用完整性：提交的内容必须正是被分类的那份内容，且必须存在独立授权/隔离记录。分类器只读取文本；本页不新增提交服务、运行时或平台接口，也不修改已部署组件、配置、快照。

## 1. 接入位置与执行环境

原始输入先做只读画像；派生稳定候选 taskId、明确方向、源文件集合和哈希后，才调用分类器取得正式结果。多目标拆成不同候选 ID，缺登记或方向的原始条目先记准备缺口，不由分类器替代接入登记。**每次进入 EVALUATION_READY、提交或重提之前，必须消费当前版本的分类结果**。没有有效结果不得绕过本流程直接 POST `/api/jobs`。它是 Agent 流程约束，平台目前不会替 Agent 强制执行。

使用现有 [分类器](../../tools/safety_classifier_v2.py)。本机仅准备清单、核对哈希和读取结果；在获准的外部环境临时目录调用分类器，只读取待分类文件，不导入、编译或运行这些文件。临时目录中脚本副本必须与本仓库当前脚本 SHA-256 一致，不使用已部署 release 目录充当工具工作目录。

**暂存目录是暂存，不得常驻（2026-10-10 实测补入）**：分类器暂存目录必须建在**仓库外路径**（如 `$env:TEMP`），**不得建在仓库根**；每个暂存目录在取回并持久化 `classification-1.json` 之后**立即删除**（持久化位是该项 `output/<batchId>/01-frozen/`）。若因故必须在仓库内暂存，**先**把该模式加入 `.gitignore`，并在当轮任务结束前删除。判断标准是行为：暂存目录成为常驻物即违反本条——早期曾在仓库根残留 27 个 `.tmp-classify-*/`（112 条 untracked 条目），是反例。

分类输入可用候选任务清单或已有 `batch.json`；单项用只有一项的同形清单，不另建格式。保留本次实际分类输入的不可覆盖快照，`inputManifestSha256` 只核对该快照；最终冻结清单增加契约/运行字段后不要求 JSON 字节相同，改以 taskId、方向和精确源文件集合/哈希核对对应。临时传输可改变路径布局，但须保留上述身份和字节；给分类器传入实际临时路径及声明哈希，并保存原始、候选、冻结与临时清单的对应，不能互换它们的清单哈希。

远端调用示意（占位路径需替换，**不在本机运行**）：

```text
<remote-python> -I -B <temporary-tools>/safety_classifier_v2.py <temporary-batch.json> <new-classifications.json> <temporary-source-base>
```

输出采用独占创建，重跑使用新文件名，保留旧证据。默认不传 `--network-isolation-configured`；只有本批当前隔离已有真实证据、且授权记录有效时才可传入。CLI 开关不验证隔离证据，不构成执行许可。

## 2. 准入判定

**判定就是分类器的判定。** `admissionStatus=ALLOWED` 且 `blockingReason=null` 即准入通过，直接进入可运行队列，无需 Agent 另行批准或再写一个决策字段：

| 分类结果 | 判定 |
|---|---|
| `ALLOWED`（`blockingReason=null`） | **准入通过，允许运行**；按本页 §3 核对引用完整性后提交 |
| `BLOCKED`（任一原因） | 不允许运行；按下方原因分别处理 |
| 未知状态/原因、损坏结果、缺项 | 不得当作 ALLOWED；补齐或重跑分类 |

`BLOCKED` 原因的处理方式由分类规则本身决定，不由 Agent 重新权衡：

- `input_error`：修复或重新冻结输入后重跑分类。
- `public_network_unverified`：取得真实隔离证据后，在新条件下**重新分类**，重新检查全部阻断与 `details.files[].credentialFindings`；不得只手改分类 JSON 或直接把旧 BLOCKED 改成放行。
- `real_credential_suspected`：停止外发和执行，人工确认并处理后重跑分类；不能只手改分类 JSON。

分类结果未改变前不重复索取同一次判定。**隔离条件、源码内容或方向发生变化时必须重新分类**，因为那已不是同一份被判定过的输入。

## 3. 引用完整性核对（机械校验，不改判分类）

以下核对只回答一个问题：**即将提交的，是否正是分类器判定过的那一份**。任一项不成立说明引用错位，须重新分类或修正引用，而不是给该任务下一个更低的准入结论：

1. **身份对应**：将分类输出 `id/dir/case` 对应冻结任务的 `taskId/direction/caseId`。逐项覆盖，不允许缺项、重复、额外任务。**平台 identity 硬门禁按文件集合校验 `source/` 树（非按扩展名过滤）**：`source/` 里的每个文件——包含源侧驱动 `source/run_case.py`——都必须出现在分类输出的 `details.files[]` 里，否则 `POST /api/jobs` 返回 `403 identity_mismatch`（2026-10-10 实测，详见[Controller 适配](../adapter/controller/remote-controller-adapter.md)）。因此源侧驱动须**与源文件一同提交给分类器**。`target/` 侧驱动不在源分类范围内，仍须独立审阅。
2. **哈希对应**：核对 `classifierVersion/classifierSha256/inputManifestSha256`，以及提交 capsule 中精确文件集合与 `details.files[].sha256`。

   **必须重新分类的情形只有四项**（分类器只读源码文本，`analysisScope=source-text-only`）：① 源码内容变化；② 随源码一同提交、会被分类器读取的执行输入变化——**源侧驱动 `source/run_case.py` 位于 `source/` 树、须随源一同分类，归入本项**，其变化触发对 `source/` 文件集合重新分类；③ 工具链（源/目标平台、编译器、标准）变化；④ 方向（源→目标语言对）变化。此时创建有父版本关联的新契约/变体并重新分类，不覆盖原冻结输入。

   **oracle（及 `target/` 侧驱动）的变化不在此列**：它们**不在 `source/` 树、不被源分类读取**，其变化**不触发重新分类，只触发「评估就绪核对」重做**（见[行为保持 §4.1](behavior-preservation-contract.md)）。分类器的 `limitations` 声明 `target_driver_dependencies_not_assessed`：源侧驱动的**文本已被覆盖/取哈希**（以过 identity 门禁），但其**运行期依赖未被评估**——不得据此反推分类器评估过驱动行为。

   同一冻结契约内的目标代码 repair 另存目标版本和审阅记录，不改原源快照、不重置累计修复预算；分类源未变的修订不需要重复成功过的源码分类。**分类器未判定的目标/驱动仍须独立审阅**，不因"分类通过了"而免于驱动四要素核对。

   **分类器输入哈希逐字节取自 manifest，大小写敏感（2026-10-10 D2-021 实测补入）**：`classifier-input.json` 的 `sourceSha256` 必须**逐字节**取自 manifest 的 `Sha256` 列，**包括大小写**；**不得**手敲、**不得** `ToLower()`、**不得**重新格式化——分类器按字节比较，小写形式不等于大写形式，会误报 `BLOCKED/input_error`（`source_hash_mismatch`）而文件内容其实正确。分类报 `source_hash_mismatch` 时**先比对字符串形式**（长度、大小写）再怀疑文件内容；`input_error` 的正规出口是修复输入后重跑分类，不得绕过门禁。此外**目录名与 taskId 不是一一对应**，落盘前必须按 manifest 的 `Origin` 列确认该 taskId 对应的源文件。
3. **独立授权/隔离记录**：ALLOWED 是文本准入判定，不替代执行授权。复用用户已经给出的本任务/批次授权，记录可追溯来源、范围、有效期，以及源/目标所用 VM、网络阻断或受控目标、合成数据和清理证据。批次沿用 [Spec05 的授权字段](../../docs/stages/stage1/specs/submission-and-batch-authorization.md#2-批次授权记录-batch-authorizationjson)；**单文件任务按"批次为一"同样产出一份最小 `batch-authorization.json`**（同一 schema 与校验，`batchId` 取该项所属批次 id、`scope` 覆盖该单项），因为服务端硬门禁要求**每次提交都随附 `batchAuthorization`**——不再把单项授权只写进冻结记录。缺少记录先补证据，不生成全部为 true 的占位授权。私网、动态或未解析目标同样按源码实际行为审阅，不能把 `requiresNetworkIsolation=false` 当成"无需隔离"的证明。
4. **现役条件**：读取实际 Controller/Runner 身份、契约、平台、工具链与就绪状态，核对授权证据仍适用于当前基线；READY/快照不是网络隔离证明。授权的 `contractHash` 与现役 `contractSetHash` 核对，它不替代本任务源码/目标哈希。

核对通过即提交，不再记录额外的 Agent 决策值；核对不通过说明引用错位或授权缺失，注明具体待准备项（`RUN_SAFETY_NOT_READY` 或对应准备缺口）并修复后重来。**这些记录不是分类器的 `admissionStatus`，也不是平台 verdict 或执行证据。**

分类文本准入与动态执行是两个门槛：分类 `ALLOWED` 表示允许运行；缺少隔离/授权记录只影响该次提交能否发出，不改变分类结论，也不构成对允许文本转换的阻断。

## 4. 留证与字段分工

在现有冻结/阶段记录保留分类原文路径与哈希、原始/临时清单对应、任务及源/目标哈希、授权来源、隔离证据、现役契约/Runner、时间和提交尝试。批量逐项登记，不能仅留一个允许总数。

分类 JSON 的兼容字段 `executionApproved` 仅表示分类 ALLOWED；**禁止复制到 `evaluator_manifest.json`**。交付清单的同名字段仍按[交付契约 §3](../framework/delivery-handoff-contract.md#3-evaluator_manifestjson-字段来源纪律三分)，在获批隔离 Controller 接收并取得 jobId 后填写。分类、平台接收与 build/行为证据分别保留。

## 5. 暂行模式边界

此模式支持遵循本工作流的 Agent 使用现有分类器，并把分类结论作为唯一准入判定。

**2026-10-10 更新（平台闭环已实现）**：平台提交端已落地准入消费器并接成 `POST /api/jobs` 的**服务端硬门禁**——capsule **一律随附** `classification` 与 `batchAuthorization` 两个字段（**每次提交都附，不因版本而省**；单文件任务按"批次为一"附最小 `batch-authorization.json`，见 §3 第 3 条），未准入直接 **403**，不可绕过（见 [平台提交端准入闭环接入记录](../../docs/stages/stage1/reports/平台提交端准入闭环接入-2026-10-10.md) 与 [Spec05](../../docs/stages/stage1/specs/submission-and-batch-authorization.md)）。**重新部署最新版 Controller 后服务端强制校验**；重新部署前的现役 1.0.26 会**忽略**这两个多出的表单字段、不报错，因此一律随附既安全、又免去 Agent 自行判断"门禁是否已生效"。无论哪种，仍**不**通过提前复制 ALLOWED、APPROVED 或 executionApproved 声称整体接入已验收——真实样本提交、拒收与"其他客户端无法绕过"的验收在隔离环境完成。平台不 lift 任何 BLOCKED、带凭证线索一律拒绝、未知态默认拒绝，与本页口径一致。
