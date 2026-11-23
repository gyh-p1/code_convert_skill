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
import re
import sys
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit

VERSION = "1.1.2"
SCHEMA = "loading-preflight/v1"
MARKER = "LOADING_READ_V1\n"
MANIFEST_PATH = "skills/routing-manifest.json"
MANIFEST_SCHEMA = "skill-routing-manifest/v1"
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
LANGUAGE_KEYS = ("c", "cpp", "csharp", "go", "powershell", "python", "ruby")
SCENE_KEYS = ("network-io", "file-io", "process-execution", "concurrency")
SYSTEM_KEYS = (
    "posix-winsock",
    "posix-windows-filesystem",
    "posix-windows-process-identity",
    "posix-windows-threads",
    "windows-registry-service-subsystem",
)
TOPIC_KEYS = ("security-behavior", "attack-tactic-index")
READ_TOOL_NAMES = ("read_file", "Read", "view_file")
READ_PATH_KEYS = ("path", "Path", "file_path", "filePath", "file")
ACTIONS = ("start", "map", "freeze", "classify", "source-precheck", "generate",
           "review", "submit", "resume", "close", "query", "collect", "terminate", "cleanup")
RECOVERY = ("query", "collect", "terminate", "cleanup")
# Classification serves evaluator admission; conversion-only actions use six common contracts.
CLASSIFIER_ACTIONS = ("classify", "source-precheck", "submit")
NUMBERED_LINE_RE = re.compile(r"^(\d+)(?:: |\t|\u2192)(.*)$")
SHOWING_LINES_RE = re.compile(r"Showing lines (\d+)-(\d+) of (\d+)")


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


def _validate_manifest(manifest):
    require(isinstance(manifest, dict) and manifest.get("schema") == MANIFEST_SCHEMA,
            "invalid routing manifest schema")
    require(manifest.get("coreEntries") == list(ENTRIES), "routing manifest coreEntries mismatch")
    require(manifest.get("coreContracts") == CORE, "routing manifest coreContracts mismatch")
    workflows = manifest.get("workflows")
    require(isinstance(workflows, dict) and set(workflows.keys()) == set(WORKFLOWS.keys()),
            "routing manifest workflows mismatch")
    for key, path in WORKFLOWS.items():
        require(isinstance(workflows[key], dict) and workflows[key].get("path") == path,
                f"routing manifest workflow path mismatch: {key}")
    require(isinstance(manifest.get("commonSemantics"), str) and manifest["commonSemantics"],
            "routing manifest commonSemantics missing")
    languages = manifest.get("languages")
    require(isinstance(languages, dict) and set(languages.keys()) == set(LANGUAGE_KEYS),
            "routing manifest languages mismatch")
    for key, item in languages.items():
        require(isinstance(item, dict) and isinstance(item.get("path"), str) and item["path"],
                f"routing manifest language path invalid: {key}")
    directions = manifest.get("directions")
    expected_dirs = {f"{s}-to-{t}": (s, t) for s in LANGUAGE_KEYS for t in LANGUAGE_KEYS if s != t}
    require(isinstance(directions, dict) and set(directions.keys()) == set(expected_dirs.keys()),
            "routing manifest directions mismatch")
    for key, (src, dst) in expected_dirs.items():
        entry = directions[key]
        require(isinstance(entry, dict) and entry.get("source") == src and entry.get("target") == dst
                and isinstance(entry.get("path"), str) and entry["path"]
                and isinstance(entry.get("references"), list),
                f"routing manifest direction invalid: {key}")
        for ref_item in entry["references"]:
            require(isinstance(ref_item, dict) and isinstance(ref_item.get("id"), str) and ref_item["id"]
                    and isinstance(ref_item.get("path"), str) and ref_item["path"],
                    f"routing manifest direction reference invalid: {key}")
    for group_name, expected_keys in (("scenes", SCENE_KEYS), ("systems", SYSTEM_KEYS), ("topics", TOPIC_KEYS)):
        group = manifest.get(group_name)
        require(isinstance(group, dict) and set(group.keys()) == set(expected_keys),
                f"routing manifest {group_name} mismatch")
        for key, item in group.items():
            require(isinstance(item, dict) and isinstance(item.get("path"), str) and item["path"],
                    f"routing manifest {group_name} path invalid: {key}")
            if "references" in item:
                require(isinstance(item["references"], list) and all(isinstance(r, str) and r for r in item["references"]),
                        f"routing manifest {group_name} references invalid: {key}")


def _requires_manifest(root):
    root = Path(root)
    if (root / MANIFEST_PATH).exists():
        return True
    skills_dir = root / "skills"
    if skills_dir.is_dir():
        allowed_rel = set(WORKFLOWS.values())
        for md_file in skills_dir.rglob("*.md"):
            rel = md_file.resolve().relative_to(root.resolve()).as_posix()
            if rel not in allowed_rel:
                return True
        for child in skills_dir.iterdir():
            if child.is_dir() and child.name != "workflows":
                return True
    skill_md = root / "SKILL.md"
    if skill_md.is_file():
        try:
            text = skill_md.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            return False
        if "routing-manifest.json" in text or "skills/directions/" in text:
            return True
    return False


def load_manifest(root):
    path = guard_path(Path(root) / MANIFEST_PATH)
    if not path.exists():
        require(not _requires_manifest(root), "required routing-manifest.json missing in knowledge repository")
        return None
    raw = path.read_bytes()
    try:
        manifest = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeError, ValueError) as exc:
        raise Invalid(f"unreadable routing manifest: {exc}") from exc
    _validate_manifest(manifest)
    return manifest, digest(raw)


def manifest_paths(manifest):
    ordered = []
    seen = set()

    def add(p):
        if p not in seen:
            seen.add(p)
            ordered.append(p)

    for p in manifest["coreEntries"]:
        add(p)
    for p in manifest["coreContracts"].values():
        add(p)
    for item in manifest["workflows"].values():
        add(item["path"])
    add(manifest["commonSemantics"])
    for item in manifest["languages"].values():
        add(item["path"])
    for item in manifest["directions"].values():
        add(item["path"])
        for ref_item in item["references"]:
            add(ref_item["path"])
    for item in manifest["scenes"].values():
        add(item["path"])
        for ref_path in item.get("references", ()):
            add(ref_path)
    for item in manifest["systems"].values():
        add(item["path"])
    for item in manifest["topics"].values():
        add(item["path"])
    return ordered


def allowed_docs(root):
    loaded = load_manifest(root)
    if loaded is not None:
        return tuple(manifest_paths(loaded[0]))
    return (*ENTRIES, *CORE.values(), *WORKFLOWS.values())


def _default_allowed_docs():
    docs = set((*ENTRIES, *CORE.values(), *WORKFLOWS.values()))
    repo_root = Path(__file__).resolve().parent.parent
    manifest_file = repo_root / MANIFEST_PATH
    if manifest_file.exists():
        loaded = load_manifest(repo_root)
        if loaded is not None:
            docs.update(manifest_paths(loaded[0]))
    return tuple(docs)


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
    findings = []
    manifest = None
    manifest_sha = None
    try:
        loaded = load_manifest(root)
        if loaded is not None:
            manifest, manifest_sha = loaded
    except Invalid as exc:
        code = "manifest-missing" if "missing" in str(exc) and not (root / MANIFEST_PATH).exists() else "manifest"
        findings.append({"severity": "error", "file": MANIFEST_PATH, "code": code, "detail": str(exc)})
    names = manifest_paths(manifest) if manifest is not None else list(ENTRIES) + list(CORE.values()) + list(WORKFLOWS.values())
    md = parser()
    texts, tokens, files, skipped = {}, {}, {}, []
    for name in names:
        try:
            raw = safe_path(root, name).read_bytes()
            texts[name] = raw.decode("utf-8-sig")
            require(texts[name].strip(), f"empty required document: {name}")
            tokens[name] = md.parse(texts[name])
            files[name] = digest(raw)
        except (OSError, UnicodeError, Invalid) as exc:
            findings.append({"severity": "error", "file": name, "code": "unreadable", "detail": str(exc)})
    if manifest is not None:
        skills_dir = root / "skills"
        if skills_dir.is_dir():
            name_set = set(names)
            for md_file in sorted(skills_dir.rglob("*.md")):
                rel = md_file.resolve().relative_to(root.resolve()).as_posix()
                if rel not in name_set:
                    findings.append({"severity": "error", "file": rel, "code": "manifest-unregistered",
                                     "detail": "unregistered markdown under skills/"})
    if "SKILL.md" in tokens:
        try:
            table_contracts(tokens["SKILL.md"])
        except Invalid as exc:
            findings.append({"severity": "error", "file": "SKILL.md", "code": "manifest", "detail": str(exc)})
    heading_cache = {name: headings(ts) for name, ts in tokens.items()}
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
            if relative not in heading_cache or (url.fragment and unquote(url.fragment) not in heading_cache[relative]):
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
    extra = {}
    if manifest is not None:
        scope = "full-core-workflows-and-knowledge-manifest"
        uncovered = ["controller", "model-injection"]
        extra["manifestSha256"] = manifest_sha
    else:
        scope = "core-seven-and-two-workflows"
        uncovered = ["languages", "directions", "scenes", "systems", "controller", "model-injection"]
    return report("structure", status="FAIL" if findings else "PASS", files=files,
                  findings=findings, skipped=skipped, contracts=CORE, workflows=WORKFLOWS,
                  parser="markdown-it-py/commonmark+table", anchorRule="unicode-category-v1",
                  parserVersion=package_version("markdown-it-py"), mdurlVersion=package_version("mdurl"),
                  scope=scope, semanticConsistency="MANUAL_REVIEW_REQUIRED",
                  uncovered=uncovered, **extra)


def make_offer(root, name, start, end):
    require(name in allowed_docs(root), "document outside declared loading scope")
    document_path = safe_path(root, name)
    raw = document_path.read_bytes()
    snapshot = raw.decode("utf-8")
    lines = snapshot.splitlines(keepends=True)
    require(lines and type(start) is int and type(end) is int and 1 <= start <= end <= len(lines), "invalid line range")
    body = "".join(lines[start - 1:end])
    payload = {"kind": "loading-read-v1", "document": name, "documentPath": str(document_path),
               "sha256": digest(raw),
               "sizeBytes": len(raw), "lineCount": len(lines), "startLine": start,
               "endLine": end, "text": body,
               "byteStart": len("".join(lines[:start - 1]).encode("utf-8")),
               "byteEnd": len("".join(lines[:end]).encode("utf-8"))}
    return report("offer", snapshotUtf8=snapshot, payload=payload)


def validate_offer(offer, allowed=None):
    require(offer["schema"] == SCHEMA and offer["kind"] == "offer", "not an offer")
    p, snapshot = offer["payload"], offer["snapshotUtf8"]
    valid_docs = allowed if allowed is not None else _default_allowed_docs()
    require(p["kind"] == "loading-read-v1" and p["document"] in valid_docs, "offer outside declared scope")
    if "documentPath" in p:
        require(_match_doc_path(p["documentPath"], p["documentPath"]), "invalid offered document path")
    raw = snapshot.encode("utf-8")
    lines = snapshot.splitlines(keepends=True)
    start, end = p["startLine"], p["endLine"]
    require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines), "invalid offer range")
    require(p["sha256"] == digest(raw) and p["sizeBytes"] == len(raw) and p["lineCount"] == len(lines), "offer snapshot mismatch")
    require(p["text"] == "".join(lines[start - 1:end]) and
            p["byteStart"] == len("".join(lines[:start - 1]).encode("utf-8")) and
            p["byteEnd"] == len("".join(lines[:end]).encode("utf-8")), "offer range mismatch")
    return p


def _is_truncated(node):
    return isinstance(node, dict) and any(node.get(k) is True for k in ("truncated", "is_truncated", "isTruncated"))


def output_strings(value):
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except (ValueError, TypeError):
            yield value
            return
        if _is_truncated(decoded):
            return
        yield value
        yield from output_strings(decoded)
    elif isinstance(value, list):
        for part in value:
            yield from output_strings(part)
    elif isinstance(value, dict):
        if _is_truncated(value):
            return
        # Only tool result containers, never call arguments or arbitrary echoed fields.
        for key in ("output", "text", "content", "result"):
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


def _match_doc_path(candidate, expected, cwd=None):
    if not isinstance(candidate, str) or not candidate or not isinstance(expected, str):
        return False
    path = Path(candidate)
    if not path.is_absolute():
        if path.anchor or not isinstance(cwd, str) or not Path(cwd).is_absolute():
            return False
        path = Path(cwd) / path
    # Match the recorded checkout without resolving aliases against today's filesystem.
    return ".." not in path.parts and str(path) == expected


def _match_native_text_block(text, payload):
    normalized = text.replace("\r\n", "\n")
    expected_text = payload["text"].replace("\r\n", "\n")
    if text == payload["text"] or normalized == expected_text:
        return True
    header = SHOWING_LINES_RE.search(normalized)
    if header:
        shown_start, shown_end, shown_total = int(header.group(1)), int(header.group(2)), int(header.group(3))
        if shown_start > payload["startLine"] or shown_end < payload["endLine"] or shown_total != payload["lineCount"]:
            return False
    numbered = {}
    for line in normalized.splitlines():
        m = NUMBERED_LINE_RE.match(line)
        if m:
            numbered[int(m.group(1))] = m.group(2)
    if not numbered:
        return False
    expected_lines = expected_text.splitlines()
    start = payload["startLine"]
    if len(expected_lines) != (payload["endLine"] - start + 1):
        # Preserve explicit trailing blank line case if splitlines omitted final empty entry.
        expected_lines = expected_text.split("\n")
        if expected_lines and expected_lines[-1] == "":
            expected_lines = expected_lines[:-1]
    if len(expected_lines) != (payload["endLine"] - start + 1):
        return False
    for offset, expected_line in enumerate(expected_lines):
        if numbered.get(start + offset) != expected_line:
            return False
    return True


def has_native_read_payload(output, payload, cwd=None):
    def check_node(node):
        if isinstance(node, str):
            try:
                decoded = json.loads(node)
            except (ValueError, TypeError):
                decoded = None
            if isinstance(decoded, (dict, list)):
                return check_node(decoded)
            normalized = node.replace("\r\n", "\n")
            if normalized.startswith(MARKER):
                try:
                    if json.loads(normalized[len(MARKER):]) == payload:
                        return True
                except ValueError:
                    pass
            return _match_native_text_block(node, payload)
        if isinstance(node, list):
            return any(check_node(part) for part in node)
        if isinstance(node, dict):
            if _is_truncated(node):
                return False
            document = node.get("document")
            expected_path = payload["documentPath"]
            if (document is not None and document != payload["document"]
                    and not _match_doc_path(document, expected_path, cwd)):
                return False
            if any(not _match_doc_path(node[key], expected_path, cwd)
                   for key in (*READ_PATH_KEYS, "documentPath") if node.get(key) is not None):
                return False
            s_val = node.get("startLine", node.get("start_line"))
            e_val = node.get("endLine", node.get("end_line"))
            if s_val is not None or e_val is not None:
                if s_val != payload["startLine"] or e_val != payload["endLine"]:
                    return False
            for key in ("output", "text", "content", "result"):
                if key in node and check_node(node[key]):
                    return True
            return False
        return False

    return check_node(output)


def _row_call_id(row):
    p = row.get("payload", {})
    return p.get("call_id", row.get("call_id"))


def _row_kind(row):
    t = row.get("type")
    if t == "response_item":
        return row.get("payload", {}).get("type")
    return t


def _row_name(row):
    p = row.get("payload", {})
    return p.get("name", row.get("name"))


def _row_output(row):
    p = row.get("payload", {})
    if "output" in p:
        return p["output"]
    for key in ("output", "result", "content"):
        if key in row:
            return row[key]
    return None


def _extract_call_args(call_row):
    p = call_row.get("payload", {})
    for container in (p, call_row):
        for key in ("arguments", "input", "args"):
            if key in container:
                val = container[key]
                if isinstance(val, dict):
                    return val
                if isinstance(val, str):
                    try:
                        decoded = json.loads(val)
                    except (ValueError, TypeError):
                        continue
                    if isinstance(decoded, dict):
                        return decoded
    return {}


def _load_log_entry(path, _log_cache=None):
    resolved_key = str(guard_path(path))
    if _log_cache is not None and resolved_key in _log_cache:
        return _log_cache[resolved_key]
    raw = Path(resolved_key).read_bytes()
    raw_lines = raw.splitlines(keepends=True)
    cum_bytes = [0]
    for raw_ln in raw_lines:
        cum_bytes.append(cum_bytes[-1] + len(raw_ln))
    rows = []
    by_call_id = {}
    for i, line in enumerate(raw.splitlines(), 1):
        try:
            row = json.loads(line)
        except ValueError:
            # Live writers may leave an incomplete final line. It has no evidentiary value.
            require(i == len(raw.splitlines()) and not raw.endswith(b"\n"), "invalid transcript JSONL")
            continue
        require(isinstance(row, dict) and isinstance(row.get("payload", {}), dict), "invalid transcript row shape")
        rows.append((i, row))
        cid = _row_call_id(row)
        if cid is not None:
            by_call_id.setdefault(cid, []).append((i, row))
    sessions = [r["payload"]["id"] for _, r in rows
                if r.get("type") == "session_meta" and isinstance(r["payload"].get("id"), str)]
    if not sessions:
        sessions = [r["sessionId"] for _, r in rows
                    if isinstance(r.get("sessionId"), str) and r["sessionId"]]
    require(len(set(sessions)) == 1 and isinstance(sessions[0], str) and sessions[0],
            "transcript session identity unavailable/ambiguous")
    entry = {"raw": raw, "cum_bytes": cum_bytes, "rows": rows,
             "by_call_id": by_call_id, "session": sessions[0]}
    if _log_cache is not None:
        _log_cache[resolved_key] = entry
    return entry


def read_log(path, _log_cache=None):
    entry = _load_log_entry(path, _log_cache=_log_cache)
    return entry["raw"], entry["rows"], entry["session"]


def context_at(rows, limit):
    epoch = 0
    for line, row in rows:
        if line >= limit:
            break
        p = row.get("payload", {})
        if row.get("type") == "compacted" or p.get("type") in ("context_compacted", "context_reset"):
            epoch = line
    return epoch


def witness(path, call_id, payload, _log_cache=None):
    entry = _load_log_entry(path, _log_cache=_log_cache)
    raw, rows, session = entry["raw"], entry["rows"], entry["session"]
    matching = entry["by_call_id"].get(call_id, ())
    calls = [(n, r) for n, r in matching if _row_kind(r) in ("function_call", "custom_tool_call", "tool_call")]
    outputs = [(n, r) for n, r in matching if _row_kind(r) in ("function_call_output", "custom_tool_call_output", "tool_result")]
    require(len(calls) == len(outputs) == 1 and calls[0][0] < outputs[0][0], "call/output association unavailable")
    tool_name = _row_name(calls[0][1])
    line, row = outputs[0]
    require(not (_is_truncated(row) or _is_truncated(row.get("payload"))),
            "host marked tool result as truncated")
    raw_out = _row_output(row)
    if tool_name in ("exec", "exec_command"):
        require(has_payload(raw_out, payload), "final host output does not contain exact complete offered payload")
        adapter = "codex-rollout-v1"
    elif tool_name in READ_TOOL_NAMES:
        call_args = _extract_call_args(calls[0][1])
        paths = [call_args[key] for key in (*READ_PATH_KEYS, "document") if call_args.get(key) is not None]
        cwd = call_args.get("cwd", call_args.get("workdir"))
        require(paths and all(_match_doc_path(path, payload.get("documentPath"), cwd) for path in paths),
                "read tool call target path missing or does not match offered document")
        req_start = next((call_args.get(k) for k in ("startLine", "StartLine", "start_line")
                          if call_args.get(k) is not None), None)
        req_end = next((call_args.get(k) for k in ("endLine", "EndLine", "end_line")
                        if call_args.get(k) is not None), None)
        if req_start is not None:
            require(type(req_start) is int and req_start <= payload["startLine"],
                    "read tool call startLine exceeds offered startLine")
        if req_end is not None:
            require(type(req_end) is int and req_end >= payload["endLine"],
                    "read tool call endLine precedes offered endLine")
        require(has_native_read_payload(raw_out, payload, cwd), "final read tool output does not contain exact offered text")
        adapter = "generic-read-tool-v1"
    else:
        raise Invalid("unsupported host read tool")
    prefix = raw[:entry["cum_bytes"][line]]
    return {"adapter": adapter, "path": str(Path(path).resolve()),
            "prefixBytes": len(prefix), "prefixSha256": digest(prefix),
            "callId": call_id, "outputLine": line, "sessionId": session,
            "contextEpoch": context_at(rows, line), "toolName": tool_name,
            "timestamp": row.get("timestamp"),
            "outputSha256": digest(encoded(raw_out))}


def make_receipt(offer, transcript, call_id):
    payload = validate_offer(offer)
    return report("receipt", evidenceGrade="HOST_RETURN_OBSERVED", offer=offer,
                  witness=witness(transcript, call_id, payload),
                  limitations=["providing text does not prove understanding or retention",
                               "only recorded compaction/reset events are detectable",
                               "local logs are auditable evidence, not tamper-proof attestation"])


def verify_receipt(receipt, allowed=None, _log_cache=None):
    require(receipt["schema"] == SCHEMA and receipt["kind"] == "receipt" and
            receipt["evidenceGrade"] == "HOST_RETURN_OBSERVED", "unverified/self-declared receipt")
    p = validate_offer(receipt["offer"], allowed=allowed)
    w = receipt["witness"]
    resolved = str(guard_path(w["path"]))
    if _log_cache is not None and resolved in _log_cache:
        prefix = _log_cache[resolved]["raw"][:w["prefixBytes"]]
    else:
        with Path(resolved).open("rb") as stream:
            prefix = stream.read(w["prefixBytes"])
    require(digest(prefix) == w["prefixSha256"], "host evidence prefix changed")
    require(witness(w["path"], w["callId"], p, _log_cache=_log_cache) == w, "host evidence association changed")
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


def _validate_closed_routing_group(group_obj, expected_items, group_name, selected):
    require(isinstance(group_obj, dict), f"routing group missing: {group_name}")
    require(set(group_obj.keys()) == set(expected_items.keys()),
            f"routing closed-set keys mismatch: {group_name}")
    for key, item_meta in expected_items.items():
        entry = group_obj[key]
        require(isinstance(entry, dict) and type(entry.get("applies")) is bool,
                f"routing applies boolean missing: {group_name}.{key}")
        require(isinstance(entry.get("basis"), str) and entry["basis"].strip(),
                f"routing basis missing: {group_name}.{key}")
        if entry["applies"]:
            selected.append(item_meta["path"])


def _resolve_routing_selected(manifest, data, action):
    routing = data.get("routing")
    if routing is None:
        require(action in ("start", "map"), "knowledge routing closed-set block required")
        return [], None
    require(isinstance(routing, dict), "routing block must be an object")
    direction = routing.get("direction")
    require(isinstance(direction, str) and direction in manifest["directions"],
            f"unknown routing direction: {direction!r}")
    dir_info = manifest["directions"][direction]
    selected = [
        manifest["commonSemantics"],
        manifest["languages"][dir_info["source"]]["path"],
        manifest["languages"][dir_info["target"]]["path"],
        dir_info["path"],
    ]
    dir_refs = {ref_item["id"]: ref_item for ref_item in dir_info["references"]}
    _validate_closed_routing_group(routing.get("directionReferences"), dir_refs, "directionReferences", selected)
    _validate_closed_routing_group(routing.get("scenes"), manifest["scenes"], "scenes", selected)
    _validate_closed_routing_group(routing.get("systems"), manifest["systems"], "systems", selected)
    _validate_closed_routing_group(routing.get("topics"), manifest["topics"], "topics", selected)
    return list(dict.fromkeys(selected)), dir_refs


def _scan_source_signals(manifest, data, dir_refs, sources, strict_signals):
    conflicts = []
    if not sources or manifest is None:
        return conflicts
    severity = "error" if strict_signals else "warning"
    routing = data.get("routing") if isinstance(data.get("routing"), dict) else None
    long_wf = data["workflows"]["long-file"]
    threshold = manifest["workflows"]["long-file"].get("lineThreshold", 700)
    for src in sources:
        src_path = guard_path(src)
        require(src_path.is_file(), f"source file unavailable for static signal scan: {src}")
        src_text = src_path.read_text(encoding="utf-8", errors="replace")
        lf_lines = src_text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
        if long_wf["applies"] is False and len(lf_lines) > threshold:
            conflicts.append({
                "severity": severity,
                "code": "trigger-signal-conflict",
                "slot": "workflows.long-file",
                "source": str(src_path),
                "signals": [f"lines={len(lf_lines)}>{threshold}"],
                "detail": f"source has {len(lf_lines)} LF lines (>{threshold}) while workflows.long-file.applies=false",
            })
        if routing is None:
            continue
        groups = [
            ("directionReferences", dir_refs or {}),
            ("scenes", manifest["scenes"]),
            ("systems", manifest["systems"]),
            ("topics", manifest["topics"]),
        ]
        for group_name, expected_items in groups:
            group_obj = routing.get(group_name, {})
            if not isinstance(group_obj, dict):
                continue
            for key, item_meta in expected_items.items():
                entry = group_obj.get(key)
                if isinstance(entry, dict) and entry.get("applies") is False:
                    signals = item_meta.get("triggerSignals", ())
                    matched = [sig for sig in signals if sig and sig in src_text]
                    if matched:
                        conflicts.append({
                            "severity": severity,
                            "code": "trigger-signal-conflict",
                            "slot": f"{group_name}.{key}",
                            "source": str(src_path),
                            "signals": matched,
                            "detail": f"source matches trigger signals {matched!r} while {group_name}.{key}.applies=false",
                        })
    return conflicts


def check_next(root, record_path, action, transcript, before_call=None, sources=None, strict_signals=False):
    if action in RECOVERY:
        return report("next", status="PASS", action=action, scope="loading-only",
                      findings=[], signalConflicts=[], exception="existing-job-query-evidence-cleanup",
                      executionAuthorized=False)
    data = loading_record(record_path)
    base = Path(record_path).resolve().parent
    findings = []
    def issue(code, detail):
        findings.append({"severity": "error", "code": code, "detail": detail})
    log_cache = {}
    raw, rows, session = read_log(transcript, _log_cache=log_cache)
    boundary = (rows[-1][0] if rows else 0) + 1
    if before_call:
        positions = [n for n, r in rows if _row_call_id(r) == before_call and
                     _row_kind(r) in ("function_call", "custom_tool_call", "tool_call")]
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
    loaded = load_manifest(root)
    manifest = loaded[0] if loaded is not None else None
    dir_refs = None
    if manifest is not None:
        routed_docs, dir_refs = _resolve_routing_selected(manifest, data, action)
        for doc in routed_docs:
            if doc not in selected:
                selected.append(doc)
    structure = read_ref(data["structure"], base)
    require(structure["kind"] == "structure" and structure["schema"] == SCHEMA and
            structure["status"] == "PASS", "structure report not PASS")
    current = check_repo(root)
    require(current["status"] == "PASS" and current["files"] == structure["files"] and
            current.get("manifestSha256") == structure.get("manifestSha256") and
            current["toolSha256"] == structure["toolSha256"] and
            current["parser"] == structure["parser"] and current["anchorRule"] == structure["anchorRule"] and
            current["parserVersion"] == structure["parserVersion"] and current["mdurlVersion"] == structure["mdurlVersion"],
            "structure version/tool changed/not PASS")
    allowed = tuple(manifest_paths(manifest)) if manifest is not None else (*ENTRIES, *CORE.values(), *WORKFLOWS.values())
    ranges = {name: [] for name in selected}
    totals = {}
    rejected_reasons = {name: [] for name in selected}
    superseded_receipts = 0
    resolved_transcript = Path(transcript).resolve()
    for pointer in data["reads"]:
        receipt = read_ref(pointer, base)
        p, w = verify_receipt(receipt, allowed=allowed, _log_cache=log_cache)
        name = p["document"]
        if name not in ranges:
            continue
        if (w["sessionId"] != session or w["contextEpoch"] != epoch or
                Path(w["path"]).resolve() != resolved_transcript):
            if "context" not in rejected_reasons[name]:
                rejected_reasons[name].append("context")
            superseded_receipts += 1
        elif w["outputLine"] >= boundary:
            if "late-read" not in rejected_reasons[name]:
                rejected_reasons[name].append("late-read")
            superseded_receipts += 1
        elif (p["sha256"] != current["files"][name] or
              ("documentPath" in p and p["documentPath"] != str(safe_path(root, name)))):
            if "version" not in rejected_reasons[name]:
                rejected_reasons[name].append("version")
            superseded_receipts += 1
        else:
            ranges[name].append((p["startLine"], p["endLine"]))
            totals[name] = p["lineCount"]
    for name, intervals in ranges.items():
        if not coverage(intervals, totals.get(name, 1)):
            for reason in rejected_reasons[name]:
                issue(reason, name)
            issue("coverage", name)
    signal_conflicts = _scan_source_signals(manifest, data, dir_refs, sources or [], strict_signals)
    if strict_signals:
        for conflict in signal_conflicts:
            issue(conflict["code"], f"{conflict['slot']}: {conflict['detail']}")
    return report("next", status="FAIL" if findings else "PASS", findings=findings,
                  signalConflicts=signal_conflicts, supersededReceipts=superseded_receipts,
                  action=action, taskId=data["taskId"],
                  runId=data["runId"], scope="loading-only",
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
    nxt.add_argument("--source", dest="sources", action="append", type=Path,
                     help="read-only source path(s) for static trigger-signal cross-check")
    nxt.add_argument("--strict-signals", action="store_true",
                     help="promote trigger-signal conflicts to failing findings")
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
            result = check_next(guard_path(args.repo), args.record, args.action, args.transcript,
                                args.before_call, sources=args.sources, strict_signals=args.strict_signals)
        save_new(args.out, encoded(result) + b"\n")
        if args.command == "record-read" and args.emit:
            print(MARKER + json.dumps(result["payload"], ensure_ascii=False))
        else:
            print(json.dumps({"kind": result["kind"], "status": result.get("status", "RECORDED"),
                              "artifact": ref(args.out), "findings": result.get("findings", []),
                              "signalConflicts": result.get("signalConflicts", [])}, ensure_ascii=False))
        return 1 if result.get("status") == "FAIL" else 0
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(json.dumps({"status": "UNAVAILABLE", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(cli())
