# Edge-case accuracy suite

Agent 0.2.0 · generated 2026-10-01T15:09:35+00:00 · **39/39 cases give the expected verdict.**

Each case asserts the verdict, the reason that produced it, and (for byte-level cases) a byte-exact match with `gold/`. Regenerate with `python -m mra.benchmark.edge`; fixtures come from `corpus/edge/_build.py`.

| case | category | expected verdict | actual | pass | reason / note |
|---|---|---|---|---|---|
| `aliased_class` | common | GREEN | GREEN | yes | — |
| `aliased_module` | common | GREEN | GREEN | yes | — |
| `cross_file_recovery` | common | GREEN | GREEN | yes | core moves first; report breaks until CORRECT migrates it |
| `cross_file_recovery_llm` | common | GREEN | GREEN | yes | same break, repaired by the LLM corrector through FakeProvider (offline) |
| `from_import` | common | GREEN | GREEN | yes | — |
| `import_cycle` | common | GREEN | GREEN | yes | — |
| `module_import` | common | GREEN | GREEN | yes | — |
| `multi_site_one_file` | common | GREEN | GREEN | yes | — |
| `sites_across_six_files` | common | GREEN | GREEN | yes | — |
| `utcfromtimestamp_alongside_utcnow` | common | GREEN | GREEN | yes | — |
| `class_body_and_classmethod` | rare | GREEN | GREEN | yes | — |
| `conditional_import` | rare | GREEN | GREEN | yes | — |
| `crlf_line_endings` | rare | GREEN | GREEN | yes | CRLF must survive byte-exact |
| `default_argument` | rare | GREEN | GREEN | yes | — |
| `encoding_cookie_non_ascii` | rare | GREEN | GREEN | yes | latin-1 source with a coding cookie and non-ASCII identifiers |
| `inside_decorator_argument` | rare | GREEN | GREEN | yes | — |
| `inside_fstring` | rare | GREEN | GREEN | yes | — |
| `inside_lambda` | rare | GREEN | GREEN | yes | — |
| `other_object_with_utcnow` | rare | GREEN | GREEN | yes | — |
| `reexport_through_init` | rare | GREEN | GREEN | yes | `datetime` reaches core.py through the package's re-export |
| `relative_imports` | rare | GREEN | GREEN | yes | — |
| `shadowed_local_name` | rare | GREEN | GREEN | yes | — |
| `tab_indentation` | rare | GREEN | GREEN | yes | — |
| `utcnow_in_strings_comments_docstrings` | rare | GREEN | GREEN | yes | only the real call may change |
| `very_long_file` | rare | GREEN | GREEN | yes | 5209 lines |
| `already_migrated` | twisted | GREEN | GREEN | yes | idempotence: zero edits, empty patch |
| `bare_reference` | twisted | YELLOW | YELLOW | yes | YELLOW residual: 1 site(s): src/pkg/core.py:3 (bare-reference) |
| `deprecated_call_in_test_file` | twisted | YELLOW | YELLOW | yes | YELLOW residual: 1 site(s): tests/test_core.py:7 |
| `empty_and_comment_only_files` | twisted | GREEN | GREEN | yes | — |
| `half_migrated` | twisted | GREEN | GREEN | yes | — |
| `star_import` | twisted | YELLOW | YELLOW | yes | YELLOW residual: 1 site(s): src/pkg/legacy.py:1 (star-import) |
| `syntax_error_file` | twisted | YELLOW | YELLOW | yes | YELLOW unparseable: src/pkg/broken.py |
| `edit_causes_infinite_loop` | failure | RED | RED | yes | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 0 failed, 1 errors — <sandbox> (Timeout: pytest exceeded the sandbox timeout); YELLOW unexecuted: coverage.json unreadable (FileNotFoundError) |
| `local_only_with_remote_providers` | failure | RED | RED | yes | RED refused: PrivacyError: MRA_PRIVACY=local-only: role 'edit' has only remote providers (deepseek (api.deepseek.com)); refusing before any network I/O |
| `pre_suite_failing` | failure | RED | RED | yes | RED precondition: test_report_pre.json: 1/2 passed, 1 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `provider_unreachable` | failure | RED | RED | yes | RED provider: ProviderError: role 'classify': every provider was unreachable or failed — local-dead at 127.0.0.1: APIConnectionError: Connection error.; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_report.py::test_age_is_small (TypeError); YELLOW residual: 1 site(s): src/pkg/report.py:7 |
| `test_needs_network` | failure | RED | RED | yes | RED precondition: test_report_pre.json: 1/2 passed, 1 failed, 0 errors; tests/test_core.py::test_fetch need(s) the network, which the sandbox does not have (--network none); YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `unfixable_break` | failure | RED | RED | yes | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_core.py::test_naive_contract (AssertionError) |
| `zero_tests` | failure | RED | RED | yes | RED precondition: test_report_pre.json: 0/0 passed, 0 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
