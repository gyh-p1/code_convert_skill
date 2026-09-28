#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pwd run-01 SELF_REPAIRED-stage orchestration (round 1; step-04 POSIX->Windows fs, batch 3/4).
Feeds the frozen contract + skills + source pwd.c + the GENERATED target.gen.cpp + the
structured self-review (self-review-1.json, verdict REPAIR-RECOMMENDED) back to the .env model
and asks for ONE corrected, complete single-file C++ target that resolves the mechanically-
fixable transform-introduced defects (esp. the compile-blocking declaration-order issue:
pwd_optind/pwd_optpos used in main before their definition) and preserves observable behaviour,
keeping irreducible platform differences (st_ino==0 identity limitation) documented. The model
performs the repair; the Agent only orchestrates and records. Saves request (NO key), raw
response, extracted target.repair-1.cpp, and metadata.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\pwd-fs-posix-to-win\output\no-rag\run-01")
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
MAX_TOKENS = int(os.environ.get("PWD_MAX_TOKENS", "120000"))
if not (KEY and MODEL and BASE):
    print("ENV_INCOMPLETE", file=sys.stderr); sys.exit(2)

pwd_c = read(os.path.join(ROOT, r"docs\test\sources\freebsd-pwd\pwd.c"))
target = read(os.path.join(CONV, "target.gen.cpp"))
review = read(os.path.join(REV, "self-review-1.json"))
sk_fs = read(os.path.join(ROOT, r"skills\systems\posix-windows-filesystem\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))

system_msg = (
    "你是代码转换修复模型。给定 POSIX/BSD C 源、上一版 Windows C++ 目标文件、以及一次结构化自审"
    "（verdict=REPAIR-RECOMMENDED），你要产出【一份修正后的完整单文件 C++ 目标】。硬性要求：\n"
    "1. 修复自审中 origin=transform-introduced 且可机械修复的缺陷，最优先消除会导致目标侧编译失败的"
    "转换引入问题——本例的阻断点是【声明顺序】：main 在 `argc -= pwd_optind; argv += pwd_optind;` 处"
    "引用了 `pwd_optind`，而 `static int pwd_optind = 1;`（及 `static int pwd_optpos = 1;`）却定义在文件后部；"
    "C++ 无隐式声明，必须把这两个静态计数器上移到 main 之前的前向声明区（例如紧随 progname 定义或紧随 "
    "pwd_getopt 前向声明之后），保持单次初始化。\n"
    "2. 在不新增能力（无网络/文件写/进程执行/权限）且保持最小改动的前提下，尽量恢复可观察行为等价。"
    "对第二项自审条目（getcwd_logical 中 `lg.st_ino != 0 &&` 守卫）：Windows 上 stat() 的 st_ino 恒为 0、"
    "st_dev 仅为卷号，源式 (st_dev,st_ino) 身份比较会对同卷任意 $PWD 误判为一致。请保留该保守守卫"
    "（使 -L 在 Windows 安全回落物理 getcwd，不打印未经校验的 $PWD），并在文件顶部注释中明确登记为"
    "相对源语义的已知平台偏差；不要臆造 GetFileInformationByHandle 等未验证等价实现。\n"
    "3. 目标工具链原生无等价、无法机械修复的平台差异（st_ino 语义、getopt 无 argv 重排、getopt 未知选项"
    "诊断文本），保持现状但在文件顶部注释中明确列为已知差异，不臆造等价实现。\n"
    "4. 保留其余全部语义与结构，不做无关的“现代化”重写。\n"
    "5. 输出必须是【单个完整的 C++ 源文件】的纯文本内容，即修正后 target.cpp 的全部内容："
    "不加任何 Markdown 代码围栏、不加解释文字、不加省略号、不截断。"
    "第一行即源代码第一行，最后一行即源代码最后一行。"
)

user_msg = f"""## 任务契约（已冻结，与生成/自审一致）

- 源语言：C（C11，POSIX/BSD）；目标语言：C++（C++17）。**跨 OS 迁移 POSIX/Linux → Windows**，目标工具链 Windows x64 MinGW/UCRT64 `g++ -std=c++17`。
- 短单文件转换，自包含无本地头。目标侧编译：`g++ -std=c++17 target.cpp -o program`。
- 须保留可观察行为：`-L` 逻辑/`-P` 物理（默认物理）、逻辑校验成功打印 `$PWD` 否则退回物理 `getcwd`、成功 `printf("%s\\n", p)`、失败 `err(1, ".")`、`exit(0)`、多余操作数或未知选项 `usage()` 输出 `usage: pwd [-L | -P]` 到 stderr 并 `exit(1)`。
- 只做让翻译单元在 C++17/Windows 下成立、并修复自审所列 transform-introduced 缺陷所必需的改动。

## 判读依据（Skill 快照）

### POSIX ↔ Windows 文件路径系统方向
{sk_fs}

### 头文件与宏可用性
{sk_hdr}

## 源翻译单元 pwd.c（转换前）

{pwd_c}

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
        "pwd.c": sha256_text(pwd_c),
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
