#!/bin/bash
# usage: probe.sh <binary> <mode> [n1 n2] : allocations per op = (calls(n2)-calls(n1))/(n2-n1)
BIN=$1; MODE=$2; N1=${3:-1000}; N2=${4:-11000}
OUT=/home/jonesde/work/moquiwork/oxide-bench/alloc/ht
mkdir -p $OUT
calls() {
  rm -f $OUT/ht.$MODE.$1.*
  heaptrack -o $OUT/ht.$MODE.$1 $BIN $MODE $1 >/dev/null 2>&1
  heaptrack_print $OUT/ht.$MODE.$1.zst 2>/dev/null | grep -m1 "^calls to allocation functions" | awk '{print $5}'
}
A=$(calls $N1); B=$(calls $N2)
echo "$MODE: $A @ $N1, $B @ $N2, per op $(python3 -c "print(($B-$A)/($N2-$N1))")"
