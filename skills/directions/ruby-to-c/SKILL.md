---
name: ruby-to-c
description: Use when converting Ruby source to C; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → C 语言转换规则

> **适用基线**：CRuby 3.4 → ISO C11。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Ruby](../../references/languages/ruby.md)与[目标语言 C](../../references/languages/c.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/ruby-to-c/README.md)；候选、冻结任务与第三方回传须分层记录。
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

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
