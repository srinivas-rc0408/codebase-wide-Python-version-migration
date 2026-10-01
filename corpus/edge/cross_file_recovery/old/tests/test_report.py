from pkg.report import age_seconds


def test_age_is_small() -> None:
    assert -5 < age_seconds() < 5
