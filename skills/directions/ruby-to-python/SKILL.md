---
name: ruby-to-python
description: Use when converting Ruby source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → Python 语言转换规则

> **适用基线**：CRuby 3.4 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/ruby-to-python/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Ruby → Python 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 RB-PY-01：Ruby 与 Python 真值模型 (0, "" 真假异同) 冲突防反转映射
1. **源码触发条件**：Ruby 源码中使用 `if obj`，且 `obj` 可能为 `0` 或空字符串 `""`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：**在 Ruby 中 `0` 与 `""` 均为真（Truthy）**，分支必然执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：**在 Python 中 `0` 与 `""` 均为假（Falsy）**！若原 Ruby 意图是判断对象是否存在（即非 `nil`），在 Python 中必须显式写为 `if obj is not None:`！
   - *不适用条件*：**绝对禁止直接翻译为 `if obj:`**！当 `obj == 0` 时，Python 判定为假导致分支被跳过，控制流发生完全逆转！
5. **错误机械替换反例**：
   ```python
   # 错误：Ruby 原型为 if val (val 可能为 0，依然执行分支)
   # 在 Python 中直接写 if val:
   val = 0
   if val: # 错误：在 Python 中 0 为 Falsy，分支被意外跳过！
       do_action()
   # 正确：显式检查是否为 None
   if val is not None:
       do_action()
   ```
6. **信息不足或实现相关时的处理**：对每个无显式操作符的条件表达式，结合上下文标注真值映射依据。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 RB-PY-02：Ruby 代码块 (Block/yield) 向 Python 回调函数与生成器映射
1. **源码触发条件**：Ruby 源码中使用 `def my_each; yield item; end` 或传递代码块。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4；目标语言 CPython 3.12（[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)）。
3. **原可观察行为**：隐式代码块接收并调用 `yield`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若用于迭代，改写为 Python 的 `yield` 生成器函数；若用于回调处理，定义显式函数参数 `callback: Callable` 并显式调用 `callback(item)`。
   - *不适用条件*：严禁在 Python 中省略回调参数，Python 没有 Ruby 的隐式代码块机制。
5. **错误机械替换反例**：
   ```python
   # 错误：试图在普通函数中直接使用 yield 但期望它表现为外部传入的回调
   # 正确：显式接收可调用对象
   def for_each(items, callback):
       for item in items:
           callback(item)
   ```
6. **信息不足或实现相关时的处理**：若代码块包含 `break` 提前退出且向外层返回值，改写为显式循环。
7. **直接官方 HTTPS 依据链接**：[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)。

### 规则 RB-PY-03：Ruby 字符串内建 Encoding 向 Python str/bytes 隔离映射
1. **源码触发条件**：Ruby 源码中调用 `str.encoding`、`str.force_encoding` 或处理二进制 `ASCII-8BIT` 字符串。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：Ruby 中 `String` 是字节序列并附带编码标签。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若编码为 `ASCII-8BIT` / `BINARY`，映射为 Python 原生 `bytes`；若为文本（如 `UTF-8`），映射为 Python `str`；互转必须显式 `.encode()` / `.decode()`。
   - *不适用条件*：严禁在 Python 中将二进制数据当成 `str`，或混淆两者进行隐式拼接。
5. **错误机械替换反例**：
   ```python
   # 错误：将字节流与文本字符串直接相加
   b = b"header:"
   s = "data"
   # msg = b + s # 抛出 TypeError: can't concat str to bytes
   # 正确：统一类型再拼接
   msg = b + s.encode('utf-8')
   ```
6. **信息不足或实现相关时的处理**：若字符串来源不可信，使用 `errors='replace'` 或在报告中标记转码风险。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
