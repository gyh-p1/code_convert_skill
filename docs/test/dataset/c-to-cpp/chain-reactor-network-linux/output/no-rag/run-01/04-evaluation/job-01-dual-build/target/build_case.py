"""Case-private remote VM build only. Do not run on the development host."""

from __future__ import annotations

import subprocess
import sys


def run(args):
    subprocess.run(args, check=True, shell=False)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {"source", "target"}:
        raise SystemExit(2)
    mode = sys.argv[1]
    run(["gcc", "-std=gnu11", "-O0", "-I.", "-c", "util.c", "-o", "util.o"])
    run(["gcc", "-std=gnu11", "-O0", "-I.", "-c", "driver.c", "-o", "driver.o"])
    if mode == "source":
        run([
            "gcc", "-std=gnu11", "-O0", "-I.", "-c",
            "networking_quarks.c", "-o", "primary.o",
        ])
        run(["gcc", "primary.o", "util.o", "driver.o", "-o", "program"])
    else:
        run([
            "g++", "-std=gnu++17", "-O0", "-I.", "-c",
            "target.cpp", "-o", "primary.o",
        ])
        run(["g++", "primary.o", "util.o", "driver.o", "-o", "program"])


if __name__ == "__main__":
    main()
