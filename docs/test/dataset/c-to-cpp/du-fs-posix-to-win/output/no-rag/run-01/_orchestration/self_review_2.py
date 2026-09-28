#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""du run-01 SELF_REVIEWED round 2 (post-repair verification; step-04 POSIX->Windows fs, batch 4/4).
Feeds the frozen contract + skills + source du.c + the REPAIRED target.repair-1.cpp + the
round-1 self-review (self-review-1.json, 12 transform-introduced issues) back to the .env model
for ONE structured static re-review: confirm which round-1 issues are now resolved, flag any
new transform-introduced defects, and give a verdict consistent with the remaining issues.
The model does the review; the Agent only orchestrates and records. No fabricated verdict on
empty/truncated/parse-fail.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime, re

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\du-fs-posix-to-win\output\no-rag\run-01")
CONV = os.path.join(RUN, "02-conversion")
OUT = os.path.join(RUN, "03-self-review")
N = 2  # second self-review round (post round-1 repair)

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
review1 = read(os.path.join(OUT, "self-review-1.json"))
sk_dir = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))
sk_abi = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\type-abi.md"))
sk_fs = read(os.path.join(ROOT, r"skills\systems\posix-windows-filesystem\SKILL.md"))

system_msg = (
    "你是代码转换自审模型（第 2 轮，修复后复审）。给定 POSIX/BSD C 源（FreeBSD du(1)）、经一次自修复的 Windows C++ "
    "目标文件 target.repair-1.cpp、上一轮自审结论（self-review-1.json，12 项 transform-introduced），"
    "以及已冻结契约与已选知识，做一次结构化【静态】复审。你不是编译器：不得断言“语法必然通过”，只能指出可定位疑点。"
    "这是【跨 OS 迁移 POSIX→Windows】，目标是对 fts/libutil/SIGINFO/UF_NODUMP/st_blocks 等 BSD 表面的近乎完整重写。硬性要求：\n"
    "1. 逐条核对上一轮 12 项 transform-introduced 是否已在本版解决："
    "重点确认阻断编译的 `typedef long long off_t;` 是否已改为不冲突别名（如 `using du_off_t = long long;`）且全文件无残留 `off_t`；"
    "以及 buf 尺寸、expand_number 溢出检查、err errno 保存+progname、`-B`/`-d` 贴合源 atoi 语义、setlocale、getbsize/BLOCKSIZE、"
    "fnmatch 边界（反斜杠结尾/`[]]`）、directory_iterator 显式递增异常处理是否落实。\n"
    "2. 找出【本次修复可能新引入】的 transform-introduced 缺陷（可定位的类型/API/顺序/资源生命周期/可观察行为偏离），"
    "给出证据（行号或片段）、可机械应用的修改、风险。\n"
    "3. 目标工具链原生无等价、无法机械修复的平台差异（st_blocks/UF_NODUMP/硬链接去重/SIGINFO/目录自身大小/符号链接 lstat），"
    "若已在文件顶部注释登记为已知差异且处理保守，则不计为需修复缺陷，可放入 risks。\n"
    "4. 只报告确有定位的缺陷；仅“可能问题”而无定位的放入 risks，不臆造。\n"
    "5. 输出必须是【单个 JSON 对象】的纯文本，无 Markdown 围栏、无解释文字、无省略。schema：\n"
    "{\n"
    '  "target_complete": true|false,\n'
    '  "coverage": {"declarations": "...", "entry": "...", "branches": "...", "public_functions": "..."},\n'
    '  "prior_issues_resolution": [\n'
    '    {"round1_issue": "简述上一轮条目", "status": "resolved|partially-resolved|unresolved|deferred-known-diff",\n'
    '     "evidence": "本版对应行号/片段"}\n'
    "  ],\n"
    '  "issues": [\n'
    '    {"location": "行号/片段", "origin": "transform-introduced|source-existing|toolchain-unknown",\n'
    '     "category": "type|api|calling-convention|platform-condition|resource-lifetime|declaration-order|behavior|other",\n'
    '     "evidence": "...", "suggested_fix": "可机械应用的修改，或\\"无需改动\\"", "risk": "..."}\n'
    "  ],\n"
    '  "risks": ["无法定位、需第三方编译确认的可能问题"],\n'
    '  "verdict": "REPAIR-RECOMMENDED|NO-REPAIR-IDENTIFIED",\n'
    '  "notes": "..."\n'
    "}\n"
    "6. verdict 必须与 issues 一致：仍存在未解决的 `transform-introduced` 缺陷即 `REPAIR-RECOMMENDED`；"
    "若上一轮 transform-introduced 均已解决或降级为已登记平台差异、且未新引入此类缺陷，则 `NO-REPAIR-IDENTIFIED`。"
    "结论与条目矛盾、空输出、截断均视为无效。"
)

user_msg = f"""## 任务契约（已冻结，与生成/自审/修复一致）

- 源语言：C（C11，POSIX/BSD）；目标语言：C++（C++17）。**跨 OS 迁移 POSIX/Linux → Windows**，目标工具链 Windows x64 MinGW/UCRT64 `g++ -std=c++17`。
- 单文件转换（本源 561 行），自包含无本地头。目标侧编译：`g++ -std=c++17 target.cpp -o program`（不假定源侧命令行宏）。
- 目标是对 fts/libutil/SIGINFO/UF_NODUMP/st_blocks 等 BSD 表面的重写：核对重写在 Windows C++17 下能否成立、可观察行为是否尽量保留、已知差异是否在注释中登记；不臆造不成立的等价，不新增能力。
- 本轮为修复后复审：确认上一轮 12 项 transform-introduced 的处置，并检查是否新引入缺陷。

## 已选转换知识（Skill 快照，判读依据）

### C → C++ 语言方向
{sk_dir}

### 头文件与宏可用性
{sk_hdr}

### 类型、接口与 C ABI
{sk_abi}

### POSIX ↔ Windows 文件路径系统方向
{sk_fs}

## 源翻译单元 du.c（转换前）

{du_c}

## 上一轮自审结论 self-review-1.json（12 项 transform-introduced）

{review1}

## 待复审的修复后目标文件 target.repair-1.cpp

{target}

## 输出

只输出符合上述 schema 的【单个 JSON 对象】纯文本。逐条给出 prior_issues_resolution，再列出本版仍存/新引入的 issues 与一致的 verdict。
"""

messages = [
    {"role": "system", "content": system_msg},
    {"role": "user", "content": user_msg},
]
payload = {"model": MODEL, "temperature": TEMP, "max_tokens": MAX_TOKENS, "stream": False, "messages": messages}

os.makedirs(OUT, exist_ok=True)
req_snapshot = {
    "stage": "SELF_REVIEWED", "round": N,
    "endpoint": BASE + "/chat/completions", "model": MODEL, "temperature": TEMP, "max_tokens": MAX_TOKENS,
    "messages": messages,
    "input_sha256": {
        "du.c": sha256_text(du_c),
        "target.repair-1.cpp": sha256_text(target),
        "self-review-1.json": sha256_text(review1),
    },
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
req_path = os.path.join(OUT, f"self-review-{N}.request.json")
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
    with open(os.path.join(OUT, f"self-review-{N}.attempt-1-failed.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps({"status": status, "body": raw}, ensure_ascii=False, indent=2))
    print(f"HTTP_ERROR {status}", file=sys.stderr); print(raw[:2000], file=sys.stderr); sys.exit(3)

with open(os.path.join(OUT, f"self-review-{N}.response.raw.json"), "w", encoding="utf-8") as f:
    f.write(raw)

obj = json.loads(raw)
choice = obj["choices"][0]
content = choice["message"].get("content") or ""
finish = choice.get("finish_reason")

parsed = None
parse_error = None
c = content.strip()
if c.startswith("```"):
    lines = c.split("\n")
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    c = "\n".join(lines).strip()
m = re.search(r"\{.*\}", c, re.DOTALL)
if m:
    try:
        parsed = json.loads(m.group(0))
    except Exception as e:
        parse_error = str(e)
else:
    parse_error = "no JSON object found in content"

meta = {
    "stage": "SELF_REVIEWED", "round": N,
    "model": obj.get("model"), "requested_model": MODEL, "temperature": TEMP, "max_tokens": MAX_TOKENS,
    "finish_reason": finish, "usage": obj.get("usage"), "response_id": obj.get("id"), "http_status": status,
    "reasoning_present": bool(choice["message"].get("reasoning_content")),
    "request_sha256": sha256_text(read(req_path)),
    "content_sha256": sha256_text(content), "content_chars": len(content),
    "parsed_ok": parsed is not None, "parse_error": parse_error,
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
with open(os.path.join(OUT, f"self-review-{N}.model.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

invalid = (finish == "length") or (not content.strip()) or (parsed is None)
if invalid:
    reason = ("finish_reason=length" if finish == "length"
              else "empty content" if not content.strip()
              else "parse_failed: " + str(parse_error))
    with open(os.path.join(OUT, f"self-review-{N}.attempt-1-failed.json"), "w", encoding="utf-8") as f:
        json.dump({"reason": reason, "finish_reason": finish, "content": content}, f, ensure_ascii=False, indent=2)
    print("INVALID status=%s finish=%s reason=%s" % (status, finish, reason), file=sys.stderr)
    print("usage=%s" % json.dumps(obj.get("usage")))
    sys.exit(4)

with open(os.path.join(OUT, f"self-review-{N}.json"), "w", encoding="utf-8") as f:
    json.dump(parsed, f, ensure_ascii=False, indent=2)

verdict = parsed.get("verdict")
issues = parsed.get("issues") or []
transform_issues = [i for i in issues if i.get("origin") == "transform-introduced"]
print("OK status=%s finish=%s verdict=%s issues=%s transform_introduced=%s complete=%s" % (
    status, finish, verdict, len(issues), len(transform_issues), parsed.get("target_complete")))
print("usage=%s" % json.dumps(obj.get("usage")))
if transform_issues and verdict != "REPAIR-RECOMMENDED":
    print("WARN: transform-introduced issues present but verdict != REPAIR-RECOMMENDED", file=sys.stderr)
if not transform_issues and verdict == "REPAIR-RECOMMENDED":
    print("WARN: verdict REPAIR-RECOMMENDED but no transform-introduced issue listed", file=sys.stderr)
