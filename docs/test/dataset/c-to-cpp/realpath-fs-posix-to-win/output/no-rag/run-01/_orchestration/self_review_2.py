#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""realpath run-01 re-review after SELF_REPAIRED round 1 (self-review round 2).
Feeds the frozen contract + skills + source realpath.c + the REPAIRED target.repair-1.cpp
+ the prior self-review (self-review-1.json) back to the .env model for ONE structured
static self-review confirming whether the located transform-introduced defects were
resolved and whether the repair (esp. reintroducing getopt via <getopt.h>) introduced any
new transform-introduced defect. Same schema/guards as round 1. The model reviews; the
Agent only orchestrates and records. No fabricated verdict on empty/truncated/parse-fail.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime, re

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\realpath-fs-posix-to-win\output\no-rag\run-01")
CONV = os.path.join(RUN, "02-conversion")
OUT = os.path.join(RUN, "03-self-review")
N = 2  # re-review round after repair-1

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
target = read(os.path.join(CONV, "target.repair-1.cpp"))
prior = read(os.path.join(OUT, "self-review-1.json"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))
sk_fs = read(os.path.join(ROOT, r"skills\systems\posix-windows-filesystem\SKILL.md"))

system_msg = (
    "你是代码转换自审模型（修复后复审）。给定 POSIX/BSD C 源、上一轮自审（self-review-1，"
    "verdict=REPAIR-RECOMMENDED）、以及据其修复后的 Windows C++ 目标文件 target.repair-1.cpp，"
    "你要做一次结构化【静态】复审。你不是编译器：不得断言“语法必然通过”，只能指出可定位的疑点。\n"
    "重点：\n"
    "1. 逐条核对上一轮的 transform-introduced 缺陷是否已解决："
    "(a) 自定义全局 realpath 是否已改名（如 x_realpath）并同步调用点、不再与 SDK 声明冲突；"
    "(b) getopt 参数置换与未知选项诊断是否已恢复（如改用 <getopt.h>/libmingwex 的 getopt/optind）；"
    "(c) realpath→_fullpath+_access 的符号链接/分隔符/260 长度差异是否已明确记录为已知语义差异。\n"
    "2. 复审【修复动作本身是否引入新的 transform-introduced 缺陷】，尤其 <getopt.h> 依赖在 "
    "mingw-w64/UCRT64 `g++ -std=c++17` 下的可用性、optind 的声明与使用、getopt 返回值处理。\n"
    "3. 只报告确有定位的缺陷；仅“可能问题”而无定位的放入 risks，不臆造缺陷。\n"
    "4. 输出必须是【单个 JSON 对象】的纯文本，无 Markdown 围栏、无解释、无省略。schema：\n"
    "{\n"
    '  "target_complete": true|false,\n'
    '  "coverage": {"declarations": "...", "entry": "...", "branches": "...", "public_functions": "..."},\n'
    '  "prior_issues_resolution": [\n'
    '    {"prior_location": "...", "status": "resolved|partially-resolved|unresolved|accepted-known-difference", "evidence": "..."}\n'
    "  ],\n"
    '  "issues": [\n'
    '    {"location": "行号/片段", "origin": "transform-introduced|source-existing|toolchain-unknown",\n'
    '     "category": "type|api|calling-convention|platform-condition|resource-lifetime|other",\n'
    '     "evidence": "...", "suggested_fix": "可机械应用的修改，或\\"无需改动\\"", "risk": "..."}\n'
    "  ],\n"
    '  "risks": ["无法定位、需第三方编译确认的可能问题"],\n'
    '  "verdict": "REPAIR-RECOMMENDED|NO-REPAIR-IDENTIFIED",\n'
    '  "notes": "..."\n'
    "}\n"
    "5. verdict 与 issues 一致：仍存在未解决的 transform-introduced 缺陷即 REPAIR-RECOMMENDED；"
    "此类缺陷均已解决或已作为已知平台差异记录，才 NO-REPAIR-IDENTIFIED。空输出/截断/矛盾均视为无效。"
)

user_msg = f"""## 任务契约（已冻结，与生成/自审一致）

- 源语言：C（C11，POSIX/BSD）；目标语言：C++（C++17）。**跨 OS 迁移 POSIX/Linux → Windows**，目标工具链 Windows x64 MinGW/UCRT64 `g++ -std=c++17`。
- 短单文件转换，自包含无本地头。目标侧编译：`g++ -std=c++17 target.cpp -o program`。
- 须保留可观察行为：`-q` 抑制告警、解析成功打印规范化路径、失败 `warn` 且 `rval=1`、退出码 `rval`、`usage()` exit(1)、无参数规范化 `"."`。

## 判读依据（Skill 快照）

### 头文件与宏可用性
{sk_hdr}

### POSIX ↔ Windows 文件路径系统方向
{sk_fs}

## 源翻译单元 realpath.c（转换前）

{rp_c}

## 上一轮自审 self-review-1.json（verdict=REPAIR-RECOMMENDED）

{prior}

## 修复后待复审的目标文件 target.repair-1.cpp

{target}

## 输出

只输出符合上述 schema 的【单个 JSON 对象】纯文本，逐条给出上一轮缺陷的解决状态、任何新缺陷、与条目一致的 verdict。
"""

messages = [
    {"role": "system", "content": system_msg},
    {"role": "user", "content": user_msg},
]
payload = {"model": MODEL, "temperature": TEMP, "max_tokens": MAX_TOKENS, "stream": False, "messages": messages}

os.makedirs(OUT, exist_ok=True)
req_snapshot = {
    "stage": "SELF_REVIEWED", "round": N, "kind": "re-review-after-repair-1",
    "endpoint": BASE + "/chat/completions", "model": MODEL, "temperature": TEMP, "max_tokens": MAX_TOKENS,
    "messages": messages,
    "input_sha256": {
        "realpath.c": sha256_text(rp_c),
        "target.repair-1.cpp": sha256_text(target),
        "self-review-1.json": sha256_text(prior),
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
    with urllib.request.urlopen(req, timeout=1200) as resp:
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
    "stage": "SELF_REVIEWED", "round": N, "kind": "re-review-after-repair-1",
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
    print("usage=%s" % json.dumps(obj.get("usage"))); sys.exit(4)

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
