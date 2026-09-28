import json
import subprocess
from pathlib import Path

# pwd POSIX/BSD->Windows liveness driver (step-04 filesystem batch, 3/4).
# The compile-quality stage counts only BUILD evidence; this run is a harmless
# liveness check: launch the built pwd with no operands and stdin at immediate
# EOF, so it prints the current working directory (default physical mode) on one
# line and exits 0 (the source's no-flag, no-operand behaviour). It touches no
# fixture, writes nothing, executes nothing else and contacts no endpoint.
# NOTE: the printed path text and separator legitimately differ by OS
# (e.g. /abs/workspace vs C:\abs\workspace), so stdoutLen is expected to differ
# across sides; behaviour is not scored at this stage.
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
