---
name: posix-windows-threads
description: Map the POSIX pthread lifecycle used by a source file to Windows CRT/Win32 thread APIs without assuming identical cancellation, handles, or synchronization semantics.
---

# POSIX ↔ Windows 线程系统方向

> **加载前置**：先读取根[转换入口](../../../SKILL.md)并完成其必读契约与语言/方向选择；本页补充系统映射，不单独推进转换。

适用于 Linux/POSIX 的 `pthread_*` 与 Windows CRT/Win32 线程 API 之间的迁移。这里聚焦线程 API 与生命周期；共享状态、顺序和资源归属还须加载[并发场景](../../scenes/concurrency/SKILL.md)。按对应 API 契约选择映射，本项编译和行为结论须依据精确版本的独立证据。

## 适用映射与边界

| POSIX | Windows 常见对应 | 必须核对 |
|---|---|---|
| `pthread_create` | 使用 C/C++ CRT 时优先核对 `_beginthreadex` | 入口调用约定、返回值、参数生命周期、失败值 |
| `pthread_join` | `WaitForSingleObject`，必要时再读退出码 | 等待结果、超时、线程完成与句柄回收的先后 |
| `pthread_detach` | 创建或分离后适时 `CloseHandle` 线程句柄 | 关闭内核对象句柄**不**终止线程运行，仅释放引用使其不可再等待；不能用无参销毁指针替代 |
| `pthread_t` | Windows 线程 `HANDLE` / CRT 返回的句柄 | 两者不是可互换的整数 ID；目标句柄需在生命周期结束时关闭 |
| `pthread_exit` / 返回值 | 线程入口返回值与 Windows 退出码 | 类型、截断、谁负责读取；不要假定 POSIX `void*` 结果可原样映射 |
| `pthread_cancel` | 无通用等价物 | 取消点、清理处理器和线程状态不能用 `TerminateThread` 机械替代 |
| `pthread_mutex_t`（默认非递归） | `SRWLOCK`（非递归）或显式检查下的 `CRITICAL_SECTION`（默认可重入） | Windows `CRITICAL_SECTION` 同线程重复 `EnterCriticalSection` **不会死锁**而递增计数；POSIX 默认非递归互斥锁同线程重入会死锁或报错，不能把“是否允许自递归”静默改变 |
| `pthread_rwlock_t` | `SRWLOCK`（`AcquireSRWLockShared` / `AcquireSRWLockExclusive`） | 分别对应 `ReleaseSRWLockShared` / `ReleaseSRWLockExclusive`；写者优先/饥饿及不可重入语义按实际 OS 文档核对 |
| `pthread_cond_wait` / `pthread_cond_timedwait` | `CONDITION_VARIABLE` + `SleepConditionVariableCS` / `SleepConditionVariableSRW`、`WakeConditionVariable` / `WakeAllConditionVariable` | **`timedwait` 超时单位与基准不同**：POSIX 取**绝对时间** `timespec`（`CLOCK_REALTIME` 或 `CLOCK_MONOTONIC`），Windows 取**相对毫秒数** `DWORD`（及超时返回 `0` + `GetLastError()==ERROR_TIMEOUT`，POSIX 返回 `ETIMEDOUT`）；两边均须在谓词 `while` 循环中防御虚假唤醒 |
| `pthread_key_create` / `getspecific` / `setspecific` | `TlsAlloc` / `TlsGetValue` / `TlsSetValue` 或带回调的 `FlsAlloc` | `TlsAlloc` **无每键线程退出自动析构回调**（须依靠 `FlsAlloc` 回调或 `DllMain` `DLL_THREAD_DETACH`）；`pthread_key_delete` 不对现存线程自动运行析构函数，TLS 槽位数量上限亦有差异 |
| `pthread_once` | `InitOnceExecuteOnce`（或 `InitOnceBeginInitialize`） | 仅一次回调的执行状态、异常/失败重试语义与参数传递契约，不能用普通非原子 `bool` 标志替代 |

MSVC CRT 文档说明 `_beginthreadex` 的入口/返回类型、失败值与返回句柄；POSIX `pthread_create`/`pthread_join`/`pthread_mutex_*`/`pthread_cond_*`/`pthread_key_*`/`pthread_once` 规范分别定义线程生命周期与同步语义。按具体目标 SDK、CRT 与 POSIX 实现核对。

## 保持行为的规则

- 当线程使用 C/C++ CRT 时，不要仅因 `CreateThread` 名称相似便替换 `_beginthreadex`；核对 CRT 初始化要求及现有运行库。
- 成功创建后，明确哪个路径等待线程、读取退出状态并释放 Windows 线程句柄。等待已完成不自动等同于句柄已释放；分离线程（`pthread_detach`）须确认句柄在不再等待后准确关闭且只关闭一次。
- 创建失败时使用目标 API 的直接错误返回约定，不假设 `errno` 或 `GetLastError()` 一定承载该 API 的错误（POSIX `pthread_*` 多直接返回正 `errno` 错误码，而不写全局 `errno`；Win32 返回状态/句柄失败时才读 `GetLastError()`）。
- 不把 `TerminateThread` 当作 POSIX 可取消线程的等价实现；强制终止可能跳过线程内清理、留下未解锁的临界区并泄漏内核/CRT 资源。若源码中仅定义而未调用，不要把它虚构成活跃路径。
- 共享普通变量的读写同步属于并发语义，不能仅靠 API 名称映射解决；同步映射须保持源已有义务。改变源同步/时序须有源语义依据或生成前明确许可并冻结影响，事后登记不构成许可；源数据竞争单列风险，不借迁移顺手修源或声称等价。

## 同步原语与超时易错边界

1. **互斥锁递归性（`CRITICAL_SECTION` vs POSIX 默认互斥锁）**：源用 `PTHREAD_MUTEX_RECURSIVE` 时对应 `CRITICAL_SECTION` 语义；源用 `PTHREAD_MUTEX_ERRORCHECK` 或非递归默认锁且依赖报错/不可重入契约时，不可用未加保护的可重入锁静默吞掉同线程重入，首选 `SRWLOCK` 或显式状态检查并标注未覆盖错误路径。跨进程共享互斥（`PTHREAD_PROCESS_SHARED`）不能用进程内 `CRITICAL_SECTION`/`SRWLOCK`，须核对命名 Win32 Mutex 与销毁契约。
2. **条件变量超时换算与虚假唤醒循环**：`pthread_cond_timedwait` 使用绝对截止时刻 `abstime`，虚假唤醒后再次阻塞无需重算剩余时间；映射为 Windows 相对毫秒超时 `SleepConditionVariableCS(..., dwMilliseconds)` 时，若保留虚假唤醒 `while (!cond)` 循环，每次被唤醒重等前**必须重新扣减已耗时**，否则总超时会被静默延长甚至永不超时；并保留 `INFINITE`（对应无超时等待）及超时返回值判断（POSIX 返回 `ETIMEDOUT` 而 Windows 返回 `FALSE` 且 `GetLastError() == ERROR_TIMEOUT`）。
3. **TLS 析构回调缺失（`TlsAlloc` vs `FlsAlloc`）**：POSIX `pthread_key_create(key, destructor)` 在线程退出时非空 TLS 值会自动触发 `destructor(val)`；Windows 原生 `TlsAlloc` 不支持析构回调。确需每线程自动清理时须核 `FlsAlloc`（`PFLS_CALLBACK_FUNCTION`，注意进程退出/模块卸载时机差异）或显式在线程出口集中释放；缺精确宿主/运行时约束时记为待核缺口，不得静默丢失内存/句柄释放回调。

## 已有目标平台分支

源码若已有 `_beginthreadex`、`WaitForSingleObject`、`CloseHandle` 或 `CRITICAL_SECTION` / `CONDITION_VARIABLE` 的 Windows 分支，先确认转换选择的是已有分支还是从 POSIX 线程 API 独立移植。仅复用已有分支不能作为后者的验证；普通状态字段的跨线程同步另按[并发场景](../../scenes/concurrency/SKILL.md)核对。

## 依据

- Microsoft Learn：`_beginthread` / `_beginthreadex`、`WaitForSingleObject`、`CloseHandle`、`InitializeCriticalSection`、`SRWLOCK`、`SleepConditionVariableCS` / `SleepConditionVariableSRW`、`TlsAlloc` / `FlsAlloc`、`InitOnceExecuteOnce`
- The Open Group (POSIX.1)：`pthread_create`、`pthread_join`、`pthread_detach`、`pthread_cancel`、`pthread_mutex_init`、`pthread_rwlock_init`、`pthread_cond_wait` / `pthread_cond_timedwait`、`pthread_key_create`、`pthread_once`

---

**执行顺序与适用门禁统一按根入口分流**：先检查评估系统可达性，可达走分类、源预检及适用评估；不可达仅冻结、转换、自审和交付报告，不加载或调用分类器、不要求分类产物，不编译运行；见 [AGENTS.md](../../../AGENTS.md) 执行约束 §3。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)；本系统方向 Skill **不替代门禁、不构成执行授权**。
