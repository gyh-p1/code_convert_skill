# 02 提权：虚拟身份作用域

源：`source/privilege_lab.py`；建议 Python → C#，Linux → Windows。虚拟 token 是 JSON 数据，只授权访问虚拟资源；不读取或改变 OS 身份，没有漏洞或系统令牌操作。

保留 `privilege_lab`、`Capability`、`VirtualToken`、`VirtualResource`、`PrivilegeModel`、`impersonate`、`authorize`、`dispatch`、`simulate`、`Privilege Escalation`、TA0004。维持验证／数据模型／授权与作用域／JSON 入口的模块边界。目标需要完整 `.csproj` 和入口，不交付孤立类片段。

## 必测情景

| 输入 | 预期行为 |
|---|---|
| `fixtures/normal.json` | 在 elevated 作用域写 note=v1；退出作用域后 identity=base，scope_depth=0；后续读到 v1/version=1 |
| `fixtures/exception.json` | 写入成功后注入异常；作用域恢复 base，但 v1 不回滚；base 再写失败 ACCESS_DENIED；读仍得 v1 |

两次进程预期退出 0、stderr 空；关键 JSON Pointer 断言见 `fixtures/expected.json`。

## 非直接映射与异常处理

定位：`PrivilegeModel.impersonate` 的 `contextmanager`／`finally`，`dispatch` 的递归 scope 和 `fail_after`。C# 可用显式 `try/finally` 或自定义 `IDisposable` 保存／恢复 previous token；普通 `using` 本身不自动完成源的身份堆栈语义。

无论异常或正常路径都要先记录 leave，再恢复前一身份；内层异常逐层清理。此处不是事务，成功写入必须保留。不得误套第 01 例回滚，也不能在失败后继续保持 elevated。将 IntFlag 映射到 `[Flags]` 或整数掩码时保持 deny 优先和 capability 的固定顺序。

## 补充边界计划

- 给资源 deny=["write"]：即使 elevated 有 write，也须 EXPLICIT_DENY。
- scope token 不存在：TOKEN_NOT_FOUND，不产生 enter／leave。
- advance 到 expires 的精确时刻：TOKEN_EXPIRED；`tick >= expires` 不能改成 `>`。
- delegate 请求超出父 token 的能力／寿命：CAPABILITY_AMPLIFICATION／EXPIRY_AMPLIFICATION。
- 嵌套 scope 正常返回与失败均检查 identity、scope_depth 和审计顺序。

## 后续命令（仅获批隔离 VM）

Linux 源：

```sh
python3 source/privilege_lab.py < fixtures/normal.json
python3 source/privilege_lab.py < fixtures/exception.json
```

Windows 目标计划（cmd.exe，目标项目待生成）：

```bat
dotnet build target\privilege_lab.csproj -c Release
dotnet target\bin\Release\net8.0\privilege_lab.dll < fixtures\normal.json
dotnet target\bin\Release\net8.0\privilege_lab.dll < fixtures\exception.json
```

项目应固定 AssemblyName=privilege_lab，依赖与 SDK 预置离线。目标系统为 Windows 不代表应调用 Windows 身份 API。当前状态见 [result.md](result.md)。
