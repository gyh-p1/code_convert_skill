# 本轮交付记录：06 信息收集

日期：2026-10-20。范围：原创样本准备，非正式转换 run。

已交付并按文本核对：`source/collection_lab.cs`（542 物理行）、`source/collection_lab.csproj`、`fixtures/normal.json`、`fixtures/exception.json`、`fixtures/expected.json`、`README.md`、本记录。源与项目 SHA-256 见 [DELIVERY.md](../DELIVERY.md)。

已审阅 UTF-8 字节配额、Ordinal 路径排序、迭代器 finally、原子恢复与再次 collect。建议 C#→PowerShell、Windows→Linux。项目只包含指定源文件，无外部 NuGet 包声明；实际 SDK 构建仍未验证。

| 维度 | 本轮记录 |
|---|---|
| 样本交付完整性 | 源、工程描述、2 输入、预期、说明已备齐 |
| 源编译／链接／运行 | UNVERIFIED |
| 目标代码 | 未生成，本轮不适用 |
| 目标语法／启动／功能等价 | UNVERIFIED |
| 命名／模块／战术保留 | 已列要求，效果 UNVERIFIED |
| 异常替代实现 | 已设计枚举释放及回滚观察点，效果 UNVERIFIED |
| 分类／隔离／清理证据 | 未取得 |

本轮未调用 dotnet、编译器、语法解析或 PowerShell 样本执行；未产生评测 job。
