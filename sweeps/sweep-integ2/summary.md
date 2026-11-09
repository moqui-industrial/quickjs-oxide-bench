## fixed

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| numeric_local_loop | 206 | 6.20 | 206 | 6.20 | 1.00 | 1.0000 |
| numeric_coercion_loop | 237 | 5.87 | 237 | 5.88 | 1.00 | 1.0006 |
| local_read_with_setup | 208 | 5.89 | 208 | 5.89 | 1.00 | 1.0000 |
| local_read | 209 | 5.89 | 209 | 5.89 | 1.00 | 1.0000 |
| bigint_32 | 269 | 5.82 | 270 | 5.84 | 1.00 | 1.0037 |
| bigint_64 | 267 | 5.75 | 266 | 5.78 | 1.00 | 1.0038 |
| bigint_256 | 265 | 5.58 | 258 | 5.60 | 0.97 | 1.0036 |
| prop_read | 199 | 6.00 | 201 | 6.00 | 1.01 | 1.0000 |
| prop_write | 200 | 6.24 | 201 | 6.24 | 1.01 | 1.0000 |
| array_read | 222 | 6.65 | 223 | 6.68 | 1.00 | 1.0036 |
| array_write | 236 | 6.88 | 234 | 6.88 | 0.99 | 1.0000 |
| call0 | 252 | 5.53 | 229 | 5.57 | 0.91 | 1.0070 |
| string_bridge | 235 | 4.85 | 236 | 4.85 | 1.00 | 1.0000 |
| type_error | 278 | 5.39 | 292 | 5.39 | 1.05 | 1.0003 |
| tdz | 294 | 5.50 | 310 | 5.50 | 1.06 | 0.9999 |
| local_move | 190 | 5.36 | 172 | 5.36 | 0.91 | 1.0000 |
| argument_move | 179 | 5.41 | 172 | 5.41 | 0.96 | 1.0000 |
| number_owner_fallback | 175 | 4.94 | 166 | 4.94 | 0.94 | 1.0000 |
| object_move | 173 | 5.18 | 167 | 5.18 | 0.97 | 1.0000 |
| empty_loop | 202 | 6.14 | 210 | 6.14 | 1.04 | 1.0000 |

candidate / base time, geometric mean over 20 workloads: 0.99
candidate / base instructions, geometric mean over 20 workloads: 1.0011

## v8

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| v8-v7-richards | 924 | 18.10 | 842 | 18.18 | 0.91 | 1.0044 |
| v8-v7-deltablue | 872 | 17.73 | 791 | 17.90 | 0.91 | 1.0095 |
| v8-v7-crypto | 597 | 14.99 | 601 | 15.03 | 1.01 | 1.0026 |
| v8-v7-raytrace | 773 | 15.53 | 740 | 15.53 | 0.96 | 0.9999 |
| v8-v7-earley-boyer | 638 | 12.92 | 595 | 12.92 | 0.93 | 1.0006 |
| v8-v7-regexp | 929 | 21.40 | 946 | 21.40 | 1.02 | 0.9999 |
| v8-v7-splay | 1146 | 18.61 | 1127 | 18.79 | 0.98 | 1.0098 |
| v8-v7-navier-stokes | 823 | 22.41 | 818 | 22.48 | 0.99 | 1.0031 |

candidate / base time, geometric mean over 8 workloads: 0.96
candidate / base instructions, geometric mean over 8 workloads: 1.0037

## Gates

- Instruction gate (eight V8 v7 programs, at most ×1.02): pass
- Loop-size gate (run_at below 16384 bytes): 15251 bytes, pass
- Samples: all passed
