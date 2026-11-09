#!/bin/bash
# Builds js_speed at each bisect point: <name>:<mr-moqui commit>:<fork commit>, through the patch path.
M=/home/jonesde/work/moquiwork/mr-moqui-r52g; F=/home/jonesde/work/moquiwork/quickjs-oxide-bisect
W=/home/jonesde/work/moquiwork/quickjs-oxide-bench/work/r52/bisect; T=$W/target
for p in "$@"; do
  IFS=: read n m f <<<"$p"
  git -C $M checkout -q -f --detach $m && git -C $F checkout -q --detach $f || { echo "$n: checkout failed"; continue; }
  (cd $M && CARGO_TARGET_DIR=$T CARGO_BUILD_JOBS=4 CARGO_PROFILE_RELEASE_DEBUG=1 cargo --config 'patch."https://github.com/moqui/quickjs-oxide".quickjs-oxide.path="../quickjs-oxide-bisect"' test --release -p moqui-host --test js_speed --no-run 2>&1 | grep -E "^error|Executable" > $W/$n.build.log)
  x=$(grep -o 'target/release/deps/js_speed-[0-9a-f]*' $W/$n.build.log | head -1)
  mkdir -p $W/$n && cp $T/release/deps/$(basename $x) $W/$n/js_speed && echo "$n: mr $m fork $f" | tee $W/$n/rev.txt
done
git -C $M checkout -q -f --detach fb0e5f78
echo built
