"""GREEN / YELLOW / RED: one answer to "can a human merge this patch?".

``verdict(run_artifacts)`` reads only what a run left behind (see
:func:`mra.report.load_run` for the keys) and returns ``{status, reasons}``.
Precedence is RED > YELLOW > GREEN; every reason that applies is listed, not
just the first, so the report can show the reviewer the whole picture.

* RED — the patch must not be merged as is: the precondition failed, the run
  crashed or gave up, the final suite is not green, the test oracle was
  touched, the patch does not apply to a fresh checkout, or a budget blew.
* YELLOW — the suite is green but the evidence is weaker than it looks:
  sites remain, it over-edited, a semantic check failed, lint got worse, a
  file could not be parsed, or an edited line never ran under any test.
* GREEN — none of the above.
"""

from __future__ import annotations

from collections import Counter
from typing import Any


def _reason(level: str, code: str, text: str, evidence: str, action: str) -> dict[str, str]:
    return {"level": level, "code": code, "text": text, "evidence": evidence, "action": action}


def _listing(items: list[str], limit: int = 5) -> str:
    shown = ", ".join(items[:limit])
    return shown + (f", +{len(items) - limit} more" if len(items) > limit else "")


def new_lint(lint: dict[str, Any]) -> list[dict[str, str]]:
    """Findings after the migration that were not there before, minus declared exemptions.

    Compared as a multiset of (code, file, message): line numbers move under
    an edit, and a count alone would hide one fixed finding plus one new one.
    ``lint["exempt"]`` is the contract's ``expected_lint``.
    """
    if lint.get("pre") is None or lint.get("post") is None:
        return []
    before = Counter((f["code"], f["file"], f["message"]) for f in lint["pre"])
    new = []
    for finding in lint["post"]:
        key = (finding["code"], finding["file"], finding["message"])
        if before[key]:
            before[key] -= 1
        elif finding["code"] not in set(lint.get("exempt") or []):
            new.append(finding)
    return new


def exempted_lint(lint: dict[str, Any]) -> list[dict[str, str]]:
    """Post-migration findings waived by the contract's ``expected_lint``."""
    exempt = set(lint.get("exempt") or [])
    return [f for f in lint.get("post") or [] if f["code"] in exempt]


def _red(a: dict[str, Any]) -> list[dict[str, str]]:
    reasons = []
    pre, post, metrics = a.get("pre_report"), a.get("post_report"), a.get("metrics")

    if a.get("crash"):
        reasons.append(_reason("RED", "crashed", "The run crashed before it finished.",
                               a["crash"].strip().splitlines()[0],
                               "Read the traceback in run_meta.json, fix the cause, re-run."))
    elif metrics is None:
        reasons.append(_reason("RED", "crashed", "The run left no metrics.json.",
                               "metrics.json missing", "Re-run; inspect the run directory."))

    if pre is not None and (pre.get("total", 0) == 0 or pre.get("failed", 0)
                            or pre.get("errors", 0)):
        reasons.append(_reason(
            "RED", "precondition",
            "The pre-migration suite was not green, so M2 is undefined (NB-10).",
            f"test_report_pre.json: {pre.get('passed', 0)}/{pre.get('total', 0)} passed, "
            f"{pre.get('failed', 0)} failed, {pre.get('errors', 0)} errors",
            "Make the original suite pass (and collect at least one test) before migrating."))

    if metrics is not None and metrics.get("outcome") == "gave_up":
        reasons.append(_reason(
            "RED", "gave_up", "The agent gave up: a failure outlived MAX_FIX_ATTEMPTS.",
            "metrics.json: outcome=gave_up",
            "Fix the blocked failures by hand; the timeline lists every attempt."))

    if post is None and not a.get("crash"):
        reasons.append(_reason(
            "RED", "suite_red", "There is no final test-suite result to judge the patch by.",
            "test_report.json missing or pre-migration only",
            "Re-run the migration; a run that never tested its result cannot pass."))
    if post is not None and (post.get("failed", 0) or post.get("errors", 0)):
        ids = [f.get("nodeid", "?") for f in post.get("failures", [])]
        reasons.append(_reason(
            "RED", "suite_red",
            "The final suite has failed, errored or uncollectable tests.",
            f"test_report.json: {post.get('failed', 0)} failed, {post.get('errors', 0)} "
            f"errors — {_listing(ids)}",
            "Fix the listed tests' failures in the migrated code (never in the tests)."))

    tampered = sorted({*a.get("tamper", []), *a.get("rejected_tamper", [])})
    if tampered:
        reasons.append(_reason(
            "RED", "tamper", "A change to the test oracle was detected (NB-4).",
            _listing(tampered),
            "Audit the patch and the CORRECT attempts; tests must not be edited."))

    check = a.get("apply_check")
    if check is not None and not check.get("ok"):
        reasons.append(_reason(
            "RED", "apply_check", "migration.patch does not apply to a fresh checkout.",
            f"git apply --check: {check.get('detail', '')}",
            "Regenerate the patch from the run's repo before using it."))

    budget, tokens = a.get("token_budget"), (metrics or {}).get("m3_tokens", 0)
    if budget and tokens > budget:
        reasons.append(_reason(
            "RED", "token_budget", "The run spent more tokens than its budget.",
            f"{tokens} tokens > MRA_TOKEN_BUDGET={budget}",
            "Raise the budget deliberately or reduce LLM use (cheaper role chain)."))
    limit, wall = a.get("run_timeout_s"), a.get("wall_clock_s") or 0
    if limit and wall > limit:
        reasons.append(_reason(
            "RED", "timeout", "The run took longer than its wall-clock limit.",
            f"{wall:.0f}s > MRA_RUN_TIMEOUT_SEC={limit}",
            "Investigate the slow step in the timeline; raise the limit only deliberately."))
    return reasons


def _yellow(a: dict[str, Any]) -> list[dict[str, str]]:
    reasons = []
    residual = a.get("residual") or {}
    left = [f"{s['file']}:{s['line']}" for s in residual.get("sites", [])]
    left += [f"{s['file']}:{s['line']} ({s['kind']})" for s in residual.get("skipped", [])]
    if left:
        reasons.append(_reason(
            "YELLOW", "residual", "Sites of the old API remain in the migrated tree.",
            f"{len(left)} site(s): {_listing(left)}",
            "Migrate the remaining sites by hand; star imports and bare references "
            "are skipped by design."))

    metrics = a.get("metrics") or {}
    if a.get("has_ground_truth") and metrics.get("m1_precision", 100.0) < 100.0:
        reasons.append(_reason(
            "YELLOW", "precision", "The agent edited sites outside the ground truth.",
            f"M1 precision {metrics['m1_precision']:.1f}%",
            "Review the over-edited sites in the Changes section and revert any that are wrong."))

    failed = [f"{c['file']}: {c['detail']}" for c in a.get("semantic", []) if not c["passed"]]
    if failed:
        reasons.append(_reason(
            "YELLOW", "semantic", "A semantic check failed.", _listing(failed, 3),
            "Inspect the named file: the code runs but may not mean what the target API means."))

    new = new_lint(a.get("lint") or {})
    if new:
        reasons.append(_reason(
            "YELLOW", "lint", "The migration introduced new ruff errors.",
            _listing([f"{f['code']} {f['file']}" for f in new], 4),
            "Run `ruff check` on the migrated tree and fix the new findings."))

    unparseable = residual.get("unparseable", [])
    if unparseable:
        reasons.append(_reason(
            "YELLOW", "unparseable", "Files were skipped because they could not be parsed.",
            _listing(unparseable), "Check those files by hand; the agent never saw them."))

    coverage = a.get("coverage") or {}
    if coverage.get("available"):
        cold = [f"{file}: 0/{len(c['changed'])} changed lines run"
                for file, c in sorted(coverage.get("files", {}).items())
                if c["changed"] and not set(c["changed"]) & set(c["executed"])]
        if cold:
            reasons.append(_reason(
                "YELLOW", "unexecuted",
                "An edited file's changes were not executed by any test.",
                _listing(cold, 3),
                "Add a test that exercises the change; a green suite that never runs it "
                "is weak evidence."))
    elif any(file for file in coverage.get("files", {})) or coverage.get("error"):
        reasons.append(_reason(
            "YELLOW", "unexecuted", "Coverage of the edited files could not be measured.",
            coverage.get("error", "coverage.json missing"),
            "Fix the sandbox and re-run the migration, or check coverage by hand."))
    return reasons


def verdict(run_artifacts: dict[str, Any]) -> dict[str, Any]:
    """``{status, reasons}`` with RED > YELLOW > GREEN; see the module docstring."""
    red, yellow = _red(run_artifacts), _yellow(run_artifacts)
    status = "RED" if red else "YELLOW" if yellow else "GREEN"
    return {"status": status, "reasons": red + yellow}


def headline(result: dict[str, Any]) -> str:
    """The one-line reason under the banner."""
    if result["reasons"]:
        first = result["reasons"][0]["text"]
        more = len(result["reasons"]) - 1
        return first + (f" (+{more} more issue{'s' * (more > 1)})" if more else "")
    return "Suite green, no residual sites, every edited file exercised by a test."
