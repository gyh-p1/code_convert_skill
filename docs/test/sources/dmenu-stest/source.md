# dmenu `stest.c` upstream source snapshot

- Repository: `dmenu` (suckless.org), upstream `https://git.suckless.org/dmenu`
- Source path: `stest.c` (companion header `arg.h` retained alongside; required to compile — supplies the `ARGBEGIN`/`ARGEND`/`EARGF`/`ARGC` CLI-arg macros)
- Pinned commit: `61e0072c3e6adfc67bafbc84e376cf26bc3680c0` (resolved with `git clone` + `git checkout`; `git rev-parse HEAD` confirmed this exact hash at retrieval).
- Retrieved: 2026-09-28 via `git clone https://git.suckless.org/dmenu` then checkout of the pinned commit (read-only; no build or execution run here). suckless serves no raw HTTP endpoint, so a clone was used rather than a raw fetch.
- License: **MIT/X Consortium License** (upstream `LICENSE` first line reads "MIT/X Consortium License"; `stest.c` line 1 references it). Accompanying upstream `LICENSE` retained in this directory; upstream `README` retained as `UPSTREAM-README.md`.
- Upstream description: `stest` is a small `test(1)`-like file-attribute filter used by `dmenu_path`; it filters a list of paths (from stdin or argv, optionally listing a directory's contents) by file-type/permission/time predicates.
- Size: `stest.c` = **109** LF physical lines (`wc -l`); `arg.h` = **49**. Within the ~600–900 physical-line target band for this stage (small, but chosen for API-surface density, not length).
- Integrity (sha256):
  - `stest.c` = `bb943c3e2c228398c592e873bb31abf18efba5c0f06c3bc39220443a7c7696bd`
  - `arg.h`   = `99ca0b684fa83f2d21899345ccc33ec357cbbe48d09c56794e3292c2e28f21b0`
  - `LICENSE` = `d9875debd0a9436f1bf91f3e1f7d1a87a5d6ba8ee393104b9c6c9dde28f72bed`

## Why this source (multi-system POSIX→Windows datapoint)

- **No platform branches**: reading the whole file confirms zero `_WIN32`/`WIN32`/`windows.h`; POSIX headers only (`sys/stat.h`, `dirent.h`, `limits.h`, `unistd.h`). Single-OS source → the conversion must supply the Windows side itself, with **no target-branch leakage** (the defect that made uhttpd unsuitable as a clean datapoint).
- **Richest POSIX-filesystem API surface of the batch** (all lack drop-in Windows equivalents): `stat`/`lstat`, `access(F_OK/R_OK/W_OK/X_OK)`, `opendir`/`readdir`/`closedir` + `struct dirent.d_name`, `getline`, and the `S_ISBLK`/`S_ISCHR`/`S_ISDIR`/`S_ISREG`/`S_ISLNK`/`S_ISFIFO` macros plus `S_ISGID`/`S_ISUID`. This is the primary consumer that will exercise (and validate/correct) `skills/systems/posix-windows-filesystem`.
- Fully **read-only**: no writes, no `unlink`/`remove`, no network, no `system`/`exec*`, no `getenv`. Reads path list from stdin or argv. Safest source of the batch.

## Build context and safety boundary

- Source-side baseline (control, POSIX): `cc -std=c11 stest.c -o stest` on the Linux VM — expected to build clean (pure POSIX).
- Target side (converted, Windows): `g++ -std=c++17 stest.cpp -o stest.exe` on the Windows VM — the conversion must map `opendir`/`readdir`→`FindFirstFile`/`FindNextFile`, `lstat`+`S_ISLNK`→reparse-point handling (or documented gap), `access` modes→`_access`/attributes, `getline`→a custom reader, and the `arg.h` macros must compile under C++.
- Exact compiler/SDK versions, C++ standard, isolation and per-case execution/compile authorization are frozen in the case's `01-frozen/frozen-inputs.md` when the run is opened, not here. **No build was run here.**

Do not modify this snapshot. Case-specific conversion instructions, frozen toolchain and any oracle belong in the case file; this directory only holds the frozen upstream snapshot.
