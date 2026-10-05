---
name: ruby-to-c
description: Use when converting Ruby source to C; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → C 语言转换规则

> **适用基线**：CRuby 3.4 → ISO C11。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Ruby](../../references/languages/ruby.md)与[目标语言 C](../../references/languages/c.md)。
> **方向案例与证据**：如本地工作区存在 `docs/test/dataset/ruby-to-c/README.md`，按其中 case 分层查看；该本地数据目录不随 Git/Skill 分发。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Ruby → C 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 RB-C-01：Ruby 真值模型 (0 为真) 向 C 条件分支逻辑翻转防范映射
1. **源码触发条件**：Ruby 源码中使用 `if val`，且 `val` 的计算结果可能为数值 `0`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 ISO C11（[WG14-N1570 §6.8.4.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：**在 Ruby 中 `0` 为真（Truthy）**，`if 0` 分支必然进入执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C 语言中 `0` 代表假！若源 Ruby 代码依赖了 `0` 为真（即仅有 `nil` 或 `false` 时才不执行），在 C 中必须显式转换为检查“是否存在/有效”的标志位；若该变量本身是业务状态码，必须显式重写条件。
   - *不适用条件*：**致命禁区**：严禁直接机械翻译为 C 的 `if (val)`，因为当 `val == 0` 时，C 语言会判定为假直接跳过分支，导致逻辑 100% 翻转！
5. **错误机械替换反例**：
   ```c
   // 错误：Ruby 原型为 if val (val 可能为 0，依然执行分支)
   // 在 C 中直接写 if (val)：
   int val = 0;
   if (val) { // 错误：在 C 中 0 为假，分支被跳过！与 Ruby 运行结果相反！
       action();
   }
   // 正确：显式检查是否有效
   if (is_valid) {
       action();
   }
   ```
6. **信息不足或实现相关时的处理**：在报告中标记所有由 Ruby 真值模型引发的潜在条件歧义。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[WG14-N1570 §6.8.4.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

### 规则 RB-C-02：Ruby 动态方法派发与开放类向 C 固定数据结构与函数指针映射
1. **源码触发条件**：Ruby 源码中使用动态方法查找、`send(:method_name)` 或在运行期动态给类增加方法。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 ISO C11。
3. **原可观察行为**：运行期动态通过符号查找方法实现并分派。
4. **目标可选写法和不适用条件**：
   - *可选映射*：完全静态化具化为固定函数；若必须支持动态多态，定义包含显式函数指针的虚表结构体（VTable）。
   - *不适用条件*：C 语言为静态编译，严禁在 C 中尝试模拟字符串形式的符号分派。
5. **错误机械替换反例**：
   ```c
   // 错误：在 C 中尝试用字符串比较模拟动态分发，性能低下且无编译检查
   // 正确：使用函数指针表
   typedef struct {
       void (*action)(void* ctx);
   } OperationVTable;
   ```
6. **信息不足或实现相关时的处理**：若源元编程极度复杂，将不可静态化的部分列为未验证阻断项。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

### 规则 RB-C-03：Ruby 异常展开向 C 返回值错误码与 goto cleanup 释放映射
1. **源码触发条件**：Ruby 源码中使用 `raise` 抛出异常并在外层 `rescue`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 ISO C11（[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：异常展开栈帧，执行 `ensure` 块，最后被 `rescue` 捕获。
4. **目标可选写法和不适用条件**：
   - *可选映射*：函数返回整数错误码；在函数末尾定义 `cleanup:` 标签，各失败点通过 `goto cleanup;` 集中释放已分配资源。
   - *不适用条件*：严禁在 C 语言中忽略分配的资源直接提前返回。
5. **错误机械替换反例**：
   ```c
   // 错误：模拟异常提前退出导致资源未释放
   char* buf = malloc(1024);
   if (check() < 0) return -1; // 错误：buf 泄漏！
   free(buf);
   // 正确：goto cleanup 确保释放
   int ret = 0;
   char* buf = malloc(1024);
   if (check() < 0) { ret = -1; goto cleanup; }
   cleanup:
   free(buf);
   return ret;
   ```
6. **信息不足或实现相关时的处理**：记录异常消息传递降级。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

### 规则 RB-C-04：Ruby 任意精度 Integer 的位运算与 pack 定宽编码向 C 定宽整数与显式掩码映射
1. **源码触发条件**：Ruby 源码中对 `Integer` 做位运算或指数运算（如 `perms.map`、`(1 << n)`、`2**k`），或用 `String#unpack('C*')`/`Array#pack('I<')`/`pack('H*')` 做二进制编解码后再作为整数参与运算。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 ISO C11（[WG14-N1570 §6.5 ¶5, §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。具体任务须冻结 `int`/`long` 的实际宽度与 `CHAR_BIT`（由 `<limits.h>`/`<stdint.h>` 与 ABI 决定）。
3. **原可观察行为**：Ruby `Integer` 无溢出概念，超出机器字长自动升级为大数表示，因此 `(1 << 40)`、`2**100` 与任何中间乘积都得到精确值；`pack('I<')`/`unpack('H*')` 按小端/十六进制在字节序列与整数之间转换，字节序与宽度由格式字符显式指定。
4. **目标可选写法和不适用条件**：
   - *可选映射*：先确认源码中该值的真实上界：能落入 64 位的用 `uint64_t`/`int64_t`（`<stdint.h>`），并**显式**用 `& ((UINT64_C(1) << n) - 1U)` 之类的掩码保持位宽；需要保持任意精度的改用已有大数库并把精度上限写进任务前提。逐字节编解码用 `memcpy` + 独立宽度变量（小端用 `uint32_t`、按字节顺序写入 `unsigned char` 数组），十六进制串用 `strtoul`/`strtoull` 或逐位查表换算。
   - *不适用条件*：严禁把 Ruby 的 `1 << n`、`2**k` 或“不会溢出”的中间结果直接落成裸 `int`——32 位或 64 位之外的移位与有符号溢出在 C 中是未定义行为，不是确定的按模截断；严禁把 `pack('I<')`/`unpack('C*')` 的宽度或字节序默默改成平台默认（`'I'`、`'l'` 这类本机宽度的格式与本机字节序不能跨 ABI 复用）。
5. **错误机械替换反例**：
   ```c
   /* 错误：直接照抄 Ruby 的任意精度移位，用裸 int 承载 */
   int shifted = 1 << 40;              /* 错误：移位宽度超出 int，未定义行为；不是按模截断 */
   int total = base * count;           /* 错误：Ruby 不会溢出，C 的有符号溢出是 UB */
   /* 正确：定宽类型 + 显式掩码；先证明上界再选宽度 */
   uint64_t shifted = UINT64_C(1) << 40;
   uint64_t masked  = value & ((UINT64_C(1) << 12) - 1U);
   ```
6. **信息不足或实现相关时的处理**：源码里检索不到该整数的上界（例如数值来自 `datastore`、网络包或另一进程）时，必须停下来标注“上界未定”并询问，不得自行选定 `int`/`long`；也不得假定 `int` 的宽度，宽度以冻结的工具链与 ABI 为准。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[WG14-N1570 §6.2.5, §6.3.1.1, §6.5 ¶5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

### 规则 RB-C-05：Ruby 可变字节串（含编码标签与内嵌 NUL）向 C 指针加长度（memcpy 而非字符串函数）映射
1. **源码触发条件**：Ruby 源码中出现字符串拼接/截取并当作字节流使用，例如 `resp_payload = icmp_id + icmp_seq + contents`、`packet.payload[0, 2]`、`@record_data << data.to_s`、`cookies_msg.split('REMOTE_DEBUGGING|')[1]`，或对网络/文件读回的数据使用 `unpack`/`gsub("\x00", '')`。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)、[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)）；目标语言 ISO C11（[WG14-N1570 §7.1.1, §7.24](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：Ruby `String` 是**可变字节序列加一个 `Encoding` 标签**；长度显式记录，因此内容可以包含 `\0`，`size`/切片/拼接都按该编码的字符语义计算；不同编码拼接失败时抛 `Encoding::CompatibilityError`，而 `ASCII-8BIT`（`BINARY`）串与任何字节互操作。
4. **目标可选写法和不适用条件**：
   - *可选映射*：为每段字节流维护“缓冲区指针 + `size_t` 长度”这对状态：纯字节用 `unsigned char *`/`uint8_t *`，确实以文本使用且按本地编码约定时才用 `char *` 且必须同时传长度；拼接/截取用 `memcpy`（必要时 `realloc` 扩容）；与 C 接口交互需要 NUL 结尾时，额外分配 `len + 1` 并在末尾写 `'\0'`，长度状态不变。
   - *不适用条件*：严禁用 `strlen`/`strcpy`/`strcat`/`strcmp`/`printf("%s")` 处理这类数据——遇到首个 `\0` 即静默截断，或读越界（UB）；严禁把 Ruby 的“编码标签”当成可以丢弃的注释：`Encoding::CompatibilityError` 在 C 中没有任何等价检查，编码不匹配会退化为静默的字节错配。
5. **错误机械替换反例**：
   ```c
   /* 错误：照抄 Ruby 的字节拼接，改用 C 字符串函数 */
   char buf[512];
   strcpy(buf, icmp_id);                 /* 错误：icmp_id 若含 \0 即被截断 */
   strcat(buf, contents);                /* 错误：长度信息丢失，且不检查目标容量 */
   size_t n = strlen(buf);               /* 错误：得到的是“到首个 \0”的长度，不是 Ruby 的 size */
   /* 正确：显式长度 + memcpy；需要 NUL 结尾时单独补 */
   size_t id_len = 2, c_len = contents_len;
   unsigned char *buf = malloc(id_len + c_len + 1);
   memcpy(buf, icmp_id, id_len);
   memcpy(buf + id_len, contents, c_len);
   buf[id_len + c_len] = '\0';
   ```
6. **信息不足或实现相关时的处理**：源码未显式给出该字符串的 `encoding`（来自 `$stdout` 抓取、shell 命令输出、注册表数据等）时，必须标注“编码与是否含 `\0` 待确认”并询问，不得默认 UTF-8 且无内嵌 NUL；目标平台的 `char` 是否为有符号、本地代码页/宽字符约定属于 OS 与 ABI 范畴，须另读系统场景 Skill。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-STRING](https://docs.ruby-lang.org/en/3.4/String.html)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[WG14-N1570 §7.1.1, §7.24](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

### 规则 RB-C-06：Ruby 隐式代码块（&:sym / &blk）向 C 函数指针 + 上下文结构体映射
1. **源码触发条件**：Ruby 源码把块对象本身当数据传递或转发，例如 `a.map(&:join)`、`keys.each { |k| ... }` 被抽成方法后再调用、`datastore['FILE_GLOBS'].split(',').each do |glob| ... end` 这类需要在转换后被复用/延迟执行的迭代体，以及 `rescue => e ... raise e` 之外把过程对象存进容器再调用的写法。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-PROC](https://docs.ruby-lang.org/en/3.4/Proc.html)）；目标语言 ISO C11（[WG14-N1570 §6.7.6.3, §6.5.2.2](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：块是携带**词法环境**的可调用对象；`&:join` 是对每个元素调用该方法的简写；`break`/`next`/`return` 在块内的含义由调用方决定（`break` 从调用方法返回、`next` 跳到下一次迭代），异常也会穿过块边界向外传播。
4. **目标可选写法和不适用条件**：
   - *可选映射*：把“块 + 捕获环境”这一对显式物化为 `struct { void (*fn)(void *ctx, item_t item); void *ctx; }`；被捕获的局部变量放进 `ctx` 指向的结构体（堆分配时明确归属谁释放），回调以 `ctx` 作为首参；循环变量由调用方逐个传入，不用全局变量代替。
   - *不适用条件*：严禁把块机械替换成无 `ctx` 参数的裸函数指针或文件级 `static` 变量——前者丢失捕获状态，后者在重入或多次调用时被覆盖，语义与 Ruby 的每次调用独立环境不同；C 无闭包，`&:sym` 也不能翻译成“按名字查表调用”而不给出显式分派表。
5. **错误机械替换反例**：
   ```c
   /* 错误：把块改成无上下文的函数指针，用文件级 static 顶替捕获环境 */
   static int g_item;                                  /* 错误：Ruby 每次调用的块环境是独立的 */
   static void join_cb(void) { printf("%d\n", g_item); }/* 错误：签名不接收元素，无法逐个迭代 */
   /* 正确：函数指针 + 显式上下文结构体 */
   typedef struct { int *items; size_t n; } join_ctx_t;
   static void join_cb(void *ctx, int item) { (void)ctx; printf("%d\n", item); }
   static void each_int(int *items, size_t n, void (*fn)(void *, int), void *ctx) {
       for (size_t i = 0; i < n; ++i) fn(ctx, items[i]);
   }
   ```
6. **信息不足或实现相关时的处理**：块内出现 `break`/`next`/`return`、或块被存入容器后在别的函数里调用（生命周期跨出定义作用域）时，必须标注该控制流与存活期未确定并询问；块捕获了 `self` 或调用方实例变量时，需先确认这些状态在 C 侧由谁持有。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-PROC](https://docs.ruby-lang.org/en/3.4/Proc.html)；[WG14-N1570 §6.7.6.3, §6.5.2.2](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
