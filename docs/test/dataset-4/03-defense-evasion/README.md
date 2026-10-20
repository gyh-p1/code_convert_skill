# 03 防御规避：惰性字节变换

源：`source/encoding_lab.py`；建议 Python → C++，Windows → Linux。只变换输入的合成文本，不加载或执行内容。保留用户类别“防御规避”，TA0005 的称谓采用仓库本地快照的 legacy category／Stealth 口径。

保留 `encoding_lab`、`Blob`、`Step`、`TransformEngine`、`RecipeSession`、`STEP_FIELDS`、`simulate` 与战术常量。维持验证／不可变 Blob／变换器／配方会话／入口的职责边界；不同表示的名称 `binary`、`utf-8`、`base64` 不得擅自统一。

## 必测情景

| 输入 | 预期行为 |
|---|---|
| `fixtures/normal.json` | abc 经 base64 编解码恢复 616263；长度 3→4→3；最终 representation=binary，same_bytes_as_input=true |
| `fixtures/exception.json` | 第一步负步长反转；第二步 stride=0 报 ZERO_STRIDE；atomic=true 还原 abc／utf-8，trace 保留已完成的第一步 |

两次进程预期退出 0、stderr 空；断言见 `fixtures/expected.json`。

## 非直接映射与异常处理

定位：`TransformEngine.slice`。C++17 的容器没有 Python `slice(start, stop, stride)` 的完整省略边界／负索引语义，应显式区分 null 和已指定的 -1，按步长方向归一化边界，然后访问字节；stride=0 在修改状态前报错。

`RecipeSession.run_recipe` 原子失败恢复 current 和 checkpoints，但保留失败前 trace；替代实现不能回滚 trace 或误保留变换后的 current。异常报告需说明 Python 切片到 C++ 索引算法及事务范围。允许换数据结构；不允许按 Unicode 字符而不是字节反转。

## 补充边界计划

- 从正常输入将步骤替换成 `[{"name":"slice","stride":-1}]`：最终 hex=636261。
- 步骤换成 `[{"name":"slice","stop":-1,"stride":-1}]`：最终空字节；与未提供 stop 不同。
- 异常输入仅把 atomic 改 false：最终 cba／binary，rolled_back=false。
- 非法 base64 返回 INVALID_BASE64；超限解压、截断、尾随 zlib 数据必须各自保持错误。
- 非 UTF-8 二进制 payload 的 summary.text 为 null，不可替换非法字节后宣称等价。

## 后续命令（仅获批隔离 VM）

Windows 源（cmd.exe）：

```bat
python source\encoding_lab.py < fixtures\normal.json
python source\encoding_lab.py < fixtures\exception.json
```

Linux 目标计划：完整 C++17 工程，入口基名 encoding_lab；离线冻结 JSON、Unicode 规范化、zlib、SHA-256 实现。构建命令必须由生成后的实际工程清单确定，不能先假定单个 `.cpp` 无外部依赖即可链接。已构建后的候选启动命令：

```sh
./target/encoding_lab < fixtures/normal.json
./target/encoding_lab < fixtures/exception.json
```

即使核心输入未调用压缩／Unicode 规范化，目标仍须完整实现源码公开操作，不能只生成通过两份输入的特化代码。当前状态见 [result.md](result.md)。
