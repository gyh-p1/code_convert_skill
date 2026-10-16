# 评估系统可达性分支：交付与加载一致性审查

审查日期：2026-10-16。对象为本仓库当前工作树的 Markdown Skill、登记加载工具及文本回归；不是样本转换报告。审查记录和原始检查结果保存在本目录。

## 1. 结论速览

不可达分支已纳入同一份交付契约，明确目录、适用件、报告和恢复要求；不复制出另一份 delivery-handoff-contract.md。两种情况下均加载七份核心契约，按任务形态另加载批量/长文件工作流；可达性只改变动态步骤的适用性。登记加载器实现保持不变，补充说明、三项回归及测试文件登记摘要。最终结构检查 PASS，53 项文本回归全部通过。

本结论限于当前工作树的文档一致性、静态加载路径和加载工具文本回归；未证明真实转换效果或任意 Agent 的实际遵守情况。

## 2. 文件变化

- [交付契约 §2.1.1.1](../../../../../references/framework/delivery-handoff-contract.md#2111-不可达仅转换的产物骨架)归档不可达产物骨架：冻结/检查/分类、模型与自审原件、最终 target、result.md、适用长文件分析及按需 manifest。未发生评估不创建 job/comparison/closure 占位；已有真实失败及未决执行保留。
- [加载说明 §4.1](../../../../../tools/README-loading.md#41-可达与不可达两条路径的加载动作)列出两条路径的既有动作。加载器不检查网络、源构建或 job，不要求前一动作已执行，也不据模式开关减少正文覆盖，故无需修改实现或新增加载字段。
- 根入口、发现入口、状态/闭环、Controller/runner 适配及批量/长文件工作流消除读取时点歧义：先读离线适配与登记坐标，再检查可达性；实时平台/runner/工具链证据仅用于可达时适用的源预检/评估，不阻塞具备文本条件的不可达生成。
- 全文搜索发现的 15 处旧门禁页脚已同步修正（6 个方向、4 个场景、5 个系统页），仅改执行路由，不改语言映射语义。行为指导、索引、交付通用核对也明确分支适用性。
- `tools/test_loading_preflight.py` 新增三项回归，`tools/loading-registration.json` 更新对应 SHA；`tools/loading_preflight.py` 仍为 1.0.0，字节身份未变。`.gitattributes` 保护本目录证据的原字节，并将原始 CRLF 识别为合法行尾；暂存检查不改写日志或哈希。

历史 `docs/` 审查、已有评估证据及用户原有未跟踪材料未作规范性回写。

## 3. 两种路径的门禁与加载

| 对象/步骤 | 系统可达 | 确认传输不可达 |
|---|---|---|
| 七份核心契约 | task-state、classifier、build、loop、evaluation、delivery、safety 全读 | 同样全读；build 用于计划与待核验范围，不要求构建原件 |
| 语言与方向知识 | 源/目标语言页及一个方向必读；场景/系统/专题按源码触发 | 相同，不因无编译而减少语义知识 |
| 批量/长文件 | 按形态加载，可叠加 | 相同；逐项推进、全文件/跨单元自审、40 项对账继续适用 |
| Controller 适配 | 健康检查前读离线连接/协议/能力/比较适配；适用提交前核实时条件 | 同样读离线正文，实时条件记未核验，不伪填隔离 |
| 冻结、分类 | 冻结写出回读，分类 ALLOWED/null | 相同；分类入口缺失/BLOCKED 仍停止生成并交报告 |
| 源预检 | 生成前源 build completed/0 及适用清理；行为分支须有效源基线 | 不开展，不虚记 SOURCE_BUILDABLE |
| 生成、自审 | 配置模型生成、独立审阅请求及有限修订，留实际原件 | 相同；免动态验证不免自审或来源记录 |
| 评估与交付 | 按正常行为/LIB 分支核适用条件、证据及交付门禁 | 不编译、不运行、不提交；完整 target/self-review/result 及适用件齐备后 PARTIAL，未开展维度 UNVERIFIED |
| 异常与恢复 | HTTP 鉴权/忙碌/未就绪/协议问题按原准备规则；未知提交或清理未确认 WAITING | 不借不可达关闭未决 job；恢复重查，补适用源预检后验证已有目标，不重复成功请求 |

共享加载动作是 start、适用 map、freeze、classify、generate、review、close，恢复前 resume；可达时另做适用 source-precheck/submit。动作加载 PASS 始终为 loading-only、executionAuthorized=false，不是分类、安全、构建或终态放行。

## 4. 验证依据与覆盖范围

| 检查 | 实际结果与证据 |
|---|---|
| 登记结构检查 | `python -B tools/loading_preflight.py check-repo --repo . --out <本目录>/structure-002.json`：PASS，findings=[]；[最终原件](structure-002.json) |
| 登记文本回归 | `python -B -m unittest discover -s tools -p test_loading_preflight.py -v`：53 tests / 28.811s / OK；[最终日志](loading-tests-002.log) |
| 两路径加载反例 | 4 种任务形态 × 两条动作路径；不提供源构建/job 仍可完成加载检查；缺任一核心契约、适用 batch 或 long-file 仍 FAIL；所有 PASS 均不授权执行 |
| 全文主题一致性 | 对 AGENTS/README/根入口、隐藏发现入口、references、skills 和 tools 加载说明搜索源构建/源预检/可达性/实时证据/平台身份/产物骨架，并回读相关上下文；[最终搜索记录](consistency-search-002.log)保留命中，不以命中数证明一致 |
| 旧措辞核对 | 同范围搜索“三道硬门禁”、无归属的“不可达仅转换按 §1.0/不可达按 §1.0”，无命中；可达分支中的 ALLOWED→源预检仍合法保留 |
| 链接与覆盖边界 | 工具检查 3 个入口、7 份契约、2 个工作流的范围内路径/锚点；人工另核新增 health、不可达产物骨架、加载动作表的标题和相对链接，并核 15 个页脚均回根入口。工具明确不覆盖语言/方向/场景/系统/Controller/模型注入，不宣称全仓所有链接已自动校验 |
| 差异格式 | `git -c core.safecrlf=false diff --check` 及包含归档原件的 `diff --cached --check`：退出码 0，无输出；证据目录保留原字节并识别 CRLF |

`structure-001.json`、`loading-tests-001.log` 及 `consistency-search-001.log` 保留为中间审查记录；最终结论使用 002 原件，不覆盖历史。

SHA-256（精确文件字节）：

| 文件 | SHA-256 |
|---|---|
| `structure-002.json` | `9d2108643c73233c82fd9810c5907422e83ef524a6c8f955c1304ed173b83761` |
| `loading-tests-002.log` | `ad53979ddf2d9dfc9b567006583a3e7c5bed9e7c5a67480aa55d64d304bd5697` |
| `consistency-search-002.log` | `4940c15cf6814b9e7a58cd3a2db50239a7bacbf09e6e53f58dc7142f849a8b8b` |
| `tools/loading_preflight.py` | `58e334711d65456c3da6560a98b4de60c64f031eed688769f0eca4bd1f1e1217` |
| `tools/test_loading_preflight.py` | `8ba3168a06c7d36f25670425daa6d679a172813ac8440ffc5281c93038e08647` |
| `references/framework/delivery-handoff-contract.md` | `56b5295b97055e192bbf7d66d23065872dea467bc1260d0560c651616acac31b` |

## 5. 未决问题与下一步

本轮未探测真实第三方系统、未调用配置模型、未开展源码/目标编译运行或 job 提交，也未访问 Controller 安装目录。文本 fixture 的两路径加载检查不等同于真实不可达故障演练、真实分类可用性或端到端转换验证。后续实际任务仍须逐项保存真实可达性、分类、生成、自审和适用评估/交付证据；若分类入口也不可用，按既有分类门槛停止生成并交报告。

在本次文档及登记加载工具审查范围内，未发现尚待修正的分支门禁/加载冲突。
