---
name: powershell-to-python
description: Use when converting PowerShell source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → Python 语言转换规则

> **适用基线**：PowerShell 7.6 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 PowerShell](../../references/languages/powershell.md)与[目标语言 Python](../../references/languages/python.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/powershell-to-python/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 PowerShell → Python 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PS-PY-01：PowerShell 管道命令链向 Python 迭代器生成器与高阶函数映射
1. **源码触发条件**：PowerShell 源码中使用 `$input | Where-Object { ... } | ForEach-Object { ... }`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：对象逐个在管道中流式传递，处理大流时不占用全部内存。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用生成器表达式 `(fn(x) for x in input if cond(x))` 保持流式惰性求值；若需立即全量结果，使用列表推导 `[fn(x) for x in input if cond(x)]`。
   - *不适用条件*：严禁在无限流上使用列表推导（会导致内存耗尽 OOM）。
5. **错误机械替换反例**：
   ```python
   # 错误：针对大文件流或无限生成流使用列表推导，撑爆内存
   # lines = [line.strip() for line in huge_file]
   # 正确：使用生成器表达式流式处理
   lines = (line.strip() for line in huge_file)
   ```
6. **信息不足或实现相关时的处理**：若源管道包含特定 Cmdlet（如 `Sort-Object`），在 Python 中需要物化为列表再排序。
7. **直接官方 HTTPS 依据链接**：[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)；[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 PS-PY-02：PowerShell 单元素解包机制向 Python 列表长度隔离映射
1. **源码触发条件**：PowerShell 源码中处理管道输出，当结果仅有一项时自动变为标量。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)）；目标语言 Python 3.12。
3. **原可观察行为**：PS 管道输出零个元素返回 `$null`，一个元素返回标量对象，两个以上返回 `object[]`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Python 函数必须保持确定的返回类型契约！若声明返回 `list`，无论空、单元素还是多元素，统一返回 `list`。
   - *不适用条件*：严禁在 Python 中模仿 PowerShell 的自动解包行为（根据元素数量动态返回标量或列表），会给调用方类型检查带来极大混乱。
5. **错误机械替换反例**：
   ```python
   # 错误：模仿 PowerShell 的动态类型展开，破坏 Python 确定性接口契约
   def query_items():
       results = fetch()
       if len(results) == 1: return results[0] # 破坏了返回 list 的约定！
       return results
   # 正确：统一返回 list
   def query_items() -> list[Item]:
       return fetch()
   ```
6. **信息不足或实现相关时的处理**：对现有调用方做出防御性 `isinstance(res, list)` 适配。
7. **直接官方 HTTPS 依据链接**：[MS-PS-ARRAY](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)。

### 规则 PS-PY-03：PowerShell 退出码回写向 Python sys.exit 与返回值映射
1. **源码触发条件**：PowerShell 源码中使用 `exit $code` 或检查 `$LASTEXITCODE`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)）；目标语言 Python 3.12。
3. **原可观察行为**：回传退出状态码。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 CLI 入口处调用 `sys.exit(code)`；在普通模块函数中返回整数状态码或抛出异常。
   - *不适用条件*：严禁在被导入的模块内部直接调用 `sys.exit()`，会导致宿主解释器退出。
5. **错误机械替换反例**：
   ```python
   # 错误：在模块库函数内部调用 sys.exit
   def validate_config(cfg):
       if not cfg: sys.exit(1) # 导致第三方调用者进程无故终止！
   # 正确：抛出异常
   def validate_config(cfg):
       if not cfg: raise ValueError("Invalid configuration")
   ```
6. **信息不足或实现相关时的处理**：若需要调用外部原生命令并获取退出码，使用 `subprocess.run(..., check=False).returncode`。
7. **直接官方 HTTPS 依据链接**：[MS-PS-AUTO](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
