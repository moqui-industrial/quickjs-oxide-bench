#!/bin/bash
# Acceptance after Rounds 33 to 47: js_speed before/now x rquickjs/oxide, the fork's Sweep and memory, Mantle 2x2.
set -u
B=/home/jonesde/work/moquiwork/oxide-bench; A=$B/accept48; W=/home/jonesde/work/moquiwork/mr-moqui
P=$W/target/profiling/bin
quiet() { while pgrep -x cargo >/dev/null || pgrep -x rustc >/dev/null || pgrep -x moqui >/dev/null; do sleep 10; done; }
quiet; echo "js_speed start $(date +%T) $(uptime)"
mkdir -p $A/js
cd $W/crates/moqui-host
for run in 1 2; do
  for bin in before now; do
    for eng in rquickjs oxide; do
      quiet
      JS_SPEED_ENGINE=$eng JS_SPEED_ONLY=script,template,screen $P/js_speed-$bin --ignored --nocapture > $A/js/$bin-$eng-$run.log 2>&1
    done
  done
done
echo "js_speed done $(date +%T)"
quiet; cd $B/base
python3 scripts/benchmark/bench.py sweep --base $B/base-8635-target/release/qjs --candidate /home/jonesde/work/moquiwork/quickjs-oxide/target/release/qjs --suite $B/suite-matrix/manifest.json --output $A/sweep > $A/sweep.log 2>&1; echo "sweep $? $(date +%T)"
python3 scripts/benchmark/bench.py memory --engine base=$B/base-8635-target/release/qjs --engine candidate=/home/jonesde/work/moquiwork/quickjs-oxide/target/release/qjs --manifest $B/suite-matrix/manifest.json --output $A/memory > $A/memory.log 2>&1; echo "memory $? $(date +%T)"
$B/mantle-pg/setup.sh $W > $A/mantle-setup.log 2>&1; echo "setup $?"
for tag in rq1 ox1 rq2 ox2; do
  eng=rquickjs; case $tag in ox*) eng=oxide;; esac
  $B/mantle-pg/run.sh $W $eng $tag $A/mantle
done
python3 $B/mantle-pg/table.py $A/mantle rq1,rq2 ox1,ox2 > $A/mantle-table.md 2>&1
$B/mantle-pg/teardown.sh
echo "all done $(date +%T)"
