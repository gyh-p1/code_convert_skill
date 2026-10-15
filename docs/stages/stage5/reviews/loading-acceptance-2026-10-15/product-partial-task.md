# 产品正文部分读取反例

仅实际返回安全边界第 1–3 行，不能据此声称七份契约已完整提供。本记录预期 check-next 返回 coverage FAIL；不是转换冻结记录，也不执行任何转换。

```loading-preflight
{
  "taskId": "PRODUCT-PARTIAL-NEGATIVE",
  "runId": "20261015-001",
  "context": {"sessionId": "01a13dfd-ea47-7613-966e-518be3aa9725", "epoch": 0},
  "workflows": {
    "batch": {"applies": false, "basis": "一个静态文档反例任务"},
    "long-file": {"applies": false, "basis": "不处理源码或分段建图"}
  },
  "structure": {"path": "structure-product-verified.json", "sha256": "8000931d1d1abb3b5e1a1cd446ba895fcec5fbee2ceb4e0c6ab2d8d89597aa74"},
  "reads": [{"path": "receipt-safety-head-002.json", "sha256": "ca3a08231b4849c66c0cb7d333ba43fc24dacaa97e00c9d01a308f1d3e1ea173"}]
}
```
