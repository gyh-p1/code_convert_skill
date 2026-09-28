#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""du run-01 GENERATED-stage orchestration (step-04 POSIX->Windows filesystem, batch 4/4).
Reads root .env for the configured translator model, builds a cross-OS C->C++
conversion request (source snapshot du.c + selected Skill snapshots + frozen task
contract), calls the OpenAI-compatible /chat/completions endpoint, and saves the raw
response, extracted target.gen.cpp, a reproducible request.json (NO api key), and model
metadata. The Agent only orchestrates; the C++ is produced by the model.
du is the pre-recorded EXPECTED-HARD datapoint: fts/libutil/SIGINFO/UF_NODUMP/st_blocks are
absent on both glibc and MinGW; the target is a near-full reimplementation. Whatever the
model produces is recorded honestly; no fabrication of a clean pass.
MAX_TOKENS defaults high (120000): deepseek-flash is a reasoning model whose reasoning_tokens
eat a low cap, yielding empty content + finish=length. Override via DU_MAX_TOKENS.
"""
import json, os, sys, hashlib, urllib.request, urllib.error, datetime

ROOT = r"E:\桌面文档\Agents System\code_convert"
RUN = os.path.join(ROOT, r"docs\test\cases\du-fs-posix-to-win\output\no-rag\run-01")
OUT = os.path.join(RUN, "02-conversion")

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
sk_dir = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\SKILL.md"))
sk_hdr = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\header-macro.md"))
sk_abi = read(os.path.join(ROOT, r"skills\directions\c-to-cpp\references\type-abi.md"))
sk_fs = read(os.path.join(ROOT, r"skills\systems\posix-windows-filesystem\SKILL.md"))
system_msg = (
    "你是代码转换执行模型，负责把给定的 POSIX/BSD C 源翻译单元（FreeBSD du(1)）转换为在 Windows 下"
    "成立的等价 C++。这是批次中最复杂的一例，源大量依赖 FreeBSD-base 表面，多数在 Windows/MinGW 缺失，"
    "需要一次接近完整的重写。硬性要求：\n"
    "1. 尽力保持可观察行为——du(1) 语义：递归遍历实参目录（默认物理 FTS_PHYSICAL），累加块用量并打印；"
    "选项 -A(以字节而非块)、-B blocksize、-H/-L/-P(符号链接跟随策略)、-a(所有文件)、-s(仅汇总)、-d depth(深度)、"
    "-c(末尾 total)、-g/-h/-k/-m(单位)、-l(不去重硬链接)、-n(忽略 nodump)、-r(兼容 no-op)、-I mask(fnmatch 忽略)、"
    "-t threshold(阈值)、-x(不跨设备)、--si；无实参默认当前目录 \".\"；usage() 打印 "
    "\"usage: du [-Aclnx] [-H | -L | -P] [-g | -h | -k | -m] [-a | -s | -d depth] [-B blocksize] [-I mask] [-t threshold] [file ...]\" "
    "到 stderr 并 exit(EX_USAGE=64)。\n"
    "2. 这是【跨 OS 迁移 POSIX→Windows】，源用的以下 BSD 接口在 Windows/MinGW 缺失，须映射或自备等价：\n"
    "   - fts(3)（fts_open/fts_read/fts_set，FTS_PHYSICAL/LOGICAL/COMFOLLOW/XDEV/SKIP，FTS_D/DP/DC/DNR/ERR/NS 等）"
    "无 Windows 等价：用 FindFirstFile/FindNextFile 或 <filesystem> 递归遍历自行实现同序（后序 DP 时对目录累加子项）、"
    "维护 fts_level/fts_path/fts_parent 汇总与 fts_bignum 等价的每目录累加；\n"
    "   - <libutil.h> humanize_number/expand_number/getbsize：BSD-only，两平台皆无，须自备等价实现（人类可读单位、阈值/块大小解析）；\n"
    "   - signal(SIGINFO,…) 与 volatile sig_atomic_t info 交互式进度：SIGINFO 是 BSD 专有信号，Windows 无 POSIX 信号语义，"
    "须删除或保守化（Windows 上无该信号，安全地不注册；保持其余行为不变），并在文件顶部注释登记为已知差异；\n"
    "   - st_flags & UF_NODUMP（-n）：Windows struct stat 无 st_flags，-n 无等价语义，保守置为 no-op 并注释登记为已知差异；\n"
    "   - st_blocks 块计量：Windows struct stat 无 st_blocks，用 st_size 近似（或 Win32 分配大小），属可观察数值差异，注释登记；\n"
    "   - (st_dev,st_ino) 硬链接去重：Windows stat() 的 st_ino 恒为 0、st_dev 仅卷号，(dev,ino) 去重在 Windows 不可靠，"
    "可保守处理（如不去重或用 GetFileInformationByHandle 的卷序列号+文件索引），保持默认行为正确并注释登记该已知差异；\n"
    "   - getopt_long/optind/optarg（<getopt.h>）：MinGW-w64 经 libmingwex 提供，可直接用；若替换为自定义解析须把状态定义在 main 之前；\n"
    "   - fnmatch（<fnmatch.h>）、err/warn/warnx/errx（<err.h>）、SLIST_*（<sys/queue.h>）、DEV_BSIZE/howmany、EX_USAGE(<sysexits.h>)："
    "MinGW 大多缺失，须自备等价（fnmatch 可用 PathMatchSpec 或自实现；err 家族用 fprintf+strerror(errno)+exit；SLIST 用 std 容器）。\n"
    "3. 只做让该程序在目标 C++17/Windows(MinGW/UCRT64) 工具链下成立所必需的改动，保持语义尽量等价；"
    "平台缺失能力按保守、可观察行为尽量一致的方式处理，不新增进程/网络/文件写删/权限能力，不臆造不成立的等价。\n"
    "4. 不确定或源语义未定义处保守处理并在注释说明，不伪装成完全等价。\n"
    "5. 本源自包含、无伴随本地头，输出无需任何本地 #include。\n"
    "6. 输出必须是【单个完整的 C++ 源文件】的纯文本内容，即 target.cpp 的全部内容："
    "不加任何 Markdown 代码围栏、不加解释文字、不加省略号、不截断。"
    "第一行即源代码第一行，最后一行即源代码最后一行。"
)

user_msg = f"""## 任务契约（已冻结）

- 源语言：C（按 C11 理解，POSIX/BSD）；目标语言：C++（C++17）。
- **做跨 OS 迁移：POSIX/Linux → Windows**。目标侧工具链为 Windows x64 MinGW/UCRT64 `g++ -std=c++17`。
- 任务模式：单文件转换（本源 561 行，批次中最复杂）。把下面的 `du.c` 翻译单元整体转换为一个 C++ 源文件 `target.cpp`。
- 本源自包含，无伴随本地头。
- 两侧编译命令：
  - 源侧基线（POSIX/BSD，Linux glibc；命令行提供 `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__unused=`）：`cc -std=c11 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D__unused= du.c -o program`（预期在 SIGINFO/UF_NODUMP/libutil 上失败，属源可移植性事实，不影响你的目标侧任务）
  - 目标侧（Windows）：`g++ -std=c++17 target.cpp -o program`（目标侧不假定源侧命令行宏，需在 C++ 内自足所有符号）
- 场景：只读——递归遍历目录、累加块用量并打印。无网络、无文件写/删、无进程/命令执行。
- 须尽力保留 du(1) 可观察行为（选项集与语义见 system 指令）。fts/libutil/SIGINFO/UF_NODUMP/st_blocks 等 BSD 表面按 system 指令映射/自备/保守化，并在文件顶部注释登记已知差异。

## 可用转换知识（Skill 快照，按需应用；不要照抄进代码）

### C → C++ 语言方向
{sk_dir}

### 头文件与宏可用性
{sk_hdr}

### 类型、接口与 C ABI
{sk_abi}

### POSIX ↔ Windows 文件路径系统方向
{sk_fs}

## 待转换的源翻译单元 du.c

{du_c}

## 输出

只输出 `target.cpp` 的完整纯文本内容。不要任何围栏、说明或省略。
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
    "endpoint": BASE + "/chat/completions",
    "model": MODEL,
    "temperature": TEMP,
    "max_tokens": MAX_TOKENS,
    "messages": messages,
    "input_sha256": {"du.c": sha256_text(du_c)},
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
req_path = os.path.join(OUT, "target.gen.request.json")
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
    with open(os.path.join(OUT, "target.gen.attempt-1-failed.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps({"status": status, "body": raw}, ensure_ascii=False, indent=2))
    print(f"HTTP_ERROR {status}", file=sys.stderr)
    print(raw[:2000], file=sys.stderr)
    sys.exit(3)

with open(os.path.join(OUT, "target.gen.response.raw.json"), "w", encoding="utf-8") as f:
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

cpp_path = os.path.join(OUT, "target.gen.cpp")
with open(cpp_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

meta = {
    "stage": "GENERATED",
    "model": obj.get("model"),
    "requested_model": MODEL,
    "temperature": TEMP,
    "max_tokens": MAX_TOKENS,
    "finish_reason": finish,
    "usage": obj.get("usage"),
    "response_id": obj.get("id"),
    "http_status": status,
    "fence_stripped": fence_stripped,
    "reasoning_present": bool(choice["message"].get("reasoning_content")),
    "request_sha256": sha256_text(read(req_path)),
    "output_sha256": sha256_text(content),
    "output_lines": content.count("\n") + 1,
    "output_chars": len(content),
    "captured_at": datetime.datetime.now().astimezone().isoformat(),
}
with open(os.path.join(OUT, "target.gen.model.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print("OK status=%s finish=%s lines=%s chars=%s fence_stripped=%s" % (
    status, finish, meta["output_lines"], meta["output_chars"], fence_stripped))
print("usage=%s" % json.dumps(obj.get("usage")))
if finish == "length":
    print("WARN: finish_reason=length -> output may be truncated", file=sys.stderr)
if not content.strip():
    print("WARN: empty content", file=sys.stderr)
