#!/usr/bin/env python3
"""Self time by layer from `perf report --stdio --no-children --sort sym` text on stdin; top symbols of each layer."""
import re, sys
layers = {}
tops = {}
def layer(sym):
    s = sym
    if re.search(r'(_int_free|__libc_malloc|__rust_dealloc|_int_malloc|cfree|unlink_chunk)', s):
        return 'alloc/libc mem'
    if re.search(r'\b(malloc|free|realloc|calloc|_int_malloc|_int_free|cfree|memcpy|memmove|memset|memcmp|__memc|__mem|_int_realloc|malloc_consolidate|unlink_chunk)\b', s) or 'alloc::alloc' in s or '__rust_alloc' in s or '__rdl_' in s or 'speed::Counting' in s or 'GlobalAlloc' in s:
        return 'alloc/libc mem'
    m = re.match(r'\[.\] (<)?([a-z_0-9]+::[a-z_0-9:]+)', s)
    head = m.group(2) if m else s
    if head.startswith('moqui_core::script::oxide') or head.startswith('moqui_core::script::host'):
        return 'bindings'
    if 'quickjs_oxide::engine::api' in head:
        return 'fork API'
    if head.startswith('oxide_core') or head.startswith('quickjs_oxide') or head.startswith('oxide_regexp'):
        return 'engine core'
    if head.startswith('moqui_core::screen'):
        return 'framework: screen'
    if head.startswith('moqui_'):
        return 'framework: other'
    if 'quickjs_oxide::engine::api' in s:
        return 'fork API'
    if 'oxide_core::' in s or 'quickjs_oxide' in s or 'oxide_regexp' in s:
        return 'engine core'
    if 'moqui_core::script::oxide' in s or 'moqui_core::script::host' in s:
        return 'bindings'
    if 'moqui_core::screen' in s:
        return 'framework: screen'
    if 'moqui_core::' in s or 'moqui_lib::' in s or 'moqui_db' in s:
        return 'framework: other'
    if 'indexmap' in s or 'hashbrown' in s or 'core::hash' in s or 'foldhash' in s or 'std::collections' in s:
        return 'hash maps'
    if '[k]' in s:
        return 'kernel'
    return 'other'
for line in sys.stdin:
    m = re.match(r'\s+([\d.]+)%\s+(.*)$', line)
    if not m:
        continue
    pct, sym = float(m.group(1)), m.group(2).strip()
    l = layer(sym)
    layers[l] = layers.get(l, 0) + pct
    tops.setdefault(l, []).append((pct, sym))
total = sum(layers.values())
for l, p in sorted(layers.items(), key=lambda x: -x[1]):
    print(f'{p / total * 100:5.1f}%  {l}')
    for pct, sym in sorted(tops[l], reverse=True)[:int(sys.argv[1]) if len(sys.argv) > 1 else 6]:
        print(f'        {pct / total * 100:5.1f}%  {sym[:150]}')
