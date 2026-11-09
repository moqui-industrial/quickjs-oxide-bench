# R51: the atom census on mr-mantle's specs

What share of a busy mr-mantle service worker's atoms are code atoms, for the shared-atoms design
(quickjs-oxide `perf/shared-atoms`, `docs/shared-atoms.md`).

## Setup

- Fork: main 1cdb77e2 with the census probe 8f76bcac cherry-picked (code only, not the doc), in a detached worktree,
  plus three local additions (`fork-census.diff`):
  - the census line names the thread: `atom census [<thread>]: ...`;
  - `atom census image [<thread>]`: of the non-builtin atoms an image unit names (keys, names) or an image function's
    constants hold, how many are named by code only, held as constants only, or both, and how many are image keys;
  - `atom census sample [<thread>] <class>`: with `QJS_ATOM_CENSUS_SAMPLES=12`, 12 texts spread evenly over each of the
    constants, object keys and other classes;
  - the fresh runtime's builtin texts are kept in a process `OnceLock`, not a thread local, so a census can run while
    a thread's locals are being destroyed.
- mr-moqui: master f72fc796 (pinned to 1cdb77e2; start texts from code images, 361f4c8e) in a detached worktree, with
  one local hook (`mr-moqui-hook.diff`): `OxideEngine::drop` collects and takes a memory report, so a runtime's census
  is printed after a collection before it goes (`atom census drop [<thread>] runtime=<addr>`).
- Run: `QJS_ATOM_CENSUS=1 QJS_ATOM_CENSUS_SAMPLES=12 MOQUI_SCRIPT_STATS_FILE=... ./moq test mr-mantle --nobuild`,
  Maximal release build. 1947 features, 1933 passed, 3 failed (SupportAssignment round robin, WorkTimeEntries,
  WorkTimesheets: unrelated to the probe), 11 skipped, 324 s.
- Reports: mr-moqui samples each runtime's heap at most every 250 ms at the end of an outermost run
  (`sample_heap_now`), so every worker runtime is counted many times: 7915 census rows over 34 threads. These rows are
  without a collection, so "other" holds some garbage. 228 runtimes were started, 84 released idle, at most 31 live.
- Drop censuses: 61 printed (43 test-parallel, 11 main, 5 worker, 1 job, 1 request). Most worker runtimes are dropped
  at thread exit, where the census panics on a thread local outside the probe (caught: `catch_unwind`), so the worker
  tables below are of the periodic reports.

Classes (each atom once, in its first class): builtin (a fresh runtime's texts), image code (named by a unit loaded
from a code image: key, name), static code (a unit the runtime compiled into its code store), dynamic code (a run-time
unit), constants (a string literal of a live function and nothing above), object keys (a live shape's key and nothing
above), other.

## Per thread, at its peak report

Each thread's report with the most atoms; "Code share" is image + static + dynamic + constants. "Last" is the thread's
last report (a worker thread's runtime may have been released and restarted between them).

| Thread | Reports | Peak atoms (units) | Builtin | Image code | Static code | Dynamic code | Constants | Object keys | Other | Code share | Last |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| main | 1085 | 23025 (439.5k) | 512 | 8899 | 1110 | 2052 | 9751 | 264 | 437 | 95% | 19313 |
| moqui-worker-12 | 292 | 9831 (160.9k) | 512 | 5014 | 99 | 0 | 3874 | 216 | 116 | 91% | 4690 |
| moqui-worker-5 | 300 | 9787 (164.9k) | 512 | 5144 | 22 | 0 | 3695 | 245 | 169 | 91% | 4728 |
| moqui-worker-2 | 288 | 9731 (161.0k) | 512 | 5013 | 2 | 0 | 3845 | 244 | 115 | 91% | 4719 |
| moqui-worker-4 | 288 | 9665 (159.1k) | 512 | 5009 | 0 | 0 | 3804 | 223 | 117 | 91% | 5714 |
| moqui-worker-13 | 306 | 7275 (112.4k) | 512 | 3775 | 0 | 0 | 2639 | 227 | 122 | 88% | 4881 |
| moqui-worker-6 | 290 | 7097 (114.3k) | 512 | 3801 | 0 | 0 | 2362 | 247 | 175 | 87% | 5672 |
| moqui-worker-15 | 278 | 6949 (106.6k) | 512 | 3626 | 0 | 0 | 2457 | 232 | 122 | 88% | 5425 |
| moqui-worker-18 | 304 | 6837 (104.1k) | 512 | 3529 | 0 | 0 | 2426 | 224 | 146 | 87% | 5681 |
| moqui-worker-19 | 290 | 6800 (106.3k) | 512 | 3647 | 0 | 0 | 2209 | 252 | 180 | 86% | 5514 |
| moqui-worker-7 | 306 | 6520 (97.9k) | 512 | 3449 | 0 | 0 | 2104 | 294 | 161 | 85% | 6470 |
| moqui-worker-16 | 320 | 6515 (94.7k) | 512 | 3429 | 0 | 0 | 2128 | 282 | 164 | 85% | 6515 |
| moqui-worker-3 | 274 | 6216 (91.8k) | 512 | 3296 | 0 | 0 | 1959 | 285 | 164 | 85% | 6216 |
| moqui-test-parallel-0 | 73 | 6154 (103.4k) | 512 | 2057 | 1170 | 0 | 1968 | 231 | 216 | 84% | 3678 |
| moqui-test-parallel-4 | 3 | 6150 (103.4k) | 512 | 3223 | 5 | 0 | 1972 | 231 | 207 | 85% | 6150 |
| moqui-test-parallel-1 | 37 | 6098 (102.9k) | 512 | 3223 | 0 | 0 | 1966 | 231 | 166 | 85% | 3677 |
| moqui-test-parallel-3 | 3 | 6098 (102.9k) | 512 | 3223 | 0 | 0 | 1966 | 231 | 166 | 85% | 6098 |
| moqui-test-parallel-2 | 6 | 6098 (102.9k) | 512 | 3223 | 0 | 0 | 1966 | 231 | 166 | 85% | 2076 |
| moqui-worker-22 | 290 | 6039 (86.6k) | 512 | 3186 | 1 | 0 | 1863 | 312 | 165 | 84% | 6014 |
| moqui-worker-1 | 289 | 5787 (85.7k) | 512 | 2627 | 381 | 0 | 1817 | 253 | 197 | 83% | 5563 |
| moqui-worker-14 | 292 | 5694 (86.3k) | 512 | 3031 | 4 | 0 | 1702 | 263 | 182 | 83% | 5569 |
| moqui-worker-8 | 274 | 5691 (80.4k) | 512 | 3016 | 0 | 0 | 1711 | 287 | 165 | 83% | 5691 |
| moqui-worker-0 | 293 | 5620 (81.6k) | 512 | 2899 | 0 | 0 | 1739 | 306 | 164 | 83% | 5620 |
| moqui-worker-11 | 291 | 5503 (82.1k) | 512 | 2849 | 19 | 0 | 1647 | 304 | 172 | 82% | 4280 |
| moqui-worker-10 | 289 | 5277 (76.1k) | 512 | 2776 | 22 | 0 | 1497 | 305 | 165 | 81% | 5104 |
| moqui-worker-21 | 287 | 5012 (70.3k) | 512 | 2646 | 0 | 0 | 1385 | 298 | 171 | 80% | 4934 |
| moqui-worker-20 | 284 | 4985 (69.2k) | 512 | 2289 | 347 | 0 | 1346 | 312 | 179 | 80% | 4980 |
| moqui-worker-9 | 272 | 4869 (69.6k) | 512 | 2544 | 0 | 0 | 1355 | 292 | 166 | 80% | 4075 |
| moqui-worker-17 | 298 | 4732 (66.6k) | 512 | 2437 | 0 | 0 | 1315 | 301 | 167 | 79% | 4306 |
| moqui-job-0 | 3 | 2511 (29.0k) | 512 | 937 | 332 | 0 | 334 | 219 | 177 | 64% | 2511 |
| moqui-request-1 | 1 | 2401 (28.2k) | 512 | 1157 | 0 | 0 | 300 | 253 | 179 | 61% | 2401 |
| moqui-request-0 | 2 | 2216 (24.8k) | 512 | 991 | 45 | 0 | 218 | 270 | 180 | 57% | 2198 |
| moqui-request-3 | 2 | 2190 (24.4k) | 512 | 1026 | 0 | 0 | 214 | 264 | 174 | 57% | 2190 |
| moqui-job-1 | 5 | 2120 (23.3k) | 512 | 937 | 66 | 0 | 205 | 225 | 175 | 57% | 2120 |

`main` is the spec runner's thread (the main and spec runtimes, which compile and make the images), not a service
worker. Its drop censuses after a collection (11; ten of 18.1k to 22.3k atoms, one of 9.0k) have the same shape:
8k to 9.6k image code, 7.6k to 9.7k constants, 166 to 200 object keys, 160 to 290 other.

The periodic reports run without a collection, but the peaks are not garbage: moqui-worker-4's runtime, collected at
its drop, still had 9634 atoms (512, 5009, 0, 0, 3804, 192, 117) against its peak report's 9665.

## The busiest workers

The four busiest service workers peak at 9.7k to 9.8k atoms (R49 saw about 11k): 512 builtin, about 5.0k image code,
3.7k to 3.9k constants, 0 to 99 static code, 216 to 245 object keys and 115 to 169 other. Code atoms are 91%, and
with builtin 96%. By text the constants are the larger part: 95k of the 160k units.

| Class | Atoms (4 busiest) | Share | Units | Share |
| --- | ---: | ---: | ---: | ---: |
| builtin | 2048 | 5.2% | 18.5k | 2.9% |
| image code | 20180 | 51.7% | 227.7k | 35.2% |
| static code | 123 | 0.3% | 1.4k | 0.2% |
| dynamic code | 0 | 0.0% | 0 | 0.0% |
| constants | 15218 | 39.0% | 379.8k | 58.8% |
| object keys | 928 | 2.4% | 12.3k | 1.9% |
| other | 517 | 1.3% | 6.3k | 1.0% |

## Aggregate

Each thread's peak report, summed.

| Class | All 34 threads | Share | Units | Share | 23 service workers | Share | Units | Share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| builtin | 17408 | 8.0% | 157.0k | 4.6% | 11776 | 7.7% | 106.2k | 4.6% |
| image code | 107928 | 49.6% | 1227.0k | 36.0% | 79032 | 51.8% | 886.3k | 38.1% |
| static code | 3625 | 1.7% | 41.7k | 1.2% | 897 | 0.6% | 9.4k | 0.4% |
| dynamic code | 2052 | 0.9% | 27.2k | 0.8% | 0 | 0.0% | 0 | 0.0% |
| constants | 71739 | 33.0% | 1776.5k | 52.1% | 50879 | 33.4% | 1202.4k | 51.6% |
| object keys | 8854 | 4.1% | 114.7k | 3.4% | 6204 | 4.1% | 80.7k | 3.5% |
| other | 5887 | 2.7% | 68.9k | 2.0% | 3644 | 2.4% | 43.5k | 1.9% |
| total | 217493 | | 3413.1k | | 152432 | | 2328.4k | |

Over the service workers, code atoms are 86% (94% with builtin); object keys and other together are 6.5%, about 250
to 300 keys and 115 to 200 others a worker, whatever its size. The worker's growth past its ~2.2k start is all image
code and constants.

## Image atoms: constants against keys and names

From `atom census image`, at each thread's peak (non-builtin atoms only). "Keys/names only" are named by an image unit
and are not an image function's constant; "constants only" are an image function's string constant and no image
unit's key or name; "both" are both.

| | Keys/names only | Constants only | Both | Of which image keys |
| --- | ---: | ---: | ---: | ---: |
| 4 busiest workers | 17092 (48.4%) | 15128 (42.8%) | 3088 (8.7%) | 19235 |
| 23 service workers | 69221 (53.6%) | 50112 (38.8%) | 9811 (7.6%) | 75617 |
| moqui-worker-12 | 4244 | 3812 | 770 | 4786 |

So about 40% of a worker's image atoms are held only as string constants, and their text is the larger part (the
constants class is 52% of the units). Nearly all of the constants class is image constants: 50112 of the workers'
50879 constants-class atoms (98.5%). Image code atoms are almost all keys (75.6k of 79.0k); the rest are function
names. Phase 2 of the design has to share the constants with the keys.

## What the object keys and other texts are

Samples spread over each class at the peak reports (`census-peaks.txt` has all of them, per thread):

- **Object keys** (216 to 312 a worker): the host table's method names and the host objects' properties
  (`setTimeZone`, `sendJsonResponse`, `resolveEntityName`, `getUserGroupIdSet`, `hasElasticApi`, `moveFile`,
  `base64UrlEncode`, `jobWorkerPool`, `engines`, `llm`), DOMException's constant names (`INDEX_SIZE_ERR`,
  `QUOTA_EXCEEDED_ERR`, `TIMEOUT_ERR`), and entity field names from entity values and maps (`externalId`,
  `historySeqId`, `vendorRoles`, `prePaymentsTotal`, `grandTotal`, `_timestamp`).
- **Other** (115 to 200 a worker): one-character strings (`"0"`, `"9"`, `"z"`), the `Intl` display names of
  languages and locales (`"French"`, `"German (Switzerland)"`, `"Spanish (Mexico)"`), HTTP header names (`trailer`,
  `upgrade`, `transfer-encoding`, `proxy-authenticate`), screen render callback names (`renderIncludeScreen`,
  `getFormInstance`, `getMenuData`, `xlsxCell`, `safeCloseList`), `"Symbol."`, `__moquiHostTable`, and some
  enumeration and status ids from data (`GLREC_CREATED`, `MKTG_CAMP_COMPLETED`). Some are garbage that the next
  collection frees: these reports run without one.
- **Constants** for comparison: service and entity names (`mantle.account.PaymentServices.check#InvoiceStatusForPayment`,
  `create#mantle.order.OrderItemWorkEffort`), component locations, error ids and messages (`"Staff edits require a
  reason"`), status ids, HTML fragments and regexps.

## Files

- `census-peaks.txt`: the census lines, trimmed: per thread its peak report (with its image split and samples), its
  last report, and every drop report. The full stderr (12 MB, 7915 reports) stays in `work/r51-census/test.stderr`.
- `fork-census.diff`: the fork worktree's change against 1cdb77e2 (the cherry-picked census plus the additions above).
- `mr-moqui-hook.diff`: the mr-moqui worktree's drop hook.
