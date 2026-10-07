# Go 语言共性语义（Go 1.27）

> **用途**：供以 Go 为源语言或目标语言的方向 Skill 按需读取；本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 严格纯值传递；指针传递指针值（内存地址拷贝），显式指针禁用算术运算（除 `unsafe.Pointer`）；切片、map、channel、interface 内部包含指针头部，值传递时其底层数据共享。
- **实现相关 / 运行时优化行为**：`[指定运行时的实现相关事实]` 编译器逃逸分析（Escape Analysis）决定变量分配在 Goroutine 栈还是堆上，属于编译器实现细节，语言规范不作物理存储位置保证。
- **机械等价禁区与转换约束**：不可认为切片传递是深拷贝（共享底层数组）；切片扩容后会静默与原数组分离；**不得把 Go 的 `nil`/零值判定与其他语言的真值判定互相当作等价**（见下条）。
- **官方资料依据**：[GO-SPEC #Type_identity, #Slice_types](https://go.dev/ref/spec)

### L1-GO-01 零值、nil 与长度是三种不同判定
1. **源码触发条件**：源码用 `if err != nil`、`if x == ""`、`if len(b) == 0`、`if v, ok := m[k]; ok`、`if fi.IsDir()` 之类的判断分流，或用 `map[string]string` 承接解析结果。
2. **冻结版本/运行时/API 前提**：Go 1.27；零值与比较语义见 [GO-SPEC #The_zero_value, #Comparison_operators](https://go.dev/ref/spec)，nil map 的读写差异见 [GO-SPEC #Map_types](https://go.dev/ref/spec)。
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
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #The_zero_value, #Comparison_operators, #Map_types](https://go.dev/ref/spec)。

### L1-GO-05 程序实参含程序名，flag 解析与参数消费必须显式重建

1. **源码触发条件**：源码从 `os.Args` 取用实参、用 `flag` 包解析，或在 `flag.Parse()` 后读取 `flag.Args()`/`os.Args[1:]`。
2. **冻结版本/运行时/API 前提**：Go 1.27（[`os.Args`](https://pkg.go.dev/os#pkg-variables)、[`flag`](https://pkg.go.dev/flag)）。
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
7. **直接官方 HTTPS 依据链接**：[Go `os.Args`](https://pkg.go.dev/os#pkg-variables)、[`flag` 包（解析停止与退出码 2）](https://pkg.go.dev/flag)、[`flag.Parse`](https://pkg.go.dev/flag#Parse)。

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` `int8`..`int64`, `uint8`..`uint64` 严格定宽；`int`/`uint` 大小取决于架构（32 或 64 位）；`uintptr` 存指针位。
- **有符号溢出行为**：`[语言规范保证]` **按补码截断回绕**（二进制算术确定行为，非 UB）；**常数表达式溢出属于编译错误**。
- **无符号溢出行为**：`[语言规范保证]` **按模截断回绕**（二进制算术确定行为）。
- **隐式提升与转换陷阱**：`[语言规范保证]` **严格禁止隐式类型转换**；即使 `int32` 与 `int` 在 64 位架构下同宽，亦必须显式强制转换。
- **官方资料依据**：[GO-SPEC #Numeric_types, #Arithmetic_operators](https://go.dev/ref/spec)

### L1-GO-02 数值文本输出必须钉住位宽与格式
1. **源码触发条件**：源码把数值转成文本——`strconv.FormatInt/FormatUint/FormatFloat`、`fmt.Sprintf`/`fmt.Printf` 的 `%d`/`%v`、`json.Marshal`，或对定宽整数做宽度依赖的格式化。
2. **冻结版本/运行时/API 前提**：Go 1.27；`strconv` 与 `fmt` 的格式语义见 [`strconv`](https://pkg.go.dev/strconv)、[`fmt`](https://pkg.go.dev/fmt)，`int` 宽度依架构见 [GO-SPEC #Numeric_types](https://go.dev/ref/spec)。
3. **原可观察行为**：
   - `int`/`uint` 的宽度**依架构**（32 或 64 位）；`fmt.Sprintf("%d", x)` 的输出宽度随类型与平台变化，`%v` 亦不保证与定宽类型一致。
   - `strconv.FormatFloat(v, 'g', -1, 64)` 使用**最短往返表示**；`fmt.Sprintf("%v", f)` 采用 `%g` 但不保证相同位数——两者输出**可能不同**。
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
   // 错误之二：用 %v 冒充源的往返精度
   s := fmt.Sprintf("%v", 1.0/3)                  // 位数可能与源的 strconv 往返格式不同
   // 正确：类型与格式都显式钉住
   var size int64 = readSize()
   s := strconv.FormatFloat(1.0/3, 'g', -1, 64)   // 最短往返，与源义务一致
   ```
6. **信息不足或实现相关时的处理**：无法确定源的有效位数与整数宽度时，标为“数值格式与位宽待确认”，并写入冻结记录；不得靠 `fmt` 默认格式充当依据。
7. **直接官方 HTTPS 依据链接**：[`strconv`](https://pkg.go.dev/strconv)；[`fmt`](https://pkg.go.dev/fmt)；[GO-SPEC #Numeric_types](https://go.dev/ref/spec)。

## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `string`：只读字节切片头部（指针 + 长度）；通常但非强制保存 UTF-8 编码字节。
- **字节序列数据结构**：`[语言规范保证]` `[]byte`：可变 8 位字节切片。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` 字符串由显式 `len` 界定，允许内部包含 `\0`；跨系统 C 调用需显式转为 NUL 结尾。
- **编码假设与转换陷阱**：`[语言规范保证]` `for range string` 按 UTF-8 解码出 Unicode 码点（`rune`），直接下标索引 `str[i]` 访问的是裸字节。
- **官方资料依据**：[GO-SPEC #String_types, #For_statements](https://go.dev/ref/spec)

### L1-GO-03 `string`/`[]byte` 必须按字节进出，不得让隐式解码改写内容
1. **源码触发条件**：源码对字节做哈希、Base64、压缩、zip 打包、协议帧拼接或读写，并对 `string`/`[]byte` 互转（`string(b)`、`[]byte(s)`、`[]rune(s)`）。
2. **冻结版本/运行时/API 前提**：Go 1.27；`string`/`[]byte` 的转换与 UTF-8 处理见 [GO-SPEC #String_types, #Conversions](https://go.dev/ref/spec)，`strings.ToValidUTF8` 与 `utf8` 包的替换语义见 [`unicode/utf8`](https://pkg.go.dev/unicode/utf8)。
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
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #String_types, #Conversions](https://go.dev/ref/spec)；[`unicode/utf8`](https://pkg.go.dev/unicode/utf8)；[`strings.ToValidUTF8`](https://pkg.go.dev/strings#ToValidUTF8)。

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` 切片（`[]T`）为 `(ptr, len, cap)` 结构；`append` 超出 cap 时自动重分配新底层数组；`[指定运行时的实现相关事实]` 切片扩容策略属于实现相关行为，规则不得依赖具体增长比例或阈值。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `map[K]V` 为内建映射类型，值传递共享数据引用。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` **Go 规范明确未规定 map 迭代顺序**；转换后代码绝对不得依赖遍历顺序。
- **迭代期间修改（Fail-Fast）**：`[语言规范保证]` Go 数据竞争是错误，必须通过同步机制避免；`[指定运行时的实现相关事实]` 运行时若检测到并发写操作可能终止程序。
- **官方资料依据**：[GO-SPEC #Map_types, #Range_clause](https://go.dev/ref/spec)

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` **显式多返回值 `(result, error)`**；`error` 为内置接口类型；严重致命故障使用 `panic`。
- **异常展开与性能模型**：`[语言规范保证]` `panic` 展开当前 Goroutine 栈，执行已注册的 `defer` 链；在 `defer` 中通过 `recover()` 截断崩溃。
- **进程退出码回传机制**：`[语言规范保证]` `os.Exit(int)` 立即终止进程（**不执行任何 `defer`！**）；`main` 正常返回退出码为 0。
- **跨语言映射关键风险**：**严禁将常规 error 机械写为 panic**；切忌用 `os.Exit` 代替错误返回，否则资源泄漏。
- **官方资料依据**：[GO-SPEC #Errors, #Handling_panics](https://go.dev/ref/spec)

### L1-GO-04 被丢弃的 error 不得变成目标的异常终止，主动返回的 error 不得被静默吞掉
1. **源码触发条件**：源码**有意丢弃** error（`f, _ := os.Open(path)`、不检查 `Scanner.Err()`、忽略 `Close()` 的返回值），**或**在失败时 `return err`、`log.Fatal`、`os.Exit(非零)`、`panic`。
2. **冻结版本/运行时/API 前提**：Go 1.27；nil 接收者方法行为见 [`os.File`](https://pkg.go.dev/os#File)、[`os.ErrInvalid`](https://pkg.go.dev/os#ErrInvalid)，`Scanner.Err` 见 [`bufio.Scanner`](https://pkg.go.dev/bufio#Scanner.Err)。
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
7. **直接官方 HTTPS 依据链接**：[`os.ErrInvalid`（nil 接收者）](https://pkg.go.dev/os#ErrInvalid)；[`bufio.Scanner.Scan`/`Err`](https://pkg.go.dev/bufio#Scanner.Scan)；[GO-SPEC #Errors, #Handling_panics](https://go.dev/ref/spec)。

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[语言规范保证]` 自动内存管理；编译器逃逸分析；运行时垃圾收集器回收无引用堆对象。
- **资源确定性释放机制**：`[语言规范保证]` `defer` 语句将资源清理延迟到**外层函数返回前按 LIFO 逆序确定性执行**；无作用域级自动析构。
- **垃圾收集（GC）停顿与机制**：`[指定运行时的实现相关事实]` 并发三色标记清除垃圾回收（依据 `GO-RT-DOC`）；非内存资源通过显式 `Close` 配合 `defer` 逆序释放。
- **悬垂与泄漏防范**：在长循环内部直接使用 `defer` 会导致资源直到整函数退出才释放，极易耗尽句柄。
- **官方资料依据**：[GO-SPEC #Defer_statements](https://go.dev/ref/spec)<br>[GO-RT-DOC](https://go.dev/doc/gc-guide)

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` 原生 Goroutine（轻量并发任务）；Channel（信道通信）；`select` 多路复用。
- **线程/调度实体映射关系**：`[指定运行时的实现相关事实]` M:N 运行时调度器（G: Goroutine, M: OS 线程, P: 逻辑处理器），由运行时根据协作与系统调用动态调度。
- **级联取消与超时机制**：`[指定运行时的实现相关事实]` `context.Context`（`WithCancel`, `WithTimeout`）通过 `ctx.Done()` 信道级联传递取消。
- **内存模型与数据竞争**：`[语言规范保证]` Go 数据竞争是错误，必须通过 channel、sync 或 sync/atomic 等同步机制避免。Go 内存模型对含数据竞争程序仍规定有限的实现约束：实现可以报告该竞争并终止程序；无竞争程序才获得顺序一致性保证。不得将 Go 的数据竞争机械描述为 C/C++ 式完全未定义行为。
- **官方资料依据**：[GO-SPEC #Go_statements](https://go.dev/ref/spec)<br>[GO-RT-DOC](https://go.dev/doc/gc-guide)<br>[GO-MEM](https://go.dev/ref/mem)<br>[GO-PKG-CONTEXT](https://pkg.go.dev/context)

## 使用边界

将本页与所选的源→目标方向 Skill 及另一语言的共性页组合使用；映射前先确认源码真实行为。文件、网络、并发和跨 OS API 的具体差异仍按[共性索引的场景/系统分流](../seven-language-common-semantics.md)选读，不从语言事实直接推断系统 API 等价。没有逐例第三方证据时，语法/构建与功能结论保持 `UNVERIFIED`；本机不运行或编译样本。
