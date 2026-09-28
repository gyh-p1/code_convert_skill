# C → C++ 转换记录

下表列的是**逐例证据**，不是方向总体通过率。`result.md` 说明最终交付版本、工具链、修订与限制；`case.md` 说明任务边界。

| case / run | 行为场景 | 来源性质 | 目标编译 | 功能证据 | 记录 |
|---|---|---|---|---|---|
| C01 uhttpd run-01 | HTTP 服务 | 上游真实服务；自带 Windows 分支，超 700 行 | UNVERIFIED；智能体文本探索稿 | UNVERIFIED | [case](c01-linux-win-network/case.md) · [result](c01-linux-win-network/output/no-rag/run-01/result.md) |
| C01 uhttpd run-02 | HTTP 服务 | 同一上游源；非独立跨 OS 移植样例 | 最终修订稿在 MinGW 探查工具链 PASS；正式目标未冻结 | 五个固定 loopback 请求的有限输出匹配，其他行为未验证 | [result](c01-linux-win-network/output/no-rag/run-02/result.md) |
| fe run-01 | Lisp 解释器 | 上游独立 C 源 | 第三方目标 build PASS | 未计分 | [case](fe-lisp-c-to-cpp/case.md) · [result](fe-lisp-c-to-cpp/output/no-rag/run-01/result.md) |
| stest run-01 | 文件元数据/遍历 | 上游 dmenu C 源 | 第三方目标 build PASS | 未计分；liveness 匹配不构成功能验证 | [case](stest-fs-posix-to-win/case.md) · [result](stest-fs-posix-to-win/output/no-rag/run-01/result.md) |
| realpath run-01 | 路径规范化 | 上游 FreeBSD C 源 | 第三方目标 build PASS | 未计分；跨 OS 路径文本不同 | [case](realpath-fs-posix-to-win/case.md) · [result](realpath-fs-posix-to-win/output/no-rag/run-01/result.md) |
| pwd run-01 | 当前目录/路径身份 | 上游 FreeBSD C 源 | 第三方目标 build PASS | 未计分；跨 OS 路径文本不同 | [case](pwd-fs-posix-to-win/case.md) · [result](pwd-fs-posix-to-win/output/no-rag/run-01/result.md) |
| du run-01 | 递归磁盘用量 | 上游 FreeBSD C 源 | **INCONCLUSIVE**：Linux 源基线缺 `libutil.h`，目标未构建 | 未计分；两侧未完成比较 | [case](du-fs-posix-to-win/case.md) · [result](du-fs-posix-to-win/output/no-rag/run-01/result.md) |
| Chain Reactor 网络 run-01 | 受控网络连接（真实 Linux API 的对抗模拟组件） | 发布方固定提交 + MIT；主源 559 行，伴随 C 依赖另计 | 第三方 Linux GNU C++17 目标 build **PASS**；源基线亦 PASS | 两侧正常/拒绝 loopback 输出在 case receiver 可见范围匹配；仅信息记录，不计功能率 | [case](chain-reactor-network-linux/case.md) · [result](chain-reactor-network-linux/output/no-rag/run-01/result.md) |

**覆盖缺口**：这一方向尚无已冻结且通过功能 oracle 的真实攻击链样例；fe 和文件系统四例主要考编译与平台 API。C01 虽有真实网络服务与有限动态证据，源自带目标平台分支，不能证明从 POSIX 逻辑独立移植。下一轮选样需补真实攻防行为与可观测义务。
