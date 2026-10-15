---
name: python-to-c
description: Use when converting Python source to C; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → C 语言转换规则

> **适用基线**：CPython 3.12 → ISO C11。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 Python](../../references/languages/python.md)与[目标语言 C](../../references/languages/c.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 Python → C 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PY-C-01：Python 动态鸭子类型向 C 静态强类型与标量/联合体具化映射
1. **源码触发条件**：Python 源码中变量动态赋值不同类型（如先赋数字后赋字典），或函数接受异构参数。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（PY-REF-DATA）；目标语言 ISO C11（WG14-N1570 §6.2.5）。
3. **原可观察行为**：Python 变量纯粹是指向堆对象的指针，动态分派方法。
4. **目标可选写法和不适用条件**：
   - *可选映射*：推导变量的真实业务类型，具化为 C 静态类型；若必须支持有限几种变体，定义带类型标签的结构体（Tagged Union）。
   - *不适用条件*：严禁在 C 中滥用 `void*` 绕过类型系统，极易触犯 C11 严格别名规则（Strict Aliasing UB）。
5. **错误机械替换反例**：
   ```c
   // 错误：使用 void* 相互强转并解引用，触犯严格别名规则引发未定义行为
   void* ptr = &my_float;
   int val = *(int*)ptr; // UB！
   // 正确：使用带类型标签的联合体
   typedef struct {
       enum { TYPE_INT, TYPE_FLOAT } type;
       union { int i; float f; } data;
   } Variant;
   ```
6. **信息不足或实现相关时的处理**：若动态类型在源码中无法静态推导，向用户报告阻断并请求类型标注。
7. **资料依据（名称/版本/章节）**：WG14-N1570 §6.5 ¶7；PY-REF-DATA。

### 规则 PY-C-02：Python 异构容器与负索引向 C 定长数组与显式长度换算映射
1. **源码触发条件**：Python 源码中使用 `list[-1]` 访问末尾元素，或使用 `list.append()` 动态追加。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12；目标语言 ISO C11。
3. **原可观察行为**：负索引自动加上容器长度访问元素；超出范围抛出 `IndexError`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 C 语言数组与长度变量，访问前手动换算下标：`int real_idx = idx < 0 ? len + idx : idx;`，并严格执行 `real_idx >= 0 && real_idx < len` 边界检查。
   - *不适用条件*：严禁在 C 语言中直接传入负数下标（如 `arr[-1]` 会直接越界访问数组头部之前的非法内存导致内存崩溃）。
5. **错误机械替换反例**：
   ```c
   // 错误：直接在 C 数组中使用负数索引
   // Python: return arr[-1]
   int get_last(const int* arr, size_t len) {
       return arr[-1]; // 严重错误：向前越界解引用非法内存！
   }
   // 正确：显式换算并校验
   int get_last(const int* arr, size_t len, int* out_val) {
       if (len == 0) return -1;
       *out_val = arr[len - 1];
       return 0;
   }
   ```
6. **信息不足或实现相关时的处理**：若容器大小动态变化，实现带 `capacity` 和 `size` 的动态数组结构体。
7. **资料依据（名称/版本/章节）**：WG14-N1570 §6.5.2.1；PY-REF-DATA §3.2。

### 规则 PY-C-03：Python 任意精度 int 向 C 定宽整数防截断失真映射
1. **源码触发条件**：Python 源码中使用大整数进行乘方、大素数或密集移位计算。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（PY-REF-DATA §3.2）；目标语言 ISO C11（WG14-N1570 §6.2.5）。
3. **原可观察行为**：Python 自动扩展位宽，永不发生算术截断溢出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：确认数值范围在 64 位内时，选用 `int64_t` 或 `uint64_t`；若确认属于密码学大整数，必须在报告中声明依赖第三方大数库（如 GMP）或重构算法。
   - *不适用条件*：严禁直接将 Python 大整数运算机械套用 C `int`，静默截断会导致计算逻辑全盘失真。
5. **错误机械替换反例**：
   ```c
   // 错误：Python 中的 1 << 40 在 C 32位系统下直接溢出未定义或截断为 0
   // Python: x = 1 << 40
   int64_t x = 1 << 40; // 错误：字面量 1 为 32 位 int，左移 40 位属未定义行为！
   // 正确：显式指定 64 位字面量
   int64_t x = ((int64_t)1) << 40;
   ```
6. **信息不足或实现相关时的处理**：若无法确认数值是否超过 64 位，向用户标记潜在溢出截断风险。
7. **资料依据（名称/版本/章节）**：WG14-N1570 §6.5.7；PY-REF-DATA §3.2。

---

### 规则 PY-C-04：Python 列表推导式与生成器表达式向 C 显式循环映射

1. **源码触发条件**：Python 源码中使用列表推导式（`[x*2 for x in items if x > 0]`）或生成器表达式（`(x*2 for x in items)`）。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（PY-REF-DATA）；目标语言 ISO C11。
3. **原可观察行为**：列表推导式立即求值；生成器表达式按后续迭代惰性求值，但最左 for 的可迭代表达式在定义时立即求值。保留求值次数/时机、部分消费、异常发生点、闭包状态和资源生命周期。
4. **目标可选写法和不适用条件**：
   - *可选映射*：列表推导式可用显式循环及有依据的容量；生成器由配置模型生成保持迭代位置与上下文的 C 目标状态机。只有已证明有限输入、求值副作用/异常时机/共享状态与部分消费均无可观察变化，或用户明确允许该差异时，才考虑预计算。
   - *不适用条件*：有副作用、外部可变状态、部分消费、可能无限输入或依赖惰性错误/清理时机时，不改为一次性数组；不使用一个共享静态状态冒充各生成器实例。C 无内建生成器不代表可以删除惰性契约。
5. **错误机械替换反例**：
   ```c
   // 错误：将列表推导式转为固定大小数组，未计算过滤后实际元素数量导致数组越界或浪费
   // Python: result = [x*2 for x in items if x > 0]
   int result[100]; // 错误：硬编码大小，若 items 长度或过滤结果数量不匹配则失败
   int count = 0;
   for (size_t i = 0; i < items_len; i++) {
       if (items[i] > 0) {
           result[count++] = items[i] * 2; // 未检查 count < 100，潜在越界！
       }
   }
   ```
6. **信息不足或实现相关时的处理**：若生成器表达式涉及复杂的嵌套作用域捕获或依赖外部可变状态，必须设计显式上下文结构体并说明状态生命周期。
7. **资料依据（名称/版本/章节）**：Python 3.12 Language Reference §6.2.4 Displays、§6.2.8 Generator expressions（最左迭代表达式与后续惰性求值）；C11 N1570 §6.5.2.1。

---

### 规则 PY-C-05：Python `with` 上下文管理器向 C 显式资源获取释放模式映射

1. **源码触发条件**：Python 源码中使用 `with open(...) as f:` 或自定义 `__enter__` / `__exit__` 的上下文管理器。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（PY-REF-CTX）；目标语言 ISO C11。
3. **原可观察行为**：进入 `with` 块时调用 `__enter__`，退出块（无论正常返回还是异常）时确定性调用 `__exit__` 清理资源。
4. **目标可选写法和不适用条件**：
   - *可选映射*：展开为 C 显式的资源获取、使用、释放模式；使用 `goto cleanup` 标签确保所有退出路径均执行清理；若涉及文件，映射为 `fopen` / `fclose`；若涉及锁，映射为 `lock` / `unlock`；
   - *不适用条件*：严禁遗漏任何提前返回分支的清理代码；严禁在 C 中依赖析构函数或自动清理（C 无此机制）。
5. **错误机械替换反例**：
   ```c
   // 错误：提前返回分支遗漏资源释放，导致文件句柄泄漏
   // Python: with open(path, 'r') as f: data = f.read(); if not valid(data): return -1
   int process_file(const char* path) {
       FILE* f = fopen(path, "r");
       if (!f) return -1;
       char data[1024];
       fread(data, 1, sizeof(data), f);
       if (!valid(data)) {
           return -1; // 错误：未调用 fclose(f)，句柄泄漏！
       }
       fclose(f);
       return 0;
   }
   // 正确：使用 goto cleanup 统一清理
   int process_file(const char* path) {
       FILE* f = fopen(path, "r");
       if (!f) return -1;
       int ret = 0;
       char data[1024];
       fread(data, 1, sizeof(data), f);
       if (!valid(data)) {
           ret = -1;
           goto cleanup;
       }
   cleanup:
       fclose(f);
       return ret;
   }
   ```
6. **信息不足或实现相关时的处理**：若 Python `__exit__` 方法包含异常抑制逻辑（返回 `True` 抑制异常），在 C 中必须使用特定错误码表示该语义，并在文档中说明。
7. **资料依据（名称/版本/章节）**：PY-REF-CTX；WG14-N1570 §7.21.5。

---

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。

## 网络 API 映射

仅在 Python socket 到 C 实现时使用。bytes 可含 NUL，C 始终传显式长度，不用 strlen。独立 C 目标用实际 socket 返回值/平台错误重建 Python 的异常路径，不能照抄带 try/catch 的 C++ 伪代码，也不引入 Python 运行时。仅在任务明确保留 CPython 扩展/嵌入时才另核 C API、GIL 与阻塞调用规则；缺对应版本的本地必要事实时记录缺口，不把释放 GIL 包在任意 Python API 调用外。通用部分 I/O 读[网络场景](../../scenes/network-io/SKILL.md)，平台错误读[系统页](../../systems/posix-winsock/SKILL.md)。
