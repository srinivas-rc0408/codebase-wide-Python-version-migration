# Edge-case accuracy suite

Agent 0.2.0 · generated 2026-10-05T04:24:19+00:00 · **117/117 cases give the expected verdict.**

Each case asserts the verdict, the reason that produced it, and (for byte-level cases) a byte-exact match with `gold/`. Regenerate with `python -m mra.benchmark.edge`; fixtures come from `corpus/edge/_build.py`.

Live: the corrector is the real model from `mra.toml`, `nvidia/nemotron-3-super-120b-a12b` via `nvidia` (3 repeat(s) per case, no fallback provider).

| case | rep | expected | actual | pass | M1 | M2 | corr | tokens | cost $ | failure class | reason / note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `aliased_class` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `aliased_class` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `aliased_class` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `aliased_module` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `aliased_module` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `aliased_module` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `cross_file_recovery` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 1696 | 0.0016 | — | core moves first; report breaks until CORRECT migrates it |
| `cross_file_recovery` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 1474 | 0.0011 | — | core moves first; report breaks until CORRECT migrates it |
| `cross_file_recovery` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 1427 | 0.0010 | — | core moves first; report breaks until CORRECT migrates it |
| `cross_file_recovery_llm` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 448 | 0.0002 | — | same break, repaired by the LLM corrector through FakeProvider (offline) |
| `cross_file_recovery_llm` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 448 | 0.0002 | — | same break, repaired by the LLM corrector through FakeProvider (offline) |
| `cross_file_recovery_llm` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 448 | 0.0002 | — | same break, repaired by the LLM corrector through FakeProvider (offline) |
| `from_import` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `from_import` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `from_import` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `import_cycle` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `import_cycle` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `import_cycle` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `module_import` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `module_import` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `module_import` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `multi_site_one_file` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `multi_site_one_file` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `multi_site_one_file` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `sites_across_six_files` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `sites_across_six_files` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `sites_across_six_files` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `utcfromtimestamp_alongside_utcnow` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `utcfromtimestamp_alongside_utcnow` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `utcfromtimestamp_alongside_utcnow` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `class_body_and_classmethod` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `class_body_and_classmethod` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `class_body_and_classmethod` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `conditional_import` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `conditional_import` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `conditional_import` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `crlf_line_endings` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | CRLF must survive byte-exact |
| `crlf_line_endings` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | CRLF must survive byte-exact |
| `crlf_line_endings` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | CRLF must survive byte-exact |
| `default_argument` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `default_argument` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `default_argument` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `encoding_cookie_non_ascii` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | latin-1 source with a coding cookie and non-ASCII identifiers |
| `encoding_cookie_non_ascii` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | latin-1 source with a coding cookie and non-ASCII identifiers |
| `encoding_cookie_non_ascii` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | latin-1 source with a coding cookie and non-ASCII identifiers |
| `inside_decorator_argument` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `inside_decorator_argument` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `inside_decorator_argument` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `inside_fstring` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `inside_fstring` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `inside_fstring` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `inside_lambda` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `inside_lambda` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `inside_lambda` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `other_object_with_utcnow` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `other_object_with_utcnow` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `other_object_with_utcnow` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `reexport_through_init` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | `datetime` reaches core.py through the package's re-export |
| `reexport_through_init` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | `datetime` reaches core.py through the package's re-export |
| `reexport_through_init` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | `datetime` reaches core.py through the package's re-export |
| `relative_imports` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 1374 | 0.0010 | — | — |
| `relative_imports` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 1392 | 0.0010 | — | — |
| `relative_imports` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 1584 | 0.0014 | — | — |
| `shadowed_local_name` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `shadowed_local_name` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `shadowed_local_name` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `tab_indentation` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `tab_indentation` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `tab_indentation` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `utcnow_in_strings_comments_docstrings` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | only the real call may change |
| `utcnow_in_strings_comments_docstrings` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | only the real call may change |
| `utcnow_in_strings_comments_docstrings` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | only the real call may change |
| `very_long_file` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | 5209 lines |
| `very_long_file` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | 5209 lines |
| `very_long_file` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | 5209 lines |
| `already_migrated` | 0 | GREEN | GREEN | yes | 0.0 | 100.0 | 0 | 0 | 0.0000 | — | idempotence: zero edits, empty patch |
| `already_migrated` | 1 | GREEN | GREEN | yes | 0.0 | 100.0 | 0 | 0 | 0.0000 | — | idempotence: zero edits, empty patch |
| `already_migrated` | 2 | GREEN | GREEN | yes | 0.0 | 100.0 | 0 | 0 | 0.0000 | — | idempotence: zero edits, empty patch |
| `bare_reference` | 0 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/core.py:3 (bare-reference) |
| `bare_reference` | 1 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/core.py:3 (bare-reference) |
| `bare_reference` | 2 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/core.py:3 (bare-reference) |
| `deprecated_call_in_test_file` | 0 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): tests/test_core.py:7 |
| `deprecated_call_in_test_file` | 1 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): tests/test_core.py:7 |
| `deprecated_call_in_test_file` | 2 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): tests/test_core.py:7 |
| `empty_and_comment_only_files` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `empty_and_comment_only_files` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `empty_and_comment_only_files` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `half_migrated` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `half_migrated` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `half_migrated` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | — |
| `star_import` | 0 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/legacy.py:1 (star-import) |
| `star_import` | 1 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/legacy.py:1 (star-import) |
| `star_import` | 2 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/legacy.py:1 (star-import) |
| `syntax_error_file` | 0 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW unparseable: src/pkg/broken.py |
| `syntax_error_file` | 1 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW unparseable: src/pkg/broken.py |
| `syntax_error_file` | 2 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW unparseable: src/pkg/broken.py |
| `edit_causes_infinite_loop` | 0 | RED | RED | yes | 100.0 | 0.0 | 1 | 467 | 0.0002 | behaviour | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 0 failed, 1 errors — <sandbox> (Timeout: pytest exceeded the sandbox timeout); YELLOW unexecuted: coverage.json unreadable (FileNotFoundError) |
| `edit_causes_infinite_loop` | 1 | RED | RED | yes | 100.0 | 0.0 | 1 | 467 | 0.0002 | behaviour | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 0 failed, 1 errors — <sandbox> (Timeout: pytest exceeded the sandbox timeout); YELLOW unexecuted: coverage.json unreadable (FileNotFoundError) |
| `edit_causes_infinite_loop` | 2 | RED | RED | yes | 100.0 | 0.0 | 1 | 470 | 0.0002 | behaviour | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 0 failed, 1 errors — <sandbox> (Timeout: pytest exceeded the sandbox timeout); YELLOW unexecuted: coverage.json unreadable (FileNotFoundError) |
| `local_only_with_remote_providers` | 0 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | — | RED refused: PrivacyError: MRA_PRIVACY=local-only: role 'edit' has only remote providers (deepseek (api.deepseek.com)); refusing before any network I/O |
| `local_only_with_remote_providers` | 1 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | — | RED refused: PrivacyError: MRA_PRIVACY=local-only: role 'edit' has only remote providers (deepseek (api.deepseek.com)); refusing before any network I/O |
| `local_only_with_remote_providers` | 2 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | — | RED refused: PrivacyError: MRA_PRIVACY=local-only: role 'edit' has only remote providers (deepseek (api.deepseek.com)); refusing before any network I/O |
| `pre_suite_failing` | 0 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | assertion | RED precondition: test_report_pre.json: 1/2 passed, 1 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `pre_suite_failing` | 1 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | assertion | RED precondition: test_report_pre.json: 1/2 passed, 1 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `pre_suite_failing` | 2 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | assertion | RED precondition: test_report_pre.json: 1/2 passed, 1 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `provider_unreachable` | 0 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | behaviour | RED provider: ProviderError: role 'classify': every provider was unreachable or failed — local-dead at 127.0.0.1: APIConnectionError: Connection error.; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_report.py::test_age_is_small (TypeError); YELLOW residual: 1 site(s): src/pkg/report.py:7 |
| `provider_unreachable` | 1 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | behaviour | RED provider: ProviderError: role 'classify': every provider was unreachable or failed — local-dead at 127.0.0.1: APIConnectionError: Connection error.; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_report.py::test_age_is_small (TypeError); YELLOW residual: 1 site(s): src/pkg/report.py:7 |
| `provider_unreachable` | 2 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | behaviour | RED provider: ProviderError: role 'classify': every provider was unreachable or failed — local-dead at 127.0.0.1: APIConnectionError: Connection error.; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_report.py::test_age_is_small (TypeError); YELLOW residual: 1 site(s): src/pkg/report.py:7 |
| `test_needs_network` | 0 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | behaviour | RED precondition: test_report_pre.json: 1/2 passed, 1 failed, 0 errors; tests/test_core.py::test_fetch need(s) the network, which the sandbox does not have (--network none); YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `test_needs_network` | 1 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | behaviour | RED precondition: test_report_pre.json: 1/2 passed, 1 failed, 0 errors; tests/test_core.py::test_fetch need(s) the network, which the sandbox does not have (--network none); YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `test_needs_network` | 2 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | behaviour | RED precondition: test_report_pre.json: 1/2 passed, 1 failed, 0 errors; tests/test_core.py::test_fetch need(s) the network, which the sandbox does not have (--network none); YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `unfixable_break` | 0 | RED | RED | yes | 100.0 | 0.0 | 3 | 2323 | 0.0009 | assertion | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_core.py::test_naive_contract (AssertionError) |
| `unfixable_break` | 1 | RED | RED | yes | 100.0 | 0.0 | 3 | 2425 | 0.0009 | assertion | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_core.py::test_naive_contract (AssertionError) |
| `unfixable_break` | 2 | RED | RED | yes | 100.0 | 0.0 | 3 | 2299 | 0.0009 | assertion | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_core.py::test_naive_contract (AssertionError) |
| `zero_tests` | 0 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | — | RED precondition: test_report_pre.json: 0/0 passed, 0 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `zero_tests` | 1 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | — | RED precondition: test_report_pre.json: 0/0 passed, 0 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `zero_tests` | 2 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | — | RED precondition: test_report_pre.json: 0/0 passed, 0 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
