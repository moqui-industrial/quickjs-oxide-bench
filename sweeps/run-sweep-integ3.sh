#!/bin/bash
set -u
B=/home/jonesde/work/moquiwork/oxide-bench
BASE=$B/base-dc5b-target/release/qjs
CAND=/home/jonesde/work/moquiwork/quickjs-oxide-integ3/target/release/qjs
while pgrep -x cargo >/dev/null || pgrep -x rustc >/dev/null || pgrep -x moqui >/dev/null; do sleep 5; done
cd $B/base
echo "== sweep integ3"
python3 scripts/benchmark/bench.py sweep --base $BASE --candidate $CAND --suite $B/suite-matrix/manifest.json --output $B/sweep-integ3 > $B/sweep-integ3.log 2>&1; echo "sweep $?"
echo "== memory integ3"
python3 scripts/benchmark/bench.py memory --engine base=$BASE --engine candidate=$CAND --manifest $B/suite-matrix/manifest.json --output $B/memory-integ3 > $B/memory-integ3.log 2>&1; echo "memory $?"
