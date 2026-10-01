from pkg.core import clock, stamp


def test_both() -> None:
    assert clock().year >= 2020 and stamp().year >= 2020
