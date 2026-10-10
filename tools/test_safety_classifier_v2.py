"""Regression checks for the authorized static classifier; fixtures are NEVER executed."""
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).with_name("safety_classifier_v2.py")
spec = importlib.util.spec_from_file_location("review_classifier", MODULE)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class StaticClassifierChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.classifier = module.SafetyClassifierV2()

    def classify(self, text, suffix=".py"):
        source = self.root / ("source" + suffix)
        source.write_text(text, encoding="utf-8")
        result = self.classifier.classify("T1", "python-to-go", "fixture", str(source))
        self.assertFalse(result.executable)
        # Spec 04: executionApproved mirrors admissionStatus, it is no longer always False.
        self.assertEqual(result.details["executionApproved"], result.admission_status == "ALLOWED")
        return result

    def assertBlocked(self, result, reason):
        self.assertEqual(result.admission_status, "BLOCKED")
        self.assertEqual(result.blocking_reason, reason)
        self.assertFalse(result.details["executionApproved"])

    def assertAllowed(self, result):
        self.assertEqual(result.admission_status, "ALLOWED")
        self.assertIsNone(result.blocking_reason)
        self.assertTrue(result.details["executionApproved"])

    # --- Spec 04 3.1 input integrity -------------------------------------------------

    def test_missing_and_invalid_encoding_are_rows(self):
        missing = self.classifier.classify("T", "c-to-go", "x", str(self.root / "missing.c"))
        self.assertEqual(missing.classification, "BLOCKED_INPUT")
        self.assertBlocked(missing, "input_error")
        source = self.root / "invalid.py"
        source.write_bytes(b"\xff\xfe\x00")
        result = self.classifier.classify("T", "python-to-go", "x", str(source))
        self.assertEqual(result.classification, "BLOCKED_INPUT")
        self.assertBlocked(result, "input_error")

    # --- Spec 04 3.2 public network --------------------------------------------------

    def test_public_literal_is_blocked_without_batch_isolation(self):
        self.assertBlocked(self.classify('host = "8.8.8.8"\nsocket.connect((host, 80))'),
                           "public_network_unverified")

    def test_public_literal_is_allowed_with_batch_isolation(self):
        isolated = module.SafetyClassifierV2(batch_network_isolation_configured=True)
        source = self.root / "net.py"
        source.write_text('socket.connect(("8.8.8.8", 80))', encoding="utf-8")
        result = isolated.classify("T", "python-to-go", "fixture", str(source))
        self.assertEqual(result.classification, "REVIEW_NETWORK")
        self.assertAllowed(result)
        self.assertTrue(result.requires_network_isolation)

    def test_private_and_loopback_are_allowed_even_without_isolation(self):
        for text in ('socket.connect(("192.168.1.1", 80))', 'socket.connect(("127.0.0.1", 80))'):
            with self.subTest(text=text):
                self.assertAllowed(self.classify(text))

    # --- Spec 04 3.3 high-confidence credentials -------------------------------------

    def test_high_confidence_credential_is_blocked(self):
        result = self.classify('key = "AKIAIOSFODNN7EXAMPLE"')
        self.assertBlocked(result, "real_credential_suspected")
        findings = result.details["files"][0]["credentialFindings"]
        self.assertEqual([f["kind"] for f in findings], ["aws_access_key_id"])

    def test_credential_excerpt_never_carries_the_secret(self):
        secret = "ghp_16C7e42F292c6912E7710c838347Ae178B4a"
        result = self.classify(f'token = "{secret}"')
        self.assertBlocked(result, "real_credential_suspected")
        finding = result.details["files"][0]["credentialFindings"][0]
        self.assertNotIn(secret, json.dumps(result.details))
        self.assertEqual(finding["excerpt"], "ghp_" + "*" * (len(secret) - 4))
        self.assertEqual(finding["length"], len(secret))

    def test_url_credential_excerpt_hides_the_password(self):
        result = self.classify('url = "https://svc:hunter2swordfish@127.0.0.1/v1"')
        finding = result.details["files"][0]["credentialFindings"][0]
        self.assertEqual(finding["excerpt"], "https://<redacted>@")
        self.assertNotIn("hunter2swordfish", json.dumps(result.details))

    def test_private_key_block_is_blocked(self):
        self.assertBlocked(self.classify("-----BEGIN RSA PRIVATE KEY-----\nMIIEow==\n"),
                           "real_credential_suspected")

    def test_placeholder_credentials_are_not_blocked(self):
        for text in ('password = "changeme"', 'api_key = "your-token-here"',
                     'token = "PLACEHOLDER"', 'secret = "example"',
                     'conn = "postgres://user:changeme@db.internal/app"'):
            with self.subTest(text=text):
                self.assertAllowed(self.classify(text))

    def test_credential_findings_are_lexical_not_proof(self):
        # A real-looking password inside a URL is blocked as a credential; the host is
        # loopback so only rule 3 can be the reason.
        result = self.classify('url = "https://svc:hunter2swordfish@127.0.0.1/v1"')
        self.assertBlocked(result, "real_credential_suspected")
        self.assertTrue(result.requires_synthetic_data)

    def test_rule_two_precedes_rule_three(self):
        # Spec 04 ordering: an unisolated public target is reported as a network block,
        # so a reviewer fixes isolation first instead of chasing a credential claim.
        result = self.classify('key = "AKIAIOSFODNN7EXAMPLE"\nurl = "https://example.invalid/v1"')
        self.assertBlocked(result, "public_network_unverified")

    # --- v2.3 lexical boundary fixes --------------------------------------------------

    def test_dash_joined_identifier_is_not_dynamic_eval(self):
        result = self.classify('mode := "translation-eval"', ".go")
        self.assertEqual(result.classification, "LOW_SIGNAL")

    def test_go_pascalcase_write_is_not_the_win32_api(self):
        """`os.WriteFile` is a Go file write, not the Win32 WriteFile: review, but not sensitive."""
        result = self.classify('_ = os.WriteFile(path, data, 0o644)', ".go")
        self.assertEqual(result.classification, "REVIEW_SIDE_EFFECTS")
        self.assertIn("filesystem", result.details["reviewGroups"])
        self.assertNotIn("sensitive", result.details["reviewGroups"])

    def test_win32_writefile_is_still_detected(self):
        self.assertEqual(self.classify('WriteFile(h, buf, n, &w, NULL);', ".c").classification,
                         "REVIEW_SIDE_EFFECTS")

    def test_hardcoded_assignment_is_not_a_parameter(self):
        result = self.classify('host = "8.8.8.8"\nsocket.connect((host, 80))')
        self.assertEqual(result.classification, "REVIEW_NETWORK")
        self.assertTrue(any(t["scope"] == "public" and t["provenance"] == "literal"
                            for t in result.details["files"][0]["network_targets"]))

    # --- v2.4 hostname false-positive (C5, D2-055) ------------------------------------

    def test_filename_literal_in_path_context_is_not_a_network_target(self):
        # D2-055: `filepath.Join(root, "demo.txt")` — a bare file name must not be
        # promoted to a DNS target by the nearby variable word `target`.
        result = self.classify('target := filepath.Join(root, "demo.txt")', ".go")
        self.assertNotEqual(result.classification, "REVIEW_NETWORK")
        self.assertAllowed(result)
        targets = result.details["files"][0].get("network_targets", [])
        self.assertNotIn("demo.txt", [t["value"] for t in targets])

    def test_real_hostname_with_network_api_is_still_a_target(self):
        # Reverse regression (anti over-correction): a real external host consumed by a
        # network API stays a target and blocked without isolation.
        result = self.classify('conn, _ := net.Dial("tcp", "attacker.example.com")', ".go")
        self.assertEqual(result.classification, "REVIEW_NETWORK")
        self.assertBlocked(result, "public_network_unverified")

    def test_hardcoded_ip_with_wsaconnect_is_still_a_target(self):
        # D2-108 regression: hard-coded IP + WSAConnect stays a network target
        # (10.x is private, so allowed without isolation, but still REVIEW_NETWORK).
        result = self.classify('const char* a = "10.9.1.6";\nWSAConnect(s, (SOCKADDR*)&sa, len, 0, 0, 0, 0);', ".cpp")
        self.assertEqual(result.classification, "REVIEW_NETWORK")
        targets = result.details["files"][0]["network_targets"]
        self.assertIn("10.9.1.6", [t["value"] for t in targets])

    def test_dynamic_network_remains_unresolved(self):
        result = self.classify("socket.connect((args.host, args.port))")
        self.assertEqual(result.details["files"][0]["network_mode"], "unresolved")
        self.assertAllowed(result)  # unresolved hosts are not literal public targets

    def test_wildcard_is_not_loopback(self):
        self.assertFalse(self.classifier.is_loopback("0.0.0.0"))
        self.assertEqual(self.classify('socket.bind(("0.0.0.0", 80))').classification, "REVIEW_NETWORK")

    def test_private_network_still_needs_review(self):
        self.assertEqual(self.classify('socket.connect(("192.168.1.1", 80))').classification, "REVIEW_NETWORK")

    def test_loopback_still_needs_review(self):
        result = self.classify('socket.connect(("127.0.0.1", 80))')
        self.assertEqual(result.details["files"][0]["network_mode"], "loopback")

    def test_ipv6_and_invalid_addresses(self):
        for value, expected in (("::1", "loopback"), ("::", "wildcard"), ("fc00::1", "private"),
                                ("fe80::1", "special"), ("999.1.2.3", "invalid-ip")):
            with self.subTest(value=value):
                self.assertEqual(module.address_scope(value), expected)

    def test_python_comments_do_not_become_targets(self):
        result = self.classify('# https://example.com\nvalue = 1 # socket.connect("8.8.8.8")')
        self.assertEqual(result.classification, "LOW_SIGNAL")

    def test_c_block_comments_and_preprocessor(self):
        result = self.classify('/* https://example.com */\n#include <stdio.h>\nint main(){return 0;}', ".c")
        self.assertEqual(result.classification, "LOW_SIGNAL")

    def test_comment_marker_in_url_is_not_a_comment(self):
        result = self.classify('url = "https://example.com/a#x"')
        self.assertEqual(result.classification, "REVIEW_NETWORK")

    def test_powershell_block_comment(self):
        self.assertEqual(self.classify('<# socket.connect("8.8.8.8") #>\n$x=1', ".ps1").classification, "LOW_SIGNAL")

    def test_here_string_is_uncertain(self):
        self.assertEqual(self.classify('$x = @"\nhello\n"@', ".ps1").classification, "REVIEW_UNCERTAIN")

    def test_file_operations_are_not_network_safety(self):
        self.assertEqual(self.classify('open("result.txt", "w")').classification, "REVIEW_SIDE_EFFECTS")

    def test_process_operations_are_retained(self):
        self.assertEqual(self.classify('subprocess.run(argv)').classification, "REVIEW_SIDE_EFFECTS")

    def test_sensitive_signals_are_not_lost_to_network(self):
        result = self.classify('WriteProcessMemory(p, b)\nsocket.connect((host, port))', ".c")
        self.assertEqual(result.classification, "REVIEW_SENSITIVE")
        self.assertIn("network", result.details["reviewGroups"])

    def test_dynamic_code_is_retained(self):
        self.assertEqual(self.classify("eval(value)").classification, "REVIEW_SENSITIVE")

    def test_cpp_streams_and_environment_inventory(self):
        for text in ('std::ofstream out(path);', 'GetEnvironmentStrings();', 'std::filesystem::current_path();'):
            with self.subTest(text=text):
                self.assertEqual(self.classify(text, '.cpp').classification, 'REVIEW_SIDE_EFFECTS')

    def test_executable_memory_registry_and_kernel_hooks(self):
        for text in ('VirtualAlloc(p, n, MEM_COMMIT, PAGE_EXECUTE_READWRITE);',
                     'RegCreateKeyExW(key, path);', 'module_init(init_function);'):
            with self.subTest(text=text):
                self.assertEqual(self.classify(text, '.c').classification, 'REVIEW_SENSITIVE')

    def test_wmi_dispatch_is_a_process_signal(self):
        self.assertEqual(self.classify('pSvc->ExecMethod(name, method);', '.cpp').classification, 'REVIEW_SIDE_EFFECTS')

    def test_native_powershell_command_is_not_low_signal(self):
        self.assertEqual(self.classify('netsh wlan show profiles name="fixture" key=clear', '.ps1').classification, 'REVIEW_SENSITIVE')

    def test_csharp_verbatim_path(self):
        result = self.classify('var path = @"C:\\";', '.cs')
        self.assertEqual(result.classification, 'LOW_SIGNAL')

    def test_powershell_text_extension_uses_declared_direction(self):
        source = self.root/'sample.text'
        source.write_text('# https://example.com\n$x=1', encoding='utf-8')
        result = self.classifier.classify('T', 'powershell-to-python', 'fixture', str(source))
        self.assertEqual(result.classification, 'LOW_SIGNAL')
        self.assertEqual(result.details['files'][0]['languageBasis'], 'direction:powershell')

    def test_main_does_not_remove_framework_dependency(self):
        result = self.classify('class MetasploitModule\n def main\n end\nend', ".rb")
        self.assertEqual(result.classification, "REVIEW_DEPENDENCY")

    def test_no_fixture_execution(self):
        self.assertEqual(self.classify('raise RuntimeError("must never execute")').classification, "LOW_SIGNAL")

    def test_missing_source_file_is_input_error(self):
        missing = self.classifier.classify("T", "c-to-go", "x", str(self.root / "missing.c"))
        self.assertEqual(missing.classification, "BLOCKED_INPUT")
        self.assertBlocked(missing, "input_error")

    def test_hash_mismatch(self):
        source = self.root / "sample.py"
        source.write_text("x=1", encoding="utf-8")
        result = self.classifier.classify_files("T", "python-to-go", "x", [source], {source: "0"*64})
        self.assertEqual(result.classification, "BLOCKED_INPUT")
        self.assertBlocked(result, "input_error")

    def test_resource_limit(self):
        source = self.root / "large.py"
        source.write_bytes(b" " * (module.MAX_BYTES + 1))
        self.assertEqual(self.classifier.classify("T", "python-to-go", "x", str(source)).classification, "BLOCKED_INPUT")

    def test_multifile_batch_keeps_missing_rows_and_all_signals(self):
        source_dir = self.root / "case" / "source"
        source_dir.mkdir(parents=True)
        (source_dir / "main.py").write_text("x=1", encoding="utf-8")
        (source_dir / "helper.py").write_text('socket.connect((host, 80))', encoding="utf-8")
        batch = self.root / "batch.json"
        batch.write_text(json.dumps({"taskCount": 2, "tasks": [
            {"taskId": "A", "direction": "python-to-go", "caseId": "case", "sourceDir": "case/source"},
            {"taskId": "B", "direction": "python-to-go", "caseId": "missing", "sourceDir": "missing/source"}]}), encoding="utf-8")
        result = module.reclassify_batch(batch, self.root / "out.json", self.root)
        self.assertEqual([row["cls"] for row in result], ["REVIEW_NETWORK", "BLOCKED_INPUT"])
        self.assertEqual(len(result[0]["details"]["files"]), 2)
        self.assertEqual(json.loads((self.root/"out.json").read_text(encoding="utf-8")), result)

    def test_path_escape_does_not_read_external_input(self):
        batch = self.root / "batch.json"
        batch.write_text(json.dumps([{"id": "A", "dir": "c-to-go", "case": "x", "sourceDir": "../outside"}]), encoding="utf-8")
        result = module.reclassify_batch(batch, self.root/"out.json", self.root)
        self.assertEqual(result[0]["cls"], "BLOCKED_INPUT")
        self.assertIn("path_outside_source_base", str(result[0]["details"]))

    def test_manifest_relative_paths_resolve_against_the_manifest(self):
        """v2.2 read these as root-relative and emitted a false BLOCKED_INPUT."""
        case = self.root / "c-to-go" / "case-1" / "source"
        case.mkdir(parents=True)
        (case / "sample.c").write_text("int main(void){return 0;}", encoding="utf-8")
        manifest = self.root / "c-to-go" / "batch.json"
        manifest.write_text(json.dumps({"taskCount": 2, "tasks": [
            {"taskId": "A", "direction": "c-to-go", "caseId": "case-1",
             "sourcePath": "case-1/source/sample.c"},
            {"taskId": "B", "direction": "c-to-go", "caseId": "case-1",
             "sourceDir": "case-1/source"}]}), encoding="utf-8")
        result = module.reclassify_batch(manifest, self.root / "out-rel.json", self.root)
        self.assertEqual([row["cls"] for row in result], ["LOW_SIGNAL", "LOW_SIGNAL"])
        self.assertTrue(all(row["admissionStatus"] == "ALLOWED" for row in result))

    def test_parent_relative_manifest_paths_still_resolve(self):
        """The other documented style (`../<direction>/<case>/source`) must keep working."""
        case = self.root / "dataset" / "c-to-go" / "case-2" / "source"
        case.mkdir(parents=True)
        (case / "sample.c").write_text("int main(void){return 0;}", encoding="utf-8")
        manifest = self.root / "dataset" / "batch-99" / "batch.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({"taskCount": 1, "tasks": [
            {"taskId": "A", "direction": "c-to-go", "caseId": "case-2",
             "sourceDir": "../c-to-go/case-2/source"}]}), encoding="utf-8")
        result = module.reclassify_batch(manifest, self.root / "out-parent.json", self.root)
        self.assertEqual(result[0]["cls"], "LOW_SIGNAL")

    def test_source_base_remains_a_hard_boundary(self):
        """Widening the base must not let a manifest read outside every allowed root."""
        outside = self.root.parent / f"outside-{self.root.name}"
        outside.mkdir(exist_ok=True)
        self.addCleanup(shutil.rmtree, outside, True)
        (outside / "secret.py").write_text("import socket", encoding="utf-8")
        confined = self.root / "dataset"
        confined.mkdir(exist_ok=True)
        manifest = confined / "batch.json"
        manifest.write_text(json.dumps({"taskCount": 1, "tasks": [
            {"taskId": "A", "direction": "python-to-go", "caseId": "x",
             "sourceDir": f"../{outside.name}"}]}), encoding="utf-8")
        result = module.reclassify_batch(manifest, self.root / "out-escape.json", confined)
        self.assertEqual(result[0]["cls"], "BLOCKED_INPUT")
        self.assertIn("path_outside_source_base", str(result[0]["details"]))

    def test_duplicate_identity_and_existing_output(self):
        batch = self.root/"batch.json"
        row = {"id": "A", "dir": "c-to-go", "case": "x"}
        batch.write_text(json.dumps([row, row]), encoding="utf-8")
        output = self.root/"out.json"
        result = module.reclassify_batch(batch, output, self.root)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(row["cls"] == "BLOCKED_INPUT" for row in result))
        before = output.read_bytes()
        with self.assertRaises(FileExistsError):
            module.reclassify_batch(batch, output, self.root)
        self.assertEqual(output.read_bytes(), before)

    def test_bom_manifest_and_frozen_source(self):
        (self.root/"source").mkdir()
        source = self.root/"source"/"sample.py"
        source.write_bytes(b"x=1\n")
        batch = self.root/"batch.json"
        batch.write_text(json.dumps({"taskCount": 1, "tasks": [{"taskId":"A", "direction":"python-to-go",
            "sourcePath":"source/sample.py", "sourceSha256":hashlib.sha256(source.read_bytes()).hexdigest()}]}), encoding="utf-8-sig")
        result = module.reclassify_batch(batch, self.root/"out.json", self.root)
        self.assertEqual(result[0]["cls"], "LOW_SIGNAL")


if __name__ == "__main__":
    unittest.main()
