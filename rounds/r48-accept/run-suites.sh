#!/bin/bash
set -u
B=/home/jonesde/work/moquiwork/oxide-bench; A=$B/accept48; W=/home/jonesde/work/moquiwork/mr-moqui
$B/gates.sh /home/jonesde/work/moquiwork/quickjs-oxide > $A/gates-main.log 2>&1; echo "gates $? $(tail -1 $A/gates-main.log) $(date +%T)"
cd $W
export CARGO_NET_GIT_FETCH_WITH_CLI=true GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=url./home/jonesde/work/moquiwork/quickjs-oxide.insteadOf GIT_CONFIG_VALUE_0=https://github.com/moqui/quickjs-oxide
./moq test-framework > $A/test-framework.log 2>&1; echo "test-framework $? $(date +%T)"
rm -f $A/stats-oxide.jsonl $A/stats-default.jsonl
script_engine=oxide MOQUI_SCRIPT_STATS_FILE=$A/stats-oxide.jsonl ./moq test-apps > $A/test-apps-oxide.log 2>&1; echo "test-apps oxide $? $(date +%T)"
MOQUI_SCRIPT_STATS_FILE=$A/stats-default.jsonl ./moq test-apps > $A/test-apps-default.log 2>&1; echo "test-apps default $? $(date +%T)"
