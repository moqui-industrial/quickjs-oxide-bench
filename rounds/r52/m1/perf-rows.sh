#!/bin/bash
# perf stat instructions:u per call on the M1a rows: one batch and six, (six - one) / (5 x calls).
# usage: perf-rows.sh <js_speed binary> <out dir>
set -u
bin=$1; out=$2; mkdir -p "$out"
cd /home/jonesde/work/moquiwork/mr-moqui/crates/moqui-host
calls=${CALLS:-20000}
half=$((calls / 2))
rows=(
  "actions|one set|$calls"
  "actions|four sets (the echo#Data body)|$calls"
  "service|set#One (one set)|$half"
  "service|echo#Inline (four sets)|$half"
  "service|BasicServices.echo#Data|$half"
)
for row in "${rows[@]}"; do
  IFS='|' read -r only name n <<<"$row"
  tag=$(echo "$name" | tr -c 'A-Za-z0-9' '_')
  for b in 1 6; do
    JS_SPEED_ONLY=$only JS_SPEED_ROW="$name" JS_SPEED_CALLS=$calls JS_SPEED_BATCHES=$b perf stat -x, -e instructions:u -o "$out/$tag.b$b.perf" \
      "$bin" --ignored --nocapture > "$out/$tag.b$b.txt" 2>&1
  done
  i1=$(grep instructions "$out/$tag.b1.perf" | cut -d, -f1)
  i6=$(grep instructions "$out/$tag.b6.perf" | cut -d, -f1)
  line=$(grep -F "  $name" "$out/$tag.b6.txt" | tail -1)
  echo "$name | instr/call $(( (i6 - i1) / (5 * n) )) | $line"
done
