---
name: powershell-to-c
description: Use when converting PowerShell source to C; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → C 语言转换规则

> **适用基线**：PowerShell 7.6 → ISO C11。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 PowerShell](../../references/languages/powershell.md)与[目标语言 C](../../references/languages/c.md)。
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

### 规则 PS-C-04：PowerShell `$null`/空字符串/空数组/空集合的真值差异向 C 指针与长度双重判定映射
1. **源码触发条件**：源码把可能为空的取值结果直接放进条件或比较，例如 `if ($UserList -eq "")`、`while ($SmallestLockoutThreshold -eq "0")` 的反面写法、`if ( $PSOs.count -gt 0)`、`if (!$CallResult)`、`if ($DomainController -and $Credential.GetNetworkCredential().Password)`；取值来源可返回“无结果”，如 `Get-Content`、`$searcher.FindAll()`、`[ADSI]`、P/Invoke 布尔返回值与 `IntPtr` 返回值。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators), [MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)）；目标语言 ISO C11（[WG14-N1570 §6.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：PowerShell 把 `$null`、空字符串、空数组、空集合以及数值 0 都按“假”参与布尔化，`$null` 参与左侧字符串比较时按空字符串处理，单元素结果自动退化为标量使 `.Count` 语义随元素个数变化；因此“无结果”“空结果”“结果为空串”在源码里往往走同一分支。
4. **目标可选写法和不适用条件**：
   - *可选映射*：C 中拆成两个显式事实——指针是否为 `NULL`、以及长度/计数是否为 0；返回“可能有/没有”的取值函数统一用 `int f(T *out, size_t *out_len)` 形式，调用点两项都判断。
   - *不适用条件*：严禁把 `if ($x)` 机械写成 `if (x)` 或 `if (*x)`：对 `char *` 只判非空会放过空字符串，对结构体指针只判非空会放过“存在但长度为 0”，对已解引用值判断还会在指针为 `NULL` 时形成空指针解引用（UB）。“有条件的映射”：若源语义确实是“非空即真”，可保留单条件，但必须在转换记录里写明该取值点按契约不会出现 `NULL`。
5. **错误机械替换反例**：
   ```c
   /* 错误：源 PS 的 if ($UserListArray.count -gt 0) 被写成只判指针 */
   if (users != NULL) {
       for (size_t i = 0; i < user_count; i++) { /* 未读 user_count，长度未定义 */ }
   }
   /* 正确：指针与长度两项都判定 */
   if (users != NULL && user_count > 0) {
       for (size_t i = 0; i < user_count; i++) { /* ... */ }
   }
   ```
6. **信息不足或实现相关时的处理**：若无法确认某取值点在无结果时是返回 `$null`、空数组还是空字符串，必须停下标注该点并向用户确认；不要把 `.Count` 与 `.Length`、把 `[int]` 转换后的 0 与 `$null` 当作同一事实处理。
7. **直接官方 HTTPS 依据链接**：[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators)；[WG14-N1570 §6.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

### 规则 PS-C-05：PowerShell 字符串内插与 `-f`/`-join` 格式组装向 C `snprintf` 与显式字节长度映射
1. **源码触发条件**：源码用双引号内插拼装文本，或使用格式/连接运算符，例如 `"$ProcessName_$ProcessId.dmp"`、`"[*] The smallest lockout threshold ... is $SmallestLockoutThreshold login attempts."`、`("PS " + (Get-Location).Path + '>')`、`$packet[10..13] -join ""`、`("{0,-10}{1,0}" -f "PORT","STATE")`、`("{0:x}" -f $value)`、`$buffer.Value -join ""`；随后把结果交给字节编码或写入。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-OPERATORS](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators), [MS-PS-QUOTES](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules)）；目标语言 ISO C11（[WG14-N1570 §7.21.6.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：内插自动对任意对象调用其字符串化（`[string]`）语义；`-f` 支持对齐与进制说明符（`{0,-10}`、`{0:x}`、`{0}`）并自动格式化参数；`-join` 连接元素序列；`.Length` 报告 UTF-16 代码单元数，而 `.NET` 编码器产出的字节数与之不同，二者在源码里常被混用（如把 `.Length` 当作字节长度传给写入 API）。
4. **目标可选写法和不适用条件**：
   - *可选映射*：用 `snprintf(buf, sizeof buf, "...%s...%d...", ...)` 组装文本，返回值先与 `sizeof buf` 比较以判定截断；需要十六进制/对齐补零时显式写字宽与进制（`%08x`、`%-10s`、`%02x`）；编码后的字节数与字符数分别用独立变量保存，缓冲区容量按编码后的最坏字节数计算。
   - *不适用条件*：严禁用 `strcat`/`sprintf` 做逐段累加内插（无界写入）；严禁把 UTF-16 代码单元数直接当作 `char` 缓冲区的字节容量（会按一半容量分配）；严禁把 `'{0:x}'` 这类补零格式机械写成 `%x`（丢失宽度与补零，出现长度不定的输出）。
5. **错误机械替换反例**：
   ```c
   /* 错误：把 -join 结果与字符串长度当字节数，且无界拼装 */
   char cmd[256];
   strcpy(cmd, "PS ");
   strcat(cmd, cwd);                  /* 未检查容量 */
   size_t nbytes = strlen(cwd);       /* 与源 .Length 的代码单元数不是同一量 */
   /* 正确：有界组装并单独换算字节数 */
   int rc = snprintf(cmd, sizeof cmd, "PS %s>", cwd);
   if (rc < 0 || (size_t)rc >= sizeof cmd) { return -1; }  /* 截断即失败 */
   size_t nbytes = (size_t)rc;        /* 实际写入字节数 */
   ```
6. **信息不足或实现相关时的处理**：源内插的对象字符串化依赖宿主与文化设置时（例如日期、浮点），必须停下标注该点的确切格式来源；目标输出编码（ASCII/UTF-8/ANSI 代码页）未冻结前，不要假定 `snprintf` 的字节数与源编码结果一致。
7. **直接官方 HTTPS 依据链接**：[WG14-N1570 §7.21.6.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)；[MS-PS-QUOTES](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules)。

### 规则 PS-C-06：PowerShell 非终止错误、`-ErrorAction Stop`、`$Error` 与 `try/catch` 向 C 返回码与错误出口映射
1. **源码触发条件**：源码使用 `-ErrorAction Stop`/`-EA SilentlyContinue`、读取 `$Error[0]`/`$_`、`$Error.Clear()`，或把易失败调用包在 `try { } catch { }` 里，例如 `Get-Content $UserList -ErrorAction stop`、`throw "[!] Could not connect to the domain..."`、`$error[0] | Out-String`、`$error.clear()`、P/Invoke 返回布尔值后的 `if (!$CallResult)` 分支。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables), [MS-PS-TRY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)）；目标语言 ISO C11（[WG14-N1570 §7.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)）。
3. **原可观察行为**：Cmdlet 的多数失败是非终止错误：写入错误流、`$?` 变为 `$false`、`$Error` 集合头部追加一条记录，而脚本继续执行；只有 `-ErrorAction Stop`（或偏好变量为 `Stop`、或显式 `throw`）才转成终止错误并被 `catch` 捕获；`$Error.Clear()` 会清空历史，使后续错误记录索引改变。源中“看起来像异常”的分支与其“是否中断控制流”的实际语义必须逐点确认。
4. **目标可选写法和不适用条件**：
   - *可选映射*：C 用返回值表达失败：每个可能失败的系统调用/库调用检查其返回值与 `errno`，向上返回 `int` 错误码、或在输出参数中带出错误信息；进程级失败用 `return code;`/`exit(code)` 回传；`try/catch` 的捕获点对应到调用点的错误检查，`finally` 中“总会执行”的清理对应到统一的 `goto cleanup` 出口。
   - *不适用条件*：严禁把非终止错误机械降级为“忽略返回值继续跑”——这正是源实现里最容易被误读的地方；同样严禁在没有语言级异常的前提下为每个失败点引入 `setjmp`/`longjmp`（它不执行清理，会跳过手工释放路径）。非失败路径必须保持不中断。
5. **错误机械替换反例**：
   ```c
   /* 错误：源里 -ErrorAction Stop 的失败点被当成“总能继续” */
   FILE *f = fopen(list_path, "r");
   while (fgets(line, sizeof line, f) != NULL) { /* 未查 f，形成空指针解引用 */ }
   /* 正确：先判定返回值并形成显式错误出口 */
   FILE *f = fopen(list_path, "r");
   if (f == NULL) { perror("open user list"); return 2; }  /* 与源的中断语义对齐 */
   while (fgets(line, sizeof line, f) != NULL) { /* ... */ }
   fclose(f);
   ```
6. **信息不足或实现相关时的处理**：若无法确定源命令的失败在当前偏好设置下是终止还是非终止（例如来自模块的 Cmdlet、或偏好由调用方设置），必须停下标注该点；`$Error` 的历史顺序与 `$Error.Clear()` 时机不要在 C 中尝试复刻，只需保留“哪个失败被观察到、是否中断”的事实。
7. **直接官方 HTTPS 依据链接**：[MS-PS-TRY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)；[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
