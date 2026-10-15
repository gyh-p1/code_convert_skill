# Ruby 语言共性语义（CRuby 3.4）

> **用途**：以 Ruby 为源语言或目标语言的任务必读本页，按源码选择适用条目；加载与门禁先见根[转换入口](../../../SKILL.md)。本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 纯面向对象模型；一切变量皆持有对象的引用；可变对象原地修改（如 `String#<<`、`Array#push`），不可变对象包含 `Integer`、`Float`、`Symbol`、`true`、`false`、`nil`。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` 立即数（Immediate values：Fixnum、Symbol 等）在 MRI 中直接编码在指针位中，无独立堆分配，属于实现优化。
- **机械等价禁区与转换约束**：严禁忽视 Ruby 原地方法（带 `!` 或 `<<`）对全部别名持有者的同步副作用；**不得把 Ruby 的真值表（仅 `nil`/`false` 为假）与其他语言的判空互相当作等价**（见下条）。
- **官方资料依据**：RB-DOC-CORE

### L1-RB-01 只有 `nil` 与 `false` 为假：真值判断不等于判空
1. **源码触发条件**：源码用 `if x` / `unless x` / `x || default` / `x && y` 分流，或依赖 `nil.to_s`、`nil` 与缺键/未初始化变量的差异。
2. **冻结版本/运行时/API 前提**：CRuby 3.4；真值与 `nil` 转换语义见 RB-DOC-CONTROL、RB-DOC-NIL。
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
7. **资料依据（名称/版本/章节）**：RB-DOC-CONTROL；RB-DOC-NIL；RB-DOC-HASH。

### L1-RB-05 程序实参不含程序名，`OptionParser` 绑定与帮助输出必须显式重建

1. **源码触发条件**：源码从 `ARGV` 取用实参，或用 `OptionParser`（含 `opts.banner`、`opts.on(...)`）解析，或直接 `ARGV.shift`/`ARGV[i]` 消费参数。
2. **冻结版本/运行时/API 前提**：CRuby 3.4（`ARGV`、`OptionParser`）。
3. **原可观察行为**：
   - **`ARGV` 不含程序名**——`ARGV[0]` 即第一个用户实参（`$0`/`$PROGRAM_NAME` 才是程序名）。
   - `OptionParser#parse!` **就地修改** `ARGV`，返回时 `ARGV` 只剩位置参数；`parse` 则不修改。
   - `OptionParser` 默认支持长选项缩写；须核对选项集合、歧义及 `require_exact` 等实际配置，不能声称“Ruby 不支持缩写”。
   - `-h/--help` 的输出**只有 banner + 选项列表**，没有 `argparse` 的 `description`/`epilog`/完整文档串；该输出属可观察行为。
4. **目标可选写法和不适用条件**：
   - *Ruby 作为源*：目标语言实参序列含程序名时（C/C++/Go/Python）须**补上偏移**；`ARGV[0]` 对应目标 `argv[1]`/`os.Args[1]`/`sys.argv[1]`，整个 `ARGV` 对应目标去掉程序名后的范围。
   - *Ruby 作为目标*：须去掉源程序名偏移；按源解析器的缩写、位置参数和剩余参数义务核对实际 OptionParser 配置。`parse!` 后不能忽略原源应拒绝的残留 `ARGV`。
   - **联合映射守卫与全部使用点**：例如未推进的 C argv 中 `argc < 3` 表示不足两个用户实参，对应 Ruby `ARGV.length < 2`，随后两个参数分别是 `ARGV[0]`、`ARGV[1]`。只改长度守卫而留下旧下标仍错。源/目标已 `shift`、`parse!` 或推进 argv 时重新核当前范围；同时保持缺参默认值、额外参数分支和 `$PROGRAM_NAME` 的诊断用途。
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
7. **资料依据（名称/版本/章节）**：Ruby `OptionParser`、`OptionParser#parse!`、`ARGV`；Python `argparse`。

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` `Integer` 统一表示（具备任意精度整数语义）。
- **有符号溢出行为**：`[语言规范保证]` **无溢出概念**；超出机器字长时自动无缝升级为大数表示。
- **无符号溢出行为**：`[语言规范保证]` 无原生无符号整数；按位操作将负数视为无限补码展开。
- **隐式提升与转换陷阱**：`[语言规范保证]` 位操作中未显式截断可能导致带符号大数，需显式使用 `& ((1 << N) - 1)` 保持位宽。
- **官方资料依据**：RB-DOC-CORE

### L1-RB-02 `to_i` 的宽松解析与格式化区域不得静默改变数值文本
1. **源码触发条件**：源码把字符串转数值（`to_i`/`Integer()`/`Float()`）或把数值转文本（内插 `"#{x}"`、`to_s`、`format`/`sprintf`）。
2. **冻结版本/运行时/API 前提**：CRuby 3.4；`String#to_i` 的**前缀解析**语义见 RB-DOC-STRING、RB-DOC-KERNEL。
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
7. **资料依据（名称/版本/章节）**：RB-DOC-STRING `to_i`；RB-DOC-KERNEL `Integer()`；RB-DOC-KERNEL `format`。

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `String`：可变字节序列，**显式附带 `Encoding` 元数据标签**（默认 UTF-8）。
- **字节序列数据结构**：`[语言规范保证]` 同样为 `String`，其编码标记为 `Encoding::BINARY` (`ASCII-8BIT`)。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` 显式记录长度，允许包含 `\0` 字节；底层 C 扩展遇到 `\0` 可能抛出 `ArgumentError`。
- **编码假设与转换陷阱**：拼接核 Encoding.compatible? 的标签/内容兼容性，不是自动尝试无损转码；不同标签也可能兼容。force_encoding 只改标签不改字节，encode 才转码；valid_encoding? 返回布尔，不因返回 false 本身抛异常。
- **官方资料依据**：RB-DOC-CORE

### L1-RB-03 字节路径必须固定为 BINARY，不得依赖默认 UTF-8
1. **源码触发条件**：源码读写二进制（`File.binread`/`binwrite`、`IO#read` 带长度、`Digest`、`Base64`、`pack`/`unpack`、socket 收发），或在文本与字节之间用 `force_encoding`/`encode` 转换。
2. **冻结版本/运行时/API 前提**：CRuby 3.4；`String#b`、`force_encoding`、`Encoding::BINARY`（`ASCII-8BIT`）与 `encode` 的转换失败语义见 RB-DOC-ENCODING、RB-DOC-STRING。
3. **原可观察行为**：
   - `File.read` 使用**默认外部编码**（通常 UTF-8）并**受 `Encoding.default_external` 影响**；`File.binread` 返回 `ASCII-8BIT`。
   - 字节串默认标记为 UTF-8 时，`valid_encoding?` 可能为假；对非法字节序列 `encode`/正则匹配会抛 `Encoding::InvalidByteSequenceError`/`UndefinedConversionError`。
   - 拼接编码不兼容可抛 CompatibilityError，不等于“标签不同就失败”或自动转码；按实际字符串与 API 核对。
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
7. **资料依据（名称/版本/章节）**：RB-DOC-ENCODING；RB-DOC-STRING；RB-DOC-IO。

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` `Array` 为内建可变序列容器，支持负数下标索引。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `Hash` 为内建键值映射容器。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` **语言规范保证保持键的插入顺序**。
- **迭代期间修改（Fail-Fast）**：`[语言规范保证]` 迭代中修改散列表键值可能导致遗漏或抛出异常。
- **官方资料依据**：RB-DOC-ARRAY<br>RB-DOC-HASH

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` `raise`/`rescue`/`ensure`/`else` 异常结构；异常派生自 `Exception`，常规异常派生自 `StandardError`。
- **异常展开与性能模型**：`[语言规范保证]` 栈回溯与异常对象实例化。
- **进程退出码回传机制**：`[语言规范保证]` `exit(int)` 抛出 `SystemExit` 异常；`exit!` 绕过 `ensure` 立即底层退出。
- **跨语言映射关键风险**：`rescue => e` 默认只捕获 `StandardError`，不捕获 `Exception`（如 `NoMemoryError`、`SignalException`）。
- **官方资料依据**：RB-DOC-EXCEPT

### L1-RB-04 被丢弃的错误不得变成异常终止，主动失败不得被 `rescue` 吞掉
1. **源码触发条件**：源码**有意忽略**失败（不检查返回的 `nil`/`false`、裸 `File.open`、`rescue` 后继续），**或**在失败时 `raise`、`abort`、`exit(非零)`、`warn` 后返回错误状态。
2. **冻结版本/运行时/API 前提**：CRuby 3.4；异常层次（`Exception` vs `StandardError`）与 `exit`/`exit!` 语义见 RB-DOC-EXCEPT、RB-DOC-KERNEL。
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
7. **资料依据（名称/版本/章节）**：RB-DOC-EXCEPT；RB-DOC-ERRNO；RB-DOC-KERNEL `exit`/`exit!`。

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[指定运行时的实现相关事实]` MRI 内存管理；自动垃圾回收（RGenGC）；非托管资源需手动绑定。
- **资源确定性释放机制**：`[语言规范保证]` 代码块闭包确保资源释放模式（如 `File.open(...) do |f| ... end` 保证自动关闭）。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 分代三色 RGenGC；GC 扫描期间受运行时机制支配。
- **悬垂与泄漏防范**：遗漏 block 形式直接调用裸 `File.open` 会导致文件描述符泄漏直至下一次 GC。
- **官方资料依据**：RB-DEV-GC

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` `Thread`；`Fiber`（轻量协作式协程）。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` MRI 全局 VM 锁（GVL）限制多线程同一时刻仅有一个在 CPU 上执行 Ruby 字节码。
- **级联取消与超时机制**：`[语言规范保证]` 线程超时控制（`Timeout.timeout`）；Fiber 协作式让出控制权。
- **内存模型与数据竞争**：`[指定运行时的实现相关事实]` 跨线程共享可变对象需互斥锁（`Mutex`）保护。
- **官方资料依据**：RB-DEV-GC<br>RB-DOC-THREAD

## 八、输出终止符

### 输出换行：puts 与字节写入

迁入原进程场景的语言事实：Ruby puts 的字符串参数已有换行时不再追加，不能视为无条件追加终止符；print/STDOUT.write 的字节输出与 puts 分开。对哈希、JSON 行或协议文本先核源函数的终止符规则。该事实不要求源码创建子进程。来源：Ruby Kernel#puts。

## 九、进程返回、替换与环境

### L1-RB-06 fork 的父、子与失败分支分别映射

1. **触发**：源码依赖 fork 返回值、调用后续语句或退出清理。
2. **前提**：CRuby 3.4，冻结 OS 是否提供 fork、是否有 block、线程与退出钩子；不从语言版本推定平台支持。
3. **事实**：无 block 的 fork 在父进程返回子 PID、子进程返回 nil；0 在 Ruby 中为真。带 block 时子进程执行 block，正常结束即退出，不继续外部后续语句。创建失败须按异常路径处理，不假定返回 C 的 -1。
4. **映射条件**：逐一对应源父/子/失败出口及等待、退出钩子；无 block 与 block 不是同形替换。源 C/POSIX 事实另读[进程系统页](../../systems/posix-windows-process-identity/SKILL.md#原生-forkexec-事实)。
5. **反例**：照抄 C 的 `pid == 0` 会漏掉 Ruby 子分支；为简洁改成 block 可能丢失源子进程的后续语句。
6. **未知**：平台不支持或源分支/退出钩子未知，记映射缺口；spawn 不提供内存副本，不自动视为等价。
7. **依据**：Ruby 3.4 Process.fork 方法说明；CRuby v3_4_0 的 process.c / rb_f_fork 实现。本条所需返回、分支与未知条件已在正文列明。

### L1-RB-07 exec 的环境与失败续行

1. **触发**：替换自身映像、指定环境或处理 exec 失败。
2. **前提**：CRuby 3.4，冻结调用形态、argv、OS 与环境契约。
3. **事实**：成功 exec 不回到 Ruby 调用点；失败抛异常。省略环境或传空 hash 默认仍继承；环境 hash 修改继承项，nil 值删除该项；`unsetenv_others: true` 清除其他项。直接参数形式与 shell 命令字符串分别核对。
4. **映射条件**：显式区分继承、合并覆盖、完整替换及空环境；源失败后继续时只处理该调用适用的异常并保持后续出口，不扩大 rescue 范围。
5. **反例**：把空 hash 当空环境；把 exec 改 system 后继续；让 C 的失败返回变成未捕获异常，均可能改变可观察行为。
6. **未知**：Linux 的 NULL envp 不能外推到其他 OS，见[系统页](../../systems/posix-windows-process-identity/SKILL.md#原生-forkexec-事实)；诊断、环境与失败路径未知时不猜。
7. **依据**：Kernel.exec；Ruby 执行环境与选项。

## 十、空白集合与临时目录

### L1-RB-08 strip 不是通用 Unicode 空白删除

1. **触发**：strip/lstrip/rstrip、空白判定或去空白后分支。
2. **前提**：CRuby 3.4 String 方法，冻结编码；正则、split 和应用自定义谓词另核。
3. **事实**：上述 String 去空白方法的集合为 NUL、HT、LF、VT、FF、CR、普通空格；不等于 Unicode White_Space。strip! 还须保持原地修改及未改变时返回 nil。
4. **映射条件**：按源方法实际集合、两端/全部删除、变异与返回值选择目标谓词，不按“空白”名称套 API。
5. **反例**：换成 Go TrimSpace 会删去源 strip 保留的 U+00A0，并保留源 strip 会删的 NUL。
6. **未知**：源用正则或自定义集合时定位定义；缺编码/定义只记录条件差异，不定案历史缺陷。
7. **依据**：Ruby String 空白定义；strip!。

### L1-RB-09 Dir.tmpdir 的候选顺序与有效性

1. **触发**：源码调用 tmpdir 标准库的 Dir.tmpdir 或依赖临时目录路径。
2. **前提**：冻结实际 tmpdir 库版本、OS、环境和初始目录状态；这里依据 Ruby v3_4_0 附带实现。
3. **事实**：依次尝试 TMPDIR、TMP、TEMP、系统临时路径、/tmp、当前目录；跳过空值及不适用候选，核目录、可写性和 world-writable/sticky 条件，找不到时抛错；会展开路径并可能写警告。
4. **映射条件**：保持候选优先级、有效性、路径展开与错误/警告；不把“返回临时路径”换成“创建目录”。
5. **反例**：Unix 上直接用 Go os.TempDir，可能忽略 TMP/TEMP 或返回 Ruby 会拒绝的路径。
6. **未知**：库可能独立升级，准确版本未知不得把此顺序当已核事实；用户显式目录优先按源调用处理。
7. **依据**：Ruby v3_4_0 的 lib/tmpdir.rb / Dir.tmpdir / Tmpname::TMPDIR_CANDIDATES；本条正文保留了所需候选顺序、校验与失败条件。

## 十一、终端键输入

### L1-RB-10 getch、getc 与 gets 的输入单位不同

1. **触发**：交互暂停、读键/字符/整行、回显或终端模式。
2. **前提**：CRuby 3.4，io/console 的实际版本、OS、输入设备与编码；合法驱动来源另见[评估准备](../../../references/framework/evaluation-readiness-contract.md)。
3. **事实**：io/console 的 getch 在 raw 模式读取字符，须加载 io/console；getc 读流字符，gets 读行。getch 不直接给出 .NET ConsoleKeyInfo 的完整键/修饰键对象。
4. **映射条件**：按源消费单位、回显、特殊键、EOF/失败与模式恢复选择；确认输入设备，不把流读取视为终端键事件。
5. **反例**：用 gets 暂停替代单键等待会增加换行要求；只取 getch 字符可能丢失源修饰键分支。
6. **未知**：无合法终端入口属于准备缺口，不伪造源栈、不删暂停或静默改读整行；只做文本/仅编译的适用性由契约定。
7. **依据**：Ruby IO.getch/getc/gets。

## 十二、标准库替换的选择引导

以CRuby3.4和实际gem/标准库版本为前提。优先保持源的调用与消费者，不把所有API同名视作等价。

| 使用点 | 引导及易错边界 |
|---|---|
| 读取及rescue | 先核读取单位、长度、EOF、已经取得的部分数据和异常范围；从Go迁入时关注n与error同时存在，不能因异常丢掉已得数据，也不为继续执行rescue整个业务函数 |
| Base64/数值解析 | 核严格/宽松API、非法字符、空白、padding、返回编码与异常；源严格不选宽松以求成功，源宽松也不无条件升级为严格 |
| split/Hash/排序 | 看首尾空项、limit、首个等号、重复键、缺键默认与是否变异；稳定性按源义务，不把语言便利语法作为重排授权 |
| ENV读取与回退 | CRuby3.4 ENV[name] 未设置返回nil，已设置值按实际OS/运行时取得；取得空串与nil不同。源只对缺失回退时保持nil判断，不无条件追加empty?或先to_s；写入空值的OS差异另核，不凭environment={}推定路径已覆盖。依据：Ruby3.4 ENV.[]、ENV.[]=及本页L1-RB-01 |
| 路径存在与对象类型 | File.exist? 以stat成功判存在，普通文件和目录均可；File.directory?只接受目录（含指向目录的链接），File.file?另判普通文件。按源谓词、链接与错误保持接受集合；C++ exists守卫后遍历的失败不能变成directory?为假后成功空跑。目标谓词stat失败可返回false，不自动保持源异常重载。未知权限/链接/错误条件单列。依据：Ruby3.4 File.exist?/directory?/file?；C++来源另读其语言页L1-CPP-06 |
| 创建文件/目录与临时目录 | 创建模式/umask、已存在文件的权限改变、递归与末级创建分别看API；Dir.tmpdir的候选校验见L1-RB-09，不等同只返回路径 |
| fork/exec/等待 | Ruby fork的子返回nil、父返回PID、失败异常与C的0/-1形态不同；先核成功/失败出口和映像替换，再选择目标。等待状态不直接当退出码，单流拼接不代合流交错 |

依据：Ruby3.4 IO/String/Hash/Kernel/Process及Base64库精确版本；fork/exec详细事实见本页§九和进程系统页。无法核具体库版本时只记该API缺口，不扩大rescue或补造入口。

## 使用边界

将本页与所选方向和另一语言事实页组合；具体场景/系统差异按[共性索引](../seven-language-common-semantics.md)选读。缺逐例第三方证据保持 UNVERIFIED，本机不运行或编译。
