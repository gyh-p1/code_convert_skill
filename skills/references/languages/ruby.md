# Ruby 语言共性语义（CRuby 3.4）

> **用途**：供以 Ruby 为源语言或目标语言的方向 Skill 按需读取；本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 纯面向对象模型；一切变量皆持有对象的引用；可变对象原地修改（如 `String#<<`、`Array#push`），不可变对象包含 `Integer`、`Float`、`Symbol`、`true`、`false`、`nil`。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` 立即数（Immediate values：Fixnum、Symbol 等）在 MRI 中直接编码在指针位中，无独立堆分配，属于实现优化。
- **机械等价禁区与转换约束**：严禁忽视 Ruby 原地方法（带 `!` 或 `<<`）对全部别名持有者的同步副作用；**不得把 Ruby 的真值表（仅 `nil`/`false` 为假）与其他语言的判空互相当作等价**（见下条）。
- **官方资料依据**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)

### L1-RB-01 只有 `nil` 与 `false` 为假：真值判断不等于判空
1. **源码触发条件**：源码用 `if x` / `unless x` / `x || default` / `x && y` 分流，或依赖 `nil.to_s`、`nil` 与缺键/未初始化变量的差异。
2. **冻结版本/运行时/API 前提**：CRuby 3.4；真值与 `nil` 转换语义见 [RB-DOC-CONTROL](https://docs.ruby-lang.org/en/3.4/syntax/control_expressions_rdoc.html)、[RB-DOC-NIL](https://docs.ruby-lang.org/en/3.4/NilClass.html)。
3. **原可观察行为**：
   - **只有 `nil` 与 `false` 为假**；`0`、`""`、`[]`、`{}`、`0.0` **全为真**。这是与 C 判空、Python 假值集合最易混淆之处。
   - `nil.to_s` → `""`；`nil.to_a` → `[]`；`nil.to_i` → `0`——`nil` 对多数转换方法有定义，不会抛 `NoMethodError`。
   - 未初始化的实例变量、`Hash#[]` 的缺键都返回 `nil`；`Hash#fetch` 缺键则抛 `KeyError`。
   - `defined?(x)` 与 `x.nil?` 判的是“是否已定义”与“是否为 nil”，二者不同。
4. **目标可选写法和不适用条件**：
   - *Ruby 作为源*：保留完整假值集合 `nil/false`。映射 Python 时可用 `x is not None and x is not False`；只写 `x is not None` 会漏掉 false，用 `x != False` 又会误并入 0。源已明确排除布尔 false 时才可只判空。
   - *Ruby 作为目标*：源为静态类型语言时，判空映射为 `x.nil?`，零值/空内容映射为 `x.zero?`/`x.empty?`。源为 Python 时尤其注意：Python `if x` 为假的情形在 Ruby 中大多为真，**必须补显式判空**。
   - *不适用条件*：源已经显式写 `!x.nil?` 时只保留判空，不新增 false 判断；普通 `if x` 则须同时处理 nil 与 false。
5. **错误机械替换反例**：
   ```ruby
   # 错误：把 Python 的 if not x 搬成 Ruby if x，分支方向与真值集合均改变
   return nil if user_input
   # 错误之三：假定 nil 与缺键是一回事
   v = h["k"]                    # 缺键得 nil；源若预期 KeyError 行为则不同
   # 正确：显式表达 nil / 空 / 零
   return nil if user_input.nil?
   return nil if user_input.empty?      # Python 中 "" 为假 → 对应这里
   return nil if user_input.zero?       # Python 中 0 为假 → 对应这里
   return nil unless err.nil?           # 源 err != nil 的非空错误分支
   v = h.fetch("k")                     # 源预期缺键即失败时
   ```
6. **信息不足或实现相关时的处理**：若无法确认源的判断表达“未设置（nil/缺键）”还是“值为零/空”，必须标注“nil 与零值语义待确认”，不得用统一真值判断合并两者。**特别注意**：`nil.to_s → ""` 会让“nil 被当成空串”在 Ruby 中静默通过，掩盖了语义差异。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CONTROL](https://docs.ruby-lang.org/en/3.4/syntax/control_expressions_rdoc.html)；[RB-DOC-NIL](https://docs.ruby-lang.org/en/3.4/NilClass.html)；[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)。

### L1-RB-05 程序实参不含程序名，`OptionParser` 绑定与帮助输出必须显式重建

1. **源码触发条件**：源码从 `ARGV` 取用实参，或用 `OptionParser`（含 `opts.banner`、`opts.on(...)`）解析，或直接 `ARGV.shift`/`ARGV[i]` 消费参数。
2. **冻结版本/运行时/API 前提**：CRuby 3.4（[`ARGV`](https://docs.ruby-lang.org/en/3.4/ARGF.html)、[`OptionParser`](https://docs.ruby-lang.org/en/3.4/OptionParser.html)）。
3. **原可观察行为**：
   - **`ARGV` 不含程序名**——`ARGV[0]` 即第一个用户实参（`$0`/`$PROGRAM_NAME` 才是程序名）。
   - `OptionParser#parse!` **就地修改** `ARGV`，返回时 `ARGV` 只剩位置参数；`parse` 则不修改。
   - `OptionParser` 默认支持长选项缩写；须核对选项集合、歧义及 `require_exact` 等实际配置，不能声称“Ruby 不支持缩写”。
   - `-h/--help` 的输出**只有 banner + 选项列表**，没有 `argparse` 的 `description`/`epilog`/完整文档串；该输出属可观察行为。
4. **目标可选写法和不适用条件**：
   - *Ruby 作为源*：目标语言实参序列含程序名时（C/C++/Go/Python）须**补上偏移**；`ARGV` 对应目标 `argv[1]`/`os.Args[1]`/`sys.argv[1]`。
   - *Ruby 作为目标*：须去掉源程序名偏移；按源解析器的缩写、位置参数和剩余参数义务核对实际 OptionParser 配置。`parse!` 后不能忽略原源应拒绝的残留 `ARGV`。
   - *不适用条件*：源码不使用命令行实参时不适用；源禁用缩写时须主动匹配该策略，不能依赖目标默认值。
5. **错误机械替换反例**：
   ```ruby
   # 错误一：把 C 的 argv 下标直接搬到 Ruby（ARGV 不含程序名）
   path = ARGV[1]                # 源 C 的 argv[1] 应是这里的 ARGV[0]
   # 错误二：源拒绝多余位置参数，目标 parse! 后却不检查残留 ARGV
   opts.parse!
   # 后续直接执行业务，遗漏原 argparse 的额外参数错误路径
   # 错误三：用 OptionParser 冒充 argparse 的帮助输出
   opts.banner = 'Usage: tool [options]'   # 缺源 argparse 的 description/epilog 全文
   # 正确（按源义务逐项重建）
   path = ARGV[0]
   # 按源规则处理残留参数、缩写歧义与完整帮助文本，不能只更换解析器名
   ```
6. **信息不足或实现相关时的处理**：无法确定源是否依赖唯一前缀、或源帮助文本的完整构成时，标为“实参绑定与帮助输出待确认”；不得以 `OptionParser` 的默认输出充当等价。
7. **直接官方 HTTPS 依据链接**：[Ruby `OptionParser`](https://docs.ruby-lang.org/en/3.4/OptionParser.html)、[`OptionParser#parse!`](https://docs.ruby-lang.org/en/3.4/OptionParser.html#method-i-parse-21)、[`ARGV`](https://docs.ruby-lang.org/en/3.4/ARGF.html)；[Python `argparse`](https://docs.python.org/3.12/library/argparse.html)。

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` `Integer` 统一表示（具备任意精度整数语义）。
- **有符号溢出行为**：`[语言规范保证]` **无溢出概念**；超出机器字长时自动无缝升级为大数表示。
- **无符号溢出行为**：`[语言规范保证]` 无原生无符号整数；按位操作将负数视为无限补码展开。
- **隐式提升与转换陷阱**：`[语言规范保证]` 位操作中未显式截断可能导致带符号大数，需显式使用 `& ((1 << N) - 1)` 保持位宽。
- **官方资料依据**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)

### L1-RB-02 `to_i` 的宽松解析与格式化区域不得静默改变数值文本
1. **源码触发条件**：源码把字符串转数值（`to_i`/`Integer()`/`Float()`）或把数值转文本（内插 `"#{x}"`、`to_s`、`format`/`sprintf`）。
2. **冻结版本/运行时/API 前提**：CRuby 3.4；`String#to_i` 的**前缀解析**语义见 [RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)、[RB-DOC-KERNEL](https://docs.ruby-lang.org/en/3.4/Kernel.html)。
3. **原可观察行为**：
   - `String#to_i` **宽松解析**：`"12abc".to_i == 12`、`"abc".to_i == 0`、`"  42  ".to_i == 42`，**不抛异常**；`Integer("abc")` 才抛 `ArgumentError`。二者不可互替。
   - `Integer` **无溢出**：超出机器字长自动升级为大数；无原生无符号整数。
   - `"#{f}"` 使用最短往返表示；`format("%.6f", f)` 等固定精度**位数不同**。
   - 数值格式化**不受区域设置影响**（Ruby 不使用 locale 切换 `Float#to_s` 的小数点）。
4. **目标可选写法和不适用条件**：
   - *Ruby 作为源*：源用 `to_i` 的宽松解析时，目标必须复现“前缀解析 + 失败给 0”的语义；源用 `Integer()` 的严格解析时，目标必须**抛错**而不是返回 0。
   - *Ruby 作为目标*：源为 .NET 时注意 `int.TryParse`/`Parse` 与 `to_i` 的三方差异；源为 Python 时注意 `int("12abc")` **抛 `ValueError`** 而 `to_i` 返回 12。
   - *不适用条件*：源本身只做无限精度算术且无字符串解析时，不涉及解析差异；但**格式化位数**仍需核对。
5. **错误机械替换反例**：
   ```ruby
   # 错误：把 Python 的严格 int() 语义套到 Ruby，或反之
   n = "12abc".to_i            # Ruby：12（宽松解析，不报错）
   # target.py: n = int("12abc")   # Python：ValueError → 控制流已改变
   # 错误之二：用默认 to_s 冒充源的固定精度
   s = (1.0 / 3).to_s          # 位数可能与源不同
   # 正确：按源的解析严格性分别重建
   n = Integer("12abc") rescue 0      # 需要严格解析并显式兜底时
   s = format("%.17g", 1.0 / 3)       # 精度按源义务冻结
   ```
6. **信息不足或实现相关时的处理**：无法确定源的解析严格性与有效位数时，标为“解析严格性与数值格式待确认”；不得用 `to_i` 的返回 0 冒充“解析成功得到 0”。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-STRING `to_i`](https://docs.ruby-lang.org/en/3.4/String.html#method-i-to_i)；[RB-DOC-KERNEL `Integer()`](https://docs.ruby-lang.org/en/3.4/Kernel.html#method-i-Integer)；[RB-DOC-KERNEL `format`](https://docs.ruby-lang.org/en/3.4/Kernel.html#method-i-format)。

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `String`：可变字节序列，**显式附带 `Encoding` 元数据标签**（默认 UTF-8）。
- **字节序列数据结构**：`[语言规范保证]` 同样为 `String`，其编码标记为 `Encoding::BINARY` (`ASCII-8BIT`)。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` 显式记录长度，允许包含 `\0` 字节；底层 C 扩展遇到 `\0` 可能抛出 `ArgumentError`。
- **编码假设与转换陷阱**：`[语言规范保证]` 两个不同 Encoding 的 String 进行拼接时，若无法无损转码将抛出 `Encoding::CompatibilityError`。
- **官方资料依据**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)

### L1-RB-03 字节路径必须固定为 BINARY，不得依赖默认 UTF-8
1. **源码触发条件**：源码读写二进制（`File.binread`/`binwrite`、`IO#read` 带长度、`Digest`、`Base64`、`pack`/`unpack`、socket 收发），或在文本与字节之间用 `force_encoding`/`encode` 转换。
2. **冻结版本/运行时/API 前提**：CRuby 3.4；`String#b`、`force_encoding`、`Encoding::BINARY`（`ASCII-8BIT`）与 `encode` 的转换失败语义见 [RB-DOC-ENCODING](https://docs.ruby-lang.org/en/3.4/Encoding.html)、[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)。
3. **原可观察行为**：
   - `File.read` 使用**默认外部编码**（通常 UTF-8）并**受 `Encoding.default_external` 影响**；`File.binread` 返回 `ASCII-8BIT`。
   - 字节串默认标记为 UTF-8 时，`valid_encoding?` 可能为假；对非法字节序列 `encode`/正则匹配会抛 `Encoding::InvalidByteSequenceError`/`UndefinedConversionError`。
   - 两个不同 Encoding 拼接且无法无损转码 → 抛 `Encoding::CompatibilityError`。
   - `String#length` 是**字符数**（按编码标签计），`bytesize` 才是字节数。
4. **目标可选写法和不适用条件**：
   - *Ruby 作为源*：字节路径用 `String#b` 或 `force_encoding(Encoding::BINARY)` 固定为 `ASCII-8BIT` 再做摘要/编码/打包；文本路径显式标 `Encoding::UTF_8` 并在边界转换。
   - *Ruby 作为目标*：源若以字节为单位，必须走 `binread`/`binwrite` 并固定 BINARY，**不得**用 `File.read` 承接；源若为文本，须显式写编码并保留源对非法字节的处理方式。
   - *不适用条件*：源本身是文本 API 且编码转换失败属源的可观察行为时，该失败路径应**保留**而非消除。
5. **错误机械替换反例**：
   ```ruby
   # 错误：把字节路径写成文本路径，校验和随之改变
   content = File.read(path)                     # 默认外部编码 + 非法字节风险
   hex = Digest::SHA256.hexdigest(content)       # 与源不一致
   # 错误之二：对二进制内容调用可能抛 Encoding 异常的字符串操作
   blob = raw.force_encoding('UTF-8')
   blob =~ /pattern/                             # 非法序列可能抛异常，改变控制流
   # 错误之三：用替换策略掩盖差异
   text = raw.encode('UTF-8', invalid: :replace, undef: :replace)   # 内容与长度都被改写
   # 正确：字节进字节出，必要时在边界显式解码
   content = File.binread(path).force_encoding(Encoding::BINARY)
   hex = Digest::SHA256.hexdigest(content)
   text = content.dup.force_encoding(Encoding::UTF_8)
   ```
6. **信息不足或实现相关时的处理**：无法确认源的编码、或源依赖按字节的长度与切片语义时，标为“编码与字节长度语义待确认”；**禁止**用 `scrub`/`encode(invalid: :replace)` 掩盖差异。也不得用 `String#length` 承接源按字节计的长度。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-ENCODING](https://docs.ruby-lang.org/en/3.4/Encoding.html)；[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)；[RB-DOC-IO](https://docs.ruby-lang.org/en/3.4/IO.html)。

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` `Array` 为内建可变序列容器，支持负数下标索引。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `Hash` 为内建键值映射容器。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` **语言规范保证保持键的插入顺序**。
- **迭代期间修改（Fail-Fast）**：`[语言规范保证]` 迭代中修改散列表键值可能导致遗漏或抛出异常。
- **官方资料依据**：[RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)<br>[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` `raise`/`rescue`/`ensure`/`else` 异常结构；异常派生自 `Exception`，常规异常派生自 `StandardError`。
- **异常展开与性能模型**：`[语言规范保证]` 栈回溯与异常对象实例化。
- **进程退出码回传机制**：`[语言规范保证]` `exit(int)` 抛出 `SystemExit` 异常；`exit!` 绕过 `ensure` 立即底层退出。
- **跨语言映射关键风险**：`rescue => e` 默认只捕获 `StandardError`，不捕获 `Exception`（如 `NoMemoryError`、`SignalException`）。
- **官方资料依据**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)

### L1-RB-04 被丢弃的错误不得变成异常终止，主动失败不得被 `rescue` 吞掉
1. **源码触发条件**：源码**有意忽略**失败（不检查返回的 `nil`/`false`、裸 `File.open`、`rescue` 后继续），**或**在失败时 `raise`、`abort`、`exit(非零)`、`warn` 后返回错误状态。
2. **冻结版本/运行时/API 前提**：CRuby 3.4；异常层次（`Exception` vs `StandardError`）与 `exit`/`exit!` 语义见 [RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)、[RB-DOC-KERNEL](https://docs.ruby-lang.org/en/3.4/Kernel.html)。
3. **原可观察行为**：
   - 多数 I/O 失败在 Ruby 中**以异常报告**：`File.open` 缺文件抛 `Errno::ENOENT`。若源语言丢弃该错误，Ruby 版必须显式 `rescue` 才能复现“继续执行”。
   - `rescue => e` **只捕获 `StandardError`**，`NoMemoryError`/`SignalException`/`SystemExit` 会穿透——这是与 `rescue Exception` 的重要区别。
   - `exit(n)` 抛 `SystemExit`（可被 `ensure`/`rescue Exception` 拦截）；**`exit!` 绕过 `ensure` 立即退出**。
   - 未捕获异常的退出码为 **1**。
4. **目标可选写法和不适用条件**（两个方向都必须覆盖）：
   - *源丢弃错误 → 目标不得变成异常终止*：只在源**确实**忽略该失败时，把对应系统错误转成 `nil`/`false` 并保留后续路径；用 `rescue SystemCallError` 精确限定，**不要**用包围整个函数的宽泛 `rescue`。
   - *源主动失败 → 目标不得静默继续*：不得用 `rescue => e; end` 把失败吞成成功；也不得用 `exit!` 代替 `exit`（`exit!` 跳过 `ensure` 清理，等价于跳过源里的清理义务）。
   - *不适用条件*：源**确实检查**并主动返回失败时，必须保留该失败分支，不能套用“忽略并继续”。
5. **错误机械替换反例**：
   ```ruby
   # 错误：源忽略打开失败并继续，目标让异常逃逸终止
   f = File.open(path, 'rb')          # Errno::ENOENT 未处理 → 提前终止
   # 错误之二：把源主动失败的路径吞掉
   begin
     run
   rescue => e
     # 静默继续，退出码变成 0
   end
   # 正确：按源的实际检查行为分别重建
   f = begin
     File.open(path, 'rb')
   rescue SystemCallError               # 仅当源确实忽略打开失败时
     nil
   end
   begin
     f.each_line { |line| consume(line) } if f
   ensure
     f&.close
   end
   ```
6. **信息不足或实现相关时的处理**：不清楚源是否检查返回值、是否输出诊断、失败后是否继续时，**不能断言退出码和产物**；把打开失败路径单列为待验证 oracle。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[RB-DOC-ERRNO](https://docs.ruby-lang.org/en/3.4/Errno.html)；[RB-DOC-KERNEL `exit`/`exit!`](https://docs.ruby-lang.org/en/3.4/Kernel.html#method-i-exit)。

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[指定运行时的实现相关事实]` MRI 内存管理；自动垃圾回收（RGenGC）；非托管资源需手动绑定。
- **资源确定性释放机制**：`[语言规范保证]` 代码块闭包确保资源释放模式（如 `File.open(...) do |f| ... end` 保证自动关闭）。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 分代三色 RGenGC；GC 扫描期间受运行时机制支配。
- **悬垂与泄漏防范**：遗漏 block 形式直接调用裸 `File.open` 会导致文件描述符泄漏直至下一次 GC。
- **官方资料依据**：[RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` `Thread`；`Fiber`（轻量协作式协程）。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` MRI 全局 VM 锁（GVL）限制多线程同一时刻仅有一个在 CPU 上执行 Ruby 字节码。
- **级联取消与超时机制**：`[语言规范保证]` 线程超时控制（`Timeout.timeout`）；Fiber 协作式让出控制权。
- **内存模型与数据竞争**：`[指定运行时的实现相关事实]` 跨线程共享可变对象需互斥锁（`Mutex`）保护。
- **官方资料依据**：[RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)<br>[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)

## 使用边界

将本页与所选的源→目标方向 Skill 及另一语言的共性页组合使用；映射前先确认源码真实行为。文件、网络、并发和跨 OS API 的具体差异仍按[共性索引的场景/系统分流](../seven-language-common-semantics.md)选读，不从语言事实直接推断系统 API 等价。没有逐例第三方证据时，语法/构建与功能结论保持 `UNVERIFIED`；本机不运行或编译样本。
