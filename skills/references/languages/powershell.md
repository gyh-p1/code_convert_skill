# PowerShell 语言共性语义（PowerShell 7.6）

> **用途**：供以 PowerShell 为源语言或目标语言的方向 Skill 按需读取；本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 变量持有 .NET 对象引用；标量基本类型按值语义求值；管道传递对象流时通过 `PSObject` 包装层反射解包。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` 管道对象解包与属性投影开销受 PowerShell 引擎管道缓冲区机制支配。
- **机械等价禁区与转换约束**：管道单元素展开（Unrolling）会将单元素数组隐式退化为标量，破坏类型契约。
- **官方资料依据**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` 底层为 .NET 整数体系；支持整型字面量后缀（`100L`, `1000D` 等）。
- **有符号溢出行为**：`[指定运行时的实现相关事实]` 默认算术超出当前类型上限时，PowerShell 引擎会**自动提升为更大宽度整型**（如 `[int32]::MaxValue + 1` 自动转为 `[int64]` 或 `[double]`）。
- **无符号溢出行为**：`[指定运行时的实现相关事实]` 显式通过 .NET 静态方法或强类型声明时遵循 .NET `unchecked` 回绕规则。
- **隐式提升与转换陷阱**：`[指定运行时的实现相关事实]` 动态弱类型转换系统在算术中自动升级类型，可能破坏对底层二进制溢出截断的依赖。
- **官方资料依据**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` 基于 .NET `System.String`（不可变 UTF-16 字符串）。
- **字节序列数据结构**：`[语言规范保证]` `[byte[]]` 数组。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` 内容中允许包含 `\0`；重定向到外部原生程序可能受宿主控制台编码截断。
- **编码假设与转换陷阱**：`[指定运行时的实现相关事实]` PowerShell 7+ 默认将文件重定向与外部管道输出编码设为 UTF-8（无 BOM）。
- **官方资料依据**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` 数组底层为固定大小 `object[]`；`[指定运行时的实现相关事实]` `+=` 追加元素会导致分配新数组并全量复制元素；存在单元素自动展开为标量机制。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `[hashtable]` 与 `[ordered]@{}` 映射结构。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` 默认 `hashtable` 遍历无序；显式声明 `[ordered]@{}` 保证插入顺序。
- **迭代期间修改（Fail-Fast）**：`[指定运行时的实现相关事实]` 遍历中修改集合会抛出集合已修改异常。
- **官方资料依据**：[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)<br>[MS-PS-HASH](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables)

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` 严格区分**终止错误**（Terminating Error，中断控制流）与**非终止错误**（Non-terminating Error，写入错误流继续运行）。
- **异常展开与性能模型**：`[指定运行时的实现相关事实]` `try`/`catch` **默认只能捕获终止错误**；受 `$ErrorActionPreference` 偏好变量严格控制。
- **进程退出码回传机制**：`[指定运行时的实现相关事实]` `$LASTEXITCODE` 记录外部进程最后返回码；Cmdlet 自身成败由 `$?`（`$true`/`$false`）记录；`exit` 终止宿主。
- **跨语言映射关键风险**：不可将 PS Cmdlet 写入的错误流直接等同于进程标准错误输出；`$?` 会被后续任意语句覆盖。
- **官方资料依据**：[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)<br>[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[指定运行时的实现相关事实]` 底层依赖 .NET CLR GC；处理大量管道对象时在进程内存中产生托管堆压力。
- **资源确定性释放机制**：`[指定运行时的实现相关事实]` 显式调用 `.Dispose()`，COM 对象必须调用 `[System.Runtime.InteropServices.Marshal]::ReleaseComObject()`。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 随宿主 .NET 运行时触发 GC。
- **悬垂与泄漏防范**：未释放的 COM 互操作对象将导致宿主子进程句柄泄露、阻碍外部进程终止。
- **官方资料依据**：[MS-PS-COM](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/new-object)

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` `Start-Job`（后台进程）；`Start-ThreadJob` / `ForEach-Object -Parallel`（多 Runspace 线程池）。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` Runspace 池映射至 .NET 线程池线程；脚本块隔离执行。
- **级联取消与超时机制**：`[指定运行时的实现相关事实]` 支持作业超时与取消命令；受宿主环境与具体命令控制。
- **内存模型与数据竞争**：`[指定运行时的实现相关事实]` 共享变量访问需使用同步包装或显式 .NET 同步锁，否则竞态数据损毁。
- **官方资料依据**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)<br>[MS-PS-THREADJOB](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs)

## 使用边界

将本页与所选的源→目标方向 Skill 及另一语言的共性页组合使用；映射前先确认源码真实行为。文件、网络、并发和跨 OS API 的具体差异仍按[共性索引的场景/系统分流](../seven-language-common-semantics.md)选读，不从语言事实直接推断系统 API 等价。没有逐例第三方证据时，语法/构建与功能结论保持 `UNVERIFIED`；本机不运行或编译样本。
