# 分类结果准入与 Agent 执行位置

本页只适用于评估可达时的运行验收准入，覆盖正式单文件、片段和批量的该分支。ALLOWED 且 blockingReason=null 先于该分支源侧预检和生成，不替代授权/逐例隔离。先按[评估准备 §1.0](../framework/evaluation-readiness-contract.md#10-转换前可达性检查与仅转换分支)核可达性；确认不可达仅转换时不加载本页、不调用分类器、不要求 ALLOWED 或分类产物，冻结后直接生成、自审和部分交付。可达时源构建必过，正常行为分支生成前取有效源基线；本轮无法合法行为评估但源可构建时按 §1.3 采用 LIB_UNOBSERVABLE_COMPILE_ONLY，仍须分类。恢复评估前补本页及分类，不追改历史判定、不另造裁决，不修改已部署组件或新增运行时。

## 1. 接入位置与执行环境

原始输入先只读画像；稳定 taskId、方向和完整源文件集合后逐项冻结，再分类。登记缺口先准备，不由分类器替代。源预检前以及每次提交/重提消费精确版本结果；没有 ALLOWED 不预检、不生成、不 POST。平台按[Controller 适配](../adapter/controller/remote-controller-adapter.md)消费分类、授权与身份字段；平台校验不替代 Agent 的前置门禁。

调用分类器前先按[任务状态 §2.2](../framework/task-state-contract.md#22-冻结落盘门禁)确认本项本 run 的 `01-frozen/frozen-inputs.md` 已写出且回读通过，并保存核对依据；缺文件、空白或身份/版本错位不得分类。候选清单可作分类输入，不代表可以省略冻结 Markdown；该检查由 Agent 手工执行，不修改分类器输出或另造准入值。

本项目的分类系统就是已登记的 [tools/safety_classifier_v2.py](../../tools/safety_classifier_v2.py)，不依赖另建分类 API、服务或专用 MCP 工具。执行转换的智能体可使用原生文件/远端执行工具，手工逐项暂存并调用这个精确登记脚本，再读取原始结果；这是登记系统组件的有限调用例外，不是辅助脚本许可。

2026-10-20 系统维护续轮将源码升级为候选 2.6，精确 SHA／旧版身份见[维护登记](../../tools/classifier-registration.json)，状态为维护测试通过、未部署。2.6 对 TypeForwardedFrom 属性中的版本和 Python 可定位异常／验证函数字段参数提供有限上下文；完整源集合有网络信号时撤销相关豁免，未知消费者不加白名单。当前源码文件存在、登记 JSON 或本机维护单测通过不代表现役平台已受信：实际 Controller 有 acceptedClassifierSha256 时核精确值，缺声明仍须已有真实受信材料。旧 2.5 原件保持其原 SHA／版本；若新组件尚未受信，准备匹配的合法组件或平台升级，不伪标哈希、扩大接受范围或手改 ALLOWED。普通转换 Agent 仍不在本机运行分类流程、修改组件／登记或执行维护单测。

调用前核脚本版本/SHA 与本任务已有的受信登记材料一致，以及获准外部临时目录、可用解释器/原生执行通道、精确单项源树/清单和结果保存位置。登记材料可以是此前已取得、版本仍适用的原件，不要求每次实时联系 Controller；缺真实登记依据仍记具体缺口，不把 runner 能力表或仓库文件存在当作平台已接受的证明。脚本只读取待分类文件，不导入、编译或运行它们；本机仍只准备清单、核哈希、读结果，不在本机运行分类样本流程。暂存副本须与受信原件同 SHA，不访问 Controller 安装目录/jobs 或部署 release，不改逻辑、不写封装或批量调度。

没有额外“分类服务”不构成缺口；在评估可达分支，登记脚本缺失/身份不符、解释器或获准执行位置/通道不可用、源树/清单不完整才记具体分类准备缺口并停止受影响动作。不可达仅转换不做分类准备，分类条件不足不阻止其文本转换；文本安全仍按安全边界独立处理。

**暂存目录不得常驻**：分类器暂存目录必须建在**仓库外路径**（如 `$env:TEMP`），**不得建在仓库根**；每个暂存目录在取回并持久化当次 `classification-<N>.json` 之后**立即删除**（本项实际 run 的 `01-frozen/`，首次通常为 classification-1；关联变体位置按交付契约）。若因故必须在仓库内暂存，**先**把该模式加入 `.gitignore`，并在当轮任务结束前删除。只清理已取回的临时副本，不删除持久化分类输入/结果或旧拒收原件。

分类输入可用候选任务清单或已有 `batch.json`；单项用只有一项的同形清单，不另建格式。保留本次实际分类输入的不可覆盖快照，`inputManifestSha256` 只核对该快照；最终冻结清单增加契约/运行字段后不要求 JSON 字节相同，改以 taskId、方向和精确源文件集合/哈希核对对应。临时传输可改变路径布局，但须保留上述身份和字节；给分类器传入实际临时路径及声明哈希，并保存原始、候选、冻结与临时清单的对应，不能互换它们的清单哈希。

**路径布局核对**：清单中相对的 `sourcePath/sourceDir` 以该清单所在目录解析；CLI 的 source-base 用于约束允许读取的范围，不会把缺失路径自动改成相对 source-base 查找。例如清单在 `<temporary>/classifier-input.json`、`sourcePath` 为 `source/program.c`，须在 `<temporary>/source/program.c` 暂存对应精确文件。仅将清单放进临时目录、把 source-base 指向另一棵树，不等于该相对路径已存在。Agent 用原生工具手工核真实布局、源身份和路径对应；缺文件按 `input_error` 修正后重分类，不伪造 ALLOWED。

远端单项调用示意（由转换智能体手工使用原生执行工具，清单只含本项；占位路径须替换，**不在本机运行**）：

```text
<remote-python> -I -B <temporary-tools>/safety_classifier_v2.py <temporary-batch.json> <new-classifications.json> <temporary-source-base>
```

输出采用独占创建，重跑使用新文件名，保留旧证据。默认不传 `--network-isolation-configured`；只有本批当前隔离已有真实证据、且授权记录有效时才可传入。CLI 开关不验证隔离证据，不构成执行许可。

误报经重分类解除也保留首轮输入/输出和拒收原件，在既有记录写旧件→新件的原因及当前引用，不删除classification-1来使目录只剩ALLOWED。描述URL、版本串或类型名被词法命中时，可追加回源定位，但Agent不据此改判或豁免真实隔离；新分类件仍须按实际输入和准入条件产生。

hostname 误报复核逐条回读 network_targets 的原值/位置和实际消费者，区分本地路径分量、分隔符、元数据版本、命名空间标识与真正送入网络 API 的目标；字符串形状不能单独证明可达行为。文件后缀、namespace 或方法名也不能成为无条件白名单，同一字面量若被用于连接仍须核网络边界。复核只记录依据，不改变分类结果；Agent 不手改 BLOCKED/ALLOWED，也不换未登记脚本放行。

正式分类必须使用平台受信登记所钉定的精确版本与 SHA-256；脚本、输出身份或登记不一致时记工具准备缺口，先取得合法版本，不伪标身份、不扩大接受列表。脚本版本变化不自动解除已有 BLOCKED；只有适用输入、条件和合法脚本对应的新分类结果可供后续门禁消费。

## 2. 准入判定

本节用于评估可达分支，判定就是分类器的判定。ALLOWED 且 blockingReason=null 后进入源侧预检，不直接跳到运行队列；不可达仅转换不适用本节。独立授权与安全仍按适用动作核对，无需另造 Agent 决策字段：

| 分类结果 | 判定 |
|---|---|
| `ALLOWED`（`blockingReason=null`） | 评估运行分类准入通过；核授权/隔离后源侧预检（构建及适用运行基线），通过再生成；每次实际提交仍核引用与评估准备 |
| `BLOCKED`（任一原因） | 不预检、不生成、不提交；按下方原因处理 |
| 未知状态/原因、损坏结果、缺项 | 不得当作 ALLOWED；补齐或重跑分类 |

`BLOCKED` 原因的处理方式由分类规则本身决定，不由 Agent 重新权衡：

- `input_error`：修复或重新冻结输入后重跑分类。
- `public_network_unverified`：取得真实隔离证据后，在新条件下**重新分类**，重新检查全部阻断与 `details.files[].credentialFindings`；不得只手改分类 JSON 或直接把旧 BLOCKED 改成放行。
- `real_credential_suspected`：停止外发和执行，人工确认并处理后重跑分类；不能只手改分类 JSON。

分类结果未改变前不重复索取同一次判定。**隔离条件、源码内容或方向发生变化时必须重新分类**，因为那已不是同一份被判定过的输入。

## 3. 引用完整性核对（机械校验，不改判分类）

以下核对只回答一个问题：**即将提交的，是否正是分类器判定过的那一份**。任一项不成立说明引用错位，须重新分类或修正引用，而不是给该任务下一个更低的准入结论：

1. **身份对应**：将分类输出 `id/dir/case` 对应冻结任务的 `taskId/direction/caseId`。逐项覆盖，不允许缺项、重复、额外任务。**平台 identity 硬门禁按文件集合校验 `source/` 树（非按扩展名过滤）**：`source/` 里的每个文件——包含源侧驱动 `source/run_case.py`——都必须出现在分类输出的 `details.files[]` 里，否则 `POST /api/jobs` 返回 `403 identity_mismatch`（详见[Controller 适配](../adapter/controller/remote-controller-adapter.md)）。因此源侧驱动须**与源文件一同提交给分类器**。`target/` 侧驱动不在源分类范围内，仍须独立审阅。
   **文件集合须双向相等**：按现有记录对应到 `source/` 内完整相对路径，分别核“提交有而分类无”和“分类有而提交无”，两向差集都为空，逐文件哈希才继续核对。包含关系不够；即使仅编译不调用已分类驱动，也不能静默把它从 source/ 删除后沿用旧分类。恢复原冻结字节与变更源集合分别按下文处理。
2. **哈希对应**：核对 `classifierVersion/classifierSha256/inputManifestSha256`，以及提交 capsule 中精确文件集合与 `details.files[].sha256`。

   输入/任务条件变化的重新分类触发项：① 源码字节；② 完整 source/ 文件集合或随源提交的输入（含合法来源源驱动）；③ 工具链/平台/标准；④ 源→目标方向。创建父版本关联变体，不覆盖旧证据。另有 §2 的隔离分类条件变化（如 public_network_unverified 解除）必须重新分类；不能把“四项”解释成可沿用旧 BLOCKED/旧隔离假设。

   **oracle（及 `target/` 侧驱动）的变化本身不在此列**：它们不在 source/ 树、不被源分类读取，单独变化不触发重新分类，但须重做[评估准备核对](../framework/evaluation-readiness-contract.md)，变体及源基线另按下文核对。分类器的 limitations 声明 target_driver_dependencies_not_assessed：源侧驱动的文本已被覆盖/取哈希（以过 identity 门禁），其运行期依赖未被评估；不得据此反推分类器评估过驱动行为。

   不重分类不等于可沿用原 run 的全部条件：oracle/输入/策略等冻结条件改变仍按[任务状态 §1/§2.1](../framework/task-state-contract.md)记录变体，源基线是否受影响按评估准备 §1.2 核对。仅改目标稿且所有分类输入/条件未变时，使用当前适用的 classification-N 引用，不强制回到编号 1。任何变更同时触发源码/源集合或隔离等条件时仍须重新分类。

   同一冻结契约内的目标代码 repair 另存目标版本和审阅记录，不改原源快照、不重置累计修复预算；分类源未变的修订不需要重复成功过的源码分类。**分类器未判定的目标/驱动仍须独立审阅**，不因"分类通过了"而免于驱动四要素核对。

   **哈希按精确字节与实际组件核对**：输入保留原 manifest 的声明值与来源，不靠手敲或猜目录恢复。当前仓库分类器在比较 sourceSha256 时统一小写并处理 `sha256:` 前缀，不能把十六进制大小写不同直接认定为文件字节不同或当前 `source_hash_mismatch` 根因。遇到该诊断先核当次 classifierSha256、完整声明值、实际路径/源集合和字节哈希；历史说法须有当次原输入/诊断支持，不用当前实现反推过去。`input_error` 的正规出口是修正引用/输入后重新分类，不能手改结果放行。**目录名与 taskId 不是一一对应**，落盘前按原清单的路径字段（如 Origin）确认对应，不把临时数据集字段当通用 schema。
3. **独立授权/隔离记录**：复用已有合法授权，记录来源、范围、有效期、双侧 VM、真实网络阻断/受控目标、合成数据和清理。batchAuthorization 字段及固定 scope 只见[Controller 适配](../adapter/controller/remote-controller-adapter.md#batchauthorization-字段与来源)；单项也必附同形最小授权，不只写冻结记录。缺证据先补，不填全部 true 占位；requiresNetworkIsolation=false 不证明私网/动态目标无需隔离。授权变化触发有效性复核；影响分类隔离假设时重新分类。
4. **现役条件**：读取实际 Controller/Runner 身份、契约、平台、工具链与就绪状态，核对授权证据仍适用于当前基线；READY/快照不是网络隔离证明。授权的 `contractHash` 与现役 `contractSetHash` 核对，它不替代本任务源码/目标哈希。

引用核对通过仅满足本节检查，不再记录额外的 Agent 决策值；仍按根入口当前阶段推进：系统可达时分类后先完成源侧预检，正式生成、自审及适用评估就绪核对完成后才提交双侧评估；确认不可达仅转换按评估准备 §1.0，不提交评估。核对不通过说明引用错位或授权缺失，注明具体待准备项（`RUN_SAFETY_NOT_READY` 或对应准备缺口）并修复后重来。**这些记录不是分类器的 `admissionStatus`，也不是平台 verdict 或执行证据。**

分类与动态执行是不同门槛：缺授权/隔离不改 ALLOWED，但阻断受影响提交；可达正常流程若源侧预检尚未完成，也不能正式模型生成。不可达仅转换按评估准备 §1.0 核文本处理条件，不要求未执行的源预检或虚填 VM 隔离。已经通过适用生成前门禁的文本交付可按实际阶段收尾，不暗示已动态验证。

## 4. 留证与字段分工

在现有冻结/阶段记录保留分类原文路径与哈希、原始/临时清单对应、任务及源/目标哈希、授权来源、隔离证据、现役契约/Runner、时间和提交尝试。批量逐项登记，不能仅留一个允许总数。

分类 JSON 的兼容字段 `executionApproved` 仅表示分类 ALLOWED；**禁止复制到 `evaluator_manifest.json`**。交付清单的同名字段仍按[交付契约 §3](../framework/delivery-handoff-contract.md#3-evaluator_manifestjson-字段来源纪律三分)，在获批隔离 Controller 接收并取得 jobId 后填写。分类、平台接收与 build/行为证据分别保留。

## 5. 平台消费与验收边界

此模式支持遵循本工作流的 Agent 使用现有分类器，并把分类结论作为唯一准入判定。

平台提交必附 classification/batchAuthorization；字段、拒收形状与组件身份统一见[Controller 适配](../adapter/controller/remote-controller-adapter.md)和[能力矩阵](../adapter/controller/runner-capability-matrix.md)。提交前核对实际接口与受信身份；ALLOWED/APPROVED/executionApproved 分别按其字段职责解释，不表示已运行或已通过。
