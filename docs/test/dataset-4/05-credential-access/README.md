# 05 凭证访问：合成记录租约

源：`source/credential_lab.go`；建议 Go → Python，Linux → Windows。只访问输入内 `fixture:` 前缀的虚构 secret；不接触浏览器、系统密钥链或其他凭证存储。secret 仅用于内存相等比较，报告固定脱敏。

保留 `credential_lab`、`CredentialRecord`、`CredentialVault`、`Lease`、`acquire`、`release`、`inspect`、`compare`、`simulate`、Credential Access／TA0006。输入验证／记录与租约／操作分派／输出模块保持可定位。Go 大写字段映射到 Python 时保留名字或提供映射，JSON 字段必须完全保留。

## 必测情景

| 输入 | 预期行为 |
|---|---|
| `fixtures/normal.json` | inspect 和两次 compare 共关闭三个租约；rotate 后 version=1；两次 compare 均 true；报告不含 secret 原值 |
| `fixtures/exception.json` | acquire 后立即失败，defer 仍 release；后续 compare 可用；active_leases=0、closed_leases=2 |

`fixtures/expected.json` 定义关键字段；正常和异常输入均预期退出 0、stderr 空。输出不可出现 fixture:one／fixture:two 原值，但 `synthetic_bytes=11` 是预期信息。

## 非直接映射与异常处理

定位：`CredentialVault.inspect` 与 `compare` 的 `defer vault.release(lease)`，错误返回值 `(any, error)`。Python 没有 Go defer 的函数返回清理机制；使用 `try/finally` 或已明确实现退出协议的上下文对象。只有 acquire 成功后才能注册 release，失败前不得增加 closed 计数。

Go `(nil,error)` 映射成 Python 异常或结果对象均可，但外围必须形成同样的 error code／field，不能输出 null result 代替业务错误。release 清空临时字节数组并更新计数，不删除 vault 中的合成记录。清零语句不代表物理内存安全擦除，报告不要扩大结论。

## 补充边界计划

- records=[]、operations=[]：records/audit/outcomes 均为 JSON 空数组，不是 null。
- secret="real-looking-value"：初始化错误 SYNTHETIC_SECRET_REQUIRED／secret，退出 2。
- expires=0 后 inspect：RECORD_EXPIRED，active=closed=0。
- rotate expected 不匹配：VERSION_CONFLICT；原 secret 仍能 compare 成功。
- integerValue 只接受整数字面量；`1.0` 或 `true` 不能在迁移中被静默接受。
- 原 Go JSON 解码器对重复对象键保留最后值；若追加重复键测试，Python 目标须按源保持，而非照搬其他 Python 样本的拒绝策略。

## 后续命令（仅获批隔离 VM）

Linux 源，Go 标准库即可，无 go.mod 或网络依赖：

```sh
go build -o credential_lab source/credential_lab.go
./credential_lab < fixtures/normal.json
./credential_lab < fixtures/exception.json
```

Windows Python 目标（cmd.exe，待生成）：

```bat
python target\credential_lab.py < fixtures\normal.json
python target\credential_lab.py < fixtures\exception.json
```

目标语法检查命令由获批平台在隔离环境提供；本机不调用 py_compile 或 AST 解析。当前状态见 [result.md](result.md)。
