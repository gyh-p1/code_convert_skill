---
name: go-to-python
description: Use when converting Go source to Python; apply this direction's language-semantic mapping and preserve observable behavior. This skill does not establish compilation or functional correctness.
---

# Go → Python 语言转换规则

> **适用基线**：Go 1.27 → CPython 3.12。具体任务仍须冻结目标工具链、运行时、OS 和 ABI。
> **共性语义**：[分类与场景索引](../../references/seven-language-common-semantics.md)；按需读取[源语言 Go](../../references/languages/go.md)与[目标语言 Python](../../references/languages/python.md)。
> **证据边界**：以下是从原方向参考库迁入的静态决策规则；本方向尚无可据此宣称的目标编译或功能验收证据。不得把规则存在、候选 case 数量或模型自评当成转换成功。

## 适用范围与前提

仅用于 Go → Python 的语言层语义映射。先从实际源码确认触发条件、接口、错误路径、资源生命周期与外部可见副作用；只有适用的规则才加载和使用。涉及文件、网络、并发或跨 OS API 时，另读相应场景/系统 Skill，不以语言层相似性推定系统行为等价。

## 方向专向规则

### 规则 GO-PY-01：Go 切片容量共享向 Python list 独立扩容语义隔离映射
1. **源码触发条件**：Go 源码中使用 `s2 := s1[1:3]` 从原切片截取新切片并修改元素。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Slice_types](https://go.dev/ref/spec)）；目标语言 Python 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：Go 中 `s2` 与 `s1` 共享底层数组，修改 `s2` 会原地影响 `s1`；直到发生 `append` 扩容后才分离。
4. **目标可选写法和不适用条件**：
   - *可选映射*：Python 的切片操作 `l2 = l1[1:3]` 会**立即创建一个全新的浅拷贝独立列表**！修改 `l2` 绝不会影响 `l1`！若业务必须依赖共享修改，必须封装带视图指针的自定义类或操作同一个列表下标。
   - *不适用条件*：绝对不能直接假定 Python 切片具有 Go 切片的底层数组共享特性。
5. **错误机械替换反例**：
   ```python
   # 错误：以为 Python 切片像 Go 切片一样共享底层存储
   l1 = [1, 2, 3, 4]
   l2 = l1[1:3] # 生成了独立列表 [2, 3]
   l2[0] = 99   # l1 完全没有变化！l1[1] 依然是 2！
   # 正确：若需修改原列表，必须显式在原列表上修改
   l1[1] = 99
   ```
6. **信息不足或实现相关时的处理**：扫描所有切片赋值，确认是否有向原切片反写数据的依赖并告警。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Slice_types](https://go.dev/ref/spec)；[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 GO-PY-02：Go 显式 error 检查向 Python 结构化异常体系映射
1. **源码触发条件**：Go 源码中存在大量 `if err != nil { return nil, err }` 样板代码。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 Python 3.12（[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：错误通过返回值显式传递，未检查不会自动抛出。
4. **目标可选写法和不适用条件**：
   - *可选映射*：转换为 Python 标准异常（如 `ValueError`, `FileNotFoundError`, `RuntimeError`），依靠异常自动冒泡传播，消除深层样板检查。
   - *不适用条件*：严禁在 Python 中模仿 Go 返回二元元组并在每一步手写 `if err is not None`（严重违背 Python 习惯用法，极易遗漏处理）。
5. **错误机械替换反例**：
   ```python
   # 错误：在 Python 中强行写 Go 风格的返回元组，违背习惯且容易被忽略
   def divide(a, b):
       if b == 0: return None, "divide by zero"
       return a / b, None
   # 正确：抛出内置异常
   def divide(a, b):
       if b == 0: raise ZeroDivisionError("divide by zero")
       return a / b
   ```
6. **信息不足或实现相关时的处理**：若原 Go 错误类型具备专有字段，定义继承自 `Exception` 的子类。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA §3.2](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 GO-PY-03：Go 并发 Goroutine 与 Channel 向 Python asyncio 协程与 Queue 映射
1. **源码触发条件**：Go 源码中使用 `go fn()` 与 `ch := make(chan int)`。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27；目标语言 Python 3.12（[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)）。
3. **原可观察行为**：轻量级协程在 M:N 调度器下执行，支持高并发 channel 通信。
4. **目标可选写法和不适用条件**：
   - *可选映射*：重写为 `async def`，channel 替换为 `asyncio.Queue`，通信使用 `await queue.put()` 与 `await queue.get()`。
   - *不适用条件*：受 CPython GIL 影响，纯 CPU 运算无法多核加速；严禁在普通函数中直接使用阻塞队列而未设超时。
5. **错误机械替换反例**：
   ```python
   # 错误：在未加入事件循环的普通线程中调用 asyncio.Queue 导致 RuntimeError
   import asyncio
   q = asyncio.Queue() # 无当前运行的事件循环时在旧版本报错或引发跨线程异常
   ```
6. **信息不足或实现相关时的处理**：若代码涉及高吞吐 CPU 运算，向用户建议使用多进程并报告差异。
7. **直接官方 HTTPS 依据链接**：[PY-REF-DATA](https://docs.python.org/3.12/reference/datamodel.html)。

### 规则 GO-PY-04：Go nil 与零值向 Python None 的真值判定映射
1. **源码触发条件**：Go 源码用 `if err != nil`、`if len(parts) == 2`、`if pr.EncodedBlob == ""`、`if line != ""`、`if len(b) == 0`、`if len(matches) > 0` 之类的判断分流，或在 `map[string]any` 里放零值（如 `local_tasking_workers.go` 的 `if len(s.Tasks) == 0`、`signal_score_ingest.go` 的 `if pr.EncodedBlob == ""`、`concurrent_pipeline.go` 的 `if line != "" && len(line) < 200`）。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #Comparison_operators](https://go.dev/ref/spec)）；目标语言 Python 3.12（[PY-TRUTH](https://docs.python.org/3.12/library/stdtypes.html)）。
3. **原可观察行为**：Go 只显式比较 nil 或具体零值；`len(x) == 0` 与 `x == nil` 是两种不同判断，空切片/空 map/空字符串本身不是 nil；`nil != 0` 且 `nil != ""`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：把 Go 的 nil 状态映射为 `None` 并显式写 `is None` / `is not None`；把长度或内容判断显式写为 `len(x) == 0` / `not x` 只在**确实只想判断非空**时使用；对 `""`、`0`、空容器分别写 `== ""`、`== 0` 或 `not any(...)`，不要合并成一处 `if not v`。
   - *不适用条件*：严禁用 Python 的真值判断机械承接 Go 的 nil 判断——Python 中 `0`、`0.0`、`""`、`b""`、`[]`、`{}`、`set()` 全为假，把 `if err is not None` 改写成 `if err` 会在 `err` 为 `""`/`0` 时静默走错分支；反向把 `if len(x) == 0` 写成 `if x is None` 会漏判空容器。
5. **错误机械替换反例**：
   ```python
   # 错误：把 Go 的 if err != nil 改写成真值判断，零值错误/空字符串会静默走错分支
   def parse_line(line):
       fields = dict(p.split("=", 1) for p in line.split(";") if "=" in p)
       if not fields["payload"]:            # Go 中这里判的是字段是否存在/长度，不是“假值”
           return None
       return fields
   # 正确：把“缺键”“空串”“nil”分别显式写出
   def parse_line(line):
       fields = {}
       for p in line.split(";"):
           if "=" not in p:
               continue
           k, v = p.split("=", 1)
           fields[k] = v
       if "payload" not in fields:            # 对照 Go 的 map 取值 ok 断言
           return None
       if fields["payload"] == "":            # 对照 Go 的 == "" 判断
           return None
       return fields
   ```
6. **信息不足或实现相关时的处理**：若无法确认原 Go 判断是想表达“未设置”还是“值为零/空”，必须标注“nil 与零值语义待确认”，不得自行合并两种判断。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #Comparison_operators](https://go.dev/ref/spec)；[PY-TRUTH](https://docs.python.org/3.12/library/stdtypes.html)。

### 规则 GO-PY-05：Go time 格式化与 Duration 向 Python datetime/秒的可比性映射
1. **源码触发条件**：Go 源码取当前时间并按 `time.RFC3339` 序列化（`time.Now().Format(time.RFC3339)`），或使用 `time.Parse`、`time.Sleep(400 * time.Millisecond)`、`context.WithTimeout(ctx, cfg.TimeoutMS*time.Millisecond)`、`time.Now().UnixNano()` 派生时间戳（如 `concurrent_pipeline.go` 的 `Created: time.Now().Format(time.RFC3339)`、`signal_score_ingest.go` 的 `time.Sleep(400 * time.Millisecond)` 与 `time.Now().UnixNano()` 命名临时文件）。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-PKG-TIME](https://pkg.go.dev/time)）；目标语言 Python 3.12（[PY-DATETIME](https://docs.python.org/3.12/library/datetime.html)、[PY-TIME](https://docs.python.org/3.12/library/time.html)）。
3. **原可观察行为**：RFC3339 输出带明确的时区偏移（本地时间通常为 `+08:00` 形态）；同一进程内两次取时间得到不同值，`time.Now()` 附带单调时钟读数用于测量；`time.Duration` 是纳秒整数，`Duration.Milliseconds()` 等按整数截断。
4. **目标可选写法和不适用条件**：
   - *可选映射*：时区感知时刻用 `datetime.datetime.now(datetime.timezone.utc)`（或显式 `timezone(timedelta(hours=8))`）后调 `.isoformat()`，并按原格式显式拼接 `Z` 或 `+00:00`；时长统一换算为秒，用 `float(ms) / 1000.0` 或 `datetime.timedelta(milliseconds=ms)`；等待用 `time.sleep(seconds)`；测量间隔用 `time.monotonic()` 而不是 `time.time()`。
   - *不适用条件*：严禁把 `datetime.datetime.now()` 的 naive 结果与 `datetime.now(timezone.utc)` 的 aware 结果做减法或比较（会抛 `TypeError`）；不得用 `time.ctime()`/默认 `str(dt)` 的输出冒充 RFC3339 文本（字段顺序、时区后缀与小数点位数都不同）；也不得把 `time.Duration` 的纳秒整数直接当秒传给 `time.sleep`。
5. **错误机械替换反例**：
   ```python
   # 错误：naive 时间冒充 RFC3339，且把 Go 的纳秒 Duration 直接当秒传入
   from datetime import datetime
   import time
   stamp = datetime.now().isoformat()        # 无时区信息，输出形如 2026-10-02T19:10:03.123456
   # 对比 Go: time.Now().Format(time.RFC3339) → 2026-10-02T19:10:03+08:00
   time.sleep(400)                           # 原意是 400 * time.Millisecond = 0.4 秒！
   # 正确：aware 时间 + 秒换算
   stamp = datetime.now().astimezone().isoformat()
   time.sleep(400 / 1000.0)
   ```
6. **信息不足或实现相关时的处理**：若无法确认原 Go 代码依赖的是本地时区还是固定偏移、是否依赖时间字符串的精确形态（下游按字符串比较或解析），必须标注“时区与时间文本格式前提待确认”，不得自行选择 UTC 或本地时间。
7. **直接官方 HTTPS 依据链接**：[GO-PKG-TIME](https://pkg.go.dev/time)；[PY-DATETIME](https://docs.python.org/3.12/library/datetime.html)、[PY-TIME](https://docs.python.org/3.12/library/time.html)。

### 规则 GO-PY-06：Go string 与 []byte 边界向 Python str 与 bytes 显式编解码映射
1. **源码触发条件**：Go 源码在字符串与字节之间互转并做字节级处理，例如 `string(raw)`、`[]byte(line)`、`buf = []byte(err.Error())`、`base64.StdEncoding.DecodeString(pr.EncodedBlob)`、`sha256.Sum256(b)`、`json.Unmarshal(out, &pr)` 与 `cmd.Output()` 捕获子进程输出（见 `manifest_zip_collect.go` 的 `b := []byte(content)` 与 `hash(b)`、`child_cmd_capture.go` 的 `buf = []byte(err.Error())`、`signal_score_ingest.go` 的 `base64` 校验分支）。
2. **冻结版本/运行时/API 前提**：源语言 Go 1.27（[GO-SPEC #String_types](https://go.dev/ref/spec)）；目标语言 Python 3.12（[PY-STDTYPES](https://docs.python.org/3.12/library/stdtypes.html)、[PY-BASE64](https://docs.python.org/3.12/library/base64.html)、[PY-JSON](https://docs.python.org/3.12/library/json.html)）。
3. **原可观察行为**：Go 的 `string`/`[]byte` 互转按原始字节进行，长度按字节计；`string` 可包含任意字节序列（包括非法 UTF-8），并可按 UTF-8 迭代出 `rune`。
4. **目标可选写法和不适用条件**：
   - *可选映射*：文本路径用 `str`（`.encode("utf-8")` / `.decode("utf-8")` 显式转换），字节路径用 `bytes`；哈希/Base64 用 `hashlib.sha256(data).hexdigest()` 与 `base64.b64encode/b64decode`；JSON 用 `json.dumps(..., ensure_ascii=False).encode("utf-8")` 与 `json.loads(text_or_bytes)`；子进程输出显式选择 `capture_output=True, text=True`（得到 `str`）或省略 `text`（得到 `bytes`），不做隐式转换。
   - *不适用条件*：**严禁在 `str` 与 `bytes` 之间做隐式转换或混用**：`"a" + b"b"` 直接抛 `TypeError`，把 `bytes` 当 `str` 传给期望文本的 API（或反之）在 Python 3 中一律失败；`decode`/`encode` 遇到非法字节会抛 `UnicodeDecodeError`/`UnicodeEncodeError`，需要保留原始字节时必须走 `bytes` 路径而不是加 `errors="ignore"` 掩盖；也不得用 Python `str` 的字符长度承接 Go 按字节计的长度（非 ASCII 时两者不同）。
5. **错误机械替换反例**：
   ```python
   # 错误：把 Go 的 []byte / string 互转机械写成 Python 的隐式字符串处理
   raw = open(path).read()                     # 文本模式读取：二进制内容已按默认编码解码
   digest = hashlib.sha256(raw).hexdigest()    # TypeError: Strings must be encoded before hashing
   blob = base64.b64decode(raw)                # 若 raw 是含非 ASCII 的 str，同样报错
   # 正确：字节进字节出，需要文本时显式解码
   raw = open(path, "rb").read()               # 对照 Go 的 os.ReadFile → []byte
   digest = hashlib.sha256(raw).hexdigest()
   blob = base64.b64decode(raw)
   text = raw.decode("utf-8")                  # 对照 Go 的 string(raw)
   ```
6. **信息不足或实现相关时的处理**：若无法确认原数据的编码，或原 Go 代码依赖 `len(string)` 按字节计的长度语义，必须标注“编码与长度语义待确认”，不得用 `errors="replace"` 之类的宽松策略掩盖差异。
7. **直接官方 HTTPS 依据链接**：[GO-SPEC #String_types](https://go.dev/ref/spec)；[PY-STDTYPES](https://docs.python.org/3.12/library/stdtypes.html)、[PY-BASE64](https://docs.python.org/3.12/library/base64.html)、[PY-JSON](https://docs.python.org/3.12/library/json.html)。

## 转换与验证边界

> **构建前提**：目标代码进入编译前还须满足链接库、工程文件、工具链版本与构建缓存等前提，并须在冻结阶段写入任务契约（平台构建命令取自契约 `buildCommand`，不自动适配）。规则见[构建前提与工具链适配](../../../references/workflow/build-prerequisites.md)。

先守住输入输出、失败路径、状态、资源释放和副作用，再考虑目标语言惯用写法；不明确的版本、平台或调用约定写为待确认。目标代码的语法/构建与行为结论分别以获批隔离评估返回的逐例证据为准；**本机不编译或运行源码及转换产物**。遵守根[转换入口](../../../SKILL.md)与[安全边界](../../../references/framework/safety-boundary.md)。
