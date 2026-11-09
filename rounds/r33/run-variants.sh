#!/bin/bash
# Round 33: one js_speed binary, each MOQUI_OXIDE_OFF setting, two runs each, on oxide; waits for a quiet machine.
# usage: run-variants.sh <js_speed binary> <out dir> [variant ...]   (variant "on" = nothing off)
set -u
bin=$1; out=$2; shift 2
variants=("$@"); [ ${#variants[@]} -eq 0 ] && variants=(on all entity leaf this keys flush)
mkdir -p "$out"
while pgrep -x 'cargo|rustc|moqui' >/dev/null || pgrep -f 'target/.*/moqui ' >/dev/null; do sleep 20; done
cd /home/jonesde/work/moquiwork/mr-moqui/crates/moqui-host
for run in 1 2; do
  for v in "${variants[@]}"; do
    off=$v; [ "$v" = on ] && off=
    MOQUI_OXIDE_OFF=$off JS_SPEED_ENGINE=oxide JS_SPEED_ONLY=script,template,screen "$bin" --ignored --nocapture \
      > "$out/$v-$run.log" 2>&1
  done
done
