"""Opt-in experience store: past corrective fixes, offered as hints to CORRECT.

OFF by default. On only when ``mra.toml`` has ``[experience] enabled = true``
or ``MRA_EXPERIENCE=on`` (``MRA_EXPERIENCE=off`` always wins). Only ``mra run``
reads that switch: the benchmark and edge runners never call :func:`from_config`,
so the user's store is never read or written by them, whatever the config
says. Ablation E builds its own throwaway store in a temp directory.

* **Where:** a local SQLite file, ``~/.mra/experience.db`` unless configured
  (``[experience] path`` or ``MRA_EXPERIENCE_DB``). A path inside the agent's
  own repository or the repository being migrated is refused. Nothing here
  does network I/O.
* **When:** only from a run whose verdict is fully GREEN (:func:`fully_green`:
  verdict GREEN, no residual sites, the whole final suite green). A fix that
  turned the suite green but left old-API sites behind is never stored — that
  is the poisoning case. Each storing run is kept as provenance (its run id and
  a hash of the task name, never the name), and a fix none of whose runs falls
  within ``ttl_days`` is expired: no hints, no skill candidate.
* **What:** after a CORRECT whose re-test is green — failure class, the
  normalised error message, the contract (source -> target), and the fix as
  a minimal diff pattern (changed lines only, no file headers). File paths are
  stripped from messages, and everything is secret-redacted before it is
  written.
* **How it is used:** on a new failure, the top-k fixes with the same failure
  class and contract, ranked by string similarity of the normalised message,
  are rendered as hints into the CORRECT prompt within ``HINT_BUDGET_CHARS``.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from datetime import UTC, datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from mra.models.privacy import redact_secrets
from mra.sandbox.runner import _ABS_PATH, normalize_message

DEFAULT_PATH = Path("~/.mra/experience.db")
#: ~300 tokens of hints at most: memory must not crowd out the file being fixed.
HINT_BUDGET_CHARS = 1200
PATTERN_MAX_LINES = 24
TOP_K = 3
DEFAULT_TTL_DAYS = 90

_FILE = re.compile(r"[\w.\-\\/]*\.py\b")
_QUOTED_PATH = re.compile(r"""['"][^'"]*[\\/][^'"]*['"]""")
AGENT_ROOT = Path(__file__).resolve().parents[3]

SCHEMA = """
CREATE TABLE IF NOT EXISTS fixes (
    id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL,
    failure_class TEXT NOT NULL,
    message TEXT NOT NULL,
    source_api TEXT NOT NULL,
    target_api TEXT NOT NULL,
    pattern TEXT NOT NULL,
    UNIQUE (failure_class, message, source_api, target_api, pattern)
);
CREATE TABLE IF NOT EXISTS observations (
    fix_id INTEGER NOT NULL REFERENCES fixes (id),
    run_id TEXT NOT NULL,
    task_key TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE (fix_id, run_id)
);
CREATE TABLE IF NOT EXISTS skills (
    id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    failure_class TEXT NOT NULL,
    source_api TEXT NOT NULL,
    target_api TEXT NOT NULL,
    rule TEXT NOT NULL,
    evidence TEXT NOT NULL,
    validation TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def task_key(task_id: str) -> str:
    """Distinct tasks are countable; the task's name is not stored."""
    return hashlib.sha256(task_id.encode()).hexdigest()[:12]


def fully_green(model: dict[str, Any]) -> bool:
    """A run report the store may learn from: GREEN, no residual sites, suite green."""
    residual = (model.get("verification") or {}).get("residual") or {}
    post = (model.get("verification") or {}).get("post") or {}
    return (
        (model.get("verdict") or {}).get("status") == "GREEN"
        and not residual.get("sites")
        and not residual.get("skipped")
        and bool(post.get("total"))
        and not post.get("failed")
        and not post.get("errors")
    )


def clean_message(message: str) -> str:
    """Normalised, path-free, secret-free: nothing that identifies a repo or a run."""
    text = _QUOTED_PATH.sub("'<path>'", message)
    text = _FILE.sub("<file>", normalize_message(text))
    return redact_secrets(text)[0][:500]


def diff_pattern(diff: str) -> str:
    """A ``git diff`` -> its changed lines only: no headers, hunks or paths."""
    lines = [
        line
        for line in diff.splitlines()
        if line[:1] in "+-" and not line.startswith(("+++", "---"))
    ]
    text = _QUOTED_PATH.sub("'<path>'", "\n".join(lines[:PATTERN_MAX_LINES]))
    return redact_secrets(_ABS_PATH.sub("<path>/", text))[0]


def format_hint(fix: dict[str, Any]) -> str:
    return f"when `{fix['message']}`, this fixed it:\n{fix['pattern']}"


class ExperienceStore:
    """One SQLite file of past fixes. ``readonly`` serves hints but learns nothing."""

    def __init__(
        self,
        path: Path | str,
        *,
        readonly: bool = False,
        forbidden: tuple[Path, ...] = (),
        ttl_days: int = DEFAULT_TTL_DAYS,
    ) -> None:
        self.path = Path(path).expanduser().resolve()
        for root in (AGENT_ROOT, *forbidden):
            if self.path.is_relative_to(Path(root).resolve()):
                raise ValueError(
                    f"experience store {self.path} is inside {root}; it must "
                    "live outside every repository (default ~/.mra/)"
                )
        self.readonly = readonly
        self.ttl_days = ttl_days

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.executescript(SCHEMA)
        return connection

    def _cutoff(self) -> str:
        return (datetime.now(UTC) - timedelta(days=self.ttl_days)).isoformat(timespec="seconds")

    def record(
        self,
        failure_class: str,
        message: str,
        contract: dict[str, Any],
        diff: str,
        *,
        run_id: str = "",
        task_id: str = "",
    ) -> bool:
        """Store one fix (and the run that produced it); False when read-only, empty, or known."""
        pattern = diff_pattern(diff)
        if self.readonly or not pattern:
            return False
        now = datetime.now(UTC).isoformat(timespec="seconds")
        key = (
            failure_class,
            clean_message(message),
            str(contract.get("source_api", "")),
            str(contract.get("target_api", "")),
            pattern,
        )
        with self._connect() as db:
            cursor = db.execute(
                "INSERT OR IGNORE INTO fixes (created_at, failure_class, message, source_api,"
                " target_api, pattern) VALUES (?, ?, ?, ?, ?, ?)",
                (now, *key),
            )
            new = cursor.rowcount == 1
            if run_id:
                (fix_id,) = db.execute(
                    "SELECT id FROM fixes WHERE failure_class = ? AND message = ? AND "
                    "source_api = ? AND target_api = ? AND pattern = ?",
                    key,
                ).fetchone()
                db.execute(
                    "INSERT OR IGNORE INTO observations VALUES (?, ?, ?, ?)",
                    (fix_id, run_id, task_key(task_id), now),
                )
            return new

    def similar(
        self, failure_class: str, message: str, contract: dict[str, Any], k: int = TOP_K
    ) -> list[dict[str, Any]]:
        """Same class and contract, ranked by similarity of the normalised message."""
        if not self.path.is_file():
            return []
        with self._connect() as db:
            rows = db.execute(
                "SELECT id, message, pattern FROM fixes WHERE failure_class = ? AND "
                "source_api = ? AND target_api = ? AND (created_at >= ? OR id IN "
                "(SELECT fix_id FROM observations WHERE created_at >= ?))",
                (
                    failure_class,
                    str(contract.get("source_api", "")),
                    str(contract.get("target_api", "")),
                    self._cutoff(),
                    self._cutoff(),
                ),
            ).fetchall()
        wanted = clean_message(message)
        scored = sorted(
            (
                (SequenceMatcher(None, wanted, text).ratio(), row_id, text, pattern)
                for row_id, text, pattern in rows
            ),
            key=lambda r: (-r[0], r[1]),
        )
        return [
            {"id": row_id, "similarity": round(score, 3), "message": text, "pattern": pattern}
            for score, row_id, text, pattern in scored[:k]
        ]

    def hints(
        self, failure_class: str, message: str, contract: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """The top-k fixes whose :func:`format_hint` text fits :data:`HINT_BUDGET_CHARS`."""
        hints, used = [], 0
        for fix in self.similar(failure_class, message, contract):
            used += len(format_hint(fix))
            if used > HINT_BUDGET_CHARS:
                break
            hints.append(fix)
        return hints

    def learn(
        self,
        repo: Path | str,
        trajectory: list[dict[str, Any]],
        contract: dict[str, Any],
        model: dict[str, Any],
    ) -> int:
        """Record every CORRECT whose very next TEST was green; returns how many were new.

        ``model`` is the run's report model (``report.json``); nothing at all is
        learnt unless it is :func:`fully_green`. The fix is the diff of that
        correction's own commit (``sha~1..sha``: CORRECT snapshots immediately
        before and after the corrector runs).
        """
        from git import Repo

        if not fully_green(model):
            return 0
        meta = model.get("meta") or {}
        learned = 0
        for event, after in zip(trajectory, trajectory[1:], strict=False):
            detail, verdict = event["detail"], after["detail"]
            if (
                event["node"] != "CORRECT"
                or after["node"] != "TEST"
                or not detail.get("sha")
                or verdict.get("failed", 1)
                or verdict.get("errors", 1)
            ):
                continue
            diff = Repo(repo).git.diff(f"{detail['sha']}~1", detail["sha"])
            learned += self.record(
                detail.get("failure_class", ""),
                detail.get("message", ""),
                contract,
                diff,
                run_id=str(meta.get("run_id") or ""),
                task_id=str(meta.get("task_id") or ""),
            )
        return learned

    # -- skill promotion (mra.skills) --------------------------------------

    def candidates(self, min_tasks: int | None = None) -> list[dict[str, Any]]:
        """Fixes reducible to one codemod rule, seen working on >= ``min_tasks`` tasks.

        Grouped by (failure class, contract, rule): the same rewrite learnt from
        different files is one candidate. Only unexpired observations count, and
        a rule already promoted or revoked is never offered again.
        """
        from mra.skills import MIN_INDEPENDENT_TASKS, derive_rule, skill_id

        minimum = MIN_INDEPENDENT_TASKS if min_tasks is None else min_tasks
        if not self.path.is_file():
            return []
        with self._connect() as db:
            rows = db.execute(
                "SELECT f.id, f.failure_class, f.source_api, f.target_api, f.pattern, "
                "o.run_id, o.task_key FROM fixes f JOIN observations o ON o.fix_id = f.id "
                "WHERE o.created_at >= ? ORDER BY f.id, o.run_id",
                (self._cutoff(),),
            ).fetchall()
            decided = {row[0] for row in db.execute("SELECT id FROM skills")}
        groups: dict[str, dict[str, Any]] = {}
        for fix_id, klass, source, target, pattern, run_id, key in rows:
            rule = derive_rule(pattern)
            if rule is None:
                continue
            ident = skill_id(klass, source, target, rule)
            group = groups.setdefault(
                ident,
                {
                    "id": ident,
                    "failure_class": klass,
                    "source_api": source,
                    "target_api": target,
                    "rule": rule,
                    "runs": set(),
                    "tasks": set(),
                    "fixes": set(),
                    "patterns": [],
                },
            )
            group["runs"].add(run_id)
            group["tasks"].add(key)
            group["fixes"].add(fix_id)
            if pattern not in group["patterns"]:
                group["patterns"].append(pattern)
        return [
            {
                **g,
                "runs": sorted(g["runs"]),
                "tasks": len(g["tasks"]),
                "fixes": sorted(g["fixes"]),
            }
            for ident, g in sorted(groups.items())
            if len(g["tasks"]) >= minimum and ident not in decided
        ]

    def _decide(self, skill: dict[str, Any], status: str, validation: dict[str, Any]) -> None:
        if self.readonly:
            raise PermissionError("read-only experience store")
        evidence = {k: skill.get(k) for k in ("runs", "tasks", "fixes", "patterns")}
        with self._connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO skills VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    skill["id"],
                    status,
                    skill["failure_class"],
                    skill["source_api"],
                    skill["target_api"],
                    json.dumps(skill["rule"]),
                    json.dumps(evidence),
                    json.dumps(validation),
                    datetime.now(UTC).isoformat(timespec="seconds"),
                ),
            )

    def promote(self, candidate: dict[str, Any], validation: dict[str, Any]) -> None:
        """Promote a validated candidate. Callers: ``mra skills approve`` only."""
        if not validation.get("ok"):
            raise ValueError(f"skill {candidate['id']} did not pass validation")
        self._decide(candidate, "promoted", validation)

    def revoke(self, ident: str) -> bool:
        """Revoke a promoted rule, or block a candidate; False when the id is unknown."""
        known = {s["id"]: s for s in self.skills()}
        known.update({c["id"]: c for c in self.candidates(min_tasks=1)})
        if ident not in known:
            return False
        self._decide(known[ident], "revoked", known[ident].get("validation") or {})
        return True

    def skills(self) -> list[dict[str, Any]]:
        """Every promoted or revoked rule, with its evidence and validation."""
        if not self.path.is_file():
            return []
        with self._connect() as db:
            db.row_factory = sqlite3.Row
            rows = [dict(r) for r in db.execute("SELECT * FROM skills ORDER BY updated_at, id")]
        for row in rows:
            for field in ("rule", "evidence", "validation"):
                row[field] = json.loads(row[field])
            row.update({k: v for k, v in row.pop("evidence").items() if k != "validation"})
        return rows

    def promoted(self) -> list[dict[str, Any]]:
        """The rules the CORRECT node may try: promoted and not revoked."""
        return [s for s in self.skills() if s["status"] == "promoted"]

    def rows(self) -> list[dict[str, Any]]:
        if not self.path.is_file():
            return []
        with self._connect() as db:
            db.row_factory = sqlite3.Row
            return [dict(row) for row in db.execute("SELECT * FROM fixes ORDER BY id")]

    def stats(self) -> dict[str, Any]:
        rows = self.rows()
        by_class: dict[str, int] = {}
        for row in rows:
            by_class[row["failure_class"]] = by_class.get(row["failure_class"], 0) + 1
        return {
            "path": str(self.path),
            "fixes": len(rows),
            "by_class": by_class,
            "contracts": sorted({f"{r['source_api']} -> {r['target_api']}" for r in rows}),
            "bytes": self.path.stat().st_size if self.path.is_file() else 0,
        }

    def purge(self) -> int:
        """Delete every stored fix, its provenance and every skill; returns the fix count."""
        count = len(self.rows())
        self.path.unlink(missing_ok=True)
        return count


def configured_path(config: dict[str, Any] | None = None) -> Path:
    from mra.models.router import load_config

    section = (config if config is not None else load_config()).get("experience") or {}
    return Path(os.getenv("MRA_EXPERIENCE_DB") or section.get("path") or DEFAULT_PATH)


def configured_ttl(config: dict[str, Any] | None = None) -> int:
    from mra.models.router import load_config

    section = (config if config is not None else load_config()).get("experience") or {}
    return int(section.get("ttl_days", DEFAULT_TTL_DAYS))


def from_config(
    config: dict[str, Any] | None = None, forbidden: tuple[Path, ...] = ()
) -> ExperienceStore | None:
    """The configured store, or None — which is the default."""
    from mra.models.router import load_config

    config = config if config is not None else load_config()
    switch = os.getenv("MRA_EXPERIENCE", "").strip().lower()
    enabled = switch in ("on", "1", "true") or (
        switch not in ("off", "0", "false")
        and bool((config.get("experience") or {}).get("enabled", False))
    )
    if not enabled:
        return None
    return ExperienceStore(
        configured_path(config), forbidden=forbidden, ttl_days=configured_ttl(config)
    )


def export_json(store: ExperienceStore) -> str:
    return json.dumps({"stats": store.stats(), "fixes": store.rows()}, indent=2)
