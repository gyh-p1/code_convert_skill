#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rc4 run-01 GENERATED-stage orchestration (LANGUAGE dimension, first datapoint, C->Go, same-OS).
Reads root .env for the configured translator model, builds a same-OS C->Go conversion request
(3 frozen C files: upstream WjCryptLib_Rc4.c/.h verbatim + authored thin CLI driver, plus inline
C->Go mapping guidance -- NO c-to-go Skill is injected because that Skill does not exist yet; it
is a step-05 OUTPUT seeded by this run, not an input), calls the OpenAI-compatible
/chat/completions endpoint, and saves the raw response, extracted target.gen.go, a reproducible
request.json (NO api key), and model metadata. The Agent only orchestrates; the Go is produced by
the model. Whatever the model produces is recorded honestly; no fabrication of a clean pass.
MAX_TOKENS defaults high (120000): deepseek-flash is a reasoning model whose reasoning_tokens eat a
low cap, yielding empty content + finish=length. Override via RC4_MAX_TOKENS.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\rc4-c-to-go\output\no-rag\run-01")
OUT = os.path.join(RUN, "02-conversion")
SRC = os.path.join(ROOT, r"docs\test\sources\wjcryptlib-rc4")

def read(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

def load_env(p):
    env = {}
    for line in read(p).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

env = load_env(os.path.join(ROOT, ".env"))
KEY = env.get("OPENAI_API_KEY", "")
MODEL = env.get("CODE_TRANSLATOR_MODEL", "")
BASE = env.get("CODE_TRANSLATOR_BASE_URL", "").rstrip("/")
TEMP = float(env.get("CODE_TRANSLATOR_TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.environ.get("RC4_MAX_TOKENS", "120000"))
if not (KEY and MODEL and BASE):
    print("ENV_INCOMPLETE", file=sys.stderr); sys.exit(2)

rc4_h = read(os.path.join(SRC, "WjCryptLib_Rc4.h"))
rc4_c = read(os.path.join(SRC, "WjCryptLib_Rc4.c"))
cli_c = read(os.path.join(SRC, "rc4_decrypt_cli.c"))
system_msg = (
    "你是代码转换执行模型，负责把给定的可移植 C 源（RC4 流密码模块 + 一个薄命令行驱动）整体转换为"
    "在 Windows 下 `go build` 成立的等价 Go：**单个 `package main` 源文件**。源为纯可移植 ANSI/C11，"
    "无平台 #ifdef，仅系统头 + 一个本地头。这是【同语言功能、跨语言 C→Go】转换，不掺入跨 OS 系统面。硬性要求：\n"
    "1. 尽力保持可观察行为——CLI 语义：用法 `program <hex-key> <hex-ciphertext>`；argc!=3 打印 usage 到 stderr 并"
    "以退出码 2 退出；key 必须是 1..256 字节的合法 hex，否则退出码 2；ciphertext 必须是合法 hex，否则退出码 2；"
    "RC4 初始化失败（KeySize==0）退出码 1；成功则把解密明文的原始字节写 stdout 并退出码 0。RC4 语义须与上游一致："
    "KSA 密钥调度（S[i]=i；j=(j+S[i]+key[i%keySize])%256 并交换）、PRGA 输出、DropN 丢弃前若干字节（本驱动 DropN=0）。\n"
    "2. C→Go 语言映射（本例考点，须换用 Go 习惯，勿机械照搬 C）：\n"
    "   - **头文件/预处理 → 包与导出**：Go 无 .h、无预处理器；把三份文件并入同一 `package main`；用**首字母大小写**表达导出/私有；无需任何本地 #include/import 自写头。\n"
    "   - **`#define SwapBytes(a,b)` 宏 → 函数或元组交换**：Go 无宏；用小函数或直接 `s[x], s[y] = s[y], s[x]`。\n"
    "   - **指针 / 手工字节缓冲 / `void*` 泛型缓冲 → `[]byte`**：`uint8_t S[256]` → `[256]byte`；`((uint8_t*)Key)[i%KeySize]` → `key[i%keySize]`；`void const*`/`void*` 无 Go 等价，一律用 `[]byte`（InBuffer/OutBuffer 同址可用同一切片或适当拷贝）。\n"
    "   - **定宽无符号与 mod-256 语义**：`uint32_t i,j` → `uint32`；`(uint8_t)i` → `byte(i)`；`(uint8_t)((hi<<4)|lo)` → `byte((hi<<4)|lo)`。Go **无隐式整型转换**，跨类型运算须显式 `byte(...)`/`uint32(...)`/`int(...)`；`byte` 天然模 256。\n"
    "   - **错误返回码 → `error`**：`Rc4Initialise`/`Rc4XorWithKey` 的 `0`/`-1`（KeySize==0）用 Go `error` 返回表达；`main` 的 `return 2/1/0` 用 `os.Exit(code)` 表达，**保持相同退出码语义**（用法错误=2、初始化失败=1、成功=0）。\n"
    "   - **`argv` 与十六进制解析 → `os.Args` + `encoding/hex`**：`argc/argv` → `os.Args`；手写 `nibble`/`hex_decode` 可改用标准库 `encoding/hex`（注意保持‘奇数长度/非法字符 → 退出码 2’的错误语义），或保留等价手写实现。\n"
    "   - **未使用的 import/变量是 Go 编译错误**：只 import 实际用到的包；若用了 `encoding/hex` 就必须用到它，否则不要 import；不要留下未使用的变量。\n"
    "3. 只做让该程序在目标 Windows `go build`（当前稳定 go 工具链）下成立所必需的改动，语义尽量等价；不新增进程执行/网络/文件写删/权限/隐蔽能力，不臆造不成立的等价。\n"
    "4. 不确定或源语义未定义处保守处理并在注释说明，不伪装成完全等价。\n"
    "5. 输出必须是【单个完整的 Go 源文件】的纯文本内容，即 target.go 的全部内容："
    "不加任何 Markdown 代码围栏、不加解释文字、不加省略号、不截断。"
    "第一行即源代码第一行（`package main`），最后一行即源代码最后一行。"
)

user_msg = f"""## 任务契约（已冻结）

- 源语言：C（按 C11 理解，纯可移植，无平台 #ifdef）；目标语言：**Go**（当前稳定 go 工具链，`package main`）。
- **同 OS 语言方向转换**：源与目标均在 Windows 构建；本例考的是 C 语言习惯→Go 语言习惯的映射，不掺跨 OS 系统面。
- 任务模式：多文件→单文件。把下面 3 份 C 文件（上游 RC4 模块 .c/.h + 薄 CLI 驱动 .c）整体转换为**一个** Go 源文件 `target.go`。
- 两侧编译命令：
  - 源侧基线（C11）：`gcc -std=c11 WjCryptLib_Rc4.c rc4_decrypt_cli.c -o program`
  - 目标侧（Go, Windows）：`go build -o program.exe`（单 package main，含 target.go）
- 场景：只读——按 hex key 对 hex 密文做 RC4 解密并把明文写 stdout。无网络、无文件写/删、无进程/命令执行。
- 须保留可观察行为：用法字符串、错误退出码（用法/hex 错误=2、RC4 初始化失败=1）、成功把明文原始字节写 stdout=0、RC4 KSA/PRGA/DropN 语义与上游一致（见 system 指令）。

## C → Go 映射指引（按需应用；这是本例考点，勿机械照搬 C 写法）

见 system 指令：头/预处理→包与导出、`#define` 宏→函数/元组交换、指针/字节缓冲/`void*`→`[]byte`、
定宽无符号与 mod-256→`byte`/`uint32` 显式转换、错误返回码→`error`+`os.Exit` 退出码、`argv`/hex→`os.Args`+`encoding/hex`、
**未使用 import/变量即编译错误**。（本项目 c-to-go Skill 尚不存在，故此处仅内联指引，不提供 Skill 快照。）

## 待转换的源（3 份 C 文件）

### 上游头文件 WjCryptLib_Rc4.h（逐字，被评译主体）
{rc4_h}

### 上游实现 WjCryptLib_Rc4.c（逐字，被评译主体）
{rc4_c}

### 薄命令行驱动 rc4_decrypt_cli.c（本项目自写 harness，非上游）
{cli_c}

## 输出

只输出 `target.go` 的完整纯文本内容。不要任何围栏、说明或省略。第一行为 `package main`。
"""

messages = [
    {"role": "system", "content": system_msg},
    {"role": "user", "content": user_msg},
]
payload = {
    "model": MODEL,
    "temperature": TEMP,
    "max_tokens": MAX_TOKENS,
    "stream": False,
    "messages": messages,
}

os.makedirs(OUT, exist_ok=True)
req_snapshot = {
    "endpoint": BASE + "/chat/completions",
    "model": MODEL,
    "temperature": TEMP,
    "max_tokens": MAX_TOKENS,
    "messages": messages,
    "input_sha256": {
        "WjCryptLib_Rc4.h": sha256_text(rc4_h),
        "WjCryptLib_Rc4.c": sha256_text(rc4_c),
        "rc4_decrypt_cli.c": sha256_text(cli_c),
    },
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
req_path = os.path.join(OUT, "target.gen.request.json")
with open(req_path, "w", encoding="utf-8") as f:
    json.dump(req_snapshot, f, ensure_ascii=False, indent=2)

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    BASE + "/chat/completions",
    data=data,
    headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=1800) as resp:
        raw = resp.read().decode("utf-8")
        status = resp.status
except urllib.error.HTTPError as e:
    raw = e.read().decode("utf-8", "replace")
    status = e.code
    with open(os.path.join(OUT, "target.gen.attempt-1-failed.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps({"status": status, "body": raw}, ensure_ascii=False, indent=2))
    print(f"HTTP_ERROR {status}", file=sys.stderr)
    print(raw[:2000], file=sys.stderr)
    sys.exit(3)

with open(os.path.join(OUT, "target.gen.response.raw.json"), "w", encoding="utf-8") as f:
    f.write(raw)

obj = json.loads(raw)
choice = obj["choices"][0]
content = choice["message"].get("content") or ""
finish = choice.get("finish_reason")

fence_stripped = False
c = content.strip("\n")
if c.startswith("```"):
    fence_stripped = True
    lines = c.split("\n")
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    content = "\n".join(lines)

go_path = os.path.join(OUT, "target.gen.go")
with open(go_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

meta = {
    "stage": "GENERATED",
    "model": obj.get("model"),
    "requested_model": MODEL,
    "temperature": TEMP,
    "max_tokens": MAX_TOKENS,
    "finish_reason": finish,
    "usage": obj.get("usage"),
    "response_id": obj.get("id"),
    "http_status": status,
    "fence_stripped": fence_stripped,
    "reasoning_present": bool(choice["message"].get("reasoning_content")),
    "request_sha256": sha256_text(read(req_path)),
    "output_sha256": sha256_text(content),
    "output_lines": content.count("\n") + 1,
    "output_chars": len(content),
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
with open(os.path.join(OUT, "target.gen.model.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print("OK status=%s finish=%s lines=%s chars=%s fence_stripped=%s" % (
    status, finish, meta["output_lines"], meta["output_chars"], fence_stripped))
print("usage=%s" % json.dumps(obj.get("usage")))
if finish == "length":
    print("WARN: finish_reason=length -> output may be truncated", file=sys.stderr)
if not content.strip():
    print("WARN: empty content", file=sys.stderr)

