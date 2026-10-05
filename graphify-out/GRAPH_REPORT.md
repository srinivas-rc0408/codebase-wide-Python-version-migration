# Graph Report - File1  (2026-10-05)

## Corpus Check
- 453 files · ~171,161 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3600 nodes · 5304 edges · 247 communities (168 shown, 79 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 275 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `48d9ff10`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SandboxRunner
- analysis/__init__.py
- test_analyzer.py
- Project Synopsis & Charter
- make_timestamp
- make_timestamp
- Migration Agent — Master Resource Pack
- make_timestamp
- make_timestamp
- 2. Low-Level Design (LLD) — the LangGraph state machine
- Data & Evaluation Protocol
- Software Requirements Specification (SRS)
- call_sites.py
- test_p2_end_to_end.py
- Literature Review & State of the Art
- paper.md
- task05_signature_break — Tier-A edit-order fixture
- CLAUDE.md
- Configuration & Secrets
- task01_datetime/gold/src/pkg/__init__.py
- task01_datetime/old/src/pkg/__init__.py
- task02_datetime_aliased/gold/src/pkg/__init__.py
- task02_datetime_aliased/old/src/pkg/__init__.py
- pkg
- pkg
- pkg
- pkg
- mra
- sandbox/runner.py
- graph.py
- cli.py
- run.py
- test_p4_graph.py
- test_recovery.py
- test_benchmark.py
- make_timestamp
- run_one
- make_timestamp
- sandbox/__init__.py
- correct_node.py
- loop.py
- issue
- 1b. Per task, per configuration
- post
- task04_multimodule/gold/src/pkg/audit.py
- task04_multimodule/old/src/pkg/audit.py
- issue
- Product Requirements Document (PRD)
- Codebase-Wide Version Migration & Refactoring Agent (MRA)
- make_timestamp
- old/src/pkg/api.py
- post
- make_timestamp
- skills.py
- ExperienceStore
- handle
- old/src/pkg/ledger.py
- test_providers.py
- gold/src/pkg/api.py
- datetime_utcnow.py
- plan_batches
- Failure analysis
- test_issue_stamps_and_posts
- task03_half_migration/gold/src/pkg/__init__.py
- task03_half_migration/old/src/pkg/__init__.py
- task04_multimodule/gold/src/pkg/__init__.py
- task04_multimodule/old/src/pkg/__init__.py
- pkg
- pkg
- pkg
- pkg
- providers/__init__.py
- model.py
- snapshot
- 1b. Per task, per configuration
- post
- elapsed_since
- post
- elapsed_since
- serve
- uptime_s
- gold/tests/test_timebase.py
- uptime_s
- benchmark/runner.py
- handle
- snapshot
- handle
- old/tests/test_timebase.py
- pdf.py
- verify_paper.py
- README.md
- tests/test_report.py
- task05_signature_break/gold/src/pkg/__init__.py
- task05_signature_break/old/src/pkg/__init__.py
- pkg
- pkg
- evidence.py
- _Skipped
- router.py
- test_experience.py
- render
- baselines.py
- edge.py
- Router
- report/__init__.py
- 1b. Per task, per configuration
- verdict.py
- test_many.py
- _build.py
- stamp
- stamp
- stamp
- stamp
- a.py
- test_all
- other_object_with_utcnow/old/src/pkg/core.py
- shadowed_local_name/old/src/pkg/core.py
- stamp
- llm_server
- test_all
- stamp
- stamp
- stamp
- stamp
- stamp
- stamp
- stamp
- job
- stamp
- stamp
- stamp
- test_both
- Any
- stamp
- stamp
- stamp
- stamp
- stamp
- stamp
- wait_for
- stamp
- label
- stamp
- stamp
- stamp
- test_long
- Clock
- crlf_line_endings/gold/src/pkg/core.py
- zero_tests/old/src/pkg/core.py
- RESULTS.md
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- pkg
- 1b. Per task, per configuration
- Any
- _ImportCollector
- experience.py
- 2. The migration targets — the actual data your agent must handle
- edge_results_live.md
- edge_results_live_memory.md
- ConvertUtcnowCommand

## God Nodes (most connected - your core abstractions)
1. `ExperienceStore` - 62 edges
2. `Router` - 45 edges
3. `SandboxRunner` - 31 edges
4. `run_migration()` - 29 edges
5. `migrate_task()` - 28 edges
6. `run_one()` - 26 edges
7. `is_test_path()` - 21 edges
8. `run_matrix()` - 21 edges
9. `build_model()` - 21 edges
10. `analyze()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `analyses()` --calls--> `analyze()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/analyzer.py
- `test_map_never_puts_a_test_file_on_the_work_list()` --calls--> `analyze()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/analyzer.py
- `test_fr3_property_holds_for_every_task_in_the_corpus()` --calls--> `analyze()`  [INFERRED]
  tests/test_p4_graph.py → src/mra/analysis/analyzer.py
- `test_task04_batches_are_dependency_ordered_and_collapse_the_cycle()` --calls--> `analyze()`  [INFERRED]
  tests/test_p4_graph.py → src/mra/analysis/analyzer.py
- `test_no_benchmark_run_touched_a_test_file()` --calls--> `is_test_path()`  [INFERRED]
  tests/test_benchmark.py → src/mra/analysis/call_sites.py

## Import Cycles
- None detected.

## Communities (247 total, 79 thin omitted)

### Community 0 - "SandboxRunner"
Cohesion: 0.12
Nodes (30): Runs a repo's suite in one throwaway container and returns a test_report. The…, SandboxRunner, _break_copy(), green_report(), fixture, needs_docker, Path, TempPathFactory (+22 more)

### Community 1 - "analysis/__init__.py"
Cohesion: 0.13
Nodes (24): analyze(), Any, Collection, Path, MAP-node analysis: locate the work, map the dependencies. Nothing else.…, Scan ``repo`` for ``target`` and map its imports. Args: repo: repository root…, build(), from_state_adjacency() (+16 more)

### Community 2 - "test_analyzer.py"
Cohesion: 0.14
Nodes (30): flat_sites(), Flatten the per-file map into one list, the form ground truth uses., analyses(), _found(), _ground_truth(), _key(), Any, fixture (+22 more)

### Community 3 - "Project Synopsis & Charter"
Cohesion: 0.17
Nodes (12): 10. Open items for first guide meeting, 1. Problem statement, 2. Proposed solution, 3. Scope and finalized migration targets, 4. Deliverables, 5. Success criteria (metrics), 6. Technology stack (summary), 7. Timeline (indicative, aligned to the build phases) (+4 more)

### Community 4 - "make_timestamp"
Cohesion: 0.12
Nodes (19): make_timestamp(), datetime, Timestamp helpers. Defines the contract that the migration changes., Return the current UTC time as a timezone-aware datetime., build_report(), datetime, Report building. Imports :mod:`pkg.core`, creating the cross-file dependency…, Return how many seconds ago ``generated_at`` was produced. (+11 more)

### Community 5 - "make_timestamp"
Cohesion: 0.12
Nodes (19): make_timestamp(), datetime, Timestamp helpers. Defines the contract that the migration changes., Return the current UTC time as a timezone-aware datetime., build_report(), datetime, Report building. Imports :mod:`pkg.core`, creating the cross-file dependency…, Return how many seconds ago ``generated_at`` was produced. Reads the clock… (+11 more)

### Community 6 - "Migration Agent — Master Resource Pack"
Cohesion: 0.12
Nodes (17): 0. Read this first — the one thing that will sink you, 10. Trap checklist (expanded with the version facts I found), 11. Questions for Dr Nimrita Koul (first meeting) — refined, 12. The paper plan (start the skeleton in week 1, not week 9), 13. Your one-sentence story (memorize it — this is the interview weapon), 1. Verified stack (checked 24 Aug 2026), 3.1 Tier A — controlled repos you author (your gold standard), 3.2 Tier B — real OSS repos (external validity) (+9 more)

### Community 7 - "make_timestamp"
Cohesion: 0.13
Nodes (17): make_timestamp(), datetime, Timestamp helpers. Defines the contract that the migration changes., Return the current UTC time as a naive datetime., build_report(), datetime, Report building. Imports :mod:`pkg.core`, creating the cross-file dependency…, Return how many seconds ago ``generated_at`` was produced. (+9 more)

### Community 8 - "make_timestamp"
Cohesion: 0.13
Nodes (17): make_timestamp(), datetime, Timestamp helpers. Defines the contract that the migration changes., Return the current UTC time as a naive datetime., build_report(), datetime, Report building. Imports :mod:`pkg.core`, creating the cross-file dependency…, Return how many seconds ago ``generated_at`` was produced. Reads the clock… (+9 more)

### Community 9 - "2. Low-Level Design (LLD) — the LangGraph state machine"
Cohesion: 0.10
Nodes (19): 1.1 Component diagram, 1.2 Component responsibilities, 1.3 Data flow (one task, happy path then recovery), 1.4 Key architectural decisions (ADR summary), 1. High-Level Design (HLD), 2.1 State machine diagram, 2.2 Nodes (contracts), 2.3 Conditional routing after TEST (the graded logic) (+11 more)

### Community 10 - "Data & Evaluation Protocol"
Cohesion: 0.11
Nodes (18): 1.1 Tier A — controlled repos you author (gold standard), 1.2 Tier A git-tagging strategy, 1.3 Tier B — real OSS repos (external validity), 1. Corpus specification, 2.1 M1 — Migration Completeness, 2.2 M2 — Post-Migration Test Pass Rate, 2.3 M3 — Token / Step Overhead, 2.4 Reference computation (already stubbed in the resource pack) (+10 more)

### Community 11 - "Software Requirements Specification (SRS)"
Cohesion: 0.11
Nodes (17): 1.1 Purpose, 1.2 Definitions, 1.3 Actors, 1. Introduction, 2. Overall description, 3. Functional requirements, 4.1 `MigrationState` (the agent's working memory), 4.2 `ground_truth.json` (Tier-A scoring key) (+9 more)

### Community 12 - "call_sites.py"
Cohesion: 0.09
Nodes (27): CallSite, _CallSiteVisitor, canonical(), dotted_path(), find_in_repo(), find_in_source(), ImportBindings, _module_name() (+19 more)

### Community 13 - "test_p2_end_to_end.py"
Cohesion: 0.14
Nodes (27): _added_import_lines(), corpus_digests(), Any, fixture, needs_docker, parametrize, Path, TempPathFactory (+19 more)

### Community 14 - "Literature Review & State of the Art"
Cohesion: 0.15
Nodes (12): 1. Problem framing: version migration vs. issue resolution, 2. Deterministic refactoring tools — the baselines, 3.1 SWE-agent — the Agent-Computer Interface (ACI), 3.2 OpenHands (formerly OpenDevin) — CodeAct and the event stream, 3.3 Agentless — the pipeline counter-argument, 3.4 Summary comparison, 3. LLM-based software-engineering systems — the SOTA, 4. Evaluation methodology in the field (+4 more)

### Community 15 - "paper.md"
Cohesion: 0.06
Nodes (34): 10. Conclusion, 1. Introduction, 2. Related Work, 3.1 The state machine, 3.2 Dependency-ordered batching, 3.3 Codemod first, model second, 3.4 The verifier and the sandbox, 3.5 Recovery and the signature-based retry cap (+26 more)

### Community 16 - "task05_signature_break — Tier-A edit-order fixture"
Cohesion: 0.06
Nodes (27): task01_datetime — Tier-A controlled task, Test-oracle rule, The `pkg` name-collision gotcha, The two states live in one commit, Import changes: deliberately empty, Running the two states, task02_datetime_aliased — Tier-A controlled task, The cross-file break (+19 more)

### Community 17 - "CLAUDE.md"
Cohesion: 0.20
Nodes (9): Coding conventions, Commit conventions, Current phase / context, Golden rules (do not violate), How to run and test, Tech stack (fixed — verified Sep 2026), What this project is, When unsure (+1 more)

### Community 18 - "Configuration & Secrets"
Cohesion: 0.22
Nodes (8): 1. First-time setup, 2. Keys, 3. Providers and roles — `mra.toml`, 4. Configuration variables (non-secret), 5. Privacy, 6. Security rules, 7. CI / grading environments, Configuration & Secrets

### Community 28 - "sandbox/runner.py"
Cohesion: 0.11
Nodes (23): Phase, _exc_type_from(), _failure_from_collector(), _failure_from_test(), failure_signature(), _lint_counts(), normalize_message(), Any (+15 more)

### Community 29 - "graph.py"
Cohesion: 0.10
Nodes (33): all_batches_done(), build_graph(), _cap(), changed_files(), finish_node(), is_green(), _key(), outcome_of() (+25 more)

### Community 30 - "cli.py"
Cohesion: 0.11
Nodes (31): main(), memory(), providers_check(), The ``mra`` command. * ``mra run --task-dir DIR`` — migrate, verify, and write…, report(), run(), _show(), skills() (+23 more)

### Community 31 - "run.py"
Cohesion: 0.12
Nodes (21): M1 and M2, following docs/05_DATA_EVALUATION_PROTOCOL.md. M3 (tokens, cost) is…, m1(), M1 — Migration Completeness. Transcribed verbatim from…, m2(), M2 — Post-Migration Test Pass Rate. Transcribed verbatim from…, _key(), main(), migrate_task() (+13 more)

### Community 32 - "test_p4_graph.py"
Cohesion: 0.05
Nodes (69): edit_context(), graph_slice(), offline_summary(), progress_facts(), Any, Rolling memory: what the model is told about everything that is not in front of…, The dependency neighbourhood, truncated to a constant number of names., The complete payload for one corrective-edit call (NFR-12). Everything except… (+61 more)

### Community 33 - "test_recovery.py"
Cohesion: 0.06
Nodes (61): apply_codemod(), Path, Run the codemod over every file in ``call_sites``; return the ones that…, State-machine nodes: plain ``state -> partial update`` functions, wired…, bad_corrector(), corpus_digest(), gave_up(), _nodes() (+53 more)

### Community 34 - "test_benchmark.py"
Cohesion: 0.09
Nodes (33): corpus_digests(), Any, parametrize, P5 acceptance: the ablations, the results artifacts and the baseline tools.…, Ablation A, the project's core claim, on the two cross-file tasks., The control: with no cross-file break there is nothing to recover, so A is flat., FR-3 order is not free to violate: the loop pays for it in CORRECT visits., With nothing to repair the regression, the wrong order leaves less migrated.… (+25 more)

### Community 35 - "make_timestamp"
Cohesion: 0.08
Nodes (28): audit_record(), audit_window(), datetime, Audit trail. Imports the clock contract and also reads the clock directly., Return the ``seconds``-long window ending now. Both ends come from the same…, Stamp an audit record from the shared clock., make_timestamp(), datetime (+20 more)

### Community 36 - "run_one"
Cohesion: 0.09
Nodes (32): P5 benchmarking: run the agent across the corpus under controlled conditions., ``python -m mra.benchmark`` — run the matrix and write the report., codemod_corrector(), Config, _env(), _f1(), main(), make_planner() (+24 more)

### Community 37 - "make_timestamp"
Cohesion: 0.08
Nodes (26): audit_record(), audit_window(), datetime, Audit trail. Imports the clock contract and also reads the clock directly., Return the ``seconds``-long window ending now. Both ends come from the same…, Stamp an audit record from the shared clock., make_timestamp(), datetime (+18 more)

### Community 38 - "sandbox/__init__.py"
Cohesion: 0.13
Nodes (23): make_correct_node(), Bind a corrector and return the node LangGraph calls. One visit repairs one…, make_edit_node(), Any, EDIT node: apply the migration codemod to the files the analyzer flagged. It…, Bind nothing and return the node LangGraph calls. The node edits…, changed_paths(), diff() (+15 more)

### Community 39 - "correct_node.py"
Cohesion: 0.11
Nodes (27): Re-apply a stored diff pattern's ``-``/``+`` line pairs to ``source``. Each…, Ablation E's deterministic corrector: it can only replay what memory recalls.…, replay(), ReplayCorrector, format_hint(), apply_source(), classify(), classify_offline() (+19 more)

### Community 41 - "loop.py"
Cohesion: 0.21
Nodes (14): Self-correction: the loop that turns a failing migration into a passing one., Corrector, is_green(), _next_failure(), Any, Path, Protocol, The recovery loop: EDIT -> TEST -> CORRECT -> TEST -> ... -> green or give up.… (+6 more)

### Community 42 - "issue"
Cohesion: 0.15
Nodes (13): issue(), Invoicing. Stamps with its OWN clock reading, not the shared one. That detail…, Post the amount to the ledger and return the invoice record., invoice_age_seconds(), Reporting. The module the batched migration is designed to leave behind., Issue an invoice and report how old it is., Seconds since the invoice was issued. Reads its *own* clock and subtracts…, summary() (+5 more)

### Community 43 - "1b. Per task, per configuration"
Cohesion: 0.11
Nodes (19): 1. The whole offline matrix, 1b. Per task, per configuration, 2. Ablations, 3. Deterministic baselines — ruff (DTZ) and pyupgrade, 4. Configuration key, A. Recovery loop ON vs OFF — the headline, B. Dependency-ordered batching vs arbitrary order, batch size 1, recovery OFF (+11 more)

### Community 44 - "post"
Cohesion: 0.17
Nodes (13): balance(), post(), datetime, Double-entry ledger. Half of the import cycle with :mod:`pkg.audit`. ``import…, Record an entry, stamped from the shared clock, and note it in the audit trail., Sum of every amount posted to ``account``., The ``seconds``-long window ending now. Both ends come from one reading, so…, snapshot_window() (+5 more)

### Community 45 - "task04_multimodule/gold/src/pkg/audit.py"
Cohesion: 0.20
Nodes (10): note(), Audit trail. The other half of the import cycle with :mod:`pkg.ledger`., Append a message to the trail, stamped from the shared clock., Read the ledger back — the call that closes the cycle. ``checked_at`` is never…, reconcile(), trail(), Audit trail, and the call that closes the import cycle with the ledger., Exercises audit -> ledger, the other direction of the cycle. (+2 more)

### Community 46 - "task04_multimodule/old/src/pkg/audit.py"
Cohesion: 0.20
Nodes (10): note(), Audit trail. The other half of the import cycle with :mod:`pkg.ledger`., Append a message to the trail, stamped from the shared clock., Read the ledger back — the call that closes the cycle. ``checked_at`` is never…, reconcile(), trail(), Audit trail, and the call that closes the import cycle with the ledger., Exercises audit -> ledger, the other direction of the cycle. (+2 more)

### Community 47 - "issue"
Cohesion: 0.23
Nodes (10): issue(), Post the amount to the ledger and return the invoice record., invoice_age_seconds(), Reporting. The module the batched migration is designed to leave behind., Issue an invoice and report how old it is., Seconds since the invoice was issued. Reads its *own* clock and subtracts…, summary(), The tripwire. ``invoice_age_seconds`` is the only place in the package where… (+2 more)

### Community 48 - "Product Requirements Document (PRD)"
Cohesion: 0.17
Nodes (12): 10. Risks, 1. Problem, 2. Goal, 3. Non-goals, 4. Users / personas, 5. User stories, 6. Scope (in / out), 7. Success metrics (+4 more)

### Community 49 - "Codebase-Wide Version Migration & Refactoring Agent (MRA)"
Cohesion: 0.13
Nodes (15): Acknowledgements, Architecture at a glance, Codebase-Wide Version Migration & Refactoring Agent (MRA), Documentation index, Edge-case accuracy suite, Evaluation, License, LLM providers and privacy (+7 more)

### Community 50 - "make_timestamp"
Cohesion: 0.24
Nodes (9): make_timestamp(), datetime, The shared clock. Nothing in the package imports anything to provide it. Most-…, Return the current UTC time as a naive datetime., The shared clock. No assertion here may depend on the migration (NB-10)., The semantic check. Fails against ``old/`` — that is the point., test_make_timestamp_is_non_decreasing(), test_make_timestamp_is_timezone_aware() (+1 more)

### Community 51 - "old/src/pkg/api.py"
Cohesion: 0.18
Nodes (8): handle(), The entry point. Depends on report, audit and config — the graph's deepest…, Serve one request. ``served_at`` is this module's own, self-contained reading., Static settings. No clock, no in-repo imports — the graph's other root., How long a record is kept, in seconds., retention_seconds(), The entry point, exercising the whole import DAG in one call., test_handle_serves_a_complete_response()

### Community 52 - "post"
Cohesion: 0.22
Nodes (8): Invoicing. Stamps with its OWN clock reading, not the shared one. That detail…, balance(), post(), Record an entry, stamped from the shared clock, and note it in the audit trail., Sum of every amount posted to ``account``., Ledger, including its self-contained clock reading., test_balance_sums_only_that_account(), test_post_returns_a_stamped_entry()

### Community 53 - "make_timestamp"
Cohesion: 0.28
Nodes (7): make_timestamp(), datetime, The shared clock. Nothing in the package imports anything to provide it. Most-…, Return the current UTC time as a naive datetime., The shared clock. No assertion here may depend on the migration (NB-10)., test_make_timestamp_is_non_decreasing(), test_make_timestamp_returns_a_datetime()

### Community 54 - "skills.py"
Cohesion: 0.12
Nodes (22): apply_rule(), _code(), derive_rule(), _extend_from_import(), _import_names(), CSTNode, Module, Path (+14 more)

### Community 56 - "ExperienceStore"
Cohesion: 0.15
Nodes (34): ExperienceStore, One SQLite file of past fixes. ``readonly`` serves hints but learns nothing., skill_id(), db(), Any, CaptureFixture, fixture, MonkeyPatch (+26 more)

### Community 57 - "handle"
Cohesion: 0.33
Nodes (6): handle(), Serve one request. ``served_at`` is this module's own, self-contained reading., The entry point, exercising the whole import DAG in one call., Syntactic success is not success: no module may be left on a naive clock., test_every_stamp_in_one_response_is_aware(), test_handle_serves_a_complete_response()

### Community 58 - "old/src/pkg/ledger.py"
Cohesion: 0.33
Nodes (6): datetime, Double-entry ledger. Half of the import cycle with :mod:`pkg.audit`. ``import…, The ``seconds``-long window ending now. Both ends come from one reading, so…, snapshot_window(), Both ends come from one reading — safe whichever side of the migration., test_snapshot_window_is_ordered()

### Community 59 - "test_providers.py"
Cohesion: 0.12
Nodes (26): FakeProvider, Exception, Message, Answers from ``reply(messages, model)`` (default: echo the last message).…, OpenAICompatibleProvider, Any, Provider layer, router fallback, privacy mode, redaction, egress — all offline.…, End to end over real HTTP: request shape out, Completion shape back. (+18 more)

### Community 60 - "gold/src/pkg/api.py"
Cohesion: 0.33
Nodes (4): The entry point. Depends on report, audit and config — the graph's deepest…, Static settings. No clock, no in-repo imports — the graph's other root., How long a record is kept, in seconds., retention_seconds()

### Community 61 - "datetime_utcnow.py"
Cohesion: 0.11
Nodes (17): FlattenSentinel, SimpleStatementLine, family(), _import_key(), _InsertTimezone, _place_timezone_import(), CSTNode, ImportFrom (+9 more)

### Community 62 - "plan_batches"
Cohesion: 0.17
Nodes (18): _chunk(), cycles(), plan_batches(), plan_node(), Any, DiGraph, PLAN node: turn the dependency graph into an ordered list of edit batches…, ``MigrationState`` -> ``edit_batches`` (+ the audit note for this step). (+10 more)

### Community 63 - "Failure analysis"
Cohesion: 0.13
Nodes (15): Failure analysis, `no-recovery` on task02_datetime_aliased, `no-recovery` on task03_half_migration, `no-recovery` on task04_multimodule, `order-alphabetical-b1-norecovery` on task02_datetime_aliased, `order-alphabetical-b1-norecovery` on task03_half_migration, `order-alphabetical-b1-norecovery` on task04_multimodule, `order-alphabetical-b1-norecovery` on task05_signature_break (+7 more)

### Community 73 - "providers/__init__.py"
Cohesion: 0.07
Nodes (27): AnthropicProvider, Message, Anthropic's native Messages API, through the pinned ``anthropic`` SDK. The…, _backoff(), Completion, KeyedProvider, Provider, Any (+19 more)

### Community 74 - "model.py"
Cohesion: 0.18
Nodes (24): build_model(), _changes(), _checks(), _edge_row(), _egress_line(), _files(), _from_state_db(), _graph() (+16 more)

### Community 75 - "snapshot"
Cohesion: 0.16
Nodes (10): The service edge: the deepest module in the import DAG., One request, its ledger entry and a metrics snapshot., serve(), Point-in-time metrics over the ledger., Entry count plus how long this reading took to assemble., snapshot(), The service edge: every module in the DAG on one call path., test_serve_returns_the_whole_response() (+2 more)

### Community 76 - "1b. Per task, per configuration"
Cohesion: 0.10
Nodes (20): 1. The whole offline matrix, 1b. Per task, per configuration, 2. Ablations, 3. Deterministic baselines — ruff (DTZ) and pyupgrade, 4. Configuration key, A. Recovery loop ON vs OFF — the headline, B. Dependency-ordered batching vs arbitrary order, batch size 1, recovery OFF (+12 more)

### Community 77 - "post"
Cohesion: 0.24
Nodes (8): age_of(), post(), Append-only ledger. Stamps entries with its own clock reading., Record one amount against an account and return the entry., Seconds since ``entry`` was posted. Hands this module's own stamp back to the…, The ledger and the call-time half of the break., test_age_of_an_entry_is_non_negative(), test_post_records_the_amount()

### Community 78 - "elapsed_since"
Cohesion: 0.33
Nodes (9): aligned(), elapsed_since(), datetime, The package clock, and the one place its contract is enforced. Every module…, The current UTC time, in whatever shape the package contract is in., Read ``stamp`` in the shape ``reference`` is in. Upgrades only, never…, Seconds between ``stamp`` and now, for a stamp this package produced. The…, utc_now() (+1 more)

### Community 79 - "post"
Cohesion: 0.24
Nodes (8): age_of(), post(), Append-only ledger. Stamps entries with its own clock reading., Record one amount against an account and return the entry., Seconds since ``entry`` was posted. Hands this module's own stamp back to the…, The ledger and the call-time half of the break., test_age_of_an_entry_is_non_negative(), test_post_records_the_amount()

### Community 80 - "elapsed_since"
Cohesion: 0.33
Nodes (9): aligned(), elapsed_since(), datetime, The package clock, and the one place its contract is enforced. Every module…, The current UTC time, in whatever shape the package contract is in., Read ``stamp`` in the shape ``reference`` is in. Upgrades only, never…, Seconds between ``stamp`` and now, for a stamp this package produced. The…, utc_now() (+1 more)

### Community 81 - "serve"
Cohesion: 0.25
Nodes (7): The service edge: the deepest module in the import DAG., One request, its ledger entry and a metrics snapshot., serve(), The service edge: every module in the DAG on one call path., Syntactic success is not success: no module may be left on a naive clock., test_every_stamp_in_one_response_is_aware(), test_serve_returns_the_whole_response()

### Community 82 - "uptime_s"
Cohesion: 0.22
Nodes (5): Start-up bookkeeping. Both of its constants are computed at *import* time. That…, Seconds since :data:`STARTED_AT`., uptime_s(), Start-up constants. Importing this module is itself the assertion., test_uptime_grows_from_the_import_stamp()

### Community 83 - "gold/tests/test_timebase.py"
Cohesion: 0.22
Nodes (8): The clock contract. No assertion here may depend on the migration (NB-10).…, The safe window: a caller that has not moved yet is upgraded for free., The refusal: an aware stamp meeting a naive clock is passed through, not…, The semantic check. Fails against ``old/`` — that is the point., test_aligned_never_strips_a_tzinfo(), test_aligned_reads_a_naive_stamp_as_utc_when_the_clock_is_aware(), test_utc_now_is_timezone_aware(), test_utc_now_returns_a_datetime()

### Community 84 - "uptime_s"
Cohesion: 0.22
Nodes (5): Start-up bookkeeping. Both of its constants are computed at *import* time. That…, Seconds since :data:`STARTED_AT`., uptime_s(), Start-up constants. Importing this module is itself the assertion., test_uptime_grows_from_the_import_stamp()

### Community 85 - "benchmark/runner.py"
Cohesion: 0.15
Nodes (28): _ablation_a(), _ablation_b(), _ablation_c(), _ablation_d(), _ablation_e(), _ablation_f(), _aggregate(), _baseline_section() (+20 more)

### Community 86 - "handle"
Cohesion: 0.33
Nodes (5): handle(), Request handling. Its own stamp never leaves the module, so it is self-…, Post one amount and return the handled record., test_handle_posts_the_entry(), test_handle_reports_uptime()

### Community 87 - "snapshot"
Cohesion: 0.33
Nodes (5): Point-in-time metrics over the ledger., Entry count plus how long this reading took to assemble., snapshot(), test_snapshot_counts_the_entries(), test_snapshot_reports_its_own_lag()

### Community 88 - "handle"
Cohesion: 0.33
Nodes (5): handle(), Request handling. Its own stamp never leaves the module, so it is self-…, Post one amount and return the handled record., test_handle_posts_the_entry(), test_handle_reports_uptime()

### Community 89 - "old/tests/test_timebase.py"
Cohesion: 0.29
Nodes (6): The clock contract. No assertion here may depend on the migration (NB-10).…, The safe window: a caller that has not moved yet is upgraded for free., The refusal: an aware stamp meeting a naive clock is passed through, not…, test_aligned_never_strips_a_tzinfo(), test_aligned_reads_a_naive_stamp_as_utc_when_the_clock_is_aware(), test_utc_now_returns_a_datetime()

### Community 90 - "pdf.py"
Cohesion: 0.14
Nodes (40): Canvas, Paragraph, ParagraphStyle, SimpleDocTemplate, banner(), _build(), _canvas_maker(), _changes() (+32 more)

### Community 91 - "verify_paper.py"
Cohesion: 0.17
Nodes (20): carries_a_figure(), cells(), check(), commit_message(), figures(), main(), pinned_defects(), post_p5_claims() (+12 more)

### Community 92 - "README.md"
Cohesion: 0.17
Nodes (5): (a) The recovery loop is what finishes a cross-file migration, (b) The existing static tools detect the work and do none of it, (c) Dependency-ordered batching: what the data actually supports, Scope and honesty notes, What the Tier-A benchmark shows

### Community 93 - "tests/test_report.py"
Cohesion: 0.13
Nodes (27): ``{status, reasons}`` with RED > YELLOW > GREEN; see the module docstring., verdict(), _codes(), _migrate(), parametrize, Verdict, evidence, the 14-page PDF report, and the codemod's import placement.…, Already migrated: 0/0 is undefined, not over-editing., ruff keeps `as` imports on their own line (I001); appending would break that. (+19 more)

### Community 98 - "evidence.py"
Cohesion: 0.12
Nodes (36): bindings_of(), exports_of(), is_test_path(), parse_repo(), Module, Path, Collect a whole module's import bindings up front., True for anything that is part of the test oracle (NB-4). (+28 more)

### Community 99 - "_Skipped"
Cohesion: 0.16
Nodes (7): Attribute, Call, CSTNode, Exports, ImportFrom, What MAP deliberately does not resolve: star imports and bare references., _Skipped

### Community 100 - "router.py"
Cohesion: 0.11
Nodes (24): Roles, privacy_mode(), cost_usd(), final_answer(), live_model(), live_ready(), load_roles(), Model router: which provider answers which role, and what it cost. Four roles,… (+16 more)

### Community 101 - "test_experience.py"
Cohesion: 0.18
Nodes (21): db(), CaptureFixture, fixture, MonkeyPatch, needs_docker, Path, Feature D: the opt-in experience store. Off by default, never touched by the…, test_env_off_beats_config_on() (+13 more)

### Community 102 - "render"
Cohesion: 0.29
Nodes (8): ``(pdf bytes, pages, truncation applied)`` — the first ladder level that fits., render(), _pages(), MonkeyPatch, _synthetic_run(), test_a_200_file_run_fits_in_14_pages_by_truncating(), test_header_footer_metadata_and_outline(), test_terminal_summary_respects_no_color()

### Community 103 - "baselines.py"
Cohesion: 0.18
Nodes (21): CompletedProcess, baseline_table(), _detect_with_ruff(), Any, Path, pyupgrade_baseline(), The honesty check: what the existing static tools already do (docs/05, §2.2).…, Detect with ruff, then let it fix what it can, and score the result. (+13 more)

### Community 104 - "edge.py"
Cohesion: 0.11
Nodes (32): cases(), held_out(), _json_or(), _judge(), _live_setup(), _llm_setup(), main(), Any (+24 more)

### Community 105 - "Router"
Cohesion: 0.10
Nodes (27): Role, LLM routing, providers, privacy and token accounting. Models come from mra.toml., host_of(), is_local(), PrivacyError, RuntimeError, Where a prompt is allowed to go, and what is scrubbed out of it first. Two…, A call was refused by the privacy policy before any network I/O. (+19 more)

### Community 106 - "report/__init__.py"
Cohesion: 0.18
Nodes (15): Migration & Refactoring Agent., build_report(), Any, datetime, Path, The run report: verdict banner, 14-page PDF, report.json, terminal summary.…, The verdict banner, key metrics, reasons and PDF path, for a terminal., A repo name that is safe in a filename on every OS. (+7 more)

### Community 107 - "1b. Per task, per configuration"
Cohesion: 0.10
Nodes (20): 1. The whole offline matrix, 1b. Per task, per configuration, 2. Ablations, 3. Deterministic baselines — ruff (DTZ) and pyupgrade, 4. Configuration key, A. Recovery loop ON vs OFF — the headline, B. Dependency-ordered batching vs arbitrary order, batch size 1, recovery OFF (+12 more)

### Community 108 - "verdict.py"
Cohesion: 0.22
Nodes (14): needs_network(), Failing tests whose error is the sandbox's missing network, not the code., headline(), _listing(), new_lint(), Any, GREEN / YELLOW / RED: one answer to "can a human merge this patch?".…, The one-line reason under the banner. (+6 more)

### Community 109 - "test_many.py"
Cohesion: 0.21
Nodes (7): t0(), t1(), t2(), t3(), t4(), t5(), test_all()

### Community 110 - "_build.py"
Cohesion: 0.31
Nodes (7): build(), case(), locate(), one(), Generate the edge-case corpus: ``python corpus/edge/_build.py``. Every case is…, ``sites``: (file, call text, occurrence[, symbol]) — the call text's first char…, _text()

### Community 111 - "stamp"
Cohesion: 0.28
Nodes (5): datetime, stamp(), age_seconds(), test_stamp_is_recent(), test_age_is_small()

### Community 112 - "stamp"
Cohesion: 0.28
Nodes (5): datetime, stamp(), age_seconds(), test_stamp_is_recent(), test_age_is_small()

### Community 113 - "stamp"
Cohesion: 0.28
Nodes (5): datetime, stamp(), age_seconds(), test_stamp_is_recent(), test_age_is_small()

### Community 114 - "stamp"
Cohesion: 0.28
Nodes (4): stamp(), age(), test_stamp_is_recent(), test_age()

### Community 115 - "a.py"
Cohesion: 0.43
Nodes (5): a_age(), a_now(), b_age(), b_now(), test_cycle()

### Community 116 - "test_all"
Cohesion: 0.38
Nodes (4): legacy(), stamp(), ok(), test_all()

### Community 117 - "other_object_with_utcnow/old/src/pkg/core.py"
Cohesion: 0.33
Nodes (4): Clock, fake(), stamp(), test_both()

### Community 118 - "shadowed_local_name/old/src/pkg/core.py"
Cohesion: 0.38
Nodes (4): fake(), FakeClock, stamp(), test_both()

### Community 119 - "stamp"
Cohesion: 0.38
Nodes (4): datetime, stamp(), old(), test_both()

### Community 120 - "llm_server"
Cohesion: 0.29
Nodes (7): SimpleNamespace, llm_server(), _no_privacy_env(), fixture, MonkeyPatch, A tiny OpenAI-compatible server on 127.0.0.1. Records every request.…, test_anthropic_provider_lifts_the_system_prompt()

### Community 121 - "test_all"
Cohesion: 0.47
Nodes (4): ages(), stamp(), window(), test_all()

### Community 122 - "stamp"
Cohesion: 0.40
Nodes (3): datetime, stamp(), test_stamp_is_recent()

### Community 123 - "stamp"
Cohesion: 0.40
Nodes (3): datetime, stamp(), test_stamp_is_recent()

### Community 124 - "stamp"
Cohesion: 0.33
Nodes (4): Replaces datetime.utcnow() one day., Like datetime.utcnow(), but tested., stamp(), test_text_untouched()

### Community 125 - "stamp"
Cohesion: 0.50
Nodes (3): datetime, stamp(), test_stamp_is_recent()

### Community 126 - "stamp"
Cohesion: 0.50
Nodes (3): datetime, stamp(), test_close_to_now()

### Community 127 - "stamp"
Cohesion: 0.50
Nodes (3): datetime, stamp(), test_stamp_is_recent()

### Community 128 - "stamp"
Cohesion: 0.50
Nodes (3): datetime, stamp(), test_stamp_is_recent()

### Community 129 - "job"
Cohesion: 0.50
Nodes (3): job(), tagged(), test_job()

### Community 130 - "stamp"
Cohesion: 0.50
Nodes (3): datetime, stamp(), test_stamp_is_recent()

### Community 131 - "stamp"
Cohesion: 0.50
Nodes (3): datetime, stamp(), test_stamp_is_recent()

### Community 132 - "stamp"
Cohesion: 0.50
Nodes (3): datetime, stamp(), test_naive_contract()

### Community 133 - "test_both"
Cohesion: 0.50
Nodes (3): from_epoch(), stamp(), test_both()

### Community 134 - "Any"
Cohesion: 0.17
Nodes (17): _codemod_corrector(), green_run(), Any, fixture, needs_docker, Path, TempPathFactory, An extra module no test imports: migrated, never executed, outside ground truth. (+9 more)

### Community 147 - "test_long"
Cohesion: 0.50
Nodes (3): later(), stamp(), test_long()

### Community 239 - "1b. Per task, per configuration"
Cohesion: 0.10
Nodes (20): 1. The whole offline matrix, 1b. Per task, per configuration, 2. Ablations, 3. Deterministic baselines — ruff (DTZ) and pyupgrade, 4. Configuration key, A. Recovery loop ON vs OFF — the headline, B. Dependency-ordered batching vs arbitrary order, batch size 1, recovery OFF (+12 more)

### Community 240 - "Any"
Cohesion: 0.10
Nodes (14): Connection, clean_message(), Any, Normalised, path-free, secret-free: nothing that identifies a repo or a run., Store one fix (and the run that produced it); False when read-only, empty, or…, Same class and contract, ranked by similarity of the normalised message., The top-k fixes whose :func:`format_hint` text fits :data:`HINT_BUDGET_CHARS`., Record every CORRECT whose very next TEST was green; returns how many were new.… (+6 more)

### Community 241 - "_ImportCollector"
Cohesion: 0.25
Nodes (6): _ImportCollector, _module_name(), BaseExpression, Import, ImportFrom, Collects the dotted module names a file imports, including submodules.

### Community 242 - "experience.py"
Cohesion: 0.13
Nodes (15): configured_ttl(), diff_pattern(), from_config(), fully_green(), Path, Opt-in experience store: past corrective fixes, offered as hints to CORRECT.…, A ``git diff`` -> its changed lines only: no headers, hunks or paths., The configured store, or None — which is the default. (+7 more)

### Community 243 - "2. The migration targets — the actual data your agent must handle"
Cohesion: 0.33
Nodes (6): 2.1 `datetime.utcnow()` → timezone-aware (EASY — build this first), 2.2 Python 3.8 → 3.12 modernization (EASY–MEDIUM, has a baseline), 2.3 `requests` → `httpx` (MEDIUM), 2.4 Pydantic v1 → v2 (HARD, well-documented — strong choice), 2.5 SQLAlchemy 1.4 → 2.0 (HARDEST — the spec's own example), 2. The migration targets — the actual data your agent must handle

### Community 246 - "ConvertUtcnowCommand"
Cohesion: 0.13
Nodes (15): CodemodContext, _fake_reply(), Classify, summarise, or return the codemod's version of the file it was shown., ConvertUtcnowCommand, BaseExpression, Call, Name, VisitorBasedCodemodCommand (+7 more)

## Knowledge Gaps
- **309 isolated node(s):** `pkg`, `pkg`, `pkg`, `pkg`, `pkg` (+304 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **79 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ExperienceStore` connect `ExperienceStore` to `run_one`, `test_experience.py`, `correct_node.py`, `edge.py`, `Any`, `experience.py`, `benchmark/runner.py`, `skills.py`, `cli.py`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Why does `Router` connect `Router` to `test_p4_graph.py`, `test_recovery.py`, `run_one`, `router.py`, `sandbox/__init__.py`, `correct_node.py`, `edge.py`, `benchmark/runner.py`, `ExperienceStore`, `test_providers.py`, `graph.py`, `cli.py`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Why does `SandboxRunner` connect `SandboxRunner` to `test_p4_graph.py`, `evidence.py`, `sandbox/__init__.py`, `baselines.py`, `loop.py`, `test_p2_end_to_end.py`, `sandbox/runner.py`, `graph.py`, `run.py`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `ExperienceStore` (e.g. with `Config` and `ReplayCorrector`) actually correct?**
  _`ExperienceStore` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `Router` (e.g. with `PrivacyError` and `Tokens`) actually correct?**
  _`Router` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SandboxRunner` (e.g. with `test_migrated_tree_satisfies_the_gold_semantic_check()` and `test_trajectory_is_reconstructed_from_the_checkpoint_file_on_disk()`) actually correct?**
  _`SandboxRunner` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `pkg`, `pkg`, `pkg` to the rest of the system?**
  _309 weakly-connected nodes found - possible documentation gaps or missing edges._