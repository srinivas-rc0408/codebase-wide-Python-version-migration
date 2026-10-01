from pkg.core import Clock


def test_clock() -> None:
    assert Clock.created.year >= 2020 and Clock.now() >= Clock.created
