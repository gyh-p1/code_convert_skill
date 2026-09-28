#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""realpath run-01 SELF_REVIEWED-stage orchestration (step-04 POSIX->Windows fs).
Feeds the frozen task contract + selected Skill snapshots + source realpath.c + the
GENERATED target.gen.cpp back to the configured .env model for ONE structured static
self-review (conversion-evaluation-loop.md §4). Saves a reproducible request (NO api
key), the raw response, the extracted structured JSON (self-review-1.json), and call
metadata. The model does the review; the Agent only orchestrates and records. No
fabricated verdict on empty/truncated/parse-fail.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime, re

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\realpath-fs-posix-to-win\output\no-rag\run-01")
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
MAX_TOKENS = int(os.environ.get("REALPATH_MAX_TOKENS", "120000"))
if not (KEY and MODEL and BASE):
    print("ENV_INCOMPLETE", file=sys.stderr); sys.exit(2)

rp_c = read(os.path.join(ROOT, r"docs\test\sources\freebsd-realpath\realpath.c"))
target = read(os.path.join(CONV, "target.gen.cpp"))
sk_dir = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))
sk_abi = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\type-abi.md"))
sk_fs = read(os.path.join(ROOT, r"skills\systems\posix-windows-filesystem\SKILL.md"))
system_msg = (
    "你是代码转换自审模型。给定 POSIX/BSD C 源翻译单元、由转换模型产出的 Windows C++ 目标文件、"
    "已冻结任务契约与已选转换知识，你要做一次结构化【静态】自审。"
    "你不是编译器：不得断言“语法必然通过”，只能指出可定位的疑点。这是【跨 OS 迁移 POSIX→Windows】，"
    "重点核对 POSIX/BSD 接口在 Windows/MinGW 下的成立性与语义保留。硬性要求：\n"
    "1. 完整性/覆盖：判断目标是否为完整单文件（无截断、无省略号、无 Markdown 围栏），"
    "关键声明、入口（`main`）、控制分支、全部函数（`usage` 及任何为迁移新增的 shim）与 flag 语义是否覆盖。\n"
    "2. 缺陷定位：找出可定位的类型/API/调用约定/平台条件/资源生命周期疑点；重点看 POSIX→Windows 迁移面"
    "（`realpath`↔`_fullpath`/`GetFullPathName` 的符号链接与存在性语义、`<err.h>`/`warn` 在 MinGW 缺失、"
    "`getopt`/`optind` 替换、`__dead2`→`[[noreturn]]`、`PATH_MAX`↔`_MAX_PATH`、`<io.h>`/`_access` 可用性）"
    "与 C++ 关键字/重载冲突（如自定义 `realpath` 与标准库符号）。"
    "每项标注来源 `transform-introduced`（转换引入）、`source-existing`（源已存在）或 `toolchain-unknown`（工具链未知），"
    "给出证据（行号或片段）、可机械应用的具体修改、风险。\n"
    "3. 只报告确有定位的缺陷；只有“可能问题”而无定位的，放入 risks 而不臆造缺陷。\n"
    "4. 关注头文件/宏依赖在目标 C++17/Windows MinGW 下是否成立，但不得据此断言编译必然通过。\n"
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

- 源语言：C（C11，POSIX/BSD）；目标语言：C++（C++17）。**做跨 OS 迁移 POSIX/Linux → Windows**，目标工具链 Windows x64 MinGW/UCRT64 `g++ -std=c++17`。
- 任务模式：短单文件转换。`realpath.c` 整体转换为单个 C++ 源文件 `target.cpp`。本源自包含、无伴随本地头。
- 两侧编译：
  - 源侧基线（POSIX/BSD，Linux glibc，命令行提供平台宏）：`cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__dead2= realpath.c -o program`
  - 目标侧（Windows）：`g++ -std=c++17 target.cpp -o program`（目标侧不假定源侧命令行宏，须在 C++ 内自足）
- 场景：只读路径规范化，无网络、无文件写入、无进程/命令执行。
- 须保留可观察行为：`-q` 抑制告警、解析成功打印规范化路径、失败 `warn` 且 `rval=1`、退出码 `rval`、`usage()` exit(1)、无参数规范化 `"."`。
- 只做让翻译单元在 C++17/Windows 下成立所必需的最小改动，语义等价，不“现代化”重写、不新增能力。

## 已选转换知识（Skill 快照，判读依据；不要求照抄进代码）

### C → C++ 语言方向
{sk_dir}

### 头文件与宏可用性
{sk_hdr}

### 类型、接口与 C ABI
{sk_abi}

### POSIX ↔ Windows 文件路径系统方向
{sk_fs}

## 源翻译单元 realpath.c（转换前）

{rp_c}

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
        "realpath.c": sha256_text(rp_c),
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
if transform_issues and verdict != "REPAIR-RECOMMENDED":
    print("WARN: transform-introduced issues present but verdict != REPAIR-RECOMMENDED", file=sys.stderr)
if not transform_issues and verdict == "REPAIR-RECOMMENDED":
    print("WARN: verdict REPAIR-RECOMMENDED but no transform-introduced issue listed", file=sys.stderr)
