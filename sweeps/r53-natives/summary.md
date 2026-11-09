## fixed

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| numeric_local_loop | 208 | 6.19 | 207 | 6.19 | 0.99 | 1.0000 |
| numeric_coercion_loop | 249 | 6.03 | 250 | 6.03 | 1.00 | 1.0000 |
| local_read_with_setup | 235 | 5.97 | 225 | 5.97 | 0.96 | 1.0000 |
| local_read | 233 | 5.97 | 226 | 5.97 | 0.97 | 1.0000 |
| bigint_32 | 275 | 5.85 | 275 | 5.85 | 1.00 | 1.0000 |
| bigint_64 | 275 | 5.79 | 280 | 5.79 | 1.02 | 1.0000 |
| bigint_256 | 269 | 5.61 | 268 | 5.61 | 1.00 | 1.0000 |
| prop_read | 208 | 6.03 | 206 | 6.03 | 0.99 | 1.0000 |
| prop_write | 208 | 6.28 | 210 | 6.28 | 1.01 | 1.0000 |
| array_read | 230 | 6.70 | 229 | 6.70 | 1.00 | 1.0000 |
| array_write | 238 | 6.93 | 237 | 6.93 | 1.00 | 1.0000 |
| call0 | 237 | 5.70 | 238 | 5.70 | 1.00 | 1.0000 |
| string_bridge | 262 | 4.97 | 262 | 4.97 | 1.00 | 1.0000 |
| type_error | 278 | 5.32 | 274 | 5.32 | 0.99 | 1.0009 |
| tdz | 303 | 5.55 | 301 | 5.55 | 0.99 | 1.0003 |
| local_move | 177 | 5.36 | 174 | 5.36 | 0.98 | 1.0000 |
| argument_move | 177 | 5.41 | 179 | 5.41 | 1.01 | 1.0000 |
| number_owner_fallback | 164 | 4.94 | 162 | 4.94 | 0.99 | 1.0000 |
| object_move | 168 | 5.18 | 168 | 5.18 | 1.00 | 1.0000 |
| empty_loop | 203 | 6.14 | 209 | 6.14 | 1.03 | 1.0000 |

candidate / base time, geometric mean over 20 workloads: 1.00
candidate / base instructions, geometric mean over 20 workloads: 1.0001

## v8

| Workload | base ms | base G instr | candidate ms | candidate G instr | candidate / base time | candidate / base instr |
|---|---|---|---|---|---|---|
| v8-v7-richards | 865 | 18.55 | 853 | 18.55 | 0.99 | 1.0000 |
| v8-v7-deltablue | 800 | 18.37 | 837 | 18.38 | 1.05 | 1.0002 |
| v8-v7-crypto | 584 | 15.12 | 628 | 15.12 | 1.08 | 1.0000 |
| v8-v7-raytrace | 774 | 15.79 | 774 | 15.80 | 1.00 | 1.0001 |
| v8-v7-earley-boyer | 637 | 13.14 | 619 | 13.14 | 0.97 | 1.0000 |
| v8-v7-regexp | 718 | 15.10 | 712 | 15.11 | 0.99 | 1.0004 |
| v8-v7-splay | 1172 | 19.06 | 1168 | 19.06 | 1.00 | 1.0000 |
| v8-v7-navier-stokes | 849 | 22.63 | 842 | 22.63 | 0.99 | 1.0000 |

candidate / base time, geometric mean over 8 workloads: 1.01
candidate / base instructions, geometric mean over 8 workloads: 1.0001

## Gates

- Instruction gate (eight V8 v7 programs, at most ×1.02): pass
- Loop-size gate (run_at below 16384 bytes): 15743 bytes, pass
- Samples: all passed
