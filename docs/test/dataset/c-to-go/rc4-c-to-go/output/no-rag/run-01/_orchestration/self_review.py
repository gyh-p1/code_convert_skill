#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rc4 run-01 SELF_REVIEWED-stage orchestration (LANGUAGE dimension, C->Go, same-OS).
Feeds the frozen task contract + the 3 frozen C files + inline C->Go guidance + the GENERATED
target.gen.go back to the configured .env model for ONE structured static self-review
(conversion-evaluation-loop.md §4). Saves a reproducible request (NO api key), the raw response,
the extracted structured JSON (self-review-1.json), and call metadata. The model does the review;
the Agent only orchestrates and records. No c-to-go Skill is injected (it does not exist yet).
No fabricated verdict on empty/truncated/parse-fail.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime, re

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\rc4-c-to-go\output\no-rag\run-01")
CONV = os.path.join(RUN, "02-conversion")
OUT = os.path.join(RUN, "03-self-review")
SRC = os.path.join(ROOT, r"docs\test\sources\wjcryptlib-rc4")
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
MAX_TOKENS = int(os.environ.get("RC4_MAX_TOKENS", "120000"))
if not (KEY and MODEL and BASE):
    print("ENV_INCOMPLETE", file=sys.stderr); sys.exit(2)

rc4_h = read(os.path.join(SRC, "WjCryptLib_Rc4.h"))
rc4_c = read(os.path.join(SRC, "WjCryptLib_Rc4.c"))
cli_c = read(os.path.join(SRC, "rc4_decrypt_cli.c"))
target = read(os.path.join(CONV, "target.gen.go"))
system_msg = (
    "你是代码转换自审模型。给定 3 份可移植 C 源（上游 RC4 模块 .h/.c + 薄 CLI 驱动 .c）、由转换模型产出的"
    "单文件 Go 目标（package main），以及已冻结任务契约与内联 C→Go 指引，你要做一次结构化【静态】自审。"
    "你不是编译器：不得断言“必然 go build 通过”，只能指出可定位的疑点。这是【同 OS 语言方向 C→Go】，"
    "重点核对 Go 成立性（尤其能直接 `go build` 失败的问题）与 RC4/CLI 语义保留。硬性要求：\n"
    "1. 完整性/覆盖：判断目标是否为完整单文件（无截断、无省略号、无 Markdown 围栏、首行 `package main`），"
    "RC4 模块面（Rc4Context 结构、Rc4Initialise/Rc4Output/Rc4Xor/Rc4XorWithKey 等价）、hex 解码、入口 `main`、"
    "以及退出码分支（用法/hex 错误=2、RC4 初始化失败=1、成功=0）是否覆盖。\n"
    "2. 缺陷定位：找出可定位的、会导致 `go build` 失败或语义偏离的疑点，尤其：\n"
    "   - **未使用的 import 或未使用的局部变量**（Go 编译错误）；反之用到却未 import 的包；\n"
    "   - **缺失/错误的整型显式转换**：`byte`/`uint32`/`int` 间运算须显式转换，Go 无隐式转换；mod-256 语义是否保持；\n"
    "   - **`void*`→`[]byte` 映射**是否正确（含 in/out 同址情形）、定长数组 `[256]byte` 与切片索引是否越界；\n"
    "   - **错误返回码→`error` / 退出码→`os.Exit`**：0/-1 是否正确映射为 error，2/1/0 退出码语义是否与源一致；\n"
    "   - **RC4 语义偏离**：KSA（S[i]=byte(i)；j=(j+S[i]+key[i%keySize])%256 交换）、PRGA、DropN 是否与上游逐字一致；\n"
    "   - **hex 解析语义**：奇数长度/非法字符/超容量 → 是否仍映射为退出码 2；空密文是否仍允许（源 clen==0 不报错）；\n"
    "   - 包/标识符大小写、未定义符号、`encoding/hex` 用法错误等。\n"
    "每项标注来源 `transform-introduced`（转换引入）、`source-existing`（源已存在）或 `toolchain-unknown`（工具链未知），"
    "给出证据（行号或片段）、可机械应用的具体修改、风险。\n"
    "3. 只报告确有定位的缺陷；只有“可能问题”而无定位的，放入 risks 而不臆造缺陷。\n"
    "4. 关注 Go 语言层面的成立性，但不得据此断言编译必然通过。\n"
    "5. 输出必须是【单个 JSON 对象】的纯文本，无 Markdown 围栏、无解释文字、无省略。schema：\n"
    "{\n"
    '  "target_complete": true|false,\n'
    '  "coverage": {"declarations": "...", "entry": "...", "branches": "...", "public_functions": "..."},\n'
    '  "issues": [\n'
    '    {"location": "行号/片段", "origin": "transform-introduced|source-existing|toolchain-unknown",\n'
    '     "category": "type|api|unused-import|unused-variable|conversion|error-handling|exit-code|behavior|package|other",\n'
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

- 源语言：C（C11，纯可移植，无平台 #ifdef）；目标语言：**Go**（当前稳定 go 工具链，`package main`）。**同 OS 语言方向**（均在 Windows 构建）。
- 任务模式：多文件→单文件。3 份 C 文件整体转换为一个 Go 源 `target.go`。
- 两侧编译：
  - 源侧基线（C11）：`gcc -std=c11 WjCryptLib_Rc4.c rc4_decrypt_cli.c -o program`
  - 目标侧（Go, Windows）：`go build -o program.exe`（单 package main，含 target.go）
- 场景：只读——按 hex key 对 hex 密文做 RC4 解密并把明文写 stdout。无网络、无文件写/删、无进程/命令执行。
- 须保留可观察行为：用法 `program <hex-key> <hex-ciphertext>`、错误退出码（用法/hex=2、RC4 初始化失败=1）、成功把明文原始字节写 stdout=0、RC4 KSA/PRGA/DropN 语义与上游一致。

## C → Go 指引（判读依据；本项目 c-to-go Skill 尚不存在，故仅内联）

头/预处理→包与导出、`#define` 宏→函数/元组交换、指针/字节缓冲/`void*`→`[]byte`、定宽无符号与 mod-256→`byte`/`uint32` 显式转换、
错误返回码→`error`+`os.Exit` 退出码、`argv`/hex→`os.Args`+`encoding/hex`、**未使用 import/变量即编译错误**。

## 源（转换前，3 份 C 文件）

### WjCryptLib_Rc4.h（上游逐字）
{rc4_h}

### WjCryptLib_Rc4.c（上游逐字）
{rc4_c}

### rc4_decrypt_cli.c（本项目自写驱动）
{cli_c}

## 待自审的目标文件 target.gen.go（转换后）

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
        "WjCryptLib_Rc4.h": sha256_text(rc4_h),
        "WjCryptLib_Rc4.c": sha256_text(rc4_c),
        "rc4_decrypt_cli.c": sha256_text(cli_c),
        "target.gen.go": sha256_text(target),
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
    with urllib.request.urlopen(req, timeout=1800) as resp:
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

