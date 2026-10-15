# 宿主文档验收记录

仅对 fixture 目录内的合成 Markdown 做加载验收，不是转换任务，不记 FROZEN、不分类、不提交 job。系统维护侧执行登记工具，当前会话通过实际工具返回取得九段正文，下面引用其原件。选择 batch 和 long-file 同时适用以验证集合并集；其余三种形态见文本回归。

```loading-preflight
{
  "taskId": "HOST-DOCUMENT-ACCEPTANCE",
  "runId": "20261015-001",
  "context": {"sessionId": "01a13dfd-ea47-7613-966e-518be3aa9725", "epoch": 0},
  "workflows": {
    "batch": {"applies": true, "basis": "合成验收形态：批量与长文件叠加，不是实际转换批次"},
    "long-file": {"applies": true, "basis": "合成验收形态：覆盖条件工作流并集"}
  },
  "structure": {"path": "structure-fixture-final.json", "sha256": "0d98ffe8a811865bda6cd87e31239cf00d83481ba58f5468ce3927550234d382"},
  "reads": [
    {"path": "receipt-fixture-state-002.json", "sha256": "330a397625849a15b4b286d3988d4481fec80ad8156287b2facc151c24d732ef"},
    {"path": "receipt-fixture-classifier-002.json", "sha256": "8ec627203d66cd7d5d180567eb22baf88b127477bce2920e7f4693c5f600f74e"},
    {"path": "receipt-fixture-build-002.json", "sha256": "2fc9f4872ae8421657fd3589271c3604879f595c1e07603fb7379ff68d43799f"},
    {"path": "receipt-fixture-loop-002.json", "sha256": "95abe58aeafd370717559ea53808371d1681ccb7b01d34f608515240bdcbf84b"},
    {"path": "receipt-fixture-evaluation-002.json", "sha256": "0d9e5ae92a9beaacce8ed43750940b30adfa37af6900ef047d813df8f4ad953d"},
    {"path": "receipt-fixture-delivery-002.json", "sha256": "303cabedadc821b10b42522d4009048a51ce2be84d872eeb5983f16a3c0a999f"},
    {"path": "receipt-fixture-safety-002.json", "sha256": "9ce67e612ba557da70bf3df69572c46863e20ea47b53b1bab896a1a952706cfd"},
    {"path": "receipt-fixture-batch-002.json", "sha256": "d778e34caa7c50b435fb2a32222474b8974fc808074238fbc0f15c5a99e1a9a7"},
    {"path": "receipt-fixture-long-002.json", "sha256": "296d9ec1ff9dea0f1630d1c47682d040a1aef012b84e3bc3c5416e1084016d83"}
  ]
}
```
