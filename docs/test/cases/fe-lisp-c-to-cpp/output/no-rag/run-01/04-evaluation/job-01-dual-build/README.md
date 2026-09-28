# job-01-dual-build · fe run-01 双侧 build 评估 capsule

状态：**已提交并执行完毕**（`COMPLETED`）。本目录是按现役 Controller `/api/jobs` 契约组装的**双侧 comparison capsule 输入**，已于 2026-09-28 经直连 Controller HTTP（`http://192.168.101.250:8443`，`POST /api/jobs`）提交，jobId=`eval-20260928-033750-71724720`。真实返回件保存于 [`returned-evidence/`](returned-evidence/)。本阶段只读 **build 证据**：目标 C++17 build `exitCode=0`（stderr 空）→ 编译 **PASS**，源侧 C11 对照基线 build `exitCode=0`。

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

## 提交与回填（已完成）

- 远端 Controller/隔离 VM 按本项目既定政策**恒就绪且已授权**：本 run 已于评估步骤直接提交。
- **本会话经直连 HTTP 8443 提交**：本机 `192.168.101.105` 与 Controller `192.168.101.250` 同 `/24` 段可直达，用 `curl.exe -F` 完成 multipart `POST /api/jobs`（`file=@capsule.zip`、`caseId=fe-lisp-c-to-cpp-run-01`、`targetOs=windows`、`targetLang=cpp`），轮询至 `COMPLETED`。连接与提交适配详见 [references/adapter/controller/remote-controller-adapter.md](../../../../../../../../../references/adapter/controller/remote-controller-adapter.md)。
- Controller 返回件已落 `returned-evidence/`：`job-id.txt`、`state.json`、`evaluation_report.json`/`.md`、`evidence-source.json`、`evidence-target.json`、`comparison.json`、`controller.log`。据其 **build 证据**已回填 run 根 `evaluator_manifest.json`（`executionApproved=true`、`thirdPartyCompileStatus=THIRD-PARTY-COMPILE-PASSED`、`syntaxVerdict=PASS`）与 `result.md` 三项结论。语法/行为结论只从真实报告回填，未由 Agent 或模型自评臆造。
