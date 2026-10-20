"""Inert text transformation model for defense-evasion conversion exercises.

Only caller-supplied synthetic text is encoded or decoded. Nothing is executed.
The label is a testing category, not evidence of operational evasion capability.
There is no process, loader, antivirus, registry or network integration.
"""

from __future__ import annotations

import base64
import binascii
import codecs
import copy
import hashlib
import json
import sys
import unicodedata
import zlib
from dataclasses import dataclass


TACTIC = "Defense Evasion (legacy category) / Stealth"
TACTIC_ID = "TA0005"
MAX_INPUT = 65536
MAX_PAYLOAD = 4096
MAX_STEPS = 16
MAX_RECIPES = 16


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


def text_value(value, field, maximum=4096, empty=True):
    if not isinstance(value, str):
        raise ModelError("TEXT_REQUIRED", field)
    if len(value) > maximum or (not empty and not value):
        raise ModelError("TEXT_LENGTH", field)
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


def bounded(data):
    if len(data) > MAX_PAYLOAD:
        raise ModelError("PAYLOAD_LIMIT", "data")
    return bytes(data)


def decode_text(data, encoding="utf-8"):
    try:
        return data.decode(encoding, errors="strict")
    except UnicodeError as error:
        raise ModelError("INVALID_TEXT_ENCODING", "data") from error


def encode_text(text, encoding="utf-8"):
    try:
        return bounded(text.encode(encoding, errors="strict"))
    except UnicodeError as error:
        raise ModelError("UNENCODABLE_TEXT", "data") from error


@dataclass(frozen=True)
class Blob:
    data: bytes
    representation: str

    @classmethod
    def from_input(cls, value):
        object_value(value, "payload")
        fields(value, {"text", "hex"}, "payload")
        if ("text" in value) == ("hex" in value):
            raise ModelError("ONE_REPRESENTATION_REQUIRED", "payload")
        if "text" in value:
            text = text_value(value["text"], "text")
            return cls(encode_text(text), "utf-8")
        text = text_value(value["hex"], "hex", MAX_PAYLOAD * 2)
        try:
            data = binascii.unhexlify(text)
        except (ValueError, binascii.Error) as error:
            raise ModelError("INVALID_HEX", "hex") from error
        return cls(bounded(data), "binary")

    def summary(self):
        result = {
            "hex": self.data.hex(),
            "length": len(self.data),
            "representation": self.representation,
        }
        try:
            result["text"] = self.data.decode("utf-8")
        except UnicodeDecodeError:
            result["text"] = None
        return result


@dataclass(frozen=True)
class Step:
    name: str
    parameters: dict

    @classmethod
    def from_input(cls, value):
        object_value(value, "step")
        name = text_value(value.get("name"), "name", 32, False)
        if name not in STEP_FIELDS:
            raise ModelError("UNKNOWN_TRANSFORM", "name")
        fields(value, STEP_FIELDS[name] | {"name"}, "step")
        return cls(name, {key: value[key] for key in value if key != "name"})


STEP_FIELDS = {
    "rotate": {"offset"},
    "repeat": {"count"},
    "assert_length": {"expected"},
    "unique_bytes": set(),
    "assert_representation": {"expected"},
    "base64_encode": set(),
    "base64_decode": set(),
    "hex_encode": set(),
    "hex_decode": set(),
    "rot13": set(),
    "reverse": set(),
    "xor": {"key"},
    "compress": {"level"},
    "decompress": set(),
    "transcode": {"source", "target"},
    "normalize": {"form"},
    "slice": {"start", "stop", "stride"},
    "assert_hex": {"expected"},
    "fail": {"code"},
}


class TransformEngine:
    def assert_representation(self, blob, parameters):
        expected = text_value(
            parameters.get("expected"),
            "expected",
            32,
            False,
        )
        if expected != blob.representation:
            raise ModelError("REPRESENTATION_MISMATCH", "expected")
        return blob

    def rotate(self, blob, parameters):
        offset = integer_value(
            parameters.get("offset"),
            "offset",
            -MAX_PAYLOAD,
            MAX_PAYLOAD,
        )
        if not blob.data:
            return Blob(b"", "binary")
        offset %= len(blob.data)
        left = blob.data[offset:]
        right = blob.data[:offset]
        return Blob(left + right, "binary")

    def repeat(self, blob, parameters):
        count = integer_value(
            parameters.get("count"),
            "count",
            0,
            16,
        )
        if len(blob.data) * count > MAX_PAYLOAD:
            raise ModelError("PAYLOAD_LIMIT", "data")
        return Blob(blob.data * count, blob.representation)

    def assert_length(self, blob, parameters):
        expected = integer_value(
            parameters.get("expected"),
            "expected",
            0,
            MAX_PAYLOAD,
        )
        if len(blob.data) != expected:
            raise ModelError("LENGTH_MISMATCH", "expected")
        return blob

    def unique_bytes(self, blob, parameters):
        seen = set()
        output = bytearray()
        for value in blob.data:
            if value in seen:
                continue
            seen.add(value)
            output.append(value)
        return Blob(bytes(output), "binary")

    def base64_encode(self, blob, parameters):
        data = bounded(base64.b64encode(blob.data))
        return Blob(data, "base64")

    def base64_decode(self, blob, parameters):
        try:
            data = base64.b64decode(blob.data, validate=True)
        except (ValueError, binascii.Error) as error:
            raise ModelError("INVALID_BASE64", "data") from error
        return Blob(bounded(data), "binary")

    def hex_encode(self, blob, parameters):
        return Blob(bounded(binascii.hexlify(blob.data)), "hex")

    def hex_decode(self, blob, parameters):
        try:
            data = binascii.unhexlify(blob.data)
        except (ValueError, binascii.Error) as error:
            raise ModelError("INVALID_HEX", "data") from error
        return Blob(bounded(data), "binary")

    def rot13(self, blob, parameters):
        text = decode_text(blob.data)
        return Blob(encode_text(codecs.encode(text, "rot_13")), "utf-8")

    def reverse(self, blob, parameters):
        return Blob(blob.data[::-1], "binary")

    def xor(self, blob, parameters):
        key = integer_value(parameters.get("key"), "key", 0, 255)
        data = bytes(value ^ key for value in blob.data)
        return Blob(data, "binary")

    def compress(self, blob, parameters):
        level = integer_value(parameters.get("level", 6), "level", 0, 9)
        data = bounded(zlib.compress(blob.data, level))
        return Blob(data, "zlib")

    def decompress(self, blob, parameters):
        decompressor = zlib.decompressobj()
        try:
            data = decompressor.decompress(blob.data, MAX_PAYLOAD + 1)
        except zlib.error as error:
            raise ModelError("INVALID_ZLIB", "data") from error
        bounded(data)
        if decompressor.unconsumed_tail:
            raise ModelError("PAYLOAD_LIMIT", "data")
        if not decompressor.eof:
            raise ModelError("TRUNCATED_ZLIB", "data")
        if decompressor.unused_data:
            raise ModelError("TRAILING_ZLIB_DATA", "data")
        return Blob(data, "binary")

    def transcode(self, blob, parameters):
        encodings = {"utf-8", "utf-16-le", "ascii", "latin-1"}
        source = text_value(parameters.get("source"), "source", 16, False)
        target = text_value(parameters.get("target"), "target", 16, False)
        if source not in encodings or target not in encodings:
            raise ModelError("UNSUPPORTED_ENCODING", "encoding")
        text = decode_text(blob.data, source)
        return Blob(encode_text(text, target), target)

    def normalize(self, blob, parameters):
        form = text_value(parameters.get("form"), "form", 8, False)
        if form not in {"NFC", "NFD", "NFKC", "NFKD"}:
            raise ModelError("NORMALIZATION_FORM", "form")
        text = decode_text(blob.data)
        normalized = unicodedata.normalize(form, text)
        return Blob(encode_text(normalized), "utf-8")

    def slice(self, blob, parameters):
        start = parameters.get("start")
        stop = parameters.get("stop")
        stride = parameters.get("stride", 1)
        if start is not None:
            integer_value(start, "start", -MAX_PAYLOAD, MAX_PAYLOAD)
        if stop is not None:
            integer_value(stop, "stop", -MAX_PAYLOAD, MAX_PAYLOAD)
        integer_value(stride, "stride", -MAX_PAYLOAD, MAX_PAYLOAD)
        if stride == 0:
            raise ModelError("ZERO_STRIDE", "stride")
        selection = slice(start, stop, stride)
        return Blob(blob.data[selection], "binary")

    def assert_hex(self, blob, parameters):
        expected = text_value(parameters.get("expected"), "expected", 8192)
        if blob.data.hex() != expected:
            raise ModelError("CONTENT_MISMATCH", "expected")
        return blob

    def fail(self, blob, parameters):
        code = text_value(parameters.get("code", "INJECTED_FAILURE"), "code", 40, False)
        raise ModelError(code, "step")

    def apply(self, blob, step):
        handlers = {
            "assert_representation": self.assert_representation,
            "rotate": self.rotate,
            "repeat": self.repeat,
            "assert_length": self.assert_length,
            "unique_bytes": self.unique_bytes,
            "base64_encode": self.base64_encode,
            "base64_decode": self.base64_decode,
            "hex_encode": self.hex_encode,
            "hex_decode": self.hex_decode,
            "rot13": self.rot13,
            "reverse": self.reverse,
            "xor": self.xor,
            "compress": self.compress,
            "decompress": self.decompress,
            "transcode": self.transcode,
            "normalize": self.normalize,
            "slice": self.slice,
            "assert_hex": self.assert_hex,
            "fail": self.fail,
        }
        return handlers[step.name](blob, step.parameters)


class RecipeSession:
    def __init__(self, initial):
        self.initial = initial
        self.current = initial
        self.engine = TransformEngine()
        self.history = []
        self.checkpoints = {}

    def checkpoint(self, name):
        name = text_value(name, "checkpoint", 32, False)
        if name in self.checkpoints:
            raise ModelError("DUPLICATE_CHECKPOINT", "checkpoint")
        if len(self.checkpoints) >= 16:
            raise ModelError("CHECKPOINT_LIMIT", "checkpoint")
        self.checkpoints[name] = self.current

    def restore(self, name):
        name = text_value(name, "restore", 32, False)
        if name not in self.checkpoints:
            raise ModelError("CHECKPOINT_NOT_FOUND", "restore")
        self.current = self.checkpoints[name]

    def run_recipe(self, value):
        object_value(value, "recipe")
        fields(
            value,
            {"name", "steps", "atomic", "checkpoint", "restore"},
            "recipe",
        )
        name = text_value(value.get("name"), "name", 64, False)
        atomic = boolean_value(value.get("atomic", True), "atomic")
        raw_steps = list_value(value.get("steps"), "steps", MAX_STEPS)
        steps = [Step.from_input(step) for step in raw_steps]
        before = self.current
        checkpoints_before = dict(self.checkpoints)
        trace = []
        try:
            if "restore" in value:
                self.restore(value["restore"])
            if "checkpoint" in value:
                self.checkpoint(value["checkpoint"])
            for index, step in enumerate(steps):
                previous = self.current
                self.current = self.engine.apply(self.current, step)
                trace.append(
                    {
                        "index": index,
                        "name": step.name,
                        "before_length": len(previous.data),
                        "after_length": len(self.current.data),
                    }
                )
        except ModelError as error:
            if atomic:
                self.current = before
                self.checkpoints = checkpoints_before
            result = {
                "name": name,
                "ok": False,
                "error": error.as_dict(),
                "rolled_back": atomic,
                "trace": trace,
            }
        else:
            result = {
                "name": name,
                "ok": True,
                "rolled_back": False,
                "trace": trace,
            }
        result["payload"] = self.current.summary()
        self.history.append(result)

    def report(self):
        return {
            "payload": self.current.summary(),
            "same_bytes_as_input": self.current.data == self.initial.data,
            "sha256": hashlib.sha256(self.current.data).hexdigest(),
            "checkpoints": sorted(self.checkpoints),
            "history": copy.deepcopy(self.history),
        }


def simulate(document):
    object_value(document, "input")
    fields(document, {"payload", "recipes"}, "input")
    initial = Blob.from_input(document.get("payload"))
    recipes = list_value(document.get("recipes"), "recipes", MAX_RECIPES)
    session = RecipeSession(initial)
    for recipe in recipes:
        session.run_recipe(recipe)
    return {
        "tactic": TACTIC,
        "tactic_id": TACTIC_ID,
        "simulation": True,
        "state": session.report(),
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
