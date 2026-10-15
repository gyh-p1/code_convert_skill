# 人工核对与工具核对的同材料比较

2026-10-15。人工回读 fixture/SKILL.md、实际返回的九段正文及 offer/receipt 元数据，再对照工具输出。变量仅为记录/核对方法；不执行样本，不更换文档内容。该比较规模小且人工由同一开发 Agent 完成，不能证明独立第三方遵守率或效率提升。

| 相同输入/边界 | 人工判断及依据 | 工具结果 |
|---|---|---|
| fixture 七契约及 batch、long-file，九份均为完整 3 行 | 根表七个精确身份、两个条件工作流均在；九份实际返回范围 1–3、lineCount=3，版本匹配，全部在本次下一动作核对前返回，加载完整 | next-fixture-final.json：PASS，selected=9 |
| 产品正文只提供 safety 1–3 行 | safety 本身共 36 行，其余六份无本路径完整提供凭证；不能记七契约加载完整 | next-product-partial-verified.json：FAIL，七项 coverage |
| 同一九段 fixture 正文，但审计边界移到提供它们的调用之前 | 所有返回均在该边界之后；当前完整不能追认历史建图前已读 | next-fixture-late-final.json：FAIL，九项 late-read 及九项 coverage |
| fixture safety 返回人为限制展示预算 | 最终显示正文 JSON 不完整，后台 offer 存在不能证明提供完成 | host-truncation-001.log：UNAVAILABLE，未生成 receipt-host-truncated.json |

本组 4 个场景的判定一致，无观察到的误报/漏报；只支持这四个场景，不外推整体错误率。原人工材料不含每段精确工具关联和字节覆盖计算，系统记录补充了这些可复核信息。

成本记录：九段正文提供在同一次宿主调用中通过九个独立系统读取命令完成；工具返回的各命令 wall_time_seconds 约 1.43–1.74 秒（相互重叠，不能相加当总耗时）。随后九次逐件关联最终凭证约 0.78–1.47 秒/件；完整下一动作检查约 1.67 秒，均可从本会话实际返回回读。人工核对未单独计时，不计算加速比；因此效率改善仍无对照证据。此组无补读；另一次产品读取命令因混有额外输出重发，旧 offer 保留，体现原样返回的使用约束。

重复提供、版本变更、换会话、已知压缩、分段中段遗漏、落盘失败及 manual 降级的注入用例由 loading-tests-final.log 覆盖。人工回退使用原生读取和文字说明，不要求第三方智能体执行本工具；无独立日志时只声明人工依据，不伪记 HOST_RETURN_OBSERVED。
