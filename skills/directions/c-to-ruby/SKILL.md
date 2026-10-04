---
name: c-to-ruby
description: Use when converting C source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C → Ruby 语言转换规则

> **适用基线**：ISO C11 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C](../../references/languages/c.md)与[目标语言 Ruby](../../references/languages/ruby.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/c-to-ruby/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 C-RB-01：C 整数溢出截断与布尔真假向 Ruby 任意精度 Integer 与真值模型映射
1. **源码触发条件**：C 源码中以 `0` 作为假进行条件判断，或利用定宽整数溢出回绕实现循环哈希算法。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：C 中 `0` 为假；数值到达上限后按模截断。
4. **目标可选写法和不适用条件**：
   - *可选映射*：条件判断显式写为 `if val != 0`；数值回绕显式施加位掩码 `& 0xFFFFFFFF`。
   - *不适用条件*：**致命禁区**：绝对禁止将 C 代码 `if (x)` 机械转换为 Ruby `if x`（Ruby 中 `0` 与 `""` 均为真，直接反转控制流！）。
5. **错误机械替换反例**：
   ```ruby
   # 错误：C 中 0 为假，Ruby 中 0 为真，逻辑彻底颠倒！
   status = 0 # C 原型返回 0 表示成功
   if status  # 错误：在 Ruby 中 0 为真（Truthy），导致错误分支在成功时反向执行！
     handle_error()
   end
   # 正确：显式与 0 比较
   if status != 0
     handle_error()
   end
   ```
6. **信息不足或实现相关时的处理**：扫描所有源判断表达式，标明隐式非零假定。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 C-RB-02：C 手动资源释放向 Ruby 块模式 (Block/Yield) 与 ensure 映射
1. **源码触发条件**：C 源码中使用 `fopen`/`fclose`、`malloc`/`free` 配对管理生命周期。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/), [RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)）。
3. **原可观察行为**：函数退出或提前返回时显式调用释放函数。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重构为接收代码块的作用域模式（如 `File.open(...) do |f| ... end`），或使用 `begin ... ensure close end` 结构。
   - *不适用条件*：严禁依赖 Ruby GC 的自动终结清理文件描述符或套接字，可能导致句柄泄漏。
5. **错误机械替换反例**：
   ```ruby
   # 错误：打开文件后未通过块或 ensure 关闭，依赖 GC 终结导致描述符耗尽
   def read_data(path)
     f = File.open(path, 'rb')
     f.read # 错误：如果发生异常或多次调用，文件句柄直到下一次 GC 前保持打开！
   end
   # 正确：使用代码块保证离开时立即关闭
   def read_data(path)
     File.open(path, 'rb') { |f| f.read }
   end
   ```
6. **信息不足或实现相关时的处理**：若涉及文件 I/O，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)。

### 规则 C-RB-03：C 细粒度并发向 Ruby Thread/Mutex 与 MRI GVL 约束映射
1. **源码触发条件**：C 源码中通过多线程加速纯 CPU 计算密集任务。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html), [RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)）。
3. **原可观察行为**：C 线程在多个物理 CPU 核心上实现真正的并行执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：I/O 密集型并发使用 `Thread` 与 `Mutex`；CPU 密集型必须重构为 `Ractor` 或多进程（`Process.fork`），并在报告中声明并发模型转变。
   - *不适用条件*：严禁假设 Ruby `Thread` 能直接并行计算；MRI 全局 VM 锁（GVL）限制同一时刻仅一个线程执行 Ruby 字节码。
5. **错误机械替换反例**：
   ```ruby
   # 错误：期望通过多个 Thread 加速 CPU 密集计算，因 GVL 限制毫无加速甚至变慢
   threads = 4.times.map do
     Thread.new { compute_heavy_hash() }
   end
   threads.each(&:join) # 无法利用多核！
   ```
6. **信息不足或实现相关时的处理**：若需要系统原生线程同步，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)；[RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
