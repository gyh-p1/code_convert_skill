"""System-side text fixtures only. No conversion samples or build commands."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).with_name("loading_preflight.py")
spec = importlib.util.spec_from_file_location("loading_preflight", MODULE)
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)
ROOT = MODULE.parent.parent


class LoadingChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        for name in (*lp.ENTRIES, *lp.CORE.values(), *lp.WORKFLOWS.values()):
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Fixture\n\nline two\nline three\nline four\n", encoding="utf-8")
        (self.repo / "AGENTS.md").write_text("# Agent\n[Root](SKILL.md)\n", encoding="utf-8")
        (self.repo / lp.ENTRIES[0]).write_text("# Discovery\n[Root](../../../SKILL.md)\n", encoding="utf-8")
        table = "# Root\n\n| 契约标识 | 必读真源 | 负责什么 | 何时消费 |\n|---|---|---|---|\n"
        table += "".join(f"| {key} | [contract]({name}) | purpose | before |\n" for key, name in lp.CORE.items())
        table += "\n" + "\n".join(f"[workflow]({name})" for name in lp.WORKFLOWS.values())
        table += "\n[uncovered](skills/other.md)\n"
        (self.repo / "SKILL.md").write_text(table, encoding="utf-8")
        self.log = self.base / "host.jsonl"
        self.rows = [{"type": "session_meta", "payload": {"id": "test-session"}}]
        self.count = 0
        self.write_log()

    def write_log(self):
        self.log.write_bytes(b"".join(lp.encoded(r) + b"\n" for r in self.rows))

    def artifact(self, name, data):
        path = self.base / name
        lp.save_new(path, lp.encoded(data))
        return lp.ref(path)

    def append_offer(self, offer, nested=True):
        self.count += 1
        call = f"read-{self.count}"
        self.rows.append({"type": "response_item", "payload": {
            "type": "custom_tool_call", "name": "exec", "call_id": call, "input": "system read"}})
        output = lp.MARKER + json.dumps(offer["payload"], ensure_ascii=False)
        if nested:
            output = [{"type": "text", "text": json.dumps({"output": output, "exit_code": 0})}]
        self.rows.append({"type": "response_item", "payload": {
            "type": "custom_tool_call_output", "call_id": call, "output": output}})
        self.write_log()
        receipt = lp.make_receipt(offer, self.log, call)
        return self.artifact(f"receipt-{self.count}.json", receipt)

    def offer(self, name, start=None, end=None):
        total = len((self.repo / name).read_bytes().decode("utf-8").splitlines(keepends=True))
        return lp.make_offer(self.repo, name, start or 1, end or total)

    def record(self, batch=False, long=False, omit=None):
        structure = lp.check_repo(self.repo)
        self.assertEqual(structure["status"], "PASS", structure["findings"])
        data = {"taskId": "T1", "runId": "R1", "context": {"sessionId": "test-session", "epoch": 0},
                "workflows": {"batch": {"applies": batch, "basis": "fixture request size"},
                              "long-file": {"applies": long, "basis": "fixture source complexity"}},
                "structure": self.artifact("structure.json", structure), "reads": []}
        for name in (*lp.CORE.values(), *(lp.WORKFLOWS.values() if batch and long else
                      [lp.WORKFLOWS["batch"]] if batch else [lp.WORKFLOWS["long-file"]] if long else [])):
            if name != omit:
                data["reads"].append(self.append_offer(self.offer(name)))
        return data

    def save_record(self, data):
        path = self.base / "frozen-inputs.md"
        path.write_text("# Existing task record\n\n```loading-preflight\n" +
                        json.dumps(data, ensure_ascii=False) + "\n```\n", encoding="utf-8")
        return path

    def check(self, data, action="freeze", before=None):
        return lp.check_next(self.repo, self.save_record(data), action, self.log, before)

    def edit(self, name, old, new):
        path = self.repo / name
        path.write_text(path.read_text(encoding="utf-8-sig").replace(old, new), encoding="utf-8")

    def test_structure_baseline_exact_scope(self):
        result = lp.check_repo(self.repo)
        self.assertEqual(result["status"], "PASS", result["findings"])
        self.assertEqual(len(result["files"]), 12)
        self.assertTrue(result["skipped"])
        self.assertIn("controller", result["uncovered"])

    def test_real_repository_structure(self):
        result = lp.check_repo(ROOT)
        self.assertEqual(result["status"], "PASS", result["findings"])

    def test_same_count_replacement(self):
        self.edit("SKILL.md", lp.CORE["task-state"], lp.CORE["safety"])
        self.assertEqual(lp.check_repo(self.repo)["findings"][0]["code"], "manifest")

    def test_missing_file(self):
        (self.repo / lp.CORE["build"]).unlink()
        self.assertEqual(lp.check_repo(self.repo)["status"], "FAIL")

    def test_empty_file(self):
        (self.repo / lp.CORE["build"]).write_text(" ", encoding="utf-8")
        self.assertEqual(lp.check_repo(self.repo)["status"], "FAIL")

    def test_unknown_table_no_fallback(self):
        self.edit("SKILL.md", "契约标识", "Unknown")
        self.assertEqual(lp.check_repo(self.repo)["status"], "FAIL")

    def test_duplicate_identity(self):
        self.edit("SKILL.md", "| build |", "| loop |")
        self.assertEqual(lp.check_repo(self.repo)["status"], "FAIL")

    def test_bad_anchor(self):
        self.edit("AGENTS.md", "SKILL.md)", "SKILL.md#absent)")
        self.assertTrue(any(f["code"] == "link" for f in lp.check_repo(self.repo)["findings"]))

    def test_inline_fence_history_not_blacklist(self):
        with (self.repo / "AGENTS.md").open("a", encoding="utf-8") as f:
            f.write("\n`[bad](SKILL.md#absent)`\n\n```md\n[bad](SKILL.md#absent)\n```\n\n> 历史：唯一脚本\n")
        self.assertEqual(lp.check_repo(self.repo)["status"], "PASS")

    def test_route_missing(self):
        (self.repo / lp.ENTRIES[0]).write_text("# Empty discovery", encoding="utf-8")
        self.assertTrue(any(f["code"] == "route" for f in lp.check_repo(self.repo)["findings"]))

    def test_path_escape(self):
        with self.assertRaises(lp.Invalid):
            lp.make_offer(self.repo, "../secret.md", 1, 1)

    def test_non_markdown_offer_rejected(self):
        with self.assertRaises(lp.Invalid):
            lp.make_offer(self.repo, ".env", 1, 1)

    def test_headings_unicode_duplicates(self):
        tokens = lp.parser().parse("# 标题：A\n# 标题：A\n# 标题：A-1\n")
        self.assertEqual(lp.headings(tokens), {"标题a", "标题a-1", "标题a-1-1"})

    def test_heading_uses_rendered_inline_text(self):
        self.assertEqual(lp.headings(lp.parser().parse("# [API](https://example.test) **Call** `x`\n")),
                         {"api-call-x"})

    def test_offer_unicode_crlf_and_bom(self):
        name = lp.CORE["build"]
        raw = b"\xef\xbb\xbf" + "# 文档\r\n\r\n第三行\r\n".encode("utf-8")
        (self.repo / name).write_bytes(raw)
        offer = lp.make_offer(self.repo, name, 2, 3)
        p = lp.validate_offer(offer)
        self.assertEqual(raw[p["byteStart"]:p["byteEnd"]].decode("utf-8"), p["text"])
        self.assertEqual(p["sha256"], lp.digest(raw))

    def test_nested_and_plain_host_returns(self):
        for nested in (True, False):
            pointer = self.append_offer(self.offer(lp.CORE["build"]), nested)
            self.assertEqual(lp.verify_receipt(lp.load_json(pointer["path"]))[1]["sessionId"], "test-session")

    def test_missing_final_payload(self):
        offer = self.offer(lp.CORE["build"])
        self.append_offer(offer)
        self.rows[-1]["payload"]["output"] = "Warning: truncated output\n" + lp.MARKER + "{"
        self.write_log()
        with self.assertRaises(lp.Invalid):
            lp.make_receipt(offer, self.log, "read-1")

    def test_modified_text_rejected(self):
        offer = self.offer(lp.CORE["build"])
        self.append_offer(offer)
        self.rows[-1]["payload"]["output"] = lp.MARKER + json.dumps({**offer["payload"], "text": "changed"})
        self.write_log()
        with self.assertRaises(lp.Invalid):
            lp.make_receipt(offer, self.log, "read-1")

    def test_forged_offer_range(self):
        offer = self.offer(lp.CORE["build"])
        offer["payload"]["endLine"] -= 1
        with self.assertRaises(lp.Invalid):
            lp.validate_offer(offer)

    def test_self_declared_not_strong(self):
        with self.assertRaises(lp.Invalid):
            lp.verify_receipt({"schema": lp.SCHEMA, "kind": "receipt", "evidenceGrade": "SELF_DECLARED"})

    def test_duplicate_call_rejected(self):
        offer = self.offer(lp.CORE["build"])
        self.append_offer(offer)
        self.rows.append(self.rows[-1])
        self.write_log()
        with self.assertRaises(lp.Invalid):
            lp.make_receipt(offer, self.log, "read-1")

    def test_log_tampering(self):
        pointer = self.append_offer(self.offer(lp.CORE["build"]))
        receipt = lp.load_json(pointer["path"])
        self.rows[0]["payload"]["id"] = "other"
        self.write_log()
        with self.assertRaises(lp.Invalid):
            lp.verify_receipt(receipt)

    def test_append_log_does_not_invalidate(self):
        pointer = self.append_offer(self.offer(lp.CORE["build"]))
        self.rows.append({"type": "event_msg", "payload": {"type": "token_count"}})
        self.write_log()
        lp.verify_receipt(lp.load_json(pointer["path"]))

    def test_four_task_shapes_and_all_actions(self):
        for batch, long in ((False, False), (True, False), (False, True), (True, True)):
            with self.subTest(batch=batch, long=long):
                # Unique artifact names within the same test instance.
                if (self.base / "structure.json").exists():
                    (self.base / "structure.json").unlink()
                data = self.record(batch, long)
                for action in lp.ACTIONS:
                    result = self.check(data, action)
                    self.assertEqual(result["status"], "PASS", result)
                    self.assertFalse(result["executionAuthorized"])

    def test_missing_contract_coverage(self):
        data = self.record(omit=lp.CORE["safety"])
        self.assertEqual(self.check(data)["status"], "FAIL")

    def test_middle_gap_and_overlap(self):
        name = lp.CORE["build"]
        data = self.record(omit=name)
        total = len((self.repo / name).read_text(encoding="utf-8").splitlines())
        data["reads"].append(self.append_offer(self.offer(name, 1, 2)))
        data["reads"].append(self.append_offer(self.offer(name, 4, total)))
        self.assertEqual(self.check(data)["status"], "FAIL")
        data["reads"].append(self.append_offer(self.offer(name, 2, 4)))
        self.assertEqual(self.check(data)["status"], "PASS")

    def test_missing_conditional_workflow(self):
        data = self.record(batch=True, long=True, omit=lp.WORKFLOWS["long-file"])
        self.assertEqual(self.check(data, "map")["status"], "FAIL")
        self.assertEqual(self.check(data, "start")["status"], "PASS")

    def test_unknown_workflow(self):
        data = self.record()
        data["workflows"]["batch"]["applies"] = None
        with self.assertRaises(lp.Invalid):
            self.check(data)

    def test_long_applicability_deferred_only_before_profiling(self):
        data = self.record()
        data["workflows"]["long-file"] = {"applies": None, "basis": "待画像确定复杂度"}
        self.assertEqual(self.check(data, "start")["status"], "PASS")
        for action in ("map", "freeze", "generate"):
            with self.assertRaises(lp.Invalid):
                self.check(data, action)

    def test_false_workflow_without_reason(self):
        data = self.record()
        data["workflows"]["batch"]["basis"] = ""
        with self.assertRaises(lp.Invalid):
            self.check(data)

    def test_version_change_requires_new_report_and_reads(self):
        data = self.record()
        path = self.repo / lp.CORE["build"]
        path.write_bytes(path.read_bytes() + b"\nChanged\n")
        with self.assertRaises(lp.Invalid):
            self.check(data)
        data["structure"] = self.artifact("structure-2.json", lp.check_repo(self.repo))
        self.assertTrue(any(f["code"] == "version" for f in self.check(data)["findings"]))

    def test_late_read_does_not_retroactively_pass(self):
        data = self.record(long=True, omit=lp.WORKFLOWS["long-file"])
        self.rows.append({"type": "response_item", "payload": {
            "type": "custom_tool_call", "name": "exec", "call_id": "map-action"}})
        self.write_log()
        data["reads"].append(self.append_offer(self.offer(lp.WORKFLOWS["long-file"])))
        self.assertEqual(self.check(data, "map", "map-action")["status"], "FAIL")
        self.assertEqual(self.check(data, "map")["status"], "PASS")

    def test_cross_session(self):
        data = self.record()
        data["context"]["sessionId"] = "other"
        with self.assertRaises(lp.Invalid):
            self.check(data)

    def test_compaction_invalidates_old_ranges(self):
        data = self.record()
        self.rows.append({"type": "compacted", "payload": {}})
        self.write_log()
        data["context"]["epoch"] = len(self.rows)
        self.assertEqual(self.check(data)["status"], "FAIL")

    def test_ref_tampering(self):
        data = self.record()
        data["reads"][0]["sha256"] = "0" * 64
        with self.assertRaises(lp.Invalid):
            self.check(data)

    def test_recovery_needs_no_loading_artifacts(self):
        for action in lp.RECOVERY:
            result = lp.check_next(self.repo, None, action, None)
            self.assertEqual(result["status"], "PASS")
            self.assertFalse(result["executionAuthorized"])

    def test_atomic_no_overwrite(self):
        path = self.base / "evidence.json"
        lp.save_new(path, b"original")
        with self.assertRaises(FileExistsError):
            lp.save_new(path, b"replacement")
        self.assertEqual(path.read_bytes(), b"original")
        self.assertEqual(list(self.base.glob(".loading-*")), [])

    def test_failed_publish_cleans_temp(self):
        with patch.object(lp.os, "link", side_effect=OSError("fixture publish failure")):
            with self.assertRaises(OSError):
                lp.save_new(self.base / "evidence.json", b"text")
        self.assertFalse((self.base / "evidence.json").exists())
        self.assertEqual(list(self.base.glob(".loading-*")), [])

    def test_cli_exit_codes_and_unavailable_no_fake_artifact(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            good = self.base / "good.json"
            self.assertEqual(lp.cli(["check-repo", "--repo", str(self.repo), "--out", str(good)]), 0)
            (self.repo / lp.CORE["build"]).unlink()
            self.assertEqual(lp.cli(["check-repo", "--repo", str(self.repo), "--out", str(self.base / "bad.json")]), 1)
            missing = self.base / "missing.json"
            self.assertEqual(lp.cli(["record-read", "--out", str(missing)]), 2)
            self.assertFalse(missing.exists())

    def test_duplicate_record_block(self):
        path = self.base / "record.md"
        path.write_text("```loading-preflight\n{}\n```\n" * 2, encoding="utf-8")
        with self.assertRaises(lp.Invalid):
            lp.loading_record(path)

    def test_controller_directory_blocked_before_access(self):
        for path in ("D:/CodeConvertRemote/Stack/jobs/test.json", "d:\\CodeConvertRemote\\Stack\\x.md"):
            with patch.object(Path, "read_bytes", side_effect=AssertionError("must not read")):
                with self.assertRaises(lp.Invalid):
                    lp.guard_path(path)

    def test_manual_statement_cannot_pass_automated_gate(self):
        data = self.record(omit=lp.CORE["safety"])
        data["manual"] = {"complete": True, "status": "PASS"}
        self.assertEqual(self.check(data)["status"], "FAIL")

    def test_unknown_document_rejected(self):
        with self.assertRaises(lp.Invalid):
            lp.make_offer(self.repo, "source/sample.md", 1, 1)

    def test_source_arguments_are_not_host_return(self):
        offer = self.offer(lp.CORE["build"])
        self.append_offer(offer)
        self.rows[-2]["payload"]["input"] = lp.MARKER + json.dumps(offer["payload"])
        self.rows[-1]["payload"]["output"] = "file prepared"
        self.write_log()
        with self.assertRaises(lp.Invalid):
            lp.make_receipt(offer, self.log, "read-1")

    def test_windows_return_line_endings(self):
        offer = self.offer(lp.CORE["build"])
        text = lp.MARKER.replace("\n", "\r\n") + json.dumps(offer["payload"])
        self.assertTrue(lp.has_payload(text, offer["payload"]))

    def test_multiple_host_results_select_exact_document(self):
        first = self.offer(lp.CORE["build"])
        second = self.offer(lp.CORE["safety"])
        outputs = [{"text": json.dumps({"output": lp.MARKER + json.dumps(o["payload"])})}
                   for o in (first, second)]
        self.assertTrue(lp.has_payload(outputs, second["payload"]))

    def test_foreign_agents_remain_manual(self):
        for name in ("AGENTS.md", "SKILL.md", lp.ENTRIES[0], lp.CORE["safety"],
                     lp.CORE["task-state"], lp.CORE["delivery"], lp.WORKFLOWS["batch"]):
            text = (ROOT / name).read_text(encoding="utf-8-sig")
            self.assertIn("第三方智能体", text, name)
            self.assertTrue("不得" in text or "不编写" in text, name)
        # This is a wording regression, not proof that arbitrary agents obey it.

    def test_malformed_log_shape_is_unavailable(self):
        self.log.write_text("[]\n", encoding="utf-8")
        with self.assertRaises(lp.Invalid):
            lp.read_log(self.log)

    def test_live_incomplete_tail_ignored_but_middle_invalid(self):
        with self.log.open("ab") as f:
            f.write(b'{"type":')
        self.assertEqual(lp.read_log(self.log)[2], "test-session")
        with self.log.open("ab") as f:
            f.write(b'\n{}\n')
        with self.assertRaises(lp.Invalid):
            lp.read_log(self.log)

    def test_registered_digest_mismatch_rejected(self):
        real_load = lp.load_json
        def wrong_registration(path):
            data = real_load(path)
            if Path(path).name == "loading-registration.json":
                data["files"]["loading_preflight.py"] = "0" * 64
            return data
        with patch.object(lp, "load_json", side_effect=wrong_registration):
            with self.assertRaises(lp.Invalid):
                lp.verify_registration()


if __name__ == "__main__":
    unittest.main(verbosity=2)
