from pkg.a import a_age
from pkg.b import b_age


def test_cycle() -> None:
    assert abs(a_age()) < 5
    assert abs(b_age()) < 5
