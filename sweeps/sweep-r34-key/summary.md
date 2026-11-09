## fixed

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| numeric_local_loop | 207 | 6.19 | 206 | 6.19 | 1.00 | 1.0000 |
| numeric_coercion_loop | 240 | 5.92 | 241 | 5.92 | 1.00 | 1.0000 |
| local_read_with_setup | 208 | 5.89 | 208 | 5.89 | 1.00 | 1.0000 |
| local_read | 208 | 5.89 | 208 | 5.89 | 1.00 | 1.0000 |
| bigint_32 | 271 | 5.84 | 272 | 5.84 | 1.00 | 1.0000 |
| bigint_64 | 268 | 5.77 | 269 | 5.77 | 1.01 | 1.0000 |
| bigint_256 | 260 | 5.60 | 259 | 5.60 | 1.00 | 1.0000 |
| prop_read | 200 | 6.00 | 199 | 6.00 | 1.00 | 1.0000 |
| prop_write | 199 | 6.23 | 199 | 6.23 | 1.00 | 1.0000 |
| array_read | 227 | 6.67 | 228 | 6.67 | 1.00 | 1.0000 |
| array_write | 236 | 6.88 | 236 | 6.88 | 1.00 | 1.0000 |
| call0 | 230 | 5.57 | 230 | 5.57 | 1.00 | 1.0000 |
| string_bridge | 234 | 4.84 | 234 | 4.84 | 1.00 | 1.0000 |
| type_error | 279 | 5.41 | 272 | 5.40 | 0.97 | 0.9997 |
| tdz | 295 | 5.51 | 286 | 5.51 | 0.97 | 1.0001 |
| local_move | 172 | 5.36 | 173 | 5.36 | 1.01 | 1.0000 |
| argument_move | 173 | 5.41 | 172 | 5.41 | 0.99 | 1.0000 |
| number_owner_fallback | 161 | 4.94 | 162 | 4.94 | 1.01 | 1.0000 |
| object_move | 168 | 5.18 | 169 | 5.18 | 1.00 | 1.0000 |
| empty_loop | 208 | 6.14 | 209 | 6.14 | 1.01 | 1.0000 |

candidate / base time, geometric mean over 20 workloads: 1.00
candidate / base instructions, geometric mean over 20 workloads: 1.0000

## v8

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| v8-v7-richards | 838 | 18.18 | 840 | 18.18 | 1.00 | 1.0000 |
| v8-v7-deltablue | 768 | 17.85 | 770 | 17.85 | 1.00 | 1.0000 |
| v8-v7-crypto | 604 | 15.03 | 626 | 15.03 | 1.04 | 1.0000 |
| v8-v7-raytrace | 747 | 15.53 | 749 | 15.53 | 1.00 | 1.0000 |
| v8-v7-earley-boyer | 593 | 12.90 | 590 | 12.90 | 0.99 | 1.0000 |
| v8-v7-regexp | 820 | 17.22 | 821 | 17.22 | 1.00 | 1.0000 |
| v8-v7-splay | 1150 | 19.03 | 1145 | 19.03 | 1.00 | 1.0000 |
| v8-v7-navier-stokes | 821 | 22.48 | 822 | 22.48 | 1.00 | 1.0000 |

candidate / base time, geometric mean over 8 workloads: 1.00
candidate / base instructions, geometric mean over 8 workloads: 1.0000

## Gates

- Instruction gate (eight V8 v7 programs, at most ×1.02): pass
- Loop-size gate (run_at below 16384 bytes): 15251 bytes, pass
- Samples: all passed
