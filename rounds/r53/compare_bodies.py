#!/usr/bin/env python3
"""Compare the body-*.out files of two screen_bench.py outputs: python3 -I compare_bodies.py <dirA> <dirB> [--show N]

Build stamps and hashes are masked in both; each differing case prints its first differing lines (split at '>')."""
import difflib, os, re, sys
a, b = sys.argv[1], sys.argv[2]
show = int(sys.argv[sys.argv.index("--show") + 1]) if "--show" in sys.argv else 6
def norm(p):
    d = open(p, "rb").read().decode("utf-8", "replace")
    d = re.sub(r"\?v=(<stamp>|[0-9a-f]+)", "?v=S", d)
    d = re.sub(r'"(<hash>|[0-9a-f]{40})"', '"H"', d)
    return d.replace(">", ">\n").splitlines()
for name in sorted(os.listdir(a)):
    if not name.startswith("body-") or not os.path.exists(os.path.join(b, name)):
        continue
    x, y = norm(os.path.join(a, name)), norm(os.path.join(b, name))
    if x == y:
        print(f"{name:22} same")
        continue
    diff = [l for l in difflib.unified_diff(x, y, lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
    print(f"{name:22} DIFF {len(diff)} lines")
    for l in diff[:show]:
        print("      " + l[:160])
