#!/bin/bash
# usage: gates.sh <worktree>  -- the fork's CI test, lint, fmt and gc-stress steps on a worktree.
# SUITE_PILOT is the pilot suite (bench.py suite build --pilot ...; default work/suite-pilot1).
set -u
B=$(cd "$(dirname "$0")/.." && pwd)
SUITE_PILOT=${SUITE_PILOT:-$B/work/suite-pilot1}
cd "$1" || exit 2
export CARGO_BUILD_JOBS=6
fail=0
step() { echo "== $*"; "$@" > /tmp/.gate.$$ 2>&1; rc=$?; tail -3 /tmp/.gate.$$ | sed 's/^/   /'; grep -E "^test result: FAILED|^error|panicked|FAILED" /tmp/.gate.$$ | head -20 | sed 's/^/   !/'; [ $rc -ne 0 ] && { echo "   FAILED rc=$rc"; fail=1; }; rm -f /tmp/.gate.$$; }
step cargo fmt --all -- --check
step cargo test --locked --workspace --all-targets
step cargo test --locked --workspace --doc
step cargo test --locked --workspace --features test262-host --lib --bins
step cargo test --locked --features test262-host --test unsupported_diagnostics
step cargo test --locked --features test262-host --test oracle test262_
step cargo clippy --locked --workspace --all-targets --all-features -- -D warnings
step cargo clippy --locked --workspace --lib --bins -- -D warnings
step cargo clippy --locked --test oracle -- -D warnings
step cargo clippy --locked --workspace --features test262-host --lib --bins -- -D warnings
step cargo clippy --locked --workspace --features test262-host --test unsupported_diagnostics --test oracle -- -D warnings
step cargo test --locked -p quickjs-oxide-core --features gc-stress
step cargo test --locked -p quickjs-oxide --features gc-stress --lib compiler::register
step cargo build --locked -p quickjs-oxide-cli --features gc-stress --bin qjs
step python3 scripts/checks/check-gc-stress.py --qjs target/debug/qjs
step cargo build --locked --release -p quickjs-oxide-cli --features gc-stress --bin qjs --target-dir target/gc-stress-release
step python3 scripts/checks/check-suite-gc-stress.py --qjs target/gc-stress-release/release/qjs --suite $SUITE_PILOT
echo "GATES $([ $fail = 0 ] && echo PASS || echo FAIL)"
