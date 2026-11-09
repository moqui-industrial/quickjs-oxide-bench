# R51: test-apps heap peaks, the declared keys against the tree

The question: the largest `./moq test-apps` process's `heap_at_max` was 76.6 and 77.0 MB on mr-moqui `1a0f6f0e` with
the pin locally at fork `34ef6147` (the declared keys; `../../work/r51/final-dk`), over the 73 MB gate. R51's phase 2
run (fork `3c741ee8` on mr-moqui `ca9d2f83`, before the localization merge) peaked at 68 MB.

The base: mr-moqui `2d0e1f29` (origin/master before `1a0f6f0e`) with its committed pin, `3c741ee8`. It ran in a
detached worktree with the six components (mr-boss, mr-home, mr-l10n, mr-mantle, mr-marble, mr-pass) as worktrees of
their current `HEAD`s. `runtime/install` and `runtime/cert` were links to the main tree's, `.env` was a copy, and the
target dir was its own. The command was `MOQUI_SCRIPT_STATS_FILE=... ./moq test-apps`, run twice. Both runs passed
3410/3410 and 19/19.

## Per process (`heap_at_max`, MB; the processes in the stats files' order)

| # | base run 1 | base run 2 | 34ef6147 run 1 | 34ef6147 run 2 | main thread's peak: base 1 / 2 | main thread's peak: 34ef6147 1 / 2 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 80.8 | 80.6 | 76.6 | 77.0 | 36.7 / 36.8 | 35.8 / 36.5 |
| 1 | 56.3 | 55.6 | 55.9 | 51.5 | 37.9 / 44.2 | 45.5 / 45.2 |
| 2 | 57.7 | 62.5 | 63.1 | 60.1 | 36.8 / 39.6 | 39.3 / 39.4 |
| 3 | 68.9 | 73.4 | 71.0 | 71.5 | 43.2 / 44.7 | 42.3 / 36.7 |
| 4 | 36.0 | 0.0 | 0.0 | 0.0 | 10.0 / – | – / – |
| 5 | 1.7 | 1.7 | 1.6 | 1.6 | 1.6 / 1.6 | 1.1 / 1.1 |
| 6 | 36.8 | 37.2 | 33.9 | 33.4 | 6.7 / 6.7 | 4.7 / 4.7 |
| 7 | 35.6 | 16.8 | 13.0 | 13.8 | 10.6 / 2.2 | 1.9 / 1.9 |

Base run 1 started its client-serve processes in another order: its process 4 ran 14,705 actions and its process 7
ran 15,082, where every other run has 0 and about 385.

## What it shows

The largest process, process 0 (89.8k actions), peaks at 80.6 to 80.8 MB on the base and at 76.6 to 77.0 MB with the
declared keys. The declared keys lower it by about 4 MB: its workers' share at the peak is 38.8 MB in base run 1 against 35.3 and 35.5
MB. So the gate miss comes from the tree. mr-moqui `2d0e1f29`, with the localization merge, already peaks at 80.7 MB
on the old fork, against 68 MB on `ca9d2f83`.

The other processes are within run-to-run noise:

- `heap_at_max` is the sum at the moment of the process's peak, so it moves with what the main thread and the workers
  held then.
- Process 2's base runs give 57.7 and 62.5 MB; the declared keys give 63.1 and 60.1.
- Process 3's base runs give 68.9 and 73.4 MB; the declared keys give 71.0 and 71.5.

There is no declared-keys growth to fix. What to look at next is in the tree: what the localization merge added to
process 0. Its main runtime holds about 36 MB at its peak and its 23 workers about 35 to 39 MB.

`script-stats-apps-base1.jsonl` and `script-stats-apps-base2.jsonl` are the base runs' stats; `results.txt` has the
spec counts.
