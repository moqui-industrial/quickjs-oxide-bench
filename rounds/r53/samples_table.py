#!/usr/bin/env python3
"""Summarize MOQUI_JS_SAMPLE folded stacks: python3 -I samples_table.py <samples.folded> [--from N] [--to M] [--top 30]

--from/--to select line numbers of the file (1-based, inclusive), as samples are appended in time order. Prints the
self share by innermost frame (function:line) and by function, and the inclusive share by function (each function
counted once a stack)."""
import argparse, collections

ap = argparse.ArgumentParser()
ap.add_argument("file")
ap.add_argument("--from", dest="start", type=int, default=1)
ap.add_argument("--to", dest="end", type=int, default=10**12)
ap.add_argument("--top", type=int, default=30)
args = ap.parse_args()

self_line, self_fn, incl_fn = collections.Counter(), collections.Counter(), collections.Counter()
total = 0
for number, line in enumerate(open(args.file), 1):
    if number < args.start or number > args.end:
        continue
    stack, _, count = line.rstrip("\n").rpartition(" ")
    count = int(count)
    frames = stack.split(";")[1:]  # the first is the label
    if not frames:
        continue
    total += count
    leaf = frames[-1]
    self_line[leaf] += count
    self_fn[leaf.rpartition(":")[0]] += count
    for fn in {f.rpartition(":")[0] for f in frames}:
        incl_fn[fn] += count

print(f"{total} samples")
for title, counter in (("self by line", self_line), ("self by function", self_fn), ("inclusive by function", incl_fn)):
    print(f"\n{title}:")
    for key, count in counter.most_common(args.top):
        print(f"  {100 * count / total:5.1f}%  {count:6}  {key}")
