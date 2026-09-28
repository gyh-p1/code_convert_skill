#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""realpath run-01 GENERATED-stage orchestration (step-04 POSIX->Windows filesystem).
Reads root .env for the configured translator model, builds a cross-OS C->C++
conversion request (source snapshot realpath.c + selected Skill snapshots + frozen
task contract), calls the OpenAI-compatible /chat/completions endpoint, and saves
the raw response, extracted target.gen.cpp, a reproducible request.json (NO api key),
and model metadata. The Agent only orchestrates; the C++ is produced by the model.
MAX_TOKENS defaults high (120000) per the stest lesson: deepseek-flash is a reasoning
model whose reasoning_tokens eat a low cap, yielding empty content + finish=length.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\realpath-fs-posix-to-win\output\no-rag\run-01")
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
MAX_TOKENS = int(os.environ.get("REALPATH_MAX_TOKENS", "120000"))
if not (KEY and MODEL and BASE):
    print("ENV_INCOMPLETE", file=sys.stderr); sys.exit(2)

rp_c = read(os.path.join(ROOT, r"docs\test\sources\freebsd-realpath\realpath.c"))
sk_dir = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))
sk_abi = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\type-abi.md"))
sk_fs = read(os.path.join(ROOT, r"skills\systems\posix-windows-filesystem\SKILL.md"))
system_msg = (
    "你是代码转换执行模型，负责把给定的 POSIX/BSD C 源翻译单元转换为在 Windows 下"
    "成立的等价 C++。硬性要求：\n"
    "1. 严格保持可观察行为——命令行 flag 语义（-q 抑制每路径告警）、每个路径参数解析成功即"
    "打印其规范化绝对路径（printf \"%s\\n\"）、解析失败时非 -q 则告警且 rval=1、"
    "退出码为 rval、usage() 打印用法到 stderr 并 exit(1)、无路径参数时规范化当前目录 \".\"。\n"
    "2. 这是【跨 OS 迁移 POSIX→Windows】：源用 realpath(3)/getopt/warn(<err.h>)/PATH_MAX/__dead2 "
    "等 POSIX/BSD 接口，其中 realpath 在 Windows 无同名等价（对应 _fullpath 或 GetFullPathName，"
    "但符号链接解析与不存在路径的存在性语义不同）、<err.h>/warn 在 MinGW-w64 缺失需自备等价、"
    "__dead2 是 FreeBSD <sys/cdefs.h> 惯用法两平台均无、PATH_MAX 在 Windows 无同名常量。"
    "只做在目标 C++17/Windows 工具链下让该翻译单元成立所必需的最小改动，保持语义等价；"
    "平台缺失能力按保守、可观察行为一致的方式处理，不新增进程/网络/文件写/权限能力。\n"
    "3. 不确定或源语义未定义处保留原样并保守处理，不臆造等价实现。\n"
    "4. 本源自包含、无伴随本地头，输出无需任何本地 #include。\n"
    "5. 输出必须是【单个完整的 C++ 源文件】的纯文本内容，即 target.cpp 的全部内容："
    "不加任何 Markdown 代码围栏、不加解释文字、不加省略号、不截断。"
    "第一行即源代码第一行，最后一行即源代码最后一行。"
)

user_msg = f"""## 任务契约（已冻结）

- 源语言：C（按 C11 理解，POSIX/BSD）；目标语言：C++（C++17）。
- **做跨 OS 迁移：POSIX/Linux → Windows**。目标侧工具链为 Windows x64 MinGW/UCRT64 `g++ -std=c++17`。
- 任务模式：短单文件转换。把下面的 `realpath.c` 翻译单元整体转换为一个 C++ 源文件 `target.cpp`。
- 本源自包含，无伴随本地头。
- 两侧编译命令：
  - 源侧基线（POSIX/BSD，Linux glibc；命令行提供 `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__dead2=`）：`cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__dead2= realpath.c -o program`
  - 目标侧（Windows）：`g++ -std=c++17 target.cpp -o program`（目标侧不假定源侧的命令行宏，需在 C++ 内自行满足所有符号）
- 场景：只读路径规范化，无网络、无文件写入、无进程/命令执行。
- 须保留 realpath(1) 语义：`getopt(argc,argv,"q")` 解析 `-q`、`optind` 后取路径列表、无参数时用 `"."`、
  对每个 path 调用 realpath 等价物成功则 `printf("%s\\n", resolved)`、失败则（非 -q 时）`warn("%s", path)` 且 `rval=1`、
  最终 `exit(rval)`、`usage()` 输出 `usage: realpath [-q] [path ...]` 到 stderr 并 `exit(1)`。

## 可用转换知识（Skill 快照，按需应用；不要照抄进代码）

### C → C++ 语言方向
{sk_dir}

### 头文件与宏可用性
{sk_hdr}

### 类型、接口与 C ABI
{sk_abi}

### POSIX ↔ Windows 文件路径系统方向
{sk_fs}

## 待转换的源翻译单元 realpath.c

{rp_c}

## 输出

只输出 `target.cpp` 的完整纯文本内容。不要任何围栏、说明或省略。
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
    "input_sha256": {"realpath.c": sha256_text(rp_c)},
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
