#!/usr/bin/env python3
"""Per thread, the atom census report with the most atoms and the one with the most reserved bytes, from a
QJS_ATOM_CENSUS stderr in r51's phase-2 format:
`atom census [thread] reserved=R live=L: atoms N (U units), S shared: builtin ..., ...[; the process shares A (U units, B bytes)]`."""
import re, sys
line_re = re.compile(r'^atom census \[([^\]]*)\] reserved=(\d+) live=(\d+): atoms (\d+) \((\d+) units\), (\d+) shared: (.*?)(?:; the process shares (\d+) \((\d+) units, (\d+) bytes\))?$')
cls_re = re.compile(r'([a-z ]+) (\d+) \((\d+)\)')
peaks, reserved, last_process = {}, {}, None
for line in open(sys.argv[1], errors='replace'):
    m = line_re.match(line.rstrip('\n'))
    if not m:
        continue
    thread, res, live = m.group(1), int(m.group(2)), int(m.group(3))
    atoms, units, shared = int(m.group(4)), int(m.group(5)), int(m.group(6))
    classes = {c.strip(): int(n) for c, n, _ in cls_re.findall(m.group(7))}
    if m.group(8):
        last_process = tuple(int(m.group(i)) for i in (8, 9, 10))
    if thread not in peaks or atoms > peaks[thread][0]:
        peaks[thread] = (atoms, units, shared, classes, res, live)
    reserved[thread] = max(reserved.get(thread, 0), res)
print('| Thread | Peak atoms (units) | Shared | Own | Image code | Constants | Object keys | Other | Reserved at the peak | Most reserved |')
print('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for thread, (atoms, units, shared, c, res, live) in sorted(peaks.items(), key=lambda kv: -kv[1][0]):
    print(f"| {thread} | {atoms} ({units/1000:.1f}k) | {shared} | {atoms-shared} | {c.get('image code',0)} | {c.get('constants',0)} | {c.get('object keys',0)} | {c.get('other',0)} | {res/1024:.0f} KiB | {reserved[thread]/1024:.0f} KiB |")
workers = [v for k, v in reserved.items() if 'worker' in k]
print(f"\nService workers: {len(workers)}, most reserved summed {sum(workers)/1048576:.1f} MiB.")
if last_process:
    print(f"The process's shared table at the last report: {last_process[0]} atoms, {last_process[1]} units, {last_process[2]} bytes.")
