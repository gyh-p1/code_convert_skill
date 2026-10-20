# 本轮交付记录：08 数据外传

日期：2026-10-20。范围：原创样本准备，非正式转换 run。

已交付并按文本核对：`source/exfiltration_lab.ps1`（503 物理行）、`fixtures/normal.json`、`fixtures/exception.json`、`fixtures/expected.json`、`README.md`、本记录。源 SHA-256 见 [DELIVERY.md](../DELIVERY.md)。

已审阅字节数组返回、UTF-8 分块、接收副本、失败 finally、缺包重试与提交摘要。建议 PowerShell→Go、Windows→Linux。收包是内存操作；不调用任何外部目标。

| 维度 | 本轮记录 |
|---|---|
| 样本交付完整性 | 源、2 输入、预期、说明已备齐 |
| 源语法／运行 | UNVERIFIED |
| 目标代码 | 未生成，本轮不适用 |
| 目标编译／链接／启动／功能等价 | UNVERIFIED |
| 命名／模块／战术保留 | 已说明连字符名称映射，效果 UNVERIFIED |
| 异常替代实现 | 已设计数组保持及缓冲清理观察点，效果 UNVERIFIED |
| 分类／隔离／清理证据 | 未取得 |

本轮使用 PowerShell 原生命令读取文本、计行和计算文件哈希，不曾加载／执行此 ps1 或调用其函数。没有源或目标运行证据。
