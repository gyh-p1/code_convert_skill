# 系统加载工具开发与验收

> 日期：2026-10-15
> 结论：三职责工具、角色边界、现有流程的文本接入及本文所列宿主文档场景已验收；仓库全套回归存在原分类器的独立基线失败，不能宣称全库全绿。
> 范围：文档结构与加载证据维护，不进行转换效果验证、样本编译/运行或平台部署。

## 1. 要求与当前证据

| 要求 | 当前证据与判定 |
|---|---|
| 一个工具检查结构、记录提供、核对下一动作 | tools/loading_preflight.py 的 check-repo、record-read、check-next；CLI 与真实宿主调用均已执行 |
| 只允许系统执行登记脚本，第三方继续无辅助脚本/逐项调度 | AGENTS、根/发现入口、安全、分类准入、任务状态、交付、批量/长文件和开发规范已回查；工具说明明确执行者；test_foreign_agents_remain_manual 保留文字回归 |
| 精确版本登记 | tools/loading-registration.json 保存脚本、测试、依赖清单的 SHA-256，CLI 操作前验证；.gitattributes 固定这些文件 LF；篡改登记摘要用例拒绝 |
| 根表为唯一清单、身份与锚点有效 | 根表增加稳定标识，限定表形制；structure-product-verified.json 对 12 份正文 PASS；同数量替换、重复身份、缺文件、坏锚点、未知表形制均有拒绝用例 |
| 真实返回证据，后台读取不冒充已提供 | 实际 exec 调用关联九份合成正文；receipt-fixture-*-002.json 回读本会话原始日志及输出，非合成宿主证明；产品 safety 片段另有实际返回 |
| 截断、分段及上下文失效 | 真实宿主截断返回 UNAVAILABLE 且无强凭证；回归覆盖中段缺口、重叠、混版、跨会话、已知压缩/恢复、日志篡改及部分写入 |
| 既有消费时点、迟读不追认 | start/map/freeze/后续动作分别核；真实 before-call 审计返回 late-read；复杂度在画像前未知可显式暂挂，到 map/freeze 前须定案，避免引入画像死锁 |
| 沿用冻结/阶段记录，不另建状态体系 | 单个 loading-preflight Markdown 块，只引用原件；工具不写 phase/lifecycle，不发模型请求或提交 job |
| 原件不可覆盖，停止仍报告，既有 job 可清理 | 独占原子发布、落盘失败测试；delivery 仍走全去向 result.md；真实 cleanup 加载例外带 executionAuthorized=false |
| 人工回退及效果验证边界 | 操作说明第 5 节；manual-comparison.md 四个同材料场景一致，未声称效率提升或任意 Agent 遵守率 |

## 2. 代码与文档变化

新增系统工具、50 项文本回归、固定依赖清单、摘要登记和操作说明；登记组件固定 LF、验收证据设 -text，避免跨 Windows checkout 改写原件字节。工具使用 Markdown AST；离线运行，不读取样本源码、不导入/执行样本，不操作 Controller 安装目录，路径拒绝用例不实际访问该目录。

产品文档仅补加载消费与执行者边界：7 份真源及其职责不变；冻结→ALLOWED/null→源预检→生成→自审→评估→取证/归因→交付门禁的顺序不变；LIB 分支、模型来源、有限修复预算、40 项对账、WAITING/终态和分层结论语义不变。分类器执行明确归系统侧，第三方智能体通过已提供入口逐项请求；没有入口保留准备缺口，不跳过分类、不新造 Controller API。

脚本许可没有扩展到第三方智能体辅助编排，未新建转换运行时或测试框架。加载结果仍是流程核对，未接入不可绕过的 hook，不能声明平台技术强制拦截。

## 3. 验证范围与原始输出

所有原件见[验收目录](loading-acceptance-2026-10-15/README.md)。维护环境为 Windows、Python 3.13.9、markdown-it-py 4.2.0、mdurl 0.1.2。系统维护侧命令：

```text
python -B -m unittest discover -s tools -p test_loading_preflight.py -v
python -B -m unittest discover -s tools -p test_safety_classifier_v2.py -q
python -B tools/loading_preflight.py check-repo --repo . --out <unique-product-report>
python -B tools/loading_preflight.py record-read --emit ...
python -B tools/loading_preflight.py record-read --offer ... --transcript ... --call-id ... --out ...
python -B tools/loading_preflight.py check-next --repo ... --record ... --action ... --transcript ... --out ...
git diff --check
git diff --exit-code HEAD -- tools/safety_classifier_v2.py tools/test_safety_classifier_v2.py
```

加载回归覆盖四种任务形态及所有动作名；关键负例不以 PASS 标签掩盖：缺项/错误/截断各自按退出码与原始 finding 验收。宿主正例使用合成短文档，不能据此推定七份真实长契约已在本轮完整加载。产品实际部分读取负例明确返回七项 coverage 缺口。

## 4. 分类器基线失败及不变性

原分类器回归执行 70 个测试，其中 `test_metadata_network_guard_covers_the_complete_source_set` 的 8 个 subtest 失败，覆盖 Python/C#、两种文件顺序、隔离开关两种条件。未隔离的预期 BLOCKED 实际 ALLOWED；已隔离时 requires_network_isolation 仍为 false。原始输出在 classifier-baseline-001.log。

两份原分类器文件与 HEAD 无 diff，本轮未改它们：源码 SHA-256 `e81ceab16f237ffe5316e7fe0d5b6f3856ca53339ab35e46873d5f47522a6313`，测试 SHA-256 `197d4d1fd18f1397c45d87f9d2565a4b54cadbf0be1d613b04ac26f41c0348cc`。这是现有受信组件的独立问题，不能为使加载工具验收全绿而修改钉定分类器或调整预期。本次加载组件验收不覆盖该缺陷修复，也不证明受影响分类场景安全；修复需独立追踪、更新受信版本并重新分类，旧结果不能改写。

## 5. 保留的能力限制

工具没有理解/持续保有/注入模型的证明能力；仅识别日志暴露的上下文恢复事件。本地日志可审计但不是防篡改认证；只验证过本文 Codex 返回形制，其他宿主字段未知时报 UNAVAILABLE。语言、方向、场景、系统及 Controller 资料仍按原规则加载，不在首版覆盖内。

人工与工具比较只有四个场景、同一开发 Agent、未独立计人工时，不据此报告加速比或整体错误率。全量转换效果、样本编译/行为、VM 隔离和平台部署均未验证。已有其他未提交目录不纳入本轮交付，不撤销、不清理。
