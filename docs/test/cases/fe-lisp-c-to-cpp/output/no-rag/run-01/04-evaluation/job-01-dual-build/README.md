# job-01-dual-build · fe run-01 双侧 build 评估 capsule

状态：**capsule 输入已就绪，待提交执行**（`READY-TO-SUBMIT`）。本目录是按现役 Controller `/api/jobs` 契约组装的**双侧 comparison capsule 输入**，用于源侧（C11 基线）与目标侧（C++17）构建并运行，本阶段只读 **build 证据**。尚无 Controller 返回件（`report.json`/`evidence-*.json`/`comparison.json`/`job-id.txt`）——它们由 Controller 执行后回填，不在本仓库预造。

## 已就绪的 capsule 输入

| 文件 | 作用 |
|---|---|
| `comparison_manifest.json` | 双侧 `buildCommand` + `runCommand`；源 `gcc -std=c11 -DFE_STANDALONE fe.c -o program`，目标 `g++ -std=c++17 -DFE_STANDALONE target.cpp -o program`（MinGW/UCRT64 下均产出 `program.exe`）。 |
| `input_profile.json` | 无 argv、无 fixtures、stdin=null、`output` 维度、30s 超时。 |
| `metadata.json` | caseId、只读/无外联边界声明、源/目标真实 sha256。 |
| `source/run_case.py`、`target/run_case.py` | form-B REPL liveness 驱动：stdin 立即 EOF，程序空跑即 `EXIT_SUCCESS`，不联网、无 fixture。 |

## zip 组装清单（提交时）

Controller 在各侧目录内执行 `buildCommand` 再 `runCommand`，故 `fe.h` 必须与被编译文件同目录：

- `source/`：`fe.c` + `fe.h`（源自 `docs/test/sources/fe/`）+ 本目录 `source/run_case.py`
- `target/`：`target.cpp`（run 根最终交付稿）+ `fe.h` + 本目录 `target/run_case.py`
- 顶层：`comparison_manifest.json`、`input_profile.json`、`metadata.json`

（大源码文件不在本目录重复留存，避免仓库冗余；zip 时按上表从各自权威落点拷入。）

## 提交与回填

- 远端 Controller/隔离 VM 按本项目既定政策**恒就绪且已授权**：到评估步骤直接提交，不再逐次确认可达性或询问是否评估。
- **本 Claude Code 会话无对接 Controller 的提交工具**（仅 `WebSearch` 获准，`.env` 仅含模型凭证，无 controller MCP/端点），故实际 POST 与证据回传经既定提交渠道进行（C01 先例由独立编排器完成）。
- Controller 返回后，在本目录落 `job-id.txt`、`report.json`/`report.md`、`evidence-source.json`、`evidence-target.json`、`comparison.json`、`logs.json`，并据其 **build 证据**回填 run 根 `evaluator_manifest.json` 的 `executionApproved`、`thirdPartyCompileStatus`、`syntaxVerdict` 与 `result.md` 三项结论。语法/行为结论只从真实报告回填，绝不由 Agent 或模型自评臆造。
