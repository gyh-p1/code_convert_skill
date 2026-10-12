# 推进至R10的完成核对与停止记录

> 状态：COMPLETE（知识维护范围）。目标：持续推进到R10完成，然后标记已完成、停止并汇报。
> 2026-10-12：以当前磁盘正文核对R1–R10，不以此前汇总的“完成”标签代证据。本次补齐R10正文和导航，未继续处理R11以后事项；此前已有的其他改动保留，不撤销或混算为本次目标。

## 完成判据

R1–R10有实际知识正文及加载入口；R10七个子主题分别具备源API事实/版本前提、按消费者选择目标的引导、反例和未知边界。知识能离线读，不新增脚本、驱动、强测、自审轮数或模型调用门禁。按用户安排不运行转换、编译、验证回归或部署；完成不表示转换效果通过。

## R1–R9当前正文核对

| 项 | 当前证据与结论 |
|---|---|
| R1 | [PY-PS-06](../../../../../skills/directions/python-to-powershell/SKILL.md)当前示例写encodedBytes，保留Base64编码结果；区分ToBase64String/FromBase64String输入输出及BOM/换行。DONE |
| R2 | 同页PY-PS-05分直接调用LASTEXITCODE与Start-Process进程对象，按源选择忽略/传播/捕获；相邻03不强迫源静默路径打印诊断。DONE |
| R3 | [Go§九](../../../../../skills/references/languages/go.md#九标准库消费点的选择引导)明确map编码顺序与range不同，struct/tag/嵌入及自定义编码分别看消费者，Encoder终止符不套Marshal。DONE |
| R4 | Go§九的平台分支、[C++§八](../../../../../skills/references/languages/cpp.md#八库抽象替换的选择引导)的case/goto作用域、[Ruby§十二及§九](../../../../../skills/references/languages/ruby.md)的fork返回分别落盘，不按当前平台或真假值机械映射。DONE |
| R5 | [Python L1-PY-11](../../../../../skills/references/languages/python.md#l1-py-11-空白分行与制表列位置)区分str/bytes、分行集合、列位置及tabsize≤0删除TAB；错误建议未固化。DONE |
| R6 | 同页L1-PY-12按同端/两端操作判断容器顺序，保留pushback消费者，拒绝appendleft+popleft为FIFO。DONE |
| R7 | 同页L1-PY-10明确optparse的唯一前缀/歧义/缺参/诊断与prog，并按覆盖方法和源接受域选择，不套其他解析器。DONE |
| R8 | [文件场景](../../../../../skills/scenes/file-io/SKILL.md)当前归档及内容变换正文区分成员/CRC/内容与压缩字节、签名义务和合法依赖；不把存储块子集当通用能力。DONE |
| R9 | [进程身份系统页](../../../../../skills/systems/posix-windows-process-identity/SKILL.md)含环境块、可变长结构、容量、令牌及AccessCheck输出；[注册表系统页](../../../../../skills/systems/windows-registry-service-subsystem/SKILL.md)分原始/展开类型及处理顺序。语言页衔接实际ABI/API未知条件，不猜偏移。DONE |

## R10七个子项的实际完成证据

| 子项 | 正文与本次核对结果 |
|---|---|
| K-P：扫描上限 | [Go L1-GO-08](../../../../../skills/references/languages/go.md#l1-go-08-scanner-的停止边界与已取得结果)：默认64×1024缓冲边界及token/终止符区别、Buffer设置、Scan/Err、已得token、业务容量与目标接受域均明确。DONE |
| K-Q：用户后端 | [L1-GO-09](../../../../../skills/references/languages/go.md#l1-go-09-用户查询后端不等于环境变量)：多数Unix纯Go文件查询与cgo/libc、osusergo标签、查询API与ID/组/错误消费者分别保持，不用USER变量代结果。DONE |
| K-R：稳定排序 | [L1-GO-10](../../../../../skills/references/languages/go.md#l1-go-10-同键顺序依实际排序接口)：Sort/Slice与Stable/SliceStable分开，按Less及同键消费者选目标，不按一个样例或消噪改变排序义务。C++/Python现有选择引导互相一致。DONE |
| K-U：超时/等待 | [L1-GO-11](../../../../../skills/references/languages/go.md#l1-go-11-截止时刻取消与等待预算)：绝对deadline、零值/刷新、相对剩余预算、Context/WaitDelay/直接进程与管道排空分别明确；网络和进程场景仍管实际行为。DONE |
| K-W：双流合并 | [L1-GO-12](../../../../../skills/references/languages/go.md#l1-go-12-合流与部分读取的消费顺序)与进程场景：共同接收点的合流不是分别读完后拼接，不反向丢来源，不承诺并发跨运行固定顺序。DONE |
| K-X：临时目录 | [Python L1-PY-14](../../../../../skills/references/languages/python.md#l1-py-14-tempfile-的候选可用性与缓存)补具体候选、可创建文件的检查、缓存/tempdir/显式dir及str/bytes；回读Go L1-GO-07与Ruby L1-RB-09的不同规则，未互套优先级。DONE |
| K-Y：部分读取 | Go L1-GO-12区分n>0+error、两种EOF返回与0,nil；新增[GO-RB-08](../../../../../skills/directions/go-to-ruby/SKILL.md)对应Ruby正长度readpartial的块/EOFError与局部异常范围，并保留源主动丢弃数据的实际行为。DONE |

## 本次修改文件

- skills/references/languages/go.md：增加L1-GO-08至12具体引导，原概览保留。
- skills/references/languages/python.md：增加L1-PY-14具体临时目录事实，原选择点保留。
- skills/directions/go-to-ruby/SKILL.md：增加GO-RB-08部分读取映射，原错误和临时目录规则保留。
- skills/references/seven-language-common-semantics.md：新增对应导航，不复制事实或索引测试案例。
- 本审查目录：完成清单及入口/状态续接；不覆盖DeepSeek原报告、原自审或原平台证据。

## 资料与静态检查

维护侧读取官方资料后提炼必要语义到本地正文；网页只作下列出处，产品读取不依赖联网。

- Go标准库官方资料：[bufio](https://pkg.go.dev/bufio)、[os/user](https://pkg.go.dev/os/user)、[sort](https://pkg.go.dev/sort)、[net](https://pkg.go.dev/net)、[io](https://pkg.go.dev/io)、[os/exec](https://pkg.go.dev/os/exec)。bufio页显示go1.27.2，其余必要语义按对应API章节核对；项目基线1.27及资料可读均不证明未来任务的工具链已安装。
- [Python3.12 tempfile](https://docs.python.org/3.12/library/tempfile.html)、[Ruby3.4 IO.readpartial](https://docs.ruby-lang.org/en/3.4/IO.html#method-i-readpartial)。

最终人工回读了新增条目全文、R1–R9对应正文和现有R10场景/临时目录事实。核标题和共性索引的相对路径/锚点；六个实际消费者文件原生Test-Path均存在。Go→Ruby入口要求回根读取两语言页，根入口必读两语言和所选方向，新增知识有实际消费者。新增条目只补语义引导，未改执行约束或门禁；本次不重复宣称全库规则技术验收。

git diff --check对本次四个产品文件无空白错误；只属文本检查。未运行测试/回归、解析器、编译器、样本、模型转换或评估服务；没有本次动态通过数，不提交/推送或部署。

## 终态与停止

R1–R10当前正文及R10七个子项已逐项核对，知识维护要求完成；状态记DONE/COMPLETE，不等同功能验证。按目标到R10停止，不新增R11以后动作或回归。活动目标在完成核对后标记complete，向用户汇报；用户确认全量回归前不启动。
