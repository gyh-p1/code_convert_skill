---
name: go-to-ruby
description: Use when converting Go source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → Ruby 语言转换规则

> **适用基线**：Go 1.27 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 Ruby](../../references/languages/ruby.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/go-to-ruby/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Go → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-RB-01：Go map 无序遍历向 Ruby Hash 有序插入遍历的隔离映射
1. **源码触发条件**：Go 源码中通过 `for k, v := range m` 遍历哈希表。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Map_types](https://go.dev/ref/spec)）；目标语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)）。
3. **原可观察行为**：Go 语言规范明确未规定 map 遍历顺序（故意引入随机种子打乱顺序）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby 的 `Hash` 规范**强制保证按键值对的插入顺序遍历**！转换至 Ruby 后，代码切不可隐式产生“顺序依赖”；若业务需要无序性（如测试随机打乱），必须显式调用 `.to_a.shuffle`。
   - *不适用条件*：严禁在转换后代码中依赖插入顺序作为业务逻辑前提，否则逆向回 Go 时必崩溃。
5. **错误机械替换反例**：
   ```ruby
   # 错误：误以为 Ruby Hash 与 Go 一样是随机遍历，编写了依赖顺序或未打乱的逻辑
   # Go: for k := range m { ... } // 每次运行顺序不同
   # Ruby: h.each { |k, v| ... } // 永远按照严格的插入顺序遍历！
   ```
6. **信息不足或实现相关时的处理**：在转换报告中明确标记 Ruby Hash 存在插入有序性保证的事实。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Map_types](https://go.dev/ref/spec)；[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)。

### 规则 GO-RB-02：Go 定宽整数模截断向 Ruby 任意精度 Integer 显式掩码映射
1. **源码触发条件**：Go 源码中使用 `uint32` 进行运算，依赖其超出 $2^{32}-1$ 时自动按模截断回绕。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：达到上限后自动截断回绕（非 UB）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Ruby 中计算后显式施加位掩码 `& 0xFFFFFFFF`，保留截断值。
   - *不适用条件*：严禁直接计算，Ruby `Integer` 自动升级为大数，高位数据残留导致哈希或校验和计算彻底错误。
5. **错误机械替换反例**：
   ```ruby
   # 错误：未加掩码截断，导致高位无限增长
   # Go: var h uint32 = 0xFFFFFFFF; h = h + 1 // h 变成 0
   h = 0xFFFFFFFF
   h = h + 1 # Ruby 中 h 变成了 4294967296，彻底失真！
   # 正确：显式截断
   h = (h + 1) & 0xFFFFFFFF
   ```
6. **信息不足或实现相关时的处理**：若涉及有符号数转换，提供补码还原函数。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 GO-RB-03：Go CSP 并发模型向 Ruby Queue/Mutex 与 GVL 约束映射
1. **源码触发条件**：Go 源码中使用多个 Goroutine 通过信道传递流水线数据。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)）。
3. **原可观察行为**：轻量协程高效流水线调度。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `Thread` 配合 `Thread::SizedQueue` 模拟带缓冲 Channel；在队列关闭时使用特定的标志对象（Sentinel Object）。
   - *不适用条件*：受 GVL 限制，纯 CPU 运算无法多核并行；注意未关闭队列会导致线程永久挂起。
5. **错误机械替换反例**：
   ```ruby
   # 错误：未关闭队列导致消费者线程 pop 永远阻塞发生死锁
   q = SizedQueue.new(10)
   # 生产者结束未通知，消费者 q.pop 永久挂死！
   # 正确：使用哨兵或关闭机制
   q.close
   ```
6. **信息不足或实现相关时的处理**：若需完全独立并发，建议采用 Ractor 模型并记录实验性质。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
