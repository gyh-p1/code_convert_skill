"""Document loading evidence; never imports, builds, or executes a sample."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version as package_version
import json
import ntpath
import os
from pathlib import Path
import sys
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit

VERSION = "1.0.1"
SCHEMA = "loading-preflight/v1"
MARKER = "LOADING_READ_V1\n"
CORE = {
    "task-state": "references/framework/task-state-contract.md",
    "classifier": "references/workflow/classifier-agent-gate.md",
    "build": "references/workflow/build-prerequisites.md",
    "loop": "references/workflow/conversion-evaluation-loop.md",
    "evaluation": "references/framework/evaluation-readiness-contract.md",
    "delivery": "references/framework/delivery-handoff-contract.md",
    "safety": "references/framework/safety-boundary.md",
}
WORKFLOWS = {name: f"skills/workflows/{name}-conversion/SKILL.md"
             for name in ("batch", "long-file")}
ENTRIES = (".agents/skills/code-convert/SKILL.md", "AGENTS.md", "SKILL.md")
ACTIONS = ("start", "map", "freeze", "classify", "source-precheck", "generate",
           "review", "submit", "resume", "close", "query", "collect", "terminate", "cleanup")
RECOVERY = ("query", "collect", "terminate", "cleanup")
# Classification serves evaluator admission; conversion-only actions use six common contracts.
CLASSIFIER_ACTIONS = ("classify", "source-precheck", "submit")


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def load_json(path):
    return json.loads(guard_path(path).read_text(encoding="utf-8-sig"))


def guard_path(path):
    path = Path(path)
    forbidden = "d:\\codeconvertremote\\stack"
    for candidate in (str(path), str(path.absolute())):
        normalized = ntpath.normcase(ntpath.normpath(candidate))
        require(normalized != forbidden and not normalized.startswith(forbidden + "\\"),
                "Controller installation/jobs paths are outside this tool's boundary")
    resolved = path.resolve()
    normalized = ntpath.normcase(ntpath.normpath(str(resolved)))
    require(normalized != forbidden and not normalized.startswith(forbidden + "\\"),
            "resolved Controller installation path is outside this tool's boundary")
    return resolved


def safe_path(root, relative):
    require(isinstance(relative, str) and relative, "empty document path")
    path = guard_path(root / relative)
    require(path.is_relative_to(root.resolve()) and path.suffix.lower() == ".md",
            "document must be Markdown inside the selected repository")
    return path


def save_new(path, data):
    """Publish a complete file with a no-replace hard link on the same volume."""
    path = guard_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".loading-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temp, path)
    finally:
        os.unlink(temp)


def report(kind, **fields):
    return {"schema": SCHEMA, "kind": kind, "toolVersion": VERSION,
            "toolSha256": digest(Path(__file__).read_bytes()),
            "createdAt": datetime.now(timezone.utc).isoformat(), **fields}


def verify_registration():
    registration = load_json(Path(__file__).with_name("loading-registration.json"))
    require(registration["version"] == VERSION and registration["executor"] == "conversion-system-only",
            "loading tool registration/version unavailable")
    for name in ("loading_preflight.py", "test_loading_preflight.py", "requirements-loading.txt"):
        require(registration["files"][name] == digest(Path(__file__).with_name(name).read_bytes()),
                f"registered component digest mismatch: {name}")


def parser():
    from markdown_it import MarkdownIt
    return MarkdownIt("commonmark").enable("table")


def walk(tokens):
    for token in tokens:
        yield token
        if token.children:
            yield from walk(token.children)


def slug(text):
    text = unicodedata.normalize("NFC", text).lower()
    return "".join(c for c in text if c in "-_ " or unicodedata.category(c)[0] in "LNM").replace(" ", "-")


def headings(tokens):
    used, counts = set(), {}
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            title = "".join(t.content for t in tokens[i + 1].children or []
                            if t.type in ("text", "code_inline", "image"))
            base = slug(title)
            n = counts.get(base, 0)
            candidate = base if n == 0 else f"{base}-{n}"
            while candidate in used:
                n += 1
                candidate = f"{base}-{n}"
            counts[base] = n + 1
            used.add(candidate)
    return used


def links(tokens):
    return [t.attrGet("href") for t in walk(tokens) if t.type == "link_open"]


def table_contracts(tokens):
    tables, current = [], None
    for token in tokens:
        if token.type == "table_open":
            current = []
        elif token.type == "table_close":
            tables.append(current)
            current = None
        elif current is not None and token.type == "inline":
            current.append(token)
    candidates = [t for t in tables if t and t[0].content == "契约标识"]
    require(len(candidates) == 1, "unknown required-contract table shape")
    cells = candidates[0]
    require(len(cells) == 4 * 8 and [t.content for t in cells[:4]] ==
            ["契约标识", "必读真源", "负责什么", "何时消费"], "unknown required-contract table columns")
    found = {}
    for i in range(4, len(cells), 4):
        ident = cells[i].content.strip("`")
        refs = links([cells[i + 1]])
        require(ident not in found and len(refs) == 1, "duplicate identity or ambiguous contract link")
        found[ident] = refs[0]
    # These identities are acceptance constraints, not an alternative loading route.
    require(found == CORE, "required contract identities differ (missing/replaced/extra)")
    return found


def check_repo(root):
    root = guard_path(root)
    names = list(ENTRIES) + list(CORE.values()) + list(WORKFLOWS.values())
    texts, tokens, files, findings, skipped = {}, {}, {}, [], []
    for name in names:
        try:
            raw = safe_path(root, name).read_bytes()
            texts[name] = raw.decode("utf-8-sig")
            require(texts[name].strip(), f"empty required document: {name}")
            tokens[name] = parser().parse(texts[name])
            files[name] = digest(raw)
        except (OSError, UnicodeError, Invalid) as exc:
            findings.append({"severity": "error", "file": name, "code": "unreadable", "detail": str(exc)})
    if "SKILL.md" in tokens:
        try:
            table_contracts(tokens["SKILL.md"])
        except Invalid as exc:
            findings.append({"severity": "error", "file": "SKILL.md", "code": "manifest", "detail": str(exc)})
    graph = {name: set() for name in names}
    for name, ts in tokens.items():
        for href in links(ts):
            url = urlsplit(href)
            if url.scheme or url.netloc:
                skipped.append({"file": name, "href": href, "reason": "external"})
                continue
            target = (root / name).parent / unquote(url.path) if url.path else root / name
            target = target.resolve()
            if not target.is_relative_to(root.resolve()):
                findings.append({"severity": "error", "file": name, "code": "escape", "detail": href})
                continue
            relative = target.relative_to(root.resolve()).as_posix()
            if relative not in names:
                skipped.append({"file": name, "href": href, "reason": "outside-scope"})
                continue
            graph[name].add(relative)
            if relative not in tokens or (url.fragment and unquote(url.fragment) not in headings(tokens[relative])):
                findings.append({"severity": "error", "file": name, "code": "link", "detail": href})
    for entry in ENTRIES[:2]:
        reached, pending = set(), [entry]
        while pending:
            current = pending.pop()
            if current not in reached:
                reached.add(current)
                pending.extend(graph[current] - reached)
        if "SKILL.md" not in reached:
            findings.append({"severity": "error", "file": entry, "code": "route", "detail": "root entry unreachable"})
    return report("structure", status="FAIL" if findings else "PASS", files=files,
                  findings=findings, skipped=skipped, contracts=CORE, workflows=WORKFLOWS,
                  parser="markdown-it-py/commonmark+table", anchorRule="unicode-category-v1",
                  parserVersion=package_version("markdown-it-py"), mdurlVersion=package_version("mdurl"),
                  scope="core-seven-and-two-workflows", semanticConsistency="MANUAL_REVIEW_REQUIRED",
                  uncovered=["languages", "directions", "scenes", "systems", "controller", "model-injection"])


def make_offer(root, name, start, end):
    require(name in (*ENTRIES, *CORE.values(), *WORKFLOWS.values()), "document outside declared loading scope")
    raw = safe_path(root, name).read_bytes()
    snapshot = raw.decode("utf-8")
    lines = snapshot.splitlines(keepends=True)
    require(lines and type(start) is int and type(end) is int and 1 <= start <= end <= len(lines), "invalid line range")
    body = "".join(lines[start - 1:end])
    payload = {"kind": "loading-read-v1", "document": name, "sha256": digest(raw),
               "sizeBytes": len(raw), "lineCount": len(lines), "startLine": start,
               "endLine": end, "text": body,
               "byteStart": len("".join(lines[:start - 1]).encode("utf-8")),
               "byteEnd": len("".join(lines[:end]).encode("utf-8"))}
    return report("offer", snapshotUtf8=snapshot, payload=payload)


def validate_offer(offer):
    require(offer["schema"] == SCHEMA and offer["kind"] == "offer", "not an offer")
    p, snapshot = offer["payload"], offer["snapshotUtf8"]
    require(p["kind"] == "loading-read-v1" and p["document"] in
            (*ENTRIES, *CORE.values(), *WORKFLOWS.values()), "offer outside declared scope")
    raw = snapshot.encode("utf-8")
    lines = snapshot.splitlines(keepends=True)
    start, end = p["startLine"], p["endLine"]
    require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines), "invalid offer range")
    require(p["sha256"] == digest(raw) and p["sizeBytes"] == len(raw) and p["lineCount"] == len(lines), "offer snapshot mismatch")
    require(p["text"] == "".join(lines[start - 1:end]) and
            p["byteStart"] == len("".join(lines[:start - 1]).encode("utf-8")) and
            p["byteEnd"] == len("".join(lines[:end]).encode("utf-8")), "offer range mismatch")
    return p


def output_strings(value):
    if isinstance(value, str):
        yield value
        try:
            decoded = json.loads(value)
        except (ValueError, TypeError):
            return
        yield from output_strings(decoded)
    elif isinstance(value, list):
        for part in value:
            yield from output_strings(part)
    elif isinstance(value, dict):
        # Only tool result containers, never call arguments or arbitrary echoed fields.
        for key in ("output", "text", "content"):
            if key in value:
                yield from output_strings(value[key])


def has_payload(output, payload):
    for text in output_strings(output):
        text = text.replace("\r\n", "\n")
        if text.startswith(MARKER):
            try:
                if json.loads(text[len(MARKER):]) == payload:
                    return True
            except ValueError:
                pass
    return False


def read_log(path):
    raw = guard_path(path).read_bytes()
    rows = []
    for i, line in enumerate(raw.splitlines(), 1):
        try:
            row = json.loads(line)
        except ValueError:
            # Live writers may leave an incomplete final line. It has no evidentiary value.
            require(i == len(raw.splitlines()) and not raw.endswith(b"\n"), "invalid transcript JSONL")
            continue
        require(isinstance(row, dict) and isinstance(row.get("payload", {}), dict), "invalid transcript row shape")
        rows.append((i, row))
    sessions = [r["payload"]["id"] for _, r in rows if r.get("type") == "session_meta"]
    require(len(set(sessions)) == 1 and isinstance(sessions[0], str) and sessions[0],
            "transcript session identity unavailable/ambiguous")
    return raw, rows, sessions[0]


def context_at(rows, limit):
    epoch = 0
    for line, row in rows:
        if line >= limit:
            break
        p = row.get("payload", {})
        if row.get("type") == "compacted" or p.get("type") in ("context_compacted", "context_reset"):
            epoch = line
    return epoch


def witness(path, call_id, payload):
    raw, rows, session = read_log(path)
    calls = [(n, r) for n, r in rows if r.get("type") == "response_item" and
             r.get("payload", {}).get("call_id") == call_id and
             r["payload"].get("type") in ("function_call", "custom_tool_call")]
    outputs = [(n, r) for n, r in rows if r.get("type") == "response_item" and
               r.get("payload", {}).get("call_id") == call_id and
               r["payload"].get("type") in ("function_call_output", "custom_tool_call_output")]
    require(len(calls) == len(outputs) == 1 and calls[0][0] < outputs[0][0], "call/output association unavailable")
    require(calls[0][1]["payload"].get("name") in ("exec", "exec_command"), "unsupported host read tool")
    line, row = outputs[0]
    require(has_payload(row["payload"]["output"], payload), "final host output does not contain exact complete offered payload")
    prefix = b"".join(raw.splitlines(keepends=True)[:line])
    return {"adapter": "codex-rollout-v1", "path": str(Path(path).resolve()),
            "prefixBytes": len(prefix), "prefixSha256": digest(prefix),
            "callId": call_id, "outputLine": line, "sessionId": session,
            "contextEpoch": context_at(rows, line), "toolName": calls[0][1]["payload"].get("name"),
            "timestamp": row.get("timestamp"),
            "outputSha256": digest(encoded(row["payload"]["output"]))}


def make_receipt(offer, transcript, call_id):
    payload = validate_offer(offer)
    return report("receipt", evidenceGrade="HOST_RETURN_OBSERVED", offer=offer,
                  witness=witness(transcript, call_id, payload),
                  limitations=["providing text does not prove understanding or retention",
                               "only recorded compaction/reset events are detectable",
                               "local logs are auditable evidence, not tamper-proof attestation"])


def verify_receipt(receipt):
    require(receipt["schema"] == SCHEMA and receipt["kind"] == "receipt" and
            receipt["evidenceGrade"] == "HOST_RETURN_OBSERVED", "unverified/self-declared receipt")
    p = validate_offer(receipt["offer"])
    w = receipt["witness"]
    with guard_path(w["path"]).open("rb") as stream:
        prefix = stream.read(w["prefixBytes"])
    require(digest(prefix) == w["prefixSha256"], "host evidence prefix changed")
    require(witness(w["path"], w["callId"], p) == w, "host evidence association changed")
    return p, w


def ref(path):
    path = guard_path(path)
    return {"path": str(path), "sha256": digest(path.read_bytes())}


def read_ref(pointer, base):
    path = guard_path(base / pointer["path"])
    require(digest(path.read_bytes()) == pointer["sha256"], f"evidence digest mismatch: {path}")
    return load_json(path)


def loading_record(path):
    tokens = parser().parse(guard_path(path).read_text(encoding="utf-8-sig"))
    blocks = [t.content for t in tokens if t.type == "fence" and t.info.strip() == "loading-preflight"]
    require(len(blocks) == 1, "one loading-preflight block required in existing frozen/stage record")
    data = json.loads(blocks[0])
    require(isinstance(data, dict) and isinstance(data.get("taskId"), str) and data["taskId"]
            and isinstance(data.get("runId"), str) and data["runId"], "task/run identity required")
    return data


def coverage(intervals, total):
    cursor = 1
    for start, end in sorted(intervals):
        if start > cursor:
            return False
        cursor = max(cursor, end + 1)
    return cursor == total + 1


def check_next(root, record_path, action, transcript, before_call=None):
    if action in RECOVERY:
        return report("next", status="PASS", action=action, scope="loading-only",
                      findings=[], exception="existing-job-query-evidence-cleanup",
                      executionAuthorized=False)
    data = loading_record(record_path)
    base = Path(record_path).resolve().parent
    findings = []
    def issue(code, detail):
        findings.append({"severity": "error", "code": code, "detail": detail})
    raw, rows, session = read_log(transcript)
    boundary = (rows[-1][0] if rows else 0) + 1
    if before_call:
        positions = [n for n, r in rows if r.get("type") == "response_item" and
                     r.get("payload", {}).get("call_id") == before_call and
                     r["payload"].get("type") in ("function_call", "custom_tool_call")]
        require(len(positions) == 1, "action call boundary unavailable/ambiguous")
        boundary = positions[0]
    epoch = context_at(rows, boundary)
    require(data["context"]["sessionId"] == session and data["context"]["epoch"] == epoch,
            "current session/context differs from loading record")
    selected = [name for key, name in CORE.items()
                if key != "classifier" or action in CLASSIFIER_ACTIONS]
    for key, name in WORKFLOWS.items():
        condition = data["workflows"][key]
        require(isinstance(condition["basis"], str) and condition["basis"].strip(),
                f"workflow applicability basis missing: {key}")
        if key == "long-file" and action == "start" and condition["applies"] is None:
            continue  # Source profiling establishes complexity before map/freeze.
        require(type(condition["applies"]) is bool, f"workflow applicability unknown: {key}")
        # Long-file classification can follow start, but is mandatory before mapping and freezing.
        if condition["applies"] and (key == "batch" or action != "start"):
            selected.append(name)
    structure = read_ref(data["structure"], base)
    require(structure["kind"] == "structure" and structure["schema"] == SCHEMA and
            structure["status"] == "PASS", "structure report not PASS")
    current = check_repo(root)
    require(current["status"] == "PASS" and current["files"] == structure["files"] and
            current["toolSha256"] == structure["toolSha256"] and
            current["parser"] == structure["parser"] and current["anchorRule"] == structure["anchorRule"] and
            current["parserVersion"] == structure["parserVersion"] and current["mdurlVersion"] == structure["mdurlVersion"],
            "structure version/tool changed/not PASS")
    ranges = {name: [] for name in selected}
    totals = {}
    for pointer in data["reads"]:
        receipt = read_ref(pointer, base)
        p, w = verify_receipt(receipt)
        name = p["document"]
        if name not in ranges:
            continue
        if (w["sessionId"] != session or w["contextEpoch"] != epoch or
                Path(w["path"]).resolve() != Path(transcript).resolve()):
            issue("context", name)
        elif w["outputLine"] >= boundary:
            issue("late-read", name)
        elif p["sha256"] != current["files"][name]:
            issue("version", name)
        else:
            ranges[name].append((p["startLine"], p["endLine"]))
            totals[name] = p["lineCount"]
    for name, intervals in ranges.items():
        if not coverage(intervals, totals.get(name, 1)):
            issue("coverage", name)
    return report("next", status="FAIL" if findings else "PASS", findings=findings,
                  action=action, taskId=data["taskId"], runId=data["runId"], scope="loading-only",
                  context={"sessionId": session, "epoch": epoch}, selected=selected,
                  boundary={"line": boundary, "prefixSha256": digest(raw)},
                  executionAuthorized=False, enforcement="AGENT_WORKFLOW_CHECK",
                  record=ref(record_path), structure=data["structure"])


def cli(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="command", required=True)
    repo = sub.add_parser("check-repo")
    repo.add_argument("--repo", type=Path, required=True)
    repo.add_argument("--out", type=Path, required=True)
    read = sub.add_parser("record-read")
    read.add_argument("--emit", action="store_true", help="prepare an offer and emit its exact text to the host")
    read.add_argument("--repo", type=Path)
    read.add_argument("--document")
    read.add_argument("--start-line", type=int)
    read.add_argument("--end-line", type=int)
    read.add_argument("--offer", type=Path)
    read.add_argument("--transcript", type=Path)
    read.add_argument("--call-id")
    read.add_argument("--out", type=Path, required=True)
    nxt = sub.add_parser("check-next")
    nxt.add_argument("--repo", type=Path, required=True)
    nxt.add_argument("--record", type=Path)
    nxt.add_argument("--action", choices=ACTIONS, required=True)
    nxt.add_argument("--transcript", type=Path)
    nxt.add_argument("--before-call")
    nxt.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)
    try:
        verify_registration()
        if args.command == "check-repo":
            result = check_repo(guard_path(args.repo))
        elif args.command == "record-read" and args.emit:
            require(args.repo and args.document and args.start_line and args.end_line and
                    not args.offer and not args.transcript and not args.call_id, "emit requires repo/document/line range only")
            result = make_offer(guard_path(args.repo), args.document, args.start_line, args.end_line)
        elif args.command == "record-read":
            require(args.offer and args.transcript and args.call_id and not args.document and not args.repo,
                    "record requires offer/transcript/call-id")
            result = make_receipt(load_json(args.offer), args.transcript, args.call_id)
        else:
            require(args.action in RECOVERY or (args.record and args.transcript), "next requires record/transcript")
            result = check_next(guard_path(args.repo), args.record, args.action, args.transcript, args.before_call)
        save_new(args.out, encoded(result) + b"\n")
        if args.command == "record-read" and args.emit:
            print(MARKER + json.dumps(result["payload"], ensure_ascii=False))
        else:
            print(json.dumps({"kind": result["kind"], "status": result.get("status", "RECORDED"),
                              "artifact": ref(args.out), "findings": result.get("findings", [])}, ensure_ascii=False))
        return 1 if result.get("status") == "FAIL" else 0
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(json.dumps({"status": "UNAVAILABLE", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(cli())
