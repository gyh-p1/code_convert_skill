---
name: go-to-python
description: Use when converting Go source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → Python 语言转换规则

> **适用基线**：Go 1.27 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/go-to-python/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Go → Python 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-PY-01：Go 切片容量共享向 Python list 独立扩容语义隔离映射
1. **源码触发条件**：Go 源码中使用 `s2 := s1[1:3]` 从原切片截取新切片并修改元素。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Slice_types](https://go.dev/ref/spec)）；目标语言 Python 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：Go 中 `s2` 与 `s1` 共享底层数组，修改 `s2` 会原地影响 `s1`；直到发生 `append` 扩容后才分离。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Python 的切片操作 `l2 = l1[1:3]` 会**立即创建一个全新的浅拷贝独立列表**！修改 `l2` 绝不会影响 `l1`！若业务必须依赖共享修改，必须封装带视图指针的自定义类或操作同一个列表下标。
   - *不适用条件*：绝对不能直接假定 Python 切片具有 Go 切片的底层数组共享特性。
5. **错误机械替换反例**：
   ```python
   # 错误：以为 Python 切片像 Go 切片一样共享底层存储
   l1 = [1, 2, 3, 4]
   l2 = l1[1:3] # 生成了独立列表 [2, 3]
   l2[0] = 99   # l1 完全没有变化！l1[1] 依然是 2！
   # 正确：若需修改原列表，必须显式在原列表上修改
   l1[1] = 99
   ```
6. **信息不足或实现相关时的处理**：扫描所有切片赋值，确认是否有向原切片反写数据的依赖并告警。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Slice_types](https://go.dev/ref/spec)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 GO-PY-02：Go 显式 error 检查向 Python 结构化异常体系映射
1. **源码触发条件**：Go 源码中存在大量 `if err != nil { return nil, err }` 样板代码。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 Python 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：错误通过返回值显式传递，未检查不会自动抛出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Python 标准异常（如 `ValueError`, `FileNotFoundError`, `RuntimeError`），依靠异常自动冒泡传播，消除深层样板检查。
   - *不适用条件*：严禁在 Python 中模仿 Go 返回二元元组并在每一步手写 `if err is not None`（严重违背 Python 习惯用法，极易遗漏处理）。
5. **错误机械替换反例**：
   ```python
   # 错误：在 Python 中强行写 Go 风格的返回元组，违背习惯且容易被忽略
   def divide(a, b):
       if b == 0: return None, "divide by zero"
       return a / b, None
   # 正确：抛出内置异常
   def divide(a, b):
       if b == 0: raise ZeroDivisionError("divide by zero")
       return a / b
   ```
6. **信息不足或实现相关时的处理**：若原 Go 错误类型具备专有字段，定义继承自 `Exception` 的子类。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 GO-PY-03：Go 并发 Goroutine 与 Channel 向 Python asyncio 协程与 Queue 映射
1. **源码触发条件**：Go 源码中使用 `go fn()` 与 `ch := make(chan int)`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：轻量级协程在 M:N 调度器下执行，支持高并发 channel 通信。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重写为 `async def`，channel 替换为 `asyncio.Queue`，通信使用 `await queue.put()` 与 `await queue.get()`。
   - *不适用条件*：受 CPython GIL 影响，纯 CPU 运算无法多核加速；严禁在普通函数中直接使用阻塞队列而未设超时。
5. **错误机械替换反例**：
   ```python
   # 错误：在未加入事件循环的普通线程中调用 asyncio.Queue 导致 RuntimeError
   import asyncio
   q = asyncio.Queue() # 无当前运行的事件循环时在旧版本报错或引发跨线程异常
   ```
6. **信息不足或实现相关时的处理**：若代码涉及高吞吐 CPU 运算，向用户建议使用多进程并报告差异。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
