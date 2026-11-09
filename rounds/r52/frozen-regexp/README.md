# R52 F1: a frozen but untouched `RegExp.prototype` stays pristine

Fork branch `perf/frozen-regexp` against fork main `34ef6147`. The cause: the sandbox's lockdown freezes
`RegExp.prototype`, which gives it a new shape. The fast paths compared the prototype's shape with the one the flag
cache was recorded for, so every `replace` in the locked template took the generic `@@replace`.

The fix: before a fast path checks the shape, `refresh_flag_cache` reads the shape the cache holds for (its own small
cell). When the prototype's shape differs, `recorded_again` records the cache again for the new shape, provided that:
- the eight flag properties are still accessors whose getters are the intrinsics;
- `exec` and the five protocol methods are still data properties.

The fast paths then compare the values (the getters, `exec`) as before. A replaced `exec` or flag getter, or a flag
made a data property, still takes the generic path.

js_speed was built from mr-moqui `fb0e5f78` in `../mr-moqui-r52f`.
- **Base:** the committed pin, `34ef6147`.
- **null:** the same fork commit through the `--config` patch path.
- **f1e:** the branch through the same patch path.

## The rows

`instructions:u`, 10,000 calls a batch, 6 batches less 1, three runs each (`rows-instructions.txt`):

| Row | null | F1 | |
|---|---:|---:|---:|
| fancy, locked down (a snapshot) | 1,093,610 / 1,092,182 / 1,092,914 | 669,042 / 664,159 / 671,761 | -38.9% |
| fancy, trusted (live context) | 771,225 / 773,272 / 769,382 | 775,151 / 777,061 / 771,644 | +0.4% (within the range) |

The default js_speed run (`template-rows.txt`):

| Row | null | F1 |
|---|---:|---:|
| locked: µs/call | 65.08 | 39.99 |
| locked: allocations | 350.4 | 228.4 |
| locked: bytes | 14,790 | 14,180 |
| trusted: µs/call | 50.39 | 50.67 |
| trusted: allocations | 304.5 | 304.5 |

The first version returned the whole cache by value from a checking function, which cost the trusted row +1.2%. The
merged one checks a small shape cell and leaves the original copies as they were. The base binary (git dependency)
and null (patch path) agree within 0.2%.
