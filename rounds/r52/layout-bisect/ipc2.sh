#!/bin/bash
# usage: ipc2.sh <binary> <section> <row> <calls>  -> instructions per call (21 batches minus 1)
X=$1; S=$2; R=$3; C=$4
cd /home/jonesde/work/moquiwork/mr-moqui-r52g
run() { JS_SPEED_ONLY=$S JS_SPEED_ROW="$R" JS_SPEED_BATCHES=$1 perf stat -x, -e instructions:u $X --ignored --nocapture 2>&1 >/dev/null | grep instructions | cut -d, -f1; }
a=$(run 1); b=$(run 21)
echo $(( (b-a)/(20*C) ))
