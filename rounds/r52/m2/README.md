# Round 52, lane M2: the binding rows

mr-moqui worktree `../mr-moqui-r52`, branch `r52-bindings`, from master ef319839. The fork moved during the lane (F2,
F3), so every build here is against one snapshot of the fork's local main, ddba97fe (`git archive` into
`work/r52/m2/fork-ddba97fe`), through `--config patch...path`. Binaries and raw outputs are in `work/r52/m2/`
(`build.sh`, `base/`, `m2a/`, `perf-a-*`).

`perf-rows.sh <binary> <out dir> <a|b>`: each row alone (`JS_SPEED_ONLY`, `JS_SPEED_ROW`) at 20000 calls (services
10000), `perf stat -e instructions:u` with 1 batch and 6, instructions per call = (six - one) / (5 x calls), and the
row's js_speed line from the six-batch run (allocations per call exact). Set `a` is M2a's rows, `b` M2b's.

## M2a: cached finds

- A chained builder call changes the find in place and returns the same object (`Ret::This`), as Java's `EntityFind`
  builder returns `this`; no new HostObject and FindState per call.
- `list()`, `one()` and `count()` leave the find as it was, so it runs again, as in Java.
- `list()`, `one()` and `iterator()` are leaves. A hit of the shared entity cache is answered without lending the
  engine (`EntityFind::list_from_cache` / `one_from_cache`). Any other find runs with the engine lent: a miss, a sim,
  a transaction-cache frame that wrote the entity, a find the cache does not answer, an entity defined at run time, a
  find one that narrows to its key, or authorization filters that may apply (the new `entity_filters_apply` hook:
  a context entered, not `moqui.*`, authz on and not disabled). The cache is read before the artifact is pushed, so a
  miss pushes nothing and counts no hit twice.

Base `work/r52/m2/base` (ef319839), M2a `work/r52/m2/m2a`; both on fork ddba97fe. `perf-a-base{1,2}.txt`,
`perf-a-m2a{1,2}.txt`.

| row | allocs base | allocs M2a | instr/call base (2 runs) | instr/call M2a (2 runs) | us/call base | us/call M2a |
|---|---:|---:|---:|---:|---:|---:|
| 10 cached entity finds | 576.2 | 486.2 | 517,168 / 518,207 | 458,268 / 460,341 | 44.4-44.7 | 39.3-39.7 |
| walk an entity list, 100 cached rows | 2340.0 | 2332.0 | 1,905,663 / 1,908,333 | 1,895,826 / 1,893,907 | 153.1-153.3 | 154.5-155.3 |
| entity-find-one, cached | 53.0 | 44.0 | 56,255 / 52,098 | 47,502 / 50,616 | 4.70-4.77 | 4.33-4.37 |
| find#Cached (10 cached finds) | 657.2 | 567.2 | 712,235 / 714,582 | 656,131 / 656,697 | 57.8-58.2 | 52.4-55.6 |

Each find saves 9 allocations and about 5,800 instructions. The list walk is the 100 row reads; its one find saves the
same, which is under 1% there.

Tests: moqui-entity lib (359 passed), moqui-core lib (1631 passed), clippy -D warnings on both crates. Specs on a
release `moqui` built from a664e02e (pinned fork): mr-boss alone 1272/1272; mr-mantle with mr-boss in one run
3216/3219, the three failures mr-boss specs that pass alone and in the mr-boss run (spec interference in one
database), and ProductsMethods over 15 s only under the build beside it.

mr-moqui commit: a664e02e.
