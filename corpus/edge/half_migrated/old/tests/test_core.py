from pkg.core import legacy, stamp
from pkg.done import ok


def test_all() -> None:
    assert legacy().year >= 2020
    assert stamp().year >= 2020 and ok().year >= 2020
