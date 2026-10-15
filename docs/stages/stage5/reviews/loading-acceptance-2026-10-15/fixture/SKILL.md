# Synthetic Loading Fixture

This table is test data, not a product loading entry.

| 契约标识 | 必读真源 | 负责什么 | 何时消费 |
|---|---|---|---|
| task-state | [State](references/framework/task-state-contract.md) | fixture | before |
| classifier | [Classifier](references/workflow/classifier-agent-gate.md) | fixture | before |
| build | [Build](references/workflow/build-prerequisites.md) | fixture | before |
| loop | [Loop](references/workflow/conversion-evaluation-loop.md) | fixture | before |
| evaluation | [Evaluation](references/framework/evaluation-readiness-contract.md) | fixture | before |
| delivery | [Delivery](references/framework/delivery-handoff-contract.md) | fixture | before |
| safety | [Safety](references/framework/safety-boundary.md) | fixture | before |

[Batch](skills/workflows/batch-conversion/SKILL.md).
[Long File](skills/workflows/long-file-conversion/SKILL.md).
