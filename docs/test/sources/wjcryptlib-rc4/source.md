# 共享源样例：WjCryptLib RC4（公有领域 C）+ 薄 CLI 驱动

> 用途：`code_convert` **语言方向维度**首个真实数据点的冻结源。方向 **C → Go**，**同 OS**（隔离语言变量）。攻防定位：RC4 是被大量真实恶意软件用于配置/字符串混淆、且是 CTF 常见的公开、已被攻破的流密码；此处作为**通用双用途编解码原语**冻结，不构成武器、加载器或规避工具。

## 1. 上游来源与许可

- 上游仓库：`WaterJuice/WjCryptLib`（<https://github.com/WaterJuice/WjCryptLib>）。
- 取用文件：`lib/WjCryptLib_Rc4.c`、`lib/WjCryptLib_Rc4.h`，分支 `master`，取用于 2026-09-28（raw.githubusercontent.com）。
- 许可：**公有领域**。文件头逐字声明：`This is free and unencumbered software released into the public domain - June 2013 waterjuice.org`（Unlicense 式奉献；仓库根无单独 LICENSE 文件，以文件头声明为准）。
- 提交 SHA：本次 API 查询遭 GitHub 未认证限流，暂缺具体 commit；**完整性以下列 sha256 为绑定锚**（真正的冻结保证），provenance 以仓库+路径+分支+取用日期记录。

## 2. 冻结文件与完整性（sha256）

| 文件 | 行数 | sha256 | 性质 |
|---|---|---|---|
| `WjCryptLib_Rc4.c` | 167 | `9c77e9b3f45dfe6162b1694b57bda665a3b24490841fa5ef95952dd1a73a72c6` | **上游逐字**（被评译主体） |
| `WjCryptLib_Rc4.h` | 94 | `f33d3a78e2f0642ad0c99d226f29eaaac844c82a0eaaae42a377b4222984f7c0` | **上游逐字**（被评译主体） |
| `rc4_decrypt_cli.c` | 94 | `9ab3ebbb8926bf580162ba2307401f8b1bb923e5ba944ef85a0a508ef5789083` | **本项目自写薄驱动**（非上游） |

- 上游 `.c/.h` 复制入库后 `Get-FileHash` 与 raw 下载一致，逐字未改。
- 被评的翻译主体是**上游 RC4 模块**（`Rc4Context` 结构 + `Rc4Initialise`/`Rc4Output`/`Rc4Xor`/`Rc4XorWithKey`）。驱动仅把该模块接到命令行以便双侧构建可运行，**不含任何自有密码学逻辑**，按本项目既定「可执行时默认补入口」政策补入，并在冻结记录中标注为 harness。

## 3. 可移植性与安全形态

- 依赖仅 `<stdint.h>`（头）与 `<stdlib.h>`（实现）；驱动另用 `<stdio.h>`/`<string.h>`。**无任何平台专有头、无 `#ifdef _WIN32`/POSIX 分支**——纯可移植 ANSI/C11，任一 OS 工具链均可干净构建（故选**同 OS**，且落在已确认支持 `c`+`go` 的 Windows Agent，规避 du 式「源基线编不过→目标跳过」的取不到证据死路）。
- 行为：只读——从 `argv` 取十六进制 key 与密文，RC4 解密后把明文写 `stdout`。**无网络、无文件写/删、无进程/命令执行、无敏感文件访问**。ATT&CK：`none`。
- liveness 采用公开 RC4 测试向量（key `"Key"` = hex `4b6579`，密文 `bbf316e8d940af0ad3` → 明文 `Plaintext`），确定性输出，双侧可比对。
