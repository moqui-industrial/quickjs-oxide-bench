#!/bin/bash
# Round 34: base 8635ecb5, candidates perf/cap-headroom and perf/key-latin1: gates, then each Sweep and memory run.
set -u
B=/home/jonesde/work/moquiwork/oxide-bench
W=/home/jonesde/work/moquiwork
[ -d $B/base-8635 ] || git -C $W/quickjs-oxide worktree add $B/base-8635 8635ecb5 >/dev/null 2>&1
(cd $B/base-8635 && cargo build --release -p quickjs-oxide-cli --bin qjs --target-dir $B/base-8635-target > $B/build-base-8635.log 2>&1); echo "base built $?"
for c in cap key; do (cd $W/quickjs-oxide-$c && cargo build --release -p quickjs-oxide-cli --bin qjs > $B/build-$c.log 2>&1); echo "$c built $?"; done
for c in cap key; do $B/gates.sh $W/quickjs-oxide-$c > $B/gates-r34-$c.log 2>&1; tail -1 $B/gates-r34-$c.log | sed "s/^/$c: /"; done
BASE=$B/base-8635-target/release/qjs
while pgrep -x cargo >/dev/null || pgrep -x rustc >/dev/null || pgrep -x moqui >/dev/null; do sleep 5; done
cd $B/base-8635
for c in cap key; do
  CAND=$W/quickjs-oxide-$c/target/release/qjs
  python3 scripts/benchmark/bench.py sweep --base $BASE --candidate $CAND --suite $B/suite-matrix/manifest.json --output $B/sweep-r34-$c > $B/sweep-r34-$c.log 2>&1; echo "sweep $c $?"
  python3 scripts/benchmark/bench.py memory --engine base=$BASE --engine candidate=$CAND --manifest $B/suite-matrix/manifest.json --output $B/memory-r34-$c > $B/memory-r34-$c.log 2>&1; echo "memory $c $?"
done
