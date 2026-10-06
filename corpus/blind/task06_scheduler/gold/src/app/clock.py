"""The scheduler's wall clock."""

from datetime import datetime as DT
from datetime import timezone


def now():
    return DT.now(timezone.utc)
