# Controller 比较策略适配：strict、noise-tolerant-v1/v2

> 文档类型：第三方比较策略的提交与证据适配（reference）
> 状态：ACTIVE，按当前平台协议及实际 comparison 配置冻结比较规则。
> 身份核对：保存本项实际 health、schema、启动身份与回传，不沿用其他任务的版本/哈希作为当前固定值。

本页供 Agent 冻结比较需求、组装现役 capsule、核对回传。比较由第三方 Controller 执行；本项目不新增比较器、运行时、Schema 或独立评分。连接、提交与未知回执恢复沿用[Controller 适配](remote-controller-adapter.md)，执行授权与隔离沿用[安全边界](../../framework/safety-boundary.md)。

当前平台支持 noise-tolerant-v2 的 workspace_path_pairs，并使用 JSON 深拷贝和严格类型比较；字段/限制见[当前协议适配 §6](platform-revision-adapter.md#6-追加归因与比较配置)。strict/v1 字段与默认保持兼容，任务必须读实际完整配置。目录映射是服务器配置，须与冻结允许差异对应；它不是任务 InputProfile 字段，不自动忽略计时、错误内容或相对文件名。

## 1. 区分服务器配置与任务输入

| 层次 | 实际入口 | 接入方式 |
|---|---|---|
| 服务器比较配置 | `GET /api/health` 的 `comparison` | 提交前保存原始响应；配置由平台在 `controller.yaml` 中管理并在启动时读取 |
| 任务比较模式与观察范围 | capsule 的 `input_profile.json` | 使用既有 `comparisonPolicy` / `observationPolicy` 字段，不新增请求字段 |
| 本次实际比较结果 | `GET /api/jobs/{jobId}/comparison` | 正常双侧比较的 `verdictReason` 带 `Comparator=...` 配置记录；diff 带规则与证据引用 |

服务器 `comparison` 对象的字段形状如下，实际取值以本项保存的 health 为准；**不是**可放进 `input_profile.json` 的任务字段。其中下划线键按接口原样保存。

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

一个服务器进程使用一套配置；任务不能通过 capsule 单独启停 `text_tokens`、`system_noise_patterns` 或 `tolerate_minor`。任务可选择 stdout/stderr 比较模式、文件 include/exclude；需要其它服务器规则时移交平台另冻配置与批次，不能伪造新字段或在失败后悄悄放宽。适用任务复用已有合法授权；业务明确要求精确值时选择能保留该义务的模式。

## 2. 按行为义务选择输出模式

| 任务事实 | `comparisonPolicy.output` 的选择 | 边界 |
|---|---|---|
| 允许临时位置、记录时间或动态端口不同，且整条输出流都适用服务器已启用的规则 | 对该流用 `normalized-text` | 该流会应用全部启用的 token 类别；没有逐字段的文本消噪开关 |
| 输出包含需保留的文件名、时间值/有效期、固定端口、签名或其它关键文本 | 对该流用 `exact` | 不应用 token 消噪；按流 digest 对应的对象比较。核实际 producer、编码、摘要与 size 的对象，未确认采集原字节时不宣称原始字节相同 |
| 输出是完整可解析 JSON，任务接受对象键顺序/展示格式差异 | 对该流用 `json-structural` | 先核真实 structuredValue 与结构/值比较；既有 ignoredJsonPaths 的声明、传递及限制见 §2.2，不增加浮点容差、数组重排或 API 行为映射 |
| 同一流既有可忽略动态值又有必须精确保留的同类值 | 用 `exact`，或将已确认的混合比较需求交平台 | 不能把整个流设为 normalized-text 后声称其中关键字段仍精确检查 |

stdout、stderr 分别选择，例如允许 stdout 的展示噪声而保留 stderr 错误诊断时，可用 `stdoutMode="normalized-text"`、`stderrMode="exact"`。省略 mode 时平台默认 exact；提交方应显式冻结模式，不能因总分低而事后换模式。

二进制/协议载荷或CRLF、编码本身属于业务义务时，核原始字节采集、摘要对象、截断和实际oracle。文本解码后的摘要不自动证明原始协议字节；不能凭字段名digest推定producer一致。展示换行允许不同时优先选择对应normalized-text或结构策略，exact不会因此自动接受差异。

### 2.1 文本消噪的实际边界

- `temporary-paths`：识别不含空白/引号的 `/tmp/`、`/var/tmp/` 与 Windows `Temp` 路径。每个输出流、每类 token 按首次出现顺序分配标签，并保留该流中重复引用的关系；不校验临时文件内容、用途或实际文件系统对象。含空格路径和其它临时根可能仍不匹配；stdout 与 stderr 之间没有统一资源映射。
- `timestamps`：识别 `YYYY-MM-DD[T或空格]HH:MM:SS` 形态及可选小数秒/时区后缀，保留同一值的重复关系；不校验日期合法性、时区换算、时差、超时或有效期。关键时间义务用 exact 或由平台禁用该类规则。
- `ephemeral-ports`：识别 `port` 后可带空格、冒号或等号的五位十进制值，仅 `49152–65535` 范围可被抽象；保留重复端口关系。`8080→9090`、范围外/非法数字仍是差异；固定高位端口也不能因处于该范围就接受消噪。其它 OS 实际分配范围或 `host:port` 格式不自动纳入。

这些规则减少冻结允许的展示差异，不证明端口真实动态分配或资源/业务行为等价。允许的原始输出差异会留下 minor diff；核实际 rule/版本。diff 摘要只保存有限前缀，不能代替完整观察。输出差异按实际 `execution.stdout` / `execution.stderr` 路径与双侧 evidenceRefs 回查；路径或引用不足时直接读取相应流原件，不改写原 diff。

**临时路径的保护性复核**：允许临时根变化不等于允许相对路径、文件名或分隔符缺失。按本项实际可取得的完整原始流表示／structuredValue、文件观察及冻结关系定位业务后缀；不能把 token 命中或 minor 标签当保护项已检查。已有报告记载目标漏写分隔符却获 semantic_pass，这只说明该历史配置可能吞掉了业务差异，不证明现役规则已修复，也不证明所有临时路径都须字面相同。

冻结时需要保留业务后缀而 temporary-paths 无法表达时，按现有能力选能保护它的 exact、结构模式或平台已支持且精确的 workspace_path_pairs；混合流无法表达则记策略能力缺口，不伪造逐字段开关、不在看到 diff 后删除字段求匹配。配置存疑时保留原判及双侧未归一化内容，说明保护项是否仍成立；已确认目标差异按有限修复闭环处理，不等平台修复才承认误译，不本机重算分数。

平台维护验收应同时包括允许的动态根变化，以及必须保留的业务文件名／漏分隔符／固定端点变化，展示归一化前后与规则范围；这是维护建议，不是 Agent 新造反例或每项追加运行的授权。阶段与责任交叉时见[评估故障分诊](evaluation-failure-triage.md)。

### 2.2 JSON 字段忽略的声明与消费

InputProfile 1.0/1.1 在 `comparisonPolicy.output.ignoredJsonPaths` 声明字符串列表；这不是任意流预处理或通用 JSONPath。字段忽略只按点分名称遍历字典并移除命中键，不遍历数组、不支持通配符，字段名自身含点时也不能据此表达其字面键。它消费流中的实际 structuredValue，不会把外层包装里的 stdout 字符串自动变成业务 JSON。

该列表属于output级，两通道采用json-structural时都会收到同一列表，不是逐通道独立配置。同名路径在两流中语义不同时，不能把两流均设JSON后声称只忽略了其中一个；须保护对应流的精确义务，现有模式无法同时表达时记细粒度能力缺口，不自行增加per-stream字段。

**声明不等于输出比较已消费**：输出比较入口须把 ignoredJsonPaths 传递给 stdout/stderr 的结构比较，并使用副本保留原 structuredValue。按本项精确实现身份和实际规则命中核实消费链，不能仅凭 schema 接受字段或低层深拷贝推定忽略生效；缺证明时记具体能力缺口，不反复重提求匹配，也不据此倒推其他 job 的根因。

仅在生成前契约明确许可、该字段不承载业务结果且其他保护项仍被实际比较时使用。冻结精确路径、对象与允许原因，保留两侧原值和命中记录；耗时用于超时/性能要求、端口用于固定端点、State/计数器用于业务结果时均受保护。不能在看到当前 diff 后直接增加忽略项；新允许条件按任务状态另记变体。字段忽略、关系归一和数值容差是不同需求，前者不证明接口范围或重复标识关系相同。

### 2.3 类型化文本 token

以下类别通过服务器 `text_tokens` 显式启用；提交前核实际实现身份及配置支持，未支持的类别不填入配置。v1/v2 默认仅 §2.1 三类；strict 不接受噪声规则，exact 流不受 token 影响。任务提交方不直接改共享部署或服务器配置。

| token | 有限识别与保护 | 不支持/不可推断 |
|---|---|---|
| durations | duration/duration_ms/elapsed/elapsed_ms/scan_ms的非负十进制值；保留标签和单位，ms/s等不同仍是差异 | 不吞超时/预算结果，不整类删数字；性能或精确耗时属业务时不用该流策略；未覆盖表示保留差异 |
| process-ids | pid/process_id/process-id/process id等带冒号/等号的数字；同一侧stdout/stderr共享重复身份映射 | 不猜无标签数字为PID，不跨job建立进程对应，不证明进程实际配对 |
| memory-addresses | address/addr/pointer标签后的十六进制值；按数值保持重复身份关系 | 不把所有十六进制载荷视为地址，不证明内存对象/内容相同 |
| endpoint-ports | host:port、IPv6括号及port标签的32768–65535候选端口；保留host与重复端口关系 | 区间只限匹配，不证明动态分配；固定高位端口或混合流仍用exact/提出细粒度需求。其它区间不覆盖 |

这些 token 仅作用于 normalized-text；两个通道均用该模式时，process-ids、memory-addresses、endpoint-ports 共享同侧身份映射，保留重复引用与拆分/合并差异，不能外推 JSON/exact 混合模式或跨 job 关系。临时路径/时间戳类别仍按流分别映射。State、业务计数器和 stderr 不提供整类忽略选项。已冻结精确义务始终优先，有限消噪不增加观察覆盖。

## 3. 文件消噪：观察范围与保护范围都要声明

`observationPolicy.filesystemInclude/filesystemExclude` 决定 Agent 采集范围；`comparisonPolicy.filesystem.include/exclude` 决定比较范围。只在比较 include 中写业务文件，不能补回 Agent 没有采集的事件；在任一排除列表中排掉业务文件也不能证明其行为保持。

**先按行为义务确定观察维度**：`observationPolicy.dimensions` 与本项冻结的行为义务对应。行为评估含文件副作用（写文件、建目录、改内容）时申请 `filesystem` 与适用 `output`，不得只申请 output 再靠驱动回显代文件证据，两侧回显不对称还会引入装置差异。文件采集、打分和内容 digest 比较均须逐项核实际路径/内容、捕获限制及现役能力，不把维度可用写成所有文件形态都已完整采集。未申请是提交准备缺口，已申请却未支持/未采得则分别记具体能力/证据缺口。涉及子进程时核 `processes` 的实际采集与比较范围；network/registry 的缺口及当前支持按能力矩阵，不盲目申请或声称覆盖。

当前默认噪声规则只包含 §1 列出的五种模式，不默认忽略 `.cache` 或锁文件。正常比较产生的文件缺失、额外或内容差异若仅涉及配置噪声路径，降为 `minor` 并保留 `noise-tolerant-v1:filesystem-noise` diff；原事件不从 EvidenceBundle 删除。重命名涉及任何非噪声路径时仍是 major。

任务明确要求检查噪声名称文件时，在比较 include 中追加覆盖该路径的非全范围模式。例如业务需要生成 `.pyc`：

采集和比较均须显式列出业务副作用路径；不得用 `**/*`、`**`、`*` 等全工作目录模式把 program.exe、对象文件、工程中间件或解释器背景产物混进业务比较。下例假定业务义务仅为 `out/result.txt` 和 `out/cache/result.pyc`；路径须逐项替换，不能套用为所有任务的范围。

```json
{
  "observationPolicy": {
    "dimensions": ["output", "filesystem"],
    "filesystemInclude": ["out/result.txt", "out/cache/result.pyc"],
    "filesystemExclude": []
  },
  "comparisonPolicy": {
    "output": {"stdoutMode": "normalized-text", "stderrMode": "exact"},
    "filesystem": {
      "include": ["out/result.txt", "out/cache/result.pyc"],
      "exclude": [],
      "contentMode": "digest",
      "ordering": "ignored"
    }
  }
}
```

这是 `input_profile.json` 的字段片段，需与既有 schemaVersion/kind/profileId/argv/stdin/environment/workingDirectory/timeoutSeconds/fixtures 等字段合并，不能单独作为完整 capsule。仅业务有此义务时追加 `.pyc` 保护，不让解释器背景产物成为所有跨语言任务的统一要求。

清单里存在动态工作目录/时间字段时，将可确定的其他文件和字段分别核观察与策略支持；不因一处无法比较就省掉全部文件内容。没有对应文件证据，stdout 的 files/total 匹配不能外推为归档或清单内容匹配。

`**/*`、`**`、`*` 三个全范围 include 不会保护噪声路径；其余 include 模式可以保护匹配文件。显式 exclude 仍先排除事件，即使同时 include，也不会被“保护”补回。没有采集或被排除的路径保持未覆盖；Agent 不得将其算作功能通过。

## 4. 次要差异容忍与结果解释

| 平台事实 | 适配处理 |
|---|---|
| 所有适用且已观察维度 matched | 原样记录平台 matched，限定为本次比较覆盖 |
| 适用且已观察维度仅有允许的 minor 差异，服务器 `tolerate_minor=true` | 维度可能 `semantic-match`，总 `behaviorVerdict` 可能 `semantic_pass`；记录规则、允许依据和原始差异 |
| 存在 critical/major，或关闭 minor 容忍后仍有差异 | 保留 mismatched/failed 与 diff，核对责任层后进入现有反馈分流 |
| 必需维度缺观察、输出截断无法解释、基线不可用 | 保留 partial/inconclusive 或平台其它原结果，不从空 diff 推断通过 |
| jobStatus=COMPLETED | 只说明作业完成；必须另外读取 report 的 codeVerdict、comparison 的 behaviorVerdict 和清理/环境 |

原 verdict 与 Agent 的观察采信分别记录，按[评估准备 §5](../../framework/evaluation-readiness-contract.md#5-原始观察采信与归因)核输入、状态、观察归属与冻结路径。即使 coverage 给出充分或 stderr 非空，也不免此核对；not-applicable 不证明无副作用。外部新增 coverage 字段只有核实当前 schema/回传后才消费，不在 capsule 中伪造。

进程差异由平台生成为 major，不提供“不同语言子进程自动等价”的豁免。network/registry、网络隔离 Attestation/Permit 及 fixture runtime 的能力须有独立接口与实际证据支持；不从比较 preset 或消噪规则推定具备这些能力。

有效matched与有效semantic_pass均可计本冻结范围的功能比较通过小计，分列两类及策略/覆盖；先按[评估准备§5.1](../../framework/evaluation-readiness-contract.md#51-有效性消噪与功能分类的次序)核有效性。它们不替代目标build、不增加观察覆盖，不宣称完整业务或普遍等价。归一化掩盖关键值时保留原verdict，另记策略不适用及依据，交平台修正后按新冻结条件重评，不本机重算或反写报告。

宽泛消噪的关系选择与保护项同样消费评估准备 §5.1。archive_bytes、host:port、错误堆栈、集合顺序只能按具体业务义务提出允许关系；本页列出的 token/模式/文件配置就是适配支持范围，不从提案推定已实现错误类别映射、数值容差、解压内容 oracle 或跨流资源对应。

## 5. 冻结、提交与取证

1. 读取 `/api/health` 与 `/api/runners`，保存完整响应；核对 ready、契约哈希、comparison 配置及实际 runner。`health.version=1.0.0` 是组件版本，不是 releaseVersion；部署发布身份见能力矩阵，不能仅凭 version 或 contractSetHash 判断消噪是否启用。comparison 缺失、未知 preset 或读取失败时，不补写本页示例当作实际配置；确认平台身份与策略后再使用受影响的消噪评估。
2. 在原冻结记录中写明 stdout/stderr 模式、文件采集/比较范围、接受差异依据、关键值保护及所依据的服务器 comparison 对象。授权与逐例隔离照原安全门槛核对；消噪配置不提供网络隔离证明。
3. 按原 `/api/jobs` 契约提交；接收回执保存jobId。编译取目标build，行为按适用oracle与comparison分层；有效matched/semantic_pass均可计冻结范围比较通过，未经有效性核对不直接按标签计入，不合成转换成功率。
4. 保存原 report、双侧 EvidenceBundle、comparison、logs 和终态；正常比较核对 `verdictReason` 的 `Comparator=...` 与冻结配置及各 diff.rule。早期基线/执行失败可能不带该配置后缀，此时保留前置 health 和原诊断，不能猜补实际比较规则。
5. 对账 source/target、job/case、输入/目标版本、观察范围与清理。提交前后配置变化或回传配置与冻结不一致时，保留该结果并记配置疑点；已知新配置不能覆盖冻结的行为义务时暂停相关评估，交平台处理后另记变体重评，不自动归因目标代码。

建议将 `controller-health-before.json`、`runners-before.json` 与 `controller-health-after.json` 保存到既有任务记录/returned-evidence。它们是本项留证文件，不是 Controller 请求字段；缺功能证据仍写 UNVERIFIED。已有批次固定同一比较配置，中断恢复时复核配置，不能将 strict 与 noise-tolerant-v1 的结果混作同一质量口径。

### 候选 v3 临时路径保护

2026-10-20 平台候选源码新增 opt-in noise-tolerant-v3，尚未部署。2026-10-21 审查修订后，默认同时关闭 temporary-paths 和 ephemeral-ports，默认文本 token 仅 timestamps；显式启用 temporary-paths 必须声明精确 workspace_path_pairs，否则配置拒绝。根对仍受数量、绝对路径、尾分隔符、具体程度及无穿越／重复约束；只替换根，不吞未登记根、业务后缀、文件名、重复关系或漏分隔符。没有把后缀的跨 OS 分隔符一律重写成等价。

数值位于临时端口区间不能证明该字段是动态分配。只有本次冻结允许且流内固定端点不被误掩盖时，才显式启用 ephemeral-ports／endpoint-ports；现有 token 没有字段级固定／动态识别能力，混合流无法保护时用严格比较。v1/v2 的旧默认不变；新 v3 不靠数值范围默认消掉固定高端口差异。历史报告不重算，当前部署须重新核身份和实际 comparison 配置。

同一候选修复 v2 有显式根对后仍套用整条临时路径 token 的问题；v1 与无根旧 v2 保留兼容行为，仍可能掩盖路径拼接差异。新任务有路径义务时选择已证实支持的 strict 或受限 v3；旧服务不假定已修复，不悄悄改变冻结配置或重算历史结果。实际 preset／token／根对由服务器合法配置提供并留原件，不能写成 capsule 的自造字段。

## 6. 配置调整与回退边界

服务器配置在启动时生效。禁用某类 token、关闭 minor 容忍或回退 strict 均由平台在确认没有活动 job 的窗口实施；Agent 不在普通转换提交中更改共享服务。strict 不应用文本/文件噪声规则，`system_noise_patterns: []` 关闭文件降级；设置 `tolerate_minor=false` 会保留 minor diff 但按不匹配处理。

配置调整或回退后重新核对健康、实际配置与 runner，建立对应配置变体，不能继承不再适用的 semantic_pass。回退与消噪均不更改执行授权、网络/数据边界，已有报告不追改。

## 7. 比较适用性与保护项

冻结比较策略时逐项核下表。所需关系超出实际 token/schema/驱动支持时记具体缺口，不自行补装置或比较器，不把缺支持变成允许差异。原始观察始终保留。

| 比较对象 | 冻结允许关系 | 必须保留的差异与边界 |
|---|---|---|
| JSON忽略项 | 已冻结非业务duration字段变化，输出入口实际转发精确路径，业务字段仍比较；原structuredValue不被修改 | 同级业务字段、类型/缺失、数组元素或未命中路径的真实差异；低层实现存在不代替端到端消费证明 |
| 动态host:port及PID/地址关系 | 已确认动态端点/标识可按对应关系变化，同一对象重复引用一致 | 固定端点、地址/资源关联错误、两次引用被错误合并或拆分；不是所有数字替换同一标签 |
| 错误展示关系 | 同一错误路径的运行时展示按冻结约定不同 | 错误类别/时点、捕获/续行、退出和副作用变化；当前无ignore-stderr模式，不造此枚举 |
| 观察有效性与源预检隔离 | 合法驱动协议确认自失败时不产有效功能通过；source-only无target比较 | 程序合法输出DRIVER-FAILURE或退出97不能仅凭字面当装置失败；历史原判不追改 |
| 服务存活期与中性fixture能力 | 合法现成驱动取得就绪和业务观察，独立同态cwd/fixture可重置并收尾 | 端口可连但日志未刷新、进程被杀后丢缓冲、共享可变目录被前一侧污染；PTY改变终端语义须另核 |
| 计数器/服务态的条件关系 | 仅冻结明确允许且不删业务含义的波动 | 不同接口集合、累计/增量、协议覆盖、单位或状态转移，均不能整类归一成通过 |

网络隔离按能力矩阵记录实际实现/快照、OS、网络策略、测量时间与覆盖及失效条件，由平台合法提供的证据支持；不以 configured=true、其他任务探针或单 OS 结果外推三 OS 隔离。不发起公网探测来替代封闭边界核验，支持缺失仍阻断受影响执行。
