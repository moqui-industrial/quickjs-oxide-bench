# Round 35 (long run, iteration 1)

Proved locally only (2026-11-08 change): js_speed switch variants, profiles, touched unit tests, fork API tests.

Fork branch `perf/plain-objects` (worktree ../quickjs-oxide-plain, from main 765afa3f):
- `Js::new_object_from`, `plain_own_data`, `dense_array_values` (6823efc2)
- `PropertyKey::as_index` (58bd5108)
- then: `InitValue` (Rust text made a heap string in one copy) for `new_object_from` and `new_array_from_inits`;
  `Scope::arg_text`.

Bindings switches (`MOQUI_OXIDE_OFF`):
- `rel`: a Release flush notes the stack's value by a 64-bit fingerprint (order-free for maps, as `java_equals`), not a
  copy; `readopt` compares prints. In-place compare for Release too.
- `obj`: maps made by `new_object_from`; plain objects and dense arrays read by `plain_own_data` /
  `dense_array_values` in `to_host` and `matches_in_place`.
- `idx`: entity list `list[i]` by `PropertyKey::as_index`.
- `str` (build 2): map and list text by `InitValue::Text`; text arguments by `Scope::arg_text`.

Profile before (r35a, Round 34 + rel): walk itemList self time engine core 25%, fork API 17%, alloc 9%, bindings 6%;
Single.qvt (script thread) engine core 43% (run_at 11%), fork API 10%, alloc 10%; List.qvt engine core 60% (run_at
24%). Bare names already beat QuickJS (376 vs 415 us), so the one-hook bare name is dropped from the backlog.
