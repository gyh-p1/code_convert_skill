---
name: csharp-to-python
description: Use when converting C# source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → Python 语言转换规则

> **适用基线**：C# 12 / .NET 8 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/csharp-to-python/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C# → Python 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CS-PY-01：C# 泛型强类型容器向 Python 动态列表/字典与类型注解映射
1. **源码触发条件**：C# 源码中使用 `List<T>`、`Dictionary<TKey, TValue>` 等静态强类型集合。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：编译器在编译期强制元素类型一致，插入不匹配类型直接编译失败。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Python 原生 `list` 与 `dict`，添加标准类型提示（`list[T]`, `dict[K, V]`）；若需严格运行时类型校验，可使用轻量装饰器或辅助检查。
   - *不适用条件*：严禁认为类型注解会在 Python 运行期自动抛出类型异常。
5. **错误机械替换反例**：
   ```python
   # 错误：以为声明类型标注后会拦截非法类型，Python 仍然允许异构数据插入
   items: list[int] = []
   items.append("text") # 运行期完全不报错，破坏后续算术逻辑！
   # 正确：必要时添加显式 isinstance 校验
   def add_item(items: list[int], val: int):
       if not isinstance(val, int): raise TypeError("Expected int")
       items.append(val)
   ```
6. **信息不足或实现相关时的处理**：若包含多维数组，转换为嵌套列表或记录结构转换。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)；[MS-CS-COLL](https://learn.microsoft.com/en-us/dotnet/csharp/iterators)。

### 规则 CS-PY-02：C# IDisposable/using 向 Python with 上下文管理器映射
1. **源码触发条件**：C# 源码中使用 `using (var r = ...)` 管理互斥锁、数据库连接或临时文件。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)）；目标语言 Python 3.12（[PY-REF-DATA §3.3.9](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：退出 `using` 代码块时确定性调用 `Dispose()`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Python 的 `with` 上下文管理器，自定义对象实现 `__enter__` 与 `__exit__` 方法，或使用 `contextlib.contextmanager` 装饰器。
   - *不适用条件*：严禁在 Python 中依赖 `__del__` 进行确定性资源释放。
5. **错误机械替换反例**：
   ```python
   # 错误：依赖 __del__ 进行非内存资源清理
   class LockGuard:
       def __del__(self): release_lock() # 错误：GC 时机不确定，易引发死锁！
   # 正确：实现上下文协议
   class LockGuard:
       def __enter__(self): acquire_lock(); return self
       def __exit__(self, exc_type, exc_val, exc_tb): release_lock()
   ```
6. **信息不足或实现相关时的处理**：若涉及标准库原生支持（如 `threading.Lock`），直接使用 `with lock:`。
7. **直接官方 HTTPS 依据链接**：[MS-CS-DISPOSE](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)；[PY-REF-DATA §3.3.9](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 CS-PY-03：C# async/await (TAP) 向 Python asyncio 协程映射
1. **源码触发条件**：C# 源码中使用 `async Task<string>` 与 `await` 进行并发异步调用。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：基于线程池的非阻塞异步任务执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：定义为 `async def`，内部调用 `await`；调用顶层使用 `asyncio.run()` 驱动事件循环。
   - *不适用条件*：严禁在未进入事件循环的情况下直接调用异步函数（仅返回协程对象而不执行）；严禁在 Python 协程内执行长耗时同步阻塞系统调用（会卡死整个单线程事件循环）。
5. **错误机械替换反例**：
   ```python
   # 错误：在协程中直接调用同步 sleep 或阻塞 I/O，阻塞整个事件循环
   async def handle():
       time.sleep(5) # 错误：卡死所有并发协程！
   # 正确：使用异步非阻塞库
   async def handle():
       await asyncio.sleep(5)
   ```
6. **信息不足或实现相关时的处理**：若必须调用阻塞库，使用 `asyncio.to_thread()` 将其分流至单独线程。
7. **直接官方 HTTPS 依据链接**：[MS-CS-ASYNC](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
