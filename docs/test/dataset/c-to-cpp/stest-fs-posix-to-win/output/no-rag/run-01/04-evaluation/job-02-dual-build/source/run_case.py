import json
import subprocess
from pathlib import Path

# stest POSIX->Windows liveness driver (step-04 filesystem batch).
# The compile-quality stage counts only BUILD evidence; this run is a harmless
# liveness check: launch the built stest with no path arguments and stdin at
# immediate EOF so its getline loop reads nothing, no filesystem entry is
# tested, it returns "no match" (exit 1), and it contacts nothing.
# No fixtures, no network, read-only.

ROOT = Path(__file__).resolve().parent


def find_exe():
    for name in ("program.exe", "program"):
        candidate = ROOT / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError("built program not found next to run_case.py")


def main():
    exe = find_exe()
    proc = subprocess.run(
        [str(exe)],
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
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
