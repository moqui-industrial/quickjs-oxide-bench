#!/usr/bin/env python3
"""Compare screen_bench.py logs: python3 -I table.py base.log c1.log [c2.log ...] [--md]

For each case: the last round's median ms and the perf loop's M instructions:u a request, with each candidate's ratio to
the first log."""
import re, sys

md = "--md" in sys.argv
logs = [a for a in sys.argv[1:] if not a.startswith("--")]


def load(path):
    out = {}
    last_round = {}
    for line in open(path):
        m = re.match(r"(\S+)\s+r(\d+) .*med\s+([\d.]+)", line)
        if m and int(m[2]) >= last_round.get(m[1], 0):
            last_round[m[1]] = int(m[2])
            out.setdefault(m[1], {})["med"] = float(m[3])
        m = re.match(r"(\S+)\s+perf\s+([\d.]+) M", line)
        if m:
            out.setdefault(m[1], {})["ins"] = float(m[2])
    return out


data = [load(p) for p in logs]
names = [p.rsplit("/", 1)[-1].removesuffix(".log") for p in logs]
head = ["case"] + [f"{n} ms" for n in names] + [f"{n} ÷" for n in names[1:]] + [f"{n} Mi" for n in names] + [f"{n} Mi ÷" for n in names[1:]]
rows = []
for case in data[0]:
    b = data[0][case]
    if "med" not in b:
        continue
    row = [case]
    row += [f"{d.get(case, {}).get('med', float('nan')):.2f}" for d in data]
    row += [f"{d.get(case, {}).get('med', float('nan')) / b['med']:.3f}" for d in data[1:]]
    row += [f"{d.get(case, {}).get('ins', float('nan')):.1f}" for d in data]
    row += [f"{d.get(case, {}).get('ins', float('nan')) / b.get('ins', float('nan')):.3f}" for d in data[1:]]
    rows.append(row)
if md:
    print("| " + " | ".join(head) + " |")
    print("|" + "|".join("---" if i == 0 else "---:" for i in range(len(head))) + "|")
    for r in rows:
        print("| " + " | ".join(r) + " |")
else:
    widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(head)]
    print("  ".join(h.rjust(w) for h, w in zip(head, widths)))
    for r in rows:
        print("  ".join(c.rjust(w) for c, w in zip(r, widths)))
