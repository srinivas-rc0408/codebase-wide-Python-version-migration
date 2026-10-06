# task07_cache: blind held-out result #2 (2026-10-06)

`src/mra/` frozen (HEAD `06da274`, v0.3.0, untouched). Live model
`nvidia/nemotron-3-super-120b-a12b`, `MRA_EXPERIENCE=off MRA_SKILLS=off`,
`mra run --llm`, 3 repeats. **Result: PASS. 3/3 runs GREEN, 9/9 criteria each, the
same patch byte for byte every time, identical to gold.**

| # | criterion | result | evidence (r1 / r2 / r3) |
|---|---|---|---|
| 1 | verdict GREEN | PASS | GREEN / GREEN / GREEN, no reasons |
| 2 | M1 100/100, decoy untouched | PASS | recall 100, precision 100; `legacy.py` byte-identical to `old/` |
| 3 | M2 100%, 0 regressions, hidden semantic pass | PASS | M2 100%, 0 regressions; hidden suite on the agent's output 6/6 (tzinfo not None, offset preserved) |
| 4 | store.py fixed by the model | PASS | `load()` now `return datetime.datetime.fromisoformat(s)`; `recover` tokens 2200 / 2053 / 2031 |
| 5 | no import changes (stamp.py rides `import datetime`) | PASS | top-level imports of `stamp.py` and `store.py` unchanged |
| 6 | patch touches only stamp.py and store.py | PASS | patch files = {`src/svc/stamp.py`, `src/svc/store.py`}; `session.py`, `legacy.py` not edited |
| 7 | tests untouched | PASS | every `tests/*.py` byte-identical to `old/`, none added |
| 8 | re-run on own output: empty, GREEN, 0 calls | PASS | empty patch, GREEN, 0 model calls (all three) |
| 9 | corrections ≤ 3; tokens, requests | PASS | 1 correction each; tokens 3327 / 3753 / 3206; requests 3 / 3 / 3 (classify + summarize + recover) |

## The model's patch (all three runs, identical; equal to `gold/`)

```diff
--- a/src/svc/stamp.py
+++ b/src/svc/stamp.py
@@ -4,4 +4,4 @@ import datetime
 
 
 def stamp():
-    return datetime.datetime.utcnow()
+    return datetime.datetime.now(datetime.timezone.utc)
--- a/src/svc/store.py
+++ b/src/svc/store.py
@@ -16,4 +16,4 @@ def save(path):
 def load(path):
     with open(path) as handle:
         s = json.load(handle)["stamp"]
-    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")
+    return datetime.datetime.fromisoformat(s)
```

`stamp.py` is the codemod (module form, no import). `store.py` is the model, via
v0.3.0 consequence repair: no residual call site was left, so CORRECT scoped the
patch to the traced files and their migrated neighbours and the model chose
`store.py`.

## Rejected attempts

None. Each run needed one correction (`ValueError: unconverted data remains: +00:00`
on `test_fresh_save_is_fresh`), and the first patch was accepted and turned the suite
green. The anti-reversal guard was therefore never exercised live.

## The guard against this task's wrong fixes (offline probe, frozen code)

Because no wrong fix was proposed live, `reversal()` was called directly on the
post-codemod tree with each candidate `store.py`:

| candidate fix in store.py | guard |
|---|---|
| `value.replace(tzinfo=None).isoformat()` (strip tzinfo) | **rejected**: adds forbidden pattern `tzinfo\s*=\s*None` |
| `strptime(s[:26], …)` (slice the offset off) | **accepted** |
| `strptime(s, "…%S.%f+00:00")` (format swallows the offset) | **accepted** |
| `fromisoformat(s)` (right) | accepted |

So the guard covers only one of the two wrong-fix shapes this task names. The two
it accepts can't reach GREEN here: the visible suite still compares an aware
stamp with a naive one, so `test_fresh_save_is_fresh` raises `TypeError` and
`test_round_trip_is_equal` fails (verified in the sandbox, see `../README.md`).
The visible tests are the backstop, not the guard.

Files: `../results.json` (scored output), `rN-migration.diff`, `rN-trajectory.json`,
`rN-report.pdf` (the agent's own PDF run report).
