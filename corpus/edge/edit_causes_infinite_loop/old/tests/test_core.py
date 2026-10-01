from datetime import datetime as D

from pkg.core import wait_for


def test_wait() -> None:
    wait_for(D(2000, 1, 1))
