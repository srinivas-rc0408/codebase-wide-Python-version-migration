"""The edge-case accuracy suite (corpus/edge) as tests: one per case.

The suite runs once per session, in parallel processes, into a temporary
directory — corpus/edge/RESULTS.md is only rewritten by
``python -m mra.benchmark.edge``. Each case asserts the verdict, the reason
code behind it, and for byte-level cases a byte-exact match with gold/.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

from mra.benchmark.edge import cases, held_out, run_suite


def _docker_ok() -> bool:
    try:
        return (
            subprocess.run(
                ["docker", "image", "inspect", "mra-sandbox:py312"],
                capture_output=True,
                check=False,
            ).returncode
            == 0
        )
    except FileNotFoundError:
        return False


pytestmark = pytest.mark.skipif(not _docker_ok(), reason="needs docker + mra-sandbox:py312")

CASES = [path.name for path in cases()]


@pytest.fixture(scope="session")
def edge_results(tmp_path_factory: pytest.TempPathFactory) -> dict[str, dict[str, Any]]:
    results = run_suite(runs_dir=Path(tmp_path_factory.mktemp("edge")))
    return {row["case"]: row for row in results["cases"]}


def test_every_category_is_covered() -> None:
    import json

    categories = {json.loads((p / "case.json").read_text())["category"] for p in cases()}
    assert categories == {"common", "rare", "twisted", "failure"}
    assert len(CASES) >= 39


@pytest.mark.parametrize("case", CASES)
def test_case_gives_the_expected_verdict(
    case: str, edge_results: dict[str, dict[str, Any]]
) -> None:
    row = edge_results[case]
    assert row["pass"], f"{case}: {'; '.join(row['problems'])} (reasons: {row['reasons']})"


def test_held_out_never_includes_a_training_case() -> None:
    from mra.benchmark.runner import train_tasks

    train = {t.name for t in train_tasks()}
    names = {c.name for c in held_out()}
    assert train and names
    assert not names & train
    assert len(names) + len(train) == len(cases())
