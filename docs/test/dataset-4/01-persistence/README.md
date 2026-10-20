# 01 持久化：虚拟启动条目事务

源：`source/persistence_lab.py`；建议 Python → Go，Windows → Linux。原创内存仿真，只存惰性标签，模拟 boot 只产生 JSON 标签，不安装启动项、不写注册表、不执行标签。

保留基名 `persistence_lab`，以及 `StartupEntry`、`PersistenceStore`、`canonical_name`、`transaction`、`dispatch`、`simulate`、`TACTIC`、`TACTIC_ID` 等符号／词根。输入验证、启动项数据模型、事务／操作分派、JSON 入口保持逻辑模块划分。Go 无类方法语法时允许映射成同名结构体方法并记录对应关系。

## 必测情景

| 输入 | 预期行为 |
|---|---|
| `fixtures/normal.json` | 安装一次性 Demo；第一个 boot 发出 welcome 并消费条目；第二次没有 emission；revision=2、boots=2 |
| `fixtures/exception.json` | 事务安装后注入失败，返回 INJECTED_FAILURE；安装、revision、审计均回滚；后续 boot 可继续且无条目 |

精确关键断言见 `fixtures/expected.json`。两情景预期进程退出 0、stderr 空；须另比较完整输出。

## 非直接映射与异常处理

定位：`PersistenceStore.transaction` 的 `@contextmanager`、`copy.deepcopy`，以及 `dispatch` 的 `fail_after`。Go 不提供 Python 生成器上下文协议和通用深复制；采用显式快照结构和保证错误出口恢复的代码。快照必须复制条目字段、列表及字典，不能只复制 map 引用。恢复 revision、tick、boot_count、emissions、events，并保留操作层错误结果。

允许内部以错误返回值替换 Python 异常；不允许吞错、只撤销条目而遗留 revision／事件、将原样本事务改成部分提交。报告需列出快照字段和恢复时序。

## 补充边界计划

- `{"operations":[]}`：空状态、revision=0、boots=0，退出 0。
- `{"operations":[{"op":"advance","delta":true}]}`：操作错误 INTEGER_REQUIRED／delta；不得把 bool 当整数。
- 依次安装名称 `Straße`、`STRASSE`：第二次应 ALREADY_EXISTS；必须保持 NFC 后 casefold 的键语义，不能用 ASCII lower 替代。
- expires=0 的条目在 tick=0 的 boot 不发出；`expire` 删除它。优先级相同按规范化键排序。

## 后续命令（仅获批隔离 VM）

从本例目录启动，源侧 Windows `cmd.exe`：

```bat
python source\persistence_lab.py < fixtures\normal.json
python source\persistence_lab.py < fixtures\exception.json
```

未来目标侧 Linux 候选命令：

```sh
go build -o target/persistence_lab target/persistence_lab.go
./target/persistence_lab < fixtures/normal.json
./target/persistence_lab < fixtures/exception.json
```

这些目标文件尚不存在。NFC／casefold 若使用离线 Unicode 包，必须交付及冻结对应依赖和实际构建命令。Windows／Linux 都只使用 stdin/stdout；不存在将标签映射到真实启动服务的要求。

本例的非初始访问路由期望为通用生成策略。初始访问分支另见根目录 `routing-cases.json`，本例不构成初始访问识别正样本。当前状态见 [result.md](result.md)。
