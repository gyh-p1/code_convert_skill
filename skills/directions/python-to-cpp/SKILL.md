---
name: python-to-cpp
description: Use when converting Python source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → C++ 语言转换规则

> **适用基线**：CPython 3.12 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Python](../../references/languages/python.md)与[目标语言 C++](../../references/languages/cpp.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/python-to-cpp/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Python → C++ 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PY-CPP-01：Python 生成器 (yield) 向 C++17 状态机迭代器类重构映射
1. **源码触发条件**：Python 源码中包含 `def gen(): yield x` 生成器函数。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 27](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：调用生成器返回迭代器对象，通过 `next()` 逐步执行并在退出时触发清理。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C++17 中手动编写一个包含状态枚举、局部变量和 `next()` 或满足迭代器协议 `operator++`/`operator*` 的类；或者重构为一次性批量生成 `std::vector`。
   - *不适用条件*：严禁使用 C++20 协程关键字（`co_yield`, `co_return`），超出 C++17 冻结基线。
5. **错误机械替换反例**：
   ```cpp
   // 错误：在 C++17 基线中违规引入 C++20 协程
   // std::generator<int> MyGen() { co_yield 1; } // 编译报错：C++17 不支持协程
   // 正确：手动实现状态机类
   class MyGen {
       int state = 0;
       int current_val;
   public:
       bool next(int& val) {
           if (state == 0) { current_val = 1; state = 1; val = current_val; return true; }
           return false;
       }
   };
   ```
6. **信息不足或实现相关时的处理**：若生成器包含复杂的异常双向传递（`gen.throw()`），必须在报告中声明该复杂控制流降级。
7. **直接官方 HTTPS 依据链接**：[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)；[WG21-N4659 Clause 27](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PY-CPP-02：Python 函数返回 None 作为可选值向 C++17 std::optional 映射
1. **源码触发条件**：Python 源码中函数在查找到数据时返回对象，未查找到时返回 `None`。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 ISO C++17（[WG21-N4659 Clause 23.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：调用方使用 `if res is None` 判定缺失。
4. **目标可选写法和不适用条件**：
   - *可选映射*：方法返回值定义为 `std::optional<T>`；缺失时返回 `std::nullopt`；调用点使用 `has_value()` 或布尔上下文检查。
   - *不适用条件*：严禁机械转换为返回裸指针 `T*` 并返回 `nullptr`（会导致所有权归属混淆及悬垂指针风险）；严禁使用 C++23 的 `std::expected`。
5. **错误机械替换反例**：
   ```cpp
   // 错误：将值对象返回转换为裸指针并返回 nullptr，造成内存泄漏或解引用崩溃
   Item* FindItem(int id) {
       if (id <= 0) return nullptr; // 谁负责释放返回的 Item*？
       return new Item(id); // 泄漏！
   }
   // 正确：使用 std::optional
   std::optional<Item> FindItem(int id) {
       if (id <= 0) return std::nullopt;
       return Item(id);
   }
   ```
6. **信息不足或实现相关时的处理**：若需要表达具体错误原因而不只是简单缺失，使用自定义 Result 结构体。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 23.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PY-CPP-03：Python with 上下文管理器向 C++17 RAII 作用域析构映射
1. **源码触发条件**：Python 源码中使用 `with lock:` 或 `with open(...) as f:` 管理作用域生命周期。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 ISO C++17（[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：离开代码块时触发 `__exit__`，无论是否抛出异常均保证清理。
4. **目标可选写法和不适用条件**：
   - *可选映射*：互斥锁使用 `std::lock_guard` 或 `std::unique_lock`；文件使用 `std::ifstream`/`std::ofstream` 栈对象。
   - *不适用条件*：严禁在 C++ 中手动编写 `lock.unlock()` 并在中间留下未经保护的异常抛出点。
5. **错误机械替换反例**：
   ```cpp
   // 错误：手动管理锁，遇到异常跳过解锁
   std::mutex mtx;
   void Action() {
       mtx.lock();
       DoWork(); // 抛出异常！
       mtx.unlock(); // 永远不执行，死锁！
   }
   // 正确：RAII 守卫
   void Action() {
       std::lock_guard<std::mutex> lock(mtx);
       DoWork();
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及文件 I/O，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
