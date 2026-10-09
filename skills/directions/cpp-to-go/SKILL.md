---
name: cpp-to-go
description: Use when converting C++ source to Go; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → Go 语言转换规则

> **适用基线**：ISO C++17 → Go 1.27。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 C++](../../references/languages/cpp.md)与[目标语言 Go](../../references/languages/go.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 C++ → Go 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-GO-01：C++ 类继承虚函数多态向 Go 隐式接口与结构体内嵌组合映射
1. **源码触发条件**：C++ 源码中定义包含纯虚函数的基类，派生类通过 `override` 覆写接口。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（[WG21-N4659 Clause 13.3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；目标语言 Go 1.27（[GO-SPEC #Interface_types](https://go.dev/ref/spec)）。
3. **原可观察行为**：通过基类指针或引用调用虚函数触发动态分派。
4. **目标可选写法和不适用条件**：
   - *可选映射*：将纯虚基类定义为 Go 的 `interface`；派生类定义为独立 `struct` 并实现相同签名的方法，实现隐式满足；代码复用通过结构体内嵌（Embedding）实现。
   - *不适用条件*：严禁在 Go 结构体内嵌中假设多态的“反向虚调用”（内嵌外层方法不会自动覆盖内层方法的内部调用）。
5. **错误机械替换反例**：
   ```go
   // 错误：在 Go 内嵌结构体中期待 C++ 虚函数双向覆盖行为
   type Base struct{}
   func (b *Base) TemplateMethod() { b.Hook() } // 永远调用 Base.Hook，无法多态覆盖！
   func (b *Base) Hook() { fmt.Println("Base") }
   type Derived struct{ Base }
   func (d *Derived) Hook() { fmt.Println("Derived") }
   // 正确：将多态解耦为显式接口参数传递
   type Hooker interface { Hook() }
   func TemplateMethod(h Hooker) { h.Hook() }
   ```
6. **信息不足或实现相关时的处理**：若 C++ 基类包含非公开私有虚函数，重构为包内私有方法。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Interface_types](https://go.dev/ref/spec)。

### 规则 CPP-GO-02：C++ 异常控制流向 Go 显式多返回值 (T, error) 与 defer 逆序清理映射
1. **源码触发条件**：C++ 源码中使用 `throw` 抛出异常并在外层 `try ... catch` 捕获。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 Go 1.27（[GO-SPEC #Errors, #Defer_statements](https://go.dev/ref/spec)）。
3. **原可观察行为**：异常沿调用栈向上展开，自动析构局部对象，直至被匹配的 catch 捕获。
4. **目标可选写法和不适用条件**：
   - *可选映射*：在允许调整接口时增加 `error` 返回值；同步改所有调用点，保留 catch 的类型选择、传播/恢复边界和错误上下文。清理按源析构时机对应；Go `defer` 在外层函数返回时执行，不是离开任意块即执行。源为块级 RAII、锁释放或循环每次清理时，用受限辅助函数/显式路径清理保持作用域与 LIFO 次序，不能直接把所有释放延迟到大函数结束。
   - *不适用条件*：不能机械把异常映射为 `panic`，也不能把显式 error 丢弃。Go 支持受限的 `panic/recover`，但它不是 C++ 任意 catch 的自动对应；只有错误边界、同一 goroutine 内展开/恢复及清理均能核对时才考虑受限实现，不以惯用写法改变异常传播。
5. **错误机械替换反例**：
   ```go
   // 错误：将常规的查找不到或输入校验错误机械替换为 panic
   func FindUser(id int) User {
       if id <= 0 { panic("invalid id") } // 错误：将常规可预期校验写为 panic！
       return user
   }
   // 正确：显式返回 error
   func FindUser(id int) (User, error) {
       if id <= 0 { return User{}, errors.New("invalid id") }
       return user, nil
   }
   ```
6. **信息不足或实现相关时的处理**：若源异常携带丰富错误上下文，定义自定义错误结构体实现 `Error() string`。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Defer_statements](https://go.dev/ref/spec#Defer_statements)；[Effective Go: Panic/Recover](https://go.dev/doc/effective_go#panic)。

### 规则 CPP-GO-03：C++ std::mutex/std::condition_variable 向 Go sync/Channel 映射
1. **源码触发条件**：C++ 源码中使用 `std::unique_lock` 和条件变量进行生产者-消费者通知。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 Go 1.27（[GO-SPEC #Channel_types](https://go.dev/ref/spec), [GO-MEM](https://go.dev/ref/mem)）。
3. **原可观察行为**：消费者在条件变量上阻塞等待唤醒，互斥锁保护队列临界区。
4. **目标可选写法和不适用条件**：
   - *可选映射*：对基于共享谓词的条件变量，优先核对 `sync.Mutex` + `sync.Cond` 的等待循环、Signal/Broadcast 和退出条件；只有任务传递/通知语义确实对应时才使用 `chan T`，并冻结容量、背压、关闭与取消语义。通道不是条件变量的通用替代物。
   - *不适用条件*：必须注意 Go 数据竞争不是未定义行为，但含竞争会导致状态损毁或程序终止，严禁无保护并发读写变量。
5. **错误机械替换反例**：
   ```go
   // 错误：使用裸变量轮询代替条件变量，且未加锁导致数据竞争
   var ready bool
   go func() { ready = true }()
   for !ready {} // 错误：数据竞争（Data Race），且极易在编译器优化下死循环！
   // 正确：使用 channel 进行安全通知
   done := make(chan struct{})
   go func() { close(done) }()
   <-done
   ```
6. **信息不足或实现相关时的处理**：若需级联取消与超时，结合 `context.WithTimeout` 处理。
7. **直接官方 HTTPS 依据链接**：[Go sync.Cond](https://pkg.go.dev/sync#Cond)；[GO-SPEC #Channel_types](https://go.dev/ref/spec#Channel_types)；[GO-MEM](https://go.dev/ref/mem)。

## 转换与验证边界

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
