# E前半补读验收，独立小范围

用户授权DeepSeek harness全量并行静态审阅，Codex验收。工作区E:/桌面文档/Agents System/code_convert，遵守AGENTS.md和code-convert发现入口。纯文档，不转换不运行；不辅助脚本、不ACL诊断/修复、不权限修改、不.env/密钥、Controller/jobs，不原证据改写。只用原生read/glob/grep，报告write；shell工具已停用，单行读取上限1048576，glob不抽样。

你是新的独立补读会话，只负责D2-278至D2-289共12项，每项实际目录见根docs/dataset-2/dataset-2-copy/manifest.csv。旧E会话已打开各项15件，但源证据/closure单行被截断；你不能照信旧全文完成声明。**每项亲读完整returned-evidence/evidence-source.json、closure.json、batch/items/<Id>.json三件原文**（共36件）。如证据指针/占位异常需额外读该项report/result/metadata，禁止用别项猜本项。

输出一个独占文件docs/dataset-2/dataset-2-copy/batch/current-system-review-2026-10-12/harness-e-check-01.md。逐项列三件真实完整路径、工具全文读取是否截断/成功、build status/exit、execution status/exit/timedOut、stdout/stderr实际内容/尺寸/digest/truncated、observations/output和限制、collectorDiagnostics、baseline身份和profile关联、closure完成/清理/oracle/provenance/所列制品、item状态是否与原件一致。不计算哈希不更改原verdict；不从collectorDiagnostics=[]推无采集问题、不把output.events=[]当stdout空、不从closure摘要证明远端制品仍在。源/目标已删的限制保留，只有源build/run不等转换完成。

不要重复读取长旧审查报告来消耗上下文。先逐项读三件并立即记录；文件有错继续读完剩余项并列具体缺口。12项全部36件亲读完成才COMPLETE，最后列已读件数、未读/截断集合及新事实。缺件如实记录，与现存未读分开，不伪造。其它组及其它报告不改。
