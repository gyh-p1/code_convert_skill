# E后半补读验收，独立小范围

用户授权DeepSeek harness全量并行静态审阅，Codex验收。工作区E:/桌面文档/Agents System/code_convert，遵守AGENTS.md和code-convert发现入口。纯文档，不转换不运行；不辅助脚本、不ACL诊断/修复、不权限修改、不.env/密钥、Controller/jobs，不原证据改写。只用原生read/glob/grep，报告write；shell工具已停用，单行读取上限1048576，glob不抽样。

新的独立补读会话，仅负责D2-290至D2-300共11项，实际目录按根docs/dataset-2/dataset-2-copy/manifest.csv。旧E已打开每项15件，但源证据/closure长单行截断，不能信旧COMPLETE。**每项亲读完整returned-evidence/evidence-source.json、closure.json、batch/items/<Id>.json三件原文**，共33件。占位/版本/回执异常再读本项report/result/metadata，不用别项猜本项。

只新写docs/dataset-2/dataset-2-copy/batch/current-system-review-2026-10-12/harness-e-check-02.md，不改旧报告。逐项列三件真实完整路径及读取是否成功/截断；build状态/退出、execution状态/退出/timeout、stdout/stderr实际内容/尺寸/digest/truncated；output观察与各限制、collectorDiagnostics；baseline和输入profile身份关联；closure清理/完成/oracle/provenance/制品指针；item记录与原件是否一致。源/目标已删的限制保留；只有源build/run不算转换完成，平台matched/semantic_pass只在适用真实冻结范围统计。

不要从空collectorDiagnostics证明采集器无问题，output.events=[]不代表stdout空；closure所列摘要不证明远端原件仍可取，也不恢复正文。不得算哈希或改原verdict、不得跑样本/提交/辅助工具。不要反复读长旧报告消耗上下文；逐项亲读三件即时记录。11项33件全读才COMPLETE，最后给已读件数、实际未读/截断集合、新事实。缺件与现存未读分开如实列。其它范围不碰。
