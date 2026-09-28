# job-01-dual-build — du 跨 OS 双侧编译 comparison capsule

本目录记录 `du-fs-posix-to-win-run-01` 提交给远端隔离 VM Controller 的**跨 OS 双侧编译**评估作业（source C @ Linux baseline，target C++ @ Windows），以及真实回传证据。

## 提交概要

| 项 | 值 |
| --- | --- |
| caseId | `du-fs-posix-to-win-run-01` |
| jobId | `eval-20260928-073929-e89be213` |
| jobStatus | `COMPLETED` |
| targetOs / targetLang | `windows` / `cpp` |
| Controller | `http://192.168.101.250:8443`（`POST /api/jobs` multipart，dev 机 `192.168.101.105` 同 /24 直连 HTTP 8443） |
| 提交方式 | `curl.exe -F "file=@capsule.zip;type=application/zip" -F caseId=... -F targetOs=windows -F targetLang=cpp` → 202 → 轮询 `GET /api/jobs/{id}` |
| 双侧定序 | Controller 先建源基线；**源失败则不建目标**（dual-runner ordering） |

## capsule 布局（本目录 = 提交内容，capsule.zip 7 项）

```
source/
  du.c            # 冻结源，sha256 d7ba9521…（源码不改，仅命令行宏）
  run_case.py     # du 只读汇总驱动：du -s . @ cwd=workspace，timeout 30，stdin DEVNULL
target/
  target.cpp      # 目标 C++（= 02-conversion/target.repair-2.cpp），sha256 cefe0aa7…
  run_case.py     # 同上驱动
comparison_manifest.json   # 源 linux/c cc C11 / 目标 windows/cpp g++ C++17 命令
input_profile.json         # argv ["-s","."]，观测维度 ["output"]，timeout 30
metadata.json              # 只读边界、预记期望、自修历史、哈希、隔离分级
```

- du 无伴随本地头，`source/`、`target/` 各仅含其 artifact + `run_case.py`。
- capsule 不含 `.env`、不含任何密钥；`run_case.py` 无联网、无外部命令、不读敏感文件，只读遍历 workspace 目录并打印一行汇总后退出。

## 真实回传结果（returned-evidence/）

| 文件 | 内容 |
| --- | --- |
| `job-id.txt` | `eval-20260928-073929-e89be213` |
| `state.json` | 作业状态机快照 |
| `evaluation_report.json` / `.md` | 权威报告：runVerdict=`blocked`、codeVerdict=`inconclusive`、behaviorVerdict=`inconclusive`、environment=`clean`、failure=`CODE_RESULT`（Source build failed; baseline cannot be established.） |
| `evidence-source.json` | 源侧 build `failed`、exitCode 1、durationMs 1057、stderr `du.c:55:10: fatal error: libutil.h: No such file or directory`；execution `blocked` |
| `evidence-target.json` | `{"detail":"evidence_not_found"}` —— 目标侧未构建（`execution.performed=false`，preflight/cleanup SKIPPED） |
| `comparison.json` | `{"detail":"comparison_not_found"}` —— 无对照 |
| `controller.log` | job 创建/完成时间戳 |

## 结论

**源基线在 glibc `FAILED_COMPILE`（`libutil.h` 缺失为首个硬阻断，其后尚有 SIGINFO/UF_NODUMP/st_flags 等 BSD 专有面）→ 目标侧构建被跳过 → 无目标 build 证据。** 与冻结 `01-frozen/frozen-inputs.md` §2.1 预记完全一致，为**失败类别数据点**：不改源、不放松命令到失真、不伪造目标通过。

编译质量阶段只据目标 build 证据判语法结论——目标未构建，故 syntaxVerdict = **INCONCLUSIVE**（非 PASS、非转换引入 FAIL）。详见 run 根 `result.md` 与 `evaluator_manifest.json`。