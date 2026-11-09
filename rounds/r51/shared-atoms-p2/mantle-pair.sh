#!/bin/bash
# Builds Maximal moqui against a fork tree and runs mr-mantle's specs with the census: mantle-pair.sh <fork dir> <out dir>
set -e
cd /home/jonesde/work/moquiwork/mr-moqui-r51
mkdir -p "$2"
CARGO_BUILD_JOBS=4 ./moq build --config "patch.\"https://github.com/moqui/quickjs-oxide\".quickjs-oxide.path=\"$1\"" > "$2/build.log" 2>&1
grep "Compiling quickjs-oxide-core" "$2/build.log" >> "$2/build.txt" || true
{ time QJS_ATOM_CENSUS=1 MOQUI_SCRIPT_STATS_FILE="$2/script-stats.jsonl" ./moq test mr-mantle --nobuild > "$2/test.stdout" 2> "$2/test.stderr"; } 2> "$2/time.txt" || true
tail -1 "$2/test.stdout"
