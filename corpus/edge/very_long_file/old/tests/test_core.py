from pkg.core import later, stamp


def test_long() -> None:
    assert stamp().year >= 2020 and later().year >= 2020
