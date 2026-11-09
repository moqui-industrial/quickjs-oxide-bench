#!/bin/bash
# usage: instr.sh <binary> <mode> [n1 n2]: instructions:u per op
BIN=$1; MODE=$2; N1=${3:-1000}; N2=${4:-201000}
c() { perf stat -x, -e instructions:u taskset -c 2 $BIN $MODE $1 2>&1 >/dev/null | awk -F, '/instructions/{print $1}'; }
A=$(c $N1); B=$(c $N2)
python3 -c "print('$MODE', round(($B-$A)/($N2-$N1)))"
