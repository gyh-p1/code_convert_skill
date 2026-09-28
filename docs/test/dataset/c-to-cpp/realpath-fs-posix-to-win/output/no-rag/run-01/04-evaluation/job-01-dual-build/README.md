# job-01-dual-build · realpath run-01 跨 OS 双侧 build 评估 capsule

状态：**已提交并执行完毕**（`COMPLETED`）。本目录是按现役 Controller `/api/jobs` 契约组装的**跨 OS 双侧 comparison capsule 输入**，已于 2026-09-28 经直连 Controller HTTP（`http://192.168.101.250:8443`，`POST /api/jobs`）提交，jobId=`eval-20260928-060834-49b1a302`。真实返回件保存于 [`returned-evidence/`](returned-evidence/)。本阶段只读 **build 证据**：目标 C++17 build（Windows）`exitCode=0`（stderr 空）→ 编译 **PASS**，源侧 C11 对照基线（Linux）build `exitCode=0`。

> 本 job 是 realpath run-01 的**首次也是唯一一次**提交（无被取代 job）。目标件已在提交前经**一轮自修**：首轮自审判 `REPAIR-RECOMMENDED`（`realpath` 命名冲突等 3 项），自修后复审判 `NO-REPAIR-IDENTIFIED`；提交的 `target/target.cpp` = run 根 `target.cpp` = `02-conversion/target.repair-1.cpp`（sha256 `460303a4…`）。

> **诚实标注：Controller 综合报告 `codeVerdict=failed`、`behaviorVerdict=mismatched` 不是编译失败。** 唯一 diff 为 output 维度 stdout 长度（源 75 vs 目标 82），因两侧规范化当前目录 `"."` 得到的绝对路径文本随 OS 不同（分隔符 + 路径），退出码（0=0）与 stderr（空=空）均一致。属冻结时即预告的按设计跨 OS 差异，本阶段不评功能、不设 oracle，不改变编译=PASS。

## 已就绪的 capsule 输入

| 文件 | 作用 |
|---|---|
| `comparison_manifest.json` | 双侧 `buildCommand` + `runCommand`；源 `cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__dead2= realpath.c -o program`（Linux），目标 `g++ -std=c++17 target.cpp -o program`（Windows MinGW/UCRT64）。`os`：source=`linux`、target=`windows`；`arch`=`x64`。 |
| `input_profile.json` | 无 argv、无 fixtures、stdin=null、`output` 维度、30s 超时。 |
| `metadata.json` | caseId、只读/无外联边界声明、源/目标真实 sha256。 |
| `source/run_case.py`、`target/run_case.py` | liveness 驱动：无参数启动、stdin 立即 EOF（无操作数 → 规范化 `"."` → 打印一条规范化绝对路径、exit 0），输出 `{"exitCode","stderrLen","stdoutLen"}`；不联网、无 fixture。已注明 stdout 长度随 OS 路径文本不同。 |

## zip 组装清单（提交时）

Controller 在各侧目录内执行 `buildCommand` 再 `runCommand`。realpath **无伴随本地头**，故各侧只含其 artifact + 驱动：

- `source/`：`realpath.c`（源自 `docs/test/sources/freebsd-realpath/`）+ 本目录 `source/run_case.py`
- `target/`：`target.cpp`（run 根最终交付稿 = 自修稿）+ 本目录 `target/run_case.py`
- 顶层：`comparison_manifest.json`、`input_profile.json`、`metadata.json`

## 提交与回填（已完成）

- 远端 Controller/隔离 VM 按本项目既定政策**恒就绪且已授权**：本 run 已于评估步骤直接提交。
- **本会话经直连 HTTP 8443 提交**：用 `curl.exe -F` 完成 multipart `POST /api/jobs`（`file=@capsule.zip`、`caseId=realpath-fs-posix-to-win-run-01`、`targetOs=windows`、`targetLang=cpp`），轮询至 `COMPLETED`。连接与提交适配详见 [remote-controller-adapter.md](../../../../../../../../../../references/adapter/controller/remote-controller-adapter.md)。
- Controller 返回件已落 `returned-evidence/`：`evaluation_report.json`/`.md`、`evidence-source.json`、`evidence-target.json`、`comparison.json`、`controller.log`、`state.json`、`job-id.txt`。据其 **build 证据**已回填 run 根 `evaluator_manifest.json`（`executionApproved=true`、`thirdPartyCompileStatus=THIRD-PARTY-COMPILE-PASSED`、`syntaxVerdict=PASS`）与 `result.md` 三项结论。语法结论只从真实 build 报告回填；`behaviorVerdict=mismatched` 亦如实记录并归因为按设计跨 OS 差异，未由 Agent 或模型自评臆造，也未把 mismatch 粉饰为 match。
