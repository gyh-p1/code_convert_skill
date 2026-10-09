---
name: c-to-ruby
description: Use when converting C source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C → Ruby 语言转换规则

> **适用基线**：ISO C11 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C](../../references/languages/c.md)与[目标语言 Ruby](../../references/languages/ruby.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 C-RB-01：C 整数溢出截断与布尔真假向 Ruby 任意精度 Integer 与真值模型映射
1. **源码触发条件**：C 源码中以 `0` 作为假进行条件判断，或利用定宽整数溢出回绕实现循环哈希算法。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：C 中 `0` 为假；数值到达上限后按模截断。
4. **目标可选写法和不适用条件**：
   - *可选映射*：条件判断显式写为 `if val != 0`；数值回绕显式施加位掩码 `& 0xFFFFFFFF`。
   - *不适用条件*：**致命禁区**：绝对禁止将 C 代码 `if (x)` 机械转换为 Ruby `if x`（Ruby 中 `0` 与 `""` 均为真，直接反转控制流！）。
5. **错误机械替换反例**：
   ```ruby
   # 错误：C 中 0 为假，Ruby 中 0 为真，逻辑彻底颠倒！
   status = 0 # C 原型返回 0 表示成功
   if status  # 错误：在 Ruby 中 0 为真（Truthy），导致错误分支在成功时反向执行！
     handle_error()
   end
   # 正确：显式与 0 比较
   if status != 0
     handle_error()
   end
   ```
6. **信息不足或实现相关时的处理**：扫描所有源判断表达式，标明隐式非零假定。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 C-RB-02：C 手动资源释放向 Ruby 块模式 (Block/Yield) 与 ensure 映射
1. **源码触发条件**：C 源码中使用 `fopen`/`fclose`、`malloc`/`free` 配对管理生命周期。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/), [RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)）。
3. **原可观察行为**：函数退出或提前返回时显式调用释放函数。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重构为接收代码块的作用域模式（如 `File.open(...) do |f| ... end`），或使用 `begin ... ensure close end` 结构。
   - *不适用条件*：严禁依赖 Ruby GC 的自动终结清理文件描述符或套接字，可能导致句柄泄漏。
5. **错误机械替换反例**：
   ```ruby
   # 错误：打开文件后未通过块或 ensure 关闭，依赖 GC 终结导致描述符耗尽
   def read_data(path)
     f = File.open(path, 'rb')
     f.read # 错误：如果发生异常或多次调用，文件句柄直到下一次 GC 前保持打开！
   end
   # 正确：使用代码块保证离开时立即关闭
   def read_data(path)
     File.open(path, 'rb') { |f| f.read }
   end
   ```
6. **信息不足或实现相关时的处理**：若涉及文件 I/O，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)。

### 规则 C-RB-03：C 细粒度并发向 Ruby Thread/Mutex 与 MRI GVL 约束映射
1. **源码触发条件**：C 源码中通过多线程加速纯 CPU 计算密集任务。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11；目标语言 CRuby 3.4（[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html), [RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)）。
3. **原可观察行为**：C 线程在多个物理 CPU 核心上实现真正的并行执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：I/O 密集型并发使用 `Thread` 与 `Mutex`；CPU 密集型必须重构为 `Ractor` 或多进程（`Process.fork`），并在报告中声明并发模型转变。
   - *不适用条件*：严禁假设 Ruby `Thread` 能直接并行计算；MRI 全局 VM 锁（GVL）限制同一时刻仅一个线程执行 Ruby 字节码。
5. **错误机械替换反例**：
   ```ruby
   # 错误：期望通过多个 Thread 加速 CPU 密集计算，因 GVL 限制毫无加速甚至变慢
   threads = 4.times.map do
     Thread.new { compute_heavy_hash() }
   end
   threads.each(&:join) # 无法利用多核！
   ```
6. **信息不足或实现相关时的处理**：若需要系统原生线程同步，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-THREAD](https://docs.ruby-lang.org/en/3.4/Thread.html)；[RB-DEV-GC](https://docs.ruby-lang.org/en/3.4/extension_rdoc.html)。

### 规则 C-RB-04：C 字节缓冲的整数下标访问向 Ruby 二进制 String 与 getbyte/bytesize 映射
1. **源码触发条件**：C 源码用 `unsigned char payload[] = {0xfc, 0x48, ...}`、`char incominginstructions[2000]` 等缓冲承载字节，并以下标读取整数（`in[len-1-i] != pad`、`printf("%02x ", payload[i])`、`payload[4*i+1] << 8`），或数据中可能含中间 `0x00`、`0x80` 以上字节。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（[WG14-N1570 §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)，`char` 的符号性由实现定义）；目标语言 CRuby 3.4（[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html), [RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：`buf[i]` 在 C 中产生整数值（`unsigned char` 恒为 0..255，`char` 可能为负）；长度是字节数；`\0` 可出现在中间且不影响按长度遍历的结果。
4. **目标可选写法和不适用条件**：
   - *可选映射*：字节缓冲用带 `Encoding::BINARY`（`ASCII-8BIT`）标签的 `String`（字面量后接 `#b`，或 `force_encoding(Encoding::BINARY)`）；长度用 `#bytesize`；逐字节取值用 `#getbyte(i)`/`#bytes`，写回用 `#setbyte` 或构造后再 `#b`；需要宽度与端序时改用 `#unpack1`/`Array#pack`。
   - *不适用条件*：严禁把 `buf[i]` 直译为 Ruby `buf[i]`——Ruby 3.4 的 `String#[]` 按整数下标返回单字符 `String`（整数区间返回子串），与整数比较恒为不相等、参与算术或与整数比较会抛类型错误；严禁对二进制缓冲使用字符语义方法（`#chars`、`#upcase`、依赖编码的 `#length`）；严禁把二进制与 UTF-8 文本直接拼接（编码不兼容会抛 `Encoding::CompatibilityError`）。
5. **错误机械替换反例**：
   ```ruby
   # 错误：把 C 的按整数下标访问直译过来（pkcs7 去填充形状）
   return 0 if data.bytesize.zero?
   pad = data[data.bytesize - 1]        # 得单字符 String，而不是 Integer
   return data.bytesize if pad != 16    # 错误：String != Integer 恒为真，校验分支被静默跳过
   # 正确：二进制缓冲用 getbyte/bytesize 做字节级比较
   data = data.b
   pad = data.getbyte(data.bytesize - 1)
   return data.bytesize if pad.nil? || pad > 16
   ```
6. **信息不足或实现相关时的处理**：若无法确认该缓冲是"文本"还是"任意字节"（尤其载荷、密钥、加密块、网络帧），必须停下确认编码意图，不得默认按 UTF-8 处理；`char` 符号性与源字节序未给出时必须标注为待确认。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 C-RB-05：C memcpy/指针强转的字节↔定宽整数重解释向 Ruby unpack1/pack 显式端序映射
1. **源码触发条件**：C 源码用 `memcpy(&a, in, 4)`/`*(uint32_t *)p` 在 4 字节与 `uint32_t` 间重解释，用手工位移拼装小端序整数（`((uint32_t)userkey[4*i+1] << 8) | ...`），用 `#define ROTL32(x,n)`/`ROTR32` 做 32 位旋转，或用 `(x & 0xFFFF)`/`>> 16` 处理序号与位域。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（[WG14-N1570 §6.2.6, §6.5.7](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）；目标语言 CRuby 3.4（[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html), [RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)）。
3. **原可观察行为**：`memcpy` 按主机字节序逐字节复制，结果依赖字节序；`uint32_t` 的移位与旋转严格按 32 位宽回绕；对负值右移由实现定义（通常为算术移位）；`(x & 0xFFFF)` 把高位清零。
4. **目标可选写法和不适用条件**：
   - *可选映射*：用显式端序指令做字节↔整数转换（`str.unpack1('V')` 小端 32 位无符号、`'N'` 大端、`'Q<'` 小端 64 位；写回用 `[v].pack('V')`）；32 位旋转先掩码再运算：`x = (((x << n) | (x >> (32 - n))) & 0xFFFFFFFF)`；`x & 0xFFFF` 直接用 `Integer#&`。
   - *不适用条件*：严禁使用依赖宿主字节序/宽度的指令（如 `'L'`/`'l'`）来替代源码中已确定的端序与宽度；严禁把 C 的定宽移位/旋转直译为 Ruby 位运算而不做位宽掩码——Ruby `Integer` 是任意精度，`>>` 对负值按无限补码展开，会得到负值或超宽结果，旋转不再等价；严禁用 `String#to_i`、十六进制解析或字符转换替代字节重解释（`memcpy` 是位模式复制，不是数值解析）。
5. **错误机械替换反例**：
   ```ruby
   # 错误：无端序指令、无位宽掩码的机械翻译
   a = in[0, 4].unpack1('L')          # 'L' 为宿主原生字节序/宽度，与源码的小端假设不一致
   rot = (a << 13) | (a >> 19)        # 错误：未掩码，且 >> 对负值按无限补码展开
   # 正确：显式小端序 + 32 位掩码后再旋转
   a = in[0, 4].unpack1('V')
   a &= 0xFFFFFFFF
   rot = ((a << 13) | (a >> 19)) & 0xFFFFFFFF
   ```
6. **信息不足或实现相关时的处理**：源文件未声明目标字节序、整数宽度或 `char` 符号性时，必须停标为待确认；涉及的加密/校验算法若依赖具体位宽，必须同时记录该位宽假设，不得凭本机实现假定小端序。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.2.6, §6.5.7](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)；[RB-DOC-ARRAY](https://docs.ruby-lang.org/en/3.4/Array.html)。

### 规则 C-RB-06：C 返回计数/EOF 与文本模式 I/O 向 Ruby IO 的 nil-EOF 与二进制模式映射
1. **源码触发条件**：C 源码用 `while ((c = fgetc(f1)) != EOF)`、`while (fgets(outgoingoutp + total, ..., stdoutp) != NULL)`、`recv`/`read`/`write`/`splice` 的返回值控制循环，用 `if (nbytes < 0)`/`(size_t)nbytes < data_size` 判失败或短写，用 `fopen(path, "r")`/`"w"` 文本模式，或读完后用 `strlen(outgoingoutp)` 重算长度。
2. **冻结版本/运行时/API 前提**：源语言 ISO C11（[WG14-N1570 §7.21](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）与 POSIX 读写返回约定（[POSIX](https://pubs.opengroup.org/onlinepubs/9699919799/)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：`fgetc` 在 EOF/错误时返回 `EOF`（负值，与 0..255 的字节值不重叠）；`read`/`recv` 返回实际字节数，可能小于请求量，失败返回 -1；文本模式在 Windows 上会把 `\r\n` 转换成 `\n`，改变字节数与内容。
4. **目标可选写法和不适用条件**：
   - *可选映射*：显式二进制模式 `File.open(path, 'rb') { |f| ... }`；整块读取用无参 `IO#read`（读到 EOF），分块读取用 `IO#read(n)`（EOF 时返回 `nil`）；流式/套接字读取用 `readpartial`（EOF 抛 `EOFError`）或 `each_byte`/`each_line` 迭代；写入用 `IO#write` 并说明短写由运行时处理，需要时显式比较其返回的字节数。
   - *不适用条件*：严禁把 `EOF`/`-1` 直译为 `0`：Ruby `IO#read(n)` 在 EOF 返回 `nil`，`File#getc` 在 EOF 也返回 `nil`，与 C 的 `EOF` 判断形状不同，`while (n = f.read(1))` 之类的写法必须按 `nil` 语义重写；严禁省略 `'b'` 模式（Windows 上的换行转换会改变字节流长度与内容）；严禁用按字符截断或搜索 `\0` 的方式重算已读长度，必须使用读取返回值或 `#bytesize`。
5. **错误机械替换反例**：
   ```ruby
   # 错误：把 C 的 EOF(-1) 与 strlen 长度语义直译过来
   f = File.open(path, 'r')             # 文本模式：Windows 上会转换换行
   while (c = f.getc) && c != -1        # EOF 时 getc 返回 nil，不是 -1
     out << c
   end
   total = out.length                   # 字符数，而不是字节数
   # 正确：二进制模式 + nil-EOF 语义 + 字节计数
   File.open(path, 'rb') { |f2| out << f2.read }   # 无参 read 读到 EOF
   total = out.bytesize
   ```
6. **信息不足或实现相关时的处理**：源文件的打开模式（`"r"` 与 `"rb"`）、目标平台是否为 Windows、以及"部分读/短写是否必须显式循环"未确认时，必须停标并说明换行/编码转换与短写语义可能改变；不得假定文本模式与二进制模式等价。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §7.21](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[POSIX](https://pubs.opengroup.org/onlinepubs/9699919799/)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
