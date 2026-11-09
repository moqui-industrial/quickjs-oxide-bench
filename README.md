# quickjs-oxide-bench

Benchmark tools and results for [moqui/quickjs-oxide](https://github.com/moqui/quickjs-oxide), the script engine of
[mr-moqui](https://github.com/moqui/mr-moqui). It holds the scripts, notes and text results of the performance rounds;
binaries, worktrees and benchmark sources stay out of git (`work/`).

Check it out next to the fork and mr-moqui:

```
moquiwork/
  quickjs-oxide/         the fork
  quickjs-oxide-bench/   this repository
  mr-moqui/
```

The status, the open items and how mr-moqui measures the engine are in mr-moqui's
[plans/Profiling2.md](https://github.com/moqui/mr-moqui/blob/master/plans/Profiling2.md) (§2 How to measure). The round
logs are in its `plans/archive/` (Profiling.md, Script-Engine-Oxide.md).

## What is here

| Path | What |
|---|---|
| `tools/gates.sh <worktree>` | the fork's CI steps on a worktree: fmt, tests, clippy, gc-stress, the pilot suite under gc-stress |
| `tools/run-sweep.sh TAG BASE CAND` | the fork's Sweep and memory runs of a candidate `qjs` against a base, in a quiet window |
| `tools/mantle-pg/` | the nine Mantle operations against a Postgres 200 µs away: `setup.sh`, `run.sh`, `table.py`, `teardown.sh` |
| `tools/ngrun/` | runs a script on quickjs-ng through rquickjs 0.14, the engine Moqui embedded before oxide |
| `sweeps/` | Sweep and memory results by tag (integ, integ2/3/5, r34-cap, r34-key, host-exotic, reentry), with their run scripts |
| `gates/`, `test262/` | `gates.sh` and Test262 logs of the fork branches |
| `rounds/rNN/` | a Profiling round's scripts, notes, tables and logs (R32 to R47; `r48-accept`, the Phase 4 acceptance; `r49-phase4`, the idle release and heap runs) |
| `rounds/f4/`, `rounds/alloc-probes/` | the F4 probes (concat, JSON, escape, template) and the allocation probes, scripts and inputs |
| `notes/` | the long-run plan and the workspace's old README (`../oxide-bench`, before this repository) |

Scripts under `rounds/` and `sweeps/` are kept as they ran: some name the old `../oxide-bench` paths.

## Working files (`work/`, not in git)

- **Base engines for the Sweep:** a detached worktree of the fork at the base commit, and its release `qjs`:
  ```
  git -C ../quickjs-oxide worktree add ../quickjs-oxide-bench/work/base-<sha> <sha>
  cargo build --release -p quickjs-oxide-cli --bin qjs --target-dir work/base-<sha>-target
  ```
  The candidate is the branch's worktree, `../quickjs-oxide-<branch>`, built with `cargo build --release -p
  quickjs-oxide-cli --bin qjs`.
- **The suites:** `work/suite-matrix` (the 37 V8 v7, Octane and AWFY programs) and `work/suite-pilot1` (`--pilot 1`),
  built by `bench.py suite build` from the three pinned sources, as the fork's
  `docs/performance/benchmarking.md` shows.
- **A round's binaries and traces:** `work/rNN/` (perf data, heaptrack files, copies of `js_speed`). Text results go in
  `rounds/rNN/` and are committed. Nothing goes under mr-moqui's `target/`, which `cargo clean` removes.

## Rules

- **Gates** for a fork branch: each of the eight V8 v7 programs at most ×1.02 of the base's instructions, and `run_at`
  under 16384 bytes; the memory geometric mean is reported.
- **Quiet:** nothing else builds or tests while a timing runs; run two of each and compare at the better one.
- **Merging:** a fork branch merges `--no-ff` into the fork's `main` with its numbers in the message; the fork is pushed
  before mr-moqui's pin moves. While `main` is unpushed, cargo resolves it from the local clone with:
  ```
  CARGO_NET_GIT_FETCH_WITH_CLI=true GIT_CONFIG_COUNT=1 \
    GIT_CONFIG_KEY_0=url.<path to>/quickjs-oxide.insteadOf \
    GIT_CONFIG_VALUE_0=https://github.com/moqui/quickjs-oxide
  ```
  A single branch can also be measured from mr-moqui with
  `cargo --config 'patch."https://github.com/moqui/quickjs-oxide".quickjs-oxide.path="../quickjs-oxide-<branch>"'`;
  no committed file names a path.
- **Test262** (`scripts/test262/test-test262.sh`) refuses to run with `GIT_EDITOR` set; run it under
  `env -u GIT_EDITOR`.
- No upstream issues or pull requests without asking.
