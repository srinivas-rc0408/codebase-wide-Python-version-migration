"""Find every call to a target symbol, whatever spelling the file uses.

This is FR-1, and the import resolution is the whole point. The same function
reaches the source three ways:

    from datetime import datetime  ->  datetime.utcnow()
    import datetime               ->  datetime.datetime.utcnow()
    import datetime as dt         ->  dt.datetime.utcnow()

A matcher written against one spelling scores zero on the others, and a regex
scores zero on all but the first. So every call is flattened to a dotted path,
its head is resolved through the module's own import bindings, and the result
is compared against one fully-qualified target. All three spellings above
resolve to ``datetime.datetime.utcnow``.

Two more ways a name reaches a module are resolved too, because real repos use
them: a relative import (``from .compat import datetime``) is anchored at the
importing file's package, and a name re-exported by another in-repo module
(``from pkg import datetime`` where ``pkg/__init__.py`` imported it) is
followed to what that module bound. Files that do not parse are skipped, not
fatal; sources are read as bytes so an encoding cookie is honoured.
"""

from __future__ import annotations

from collections.abc import Collection
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import libcst as cst
from libcst.metadata import ImportAssignment, MetadataWrapper, PositionProvider, ScopeProvider

from mra.analysis.dep_graph import module_index, python_files

#: module dotted name -> {name it binds by import -> fully-qualified target}
Exports = dict[str, dict[str, str]]


@dataclass(frozen=True)
class CallSite:
    """One located call, in the ``mra:call_site`` shape (SRS §4.2)."""

    file: str
    line: int
    col: int
    symbol: str
    kind: str = "call"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def dotted_path(node: cst.BaseExpression) -> tuple[cst.Name, list[str]] | None:
    """Flatten ``a.b.c`` into its head ``Name`` node and the attribute names after it.

    Returns None for anything that is not a plain dotted path — ``f().g()``,
    ``obj[0].g()``, a call on a literal — because those cannot be resolved
    statically through imports and must not be guessed at.
    """
    attributes: list[str] = []
    current = node
    while isinstance(current, cst.Attribute):
        attributes.append(current.attr.value)
        current = current.value
    if not isinstance(current, cst.Name):
        return None
    return current, list(reversed(attributes))


def _module_name(node: cst.BaseExpression) -> str:
    """Dotted text of an import's module expression (``a.b.c``)."""
    if isinstance(node, cst.Name):
        return node.value
    if isinstance(node, cst.Attribute):
        return f"{_module_name(node.value)}.{node.attr.value}"
    return ""


class ImportBindings(cst.CSTVisitor):
    """Maps each locally bound name to the fully-qualified thing it refers to.

    One implementation of the import rules, shared by the finder and the
    codemod — a second copy is how the two drift and the codemod edits a site
    the analyzer never reported.
    """

    def __init__(self, package: str = "") -> None:
        #: local name -> fully-qualified thing it is bound to
        self.bindings: dict[str, str] = {}
        #: this file's package, to anchor relative imports ("" = unknown)
        self.package = package

    def visit_Import(self, node: cst.Import) -> None:
        for alias in node.names:
            dotted = _module_name(alias.name)
            if not dotted:
                continue
            if alias.asname is not None:
                # `import a.b as x` binds x -> a.b
                self.bindings[str(alias.evaluated_alias)] = dotted
            else:
                # `import a.b` binds only the head package, a -> a
                head = dotted.split(".")[0]
                self.bindings[head] = head

    def visit_ImportFrom(self, node: cst.ImportFrom) -> None:
        if isinstance(node.names, cst.ImportStar):
            # A star import binds names we cannot see without importing the
            # module. Resolving it is out of scope; skipping it costs recall,
            # inventing bindings would cost precision.
            return
        module = _module_name(node.module) if node.module is not None else ""
        if node.relative:
            if not self.package:
                return  # cannot anchor `from . import x` without knowing where "." is
            parts = self.package.split(".")
            climb = len(node.relative) - 1
            if climb >= len(parts) + 1:
                return
            module = ".".join([*parts[: len(parts) - climb], *([module] if module else [])])
        for alias in node.names:
            name = str(alias.evaluated_name)
            binding = str(alias.evaluated_alias) if alias.asname is not None else name
            self.bindings[binding] = f"{module}.{name}" if module else name


def bindings_of(module: cst.Module, package: str = "") -> dict[str, str]:
    """Collect a whole module's import bindings up front."""
    collector = ImportBindings(package)
    module.visit(collector)
    return collector.bindings


def canonical(dotted: str, exports: Exports | None) -> str:
    """Follow re-exports: ``pkg.datetime`` -> ``datetime.datetime`` if pkg imported it."""
    for _ in range(8):  # re-export chains are short; a cycle must not spin
        parts = dotted.split(".")
        for i in range(len(parts) - 1, 0, -1):
            bound = (exports or {}).get(".".join(parts[:i]), {}).get(parts[i])
            if bound is not None:
                dotted = ".".join([bound, *parts[i + 1 :]])
                break
        else:
            return dotted
    return dotted


def is_test_path(path: str) -> bool:
    """True for anything that is part of the test oracle (NB-4)."""
    parts = Path(path).parts
    name = Path(path).name
    return (
        any(part in ("tests", "test") for part in parts)
        or name.startswith("test_")
        or name.endswith("_test.py")
        or name == "conftest.py"
    )


class _CallSiteVisitor(ImportBindings):
    """Resolves every dotted call against this module's import bindings."""

    METADATA_DEPENDENCIES = (PositionProvider, ScopeProvider)

    def __init__(
        self, targets: Collection[str], file: str, package: str = "", exports: Exports | None = None
    ) -> None:
        super().__init__(package)
        self.targets = set(targets)
        self.exports = exports
        self.file = file
        self.sites: list[CallSite] = []

    def _shadowed(self, head: cst.Name) -> bool:
        """True if ``head`` is bound by anything other than an import here.

        Guards precision: a local ``datetime = FakeClock()`` makes
        ``datetime.utcnow()`` a different function entirely, and editing it
        would be a wrong edit, not a missed one.
        """
        try:
            scope = self.get_metadata(ScopeProvider, head)
        except KeyError:
            return False  # no scope info; fall back to the binding pass
        if scope is None:
            return False
        assignments = list(scope[head.value])
        if not assignments:
            return False
        return not all(isinstance(a, ImportAssignment) for a in assignments)

    def visit_Call(self, node: cst.Call) -> None:
        flattened = dotted_path(node.func)
        if flattened is None:
            return
        head, attributes = flattened
        base = self.bindings.get(head.value)
        if base is None or self._shadowed(head):
            return
        resolved = canonical(".".join([base, *attributes]) if attributes else base, self.exports)
        if resolved not in self.targets:
            return
        position = self.get_metadata(PositionProvider, node).start
        self.sites.append(
            CallSite(file=self.file, line=position.line, col=position.column, symbol=resolved)
        )


def _targets(target: str | Collection[str]) -> set[str]:
    return {target} if isinstance(target, str) else set(target)


def find_in_source(
    source: str | bytes,
    target: str | Collection[str],
    file: str,
    package: str = "",
    exports: Exports | None = None,
) -> list[CallSite]:
    """Locate every call to ``target`` (one symbol or several) in one module's source."""
    wrapper = MetadataWrapper(cst.parse_module(source))
    visitor = _CallSiteVisitor(_targets(target), file, package, exports)
    wrapper.visit(visitor)
    return visitor.sites


def parse_repo(repo: Path | str) -> tuple[dict[Path, tuple[cst.Module, str]], list[str]]:
    """Every parseable file -> (module, package), plus the repo-relative files that do not parse."""
    repo = Path(repo)
    names = {path: name for name, path in module_index(repo).items()}
    parsed: dict[Path, tuple[cst.Module, str]] = {}
    unparseable: list[str] = []
    for path in python_files(repo):
        own = names.get(path, "")
        package = own if path.name == "__init__.py" else own.rpartition(".")[0]
        try:
            parsed[path] = (cst.parse_module(path.read_bytes()), package)
        except cst.ParserSyntaxError:
            unparseable.append(path.relative_to(repo).as_posix())
    return parsed, unparseable


def exports_of(repo: Path | str, parsed: dict[Path, tuple[cst.Module, str]]) -> Exports:
    """What each in-repo module binds by import — the names it re-exports."""
    return {
        name: bindings_of(parsed[path][0], parsed[path][1])
        for name, path in module_index(repo).items()
        if path in parsed
    }


def find_in_repo(
    repo: Path | str, target: str | Collection[str], files: list[Path] | None = None
) -> dict[str, list[dict[str, Any]]]:
    """Scan a repo for ``target`` and return the ``MigrationState.call_sites`` map.

    Shape is ``{repo-relative file: [call_site, ...]}`` (SRS §4.1). Files with
    no hit are omitted, so ``|A|`` is the sum of the list lengths. A file that
    does not parse holds no site this scan can see; the run report lists it.
    """
    repo = Path(repo)
    parsed, _ = parse_repo(repo)
    exports = exports_of(repo, parsed)
    targets = _targets(target)
    found: dict[str, list[dict[str, Any]]] = {}
    for path in files if files is not None else python_files(repo):
        if path not in parsed:
            continue
        module, package = parsed[path]
        relative = path.relative_to(repo).as_posix()
        visitor = _CallSiteVisitor(targets, relative, package, exports)
        MetadataWrapper(module).visit(visitor)
        if visitor.sites:
            found[relative] = [site.to_dict() for site in visitor.sites]
    return found
