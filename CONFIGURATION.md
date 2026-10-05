# Configuration & Secrets

How to configure the MRA and manage API keys **securely**. This document contains no secrets — real keys live only in your local, gitignored `.env` file.

> **Why there is no `api_keys.md`:** putting API keys in a markdown (or any tracked) file is how secrets get committed to git and leaked publicly. Once a key is in git history it is compromised even after deletion. Keys go in environment variables, loaded from a `.env` file that git ignores. This is the standard, non-negotiable pattern.

## 1. First-time setup

```bash
cp .env.example .env      # create your local, private config
$EDITOR .env              # fill in real values
```

`.env` is listed in `.gitignore`. Verify it is ignored before your first commit:

```bash
git check-ignore .env     # should print: .env
git status                # .env must NOT appear as a tracked/staged file
```

## 2. Keys

Keys live only in environment variables. Which variable each provider reads is
set by `api_key_env` in `mra.toml` (§3) — the config holds the variable's
**name**, never the key. `api_key_envs = ["A", "B"]` gives an ordered list: B is
used only when the server refuses A (401/403). A rate limit (429) backs off and
retries the same key up to `max_retries` times (default 2); a timeout,
connection error or 5xx is retried once, then the run fails RED `provider`.
Each call logs the variable name that served it, never its value.

| Variable | Used by (in `mra.example.toml`) | Notes |
|---|---|---|
| `DEEPSEEK_API_KEY` | `deepseek-pro`, `deepseek-flash` | |
| `NVIDIA_API_KEY`, `NVIDIA_API_KEY_2` | `nvidia` (commented) | Primary and backup key. |
| `OPENAI_API_KEY` | `openai` | |
| `ANTHROPIC_API_KEY` | `anthropic` | |
| `GLM_API_KEY` | `glm` | |
| *(none)* | `ollama` and other local runtimes | A local server needs no key; omit `api_key_env`. |

The live benchmark arms and the two live tests run when every role in
`mra.toml` names the same single provider and its key is set; otherwise they
are skipped, never faked.

No key is required at all for the deterministic path (codemods + deterministic
corrector). With nothing usable configured, `Router.available` is false and
every node takes its offline branch.

## 3. Providers and roles — `mra.toml`

Every model name and base URL comes from `mra.toml` (gitignored). Start from the
committed template:

```bash
cp mra.example.toml mra.toml
mra providers check          # ping each entry: reachable / WARN + latency
```

`MRA_CONFIG=/path/to/file.toml` points at a different file.

**Providers.** Each `[providers.<name>]` table is one endpoint:

| Key | Meaning |
|---|---|
| `provider` | `openai-compatible` (DeepSeek, OpenAI, GLM, Ollama, vLLM, llama.cpp server, LM Studio) or `anthropic` (native SDK) |
| `base_url` | Endpoint root, e.g. `http://localhost:11434/v1` for Ollama. Required. |
| `model` | Model name sent to that endpoint. Required. |
| `api_key_env` | Name of the env var holding the key. Omit for a keyless local runtime. |
| `timeout_s` | Per-call timeout before falling back (default `120`). |
| `redact_secrets` | Scrub secret-shaped strings before sending (default: `true` for remote hosts, `false` for local ones). |

**Roles.** `[roles]` maps each of the four roles to an ordered chain of provider
names. The first is the primary; later entries are tried only if an earlier one
raises or times out:

| Role | Used for | Billing tier (M3) |
|---|---|---|
| `edit` | LLM edits | pro |
| `recover` | Corrective patches in the CORRECT loop | pro |
| `summarize` | Rolling progress note | flash |
| `classify` | Failure classification | flash |

```toml
[roles]
recover = ["ollama", "deepseek-pro"]   # local first, DeepSeek if Ollama is down
```

Every served call is recorded in `Router.calls` with role, provider, model,
`tokens_in`/`tokens_out`, latency, redaction count and, when it was a fallback,
`fallback_from`. The example's base URLs and model names are starting points —
verify them in each provider's docs. Note the pinned Anthropic SDK takes no
`temperature`, so `MRA_LLM_TEMPERATURE` does not apply to the `anthropic` provider.

The benchmark's `edit-v4-flash` arm serves `recover` with the `classify` chain.

## 4. Configuration variables (non-secret)

These tune the agent and mirror the non-functional constraints in `docs/03_SRS.md §6`.

| Variable | Meaning | Default |
|---|---|---|
| `MRA_CONFIG` | Path to the provider/role config | `mra.toml` |
| `MRA_PRIVACY` | `local-only` to forbid every non-local provider (§5) | unset |
| `MRA_MAX_FIX_ATTEMPTS` | Recovery retry ceiling per failure signature | `3` |
| `MRA_TOKEN_BUDGET` | Per-task token ceiling; a run over it is reported RED (recorded in `run_meta.json`; the run is not aborted) | `2000000` |
| `MRA_RUN_TIMEOUT_SEC` | Per-run wall-clock limit; a run over it is reported RED (not aborted) | `1800` |
| `MRA_PYTEST_TIMEOUT_SEC` | Per-`pytest` invocation timeout (in sandbox) | `120` |
| `MRA_EDIT_BATCH_SIZE` | Files per EDIT batch (ablation variable) | `3` |
| `MRA_LLM_TEMPERATURE` | LLM temperature (determinism) | `0.1` |
| `MRA_SANDBOX_IMAGE` | Docker image tag for the sandbox | `mra-sandbox:py312` |
| `MRA_CONTAINER_RUNTIME` | `docker` or `podman` | `docker` |
| `NO_COLOR` | Any non-empty value turns off the coloured verdict banner in `mra run` / `mra report` | unset |
| `MRA_EXPERIENCE` | `on` / `off` for the experience store (§5); `off` beats `mra.toml` | unset (= off) |
| `MRA_EXPERIENCE_DB` | Experience store file | `~/.mra/experience.db` |
| `MRA_SKILLS` | `on` / `off` for promoted skills in `mra run` (§5); `off` beats `mra.toml` | unset (= off) |

`MRA_EDIT_MODEL`, `MRA_UTILITY_MODEL` and `DEEPSEEK_BASE_URL` were removed in
0.2.0; set `model` / `base_url` in `mra.toml` instead.

## 5. Privacy

The router enforces these before any byte reaches a provider (`src/mra/models/privacy.py`):

- **`MRA_PRIVACY=local-only`** — only providers whose `base_url` host is
  `localhost`, a loopback address (`127.0.0.1`, `::1`) or a private-network
  address (`10/8`, `172.16/12`, `192.168/16`, …) may be called. Anything else
  raises `PrivacyError` before a socket opens or a DNS lookup happens. This
  applies to fallbacks too: in `["ollama", "deepseek-pro"]`, an Ollama failure
  raises `PrivacyError` rather than sending the prompt to DeepSeek. The check is
  on the configured URL text, not on DNS, so a hostname is always treated as
  remote. An unrecognised `MRA_PRIVACY` value is an error, not "off".
- **Secret redaction** — for remote providers (by default), strings shaped like
  API keys and tokens (`sk-…`, AWS `AKIA…`, GitHub `ghp_…`/`github_pat_…`, Slack
  `xox…-`, Google `AIza…`, JWTs, PEM private keys, and `*key|secret|token|password
  = "…"` assignments) are replaced with `[REDACTED]` in the code context before
  sending. The count is logged per call as `redactions`.
- **Data-egress log** — `Router.egress` records, per remote host, the number of
  calls and bytes sent this run. Local hosts are not counted.
- **Experience store (opt-in, off by default)** — `[experience] enabled = true`
  (optional `path = "..."`) in `mra.toml`, or `MRA_EXPERIENCE=on`, makes `mra run`
  keep a local SQLite file of past fixes (`src/mra/memory/experience.py`). Only
  from a run whose report is fully GREEN (verdict GREEN, no residual sites, the
  whole suite green): a fix that passed the tests but left old-API sites behind
  is never stored. Each storing run is kept as provenance (run id, and a hash of
  the task name — never the name); entries none of whose runs is within
  `ttl_days` (default 90) are expired and ignored. From such a run, for each
  CORRECT whose re-test is green, it stores the failure class, the normalised
  message, the contract and the changed lines of the fix — never a file path,
  and secret-redacted. On a new failure the closest past fixes go into the
  CORRECT prompt as hints (capped at 1200 chars). The file is refused if it would
  sit inside the agent's repo or the repo being migrated, and nothing in it is
  ever sent anywhere except as those hints, to the provider your `recover` role
  already uses. The benchmark never reads or writes it. `mra memory stats`,
  `mra memory export` (JSON), `mra memory purge` (deletes it — fixes,
  provenance and promoted skills — no prompt).
- **Promoted skills (opt-in, off by default)** — `src/mra/skills.py`. A fix the
  store saw work in fully GREEN runs on at least 3 *distinct* tasks, for the
  same failure class and contract, becomes a candidate, reduced to a LibCST
  rule (the smallest changed expressions plus the imports they add).
  `mra skills review` lists candidates with their run ids and rule;
  `mra skills approve <id>` first re-runs the full edge suite and the
  deterministic Tier-A matrix with the rule on, and promotes it only if both
  are unchanged; `mra skills revoke <id>` stops a rule and stops it being
  offered again. Nothing is promoted automatically. With `[skills] enabled =
  true` or `MRA_SKILLS=on`, `mra run` tries promoted rules in CORRECT before the
  corrector (so before any model call); the report's timeline and
  `skills_fired` name the rule. EDIT is already a codemod and calls no model.
  The benchmark never reads promoted skills (ablation F builds its own).

## 6. Security rules

- **Never** commit `.env`, a key, or a token. If `git status` ever shows `.env`, stop and fix `.gitignore`.
- **Never** print a key to logs or the trajectory. Log the *model ID* and *token counts*, not credentials.
- **Never** pass secrets in URL query strings.
- **If a key is exposed** (pushed to a public repo, pasted in an issue), **rotate it immediately** at the provider and purge git history if needed.
- Inside the sandbox, the agent runs with `--network none` at execution time; the key is used only by the host-side orchestrator that calls the LLM API, not inside the code-execution container.
- Keep `.env.example` in sync with `.env` **keys** (names only, placeholder values) so collaborators know what to set.

## 7. CI / grading environments

For CI or a shared grading machine, set the same variables as real environment secrets (e.g. repository secrets), not a committed file. The code reads `os.environ` either way, so no code changes are needed.
