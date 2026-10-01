"""Generate the edge-case corpus: ``python corpus/edge/_build.py``.

Every case is a tiny repo under ``<case>/old`` with a passing pre-migration
suite (unless the case is about the suite failing), a hand-written
``ground_truth.json`` and a ``case.json`` holding the expected verdict.

Ground-truth sites are located by searching for the literal call text a case
names — never by running the analyzer, so the expectation cannot inherit the
analyzer's blind spots. ``gold/`` holds byte-exact expected files for the cases
that are about bytes (CRLF, tabs, encoding).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
UTCNOW = "datetime.datetime.utcnow"
UTCFROMTS = "datetime.datetime.utcfromtimestamp"

PYPROJECT = """[project]
name = "pkg"
version = "0.1.0"
requires-python = "==3.12.*"

[tool.pytest.ini_options]
testpaths = ["tests"]
"""

CASES: list[dict] = []


def case(name: str, category: str, expect: str, files: dict[str, str | bytes],
         sites: list[tuple[str, str, int] | tuple[str, str, int, str]], *, code: str = "",
         evidence: str = "", mode: str = "deterministic", env: dict | None = None,
         gold: dict[str, str | bytes] | None = None, note: str = "") -> None:
    """``sites``: (file, call text, occurrence[, symbol]) — the call text's first char is the col."""
    CASES.append(dict(name=name, category=category, expect=expect, files=files, sites=sites,
                      code=code, evidence=evidence, mode=mode, env=env or {}, gold=gold or {},
                      note=note))


def _text(content: str | bytes) -> str:
    if isinstance(content, str):
        return content
    return content.decode("latin-1") if b"coding: latin-1" in content else content.decode()


def locate(files: dict[str, str | bytes], file: str, needle: str, nth: int,
           symbol: str = UTCNOW) -> dict:
    text = _text(files[file])
    index = -1
    for _ in range(nth + 1):
        index = text.index(needle, index + 1)
    before = text[:index]
    line = before.count("\n") + 1
    col = index - (before.rfind("\n") + 1)
    return {"file": file, "line": line, "col": col, "symbol": symbol, "kind": "call"}


# -- shared snippets ----------------------------------------------------------

CORE = '''from datetime import datetime


def stamp() -> datetime:
    return datetime.utcnow()
'''
TEST_CORE = '''from pkg.core import stamp


def test_stamp_is_recent() -> None:
    assert stamp().year >= 2020
'''


def simple(extra: dict[str, str | bytes] | None = None) -> dict[str, str | bytes]:
    return {"src/pkg/__init__.py": "", "src/pkg/core.py": CORE,
            "tests/test_core.py": TEST_CORE, **(extra or {})}


CORE_SITE = ("src/pkg/core.py", "datetime.utcnow()", 0)

# -- COMMON -----------------------------------------------------------------------

case("from_import", "common", "GREEN", simple(), [CORE_SITE])

case("module_import", "common", "GREEN", {
    "src/pkg/__init__.py": "",
    "src/pkg/core.py": "import datetime\n\n\ndef stamp():\n    return datetime.datetime.utcnow()\n",
    "tests/test_core.py": TEST_CORE,
}, [("src/pkg/core.py", "datetime.datetime.utcnow()", 0)])

case("aliased_module", "common", "GREEN", {
    "src/pkg/__init__.py": "",
    "src/pkg/core.py": "import datetime as dt\n\n\ndef stamp():\n    return dt.datetime.utcnow()\n",
    "tests/test_core.py": TEST_CORE,
}, [("src/pkg/core.py", "dt.datetime.utcnow()", 0)])

case("aliased_class", "common", "GREEN", {
    "src/pkg/__init__.py": "",
    "src/pkg/core.py": "from datetime import datetime as DT\n\n\ndef stamp():\n"
                       "    return DT.utcnow()\n",
    "tests/test_core.py": TEST_CORE,
}, [("src/pkg/core.py", "DT.utcnow()", 0)])

MULTI = '''from datetime import datetime, timedelta


def stamp():
    return datetime.utcnow()


def window():
    start = datetime.utcnow()
    return start, start + timedelta(hours=1), datetime.utcnow()


def ages(values):
    return [datetime.utcnow() - v for v in values]
'''
case("multi_site_one_file", "common", "GREEN", {
    "src/pkg/__init__.py": "", "src/pkg/core.py": MULTI,
    "tests/test_core.py": "from pkg.core import ages, stamp, window\n\n\n"
                          "def test_all() -> None:\n    assert stamp().year >= 2020\n"
                          "    start, end, now = window()\n    assert end > start\n"
                          "    assert ages([stamp()])[0].total_seconds() >= 0\n",
}, [("src/pkg/core.py", "datetime.utcnow()", i) for i in range(4)])

MANY = {f"src/pkg/m{i}.py": f"from datetime import datetime\n\n\ndef t{i}():\n"
                            "    return datetime.utcnow()\n" for i in range(6)}
case("sites_across_six_files", "common", "GREEN", {
    "src/pkg/__init__.py": "", **MANY,
    "tests/test_many.py": "".join(f"from pkg.m{i} import t{i}\n" for i in range(6))
    + "\n\ndef test_all() -> None:\n"
    + "".join(f"    assert t{i}().year >= 2020\n" for i in range(6)),
}, [(f"src/pkg/m{i}.py", "datetime.utcnow()", 0) for i in range(6)])

# report.py subtracts its own naive utcnow() from core's value: once core is
# migrated (batch 0) and report is not, the suite breaks across the files.
CROSS = {
    "src/pkg/__init__.py": "",
    "src/pkg/core.py": CORE,
    "src/pkg/report.py": "from datetime import datetime\n\nfrom pkg.core import stamp\n\n\n"
                         "def age_seconds():\n    return (datetime.utcnow() - stamp())"
                         ".total_seconds()\n",
    "tests/test_core.py": TEST_CORE,
    "tests/test_report.py": "from pkg.report import age_seconds\n\n\n"
                            "def test_age_is_small() -> None:\n"
                            "    assert -5 < age_seconds() < 5\n",
}
CROSS_SITES = [CORE_SITE, ("src/pkg/report.py", "datetime.utcnow()", 0)]
case("cross_file_recovery", "common", "GREEN", CROSS, CROSS_SITES,
     note="core moves first; report breaks until CORRECT migrates it")

case("cross_file_recovery_llm", "common", "GREEN", CROSS, CROSS_SITES, mode="llm-fake",
     note="same break, repaired by the LLM corrector through FakeProvider (offline)")

case("import_cycle", "common", "GREEN", {
    "src/pkg/__init__.py": "",
    "src/pkg/a.py": "from datetime import datetime\n\nimport pkg.b\n\n\ndef a_now():\n"
                    "    return datetime.utcnow()\n\n\ndef a_age():\n"
                    "    return (pkg.b.b_now() - a_now()).total_seconds()\n",
    "src/pkg/b.py": "from datetime import datetime\n\nimport pkg.a\n\n\ndef b_now():\n"
                    "    return datetime.utcnow()\n\n\ndef b_age():\n"
                    "    return (pkg.a.a_now() - b_now()).total_seconds()\n",
    "tests/test_cycle.py": "from pkg.a import a_age\nfrom pkg.b import b_age\n\n\n"
                           "def test_cycle() -> None:\n    assert abs(a_age()) < 5\n"
                           "    assert abs(b_age()) < 5\n",
}, [("src/pkg/a.py", "datetime.utcnow()", 0), ("src/pkg/b.py", "datetime.utcnow()", 0)])

case("utcfromtimestamp_alongside_utcnow", "common", "GREEN", {
    "src/pkg/__init__.py": "",
    "src/pkg/core.py": "from datetime import datetime\n\n\ndef stamp():\n"
                       "    return datetime.utcnow()\n\n\ndef from_epoch(t):\n"
                       "    return datetime.utcfromtimestamp(t)\n",
    "tests/test_core.py": "from pkg.core import from_epoch, stamp\n\n\n"
                          "def test_both() -> None:\n    assert stamp().year >= 2020\n"
                          "    assert from_epoch(0).year == 1970\n",
}, [CORE_SITE, ("src/pkg/core.py", "datetime.utcfromtimestamp(t)", 0, UTCFROMTS)])

# -- RARE -------------------------------------------------------------------------


def one(name: str, source: str, test: str, needles: list[tuple[str, int]], **kw) -> None:
    case(name, "rare", kw.pop("expect", "GREEN"),
         {"src/pkg/__init__.py": "", "src/pkg/core.py": source, "tests/test_core.py": test},
         [("src/pkg/core.py", n, i) for n, i in needles], **kw)


one("default_argument",
    "from datetime import datetime\n\n\ndef stamp(t=datetime.utcnow()):\n    return t\n",
    "from pkg.core import stamp\n\n\ndef test_default() -> None:\n"
    "    assert stamp().year >= 2020\n", [("datetime.utcnow()", 0)])
one("inside_lambda",
    "from datetime import datetime\n\nstamp = lambda: datetime.utcnow()  # noqa: E731\n",
    TEST_CORE, [("datetime.utcnow()", 0)])
one("inside_fstring",
    "from datetime import datetime\n\n\ndef label():\n    return f\"at {datetime.utcnow():%Y}\"\n",
    "from pkg.core import label\n\n\ndef test_label() -> None:\n"
    "    assert label().startswith(\"at 20\")\n", [("datetime.utcnow()", 0)])
one("inside_decorator_argument",
    "from datetime import datetime\n\n\ndef tagged(when):\n    def wrap(f):\n"
    "        f.when = when\n        return f\n    return wrap\n\n\n"
    "@tagged(datetime.utcnow())\ndef job():\n    return 1\n",
    "from pkg.core import job\n\n\ndef test_job() -> None:\n"
    "    assert job() == 1 and job.when.year >= 2020\n", [("datetime.utcnow()", 0)])
one("class_body_and_classmethod",
    "from datetime import datetime\n\n\nclass Clock:\n    created = datetime.utcnow()\n\n"
    "    @classmethod\n    def now(cls):\n        return datetime.utcnow()\n",
    "from pkg.core import Clock\n\n\ndef test_clock() -> None:\n"
    "    assert Clock.created.year >= 2020 and Clock.now() >= Clock.created\n",
    [("datetime.utcnow()", 0), ("datetime.utcnow()", 1)])
one("conditional_import",
    "try:\n    from datetime import UTC, datetime\nexcept ImportError:  # Python < 3.11\n"
    "    from datetime import datetime\n\n    UTC = None\n\n\ndef stamp():\n"
    "    return datetime.utcnow()\n", TEST_CORE, [("datetime.utcnow()", 0)])

case("reexport_through_init", "rare", "GREEN", {
    "src/pkg/__init__.py": "from datetime import datetime\n",
    "src/pkg/core.py": "from pkg import datetime\n\n\ndef stamp():\n"
                       "    return datetime.utcnow()\n",
    "tests/test_core.py": TEST_CORE,
}, [CORE_SITE], note="`datetime` reaches core.py through the package's re-export")

case("relative_imports", "rare", "GREEN", {
    "src/pkg/__init__.py": "",
    "src/pkg/compat.py": "from datetime import datetime\n",
    "src/pkg/core.py": "from .compat import datetime\n\n\ndef stamp():\n"
                       "    return datetime.utcnow()\n",
    "src/pkg/report.py": "from datetime import datetime\n\nfrom .core import stamp\n\n\n"
                         "def age():\n    return (datetime.utcnow() - stamp()).total_seconds()\n",
    "tests/test_core.py": TEST_CORE,
    "tests/test_report.py": "from pkg.report import age\n\n\ndef test_age() -> None:\n"
                            "    assert abs(age()) < 5\n",
}, [CORE_SITE, ("src/pkg/report.py", "datetime.utcnow()", 0)])

CRLF_OLD = CORE.replace("\n", "\r\n").encode()
CRLF_NEW = CORE.replace("import datetime", "import datetime, timezone").replace(
    "datetime.utcnow()", "datetime.now(timezone.utc)").replace("\n", "\r\n").encode()
case("crlf_line_endings", "rare", "GREEN", simple({"src/pkg/core.py": CRLF_OLD}), [CORE_SITE],
     gold={"src/pkg/core.py": CRLF_NEW}, note="CRLF must survive byte-exact")

TABS_OLD = "from datetime import datetime\n\n\ndef stamp():\n\tif True:\n\t\treturn datetime.utcnow()\n"
TABS_NEW = TABS_OLD.replace("import datetime", "import datetime, timezone").replace(
    "datetime.utcnow()", "datetime.now(timezone.utc)")
case("tab_indentation", "rare", "GREEN", simple({"src/pkg/core.py": TABS_OLD}), [
    ("src/pkg/core.py", "datetime.utcnow()", 0)], gold={"src/pkg/core.py": TABS_NEW})

LATIN = ("# -*- coding: latin-1 -*-\n\"\"\"Zeitstempel für Größen.\"\"\"\nfrom datetime import "
         "datetime\n\ngröße = \"maß\"\n\n\ndef stamp():\n    return datetime.utcnow()\n")
LATIN_NEW = LATIN.replace("import datetime\n", "import datetime, timezone\n").replace(
    "datetime.utcnow()", "datetime.now(timezone.utc)")
case("encoding_cookie_non_ascii", "rare", "GREEN",
     simple({"src/pkg/core.py": LATIN.encode("latin-1")}), [CORE_SITE],
     gold={"src/pkg/core.py": LATIN_NEW.encode("latin-1")},
     note="latin-1 source with a coding cookie and non-ASCII identifiers")

LONG = "from datetime import datetime\n\n\n" + "".join(
    f"def f{i}(x):\n    return x + {i}\n\n\n" for i in range(1300)) + \
    "def stamp():\n    return datetime.utcnow()\n\n\ndef later():\n    return datetime.utcnow()\n"
case("very_long_file", "rare", "GREEN", simple({
    "src/pkg/core.py": LONG,
    "tests/test_core.py": "from pkg.core import later, stamp\n\n\ndef test_long() -> None:\n"
                          "    assert stamp().year >= 2020 and later().year >= 2020\n"}),
     [("src/pkg/core.py", "datetime.utcnow()", 0), ("src/pkg/core.py", "datetime.utcnow()", 1)],
     note=f"{LONG.count(chr(10))} lines")

# -- TWISTED / ADVERSARIAL ----------------------------------------------------------

one("utcnow_in_strings_comments_docstrings",
    "\"\"\"Replaces datetime.utcnow() one day.\"\"\"\nfrom datetime import datetime\n\n"
    "HELP = \"call datetime.utcnow() for the time\"\n\n\ndef stamp():\n"
    "    \"\"\"Like datetime.utcnow(), but tested.\"\"\"\n"
    "    # datetime.utcnow() is deprecated\n    return datetime.utcnow()\n",
    "from pkg.core import HELP, stamp\n\n\ndef test_text_untouched() -> None:\n"
    "    assert \"datetime.utcnow()\" in HELP and stamp().year >= 2020\n",
    [("return datetime.utcnow()", 0)], note="only the real call may change")
CASES[-1]["sites"] = [("src/pkg/core.py", "datetime.utcnow()", 4)]

one("other_object_with_utcnow",
    "from datetime import datetime\n\n\nclass Clock:\n    def utcnow(self):\n"
    "        return 42\n\n\nclock = Clock()\n\n\ndef fake():\n    return clock.utcnow()\n\n\n"
    "def stamp():\n    return datetime.utcnow()\n",
    "from pkg.core import fake, stamp\n\n\ndef test_both() -> None:\n"
    "    assert fake() == 42 and stamp().year >= 2020\n", [("datetime.utcnow()", 0)])

one("shadowed_local_name",
    "from datetime import datetime\n\n\nclass FakeClock:\n    def utcnow(self):\n"
    "        return 7\n\n\ndef fake():\n    datetime = FakeClock()\n"
    "    return datetime.utcnow()\n\n\ndef stamp():\n    return datetime.utcnow()\n",
    "from pkg.core import fake, stamp\n\n\ndef test_both() -> None:\n"
    "    assert fake() == 7 and stamp().year >= 2020\n", [("datetime.utcnow()", 1)])

case("already_migrated", "twisted", "GREEN", simple({
    "src/pkg/core.py": "from datetime import datetime, timezone\n\n\ndef stamp():\n"
                       "    return datetime.now(timezone.utc)\n"}), [],
     note="idempotence: zero edits, empty patch")

case("half_migrated", "twisted", "GREEN", {
    "src/pkg/__init__.py": "",
    "src/pkg/core.py": "from datetime import datetime, timezone\n\n\ndef stamp():\n"
                       "    return datetime.now(timezone.utc)\n\n\ndef legacy():\n"
                       "    return datetime.utcnow()\n",
    "src/pkg/done.py": "from datetime import datetime, timezone\n\n\ndef ok():\n"
                       "    return datetime.now(timezone.utc)\n",
    "tests/test_core.py": "from pkg.core import legacy, stamp\nfrom pkg.done import ok\n\n\n"
                          "def test_all() -> None:\n    assert legacy().year >= 2020\n"
                          "    assert stamp().year >= 2020 and ok().year >= 2020\n",
}, [("src/pkg/core.py", "datetime.utcnow()", 0)])

one("bare_reference", "from datetime import datetime\n\nclock = datetime.utcnow\n\n\n"
    "def stamp():\n    return datetime.utcnow()\n",
    "from pkg.core import clock, stamp\n\n\ndef test_both() -> None:\n"
    "    assert clock().year >= 2020 and stamp().year >= 2020\n",
    [("datetime.utcnow()", 0)], expect="YELLOW", code="residual",
    evidence="bare-reference", note="known gap: a reference is not a call")
CASES[-1]["category"] = "twisted"

case("star_import", "twisted", "YELLOW", {
    "src/pkg/__init__.py": "", "src/pkg/core.py": CORE,
    "src/pkg/legacy.py": "from datetime import *  # noqa: F403\n\n\ndef old():\n"
                         "    return datetime.utcnow()  # noqa: F405\n",
    "tests/test_core.py": "from pkg.core import stamp\nfrom pkg.legacy import old\n\n\n"
                          "def test_both() -> None:\n"
                          "    assert stamp().year >= 2020 and old().year >= 2020\n",
}, [CORE_SITE], code="residual", evidence="star-import",
     note="known gap: names behind a star import are not resolved")

case("deprecated_call_in_test_file", "twisted", "YELLOW", simple({
    "tests/test_core.py": "from datetime import datetime\n\nfrom pkg.core import stamp\n\n\n"
                          "def test_close_to_now() -> None:\n"
                          "    assert abs((stamp().replace(tzinfo=None) - datetime.utcnow())"
                          ".total_seconds()) < 5\n"}),
     [CORE_SITE], code="residual", evidence="tests/test_core.py",
     note="the test oracle is never edited; its own deprecated call is reported")

case("syntax_error_file", "twisted", "YELLOW", simple({
    "src/pkg/broken.py": "def oops(:\n    return datetime.utcnow()\n"}),
     [CORE_SITE], code="unparseable", evidence="src/pkg/broken.py",
     note="skipped and reported; core.py still migrated")

case("empty_and_comment_only_files", "twisted", "GREEN", simple({
    "src/pkg/empty.py": "", "src/pkg/notes.py": "# nothing here\n# datetime.utcnow()\n"}),
     [CORE_SITE])

# -- FAILURE PATHS ----------------------------------------------------------------------

case("pre_suite_failing", "failure", "RED", simple({
    "tests/test_core.py": TEST_CORE + "\n\ndef test_already_broken() -> None:\n"
                                      "    assert 1 == 2\n"}),
     [CORE_SITE], code="precondition", note="NB-10: refuse to migrate")

case("zero_tests", "failure", "RED", simple({"tests/test_core.py": "# no tests yet\n"}),
     [CORE_SITE], code="precondition")

case("test_needs_network", "failure", "RED", simple({
    "tests/test_core.py": TEST_CORE + "\n\ndef test_fetch() -> None:\n    import socket\n\n"
                                      "    socket.getaddrinfo(\"example.com\", 80)\n"}),
     [CORE_SITE], code="precondition", evidence="network")

case("edit_causes_infinite_loop", "failure", "RED", {
    "src/pkg/__init__.py": "",
    "src/pkg/core.py": "from datetime import datetime\n\n\ndef wait_for(deadline):\n"
                       "    while True:\n        try:\n"
                       "            if datetime.utcnow() >= deadline:\n                return\n"
                       "        except TypeError:  # aware vs naive: retries forever\n"
                       "            continue\n",
    "tests/test_core.py": "from datetime import datetime as D\n\nfrom pkg.core import wait_for\n\n\n"
                          "def test_wait() -> None:\n    wait_for(D(2000, 1, 1))\n",
}, [("src/pkg/core.py", "datetime.utcnow()", 0)], code="suite_red", evidence="Timeout",
     env={"MRA_PYTEST_TIMEOUT_SEC": "8", "MRA_MAX_FIX_ATTEMPTS": "1"})

case("unfixable_break", "failure", "RED", simple({
    "tests/test_core.py": "from pkg.core import stamp\n\n\ndef test_naive_contract() -> None:\n"
                          "    assert stamp().tzinfo is None\n"}),
     [CORE_SITE], code="gave_up", note="the oracle pins naive datetimes; nothing can fix it")

case("provider_unreachable", "failure", "RED", CROSS, CROSS_SITES, mode="llm-unreachable",
     code="provider", evidence="unreachable")

case("local_only_with_remote_providers", "failure", "RED", simple(), [CORE_SITE],
     mode="llm-remote", env={"MRA_PRIVACY": "local-only"}, code="refused",
     evidence="local-only")


def build() -> None:
    for old in HERE.glob("*/case.json"):
        shutil.rmtree(old.parent)
    for spec in CASES:
        root = HERE / spec["name"]
        files = {"pyproject.toml": PYPROJECT, **spec["files"]}
        for rel, content in files.items():
            path = root / "old" / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content if isinstance(content, bytes) else content.encode())
        for rel, content in spec["gold"].items():
            path = root / "gold" / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content if isinstance(content, bytes) else content.encode())
        truth = {
            "task_id": spec["name"],
            "source_api": "datetime.utcnow",
            "target_api": "datetime.now(timezone.utc)",
            "call_sites": [locate(spec["files"], *site) for site in spec["sites"]],
        }
        (root / "ground_truth.json").write_text(json.dumps(truth, indent=2) + "\n")
        meta = {k: spec[k] for k in ("category", "expect", "code", "evidence", "mode", "env",
                                     "note")}
        meta["gold"] = sorted(spec["gold"])
        (root / "case.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"{len(CASES)} cases written under {HERE}")


if __name__ == "__main__":
    build()
