#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fe run-01 SELF_REVIEWED-stage orchestration.
Feeds the frozen task contract + selected Skill snapshots + source fe.c + the
GENERATED target.gen.cpp back to the configured .env model for ONE structured
static self-review (conversion-evaluation-loop.md §4). Saves a reproducible
request (NO api key), the raw response, the extracted structured JSON
(self-review-1.json), and call metadata. The model does the review; the Agent
only orchestrates and records. No fabricated verdict on empty/truncated/parse-fail.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime, re

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\fe-lisp-c-to-cpp\output\no-rag\run-01")
CONV = os.path.join(RUN, "02-conversion")
OUT = os.path.join(RUN, "03-self-review")
N = 1  # first self-review round

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
target = read(os.path.join(CONV, "target.gen.cpp"))
sk_long = read(os.path.join(ROOT, r"skills\workflows\long-file-conversion\SKILL.md"))
sk_dir = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))
sk_abi = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\type-abi.md"))

system_msg = (
    "你是代码转换自审模型。给定 C 源翻译单元、由转换模型产出的 C++ 目标文件、"
    "已冻结任务契约与已选转换知识，你要做一次结构化【静态】自审。"
    "你不是编译器：不得断言“语法必然通过”，只能指出可定位的疑点。硬性要求：\n"
    "1. 完整性/覆盖：判断目标是否为完整单文件（无截断、无省略号、无 Markdown 围栏），"
    "关键声明、入口（`FE_STANDALONE` 下的 `main`/`onerror`）、控制分支、全部公开函数是否覆盖。\n"
    "2. 缺陷定位：找出可定位的类型/API/调用约定/平台条件/资源生命周期疑点；每一项标注来源为"
    "`transform-introduced`（转换引入）、`source-existing`（源已存在）或 `toolchain-unknown`（工具链未知），"
    "给出证据（行号或代码片段）、可机械应用的具体修改、风险。\n"
    "3. 只报告确有定位的缺陷；只有“可能问题”而无定位的，放入 risks 而不臆造缺陷。\n"
    "4. 关注头文件/宏依赖（含 `min`/`max` 之类）与实际分支在目标 C++17 下是否成立，"
    "但不得据此断言编译必然通过。\n"
    "5. 输出必须是【单个 JSON 对象】的纯文本，无 Markdown 围栏、无解释文字、无省略。schema：\n"
    "{\n"
    '  "target_complete": true|false,\n'
    '  "coverage": {"declarations": "...", "entry": "...", "branches": "...", "public_functions": "..."},\n'
    '  "issues": [\n'
    '    {"location": "行号/片段", "origin": "transform-introduced|source-existing|toolchain-unknown",\n'
    '     "category": "type|api|calling-convention|platform-condition|resource-lifetime|other",\n'
    '     "evidence": "...", "suggested_fix": "可机械应用的修改，或\\"无需改动\\"", "risk": "..."}\n'
    "  ],\n"
    '  "risks": ["无法定位、需第三方编译确认的可能问题"],\n'
    '  "verdict": "REPAIR-RECOMMENDED|NO-REPAIR-IDENTIFIED",\n'
    '  "notes": "..."\n'
    "}\n"
    "6. verdict 必须与 issues 一致：存在未解决的 `transform-introduced` 缺陷即 `REPAIR-RECOMMENDED`；"
    "无此类缺陷才 `NO-REPAIR-IDENTIFIED`。结论与条目矛盾、空输出、截断均视为无效。"
)

user_msg = f"""## 任务契约（已冻结，与生成时一致）

- 源语言：C（C11）；目标语言：C++（C++17）。同一目标 OS，不跨 OS 迁移；源无平台 `#ifdef` 分支。
- 任务模式：长单文件转换。`fe.c` 整体转换为单个 C++ 源文件 `target.cpp`。
- 伴随头文件 `fe.h` 在 C++ 下可直接编译，**保持 `#include "fe.h"` 不变，不并入输出**。
- 保留 `#ifdef FE_STANDALONE` 块（含 `main`、`onerror`、`<setjmp.h>`）；编译两侧：
  - 源侧基线：`gcc -std=c11 -DFE_STANDALONE fe.c -o program`
  - 目标侧：`g++ -std=c++17 -DFE_STANDALONE target.cpp -o program`
- 场景：无网络、无文件系统写入、无进程/命令执行。
- 须保留解释器语义：mark-sweep GC、tagged `union`、宏的求值次数、指针算术、聚合初始化、`longjmp`/`setjmp` 控制流。
- 只做让翻译单元在 C++17 下成立所必需的最小改动，不“现代化”重写。

## 已选转换知识（Skill 快照，判读依据；不要求照抄进代码）

### 长单文件转换工作流
{sk_long}

### C → C++ 语言方向
{sk_dir}

### 头文件与宏可用性
{sk_hdr}

### 类型、接口与 C ABI
{sk_abi}

## 伴随头文件 fe.h（保持 #include，不并入输出）

{fe_h}

## 源翻译单元 fe.c（转换前）

{fe_c}

## 待自审的目标文件 target.gen.cpp（转换后）

{target}

## 输出

只输出符合上述 schema 的【单个 JSON 对象】纯文本。逐项给出位置、来源、证据、可机械应用的修改与风险，并给出与条目一致的 verdict。
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
    "stage": "SELF_REVIEWED",
    "round": N,
    "endpoint": BASE + "/chat/completions",
    "model": MODEL,
    "temperature": TEMP,
    "max_tokens": MAX_TOKENS,
    "messages": messages,
    "input_sha256": {
        "fe.c": sha256_text(fe_c),
        "fe.h": sha256_text(fe_h),
        "target.gen.cpp": sha256_text(target),
    },
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
req_path = os.path.join(OUT, f"self-review-{N}.request.json")
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
    with open(os.path.join(OUT, f"self-review-{N}.attempt-1-failed.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps({"status": status, "body": raw}, ensure_ascii=False, indent=2))
    print(f"HTTP_ERROR {status}", file=sys.stderr)
    print(raw[:2000], file=sys.stderr)
    sys.exit(3)

with open(os.path.join(OUT, f"self-review-{N}.response.raw.json"), "w", encoding="utf-8") as f:
    f.write(raw)

obj = json.loads(raw)
choice = obj["choices"][0]
content = choice["message"].get("content") or ""
finish = choice.get("finish_reason")

# extract the single JSON object (deterministic; failures are recorded, not faked)
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
    "stage": "SELF_REVIEWED",
    "round": N,
    "model": obj.get("model"),
    "requested_model": MODEL,
    "temperature": TEMP,
    "max_tokens": MAX_TOKENS,
    "finish_reason": finish,
    "usage": obj.get("usage"),
    "response_id": obj.get("id"),
    "http_status": status,
    "reasoning_present": bool(choice["message"].get("reasoning_content")),
    "request_sha256": sha256_text(read(req_path)),
    "content_sha256": sha256_text(content),
    "content_chars": len(content),
    "parsed_ok": parsed is not None,
    "parse_error": parse_error,
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
# consistency guard between verdict and issues (reported, not silently trusted)
if transform_issues and verdict != "REPAIR-RECOMMENDED":
    print("WARN: transform-introduced issues present but verdict != REPAIR-RECOMMENDED", file=sys.stderr)
if not transform_issues and verdict == "REPAIR-RECOMMENDED":
    print("WARN: verdict REPAIR-RECOMMENDED but no transform-introduced issue listed", file=sys.stderr)

