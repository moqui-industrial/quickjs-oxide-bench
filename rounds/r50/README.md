# Round 50: tiers 0 to 2

Profiling2 §5's tiers 0 to 2, 2026-11-08. The results are in mr-moqui's `plans/Profiling2.md` ("Round 50: tiers 0 to
2") and in the commit messages of the fork's merges (c83824fd to 1cdb77e2) and of mr-moqui c497d59a to 42522af6.

The raw outputs were under mr-moqui's `target/profiling/r50/` and were lost to a `cargo clean`. They were:
- `base/`: js_speed at mr-moqui c497d59a on the fork's 7cf1f530, 16 codegen units, two runs;
- `c1/`: one codegen unit and thin LTO, build times;
- `a1`..`a7`, `b1`..`b4`, `box-*`, `c2`..`c4`: each item's binary and rows, with `perf stat -e instructions:u`
  (6 batches less 1);
- `final/`: the quiet pass, base against mr-moqui 361f4c8e on the fork's 362cf9ed, with `table.md`, and the
  `MOQUI_SCRIPT_STATS_FILE` lines of test-framework and test-apps.

The base can be rebuilt from mr-moqui c497d59a with the 7cf1f530 pin.
