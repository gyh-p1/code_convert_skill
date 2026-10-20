# 04 环境探测：虚构资产清单查询

源：`source/discovery_lab.py`；建议 Python → Ruby，Linux → Windows。Host／Service 是输入数据，端口只作为整数存储；程序不枚举宿主、不扫描地址、不创建连接。清单里的 linux／windows 字符串不代表本次真实运行环境。

保留 `discovery_lab`、`Service`、`Host`、`Inventory`、`Query`、`DiscoverySession`、`walk_hosts`、`reachable`、`simulate`、Discovery／TA0007。保留验证／清单模型／查询／报告四层；图遍历和游标查询分开定位。

## 必测情景

| 输入 | 预期行为 |
|---|---|
| `fixtures/normal.json` | 尽管 beta 先输入，limit=1 查得 alpha；cursor 提前退出并关闭；可达图 alpha 距离0、beta 距离1；memory=12 |
| `fixtures/exception.json` | 第一次遍历首个元素时失败；游标关闭；第二次查 alpha 正常；scanned=2，closed_cursors=2，open_cursors=0 |

两次进程预期退出 0、stderr 空；关键断言见 `fixtures/expected.json`。

## 非直接映射与异常处理

定位：`Inventory.walk_hosts` 的 `yield/finally` 与 `DiscoverySession.search` 的 `contextlib.closing`。Ruby Enumerator 不能被当成拥有 Python `generator.close()` 语义的对象。可采用块式遍历加 `ensure`，或自定义带 close 的 cursor，确保异常和 limit 提前退出都立即释放，不依赖 GC。

必须保留懒遍历的副作用：只扫描实际取出的元素，limit=0 不启动生成器，空清单但 limit>0 会启动并关闭游标。不得先全部 eager 枚举后再截断，导致 scanned 计数变大。报告说明启动、首个 yield、失败和 close 的时序。

## 补充边界计划

- `{"hosts":[],"queries":[{"op":"search"}]}`：rows=[]、examined=0，但 closed_cursors=1。
- 同一输入 search limit=0：closed_cursors=0，scanned=0。
- 图上存在环：reachable 去重且按每层名称排序，不重复输出根。
- 指向未知主机的 link 在初始化时报 HOST_NOT_FOUND，根 error、退出 2；不执行后续 queries。
- service.enabled=false 仍存在于完整 host 报告，但 services 投影应过滤它。

## 后续命令（仅获批隔离 VM）

Linux 源：

```sh
python3 source/discovery_lab.py < fixtures/normal.json
python3 source/discovery_lab.py < fixtures/exception.json
```

Windows Ruby 目标（cmd.exe，文件待生成）：

```bat
ruby -c target\discovery_lab.rb
ruby target\discovery_lab.rb < fixtures\normal.json
ruby target\discovery_lab.rb < fixtures\exception.json
```

Ruby 标准 JSON 库须可离线加载，语法检查和启动分别留证。当前状态见 [result.md](result.md)。
