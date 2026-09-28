#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stest run-01 GENERATED-stage orchestration (step-04 POSIX->Windows filesystem).
Reads root .env for the configured translator model, builds a cross-OS C->C++
conversion request (source snapshot stest.c + arg.h + selected Skill snapshots +
frozen task contract), calls the OpenAI-compatible /chat/completions endpoint,
and saves the raw response, extracted target.gen.cpp, a reproducible request.json
(NO api key), and model metadata. The Agent only orchestrates; the C++ is produced
by the configured model.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\stest-fs-posix-to-win\output\no-rag\run-01")
OUT = os.path.join(RUN, "02-conversion")

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
MAX_TOKENS = int(os.environ.get("STEST_MAX_TOKENS", "32000"))
if not (KEY and MODEL and BASE):
    print("ENV_INCOMPLETE", file=sys.stderr); sys.exit(2)

stest_c = read(os.path.join(ROOT, r"docs\test\sources\dmenu-stest\stest.c"))
arg_h = read(os.path.join(ROOT, r"docs\test\sources\dmenu-stest\arg.h"))
sk_dir = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))
sk_abi = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\type-abi.md"))
sk_fs = read(os.path.join(ROOT, r"skills\systems\posix-windows-filesystem\SKILL.md"))
system_msg = (
    "你是代码转换执行模型，负责把给定的 POSIX/Linux C 源翻译单元转换为在 Windows 下"
    "成立的等价 C++。硬性要求：\n"
    "1. 严格保持可观察行为——命令行 flag 语义、退出码约定（无匹配返回 1、有匹配返回 0、"
    "用法错误 exit(2)）、stdout 内容（匹配即 puts(name)）、错误路径与副作用一律不变。\n"
    "2. 这是【跨 OS 迁移 POSIX→Windows】：源用 stat/lstat/access(F_OK/R_OK/W_OK/X_OK)/"
    "opendir/readdir/getline/S_ISBLK/S_ISCHR/S_ISDIR/S_ISREG/S_ISLNK/S_ISFIFO 等 POSIX "
    "文件系统接口，其中部分在 Windows/MinGW 并非同名等价（如无 lstat、X_OK 不被 _access 支持、"
    "无 S_ISLNK/S_ISBLK/S_ISCHR/S_ISFIFO、getline/PATH_MAX 可能缺）。只做在目标 C++17/Windows "
    "工具链下让该翻译单元成立所必需的最小改动，保持语义等价；平台缺失能力按保守、可观察行为一致的方式处理，"
    "不新增进程/网络/文件写/权限能力。\n"
    "3. 不确定或源语义未定义处保留原样并保守处理，不臆造等价实现。\n"
    "4. 伴随本地头 `arg.h` 已随源提供，**保持 `#include \"arg.h\"` 不变，不要把 arg.h 的内容并入输出**。\n"
    "5. 输出必须是【单个完整的 C++ 源文件】的纯文本内容，即 target.cpp 的全部内容："
    "不加任何 Markdown 代码围栏、不加解释文字、不加省略号、不截断。"
    "第一行即源代码第一行，最后一行即源代码最后一行。"
)

user_msg = f"""## 任务契约（已冻结）

- 源语言：C（按 C11 理解，纯 POSIX）；目标语言：C++（C++17）。
- **做跨 OS 迁移：POSIX/Linux → Windows**。目标侧工具链为 Windows x64 MinGW/UCRT64 `g++ -std=c++17`。
- 任务模式：短单文件转换。把下面的 `stest.c` 翻译单元整体转换为一个 C++ 源文件 `target.cpp`。
- 伴随本地头 `arg.h`（dmenu 的 ARGBEGIN/ARGEND 参数解析宏）已随源提供，**保持 `#include \"arg.h\"` 不变，不要把 arg.h 的内容并入输出**。
- 两侧编译命令：
  - 源侧基线（POSIX，Linux）：`cc -std=c11 stest.c -o program`
  - 目标侧（Windows）：`g++ -std=c++17 target.cpp -o program`
- 场景：只读文件系统遍历，无网络、无文件写入、无进程/命令执行。
- 须保留 stest 语义：flag 数组 `flag[26]`、`FLAG(x)` 宏、`-n/-o` 取时间基准、`-l` 目录遍历、`-v` 取反、`-q` 命中即 exit(0)、无参数时从 stdin 逐行读取、退出码 `match?0:1`、`usage()` exit(2)。

## 可用转换知识（Skill 快照，按需应用；不要照抄进代码）

### C → C++ 语言方向
{sk_dir}

### 头文件与宏可用性
{sk_hdr}

### 类型、接口与 C ABI
{sk_abi}

### POSIX ↔ Windows 文件路径系统方向
{sk_fs}

## 伴随本地头 arg.h（保持 #include，不并入输出，仅供理解宏）

{arg_h}

## 待转换的源翻译单元 stest.c

{stest_c}

## 输出

只输出 `target.cpp` 的完整纯文本内容（含被保留的 `#include \"arg.h\"`）。不要任何围栏、说明或省略。
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

# reproducible request snapshot (no key)
os.makedirs(OUT, exist_ok=True)
req_snapshot = {
    "endpoint": BASE + "/chat/completions",
    "model": MODEL,
    "temperature": TEMP,
    "max_tokens": MAX_TOKENS,
    "messages": messages,
    "input_sha256": {
        "stest.c": sha256_text(stest_c),
        "arg.h": sha256_text(arg_h),
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
    with urllib.request.urlopen(req, timeout=1200) as resp:
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

# deterministic fence strip (recorded)
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

cpp_path = os.path.join(OUT, "target.gen.cpp")
with open(cpp_path, "w", encoding="utf-8", newline="\n") as f:
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

