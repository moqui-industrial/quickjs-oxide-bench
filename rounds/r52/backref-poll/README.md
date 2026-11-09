# R52 F3: back-references are polled

Branch fix/backref-poll on fork main c64d537d. The executor calls
`poller.step_by(len)` before each back-reference compare, forward and
backward, so a long capture counts toward the interrupt poll interval.

js_speed regexp row, instructions:u per call (6 batches less 1), three runs,
mr-moqui fb0e5f78 with the fork patched in:

| build | runs |
|---|---|
| main (c64d537d) | 2,963,270 / 2,974,338 / 2,984,676 |
| F3 | 2,975,657 / 2,975,192 / 2,975,219 |

Flat: the medians differ by about 0.03%.

V8 v7, `bench.py`, repeat 2, abba, cpu 2 (see v8-v7.md): regexp ×1.0057
instructions, richards ×1.0000. Both are within ×1.02.

Test: `a_long_back_reference_is_polled` (regexp executor) fails without the fix.
