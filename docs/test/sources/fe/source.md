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
- **Independent long source**: distinct from uhttpd and used by the [fe C→C++ compile run](../../dataset/c-to-cpp/fe-lisp-c-to-cpp/case.md). At 879 physical lines it does not validate the 700-line planned upper bound; the former four-case sample quota was cancelled.

## Build context and safety boundary

- Standalone program vs translation unit: a `main` exists only under `#ifdef FE_STANDALONE` (a REPL that also includes `<setjmp.h>`). Without that macro, `fe.c` compiles as a **library translation unit**. The actual run used `FE_STANDALONE` for both sides of the authorized comparison capsule; its result is recorded in the case, not inferred from this source note.
- Static safety boundary: no `system` / `exec` / `popen` / `socket` / `unlink` / `remove`; **no network**. The only `fopen` is inside the optional standalone REPL, reading a script path given on the command line. Low risk; nothing external is contacted.
- Dual-side build details, toolchain and returned evidence are recorded in the [fe case](../../dataset/c-to-cpp/fe-lisp-c-to-cpp/case.md) and its run. This source snapshot itself was only fetched and archived; no code is executed by reading this directory.

Do not modify this source snapshot. Case-specific instructions and evidence belong in the dedicated case; this directory holds the frozen upstream source and license.
