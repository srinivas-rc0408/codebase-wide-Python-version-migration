"""Verified skill promotion: a fix the store has seen work, turned into a codemod.

Opt-in, and off in every benchmark path unless a run is handed rules explicitly.

1. **Candidates** — :meth:`ExperienceStore.candidates`: a fix that succeeded in
   at least :data:`MIN_INDEPENDENT_TASKS` fully GREEN runs on *distinct* tasks,
   for the same failure class and contract. Repeats of one deterministic task
   are the same evidence three times, so they count once.
2. **Codemod** — :func:`derive_rule` reduces the stored ``-``/``+`` line pairs
   to their smallest changed expressions plus the imports they need;
   :class:`RuleCommand` is the LibCST codemod that replays exactly that.
3. **Validation** — :func:`validate` runs the full edge suite and the
   deterministic Tier-A matrix with the rule on; both must be unchanged.
4. **Promotion** — only ``mra skills approve <id>``, which validates first.
   Nothing is promoted automatically.
5. **Use** — the CORRECT node tries promoted rules before its corrector (the
   LLM, with ``--llm``) and records the rule id in the trajectory, which is
   where the run report reads it from. EDIT never calls an LLM — it is already
   a codemod — so there is nothing there for a rule to pre-empt.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

import libcst as cst
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor

from mra.analysis.call_sites import is_test_path

MIN_INDEPENDENT_TASKS = 3
ROOT = Path(__file__).resolve().parents[2]
COMMITTED_EDGE = ROOT / "corpus" / "edge" / "results.json"
COMMITTED_MATRIX = ROOT / "runs" / "benchmark" / "results.json"
#: What "the Tier-A results are unchanged" compares. Wall clock is not a result.
MATRIX_FIELDS = (
    "outcomes",
    "m1_recall_mean",
    "m1_precision_mean",
    "m2_pass_rate_mean",
    "m2_regressions_mean",
    "corrections_mean",
    "m3_tokens_mean",
    "m3_steps_mean",
    "cost_usd_mean",
)


# -- 2. a stored fix -> a rule -> a codemod --------------------------------


def _code(node: cst.CSTNode) -> str:
    return cst.Module(body=[]).code_for_node(node)


def _smallest_change(old: cst.CSTNode, new: cst.CSTNode) -> tuple[cst.CSTNode, cst.CSTNode]:
    """Descend while exactly one child differs; stop where the change is."""
    while type(old) is type(new):
        pairs = list(zip(old.children, new.children, strict=False))
        if len(old.children) != len(new.children):
            break
        differing = [(a, b) for a, b in pairs if not a.deep_equals(b)]
        if len(differing) != 1:
            break
        old, new = differing[0]
    return old, new


def _import_names(statement: cst.CSTNode) -> tuple[str, set[str]] | None:
    """``from m import a, b`` -> ("m", {"a", "b"}); anything else -> None."""
    if not isinstance(statement, cst.SimpleStatementLine) or len(statement.body) != 1:
        return None
    node = statement.body[0]
    if not isinstance(node, cst.ImportFrom) or node.module is None or node.relative:
        return None
    if isinstance(node.names, cst.ImportStar):
        return None
    return _code(node.module), {_code(alias.name) for alias in node.names if not alias.asname}


def derive_rule(pattern: str) -> dict[str, list[list[str]]] | None:
    """A stored diff pattern -> ``{"replace": [[old, new]], "imports": [[module, name]]}``.

    None when the pattern does not reduce to expression rewrites plus added
    ``from`` imports — a multi-line statement, unequal ``-``/``+`` counts, a
    removed import, or a change whose old side is a bare name (renaming every
    occurrence of an identifier is not a fix, it is a hazard).
    """
    lines = pattern.splitlines()
    old_lines = [line[1:] for line in lines if line.startswith("-")]
    new_lines = [line[1:] for line in lines if line.startswith("+")]
    if not old_lines or len(old_lines) != len(new_lines):
        return None
    replace: set[tuple[str, str]] = set()
    imports: set[tuple[str, str]] = set()
    for old_line, new_line in zip(old_lines, new_lines, strict=True):
        try:
            old, new = cst.parse_statement(old_line.strip()), cst.parse_statement(new_line.strip())
        except cst.ParserSyntaxError:
            return None
        if old.deep_equals(new):
            continue
        old_import, new_import = _import_names(old), _import_names(new)
        if old_import or new_import:
            if not (old_import and new_import) or old_import[0] != new_import[0]:
                return None
            if not old_import[1] <= new_import[1]:
                return None
            imports |= {(new_import[0], name) for name in new_import[1] - old_import[1]}
            continue
        before, after = _smallest_change(old, new)
        if not isinstance(before, cst.BaseExpression) or not isinstance(after, cst.BaseExpression):
            return None
        if isinstance(before, cst.Name):
            return None
        replace.add((_code(before), _code(after)))
    if not replace:
        return None
    return {"replace": sorted(map(list, replace)), "imports": sorted(map(list, imports))}


def skill_id(failure_class: str, source_api: str, target_api: str, rule: dict[str, Any]) -> str:
    key = json.dumps([failure_class, source_api, target_api, rule], sort_keys=True)
    return hashlib.sha256(key.encode()).hexdigest()[:10]


class RuleCommand(VisitorBasedCodemodCommand):
    """Replace each expression structurally equal to a rule's old side; add its imports."""

    DESCRIPTION = "Replay a promoted rule."

    def __init__(self, context: CodemodContext, rule: dict[str, Any]) -> None:
        super().__init__(context)
        # ponytail: exact structural match (deep_equals), so an aliased spelling
        # (`dt.utcnow()`) never matches; widen with libcst matchers if a rule needs to.
        self.replace = [
            (cst.parse_expression(o), cst.parse_expression(n)) for o, n in rule["replace"]
        ]
        self.imports = rule["imports"]
        self.fired = False

    def transform_module_impl(self, tree: cst.Module) -> cst.Module:
        tree = super().transform_module_impl(tree)
        if not self.fired:
            return tree
        for module, name in self.imports:
            extended = _extend_from_import(tree, module, name)
            if extended is None:  # no `from module import ...` to extend
                AddImportsVisitor.add_needed_import(self.context, module, name)
            else:
                tree = extended
        return tree

    def on_leave(self, original_node: cst.CSTNode, updated_node: cst.CSTNode) -> Any:
        updated = super().on_leave(original_node, updated_node)
        if isinstance(original_node, cst.BaseExpression):
            for old, new in self.replace:
                if original_node.deep_equals(old):
                    self.fired = True
                    return new
        return updated


def _extend_from_import(tree: cst.Module, module: str, name: str) -> cst.Module | None:
    """Add ``name`` to the first top-level ``from module import ...``, in sorted place.

    The same tree when it is already imported there; None when there is no such
    line (the caller falls back to AddImportsVisitor).
    """
    body = list(tree.body)
    for index, line in enumerate(body):
        found = _import_names(line)
        if found is None or found[0] != module:
            continue
        if name in found[1]:
            return tree
        node = line.body[0]
        names = list(node.names)
        at = next((i for i, a in enumerate(names) if a.evaluated_name > name), len(names))
        comma = cst.Comma(whitespace_after=cst.SimpleWhitespace(" "))
        alias = cst.ImportAlias(name=cst.Name(name))
        if at == len(names):
            names[-1] = names[-1].with_changes(comma=comma)
        else:
            alias = alias.with_changes(comma=comma)
        names.insert(at, alias)
        body[index] = line.with_changes(body=[node.with_changes(names=names)])
        return tree.with_changes(body=body)
    return None


def apply_rule(repo: Path | str, relative: str, rule: dict[str, Any]) -> list[str]:
    """Run one rule over one file, byte-preserving; NB-4: never a test file."""
    if is_test_path(relative):
        raise PermissionError(f"NB-4: a rule may not edit the test oracle ({relative})")
    path = Path(repo) / relative
    source = path.read_bytes()
    command = RuleCommand(CodemodContext(filename=str(path)), rule)
    migrated = command.transform_module(cst.parse_module(source)).bytes
    if migrated == source:
        return []
    path.write_bytes(migrated)
    return [relative]


def matching(rules: list[dict[str, Any]], failure_class: str, contract: dict[str, Any]) -> list:
    """The promoted rules that apply to this failure class under this contract."""
    return [
        r
        for r in rules
        if r["failure_class"] == failure_class
        and r["source_api"] == str(contract.get("source_api", ""))
        and r["target_api"] == str(contract.get("target_api", ""))
    ]


# -- 3. validation ---------------------------------------------------------


def compare_edge(results: dict[str, Any], committed: dict[str, Any]) -> list[str]:
    """Every committed case still passes with the same verdict."""
    before = {c["case"]: c for c in committed["cases"]}
    after = {c["case"]: c for c in results["cases"]}
    problems = [f"edge {name}: missing" for name in before if name not in after]
    for name, row in after.items():
        was = before.get(name)
        if was is None:
            continue
        if not row["pass"] or row["actual"] != was["actual"]:
            problems.append(f"edge {name}: {was['actual']} -> {row['actual']} {row['problems']}")
    return problems


def compare_matrix(results: dict[str, Any], committed: dict[str, Any]) -> list[str]:
    """Every (config, task) aggregate equal on :data:`MATRIX_FIELDS`."""
    before = {(a["config"], a["task_id"]): a for a in committed["aggregates"]}
    problems = []
    for entry in results["aggregates"]:
        was = before.get((entry["config"], entry["task_id"]))
        if was is None:
            problems.append(f"matrix {entry['config']}/{entry['task_id']}: not in results.json")
            continue
        for field in MATRIX_FIELDS:
            if entry[field] != was[field]:
                problems.append(
                    f"matrix {entry['config']}/{entry['task_id']} {field}: "
                    f"{was[field]} -> {entry[field]}"
                )
    return problems


def validate(
    skill: dict[str, Any],
    *,
    edge_cases: list[str] | None = None,
    tasks: list[str] | None = None,
    configs: list[str] | None = None,
) -> dict[str, Any]:
    """Run the edge suite and the deterministic Tier-A matrix with ``skill`` on.

    ``None`` everywhere means the full gate (39 edge cases, every committed
    deterministic config on every task); the narrower arguments exist for tests.
    """
    from mra.benchmark.edge import run_suite
    from mra.benchmark.runner import CONFIGS, run_matrix

    committed_edge = json.loads(COMMITTED_EDGE.read_text())
    if edge_cases:
        committed_edge["cases"] = [c for c in committed_edge["cases"] if c["case"] in edge_cases]
    committed_matrix = json.loads(COMMITTED_MATRIX.read_text())
    ran = {(r["config"], r["task_id"]) for r in committed_matrix["rows"]}
    names = configs or sorted({c for c, _ in ran})
    chosen = [c for c in CONFIGS if c.name in names and not c.requires_key]
    with tempfile.TemporaryDirectory(prefix="mra-skill-validate-") as scratch:
        edge = run_suite(runs_dir=Path(scratch) / "edge", only=edge_cases, rules=[skill])
        matrix = run_matrix(
            tasks or committed_matrix["tasks"],
            chosen,
            repeats=committed_matrix["repeats"],
            out_dir=Path(scratch) / "matrix",
            baselines=False,
            rules=[skill],
        )
    problems = compare_edge(edge, committed_edge) + compare_matrix(matrix, committed_matrix)
    return {
        "ok": not problems,
        "edge": f"{edge['passed']}/{edge['total']}",
        "matrix_runs": len(matrix["rows"]),
        "problems": problems,
    }


# -- opt-in ----------------------------------------------------------------


def from_config(config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Promoted rules for ``mra run``, or ``[]`` — the default.

    On only with ``[skills] enabled = true`` in mra.toml or ``MRA_SKILLS=on``
    (``MRA_SKILLS=off`` always wins). Benchmarks never call this.
    """
    from mra.memory.experience import ExperienceStore, configured_path
    from mra.models.router import load_config

    config = config if config is not None else load_config()
    switch = os.getenv("MRA_SKILLS", "").strip().lower()
    enabled = switch in ("on", "1", "true") or (
        switch not in ("off", "0", "false")
        and bool((config.get("skills") or {}).get("enabled", False))
    )
    return ExperienceStore(configured_path(config)).promoted() if enabled else []
