# Graph Report - File1  (2026-10-02)

## Corpus Check
- 443 files · ~134,644 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3407 nodes · 4878 edges · 251 communities (174 shown, 77 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 249 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d080cff1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_sandbox.py
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
- test_p4_graph.py
- graph.py
- cli.py
- metrics/__init__.py
- summarize
- test_recovery.py
- test_benchmark.py
- make_timestamp
- run_one
- make_timestamp
- sandbox/__init__.py
- correct_node.py
- loop.py
- issue
- 2. Ablations
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
- SandboxRunner
- sandbox/runner.py
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
- Provider
- model.py
- snapshot
- ImportBindings
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
- What the Tier-A benchmark shows
- verdict
- task05_signature_break/gold/src/pkg/__init__.py
- task05_signature_break/old/src/pkg/__init__.py
- pkg
- pkg
- evidence.py
- _aware
- run.py
- ExperienceStore
- apply_codemod
- 2. The migration targets — the actual data your agent must handle
- edge.py
- Router
- report/__init__.py
- Any
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
- tests/test_report.py
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
- PreconditionError
- _ImportCollector
- redact_secrets
- Benchmark results — Tier A
- task04_multimodule — Tier-A batching and scale fixture
- 1b. Per task, per configuration
- task02_datetime_aliased — Tier-A controlled task
- task03_half_migration — Tier-A recovery test bed
- task01_datetime — Tier-A controlled task
- replay

## God Nodes (most connected - your core abstractions)
1. `Router` - 40 edges
2. `ExperienceStore` - 32 edges
3. `run_migration()` - 31 edges
4. `SandboxRunner` - 31 edges
5. `migrate_task()` - 28 edges
6. `run_one()` - 23 edges
7. `build_model()` - 21 edges
8. `analyze()` - 20 edges
9. `is_test_path()` - 19 edges
10. `collect()` - 19 edges

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

## Communities (251 total, 77 thin omitted)

### Community 0 - "test_sandbox.py"
Cohesion: 0.11
Nodes (30): _break_copy(), green_report(), fixture, needs_docker, Path, TempPathFactory, P0 acceptance: the sandbox verifies a real corpus task and reports it as data.…, The source tree is mounted :ro and copied inside; a run must not touch it. The… (+22 more)

### Community 1 - "analysis/__init__.py"
Cohesion: 0.13
Nodes (24): analyze(), Any, Collection, Path, MAP-node analysis: locate the work, map the dependencies. Nothing else.…, Scan ``repo`` for ``target`` and map its imports. Args: repo: repository root…, build(), from_state_adjacency() (+16 more)

### Community 2 - "test_analyzer.py"
Cohesion: 0.14
Nodes (31): flat_sites(), Flatten the per-file map into one list, the form ground truth uses., m1(), analyses(), _found(), _ground_truth(), _key(), Any (+23 more)

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
Cohesion: 0.12
Nodes (17): 1.1 Purpose, 1.2 Definitions, 1.3 Actors, 1. Introduction, 2. Overall description, 3. Functional requirements, 4.1 `MigrationState` (the agent's working memory), 4.2 `ground_truth.json` (Tier-A scoring key) (+9 more)

### Community 12 - "call_sites.py"
Cohesion: 0.11
Nodes (26): bindings_of(), CallSite, _CallSiteVisitor, canonical(), dotted_path(), exports_of(), find_in_repo(), find_in_source() (+18 more)

### Community 13 - "test_p2_end_to_end.py"
Cohesion: 0.14
Nodes (27): _added_import_lines(), corpus_digests(), Any, fixture, needs_docker, parametrize, Path, TempPathFactory (+19 more)

### Community 14 - "Literature Review & State of the Art"
Cohesion: 0.15
Nodes (12): 1. Problem framing: version migration vs. issue resolution, 2. Deterministic refactoring tools — the baselines, 3.1 SWE-agent — the Agent-Computer Interface (ACI), 3.2 OpenHands (formerly OpenDevin) — CodeAct and the event stream, 3.3 Agentless — the pipeline counter-argument, 3.4 Summary comparison, 3. LLM-based software-engineering systems — the SOTA, 4. Evaluation methodology in the field (+4 more)

### Community 15 - "paper.md"
Cohesion: 0.07
Nodes (29): 10. Conclusion, 1. Introduction, 2. Related Work, 3.1 The state machine, 3.2 Dependency-ordered batching, 3.3 Codemod first, model second, 3.4 The verifier and the sandbox, 3.5 Recovery and the signature-based retry cap (+21 more)

### Community 16 - "task05_signature_break — Tier-A edit-order fixture"
Cohesion: 0.18
Nodes (7): Running the two states, task05_signature_break — Tier-A edit-order fixture, The import DAG, The three orders, What each module contributes, What makes the break asymmetric, Why it is a hard break, not a test failure

### Community 17 - "CLAUDE.md"
Cohesion: 0.20
Nodes (9): Coding conventions, Commit conventions, Current phase / context, Golden rules (do not violate), How to run and test, Tech stack (fixed — verified Sep 2026), What this project is, When unsure (+1 more)

### Community 18 - "Configuration & Secrets"
Cohesion: 0.22
Nodes (8): 1. First-time setup, 2. Keys, 3. Providers and roles — `mra.toml`, 4. Configuration variables (non-secret), 5. Privacy, 6. Security rules, 7. CI / grading environments, Configuration & Secrets

### Community 28 - "test_p4_graph.py"
Cohesion: 0.07
Nodes (49): bad_corrector(), capped03(), corpus_digests(), graph03(), graph04(), _nodes(), Any, fixture (+41 more)

### Community 29 - "graph.py"
Cohesion: 0.12
Nodes (30): all_batches_done(), build_graph(), _cap(), changed_files(), finish_node(), is_green(), _key(), outcome_of() (+22 more)

### Community 30 - "cli.py"
Cohesion: 0.13
Nodes (27): Roles, main(), memory(), providers_check(), The ``mra`` command. * ``mra run --task-dir DIR`` — migrate, verify, and write…, report(), run(), configured_path() (+19 more)

### Community 31 - "metrics/__init__.py"
Cohesion: 0.33
Nodes (4): M1 and M2, following docs/05_DATA_EVALUATION_PROTOCOL.md. M3 (tokens, cost) is…, M1 — Migration Completeness. Transcribed verbatim from…, m2(), M2 — Post-Migration Test Pass Rate. Transcribed verbatim from…

### Community 32 - "summarize"
Cohesion: 0.14
Nodes (18): graph_slice(), offline_summary(), progress_facts(), Any, Rolling memory: what the model is told about everything that is not in front of…, The dependency neighbourhood, truncated to a constant number of names., Everything worth remembering about a run, in constant size. Deliberately counts…, The deterministic digest, used when no model is available. Also the input the… (+10 more)

### Community 33 - "test_recovery.py"
Cohesion: 0.06
Nodes (55): bad_corrector(), corpus_digest(), gave_up(), _nodes(), oracle_tampering_corrector(), Any, fixture, needs_docker (+47 more)

### Community 34 - "test_benchmark.py"
Cohesion: 0.05
Nodes (67): CompletedProcess, baseline_table(), _detect_with_ruff(), Any, Path, pyupgrade_baseline(), The honesty check: what the existing static tools already do (docs/05, §2.2).…, Run pyupgrade over the task and score it the same way. (+59 more)

### Community 35 - "make_timestamp"
Cohesion: 0.08
Nodes (28): audit_record(), audit_window(), datetime, Audit trail. Imports the clock contract and also reads the clock directly., Return the ``seconds``-long window ending now. Both ends come from the same…, Stamp an audit record from the shared clock., make_timestamp(), datetime (+20 more)

### Community 36 - "run_one"
Cohesion: 0.12
Nodes (20): P5 benchmarking: run the agent across the corpus under controlled conditions., ``python -m mra.benchmark`` — run the matrix and write the report., codemod_corrector(), Config, _env(), _f1(), main(), Path (+12 more)

### Community 37 - "make_timestamp"
Cohesion: 0.08
Nodes (26): audit_record(), audit_window(), datetime, Audit trail. Imports the clock contract and also reads the clock directly., Return the ``seconds``-long window ending now. Both ends come from the same…, Stamp an audit record from the shared clock., make_timestamp(), datetime (+18 more)

### Community 38 - "sandbox/__init__.py"
Cohesion: 0.22
Nodes (15): make_correct_node(), Bind a corrector and return the node LangGraph calls. One visit repairs one…, changed_paths(), diff(), Path, Git snapshot / rollback / diff, exposed as agent tools. These operate on the…, Open ``path`` as a git repo, initializing it if it is not one yet., Commit the whole working tree and return the new commit SHA. Allows an empty… (+7 more)

### Community 39 - "correct_node.py"
Cohesion: 0.13
Nodes (23): edit_context(), The complete payload for one corrective-edit call (NFR-12). Everything except…, apply_source(), classify(), classify_offline(), corrective_patch(), extract_source(), _hinted_files() (+15 more)

### Community 41 - "loop.py"
Cohesion: 0.21
Nodes (14): Self-correction: the loop that turns a failing migration into a passing one., Corrector, is_green(), _next_failure(), Any, Path, Protocol, The recovery loop: EDIT -> TEST -> CORRECT -> TEST -> ... -> green or give up.… (+6 more)

### Community 42 - "issue"
Cohesion: 0.15
Nodes (13): issue(), Invoicing. Stamps with its OWN clock reading, not the shared one. That detail…, Post the amount to the ledger and return the invoice record., invoice_age_seconds(), Reporting. The module the batched migration is designed to leave behind., Issue an invoice and report how old it is., Seconds since the invoice was issued. Reads its *own* clock and subtracts…, summary() (+5 more)

### Community 43 - "2. Ablations"
Cohesion: 0.22
Nodes (9): 2. Ablations, A. Recovery loop ON vs OFF — the headline, B. Dependency-ordered batching vs arbitrary order, batch size 1, recovery OFF, batch size 1, recovery on, batch size 3, recovery on, C. Edit model — V4-Pro vs V4-Flash, D. Batch size 1 vs 3 vs 5 (+1 more)

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

### Community 54 - "SandboxRunner"
Cohesion: 0.24
Nodes (6): make_test_node(), TEST node: verify the tree in the sandbox and write the report into state…, Bind the sandbox and return the node LangGraph calls., Runs a repo's suite in one throwaway container and returns a test_report. The…, Shell run inside the container. `timeout` here is what enforces NFR-4., SandboxRunner

### Community 56 - "sandbox/runner.py"
Cohesion: 0.13
Nodes (22): Phase, _exc_type_from(), _failure_from_collector(), _failure_from_test(), failure_signature(), _lint_counts(), normalize_message(), Any (+14 more)

### Community 57 - "handle"
Cohesion: 0.33
Nodes (6): handle(), Serve one request. ``served_at`` is this module's own, self-contained reading., The entry point, exercising the whole import DAG in one call., Syntactic success is not success: no module may be left on a naive clock., test_every_stamp_in_one_response_is_aware(), test_handle_serves_a_complete_response()

### Community 58 - "old/src/pkg/ledger.py"
Cohesion: 0.33
Nodes (6): datetime, Double-entry ledger. Half of the import cycle with :mod:`pkg.audit`. ``import…, The ``seconds``-long window ending now. Both ends come from one reading, so…, snapshot_window(), Both ends come from one reading — safe whichever side of the migration., test_snapshot_window_is_ordered()

### Community 59 - "test_providers.py"
Cohesion: 0.07
Nodes (40): Exception, AnthropicProvider, Message, Anthropic's native Messages API, through the pinned ``anthropic`` SDK. The…, Completion, KeyedProvider, TypedDict, The provider contract and the key lookup every networked provider shares. (+32 more)

### Community 60 - "gold/src/pkg/api.py"
Cohesion: 0.33
Nodes (4): The entry point. Depends on report, audit and config — the graph's deepest…, Static settings. No clock, no in-repo imports — the graph's other root., How long a record is kept, in seconds., retention_seconds()

### Community 61 - "datetime_utcnow.py"
Cohesion: 0.12
Nodes (17): FlattenSentinel, SimpleStatementLine, family(), _import_key(), _InsertTimezone, _place_timezone_import(), CSTNode, ImportFrom (+9 more)

### Community 62 - "plan_batches"
Cohesion: 0.16
Nodes (20): make_planner(), Return the PLAN node for an ordering arm. * ``dependency`` — the agent's own…, _chunk(), cycles(), plan_batches(), plan_node(), Any, DiGraph (+12 more)

### Community 63 - "Failure analysis"
Cohesion: 0.13
Nodes (15): Failure analysis, `no-recovery` on task02_datetime_aliased, `no-recovery` on task03_half_migration, `no-recovery` on task04_multimodule, `order-alphabetical-b1-norecovery` on task02_datetime_aliased, `order-alphabetical-b1-norecovery` on task03_half_migration, `order-alphabetical-b1-norecovery` on task04_multimodule, `order-alphabetical-b1-norecovery` on task05_signature_break (+7 more)

### Community 73 - "Provider"
Cohesion: 0.25
Nodes (6): Provider, Message, Protocol, make_provider(), Any, Build the provider for one ``[providers.<name>]`` table of ``mra.toml``.

### Community 74 - "model.py"
Cohesion: 0.18
Nodes (24): build_model(), _changes(), _checks(), _edge_row(), _egress_line(), _files(), _from_state_db(), _graph() (+16 more)

### Community 75 - "snapshot"
Cohesion: 0.16
Nodes (10): The service edge: the deepest module in the import DAG., One request, its ledger entry and a metrics snapshot., serve(), Point-in-time metrics over the ledger., Entry count plus how long this reading took to assemble., snapshot(), The service edge: every module in the DAG on one call path., test_serve_returns_the_whole_response() (+2 more)

### Community 76 - "ImportBindings"
Cohesion: 0.22
Nodes (7): ImportBindings, _module_name(), BaseExpression, Import, ImportFrom, Dotted text of an import's module expression (``a.b.c``)., Maps each locally bound name to the fully-qualified thing it refers to. One…

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
Cohesion: 0.18
Nodes (24): _ablation_a(), _ablation_b(), _ablation_c(), _ablation_d(), _ablation_e(), _aggregate(), _baseline_section(), _cell() (+16 more)

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
Cohesion: 0.13
Nodes (42): Canvas, Paragraph, ParagraphStyle, SimpleDocTemplate, banner(), _build(), _canvas_maker(), _changes() (+34 more)

### Community 91 - "verify_paper.py"
Cohesion: 0.29
Nodes (11): carries_a_figure(), cells(), check(), figures(), main(), Check paper.md against the artefacts it cites. Run after any benchmark rerun.…, True if the line states a number, ignoring identifiers that contain digits., Every table under `header`, in document order, header and rule dropped. (+3 more)

### Community 92 - "What the Tier-A benchmark shows"
Cohesion: 0.40
Nodes (5): (a) The recovery loop is what finishes a cross-file migration, (b) The existing static tools detect the work and do none of it, (c) Dependency-ordered batching: what the data actually supports, Scope and honesty notes, What the Tier-A benchmark shows

### Community 93 - "verdict"
Cohesion: 0.19
Nodes (16): ``{status, reasons}`` with RED > YELLOW > GREEN; see the module docstring., verdict(), _codes(), parametrize, Already migrated: 0/0 is undefined, not over-editing., test_green_when_nothing_is_wrong(), test_lint_is_a_multiset_and_contract_exemptions_are_honoured(), test_new_timezone_import_lands_where_isort_puts_it() (+8 more)

### Community 98 - "evidence.py"
Cohesion: 0.15
Nodes (27): is_test_path(), parse_repo(), True for anything that is part of the test oracle (NB-4)., Every parseable file -> (module, package), plus the repo-relative files that do…, apply_check(), base_commit(), collect(), _coverage() (+19 more)

### Community 99 - "_aware"
Cohesion: 0.15
Nodes (10): Attribute, _aware(), _Calls, Call, CSTNode, Exports, ImportFrom, (naive now()/fromtimestamp() calls, tz arguments that do not resolve) in one… (+2 more)

### Community 100 - "run.py"
Cohesion: 0.10
Nodes (28): LLM routing, providers, privacy and token accounting. Models come from mra.toml., cost_usd(), Model router: which provider answers which role, and what it cost. Four roles,…, M3 cost from the token counters, per docs/05 §2.4., Every token in and out, across both tiers — the M3 headline number., total_tokens(), _key(), main() (+20 more)

### Community 101 - "ExperienceStore"
Cohesion: 0.10
Nodes (33): CaptureFixture, Connection, clean_message(), ExperienceStore, format_hint(), Any, Store one fix; returns False when read-only, empty, or already known., Same class and contract, ranked by similarity of the normalised message. (+25 more)

### Community 102 - "apply_codemod"
Cohesion: 0.33
Nodes (5): apply_codemod(), Path, EDIT node: apply the migration codemod to the files the analyzer flagged. It…, Run the codemod over every file in ``call_sites``; return the ones that…, State-machine nodes: plain ``state -> partial update`` functions, wired…

### Community 103 - "2. The migration targets — the actual data your agent must handle"
Cohesion: 0.33
Nodes (6): 2.1 `datetime.utcnow()` → timezone-aware (EASY — build this first), 2.2 Python 3.8 → 3.12 modernization (EASY–MEDIUM, has a baseline), 2.3 `requests` → `httpx` (MEDIUM), 2.4 Pydantic v1 → v2 (HARD, well-documented — strong choice), 2.5 SQLAlchemy 1.4 → 2.0 (HARDEST — the spec's own example), 2. The migration targets — the actual data your agent must handle

### Community 104 - "edge.py"
Cohesion: 0.07
Nodes (35): cases(), _fake_reply(), _judge(), _llm_setup(), main(), Any, Path, Edge-case accuracy suite: ``python -m mra.benchmark.edge``. Runs every case… (+27 more)

### Community 105 - "Router"
Cohesion: 0.11
Nodes (21): Role, host_of(), is_local(), privacy_mode(), PrivacyError, RuntimeError, Where a prompt is allowed to go, and what is scrubbed out of it first. Two…, A call was refused by the privacy policy before any network I/O. (+13 more)

### Community 106 - "report/__init__.py"
Cohesion: 0.24
Nodes (12): build_report(), Any, datetime, Path, The run report: verdict banner, 14-page PDF, report.json, terminal summary.…, A repo name that is safe in a filename on every OS., Render the PDF and report.json from the run directory. Returns (pdf path,…, Run the migration, then always gather evidence and write the report.… (+4 more)

### Community 107 - "Any"
Cohesion: 0.17
Nodes (17): _codemod_corrector(), green_run(), Any, fixture, needs_docker, Path, TempPathFactory, An extra module no test imports: migrated, never executed, outside ground truth. (+9 more)

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
Cohesion: 0.33
Nodes (6): SimpleNamespace, llm_server(), _no_privacy_env(), fixture, MonkeyPatch, A tiny OpenAI-compatible server on 127.0.0.1. Records every request.

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

### Community 134 - "tests/test_report.py"
Cohesion: 0.15
Nodes (18): _migrate(), _pages(), MonkeyPatch, Verdict, evidence, the 14-page PDF report, and the codemod's import placement.…, ruff keeps `as` imports on their own line (I001); appending would break that., task02's point: `import datetime as dt` already reaches dt.timezone., _synthetic_run(), test_a_200_file_run_fits_in_14_pages_by_truncating() (+10 more)

### Community 147 - "test_long"
Cohesion: 0.50
Nodes (3): later(), stamp(), test_long()

### Community 239 - "1b. Per task, per configuration"
Cohesion: 0.10
Nodes (20): 1. The whole offline matrix, 1b. Per task, per configuration, 2. Ablations, 3. Deterministic baselines — ruff (DTZ) and pyupgrade, 4. Configuration key, A. Recovery loop ON vs OFF — the headline, B. Dependency-ordered batching vs arbitrary order, batch size 1, recovery OFF (+12 more)

### Community 240 - "PreconditionError"
Cohesion: 0.33
Nodes (5): Ablation E's deterministic corrector: it can only replay what memory recalls.…, ReplayCorrector, PreconditionError, RuntimeError, NB-10: the pre-migration suite is not green (or collects nothing); refuse to…

### Community 241 - "_ImportCollector"
Cohesion: 0.25
Nodes (6): _ImportCollector, _module_name(), BaseExpression, Import, ImportFrom, Collects the dotted module names a file imports, including submodules.

### Community 242 - "redact_secrets"
Cohesion: 0.40
Nodes (5): diff_pattern(), A ``git diff`` -> its changed lines only: no headers, hunks or paths., Return ``text`` with secret-shaped strings replaced, and how many were., redact_secrets(), test_redact_secrets_counts_each_secret_once()

### Community 243 - "Benchmark results — Tier A"
Cohesion: 0.29
Nodes (4): 1. The whole offline matrix, 3. Deterministic baselines — ruff (DTZ) and pyupgrade, 4. Configuration key, Benchmark results — Tier A

### Community 245 - "task04_multimodule — Tier-A batching and scale fixture"
Cohesion: 0.33
Nodes (6): Running the two states, task04_multimodule — Tier-A batching and scale fixture, The cross-batch break, The expected batch plan, The import DAG, What each module contributes

### Community 247 - "1b. Per task, per configuration"
Cohesion: 0.33
Nodes (6): 1b. Per task, per configuration, task01_datetime, task02_datetime_aliased, task03_half_migration, task04_multimodule, task05_signature_break

### Community 249 - "task02_datetime_aliased — Tier-A controlled task"
Cohesion: 0.40
Nodes (5): Import changes: deliberately empty, Running the two states, task02_datetime_aliased — Tier-A controlled task, The cross-file break, The one factor that varies: import style

### Community 250 - "task03_half_migration — Tier-A recovery test bed"
Cohesion: 0.40
Nodes (5): Running the two states, task03_half_migration — Tier-A recovery test bed, The half-migration, The three modules, What `old/` and `gold/` are

### Community 251 - "task01_datetime — Tier-A controlled task"
Cohesion: 0.50
Nodes (4): task01_datetime — Tier-A controlled task, Test-oracle rule, The `pkg` name-collision gotcha, The two states live in one commit

### Community 252 - "replay"
Cohesion: 0.67
Nodes (3): Re-apply a stored diff pattern's ``-``/``+`` line pairs to ``source``. Each…, replay(), test_replay_applies_a_learnt_pattern()

## Knowledge Gaps
- **271 isolated node(s):** `pkg`, `pkg`, `pkg`, `pkg`, `pkg` (+266 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **77 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Router` connect `Router` to `summarize`, `test_recovery.py`, `run_one`, `run.py`, `sandbox/__init__.py`, `correct_node.py`, `edge.py`, `benchmark/runner.py`, `test_providers.py`, `test_p4_graph.py`, `graph.py`, `cli.py`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Why does `run_migration()` connect `graph.py` to `test_analyzer.py`, `run_one`, `run.py`, `sandbox/__init__.py`, `ExperienceStore`, `Router`, `report/__init__.py`, `PreconditionError`, `benchmark/runner.py`, `SandboxRunner`, `test_p4_graph.py`, `metrics/__init__.py`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Why does `SandboxRunner` connect `SandboxRunner` to `test_sandbox.py`, `test_benchmark.py`, `evidence.py`, `run.py`, `sandbox/__init__.py`, `loop.py`, `test_p2_end_to_end.py`, `sandbox/runner.py`, `test_p4_graph.py`, `graph.py`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Router` (e.g. with `PrivacyError` and `Tokens`) actually correct?**
  _`Router` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ExperienceStore` (e.g. with `Config` and `ReplayCorrector`) actually correct?**
  _`ExperienceStore` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SandboxRunner` (e.g. with `test_migrated_tree_satisfies_the_gold_semantic_check()` and `test_trajectory_is_reconstructed_from_the_checkpoint_file_on_disk()`) actually correct?**
  _`SandboxRunner` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `pkg`, `pkg`, `pkg` to the rest of the system?**
  _271 weakly-connected nodes found - possible documentation gaps or missing edges._