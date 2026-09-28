import json
import subprocess
from pathlib import Path

# du POSIX/BSD->Windows liveness driver (step-04 filesystem batch, 4/4).
# The compile-quality stage counts only BUILD evidence; this run is a harmless
# liveness check: launch the built du in summarize mode over the workspace
# directory itself ("-s ."), so it recursively walks the read-only working
# directory, accumulates block usage and prints a single summary line, then
# exits. It writes nothing, deletes nothing, executes nothing else and contacts
# no endpoint; stdin is at immediate EOF.
# NOTE: reported block counts and the printed path text legitimately differ by
# OS (BSD st_blocks vs the Windows file-size/512 approximation, and path
# separator), so stdoutLen is expected to differ across sides; behaviour is not
# scored at this stage.
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
        [str(exe), "-s", "."],
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
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()