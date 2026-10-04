---
name: ruby-to-go
description: Use when converting Ruby source to Go; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Ruby → Go 语言转换规则

> **适用基线**：CRuby 3.4 → Go 1.27。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[七语言共性语义参考库](../../references/seven-language-common-semantics.md)。
> **方向案例与证据**：[同方向数据集](../../../docs/test/dataset/ruby-to-go/README.md)；候选、冻结任务与第三方回传须分层记录。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Ruby → Go 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 RB-GO-01：Ruby 动态鸭子类型向 Go 显式接口定义与满足映射
1. **源码触发条件**：Ruby 源码中依赖对象具备某个方法即可调用（鸭子类型），未声明显式继承或接口。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4；目标语言 Go 1.27（[GO-SPEC #Interface_types](https://go.dev/ref/spec)）。
3. **原可观察行为**：运行期只要响应方法（`respond_to?`）即调用成功，否则抛出 `NoMethodError`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在 Go 中显式定义 `type Duck interface { Method() }`，Go 结构体只需拥有对应签名的方法即可自动、隐式满足该接口，完美契合鸭子类型本质。
   - *不适用条件*：严禁使用 `interface{}` / `any` 加大量的运行时反射（`reflect`），会极大破坏 Go 性能与静态类型安全。
5. **错误机械替换反例**：
   ```go
   // 错误：滥用 reflect 反射调用方法模拟鸭子类型
   func Invoke(obj any) {
       reflect.ValueOf(obj).MethodByName("Action").Call(nil) // 脆弱、极其低效
   }
   // 正确：定义精确接口
   type Actioner interface { Action() }
   func Invoke(obj Actioner) { obj.Action() }
   ```
6. **信息不足或实现相关时的处理**：若对象响应的方法集极度动态，提取公共最小子集接口。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Interface_types](https://go.dev/ref/spec)。

### 规则 RB-GO-02：Ruby 异常控制流向 Go 显式多返回值 (T, error) 映射
1. **源码触发条件**：Ruby 源码中使用 `raise CustomError.new(...)` 并依赖多层拦截。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)）；目标语言 Go 1.27（[GO-SPEC #Errors](https://go.dev/ref/spec)）。
3. **原可观察行为**：抛出异常后中断当前调用链。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重写为 Go 的 `(T, error)` 返回值；在调用点逐层处理。
   - *不适用条件*：严禁将业务异常机械翻译为 Go `panic`。
5. **错误机械替换反例**：
   ```go
   // 错误：将 Ruby 的常规业务异常翻译为 panic
   func Validate(age int) {
       if age < 0 { panic("invalid age") } // 错误：导致不可预期的崩溃！
   }
   // 正确：返回 error
   func Validate(age int) error {
       if age < 0 { return errors.New("invalid age") }
       return nil
   }
   ```
6. **信息不足或实现相关时的处理**：若原 Ruby 错误存在丰富字段，定义包含相同字段的 Go 结构体。
7. **直接官方 HTTPS 依据链接**：[RB-DOC-EXCEPT](https://docs.ruby-lang.org/en/3.4/Exception.html)；[GO-SPEC #Errors](https://go.dev/ref/spec)。

### 规则 RB-GO-03：Ruby 任意精度数值向 Go 定宽整数模截断防溢出映射
1. **源码触发条件**：Ruby 源码中使用大整数算术或位运算。
2. **冻结版本/运行时/API 前提**：源语言 CRuby 3.4（[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)）；目标语言 Go 1.27（[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)）。
3. **原可观察行为**：数值任意精度，无固定溢出边界。
4. **目标可选写法和不适用条件**：
   - *可选映射*：若数值在 64 位内，使用 `int64`/`uint64`，注意溢出时 Go 是按模截断回绕（不会抛出异常）；若需保持无限精度，使用 `math/big.Int`。
   - *不适用条件*：严禁在数值可能超过 64 位时仍然采用裸 `int`。
5. **错误机械替换反例**：
   ```go
   // 错误：在 Go 中使用普通 int 进行超大数计算导致溢出截断
   // Ruby: 2**100
   var x int64 = 1 << 100 // 编译报错或溢出！
   // 正确：使用 big.Int
   x := new(big.Int).Exp(big.NewInt(2), big.NewInt(100), nil)
   ```
6. **信息不足或实现相关时的处理**：若无法确定上限，优先使用 `math/big` 并在报告中提示性能开销。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Arithmetic_operators](https://go.dev/ref/spec)；[RB-DOC-CORE](https://docs.ruby-lang.org/en/3.4/)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
