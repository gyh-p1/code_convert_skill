# Harness C 覆盖清单（D2-161 .. D2-240）

> 状态：**IN_PROGRESS**（62 个存在项全部已逐件阅读；**验收补读轮**已重读多数原截断件，剩余集合见 §5 末「仍未补读」）。
> 范围：`docs/dataset-2/dataset-2-copy/manifest.csv` 中 `Id` 落在 D2-161..D2-240 的 **80 个编号位**；**实际存在 62 项**（与 `harness-acceptance-index.md` 的 C=62 一致），**18 个编号位不存在**（§2）。
> 引用基准：本文件内相对路径以 `docs/dataset-2/dataset-2-copy/` 为基准；每项目录形如 `<direction>/<case-dir>/`，工程产物在其 `output/batch/` 下。本文件在审阅目录内，故根 manifest/README 为 `../../manifest.csv`、`../../README.md`，batch 资料为 `../`。
> 读取状态：`✅已读` / `⬜未读` / `⚠️截断` / `∅空文件` / `✖缺件`。§4 中每项列出**全部现存文件名**（不省略、不用“同结构”代本项）。
> 方法：文件名来自原生 glob/spill 全量清单；正文由本会话及本会话派生的并行子审阅会话逐件阅读；主会话另行逐件读 `batch/items/<ID>.json` 与 manifest 行。源/目标代码已删，不得由哈希/摘要复原实现事实。

## 1. 编号位与状态总览

| 编号 | manifest | direction | 磁盘用例目录 | 阅读 |
|---|---|---|---|---|
| D2-161..166 | 有 | c-to-go | 见 §4 | ✅ |
| D2-167..173 | 有 | c-to-powershell | 见 §4 | ✅ |
| D2-174..178 | 有 | c-to-python | 见 §4 | ✅ |
| D2-179..183 | 有 | c-to-ruby | 见 §4 | ✅ |
| D2-184..188 | 有 | go-to-c | 见 §4 | ✅ |
| D2-189..193 | 有 | go-to-cpp | 见 §4 | ✅ |
| D2-194..198 | 有 | go-to-csharp | 见 §4 | ✅ |
| D2-199..203 | 有 | go-to-powershell | 见 §4 | ✅ |
| D2-204..208 | 有 | go-to-python | 见 §4 | ✅ |
| D2-209 | 有 | go-to-ruby | `go-to-ruby/D2-209-go-gpersist.go` | ✅ |
| D2-210 | 有 | csharp-to-powershell | `csharp-to-powershell/D2-210-cs-maliciousclickoncemsbuild.cs` | ✅ |
| D2-211..213 | 有 | go-to-ruby | 见 §4 | ✅ |
| D2-217 | 有 | powershell-to-cpp | `powershell-to-cpp/D2-217-ps-install-powershell.ps1` | ✅ |
| D2-222 | 有 | csharp-to-go | `csharp-to-go/D2-222-cs-.upstream-sharpup-sharpup-checks-alwaysinstallelevated.cs` | ✅ |
| D2-232..233 | 有 | powershell-to-ruby | 见 §4 | ✅ |
| D2-235,236,238,239,240 | 有 | python-to-c | 见 §4 | ✅ |

## 2. 范围内缺号（manifest 与磁盘均无用例目录，共 18 个）

`D2-214`、`D2-215`、`D2-216`、`D2-218`、`D2-219`、`D2-220`、`D2-221`、`D2-223`、`D2-224`、`D2-225`、`D2-226`、`D2-227`、`D2-228`、`D2-229`、`D2-230`、`D2-231`、`D2-234`、`D2-237`。合计 62＋18＝80。缺号项无文件清单可列，登记为「不存在（已移除）」；不在 manifest 的其它编号亦不属本范围。

## 2A. 缺件判定口径与读取限制

- `result.md` 为交付契约 §1.1 应有件；磁盘缺即 **✖缺件**。
- `02-conversion/`、`03-self-review/`：仅当实际发生模型请求时应有；`requests=0` 项记「未发生（不适用）」。
- `evaluator_manifest.json`、target 正文、`comparison.json`、`evidence-target.json`：仅生成/比较发生后应有；未生成项记不适用。
- **读取限制两阶段**：第一轮单行 >2000 字符被 `read` 截断且不可分页（记 ⚠️截断）；验收后官方 `readMaxLineLength`/`readMaxBytes` 提高至 1048576，第二轮用原生 read 重读，§5 逐件登记「已解除／仍未读」。
- 源/目标代码已删除，`source/` 无文件；**该不确定性不因全文读到而解除**。

## 3. 检查点

| 检查点 | 覆盖 | 状态 | 备注 |
|---|---|---|---|
| CP-0 | D2-161..240 映射 | 完成 | 62 存在 + 18 缺号 |
| CP-1 | D2-161..180 | 完成 | cases-01 |
| CP-2 | D2-181..200 | 完成 | cases-02 |
| CP-3 | D2-201..220（14 存在项） | 完成 | cases-03 |
| CP-4 | D2-221..240（8 存在项） | 完成 | cases-04 |
| CP-5 | 验收补读轮 | **进行中** | §5；剩余见末行 |

## 4. 逐项文件清单与读取状态

> 每项按目录分组列出全部现存文件；`01-frozen` 等目录内为该目录下的文件名（非路径）。

### D2-161 — c-to-go — `c-to-go/D2-161-c-c-date.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability-linux/` ✅：`comparison_manifest.json`、`input_profile.json`、`metadata.json`；`returned-evidence/` ✅：`evaluation_report.json`、`evidence-source.json`
- ✖缺件：`result.md`；`evaluator_manifest.json` 不适用

### D2-162 — c-to-go — `c-to-go/D2-162-c-c-uname.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability-linux/` ✅：`comparison_manifest.json`、`input_profile.json`、`metadata.json`；`returned-evidence/` ✅：`evaluation_report.json`、`evidence-source.json`
- `04-evaluation/job-00b-source-buildability-blocker-isolation/` ✅：`comparison_manifest.json`、`input_profile.json`、`metadata.json`；`returned-evidence/` ✅：`evidence-source.json`
- ✖缺件：`result.md`、job-00b `evaluation_report.json`

### D2-163 — c-to-go — `c-to-go/D2-163-c-c-wc.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability-linux/` ✅：`comparison_manifest.json`、`input_profile.json`、`metadata.json`；`returned-evidence/` ✅：`evaluation_report.json`、`evidence-source.json`
- ✖缺件：`result.md`

### D2-164 — c-to-go — `c-to-go/D2-164-c-c-ln.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability-linux/` ✅：`comparison_manifest.json`、`input_profile.json`、`metadata.json`；`returned-evidence/` ✅：`evaluation_report.json`、`evidence-source.json`
- ✖缺件：`result.md`

### D2-165 — c-to-go — `c-to-go/D2-165-c-c-tr.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability-linux/` ✅：`comparison_manifest.json`、`input_profile.json`、`metadata.json`；`returned-evidence/` ✅：`evaluation_report.json`、`evidence-source.json`
- ✖缺件：`result.md`

### D2-166 — c-to-go — `c-to-go/D2-166-c-c-uniq.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability-linux/` ✅：`comparison_manifest.json`、`input_profile.json`、`metadata.json`；`returned-evidence/` ✅：`evaluation_report.json`、`evidence-source.json`
- ✖缺件：`result.md`

### D2-167 — c-to-powershell — `c-to-powershell/D2-167-c-c-byebyedll.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-00b-relaxed-ptr-warning/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- ✖缺件：`result.md`、`evaluator_manifest.json`（不适用）

### D2-168 — c-to-powershell — `c-to-powershell/D2-168-c-c-chmod.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `04-evaluation/job-00b-source-buildability-linux/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- ✖缺件：`result.md`、job-00b `comparison.json`/`evaluation_report.md`

### D2-169 — c-to-powershell — `c-to-powershell/D2-169-c-c-loadlibraryr.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `04-evaluation/job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- ✖缺件：`result.md`、`comparison.json`（`comparisonRef` 指向但未回传）

### D2-170 — c-to-powershell — `c-to-powershell/D2-170-c-c-cmp.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `job-00b-source-buildability-linux/` ✅：同 6 配置件；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- ✖缺件：`result.md`、两侧 `evaluation_report.md`

### D2-171 — c-to-powershell — `c-to-powershell/D2-171-c-c-head.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`（缺 `casePath` 行）
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `job-00b-source-buildability-linux/` ✅：同 6 配置件；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- ✖缺件：`result.md`、两侧 `evaluation_report.md`

### D2-172 — c-to-powershell — `c-to-powershell/D2-172-c-c-env.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`（缺 `casePath` 行）
- `job-00-source-buildability/` ✅ 与 `job-00b-source-buildability-linux/` ✅：各 6 配置件；`returned-evidence/` 各 ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- ✖缺件：`result.md`、两侧 `evaluation_report.md`

### D2-173 — c-to-powershell — `c-to-powershell/D2-173-c-c-kill.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`（缺 `casePath` 行）
- `job-00-source-buildability/` ✅ 与 `job-00b-source-buildability-linux/` ✅：各 6 配置件；`returned-evidence/` 各 ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- ✖缺件：`result.md`、两侧 `evaluation_report.md`

### D2-174 — c-to-python — `c-to-python/D2-174-c-c-feal8_encrypt.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/` ✅：`request.system.txt`、`target.gen.model.json`（**仅哈希，无正文**）
- `03-self-review/` ✅：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `job-00-source-buildability/` ✅：`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`runners-before.json`；`returned-evidence/` ✅：`evaluation_report.json`、`evidence-source.json`
- `job-01-dual-build/` ✅：`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`；`returned-evidence/` ✅：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `output/batch/` ✅：`evaluator_manifest.json`、`result.md`
- ✖缺件：job-00 `evidence-target.json`、`comparison.json`

### D2-175 — c-to-python — `c-to-python/D2-175-c-c-wjcryptlib_rc4.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- ✖缺件：`result.md`、`evaluator_manifest.json`、job-00 `comparison.json`

### D2-176 — c-to-python — `c-to-python/D2-176-c-c-pwd.c`
- `01-frozen/` ✅（2 件）：`classification-1.json`、`classifier-input.json`；**✖缺 `frozen-inputs.md`**
- `02-conversion/` ✅（1 件）：`request.system.txt`；**✖缺 `target.gen.model.json`**
- `03-self-review/` ✅：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `job-01-dual-build/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `output/batch/` ✅：`evaluator_manifest.json`、`result.md`

### D2-177 — c-to-python — `c-to-python/D2-177-c-c-which.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/` ✅：`repair1.system.txt`、`request.system.txt`、`target.gen.model.json`、`target.self-repair-1.model.json`（后两件仅哈希）
- `03-self-review/` ✅：`review.system.txt`、`review2.system.txt`、`self-review-1.json`、`self-review-1.model.json`、`self-review-2.json`、`self-review-2.model.json`
- `job-00-source-buildability-linux/` ✅：`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`；`returned-evidence/` ✅：`evaluation_report.json`（=`{"detail":"job_report_not_found"}`）、`evidence-source.json`
- `job-01-dual-build/` ✅：`attribution.md`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`；`returned-evidence/` ✅：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `job-02-argv-forwarding/` ✅：`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`；`returned-evidence/` ✅：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `output/batch/` ✅：`evaluator_manifest.json`、`result.md`
- ✖缺件：job-01/job-02 `controller-health-before.json`

### D2-178 — c-to-python — `c-to-python/D2-178-c-c-strnsubst.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability-linux/` ✅：`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`；`returned-evidence/` ✅：`evaluation_report.json`、`evidence-source.json`
- ✖缺件：`result.md`

### D2-179 — c-to-ruby — `c-to-ruby/D2-179-c-c-enumdesktopsa_hack.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅ 与 `job-00b-relaxed-implicit-decl/` ✅：各 `batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` 各 ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- ✖缺件：`result.md`

### D2-180 — c-to-ruby — `c-to-ruby/D2-180-c-c-rc4_decrypt_cli.c`
- `01-frozen/` ✅（2 件）：`classification-1.json`、`classifier-input.json`；**✖缺 `frozen-inputs.md`**
- `02-conversion/` ✅：`repair.system.txt`、`repair2.system.txt`、`request.system.txt`（**无 `target.gen.model.json`/`target.self-repair-*.model.json`**）
- `03-self-review/` ✅：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `job-00-source-buildability/` ✅：6 配置件；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `job-01-dual-build/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`controller-health-before.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `job-02-dual-build-eval-repair-1/` ✅：同 7 配置件 + 同 7 evidence
- `output/batch/` ✅：`evaluator_manifest.json`、`result.md`
- ✖缺件：job-00 `comparison.json`、`evaluation_report.md`

### D2-181 — c-to-ruby — `c-to-ruby/D2-181-c-c-speck_encrypt.c`
- `01-frozen/` ✅（2 件）：`classification-1.json`、`classifier-input.json`；**✖缺 `frozen-inputs.md`**
- `02-conversion/` ✅：`request.system.txt`（无 model.json）
- `03-self-review/` ✅：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `job-00-source-buildability/` ✅ 与 `job-01-dual-build/` ✅：各 7 配置件 + 7 evidence（`comparison.json`、`controller-health-after.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`）
- `output/batch/` ✅：`evaluator_manifest.json`、`result.md`

### D2-182 — c-to-ruby — `c-to-ruby/D2-182-c-c-virtualallocex_hack.c`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- ✖缺件：`result.md`

### D2-183 — c-to-ruby — `c-to-ruby/D2-183-c-c-realpath.c`
- `01-frozen/` ✅；`02-conversion/` ✅：`request.system.txt`；`03-self-review/` ✅：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `job-00-source-buildability/` ✅、`job-00b-source-buildability-linux/` ✅、`job-01-dual-build/` ✅：各 7 配置件 + 7 evidence
- `output/batch/` ✅：`evaluator_manifest.json`、`result.md`

### D2-184 — go-to-c — `go-to-c/D2-184-go-gobound.go`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`evidence-source.json`（`evidence_not_found`）
- `output/batch/` ✅：`result.md`

### D2-185 — go-to-c — `go-to-c/D2-185-go-filepath.go` … D2-188 — `go-to-c/D2-188-go-createprocess.go`
- 四项结构相同，均 ✅：`01-frozen/{classification-1.json, classifier-input.json, frozen-inputs.md}`；`job-00-source-buildability/{batch-authorization.json, comparison_manifest.json, input_profile.json, metadata.json, job-id.txt, this-task-classification.json, returned-evidence/evidence-source.json}`；`result.md`

### D2-189 — go-to-cpp — `go-to-cpp/D2-189-go-hex.go`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`evidence-source.json`
- `output/batch/` ✅：`result.md`

### D2-190 — go-to-cpp — `go-to-cpp/D2-190-go-runpe.go`
- 同 D2-189 全部 11 件 ✅（`01-frozen` 3、`job-00` 7、`result.md`）

### D2-191 — go-to-cpp — `go-to-cpp/D2-191-go-psexec.go`
- `01-frozen/` ✅：`classifier-input.json`、`classification-2.json`、`frozen-inputs.md`（`classification-1.json` 按纪律删除）
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`evidence-source.json`
- `output/batch/` ✅：`result.md`

### D2-192 — go-to-cpp — `go-to-cpp/D2-192-go-buffer.go`
- 同 D2-189 全部 11 件 ✅

### D2-193 — go-to-cpp — `go-to-cpp/D2-193-go-csv_reader.go`
- 同 D2-189 全部 11 件 ✅

### D2-194 — go-to-csharp — `go-to-csharp/D2-194-go-reverse-shell.go`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/` ✅：`observed-source-stderr.txt`、`observed-source-stdout.txt`、`request.system.txt`、`target.gen.model.json`
- `03-self-review/` ✅：`review.system.txt`、`self-review-1.json`、`self-review-1.model.json`
- `job-00-source-buildability/` ✅：6 配置件 + `returned-evidence/evidence-source.json`
- `job-01-dual-build/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`comparison.json`、`controller.log`、`evaluation_report.json`、`evidence-source.json`、`evidence-target.json`
- `output/batch/` ✅：`evaluator_manifest.json`、`result.md`
- ✖缺件：`repair*.system.txt`、`target.self-repair-*.model.json`（`codeRevisions=1` 却无修复原件）；job `controller-health-*`/`runners-*`

### D2-195 — go-to-csharp — `go-to-csharp/D2-195-go-atoi.go`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`；`job-00-source-buildability/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`、`returned-evidence/evidence-source.json`；`result.md` ✅

### D2-196 — go-to-csharp — `go-to-csharp/D2-196-go-match.go`
- 同 D2-195 全部 11 件 ✅

### D2-197 — go-to-csharp — `go-to-csharp/D2-197-go-sort.go`
- `01-frozen/` ✅：`frozen-inputs.md`、`classifier-input.json`、`classifier-input-2.json`、`classification-1.json`、`classification-2.json`
- `job-00-source-buildability/` ✅：`job-id.txt`、`metadata.json`、`input_profile.json`、`source_preflight_manifest.json`、`batch-authorization.json`、`this-task-classification.json`；`returned-evidence/` ✅：`controller.log`、`evaluation_report.md`、`evaluation_report.json`、`closure.json`、`evidence-source.json`
- `job-00b-source-buildability/` ✅：同 6 配置件 + 同 5 evidence
- `output/batch/` ✅：`result.md`
- 缺：`comparison_manifest.json`（改用 source-only 形态，不适用）

### D2-198 — go-to-csharp — `go-to-csharp/D2-198-go-screenshot_windows.go`
- `01-frozen/` ✅：`frozen-inputs.md`、`classifier-input.json`、`classification-1.json`
- `job-00-source-buildability/` ✅：`job-id.txt`、`metadata.json`、`input_profile.json`、`source_preflight_manifest.json`、`batch-authorization.json`、`this-task-classification.json`；`returned-evidence/` ✅：`controller.log`、`evaluation_report.md`、`evaluation_report.json`、`closure.json`、`evidence-source.json`
- `output/batch/` ✅：`result.md`

### D2-199 — go-to-powershell — `go-to-powershell/D2-199-go-shell_reverse_tcp.go`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/` ✅：`target.gen.model.json`；`03-self-review/` ✅：`self-review-1.json`、`self-review-1.model.json`（无 `review.system.txt`）
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`source_preflight_manifest.json`、`this-task-classification.json`（**无 `returned-evidence/`**）
- `job-01-dual-build/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `output/batch/` ✅：`evaluator_manifest.json`、`result.md`

### D2-200 — go-to-powershell — `go-to-powershell/D2-200-go-EarlyBird.go`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`source_preflight_manifest.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`
- `output/batch/` ✅：`result.md`

### D2-201 — go-to-powershell — `go-to-powershell/D2-201-go-UuidFromString.go`
- 同 D2-200 全部 15 件 ✅

### D2-202 — go-to-powershell — `go-to-powershell/D2-202-go-itoa.go`
- 同 D2-200 全部 15 件 ✅

### D2-203 — go-to-powershell — `go-to-powershell/D2-203-go-reader.go`
- 同 D2-200 全部 15 件 ✅

### D2-204 — go-to-python — `go-to-python/D2-204-go-createremotethread.go`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`source_preflight_manifest.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`
- `output/batch/` ✅：`result.md`

### D2-205 — go-to-python — `go-to-python/D2-205-go-CreateRemoteThreadNative.go`
- 同 D2-204 全部 15 件 ✅

### D2-206 — go-to-python — `go-to-python/D2-206-go-EtwpCreateEtwThread.go`
- 同 D2-204 全部 15 件 ✅

### D2-207 — go-to-python — `go-to-python/D2-207-go-ProcessInjection.go`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `02-conversion/` ✅：`target.gen.model.json`、`target.self-repair-1.model.json`；`03-self-review/` ✅：`self-review-1.json`、`self-review-1.model.json`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`source_preflight_manifest.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`
- `job-01-dual-build/` ✅：`batch-authorization.json`、`comparison_manifest.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`comparison.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`、`evidence-target.json`
- `output/batch/` ✅：`result.md`
- ✖缺件：`evaluator_manifest.json`、`case.md`、全部 raw request/response

### D2-208 — go-to-python — `go-to-python/D2-208-go-search.go`
- 同 D2-204 全部 15 件 ✅

### D2-209 — go-to-ruby — `go-to-ruby/D2-209-go-gpersist.go`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`source_preflight_manifest.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`
- `output/batch/` ✅：`result.md`

### D2-210 — csharp-to-powershell — `csharp-to-powershell/D2-210-cs-maliciousclickoncemsbuild.cs`
- `01-frozen/` ✅：`frozen-inputs.md`、`classification-1.json`、`classifier-input.json`、`classification-2.json`、`classifier-input-2.json`
- `job-00-source-buildability/` ✅：6 配置件 + `returned-evidence/{closure.json, controller.log, evaluation_report.json, evaluation_report.md, evidence-source.json}`
- `job-01-source-baseline/` ✅：6 配置件 + 同 5 evidence
- `output/batch/` ✅：`result.md`

### D2-211 — go-to-ruby — `go-to-ruby/D2-211-go-bypassUACgo.go`
- 同 D2-209 全部 15 件 ✅

### D2-212 — go-to-ruby — `go-to-ruby/D2-212-go-keylogger.go`
- 同 D2-209 全部 15 件 ✅

### D2-213 — go-to-ruby — `go-to-ruby/D2-213-go-Syscall.go`
- 同 D2-209 全部 15 件 ✅

### D2-217 — powershell-to-cpp — `powershell-to-cpp/D2-217-ps-install-powershell.ps1`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `output/batch/` ✅：`result.md`
- `02/03/04` 未发生（BLOCKED，不适用）

### D2-222 — csharp-to-go — `csharp-to-go/D2-222-cs-.upstream-sharpup-sharpup-checks-alwaysinstallelevated.cs`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`source_preflight_manifest.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`
- `output/batch/` ✅：`result.md`

### D2-232 — powershell-to-ruby — `powershell-to-ruby/D2-232-cpp-safe_attck_cpp_suite-build_run.ps1`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`classification-2.json`、`classifier-input-2.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`source_preflight_manifest.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`
- `job-00b-source-buildability/` ✅：同 6 配置件 + 同 5 evidence
- `output/batch/` ✅：`result.md`

### D2-233 — powershell-to-ruby — `powershell-to-ruby/D2-233-cpp-safe_attck_cpp_suite-build_run_advanced.ps1`
- `01-frozen/` ✅：`classification-1.json`、`classifier-input.json`、`frozen-inputs.md`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`source_preflight_manifest.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`
- `output/batch/` ✅：`result.md`

### D2-235 — python-to-c — `python-to-c/D2-235-python-psexec.py`
- `01-frozen/` ✅：`frozen-inputs.md`、`classification-2.json`、`classifier-input-2.json`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`source_preflight_manifest.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`
- `output/batch/` ✅：`result.md`

### D2-236 — python-to-c — `python-to-c/D2-236-python-pwncat.py`
- `01-frozen/` ✅：`frozen-inputs.md`、`classification-2.json`、`classifier-input-2.json`
- `job-00-source-buildability/` ✅：`batch-authorization.json`、`input_profile.json`、`job-id.txt`、`metadata.json`、`source_preflight_manifest.json`、`this-task-classification.json`；`returned-evidence/` ✅：`closure.json`、`controller.log`、`evaluation_report.json`、`evaluation_report.md`、`evidence-source.json`
- `output/batch/` ✅：`result.md`

### D2-238 — python-to-c — `python-to-c/D2-238-python-getst.py`
- `01-frozen/` ✅：`frozen-inputs.md`、`classification-1.json`、`classifier-input.json`
- `job-00-source-buildability/` ✅：同上 6 配置件 + 5 evidence
- `output/batch/` ✅：`result.md`

### D2-239 — python-to-c — `python-to-c/D2-239-python-ticketer.py`
- `01-frozen/` ✅：`frozen-inputs.md`、`classification-1.json`、`classifier-input.json`
- `job-00-source-buildability/` ✅：同上 6 配置件 + 5 evidence
- `output/batch/` ✅：`result.md`

### D2-240 — python-to-c — `python-to-c/D2-240-python-reg.py`
- `01-frozen/` ✅：`frozen-inputs.md`、`classification-1.json`、`classifier-input.json`
- `job-00-source-buildability/` ✅：同上 6 配置件 + 5 evidence
- `output/batch/` ✅：`result.md`

## 5. 验收补读记录（`readMaxLineLength`/`readMaxBytes` 提高至 1048576 后）

| 文件 | 原状态 | 结果 | 补读获得的关键字段 |
|---|---|---|---|
| `c-to-go/D2-161…166` 共 7 件 `job-00(-00b)/returned-evidence/evidence-source.json` | ⚠️截断 | **已解除** | `observations`（`output=blocked`+`limitations:["execution did not start"]`、registry/network `not-applicable`）、`coverage.dimensions`、`collectorDiagnostics:[]`；D2-162 job-00b `caseId …blocker-isolation`；D2-164 stderr 全文 1099 B `digest 804ff875…` |
| `c-to-powershell/D2-167…173` 共 15 件 `returned-evidence/evidence-source.json`（169 另含 `evidence-target.json`/`evaluation_report.json`） | ⚠️截断 | **已解除** | D2-167 job-00b `execution.status="timed-out"`/`durationMs 30019`/`timedOut true`；D2-169 源 `exitCode 97`+`DRIVER-FAILURE: no runnable artifact…`、target placeholder 29 B、`evaluation_report schemaVersion 3.0`/`comparisonRef comparison/result.json`；其余 stderr 全文字节与 digest |
| `c-to-python/D2-174/output/batch/03-self-review/self-review-1.json` | ⚠️截断 | **已解除** | 全部 11 条（原前 6 条）+ `unresolved:[]` |
| `c-to-python/D2-177/.../self-review-1.json` | ⚠️截断 | **已解除** | 全部 12 条（新增 getopt 未知选项、PATH 未设、多参数、初始化顺序、整体、GNU argv 重排）+ `unresolved` |
| `c-to-python/D2-177/.../self-review-2.json` | ⚠️截断 | **已解除** | 全部 8 条（新增 `-a/-s`、`os.fsencode` 语义、其他排查）+ `unresolved` |
| `go-to-c/D2-185…188` 共 4 件 `evidence-source.json` | ⚠️截断 | **已解除** | D2-185 stderr 全文 473 B（含被 frozen 漏记的 `:305:5: undefined: IsAbs`）；D2-186 execution stderr 254 B `SyntaxError`；D2-187 279 B；D2-188 175 B |
| `go-to-cpp/D2-189…193` 共 5 件 `evidence-source.json` | ⚠️截断 | **已解除** | D2-189/193 execution `PermissionError [Errno 13]`（1333 B）；**D2-190 `OSError [WinError 216]`（EXE 机器类型不匹配，更正“未产出文件”推断）**；D2-191 878 B 五模块；D2-192 65 B |
| `powershell-to-ruby/D2-232`（6 件）/`D2-233`（2 件）`closure.json`+`evidence-source.json` | ⚠️截断 | **已解除**（子审阅会话重读） | D2-232 job-00 `exit 97`+DRIVER-FAILURE、job-00b stdout 1614 B/stderr 2591 B；D2-233 stdout 1819 B/stderr 空 |
| `python-to-c/D2-235/236/238/239/240` 各 `closure.json`+`evidence-source.json`（10 件） | ⚠️截断 | **已解除**（子审阅会话重读） | 各 build/exec 退出码、`ModuleNotFoundError`/argparse 全文、`oracleStatus/programOutputProvenance=UNVERIFIED` |

**仍未补读（精确集合）**：
- `c-to-python`：D2-174 job-00/job-01、D2-175、D2-176 job-00/job-01、D2-177 job-00/job-01/job-02、D2-178 的 `returned-evidence/{evidence-source.json, evidence-target.json, evaluation_report.json, comparison.json}` 中原 ⚠️截断件。
- `c-to-ruby`：D2-179…183 各 job 的 `evidence-source.json`/`evidence-target.json`/`evaluation_report.json`（原 ⚠️截断件）。
- `go-to-csharp`：D2-194（`target.gen.model.json`、`self-review-1.json`、`self-review-1.model.json`、job-00/job-01 evidence 共 7 件）、D2-195…198 各 `evidence-source.json`/`closure.json`/`evaluation_report.json`。
- `go-to-powershell`：D2-199…203 各 `evidence-source.json`/`evidence-target.json`/`closure.json`/`evaluation_report.json`。
- `go-to-python`：D2-204…208 各 `evidence-source.json`/`closure.json`/`evaluation_report.json`（204/205/206/208 共 8 件；207 共 6 件）。
- `go-to-ruby`：D2-209/211/212/213 各 `evidence-source.json`/`closure.json`/`evaluation_report.json`。
- `csharp-to-powershell` D2-210、`csharp-to-go` D2-222：各 `evidence-source.json`/`closure.json`/`evaluation_report.json`。
上述未补读件在第一轮均已读到前缀并在 cases 中引用了关键事实；在补读完成前，本文件保持 **IN_PROGRESS**，不对全范围发 COMPLETE。

### 5.1 补读追加（go-to-csharp D2-194，第二轮）

| 文件 | 原状态 | 结果 | 补读获得的关键字段 |
|---|---|---|---|
| `go-to-csharp/D2-194/.../02-conversion/target.gen.model.json` | ⚠️截断 | **已解除** | **并非仅哈希**：含完整 `role:assistant` 的 `content`（完整 C# 目标代码）与 `reasoning_content`（模型推理，不作审阅结论）⇒ 该件是完整响应 |
| `go-to-csharp/D2-194/.../03-self-review/self-review-1.json` | ⚠️截断 | **已解除** | 全文：`REPAIR-RECOMMENDED` 1 条（`CmdSwitch` 缺 `case "exec"`，`Ex` 成死代码；origin=Go→C# translation omission；含 proposed_fix/risk 全文） |
| `go-to-csharp/D2-194/.../job-01-dual-build/returned-evidence/evidence-target.json` | ⚠️截断 | **已解除** | build stdout 全文 1595 B（`probe.csproj` restore + 2× `CS8632` + `Build succeeded.`）；build stderr 670 B（`.NET 10.0` / SDK `10.0.110`）；execution `exitCode 150`、stderr 全文 606 B：`You must install or update .NET to run this application. … Framework 'Microsoft.NETCore.App', version '8.0.0' … The following frameworks were found: 10.0.10` ⇒ **确认 exit 150 为 runner 缺 .NET 8 运行时（环境），非转换引入** |
