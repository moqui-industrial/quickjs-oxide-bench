#!/usr/bin/env python3
"""Inclusive share of samples whose stack holds each pattern: python3 -I inclusive.py <perf script -F ip,sym output> pat..."""
import sys
stacks, cur = [], []
for line in open(sys.argv[1]):
    line = line.strip()
    if not line:
        if cur: stacks.append(" | ".join(cur)); cur = []
        continue
    parts = line.split(None, 1)
    cur.append(parts[1] if len(parts) > 1 else parts[0])
if cur: stacks.append(" | ".join(cur))
n = len(stacks)
for pat in sys.argv[2:]:
    k = sum(1 for s in stacks if pat in s)
    print(f"{100 * k / n:6.1f}%  {pat}")
