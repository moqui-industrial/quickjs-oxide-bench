#!/bin/bash
# usage: build.sh <out name>; builds js_speed from the r52 worktree against the fork's local main
set -e
cd /home/jonesde/work/moquiwork/mr-moqui-r52
FORK=${FORK:-/home/jonesde/work/moquiwork/quickjs-oxide-bench/work/r52/m2/fork-ddba97fe}
T=/home/jonesde/work/moquiwork/quickjs-oxide-bench/work/r52/m2/target
CARGO_TARGET_DIR=$T CARGO_BUILD_JOBS=4 CARGO_PROFILE_RELEASE_DEBUG=1 cargo --config "patch.\"https://github.com/moqui/quickjs-oxide\".quickjs-oxide.path=\"${FORK}\"" test --release -p moqui-host --test js_speed --no-run > $T/../build-$1.log 2>&1; grep -E "^(error|warning: unused)|Executable" $T/../build-$1.log || true
f=$(ls -t $T/release/deps/js_speed-* | grep -v '\.d$' | head -1)
mkdir -p $T/../$1; cp $f $T/../$1/js_speed
echo "built $1 from $(git rev-parse --short HEAD) fork ${FORK}" | tee $T/../$1/built.txt
