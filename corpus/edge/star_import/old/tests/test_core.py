from pkg.core import stamp
from pkg.legacy import old


def test_both() -> None:
    assert stamp().year >= 2020 and old().year >= 2020
