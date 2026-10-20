"""Discovery of a supplied fictional inventory, never of the executing host.

All hosts, accounts and services are input data. No sockets or OS probes exist.
Generator lifetime and exception cleanup are deliberate conversion subjects.
"""

from __future__ import annotations

import copy
import json
import sys
from contextlib import closing
from dataclasses import dataclass


TACTIC = "Discovery"
TACTIC_ID = "TA0007"
MAX_INPUT = 65536
MAX_HOSTS = 32
MAX_QUERIES = 32


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


def list_value(value, field, maximum):
    if not isinstance(value, list):
        raise ModelError("LIST_REQUIRED", field)
    if len(value) > maximum:
        raise ModelError("LIMIT", field)
    return value


def text_value(value, field, maximum=80):
    if not isinstance(value, str):
        raise ModelError("TEXT_REQUIRED", field)
    if not value or len(value) > maximum:
        raise ModelError("TEXT_LENGTH", field)
    if any(ord(char) < 32 for char in value):
        raise ModelError("CONTROL_CHARACTER", field)
    return value


def integer_value(value, field, minimum, maximum):
    if type(value) is not int:
        raise ModelError("INTEGER_REQUIRED", field)
    if not minimum <= value <= maximum:
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


def choice(value, choices, field):
    value = text_value(value, field)
    if value not in choices:
        raise ModelError("UNKNOWN_CHOICE", field)
    return value


def labels(value, field, maximum=16):
    values = list_value(value, field, maximum)
    result = []
    seen = set()
    for value in values:
        label = text_value(value, field)
        if label in seen:
            raise ModelError("DUPLICATE_LABEL", field)
        result.append(label)
        seen.add(label)
    return tuple(result)


@dataclass(frozen=True)
class Service:
    name: str
    port: int
    enabled: bool

    @classmethod
    def from_input(cls, value):
        object_value(value, "service")
        fields(value, {"name", "port", "enabled"}, "service")
        return cls(
            name=text_value(value.get("name"), "service.name"),
            port=integer_value(value.get("port"), "port", 1, 65535),
            enabled=boolean_value(value.get("enabled", True), "enabled"),
        )

    def as_dict(self):
        return {
            "name": self.name,
            "port": self.port,
            "enabled": self.enabled,
        }


@dataclass(frozen=True)
class Host:
    name: str
    system: str
    zone: str
    memory: int
    online: bool
    tags: tuple
    accounts: tuple
    services: tuple

    @classmethod
    def from_input(cls, value):
        object_value(value, "host")
        fields(
            value,
            {
                "name",
                "system",
                "zone",
                "memory",
                "online",
                "tags",
                "accounts",
                "services",
            },
            "host",
        )
        services = []
        seen = set()
        for raw in list_value(value.get("services", []), "services", 16):
            service = Service.from_input(raw)
            if service.name in seen:
                raise ModelError("DUPLICATE_SERVICE", "service.name")
            services.append(service)
            seen.add(service.name)
        return cls(
            name=text_value(value.get("name"), "host.name"),
            system=choice(
                value.get("system", "fictional"),
                {"fictional", "linux", "windows"},
                "system",
            ),
            zone=text_value(value.get("zone", "lab"), "zone"),
            memory=integer_value(value.get("memory", 0), "memory", 0, 1048576),
            online=boolean_value(value.get("online", True), "online"),
            tags=labels(value.get("tags", []), "tags"),
            accounts=labels(value.get("accounts", []), "accounts"),
            services=tuple(services),
        )

    def as_dict(self):
        return {
            "name": self.name,
            "system": self.system,
            "zone": self.zone,
            "memory": self.memory,
            "online": self.online,
            "tags": list(self.tags),
            "accounts": list(self.accounts),
            "services": [service.as_dict() for service in self.services],
        }


class Inventory:
    def __init__(self, values):
        self.hosts = {}
        self.links = {}
        self.open_cursors = 0
        self.closed_cursors = 0
        self.scanned = 0
        self.audit = []
        for value in list_value(values, "hosts", MAX_HOSTS):
            host = Host.from_input(value)
            if host.name in self.hosts:
                raise ModelError("DUPLICATE_HOST", "host.name")
            self.hosts[host.name] = host
            self.links[host.name] = set()

    def load_links(self, values):
        for value in list_value(values, "links", 64):
            object_value(value, "link")
            fields(value, {"from", "to"}, "link")
            source = self.find(value.get("from"))
            target = self.find(value.get("to"))
            if source.name == target.name:
                raise ModelError("SELF_LINK", "link")
            self.links[source.name].add(target.name)
            self.links[target.name].add(source.name)

    def find(self, name):
        name = text_value(name, "host")
        if name not in self.hosts:
            raise ModelError("HOST_NOT_FOUND", "host")
        return self.hosts[name]

    def walk_hosts(self):
        self.open_cursors += 1
        self.audit.append({"event": "open_cursor"})
        try:
            for name in sorted(self.hosts):
                self.scanned += 1
                yield self.hosts[name]
        finally:
            self.open_cursors -= 1
            self.closed_cursors += 1
            self.audit.append({"event": "close_cursor"})

    def neighbors(self, name):
        host = self.find(name)
        return sorted(self.links[host.name])

    def reachable(self, name, depth):
        root = self.find(name)
        integer_value(depth, "depth", 0, MAX_HOSTS)
        visited = {root.name}
        frontier = [root.name]
        result = [{"name": root.name, "distance": 0}]
        for distance in range(1, depth + 1):
            following = set()
            for current in frontier:
                following.update(self.links[current] - visited)
            frontier = sorted(following)
            if not frontier:
                break
            for current in frontier:
                visited.add(current)
                result.append({"name": current, "distance": distance})
        return result

    def statistics(self):
        systems = {}
        zones = {}
        enabled = 0
        accounts = set()
        total_memory = 0
        for host in self.hosts.values():
            systems[host.system] = systems.get(host.system, 0) + 1
            zones[host.zone] = zones.get(host.zone, 0) + 1
            enabled += sum(service.enabled for service in host.services)
            accounts.update(host.accounts)
            total_memory += host.memory
        return {
            "hosts": len(self.hosts),
            "systems": systems,
            "zones": zones,
            "enabled_services": enabled,
            "distinct_accounts": len(accounts),
            "memory": total_memory,
            "edges": sum(len(value) for value in self.links.values()) // 2,
        }

    def export(self):
        return {
            "hosts": [self.hosts[name].as_dict() for name in sorted(self.hosts)],
            "links": {name: sorted(self.links[name]) for name in sorted(self.links)},
            "open_cursors": self.open_cursors,
            "closed_cursors": self.closed_cursors,
            "scanned": self.scanned,
            "audit": copy.deepcopy(self.audit),
        }


@dataclass(frozen=True)
class Query:
    system: str | None
    zone: str | None
    tag: str | None
    online: bool | None
    minimum_memory: int
    limit: int
    fail_after: int | None
    projection: str

    @classmethod
    def from_input(cls, value):
        fields(
            value,
            {
                "op",
                "system",
                "zone",
                "tag",
                "online",
                "minimum_memory",
                "limit",
                "fail_after",
                "projection",
            },
            "query",
        )
        system = value.get("system")
        zone = value.get("zone")
        tag = value.get("tag")
        online = value.get("online")
        fail_after = value.get("fail_after")
        if system is not None:
            choice(system, {"fictional", "linux", "windows"}, "system")
        if zone is not None:
            text_value(zone, "zone")
        if tag is not None:
            text_value(tag, "tag")
        if online is not None:
            boolean_value(online, "online")
        if fail_after is not None:
            integer_value(fail_after, "fail_after", 1, MAX_HOSTS)
        return cls(
            system=system,
            zone=zone,
            tag=tag,
            online=online,
            minimum_memory=integer_value(
                value.get("minimum_memory", 0), "minimum_memory", 0, 1048576
            ),
            limit=integer_value(value.get("limit", MAX_HOSTS), "limit", 0, MAX_HOSTS),
            fail_after=fail_after,
            projection=choice(
                value.get("projection", "names"),
                {"names", "hosts", "services", "accounts"},
                "projection",
            ),
        )

    def accepts(self, host):
        if self.system is not None and host.system != self.system:
            return False
        if self.zone is not None and host.zone != self.zone:
            return False
        if self.tag is not None and self.tag not in host.tags:
            return False
        if self.online is not None and host.online != self.online:
            return False
        return host.memory >= self.minimum_memory

    def project(self, host):
        if self.projection == "names":
            return host.name
        if self.projection == "hosts":
            return host.as_dict()
        if self.projection == "services":
            return {
                "host": host.name,
                "services": [
                    service.as_dict()
                    for service in host.services
                    if service.enabled
                ],
            }
        return {"host": host.name, "accounts": sorted(host.accounts)}


class DiscoverySession:
    def __init__(self, inventory):
        self.inventory = inventory
        self.results = []

    def search(self, value):
        query = Query.from_input(value)
        rows = []
        examined = 0
        if query.limit == 0:
            return {"rows": [], "examined": 0}
        with closing(self.inventory.walk_hosts()) as cursor:
            for host in cursor:
                examined += 1
                if examined == query.fail_after:
                    raise ModelError("INJECTED_FAILURE", "cursor")
                if query.accepts(host):
                    rows.append(query.project(host))
                if len(rows) == query.limit:
                    break
        return {"rows": rows, "examined": examined}

    def dispatch(self, value):
        object_value(value, "query")
        operation = choice(
            value.get("op"),
            {"search", "inspect", "neighbors", "reachable", "statistics"},
            "op",
        )
        if operation == "search":
            return self.search(value)
        if operation == "statistics":
            fields(value, {"op"}, "query")
            return self.inventory.statistics()
        if operation == "reachable":
            fields(value, {"op", "host", "depth"}, "query")
            return {
                "reachable": self.inventory.reachable(
                    value.get("host"), value.get("depth", 1)
                )
            }
        fields(value, {"op", "host"}, "query")
        if operation == "neighbors":
            return {"neighbors": self.inventory.neighbors(value.get("host"))}
        return {"host": self.inventory.find(value.get("host")).as_dict()}

    def run(self, values):
        for index, value in enumerate(list_value(values, "queries", MAX_QUERIES)):
            try:
                result = self.dispatch(value)
                self.results.append({"index": index, "ok": True, "result": result})
            except ModelError as error:
                self.results.append(
                    {"index": index, "ok": False, "error": error.as_dict()}
                )

    def report(self):
        return {
            "tactic": TACTIC,
            "tactic_id": TACTIC_ID,
            "simulation": True,
            "outcomes": copy.deepcopy(self.results),
            "state": self.inventory.export(),
        }


def simulate(document):
    object_value(document, "input")
    fields(document, {"hosts", "links", "queries"}, "input")
    inventory = Inventory(document.get("hosts", []))
    inventory.load_links(document.get("links", []))
    session = DiscoverySession(inventory)
    session.run(document.get("queries"))
    return session.report()


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
