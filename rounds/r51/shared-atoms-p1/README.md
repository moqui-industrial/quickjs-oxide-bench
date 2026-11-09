# R51: shared atoms, phase 1 (the builtin atoms)

Fork branch `perf/shared-atoms` against fork `1cdb77e2` (main, pushed). The design is the fork's
`docs/shared-atoms.md`. Phase 1 puts the atoms interned while a runtime is created into one process-wide table
(`core/src/heap/shared.rs`): the realm's names and the builtins' properties, 512 atoms. A later runtime finds them
there and imports their ids into its own atom table.

js_speed was built from mr-moqui `f72fc796` (pinning 1cdb77e2) in `../mr-moqui-r51`. The base build has no patch
path set; the candidate uses `--config 'patch...quickjs-oxide.path="../quickjs-oxide-shared-atoms"'`. Lane C was
building at the same time, so the evidence is allocation counts, bytes and `instructions:u`, not wall time.

## Memory (`cold.txt`; `JS_SPEED_ONLY=cold`, run twice, identical)

| | base | phase 1 |
|---|---:|---:|
| engine start: allocations | 9,277 | 8,747 |
| engine start: bytes | 2,883,698 | 2,674,561 |
| engine start: js kept | 880,333 | 812,956 |
| then first render (List html): js kept | 613,291 | 484,159 |
| a new thread's runtime after its first script: reserved / live | 860 / 398 KiB | 795 / 373 KiB |
| the same after List html | 1132 / 520 KiB | 1121 / 495 KiB |

A fresh fork runtime: one eval and a collection, after one runtime was already made in the process. Probe:
`tests/zz_probe.rs`, not committed.

| | base | phase 1 |
|---|---:|---:|
| reserved | 171,176 B | 125,463 B |
| used | 107,864 B | 82,767 B |
| string records | 514 | 2 |

## Atom census (`census-js_speed.txt`, `QJS_ATOM_CENSUS=1`)

| Thread | Atoms | Shared | Builtin |
|---|---:|---:|---:|
| main thread, after every row | 4187 | 512 | 512 |
| a new thread, after its first script and screen | 3064 | 512 | 512 |

The rest of each thread's atoms are image code (989 and 1395) and constants (1417 and 797): these are phase 2.

## Instructions per call (`rows-10000.txt`)

These are js_speed rows at 10,000 calls a batch, taking 6 batches minus 1, two runs each.

| Row | base | phase 1 | |
|---|---:|---:|---:|
| walk itemList | 1,078,839 | 1,088,873 | +0.9% |
| 100 reads of item.name | 280,463 | 281,978 | +0.5% |
| JSON stringify + parse | 1,448,025 | 1,466,000 | +1.2% |
| $esc | 759,661 | 769,082 | +1.2% |
| 1000 string concatenations | 1,774,074 | 1,827,023 | +3.0% |
| split('') + charAt | 1,230,562 | 1,231,801 | +0.1% |
| 1000 numbers to text | 2,899,459 | 2,947,163 | +1.6% |
| JSON.parse of the locked snapshot | 136,466 | 138,746 | +1.7% |
| 100 objects made | 507,462 | 508,221 | +0.1% |
| 10 cached entity finds | 515,214 | 514,817 | 0.0% |
| regexp scan | 2,896,933 | 2,950,789 | +1.9% |

The rows that make many strings cost 1 to 3% more. In `concat.js` (the concatenation row under `qjs`, 3M iterations)
the extra is about 49 instructions an iteration, +3.2%. A sampled profile puts it in glibc's `malloc` (+30% of its
samples), not in the engine's code. Both runs do the same 273 collections, but the reserved heap differs (1651 KiB in
the base, 2002 KiB in phase 1), so the allocator's state differs. Earlier candidates bought down the engine's own share:
- the shared record's read out of line;
- `Strings::alloc` and the hot accessors inlined;
- the collector's rope paths reading the arena directly.

A `Heap::string_repr` accessor with one shared test measured no better and was dropped.

## The V8 v7 programs (`v8-v7.md`; `bench.py run`, 2 repetitions, ABBA, instructions)

All are within the ×1.02 gate. The geometric mean is 1.0029.

The worst is splay at 1.0120. `--gc-stats` shows 11 collections where the base does 10: its live bytes no longer
count the builtin atoms, so the budget falls differently.

## Checks

- **Tests:** core, `embedding_api`, `host_exotic`, `reentry`, `code_images`, `host_compile` and the root lib tests pass, and so does core under
  `gc-stress`. The new tests are:
  - a text keeps one id in each heap (a runtime's own atom made before the text was shared stays);
  - eight threads adding the same texts get one id each;
  - runtimes made on eight threads at once share the builtin names.
- **Lint:** `cargo fmt --all -- --check` and the five clippy commands of CI with `-D warnings` pass.
- **Test262:** the focused replay matches (6814 pass of 6844).
