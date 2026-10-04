# Benchmark results — Tier A

Generated 2026-10-04T02:58:53.075506+00:00 · 3 repeat(s) per (task, config) · mean ±spread across repeats.

Every row is one agent configuration on one task. `baseline` is the reference (recovery on, dependency-ordered batches of 3, deterministic corrector); every other configuration changes exactly one thing about it (docs/05 §3).

## 1. The whole offline matrix

Every (task, configuration) pair in one table — the paper's reference grid. The per-task breakdowns below are the same rows, split for reading. Live-model rows are absent by design; see §2C.

| task / config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `task01_datetime / rules-off` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.52 ±0.05 |
| `task01_datetime / rules-on` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.49 ±0.11 |
| `task02_datetime_aliased / rules-off` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 3 | 11 | 0 | 0.0000 | 3.68 ±0.22 |
| `task02_datetime_aliased / rules-on` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 3 | 11 | 0 | 0.0000 | 3.75 ±0.24 |
| `task03_half_migration / rules-off` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 3 | 11 | 0 | 0.0000 | 3.64 ±0.38 |
| `task03_half_migration / rules-on` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 3 | 11 | 0 | 0.0000 | 3.81 ±0.17 |
| `task04_multimodule / rules-off` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 9 | 27 | 0 | 0.0000 | 10.14 ±0.59 |
| `task04_multimodule / rules-on` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 9 | 27 | 0 | 0.0000 | 10.23 ±0.17 |
| `task05_signature_break / rules-off` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.01 ±0.10 |
| `task05_signature_break / rules-on` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.06 ±0.19 |

## 1b. Per task, per configuration

### task01_datetime

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rules-off` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.52 ±0.05 |
| `rules-on` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.49 ±0.11 |

### task02_datetime_aliased

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rules-off` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 3 | 11 | 0 | 0.0000 | 3.68 ±0.22 |
| `rules-on` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 3 | 11 | 0 | 0.0000 | 3.75 ±0.24 |

### task03_half_migration

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rules-off` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 3 | 11 | 0 | 0.0000 | 3.64 ±0.38 |
| `rules-on` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 3 | 11 | 0 | 0.0000 | 3.81 ±0.17 |

### task04_multimodule

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rules-off` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 9 | 27 | 0 | 0.0000 | 10.14 ±0.59 |
| `rules-on` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 9 | 27 | 0 | 0.0000 | 10.23 ±0.17 |

### task05_signature_break

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rules-off` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.01 ±0.10 |
| `rules-on` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.06 ±0.19 |

## 2. Ablations

### A. Recovery loop ON vs OFF — the headline

The only variable is whether the CORRECT loop may run. Both arms use the deterministic corrector, so this contrast is reproducible without an API key: the loop's *mechanics* are what is being measured, not the model's.

### B. Dependency-ordered batching vs arbitrary order

`baseline`/`batch-1` use the FR-3 order; the `order-alphabetical` arms ignore the graph; the `order-fr3-violating` arms are `plan_batches` on the *reversed* graph — dependents before their dependencies, the inversion docs/04 §3.4's pseudocode produces if its missing `.reverse()` is taken literally.

Read the three groups separately. At batch 3 a small task is only one or two batches wide, so edit order and batch size are confounded — an order that happens to put a producer and its consumer in the same batch never exposes the intermediate state at all. The `-b1` group edits one file per batch, where sequence is the only variable left. The `-norecovery` group then removes the loop, which is the only way to see what an order costs when nothing is there to repair it.

#### batch size 3, recovery on

#### batch size 1, recovery on

#### batch size 1, recovery OFF

#### What the data says

Corrective edits per task, one file per batch, recovery on (lower is better):


Outcome with the loop off, one file per batch — the same three orders with nothing to repair them:


Three findings.

1. **No task separates the orders with the loop off.** Every arm that breaks, breaks in both directions.

2. **The dependents-first order is never cheaper and is sometimes the most expensive arm run** — on `task04_multimodule` it spends the full NFR-1 retry ceiling of 3 attempts where the dependency order spends 2, i.e. it finishes one attempt away from failing the task. That is what violating FR-3 costs when a loop is there to absorb it: not a wrong answer, a thinner margin.

3. **With the loop on, order is a cost and not a verdict.** Every order completes every Tier-A task, `task05_signature_break` included. Dependency order is never the most expensive arm and the dependents-first order is never the cheapest, but the ranking is not uniform: file-name order is the cheapest arm on `task04` (1 corrective edit against the dependency order's 2), which is luck about which files that particular alphabet happens to group, and the same order costs 2 where the dependency order costs 0 on `task05`. The ordering claim this corpus supports is therefore conditional: *dependency order removes the corrective edits on the task built to expose ordering, and without a recovery loop it is the difference between a green migration and a failed one.*

One honest caveat on `task01`–`task04`: file-name order is not a worse order there. Those tasks are one or two batches wide at batch 3, so alphabetical order degenerates into a near big-bang migration that never exposes an intermediate state. That is a property of a small corpus, not evidence that the graph is unnecessary — `task05` exists precisely because the four earlier tasks could not separate the orders.

### D. Batch size 1 vs 3 vs 5

Batch size caps how many files one EDIT touches before the suite runs again (NFR-5): smaller batches localize a failure more precisely and cost more TEST steps.

### C. Edit model — V4-Pro vs V4-Flash

**Requires a key — not run.** `rules-off-llm`, `rules-on-llm` needs `DEEPSEEK_API_KEY`; the offline matrix above is complete without it.

Caveat for when it does run: `Router.TIER` bills a *recover* call to the pro tier whatever model serves it, so the cost column for the V4-Flash arm is an upper bound, not a quote.

### F. Promoted rules OFF vs ON (held-out Tier-A tasks)

Rules: the skill candidates of a store warmed on 27 training-split task(s) — a fix seen in fully GREEN runs on at least 3 distinct tasks, reduced to a LibCST rule — 0 candidate(s). No Tier-A task is in the training split.

The deterministic pair's corrector repairs nothing, so every repair in `rules-on` is a rule's. Accuracy is M1 recall; attempts are CORRECT visits.

| task | config | outcome | M1 recall | corrections | rules fired | tokens |
|---|---|---|---|---|---|---|
| task01_datetime | `rules-off` | 3× success | 100.0 | 0.0 | 0.0 | 0 |
| task01_datetime | `rules-on` | 3× success | 100.0 | 0.0 | 0.0 | 0 |
| task02_datetime_aliased | `rules-off` | 3× gave_up | 50.0 | 3.0 | 0.0 | 0 |
| task02_datetime_aliased | `rules-on` | 3× gave_up | 50.0 | 3.0 | 0.0 | 0 |
| task03_half_migration | `rules-off` | 3× gave_up | 33.3 | 3.0 | 0.0 | 0 |
| task03_half_migration | `rules-on` | 3× gave_up | 33.3 | 3.0 | 0.0 | 0 |
| task04_multimodule | `rules-off` | 3× gave_up | 66.7 | 9.0 | 0.0 | 0 |
| task04_multimodule | `rules-on` | 3× gave_up | 66.7 | 9.0 | 0.0 | 0 |
| task05_signature_break | `rules-off` | 3× success | 100.0 | 0.0 | 0.0 | 0 |
| task05_signature_break | `rules-on` | 3× success | 100.0 | 0.0 | 0.0 | 0 |

**Live pair requires a key — not run.**

## 3. Deterministic baselines — ruff (DTZ) and pyupgrade

The honesty check (docs/05, RESOURCE_PACK §2.2): what do the existing static tools already do on these tasks?

| task | tool | detected | \|A\| | detect recall | fixed | M1 recall after fix | suite after fix |
|---|---|---|---|---|---|---|---|
| task01_datetime | `ruff (DTZ)` | 1 | 1 | 100% | 0 | 0% | 5/5 passed |
| task01_datetime | `pyupgrade` | 0 | 1 | 0% | 0 | 0% | 5/5 passed |
| task02_datetime_aliased | `ruff (DTZ)` | 2 | 2 | 100% | 0 | 0% | 5/5 passed |
| task02_datetime_aliased | `pyupgrade` | 0 | 2 | 0% | 0 | 0% | 5/5 passed |
| task03_half_migration | `ruff (DTZ)` | 3 | 3 | 100% | 0 | 0% | 7/7 passed |
| task03_half_migration | `pyupgrade` | 0 | 3 | 0% | 0 | 0% | 7/7 passed |
| task04_multimodule | `ruff (DTZ)` | 6 | 6 | 100% | 0 | 0% | 11/11 passed |
| task04_multimodule | `pyupgrade` | 0 | 6 | 0% | 0 | 0% | 11/11 passed |
| task05_signature_break | `ruff (DTZ)` | 7 | 6 | 100% | 0 | 0% | 14/14 passed |
| task05_signature_break | `pyupgrade` | 0 | 6 | 0% | 0 | 0% | 14/14 passed |

`detected` counts sites the tool reported; `fixed` counts files it rewrote. A tool that reports a site but cannot rewrite it scores 0 on M1 however good its detection is — and none of them can repair the cross-file break that task03/task04 are built around, because they never edit anything.

## 4. Configuration key

| config | what it changes |
|---|---|
| `rules-off` | no-op corrector, no promoted rules (control) |
| `rules-on` | no-op corrector, rules from the training split's candidates |
| `rules-off-llm` | live corrective edits, no promoted rules |
| `rules-on-llm` | live corrective edits, rules tried first |

*Generated by `python -m mra.benchmark`.*
