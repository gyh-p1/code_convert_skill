---
name: ruby-to-go
description: Use when converting Ruby source to Go; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → Go 语言转换规则

> **适用基线**：CRuby 3.4 → Go 1.27。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Ruby](../../references/languages/ruby.md)与[目标语言 Go](../../references/languages/go.md)。
> **方向案例与证据**：如本地工作区存在 `docs/test/dataset/ruby-to-go/README.md`，按其中 case 分层查看；该本地数据目录不随 Git/Skill 分发。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Ruby → Go 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 RB-GO-01：Ruby 动态鸭子类型向 Go 显式接口定义与满足映射
1. **源码触发条件**：Ruby 源码中依赖对象具备某个方法即可调用（鸭子类型），未声明显式继承或接口。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4；目标语言 Go 1.27（[GO-SPEC #Interface_types](https://go.dev/ref/spec)）。
3. **原可观察行为**：运行期只要响应方法（`respond_to?`）即调用成功，否则抛出 `NoMethodError`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Go 中显式定义 `type Duck interface { Method() }`，Go 结构体只需拥有对应签名的方法即可自动、隐式满足该接口，完美契合鸭子类型本质。
   - *不适用条件*：严禁使用 `interface{}` / `any` 加大量的运行时反射（`reflect`），会极大破坏 Go 性能与静态类型安全。
5. **错误机械替换反例**：
   ```go
   // 错误：滥用 reflect 反射调用方法模拟鸭子类型
   func Invoke(obj any) {
       reflect.ValueOf(obj).MethodByName("Action").Call(nil) // 脆弱、极其低效
   }
   // 正确：定义精确接口
   type Actioner interface { Action() }
   func Invoke(obj Actioner) { obj.Action() }
   ```
6. **信息不足或实现相关时的处理**：若对象响应的方法集极度动态，提取公共最小子集接口。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Interface_types](https://go.dev/ref/spec)。

### 规则 RB-GO-02：Ruby 异常控制流向 Go 显式多返回值 (T, error) 映射
1. **源码触发条件**：Ruby 源码中使用 `raise CustomError.new(...)` 并依赖多层拦截。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec)）。
3. **原可观察行为**：抛出异常后中断当前调用链。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重写为 Go 的 `(T, error)` 返回值；在调用点逐层处理。
   - *不适用条件*：严禁将业务异常机械翻译为 Go `panic`。
5. **错误机械替换反例**：
   ```go
   // 错误：将 Ruby 的常规业务异常翻译为 panic
   func Validate(age int) {
       if age < 0 { panic("invalid age") } // 错误：导致不可预期的崩溃！
   }
   // 正确：返回 error
   func Validate(age int) error {
       if age < 0 { return errors.New("invalid age") }
       return nil
   }
   ```
6. **信息不足或实现相关时的处理**：若原 Ruby 错误存在丰富字段，定义包含相同字段的 Go 结构体。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[GO-SPEC #Errors](https://go.dev/ref/spec)。

### 规则 RB-GO-03：Ruby 任意精度数值向 Go 定宽整数模截断防溢出映射
1. **源码触发条件**：Ruby 源码中使用大整数算术或位运算。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 Go 1.27（[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)）。
3. **原可观察行为**：数值任意精度，无固定溢出边界。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若数值在 64 位内，使用 `int64`/`uint64`，注意溢出时 Go 是按模截断回绕（不会抛出异常）；若需保持无限精度，使用 `math/big.Int`。
   - *不适用条件*：严禁在数值可能超过 64 位时仍然采用裸 `int`。
5. **错误机械替换反例**：
   ```go
   // 错误：在 Go 中使用普通 int 进行超大数计算导致溢出截断
   // Ruby: 2**100
   var x int64 = 1 << 100 // 编译报错或溢出！
   // 正确：使用 big.Int
   x := new(big.Int).Exp(big.NewInt(2), big.NewInt(100), nil)
   ```
6. **信息不足或实现相关时的处理**：若无法确定上限，优先使用 `math/big` 并在报告中提示性能开销。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 RB-GO-04：Ruby 块与 `&:sym` 迭代向 Go 显式循环、函数值与 zero value 语义映射
1. **源码触发条件**：Ruby 源码用块做迭代或转换，例如 `keys.each do |k| ... end`、`perm.map { |i| scrambled[i] }.join`、`files.each do |file| ... end`、`a.map(&:join)`、`next if cls.nil?`、`next unless k == 'auth'`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-PROC](https://docs.ruby-lang.org/en/3.4/Proc.html)）；目标语言 Go 1.27（[GO-SPEC #For_statements, #Function_types](https://go.dev/ref/spec)）。
3. **原可观察行为**：块可能一次都不执行（空集合）、可能被短路（`next` 跳过本次、`break` 终止整个迭代并让调用方方法返回该值）、可能在中途抛异常终止循环；块内 `next` 之后的语句不执行，`break` 之后的迭代不再发生。
4. **目标可选写法和不适用条件**：
   - *可选映射*：`each` → `for _, item := range items`；`map { }.join` 这类"逐元素变换再拼接"用 `strings.Builder`/`strings.Join` + 显式循环，或把变换写成具名函数再以函数值传入；`next` → `continue`；`break` → `break`（并让外层用返回值/labeled break 表达"从调用方法返回"）；需要把块当数据传递时用 `func(T) R` 或 `func(T) (R, error)` 类型的参数，块内错误用 error 返回值传出而**不是** panic。
   - *不适用条件*：严禁把 Ruby 的块一律改写成 Go 的方法值或 `interface{}` 分派；严禁用 `defer` 模拟块的"迭代体在某元素上提前退出"——`defer` 的粒度是函数返回，不是循环迭代；`&:sym` 也不能翻译为 `reflect` 反射按名调用。
5. **错误机械替换反例**：
   ```go
   // 错误：把 break 语义套在 defer 上，清理时机整体错位
   for _, f := range files {
       defer f.Close()               // 错误：直到整个函数返回才关闭，长循环耗尽句柄
       if f.Name == "stop" { break }
   }
   // 错误：块内的 next 被翻成 return，循环被整体终止
   for _, k := range keys {
       if k == "" { return nil }     // 错误：Ruby 的 next 只跳过本次迭代
       hex += normalize(k)
   }
   // 正确：continue 保留"跳过本次"，清理放在单次迭代内显式调用
   for _, k := range keys {
       if k == "" { continue }
       hex += normalize(k)
   }
   ```
6. **信息不足或实现相关时的处理**：块内出现 `break` 且其返回值被调用方使用、或块被存进变量后延迟调用（生命周期跨出当前函数）时，必须标注"控制流与存活期未定"并询问；块是否可能为空集合必须从源码确认（决定零次执行是否合法），不得默认至少执行一次。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-PROC](https://docs.ruby-lang.org/en/3.4/Proc.html)；[GO-SPEC #For_statements, #Function_types](https://go.dev/ref/spec)。

### 规则 RB-GO-05：Ruby Hash/Array 向 Go map/切片映射（nil map 写入 panic、零值与键存在性、切片别名）
1. **源码触发条件**：Ruby 源码构造并逐项写入映射或数组，例如 `avs = {}` 后 `avs[avn] = av_note`、`ret = {}` 后 `ret[s.gsub(...)] = drive`、`values = {}` 后 `values[name] = data.to_s`、`hex = ''` 后 `hex << ...`、`sessions << net_session_enum(...)` 后 `sessions.flatten!`、`unsigned = sorted.map { |b| (b - first) & 0xff }`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)、[RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)）；目标语言 Go 1.27（[GO-SPEC #Map_types, #Slice_types, #Append](https://go.dev/ref/spec)）。
3. **原可观察行为**：Ruby `Hash` 保留插入顺序、允许值为 `nil` 且"键存在"与"值为 nil"可分别观察（`key?` / `[]` 返回 `nil` 无法区分二者）；`Array` 无固定容量，`<<`/`+` 就地改变或合并元素，负数下标与范围切片（`-1`、`[1..]`）合法。
4. **目标可选写法和不适用条件**：
   - *可选映射*：映射关系用 `map[K]V` 并**必须**用 `make(map[K]V)` 或字面量初始化后再写入；需要"键是否存在"语义时用二值取值 `v, ok := m[k]`（不要用零值判断）；需要保留插入顺序以匹配 Ruby 遍历时，额外维护 `[]K` 键序列，遍历它而不是 `range` map；动态序列用 `[]T` + `append`，切片/取尾用切片表达式（`items[1:]`）并显式处理空切片边界。
   - *不适用条件*：严禁对声明为 `var m map[K]V` 的 nil map 直接赋值——Go 在运行期 panic（"assignment to entry in nil map"），与 Ruby 的 `h[k] = v` 自动建键完全不同；严禁依赖 `range` map 的遍历顺序复现 Ruby `Hash` 插入顺序（Go 规范明确不规定顺序）；严禁把切片当成 Ruby `Array` 的深拷贝：切片是共享底层数组的头部，`append` 可能原地改写原数组或静默分离，必须明确谁是所有者。
5. **错误机械替换反例**：
   ```go
   // 错误：nil map 直接写入，运行期 panic；用零值判断键存在性
   var values map[string]string           // 错误：nil map
   values["ParentIdPrefix"] = uid         // panic: assignment to entry in nil map
   if values["Disk"] == "" { }            // 错误：无法区分"键不存在"与"值为空串"
   // 错误：依赖 map 顺序复现 Ruby Hash 的插入顺序输出
   for name, v := range values { out += name + "=" + v + "\n" } // 错误：顺序未定义
   // 正确：显式初始化、二值取值、保序键序列
   values := make(map[string]string)
   v, ok := values["Disk"]
   keys := make([]string, 0, len(values))
   for _, name := range keys { out += name + "=" + values[name] + "\n" }
   ```
6. **信息不足或实现相关时的处理**：Ruby `Hash` 的遍历顺序是否被外部观察（输出、文件名、报告内容）必须从源码判断——被观察时需保留顺序并写入报告，未确认时标注"顺序是否可观察待确认"；`Array#flatten!`/`compact` 这类方法是否在源码里承担"去空值"职责要逐点确认，Go 的切片不会自动剔除零值元素。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)；[RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)；[GO-SPEC #Map_types, #Slice_types](https://go.dev/ref/spec)。

### 规则 RB-GO-06：Ruby 二进制打包与字节处理（pack/unpack、整数取字节）向 Go 定宽类型与 encoding/binary 映射
1. **源码触发条件**：Ruby 源码做二进制编解码或逐字节处理，例如 `[encoded_payload.length].pack('I<') + encoded_payload`、`scrambled = [hex].pack('H*')`、`h['pMacAddr'].unpack('C*').map { |e| '%02x' % e }.join(':')`、`data.unpack('V')`、`perm.map { |i| scrambled[i] }.join`、`gsub("\x00", '')`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)、[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)）；目标语言 Go 1.27（[GO-PKG-BINARY](https://pkg.go.dev/encoding/binary)、[GO-PKG-HEX](https://pkg.go.dev/encoding/hex)、[GO-SPEC #String_types](https://go.dev/ref/spec)）。
3. **原可观察行为**：Ruby `String` 是字节序列（可含 `\0`，显式长度），`Integer#[n]` 与 `unpack('C*')` 都给出 **0–255 的整数**；`pack('I<')` 按小端写出 4 字节，`pack('H*')` 按十六进制把字符串解成字节，`unpack('V')` 按小端读 32 位；这些格式字符把宽度与字节序写在源码里，与运行平台无关。
4. **目标可选写法和不适用条件**：
   - *可选映射*：字节序列统一用 `[]byte`（`string` 是不可变只读字节头部，二者互转要显式拷贝）；定宽小端编解码用 `encoding/binary` 的 `binary.LittleEndian.PutUint32`/`Uint32` 并配 `[4]byte` 缓冲区；十六进制用 `hex.DecodeString`/`hex.EncodeToString`；逐字节十六进制展示用 `fmt.Sprintf("%02x", b)`；单字节取值为整数时用 `b := data[i]`（类型已是 `byte`），参与算术前显式转 `int`。
   - *不适用条件*：严禁用 `int`/`uint` 顶替 Ruby 里显式定宽的量——Go 的 `int` 宽度随架构变化，`PutUint32`/`binary.LittleEndian` 这类 API 要求精确类型，宽度不明的 `int` 既编译不过也破坏格式约定；严禁用 `string` 承载二进制数据后按下标取字符（`s[i]` 得到 `byte` 但 `for range s` 按 UTF-8 解码出 `rune`，含 `\0` 或非 UTF-8 字节时结果完全不同）；严禁用 `strconv`/`strings` 家族解析二进制串代替 `encoding/hex`、`encoding/binary`。
5. **错误机械替换反例**：
   ```go
   // 错误：Ruby 的 [n].pack('I<') 用平台宽度 int + 字符串拼接顶替
   var n int = len(payload)
   buf := fmt.Sprintf("%d", n) + string(payload)  // 错误：不是 4 字节小端，长度前缀变成十进制文本
   // 错误：用 for range 遍历二进制串（按 UTF-8 解码，逐字节语义丢失）
   for _, ch := range macBytes { fmt.Printf("%02x", ch) } // 错误：macBytes 含非 UTF-8 字节时得到码点而非字节
   // 正确：定宽小端编码 + 显式字节遍历
   var hdr [4]byte
   binary.LittleEndian.PutUint32(hdr[:], uint32(len(payload)))
   frame := append(hdr[:], payload...)
   for i := 0; i < len(macBytes); i++ { fmt.Printf("%02x", macBytes[i]) }
   ```
6. **信息不足或实现相关时的处理**：Ruby 格式字符串的宽度/字节序（`'I<'` 与 `'I'`、`'V'` 与 `'N'`）必须逐个确认后才选 Go 侧 API；源数据是文本还是二进制无法从局部源码判定（来自 socket、注册表、子进程输出）时必须标注并询问，不得默认按文本处理；`RubySMB`/`Rex`/`Win32::Registry` 等框架 API 返回值的字节布局属框架契约，本地源码不足以确认时应把该点列为缺口。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)；[GO-PKG-BINARY](https://pkg.go.dev/encoding/binary)；[GO-PKG-HEX](https://pkg.go.dev/encoding/hex)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
