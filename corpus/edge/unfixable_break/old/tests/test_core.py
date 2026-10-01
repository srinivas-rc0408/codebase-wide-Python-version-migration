from pkg.core import stamp


def test_naive_contract() -> None:
    assert stamp().tzinfo is None
