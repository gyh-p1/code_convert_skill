# 本轮交付记录：03 防御规避

日期：2026-10-20。范围：原创样本准备，非正式转换 run。

已交付并按文本核对：`source/encoding_lab.py`（503 物理行）、`fixtures/normal.json`、`fixtures/exception.json`、`fixtures/expected.json`、`README.md`、本记录。源 SHA-256 见 [DELIVERY.md](../DELIVERY.md)。

已审阅 Blob 表示、切片异常、配方原子回滚与保留 trace；补充 rotate、repeat、unique_bytes 和长度／表示断言操作。建议 Python→C++、Windows→Linux。压缩、Unicode 和 JSON 的目标依赖尚待生成时选定并离线冻结。

| 维度 | 本轮记录 |
|---|---|
| 样本交付完整性 | 源、2 输入、预期、说明已备齐 |
| 源语法／构建／运行 | UNVERIFIED |
| 目标代码 | 未生成，本轮不适用 |
| 目标编译／链接／启动／功能等价 | UNVERIFIED |
| 命名／模块／战术保留 | 已列要求；保留 legacy category／Stealth 口径，效果 UNVERIFIED |
| 异常替代实现 | 已设计负步长与零步长情景，效果 UNVERIFIED |
| 分类／隔离／清理证据 | 未取得 |

没有虚构的“已编译”或“已等价”结论；所有预期待后续外部评测核验。
