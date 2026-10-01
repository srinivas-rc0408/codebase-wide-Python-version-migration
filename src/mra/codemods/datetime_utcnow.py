"""T1 codemod: ``datetime.utcnow()`` -> ``datetime.now(timezone.utc)``.

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
"""

from __future__ import annotations

import libcst as cst
from libcst.codemod import VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor

from mra.analysis.call_sites import bindings_of, dotted_path

#: The symbol this codemod migrates, as the analyzer resolves it.
TARGET = "datetime.datetime.utcnow"

#: Ruff rules the migration's own target API trips, declared so the run report
#: can exempt them openly rather than count them as regressions. UP017 asks for
#: ``datetime.UTC`` in place of ``timezone.utc`` — the very spelling the
#: contract mandates.
EXPECTED_LINT = ["UP017"]

#: What each binding form resolves to, and what it implies about imports.
_CLASS_BINDING = "datetime.datetime"  # from datetime import datetime [as d]
_MODULE_BINDING = "datetime"  # import datetime [as dt]


class ConvertUtcnowCommand(VisitorBasedCodemodCommand):
    """Rewrite every resolved ``datetime.utcnow()`` call, whatever its spelling."""

    DESCRIPTION = "Replace datetime.utcnow() with datetime.now(timezone.utc)."

    def __init__(self, context) -> None:
        super().__init__(context)
        self.bindings: dict[str, str] = {}
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
                AddImportsVisitor.add_needed_import(self.context, "datetime", "timezone")
        return tree

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        flattened = dotted_path(updated_node.func)
        if flattened is None or updated_node.args:
            # utcnow() takes no arguments; anything with args is not our target.
            return updated_node
        head, attributes = flattened
        base = self.bindings.get(head.value)
        if base is None:
            return updated_node
        if ".".join([base, *attributes]) != TARGET:
            return updated_node

        # `.with_changes(attr=...)` keeps the receiver node untouched, so
        # whitespace, comments and the original spelling all survive (FR-5).
        new_func = updated_node.func.with_changes(attr=cst.Name("now"))

        if base == _CLASS_BINDING:
            # `datetime` here is the class; timezone has to be imported.
            self.needs_timezone = True
            timezone = cst.Attribute(value=cst.Name("timezone"), attr=cst.Name("utc"))
        elif base == _MODULE_BINDING:
            # `dt.timezone` rides the import that is already there.
            timezone = cst.Attribute(
                value=cst.Attribute(value=cst.Name(head.value), attr=cst.Name("timezone")),
                attr=cst.Name("utc"),
            )
        else:  # pragma: no cover - TARGET only resolves through the two above
            return updated_node

        self.edits.append(f"{head.value}.{'.'.join(attributes)} -> now(...)")
        return updated_node.with_changes(func=new_func, args=[cst.Arg(value=timezone)])


class _InsertTimezone(cst.CSTTransformer):
    """Add ``timezone`` to the first ``from datetime import ...`` binding the class.

    Inserted before the first name that sorts after it; the other names, their
    order and their commas are left exactly as written.
    """

    def __init__(self) -> None:
        self.done = False

    def leave_ImportFrom(self, original_node: cst.ImportFrom,
                         updated_node: cst.ImportFrom) -> cst.ImportFrom:
        names = updated_node.names
        if (self.done or isinstance(names, cst.ImportStar) or updated_node.relative
                or updated_node.module is None
                or cst.Module([]).code_for_node(updated_node.module) != "datetime"
                or not any(alias.evaluated_name == "datetime" for alias in names)):
            return updated_node
        self.done = True
        names = list(names)
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
        return updated_node.with_changes(names=names)
