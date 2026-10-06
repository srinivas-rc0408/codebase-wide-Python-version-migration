from app.report import age_days


def test_age_days_is_non_negative_int() -> None:
    days = age_days()
    assert isinstance(days, int)
    assert days >= 0
