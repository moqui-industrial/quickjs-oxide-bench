## fixed

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| numeric_local_loop | 210 | 6.20 | 209 | 6.19 | 0.99 | 0.9999 |
| numeric_coercion_loop | 239 | 5.88 | 239 | 5.92 | 1.00 | 1.0070 |
| local_read_with_setup | 209 | 5.89 | 209 | 5.89 | 1.00 | 0.9999 |
| local_read | 208 | 5.89 | 209 | 5.89 | 1.00 | 0.9999 |
| bigint_32 | 270 | 5.84 | 271 | 5.84 | 1.00 | 0.9993 |
| bigint_64 | 267 | 5.78 | 267 | 5.77 | 1.00 | 0.9992 |
| bigint_256 | 258 | 5.60 | 257 | 5.60 | 0.99 | 0.9999 |
| prop_read | 198 | 6.00 | 198 | 6.00 | 1.00 | 0.9999 |
| prop_write | 201 | 6.24 | 197 | 6.23 | 0.98 | 0.9999 |
| array_read | 223 | 6.68 | 227 | 6.67 | 1.02 | 0.9999 |
| array_write | 234 | 6.88 | 235 | 6.88 | 1.01 | 0.9999 |
| call0 | 229 | 5.57 | 230 | 5.57 | 1.01 | 0.9998 |
| string_bridge | 235 | 4.85 | 234 | 4.84 | 1.00 | 0.9966 |
| type_error | 277 | 5.28 | 266 | 5.29 | 0.96 | 1.0015 |
| tdz | 305 | 5.52 | 287 | 5.53 | 0.94 | 1.0019 |
| local_move | 172 | 5.36 | 171 | 5.36 | 0.99 | 0.9998 |
| argument_move | 173 | 5.41 | 172 | 5.41 | 0.99 | 0.9998 |
| number_owner_fallback | 162 | 4.94 | 161 | 4.94 | 1.00 | 0.9998 |
| object_move | 168 | 5.18 | 167 | 5.18 | 1.00 | 0.9998 |
| empty_loop | 210 | 6.14 | 207 | 6.14 | 0.99 | 0.9999 |

candidate / base time, geometric mean over 20 workloads: 0.99
candidate / base instructions, geometric mean over 20 workloads: 1.0002

## v8

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| v8-v7-richards | 816 | 18.18 | 831 | 18.18 | 1.02 | 0.9999 |
| v8-v7-deltablue | 781 | 17.90 | 766 | 17.85 | 0.98 | 0.9974 |
| v8-v7-crypto | 585 | 15.03 | 606 | 15.03 | 1.04 | 1.0000 |
| v8-v7-raytrace | 746 | 15.53 | 745 | 15.53 | 1.00 | 1.0000 |
| v8-v7-earley-boyer | 596 | 12.92 | 591 | 12.90 | 0.99 | 0.9984 |
| v8-v7-regexp | 942 | 21.40 | 818 | 17.23 | 0.87 | 0.8051 |
| v8-v7-splay | 1129 | 18.79 | 1138 | 19.03 | 1.01 | 1.0123 |
| v8-v7-navier-stokes | 825 | 22.48 | 820 | 22.48 | 0.99 | 1.0000 |

candidate / base time, geometric mean over 8 workloads: 0.99
candidate / base instructions, geometric mean over 8 workloads: 0.9742

## Gates

- Instruction gate (eight V8 v7 programs, at most ×1.02): pass
- Loop-size gate (run_at below 16384 bytes): 15251 bytes, pass
- Samples: all passed
