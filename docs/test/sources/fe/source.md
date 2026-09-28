# fe upstream source snapshot

- Repository: `rxi/fe`
- Source path: `src/fe.c` (companion header `src/fe.h` retained alongside; required to compile)
- Pinned commit: `3efa075` (2020-04-05). Full 40-char SHA was not resolved (GitHub API rate-limited at retrieval); integrity is instead pinned by the file hashes below.
- Retrieved: 2026-09-27 via `raw.githubusercontent.com` (read-only fetch; no build or execution run here).
- License: MIT (©2020 rxi); accompanying upstream `LICENSE` is retained in this directory. Upstream `README.md` retained as `UPSTREAM-README.md`.
- Upstream project description: a small, self-contained Lisp interpreter in ANSI C with a mark-and-sweep garbage collector.
- Size: `fe.c` = **879** LF-normalized physical lines (`fe.h` = 61). Within the current ~600–900 physical-line target for a clean C → C++ compile datapoint.
- Integrity (sha256):
  - `fe.c` = `3fc7466e9ae2c114e6fdf36410fc8804a20c83d5c21babcaf664567af6276807`
  - `fe.h` = `4b30a0f26a8a3c186047a5f6ff60779811de5dfa596c2ea9942398cc0034a69e`

## Why this source (compile-quality datapoint)

- **No platform branches**: no `_WIN32` / `__linux__` / `__BSD__` conditionals. `fe.c` includes only `<string.h>` and `"fe.h"`; `fe.h` includes `<stdlib.h>` and `<stdio.h>`. This keeps the C → C++ compile signal free of target-OS-branch leakage (the defect that made C01/uhttpd unsuitable as a clean first datapoint).
- **High logic density**: heavy use of `union`, function pointers, macros, pointer arithmetic and aggregate initialization — the C constructs most likely to surface real C → C++ compile deltas (implicit conversions, `void*`, initialization forms).
- **Independent second long source**: distinct from uhttpd; fills the "second independent long source" gap recorded in `../../four-case-matrix.md`.

## Build context and safety boundary

- Standalone program vs translation unit: a `main` exists only under `#ifdef FE_STANDALONE` (a REPL that also includes `<setjmp.h>`). Without that macro, `fe.c` compiles as a **library translation unit**. Either mode is a valid compile target; the current stage reads build evidence only, so a REPL entry point is not required.
- Static safety boundary: no `system` / `exec` / `popen` / `socket` / `unlink` / `remove`; **no network**. The only `fopen` is inside the optional standalone REPL, reading a script path given on the command line. Low risk; nothing external is contacted.
- Dual-side build (to be frozen per-case when submitted to an approved isolated capability): source side compiles as C (e.g. `cc -std=c11 -c fe.c`), target side compiles the converted file as C++ (e.g. `g++ -std=c++17 -c fe.cpp`), each with `fe.h` present. Exact target OS/arch, compiler/SDK, C++ standard, isolation and per-case execution/compile authorization are recorded at freeze time in the case file, not here. **No build was run here.**

Do not modify this source snapshot. Case-specific conversion instructions, frozen toolchain and any behavior oracle belong in a dedicated case file when a conversion run is opened; this directory only holds the frozen upstream snapshot.
