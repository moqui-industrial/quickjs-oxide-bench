#!/bin/bash
W=/home/jonesde/work/moquiwork/quickjs-oxide-bench/work/r51
$W/mantle-pair.sh ../quickjs-oxide-bench/work/base-p2 $W/mantle-k0
$W/mantle-pair.sh ../quickjs-oxide-bench/work/cand-p3 $W/mantle-k1
cd /home/jonesde/work/moquiwork/mr-moqui-r51
for t in base-p2:k0 cand-p3:k1; do
  CARGO_TARGET_DIR=$W/target CARGO_BUILD_JOBS=4 CARGO_PROFILE_RELEASE_DEBUG=1 cargo --config "patch.\"https://github.com/moqui/quickjs-oxide\".quickjs-oxide.path=\"../quickjs-oxide-bench/work/${t%%:*}\"" test --release -p moqui-host --test js_speed --no-run 2>&1 | grep -E "^error"
  f=$(ls -t $W/target/release/deps/js_speed-* | grep -v '\.d$' | head -1); mkdir -p $W/${t#*:}; cp $f $W/${t#*:}/js_speed
done
echo all-done
