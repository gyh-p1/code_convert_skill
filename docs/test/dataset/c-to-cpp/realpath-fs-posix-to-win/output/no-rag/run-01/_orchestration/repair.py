#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""realpath run-01 SELF_REPAIRED-stage orchestration (round 1; step-04 POSIX->Windows fs).
Feeds the frozen contract + skills + source realpath.c + the GENERATED target.gen.cpp +
the structured self-review (self-review-1.json, verdict REPAIR-RECOMMENDED) back to the
.env model and asks for ONE corrected, complete single-file C++ target that resolves the
mechanically-fixable transform-introduced defects (esp. the realpath name collision) and
preserves observable behaviour, keeping irreducible platform differences documented. The
model performs the repair; the Agent only orchestrates and records. Saves request (NO
key), raw response, extracted target.repair-1.cpp, and metadata.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\realpath-fs-posix-to-win\output\no-rag\run-01")
CONV = os.path.join(RUN, "02-conversion")
REV = os.path.join(RUN, "03-self-review")
N = 1

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
target = read(os.path.join(CONV, "target.gen.cpp"))
review = read(os.path.join(REV, "self-review-1.json"))
sk_fs = read(os.path.join(ROOT, r"skills\systems\posix-windows-filesystem\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))

system_msg = (
    "你是代码转换修复模型。给定 POSIX/BSD C 源、上一版 Windows C++ 目标文件、以及一次结构化自审"
    "（verdict=REPAIR-RECOMMENDED），你要产出【一份修正后的完整单文件 C++ 目标】。硬性要求：\n"
    "1. 修复自审中 origin=transform-introduced 且可机械修复的缺陷，最优先消除会导致目标侧编译失败的"
    "转换引入问题（例如自定义全局函数 realpath 与 mingw-w64 <stdlib.h> 可能声明的 realpath 冲突——"
    "按自审建议改名为 x_realpath 并同步调用点）。\n"
    "2. 在不新增能力（无网络/文件写/进程执行/权限）且保持最小改动的前提下，尽量恢复可观察行为等价"
    "（如选项解析的参数置换语义——mingw-w64 经 libmingwex/<getopt.h> 提供 getopt/optind，可直接使用以对齐源）。\n"
    "3. 目标工具链原生无等价、无法机械修复的平台差异（realpath 不解析符号链接/junction、路径分隔符、"
    "_MAX_PATH=260 长度上限），保持现状但在文件顶部注释中明确列为已知语义差异，不臆造等价实现。\n"
    "4. 保留其余全部语义与结构，不做无关的“现代化”重写。\n"
    "5. 输出必须是【单个完整的 C++ 源文件】的纯文本内容，即修正后 target.cpp 的全部内容："
    "不加任何 Markdown 代码围栏、不加解释文字、不加省略号、不截断。"
    "第一行即源代码第一行，最后一行即源代码最后一行。"
)

user_msg = f"""## 任务契约（已冻结，与生成/自审一致）

- 源语言：C（C11，POSIX/BSD）；目标语言：C++（C++17）。**跨 OS 迁移 POSIX/Linux → Windows**，目标工具链 Windows x64 MinGW/UCRT64 `g++ -std=c++17`。
- 短单文件转换，自包含无本地头。目标侧编译：`g++ -std=c++17 target.cpp -o program`。
- 须保留可观察行为：`-q` 抑制告警、解析成功打印规范化路径、失败 `warn` 且 `rval=1`、退出码 `rval`、`usage()` exit(1)、无参数规范化 `"."`。
- 只做让翻译单元在 C++17/Windows 下成立、并修复自审所列 transform-introduced 缺陷所必需的改动。

## 判读依据（Skill 快照）

### POSIX ↔ Windows 文件路径系统方向
{sk_fs}

### 头文件与宏可用性
{sk_hdr}

## 源翻译单元 realpath.c（转换前）

{rp_c}

## 上一版目标文件 target.gen.cpp（待修正）

{target}

## 结构化自审结论 self-review-1.json（verdict=REPAIR-RECOMMENDED）

{review}

## 输出

只输出修正后 `target.cpp` 的完整纯文本内容。不要任何围栏、说明或省略。
"""

messages = [
    {"role": "system", "content": system_msg},
    {"role": "user", "content": user_msg},
]
payload = {"model": MODEL, "temperature": TEMP, "max_tokens": MAX_TOKENS, "stream": False, "messages": messages}

req_snapshot = {
    "stage": "SELF_REPAIRED", "round": N,
    "endpoint": BASE + "/chat/completions", "model": MODEL, "temperature": TEMP, "max_tokens": MAX_TOKENS,
    "messages": messages,
    "input_sha256": {
        "realpath.c": sha256_text(rp_c),
        "target.gen.cpp": sha256_text(target),
        "self-review-1.json": sha256_text(review),
    },
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
req_path = os.path.join(CONV, f"target.repair-{N}.request.json")
with open(req_path, "w", encoding="utf-8") as f:
    json.dump(req_snapshot, f, ensure_ascii=False, indent=2)

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    BASE + "/chat/completions", data=data,
    headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=1200) as resp:
        raw = resp.read().decode("utf-8"); status = resp.status
except urllib.error.HTTPError as e:
    raw = e.read().decode("utf-8", "replace"); status = e.code
    with open(os.path.join(CONV, f"target.repair-{N}.attempt-1-failed.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps({"status": status, "body": raw}, ensure_ascii=False, indent=2))
    print(f"HTTP_ERROR {status}", file=sys.stderr); print(raw[:2000], file=sys.stderr); sys.exit(3)

with open(os.path.join(CONV, f"target.repair-{N}.response.raw.json"), "w", encoding="utf-8") as f:
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

cpp_path = os.path.join(CONV, f"target.repair-{N}.cpp")
with open(cpp_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

meta = {
    "stage": "SELF_REPAIRED", "round": N,
    "model": obj.get("model"), "requested_model": MODEL, "temperature": TEMP, "max_tokens": MAX_TOKENS,
    "finish_reason": finish, "usage": obj.get("usage"), "response_id": obj.get("id"), "http_status": status,
    "fence_stripped": fence_stripped,
    "reasoning_present": bool(choice["message"].get("reasoning_content")),
    "request_sha256": sha256_text(read(req_path)),
    "output_sha256": sha256_text(content),
    "output_lines": content.count("\n") + 1, "output_chars": len(content),
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
with open(os.path.join(CONV, f"target.repair-{N}.model.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print("OK status=%s finish=%s lines=%s chars=%s fence_stripped=%s" % (
    status, finish, meta["output_lines"], meta["output_chars"], fence_stripped))
print("usage=%s" % json.dumps(obj.get("usage")))
if finish == "length":
    print("WARN: finish_reason=length -> output may be truncated", file=sys.stderr)
if not content.strip():
    print("WARN: empty content", file=sys.stderr)
