# Graph Report - File1  (2026-10-01)

## Corpus Check
- 171 files · ~93,979 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1425 nodes · 2404 edges · 102 communities (79 shown, 23 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 178 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5cef26f4`
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
- router.py
- run.py
- correct_node.py
- test_recovery.py
- test_benchmark.py
- make_timestamp
- run_one
- make_timestamp
- sandbox/__init__.py
- new_state
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
- baselines.py
- _ImportCollector
- _CallSiteVisitor
- handle
- old/src/pkg/ledger.py
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
- test_providers.py
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
- models/__init__.py
- verify_paper.py
- What the Tier-A benchmark shows
- Provider
- task05_signature_break/gold/src/pkg/__init__.py
- task05_signature_break/old/src/pkg/__init__.py
- pkg
- pkg
- llm_server
- is_local
- SandboxRunner
- .complete

## God Nodes (most connected - your core abstractions)
1. `Router` - 35 edges
2. `migrate_task()` - 28 edges
3. `SandboxRunner` - 28 edges
4. `run_migration()` - 25 edges
5. `run_one()` - 19 edges
6. `analyze()` - 17 edges
7. `FakeProvider` - 16 edges
8. `locate()` - 16 edges
9. `apply_codemod()` - 16 edges
10. `Migration Agent — Master Resource Pack` - 16 edges

## Surprising Connections (you probably didn't know these)
- `analyses()` --calls--> `analyze()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/analyzer.py
- `test_fr3_property_holds_for_every_task_in_the_corpus()` --calls--> `analyze()`  [INFERRED]
  tests/test_p4_graph.py → src/mra/analysis/analyzer.py
- `test_task04_batches_are_dependency_ordered_and_collapse_the_cycle()` --calls--> `analyze()`  [INFERRED]
  tests/test_p4_graph.py → src/mra/analysis/analyzer.py
- `test_every_import_spelling_resolves_to_one_symbol()` --calls--> `find_in_source()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/call_sites.py
- `test_finder_does_not_match_lookalikes()` --calls--> `find_in_source()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/call_sites.py

## Import Cycles
- None detected.

## Communities (102 total, 23 thin omitted)

### Community 0 - "test_sandbox.py"
Cohesion: 0.06
Nodes (49): Phase, _exc_type_from(), _failure_from_collector(), _failure_from_test(), failure_signature(), _lint_counts(), normalize_message(), Any (+41 more)

### Community 1 - "analysis/__init__.py"
Cohesion: 0.13
Nodes (25): analyze(), Any, Path, MAP-node analysis: locate the work, map the dependencies. Nothing else.…, Scan ``repo`` for ``target`` and map its imports. Args: repo: repository root…, build(), from_state_adjacency(), module_index() (+17 more)

### Community 2 - "test_analyzer.py"
Cohesion: 0.19
Nodes (20): flat_sites(), Flatten the per-file map into one list, the form ground truth uses., analyses(), _ground_truth(), _key(), Any, fixture, parametrize (+12 more)

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
Cohesion: 0.09
Nodes (23): 0. Read this first — the one thing that will sink you, 10. Trap checklist (expanded with the version facts I found), 11. Questions for Dr Nimrita Koul (first meeting) — refined, 12. The paper plan (start the skeleton in week 1, not week 9), 13. Your one-sentence story (memorize it — this is the interview weapon), 1. Verified stack (checked 24 Aug 2026), 2.1 `datetime.utcnow()` → timezone-aware (EASY — build this first), 2.2 Python 3.8 → 3.12 modernization (EASY–MEDIUM, has a baseline) (+15 more)

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
Cohesion: 0.24
Nodes (9): CallSite, find_in_repo(), find_in_source(), Any, Path, Find every call to a target symbol, whatever spelling the file uses. This is…, Locate every call to ``target`` in one module's source text., Scan a repo for ``target`` and return the ``MigrationState.call_sites`` map.… (+1 more)

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
Cohesion: 0.06
Nodes (27): task01_datetime — Tier-A controlled task, Test-oracle rule, The `pkg` name-collision gotcha, The two states live in one commit, Import changes: deliberately empty, Running the two states, task02_datetime_aliased — Tier-A controlled task, The cross-file break (+19 more)

### Community 17 - "CLAUDE.md"
Cohesion: 0.20
Nodes (9): Coding conventions, Commit conventions, Current phase / context, Golden rules (do not violate), How to run and test, Tech stack (fixed — verified Sep 2026), What this project is, When unsure (+1 more)

### Community 18 - "Configuration & Secrets"
Cohesion: 0.22
Nodes (8): 1. First-time setup, 2. Keys, 3. Providers and roles — `mra.toml`, 4. Configuration variables (non-secret), 5. Privacy, 6. Security rules, 7. CI / grading environments, Configuration & Secrets

### Community 28 - "test_p4_graph.py"
Cohesion: 0.05
Nodes (61): ConvertUtcnowCommand, Rewrite every resolved ``datetime.utcnow()`` call, whatever its spelling., Deterministic libcst codemods, one per migration task (golden rule 5)., apply_codemod(), Any, Path, Run the codemod over every file in ``call_sites``; return the ones that…, State-machine nodes: plain ``state -> partial update`` functions, wired… (+53 more)

### Community 29 - "graph.py"
Cohesion: 0.12
Nodes (29): all_batches_done(), build_graph(), _cap(), changed_files(), finish_node(), is_green(), _key(), outcome_of() (+21 more)

### Community 30 - "router.py"
Cohesion: 0.12
Nodes (27): Roles, main(), providers_check(), The ``mra`` command. ``mra providers check`` pings every configured provider.…, Migration & Refactoring Agent., host_of(), privacy_mode(), Where a prompt is allowed to go, and what is scrubbed out of it first. Two… (+19 more)

### Community 31 - "run.py"
Cohesion: 0.12
Nodes (18): Collection, M1 and M2, following docs/05_DATA_EVALUATION_PROTOCOL.md. M3 (tokens, cost) is…, m1(), M1 — Migration Completeness. Transcribed verbatim from…, m2(), M2 — Post-Migration Test Pass Rate. Transcribed verbatim from…, _key(), main() (+10 more)

### Community 32 - "correct_node.py"
Cohesion: 0.07
Nodes (41): edit_context(), graph_slice(), offline_summary(), progress_facts(), Any, Rolling memory: what the model is told about everything that is not in front of…, The dependency neighbourhood, truncated to a constant number of names., The complete payload for one corrective-edit call (NFR-12). Everything except… (+33 more)

### Community 33 - "test_recovery.py"
Cohesion: 0.08
Nodes (48): bad_corrector(), corpus_digest(), gave_up(), _nodes(), oracle_tampering_corrector(), Any, fixture, needs_docker (+40 more)

### Community 34 - "test_benchmark.py"
Cohesion: 0.08
Nodes (43): ablation_a(), ablation_b(), ablation_b_task05(), corpus_digests(), matrix(), Any, fixture, parametrize (+35 more)

### Community 35 - "make_timestamp"
Cohesion: 0.08
Nodes (28): audit_record(), audit_window(), datetime, Audit trail. Imports the clock contract and also reads the clock directly., Return the ``seconds``-long window ending now. Both ends come from the same…, Stamp an audit record from the shared clock., make_timestamp(), datetime (+20 more)

### Community 36 - "run_one"
Cohesion: 0.11
Nodes (21): P5 benchmarking: run the agent across the corpus under controlled conditions., ``python -m mra.benchmark`` — run the matrix and write the report., codemod_corrector(), Config, _env(), _f1(), failure_analysis(), main() (+13 more)

### Community 37 - "make_timestamp"
Cohesion: 0.08
Nodes (26): audit_record(), audit_window(), datetime, Audit trail. Imports the clock contract and also reads the clock directly., Return the ``seconds``-long window ending now. Both ends come from the same…, Stamp an audit record from the shared clock., make_timestamp(), datetime (+18 more)

### Community 38 - "sandbox/__init__.py"
Cohesion: 0.19
Nodes (17): make_correct_node(), Bind a corrector and return the node LangGraph calls. One visit repairs one…, changed_paths(), diff(), Path, Git snapshot / rollback / diff, exposed as agent tools. These operate on the…, Open ``path`` as a git repo, initializing it if it is not one yet., Commit the whole working tree and return the new commit SHA. Allows an empty… (+9 more)

### Community 39 - "new_state"
Cohesion: 0.16
Nodes (14): Every token in and out, across both tiers — the M3 headline number., total_tokens(), Contract, MigrationState, new_state(), TypedDict, ``MigrationState`` — the agent's working memory. A transcription of the…, What is being migrated, from the task's ``ground_truth.json``. (+6 more)

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
Cohesion: 0.15
Nodes (13): Acknowledgements, Architecture at a glance, Codebase-Wide Version Migration & Refactoring Agent (MRA), Documentation index, Evaluation, License, LLM providers and privacy, Quickstart (+5 more)

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

### Community 54 - "baselines.py"
Cohesion: 0.16
Nodes (23): CompletedProcess, baseline_table(), _detect_with_ruff(), Any, Path, pyupgrade_baseline(), The honesty check: what the existing static tools already do (docs/05, §2.2).…, Run pyupgrade over the task and score it the same way. (+15 more)

### Community 55 - "_ImportCollector"
Cohesion: 0.25
Nodes (6): _ImportCollector, _module_name(), BaseExpression, Import, ImportFrom, Collects the dotted module names a file imports, including submodules.

### Community 56 - "_CallSiteVisitor"
Cohesion: 0.18
Nodes (9): Name, _CallSiteVisitor, dotted_path(), Call, Resolves every dotted call against this module's import bindings., True if ``head`` is bound by anything other than an import here. Guards…, Flatten ``a.b.c`` into its head ``Name`` node and the attribute names after it.…, BaseExpression (+1 more)

### Community 57 - "handle"
Cohesion: 0.33
Nodes (6): handle(), Serve one request. ``served_at`` is this module's own, self-contained reading., The entry point, exercising the whole import DAG in one call., Syntactic success is not success: no module may be left on a naive clock., test_every_stamp_in_one_response_is_aware(), test_handle_serves_a_complete_response()

### Community 58 - "old/src/pkg/ledger.py"
Cohesion: 0.33
Nodes (6): datetime, Double-entry ledger. Half of the import cycle with :mod:`pkg.audit`. ``import…, The ``seconds``-long window ending now. Both ends come from one reading, so…, snapshot_window(), Both ends come from one reading — safe whichever side of the migration., test_snapshot_window_is_ordered()

### Community 60 - "gold/src/pkg/api.py"
Cohesion: 0.33
Nodes (4): The entry point. Depends on report, audit and config — the graph's deepest…, Static settings. No clock, no in-repo imports — the graph's other root., How long a record is kept, in seconds., retention_seconds()

### Community 61 - "datetime_utcnow.py"
Cohesion: 0.33
Nodes (4): T1 codemod: ``datetime.utcnow()`` -> ``datetime.now(timezone.utc)``.…, make_edit_node(), EDIT node: apply the migration codemod to the files the analyzer flagged. It…, Bind nothing and return the node LangGraph calls. The node edits…

### Community 62 - "plan_batches"
Cohesion: 0.14
Nodes (22): make_planner(), Return the PLAN node for an ordering arm. * ``dependency`` — the agent's own…, _chunk(), cycles(), plan_batches(), plan_node(), Any, DiGraph (+14 more)

### Community 63 - "Failure analysis"
Cohesion: 0.13
Nodes (15): Failure analysis, `no-recovery` on task02_datetime_aliased, `no-recovery` on task03_half_migration, `no-recovery` on task04_multimodule, `order-alphabetical-b1-norecovery` on task02_datetime_aliased, `order-alphabetical-b1-norecovery` on task03_half_migration, `order-alphabetical-b1-norecovery` on task04_multimodule, `order-alphabetical-b1-norecovery` on task05_signature_break (+7 more)

### Community 73 - "providers/__init__.py"
Cohesion: 0.14
Nodes (12): AnthropicProvider, Message, Anthropic's native Messages API, through the pinned ``anthropic`` SDK. The…, Completion, KeyedProvider, TypedDict, The provider contract and the key lookup every networked provider shares., Common state: where it lives, which env var holds its key, how long to wait.… (+4 more)

### Community 74 - "test_providers.py"
Cohesion: 0.16
Nodes (20): FakeProvider, Answers from ``reply(messages, model)`` (default: echo the last message).…, OpenAICompatibleProvider, Any, Provider layer, router fallback, privacy mode, redaction, egress — all offline.…, Every call is recorded with who served it, the model, and the tokens., End to end over real HTTP: request shape out, Completion shape back., _router() (+12 more)

### Community 75 - "snapshot"
Cohesion: 0.16
Nodes (10): The service edge: the deepest module in the import DAG., One request, its ledger entry and a metrics snapshot., serve(), Point-in-time metrics over the ledger., Entry count plus how long this reading took to assemble., snapshot(), The service edge: every module in the DAG on one call path., test_serve_returns_the_whole_response() (+2 more)

### Community 76 - "ImportBindings"
Cohesion: 0.14
Nodes (11): bindings_of(), ImportBindings, _module_name(), BaseExpression, Import, ImportFrom, Module, Collect a whole module's import bindings up front. (+3 more)

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
Cohesion: 0.23
Nodes (19): _ablation_a(), _ablation_b(), _ablation_c(), _ablation_d(), _aggregate(), _baseline_section(), _cell(), _failures() (+11 more)

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

### Community 90 - "models/__init__.py"
Cohesion: 0.18
Nodes (11): Role, RuntimeError, LLM routing, providers, privacy and token accounting. Models come from mra.toml., PrivacyError, A call was refused by the privacy policy before any network I/O., Return ``text`` with secret-shaped strings replaced, and how many were., redact_secrets(), Endpoint (+3 more)

### Community 91 - "verify_paper.py"
Cohesion: 0.29
Nodes (11): carries_a_figure(), cells(), check(), figures(), main(), Check paper.md against the artefacts it cites. Run after any benchmark rerun.…, True if the line states a number, ignoring identifiers that contain digits., Every table under `header`, in document order, header and rule dropped. (+3 more)

### Community 92 - "What the Tier-A benchmark shows"
Cohesion: 0.40
Nodes (5): (a) The recovery loop is what finishes a cross-file migration, (b) The existing static tools detect the work and do none of it, (c) Dependency-ordered batching: what the data actually supports, Scope and honesty notes, What the Tier-A benchmark shows

### Community 93 - "Provider"
Cohesion: 0.25
Nodes (6): Provider, Message, Protocol, make_provider(), Any, Build the provider for one ``[providers.<name>]`` table of ``mra.toml``.

### Community 98 - "llm_server"
Cohesion: 0.29
Nodes (7): SimpleNamespace, llm_server(), _no_privacy_env(), fixture, MonkeyPatch, A tiny OpenAI-compatible server on 127.0.0.1. Records every request., test_anthropic_provider_lifts_the_system_prompt()

### Community 99 - "is_local"
Cohesion: 0.33
Nodes (5): is_local(), True for no-network, localhost, loopback and private-network addresses., parametrize, test_is_local(), test_live_provider_answers()

### Community 100 - "SandboxRunner"
Cohesion: 0.40
Nodes (5): make_test_node(), TEST node: verify the tree in the sandbox and write the report into state…, Bind the sandbox and return the node LangGraph calls., Runs a repo's suite in one throwaway container and returns a test_report. The…, SandboxRunner

## Knowledge Gaps
- **213 isolated node(s):** `pkg`, `pkg`, `pkg`, `pkg`, `pkg` (+208 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SandboxRunner` connect `SandboxRunner` to `test_sandbox.py`, `sandbox/__init__.py`, `loop.py`, `test_p2_end_to_end.py`, `baselines.py`, `test_p4_graph.py`, `graph.py`, `run.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `Router` connect `graph.py` to `correct_node.py`, `test_recovery.py`, `is_local`, `run_one`, `sandbox/__init__.py`, `new_state`, `test_providers.py`, `benchmark/runner.py`, `models/__init__.py`, `test_p4_graph.py`, `router.py`, `run.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Router` (e.g. with `PrivacyError` and `Tokens`) actually correct?**
  _`Router` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SandboxRunner` (e.g. with `test_migrated_tree_satisfies_the_gold_semantic_check()` and `test_trajectory_is_reconstructed_from_the_checkpoint_file_on_disk()`) actually correct?**
  _`SandboxRunner` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `pkg`, `pkg`, `pkg` to the rest of the system?**
  _213 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_sandbox.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05844155844155844 - nodes in this community are weakly interconnected._
- **Should `analysis/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12698412698412698 - nodes in this community are weakly interconnected._