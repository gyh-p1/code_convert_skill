# FreeBSD `realpath(1)` (`bin/realpath/realpath.c`) upstream source snapshot

- Repository: `freebsd/freebsd-src` (`https://github.com/freebsd/freebsd-src`)
- Source path: `bin/realpath/realpath.c` (self-contained; system headers only, no local `""` includes)
- Pinned ref: tag **`release/14.2.0`** = commit `89042d64c83ca92d90bd3d161eebc353d5edb3c6` (resolved via `git ls-remote --tags`). Integrity anchored by the file sha256 below.
- Retrieved: 2026-09-28 via `raw.githubusercontent.com/.../release/14.2.0/...` (read-only fetch; no build or execution run here).
- License: **BSD-3-Clause** (`SPDX-License-Identifier: BSD-3-Clause` on line 2; Regents of the University of California). Repo top-level `COPYRIGHT` retained here as `COPYRIGHT.freebsd`.
- Upstream description: canonicalizes each path argument (relative → absolute, resolving symlinks) via `realpath(3)` and prints it; `-q` suppresses per-path warnings.
- Size: **82** LF physical lines (`wc -l`).
- Integrity (sha256): `realpath.c` = `179ec5ea1f7e6197c9acf9785c4933a379fed0839fb788be376ea8caff4de889`

## Why this source (multi-system POSIX→Windows datapoint)

- **No platform branches**: full read + grep confirm no `_WIN32`/`WIN32`/`windows.h`. Single-OS source → conversion supplies the Windows side, no target-branch leakage.
- **Directly exercises the headline `posix-windows-filesystem` rule**: `realpath(3)` ↔ `GetFullPathName`/`_fullpath` — the exact row that skill is built around (symlink resolution + existence semantics differ, not equivalent).
- Read-only (resolve + print); reads only `argv`. No writes/delete/network/exec.
- Thin API surface (essentially one `realpath()` call plus `getopt`); a small, focused datapoint rather than a broad one.

## Build context and safety boundary

- **FreeBSD-ism affecting even the Linux source baseline**: `usage(void) __dead2;` uses the BSD `__dead2` attribute macro from `<sys/cdefs.h>`, which glibc's `<sys/cdefs.h>` does **not** define → the C source may not build unmodified on the Linux VM. `<err.h>` (`warn`) exists on glibc. This is recorded as portability attribution; the source is frozen and not edited.
- Source-side baseline (control, POSIX): `cc -std=c11 realpath.c -o realpath` on the Linux VM — may fail on `__dead2`; that is source-portability attribution, not a conversion defect.
- Target side (converted, Windows): `g++ -std=c++17 realpath.cpp -o realpath.exe` on the Windows VM — conversion must map `realpath`→`_fullpath`/`GetFullPathName`, provide `getopt`/`warn`/`__dead2`/`PATH_MAX` equivalents.
- Exact toolchain, C++ standard, isolation and authorization frozen in the case's `01-frozen/frozen-inputs.md`. **No build was run here.**

Do not modify this snapshot.
