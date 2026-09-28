# FreeBSD `du(1)` (`usr.bin/du/du.c`) upstream source snapshot

- Repository: `freebsd/freebsd-src` (`https://github.com/freebsd/freebsd-src`)
- Source path: `usr.bin/du/du.c` (self-contained single file; system headers only)
- Pinned ref: tag **`release/14.2.0`** = commit `89042d64c83ca92d90bd3d161eebc353d5edb3c6` (`git ls-remote --tags`). Integrity anchored by the file sha256 below.
- Retrieved: 2026-09-28 via `raw.githubusercontent.com/.../release/14.2.0/...` (read-only fetch; no build or execution run here).
- License: **BSD-3-Clause** (`SPDX-License-Identifier: BSD-3-Clause` on line 2; derived from Berkeley code by Chris Newcomb). Repo top-level `COPYRIGHT` retained here as `COPYRIGHT.freebsd`.
- Upstream description: recursive directory disk-usage summarizer; walks trees with `fts(3)`, sums block usage with hardlink de-duplication, human-readable/threshold/ignore options.
- Size: **561** LF physical lines (`wc -l`). Under the ~900 cap; by far the largest and most complex of the batch.
- Integrity (sha256): `du.c` = `d7ba9521006f876879a8e181c13547cf385184aa620fe7600518fd566197ae41`

## Why this source (multi-system POSIX→Windows datapoint)

- **No platform branches**: full read + grep confirm no `_WIN32`/`WIN32`/`windows.h`. Single-OS source → no target-branch leakage.
- Richest directory-walk sample: `fts_open`/`fts_read`/`fts_set` recursive traversal, `st_blocks`/`st_size`/`st_nlink` accounting, `fnmatch` ignore masks, hardlink hash de-dup. A substantial `posix-windows-filesystem` consumer (recursive walk ↔ `FindFirstFile`/`FindNextFile`).
- Read-only (traverse + sum + print); reads env `BLOCKSIZE`. No writes/delete/network/exec.

## ⚠️ Heavy FreeBSD-specific surface (expected hard datapoint)

Unlike the other three, `du.c` depends on a **broad FreeBSD-base surface that is absent on both the Linux source-baseline VM and the Windows/MinGW target**, so it is expected to be a hard, likely-failing datapoint whose value is feeding failure-class → skill rules (stage plan step 5), not a clean pass:

- `<fts.h>` `fts_open`/`fts_read`/`fts_set` — no Windows equivalent (must be reimplemented on `FindFirstFile`/`FindNextFile`); on Linux `fts` exists but with `_FILE_OFFSET_BITS` caveats.
- `<libutil.h>` `humanize_number`/`expand_number`/`getbsize` — **BSD-only; not in glibc** (Linux needs `libbsd`) and absent on MinGW.
- `signal(SIGINFO, …)` and `__unused` — **not defined on Linux or Windows** (BSD-only).
- `st_flags & UF_NODUMP` — BSD inode flags, **absent on Linux and Windows**.
- `<sys/queue.h>` `SLIST_*`, `<fnmatch.h>`, `<getopt.h>` `getopt_long`, `DEV_BSIZE`, `howmany`, `EX_USAGE` (`<sysexits.h>`), `<err.h>` — mixed glibc availability, **largely absent on MinGW**.

Consequence: the C **source baseline is not expected to build on the plain-glibc Linux VM** (libutil/SIGINFO/UF_NODUMP), and the Windows C++ target requires an essentially full reimplementation. This is recorded up front so the result is read as an attribution/skill-gap datapoint, not a conversion-quality regression.

## Build context and safety boundary

- Source-side baseline (control, POSIX): `cc -std=c11 du.c -o du` on the Linux VM — **expected to fail** on the BSD-only deps above (source-portability attribution, not a conversion defect).
- Target side (converted, Windows): `g++ -std=c++17 du.cpp -o du.exe` on the Windows VM — a large reimplementation lift; whatever the model produces is scored only on the target build.
- Exact toolchain, C++ standard, isolation and authorization frozen in the case's `01-frozen/frozen-inputs.md`. **No build was run here.**

Do not modify this snapshot.
