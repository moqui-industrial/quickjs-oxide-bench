# R51: shared atoms, phase 2 (the image atoms)

Fork branch `perf/shared-atoms` (91145c8e) against phase 1 (fork main 66db6a8f). `Compiler::load_image` sets
`Heap::share_atoms` while it loads, so an image's keys, function names and string constants go in the process's
shared table, while it has room. The design is the fork's `docs/shared-atoms.md`.

## mr-mantle

mr-moqui `f72fc796` ran in `../mr-moqui-r51`, with the five components as detached worktrees of their current
`HEAD`s, and the census agent's drop hook (`../census-mantle/mr-moqui-hook.diff`). `mantle-pair.sh` builds Maximal
`moqui` with the fork's path as a cargo patch and runs `QJS_ATOM_CENSUS=1 MOQUI_SCRIPT_STATS_FILE=...
./moq test mr-mantle --nobuild`.

Both fork trees carried the same probe line for the run (`census-print.py`). It prints the thread name and the
report's reserved and live bytes with each census. That line is not in the merged code: phase 2 takes the print out
of the library.

Both runs: 1947 features, 1946 passed. The one failure is the same in both, SupportAssignment's round robin
(the census agent's run had it too). Each run took about 300 s.

| | phase 1 | phase 2 |
|---|---:|---:|
| busiest worker: atoms (its own) | 11,614 (11,102) | 13,302 (831) |
| service workers' most reserved, median | 3324 KiB | 2230 KiB |
| service workers' most reserved, summed (23) | 70.8 MiB | 53.6 MiB |
| the five largest workers' most reserved | 4098, 3991, 3846, 3813, 3714 KiB | 3953, 3553, 3218, 3139, 3020 KiB |
| the process's runtimes at their peak (`heap_at_max`) | 99.7 MB | 75.4 MB |
| the main thread's peak atoms (its own) | 22,798 (22,286) | 23,391 (7,643) |
| the process's shared table | 512 atoms | 28,858 atoms, 579k units, 4.2 MB |

Per-thread peaks: `mantle-p1-peaks.md` and `mantle-p2-peaks.md`. The runtimes at the peak: `script-stats-summary.txt`.

A worker keeps 600 to 850 atoms of its own: the host's keys, one-character strings and the rest. The reserved bytes are
the heap's; the shared table is the process's, once.

## js_speed (`cold.txt`, `rows-10000.txt`)

| | base 1cdb77e2 | phase 1 | phase 2 |
|---|---:|---:|---:|
| engine start: allocations | 9,277 | 8,746 | 7,775 |
| engine start: js kept | 880,333 | 812,956 | 750,885 |
| new thread's runtime after its first script: reserved / live | 860 / 398 KiB | 795 / 373 KiB | 734 / 325 KiB |
| the same after List html | 1132 / 520 KiB | 1121 / 495 KiB | 863 / 392 KiB |

The script rows run on the thread that compiles the images, whose atoms stay its own. Their instructions are as in
phase 1 (`../shared-atoms-p1`). The V8 v7 instructions are as in phase 1 too (`v8-v7.md`, geomean 1.0029): `qjs`
loads no images.

## Phase 3: the key tables (`mantle-key-tables.txt`)

These come from a third mantle run, which also counted each runtime's image units and their key-table entries:

| | image units | key entries |
|---|---:|---:|
| main | 6,244 | 64,890 |
| the four largest workers | 2,918 to 3,786 | 28k to 36k |

That is 115 to 145 KB of keys a busy worker, plus one allocation for each unit's table. Across 23 workers it is 3 to 5
MB, about 6% of what phase 2 leaves.
