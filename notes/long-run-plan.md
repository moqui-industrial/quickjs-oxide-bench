# The long run: profiling and optimization iterations, about 12 hours

It starts after Round 34 is committed and `git pull` merged.

## An iteration (about 45 to 75 minutes)

1. **Pick** two to four changes from the backlog below, by what the last profile showed.
2. **Write each behind a temporary switch** (`MOQUI_OXIDE_OFF`, `script/oxide/opt.rs`).
   - A fork change goes on a branch of its own from the fork's local `main`.
   - Then it merges into the run's integration branch (`integ/moqui-long`). The bindings build against that branch
     through a `--config patch` on the command line; no committed file names the path.
3. **Tests while working**, in this order:
   - the fork's tests for the touched area (`embedding_api`, `host_exotic`, core lib);
   - mr-moqui's `script::` and `screen::` unit tests;
   - the specs of what was touched.
4. **One release build, one timing.** `js_speed` all on, against the last commit's binary (or `MOQUI_OXIDE_OFF=all`),
   two runs, limited to the rows the changes touch (`JS_SPEED_ROW`). No run with each switch off (changed 2026-11-08):
   each change's own number is deferred to the final acceptance (below).
5. **A profile** (`perf record -F 4000`, `layers.py`) of the rows that moved most, or that lose most to QuickJS. It
   picks the next iteration's changes.
6. **Record** in `roundNN/notes.md`: each change's own µs and allocations, and the layer split.

## Proved locally, then committed (changed 2026-11-08)

No fork Sweep or memory runs, no `gates.sh`, no Mantle runs and no full-suite runs (`test-framework`, `test-apps`).
An iteration is proved by its own `js_speed` variants, a profile, the touched unit tests (mr-moqui's `script::`,
`screen::`, entity) and the fork's API tests (`embedding_api`, `host_exotic`, the core lib tests touched). Then:
- the switches folded, clippy clean on the touched crates;
- the fork's branches merged `--no-ff` into its local `main`, the rev bumped (`insteadOf` to the local clone);
- A round's section (plans/Profiling2.md now holds the status; new rounds go there), and the commit. Commit every iteration or two; no pushes, no upstream issues or PRs.

## The final acceptance: done (Profiling Round 48, `accept48/`)

- **Done in Round 48:**
  - the fork's `gates.sh` and Sweep on `main` 7cf1f530 against 8635ecb5, which covers every branch merged since
    Round 34;
  - the memory sweep;
  - the full suites under both engines;
  - Mantle two runs of each engine;
  - `js_speed` before (680c2ee5) and after.
- **Not measured on their own:** Round 36's `katom`, `eqs` and `spk`. Each round's changes were measured as A/B builds
  when they went in, so these switches were not rebuilt. They are inside the before/after totals.

## Rules learned in Rounds 33 and 34
- **The fork patched in:** `target/profiling/patch.sh <worktree> <cargo args>` (restores `Cargo.lock`). For
  `cargo clippy` the `--config` must come after the subcommand, as `cargo-clippy` drops a leading one.
- **Stopping a job:** `kill <pid>` from `pgrep -x` or `ps`, never `pkill -f` (it matches the shell running it).

- **Nothing builds while a timing or a Sweep runs.** Every timing script waits for no cargo, rustc or moqui first.
  Builds go only in the gaps.
- **A wait on another job** waits on its PID (`kill -0`), never `pgrep -f` on a script's name (it matches the
  launcher's own command line).
- **`Cargo.lock`:** restore it after every patched build (`target/profiling/Cargo.lock.r33`, renewed at each commit
  point).
- **Large files:** binaries and profiles go under `target/profiling`; old binaries are deleted; `df` and `free` are
  checked at each commit point.
- **A change that fails tests** is fixed within the iteration, or reverted and recorded, and the run goes on.
- **Never touch** the other moqui on 8080/8443/2222, or the Docker containers other than `moqui-pg18`.

## The backlog, by expected payoff (re-ranked by each profile)

1. **A Release flush without the copy.**
   - Today a Release keeps its own copy of the stack's value for `readopt`.
   - A stack frame's write generation (or a value's stamp) would let `readopt` know the stack is unchanged without the
     copy.
   - Rows: the service calls with `itemList` tracked (290 µs over the untracked row), `sri` Release methods, Mantle.
2. **Strings in one copy (fork).**
   - A `Value` from `&str` lowered straight onto the heap (`NativeCx::new_string`).
   - A borrowed read of a JS string's text, in place of `to_utf8_lossy`.
   - Rows: `to_js` of every map field, the `sri.write` chunks, and the screens.
3. **Plain objects built in one step (fork).**
   - `create_data_property` (no `[[Set]]`, no receiver lowered), or `new_object_from(&[(key, value)])`.
   - A slice form of `new_array_from_values`.
   - Rows: walk itemList, templates, List screens.
4. **`PropertyKey::as_index` (fork),** so a `list[i]` of an entity list makes no string.
5. **A bare name in one hook (fork):** a host exotic class answers `has` and `get` in one dispatch. Rows: bare-name
   reads and writes (about 10% estimated).
6. **`apply#Settlement` and `get#PaymentFinanceDetail`** (×1.12 and ×1.10 of QuickJS): a profile of the Mantle run's
   oxide side, to see which binding path they take.
7. **Wrappers kept across runs** for tracked maps and lists (weak handles in the fork). Larger; only if the profiles
   still show conversion at the top after 1 to 3.
8. **The heap** (Phase 3's missed gate, 91 to 118 MB a worker):
   - why about 30 runtimes a process, and whether the idle ones can shed;
   - the arenas' interior free space (fork).

   Measure with `MOQUI_SCRIPT_HEAP_LOG` before choosing.
9. **The allocator:** what the server uses in production builds, and whether the bindings' small, short-lived
   allocations would gain from a thread-local arena or a different global allocator. Measure first.

## What the run leaves

- Commits in mr-moqui at each commit point, with the fork's `main` merged locally and the rev bumped; nothing pushed.
- `../oxide-bench/round35..NN/`: the raw logs, profiles' splits and notes.
- plans/Profiling2.md updated for the next session.
- A short report: each change's effect, the rows against QuickJS, and what was tried and dropped.
