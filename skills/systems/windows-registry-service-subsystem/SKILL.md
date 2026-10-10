---
name: windows-registry-service-subsystem
description: Use as the source-OS -> target-OS layer when source code reads or writes the Windows registry, or creates, reconfigures, starts, stops or deletes a Windows service. Covers hive/key/value semantics, view redirection, data-type and length conventions, service state transitions, access rights, error sources and cleanup that must not be translated by name alone. Windows-only subsystem knowledge; it does not claim a POSIX equivalent exists and is not a behavior guarantee.
---

# Windows 注册表与服务子系统方向

本 Skill 是**系统方向**知识中 Windows 专有子系统的一份，覆盖注册表与服务控制管理器（SCM）两块的 API 语义义务。它与语言方向 Skill（如 [C → Go](../../directions/c-to-go/SKILL.md)）和 [进程执行场景](../../scenes/process-execution/SKILL.md) **共同阅读**：语言方向负责 API 与错误模型映射，本 Skill 只负责这两类 Windows 子系统"必须保留什么、哪里没有等价物"。它是静态规则与风险说明，**不保证**目标代码可编译、可移植或行为等价。

**方向不对称的说明**：注册表与服务在 POSIX/Linux 上**没有直接等价物**（配置文件与 init/systemd 不是同一模型）。因此本 Skill 对 Windows → POSIX 方向主要给出"不可映射项与替代方案的边界"，对 Windows → 其他语言（Go/Python/C#/PowerShell/Ruby）方向主要给出"子系统语义义务"，因为目标语言通常用封装库访问同一子系统。两种情形都不允许把"写了个配置文件"当成注册表等价。

## 触发条件与前提

- **触发**：源码确有注册表行为（`RegOpenKey*`/`RegQueryValue*`/`RegSetValue*`/`RegCreateKey*`/`RegDelete*`/`RegCloseKey`，或目标语言等价的注册表封装）或服务行为（`OpenSCManager*`/`OpenService*`/`CreateService*`/`ChangeServiceConfig*`/`StartService*`/`ControlService`/`QueryServiceStatus*`/`DeleteService`/`CloseServiceHandle`，或等价的 SCM 封装）。
- **前提**：先冻结目标 Windows 版本与架构（32/64 位）、目标语言运行时与其注册表/服务库、进程的位宽与清单（manifest）声明、运行账户与其特权、以及目标机器上是否已存在目标键/服务。不明时先询问或标为待确认。
- **安全边界**：本 Skill 只讲语义保持，不提供持久化、绕过检测或提权方法，也不授权运行样本；本条目的样例素材仅作静态审读。

## 应始终保留的可观察行为

- **位置精确性**：操作的是哪个根键（`HKEY_CURRENT_USER` / `HKEY_LOCAL_MACHINE` / …）、哪个子键路径、哪个值名（含大小写与空值名），以及一次操作影响的用户范围（当前用户 vs 全机）。
- **数据类型**：值的类型（`REG_SZ`/`REG_EXPAND_SZ`/`REG_DWORD`/`REG_QWORD`/`REG_BINARY`/`REG_MULTI_SZ`）必须保持；类型变化会改变读取方行为，且字符串与二进制的长度单位不同。
- **读写的可观察结果**：写后能否立刻读回、默认值与"值不存在"是否可区分、失败时是否留下部分写入（多值写入不是原子操作）。
- **服务状态机**：服务的存在性、启动类型、可执行路径、账户、当前状态（停止/启动中/运行/停止中）与状态转换顺序；以及失败后是否回滚到原配置。
- **权限与错误**：访问被拒绝、找不到键/服务、类型不匹配等失败类别；错误来自 `LONG` 返回值还是 `GetLastError()`。
- **清理顺序**：所有打开的键句柄与 SCM/服务句柄都必须关闭；错误路径上不得泄漏句柄，也不得在失败后留下被改动的配置。

## 注册表：差异与必须处理的点

| 主题 | 源码常见写法 | 转换必须处理的点 |
|---|---|---|
| 根键与访问权限 | `RegOpenKeyEx(HKEY_CURRENT_USER, "SOFTWARE\\...", 0, KEY_WRITE, &h)` | 根键决定用户范围；访问掩码（`KEY_READ`/`KEY_WRITE`/`KEY_ALL_ACCESS`）决定失败类别。只读改名写会让"权限不足"变成"运行期失败"，必须按源的实际意图保留 |
| 键不存在 | `RegOpenKeyEx` 返回 `ERROR_FILE_NOT_FOUND` | 目标语言封装常把"键不存在"变成异常或 `None`/空集合；源若把该错误当正常分支，目标侧必须显式区分"不存在"与"读取失败" |
| 创建键 | `RegCreateKeyEx` 的 `REG_OPTION_NON_VOLATILE` / 是否已存在 | 创建语义是"打开或创建"，本身不是幂等承诺；须保留"已存在时不覆盖已有值"这一差别 |
| 值类型与长度 | `RegSetValueExA/W` 的 `lpData` 与 `cbData` | **长度按字节且包含字符串终止符**：`REG_SZ`、`REG_EXPAND_SZ` 的 `cbData` 须包含结尾 NUL，`REG_MULTI_SZ` 须包含双 NUL；同时核对 A/W 版本、实际编码和字符宽度，不能把字符数直接当字节数。二进制值按实际字节数，不额外补字符串终止符。依据：[RegSetValueExW 的 lpData/cbData 契约](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regsetvalueexw) |
| 读取缓冲区与尺寸 | 先查询尺寸再分配，或固定缓冲区 | 尺寸是**字节数**不是字符数；`REG_EXPAND_SZ` 与 `REG_SZ` 的读取方是否做环境变量展开不同，不能互换类型 |
| 位宽视图重定向 | 32 位进程访问 `SOFTWARE` 下的键 | 64 位系统上 32 位进程默认被重定向到 `Wow6432Node` 视图；源码依赖的视图必须显式决定（`KEY_WOW64_64KEY`/`KEY_WOW64_32KEY`），否则读到的键与 64 位程序不同 |
| 注册表虚拟化 | 老式程序写 `HKLM\Software` | 在部分配置下会被虚拟化到每用户位置；转换不得假定写入的物理位置与逻辑路径一致，须按目标实际配置核对 |
| 值删除与键删除 | `RegDeleteValue` / `RegDeleteKeyEx` | 键删除受子键存在与位宽视图影响；`RegDeleteKey` 与 `RegDeleteKeyEx` 的语义不同，不能互换 |
| 刷新与持久化 | `RegFlushKey` | 何时真正落盘不是写入返回即完成；不要为了"看起来干净"删除 `RegFlushKey`，也不要以为它是崩溃安全的承诺 |
| 错误来源 | 返回 `LONG`，成功为 `ERROR_SUCCESS` | 这些 API **不设置** `errno`、也不等价于 `GetLastError()` 语义；转换后统一按一种错误来源读，不能混读 |

若源代码对 `REG_SZ` 仅传 `strlen(s)`、遗漏终止符字节，记录为源已有风险并定位实际 A/W 调用与输入，不能把它提炼成正确的通用长度规则。转换时不得未经确认就补终止符并宣称行为未变；目标封装若无法表达源的原始长度行为，列出差异，按已确认任务契约处理或保持待确认。

## 服务：差异与必须处理的点

| 主题 | 源码常见写法 | 转换必须处理的点 |
|---|---|---|
| 句柄与权限 | `OpenSCManagerA(host, SERVICES_ACTIVE_DATABASE, SC_MANAGER_ALL_ACCESS)` | 打开 SCM/服务都需要对应访问权限，通常要求提升后的管理员身份；失败类别是"访问被拒绝"而非"不存在"，须分开处理 |
| 打开服务 | `OpenServiceA(scm, name, SERVICE_ALL_ACCESS)` | 服务名与显示名不同；用显示名查不到。访问掩码决定能做什么（查询状态、启动、改配置各自不同） |
| 启动类型与配置 | `ChangeServiceConfigA(svc, SERVICE_NO_CHANGE, SERVICE_DEMAND_START, ...)` | `SERVICE_NO_CHANGE` 是"不改这一项"的哨兵，不是有效取值；把"不改"错传成具体值会静默改变服务启动方式 |
| 修改可执行路径 | `ChangeServiceConfigA(svc, ..., payload, ...)` | 路径字符串的引用规则（含空格时）与源一致；修改是**立即生效于磁盘配置**，不等于服务已重启 |
| 启动与状态轮询 | `StartServiceA(svc, 0, NULL)` 后直接读 `QueryServiceStatus` | `StartService` 返回成功只表示命令被接受；服务进入运行态需要轮询，源码若依赖轮询结果，目标侧必须保留轮询与超时 |
| 停止/控制 | `ControlService(svc, SERVICE_CONTROL_STOP, &status)` | 停止是请求；服务可能拒绝、可能超时。不能把"发出停止"当成"已停止" |
| 状态字段 | `SERVICE_STATUS`（`dwCurrentState`/`dwWin32ExitCode`/`dwServiceSpecificExitCode`） | 服务自身退出码在 `dwServiceSpecificExitCode`，与 SCM 级错误码不同来源，别混用 |
| 创建/删除服务 | `CreateService` / `DeleteService` | 创建需要目标可执行文件已存在；删除对已启动服务的行为受版本与状态影响，须显式处理失败分支 |
| 配置回滚 | 先改配置、启动、再改回原值（如凭据/路径的一次性替换） | 源码若在失败路径上"改回原配置"，目标侧必须保留回滚及其失败处理；丢掉回滚会留下被修改的系统配置 |
| 句柄清理 | 结束时 `CloseServiceHandle` | SCM 与服务的句柄**都要**关闭；顺序与错误路径上的关闭都要保留，泄漏句柄会阻塞服务对象释放 |

## 等价不可用（须停标，不得伪造映射）

- **POSIX 侧没有注册表**：`~/.config`、`/etc` 下的文本配置、`gsettings`/`dconf` 都不是注册表等价物（无位宽视图、无类型系统、无每用户/全机同一 API）。Windows → POSIX 方向必须把注册表访问列为**需重设计的缺口**，给出替代方案并说明可观察差异（键路径映射、类型、默认值、失败类别）。
- **POSIX 侧没有 SCM**：`init`/`systemd`/`launchd` 的服务模型（单元文件、目标/依赖、重启策略）与 SCM 的 `SERVICE_STATUS` 状态机不是同构映射；Windows → POSIX 的"服务"改写须按目标 init 模型重新设计，不能按 API 名对照。
- **跨机 SCM 访问**：通过 `OpenSCManager` 指定远端主机名走的是远程管理协议，目标语言/平台的远端等价物通常完全不同（或不可用），涉及时列缺口。
- 注册表/服务的**安全与策略行为**（ACL、注册表虚拟化的具体触发条件、服务账户与登录权利）属于系统策略范畴，本 Skill 只要求"不静默放宽或收窄"，具体配置须以目标环境的实际策略为准。
- SCM 相关操作所需特权（如加载驱动、调试程序）的启用方式属 [POSIX ↔ Windows 进程创建与身份/权限](../posix-windows-process-identity/SKILL.md)，本 Skill 不重复。

## 与其它 Skill 的组合

- 语言方向 Skill：负责 API 名、类型、错误模型（`LONG` vs 异常 vs error 值）与目标语言库选择。
- [POSIX ↔ Windows 进程创建与身份/权限](../posix-windows-process-identity/SKILL.md)：服务启动、令牌与特权启用、进程创建语义在此。
- [POSIX ↔ Windows 文件路径](../posix-windows-filesystem/SKILL.md)：注册表路径串使用的是反斜杠与保留名规则，路径解析与规范化差异在此。
- [进程执行场景](../../scenes/process-execution/SKILL.md)：服务/子进程的输出、超时与后代回收在此。
- 冲突时先保留源程序的可观察义务（位置、类型、状态机、回滚），写出平台差异与缺少的依据，再给有条件的转换。

## 依据

- Microsoft Learn：[`RegOpenKeyExW`](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regopenkeyexw)、[`RegCreateKeyExW`](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regcreatekeyexw)、[`RegSetValueExW`](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regsetvalueexw)、[`RegQueryValueExW`](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regqueryvalueexw)、[`RegDeleteValueW`](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regdeletevaluew)、[`RegCloseKey`](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regclosekey)、[`RegFlushKey`](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regflushkey)：键/值语义、类型、长度约定与返回值。
- Microsoft Learn：[Registry Value Types](https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-value-types) 与 [32-bit and 64-bit Application Data in the Registry](https://learn.microsoft.com/en-us/windows/win32/sysinfo/32-bit-and-64-bit-application-data-in-the-registry)：类型与位宽视图/重定向。
- Microsoft Learn：[`OpenSCManagerW`](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-openscmanagerw)、[`OpenServiceW`](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-openservicew)、[`CreateServiceW`](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-createservicew)、[`ChangeServiceConfigW`](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-changeserviceconfigw)、[`StartServiceW`](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-startservicew)、[`ControlService`](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-controlservice)、[`QueryServiceStatusEx`](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-queryservicestatusex)、[`DeleteService`](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-deleteservice)、[`CloseServiceHandle`](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-closeservicehandle)：SCM/服务句柄、配置、状态机与清理。
- Microsoft Learn：[Service Control Manager](https://learn.microsoft.com/en-us/windows/win32/services/service-control-manager) 与 [Service Status Structures](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/ns-winsvc-service_status)：状态字段与状态转换。

以上为平台规则依据，不是特定 Windows 版本、SDK、语言运行时或转换结果的验证记录；目标为具体版本/位宽时须核对对应文档。本 Skill 未经本项目转换样例验证。同时遵守根入口和[安全边界](../../../references/framework/safety-boundary.md)。**执行顺序受根入口三道硬门禁约束**（分类 `ALLOWED` → 源侧构建预检 → 评估就绪核对），见 [AGENTS.md](../../../AGENTS.md) 执行约束 §3。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)；本系统方向 Skill **不替代门禁、不构成执行授权**。
