---
name: go-to-ruby
description: Use when converting Go source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → Ruby 语言转换规则

> **适用基线**：Go 1.27 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 Go](../../references/languages/go.md)与[目标语言 Ruby](../../references/languages/ruby.md)，按源码选择适用规则。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Go → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-RB-01：Go map 无序遍历向 Ruby Hash 有序插入遍历的隔离映射
1. **源码触发条件**：Go 源码中通过 `for k, v := range m` 遍历哈希表。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Map_types）；目标语言 CRuby 3.4（RB-DOC-HASH）。
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
7. **资料依据（名称/版本/章节）**：GO-SPEC #Map_types；RB-DOC-HASH。

### 规则 GO-RB-02：Go 定宽整数模截断向 Ruby 任意精度 Integer 显式掩码映射
1. **源码触发条件**：Go 源码中使用 `uint32` 进行运算，依赖其超出 $2^{32}-1$ 时自动按模截断回绕。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Arithmetic_operators）；目标语言 CRuby 3.4（RB-DOC-CORE）。
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
7. **资料依据（名称/版本/章节）**：GO-SPEC #Arithmetic_operators；RB-DOC-CORE。

### 规则 GO-RB-03：Go CSP 并发模型向 Ruby Queue/Mutex 与 GVL 约束映射
1. **源码触发条件**：Go 源码中使用多个 Goroutine 通过信道传递流水线数据。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 CRuby 3.4（RB-DOC-THREAD）。
3. **原可观察行为**：轻量协程高效流水线调度。
4. **目标可选写法和不适用条件**：
   - *可选映射*：仅容量、发送/接收会合、关闭后排空/零值与成功标志、关闭发送失败及 select 义务都可对应时考虑 Thread/SizedQueue。普通队列或 sentinel 不自动承接无缓冲 channel；sentinel 还可能占容量或与合法数据冲突，不能默认添加。
   - *不适用条件*：受 GVL 限制，纯 CPU 运算无法多核并行；注意未关闭队列会导致线程永久挂起。
5. **错误机械替换反例**：
   ```ruby
   # 错误：未关闭队列导致消费者线程 pop 永远阻塞发生死锁
   q = SizedQueue.new(10)
   # 生产者结束未通知，消费者 q.pop 永久挂死！
   # 队列关闭只是候选动作，还须核源 channel 的排空/零值与发送失败；非完整映射
   q.close
   ```
6. **信息不足或实现相关时的处理**：共享、容量/关闭/select 或调度消费者未知时记录具体缺口，停止受影响映射；不因性能或“独立并发”改成 Ractor，也不以记录实验性质代允许差异。
7. **资料依据（名称/版本/章节）**：RB-DOC-THREAD。

### 规则 GO-RB-04：Go nil 与零值向 Ruby nil 与真值判断的映射
1. **源码触发条件**：Go 源码用 `if err != nil`、`if pr.EncodedBlob == ""`、`if len(b) == 0`、`if len(kv) != 2`、`if line != "" && len(line) < 200` 之类的判断分流，并用 `map[string]string` 承接解析结果（如 `inbox_batch_validate.go` 的 `if len(kv) != 2 { return nil, fmt.Errorf(...) }`、`signal_score_ingest.go` 的 `if err != nil || fi.IsDir()`、`manifest_hash_catalog.go` 的 `make([]fileMeta, 0, len(files))`）。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Comparison_operators）；目标语言 CRuby 3.4（RB-DOC-CONTROL）。
3. **原可观察行为**：Go 中只有显式的 `nil`/零值比较才为真，`0`、`""`、空切片、空 map 都是普通值；`len(x) == 0` 与 `x == nil` 是不同判断；从 nil map 读取返回零值、写入则 panic。
4. **目标可选写法和不适用条件**：
   - *可选映射*：nil 状态映射为 Ruby `nil` 并显式写 `if x.nil?` / `unless x.nil?`；长度或内容判断显式写 `if x.empty?` / `if x == ""` / `if x.zero?`；从 map 取值需要区分“缺键”时用 `fetch` 或 `key?` 判断而不是 `h[k]`。
   - *不适用条件*：Ruby 真值仅排除 nil/false，0 与空串仍为真；是否可用 if x 承接非 nil 判断取决于目标值域是否含 false，不能声称空串/0 会跳过分支。Go nil map 读零值、写 panic，Ruby Hash 的缺键/默认值/写入须分别对应，不声称 Go 会自动创建键。
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
7. **资料依据（名称/版本/章节）**：GO-SPEC #Comparison_operators；RB-DOC-CONTROL。

### 规则 GO-RB-05：Go defer 逆序清理向 Ruby ensure 块与块式资源方法的映射
1. **源码触发条件**：Go 源码用 `defer` 登记清理动作，例如 `signal_score_ingest.go` 的 `defer os.Remove(tmpPy)`、`defer resp.Body.Close()`、`defer cancel()`，以及 `loopback_tcp_receiver.go`/`notes_zip_bundle.go` 中 `defer ln.Close()`、`defer f.Close()` 与 zip 写入器的 `defer zipWriter.Close()` 顺序。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #Defer_statements）；目标语言 CRuby 3.4（RB-DOC-EXCEPT、RB-DOC-FILE）。
3. **原可观察行为**：`defer` 在外层函数返回前按 LIFO 逆序执行，对正常返回、提前 `return` 与异常展开均生效；`os.Exit` 会跳过所有 `defer`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：函数级 ensure 须对应实际注册的动作、注册时参数、LIFO 及退出边界；块式资源 API 只在块结束就是源函数级释放点时适用。源忽略 os.Remove/Close 失败时不得让 Ruby 删除/关闭异常新增传播，也不添加源不存在的先查存在后删除。
   - *不适用条件*：rescue/retry 不自动承接所有清理路径；Go os.Exit 跳过 defer，Ruby exit 会展开 ensure，exit! 则跳过退出处理，须逐项核退出码/清理/缓冲副作用后选用，不能全禁 exit!。Ruby throw/catch 是非局部控制流，不能当成异常类型/捕获范围的直接等价，也不能声称其不展开 ensure。
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
7. **资料依据（名称/版本/章节）**：GO-SPEC #Defer_statements；RB-DOC-EXCEPT、RB-DOC-FILE。

### 规则 GO-RB-06：Go []byte 字节切片向 Ruby String 编码标签的边界映射
1. **源码触发条件**：Go 源码对字节切片做哈希、Base64 编解码、压缩打包与读写，例如 `manifest_hash_catalog.go` 的 `sumHex(b []byte)`（`sha256` + `hex.EncodeToString`）、`notes_zip_bundle.go` 的 zip 写入、`signal_score_ingest.go` 的 `base64.StdEncoding.DecodeString(pr.EncodedBlob)` 校验分支、`loopback_ack_exchange.go` 的按字节拼接 `"ACK|" + parts[1] + "\n"`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（GO-SPEC #String_types）；目标语言 CRuby 3.4（RB-DOC-STRING、RB-DOC-ENCODING）。
3. **原可观察行为**：Go 的 `[]byte`/`string` 按原始字节处理，长度按字节计，允许非法 UTF-8；`string(b)` 与 `[]byte(s)` 互转不改变字节。
4. **目标可选写法和不适用条件**：
   - *可选映射*：字节路径用 `String#b` 或显式 `force_encoding(Encoding::BINARY)` 固定为 ASCII-8BIT，再做 `Digest::SHA256.digest`/`Base64.strict_encode64`/`pack("H*")` 等字节级操作；文本路径显式标 `Encoding::UTF_8` 并用 `encode`/`force_encoding` 在边界处转换；文件读写按用途选 `File.binread`/`File.binwrite` 与文本模式。
   - *不适用条件*：不得为原始字节路径新增转码/替换或传播源不存在的编码失败；拼接按 Encoding.compatible? 核对，valid_encoding? 返回 false 本身不抛错。length 与 bytesize 按源消费者选择；不能把任意字节的读取等同于所有后续操作均不失败。
5. **错误机械替换反例**：
   ```ruby
   # 风险候选：文本 IO 配置可能改变字节；需核精确模式，不能只凭接口名断言不同
   content = File.read(path)                 # 是否改字节取决于 IO 转码/文本模式；只改标签不自动改变摘要
   hex = Digest::SHA256.hexdigest(content)   # 不能仅凭 File.read 就断言摘要不同，需核真实字节
   # 正确：字节进字节出，必要时再显式解码为文本
   content = File.binread(path).force_encoding(Encoding::BINARY)
   hex = Digest::SHA256.hexdigest(content)   # 对照 Go 的 sumHex(b []byte)
   # 只有源明确解码/验证时才进入文本边界；force_encoding 不校验或修复非法字节。
   ```
6. **信息不足或实现相关时的处理**：若无法确认原数据的编码，或原 Go 代码依赖按字节的长度与切片下标语义，必须标注“编码与字节长度语义待确认”，不得用 `scrub`/`encode(invalid: :replace)` 之类的宽松策略掩盖差异。
7. **资料依据（名称/版本/章节）**：GO-SPEC #String_types；RB-DOC-STRING、RB-DOC-ENCODING。

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
7. **资料依据（名称/版本/章节）**：Go `os.File` nil 接收者的 `ErrInvalid`；Go `bufio.Scanner.Scan`；Ruby 3.4 `Errno`。

### 规则 GO-RB-08：部分字节与EOF/异常的选择引导

触发为源实际消费Reader返回的有效长度与错误；先读[Go L1-GO-12](../../references/languages/go.md#l1-go-12-合流与部分读取的消费顺序)及Ruby字节/错误正文。Go的n、err不直接等于Ruby一个String或一次异常。Ruby3.4 IO.readpartial正长度请求可返回当时取得的块，在无数据的EOF抛EOFError；此前已经返回的块仍须按源消费者保留，不能因后续异常清空累计结果。长度0的分支另按两侧接口核，不套正长度的EOF条件。

只有源确实先消费有效字节再处理EOF/错误时，才选择相应的块累积及局部异常分流；源有意丢弃或传播时保持对应路径。按实际Read/read/readpartial接口区分长度、阻塞、编码标签、nil/空串/EOF，不把所有异常rescue成成功，也不凭异常恢复不存在的字节。未能表达源返回形态时注明具体缺口。本条仅引导目标选择，不生成辅助驱动或要求回归。依据：Go io.Reader；Ruby3.4 IO.readpartial、字节读取与异常。

### 临时目录选择的适用边界

涉及 Go os.TempDir 与 Ruby Dir.tmpdir 时，分别读[Go L1-GO-07](../../references/languages/go.md#l1-go-07-ostempdir-选路径不检查目录可用性)与[Ruby L1-RB-09](../../references/languages/ruby.md#l1-rb-09-dirtmpdir-的候选顺序与有效性)。上文进程/清理例中的 Dir.tmpdir 只演示清理结构，不证明源目录选择已等价；候选优先级、可用性、回退/诊断依准确版本对应，不能借换目录使评估匹配。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
