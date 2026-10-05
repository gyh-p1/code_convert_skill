---
name: python-to-ruby
description: Use when converting Python source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → Ruby 语言转换规则

> **适用基线**：CPython 3.12 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Python](../../references/languages/python.md)与[目标语言 Ruby](../../references/languages/ruby.md)。
> **方向案例与证据**：如本地工作区存在 `docs/test/dataset/python-to-ruby/README.md`，按其中 case 分层查看；该本地数据目录不随 Git/Skill 分发。
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

### 规则 PY-RB-04：Python `/` 真除法向 Ruby `Integer#/` 整除（向下取整）映射
1. **源码触发条件**：Python 源码中出现两个整数相除 `/`（如 `ticks / 1_000_000`）、`//`、`%` 或 `divmod(...)`，用于时间戳换算、比例/评分换算或分页计算。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-EXPR](https://docs.python.org/3.12/reference/expressions.html)）；目标语言 CRuby 3.4（[RB-DOC-INT](https://docs.ruby-lang.org/en/3.4/Integer.html)）。
3. **原可观察行为**：Python `/` 是真除法，`int / int` 返回 `float`（`7 / 2 == 3.5`）；`//` 向下取整（`7 // 2 == 3`、`-7 // 2 == -4`）；`%` 与 `divmod` 的余数符号跟随除数（`-7 % 3 == 2`）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：要保持 Python `/` 的浮点商写 `a.fdiv(b)` 或 `a.to_f / b`；要保持 Python `//` 写 `a / b` 或 `a.div(b)`；要保持 `%`/`divmod` 写 `a % b` / `a.divmod(b)`（Ruby 的 `%`、`divmod` 与 Python 同为向下取整语义，可逐条对应）。目标确实需要整数结果时，用 `divmod` 同时取商与余数，避免商取整后余数无处可查。
   - *不适用条件*：严禁把 `a / b` 原样照抄进 Ruby——两个整数相除会被**截断为整数**（Ruby 文档示例：`4 / 3` 得 `1`、`4 / -3` 得 `-2`），小数部分静默消失且无法由后续运算恢复；反过来把 Python `//` 改写成 `(a.to_f / b).to_i` 只属于“有条件的映射”：正数下结果相同，负数下 `to_i` 向零截断而 Python 向下取整（`-7 // 2 == -4`，而 `(-7.0 / 2).to_i == -3`）。
5. **错误机械替换反例**：
   ```ruby
   # Python 原型：unix_sec = (ticks / 1_000_000) - CHROMIUM_EPOCH_OFFSET
   ticks = 13_345_678_901_234_567
   unix_sec = (ticks / 1_000_000) - 11_644_473_600       # 错误：Ruby 整除，亚秒部分被丢弃
   unix_sec = ticks.fdiv(1_000_000) - 11_644_473_600     # 正确：保留浮点商
   # Python 原型：ratio = total // chunk
   ratio = (total.to_f / chunk).to_i                     # 有条件：负数时向零截断，与 Python // 不同
   ratio = total / chunk                                 # 正确：Ruby 的整数 / 即 Python 的 //
   ```
6. **信息不足或实现相关时的处理**：`/` 两侧类型不确定时（可能来自 `sum()`、配置读取或数据库列）必须先确认是 `Integer` 还是 `Float`，不得按整除假设；源若同时使用 `//` 与 `%`，必须成对保留（商与余数各自对应），不得只改一处。
7. **直接官方 HTTPS 依据链接**：[PY-REF-EXPR](https://docs.python.org/3.12/reference/expressions.html)；[RB-DOC-INT](https://docs.ruby-lang.org/en/3.4/Integer.html)。

### 规则 PY-RB-05：Python `str`/`bytes` 编码边界向 Ruby `String` 编码标签（Encoding）映射
1. **源码触发条件**：Python 源码中出现 `open(path, 'rb')`/`'wb'`、`bytes`/`bytearray`、`.encode()`/`.decode()`，或同时使用 HTTP 响应的 `response.text` 与 `response.content`。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 CRuby 3.4（[RB-DOC-STR](https://docs.ruby-lang.org/en/3.4/String.html)、[RB-DOC-ENC](https://docs.ruby-lang.org/en/3.4/Encoding.html)）。
3. **原可观察行为**：Python `str` 与 `bytes` 是不同类型、混用抛 `TypeError`；`'rb'` 读出 `bytes`，带 `encoding='utf-8'` 的文本写入按该编码编码；`response.text`（已解码文本）与 `response.content`（原始字节）是两条不同数据。
4. **目标可选写法和不适用条件**：
   - *可选映射*：二进制读/写用 `File.binread(path)` / `File.binwrite(path, data)`（`ASCII-8BIT` 的 `String`，对应 Python `bytes`）；文本读/写用 `File.read(path, encoding: 'UTF-8')` / `File.write(path, s, encoding: 'UTF-8')`；需要显式标注或改写编码标签时用 `str.b`、`str.force_encoding(Encoding::BINARY)`、`str.encode('UTF-8')`。
   - *不适用条件*：严禁把 Python 的 `str`/`bytes` 类型区分当成 Ruby 的类型区分——Ruby 两者都是 `String`，只差一个 `Encoding` 标签，错误写法不会在赋值或传参处报错，而是在拼接、正则或写盘时才以 `Encoding::CompatibilityError` 或“写出的字节与源不同”的形式暴露；也严禁假定 `File.read` 的默认编码等于源 `open()` 的默认编码（Ruby 用 `Encoding.default_external`，Python 用 locale 首选编码，两套默认值都不构成转换保证）。
5. **错误机械替换反例**：
   ```ruby
   # Python 原型：body = open(p, 'rb').read()   # bytes ；text = response.text   # str
   body = File.read(path)                 # 错误（对应 Python 'rb' 的二进制读）：按默认外部编码当文本读，字节与编码标签都可能不符
   body = File.binread(path)              # 正确：ASCII-8BIT 字节串，等价于 Python 的 'rb'
   mixed = body + suffix                  # 错误：ASCII-8BIT 与 UTF-8 拼接，含非 ASCII 字节时抛 Encoding::CompatibilityError
   mixed = body.dup.force_encoding(Encoding::UTF_8) + suffix   # 有条件：须先确认 body 确为 UTF-8 字节
   File.binwrite(out, mixed.encode(Encoding::UTF_8))           # 正确：写出前显式确定编码
   ```
6. **信息不足或实现相关时的处理**：源未声明编码时（`open()` 无 `encoding=`、依赖响应头或第三方库自行猜测解码）必须标为待确认并询问；不得默认 UTF-8，也不得以“两边默认都是 UTF-8”作为等价依据。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-STR](https://docs.ruby-lang.org/en/3.4/String.html)；[RB-DOC-ENC](https://docs.ruby-lang.org/en/3.4/Encoding.html)；[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 PY-RB-06：Python `dict` 键缺失（`KeyError`/`get`）向 Ruby `Hash` 的 `nil`/`fetch` 映射
1. **源码触发条件**：Python 源码中出现 `d[k]`、`d.get(k, default)`、`d[k] or default`、`k in d`、`try/except KeyError`，或把 `sqlite3.Row`、JSON 解析结果当映射并按字符串键取值（如 `row["url"] or ""`、`r.get("reason", "")`）。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-LIB-STDTYPES](https://docs.python.org/3.12/library/stdtypes.html)）；目标语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)）。
3. **原可观察行为**：Python `d[k]` 缺键抛 `KeyError`（可被 `except KeyError` 捕获而改变控制流）；`d.get(k, default)` 缺键返回 `default`，但键存在而值为 `None` 时仍返回 `None`；`d[k] or default` 在值为 `0`/`""`/`[]` 时同样走兜底。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`d.get(k, default)` 映射为 `h.fetch(k, default)`；`k in d` 映射为 `h.key?(k)`；依赖 `KeyError` 的控制流映射为 `begin ... rescue KeyError ... end`（Ruby `Hash#fetch` 缺键同样抛 `KeyError`）；要复现 `d[k] or default` 的兜底写 `h.fetch(k, nil) || default`。`defaultdict(list)` 一类共享默认容器写 `Hash.new { |hash, key| hash[key] = [] }`，不要写 `Hash.new([])`。
   - *不适用条件*：严禁把 `d[k]`、`d.get(k, default)` 一律机械替换为 `h[k]`——Ruby `Hash#[]` 缺键返回 `nil` 且**不抛错**，源中“缺键即失败/即走异常分支”的路径会带着 `nil` 继续向后传，直到算术、`strip`、字符串插值处才以 `NoMethodError` 或静默空值暴露；反之 `h[k] || default` 也不是 `get` 的等价物：`get` 只在缺键时取默认值，而 `||` 在值为 `nil`/`false` 时也取默认值（Ruby 中 `0`、`""` 为真，故这两者不触发兜底）。
5. **错误机械替换反例**：
   ```ruby
   # Python 原型：url = (row["url"] or "").strip() ；count = row["visit_count"] or 0
   url   = row["url"].strip                     # 错误：缺键得 nil，nil.strip 抛 NoMethodError
   url   = (row.fetch("url", "") || "").strip   # 正确：fetch 给默认值，|| 复现 Python 的 or 兜底
   count = row["visit_count"]                   # 错误：对应 d.get(k, 0)，缺键得 nil 而不是 0
   count = row.fetch("visit_count", 0)          # 正确：默认值语义与 dict.get 一致
   reason = row.fetch("reason", "")             # 对应 Python 的 r.get("reason", "")
   ```
6. **信息不足或实现相关时的处理**：源的键类型不确定时必须先确认——Ruby 中 `"url"` 与 `:url`、`"1"` 与 `1` 是不同的键，JSON 解析默认给字符串键而惯用 Ruby 代码常改写成符号键；键类型未定时保持与源一致的字符串键并标注待确认，不得默默改成符号。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)；[PY-LIB-STDTYPES](https://docs.python.org/3.12/library/stdtypes.html)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
