---
name: python-to-c
description: Use when converting Python source to C; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Python → C 语言转换规则

> **适用基线**：CPython 3.12 → ISO C11。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Python](../../references/languages/python.md)与[目标语言 C](../../references/languages/c.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/python-to-c/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Python → C 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PY-C-01：Python 动态鸭子类型向 C 静态强类型与标量/联合体具化映射
1. **源码触发条件**：Python 源码中变量动态赋值不同类型（如先赋数字后赋字典），或函数接受异构参数。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 ISO C11（[WG14-N1570 §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
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
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.5 ¶7](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

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
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.5.2.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 PY-C-03：Python 任意精度 int 向 C 定宽整数防截断失真映射
1. **源码触发条件**：Python 源码中使用大整数进行乘方、大素数或密集移位计算。
2. **冻结版本/运行时/API 前提**：源语言 CPython 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）；目标语言 ISO C11（[WG14-N1570 §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
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
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.5.7](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
