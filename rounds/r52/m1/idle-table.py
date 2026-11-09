#!/usr/bin/env python3
"""One row per process (largest heap first; the order processes end in varies) of MOQUI_SCRIPT_STATS_FILE files: heap_at_max (MB), engines_started, released_idle.
Usage: idle-table.py label=file [label=file ...]"""
import json, sys
runs = []
for arg in sys.argv[1:]:
    label, path = arg.split('=', 1)
    rows = sorted((json.loads(line)['oxide'] for line in open(path) if line.strip()), key=lambda o: -o['heap_at_max'])
    runs.append((label, rows))
print('| # | ' + ' | '.join(f'{l} heap MB / started / released' for l, _ in runs) + ' |')
print('|---|' + '---:|' * len(runs))
for i in range(max(len(r) for _, r in runs)):
    cells = []
    for _, rows in runs:
        o = rows[i] if i < len(rows) else None
        cells.append('–' if o is None else f"{o['heap_at_max'] / 1e6:.1f} / {o['engines_started']} / {o['released_idle']}")
    print(f'| {i} | ' + ' | '.join(cells) + ' |')
for label, rows in runs:
    print(f"\n{label}: max heap {max(o['heap_at_max'] for o in rows) / 1e6:.1f} MB, summed {sum(o['heap_at_max'] for o in rows) / 1e6:.1f} MB, "
          f"started {sum(o['engines_started'] for o in rows)}, released {sum(o['released_idle'] for o in rows)}", end='')
print()
