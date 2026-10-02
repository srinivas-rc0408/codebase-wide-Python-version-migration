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

import json
import os
import re
import sqlite3
from datetime import UTC, datetime
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
)
"""


def clean_message(message: str) -> str:
    """Normalised, path-free, secret-free: nothing that identifies a repo or a run."""
    text = _QUOTED_PATH.sub("'<path>'", message)
    text = _FILE.sub("<file>", normalize_message(text))
    return redact_secrets(text)[0][:500]


def diff_pattern(diff: str) -> str:
    """A ``git diff`` -> its changed lines only: no headers, hunks or paths."""
    lines = [line for line in diff.splitlines()
             if line[:1] in "+-" and not line.startswith(("+++", "---"))]
    text = _QUOTED_PATH.sub("'<path>'", "\n".join(lines[:PATTERN_MAX_LINES]))
    return redact_secrets(_ABS_PATH.sub("<path>/", text))[0]


def format_hint(fix: dict[str, Any]) -> str:
    return f"when `{fix['message']}`, this fixed it:\n{fix['pattern']}"


class ExperienceStore:
    """One SQLite file of past fixes. ``readonly`` serves hints but learns nothing."""

    def __init__(self, path: Path | str, *, readonly: bool = False,
                 forbidden: tuple[Path, ...] = ()) -> None:
        self.path = Path(path).expanduser().resolve()
        for root in (AGENT_ROOT, *forbidden):
            if self.path.is_relative_to(Path(root).resolve()):
                raise ValueError(f"experience store {self.path} is inside {root}; it must "
                                 "live outside every repository (default ~/.mra/)")
        self.readonly = readonly

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.execute(SCHEMA)
        return connection

    def record(self, failure_class: str, message: str, contract: dict[str, Any],
               diff: str) -> bool:
        """Store one fix; returns False when read-only, empty, or already known."""
        pattern = diff_pattern(diff)
        if self.readonly or not pattern:
            return False
        with self._connect() as db:
            cursor = db.execute(
                "INSERT OR IGNORE INTO fixes (created_at, failure_class, message, source_api,"
                " target_api, pattern) VALUES (?, ?, ?, ?, ?, ?)",
                (datetime.now(UTC).isoformat(timespec="seconds"), failure_class,
                 clean_message(message), str(contract.get("source_api", "")),
                 str(contract.get("target_api", "")), pattern))
            return cursor.rowcount == 1

    def similar(self, failure_class: str, message: str, contract: dict[str, Any],
                k: int = TOP_K) -> list[dict[str, Any]]:
        """Same class and contract, ranked by similarity of the normalised message."""
        if not self.path.is_file():
            return []
        with self._connect() as db:
            rows = db.execute(
                "SELECT id, message, pattern FROM fixes WHERE failure_class = ? AND "
                "source_api = ? AND target_api = ?",
                (failure_class, str(contract.get("source_api", "")),
                 str(contract.get("target_api", "")))).fetchall()
        wanted = clean_message(message)
        scored = sorted(((SequenceMatcher(None, wanted, text).ratio(), row_id, text, pattern)
                         for row_id, text, pattern in rows), key=lambda r: (-r[0], r[1]))
        return [{"id": row_id, "similarity": round(score, 3), "message": text,
                 "pattern": pattern} for score, row_id, text, pattern in scored[:k]]

    def hints(self, failure_class: str, message: str,
              contract: dict[str, Any]) -> list[dict[str, Any]]:
        """The top-k fixes whose :func:`format_hint` text fits :data:`HINT_BUDGET_CHARS`."""
        hints, used = [], 0
        for fix in self.similar(failure_class, message, contract):
            used += len(format_hint(fix))
            if used > HINT_BUDGET_CHARS:
                break
            hints.append(fix)
        return hints

    def learn(self, repo: Path | str, trajectory: list[dict[str, Any]],
              contract: dict[str, Any]) -> int:
        """Record every CORRECT whose very next TEST was green; returns how many were new.

        The fix is the diff of that correction's own commit (``sha~1..sha``:
        CORRECT snapshots immediately before and after the corrector runs).
        """
        from git import Repo

        learned = 0
        for event, after in zip(trajectory, trajectory[1:], strict=False):
            detail, verdict = event["detail"], after["detail"]
            if (event["node"] != "CORRECT" or after["node"] != "TEST" or not detail.get("sha")
                    or verdict.get("failed", 1) or verdict.get("errors", 1)):
                continue
            diff = Repo(repo).git.diff(f"{detail['sha']}~1", detail["sha"])
            learned += self.record(detail.get("failure_class", ""), detail.get("message", ""),
                                   contract, diff)
        return learned

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
        return {"path": str(self.path), "fixes": len(rows), "by_class": by_class,
                "contracts": sorted({f"{r['source_api']} -> {r['target_api']}" for r in rows}),
                "bytes": self.path.stat().st_size if self.path.is_file() else 0}

    def purge(self) -> int:
        """Delete every stored fix; returns how many there were."""
        count = len(self.rows())
        self.path.unlink(missing_ok=True)
        return count


def configured_path(config: dict[str, Any] | None = None) -> Path:
    from mra.models.router import load_config

    section = (config if config is not None else load_config()).get("experience") or {}
    return Path(os.getenv("MRA_EXPERIENCE_DB") or section.get("path") or DEFAULT_PATH)


def from_config(config: dict[str, Any] | None = None,
                forbidden: tuple[Path, ...] = ()) -> ExperienceStore | None:
    """The configured store, or None — which is the default."""
    from mra.models.router import load_config

    config = config if config is not None else load_config()
    switch = os.getenv("MRA_EXPERIENCE", "").strip().lower()
    enabled = switch in ("on", "1", "true") or (
        switch not in ("off", "0", "false")
        and bool((config.get("experience") or {}).get("enabled", False)))
    return ExperienceStore(configured_path(config), forbidden=forbidden) if enabled else None


def export_json(store: ExperienceStore) -> str:
    return json.dumps({"stats": store.stats(), "fixes": store.rows()}, indent=2)
