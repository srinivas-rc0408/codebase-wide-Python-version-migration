"""The scheduler's wall clock."""

from datetime import datetime as DT


def now():
    return DT.utcnow()
