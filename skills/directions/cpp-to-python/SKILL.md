---
name: cpp-to-python
description: Use when converting C++ source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → Python 语言转换规则

> **适用基线**：ISO C++17 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C++](../../references/languages/cpp.md)与[目标语言 Python](../../references/languages/python.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C++ → Python 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-PY-01：C++ 模板泛型特化向 Python 动态方法派发与类型标注映射
1. **源码触发条件**：C++ 源码中定义函数模板或类模板，依赖静态类型推导。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 17](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：编译期针对每个实例化类型生成独立机器码，不匹配类型触发编译报错。
4. **目标可选写法和不适用条件**：
   - *可选映射*：先盘点本任务实际模板实例、特化、重载选择及其可观察结果，按实例映射为函数或显式分派。`typing.TypeVar` 不执行 C++ 编译期约束；仅当源选择逻辑确实等于首参数运行时类型分派时才用 `functools.singledispatch`，并核对继承、隐式转换与多参数选择差异。
   - *不适用条件*：SFINAE、模板特化或编译期常量若改变本次行为，不能因 Python 无同构机制而删掉；冻结实际已选结果或显式实现等效选择。无法确定实例/选择范围时报告知识缺口，不用泛型标注冒充语义保持。
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

### 规则 CPP-PY-02：C++ 运算符重载向 Python 特殊方法与可哈希性映射
1. **源码触发条件**：源定义 `operator==`、`operator<`、`operator[]`，或实际将该类型用作关联容器的键。
2. **冻结版本/运行时/API 前提**：ISO C++17 → CPython 3.12；按实际容器的比较器/哈希器与 [Python 数据模型](https://docs.python.org/3.12/reference/datamodel.html#object.__hash__)核对。
3. **原可观察行为**：重载定义比较、索引或键身份规则；有相等比较不自动表示该类型需可哈希，`std::map` 的排序比较也不自动等于 `operator==`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按源实际语义定义 `__eq__`、`__lt__`、`__getitem__`；只有目标需要哈希键且等价字段在作为键期间稳定时才定义与相等一致的 `__hash__`。
   - *不适用条件*：不能要求所有定义 `__eq__` 的类都补 `__hash__`。按可变内容比较的对象通常应保持不可哈希；源码需作为键时先核对源键副本/不可变性，可采用契约允许的不可变键表示，不能直接给可变对象加内容哈希。
5. **错误机械替换反例**：为可变 `Item.id` 同时定义按 id 相等和 `hash(self.id)`，放入 set/dict 后又修改 id，会改变哈希并破坏查找；“补上 __hash__ 就正确”不是规则。仅在 id 保持稳定且源键规则一致时，该映射才有前提。
6. **信息不足或实现相关时的处理**：未确定实际键用法、字段可变性、比较器或混合类型比较时，逐项登记未知。Python 无对应特殊方法的源操作需显式接口，不能静默省略。
7. **直接官方 HTTPS 依据链接**：[Python object.__hash__](https://docs.python.org/3.12/reference/datamodel.html#object.__hash__)（相等/哈希一致性与可变键约束）。

### 规则 CPP-PY-03：C++ std::thread 向 Python 线程/任务的功能边界与 GIL 限制
1. **源码触发条件**：源创建 `std::thread`，涉及 CPU 计算、I/O、共享状态、同步或取消。
2. **冻结版本/运行时/API 前提**：ISO C++17 → CPython 3.12；[threading](https://docs.python.org/3.12/library/threading.html)与 [multiprocessing](https://docs.python.org/3.12/library/multiprocessing.html#programming-guidelines)。不外推到不同解释器/版本。
3. **原可观察行为**：需保留线程拓扑、共享地址空间、错误、完成等待及可见顺序；线程并行不保证耗时线性缩短，性能要求另冻判据。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若需保留进程内共享状态与线程生命周期，核对 `threading` 的同步与 join 映射，并说明 CPython 3.12 中纯 Python CPU 代码受 GIL 限制。仅在源任务彼此独立、输入/输出可传递、进程模型差异已获允许且性能需求明确时，才考虑 `ProcessPoolExecutor`/进程池。
   - *不适用条件*：不为加速强制改多进程；跨进程数据复制/序列化、对象身份、共享资源、启动方式、异常/取消都须核对。I/O 密集也不自动许可改 `asyncio`，异步模型改变属于显式转换决定。
5. **错误机械替换反例**：源 worker 修改同一共享对象，父线程 join 后读取该对象；机械改进程池却未建立等效状态传递，worker 修改不会自动成为父进程对象的新状态。速度或能启动不是功能一致证据。
6. **信息不足或实现相关时的处理**：涉及线程/任务都加载[并发场景](../../scenes/concurrency/SKILL.md)，不只在出现共享内存词时加载。无既定并行性能义务时先保持功能；共享状态/取消边界未明则报告缺口，不擅自重构。
7. **直接官方 HTTPS 依据链接**：[Python 3.12 threading](https://docs.python.org/3.12/library/threading.html)；[multiprocessing 编程约束](https://docs.python.org/3.12/library/multiprocessing.html#programming-guidelines)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
