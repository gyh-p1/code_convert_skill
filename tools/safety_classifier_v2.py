#!/usr/bin/env python3
"""Static review triage, v2.4 with tiered admission policy (Spec 04).

Reads text only; implements "block only highest-risk" instead of "executable=False for all".
Classification determines ALLOWED vs BLOCKED based on VM isolation capabilities.

v2.4 change over v2.3:
  * Hostname heuristic no longer promotes a bare file-name literal (e.g.
    `"demo.txt"`) to a network target just because a weak context word such as
    the variable name `target` is on the same line. A QUOTED_HOST value that is
    a known file extension and has no real network API in context is treated as
    a path. Real hosts (with a network API like Dial/connect on the line) and
    hard-coded IPs are unaffected. Fixes dataset-2 D2-055 false positive.

v2.3 changes over v2.2, all required by docs/stages/stage1/specs/tiered-admission-policy.md:
  * Input paths are resolved against the manifest's own directory, not the repository
    root. v2.2 read batch.json `sourcePath`/`sourceDir` as root-relative, so every
    manifest written in the documented `../<direction>/<case>/source` style that did
    not coincide with `<source_base>/<direction>/...` became a false BLOCKED_INPUT.
  * Rule 3 (high-confidence real credential) is implemented; v2.2 shipped it as a
    placeholder comment and could never emit `real_credential_suspected`.
  * The batch-level network isolation switch is reachable from the CLI; v2.2 always
    passed False, so Spec 04 3.2 could not be cleared by configuration.
  * Lexical boundaries no longer fire on substrings of ordinary identifiers
    (`os.WriteFile` is not the Windows API, `translation-eval` is not dynamic eval).
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VERSION = "2.4"
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

# Spec 04 3.3: block only HIGH-CONFIDENCE real credential material. A keyword such as
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
# These extensions are file suffixes, never meaningful network hosts; a value
# ending in one is treated as a path, not a target, UNLESS the surrounding line
# shows a real network API (see analyze_behavior).
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
    """Spec 04 3.3: report credential material that is very unlikely to be a placeholder.

    Findings carry line, kind and a redacted excerpt only. Spec 01 4 requires that
    reports keep clues and positions rather than copying source, and a credential is
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
    """Compatibility name for v2.2 tiered admission; no execution/HTTP/import of samples."""

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

    def analyze_behavior(self, source_code: str, file_path: str, language_hint: str = "") -> dict[str, Any]:
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
        for pattern in (URL, IPV4, QUOTED_HOST):
            for match in pattern.finditer(code):
                value = match.group(1) if pattern is not IPV4 else match.group()
                if pattern is URL:
                    value = url_host(value)
                    value = value.split("]", 1)[0] + "]" if value.startswith("[") else value.split(":", 1)[0]
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
                line = code.count("\n", 0, match.start()) + 1
                targets[(line, value)] = {"value": value, "line": line, "scope": address_scope(value),
                                          "provenance": "literal", "redirectVerified": False}
        scopes = sorted({target["scope"] for target in targets.values()})
        has_network = bool(signals["network"] or targets)
        mode = "mixed" if len(scopes) > 1 else (scopes[0] if scopes else ("unresolved" if has_network else "none-detected"))
        credentials = detect_high_confidence_real_credential(code)
        return {"signals": signals, "network_mode": mode,
                "network_targets": list(targets.values()), "limitations": limitations,
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
            except (OSError, UnicodeError, ValueError) as exc:
                errors.append({"file": path.name, "type": type(exc).__name__,
                               "reason": str(exc) if isinstance(exc, ValueError) and not isinstance(exc, UnicodeError) else "unreadable_or_missing_source"})
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

        # Determine admission status based on tiered policy (Spec 04)
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
        # Spec 04 3.3: only credential *formats*; a bare "password"/"key"/"token"
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

    Spec 04 3.1 blocks a task only for a real input-integrity failure. A path that
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
        help="Spec 04 3.2: batch-level network isolation is configured, so public/hostname "
             "network targets are admission-eligible instead of blocked. Only pass this when "
             "the batch-authorization.json evidence exists; it is not verified here.")
    args = parser.parse_args()
    reclassify_batch(args.input_json, args.output_json, args.source_base,
                     batch_network_isolation_configured=args.network_isolation_configured)
