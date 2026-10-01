from pkg.report import age


def test_age() -> None:
    assert abs(age()) < 5
