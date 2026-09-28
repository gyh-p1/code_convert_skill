#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fe run-01 GENERATED-stage orchestration.
Reads root .env for the configured translator model, builds a conversion request
(source snapshot + selected Skill snapshots + task contract), calls the OpenAI-
compatible /chat/completions endpoint, and saves the raw response, the extracted
target.gen.cpp, a reproducible request.json (NO api key), and model metadata.
The Agent only orchestrates; the C++ code is produced by the configured model.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\fe-lisp-c-to-cpp\output\no-rag\run-01")
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
MAX_TOKENS = int(os.environ.get("FE_MAX_TOKENS", "120000"))
if not (KEY and MODEL and BASE):
    print("ENV_INCOMPLETE", file=sys.stderr); sys.exit(2)

fe_c = read(os.path.join(ROOT, r"docs\test\sources\fe\fe.c"))
fe_h = read(os.path.join(ROOT, r"docs\test\sources\fe\fe.h"))
sk_long = read(os.path.join(ROOT, r"skills\workflows\long-file-conversion\SKILL.md"))
sk_dir = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))
sk_abi = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\type-abi.md"))

system_msg = (
    "你是代码转换执行模型，负责把给定的 C 源翻译单元转换为等价的 C++。"
    "硬性要求：\n"
    "1. 严格保持可观察行为——公开函数签名、返回值约定、结构体/联合布局、"
    "整数宽度与符号性、控制流、错误路径、资源生命周期、标准输出内容与副作用一律不变。\n"
    "2. 只做在目标 C++ 标准下让该翻译单元成立所必需的最小改动；不为“现代化”"
    "重写逻辑、不改所有权模型、不改分配方式、不新增进程/网络/文件/权限能力。\n"
    "3. 不确定或源语义未定义处保留原样，不臆造等价实现。\n"
    "4. 输出必须是【单个完整的 C++ 源文件】的纯文本内容，即 target.cpp 的全部内容："
    "不加任何 Markdown 代码围栏、不加解释文字、不加省略号、不截断。"
    "第一行即源代码第一行，最后一行即源代码最后一行。"
)

user_msg = f"""## 任务契约（已冻结）

- 源语言：C（按 C11 理解）；目标语言：C++（C++17）。
- 同一目标 OS，不做跨 OS 迁移；源无平台 #ifdef 分支。
- 任务模式：长单文件转换。把下面的 `fe.c` 翻译单元整体转换为一个 C++ 源文件 `target.cpp`。
- 伴随头文件 `fe.h` 已随源提供且在 C++ 下可直接编译，**保持 `#include "fe.h"` 不变，不要把 fe.h 的内容并入输出**。
- 保留 `#ifdef FE_STANDALONE` 块（含 `main`、`onerror`、`<setjmp.h>`）；编译时会定义 `FE_STANDALONE` 并链接为可执行程序，两侧命令：
  - 源侧基线：`gcc -std=c11 -DFE_STANDALONE fe.c -o program`
  - 目标侧：`g++ -std=c++17 -DFE_STANDALONE target.cpp -o program`
- 场景：无网络、无文件系统写入（仅按命令行参数只读打开脚本）、无进程/命令执行。
- 保留解释器语义：mark-sweep GC、tagged `union`、宏的求值次数、指针算术、聚合初始化、`longjmp`/`setjmp` 控制流。

## 可用转换知识（Skill 快照，按需应用；不要照抄进代码）

### 长单文件转换工作流
{sk_long}

### C → C++ 语言方向
{sk_dir}

### 头文件与宏可用性
{sk_hdr}

### 类型、接口与 C ABI
{sk_abi}

## 伴随头文件 fe.h（保持 #include，不并入输出，仅供理解类型）

{fe_h}

## 待转换的源翻译单元 fe.c

{fe_c}

## 输出

只输出 `target.cpp` 的完整纯文本内容（含被保留的 `#include "fe.h"` 与 `#ifdef FE_STANDALONE` 块）。不要任何围栏、说明或省略。
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
        "fe.c": sha256_text(fe_c),
        "fe.h": sha256_text(fe_h),
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
