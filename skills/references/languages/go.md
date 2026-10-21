# Go 语言共性语义（Go 1.27）

> **用途**：以 Go 为源语言或目标语言的任务必读本页，按源码选择适用条目；加载与门禁先见根[转换入口](../../../SKILL.md)。本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：按条目中的语言版本、资料依据和源码触发条件选择适用事实；跨语言关注点见[七语言共性索引](../seven-language-common-semantics.md)。目标工具链能力与编译、行为结论须依据本项精确版本的独立证据。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 严格纯值传递；指针传递指针值（内存地址拷贝），显式指针禁用算术运算（除 `unsafe.Pointer`）；切片、map、channel、interface 内部包含指针头部，值传递时其底层数据共享。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` 编译器逃逸分析（Escape Analysis）决定变量分配在 Goroutine 栈还是堆上，属于编译器实现细节，语言规范不作物理存储位置保证。
- **机械等价禁区与转换约束**：不可认为切片传递是深拷贝（共享底层数组）；切片扩容后会静默与原数组分离；**不得把 Go 的 `nil`/零值判定与其他语言的真值判定互相当作等价**（见下条）。
- **官方资料依据**：GO-SPEC #Type_identity, #Slice_types

### L1-GO-01 零值、nil 与长度是三种不同判定
1. **源码触发条件**：源码用 `if err != nil`、`if x == ""`、`if len(b) == 0`、`if v, ok := m[k]; ok`、`if fi.IsDir()` 之类的判断分流，或用 `map[string]string` 承接解析结果。
2. **冻结版本/运行时/API 前提**：Go 1.27；零值与比较语义见 GO-SPEC #The_zero_value, #Comparison_operators，nil map 的读写差异见 GO-SPEC #Map_types。
3. **原可观察行为**：
   - 只有显式的 `nil`/零值比较才为真；`0`、`""`、空切片、空 map 都是**普通值**，参与布尔上下文时必须写比较式（Go 没有隐式真值转换）。
   - `len(x) == 0` 与 `x == nil` 是**不同**判断：空但非 nil 的切片两者结果不同。
   - 从 nil map **读取**返回零值；向 nil map **写入** panic。
4. **目标可选写法和不适用条件**：
   - *Go 作为源*：nil 状态映射到目标的 null/nil/None 检查，长度/内容判断映射到目标的 `empty?`/`== ""`/`zero?` 等；需要区分“缺键”时用 `fetch`/`key?`/`ContainsKey` 而不是默认取值。
   - *Go 作为目标*：源语言的真值判定必须**显式重建为比较**；源里 `if x` 在 Go 中不可直接编译（非布尔），不要企图用 `if x != 0` 一律替代——先确认源判的是哪种“空”。
   - *不适用条件*：源判的是纯数值零值时，不涉及 nil，不要加 nil 检查。
5. **错误机械替换反例**：
   ```go
   // 错误：把其他语言的 if x 真值判断搬成 nil 比较，漏掉空串/零值形态
   if err != nil { return err }          // 源若是 if err（err 为 ""/0 亦为假）则语义已被取反
   // 错误之二：假定从 nil map 写入会返回零值
   var m map[string]int
   m["k"]++                              // panic: assignment to entry in nil map
   // 正确：分别表达 nil、长度与缺键
   if err != nil { return err }
   if len(b) == 0 { /* 空内容分支，与 nil 分开 */ }
   if v, ok := m[k]; ok { use(v) }
   ```
6. **信息不足或实现相关时的处理**：无法确认源的判断表达“未设置（nil/缺键）”还是“值为零/空”时，必须标为“nil 与零值语义待确认”，不得用统一真值判断合并两者。目标语言为动态语言时，须先核对该语言的假值集合（Ruby 只有 `nil`/`false` 为假，`""` 与 `0` 为真）。
7. **资料依据（名称/版本/章节）**：GO-SPEC #The_zero_value, #Comparison_operators, #Map_types。

### L1-GO-05 程序实参含程序名，flag 解析与参数消费必须显式重建

1. **源码触发条件**：源码从 `os.Args` 取用实参、用 `flag` 包解析，或在 `flag.Parse()` 后读取 `flag.Args()`/`os.Args[1:]`。
2. **冻结版本/运行时/API 前提**：Go 1.27（`os.Args`、`flag`）。
3. **原可观察行为**：
   - **`os.Args[0]` 是程序名**，用户实参从 **`os.Args[1]`** 开始——与 C# `args`、Ruby `ARGV`（**不含**程序名）不同。
   - `flag` 包在遇到**第一个非 flag 参数**时即停止解析（与 GNU `getopt` 的**置换**行为相反）；之后的参数**不会**被当作 flag。
   - `flag.Parse()` 会向 **stderr** 写出 flag 用法/错误，并在遇到未定义 flag 时以**状态码 2** 退出。
4. **目标可选写法和不适用条件**：
   - *Go 作为源*：目标语言实参序列不含程序名时须**去掉 `os.Args[0]`**；反之（目标含程序名，如 C/C++/Python `sys.argv`）须保留偏移。
   - *Go 作为目标*：源的"无实参"须由 `len(os.Args) <= 1` 表达，不得用 `os.Args[0] == ""`；源若依赖 flag 与操作数**交错**（GNU 式）而 Go `flag` 不支持，必须显式重建该解析。
   - *不适用条件*：源码不使用命令行实参时不适用。
5. **错误机械替换反例**：
   ```go
   // 错误一：把 C#/Ruby 的“不含程序名”习惯套到 os.Args
   path := os.Args[0]              // 取到的是程序名
   // 错误二：假定 flag 会像 GNU getopt 一样置换
   //   `prog operands -verbose` 中 -verbose 不会被解析（flag 在第一个非 flag 处停止）
   // 正确
   if len(os.Args) < 2 { usage() }
   path := os.Args[1]
   ```
6. **信息不足或实现相关时的处理**：无法确认源是否依赖 flag 与操作数交错、或目标语言实参序列是否含程序名时，标为“实参偏移与解析器语义待确认”。
7. **资料依据（名称/版本/章节）**：Go `os.Args`、`flag` 包（解析停止与退出码 2）、`flag.Parse`。

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` `int8`..`int64`, `uint8`..`uint64` 严格定宽；`int`/`uint` 大小取决于架构（32 或 64 位）；`uintptr` 存指针位。
- **有符号溢出行为**：`[语言规范保证]` **按补码截断回绕**（二进制算术确定行为，非 UB）；**常数表达式溢出属于编译错误**。
- **无符号溢出行为**：`[语言规范保证]` **按模截断回绕**（二进制算术确定行为）。
- **隐式提升与转换陷阱**：`[语言规范保证]` 不同整数类型的变量不能只因位宽相同就视为可隐式互换；冻结具体类型与实现宽度，不假定 int32 与 x64 实现的 int 同宽。
- **官方资料依据**：GO-SPEC #Numeric_types, #Arithmetic_operators

### L1-GO-02 数值文本输出必须钉住位宽与格式
1. **源码触发条件**：源码把数值转成文本——`strconv.FormatInt/FormatUint/FormatFloat`、`fmt.Sprintf`/`fmt.Printf` 的 `%d`/`%v`、`json.Marshal`，或对定宽整数做宽度依赖的格式化。
2. **冻结版本/运行时/API 前提**：Go 1.27；`strconv` 与 `fmt` 的格式语义见 `strconv`、`fmt`，`int` 宽度依架构见 GO-SPEC #Numeric_types。
3. **原可观察行为**：
   - `int`/`uint` 的范围依实现宽度；普通 `%d` 表示实际数值的十进制文本，不因类型宽度自动加填充。格式字符串的宽度、符号/填充选项与数值范围分别核对。
   - `strconv.FormatFloat(v, 'g', -1, 64)` 使用最短往返表示；普通浮点的 fmt `%v` 默认 `%g`，默认 `%g` 也取足以唯一识别值的最少位数。不能据两种 API 名称认定必有差异；显式精度/标志、float32/64 或自定义 Formatter/Stringer 等另核，格式依实际调用保持。
   - `json.Marshal` 对 `float64` 使用特定最短表示与转义规则，且对 `int64` 超出 JS 安全整数范围时不报错。
4. **目标可选写法和不适用条件**：
   - *Go 作为源*：目标语言的数值格式化必须显式选定与源一致的有效位数与区域设置；源用 `strconv` 的往返格式时，目标也须用等价的往返格式。
   - *Go 作为目标*：源若依赖定宽（如 C `%lld`、PRI 宏），目标应显式选 `int64/uint64` 而非 `int`，并按架构无关的方式输出。
   - *不适用条件*：源本身只有定宽类型且目标也是定宽类型时，不存在 `int` 宽度歧义，仍须核对**有效位数**。
5. **错误机械替换反例**：
   ```go
   // 错误：用 int 承接源的定宽 64 位量，32 位目标上静默截断语义
   var size int = readSize()                      // 源可能明确是 int64
   fmt.Printf("%d\n", size)
   // 错误之二：固定 6 位小数替换源的最短往返格式
   s := fmt.Sprintf("%.6f", 1.0/3)                // 精度/尾零策略已改变
   // 正确：类型与格式都显式钉住
   var size int64 = readSize()
   s := strconv.FormatFloat(1.0/3, 'g', -1, 64)   // 最短往返，与源义务一致
   ```
6. **信息不足或实现相关时的处理**：无法确定源的有效位数与整数宽度时，标为“数值格式与位宽待确认”，并写入冻结记录；不得靠 `fmt` 默认格式充当依据。
7. **资料依据（名称/版本/章节）**：`strconv`；`fmt`；GO-SPEC #Numeric_types。

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `string`：只读字节切片头部（指针 + 长度）；通常但非强制保存 UTF-8 编码字节。
- **字节序列数据结构**：`[语言规范保证]` `[]byte`：可变 8 位字节切片。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` 字符串由显式 `len` 界定，允许内部包含 `\0`；跨系统 C 调用需显式转为 NUL 结尾。
- **编码假设与转换陷阱**：`[语言规范保证]` `for range string` 按 UTF-8 解码出 Unicode 码点（`rune`），直接下标索引 `str[i]` 访问的是裸字节。
- **官方资料依据**：GO-SPEC #String_types, #For_statements

### L1-GO-03 `string`/`[]byte` 必须按字节进出，不得让隐式解码改写内容
1. **源码触发条件**：源码对字节做哈希、Base64、压缩、zip 打包、协议帧拼接或读写，并对 `string`/`[]byte` 互转（`string(b)`、`[]byte(s)`、`[]rune(s)`）。
2. **冻结版本/运行时/API 前提**：Go 1.27；`string`/`[]byte` 的转换与 UTF-8 处理见 GO-SPEC #String_types, #Conversions，`strings.ToValidUTF8` 与 `utf8` 包的替换语义见 `unicode/utf8`。
3. **原可观察行为**：
   - `string` 与 `[]byte` 互转**不改变字节**；`len(s)` 是**字节数**，`utf8.RuneCountInString(s)` 才是码点数。
   - `for range string` **按 UTF-8 解码**：非法字节会在迭代结果中产出 `utf8.RuneError`（U+FFFD），且不报告错误；原字符串的字节本身不会被改写。
   - `strings.ToValidUTF8`/`utf8.DecodeRune` 对非法序列的替换同样会改变长度与内容。
4. **目标可选写法和不适用条件**：
   - *Go 作为源*：字节路径必须映射到目标语言的字节类型并保持字节级长度语义；文本路径须显式声明编码，且不得依赖目标的默认解码。
   - *Go 作为目标*：源若以字节为单位，走 `[]byte`；需要文本时才 `string(b)`，且**不得**用 `for range string` 处理可能含非法 UTF-8 的字节；迭代值会将无效编码表示为 U+FFFD，丢失逐字节语义。
   - *不适用条件*：源确实**有意**按码点遍历文本（如按字符切分已确认合法的 UTF-8）时，`for range` 是要保留的行为，此时应显式校验 `utf8.Valid` 并在无效时保留源的处理方式。
5. **错误机械替换反例**：
   ```go
   // 错误：用 for range string 处理二进制，非法字节被替换成 U+FFFD
   for _, r := range string(blob) { out = append(out, byte(r)) }   // blob 已被改写
   // 错误之二：用 len(string) 冒充源按字节计的长度已足够（非 ASCII 字符数≠字节数）
   n := len([]rune(s))                     // 与源的 len(s) 字节数语义相反
   // 正确：字节路径保持字节
   h := sha256.Sum256(blob)
   out = append(out, blob...)              // 逐字节操作，不经过 rune 解码
   ```
6. **信息不足或实现相关时的处理**：无法确认源数据的编码、或源是否依赖按字节的长度与切片下标语义时，标为“编码与字节长度语义待确认”；**禁止**用替换策略（`strings.ToValidUTF8`、U+FFFD）掩盖差异。
7. **资料依据（名称/版本/章节）**：GO-SPEC #String_types, #Conversions；`unicode/utf8`；`strings.ToValidUTF8`。

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` 切片（`[]T`）为 `(ptr, len, cap)` 结构；`append` 超出 cap 时自动重分配新底层数组；`[指定运行时的实现相关事实]` 切片扩容策略属于实现相关行为，规则不得依赖具体增长比例或阈值。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `map[K]V` 为内建映射类型，值传递共享数据引用。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` **Go 规范明确未规定 map 迭代顺序**；转换后代码绝对不得依赖遍历顺序。
- **迭代期间修改（Fail-Fast）**：`[语言规范保证]` Go 数据竞争是错误，必须通过同步机制避免；`[指定运行时的实现相关事实]` 运行时若检测到并发写操作可能终止程序。
- **官方资料依据**：GO-SPEC #Map_types, #Range_clause

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` **显式多返回值 `(result, error)`**；`error` 为内置接口类型；严重致命故障使用 `panic`。
- **异常展开与性能模型**：`[语言规范保证]` `panic` 展开当前 Goroutine 栈，执行已注册的 `defer` 链；在 `defer` 中通过 `recover()` 截断崩溃。
- **进程退出码回传机制**：`[语言规范保证]` `os.Exit(int)` 立即终止进程（**不执行任何 `defer`！**）；`main` 正常返回退出码为 0。
- **跨语言映射关键风险**：**严禁将常规 error 机械写为 panic**；切忌用 `os.Exit` 代替错误返回，否则资源泄漏。
- **官方资料依据**：GO-SPEC #Errors, #Handling_panics

### L1-GO-04 被丢弃的 error 不得变成目标的异常终止，主动返回的 error 不得被静默吞掉
1. **源码触发条件**：源码**有意丢弃** error（`f, _ := os.Open(path)`、不检查 `Scanner.Err()`、忽略 `Close()` 的返回值），**或**在失败时 `return err`、`log.Fatal`、`os.Exit(非零)`、`panic`。
2. **冻结版本/运行时/API 前提**：Go 1.27；nil 接收者方法行为见 `os.File`、`os.ErrInvalid`，`Scanner.Err` 见 `bufio.Scanner`。
3. **原可观察行为**：
   - 丢弃 `os.Open` 的错误时得到 nil `*os.File`；其 `Read`/`Close` **返回 `os.ErrInvalid` 而非自动 panic**，`Scanner.Scan()` 因读取错误返回 false。若调用方不查 `Scanner.Err()`，可继续以空结果写报告并以 0 退出。
   - 主动返回 error 的路径：错误沿调用链传播，由调用方决定退出码；`os.Exit` **不执行任何 `defer`**。
4. **目标可选写法和不适用条件**（两个方向都必须覆盖）：
   - *源丢弃 error → 目标不得变成异常终止*：目标语言的“抛错”只应在源**确实会失败退出**的位置保留；源丢弃错误处必须映射为非致命路径并保留后续空结果路径。
   - *源返回/传播 error → 目标不得静默继续*：不得用宽泛 `rescue`/`catch`/`except Exception` 把它吞成成功。
   - *不适用条件*：源**确实检查** `err` 或 `Scanner.Err()` 并主动返回非零状态时，目标必须保留该失败分支，不能套用“忽略并继续”。
5. **错误机械替换反例**：
   ```go
   // 源：忽略打开与扫描错误，继续产出空结果并以 0 退出
   f, _ := os.Open(path)
   sc := bufio.NewScanner(f)
   for sc.Scan() { consume(sc.Text()) }        // 未检查 sc.Err()
   // 目标（错误）：让打开失败抛异常终止进程
   // target.rb: f = File.open(path, 'rb')     # Errno::ENOENT 未处理 → 提前终止
   // 目标（错误之二）：把源主动返回的失败分支吞掉
   // target.rb: begin ... rescue StandardError; end   # 静默继续，退出码变 0
   ```
   更严重的形态是**反向误判**：以“nil `*os.File` 会 panic”为由撤销正确的 guard 修订。该前提不成立——nil 接收者的 `Read`/`Close` 返回 `os.ErrInvalid`。
6. **信息不足或实现相关时的处理**：若不清楚源是否检查 `Scanner.Err()`、`defer f.Close()` 的返回值、或后续报告写入是否成功，**不能断言退出码和产物**；把打开失败路径单列为待验证 oracle。
7. **资料依据（名称/版本/章节）**：`os.ErrInvalid`（nil 接收者）；`bufio.Scanner.Scan`/`Err`；GO-SPEC #Errors, #Handling_panics。

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[语言规范保证]` 自动内存管理；编译器逃逸分析；运行时垃圾收集器回收无引用堆对象。
- **资源确定性释放机制**：`[语言规范保证]` `defer` 语句将资源清理延迟到**外层函数返回前按 LIFO 逆序确定性执行**；无作用域级自动析构。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 并发三色标记清除垃圾回收（依据 `GO-RT-DOC`）；非内存资源通过显式 `Close` 配合 `defer` 逆序释放。
- **跨迭代资源占用**：循环内注册的 `defer` 仍等到外层函数返回才执行，资源可能持续占用。是否属于转换引入的缺陷取决于源实际释放时点；源逐次释放不能被延迟，源跨迭代持有也不能被目标提前关闭。
- **官方资料依据**：GO-SPEC #Defer_statements<br>GO-RT-DOC

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` 原生 Goroutine（轻量并发任务）；Channel（信道通信）；`select` 多路复用。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` M:N 运行时调度器（G: Goroutine, M: OS 线程, P: 逻辑处理器），由运行时根据协作与系统调用动态调度。
- **级联取消与超时机制**：`[指定运行时的实现相关事实]` `context.Context`（`WithCancel`, `WithTimeout`）通过 `ctx.Done()` 信道级联传递取消。
- **内存模型与数据竞争**：`[语言规范保证]` Go 数据竞争是错误，必须通过 channel、sync 或 sync/atomic 等同步机制避免。Go 内存模型对含数据竞争程序仍规定有限的实现约束：实现可以报告该竞争并终止程序；无竞争程序才获得顺序一致性保证。不得将 Go 的数据竞争机械描述为 C/C++ 式完全未定义行为。
- **官方资料依据**：GO-SPEC #Go_statements<br>GO-RT-DOC<br>GO-MEM<br>GO-PKG-CONTEXT

## 八、空白与临时目录

### L1-GO-06 Unicode 空白不等于其他语言的 strip 集合

1. **触发**：strings.TrimSpace、unicode.IsSpace 或去空白后分支。
2. **前提**：冻结实际 Go 版本、Unicode 表与输入编码；Go 1.27 是知识基线，不证明已安装或文档已对应该构建。
3. **事实**：TrimSpace 按 Unicode 空白删除两端；unicode.IsSpace 采用 Unicode White_Space，包含 U+00A0，不含 NUL。Trim 的 cutset 与 TrimFunc 的谓词是另一种指定方式。
4. **映射条件**：源集合一致才用 TrimSpace；否则保留实际 cutset/谓词、删除范围及源变异/返回值。
5. **反例**：Ruby strip 与 TrimSpace 在 NUL、U+00A0 上会得到不同结果，不能只用 ASCII 正常样例定等价。
6. **未知**：冻结版本表或非 UTF-8 输入相关边界未知时标待核；不同库名不是缺陷归因证据。
7. **依据**：strings.TrimSpace/TrimFunc；unicode.IsSpace。

### L1-GO-07 os.TempDir 选路径不检查目录可用性

1. **触发**：os.TempDir 或临时目录落点参与输出/文件副作用。
2. **前提**：冻结 Go 工具链、GOOS 与环境；文档事实须与实际版本核对。
3. **事实**：官方 os 文档规定 Unix 取非空 TMPDIR，否则 /tmp；Windows 按 GetTempPath 的规则，Plan 9 为 /tmp。返回目录不保证存在或可访问，不是创建/校验操作。
4. **映射条件**：仅当源优先级与验证义务一致时直接替换；源逐候选校验/回退的算法仍须保留。
5. **反例**：TMPDIR 为空、TMP 指向有效目录时，不能把 Ruby Dir.tmpdir 与 Unix os.TempDir 当同义；两个 API 都返回字符串不证明副作用落点相同。
6. **未知**：Windows API、运行时变更或源自定义算法未明时待核，不从宿主环境代推隔离环境。
7. **依据**：os.TempDir；Ruby 版本化实现。

## 九、标准库消费点的选择引导

适用于本项目Go知识基线；实际标准库版本、构建标签、GOOS和CGO条件依冻结事实。本节帮助选映射，不新增强测或默认修复。

| 源码触发 | 先理解的语义 | 目标选择与反例 |
|---|---|---|
| encoding/json输出 | `encoding/json`的map编码键排序不同于map range的未规定顺序；struct字段/tag/嵌入和自定义Marshal另核。Encoder.Encode在JSON后写换行，Marshal不因此自动带换行 | 保持源的字段集、数值/布尔/null身份、转义、非法UTF-8策略、缩进及终止符；业务只要求对象语义时可用结构比较，但转换不能因比较器宽松而删除源输出义务。不把json/v2或目标库默认当v1契约 |
| bufio.Scanner/固定容量容器 | 停止条件、Buffer配置、Err检查、已取得token与固定截断范围均是消费者的一部分 | 目标逐行读取不天然有相同长度上限；源忽略Err也不授权丢掉已取得数据或强制抛异常。容量上界未知时保留源定义，不加任意100项上限 |
| sort.Sort/Stable/SliceStable等 | 核实际函数与Less及同键元素的后续用途 | 不稳定接口不能升级为规定某个同键排列；源稳定性有义务时选稳定映射。冻结输入只有唯一键不取消实现义务 |
| time/计数器 | 核取时点、时区、布局、累计/增量及采样区间；时间展示与测量定义不同 | 展示时刻可属于允许差异，取时点/窗口/单位不能自动消噪；性能计数器按实际集合和定义映射，不以同名数值互换 |
| runtime.GOOS/构建标签 | 看源码按平台选了哪些声明、调用和出口；运行平台事实与构建时选择分别核 | 目标按对应平台保留选中分支，不无条件执行原Windows/POSIX分支；未知SDK或未选分支只写对应范围，不凭当前OS证明所有平台可用 |
| os/user或环境读取 | 后端、CGO/构建标签、缓存和查询来源可能影响结果；os.Getenv的空串与LookupEnv的存在位不同 | 保留源选用的查询与missing/empty分流，不把环境变量默认值当实际账户信息。后端未知只记精确缺口，不声明跨平台同源 |
| Read及进程双流 | `n>0`与error可同时存在；CombinedOutput合并流不等于分别读完后拼接 | 先消费有效字节再按源处理错误；源需交错观察时选择相同合流模型，无法保证交错顺序则说明条件，不用stdout+stderr拼接冒充 |

依据：Go Language Specification；encoding/json Marshal/Encoder.Encode；bufio.Scanner/Buffer/Err；sort；time；os.Getenv/LookupEnv；os/user；io.Reader；os/exec。版本/后端未核的实现细节不由本表补成保证。

### L1-GO-08 Scanner 的停止边界与已取得结果

源码使用Scanner时，先定位Split函数、Buffer设置、Scan停止后的Err检查及已得token的消费者。Go 1.27标准库默认MaxScanTokenSize为64×1024字节；实际可接受token还受终止符、max与cap(buf)影响，不能据此声称任意64KiB行都成功。Buffer须在开始扫描前配置。Scan返回false可能是EOF，也可能是读取/过长token等错误，Err区分其中非EOF错误。

目标逐行读取通常不天然有相同边界；只有源确实允许扩大接受域时才取消上限。源忽略Err而继续消费先前token时，保持部分结果与后续路径，不额外抛异常，也不将所有结果清空；固定100项等业务截断与Scanner字节边界是不同限制。源Split/Buffer具体配置未知时记对应缺口，不猜一套统一上限。依据：Go 1.27 bufio.Scanner、MaxScanTokenSize、Buffer、Scan、Err。

### L1-GO-09 用户查询后端不等于环境变量

源码使用os/user时，先看Current、Lookup、LookupId或GroupIds及其字段消费者，再核GOOS、CGO、构建标签和账户来源。多数Unix平台有纯Go解析/etc/passwd、/etc/group与cgo调用libc查询两类实现；cgo及所需libc例程可用时采用后者，osusergo标签可强制纯Go。两者可能覆盖不同账户/组来源，不能把本地文件结果或USER环境变量当所有查询的替代。

目标可选同来源的系统/库查询，但还要保持ID与名称、组集合、missing/错误及缓存条件；只输出用户名的一条路径不说明组信息也等价。平台或后端未核时只记录具体映射条件，不根据当前宿主用户名补答案，也不新增身份能力。依据：Go 1.27 os/user包说明及相应查询API。

### L1-GO-10 同键顺序依实际排序接口

sort.Sort与sort.Slice不保证稳定；sort.Stable与sort.SliceStable保持相等元素的原顺序。先看源码选哪个接口、Less何时将元素视作相等及排序后的消费者，再选目标稳定/非稳定方案；不得为了消噪给源有顺序义务的集合重新排列。

源稳定时，可选目标稳定接口或有同等前提的显式原序号策略；源未规定同键顺序时，不从一个样例推定固定排列，也不把额外按名称排序当原规则。比较器是否满足要求、是否依赖实现的具体排列未知时写局部缺口，不把所有排序都升级为稳定保证。依据：Go 1.27 sort.Sort/Slice/Stable/SliceStable及Interface.Less。

### L1-GO-11 截止时刻、取消与等待预算

net.Conn的SetDeadline是绝对时刻，覆盖待执行及当前阻塞的I/O，不仅下一次调用；零值表示不超时，超过截止后需源明确更新才能恢复。目标仅有相对timeout时，按源是否共享截止或每次刷新选择剩余预算，而不是每次调用重新给满同一时长；源本来实现idle timeout时则保持刷新点。

os/exec另有启动、Context取消、直接进程退出和管道排空：CommandContext默认取消直接进程，WaitDelay从Context结束或观察到进程退出的较早时点计时，限制取消后未退出或I/O管道未关闭的等待，不是命令从启动起的总timeout，也不保证后代全树已回收。源自定义Cancel/WaitDelay、目标时钟或树清理能力未知时说明该映射点。具体网络/进程行为继续读对应场景，不新增驱动或测试。依据：Go 1.27 net.Conn、os/exec CommandContext/Cmd.Wait/WaitDelay。

### L1-GO-12 合流与部分读取的消费顺序

io.Reader允许在返回n>0时同时返回错误，也允许最后一块数据先返回err=nil、下次再返回EOF；0,nil本身不是EOF。先对应源实际消费p[:n]和错误的顺序。源按Reader契约消费时保留有效字节后再处理错误；源实际丢弃部分数据时记录源行为/风险，不替源修复。目标异常式API没有天然的n、err二元返回，可选择对应已得块和失败状态的表示，不能从异常猜出未取得字节。

CombinedOutput取得合并stdout/stderr；分别采集后stdout+stderr拼接不保留合流关系。源需要来源分离时也不能反向合并。映射以源的共同输出接收点、已得字节、错误及等待范围为依据，不承诺并发输出跨运行具有固定顺序。仅能分流而无等价合流条件时说明限制，不新增装置代码。依据：Go 1.27 io.Reader、os/exec CombinedOutput；方向映射按实际两语言正文。

### L1-GO-13 Windows API 的包归属与导出边界

1. **触发/前提**：向 Go 映射 Windows 平台 API，或源使用 `syscall`、`golang.org/x/sys/windows`、动态库入口。冻结实际 Go 工具链、GOOS/GOARCH、SDK/ABI 与必要模块版本；本节说明包和调用层的边界，不声明完整 Win32 API 已覆盖。
2. **标准库范围**：`syscall` 的 Windows 实现只导出其中实际声明的成员，不是 Win32 SDK 的完整同名投影。`NewLazyDLL`/`NewProc` 是动态库及符号查找入口，不会为 Go 包自动增加其他函数或 `MEM_*`/`PAGE_*` 常量。不能从 C 头文件存在某符号，就写出 `syscall.<同名符号>`；已有转换曾因这种假设出现未定义成员的真实编译错误。
3. **扩展模块范围**：`golang.org/x/sys/windows` 是单独的扩展模块，不因安装 Go 工具链就成为标准库。选择其中 API 时核本项已冻结版本的导出声明、参数/返回类型和合法依赖材料；不静默增加/下载模块，不从包名推定所有 Windows API 都存在。依赖准备仍按[构建前提](../../../references/workflow/build-prerequisites.md#23--go)。
4. **动态绑定范围**：动态找到库/符号不证明 ABI、参数宽度、返回/错误含义、指针生命周期或调用条件正确，也不由语法/编译通过证明运行时符号存在。只有源义务和对应接口事实足够明确时，才能把已有合法绑定方式作为候选；不把动态绑定设为所有 API 的统一替换方案。
5. **选择与未知处理**：在既有映射依据中记录“源使用点→目标包/符号→本地声明来源和精确版本→依赖及未验证条件”。必要导出或 ABI 事实缺失时标记该映射缺口，不编造声明、常量或成功结果；不把联网查询作为后续调用者的必需步骤。本页只提供选择依据，不增加自审轮次或本机检查。
6. **反例**：把扩展模块中的函数写成标准库成员；把查到符号当作签名已确认；把某一平台/版本的可用性推到所有 GOOS/GOARCH。这些都不能凭名字或一次编译通过推定成立。
7. **依据与结论范围**：Go 官方 `syscall` Windows 实现的 `dll_windows.go`（`LazyDLL`/`NewLazyDLL`/`NewProc`）及 `golang.org/x/sys` 模块说明。具体 API 导出仍以本任务的合法本地声明/冻结版本为准；本节不替代该目标的编译、加载或行为证据，不提供专用平台调用实现。

### L1-GO-14 大小写映射不提供完整规范化与 casefold

1. **触发／前提**：Go 1.27 的 unicode/strings/utf8 与源端规范化、折叠或码点计长对应；Unicode 数据版本按实际工具链与库冻结。
2. **事实**：`unicode.ToLower` 是单 rune 的大小写映射，不提供 `ß`→`ss` 这样的多码点完整折叠；Go 标准库不提供完整 NFC/NFD/NFKC/NFKD 接口。`golang.org/x/text/unicode/norm` 和 `golang.org/x/text/cases` 是单独模块，不因包路径带 golang.org 就成为离线已安装的标准库。
3. **选择／反例**：按源语义及合法离线库选择 norm/cases 或有完整依据的实现，明确 normalization 与 fold 的顺序；不能用 ToLower 加少数特例对所有输入宣称等效。`len(s)`、RuneCountInString 和源 UTF-16 长度分别选择；NFC 的 Jamo 组合或 fold 的字符扩展应进入相关候选边界。
4. **未知与依据**：缺模块不在提交宿主编译探测、不临时联网取库，消费构建前提 §0.2 的支持范围／依赖记录。依据：Go unicode.ToLower/Version、unicode/utf8；x/text norm 的 Form、cases.Fold；对应 Unicode 版本的规范化／折叠资料。本条不是模块可用性或转换效果证明。

### L1-GO-15 encoding/json 的替换、重复键与数值路径

1. **触发／前提**：Go 1.27 标准库 `encoding/json`（不是任意第三方或实验 JSON 实现），Marshal/Decoder、UseNumber、目标类型及读取 EOF 的实际组合。
2. **事实**：该包接受重复同名键，后遇值按解码目标替换或合并，不自动报重复键；对字符串的非法 UTF-8／孤立 UTF-16 代理项可替换为 U+FFFD。向 interface 解码数字默认浮点；UseNumber 保留 json.Number，随后 ParseInt 的词法、位宽与范围检查属于另外一层。一次 Decode 成功不证明输入后无第二个 JSON 值，源若检查 EOF 须保留。
3. **映射／反例**：先定位源的原始 UTF-8 校验、重复键 hooks、非有限常量和整数／布尔区分；不能用 Python 默认 loads 原样代替 Go 的代理项处理，也不能在 Go 目标默认接受重复键来替代源的拒绝。nil slice 的 JSON null 与非 nil 空 slice 的 [] 有外部区别；保留是否返回数组对象的协议。
4. **未知与依据**：JSON 层的转义代理项处理和原始字节解码分开，源深度限制／错误分流不从另一个包默认值推定。依据：Go encoding/json 的 Security Considerations、Unmarshal、Decoder.Decode/UseNumber、Marshal；strconv.ParseInt。实际编译及行为仍独立取证。

## 使用边界

将本页与所选的源→目标方向 Skill 及另一语言的共性页组合使用；映射前先确认源码真实行为。文件、网络、并发和跨 OS API 的具体差异仍按[共性索引的场景/系统分流](../seven-language-common-semantics.md)选读，不从语言事实直接推断系统 API 等价。没有逐例第三方证据时，语法/构建与功能结论保持 `UNVERIFIED`；本机不运行或编译样本。
