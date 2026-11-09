#!/usr/bin/env python3
"""Rows of each variant's better run: us/call and allocs/call. usage: table.py <dir> [variant ...]"""
import re, sys, glob, os
d = sys.argv[1]
variants = sys.argv[2:] or ['on', 'all', 'entity', 'leaf', 'this', 'keys', 'flush']
row = re.compile(r'^  (\S.*?)\s{2,}(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+(-?\d+)')
data = {}
for v in variants:
    for f in sorted(glob.glob(os.path.join(d, f'{v}-*.log'))):
        for line in open(f):
            m = row.match(line)
            if not m or 'batch' in line:
                continue
            name, us, allocs = m.group(1), float(m.group(4)), float(m.group(6))
            best = data.setdefault(v, {}).get(name)
            if best is None or us < best[0]:
                data[v][name] = (us, allocs)
names = list(data.get(variants[0], {}).keys())
print('| row | ' + ' | '.join(variants) + ' |')
print('|---|' + '---:|' * len(variants))
for n in names:
    cells = []
    for v in variants:
        us, al = data.get(v, {}).get(n, (float('nan'), float('nan')))
        cells.append(f'{us:.2f} ({al:.0f})')
    print(f'| {n} | ' + ' | '.join(cells) + ' |')
