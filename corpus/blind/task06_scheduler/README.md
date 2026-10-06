# task06_scheduler — blind held-out fixture

Built after `src/mra/` was frozen; nothing in the agent was written or tuned
against it. Contract as Tier-A: `datetime.utcnow()` → `datetime.now(timezone.utc)`
and `utcfromtimestamp(t)` → `fromtimestamp(t, timezone.utc)`.

**|A| = 2 call sites** (positions from a libcst pass over `old/`):

| file | line:col | call | binding |
|---|---|---|---|
| `src/app/clock.py` | 7:11 | `DT.utcnow()` | `from datetime import datetime as DT` |
| `src/app/config.py` | 9:11 | `dtm.datetime.utcfromtimestamp(0)` | `import datetime as dtm` |

## What makes it hard

* **A naive constant that is not a call site.** `config.EPOCH =
  dtm.datetime(2020, 1, 1)` is naive. Once the clock is aware,
  `report.age_days()` (`clock.now() - config.EPOCH`) raises `TypeError`, so
  the deterministic codemod alone leaves the suite red and recovery must act.
  The right fix is in `config.py` (`tzinfo=dtm.timezone.utc`, no new import —
  the module alias already reaches it). Editing `report.py` (e.g. stripping
  `tzinfo`) also turns the visible suite green but is the wrong fix: gold's
  hidden `tests/test_semantic.py` catches it.
* **Two import spellings.** The aliased class import needs a new
  `from datetime import timezone`; the module alias needs none.
* **A real import cycle.** `jobs.py` ↔ `scheduler.py`, both at module level.
* **Decoys.** `decoys.py` has `FakeClock.utcnow()` (called) and the literal
  text `datetime.utcnow()` in its docstring and a log message. The tests pin
  both strings byte-for-byte.

## Trees

* `old/` — 8 tests, green; none assumes timezone-awareness.
* `gold/` — `clock.py` and `config.py` changed, everything else identical,
  plus the hidden `tests/test_semantic.py` (`clock.now().tzinfo` and
  `config.EPOCH.tzinfo` are not `None`). 10 tests, green.
