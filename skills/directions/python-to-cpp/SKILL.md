---
name: python-to-cpp
description: Use when converting Python source to C++; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → C++ 语言转换规则

> **适用基线**：CPython 3.12 → ISO C++17。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 Python](../../references/languages/python.md)与[目标语言 C++](../../references/languages/cpp.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 Python → C++ 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PY-CPP-01：Python 生成器 (yield) 向 C++17 状态机迭代器类重构映射
1. **源码触发条件**：Python 源码中包含 `def gen(): yield x` 生成器函数。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（PY-REF-YIELD）；目标语言 ISO C++17（WG21-N4659 Clause 27）。
3. **原可观察行为**：调用生成器返回迭代器对象，通过 `next()` 逐步执行并在退出时触发清理。
4. **目标可选写法和不适用条件**：
   - *可选映射*：C++17 状态机/迭代器候选须保持每次推进、局部状态、停止/关闭、异常与清理时点。仅源码已完整消费且提前生成的副作用、异常和内存行为不可观察时才考虑一次性 vector；不能因目标没有 generator 就自动物化。
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
6. **信息不足或实现相关时的处理**：源使用gen.throw等双向异常/恢复路径时，定位消费者和生成器内部捕获/清理，核状态机是否能保持；契约未知则停止受影响映射，记缺口。不以“声明降级”允许删除异常传递，采用不同语义须有生成前许可。
7. **资料依据（名称/版本/章节）**：PY-REF-YIELD；WG21-N4659 Clause 27。

### 规则 PY-CPP-02：Python 函数返回 None 作为可选值向 C++17 std::optional 映射
1. **源码触发条件**：Python 源码中函数在查找到数据时返回对象，未查找到时返回 `None`。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 ISO C++17（WG21-N4659 Clause 23.6）。
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
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 23.6。

### 规则 PY-CPP-03：Python with 上下文管理器向 C++17 RAII 作用域析构映射
1. **源码触发条件**：Python 源码中使用 `with lock:` 或 `with open(...) as f:` 管理作用域生命周期。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 ISO C++17（WG21-N4659 Clause 6.7）。
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
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 6.7。

### 规则 PY-CPP-04：Python struct 格式与任意精度 int 向 C++17 定宽整数与显式字节序映射
1. **源码触发条件**：Python 源码用 `struct.unpack('<i', f.read(4))[0]`、`struct.unpack('!B', ...)`、`struct.pack("<I", value)` 读取或写入定宽字段，或在二进制偏移计算中使用可能超出 64 位的整数。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（PY-LIB-STRUCT）；目标语言 ISO C++17（WG21-N4659 Clause 6.9.1, Clause 24.3）。
3. **原可观察行为**：`struct` 格式字符锁定"宽度 + 字节序"：`<i` 为 4 字节小端有符号、`<H` 为 2 字节小端无符号、`!` 为网络序；`pack` 写入超出该格式表示范围的值抛 `struct.error`；解包结果是 Python 任意精度 `int`，不会溢出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：按格式宽度/符号/端序、输入完整长度及源失败边界选表示，显式逐字节组合/输出；memcpy 仅复制表示，不能转换端序。pack 超范围须保失败，只有源已有掩码/截断时才做相同截断；解包后的算术仍可能需任意精度，不能因字段定宽就截断所有中间值。
   - *不适用条件*：严禁用 `int`/`long`/`unsigned` 代替格式字符对应的宽度（C++ 标准不保证 `int` 为 32 位，宽度由实现裁定）；严禁用 `(int32_t*)ptr` 或类型双关从字节缓冲直接取值（对齐与严格别名约束下是未定义行为，须 `std::memcpy`）；严禁把有符号字段按无符号重组或反之（负值位模式被重新解释）。
5. **错误机械替换反例**：
   ```cpp
   // Python 原型：flItms['MachineType'] = struct.unpack('<H', binary.read(2))[0]
   int machine_type;                              // 错误：宽度不保证是 16 位
   std::memcpy(&machine_type, buf + off, 2);      // 错误：小端缓冲区被按宿主字节序解释
   // 条件示意：已按源 unpack 的失败边界核输入至少两个 uint8_t 字节
   const std::uint16_t machine_type = static_cast<std::uint16_t>(buf[off])
       | (static_cast<std::uint16_t>(buf[off + 1]) << 8);
   // Python 原型：f.write(struct.pack("<I", len(cert)))
   // 错误候选：直接 uint32_t(cert.size()) 截断会丢源 struct.error；先按 <I 范围核并保失败。
   ```
6. **信息不足或实现相关时的处理**：若源字段宽度来自运行期读取（例如按 `Magic` 值选择 4 字节或 8 字节分支），必须保留该分支结构而不能先固定宽度；字节序、目标平台 `int` 宽度或是否需要大数语义未冻结时标注为待确认。
7. **资料依据（名称/版本/章节）**：PY-LIB-STRUCT；WG21-N4659 Clause 24.3。

### 规则 PY-CPP-05：Python 负索引与裁剪切片向 C++17 显式边界检查映射
1. **源码触发条件**：Python 源码使用 `lst[-1]`、`buf[-n:]`、`seq[a:b]`、`f.seek(-size, io.SEEK_END)` 或 `sys.exit(-1)` 这类负值/裁剪式访问。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（PY-REF-SUBSCRIPTIONS）；目标语言 ISO C++17（WG21-N4659 Clause 26.3）。
3. **原可观察行为**：Python 负索引等价于 `len + i`；切片超界被静默裁剪（`b > len` 取到末尾，负边界从末尾折算），不抛异常；`seek` 的负偏移是相对文件末尾的有符号偏移；进程退出码语义受平台约束（POSIX 只有低 8 位可观察）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：步长为 1 的切片先将负边界按长度换算，再分别裁剪到 `[0, len]`，起点不小于终点时返回空结果；不得用超界报错代替源裁剪。单项负索引另行换算并保留越界失败，不能与切片混用。文件定位用 `tellg()/seekg()` 配合有符号 `std::streamoff`；外部任意精度边界还需先安全归一化再收窄。
   - *不适用条件*：严禁把负下标直接传给 `operator[]`（`size_t` 转换后成为极大正数，越界访问属未定义行为，比源语言的取末尾元素语义完全不同）；严禁用 `operator[]` 代替 Python 的边界检查语义（`std::vector::operator[]` 不做检查）；严禁假定"切片越界会被裁剪"（C++ 侧必须自己裁剪或改用迭代器区间）。
5. **错误机械替换反例**：
   ```cpp
   // Python 原型：cert = data[-2:]                       // 取末尾两个字节
   std::vector<std::uint8_t> cert(data[-2], data[-1]);    // 错误：负下标 -> size_t 极大值，UB
   // 保留 data[-2:] 的裁剪：不足两个元素时取全部
   std::vector<std::uint8_t> cert;
   const auto count = std::min<std::size_t>(2, data.size());
   cert.assign(data.end() - count, data.end());
   // Python 原型：f.seek(-flItms['CertSize'], io.SEEK_END)
   f.seekg(-static_cast<std::streamoff>(cert_size), std::ios::end); // 正确：有符号偏移 + 末尾基准
   ```
6. **信息不足或实现相关时的处理**：若源切片的边界依赖运行期数据且源码未做宽度假设，须把"哪个变量可能为负、哪个切片可能超界"逐条列出；进程退出码需要跨平台一致时先冻结平台与退出码宽度语义。
7. **资料依据（名称/版本/章节）**：PY-REF-SUBSCRIPTIONS；WG21-N4659 Clause 26.3。

### 规则 PY-CPP-06：Python 异常层次向 C++17 异常类型与 RAII 清理映射
1. **源码触发条件**：Python 源码使用 `try`/`except` 分派不同失败（`except KeyError`、`except IndexError`、`except OSError`、`except ValueError`、`except Exception`），并在 `finally` 中执行文件关闭或缓冲清理。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（PY-REF-EXCEPT）；目标语言 ISO C++17（WG21-N4659 Clause 18, Clause 15.4）。
3. **原可观察行为**：Python 按异常类层次匹配 `except` 子句，`finally` 在所有出口执行；异常对象携带消息与回溯，未被捕获时解释器打印回溯并设置退出码。C++ 异常沿栈逆序析构已构造对象，未捕获异常调用 `std::terminate()`；C++ 没有 `finally` 语句。
4. **目标可选写法和不适用条件**：
   - *可选映射*：只有源不区分类型/字段/身份时才合并到标准异常；源分别捕获 KeyError 与 IndexError 时不能都改 out_of_range 后丢区分。finally 的动作、覆盖原异常/返回值与失败传播须显式对应；默认 noexcept 析构不能代会抛错的清理。RAII 仅其退出点与无新增失败条件一致时适用。
   - *不适用条件*：严禁让异常跨越 C ABI 边界（以 C 调用约定导出的函数或回调中抛出的异常必须就地 `catch (...)` 并转成错误码）；严禁用 `std::terminate` 或 `abort()` 模拟 Python 未捕获异常的输出行为而不核对退出码与诊断信息；严禁在 `catch` 中先吞掉异常再返回默认值（失败路径拓扑被改变）。
5. **错误机械替换反例**：
   ```cpp
   // Python 原型：try: parse(buf) except KeyError: ... finally: f.close()
   // 错误：手工 fclose 无法在 parse 抛出异常时执行
   FILE* f = std::fopen(path, "rb");
   parse(buf);                 // 抛出 std::out_of_range -> f 永不关闭
   std::fclose(f);
   // 条件候选：仅文件关闭失败不被源观察/传播且退出作用域一致时适用
   std::ifstream f(path, std::ios::binary);
   if (!f) { throw std::runtime_error("open failed"); }
   parse(buf);                 // 异常向上传播，f 的析构函数保证关闭
   ```
6. **信息不足或实现相关时的处理**：若该函数会被 C 代码或回调调用（ABI 边界不明确），先把调用方语言与调用约定标为待确认；若 Python 侧依赖异常消息文本做分支，需说明 C++ 侧无同构消息契约。
7. **资料依据（名称/版本/章节）**：PY-REF-EXCEPT；WG21-N4659 Clause 18。

### Unicode 及头文件消费点

源使用 unicodedata.normalize/casefold 时，读 [Python L1-PY-16](../../references/languages/python.md#l1-py-16-unicode-规范化折叠与文本长度分别保持) 与 [C++ L1-CPP-07](../../references/languages/cpp.md#l1-cpp-07-文本容器与-locale-不等于-unicode-规范化)，分别对应规范化形式、键／长度消费者与离线依赖。容器换成 u32string 不自动提供规范化，子集表须按明确交付范围报告。

引入 zlib 等头文件后，宏替换可影响看似位于命名空间内的常量；按[构建前提](../../../references/workflow/build-prerequisites.md) §2.1 及真实诊断记录必要局部改名，不能以删分支或改常量值解决冲突。构建失败与库可用性／业务等价分别报告。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
