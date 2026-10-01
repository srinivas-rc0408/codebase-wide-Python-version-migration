from pkg.core import stamp


def test_stamp_is_recent() -> None:
    assert stamp().year >= 2020
