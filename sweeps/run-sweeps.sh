#!/bin/bash
set -u
B=/home/jonesde/work/moquiwork/oxide-bench
BASE=$B/base-target/release/qjs
cd $B/base
for C in host-exotic reentry integ; do
  echo "== sweep $C"
  python3 scripts/benchmark/bench.py sweep --base $BASE --candidate /home/jonesde/work/moquiwork/quickjs-oxide-$C/target/release/qjs --suite $B/suite-matrix/manifest.json --output $B/sweep-$C > $B/sweep-$C.log 2>&1; echo "exit $?"
done
echo "== memory host-exotic"
python3 scripts/benchmark/bench.py memory --engine base=$BASE --engine candidate=/home/jonesde/work/moquiwork/quickjs-oxide-host-exotic/target/release/qjs --manifest $B/suite-matrix/manifest.json --output $B/memory-host-exotic > $B/memory-host-exotic.log 2>&1; echo "exit $?"
