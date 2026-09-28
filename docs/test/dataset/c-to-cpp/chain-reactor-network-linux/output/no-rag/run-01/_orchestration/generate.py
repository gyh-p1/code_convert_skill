#!/usr/bin/env python3
"""Run-specific text conversion request. Never compiles or executes source/target."""

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
OUT = RUN / "02-conversion"


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
atoms_h = read("docs/test/sources/chain-reactor-network/atoms.h")
util_h = read("docs/test/sources/chain-reactor-network/util.h")
util_c = read("docs/test/sources/chain-reactor-network/util.c")
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
    "你是本工作区配置的代码转换模型。把给定的完整 C 翻译单元转换为 Linux GNU C++17 的"
    "单个完整 target.cpp。只做保持源行为和构建 C++ 所需的修改；不现代化重写，不修源已有缺陷，"
    "不新增网络、进程、文件、权限或隐蔽能力。保留所有连接、监听、socketcall、错误与清理路径，"
    "不得因为本 case 只观察 quark_connect 就删去其它函数。共享 atoms.h、util.h、util.c、"
    "driver.c 不属于输出，不得改写；target.cpp 必须与同一 C driver.c 中的 quark_connect 调用"
    "保持 C 链接 ABI，并与原样 C util.c 的 urand 正确链接。源里的随机读取未完整检查、"
    "单次 send 可能短写、socket 创建失败时可能返回 0，这些是源行为，不要擅自修正。"
    "只输出纯 C++ 源代码，不加 Markdown 围栏、解释、省略号或额外文件。"
)
skill_text = "\n\n".join(f"### {name}\n{content}" for name, content in skills.items())
user_message = f"""## 冻结的任务契约
{contract}

## 适用转换知识（按事实使用，不复制进输出）
{skill_text}

## 共享 C 头 atoms.h（保持原件）
{atoms_h}

## 共享 C 头 util.h（保持原件）
{util_h}

## 原样 C 伴随实现 util.c（仅供理解 ABI/urand；不转换）
{util_c}

## case 私有入口 driver.c（保持原件；须与目标 C++ 正确链接）
{driver}

## 待转换完整 C 翻译单元 networking_quarks.c
{source}

## 输出
只输出单个完整 target.cpp 的纯文本，保留源文件全部函数和平台条件分支。
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
    "endpoint": endpoint,
    "model": model,
    "temperature": temperature,
    "max_tokens": max_tokens,
    "messages": messages,
    "input_sha256": {
        "networking_quarks.c": sha256_text(source),
        "atoms.h": sha256_text(atoms_h),
        "util.h": sha256_text(util_h),
        "util.c": sha256_text(util_c),
        "driver.c": sha256_text(driver),
        "frozen-inputs.md": sha256_text(contract),
    },
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
request_path = OUT / "target.gen.request.json"
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
    (OUT / "target.gen.attempt-1-failed.json").write_text(
        json.dumps({"status": error.code, "body": raw}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"HTTP_ERROR {error.code}", file=sys.stderr)
    sys.exit(3)

(OUT / "target.gen.response.raw.json").write_text(raw, encoding="utf-8")
result = json.loads(raw)
choice = result["choices"][0]
content = choice["message"].get("content") or ""
finish_reason = choice.get("finish_reason")
fence_stripped = False
if content.strip().startswith("```"):
    fence_stripped = True
    lines = content.strip("\n").split("\n")
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    content = "\n".join(lines)
(OUT / "target.gen.cpp").write_text(content, encoding="utf-8", newline="\n")

metadata = {
    "stage": "GENERATED",
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
    "output_sha256": sha256_text(content),
    "output_lines": content.count("\n") + 1,
    "output_chars": len(content),
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
(OUT / "target.gen.model.json").write_text(
    json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(
    "OK status=%s finish=%s lines=%s chars=%s fence_stripped=%s"
    % (status, finish_reason, metadata["output_lines"], metadata["output_chars"], fence_stripped)
)
print("usage=" + json.dumps(result.get("usage")))
if finish_reason == "length" or not content.strip():
    print("WARN: output may be incomplete", file=sys.stderr)
