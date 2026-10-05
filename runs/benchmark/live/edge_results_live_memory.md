# Edge-case accuracy suite

Agent 0.2.0 · generated 2026-10-05T04:26:16+00:00 · **36/36 cases give the expected verdict.**

Each case asserts the verdict, the reason that produced it, and (for byte-level cases) a byte-exact match with `gold/`. Regenerate with `python -m mra.benchmark.edge`; fixtures come from `corpus/edge/_build.py`.

Live: the corrector is the real model from `mra.toml`, `nvidia/nemotron-3-super-120b-a12b` via `nvidia` (3 repeat(s) per case, no fallback provider).

| case | rep | expected | actual | pass | M1 | M2 | corr | tokens | cost $ | failure class | reason / note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `cross_file_recovery_llm` | 0 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 448 | 0.0002 | — | same break, repaired by the LLM corrector through FakeProvider (offline) |
| `cross_file_recovery_llm` | 1 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 448 | 0.0002 | — | same break, repaired by the LLM corrector through FakeProvider (offline) |
| `cross_file_recovery_llm` | 2 | GREEN | GREEN | yes | 100.0 | 100.0 | 1 | 448 | 0.0002 | — | same break, repaired by the LLM corrector through FakeProvider (offline) |
| `bare_reference` | 0 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/core.py:3 (bare-reference) |
| `bare_reference` | 1 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/core.py:3 (bare-reference) |
| `bare_reference` | 2 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/core.py:3 (bare-reference) |
| `deprecated_call_in_test_file` | 0 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): tests/test_core.py:7 |
| `deprecated_call_in_test_file` | 1 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): tests/test_core.py:7 |
| `deprecated_call_in_test_file` | 2 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): tests/test_core.py:7 |
| `star_import` | 0 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/legacy.py:1 (star-import) |
| `star_import` | 1 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/legacy.py:1 (star-import) |
| `star_import` | 2 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW residual: 1 site(s): src/pkg/legacy.py:1 (star-import) |
| `syntax_error_file` | 0 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW unparseable: src/pkg/broken.py |
| `syntax_error_file` | 1 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW unparseable: src/pkg/broken.py |
| `syntax_error_file` | 2 | YELLOW | YELLOW | yes | 100.0 | 100.0 | 0 | 0 | 0.0000 | — | YELLOW unparseable: src/pkg/broken.py |
| `edit_causes_infinite_loop` | 0 | RED | RED | yes | 100.0 | 0.0 | 1 | 587 | 0.0003 | behaviour | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 0 failed, 1 errors — <sandbox> (Timeout: pytest exceeded the sandbox timeout); YELLOW unexecuted: coverage.json unreadable (FileNotFoundError) |
| `edit_causes_infinite_loop` | 1 | RED | RED | yes | 100.0 | 0.0 | 1 | 562 | 0.0003 | behaviour | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 0 failed, 1 errors — <sandbox> (Timeout: pytest exceeded the sandbox timeout); YELLOW unexecuted: coverage.json unreadable (FileNotFoundError) |
| `edit_causes_infinite_loop` | 2 | RED | RED | yes | 100.0 | 0.0 | 1 | 475 | 0.0002 | behaviour | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 0 failed, 1 errors — <sandbox> (Timeout: pytest exceeded the sandbox timeout); YELLOW unexecuted: coverage.json unreadable (FileNotFoundError) |
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
| `unfixable_break` | 0 | RED | RED | yes | 100.0 | 0.0 | 3 | 2477 | 0.0010 | assertion | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_core.py::test_naive_contract (AssertionError) |
| `unfixable_break` | 1 | RED | RED | yes | 100.0 | 0.0 | 3 | 2318 | 0.0009 | assertion | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_core.py::test_naive_contract (AssertionError) |
| `unfixable_break` | 2 | RED | RED | yes | 100.0 | 0.0 | 3 | 2309 | 0.0009 | assertion | RED gave_up: metrics.json: outcome=gave_up; RED suite_red: test_report.json: 1 failed, 0 errors — tests/test_core.py::test_naive_contract (AssertionError) |
| `zero_tests` | 0 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | — | RED precondition: test_report_pre.json: 0/0 passed, 0 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `zero_tests` | 1 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | — | RED precondition: test_report_pre.json: 0/0 passed, 0 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
| `zero_tests` | 2 | RED | RED | yes | None | None | 0 | 0 | 0.0000 | — | RED precondition: test_report_pre.json: 0/0 passed, 0 failed, 0 errors; YELLOW residual: 1 site(s): src/pkg/core.py:5 |
