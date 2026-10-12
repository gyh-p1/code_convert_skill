# DeepSeek harness 并行审阅与Codex验收索引

> 用户2026-10-12授权多个DeepSeek harness会话审阅，Codex只负责验收。使用已安装官方dsh headless入口；每次调用形成持久化Session，stdout真实事件与stderr原件分别保存。未安装软件、未读取凭证、未调用样本/转换/评估运行时。
> 状态：本轮阶段收尾，未全量验收；用户最新确认现有材料足够，本轮不再补读。所有本轮headless调用已退出，当前状态见[收尾记录](phase-close-2026-10-12.md)。启动成功不等于审阅完成；DeepSeek报告标COMPLETE也须经Codex核覆盖及原件后才能记验收完成。

## 分工与全集

manifest有277在册项，编号001至300有23个移除项；不能用最大编号或区间长度作分母。原生rg逐范围计数核：6+73+79+62+34+23=277。

| 负责方 | 范围 | 实际在册项数 | 会话 / 事件原件 | 验收状态 |
|---|---|---:|---|---|
| Codex此前已读 | D2-001至006 | 6 | [逐项记录](full-review-cases-01.md)，各目录204件正文；与96自审集合有交集，不重复加计 | 正文已审，证据/删除限制如实保留 |
| Harness A | D2-007至080 | 73 | session-24fff24d-1f21-4de0-8567-71293f917140；harness-a.events.jsonl | 已退出；待读/截断及覆盖对账保留 |
| Harness B | D2-081至160 | 79 | session-fadb91d3-4c45-4348-aac7-2a4b01ad529b；harness-b.events.jsonl | 已退出；209件截断，19条计数差异未验收 |
| Harness C | D2-161至240 | 62 | session-cfd99848-0d46-4b9f-9b10-a9a90102e0e6；harness-c.events.jsonl | 已退出；剩余截断和统计矛盾未验收 |
| Harness D | D2-241至277及batch层原件 | 34 | session-0b5c874e-3b4a-4b28-b0e5-028d3bdde317；harness-d.events.jsonl | 已退出；声明正文已读，逐文件清单及结论待验收 |
| Harness E | D2-278至300 | 23 | session-641d2ec8-03e8-4ce7-997b-a31ab244f50e；harness-e.events.jsonl | 已退出；追加两个独立补读报告，未全组验收 |

A/B/C/D首批任务文字按编号区间长度写的74/80/80/37不是实际项数；此处根据manifest明确更正，任务范围不变，不重写实际已发送的用户请求事件。A已主动识别026移除。E补足最初分工未包含的278至300，未将漏分工说成已审。

审查总入口：[全量覆盖索引](full-review-index-2026-10-12.md)。96份正式自审正文登记属于已完成的独立阅读范围，各harness仍需核其原始响应/版本/独立证据，不靠既有登记跳过工程原件。

## 验收标准

1. 用manifest和磁盘完整清单逐项核分工全集与报告集合，缺项/额外项/重复项分别记录；batch根层、失败attempt和不在manifest中的原件也需去向。不能抽取几项通过便验收整组。
2. 各会话逐文件列真实路径及已读/空件/缺件/截断/未读，核harness的真实工具读取事件。文件名相似、schema重复或只有metadata均不授权跳过内容；模型reasoning不当结论。
3. 审阅结论定位回原件，源/目标已删的事实只到历史引用层。高影响优化逐条核当前规则/精确版本/双侧证据；错误建议拒绝固化，NO-REPAIR中的疑点保留。
4. 确认没有脚本/样本执行、转换模型调用、评估提交、Controller/jobs访问或凭证泄露。若harness尝试越界及时停止/纠偏；真实已发生事件保留不洗掉。
5. 知识、流程/契约、评估分层汇总，历史已解决、当前仍需改、证据不足和验证假设分别列；消噪保原件和关键义务，有效matched与semantic_pass的通过小计分列两类与覆盖。
6. 未完整覆盖/未核完关键结论时保持IN_PROGRESS/PARTIAL，不能发全量完成声明。不会用本机重算或修改平台原判完成验收。

## 后续记录

2026-10-12第一轮观察到harness原生read/grep默认单行2000字符截断。官方headless配置schema提供tool-fs的readMaxLineLength/readMaxBytes和tool-fs-search的grepMaxLineBytes，已编写仅供本审阅启动参数使用的声明式[harness-read-full-lines.patch.yml](harness-read-full-lines.patch.yml)，取1048576；没有可执行表达式、脚本、权限或沙箱变更，不改全局用户配置。活动Session不冒充已经消费新参数；待原调用退出后按准确Session逐个续接补读，真实事件另存。

- A/C/D/E首次headless已退出，已准确续接补读；真实事件为各自harness-*-followup-01.events.jsonl。A/C/D的新read回执及E的D2-278 closure证明长行上限真实生效。
- D/E的首次COMPLETE包含工具截断，**Codex验收不接受**；E补读报告已退回IN_PROGRESS，不能据进程exit0判完成。
- B首次事件call_00_CKPDDQMGbjrJP0htun1V1957尝试调用harness随附ACL诊断/修复脚本并申请danger-full-access；工具原回执为“requires approval, but no approval channel is available”，**被拦截，未执行**。原生命令核其输出目录E:/桌面文档/Agents System/acl-recovery不存在；不据此证明所有权限状态，只记录没有该次报告落盘。此尝试违反本任务仅审阅约束，不采纳，也不请求放宽权限。
- 本审阅CLI patch随后停用tool-bash和tool-pwsh（官方entryMetadata支持disabled布尔），保留原生文件工具与报告写入；不改用户全局配置和沙箱权限。活动旧调用不冒称已消费该更新，之后续接才适用。
- 原patch覆盖tool-fs-search配置时遗漏required的sampleOverCapGlobResults，followup-01及E-followup-02的stderr有该插件挂载ValidationError。read上限已生效，但当轮glob/grep不可用，不能把schema diagnostics=[]或headless exit0当插件运行就绪。已按官方config33 schema补sampleOverCapGlobResults=false及glob/grep全量上限10000、元数据展示1048576，随后调用再核stderr/真实工具回执；旧异常原件保留。

会话完成/需续接时，使用官方headless --session-id准确续接，不与同一活动Session并发写入。任务文本和每次真实事件分别留存，不写复用编排脚本。最终验收报告单独新建，不覆盖过程记录。
