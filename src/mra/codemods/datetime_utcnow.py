"""T1 codemod: ``datetime.utcnow()`` -> ``datetime.now(timezone.utc)``.

The same deprecation covers ``utcfromtimestamp(t)`` ->
``fromtimestamp(t, timezone.utc)``; both are migrated, and both are what MAP
and the residual check look for (:func:`family`).

Deterministic, so it is a codemod and not an LLM call (golden rule 5): exact,
reproducible, and zero tokens against M3.

The edit is not one rewrite but two, and picking the wrong one costs precision:

    from datetime import datetime   datetime.utcnow()
                                 -> datetime.now(timezone.utc)      + import
    import datetime                datetime.datetime.utcnow()
                                 -> datetime.datetime.now(datetime.timezone.utc)
    import datetime as dt          dt.datetime.utcnow()
                                 -> dt.datetime.now(dt.timezone.utc)

Only the from-import form needs a new import. Under a module import the
timezone is already reachable through the same binding, so adding
``from datetime import timezone`` there is an unnecessary edit — exactly what
task02 was built to catch.

The new name goes into its sorted slot *within* the existing
``from datetime import ...`` statement, and nothing else in the import block is
touched (NB-2). ``AddImportsVisitor`` prepended it instead
(``timezone, datetime``), which the gold trees and ruff's I001 both reject; it
remains only as the fallback for a module with no such statement to extend.
An *aliased* statement (``from datetime import datetime as DT``) is not
extended: ruff keeps ``as`` imports on their own line, so ``timezone`` gets a
new ``from datetime import timezone`` line directly after it.

Given the analyzer's sites, only those exact positions are rewritten: the
analyzer is the one resolver (shadowing, re-exports, relative imports), and a
codemod that re-resolved names on its own would edit a shadowed
``datetime.utcnow()`` the analyzer had rightly rejected.
"""

from __future__ import annotations

import sys

import libcst as cst
from libcst.codemod import VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor
from libcst.metadata import PositionProvider

from mra.analysis.call_sites import bindings_of, dotted_path

#: The symbol this codemod migrates, as the analyzer resolves it.
TARGET = "datetime.datetime.utcnow"
UTCFROMTIMESTAMP = "datetime.datetime.utcfromtimestamp"
#: Every deprecated spelling this migration removes: what MAP and the residual
#: check search for, so a missed ``utcfromtimestamp`` can never read as GREEN.
TARGETS = (TARGET, UTCFROMTIMESTAMP)
#: deprecated method -> its timezone-aware replacement
_RENAMES = {"utcnow": "now", "utcfromtimestamp": "fromtimestamp"}

#: Ruff rules the migration's own target API trips, declared so the run report
#: can exempt them openly rather than count them as regressions. UP017 asks for
#: ``datetime.UTC`` in place of ``timezone.utc`` — the very spelling the
#: contract mandates.
EXPECTED_LINT = ["UP017"]

#: What each binding form resolves to, and what it implies about imports.
_CLASS_BINDING = "datetime.datetime"  # from datetime import datetime [as d]
_MODULE_BINDING = "datetime"  # import datetime [as dt]


def family(target: str) -> tuple[str, ...]:
    """The symbols a run for ``target`` migrates and audits."""
    return TARGETS if target in TARGETS else (target,)


class ConvertUtcnowCommand(VisitorBasedCodemodCommand):
    """Rewrite ``utcnow()`` / ``utcfromtimestamp(t)`` calls, whatever their spelling.

    ``sites`` — ``(line, col)`` positions from the analyzer — restricts the
    rewrite to exactly those calls; without it every call that resolves through
    this module's own imports is rewritten.
    """

    DESCRIPTION = "Replace datetime.utcnow() with datetime.now(timezone.utc)."
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, context, sites: set[tuple[int, int]] | None = None) -> None:
        super().__init__(context)
        self.bindings: dict[str, str] = {}
        self.sites = sites
        #: repo-facing record of what changed, for the trajectory.
        self.edits: list[str] = []

    def transform_module_impl(self, tree: cst.Module) -> cst.Module:
        # Bindings are collected up front rather than during traversal, so a
        # call inside a function defined above the import still resolves.
        self.bindings = bindings_of(tree)
        self.needs_timezone = False
        tree = super().transform_module_impl(tree)
        if self.needs_timezone and self.bindings.get("timezone") != "datetime.timezone":
            inserter = _InsertTimezone()
            tree = tree.visit(inserter)
            if not inserter.done:
                placed = _place_timezone_import(tree)
                if placed is None:  # no top-level import block at all
                    AddImportsVisitor.add_needed_import(self.context, "datetime", "timezone")
                else:
                    tree = placed
        return tree

    def _form(self, original: cst.Call, head: cst.Name, attributes: list[str]) -> str | None:
        """``"class"`` / ``"module"`` binding of a call to migrate, or None to leave it."""
        if self.sites is not None:
            start = self.get_metadata(PositionProvider, original).start
            if (start.line, start.column) not in self.sites:
                return None
            # The analyzer already resolved it; the call's shape says which form.
            return {1: "class", 2: "module"}.get(len(attributes))
        base = self.bindings.get(head.value)
        if base is None or ".".join([base, *attributes]) not in TARGETS:
            return None
        return {_CLASS_BINDING: "class", _MODULE_BINDING: "module"}.get(base)

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        flattened = dotted_path(updated_node.func)
        if flattened is None or not flattened[1] or flattened[1][-1] not in _RENAMES:
            return updated_node
        head, attributes = flattened
        method = attributes[-1]
        # utcnow() takes no arguments, utcfromtimestamp(t) exactly one positional.
        arity = 0 if method == "utcnow" else 1
        if len(updated_node.args) != arity or any(a.keyword or a.star
                                                  for a in updated_node.args):
            return updated_node
        form = self._form(original_node, head, attributes)
        if form is None:
            return updated_node

        # `.with_changes(attr=...)` keeps the receiver node untouched, so
        # whitespace, comments and the original spelling all survive (FR-5).
        new_func = updated_node.func.with_changes(attr=cst.Name(_RENAMES[method]))
        if form == "class":
            # `datetime` here is the class; timezone has to be imported.
            self.needs_timezone = True
            timezone = cst.Attribute(value=cst.Name("timezone"), attr=cst.Name("utc"))
        else:
            # `dt.timezone` rides the import that is already there.
            timezone = cst.Attribute(
                value=cst.Attribute(value=cst.Name(head.value), attr=cst.Name("timezone")),
                attr=cst.Name("utc"),
            )
        self.edits.append(f"{head.value}.{'.'.join(attributes)} -> {_RENAMES[method]}(...)")
        args = [*(a.with_changes(comma=cst.MaybeSentinel.DEFAULT) for a in updated_node.args),
                cst.Arg(value=timezone)]
        return updated_node.with_changes(func=new_func, args=args)


class _InsertTimezone(cst.CSTTransformer):
    """Add ``timezone`` to the first ``from datetime import ...`` binding the class.

    Inserted before the first name that sorts after it; the other names, their
    order and their commas are left exactly as written. An aliased statement
    gets a separate ``from datetime import timezone`` line after it instead.
    """

    def __init__(self) -> None:
        self.done = False

    def leave_SimpleStatementLine(
        self, original_node: cst.SimpleStatementLine, updated_node: cst.SimpleStatementLine,
    ) -> cst.SimpleStatementLine | cst.FlattenSentinel[cst.SimpleStatementLine]:
        if self.done or len(updated_node.body) != 1:
            return updated_node
        node = updated_node.body[0]
        if (not isinstance(node, cst.ImportFrom) or isinstance(node.names, cst.ImportStar)
                or node.relative or node.module is None
                or cst.Module([]).code_for_node(node.module) != "datetime"
                or not any(alias.evaluated_name == "datetime" for alias in node.names)):
            return updated_node
        self.done = True
        if any(alias.asname is not None for alias in node.names):
            own_line = cst.SimpleStatementLine(body=[cst.ImportFrom(
                module=cst.Name("datetime"), names=[cst.ImportAlias(name=cst.Name("timezone"))])])
            return cst.FlattenSentinel([updated_node, own_line])
        return updated_node.with_changes(body=[_with_timezone(node)])


def _import_key(line: cst.CSTNode) -> tuple[int, int, str] | None:
    """isort's order for a top-level import line: (section, from-ness, module)."""
    if not isinstance(line, cst.SimpleStatementLine) or len(line.body) != 1:
        return None
    node = line.body[0]
    if isinstance(node, cst.Import):
        module, kind = cst.Module([]).code_for_node(node.names[0].name), 0
    elif isinstance(node, cst.ImportFrom):
        if node.relative:
            return (4, 1, "")
        module, kind = cst.Module([]).code_for_node(node.module), 1
    else:
        return None
    top = module.split(".")[0]
    section = 0 if top == "__future__" else 1 if top in sys.stdlib_module_names else 2
    return (section, kind, module)


def _place_timezone_import(tree: cst.Module) -> cst.Module | None:
    """Insert ``from datetime import timezone`` where isort would put it.

    Used when no ``from datetime import ...`` exists to extend — e.g. ``datetime``
    arrived through a re-export. Goes before the first top-level import that
    sorts after it (stdlib < third/first party < relative), and a different
    section after it gets the blank line isort separates sections with.
    """
    new_key = (1, 1, "datetime")
    body = list(tree.body)
    imports = [i for i, line in enumerate(body) if _import_key(line) is not None]
    if not imports:
        return None
    later = next((i for i in imports if _import_key(body[i]) > new_key), None)
    new = cst.SimpleStatementLine(body=[cst.ImportFrom(
        module=cst.Name("datetime"), names=[cst.ImportAlias(name=cst.Name("timezone"))])])
    if later is None:
        body.insert(imports[-1] + 1, new)
        return tree.with_changes(body=body)
    following = body[later]
    previous = [i for i in imports if i < later]
    if not previous or _import_key(body[previous[-1]])[0] != new_key[0]:
        # First of its section: it takes over the separating blank lines/comments.
        new = new.with_changes(leading_lines=following.leading_lines)
    if _import_key(following)[0] != new_key[0]:
        following = following.with_changes(leading_lines=[cst.EmptyLine()])
    else:
        following = following.with_changes(leading_lines=[])
    body[later:later + 1] = [new, following]
    return tree.with_changes(body=body)


def _with_timezone(node: cst.ImportFrom) -> cst.ImportFrom:
    names = list(node.names)
    index = next((i for i, alias in enumerate(names) if alias.evaluated_name > "timezone"),
                 len(names))
    # Reuse the list's own separator, so a one-per-line list stays one per line.
    comma = next((alias.comma for alias in names[:-1] if isinstance(alias.comma, cst.Comma)),
                 cst.Comma(whitespace_after=cst.SimpleWhitespace(" ")))
    if index == len(names):
        # Appending: the old last name now needs a separator, and the new one
        # inherits whatever trailed it (nothing, or a trailing comma).
        last = names[-1]
        new = cst.ImportAlias(name=cst.Name("timezone"), comma=last.comma)
        names[-1] = last.with_changes(comma=comma)
    else:
        new = cst.ImportAlias(name=cst.Name("timezone"), comma=comma)
    names.insert(index, new)
    return node.with_changes(names=names)
