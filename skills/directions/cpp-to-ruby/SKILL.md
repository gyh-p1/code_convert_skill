---
name: cpp-to-ruby
description: Use when converting C++ source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → Ruby 语言转换规则

> **适用基线**：ISO C++17 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C++](../../references/languages/cpp.md)与[目标语言 Ruby](../../references/languages/ruby.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 C++ → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-RB-01：C++ 拷贝构造与对象封装向 Ruby 对象引用与深拷贝映射
1. **源码触发条件**：C++ 源码中依赖对象按值传递或显式自定义拷贝构造函数完成深拷贝。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 CRuby 3.4（RB-DOC-CORE）。
3. **原可观察行为**：按源实际复制构造/赋值运算符决定成员复制、别名与资源所有权；C++ 复制并不普遍保证深拷贝，指针成员或共享资源可继续别名。仅源明确深拷贝的成员才要求独立，不能擅自把共享身份改成复制。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按源复制契约选择 `dup` 与 `initialize_copy`，显式复制需独立的成员并保留需共享的成员。Ruby `dup` 默认是浅复制，`initialize_copy` 也不会自动递归深复制；通用 Marshal 往返不能代替任意对象的复制契约，资源/身份/自定义钩子须另核，不反序列化不可信材料。
   - *不适用条件*：严禁认为 `b = a` 会产生独立拷贝，Ruby 仅复制对象引用别名。
5. **错误机械替换反例**：
   ```ruby
   # 错误：将对象别名直接传递，修改内部状态污染原对象
   class Config
     attr_accessor :data
     def initialize(d); @data = d; end
   end
   c1 = Config.new([1, 2])
   c2 = c1 # 仅仅是别名！
   c2.data << 3 # c1.data 也被污染变成 [1, 2, 3]！
   # 有条件的映射：源确实复制该整数数组时，initialize_copy 配合 dup
   class Config
     def initialize_copy(orig)
       super
       @data = orig.data.dup
     end
   end
   c2 = c1.dup
   ```
6. **信息不足或实现相关时的处理**：若对象包含复杂原生资源指针，在转换报告中标明不可序列化限制。
7. **资料依据（名称/版本/章节）**：C++17 复制构造 §15.8.1；Ruby Object#dup/initialize_copy。

### 规则 CPP-RB-02：C++ RAII 锁管理向 Ruby Mutex#synchronize 作用域映射
1. **源码触发条件**：C++ 源码中使用 `std::lock_guard<std::mutex> lock(mtx)`。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 CRuby 3.4（RB-DOC-THREAD）。
3. **原可观察行为**：进入作用域加锁，退出作用域无论是否抛出异常均自动解锁。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 `mutex.synchronize do ... end` 代码块。
   - *不适用条件*：严禁手动调用裸 `mutex.lock` 而不放在 `begin ... ensure mutex.unlock end` 中，否则异常会导致死锁。
5. **错误机械替换反例**：
   ```ruby
   # 错误：手动加锁未设 ensure，异常导致永久死锁
   mtx.lock
   dangerous_action() # 抛出异常！
   mtx.unlock # 永远无法执行，死锁！
   # 正确：使用 synchronize 块
   mtx.synchronize do
     dangerous_action()
   end
   ```
6. **信息不足或实现相关时的处理**：若代码涉及递归加锁，使用 `Monitor` 替代 `Mutex`。
7. **资料依据（名称/版本/章节）**：RB-DOC-THREAD。

### 规则 CPP-RB-03：C++ std::map 有序关联容器向 Ruby Hash 插入顺序语义约束
1. **源码触发条件**：C++ 源码中使用 `std::map<Key, Value>` 依赖遍历时按键升序排列的性质。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（WG21-N4659 Clause 26.4）；目标语言 CRuby 3.4（RB-DOC-HASH）。
3. **原可观察行为**：std::map 按实例的比较器排序，默认 std::less 只是一个情况；键等价也由比较器决定，不自动等于 Ruby hash/eql?。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Hash 插入顺序不代 map 比较序；仅源比较器与 Ruby 的排序/键等价一致时可考虑 Hash 加排序。自定义比较器的去重、查找、默认插入与遍历须一起保留，不只事后 sort_by。
   - *不适用条件*：严禁将 C++ `std::map` 机械替换为 Ruby 原生 `Hash` 后直接依赖遍历有序性，插入顺序不同将导致遍历结果完全不同。
5. **错误机械替换反例**：
   ```ruby
   # 错误：误以为 Ruby Hash 自动按键排序
   h = {}
   h[10] = "b"; h[1] = "a"
   h.keys # 得到 [10, 1]，而 C++ std::map 遍历得到的是 [1, 10]！
   # 条件候选：仅此整数键与源默认升序/等价一致时适用
   h.sort.each do |key, val|
     # 此处严格按键递增遍历
   end
   ```
6. **信息不足或实现相关时的处理**：若键类型无自然排序，向用户确认排序依据并在报告中标注。
7. **资料依据（名称/版本/章节）**：RB-DOC-HASH。

### 规则 CPP-RB-04：C++ 通用 RAII 与多出口清理向 Ruby `begin ... ensure` / 块作用域映射
1. **源码触发条件**：C++ 源码依赖类析构函数释放文件句柄、临时文件、网络连接、动态资源或回滚事务，且存在提前 `return` 或异常展开路径。
2. **冻结版本/运行时/API 前提**：ISO C++17（WG21-N4659 Clause 15.2）→ CRuby 3.4（RB-DOC-CORE、`ensure`、`ObjectSpace.define_finalizer`）。
3. **原可观察行为**：离开作用域时同步确定性执行析构函数，先构造后释放。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用标准块形式资源 API（如 `File.open(...) { |f| ... }`）或显式 `begin ... ensure ... end` 保证正常返回、提前返回及抛异常时同步确定性释放。多资源时嵌套块或逆序在 `ensure` 内保护性逐个释放，避免首个释放抛错掩盖其余释放。
   - *不适用条件*：严禁依赖 `ObjectSpace.define_finalizer` 模拟 C++ 析构（GC 回收时机不确定且受引用保留影响，进程退出行为亦有别）。
5. **错误机械替换反例**：
   ```ruby
   # 错误：将 C++ RAII 文件包装简化为显式 close 而不放进 ensure，提前 return 或异常即泄漏
   def process(path)
     f = File.open(path, "rb")
     return nil if f.size == 0 # 句柄泄漏！
     f.read
   ensure
     # 若 f 在上面赋值且此处统一判断 f&.close，才可保安全，否则 return nil 漏掉 close
   end

   # 正确：优先块作用域或 ensure 保护
   def process(path)
     File.open(path, "rb") do |f|
       return nil if f.size == 0
       f.read
     end
   end
   ```
6. **信息不足或实现相关时的处理**：若 C++ 析构函数中允许吞错或需保留主异常，Ruby `ensure` 中清理出错不能覆盖尚未处理的外层异常。
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 15.2；Ruby 3.4 `ensure` 与 `IO.open` 块协议。

### 规则 CPP-RB-05：C++ 向零除法与定宽回绕向 Ruby 整数除法与任意精度映射
1. **源码触发条件**：C++ 源码中存在负数整型 `/`、`%`，或依赖固定位宽整数（如 `uint32_t`/`uint64_t`）的模算术回绕与移位。
2. **冻结版本/运行时/API 前提**：ISO C++17 → CRuby 3.4（`Integer#div`、`Integer#modulo`、`Integer#remainder`）。
3. **原可观察行为**：C++ `/` 向零截断、`%` 符号与被除数一致（`-7 / 3 == -2`、`-7 % 3 == -1`）；无符号整数按位宽取模。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby `Integer#/` 与 `Integer#%` 均采用**向下取整（Floor）**（`-7 / 3 == -3`、`-7 % 3 == 2`）；与 C/C++ `%` 等价的向零取余是 `a.remainder(b)`，对应向零商为 `((a < 0) ^ (b < 0)) ? -(a.abs / b.abs) : (a.abs / b.abs)`。定宽无符号计算每次溢出/左移后须显式按位掩码（如 `& 0xFFFFFFFF`）截取。
   - *不适用条件*：严禁把负整数上的 C++ `/`、`%` 直接写成 Ruby `/`、`%`；严禁把 Ruby `Integer` 任意精度直接当作会自然 32/64 位回绕。
5. **错误机械替换反例**：
   ```ruby
   # 错误：直接使用 Ruby / 和 % 处理负数，并忽略 uint32 位宽截断
   q = -7 / 3   # Ruby 得 -3（C++ 为 -2）
   r = -7 % 3   # Ruby 得 2（C++ 为 -1）
   x = (0xFFFFFFFF + 2) # 得 4294967297（C++ uint32_t 为 1）

   # 正确：余数用 remainder，向零商用明确绝对值定号并加位宽掩码
   r = (-7).remainder(3)                  # 得 -1
   q = ((-7) - r) / 3                     # 得 -2
   x = (0xFFFFFFFF + 2) & 0xFFFFFFFF      # 得 1
   ```
6. **信息不足或实现相关时的处理**：若 C++ 原表达式混合有符号/无符号整型触发常规算术提升，先还原 C++ 提升后无符号宽度再加掩码。
7. **资料依据（名称/版本/章节）**：CRuby 3.4 `Integer#/`、`Integer#remainder`；WG21-N4659 Clause 8.6。

### 规则 CPP-RB-06：C++ 零值假判定向 Ruby 真值模型（`0`/`""`/`[]` 皆为真）防误判映射
1. **源码触发条件**：C++ 源码中存在 `if (count)`、`if (!err)`、`while (len)`、`if (ptr)` 等直接把整数、字符或指针当作布尔条件判断的表达式。
2. **冻结版本/运行时/API 前提**：ISO C++17（WG21-N4659 Clause 7.14）→ CRuby 3.4（RB-DOC-CORE Truthiness）。
3. **原可观察行为**：C++ 中 `0`、`'\0'`、`0.0`、`nullptr` 转为 `bool` 均评估为 `false`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Ruby 中**只有 `false` 和 `nil` 为假**——整数 `0`、浮点数 `0.0`、空字符串 `""`、空数组 `[]` 全部为真（Truthy）！因此 C++ 数值/长度条件必须显式补全 `!= 0` / `== 0`，指针判空显式用 `nil?` / `!ptr.nil?`。
   - *不适用条件*：严禁把 C++ `if (n)`、`if (!rc)` 直接译为 Ruby `if n`、`unless rc`（在 Ruby 中 `n == 0` 时条件恒为真，逻辑完全反转！）。
5. **错误机械替换反例**：
   ```ruby
   # 错误：将 C++ if (!status_code) 机械写成 unless status_code
   status_code = 0 # C++ 表示成功（假），但在 Ruby 中 0 是 truthy！
   puts "ok" unless status_code # 永远不会输出 "ok"！

   # 正确：显式比较 0 与 nil
   puts "ok" if status_code == 0
   ```
6. **信息不足或实现相关时的处理**：对同时返回整数错误码或 `nil` 的函数，明确区分 `nil?` 与 `== 0`。
7. **资料依据（名称/版本/章节）**：CRuby 3.4 语言真值语义；WG21-N4659 Clause 7.14。

### 规则 CPP-RB-07：C++ `std::string` 原始字节向 Ruby `ASCII-8BIT` 二进制编码映射
1. **源码触发条件**：C++ 源码将 `std::string` 用于字节协议、加密/哈希缓冲、二进制文件读取或可能包含 `\0` 与非 UTF-8 字节的内容。
2. **冻结版本/运行时/API 前提**：ISO C++17 → CRuby 3.4（`String#encoding`、`Encoding::BINARY`/`ASCII_8BIT`、`bytesize`）。
3. **原可观察行为**：`std::string::size()` 与下标按单字节处理，不要求合法 UTF-8 编码，也不会因非 UTF-8 序列抛出编码异常。
4. **目标可选写法和不适用条件**：
   - *可选映射*：二进制缓冲与原始协议数据使用 `Encoding::ASCII_8BIT`（别名 `BINARY`），创建字面量或转码缓冲时明确 `.b`，并以 `.bytesize` / `.getbyte(i)` / `.byteslice` 替代按字符（Codepoint）计数的 `.length` / `[]`。文件读写对应 `"rb"` / `"wb"` 二进制模式。
   - *不适用条件*：严禁对原始字节 `String` 默认使用 UTF-8 字符串的 `.length` / `.chars` / 正则拼接，这会在非 UTF-8 字节上触发 `Encoding::CompatibilityError` 或 `ArgumentError: invalid byte sequence in UTF-8`。
5. **错误机械替换反例**：
   ```ruby
   # 错误：以 UTF-8 模式读取或对原始二进制 String 使用 .length 计算字节数
   raw = "\xFF\x00A"
   len = raw.length # 若为非合法 UTF-8 后续调用 split/gsub/encode 直接抛异常！

   # 正确：声明 ASCII-8BIT 并用 bytesize / byteslice
   raw = "\xFF\x00A".b
   len = raw.bytesize # 稳定返回 3，支持嵌入 \x00 与任意字节
   ```
6. **信息不足或实现相关时的处理**：若同一字符串后续要输出为 UTF-8 文本或 JSON，记录源文本/二进制边界与失败处理，不随意 `scrub`。
7. **资料依据（名称/版本/章节）**：CRuby 3.4 `String#b`、`String#bytesize`、`Encoding`。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
