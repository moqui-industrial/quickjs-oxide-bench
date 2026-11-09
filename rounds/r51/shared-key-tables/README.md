# R51: shared atoms, phase 3 (shared key tables)

Fork branch `perf/shared-key-tables` against fork main `3c741ee8` (phase 2). mr-moqui master `2d0e1f29` ran in
`../mr-moqui-r51`, with the five components as detached worktrees and the drop hook
(`work/r51/mr-moqui-r51-drop-hook.diff`). Both fork trees carried a census print in `memory_report` for the run only
(thread, reserved and live bytes; not committed). `p3-all.sh` and `p3-k2.sh` ran the builds and the runs.

- **k0**: the base, phase 2.
- **k1**: image units share their key table (`ImageUnit::shared_keys`) when every key resolves to it.
- **k2**: k1, plus the embedder's keys (`NativeCx::key_from_latin1`, `key_from_units`) are shared atoms too. This is
  the merged change.

## mr-mantle (`mantle-k*-key-tables.md`, `script-stats-summary.txt`)

| | k0 | k1 | k2 |
|---|---:|---:|---:|
| service workers' key entries in tables of their own | 406,593 of 406,593 | 304,733 of 416,046 | 128,844 of 419,528 |
| the same as bytes (4 a key) | 1.63 MB | 1.22 MB | 0.52 MB |
| image units in the workers (each a table before) | 48,813 | 49,975 | 50,045 |
| workers' most reserved: median | 2327 KiB | 2289 KiB | 2284 KiB |
| workers' most reserved: summed (23) | 54.3 MiB | 54.9 MiB | 52.9 MiB |
| `heap_at_max` | 79.4 MB | 79.1 MB | 65.3 MB |

**Why k1 shared little.** A unit naming one of the host's keys (`ec`, the host table's members, entity fields)
cannot share its table: each worker interned those keys as its own atoms before its first image load. Sharing the
embedder's keys (k2) fixes that.

**Reserved bytes.** k2's lower `heap_at_max` also comes from the host's atoms leaving the runtimes' string arenas.
`heap_at_max` is a single snapshot, so it moves with what the workers were doing at that moment. The key tables are
outside the reserved heap, in the code store.

**Spec results** (`mantle-results.txt`): k0 and k1 passed all 1947. k2 failed two:
- AccountingCollections' instalment ages 9 days, not 10;
- SupportCases' "Today".

Its run began at 23:00 CST, past midnight UTC. Rerun alone at 23:10, the base (k0's binary) fails the same two, so
they depend on the date, not on this change.

## js_speed (`cold-k0.txt`, `cold-k2.txt`, `rows-10000.txt`, `start-instructions.txt`)

Cold section, three runs each:

| | k0 | k2 |
|---|---:|---:|
| engine start: allocations | 7,775 | 6,421 to 6,503 |
| engine start: bytes | 2,548,618 | 2,471,885 to 2,480,553 |
| engine start: js kept | 750,885 | 718,996 |
| engine start: time, median of 3 (min) | 1.74 ms (1.43) | 1.65 ms (1.41) |
| first render, List html: allocations | 16,269 | 16,247 |
| first render: bytes | 2,160,050 | 1,803,274 |
| first render: js kept | 537,570 | 343,134 |
| a new thread's runtime after List html: reserved / live | 863 / 392 KiB | 812 / 368 KiB |

The time is within noise. The whole cold section measured 7.08G to 7.20G instructions in both builds: a start's
saving is lost in the process's own noise.

**Property rows** at 10,000 calls a batch, 6 batches minus 1, two runs each: walk itemList, item.name, 100 objects,
cached finds, JSON stringify, nowTimestamp, noop service calls and walk an entity list are all within ±1%. A key read
is not slower.

## V8 v7 (`v8-v7.md`)

Against `qjs` at 3c741ee8: geometric mean 1.0001, the largest 1.0005 (regexp).
