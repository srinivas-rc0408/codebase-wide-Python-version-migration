"""P1 acceptance: the analyzer must score 100/100 on both corpus tasks.

task01 is the easy control. task02 is the one that matters: its two call sites
are spelled `datetime.datetime.utcnow()` and `dt.datetime.utcnow()`, so a
matcher built for task01's `datetime.utcnow()` — and any regex — scores zero.
Both must resolve to the same fully-qualified symbol.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from mra.analysis import analyze, build, find_in_source, flat_sites, to_state_adjacency
from mra.metrics import m1

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS = REPO_ROOT / "corpus" / "tierA"
TARGET = "datetime.datetime.utcnow"

#: Comparison key. Stricter than the resource pack's (file, line, symbol): a
#: column error would slip past that and break a position-based codemod later.
KEY_FIELDS = ("file", "line", "col", "symbol")


def _key(site: dict[str, Any]) -> tuple:
    return tuple(site[field] for field in KEY_FIELDS)


def _ground_truth(task: str) -> dict[str, Any]:
    return json.loads((CORPUS / task / "ground_truth.json").read_text())


@pytest.fixture(scope="session")
def analyses() -> dict[str, dict[str, Any]]:
    return {
        task: analyze(CORPUS / task / "old", TARGET)
        for task in ("task01_datetime", "task02_datetime_aliased")
    }


# -- call sites ------------------------------------------------------------


def test_task01_finds_the_single_from_import_site(analyses: dict[str, Any]) -> None:
    sites = flat_sites(analyses["task01_datetime"]["call_sites"])
    expected = _ground_truth("task01_datetime")["call_sites"]
    assert len(sites) == 1
    assert {_key(s) for s in sites} == {_key(s) for s in expected}
    assert sites[0]["symbol"] == TARGET
    assert sites[0]["kind"] == "call"


def test_task02_resolves_module_and_aliased_spellings(analyses: dict[str, Any]) -> None:
    """The alias test. Two spellings, one resolved symbol, exact positions."""
    call_sites = analyses["task02_datetime_aliased"]["call_sites"]
    sites = flat_sites(call_sites)
    expected = _ground_truth("task02_datetime_aliased")["call_sites"]

    assert len(sites) == 2
    assert set(call_sites) == {"src/pkg/core.py", "src/pkg/report.py"}
    assert {_key(s) for s in sites} == {_key(s) for s in expected}
    # Different spellings, identical FQN — that is what the resolver buys.
    assert {s["symbol"] for s in sites} == {TARGET}


@pytest.mark.parametrize(
    ("source", "reason"),
    [
        (
            "import datetime\n\nclass Clock:\n    def utcnow(self): ...\n\n"
            "clock = Clock()\nclock.utcnow()\n",
            "method on an unrelated object",
        ),
        (
            "from fakeclock import datetime\n\ndatetime.utcnow()\n",
            "same spelling, different module",
        ),
        (
            # Spelled exactly like the target: only the ScopeProvider shadow
            # check rejects this, the import-binding pass alone would match.
            "import datetime\n\ndatetime = object()\ndatetime.datetime.utcnow()\n",
            "import shadowed by a local rebinding",
        ),
        (
            "import datetime\n\ndatetime.datetime.now()\n",
            "sibling method on the right module",
        ),
    ],
)
def test_finder_does_not_match_lookalikes(source: str, reason: str) -> None:
    """False positives cost M1 precision and cause wrong edits, not missed ones."""
    assert find_in_source(source, TARGET, "x.py") == [], reason


@pytest.mark.parametrize(
    "source",
    [
        "from datetime import datetime\n\ndatetime.utcnow()\n",
        "import datetime\n\ndatetime.datetime.utcnow()\n",
        "import datetime as dt\n\ndt.datetime.utcnow()\n",
        "from datetime import datetime as d\n\nd.utcnow()\n",
    ],
)
def test_every_import_spelling_resolves_to_one_symbol(source: str) -> None:
    sites = find_in_source(source, TARGET, "x.py")
    assert len(sites) == 1
    assert sites[0].symbol == TARGET


# -- dependency graph ------------------------------------------------------


@pytest.mark.parametrize("task", ["task01_datetime", "task02_datetime_aliased"])
def test_dep_graph_has_the_cross_file_edge_and_nothing_spurious(task: str) -> None:
    graph = build(CORPUS / task / "old")
    assert graph.has_edge("src/pkg/report.py", "src/pkg/core.py")
    # Exact edge set: stdlib imports must not become edges, and neither may
    # anything the files do not actually import.
    assert set(graph.edges) == {
        ("src/pkg/report.py", "src/pkg/core.py"),
        ("tests/test_core.py", "src/pkg/core.py"),
        ("tests/test_report.py", "src/pkg/report.py"),
    }


@pytest.mark.parametrize("task", ["task01_datetime", "task02_datetime_aliased"])
def test_state_adjacency_is_importers_per_file(task: str) -> None:
    """SRS §4.1 defines dep_graph as file -> files that import it (predecessors)."""
    adjacency = to_state_adjacency(build(CORPUS / task / "old"))
    assert adjacency == {
        "src/pkg/core.py": ["src/pkg/report.py", "tests/test_core.py"],
        "src/pkg/report.py": ["tests/test_report.py"],
    }


# -- scoring ---------------------------------------------------------------


@pytest.mark.parametrize("task", ["task01_datetime", "task02_datetime_aliased"])
def test_m1_is_perfect_on_both_tasks(task: str, analyses: dict[str, Any]) -> None:
    """Recall 100 = missed nothing; precision 100 = matched nothing extra."""
    found = {_key(s) for s in flat_sites(analyses[task]["call_sites"])}
    truth = {_key(s) for s in _ground_truth(task)["call_sites"]}
    # At analysis time every found site is a claim; correctness is the overlap.
    score = m1(agent_sites=found, correct_sites=found, ground_truth_sites=truth)
    assert score["recall"] == 100.0
    assert score["precision"] == 100.0


def test_report_m1_comparison(analyses: dict[str, Any]) -> None:
    """Prints the analyzer-vs-ground-truth comparison. Run with `pytest -s` to read it."""
    for task, analysis in analyses.items():
        truth = _ground_truth(task)
        found = {_key(s) for s in flat_sites(analysis["call_sites"])}
        expected = {_key(s) for s in truth["call_sites"]}
        score = m1(agent_sites=found, correct_sites=found, ground_truth_sites=expected)

        print(f"\n=== {task} (difficulty: {truth['difficulty']}) ===")
        print(f"{'':2}{'source':10} {'file':20} {'line:col':9} symbol")
        for key in sorted(expected | found):
            file, line, col, symbol = key
            mark = "both" if key in expected & found else (
                "gt-only" if key in expected else "extra"
            )
            print(f"{'':2}{mark:10} {file:20} {f'{line}:{col}':9} {symbol}")
        print(f"{'':2}|A|={len(expected)}  found={len(found)}  "
              f"recall={score['recall']:.1f}%  precision={score['precision']:.1f}%  "
              f"f1={score['f1']:.1f}%")
        assert score["f1"] == 100.0


# -- resolution beyond one file's own imports (found by corpus/edge) ----------


def _repo(tmp_path: Path, files: dict[str, str | bytes]) -> Path:
    for rel, content in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode())
    return tmp_path


def _found(repo: Path, target: Any = TARGET) -> list[tuple[str, int]]:
    from mra.analysis import find_in_repo

    return sorted((s["file"], s["line"]) for sites in find_in_repo(repo, target).values()
                  for s in sites)


def test_reexport_through_package_init_resolves(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "src/pkg/__init__.py": "from datetime import datetime\n",
        "src/pkg/core.py": "from pkg import datetime\n\nx = datetime.utcnow()\n"})
    assert _found(repo) == [("src/pkg/core.py", 3)]


def test_relative_import_resolves_against_the_files_package(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "src/pkg/__init__.py": "",
        "src/pkg/compat.py": "from datetime import datetime\n",
        "src/pkg/core.py": "from .compat import datetime\n\nx = datetime.utcnow()\n"})
    assert _found(repo) == [("src/pkg/core.py", 3)]


def test_unparseable_and_latin1_files_do_not_crash_the_scan(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "src/pkg/__init__.py": "",
        "src/pkg/broken.py": "def oops(:\n",
        "src/pkg/latin.py": "# -*- coding: latin-1 -*-\ngröße = 1\nfrom datetime import "
                            "datetime\nx = datetime.utcnow()\n".encode("latin-1")})
    assert _found(repo) == [("src/pkg/latin.py", 4)]
    assert "src/pkg/broken.py" in build(repo).nodes


def test_map_never_puts_a_test_file_on_the_work_list(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "src/pkg/__init__.py": "",
        "src/pkg/core.py": "from datetime import datetime\nx = datetime.utcnow()\n",
        "tests/test_core.py": "from datetime import datetime\ny = datetime.utcnow()\n"})
    assert sorted(analyze(repo, TARGET)["call_sites"]) == ["src/pkg/core.py"]


def test_utcfromtimestamp_is_part_of_the_family(tmp_path: Path) -> None:
    from mra.codemods.datetime_utcnow import family

    repo = _repo(tmp_path, {"m.py": "from datetime import datetime\n"
                                    "a = datetime.utcnow()\nb = datetime.utcfromtimestamp(0)\n"})
    assert _found(repo, family(TARGET)) == [("m.py", 2), ("m.py", 3)]
