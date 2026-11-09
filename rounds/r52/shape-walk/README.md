# R52 F2: a plain object walked by its shape, an Array by its elements

Fork branch `perf/shape-walk` against fork main `570f5b59` (F1).

## The change

- **Core:**
  - `Heap::plain_data_entries` (and `NativeCx`'s) reads a plain object's own data properties from its shape and slots
    into a buffer, in `[[OwnPropertyKeys]]` order: the strings, then the symbols.
  - It reads no list of keys and makes no descriptor or per-key `Get`.
  - It returns `false` for anything else: an object that is not ordinary, has elements or inherits from another
    prototype; an accessor; a pending property; an atom that spells an array index.
  - `Heap::dense_array_elements` copies a dense Array's values, `0` to its length, and returns `false` for a hole or a
    sparse Array.
- **API:**
  - `visit_plain_own_data` now reads through `plain_data_entries`; its contract and its `None` cases are unchanged.
  - New `visit_plain_own_text`: the same with each key's text borrowed, so no key is lifted. It is `None` also when the
    object has a symbol key.
  - New `visit_dense_array`: an Array's elements shown one at a time. A string is borrowed, a callable marked and the
    rest lifted, with no `Vec<Value>` of lifted elements.
  - The buffers are kept on the runtime's `Shared` between calls.

mr-moqui is unchanged for these rows: its `tracked.rs` `matches_in_place` and `convert.rs` `to_host_in` already call
`visit_plain_own_data`. Using `visit_dense_array` and `visit_plain_own_text` there is M2b.

## The rows

js_speed was built from mr-moqui `fb0e5f78` in `../mr-moqui-r52f`, with both sides through the `--config` patch path.
The base is fork main `570f5b59`.

`instructions:u` per call, 2000 calls a batch, 6 batches less 1, three runs each (`rows-instructions.txt`):

| Row | base | F2 | |
|---|---:|---:|---:|
| walk itemList, 100 context maps | 1,088,293 / 1,108,508 / 1,102,164 | 948,044 / 955,515 / 967,691 | -13.0% |
| value `itemList.length` (100 maps) | 1,073,228 / 1,052,517 / 1,041,763 | 900,006 / 919,128 / 960,520 | -12.2% |
| 10 noop service calls, itemList tracked | 3,454,543 / 3,422,403 / 3,444,707 | 3,163,037 / 3,168,476 / 3,133,087 | -8.3% |

The default run (`rows-allocations.txt`):

| Row | base: µs/call, allocations, bytes | F2: µs/call, allocations, bytes |
|---|---|---|
| walk itemList | 67.52, 706.4, 31,954 | 57.58, 406.4, 25,546 |
| `itemList.length` | 67.36, 706.4, 33,211 | 56.60, 406.4, 26,277 |
| noop service calls, itemList tracked | 199.94, 1931.4, 127,638 | 176.64, 1331.4, 114,838 |
