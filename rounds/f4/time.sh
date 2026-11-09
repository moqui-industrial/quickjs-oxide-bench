#!/bin/bash
# usage: time.sh <reps> <workload...> -- name=binary ...: median wall time per engine, pinned to CPU 7.
REPS=$1; shift; W=(); while [ "$1" != "--" ]; do W+=("$1"); shift; done; shift
cd /home/jonesde/work/moquiwork/oxide-bench/f4
for w in "${W[@]}"; do
  line="$w"
  for spec in "$@"; do
    name=${spec%%=*}; bin=${spec#*=}; ts=()
    for r in $(seq $REPS); do ts+=($( { /usr/bin/time -f "%e" taskset -c 7 $bin $w.js >/dev/null; } 2>&1 )); done
    med=$(printf "%s\n" "${ts[@]}" | sort -n | sed -n "$(( (REPS+1)/2 ))p")
    line="$line $name=$med"
  done
  echo "$line"
done
