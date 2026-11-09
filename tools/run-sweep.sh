#!/bin/bash
# usage: run-sweep.sh TAG BASE_QJS CANDIDATE_QJS
# The fork's Sweep and memory runs of a candidate qjs against a base qjs, over work/suite-matrix (bench.py suite build,
# the fork's docs/performance/benchmarking.md). It waits for a quiet window (no cargo, rustc or moqui), runs from the
# fork checkout FORK (default ../quickjs-oxide), and writes sweeps/TAG/, sweeps/TAG.log, sweeps/memory-TAG{,.log}.
set -u
B=$(cd "$(dirname "$0")/.." && pwd)
TAG=$1; BASE=$2; CAND=$3
FORK=${FORK:-$B/../quickjs-oxide}
MANIFEST=${MANIFEST:-$B/work/suite-matrix/manifest.json}
while pgrep -x cargo >/dev/null || pgrep -x rustc >/dev/null || pgrep -x moqui >/dev/null; do sleep 5; done
cd "$FORK" || exit 2
echo "== sweep $TAG"
python3 scripts/benchmark/bench.py sweep --base "$BASE" --candidate "$CAND" --suite "$MANIFEST" --output "$B/sweeps/$TAG" > "$B/sweeps/$TAG.log" 2>&1; echo "sweep $?"
echo "== memory $TAG"
python3 scripts/benchmark/bench.py memory --engine base="$BASE" --engine candidate="$CAND" --manifest "$MANIFEST" --output "$B/sweeps/memory-$TAG" > "$B/sweeps/memory-$TAG.log" 2>&1; echo "memory $?"
