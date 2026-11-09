# R52 end pass: the slower no-host rows are code layout

The quiet pass showed rows with no host work slower in the final build (adds to a
local +9%, objects +9%, concatenation +7%, Plain.qvt +19%, value `a` +10%), with
allocations unchanged. They are not a code cost.

**Instructions are flat.** instructions:u per call (21 batches less 1, `ipc2.sh`),
two alternating passes:

| row | base | final |
|---|---|---|
| 1000 adds to a local | 243,901 / 243,598 | 246,367 / 243,540 |
| 100 objects made and walked | 512,841 / 520,764 | 521,408 / 517,156 |
| 1000 string concatenations | 1,889,452 / 1,891,291 | 1,894,439 / 1,890,198 |

**The interpreter is the same code.** `oxide_core::vm::interp::run_at` is 0x3dd3
bytes in both binaries, and its disassembly differs in one field offset only
(0x208 to 0x210, the realm field F1 added; `run_at-base-vs-final.diff`). The
adds row spends its time there.

**Bisect.** `build.sh` built js_speed at every point through the patch path, in
one target dir. `wall.sh` gives us/call, pinned to CPU 2, 3 alternating passes
(`wall.txt`). The adds row follows where `run_at` starts in its 64-byte line:

| build | mr-moqui | fork | run_at mod 64 | adds, us |
|---|---|---|---|---|
| base (git pin) | fb0e5f78 | 34ef6147 | 0x20 | 8.00-8.12 |
| a-base | fb0e5f78 | 34ef6147 | 0x20 | 8.01-8.06 |
| b-f1 | fb0e5f78 | 570f5b59 | 0x30 | 8.87-9.42 |
| c-f2 | fb0e5f78 | c64d537d | 0x30 | 8.80-9.04 |
| d-f3 | fb0e5f78 | ddba97fe | 0x30 | 8.99-9.40 |
| e-set | 9629dcdb | ddba97fe | 0x00 | 7.97-7.99 |
| f-oom | 6304f480 | ddba97fe | 0x30 | 8.80-9.40 |
| g-idle | ef319839 | ddba97fe | 0x30 | 8.68-9.28 |
| h-finds | 2ffd2725 | ddba97fe | 0x10 | 7.96-8.39 |
| i-walk | e7041354 | ddba97fe | 0x10 | 7.97-8.05 |
| j-final | e36b0c9b | ddba97fe | 0x00 | 8.01-8.05 |
| final (git pin) | e36b0c9b | ddba97fe | 0x30 | 9.41-9.46 |

The same source as the final, built through the patch path (j-final), runs the
adds row at the base's speed. Every build with `run_at` at 0x30 is slow, and
every other build is fast, on both sides of the bisect. The objects row moves
on its own pattern (e-set and final slow), which is another placement effect.
Concatenation (97.6-100.3), Plain.qvt (36-41) and value `a` (0.40-0.45) are
within run-to-run spread when pinned.

No change is made: the cost comes and goes with unrelated edits. Aligning the
interpreter's hot function would need an unstable compiler option.
