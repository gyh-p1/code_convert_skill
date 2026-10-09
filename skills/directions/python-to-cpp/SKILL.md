---
name: python-to-cpp
description: Use when converting Python source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → C++ 语言转换规则

> **适用基线**：CPython 3.12 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Python](../../references/languages/python.md)与[目标语言 C++](../../references/languages/cpp.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Python → C++ 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PY-CPP-01：Python 生成器 (yield) 向 C++17 状态机迭代器类重构映射
1. **源码触发条件**：Python 源码中包含 `def gen(): yield x` 生成器函数。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 27](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：调用生成器返回迭代器对象，通过 `next()` 逐步执行并在退出时触发清理。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C++17 中手动编写一个包含状态枚举、局部变量和 `next()` 或满足迭代器协议 `operator++`/`operator*` 的类；或者重构为一次性批量生成 `std::vector`。
   - *不适用条件*：严禁使用 C++20 协程关键字（`co_yield`, `co_return`），超出 C++17 冻结基线。
5. **错误机械替换反例**：
   ```cpp
   // 错误：在 C++17 基线中违规引入 C++20 协程
   // std::generator<int> MyGen() { co_yield 1; } // 编译报错：C++17 不支持协程
   // 正确：手动实现状态机类
   class MyGen {
       int state = 0;
       int current_val;
   public:
       bool next(int& val) {
           if (state == 0) { current_val = 1; state = 1; val = current_val; return true; }
           return false;
       }
   };
   ```
6. **信息不足或实现相关时的处理**：若生成器包含复杂的异常双向传递（`gen.throw()`），必须在报告中声明该复杂控制流降级。
7. **直接官方 HTTPS 依据链接**：[PY-REF-YIELD](https://docs.python.org/3.12/reference/expressions.html)；[WG21-N4659 Clause 27](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PY-CPP-02：Python 函数返回 None 作为可选值向 C++17 std::optional 映射
1. **源码触发条件**：Python 源码中函数在查找到数据时返回对象，未查找到时返回 `None`。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 ISO C++17（[WG21-N4659 Clause 23.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：调用方使用 `if res is None` 判定缺失。
4. **目标可选写法和不适用条件**：
   - *可选映射*：方法返回值定义为 `std::optional<T>`；缺失时返回 `std::nullopt`；调用点使用 `has_value()` 或布尔上下文检查。
   - *不适用条件*：严禁机械转换为返回裸指针 `T*` 并返回 `nullptr`（会导致所有权归属混淆及悬垂指针风险）；严禁使用 C++23 的 `std::expected`。
5. **错误机械替换反例**：
   ```cpp
   // 错误：将值对象返回转换为裸指针并返回 nullptr，造成内存泄漏或解引用崩溃
   Item* FindItem(int id) {
       if (id <= 0) return nullptr; // 谁负责释放返回的 Item*？
       return new Item(id); // 泄漏！
   }
   // 正确：使用 std::optional
   std::optional<Item> FindItem(int id) {
       if (id <= 0) return std::nullopt;
       return Item(id);
   }
   ```
6. **信息不足或实现相关时的处理**：若需要表达具体错误原因而不只是简单缺失，使用自定义 Result 结构体。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 23.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PY-CPP-03：Python with 上下文管理器向 C++17 RAII 作用域析构映射
1. **源码触发条件**：Python 源码中使用 `with lock:` 或 `with open(...) as f:` 管理作用域生命周期。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 ISO C++17（[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：离开代码块时触发 `__exit__`，无论是否抛出异常均保证清理。
4. **目标可选写法和不适用条件**：
   - *可选映射*：互斥锁使用 `std::lock_guard` 或 `std::unique_lock`；文件使用 `std::ifstream`/`std::ofstream` 栈对象。
   - *不适用条件*：严禁在 C++ 中手动编写 `lock.unlock()` 并在中间留下未经保护的异常抛出点。
5. **错误机械替换反例**：
   ```cpp
   // 错误：手动管理锁，遇到异常跳过解锁
   std::mutex mtx;
   void Action() {
       mtx.lock();
       DoWork(); // 抛出异常！
       mtx.unlock(); // 永远不执行，死锁！
   }
   // 正确：RAII 守卫
   void Action() {
       std::lock_guard<std::mutex> lock(mtx);
       DoWork();
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及文件 I/O，加载 [`skills/scenes/file-io/SKILL.md`](../../scenes/file-io/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 6.7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PY-CPP-04：Python struct 格式与任意精度 int 向 C++17 定宽整数与显式字节序映射
1. **源码触发条件**：Python 源码用 `struct.unpack('<i', f.read(4))[0]`、`struct.unpack('!B', ...)`、`struct.pack("<I", value)` 读取或写入定宽字段，或在二进制偏移计算中使用可能超出 64 位的整数。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-LIB-STRUCT](https://docs.python.org/3.12/library/struct.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 6.9.1, Clause 24.3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：`struct` 格式字符锁定"宽度 + 字节序"：`<i` 为 4 字节小端有符号、`<H` 为 2 字节小端无符号、`!` 为网络序；`pack` 写入超出该格式表示范围的值抛 `struct.error`；解包结果是 Python 任意精度 `int`，不会溢出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按格式字符选定宽类型（`<i`→`std::int32_t`，`<H`→`std::uint16_t`，`<Q`→`std::uint64_t`，`!B`→`std::uint8_t`），读取与写回统一用定宽类型配合 `std::memcpy`，字节序按格式字符**显式重组**（小端用 `std::uint32_t` 逐字节移位累加后 `static_cast`，不使用依赖宿主的类型双关），无符号写回再施加宽度掩码；确实需要任意精度时声明改用大数库。
   - *不适用条件*：严禁用 `int`/`long`/`unsigned` 代替格式字符对应的宽度（C++ 标准不保证 `int` 为 32 位，宽度由实现裁定）；严禁用 `(int32_t*)ptr` 或类型双关从字节缓冲直接取值（对齐与严格别名约束下是未定义行为，须 `std::memcpy`）；严禁把有符号字段按无符号重组或反之（负值位模式被重新解释）。
5. **错误机械替换反例**：
   ```cpp
   // Python 原型：flItms['MachineType'] = struct.unpack('<H', binary.read(2))[0]
   int machine_type;                              // 错误：宽度不保证是 16 位
   std::memcpy(&machine_type, buf + off, 2);      // 错误：小端缓冲区被按宿主字节序解释
   // 正确：定宽 + 复制字节 + 显式按小端重组
   std::uint16_t raw16 = 0;
   std::memcpy(&raw16, buf + off, sizeof(raw16));
   const std::uint16_t machine_type = static_cast<std::uint16_t>(raw16); // 需小端时逐字节重组
   // Python 原型：f.write(struct.pack("<I", len(cert)))
   const std::uint32_t cert_len = static_cast<std::uint32_t>(cert.size()); // 超范围时静默截断
   ```
6. **信息不足或实现相关时的处理**：若源字段宽度来自运行期读取（例如按 `Magic` 值选择 4 字节或 8 字节分支），必须保留该分支结构而不能先固定宽度；字节序、目标平台 `int` 宽度或是否需要大数语义未冻结时标注为待确认。
7. **直接官方 HTTPS 依据链接**：[PY-LIB-STRUCT](https://docs.python.org/3.12/library/struct.html)；[WG21-N4659 Clause 24.3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PY-CPP-05：Python 负索引与裁剪切片向 C++17 显式边界检查映射
1. **源码触发条件**：Python 源码使用 `lst[-1]`、`buf[-n:]`、`seq[a:b]`、`f.seek(-size, io.SEEK_END)` 或 `sys.exit(-1)` 这类负值/裁剪式访问。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-SUBSCRIPTIONS](https://docs.python.org/3.12/reference/expressions.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 26.3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：Python 负索引等价于 `len + i`；切片超界被静默裁剪（`b > len` 取到末尾，负边界从末尾折算），不抛异常；`seek` 的负偏移是相对文件末尾的有符号偏移；进程退出码语义受平台约束（POSIX 只有低 8 位可观察）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：切片改写为 `start`/`count` 两个显式变量并先做 `start >= 0 && count >= 0 && start + count <= v.size()` 校验；负索引先换算（`i += static_cast<std::ptrdiff_t>(v.size())`）再校验 `i >= 0`；越界访问使用 `v.at(i)` 以保留"抛异常"的可观察失败；文件定位用 `tellg()/seekg()` 配合有符号 `std::streamoff`。
   - *不适用条件*：严禁把负下标直接传给 `operator[]`（`size_t` 转换后成为极大正数，越界访问属未定义行为，比源语言的取末尾元素语义完全不同）；严禁用 `operator[]` 代替 Python 的边界检查语义（`std::vector::operator[]` 不做检查）；严禁假定"切片越界会被裁剪"（C++ 侧必须自己裁剪或改用迭代器区间）。
5. **错误机械替换反例**：
   ```cpp
   // Python 原型：cert = data[-2:]                       // 取末尾两个字节
   std::vector<std::uint8_t> cert(data[-2], data[-1]);    // 错误：负下标 -> size_t 极大值，UB
   // 正确：显式换算并校验
   std::vector<std::uint8_t> cert;
   if (data.size() >= 2) {
       cert.assign(data.end() - 2, data.end());
   }
   // Python 原型：f.seek(-flItms['CertSize'], io.SEEK_END)
   f.seekg(-static_cast<std::streamoff>(cert_size), std::ios::end); // 正确：有符号偏移 + 末尾基准
   ```
6. **信息不足或实现相关时的处理**：若源切片的边界依赖运行期数据且源码未做宽度假设，须把"哪个变量可能为负、哪个切片可能超界"逐条列出；进程退出码需要跨平台一致时先冻结平台与退出码宽度语义。
7. **直接官方 HTTPS 依据链接**：[PY-REF-SUBSCRIPTIONS](https://docs.python.org/3.12/reference/expressions.html)；[WG21-N4659 Clause 26.3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### 规则 PY-CPP-06：Python 异常层次向 C++17 异常类型与 RAII 清理映射
1. **源码触发条件**：Python 源码使用 `try`/`except` 分派不同失败（`except KeyError`、`except IndexError`、`except OSError`、`except ValueError`、`except Exception`），并在 `finally` 中执行文件关闭或缓冲清理。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-EXCEPT](https://docs.python.org/3.12/reference/executionmodel.html)）；目标语言 ISO C++17（[WG21-N4659 Clause 18, Clause 15.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：Python 按异常类层次匹配 `except` 子句，`finally` 在所有出口执行；异常对象携带消息与回溯，未被捕获时解释器打印回溯并设置退出码。C++ 异常沿栈逆序析构已构造对象，未捕获异常调用 `std::terminate()`；C++ 没有 `finally` 语句。
4. **目标可选写法和不适用条件**：
   - *可选映射*：失败类型映射到标准异常类（缺键/越界→`std::out_of_range`，非法取值→`std::invalid_argument`，运行期失败→`std::runtime_error`，内存不足→`std::bad_alloc`），并按"派生类在前"的 `catch` 顺序排列；`finally` 清理改写为 RAII 包装（`std::ifstream`/`std::lock_guard`/自定义析构函数），需要 `catch` 后重抛时用裸 `throw;`。
   - *不适用条件*：严禁让异常跨越 C ABI 边界（以 C 调用约定导出的函数或回调中抛出的异常必须就地 `catch (...)` 并转成错误码）；严禁用 `std::terminate` 或 `abort()` 模拟 Python 未捕获异常的输出行为而不核对退出码与诊断信息；严禁在 `catch` 中先吞掉异常再返回默认值（失败路径拓扑被改变）。
5. **错误机械替换反例**：
   ```cpp
   // Python 原型：try: parse(buf) except KeyError: ... finally: f.close()
   // 错误：手工 fclose 无法在 parse 抛出异常时执行
   FILE* f = std::fopen(path, "rb");
   parse(buf);                 // 抛出 std::out_of_range -> f 永不关闭
   std::fclose(f);
   // 正确：RAII 负责清理，异常只在本编译单元内传播
   std::ifstream f(path, std::ios::binary);
   if (!f) { throw std::runtime_error("open failed"); }
   parse(buf);                 // 异常向上传播，f 的析构函数保证关闭
   ```
6. **信息不足或实现相关时的处理**：若该函数会被 C 代码或回调调用（ABI 边界不明确），先把调用方语言与调用约定标为待确认；若 Python 侧依赖异常消息文本做分支，需说明 C++ 侧无同构消息契约。
7. **直接官方 HTTPS 依据链接**：[PY-REF-EXCEPT](https://docs.python.org/3.12/reference/executionmodel.html)；[WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
