#!/bin/bash
cd /home/jonesde/work/moquiwork/mr-moqui
export CARGO_NET_GIT_FETCH_WITH_CLI=true GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=url./home/jonesde/work/moquiwork/quickjs-oxide.insteadOf GIT_CONFIG_VALUE_0=https://github.com/moqui/quickjs-oxide
A=$PWD/../oxide-bench/phase4
cargo clippy --workspace --all-targets --message-format short 2>&1 | grep -E "^(crates|runtime).*(warning|error)" > $A/r49-clippy.log; echo "clippy $(wc -l < $A/r49-clippy.log)"
./moq test-framework > $A/r49-framework.log 2>&1; echo "framework $?"
rm -f $A/r49-stats.jsonl
MOQUI_SCRIPT_STATS_FILE=$A/r49-stats.jsonl ./moq test-apps > $A/r49-apps.log 2>&1; echo "apps $?"
