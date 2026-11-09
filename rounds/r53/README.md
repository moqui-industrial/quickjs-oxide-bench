# Round 53: full screen renders

mr-moqui's [plans/Profiling2.md](https://github.com/moqui/mr-moqui/blob/master/plans/Profiling2.md) Round 53 has the
results. These are the tools; their outputs go in `work/r53/`.

## Timing screens over HTTP

Run a release server from mr-moqui (`./moq run-production`) with the screen tarpit off: the demo data stops a user
after 120 renders of a screen in a minute. Add this to `runtime/conf/MoquiProductionConf.xml` for the run and take it
out after:

```xml
<artifact-execution-facade><artifact-execution type="AT_XML_SCREEN" authz-enabled="true" tarpit-enabled="false"/></artifact-execution-facade>
```

Then:

```
python3 -I screen_bench.py --label NAME --out ../../work/r53/NAME --perf-pid <server pid> [--cases B-html,B-qvt] [--rounds 3 --n 100]
python3 -I table.py ../../work/r53/base.log ../../work/r53/NAME.log      # medians and instructions, with ratios
python3 -I compare_bodies.py ../../work/r53/base ../../work/r53/NAME     # outputs, build stamps masked
```

`screen_bench.py` logs in as john.doe, times each case (A Cache List, B Tools Entities with 1,482 rows, C Cache
Elements, D Artifact Stats, E the System dashboard; each html, qvt and tui, and A's menu JSON) and runs
`perf stat -e instructions:u` on the server over a fixed loop. Read the instructions: wall times of small pages move
up to 20% between builds. Pages that show live data (cache counts, memory, the services and screens known) differ
between servers; mask the numbers (or compare Entities, whose output is fixed).

## Where a render's time goes

- **`MOQUI_RENDER_PROFILE=<file>`** on the server: a JSON line per render with each phase's count and inclusive and
  exclusive time (units, each host method, conversions, flushes). `profile_table.py <file> --match Entities` sums it.
  It adds 5 to 15% to a render with many host calls.
- **`MOQUI_JS_SAMPLE=<file>`**: the script sampler (quickjs-oxide's `Runtime::start_sampling`), folded stacks under
  each render's path. `samples_table.py <file> [--from N --to M]` gives self and inclusive shares by function; render
  one screen and mode at a time, since lines append in order. `name_(native)` frames are builtins and host functions.
  The sampler is in every build since mr-moqui pinned quickjs-oxide at 223a2047; f873d7e7 counts the time in a
  native function as the native's.
- **`MOQUI_UNIT_DUMP=<dir>`**: each generated screen unit and mode runtime as a file, to read the code a render runs.
- **perf** on a frame-pointer build: `inclusive.py` gives inclusive shares from `perf script -F ip,sym` output.

`js-sampler-mr-moqui.patch` is the mr-moqui side as it was before the pin moved (committed in mr-moqui 8e0277e7).
