---
name: powershell-to-c
description: Use when converting PowerShell source to C; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → C 语言转换规则

> **适用基线**：PowerShell 7.6 → ISO C11。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 PowerShell](../../references/languages/powershell.md)与[目标语言 C](../../references/languages/c.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/powershell-to-c/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 PowerShell → C 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PS-C-01：PowerShell 动态对象管道向 C 底层字节流与固定结构体降级映射
1. **源码触发条件**：PowerShell 源码中通过管道传递具备属性的对象（如 `Get-Process | Select-Object Id, ProcessName`）。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 ISO C11（[WG14-N1570 §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：传递强类型 .NET PSObject 包装对象，下游通过属性名直接提取字段。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C 中定义明确的 `struct` 结构体，字段定宽且强类型化；管道传递转换为结构体指针数组或线性缓冲区循环处理。
   - *不适用条件*：严禁在 C 中尝试模拟动态属性反射字典，维护开销极大且容易内存泄漏。
5. **错误机械替换反例**：
   ```c
   // 错误：在 C 中使用字符串名值对链表模拟 PSObject，内存开销暴增且极易泄漏
   // 正确：定义具体的 C 结构体
   typedef struct {
       int32_t id;
       char name[64];
   } ProcessInfo;
   ```
6. **信息不足或实现相关时的处理**：若源对象属性动态不固定，提取所需字段子集并向用户确认。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)；[WG14-N1570 §6.2.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

### 规则 PS-C-02：PowerShell 弱类型隐式转换向 C 严格显式转换与溢出防范映射
1. **源码触发条件**：PowerShell 源码中将字符串数字与整数直接混算（如 `'100' + 20` 或 `20 + '100'`）。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6；目标语言 ISO C11（[WG14-N1570 §6.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：PowerShell 根据左操作数类型决定是执行字符串拼接（`'100' + 20 -> '10020'`）还是数值相加（`20 + '100' -> 120`）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C 语言中严禁依赖隐式转换！数值计算显式调用 `strtol` 转换并校验错误；字符串拼接显式使用 `snprintf`。
   - *不适用条件*：严禁直接使用 `atoi`（不提供溢出检查与非法字符位置检测）。
5. **错误机械替换反例**：
   ```c
   // 错误：使用 atoi 未检测错误，非法输入时静默返回 0
   int val = atoi(str);
   // 正确：使用 strtol 校验合法性
   char* endptr;
   long val = strtol(str, &endptr, 10);
   if (*endptr != '\0') { /* 解析失败处理 */ }
   ```
6. **信息不足或实现相关时的处理**：标记由于操作数顺序导致语义分化的潜在风险。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §6.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

### 规则 PS-C-03：PowerShell 错误偏好与 $LASTEXITCODE 向 C 显式错误状态码映射
1. **源码触发条件**：PowerShell 源码中配置 `$ErrorActionPreference` 并检查 `$LASTEXITCODE`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables), [MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)）；目标语言 ISO C11。
3. **原可观察行为**：非终止错误被忽略或打印，最后外部程序退出码被 `$LASTEXITCODE` 记录。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 C 中每一步系统调用显式检查返回值与 `errno`，在 `main` 退出时通过 `return code;` 或 `exit(code)` 回传。
   - *不适用条件*：严禁在 C 语言中忽略系统调用返回值。
5. **错误机械替换反例**：
   ```c
   // 错误：忽略文件移除返回值，与 PS 的非终止错误静默继续不同，在底层引发数据不一致
   remove(filepath); // 未检查返回值！
   // 正确：显式检查并记录
   if (remove(filepath) != 0) {
       perror("remove failed");
   }
   ```
6. **信息不足或实现相关时的处理**：若涉及外部进程执行，加载 [`skills/scenes/concurrency/SKILL.md`](../../scenes/concurrency/SKILL.md)。
7. **直接官方 HTTPS 依据链接**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)；[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
