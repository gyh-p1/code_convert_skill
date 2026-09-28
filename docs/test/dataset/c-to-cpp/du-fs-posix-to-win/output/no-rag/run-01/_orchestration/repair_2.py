#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""du run-01 SELF_REPAIRED round 2 (final; step-04 POSIX->Windows fs, batch 4/4).
Feeds the frozen contract + skills + source du.c + the round-1 repaired target.repair-1.cpp +
the round-2 self-review (self-review-2.json: off_t blocker + 10/12 resolved, 2 documented
known-diffs, 3 residual transform-introduced behaviour nits) back to the .env model for ONE
final corrected complete single-file C++ target that resolves the 3 residual mechanically-fixable
issues (fnmatch ']'-as-first-char range, directory_iterator follow_directory_symlink under -L/-H,
'--si' unique-prefix abbreviation) without regressing the round-1 fixes and while keeping
irreducible platform differences documented. Repair budget (<=2) is exhausted after this round.
The model performs the repair; the Agent only orchestrates and records.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\du-fs-posix-to-win\output\no-rag\run-01")
CONV = os.path.join(RUN, "02-conversion")
REV = os.path.join(RUN, "03-self-review")
N = 2

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
MAX_TOKENS = int(os.environ.get("DU_MAX_TOKENS", "120000"))
if not (KEY and MODEL and BASE):
    print("ENV_INCOMPLETE", file=sys.stderr); sys.exit(2)

du_c = read(os.path.join(ROOT, r"docs\test\sources\freebsd-du\du.c"))
target = read(os.path.join(CONV, "target.repair-1.cpp"))
review2 = read(os.path.join(REV, "self-review-2.json"))
sk_fs = read(os.path.join(ROOT, r"skills\systems\posix-windows-filesystem\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))

system_msg = (
    "你是代码转换修复模型（第 2 轮，最终修复）。给定 POSIX/BSD C 源（FreeBSD du(1)）、上一轮已修复的 Windows C++ "
    "目标 target.repair-1.cpp、以及第 2 轮结构化复审（self-review-2.json：编译阻断的 off_t 冲突及 10/12 项已解决，2 项"
    "降级为已登记平台差异，仍有 3 项可定位的 transform-introduced 行为缺陷），你要产出【一份最终修正后的完整单文件 C++ 目标】。硬性要求：\n"
    "1. 精确修复 self-review-2.json issues[] 中列出的 3 项 transform-introduced 缺陷，均为可机械修复，不得回退上一轮已解决项：\n"
    "   - `fnmatch_impl` 字符类：首字符 `]` 不应作为范围起始（如 `[]-a]` 应把 `]` 当字面量）。"
    "在范围分支前判断是否为字符类首字符（`p == pat+1`，或 negate 时 `p == pat+2`），首字符按字面量处理，不进入 `p[1]=='-'` 范围分支；\n"
    "   - `process_path` 目录遍历：当 `follow`（`-L`，或 `-H` 且命令行实参）为真时，`directory_iterator` 应传入 "
    "`std::filesystem::directory_options::follow_directory_symlink`，否则用 `directory_options::none`，以贴合源 FTS_LOGICAL/FTS_COMFOLLOW 跟随目录符号链接遍历；\n"
    "   - `main` 长选项：源用 `getopt_long`，接受唯一前缀缩写（如 `--s` 匹配 `--si`）。改为接受 `--si` 的唯一非空前缀"
    "（如 `strncmp(arg+2, \"si\", strlen(arg+2))==0 && strlen(arg+2)>0`），仍对未知长选项调用 `usage()`。\n"
    "2. 保留上一轮全部已解决项（du_off_t 别名、buf[32]、expand_number 溢出检查、err errno 保存+progname、-B/-d 用 atoi、"
    "setlocale、getbsize/BLOCKSIZE、fnmatch 反斜杠结尾与 `[]]` 首字符、directory_iterator 显式递增异常处理），不得引入新的编译阻断或语义回退，全文件保持无裸 `off_t`。\n"
    "3. self-review-2.json 中 status=deferred-known-diff 的 2 项（目录自身大小、非目录符号链接 lstat）以及 risks 中"
    "目标工具链原生无等价的平台差异（st_blocks/UF_NODUMP/硬链接去重/SIGINFO/-x 盘符/目录循环/枚举顺序/humanize 舍入/路径编码），"
    "保持保守处理并维持文件顶部注释登记，不臆造等价、不新增能力。\n"
    "4. 目标编译命令固定为 `g++ -std=c++17 target.cpp -o program`，不因 `-lstdc++fs` 顾虑而改命令或引入本机假设；如有顾虑仅在注释记录。\n"
    "5. 不做无关“现代化”重写，不新增网络/文件写删/进程执行/权限能力。\n"
    "6. 输出必须是【单个完整的 C++ 源文件】的纯文本内容，即最终 target.cpp 的全部内容："
    "不加任何 Markdown 代码围栏、不加解释文字、不加省略号、不截断。第一行即源代码第一行，最后一行即源代码最后一行。"
)

user_msg = f"""## 任务契约（已冻结，与生成/自审/修复一致）

- 源语言：C（C11，POSIX/BSD）；目标语言：C++（C++17）。**跨 OS 迁移 POSIX/Linux → Windows**，目标工具链 Windows x64 MinGW/UCRT64 `g++ -std=c++17`。
- 单文件转换（本源 561 行），自包含无本地头。目标侧编译：`g++ -std=c++17 target.cpp -o program`。
- 本轮为最终修复（修复预算 ≤2 已在本轮用尽）：只精确修复第 2 轮复审列出的 3 项 transform-introduced 缺陷，不回退既有修复，保持已登记平台差异。

## 判读依据（Skill 快照）

### POSIX ↔ Windows 文件路径系统方向
{sk_fs}

### 头文件与宏可用性
{sk_hdr}

## 源翻译单元 du.c（转换前）

{du_c}

## 上一轮修复后目标 target.repair-1.cpp（待最终修正）

{target}

## 第 2 轮结构化复审 self-review-2.json（verdict=REPAIR-RECOMMENDED，3 项 transform-introduced 待修）

{review2}

## 输出

只输出最终修正后 `target.cpp` 的完整纯文本内容。不要任何围栏、说明或省略。
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
        "du.c": sha256_text(du_c),
        "target.repair-1.cpp": sha256_text(target),
        "self-review-2.json": sha256_text(review2),
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
    with urllib.request.urlopen(req, timeout=1800) as resp:
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
