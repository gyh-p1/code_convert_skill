---
name: go-to-ruby
description: Use when converting Go source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → Ruby 语言转换规则

> **适用基线**：Go 1.27 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 Ruby](../../references/languages/ruby.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Go → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-RB-01：Go map 无序遍历向 Ruby Hash 有序插入遍历的隔离映射
1. **源码触发条件**：Go 源码中通过 `for k, v := range m` 遍历哈希表。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Map_types](https://go.dev/ref/spec)）；目标语言 CRuby 3.4（[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)）。
3. **原可观察行为**：Go 语言规范明确未规定 map 遍历顺序（故意引入随机种子打乱顺序）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby 的 `Hash` 规范**强制保证按键值对的插入顺序遍历**！转换至 Ruby 后，代码切不可隐式产生“顺序依赖”；若业务需要无序性（如测试随机打乱），必须显式调用 `.to_a.shuffle`。
   - *不适用条件*：严禁在转换后代码中依赖插入顺序作为业务逻辑前提，否则逆向回 Go 时必崩溃。
5. **错误机械替换反例**：
   ```ruby
   # 错误：误以为 Ruby Hash 与 Go 一样是随机遍历，编写了依赖顺序或未打乱的逻辑
   # Go: for k := range m { ... } // 每次运行顺序不同
   # Ruby: h.each { |k, v| ... } // 永远按照严格的插入顺序遍历！
   ```
6. **信息不足或实现相关时的处理**：在转换报告中明确标记 Ruby Hash 存在插入有序性保证的事实。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Map_types](https://go.dev/ref/spec)；[RB-DOC-HASH](https://docs.ruby-lang.org/en/3.4/Hash.html)。

### 规则 GO-RB-02：Go 定宽整数模截断向 Ruby 任意精度 Integer 显式掩码映射
1. **源码触发条件**：Go 源码中使用 `uint32` 进行运算，依赖其超出 $2^{32}-1$ 时自动按模截断回绕。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：达到上限后自动截断回绕（非 UB）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Ruby 中计算后显式施加位掩码 `& 0xFFFFFFFF`，保留截断值。
   - *不适用条件*：严禁直接计算，Ruby `Integer` 自动升级为大数，高位数据残留导致哈希或校验和计算彻底错误。
5. **错误机械替换反例**：
   ```ruby
   # 错误：未加掩码截断，导致高位无限增长
   # Go: var h uint32 = 0xFFFFFFFF; h = h + 1 // h 变成 0
   h = 0xFFFFFFFF
   h = h + 1 # Ruby 中 h 变成了 4294967296，彻底失真！
   # 正确：显式截断
   h = (h + 1) & 0xFFFFFFFF
   ```
6. **信息不足或实现相关时的处理**：若涉及有符号数转换，提供补码还原函数。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 GO-RB-03：Go CSP 并发模型向 Ruby Queue/Mutex 与 GVL 约束映射
1. **源码触发条件**：Go 源码中使用多个 Goroutine 通过信道传递流水线数据。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)）。
3. **原可观察行为**：轻量协程高效流水线调度。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `Thread` 配合 `Thread::SizedQueue` 模拟带缓冲 Channel；在队列关闭时使用特定的标志对象（Sentinel Object）。
   - *不适用条件*：受 GVL 限制，纯 CPU 运算无法多核并行；注意未关闭队列会导致线程永久挂起。
5. **错误机械替换反例**：
   ```ruby
   # 错误：未关闭队列导致消费者线程 pop 永远阻塞发生死锁
   q = SizedQueue.new(10)
   # 生产者结束未通知，消费者 q.pop 永久挂死！
   # 正确：使用哨兵或关闭机制
   q.close
   ```
6. **信息不足或实现相关时的处理**：若需完全独立并发，建议采用 Ractor 模型并记录实验性质。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)。

### 规则 GO-RB-04：Go nil 与零值向 Ruby nil 与真值判断的映射
1. **源码触发条件**：Go 源码用 `if err != nil`、`if pr.EncodedBlob == ""`、`if len(b) == 0`、`if len(kv) != 2`、`if line != "" && len(line) < 200` 之类的判断分流，并用 `map[string]string` 承接解析结果（如 `inbox_batch_validate.go` 的 `if len(kv) != 2 { return nil, fmt.Errorf(...) }`、`signal_score_ingest.go` 的 `if err != nil || fi.IsDir()`、`manifest_hash_catalog.go` 的 `make([]fileMeta, 0, len(files))`）。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Comparison_operators](https://go.dev/ref/spec)）；目标语言 CRuby 3.4（[RB-DOC-CONTROL](https://docs.ruby-lang.org/en/3.4/syntax/control_expressions_rdoc.html)）。
3. **原可观察行为**：Go 中只有显式的 `nil`/零值比较才为真，`0`、`""`、空切片、空 map 都是普通值；`len(x) == 0` 与 `x == nil` 是不同判断；从 nil map 读取返回零值、写入则 panic。
4. **目标可选写法和不适用条件**：
   - *可选映射*：nil 状态映射为 Ruby `nil` 并显式写 `if x.nil?` / `unless x.nil?`；长度或内容判断显式写 `if x.empty?` / `if x == ""` / `if x.zero?`；从 map 取值需要区分“缺键”时用 `fetch` 或 `key?` 判断而不是 `h[k]`。
   - *不适用条件*：**严禁把 Go 的 `!= nil` 判断机械改写成 Ruby 的 `if x` 真值判断**——Ruby 中只有 `nil` 与 `false` 为假，`0`、`""`、`[]`、`{}` 全为真，因此 `if err` 在 `err` 是空串或 0 时不会进入分支，逻辑会被静默取反；也不得假定 Ruby 会像 Go 的 nil map 那样自动生成键（`h[k] += 1` 在缺键时对 `nil` 调 `+` 会抛 `NoMethodError`）。
5. **错误机械替换反例**：
   ```ruby
   # 错误：把 Go 的 err != nil / line != "" 直接写成真值判断
   def parse_kv(line)
     h = {}
     line.split(";").each do |p|
       k, v = p.split("=", 2)
       return nil if v.empty?          # v 为 nil 时抛 NoMethodError；"" 时又误判
       h[k] = v
     end
     return nil if h["mode"]           # Go 中这里是 h["mode"] == "" / 缺键判断
     h
   end
   # 正确：nil、空串、缺键分别显式判断
   def parse_kv(line)
     h = {}
     line.split(";").each do |p|
       next unless p.include?("=")
       k, v = p.split("=", 2)
       h[k] = v
     end
     return nil if h["mode"].nil?      # 对照 Go 的缺键 / nil 判断
     return nil if h["mode"].empty?    # 对照 Go 的 == "" 判断
     h
   end
   ```
6. **信息不足或实现相关时的处理**：若无法确认原 Go 判断表达的是“未设置（nil/缺键）”还是“值为零/空”，必须标注“nil 与零值语义待确认”，不得用统一真值判断合并两者。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Comparison_operators](https://go.dev/ref/spec)；[RB-DOC-CONTROL](https://docs.ruby-lang.org/en/3.4/syntax/control_expressions_rdoc.html)。

### 规则 GO-RB-05：Go defer 逆序清理向 Ruby ensure 块与块式资源方法的映射
1. **源码触发条件**：Go 源码用 `defer` 登记清理动作，例如 `signal_score_ingest.go` 的 `defer os.Remove(tmpPy)`、`defer resp.Body.Close()`、`defer cancel()`，以及 `loopback_tcp_receiver.go`/`notes_zip_bundle.go` 中 `defer ln.Close()`、`defer f.Close()` 与 zip 写入器的 `defer zipWriter.Close()` 顺序。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Defer_statements](https://go.dev/ref/spec)）；目标语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)、[RB-DOC-FILE](https://docs.ruby-lang.org/en/3.4/File.html)）。
3. **原可观察行为**：`defer` 在外层函数返回前按 LIFO 逆序执行，对正常返回、提前 `return` 与异常展开均生效；`os.Exit` 会跳过所有 `defer`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：函数级清理用 `begin ... ensure ... end`，多个清理按 Go 的逆序从上到下排列；文件/套接字等资源优先用块式 API（`File.open(path, "wb") { |f| ... }`）把关闭责任交给语言；只应清理一次的临时文件用 `ensure` 中的 `File.delete(path) if File.exist?(path)` 显式判存。
   - *不适用条件*：**严禁把 `ensure` 块的清理写成 `rescue` 或 `retry` 分支**——`ensure` 无条件执行，而 `rescue` 只在异常时执行，把清理放进 `rescue` 会让正常返回路径漏掉清理；也不得用 `exit!` 代替 `exit`（`exit!` 绕过 `ensure`，等价于 Go 中跳过 `defer` 的 `os.Exit`），不得把 `throw`/`catch` 当异常使用（`throw` 不触发展开语义，与 Go 的 `panic` 展开不同）。
5. **错误机械替换反例**：
   ```ruby
   # 错误：把 defer 的清理职责放进 rescue，正常返回时临时文件不删
   def run_python_stage(signals)
     tmp = File.join(Dir.tmpdir, "stage_#{Time.now.to_i}.py")
     File.write(tmp, PY_TRANSFORMER)
     out = `python3 #{tmp}`
     JSON.parse(out)
   rescue StandardError => e
     File.delete(tmp) if File.exist?(tmp)   # 只在异常时清理，正常返回泄漏临时文件
     raise
   end
   # 正确：ensure 无条件清理，顺序对齐 Go 的 LIFO
   def run_python_stage(signals)
     tmp = File.join(Dir.tmpdir, "stage_#{Time.now.to_i}.py")
     File.write(tmp, PY_TRANSFORMER)
     begin
       JSON.parse(`python3 #{tmp}`)
     ensure
       File.delete(tmp) if File.exist?(tmp)  # 对照 defer os.Remove(tmpPy)
     end
   end
   ```
6. **信息不足或实现相关时的处理**：若原 Go 代码在 `defer` 中修改具名返回值，或依赖 `defer` 在 `panic` 展开期间仍执行，必须标注“具名返回值副作用 / panic 展开期间的清理语义待确认”，不得假定 `ensure` 无条件承接。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Defer_statements](https://go.dev/ref/spec)；[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)、[RB-DOC-FILE](https://docs.ruby-lang.org/en/3.4/File.html)。

### 规则 GO-RB-06：Go []byte 字节切片向 Ruby String 编码标签的边界映射
1. **源码触发条件**：Go 源码对字节切片做哈希、Base64 编解码、压缩打包与读写，例如 `manifest_hash_catalog.go` 的 `sumHex(b []byte)`（`sha256` + `hex.EncodeToString`）、`notes_zip_bundle.go` 的 zip 写入、`signal_score_ingest.go` 的 `base64.StdEncoding.DecodeString(pr.EncodedBlob)` 校验分支、`loopback_ack_exchange.go` 的按字节拼接 `"ACK|" + parts[1] + "\n"`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #String_types](https://go.dev/ref/spec)）；目标语言 CRuby 3.4（[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)、[RB-DOC-ENCODING](https://docs.ruby-lang.org/en/3.4/Encoding.html)）。
3. **原可观察行为**：Go 的 `[]byte`/`string` 按原始字节处理，长度按字节计，允许非法 UTF-8；`string(b)` 与 `[]byte(s)` 互转不改变字节。
4. **目标可选写法和不适用条件**：
   - *可选映射*：字节路径用 `String#b` 或显式 `force_encoding(Encoding::BINARY)` 固定为 ASCII-8BIT，再做 `Digest::SHA256.digest`/`Base64.strict_encode64`/`pack("H*")` 等字节级操作；文本路径显式标 `Encoding::UTF_8` 并用 `encode`/`force_encoding` 在边界处转换；文件读写按用途选 `File.binread`/`File.binwrite` 与文本模式。
   - *不适用条件*：**严禁把二进制内容当作默认 UTF-8 的 `String` 直接参与拼接、正则或编码转换**——不同 `Encoding` 的两串拼接且无法无损转码时会抛 `Encoding::CompatibilityError`，对非法字节序列做 `encode`/`valid_encoding?` 检查失败会抛 `Encoding::InvalidByteSequenceError`/`UndefinedConversionError`，二者都会改变原程序“永不因编码失败”的可观察行为；也不得依赖 `String#length` 承接 Go 按字节计的长度（非 ASCII 时字符数不等于字节数）。
5. **错误机械替换反例**：
   ```ruby
   # 错误：把 Go 的 hex.EncodeToString(sha256.Sum256(b)) 机械写成文本路径
   content = File.read(path)                 # 文本模式：按外部编码解码，字节已被改写
   hex = Digest::SHA256.hexdigest(content)   # 校验和与 Go 版不一致
   # 正确：字节进字节出，必要时再显式解码为文本
   content = File.binread(path).force_encoding(Encoding::BINARY)
   hex = Digest::SHA256.hexdigest(content)   # 对照 Go 的 sumHex(b []byte)
   text  = content.dup.force_encoding(Encoding::UTF_8)
   text = text.encode(Encoding::UTF_8) if text.valid_encoding? == false  # 边界处显式处理
   ```
6. **信息不足或实现相关时的处理**：若无法确认原数据的编码，或原 Go 代码依赖按字节的长度与切片下标语义，必须标注“编码与字节长度语义待确认”，不得用 `scrub`/`encode(invalid: :replace)` 之类的宽松策略掩盖差异。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #String_types](https://go.dev/ref/spec)；[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)、[RB-DOC-ENCODING](https://docs.ruby-lang.org/en/3.4/Encoding.html)。

### 规则 GO-RB-07：被丢弃的文件打开错误不能变成 Ruby 的异常终止
1. **源码触发条件**：Go 以 `f, _ := os.Open(path)` 丢弃打开错误，将可能为 nil 的 `*os.File` 交给 `bufio.Scanner`，不检查 `Scanner.Err()`，后续仍生成结果。
2. **冻结版本/运行时/API 前提**：Go 1.27 → Ruby 3.4；需确认源码确实忽略打开、扫描和 `Close` 的错误，且目标路径与输出义务已冻结。
3. **原可观察行为**：本触发形态下，打开失败得到 nil `*os.File`；其 `Read`/`Close` 返回 `os.ErrInvalid` 而非自动 panic，`Scanner.Scan()` 因读取错误返回 false。若调用方不查 `Scanner.Err()`，可继续以空结果写报告并以 0 退出（前提是后续写入成功）。Ruby `File.open` 则会抛如 `Errno::ENOENT` 的异常，未经处理时提前终止。
4. **目标可选写法和不适用条件**：只在源确实丢弃该错误时，把 `File.open` 的相应系统错误转换成 nil，并以 `if f` 跳过扫描、在清理处用 `f&.close`，保留后续空结果路径；不要用包围整个函数的宽泛 `rescue` 吞掉解析或报告写入错误。若 Go 检查 `err` 或 `Scanner.Err()`、主动返回非零状态，Ruby 必须保留那个失败分支，不能套用“忽略并继续”。
5. **错误机械替换反例**：
   ```ruby
   f = File.open(path, 'rb')                 # 错误：缺文件时提前抛异常
   f = begin
     File.open(path, 'rb')
   rescue SystemCallError
     nil
   end
   begin
     f.each_line { |line| consume(line) } if f # 仅在源忽略打开/扫描错误时继续
   ensure
     f&.close
   end
   ```
6. **信息不足或实现相关时的处理**：若不清楚 Go 是否检查 `Scanner.Err()`、`defer f.Close()` 的返回值、或后续报告写入是否成功，不能断言退出码和产物；把打开失败路径单列为待验证 oracle。
7. **直接官方 HTTPS 依据链接**：[Go `os.File` nil 接收者的 `ErrInvalid`](https://pkg.go.dev/os#ErrInvalid)；[Go `bufio.Scanner.Scan`](https://pkg.go.dev/bufio#Scanner.Scan)；[Ruby 3.4 `Errno`](https://docs.ruby-lang.org/en/3.4/Errno.html)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
