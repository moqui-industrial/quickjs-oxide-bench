| row | base µs | final µs | ÷ | base allocs | final allocs |
|---|---:|---:|---:|---:|---:|
| value `a` (a bare name) | 0.40 | 0.44 | 1.10 | 0.0 | 0.0 |
| value `a + b * 2` | 0.60 | 0.63 | 1.05 | 0.0 | 0.0 |
| value `item.name` (a map's field) | 1.27 | 1.17 | 0.92 | 12.0 | 9.0 |
| value `{x: a, y: item.name}` (a new map) | 1.92 | 1.70 | 0.89 | 23.0 | 17.0 |
| value `price.multiply(dqty)` (decimals) | 1.51 | 1.47 | 0.97 | 12.0 | 12.0 |
| value `itemList.length` (100 maps) | 65.72 | 52.79 | 0.80 | 706.4 | 406.3 |
| condition `status == 'ACTIVE' && qty > 2` | 0.71 | 0.76 | 1.07 | 3.0 | 3.0 |
| expand `Item ${item.itemId}: ${item.name}` | 1.66 | 1.55 | 0.93 | 14.0 | 11.0 |
| expand plain text, no ${} | 0.02 | 0.02 | 1.00 | 1.0 | 1.0 |
| value `a + N`, new text each call | 1.08 | 1.22 | 1.13 | 13.0 | 13.0 |
| empty script | 0.18 | 0.19 | 1.06 | 0.0 | 0.0 |
| 1000 adds to a local | 8.02 | 8.77 | 1.09 | 0.0 | 0.0 |
| 1000 adds to a bare name (context) | 359.17 | 379.92 | 1.06 | 0.0 | 0.0 |
| 100 objects made and walked, locals | 22.94 | 24.91 | 1.09 | 100.1 | 100.1 |
| walk itemList, 100 context maps | 67.29 | 55.02 | 0.82 | 706.4 | 406.3 |
| 100 reads of item.name (context map) | 16.71 | 16.34 | 0.98 | 9.0 | 6.0 |
| 100 decimal multiply + add | 69.00 | 69.71 | 1.01 | 612.5 | 612.5 |
| 100 ec.user.nowTimestamp (host getter) | 32.15 | 32.59 | 1.01 | 502.1 | 502.1 |
| 10 cached entity finds | 45.13 | 39.87 | 0.88 | 576.1 | 486.1 |
| walk an entity list, 100 cached rows | 153.77 | 154.40 | 1.00 | 2339.4 | 2331.4 |
| 100 cache gets (a host method, a text argument) | 23.71 | 24.24 | 1.02 | 206.0 | 206.0 |
| 10 noop service calls | 86.95 | 87.04 | 1.00 | 820.0 | 820.0 |
| 10 noop service calls, itemList tracked | 187.07 | 163.24 | 0.87 | 1931.4 | 1331.3 |
| 1000 string concatenations | 97.36 | 103.73 | 1.07 | 1024.2 | 1024.1 |
| JSON stringify + parse of 100 objects | 69.90 | 71.45 | 1.02 | 421.5 | 421.5 |
| $esc over 100 strings | 40.57 | 41.05 | 1.01 | 320.2 | 320.2 |
| JSON.parse of the locked snapshot | 7.11 | 7.13 | 1.00 | 42.1 | 42.1 |
| 1000 numbers to text | 153.83 | 155.50 | 1.01 | 993.7 | 993.7 |
| split('') + charAt, 1000 chars | 45.21 | 45.56 | 1.01 | 5.2 | 5.2 |
| regexp scan of a 200-line log | 165.08 | 166.20 | 1.01 | 1578.2 | 1578.8 |
| empty actions | 0.28 | 0.29 | 1.04 | 0.0 | 0.0 |
| one set | 0.93 | 0.19 | 0.20 | 6.0 | 2.0 |
| four sets (the echo#Data body) | 2.91 | 0.48 | 0.16 | 26.0 | 4.0 |
| iterate 100 context maps with if and set | 260.71 | 233.44 | 0.90 | 2499.6 | 1674.5 |
| entity-find-one, cached | 4.84 | 4.45 | 0.92 | 53.0 | 44.0 |
| noop#Inline (empty actions) | 8.26 | 8.02 | 0.97 | 84.0 | 84.0 |
| set#One (one set) | 9.70 | 7.91 | 0.82 | 96.1 | 88.0 |
| echo#Inline (four sets) | 13.35 | 10.49 | 0.79 | 144.0 | 121.0 |
| echo#Script (the same, a .js file) | 13.25 | 13.19 | 1.00 | 143.0 | 143.0 |
| BasicServices.echo#Data (typed parameters) | 11.79 | 8.40 | 0.71 | 120.0 | 94.0 |
| loop#Actions (100 items, XML actions) | 340.94 | 306.97 | 0.90 | 3389.7 | 2474.5 |
| loop#Script (100 items, one script) | 60.63 | 52.58 | 0.87 | 570.3 | 349.3 |
| calc#Decimal (20 multiply + add) | 32.54 | 33.04 | 1.02 | 369.2 | 369.2 |
| call#Nested (service-call to set#One) | 18.14 | 16.98 | 0.94 | 180.0 | 169.0 |
| find#Cached (10 cached finds) | 56.38 | 50.78 | 0.90 | 657.1 | 567.1 |
| fancy, trusted (live context) | 49.20 | 46.70 | 0.95 | 303.5 | 243.4 |
| fancy, locked down (a snapshot) | 62.22 | 39.01 | 0.63 | 350.4 | 228.4 |
| Plain, html (one label) | 27.30 | 27.21 | 1.00 | 237.2 | 237.2 |
| Labels, html (40 expanded labels) | 234.58 | 226.92 | 0.97 | 1673.8 | 1538.3 |
| Single, html (form-single, 11 fields) | 318.88 | 309.69 | 0.97 | 2257.7 | 2109.2 |
| Single.qvt (form-single, 11 fields) | 523.47 | 506.18 | 0.97 | 3415.9 | 3125.3 |
| List, html, 20 rows | 1738.39 | 1784.68 | 1.03 | 13570.9 | 13348.9 |
| List, html, 100 rows | 8019.67 | 8289.01 | 1.03 | 65478.6 | 64375.5 |
| Plain.qvt | 24.74 | 29.42 | 1.19 | 224.2 | 224.4 |
| List.qvt, 100 rows | 12785.04 | 13314.74 | 1.04 | 79938.7 | 79134.2 |
| List, text, 100 rows | 2167.27 | 2143.55 | 0.99 | 23478.5 | 22662.0 |
| engine start (a thread's first script) | 1420.18 | 1420.00 | 1.00 | 6166.0 | 6182.0 |
| then first render, List html 20 rows | 2560.84 | 2522.98 | 0.99 | 15769.0 | 15539.0 |
| then a second screen, Plain html | 85.44 | 81.64 | 0.96 | 352.0 | 352.0 |

geometric mean ÷ over 59 rows: 0.913
