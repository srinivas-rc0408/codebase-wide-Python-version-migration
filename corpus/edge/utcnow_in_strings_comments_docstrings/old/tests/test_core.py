from pkg.core import HELP, stamp


def test_text_untouched() -> None:
    assert "datetime.utcnow()" in HELP and stamp().year >= 2020
