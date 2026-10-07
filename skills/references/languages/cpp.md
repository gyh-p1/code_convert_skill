# C++ 语言共性语义（ISO C++17）

> **用途**：供以 C++ 为源语言或目标语言的方向 Skill 按需读取；本页仅保存该语言的跨方向事实与风险，不指定任何源→目标映射。
> **知识与证据边界**：由原[七语言共性索引](../seven-language-common-semantics.md)的七个机制表逐行迁入；原有版本/官方依据随条目保留。静态事实不代表目标工具链已部署，也不代表任一方向的编译或行为已验收。
> **分类**：`[语言规范保证]`、`[指定运行时的实现相关事实]`、`[待专题核验，不可用于确定转换规则]` 的含义见[共性索引](../seven-language-common-semantics.md)。具体任务仍须冻结版本、运行时、OS、架构和 ABI。

## 一、值、引用、别名与可变性

- **语言规范保证**：`[语言规范保证]` 纯值传递与显式左值引用（`&`）/右值引用（`&&`）；移动语义（Move Semantics）转移资源所有权，原对象进入有效但未指定状态；`const` 限定符在类型系统中强制。
- **实现相关 / 运行时优化行为**：`[语言规范保证]` 复制省略（Guaranteed Copy Elision / RVO）由规范强制；`[指定运行时的实现相关事实]` 具体内存分配由存储期与编译器裁定。
- **机械等价禁区与转换约束**：不可将 C++ 移动语义机械等同于浅拷贝或解引用；移动后原对象析构仍会被调用；**不得把 C++ 的指针/智能指针判空与其他语言的“假值/真空值”判定互相当作等价**（见下条）。
- **官方资料依据**：[WG21-N4659 Clause 11.3, Clause 15.8](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)

### L1-CPP-01 判空与真值不是同一件事
1. **源码触发条件**：C++ 代码用 `if (p)` / `if (!p)` 判空（裸指针、`unique_ptr`/`shared_ptr` 的 `explicit operator bool`），或用 `if (n)` / `if (s.size())` 做零值/空容器判断。
2. **冻结版本/运行时/API 前提**：ISO C++17；智能指针的布尔转换见 [WG21-N4659 Clause 23.11](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。
3. **原可观察行为**：`if (ptr)` 判“是否持有对象/是否为空”，**与所指内容是否为空无关**；`if (str.size())` 判长度非零，与 `std::string` 内容中是否只有 `\0` 无关。`std::string` 可以合法地持有空内容但长度为 0，也可以持有含内部 `\0` 的非空内容。
4. **目标可选写法和不适用条件**：
   - *C++ 作为源*：把“是否持有”落到目标的 null/nil/None 检查，把“内容/长度为空”落到目标的长度或空容器检查，**两者不得合并**。
   - *C++ 作为目标*：源语言的真值判定必须显式重建；不得因为 `operator bool` 存在就把任意对象的真值判断等同于判空。
   - *不适用条件*：源中 `if` 判定的是纯数值零值或枚举时，不属判空，不要加空指针检查。
5. **错误机械替换反例**：
   ```cpp
   // 错误：把 Python 的空串/零值假值语义搬到 C++ 判空
   if (!cmdline) { return -1; }        // 只判“指针为空”，空串仍然通过
   // 错误之二：把 C++ 的 holder 判空当成内容非空
   if (sp) { use(*sp); }               // sp 非空不代表 *sp 的字符串非空
   // 正确：分别表达两层判断
   if (!sp) { return -1; }
   if (sp->empty()) { /* 内容为空的独立分支 */ }
   ```
6. **信息不足或实现相关时的处理**：无法确定源的判定表达“未持有”还是“内容为空”时，标为“判空与空值语义待确认”，不得用统一真值判断合并两者。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 7.3.11, Clause 23.11](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。

### L1-CPP-05 程序实参的计数基准与解析器语义必须显式重建

1. **源码触发条件**：源码从 `main(int argc, char* argv[])` 取用命令行实参，或用 `<getopt.h>` 的 `getopt`/`getopt_long`，或把 `argv` 交给下游/子进程。
2. **冻结版本/运行时/API 前提**：ISO C++17（[WG21-N4659 Clause 6.6.1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）；`getopt_long` 的行为取决于 **libc 实现**。
3. **原可观察行为**：
   - 当 `argc > 0` 时，`argv[0]` 表示程序名或空字符串；标准允许 `argc == 0`。`argv[argc]` 为空指针。"没有用户实参"由 `argc < 2` 判断。
   - `getopt`/`getopt_long` 保存**解析进度**（`optind`/`optarg`/`optopt`），该状态**跨调用保留**；glibc 默认**置换** `argv`，并允许长选项**唯一前缀**匹配。
   - 对未知选项 glibc 会**先自行输出诊断行**再返回 `'?'`；该输出属可观察行为。
4. **目标可选写法和不适用条件**：
   - *C++ 作为源*：目标语言的实参序列是否含程序名（Go `os.Args`、Python `sys.argv` 含；C# `args`、Ruby `ARGV` 不含）决定偏移，必须显式核对。
   - *C++ 作为目标*：源的"无用户实参"重建为 `argc < 2`；**不得**用 `argv[0] == nullptr` 判断用户实参数。
   - *不适用条件*：源码未使用命令行实参时不适用；源码显式设置 `POSIXLY_CORRECT` 关闭置换时，**不置换**才是要保留的行为。
5. **错误机械替换反例**：
   ```cpp
   // 错误一：把"数组不含程序名"的目标语言习惯套到 C++ 的 argv
   const char* first = argv[0];           // 取到的是程序名
   // 错误二：用 argv[0] 判空表达“没给参数”
   if (argv[0] == nullptr) { usage(); }   // 不能判断是否有用户实参
   // 错误三：把 getopt 的解析进度当成每次调用重新开始
   // 正确
   if (argc < 2) { usage(); }
   const char* first = argv[1];
   ```
6. **信息不足或实现相关时的处理**：无法确认源 libc、或无法确认是否依赖唯一前缀/置换时，标为“实参绑定与解析器语义待确认”；不得默认 glibc 行为。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 6.6.1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[POSIX `getopt`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/getopt.html)；[glibc `getopt_long`](https://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Options.html)。

## 二、整数宽度、溢出、符号性与转换

- **整数宽度规范**：`[语言规范保证]` 宽度规则继承 C；定义 `std::int32_t` 等定宽类型。
- **有符号溢出行为**：`[语言规范保证]` **未定义行为（UB）**（规范与 C 保持严格一致）。
- **无符号溢出行为**：`[语言规范保证]` **按模截断回绕**（Modulo $2^n$）。
- **隐式提升与转换陷阱**：`[语言规范保证]` 继承 C 整型提升规则；`std::size_t` 与带符号整数比较易引发反常循环。
- **官方资料依据**：[WG21-N4659 Clause 6.9.1, Clause 7.6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)

### L1-CPP-02 数值文本输出必须钉住格式与区域设置
1. **源码触发条件**：源码把数值以文本写出——`printf` 族、`std::ostringstream`/`std::to_string` 或 `std::cout <<`；`std::format` 不在 C++17 基线内。
2. **冻结版本/运行时/API 前提**：ISO C++17；新流继承构造时的全局 C++ locale；`std::to_string` 依标准的 `sprintf` 格式化语义，须另核对 C locale，不能宣称不受 locale 影响。
3. **原可观察行为**：
   - 流的数值格式受 `std::locale`（含 `imbue`）影响：小数点符号、千位分组**随区域设置变化**。
   - C++17 `std::to_string` 使用 `"%f"`/`"%d"` 等格式，浮点通常保留 6 位小数；小数点受 C locale 影响，与流的 locale 和有效位数设置是不同机制。
   - `std::cout <<` 与 `printf` 混用时的缓冲交错顺序属未指定行为。
4. **目标可选写法和不适用条件**：
   - *C++ 作为源*：目标语言的数值格式化必须显式钉住区域设置与有效位数，不得依赖目标运行时“碰巧与源一致”的默认值。
   - *C++ 作为目标*：源语言若依赖固定区域，按契约选择经典 locale 的流与明确精度；使用 `printf`/`to_string` 仍须核对 C locale，不能把切换 API 当作消除区域依赖。
   - *不适用条件*：源本身**有意**按用户区域设置输出（面向终端展示的本地化）时，区域依赖是要**保留**的行为，应显式冻结 locale 而不是消除它。
5. **错误机械替换反例**：
   ```cpp
   // 错误：源用 Python str(x) 的固定格式，目标却走了 locale 相关流
   std::ostringstream os;                 // 进程若设为 de_DE.UTF-8
   os << 1.5;                             // 得到 "1,5"，分隔符已变
   // 错误之二：用 to_string 冒充源的有效位数
   std::string s = std::to_string(1.0/3); // "0.333333"，源可能是 "0.3333333333333333"
   // 正确：钉住经典 locale 与显式精度
   std::ostringstream os;
   os.imbue(std::locale::classic());
   os << std::setprecision(17) << value;  // 精度按源的义务冻结，不靠默认值
   ```
6. **信息不足或实现相关时的处理**：无法确定源的有效位数与区域依赖时，标为“数值格式与区域设置待确认”，并把该文本列为 oracle 观察点；不得用“看起来一样”的默认输出充当依据。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 21.3, Clause 30.5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[cppreference `std::to_string`](https://en.cppreference.com/w/cpp/string/basic_string/to_string)。


## 三、字符串、字节、NUL、Unicode 与编码

- **字符串数据结构**：`[语言规范保证]` `std::string`（显式长度 + 缓冲区）；`std::string_view`（非拥有视窗：指针 + 长度）。
- **字节序列数据结构**：`[语言规范保证]` `std::vector<uint8_t>` 或 `std::byte[]`。
- **NUL (`\0`) 字符语义与处理**：`[语言规范保证]` `std::string` 允许内容包含内部 `\0`，`size()` 独立于内容；`c_str()` 追加尾随 `\0`；`std::string_view` **不保证以 `\0` 结尾**。
- **编码假设与转换陷阱**：`[语言规范保证]` 基础类型按代码单元操作；标准库不执行隐式编码转码。
- **官方资料依据**：[WG21-N4659 Clause 24.3, Clause 24.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)

### L1-CPP-03 字节进必须字节出：流不得被隐式套上文本翻译或编码转换
1. **源码触发条件**：源码以字节处理数据（`std::vector<uint8_t>`/`std::byte[]`、摘要与压缩、协议帧、二进制文件），或使用宽字符/文本流（`std::wcout`、`std::wofstream`、`std::locale` 编解码面）。
2. **冻结版本/运行时/API 前提**：ISO C++17；`std::basic_filebuf` 的字节/宽字符取向与 `std::codecvt` facet 见 [WG21-N4659 Clause 30.3, Clause 28.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)。
3. **原可观察行为**：
   - `std::ofstream`/`std::ifstream` 默认未设 `std::ios::binary`；文本/二进制区别取决于打开模式与平台。在 Windows CRT 文本模式下 LF 可翻译为 CRLF，**不能**由“C++ 流”推断输出为裸 LF。
   - `std::endl` 插入换行并刷新；最终字节须核对源 OS、CRT、stdout 模式及驱动是否归一化，不能只看插入的字符。
   - 宽字符流会经 `codecvt` facet 转换，**转换失败**使流进入 fail 状态并可能丢失数据。
   - `basic_ios::narrow`/`widen` 是字符转换接口，不是 C `FILE*` 的流取向开关；C `FILE*` 窄/宽取向与 C++ codecvt 须分开核对。
4. **目标可选写法和不适用条件**：
   - *C++ 作为源*：目标语言的字节层必须承接字节数据；只有在明确需要文本时才显式解码，且解码失败处理须与源一致。目标为 Windows 且经 CRT 文本模式时，**必须**用二进制模式。
   - *C++ 作为目标*：源语言若为文本类型，须显式选定编码并在边界一次转换；不得让宽字符 facet 或平台默认代码页替换字节。
   - *不适用条件*：源确为**面向终端/控制台的文本输出**且宽字符/本地代码页转换是可观察行为时，该转换应**保留**而非消除。
5. **错误机械替换反例**：
   ```cpp
   // 错误：声称 C++ 文件流天然二进制
   std::ofstream out(path);              // Windows 文本模式可能翻译换行
   // 按源确有的字节义务选择打开模式
   std::ofstream out(path, std::ios::binary);
   // 错误之二：二进制内容经宽字符流，编码转换失败静默丢数据
   std::wcout << blob;                    // blob 不是合法文本时流进入 fail 状态
   // 正确：字节路径保持字节，文本路径显式声明编码与换行
   out.write(reinterpret_cast<const char*>(blob.data()),
             static_cast<std::streamsize>(blob.size()));
   ```
6. **信息不足或实现相关时的处理**：无法确认源的换行与编码义务时，标为“编码与换行翻译位置待确认”；**禁止**用替换字符掩盖差异，也不要用 `std::endl` 的“刷新”副作用代替换行语义。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 28.4, Clause 30.3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[cppreference `std::endl`](https://en.cppreference.com/w/cpp/io/manip/endl)。

## 四、数组、容器、切片、迭代和顺序

- **数组/切片连续性与扩容**：`[语言规范保证]` `std::vector` 元素存储物理连续；`std::array` 固定容量连续存储，存储期与宿主对象一致；`[指定运行时的实现相关事实]` `vector` 扩容增长策略由实现决定，规范仅保证均摊常数复杂度。
- **键值映射（Map/Dict）实现**：`[语言规范保证]` `std::map` 为按键比较严格有序关联容器；`std::unordered_map` 为无序关联容器。
- **Map 遍历迭代顺序保证**：`[语言规范保证]` `std::map` 严格按键排序遍历；`std::unordered_map` 不保证任何顺序，重哈希可能改变顺序。
- **迭代期间修改（Fail-Fast）**：`[语言规范保证]` 容器修改可能引发迭代器失效（`vector` 插入可能失效全部迭代器；树节点关联容器插入不失效现有节点迭代器）。
- **官方资料依据**：[WG21-N4659 Clause 26](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)

## 五、异常、错误、退出码与可观察失败

- **语言级错误表示机制**：`[语言规范保证]` `try`/`catch`/`throw` 异常处理；无 `std::expected`（C++23）；错误码模式（`std::error_code`）。
- **异常展开与性能模型**：`[语言规范保证]` 语言规范定义异常类型体系与栈展开（Stack Unwinding）语义，沿栈逆序调用已构造局部对象的析构函数（RAII 展开）；标准不作底层“零成本”实现保证。
- **进程退出码回传机制**：`[语言规范保证]` 继承 C 的 `exit()` 与 `main` 返回机制；未捕获异常导致调用 `std::terminate()` 异常终止。
- **跨语言映射关键风险**：**严禁让 C++ 异常跨越 C ABI 边界**；跨界必须在边界包裹 `try ... catch(...)` 并转为错误码。
- **官方资料依据**：[WG21-N4659 Clause 18](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)

### L1-CPP-04 异常不得替换源端被丢弃的错误，源端主动失败不得被静默吞掉
1. **源码触发条件**：源码对可失败调用的结果**有意忽略**（未检查返回值/`error_code`、忽略部分成功），**或**在失败时 `throw`、返回非零、`std::exit(非零)`。
2. **冻结版本/运行时/API 前提**：ISO C++17；未捕获异常调用 `std::terminate`（[WG21-N4659 Clause 18.6.3.4, Clause 15.5.1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)）。
3. **原可观察行为**：
   - 忽略错误的路径：C++ 不会自动终止；程序继续并产出**当时能达到的结果**。若源忽略 `.open()`/`.close()`/`remove()` 的失败，则这些失败不产生可观察信号。
   - 主动失败的路径：异常被捕获前的栈展开按规则执行析构；未捕获时调用 `std::terminate`，栈是否完整展开由实现决定，退出状态亦须按运行环境记录。
4. **目标可选写法和不适用条件**（两个方向都必须覆盖）：
   - *源丢弃错误 → 目标不得变成异常终止*：目标语言的“抛错”只应在源**确实会失败退出**的位置保留；源忽略失败的路径必须映射为非致命路径。
   - *源主动失败 → 目标不得静默继续*：`throw`/非零返回必须映射为目标的失败传播，不得被宽泛 `catch (...)`/`rescue`/`except Exception` 吞掉。
   - *不适用条件*：源**确实检查**并据此失败时，不得套用“忽略并继续”。
5. **错误机械替换反例**：
   ```cpp
   // 源：directory_iterator 的 operator++ 抛异常，而源 fts 是“报告后继续”
   for (auto& e : std::filesystem::directory_iterator(dir)) {   // 抛异常直接终止?
       report(e);
   }
   // 错误之二：用 catch(...) 把源的失败分支吞成成功
   try { run(); } catch (...) { }        // 静默继续，退出码变成 0
   // 正确：按源语义分别处理——该继续的路径用 error_code 重载，该失败的路径传播
   std::error_code ec;
   for (auto it = std::filesystem::directory_iterator(dir, ec);
        !ec && it != std::filesystem::directory_iterator(); it.increment(ec)) {
       if (ec) { report_and_continue(ec); break; }   // 对齐源“报告后继续”
       report(*it);
   }
   ```
6. **信息不足或实现相关时的处理**：无法确认源是否检查、是否输出诊断、是否继续时，把该错误路径单列为待验证 oracle；不得以“异常更安全”为由默认改变控制流。
7. **直接官方 HTTPS 依据链接**：[WG21-N4659 Clause 15.5.1, Clause 18.6.3.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)；[cppreference `directory_iterator::increment`](https://en.cppreference.com/w/cpp/filesystem/directory_iterator/increment)。

## 六、内存、资源所有权、析构、GC 与终结

- **内存管理模型**：`[语言规范保证]` RAII（Resource Acquisition Is Initialization）：对象生命周期与作用域严格绑定；智能指针（`unique_ptr`, `shared_ptr`）。
- **资源确定性释放机制**：`[语言规范保证]` **确定性析构（Deterministic Destruction）**：离开作用域逆序调用析构函数，保证异常安全。
- **垃圾收集（GC）停顿与机制**：`[语言规范保证]` 无原生内置 GC。
- **悬垂与泄漏防范**：`std::string_view` 或引用引向已析构临时对象会导致严重悬挂引用。
- **官方资料依据**：[WG21-N4659 Clause 6.7, Clause 15.4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)

## 七、异步、并发、取消与阻塞

- **语言内建并发原语**：`[语言规范保证]` `std::thread`, `std::mutex`, `std::condition_variable`, `std::async`/`std::future`；无协程（C++20）。
- **线程/调度实体映射关系**：`[语言规范保证]` 标准定义程序内执行线程；底层 OS 线程调度属于平台实现，规范不作 1:1 映射保证。
- **级联取消与超时机制**：`[语言规范保证]` `std::future` 超时等待（`wait_for`）；无统一取消 Token（`std::stop_token` 为 C++20）。
- **内存模型与数据竞争**：`[语言规范保证]` 严格 C++11/C++17 内存模型；数据竞争（Data Race）属于未定义行为（UB）。
- **官方资料依据**：[WG21-N4659 Clause 33](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)

## 使用边界

将本页与所选的源→目标方向 Skill 及另一语言的共性页组合使用；映射前先确认源码真实行为。文件、网络、并发和跨 OS API 的具体差异仍按[共性索引的场景/系统分流](../seven-language-common-semantics.md)选读，不从语言事实直接推断系统 API 等价。没有逐例第三方证据时，语法/构建与功能结论保持 `UNVERIFIED`；本机不运行或编译样本。
