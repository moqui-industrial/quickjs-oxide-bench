| row | base us | w12 us | ratio | base allocs | w12 allocs |
|---|---:|---:|---:|---:|---:|
| value `a` (a bare name) | 0.41 | 0.40 | 0.976 | 0 | 0 |
| value `a + b * 2` | 0.60 | 0.57 | 0.950 | 0 | 0 |
| value `item.name` (a map's field) | 1.23 | 1.14 | 0.927 | 9 | 9 |
| value `{x: a, y: item.name}` (a new map) | 1.80 | 1.69 | 0.939 | 17 | 17 |
| value `price.multiply(dqty)` (decimals) | 1.64 | 1.54 | 0.939 | 13 | 13 |
| value `itemList.length` (100 maps) | 52.26 | 52.31 | 1.001 | 406 | 406 |
| condition `status == 'ACTIVE' && qty > 2` | 0.77 | 0.70 | 0.909 | 3 | 3 |
| expand `Item ${item.itemId}: ${item.name}` | 1.47 | 1.43 | 0.973 | 11 | 11 |
| expand plain text, no ${} | 0.02 | 0.02 | 1.000 | 1 | 1 |
| value `a + N`, new text each call | 4.58 | 4.60 | 1.004 | 83 | 83 |
| empty script | 0.19 | 0.18 | 0.947 | 0 | 0 |
| 1000 adds to a local | 8.54 | 8.00 | 0.937 | 0 | 0 |
| 1000 adds to a bare name (context) | 370.15 | 311.74 | 0.842 | 0 | 0 |
| 100 objects made and walked, locals | 22.45 | 22.41 | 0.998 | 100 | 100 |
| walk itemList, 100 context maps | 54.50 | 54.69 | 1.003 | 406 | 406 |
| 100 reads of item.name (context map) | 16.52 | 16.25 | 0.984 | 6 | 6 |
| 100 decimal multiply + add | 70.44 | 75.04 | 1.065 | 614 | 614 |
| 100 ec.user.nowTimestamp (host getter) | 32.85 | 34.11 | 1.038 | 502 | 502 |
| 10 cached entity finds | 41.27 | 40.80 | 0.989 | 486 | 466 |
| walk an entity list, 100 cached rows | 157.34 | 154.37 | 0.981 | 2331 | 2329 |
| 100 cache gets (a host method, a text argument) | 25.88 | 25.99 | 1.004 | 206 | 206 |
| 10 noop service calls | 88.00 | 78.44 | 0.891 | 820 | 590 |
| 10 noop service calls, itemList tracked | 164.99 | 155.00 | 0.939 | 1331 | 1101 |
| 1000 string concatenations | 101.67 | 101.61 | 0.999 | 1024 | 1024 |
| JSON stringify + parse of 100 objects | 70.29 | 70.26 | 1.000 | 422 | 422 |
| JSON.parse of the locked snapshot | 7.19 | 7.20 | 1.001 | 42 | 42 |
| 1000 numbers to text | 153.62 | 153.53 | 0.999 | 994 | 994 |
| split('') + charAt, 1000 chars | 46.87 | 46.27 | 0.987 | 5 | 5 |
| regexp scan of a 200-line log | 164.73 | 161.25 | 0.979 | 1578 | 1578 |
| empty actions | 0.29 | 0.65 | 2.241 | 0 | 0 |
| one set | 0.19 | 0.16 | 0.842 | 2 | 2 |
| four sets (the echo#Data body) | 0.48 | 0.36 | 0.750 | 4 | 4 |
| iterate 100 context maps with if and set | 229.29 | 213.26 | 0.930 | 1674 | 1674 |
| entity-find-one, cached | 4.56 | 3.83 | 0.840 | 44 | 31 |
| noop#Inline (empty actions) | 7.98 | 7.02 | 0.880 | 84 | 61 |
| set#One (one set) | 8.23 | 7.28 | 0.885 | 88 | 69 |
| echo#Inline (four sets) | 10.29 | 9.34 | 0.908 | 121 | 102 |
| echo#Script (the same, a .js file) | 13.62 | 11.78 | 0.865 | 143 | 124 |
| BasicServices.echo#Data (typed parameters) | 8.44 | 7.96 | 0.943 | 94 | 91 |
| loop#Actions (100 items, XML actions) | 300.83 | 283.80 | 0.943 | 2474 | 2452 |
| loop#Script (100 items, one script) | 51.05 | 50.08 | 0.981 | 349 | 326 |
| calc#Decimal (20 multiply + add) | 33.51 | 32.35 | 0.965 | 370 | 347 |
| call#Nested (service-call to set#One) | 17.09 | 15.99 | 0.936 | 169 | 143 |
| find#Cached (10 cached finds) | 51.42 | 51.07 | 0.993 | 567 | 524 |
| body#Large (a 5 KB body, three sets run) | 13.08 | 11.46 | 0.876 | 111 | 88 |
| call#Context (30 names, a 50-map list, 10 calls in-map context) | 482.31 | 229.55 | 0.476 | 6872 | 2165 |
| loop#Calls (20 service-calls in an iterate) | 238.45 | 229.98 | 0.964 | 2116 | 2033 |
| fancy, trusted (live context) | 47.92 | 32.19 | 0.672 | 244 | 121 |
| fancy, locked down (a snapshot) | 40.16 | 25.83 | 0.643 | 228 | 106 |
| Plain, html (one label) | 28.27 | 28.43 | 1.006 | 241 | 227 |
| Labels, html (40 expanded labels) | 237.70 | 224.12 | 0.943 | 1543 | 1447 |
| Single, html (form-single, 11 fields) | 309.72 | 321.06 | 1.037 | 2101 | 2044 |
| Single.qvt (form-single, 11 fields) | 504.53 | 502.63 | 0.996 | 3124 | 3059 |
| List, html, 20 rows | 1441.17 | 1431.72 | 0.993 | 11277 | 11169 |
| List, html, 100 rows | 6524.23 | 6502.37 | 0.997 | 53891 | 53464 |
| Plain.qvt | 30.66 | 25.02 | 0.816 | 228 | 217 |
| List.qvt, 100 rows | 10980.97 | 10953.41 | 0.997 | 70040 | 68998 |
| List, text, 100 rows | 2050.09 | 1960.09 | 0.956 | 19946 | 19520 |
| List, tui, 100 rows | 2395.27 | 2301.59 | 0.961 | 22253 | 21829 |
| Links, html, 100 rows | 6011.39 | 5964.13 | 0.992 | 52597 | 51266 |
| Links.qvt, 100 rows | 8871.78 | 9043.74 | 1.019 | 58350 | 57018 |
| Links, tui, 100 rows | 3522.54 | 3550.42 | 1.008 | 33891 | 32555 |
