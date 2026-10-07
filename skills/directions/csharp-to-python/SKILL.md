---
name: csharp-to-python
description: Use when converting C# source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C# → Python 语言转换规则

> **适用基线**：C# 12 / .NET 8 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C#](../../references/languages/csharp.md)与[目标语言 Python](../../references/languages/python.md)。
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

### 规则 CS-PY-04：C# NullReferenceException/键缺失失败向 Python 显式 None 判断与等价异常映射
1. **源码触发条件**：C# 源码使用强制解引用与 `?.`/`??` 组合（`cred.TicketBlob?.Length ?? 0`、`(_targetUser ?? "无")`），或在未先判空的情况下取成员（`string.IsNullOrEmpty(hex)` 后 `hex.Replace(...)`），或依赖 `Dictionary` 的 `containsKey`/索引器区分"键缺失"。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)）；目标语言 Python 3.12（[PY-REF-EXCEPT](https://docs.python.org/3.12/reference/executionmodel.html)）。
3. **原可观察行为**：空引用取成员抛 `System.NullReferenceException`，`Dictionary` 键缺失抛 `KeyNotFoundException`，`??` 只在左值为 `null` 时取右值；这些失败都可被 `catch` 按类型分辨并转成退出码或错误输出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：空值统一用 `None` 表达，判空写 `if x is None`，缺省用 `x if x is not None else default`；异常按语义就近映射（空引用→`AttributeError`/`TypeError`，字典缺键→`KeyError`，下标越界→`IndexError`，参数非法→`ValueError`），并按"具体类型在前、`Exception` 在后"的顺序排列 `except`。
   - *不适用条件*：严禁把判空写成 `if not x`（`0`、`""`、`[]`、`False` 会被当作缺失，行为被静默改变）；严禁用裸 `except:` 把 `NullReferenceException` 与 `KeyError` 合并成同一分支（丢失失败类型，也吞掉 `KeyboardInterrupt`/`SystemExit`）；严禁在"键缺失属正常分支"的位置改用 `dict[key]`。
5. **错误机械替换反例**：
   ```python
   # C# 原型：Console.WriteLine($"Ticket Size : {cred.TicketBlob?.Length ?? 0} bytes");
   # 错误：用真值判断代替 is None，空字节串与 0 被误判为缺失
   size = len(cred.ticket_blob) if cred.ticket_blob else 0
   # C# 原型：if (arguments.ContainsKey("/ticket")) { string kirbi64 = arguments["/ticket"]; }
   kirbi64 = arguments["/ticket"] if "/ticket" in arguments else None  # 正确：显式区分缺失
   try:
       raw = bytes.fromhex(arguments["/servicekey"])
   except KeyError as exc:          # 正确：键缺失与格式错误分开捕获
       print(f"[X] missing argument {exc}")
   except ValueError:
       print("[X] /servicekey is not valid hex")
   ```
6. **信息不足或实现相关时的处理**：若源属性 getter 带副作用或可能抛非空引用类异常，或 `?.` 链中每一跳的空语义不同（"缺失" vs "空集合" vs "业务 0 值"），必须停下来标注该字段的空值契约，不得按单一 `None` 统一改写。
7. **直接官方 HTTPS 依据链接**：[PY-REF-EXCEPT](https://docs.python.org/3.12/reference/executionmodel.html)；[MS-CS-EXCEPT](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)。

### 规则 CS-PY-05：C# Encoding.UTF8/Unicode 字节序列向 Python str/bytes 与 codec 显式映射
1. **源码触发条件**：C# 源码出现 `Encoding.UTF8.GetBytes`/`GetString`、`Encoding.Unicode.GetBytes`（即 `Encoding.Unicode`）、`ASCIIEncoding`、`Convert.FromBase64String`/`ToBase64String`，并在其后用 `.Length`、`Substring`、`BitConverter.ToString` 处理结果。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-STRING](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)）；目标语言 Python 3.12（[PY-LIB-CODECS](https://docs.python.org/3.12/library/codecs.html)）。
3. **原可观察行为**：`Encoding.UTF8` 产出的字节等于 UTF-8 字节序列；`Encoding.Unicode` 是 UTF-16 小端、**不写 BOM**（ASCII 字符占 2 字节）；`Convert.FromBase64String` 对含空白或非法字符的输入抛 `FormatException`；`string.Length` 计 UTF-16 代码单元（代理对占 2）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`str` 与 `bytes` 严格分离，`s.encode('utf-8')` / `b.decode('utf-8')` 成对出现；UTF-16 小端用 `s.encode('utf-16-le')`，UTF-16BE 用 `'utf-16-be'`，需要 BOM 时写 `'utf-8-sig'`/`'utf-16'` 并在注释中说明；Base64 用 `base64.b64decode(s, validate=True)` 与 `base64.b64encode(b)`；`Encoding.ASCII` 用 `'ascii'` 并显式处理不可编码字符。
   - *不适用条件*：严禁把 `Encoding.Unicode.GetBytes` 机械替换为 `.encode('utf-8')`（每字符字节数改变，下游按偏移拼接/替换的算法全部错位）；严禁对 `bytes` 调用 `len()` 后再与 C# `string.Length` 互换使用；严禁混用 `str` 与 `bytes`（拼接、正则、切片都会直接抛 `TypeError`，而不是源语言的隐式行为）。
5. **错误机械替换反例**：
   ```python
   # C# 原型：BitConverter.ToString(Encoding.Unicode.GetBytes(sigString)).Replace("-", "")
   # 错误：把 UTF-16 的按字符 2 字节序列当成 UTF-8 字节序列
   hex_replace = sig_string.encode('utf-8').hex()   # 错误：ASCII 字符只占 1 字节，长度与源不一致
   # C# 原型：BitConverter.ToString(Encoding.UTF8.GetBytes(menuString)).Replace("-", "")
   hex_replace = menu_string.encode('utf-8').hex()  # 正确：与 Encoding.UTF8 对应
   utf16_hex = sig_string.encode('utf-16-le').hex() # 正确：与 Encoding.Unicode 对应（无 BOM）
   n_bytes = len(sig_string.encode('utf-16-le'))    # 正确：需要字节长度时先编码再计数
   ```
6. **信息不足或实现相关时的处理**：源码若在非 ASCII 文本上做 `Length`/`Substring` 定位，必须先确认按"字符"还是"字节/代码单元"语义，并确认目标侧是否要求逐字节复现（例如十六进制替换的偏移量），无法确认时把编码契约写为待确认。
7. **直接官方 HTTPS 依据链接**：[PY-LIB-CODECS](https://docs.python.org/3.12/library/codecs.html)；[PY-LIB-BASE64](https://docs.python.org/3.12/library/base64.html)。

### 规则 CS-PY-06：C# unchecked 定宽整数回绕与装箱向 Python 任意精度 int 的显式截断映射
1. **源码触发条件**：C# 源码对 `int`/`uint`/`long` 做加减乘或移位并依赖默认 `unchecked` 回绕（哈希、异或混淆、长度/校验和计算），或把定宽值装箱进 `object`/`Dictionary<string, object>` 后在两处强转。
2. **冻结版本/运行时/API 前提**：源语言 C# 12 / .NET 8（[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：默认 `unchecked` 上下文中定宽整数按补码截断回绕（`int.MaxValue + 1` 得 `int.MinValue`），`checked` 作用域内则抛 `OverflowException`；装进 `object` 后拆箱回窄类型会按目标宽度重新截断。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Python `int` 为任意精度，需要保留回绕语义时显式施加位掩码并回解读符号位：`v = (v + 1) & 0xFFFFFFFF`；`& 0x7FFFFFFF` 用于只保留 31 位等特定位宽场景；有符号回绕按位宽写 `mask = 0xFFFFFFFF; v = v & mask; v = v - (1 << 32) if v >= (1 << 31) else v`；把定宽意图写进类型标注并在 docstring 中声明位宽契约。
   - *不适用条件*：严禁假定 Python 也会截断（数值会一直增长，写入二进制/长度字段时才在编码步骤报错或静默变形）；严禁对带符号值直接使用 `& 0xFFFFFFFF` 而不做符号回读（`-1 & 0xFFFFFFFF` 得 `4294967295`，符号被静默翻转）；严禁依赖位掩码模拟 `checked` 的 `OverflowException`（掩码是静默截断，不会抛出）。
5. **错误机械替换反例**：
   ```python
   CHECKSUM_MASK = 0xFFFFFFFF
   # C# 原型：unchecked { int h = (h << 5) + h + c; }  // 32 位补码回绕
   def hash32(data: bytes, h: int = 0) -> int:
       for c in data:
           h = (h << 5) + h + c       # 错误：Python 不做 32 位回绕，h 会无限增长
       return h
   # 正确：每步显式截断到 32 位无符号范围，再按需要回读为有符号 int32
   def hash32(data: bytes, h: int = 0) -> int:
       for c in data:
           h = ((h << 5) + h + c) & CHECKSUM_MASK
       return h
   ```
6. **信息不足或实现相关时的处理**：源码未显式写 `checked`/`unchecked` 时，其实际语义还受项目编译选项与常量表达式规则影响，无法从单个方法体确认时，把"该表达式是否允许回绕"标为待确认；需要真任意精度继续运算的场景，则不要手工模拟回绕。
7. **直接官方 HTTPS 依据链接**：[MS-CS-CHECKED](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked)；[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
