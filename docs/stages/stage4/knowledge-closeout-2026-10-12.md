# 本批转换知识收尾（2026-10-12）

> 状态：R-01–R-10 TEXT_COMPLETE / STATIC_REVIEWED；知识维护范围收尾。效果、真实注入和全量回归 UNVERIFIED。
> 用户确认依次修订，知识语义以引导为主，不进行验证回归；最终全量回归由用户另行确认。本记录不宣布全系统优化完成。

后续接续：R-11–R-16 的流程/评估文本及源码候选也已收尾，见[六项修订完成记录](r11-r16-closeout-2026-10-12.md)。本知识记录的范围与未验证边界保持不变。

## 1. 完成范围与长期落点

本批已浏览并登记全部 96 份正式自审正文，形成 27 类知识维护去向；DeepSeek 多组发现经 Codex 区分已有规则、需补充、错误建议和证据不足。R-01–R-10 的应补正文及已定位错误修订均已落盘，R-10 七个子项已单独完成核对。本批知识侧没有遗留待写条目；未知精确版本、ABI、源消费者和历史归因作为规则适用边界保留，不能用通用引导猜补。

长期知识真源仍是仓库语言/方向/场景/系统正文，读取不依赖测试集、工程页或网页。本阶段接续记录见[修订任务 §10–11](tasks/evidence-quality-checklist.md#10-本批知识收尾与后续队列2026-10-12)。

本轮审查目录的 89 份文件已整体复制到 [review 归档](reviews/dataset-2-2026-10-12/README.md)，包括自审的两组逐项登记、27 类处置、DeepSeek A–E 的任务/事件/发现/覆盖与后续纠偏、历史修订记录及 R10 核对；另存原目录 README 和两份 optimization-inputs 汇总。原报告保持历史措辞，当前状态以本文件及阶段任务清单为准。

`dataset-2-copy/` 最终不作为保留目录或修订消费者，本轮没有删除。归档保存的是审查产物和问题汇总，**不是全部 5921 件原用例过程证据的备份**；历史案例路径、原件清单和报告中的旧相对链接只作出处定位，删除数据集后不能凭这些记录还原源码或复验旧 job。后续 R-11–R-16 在阶段方案/任务中续接，不要求读取将被移除的目录。

全量工程产物逐件验收没有完成；用户确认大部分案例读取归纳已经足够后结束审查。96/96 自审正文登记、知识维护完成与全量工程审毕是不同范围，不互相替代。

## 2. R-01–R-10 最终知识正文

| 修订 | 当前落点与完成内容 |
|---|---|
| R-01 | [Python→PowerShell](../../../skills/directions/python-to-powershell/SKILL.md) PY-PS-06：保留源写盘的 Base64 编码后字节，区分编码/解码输入输出及 BOM/换行；纠正旧示例 |
| R-02 | 同页 PY-PS-05/03：直接执行的 LASTEXITCODE 与 Start-Process 对象/等待分开，启动失败、退出、源忽略或传播分别保持；源静默路径不新增诊断 |
| R-03 | [Go §九](../../../skills/references/languages/go.md#九标准库消费点的选择引导)：JSON map/struct/tag/自定义编码与 range 顺序分开，Encode 终止符不机械套 Marshal |
| R-04 | Go 平台选择分支、[C++ §八](../../../skills/references/languages/cpp.md#八库抽象替换的选择引导) case/goto 作用域、[Ruby](../../../skills/references/languages/ruby.md) fork/exec 返回与错误事实分别补齐 |
| R-05 | [Python L1-PY-11](../../../skills/references/languages/python.md#l1-py-11-空白分行与制表列位置)：str/bytes 分行集合、列位置与 expandtabs；tabsize≤0 删除 TAB |
| R-06 | 同页 L1-PY-12：按两端/同端操作组合决定顺序，appendleft+popleft 为后入先出，保留 pushback 消费者 |
| R-07 | 同页 L1-PY-10：optparse 唯一前缀、歧义、缺参、诊断/退出及 prog；按实际覆盖方法与接受域选择目标 |
| R-08 | [文件场景](../../../skills/scenes/file-io/SKILL.md)：归档成员/CRC/内容、压缩字节/签名、合法依赖与实现子集分开；不以自洽编解码证明通用合法性 |
| R-09 | [进程身份系统](../../../skills/systems/posix-windows-process-identity/SKILL.md)、[注册表系统](../../../skills/systems/windows-registry-service-subsystem/SKILL.md)及语言页：环境块、可变长结构/缓冲、令牌/AccessCheck、原始与展开值及处理顺序；不猜 SDK 偏移 |
| R-10 | Go L1-GO-08–12、Python L1-PY-14、[Go→Ruby](../../../skills/directions/go-to-ruby/SKILL.md) GO-RB-08及[共性导航](../../../skills/references/seven-language-common-semantics.md)：扫描上限、用户后端、排序稳定性、deadline/等待、双流、临时目录、部分读取七个子项全部落盘 |

详细七子项及维护资料见归档内 [R10 完成核对](reviews/dataset-2-2026-10-12/R10-completion-audit-2026-10-12.md)；其“到 R10 停止”是上一目标完成时点，本次授权继续 R11 不改写该历史记录。

## 3. 27 类建议最终处置

| 建议簇（保留全部编号） | 本批最终维护去向 |
|---|---|
| K-A/F/G/H/L/M | C/C#/PowerShell 语言事实、进程身份与 Windows 子系统引导已补；Winsock 初始化沿用现有正文。环境块/布局/容量/有效权限/展开按具体 API 与平台选择，不推广成模块加载保证 |
| K-B/C/D/I | C 容量/借用、C++ 库替换/异常/创建/枚举、文件系统容量/创建模式引导已补；既有资源和错误规则继续消费，不以路径层数判断创建能力 |
| K-E/K/U/W | 进程等待/错误/双流、Python→PowerShell 和 Go deadline/WaitDelay 已补；终端/公开接口规则沿用，冻结 EOF 不授权删除调用 |
| K-J/N/R/S/Z | Python 解析器/文本/容器/解码、Go 及目标语言分割/默认插入/排序引导已补；按精确函数接受域和实际消费者选映射，不无条件排序或改容器 |
| K-O/P/Q/AA | Go 时间/计数器/Scanner/用户后端/平台分支、语言和文件页创建模式引导已补；采样值放宽不改变计数定义、后端或窗口 |
| K-T/V/X/Y | 文件变换/归档/清理、网络部分结果、Ruby 既有临时目录与 Go→Ruby 部分读取、Python tempfile 候选/检查/缓存已补；按源传播/忽略保持 |

逐条历史建议见[40 份登记](reviews/dataset-2-2026-10-12/full-review-self-reviews-01.md)、[56 份登记](reviews/dataset-2-2026-10-12/full-review-self-reviews-02.md)及[初审处置表](reviews/dataset-2-2026-10-12/full-review-knowledge-disposition.md)。初审“待补/未改”保留原时点，不作为当前未完成任务。补充不是采纳所有自审断言，也不证明已删除实现的历史缺陷成立。

拒绝固化的事实包括：tabsize≤0 保留 TAB、appendleft+popleft 为 FIFO、Go IsSpace 只含 Latin-1 集合、Unix Go TempDir 增加 TMP/TEMP、PowerShell int 强转即 floor、gnu_getopt 不受 POSIXLY_CORRECT 影响、非 NULL 空环境值等于 missing、os.ExpandEnv 等于 Windows %VAR% 展开。helper/help 文件存在不能证明 exec 分派臂，缺源依据不能采用大写路径建议；跨语言一律禁止第三方压缩库也未采纳。错误报告归档保留，频次或后轮 NO-REPAIR 不提高其可信度。

## 4. 静态依据与未验证范围

此前逐项核对过上述当前正文、R10 新条目全文、实际语言/方向消费者及导航；具体路径和 Git 格式检查记录保存在 R10 核对与修订交付中。本次回读归档入口、两组自审边界、处置/结果/R10 记录，核归档目录与当前产品落点，再将最新状态写入阶段导航/方案/任务。不把复制成功或回链可达当技术效果验证。

未编译或运行样本、目标、构建/平台测试、分类器、辅助脚本；未发转换模型请求、提交评估 job、连接 Controller、部署、提交或推送。E1 原证据/统计闭合、E2 历史归因/真实注入、E3 合法入口材料、E4 效果回归及 P1 平台验收仍按阶段清单保留。知识侧本批收尾不解除这些独立任务，也不保证全部旧知识或所有方向全面正确。
