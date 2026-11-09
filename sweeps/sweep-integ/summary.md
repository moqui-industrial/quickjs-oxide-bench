## fixed

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| numeric_local_loop | 205 | 6.20 | 207 | 6.20 | 1.01 | 1.0000 |
| numeric_coercion_loop | 238 | 5.87 | 237 | 5.87 | 1.00 | 1.0000 |
| local_read_with_setup | 208 | 5.89 | 208 | 5.89 | 1.00 | 1.0000 |
| local_read | 208 | 5.89 | 209 | 5.89 | 1.00 | 1.0000 |
| bigint_32 | 269 | 5.82 | 271 | 5.82 | 1.01 | 1.0000 |
| bigint_64 | 266 | 5.75 | 266 | 5.75 | 1.00 | 1.0000 |
| bigint_256 | 258 | 5.58 | 258 | 5.58 | 1.00 | 1.0000 |
| prop_read | 198 | 6.00 | 202 | 6.00 | 1.02 | 1.0000 |
| prop_write | 200 | 6.24 | 200 | 6.24 | 1.00 | 1.0000 |
| array_read | 224 | 6.65 | 225 | 6.65 | 1.00 | 1.0000 |
| array_write | 237 | 6.88 | 237 | 6.88 | 1.00 | 1.0000 |
| call0 | 253 | 5.53 | 252 | 5.53 | 0.99 | 1.0000 |
| string_bridge | 234 | 4.85 | 236 | 4.85 | 1.01 | 1.0000 |
| type_error | 286 | 5.28 | 270 | 5.28 | 0.94 | 1.0008 |
| tdz | 313 | 5.52 | 295 | 5.52 | 0.94 | 0.9999 |
| local_move | 178 | 5.36 | 190 | 5.36 | 1.07 | 1.0000 |
| argument_move | 175 | 5.41 | 176 | 5.41 | 1.01 | 1.0000 |
| number_owner_fallback | 165 | 4.94 | 173 | 4.94 | 1.05 | 1.0000 |
| object_move | 169 | 5.18 | 172 | 5.18 | 1.01 | 1.0000 |
| empty_loop | 204 | 6.14 | 202 | 6.14 | 0.99 | 1.0000 |

candidate / base time, geometric mean over 20 workloads: 1.00
candidate / base instructions, geometric mean over 20 workloads: 1.0000

## v8

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| v8-v7-richards | 902 | 18.11 | 919 | 18.10 | 1.02 | 0.9994 |
| v8-v7-deltablue | 856 | 17.79 | 865 | 17.73 | 1.01 | 0.9969 |
| v8-v7-crypto | 582 | 15.00 | 588 | 14.99 | 1.01 | 0.9996 |
| v8-v7-raytrace | 781 | 15.54 | 777 | 15.53 | 1.00 | 0.9990 |
| v8-v7-earley-boyer | 633 | 12.92 | 634 | 12.92 | 1.00 | 1.0001 |
| v8-v7-regexp | 957 | 21.40 | 922 | 21.40 | 0.96 | 1.0000 |
| v8-v7-splay | 1161 | 18.68 | 1149 | 18.61 | 0.99 | 0.9964 |
| v8-v7-navier-stokes | 823 | 22.41 | 821 | 22.41 | 1.00 | 1.0000 |

candidate / base time, geometric mean over 8 workloads: 1.00
candidate / base instructions, geometric mean over 8 workloads: 0.9989

## Gates

- Instruction gate (eight V8 v7 programs, at most ×1.02): pass
- Loop-size gate (run_at below 16384 bytes): 15210 bytes, pass
- Samples: all passed
