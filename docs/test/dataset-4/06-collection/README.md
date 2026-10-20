# 06 信息收集：虚拟文档暂存

源：`source/collection_lab.cs` 和 `source/collection_lab.csproj`；建议 C# → PowerShell，Windows → Linux。`/lab/a` 是字典键，不是实际文件路径；输入中的合成文本由程序暂存在内存，不读取磁盘。

保留 `collection_lab`、`CollectionLab`、`VirtualDocument`、`VirtualRepository`、`CollectionSession`、`ReadCandidates`、`Collect`、`Stage`、`Manifest`、`Program.Simulate`、Collection／TA0009。项目文件是源码构建描述，不是额外样本。保留验证／文档模型／迭代收集／入口职责，JSON 字段名不变。

## 必测情景

| 输入 | 预期行为 |
|---|---|
| `fixtures/normal.json` | 猫占 UTF-8 3 字节，ab 占2；quota=5 恰好成功；manifest bytes=5、generation=2，reader 关闭 |
| `fixtures/exception.json` | 首个 Stage 完成后失败，atomic=true 撤销暂存和 generation；manifest 为空；随后 limit=1 成功，最终 bytes=3、generation=1 |

两个情景退出 0、stderr 空，关键断言见 `fixtures/expected.json`。异常情景两次读枚举结束后 active_readers=0、closed_readers=2。

## 非直接映射与异常处理

定位：`VirtualRepository.ReadCandidates` 的 `yield return/finally`，`CollectionSession.Collect` 的 foreach 提前退出和 catch 回滚。PowerShell pipeline 不是 C# IEnumerable 的自动 Dispose 协议；应采用明确边界的枚举过程，并在 finally 中关闭一次 reader。

不能因 PowerShell 函数默认输出中间表达式，把计数器、列表 Add 结果或清理返回值混入 stdout；输出只能有最终 JSON。源码的字节配额按 UTF-8 计算，而非 `.Length` 字符数。原子失败恢复暂存集合／generation，但 reader 审计关闭记录仍保留。

## 补充边界计划

- normal 输入 quota 改4：第二份文档使 QUOTA_EXCEEDED；atomic 默认 true，第一份也回滚。
- 同一情景显式 atomic=false：第一份保留3字节，generation=1；错误照常报告。
- `{"documents":[],"operations":[{"op":"collect","limit":0}]}`：不启动 reader，closed=0。
- 虚拟路径 `/lab/../x` 或 Windows 风格反斜线：VIRTUAL_PATH，禁止转换时调用系统路径归一化改变该规则。
- readable=false 的文档触发 READ_DENIED；不可自动跳过并报告完整成功。
- 源使用 Ordinal 排序，PowerShell 的默认文化排序／不区分大小写不得替代。

## 后续命令（仅获批隔离 VM）

Windows 源（cmd.exe，SDK 8 离线预置）：

```bat
dotnet build source\collection_lab.csproj -c Release
dotnet source\bin\Release\net8.0\collection_lab.dll < fixtures\normal.json
dotnet source\bin\Release\net8.0\collection_lab.dll < fixtures\exception.json
```

Linux PowerShell 7 目标，文件待生成：

```sh
pwsh -NoLogo -NoProfile -File target/collection_lab.ps1 < fixtures/normal.json
pwsh -NoLogo -NoProfile -File target/collection_lab.ps1 < fixtures/exception.json
```

Linux 上同样需要保留虚拟路径规则，不能借 `/lab` 字样创建真实目录。PowerShell 语法检查由平台提供，只在隔离环境做。当前状态见 [result.md](result.md)。
