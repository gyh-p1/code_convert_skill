# E组验收退回与继续补读

继续同一E Session，仅D2-278至300实际23项。你的原COMPLETE声明因单行正文未全读被退回；目前工具上限已真实解除，应继续完成剩余原件，不能把“打开过文件”算已读全文。

请直接阅读harness-e-supplement-reread.md的未完成集合。其数字互相矛盾：§3写34件，§4写38件，表中列8件已补；有处又写D2-300 closure已读/未读并存。以真实read回执逐文件对账，不先猜数。把每个未补读的真实evidence-source.json和closure.json全文读完，更新补读表和coverage；零collectorDiagnostics仅支持未记录诊断，不能证明采集器没有失败；output.events=[]也不等于stdout没内容，真实stdout/structuredValue须另核。closure摘要支持平台记录制品，不自动证明远端正文仍存在，更不能恢复报告内容。继续核23项items原件，原任务明确要读，对它们“不改”不等于“不核”。不读batch/events或其它组用例目录。

不要重读整套长契约和已经完成的历史报告以消耗上下文；维持既有约束，直接补文件。官方启动patch保留readMaxLineLength/readMaxBytes/grepMaxLineBytes=1048576，并已停用bash/pwsh工具；只用原生read/glob/grep与报告write/edit。不得任何辅助脚本、ACL诊断/修复、运行/分类/转换/评估或Controller/jobs、.env/密钥访问。不要安装或改权限。

完整范围读完允许COMPLETE；缺原件照实记录审阅限制，不把不存在的应有件算待阅读，但现存正文未读必须PENDING。每件具体路径/状态明确，不能同结构代枚举，修正manifest/README相对链接为../../。可以用独占只读子会话分担剩余文件，但必须回收每件真实读取结果，不能只等子会话便终止父任务。继续完成再交验收。
