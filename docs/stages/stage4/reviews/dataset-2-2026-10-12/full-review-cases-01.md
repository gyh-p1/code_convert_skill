# 全量工程产物审查：逐项记录 01

> 按 manifest 顺序推进，不是抽样。只有下表列出的项完成了所存过程文件正文审阅；不向未读项外推。源/目标、capsule 和部分模型原响应已不在副本中，缺件是当前审阅限制，不据此追改历史交付状态。

## D2-001 / cpp-to-c / chunked_manifest_exfil

本项目录34件全部正文已读（包括两份 model.json，它们实际是元数据而非响应正文）；另已读 manifest 对应行、batch/items/D2-001.json 与此前登记的 self-review-1.json。覆盖清单：

- 01-frozen：frozen-inputs.md、classifier-input.json、classification-1.json。
- 02-conversion：request.system.txt、target.gen.model.json。
- 03-self-review：review.system.txt、self-review-1.json、self-review-1.model.json。
- job-00-source-buildability：input_profile.json、comparison_manifest.json、metadata.json、job-id.txt、controller-health-before.json、runners-before.json；returned-evidence 内 source/target 证据、comparison、JSON/Markdown报告、controller.log、controller-health-after.json，共13件。
- job-01-dual-build：input_profile.json、comparison_manifest.json、metadata.json、job-id.txt；returned-evidence 内 source/target 证据、comparison、JSON/Markdown报告、controller.log、controller-health-after.json，共11件。
- 根层：result.md、evaluator_manifest.json。

### 原件支持的发现

1. job-00 使用占位 target 而且实际运行双侧，平台 mismatched 来源为源 missing_bundle JSON 与目标空输出；不是转换失败。现行 source-preflight 已支持 source-only，旧装置问题不再提出新增占位机制。
2. job-01 两侧 build completed/0，execution completed/0，外层观察 stdout 为驱动 JSON：`case、exitCode、stderr、stdout`；内层程序 stdout 是 JSON **字符串**并带 `\r\n`。两侧外层148字节相同，comparison matched，双侧cleanup PASSED。这支持冻结 missing_bundle 路径通过，不支持发送路径。
3. profile 的 json-structural 解析的是**驱动封装**，未递归解析其中的程序 stdout JSON字符串。键顺序/程序换行等跨语言差异会留在字符串内；外层结构相同也不能证明封装忠实。评估优化应区分装置观察与程序观察，按已提供驱动的精确协议提取/分类，保留原封装和程序原流；不能猜测并任意递归解析一切字符串。
4. frozen 记驱动 timeout=60，profile timeoutSeconds=30；驱动正文已删，不能复核实际内层60是否生效。超时关系及实际argv/cwd须由提供者版本/回传支持，不能只记文字。
5. frozen 列出8份知识及哈希；request.system 只给摘录，model元数据给 system/user/rawResponse 哈希，无原user正文、原响应或知识片段映射，无法核实8份知识全部进入模型。现行知识消费契约已区分可达、已读、注入、效果；本历史项只能记可追溯性不足，不能用当前页反推历史注入。
6. item 记failedAttempts=1、result描述请求体UTF-8错误，但目录未见该失败attempt原件；model元数据的rawResponseSha256不能代原响应。统计保留“历史报告一次失败，副本原件缺失”，不擅自清零。
7. evidence baseline artifactHash 是目录/制品哈希，metadata sourceHash/targetHash 是单文件哈希，值不同本身不是错。缺capsule/树清单时，不能仅凭不同值断言版本错，也不能视为关联已核实。toolchainFingerprint={}，health只报1.0.0及contractSetHash，不足以确定具体产品修订身份。
8. result把OOM差异称为环境性极端路径：源异常终止，目标继续发送部分数据并报告更少bytes。这是候选转换语义差异，**触发条件是资源不足，不等于origin=environment**。本次未运行该路径，不能判已证实缺陷；知识应区分触发条件、差异归因与冻结覆盖。
9. evaluator manifest 的success=true/hasSource=true/hasTranslatedCode=true/hasReplayArtifact=true为历史交付声明；当前副本删去了相应正文/zip，链接仍指docs/test旧路径。历史记录不改，审阅可交付性与历史交付声明分开。
10. `coverage=100%`只表示1个适用观察维度被采集，三条主要路径中仅missing_bundle被观察。统计保留维度覆盖、路径覆盖和义务覆盖的分别说明，不能将100%写作完整功能覆盖。

### 优化去向

- 知识：沿用自审登记K-C，并补记“极端触发条件不决定origin”；其当前知识真源覆盖尚需逐条对照。
- 流程/契约：现行源预检与知识消费已解决机制方向；待核实际落实。失败原件、精确驱动引用、timeout层次、制品与文件哈希关联仍是审阅要点。
- 评估：合法驱动封装下的程序流分离、内层结构化比较与程序输出来源证明；应在冻结协议下消费，不通过泛化ignore掩盖真实程序差异。

本项保存原matched；审查认可“missing_bundle冻结观察范围通过”，发送/no_receiver/OOM等仍UNVERIFIED。未编译、运行、重评或恢复已删代码。

## D2-002 / cpp-to-c / elevation_probe

目录28件全部正文已读；另已读manifest对应行与item。01/02/03和根层共10件；job-00共7件（6件输入/health/runner材料及source证据）；job-01共11件。正式自审正文已在第1组登记，其余以确定排序分段读完，无工具截断遗漏。

- job-01两侧build与execution均completed/0，两侧外层stdout149字节，内层 `is_elevated=true,action=check_only` 相同，matched，双侧cleanup PASSED。可接受冻结成功查询路径通过。
- job-00仅保存source证据，无本job报告、清理、comparison、target证据；不能从job-01清理倒推job-00清理，不能因目录形状看似同001就假设相同。历史源构建0有证据，但该预检清理在副本中不可核实。
- 同为外层驱动JSON而程序JSON在stdout字符串内，适用001提出的协议解析/内层规范化问题；timeout60文字与profile30仍不一致。
- 分类requiresSyntheticData=true由TOKEN_QUERY敏感词触发，但任务只是自身令牌只读查询，credentialFindings=[]。候选分类优化应细分只读权限观察与真实敏感数据访问；不能仅因报告说不需要合成数据就删除分类原件。
- `is_elevated`是本项业务输出，不能因它依赖环境就全局消噪掉。环境同权限上下文应一致；有差异时先核上下文，再判断转换映射。当前成功值不能证明两个API失败路径及非Windows分支。
- request只列摘录；model只有元数据。知识实际注入和精确源/目标关系仍受原正文及capsule缺失限制。manifest的success/has*是历史声明，与删后副本可检查性分列。

## D2-003 / cpp-to-c / env_discovery_report

目录43件全部正文已读，另已读item与manifest对应行。覆盖01/02/03全部、job-00、job-01含attribution、job-02、根result/manifest；按路径排序分段完整读取，包含失败/装置attempt。

- 源预检build completed/0；其report记双侧cleanup PASSED。job-01 output matched，filesystem唯一major差异确为program.exe（源265204B，目标146597B、digest不同）；业务文件两侧272B且digest相同。job-02将范围`**/*`收窄至`out/**`，两侧output+filesystem matched，cleanup PASSED；旧mismatched原件保留，源/目标metadata哈希未变。该重评不计转换修复或新增用例。
- 这支持“构建二进制不应按业务副作用字节比较”的宽泛消噪方向。但简单只观察已声明路径会失去**发现目标新增未声明副作用**的能力。更好的评估准备/采集是区别构建阶段与运行阶段基线及装置文件，业务比较范围与越界副作用检查分别保留；不能全局忽略exe/pyc（业务本身可能产出这些文件）。本审查不新增驱动或触发运行。
- 程序报告JSON文件仅有size/digest，无文件正文/structuredSummary。可证明本观察字节一致，无法从回传核对环境值合法性/字段语义；将来跨系统环境值消噪需有结构化原件和明确映射，不能只凭digest不同忽略全文件。
- frozen/request记“上限1000”；review.system和自审指出实际`++topItems; if(topItems>1000) break`可达1001。request的人为行为摘要可能比源更严格并诱导错误转换。知识候选：保持条件、计数与break先后次序，规范值不能代替源码边界。当前实测4条不能验证1000/1001边界。
- 自审“只有3层以上才会失败”是对本实现调用序列的概括，不能作为mkdir一般规则；相同路径文本在父目录已存在时可创建末级。保留事实条件，避免把错误泛化纳入知识。
- 自审发现mkdir失败返回值被忽略与源异常终止不同，报告只写默认成功条件未阻断。记录候选差异及未覆盖，而不是以NO-REPAIR或当前文件匹配解除全部异常路径义务。
- “禁止全范围filesystemInclude”在旧报告仅写本项attribution，不是所有新任务会读的规则真源。当前契约如已要求限定范围，也仍应兼顾新增副作用观察，避免把历史装置经验扩大成盲区。
- 驱动封装/timeout/模型原响应与知识注入追溯限制同001；不重新把这些重复现象计作独立根因。

## D2-004 / cpp-to-c / fake_cred_loader

目录37件全部正文已读（含首次BLOCKED分类、2轮自审、修复请求与元数据、2个job全部现存文件）；另已读item与manifest对应行。

- 首次分类source_hash_mismatch得到BLOCKED；后续classifier-input和classification-1使用正确64位哈希并ALLOWED。**frozen-inputs.md仍保留漏字符的错误hash** `...a863eceab7...`，而正确值为`...a863eceeab7...`。不是仅有已修正的分类attempt：冻结正文未同步修正，报告“与manifest相符”不成立。现行冻结回读/动作前核对规则已覆盖此风险，历史项不能说该落实已核实通过；不改原冻结记录。
- request.system及review.system把getline阶段保留CR的语义直接当作Windows文本ifstream输入语义；还称C getline同样丢弃LF，混淆不同API契约。自审1正确区分Windows文本转译与二进制读取，提出rb→r，修复模型元数据有parent/final哈希与1行改动说明；复审支持反例3/3。该知识必须连同OS、运行库、打开模式、分行API分层解释，不能仅给“去掉CR/LF”的口诀。
- job-01 metadata目标哈希为修复后9867…版本；两侧build completed/0、execution completed/0，stdout112字节、missing文件loaded=0相同，matched、双侧cleanup PASSED。**CRLF/空行修复仍无行为验证**；静态修复证据与冻结场景通过分别统计，不把matched当“缺陷已动态验证”。
- job-00报告支持源build0及双侧cleanup PASSED；占位target比较mismatched属旧预检装置，现行source-only机制可避开。
- 最终result虽§4/§5明示未运行修复路径，§3仍标题“真实缺陷，已修复”。优化写法应为“已按定位建议修订，静态复审未见残留；修复路径行为UNVERIFIED”，避免读者只看标题便外推。
- 模型元数据4次调用与item请求数4对应；原完整请求/响应缺失，不由哈希替代。旧manifest删除后副本限制及封装/timeout问题同前。

## D2-005 / cpp-to-c / local_c2_ping

目录31件全部正文已读，另已读item与manifest对应行：01/02/03、job-00及job-01全部现存材料、result/manifest。

- job-00源build0且report双侧cleanup PASSED，旧占位target比较mismatched不记转换失败。job-01双侧build/execution completed/0、stdout141字节一致、no_local_c2路径matched，双侧cleanup PASSED。
- 固定合法127.0.0.1的inet_pton→inet_addr有静态理由，但不能泛化为所有地址/错误处理同义；成功send/recv、含NUL回显、WSAStartup失败及非Windows分支均未动态观察。宽泛消噪不能把未来通信端点/消息内容差异吞掉。
- frozen记“未启动接收端所以必然失败”。未启动本任务接收端不等于已证明端口没有其它监听；历史真实观察是失败路径，足以限定本次比较范围，但未来条件须靠隔离环境/提供者真实初态证据，不能靠该逻辑推断。
- result宣称target47行，生成metadata记57行、1482B，且无修订。当前正文已删，不能定案哪个行数正确，交付行数与实际版本追溯标疑点；哈希c01c…在item/metadata一致只是声明关联，不代capsule树清单。
- 输入/模式、外层驱动JSON、timeout60/30及模型原件/工具链身份的局限逐项核过，同前。frozen所列selected skills未列两语言页，不能从方向页可达反推本轮已读/模型已注入。

## D2-006 / cpp-to-c / xor_codec_transform

目录31件全部正文已读，另已读item与manifest对应行：01/02/03、job-00及job-01全部现存材料、result/manifest。

- job-00源build completed/0，冻结命令无额外pthread库在本工具链确实可用；report记双侧cleanup PASSED。只可支持这条具体构建命令，不泛化为全部MinGW std::thread库无需链接。占位target的mismatched仍是旧预检装置结果。
- job-01双侧build/execution completed/0，stdout171字节一致、decode_ok=true与SAFE-MODE-VALIDATION-PATH相同，matched、双侧cleanup PASSED。该确定性常量输入不需要新增时间/随机消噪。
- 自审及report称“小输入所以OOM不可达”不充分：冻结没有提供保证分配成功的环境前提。正确记当前未触发/未观察；源异常与目标0退出候选仍保留，不要求为这项新增强制故障注入。
- toupper实参须避免负char的规则已有；request中“省略unsigned转换后所有0x80以上XOR结果都会不同”是另一个技术断言，不能因为目标保留源写法且默认ASCII通过就升级为通则。需精确整数提升、char表示/回写与实际目标实现依据。
- 当前常量程序无法仅靠fixture改变plain。旧report建议“把plain参数化”是新源码/接口变体，会改变任务；后续观察须由用户/获批平台提供合法入口或准确新样本，并重新冻结，Agent不能自行改源或生成驱动来验证库边界。
- split尾空/中间空/空输入及非Windows分支只有静态审阅。sleep40ms保留的文字/目标引用不等于本次真实时序证明；只有输出维度通过。
- 模型元数据/请求数对应2次，目标哈希d9a9…在item/metadata一致。删除后版本追溯、外层封装、timeout及工具链身份限制同前，已逐项核过。

下一项从manifest D2-007继续。当前连续完成6项、其用例目录共204件存留文件正文，不以这些项代替其余271项；96份自审覆盖与此计数存在交集，不能相加当作文件总覆盖。
