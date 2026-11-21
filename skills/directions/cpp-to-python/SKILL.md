---
name: cpp-to-python
description: Use when converting C++ source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → Python 语言转换规则

> **适用基线**：ISO C++17 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C++](../../references/languages/cpp.md)与[目标语言 Python](../../references/languages/python.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 C++ → Python 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-PY-01：C++ 模板泛型特化向 Python 动态方法派发与类型标注映射
1. **源码触发条件**：C++ 源码中定义函数模板或类模板，依赖静态类型推导。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（WG21-N4659 Clause 17）；目标语言 Python 3.12（PY-REF-DATA）。
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
7. **资料依据（名称/版本/章节）**：PY-REF-DATA。

### 规则 CPP-PY-02：C++ 运算符重载向 Python 特殊方法与可哈希性映射
1. **源码触发条件**：源定义 `operator==`、`operator<`、`operator[]`，或实际将该类型用作关联容器的键。
2. **冻结版本/运行时/API 前提**：ISO C++17 → CPython 3.12；按实际容器的比较器/哈希器与 Python 数据模型核对。
3. **原可观察行为**：重载定义比较、索引或键身份规则；有相等比较不自动表示该类型需可哈希，`std::map` 的排序比较也不自动等于 `operator==`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按源实际语义定义 `__eq__`、`__lt__`、`__getitem__`；只有目标需要哈希键且等价字段在作为键期间稳定时才定义与相等一致的 `__hash__`。
   - *不适用条件*：不能要求所有定义 `__eq__` 的类都补 `__hash__`。按可变内容比较的对象通常应保持不可哈希；源码需作为键时先核对源键副本/不可变性，可采用契约允许的不可变键表示，不能直接给可变对象加内容哈希。
5. **错误机械替换反例**：为可变 `Item.id` 同时定义按 id 相等和 `hash(self.id)`，放入 set/dict 后又修改 id，会改变哈希并破坏查找；“补上 __hash__ 就正确”不是规则。仅在 id 保持稳定且源键规则一致时，该映射才有前提。
6. **信息不足或实现相关时的处理**：未确定实际键用法、字段可变性、比较器或混合类型比较时，逐项登记未知。Python 无对应特殊方法的源操作需显式接口，不能静默省略。
7. **资料依据（名称/版本/章节）**：Python object.__hash__（相等/哈希一致性与可变键约束）。

### 规则 CPP-PY-03：C++ std::thread 向 Python 线程/任务的功能边界与 GIL 限制
1. **源码触发条件**：源创建 `std::thread`，涉及 CPU 计算、I/O、共享状态、同步或取消。
2. **冻结版本/运行时/API 前提**：ISO C++17 → CPython 3.12；threading与 multiprocessing。不外推到不同解释器/版本。
3. **原可观察行为**：需保留线程拓扑、共享地址空间、错误、完成等待及可见顺序；线程并行不保证耗时线性缩短，性能要求另冻判据。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若需保留进程内共享状态与线程生命周期，核对 `threading` 的同步与 join 映射，并说明 CPython 3.12 中纯 Python CPU 代码受 GIL 限制。仅在源任务彼此独立、输入/输出可传递、进程模型差异已获允许且性能需求明确时，才考虑 `ProcessPoolExecutor`/进程池。
   - *不适用条件*：不为加速强制改多进程；跨进程数据复制/序列化、对象身份、共享资源、启动方式、异常/取消都须核对。I/O 密集也不自动许可改 `asyncio`，异步模型改变属于显式转换决定。
5. **错误机械替换反例**：源 worker 修改同一共享对象，父线程 join 后读取该对象；机械改进程池却未建立等效状态传递，worker 修改不会自动成为父进程对象的新状态。速度或能启动不是功能一致证据。
6. **信息不足或实现相关时的处理**：涉及线程/任务都加载[并发场景](../../scenes/concurrency/SKILL.md)，不只在出现共享内存词时加载。无既定并行性能义务时先保持功能；共享状态/取消边界未明则报告缺口，不擅自重构。
7. **资料依据（名称/版本/章节）**：Python 3.12 threading；multiprocessing 编程约束。

### 规则 CPP-PY-04：C++ 确定性 RAII 析构向 Python `with` / `try...finally` 映射
1. **源码触发条件**：C++ 源码依赖局部对象析构函数释放文件句柄、锁、事务或缓冲区等非内存资源，包含提前返回或异常展开路径。
2. **冻结版本/运行时/API 前提**：ISO C++17（WG21-N4659 Clause 15.2/6.7）→ CPython 3.12（PY-REF-CTX）。
3. **原可观察行为**：离开词法作用域时按构造逆序（LIFO）同步确定性执行析构清理，即使抛出异常也不延迟。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用上下文管理器（`with ...:`、`contextlib.ExitStack`）或 `try ... finally` 在离开作用域时按逆序同步释放资源。
   - *不适用条件*：严禁把资源清理寄托在 `__del__` 终结器上——循环引用、解释器退出序或非 CPython 实现均会延迟甚至跳过 `__del__`。
5. **错误机械替换反例**：
   ```python
   # 错误：依赖 __del__ 代替 C++ RAII 析构释放锁或文件
   class Guard:
       def __init__(self, lock):
           self.lock = lock
           self.lock.acquire()
       def __del__(self):
           self.lock.release() # 时机不确定，若发生引用保留则长期不解锁！

   # 正确：实现上下文管理器协议并使用 with
   class Guard:
       def __init__(self, lock):
           self.lock = lock
       def __enter__(self):
           self.lock.acquire()
           return self
       def __exit__(self, exc_type, exc, tb):
           self.lock.release()
           return False
   ```
6. **信息不足或实现相关时的处理**：若原 C++ 析构包含多个成员的逆序释放且中途可能抛异常，在目标 `__exit__` 或嵌套 `with`/`ExitStack` 中显式保留全部释放与异常传播规则。
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 15.2；PY-REF-CTX、`contextlib.ExitStack`。

### 规则 CPP-PY-05：C++ 按值拷贝语义向 Python 对象引用别名与显式拷贝映射
1. **源码触发条件**：C++ 源码将 `struct` / `std::vector` / 容器按值传参或通过 `b = a` 复制后独立修改副本或原对象。
2. **冻结版本/运行时/API 前提**：ISO C++17 → CPython 3.12（PY-REF-DATA、`copy` 模块）。
3. **原可观察行为**：按值赋值为目标对象创建独立存储与拷贝（除非字段本身为共享指针或引用），修改副本不回写原对象；同时若源码本身按引用 `T&` 或 `shared_ptr` 传递，则原值必须共享可见修改。
4. **目标可选写法和不适用条件**：
   - *可选映射*：先区分源声明是按值（`T`）还是按引用/指针（`T&`/`T*`）；按值且后续会被修改的复合对象，在绑定或传参边界显式复制（如 `copy.deepcopy` 或显式逐字段拷贝工厂），共享引用则保留原对象别名。
   - *不适用条件*：严禁将 C++ 按值传递直接写成 Python 普通赋值 `b = a` 并原地修改内部列表或属性，这会导致原对象状态被静默污染。
5. **错误机械替换反例**：
   ```python
   # 错误：将 C++ 按值传参 struct State { std::vector<int> items; }; 机械译为别名修改
   def step(state):
       state.items.append(99) # 污染调用方传入的 orig！

   # 正确（对应源按值语义）：在进入按值边界时显式构造独立副本
   def step(state):
       local_state = state.clone() # 显式复制须独立的成员
       local_state.items.append(99)
       return local_state
   ```
6. **信息不足或实现相关时的处理**：混合含共享资源句柄与独立值字段的类型须按成员所有权分别拷贝或引用共享，不在报告中以“浅/深拷贝”一言以蔽之。
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 15.8；PY-REF-DATA、`copy.copy`/`copy.deepcopy`。

### 规则 CPP-PY-06：C++ 向零截断整数除法与定宽回绕向 Python 向下取整与位掩码映射
1. **源码触发条件**：C++ 源码中出现负数整数 `/`、`%` 运算，或依赖固定位宽有符号/无符号整型（如 `uint32_t`、`uint64_t`）算术、移位溢出回绕。
2. **冻结版本/运行时/API 前提**：ISO C++17（WG21-N4659 Clause 8.6 / 6.9.1）→ CPython 3.12（PY-REF-DATA）。
3. **原可观察行为**：C++ `/` 朝零截断，且 `(a / b) * b + a % b == a`（`-7 / 3 == -2`、`-7 % 3 == -1`）；无符号定宽运算按 $2^W$ 取模，高位移出即截断。
4. **目标可选写法和不适用条件**：
   - *可选映射*：向零除法在存在负数时写显式语义转换（如 `int(a / b)` 对小整数，或仅整数路径 `math.trunc`/符号校正后绝对值相除，再以 `a - q * b` 得 C 余数）；定宽无符号回绕与移位对结果显式按掩码（`& 0xFFFFFFFF`、`& 0xFFFFFFFFFFFFFFFF`）截断。
   - *不适用条件*：严禁直接把 C++ 负数 `/`、`%` 译为 Python `//`、`%`（`-7 // 3 == -3`、`-7 % 3 == 2`）；严禁省略定宽无符号溢出与左移的高位掩码（Python `int` 任意精度不会截断）。
5. **错误机械替换反例**：
   ```python
   # 错误：直接用 // 和 % 以及不加掩码的 uint32 位运算
   q = -7 // 3        # Python 得 -3（C++ 为 -2）
   r = -7 % 3         # Python 得 2（C++ 为 -1）
   h = (1 << 32) - 1
   h = h + 2          # Python 得 4294967297（C++ uint32_t 回绕为 1）

   # 正确：保持向零除法与 32 位无符号模意义
   q = -((-7) // 3) if (-7 < 0) != (3 < 0) else (-7) // 3  # 或精确向零符号函数
   r = -7 - q * 3                                           # 得 -1
   h = (0xFFFFFFFF + 2) & 0xFFFFFFFF                        # 得 1
   ```
6. **信息不足或实现相关时的处理**：C++ 源码若自身发生有符号整数溢出（UB），须按源风险单独登记，不能把源 UB 伪称为可迁移规则。
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 8.6（Multiplicative operators）；Python Reference §6.7。

### 规则 CPP-PY-07：C++ `std::string` 原始字节与 `std::optional`/`nullptr` 哨兵映射
1. **源码触发条件**：C++ 源码用 `std::string` 承载原始协议字节、二进制缓冲或可能含 `\0` 与非 UTF-8 字节的数据，或用 `std::optional<T>` / 指针判空表达缺失状态。
2. **冻结版本/运行时/API 前提**：ISO C++17 → CPython 3.12（PY-REF-DATA、`bytes` / `str`）。
3. **原可观察行为**：`std::string` 本质是任意 `char` 字节序列容器，`size()` 返回字节数且允许内嵌 `\0`；`std::optional<int>` 为 `0` 时 `has_value()` 仍为 `true`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：原始字节流、定长字节长度与任意二进制协议优先映射为 `bytes`/`bytearray`；确定为文本时明确源编码再解码为 `str`；`std::optional`/`nullptr` 判空必须用 `is None` / `is not None`。
   - *不适用条件*：严禁用 `if opt:` 替代 `opt.has_value()`（当值恰好为 `0`、`""`、`False` 或空容器时逻辑反转）；严禁把含原始任意字节的 `std::string` 无条件假设为合法 UTF-8 `str`。
5. **错误机械替换反例**：
   ```python
   # 错误：将 optional<int> == 0 判成无值
   def check(opt):
       if not opt: # 若 opt == 0，Python 误判为缺失！
           return -1
       return opt

   # 正确：显式区分 None 与零值
   def check(opt):
       if opt is None:
           return -1
       return opt
   ```
6. **信息不足或实现相关时的处理**：文本编码未明确时保留 bytes 或登记编码缺口，不静默使用 `errors="ignore"` 丢弃字节。
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 24.3；Python 3.12 Built-in Types (`bytes`, `None`).

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
