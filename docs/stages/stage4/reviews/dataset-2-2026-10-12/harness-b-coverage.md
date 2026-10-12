# DeepSeek harness B 覆盖清单（D2-081–D2-160）

> 状态：**COMPLETE**（79/79 项逐项审阅完成；D2-081–D2-160 逐项文件清单已按独立 `glob` 回填；未读集合为空；审计差异 19 条已登记）
> 范围：`docs/dataset-2/dataset-2-copy/manifest.csv` 中 D2-081 至 D2-160。
> 范围核对：该区间 manifest 实际只有 **79 行**——**D2-113 不在 manifest 中**（第112行 D2-112 之后直接是 D2-114）。用户口径“80项”按 Id 区间计；本清单按实际存在的 79 项逐项登记，并单列 D2-113 缺失。
> 边界：纯静态文本审阅，不编译/不运行/不调用模型/不提交/不访问 Controller；原源与目标已删除，缺件如实登记、不复原。
> 逐项证据见 `harness-b-cases-01.md`…`04.md`；跨项发现见 `harness-b-findings.md`。

## 工具与环境限制（影响“已读”判据）

1. **PowerShell 不可用**：本会话 `pwsh` 沙箱在授予工作区写权限时报 Windows 错误（`SetNamedSecurityInfoW failed (Win32 5)`），且 `danger-full-access` 升级无审批通道，故 `Get-Content`/目录枚举不可用。全部工作改用原生文件工具（`read`/`glob`/`grep`）完成，等价于“只用原生文件工具、rg 手工分段阅读”。
2. **单行超长文本被工具截断**：`read` 与 `grep` 对**同一行**的输出都截断在约 2000 字符（显示 `line truncated to 2000 chars`）。**单行**证据文件（`evidence-*.json`、`comparison.json`、`evaluation_report.json`、`metadata.json`、`input_profile.json`、`comparison_manifest.json`、`evaluator_manifest.json`、`classifier-input.json`、`classification-*.json`、`this-task-classification.json`、`batch-authorization.json`、`controller-health-*.json`、`runners-before.json`）第 2000 字符之后的内容用本会话工具**无法读取**。凡此情形标 `已读(截断)/可见部分（工具2000字符/行截断）`，并尽力用分段 `grep` 提取靠前字段；不得据此声称已读全文。**实测澄清**：(a) `batch/items/*.json` 为**多行**美化 JSON（31–81 行），本区间 79/79 完整可读，**不受**该限制；(b) **同一文件名在不同项可能是单行、也可能是美化多行**——例如 `comparison_manifest.json` 在 D2-155 job-00b 为 20 行美化 JSON（全文可读），在其它项为单行；`frozen-inputs.md`/`classification-*.json` 同样有 30 行与 169 行两种规模。故“已读/已读(截断)”必须**逐项**判定。
3. 多行文件（`frozen-inputs.md`、`request.system.txt`、`repair*.system.txt`、`review.system.txt`、`self-review-*.json`、`evaluation_report.md`、`result.md`、`controller.log`、`observed-source-*.txt`、`batch/items/*.json`）可完整读取。**`target.gen.model.json` 有两种形制，不能一律当元数据**：① 调用元数据（无 `content`，如 D2-151 实测 24 行）；② **原始模型响应正文** `{"role":"assistant","content":"```…```"}`（含目标代码，如 D2-123、D2-109 实测）。逐项打开判定。

## 覆盖统计（滚动）

| 指标 | 数量 |
|---|---|
| 冻结范围内 manifest 行 | 79 |
| 已登记项（本文件已列实际目录） | 79 |
| 本文件已按 glob 回填项 | **79**（D2-081–D2-160，无 D2-113） |
| 现存文件合计（全区间 glob 实测） | **1393**（第一段 770 + 第二段 623） |
| 已读合计（取自 cases 表） | **1265**（第一段 718 + 第二段 547） |
| 已读(截断)合计（取自 cases 表） | **198**（第一段 134 + 第二段 64） |
| 未读合计（取自 cases 表） | **0** |
| 空文件（合法 0 字节采集件） | **8**：D2-102、109、111、116、117、118、126、133（D2-126 在 cases-03 覆盖表计 0，其记录另注明该文件为合法 0 字节） |
| 缺件 | 逐项见四份 cases 文件与 `harness-b-findings.md` §3/§3bis/§3ter/§3quater |
| 无任何过程材料的项 | 5（D2-156、D2-157、D2-158、D2-159、D2-160） |
| 审计差异项（glob 计数 ≠ cases 表计数） | **19**（第一段 13 + 第二段 6） |
| 完整审阅完成 | **79 / 79** |

> 本表「现存文件合计」与「审计差异」均以本次逐项 `glob docs/dataset-2/dataset-2-copy/*/D2-0NN-*/**/*` 的实测结果为唯一权威清单；cases 表的“现存”列仅作对照，不作为计数依据。

## 逐项文件清单（D2-081–D2-120，计数以 glob 为准）

### D2-081 ｜ cpp-to-csharp ｜ 现存 11 ｜ 已读 11 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-csharp/D2-081-cpp-str_cat.cc/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evidence-source.json`

### D2-082 ｜ cpp-to-go ｜ 现存 18 ｜ 已读 18 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 8
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-082-cpp-t1218.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evidence-source.json`
- `04-evaluation/job-00b-source-buildability-corrected-command/`：`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`
  - `returned-evidence/`：`evidence-source.json`

### D2-083 ｜ cpp-to-go ｜ 现存 3 ｜ 已读 3 ｜ 已读(截断) 0 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-083-cpp-cppwsmanwinrm.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`

### D2-084 ｜ cpp-to-go ｜ 现存 13 ｜ 已读 13 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-084-cpp-civil_time.cc/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evidence-source.json`

### D2-085 ｜ cpp-to-go ｜ 现存 13 ｜ 已读 13 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-085-cpp-match.cc/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evidence-source.json`

### D2-086 ｜ cpp-to-go ｜ 现存 13 ｜ 已读 13 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-086-cpp-str_split.cc/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evidence-source.json`

### D2-087 ｜ cpp-to-go ｜ 现存 11 ｜ 已读 11 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 5
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-go/D2-087-cpp-substitute.cc/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evidence-source.json`

### D2-088 ｜ cpp-to-powershell ｜ 现存 40 ｜ 已读 40 ｜ 已读(截断) 7 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 10
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-088-cpp-safe_attck_cpp_suite-resource_manifest_builder.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/`：`request.system.txt`、`target.gen.model.json`、`target.self-repair-1.model.json`、`target.self-repair-1.proposal.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.md`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.md`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-089 ｜ cpp-to-powershell ｜ 现存 23 ｜ 已读 23 ｜ 已读(截断) 4 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 9
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-089-cpp-shell-aes.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-00b-fpermissive/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`

### D2-090 ｜ cpp-to-powershell ｜ 现存 13 ｜ 已读 13 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 6
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-090-cpp-env_detect.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`

### D2-091 ｜ cpp-to-powershell ｜ 现存 42 ｜ 已读 38 ｜ 已读(截断) 5 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 8
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-091-cpp-process_enum.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`request.system.txt`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-00b-argv-refreeze/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-092 ｜ cpp-to-powershell ｜ 现存 47 ｜ 已读 49 ｜ 已读(截断) 7 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 8
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-092-cpp-winhttp_impl.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`repair.system.txt`、`request.system.txt`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-02-dual-build-eval-repair-1/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-093 ｜ cpp-to-powershell ｜ 现存 48 ｜ 已读 53 ｜ 已读(截断) 8 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 8
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-093-cpp-inject_channel.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`repair.system.txt`、`repair2.system.txt`、`request.system.txt`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-02-dual-build-eval-repair-2/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-094 ｜ cpp-to-powershell ｜ 现存 1 ｜ 已读 1 ｜ 已读(截断) 0 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 5
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-powershell/D2-094-cpp-screenshot.cpp/output/batch`
- `01-frozen/`：`frozen-inputs.md`

### D2-095 ｜ cpp-to-python ｜ 现存 32 ｜ 已读 37 ｜ 已读(截断) 5 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 8
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-095-cpp-safe_attck_cpp_suite-local_c2_retry.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`request.system.txt`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-096 ｜ cpp-to-python ｜ 现存 32 ｜ 已读 36 ｜ 已读(截断) 8 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 8
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-096-cpp-safe_attck_cpp_suite-collection_bundle.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`request.system.txt`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-097 ｜ cpp-to-python ｜ 现存 32 ｜ 已读 45 ｜ 已读(截断) 8 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 8
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-097-cpp-evil_inj.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`request.system.txt`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-098 ｜ cpp-to-python ｜ 现存 1 ｜ 已读 1 ｜ 已读(截断) 0 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 5
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-098-cpp-evil1.cpp/output/batch`
- `01-frozen/`：`frozen-inputs.md`

### D2-099 ｜ cpp-to-python ｜ 现存 1 ｜ 已读 1 ｜ 已读(截断) 0 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 5
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-099-cpp-processfind.cpp/output/batch`
- `01-frozen/`：`frozen-inputs.md`

### D2-100 ｜ cpp-to-python ｜ 现存 13 ｜ 已读 14 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 7
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-100-cpp-encode.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`

### D2-101 ｜ cpp-to-python ｜ 现存 1 ｜ 已读 1 ｜ 已读(截断) 0 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-python/D2-101-cpp-hooking.cpp/output/batch`
- `01-frozen/`：`frozen-inputs.md`

### D2-102 ｜ cpp-to-ruby ｜ 现存 13 ｜ 已读 10 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 1 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-ruby/D2-102-cpp-dllmain-dllmain.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability-windows/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`evaluation_report.json`、`evidence-source.json`
- `04-evaluation/job-00b-source-buildability-contract-corrected/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`evaluation_report.json`、`evidence-source.json`

### D2-103 ｜ cpp-to-ruby ｜ 现存 30 ｜ 已读 19 ｜ 已读(截断) 10 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-ruby/D2-103-cpp-safe_attck_cpp_suite-host_env_snapshot.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `03-self-review/`：`self-review-1.json`
- `04-evaluation/job-00-source-buildability-linux/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`evaluation_report.json`、`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`attribution.md`、`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-02-balanced-entries/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`result.md`

### D2-104 ｜ cpp-to-ruby ｜ 现存 19 ｜ 已读 16 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-ruby/D2-104-cpp-safe_attck_cpp_suite-reversible_rename.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `03-self-review/`：`self-review-1.json`
- `04-evaluation/job-00-source-buildability-linux/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`evaluation_report.json`、`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`result.md`

### D2-105 ｜ cpp-to-ruby ｜ 现存 19 ｜ 已读 15 ｜ 已读(截断) 4 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-ruby/D2-105-cpp-safe_attck_cpp_suite-rollback_rename_cycle.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `03-self-review/`：`self-review-1.json`
- `04-evaluation/job-00-source-buildability-linux/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`evaluation_report.json`、`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`result.md`

### D2-106 ｜ cpp-to-ruby ｜ 现存 19 ｜ 已读 17 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-ruby/D2-106-cpp-safe_attck_cpp_suite-collection_manifest.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `03-self-review/`：`self-review-1.json`
- `04-evaluation/job-00-source-buildability-linux/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`evaluation_report.json`、`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`result.md`

### D2-107 ｜ cpp-to-ruby ｜ 现存 12 ｜ 已读 11 ｜ 已读(截断) 0 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-ruby/D2-107-cpp-cartoon.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability-windows/`：`comparison_manifest.json`、`input_profile.json`、`metadata.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`

### D2-108 ｜ cpp-to-ruby ｜ 现存 3 ｜ 已读 4 ｜ 已读(截断) 0 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/cpp-to-ruby/D2-108-cpp-shell.cpp/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`

### D2-109 ｜ csharp-to-c ｜ 现存 53 ｜ 已读 40 ｜ 已读(截断) 10 ｜ 未读 0 ｜ 空文件 1 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-c/D2-109-cs-.upstream-sharpup-sharpup-utilities-fileutils.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classification-2.json`、`classification-3.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-00b-source-buildability-net48/`：`job-id.txt`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-00c-source-buildability-net48/`：`job-id.txt`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-110 ｜ csharp-to-c ｜ 现存 11 ｜ 已读 11 ｜ 已读(截断) 0 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-c/D2-110-cs-hashcode.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evaluation_report.md`、`evidence-source.json`

### D2-111 ｜ csharp-to-c ｜ 现存 33 ｜ 已读 25 ｜ 已读(截断) 8 ｜ 未读 0 ｜ 空文件 1 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-c/D2-111-cs-pe.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evaluation_report.md`、`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-1state-devicefault.json`、`job-id2.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-112 ｜ csharp-to-c ｜ 现存 11 ｜ 已读 9 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-c/D2-112-cs-random.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evaluation_report.md`、`evidence-source.json`

### D2-113 ｜ **不在 manifest**（Id 区间缺号，非缺件）
- 本清单按用户「80 项」的口径不为其建项：manifest 第 112 行 `D2-112` 之后直接是 `D2-114`。
- glob `docs/dataset-2/dataset-2-copy/*/D2-113-*/**/*` **无任何结果**，副本内不存在该 Id 的实际目录，故既无「现存」计数也无缺件。

### D2-114 ｜ csharp-to-c ｜ 现存 11 ｜ 已读 9 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-c/D2-114-cs-boolean.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classification-2.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`

### D2-115 ｜ csharp-to-c ｜ 现存 10 ｜ 已读 8 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-c/D2-115-cs-mathf.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`

### D2-116 ｜ csharp-to-cpp ｜ 现存 32 ｜ 已读 24 ｜ 已读(截断) 8 ｜ 未读 0 ｜ 空文件 1 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-cpp/D2-116-cs-.upstream-redteamtest-backup-processdllhijack.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classification-2.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`job-id2.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-117 ｜ csharp-to-cpp ｜ 现存 33 ｜ 已读 25 ｜ 已读(截断) 8 ｜ 未读 0 ｜ 空文件 1 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-cpp/D2-117-cs-.upstream-redteamtest-backup-cachedgpppassword.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-after.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-118 ｜ csharp-to-cpp ｜ 现存 31 ｜ 已读 23 ｜ 已读(截断) 8 ｜ 未读 0 ｜ 空文件 1 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-cpp/D2-118-cs-.upstream-redteamtest-backup-modifiableservices.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-after.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-119 ｜ csharp-to-cpp ｜ 现存 11 ｜ 已读 9 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-cpp/D2-119-cs-.upstream-redteamtest-backup-unquotedservicepath.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-120 ｜ csharp-to-cpp ｜ 现存 11 ｜ 已读 9 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-cpp/D2-120-cs-binarylauncher.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

## 审计差异（glob 计数 vs cases 表计数）

本 40 项中，**13 项**的 glob 实测计数与 `harness-b-cases-01.md` / `harness-b-cases-02.md` 覆盖表的「现存文件数」列不相等（其余 27 项相等，未列）。计数以本次 glob 为准。

| 项 | glob 计数 | cases 表计数 | 差 |
|---|---|---|---|
| D2-091 | 42 | 38 | +4 |
| D2-092 | 47 | 49 | −2 |
| D2-093 | 48 | 53 | −5 |
| D2-095 | 32 | 37 | −5 |
| D2-096 | 32 | 36 | −4 |
| D2-097 | 32 | 45 | −13 |
| D2-100 | 13 | 14 | −1 |
| D2-102 | 13 | 12 | +1 |
| D2-103 | 30 | 29 | +1 |
| D2-104 | 19 | 18 | +1 |
| D2-107 | 12 | 11 | +1 |
| D2-108 | 3 | 4 | −1 |
| D2-109 | 53 | 50 | +3 |

- 40 项 glob 合计 **770**；cases 表对应合计 **790**；差值 **−20**，与上表逐条差值之和一致。
- 任务书已预告的三处（D2-091、D2-093、D2-095）自报有误，本 glob 与任务书给出的真值完全一致（42 / 48 / 32）；其余 10 处差异为本轮新发现，一并列出。
- 差异方向的含义：`+`＝cases 表少记（文件实际存在）；`−`＝cases 表多记（副本内没有那么多文件，含已删件被计入的情形）。本清单不回填、不删改 cases 文件。

## 未读集合

本区间（D2-081–D2-120，40 项）未读集合为空：40 项 `未读` 列合计为 **0**。逐项判定见 `harness-b-cases-01.md` / `harness-b-cases-02.md`。

## 附注

- 逐件读取状态（哪一件是“已读(截断)”、哪一件是 0 字节空原件）逐项见 `harness-b-cases-01.md` / `harness-b-cases-02.md` 的对应记录；本清单的“已读/截断”计数取自该两文件的覆盖表。
- 本清单所有“现存 N”与文件名清单均来自本次逐项 `glob docs/dataset-2/dataset-2-copy/*/D2-0NN-*/**/*` 的实测；glob 只返回文件、不返回目录，故“现存 N”＝该用例 `output/batch` 树内实际文件件数（不含空目录）。上表差异中的 `+` 项说明副本内仍有 cases 表未记的现存文件；`−` 项说明 cases 表把副本内不存在的件也计入了现存数。

## 进度日志

- 2026-10-12：建立清单（IN_PROGRESS）；保留“工具与环境限制”3 条；范围 79 项（D2-113 不在 manifest）。
- 2026-10-12（前 40 项）：D2-081–D2-120 文件清单按 glob 回填完成；现存合计 770；计数与 cases 表差异 13 条见上；未读集合为空。

## 逐项文件清单（D2-121–D2-160，计数以 glob 为准）

### D2-121 ｜ csharp-to-cpp ｜ 现存 12 ｜ 已读 10 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-cpp/D2-121-cs-stack.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classification-2.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-122 ｜ csharp-to-cpp ｜ 现存 12 ｜ 已读 10 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-cpp/D2-122-cs-version.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classification-2.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-123 ｜ csharp-to-go ｜ 现存 30 ｜ 已读 23 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 `frozen-inputs.md`、根级 `target.go`
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-go/D2-123-cs-.upstream-redteamtest-backup-registryautoruns.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-124 ｜ csharp-to-go ｜ 现存 30 ｜ 已读 27 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 `frozen-inputs.md`、根级 `target.go`
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-go/D2-124-cs-.upstream-redteamtest-backup-alwaysinstallelevated.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-125 ｜ csharp-to-go ｜ 现存 30 ｜ 已读 26 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 `frozen-inputs.md`、根级 `target.go`
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-go/D2-125-cs-.upstream-redteamtest-backup-hijackablepaths.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-126 ｜ csharp-to-go ｜ 现存 30 ｜ 已读 27 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 1（`02-conversion/observed-source-stderr.txt`，合法 0 字节采集件） ｜ 缺件 `frozen-inputs.md`、根级 `target.go`
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-go/D2-126-cs-.upstream-redteamtest-backup-tokenprivileges.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-127 ｜ csharp-to-go ｜ 现存 11 ｜ 已读 9 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-go/D2-127-cs-.upstream-sharpup-sharpup-program.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-128 ｜ csharp-to-go ｜ 现存 33 ｜ 已读 31 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 根级 `target.go`；另缺 `02-conversion/request.system.txt`
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-go/D2-128-cs-.upstream-sharpup-sharpup-utilities-registryutils.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classification-2.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`job-id-cs5001.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`、`evidence-source-cs5001.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-129 ｜ csharp-to-go ｜ 现存 11 ｜ 已读 8 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 见下
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-go/D2-129-cs-index.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-130 ｜ csharp-to-powershell ｜ 现存 31 ｜ 已读 27 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 根级 `target.ps1`
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-powershell/D2-130-cs-.upstream-redteamtest-backup-unattendedinstallfiles.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-131 ｜ csharp-to-powershell ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 不适用（非可转换去向）；job-00 无 report/controller.log/health/capsule
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-powershell/D2-131-cs-.upstream-sharpup-sharpup-checks-modifiableservices.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-132 ｜ csharp-to-powershell ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 同 D2-131
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-powershell/D2-132-cs-.upstream-sharpup-sharpup-checks-processdllhijack.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-133 ｜ csharp-to-powershell ｜ 现存 30 ｜ 已读 23 ｜ 已读(截断) 7 ｜ 未读 0 ｜ 空文件 1（`02-conversion/observed-source-stderr.txt`） ｜ 缺件 根级 `target.ps1`、`02-conversion/request.system.txt`、`01-frozen/classification-1.json`
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-powershell/D2-133-cs-.upstream-sharpup-sharpup-native-win32.cs/output/batch`
- `01-frozen/`：`classification-2.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-134 ｜ csharp-to-powershell ｜ 现存 31 ｜ 已读 25 ｜ 已读(截断) 6 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 根级 `target.ps1`
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-powershell/D2-134-cs-amsi.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/`：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-135 ｜ csharp-to-powershell ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 同 D2-131
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-powershell/D2-135-cs-sharpcom.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-136 ｜ csharp-to-powershell ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 同 D2-131
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-powershell/D2-136-cs-range.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-137 ｜ csharp-to-python ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 同 D2-131（非可转换去向）
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-python/D2-137-cs-.upstream-sharpup-sharpup-checks-cachedgpppassword.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-138 ｜ csharp-to-python ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 同 D2-137
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-python/D2-138-cs-.upstream-sharpup-sharpup-checks-domaingpppassword.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-139 ｜ csharp-to-python ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 同 D2-137（长路径装置注意已登记）
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-python/D2-139-cs-.upstream-sharpup-sharpup-checks-modifiablescheduledtaskfile.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-140 ｜ csharp-to-python ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 同 D2-137；`01-frozen/classification-1.json` 已删（只有 `classification-2.json`）
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-python/D2-140-cs-.upstream-sharpup-sharpup-checks-modifiableserviceregistrykeys.cs/output/batch`
- `01-frozen/`：`classification-2.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-141 ｜ csharp-to-python ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3（job-00 的 report.json/report.md/controller.log）
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-python/D2-141-cs-.upstream-sharpup-sharpup-checks-tokenprivileges.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-142 ｜ csharp-to-python ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-python/D2-142-cs-.upstream-sharpup-sharpup-checks-unquotedservicepath.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-143 ｜ csharp-to-python ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-python/D2-143-cs-.upstream-sharpup-sharpup-utilities-identityutils.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-144 ｜ csharp-to-ruby ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-144-cs-.upstream-sharpup-sharpup-checks-hijackablepaths.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-145 ｜ csharp-to-ruby ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-145-cs-.upstream-sharpup-sharpup-checks-mcafeesitelistfiles.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-146 ｜ csharp-to-ruby ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-146-cs-.upstream-sharpup-sharpup-checks-modifiableservicebinaries.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-147 ｜ csharp-to-ruby ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-147-cs-.upstream-sharpup-sharpup-checks-registryautologons.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-148 ｜ csharp-to-ruby ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-148-cs-.upstream-sharpup-sharpup-checks-registryautoruns.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-149 ｜ csharp-to-ruby ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-149-cs-.upstream-sharpup-sharpup-checks-unattendedinstallfiles.cs/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-150 ｜ csharp-to-ruby ｜ 现存 11 ｜ 已读 10 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 3；`01-frozen/classification-1.json` 已删（只有 `classification-2.json`）
- 实际目录：`docs/dataset-2/dataset-2-copy/csharp-to-ruby/D2-150-cs-.upstream-sharpup-sharpup-properties-assemblyinfo.cs/output/batch`
- `01-frozen/`：`classification-2.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`evidence-source.json`
- `根层/`：`result.md`

### D2-151 ｜ c-to-cpp ｜ 现存 41 ｜ 已读 35 ｜ 已读(截断) 6 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 根级 `target.cpp`、`02-conversion/target.gen.cpp`、`02-conversion/target.gen.raw.txt`（副本删正文）
- 实际目录：`docs/dataset-2/dataset-2-copy/c-to-cpp/D2-151-c-c-rm.c/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/`：`request.system.txt`、`target.gen.model.json`
- `03-self-review/`：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `04-evaluation/job-00-source-buildability/`：`attempt-1-403.json`、`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`controller-health-after.json`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-01-dual-build/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`controller-health-after.json`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `根层/`：`evaluator_manifest.json`、`result.md`

### D2-152 ｜ c-to-cpp ｜ 现存 27 ｜ 已读 25 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 `result.md`
- 实际目录：`docs/dataset-2/dataset-2-copy/c-to-cpp/D2-152-c-c-du.c/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`evaluation_report.json`、**`evaluation_report.md.md`（双扩展名，全副本唯一）**、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-00b-source-buildability-linux/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`

### D2-153 ｜ c-to-cpp ｜ 现存 18 ｜ 已读 17 ｜ 已读(截断) 1 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 `result.md`
- 实际目录：`docs/dataset-2/dataset-2-copy/c-to-cpp/D2-153-c-c-cp.c/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`
  - `returned-evidence/`：`comparison.json`、`controller.log`、`controller-health-after.json`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`

### D2-154 ｜ c-to-cpp ｜ 现存 25 ｜ 已读 23 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 `result.md`
- 实际目录：`docs/dataset-2/dataset-2-copy/c-to-cpp/D2-154-c-c-sort.c/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-00b-source-buildability-linux/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`

### D2-155 ｜ c-to-cpp ｜ 现存 23 ｜ 已读 21 ｜ 已读(截断) 2 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 `result.md`
- 实际目录：`docs/dataset-2/dataset-2-copy/c-to-cpp/D2-155-c-c-xargs.c/output/batch`
- `01-frozen/`：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-00b-source-buildability-linux/`：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`
  - `returned-evidence/`：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`

### D2-156 ｜ c-to-csharp ｜ **无目录/无过程材料，现存 0** ｜ 已读 0 ｜ 已读(截断) 0 ｜ 未读 0 ｜ 空文件 0 ｜ 缺件 `frozen-inputs.md` + `result.md`
- `docs/dataset-2/dataset-2-copy/c-to-csharp/**` 在副本内 **0 文件**；本项只有 `batch/items/D2-156.json`（已读，31 行）。

### D2-157 ｜ c-to-csharp ｜ **无目录/无过程材料，现存 0** ｜ 缺件 `frozen-inputs.md` + `result.md`
- 只有 `batch/items/D2-157.json`（已读，31 行）。

### D2-158 ｜ c-to-csharp ｜ **无目录/无过程材料，现存 0** ｜ 缺件 `frozen-inputs.md` + `result.md`
- 只有 `batch/items/D2-158.json`（已读，31 行）。

### D2-159 ｜ c-to-csharp ｜ **无目录/无过程材料，现存 0** ｜ 缺件 `frozen-inputs.md` + `result.md`
- 只有 `batch/items/D2-159.json`（已读，31 行）。

### D2-160 ｜ c-to-csharp ｜ **无目录/无过程材料，现存 0** ｜ 缺件 `frozen-inputs.md` + `result.md`
- 只有 `batch/items/D2-160.json`（已读，31 行）。

## 审计差异（D2-121–D2-160，glob 计数 vs cases 表计数）

本 40 项中 **6 项**不相等（其余 34 项相等，含 D2-156–160 双方均为 0）：

| 项 | glob 计数 | cases 表计数 | 差（glob − cases） |
|---|---|---|---|
| D2-123 | 30 | 25 | +5 |
| D2-124 | 30 | 29 | +1 |
| D2-125 | 30 | 28 | +2 |
| D2-126 | 30 | 29 | +1 |
| D2-129 | 11 | 10 | +1 |
| D2-130 | 31 | 29 | +2 |

- 本 40 项 glob 合计 **623**；`harness-b-cases-03.md`/`04.md` 覆盖表对应合计 **611**；差 **+12**，与上表逐条差值之和一致。
- 方向：全部为 `+`，即 cases 表**少记**了副本内实际存在的文件（glob 为准）。本清单不回填、不删改 cases 文件。

## 未读集合（全区间结论）

**全区间 79 项未读集合为空**：D2-081–D2-120 的 40 项与 D2-121–D2-160 的 39 项（D2-156–160 无材料）`未读` 列合计均为 **0**。
**限制（非未读，但影响“已读完整性”）**：单行超过约 2000 字符的文件只读到工具可见窗口（逐项标 `已读(截断)`）；全区间 `已读(截断)` 合计 = 第一段 134 + 第二段（D2-121–160）75 = **209**，逐件清单见四份 cases 文件。工具限制本身不构成“未读”，但**不得**据此声称那些文件的第 2000 字符之后已读。

## 附注（续）

- 全区间现存文件合计 = 第一段 **770** + 第二段 **623** = **1393 件**（含 D2-156–160 的 0 件；不含 `batch/items/*.json` 的 79 件与批级文档）。
- D2-121–D2-160 的“已读/已读(截断)/未读/空文件”取自 `harness-b-cases-03.md`/`harness-b-cases-04.md` 的覆盖表；D2-141–150 的 10 项并列（同结构、同计数）。
- `evaluation_report.md.md`（D2-152）的双扩展名、`attempt-1-403.json`（D2-151）的存在、`classification-1.json` 的缺件（D2-133/140）等形制事实已逐项写入上表与 cases 文件。

## 进度日志（终）

- 2026-10-12：建立清单（IN_PROGRESS）；保留“工具与环境限制”3 条；范围 79 项（D2-113 不在 manifest）。
- 2026-10-12（前 40 项）：D2-081–D2-120 文件清单按 glob 回填完成；现存合计 770；计数与 cases 表差异 13 条；未读集合为空。
- 2026-10-12（后 40 项，含 D2-156–160 无材料）：D2-121–D2-160 文件清单按 glob 回填完成；现存合计 623；审计差异 6 条。
- 2026-10-12（收官）：**全区间 79 项逐项审阅与文件清单回填完成**；现存文件合计 1393；未读集合为空；审计差异共 19 条（前段 13 + 后段 6）；状态置 **COMPLETE**。
