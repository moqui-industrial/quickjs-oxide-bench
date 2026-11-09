> The workspace README of `../oxide-bench`, before it became this repository (2026-11-08). Kept as it was; the
> current one is `../README.md`.

# oxide-bench

The measurement workspace for the quickjs-oxide fork (`../quickjs-oxide`, `github.com/moqui/quickjs-oxide`) and for the
engine rows of mr-moqui's [Profiling2](../mr-moqui/plans/Profiling2.md) (§2 How to measure; the round logs are in
`plans/archive/Profiling.md` and `plans/archive/Script-Engine-Oxide.md`). Nothing here is in a repository; it is kept on this machine.

## The fork's Sweep (upstream's gate, run before a fork branch merges to the fork's `main`)

- `base/` is a detached worktree of the fork, used to run upstream's `scripts/benchmark/bench.py`. `base-main/` is
  another one, at an older fork `main`. The `*-target/release/qjs` binaries are the base engines:
  - `base-target`: upstream's 3a9ceb96;
  - `base-main-target`: the fork's dd26f7ae;
  - `base-dc5b-target`: the fork's dc5b0c5d, the base of Round 32's F4 Sweep.
- **Before the next Sweep**, build a base from the fork's current `main`:
  1. `git -C ../quickjs-oxide worktree add ../oxide-bench/base-<sha> <sha>`;
  2. `cargo build --release -p quickjs-oxide-cli --bin qjs --target-dir ../oxide-bench/base-<sha>-target`.
- **The candidate** is the branch's worktree, `../quickjs-oxide-<branch>`, built with `cargo build --release -p
  quickjs-oxide-cli --bin qjs`.
- **Run:** `run-sweep-integ5.sh` is the template. It waits until no cargo, rustc or moqui process runs (a quiet window:
  nothing else builds or tests), then runs `bench.py sweep` and `bench.py memory` over `suite-matrix/manifest.json`. It
  writes `sweep-<tag>/summary.md` and `memory-<tag>.log`.
- **Gates:**
  - each of the eight V8 v7 programs at most ×1.02 base instructions;
  - `run_at` under 16384 bytes;
  - the memory geometric mean is reported.
- **Other checks:**
  - `gates.sh <worktree>` runs upstream's CI steps (tests, clippy, fmt, gc-stress).
  - `t262-*.log` are the Test262 runs.
- **Merging:** a fork branch merges `--no-ff` into the fork's `main` with the Sweep's numbers in the message. The user
  pushes the fork's `main` before mr-moqui. Then mr-moqui's `Cargo.toml` rev is bumped and `cargo update -p
  quickjs-oxide` is run. While the fork's `main` is unpushed, `cargo` resolves it from the local clone with:
  ```
  CARGO_NET_GIT_FETCH_WITH_CLI=true GIT_CONFIG_COUNT=1 \
    GIT_CONFIG_KEY_0=url./home/jonesde/work/moquiwork/quickjs-oxide.insteadOf \
    GIT_CONFIG_VALUE_0=https://github.com/moqui/quickjs-oxide
  ```
- **Upstream:** no upstream issues or PRs without asking the user.

## The Mantle operations against a Postgres 200 µs away (`mantle-pg/`)

Profiling Rounds 26, 27 and 32. It needs a release build of mr-moqui (`./moq build --release`) and the `moqui-pg18`
docker container (`--cap-add NET_ADMIN`). Never touch the other containers.

1. `mantle-pg/setup.sh <mr-moqui dir>` loads every component's data into the template database `p_tpl` and adds the
   delay.
2. `mantle-pg/run.sh <mr-moqui dir> <engine> <tag> <out dir>`, alternating the engines with two runs each (rq1, ox1,
   rq2, ox2).
3. `mantle-pg/table.py <out dir> rq1,rq2 ox1,ox2` gives the median ms a call of the nine services and their totals.
4. `mantle-pg/teardown.sh` removes the delay and the databases and stops the container.

## Round 32's raw data (`round32/`)

- The census files of the Mantle runs.
- The `js_speed` output, two runs of each engine.
- The `MOQUI_SCRIPT_STATS_FILE` lines of `./moq test-apps` under each engine, with each process's heap peaks.
