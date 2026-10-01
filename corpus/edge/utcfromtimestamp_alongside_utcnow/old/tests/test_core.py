from pkg.core import from_epoch, stamp


def test_both() -> None:
    assert stamp().year >= 2020
    assert from_epoch(0).year == 1970
