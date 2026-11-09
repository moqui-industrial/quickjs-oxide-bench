# Round 52: the quiet pass

The round's base, mr-moqui fb0e5f78 on fork 34ef6147, against the final, mr-moqui e36b0c9b on fork ddba97fe. Both are
release builds with debug info. Two runs each, alternating, with nothing else running (`run.sh`). `table.md` comes from
`tools/js-speed-table.py base-run1.txt base-run2.txt -- final-run1.txt final-run2.txt`. Over the 59 rows the geometric
mean is ×0.913.

The +7 to +19% on rows with no host work (1000 adds to a local, 100 objects, Plain.qvt) is code placement, not code:
see `../layout-bisect`.

The suites on the final passed: the fork's full suite and the focused Test262 run; mr-moqui test-framework, cargo test
--workspace (71 binaries) and test-apps (3410/3410). The largest test-apps process peaked at 62.4 MB.
