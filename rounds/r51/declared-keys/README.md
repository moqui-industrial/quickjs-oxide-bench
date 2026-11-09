# R51: declared shared keys (phase 3 reworked)

Phase 3 (fork b0ae1755) shared every key the embedder made (`NativeCx::key_from_latin1`, `key_from_units`). Map keys
from run-time data, such as a request's JSON or arbitrary field names, then piled up in the process's shared table,
whose atoms are never freed, until its cap. Fork branch `perf/declared-keys` takes that out. The image key-table sharing
stays. In its place:

- `Runtime::share_keys(texts)`: the embedder declares texts as the process's shared keys;
- `Runtime::set_share_atoms(bool)` and `sharing_atoms(f)`: every new atom is shared while the flag is set, for the
  embedder's start.

mr-moqui uses them in `OxideEngine`:

- **The start.** From the runtime's creation to the end of `finish_start`, everything is shared: `ec` and its
  members, the host table, the host objects, the shims, the helpers and the start code. It is the same in every runtime,
  and the flag is cleared before any run-time data.
- **The entity model.** Once a process, the entity names, full names, short aliases, field and alias names, and
  relationship short aliases are declared. The list is bounded by the model.

Keys made from run-time data stay the runtime's own and are collected as before. A fork test,
`runtime_map_keys_stay_out_of_the_shared_table`, covers a parsed map's keys, a computed key and a host's map keys.

**Runs.** mr-moqui master `2d0e1f29` with that change, the drop hook and the census print, in `../mr-moqui-r51`
(`p3-k3.sh`). The k1 and k2 rows are from `../shared-key-tables` (same mr-moqui commit).

## mr-mantle

| | k1 (image keys only) | k2 (every embedder key) | k3 (declared) |
|---|---:|---:|---:|
| workers' key entries in tables of their own | 304,733 of 416,046 | 128,844 of 419,528 | 18,933 of 417,420 |
| workers' most reserved: median | 2289 KiB | 2284 KiB | 2177 KiB |
| workers' most reserved: summed (23) | 54.9 MiB | 52.9 MiB | 52.0 MiB |
| `heap_at_max` | 79.1 MB | 65.3 MB | 74.0 MB |
| the shared table at the end | 28,281 atoms, 3.2 MB | 31,081 atoms, 4.3 MB | 34,525 atoms, 686k units, 5.7 MB |

`heap_at_max` is one snapshot, of what the workers held at that moment.

The shared table's growth over the run is in `shared-table-growth.txt`:

- **k3** starts at 11.6k atoms: the start and the model, bounded by the model. It grows only as new code images load,
  to 34.5k.
- **k2** starts at 1k and grows with the images and every key the host made, data keys among them.

**Spec results.** k3 failed the two date-dependent specs that k2 failed: AccountingCollections' instalment ageing
(9 days, not 10, with two skipped after it) and SupportCases' "Today". The run was past midnight UTC, and at this hour
the base fails the same two (`../shared-key-tables`).

## js_speed, a new thread (`cold-k3.txt`)

| | k0 (phase 2) | k2 | k3 |
|---|---:|---:|---:|
| engine start: allocations | 7,775 | 6,421 | 6,166 |
| engine start: bytes | 2,548,618 | 2,471,885 | 2,465,273 |
| first render: allocations | 16,269 | 16,247 | 15,769 |
| first render: js kept | 537,570 | 343,134 | 342,334 |
| after List html: reserved / live | 863 / 392 KiB | 812 / 368 KiB | 808 / 366 KiB |

The k0 and k2 columns are from `../shared-key-tables/cold-*.txt`. k3's engine start took 1.41 ms (min 1.39) in both
runs.
