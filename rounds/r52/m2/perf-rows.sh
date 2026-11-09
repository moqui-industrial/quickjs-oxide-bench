#!/bin/bash
# perf stat instructions:u per call on lane M2's rows: one batch and six, (six - one) / (5 x calls), and the row's
# js_speed line (allocations per call are exact).
# usage: perf-rows.sh <js_speed binary> <out dir> <set: a|b>
set -u
bin=$1; out=$2; set=${3:-a}; mkdir -p "$out"
cd /home/jonesde/work/moquiwork/mr-moqui-r52/crates/moqui-host
calls=${CALLS:-20000}
half=$((calls / 2))
if [ "$set" = a ]; then
rows=(
  "script|10 cached entity finds|$calls"
  "script|walk an entity list, 100 cached rows|$calls"
  "actions|entity-find-one, cached|$calls"
  "service|find#Cached (10 cached finds)|$half"
)
else
rows=(
  "script|walk itemList, 100 context maps|$calls"
  "expr|value \`itemList.length\` (100 maps)|$calls"
  "script|10 noop service calls, itemList tracked|$calls"
  "actions|iterate 100 context maps with if and set|$calls"
)
fi
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
