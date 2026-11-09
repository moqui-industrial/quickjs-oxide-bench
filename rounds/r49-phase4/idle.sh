#!/bin/bash
cd /home/jonesde/work/moquiwork/mr-moqui
export CARGO_NET_GIT_FETCH_WITH_CLI=true GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=url./home/jonesde/work/moquiwork/quickjs-oxide.insteadOf GIT_CONFIG_VALUE_0=https://github.com/moqui/quickjs-oxide
A=$PWD/../oxide-bench/phase4
for ms in 600000 10000 2000 500; do
  rm -f $A/idle-$ms.jsonl
  PROBE_IDLE_MS=$ms MOQUI_SCRIPT_STATS_FILE=$A/idle-$ms.jsonl ./moq test mr-mantle > $A/idle-$ms.log 2>&1
  echo "$ms $? $(grep -E '^[0-9]+ features' $A/idle-$ms.log | tail -1)"
done
