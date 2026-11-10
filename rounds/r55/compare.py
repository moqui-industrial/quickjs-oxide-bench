"""usage: compare.py DIR PREFIX A B -- best of the runs DIR/PREFIX-{A,B}-N.txt of js_speed rows: us/call and allocations."""
import re, glob, sys
W, P, A, B = sys.argv[1:5]
def load(t):
    rows = {}
    for f in sorted(glob.glob(f'{W}/{P}-{t}-*.txt')):
        for l in open(f):
            m = re.match(r'  (.+?)\s{2,}(\d+)\s+([\d.]+)\s+([\d.]+)\s+\d+\s+([\d.]+)', l)
            if m:
                rows.setdefault(m.group(1), []).append((float(m.group(4)), float(m.group(5))))
    return rows
a, b = load(A), load(B)
print(f"| row | {A} us | {B} us | ratio | {A} allocs | {B} allocs |\n|---|---:|---:|---:|---:|---:|")
for k in a:
    if k in b:
        x = min(v[0] for v in a[k]); y = min(v[0] for v in b[k])
        print(f"| {k} | {x:.2f} | {y:.2f} | {y / x:.3f} | {a[k][0][1]:.0f} | {b[k][0][1]:.0f} |")
