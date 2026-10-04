---
name: cpp-to-python
description: Use when converting C++ source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → Python 语言转换规则

> **适用基线**：ISO C++17 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C++](../../references/languages/cpp.md)与[目标语言 Python](../../references/languages/python.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/cpp-to-python/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C++ → Python 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-PY-01：C++ 模板泛型特化向 Python 动态方法派发与类型标注映射
1. **源码触发条件**：C++ 源码中定义函数模板或类模板，依赖静态类型推导。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 17](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：编译期针对每个实例化类型生成独立机器码，不匹配类型触发编译报错。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为接收通用对象的单动态函数，结合 `typing.TypeVar` 标注；若有特定类型的分支逻辑，使用 `functools.singledispatch`。
   - *不适用条件*：严禁尝试在 Python 运行期模拟 C++ 编译期 SFINAE 或模板元编程递归展开。
5. **错误机械替换反例**：
   ```python
   # 错误：试图通过字符串反射检查类型模拟模板重载
   def process(val):
       if type(val).__name__ == 'int': ... # 脆弱且破坏多态
   # 正确：使用标准 singledispatch 装饰器分派
   from functools import singledispatch
   @singledispatch
   def process(val):
       raise NotImplementedError(f"Unsupported type: {type(val)}")
   @process.register(int)
   def _(val: int): ...
   ```
6. **信息不足或实现相关时的处理**：若存在重度模板数值计算，在报告中标明 Python 运行期解释性能损失。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 CPP-PY-02：C++ 运算符重载向 Python 双下划线特殊方法映射
1. **源码触发条件**：C++ 源码中重载 `operator==`、`operator<`、`operator[]` 等运算符。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 Python 3.12（[PY-REF-DATA §3.3](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：通过中缀表达式调用自定义函数；`const` 引用传参。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重写为 `__eq__`、`__lt__`、`__getitem__`；需同时保持 `__hash__` 一致性（可哈希对象若实现 `__eq__` 必须实现 `__hash__`）。
   - *不适用条件*：严禁只实现 `__eq__` 而遗漏 `__hash__` 导致自定义对象无法存入 `set` 或作为 `dict` 键。
5. **错误机械替换反例**：
   ```python
   # 错误：实现 __eq__ 未实现 __hash__，导致对象变为不可哈希（unhashable）
   class Item:
       def __init__(self, id): self.id = id
       def __eq__(self, other): return isinstance(other, Item) and self.id == other.id
   # s = {Item(1)} # 抛出 TypeError: unhashable type: 'Item'
   # 正确：显式实现 __hash__
   class Item:
       def __init__(self, id): self.id = id
       def __eq__(self, other): return isinstance(other, Item) and self.id == other.id
       def __hash__(self): return hash(self.id)
   ```
6. **信息不足或实现相关时的处理**：若重载了逗号表达式或地址运算符 `&`，Python 无等价魔术方法，必须重构成显式普通函数。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA §3.3](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 CPP-PY-03：C++ std::thread 多核并行向 Python 进程池/异步与 GIL 约束映射
1. **源码触发条件**：C++ 源码中启动多个 `std::thread` 并发执行密集数学计算。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 Python 3.12 / CPython 3.12（[CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/)）。
3. **原可观察行为**：多线程在多个物理核上并发推进，线性缩短总运行时间。
4. **目标可选写法和不适用条件**：
   - *可选映射*：CPU 密集型任务必须重写为 `multiprocessing.Pool` 或 `concurrent.futures.ProcessPoolExecutor`；若为 I/O 阻塞，可使用 `asyncio`。
   - *不适用条件*：严禁直接替换为 `threading.Thread`，受 CPython GIL 限制，纯 Python 代码的多线程无法实现多核 CPU 并行计算加速。
5. **错误机械替换反例**：
   ```python
   # 错误：使用 threading.Thread 进行 CPU 密集型运算，受 GIL 限制无加速
   import threading
   threads = [threading.Thread(target=heavy_calc) for _ in range(4)]
   for t in threads: t.start()
   for t in threads: t.join() # 实际由于 GIL 轮流锁，耗时比单线程还长！
   # 正确：使用进程池突破 GIL
   from concurrent.futures import ProcessPoolExecutor
   with ProcessPoolExecutor() as executor:
       futures = [executor.submit(heavy_calc) for _ in range(4)]
   ```
6. **信息不足或实现相关时的处理**：若代码涉及共享内存通信，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[CPY-DEV-GC](https://devguide.python.org/internals/garbage-collector/)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
