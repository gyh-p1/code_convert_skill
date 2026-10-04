---
name: powershell-to-ruby
description: Use when converting PowerShell source to Ruby; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# PowerShell → Ruby 语言转换规则

> **适用基线**：PowerShell 7.6 → CRuby 3.4。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 PowerShell](../../references/languages/powershell.md)与[目标语言 Ruby](../../references/languages/ruby.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/powershell-to-ruby/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 PowerShell → Ruby 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 PS-RB-01：PowerShell 管道流式传输向 Ruby Enumerable 链式方法调用映射
1. **源码触发条件**：PowerShell 源码中使用 `$data | Where-Object { ... } | ForEach-Object { ... }`。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)）；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：对象逐个通过管道过滤与投影。
4. **目标可选写法和不适用条件**：
   - *可选映射*：使用 Ruby `Enumerable` 链式调用：`data.select { |x| ... }.map { |x| ... }`；若针对大集合需惰性求值，在链首追加 `.lazy`（如 `data.lazy.select { ... }.map { ... }`）。
   - *不适用条件*：严禁直接在巨型数组上链式调用全量数组生成方法，避免多次中间数组分配。
5. **错误机械替换反例**：
   ```ruby
   # 错误：对超大流未使用 lazy，导致连续创建多重巨型中间数组引发内存溢出
   # huge_data.select { ... }.map { ... }
   # 正确：使用 .lazy 保持管道惰性流式计算
   huge_data.lazy.select { |x| x.valid? }.map { |x| x.process }
   ```
6. **信息不足或实现相关时的处理**：若源数据为哈希表，注意 Ruby 中迭代得到的是 `[key, value]` 数组。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)；[MS-PS-PIPE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)。

### 规则 PS-RB-02：PowerShell 非终止错误策略向 Ruby 显式 rescue 代码块映射
1. **源码触发条件**：PowerShell 源码中使用 `$ErrorActionPreference = 'SilentlyContinue'` 忽略命令错误。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6（[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)）；目标语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）。
3. **原可观察行为**：命令遇到非终止错误时不中断脚本，静默跳过继续执行。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Ruby 中对易出错的方法显式包裹 `begin ... rescue StandardError ... end`，或在单行使用 `action rescue nil`（仅限明确无副作用的只读探测）。
   - *不适用条件*：严禁在关键文件写或网络通信中滥用全局 `rescue nil`，会掩盖权限或路径等严重错误。
5. **错误机械替换反例**：
   ```ruby
   # 错误：滥用 rescue nil 掩盖核心业务异常
   File.write(target_path, content) rescue nil # 若目录不存在或无权限，静默失败且无日志！
   # 正确：针对性捕获并处理
   begin
     File.write(target_path, content)
   rescue SystemCallError => e
     warn "Write failed: #{e.message}"
   end
   ```
6. **信息不足或实现相关时的处理**：在报告中列出所有被降级为静默忽略的错误点。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[MS-PS-PREF](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)。

### 规则 PS-RB-03：PowerShell 字符转义反引号向 Ruby 双引号标准转义映射
1. **源码触发条件**：PowerShell 源码中使用反引号进行转义（如 `` `n `` 代表换行，`` `t `` 代表制表符，`` `$ `` 代表转义美元符）。
2. **冻结版本/运行时/API 前提**：源语言 PowerShell 7.6；目标语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）。
3. **原可观察行为**：PowerShell 特有的反引号作为转义前缀。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Ruby 双引号标准转义字符（`\n`, `\t`）；变量内插转换为 `#{var}`。
   - *不适用条件*：严禁在 Ruby 字符串中保留反引号转义字符，Ruby 双引号中反引号没有转义语义，会导致字面残留 `\``。
5. **错误机械替换反例**：
   ```ruby
   # 错误：将 PS 的反引号转义原样保留
   text = "`nHello" # 在 Ruby 中输出的是 "`nHello" 字面量，而不是换行！
   # 正确：转换为标准反斜杠转义
   text = "\nHello"
   ```
6. **信息不足或实现相关时的处理**：扫描源码所有反引号转义并做正规化替换。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
