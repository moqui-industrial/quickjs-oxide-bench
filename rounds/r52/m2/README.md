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

## M2b: walk itemList (mr-moqui ec0a1398)

Uses F2's visitors (fork c64d537d, in the ddba97fe snapshot): `tracked.rs` `matches_in_place` visits an array's
elements in place (`visit_dense_array`; text and scalars compared there, objects walked after) and a map's keys by
their text (`visit_plain_own_text`, no key lifted); `convert.rs` `to_host_in` converts an array's text and scalars
in the visit and copies a map's keys from their text. A symbol key, a sparse array, a function or text against a host
value shown as text goes the old way. mr-moqui needs the pin moved to a fork main with F2 to build this.

M2a `work/r52/m2/m2a` (a664e02e) against M2b `work/r52/m2/m2b` (ec0a1398), both on fork ddba97fe; `perf-b-*.txt`.
M2a run 1's walk itemList (1,019,426) is an outlier; the table uses both runs.

| row | allocs M2a | allocs M2b | instr/call M2a (2 runs) | instr/call M2b (2 runs) | us/call M2a | us/call M2b |
|---|---:|---:|---:|---:|---:|---:|
| walk itemList, 100 context maps | 406.9 | 406.6 | 1,019,426 / 955,095 | 934,112 / 937,828 | 57.5-60.1 | 54.4-54.8 |
| value `itemList.length` (100 maps) | 407.0 | 406.7 | 909,447 / 912,044 | 889,636 / 888,173 | 55.9-56.0 | 53.2-53.3 |
| 10 noop service calls, itemList tracked | 1332.0 | 1331.7 | 3,179,078 / 3,187,832 | 3,142,565 / 3,153,544 | 167.5-168.6 | 162.5-164.6 |
| iterate 100 context maps with if and set | 1897.4 | 1675.0 | 3,571,394 / 3,569,926 | 3,428,713 / 3,430,998 | 241.0-244.2 | 230.6-232.8 |

### The profile (`profile-walk-itemlist.txt`)

A frame-pointer build of the M2b source (`work/r52/m2/fp`), `perf record -F 999 -g` on walk itemList alone. The read
of `itemList` is now the larger part:

- `to_js_at` 52% inclusive. Of that, the fork's `ExoticScope::new_array_from_inits` is 36%: `View::object_from`
  (32%) makes each map's object with `core.new_object()` and then a `define_own_property` per property, with a full
  descriptor (`NativeCx::define_own_property` 11%, `ordinary_define` 9%), plus a new string record per text value
  (`alloc_string_record` 7%, `StringRepr::from_text` 5%).
- `to_init` 13%, with `OxideEngine::key` 5% (a key per property, for 100 maps with the same keys).
- The end-of-run compare (`tracked::flush`, `matches_in_place`) is 24%. GC (`Heap::collect`) is 10%.

Fork follow-up for lane F: `object_from` for an `InitValue::Object` could append data properties to a fresh ordinary
object by shape transitions (or one shape per key list, as JSON.parse builds objects) instead of
`define_own_property` per property. On the mr-moqui side, `to_init` could reuse the keys of the previous map in a
list when they are the same.

Tests: moqui-core lib (1632 passed, with a new oxide test of lists and maps compared and converted in place); clippy
-D warnings on moqui-core with the fork patch.
