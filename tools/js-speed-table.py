#!/usr/bin/env python3
"""Compares js_speed outputs: the best of each side's runs, per row, as a Markdown table.

usage: js-speed-table.py BASE_RUN... -- FINAL_RUN...

Each run is the stdout of a js_speed binary run with `--ignored --nocapture`. A row is matched by its name; the time is
the better of the runs, the allocations come from the first. The last line is the geometric mean of the ratios.
"""
import math
import re
import sys


def load(path):
    rows = {}
    for line in open(path, errors="replace"):
        t = line.split()
        if len(t) < 12 or not re.match(r"^[\d.]+-[\d.]+$", t[-1]):
            continue
        try:
            us = float(t[-9])
            allocs = float(t[-7])
        except ValueError:
            continue
        rows[" ".join(t[:-11])] = (us, allocs)
    return rows


def best(paths):
    runs = [load(p) for p in paths]
    out = {}
    for name, (us, allocs) in runs[0].items():
        out[name] = (min(r[name][0] for r in runs if name in r), allocs)
    return out


def main(argv):
    if "--" not in argv:
        sys.exit(__doc__)
    i = argv.index("--")
    base, final = best(argv[:i]), best(argv[i + 1 :])
    print("| row | base µs | final µs | ÷ | base allocs | final allocs |")
    print("|---|---:|---:|---:|---:|---:|")
    logs = []
    for name, (bu, ba) in base.items():
        if name not in final or bu == 0:
            continue
        fu, fa = final[name]
        ratio = fu / bu
        logs.append(math.log(ratio))
        print(f"| {name} | {bu:.2f} | {fu:.2f} | {ratio:.2f} | {ba:.1f} | {fa:.1f} |")
    print(f"\ngeometric mean ÷ over {len(logs)} rows: {math.exp(sum(logs) / len(logs)):.3f}")


if __name__ == "__main__":
    main(sys.argv[1:])
