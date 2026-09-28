import hashlib
import json
import subprocess
from pathlib import Path

# rc4 C->Go same-OS liveness driver (LANGUAGE dimension, first datapoint).
# The compile-quality stage counts only BUILD evidence; this run is a harmless,
# deterministic liveness check: launch the built RC4 decryptor on the PUBLIC RC4
# test vector (key "Key" = hex 4b6579, ciphertext bbf316e8d940af0ad3), which
# decrypts to the ASCII plaintext "Plaintext", then exits. It reads only argv,
# writes only stdout, deletes nothing, executes nothing else and contacts no
# endpoint; stdin is at immediate EOF.
# Same-OS, same semantics on both sides, so exitCode / stdout are expected to be
# byte-identical across the C source build and the Go target build. Behaviour is
# not scored at this stage; this is liveness only.
# No fixtures, no network, read-only.

ROOT = Path(__file__).resolve().parent

# Public RC4 test vector -> plaintext "Plaintext".
ARGS = ["4b6579", "bbf316e8d940af0ad3"]


def find_exe():
    for name in ("program.exe", "program"):
        candidate = ROOT / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError("built program not found next to run_case.py")


def main():
    exe = find_exe()
    proc = subprocess.run(
        [str(exe)] + ARGS,
        cwd=str(ROOT),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
    )
    print(
        json.dumps(
            {
                "exitCode": proc.returncode,
                "stdoutLen": len(proc.stdout),
                "stderrLen": len(proc.stderr),
                "stdoutSha256": hashlib.sha256(proc.stdout).hexdigest(),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
