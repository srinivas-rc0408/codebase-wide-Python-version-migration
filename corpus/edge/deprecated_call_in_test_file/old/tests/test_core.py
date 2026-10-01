from datetime import datetime

from pkg.core import stamp


def test_close_to_now() -> None:
    assert abs((stamp().replace(tzinfo=None) - datetime.utcnow()).total_seconds()) < 5
