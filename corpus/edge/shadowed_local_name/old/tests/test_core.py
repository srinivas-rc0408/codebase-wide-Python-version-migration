from pkg.core import fake, stamp


def test_both() -> None:
    assert fake() == 7 and stamp().year >= 2020
