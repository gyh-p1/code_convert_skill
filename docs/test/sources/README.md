# 共享源快照索引

这里只保存已有[转换数据集](../dataset/README.md) case 消费的上游源快照、必要本地头文件、许可证和来源说明。源文件保持冻结，不因目录整理而改写；case 私有的无许可确认 fixture 留在[候选区](../candidates/long-file-structure-candidate/case.md)。

| 源目录 | 来源/许可说明 | 当前消费者 | 用途与证据边界 |
|---|---|---|---|
| [dmenu-stest](dmenu-stest/source.md) | dmenu，MIT/X | [stest](../dataset/c-to-cpp/stest-fs-posix-to-win/case.md) | C→C++ POSIX→Windows；目标编译 PASS |
| [fe](fe/source.md) | rxi/fe，MIT | [fe](../dataset/c-to-cpp/fe-lisp-c-to-cpp/case.md) | C→C++；目标编译 PASS，879 行超 700 计划上限 |
| [freebsd-du](freebsd-du/source.md) | FreeBSD，BSD-3 | [du](../dataset/c-to-cpp/du-fs-posix-to-win/case.md) | 源基线缺 `libutil.h`，目标未构建 |
| [freebsd-pwd](freebsd-pwd/source.md) | FreeBSD，BSD-3 | [pwd](../dataset/c-to-cpp/pwd-fs-posix-to-win/case.md) | C→C++ POSIX→Windows；目标编译 PASS |
| [freebsd-realpath](freebsd-realpath/source.md) | FreeBSD，BSD-3 | [realpath](../dataset/c-to-cpp/realpath-fs-posix-to-win/case.md) | C→C++ POSIX→Windows；目标编译 PASS |
| [uhttpd](uhttpd/source.md) | PJO2/uhttpd，GPL-2.0-or-later | [C01 历史探索](../dataset/c-to-cpp/c01-linux-win-network/case.md) | 保留 run-01/02 可追溯性；原固定四例计划已取消，1,317 行超上限 |
| [wjcryptlib-rc4](wjcryptlib-rc4/source.md) | WjCryptLib，文件头公有领域声明；CLI 驱动自写 | [RC4](../dataset/c-to-go/rc4-c-to-go/case.md) | C→Go 探索；Windows 文件名大小写哈希排序故障，目标未构建 |
| [chain-reactor-network](chain-reactor-network/source.md) | Red Canary Chain Reactor 固定提交，MIT | [Chain Reactor 网络 case](../dataset/c-to-cpp/chain-reactor-network-linux/case.md) | 主源 Linux C 559 行、伴随依赖另计；最终目标在隔离 Linux GNU C++17 下 build PASS，有限 loopback 输出仅信息记录 |

这八份源都有当前数据集 case 消费者，不按旧“四例格子”复制或删除。来源说明中的历史选择理由不等于当前测试计划。新增源时先写逐文件来源/许可、上游版本、原件/改写差异及目标 case；未经审阅的旧用例只留在[候选索引](../dataset/legacy-candidates.md)，不整包复制到这里。
