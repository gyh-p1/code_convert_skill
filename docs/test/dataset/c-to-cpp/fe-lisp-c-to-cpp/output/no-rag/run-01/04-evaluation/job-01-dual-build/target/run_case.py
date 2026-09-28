import json
import subprocess
from pathlib import Path

# fe form-B (FE_STANDALONE) liveness driver.
# The compile-quality stage counts only BUILD evidence; this run is a harmless
# liveness check: launch the built REPL with stdin at immediate EOF so it reads
# no expression, exits EXIT_SUCCESS, and contacts nothing. No fixtures, no network.

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
