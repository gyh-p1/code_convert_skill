---
name: cpp-to-go
description: Use when converting C++ source to Go; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# C++ → Go 语言转换规则

> **适用基线**：ISO C++17 → Go 1.27。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：先读根[转换入口](../../../SKILL.md)的必读契约；[分类与场景索引](../../references/seven-language-common-semantics.md)；必读[源语言 C++](../../references/languages/cpp.md)与[目标语言 Go](../../references/languages/go.md)，按源码选择适用规则。
> **证据边界**：以下规则用于当前任务的映射选择；目标编译与功能结论须依据本项精确版本的独立证据，不以规则存在或模型自评替代。

## 适用范围与前提

仅用于 C++ → Go 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 CPP-GO-01：C++ 类继承虚函数多态向 Go 隐式接口与结构体内嵌组合映射
1. **源码触发条件**：C++ 源码中定义包含纯虚函数的基类，派生类通过 `override` 覆写接口。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17（WG21-N4659 Clause 13.3）；目标语言 Go 1.27（GO-SPEC #Interface_types）。
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
7. **资料依据（名称/版本/章节）**：GO-SPEC #Interface_types。

### 规则 CPP-GO-02：C++ 异常控制流向 Go 显式多返回值 (T, error) 与 defer 逆序清理映射
1. **源码触发条件**：C++ 源码中使用 `throw` 抛出异常并在外层 `try ... catch` 捕获。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 Go 1.27（GO-SPEC #Errors, #Defer_statements）。
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
7. **资料依据（名称/版本/章节）**：GO-SPEC #Defer_statements；Effective Go: Panic/Recover。

### 规则 CPP-GO-03：C++ std::mutex/std::condition_variable 向 Go sync/Channel 映射
1. **源码触发条件**：C++ 源码中使用 `std::unique_lock` 和条件变量进行生产者-消费者通知。
2. **冻结版本/运行时/API 前提**：源语言 ISO C++17；目标语言 Go 1.27（GO-SPEC #Channel_types, GO-MEM）。
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
7. **资料依据（名称/版本/章节）**：Go sync.Cond；GO-SPEC #Channel_types；GO-MEM。

### 规则 CPP-GO-04：C++ 块级与循环内 RAII 析构向 Go 函数级 `defer` 的作用域映射
1. **源码触发条件**：C++ 源码在 `if` 分支、`for`/`while` 循环体内或嵌套代码块 `{ ... }` 中声明带析构函数的局部守卫（文件、锁、事务、临时对象）。
2. **冻结版本/运行时/API 前提**：ISO C++17（WG21-N4659 Clause 6.7）→ Go 1.27（GO-SPEC #Defer_statements）。
3. **原可观察行为**：每个局部块或每次循环迭代结束时立即执行析构（释放锁/关闭文件），不会累积到外层函数返回才释放。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Go `defer` 绑定到**外层包含函数**而非词法块。循环体与短临界区必须抽成受限局部函数（或匿名闭包调用 `func() { ... }()`)，在该闭包的 `defer` 中立即释放；或显式在路径出口释放。
   - *不适用条件*：严禁在 `for` 循环体内直接写 `defer f.Close()` 或 `defer mu.Unlock()`——文件句柄将堆积至函数结束，锁则会在第二次迭代直接自我死锁。
5. **错误机械替换反例**：
   ```go
   // 错误：循环内直接 defer 锁或文件关闭，下一次迭代死锁或句柄泄漏
   for _, p := range paths {
       f, err := os.Open(p)
       if err != nil { return err }
       defer f.Close() // 直到整个外层函数返回才关闭！
   }

   // 正确：将单次迭代逻辑封装为闭包，保证每次迭代结束即触发 defer
   for _, p := range paths {
       if err := func() error {
           f, err := os.Open(p)
           if err != nil { return err }
           defer f.Close()
           return process(f)
       }(); err != nil {
           return err
       }
   }
   ```
6. **信息不足或实现相关时的处理**：若循环内提前 `break`/`return`/`continue` 的清理条件复杂，抽取命名 helper 返回显式状态码或错误以保持控制流清晰。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Defer_statements；WG21-N4659 Clause 6.7。

### 规则 CPP-GO-05：C++ `std::map` 有序遍历与索引查找语义向 Go 随机 `map` 映射
1. **源码触发条件**：C++ 源码使用 `std::map` 遍历依赖按键序输出，或区分 `m.find(k)`（只读）与 `m[k]`（缺键自动插入零值/默认构造成员）。
2. **冻结版本/运行时/API 前提**：ISO C++17（WG21-N4659 Clause 26.4）→ Go 1.27（GO-SPEC #Map_types、`slices.Sort`）。
3. **原可观察行为**：`std::map` 始终按比较器有序遍历；`operator[]` 在键不存在时会修改容器插入默认值，而 `find`/`at` 不会修改。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Go `for k, v := range m` 遍历顺序有意随机化；若源顺序可观察，须先收集键切片按源比较器排序后再遍历。只读查找用 `v, ok := m[k]`，明确区分缺失与零值；仅当源调用 `operator[]` 并依赖自动插入副作用时，才在 `!ok` 时显式插入零值并写回（尤其值类型为 `struct` 时，`m[k].Field = x` 在 Go 中无法直接寻址编译报错）。
   - *不适用条件*：严禁直接用 `range m` 替代 `std::map` 序输出；严禁误认为 `m[k]` 会像 `std::map` 一样自动在缺键时往 map 插入元素。
5. **错误机械替换反例**：
   ```go
   // 错误：直接 range Go map 替代 std::map 有序遍历，输出每次随机乱序
   for k, v := range m {
       fmt.Println(k, v)
   }

   // 正确：显式提取并按源比较序排序键后再输出
   keys := make([]string, 0, len(m))
   for k := range m {
       keys = append(keys, k)
   }
   slices.Sort(keys)
   for _, k := range keys {
       fmt.Println(k, m[k])
   }
   ```
6. **信息不足或实现相关时的处理**：C++ 自定义比较器的等价判定（Strict Weak Ordering）与字符串大小写/文化排序规则若不同于 Go 字典序，按自定义 `slices.SortFunc` 保持。
7. **资料依据（名称/版本/章节）**：WG21-N4659 Clause 26.4；GO-SPEC #For_range、#Map_types。

### 规则 CPP-GO-06：C++ 容器值拷贝向 Go slice/map 引用共享语义的防污染映射
1. **源码触发条件**：C++ 源码将 `std::vector` / `std::map` 按值拷贝（`auto copy = orig;`）或按值传参后独立修改或 `push_back`。
2. **冻结版本/运行时/API 前提**：ISO C++17 → Go 1.27（GO-SPEC #Slice_types、`slices.Clone`、`maps.Clone`）。
3. **原可观察行为**：C++ 值容器赋值与按值传参复制整份底层元素存储；对副本修改或扩容绝不反写原容器。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Go 中 `b := a` 复制的是 slice header 或 map header，底层数组/哈希表仍共享！当源按值拷贝并会写入/切片追加时，必须用 `slices.Clone(a)` / `maps.Clone(a)`（元素含指针或嵌套引用时逐层深克隆），并对子切片写操作使用三索引切片 `s[l:h:h]` 限制容量防 `append` 覆盖原底层数组后续元素。
   - *不适用条件*：严禁将 C++ 按值复制的 `std::vector` 直接写成 `b := a` 后写入或 `append`。
5. **错误机械替换反例**：
   ```go
   // 错误：切片赋值共享底层数组，且未设 cap 上限的 append 污染 orig
   orig := []int{1, 2, 3, 4}
   sub := orig[:2]
   sub = append(sub, 99) // 覆盖了 orig[2] 变成 [1, 2, 99, 4]！

   // 正确：若要求与 orig 独立，显式 Clone 或使用完整切片表达式隔离容量
   isolated := slices.Clone(orig[:2])
   isolated = append(isolated, 99)
   ```
6. **信息不足或实现相关时的处理**：区分零长度非 nil 空切片 `[]T{}` 与 `nil` 切片（影响 `encoding/json` 输出为 `[]` 或 `null`，见 `L1-GO-15`）。
7. **资料依据（名称/版本/章节）**：GO-SPEC #Slice_types、#Appending_and_copying_slices；标准库 `slices`/`maps`。

### 规则 CPP-GO-07：C++ `std::string` 原始字节与隐式整型提升向 Go `[]byte`/`string` 与显式转换映射
1. **源码触发条件**：C++ 源码使用 `std::string` 承载含任意字节/`\0` 数据、按字节下标迭代 `s[i]`，或依赖 `char`/`int`/`size_t` 之间隐式窄/宽转换。
2. **冻结版本/运行时/API 前提**：ISO C++17 → Go 1.27（GO-SPEC #Conversions、`for range`）。
3. **原可观察行为**：`std::string::size()` 与下标按单字节操作，即使存在 `\0` 或非 UTF-8 字节也能无损保持；整型之间自动按 C++ 规则隐式提升或算术转换。
4. **目标可选写法和不适用条件**：
   - *可选映射*：含可能非 UTF-8 原始字节、内嵌 `\0` 或需可变字节缓冲时映射为 `[]byte`；按字节遍历使用索引循环 `for i := 0; i < len(s); i++`，只有确认为按 UTF-8 Unicode 码点遍历时才使用 `for _, r := range s`（注意遇到非法 UTF-8 字节时 Go `for range` 会替换成 `U+FFFD`，掩盖原字节！）。Go 不允许整型混合隐式转换，全部跨类型运算须显式转换并核符号与截断边界。
   - *不适用条件*：严禁用 `for _, r := range s` 替代逐字节检查；严禁将无符号长度减法改写为可能无符号下溢的逆序。
5. **错误机械替换反例**：
   ```go
   // 错误：对可能含非 UTF-8 原始字节的字符串使用 range，非法字节被变成 U+FFFD (0xFFFD)
   for _, ch := range rawStr {
       out = append(out, byte(ch)) // 若 ch==U+FFFD，byte(ch) 被静默截断为 0xFD，数据彻底损毁！
   }

   // 正确：按字节维度处理时直接使用索引遍历 []byte 或 s[i]
   for i := 0; i < len(rawBytes); i++ {
       out = append(out, rawBytes[i])
   }
   ```
6. **信息不足或实现相关时的处理**：编码边界未知时默认保守保留 `[]byte` 并标出与文本格式化消费者（如 `%s`、JSON 输出）的衔接点。
7. **资料依据（名称/版本/章节）**：GO-SPEC #For_range、#String_types、#Conversions。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
