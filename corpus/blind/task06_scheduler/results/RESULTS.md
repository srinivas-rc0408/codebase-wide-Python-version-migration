# task06_scheduler: blind held-out result (2026-10-06)

`src/mra/` frozen (HEAD `f97bf67`, untouched). Live model
`nvidia/nemotron-3-super-120b-a12b`, `MRA_EXPERIENCE=off MRA_SKILLS=off`,
`mra run --llm`, 3 repeats. **Result: FAIL. 3/3 runs RED, the same way each time.**

| # | criterion | result | evidence (r1 / r2 / r3) |
|---|---|---|---|
| 1 | verdict GREEN | **FAIL** | RED / RED / RED: `gave_up` after MAX_FIX_ATTEMPTS; final suite 7/8 |
| 2 | M1 100/100, decoys untouched | PASS | recall 100, precision 100; `decoys.py` byte-identical to `old/` |
| 3 | M2 100%, 0 regressions, hidden semantic pass | **FAIL** | M2 87.5%, 1 regression (`test_age_days_is_non_negative_int`, TypeError); hidden: 1 failed (`test_epoch_is_timezone_aware`), 1 passed |
| 4 | EPOCH fixed by the model | **FAIL** | EPOCH unchanged; `recover` tokens 0. The model was never asked for a patch (see below) |
| 5 | clock +timezone, config no import | PASS | `from datetime import timezone` added to clock.py; config.py imports still only `import datetime as dtm` |
| 6 | patch touches only clock.py, config.py | PASS | patch files = {clock.py, config.py}; report.py not edited |
| 7 | tests untouched | PASS | every `tests/*.py` byte-identical to `old/` |
| 8 | re-run on own output: empty, GREEN, 0 calls | **FAIL** | empty patch and 0 model calls, but RED: the input suite is 7/8, so NB-10 refuses to migrate |
| 9 | corrections ≤ 3; tokens, requests | PASS (cap) | 3 corrections each, all no-ops; tokens 2425 / 2282 / 2216; requests 6 / 6 / 6 (3 classify + 3 summarize) |

## Why it fails

The codemod migrates both call sites correctly (the patch is identical in all 3 runs, see
`r1-migration.diff`). The suite then fails in `report.age_days()`: the clock is now
aware, and `config.EPOCH` is still naive.

CORRECT can't fix this. `LLMCorrector.__call__` (`src/mra/nodes/correct_node.py`)
calls `locate()`, which re-runs MAP and returns `None` when no unmigrated call site
remains (lines 141–144). The corrector then returns `[]` with reason "nothing left to
migrate", and that happens **before** the `recover` model call. Each attempt spends one
`classify` and one `summarize` call and changes nothing. After 3 attempts on the same
signature, the loop gives up.

So the gap is structural, not a weakness of the model. Recovery only repairs files that
still contain a deprecated call site, and a naive constant that the migration made
incompatible is out of its reach.

Files: `../results.json` (scored output), `rN-migration.diff`, `rN-trajectory.json`,
`rN-report.pdf` (the agent's own PDF run report).
