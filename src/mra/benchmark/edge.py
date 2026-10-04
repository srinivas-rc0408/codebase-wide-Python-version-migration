"""Edge-case accuracy suite: ``python -m mra.benchmark.edge``.

Runs every case under ``corpus/edge/`` through the full agent and report
(``run_with_report``) and checks the *verdict*, not just "green": the status,
the reason code that produced it, a word the reason's evidence must contain,
and — for byte-level cases — that the migrated file equals ``gold/`` exactly.

Fully offline. LLM cases use :class:`FakeProvider` (answers from the codemod),
a dead localhost port (unreachable provider), or a remote URL under
``MRA_PRIVACY=local-only`` (refused before any I/O). Each case runs in its own
process, because cases set environment variables (timeouts, privacy).

Writes ``corpus/edge/RESULTS.md`` and ``results.json``; the latter is what a
run report's verification table cites.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import tempfile
from concurrent.futures import ProcessPoolExecutor
from datetime import UTC, datetime
from multiprocessing import get_context
from pathlib import Path
from typing import Any

from mra import __version__

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EDGE = ROOT / "corpus" / "edge"
DEFAULT_RUNS = ROOT / "runs" / "edge"
ORDER = {"common": 0, "rare": 1, "twisted": 2, "failure": 3}


def cases(edge: Path = DEFAULT_EDGE) -> list[Path]:
    found = [p.parent for p in edge.glob("*/case.json")]
    return sorted(
        found, key=lambda p: (ORDER[json.loads((p / "case.json").read_text())["category"]], p.name)
    )


# -- LLM set-ups ------------------------------------------------------------


def _fake_reply(messages: list[dict[str, str]], model: str) -> str:
    """Classify, summarise, or return the codemod's version of the file it was shown."""
    import libcst as cst
    from libcst.codemod import CodemodContext

    from mra.codemods.datetime_utcnow import ConvertUtcnowCommand

    system, user = messages[0]["content"], messages[-1]["content"]
    if "one word" in system:
        return "behaviour"
    if "progress note" in system:
        return "Earlier batches migrated; one cross-module break outstanding."
    source = user.split("```python\n", 1)[1].rsplit("```", 1)[0]
    module = ConvertUtcnowCommand(CodemodContext()).transform_module(cst.parse_module(source))
    return f"```python\n{module.code}```"


def _dead_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def _llm_setup(mode: str, task_dir: Path) -> Any:
    def setup(run_id: str) -> dict[str, Any]:
        from mra.codemods.datetime_utcnow import TARGET
        from mra.models import ROLES, Endpoint, Router
        from mra.models.providers import FakeProvider, OpenAICompatibleProvider
        from mra.nodes.correct_node import LLMCorrector
        from mra.state import new_state

        if mode == "llm-fake":
            provider: Any = FakeProvider("fake-llm", reply=_fake_reply)
        elif mode == "llm-unreachable":
            provider = OpenAICompatibleProvider(
                name="local-dead", base_url=f"http://127.0.0.1:{_dead_port()}/v1", timeout_s=2
            )
        else:  # llm-remote: a key is "set", the host is remote
            os.environ["EDGE_DUMMY_KEY"] = "not-a-real-key"
            provider = OpenAICompatibleProvider(
                name="deepseek", base_url="https://api.deepseek.com", api_key_env="EDGE_DUMMY_KEY"
            )
        truth = json.loads((task_dir / "ground_truth.json").read_text())
        contract = {
            "task_id": task_dir.name,
            "source_api": truth["source_api"],
            "target_api": truth["target_api"],
        }
        state = new_state(run_id, "", contract)
        router = Router(
            state["tokens"], roles={role: [Endpoint(provider, "edge-model")] for role in ROLES}
        )
        return {
            "router": router,
            "state": state,
            "corrector": LLMCorrector(router, TARGET, contract),
        }

    return setup


def _live_setup(task_dir: Path, store: str | None) -> Any:
    """The real router from ``mra.toml`` as corrector; ``store`` = a frozen experience db."""

    def setup(run_id: str) -> dict[str, Any]:
        from mra.codemods.datetime_utcnow import TARGET
        from mra.memory.experience import ExperienceStore
        from mra.models import Router, load_roles
        from mra.nodes.correct_node import LLMCorrector
        from mra.state import new_state

        truth = json.loads((task_dir / "ground_truth.json").read_text())
        contract = {
            "task_id": task_dir.name,
            "source_api": truth["source_api"],
            "target_api": truth["target_api"],
        }
        state = new_state(run_id, "", contract)
        router = Router(state["tokens"], roles=load_roles())
        memory = None if store is None else ExperienceStore(store, readonly=True)
        return {
            "router": router,
            "state": state,
            "corrector": LLMCorrector(router, TARGET, contract, memory),
        }

    return setup


def held_out(edge: Path = DEFAULT_EDGE) -> list[Path]:
    """Cases outside ablation E's training split: the only ones a warmed store may score."""
    from mra.benchmark.runner import train_tasks

    train = {t.name for t in train_tasks(edge)}
    return [c for c in cases(edge) if c.name not in train]


# -- one case ---------------------------------------------------------------


def _relative(path: Path) -> str:
    path = Path(path).resolve()
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.name


def run_case(
    task_dir: Path | str,
    runs_dir: Path | str,
    live: bool = False,
    store: str | None = None,
    repeat: int = 0,
    rules: list[dict[str, Any]] | tuple = (),
) -> dict[str, Any]:
    """Run one case and judge it. Runs in a fresh process (see the module docstring).

    ``live`` swaps the codemod corrector for the real model on deterministic
    cases; the ``llm-*`` cases keep their provider set-up, since the provider
    failure is what they test.
    """
    from mra.benchmark.runner import _failures, codemod_corrector
    from mra.report import run_with_report

    task_dir = Path(task_dir)
    spec = json.loads((task_dir / "case.json").read_text())
    os.environ.update(spec["env"])
    if spec["mode"] != "deterministic":
        setup = _llm_setup(spec["mode"], task_dir)
    else:
        setup = _live_setup(task_dir, store) if live else None
    run_id = task_dir.name if not repeat else f"{task_dir.name}-r{repeat}"
    result = run_with_report(
        task_dir,
        run_id=run_id,
        runs_dir=runs_dir,
        corrector=codemod_corrector,
        setup=setup,
        rules=rules,
    )
    model = result["model"]
    actual = model["verdict"]["status"]
    reasons = model["verdict"]["reasons"]
    problems = []
    if actual != spec["expect"]:
        problems.append(f"verdict {actual}, expected {spec['expect']}")
    if spec["code"]:
        matching = [r for r in reasons if r["code"] == spec["code"]]
        if not matching:
            problems.append(f"no `{spec['code']}` reason")
        elif spec["evidence"] and not any(
            spec["evidence"].lower() in f"{r['text']} {r['evidence']}".lower() for r in matching
        ):
            problems.append(f"`{spec['code']}` reason does not mention '{spec['evidence']}'")
    if spec["code"] in ("precondition", "refused") and model["changes"]:
        problems.append(f"refused, yet edited {len(model['changes'])} file(s)")
    recall = (model["metrics"] or {}).get("m1_recall")
    truth = json.loads((task_dir / "ground_truth.json").read_text())["call_sites"]
    if spec["expect"] != "RED" and truth and recall != 100.0:
        # A verdict that is right for the wrong reason: a missed site no check noticed.
        problems.append(f"M1 recall {recall} — a ground-truth site was not migrated")
    for rel in spec["gold"]:
        produced = result["out_dir"] / "repo" / rel
        expected = (task_dir / "gold" / rel).read_bytes()
        if not produced.is_file() or produced.read_bytes() != expected:
            problems.append(f"{rel} is not byte-identical to gold/")
    metrics = model["metrics"] or {}
    out = result["out_dir"]
    trajectory = _json_or(out / "trajectory.json", [])
    return {
        "case": task_dir.name,
        "category": spec["category"],
        "repeat": repeat,
        "expected": spec["expect"],
        "actual": actual,
        "pass": not problems,
        "problems": problems,
        "reasons": [f"{r['level']} {r['code']}: {r['evidence']}" for r in reasons],
        # Relative: results.json is committed, and an absolute path names the machine.
        "note": spec["note"],
        "pdf": _relative(result["pdf"]),
        "m1_recall": metrics.get("m1_recall"),
        "m2_pass_rate": metrics.get("m2_pass_rate"),
        "corrections": sum(1 for e in trajectory if e.get("node") == "CORRECT"),
        "tokens": metrics.get("m3_tokens", 0),
        "cost_usd": metrics.get("m3_cost_usd", 0.0),
        "failure_classes": sorted(
            {f["failure_class"] for f in _failures(_json_or(out / "test_report.json", {}))}
        ),
    }


def _json_or(path: Path, default: Any) -> Any:
    return json.loads(path.read_text()) if path.is_file() else default


def _judge(
    task_dir: Path,
    runs_dir: Path,
    live: bool = False,
    store: str | None = None,
    repeat: int = 0,
    rules: list[dict[str, Any]] | tuple = (),
) -> dict[str, Any]:
    """``run_case``, but an exception escaping the agent *and* its report is a failed row."""
    try:
        return run_case(task_dir, runs_dir, live, store, repeat, rules)
    except Exception as exc:
        spec = json.loads((task_dir / "case.json").read_text())
        return {
            "case": task_dir.name,
            "category": spec["category"],
            "repeat": repeat,
            "expected": spec["expect"],
            "actual": "NO REPORT",
            "pass": False,
            "problems": [f"no report: {type(exc).__name__}: {exc}"[:300]],
            "reasons": [],
            "note": spec["note"],
            "pdf": "",
        }


def run_suite(
    edge: Path = DEFAULT_EDGE,
    runs_dir: Path = DEFAULT_RUNS,
    only: list[str] | None = None,
    workers: int = 6,
    live: bool = False,
    memory: bool = False,
    repeats: int = 1,
    rules: list[dict[str, Any]] | tuple = (),
) -> dict[str, Any]:
    """Judge every case ``repeats`` times.

    ``memory`` (live only) warms an experience store on the training split
    (:func:`mra.benchmark.runner.train_tasks`), freezes it, and evaluates only
    the cases *outside* that split: scoring a case the store learnt from is leakage.
    """
    selected = [c for c in cases(edge) if not only or c.name in only]
    store = None
    warmup: dict[str, Any] = {}
    scratch = None
    if memory:
        from mra.benchmark.runner import train_tasks, warm_store
        from mra.memory.experience import ExperienceStore

        train = train_tasks(edge)
        scratch = Path(tempfile.mkdtemp(prefix="mra-edge-memory-"))
        warmup = warm_store(ExperienceStore(scratch / "experience.db"), train, scratch / "runs")
        store = str(scratch / "experience.db")
        selected = [c for c in selected if c in held_out(edge)]
    jobs = [(case, r) for case in selected for r in range(repeats)]
    try:
        # One process per case (max_tasks_per_child=1): no env var leaks between cases.
        with ProcessPoolExecutor(
            max_workers=workers, mp_context=get_context("spawn"), max_tasks_per_child=1
        ) as pool:
            rows = list(
                pool.map(
                    _judge,
                    [case for case, _ in jobs],
                    [runs_dir] * len(jobs),
                    [live] * len(jobs),
                    [store] * len(jobs),
                    [r for _, r in jobs],
                    [rules] * len(jobs),
                )
            )
    finally:
        if scratch is not None:
            shutil.rmtree(scratch, ignore_errors=True)
    return {
        "agent_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "live": live,
        "repeats": repeats,
        "experience_warmup": warmup,
        "passed": sum(r["pass"] for r in rows),
        "total": len(rows),
        "cases": rows,
    }


def render(results: dict[str, Any]) -> str:
    lines = [
        "# Edge-case accuracy suite",
        "",
        f"Agent {results['agent_version']} · generated {results['generated_at']} · "
        f"**{results['passed']}/{results['total']} cases give the expected verdict.**",
        "",
        "Each case asserts the verdict, the reason that produced it, and (for byte-level "
        "cases) a byte-exact match with `gold/`. Regenerate with "
        "`python -m mra.benchmark.edge`; fixtures come from `corpus/edge/_build.py`.",
        "",
        "| case | category | expected verdict | actual | pass | reason / note |",
        "|---|---|---|---|---|---|",
    ]
    live = results.get("live", False)
    if live:
        lines[-2:] = [
            "Live: the corrector is the real model from `mra.toml` "
            f"({results['repeats']} repeat(s) per case).",
            "",
            "| case | rep | expected | actual | pass | M1 | M2 | corr | tokens | cost $ "
            "| failure class | reason / note |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]
    for row in results["cases"]:
        detail = "; ".join(row["problems"]) or "; ".join(row["reasons"]) or row["note"] or "—"
        detail = re.sub(r"\s+", " ", detail).replace("|", "\\|")
        verdict = f"{row['expected']} | {row['actual']} | {'yes' if row['pass'] else '**NO**'}"
        if live:
            lines.append(
                f"| `{row['case']}` | {row['repeat']} | {verdict} | {row.get('m1_recall')} | "
                f"{row.get('m2_pass_rate')} | {row.get('corrections', 0)} | "
                f"{row.get('tokens', 0)} | {row.get('cost_usd', 0.0):.4f} | "
                f"{', '.join(row.get('failure_classes', [])) or '—'} | {detail} |"
            )
        else:
            lines.append(f"| `{row['case']}` | {row['category']} | {verdict} | {detail} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the edge-case accuracy suite.")
    parser.add_argument("--edge", default=str(DEFAULT_EDGE))
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS))
    parser.add_argument(
        "--out", default=None, help="where RESULTS.md/results.json go (default: the edge directory)"
    )
    parser.add_argument("--cases", nargs="*", default=None)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--live", action="store_true", help="real model as corrector (mra.toml)")
    parser.add_argument(
        "--memory", action="store_true", help="with --live: warmed store, held-out cases only"
    )
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument(
        "--stem",
        default=None,
        help="write <stem>.json/<stem>.md instead of results.json/RESULTS.md",
    )
    args = parser.parse_args(argv)
    if args.memory and not args.live:
        parser.error("--memory needs --live")
    results = run_suite(
        Path(args.edge),
        Path(args.runs_dir),
        args.cases,
        args.workers,
        live=args.live,
        memory=args.memory,
        repeats=args.repeats,
    )
    out = Path(args.out or args.edge)
    out.mkdir(parents=True, exist_ok=True)
    json_name, md_name = (
        ("results.json", "RESULTS.md")
        if args.stem is None
        else (f"{args.stem}.json", f"{args.stem}.md")
    )
    (out / json_name).write_text(json.dumps(results, indent=2) + "\n")
    (out / md_name).write_text(render(results))
    print(
        f"{results['passed']}/{results['total']} cases give the expected verdict -> {out / md_name}"
    )
    for row in results["cases"]:
        if not row["pass"]:
            print(f"  MISMATCH {row['case']}: {'; '.join(row['problems'])}")
    return 0 if results["passed"] == results["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
