# Round 33 notes

## Builds

- `target/profiling/bin/js_speed-base`: master 2cfc469d.
- `js_speed-r33a`: switches entity, leaf, this, keys, flush.
- `js_speed-r33b`: adds now.

## Variant runs

- `a/`: on, all, and each switch off, two runs each.
- `b/`: on, all, now.
- `table.py <dir> [variants]` prints each variant's better run.

## Profile, self time by layer (perf -F 4000, `layers.py`)

### walk itemList, 100 context maps

| Layer | Share |
|---|---:|
| engine core | 36% |
| alloc | 23% |
| fork API | 16% |
| bindings | 5% |
| framework | 5% |
| hash | 2.5% |

- **Engine core:** `Heap::bytes` 3.1%; `AtomTable::find` 2.1%; `intern_repr` 1.7%; `Vec<u16>` collect for `View::key` 2%.
- **Fork API:** `View::key` 2%, `Runtime::enter` 1.8%, `lower` 1.5%, `set_property_with_receiver` 1.2%.
- **Bindings:** `matches_host` 2.9%.

### 100 nowTimestamp

| Layer | Share |
|---|---:|
| engine | 25% |
| bindings | 10% |
| alloc | 9% |
| fork API | 8% |
| framework | 8% |

- **Engine:** `Heap::bytes` 4.4%.
- **Bindings:** `trampoline` 5.3%.
- **Framework:** `temporal_text` 1.6%, plus `basic_convert` through text (`i64` to `string`, split).

### walk an entity list, 100 cached rows

| Layer | Share |
|---|---:|
| engine | 23% |
| alloc | 19% |
| framework | 17% |
| fork API | 12% |
| bindings | 8% |

- **Engine:** `NativeCx::restore` 5.5%.
- **Fork API:** `lend` 5.4%. With `restore`, that is the lend around the localized `description` read, about 0.2 µs a row.
- **Framework:** `localize_field` and `read_localized` together about 4%.

## Found in the fork's engine

**`Heap::bytes` on every allocation under a cap.**
- `always_slow()` is true whenever `limits.max_bytes` is set, and Moqui sets 64 MiB.
- Every safepoint then takes `safepoint_slow`, which sums `bytes()` (14 arenas and tables) and `growth_bytes()`. That is 2 to 5% of every row.
- **Fix:** a cap headroom computed at the slow path. Reserved bytes grow only by arena steps, which is at most what was allocated since plus one step per arena. The fast path then checks `allocated + nominal < min(threshold, cap_limit)`. Round 34.

## Moved

**The in-place flush comparison** (compare under the stack's borrow, with no clone) needs the fork to say whether an object is ordinary (no Proxy traps, no exotic hooks) without running code: no API does. It goes to Round 34, with an `is_ordinary_object` API.
- **Measured cost:** 10 noop service calls take 387 µs with itemList tracked and 93 µs without. That is about 29 µs a flush of a 100-map list: the clone, then `matches_host`.

## Round 34 candidates found here

- the cap headroom fast path (engine);
- `is_ordinary_object`, then the in-place flush;
- `View::key` with the Latin-1 path, or pre-interned keys;
- a localized field read that skips the lend when the l10n cache has it (bindings and framework);
- `PropertyKey::as_index` (`ListValues` still allocates one string a `list[i]` for `to_js_string` of an index key).
