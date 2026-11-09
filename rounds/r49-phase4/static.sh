#!/bin/bash
cd /home/jonesde/work/moquiwork/mr-moqui
export CARGO_NET_GIT_FETCH_WITH_CLI=true GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=url./home/jonesde/work/moquiwork/quickjs-oxide.insteadOf GIT_CONFIG_VALUE_0=https://github.com/moqui/quickjs-oxide
A=$PWD/../oxide-bench/phase4
for k in 1024 2048; do
  rm -f $A/static-$k.jsonl
  PROBE_IDLE_MS=600000 PROBE_STATIC_KIB=$k MOQUI_SCRIPT_STATS_FILE=$A/static-$k.jsonl ./moq test mr-mantle > $A/static-$k.log 2>&1
  echo "$k $? $(grep -E 'specs in' $A/static-$k.log | tail -1)"
done
