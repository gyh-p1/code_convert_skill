---
name: python-to-ruby
description: Use when converting Python source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → Ruby 语言转换规则

> **适用基线**：CPython 3.12 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/python-to-ruby/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Python → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PY-RB-01：Python 与 Ruby 真值模型 (0, "" 真假异同) 冲突防反转映射
1. **源码触发条件**：Python 源码中使用 `if val:` 进行条件分支判断，其中 `val` 可能是数字 `0` 或空字符串 `""`。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：在 Python 中，数字 `0`、浮点 `0.0`、空字符串 `""`、空列表 `[]`、空字典 `{}` 均为**假（Falsy）**！
4. **目标可选写法和不适用条件**：
   - *可选映射*：**在 Ruby 中，只有 `false` 和 `nil` 为假，`0` 和 `""` 均为真（Truthy）**！若原 Python 意图是判断非零，必须在 Ruby 中显式写为 `if val != 0`；若意图是判断非空字符串，必须显式写为 `if !val.empty?`。
   - *不适用条件*：**绝对禁止直接翻译为 `if val`**！这会导致 Python 中条件为假的分支在 Ruby 中 100% 反向执行！
5. **错误机械替换反例**：
   ```ruby
   # 错误：Python 期望在 count == 0 时不进入分支，Ruby 却直接进入分支！
   # Python 原型:
   # if count: print("has items")
   count = 0
   if count # 错误：在 Ruby 中 0 是 Truthy，打印了 "has items"！
     puts "has items"
   end
   # 正确：显式判定
   if count != 0
     puts "has items"
   end
   ```
6. **信息不足或实现相关时的处理**：对每个无比较符的裸 `if x` 条件，严格依据其类型上下文替换为显式谓词。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 PY-RB-02：Python with 上下文管理向 Ruby 资源块模式 (Block/yield) 映射
1. **源码触发条件**：Python 源码中使用 `with open(path) as f:` 进行文件读写。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：离开作用域时无论是否发生异常均确保关闭底层文件句柄。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重构为 Ruby 原生代码块传递：`File.open(path) do |f| ... end`。
   - *不适用条件*：严禁写成无块形式的 `f = File.open(path)` 而不显式 `ensure f.close`。
5. **错误机械替换反例**：
   ```ruby
   # 错误：省略代码块，异常时文件句柄泄漏
   f = File.open(path, 'r')
   content = f.read
   f.close # 若 read 抛出异常，close 被跳过！
   # 正确：使用块自动管理生命周期
   content = File.open(path, 'r') { |f| f.read }
   ```
6. **信息不足或实现相关时的处理**：若涉及文件路径操作，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 PY-RB-03：Python 异常基类向 Ruby StandardError 捕获边界映射
1. **源码触发条件**：Python 源码中使用 `except Exception as e:` 捕获常规业务异常。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）。
3. **原可观察行为**：捕获所有从 `Exception` 派生的非系统退出异常（`SystemExit`、`KeyboardInterrupt` 继承自 `BaseException` 不被捕获）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Ruby 中使用 `rescue => e` 或 `rescue StandardError => e`（Ruby 默认 rescue 的正是 `StandardError` 及其子类）。
   - *不适用条件*：**致命禁区**：绝对不要在 Ruby 中写 `rescue Exception => e`！在 Ruby 中 `Exception` 是最顶层基类，盲捕获它会导致系统中断信号（`SignalException`）、语法错误（`SyntaxError`）和内存耗尽（`NoMemoryError`）全部被意外吞没，导致进程无法正常终止！
5. **错误机械替换反例**：
   ```ruby
   # 错误：捕获了最顶层 Exception，导致 kill 信号或内存耗尽被吞没
   begin
     do_work()
   rescue Exception => e # 致命错误：屏蔽了系统致命信号！
     puts "error: #{e}"
   end
   # 正确：捕获 StandardError
   begin
     do_work()
   rescue StandardError => e
     puts "error: #{e}"
   end
   ```
6. **信息不足或实现相关时的处理**：若 Python 捕获了专有异常，定义对应的 Ruby 异常派生自 `StandardError`。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
