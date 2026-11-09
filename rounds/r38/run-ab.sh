#!/bin/bash
# A/B of two js_speed binaries on oxide, two runs each, the rows matching $ROWS (a JS_SPEED_ROW each)
out=$1; shift; a=$1; b=$2
mkdir -p "$out"; cd /home/jonesde/work/moquiwork/mr-moqui/crates/moqui-host
for run in 1 2; do
  for name in a b; do
    bin=${!name}
    JS_SPEED_ENGINE=oxide JS_SPEED_ONLY=script,template,screen "$bin" --ignored --nocapture > "$out/$name-$run.log" 2>&1
  done
done
