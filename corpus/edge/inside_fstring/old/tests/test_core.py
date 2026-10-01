from pkg.core import label


def test_label() -> None:
    assert label().startswith("at 20")
