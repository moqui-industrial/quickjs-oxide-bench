#!/bin/bash
# Round 34, after run-r34a.sh: the js_speed timings of every binary (quiet), then the gates and Sweeps of ord and hnd.
set -u
B=/home/jonesde/work/moquiwork/oxide-bench
W=/home/jonesde/work/moquiwork
P=$W/mr-moqui/target/profiling/bin
while kill -0 3336487 2>/dev/null; do sleep 20; done
while pgrep -x cargo >/dev/null || pgrep -x rustc >/dev/null || pgrep -x moqui >/dev/null; do sleep 5; done
$B/round33/run-ab.sh $B/round34/ab2 r33=$P/js_speed-r33 cap=$P/js_speed-cap key=$P/js_speed-key ord=$P/js_speed-ord hnd=$P/js_speed-hnd integ=$P/js_speed-integ34
$B/round33/run-variants.sh $P/js_speed-integ34 $B/round34/integ on all inplace hnd
echo "timed"
for c in ord hnd; do (cd $W/quickjs-oxide-$c && cargo build --release -p quickjs-oxide-cli --bin qjs > $B/build-$c.log 2>&1); echo "$c built $?"; done
for c in ord hnd; do $B/gates.sh $W/quickjs-oxide-$c > $B/gates-r34-$c.log 2>&1; tail -1 $B/gates-r34-$c.log | sed "s/^/$c: /"; done
BASE=$B/base-8635-target/release/qjs
while pgrep -x cargo >/dev/null || pgrep -x rustc >/dev/null || pgrep -x moqui >/dev/null; do sleep 5; done
cd $B/base-8635
for c in ord hnd; do
  CAND=$W/quickjs-oxide-$c/target/release/qjs
  python3 scripts/benchmark/bench.py sweep --base $BASE --candidate $CAND --suite $B/suite-matrix/manifest.json --output $B/sweep-r34-$c > $B/sweep-r34-$c.log 2>&1; echo "sweep $c $?"
done
