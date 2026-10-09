---
name: cpp-to-ruby
description: Use when converting C++ source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → Ruby 语言转换规则

> **适用基线**：ISO C++17 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C++](../../references/languages/cpp.md)与[目标语言 Ruby](../../references/languages/ruby.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C++ → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-RB-01：C++ 拷贝构造与对象封装向 Ruby 对象引用与深拷贝映射
1. **源码触发条件**：C++ 源码中依赖对象按值传递或显式自定义拷贝构造函数完成深拷贝。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：按源实际复制构造/赋值运算符决定成员复制、别名与资源所有权；C++ 复制并不普遍保证深拷贝，指针成员或共享资源可继续别名。仅源明确深拷贝的成员才要求独立，不能擅自把共享身份改成复制。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按源复制契约选择 `dup` 与 `initialize_copy`，显式复制需独立的成员并保留需共享的成员。Ruby `dup` 默认是浅复制，`initialize_copy` 也不会自动递归深复制；通用 Marshal 往返不能代替任意对象的复制契约，资源/身份/自定义钩子须另核，不反序列化不可信材料。
   - *不适用条件*：严禁认为 `b = a` 会产生独立拷贝，Ruby 仅复制对象引用别名。
5. **错误机械替换反例**：
   ```ruby
   # 错误：将对象别名直接传递，修改内部状态污染原对象
   class Config
     attr_accessor :data
     def initialize(d); @data = d; end
   end
   c1 = Config.new([1, 2])
   c2 = c1 # 仅仅是别名！
   c2.data << 3 # c1.data 也被污染变成 [1, 2, 3]！
   # 有条件的映射：源确实复制该整数数组时，initialize_copy 配合 dup
   class Config
     def initialize_copy(orig)
       super
       @data = orig.data.dup
     end
   end
   c2 = c1.dup
   ```
6. **信息不足或实现相关时的处理**：若对象包含复杂原生资源指针，在转换报告中标明不可序列化限制。
7. **直接官方 HTTPS 依据链接**：[C++17 复制构造 §15.8.1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[Ruby Object#dup/initialize_copy](https://docs.ruby-lang.org/en/3.4/Object.html#method-i-dup)。

### 规则 CPP-RB-02：C++ RAII 锁管理向 Ruby Mutex#synchronize 作用域映射
1. **源码触发条件**：C++ 源码中使用 `std::lock_guard<std::mutex> lock(mtx)`。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)）。
3. **原可观察行为**：进入作用域加锁，退出作用域无论是否抛出异常均自动解锁。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `mutex.synchronize do ... end` 代码块。
   - *不适用条件*：严禁手动调用裸 `mutex.lock` 而不放在 `begin ... ensure mutex.unlock end` 中，否则异常会导致死锁。
5. **错误机械替换反例**：
   ```ruby
   # 错误：手动加锁未设 ensure，异常导致永久死锁
   mtx.lock
   dangerous_action() # 抛出异常！
   mtx.unlock # 永远无法执行，死锁！
   # 正确：使用 synchronize 块
   mtx.synchronize do
     dangerous_action()
   end
   ```
6. **信息不足或实现相关时的处理**：若代码涉及递归加锁，使用 `Monitor` 替代 `Mutex`。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)。

### 规则 CPP-RB-03：C++ std::map 有序关联容器向 Ruby Hash 插入顺序语义约束
1. **源码触发条件**：C++ 源码中使用 `std::map<Key, Value>` 依赖遍历时按键升序排列的性质。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 26.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)）。
3. **原可观察行为**：`std::map` 无论插入顺序如何，遍历顺序严格按照键的 `operator<` 排序。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby 的 `Hash` 保证的是**键的插入顺序**，而非按键排序！若需要按键有序遍历，必须在遍历前显式调用 `.sort_by { |k, v| k }`。
   - *不适用条件*：严禁将 C++ `std::map` 机械替换为 Ruby 原生 `Hash` 后直接依赖遍历有序性，插入顺序不同将导致遍历结果完全不同。
5. **错误机械替换反例**：
   ```ruby
   # 错误：误以为 Ruby Hash 自动按键排序
   h = {}
   h[10] = "b"; h[1] = "a"
   h.keys # 得到 [10, 1]，而 C++ std::map 遍历得到的是 [1, 10]！
   # 正确：显式按键排序遍历
   h.sort.each do |key, val|
     # 此处严格按键递增遍历
   end
   ```
6. **信息不足或实现相关时的处理**：若键类型无自然排序，向用户确认排序依据并在报告中标注。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
