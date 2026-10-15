# 加载工具验收原件

本目录保存系统维护侧开发与验收原件，不进入产品加载链。fixture/ 是合成 Markdown 树，不是源码或实际转换任务；document-task.md 的任务身份仅用于宿主集成测试，不记真实 FROZEN/分类/job。

当前适用原件：

- `structure-product-verified.json`：最终产品 12 份正文静态结构，范围内 PASS。
- `structure-fixture-final.json`：当前工具版本对应的合成树结构，PASS。
- `receipt-fixture-*-002.json`：九份合成文档的真实宿主返回证据；offer-fixture-*.json 保存当次精确正文。
- `receipt-safety-head-002.json`：产品 safety 1–3 行真实返回，覆盖仅为片段。
- `document-task.md`、`next-fixture-final.json`：九份合成文档完整加载的真实宿主闭环，PASS。
- `product-partial-task.md`、`next-product-partial-verified.json`：产品部分读取应拒绝，FAIL 是预期结果。
- `next-fixture-late-final.json`：既有动作边界之前未提供，应拒绝，FAIL 是预期结果。
- `offer-host-truncated.json`、`host-truncation-001.log`：真实宿主截断，记录命令 exit 2；不存在 receipt-host-truncated.json 是正确行为。
- `next-cleanup-final.json`：缺加载件仍允许沿既有 job 清理的加载例外，非执行授权。
- `loading-tests-final.log`：最终组件回归原始输出；`classifier-baseline-001.log`：未修改的安全分类器回归失败原文。
- `manual-comparison.md`：同材料人工与工具核对，含小样本限制和成本记录。

其余无 final/verified 或无 002 后缀的同类原件是开发中间版本，保留以说明发现与修订，不作为当前通过依据。document-task.md 和 product-partial-task.md 保留当前指针，历史 next 原件包含当次记录摘要；不能用当前任务说明反推过去检查。

宿主证据引用本会话原始 rollout 的绝对路径、前缀摘要和调用标识，未将含无关上下文的整份个人会话日志复制入仓库。原日志须按本任务记录保留；移交到另一主机时，需由系统受控移交对应原日志并重新核指针，不能编辑 receipt 指针后继续宣称原件完整。单元 fixture 日志是合成输入，真实宿主凭证仅限上列实际返回。
