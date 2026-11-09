#!/bin/bash
# The quiet pass: the round's base js_speed against the final one, alternating, two runs each.
set -e
W=/home/jonesde/work/moquiwork/quickjs-oxide-bench/work/r52
for i in 1 2; do
  "$W/base/js_speed" --ignored --nocapture > "$W/final/base-run$i.txt" 2>&1
  "$W/final/js_speed" --ignored --nocapture > "$W/final/final-run$i.txt" 2>&1
done
echo done
