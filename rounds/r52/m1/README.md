# Round 52, lane M1: mr-moqui actions, OOM cleanup, idle release

mr-moqui master from fb0e5f78 (pin 34ef6147). Binaries and raw outputs are in `work/r52/` (`base/`, `m1/`).

## Base (`work/r52/base/`)

js_speed built at fb0e5f78 before any change, run twice in full (`run1.txt`, `run2.txt`, about 55 s each).

## M1a: a native path for trivial `<set>` (mr-moqui 9629dcdb)

`perf-rows.sh <binary> <dir>`: each row alone (`JS_SPEED_ONLY`, `JS_SPEED_ROW`) at 20000 calls (services 10000),
`perf stat -e instructions:u` with 1 batch and 6, instructions per call = (six - one) / (5 x calls). perf counts the
whole process tree (the embedded Postgres too), so the small rows' instructions vary by a few thousand; allocations
are exact. Another lane measured at the same time, so wall time is indicative only.

| row | allocs base | allocs M1a | instr/call base (2 runs) | instr/call M1a (2 runs) | us/call base | us/call M1a |
|---|---:|---:|---:|---:|---:|---:|
| one set | 6.0 | 2.0 | 15,519 / 13,586 | 2,090 / 4,095 | 0.97 | 0.19 |
| four sets (the echo#Data body) | 26.0 | 4.0 | 40,569 / 40,722 | 8,514 / 5,168 | 2.98 | 0.49 |
| set#One (one set) | 96.0 | 88.0 | 194,030 / 187,860 | 158,582 / 160,468 | 9.5 | 8.1 |
| echo#Inline (four sets) | 144.0 | 121.0 | 245,596 / 244,539 | 202,766 / 205,518 | 14.0-15.0 | 10.8 |
| BasicServices.echo#Data | 120.1 | 94.0 | 217,137 / 224,701 | 182,841 / 182,071 | 12.5-12.8 | 8.3-8.5 |

Behaviour change: a planned set keeps host types (Timestamp/Date/Time stay temporal, F64 stays F64, I64 stays I64);
echo#Data returns `timestampOut` as a Timestamp, as Java.

Semantics kept from the generated script, which differ from Java's template: `default-value` applies on null or ""
(Groovy's `?:` also on 0, false and empty collections), and `set-if-empty="false"` skips null or "" (Java's
`isEmpty` also skips an empty list or map).

## M1b: the OOM cleanup (mr-moqui 6304f480)

The fork's 3f5d5809 (in pin 34ef6147) gives a compile that runs out while lowering as `OutOfMemory`;
`compile_out_of_memory`, its call, its test and the `Internal("out of memory")` arm are gone. script:: and service::
tests pass (620), all of moqui-core's lib tests (1630).

## M1c: the idle release at 0.5 s (mr-moqui ef319839)

Release builds `work/r52/m1/moqui-1s` and `moqui-500ms` (mr-moqui 6304f480, and with `IDLE_RUNTIME` 500 ms),
`MOQUI_SCRIPT_STATS_FILE=... ./moq test-apps --nobuild` twice each, then `./moq test mr-mantle --nobuild` once each
(`idle-table.py`; the `stats-*.jsonl` files here). Every run passed (3410/3410 specs' features, 19/19 client).

| # | 1s-r1 heap MB / started / released | 1s-r2 heap MB / started / released | 500ms-r1 heap MB / started / released | 500ms-r2 heap MB / started / released |
|---|---:|---:|---:|---:|
| 0 | 75.5 / 162 / 96 | 76.9 / 146 / 78 | 58.2 / 305 / 238 | 56.9 / 522 / 444 |
| 1 | 70.1 / 174 / 133 | 69.8 / 175 / 134 | 57.0 / 447 / 389 | 56.2 / 377 / 310 |
| 2 | 65.4 / 264 / 206 | 61.2 / 266 / 210 | 56.7 / 522 / 444 | 55.3 / 471 / 412 |
| 3 | 55.9 / 265 / 187 | 58.6 / 265 / 187 | 50.6 / 533 / 494 | 52.1 / 540 / 500 |
| 4 | 34.2 / 35 / 0 | 34.2 / 35 / 0 | 33.6 / 35 / 0 | 31.8 / 47 / 21 |
| 5 | 30.4 / 71 / 21 | 15.0 / 20 / 0 | 11.1 / 16 / 0 | 15.2 / 23 / 0 |
| 6 | 29.7 / 48 / 21 | 1.6 / 3 / 0 | 1.6 / 3 / 0 | 1.6 / 3 / 0 |
| 7 | 1.6 / 3 / 0 | 0.0 / 0 / 0 | 0.0 / 0 / 0 | 0.0 / 0 / 0 |

1s-r1: max heap 75.5 MB, summed 362.9 MB, started 1022, released 664
1s-r2: max heap 76.9 MB, summed 317.4 MB, started 910, released 609
500ms-r1: max heap 58.2 MB, summed 268.9 MB, started 1861, released 1565
500ms-r2: max heap 56.9 MB, summed 269.1 MB, started 1983, released 1687

| | 1 s run 1 | 1 s run 2 | 0.5 s run 1 | 0.5 s run 2 |
|---|---:|---:|---:|---:|
| test-apps wall time | 279 s | 263 s | 258 s | 270 s |

mr-mantle alone: 1 s 65.2 MB heap_at_max, 291 started, 126 released, 332 s; 0.5 s 53.5 MB, 714 started, 573
released, 325 s.

Kept: the peaks fall by about 18 MB (largest process 76 -> 57 MB) and the suite time does not rise; runtimes started
roughly double (about 1900 against 960 over the suite).
