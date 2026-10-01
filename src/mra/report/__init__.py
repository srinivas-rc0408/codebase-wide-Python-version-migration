"""The run report: verdict banner, 14-page PDF, report.json, terminal summary.

``run_with_report`` wraps :func:`mra.graph.run_migration`; the report is built
in a ``finally`` block so a RED or crashed run still gets one. ``build_report``
rebuilds it from the run directory alone (``mra report <run_id>``).
"""

from __future__ import annotations

import json
import os
import re
import time
import traceback
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mra import __version__
from mra.codemods.datetime_utcnow import TARGET
from mra.report import evidence
from mra.report.model import build_model, load_run
from mra.report.pdf import render

ANSI = {"GREEN": "\033[1;97;42m", "YELLOW": "\033[1;30;43m", "RED": "\033[1;97;41m"}
RESET = "\033[0m"


def sanitize(name: str) -> str:
    """A repo name that is safe in a filename on every OS."""
    return re.sub(r"[^A-Za-z0-9_-]+", "_", name).strip("_") or "repo"


def report_filename(repo_name: str, when: datetime) -> str:
    return f"{sanitize(repo_name)}_MigrationReport_v{__version__}_{when:%Y%m%d-%H%M}.pdf"


def build_report(out_dir: Path | str) -> tuple[Path, dict[str, Any]]:
    """Render the PDF and report.json from the run directory. Returns (pdf path, model)."""
    out_dir = Path(out_dir).resolve()
    model = build_model(load_run(out_dir))
    now = datetime.now().astimezone()
    data, pages, cuts = render(model, generated=now.strftime("%Y-%m-%d %H:%M %Z"))
    model["pdf"] = {"pages": pages, "truncation": cuts}
    (out_dir / "report.json").write_text(json.dumps(model, indent=2, default=str) + "\n")
    path = out_dir / report_filename(model["meta"].get("repo_name") or out_dir.name, now)
    path.write_bytes(data)
    return path, model


def run_with_report(task_dir: Path | str, *, run_id: str | None = None,
                    runs_dir: Path | str = "runs", router: Any = None,
                    **run_kwargs: Any) -> dict[str, Any]:
    """Run the migration, then always gather evidence and write the report."""
    from mra.graph import run_migration

    task_dir = Path(task_dir)
    run_id = run_id or uuid.uuid4().hex[:12]
    out_dir = Path(runs_dir) / run_id
    truth_path = task_dir / "ground_truth.json"
    truth = json.loads(truth_path.read_text()) if truth_path.is_file() else {}
    started, clock = datetime.now(UTC), time.perf_counter()
    crash = crash_summary = None
    try:
        run_migration(task_dir, run_id=run_id, runs_dir=runs_dir, router=router, **run_kwargs)
    except Exception as exc:
        crash, crash_summary = traceback.format_exc(), f"{type(exc).__name__}: {exc}"
    finally:
        out_dir.mkdir(parents=True, exist_ok=True)
        meta = {
            "run_id": run_id, "task_id": task_dir.name, "repo_name": task_dir.name,
            "agent_version": __version__, "target": run_kwargs.get("target", TARGET),
            "source_api": truth.get("source_api"), "target_api": truth.get("target_api"),
            "has_ground_truth": bool(truth.get("call_sites") is not None),
            "started_at": started.isoformat(timespec="seconds"),
            "wall_clock_s": round(time.perf_counter() - clock, 3),
            "token_budget": int(os.getenv("MRA_TOKEN_BUDGET", "2000000")),
            "run_timeout_s": int(os.getenv("MRA_RUN_TIMEOUT_SEC", "1800")),
            "crash": crash,
            "crash_summary": crash_summary,
            "llm": {
                "calls": getattr(router, "calls", []),
                "egress": getattr(router, "egress", {}),
                "privacy": getattr(router, "privacy", os.getenv("MRA_PRIVACY", "")),
            },
        }
        (out_dir / "run_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
        evidence.collect(out_dir, meta["target"], task_dir.name, run_id)
        pdf, model = build_report(out_dir)
    return {"run_id": run_id, "out_dir": out_dir, "pdf": pdf, "model": model,
            "crashed": crash is not None}


def terminal_summary(model: dict[str, Any], pdf: Path, *, color: bool | None = None) -> str:
    """The verdict banner, key metrics, reasons and PDF path, for a terminal."""
    color = not os.getenv("NO_COLOR") if color is None else color
    status = model["verdict"]["status"]
    tag = f" {status} "
    tag = f"{ANSI[status]}{tag}{RESET}" if color else f"[{status}]"
    meta, m = model["meta"], model["metrics"]
    lines = [f"{tag} {meta.get('repo_name')}  {meta.get('source_api')} -> "
             f"{meta.get('target_api')}  (run {meta.get('run_id')})",
             f"  {model['headline']}"]
    if m:
        lines.append(f"  M1 recall {m['m1_recall']:.1f}%  precision {m['m1_precision']:.1f}%   "
                     f"M2 {m['m2_pass_rate']:.1f}% ({m['m2_regressions']} regressions)   "
                     f"M3 {m['m3_tokens']:,} tokens, {m['m3_steps']} steps")
    lines.append(f"  Data egress: {model['llm']['egress_line']}")
    for reason in model["verdict"]["reasons"]:
        lines.append(f"  - {reason['level']}: {reason['text']} [{reason['evidence']}]")
    lines.append(f"  Report: {Path(pdf).resolve()}")
    return "\n".join(lines)


__all__ = ["build_report", "report_filename", "run_with_report", "sanitize",
           "terminal_summary"]
