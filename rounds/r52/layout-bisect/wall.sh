#!/bin/bash
# usage: wall.sh name=binary ...  -> us/call of the slow rows (5 batches, median), three alternating passes
cd /home/jonesde/work/moquiwork/mr-moqui-r52g
for pass in 1 2 3; do for e in "$@"; do
  out=$( (JS_SPEED_ONLY=script JS_SPEED_ROW="1000 " taskset -c 2 ${e#*=} --ignored --nocapture; JS_SPEED_ONLY=script JS_SPEED_ROW="100 objects made" taskset -c 2 ${e#*=} --ignored --nocapture; JS_SPEED_ONLY=screen JS_SPEED_ROW="Plain.qvt" taskset -c 2 ${e#*=} --ignored --nocapture; JS_SPEED_ONLY=expr JS_SPEED_ROW="value \`a\` (a bare" taskset -c 2 ${e#*=} --ignored --nocapture) 2>&1 | grep -E "^  (1000 adds to a local|100 objects made|1000 string|Plain.qvt|value .a. \(a bare)" | awk '{for(i=1;i<=NF;i++) if($i ~ /^[0-9]+$/ && $(i+1) ~ /\./){print $(i+2); break}}' | tr '\n' ' ')
  echo "${e%%=*}: $out"
done; done
