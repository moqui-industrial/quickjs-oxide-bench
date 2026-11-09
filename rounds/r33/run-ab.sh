#!/bin/bash
# usage: run-ab.sh <out dir> <tag>=<binary> ...   two runs of each, alternating, on oxide
set -u; out=$1; shift; mkdir -p "$out"
cd /home/jonesde/work/moquiwork/mr-moqui/crates/moqui-host
for run in 1 2; do for pair in "$@"; do tag=${pair%%=*}; bin=${pair#*=}
  JS_SPEED_ENGINE=oxide JS_SPEED_ONLY=script,template,screen "$bin" --ignored --nocapture > "$out/$tag-$run.log" 2>&1
done; done
