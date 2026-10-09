---
name: ruby-to-python
description: Use when converting Ruby source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → Python 语言转换规则

> **适用基线**：CRuby 3.4 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Ruby](../../references/languages/ruby.md)与[目标语言 Python](../../references/languages/python.md)。
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

### 规则 RB-PY-04：Ruby Symbol 向 Python str / enum.Enum 的选择与相等性映射
1. **源码触发条件**：Ruby 源码用 `Symbol` 作状态标记、选项或散列键，例如 `origin_type: :session`、`private_type: :ssh_key`、`update: :unique_data`、`data: { :company => company }`、`credentials = { origin_type: :session, ... }`、`values[:starttype]`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-SYMBOL](https://docs.ruby-lang.org/en/3.4/Symbol.html)）；目标语言 CPython 3.12（[PY-LIB-ENUM](https://docs.python.org/3.12/library/enum.html)、[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：`Symbol` 是不可变、可哈希、全局唯一且可驻留的标识符，相等按身份；同一个 `:session` 无论出现在何处都是同一对象；`Symbol#to_s` 才是文本，`:'a b'` 这类含空格/非标识符字符的符号在 Ruby 中合法；符号可作 `Hash` 键，且 `Hash` 保留键的插入顺序。
4. **目标可选写法和不适用条件**：
   - *可选映射*：取值封闭且只在本程序内比较的状态量优先用 `enum.Enum`（成员用 `auto()` 或显式值），比较一律在成员之间进行；需要与外部交换（JSON、日志、配置）或键来自运行期时用 `str`（含非标识符字符时必须是 `str`）；Python 3.11 起若既要字符串可比性又要枚举成员身份，可用 `enum.StrEnum`——采用前必须先声明目标解释器版本不低于 3.11。
   - *不适用条件*：严禁把符号翻译成"裸字符串字面量"与枚举成员混比（`MyEnum.Session == "session"` 恒为 False，产生静默分支失效），也严禁把外部输入直接 `MyEnum(value)` 而不处理 `ValueError`；**`enum.Enum` 必须用 `MyEnum["Session"]`（按成员名）或 `MyEnum("session")`（按值）取值，二者不可混用**。
5. **错误机械替换反例**：
   ```python
   import enum
   class CredType(enum.Enum):
       SESSION = "session"
   # 错误：成员与字符串混比，两边类型不同，条件永远不成立
   if data["origin_type"] == "session":      # 错误：data 中该字段可能是 CredType.SESSION，此比较恒为 False
       handle_session()
   # 错误：按键取值的方式与枚举的构造方式混用
   t = CredType["SESSION"]                   # 错误："SESSION" 不是成员名；KeyError
   # 正确：成员之间比较；外部输入按值构造并按成员名取用
   if data["origin_type"] == CredType.SESSION:
       handle_session()
   t = CredType("session")                   # 正确：按成员值构造
   ```
6. **信息不足或实现相关时的处理**：符号的取值集合是否封闭（是否来自 `datastore`、JSON、网络或用户输入）必须从源码确认；无法确认时标注"键集合开放"并询问，不得用 `enum.Enum` 收窄取值域；符号是否含非标识符字符必须逐个核对（`:'a b'` 无法变成枚举成员名）；若选择 `StrEnum`，必须确认目标解释器版本，不得假定 3.11 及以上。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-SYMBOL](https://docs.ruby-lang.org/en/3.4/Symbol.html)；[PY-LIB-ENUM](https://docs.python.org/3.12/library/enum.html)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 RB-PY-05：Ruby 块/`yield` 向 Python 生成器或显式回调的选择（`break`/`next` 与惰性）
1. **源码触发条件**：Ruby 源码用块驱动迭代或把块当过程传递，例如 `::File.open(resource_file).each_line(chomp: true) do |cmd| next if cmd.strip.empty? ... end`、`commands.each do |cmd| ... next if cmd.strip.empty? ... end`、`path.scan(...).flatten[0]`、`creds.each do |cred| ... end`、`files.map { |f| ... }`、`&:join` 简写。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-PROC](https://docs.ruby-lang.org/en/3.4/Proc.html)）；目标语言 CPython 3.12（[PY-REF-EXPR-YIELD](https://docs.python.org/3.12/reference/expressions.html)、[PY-LIB-TYPING](https://docs.python.org/3.12/library/typing.html)）。
3. **原可观察行为**：`yield` 把控制权交给块并取其返回值（`each` 等返回原集合，而非块结果）；块内 `next v` 让 `yield` 求值为 `v` 并继续；块内 `break v` **终止调用方方法的迭代**且该方法的返回值为 `v`；不含 `yield` 的普通方法返回 `Enumerator` 时迭代是惰性的。
4. **目标可选写法和不适用条件**：
   - *可选映射*：源码中方法本身用 `yield` 逐项产出、调用方只做遍历时，写成生成器函数（在循环里 `yield item`）；源码只做"逐项消费"、不产出序列时，写成显式回调参数（`def for_each(items, callback: Callable[[T], None]) -> None`）并显式 `callback(item)`；`next` → `continue`。
   - *不适用条件*：严禁把普通函数里出现 `yield` 就当"外部传入回调的等价写法"——一旦函数体含 `yield`，调用它得到的是生成器对象而**不再执行函数体**，副作用会被推迟到迭代时；严禁把 Ruby 的 `break v` 机械翻译成生成器里的 `break`（那只是结束本生成器，无法把值作为"调用方方法的返回值"），需要在生成器外用显式标志/返回值重建该语义，或改写为"提前返回"的控制结构。
5. **错误机械替换反例**：
   ```python
   # 错误：把 Ruby 混合了 yield 与 break 的方法直接照抄，副作用时机与返回值语义都变了
   def run_commands(commands):
       for cmd in commands:
           yield cmd.strip()
           break            # 错误：只结束本生成器，无法把值返回给调用方方法
   def run():
       run_commands(commands)          # 错误：生成器未迭代，命令一条都不会执行
   # 正确：不需要产出序列时用显式回调，副作用在调用点发生
   def for_each_command(commands, callback):
       for cmd in commands:
           if not cmd.strip():
               continue
           callback(cmd)
   ```
6. **信息不足或实现相关时的处理**：源码块内出现 `break`/`return` 时必须确认其返回值的接收者与期望的控制流落点，无法确认时停下询问；块是否可能因惰性求值而"永不执行"（例如结果被丢弃、只取前若干项）必须从调用点确认；块内异常是否应传播到调用方也要显式写明，不能默认吞掉。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-PROC](https://docs.ruby-lang.org/en/3.4/Proc.html)；[PY-REF-EXPR-YIELD](https://docs.python.org/3.12/reference/expressions.html)；[PY-LIB-TYPING](https://docs.python.org/3.12/library/typing.html)。

### 规则 RB-PY-06：Ruby 哈希/数组容器与可变默认值陷阱向 Python dict/list 映射
1. **源码触发条件**：Ruby 源码构造并就地修改容器，或把容器当可选参数传递，例如 `com_opts = {}` 后 `com_opts[:net_clr] = 4.0`、`dirs = []` 后 `dirs << ENV['HOME']`、`data[:data] = { :token => token }`、`credential_data.merge!(service_data)`、`dirs.uniq.compact`、`sessions.flatten!`、`ret[s.gsub(...)] = drive`、`avs[avn] = av_note`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)、[RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)）；目标语言 CPython 3.12（[PY-REF-DATA §3.1, §3.3](https://docs.python.org/3.12/reference/datamodel.html)、[PY-LIB-COLLECTIONS](https://docs.python.org/3.12/library/collections.html)）。
3. **原可观察行为**：Ruby `Hash` 保留插入顺序、键可以缺失（`h[k]` 返回 `nil` 而不建键）、允许 `nil` 作为值；`Array#<<`/`merge!`/`flatten!`/`compact!` **就地**修改接收者，因此所有持有同一对象的别名都看到变化；把 Hash/Array 作为方法默认参数时，Ruby 每次调用都重新求值默认表达式，得到新对象。
4. **目标可选写法和不适用条件**：
   - *可选映射*：有序键值对用 `dict`（3.7 起保留插入顺序），缺键读取用 `d.get(k, default)` 或 `if k in d`；就地合并用 `d.update(other)`（对应 `merge!`）；追加用 `list.append(x)`；去重保序用 `dict.fromkeys(seq)`；**默认参数一律写成 `None` 再在函数体内初始化**（`def f(opts=None): opts = {} if opts is None else opts`）。
   - *不适用条件*：**严禁把可变容器直接写成默认参数值**（`def f(opts={})`、`def f(items=[])`）——默认对象在函数定义时创建一次并被所有调用共享，前一次调用的修改会泄漏到后一次，这与 Ruby 每次重新求值默认表达式的行为不同；严禁用 `d[k]` 读取可能缺失的键（会抛 `KeyError`，而 Ruby 返回 `nil`）；严禁假定 `list.sort()`/`reverse()` 的返回值（就地排序返回 `None`，Ruby 的 `sort` 返回新数组）。
5. **错误机械替换反例**：
   ```python
   # 错误：把 Ruby 的可选 Hash 参数翻成可变默认值，多次调用之间相互污染
   def report_note(data, options={}):        # 错误：默认 dict 只创建一次，被所有调用共享
       options['update'] = 'unique_data'
       return options
   # 错误：把 Hash 缺键返回 nil 当成 dict 下标读取
   value = parsed['auths']['auth']           # 错误：缺键抛 KeyError，Ruby 返回 nil
   # 正确：None 哨兵 + 缺键安全读取
   def report_note(data, options=None):
       options = dict(options) if options else {}
       options['update'] = 'unique_data'
       return options
   value = parsed.get('auths', {}).get('auth')
   ```
6. **信息不足或实现相关时的处理**：源码未明确调用方是否依赖"就地修改可见于别名"时，必须标注"别名可观察性待确认"并询问（Python 侧选择就地 `update`/`append` 还是返回新对象取决于这一点）；`uniq`/`compact`/`flatten` 是否承担剔除 `nil` 语义要逐点确认，Python 侧不会自动剔除 `None`；源码里 `Hash` 的插入顺序若被外部观察（输出、文件名），需在报告中写明 Python 侧依赖 3.7+ 的保序保证。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)；[RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)；[PY-REF-DATA §3.1, §3.3](https://docs.python.org/3.12/reference/datamodel.html)；[PY-LIB-COLLECTIONS](https://docs.python.org/3.12/library/collections.html)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
