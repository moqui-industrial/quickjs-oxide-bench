#!/usr/bin/env python3
"""Per thread: the census report with the most reserved bytes, its atoms, image units and key-table entries (all, and
the runtime's own: phase 3 counts those apart). Usage: key-tables.py <stderr>"""
import re, statistics, sys
rx = re.compile(r'^atom census \[([^\]]*)\] reserved=(\d+) live=(\d+): atoms (\d+) .*?(\d+) image units, (\d+) key entries(?: \((\d+) own\))?')
best = {}
for line in open(sys.argv[1], errors='replace'):
    m = rx.match(line)
    if not m:
        continue
    t, res = m.group(1), int(m.group(2))
    row = (res, int(m.group(4)), int(m.group(5)), int(m.group(6)), int(m.group(7)) if m.group(7) else int(m.group(6)))
    if res > best.get(t, (0,))[0]:
        best[t] = row
print('| Thread | Most reserved | Atoms | Image units | Key entries | Own key entries |')
print('|---|---:|---:|---:|---:|---:|')
for t, (res, atoms, units, keys, own) in sorted(best.items(), key=lambda kv: -kv[1][0])[:8]:
    print(f'| {t} | {res // 1024} KiB | {atoms} | {units} | {keys} | {own} |')
workers = [v for k, v in best.items() if 'worker' in k]
print(f"\nService workers: {len(workers)}; most reserved median {statistics.median(v[0] for v in workers) // 1024} KiB, "
      f"summed {sum(v[0] for v in workers) / 1048576:.1f} MiB; own key entries summed {sum(v[4] for v in workers)} "
      f"of {sum(v[3] for v in workers)}; image units summed {sum(v[2] for v in workers)}.")
