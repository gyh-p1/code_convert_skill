# Controller 比较策略适配：noise-tolerant-v1

> 文档类型：第三方比较策略的提交与证据适配（reference）
> 状态：ACTIVE（适用现役 `1.0.26` 统一部署；`noise-tolerant-v1` 比较配置自 `1.0.25-noise.1` 沿用并已在 1.0.26 健康验收中复核一致）
> 更新：2026-10-09
> 部署身份、取证范围与实时能力入口：[Runner 能力矩阵](runner-capability-matrix.md)；当前部署身份见[1.0.26 部署记录](../../../docs/stages/stage1/reports/1.0.26部署与快照更新记录-2026-10-09.md)，消噪试用的历史值见[能力矩阵 §1.3](runner-capability-matrix.md#13-controller-消噪部署2026-10-09历史)

本页供 Agent 冻结比较需求、组装现役 capsule、核对回传。比较由第三方 Controller 执行；本项目不新增比较器、运行时、Schema 或独立评分。连接、提交与未知回执恢复沿用[Controller 适配](remote-controller-adapter.md)，执行授权与隔离沿用[安全边界](../../framework/safety-boundary.md)。

## 1. 区分服务器配置与任务输入

| 层次 | 实际入口 | 接入方式 |
|---|---|---|
| 服务器比较配置 | `GET /api/health` 的 `comparison` | 提交前保存原始响应；配置由平台在 `controller.yaml` 中管理并在启动时读取 |
| 任务比较模式与观察范围 | capsule 的 `input_profile.json` | 使用既有 `comparisonPolicy` / `observationPolicy` 字段，不新增请求字段 |
| 本次实际比较结果 | `GET /api/jobs/{jobId}/comparison` | 正常双侧比较的 `verdictReason` 带 `Comparator=...` 配置记录；diff 带规则与证据引用 |

当前在线配置如下。这是服务器 `comparison` 对象的字段形状，**不是**可放进 `input_profile.json` 的任务字段；其中下划线键按真实接口原样保存。

```json
{
  "preset": "noise-tolerant-v1",
  "text_tokens": ["temporary-paths", "timestamps", "ephemeral-ports"],
  "system_noise_patterns": [
    "**/.DS_Store", "**/Thumbs.db", "**/desktop.ini",
    "**/__pycache__/**", "**/*.pyc"
  ],
  "tolerate_minor": true
}
```

一个服务器进程使用一套配置；任务不能通过 capsule 单独启停 `text_tokens`、`system_noise_patterns` 或 `tolerate_minor`。任务可选择 stdout/stderr 比较模式、文件 include/exclude；需要其它服务器规则时移交平台另冻配置与批次，不能伪造新字段或在失败后悄悄放宽。用户已认可本版三项思路，适用任务直接复用已有授权；业务明确要求精确值时优先选能保留该义务的现有模式。

## 2. 按行为义务选择输出模式

| 任务事实 | `comparisonPolicy.output` 的选择 | 边界 |
|---|---|---|
| 允许临时位置、记录时间或动态端口不同，且整条输出流都适用服务器已启用的规则 | 对该流用 `normalized-text` | 该流会应用全部启用的 token 类别；没有逐字段的文本消噪开关 |
| 输出包含需保留的文件名、时间值/有效期、固定端口、签名或其它关键文本 | 对该流用 `exact` | 不应用新增 token 消噪；平台按流 digest 比较，digest 已规范化 CRLF→LF，不能声称逐原始字节相同 |
| 输出是完整可解析 JSON，任务接受对象键顺序/展示格式差异 | 对该流用 `json-structural` | 沿用平台结构/值比较；本版不增加字段豁免、浮点容差、数组重排或 API 行为映射 |
| 同一流既有可忽略动态值又有必须精确保留的同类值 | 用 `exact`，或将已确认的混合比较需求交平台 | 不能把整个流设为 normalized-text 后声称其中关键字段仍精确检查 |

stdout、stderr 分别选择，例如允许 stdout 的展示噪声而保留 stderr 错误诊断时，可用 `stdoutMode="normalized-text"`、`stderrMode="exact"`。省略 mode 时平台默认 exact；提交方应显式冻结模式，不能因总分低而事后换模式。

二进制/协议载荷或 CRLF、编码本身属于业务义务时，需向平台确认相应原始字节证据与 oracle；本版 stdout 文本 digest 不足以承诺此类原始字节义务。不要把本页的模式选择变成对所有程序的统一等价标准。

### 2.1 文本消噪的实际边界

- `temporary-paths`：识别不含空白/引号的 `/tmp/`、`/var/tmp/` 与 Windows `Temp` 路径。每个输出流、每类 token 按首次出现顺序分配标签，并保留该流中重复引用的关系；不校验临时文件内容、用途或实际文件系统对象。含空格路径和其它临时根可能仍不匹配；stdout 与 stderr 之间没有统一资源映射。
- `timestamps`：识别 `YYYY-MM-DD[T或空格]HH:MM:SS` 形态及可选小数秒/时区后缀，保留同一值的重复关系；不校验日期合法性、时区换算、时差、超时或有效期。关键时间义务用 exact 或由平台禁用该类规则。
- `ephemeral-ports`：识别 `port` 后可带空格、冒号或等号的五位十进制值，仅 `49152–65535` 范围可被抽象；保留重复端口关系。`8080→9090`、范围外/非法数字仍是差异；固定高位端口也不能因处于该范围就接受消噪。其它 OS 实际分配范围或 `host:port` 格式不自动纳入。

这些规则减少已认可的展示差异，不证明端口真实动态分配或资源/业务行为等价。允许的原始输出差异会留下 `minor` diff，文本规则为 `noise-tolerant-v1:text-tokens:<启用类别>`；消噪前的输出在 EvidenceBundle 中保留，diff 摘要仅保留前 240 字符，完整性仍须核对实际采集长度、截断与原始引用。当前 `diff.path=stream.normalizedText` 和对应 evidenceRefs 不单独标明 stdout/stderr，定位反馈时需回查双侧 execution.stdout/execution.stderr 与冻结模式。

## 3. 文件消噪：观察范围与保护范围都要声明

`observationPolicy.filesystemInclude/filesystemExclude` 决定 Agent 采集范围；`comparisonPolicy.filesystem.include/exclude` 决定比较范围。只在比较 include 中写业务文件，不能补回 Agent 没有采集的事件；在任一排除列表中排掉业务文件也不能证明其行为保持。

当前默认噪声规则只包含 §1 列出的五种模式，不默认忽略 `.cache` 或锁文件。正常比较产生的文件缺失、额外或内容差异若仅涉及配置噪声路径，降为 `minor` 并保留 `noise-tolerant-v1:filesystem-noise` diff；原事件不从 EvidenceBundle 删除。重命名涉及任何非噪声路径时仍是 major。

任务明确要求检查噪声名称文件时，在比较 include 中追加覆盖该路径的非全范围模式。例如业务需要生成 `.pyc`：

```json
{
  "observationPolicy": {
    "dimensions": ["output", "filesystem"],
    "filesystemInclude": ["**/*"],
    "filesystemExclude": []
  },
  "comparisonPolicy": {
    "output": {"stdoutMode": "normalized-text", "stderrMode": "exact"},
    "filesystem": {
      "include": ["**/*", "**/*.pyc"],
      "exclude": [],
      "contentMode": "digest",
      "ordering": "ignored"
    }
  }
}
```

这是 `input_profile.json` 的字段片段，需与既有 schemaVersion/kind/profileId/argv/stdin/environment/workingDirectory/timeoutSeconds/fixtures 等字段合并，不能单独作为完整 capsule。仅业务有此义务时追加 `.pyc` 保护，不让解释器背景产物成为所有跨语言任务的统一要求。

`**/*`、`**`、`*` 三个全范围 include 不会保护噪声路径；其余 include 模式可以保护匹配文件。显式 exclude 仍先排除事件，即使同时 include，也不会被“保护”补回。没有采集或被排除的路径保持未覆盖；Agent 不得将其算作功能通过。

## 4. 次要差异容忍与结果解释

| 平台事实 | 适配处理 |
|---|---|
| 所有适用且已观察维度 matched | 原样记录平台 matched，限定为本次比较覆盖 |
| 适用且已观察维度仅有允许的 minor 差异，服务器 `tolerate_minor=true` | 维度可能 `semantic-match`，总 `behaviorVerdict` 可能 `semantic_pass`；记录规则、允许依据和原始差异 |
| 存在 critical/major，或关闭 minor 容忍后仍有差异 | 保留 mismatched/failed 与 diff，核对责任层后进入现有反馈分流 |
| 必需维度缺观察、输出截断无法解释、基线不可用 | 保留 partial/inconclusive 或平台其它原结果，不从空 diff 推断通过 |
| jobStatus=COMPLETED | 只说明作业完成；必须另外读取 report 的 codeVerdict、comparison 的 behaviorVerdict 和清理/环境 |

当前进程差异仍由平台生成为 major，没有新增“不同语言子进程自动等价”的豁免。network/registry 不因本次升级获得采集能力；Profile、Attestation、Permit 与 fixture runtime 也未在本次实现。

`semantic_pass` 在本试用配置下已包含上述显式消噪，不再仅指 host/user/cwd_items。它不替代目标侧 build 证据、不增加观察覆盖，不直接记作本项目功能验收通过。若归一化掩盖任务关键值，保留平台原 verdict，另记策略不适用及具体源/目标证据，交平台修正配置后重评；不能在本机重算或反写原报告。

## 5. 冻结、提交与取证

1. 读取 `/api/health` 与 `/api/runners`，保存完整响应；核对 ready、契约哈希、comparison 配置及实际 runner。`health.version=1.0.0` 是组件版本，不是 releaseVersion；部署发布身份见能力矩阵，不能仅凭 version 或 contractSetHash 判断消噪是否启用。comparison 缺失、未知 preset 或读取失败时，不补写本页示例当作实际配置；确认平台身份与策略后再使用受影响的消噪评估。
2. 在原冻结记录中写明 stdout/stderr 模式、文件采集/比较范围、接受差异依据、关键值保护及所依据的服务器 comparison 对象。授权与逐例隔离照原安全门槛核对；消噪配置不提供网络隔离证明。
3. 按原 `/api/jobs` 契约提交；接收回执保存 jobId。当前编译质量阶段继续采用获批双侧执行形态，编译结果只取对应目标侧 build，不因为本版有行为结果而扩大产品质量指标。
4. 保存原 report、双侧 EvidenceBundle、comparison、logs 和终态；正常比较核对 `verdictReason` 的 `Comparator=...` 与冻结配置及各 diff.rule。早期基线/执行失败可能不带该配置后缀，此时保留前置 health 和原诊断，不能猜补实际比较规则。
5. 对账 source/target、job/case、输入/目标版本、观察范围与清理。提交前后配置变化或回传配置与冻结不一致时，保留该结果并记配置疑点；已知新配置不能覆盖冻结的行为义务时暂停相关评估，交平台处理后另记变体重评，不自动归因目标代码。

建议将 `controller-health-before.json`、`runners-before.json` 与 `controller-health-after.json` 保存到既有任务记录/returned-evidence。它们是本次适配留证文件，不是新 Controller 字段；缺功能证据仍写 UNVERIFIED。已有批次固定同一比较配置，中断恢复时复核配置，不能将 strict 与 noise-tolerant-v1 的结果混作同一质量口径。

## 6. 配置调整与回退边界

服务器配置在启动时生效。禁用某类 token、关闭 minor 容忍或回退 strict 均由平台在确认没有活动 job 的窗口实施；Agent 不在普通转换提交中更改共享服务。服务器 strict 无新增文本/文件噪声规则，`system_noise_patterns: []` 关闭文件降级；设置 `tolerate_minor=false` 会保留 minor diff 但按不匹配处理。

原 1.0.24 的备份与恢复入口由平台保存，本项目只记录对接所需事实。回退后重新核对健康、实际配置与 runner，建立新配置变体，不能继承旧版本 semantic_pass。回退与消噪均不更改执行授权、网络/数据边界，历史报告不追改。当前适配经过静态核对与既有接口只读复核，未开展新转换或效果测试。
