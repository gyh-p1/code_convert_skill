# 08 数据外传：内存分块接收端

源：`source/exfiltration_lab.ps1`；建议 PowerShell → Go，Windows → Linux。接收端只是 Dictionary，数据只来自 stdin，不访问文件或地址，不把任何内容发送到网络。“外传”是本例的业务模拟主题。

保留 `exfiltration_lab`、TACTIC／TACTIC_ID、ModelError、Get-Chunk、Send-Packet、Receive-Packet、Complete-Transfer、Invoke-Simulation 的语义词根和对应关系。Go 不能使用带连字符的标识符，可映射 `Get_Chunk` 等；必须记录映射。保留验证／字节分块／接收状态／JSON 入口四层。

## 必测情景

| 输入 | 预期行为 |
|---|---|
| `fixtures/normal.json` | 猫a 按字节切成 e78c、ab61；重复发第0包不重复落盘；commit 成功；attempts=3、duplicates=1、closed_buffers=3 |
| `fixtures/exception.json` | send_all 在第2次发送失败；第0包保留、missing=[1]，活动缓冲=0；重试只补缺包，最终 commit 成功 |

两情景均退出 0、stderr 空，断言见 `fixtures/expected.json`。中间字节块可以不是有效 UTF-8，不得单独解码后替换乱码。

## 非直接映射与异常处理

定位：`Get-Bytes`、`Get-Chunk`、`Get-Missing` 的一元逗号，以及 `Send-Packet` 的 try/finally。PowerShell 管道会展开集合，空集合也可能不产出对象；本源显式返回数组。Go 使用 `[]byte`／`[]int` 时应区分空切片和 nil，序列化 missing=[] 不能变成 null。

finally 清理每次发送缓冲并递减 active；成功和失败均增加 closed。替代实现可用 Go defer，但不能撤销此前已确认的包，不能把错误吞掉继续发送剩余包。接收端保存副本，清零临时缓冲不能把已接收数据清零。报告要解释字节副本所有权与异常后的计数。

## 补充边界计划

- `{"text":"","operations":[{"op":"send_all"},{"op":"commit"}]}`：0包、missing=[]、成功提交空数据、attempts=closed=0。
- `{"text":"a","chunk_size":1,"operations":[{"op":"send_all"},{"op":"commit"}]}`：单字节数组不是数字标量，包 hex=61。
- 正常发送后再发送相同 index 且 corrupt=true：PACKET_CONFLICT，原包保留且 buffer 关闭。
- 首次 corrupt=true 成功收包，commit 返回 DIGEST_MISMATCH；remove 后重发可恢复。
- cancel 清空内存包，后续 send／commit 返回 TRANSFER_CANCELLED。
- 文本长度限制使用 PowerShell/.NET UTF-16 长度，数据配额使用 UTF-8 字节数；Go 不应将二者都换成 rune 个数。

## 后续命令（仅获批隔离 VM）

Windows 源（cmd.exe；PowerShell 7.4+ 候选）：

```bat
pwsh -NoLogo -NoProfile -File source\exfiltration_lab.ps1 < fixtures\normal.json
pwsh -NoLogo -NoProfile -File source\exfiltration_lab.ps1 < fixtures\exception.json
```

Linux Go 目标，文件待生成：

```sh
go build -o target/exfiltration_lab target/exfiltration_lab.go
./target/exfiltration_lab < fixtures/normal.json
./target/exfiltration_lab < fixtures/exception.json
```

PowerShell 的 `<` 重定向在示例中由 cmd.exe 处理，不是在 PowerShell 交互提示符输入。两侧启动均不用 profile、不加载外部模块。当前状态见 [result.md](result.md)。
