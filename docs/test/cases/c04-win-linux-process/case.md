# C04 候选规格：Windows → Linux / 受限进程调用

> 状态：candidate（仅规格；无源代码；不可执行）

## 源 fixture 边界

新建 Win32 C 单文件用 `CreateProcess` 启动同一 case 内审阅过的固定 helper；目标 Linux C++ 使用适当的直接进程 API。命令、argv、cwd、环境标记均为常量或由受限 harness 提供的 case 路径；不使用 shell、不执行系统管理命令、不接受源码外命令、不提权。helper 只向 stdout/stderr 输出固定合成标记并返回预设码。

## 预设 oracle

- helper 的 argv 边界、cwd 和唯一合成环境变量逐项相同；不把参数数组改为 shell 拼接。
- 固定 stdout/stderr 字节和 exit code 精确对照；分别覆盖正常码、非零码、启动失败和有限超时。
- 父子进程等待、超时终止、句柄/fd 关闭及子进程回收均有明确检查；结束后没有遗留 helper。
- 只能执行该 helper 的固定路径；运行审计中出现其他进程或命令立即停止并判安全失败。

## 安全 Gate

仅在隔离 VM 中运行自带的可审阅 helper；不调用 cmd、PowerShell、shell 或外部程序。此文件未写、未编译、未运行；进程 API 映射及 helper 构建方式待审阅。
