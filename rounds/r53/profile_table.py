#!/usr/bin/env python3
"""Summarize a MOQUI_RENDER_PROFILE file: per (path, mode), the median total and the mean exclusive time per phase.

    python3 -I profile_table.py <profile.jsonl> [--skip 1] [--top 25] [--match Entities]

`--skip N` drops each (path, mode)'s first N lines (the first render's compile). Host calls are listed by method with
their counts per render. Unit exclusive time is the interpreter running macro and unit code between host calls.
"""
import argparse, collections, json, statistics

ap = argparse.ArgumentParser()
ap.add_argument("file")
ap.add_argument("--skip", type=int, default=1)
ap.add_argument("--top", type=int, default=25)
ap.add_argument("--match", default="")
args = ap.parse_args()

groups = collections.defaultdict(list)
for line in open(args.file):
    line = line.strip()
    if not line:
        continue
    rec = json.loads(line)
    if args.match and args.match not in rec["path"]:
        continue
    groups[(rec["path"], rec["mode"])].append(rec)

for (path, mode), recs in groups.items():
    recs = recs[args.skip:]
    if not recs:
        continue
    n = len(recs)
    total = statistics.median(r["total_us"] for r in recs)
    sums = collections.defaultdict(lambda: [0, 0.0, 0.0])
    for r in recs:
        for name, p in r["phases"].items():
            s = sums[name]
            s[0] += p["n"]
            s[1] += p["excl_us"]
            s[2] += p["incl_us"]
    rows = sorted(((name, c / n, e / n, i / n) for name, (c, e, i) in sums.items()), key=lambda x: -x[2])
    excl_sum = sum(r[2] for r in rows)
    host_excl = sum(r[2] for r in rows if r[0].startswith("host:"))
    host_calls = sum(r[1] for r in rows if r[0].startswith("host:"))
    print(f"\n== {path} [{mode}]  {n} renders, median total {total / 1000:.2f} ms (sum of exclusive {excl_sum / 1000:.2f} ms)")
    groups_excl = collections.OrderedDict()
    for name, c, e, i in rows:
        g = "host bodies" if name.startswith("host:") else name
        groups_excl[g] = groups_excl.get(g, 0) + e
    print("   by phase (exclusive):")
    for g, e in sorted(groups_excl.items(), key=lambda x: -x[1]):
        print(f"     {g:28} {e / 1000:8.2f} ms  {100 * e / excl_sum:5.1f}%")
    print(f"   host calls: {host_calls:.0f} a render, bodies {host_excl / 1000:.2f} ms "
          f"({1000 * host_excl / max(host_calls, 1) / 1000:.2f} µs a call)")
    print(f"   top host methods (exclusive):          calls    ms    µs/call   incl ms")
    for name, c, e, i in [r for r in rows if r[0].startswith("host:")][: args.top]:
        print(f"     {name[5:]:34} {c:8.0f} {e / 1000:7.2f} {e / max(c, 1):8.2f} {i / 1000:8.2f}")
