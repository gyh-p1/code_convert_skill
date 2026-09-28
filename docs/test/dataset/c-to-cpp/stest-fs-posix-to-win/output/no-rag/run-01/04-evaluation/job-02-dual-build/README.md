# job-02-dual-build · stest run-01 跨 OS 双侧 build 评估 capsule

状态：**已提交并执行完毕**（`COMPLETED`）。本目录是按现役 Controller `/api/jobs` 契约组装的**跨 OS 双侧 comparison capsule 输入**，已于 2026-09-28 经直连 Controller HTTP（`http://192.168.101.250:8443`，`POST /api/jobs`）提交，jobId=`eval-20260928-053745-2a386af5`。真实返回件保存于 [`returned-evidence/`](returned-evidence/)。本阶段只读 **build 证据**：目标 C++17 build（Windows）`exitCode=0`（stderr 空）→ 编译 **PASS**，源侧 C11 对照基线（Linux）build `exitCode=0`。

> 本 job-02 取代 [`../job-01-dual-build`](../job-01-dual-build)：job-01（`eval-20260928-053326-9a8ae00e`）因源侧基线命令 `cc -std=c11 stest.c -o program` 缺 POSIX 特性测试宏，源基线 build FAILED，dual-runner 因此未构建目标侧。修正源命令（补 `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE`）后以本 job-02 重取；**目标命令与 `target.cpp` 均未改**。job-01 失败证据保留、不倒填。

## 已就绪的 capsule 输入

| 文件 | 作用 |
|---|---|
| `comparison_manifest.json` | 双侧 `buildCommand` + `runCommand`；源 `cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE stest.c -o program`（Linux），目标 `g++ -std=c++17 target.cpp -o program`（Windows MinGW/UCRT64）。`os`：source=`linux`、target=`windows`；`arch`=`x64`。 |
| `input_profile.json` | 无 argv、无 fixtures、stdin=null、`output` 维度、30s 超时。 |
| `metadata.json` | caseId、只读/无外联边界声明、源/目标真实 sha256。 |
| `source/run_case.py`、`target/run_case.py` | liveness 驱动：无参数启动、stdin 立即 EOF（`getline` 立即 EOF → `match=0` → 返回 1），打印 `{"exitCode","stderrLen","stdoutLen"}`；不联网、无 fixture。 |

## zip 组装清单（提交时）

Controller 在各侧目录内执行 `buildCommand` 再 `runCommand`，故 `arg.h` 必须与被编译文件同目录：

- `source/`：`stest.c` + `arg.h`（源自 `docs/test/sources/dmenu-stest/`）+ 本目录 `source/run_case.py`
- `target/`：`target.cpp`（run 根最终交付稿）+ `arg.h` + 本目录 `target/run_case.py`
- 顶层：`comparison_manifest.json`、`input_profile.json`、`metadata.json`

## 提交与回填（已完成）

- 远端 Controller/隔离 VM 按本项目既定政策**恒就绪且已授权**：本 run 已于评估步骤直接提交。
- **本会话经直连 HTTP 8443 提交**：用 `curl.exe -F` 完成 multipart `POST /api/jobs`（`file=@capsule.zip`、`caseId=stest-fs-posix-to-win-run-01`、`targetOs=windows`、`targetLang=cpp`），轮询至 `COMPLETED`。连接与提交适配详见 [remote-controller-adapter.md](../../../../../../../../../../references/adapter/controller/remote-controller-adapter.md)。
- Controller 返回件已落 `returned-evidence/`：`evaluation_report.json`/`.md`、`evidence-source.json`、`evidence-target.json`、`comparison.json` 等。据其 **build 证据**已回填 run 根 `evaluator_manifest.json`（`executionApproved=true`、`thirdPartyCompileStatus=THIRD-PARTY-COMPILE-PASSED`、`syntaxVerdict=PASS`）与 `result.md` 三项结论。语法/行为结论只从真实报告回填，未由 Agent 或模型自评臆造。
