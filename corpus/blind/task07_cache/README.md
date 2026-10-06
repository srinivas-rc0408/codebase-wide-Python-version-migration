# task07_cache — blind held-out fixture #2

Built after `src/mra/` was frozen; nothing in the agent was written or tuned
against it. Contract as Tier-A: `datetime.utcnow()` → `datetime.now(timezone.utc)`.

**|A| = 1 call site** (position from a libcst pass over `old/`):

| file | line:col | call | binding |
|---|---|---|---|
| `src/svc/stamp.py` | 7:11 | `datetime.datetime.utcnow()` | `import datetime` |

## What makes it hard

* **The break is in a parser, not at a call site.** `store.save()` writes
  `stamp().isoformat()`. Once the stamp is aware, that string ends in `+00:00`,
  and `store.load()` — `datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")` —
  raises `ValueError: unconverted data remains: +00:00`. The codemod alone leaves
  2/4 tests red, and `store.py` holds no deprecated call.
* **The right fix** is in `store.py`: `datetime.datetime.fromisoformat(s)` (gold),
  or equivalently a `%z` format. No import changes anywhere — the module import
  already reaches `datetime.timezone`.
* **Wrong fixes** stop `load()` raising only by dropping the offset: stripping
  `tzinfo` before `isoformat()`, or slicing/re-formatting the string so `+00:00`
  is discarded. Both leave `session.is_fresh()` subtracting naive from aware
  (visible suite stays red), and gold's hidden `tests/test_semantic.py` fails them.
* **Decoy.** `legacy.py` has `LegacyClock.utcnow()` (called) and the literal text
  `datetime.utcnow()` in its module docstring; the tests pin both.

## Trees (verified in the sandbox before any agent run)

| tree | result |
|---|---|
| `old/` | 4/4 green; no test assumes timezone-awareness |
| `gold/` | 6/6 green (`stamp.py` and `store.py` changed, plus hidden `tests/test_semantic.py`) |
| codemod only + hidden tests | 2/6 — `ValueError: unconverted data remains: +00:00` |
| wrong fix: `strptime(s[:26], …)` + hidden | 2/6 |
| wrong fix: `value.replace(tzinfo=None).isoformat()` + hidden | 2/6 |
| right fix: `%z` format + hidden | 6/6 |

`old/` has a one-in-a-million flake by construction: `isoformat()` omits the
fraction when `microsecond == 0`, and the `%f` format then fails.
