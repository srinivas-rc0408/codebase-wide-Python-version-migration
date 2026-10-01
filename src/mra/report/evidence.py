"""The verification pass that runs once, at the end of a run: ``verification.json``.

Everything the verdict needs beyond the graph's own artifacts is measured here
and frozen to disk, so the report stays a pure function of files in the run
directory and ``mra report`` can rebuild it without touching the sandbox.

* residual MAP on the migrated tree — no ground truth needed, so it works on a
  real repo; also lists what MAP skips by design (star imports, bare
  references) and files it could not parse;
* semantic checks for the migration's target API;
* ``git apply --check`` of migration.patch on a fresh export of the
  pre-migration commit;
* ruff before (on that export) and after, and coverage.py over the final
  suite — both inside the sandbox, never on the host (golden rule 3).

Each step records its own error instead of raising: a crashed run still gets
whatever evidence can be gathered.
"""

from __future__ import annotations

import io
import json
import re
import shutil
import tarfile
from pathlib import Path
from typing import Any

import libcst as cst
from git import Git, GitCommandError, Repo
from libcst.metadata import MetadataWrapper, PositionProvider

from mra.analysis.call_sites import ImportBindings, bindings_of, dotted_path, find_in_source
from mra.analysis.dep_graph import python_files
from mra.codemods.datetime_utcnow import TARGET as UTCNOW
from mra.nodes.correct_node import is_test_path
from mra.sandbox import SandboxRunner, diff

CONTAINER_PREFIX = "/work/repo_rw/"
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


# -- the patch ----------------------------------------------------------------


def parse_patch(patch: str) -> dict[str, dict[str, Any]]:
    """``git diff`` text -> ``{file: {added, removed, new_lines, hunks}}``."""
    files: dict[str, dict[str, Any]] = {}
    current: dict[str, Any] | None = None
    old_path = ""
    line_no = 0
    for line in patch.splitlines():
        if line.startswith("--- "):
            old_path = line[6:] if line.startswith("--- a/") else ""
        elif line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else old_path
            current = files.setdefault(path, {"added": 0, "removed": 0,
                                              "new_lines": [], "hunks": []})
        elif current is not None and (match := HUNK.match(line)):
            line_no = int(match.group(1))
            current["hunks"].append([line])
        elif current is not None and current["hunks"] and line[:1] in ("+", "-", " "):
            current["hunks"][-1].append(line)
            if line.startswith("+"):
                current["added"] += 1
                current["new_lines"].append(line_no)
                line_no += 1
            elif line.startswith("-"):
                current["removed"] += 1
            else:
                line_no += 1
    return files


# -- residual MAP -------------------------------------------------------------


class _Skipped(ImportBindings):
    """What MAP deliberately does not resolve: star imports and bare references."""

    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, target: str, bindings: dict[str, str]) -> None:
        super().__init__()
        self.target, self.resolved_bindings = target, bindings
        self.called: set[int] = set()
        self.found: list[dict[str, Any]] = []

    def _add(self, node: cst.CSTNode, kind: str, text: str) -> None:
        line = self.get_metadata(PositionProvider, node).start.line
        self.found.append({"line": line, "kind": kind, "text": text})

    def visit_ImportFrom(self, node: cst.ImportFrom) -> None:
        if isinstance(node.names, cst.ImportStar) and node.module is not None:
            module = cst.Module([]).code_for_node(node.module)
            if self.target.startswith(module + "."):
                self._add(node, "star-import", f"from {module} import *")

    def visit_Call(self, node: cst.Call) -> None:
        self.called.add(id(node.func))

    def visit_Attribute(self, node: cst.Attribute) -> None:
        flattened = dotted_path(node)
        if flattened is None or id(node) in self.called:
            return
        head, attributes = flattened
        base = self.resolved_bindings.get(head.value)
        if base and ".".join([base, *attributes]) == self.target:
            self._add(node, "bare-reference", cst.Module([]).code_for_node(node))


def residual_scan(repo: Path, target: str) -> dict[str, list[Any]]:
    """Re-run MAP over the migrated tree, plus what MAP skips by design."""
    sites: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    unparseable: list[str] = []
    for path in python_files(repo):
        relative = path.relative_to(repo).as_posix()
        source = path.read_text(errors="replace")
        try:
            module = cst.parse_module(source)
        except cst.ParserSyntaxError:
            unparseable.append(relative)
            continue
        sites += [site.to_dict() for site in find_in_source(source, target, relative)]
        visitor = _Skipped(target, bindings_of(module))
        MetadataWrapper(module).visit(visitor)
        skipped += [{"file": relative, **found} for found in visitor.found]
    return {"sites": sites, "skipped": skipped, "unparseable": unparseable}


# -- semantic checks ----------------------------------------------------------


class _NowCalls(cst.CSTVisitor):
    def __init__(self) -> None:
        self.calls: list[cst.Call] = []

    def visit_Call(self, node: cst.Call) -> None:
        self.calls.append(node)


def _resolve(node: cst.BaseExpression, bindings: dict[str, str]) -> str | None:
    flattened = dotted_path(node)
    if flattened is None:
        return None
    head, attributes = flattened
    base = bindings.get(head.value)
    return ".".join([base, *attributes]) if base else None


def _aware_now(source: str) -> tuple[int, list[str]]:
    """(naive ``datetime.now()`` count, tz arguments that do not resolve)."""
    try:
        module = cst.parse_module(source)
    except cst.ParserSyntaxError:
        return 0, ["file does not parse"]
    bindings = bindings_of(module)
    visitor = _NowCalls()
    module.visit(visitor)
    naive, unresolved = 0, []
    for call in visitor.calls:
        if _resolve(call.func, bindings) != "datetime.datetime.now":
            continue
        tz = next((a.value for a in call.args if a.keyword is None or a.keyword.value == "tz"),
                  None)
        if tz is None:
            naive += 1
        elif isinstance(tz, cst.Attribute | cst.Name) and _resolve(tz, bindings) is None:
            unresolved.append(cst.Module([]).code_for_node(tz))
    return naive, unresolved


def semantic_checks(base: Path | None, repo: Path, files: list[str],
                    target: str) -> list[dict[str, Any]]:
    """Per edited file: does the new code still mean what the target API means?

    Only ``datetime.utcnow`` has checks so far: the migrated call must be
    timezone-aware (no new naive ``datetime.now()``) and its ``tz`` must
    resolve through an import (``timezone.utc`` without ``timezone`` imported
    is a NameError the moment it runs).
    """
    if target != UTCNOW:
        return []
    checks = []
    for file in files:
        after = repo / file
        if not after.is_file():
            continue
        naive_after, unresolved = _aware_now(after.read_text())
        before = base / file if base is not None else None
        naive_before = _aware_now(before.read_text())[0] if before and before.is_file() else 0
        problems = []
        if naive_after > naive_before:
            problems.append(f"{naive_after - naive_before} new naive datetime.now()")
        if unresolved:
            problems.append("tz not imported: " + ", ".join(sorted(set(unresolved))))
        checks.append({"check": "migrated datetime.now() is timezone-aware", "file": file,
                       "passed": not problems,
                       "detail": "; ".join(problems) or "aware, tz resolves to an import"})
    return checks


# -- the fresh checkout, apply-check, sandbox runs ----------------------------


def base_commit(repo: Path) -> str:
    """The run's first commit: ``run_migration``'s pre-migration snapshot."""
    return Repo(repo).git.rev_list("--max-parents=0", "HEAD").splitlines()[0]


def export_tree(repo: Path, sha: str, dest: Path) -> Path:
    """A fresh checkout of ``sha`` with no git metadata, via ``git archive``."""
    buffer = io.BytesIO()
    Repo(repo).archive(buffer, treeish=sha, format="tar")
    buffer.seek(0)
    dest.mkdir(parents=True)
    with tarfile.open(fileobj=buffer) as archive:
        archive.extractall(dest, filter="data")
    return dest


def apply_check(fresh: Path, patch_path: Path) -> dict[str, Any]:
    if not patch_path.read_text().strip():
        return {"ok": True, "detail": "empty patch"}
    try:
        Git(fresh).apply("--check", str(patch_path.resolve()))
    except GitCommandError as exc:
        return {"ok": False, "detail": (exc.stderr or str(exc)).strip()[:300]}
    return {"ok": True, "detail": "applies cleanly"}


def _coverage(path: Path, patch_files: dict[str, dict[str, Any]]) -> dict[str, Any]:
    edited = {f: p["new_lines"] for f, p in patch_files.items() if not is_test_path(f)}
    try:
        data = json.loads(path.read_text())["files"]
    except (OSError, ValueError, KeyError) as exc:
        return {"available": False, "error": f"coverage.json unreadable ({type(exc).__name__})",
                "files": {f: {"changed": lines, "executed": []} for f, lines in edited.items()}}
    executed = {name.removeprefix(CONTAINER_PREFIX): entry.get("executed_lines", [])
                for name, entry in data.items()}
    return {"available": True, "files": {
        f: {"changed": lines, "executed": sorted(set(lines) & set(executed.get(f, [])))}
        for f, lines in edited.items()}}


def _ruff_findings(path: Path) -> list[dict[str, str]] | None:
    """ruff's JSON output -> ``[{code, file, message}]`` (no line numbers: edits move them)."""
    try:
        raw = json.loads(path.read_text())
    except (OSError, ValueError):
        return None
    return sorted(({"code": d.get("code") or "", "message": d.get("message", ""),
                    "file": d.get("filename", "").removeprefix(CONTAINER_PREFIX)}
                   for d in raw), key=lambda f: (f["file"], f["code"], f["message"]))


def _step(evidence: dict[str, Any], key: str, compute: Any) -> Any:
    try:
        evidence[key] = compute()
    except Exception as exc:  # evidence, not control flow: record and carry on
        evidence.setdefault("errors", {})[key] = f"{type(exc).__name__}: {exc}"[:300]
    return evidence.get(key)


def collect(out_dir: Path, target: str, task_id: str, run_id: str) -> dict[str, Any]:
    """Measure everything and write ``verification.json``. Never raises."""
    repo, patch_path = out_dir / "repo", out_dir / "migration.patch"
    verify_dir = out_dir / "verify"
    shutil.rmtree(verify_dir, ignore_errors=True)
    evidence: dict[str, Any] = {"target": target}
    sha = _step(evidence, "base_sha", lambda: base_commit(repo))
    if sha and not patch_path.is_file():
        # A crashed run never reached the line that writes the patch; the edits
        # it did make are still in git, and the report must show them.
        def salvage() -> bool:
            patch_path.write_text(diff(repo, sha))
            return True

        _step(evidence, "patch_salvaged", salvage)
    patch_files = parse_patch(patch_path.read_text()) if patch_path.is_file() else {}

    _step(evidence, "inventory", lambda: [
        {"file": p.relative_to(repo).as_posix(), "loc": len(p.read_text(errors="replace")
                                                            .splitlines())}
        for p in python_files(repo)])
    _step(evidence, "residual", lambda: residual_scan(repo, target))
    fresh = _step(evidence, "fresh_checkout",
                  lambda: str(export_tree(repo, sha, verify_dir / "fresh"))) if sha else None
    fresh_path = Path(fresh) if fresh else None
    if fresh_path and patch_path.is_file():
        _step(evidence, "apply_check", lambda: apply_check(fresh_path, patch_path))
    edited = sorted(f for f in patch_files if not is_test_path(f) and f.endswith(".py"))
    _step(evidence, "semantic", lambda: semantic_checks(fresh_path, repo, edited, target))

    sandbox = SandboxRunner(runs_dir=verify_dir)
    lint: dict[str, Any] = {"pre": None, "post": None}
    if fresh_path:
        _step(evidence, "lint_baseline_report", lambda: sandbox.run(
            fresh_path, task_id=task_id, phase="pre", run_id=f"{run_id}-baseline"))
        lint["pre"] = _ruff_findings(verify_dir / f"{run_id}-baseline" / "ruff.json")
    if repo.is_dir():
        _step(evidence, "coverage_report", lambda: sandbox.run(
            repo, task_id=task_id, phase="post", run_id=f"{run_id}-coverage", coverage=True))
        lint["post"] = _ruff_findings(verify_dir / f"{run_id}-coverage" / "ruff.json")
        evidence["coverage"] = _coverage(verify_dir / f"{run_id}-coverage" / "coverage.json",
                                         patch_files)
    evidence["lint"] = lint
    evidence.pop("fresh_checkout", None)
    shutil.rmtree(verify_dir / "fresh", ignore_errors=True)
    (out_dir / "verification.json").write_text(json.dumps(evidence, indent=2) + "\n")
    return evidence
