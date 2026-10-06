"""Consequence repair (v0.3.0): CORRECT when no residual call site is left.

task06_scheduler is the fixture: the codemod migrates both call sites, and the
suite still breaks in report.py because config.EPOCH is a naive constant. The
model is asked for a patch scoped to the traced files and their migrated
neighbours, and an anti-reversal guard rejects any patch that undoes the
migration. Offline throughout: FakeProvider stands in for the model.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import pytest

from mra.analysis import call_sites as call_sites_module
from mra.codemods.datetime_utcnow import TARGET, family
from mra.models import ROLES, Endpoint, Router
from mra.models.providers import FakeProvider
from mra.nodes.correct_node import LLMCorrector, consequence_scope
from mra.nodes.edit_node import apply_codemod
from mra.recovery import DEFAULT_MAX_FIX_ATTEMPTS, recover

TASK = Path(__file__).resolve().parents[1] / "corpus" / "blind" / "task06_scheduler"
CONTRACT = {
    "task_id": "task06_scheduler",
    "source_api": "datetime.utcnow",
    "target_api": "datetime.now(timezone.utc)",
}
FAILURE = {
    "nodeid": "tests/test_report.py::test_age_days_is_non_negative_int",
    "signature": "0be79751c957972b",
    "exc_type": "TypeError",
    "message": "TypeError: can't subtract offset-naive and offset-aware datetimes",
    "file": "src/app/report.py",
    "line": 7,
    "trace": (
        ">       days = age_days()\n\ntests/test_report.py:5: \n"
        ">       return (clock.now() - config.EPOCH).days\n"
        "E       TypeError: can't subtract offset-naive and offset-aware datetimes\n\n"
        "src/app/report.py:7: TypeError"
    ),
}
REPORT_PY = "src/app/report.py"
CONFIG_PY = "src/app/config.py"
TZ_STRIPPED = (
    (TASK / "old" / REPORT_PY)
    .read_text()
    .replace("clock.now() - config.EPOCH", "clock.now().replace(tzinfo=None) - config.EPOCH")
)


@pytest.fixture
def migrated(tmp_path: Path) -> tuple[Path, dict[str, Any]]:
    """task06 after EDIT: both call sites migrated, report.py broken."""
    work = tmp_path / "repo"
    shutil.copytree(TASK / "old", work)
    sites = call_sites_module.find_in_repo(work, family(TARGET))
    apply_codemod(work, sites)
    assert call_sites_module.find_in_repo(work, family(TARGET)) == {}
    return work, {"call_sites": sites}


def corrector_replying(patch: str) -> tuple[LLMCorrector, list[str]]:
    """An LLMCorrector whose model answers every patch request with ``patch``."""
    asked: list[str] = []

    def reply(messages: list[dict[str, str]], model: str) -> str:
        if "one word" in messages[0]["content"]:
            return "behaviour"
        asked.append(messages[-1]["content"])
        return patch

    router = Router(roles={r: [Endpoint(FakeProvider("fake", reply=reply), "m")] for r in ROLES})
    return LLMCorrector(router, TARGET, CONTRACT), asked


def fenced(file: str, source: str) -> str:
    return f"FILE: {file}\n```python\n{source}```\n"


def test_scope_is_the_traced_file_plus_its_migrated_neighbours(migrated) -> None:
    work, context = migrated
    assert consequence_scope(work, FAILURE, set(context["call_sites"])) == [
        "src/app/clock.py",
        CONFIG_PY,
        REPORT_PY,
    ]


def test_a_the_right_fix_is_accepted(migrated) -> None:
    """No residual site, yet the model is asked, and the EPOCH fix lands."""
    work, context = migrated
    gold = (TASK / "gold" / CONFIG_PY).read_text()
    corrector, asked = corrector_replying(fenced(CONFIG_PY, gold))

    assert corrector(work, FAILURE, context) == [CONFIG_PY]
    assert (work / CONFIG_PY).read_text() == gold
    assert len(asked) == 1 and f"FILE: {REPORT_PY}" in asked[0] and "FILE: tests/" not in asked[0]
    assert corrector.log[-1]["mode"] == "consequence"


def test_b_a_tz_stripping_fix_is_rejected(migrated) -> None:
    work, context = migrated
    before = (work / REPORT_PY).read_text()
    corrector, asked = corrector_replying(fenced(REPORT_PY, TZ_STRIPPED))

    assert corrector(work, FAILURE, context) == []
    assert (work / REPORT_PY).read_text() == before
    assert len(asked) == 1  # the model was asked; its patch was refused
    assert "forbidden pattern" in corrector.log[-1]["rejected"]


def test_b_reintroducing_the_source_api_is_rejected(migrated) -> None:
    work, context = migrated
    before = (work / "src/app/clock.py").read_text()
    corrector, _ = corrector_replying(
        fenced("src/app/clock.py", (TASK / "old" / "src/app/clock.py").read_text())
    )

    assert corrector(work, FAILURE, context) == []
    assert (work / "src/app/clock.py").read_text() == before
    assert "reintroduces" in corrector.log[-1]["rejected"]


@pytest.mark.parametrize("file", ["src/app/decoys.py", "tests/test_report.py"])
def test_c_edits_outside_scope_are_rejected(migrated, file: str) -> None:
    work, context = migrated
    before = (work / file).read_text()
    corrector, _ = corrector_replying(fenced(file, before + "\nX = 1\n"))

    assert corrector(work, FAILURE, context) == []
    assert (work / file).read_text() == before
    assert "outside scope" in corrector.log[-1]["rejected"]


class AlwaysRed:
    """A runner whose suite never goes green, with no sandbox behind it."""

    def __init__(self) -> None:
        self.runs = 0

    def run(self, repo: Path, **_: Any) -> dict[str, Any]:
        self.runs += 1
        return {"total": 8, "passed": 7, "failed": 1, "errors": 0, "failures": [FAILURE]}


class Events:
    def __init__(self) -> None:
        self.events: list[tuple[str, str, dict[str, Any]]] = []

    def record(self, node: str, action: str, **detail: Any) -> None:
        self.events.append((node, action, detail))


def test_d_rejected_patches_count_and_the_cap_still_holds(migrated) -> None:
    """Every rejected patch spends an attempt; the loop stops at exactly the cap."""
    work, context = migrated
    corrector, asked = corrector_replying(fenced(REPORT_PY, TZ_STRIPPED))
    runner = AlwaysRed()

    result = recover(
        work,
        runner.run(work),
        runner=runner,
        corrector=corrector,
        task_id="task06_scheduler",
        trajectory=Events(),
        context=context,
    )

    assert result["outcome"] == "gave_up"
    assert result["rounds"] == DEFAULT_MAX_FIX_ATTEMPTS == 3
    assert len(asked) == 3
    assert all(c["changed"] == [] for c in result["corrections"])
    assert all("forbidden pattern" in c["rejected"] for c in result["corrections"])
    assert "replace(tzinfo=None)" not in (work / REPORT_PY).read_text()
