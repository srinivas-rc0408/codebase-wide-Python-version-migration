from pkg.core import fake, stamp


def test_both() -> None:
    assert fake() == 42 and stamp().year >= 2020
