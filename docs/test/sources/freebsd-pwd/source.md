# FreeBSD `pwd(1)` (`bin/pwd/pwd.c`) upstream source snapshot

- Repository: `freebsd/freebsd-src` (`https://github.com/freebsd/freebsd-src`)
- Source path: `bin/pwd/pwd.c` (self-contained; system headers only)
- Pinned ref: tag **`release/14.2.0`** = commit `89042d64c83ca92d90bd3d161eebc353d5edb3c6` (`git ls-remote --tags`). Integrity anchored by the file sha256 below.
- Retrieved: 2026-09-28 via `raw.githubusercontent.com/.../release/14.2.0/...` (read-only fetch; no build or execution run here).
- License: **BSD-3-Clause** (`SPDX-License-Identifier: BSD-3-Clause` on line 2). Repo top-level `COPYRIGHT` retained here as `COPYRIGHT.freebsd`.
- Upstream description: prints the current working directory; `-P` (physical, default) via `getcwd(NULL,0)`, `-L` (logical) validating `$PWD` against `.` by `st_dev`/`st_ino` before trusting it.
- Size: **123** LF physical lines (`wc -l`).
- Integrity (sha256): `pwd.c` = `cf8b57f4b95abf55f7c64446686126202756411b64370751ffb21f0de93d3f68`

## Why this source (multi-system POSIX→Windows datapoint)

- **No platform branches**: full read + grep confirm no `_WIN32`/`WIN32`/`windows.h`. Single-OS source → no target-branch leakage.
- Exercises the `getcwd` ↔ `GetCurrentDirectory`/`_getcwd` row of `posix-windows-filesystem`, plus `$PWD`-vs-physical logical-cwd semantics and device/inode identity (`st_dev`/`st_ino`) — the last has no direct Windows equivalent (Windows uses volume serial + file index), a genuine mapping boundary.
- Read-only (print cwd); reads env `PWD`. No writes/delete/network/exec.

## Build context and safety boundary

- **FreeBSD-ism affecting even the Linux source baseline**: `usage(void) __dead2` uses the BSD `__dead2` macro from `<sys/cdefs.h>` (not defined by glibc) → C source may not build unmodified on the Linux VM; recorded as portability attribution, source not edited. `<err.h>` (`err`) exists on glibc.
- Source-side baseline (control, POSIX): `cc -std=c11 pwd.c -o pwd` on the Linux VM — may fail on `__dead2` (source-portability attribution, not a conversion defect).
- Target side (converted, Windows): `g++ -std=c++17 pwd.cpp -o pwd.exe` on the Windows VM — conversion must map `getcwd`→`_getcwd`, `st_dev`/`st_ino` identity → Windows file-id semantics (or documented gap), and provide `getopt`/`err`/`__dead2` equivalents.
- Exact toolchain, C++ standard, isolation and authorization frozen in the case's `01-frozen/frozen-inputs.md`. **No build was run here.**

Do not modify this snapshot.
