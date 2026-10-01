from pkg.core import stamp


def test_default() -> None:
    assert stamp().year >= 2020
