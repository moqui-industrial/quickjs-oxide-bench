#!/bin/bash
cd /home/jonesde/work/moquiwork/mr-moqui
export CARGO_NET_GIT_FETCH_WITH_CLI=true GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=url./home/jonesde/work/moquiwork/quickjs-oxide.insteadOf GIT_CONFIG_VALUE_0=https://github.com/moqui/quickjs-oxide
A=../oxide-bench/phase4
rm -f $A/stats-apps.jsonl
MOQUI_SCRIPT_STATS_FILE=$PWD/$A/stats-apps.jsonl ./moq test-apps > $A/test-apps.log 2>&1; echo "test-apps $?"
(. scripts/wasm-env.sh && CARGO_TARGET_DIR=target/browser cargo check -p moqui-browser --target wasm32-unknown-emscripten) > $A/wasm.log 2>&1; echo "wasm $?"
