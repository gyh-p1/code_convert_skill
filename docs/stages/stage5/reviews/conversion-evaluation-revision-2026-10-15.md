# 转换与评估修订验收记录（2026-10-15）

> 后续提交状态：用户追加要求保持分类器准入语义后，已修单冒号hostname候选丢弃、方法名豁免和同文件跨语句消费者问题；单文件阶段68项分类器及31项平台准入测试通过。随后新增的双文件源集合测试仍有8条失败记录（含隔离开关/文件顺序subtests，完整自测共70项）；用户明确当前无双文件场景、停止继续收尾，随后要求两仓库先提交推送。本次按当前快照提交，不声称完整分类器自测通过，不实现、删除或跳过这些双文件用例。下文63项及源码哈希/归档属于此前精确版本，不能代表当前候选；追加原输出保存在评估仓库本地out/classifier-policy-followup-2026-10-15。没有发布/部署或改变平台信任SHA。

> 状态：仓库规则/知识、分类器和评估源码修订及本轮维护回归完成；未发布/部署，未重跑数据集转换或真实VM/job。
> 对应[修订方案](../plans/conversion-evaluation-revision-2026-10-15.md)。报告事实按用户要求直接采信，本轮没有重做历史原始证据审计；工程验收记录不进入产品必读链。

## 1. 授权、范围与方案裁决

用户先确认此前审阅意见，要求先确定方案再持续修订；随后明确包含现有分类器和相邻评估仓库源码，最后明确授权“允许仅这轮维护测试在本机运行”。该限定例外只覆盖现有unittest/pytest及既有无害临时文件/进程fixture，不覆盖数据集样本、正式模型调度、转换job、现役Controller或部署。没有修改永久执行红线以扩大授权。

保留开始时已有的未提交文件：转换仓库的stage1部署/任务记录、remote-controller-adapter、runner-capability-matrix、评估准备/构建前提/C#页及已有stage4/5资料；评估仓库的README、Agent main/observations及其测试。对重叠文档只增量补本轮内容，不重写原job/items/events、原缺陷报告或历史测试结果。

采纳“已知缺陷与评估范围分别处理、修复保留源行为、先有效性再比较、观察对象/范围明确、知识归真源”。未采纳“全部REPAIR都修”“命中必须>0”“整类忽略State/counter/stderr”“所有项强制三OS”“Agent新写驱动/比较器”。比较器源码在既有评估系统中修订，不在转换仓库新建运行时。

## 2. 需求到实际交付

| 需求 | 实际落点与验收结论 |
|---|---|
| C1 已知缺陷不被oracle等理由关闭 | 闭环§1/§3.1/§4、评估准备§4/§5、任务状态§2.1、交付§2.3、发现/根入口/AGENTS和两工作流；明确有限修复、预先许可例外、未修复/修后未验证分别交付。静态定位路径的反馈清单已条件化，不伪造动态反例 |
| C2 修复不能绕过源行为 | 闭环§2/§3.2/§5、行为指导§5及长文件§4.1；核源条件/调用/失败路径→父稿错误→修改→保持依据→待验证范围。不增加无限自审，合法内联/重命名仍允许 |
| C3 知识补齐 | C注释定界、C++ getenv/存在谓词、Ruby ENV/对象类型、Python ctypes、PowerShell类内名称、C#抽象成员、身份系统的描述符/ACL、网络统计范围和共性导航；旧参数下标/常量/标签等已有充分正文不重复新增 |
| E1 有效性与预检 | 评估准备和适配保留source-only/占位目标排除、真实执行来源、exit97只是线索；源码链已具备独立源预检，本轮不重复实现。没有可信驱动失败协议时不根据文本猜失败 |
| E2 观察设计 | 任务状态/评估准备、文件/网络知识：对象/接口集合/范围/单位/窗口先对应；独立同态cwd、环境继承/空值及副作用实际维度，边界输入按源触发记录覆盖 |
| E3 比较能力及保护 | 评估准备§5.1、比较适配§2.2/§2.3/§7和既有比较器源码；忽略项端到端消费，新token显式启用，默认保持，原件不变，单位/host/重复身份受保护，无整类State/counter/stderr豁免 |
| E4 §1.3仅编译 | 已有规则明确，保留全部前提/报告/目标验证义务；补消费而不另造同义门禁，不由缺入口跳过源构建已过的适用生成 |
| E5 准备与分类 | 构建前提补同源/候选证据边界及GenerateAssemblyInfo；分类准入保留正规重分类/钉SHA。v2.5候选修无效IP与精确元数据上下文，真实网络反例和原有凭据门禁仍测试覆盖 |
| H1 交付与统计 | result五栏目补已知未解决问题槽位；任务状态/批量按问题分别归因，按taskId计项，matched不消除覆盖外误译 |
| L1 加载链 | 下节实际穷举66份skills Markdown并逐页核路由/相关规则，另核发现、AGENTS、根及本轮契约/适配链接；修掉“登记降级即可继续”及历史状态固化残留 |
| S1–S4 实现与验证 | 两仓库实现/测试及适配同步；分类器63项、比较器单文件162项、评估完整套件712项通过。单文件162已包含于712，不重复计总数；候选尚未发布/部署 |

## 3. 实际修改文件

路径均相对转换仓库，以下是本轮范围，不将开始时已有其他修改算成本轮产出：

- 入口：`.agents/skills/code-convert/SKILL.md`、`AGENTS.md`、`SKILL.md`。
- 契约：`references/framework/task-state-contract.md`、`evaluation-readiness-contract.md`、`delivery-handoff-contract.md`。
- 工作流参考：`references/workflow/conversion-evaluation-loop.md`、`behavior-preservation-contract.md`、`build-prerequisites.md`、`classifier-agent-gate.md`。
- 适配：`references/adapter/controller/comparison-policy-adapter.md`、`platform-revision-adapter.md`。
- 共享知识：`skills/references/seven-language-common-semantics.md`，`skills/references/languages/{c,cpp,csharp,powershell,python,ruby}.md`。
- 场景/系统：`skills/scenes/{file-io,network-io}/SKILL.md`，`skills/systems/{posix-windows-process-identity,posix-windows-threads}/SKILL.md`。
- 方向：`skills/directions/{c-to-python,cpp-to-c,cpp-to-csharp,csharp-to-go,go-to-c,go-to-csharp,powershell-to-ruby,python-to-cpp,ruby-to-c,ruby-to-cpp,ruby-to-csharp}/SKILL.md`。
- 工作流Skill：`skills/workflows/{batch-conversion,long-file-conversion}/SKILL.md`。
- 工具及现有自测：`tools/safety_classifier_v2.py`、`tools/test_safety_classifier_v2.py`。
- 本工作包：stage5 README、本方案、本记录；未实施原Stage5拟议载入检查器，没有新增辅助脚本。

相邻评估仓库的本轮文件：`packages/evaluation-core/evaluation_core/evidence_comparator.py`、`tests/test_evidence_comparator.py`（位于该包内）、`README.md`及[评估修订记录](../../../../../third-party-evaluation-system/docs/defect-review-revision-2026-10-15.md)。未修改其默认SANCTIONED_CLASSIFIER_SHA256，现役信任不因源码候选变动。

## 4. 加载路径回查的真实范围

先用原生rg --files穷举，不以历史42/9数量代替磁盘。实际skills下66份Markdown：54个SKILL.md、9个共享参考、3个随附页；再核3个主入口。下表展开所核对象，结果是本轮规则的路由/边界与相关语义检查，不是全部技术事实逐字审核或所有历史链接的机械验收。

| 对象前缀 | 已逐页核对的身份/范围 |
|---|---|
| directions/c-to-* | cpp、csharp、go、powershell、python、ruby；各页根路由、语言引用、验证边界及相关差异/门禁段 |
| directions/cpp-to-* | c、csharp、go、powershell、python、ruby；同上 |
| directions/csharp-to-* | c、cpp、go、powershell、python、ruby；同上 |
| directions/go-to-* | c、cpp、csharp、powershell、python、ruby；同上 |
| directions/powershell-to-* | c、cpp、csharp、go、python、ruby；同上 |
| directions/python-to-* | c、cpp、csharp、go、powershell、ruby；同上 |
| directions/ruby-to-* | c、cpp、csharp、go、powershell、python；同上 |
| scenes | network-io、file-io、process-execution、concurrency：加载前置、真实行为义务、条件oracle/仅编译与根/安全回链 |
| systems | posix-winsock、posix-windows-filesystem、posix-windows-process-identity、posix-windows-threads、windows-registry-service-subsystem：同上及适用修复/差异段 |
| workflows / attack | batch-conversion、long-file-conversion及attack-tactic-index：加载时点、门禁/收尾/预算、离线分类边界 |
| references/languages | c、cpp、csharp、go、powershell、python、ruby：入口/证据边界与本轮触发语义段；common导航全文，security行为义务/离线边界 |
| 随附页 | c-to-cpp/references/type-abi.md、header-macro.md及network-io/references/security-behavior.md全文；前两者由方向条件加载，后者是兼容入口，不单独授权推进 |

42方向均能回根和安全边界，场景/系统均保留前置与不替代门禁说明；不在每页复制新契约。主干按发现→AGENTS→根→适用工作流→各真源→适配回查。新相对路径/锚点人工按正文核对，先排除代码块与行内代码；CPP06、PY15、C/PS/C#章节、网络统计、比较§2.2、闭环§3.1和交付§2.3均有对应现存标题。

独立审阅与进一步语义搜索发现并修正：GO-CS路由/超时/近似、RB-CS文本规范化、NET集合/FILE归档、线程同步、其余方向的“声明降级”捷径；GO-CS示例改局部候选，CS-GO不再把UTF16单位直接改rune/byte。C→Python、C++→C、Go→C不再把历史未验证状态固化为新任务结论。所有修订后定点复核未留必须修改的问题；未审的全量技术事实仍不宣称正确。

## 5. 纸面情景及源码独立审阅

修订前先以报告的既有失败作输入，再由只读智能体核8情景的现有规则；这不是实际转换压力实验。修订后逐项核：oracle受阻但已确认参数误传；硬编码删调用；未设置/空串和exists/目录；占位目标/合法exit97；不同计数范围；服务态/stderr业务保护；缺入口§1.3；候选OS遗漏。均能从真实入口到达对应处理规则。

实现由另一个只读审阅者检查stream→output→bundle、分类器词法/准入、默认策略和跨流身份关系。其指出的普通xmlns变量豁免、namespace URI内IPv4重扫、紧邻单位、data-xmlns/其他属性值内xmlns四类问题均修正并补回归；最后一类先实际复现2失败再修复。审阅不是运行证据，测试结论只据下节命令回传。

## 6. 维护回归与精确版本

运行时复用评估仓库现有`out/release-venv/Scripts/python.exe`：Python3.12.13、pytest9.0.3，符合发布锁>=3.11,<3.13。没有安装依赖、调用模型、运行数据集样本或提交job。先基线区分，再当前定向、完整套件；最后分类器属性边界修订只重跑受影响分类器，评估源码此后未变。

| 测试 | 实际结果与证据 |
|---|---|
| 比较器旧稿＋新入口测试 | 3 failed、159 deselected，exit1；red-comparator.log/xml |
| 当前比较器单文件 | 162 passed，0.85s，exit0；comparator-final.log/xml |
| 当前评估完整套件 | evaluation-core/Controller/VM Agent/release共712 passed，71.35s，exit0；platform-full.log/xml |
| 分类器旧稿对照 | 初次标点fixture未区分旧稿，补精确endpoint上下文后60项产生7个失败记录（含subtests）；red-classifier.log、red-classifier-2.log均保留 |
| 分类器首轮及边界修订 | 60项通过后，新增属性边界用例实际63项中2失败；修正后63项全部通过，exit0；classifier-final.log、classifier-attribute-red.log、classifier-final-2.log |

162已包含在712内；63是另一套分类器方法数，不是转换任务数。日志中的合成分类准入百分比不作为转换成功率。基线测试是在用户许可后补做的区分验证，不冒称实现全过程先运行RED。stdout/stderr经PowerShell终端文本采集，部分旧失败路径显示有编码替换，原日志保留；不称程序原始字节取证，JUnit与已知精确路径另可核对。

原件在[评估仓库本轮证据目录](../../../../../third-party-evaluation-system/out/defect-review-tests-2026-10-15/)，被Git忽略，不能以文档代替原件交接。旧稿归档、最终实现/测试归档及实际平台树一起保留，不把HEAD当未提交工作树身份。

| 对象 | SHA-256 |
|---|---|
| classifier v2.5候选 | ABE35081063CD9F5F69ED3063D92A24FD1E184BD42E5E15EB2FA7389BFA2DB08 |
| classifier自测 | A11D3D1E9B84D9FA2F8CA8E4C52D36E9DC7927744A501199263F63EFA79C38B9 |
| evidence_comparator.py | CABD236C5B4F4CF7FD72E02712D95AA543482822AE921F46ABF919E33B817DA6 |
| comparator自测 | 2B9397D185F292D81E954232678D258D1B77A12EFACB139002877415FF5F3DC2 |
| tested-sources.tar（4文件） | C195E3D40593541AED0488DA5320E014452264E15B83D51CF95049146B69AC16 |
| tested-platform-tree.tar（apps/packages/tools/infra） | 2C0253E7B856E116F165D41BDA94287DB38D34D286D25F2BA6061A55E2566FEE |

平台树归档包含开始时已有源码修改，排除缓存/pyc及潜在凭据模式；原生文件名搜索在所选目录未发现.env/pem/key。baseline来自转换HEAD `120d592c95984cc1cdd6009e2c0dbc1e9c2ab337` 与评估HEAD `3c136b074466c54daad85034379396135a924765`；同条件基线及旧测试文本归档均保留。

## 7. 未验证与操作边界

- 维护回归支持本次源码/合成fixture，不证明42方向、全部历史40项或真实攻防场景转换效果。没有修订历史target、重写原判或凭当前知识回填历史模型注入。
- 分类器v2.5尚未发布及纳入平台信任SHA；默认仍v2.4，不用新候选冒充已登记版本放行。发布/信任登记与真实隔离验收另有审批流程，本轮未执行。
- 类型化规则是有限显式能力；不推断所有端口动态，不默认忽略业务服务态/计数器/stderr，不新增独立驱动来源协议、collector或隔离证明。无法证明来源的旧观察仍保留UNVERIFIED。
- 临时基线目录已确认在`C:/Users/86135/AppData/Local/Temp/cc-review-20261015-01a13daa-baseline`。递归清理被自动审批拒绝，仅返回blocked by policy；两个分类器脚本副本已用精确路径单独删除。其余已归档的基线包/解包目录保留待人工清理，不通过其他shell绕过拒绝。
- 两仓库最终diff、空白、必要相对引用及源码身份已在收尾回读；没有推送、提交或改部署。

## 8. 维护侧出处核对

必要语义已写入产品本地正文，不把以下网页作为调用方依赖。本轮维护参考Microsoft Win32 [AccessCheck](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-accesscheck)、[GetNamedSecurityInfoW](https://learn.microsoft.com/en-us/windows/win32/api/aclapi/nf-aclapi-getnamedsecurityinfow)；Ruby3.4 [ENV](https://docs.ruby-lang.org/en/3.4/ENV.html)、[File](https://docs.ruby-lang.org/en/3.4/File.html)；Python3.12 [ctypes](https://docs.python.org/3.12/library/ctypes.html)；.NET8 [Stream源码](https://raw.githubusercontent.com/dotnet/runtime/v8.0.0/src/libraries/System.Private.CoreLib/src/System/IO/Stream.cs)、[GenerateAssemblyInfo](https://learn.microsoft.com/dotnet/core/tools/csproj)；PowerShell [类属性](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_classes_properties?view=powershell-7.6)；psutil官方Network接口说明。C++ exists依据项目既有C++17条款和报告事实，当前工作草案仅作语义交叉参考，本轮未取得N4659 PDF新副本；不把当前草案版本当C++17效果证明。
