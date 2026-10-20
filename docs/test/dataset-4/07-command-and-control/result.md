# 本轮交付记录：07 命令和控制

日期：2026-10-20。范围：原创样本准备，非正式转换 run。

已交付并按文本核对：`source/command_lab.rb`（501 物理行）、`fixtures/normal.json`、`fixtures/exception.json`、`fixtures/expected.json`、`README.md`、本记录。源 SHA-256 见 [DELIVERY.md](../DELIVERY.md)。

已审阅受限命令集合、租约状态机、ensure 清理、重试上限和 unregister。建议 Ruby→C、Linux→Windows。只模拟队列；未生成服务端、客户端或远程执行程序。C 工程的 JSON 实现、依赖与构建命令待正式转换确定。

| 维度 | 本轮记录 |
|---|---|
| 样本交付完整性 | 源、2 输入、预期、说明已备齐 |
| 源语法／运行 | UNVERIFIED |
| 目标代码 | 未生成，本轮不适用 |
| 目标编译／链接／启动／功能等价 | UNVERIFIED |
| 命名／模块／战术保留 | 已说明 terminal? 等必要改名，效果 UNVERIFIED |
| 异常替代实现 | 已设计 ensure→清理出口观察点，效果 UNVERIFIED |
| 分类／隔离／清理证据 | 未取得 |

没有 Ruby 语法检查或 C 构建证据；expected 值是设计预期。
