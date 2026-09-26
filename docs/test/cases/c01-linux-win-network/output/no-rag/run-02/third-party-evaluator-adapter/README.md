# C01 run-02 第三方评估记录

状态：探索性、已执行；不是正式 No-RAG 基线。修复前的 `run-02/target.cpp` 保存在 `target.pre-repair.cpp`，当前 `target.cpp` 是经第三方诊断和配置模型补丁修复的版本。所有构建和运行均由旧仓库 Remote Controller 调度到报告所列 Linux/Windows x64 VM Runner；本仓库没有本地编译或运行。

## Job 时间线

| Job | 目的 | 结果 |
|---|---|---|
| `eval-20260926-052137-b10a6e2f` | 初次比较；Windows 命令以 MinGW `g++ -D_MSC_VER` 选目标分支 | Linux 源编译/运行成功；目标构建失败。除 `min` 未声明外，强行定义 `_MSC_VER` 还触发 MinGW 系统头 `__uuidof` 诊断；行为未评估。不可把该次所有诊断都归因目标代码。 |
| `eval-20260926-052507-8c9beb3a` | 单变量诊断：只将分支宏换为 `-D__POCC__` | 源端成功；目标端仍只报 `target.cpp:718` 的 `min` 未声明；目标未运行。 |
| `eval-20260926-052820-e96bf2ee` | `.env` 配置模型 `deepseek-flash` 根据第三方错误建议最小修复；Agent 将单行替换机械应用到独立副本 | Linux 源与 Windows 修订目标均构建、运行成功；Controller：`codeVerdict=passed`、`behaviorVerdict=matched`、环境 clean。 |

## 修订与工具链边界

修订副本：`target.repair-01.cpp`。唯一替换为：

```diff
- len = min(url_length, name_size - 1);
+ len = (url_length < name_size - 1) ? url_length : (name_size - 1);
```

模型原始建议、响应元数据与 SHA-256 见 `model-repair-proposal-retry.json`、`model-repair-metadata-retry.json`、`repair-provenance.json`。首个模型修复响应达到 token 上限且不完整，未应用；随后禁用 reasoning 重试成功。

成功的诊断命令是 `g++ -D__POCC__ -std=c++17 target.cpp -o program.exe -lws2_32`，Runner 诊断表明 MinGW/UCRT64。`__POCC__` 仅用于选中源码内 Windows 兼容分支；这不是 Pelles C 编译结果，也不是 MSVC/SDK 编译证明。原始基线 target 仍未通过该探查编译。

## 行为证据边界

固定 helper 只绑定服务到 `127.0.0.1`，在独立工作目录创建临时 docroot，发出 GET `/`、GET 已知文件、HEAD 已知文件、GET 缺失文件和未知扩展请求，再终止服务并清理 fixture。比较只观察 stdout JSON 结构；该轮 1/1 applicable dimension matched。没有验证并发压力、路径边界、安全属性、文件系统副作用、进程树或网络遥测。Controller 返回的证据未说明 VM 的外网出口策略，因此不声称已验证 OS 级 egress isolation；本结果仅记为用户授权的独立 VM 执行。

`repair-01-report.json` 是 Controller canonical report；同前缀 `evidence-source/target.json`、`comparison.json` 为原始证据。另两个 job 的报告、source/target evidence、comparison 与生命周期日志分别保存在 `remote-*`、`pocc-*` 文件。完整输入 capsule 和 hash/provenance 一并保留。
