"""Virtual identity and scoped capability elevation over synthetic resources.

No operating-system identity is queried or changed. Tokens are model objects.
No commands, subprocesses, exploit primitives or real credentials are used.
The program consumes JSON on stdin and reports its virtual state as JSON.
"""

from __future__ import annotations

import copy
import json
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from enum import IntFlag


TACTIC = "Privilege Escalation"
TACTIC_ID = "TA0004"
MAX_INPUT = 65536
MAX_OPERATIONS = 128


class ModelError(Exception):
    def __init__(self, code, field):
        super().__init__(code)
        self.code = code
        self.field = field

    def as_dict(self):
        return {"code": self.code, "field": self.field}


def object_value(value, field):
    if not isinstance(value, dict):
        raise ModelError("OBJECT_REQUIRED", field)
    return value


def list_value(value, field, maximum=128):
    if not isinstance(value, list):
        raise ModelError("LIST_REQUIRED", field)
    if len(value) > maximum:
        raise ModelError("LIMIT", field)
    return value


def text_value(value, field):
    if not isinstance(value, str):
        raise ModelError("TEXT_REQUIRED", field)
    if not value or len(value) > 80:
        raise ModelError("TEXT_LENGTH", field)
    if any(ord(char) < 32 for char in value):
        raise ModelError("CONTROL_CHARACTER", field)
    return value


def integer_value(value, field, maximum=10000):
    if type(value) is not int:
        raise ModelError("INTEGER_REQUIRED", field)
    if value < 0 or value > maximum:
        raise ModelError("INTEGER_RANGE", field)
    return value


def boolean_value(value, field):
    if type(value) is not bool:
        raise ModelError("BOOLEAN_REQUIRED", field)
    return value


def fields(value, permitted, field):
    unknown = sorted(set(value) - set(permitted))
    if unknown:
        raise ModelError("UNKNOWN_FIELD", field + "." + unknown[0])


class Capability(IntFlag):
    READ = 1
    WRITE = 2
    DELEGATE = 4
    AUDIT = 8


CAPABILITY_NAMES = {
    "read": Capability.READ,
    "write": Capability.WRITE,
    "delegate": Capability.DELEGATE,
    "audit": Capability.AUDIT,
}


def parse_capabilities(value):
    values = list_value(value, "capabilities", 4)
    mask = Capability(0)
    seen = set()
    for name in values:
        name = text_value(name, "capability")
        if name not in CAPABILITY_NAMES:
            raise ModelError("UNKNOWN_CAPABILITY", "capability")
        if name in seen:
            raise ModelError("DUPLICATE_CAPABILITY", "capability")
        seen.add(name)
        mask |= CAPABILITY_NAMES[name]
    return mask


def capability_names(mask):
    return [
        name
        for name, value in CAPABILITY_NAMES.items()
        if mask & value
    ]


@dataclass(frozen=True)
class VirtualToken:
    name: str
    principal: str
    capabilities: Capability
    expires: int
    parent: str | None

    def as_dict(self):
        return {
            "name": self.name,
            "principal": self.principal,
            "capabilities": capability_names(self.capabilities),
            "expires": self.expires,
            "parent": self.parent,
        }


@dataclass
class VirtualResource:
    name: str
    value: str
    deny: Capability
    version: int = 0

    def as_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "deny": capability_names(self.deny),
            "version": self.version,
        }


class PrivilegeModel:
    def __init__(self, document):
        self.tick = 0
        self.current = "base"
        self.stack = []
        self.audit = []
        self.revoked = set()
        self.tokens = {}
        self.resources = {}
        principal = text_value(document.get("principal", "lab-user"), "principal")
        capabilities = parse_capabilities(document.get("base", ["read"]))
        self.tokens["base"] = VirtualToken(
            name="base",
            principal=principal,
            capabilities=capabilities,
            expires=10000,
            parent=None,
        )
        self.load_tokens(document.get("tokens", []))
        self.load_resources(document.get("resources", []))

    def load_tokens(self, values):
        for value in list_value(values, "tokens", 32):
            object_value(value, "token")
            fields(
                value,
                {"name", "principal", "capabilities", "expires"},
                "token",
            )
            name = text_value(value.get("name"), "name")
            if name in self.tokens:
                raise ModelError("DUPLICATE_TOKEN", "name")
            self.tokens[name] = VirtualToken(
                name=name,
                principal=text_value(value.get("principal", "lab-user"), "principal"),
                capabilities=parse_capabilities(value.get("capabilities", [])),
                expires=integer_value(value.get("expires", 10000), "expires"),
                parent=None,
            )

    def load_resources(self, values):
        for value in list_value(values, "resources", 32):
            object_value(value, "resource")
            fields(value, {"name", "value", "deny"}, "resource")
            name = text_value(value.get("name"), "name")
            if name in self.resources:
                raise ModelError("DUPLICATE_RESOURCE", "name")
            self.resources[name] = VirtualResource(
                name=name,
                value=text_value(value.get("value"), "value"),
                deny=parse_capabilities(value.get("deny", [])),
            )

    def record(self, action, detail):
        self.audit.append(
            {
                "action": action,
                "detail": detail,
                "identity": self.current,
                "tick": self.tick,
            }
        )

    def token(self, name):
        name = text_value(name, "token")
        if name not in self.tokens:
            raise ModelError("TOKEN_NOT_FOUND", "token")
        token = self.tokens[name]
        visited = set()
        cursor = token
        while cursor is not None:
            if cursor.name in visited:
                raise ModelError("TOKEN_CYCLE", "token")
            visited.add(cursor.name)
            if cursor.name in self.revoked:
                raise ModelError("TOKEN_REVOKED", "token")
            if self.tick >= cursor.expires:
                raise ModelError("TOKEN_EXPIRED", "token")
            cursor = self.tokens.get(cursor.parent)
        return token

    def resource(self, name):
        name = text_value(name, "resource")
        if name not in self.resources:
            raise ModelError("RESOURCE_NOT_FOUND", "resource")
        return self.resources[name]

    def authorize(self, resource, capability):
        token = self.token(self.current)
        if resource.deny & capability:
            raise ModelError("EXPLICIT_DENY", "resource")
        if (token.capabilities & capability) != capability:
            raise ModelError("ACCESS_DENIED", "capability")
        return token

    @contextmanager
    def impersonate(self, name):
        token = self.token(name)
        if len(self.stack) >= 4:
            raise ModelError("SCOPE_DEPTH", "token")
        previous = self.current
        self.stack.append(previous)
        self.current = token.name
        self.record("enter", token.name)
        try:
            yield token
        finally:
            self.record("leave", token.name)
            self.current = self.stack.pop()

    def read(self, name):
        resource = self.resource(name)
        self.authorize(resource, Capability.READ)
        self.record("read", resource.name)
        return {"value": resource.value, "version": resource.version}

    def write(self, name, value, expected):
        resource = self.resource(name)
        self.authorize(resource, Capability.WRITE)
        value = text_value(value, "value")
        if expected is not None:
            integer_value(expected, "expected")
            if expected != resource.version:
                raise ModelError("VERSION_CONFLICT", "expected")
        resource.value = value
        resource.version += 1
        self.record("write", resource.name)
        return {"version": resource.version}

    def delegate(self, operation):
        parent = self.token(self.current)
        if not parent.capabilities & Capability.DELEGATE:
            raise ModelError("DELEGATION_DENIED", "token")
        name = text_value(operation.get("name"), "name")
        if name in self.tokens:
            raise ModelError("DUPLICATE_TOKEN", "name")
        if len(self.tokens) >= 64:
            raise ModelError("TOKEN_LIMIT", "tokens")
        capabilities = parse_capabilities(operation.get("capabilities", []))
        if int(capabilities) & ~int(parent.capabilities):
            raise ModelError("CAPABILITY_AMPLIFICATION", "capabilities")
        expires = integer_value(operation.get("expires"), "expires")
        if expires <= self.tick or expires > parent.expires:
            raise ModelError("EXPIRY_AMPLIFICATION", "expires")
        self.tokens[name] = VirtualToken(
            name=name,
            principal=parent.principal,
            capabilities=capabilities,
            expires=expires,
            parent=parent.name,
        )
        self.record("delegate", name)
        return {"delegated": name}

    def revoke(self, name):
        token = self.token(name)
        current = self.token(self.current)
        if not current.capabilities & Capability.DELEGATE:
            raise ModelError("DELEGATION_DENIED", "token")
        if token.name == "base":
            raise ModelError("BASE_REVOCATION", "token")
        self.revoked.add(token.name)
        self.record("revoke", token.name)
        return {"revoked": token.name}

    def advance(self, delta):
        integer_value(delta, "delta")
        integer_value(self.tick + delta, "tick")
        self.tick += delta
        return {"tick": self.tick}

    def explain_access(self, name):
        resource = self.resource(name)
        token = self.token(self.current)
        decisions = []
        for capability, mask in CAPABILITY_NAMES.items():
            if resource.deny & mask:
                reason = "EXPLICIT_DENY"
                allowed = False
            elif token.capabilities & mask:
                reason = "GRANTED"
                allowed = True
            else:
                reason = "ACCESS_DENIED"
                allowed = False
            decisions.append(
                {
                    "capability": capability,
                    "allowed": allowed,
                    "reason": reason,
                }
            )
        return {
            "identity": token.name,
            "principal": token.principal,
            "resource": resource.name,
            "decisions": decisions,
        }

    def lineage(self, name):
        token = self.token(name)
        result = []
        while token is not None:
            result.append(token.name)
            token = self.tokens.get(token.parent)
        return {"lineage": result}

    def export(self):
        return {
            "identity": self.current,
            "scope_depth": len(self.stack),
            "tick": self.tick,
            "tokens": [self.tokens[key].as_dict() for key in sorted(self.tokens)],
            "resources": [
                self.resources[key].as_dict()
                for key in sorted(self.resources)
            ],
            "revoked": sorted(self.revoked),
            "audit": copy.deepcopy(self.audit),
        }


OP_FIELDS = {
    "explain": {"op", "resource"},
    "lineage": {"op", "token"},
    "read": {"op", "resource"},
    "write": {"op", "resource", "value", "expected"},
    "scope": {"op", "token", "steps", "fail_after"},
    "delegate": {"op", "name", "capabilities", "expires"},
    "revoke": {"op", "token"},
    "advance": {"op", "delta"},
    "identity": {"op"},
}


def dispatch(model, operation, depth=0):
    object_value(operation, "operation")
    kind = text_value(operation.get("op"), "op")
    if kind not in OP_FIELDS:
        raise ModelError("UNKNOWN_OPERATION", "op")
    fields(operation, OP_FIELDS[kind], "operation")
    if kind == "explain":
        return model.explain_access(operation.get("resource"))
    if kind == "lineage":
        return model.lineage(operation.get("token"))
    if kind == "identity":
        return {"identity": model.current}
    if kind == "read":
        return model.read(operation.get("resource"))
    if kind == "write":
        return model.write(
            operation.get("resource"),
            operation.get("value"),
            operation.get("expected"),
        )
    if kind == "delegate":
        return model.delegate(operation)
    if kind == "revoke":
        return model.revoke(operation.get("token"))
    if kind == "advance":
        return model.advance(operation.get("delta"))
    if depth >= 4:
        raise ModelError("SCOPE_DEPTH", "steps")
    steps = list_value(operation.get("steps"), "steps", 8)
    fail_after = operation.get("fail_after")
    if fail_after is not None:
        integer_value(fail_after, "fail_after", len(steps))
        if fail_after == 0:
            raise ModelError("INTEGER_RANGE", "fail_after")
    outcomes = []
    with model.impersonate(operation.get("token")):
        for index, step in enumerate(steps, 1):
            outcomes.append(dispatch(model, step, depth + 1))
            if index == fail_after:
                raise ModelError("INJECTED_FAILURE", "scope")
    return {"scope_results": outcomes}


def simulate(document):
    object_value(document, "input")
    fields(
        document,
        {"principal", "base", "tokens", "resources", "operations"},
        "input",
    )
    model = PrivilegeModel(document)
    operations = list_value(document.get("operations"), "operations")
    outcomes = []
    for index, operation in enumerate(operations):
        try:
            result = dispatch(model, operation)
            outcomes.append({"index": index, "ok": True, "result": result})
        except ModelError as error:
            outcomes.append(
                {"index": index, "ok": False, "error": error.as_dict()}
            )
    return {
        "tactic": TACTIC,
        "tactic_id": TACTIC_ID,
        "simulation": True,
        "outcomes": outcomes,
        "state": model.export(),
    }


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ModelError("DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def reject_constant(value):
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
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
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
