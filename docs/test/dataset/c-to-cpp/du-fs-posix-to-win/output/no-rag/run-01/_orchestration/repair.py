#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""du run-01 SELF_REPAIRED-stage orchestration (round 1; step-04 POSIX->Windows fs, batch 4/4).
Feeds the frozen contract + skills + source du.c + the GENERATED target.gen.cpp + the
structured self-review (self-review-1.json, verdict REPAIR-RECOMMENDED, 12 transform-introduced
issues) back to the .env model and asks for ONE corrected, complete single-file C++ target that
resolves the mechanically-fixable transform-introduced defects (top priority: the compile-blocking
`typedef long long off_t;` clash with MinGW's system off_t; plus buf sizing, expand_number
overflow, fnmatch edge cases, err errno-save+progname, strtol strictness vs atoi, setlocale,
getbsize/BLOCKSIZE, directory_iterator exception handling) and preserves observable behaviour,
keeping irreducible platform differences (st_blocks/UF_NODUMP/hardlink-dedup/SIGINFO) documented.
The model performs the repair; the Agent only orchestrates and records.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\du-fs-posix-to-win\output\no-rag\run-01")
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
MAX_TOKENS = int(os.environ.get("DU_MAX_TOKENS", "120000"))
if not (KEY and MODEL and BASE):
    print("ENV_INCOMPLETE", file=sys.stderr); sys.exit(2)

du_c = read(os.path.join(ROOT, r"docs\test\sources\freebsd-du\du.c"))
target = read(os.path.join(CONV, "target.gen.cpp"))
review = read(os.path.join(REV, "self-review-1.json"))
sk_fs = read(os.path.join(ROOT, r"skills\systems\posix-windows-filesystem\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))

system_msg = (
    "你是代码转换修复模型。给定 POSIX/BSD C 源（FreeBSD du(1)）、上一版 Windows C++ 目标文件、以及一次结构化自审"
    "（verdict=REPAIR-RECOMMENDED，12 项 transform-introduced），你要产出【一份修正后的完整单文件 C++ 目标】。硬性要求：\n"
    "1. 最优先消除会导致目标侧编译失败的转换引入问题——本例的阻断点是【类型重定义冲突】："
    "`typedef long long off_t;` 会与 MinGW/UCRT64 系统头（经 `<filesystem>`/`<sys/stat.h>` 间接引入）已有的 `off_t` 冲突。"
    "请删除该 typedef，改用不冲突的别名（如 `using du_off_t = long long;`，宽度保持 64 位），"
    "并把 `expand_number` 参数、`threshold`、`threshold_sign` 等一并改用该别名，全文件一致、无残留 `off_t`。\n"
    "2. 修复自审中 origin=transform-introduced 且可机械修复、能提升可观察行为等价的缺陷（在不新增能力、保持最小改动前提下）：\n"
    "   - `prthumanval` 的 `char buf[5]` 扩大到足够（如 `char buf[32]`）避免 snprintf 截断；\n"
    "   - `expand_number` 后缀乘法前做溢出检查（`value > LLONG_MAX/factor` 时返回 -1）；\n"
    "   - `err` 开头保存 `int e = errno;` 再用，并加程序名前缀（从 argv[0] 取 basename 存全局 progname）；\n"
    "   - `-B`/`-d` 用 `atoi` 语义（源用 atoi，不因尾随字符拒绝）以贴合源可观察行为，或保留 strtol 但不因 `*endptr!=0` 拒绝；\n"
    "   - `main` 开头加 `#include <clocale>` 与 `setlocale(LC_ALL, \"\");`；\n"
    "   - 实现 `getbsize` 等价：读 `BLOCKSIZE` 环境变量解析，失败回退 512；\n"
    "   - `fnmatch_impl` 字符类反斜杠结尾越界、`[]]` 字面量首字符等边界修正（或换用更稳妥的等价实现）；\n"
    "   - `directory_iterator` 递增可能抛异常：改用带 `error_code` 的显式递增或 try/catch 映射为 warnx + rval=1 并继续，避免未捕获异常终止。\n"
    "3. 目标工具链原生无等价、无法机械修复的平台差异，保持保守处理并在文件顶部注释中明确列为已知差异，不臆造等价实现：\n"
    "   - `st_blocks` 缺失（用 st_size/文件大小近似）、`UF_NODUMP`/`-n` 无等价（no-op）、硬链接 `(st_dev,st_ino)` 去重在 Windows 不可靠"
    "（st_ino 恒 0）、`SIGINFO` 进度报告 Windows 无信号语义（不注册）、目录自身大小与符号链接 lstat 语义在 `<filesystem>` 下的偏差。"
    "对目录/符号链接大小，尽量用 symlink_status 区分并注释，不把不成立的等价说成等价。\n"
    "4. 不要因为担心 `<filesystem>` 链接（`-lstdc++fs`）而改变目标编译命令或引入本机假设；目标命令固定为 `g++ -std=c++17 target.cpp -o program`，"
    "现代 MinGW/UCRT64 GCC 已将 filesystem 并入 libstdc++。若确有顾虑，仅在注释中记录为 toolchain 风险，不改命令。\n"
    "5. 保留其余全部语义与结构，不做无关的“现代化”重写，不新增网络/文件写删/进程执行/权限能力。\n"
    "6. 输出必须是【单个完整的 C++ 源文件】的纯文本内容，即修正后 target.cpp 的全部内容："
    "不加任何 Markdown 代码围栏、不加解释文字、不加省略号、不截断。"
    "第一行即源代码第一行，最后一行即源代码最后一行。"
)

user_msg = f"""## 任务契约（已冻结，与生成/自审一致）

- 源语言：C（C11，POSIX/BSD）；目标语言：C++（C++17）。**跨 OS 迁移 POSIX/Linux → Windows**，目标工具链 Windows x64 MinGW/UCRT64 `g++ -std=c++17`。
- 单文件转换（本源 561 行），自包含无本地头。目标侧编译：`g++ -std=c++17 target.cpp -o program`。
- 目标是对 fts/libutil/SIGINFO/UF_NODUMP/st_blocks 等 BSD 表面的重写：先保证目标能在 Windows C++17 编译成立（消除 off_t 重定义等阻断点），再尽量恢复 du(1) 可观察行为等价，无法等价的平台差异登记在文件顶部注释。
- 只做让翻译单元在 C++17/Windows 下成立、并修复自审所列 transform-introduced 缺陷所必需的改动。

## 判读依据（Skill 快照）

### POSIX ↔ Windows 文件路径系统方向
{sk_fs}

### 头文件与宏可用性
{sk_hdr}

## 源翻译单元 du.c（转换前）

{du_c}

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
        "du.c": sha256_text(du_c),
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
