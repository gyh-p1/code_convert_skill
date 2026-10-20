"""In-memory persistence model. No registry, files, processes or host access.

The model stores inert labels, never commands. A boot event only returns labels.
Input is one JSON document on stdin; output is one JSON document on stdout.
This is an original synthetic conversion specimen, not an intrusion tool.
"""

from __future__ import annotations

import copy
import json
import sys
import unicodedata
from contextlib import contextmanager
from dataclasses import dataclass


TACTIC = "Persistence"
TACTIC_ID = "TA0003"
MAX_ENTRIES = 64
MAX_OPERATIONS = 128
MAX_INPUT = 65536


class ModelError(Exception):
    def __init__(self, code, field):
        super().__init__(code)
        self.code = code
        self.field = field

    def as_dict(self):
        return {"code": self.code, "field": self.field}


def require_object(value, field):
    if not isinstance(value, dict):
        raise ModelError("OBJECT_REQUIRED", field)
    return value


def require_list(value, field, maximum):
    if not isinstance(value, list):
        raise ModelError("LIST_REQUIRED", field)
    if len(value) > maximum:
        raise ModelError("LIMIT", field)
    return value


def require_text(value, field, maximum=80):
    if not isinstance(value, str):
        raise ModelError("TEXT_REQUIRED", field)
    if not value or len(value) > maximum:
        raise ModelError("TEXT_LENGTH", field)
    if any(ord(char) < 32 for char in value):
        raise ModelError("CONTROL_CHARACTER", field)
    return value


def require_integer(value, field, minimum=0, maximum=100000):
    if type(value) is not int:
        raise ModelError("INTEGER_REQUIRED", field)
    if not minimum <= value <= maximum:
        raise ModelError("INTEGER_RANGE", field)
    return value


def require_boolean(value, field):
    if type(value) is not bool:
        raise ModelError("BOOLEAN_REQUIRED", field)
    return value


def reject_unknown(value, permitted, field):
    unknown = sorted(set(value) - set(permitted))
    if unknown:
        raise ModelError("UNKNOWN_FIELD", field + "." + unknown[0])


def require_choice(value, choices, field):
    value = require_text(value, field)
    if value not in choices:
        raise ModelError("UNKNOWN_CHOICE", field)
    return value


def canonical_name(value):
    name = require_text(value, "name")
    normalized = unicodedata.normalize("NFC", name)
    if normalized.strip() != normalized:
        raise ModelError("SURROUNDING_SPACE", "name")
    if "/" in normalized or "\\" in normalized:
        raise ModelError("NOT_A_LABEL", "name")
    return normalized.casefold()


@dataclass
class StartupEntry:
    name: str
    label: str
    owner: str
    priority: int
    once: bool
    enabled: bool
    expires: int | None
    revision: int

    @classmethod
    def from_input(cls, value, revision):
        require_object(value, "entry")
        reject_unknown(
            value,
            {
                "name",
                "label",
                "owner",
                "priority",
                "once",
                "enabled",
                "expires",
            },
            "entry",
        )
        name = require_text(value.get("name"), "name")
        canonical_name(name)
        label = require_text(value.get("label"), "label")
        owner = require_text(value.get("owner", "lab-user"), "owner")
        priority = require_integer(value.get("priority", 0), "priority")
        once = require_boolean(value.get("once", False), "once")
        enabled = require_boolean(value.get("enabled", True), "enabled")
        expires = value.get("expires")
        if expires is not None:
            require_integer(expires, "expires")
        return cls(
            name=name,
            label=label,
            owner=owner,
            priority=priority,
            once=once,
            enabled=enabled,
            expires=expires,
            revision=revision,
        )

    def key(self):
        return canonical_name(self.name)

    def is_expired(self, tick):
        return self.expires is not None and tick >= self.expires

    def is_ready(self, tick):
        return self.enabled and not self.is_expired(tick)

    def as_dict(self):
        return {
            "name": self.name,
            "label": self.label,
            "owner": self.owner,
            "priority": self.priority,
            "once": self.once,
            "enabled": self.enabled,
            "expires": self.expires,
            "revision": self.revision,
        }


class PersistenceStore:
    def __init__(self):
        self.entries = {}
        self.revision = 0
        self.tick = 0
        self.boot_count = 0
        self.emissions = []
        self.events = []

    def snapshot(self):
        return copy.deepcopy(
            (
                self.entries,
                self.revision,
                self.tick,
                self.boot_count,
                self.emissions,
                self.events,
            )
        )

    def restore(self, snapshot):
        (
            self.entries,
            self.revision,
            self.tick,
            self.boot_count,
            self.emissions,
            self.events,
        ) = copy.deepcopy(snapshot)

    @contextmanager
    def transaction(self):
        snapshot = self.snapshot()
        try:
            yield self
            self.check_invariants()
        except Exception:
            self.restore(snapshot)
            raise

    def check_invariants(self):
        if len(self.entries) > MAX_ENTRIES:
            raise ModelError("CAPACITY", "entries")
        for key, entry in self.entries.items():
            if key != entry.key():
                raise ModelError("KEY_INVARIANT", "entries")
            if entry.revision > self.revision:
                raise ModelError("REVISION_INVARIANT", "entries")

    def record(self, action, name):
        self.events.append(
            {
                "action": action,
                "name": name,
                "tick": self.tick,
                "revision": self.revision,
            }
        )

    def locate(self, name):
        key = canonical_name(name)
        if key not in self.entries:
            raise ModelError("NOT_FOUND", "name")
        return key, self.entries[key]

    def check_expected_revision(self, expected):
        if expected is None:
            return
        require_integer(expected, "expected_revision")
        if expected != self.revision:
            raise ModelError("REVISION_CONFLICT", "expected_revision")

    def install(self, value, replace=False, expected=None):
        self.check_expected_revision(expected)
        require_boolean(replace, "replace")
        entry = StartupEntry.from_input(value, self.revision + 1)
        key = entry.key()
        if key in self.entries and not replace:
            raise ModelError("ALREADY_EXISTS", "name")
        if key not in self.entries and len(self.entries) >= MAX_ENTRIES:
            raise ModelError("CAPACITY", "entries")
        self.revision += 1
        self.entries[key] = entry
        self.record("install", entry.name)
        return {"installed": entry.name}

    def remove(self, name, missing_ok=False):
        require_boolean(missing_ok, "missing_ok")
        key = canonical_name(name)
        if key not in self.entries:
            if missing_ok:
                return {"removed": False}
            raise ModelError("NOT_FOUND", "name")
        entry = self.entries.pop(key)
        self.revision += 1
        self.record("remove", entry.name)
        return {"removed": True}

    def set_enabled(self, name, enabled):
        require_boolean(enabled, "enabled")
        key, entry = self.locate(name)
        self.revision += 1
        entry.enabled = enabled
        entry.revision = self.revision
        self.entries[key] = entry
        self.record("enable" if enabled else "disable", entry.name)
        return {"enabled": enabled}

    def advance(self, delta):
        require_integer(delta, "delta")
        new_tick = self.tick + delta
        require_integer(new_tick, "tick")
        self.tick = new_tick
        self.record("advance", "clock")
        return {"tick": self.tick}

    def ordered_entries(self):
        return sorted(
            self.entries.values(),
            key=lambda entry: (entry.priority, entry.key()),
        )

    def boot(self):
        self.boot_count += 1
        emitted = []
        consumed = []
        for entry in self.ordered_entries():
            if not entry.is_ready(self.tick):
                continue
            emission = {
                "boot": self.boot_count,
                "name": entry.name,
                "label": entry.label,
                "owner": entry.owner,
            }
            emitted.append(emission)
            self.emissions.append(emission)
            if entry.once:
                consumed.append(entry.key())
        for key in consumed:
            entry = self.entries.pop(key)
            self.revision += 1
            self.record("consume_once", entry.name)
        self.record("boot", "simulated-boot")
        return {"emitted": emitted}

    def expire(self):
        expired = []
        for entry in self.ordered_entries():
            if entry.is_expired(self.tick):
                expired.append(entry.key())
        names = []
        for key in expired:
            entry = self.entries.pop(key)
            names.append(entry.name)
            self.revision += 1
            self.record("expire", entry.name)
        return {"expired": names}

    def inspect(self, name):
        _, entry = self.locate(name)
        return {
            "entry": entry.as_dict(),
            "ready": entry.is_ready(self.tick),
        }

    def statistics(self):
        owners = {}
        ready = 0
        expired = 0
        once = 0
        disabled = 0
        for entry in self.entries.values():
            owners[entry.owner] = owners.get(entry.owner, 0) + 1
            ready += int(entry.is_ready(self.tick))
            expired += int(entry.is_expired(self.tick))
            once += int(entry.once)
            disabled += int(not entry.enabled)
        return {
            "total": len(self.entries),
            "ready": ready,
            "expired": expired,
            "once": once,
            "disabled": disabled,
            "owners": owners,
            "emitted": len(self.emissions),
            "remaining_capacity": MAX_ENTRIES - len(self.entries),
        }

    def export(self):
        return {
            "entries": [entry.as_dict() for entry in self.ordered_entries()],
            "revision": self.revision,
            "tick": self.tick,
            "boots": self.boot_count,
            "emissions": copy.deepcopy(self.emissions),
            "events": copy.deepcopy(self.events),
        }


OP_FIELDS = {
    "statistics": {"op"},
    "install": {"op", "entry", "replace", "expected_revision"},
    "remove": {"op", "name", "missing_ok"},
    "enable": {"op", "name", "enabled"},
    "advance": {"op", "delta"},
    "boot": {"op"},
    "expire": {"op"},
    "inspect": {"op", "name"},
    "transaction": {"op", "steps", "fail_after"},
}


def dispatch(store, operation, nested=False):
    operation = require_object(operation, "operation")
    kind = require_choice(operation.get("op"), OP_FIELDS, "op")
    reject_unknown(operation, OP_FIELDS[kind], "operation")
    if kind == "statistics":
        return store.statistics()
    if kind == "install":
        return store.install(
            operation.get("entry"),
            operation.get("replace", False),
            operation.get("expected_revision"),
        )
    if kind == "remove":
        return store.remove(
            operation.get("name"),
            operation.get("missing_ok", False),
        )
    if kind == "enable":
        return store.set_enabled(
            operation.get("name"),
            operation.get("enabled"),
        )
    if kind == "advance":
        return store.advance(operation.get("delta"))
    if kind == "boot":
        return store.boot()
    if kind == "expire":
        return store.expire()
    if kind == "inspect":
        return store.inspect(operation.get("name"))
    if nested:
        raise ModelError("NESTED_TRANSACTION", "op")
    steps = require_list(operation.get("steps"), "steps", 16)
    fail_after = operation.get("fail_after")
    if fail_after is not None:
        require_integer(fail_after, "fail_after", 1, len(steps))
    results = []
    with store.transaction():
        for index, step in enumerate(steps, 1):
            results.append(dispatch(store, step, nested=True))
            if index == fail_after:
                raise ModelError("INJECTED_FAILURE", "transaction")
    return {"committed": results}


def simulate(document):
    document = require_object(document, "input")
    reject_unknown(document, {"operations"}, "input")
    operations = require_list(
        document.get("operations"),
        "operations",
        MAX_OPERATIONS,
    )
    store = PersistenceStore()
    outcomes = []
    for index, operation in enumerate(operations):
        try:
            with store.transaction():
                result = dispatch(store, operation)
            outcomes.append(
                {"index": index, "ok": True, "result": result}
            )
        except ModelError as error:
            outcomes.append(
                {"index": index, "ok": False, "error": error.as_dict()}
            )
    return {
        "tactic": TACTIC,
        "tactic_id": TACTIC_ID,
        "simulation": True,
        "outcomes": outcomes,
        "state": store.export(),
    }


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ModelError("DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def reject_nonfinite(value):
    raise ModelError("NONFINITE_NUMBER", "input")


def read_document():
    raw = sys.stdin.buffer.read(MAX_INPUT + 1)
    if len(raw) > MAX_INPUT:
        raise ModelError("INPUT_TOO_LARGE", "input")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ModelError("INVALID_UTF8", "input") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_nonfinite,
        )
    except (json.JSONDecodeError, RecursionError) as error:
        raise ModelError("INVALID_JSON", "input") from error


def write_document(document):
    text = json.dumps(
        document,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))


def main():
    try:
        result = simulate(read_document())
    except ModelError as error:
        write_document({"error": error.as_dict(), "simulation": True})
        return 2
    write_document(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
