#!/usr/bin/env python3
"""One configured-model static self-review; never compiles or executes artifacts."""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUN = HERE.parent
ROOT = next(
    parent for parent in HERE.parents
    if (parent / "SKILL.md").is_file() and (parent / "docs" / "test").is_dir()
)
OUT = RUN / "03-self-review"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


env = load_env(ROOT / ".env")
key = env.get("OPENAI_API_KEY", "")
model = env.get("CODE_TRANSLATOR_MODEL", "")
base = env.get("CODE_TRANSLATOR_BASE_URL", "").rstrip("/")
temperature = float(env.get("CODE_TRANSLATOR_TEMPERATURE", "0.2"))
max_tokens = int(os.environ.get("CHAIN_MAX_TOKENS", "120000"))
if not (key and model and base):
    print("ENV_INCOMPLETE", file=sys.stderr)
    sys.exit(2)

source = read("docs/test/sources/chain-reactor-network/networking_quarks.c")
target = read(
    "docs/test/dataset/c-to-cpp/chain-reactor-network-linux/"
    "output/no-rag/run-01/02-conversion/target.gen.cpp"
)
atoms_h = read("docs/test/sources/chain-reactor-network/atoms.h")
util_h = read("docs/test/sources/chain-reactor-network/util.h")
driver = read("docs/test/dataset/c-to-cpp/chain-reactor-network-linux/driver.c")
contract = read(
    "docs/test/dataset/c-to-cpp/chain-reactor-network-linux/"
    "output/no-rag/run-01/01-frozen/frozen-inputs.md"
)
skills = {
    "C→C++ 语言方向": read("skills/directions/c-to-cpp/SKILL.md"),
    "网络 I/O 场景": read("skills/scenes/network-io/SKILL.md"),
    "长单文件工作流": read("skills/workflows/long-file-conversion/SKILL.md"),
    "头文件与宏": read("skills/directions/c-to-cpp/references/header-macro.md"),
    "类型与 C ABI": read("skills/directions/c-to-cpp/references/type-abi.md"),
}

system_message = (
    "你是配置模型的代码转换静态自审者，不是编译器。给定 C 原件、生成的 C++ 和冻结契约，"
    "逐项核对完整性、全部公开函数与未调用分支、类型/头文件/宏、GNU C++17 平台语法、"
    "C driver 的 quark_connect 链接 ABI、原样 C util.c 的 urand 链接、网络/进程/文件副作用、"
    "资源与错误路径。区分 transform-introduced、source-existing、toolchain-unknown。"
    "只把可定位的转换引入缺陷放 issues；无法确认的放 risks。不得以自审声称编译或功能通过。"
    "只输出单个 JSON 对象，不加围栏或说明。schema："
    '{"target_complete":true,"coverage":{"functions":"...","branches":"...","abi":"..."},'
    '"issues":[{"location":"...","origin":"transform-introduced|source-existing|toolchain-unknown",'
    '"category":"type|api|calling-convention|platform-condition|resource-lifetime|behavior|other",'
    '"evidence":"...","suggested_fix":"...","risk":"..."}],'
    '"risks":["..."],"verdict":"REPAIR-RECOMMENDED|NO-REPAIR-IDENTIFIED","notes":"..."}'
    "。有未解决的 transform-introduced 问题则 verdict=REPAIR-RECOMMENDED，否则 NO-REPAIR-IDENTIFIED。"
)
skill_text = "\n\n".join(f"### {name}\n{content}" for name, content in skills.items())
user_message = f"""## 冻结任务契约
{contract}

## 已选 Skill 快照
{skill_text}

## 伴随头 atoms.h
{atoms_h}

## 伴随头 util.h
{util_h}

## 同一 C driver.c（只限 loopback）
{driver}

## 原始 C 完整翻译单元
{source}

## 配置模型首次输出 C++ 完整翻译单元
{target}

请仅输出上述 schema 的 JSON。若只是工具链未知，不把它伪造为确定转换缺陷。
"""

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message},
]
payload = {
    "model": model,
    "temperature": temperature,
    "max_tokens": max_tokens,
    "stream": False,
    "messages": messages,
}

OUT.mkdir(parents=True, exist_ok=True)
endpoint = base + "/chat/completions"
request_snapshot = {
    "stage": "SELF_REVIEWED",
    "round": 1,
    "endpoint": endpoint,
    "model": model,
    "temperature": temperature,
    "max_tokens": max_tokens,
    "messages": messages,
    "input_sha256": {
        "networking_quarks.c": sha256_text(source),
        "target.gen.cpp": sha256_text(target),
        "atoms.h": sha256_text(atoms_h),
        "util.h": sha256_text(util_h),
        "driver.c": sha256_text(driver),
    },
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
request_path = OUT / "self-review-1.request.json"
request_path.write_text(json.dumps(request_snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
request = urllib.request.Request(
    endpoint,
    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(request, timeout=1200) as response:
        raw = response.read().decode("utf-8")
        status = response.status
except urllib.error.HTTPError as error:
    raw = error.read().decode("utf-8", "replace")
    (OUT / "self-review-1.attempt-1-failed.json").write_text(
        json.dumps({"status": error.code, "body": raw}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"HTTP_ERROR {error.code}", file=sys.stderr)
    sys.exit(3)

(OUT / "self-review-1.response.raw.json").write_text(raw, encoding="utf-8")
result = json.loads(raw)
choice = result["choices"][0]
content = choice["message"].get("content") or ""
finish_reason = choice.get("finish_reason")
value = content.strip()
fence_stripped = False
if value.startswith("```"):
    fence_stripped = True
    lines = value.split("\n")
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    value = "\n".join(lines)
try:
    review = json.loads(value)
except json.JSONDecodeError as error:
    (OUT / "self-review-1.parse-error.json").write_text(
        json.dumps({"error": str(error), "content": content}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("INVALID_REVIEW_JSON", file=sys.stderr)
    sys.exit(4)
if finish_reason != "stop" or review.get("verdict") not in {
    "REPAIR-RECOMMENDED", "NO-REPAIR-IDENTIFIED"
} or not isinstance(review.get("issues"), list):
    print("INVALID_REVIEW_VERDICT_OR_FINISH", file=sys.stderr)
    sys.exit(5)
if review["verdict"] == "NO-REPAIR-IDENTIFIED" and any(
    issue.get("origin") == "transform-introduced" for issue in review["issues"]
):
    print("CONTRADICTORY_REVIEW", file=sys.stderr)
    sys.exit(6)
(OUT / "self-review-1.json").write_text(
    json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8"
)
metadata = {
    "stage": "SELF_REVIEWED",
    "round": 1,
    "model": result.get("model"),
    "requested_model": model,
    "temperature": temperature,
    "max_tokens": max_tokens,
    "finish_reason": finish_reason,
    "usage": result.get("usage"),
    "response_id": result.get("id"),
    "http_status": status,
    "fence_stripped": fence_stripped,
    "reasoning_present": bool(choice["message"].get("reasoning_content")),
    "request_sha256": sha256_text(request_path.read_text(encoding="utf-8")),
    "target_sha256": sha256_text(target),
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
(OUT / "self-review-1.model.json").write_text(
    json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"OK status={status} finish={finish_reason} verdict={review['verdict']} issues={len(review['issues'])}")
print("usage=" + json.dumps(result.get("usage")))
