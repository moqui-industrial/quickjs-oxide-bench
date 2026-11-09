#!/bin/bash
# glibc malloc against jemalloc (LD_PRELOAD) on the Round 36 binary, two runs each, oxide and rquickjs
bin=/home/jonesde/work/moquiwork/mr-moqui/target/profiling/bin/js_speed-r36c; out=/home/jonesde/work/moquiwork/oxide-bench/round37
cd /home/jonesde/work/moquiwork/mr-moqui/crates/moqui-host
for run in 1 2; do
  for eng in oxide rquickjs; do
    JS_SPEED_ENGINE=$eng JS_SPEED_ONLY=script,template,screen $bin --ignored --nocapture > $out/$eng-glibc-$run.log 2>&1
    LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2 JS_SPEED_ENGINE=$eng JS_SPEED_ONLY=script,template,screen $bin --ignored --nocapture > $out/$eng-jemalloc-$run.log 2>&1
  done
done
