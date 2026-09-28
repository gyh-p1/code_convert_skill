# 候选：长文件结构基线

> 状态：candidate（源文件已归档；有未验证的 No-RAG 目标草稿；未执行/未验收）  
> 源文件：`source/harmless_long_fixture.c`  
> 旧来源：`E:\桌面文档\Code_Convert\.codeconvert-state\datasets\candidates\s13-long-fixture\harmless_long_fixture.c`

## 初步信息

- 语言：C；旧文件 640 行。
- 内容：固定容量记录结构、25 个小函数、内存聚合、汇总输出和文本报告。
- 转换方向候选：C → C++。
- 系统方向：旧记录为 Linux 同平台长文件 fixture，不覆盖 Linux → Windows 或 Windows → Linux。
- 场景候选：长文件结构/状态；stdout/stderr 与相对路径文本文件输出。
- 来源性质：旧项目内部候选 fixture；尚未确认可对外再分发的许可证，先限项目内研究使用。

## 静态安全观察

源码自述仅做确定性内存聚合和文件写入；静态检查未发现 socket、进程创建或外部连接调用。每个 `fixture_unit_*` 有容量判断；`main` 依序调用这些函数并输出汇总。需注意 `fixture_write_report` 用 `fopen(path, "w")` 打开相对路径 `fixture_records.txt`，会在当前工作目录创建或覆盖该文件；若获准执行，只能在一次性隔离工作目录中进行。

静态观察不等于完整安全审计。未执行或编译；有一个未验证的保守 C++ 候选草稿，见 `output/no-rag/target.cpp` 和 `result.md`。此样例仅是长文件工作流/同平台流程候选，不属于任何已批准的转换测试。

## 待补条件

- 复核来源/内部使用授权及原仓库证据链；
- 为汇总 stdout、stderr、退出码、报告文件的字节内容和错误路径定义行为 oracle；
- 明确隔离目录和允许的语法/行为检查；
- 若未来确需使用，先为新任务写方案并完成上述来源、授权和隔离审阅，再另开转换 run。现有 `output/no-rag/target.cpp` 只是候选草稿，不是冻结基线；不沿用已取消四例计划的 RAG 配对步骤。
