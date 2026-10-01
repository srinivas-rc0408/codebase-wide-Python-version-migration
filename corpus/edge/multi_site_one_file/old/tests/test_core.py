from pkg.core import ages, stamp, window


def test_all() -> None:
    assert stamp().year >= 2020
    start, end, now = window()
    assert end > start
    assert ages([stamp()])[0].total_seconds() >= 0
