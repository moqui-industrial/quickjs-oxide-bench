## fixed

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| numeric_local_loop | 206 | 6.19 | 213 | 6.19 | 1.03 | 1.0000 |
| numeric_coercion_loop | 240 | 5.92 | 240 | 5.92 | 1.00 | 1.0000 |
| local_read_with_setup | 208 | 5.89 | 205 | 5.89 | 0.99 | 1.0000 |
| local_read | 208 | 5.89 | 206 | 5.89 | 0.99 | 1.0000 |
| bigint_32 | 271 | 5.84 | 269 | 5.82 | 0.99 | 0.9969 |
| bigint_64 | 268 | 5.77 | 268 | 5.75 | 1.00 | 0.9969 |
| bigint_256 | 258 | 5.60 | 257 | 5.58 | 1.00 | 0.9970 |
| prop_read | 198 | 6.00 | 207 | 6.00 | 1.04 | 1.0000 |
| prop_write | 199 | 6.23 | 202 | 6.23 | 1.01 | 1.0000 |
| array_read | 226 | 6.67 | 219 | 6.67 | 0.97 | 1.0000 |
| array_write | 236 | 6.88 | 237 | 6.88 | 1.00 | 1.0000 |
| call0 | 231 | 5.57 | 230 | 5.57 | 0.99 | 1.0000 |
| string_bridge | 234 | 4.84 | 234 | 4.82 | 1.00 | 0.9975 |
| type_error | 274 | 5.40 | 276 | 5.39 | 1.01 | 0.9987 |
| tdz | 289 | 5.51 | 296 | 5.50 | 1.02 | 0.9988 |
| local_move | 173 | 5.36 | 194 | 5.36 | 1.12 | 1.0000 |
| argument_move | 172 | 5.41 | 184 | 5.41 | 1.07 | 1.0000 |
| number_owner_fallback | 161 | 4.94 | 179 | 4.94 | 1.11 | 1.0000 |
| object_move | 168 | 5.18 | 180 | 5.18 | 1.07 | 1.0000 |
| empty_loop | 209 | 6.14 | 215 | 6.14 | 1.03 | 1.0000 |

candidate / base time, geometric mean over 20 workloads: 1.02
candidate / base instructions, geometric mean over 20 workloads: 0.9993

## v8

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| v8-v7-richards | 823 | 18.18 | 847 | 18.18 | 1.03 | 1.0000 |
| v8-v7-deltablue | 771 | 17.85 | 766 | 17.85 | 0.99 | 0.9999 |
| v8-v7-crypto | 599 | 15.03 | 607 | 15.03 | 1.01 | 1.0000 |
| v8-v7-raytrace | 746 | 15.53 | 744 | 15.51 | 1.00 | 0.9990 |
| v8-v7-earley-boyer | 593 | 12.90 | 603 | 12.89 | 1.02 | 0.9991 |
| v8-v7-regexp | 835 | 17.22 | 823 | 17.22 | 0.99 | 0.9998 |
| v8-v7-splay | 1145 | 19.03 | 1147 | 19.00 | 1.00 | 0.9984 |
| v8-v7-navier-stokes | 824 | 22.48 | 820 | 22.48 | 1.00 | 1.0000 |

candidate / base time, geometric mean over 8 workloads: 1.00
candidate / base instructions, geometric mean over 8 workloads: 0.9995

## Gates

- Instruction gate (eight V8 v7 programs, at most ×1.02): pass
- Loop-size gate (run_at below 16384 bytes): 15251 bytes, pass
- Samples: all passed
