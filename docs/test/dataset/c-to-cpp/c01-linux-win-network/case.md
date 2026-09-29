# C01：uhttpd Linux → Windows（历史探索）

> 状态：HISTORICAL-EXPLORATION（run-01 文本稿、run-02 获批隔离探索已结束；原固定四例任务已[取消](../../../../项目开发规范.md#当前开发阶段与退出条件)）
> 共享源样例：`当前 run 的 source/ 冻结副本`（共享源快照已清理；冻结副本见当前 run 的 `source/` 目录）
> 上游来源与许可：上游来源说明已清理；冻结副本见当前 run 的 `source/` 目录 与随附 GPL-2.0-or-later `LICENSE`

## 转换方向与标签

- 源：C；本次按 Linux x64 与 POSIX `UNIX` 编译分支理解。
- 目标：C++；Windows x64。MSVC-compatible C++17 是文本探索假设，尚未冻结工具链。
- 场景：`network-io`、`file-io`、`concurrency`；HTTP 静态服务、socket accept/并发线程、docroot 文件读取、GET/HEAD 和错误响应。
- ATT&CK：tactic/technique `none`；仅凭 HTTP/socket 服务不足以推断对抗行为。
- 输出：[`run-01/target.cpp`](output/no-rag/run-01/target.cpp) 为此前智能体文本探索稿；[`run-02/target.cpp`](output/no-rag/run-02/target.cpp) 由根 `.env` 配置模型生成并经同模型修订。run-02 的修订稿在获批隔离评估中通过五个固定 loopback HTTP 请求的输出比较；oracle/输入尚未冻结，两者都不是正式 No-RAG 基线。
- 尺寸：1,317 物理行，约 1,092 LOC；**超过 700 物理行计划上限**。这是用户确认的超限探索候选，不计入 ≤700 行边界验证。

## 可观察运行边界

获批执行时只用一次性隔离环境；启动参数固定为 loopback `127.0.0.1`、临时高位端口和本 case 空临时 docroot。必须显式传 `-i 127.0.0.1`、`-p <隔离端口>`、`-d <case临时目录>`；不得用默认监听配置、真实内容目录或公网接口。客户端仅请求本地固定路径，不发送任意路径/压力流量。结束后停止服务并销毁临时目录。

此前 run-02 已获一次逐例隔离执行授权，见其 `04-evaluation/` 证据；该授权不扩展到新的 run、样例或工具链。原四例功能 oracle 计划已经取消；历史五个请求的有限结果仅归属 run-02。任何新任务仍须另立方案并核对授权与隔离条件。

## 行为 oracle 草案

使用固定临时文档集：`index.html` 与一个普通文本文件，内容为固定 ASCII/UTF-8 字节。逐项比较源 C 与目标 C++：

1. `GET /`：HTTP 状态、稳定响应头、Content-Length 与 body 字节；
2. `GET /known.txt`：状态及 body 字节精确相同；
3. `HEAD /known.txt`：状态和实体头与约定一致，body 为空；
4. `GET /missing.txt`：404 状态与错误响应类别；
5. 未注册扩展名：415（或源码实际返回类别），响应长度/错误说明一致；
6. stderr 中仅比较预先选定的稳定错误/启动信息，剔除时间戳、端口等环境变量；进程启动失败与请求处理失败分别记录；
7. 检查工作线程、客户端 socket、文件句柄能在正常请求/失败路径清理，无残留服务进程/外部监听。

oracle 冻结时需根据源代码响应格式挑选稳定头部字段；不把 Date、动态端口等环境字段作字节等价要求。不得事后因转换失败而放宽 oracle。

## 静态风险观察（非完整审计）

- 源码支持 `-i` 限定绑定地址、`-d` 更换服务目录、`-p` 指定端口；必须固定为 loopback/临时目录。
- 请求路径会触发 docroot 下文件读取；仅放入无敏感固定文件，检查路径归一化规则后再批准执行。
- 静态检索未发现命令/进程创建调用；`_killthread` 定义中包含强制线程终止 API，但本文件未见其调用点。这不是完整安全审计。
- 单文件有多线程与跨平台兼容封装；目标侧工具链/标准、线程 API、socket 错误码和 POSIX/Windows 路径行为仍须按 [source-analysis.md](output/no-rag/run-01/source-analysis.md) 记录的缺口审阅。
- 上游源文件已经内含 Windows 实现；C01 目标稿复用它，因此存在目标分支泄漏，不能据此声称验证了独立 POSIX→Win32 移植能力。
- GPL-2.0-or-later 源码随附原许可证。若对外分发目标/修改版本，需完成合规审查并保留版权/许可声明。

本 case 是旧固定四例中唯一实际产生转换 run 的任务。拟议的 Windows→Linux 反向 C02 从未产生 run，已随专项取消；uhttpd 源仍因本历史探索而保留。
