#!/usr/bin/env python3
"""Static text classifier with highest-risk blocking admission.

Input-integrity errors block first; public/hostname targets without declared
network isolation block next; high-confidence credential findings also block.
Other review signals remain admission-eligible with applicable context flags.
ALLOWED is classification only, not execution authorization or proof of isolation.

Ambiguous hostname:port/service literals follow hostname admission rules.
Explicit XML-literal namespace and C# assembly-version metadata exclusions apply
only in a source set without detected network signals; method names establish no exemption.
Known file suffixes without network API context can identify path literals.
Input paths resolve within the manifest-directory and declared-source-base bounds.
Samples are read as text, never imported, compiled, or executed.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import ipaddress
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VERSION = "2.6"
MAX_BYTES = 2 * 1024 * 1024
MAX_FILES = 128
SOURCE_EXTENSIONS = {".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".cs",
                     ".go", ".py", ".ps1", ".psm1", ".rb"}
# These are lexical signals, deliberately not claims about reachability.
# Case matters where two ecosystems spell the same idea differently: Go/Python/C#
# PascalCase module functions (`os.WriteFile`, `subprocess.Popen`) must not be read
# as the Win32 API of the same name, or every Go file becomes a Windows file-write.
SIGNALS = {
    "network": r"\b(?:socket|connect|bind|listen|accept|tcpclient|tcpserver|udpclient|"
               r"webclient|httpclient|requests|urlopen|curl|wget|invoke-webrequest|"
               r"invoke-restmethod|getaddrinfo|gethostbyname|dnsquery|sendto|recvfrom|"
               r"winhttp\w*|internetopen\w*|downloadstring|downloadfile)\b|"
               r"\b(?:net|http)\s*\.\s*(?:dial\w*|listen\w*|get|post|serve\w*)\b",
    "filesystem": r"\b(?:fopen|fwrite|unlink|remove|rename|WriteFile|DeleteFile\w*|"
                  r"CreateFile\w*|WriteAll\w*|ReadAll\w*|Remove-Item|Set-Content|Out-File|New-Item|"
                  r"write_text|write_bytes|read_text|read_bytes|rmtree|mkdir|chmod|fstream|ifstream|"
                  r"ofstream|filesystem|directory_iterator|creat|symlink|writefile|readfile)\b|"
                  r"\bopen\s*\(|"
                  # Go standard library is spelled in PascalCase too, but the receiver
                  # is `os`, so it is a distinct construct from the Win32 API.
                  r"\bos\s*\.\s*(?i:WriteFile|ReadFile|Create|Remove|RemoveAll|Mkdir\w*|OpenFile|Rename)\b",
    "process": r"\b(?:subprocess|popen|system|execve|execl|fork|spawn|"
               r"createprocess\w*|shellexecute\w*|start-process|invoke-expression|"
               r"process\s*\.\s*start|exec\s*\.\s*command|os\s*\.\s*exec|win32_process|execmethod|"
               r"netsh|wmic|schtasks|cmd\.exe|powershell\.exe|pwsh|bash|sudo)\b",
    "discovery": r"\b(?:getenvironment\w*|getenv|environ|psutil|getcomputername\w*|getusername\w*|getuid|geteuid)\b",
    "sensitive": r"\b(?:virtualalloc\w*|virtualprotect\w*|writeprocessmemory|createremotethread|"
                 r"minidumpwritedump|openprocesstoken|adjusttokenprivileges|"
                 r"credential|lsass|ptrace|setuid|regset\w*|regdelete\w*|regcreate\w*|"
                 r"regopen\w*|registrykey|winreg|mprotect|page_execute\w*|"
                 r"ntallocatevirtualmemory|module_init|module_exit|kallsyms_lookup_name|__asm|asm)\b|"
                 r"\bnetsh\b[^\n]*\bkey\s*=\s*clear\b",
    "dynamic_code": r"(?<![\w.\-])(?:eval|exec|compile|loadlibrary\w*|"
                    r"getprocaddress|dlopen|dlsym|add-type)(?![\w.\-])|"
                    r"(?<![\w.\-])invoke-expression(?![\w.\-])",
    "framework": r"\bMetasploitModule\b|\bMsf::|\brequire\s*['\"]msf",
}
# Signals that must respect case: a lowercase-only match is a different construct.
CASE_SENSITIVE_SIGNALS = {"filesystem"}
COMPILED = {name: re.compile(pattern, 0 if name in CASE_SENSITIVE_SIGNALS else re.I)
            for name, pattern in SIGNALS.items()}
URL = re.compile(r"\b(?:https?|ftp|tcp|udp)://(?:[^/\s@'\"]{0,80}@)?(\[[^\]]+\]|[A-Za-z0-9_.\-]+)", re.I)
IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
QUOTED_HOST = re.compile(r"""['"](\[?[A-Fa-f0-9:]+\]?|localhost|(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,63})['"]""", re.I)
PRIVATE_V4 = tuple(ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"))
PRIVATE_V6 = ipaddress.ip_network("fc00::/7")

# Block only HIGH-CONFIDENCE real credential material. A keyword such as
# "password" is explicitly NOT enough, because the body must be a placeholder value.
# These patterns describe credential *formats* that cannot be produced by accident.
CREDENTIAL_PATTERNS = {
    "private_key_block": re.compile(r"-----BEGIN\s+(?:RSA|DSA|EC|OPENSSH|PGP|ENCRYPTED)?\s*PRIVATE KEY-----"),
    "aws_access_key_id": re.compile(r"\b(?:AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    "slack_token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),
    "google_api_key": re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b"),
    "url_with_password": re.compile(r"\b[a-z][a-z0-9+.\-]*://[^/\s:@'\"]{1,64}:[^/\s:@'\"]{6,}@"),
}
# Assignment-looking hosts such as "password": "changeme" are placeholders, not credentials.
CREDENTIAL_PLACEHOLDERS = re.compile(
    r"^(?:|x+|X+|\.+|_+|-+|\*+|\$\{[^}]*\}|%[sd]|\{\{?[\w.\-]*\}?\}?|"
    r"change[-_]?me|changeme|placeholder|example|sample|test|testing|dummy|fake|mock|"
    r"redacted|todo|fixme|none|null|nil|<[^>]*>|your[-_ ]?\w*|my[-_ ]?\w*|"
    r"secret|password|passwd|pwd|token|apikey|api[-_]key|username|user|admin|"
    r"0{4,}|1{4,}|1234567?8?|abc123|foo|bar|baz|bob|alice)$",
    re.I)

# `scheme://user:password@host` — the host is what network scope must judge, and the
# userinfo part must never be mistaken for a hostname.
URL_USERINFO = re.compile(r"://[^/\s@'\"]*@")


def url_host(value: str) -> str:
    """Return the host part of a URL match, dropping any userinfo component."""
    return URL_USERINFO.sub("://", value, count=1)


# Bare file-name literals (data/config/log/source files) share the
# `label.label` shape of a DNS name, so QUOTED_HOST matches e.g. "demo.txt".
# These common file suffixes support a lexical path candidate; they are not a
# hostname whitelist. A surrounding network API keeps the value as a target
# (see analyze_behavior); data flow outside that context remains unproven.
FILENAME_EXTENSIONS = {
    "txt", "text", "json", "yaml", "yml", "xml", "csv", "tsv", "log", "bak",
    "tmp", "ini", "cfg", "conf", "dat", "lock", "md", "pdf", "html", "htm",
    "py", "rb", "go", "cs", "cpp", "c", "h", "js", "ts", "ps1", "psm1",
}


def _looks_like_filename(value: str) -> bool:
    """True when a QUOTED_HOST literal is really a file name, not a hostname."""
    if "://" in value or "@" in value or ":" in value:
        return False
    _, dot, ext = value.rpartition(".")
    return bool(dot) and ext.lower() in FILENAME_EXTENSIONS


def _metadata_literal_reason(code: str, start: int, suffix: str) -> str | None:
    """Recognize literal metadata syntax, never infer receiver types from method names.

    Deliberately not a data-flow/reachability proof. Ambiguous URL assignments stay
    network candidates, and another occurrence used by a network API is examined
    independently. Caller disables these exclusions when any network signal is
    present in this source; a local statement alone cannot prove data-flow safety.
    """
    prefix = code[max(0, start - 512):start]
    statement = re.split(r"[;\n]", prefix)[-1]
    if COMPILED["network"].search(statement):
        return None
    if re.search(
        r'''<[A-Za-z_][\w:.-]*(?:\s+[A-Za-z_][\w:.-]*\s*=\s*(?P<xml_quote>\\?["'])(?:(?!(?P=xml_quote)|<).)*(?P=xml_quote))*\s+xmlns(?::[A-Za-z_][\w.-]*)?\s*=\s*\\?["']$''',
        statement,
    ):
        return "xml-namespace"
    if suffix == ".cs" and re.search(
        r'''\[\s*assembly\s*:\s*(?:System\.Reflection\.)?Assembly(?:File|Informational)?Version(?:Attribute)?\s*\(\s*["']$''',
        statement,
    ):
        return "assembly-version"
    if suffix == ".cs" and re.search(
        r'''\[\s*(?:System\.Runtime\.CompilerServices\.)?TypeForwardedFrom(?:Attribute)?\s*\(\s*"[A-Za-z_][\w.]*,\s*Version=$''',
        statement,
    ) and re.match(r'''\d+\.\d+\.\d+\.\d+,\s*Culture=[A-Za-z_-]+,\s*PublicKeyToken=[a-fA-F0-9]+"\s*\)\s*\]''', code[start:]):
        return "type-forwarded-assembly-version"
    return None


def _python_field_label_spans(code: str) -> list[tuple[int, int, str]]:
    """Only locally proved exception/validator field arguments.

    Parsing text does not import/evaluate it. Unknown syntax, receivers, rebinding
    or field uses remain candidates. The caller disables this across the entire
    source set if any network signal is present; no hostname is whitelisted.
    """
    try:
        tree = ast.parse(code)
    except (SyntaxError, ValueError, RecursionError, MemoryError):
        return []
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    builtin_errors = {"Exception", "ValueError", "TypeError", "KeyError", "RuntimeError", "AssertionError"}
    error_fields = {}
    rebound = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            rebound.add(node.id)
        elif isinstance(node, ast.arg):
            rebound.add(node.arg)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            rebound.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, (ast.Store, ast.Del)):
            target = node
            while isinstance(target, ast.Attribute):
                rebound.add(target.attr)
                target = target.value
            if isinstance(target, ast.Name):
                rebound.add(target.id)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"setattr", "delattr", "globals", "locals", "vars", "eval", "exec", "__import__"}:
            return []  # Dynamic namespace/class mutation has no local binding proof.
    if rebound & {"__class__", "__dict__"}:
        return []
    definitions = Counter(node.name for node in ast.walk(tree) if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)))
    trusted_builtin_errors = builtin_errors - rebound - set(definitions)
    trusted_super = "super" not in rebound and "super" not in definitions
    for node in tree.body:
        if (not isinstance(node, ast.ClassDef) or node.name in rebound or definitions[node.name] != 1
                or node.decorator_list or node.keywords or len(node.bases) != 1
                or not isinstance(node.bases[0], ast.Name) or node.bases[0].id not in trusted_builtin_errors):
            continue
        methods = [item for item in node.body if isinstance(item, ast.FunctionDef)]
        if any(item.decorator_list or (item.name.startswith("__") and item.name.endswith("__") and item.name != "__init__") for item in methods):
            continue
        if any(not isinstance(item, (ast.FunctionDef, ast.Pass)) and not (
                isinstance(item, ast.Expr) and isinstance(item.value, ast.Constant) and isinstance(item.value.value, str)) for item in node.body):
            continue
        calls = [item for item in ast.walk(node) if isinstance(item, ast.Call)]
        def safe_call(call):
            return trusted_super and ((isinstance(call.func, ast.Name) and call.func.id == "super" and not call.args and not call.keywords) or (
                isinstance(call.func, ast.Attribute) and call.func.attr == "__init__"
                and isinstance(call.func.value, ast.Call) and isinstance(call.func.value.func, ast.Name)
                and call.func.value.func.id == "super" and not call.func.value.args and not call.func.value.keywords))
        if not all(safe_call(call) for call in calls):
            continue
        initializer = next((item for item in methods if item.name == "__init__"), None)
        if initializer and not initializer.args.vararg and not initializer.args.kwarg:
            parameters = {argument.arg for argument in initializer.args.args}
            def simple_value(value):
                return isinstance(value, ast.Constant) or isinstance(value, ast.Name) and value.id in parameters
            def simple_initializer(statement):
                if isinstance(statement, ast.Pass):
                    return True
                if isinstance(statement, ast.Expr):
                    value = statement.value
                    return isinstance(value, ast.Constant) and isinstance(value.value, str) or (
                        isinstance(value, ast.Call) and safe_call(value) and not value.keywords and all(simple_value(arg) for arg in value.args))
                return (isinstance(statement, ast.Assign) and len(statement.targets) == 1
                    and isinstance(statement.targets[0], ast.Attribute) and isinstance(statement.targets[0].value, ast.Name)
                    and statement.targets[0].value.id == "self" and not statement.targets[0].attr.startswith("__") and simple_value(statement.value))
            if not all(simple_initializer(statement) for statement in initializer.body):
                continue
            names = [arg.arg for arg in initializer.args.args][1:]
            error_fields[node.name] = {index for index, name in enumerate(names) if name in {"field", "field_path", "field_name"}}
    error_names = trusted_builtin_errors | set(error_fields)
    validators = {}
    for function in tree.body:
        if (not isinstance(function, ast.FunctionDef) or function.name in rebound or definitions[function.name] != 1
                or function.decorator_list or function.args.vararg or function.args.kwarg):
            continue
        fields = {}
        for index, argument in enumerate(function.args.args):
            if argument.arg not in {"field", "field_path", "field_name"}:
                continue
            uses = [item for item in ast.walk(function) if isinstance(item, ast.Name) and item.id == argument.arg]
            valid = bool(uses)
            for use in uses:
                if not isinstance(use.ctx, ast.Load):
                    valid = False
                    break
                parent = parents.get(use)
                if (not isinstance(parent, ast.Call) or not isinstance(parent.func, ast.Name)
                        or parent.func.id not in error_names or not isinstance(parents.get(parent), ast.Raise)):
                    valid = False
                    break
                if parent.func.id in error_fields and not any(parent.args[position] is use for position in error_fields[parent.func.id] if position < len(parent.args)):
                    valid = False
                    break
            if valid:
                fields[index] = argument.arg
        if fields:
            validators[function.name] = fields
    lines = code.splitlines(keepends=True)
    offsets, offset = [], 0
    for line in lines:
        offsets.append(offset)
        offset += len(line)
    spans = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str) or not re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+", node.value):
            continue
        parent = parents.get(node)
        label = False
        if isinstance(parent, ast.Call) and isinstance(parent.func, ast.Name):
            allowed = validators.get(parent.func.id, error_fields.get(parent.func.id, {}))
            label = any(position < len(parent.args) and parent.args[position] is node for position in allowed)
            label = label or any(keyword.value is node and keyword.arg in set(validators.get(parent.func.id, {}).values()) for keyword in parent.keywords)
        if label:
            begin = offsets[node.lineno - 1] + len(lines[node.lineno - 1].encode("utf-8")[:node.col_offset].decode("utf-8"))
            end = offsets[node.end_lineno - 1] + len(lines[node.end_lineno - 1].encode("utf-8")[:node.end_col_offset].decode("utf-8"))
            spans.append((begin, end, "declared-field-label"))
    return spans



def strip_comments(text: str, suffix: str) -> tuple[str, list[str]]:
    """Small lexer preserving strings/newlines; unsupported constructs stay uncertain."""
    hash_comments = suffix in {".py", ".rb", ".ps1", ".psm1"}
    c_comments = suffix in {".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".cs", ".go"}
    limitations = []
    if suffix in {".ps1", ".psm1"} and re.search(r"""@['"]|['"]@""", text):
        limitations.append("powershell_here_string_requires_review")
    if suffix == ".rb" and re.search(r"<<[-~]?|^=begin", text, re.M):
        limitations.append("ruby_heredoc_or_block_comment_requires_review")
    if suffix in {".cpp", ".cc", ".cxx", ".hpp"} and 'R"' in text:
        limitations.append("cpp_raw_string_requires_review")
    out = []
    i = 0
    while i < len(text):
        start = i
        if suffix in {".ps1", ".psm1"} and text.startswith("<#", i):
            end = text.find("#>", i + 2)
            if end < 0:
                limitations.append("unterminated_comment")
                end = len(text) - 2
            i = end + 2
            out.append(re.sub(r"[^\n]", " ", text[start:i]))
        elif c_comments and text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end < 0:
                limitations.append("unterminated_comment")
                end = len(text) - 2
            i = end + 2
            out.append(re.sub(r"[^\n]", " ", text[start:i]))
        elif (hash_comments and text[i] == "#") or (c_comments and text.startswith("//", i)):
            end = text.find("\n", i)
            i = end if end >= 0 else len(text)
            out.append(" " * (i - start))
        elif text[i] in "'\"" or (suffix == ".go" and text[i] == chr(96)):
            quote = text[i]
            verbatim = suffix == ".cs" and quote == '"' and i > 0 and text[i - 1] == "@"
            token = quote * 3 if suffix == ".py" and text.startswith(quote * 3, i) else quote
            i += len(token)
            closed = False
            while i < len(text):
                if (text[i] == "\\" and quote != chr(96) and not verbatim and suffix not in {".ps1", ".psm1"}) or (text[i] == chr(96) and suffix in {".ps1", ".psm1"} and quote == '"'):
                    i += 2
                elif text.startswith(token, i):
                    # C# verbatim and PowerShell single quoted strings may double quotes.
                    if len(token) == 1 and text.startswith(quote * 2, i) and suffix in {".cs", ".ps1", ".psm1"}:
                        i += 2
                    else:
                        i += len(token)
                        closed = True
                        break
                else:
                    i += 1
            if not closed:
                limitations.append("unterminated_or_unsupported_string")
            out.append(text[start:i])
        else:
            out.append(text[i])
            i += 1
    return "".join(out), sorted(set(limitations))


def address_scope(value: str) -> str:
    value = value.strip("[]").lower()
    if value == "localhost":
        return "loopback"
    try:
        addr = ipaddress.ip_address(value)
    except ValueError:
        return "invalid-ip" if re.fullmatch(r"[\d.]+", value) else "hostname"
    if addr.is_unspecified:
        return "wildcard"
    if addr.is_loopback:
        return "loopback"
    if addr.version == 4 and any(addr in network for network in PRIVATE_V4):
        return "private"
    if addr.version == 6 and addr in PRIVATE_V6:
        return "private"
    if addr.is_global:
        return "public"
    return "special"  # documentation, link-local, multicast, reserved: still need review


def detect_high_confidence_real_credential(code: str) -> list[dict[str, Any]]:
    """Report credential material that is very unlikely to be a placeholder.

    Findings carry line, kind and a redacted excerpt only. Reports keep clues and
    positions rather than copying source, and a credential is
    the one token that must never be written into an output file even if it is later
    judged synthetic: the excerpt is truncated to a non-reconstructable prefix.
    """
    findings = []
    for kind, pattern in CREDENTIAL_PATTERNS.items():
        for match in pattern.finditer(code):
            text = match.group()
            if kind == "url_with_password":
                password = text.rsplit(":", 1)[1].split("@", 1)[0]
                if CREDENTIAL_PLACEHOLDERS.match(password):
                    continue
                excerpt = text.split(":", 2)[0] + "://<redacted>@"
            elif kind == "private_key_block":
                excerpt = "-----BEGIN PRIVATE KEY-----"
            else:
                prefix = text[:4]
                excerpt = prefix + "*" * max(len(text) - len(prefix), 3)
            findings.append({"kind": kind, "line": code.count("\n", 0, match.start()) + 1,
                             "excerpt": excerpt, "length": len(text)})
    return sorted(findings, key=lambda item: (item["line"], item["kind"]))


@dataclass
class SafetyClassification:
    task_id: str
    direction: str
    case_id: str
    classification: str
    reason: str
    details: dict[str, Any]
    executable: bool = False  # Deprecated but kept for compatibility
    admission_status: str = "BLOCKED"  # "ALLOWED" or "BLOCKED"
    blocking_reason: str | None = None  # "input_error" | "public_network_unverified" | "real_credential_suspected"
    requires_network_isolation: bool = False
    requires_synthetic_data: bool = False


class SafetyClassifierV2:
    """Static tiered admission; no execution, HTTP access, or import of samples."""

    def __init__(self, batch_network_isolation_configured: bool = False):
        """
        Args:
            batch_network_isolation_configured: Whether network isolation is configured
                at batch level (blocking public network access). When True, tasks with
                public network targets are ALLOWED; when False, they are BLOCKED.
        """
        self.batch_network_isolation_configured = batch_network_isolation_configured

    def is_loopback(self, target: str) -> bool:
        return address_scope(target) == "loopback"

    def is_private_ip(self, target: str) -> bool:
        return address_scope(target) == "private"

    def analyze_behavior(self, source_code: str, file_path: str, language_hint: str = "", *,
                         source_set_has_network: bool = False) -> dict[str, Any]:
        suffix = Path(file_path).suffix.lower()
        if suffix in {".text", ".txt"} and language_hint == "powershell":
            suffix = ".ps1"  # Declared batch direction; record the basis below.
        code, limitations = strip_comments(source_code, suffix)
        if suffix not in SOURCE_EXTENSIONS:
            limitations.append("unsupported_extension")
        signals = {name: sorted({code.count("\n", 0, m.start()) + 1
                                 for m in pattern.finditer(code)})
                   for name, pattern in COMPILED.items()}
        targets = {}
        excluded_literals = []
        metadata_spans: list[tuple[int, int, str]] = _python_field_label_spans(code) if suffix == ".py" and not signals["network"] and not source_set_has_network else []
        for pattern in (URL, IPV4, QUOTED_HOST):
            for match in pattern.finditer(code):
                value = match.group(1) if pattern is not IPV4 else match.group()
                if pattern is URL:
                    value = url_host(value)
                    value = value.split("]", 1)[0] + "]" if value.startswith("[") else value.split(":", 1)[0]
                line = code.count("\n", 0, match.start()) + 1
                # Failure to parse an IP does not rule out hostname:port/service.
                # Keep ambiguous single-colon candidates on the legacy hostname
                # path; punctuation and unambiguous malformed IPs are not hosts.
                if pattern is QUOTED_HOST and ":" in value:
                    try:
                        ipaddress.ip_address(value.strip("[]"))
                    except ValueError:
                        if not re.fullmatch(r"[A-Za-z0-9]+:[A-Za-z0-9]+", value):
                            excluded_literals.append({"value": value, "line": line, "reason": "not-an-ip-address"})
                            continue
                literal_start = match.start(1) if pattern is QUOTED_HOST else match.start()
                metadata_reason = next((reason for begin, end, reason in metadata_spans
                                        if begin <= match.start() and match.end() <= end), None)
                if metadata_reason is None and not signals["network"] and not source_set_has_network:
                    metadata_reason = _metadata_literal_reason(code, literal_start, suffix)
                if metadata_reason:
                    excluded_literals.append({"value": value, "line": line, "reason": metadata_reason})
                    metadata_spans.append((match.start(), match.end(), metadata_reason))
                    continue
                # Do not confuse numeric version fragments or empty string with a hostname.
                if pattern is QUOTED_HOST and ":" not in value and "." not in value and value.lower() != "localhost":
                    continue
                if pattern is QUOTED_HOST and address_scope(value) == "hostname":
                    line_start = code.rfind("\n", 0, match.start()) + 1
                    line_end = code.find("\n", match.end())
                    context = code[line_start:line_end if line_end >= 0 else len(code)]
                    strong_network = bool(COMPILED["network"].search(context))
                    # A bare filename literal is a path, not a DNS target. Only
                    # promote it to a network target when the line also shows a
                    # real network API — otherwise a nearby word such as the
                    # variable name `target` in `target := filepath.Join(root,
                    # "demo.txt")` must not make demo.txt a network target.
                    if _looks_like_filename(value) and not strong_network:
                        continue
                    if not (strong_network or re.search(
                            r"\b(?:host|hostname|server|endpoint|url|uri|destination|target)\b", context, re.I)):
                        continue  # e.g. open("result.txt") is not a DNS target
                targets[(line, value)] = {"value": value, "line": line, "scope": address_scope(value),
                                          "provenance": "literal", "redirectVerified": False}
        scopes = sorted({target["scope"] for target in targets.values()})
        has_network = bool(signals["network"] or targets)
        mode = "mixed" if len(scopes) > 1 else (scopes[0] if scopes else ("unresolved" if has_network else "none-detected"))
        credentials = detect_high_confidence_real_credential(code)
        return {"signals": signals, "network_mode": mode,
                "network_targets": list(targets.values()), "limitations": limitations,
                "excluded_network_literals": excluded_literals,
                "credentialFindings": credentials,
                "has_high_confidence_credential": bool(credentials),
                "has_network": has_network, "has_file_ops": bool(signals["filesystem"]),
                "has_process_exec": bool(signals["process"]),
                "msf_dependent": bool(signals["framework"]),
                "languageBasis": "direction:powershell" if Path(file_path).suffix.lower() in {".text", ".txt"} and suffix == ".ps1" else "extension"}

    def classify(self, task_id: str, direction: str, case_id: str, source_path: str) -> SafetyClassification:
        return self.classify_files(task_id, direction, case_id, [Path(source_path)])

    def classify_files(self, task_id: str, direction: str, case_id: str,
                       source_paths: list[Path], expected_hashes: dict[Path, str] | None = None) -> SafetyClassification:
        files, errors = [], []
        analyzed_sources = []
        expected_hashes = expected_hashes or {}
        if not source_paths:
            errors.append("missing_source")
        if len(source_paths) > MAX_FILES:
            errors.append("file_count_limit")
            source_paths = []
        for path in source_paths:
            try:
                if any(p.is_symlink() or getattr(p, "is_junction", lambda: False)() for p in (path, *path.parents)):
                    raise ValueError("linked_path")
                with path.open("rb") as stream:
                    raw = stream.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    raise ValueError("file_size_limit")
                digest = hashlib.sha256(raw).hexdigest()
                expected = expected_hashes.get(path)
                if expected and digest.lower() != expected.lower().removeprefix("sha256:"):
                    raise ValueError("source_hash_mismatch")
                text = raw.decode("utf-8-sig")  # Do not silently discard undecodable bytes.
                if "\x00" in text:
                    raise ValueError("binary_or_unsupported_encoding")
                files.append({"name": path.name, "sha256": digest,
                              **self.analyze_behavior(text, str(path), direction.split("-to-", 1)[0])})
                analyzed_sources.append((files[-1], text, str(path)))
            except (OSError, UnicodeError, ValueError) as exc:
                errors.append({"file": path.name, "type": type(exc).__name__,
                               "reason": str(exc) if isinstance(exc, ValueError) and not isinstance(exc, UnicodeError) else "unreadable_or_missing_source"})
        # Metadata may be consumed by a network API in another submitted file.
        # Reuse the validated text, independent of input order; retain filename
        # and malformed-address exclusions rather than promoting every literal.
        if any(file["signals"]["network"] for file in files):
            for file, text, file_path in analyzed_sources:
                if any(entry["reason"] in {"xml-namespace", "assembly-version", "type-forwarded-assembly-version", "declared-field-label"}
                       for entry in file["excluded_network_literals"]):
                    file.update(self.analyze_behavior(
                        text, file_path, direction.split("-to-", 1)[0], source_set_has_network=True))
        groups = sorted({name for file in files for name, lines in file["signals"].items() if lines})
        if any(file["has_network"] for file in files) and "network" not in groups:
            groups.append("network")
        if errors:
            cls, reason = "BLOCKED_INPUT", "source_incomplete_or_invalid"
        elif "framework" in groups:
            cls, reason = "REVIEW_DEPENDENCY", "framework_dependency_requires_environment"
        elif any(file["limitations"] for file in files):
            cls, reason = "REVIEW_UNCERTAIN", "lexical_coverage_incomplete"
        elif "sensitive" in groups or "dynamic_code" in groups:
            cls, reason = "REVIEW_SENSITIVE", "sensitive_or_dynamic_operations"
        elif "network" in groups:
            cls, reason = "REVIEW_NETWORK", "network_scope_and_inputs_require_review"
        elif "process" in groups or "filesystem" in groups or "discovery" in groups:
            cls, reason = "REVIEW_SIDE_EFFECTS", "local_effects_require_review"
        else:
            cls, reason = "LOW_SIGNAL", "no_known_signal_detected_not_proven_safe"

        # Determine admission status based on the highest-risk blocking policy.
        admission_status, blocking_reason, requires_network_isolation, requires_synthetic_data = self._determine_admission(
            cls, groups, files, errors
        )

        return SafetyClassification(
            task_id, direction, case_id, cls, reason,
            {
                "classifierVersion": VERSION,
                "reviewGroups": sorted(groups),
                "files": files,
                "inputErrors": errors,
                "analysisScope": "source-text-only",
                "executionApproved": admission_status == "ALLOWED",  # Derived from admission_status
                "admissionStatus": admission_status,
                "blockingReason": blocking_reason,
                "requiresNetworkIsolation": requires_network_isolation,
                "requiresSyntheticData": requires_synthetic_data,
                "limitations": [
                    "lexical_heuristics_not_dataflow",
                    "target_driver_dependencies_not_assessed",
                    "isolation_and_authorization_not_assessed"
                ]
            },
            executable=False,  # Deprecated, always False for compatibility
            admission_status=admission_status,
            blocking_reason=blocking_reason,
            requires_network_isolation=requires_network_isolation,
            requires_synthetic_data=requires_synthetic_data
        )

    def _determine_admission(
        self,
        classification: str,
        groups: list[str],
        files: list[dict],
        errors: list
    ) -> tuple[str, str | None, bool, bool]:
        """Determine admission status based on tiered policy.

        Returns: (admission_status, blocking_reason, requires_network_isolation, requires_synthetic_data)
        """
        # Rule 1: Input errors → BLOCKED
        if errors:
            return "BLOCKED", "input_error", False, False

        # Check network targets
        has_public_network = False
        has_private_network = False
        network_scopes = set()

        for file in files:
            for target in file.get("network_targets", []):
                scope = target.get("scope", "")
                network_scopes.add(scope)
                if scope in ("public", "hostname"):
                    has_public_network = True
                elif scope == "private":
                    has_private_network = True

        # Rule 2: Public network targets without batch isolation → BLOCKED
        if has_public_network and not self.batch_network_isolation_configured:
            return "BLOCKED", "public_network_unverified", True, False

        # Rule 3: High-confidence real credential material → BLOCKED pending human review.
        # Only credential *formats*; a bare "password"/"key"/"token"
        # keyword with a placeholder value must stay ALLOWED.
        credential_findings = [finding
                               for file in files
                               for finding in file.get("credentialFindings", [])]
        if credential_findings:
            return "BLOCKED", "real_credential_suspected", has_public_network or has_private_network, True

        # Default: ALLOWED (with context flags)
        requires_network_isolation = has_public_network or has_private_network
        requires_synthetic_data = "sensitive" in groups or "dynamic_code" in groups

        return "ALLOWED", None, requires_network_isolation, requires_synthetic_data


def checked_path(path: Path, root: Path) -> Path:
    if any(p.is_symlink() or getattr(p, "is_junction", lambda: False)() for p in (path, *path.parents)):
        raise ValueError("linked_path")
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("path_outside_source_base")
    return resolved


def manifest_roots(input_json: Path, source_base: Path) -> tuple[Path, ...]:
    """Ordered containment roots a manifest path may legitimately resolve inside.

    Input admission blocks a task only for a real integrity failure. A path that
    simply uses a different base directory is not one, so both readings are tried:
    the manifest's own directory first (the documented `../<direction>/<case>/source`
    style), then the declared source base (root-relative style). `source_base` is
    always present, so no manifest can widen its own read scope.
    """
    # Both roots must be fully resolved: checked_path compares an already-resolved
    # candidate against them, so a symlinked or `..`-bearing root would silently
    # reject every legitimate path.
    roots = [input_json.parent.resolve(), source_base.resolve()]
    ordered = []
    for root in roots:
        if root not in ordered:
            ordered.append(root)
    return tuple(ordered)


def resolve_declared(value: str, manifest_dir: Path, roots: tuple[Path, ...]) -> Path:
    """Resolve one declared manifest path against the first root that contains it.

    The value is always interpreted relative to the manifest that declares it (that
    is the documented convention). Each containment root is then tried in order, so
    both `case-1/source/...` and `../<direction>/<case>/source` resolve, while a path
    that escapes every root is still rejected.
    """
    candidate = Path(value)
    absolute = candidate if candidate.is_absolute() else manifest_dir / candidate
    failures = []
    for root in roots:
        try:
            return checked_path(absolute, root)
        except (OSError, ValueError) as exc:
            failures.append(exc)
    raise failures[0]


def task_sources(item: dict, input_json: Path, source_base: Path) -> tuple[list[Path], dict[Path, str]]:
    roots = manifest_roots(input_json, source_base)
    manifest_dir = roots[0]
    expected = {}
    if item.get("sourcePath"):
        path = resolve_declared(item["sourcePath"], manifest_dir, roots)
        folder = path.parent
        declared = [path]
        if item.get("sourceSha256"):
            expected[path] = item["sourceSha256"]
    else:
        if item.get("sourceDir"):
            folder = resolve_declared(item["sourceDir"], manifest_dir, roots)
        else:
            folder = resolve_declared(str(Path(str(item.get("direction", item.get("dir", "")))) /
                                            str(item.get("caseId", item.get("case", ""))) / "source"),
                                      manifest_dir, roots)
        declared = []
        for entry in item.get("sourceFiles", []):
            path = checked_path(folder / entry["name"], folder)
            declared.append(path)
            if entry.get("sha256"):
                expected[path] = entry["sha256"]
    # Review all files, including unsupported companion files. Missing declared
    # files are retained so each affected task produces BLOCKED_INPUT.
    discovered = []
    if folder.is_dir():
        for candidate in folder.rglob("*"):
            try:
                checked = checked_path(candidate, folder)
            except ValueError:
                continue  # a link inside the case is not a declared source
            if checked.is_file():
                discovered.append(checked)
                if len(discovered) > MAX_FILES:
                    raise ValueError("file_count_limit")
    return sorted(set(declared + discovered), key=str), expected


def reclassify_batch(input_json: Path, output_json: Path, source_base: Path,
                     batch_network_isolation_configured: bool = False) -> list[dict]:
    source_base = source_base.resolve()
    raw_input = input_json.read_bytes()
    data = json.loads(raw_input.decode("utf-8-sig"))
    tasks = data.get("tasks") if isinstance(data, dict) else data
    if not isinstance(tasks, list):
        raise ValueError("input must be a task list or batch object with tasks")
    if isinstance(data, dict) and data.get("taskCount", len(tasks)) != len(tasks):
        raise ValueError("taskCount mismatch")
    ids = [str(item.get("taskId", item.get("id", ""))) for item in tasks if isinstance(item, dict)]
    duplicates = {task_id for task_id, count in Counter(ids).items() if count > 1}
    classifier = SafetyClassifierV2(batch_network_isolation_configured=batch_network_isolation_configured)
    classifier_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    rows = []
    for index, item in enumerate(tasks):
        item = item if isinstance(item, dict) else {}
        task_id = str(item.get("taskId", item.get("id", "")))
        direction = str(item.get("direction", item.get("dir", "")))
        case_id = str(item.get("caseId", item.get("case", "")))
        if not case_id and item.get("casePath"):
            case_id = Path(item["casePath"]).parent.name
        try:
            if not task_id or task_id in duplicates or not direction:
                raise ValueError("missing_or_duplicate_task_identity")
            paths, expected = task_sources(item, input_json, source_base)
            result = classifier.classify_files(task_id, direction, case_id, paths, expected)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            result = SafetyClassification(
                task_id, direction, case_id, "BLOCKED_INPUT",
                "invalid_task_input",
                {
                    "inputErrors": [type(exc).__name__ + ":" + str(exc)],
                    "executionApproved": False,
                    "admissionStatus": "BLOCKED",
                    "blockingReason": "input_error"
                },
                executable=False,
                admission_status="BLOCKED",
                blocking_reason="input_error"
            )
        rows.append({
            "id": task_id or f"invalid-row-{index}",
            "dir": direction,
            "case": case_id,
            "cls": result.classification,
            "reason": result.reason,
            "details": result.details,
            "executable": False,
            "executionApproved": result.details.get("executionApproved", False),
            "admissionStatus": result.admission_status,
            "blockingReason": result.blocking_reason,
            "requiresNetworkIsolation": result.requires_network_isolation,
            "requiresSyntheticData": result.requires_synthetic_data,
            "classifierVersion": VERSION,
            "classifierSha256": classifier_hash,
            "inputManifestSha256": hashlib.sha256(raw_input).hexdigest(),
            "old_cls": item.get("cls"),
            "old_reason": item.get("reason")
        })
    output_json.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive create protects input, frozen source and historical classification files.
    with output_json.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(rows, stream, ensure_ascii=False, indent=2)
        stream.write("\n")

    allowed_count = sum(1 for row in rows if row["admissionStatus"] == "ALLOWED")
    blocked_count = sum(1 for row in rows if row["admissionStatus"] == "BLOCKED")

    print(json.dumps({
        "input": str(input_json),
        "total": len(rows),
        "classes": dict(Counter(row["cls"] for row in rows)),
        "admissionSummary": {
            "allowed": allowed_count,
            "blocked": blocked_count,
            "allowedRate": f"{allowed_count / len(rows) * 100:.1f}%" if rows else "0%",
            "byBlockingReason": dict(Counter(row["blockingReason"] for row in rows
                                             if row["admissionStatus"] == "BLOCKED"))
        },
        "networkIsolationConfigured": batch_network_isolation_configured,
        "executable": 0,  # Deprecated, always 0
        "output": str(output_json)
    }, ensure_ascii=False))
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("source_base", type=Path)
    parser.add_argument(
        "--network-isolation-configured", action="store_true",
        help="Batch-level network isolation is configured, so public/hostname "
             "network targets are admission-eligible instead of blocked. Only pass this when "
             "the batch-authorization.json evidence exists; it is not verified here.")
    args = parser.parse_args()
    reclassify_batch(args.input_json, args.output_json, args.source_base,
                     batch_network_isolation_configured=args.network_isolation_configured)
