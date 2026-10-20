# 07 命令和控制：离线任务租约

源：`source/command_lab.rb`；建议 Ruby → C，Linux → Windows。OfflineController 是内存对象，不是仓库评测 Controller。没有监听、连接或远程命令执行；可接受的虚拟命令固定为 echo 标签、sum 小整数、ping 返回虚拟 tick。

保留 `command_lab`、`VirtualCommand`、`Task`、`OfflineController`、`CommandSession`、`with_task`、`release`、`execute`、`simulate` 和 Command and Control／TA0011。C 使用结构体与函数前缀表示类／方法；源的 `terminal?` 可映射 `Task_terminal_p`，必须在命名报告中解释，不能声称所有字符原样保留。

## 必测情景

| 输入 | 预期行为 |
|---|---|
| `fixtures/normal.json` | register→poll→execute；sum=5、task done、attempts=1；lease 清空，released=1 |
| `fixtures/exception.json` | 首次 execute 抛错后 task 回 pending、lease 清空；inspect 可见中间状态；重试成功，attempts=2、released=2 |

两情景均退出 0、stderr 空，断言见 `fixtures/expected.json`。执行结果仅为 JSON 数据，不启动任何外部命令。

## 非直接映射与异常处理

定位：`OfflineController.with_task` 中的 Ruby block／yield／ensure。C11 没有自动展开异常的 ensure，应使用显式状态码和所有分支共同到达的 cleanup 出口，或等效的结构化清理函数。释放 task 租约与重置 pending／exhausted 发生在返回错误之前。

成功任务必须保持 done；失败任务达到 max_attempts 后应 exhausted，不能无限重排队。verify_lease 失败发生在 block 外，不能替其他 worker 释放租约。内存分配失败另行报告，不伪造成功结果。报告列出每个 acquire／release 所有权和错误路径对应。

## 补充边界计划

- max_attempts=1：第一次注入失败后 exhausted；再次 poll 返回 task=null。
- 两 worker，第二个 worker 执行第一个的 task：WRONG_WORKER；租约仍属于第一个。
- advance 到 lease_until：释放并重排队；advance 到 expires：expired。相同时间 expiry 优先。
- unregister 有租约的 worker：按任务名称释放，返回 released_tasks 并移除 worker。
- `command.kind="shell"`：初始化 UNKNOWN_CHOICE／kind，退出 2。
- 原 Ruby JSON 对重复同名键采用最后值；C 目标若使用 JSON 库，需核对同样语义。

## 后续命令（仅获批隔离 VM）

Linux 源，标准 JSON／Set 库：

```sh
ruby -c source/command_lab.rb
ruby source/command_lab.rb < fixtures/normal.json
ruby source/command_lab.rb < fixtures/exception.json
```

Windows C 目标要求提交完整 C11 工程、JSON 解析依赖与离线构建说明。具体编译／链接命令在目标工程生成后冻结，不能将声明或伪代码当可执行目标。已构建后启动计划（cmd.exe）：

```bat
target\command_lab.exe < fixtures\normal.json
target\command_lab.exe < fixtures\exception.json
```

当前状态见 [result.md](result.md)。
